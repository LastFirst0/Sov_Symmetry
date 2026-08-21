"""Fail-closed reference parser for versioned empirical claim packets.

This module validates declared evidence structure and returns no empirical truth verdict.
It intentionally leaves analysis of an empirical statement to a separately bound method.
"""
from __future__ import annotations

import math
from collections.abc import Mapping
from typing import Any

from .errors import CoreContractError

_SCHEMA = "sov.empirical_claim_packet"
_VERSION = "0.1.0"
_STATES = {"draft", "described", "bound", "executed", "reviewed", "withdrawn"}
_ACCESS = {"open", "restricted", "unavailable"}
_UNCERTAINTY = {"measurement", "sampling", "model", "mixed", "unknown"}


def _error(code: str, message: str, path: str) -> None:
    raise CoreContractError(code, message, path=path)


def _mapping(value: Any, path: str, code: str = "E_EMPIRICAL_SCHEMA") -> dict[str, Any]:
    if not isinstance(value, Mapping):
        _error(code, "must be an object", path)
    return dict(value)


def _string(value: Any, path: str, code: str = "E_EMPIRICAL_SCHEMA") -> str:
    if not isinstance(value, str) or not value.strip():
        _error(code, "must be a non-empty string", path)
    return value


def _list(value: Any, path: str, code: str = "E_EMPIRICAL_SCHEMA") -> list[Any]:
    if not isinstance(value, list):
        _error(code, "must be an array", path)
    return value


def _number(value: Any, path: str, code: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(float(value)):
        _error(code, "must be a finite number", path)
    return float(value)


def _dataset(value: Any, path: str) -> dict[str, Any]:
    dataset = _mapping(value, path, "E_EMPIRICAL_PROVENANCE")
    for key in ("dataset_id", "version", "media_type", "license"):
        _string(dataset.get(key), f"{path}.{key}", "E_EMPIRICAL_PROVENANCE")
    if "content_sha256" not in dataset:
        _error("E_EMPIRICAL_PROVENANCE", "requires content_sha256 or an explicit null", f"{path}.content_sha256")
    digest = dataset["content_sha256"]
    if digest is not None and (not isinstance(digest, str) or len(digest) != 64 or any(char not in "0123456789abcdef" for char in digest.lower())):
        _error("E_EMPIRICAL_PROVENANCE", "must be a SHA-256 hex digest or null", f"{path}.content_sha256")
    access = _mapping(dataset.get("access"), f"{path}.access", "E_EMPIRICAL_PROVENANCE")
    if access.get("status") not in _ACCESS:
        _error("E_EMPIRICAL_PROVENANCE", f"status must be one of {sorted(_ACCESS)}", f"{path}.access.status")
    if access["status"] == "open":
        _string(access.get("locator"), f"{path}.access.locator", "E_EMPIRICAL_PROVENANCE")
    _string(access.get("access_conditions"), f"{path}.access.access_conditions", "E_EMPIRICAL_PROVENANCE")
    custodian = _mapping(dataset.get("custodian"), f"{path}.custodian", "E_EMPIRICAL_PROVENANCE")
    _string(custodian.get("id"), f"{path}.custodian.id", "E_EMPIRICAL_PROVENANCE")
    _string(custodian.get("role"), f"{path}.custodian.role", "E_EMPIRICAL_PROVENANCE")
    return dataset


def _uncertainty(value: Any) -> dict[str, Any]:
    uncertainty = _mapping(value, "uncertainty", "E_EMPIRICAL_UNCERTAINTY")
    if uncertainty.get("kind") not in _UNCERTAINTY:
        _error("E_EMPIRICAL_UNCERTAINTY", f"kind must be one of {sorted(_UNCERTAINTY)}", "uncertainty.kind")
    estimate = _mapping(uncertainty.get("estimate"), "uncertainty.estimate", "E_EMPIRICAL_UNCERTAINTY")
    _number(estimate.get("value"), "uncertainty.estimate.value", "E_EMPIRICAL_UNCERTAINTY")
    _string(estimate.get("unit"), "uncertainty.estimate.unit", "E_EMPIRICAL_UNCERTAINTY")
    components = _list(uncertainty.get("components"), "uncertainty.components", "E_EMPIRICAL_UNCERTAINTY")
    if uncertainty["kind"] != "unknown" and not components:
        _error("E_EMPIRICAL_UNCERTAINTY", "known uncertainty requires at least one component", "uncertainty.components")
    for index, component_raw in enumerate(components):
        component = _mapping(component_raw, f"uncertainty.components[{index}]", "E_EMPIRICAL_UNCERTAINTY")
        for key in ("id", "class", "description", "unit"):
            _string(component.get(key), f"uncertainty.components[{index}].{key}", "E_EMPIRICAL_UNCERTAINTY")
        _number(component.get("standard_uncertainty"), f"uncertainty.components[{index}].standard_uncertainty", "E_EMPIRICAL_UNCERTAINTY")
    _string(uncertainty.get("combination_method"), "uncertainty.combination_method", "E_EMPIRICAL_UNCERTAINTY")
    combined = _mapping(uncertainty.get("combined_standard_uncertainty"), "uncertainty.combined_standard_uncertainty", "E_EMPIRICAL_UNCERTAINTY")
    _number(combined.get("value"), "uncertainty.combined_standard_uncertainty.value", "E_EMPIRICAL_UNCERTAINTY")
    _string(combined.get("unit"), "uncertainty.combined_standard_uncertainty.unit", "E_EMPIRICAL_UNCERTAINTY")
    expanded = uncertainty.get("expanded_uncertainty")
    if expanded is not None:
        expanded = _mapping(expanded, "uncertainty.expanded_uncertainty", "E_EMPIRICAL_UNCERTAINTY")
        _number(expanded.get("value"), "uncertainty.expanded_uncertainty.value", "E_EMPIRICAL_UNCERTAINTY")
        coverage = _number(expanded.get("coverage_factor"), "uncertainty.expanded_uncertainty.coverage_factor", "E_EMPIRICAL_UNCERTAINTY")
        if coverage <= 0:
            _error("E_EMPIRICAL_UNCERTAINTY", "coverage_factor must be positive", "uncertainty.expanded_uncertainty.coverage_factor")
    interpretation = uncertainty.get("interval_or_confidence")
    if interpretation is not None:
        interpretation = _mapping(interpretation, "uncertainty.interval_or_confidence", "E_EMPIRICAL_UNCERTAINTY")
        _string(interpretation.get("statement"), "uncertainty.interval_or_confidence.statement", "E_EMPIRICAL_UNCERTAINTY")
        _string(interpretation.get("basis"), "uncertainty.interval_or_confidence.basis", "E_EMPIRICAL_UNCERTAINTY")
    return uncertainty


def parse_empirical_claim_packet(packet: Mapping[str, Any]) -> dict[str, Any]:
    """Parse and validate a packet; never infer or execute an empirical conclusion."""
    normalized = _mapping(packet, "packet")
    if normalized.get("schema") != _SCHEMA or normalized.get("schema_version") != _VERSION:
        _error("E_EMPIRICAL_SCHEMA", "unsupported empirical packet schema or version", "schema")
    for key in ("packet_id", "claim_id", "statement"):
        _string(normalized.get(key), key)
    if normalized.get("claim_class") != "empirical":
        _error("E_EMPIRICAL_CLASS", "claim_class must be empirical", "claim_class")
    if "framework_id" in normalized and normalized["framework_id"] is not None:
        _string(normalized["framework_id"], "framework_id")
    state = normalized.get("state", "draft")
    if state not in _STATES:
        _error("E_EMPIRICAL_STATE", f"state must be one of {sorted(_STATES)}", "state")
    target = _mapping(normalized.get("target_quantity"), "target_quantity")
    for key in ("name", "unit", "scope"):
        _string(target.get(key), f"target_quantity.{key}")
    datasets = _list(normalized.get("datasets"), "datasets", "E_EMPIRICAL_PROVENANCE")
    if not datasets:
        _error("E_EMPIRICAL_PROVENANCE", "requires at least one dataset", "datasets")
    for index, dataset in enumerate(datasets): _dataset(dataset, f"datasets[{index}]")
    provenance = _mapping(normalized.get("provenance"), "provenance", "E_EMPIRICAL_PROVENANCE")
    for key in ("entities", "activities", "agents", "derivations"):
        _list(provenance.get(key), f"provenance.{key}", "E_EMPIRICAL_PROVENANCE")
    _uncertainty(normalized.get("uncertainty"))
    binding = _mapping(normalized.get("analysis_binding"), "analysis_binding", "E_EMPIRICAL_ANALYSIS")
    for key in ("method_id", "protocol_version", "input_mapping", "output_schema"):
        _string(binding.get(key), f"analysis_binding.{key}", "E_EMPIRICAL_ANALYSIS")
    if not isinstance(binding.get("review_required"), bool):
        _error("E_EMPIRICAL_ANALYSIS", "review_required must be boolean", "analysis_binding.review_required")
    _mapping(normalized.get("governance"), "governance", "E_EMPIRICAL_GOVERNANCE")
    non_claims = _list(normalized.get("non_claims"), "non_claims")
    if not non_claims or not all(isinstance(item, str) and item.strip() for item in non_claims):
        _error("E_EMPIRICAL_SCHEMA", "requires at least one non-claim", "non_claims")
    if state in {"bound", "executed", "reviewed"} and not binding.get("method_id"):
        _error("E_EMPIRICAL_STATE", "bound or later state requires a method binding", "analysis_binding")
    return normalized


def empirical_kernel_outcome(packet: Mapping[str, Any]) -> dict[str, Any]:
    """Return the explicit core boundary for an empirical claim packet."""
    normalized = parse_empirical_claim_packet(packet)
    return {"packet_id": normalized["packet_id"], "status": "unverifiable", "reason_code": "E_EMPIRICAL_ANALYSIS_EXTERNAL", "plain_status": "Cannot be concluded by the structural kernel alone.", "next_action": "Run the separately versioned analysis_binding process and attach its scoped receipt.", "scope": "Packet validation checks evidence description and does not assess the empirical statement."}
