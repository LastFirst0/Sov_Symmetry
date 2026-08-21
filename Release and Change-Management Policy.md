# Release and Change-Management Policy

## Versioning

Core schemas, operation registries, predicate semantics, and API versions use semantic versioning. A canonicalization or evidence-record change is breaking unless a legacy reader/verifier and migration record are provided. Experimental GU modules must be separately versioned and cannot imply core stability.

## Compatibility

| Change | Required action |
|---|---|
| New optional field | Backward-compatible schema update plus fixture |
| New operation/predicate | Registry version increment, test vectors, status/error contract |
| Changed canonical bytes/hash | Major-version migration, dual reader, rehash policy, ADR and human gate |
| Removed/deprecated API | Published deprecation period, migration guide, generated-client tests |
| New external connector scope | Connector matrix update, data/security review, human confirmation if effects/secrets expand |
| Claim promotion | Source/evidence review, falsification update, independent review, human gate for external publication |

## CI stages

1. **Static:** pinned toolchain, formatting, type/lint, lockfile/dependency policy.
2. **Core:** pure unit/property/golden/invalid/tamper fixtures.
3. **Reference:** optional Python/Lean differential/formal anchor checks, artifacted separately.
4. **Contract:** OpenAPI validation, generated-client and provider/consumer compatibility.
5. **Integration:** bounded runtime-plan to evidence trace.
6. **Advisory experimental:** broad workbench, model, P2P, and demo checks; never used to establish green-core correctness.
7. **Release:** clean install, evidence bundle, SBOM/dependency report, limitation register, checksums; signing audit-only after reproducibility.

## Incident and rollback

An incident is opened for false `verified` status, canonical hash collision/mismatch, leaked secret, unauthorized side effect, evidence corruption, incompatible release, or undocumented claim promotion. The immediate response is to stop promotion/release, preserve evidence, mark affected outputs as `unverifiable`, identify scope by evidence ID/version, and issue a successor ADR/change record. Rollback restores a prior signed/reproducible release artifact and retains the incident trail.

## Change packet

Every substantial change includes problem statement, source/ADR links, affected claim classes, schema/API impact, tests/fixtures, benchmark impact, security/privacy review, evidence IDs, limitation update, release/rollback plan, dashboard status update, and next decision.
