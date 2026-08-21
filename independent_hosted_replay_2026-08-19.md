# Independent Hosted Replay Evidence Record

**Recorded:** 2026-08-19  
**Execution label:** `hosted-independent-replay-final-2026-08-19`  
**Hosted workflow run:** [GitHub Actions run 32226422399](https://github.com/LastFirst0/Sovereign_Engine/actions/runs/32226422399)  
**Workflow definition branch:** `v2.0-clean-release`  
**Replayed bounded evidence source:** `evidence/independent-replay-complete-20260819`  
**Checked-out source commit:** `1d94648c89d5d0e6743e4136911923dcc5f691cf`

## Purpose and Boundary

This record retains the outcome of a clean GitHub-hosted replay of the declared bounded kernel and corpus scope. It is **reproducibility evidence for software contracts and supplied fixtures**, not evidence that a scientific, historical, theological, clinical, or other interpretive claim is true. The workflow used a fresh hosted environment, an explicit source reference, a bundled project-document snapshot, and the public code and corpus files named below.[1]

The replay was deliberately fail-closed. Its first two attempts exposed missing dependencies in the declared round-trip test path: first `scipy` through an unrelated root test configuration, then `scipy` through an explicitly selected protocol test. The workflow was narrowed with `--confcutdir=tests` and its declared dependency closure was amended to install SciPy before the final run. These changes prevent an implicit developer-machine dependency from being treated as evidence of a reproducible success.[1]

## Retained Replay Identity

| Item | Retained value | Interpretation |
|---|---|---|
| Workflow result | `success` | All declared hosted replay steps completed. |
| Runtime environment | GitHub-hosted `ubuntu-latest`, Python 3.12, stable Rust toolchain | A distinct clean hosted environment executed the bounded release path. |
| Offline release matrix | `65 passed` in Python; `4 passed` in Rust; `OFFLINE_KERNEL_ECOSYSTEM_RELEASE_MATRIX=PASS` | The declared Python/Rust bounded matrix completed successfully. |
| Focused source and adapter tests | `45 passed` | The supplied Living Word validation, negative validator, quarantined adapter, and tensor candidate tests completed. |
| Artifact retention | `independent-evidence-replay-32226422399` | Commit, source hashes, matrix log, and focused-test log were uploaded by the workflow and downloaded for this record. |

## Source-Identity Hashes

| File | SHA-256 |
|---|---|
| `data/living_word/Genesis_OSHB.json` | `ddadbb315bb13fcca64ebfabaeb3006fc5294cda50676db1d570c7f6cd8de7ef` |
| `data/living_word/John_SBLGNT.json` | `ad93149058a0570a9c3917c62c53159619daf04cfa172036efdc52df457372ea` |
| `sov_evidence_geometry_core/universal.py` | `4b84125b2dc45c8aa2c5ceb645ddc38b2d89393c9f56a4ead391692dcd142226` |
| `sov_evidence_geometry_core/legacy_runtime_adapter.py` | `b17aed29083f5fb838cc6cde6d06ad9b61c1efc5c3f8d5f6b8ea53f80b9bcc6c` |
| `sov_evidence_geometry_core/tensor_accelerator.py` | `9f658a3c2926b47a502d109e33f6deb105f11febe16fe9aaf31d4db3c6c1ae2e` |

## Evidence Interpretation

> The replay establishes that the exact named commit, fixture files, and bounded commands completed in a clean hosted environment under the recorded workflow. It does not establish that a legacy runtime output is authoritative, that an optional accelerator can issue receipts, or that source acceptance is publication or verification.

The quarantined legacy adapters remain candidate generators. The optional tensor accelerator remains candidate-only; deterministic CPU confirmation retains receipt authority. The supplied Living Word files were checked for declared structure and URI-format conditions only. No semantic or interpretive conclusion is implied.

## Retained Local Copy

The downloaded GitHub Actions artifact is retained in the task workspace at:

```text
/home/ubuntu/independent_replay_32226422399/independent-evidence-replay-32226422399/
```

It contains `commit.txt`, `source_hashes.sha256`, `offline_release_matrix.log`, `corpus_and_adapter.log`, `replay_label.txt`, and `requested_source_ref.txt`.

## References

[1]: https://github.com/LastFirst0/Sovereign_Engine/actions/runs/32226422399 "Independent Evidence Replay run 32226422399"
