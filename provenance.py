"""Replayable provenance and optional local advanced evidence for simple receipts."""
from __future__ import annotations
from collections.abc import Mapping
from typing import Any
from .errors import CoreContractError
from .simple import check_identity_matrix, check_matrix_inverse, check_symmetric_matrix

_CHECKS = {
    "matrix.symmetric.v1": lambda p: check_symmetric_matrix(p["input"]),
    "matrix.identity.v1": lambda p: check_identity_matrix(p["input"]),
    "matrix.inverse.v1": lambda p: check_matrix_inverse(p["left"], p["right"]),
}

def receipt_bundle(receipt: Mapping[str, Any], *, assurance: Mapping[str, Any] | None = None) -> dict[str, Any]:
    provenance = receipt.get("provenance")
    if not isinstance(provenance, Mapping) or not isinstance(provenance.get("check"), str):
        raise CoreContractError("E_SCHEMA_INVALID", "receipt lacks replayable provenance")
    bundle = {"schema": "sov.receipt_bundle", "schema_version": "0.1.0", "receipt": dict(receipt), "provenance": dict(provenance)}
    if assurance is not None:
        bundle["advanced_assurance"] = dict(assurance)
    return bundle

def replay_receipt_bundle(bundle: Mapping[str, Any]) -> dict[str, Any]:
    if bundle.get("schema") != "sov.receipt_bundle" or bundle.get("schema_version") != "0.1.0":
        raise CoreContractError("E_SCHEMA_INVALID", "unsupported receipt bundle")
    receipt, provenance = bundle.get("receipt"), bundle.get("provenance")
    if not isinstance(receipt, Mapping) or not isinstance(provenance, Mapping):
        raise CoreContractError("E_SCHEMA_INVALID", "receipt bundle requires receipt and provenance")
    check = provenance.get("check")
    evaluator = _CHECKS.get(check)
    if evaluator is None:
        return {"status": "unverifiable", "reason_code": "E_OPERATION_UNKNOWN", "message": "This receipt uses a check that this replay tool does not support."}
    recomputed = evaluator(provenance)
    if recomputed["receipt_id"] != receipt.get("receipt_id"):
        return {"status": "fail", "reason_code": "E_ID_MISMATCH", "message": "The receipt does not match its declared provenance.", "recomputed_receipt": recomputed}
    return {"status": "verified", "receipt_id": recomputed["receipt_id"], "message": "The receipt was replayed from its declared provenance."}

def advanced_evidence_export(bundle: Mapping[str, Any]) -> dict[str, Any]:
    replay = replay_receipt_bundle(bundle)
    assurance = bundle.get("advanced_assurance")
    return {"schema": "sov.advanced_evidence_export", "schema_version": "0.1.0", "receipt_replay": replay, "assurance_status": "recorded" if isinstance(assurance, Mapping) else "not_recorded", "advanced_assurance": dict(assurance) if isinstance(assurance, Mapping) else None, "scope": "Local export only. Any signature, quorum, or Merkle field is evidence only when explicitly recorded; absent fields do not imply trust."}
