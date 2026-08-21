# Remaining Subsystem Specification Catalog v0.1

**Status:** Proposed architecture catalog.  
**Principle:** Each subsystem is an adapter around, not an owner of, Core Contract semantics. No component below may cause a core predicate to return `verified` without the core’s registered evaluator and evidence record.

## 1. Subsystem contracts

| ID | Subsystem | Purpose | Owns | Explicitly does not own | Entrance gate | Exit gate |
|---|---|---|---|---|---|---|
| S1 | Core SDK/reference interpreter | Canonical IDs, schemas, semantic validation, small invariant registry | Core bytes, typed errors, local evaluation | Network, persistence, keys, GU physical semantics | Core Contract accepted | 17 fixture pack + Python/Rust parity plan |
| S2 | Evidence persistence | Local-first immutable-object storage and query index | Atomic write/read, manifest, garbage-collection policy | Object identity, mutable overwrite, distributed replication | S1 fixture IDs frozen | Offline replay after clean restore |
| S3 | Audit trail | Attest/commit evidence references over time | Events, DSSE envelopes, checkpoints, proof verification | Predicate evaluation, consensus, truth claims | S1 + key/threat policy | Inclusion/consistency/tamper suite |
| S4 | Quorum verification | Aggregate independently signed responses | Request/response equivalence, threshold decision | P2P, leader election, result mutation | S3 fixture signing profile | `2-of-3` offline test suite + incident simulation |
| S5 | Claim and hypothesis graph | Bind claims to source, assumptions, evidence, falsifier, lifecycle | Claim status, promotion records, source authority | Rewriting source semantics or elevating GU claims | Research-quarantine policy accepted | Every displayed claim has source/falsifier/limitations |
| S6 | Registry and version governance | Compile/register operations, predicates, conventions, schemas | Version manifest, compatibility checks, deprecations | Dynamic plugins/callbacks | S1 | Unknown IDs fail closed; upgrade/migration fixtures |
| S7 | API/CLI/SDK transport | Local user-facing operations over core | Request envelopes, generated client compatibility, auth adapter boundaries | Semantic defaults, public service operation | S1, OpenAPI reconciliation | Contract-test and generated-client CI |
| S8 | Logos and explanation adapter | Render evidence in plain language | Explanation templates, audience views, citations | Executing code, creating truth/evidence | S1 + S5 | Explanation-to-evidence trace every time |
| S9 | Monad/runtime state adapter | Coordinate long-running workflows outside core | Job state, retry policy, adapter execution logs | Core registry mutation or implicit evaluator selection | S1, S2 | Crash/replay/idempotency suite |
| S10 | Dashboard/product views | Inspect program, claims, and evidence | UI projection and filters | Source-of-truth authority | S5, S7 | Every UI status links to source evidence |
| S11 | Release/evidence operations | Build, test, SBOM, attestation, release decision | Release packet, policy checkpoints, rollback | Changing core output after sign-off | S1 + S3 | Clean-install and release-replay gates |
| S12 | Connector/control plane | Run bounded research, ingestion, and audit workflows | Least-privilege task envelopes, provenance | Unreviewed source promotion, dynamic credential handling | S5, data/threat policy | Capability denial and audit trace tests |

## 2. Evidence persistence specification

The v0.1 persistence implementation is local-first. The immutable object store has three layers: `objects/<prefix>/<content-id>.json` for canonical objects, `attachments/<sha256>` for nonsemantic source/derived bytes, and a replaceable local SQLite index for lookup only. An index loss must be recoverable from object manifests; an object loss must be detectable through manifest/replay verification.

| Requirement | Contract |
|---|---|
| Write path | Validate → derive ID → write temp file → fsync file → rename atomically → append manifest entry → fsync manifest directory where supported |
| Collision | Same ID + same bytes is idempotent; same ID + different bytes is `E_ID_MISMATCH` and security incident |
| Mutability | Canonical object bytes never overwritten; labels/notes live in a separate mutable envelope keyed by object ID |
| Retention | Core evidence and audit attachments use policy-governed retention; source classification determines local/export access |
| GC | Disabled by default; only orphan attachments with no manifest reference may be removed after a signed/recorded retention decision |
| Backup/restore | Export manifest plus object/attachment hashes; restore must reproduce manifest root and replay selected evidence |

## 3. Claim graph and source authority specification

The claim graph uses immutable claim revisions. Each revision has `claim_id`, statement, level, source references, authority tier, assumptions, evidence IDs, falsifier, lifecycle, limitations, and reviewer/promotion record. Claim transitions are controlled by the research-quarantine policy; a UI must never collapse `supported_bounded` into an unqualified “true.”

## 4. Registry and compatibility specification

Registry entries are compiled or reviewed static artifacts. Each entry requires: operation/predicate ID; semantic version; input kinds; output kinds; convention and scalar policies; required assumptions; deterministic flag; resource ceiling; implementation release; fixture IDs; and deprecation/migration data. Compatibility is checked at request validation; unknown or incompatible IDs return `unverifiable`/typed error. Dynamic imports, URL plugins, and unpinned package resolvers are prohibited.

## 5. API/CLI and adapter specification

The default interface is local CLI and Python SDK. A future service is a thin transport adapter around the same schemas; it must not accept free-form executable expressions or silently inject a convention, assumption, source, or tolerance. The OpenAPI contract remains a design artifact until Core Contract schemas, error mapping, threat model, rate/size limits, and client compatibility tests are accepted.

Logos receives read-only evidence bundles and may generate an explanation only when every statement is linked to source/evidence IDs. Monad receives explicit request IDs and idempotency keys; it may schedule/retry adapters but cannot alter an input/output ID, registry manifest, policy, or verdict.

## 6. Operations, observability, and release specification

| Surface | Minimum requirement |
|---|---|
| CI | Isolated jobs: format/lint, SDK unit/fixtures, schema/compatibility, formal-reference audit, integration smoke, advisory experiments |
| Release packet | Source revision, lock/toolchain digest, fixture results, SBOM, known limitations, policy versions, approver identity, rollback target |
| Metrics | Nonsemantic counters/timings only: request count, status counts, evaluator duration, cache hit, proof verification result; never hash unredacted source text into metrics |
| Logs | Structured, redacted, request/evidence IDs; no private keys, source payloads, or credentials |
| Incident | P0 for canonical-byte divergence, ID collision, signed equivocation, key compromise, or unauthorized policy mutation; freeze promotion and preserve evidence |
| Change control | Contract/registry/canonical-byte change requires ADR, compatibility assessment, migration test vectors, and clean-install replay |

## 7. Dependency order

`S1 → S2 → S3 → S4` is the trust path. `S5` proceeds alongside S1 but stays quarantined from core semantics. `S6` is required before S7–S12 become production-facing. S8–S10 are evidence-reading adapters; S11–S12 must prove they cannot bypass S1/S3.
