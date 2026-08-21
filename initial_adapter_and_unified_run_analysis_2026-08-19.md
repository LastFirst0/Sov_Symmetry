# Initial External-Adapter and Unified-Replay Analysis

**Recorded:** 2026-08-19  
**Latest unified replay:** [GitHub Actions run 32235300661](https://github.com/LastFirst0/sovereign-engine-dashboard/actions/runs/32235300661)  
**Candidate package:** [Sovereign Adapter Candidate — Nondecreasing](https://github.com/LastFirst0/Sovereign-Adapter-Candidate-Nondecreasing)  
**Candidate self-check:** [GitHub Actions run 32235113567](https://github.com/LastFirst0/Sovereign-Adapter-Candidate-Nondecreasing/actions/runs/32235113567)

## Executive Finding

The first separately packaged adapter candidate has completed its deterministic reference and fixture checks but remains **quarantined** by design. Seven of eight admission gates passed; the review gate blocked because there are no independent semantics and implementation reviewers. This is the correct security outcome. The candidate must not be activated, described as third-party-originated, or used as verification authority.[1]

The updated single-runner full-platform replay also passed after the replay-access panel and candidate package were added. It confirms the named dashboard source, checksum-pinned kernel snapshot, focused corpus/adapter tests, and retired/active key-continuity verification in one fresh GitHub environment.[2]

## 1. Separately Packaged Candidate

The candidate is a deliberately narrow predicate: it tests whether a declared list of one to eight exact integers is nondecreasing. It returns only `verified`, `fail`, or `unverifiable`, plus a deterministic receipt ID. It does not model a theory, experimental mechanism, personal data, clinical outcome, or real-world ordering.

| Identity item | Recorded value |
|---|---|
| Candidate ID | `external.candidate.nondecreasing-sequence@0.1.0` |
| Source baseline | `e214f10f23bbb155b6e6d63edcc85c7d62d7e3ec` |
| First admission record | `d4b73ae5e6bc7f8d6f0b6f6c6c054a900fead5a0` |
| First release tag | `external-candidate-v0.1.0-first-run` |
| Frozen fixture SHA-256 | `f5eb0d7e49daec7d1e92332b344fb816f61b9afcfd20c371b2595b57a340d75a` |
| Candidate self-check | 3 deterministic tests passed locally; hosted self-check run 32235113567 passed. |

### Admission-Gate Result

| Gate | Result | Evidence-bounded interpretation |
|---:|---|---|
| 0 — Intent | Pass | Scope and non-claims are explicit. |
| 1 — Semantics | Pass | Schema, assumptions, dimensions, tolerance policy, and predicate are declared. |
| 2 — Evidence | Pass | Frozen fixtures cover positive, negative, malformed, boundary, mutation, and neutrality cases. |
| 3 — Reference | Pass | Six non-neutrality fixtures matched their declared results. |
| 4 — Neutrality | Pass | Three provenance labels returned the same `verified` state and receipt ID. |
| 5 — Assurance | Pass | Local deterministic receipt IDs were inspectable; no unavailable layer was treated as present. |
| 6 — Review | **Block** | No independent scoped semantics or implementation review exists. |
| 7 — Release | Pass | Version, source baseline, rollback reference, and narrow public statement are recorded. |

> **Decision: quarantine.** The block is not a malfunction. It preserves the admission rule that two genuine independent scoped reviews are required before any candidate could be considered for a later activation decision.

### Negative Result Retained

The initial candidate self-check, [run 32235037809](https://github.com/LastFirst0/Sovereign-Adapter-Candidate-Nondecreasing/actions/runs/32235037809), failed because the clean runner lacked an explicit `pytest` installation. The failure was retained rather than hidden. A minimal dependency declaration was added; the corrected self-check then passed as run `32235113567`. This demonstrates dependency closure for the candidate’s own deterministic tests, not core-kernel admission.[1]

## 2. Updated Unified Replay

The latest single-runner replay is labeled `full-platform-rerun-after-replay-panel-and-adapter-candidate-2026-08-19`. It executed the published dashboard commit `30a259f208087edb6bfb613773401e39d86f717d` and retained its GitHub artifact at:

```text
/home/ubuntu/full_platform_rerun_32235300661/full-platform-end-to-end-replay-32235300661/
```

| Component | Result |
|---|---|
| Dashboard contracts | **84 passed; 2 opt-in skipped** |
| Dashboard build | **Passed**; existing bundle-size warning remains non-fatal. |
| Kernel snapshot | SHA-256 matched `60ad45520d360348aad70ddd0776b846d38db8d615e965efe54e4cbcd5c60d86`. |
| Offline kernel matrix | **`OFFLINE_KERNEL_ECOSYSTEM_RELEASE_MATRIX=PASS`** |
| Focused corpus/adapter suite | **45 passed** |
| Pre-rotation envelope | Expected digest matched; signature valid with retained public material. |
| Post-rotation envelope | Expected digest matched; signature valid with retained public material. |

## 3. What the Initial Run Establishes—and Does Not Establish

The evidence establishes that the named dashboard revision, declared kernel snapshot, bounded fixtures, and two retained signed envelopes could be executed or verified in a fresh hosted environment. It also establishes that the candidate’s reference evaluator has deterministic behavior for its declared fixtures and that review-gate quarantine operates as intended.

It does **not** establish that the candidate is a third-party package, independently reviewed, admitted to dispatch, scientifically valid, empirically explanatory, or suitable for use beyond its finite structural predicate. It does not convert a receipt signature into a claim about the truth of any theory or interpretation.

## 4. Initial-Run Controls and Next Review Conditions

| Control | Current state | Condition before advancement |
|---|---|---|
| Candidate source identity | Separate private repository, immutable commits and tag | Preserve release tag and package/report hashes. |
| Fixture integrity | Frozen SHA-256 with local and hosted self-check | Any fixture change requires a version bump, new hash, and full admission rerun. |
| Independence | **Not met** | Obtain two reviewers with distinct identities and scoped semantics/implementation rationales. |
| Runtime activation | **Not permitted** | Require independent reviews, a fresh eight-gate report, and a separate explicit dispatch decision. |
| Platform replay | Current rerun passed | Repeat after material dashboard, kernel-snapshot, fixture, signing-policy, or retained-envelope changes. |

## References

[1]: https://github.com/LastFirst0/Sovereign-Adapter-Candidate-Nondecreasing "Separately packaged candidate adapter repository"
[2]: https://github.com/LastFirst0/sovereign-engine-dashboard/actions/runs/32235300661 "Updated Full Platform End-to-End Replay run 32235300661"
