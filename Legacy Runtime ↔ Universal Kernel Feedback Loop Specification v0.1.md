# Legacy Runtime ↔ Universal Kernel Feedback Loop Specification v0.1

**Status:** Proposed implementation contract  
**Purpose:** Define a concrete, fail-closed research loop in which a legacy geometry runtime can propose experiment artifacts while the universal kernel records, verifies, and governs bounded evidence.  
**Non-goal:** This specification does not make the legacy runtime, an LLM, a geometric score, or a successful benchmark self-verifying.

## 1. System intent and trust separation

The feedback loop exists to convert broad geometry ideas into **versioned experiments with visible outcomes**. It has three independent functions: the legacy runtime proposes candidates, an independent evaluation runner measures candidates against declared baselines, and the universal kernel verifies evidence-package integrity and controls promotion. The candidate runtime never writes a verified result, chooses its own acceptance rule after execution, or edits the verifier registry.

| Component | Trust level | May do | Must never do |
|---|---|---|---|
| **Legacy Research Runtime (LRR)** | Quarantined candidate producer | Generate a declared transform, embedding artifact, model checkpoint reference, feature set, or visualization. | Sign its own promotion, rewrite frozen experiment rules, alter result manifests, or label itself “verified.” |
| **Experiment Registry (ER)** | Controlled metadata service | Validate proposals, freeze versions, issue experiment IDs, manage state transitions, and append audit events. | Execute untrusted callbacks named in a request or accept missing baselines/metrics. |
| **Independent Evaluation Runner (IER)** | Isolated evaluator | Run code from an allowlisted container/image against a frozen dataset and evaluator. | Reuse LRR-reported metrics without recomputation or access production signing keys. |
| **Universal Kernel Gate (UKG)** | Small trusted verifier | Canonicalize packet fields, recompute hashes, verify schemas/manifests/signatures, evaluate code-owned predicates, and issue bounded receipts. | Train a model, choose an ontology, infer a theory, or decide a value-laden publication/deployment question. |
| **Human Review Authority (HRA)** | Accountable decision maker | Interpret scoped results; approve, reject, or quarantine experimental adapters. | Rewrite immutable evidence or call an exploratory outcome a production proof without a new approved gate. |
| **Dashboard / Explorer** | Untrusted presentation layer | Display facts from receipts, statuses, limitations, and comparisons. | Compute pass/fail itself, hide a failed control, or render an exploratory metric as theory verification. |

## 2. Non-negotiable invariants

1. **Every accepted experiment has one frozen proposal digest.** Changing a dataset, split, model image, candidate parameters, baseline, metric, budget, or non-claim creates a new experiment revision.
2. **The candidate does not grade itself.** Any metric produced by the LRR is `reported`, not `independently_recomputed`, until the IER emits an artifact that the UKG validates.
3. **No result is promoted merely because it is positive.** A promotion predicate requires declared baseline, holdout result, artifact integrity, evidence completeness, and human decision.
4. **Unknown means blocked.** Missing schema, unknown operation, mismatched hash, expired key, unavailable baseline, unreproducible result, or missing reviewer decision produces `unverifiable`, `quarantined`, or `rejected`; it never produces a successful gate.
5. **Evidence is append-only.** Revised interpretation or display text is stored separately from immutable proposal, candidate, evaluator, and verifier cores.
6. **Theory labels are provenance only.** `framework_id: legacy:e8` may label a proposal, but cannot select executable code, tolerance, expected result, or pass status.

## 3. Domain objects and canonical fields

All core objects use strict JSON, versioned schema IDs, canonical JSON bytes, and SHA-256 content identifiers. The canonical core excludes presentation copy, dashboard layout, and transient scheduling information. The existing core canonicalization and receipt policy remain the reference for core IDs. [1]

| Object | Schema ID | Immutable core fields | Producing authority | Terminal use |
|---|---|---|---|---|
| **Experiment Proposal** | `sov.experiment_proposal.v0.1` | `proposal_id`, `hypothesis`, `claim_class`, `dataset`, `splits`, `baselines`, `candidate_family`, `metrics`, `selection_rule`, `falsification_rule`, `budget`, `non_claims` | Human/research steward | Establishes what would count as a result. |
| **Frozen Experiment** | `sov.frozen_experiment.v0.1` | `experiment_id`, `proposal_sha256`, `schema_registry_version`, `approved_image_digests`, `dataset_manifest_sha256`, `created_by` | ER | Binds a run to immutable terms. |
| **Candidate Submission** | `sov.candidate_submission.v0.1` | `candidate_id`, `experiment_id`, `source_revision`, `image_digest`, `entrypoint_id`, `parameters`, `artifact_manifest_sha256`, `declared_framework_id` | LRR | Requests evaluation; no verdict field allowed. |
| **Evaluation Request** | `sov.evaluation_request.v0.1` | `request_id`, `experiment_id`, `candidate_id`, `baseline_ids`, `evaluator_version`, `resource_budget` | ER | Authorizes the IER to run only named allowlisted operations. |
| **Evaluation Bundle** | `sov.evaluation_bundle.v0.1` | `bundle_id`, `request_id`, `input_manifest_sha256`, `output_manifest_sha256`, `metrics`, `uncertainty`, `logs_digest`, `environment_digest`, `exit_status` | IER | Supplies independently recomputed measured results. |
| **Gate Receipt** | `sov.experiment_gate_receipt.v0.1` | `receipt_id`, `experiment_id`, input hashes, predicate versions, terminal status, reason codes, scope | UKG | States whether the evidence package meets a narrow gate. |
| **Review Decision** | `sov.review_decision.v0.1` | `decision_id`, `receipt_id`, `reviewer_id`, `decision`, `rationale`, `scope`, `signature_ref` | HRA | Gives accountable human disposition. |
| **Feedback Packet** | `sov.runtime_feedback.v0.1` | `feedback_id`, `candidate_id`, `gate_receipt_id`, allowed metrics, reason codes, next permitted action | ER/UKG | Safely tells LRR what to improve or investigate next. |

### 3.1 Required Experiment Proposal structure

```json
{
  "schema": "sov.experiment_proposal",
  "schema_version": "0.1.0",
  "proposal_id": "experiment:hierarchy-recovery:001",
  "claim_class": "computational",
  "hypothesis": "Candidate C improves held-out direct-hypernym recovery over named baseline B under the declared protocol.",
  "framework_id": "legacy:e8-research",
  "dataset": {
    "dataset_id": "oewn:2025:animal-spanning-tree",
    "content_sha256": "<64-lowercase-hex>",
    "license": "CC-BY-4.0",
    "access": "open"
  },
  "splits": {
    "selection": "deterministic-hash-v1",
    "holdout": "deterministic-hash-v1",
    "forbidden_overlap": true
  },
  "baselines": ["euclidean-cosine-text-v1", "random-ranking-v1"],
  "candidate_family": "hyperbolic-text-heuristic-v0",
  "metrics": ["top1", "top3", "mrr", "mean_rank"],
  "selection_rule": "Choose candidate settings only on selection split; evaluate once on holdout.",
  "falsification_rule": "No candidate advantage if holdout Top-1 delta 95% bootstrap lower bound is less than or equal to zero.",
  "budget": {"cpu_seconds": 600, "memory_mb": 2048, "network": "disabled"},
  "non_claims": [
    "No claim about a universal geometry of language.",
    "No claim about E8, Hopf fibrations, cognition, or reality."
  ]
}
```

The registry rejects the proposal if any required property is omitted, baseline set is empty, selection and holdout splits overlap, or a `framework_id` attempts to select an operation. An LRR-provided command line, Python path, URL, shell expression, or callback may **not** be treated as an executable evaluator instruction.

## 4. State machine

```text
draft
  └─submit→ submitted
       ├─schema/hash/baseline failure→ rejected
       └─validation→ frozen
            └─candidate accepted for queue→ queued
                 ├─budget/image/allowlist failure→ quarantined
                 └─isolated run starts→ running
                      ├─run failure→ execution_failed
                      └─artifact emission→ candidate_reported
                           └─independent recomputation→ independently_evaluated
                                ├─receipt integrity/predicate failure→ evidence_failed
                                ├─missing evidence→ unverifiable
                                └─complete receipt→ review_pending
                                     ├─review reject→ rejected
                                     ├─review defer→ quarantined
                                     └─review accept→ admitted_experimental
```

Only these transition actors are allowed:

| Transition | Actor | Required evidence |
|---|---|---|
| `submitted → frozen` | ER | Valid proposal schema; frozen dataset/version; baseline list; explicit metric/falsification and non-claims. |
| `frozen → queued` | ER | Approved candidate manifest, code revision, image digest, resource policy, no forbidden capability. |
| `queued → running` | IER | Isolated job with network disabled by default, read-only dataset mount, write-only results mount, and no signing credential. |
| `candidate_reported → independently_evaluated` | IER | Fresh evaluator outputs and complete logs/manifests. |
| `independently_evaluated → review_pending` | UKG | Recomputed input/output hashes, allowed predicate, complete evidence package, and no unknown operation. |
| `review_pending → admitted_experimental` | HRA | Signed human decision that repeats scope and non-claims. |

No automated transition reaches `admitted_experimental`. No transition reaches a term such as `true`, `coherent`, `validated theory`, `safe`, or `production-ready`.

## 5. Exact gate predicates

The UKG contains a code-owned registry of predicates. Requests reference a named version only; they do not carry executable logic.

| Predicate ID | Assertion level | Inputs | Pass condition | Failure/rejection consequence |
|---|---|---|---|---|
| `experiment.proposal_complete.v1` | Exact check | Proposal object | All required fields/type constraints/non-claims present. | `rejected:E_PROPOSAL_INCOMPLETE` |
| `experiment.dataset_pinned.v1` | Exact check | Dataset manifest | Content digest, license, source, and split rule match frozen proposal. | `unverifiable:E_DATASET_UNPINNED` |
| `experiment.candidate_allowed.v1` | Tested contract | Candidate manifest | Image, entrypoint ID, parameter keys, and budget match approved allowlist. | `quarantined:E_CANDIDATE_NOT_ALLOWED` |
| `experiment.evaluator_recomputed.v1` | Tested contract | Candidate/evaluator bundles | IER output manifest and evaluation request match; no candidate metric is substituted. | `unverifiable:E_EVALUATOR_NOT_INDEPENDENT` |
| `experiment.holdout_delta.v1` | Numeric check | Frozen metric outputs and bootstrap details | The lower confidence bound and effect rule satisfy the predeclared threshold. | `fail:E_HOLDOUT_ADVANTAGE_NOT_SUPPORTED` |
| `experiment.baseline_complete.v1` | Exact check | Evaluation bundle | All named baselines completed under same task/split and compatible budget. | `unverifiable:E_BASELINE_MISSING` |
| `experiment.artifact_integrity.v1` | Exact check | Artifact manifest, signatures, logs | Recomputed hashes and signatures match; no stale/missing artifact. | `fail:E_ARTIFACT_INTEGRITY` |
| `experiment.review_present.v1` | Exact check | Review decision | Valid signature/reference and scoped human decision are present. | `unverifiable:E_REVIEW_REQUIRED` |

The hierarchy pilot currently fails the `experiment.holdout_delta.v1` advancement condition: the candidate produced lower held-out Top-1 recovery than the Euclidean baseline, and the reported bootstrap lower bound did not show an advantage. It remains a valid negative-result artifact rather than a defect to hide. [2]

## 6. Interfaces and endpoints

These are internal service contracts. They can be implemented through tRPC for the dashboard backend, CLI calls for local research, or a future authenticated API. They are not public endpoints by default.

| Operation | Request | Response | Access rule |
|---|---|---|---|
| `POST /v1/experiments/proposals` | Experiment Proposal | Proposal receipt or typed rejection | Research steward role. |
| `POST /v1/experiments/{id}/freeze` | Approver identity + dataset manifest | Frozen Experiment | Separate registry authority. |
| `POST /v1/experiments/{id}/candidates` | Candidate Submission | Queue decision | LRR service account; no review privilege. |
| `POST /v1/evaluations` | Evaluation Request | IER job reference | Registry only. |
| `POST /v1/evaluations/{id}/bundle` | Evaluation Bundle | Integrity-receipt request | IER only; signed workload identity. |
| `POST /v1/gates/evaluate` | Frozen experiment plus bundles | Gate Receipt | UKG only; code-owned predicate registry. |
| `POST /v1/reviews` | Review Decision | Decision receipt | Authorized reviewer; no mutation of evidence core. |
| `GET /v1/experiments/{id}` | Experiment ID | Read-only complete state/provenance graph | Redacted by artifact access policy. |
| `GET /v1/experiments/{id}/feedback` | Candidate identity | Narrow Feedback Packet | LRR receives only approved aggregate details. |

### 6.1 Optional Manus API integration

The Manus API is optional orchestration infrastructure, never a source of trusted verdicts. A controlled integration may create a research-assistance task for documentation, code review, or a bounded analysis plan; its `task_id`, versioned prompt, attachments, and structured output can be attached as **provenance metadata**. The task’s prose must not become a passing gate result until an independent evaluator and UKG predicate process it. Any production use must follow the Manus API v2 task lifecycle, structured-output, authentication, and webhook verification contracts. [3]

## 7. Runtime isolation, capabilities, and operational safety

| Resource | LRR | IER | UKG | Policy |
|---|---|---|---|---|
| Public experiment data | Read-only copy only | Read-only pinned copy | Hash/manifest only | Data content is not stored in receipts unless policy permits. |
| Network | Disabled by default | Disabled | Disabled | Explicit, logged exception only for approved data acquisition. |
| Kernel source/registry | Read only | Read only | Controlled release only | No LRR/IER write capability. |
| Release keys | No access | No access | Verification public keys only; signing occurs in separate authority. | Key custody is outside workloads. |
| Result store | Candidate staging only | Write evaluator bundle once | Append receipt only | No overwrite/delete path from candidate. |
| Secrets | None | Narrow dataset credential if unavoidable | Verification-specific only | No shared environment variables across roles. |

The first implementation should run locally in separate directories/process identities, then migrate to short-lived containers. It should never start as a networked self-modifying agent. Resource ceilings, read-only inputs, no network by default, and signed/hashed manifest checks are part of the experiment definition rather than later operations polish.

## 8. Reusable component assessment

| Component | Intended use | Recommended posture | Important boundary |
|---|---|---|---|
| [Open English WordNet + `wn`](https://github.com/globalwordnet/english-wordnet) | Public lexical hierarchy corpus for pilots. | **Use now** for open, pinned sample experiments; record lexicon version/license. | It is an evaluation resource, not a theory of all semantics. |
| [Geoopt](https://github.com/geoopt/geoopt) | Riemannian/hyperbolic optimization in a future PyTorch candidate. | **Evaluate for later use**, pin version/image, test with independent Euclidean baselines. | Geoopt may optimize a chosen manifold objective; it does not validate why that manifold is linguistically correct. |
| [giotto-tda](https://github.com/giotto-ai/giotto-tda) | Exploratory topological measurements. | **Research-only review** after license analysis; do not couple it to the trusted kernel. | Its AGPLv3 licensing and estimator sensitivity require legal and methodological review. |
| [MLflow](https://github.com/mlflow/mlflow) | Convenience experiment tracking. | **Optional presentation/provenance helper**; export immutable manifests into UKG. | An MLflow run is not a gate receipt or an integrity authority. |
| Manus API v2 | Controlled external task orchestration. | **Optional**, attached as provenance only. | Agent output does not become verified evidence by itself. [3] |

## 9. Initial implementation sequence

1. Implement strict JSON schemas for the eight domain objects and write positive, negative, malformed, and one-field-tamper fixtures.
2. Build the local Experiment Registry with append-only event records and the state-machine allowlist.
3. Wrap the current hierarchy script as an IER baseline job with a pinned input manifest and bounded resource policy.
4. Implement the eight code-owned gate predicates as pure local functions and test that unknown predicates/callbacks fail closed.
5. Add a simple read-only dashboard view that separates candidate-reported metrics from independently recomputed metrics and from review decision.
6. Add reviewer signatures/identity policy only after local receipt behavior and tamper fixtures are stable.
7. Evaluate one exact legacy mathematics adapter proposal, beginning with representation and fixture design—not theory-level language.

## 10. Acceptance criteria

The first feedback-loop release is ready for internal research use only when: every core object canonicalizes deterministically; altered manifest/data/code artifacts fail integrity; an LRR cannot transition an experiment beyond `candidate_reported`; an IER rerun changes neither frozen inputs nor baseline definitions; missing baseline/holdout/review evidence blocks promotion; the dashboard visibly distinguishes `reported`, `independently_evaluated`, and `admitted_experimental`; and the complete experiment can be recreated from manifests with no network access after data retrieval.

## References

[1]: file:///home/ubuntu/sovereign_engine/sov_evidence_geometry_core/__init__.py "Current isolated core package exports"
[2]: file:///home/ubuntu/sovereign_engine/artifacts/hierarchy_recovery_v0/EXPERIMENT_REPORT.md "Hierarchy-Recovery Experiment v0"
[3]: file:///home/ubuntu/skills/manus-api/SKILL.md "Manus API Integration Guide"
