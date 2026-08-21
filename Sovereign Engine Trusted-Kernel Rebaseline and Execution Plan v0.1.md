# Sovereign Engine Trusted-Kernel Rebaseline and Execution Plan v0.1

**Status:** Decision-ready plan.  
**Scope:** The isolated deterministic evidence–geometry core and its Q1 offline verification-harness promotion path.  
**Out of scope:** The legacy experimental repository surface, GU physical claims, agent runtime, UI, P2P/network consensus, LLMs, and product demonstrations except where they exercise published core fixtures.

## Executive answer

**Yes, kernel work is still the central program.** The active trusted kernel is the isolated `sov_evidence_geometry_core` Python reference package plus the intentionally narrow `sov-contract-parity` Rust harness—not the broader legacy repository. The dashboard, meaning layer, and Invariant Lab are support surfaces that make the kernel inspectable and understandable; they do not count as kernel completion.

The evidence-weighted completion score is **41%** for the **offline trusted-kernel program**, and **39%** for the **promotion-ready kernel release boundary**. These are planning indicators, not a claim of production readiness. They use explicit weights and evidence states below, rather than raw file count, test count, or broad-repository claims. The Q1 release is correctly classified as **candidate-with-blockers**.[1]

> **Release conclusion:** Q1 can be reviewed and replayed within the offline fixture boundary. It is not a production consensus service, cryptographic key-custody system, or proof of any physical Geometric Unity claim.[1]

## What is complete, partial, and blocked

| Capability category | Weight | Evidence-backed state | Credit | Weighted contribution | Basis |
|---|---:|---|---:|---:|---|
| Deterministic Core Contract, JCS IDs, typed statuses | 20% | Implemented in Python reference; normative contract still records ADR acceptance prerequisites | 70% | 14.0 | Core Contract §§2–5, 9–12.[2] |
| Cross-language conformance | 20% | Rust covers canonicalization/content IDs and a small invariant subset only | 25% | 5.0 | Rust harness scope; 17-case full pack remains required.[2] |
| Geometry/invariant evaluation | 15% | Tensor symmetry and metric-inverse checks are exercised; broader K0–K3 fixtures are incomplete | 50% | 7.5 | Core Contract conformance and program Gate 2.[2] [3] |
| Local evidence, quorum, and offline audit | 15% | File store, DSSE HMAC fixtures, Merkle primitives, Q0 and Q1 oracle/campaign evidence exist | 75% | 11.25 | Q1 boundary and oracle policy.[4] [5] |
| Public-key cryptographic profile | 10% | HMAC fixture binding only; Ed25519 lifecycle, rotation, and revocation absent | 10% | 1.0 | Q1 release blockers.[1] |
| Durable quorum decision records and checkpoint replay | 10% | Local store/audit primitives exist; quorum/rejection/equivocation persistence and automatic checkpoint integration remain blocked | 10% | 1.0 | Q1 release blockers.[1] |
| Operational release security and formal bridge | 10% | Threat/test-oracle/claims documents exist; QG5 operational review and a meaningful formal bridge do not | 10% | 1.0 | Q1 boundary and Core Contract limits.[1] [2] |
| **Total offline-kernel completion** | **100%** | **Foundation in place; promotion gates incomplete** |  | **40.75% → 41%** | Weighted model |

For a **promotion-ready** score, the cryptographic and durable-store categories receive zero credit until their required evidence exists, producing **38.75% → 39%**. This prevents local HMAC fixtures or standalone Merkle primitives from being counted as operational security completion.

## Completion measurement policy

Completion is gated by the published contract rather than feature breadth. A category earns credit only when its required artifacts are versioned, replayable, and independently testable.

| Evidence class | Counts toward completion | Does not count as |
|---|---|---|
| Tested contract | Fixed-seed tests, fixture manifest, output/ID checks, tamper case | General security proof or physical truth |
| Cross-language parity | Shared published bytes, results, errors, and named release/toolchain versions | Parity for unimplemented predicates |
| Cryptographic profile | Public-key vectors, negative cases, key-policy tests, lifecycle documentation | Key custody or live-network security without operations evidence |
| Durable audit | Restart/replay, rejection/equivocation persistence, inclusion/consistency verification | Availability, replication, or BFT |
| Formal anchor | Theorem source, assumptions, Lean statement, bridge-to-code evidence | Proof of an entire runtime or GU physical claim |

## Narrow release boundary

The next promotable unit is **`sov-core-offline-rc`**: a clean-installable offline verifier that consumes a signed fixture manifest and deterministically emits canonical decision records. It must contain no network discovery, remote key acquisition, database dependency, runtime plugins, LLM calls, mutable callbacks, or physical-theory interpretation. This matches the contract’s deterministic boundary.[2]

## Multi-wave execution portfolio

### Wave K1 — Contract and conformance freeze

**Objective:** Make the core’s legal input/output surface complete enough that Python and Rust can be judged against the same immutable suite.

| Work package | Can run with | Deliverable | Exit gate |
|---|---|---|---|
| K1-A: ADR and release-profile acceptance | K1-B, K1-C | Accepted ADR list; exact `sov-core-offline-rc` profile | Contract status no longer depends on unaccepted ADRs |
| K1-B: 17-case canonical fixture pack | K1-A, K1-C | Versioned fixture JSON, expected canonical bytes/IDs/status/errors, SHA-256 manifest | Python reproduces all 17 and tamper manifest fails closed |
| K1-C: Registry/error map | K1-A, K1-B | Code-owned operation/predicate/error inventory including rational scalar support | Unknown ID/scalar produces typed error or `unverifiable`, never success |
| K1-D: Clean CI baseline | K1-A–C | Separate Python/Rust/fixture-manifest jobs with toolchain and checksum artifacts | Fresh checkout passes required jobs |

**Non-goals:** New tensor operations, UI, P2P, signing implementation, or GU-model semantics.

### Wave K2 — Cross-language parity and offline public-key profile

**Objective:** Eliminate the two largest deterministic gaps: full fixture parity and non-HMAC cryptographic binding.

| Work package | Dependency | Deliverable | Exit gate |
|---|---|---|---|
| K2-A: Rust full conformance adapter | K1 fixture manifest | Schema/semantic reason mapping, rationals, all 17 cases, canonical-byte parity report | Python/Rust parity passes in a clean CI job |
| K2-B: Ed25519 DSSE fixture profile | K1 registry/error map | Offline key fixture set, verification adapter, invalid/revoked/unknown key cases, policy document | Signature, PAE/payload, key-ID, and policy mutations reject with preserved evidence |
| K2-C: Differential/property fuzzing | K2-A, K2-B | Fixed seeds, corpus minimization, cross-language digest comparison | No unexplained outcome across named campaign; report is bounded |

### Wave K3 — Durable decisions and append-only audit integration

**Objective:** Turn local decision outcomes into restart-safe, replayable audit evidence.

| Work package | Dependency | Deliverable | Exit gate |
|---|---|---|---|
| K3-A: Durable quorum-decision schema | K1 registry | Decision/rejection/equivocation object schemas and file-store atomics | Restart preserves accepted and rejected responses with IDs unchanged |
| K3-B: Merkle checkpoint binding | K3-A | Decision-to-log inclusion, consistency artifacts, checkpoint manifest | Inclusion and consistency verification succeed after restart; mutation fails |
| K3-C: Audit replay campaign | K3-A/B | Crash/restart/tamper corpus and machine-readable report | No accepted decision silently disappears or changes terminal state |

### Wave K4 — Operational review and release candidate

**Objective:** Convert the offline harness into a release-candidate package without falsely claiming consensus.

| Work package | Dependency | Deliverable | Exit gate |
|---|---|---|---|
| K4-A: Key management and incident policy | K2-B | Lifecycle, rotation, revocation, test key handling, incident runbook | QG5 review explicitly accepts all residual risks |
| K4-B: Performance and resource limits | K1–K3 | Target-hardware benchmark harness/raw results, bound settings | Latency/RSS/limit behavior published; no extrapolated capacity claim |
| K4-C: Release evidence bundle | K2–K4-B | Signed source/tag identity, clean install output, checksums, fixture and claim manifests | `candidate-with-blockers` becomes `offline-rc` only when every required artifact verifies |

### Wave K5 — Formal anchors and bounded geometry increments

**Objective:** Expand the mathematical core only after the verifier is stable.

| Work package | Dependency | Deliverable | Exit gate |
|---|---|---|---|
| K5-A: Formal bridge inventory | K1 | Map predicate → theorem/assumptions → Lean statement → code bridge status | Every `formal_anchor` status is justified or downgraded |
| K5-B: Geometry fixture increments K0–K3 | K1 and formal inventory | Flat, non-flat, torsion/gauge, and invalid-index fixture records | Residuals and failure cases replay under contract rules |
| K5-C: Meaning/source-span coverage | K5-B | Equation-to-fixture-to-concept graph | No GU hypothesis is silently promoted through UI wording |

## First coordinated implementation batch: K1 + K2 preparation

Work begins as a **batch**, but feature code must still land behind these shared contracts. The immediate parallel streams are:

1. **Fixture stream:** publish the 17-case pack, canonical byte outputs, tamper variants, and manifest verifier.
2. **Rust stream:** map the current narrow Rust harness to the full fixture schema and error taxonomy; add rationals after fixture bytes freeze.
3. **Crypto stream:** write the offline Ed25519 fixture/key-policy profile and negative-case matrix; do not connect network key discovery.
4. **Persistence stream:** finalize the decision/rejection/equivocation schema and atomic file-store interface, but defer Merkle binding until IDs are stable.
5. **Release stream:** split CI into Python, Rust, fixture-manifest, cross-language, and release-evidence jobs; every missing artifact is a hard failure or explicit `unverifiable`.

These streams share a weekly integration gate: identical fixture-manifest hash, no dynamic operation registry, no missing reason code, and no affirmative result from an exception path.

## Critical risks and controls

| Risk | Trigger | Preventive control | Fallback | Owner role |
|---|---|---|---|---|
| Legacy code pollutes green core | New import reaches broad runtime or P2P module | Import allowlist and clean-install test | Quarantine module and block merge | Kernel owner |
| Parity drift | Canonical bytes/errors disagree | Golden manifest and byte-level diff artifact | Mark parity advisory; block promotion | Rust parity owner |
| Key fixture mistaken for custody | Docs/status omit “offline fixture” | Mandatory boundary label in profile and UI | Remove promotion claim | Crypto/release owner |
| Audit evidence silently changes | Restart/tamper replay mismatch | Immutable content IDs + atomic write/replay corpus | Fence release and rebuild store | Evidence owner |
| GU interpretation overclaim | Hypothesis appears as verdict | Claim-class validation and source-span review | Downgrade language to hypothesis | Formal/scientific reviewer |

## Immediate decision requests

1. Accept the narrow **offline verifier** release boundary and keep all network/BFT/key-custody claims out of K1–K4.
2. Freeze the 17-case fixture manifest as the shared contract before extending Rust or signature adapters.
3. Assign one accountable owner to each of: kernel/fixtures, Rust parity, cryptographic profile, durable audit, release/CI, and formal review.

## References

[1] `q1_release_candidate/RELEASE_CANDIDATE.md` (lines 1–7), local project evidence workspace.  
[2] `SOV_CORE_CONTRACT_v0.1.md` (especially §§2–5, 9–13), local project evidence workspace.  
[3] `PROGRAM_CONTROL_CENTER.md` (lines 92–105), local project evidence workspace.  
[4] `Q1_RELEASE_BOUNDARY.md` (lines 1–27), local project evidence workspace.  
[5] `Q1_TEST_ORACLE.md` (lines 1–26), local project evidence workspace.
