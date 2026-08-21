"""Fail-closed verifier for K1 shared conformance-fixture manifests."""
from __future__ import annotations
import hashlib, json
from pathlib import Path
from typing import Any, Mapping
from .errors import CoreContractError
EXPECTED_COUNTS = {"valid_object": 8, "invalid_request": 4, "unverifiable_result": 2, "failed_predicate": 1, "tamper": 1, "determinism": 1}
def verify_fixture_manifest(manifest_path: str | Path, repository_root: str | Path) -> dict[str, Any]:
    try: manifest = json.loads(Path(manifest_path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc: raise CoreContractError("E_AUDIT_TAMPER", "fixture manifest unreadable") from exc
    if not isinstance(manifest, Mapping) or manifest.get("schema") != "sov.fixture-manifest.v0" or manifest.get("schema_version") != "0.1.0-candidate": raise CoreContractError("E_SCHEMA_INVALID", "unsupported fixture manifest schema")
    entries = manifest.get("entries")
    if not isinstance(entries, list) or len(entries) != 1: raise CoreContractError("E_SCHEMA_INVALID", "manifest requires exactly one K1 fixture entry")
    entry = entries[0]
    if not isinstance(entry, Mapping) or not isinstance(entry.get("path"), str) or not isinstance(entry.get("sha256"), str): raise CoreContractError("E_SCHEMA_INVALID", "fixture entry missing path or digest")
    fixture_path = Path(repository_root) / entry["path"]
    try: raw = fixture_path.read_bytes(); pack = json.loads(raw.decode("utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc: raise CoreContractError("E_AUDIT_TAMPER", "fixture pack unreadable") from exc
    digest = hashlib.sha256(raw).hexdigest()
    if digest != entry["sha256"]: raise CoreContractError("E_AUDIT_TAMPER", "fixture pack digest mismatch")
    fixtures = pack.get("fixtures") if isinstance(pack, Mapping) else None
    if not isinstance(fixtures, list): raise CoreContractError("E_SCHEMA_INVALID", "fixture pack lacks fixtures")
    counts: dict[str, int] = {}
    for fixture in fixtures:
        category = fixture.get("category") if isinstance(fixture, Mapping) else None
        if not isinstance(category, str): raise CoreContractError("E_SCHEMA_INVALID", "fixture category missing")
        counts[category] = counts.get(category, 0) + 1
    if len(fixtures) != 17 or counts != EXPECTED_COUNTS or entry.get("fixtures") != 17 or entry.get("categories") != EXPECTED_COUNTS: raise CoreContractError("E_AUDIT_TAMPER", "fixture counts do not match K1 contract")
    return {"fixture_path": str(fixture_path), "sha256": digest, "fixture_count": len(fixtures), "categories": counts}
