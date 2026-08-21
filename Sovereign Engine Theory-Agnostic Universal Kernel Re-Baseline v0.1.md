# Sovereign Engine Theory-Agnostic Universal Kernel Re-Baseline v0.1

## Decision

The Sovereign Engine kernel is **not a Geometric Unity kernel** and does not assume that any named unification program, metaphysical system, or scientific theory is its preferred ontology. It is a general verification substrate for **declared claims**, **declared structures**, **named checks**, and **inspectable evidence**.

Geometric Unity, causal/discrete approaches, exceptional-algebra programs, amplitude/twistor approaches, noncommutative geometry, holographic quantum-information approaches, and other frameworks are treated as possible **sources of claim packets**. They receive no special truth status, evaluation rule, or roadmap priority merely because they are named. The supplied project statement is therefore treated as a framework landscape, not as a catalogue of validated physical conclusions.[1]

## What the kernel evaluates

| Claim class | Kernel outcome | Required evidence |
|---|---|---|
| Formal | `verified`, `fail`, or `unverifiable` for a named formal object/check | Explicit definitions, assumptions, and a deterministic procedure or proof reference |
| Structural | A receipt for a finite declared structure | Canonicalized input plus an implemented predicate |
| Computational | A replayable output for a specified algorithm/run | Versioned code, input, environment constraints, and expected outcome |
| Empirical | Usually `unverifiable` inside the present kernel | Measurement protocol, data provenance, uncertainty model, and statistical test |
| Interpretive | Not reduced to a kernel verdict | Arguments, source text, competing interpretations, and explicit assumptions |
| Metaphysical | Not reduced to a kernel verdict | Philosophical reasoning; no promotion through a structural receipt |

A check can support one narrow statement—for example, that a given matrix is symmetric. It cannot, by itself, settle whether a cosmological model, a theory of quantum gravity, a sacred-geometry interpretation, or reality as a whole is correct.

## Universal framework-adapter contract

The implementation introduces `sov.structural_claim_packet` v0.1. It contains `framework_id`, `claim_id`, `claim_class`, `check`, and declared input. `framework_id` is an **opaque provenance label**, not a dispatch key for special mathematics. The same structural input receives the same receipt ID regardless of whether its source is labelled `framework:geometric-unity`, `framework:causal-set`, or `framework:custom`.

```json
{
  "schema": "sov.structural_claim_packet",
  "schema_version": "0.1.0",
  "framework_id": "framework:example",
  "claim_id": "claim:matrix-symmetry",
  "claim_class": "structural",
  "check": "matrix.symmetric.v1",
  "input": [[1, 2], [2, 4]]
}
```

The current adapter implements three finite matrix checks. Unsupported structural checks and all empirical, interpretive, and metaphysical claims return `unverifiable` rather than receiving a fabricated score or a theory-level verdict.

## Correction register

| Earlier wording or context | Correction | Disposition |
|---|---|---|
| “Geometric Unity meaning layer” | Historical research corpus, not kernel ontology | Preserve as archived source material; label as one research strand |
| E8, Hopf fibrations, tensors, holography | Candidate mathematical vocabularies and possible adapters | No priority or truth privilege in the kernel |
| “Physical claim” warnings naming GU only | Broaden to all theory-level or reality-level claims | Replace in future public summaries |
| “Universal” interpreted as a universal physical theory | Universal means framework-neutral verification mechanics | Required terminology rule |
| Holographic or multiscale language | A research hypothesis family that may supply formal/structural/empirical packets | Must carry explicit claim class and evidence type |

## Release posture

The completed offline kernel release remains valid because its receipt, replay, audit, fixture-signature, and parity mechanics do not depend on a preferred physical theory. Its public documentation is reinterpreted as a theory-neutral substrate. Any later adapter must add a named predicate, fixtures, scope, and claim-class boundary before it can produce a receipt.

## Roadmap change

The next program is not “implement Geometric Unity.” It is **build a framework-adapter portfolio**: select a small, well-defined structural claim from different traditions, encode it without importing theory-level conclusions, and compare evidence boundaries. A candidate adapter is admitted only when it specifies the object, assumptions, predicate, expected outcomes, fixtures, and what a successful receipt does *not* establish.

## References

[1] `science_project.md` (user-provided project statement): alternatives spanning causal/discrete, algebraic, amplitude/twistor, noncommutative, and holographic/QEC frameworks; treated here as research context, not an authoritative validation source.
