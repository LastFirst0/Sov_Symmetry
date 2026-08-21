# Sovereign Engine Repository Evidence Matrix

**Baseline repository revision:** `167802301a1b6f658b44a80bb7b3f62b839f205a`  
**Method:** Static repository and GitHub evidence inspection; no project application code was executed.  
**Scope:** Observed facts are distinct from recommendations and hypotheses.

## Observed repository facts

| ID | Observed fact | Source | Implication | Confidence | Next verification |
|---|---|---|---|---|---|
| R1-01 | The repository is a heterogeneous workspace containing Rust crates, Python subsystems, Lean files, database/provenance assets, dashboards, apps, scripts, data, and generated artifacts. | `PHASE_0_BASELINE.md`; repository topology | A single broad health signal cannot credibly represent all subsystems. | High | Produce module ownership and extraction map. |
| R1-02 | The current CI workflow runs a one-click system launcher, a Lean comparator script, and `cargo test --workspace` in one job. | `.github/workflows/ci.yml:9-49` | CI couples unrelated Python, Lean, Rust, server, and workbench surfaces; failures cannot isolate a kernel boundary. | High | Split into independent required checks with artifacted outcomes. |
| R1-03 | The launcher’s `--test` mode imports/runs workbench, Ollama server, and MCP server tests before reporting blanket success. | `start_sovereign_engine.sh:29-37` | The current Python gate is an expansive smoke test, not a minimal core test. | High | Introduce a scoped kernel test command before retaining broad integration smoke tests. |
| R1-04 | Representative GitHub Actions failures from 2026-07-24 fail during import of `sov_math/core/unified_geometry.py` because `Any` is not defined. | `ci_failure_evidence.log:584-599` | The latest observed CI failure is a deterministic Python import defect, not evidence that all claimed mathematical subsystems fail. | High | Repair only after a narrow package/test boundary is selected; add import/type gate. |
| R1-05 | The failure occurs through `scripts/sovereign_workbench.py` → `sov_heart.colony` → `sov_math.core.unified_geometry`, showing broad top-level import coupling. | `ci_failure_evidence.log:585-598`; `scripts/sovereign_workbench.py` overview | The workbench test conceals subsystem-specific state behind a broad import graph. | High | Make optional/exploratory components lazy adapters or isolate their tests. |
| R1-06 | `crates/sov-core` exists as a small Rust package with only `serde` and `serde_json` dependencies; its current source inventory contains `Vector`, `MetricState`, and `CensusResult`. | `crates/sov-core/Cargo.toml`; `sov_core_inventory.md` | It is a plausible seed, but not yet the full typed geometry/evidence kernel specified by the roadmap. | High | Audit public semantics and add fixtures before designating it green core. |
| R1-07 | A database adapter already implements sorted-key JSON normalization, SHA3-256 hashing, and a simple deterministic-hash test. | `database/adapters/python/register_artifact.py:24-54`; `database/tests/test_canonical_hash.py` overview | A useful evidence-kernel slice exists, but is entangled with network/database/embedding side effects. | High | Extract pure canonicalization/hash module and expand test vectors. |
| R1-08 | The adapter uses development-default Postgres/Neo4j credentials and network-service defaults, and combines canonicalization with KMS, embedding, database, graph, and signing effects. | `database/adapters/python/register_artifact.py:16-22,56-135` | The adapter is not a trusted-core implementation; its deterministic core must be separated from mutable I/O adapters. | High | ADR for pure core/adapter split and secret/config handling. |
| R1-09 | The CI workflow installs actions/toolchains through floating selectors (`latest`, `stable`) and installs Lean by piping a remote script into `sh`. | `.github/workflows/ci.yml:18-34` | Supply-chain and reproducibility evidence is weak for a future release-grade verifier pipeline. | High | Pin versions/digests, establish lock/toolchain evidence, and use a reviewed install path. |
| R1-10 | The architecture document asserts broad geometry-native runtime claims and lists paths that do not align cleanly with the observed current repository layout. | `ARCHITECTURE.md:1-105`; `PROJECT_STATUS_AND_ROADMAP.md` overview | Documentation drift and claim-to-code mismatch must be tracked explicitly. | Medium-high | Run a doc-to-path and claim-to-evidence audit. |
| R1-11 | Documentation claims such as “100% scale-invariant,” “O(1)” replacement, and “eliminating vanishing/exploding gradients” are present in architecture narrative without linked benchmark/evidence records in the inspected source. | `ARCHITECTURE.md:24-60` | These are repository assertions/hypotheses, not verified performance/scientific facts in the program record. | High | Assign claim classes and benchmark/formal obligations. |

## Credibility gap

The principal credibility gap is not lack of ambition or artifact volume. It is the absence of a **narrow, reproducible, evidence-backed release unit** separating deterministic geometry/provenance behavior from broad runtime, network, UI, model, game, and experimental surfaces. The available CI evidence currently fails before such a boundary can be assessed. Repository documentation also carries several performance and physical/semantic claims without a discoverable bridge to fixtures, formal references, or measured benchmarks.

## Proposed green-core boundary

### Candidate v0.1 release unit: `sov-evidence-geometry-core`

The candidate release unit should be a small, independently installable library—not a server, swarm, dashboard, model runtime, or GU physical-theory claim. It should own canonical object identity, typed basic geometry contracts, operation/predicate registration, evidence record serialization, and replayable statuses.

| Retain in v0.1 core | Why |
|---|---|
| Canonical AST and source-span records | Stable identity and traceability |
| Canonical serialization + content hashing | Replay and tamper detection |
| Typed manifold/tensor/metric/form metadata | Foundation for operations and APIs |
| Versioned operation and predicate registry | Fail-closed execution boundary |
| Evidence core record + `verified` / `fail` / `unverifiable` statuses | Auditable result semantics |
| Small standard fixtures | Reproducible correctness claims |

| Explicitly outside v0.1 core | Treatment |
|---|---|
| LLM/Ollama servers, MCP servers, web workbench | Adapter/integration surface |
| Colony, P2P, consensus, swarm, routing | Deferred until a verified use case and threat model |
| Games, pets, biblical apps, hardware/audio experiences | Demonstration adapters |
| Database/Neo4j/KMS/embedding calls | I/O adapters behind pure core interfaces |
| Broad GU physics and generation claims | Versioned hypotheses with obligations |
| GPU/model/checkpoint runtime | Experimental performance layer |

## Extraction map

| Current source | Proposed destination | Treatment | Migration condition |
|---|---|---|---|
| `crates/sov-core/` | `core/rust/` or dedicated `sov-evidence-geometry-core` crate | Retain and redesign around explicit contracts | Public API and fixtures defined |
| `database/adapters/python/register_artifact.py` canonical functions | Pure canonicalization reference module | Extract/rewrite | No network imports or default credentials in pure module |
| `database/specs/canonical_serialization.md` | Core specification | Retain, reconcile with code and test vectors | Canonical byte-policy ADR accepted |
| `database/tests/test_canonical_hash.py` | Core fixture suite | Extend | Add permutations, nested values, tamper, unsupported schema tests |
| `sov_math/core/unified_geometry.py` | Experimental mathematical adapter | Quarantine from core CI until notation/types reviewed | Import/type defects fixed and fixtures specified |
| `sov_heart/*`, `scripts/*`, server/UI paths | Integration/test layer | Split from core gate | Contract tests exist against stable core |
| `lean_verification/*` | Formal-reference layer | Retain selectively | Each proof is linked to a named statement and implementation bridge |

## Immediate corrective sequence

1. Create an ADR accepting or revising the green-core boundary.
2. Establish a pure import/type/test job for the core before broad system diagnostics.
3. Extract deterministic canonicalization and hashing from database/network adapters.
4. Define fixture manifests and a tamper suite before adding broad performance claims.
5. Split CI into format/type, core unit/fixture, formal-reference, integration smoke, and advisory experimental jobs.
6. Create a documentation claim ledger; downgrade unsupported assertions to `repository_observation` or `gu_hypothesis` until evidence exists.

## Limitations

This matrix documents source inspection and a small set of representative GitHub workflow failures. It does not prove that no other passing CI runs, tests, benchmarks, or private artifacts exist. It does not execute code, prove a mathematical result, or establish the physical validity of any GU claim.
