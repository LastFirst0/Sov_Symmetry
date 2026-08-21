# Evidence-First Gate Matrix

| Gate | Claim | Required evidence | Blocked if failed |
|---|---|---|---|
| G0 | Authority is explicit | Source manifest, authority hierarchy, accepted decision records | Interpretation and policy changes |
| G1 | Core is deterministic | Canonical bytes, schema, ID, error, fixture tests | Storage, audit, API work |
| G2 | Implementations agree | Shared vectors: bytes, IDs, statuses, reason codes, outputs | Release claims beyond reference |
| G3 | Evidence survives replay | Clean restore, manifest verification, tamper/collision cases | Audit/signing work |
| G4 | Audit is cryptographically bounded | Key policy, payload binding, proof, equivocation tests | Quorum/release attestation |
| G5 | Quorum is a bounded aggregation | Unique signer, policy, conflict, stale/revoked key, availability tests | Multi-node deployment claims |
| G6 | Claims remain legible and bounded | Source → claim → evidence → limitation trace | Public explanation or dashboard |
| G7 | Release is reproducible | Clean build, SBOM, release packet, rollback drill | Published artifact |
