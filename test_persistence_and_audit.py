"""Durability and audit primitives tests for the Core Contract reference package."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from sov_evidence_geometry_core import derive_id
from sov_evidence_geometry_core.audit import LocalTransparencyLog, build_audit_event, dsse_pae
from sov_evidence_geometry_core.errors import CoreContractError
from sov_evidence_geometry_core.persistence import FileObjectStore


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
    body = {"schema": "sov.core.object", "schema_version": "0.1.0", "object_kind": kind, "convention_profile": PROFILE, "assumptions": [], "content": content}
    return {"id": derive_id(body), "canonical_body": body}


class DurableStoreTests(unittest.TestCase):
    def test_clean_reopen_replays_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            store = FileObjectStore(directory)
            manifold = envelope("manifold", {"name": "M1", "dimension": 1, "orientation_mode": "declared", "signature": {"positive": 1, "negative": 0, "zero": 0}})
            store.put(manifold)
            chart = envelope("chart", {"manifold_id": manifold["id"], "name": "x", "coordinates": ["x0"]})
            store.put(chart)
            first_root = store.verify_manifest()
            reopened = FileObjectStore(directory)
            self.assertEqual(reopened.get(chart["id"]), chart)
            self.assertEqual(reopened.verify_manifest(), first_root)

    def test_tampered_record_is_detected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            store = FileObjectStore(directory)
            manifold = envelope("manifold", {"name": "M1", "dimension": 1, "orientation_mode": "declared", "signature": {"positive": 1, "negative": 0, "zero": 0}})
            object_id = store.put(manifold)
            store._path(object_id).write_text('{"id":"tampered"}', encoding="utf-8")
            with self.assertRaisesRegex(CoreContractError, "E_AUDIT_TAMPER|E_SCHEMA_INVALID"):
                store.verify_manifest()


class AuditPrimitiveTests(unittest.TestCase):
    def event(self, number: int) -> dict:
        return build_audit_event(
            event_type="core_evidence_attested",
            core_evidence_id=f"sov:sha256:{number:064x}",
            actor_role="release_attestor",
            release_id="release:core-v0.1.0",
            policy_id="policy:sha256:" + "a" * 64,
            payload_hash="sha256:" + "b" * 64,
            sequence_hint=number,
        )

    def test_dsse_pae_matches_protocol_vector(self) -> None:
        self.assertEqual(dsse_pae("http://example.com/helloworld", b"hello world"), b"DSSEv1 29 http://example.com/helloworld 11 hello world")

    def test_inclusion_and_consistency_proofs_verify_and_tampering_fails(self) -> None:
        log = LocalTransparencyLog()
        events = [self.event(number) for number in range(3)]
        log.append(events[0])
        first = log.checkpoint(policy_id="policy:sha256:" + "a" * 64, issued_at_utc="2026-08-17T00:00:00Z")
        log.append(events[1])
        log.append(events[2])
        latest = log.checkpoint(policy_id="policy:sha256:" + "a" * 64, issued_at_utc="2026-08-17T00:01:00Z", previous_checkpoint_id=first["id"])
        proof = log.inclusion_proof(1)
        self.assertTrue(LocalTransparencyLog.verify_inclusion(events[1], proof, latest))
        tampered = dict(proof)
        tampered["leaf_hash"] = "sha256:" + "0" * 64
        self.assertFalse(LocalTransparencyLog.verify_inclusion(events[1], tampered, latest))
        consistency = log.consistency_proof(1)
        self.assertTrue(LocalTransparencyLog.verify_consistency(first, latest, consistency))
        consistency["appended_leaf_hashes"][0] = "sha256:" + "0" * 64
        self.assertFalse(LocalTransparencyLog.verify_consistency(first, latest, consistency))
