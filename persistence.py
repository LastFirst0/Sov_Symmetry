"""Durable local storage for immutable Core Contract records.

This is a local, single-writer reference store. It does not claim WORM media,
distributed replication, public transparency, or key-backed attestations.
"""

from __future__ import annotations

import hashlib
import os
import re
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from .canonical import canonicalize, parse_strict_json
from .errors import CoreContractError
from .validation import validate_core_record


class FileObjectStore:
    """Atomic, content-addressed, local persistence with a replayable manifest."""

    MANIFEST_NAME = "manifest.jsonl"

    def __init__(self, root: str | Path) -> None:
        self.root = Path(root)
        self.objects = self.root / "objects"
        self.objects.mkdir(parents=True, exist_ok=True)
        self.manifest = self.root / self.MANIFEST_NAME
        self.manifest.touch(exist_ok=True)

    @staticmethod
    def _digest_from_id(object_id: str) -> str:
        try:
            prefix, algorithm, digest = object_id.split(":", 2)
        except ValueError as exc:
            raise CoreContractError("E_SCHEMA_INVALID", "malformed content identifier") from exc
        if prefix != "sov" or algorithm != "sha256" or not re.fullmatch(r"[0-9a-f]{64}", digest):
            raise CoreContractError("E_SCHEMA_INVALID", "unsupported content identifier")
        return digest

    def _path(self, object_id: str) -> Path:
        digest = self._digest_from_id(object_id)
        return self.objects / digest[:2] / f"{digest}.json"

    @staticmethod
    def _record_hash(record: Mapping[str, Any]) -> str:
        return "sha256:" + hashlib.sha256(canonicalize(record)).hexdigest()

    @staticmethod
    def _atomic_write(path: Path, payload: bytes) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        temporary = path.with_suffix(path.suffix + f".tmp.{os.getpid()}")
        descriptor = os.open(temporary, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
        try:
            with os.fdopen(descriptor, "wb") as handle:
                handle.write(payload)
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(temporary, path)
            directory = os.open(path.parent, os.O_RDONLY)
            try:
                os.fsync(directory)
            finally:
                os.close(directory)
        finally:
            if temporary.exists():
                temporary.unlink(missing_ok=True)

    def _append_manifest(self, entry: Mapping[str, Any]) -> None:
        payload = canonicalize(entry) + b"\n"
        with self.manifest.open("ab") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())

    def put(self, record: Mapping[str, Any]) -> str:
        normalized = validate_core_record(record, resolver=self.get)
        object_id = normalized["id"]
        payload = canonicalize(normalized)
        path = self._path(object_id)
        if path.exists():
            if path.read_bytes() != payload:
                raise CoreContractError("E_ID_MISMATCH", "same content ID maps to distinct durable bytes")
            return object_id
        self._atomic_write(path, payload)
        self._append_manifest(
            {
                "schema": "sov.local_manifest_entry",
                "schema_version": "0.1.0",
                "action": "put",
                "object_id": object_id,
                "record_hash": self._record_hash(normalized),
            }
        )
        return object_id

    def put_opaque(self, record: Mapping[str, Any]) -> str:
        object_id = record.get("id")
        if not isinstance(object_id, str) or not object_id.startswith("sov:sha256:"):
            raise CoreContractError("E_SCHEMA_INVALID", "opaque record requires a sov content ID")
        if record.get("schema") not in {"sov.quorum.durable_record", "sov.local_audit_artifact"}:
            raise CoreContractError("E_SCHEMA_INVALID", "unsupported opaque record schema")
        payload = canonicalize(record); path = self._path(object_id)
        if path.exists():
            if path.read_bytes() != payload: raise CoreContractError("E_ID_MISMATCH", "same opaque ID maps to distinct bytes")
            return object_id
        self._atomic_write(path, payload)
        self._append_manifest({"schema":"sov.local_manifest_entry","schema_version":"0.1.0","action":"put_opaque","object_id":object_id,"record_hash":self._record_hash(record)})
        return object_id

    def get(self, object_id: str) -> dict[str, Any]:
        path = self._path(object_id)
        if not path.exists():
            raise CoreContractError("E_REFERENCE_MISSING", f"unknown object {object_id}")
        try:
            raw_bytes = path.read_bytes()
            raw = parse_strict_json(raw_bytes.decode("utf-8"))
        except (OSError, UnicodeDecodeError) as exc:
            raise CoreContractError("E_AUDIT_TAMPER", f"unable to read stored object {object_id}") from exc
        if not isinstance(raw, dict) or canonicalize(raw) != raw_bytes:
            raise CoreContractError("E_AUDIT_TAMPER", "stored object bytes are not canonical")
        return raw

    def manifest_entries(self) -> list[dict[str, Any]]:
        entries: list[dict[str, Any]] = []
        for line_number, line in enumerate(self.manifest.read_text(encoding="utf-8").splitlines(), start=1):
            if not line:
                continue
            entry = parse_strict_json(line)
            if not isinstance(entry, dict):
                raise CoreContractError("E_AUDIT_TAMPER", f"manifest entry {line_number} is not an object")
            entries.append(entry)
        return entries

    def manifest_root(self) -> str:
        return "sha256:" + hashlib.sha256(canonicalize(self.manifest_entries())).hexdigest()

    def verify_manifest(self) -> str:
        seen: set[str] = set()
        for entry in self.manifest_entries():
            if entry.get("action") not in {"put", "put_opaque"}:
                raise CoreContractError("E_AUDIT_TAMPER", "unsupported local manifest action")
            object_id = entry.get("object_id")
            if not isinstance(object_id, str) or object_id in seen:
                raise CoreContractError("E_AUDIT_TAMPER", "manifest has missing or duplicate object identity")
            seen.add(object_id)
            record = self.get(object_id)
            if self._record_hash(record) != entry.get("record_hash"):
                raise CoreContractError("E_AUDIT_TAMPER", "stored object does not match manifest hash")
            if entry.get("action") == "put":
                validate_core_record(record, resolver=self.get)
            elif record.get("schema") not in {"sov.quorum.durable_record", "sov.local_audit_artifact"} or record.get("schema_version") != "0.1.0":
                raise CoreContractError("E_AUDIT_TAMPER", "opaque record has an invalid schema boundary")
        return self.manifest_root()
