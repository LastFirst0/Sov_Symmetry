import base64, json
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from sov_evidence_geometry_core import (attach_local_audit, check_symmetric_matrix, receipt_bundle, verify_ed25519_dsse_fixture, verify_local_audit_attachment)
from sov_evidence_geometry_core.audit import dsse_pae
from sov_evidence_geometry_core.persistence import FileObjectStore

def test_real_local_attachment_stores_and_verifies_inclusion(tmp_path):
    bundle = receipt_bundle(check_symmetric_matrix([[1,2],[2,4]])); attachment = attach_local_audit(bundle, FileObjectStore(tmp_path))
    assert attachment["local_only"] is True and verify_local_audit_attachment(attachment)["status"] == "verified"
    attachment["event"]["body"]["event_type"] = "tampered"
    assert verify_local_audit_attachment(attachment)["status"] == "fail"

def _fixture():
    private = Ed25519PrivateKey.from_private_bytes(bytes(range(1,33))); public = private.public_key().public_bytes_raw()
    payload = json.dumps({"request_id":"request:fixture","outcome":"verified"}, sort_keys=True, separators=(",", ":")).encode()
    envelope={"payloadType":"application/vnd.sovereign.quorum.response.v1+json","payload":base64.b64encode(payload).decode(),"signatures":[{"keyid":"key:fixture-01","algorithm":"ed25519","sig":base64.b64encode(private.sign(dsse_pae("application/vnd.sovereign.quorum.response.v1+json",payload))).decode()}]}
    policy={"policy_id":"policy:fixture.v1","keys":{"key:fixture-01":{"state":"active","public_key":base64.b64encode(public).decode()}}}
    return envelope, policy

def test_offline_ed25519_fixture_and_key_policy_outcomes():
    envelope, policy = _fixture(); assert verify_ed25519_dsse_fixture(envelope, policy)["status"] == "verified"
    policy["keys"]["key:fixture-01"]["state"] = "revoked"; assert verify_ed25519_dsse_fixture(envelope, policy)["reason_code"] == "E_KEY_REVOKED"
def test_offline_ed25519_tamper_fails_signature():
    envelope, policy = _fixture(); envelope["payload"] = base64.b64encode(b'{"request_id":"mutated"}').decode(); assert verify_ed25519_dsse_fixture(envelope, policy)["reason_code"] == "E_SIGNATURE_INVALID"
