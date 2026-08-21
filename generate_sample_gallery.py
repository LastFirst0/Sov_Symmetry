"""Generate public claim journeys from the authoritative six-adapter fixture pack."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from sov_evidence_geometry_core import (
    check_identity_matrix,
    check_matrix_inverse,
    check_partial_order,
    check_rank3_last_indices_symmetric,
    check_symmetric_matrix,
    check_undirected_connected_graph,
    receipt_bundle,
)

PACK = ROOT / "tests" / "core_contract" / "data" / "universal_six_adapter_fixture_pack.json"
DEFAULT_OUTPUT = ROOT / "artifacts" / "sample_gallery" / "v0.1"
DEFAULT_DOC = ROOT / "docs" / "how-to" / "generated-sample-gallery.md"

ADAPTERS = {
    "matrix.symmetric.v1": {
        "title": "Matrix symmetry",
        "command": "symmetric",
        "non_claim": "This checks only whether the declared finite matrix equals its transpose.",
        "evaluate": lambda case: check_symmetric_matrix(case["input"]),
    },
    "matrix.identity.v1": {
        "title": "Identity matrix",
        "command": "identity",
        "non_claim": "This checks only whether the declared finite matrix has ones on its diagonal and zeros elsewhere.",
        "evaluate": lambda case: check_identity_matrix(case["input"]),
    },
    "matrix.inverse.v1": {
        "title": "Matrix inverse",
        "command": "inverse",
        "non_claim": "This checks only whether the two declared finite matrices multiply to the identity in both orders.",
        "evaluate": lambda case: check_matrix_inverse(case["input"], case.get("inverse")),
    },
    "relation.partial_order.v1": {
        "title": "Finite partial order",
        "command": "partial-order",
        "non_claim": "This checks only the declared finite relation matrix; it does not establish a real-world ordering.",
        "evaluate": lambda case: check_partial_order(case["input"]),
    },
    "graph.undirected_connected.v1": {
        "title": "Undirected graph connectivity",
        "command": "graph-connected",
        "non_claim": "This checks only connectivity of the declared finite undirected adjacency matrix.",
        "evaluate": lambda case: check_undirected_connected_graph(case["input"]),
    },
    "tensor.rank3_last_indices_symmetric.v1": {
        "title": "Rank-three tensor last-index symmetry",
        "command": "tensor-last-symmetric",
        "non_claim": "This checks only last-index symmetry in the declared finite rank-three tensor.",
        "evaluate": lambda case: check_rank3_last_indices_symmetric(case["input"]),
    },
}


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def display_path(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def build_gallery(output: Path, doc_path: Path) -> dict:
    pack = json.loads(PACK.read_text(encoding="utf-8"))
    output.mkdir(parents=True, exist_ok=True)
    journeys = []
    for check, adapter in ADAPTERS.items():
        selected = {case["class"]: case for case in pack["cases"] if case["check"] == check and case["class"] in {"positive", "negative", "malformed", "mutation"}}
        expected = {"positive", "negative", "malformed", "mutation"}
        if set(selected) != expected:
            raise SystemExit(f"fixture pack is incomplete for {check}: expected {expected}, got {set(selected)}")
        samples = []
        folder = output / adapter["command"]
        folder.mkdir(parents=True, exist_ok=True)
        for sample_kind, expected_status in (("positive", "verified"), ("negative", "fail"), ("malformed", "unverifiable"), ("mutation", "fail")):
            case = selected[sample_kind]
            receipt = adapter["evaluate"](case)
            if receipt["status"] != expected_status:
                raise SystemExit(f"fixture outcome drift for {case['id']}: {receipt['status']} != {expected_status}")
            record = {
                "schema": "sov.public_claim_journey_sample",
                "schema_version": "0.1.0",
                "adapter_id": check,
                "case_id": case["id"],
                "sample_kind": sample_kind,
                "expected_status": expected_status,
                "declared_input": case["input"],
                "declared_inverse": case.get("inverse"),
                "receipt": receipt,
                "bundle": receipt_bundle(receipt),
                "replay_command": f"python tools/sov_kernel.py replay --bundle artifacts/sample_gallery/v0.1/{adapter['command']}/{sample_kind}.json",
                "non_claim": adapter["non_claim"],
            }
            write_json(folder / f"{sample_kind}.json", record)
            samples.append({"kind": sample_kind, "status": expected_status, "path": display_path(folder / f"{sample_kind}.json"), "case_id": case["id"]})
        journeys.append({"adapter_id": check, "title": adapter["title"], "command": adapter["command"], "samples": samples, "non_claim": adapter["non_claim"]})
    index = {"schema": "sov.public_claim_journey_gallery", "schema_version": "0.1.0", "fixture_pack": str(PACK.relative_to(ROOT)), "journeys": journeys}
    write_json(output / "index.json", index)
    lines = ["# Generated Public Claim Journeys", "", "This file is generated from the shared six-adapter fixture pack. Do not edit receipt examples manually.", ""]
    for journey in journeys:
        lines.extend([f"## {journey['title']}", "", "| Outcome | Fixture | Generated sample |", "|---|---|---|"])
        for sample in journey["samples"]:
            lines.append(f"| `{sample['kind']}` → `{sample['status']}` | `{sample['case_id']}` | `{sample['path']}` |")
        lines.extend(["", f"> **Non-claim:** {journey['non_claim']}", "", f"Run: `python tools/sov_kernel.py check {journey['command']} --input '<JSON>'`", ""])
    doc_path.parent.mkdir(parents=True, exist_ok=True)
    doc_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return index


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate synchronized public claim journeys from the six-adapter fixture pack.")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    args = parser.parse_args()
    index = build_gallery(args.output, args.doc)
    print(json.dumps({"journey_count": len(index["journeys"]), "output": str(args.output), "documentation": str(args.doc)}))


if __name__ == "__main__":
    main()
