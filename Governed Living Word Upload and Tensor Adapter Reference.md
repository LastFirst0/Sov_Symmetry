# Governed Living Word Upload and Tensor Adapter Reference

## 1. Server storage wrapper for governed corpus intake

The dashboard should add a **server-only** wrapper around the platform storage primitive rather than exposing storage credentials or raw object paths to the browser. The browser may submit selected file bytes to a protected endpoint, but the server must authorize the request, validate the declared corpus role and content structure, calculate the content digest, store bytes under a server-generated key, and record only the object reference and metadata in the database. Uploading a file is a **source-intake operation**, not a verification verdict or publication event.

| Layer | Responsibility | Must not do |
|---|---|---|
| Browser upload panel | Select one approved JSON file, show declared corpus role, display local size/digest preview, and submit to the protected route | Decide that a source is valid evidence or publish it |
| Protected server procedure | Verify owner authority, cap size, parse JSON, run structural gate, hash bytes, assign a collision-resistant object key, call `storagePut`, and create an immutable intake record | Trust a client-provided filename, digest, verdict, or source URL |
| Object storage | Retain source bytes using the returned key and `/manus-storage/…` URL | Store reviewer decisions or private keys |
| Database | Persist source role, original filename, object key/URL, SHA-256, byte length, validation report, uploader, timestamp, and review/publication linkage | Store the full 9–19 MB JSON payload in a table |
| Publication workflow | Require the existing independent-review and owner-publish gates before a source metadata record becomes public | Re-run, reinterpret, or promote a corpus test result as a research conclusion |

### Recommended durable record

Add a `corpus_source_intakes` table with the following fields. This is separate from `researchArtifacts`, because the record describes a supplied data source and a mechanical validation run rather than a scientific finding.

| Field | Type / rule | Purpose |
|---|---|---|
| `id` | generated primary key | Stable record identity |
| `source_role` | enum: `genesis_oshb`, `john_sblgnt` | Prevents arbitrary corpus substitution |
| `original_filename` | bounded text | User-visible provenance |
| `storage_key`, `storage_url` | non-null text | Server-generated object reference |
| `sha256` | 64 lowercase hex characters | Exact-byte integrity identity |
| `byte_length` | positive integer | Upload-boundary audit |
| `validation_status` | `accepted`, `rejected`, `unavailable` | Mechanical gate state only |
| `validation_report_json` | JSON | Word count, sampled schema checks, error code, validator version |
| `uploaded_by`, `uploaded_at` | immutable actor/time | Intake audit trail |
| `publication_request_key` | nullable foreign key | Existing review-gate linkage |

### Minimal server API shape

The preferred transport is an authenticated `multipart/form-data` server route such as `POST /api/corpus-sources/intake`, because browser `File` objects are not appropriate tRPC inputs. It should use the same owner-token/authentication rule as current staging operations, then use a narrow server helper:

```ts
// server/corpusStorage.ts
import { createHash, randomUUID } from "node:crypto";
import { storagePut } from "./storage";

export async function storeValidatedCorpusSource(input: {
  sourceRole: "genesis_oshb" | "john_sblgnt";
  originalFilename: string;
  bytes: Buffer;
  validatedReport: Record<string, unknown>;
}) {
  const sha256 = createHash("sha256").update(input.bytes).digest("hex");
  const key = `governed-corpus/${input.sourceRole}/${sha256}-${randomUUID()}.json`;
  const stored = await storagePut(key, input.bytes, "application/json");
  return { ...stored, sha256, byteLength: input.bytes.byteLength };
}
```

The wrapper needs a local `server/storage.ts` implementation that exports `storagePut`. It should call the platform-managed object-storage service using only injected server credentials and return `{ key, url }`; it must never expose the injected credential to React. The generated `url` should be stored exactly as returned, normally `/manus-storage/{key}`.

The protected route should follow this sequence:

1. Authenticate the request and enforce the existing owner-only intake policy.
2. Reject more than one file, non-JSON MIME types, empty payloads, and a fixed size ceiling before parsing.
3. Accept only the two declared roles and verify the role/file-name pair. Do not infer a role from arbitrary content.
4. Parse JSON as a top-level array and validate the same required word/letter fields, URI grammar, language segment, word-count floor, sampled URI-field consistency, and full surface/letter-length consistency used by `tests/test_living_word.py`.
5. Hash the exact received bytes using SHA-256; do not trust a client-side digest.
6. Store bytes only after validation succeeds. Persist the source-intake metadata and an immutable audit event in one database transaction after storage returns successfully.
7. Return the storage URL, digest, validation report, and an explicit statement that **acceptance only means the file met the declared source schema**.
8. Optionally create a staged `researchArtifact` pointing to that source URL. It remains unpublished until the already-required independent reviewer approvals and owner publication action occur.

Validation must fail closed. A malformed source, unrecognized role, duplicate conflict, unavailable storage operation, or database-write failure must return an error and must not create a public source record. A storage object that cannot be linked to an audited database record should be treated as unreferenced and unavailable to the archive UI.

## 2. Living Word validation: 15 passing tests

The supplied sources were copied to the legacy runtime’s expected paths:

| Source role | Expected runtime path | SHA-256 | Result |
|---|---|---|---|
| Genesis OSHB | `data/living_word/Genesis_OSHB.json` | `ddadbb315bb13fcca64ebfabaeb3006fc5294cda50676db1d570c7f6cd8de7ef` | 6/6 source tests passed |
| John SBLGNT | `data/living_word/John_SBLGNT.json` | `ad93149058a0570a9c3917c62c53159619daf04cfa172036efdc52df457372ea` | 6/6 source tests passed |
| Sovereign URI protocol | Code-only protocol checks | n/a | 3/3 tests passed |

`pytest -q tests/test_living_word.py` completed with **15 passed in 0.81 seconds**. These are structural and provenance-format checks; they do not assert theological, historical, semantic, clinical, or empirical conclusions.

| Test group | Exact test | What passed |
|---|---|---|
| Genesis OSHB | `test_file_exists` | Expected corpus file was present |
| Genesis OSHB | `test_is_valid_json` | File parsed as UTF-8 JSON |
| Genesis OSHB | `test_minimum_word_count` | Sequence met the conservative 8,086-word floor |
| Genesis OSHB | `test_structure_and_uris` | Required fields, sampled `sov://` word/letter URI grammar, Hebrew URI segment, non-empty surfaces, positive coordinates, letters, full surface/letter-length consistency, and sampled URI coordinate consistency held |
| Genesis OSHB | `test_first_word_bereshit` | First record was Genesis 1:1 word 1 and surface contained a required Hebrew root character |
| Genesis OSHB | `test_no_empty_surfaces` | No blank surface strings occurred |
| John SBLGNT | `test_file_exists` | Expected corpus file was present |
| John SBLGNT | `test_is_valid_json` | File parsed as UTF-8 JSON |
| John SBLGNT | `test_minimum_word_count` | Sequence met the 15,438-word floor |
| John SBLGNT | `test_structure_and_uris` | Required fields, sampled URI grammar, Greek URI segment, non-empty surfaces, positive coordinates, letters, full surface/letter-length consistency, and sampled URI coordinate consistency held |
| John SBLGNT | `test_first_word_en` | First record was John 1:1 word 1 and surface contained Greek epsilon or nu |
| John SBLGNT | `test_no_empty_surfaces` | No blank surface strings occurred |
| Sovereign Protocol | `test_text_uri_roundtrip` | A Hebrew text URI constructed and parsed back to the declared chapter and verse |
| Sovereign Protocol | `test_letter_uri_roundtrip` | A Greek letter URI constructed and parsed back to its declared chapter and letter index |
| Sovereign Protocol | `test_fingerprint_determinism` | Repeated SHA-256-style protocol fingerprint generation produced the same 64-character hex value |

## 3. Quarantined rank-three tensor final-index symmetry adapter

`adapt_legacy_runtime_tensor_last_symmetric` is a deliberately narrow translator from an opaque legacy candidate to a universal structural-claim packet. It accepts only a non-empty `candidate_id` and a declared finite `tensor` payload. It does **not** import a legacy model, evaluate legacy runtime logic, accept a legacy conclusion, or claim that the tensor represents a physical field.

```text
legacy candidate
  { candidate_id, tensor }
          |
          v
quarantined adapter
  validates only presence/basic container boundary
  emits a neutral packet with framework provenance
          |
          v
universal verifier
  checks T[i,j,k] = T[i,k,j]
  returns verified, fail, or unverifiable
          |
          v
receipt
  exact finite predicate result + mismatch details/scope
```

The adapter emits the supported universal check name `tensor.rank3_last_indices_symmetric.v1`. The universal kernel then calls `check_rank3_last_indices_symmetric`, which requires a finite rank-three numeric tensor where the final two dimensions are equal. It compares every component to its final-index-swapped partner:

> **Predicate:** for every valid `i`, `j`, and `k`, the declared value must satisfy `T[i,j,k] = T[i,k,j]`.

The positive control uses `[[[1, 2], [2, 3]]]`. Here `T[0,0,1] = 2` and `T[0,1,0] = 2`, so the receipt has status `verified`. The negative control uses `[[[1, 2], [3, 4]]]`. Here `T[0,0,1] = 2` while `T[0,1,0] = 3`, so the result is `fail`; this confirms the check can reject a close but non-symmetric input.

| Property | Guaranteed | Explicitly not guaranteed |
|---|---|---|
| Packet provenance | The packet identifies `legacy-runtime-quarantined` and a candidate identifier | Identity is not an endorsement of the legacy runtime |
| Structural result | Exact finite comparison of declared tensor values | No coordinate-invariance, field-equation, physical, semantic, or theory-level conclusion |
| Negative control | Asymmetric final indices produce `fail` | Failure does not diagnose why a legacy generator produced the values |
| Malformed input | Non-rank-three/non-numeric/non-square final axes produce `unverifiable` | Unverifiable does not imply falsehood |

This division is the quarantine: the legacy runtime may generate a candidate; the adapter reduces it to a small, declared, replayable finite predicate; the universal kernel determines only whether that predicate holds on those supplied values.
