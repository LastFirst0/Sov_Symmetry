# Multi-Node Quorum Verification Specification v0.1

**Status:** Proposed subsystem contract.  
**Scope:** Signed aggregation of independent evaluation records for the same immutable Core Contract request.  
**Non-goals:** Consensus ordering, leader election, P2P routing, token economics, Proof-of-Useful-Work, distributed storage, liveness guarantees, or a claim that majority agreement establishes physical truth.

## 1. Model

A verification quorum answers a narrow question: **did at least `t` distinct policy-approved verifier identities produce compatible signed outputs for exactly the same request and contract release?** The answer is an auditable meta-result, not a replacement for the core result and not a distributed consensus decision.

DSSE describes threshold validation in terms of signatures from at least `t` unique trusted public keys; a key hint must not make a security decision. [1] The quorum policy carries this rule forward and rejects duplicate signer identities, stale policies, and incompatible evaluator releases.

## 2. Inputs and identities

| Item | Required fields | Rule |
|---|---|---|
| `verification_request` | `request_id`, ordered input IDs, operation ID, convention profile ID, assumption IDs, contract version, scalar/tolerance profile | `request_id` is `quorum:sha256:<digest(JCS(body))>`; all nodes receive exactly these bytes or a derived immutable request object |
| `verifier_identity` | `node_id`, `key_id`, public key, software release ID, environment class, active policy IDs | One active trusted key counts at most once per policy |
| `verifier_response` | `request_id`, `status`, output IDs, predicate results, reason codes, evaluator release ID, core contract version, signed envelope | Response is invalid if any request binding differs |
| `quorum_policy` | `policy_id`, candidate node/key IDs, threshold, compatibility rules, expiration, revocation reference, diversity constraints | Threshold is `1 ≤ t ≤ n`; policy is immutable and versioned |
| `quorum_decision` | policy/request IDs, accepted/rejected response IDs, equivalence class, decision status, limitation codes | Decision is attested and may be logged; it does not modify responses |

## 3. Compatibility and decision rules

Responses are compatible only when they share: identical `request_id`; Core Contract major/minor version; operation/predicate ID and version; convention profile; scalar and tolerance profile; evaluator release allowed by policy; and identical canonical output IDs for `verified` outcomes. For `fail`, the same predicate must fail under the same residual category. `unverifiable` responses must expose compatible missing/unsupported reason codes but cannot form an affirmative verification quorum.

| Condition | Quorum decision | Meaning |
|---|---|---|
| `t` unique trusted keys sign compatible `verified` responses | `threshold_verified` | A policy threshold reproduced the named core result; it is not a physical validation claim |
| `t` unique trusted keys sign compatible `fail` responses | `threshold_failed` | A policy threshold reproduced a named failed predicate |
| Any accepted response incompatibly differs from a competing accepted class | `contested` | Preserve all evidence; no automatic tie break |
| Fewer than `t` valid unique responses before deadline | `insufficient_quorum` | Availability/liveness limitation, not mathematical failure |
| `t` compatible `unverifiable` responses | `threshold_unverifiable` | The named prerequisite is commonly absent/unsupported; no affirmative claim |
| Signature/key/policy request binding invalid | `rejected_response` | Excluded and preserved in audit trail |

Quorum aggregation MUST be deterministic: order responses by `(key_id, response_id)`, group by a canonical equivalence key, and choose no winning group if more than one group reaches threshold or a policy-defined conflict condition occurs. A policy MAY require an environment diversity tag (for example, separate language/runtime families) but MAY NOT count two keys from the same declared verifier identity as independent.

## 4. Policy baseline

No global production threshold is selected in v0.1. The first test profile is `2-of-3` **offline fixture verification** with three distinct test keys, two independently maintained evaluator paths, and no network service. A production policy requires an approved threat model, key inventory/rotation plan, node operator responsibilities, diversity assessment, incident response, and independent security review. Threshold trust is a mechanism for reducing single-key compromise exposure, not a substitute for those controls. [2] [3]

## 5. Attack and failure cases

| Scenario | Required behavior |
|---|---|
| Duplicate signatures or duplicate keys | Count once; reject duplicate signer record |
| Same key reused under another node ID | Count once by active key policy identity; emit audit event |
| Stale/revoked key or expired policy | Reject response; do not silently downgrade threshold |
| Different core contract or convention profile | `contested` if otherwise trusted; no grouping |
| Different result output IDs | `contested`, even when textual explanations agree |
| Compromised threshold of keys | Raise critical incident; freeze policy promotion and rotate/re-establish trust out of band |
| Network partition/DoS | `insufficient_quorum`; no retry loop may manufacture a result |
| Verifier equivocation | Preserve both signed responses and generate audit event; never discard the minority response |

## 6. Required conformance tests

The first implementation must test: valid `2-of-3` compatible verified quorum; duplicate-key non-counting; wrong request hash; wrong payload type; stale policy; revoked key; same result status but different output IDs; cross-version incompatibility; threshold failure; threshold unverifiable; signer equivocation; deterministic order independence; and integration with an audit attestation. No P2P or consensus test is in scope until the separate distributed-protocol specification and threat model exist.

## 7. API boundary

The v0.1 local interface is `aggregate(policy, request, responses) -> quorum_decision`. It accepts already verified response envelopes and a locally available policy. It performs no network discovery, key download, dynamic code execution, or storage mutation other than emitting a return value/audit event through an explicit adapter.

## References

[1] [DSSE Protocol v1.0.2](https://github.com/secure-systems-lab/dsse/blob/master/protocol.md)  
[2] [The Update Framework Specification](https://theupdateframework.github.io/specification/latest/)  
[3] [NIST SP 800-57 Part 1 Rev. 5](https://csrc.nist.gov/pubs/sp/800/57/pt1/r5/final)
