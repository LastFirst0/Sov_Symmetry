from sov_evidence_geometry_core.legacy_runtime_adapter import adapt_legacy_runtime_connectivity, adapt_legacy_runtime_partial_order, adapt_legacy_runtime_tensor_last_symmetric
from sov_evidence_geometry_core.universal import evaluate_structural_claim


def test_legacy_runtime_adapter_emits_only_a_bounded_structural_packet():
    packet = adapt_legacy_runtime_connectivity({"candidate_id": "candidate-connected", "edges": [["a", "b"], ["b", "c"]]})
    outcome = evaluate_structural_claim(packet)
    assert outcome["status"] == "verified"
    assert outcome["trace"]["framework_id"] == "legacy-runtime-quarantined"
    assert "does not validate the legacy runtime" in packet["non_claims"][0].lower()


def test_legacy_runtime_adapter_negative_control_is_a_disconnected_graph_failure():
    packet = adapt_legacy_runtime_connectivity({"candidate_id": "candidate-disconnected-control", "edges": [["a", "b"], ["c", "d"]]})
    outcome = evaluate_structural_claim(packet)
    assert outcome["status"] == "fail"
    assert outcome["receipt"]["details"]["unreachable_vertices"] == [2, 3]


def test_legacy_runtime_partial_order_adapter_and_transitivity_negative_control():
    positive = adapt_legacy_runtime_partial_order({"candidate_id": "order-positive", "nodes": ["a", "b"], "relations": [["a", "a"], ["a", "b"], ["b", "b"]]})
    negative = adapt_legacy_runtime_partial_order({"candidate_id": "order-negative", "nodes": ["a", "b", "c"], "relations": [["a", "a"], ["b", "b"], ["c", "c"], ["a", "b"], ["b", "c"]]})
    assert evaluate_structural_claim(positive)["status"] == "verified"
    assert evaluate_structural_claim(negative)["status"] == "fail"


def test_legacy_runtime_tensor_adapter_and_asymmetry_negative_control():
    positive = adapt_legacy_runtime_tensor_last_symmetric({"candidate_id": "tensor-positive", "tensor": [[[1, 2], [2, 3]]]})
    negative = adapt_legacy_runtime_tensor_last_symmetric({"candidate_id": "tensor-negative", "tensor": [[[1, 2], [3, 4]]]})
    assert evaluate_structural_claim(positive)["status"] == "verified"
    assert evaluate_structural_claim(negative)["status"] == "fail"
