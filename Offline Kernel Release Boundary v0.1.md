# Offline Kernel Release Boundary v0.1

## Release statement

This release is a **small, deterministic, offline verification kernel**. It accepts a declared finite matrix input for three checks—symmetry, identity, and declared inverse product—and emits readable replayable receipts. It can attach optional local audit artifacts and verify deterministic offline Ed25519 DSSE fixtures.

## Required acceptance gates

| Gate | Pass condition |
|---|---|
| Public checks | Symmetry, identity, and inverse checks produce `verified`, `fail`, or `unverifiable` with plain-language explanation and scope. |
| Replay | A receipt bundle recomputes to the same receipt ID; modified provenance yields a typed non-passing result. |
| Local audit | A persisted local audit attachment verifies inclusion against its local checkpoint; altered evidence fails. |
| Fixture signature | A fixed Ed25519 DSSE vector validates only against an active policy-listed key; policy or payload mutation fails. |
| Deterministic contract | The frozen 17-case pack validates through the reference and Rust parity paths. |
| Isolation | Release tests run without legacy runtime imports. |
| Documentation | A user guide, FAQ, assurance specification, CLI help, and release boundary are delivered together. |

## Explicitly outside this release

This release does not operate production key custody, remote discovery, rotation, hardware-backed protection, a distributed consensus service, a replicated public transparency log, public log monitoring, broad symbolic algebra, formal theorem proving, or physical-theory validation. Those are follow-on operational or research programs, not incomplete hidden features.
