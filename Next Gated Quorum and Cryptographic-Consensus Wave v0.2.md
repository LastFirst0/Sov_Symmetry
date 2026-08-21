# Next Gated Quorum and Cryptographic-Consensus Wave v0.2

**Status:** Implementation design; not an authorization to deploy a distributed consensus service.  
**Objective:** Extend the deterministic Core Contract with an offline, policy-governed aggregation layer that can prove whether distinct verifier identities produced compatible results for the same immutable request. The wave must produce auditable evidence for agreement, conflict, key/policy rejection, and insufficient availability without changing the underlying core verdict.

## 1. Boundary and non-goals

The wave is a **verification protocol** before it is a distributed system. It accepts already validated Core Contract requests, already evaluated response envelopes, immutable key/policy records, and explicit audit adapters. It does not discover nodes, elect leaders, order a network log, replicate storage, guarantee liveness, select a block producer, mint tokens, or infer physical truth. “Consensus” in this document means agreement evidence under a declared trust policy; it does not mean Byzantine consensus.

The first implementation profile is an offline `2-of-3` fixture profile with three distinct verifier identities, two evaluator paths, a fixed request, fixed policy, fixed release IDs, and deterministic response ordering. The network and key-custody surfaces are represented only by fixtures until their threat model and operational owner are accepted.

## 2. Protocol objects

| Object | Canonical subject | Required identity or binding |
|---|---|---|
| `verification_request` | Core operation ID, ordered input IDs, convention profile, assumptions, scalar/tolerance profiles, contract version | `quorum:sha256:<JCS(body)>`; exact bytes bind every response |
| `verifier_identity` | Node ID, active key ID, software release, environment class, policy memberships | Key identity counts once; node aliases cannot create independence |
| `verifier_response` | Request ID, core status, output IDs, reason codes, scope, evaluator release, audit-event ID | DSSE payload binds exact response bytes and payload type |
| `quorum_policy` | Policy ID, candidate keys/nodes, threshold, compatibility profile, validity/revocation state, diversity rules | Immutable `policy:sha256:<JCS(body)>` |
| `quorum_decision` | Request/policy IDs, accepted/rejected response IDs, equivalence classes, decision status, limitations | Derived `quorum_decision:sha256:<JCS(body)>`; never mutates responses |
| `equivocation_evidence` | Same signer/request with incompatible signed responses or same log/tree size with conflicting roots | References both immutable artifacts; raises a critical incident |

All signed payloads use a DSSE type that names exact encoding and schema. Generic `application/json` is prohibited. Core object IDs and audit IDs remain independent of signatures, timestamps, transport addresses, and dashboard labels.

## 3. Compatibility and equivalence

A response is eligible only if its signature, key, policy, request ID, contract version, operation ID/version, convention profile, scalar policy, tolerance policy, evaluator release, and payload hash are valid. Responses are grouped by a canonical equivalence key:

```text
(request_id,
 core_contract_version,
 operation_id/version,
 predicate_id/version,
 convention_profile_id,
 scalar_policy_id,
 tolerance_policy_id,
 result_status,
 output_ids,
 reason_code_class,
 verification_scope)
```

`verified` responses require identical output IDs and compatible verification scope. `fail` responses require the same predicate failure class and compatible residual category. `unverifiable` responses cannot form an affirmative quorum; they may form `threshold_unverifiable` only when their missing/unsupported reason class is compatible.

A response with the same text explanation but a different output ID is incompatible. Two keys attached to one active verifier identity count once. A key hint, node label, or transport address never makes a response trusted.

## 4. Deterministic decision function

The local API is:

```text
aggregate(policy, request, responses) -> quorum_decision
```

The function performs no I/O, discovery, key download, dynamic code execution, clock lookup, or storage mutation. It sorts candidate responses by `(active_key_id, response_id)`, rejects invalid or stale inputs while preserving rejection evidence, groups compatible responses, and applies the policy threshold.

| Condition | Decision | Required meaning |
|---|---|---|
| `t` unique active trusted keys sign one compatible `verified` class | `threshold_verified` | Threshold reproduced the named core result |
| `t` unique active trusted keys sign one compatible `fail` class | `threshold_failed` | Threshold reproduced a named failed predicate |
| `t` compatible `unverifiable` responses | `threshold_unverifiable` | Prerequisite absence is common; no affirmative claim |
| Multiple incompatible classes or valid equivocation | `contested` | Preserve all classes; no automatic winner |
| Fewer than `t` eligible responses | `insufficient_quorum` | Availability limitation, not predicate failure |
| Invalid signature, key, policy, request binding, or payload type | `rejected_response` | Excluded but preserved as evidence |

A policy must define whether environment diversity is required. Diversity is a declared anti-common-mode-failure constraint, not proof of independence. If two groups reach threshold under conflicting classes, the result is `contested`.

## 5. Cryptographic protocol profiles

### Profile A: signed response fixture

Each verifier signs a DSSE envelope over the exact canonical response payload. The response must reference the immutable request ID, core evidence ID, evaluator release, policy ID, and verification scope. The verifier key is selected by the immutable key policy; a payload key hint is advisory only.

### Profile B: checkpoint attestation fixture

The local transparency-log checkpoint is separately attested. A quorum decision may reference the checkpoint ID and inclusion proof, but the quorum layer does not own tree ordering. Two valid checkpoint roots for the same `log_id` and `tree_size` create equivocation evidence and block release promotion.

### Profile C: threshold decision fixture

The decision itself may be signed by one release attestor only after the underlying response threshold and policy checks pass. Multi-signature decision attestation is an additive profile. It cannot hide rejected responses or replace the response-level evidence.

No production algorithm is selected by the Core Contract. The first fixture profile may use Ed25519 for deterministic offline tests, but algorithm selection, key encoding, rotation, revocation, compromise recovery, and hardware custody require the separate key-management policy and security review.

## 6. Failure and adversarial matrix

| Attack or failure | Required result |
|---|---|
| Duplicate signature or duplicate active key | Count once; preserve duplicate evidence |
| Same key under another node ID | Count once; emit identity-alias event |
| Stale, expired, or revoked key/policy | `rejected_response`; never silently lower threshold |
| Wrong request ID or payload type | `rejected_response` |
| Same status, different outputs | `contested` if trusted; never choose by arrival order |
| Different contract/convention/scalar/tolerance release | Incompatible class; `contested` if competing trusted class exists |
| Verifier sends two incompatible valid responses | `contested` plus equivocation evidence |
| Missing nodes, timeout, or partition | `insufficient_quorum`; no retry may manufacture agreement |
| Compromised threshold | Critical incident; freeze promotion and rotate trust out of band |
| Malformed policy threshold (`t=0`, `t>n`, duplicate candidates) | Request error; no decision record |
| Order permutation | Byte-identical decision and reason codes |
| Same result with different audit metadata | Core equivalence remains same; audit metadata cannot change grouping |

## 7. Implementation work packages

| Work package | Scope | Exit gate |
|---|---|---|
| Q0 | Freeze policy/schema/identity decisions and add ADR | Accepted protocol and threat-model deltas |
| Q1 | Implement pure request/response/policy schemas and canonical equivalence key | Schema and semantic negative suite passes |
| Q2 | Implement deterministic local aggregator and decision records | 2-of-3 positive, failure, unverifiable, contested, and insufficient fixtures pass |
| Q3 | Implement offline DSSE/key-policy verifier adapter | Payload binding, key status, duplicate identity, and revocation fixtures pass |
| Q4 | Integrate audit events/checkpoints/proofs | Every decision references immutable evidence and replayable audit proofs |
| Q5 | Adversarial model and property/fuzz campaigns | No unexplained collision, nondeterminism, or fail-open path |
| Q6 | Go/no-go review | No production network/quorum release without security, operations, and incident gates |

## 8. Required promotion gates

**QG1 — semantic agreement:** schemas, canonical equivalence, and typed decision statuses are accepted.  
**QG2 — cryptographic binding:** DSSE payload type, exact bytes, key policy, revocation, and duplicate identity rules are tested.  
**QG3 — audit integration:** quorum decisions replay against durable evidence and audit checkpoints; equivocation is preserved.  
**QG4 — adversarial confidence:** fuzz/property suite runs at a fixed seed corpus and produces no unexplained identity collision, decision nondeterminism, or fail-open result.  
**QG5 — operational decision:** threat model, key lifecycle, node responsibility, incident severity, retention, rollback, and security review are accepted.

Until QG5 passes, the subsystem is an offline verification harness only.

## References

[1] [DSSE Protocol](https://github.com/secure-systems-lab/dsse/blob/master/protocol.md)  
[2] [The Update Framework Specification](https://theupdateframework.github.io/specification/latest/)  
[3] [NIST SP 800-57 Part 1 Rev. 5](https://csrc.nist.gov/pubs/sp/800/57/pt1/r5/final)  
[4] [RFC 6962: Certificate Transparency](https://www.rfc-editor.org/info/rfc6962/)  
[5] [RFC 9162: Certificate Transparency Version 2.0](https://www.rfc-editor.org/info/rfc9162)

## References

[1] [DSSE Protocol v1.0.2](https://github.com/secure-systems-lab/dsse/blob/master/protocol.md)  
[2] [The Update Framework Specification](https://theupdateframework.github.io/specification/latest/)  
[3] [NIST SP 800-57 Part 1 Rev. 5](https://csrc.nist.gov/pubs/800-57/pt1/r5/final)  
[4] [RFC 6962: Certificate Transparency](https://www.rfc-editor.org/info/rfc6962)  
[5] [RFC 9162: Certificate Transparency Version 2.0](https://www.rfc-editor.org/info/rfc9162)
