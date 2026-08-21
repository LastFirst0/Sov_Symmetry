"""Populate expected IDs in the contract fixture pack using the reference SDK.

Run only when the canonical fixture body changes.  This is a generation utility;
the committed tests independently recompute every derived ID.
"""

from __future__ import annotations

import json
from pathlib import Path

from sov_evidence_geometry_core.canonical import derive_evidence_id, derive_id


ROOT = Path(__file__).resolve().parents[1]
SOURCE_FIXTURE_PATH = Path("/home/ubuntu/projects/sov-e4e91854/fixtures/sov_core_v0_1_fixture_pack.json")
DESTINATION_FIXTURE_PATH = ROOT / "tests" / "core_contract" / "data" / "sov_core_v0_1_fixture_pack.json"


def replace_known_ids(value: object, substitutions: dict[str, str]) -> object:
    if isinstance(value, str):
        return substitutions.get(value, value)
    if isinstance(value, list):
        return [replace_known_ids(item, substitutions) for item in value]
    if isinstance(value, dict):
        return {key: replace_known_ids(item, substitutions) for key, item in value.items()}
    return value


def main() -> None:
    pack = json.loads(SOURCE_FIXTURE_PATH.read_text(encoding="utf-8"))
    substitutions: dict[str, str] = {}
    for fixture in pack["fixtures"]:
        record = fixture["input"].get("core_record")
        if record is None:
            continue
        original_id = record["id"]
        record = replace_known_ids(record, substitutions)
        fixture["input"]["core_record"] = record
        if record.get("schema") == "sov.core.evidence":
            object_id = derive_evidence_id(record)
            record["id"] = object_id
            record["canonical_body_hash"] = object_id
        else:
            object_id = derive_id(record["canonical_body"])
            record["id"] = object_id
        substitutions[original_id] = object_id
        fixture["expected"]["canonical_id"] = object_id
    DESTINATION_FIXTURE_PATH.write_text(json.dumps(pack, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"updated {DESTINATION_FIXTURE_PATH}")


if __name__ == "__main__":
    main()
