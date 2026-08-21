# Work Package Q1 Release Boundary

## Decision

Q1 is an **offline verification-harness release candidate**. It extends the Core Contract with deterministic request, response, policy, equivalence, and decision behavior. It does not authorize a distributed consensus service, live node discovery, key download, network transport, leader election, storage replication, or production key custody.

## Included

The candidate includes the Python quorum adapter, its exact DSSE fixture binding profile, active-key and policy checks, duplicate-identity handling, equivocation detection, deterministic response ordering, typed decision statuses, the Q1 security-audit harness, the published Q0 adversarial corpus, and the Rust parity baseline.

## Excluded

Ed25519 or other production public-key profiles, rotation and revocation operations, HSM custody, remote key discovery, live transparency-log replication, operational incident response, availability/liveness guarantees, Byzantine fault tolerance, and claims about the physical truth of any geometric or tensor result remain outside this candidate.

## Supported decision statuses

| Status | Meaning |
|---|---|
| `threshold_verified` | The declared threshold of unique active identities reproduced one compatible verified core result. |
| `threshold_failed` | The declared threshold reproduced one compatible named predicate failure. |
| `threshold_unverifiable` | A compatible threshold of responses shared a prerequisite limitation; no affirmative claim is made. |
| `contested` | Trusted responses conflict or a signer equivocates; no automatic winner is selected. |
| `insufficient_quorum` | Fewer than the declared threshold of eligible identities remain. |

## Promotion condition

The Q1 candidate may advance only after semantic agreement, cryptographic binding, audit integration, adversarial confidence, and operational review have evidence artifacts. Until the operational review passes, all documentation must use the phrase **offline verification harness**.
