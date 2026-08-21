# Third-Party Theoretical Framework Adapter Specification v0.1

## Status and intent

This is the admission specification for third-party framework adapters to the theory-agnostic Sovereign Engine kernel. An adapter may contribute **bounded checkable structures**. It may not grant special ontology, scientific endorsement, or evaluator privileges to its source framework.

> A successful receipt supports only the named predicate over the declared input and assumptions. It never validates an entire theory, physical interpretation, or worldview.

## Conformance vocabulary

| Term | Meaning |
|---|---|
| Framework | A provenance source for claims, notation, and references. |
| Adapter | A versioned mapping from a packet schema to one or more named predicates. |
| Claim packet | A declared object, claim class, check, assumptions, and source references. |
| Predicate | A deterministic, versioned operation with explicit terminal outcomes. |
| Fixture pack | Positive, negative, malformed, boundary, and mutation cases with declared expected outcomes. |
| Receipt | The replayable output of one predicate evaluation. |

## Adapter identity and neutrality

An adapter must publish an immutable `adapter_id`, semantic version, maintainer identity, license, and source references. The kernel must treat `framework_id` as opaque provenance. The evaluator **MUST NOT** branch on a framework label, theory name, source author, or interpretation.

## Required claim packet

```json
{
  "schema": "sov.structural_claim_packet",
  "schema_version": "0.1.0",
  "framework_id": "framework:third-party-example",
  "claim_id": "claim:bounded-structure",
  "claim_class": "formal | structural | computational | empirical | interpretive | metaphysical",
  "check": "namespace.predicate.v1",
  "input": {},
  "assumptions": [],
  "source_refs": []
}
```

Adapters may add namespaced input fields only when their schemas make each field typed, finite or bounded where required, and replayable. Hidden data fetches, mutable global state, unversioned dependencies, and implicit theory defaults are forbidden in the deterministic evaluation path.

## Claim-class behavior

| Claim class | Current kernel behavior |
|---|---|
| `formal`, `structural`, `computational` | Eligible for a deterministic predicate after admission. |
| `empirical` | Must return `unverifiable` until an external measurement and statistical process is attached. |
| `interpretive`, `metaphysical` | Must return `unverifiable`; they are not converted into kernel truth values. |

## Predicate requirements

Every predicate MUST state its object representation, dimensions or index conventions, assumptions, exact equality/tolerance policy, and scope. It MUST return only `verified`, `fail`, or `unverifiable`; include a plain-language explanation; identify mismatches or missing requirements; and specify non-claims.

## Fixture and mutation policy

A candidate adapter is admitted only with a frozen fixture pack containing at least one case in every row below.

| Fixture class | Minimum requirement | Expected behavior |
|---|---|---|
| Positive | Predicate holds | `verified` |
| Negative | Predicate is well-formed but violated | `fail` plus local mismatch evidence |
| Malformed | Input shape/type/assumption invalid | `unverifiable` with typed reason |
| Boundary | Smallest and largest supported dimensions | Stable, deterministic result |
| Mutation | One controlled change from a positive fixture | Must not remain an unexplained pass |
| Neutrality | Same input under at least three provenance labels | Same receipt ID and outcome |

## Replay, audit, and assurance

All admitted predicates MUST produce replayable provenance. Optional audit, Merkle, signature, or quorum evidence may be attached only when actually recorded; absence must be represented as not recorded. No adapter may imply a public transparency log, production key management, or distributed consensus from local fixture evidence.

## Independent review gates

1. **Schema review:** packet and fixture schemas are complete and versioned.
2. **Semantic review:** predicate and assumptions are independently readable.
3. **Neutrality review:** no framework-conditioned evaluator branch exists.
4. **Mutation review:** failures and malformed cases are explained and stable.
5. **Scope review:** public copy makes non-claims prominent.
6. **Release review:** reproducible command, fixture hashes, and test report are published.

## Rejection conditions

An adapter is rejected or quarantined if it embeds a theory-level conclusion in a receipt, depends on unpublished data, silently changes fixture behavior, branches on framework provenance, hides a non-finite/tolerance policy, or labels an empirical/metaphysical statement as `verified` by a structural predicate.

## References

[1] `UNIVERSAL_FRAMEWORK_ADAPTER_CONTRACT_v0.1.md`.  
[2] `UNIVERSAL_ADAPTER_PORTFOLIO_ROADMAP_v0.1.md`.  
[3] `UNIVERSAL_SIX_ADAPTER_INTEGRATION_REPORT.json`.
