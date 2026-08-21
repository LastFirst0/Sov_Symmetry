from sov_evidence_geometry_core import advanced_evidence_export, check_symmetric_matrix, receipt_bundle, replay_receipt_bundle

def test_bundle_replays_same_simple_receipt():
    receipt = check_symmetric_matrix([[1, 2], [2, 4]])
    bundle = receipt_bundle(receipt)
    assert replay_receipt_bundle(bundle)["status"] == "verified"
    assert advanced_evidence_export(bundle)["assurance_status"] == "not_recorded"
def test_bundle_tamper_is_a_non_passing_replay_result():
    receipt = check_symmetric_matrix([[1, 2], [2, 4]])
    bundle = receipt_bundle(receipt); bundle["provenance"]["input"] = [[1, 3], [2, 4]]
    replay = replay_receipt_bundle(bundle)
    assert replay["status"] == "fail" and replay["reason_code"] == "E_ID_MISMATCH"
def test_advanced_export_preserves_recorded_local_evidence_without_upgrading_its_claim():
    receipt = check_symmetric_matrix([[1, 2], [2, 4]])
    export = advanced_evidence_export(receipt_bundle(receipt, assurance={"audit_event_id":"audit:sha256:test", "checkpoint_id":"checkpoint:sha256:test", "local_only":True}))
    assert export["assurance_status"] == "recorded" and export["advanced_assurance"]["local_only"] is True
