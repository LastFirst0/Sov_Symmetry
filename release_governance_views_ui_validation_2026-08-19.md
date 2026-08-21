# Release Governance Views — UI Validation Record

**Date:** 2026-08-19  
**Route reviewed:** `/archive`  
**Scope:** Public release-evidence index, owner-scoped reviewer invitation-expiry reminder, and owner-scoped material-tag approval workspace.

## Responsive review

| Viewport | Observation | Result |
| --- | --- | --- |
| Desktop, 1280 × 720 | The archive header, existing publication controls, and new governance surfaces render in the established archive layout. Public evidence uses explicit result labels, scope, limitation, and outbound record links. | Reviewed |
| Mobile, 375 × 812 | The full archive remains a single-column vertical sequence. New release-evidence and governance content follows the existing mobile reading order, with no horizontal presentation-only affordance required to understand validation state. | Reviewed |

## Boundary checks

The **Public Release Evidence** panel contains no token field, dispatch action, or other release-control input. It exposes only bounded status, source commit, timestamp, scope, limitation, and an inspectable GitHub record link.

The **Invitation Expiry Reminders** and **Material Tag Approval** panels are visibly owner-scoped. They require the existing in-memory owner token before requesting invitation lifecycle data, tag eligibility, or workflow dispatch. They make no email, credential, membership, tag-creation, approval-record-editing, or release-note-publishing claim.

The owner approval flow dispatches the canonical GitHub approval workflow only after a dashboard preview reports a matching successful unified replay and material gate for the tag’s exact commit. The GitHub workflow independently repeats those validations before writing any approval record.

## Limitations

This review confirms rendered layout and declared access boundaries. It does not create an actual material tag, dispatch an approval from the UI, or publish a release note. The separately retained hosted negative test remains the evidence that an existing but unapproved tag is blocked before publication.

## Clean hosted replay

The clean GitHub-hosted **Dashboard Contract Replay** completed successfully as [run 32243335662](https://github.com/LastFirst0/sovereign-engine-dashboard/actions/runs/32243335662) for dashboard commit `93e236af4a997ac0c988e2278a027aa940225304`. The replay validates the committed dashboard contracts and production build without receiving the server-only GitHub release-integration credential. Credential-dependent live checks therefore remain explicitly opt-in in that environment; they do not use a fallback token or report an inferred success.

## Near-expiry invitation export review

The owner-scoped **Invitation Expiry Reminders** panel now presents a manually triggered **Download expiring invitations CSV** control alongside its owner token input. At desktop (1280 × 720) and mobile (375 × 812) widths, it stays in the established single-column governance flow and remains keyboard-reachable. The copy specifies the fixed 72-hour pending-invitation boundary, the omitted sensitive fields, and the audit-receipt behavior.

The review did not create a production export receipt or download an invitation list. Contract tests cover the exact pending/72-hour lifecycle filter, CSV escaping, omission of terminal records, the owner-only API boundary, and receipt-creation call. The export intentionally contains no invitation notes, proposed reviewer IDs, reviewer tokens, or membership changes.

The clean GitHub-hosted **Dashboard Contract Replay** also passed as [run 32245286879](https://github.com/LastFirst0/sovereign-engine-dashboard/actions/runs/32245286879) for export source commit `10b3633eef3e27a632108e582ea6266ef8a43954`. As with the preceding governance replay, the hosted runner received no server-only integration credentials; external live checks remain explicitly opt-in rather than being simulated or silently bypassed.

## Configurable export and printable summary review

At desktop width, the invitation reminder panel retains its owner-token boundary while exposing a 24-, 48-, or 72-hour window selector, manual CSV export action, receipt-history action, and printable-summary action. The controls remain grouped in the existing governance flow rather than appearing as public archive actions. A loaded print view contains only the export-safe invitation fields, selected window, generated timestamp, and a point-in-time limitation; print styling suppresses surrounding application chrome.

The clean GitHub-hosted **Dashboard Contract Replay** passed as [run 32246846678](https://github.com/LastFirst0/sovereign-engine-dashboard/actions/runs/32246846678) for configurable-workflow commit `73c6e005058fd95a859e47905c691e718dc835c0`. As with prior governance replays, the hosted runner did not receive server-only credentials; live external checks remained explicit opt-ins.

## Receipt manifest and comparison review

The owner receipt-history surface now offers selected-receipt manifest inspection and two-receipt comparison only after the owner-scoped history has been loaded. Manifest detail is bounded to the stored invitation ID and recorded expiry timestamp. Comparison shows selected window, count, digest equality, and entry-set differences, while expressly declining to infer a reviewer’s current status or the cause of a difference. The printable summary also includes a short owner-controlled retention note. Mobile review preserved the archive reading order for the new controls.

The clean GitHub-hosted **Dashboard Contract Replay** passed as [run 32247880850](https://github.com/LastFirst0/sovereign-engine-dashboard/actions/runs/32247880850) for receipt-detail source commit `02eee213a80bd989523e9ff10ae3927d5aadc213`. No server-only integration credentials were injected; external live checks remained explicit opt-ins.

## Local digest and comparison-report review

The receipt manifest view now offers browser-local SHA-256 recomputation against the retained digest. It presents only match, mismatch, or unavailable outcomes and does not modify the receipt ledger. A loaded two-receipt comparison now offers read-only CSV and JSON report downloads that preserve selected receipt identity, declared metadata, manifest-entry differences, and an interpretation boundary. Mobile review preserved the archive reading order for these additional owner-only controls.

The clean GitHub-hosted **Dashboard Contract Replay** passed as [run 32248711816](https://github.com/LastFirst0/sovereign-engine-dashboard/actions/runs/32248711816) for local-digest and comparison-report source commit `2e1110065404ad0cf1438fdebbc0507d1f1df473`. The hosted runner did not receive server-only integration credentials; external live checks remained explicit opt-ins.
