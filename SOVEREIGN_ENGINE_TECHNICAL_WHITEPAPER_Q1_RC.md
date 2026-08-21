# Sovereign Engine: Geometry-Native Verification Architecture and Q1 Release Candidate

**Author:** Manus AI  
**Status:** Q1 offline verification-harness release candidate  
**Date:** 2026-08-17

## Abstract

The Sovereign Engine is being developed as a geometry-native, provenance-aware reasoning platform. Its central engineering claim is deliberately narrower than its research ambition: a small deterministic kernel can make geometric and tensor-calculus results replayable, content-addressed, and auditable when every operation, input, invariant, and limitation is explicit. The platform therefore separates a meaning layer from a trusted computational kernel, and separates kernel verdicts from multi-identity agreement evidence.

This whitepaper documents the current architecture, the Core Contract v0.1 boundary, the local quorum protocol, the Q0 adversarial campaign, the Q1 security-audit oracle, and the release-candidate evidence package. It also states what the evidence does not establish. In particular, the current implementation is an offline verification harness, not Byzantine consensus, not a production public-key system, and not a proof that any Geometric Unity hypothesis or physical interpretation is true.

## 1. Program thesis and evidence posture

The meaning layer translates technical concepts into stable records: names, symbols, source spans, normalized notation, claim class, dependencies, examples, and verification obligations. The kernel consumes only typed, canonical inputs. The evidence layer records immutable core objects, derived IDs, typed statuses, and replay information. The quorum layer answers a different question: whether distinct declared identities produced compatible evidence for the same request under a fixed policy.

> A quorum decision is agreement evidence under a declared trust policy; it is not a physical-truth oracle.

The program uses five evidence classes: mathematical fact, tested software contract, measured benchmark, modeled projection, and research hypothesis. This classification prevents a successful fixture replay from being presented as a theorem, and prevents a geometric research conjecture from entering the trusted kernel as if it were established mathematics.

## 2. Architecture spine

| Layer | Responsibility | Current evidence | Boundary |
|---|---|---|---|
| Meaning layer | Decode concepts, equations, variables, source spans, and hypotheses into a machine-readable registry. | Transcript inventory, tensor deep dive, architecture artifacts. | Does not certify truth by naming or visualization. |
| Core Contract | Canonicalize requests and outputs, derive content IDs, validate schemas, and evaluate registered invariants. | Python reference SDK and Rust parity crate. | Does not discover operations or execute callbacks from evidence. |
| Durable evidence | Store immutable objects, manifests, audit events, Merkle checkpoints, and proofs. | Local file store and audit primitives. | Current quorum integration remains a release blocker. |
| Local quorum | Validate signed response fixtures, policy membership, identity uniqueness, equivalence, threshold, and equivocation. | Q0 implementation, Q1 audit, Q0 fuzz campaign. | No network, liveness, leader election, or production key custody. |
| Documentation and control plane | Present workstreams, artifacts, claims, limitations, release gates, and next wave. | Mission Control Ledger and this whitepaper. | Presentation cannot substitute for replayable evidence. |

## 3. Core Contract and geometry meaning layer

The Core Contract uses canonical JSON serialization and SHA-256 content addressing. An operation has an explicit operation ID and version, canonical inputs, a code-owned predicate registry, and a typed result status: `verified`, `fail`, or `unverifiable`. Invariant checks can establish structural properties such as tensor symmetry, metric-inverse relationships, or exact rational identities. They cannot establish semantic or physical meaning without a separately verified bridge.

The meaning layer is the interpretive boundary. For each term or equation it should preserve the original source span, normalized notation, variable roles, dimensions or index positions, convention profile, assumptions, claim class, and a test or falsification obligation. This is where concepts such as metric tensors, inverse metrics, curvature, torsion, fiber variables, and symmetry claims become digestible without being silently promoted from hypothesis to fact.

## 4. Quorum protocol

The local API is:

```text
aggregate(policy, request, responses) -> quorum_decision
```

A response is eligible only when its DSSE payload type, exact canonical bytes, key, policy, request binding, contract version, operation and predicate versions, convention profile, scalar policy, tolerance policy, evaluator release, and payload hash satisfy the declared profile. Compatible responses are grouped by a canonical equivalence key that includes request identity, contract and operation versions, predicate identity, conventions, scalar and tolerance policies, result status, output IDs, reason-code class, and verification scope.

The decision statuses are deliberately typed. A verified threshold reproduces a named core result. A failed threshold reproduces a named failed predicate. An unverifiable threshold records a common prerequisite limitation and makes no affirmative claim. A contested result preserves incompatible classes or valid signer equivocation. Insufficient quorum records an availability limitation rather than predicate failure. Rejected responses remain evidence and do not silently lower the threshold.

## 5. Q0 adversarial evidence

The published deterministic campaign exercised 5,750 cases: 1,650 duplicate-identity cases, 2,000 equivocation cases, 1,000 response-order permutations, 500 request-binding mutations, 500 signature mutations, and 100 invalid-policy cases. The report recorded zero unexplained failures. The focused Python quorum, persistence, audit, and fuzz-regression suite replayed 14 tests successfully in the isolated collection path; the Rust parity crate replayed two unit/parity tests successfully.

These results support a bounded tested-contract claim: the named implementation matched its expected outcomes over the named fixture corpus. They do not prove universal collision resistance, production cryptographic security, Byzantine consensus, independence of operators, or truth of the underlying geometry.

## 6. Q1 security audit

The Q1 harness adds an independent oracle over ten cases: positive threshold, response-order independence, duplicate-response counting, stale-signature mutation, valid equivocation, wrong request binding, wrong payload type, revoked-key exclusion, malformed threshold fail-closed behavior, and response-ID handling. The run used seed `1363226673` and passed 10 of 10 cases.

The strongest observed outcomes are fail-closed behaviors. A mutated payload with a stale signature is excluded. A valid incompatible response from the same identity creates `contested`. A wrong request ID or generic JSON payload type cannot contribute to threshold. A malformed threshold raises a typed request error rather than producing a decision.

Q1 remains a candidate-with-blockers because audit checkpoint integration, public-key fixtures, complete Rust schema/error parity, and operational key-management review are not yet complete.

## 7. Release gates

| Gate | Current state | Required next evidence |
|---|---|---|
| QG1 semantic agreement | Partial; Python local behavior and Rust baseline exist. | Full 17-case fixture/error mapping and rational scalar parity. |
| QG2 cryptographic binding | Fixture-only HMAC binding tested. | Ed25519 offline fixtures, policy lifecycle, and rotation/revocation cases. |
| QG3 audit integration | Durable audit primitives exist separately. | Persist decision, rejection, equivocation, checkpoint, and proof references. |
| QG4 adversarial confidence | Q0 5,750-case campaign and Q1 10-case oracle pass. | Expand Q1 campaign and add resource/error injection cases. |
| QG5 operational decision | Not passed. | Threat model approval, key custody, incident severity, retention, rollback, and owners. |

## 8. Release-candidate contents

The release candidate must include the source revision, environment record, fixture manifest, canonical vectors, focused test output, fuzz reports, Q1 audit report, claims and limitations register, threat model, test-oracle policy, SHA-256 checksums, and a release decision. A signature must never be fabricated; if signing is unavailable, the artifact must state that fact and remain unsigned.

## 9. Risks and falsification obligations

The highest risks are common-mode failure between evaluator paths, identity-policy mistakes, incomplete audit persistence, unsupported key lifecycle behavior, and accidental promotion of meaning-layer hypotheses into kernel assertions. The next falsification round must target unknown schema versions, verifier exceptions, partial persistence, conflicting equal-size audit roots, duplicated candidate identities, unsupported scalar policies, and resource exhaustion. Every case needs a predeclared oracle and a bounded runtime.

## 10. Next wave

The next coordinated wave should complete Rust parity, persist quorum records through the file store, transition offline fixtures to Ed25519, and integrate Merkle checkpoints with decision replay. Only after those artifacts pass should the program begin QG5 operational review. Networked quorum, key custody, production deployment, and claims of Byzantine consensus remain deferred.

## References

[1]: [Core Contract v0.1 specification](./SOV_CORE_CONTRACT_v0.1.md)  
[2]: [Next Gated Quorum Consensus Wave v0.2](./NEXT_GATED_QUORUM_CONSENSUS_WAVE_v0.2.md)  
[3]: [Q0 implementation and fuzz report](./Q0_IMPLEMENTATION_AND_FUZZ_REPORT.md)  
[4]: [Q1 release boundary](./Q1_RELEASE_BOUNDARY.md)  
[5]: [Q1 threat model](./Q1_THREAT_MODEL.md)  
[6]: [Q1 test oracle](./Q1_TEST_ORACLE.md)  
[7]: [Q1 claims and limitations](./Q1_CLAIMS_AND_LIMITATIONS.md)  
[8]: [DSSE protocol](https://github.com/secure-systems-lab/dsse/blob/master/protocol.md)  
[9]: [RFC 9162 Certificate Transparency v2](https://www.rfc-editor.org/rfc/rfc9162)
