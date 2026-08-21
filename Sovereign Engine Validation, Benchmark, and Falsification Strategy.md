# Sovereign Engine Validation, Benchmark, and Falsification Strategy

## Correctness is layered

A valid software result, a valid mathematical mapping, and a valid physical claim are different propositions. They are tested with different evidence and must never be merged by dashboards or marketing language.

| Layer | Question | Passing evidence | Failure / unresolved condition |
|---|---|---|---|
| Schema and type | Is the object well-formed? | Typed AST and validation report | Invalid schema/index/domain/unit |
| Mathematical operation | Does a registered operation satisfy its stated identity on declared assumptions? | Fixture, residual/predicate, convention profile | Predicate fails or assumption absent |
| Implementation parity | Do independent implementations agree within declared bounds? | Differential fixture against reference backend | Divergence with preserved input/output evidence |
| Formal anchor | Has a selected statement been checked in Lean with explicit bridge scope? | Theorem ID, Lean revision/build record, bridge analysis | Missing theorem/bridge or build failure |
| System integration | Does runtime plan invoke core deterministically and preserve evidence? | Trace fixture from plan to evidence | Opaque mutation, unknown operation, nondeterministic output |
| Performance | Does a named workload meet a measured target? | Harness, hardware/toolchain, payloads, raw data, percentile table | Missing harness or target miss |
| GU hypothesis | Does a source-complete theory proposal survive derivation/probe/review? | Exact definition, derivation, reproduction, falsifier analysis | Missing formulae/assumptions; contrary derivation/data |

## Test pyramid and required artifacts

| Test type | Minimal artifacts | Required initial examples |
|---|---|---|
| Static | Toolchain lock, formatter/type/lint reports | Rust/Python import/type checks; schema validation |
| Unit | Canonical input, expected output, convention ID | Metric symmetry, inverse metric, index raise/lower, `d^2=0` |
| Property/metamorphic | Seed, generator version, shrink output | Permutation-stable serialization, `d^2=0`, contraction compatibility |
| Golden | Input, exact expected canonical output/hash, assumptions | Minkowski flat metric, standard sphere/Hopf data, simple gauge connection |
| Differential | Internal/reference versions and divergence policy | SymPy/EinsteinPy comparison on explicitly supported standard cases |
| Formal | Theorem name, revision, assumption map | One scalar/tensor identity with an executable bridge analysis |
| API | OpenAPI version, generated client, consumer/provider results | Expected `verified`, `fail`, `unverifiable` envelopes |
| Tamper/replay | Original record, one-character mutation, verifier result | Hash mismatch, unknown operation, altered assumption, missing source |
| Integration | Plan trace, core record, explanation link | Runtime plan cannot bypass registered operation/predicate |
| Benchmark | Hardware/OS/toolchain, payloads, p50/p95/p99, RSS, raw logs | Canonicalization, hash, operation, replay baseline |

## Falsification rules

1. A GU-specific hypothesis is not “passed” by a standard geometry fixture; the fixture can only test the standard component.
2. Missing definitions, transformations, actions, representations, or observables require `unverifiable` and an obligation record.
3. A hypothesis must name a contrary result. “More evidence needed” is not a falsifier.
4. Numerical agreement is bounded by a declared precision, coordinate chart, signature, convention, and reference implementation.
5. Benchmarks require workloads representative of the named claim; O(1) algebraic step count cannot be generalized into O(1) end-to-end navigation without cost accounting.

## Release-evidence bundle

Every green-core release must package source revision, clean-install log, lock/toolchain record, test report, fixture manifest, API compatibility report, SBOM/dependency policy report, evidence schema version, known-limitations record, checksum, and rollback instructions. Signing is audit-only after the bundle is reproducible; it is not a substitute for the bundle.
