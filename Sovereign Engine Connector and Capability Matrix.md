# Sovereign Engine Connector and Capability Matrix

## Current enabled capabilities

The following capabilities were observed as enabled during the Phase R0 inventory. Enablement does not itself authorize every use; each invocation must remain within the approved scope below.

| Capability | Observed state | Approved near-term role | Data class | Default classification | Fallback | Disable / rollback |
|---|---|---|---|---|---|---|
| GitHub | Enabled | Repository history, PR/issue/CI evidence, release metadata, open-source evaluation | Repository metadata and user-authorized source | Development + research | Local clone and public repository pages | Stop CLI/API queries; preserve local evidence manifest |
| Google Workspace | Enabled | Read-only source inventory and selected project documents | User-controlled documents | Research-only | Project-shared files and user-provided exports | Stop document retrieval; remove document IDs from active source manifest |
| Cloudflare | Enabled | Future deployment/edge architecture research only | Infrastructure metadata | Excluded from core research execution | Public docs / local architecture | Do not invoke account-changing operations |
| Cloudflare Worker Bindings | Enabled | Future data-store and Worker feasibility research only | Infrastructure metadata | Excluded from core research execution | Local prototypes | Do not create, mutate, or deploy bindings |
| Mobbin | Enabled | UI-pattern research for future product surfaces | Public UI references | Research-only | Public design documentation | Stop reference lookup; retain only source URLs |
| CoinGecko | Enabled | Not relevant to current meaning-kernel scope | Market data | Excluded | None needed | Do not invoke |
| Financial Datasets | Enabled | Not relevant to current meaning-kernel scope | Financial data | Excluded | None needed | Do not invoke |
| PopHIVE | Enabled | Not relevant to current meaning-kernel scope | Public-health data | Excluded | None needed | Do not invoke |

## Control-plane policy

The program treats external integrations as untrusted dependencies. Their outputs may inform research but cannot establish a mathematical, physical, or software claim without provenance, independent review where material, and explicit claim classification.

| Control | Default requirement |
|---|---|
| Least privilege | Use only the narrow operation required by the active research work package. |
| External effects | No deployment, publication, configuration mutation, credential change, or schedule creation without explicit human confirmation. |
| Provenance | Record connector/provider, query/purpose, access date, returned source IDs/URLs, and material limitations. |
| Retries | Retriable reads are bounded and idempotent; write requests require an idempotency key and review gate. |
| Data minimization | Retrieve only source fields needed for the research claim; do not export secrets, private tokens, or unrelated documents. |
| Failure | Provider error, access denial, schema drift, or ambiguous result produces `unverifiable`, not a guessed substitution. |
| Vendor fallback | Preserve a provider-neutral source model so each result can be re-collected through another approved source. |

## Proposed Manus API task modes

| Mode | Purpose | Required structured result fields | Human gate |
|---|---|---|---|
| `research_intake` | Normalize a source or external research finding | source IDs, observed facts, claim classes, confidence, limitations, obligations | No |
| `architecture_review` | Compare architecture options and create an ADR packet | options, decision drivers, recommendation, reversibility, tests, risks | Cross-workstream core decision |
| `implementation_packet` | Implement a bounded approved work package | changed files, tests, fixtures, API impact, evidence IDs, open risks | Code/architecture review |
| `evidence_audit` | Verify a claim or evidence bundle | canonical inputs, predicates, statuses, counterevidence, replay result | No unless promotion requested |
| `release_packet` | Prepare a release-quality bundle | version, compatibility, clean install, checksums, limitations, rollback plan | Release decision |
| `program_review` | Summarize progress and blocked decisions | milestone state, evidence delta, risks, dependencies, next portfolio | Resourcing or scope change |

## Explicitly deferred integrations

The program does not yet require a production database, payment provider, external hosting, social distribution, calendar automation, CRM, or financial/public-health data feeds. These remain excluded until a specific approved user story, data classification, threat model, and fallback path exist.
