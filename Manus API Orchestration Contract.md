# Manus API Orchestration Contract

## Architecture position

Manus API v2 is the program control plane for bounded work packages. It does not become the authoritative store for canonical mathematical objects, evidence cores, or physical claims. The authoritative state remains the versioned repository, the evidence ledger, and the approved project source set.

## Durable entities

| Entity | Role | Required controls |
|---|---|---|
| Project | Durable program policy, source manifest, style, and reusable work-package instructions | Versioned policy references; no one-off task details |
| Task | Bounded research, design, implementation, test, or review unit | Objective, inputs, constraints, acceptance criteria, structured result |
| File | Source bundle, fixture, evidence report, or review packet | Immutable reference in output; retention and sensitivity declared |
| Webhook | Event delivery for production task state transitions | Signature verification, idempotency, retries, dead-letter record |

## Standard work-package envelope

```json
{
  "schema": "sov.work_package.v1",
  "program": "Sovereign Engine",
  "workstream": "WS-B",
  "research_id": "R-A01",
  "mode": "implementation_packet",
  "objective": "Implement a bounded fixture or contract",
  "inputs": ["source IDs", "repository paths", "prior evidence IDs"],
  "constraints": ["do not infer missing GU physics", "preserve canonical schema compatibility"],
  "acceptance": ["tests pass", "evidence record emitted", "limitations documented"],
  "human_gate": "code_review",
  "expiry": "YYYY-MM-DD"
}
```

## Standard structured result

```json
{
  "schema": "sov.work_result.v1",
  "status": "verified | fail | unverifiable",
  "summary": "bounded factual result",
  "observed_facts": [],
  "recommendations": [],
  "hypotheses": [],
  "changed_files": [],
  "tests": [],
  "evidence_ids": [],
  "source_ids": [],
  "limitations": [],
  "risks": [],
  "open_obligations": [],
  "decision_effect": "none | ADR required | human gate required",
  "recommended_next_tasks": []
}
```

## State machine and reliability policy

`draft → submitted → running → waiting_for_input | waiting_for_confirmation | completed | failed | stopped` is the expected task lifecycle. Agent questions are answered through continuation messages; externally consequential confirmations use the explicit confirmation path. Production delivery should prefer signed webhooks; polling is allowed only for prototypes and local scripts.

Every event consumer must deduplicate by event ID or immutable task/output identity, log retry count, record failed events in a dead-letter queue, and preserve the last known terminal state. Any missing structured result, invalid schema, or unverifiable source reference is a failed automation outcome, not a success with empty data.
