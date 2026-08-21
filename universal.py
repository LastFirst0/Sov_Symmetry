"""Theory-agnostic adapter for declared structural claims.

The kernel verifies only the named finite check and declared input. Framework IDs are
opaque labels: they influence traceability, never evaluation semantics.
"""
from __future__ import annotations
from collections.abc import Mapping
from typing import Any
from .errors import CoreContractError
from .simple import check_identity_matrix, check_matrix_inverse, check_symmetric_matrix, check_partial_order, check_undirected_connected_graph, check_rank3_last_indices_symmetric

_SUPPORTED = {"matrix.symmetric.v1", "matrix.identity.v1", "matrix.inverse.v1", "relation.partial_order.v1", "graph.undirected_connected.v1", "tensor.rank3_last_indices_symmetric.v1"}

def evaluate_structural_claim(packet: Mapping[str, Any]) -> dict[str, Any]:
    if packet.get("schema") != "sov.structural_claim_packet" or packet.get("schema_version") != "0.1.0":
        raise CoreContractError("E_SCHEMA_INVALID", "unsupported structural claim packet")
    framework_id, claim_id, claim_class, check = packet.get("framework_id"), packet.get("claim_id"), packet.get("claim_class"), packet.get("check")
    if not all(isinstance(value, str) and value for value in (framework_id, claim_id, claim_class, check)):
        raise CoreContractError("E_SCHEMA_INVALID", "framework_id, claim_id, claim_class, and check are required")
    trace = {"framework_id": framework_id, "claim_id": claim_id, "claim_class": claim_class, "check": check}
    if claim_class not in {"formal", "structural", "computational"}:
        return {"status":"unverifiable","plain_status":"cannot be checked from this input","why":"This claim class needs an empirical study, interpretive argument, or other evidence outside this deterministic structural kernel.","trace":trace,"scope":"The kernel does not decide the truth of an entire framework, metaphysical assertion, or empirical theory."}
    if check not in _SUPPORTED:
        return {"status":"unverifiable","plain_status":"cannot be checked from this input","why":"This named structural check is not implemented in this release.","trace":trace,"scope":"Unsupported checks are not approximated or guessed."}
    if check == "matrix.symmetric.v1": receipt = check_symmetric_matrix(packet.get("input", []))
    elif check == "matrix.identity.v1": receipt = check_identity_matrix(packet.get("input", []))
    elif check == "relation.partial_order.v1": receipt = check_partial_order(packet.get("input", []))
    elif check == "graph.undirected_connected.v1": receipt = check_undirected_connected_graph(packet.get("input", []))
    elif check == "tensor.rank3_last_indices_symmetric.v1": receipt = check_rank3_last_indices_symmetric(packet.get("input", []))
    else:
        inverse = packet.get("inverse")
        receipt = check_matrix_inverse(packet.get("input", []), inverse if isinstance(inverse, list) else [])
    return {"status":receipt["status"],"plain_status":receipt["plain_status"],"receipt":receipt,"trace":trace,"scope":"This result evaluates only the declared structural claim and input. The framework identifier is provenance, not a preferred ontology or scientific verdict."}
