"""Core Contract shape, identity, and semantic validation."""

from __future__ import annotations

from collections.abc import Callable, Mapping
from fractions import Fraction
from math import gcd
from typing import Any

from .canonical import derive_evidence_id, derive_id
from .errors import CoreContractError
from .schema import validate_schema

Resolver = Callable[[str], Mapping[str, Any]]


def _record_kind(record: Mapping[str, Any]) -> str:
    if record.get("schema") == "sov.core.evidence":
        return "evidence_record"
    body = record.get("canonical_body")
    if isinstance(body, Mapping):
        return str(body.get("object_kind", ""))
    return ""


def _body(record: Mapping[str, Any]) -> Mapping[str, Any]:
    body = record.get("canonical_body")
    if not isinstance(body, Mapping):
        raise CoreContractError("E_SCHEMA_INVALID", "object envelope lacks canonical_body")
    return body


def _resolve(resolver: Resolver | None, object_id: str, expected_kind: str | None = None) -> Mapping[str, Any]:
    if resolver is None:
        raise CoreContractError("E_REFERENCE_MISSING", f"resolver unavailable for {object_id}")
    record = resolver(object_id)
    if expected_kind and _record_kind(record) != expected_kind:
        raise CoreContractError("E_REFERENCE_KIND", f"{object_id} is {_record_kind(record)!r}, expected {expected_kind!r}")
    return record


def _validate_scalar(value: Any) -> None:
    if not isinstance(value, Mapping):
        return
    kind = value.get("kind")
    if kind == "rational":
        numerator = int(str(value["numerator"]))
        denominator = int(str(value["denominator"]))
        if denominator <= 0 or gcd(abs(numerator), denominator) != 1:
            raise CoreContractError("E_CANONICALIZATION", "rational scalar must be reduced with a positive denominator")
    if kind == "float64":
        bits = str(value["ieee754_be_hex"])
        exponent = int(bits[:3], 16) & 0x7FF
        if exponent == 0x7FF or bits == "8000000000000000":
            raise CoreContractError("E_CANONICALIZATION", "non-finite or negative-zero float64 is prohibited")


def _validate_expression(expression: Any) -> None:
    if not isinstance(expression, Mapping):
        return
    if "kind" in expression:
        _validate_scalar(expression)
        return
    for field in ("arguments", "terms", "factors"):
        for item in expression.get(field, []):
            _validate_expression(item)


def _validate_components(components: Mapping[str, Any], *, dimension: int, rank: int) -> None:
    mode = components["mode"]
    if mode == "symbolic":
        _validate_expression(components["expression"])
        return
    seen: set[tuple[int, ...]] = set()
    for component in components["components"]:
        indices = tuple(component["indices"])
        if len(indices) != rank or any(index >= dimension for index in indices):
            raise CoreContractError("E_INDEX_INVALID", "component indices do not match rank or manifold dimension")
        if indices in seen:
            raise CoreContractError("E_INDEX_INVALID", "duplicate sparse component index tuple")
        seen.add(indices)
        _validate_scalar(component["value"])


def _manifold_dimension(record: Mapping[str, Any]) -> int:
    return int(_body(record)["content"]["dimension"])


def _validate_object_semantics(record: Mapping[str, Any], resolver: Resolver | None) -> None:
    body = _body(record)
    kind = body["object_kind"]
    content = body["content"]
    if kind == "manifold":
        signature = content.get("signature")
        if signature and sum(signature.values()) != content["dimension"]:
            raise CoreContractError("E_DIMENSION_MISMATCH", "manifold signature entries must sum to manifold dimension")
        return
    if kind == "chart":
        manifold = _resolve(resolver, content["manifold_id"], "manifold")
        if len(content["coordinates"]) != _manifold_dimension(manifold):
            raise CoreContractError("E_DIMENSION_MISMATCH", "chart coordinate count must equal manifold dimension")
        return
    manifold = _resolve(resolver, content["manifold_id"], "manifold")
    dimension = _manifold_dimension(manifold)
    chart = _resolve(resolver, content["chart_id"], "chart")
    if _body(chart)["content"]["manifold_id"] != content["manifold_id"]:
        raise CoreContractError("E_REFERENCE_KIND", "chart and object reference different manifolds")
    if kind == "tensor":
        _validate_components(content["components"], dimension=dimension, rank=len(content["slots"]))
        for symmetry in content.get("symmetries", []):
            if any(slot >= len(content["slots"]) for slot in symmetry["slots"]):
                raise CoreContractError("E_INDEX_INVALID", "symmetry references an absent tensor slot")
        return
    if kind == "metric":
        signature = content["signature"]
        if sum(signature.values()) != dimension:
            raise CoreContractError("E_DIMENSION_MISMATCH", "metric signature must sum to manifold dimension")
        _validate_components(content["components"], dimension=dimension, rank=2)
        if content.get("inverse_metric_id"):
            _resolve(resolver, content["inverse_metric_id"])
        return
    if kind == "form":
        if content["degree"] > dimension:
            raise CoreContractError("E_DIMENSION_MISMATCH", "form degree exceeds manifold dimension")
        _validate_components(content["components"], dimension=dimension, rank=content["degree"])
        return
    if kind == "connection":
        if content["kind"] == "levi_civita" and not content.get("metric_id"):
            raise CoreContractError("E_REFERENCE_MISSING", "Levi-Civita connection requires metric_id")
        if content.get("metric_id"):
            metric = _resolve(resolver, content["metric_id"], "metric")
            if _body(metric)["content"]["manifold_id"] != content["manifold_id"]:
                raise CoreContractError("E_REFERENCE_KIND", "connection metric is defined on another manifold")
        _validate_components(content["coefficients"], dimension=dimension, rank=3)
        return
    if kind == "orientation":
        return
    raise CoreContractError("E_SCHEMA_INVALID", f"unsupported object kind {kind!r}")


def _validate_evidence_semantics(record: Mapping[str, Any], resolver: Resolver | None) -> None:
    derived = derive_evidence_id(record)
    if record["id"] != derived or record["canonical_body_hash"] != derived:
        raise CoreContractError("E_ID_MISMATCH", "evidence ID or canonical_body_hash differs from canonical evidence body")
    for object_id in [*record["input_ids"], *record["output_ids"]]:
        _resolve(resolver, object_id)
    outcomes = {result["outcome"] for result in record["predicate_results"]}
    status = record["status"]
    if status == "verified" and outcomes != {"pass"}:
        raise CoreContractError("E_SCHEMA_INVALID", "verified evidence requires all predicate outcomes to pass")
    if status == "fail" and "fail" not in outcomes:
        raise CoreContractError("E_SCHEMA_INVALID", "failed evidence requires at least one failed predicate")
    if status == "unverifiable" and "unverifiable" not in outcomes:
        raise CoreContractError("E_SCHEMA_INVALID", "unverifiable evidence requires at least one unverifiable predicate")


def validate_core_record(record: Mapping[str, Any], *, resolver: Resolver | None = None) -> dict[str, Any]:
    """Validate schema, derived identity, and semantic constraints for one core record."""

    normalized = dict(record)
    validate_schema("core", normalized)
    if normalized.get("schema") == "sov.core.evidence":
        _validate_evidence_semantics(normalized, resolver)
        return normalized
    body = _body(normalized)
    derived = derive_id(body)
    if normalized["id"] != derived:
        raise CoreContractError("E_ID_MISMATCH", "object ID differs from canonical body hash")
    _validate_object_semantics(normalized, resolver)
    return normalized


def validate_quarantine_packet(packet: Mapping[str, Any]) -> dict[str, Any]:
    """Validate a policy packet's strict shape; lifecycle interpretation remains policy-level."""

    normalized = dict(packet)
    validate_schema("quarantine", normalized)
    return normalized


def scalar_fraction(value: Mapping[str, Any]) -> Fraction:
    """Convert an exact scalar to Fraction or signal that evaluation is unsupported."""

    kind = value.get("kind")
    if kind == "integer":
        return Fraction(int(value["value"]), 1)
    if kind == "rational":
        return Fraction(int(value["numerator"]), int(value["denominator"]))
    raise CoreContractError("E_SCALAR_UNSUPPORTED", f"exact matrix predicate cannot evaluate scalar kind {kind!r}")
