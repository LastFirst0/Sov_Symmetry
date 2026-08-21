"""A small fail-closed invariant interpreter for Core Contract v0.1."""

from __future__ import annotations

from collections.abc import Callable
from fractions import Fraction
from typing import Any

from .canonical import derive_evidence_id
from .errors import CoreContractError
from .store import MemoryObjectStore
from .types import Evaluation, EvaluationStatus, PredicateOutcome
from .validation import _body, _manifold_dimension, scalar_fraction


Predicate = Callable[[tuple[str, ...]], Evaluation]


class ReferenceInterpreter:
    """Evaluate the deliberately small v0.1 invariant registry.

    The registry is code-owned.  Unknown operations never execute user input and
    therefore return an ``unverifiable`` outcome rather than attempting dynamic
    imports or expression evaluation.
    """

    def __init__(self, store: MemoryObjectStore) -> None:
        self.store = store
        self._registry: dict[str, Predicate] = {
            "tensor.dimension.v1": self._tensor_dimension,
            "tensor.symmetry.v1": self._tensor_symmetry,
            "metric.inverse.v1": self._metric_inverse,
            "connection.torsion_free.v1": self._connection_torsion_free,
            "evidence.replay.v1": self._evidence_replay,
        }

    @property
    def registered_operations(self) -> tuple[str, ...]:
        return tuple(sorted(self._registry))

    def evaluate(self, operation_id: str, input_ids: list[str] | tuple[str, ...]) -> Evaluation:
        operation = self._registry.get(operation_id)
        if operation is None:
            return Evaluation.unverifiable(operation_id, "E_OPERATION_UNKNOWN")
        try:
            return operation(tuple(input_ids))
        except CoreContractError as exc:
            return Evaluation.unverifiable(operation_id, exc.code)

    def _tensor_dimension(self, input_ids: tuple[str, ...]) -> Evaluation:
        if len(input_ids) != 1:
            return Evaluation.unverifiable("tensor.dimension.v1", "E_SCHEMA_INVALID")
        record = self.store.get(input_ids[0])
        body = _body(record)
        if body["object_kind"] not in {"tensor", "metric", "form", "connection"}:
            return Evaluation.unverifiable("tensor.dimension.v1", "E_REFERENCE_KIND")
        outcome = PredicateOutcome("tensor.dimension.v1", EvaluationStatus.VERIFIED, "VERIFIED")
        return Evaluation("tensor.dimension.v1", EvaluationStatus.VERIFIED, ("VERIFIED",), (outcome,))

    @staticmethod
    def _fraction_scalar(value: Fraction) -> dict[str, Any]:
        if value.denominator == 1:
            return {"kind": "integer", "value": str(value.numerator)}
        return {
            "kind": "rational",
            "numerator": str(value.numerator),
            "denominator": str(value.denominator),
        }

    @staticmethod
    def _sparse_component_map(record: dict[str, Any], *, expected_rank: int | None = None) -> dict[tuple[int, ...], Fraction]:
        components = _body(record)["content"]["components"]
        if components["mode"] != "sparse_exact":
            raise CoreContractError("E_SCALAR_UNSUPPORTED", "predicate requires sparse_exact components")
        result: dict[tuple[int, ...], Fraction] = {}
        for component in components["components"]:
            indices = tuple(component["indices"])
            if expected_rank is not None and len(indices) != expected_rank:
                raise CoreContractError("E_INDEX_INVALID", "component rank is incompatible with predicate")
            result[indices] = scalar_fraction(component["value"])
        return result

    def _tensor_symmetry(self, input_ids: tuple[str, ...]) -> Evaluation:
        if len(input_ids) != 1:
            return Evaluation.unverifiable("tensor.symmetry.v1", "E_SCHEMA_INVALID")
        record = self.store.get(input_ids[0])
        body = _body(record)
        if body["object_kind"] != "tensor":
            return Evaluation.unverifiable("tensor.symmetry.v1", "E_REFERENCE_KIND")
        declared = body["content"].get("symmetries", [])
        if not declared:
            return Evaluation.unverifiable("tensor.symmetry.v1", "E_ASSUMPTION_MISSING")
        components = self._sparse_component_map(record, expected_rank=len(body["content"]["slots"]))
        for symmetry in declared:
            slots = symmetry["slots"]
            if len(slots) != 2:
                return Evaluation.unverifiable("tensor.symmetry.v1", "E_FEATURE_DEFERRED")
            left, right = slots
            all_indices = set(components)
            all_indices |= {
                tuple(index[right] if position == left else index[left] if position == right else index[position] for position in range(len(index)))
                for index in components
            }
            for indices in all_indices:
                swapped = list(indices)
                swapped[left], swapped[right] = swapped[right], swapped[left]
                observed = components.get(indices, Fraction(0, 1))
                peer = components.get(tuple(swapped), Fraction(0, 1))
                expected = peer if symmetry["kind"] == "symmetric" else -peer
                if observed != expected:
                    residual = self._fraction_scalar(abs(observed - expected))
                    outcome = PredicateOutcome(
                        "tensor.symmetry.v1",
                        EvaluationStatus.FAIL,
                        "E_PREDICATE_FAILED",
                        {"kind": "exact_zero", "value": residual},
                    )
                    return Evaluation("tensor.symmetry.v1", EvaluationStatus.FAIL, ("E_PREDICATE_FAILED",), (outcome,))
        outcome = PredicateOutcome("tensor.symmetry.v1", EvaluationStatus.VERIFIED, "VERIFIED")
        return Evaluation("tensor.symmetry.v1", EvaluationStatus.VERIFIED, ("VERIFIED",), (outcome,))

    @staticmethod
    def _exact_matrix(record: dict[str, Any], dimension: int) -> list[list[Fraction]]:
        components = ReferenceInterpreter._sparse_component_map(record, expected_rank=2)
        matrix = [[Fraction(0, 1) for _ in range(dimension)] for _ in range(dimension)]
        for (row, column), value in components.items():
            matrix[row][column] = value
        return matrix

    def _metric_inverse(self, input_ids: tuple[str, ...]) -> Evaluation:
        if len(input_ids) != 2:
            return Evaluation.unverifiable("metric.inverse.v1", "E_SCHEMA_INVALID")
        metric, inverse = (self.store.get(object_id) for object_id in input_ids)
        metric_body, inverse_body = _body(metric), _body(inverse)
        if metric_body["object_kind"] != "metric" or inverse_body["object_kind"] not in {"metric", "tensor"}:
            return Evaluation.unverifiable("metric.inverse.v1", "E_REFERENCE_KIND")
        if metric_body["content"]["manifold_id"] != inverse_body["content"]["manifold_id"]:
            return Evaluation.unverifiable("metric.inverse.v1", "E_DIMENSION_MISMATCH")
        manifold = self.store.get(metric_body["content"]["manifold_id"])
        dimension = _manifold_dimension(manifold)
        left = self._exact_matrix(metric, dimension)
        right = self._exact_matrix(inverse, dimension)
        maximum_residual = Fraction(0, 1)
        for row in range(dimension):
            for column in range(dimension):
                product = sum(left[row][index] * right[index][column] for index in range(dimension))
                expected = Fraction(1 if row == column else 0, 1)
                maximum_residual = max(maximum_residual, abs(product - expected))
        residual = {"kind": "exact_zero", "value": self._fraction_scalar(maximum_residual)}
        if maximum_residual == 0:
            outcome = PredicateOutcome("metric.inverse.v1", EvaluationStatus.VERIFIED, "VERIFIED", residual)
            return Evaluation("metric.inverse.v1", EvaluationStatus.VERIFIED, ("VERIFIED",), (outcome,))
        outcome = PredicateOutcome("metric.inverse.v1", EvaluationStatus.FAIL, "E_PREDICATE_FAILED", residual)
        return Evaluation("metric.inverse.v1", EvaluationStatus.FAIL, ("E_PREDICATE_FAILED",), (outcome,))

    def _connection_torsion_free(self, input_ids: tuple[str, ...]) -> Evaluation:
        if len(input_ids) != 1:
            return Evaluation.unverifiable("connection.torsion_free.v1", "E_SCHEMA_INVALID")
        record = self.store.get(input_ids[0])
        body = _body(record)
        if body["object_kind"] != "connection":
            return Evaluation.unverifiable("connection.torsion_free.v1", "E_REFERENCE_KIND")
        components = self._sparse_component_map(record, expected_rank=3)
        all_indices = set(components)
        all_indices |= {(rho, nu, mu) for rho, mu, nu in components}
        for rho, mu, nu in all_indices:
            observed = components.get((rho, mu, nu), Fraction(0, 1))
            peer = components.get((rho, nu, mu), Fraction(0, 1))
            if observed != peer:
                residual = {"kind": "exact_zero", "value": self._fraction_scalar(abs(observed - peer))}
                outcome = PredicateOutcome("connection.torsion_free.v1", EvaluationStatus.FAIL, "E_PREDICATE_FAILED", residual)
                return Evaluation("connection.torsion_free.v1", EvaluationStatus.FAIL, ("E_PREDICATE_FAILED",), (outcome,))
        outcome = PredicateOutcome("connection.torsion_free.v1", EvaluationStatus.VERIFIED, "VERIFIED")
        return Evaluation("connection.torsion_free.v1", EvaluationStatus.VERIFIED, ("VERIFIED",), (outcome,))

    def _evidence_replay(self, input_ids: tuple[str, ...]) -> Evaluation:
        if len(input_ids) != 1:
            return Evaluation.unverifiable("evidence.replay.v1", "E_SCHEMA_INVALID")
        record = self.store.get(input_ids[0])
        if record.get("schema") != "sov.core.evidence":
            return Evaluation.unverifiable("evidence.replay.v1", "E_REFERENCE_KIND")
        expected = derive_evidence_id(record)
        if expected != record["id"] or expected != record["canonical_body_hash"]:
            outcome = PredicateOutcome("evidence.replay.v1", EvaluationStatus.FAIL, "E_ID_MISMATCH")
            return Evaluation("evidence.replay.v1", EvaluationStatus.FAIL, ("E_ID_MISMATCH",), (outcome,))
        outcome = PredicateOutcome("evidence.replay.v1", EvaluationStatus.VERIFIED, "VERIFIED")
        return Evaluation("evidence.replay.v1", EvaluationStatus.VERIFIED, ("VERIFIED",), (outcome,))
