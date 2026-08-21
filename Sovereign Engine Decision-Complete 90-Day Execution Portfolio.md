# Sovereign Engine Decision-Complete 90-Day Execution Portfolio

**Planning horizon:** 13 weeks  
**Basis:** Approved program roadmap plus research/architecture findings as of 2026-08-16.  
**Portfolio rule:** A work package closes only with output, acceptance evidence, known limitations, a dashboard update, and a decision effect.

## Capacity scenarios

| Scenario | Roles assumed | Capacity | Recommended use |
|---|---|---:|---|
| Lean | 1.0 technical lead, 0.5 math/verification, 0.25 platform, 0.25 program | 2.0 FTE; 26.0 FTE-weeks | Sequence high-leverage core work; defer full API/demo integration. |
| Core | 1.0 kernel, 1.0 verification, 0.5 research, 0.5 platform, 0.25 product, 0.25 program | 3.5 FTE; 45.5 FTE-weeks | Recommended baseline; reaches green-core alpha, evidence path, and one audited demo. |
| Acceleration | 1.0 kernel, 1.0 verification, 1.0 research, 1.0 platform, 0.5 product, 0.5 program | 5.0 FTE; 65.0 FTE-weeks | Adds API clients and three demo journeys only if core gates remain green. |

These are capacity assumptions, not commitments or cost estimates. They exclude external-review waiting time and production infrastructure operations.

## Release sequence

| Release | Weeks | Objective | Non-goals | Gate |
|---|---|---|---|---|
| R0: Evidence baseline | 1–2 | Freeze sources, accept core boundaries, finish registries and policies | New runtime features, distributed systems, GU promotion | M0 / Gate 1 |
| R1: Geometry/evidence alpha | 3–6 | K0–K3 typed core, canonical evidence records, standard fixtures | Full E8/GU operators, servers, graph DB | M1 / partial Gate 2 |
| R2: Curvature/replay beta | 7–9 | K4–K6, replay/tamper, reference parity, OpenAPI alignment | Production signing, P2P/consensus, autonomous agents | M2 / Gates 2–3 |
| R3: Audited vertical slice | 10–13 | One end-to-end intent→operation→evidence→explanation demo; SDK/contract draft; release packet | Physical validation, production cluster, broad public launch | M3 / pilot Gates 4–6 |

## Work packages

| ID | Window | Owner role | Dependencies | Deliverable and acceptance evidence | Risk / non-goal |
|---|---|---|---|---|---|
| WP-01 | W1 | Program architect | Source manifest | Research register, governance policy, ADR index, connector matrix, dashboard input schema | Does not enable new integrations or schedules |
| WP-02 | W1–2 | Scientific review lead | Transcript, deep dive, standard sources | Equation registry, notation policy, claim graph skeleton, GU falsification register; every priority item typed or `unverifiable` | Does not derive missing GU equations |
| WP-03 | W1–2 | Kernel architect | Repository evidence matrix | ADRs 001/002/003/006 accepted or explicitly pending; core extraction plan | Does not split repository yet |
| WP-04 | W2–3 | Reliability lead | ADR-003 | Canonical serialization/hash reference spec, test vectors, tamper suite, evidence schema v1 | No database/KMS/graph dependency in pure core |
| WP-05 | W3–4 | Mathematical software lead | Object model, notation policy | K1/K2 typed manifold/tensor/metric operations; invalid index/variance/unit tests; Euclidean/Minkowski fixtures | No physical model interpretation |
| WP-06 | W4–5 | Mathematical software lead | K1/K2 | K3 connection, Levi-Civita, torsion/contortion operations with convention IDs; compatibility/torsion fixtures | GU augmented connection remains `unverifiable` |
| WP-07 | W5–6 | Verification lead | K3, evidence schema | Operation/predicate registry and evidence/replay engine; unknown operation/missing assumption failure cases | No opaque callback/plugin execution |
| WP-08 | W6–7 | Mathematical software lead | K3, registry | K4 curvature/Ricci/scalar/Einstein chain and Bianchi residual fixtures; flat plus one non-flat standard case | No unbenchmarkable performance claims |
| WP-09 | W7–8 | Mathematical software lead | K4, registry | K5/K6 forms, gauge curvature, Bianchi fixtures; explicit representation/convention checks | No GU action evaluator |
| WP-10 | W7–9 | Formal methods lead | Equation registry, core IDs | Lean-anchor audit: named stable theorems, build/revision record, bridge status; one selected formal anchor | Does not certify full runtime |
| WP-11 | W8–9 | API/platform lead | Evidence schemas, registry | OpenAPI semantic diff, contract tests, generated-client smoke plan, error/status envelopes | No public API commitment before core semantics stable |
| WP-12 | W9–10 | Reliability/provenance lead | Core fixtures, OpenAPI | Differential-test report against approved reference adapters; benchmark harness plus baseline metadata | No performance headline without raw results |
| WP-13 | W10–11 | Product/visualization lead | Core and evidence records | Tensor audit journey demonstrating source→object→operation→evidence→limitation | No independent demo truth model |
| WP-14 | W11–12 | Release/reliability lead | WP-04–13 | Release evidence bundle, SBOM/dependency policy report, CI split plan, audit-only signing recommendation | No production signing enforcement |
| WP-15 | W12–13 | Program architect | All prior packages | 90-day review, dashboard update, ADR review, next-quarter portfolio with only irreducible decision requests | No retroactive promotion of hypotheses |

## Acceptance gates

| Gate | Must be true | Automatic evidence | Human review trigger |
|---|---|---|---|
| G0 | Scope, sources, owners, policies, and adapters are known | Source/connector manifests and register | New external scope or data class |
| G1 | Priority equations/claims are typed and attributed | Registry coverage report and unresolved obligations | Physical-claim promotion |
| G2 | Core fixture operations are deterministic and fail closed | Clean install, fixed fixtures, invalid/tamper results | Canonical format/API break |
| G3 | Evidence can replay independently of UI/store | Replay report and one-character mutation failure | Persistence/signature trust change |
| G4 | Runtime cannot bypass core and explanations retain status | End-to-end trace fixture | New autonomous external effect |
| G5 | Demo teaches without overclaiming | Outsider task/audit result and source links | Public publication |
| G6 | API/SDK and local core have contract/replay parity | OpenAPI diff, generated client, contract suite | Breaking compatibility |
| G7 | Release evidence bundle is complete | Clean install, SBOM, known limitations, checksums | Release/publish decision |

## Critical dependency chain

`WP-01/02/03 → WP-04 → WP-05 → WP-06 → WP-07 → WP-08/09 → WP-10/11/12 → WP-13 → WP-14 → WP-15`

Parallel work is allowed only where it does not establish a new cross-workstream contract. Product demo design may begin during WP-08 but cannot compute authoritative values until the relevant core operations and fixtures have passed.

## Default decisions that remove routine questions

1. Use Rust for core types/verifier, Python for exploration/reference fixtures, and Lean for selected proof anchors.
2. Use content-addressed immutable cores and non-hashed display envelopes.
3. Prefer filesystem/SQLite-compatible persistence before managed graph/database services.
4. Return only `verified`, `fail`, or `unverifiable`; omit a fourth “soft pass” category.
5. Defer P2P, consensus, blockchain, private KMS, and production cluster work until a specific verified use case, threat model, and core gate exist.
6. Treat any GU-specific physical assertion as a versioned hypothesis with an explicit falsifier and promotion requirement.
7. Use OpenAPI as the single semantic contract; derive SDK/CLI/MCP behavior from it rather than creating parallel semantics.
8. Do not create a custom Sovereign skill until repeated use shows a stable input/output workflow.

## Irreducible decision backlog

Only these decisions should require human input during this horizon.

| ID | Decision | Why policy cannot decide it | Latest safe date | Default if no decision |
|---|---|---|---|---|
| D-01 | Capacity scenario | Determines throughput, sequencing, and staffing commitment | Week 1 | Lean scenario |
| D-02 | Scope of external/public release | Controls legal/reputational/publication risk | Before WP-13/14 | Internal research release only |
| D-03 | Expert reviewer pool and participation terms | Requires human relationships and accountability | Week 4 | Keep claims at internal `unverifiable` / research status |
| D-04 | Canonical serialization breaking migration, if needed | Affects existing consumer/evidence compatibility | Before first published core tag | Preserve legacy readers and defer change |
| D-05 | SEO track geography and data provider | Cannot responsibly invent country/market/data scope | Only when content work activates | No keyword-volume report |

## First coordinated execution wave

The next execution wave is **WP-02, WP-03, and WP-04**, which can be run with bounded shared inputs. It does not need new feature ideation. Its deliverable is the accepted semantic/evidence kernel contract that makes later implementations testable and non-contradictory.
