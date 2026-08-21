"""Deterministic tests for the Core Contract v0.1 Python reference SDK."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

from sov_evidence_geometry_core import MemoryObjectStore, ReferenceInterpreter, canonicalize, derive_id, parse_strict_json
from sov_evidence_geometry_core.canonical import derive_evidence_id
from sov_evidence_geometry_core.errors import CoreContractError
from sov_evidence_geometry_core.schema import validate_schema
from sov_evidence_geometry_core.types import EvaluationStatus


PROFILE = {
    "id": "convention:standard.v1",
    "curvature_sign": "RhoSigmaMuNu_v1",
    "metric_signature_order": "positive_negative_zero",
    "index_notation": "einstein_ascii_v1",
    "scalar_policy": "exact_only",
    "coordinate_basis": "coordinate_basis_required",
    "unit_policy": "dimensionless_only",
    "tolerance_policy": "tolerance:exact.v1",
}


def envelope(kind: str, content: dict, assumptions: list[str] | None = None) -> dict:
    body = {
        "schema": "sov.core.object",
        "schema_version": "0.1.0",
        "object_kind": kind,
        "convention_profile": PROFILE,
        "assumptions": assumptions or [],
        "content": content,
    }
    return {"id": derive_id(body), "canonical_body": body}


def integer(value: int) -> dict:
    return {"kind": "integer", "value": str(value)}


def diagonal_components(dimension: int, diagonal: list[int]) -> dict:
    return {
        "mode": "sparse_exact",
        "components": [
            {"indices": [index, index], "value": integer(value)}
            for index, value in enumerate(diagonal[:dimension])
        ],
    }


class CanonicalizationTests(unittest.TestCase):
    def test_sorting_is_stable(self) -> None:
        self.assertEqual(canonicalize({"b": 1, "a": 2}), b'{"a":2,"b":1}')

    def test_content_id_matches_external_sha256_vector(self) -> None:
        self.assertEqual(
            derive_id({"b": 1, "a": 2}),
            "sov:sha256:d3626ac30a87e6f7a6428233b3c68299976865fa5508e4267c5415c76af7a772",
        )

    def test_duplicate_json_key_rejected(self) -> None:
        with self.assertRaisesRegex(CoreContractError, "E_CANONICALIZATION"):
            parse_strict_json('{"a":1,"a":2}')

    def test_raw_float_rejected(self) -> None:
        with self.assertRaisesRegex(CoreContractError, "E_CANONICALIZATION"):
            canonicalize({"value": 0.5})


class InterpreterTests(unittest.TestCase):
    def setUp(self) -> None:
        self.store = MemoryObjectStore()
        self.manifold = envelope("manifold", {"name": "M2", "dimension": 2, "orientation_mode": "declared", "signature": {"positive": 2, "negative": 0, "zero": 0}})
        self.store.put(self.manifold)
        self.chart = envelope("chart", {"manifold_id": self.manifold["id"], "name": "x", "coordinates": ["x0", "x1"]})
        self.store.put(self.chart)
        self.interpreter = ReferenceInterpreter(self.store)

    def metric(self, name: str, diagonal: list[int]) -> dict:
        return envelope(
            "metric",
            {
                "manifold_id": self.manifold["id"],
                "chart_id": self.chart["id"],
                "name": name,
                "signature": {"positive": 2, "negative": 0, "zero": 0},
                "components": diagonal_components(2, diagonal),
                "nondegeneracy": "fixture_verified",
            },
        )

    def test_metric_inverse_verified(self) -> None:
        metric = self.metric("g", [1, 1])
        inverse = self.metric("g_inv", [1, 1])
        self.store.put(metric)
        self.store.put(inverse)
        result = self.interpreter.evaluate("metric.inverse.v1", [metric["id"], inverse["id"]])
        self.assertEqual(result.status, EvaluationStatus.VERIFIED)

    def test_metric_inverse_failure_is_explicit(self) -> None:
        metric = self.metric("g", [1, 1])
        not_inverse = self.metric("not_inverse", [1, 2])
        self.store.put(metric)
        self.store.put(not_inverse)
        result = self.interpreter.evaluate("metric.inverse.v1", [metric["id"], not_inverse["id"]])
        self.assertEqual(result.status, EvaluationStatus.FAIL)
        self.assertEqual(result.reason_codes, ("E_PREDICATE_FAILED",))

    def test_unknown_operation_is_unverifiable(self) -> None:
        result = self.interpreter.evaluate("gu.complete_action.v1", [])
        self.assertEqual(result.status, EvaluationStatus.UNVERIFIABLE)
        self.assertEqual(result.reason_codes, ("E_OPERATION_UNKNOWN",))

    def test_exact_symmetric_tensor_is_verified(self) -> None:
        tensor = envelope(
            "tensor",
            {
                "manifold_id": self.manifold["id"],
                "chart_id": self.chart["id"],
                "name": "s",
                "slots": [{"variance": "covariant", "label": "mu"}, {"variance": "covariant", "label": "nu"}],
                "symmetries": [{"kind": "symmetric", "slots": [0, 1]}],
                "units": [],
                "components": {"mode": "sparse_exact", "components": [{"indices": [0, 1], "value": integer(3)}, {"indices": [1, 0], "value": integer(3)}]},
            },
        )
        self.store.put(tensor)
        result = self.interpreter.evaluate("tensor.symmetry.v1", [tensor["id"]])
        self.assertEqual(result.status, EvaluationStatus.VERIFIED)

    def test_asymmetric_tensor_fails(self) -> None:
        tensor = envelope(
            "tensor",
            {
                "manifold_id": self.manifold["id"],
                "chart_id": self.chart["id"],
                "name": "bad_s",
                "slots": [{"variance": "covariant", "label": "mu"}, {"variance": "covariant", "label": "nu"}],
                "symmetries": [{"kind": "symmetric", "slots": [0, 1]}],
                "units": [],
                "components": {"mode": "sparse_exact", "components": [{"indices": [0, 1], "value": integer(3)}]},
            },
        )
        self.store.put(tensor)
        result = self.interpreter.evaluate("tensor.symmetry.v1", [tensor["id"]])
        self.assertEqual(result.status, EvaluationStatus.FAIL)

    def test_id_tampering_rejected_at_store_boundary(self) -> None:
        bad = self.metric("g", [1, 1])
        bad["id"] = "sov:sha256:" + "0" * 64
        with self.assertRaisesRegex(CoreContractError, "E_ID_MISMATCH"):
            self.store.put(bad)

    def test_evidence_replay(self) -> None:
        metric = self.metric("g", [1, 1])
        self.store.put(metric)
        evidence = {
            "schema": "sov.core.evidence",
            "schema_version": "0.1.0",
            "operation_id": "tensor.dimension.v1",
            "input_ids": [metric["id"]],
            "output_ids": [],
            "convention_profile_id": "convention:standard.v1",
            "assumption_ids": [],
            "verification_scope": "schema",
            "predicate_results": [{"predicate_id": "tensor.dimension.v1", "outcome": "pass", "reason_code": "VERIFIED"}],
            "status": "verified",
            "reason_codes": ["VERIFIED"],
            "limitations": [],
        }
        evidence_id = derive_evidence_id(evidence)
        evidence["id"] = evidence_id
        evidence["canonical_body_hash"] = evidence_id
        self.store.put(evidence)
        result = self.interpreter.evaluate("evidence.replay.v1", [evidence_id])
        self.assertEqual(result.status, EvaluationStatus.VERIFIED)


class PublishedFixturePackTests(unittest.TestCase):
    def test_all_published_valid_objects_have_resolvable_final_ids(self) -> None:
        fixture_path = Path(__file__).parent / "data" / "sov_core_v0_1_fixture_pack.json"
        pack = json.loads(fixture_path.read_text(encoding="utf-8"))
        self.assertEqual(len(pack["fixtures"]), 17)
        store = MemoryObjectStore()
        accepted = 0
        for fixture in pack["fixtures"]:
            validate_schema("conformance", fixture)
            record = fixture["input"].get("core_record")
            if fixture["category"] != "valid_object":
                continue
            self.assertIsNotNone(record)
            asserted_id = store.put(record)
            self.assertEqual(asserted_id, fixture["expected"]["canonical_id"])
            accepted += 1
        self.assertEqual(accepted, 8)
        evidence = next(
            fixture["input"]["core_record"]
            for fixture in pack["fixtures"]
            if fixture["input"].get("core_record", {}).get("schema") == "sov.core.evidence"
        )
        result = ReferenceInterpreter(store).evaluate("evidence.replay.v1", [evidence["id"]])
        self.assertEqual(result.status, EvaluationStatus.VERIFIED)


if __name__ == "__main__":
    unittest.main()
