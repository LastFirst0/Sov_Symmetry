"""Validate claims and limitations before documentation or release promotion."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTER = ROOT / "data" / "claim_limitations.json"
CLASSES = {"tested_contract", "mathematical_definition", "formal_reference", "empirical_packet", "external_analysis_receipt", "research_hypothesis", "interpretation"}
APPROVALS = {"draft", "candidate", "approved", "archival", "rejected"}
REQUIRED = {"claim_id", "claim_class", "title", "source", "scope", "owner_role", "version", "approval_state", "limitation"}


def validate(path: Path = REGISTER) -> dict:
    record = json.loads(path.read_text(encoding="utf-8"))
    if record.get("schema") != "sov.claim_limitation_register" or record.get("schema_version") != "0.1.0":
        raise ValueError("E_CLAIM_REGISTER_SCHEMA")
    seen = set()
    for index, claim in enumerate(record.get("claims", [])):
        missing = REQUIRED - set(claim)
        if missing or not all(isinstance(claim[key], str) and claim[key].strip() for key in REQUIRED):
            raise ValueError(f"E_CLAIM_REGISTER_FIELDS:{index}:{','.join(sorted(missing))}")
        if claim["claim_id"] in seen:
            raise ValueError(f"E_CLAIM_REGISTER_DUPLICATE:{claim['claim_id']}")
        seen.add(claim["claim_id"])
        if claim["claim_class"] not in CLASSES:
            raise ValueError(f"E_CLAIM_REGISTER_CLASS:{claim['claim_id']}")
        if claim["approval_state"] not in APPROVALS:
            raise ValueError(f"E_CLAIM_REGISTER_APPROVAL:{claim['claim_id']}")
        if not (ROOT / claim["source"]).exists():
            raise ValueError(f"E_CLAIM_REGISTER_SOURCE:{claim['claim_id']}")
    if not seen:
        raise ValueError("E_CLAIM_REGISTER_EMPTY")
    return {"schema": "sov.claim_limitation_register_report", "version": "0.1.0", "claim_count": len(seen), "status": "verified"}


if __name__ == "__main__":
    print(json.dumps(validate(), sort_keys=True))
