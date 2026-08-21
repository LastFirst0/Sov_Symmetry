# External Adapter Eight-Gate Scorecard and Checklist v0.1

## Use

Use one scorecard per candidate adapter release. A candidate passes only when every required row is marked **Pass** with linked evidence. “Not applicable” is not allowed for neutrality, fixtures, replay, scope, or release; a candidate that cannot satisfy a gate is quarantined rather than admitted.

| Gate | Required evidence | Pass condition | Reviewer decision | Evidence link / hash |
|---|---|---|---|---|
| 0. Intent | Candidate brief and non-claims | Predicate and scope are understandable without accepting source theory. | Pass / Block | |
| 1. Semantics | Object schema, notation, dimensions, tolerance policy | Independent reviewer can restate input, output, assumptions, and failure cases. | Pass / Block | |
| 2. Evidence | Frozen fixture pack and manifest | Positive, negative, malformed, boundary, mutation, and neutrality cases are declared before test run. | Pass / Block | |
| 3. Reference | Pure reference evaluator and clean-run log | Same declared input produces same receipt in a clean environment with no network/global state. | Pass / Block | |
| 4. Neutrality | ≥3 provenance-label comparison report | Same object/check returns same status and receipt ID under each label. | Pass / Block | |
| 5. Assurance | Replay bundle and optional local audit evidence | Recorded evidence is inspectable; unavailable layers are marked unavailable. | Pass / Block | |
| 6. Review | Semantics and implementation review records | Two independent scoped reviews are complete; disagreements are resolved or block release. | Pass / Block | |
| 7. Release | Versioned package, test report, manifest, rollback point | Immutable artifacts and scoped public statement are published. | Pass / Block | |

## Scorecard completion checklist

- [ ] Candidate has no theory-level conclusion in its adapter specification or receipts.
- [ ] Fixture expectations were written before running the candidate implementation.
- [ ] Non-finite values, shape errors, and undefined conventions fail closed.
- [ ] A one-field mutation of each positive fixture produces an explained result change or `unverifiable`.
- [ ] Framework name is used only as provenance; no runtime branch reads it to choose a predicate.
- [ ] Every user-facing claim says what the adapter checks and what it does not establish.
- [ ] Release steward confirms all artifact hashes and records the version identifier.

## Final decision

| Candidate ID | Version | Decision | Blockers / conditions | Release steward | Date |
|---|---|---|---|---|---|
| | | Admit / Quarantine / Reject | | | |
