---
name: sovereign-evidence-build
description: Build evidence-first research software from ambiguous technical material into a bounded, reproducible core. Use when a project needs source governance, claim classification, mathematical/software contracts, deterministic canonical data, falsification gates, cross-language parity, auditability, or a staged implementation roadmap before feature growth.
---

# Evidence-First Build Workflow

Use this workflow to turn a technical, mathematical, scientific, or systems-research project into a small verifiable kernel and controlled adapters. Do not treat narrative, transcript, hypothesis, benchmark, or generated content as an established fact.

## Core rule

Keep these planes separate:

| Plane | May contain | May not do |
|---|---|---|
| Source | Originals, extracts, hashes, authority tier | Change source meaning |
| Claim | Statement, assumptions, falsifier, lifecycle | Become verified merely by repetition |
| Core | Canonical data, typed operations, deterministic predicates | Read network state, credentials, mutable labels, or agents |
| Evidence | Input/output IDs, result, reason codes, limits | Rewrite core bytes or silently upgrade a claim |
| Adapter | UI, API, storage, scheduling, explanations | Set core verdicts or inject defaults |

## Workflow

### 1. Freeze evidence and authority

Create a source manifest before analysis. Assign each source an ID, content hash, origin, retrieval date, license/handling rule, authority tier, and scope. Define the authority order; accepted ADRs and versioned contracts should outrank project notes and dashboard views.

Classify every statement as one of: established formal result; standard computation; observed repository behavior; engineering target; hypothesis; narrative/interpretation; or unverified assertion. Require an assumption list and falsifier for every hypothesis.

### 2. Decide the smallest trusted core

Write a Core Contract before building integrations. Specify canonical serialization, object IDs, error taxonomy, scalar/numerical policy, convention profiles, object schemas, status model, operation registry, determinism, and versioning. Keep the core local, pure, and fail-closed.

Use only three terminal result statuses: `verified`, `fail`, and `unverifiable`. A transport, review, or release lifecycle is separate from these result statuses.

### 3. Write adversarial tests before growth

Create fixtures for valid, invalid request, unsupported/unverifiable, failed predicate, tamper, and determinism cases. State the oracle tier for every predicate: formal proof; analytic result; independent standard implementation; symbolic reference; numerical reference; or no oracle. No oracle means `unverifiable`.

Require a negative case for every positive case. Make all known mismatches and numerical-conditioning limits observable in evidence records.

### 4. Implement a reference path and parity plan

Implement the narrowest reference SDK first. Canonicalize, validate schema and semantics, recompute identity, and run a small static registry of predicates. Never dynamically import evaluators, execute user expressions, or make network calls in the core.

Before claiming a second implementation, share immutable fixture vectors and compare exact canonical bytes, IDs, terminal statuses, reason codes, and output IDs. Do not call independently passing test suites “parity.”

### 5. Add adapters in trust order

Add persistence after the pure core; add audit attestations after durable replay; add offline quorum after audit fixtures; add APIs/UI/automation only after they can preserve the same typed contracts. Every adapter must prove it cannot mutate canonical core semantics.

### 6. Gate releases and research promotion

Use the gate template at `templates/gate_matrix.md`. A failed gate reopens the prior boundary; do not overwrite fixtures or relax a policy without an ADR, migration analysis, and reproducer. Preserve failed and contested evidence.

## Required deliverables

Produce, at minimum: source manifest; claim/hypothesis and falsification register; Core Contract; schemas; fixtures; validation report; ADR index; threat/data policy; build plan; and a final report that states what is implemented versus deferred.

## Safety and scope controls

- Do not call a mathematical model, a demo, a benchmark, a quorum, or a signed artifact proof of an external physical claim unless its stated falsifier and evidence level justify that conclusion.
- Treat source ingestion, keys, network endpoints, public APIs, consensus, agents, and narratives as adapters until their threat model and contract are accepted.
- Keep core IDs and canonical bytes independent of mutable metadata, dashboards, timestamps, and signatures.
- Defer a subsystem when its use case, adversary model, oracle, and owner are not explicit.

## Completion checklist

Use the gate matrix. Deliver only after recording both passed checks and known limits. If a project cannot produce a small local replayable path, stop feature growth and repair the core contract first.
