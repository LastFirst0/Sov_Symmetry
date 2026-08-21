# Sovereign Engine Program Control Center

**Baseline:** repository commit `167802301a1b6f658b44a80bb7b3f62b839f205a`  
**Roadmap:** `SOVEREIGN_ENGINE_PROGRAM_ROADMAP.md`  
**Operating principle:** no substantial work proceeds without an owner, acceptance criteria, evidence target, and milestone destination.

## Current north star

Sovereign Engine is being developed as a **geometry-native, provenance-aware, verifiable meaning system**. The near-term product is the reproducible meaning kernel and demonstration platform. Geometric Unity-specific physics remains a versioned hypothesis program and is not treated as established fact.

## Workstream registry

| ID | Workstream | Current status | Immediate outcome | Primary dependencies |
|---|---|---|---|---|
| WS-A | Meaning and ontology | Registry/policy foundation complete | Implement source-span graph and coverage report against repository paths | Transcript, analysis, dossier, canonical registry |
| WS-B | Tensor and geometry kernel | Target boundary and increments defined | Implement K0–K3 inside green-core package boundary | Blueprint, simulation, repository geometry, ADRs |
| WS-C | Verification and evidence | Evidence architecture and validation policy complete | Implement canonicalization/hash vectors, registry, and replay core | WS-A, WS-B, ADR-003 |
| WS-D | Runtime and intelligence | Architecture intent documented | Runtime request envelope and adapters | WS-B, WS-C |
| WS-E | Embodiment and UX | Prototype surface inventoried | Three coherent demonstration journeys | WS-B, WS-C, attached explorers |
| WS-F | API and developer platform | OpenAPI baseline and code-generation policy complete | Build generated-client contract suite after core schemas stabilize | WS-B, WS-C |
| WS-G | Program automation | Connector matrix and orchestration contract complete | Implement bounded task/result envelopes once core work packages are active | All workstreams, shared files |
| WS-H | Scientific validation | Hypothesis/falsification and external-source records complete | Audit formal anchors, reference parity, and benchmark evidence | WS-A, WS-B, external references |

## Artifact status

| Artifact | Status | Role | Next decision |
|---|---|---|---|
| `SOVEREIGN_ENGINE_MEANING_LAYER.md` | Baseline | Conceptual identity and full-story reconstruction | Promote key concepts into registry |
| `GU_TENSOR_CALCULUS_DEEP_DIVE.md` | Baseline | Equation and variable significance | Convert equations into executable fixture records |
| `SOVEREIGN_ENGINE_TENSOR_BLUEPRINT_AND_API.md` | Baseline | Implementation architecture and contracts | Align with repository module boundaries |
| `sovereign_engine_api.openapi.yaml` | Validated baseline | External client contract | Add generated SDK and compatibility CI |
| `simulate_tensor_state.py` | Verified fixture | Controlled tensor-state pipeline | Add non-flat and failure fixtures |
| `tensor_simulation_report.md` | Verified evidence | Simulation interpretation | Link results to invariant registry |
| `GU_MEANING_LAYER_SLIDES.md` | Baseline | Deck content source | Keep synchronized with roadmap milestones |
| `gu_meaning_layer_deck/` | Presented | Research communication surface | Use as program review template |
| `PHASE_0_BASELINE.md` | Frozen | Repository and artifact inventory | Refresh only at milestone boundaries |
| `geometric_unity.txt` | Source | Primary transcript | Maintain source-span identifiers |
| `geometric_unity_analysis.txt` | Source | Initial supplied interpretation | Reconcile with canonical claim classes |
| Attached explorers | Inventory complete | Embodiment and visualization candidates | Select three demonstration journeys |
| `REPOSITORY_EVIDENCE_MATRIX.md` | Completed | Observed repository/CI/security credibility findings and green-core proposal | Accept ADR-001/003/006 and extract pure core |
| `CANONICAL_EQUATION_REGISTRY.json` | Completed | Machine-readable priority equation object model | Extend source spans and concept graph |
| `GU_HYPOTHESIS_FALSIFICATION_REGISTER.md` | Completed | GU proposal boundaries, missing prerequisites, and falsifiers | Maintain through research and review |
| `TARGET_ARCHITECTURE_AND_ADR_PROGRAM.md` | Completed | Target layer boundaries and ADR program | Accept required ADRs on schedule |
| `SOVEREIGN_ENGINE_DECISION_COMPLETE_90_DAY_PORTFOLIO.md` | Completed | Sequenced work packages, capacity scenarios, gates, and decision backlog | Run WP-02/03/04 foundation wave |
| `VALIDATION_AND_FALSIFICATION_STRATEGY.md` | Completed | Test hierarchy, release evidence, and scientific boundary policy | Implement fixture manifests and CI split |
| `ECOSYSTEM_BUILD_BUY_ADAPT_MATRIX.md` | Completed | Dependency and adoption decisions | Review candidates before integrating |

## Canonical claim classes

| Class | Meaning | Allowed language |
|---|---|---|
| `standard` | Established mathematical or physical definition | “is defined as,” “satisfies,” “theorem/identity” |
| `transcript_mapping` | Normalized interpretation of oral or imperfect transcription | “likely refers to,” “maps to,” “in this passage” |
| `repository_observation` | Behavior or design found in the repository | “the repository contains,” “the code declares” |
| `software_contract` | Intended or tested implementation behavior | “the API must,” “the verifier returns” |
| `gu_hypothesis` | Geometric Unity-specific physical or representational proposal | “the transcript proposes,” “requires validation” |

## First coordinated execution wave

| Work item | Workstream | Acceptance criteria | Evidence target | Milestone |
|---|---|---|---|---|
| WA-001: Meaning registry v1 | WS-A | Every priority term has preferred notation, aliases, source spans, class, owner, and status | JSON registry plus coverage report | M1 |
| WB-001: Tensor fixture suite | WS-B | Flat, curved, torsion, gauge, and invalid fixtures with residuals | Machine-readable fixture results | M2 |
| WC-001: Invariant registry | WS-C | IDs for dimension, symmetry, inverse, torsion, curvature, Bianchi, replay, and claim status | Registry plus replay tests | M3 |
| WD-001: Runtime request envelope | WS-D | Natural-language intent can be represented with candidate objects, allowed operations, evidence requirements, and budget | Schema and sample trace | M3 |
| WE-001: Three demonstrations | WS-E | Tensor lab, geometry explorer, and provenance audit map to canonical operations | Journey scripts and screenshots/visuals | M4 |
| WF-001: Generated API clients | WS-F | Python, TypeScript, and Rust clients compile against OpenAPI baseline | CI compatibility report | M5 |
| WG-001: Manus orchestration template | WS-G | Bounded task produces structured result, artifact references, tests, and human-gate decision | Task template, output schema, runbook | M6 |
| WH-001: Claim/limitation register | WS-H | Every GU-specific claim has required-obligation checklist and evidence status | Review register | M7 |

## Decision log

| Decision | Current position | Rationale | Revisit trigger |
|---|---|---|---|
| Product identity | Meaning infrastructure platform | Unifies repository and prototypes without overclaiming physics | Evidence shows a better bounded product |
| Trusted-core boundary | Deterministic tensor/geometry/provenance kernel | Protects correctness from model drift | Kernel becomes insufficient for demonstrated use cases |
| GU physics status | Hypothesis modules | Transcript does not provide complete derivations or empirical bridge | Complete notation, derivation, fixtures, and comparison exist |
| Manus API role | Program control plane, not mathematical source of truth | Enables scale without outsourcing canonical state | Ledger/repository architecture changes |
| Demonstration strategy | Three outsider-readable journeys first | Converts abstraction into testable understanding | Usability review identifies better sequence |
| API strategy | OpenAPI-first, versioned, evidence-bearing | Enables client generation and contract tests | Transport or deployment constraints require revision |

## Milestone gate checklist

### Gate 0 — Baseline

- [x] Roadmap approved and saved.
- [x] Repository commit and artifact inventory recorded.
- [x] Workstreams and owner roles defined.
- [x] Existing artifacts assigned status and next decision.
- [x] Canonical registry, research register, and decision-complete portfolio written to project evidence workspace.

### Gate 1 — Meaning layer

- [x] Priority equation registry and notation policy established from transcript analysis.
- [x] GU hypothesis register classifies missing definitions and falsification obligations.
- [ ] Concept graph links every term/equation to repository modules, tests, and demonstrations.
- [ ] Coverage report identifies unresolved or unowned terms across full repository inventory.

### Gate 2 — Mathematical kernel

- [x] Flat Minkowski fixture executed with 11 checks and 0 failures.
- [ ] Non-flat curvature fixture executed.
- [ ] Failure and invalid-index fixtures executed.
- [ ] Deterministic serialization and hash replay implemented.

## Program review cadence

At each program review, produce one packet containing: milestone status, changed artifacts, test/evidence summary, unresolved decisions, risk changes, demonstration state, API compatibility, and the next coordinated work wave. Individual tasks should be grouped into these packets rather than delivered as unrelated conversational fragments.

## Immediate next coordinated wave

The next wave is already decision-bounded as **WP-02, WP-03, and WP-04** in `SOVEREIGN_ENGINE_DECISION_COMPLETE_90_DAY_PORTFOLIO.md`. It completes source-span/concept graph coverage, accepts the green-core/evidence/claim-policy ADRs, and defines canonicalization/hash vectors and tamper fixtures. No unrelated runtime, P2P, GU-action, or demonstration feature should start before this foundation packet is accepted.

## Theory-neutral archival-context notice

Any Geometric Unity or other theory-specific material referenced here is retained as historical research provenance, not as the governing ontology of the active kernel. The current kernel accepts framework identifiers only as provenance labels and evaluates only admitted, bounded structural claims under `THEORY_AGNOSTIC_UNIVERSAL_KERNEL_REBASELINE_v0.1.md` and `UNIVERSAL_FRAMEWORK_ADAPTER_CONTRACT_v0.1.md`.
