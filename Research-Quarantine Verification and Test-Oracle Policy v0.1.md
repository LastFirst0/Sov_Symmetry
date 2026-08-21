# Research-Quarantine Verification and Test-Oracle Policy v0.1

**Status:** Proposed policy; becomes binding only with ADR-006 acceptance.  
**Scope:** Celestial/narrative mappings, scripture-ingestion semantics, broad E8 resonance mappings, GU physical/representational claims, consensus/PoUW claims, and any performance assertion lacking a named reproducible workload.

## 1. Purpose and non-negotiable boundary

Research quarantine allows the program to preserve, analyze, and challenge high-ambiguity material **without importing it as core semantics, physical truth, or verified product behavior**. A quarantined item can contribute source references, normalized notation, standard sub-problems, experimental adapters, and falsification work. It cannot change a core predicate, determine an evidence status, or be described as established physics.

> A successful standard calculation involving a quarantined expression verifies only the declared standard calculation. It does not verify the broader GU, narrative, performance, or physical interpretation.

## 2. Required claim packet

No quarantined item exists in the system without a `sov.research.quarantine.v0.1` packet. The packet is invalid unless all required fields are present.

| Field | Exact requirement |
|---|---|
| `quarantine_id` | `rq:sha256:` followed by 64 lowercase hexadecimal characters; derived from the canonical packet body excluding `quarantine_id`, lifecycle history, and display fields. |
| `category` | One of `gu_physics`, `gu_representation`, `celestial_narrative`, `semantic_mapping`, `performance`, `consensus_protocol`, or `other_experimental`. |
| `claim_text` | One atomic, falsifiable statement. It must not combine a mathematical identity, software behavior, and physical consequence in one sentence. |
| `claim_level` | Exactly one of `mathematical`, `software`, `physical`, `semantic`, or `performance`. |
| `source_refs` | At least one immutable source reference with authority tier, locator, retrieved date, and content hash where available. |
| `normalized_statement` | Definitions of every symbol, space, representation, action, unit, and convention needed to evaluate the specific claim. Missing items are listed, never inferred. |
| `assumptions` | Explicit finite list of active assumptions; an empty list is allowed only for a purely syntactic/source observation. |
| `falsifier` | A contrary derivation, incompatible theorem, counterexample class, benchmark result, or empirical outcome. “Needs more evidence” is not a falsifier. |
| `oracle_plan` | Ordered list of eligible oracle tiers, exact fixture/dataset references, expected outputs, and disagreement rule. |
| `promotion_target` | One of `remain_quarantined`, `standard_kernel_candidate`, `experimental_adapter`, `documentation_only`, or `retired`. |
| `owner_role` and `review_due` | Accountable role and ISO-8601 review date. |

## 3. Lifecycle and allowed transitions

The research lifecycle is separate from the core result status vocabulary. A packet may carry a local test result of `verified`, `fail`, or `unverifiable`; this does not change the lifecycle state by itself.

| State | Entry criterion | Allowed activity | Exit criterion |
|---|---|---|---|
| `intake` | Source present but no normalized statement | Source hashing, extraction, classification | Required claim packet complete |
| `normalized` | Claim packet complete; all unknowns enumerated | Standard-subclaim isolation, oracle planning | Every symbol/context needed for a proposed test is declared |
| `specified` | Testable subclaim and fixture design exist | Implement test harness, analytic derivation, source review | At least one eligible oracle executes or a blocker is recorded |
| `challenged` | At least one oracle result or counterexample exists | Reproduce, triage, compare independent methods | Result adjudicated with evidence record |
| `supported_bounded` | Claim’s limited statement passes its promotion rule | Use only with exact scope/limitations | New contrary evidence, scope change, or review date reached |
| `falsified` | Registered falsifier succeeds or contradiction is established | Preserve counterexample and prevent promotion | Only a materially different replacement claim may restart at intake |
| `parked` | Missing prerequisite has no funded/defined resolution path | Preserve source/obligation; no active implementation | Prerequisite is supplied and reviewed |
| `retired` | Claim no longer relevant or duplicate | Preserve historical record | None; never delete evidence |

Permitted transitions are `intake→normalized→specified→challenged→supported_bounded|falsified|parked`, with `supported_bounded→challenged` on new evidence. Direct promotion from `intake`, `normalized`, or `parked` is prohibited.

## 4. Test-oracle hierarchy

An oracle is eligible only when its domain matches the claim, its version and inputs are fixed, its execution or source is reviewable, and it is not the same implementation path being tested. Oracles provide evidence; they do not vote. The highest applicable tier governs adjudication.

| Tier | Oracle class | Exact use | Cannot establish alone |
|---|---|---|---|
| O0 | Schema/type validator | Checks packet/object well-formedness, identifiers, referenced versions, and field constraints | Mathematical or physical truth |
| O1 | Machine-checked formal theorem | Checks a named theorem at fixed prover/library revision with explicit assumptions and bridge mapping | Runtime equivalence unless the implementation bridge is separately tested |
| O2 | Analytic derivation or exact closed-form fixture | Checks a derivation whose steps, conventions, and exact expected result are preserved | A broader physical/narrative interpretation |
| O3 | Independent standard implementation | Checks a supported calculation against an independently maintained package or independent in-house implementation | A claim outside the shared model/assumptions |
| O4 | Reproducible numerical experiment | Checks a finite fixture with fixed scalar mode, tolerance, hardware/toolchain metadata, random seed if any, and raw result | Exact identity or universal/physical claim |
| O5 | Primary literature or source evidence | Establishes what a source states and supports standards-context review | A claim merely because a source asserts it |
| O6 | Independent expert review | Reviews derivation, model scope, and interpretation under a recorded conflict-of-interest rule | A result lacking reproducible O1–O5 evidence where such evidence is possible |

### Oracle eligibility test

An oracle plan must answer all questions below. A single `no` makes that oracle unavailable and the affected test returns `unverifiable`.

1. Does the oracle evaluate the exact normalized subclaim rather than a loose analogue?
2. Is the oracle’s version, input, convention profile, and execution/source locator recorded?
3. Is the oracle independent of the implementation under test? Shared code, copied formulas, or shared bug-prone transformation logic must be declared.
4. Are its mathematical domain, scalar mode, coordinate chart, signature, units, and boundary conditions compatible?
5. Is the expected output or acceptance predicate defined before evaluation?
6. Can a third party reproduce or inspect the evidence without privileged mutable state?

## 5. Adjudication rules

| Situation | Required status | Required action |
|---|---|---|
| O1 theorem contradicts O2–O4 result within matching assumptions | `fail` for the tested implementation/claim instance | Freeze promotion; inspect bridge, assumptions, and counterexample. |
| O2 exact fixture contradicts O3/O4 | `fail` for the lower-tier implementation result | Preserve discrepancy; correct or bound the implementation. |
| Two O3 references disagree | `unverifiable` | Publish differential inputs/outputs; identify convention or domain mismatch before retrying. |
| O4 residual exceeds declared tolerance | `fail` | Preserve raw output and numerical metadata; do not widen tolerance post hoc. |
| O4 passes but no O1–O3 oracle applies | `supported_bounded` only for the named numerical fixture | State that no general theorem or physical conclusion follows. |
| Source supports text but definitions are incomplete | `unverifiable` | Keep source claim and missing-prerequisite obligations. |
| Falsifier succeeds | `falsified` | Retire the exact claim; a replacement must receive a new ID. |

There is no majority voting. Two correlated O4 runs never outweigh an O1/O2 contradiction. A result cannot be upgraded by averaging residuals, changing a convention after seeing output, or excluding inconvenient fixtures without a pre-declared applicability rule.

## 6. Exact verification criteria by quarantine category

| Category | Minimum packet additions | Verification threshold | Promotion ceiling |
|---|---|---|---|
| `gu_physics` | Full action/dynamics, spaces/bundles/groups, representation content, boundary/initial conditions, observable consequence, empirical comparison plan | O1 or O2 for each mathematical subclaim; O3/O4 reproduction where computational; O6 independent review before external interpretation | `supported_bounded` unless an empirical program and independent domain review exist; never `verified` as physical theory from software tests alone |
| `gu_representation` | Representation definitions, decomposition, multiplicities, maps, compatibility conventions | O1 or O2 plus O3 differential check for computable instances | Standard sub-formula may become `standard_kernel_candidate`; broad representation interpretation remains quarantined |
| `celestial_narrative` | Ephemeris source/version, time standard, location/frame, mapping function, pre-registered scoring rule, null model | O4 with held-out data and a falsifying null comparison; O5 source provenance | Documentation-only or experimental adapter; never core truth semantics |
| `semantic_mapping` | Corpus/source rights, canonical identifiers, mapping function, ambiguity policy, annotation/reviewer protocol | O0/O5 plus inter-review agreement plan or deterministic lexical rule; O4 only where metrics are defined | Experimental adapter or documentation-only |
| `performance` | Exact workload, operation count, dataset/payload, hardware/OS/toolchain, resource metric, baseline, warm-up policy, raw results | O4 repeated benchmark with median/p95/p99 and counter-baseline; independent reproduction for public claim | Benchmark claim for named workload only; no complexity/universality statement without analysis |
| `consensus_protocol` | Protocol state machine, message formats, adversary/threat model, safety/liveness definitions, resource model, simulator/test harness | O1/O2 for finite protocol invariants where feasible; O4 adversarial simulation; O6 security review | Experimental protocol only until formal/specification and adversarial evidence mature |

## 7. Promotion, isolation, and removal rules

### Standard-kernel candidate

A quarantined subclaim may be proposed for the core only if it has been separated from its GU/narrative interpretation and is expressed as a standard mathematical or software contract. It must satisfy all of the following: an accepted Core Contract version; canonical object/operation/predicate IDs; O1 or O2 evidence; an O3 reference check when feasible; deterministic fixture and tamper/replay records; explicit limitations; and approval through the relevant ADR.

### Experimental adapter

An item with a complete algorithm but unresolved theoretical interpretation may enter an experimental adapter if it cannot affect core status, is visibly labeled `experimental`, preserves all claim/assumption metadata, has a kill switch, and is covered by an abuse/overclaim test. It may not be the sole oracle for any core result.

### Documentation-only

An item remains documentation-only when its primary value is historical context, visualization, or attributed interpretation. It can be shown in UI only with source links, lifecycle state, and limitation banner.

### Removal from active research

An item is parked or retired after the defined review date if prerequisites remain absent, the falsifier succeeds, the source is not usable under data/license policy, or the item duplicates a better-defined claim. Removal from active work never deletes the source packet or counterexample.

## 8. Required evidence record for every executed test

Every oracle run produces a core-independent evidence attachment containing: `quarantine_id`, claim revision, oracle tier and identity, input object IDs, convention profile, scalar/numerical policy, expected predicate, raw output reference/hash, normalized result, status, residual/tolerance if applicable, limitations, contrary outcome, executor/toolchain, UTC timestamp, and replay command or formal/source locator.

## 9. Prohibited behaviors

The following are policy violations: treating source rhetoric as a formula; claiming physical verification from a standard fixture; using an LLM explanation as an oracle; using the implementation under test as its own independent O3 oracle; silently changing tolerance or convention; allowing quarantined behavior to set `verified`; omitting a negative/tamper case; and releasing a result without its limitation/falsifier field.

## 10. Policy conformance checks

The program review must reject a quarantine packet if a required source, definition, falsifier, oracle plan, owner, review date, or promotion target is absent. CI may validate packet schema and reference integrity; human review confirms independence, interpretation, and promotion. Any missing condition returns `unverifiable`, not a warning-level pass.

## References

[1] [JSON Schema Specification, Draft 2020-12](https://json-schema.org/specification)  
[2] [RFC 8785: JSON Canonicalization Scheme](https://www.rfc-editor.org/info/rfc8785/)
