# Empirical Claim Packet Specification v0.1

## Purpose and boundary

An empirical claim packet records **what was measured or observed**, **where the data came from**, **how it was transformed**, **how uncertainty was represented**, and **which external method may analyze it**. It does not allow the deterministic structural kernel to pronounce an empirical claim `verified`. Until a separately admitted empirical analysis process is run, the kernel returns `unverifiable` with an explanation of the missing process.

This design borrows the separation of entities, activities, agents, derivations, and bundles from W3C PROV, while retaining a compact JSON contract.[1] It also targets FAIR-aligned identifier, metadata, access, license, provenance, and community-standard practices without claiming FAIR certification.[2] Measurement packets require explicit uncertainty components, methods, coverage information, and the basis of any confidence statement, consistent with NIST reporting guidance.[3]

## Packet envelope

```json
{
  "schema": "sov.empirical_claim_packet",
  "schema_version": "0.1.0",
  "packet_id": "empirical:example:0001",
  "claim_id": "claim:example:effect",
  "claim_class": "empirical",
  "framework_id": "framework:provenance-only",
  "statement": "Human-readable empirical statement, not a kernel verdict.",
  "target_quantity": {},
  "datasets": [],
  "provenance": {},
  "uncertainty": {},
  "analysis_binding": {},
  "governance": {},
  "non_claims": []
}
```

`framework_id` is optional provenance and MUST NOT select the analytic method, decision threshold, or receipt status. A packet must be self-describing enough to replay identity and lineage checks even if a data payload is access-controlled or unavailable.

## Required fields

| Field | Required content | Validation rule |
|---|---|---|
| `packet_id` | Stable, globally unique packet identifier | Immutable after publication. |
| `claim_id` | Stable identifier for the bounded empirical question | Must not encode a theory-level conclusion. |
| `statement` | Plain-language observation/question | Must distinguish measurement from interpretation. |
| `target_quantity` | Name, symbol, unit, domain, population/time scope | Unit/scale and scope must be stated. |
| `datasets` | One or more versioned data entity descriptors | Every descriptor has identifier, content hash or stated hash absence, version, owner/custodian, access status, and license. |
| `provenance` | Entity/activity/agent/derivation lineage | Each transform cites software/method version, parameters, time, and responsible agent or organization. |
| `uncertainty` | Measurement or model uncertainty representation | Method, components, combination rule, and interpretation basis must be explicit. |
| `analysis_binding` | External statistical/model method reference | Must name method version, executable or protocol ID, input mapping, and predeclared output type. |
| `governance` | Ethics/access/retention/review records as applicable | Missing/unknown information must be declared, never inferred. |
| `non_claims` | Explicit statements the packet cannot establish | Must include no automatic theory validation. |

## Dataset descriptor

```json
{
  "dataset_id": "doi-or-content-address",
  "version": "2026-08-18",
  "content_sha256": "hex-or-null-with-reason",
  "media_type": "text/csv",
  "schema_ref": "schema:example.v1",
  "access": {"status": "open|restricted|unavailable", "locator": "uri-or-null", "access_conditions": "text"},
  "license": "SPDX-or-text",
  "custodian": {"id": "org-or-person", "role": "publisher|steward|collector"},
  "collection_window": {"start": "ISO-8601-or-null", "end": "ISO-8601-or-null"},
  "quality_notes": []
}
```

The descriptor is a content identity and provenance statement, not a claim that data are accurate, representative, legal to reuse in all contexts, or sufficient for inference. Metadata must remain available when possible even if data access later changes, consistent with FAIR principle A2.[2]

## Provenance graph

The `provenance` object contains `entities`, `activities`, `agents`, `used`, `generated`, and `derived_from` edges. It follows PROV’s core distinction among data entities, processing activities, responsible agents, and derivations.[1] A transform is never represented merely by a label: it records input IDs, output ID, method/software version, parameters or their hashed reference, timestamp, and execution environment.

## Uncertainty model

```json
{
  "kind": "measurement|sampling|model|mixed|unknown",
  "estimate": {"value": 0.0, "unit": "unit-or-1"},
  "components": [
    {"id": "u1", "class": "statistical|other", "description": "text", "standard_uncertainty": 0.0, "unit": "unit-or-1", "degrees_of_freedom": null}
  ],
  "combination_method": "named-method-or-protocol-ref",
  "combined_standard_uncertainty": {"value": 0.0, "unit": "unit-or-1"},
  "expanded_uncertainty": {"value": 0.0, "unit": "unit-or-1", "coverage_factor": 2.0},
  "interval_or_confidence": {"statement": "optional, with basis", "level": null},
  "assumptions": [],
  "limitations": []
}
```

If a confidence level or interval is stated, the packet must cite its basis; a coverage factor or uncertainty number alone may not be silently interpreted as a probability statement.[3]

## Analysis binding and outcomes

`analysis_binding` names an external process such as a preregistered statistical test, model fit, simulation protocol, or evidence synthesis workflow. It specifies inputs, software/container/version or written protocol, parameter declaration, decision rule if any, output schema, and independent review requirement. The core kernel may validate packet shape, identity, hashes, and provenance references, but it returns `unverifiable` for the empirical statement until an independently versioned analysis receipt is attached.

An empirical analysis receipt MUST distinguish: successful execution, method validity, data limitations, statistical/model output, and interpretation. It MUST NOT collapse a p-value, fit score, posterior, or classifier output into a theory-level `verified` status.

## State machine

| State | Meaning |
|---|---|
| `draft` | Incomplete packet; not eligible for analysis. |
| `described` | Required identity/provenance/uncertainty fields present. |
| `bound` | External method and inputs are frozen. |
| `executed` | An external analysis receipt has been attached. |
| `reviewed` | Independent review record is attached. |
| `withdrawn` | Packet remains identifiable; use is blocked with a reason. |

## Rejection and quarantine conditions

The packet is rejected or quarantined if it lacks immutable data identity, hides a transformation, supplies a confidence interpretation without its basis, silently changes access/license status, treats missing uncertainty as zero uncertainty, uses framework provenance as a decision rule, or labels empirical/model output as proof of an entire theory.

## References

[1] [W3C PROV Overview](https://www.w3.org/TR/prov-overview/) and [PROV-DM](https://www.w3.org/TR/prov-dm/).

[2] [GO FAIR: FAIR Principles](https://www.go-fair.org/fair-principles/).

[3] [NIST TN 1297: Reporting Uncertainty](https://www.nist.gov/pml/nist-technical-note-1297/nist-tn-1297-7-reporting-uncertainty).
