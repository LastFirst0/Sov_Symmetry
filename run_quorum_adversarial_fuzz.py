"""Deterministic adversarial campaign for the pure local Q0 aggregator."""
from __future__ import annotations

import base64
import copy
import itertools
import json
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from sov_evidence_geometry_core.canonical import canonicalize
from sov_evidence_geometry_core.errors import CoreContractError
from sov_evidence_geometry_core.quorum import DSSE_PAYLOAD_TYPE, aggregate, build_fixture_response, fixture_sign

SEED = 0x51554F52554D5F51


def setup():
    request = {
        "request_id": "quorum:sha256:adversarial-fixture",
        "contract_version": "sov.core.contract.v0.1",
        "operation_id": "metric.inverse.v1",
        "predicate_id": "metric.inverse.identity.v1",
        "convention_profile_id": "convention:standard.v1",
        "scalar_policy_id": "scalar:exact.v1",
        "tolerance_policy_id": "tolerance:exact.v1",
    }
    secrets = {f"key-{letter}": f"q0-secret-{letter}".encode() for letter in "abc"}
    policy = {
        "policy_id": "policy:fixture-q0-2of3-adversarial",
        "threshold": 2,
        "candidates": [
            {"key_id": key, "node_id": f"node-{key[-1]}", "status": "active", "algorithm": "hmac-sha256-fixture-only", "fixture_secret_b64": base64.b64encode(secret).decode()}
            for key, secret in secrets.items()
        ],
    }
    return request, policy, secrets


def response(request, policy, secrets, key, output="sov:sha256:ok", tag="base"):
    return build_fixture_response(request=request, policy=policy, key_id=key, secret=secrets[key], status="verified", output_ids=(output,), reason_codes=("VERIFIED",), response_tag=tag)


def main():
    rng = random.Random(SEED)
    request, policy, secrets = setup()
    counts = {"duplicate_identity_cases": 0, "equivocation_cases": 0, "order_cases": 0, "binding_mutations": 0, "signature_mutations": 0, "invalid_policy_cases": 0}
    failures = []

    for index in range(2000):
        chosen = [rng.choice(["key-a", "key-b", "key-c"]) for _ in range(rng.randrange(2, 7))]
        responses = [response(request, policy, secrets, key, tag=f"same-{index}-{position}") for position, key in enumerate(chosen)]
        decision = aggregate(policy, request, responses)
        accepted = decision["body"]["accepted_response_ids"]
        if len(accepted) != len(set(accepted)):
            failures.append({"kind": "duplicate_accepted_response_id", "case": index})
        if len(set(chosen)) < len(chosen):
            counts["duplicate_identity_cases"] += 1

    for index in range(2000):
        key = rng.choice(["key-a", "key-b", "key-c"])
        other = rng.choice([candidate for candidate in ["key-a", "key-b", "key-c"] if candidate != key])
        response_a = response(request, policy, secrets, key, output=f"sov:sha256:out-{index}-a", tag=f"eq-a-{index}")
        response_b = response(request, policy, secrets, key, output=f"sov:sha256:out-{index}-b", tag=f"eq-b-{index}")
        response_c = response(request, policy, secrets, other, output=f"sov:sha256:out-{index}-b", tag=f"eq-c-{index}")
        decision = aggregate(policy, request, [response_a, response_b, response_c])
        if decision["body"]["decision_status"] != "contested" or not decision["body"]["equivocation_evidence"]:
            failures.append({"kind": "equivocation_not_contested", "case": index, "decision": decision})
        counts["equivocation_cases"] += 1

    base = [response(request, policy, secrets, "key-a"), response(request, policy, secrets, "key-b"), response(request, policy, secrets, "key-c")]
    baseline = aggregate(policy, request, base)["decision_id"]
    for index in range(1000):
        permutation = list(base)
        rng.shuffle(permutation)
        observed = aggregate(policy, request, permutation)["decision_id"]
        if observed != baseline:
            failures.append({"kind": "order_dependence", "case": index, "observed": observed, "baseline": baseline})
        counts["order_cases"] += 1

    for index in range(1000):
        mutated = copy.deepcopy(response(request, policy, secrets, "key-a", tag=f"mut-{index}"))
        payload = mutated["payload"]
        if index % 2 == 0:
            payload["request_id"] = f"quorum:sha256:wrong-{index}"
            counts["binding_mutations"] += 1
        else:
            payload["output_ids"] = [f"sov:sha256:mutated-{index}"]
            counts["signature_mutations"] += 1
        payload_bytes = canonicalize(payload)
        mutated["envelope"]["payload"] = base64.b64encode(payload_bytes).decode()
        if index % 2 == 0:
            mutated["envelope"]["signatures"][0]["sig"] = fixture_sign(DSSE_PAYLOAD_TYPE, payload_bytes, secrets["key-a"])
        else:
            mutated["envelope"]["signatures"][0]["sig"] = base64.b64encode(b"wrong-signature").decode()
        decision = aggregate(policy, request, [mutated, response(request, policy, secrets, "key-b", tag=f"mut-b-{index}")])
        if decision["body"]["decision_status"] not in {"threshold_verified", "insufficient_quorum"}:
            failures.append({"kind": "unexpected_mutation_decision", "case": index, "decision": decision})

    for index in range(100):
        bad = copy.deepcopy(policy)
        if index % 2 == 0:
            bad["threshold"] = 0
        else:
            bad["candidates"] = bad["candidates"] + [copy.deepcopy(bad["candidates"][0])]
        try:
            aggregate(bad, request, base)
            failures.append({"kind": "invalid_policy_accepted", "case": index})
        except CoreContractError:
            counts["invalid_policy_cases"] += 1

    report = {"schema": "sov.quorum.adversarial_fuzz_report", "version": "0.1.0", "seed": SEED, "counts": counts, "failures": failures, "total_cases": sum(counts.values())}
    Path(sys.argv[1]).write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    raise SystemExit(2 if failures else 0)


if __name__ == "__main__":
    main()
