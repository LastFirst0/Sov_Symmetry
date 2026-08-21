# Sovereign Engine Offline Kernel v0.1: Release Guide

## Release status

**Complete for the declared offline boundary.** This release is a small, deterministic kernel that runs three useful matrix checks, produces readable replayable receipts, optionally attaches local audit evidence, and validates deterministic offline Ed25519 DSSE fixtures. The release matrix and bundled manifest make the boundary reproducible.

> The release is complete as an **offline kernel foundation**. It is not a claim that production key operations, distributed consensus, public transparency, broad geometry automation, or physical-theory validation have been completed.

## What a user can do now

| Task | Command | Result |
|---|---|---|
| Check symmetry | `PYTHONPATH=. python tools/sov_kernel.py check symmetric --input '[[1,2],[2,4]]'` | A readable receipt for whether `Aᵀ = A`. |
| Check identity | `PYTHONPATH=. python tools/sov_kernel.py check identity --input '[[1,0],[0,1]]'` | A receipt for whether a matrix is identity. |
| Check an inverse candidate | `PYTHONPATH=. python tools/sov_kernel.py check inverse --input '{"left":[[2,0],[0,3]],"right":[[0.5,0],[0,0.3333333333333333]]}'` | A receipt showing the declared product and any mismatch. |
| Add local audit evidence | Add `--audit-store /path/to/local-store` | An optional attachment with persisted artifacts, a local checkpoint, and inclusion proof. |
| Replay a result | `PYTHONPATH=. python tools/sov_kernel.py replay --bundle receipt-output.json` | `verified`, `fail`, or `unverifiable` replay result. |
| Run all release gates | `./tools/run_offline_kernel_release.sh` | The isolated release matrix. |
| Rebuild evidence bundle | `PYTHONPATH=. python tools/build_offline_kernel_release_bundle.py` | `dist/offline-kernel-v0.1/` with manifest and documentation. |

## What the receipts mean

A receipt reports one of three terminal states. **Holds in this check** means the named rule held for the declared input. **Does not hold in this check** means the input was sufficient and a mismatch is shown. **Cannot be checked from this input** means a required input, supported representation, or assumption was missing; it is not a disguised failure.

The receipt includes the question, explanation, mismatch or missing-input detail, scope, next action, stable ID, and replay provenance. These fields help a person understand the result before they need any audit vocabulary.

## Optional advanced assurance

The normal receipt is enough for ordinary use. The advanced export can carry only explicitly recorded evidence: a local persisted receipt bundle, audit event, local Merkle checkpoint and inclusion proof, or fixture signature status. An absent signature, quorum, or Merkle field is always **not recorded**, not “trusted by default.”

The Ed25519 verifier validates deterministic fixture vectors only. It recognizes an active versus revoked policy-listed key and rejects unknown keys, algorithm changes, malformed encoding, and altered payloads. It does not provide remote key discovery or operational key custody.

## Release verification summary

The release runner executes the focused Python suite for public checks, provenance replay, audit attachment, Ed25519 fixtures, frozen manifest, durable records, audit/persistence, and quorum behavior. It also executes the Rust contract-parity suite and performs a CLI check-and-replay smoke test. The release bundle copies the code, selected tests, shared fixture pack, documentation, and a SHA-256 manifest into `dist/offline-kernel-v0.1/`.

## Follow-on work, deliberately separate

| Follow-on program | Why it is not part of this release |
|---|---|
| Production key management | Requires actual key lifecycle, authorization, rotation, revocation distribution, and operational monitoring. |
| Replicated/public transparency | Requires multi-writer protocol, availability, monitoring, and independent log observation. |
| Distributed quorum service | Requires network transport, node identity governance, failure handling, and operational consensus policy. |
| More mathematical checks | Should be added one at a time through the same named predicate, fixture, receipt, and scope pattern. |
| Formal proof bridges / research claims | Require a separate formalization and scientific-evidence program. |

## References

[1] `OFFLINE_KERNEL_RELEASE_BOUNDARY_v0.1.md`, release acceptance boundary.  
[2] `PLAIN_LANGUAGE_KERNEL_GUIDE.md`, public model and examples.  
[3] `ADVANCED_ASSURANCE_EXPOSURE_SPEC_v0.1.md`, advanced exposure contract.  
[4] `tools/run_offline_kernel_release.sh`, executable release matrix.  
[5] `dist/offline-kernel-v0.1/RELEASE_MANIFEST.json`, reproducible evidence inventory.
