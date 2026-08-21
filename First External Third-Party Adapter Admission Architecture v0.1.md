# First External Third-Party Adapter Admission Architecture v0.1

## Objective

The first external adapter is a governance proof, not a marketing partnership. It demonstrates that an independently sourced theoretical framework can submit a bounded structural predicate without receiving special evaluator behavior or a theory-level endorsement.

## Candidate profile

The first candidate SHOULD be selected for a small finite object, independently understandable predicate, openly licensable fixtures, stable notation, and a maintainer willing to publish assumptions and non-claims. It SHOULD NOT require proprietary data, a large legacy runtime, hidden numerical tolerances, live network calls, or an empirical/metaphysical conclusion.

## Admission lanes

| Lane | Artifact | Independent gate | Blocking condition |
|---|---|---|---|
| 0. Intent | One-page candidate brief | Scope and non-claims readable by non-maintainers | Framework-level conclusion embedded in brief. |
| 1. Semantics | Object schema and predicate specification | Reviewer can state input/output without source theory | Undefined notation, dimensions, or tolerance policy. |
| 2. Evidence | Frozen fixture pack and hashes | Positive, negative, malformed, boundary, mutation, neutrality cases | Missing expected outcome or implementation-derived oracle. |
| 3. Reference | Standalone reference evaluator | Deterministic replay in clean environment | Network/global-state dependency. |
| 4. Neutrality | Provenance-label test | Same object/check under ≥3 labels gives same receipt ID | Framework-conditioned code path. |
| 5. Assurance | Receipt, replay, local audit bundle | All recorded evidence is inspectable; absence is explicit | Local evidence presented as operational service. |
| 6. Review | Two-role review record | Semantics reviewer and implementation reviewer sign scoped findings | Unresolved disagreement. |
| 7. Release | Versioned adapter package | Reproducible build/test manifest and rollback point | Mutable release artifact. |

## Architecture

The admission system has five separated components:

1. **Candidate registry** stores descriptive metadata only; no candidate may influence kernel dispatch through this registry.
2. **Adapter package** contains a namespaced schema, pure reference evaluator, fixtures, tests, and documentation.
3. **Independent harness** runs package fixtures, mutation tests, replay tests, and neutrality tests outside the adapter’s own assertion path.
4. **Evidence ledger** records hashes, reports, review records, and optional local audit attachments.
5. **Publication boundary** exposes only admitted adapter IDs, versions, scopes, and non-claims; quarantined work remains clearly labeled.

## Governance roles

| Role | May do | May not do |
|---|---|---|
| Candidate maintainer | Define predicate, write reference evaluator, submit fixtures | Self-approve semantic and implementation review. |
| Semantics reviewer | Assess stated predicate, assumptions, and scope | Infer missing theory claims or modify evidence silently. |
| Implementation reviewer | Assess determinism, boundary handling, replay, neutrality | Decide scientific merit of framework. |
| Release steward | Publish immutable bundle and rollback metadata | Override failed gates. |
| Registry observer | Inspect artifacts and receipts | Treat admission as theory endorsement. |

## Required package layout

```text
adapter/
  ADAPTER_SPEC.md
  schema/claim_packet.schema.json
  reference/<pure evaluator>
  fixtures/fixture_pack.json
  tests/test_oracle.*
  evidence/fixture_manifest.sha256
  NON_CLAIMS.md
  LICENSE
```

## Success criterion

The first external adapter is admitted only when every lane passes and the published statement is: “This version of this adapter deterministically evaluates the stated predicate over the declared finite object.” It must not say that the source framework is true, complete, preferred, scientifically confirmed, or more fundamental than alternatives.

## First pilot decision

No real framework is preselected by this architecture. The pilot begins only after a candidate brief is submitted and evaluated under the same neutral lanes. This avoids using a design document to quietly choose a favored ontology.
