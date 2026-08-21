# Sovereign Engine: Research, Architecture, and Operating-Policy Expansion Plan

## Purpose

This plan expands the existing Sovereign Engine roadmap from a directional program model into a **decision-ready technical operating system**. The goal is to eliminate avoidable future clarification loops by establishing default policies, architecture decision records, work-package templates, evidence standards, research pipelines, test gates, falsification procedures, integration boundaries, and escalation rules before broad implementation accelerates.

The plan does **not** assume that unresolved Geometric Unity (GU) claims are established physics. It creates a method for representing, testing, auditing, visualizing, and potentially falsifying those claims without contaminating the trusted software core or the project’s public narrative.

## Planning principles and default decisions

The following policies will be treated as defaults unless a future work item explicitly meets an exception criterion. This is intended to reduce questions that should already be settled by project policy.

| Policy area | Default decision | Exception threshold |
|---|---|---|
| Source of truth | Git repository + canonical evidence records + versioned project files | A new source must offer immutable IDs, provenance, export, and reviewability |
| Mathematical claim status | `standard`, `transcript_mapping`, `repository_observation`, `software_contract`, `gu_hypothesis` | Any added class requires an ADR and migration path |
| Result status | `verified`, `fail`, `unverifiable` only | A fourth status requires proof it does not weaken fail-closed behavior |
| Trusted core | Deterministic canonicalization, typed geometry, operation registry, invariants, replay, evidence | ML/LLM, UI, distributed services, and speculative GU modules remain adapters |
| Missing notation or equations | Return `unverifiable`; create an obligation record | Never infer missing theory from prose proximity |
| API strategy | OpenAPI-first, versioned, evidence-bearing, generated clients | Transport additions must preserve semantic contract and replay parity |
| Architecture change | ADR before cross-workstream interface changes | Emergency changes need incident record and retrospective ADR |
| Tests | Fixture-first, deterministic, versioned, tamper-tested | Exploratory notebooks cannot be merge/release evidence alone |
| Release rule | Release only on clean install, deterministic tests, evidence manifest, compatible API, and known-limitations record | Experimental release must be labeled and isolated |
| Security posture | Fail closed; least privilege; no untrusted callbacks; no production chaos from ordinary CI | Expanded authority requires a threat model and explicit owner |
| Research quality | Primary source + independent corroboration where possible; uncertainty recorded | Hypotheses may be logged without corroboration but not promoted |
| Human decision gates | Human review only for irreversible actions, physical-claim promotion, security exposure, scope changes, external publication, and budget changes | Everything else follows the approved policy matrix |

## Program research architecture

The research program will operate in six coordinated evidence lanes. Each lane will report explicit observed facts, recommendations, hypotheses, risks, and open obligations separately.

| Lane | Primary question | Principal sources | Outputs |
|---|---|---|---|
| A. Repository reality | What exists, runs, conflicts, and is credible today? | Git history, branch/workflow records, manifests, CI, source, tests, docs | Repository evidence matrix, credibility-gap report, green-core extraction map |
| B. Mathematical meaning | What do transcript equations and symbols actually mean? | Transcript spans, deep dive, standard references, formal sources | Equation registry, notation policy, theorem/assumption matrix, test candidates |
| C. System architecture | What architecture is necessary, sufficient, and defensible? | Existing architecture, code domains, comparable open source systems | Target architecture, ADR set, module boundaries, data/control-flow model |
| D. Competitive and ecosystem intelligence | Which tools, libraries, patterns, skills, and adjacent systems should be adopted, adapted, or excluded? | GitHub, package ecosystems, papers, maintainer docs, conference/video evidence | Build/buy/adapt matrix, skill/plugin register, integration risk ledger |
| E. Product and audience discovery | What audiences, use cases, terminology, and market-language gaps exist? | Project communications, public web/SEO research, user journeys, adjacent communities | Persona/use-case matrix, positioning options, keyword/competitor report if scoped |
| F. Validation and falsification | What could prove a software claim, mathematical mapping, or GU hypothesis wrong? | Fixture design, formal methods, numerical experiments, literature conflicts, adversarial review | Falsification register, test pyramid, benchmark plan, scientific review packet |

## Execution phases

### Phase R0 — Evidence freeze and research governance

**Purpose:** Make the next analysis round reproducible and ensure no result is silently based on stale or untraceable material.

1. Freeze a source manifest for the Git repository: commit, branches, tags, current working-tree state, workflows, lock files, key docs, generated artifacts, test inventories, and existing technical reports.
2. Inventory project-shared files, attached exploratory archives, existing website/dashboard artifacts, current connector configuration, available MCP capabilities, GitHub access, and Google Workspace materials available to this project.
3. Create a research register recording research question, lane, owner role, source set, confidence, delivery format, human-gate requirement, and expiry/review date.
4. Create policy documents for claim classification, source quality, citation, evidence retention, data handling, external integration, and expert-review escalation.
5. Establish a single ADR index and a standard ADR template with context, decision, alternatives, consequences, evidence, owner, review date, and reversal procedure.

**Exit criteria:** Every research work package has a source manifest and output schema. All future references can link to stable source paths or external URLs. The roadmap, control center, and dashboard have an authoritative input model.

### Phase R1 — Repository and Git history forensic analysis

**Purpose:** Recover a truthful picture of the codebase before expanding it.

1. Analyze the repository topology: Rust crates, Python kernels, Lean verification, apps, dashboard, database, logos, agents, scripts, CI, archived materials, and generated data.
2. Reconstruct architectural evolution from Git history: formation of subsystems, burst commits, abandoned branches, recurrent defects, files with high churn, core maintainers, and documentation drift.
3. Compare README/public claims, architecture documents, completion reports, status files, issue/PR history, CI workflows, lockfiles, and actual test/compile signals.
4. Identify a **green-core boundary**: the smallest installable, testable, user-relevant package that can be defended by reproducible evidence.
5. Produce an extraction/quarantine map: current path → retained core, adapter, integration surface, experimental area, archived/quarantine candidate, owner, and migration condition.
6. Run a static security and supply-chain review of dependency manifests, CI permissions, secrets exposure patterns, script execution, package boundaries, and release mechanics. Do not execute untrusted or destructive code.

**Exit criteria:** A repository evidence table, contradiction register, core-boundary proposal, CI credibility report, dependency/supply-chain risk report, and an ADR set for target modularization are complete.

### Phase R2 — Transcript, mathematics, and GU claim reconstruction

**Purpose:** Convert abstract discussion into a precise, evidence-labeled object model and explicit research obligations.

1. Reconcile the original transcript, supplied analysis, current meaning-layer dossier, and tensor-calculus deep dive into a **canonical equation and notation registry**.
2. For every equation, symbol, tensor index, connection, form, bundle, manifold, representation, and proposed dimensional structure, record: normalized notation, domain/codomain, units where relevant, assumptions, sign convention, source span, standard definition, physical interpretation, implementation type, invariant candidates, and claim class.
3. Build a concept/equation graph linking source spans to repository modules, APIs, tests, fixtures, demonstrations, external references, and open obligations.
4. Build a GU hypothesis dossier. For each GU-specific proposal—e.g., observerse, metric-bundle dimensional claims, 14D/75D references, E8 links, rolled-up complexes, generation claims, actions, and physical predictions—state: exact available definition, missing definition, theoretical prerequisites, derivation obligation, calculation/fixture candidate, empirical pathway, falsifiers, and promotion rule.
5. Create a notation and convention policy covering coordinate signatures, curvature signs, torsion signs, index placement, differential-form conventions, spinor/Clifford conventions, units, symbol aliases, and dimensional analysis.
6. Create an expert-review queue for items that cannot responsibly be resolved by repository inspection and public sources alone.

**Exit criteria:** Every priority concept and equation is typed, attributed, classed, and linked to either a test, a formal reference, or an explicit unresolved obligation. No prose-only physical claim appears in production contracts without a status boundary.

### Phase R3 — Architecture decision program

**Purpose:** Turn findings into an intentional architecture rather than incremental accretion.

The team will evaluate, decide, and record the following architecture topics through ADRs. Each ADR must compare at least two viable options, give a recommendation, list rejected alternatives, identify migration impact, and define verification criteria.

| ADR domain | Required decision | Default direction to evaluate |
|---|---|---|
| Core language boundary | Rust/Python/Lean division of responsibility | Rust for deterministic kernel/verifier, Python for exploration/fixtures, Lean for selected formal anchors |
| Canonical object model | AST, type system, schema versioning, IDs | Content-addressed immutable core + non-hashed display envelope |
| Symbolic/numeric model | How exact symbolic and finite numerical modes interoperate | Shared typed AST, explicit evaluator backends, no implicit numeric coercion |
| Tensor semantics | Index/variance/bundle/manifold/units rules | Compile-time or schema-time typed validation plus runtime verification |
| Operation registry | How operations and predicates are named/executed | Code-owned versioned registries; evidence cannot select arbitrary callbacks |
| Evidence ledger | Storage, hash policy, signing, replay, retention, queries | Append-only logical model, canonical serialization, manifest/replay verification |
| Claim graph | Relation between mathematical claims and software evidence | Claims reference evidence, not vice versa; physical claims require obligations |
| Runtime interface | Logos/Monad/retrieval/agent boundary | Runtime plans typed operations, kernel executes them, adapters only explain/visualize |
| API and SDK | REST/OpenAPI/CLI/MCP/FFI relationship | One semantic contract with generated clients and contract tests |
| Data persistence | Local/offline-first vs database/graph services | Start filesystem/SQLite-compatible evidence store; promote services only on measured need |
| Distributed/consensus surfaces | Whether/when colony, P2P, blockchain-like ideas are needed | Defer from green core until a specific verified use case and threat model exist |
| UI/demonstration | How exploratory games/apps map to actual kernel semantics | Curated adapters backed by fixture/evidence links, not independent truth models |
| Deployment | Developer-first packaging, CI, releases, environments | Reproducible local build plus artifacted CI; no production cluster before core gate |

**Exit criteria:** The ADR index defines the target architecture, component ownership, interface contracts, non-goals, migration sequence, and reversal conditions for every cross-cutting decision.

### Phase R4 — Build/buy/adapt ecosystem analysis

**Purpose:** Avoid inventing foundations that established projects already solve while preserving Sovereign Engine’s unique meaning/evidence layer.

1. Search GitHub and package ecosystems for mature candidates in symbolic math, tensor calculus, differential geometry, geometric algebra, graph databases, provenance, content addressing, proof assistants, schema validation, API code generation, observability, policy engines, static analysis, and developer portals.
2. Score candidates for license compatibility, community health, release cadence, documentation, typed interfaces, deterministic behavior, security posture, language compatibility, test maturity, integration cost, and abandonment risk.
3. Produce a **build/buy/adapt/avoid** matrix. Adopt only when the external project meets the trust boundary and can be wrapped by internal semantic contracts.
4. Search the verified skill ecosystem for reusable capabilities in scientific computing, formal verification, code review, testing, observability, research synthesis, documentation, project management, and agent orchestration.
5. Create a gap matrix distinguishing: existing installed skill, beneficial external skill to evaluate, necessary custom Sovereign Engine skill, and intentionally unsupported workflow.
6. Use the skill-creation framework only after repeated usage reveals a stable Sovereign-specific workflow. Candidate custom skills to assess include `sov-evidence-audit`, `sov-fixture-authoring`, `sov-claim-classification`, `sov-adr-review`, and `sov-release-evidence`.

**Exit criteria:** All foundational dependencies and skills have an explicit adopted/adapted/deferred/rejected decision, owner, license/security review state, and integration test requirement.

### Phase R5 — Connector, API, and automation control-plane design

**Purpose:** Make external capabilities auditable, least-privilege, and policy-driven instead of opportunistic.

1. Audit available connectors, MCP servers, GitHub capabilities, Google Workspace access, financial/market providers, and browser access. Classify each as research-only, development-only, production candidate, or excluded.
2. Define connector policy: secrets ownership, least privilege, allowed data classes, provenance requirements, caching/retention, failure handling, human confirmation boundaries, and vendor lock-in fallback.
3. Design Manus API v2 orchestration with Projects for durable policy, Tasks for bounded work packages, Files for source/output packages, Structured Output for machine-readable results, and Webhooks for production event delivery.
4. Specify task/result schemas for research intake, architecture review, implementation, test run, evidence audit, demonstration build, release preparation, and program review.
5. Define idempotency, retries, dead-letter handling, event signatures, state machine transitions, budget controls, agent-profile selection, and explicit handling of waiting/confirmation states.
6. Create a schedule policy for recurring research scans, CI/benchmark review, dependency watch, evidence drift audit, and milestone review. No schedule will be created until the policy and runbook are approved.
7. Define a connector-capability matrix: desired use, required tool, data classification, approved scope, fallback path, test method, and disable/rollback action.

**Exit criteria:** A zero-trust integration model, task orchestration contract, structured-result schema, webhook/retry policy, and connector approval matrix are complete. No connector is enabled or used beyond its approved role.

### Phase R6 — Competitive, gap, and audience research

**Purpose:** Ground product, documentation, communication, and developer adoption in evidence rather than internal terminology alone.

This phase contains two distinct tracks. The project does not yet have a declared public domain, target country, seed terms, or SEO data provider. Therefore, keyword research will not fabricate search volumes or competitor gaps. The plan establishes the research protocol and treats final country/data-source selection as a controlled decision.

1. Conduct a technical ecosystem comparison against relevant categories: computational geometry systems, symbolic/numeric math tools, theorem/evidence systems, AI agent orchestration frameworks, knowledge graph/provenance platforms, and interactive science/education experiences.
2. Perform an audience/use-case analysis: research mathematician/physicist, mathematical software engineer, AI-systems engineer, technical educator, collaborator/reviewer, and developer integrator. Identify jobs-to-be-done, confidence barriers, required evidence, and product surfaces.
3. Identify content/communication gaps between Sovereign Engine’s current vocabulary and terms practitioners actually use. Produce landing-page, documentation, developer-relations, and research-publication recommendations.
4. When an SEO/keyword track is activated, first record the seed topic(s), target country or global scope, domain/website scope, target audience, and chosen data source. If an Ahrefs, Semrush, DataForSEO, or Similarweb connector is available and explicitly approved, use it; otherwise label public-data findings as estimates. The eventual deliverable will follow the required three-tab, 300-keyword workbook structure.
5. Use primary-source conference talks, maintainer presentations, demos, and interviews where they materially clarify architecture or adoption tradeoffs. Analyze selected videos with structured quote/data extraction and cross-validate factual claims against documentation and independent sources.

**Exit criteria:** A competitor/ecosystem map, persona/use-case matrix, product gap analysis, terminology translation guide, and an SEO research brief with explicit scope/data-source decision are complete.

### Phase R7 — Verification, testing, benchmarking, and falsification program

**Purpose:** Define what it means for the system to be correct, incomplete, unsafe, slow, or scientifically unsupported before development expands.

1. Establish the test pyramid:

| Test layer | Target | Required controls |
|---|---|---|
| Static checks | Formatting, types, lint, dependency policy | Reproducible toolchain and lockfile checks |
| Unit tests | Canonicalization, typing, algebraic/tensor operations | Exact fixtures and invalid-input cases |
| Property/metamorphic tests | Symmetries, invariants, coordinate/convention transformations | Generated cases with bounded seeds and shrinkable failures |
| Golden fixtures | Standard mathematical examples | Versioned input/output/residual/assumption manifests |
| Differential tests | Internal backends versus trusted references | Explicit known divergence registry |
| Formal references | Selected high-value statements | Lean/formal proof links with implementation bridge status |
| API/contract tests | OpenAPI, SDKs, error semantics | Consumer/provider compatibility and generated-client tests |
| Replay/tamper tests | Evidence core and serialization | One-character change, unsupported operation, bad hash, missing assumption |
| Integration tests | Runtime plan → core operation → evidence → explanation | No opaque mutation and deterministic terminal status |
| Performance tests | Canonicalize, hash, operate, verify, replay | Hardware/toolchain/payload/concurrency evidence |
| Resilience tests | Bounded queues, storage persistence, worker loss | In-process fault injection before any cluster experiment |
| UX comprehension tests | Demonstrations and dashboard | Outsider task completion and misconception capture |

2. Create a falsification register. Each GU-specific hypothesis must list prerequisites, derivation, independent reproduction path, numerical/symbolic probe, contrary result, unresolved dependencies, and review status.
3. Create a claim-promotion ladder: `logged → specified → mathematically linked → fixture-tested → independently reviewed → empirical candidate`. Promotion requires stated evidence; no stage implies the next.
4. Define benchmark policy: record hardware, OS, toolchain, optimization flags, payload distribution, concurrency, allocations, p50/p95/p99, RSS, failure rate, and raw artifacts. Estimates remain estimates until target-environment measurements exist.
5. Define security/reliability tests: malicious evidence payloads, invalid schemas, registry mismatch, serialization collisions, dependency compromise signals, permission boundaries, webhook replay/signature failures, and data-store divergence.

**Exit criteria:** A versioned test strategy, fixture manifest format, invariant registry, benchmark harness plan, falsification register, release-evidence bundle definition, and failure-mode playbook are approved.

### Phase R8 — Roadmap synthesis and execution portfolio

**Purpose:** Convert the research round into a complete, sequenced, owned, and measurable program plan.

1. Replace broad roadmap language with a 30/60/90-day execution portfolio and milestone-sized releases.
2. For each work package, specify owner role, dependencies, decision rights, inputs, deliverables, acceptance criteria, evidence artifacts, test gates, user-facing demonstration, risk, non-goals, and next decision.
3. Calculate implementation effort and staffing scenarios using transparent assumptions; label estimates as ranges and maintain a capacity model.
4. Design a program dashboard data model and update the existing Mission Control Ledger to surface the authoritative backlog, evidence status, critical dependencies, ADRs, research confidence, and blocked decisions.
5. Write a release policy and change-management policy covering semantic versioning, deprecation, schema migration, API compatibility, evidence migration, documentation, incident response, and rollback.
6. Publish an executive technical package: architecture brief, program roadmap, ADR index, evidence/test strategy, falsification register, integration policy, ecosystem/skills matrix, and decision-request log.

**Exit criteria:** The revised roadmap is decision-complete for the next 90 days, with named workstreams, gate criteria, policy defaults, dependency dates, cost/risk assumptions, and an explicit decision backlog containing only genuinely irreducible choices.

## Research deliverables

| Deliverable | Format | Purpose |
|---|---|---|
| Research source manifest | Markdown + JSON | Reproduce every analysis input |
| Repository evidence matrix | Markdown + structured table | Separate observed state from recommendation |
| Green-core extraction plan | ADR set + migration map | Bound the first credible release unit |
| Canonical concept/equation registry | JSON/JSON-LD + human guide | Generate docs, APIs, prompts, fixtures, and visualizations |
| GU hypothesis and falsification dossier | Markdown + register | Make missing prerequisites and possible disproof visible |
| Architecture decision record set | ADR Markdown files | Lock cross-cutting choices and their reasons |
| Build/buy/adapt matrix | Spreadsheet/Markdown | Avoid recreating stable open-source foundations |
| Skill/plugin and connector matrix | Markdown + policy JSON | Make integration use intentional and auditable |
| Manus API orchestration kit | Schemas + runbook + examples | Make work packages repeatable rather than prompt-dependent |
| Verification and test strategy | Markdown + fixture manifest | Make claims replayable and releases defensible |
| Benchmark and reliability protocol | Markdown + harness design | Prevent imaginary performance/reliability claims |
| Competitor/gap and audience analysis | Report + optional keyword workbook | Bridge internal terminology and external relevance |
| Expanded 30/60/90-day roadmap | Markdown + dashboard data | Coordinate portfolio execution |

## Decision protocol: questions eliminated vs. questions retained

The program will not ask for confirmation on routine decisions already covered by the policy table. It will ask only when a choice changes irreversible scope, legal/privacy exposure, capital/time commitment, physical-claim promotion, external publication, security posture, or a key product audience.

| Decision type | Policy result | Human input needed? |
|---|---|---|
| Missing GU equation | Mark `unverifiable`; create obligation | No |
| Ambiguous notation | Preserve source and register normalized candidate with uncertainty | No, unless it changes a promoted claim |
| New core dependency | Score build/buy/adapt against adopted rubric | No for evaluation; yes for license/security exception |
| Test addition | Follow test-pyramid and fixture policy | No |
| CI gate change | Apply release-evidence criteria | Yes if it affects developer workflow or release latency materially |
| Connector usage | Follow connector approval matrix | Yes only for new scopes, secrets, or external side effects |
| SEO volume data | Never fabricate | Yes: country/global scope and data-source decision are required only when that workstream activates |
| GU hypothesis publication | Require promotion-ladder evidence and independent review | Yes |
| Large architecture change | ADR with reversible path | Yes if it changes green-core boundary or major technology commitment |

## Assumptions and open risks

1. The repository checkout, project-shared source files, and existing previous deliverables are available as the initial evidence base.
2. GitHub integration is available for repository/history analysis; Google Workspace sources will be reviewed only where the currently configured access permits and only as data, not as instructions.
3. Connector and MCP availability will be audited before any external-service-dependent research pipeline is invoked; new connector creation or scope escalation will require user confirmation through the normal review flow.
4. Keyword research is conditional on a later explicit scope decision, because the mandatory country and data-source choices are currently unknown.
5. The plan will prioritize authoritative source material and exact repository evidence over broad commentary. Video research is supplemental primary evidence and will be cross-validated.
6. No project code will be executed merely to inspect it. Any test, build, benchmark, or simulation execution will be explicitly classified, sandboxed, versioned, and recorded as evidence.

## Completion standard

The research and architecture round is complete only when the expanded roadmap can be used to create bounded work packages with no repeated rediscovery of scope, policy, acceptance criteria, evidence status, or integration rules. Remaining open questions must be visible in a decision backlog and must be genuinely consequential—not routine details that the program should have decided for itself.
