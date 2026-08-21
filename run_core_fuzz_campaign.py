"""Deterministic cross-language and durable-store fuzz campaign.

The campaign is intentionally dependency-light and records minimized examples
for every mismatch. It does not claim a cryptographic proof of SHA-256
collision resistance; it searches for implementation-induced identity errors.
"""

from __future__ import annotations

import json
import os
import random
import shutil
import subprocess
import tempfile
import time
from pathlib import Path
from typing import Any

from sov_evidence_geometry_core import derive_id
from sov_evidence_geometry_core.canonical import canonicalize
from sov_evidence_geometry_core.errors import CoreContractError
from sov_evidence_geometry_core.persistence import FileObjectStore

ROOT = Path(__file__).resolve().parents[1]
RUST_BIN = ROOT / "target" / "debug" / "parity_cli"
SEEDS = [0x534F565F5231, 0x534F565F5232, 0x534F565F5031]


def random_string(rng: random.Random, length: int) -> str:
    alphabet = "abcXYZ012-_" + "éΩ中"
    return "".join(rng.choice(alphabet) for _ in range(length))


def random_value(rng: random.Random, depth: int = 0) -> Any:
    choices = ["null", "bool", "int", "string"] if depth >= 5 else ["null", "bool", "int", "string", "array", "object"]
    kind = rng.choice(choices)
    if kind == "null":
        return None
    if kind == "bool":
        return bool(rng.randrange(2))
    if kind == "int":
        return rng.choice([-9007199254740992, -9007199254740991, -1, 0, 1, 9007199254740991, 9007199254740992, rng.randrange(-100000, 100000)])
    if kind == "string":
        return random_string(rng, rng.randrange(0, 12))
    if kind == "array":
        return [random_value(rng, depth + 1) for _ in range(rng.randrange(0, 6))]
    keys = [random_string(rng, rng.randrange(1, 7)) for _ in range(rng.randrange(0, 6))]
    return {key: random_value(rng, depth + 1) for key in keys}


def rust_canonical_campaign(count: int) -> dict[str, Any]:
    if not RUST_BIN.exists():
        raise RuntimeError(f"missing Rust CLI: {RUST_BIN}")
    cases: list[Any] = []
    for seed in SEEDS[:2]:
        rng = random.Random(seed)
        cases.extend(random_value(rng) for _ in range(count // 2))
    started = time.monotonic()
    process = subprocess.Popen([str(RUST_BIN)], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
    assert process.stdin is not None and process.stdout is not None
    mismatches: list[dict[str, Any]] = []
    accepted = rejected = 0
    seen_ids: dict[str, bytes] = {}
    for index, value in enumerate(cases):
        process.stdin.write(json.dumps({"value": value}, ensure_ascii=False, separators=(",", ":")) + "\n")
        process.stdin.flush()
        raw = process.stdout.readline()
        if not raw:
            mismatches.append({"case": index, "kind": "rust_process_terminated", "value": value})
            break
        rust = json.loads(raw)
        try:
            python_bytes = canonicalize(value)
            python_id = derive_id(value)
            accepted += 1
            expected = {"ok": True, "canonical_hex": python_bytes.hex(), "id": python_id}
            prior = seen_ids.get(python_id)
            if prior is not None and prior != python_bytes:
                mismatches.append({"case": index, "kind": "python_identity_collision", "id": python_id, "value": value})
            seen_ids[python_id] = python_bytes
        except CoreContractError as error:
            rejected += 1
            expected = {"ok": False, "code": error.code}
        if rust.get("ok") != expected.get("ok") or (rust.get("ok") and (rust.get("canonical_hex"), rust.get("id")) != (expected.get("canonical_hex"), expected.get("id"))) or (not rust.get("ok") and rust.get("code") != expected.get("code")):
            mismatches.append({"case": index, "kind": "rust_python_mismatch", "value": value, "expected": expected, "observed": rust})
    process.stdin.close()
    process.wait(timeout=10)
    return {"cases": len(cases), "accepted": accepted, "rejected": rejected, "unique_ids": len(seen_ids), "mismatches": mismatches, "seconds": round(time.monotonic() - started, 3)}


def record(number: int) -> dict[str, Any]:
    body = {
        "schema": "sov.core.object",
        "schema_version": "0.1.0",
        "object_kind": "manifold",
        "convention_profile": {
            "id": "convention:standard.v1",
            "curvature_sign": "RhoSigmaMuNu_v1",
            "metric_signature_order": "positive_negative_zero",
            "index_notation": "einstein_ascii_v1",
            "scalar_policy": "exact_only",
            "coordinate_basis": "coordinate_basis_required",
            "unit_policy": "dimensionless_only",
            "tolerance_policy": "tolerance:exact.v1",
        },
        "assumptions": [],
        "content": {"name": f"M{number}", "dimension": (number % 8) + 1, "orientation_mode": "declared", "signature": {"positive": (number % 8) + 1, "negative": 0, "zero": 0}},
    }
    return {"id": derive_id(body), "canonical_body": body}


def durable_store_campaign(count: int) -> dict[str, Any]:
    started = time.monotonic()
    errors: list[dict[str, Any]] = []
    idempotent_cases = collision_cases = manifest_cases = 0
    with tempfile.TemporaryDirectory() as directory:
        store = FileObjectStore(directory)
        records = [record(index) for index in range(count)]
        for item in records:
            store.put(item)
        before = len(store.manifest_entries())
        for item in records:
            store.put(item)
        after = len(store.manifest_entries())
        idempotent_cases = count if before == after == count else 0
        try:
            store.verify_manifest()
        except Exception as error:  # pragma: no cover - campaign report path
            errors.append({"kind": "clean_replay_failure", "error": repr(error)})
        with tempfile.TemporaryDirectory() as tamper_directory:
            local = FileObjectStore(tamper_directory)
            item = records[0]
            object_id = local.put(item)
            for index in range(250):
                object_path = local._path(object_id)
                original = object_path.read_bytes()
                object_path.write_bytes(original + (b" " if index % 2 == 0 else b"x"))
                try:
                    local.verify_manifest()
                    errors.append({"kind": "tamper_accepted", "case": index})
                except (CoreContractError, json.JSONDecodeError):
                    collision_cases += 1
                object_path.write_bytes(original)
            local.verify_manifest()
            original_manifest = local.manifest.read_bytes()
            for index in range(250):
                local.manifest.write_bytes(original_manifest + (b"{\"schema\":\"corrupt\"}\n" if index % 2 == 0 else b"{"))
                try:
                    local.verify_manifest()
                    errors.append({"kind": "manifest_corruption_accepted", "case": index})
                except (CoreContractError, json.JSONDecodeError):
                    manifest_cases += 1
            local.manifest.write_bytes(original_manifest)
            local.verify_manifest()
        for malformed in ["", "sov", "sov:sha256", "sov:sha256:xyz", "other:sha256:" + "a" * 64, "sov:sha256:" + "../" + "a" * 61]:
            try:
                path = store._path(malformed)
                if not path.resolve().is_relative_to(store.objects.resolve()):
                    errors.append({"kind": "path_escape", "value": malformed, "path": str(path)})
            except CoreContractError:
                pass
        manifest_root = store.verify_manifest()
    return {"valid_records": count, "idempotent_cases": idempotent_cases, "tamper_rejection_cases": collision_cases, "manifest_corruption_rejection_cases": manifest_cases, "manifest_root": manifest_root, "errors": errors, "seconds": round(time.monotonic() - started, 3)}


def main() -> None:
    if len(os.sys.argv) != 2:
        raise SystemExit("usage: run_core_fuzz_campaign.py REPORT.json")
    report_path = Path(os.sys.argv[1])
    report = {"schema": "sov.fuzz.campaign.report", "version": "0.1.0", "seeds": SEEDS, "rust_canonical": rust_canonical_campaign(10000), "python_store": durable_store_campaign(1000)}
    report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"rust": report["rust_canonical"], "store": {key: value for key, value in report["python_store"].items() if key not in {"manifest_root"}}}, indent=2))
    if report["rust_canonical"]["mismatches"] or report["python_store"]["errors"]:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
