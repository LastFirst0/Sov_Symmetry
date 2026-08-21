import copy
import pytest
from sov_evidence_geometry_core.empirical import empirical_kernel_outcome, parse_empirical_claim_packet
from sov_evidence_geometry_core.errors import CoreContractError

VALID={
"schema":"sov.empirical_claim_packet","schema_version":"0.1.0","packet_id":"empirical:demo:1","claim_id":"claim:demo","claim_class":"empirical","framework_id":"framework:provenance-only","statement":"A bounded measured quantity.","state":"bound","target_quantity":{"name":"x","unit":"m","scope":"sample s"},"datasets":[{"dataset_id":"data:demo","version":"1","content_sha256":"a"*64,"media_type":"text/csv","license":"CC-BY-4.0","access":{"status":"open","locator":"https://example.test/data","access_conditions":"public"},"custodian":{"id":"org:demo","role":"steward"}}],"provenance":{"entities":[],"activities":[],"agents":[],"derivations":[]},"uncertainty":{"kind":"measurement","estimate":{"value":1.0,"unit":"m"},"components":[{"id":"u1","class":"statistical","description":"repeatability","standard_uncertainty":0.1,"unit":"m"}],"combination_method":"root-sum-square","combined_standard_uncertainty":{"value":0.1,"unit":"m"},"expanded_uncertainty":{"value":0.2,"unit":"m","coverage_factor":2},"interval_or_confidence":{"statement":"approximate interval","basis":"declared normal approximation"}},"analysis_binding":{"method_id":"method:demo","protocol_version":"1","input_mapping":"dataset to x","output_schema":"result.v1","review_required":True},"governance":{"review_status":"pending"},"non_claims":["This packet does not verify a theory."]}

def test_empirical_packet_validates_and_returns_external_analysis_boundary():
    assert parse_empirical_claim_packet(VALID)["packet_id"] == "empirical:demo:1"
    outcome=empirical_kernel_outcome(VALID)
    assert outcome["status"] == "unverifiable"
    assert outcome["reason_code"] == "E_EMPIRICAL_ANALYSIS_EXTERNAL"

@pytest.mark.parametrize("path,value,code",[("claim_class","structural","E_EMPIRICAL_CLASS"),("datasets",[],"E_EMPIRICAL_PROVENANCE"),("uncertainty.interval_or_confidence",{"statement":"95%"},"E_EMPIRICAL_UNCERTAINTY"),("analysis_binding.review_required","yes","E_EMPIRICAL_ANALYSIS")])
def test_empirical_packet_fails_closed(path,value,code):
    packet=copy.deepcopy(VALID); current=packet; parts=path.split('.')
    for part in parts[:-1]: current=current[part]
    current[parts[-1]]=value
    with pytest.raises(CoreContractError) as exc: parse_empirical_claim_packet(packet)
    assert exc.value.code == code
