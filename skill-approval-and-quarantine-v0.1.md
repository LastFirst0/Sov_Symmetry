# Skill Approval and Quarantine v0.1

## Decision rule

External skills are dependencies, not authorities. The approval sequence is **discover → inspect → quarantine trial → score → human approval → reversible import**. No skill, model, source connector, or generated narrative can produce a kernel `verified` result; that status remains limited to registered deterministic predicates and reviewable evidence.

Custom Sovereign-specific skills are also deferred until the same stable workflow has completed successfully **three times**, uses a versioned schema, has a deterministic fixture, and contains non-obvious reusable policy or automation. A candidate custom skill cannot encode an unverified theory as a rule.

## Candidate assessment record

The machine-readable record is [`skill_quarantine_register.json`](../../data/skill_quarantine_register.json). The assessment below records what was inspected on 2026-08-18. None is imported.

| Candidate | Observed fit | Primary limitation | Disposition | Next admissible step |
|---|---|---|---|---|
| Biopython v1.2 | Local public-sequence parsing and format handling may support a fixture-backed intake path | Dependency and untrusted-file parser review required; network retrieval is not deterministic evidence | Quarantine candidate | Public FASTA parsing trial with digest and malformed-input fixtures |
| Genomic Intelligence v1.0 | Hosted sequence-model outputs could be exploratory analysis artifacts | Third-party sequence transfer, provider/model provenance, and output retention require separate review; outputs cannot verify a claim | Deferred | Explicit approved public-data-only exploratory receipt trial |
| Literature Review v1.7 | Some search/citation practices overlap with source-intake needs | Requires non-approved dependencies and mandatory generated figures; optional external LLM path is outside current boundaries | Not approved | Re-scope to a provenance-only metadata workflow before reconsideration |
| TorchDrug v1.1 | Molecular graph/protein modelling may later support a bounded research experiment | Published runtime compatibility does not match the current Python environment; native dependencies and compute budget need a separate environment | Blocked | Demonstrate a pinned compatible environment and seeded public benchmark |

## Quarantine scorecard

Each candidate must be assessed against all criteria below. A missing item produces `unverifiable` rather than an inferred approval.

| Criterion | Required evidence | Pass threshold |
|---|---|---|
| Source and license | Pinned repository revision, license text, and maintainer/release metadata | License and revision recorded; no ambiguous redistribution condition |
| Scope overlap | Existing capability matrix and work-package boundary | Adds a real gap; does not duplicate a governed capability without advantage |
| Data handling | Source destinations, fields, retention, credentials, and public/private classification | Data is minimized; no personal or clinical sequence transfer without a specific separate authorization |
| Determinism | Fixture, seed, environment lock, and replay behavior | Stable declared output or an explicitly exploratory non-verdict result |
| Dependency fit | Runtime, native/system requirement, version and resource profile | Compatible reviewed environment or a separate approved worker plan |
| Evidence packaging | Source manifest, receipt, limitation and output schema | Fits the empirical packet and falsification workflow without browser-side inference |
| Rollback | Disable/import removal and artifact retention procedure | A reversible path is documented and tested |

## Custom-skill creation gate

When a workflow clears the three-use threshold, create only a small skill with a concise trigger description, versioned reference schemas, deterministic scripts where warranted, and at least one invalid/tamper fixture. Candidate future skills remain `sov-research-work-package`, `sov-dataset-manifest`, `sov-molecular-benchmark`, `sov-experiment-gate`, `sov-adapter-review`, `sov-release-evidence`, and `sov-dashboard-feed`. None is created by this policy.

## References

[1] [Skill and pipeline gap matrix](skill_and_pipeline_gap_matrix.md)

[2] [K-Dense scientific-agent-skills repository](https://github.com/K-Dense-AI/scientific-agent-skills)

[3] [Quarantine register v0.1](../../data/skill_quarantine_register.json)
