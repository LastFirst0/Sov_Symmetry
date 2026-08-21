"""Offline verification of a release manifest bound to an Ed25519 DSSE attestation."""
from __future__ import annotations

import base64
import hashlib
import json
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

from .audit import dsse_pae
from .canonical import canonicalize

RELEASE_PAYLOAD_TYPE = "application/vnd.sovereign.release-attestation.v1+json"
ALLOWED_EXTERNAL_FILES = frozenset({"RELEASE_MANIFEST.json", "RELEASE_ATTESTATION.dsse.json", "release_verification_report.json"})


def _sha_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _canonical_sha(value: Mapping[str, Any]) -> str:
    return _sha_bytes(canonicalize(value))


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def release_statement(manifest: Mapping[str, Any], manifest_bytes: bytes) -> dict[str, Any]:
    files = manifest.get("files")
    if not isinstance(files, Mapping) or not files:
        raise ValueError("release manifest has no file digest map")
    release = manifest.get("release")
    boundary = manifest.get("boundary")
    if not isinstance(release, str) or not release or not isinstance(boundary, str) or not boundary:
        raise ValueError("release manifest is missing release or boundary")
    return {
        "schema": "sov.release_attestation_statement",
        "schema_version": "0.1.0",
        "release": release,
        "boundary": boundary,
        "manifest_sha256": _sha_bytes(manifest_bytes),
        "file_list_sha256": _canonical_sha(dict(files)),
        "matrix_stdout_sha256": _sha_bytes(str(manifest.get("verification_stdout", "")).encode("utf-8")),
    }


def _verify_manifest_files(bundle: Path, manifest: Mapping[str, Any]) -> tuple[bool, str | None, list[str]]:
    files = manifest.get("files")
    if not isinstance(files, Mapping) or not files:
        return False, "E_MANIFEST_SCHEMA", []
    listed = []
    for relative, expected in files.items():
        if not isinstance(relative, str) or not isinstance(expected, str) or len(expected) != 64:
            return False, "E_MANIFEST_SCHEMA", []
        path = bundle / relative
        if not path.is_file() or _sha_bytes(path.read_bytes()) != expected:
            return False, "E_MANIFEST_FILE_TAMPER", [relative]
        listed.append(relative)
    expected_paths = set(listed) | ALLOWED_EXTERNAL_FILES
    unexpected = sorted(str(path.relative_to(bundle)) for path in bundle.rglob("*") if path.is_file() and str(path.relative_to(bundle)) not in expected_paths)
    if unexpected:
        return False, "E_UNEXPECTED_FILE", unexpected
    return True, None, []


def _verify_envelope(envelope: Mapping[str, Any], policy: Mapping[str, Any], expected_statement: Mapping[str, Any]) -> dict[str, Any]:
    if envelope.get("payloadType") != RELEASE_PAYLOAD_TYPE:
        return {"status": "fail", "reason_code": "E_PAYLOAD_TYPE"}
    if policy.get("schema") != "sov.release_key_policy" or policy.get("schema_version") != "0.1.0":
        return {"status": "unverifiable", "reason_code": "E_POLICY_SCHEMA"}
    if policy.get("allowed_payload_type") != RELEASE_PAYLOAD_TYPE:
        return {"status": "unverifiable", "reason_code": "E_POLICY_PAYLOAD_TYPE"}
    signatures = envelope.get("signatures")
    if not isinstance(signatures, list) or len(signatures) != 1 or not isinstance(signatures[0], Mapping):
        return {"status": "fail", "reason_code": "E_SIGNATURE_COUNT"}
    signature = signatures[0]
    if signature.get("algorithm") != "ed25519":
        return {"status": "fail", "reason_code": "E_ALGORITHM"}
    keys = policy.get("keys")
    key = keys.get(signature.get("keyid")) if isinstance(keys, Mapping) else None
    if not isinstance(key, Mapping):
        return {"status": "fail", "reason_code": "E_KEY_UNKNOWN"}
    if key.get("state") != "active":
        return {"status": "fail", "reason_code": "E_KEY_REVOKED"}
    try:
        payload = base64.b64decode(str(envelope["payload"]), validate=True)
        public_key = base64.b64decode(str(key["public_key"]), validate=True)
        raw_signature = base64.b64decode(str(signature["sig"]), validate=True)
        Ed25519PublicKey.from_public_bytes(public_key).verify(raw_signature, dsse_pae(RELEASE_PAYLOAD_TYPE, payload))
        statement = json.loads(payload.decode("utf-8"))
    except (KeyError, ValueError, TypeError, UnicodeDecodeError, json.JSONDecodeError):
        return {"status": "fail", "reason_code": "E_ENVELOPE_MALFORMED"}
    except InvalidSignature:
        return {"status": "fail", "reason_code": "E_SIGNATURE_INVALID"}
    if statement != dict(expected_statement):
        return {"status": "fail", "reason_code": "E_STATEMENT_MISMATCH"}
    return {"status": "verified", "reason_code": None, "key_id": signature["keyid"], "policy_id": policy.get("policy_id")}


def verify_release_artifact(bundle_dir: str | Path, *, policy_path: str | Path | None = None, attestation_path: str | Path | None = None) -> dict[str, Any]:
    """Return a terminal offline verification report; never fetch keys or network material."""
    bundle = Path(bundle_dir)
    manifest_path = bundle / "RELEASE_MANIFEST.json"
    if not manifest_path.is_file():
        return {"schema": "sov.release_verification_report", "schema_version": "0.1.0", "status": "unverifiable", "reason_code": "E_MANIFEST_MISSING", "scope": "No release manifest was available."}
    try:
        manifest_bytes = manifest_path.read_bytes()
        manifest = json.loads(manifest_bytes.decode("utf-8"))
        integrity, reason, affected = _verify_manifest_files(bundle, manifest)
        statement = release_statement(manifest, manifest_bytes)
    except (OSError, ValueError, TypeError, json.JSONDecodeError):
        return {"schema": "sov.release_verification_report", "schema_version": "0.1.0", "status": "fail", "reason_code": "E_MANIFEST_MALFORMED", "scope": "The manifest cannot be parsed or bound."}
    base = {
        "schema": "sov.release_verification_report",
        "schema_version": "0.1.0",
        "release": manifest.get("release"),
        "manifest_sha256": _sha_bytes(manifest_bytes),
        "file_list_sha256": statement["file_list_sha256"],
        "checked_file_count": len(manifest["files"]),
        "scope": "Offline release identity, listed-file binding, DSSE attestation, and public-key policy only; not scientific validity or operational key custody.",
    }
    if not integrity:
        return {**base, "status": "fail", "reason_code": reason, "affected_paths": affected}
    policy_file = Path(policy_path) if policy_path else bundle / "policies" / "release_key_policy.v0.1.json"
    attestation_file = Path(attestation_path) if attestation_path else bundle / "RELEASE_ATTESTATION.dsse.json"
    if not policy_file.is_file():
        return {**base, "status": "unverifiable", "reason_code": "E_POLICY_MISSING"}
    if not attestation_file.is_file():
        return {**base, "status": "unverifiable", "reason_code": "E_ATTESTATION_MISSING", "policy_path": str(policy_file)}
    try:
        result = _verify_envelope(_read_json(attestation_file), _read_json(policy_file), statement)
    except (OSError, json.JSONDecodeError):
        result = {"status": "fail", "reason_code": "E_ATTESTATION_OR_POLICY_MALFORMED"}
    return {**base, **result, "policy_path": str(policy_file), "attestation_path": str(attestation_file)}
