# Full-Platform End-to-End Replay Evidence Record

**Recorded:** 2026-08-19  
**Hosted workflow:** [Full Platform End-to-End Replay, run 32232417722](https://github.com/LastFirst0/sovereign-engine-dashboard/actions/runs/32232417722)  
**Workflow source commit:** `df85f00a6d7d6ef011c47e7d1c29650c44f4ad25`  
**Pinned kernel-source snapshot:** `/manus-storage/sovereign_kernel_bounded_replay_1d94648_complete.tar_3765e4c8.gz`  
**Pinned snapshot SHA-256:** `60ad45520d360348aad70ddd0776b846d38db8d615e965efe54e4cbcd5c60d86`

## Purpose and Boundary

This is the final, **single GitHub-hosted runner** replay that joins the program’s declared bounded components: dashboard contracts/build, the pinned offline kernel release matrix and corpus/adapter checks, and real retired/active receipt-bundle continuity verification. It replaces the earlier composite-only evidence boundary for this gate.[1]

The runner used a job-generated dashboard signer for its self-contained contract tests. It did not receive a production private key, database credential, or storage credential. The real pre- and post-rotation bundle envelopes were retrieved from their retained managed-storage URLs and checked against fixed SHA-256 values before their signatures were verified using public JWK material only.[1]

> The replay confirms reproducibility of the named software, fixture, and archive-integrity boundaries. It does not verify a scientific theory, make a clinical or personal-genomic claim, grant verification authority to a legacy adapter, or treat source acceptance as publication.

## Single-Runner Result

| Component | Fresh-run result | Evidence boundary |
|---|---|---|
| Dashboard contract suite | **83 tests passed; 2 opt-in tests skipped** | Self-contained contracts use an ephemeral Ed25519 signer and declared non-production configuration. |
| Dashboard production build | **Passed** | Production bundle completed; the retained log reports only the existing chunk-size warning. |
| Kernel snapshot acquisition | **Passed** | Runner downloaded the non-secret source snapshot and SHA-256 matched `60ad45520d360348aad70ddd0776b846d38db8d615e965efe54e4cbcd5c60d86`. |
| Offline kernel matrix | **`OFFLINE_KERNEL_ECOSYSTEM_RELEASE_MATRIX=PASS`** | The declared Python/Rust bounded release matrix completed from the pinned snapshot. |
| Focused corpus/adapter tests | **45 passed** | Living Word structural validators, quarantined adapter tests, and tensor candidate accelerator tests completed. |
| Retired/active key continuity | **Passed** | Both actual retained envelopes matched fixed digests and their Ed25519 signatures verified solely from public material. |

## Archive Continuity Inputs

| Envelope | Retained key fingerprint | SHA-256 | Public-material signature result |
|---|---|---|---|
| Pre-rotation receipt `export_mszsbiq4_351317f7` | `4ae1ae137b5de0f541a48f589dbb87ca4034727d0b9e0f6dfb7857d265c1ffa0` | `5045edf260ea063ab9238f6f462f61d30cd3d4dfb52351ac5b743b16cacd91b0` | Valid |
| Post-rotation receipt `export_msztbfj2_76d42fcc` | `01ac7ea1649069cb68e70ddff4314a03e847612ecff8ddf8fce3795b05452d8e` | `74f204548503842094d763bb2153c5d8115a597dd568cc892a1787c06b6c3160` | Valid |

## Retained Artifact

The full GitHub Actions artifact was downloaded to:

```text
/home/ubuntu/full_platform_replay_32232417722/full-platform-end-to-end-replay-32232417722/
```

It retains the dashboard test/build logs, kernel snapshot and source hashes, offline release-matrix log, focused corpus/adapter log, the two bundle envelopes and their hash manifest, and the public-material verification report.

## Operational Interpretation

This end-to-end replay closes the requested reproducibility gate for the exact bounded components above. Future changes to the dashboard contract, kernel source snapshot, corpus fixture, signing policy, or retained-envelope format should require a new pinned-snapshot replay. An independently originated external adapter package remains a future admission opportunity; the completed local scorecard exercise remains a candidate test rather than runtime activation.

## Updated Material-Change Rerun

After adding the dashboard replay-access panel and separately packaged candidate-admission materials, the same single-runner workflow was rerun successfully as [run 32235300661](https://github.com/LastFirst0/sovereign-engine-dashboard/actions/runs/32235300661). That run completed **84 dashboard tests with 2 opt-in skips**, the same checksum-pinned kernel matrix, **45 focused corpus/adapter tests**, and both retained-envelope public-material checks. Its downloaded artifact is retained at `/home/ubuntu/full_platform_rerun_32235300661/full-platform-end-to-end-replay-32235300661/`.

## References

[1]: https://github.com/LastFirst0/sovereign-engine-dashboard/actions/runs/32232417722 "Full Platform End-to-End Replay run 32232417722"
