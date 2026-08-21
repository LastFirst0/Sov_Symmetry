import base64
import itertools
import unittest

from sov_evidence_geometry_core.canonical import canonicalize
from sov_evidence_geometry_core.quorum import DSSE_PAYLOAD_TYPE, aggregate, build_fixture_response, fixture_sign



class QuorumFixtureTests(unittest.TestCase):
    def setUp(self):
        self.request = {
            "request_id": "quorum:sha256:request-fixture",
            "contract_version": "sov.core.contract.v0.1",
            "operation_id": "metric.inverse.v1",
            "predicate_id": "metric.inverse.identity.v1",
            "convention_profile_id": "convention:standard.v1",
            "scalar_policy_id": "scalar:exact.v1",
            "tolerance_policy_id": "tolerance:exact.v1",
        }
        secrets = {"key-a": b"fixture-secret-a", "key-b": b"fixture-secret-b", "key-c": b"fixture-secret-c"}
        self.secrets = secrets
        self.policy = {
            "policy_id": "policy:fixture-q0-2of3",
            "threshold": 2,
            "candidates": [
                {"key_id": key, "node_id": f"node-{key[-1]}", "status": "active", "algorithm": "hmac-sha256-fixture-only", "fixture_secret_b64": base64.b64encode(secret).decode("ascii")}
                for key, secret in secrets.items()
            ],
        }

    def response(self, key, status="verified", output_ids=("sov:sha256:result-ok",), reason_codes=("VERIFIED",), tag="default"):
        return build_fixture_response(request=self.request, policy=self.policy, key_id=key, secret=self.secrets[key], status=status, output_ids=output_ids, reason_codes=reason_codes, response_tag=tag)

    def test_threshold_verified(self):
        decision = aggregate(self.policy, self.request, [self.response("key-a"), self.response("key-b"), self.response("key-c")])
        self.assertEqual(decision["body"]["decision_status"], "threshold_verified")
        self.assertEqual(len(decision["body"]["accepted_response_ids"]), 3)

    def test_order_independence(self):
        responses = [self.response("key-a"), self.response("key-b"), self.response("key-c")]
        decisions = {aggregate(self.policy, self.request, order)["decision_id"] for order in itertools.permutations(responses)}
        self.assertEqual(decisions, {aggregate(self.policy, self.request, responses)["decision_id"]})

    def test_duplicate_same_identity_counts_once(self):
        responses = [self.response("key-a"), self.response("key-a"), self.response("key-b")]
        decision = aggregate(self.policy, self.request, responses)
        self.assertEqual(decision["body"]["decision_status"], "threshold_verified")
        self.assertEqual(len(decision["body"]["accepted_response_ids"]), 2)

    def test_equivocation_contests_even_with_threshold(self):
        responses = [self.response("key-a", output_ids=("sov:sha256:result-a",), tag="a"), self.response("key-a", output_ids=("sov:sha256:result-b",), tag="b"), self.response("key-b")]
        decision = aggregate(self.policy, self.request, responses)
        self.assertEqual(decision["body"]["decision_status"], "contested")
        self.assertEqual(len(decision["body"]["equivocation_evidence"]), 1)

    def test_one_qualifying_output_class_wins_over_nonqualifying_minority(self):
        responses = [self.response("key-a"), self.response("key-b", output_ids=("sov:sha256:result-other",), tag="different"), self.response("key-c", output_ids=("sov:sha256:result-other",), tag="different")]
        decision = aggregate(self.policy, self.request, responses)
        self.assertEqual(decision["body"]["decision_status"], "threshold_verified")

    def test_wrong_request_binding_rejected(self):
        response = self.response("key-a")
        response["payload"]["request_id"] = "quorum:sha256:wrong"
        payload_bytes = canonicalize(response["payload"])
        response["envelope"]["payload"] = base64.b64encode(payload_bytes).decode("ascii")
        response["envelope"]["signatures"][0]["sig"] = fixture_sign(DSSE_PAYLOAD_TYPE, payload_bytes, self.secrets["key-a"])
        decision = aggregate(self.policy, self.request, [response, self.response("key-b")])
        self.assertEqual(decision["body"]["decision_status"], "insufficient_quorum")
        self.assertEqual(decision["body"]["rejected"][0]["code"], "E_REQUEST_BINDING")

    def test_stale_key_rejected(self):
        stale = dict(self.policy)
        stale["candidates"] = [dict(candidate) for candidate in self.policy["candidates"]]
        stale["candidates"][0]["status"] = "revoked"
        decision = aggregate(stale, self.request, [self.response("key-a"), self.response("key-b")])
        self.assertEqual(decision["body"]["decision_status"], "insufficient_quorum")
        self.assertEqual(decision["body"]["rejected"][0]["code"], "E_KEY_REJECTED")

    def test_failed_predicate_threshold(self):
        decision = aggregate(self.policy, self.request, [self.response("key-a", status="fail", output_ids=(), reason_codes=("E_PREDICATE_FAILED",)), self.response("key-b", status="fail", output_ids=(), reason_codes=("E_PREDICATE_FAILED",))])
        self.assertEqual(decision["body"]["decision_status"], "threshold_failed")


if __name__ == "__main__":
    unittest.main()
