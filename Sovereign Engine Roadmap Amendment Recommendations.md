# Sovereign Engine Roadmap Amendment Recommendations

**Review basis:** The 90-day portfolio, target architecture/ADR program, validation strategy, repository evidence matrix, and ADR index as of 2026-08-16.  
**Bottom line:** Preserve the evidence-first core. Tighten its operating model before implementation. The package is strong on vision, boundaries, and test categories; it is weaker on decision finality, source-of-truth control, threat modeling, and the precise v0.1 core contract.

## Priority amendments

| Priority | Change | Why it matters | Concrete amendment | Effect if accepted |
|---|---|---|---|---|
| P0 | **Replace “decision-complete” with “policy-complete, pending ADR acceptance.”** | All twelve foundational ADRs remain `Proposed`, while the portfolio assumes their defaults. This creates a governance contradiction: teams can claim a policy is settled without accepting the decision. | Add an **ADR ratification sprint** before WP-04. ADR-001, 002, 003, 005, and 006 must be `Accepted` or explicitly `Rejected` with a reversible alternative. “Pending” must not unlock core implementation. | Prevents false certainty and stops future re-litigation of the trusted boundary. |
| P0 | **Add a source-of-truth hierarchy.** | The current program uses repository files, project-workspace files, Google Drive documents, generated assets, and external sources. Without an authority hierarchy, conflicting documents can quietly compete. | Adopt: `accepted ADR + versioned core spec` > `canonical registry/evidence records` > `repository implementation/tests` > `approved research register` > `Drive historical documents` > `transcript interpretation` > `dashboard projection`. Every artifact declares its authority tier. | Removes ambiguity over which artifact wins when claims or designs differ. |
| P0 | **Write a Core Contract v0.1 before K0 implementation.** | The architecture identifies the core, but it does not yet freeze the exact object algebra, canonical bytes, error taxonomy, determinism policy, or extension rules. | Add `SOV_CORE_CONTRACT_v0.1.md` with exact schemas for object IDs, scalar domain, tensor indices, dimensions, convention profiles, units, errors, status transitions, hash input, and extension/version rules. Require 10–20 canonical plus invalid/tamper vectors. | Turns the green-core concept into an implementable, reviewable specification. |
| P0 | **Add a threat model and data-governance policy.** | The evidence/connector model handles provenance but not adversaries, sensitive inputs, source licenses, retention, redaction, or privacy. Current repository evidence also shows insecure development-default credentials in an adapter. | Add `THREAT_MODEL_v0.1.md` and `DATA_GOVERNANCE_POLICY.md`. Define assets, adversaries, trust boundaries, abuse cases, secret handling, data classifications, source licensing/attribution, retention, export, redaction, and incident severity. | Makes the evidence layer safe to use with real sources and prevents premature connector expansion. |
| P0 | **Split CI before feature growth.** | The current broad launcher fails through an unrelated Python import path, so it is not a credible health signal for the future core. | Make WP-03 produce five independent checks: pinned static/toolchain, pure core unit/fixtures, reference/formal anchors, integration smoke, advisory experiments. Make only the first two required for v0.1. | Gives the program an honest green signal and isolates experimental breakage. |
| P1 | **Add a mathematically explicit numerical-analysis policy.** | “Precision” appears in the validation plan, but no policy fixes scalar fields, exact-versus-float selection, tolerance derivation, coordinate singularities, conditioning, or residual interpretation. | Add `NUMERICAL_SEMANTICS_POLICY.md`: rational/symbolic versus IEEE float rules, absolute/relative tolerance structure, NaN/∞ policy, conditioning flags, coordinate/chart validity, and reproducibility of BLAS/toolchains. | Prevents numerical agreement from being mistaken for a theorem. |
| P1 | **Move the Lean work earlier and narrow it.** | A Lean audit in weeks 7–9 is too late to discover that formal anchors are stale, unbuildable, or semantically disconnected from core types. | Split WP-10 into `WP-10a` in Week 2: inventory/build/check every candidate proof and map theorem claims to source; then `WP-10b` in Weeks 7–9: one high-value bridge proof. | Reduces late architectural surprises while keeping formalization bounded. |
| P1 | **Make test-oracle policy explicit.** | Differential tests are planned, but the plan does not state when a reference library is eligible as an oracle, how disagreements are adjudicated, or when an internal predicate takes precedence. | Add an oracle hierarchy: exact formal result; analytic fixture; independently implemented standard reference; symbolic reference; numerical reference; no oracle → `unverifiable`. Every differential fixture records expected divergence scope. | Prevents “two implementations agree” from becoming an unexamined correctness claim. |
| P1 | **Add a termination and pivot policy.** | The roadmap controls scope but does not state when to abandon, redesign, or isolate a module whose assumptions cannot be completed. | Define stop conditions: two incompatible convention profiles without resolution; no reproducible theorem bridge; repeated nondeterministic canonical bytes; reference disagreement unresolved after triage; no user can finish an audit journey after two iterations. | Converts sunk-cost risk into a planned decision process. |
| P1 | **Add measurable program and user outcomes.** | Gates are artifact-centric. They do not yet show whether the meaning layer makes work clearer, faster, or safer for an outside user. | At R0 record baseline review latency, CI isolation, and audit-journey completion. At R3 set explicit improvement targets after baseline, not before. Capture confusion points and misinterpretations as defects. | Keeps the platform from becoming internally elegant but externally unusable. |
| P1 | **Upgrade release operations from a policy to a runbook.** | The release policy has good categories but omits a release captain, severity taxonomy, evidence retention, approval ownership, emergency rollback ownership, and post-incident review. | Add `RELEASE_RUNBOOK.md` and `INCIDENT_SEVERITY_MATRIX.md`; define required approvers by release class, hold points, retention windows, and drill frequency. | Makes a future “release evidence bundle” operational rather than aspirational. |
| P2 | **Make API exposure deliberately later and narrower.** | The OpenAPI baseline is valuable, but server/API work risks freezing transport semantics before core object/error semantics are stable. | Reframe WP-11 as **schema and SDK compatibility design** only. Do not stand up a public service or external webhook until Core Contract v0.1 and G3 replay are passed. | Protects the core from premature client and network commitments. |
| P2 | **Add a dependency admission policy.** | The build/buy/adapt matrix identifies candidates but not a repeatable acceptance process for packages, transitive dependencies, licenses, security notices, or removal. | Require an admission record: purpose, authority boundary, license, maintainer/activity signal, pinned version, SBOM entry, test fixture, fallback/removal plan. | Avoids dependency creep and unclear external authority. |
| P2 | **Synchronize status automatically.** | The ADR index is still `Proposed` and several research lanes remain active/queued although related artifacts were produced. | Define `draft → reviewed → accepted/deferred → superseded` states and make a program-review check reconcile ADR index, research register, dashboard JSON, and portfolio status. | Prevents the dashboard and documents from drifting into a second source of truth. |

## Remove or rewrite

| Action | Item | Rationale | Replacement |
|---|---|---|---|
| Remove from active plan | Any performance language such as “O(1) navigation,” “100% scale-invariant,” or accelerator claims without workload-specific evidence | The repository evidence matrix already classifies these as unsupported documentation assertions. | Keep as attributed claims in a benchmark obligation ledger with workload, resource model, and disconfirming condition. |
| Remove from core roadmap | Celestial/narrative mappings, scripture-ingestion semantics, broad E8 “resonance,” and consensus/blockchain framing | They are neither required to establish a geometry/evidence core nor currently specified/reproducible. Their presence amplifies confusion and credibility risk. | Place in a `research-quarantine` portfolio, with only source/claim/falsifier normalization work permitted. |
| Rewrite | “Acceleration” scenario’s implication that it reliably adds three demos | FTE arithmetic does not include integration, reviewer, CI, and coordination overhead. | State it as a capacity hypothesis subject to G2/G3 evidence, not a delivery promise. |
| Rewrite | The three-status result model as the sole lifecycle state | `verified`/`fail`/`unverifiable` are result statuses, not review, availability, reproducibility, or publication states. | Keep the three result statuses; add separate evidence lifecycle and claim-promotion state machines. |
| Remove from early scope | Custom skills and broad agent autonomy | Both depend on a stable repeated workflow and would ossify an immature schema. | Retain only bounded task templates and typed work-result envelopes. |

## Defer with explicit reopening conditions

| Deferred area | Reopen only when |
|---|---|
| Graph database, embeddings, vector retrieval | Offline evidence replay and a measured query/use-case profile show files/SQLite are insufficient. |
| Public API, webhooks, client publication | Core Contract v0.1, G3 replay, contract compatibility, threat/data policy, and release runbook are accepted. |
| Sigstore enforcement or private trust infrastructure | Reproducible artifacts exist, audit-only signing has succeeded, CI identity is defined, and an operations owner accepts the burden. |
| P2P, consensus, Proof-of-Useful-Work | A specific user problem, adversarial model, protocol spec, and standard test/failure suite exist. |
| GU physical-claim evaluator | A source-complete mathematical statement includes spaces, actions, representation, observable consequence, and falsifier. |
| External skill creation | The same typed workflow has produced three stable, reviewed examples with recurring inputs/outputs. |

## Recommended revised first wave

The original first wave was **WP-02, WP-03, WP-04**. I would change it to a six-week foundation sequence that is still compact but removes hidden assumptions:

| Sequence | Work | Exit condition |
|---|---|---|
| F0 | Authority hierarchy, source/data governance, threat model | Every source and artifact has authority/data class and handling rule. |
| F1 | ADR ratification: 001, 002, 003, 005, 006 | Accepted decisions or clearly stated reversible alternatives; no “pending” core scope. |
| F2 | Core Contract v0.1 plus fixture/oracle/numerical policies | Exact schema, canonicalization, error/tolerance rules, and initial test vector set are versioned. |
| F3 | Extract pure core and split CI | Clean core job passes independently of workbench/network/optional components. |
| F4 | Implement a thin vertical slice | One metric/tensor operation produces a replayable evidence record and an invalid/tamper case. |
| F5 | Review and pivot | Review cost, deterministic behavior, user audit clarity, and open assumptions before K3–K6. |

## What I would keep unchanged

Keep the five claim classes, narrow evidence–geometry core, Rust/Python/Lean separation, immutable core/mutable envelope distinction, `verified`/`fail`/`unverifiable` result vocabulary, controlled adapter boundary, standard-fixture-first testing, audit-only signing stance, and explicit GU hypothesis quarantine. They are the strongest parts of the existing strategy.

## Only human decisions that remain after these amendments

The amendments reduce the human decision surface to capacity, external-release scope, named expert-review participation, and any truly breaking canonicalization migration. All other questions should be answered by the ratified policies and ADRs above.

## Internal references

- `SOVEREIGN_ENGINE_DECISION_COMPLETE_90_DAY_PORTFOLIO.md`
- `TARGET_ARCHITECTURE_AND_ADR_PROGRAM.md`
- `VALIDATION_AND_FALSIFICATION_STRATEGY.md`
- `REPOSITORY_EVIDENCE_MATRIX.md`
- `ADR_INDEX.md`
