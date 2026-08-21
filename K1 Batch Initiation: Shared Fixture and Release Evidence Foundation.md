# K1 Batch Initiation: Shared Fixture and Release Evidence Foundation

**Status:** Started; shared inputs frozen as a candidate, not yet a promotion artifact.  
**Boundary:** `sov-core-offline-rc` only.

## Entry evidence

The repository currently contains a 17-case v0.1 fixture pack with the Core Contract’s intended distribution: 8 valid objects, 4 invalid requests, 2 `unverifiable` outcomes, 1 failed predicate, 1 tamper case, and 1 determinism case. Its SHA-256 is recorded in `K1_FIXTURE_MANIFEST_CANDIDATE.json`. The existing Rust crate passes its own 2 tests but remains intentionally narrow; that is a baseline, not full conformance.

## Active streams

| Stream | Starting artifact | First concrete output | Blocking dependency | Exit evidence |
|---|---|---|---|---|
| Fixture and registry | Candidate manifest | Manifest verifier plus expected byte/status/error table | ADR acceptance | Python validates the manifest and all 17 cases |
| Rust parity | Current 2-test crate | Fixture-loader design and coverage map | Frozen fixture manifest | Rust executes every case or reports a known gap; unknown paths cannot pass |
| Offline public-key profile | Q1 HMAC fixture boundary | Ed25519 profile and negative-case matrix | Key-policy version | Invalid payload/key/policy cases preserve rejection evidence |
| Durable audit | File store and Q0/Q1 decision shape | Decision/rejection/equivocation record schema | Canonical decision-ID contract | Restart/tamper replay preserves all terminal evidence |
| Release evidence | Existing Q1 report process | CI job specification and clean-install checklist | All above artifacts | Required jobs emit checksums, toolchains, fixture hash, and status |

## Integration rhythm

No stream may independently change a fixture’s semantics. A change requires a version increment, fixture manifest update, Python reference result, Rust parity result, and a recorded limitation if one adapter is not yet capable. The weekly integration gate rejects missing reason codes, dynamic predicate names, unknown scalar coercions, or a passing outcome caused by an exception.

## Next implementation checkpoint

1. Add the manifest verifier to the isolated Python package and test that an edited fixture is rejected.
2. Add a Rust fixture-loader skeleton that distinguishes unsupported cases from passing cases.
3. Publish the Ed25519 fixture profile as an offline policy specification before adopting a crypto library.
4. Add durable record-schema tests for a decision plus rejected and equivocation responses.

These four outputs are deliberately coordinated: they can proceed in parallel only while all consume the candidate manifest and immutable Core Contract vocabulary.
