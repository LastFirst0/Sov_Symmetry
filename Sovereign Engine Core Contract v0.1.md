# Sovereign Engine Core Contract v0.1

**Contract identifier:** `sov.core.contract.v0.1`  
**Status:** Proposed; requires ADR-001, ADR-002, ADR-003, ADR-005, and ADR-006 acceptance before implementation is declared conformant.  
**Normative schema:** `schemas/sov.core.v0_1.schema.json`  
**Scope:** The deterministic evidence–geometry core only. This contract excludes network access, databases, LLMs, UI, agent routing, signing services, consensus, GU physical evaluation, and mutable display metadata.

## 1. Normative language and authority

The terms **MUST**, **MUST NOT**, **REQUIRED**, **SHOULD**, **SHOULD NOT**, and **MAY** are normative. If this document conflicts with a lower-authority artifact, this document governs after its ADR acceptance. A future accepted contract version supersedes this version only through an explicit migration record.

## 2. Core promise

Given the same validated canonical inputs, operation ID/version, predicate ID/version, convention profile, scalar policy, and implementation release, a conforming core MUST produce the same canonical result or the same typed error. It MUST never infer omitted assumptions, source meanings, physical interpretation, or executable callbacks.

The core recognizes exactly three **evaluation statuses**: `verified`, `fail`, and `unverifiable`. They describe a concrete operation/predicate instance only. They are not claim-publication state, research lifecycle, availability, or human approval.

## 3. Supported v0.1 object algebra

| Object kind | Required purpose | v0.1 limit |
|---|---|---|
| `manifold` | Finite-dimensional declared base space | Dimension 1–256; no automatic topology inference |
| `chart` | Named coordinate chart over a manifold | Coordinate symbols unique; transition maps are deferred |
| `tensor` | Tensor with typed slots and component encoding | Slot variance, symmetry declarations, and finite rank only |
| `metric` | Nondegenerate symmetric covariant rank-2 tensor declaration | Inverse/nondegeneracy may be a verified fixture or an explicit assumption |
| `form` | Differential form with declared degree and coefficient algebra | Exterior algebra contracts only; integration is deferred |
| `connection` | Affine, Levi–Civita, or gauge connection declaration | Spin connection/Dirac implementation deferred from executable core |
| `expression` | Typed symbolic expression or exact/float scalar leaf | No simplifier may alter semantic meaning without a registered operation |
| `orientation` | Declared orientation context | Required for Hodge operations; no implicit orientation |
| `evidence_record` | Replayable operation/predicate outcome | Immutable canonical core; display envelope is external |

## 4. Identifiers and references

Every semantic object ID and evidence ID has the form `sov:sha256:<64 lowercase hexadecimal characters>`. IDs are derived, never user-assigned. A reference is valid only if it points to an object of the required kind and schema version. A missing, unknown, cyclic, wrong-kind, or version-incompatible reference MUST yield a typed error or `unverifiable` outcome.

## 5. Canonicalization and hashing

Canonical bytes are UTF-8 JSON Canonicalization Scheme (JCS) bytes over the **canonical body**, followed by SHA-256. JCS requires I-JSON-compatible input, deterministic object-key ordering, preserved array order, and rejects duplicate properties, invalid Unicode, NaN, and Infinity. SHA-256 yields a 256-bit message digest suitable for detecting changes, but does not alone prove authorship or truth. [1] [2]

### 5.1 Canonical body rules

The canonical body MUST contain only semantic fields: `schema`, `schema_version`, `object_kind`, `convention_profile`, `assumptions`, and `content`. It MUST NOT contain an ID, timestamp, UI label, source retrieval timestamp, display text, thumbnail, network locator, signature, owner, or mutable lifecycle field.

The object ID is:

```text
object_id = "sov:sha256:" + lowercase_hex(SHA-256(JCS(canonical_body)))
```

Evidence IDs use the same formula over their canonical evidence body. Source/provenance attachments are stored outside the hashed semantic object but MUST be hash-addressed and referenced by evidence/claim packets.

### 5.2 Scalar representation

Raw JSON numbers are prohibited in canonical mathematical payloads. A scalar MUST be one of:

| Scalar kind | Canonical representation | Rule |
|---|---|---|
| `integer` | Decimal string matching `0|[1-9][0-9]*` or a leading `-` version | No `+`, leading zero, or whitespace. |
| `rational` | Reduced signed numerator string plus positive denominator string | `gcd(abs(numerator), denominator)=1`; zero denominator prohibited. |
| `float64` | Exactly 16 lowercase hex digits representing IEEE-754 binary64 bits | NaN, ±Infinity, and negative-zero bit pattern are prohibited in v0.1. |
| `symbol` | Identifier with optional typed index list | No implicit units, assumptions, or simplification. |

The core MUST NOT coerce between scalar kinds unless a registered operation explicitly names the conversion and records its loss/assumption semantics.

## 6. Conventions and assumptions

Every operation MUST reference one immutable `convention_profile`. The v0.1 profile includes curvature sign, metric signature order, index notation, scalar policy, coordinate basis policy, unit policy, and tolerance policy. No default convention is permitted at operation execution time.

Assumptions are immutable IDs referencing registered predicates or declarative conditions. Free-text assumptions are prohibited in canonical bodies. Examples include `assumption:smooth_chart.v1`, `assumption:nondegenerate_metric.v1`, and `assumption:coordinate_basis.v1`.

## 7. Object validation rules

JSON Schema validates shape; semantic validation enforces cross-object and mathematical conditions. A conforming implementation performs both before operation evaluation.

| Object | Schema requirements | Semantic requirements |
|---|---|---|
| Manifold | Dimension, scalar policy, declared signature/orientation mode | Dimension equals coordinate count for a full chart; signature entries sum to dimension when supplied |
| Chart | Valid manifold reference; unique coordinate identifiers | Chart dimension equals referenced manifold dimension |
| Tensor | Typed slots, manifold/chart reference, component encoding, symmetry list | Slot count equals rank; symmetry slots are in range; sparse keys cover exact rank; component indices are in bounds |
| Metric | Tensor-like fields, declared signature, symmetry | Covariant rank two, symmetric; signature compatible with manifold; inverse/nondegeneracy is proven or assumed—not silently asserted |
| Form | Degree, manifold/chart, coefficient algebra, component encoding | `0 ≤ degree ≤ dimension`; multi-index ordering follows declared antisymmetry convention |
| Connection | Kind, manifold/chart, coefficients, required context references | Levi–Civita requires metric; gauge requires bundle/algebra reference; properties are results/assumptions, not labels |
| Expression | Typed AST node | Every referenced symbol/object/index resolves and has type-compatible operands |
| Evidence | Operation/predicate IDs, input IDs, output IDs, status, limitation codes | Operation schema accepts input kinds; a `verified` status requires all required predicates pass and no missing assumption |

## 8. Operation and predicate registry

The registry is code-owned and versioned. Each operation defines its exact ID, semantic version, input object-kind signature, parameter schema, output kind(s), required convention fields, required assumptions, deterministic flag, and supported scalar modes. Each predicate defines its ID, input signature, acceptance condition, residual type, tolerance schema, and status mapping.

Operations and predicates not present in the compiled registry MUST NOT execute. User-supplied code, callback names, dynamic imports, plugin URLs, or expression evaluation strings are prohibited.

## 9. Status mapping

| Condition | Evaluation status | Required reason code |
|---|---|---|
| All input/schema/reference checks pass; all required predicates pass under declared assumptions | `verified` | `VERIFIED` |
| Inputs are evaluable but a required predicate fails or residual exceeds predeclared tolerance | `fail` | Specific predicate failure code |
| Required definition, assumption, oracle, scalar-mode support, reference, or operation is absent; unsupported feature; evaluator cannot establish predicate | `unverifiable` | Specific missing/unsupported code |
| Schema/identifier/canonicalization violation | No result record; typed request error | Specific `E_*` code |

`verified` MAY mean a syntactic, mathematical, or numerical fixture predicate passed. The evidence record MUST declare `verification_scope` as `schema`, `exact_symbolic`, `exact_analytic`, `numerical_fixture`, `differential_reference`, or `formal_anchor`. It MUST NOT be rendered as a physical-theory verdict.

## 10. Error taxonomy

| Code | Meaning | Retry policy |
|---|---|---|
| `E_SCHEMA_INVALID` | JSON fails the published schema | Fix input |
| `E_CANONICALIZATION` | Duplicate key, invalid Unicode, invalid scalar encoding, or noncanonical semantic field | Fix input; never auto-rewrite silently |
| `E_ID_MISMATCH` | Supplied ID differs from derived canonical ID | Fix input or investigate tampering |
| `E_REFERENCE_MISSING` | Referenced object/evidence does not exist | Supply reference |
| `E_REFERENCE_KIND` | Referenced object has wrong kind/schema | Correct graph |
| `E_DIMENSION_MISMATCH` | Dimensions, coordinate count, or signature conflict | Correct model |
| `E_INDEX_INVALID` | Variance, slot, contraction, symmetry, or component index invalid | Correct expression/object |
| `E_CONVENTION_MISSING` | Required convention profile field absent | Supply accepted profile |
| `E_ASSUMPTION_MISSING` | Required assumption not declared/established | Return `unverifiable` when operation can otherwise be represented |
| `E_OPERATION_UNKNOWN` | Operation ID/version unavailable | Return `unverifiable` or upgrade implementation |
| `E_PREDICATE_UNKNOWN` | Predicate ID/version unavailable | Return `unverifiable` |
| `E_SCALAR_UNSUPPORTED` | Requested scalar kind/mode unsupported | Return `unverifiable` |
| `E_NUMERICAL_NONFINITE` | Evaluation produced NaN or infinity | Return `fail` with raw-output reference |
| `E_RESOURCE_LIMIT` | Declared deterministic resource limit reached | Return `unverifiable`; preserve limit metadata |
| `E_INTERNAL_DETERMINISM` | Same canonical request produced inconsistent canonical output | Quarantine release; never emit `verified` |

## 11. Determinism and resource limits

The v0.1 core MUST be pure with respect to semantic evaluation: no network, clock, filesystem, random source, environment variable, database, GPU, process-global cache, or mutable registry access may influence canonical output. Implementations MUST set and record maximum AST depth, object bytes, array entries, tensor rank, component count, evaluation steps, and wall-clock budget. Exceeding a limit returns `unverifiable` with `E_RESOURCE_LIMIT`; it is not a proof of failure.

## 12. Conformance suite

An implementation is v0.1 conformant only if it passes all published schema and fixture cases, including canonicalization key-order stability, duplicate-key rejection, Unicode handling, rational reduction validation, nonfinite float rejection, object-ID recomputation, wrong-kind reference rejection, invalid contraction rejection, metric signature failure, unknown-operation fail-closed behavior, missing-assumption `unverifiable`, predicate failure `fail`, and evidence replay/tamper mismatch.

The minimum fixture pack contains 17 cases: 8 valid/verified, 4 invalid request failures, 2 `unverifiable` outcomes, 1 failed-predicate outcome, and 2 tamper/determinism failures. Implementations MUST run the same fixture pack in Rust and Python reference adapters; Lean anchors are additive and do not replace fixture conformance.

## 13. Non-goals and extension rules

The contract does not define arbitrary CAS simplification, automatic theorem proving, topology inference, general tensor density algebra, spinor spectra, E8/GU action semantics, physical prediction, external signing, persistent storage, or API transport. New object kinds, changed scalar semantics, canonical-byte changes, and relaxed validation require a new schema version, ADR, migration/compatibility analysis, and conformance fixture expansion.

## References

[1] [RFC 8785: JSON Canonicalization Scheme](https://www.rfc-editor.org/info/rfc8785/)  
[2] [NIST FIPS 180-4: Secure Hash Standard](https://csrc.nist.gov/pubs/fips/180-4/upd1/final)  
[3] [JSON Schema Specification, Draft 2020-12](https://json-schema.org/specification)
