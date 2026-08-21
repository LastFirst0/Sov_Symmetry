# K1 Chained Execution Report

**Boundary:** `sov-core-offline-rc` foundation only.  
**Status:** **partial pass; promotion blocked by design.**

## What this chained batch completed

| Chain link | Artifact or check | Observed result | Gate state |
|---|---|---|---|
| Shared fixture freeze | `K1_FIXTURE_MANIFEST_CANDIDATE.json` | SHA-256 `e3b36640661588c54320878aa7b7bd7f1c347701296179d4b4b08e0a4f0d1e02`; 17 fixtures with required 8/4/2/1/1/1 distribution | Passed as candidate, not attested |
| Python fail-closed manifest verification | `fixture_manifest.py` + 2 targeted tests | Correct digest/counts accepted; edited digest raises `E_AUDIT_TAMPER` | Passed |
| Rust shared-fixture ingestion | `verify_k1_fixture_manifest` + Rust test | Correct pack returns 17; altered digest produces `E_AUDIT_TAMPER`; crate suite is 3/3 | Passed for manifest boundary only |
| Offline public-key policy | `K1_OFFLINE_ED25519_PROFILE.md` | Algorithm, PAE, key-policy, and negative-case contract documented | Spec only; implementation blocked pending vectors |
| Durable decision contract | `sov.quorum.durable_record.v0_1.schema.json` | 3 representative kinds validate; unexpected property rejects | Schema-level pass; persistence wiring remains pending |

## Test evidence

```text
Python isolated core surface: 14 passed
Rust parity surface:           3 passed
Durable schema examples:       3 accepted; extra-field rejection observed
```

The first Python attempt exposed an unrelated broad-repository `conftest.py` import requiring `scipy`; K1 tests were then run with `--confcutdir=tests/core_contract`. This is a credibility signal: the isolated kernel is testable, but the repository-wide test surface remains contaminated by legacy imports and must not be used as the K1 release gate.

## What this does not establish

The Rust adapter does **not** yet execute the semantic rules of all 17 fixtures; it verifies the shared fixture artifact and fails closed on manifest tampering. Ed25519 is **not** yet executable; the profile is an offline policy draft. Durable decision records are **not** yet written through `FileObjectStore`, and Merkle checkpoint integration is not yet implemented. Therefore, K1 does not change the Q1 classification from `candidate-with-blockers`.

## Next chained gate

1. Implement the full Rust adapter mapping for schema/error/rational cases against the frozen pack.
2. Add deterministic Ed25519 test vectors and a verifier adapter with rejection-evidence tests.
3. Persist decision, rejection, and equivocation records atomically; then bind them to the audit log and restart/tamper replay corpus.
4. Create clean CI jobs that emit toolchain version, fixture-manifest hash, test output, and artifact checksums.

No key discovery, networking, consensus, GUI feature, or GU physical interpretation is permitted to enter this gate.
