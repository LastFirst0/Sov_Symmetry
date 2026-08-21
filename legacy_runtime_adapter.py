"""Quarantined bridge from legacy-runtime candidates to one neutral finite predicate.

The legacy runtime supplies only opaque candidate graph data. This adapter never imports
or validates legacy ontology, mathematical claims, or runtime conclusions; it creates a
versioned graph-connectivity packet for the universal verifier.
"""
from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any


def adapt_legacy_runtime_connectivity(candidate: Mapping[str, Any]) -> dict[str, Any]:
    candidate_id = candidate.get("candidate_id")
    edges = candidate.get("edges")
    if not isinstance(candidate_id, str) or not candidate_id:
        raise ValueError("E_LEGACY_CANDIDATE_ID_REQUIRED")
    if not isinstance(edges, Sequence) or isinstance(edges, (str, bytes)):
        raise ValueError("E_LEGACY_EDGES_REQUIRED")
    normalized: list[list[str]] = []
    for edge in edges:
        if not isinstance(edge, Sequence) or isinstance(edge, (str, bytes)) or len(edge) != 2 or not all(isinstance(node, str) and node for node in edge):
            raise ValueError("E_LEGACY_EDGE_INVALID")
        normalized.append([edge[0], edge[1]])
    vertices = sorted({node for edge in normalized for node in edge})
    index = {node: position for position, node in enumerate(vertices)}
    adjacency = [[0 for _ in vertices] for _ in vertices]
    for left, right in normalized:
        adjacency[index[left]][index[right]] = 1
        adjacency[index[right]][index[left]] = 1
    return {
        "schema": "sov.structural_claim_packet", "schema_version": "0.1.0",
        "framework_id": "legacy-runtime-quarantined", "claim_id": f"legacy-connectivity:{candidate_id}",
        "claim_class": "structural", "check": "graph.undirected_connected.v1", "input": adjacency,
        "provenance": {"candidate_id": candidate_id, "adapter": "legacy_runtime_connectivity.v0.1", "vertex_labels": vertices},
        "non_claims": ["This does not validate the legacy runtime.", "This does not establish an empirical, physical, semantic, or theoretical conclusion."],
    }


def adapt_legacy_runtime_partial_order(candidate: Mapping[str, Any]) -> dict[str, Any]:
    candidate_id, nodes, relations = candidate.get("candidate_id"), candidate.get("nodes"), candidate.get("relations")
    if not isinstance(candidate_id, str) or not candidate_id or not isinstance(nodes, Sequence) or isinstance(nodes, (str, bytes)) or not all(isinstance(node, str) and node for node in nodes):
        raise ValueError("E_LEGACY_ORDER_CANDIDATE_INVALID")
    if not isinstance(relations, Sequence) or isinstance(relations, (str, bytes)):
        raise ValueError("E_LEGACY_ORDER_RELATIONS_REQUIRED")
    labels = list(nodes)
    if len(set(labels)) != len(labels):
        raise ValueError("E_LEGACY_ORDER_NODES_DUPLICATE")
    index = {label: position for position, label in enumerate(labels)}
    matrix = [[0 for _ in labels] for _ in labels]
    for relation in relations:
        if not isinstance(relation, Sequence) or isinstance(relation, (str, bytes)) or len(relation) != 2 or relation[0] not in index or relation[1] not in index:
            raise ValueError("E_LEGACY_ORDER_RELATION_INVALID")
        matrix[index[relation[0]]][index[relation[1]]] = 1
    return {
        "schema": "sov.structural_claim_packet", "schema_version": "0.1.0",
        "framework_id": "legacy-runtime-quarantined", "claim_id": f"legacy-order:{candidate_id}",
        "claim_class": "structural", "check": "relation.partial_order.v1", "input": matrix,
        "provenance": {"candidate_id": candidate_id, "adapter": "legacy_runtime_partial_order.v0.1", "node_labels": labels},
        "non_claims": ["This does not validate the legacy runtime.", "This checks only the declared finite relation matrix."],
    }


def adapt_legacy_runtime_tensor_last_symmetric(candidate: Mapping[str, Any]) -> dict[str, Any]:
    """Adapt a finite legacy tensor candidate to the neutral final-axis symmetry check.

    The candidate remains opaque.  This boundary validates shape and finite numeric
    entries only; it neither imports nor endorses legacy-runtime interpretation.
    """
    candidate_id, tensor = candidate.get("candidate_id"), candidate.get("tensor")
    if not isinstance(candidate_id, str) or not candidate_id:
        raise ValueError("E_LEGACY_TENSOR_CANDIDATE_ID_REQUIRED")
    if not isinstance(tensor, Sequence) or isinstance(tensor, (str, bytes)) or not tensor:
        raise ValueError("E_LEGACY_TENSOR_REQUIRED")
    return {
        "schema": "sov.structural_claim_packet", "schema_version": "0.1.0",
        "framework_id": "legacy-runtime-quarantined", "claim_id": f"legacy-tensor-last-symmetric:{candidate_id}",
        "claim_class": "structural", "check": "tensor.rank3_last_indices_symmetric.v1", "input": tensor,
        "provenance": {"candidate_id": candidate_id, "adapter": "legacy_runtime_tensor_last_symmetric.v0.1"},
        "non_claims": ["This does not validate the legacy runtime.", "This checks only declared finite tensor last-axis symmetry."],
    }
