"""Generate immutable Python-reference vectors for Rust Core Contract parity tests."""

from __future__ import annotations

import json
from pathlib import Path

from sov_evidence_geometry_core.canonical import derive_id


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "tests" / "core_contract" / "data" / "cross_language_invariant_vectors.json"

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


def envelope(kind: str, content: dict) -> dict:
    body = {
        "schema": "sov.core.object",
        "schema_version": "0.1.0",
        "object_kind": kind,
        "convention_profile": PROFILE,
        "assumptions": [],
        "content": content,
    }
    return {"id": derive_id(body), "canonical_body": body}


def integer(value: int) -> dict:
    return {"kind": "integer", "value": str(value)}


def diagonal(diagonal_values: list[int]) -> dict:
    return {
        "mode": "sparse_exact",
        "components": [
            {"indices": [index, index], "value": integer(value)}
            for index, value in enumerate(diagonal_values)
        ],
    }


def main() -> None:
    manifold = envelope(
        "manifold",
        {"name": "M2", "dimension": 2, "orientation_mode": "declared", "signature": {"positive": 2, "negative": 0, "zero": 0}},
    )
    chart = envelope("chart", {"manifold_id": manifold["id"], "name": "x", "coordinates": ["x0", "x1"]})

    def metric(name: str, values: list[int]) -> dict:
        return envelope(
            "metric",
            {
                "manifold_id": manifold["id"],
                "chart_id": chart["id"],
                "name": name,
                "signature": {"positive": 2, "negative": 0, "zero": 0},
                "components": diagonal(values),
                "nondegeneracy": "fixture_verified",
            },
        )

    metric_g = metric("g", [1, 1])
    metric_inverse = metric("g_inverse", [1, 1])
    metric_not_inverse = metric("not_inverse", [1, 2])
    symmetric = envelope(
        "tensor",
        {
            "manifold_id": manifold["id"],
            "chart_id": chart["id"],
            "name": "symmetric",
            "slots": [{"variance": "covariant", "label": "mu"}, {"variance": "covariant", "label": "nu"}],
            "symmetries": [{"kind": "symmetric", "slots": [0, 1]}],
            "units": [],
            "components": {"mode": "sparse_exact", "components": [{"indices": [0, 1], "value": integer(3)}, {"indices": [1, 0], "value": integer(3)}]},
        },
    )
    asymmetric = envelope(
        "tensor",
        {
            "manifold_id": manifold["id"],
            "chart_id": chart["id"],
            "name": "asymmetric",
            "slots": [{"variance": "covariant", "label": "mu"}, {"variance": "covariant", "label": "nu"}],
            "symmetries": [{"kind": "symmetric", "slots": [0, 1]}],
            "units": [],
            "components": {"mode": "sparse_exact", "components": [{"indices": [0, 1], "value": integer(3)}]},
        },
    )
    records = [manifold, chart, metric_g, metric_inverse, metric_not_inverse, symmetric, asymmetric]
    scenarios = [
        {"name": "metric_inverse_verified", "operation_id": "metric.inverse.v1", "input_ids": [metric_g["id"], metric_inverse["id"]], "expected": {"status": "verified", "reason_codes": ["VERIFIED"]}},
        {"name": "metric_inverse_failed", "operation_id": "metric.inverse.v1", "input_ids": [metric_g["id"], metric_not_inverse["id"]], "expected": {"status": "fail", "reason_codes": ["E_PREDICATE_FAILED"]}},
        {"name": "tensor_symmetry_verified", "operation_id": "tensor.symmetry.v1", "input_ids": [symmetric["id"]], "expected": {"status": "verified", "reason_codes": ["VERIFIED"]}},
        {"name": "tensor_symmetry_failed", "operation_id": "tensor.symmetry.v1", "input_ids": [asymmetric["id"]], "expected": {"status": "fail", "reason_codes": ["E_PREDICATE_FAILED"]}},
        {"name": "unknown_operation_unverifiable", "operation_id": "gu.complete_action.v1", "input_ids": [], "expected": {"status": "unverifiable", "reason_codes": ["E_OPERATION_UNKNOWN"]}},
    ]
    document = {"schema": "sov.cross_language_vectors", "schema_version": "0.1.0", "records": records, "scenarios": scenarios}
    OUTPUT.write_text(json.dumps(document, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}")


if __name__ == "__main__":
    main()
