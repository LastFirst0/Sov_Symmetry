import tempfile
from pathlib import Path
import pytest
from sov_evidence_geometry_core import DurableQuorumLedger, FileObjectStore
from sov_evidence_geometry_core.audit import LocalTransparencyLog
from sov_evidence_geometry_core.errors import CoreContractError

def decision():
    return {"decision_id":"quorum_decision:sha256:" + "a" * 64,"body":{"request_id":"request:k1","policy_id":"policy:k1","decision_status":"contested","accepted_response_ids":[],"rejected":[{"response_id":"bad","code":"E_SIGNATURE_INVALID"}],"equivocation_evidence":[{"node_id":"node:1","payload_hashes":["a"*64,"b"*64]}]}}

def test_durable_quorum_records_restart_and_merkle_inclusion():
    with tempfile.TemporaryDirectory() as root:
        store=FileObjectStore(root); ledger=DurableQuorumLedger(store); result=ledger.persist(decision())
        assert len(result["records"]) == 3
        assert LocalTransparencyLog.verify_inclusion(result["records"][0]["event"], ledger.log.inclusion_proof(0), result["checkpoint"])
        reopened=FileObjectStore(root); reopened.verify_manifest()
        assert reopened.get(result["records"][1]["record_id"])["record_kind"] == "rejection"

def test_durable_quorum_tamper_fails_on_replay():
    with tempfile.TemporaryDirectory() as root:
        store=FileObjectStore(root); result=DurableQuorumLedger(store).persist(decision()); path=store._path(result["records"][0]["record_id"]); path.write_text("{}")
        with pytest.raises(CoreContractError) as error: FileObjectStore(root).verify_manifest()
        assert error.value.code == "E_AUDIT_TAMPER"
