# Universal Framework Adapter Contract v0.1

## Purpose

This contract allows research frameworks to submit bounded structural claims to the kernel without granting special ontology, scientific endorsement, or hidden theory-specific behavior.

## Required packet fields

| Field | Meaning | Constraint |
|---|---|---|
| `framework_id` | Source/provenance label | Opaque string; never selects evaluation semantics |
| `claim_id` | Stable local claim label | Opaque string; unique within framework scope |
| `claim_class` | `formal`, `structural`, `computational`, `empirical`, `interpretive`, or `metaphysical` | Only the first three are candidates for current deterministic checks |
| `check` | Named predicate | Must be implemented and versioned |
| `input` | Declared finite object | Must meet the predicate’s typed schema |
| `assumptions` | Optional explicit restrictions | Must be exposed in the receipt scope |
| `source_refs` | Optional source/provenance references | Do not convert sources into proof |

## Terminal behavior

A supported formal, structural, or computational claim receives the standard receipt outcomes. An unsupported check returns `unverifiable`. Empirical, interpretive, and metaphysical claims return `unverifiable` in the current deterministic kernel, with a direct explanation of the missing evidence process.

## Admission checklist for a new adapter

1. State the exact object and its representation.
2. State the predicate in ordinary language and, where applicable, formal notation.
3. List assumptions and the intended domain.
4. Provide positive, negative, malformed, and boundary fixtures.
5. State the expected receipt fields and non-claims.
6. Define replay and audit behavior.
7. Obtain independent review before any theory-level language appears in user-facing output.
