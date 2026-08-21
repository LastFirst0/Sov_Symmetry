# Sovereign Engine Program Roadmap and Strategy

## Goal

Move Sovereign Engine from a sequence of isolated, small-step explorations into a coordinated research-and-engineering program with a stable north star, explicit workstreams, shared contracts, milestone gates, reusable automation, and evidence-based release criteria.

> **Decision-complete addendum (2026-08-16).** The broad program direction in this document is now operationalized by `SOVEREIGN_ENGINE_DECISION_COMPLETE_90_DAY_PORTFOLIO.md`, `TARGET_ARCHITECTURE_AND_ADR_PROGRAM.md`, `RELEASE_AND_CHANGE_MANAGEMENT_POLICY.md`, `VALIDATION_AND_FALSIFICATION_STRATEGY.md`, and `PROGRAM_DASHBOARD_INPUT_MODEL.json`. Those documents define the default architecture, work-package acceptance criteria, test/falsification gates, release rules, and the small set of decisions that cannot be resolved by policy.

The program should produce a **geometry-native, provenance-aware, verifiable meaning system** without treating unresolved Geometric Unity claims as established physics. The immediate strategic objective is to make the project coherent and developable: every major concept should have a canonical definition, a software representation, an invariant or test, an evidence status, and a visible path to demonstration.

## Strategic thesis

Sovereign Engine should be built as a **meaning infrastructure platform**, not as a collection of loosely connected experiments and not as an unsupported theory-of-everything implementation. The platform has five layers:

| Layer | Strategic role | Primary output |
|---|---|---|
| Meaning ontology | Define what the system believes an object, relation, transformation, observation, claim, and proof are | Canonical ontology and glossary |
| Mathematical kernel | Represent typed manifolds, tensors, forms, connections, curvature, projective geometry, E8 operations, and symbolic expressions | Deterministic tensor/geometry library |
| Verification and provenance | Check invariants, preserve assumptions, replay operations, and separate verified facts from hypotheses | Evidence ledger and status engine |
| Intelligence/runtime | Use Logos, Monad, colony, routing, retrieval, and translation over the verified substrate | Geometry-aware reasoning runtime |
| Embodiment and automation | Make the system understandable and useful through UI, visualization, games, hardware, APIs, and Manus-driven workflows | Demonstrations, clients, agents, and operational loops |

The primary dependency direction is **ontology → kernel → verification → runtime → embodiment**. Experiments can proceed in parallel, but production claims must flow through this dependency spine.

## Program principles

1. **One canonical vocabulary.** Every term from the transcript, repository, or prototype must have one preferred definition, aliases, source references, confidence status, and owning module.
2. **Separate mathematics from interpretation.** Standard mathematical definitions, transcript mappings, repository observations, software contracts, and GU physical hypotheses must be different claim classes.
3. **Small trusted core, broad adapters.** The trusted core should remain deterministic and narrow. Logos, LLMs, visualizers, games, and external integrations should consume and explain core records rather than silently redefine them.
4. **Evidence before scale.** Do not optimize swarm scale, broad multimodal translation, or ambitious physical claims before the kernel and replay system work on controlled fixtures.
5. **Every result has a status.** The system returns `verified`, `fail`, or `unverifiable`; it never fills missing theory with plausible prose.
6. **Demonstrations are first-class.** Each major abstract capability must have an explanatory visual, a machine-readable fixture, and a user-facing demonstration.
7. **Automate the program, not just individual tasks.** Manus API should orchestrate bounded research, implementation, test, documentation, and review tasks around shared artifacts and project instructions.

## Target operating model

The project should be managed as a portfolio of coordinated workstreams with a single program backlog and a common evidence model. Each workstream owns deliverables, but no workstream is allowed to establish cross-cutting claims without linking to canonical objects and evidence records.

| Workstream | Owner role | Scope | Exit artifact |
|---|---|---|---|
| WS-A: Meaning and ontology | Research architect | Glossary, claim taxonomy, source map, concept graph, identity model | Versioned meaning-layer specification |
| WS-B: Tensor and geometry kernel | Mathematical software lead | Tensors, indices, manifolds, metrics, connections, forms, curvature, E8/projective operations | Tested library and reference fixtures |
| WS-C: Verification and evidence | Reliability/provenance lead | Invariants, replay, hashes, status engine, evidence ledger, claim evaluation | Verification service and audit reports |
| WS-D: Runtime and intelligence | Systems lead | Logos, Monad, retrieval, transformation planning, routing, colony/consensus adapters | Runtime integration against verified kernel |
| WS-E: Embodiment and UX | Product/visualization lead | Dashboards, explorers, games, audio, hardware, explanatory renderers | Demonstration suite and user journeys |
| WS-F: API and developer platform | API/platform lead | OpenAPI, SDKs, CLI, MCP, webhooks, versioning, examples, compatibility | Client-generation-ready developer platform |
| WS-G: Program automation | Automation lead | Manus API tasks, projects, files, structured outputs, webhooks, scheduled research/build loops | Reproducible orchestration workflows |
| WS-H: Scientific validation | Independent review lead | Literature checks, mathematical review, numerical benchmarks, claim audits, falsification attempts | Evidence and limitations register |

## Program phases and gates

### Phase 0 — Program reset and baseline

**Objective:** Establish the single source of truth and stop fragmentation.

Create a versioned program charter, repository map, terminology registry, evidence taxonomy, architecture decision record index, and backlog organized by workstream. Freeze a baseline commit and record the current state of the meaning dossier, OpenAPI contract, tensor simulation, slide deck, attached prototypes, and repository inventory.

**Gate 0:** Every major existing artifact is assigned to an owner workstream, a status, and a next decision. No new feature starts without a workstream, acceptance criteria, and evidence target.

### Phase 1 — Meaning layer and claim graph

**Objective:** Convert the transcript and repository into a canonical semantic model.

Build a glossary with preferred symbols and aliases; classify each statement as standard mathematics, transcript mapping, repository observation, software target, or GU hypothesis; create a concept graph linking terms to source spans, repository paths, equations, tests, and visual demonstrations; define the object/relation/transformation/claim/evidence ontology.

The key output is not another narrative report. It is a machine-readable registry that can generate reports, API examples, diagrams, speaker notes, and task prompts.

**Gate 1:** Every equation and major term in the current transcript inventory has an owner, a normalized notation, a source span, an evidence class, and either a test or an explicit unresolved status.

### Phase 2 — Deterministic mathematical kernel

**Objective:** Implement the reusable mathematical substrate before higher-level intelligence.

Sequence implementation as follows:

| Increment | Scope | Required evidence |
|---|---|---|
| K0 | Canonical AST, IDs, serialization, source spans | Hash stability and tamper tests |
| K1 | Typed manifolds, vectors, covectors, tensors, variance, contractions | Rejection tests for invalid dimensions and index pairings |
| K2 | Metrics, inverse metrics, trace, raising/lowering, volume/orientation | Analytic fixtures including Euclidean and Minkowski metrics |
| K3 | Connections, Levi–Civita derivation, torsion, contortion | Metric compatibility and torsion-free fixtures |
| K4 | Riemann, Ricci, scalar, Einstein tensor, Bianchi checks | Flat and non-flat analytic fixtures with residuals |
| K5 | Differential forms, wedge, exterior derivative, Hodge star | Degree and `d²=0` fixtures |
| K6 | Gauge connection, curvature 2-form, covariant derivative, `D²`, `DF` | Abelian and non-abelian fixture suite |
| K7 | Spinor/Dirac symbolic layer and Clifford obligations | Symbolic contract tests; no unsupported physical claims |
| K8 | E8 roots/Weyl reflections, projective/Fubini–Study, Hopf metadata | Algebraic invariance and projection fixtures |

**Gate 2:** The kernel can reproduce all registered fixture identities, return residuals and assumptions, serialize deterministically, and distinguish `verified`, `fail`, and `unverifiable`.

### Phase 3 — Verification, provenance, and evidence ledger

**Objective:** Make every operation auditable and every claim bounded.

Implement the operation registry, invariant registry, evidence schema, replay engine, provenance links, limitation fields, and claim evaluator. Store immutable mathematical cores separately from mutable display envelopes. Add evidence graph queries: “which source supports this result?”, “which transformations produced it?”, “which assumptions were active?”, and “what would invalidate it?”

**Gate 3:** A result can be deleted from a display database without destroying its canonical identity or replay record. A one-character input change must produce a different canonical hash. Missing GU definitions must produce `unverifiable`.

### Phase 4 — Runtime integration

**Objective:** Connect verified geometry to Logos, Monad, retrieval, routing, and transformation planning.

Logos should translate user language into typed candidate objects and operations. Monad should apply deterministic state transitions. Retrieval should return geometry plus provenance, not only a similarity score. Colony and consensus should coordinate candidate states and evidence records, not vote on unconstrained prose.

Introduce a runtime request envelope containing user intent, candidate objects, allowed operations, evidence requirements, budget, and safety policy. The runtime must be able to explain why a transformation was selected and which invariants survived.

**Gate 4:** A complete end-to-end request can move from natural language to canonical objects, verified transformations, evidence records, and an explanation, with no opaque mutation of the trusted core.

### Phase 5 — Demonstration and embodiment suite

**Objective:** Make the abstract system understandable and evaluate usability.

Organize the attached explorers into a coherent demonstration portfolio rather than treating them as unrelated projects. Each demonstration must map a visible behavior to a canonical object and an invariant.

| Demonstration family | Purpose |
|---|---|
| Geometry explorer | Show metrics, curvature, projections, fibers, and coordinate changes |
| E8/Weyl explorer | Show roots, reflections, adjacency, and preserved structure |
| Phase/projective explorer | Show amplitude-phase states, Bloch/Hopf projections, and Fubini–Study distance |
| Tensor laboratory | Let users inspect a metric, connection, curvature chain, and residuals |
| Runtime dashboard | Show ingestion, transformation, evidence, claim status, and provenance |
| Game/simulation surface | Teach state transitions, attractors, constraints, and exploration through interaction |
| Audio/hardware surface | Translate selected invariants into sonification or sensor/actuator behavior |

**Gate 5:** At least three end-to-end journeys are usable by a technically literate outsider without reading the entire repository: a tensor-calculus journey, a geometric navigation journey, and a provenance/claim-audit journey.

### Phase 6 — Developer platform and external APIs

**Objective:** Make the meaning layer consumable by clients and future services.

Treat the OpenAPI specification as a versioned product. Generate Python, TypeScript, and Rust clients; publish examples; define compatibility rules; add idempotency keys, pagination where needed, error envelopes, evidence IDs, and webhook events. Expose local CLI and MCP adapters using the same contracts.

API releases should be gated by schema compatibility, fixture parity, and replay parity between local and service implementations. Physical GU hypothesis endpoints must be explicitly marked as experimental and must return evidence status.

**Gate 6:** A new client can register a manifold, define a metric, compute curvature, retrieve evidence, and evaluate a claim using generated code and documented fixtures.

### Phase 7 — Program automation through Manus API

**Objective:** Turn the roadmap into a repeatable operating loop rather than a series of ad hoc prompts.

Use Manus API v2 for orchestration. Create or reuse a durable Manus Project containing the program charter, ontology rules, evidence policy, writing style, and repository workflow. Use task creation for independent work packages and follow-up messages for multi-turn refinement. Use structured output schemas for machine-readable research findings, implementation plans, test reports, and review decisions. Use file upload/reference for source bundles. Use webhooks for production result delivery and idempotent processing; use polling only for prototypes.

Recommended automation lanes:

| Lane | Trigger | Agent output | Human gate |
|---|---|---|---|
| Research intake | New source, transcript, or paper | Normalized claims, equations, citations, uncertainty | Approve source classification |
| Kernel implementation | Approved issue with acceptance criteria | Code, tests, fixture results, API impact | Review mathematical and software diff |
| Evidence audit | New claim or changed equation | Claim matrix, missing evidence, contradiction report | Accept, revise, or reject claim |
| Demonstration build | Kernel capability reaches gate | Visual prototype, script, mapping to invariants | Usability and correctness review |
| Release preparation | Milestone closes | Changelog, OpenAPI diff, SDK examples, test report | Release decision |
| Program review | Weekly or milestone schedule | Status dashboard, risks, blocked decisions, next portfolio | Reprioritize workstreams |

Manus API should orchestrate tasks and artifacts; it must not become the source of truth for mathematical state. The repository, canonical evidence ledger, and versioned project files remain authoritative.

**Gate 7:** A repeatable automation run can take a bounded work package from issue to research/code artifact, tests, evidence record, review packet, and status update without manual prompt reconstruction.

### Phase 8 — Scientific and systems validation

**Objective:** Prevent internal coherence from being mistaken for physical validation.

Create an independent review cadence with mathematical reviewers, software reviewers, and domain reviewers. Benchmark symbolic correctness, numerical stability, performance, storage growth, and explainability. Maintain a falsification register for claims that could be disproved by counterexample, missing assumptions, or literature conflict.

GU-specific claims should be promoted only when they have: complete notation; defined spaces, bundles, groups, actions, and boundary conditions; derivation or proof; reproducible numerical/symbolic fixtures; comparison to established theory; and a stated empirical pathway.

**Gate 8:** The project can publish a claim matrix that clearly distinguishes what is proven, tested, observed, hypothesized, or unknown.

## Manus API operating strategy

Use the API as a **program control plane** with four durable objects:

| Object | Function |
|---|---|
| Project | Durable instructions, persona, evidence policy, repository conventions, and shared files |
| Task | Bounded work package with inputs, acceptance criteria, and output schema |
| File | Versioned source bundle, report, fixture, or review artifact |
| Webhook/event | Result delivery, state transition, and automation trigger |

Each task should carry a standard envelope:

```json
{
  "program": "Sovereign Engine",
  "workstream": "WS-C",
  "objective": "Implement contracted Bianchi invariant",
  "inputs": ["source IDs", "repository paths", "prior evidence IDs"],
  "constraints": ["do not infer missing GU physics", "preserve API compatibility"],
  "acceptance": ["fixture passes", "evidence record emitted", "docs updated"],
  "output_schema": "sov.work_result.v1",
  "human_gate": "mathematical_review"
}
```

The standard structured result should include `status`, `summary`, `changed_files`, `tests`, `evidence_ids`, `risks`, `open_decisions`, and `recommended_next_tasks`. This allows the program dashboard to aggregate work without parsing prose.

## Portfolio prioritization

Prioritize work using a four-factor score:

\[
P = 0.35E + 0.30D + 0.20R + 0.15U
\]

where `E` is evidence value, `D` is dependency leverage, `R` is risk reduction, and `U` is user-facing demonstrability. Each factor is scored from 0 to 5 and recorded with rationale. This is a planning heuristic, not a scientific measure.

High-priority items are those that unlock many downstream workstreams, reduce ambiguity, and produce a visible demonstration. Examples include canonical tensor types, evidence records, non-flat curvature fixtures, OpenAPI compatibility, and the claim registry. Low-priority items include broad speculative integrations that do not yet have a stable semantic contract.

## Milestone portfolio

| Milestone | Target state | Required deliverables |
|---|---|---|
| M0: Coherent program | One roadmap and evidence taxonomy | Program charter, registry, baseline, backlog |
| M1: Meaning kernel | Concepts and equations are canonical | Ontology, glossary, claim graph, equation registry |
| M2: Verified geometry | Core tensor operations are reproducible | Kernel, fixtures, invariant registry, replay |
| M3: Evidence runtime | Claims and transformations are auditable | Ledger, claim evaluator, Logos/Monad adapters |
| M4: Demonstration system | Outsiders can understand and test it | Tensor lab, geometry explorer, provenance dashboard |
| M5: Developer platform | External clients can integrate | OpenAPI, SDKs, CLI, MCP, webhooks, examples |
| M6: Automated program | Work packages run through repeatable orchestration | Manus Project, structured task flows, event handlers |
| M7: Scientific review | Claims have explicit validation boundaries | Review packets, benchmark suite, falsification register |

## Definition of done for any substantial feature

A feature is complete only when its implementation, tests, documentation, evidence, and demonstration agree. The minimum packet contains:

1. A canonical object or operation definition.
2. Source references and claim classification.
3. Input/output schemas and version impact.
4. Deterministic unit and fixture tests.
5. Invariant results with tolerances and assumptions.
6. Replayable evidence record and stable hash.
7. API/CLI/runtime integration if applicable.
8. Plain-language explanation and visualization path.
9. Known limitations and unresolved questions.
10. A next-step recommendation that is linked to a program milestone.

## Risk register and controls

| Risk | Consequence | Control |
|---|---|---|
| Transcript ambiguity | Incorrect equations or symbols become code | Source spans, notation registry, unresolved status, expert review |
| Internal coherence mistaken for physics | Overclaiming and loss of credibility | Claim classes, independent review, falsification register |
| Prototype fragmentation | Repeated work and incompatible interfaces | Workstream ownership, canonical ontology, API-first contracts |
| LLM drift | Silent changes to definitions or evidence | Deterministic core, structured outputs, replay, human gates |
| Scope expansion | No milestone closure | Portfolio scoring, phase gates, explicit non-goals |
| Automation failure | Lost results or duplicate work | Webhook signatures, idempotency, retries, durable artifacts |
| Performance bottlenecks | Kernel unusable at runtime scale | Fixture benchmarks, profiling gates, bounded representations |
| Visualization misleads | Users confuse analogy with proof | Captions, claim status, source links, uncertainty styling |

## Immediate strategic decisions

The roadmap assumes the following decisions, which should be confirmed at the next program review:

1. Sovereign Engine’s near-term product is the **verifiable meaning kernel and demonstration platform**, not a completed physical unification theory.
2. The tensor/geometry kernel and evidence ledger are the first production-quality foundations.
3. GU-specific physics is maintained as versioned hypotheses with explicit missing obligations.
4. The attached explorers become a curated demonstration suite with shared contracts.
5. Manus API is used as an orchestration layer for research, implementation, review, and release packets—not as the authority for canonical mathematical state.
6. Every milestone closes with an evidence packet and a public-facing explanation, not only code.

## First 30-day program start

**Week 1:** Approve the charter, create workstream ownership, freeze the baseline, and finalize the ontology/evidence taxonomy.  
**Week 2:** Finish K0–K2 kernel contracts, publish the equation registry, and convert the existing OpenAPI into the first compatibility baseline.  
**Week 3:** Implement K3–K5 fixtures and evidence replay; select three demonstration journeys and map each to canonical operations.  
**Week 4:** Create the Manus Project orchestration template, structured work-result schema, review gates, milestone dashboard, and M2 release packet.

The program should then operate in milestone-sized increments, with autonomous work packages running in parallel inside the approved architecture rather than requiring a new conversational reconstruction for every small step.

## Open risks and unresolved decisions

The roadmap does not resolve the exact GU action, the precise metric on the space of metrics, the claimed 75-dimensional invariant subspace, the representation-theoretic origin of three generations, or the empirical status of cross-domain invariants. Those remain named research programs with explicit obligations. The roadmap’s purpose is to make them investigable without allowing them to destabilize the verified software foundation.
