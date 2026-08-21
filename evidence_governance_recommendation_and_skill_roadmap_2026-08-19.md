# Evidence-Governance Recommendation and Skill Roadmap

**Scope:** This roadmap concerns the dashboard’s governed evidence workflows. It does not change the universal kernel’s three-outcome contract, admit a quarantined adapter, infer reviewer independence, or make empirical, clinical, therapeutic, or personal-genomic claims.

## Prioritized recommendations

| Priority | Recommendation | Rationale and bounded outcome | Suggested acceptance evidence |
| --- | --- | --- | --- |
| 1 | Receipt-detail verification panel | Let an owner inspect a selected immutable manifest against its recorded digest and expose a clearly labeled local verification outcome. | Deterministic digest recomputation test, malformed-manifest failure case, owner-only router contract, and responsive review. |
| 2 | Receipt comparison export | Permit export of a two-receipt difference summary as CSV/JSON, retaining a separate comparison receipt rather than overwriting either source record. | Frozen comparison fixture, separate receipt schema or manifest namespace, no-write-on-source assertion, and hosted replay. |
| 3 | Receipt retention policy register | Replace the printable-summary guidance with a managed policy record that defines owner-selected retention categories and review dates without deleting evidence automatically. | Owner-only policy mutation, append-only revision history, expired-policy alert presentation, and failure-path tests. |
| 4 | Reviewer onboarding readiness board | Bring pending invitations, membership eligibility, current assignment workload, and near-expiry windows together without treating an invitation as a credential or independent review. | Joined data-contract tests, scope-safe labels, mobile/desktop review, and explicit non-admission copy. |
| 5 | Material-release evidence packet | Export a read-only release packet that links exact tag, commit, replay, gate, approval, and publication status; do not turn dashboard records into release authority. | Exact-commit mismatch negative test, independent local packet verifier, and hosted expected-failure evidence. |
| 6 | Structured data-intake provenance cards | Make approved source intake provenance and limitation fields easier to compare with research artifact receipts, keeping source acceptance distinct from an evidence verdict. | Durable schema mapping, source/claim-boundary tests, and public-safe display review. |

## Skills to create

| Proposed skill | Trigger and purpose | Reusable contents | Completion standard |
| --- | --- | --- | --- |
| `governed-receipt-operations` | Use when adding, inspecting, verifying, comparing, or exporting immutable dashboard receipt records. | Receipt schema reference, pure manifest/digest comparator, tRPC authorization template, fixture pack, and UI checklist. | At least one real receipt workflow uses it; its scripts pass normal and malformed-fixture tests. |
| `evidence-release-governance` | Use when changing replay, material-tag, approval, or release-note control paths. | Exact-commit policy template, GitHub workflow decision matrix, fail-closed test checklist, and evidence-record template. | A clean hosted replay and a retained expected-failure test validate the path. |
| `reviewer-onboarding-governance` | Use when extending reviewer membership, invitations, assignment events, or workload views. | Lifecycle state machine, role/scope authorization matrix, expiry-window helper, safe-copy guidance, and UI acceptance checklist. | Contract tests prove no invitation creates credentials or satisfies independent-review requirements. |
| `evidence-dashboard-accessibility` | Use when adding dashboards, printable summaries, exports, or audit panels that must remain legible and safe across devices. | Responsive/print checklist, semantic-table template, offline-copy limitations, keyboard tests, and no-secret display rules. | Desktop/mobile/print review and component accessibility tests pass. |
| `bounded-research-operations-roadmap` | Use when turning evidence gaps into sequenced, testable work packages without overclaiming research outcomes. | Prioritization rubric, risk register template, stop-rule template, acceptance-evidence matrix, and dependency graph guide. | Each proposed work package has a named boundary, owner, negative case, validation path, and completion artifact. |

> **Skill creation decision:** Create `governed-receipt-operations` first. It consolidates the workflow now repeated across archive exports, invitation exports, manifests, comparisons, digests, and owner-scoped history. Build the other skills only after one additional real use case demonstrates that their patterns recur.

## Delivery order

The next implementation should be the **receipt-detail verification panel**, followed by **receipt comparison export**, because both operate only on existing immutable records and can be tested without automating notifications, changing reviewer membership, or creating a release. The retention-policy register should follow after an owner explicitly chooses the organization’s retention categories and review cadence.
