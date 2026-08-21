from sov_evidence_geometry_core import evaluate_structural_claim

def _packet(framework_id):
    return {"schema":"sov.structural_claim_packet","schema_version":"0.1.0","framework_id":framework_id,"claim_id":"claim:symmetry","claim_class":"structural","check":"matrix.symmetric.v1","input":[[1,2],[2,4]]}
def test_framework_label_is_traceability_not_evaluation_semantics():
    a=evaluate_structural_claim(_packet("framework:geometric-unity")); b=evaluate_structural_claim(_packet("framework:causal-set")); c=evaluate_structural_claim(_packet("framework:custom"))
    assert [a["status"],b["status"],c["status"]] == ["verified","verified","verified"]
    assert a["receipt"]["receipt_id"] == b["receipt"]["receipt_id"] == c["receipt"]["receipt_id"]
def test_empirical_and_metaphysical_claims_are_not_promoted_to_kernel_verdicts():
    packet=_packet("framework:any"); packet["claim_class"]="empirical"
    result=evaluate_structural_claim(packet)
    assert result["status"] == "unverifiable" and "entire framework" in result["scope"]
def test_unknown_structural_check_fails_closed_as_unverifiable():
    packet=_packet("framework:any"); packet["check"]="tensor.holographic.v9"
    assert evaluate_structural_claim(packet)["status"] == "unverifiable"
def test_partial_order_is_a_framework_neutral_structural_adapter():
    packet={"schema":"sov.structural_claim_packet","schema_version":"0.1.0","framework_id":"framework:any","claim_id":"claim:finite-order","claim_class":"structural","check":"relation.partial_order.v1","input":[[1,1,1],[0,1,1],[0,0,1]]}
    assert evaluate_structural_claim(packet)["status"] == "verified"
    packet["input"]=[[1,1],[1,1]]
    assert evaluate_structural_claim(packet)["status"] == "fail"

def test_partial_order_refuses_nonbinary_or_float_relation_entries():
    packet={"schema":"sov.structural_claim_packet","schema_version":"0.1.0","framework_id":"framework:any","claim_id":"claim:bad-order","claim_class":"structural","check":"relation.partial_order.v1","input":[[1,0.0],[0,1]]}
    assert evaluate_structural_claim(packet)["status"] == "unverifiable"
def test_graph_connectivity_adapter_has_exact_positive_negative_and_unverifiable_paths():
    base={"schema":"sov.structural_claim_packet","schema_version":"0.1.0","framework_id":"framework:any","claim_id":"claim:graph","claim_class":"structural","check":"graph.undirected_connected.v1"}
    assert evaluate_structural_claim({**base,"input":[[0,1,0],[1,0,1],[0,1,0]]})["status"] == "verified"
    assert evaluate_structural_claim({**base,"input":[[0,0],[0,0]]})["status"] == "fail"
    assert evaluate_structural_claim({**base,"input":[[0,1],[0,0]]})["status"] == "unverifiable"
def test_rank3_tensor_adapter_has_exact_positive_negative_and_unverifiable_paths():
    base={"schema":"sov.structural_claim_packet","schema_version":"0.1.0","framework_id":"framework:any","claim_id":"claim:tensor","claim_class":"structural","check":"tensor.rank3_last_indices_symmetric.v1"}
    assert evaluate_structural_claim({**base,"input":[[[1,2],[2,3]],[[4,5],[5,6]]]})["status"] == "verified"
    assert evaluate_structural_claim({**base,"input":[[[1,2],[9,3]]]})["status"] == "fail"
    assert evaluate_structural_claim({**base,"input":[[[1,2,3],[2,3,4]]]})["status"] == "unverifiable"
