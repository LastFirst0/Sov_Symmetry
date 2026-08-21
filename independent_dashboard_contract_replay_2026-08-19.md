# Independent Dashboard Contract Replay Evidence Record

**Recorded:** 2026-08-19  
**Execution label:** `dashboard-contract-replay-2026-08-19-final`  
**Hosted workflow run:** [GitHub Actions run 32227982742](https://github.com/LastFirst0/sovereign-engine-dashboard/actions/runs/32227982742)  
**Repository and source:** `LastFirst0/sovereign-engine-dashboard`, `main` at `77c3c42732bc8753818bbc081f0e83f100f94ce1`

## Purpose and Scope

This record retains a clean GitHub-hosted replay of the dashboard’s deterministic contract suite and production build. The job intentionally used an **ephemeral Ed25519 signing key**, non-production owner/reviewer values, and a harmless fake storage-service base URL. It did not receive the production private key, live database credentials, or managed storage credentials.[1]

> The replay establishes that the named dashboard source completed its self-contained contract and build boundary in a clean hosted environment. It does **not** verify live database state, produce a production receipt, or cryptographically replay a real retired signing key.

## Retained Result

| Item | Observed result | Boundary |
|---|---|---|
| Hosted workflow | `success` | GitHub-hosted Ubuntu runner; no project production secret was used. |
| Contract suite | **37 test files passed; 2 opt-in test files skipped; 82 tests passed; 2 skipped** | The skipped tests require explicitly opt-in live resources and were not silently treated as passing. |
| Production build | **Passed** | Vite and server bundle completed; the retained log contains a bundle-size warning, not a build failure. |
| Signing-key tests | Passed with a job-generated ephemeral Ed25519 key | Validates public descriptor and signature contract behavior; it is not historical production-key continuity evidence. |
| Storage failure tests | Passed using the declared mock failure paths under an explicit harmless configuration | Does not upload or retain any object. |

## Source Identity

| File | SHA-256 |
|---|---|
| `client/src/signingKeyHistoryContract.test.ts` | `b6a98cb9513d0d9bf5c60e4daabac897fe367ff584211ac028041024c8b3a9aa` |
| `client/src/receiptSigningSecret.test.ts` | `df1d7c137184b1a7c031853456d3fa586f8e026177175beb379ae3c3b491598d` |
| `server/receiptBundles.ts` | `7b22bf8d56b922a4c128b5f72813a0f4eb8e9cd4786c2cb6110564c488962d90` |
| `server/routers.ts` | `74e1c0001303c441b6f3be0ddaa62971f8371214e6196e377ccc965fab0b9468` |

## Relationship to the Kernel Replay

The dashboard replay is retained separately from the successful bounded kernel-and-corpus replay at [run 32226422399](https://github.com/LastFirst0/Sovereign_Engine/actions/runs/32226422399). The two clean hosted runs independently reproduce their own repository boundaries. They should not be described as a single all-components replay because GitHub’s default workflow token for the private dashboard repository cannot read the separate private kernel repository.[1] [2]

The remaining full-platform requirement is narrower and more demanding: a future replay needs an actual retained pre-rotation signed-bundle envelope plus its retained public-key record. The system retains key metadata and signature-event metadata but did not retain a complete old bundle envelope in the workspace, so that historical signature cannot be reconstructed without violating the retired-private-key boundary.

## Retained Local Copy

The downloaded hosted artifact is retained in the task workspace at:

```text
/home/ubuntu/dashboard_replay_32227982742/dashboard-contract-replay-32227982742/
```

It contains the requested source reference, checked-out commit, source-hash manifest, contract-test log, and build log.

## References

[1]: https://github.com/LastFirst0/sovereign-engine-dashboard/actions/runs/32227982742 "Dashboard Contract Replay run 32227982742"
[2]: https://github.com/LastFirst0/Sovereign_Engine/actions/runs/32226422399 "Independent Evidence Replay run 32226422399"
