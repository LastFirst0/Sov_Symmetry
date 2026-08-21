# Sovereign Engine Skill and Pipeline Gap Matrix

## Installed skills to use now

| Skill | Approved program role | Output / gate | Current action |
|---|---|---|---|
| `evidence-first-technical-strategy` | Repository evidence, green-core extraction, ADR/release-gate design | Evidence matrix, ADRs, execution portfolio | Active |
| `github-gem-seeker` | Find mature foundations before building equivalents | Candidate matrix with license/security status | Active through GitHub CLI evidence |
| `youtube-video-research` | Extract first-hand maintainer/practitioner tradeoffs | Attributed video evidence, cross-validated | Active for Lean and Sigstore |
| `manus-api` | Define bounded task packets and structured result contracts | Orchestration contract / runbook | Active |
| `automation-and-scheduling` | Future recurring scans, drift audits, benchmark reviews | Policy first; no schedule until runbook approval | Deferred until policy package accepted |
| `builtin-llm-models` | Only if later building sandbox bulk classification/summarization or web LLM features | Model-selection and costed request design | Not needed yet |
| `persistent-computing` | Only if validated workloads require durable workers, cluster processes, or sustained benchmarks | Hosting decision memo | Deferred |
| `imagegen` / `video-generator` | Evidence-linked visual demos and educational assets | Asset provenance and claim labels | Optional adapter work |
| `webdev-readme-static` | Continue Mission Control Ledger as a read-only operational view | Dashboard data-model integration | Deferred pending authoritative backlog schema |
| `skill-creator` | Create Sovereign-specific skills only after repeated stable workflows are observed | Skill proposal and test fixture | Do not create yet |

## Candidate future Sovereign-specific skills

| Candidate | Trigger for creation | Required inputs | Deterministic output | Why not now |
|---|---|---|---|---|
| `sov-evidence-audit` | Three recurring evidence-package reviews with the same schema | Evidence manifest, predicates, records | Audit report with statuses and tamper/replay checklist | Schema is still being stabilized |
| `sov-fixture-authoring` | Three standard tensor fixture types repeatedly authored | Convention profile, operation ID, expected result | Fixture + manifest + invalid/tamper cases | Canonical AST/registry not implemented |
| `sov-claim-classification` | Recurrent need to triage transcript/repo claims | Source spans, references, claim metadata | Typed claim graph update + obligations | Vocabulary registry needs broader coverage |
| `sov-adr-review` | Multiple cross-workstream ADRs await review | ADR template, evidence matrix, decision rubric | Review checklist and decision recommendation | ADR backlog has only initial proposals |
| `sov-release-evidence` | Green core produces versioned artifacts | Build records, test results, hashes, SBOM | Release evidence bundle and verdict | No stable release pipeline exists |

## Pipeline policy

Every automated pipeline is a typed, bounded work package. It follows this chain:

`source manifest → claim/object classification → operation plan → deterministic execution or evidence review → status → immutable evidence record → dashboard projection → ADR/decision effect`.

LLM or agent stages can summarize, suggest, and generate drafts, but they cannot issue a `verified` status. Only registered deterministic predicates and reviewable evidence can do that. A failed tool call, missing source, or unstable interpretation is recorded as `unverifiable` with an obligation, not retried by invention.

## External-skill discovery status

The external skill finder’s live GitHub fetch path failed with a JSON-parsing issue and returned no cache matches. That is a discovery limitation. The program therefore relies on the installed skills above plus direct GitHub/documentation evaluation until a later verified skill search succeeds.
