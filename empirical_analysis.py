"""Versioned binding between an empirical packet and an external method receipt.

This boundary validates declared lineage and execution metadata. It does not
assess the scientific conclusion expressed by a method output.
"""
from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from .empirical import parse_empirical_claim_packet
from .errors import CoreContractError

_SCHEMA = "sov.empirical_analysis_receipt"
_VERSION = "0.1.0"
_EXECUTION = {"completed", "failed", "not_run"}
_REVIEW = {"pending", "approved", "rejected", "not_required"}


def _error(code: str, message: str, path: str) -> None:
    raise CoreContractError(code, message, path=path)


def _mapping(value: Any, path: str) -> dict[str, Any]:
    if not isinstance(value, Mapping):
        _error("E_ANALYSIS_RECEIPT_SCHEMA", "must be an object", path)
    return dict(value)


def _string(value: Any, path: str) -> str:
    if not isinstance(value, str) or not value.strip():
        _error("E_ANALYSIS_RECEIPT_SCHEMA", "must be a non-empty string", path)
    return value


def _string_list(value: Any, path: str) -> list[str]:
    if not isinstance(value, list) or not value or not all(isinstance(item, str) and item.strip() for item in value):
        _error("E_ANALYSIS_RECEIPT_SCHEMA", "must be a non-empty list of strings", path)
    return list(value)


def parse_empirical_analysis_receipt(receipt: Mapping[str, Any], packet: Mapping[str, Any]) -> dict[str, Any]:
    """Validate a method receipt and bind it to a validated empirical packet."""
    declared_packet = parse_empirical_claim_packet(packet)
    normalized = _mapping(receipt, "analysis_receipt")
    if normalized.get("schema") != _SCHEMA or normalized.get("schema_version") != _VERSION:
        _error("E_ANALYSIS_RECEIPT_SCHEMA", "unsupported analysis receipt schema or version", "schema")
    for key in ("receipt_id", "packet_id", "claim_id"):
        _string(normalized.get(key), key)
    if normalized["packet_id"] != declared_packet["packet_id"] or normalized["claim_id"] != declared_packet["claim_id"]:
        _error("E_ANALYSIS_RECEIPT_LINEAGE", "packet_id and claim_id must match the bound packet", "packet_id")
    method = _mapping(normalized.get("method"), "method")
    binding = declared_packet["analysis_binding"]
    for key in ("method_id", "protocol_version", "software_id", "software_version", "environment_digest"):
        _string(method.get(key), f"method.{key}")
    if method["method_id"] != binding["method_id"] or method["protocol_version"] != binding["protocol_version"]:
        _error("E_ANALYSIS_RECEIPT_LINEAGE", "method identity must match analysis_binding", "method")
    datasets = normalized.get("datasets")
    if not isinstance(datasets, list) or not datasets:
        _error("E_ANALYSIS_RECEIPT_LINEAGE", "requires at least one bound dataset", "datasets")
    packet_datasets = {(item["dataset_id"], item["version"], item["content_sha256"]) for item in declared_packet["datasets"]}
    receipt_datasets = set()
    for index, item in enumerate(datasets):
        dataset = _mapping(item, f"datasets[{index}]")
        for key in ("dataset_id", "version"):
            _string(dataset.get(key), f"datasets[{index}].{key}")
        digest = dataset.get("content_sha256")
        if digest is not None and (not isinstance(digest, str) or len(digest) != 64):
            _error("E_ANALYSIS_RECEIPT_LINEAGE", "content_sha256 must be a SHA-256 digest or null", f"datasets[{index}].content_sha256")
        receipt_datasets.add((dataset["dataset_id"], dataset["version"], digest))
    if receipt_datasets != packet_datasets:
        _error("E_ANALYSIS_RECEIPT_LINEAGE", "receipt datasets must exactly match packet datasets", "datasets")
    if not isinstance(normalized.get("parameters"), Mapping):
        _error("E_ANALYSIS_RECEIPT_SCHEMA", "parameters must be an object", "parameters")
    output = _mapping(normalized.get("output"), "output")
    for key in ("schema", "content_sha256"):
        _string(output.get(key), f"output.{key}")
    if output["schema"] != binding["output_schema"]:
        _error("E_ANALYSIS_RECEIPT_LINEAGE", "output schema must match analysis_binding", "output.schema")
    _string_list(normalized.get("assumptions"), "assumptions")
    _string_list(normalized.get("limitations"), "limitations")
    if normalized.get("execution_status") not in _EXECUTION:
        _error("E_ANALYSIS_RECEIPT_SCHEMA", f"execution_status must be one of {sorted(_EXECUTION)}", "execution_status")
    if normalized.get("review_status") not in _REVIEW:
        _error("E_ANALYSIS_RECEIPT_SCHEMA", f"review_status must be one of {sorted(_REVIEW)}", "review_status")
    if binding["review_required"] and normalized["review_status"] == "not_required":
        _error("E_ANALYSIS_RECEIPT_REVIEW", "packet requires review; receipt cannot mark review not_required", "review_status")
    _string(normalized.get("scope"), "scope")
    _string_list(normalized.get("non_claims"), "non_claims")
    if "scientific_conclusion" in normalized or "truth_verdict" in normalized:
        _error("E_ANALYSIS_RECEIPT_SCOPE", "analysis receipt cannot contain a scientific truth verdict", "analysis_receipt")
    return normalized


def empirical_evidence_status(packet: Mapping[str, Any], receipt: Mapping[str, Any] | None = None) -> dict[str, Any]:
    """Return a scoped status while preserving the no-inference boundary."""
    declared = parse_empirical_claim_packet(packet)
    if receipt is None:
        return {"packet_id": declared["packet_id"], "status": "unverifiable", "reason_code": "E_EMPIRICAL_ANALYSIS_EXTERNAL", "analysis_receipt": "absent", "next_action": "Attach a versioned external analysis receipt.", "scope": "No empirical truth verdict is made."}
    bound = parse_empirical_analysis_receipt(receipt, declared)
    return {"packet_id": declared["packet_id"], "status": "unverifiable", "reason_code": "E_EMPIRICAL_INTERPRETATION_EXTERNAL", "analysis_receipt": "bound", "execution_status": bound["execution_status"], "review_status": bound["review_status"], "next_action": "Interpret the external result within its method, assumptions, limitations, and applicable review process.", "scope": "The receipt verifies declared lineage and execution metadata, not an empirical truth verdict."}
