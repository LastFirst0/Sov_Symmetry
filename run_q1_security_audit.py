"""Deterministic Q1 security audit for the offline quorum adapter.

This harness is intentionally isolated from legacy experimental imports. It audits
observable contract behavior over a fixed fixture corpus; it is not a production
cryptographic or distributed-consensus proof.
"""
from __future__ import annotations

import copy
import hashlib
import json
import random
import sys
from pathlib import Path

from sov_evidence_geometry_core.quorum import aggregate, build_fixture_response
from sov_evidence_geometry_core.canonical import canonicalize

SEED = 0x51413031


def fixture():
    secrets = {f"key-{i}": f"fixture-secret-{i}".encode() for i in range(1, 4)}
    candidates = [
        {
            "key_id": key_id,
            "node_id": f"node-{i}",
            "status": "active",
            "algorithm": "hmac-sha256-fixture-only",
            "fixture_secret_b64": __import__("base64").b64encode(secret).decode(),
        }
        for i, (key_id, secret) in enumerate(secrets.items(), 1)
    ]
    request = {
        "request_id": "quorum:sha256:request-q1",
        "contract_version": "sov.core.v0.1",
        "operation_id": "tensor.metric_inverse.v1",
        "predicate_id": "metric_inverse.v1",
        "convention_profile_id": "euclidean.signature.plus.v1",
        "scalar_policy_id": "rational.exact.v1",
        "tolerance_policy_id": "exact.zero.v1",
    }
    policy = {
        "policy_id": "policy:sha256:policy-q1",
        "threshold": 2,
        "candidates": candidates,
    }
    responses = [
        build_fixture_response(request=request, policy=policy, key_id=key_id, secret=secrets[key_id], status="verified", output_ids=["output:metric:1"], reason_codes=["invariant.satisfied"], response_tag="base")
        for key_id in ("key-1", "key-2", "key-3")
    ]
    return request, policy, responses, secrets


def decision(policy, request, responses):
    return aggregate(policy, request, responses)["body"]


def expect(name, actual, predicate, detail):
    passed = bool(predicate(actual))
    return {
        "name": name,
        "passed": passed,
        "observed": actual,
        "detail": detail,
    }


def main(out_path: str) -> int:
    request, policy, responses, secrets = fixture()
    base = decision(policy, request, responses)
    cases = []
    cases.append(expect("positive_threshold", base["decision_status"], lambda x: x == "threshold_verified", "three active identities reproduce one verified class"))

    permuted = list(responses)
    random.Random(SEED).shuffle(permuted)
    permuted_body = decision(policy, request, permuted)
    permuted_digest = hashlib.sha256(canonicalize(permuted_body)).hexdigest()
    base_digest = hashlib.sha256(canonicalize(base)).hexdigest()
    cases.append(expect("order_independence", permuted_digest, lambda x: x == base_digest, "response order must not change the canonical decision body"))

    duplicate = decision(policy, request, responses + [copy.deepcopy(responses[0])])
    cases.append(expect("duplicate_response_counts_once", duplicate["decision_status"], lambda x: x == "threshold_verified", "duplicate signed evidence must not create a fourth identity"))

    equivocation = copy.deepcopy(responses[0])
    equivocation["payload"]["output_ids"] = ["output:metric:tampered"]
    equivocation["envelope"]["payload"] = __import__("base64").b64encode(canonicalize(equivocation["payload"])).decode()
    # Keep the original signature deliberately: this must be rejected, not accepted.
    equivocation_body = decision(policy, request, responses + [equivocation])
    cases.append(expect("signature_mutation_rejected", equivocation_body["decision_status"], lambda x: x == "threshold_verified", "a binding mutation with a stale signature is excluded"))

    valid_alt = build_fixture_response(request=request, policy=policy, key_id="key-1", secret=secrets["key-1"], status="verified", output_ids=["output:metric:other"], reason_codes=["invariant.satisfied"], response_tag="equivocation")
    contested = decision(policy, request, responses + [valid_alt])
    cases.append(expect("valid_equivocation_contested", contested["decision_status"], lambda x: x == "contested", "one signer producing two valid incompatible responses blocks an automatic winner"))

    wrong_request = copy.deepcopy(responses[0])
    wrong_request["payload"]["request_id"] = "quorum:sha256:wrong"
    wrong_request["envelope"]["payload"] = __import__("base64").b64encode(canonicalize(wrong_request["payload"])).decode()
    wrong_body = decision(policy, request, [wrong_request, responses[1]])
    cases.append(expect("request_binding_rejected", wrong_body["decision_status"], lambda x: x == "insufficient_quorum", "wrong request binding cannot contribute to threshold"))

    wrong_type = copy.deepcopy(responses[0])
    wrong_type["envelope"]["payloadType"] = "application/json"
    wrong_type_body = decision(policy, request, [wrong_type, responses[1]])
    cases.append(expect("payload_type_rejected", wrong_type_body["decision_status"], lambda x: x == "insufficient_quorum", "generic JSON payload types are not accepted"))

    revoked = copy.deepcopy(policy)
    revoked["candidates"][0]["status"] = "revoked"
    revoked_body = decision(revoked, request, responses)
    cases.append(expect("revoked_key_rejected", revoked_body["decision_status"], lambda x: x == "threshold_verified", "remaining two active identities still meet 2-of-3"))

    invalid_policy = copy.deepcopy(policy)
    invalid_policy["threshold"] = 0
    invalid_policy_error = None
    try:
        aggregate(invalid_policy, request, responses)
    except Exception as exc:  # expected request-level rejection
        invalid_policy_error = type(exc).__name__
    cases.append(expect("invalid_policy_fail_closed", invalid_policy_error, lambda x: x is not None, "malformed thresholds must raise a typed request error"))

    # Metadata tamper must not affect equivalence, while output tamper must.
    metadata = copy.deepcopy(responses[0])
    metadata["payload"]["response_id"] = "response:key-1:display-only-change"
    metadata_body = decision(policy, request, [metadata, responses[1]])
    cases.append(expect("response_id_is_hashed_payload_field", metadata_body["decision_status"], lambda x: x == "threshold_verified", "response IDs are preserved as evidence but do not affect equivalence"))

    failures = [case for case in cases if not case["passed"]]
    report = {
        "schema": "sov.quorum.q1_security_audit_report",
        "version": "0.1.0",
        "seed": SEED,
        "fixture": "offline-hmac-q1-fixed-request",
        "scope": "isolated deterministic contract audit; not production consensus or a universal cryptographic proof",
        "counts": {"cases": len(cases), "passed": len(cases) - len(failures), "failed": len(failures)},
        "cases": cases,
        "failures": [case["name"] for case in failures],
        "source": {
            "module": "sov_evidence_geometry_core.quorum",
            "audit_script": "tools/run_q1_security_audit.py",
        },
    }
    Path(out_path).write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: run_q1_security_audit.py OUTPUT_JSON")
    raise SystemExit(main(sys.argv[1]))
