# Q1 Threat Model

## System under review

The subject is the deterministic local aggregation function `aggregate(policy, request, responses)`. It consumes already-formed Core Contract requests, signed response envelopes, and an immutable quorum policy. It performs no network I/O, key discovery, clock lookup, storage mutation, or dynamic code execution.

## Assets

The primary assets are the canonical request bytes, response payload bytes, DSSE payload type, active key-to-identity mapping, policy threshold, decision body, rejection evidence, and equivocation evidence. Integrity and provenance matter more than availability in this wave.

## Trust boundaries

The code-owned operation and predicate registry is trusted application code. Fixture policy and response data are untrusted inputs. The HMAC profile is a test-only binding mechanism and must not be interpreted as production key security. The durable audit store is a separate boundary: Q1 references it conceptually but does not claim integrated checkpoint persistence.

## Adversaries and abuse cases

| Adversary or failure | Required defensive behavior |
|---|---|
| Mutated request or policy binding | Reject the response or produce insufficient quorum. |
| Stale, revoked, unknown, or unsupported key | Preserve rejection evidence and exclude the response. |
| Duplicate response or identity alias | Count one identity once and preserve duplicate evidence. |
| One signer emits incompatible valid responses | Produce `contested` and equivocation evidence. |
| Different output IDs under the same status | Never choose by arrival order; preserve competing classes. |
| Invalid threshold or duplicate policy candidates | Raise a typed request error; create no decision. |
| Response reordering | Produce a byte-identical decision body and decision ID. |
| Verifier exception or malformed envelope | Fail closed; do not produce an affirmative threshold result. |
| Conflicting equal-size audit roots | Block promotion and preserve both artifacts for incident review. |

## Out of scope

Q1 does not assess private-key extraction, HSM compromise, side-channel resistance, network partition behavior, quorum liveness, Sybil resistance in a live registry, operator collusion, or the semantic validity of the underlying geometry. These require QG5 operational review and separate empirical evidence.

## Severity policy

Any unexpected affirmative decision, identity double-count, request-binding acceptance, order-dependent decision, or lost equivocation artifact is release-blocking. A known limitation or unsupported profile is not a defect when it is explicitly marked and gated.
