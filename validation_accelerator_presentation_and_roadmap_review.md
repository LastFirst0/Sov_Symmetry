# Validation, Accelerator, Presentation, and Roadmap Review

**Review date:** 2026-08-19. This review discusses implemented code and recorded test evidence. It does not convert structural validation, source acceptance, or candidate acceleration into a claim about the meaning or truth of a corpus, theory, organism, or empirical domain.

## 1. Living Word Negative Tests: What They Catch

The source validator exists at `server/livingWordValidation.ts`; the dashboard-side contract tests are in `client/src/livingWordValidation.test.ts`, `client/src/corpusIntake.test.ts`, and `client/src/corpusIntakeFailures.test.ts`. Its role is deliberately narrow: it accepts only one of two **declared source roles**, checks the source bytes against the required structural profile, hashes the original bytes, and returns a source-acceptance report. It neither constructs a research verdict nor publishes an artifact.

| Rejection class | Enforced code | Why it matters | Resulting behavior |
|---|---|---|---|
| Unknown role | `E_CORPUS_ROLE_UNSUPPORTED` | Prevents an arbitrary JSON document being labeled as a recognized corpus. | HTTP 422 before storage. |
| Role/filename mismatch | `E_CORPUS_ROLE_FILENAME_MISMATCH` | Prevents the Greek and Hebrew source profiles from being silently swapped. | HTTP 422 before storage. |
| Empty or oversized bytes | `E_CORPUS_SIZE_INVALID` | Rejects null input and a payload beyond the 25 MB route limit. | HTTP 422 before storage. |
| Non-JSON or non-array root | `E_CORPUS_JSON_INVALID`, `E_CORPUS_TOP_LEVEL_INVALID` | Prevents parser ambiguity and non-sequence data from entering the corpus path. | HTTP 422 before storage. |
| Insufficient word count | `E_CORPUS_WORD_COUNT` | Requires the declared minimum structural length for the selected source profile. | HTTP 422 before storage. |
| Missing word fields | `E_CORPUS_WORD_SCHEMA` | Prevents partial records from posing as complete source words. | HTTP 422 before storage. |
| Invalid word URI or coordinates | `E_CORPUS_WORD_URI_INVALID`, `E_CORPUS_COORDINATE_INVALID`, `E_CORPUS_URI_COORDINATE_MISMATCH` | Ensures declared identifier and scalar coordinates agree. | HTTP 422 before storage. |
| Invalid letters or surface mismatch | `E_CORPUS_LETTERS_INVALID`, `E_CORPUS_LETTER_URI_INVALID`, `E_CORPUS_LETTER_CHAR_INVALID`, `E_CORPUS_SURFACE_LETTER_MISMATCH` | Ensures a word’s visible surface and declared letter decomposition are structurally coherent. | HTTP 422 before storage. |
| Unauthorized request | `E_FORBIDDEN` | Prevents validation, storage, and metadata creation without owner authorization. | HTTP 403 before parsing. |
| Storage or metadata persistence error | `STORAGE_*`, `DATABASE_UNAVAILABLE` | Keeps a failed operational step from producing a public source record. | HTTP 502 and no accepted intake row. |

The current tests exercise normal acceptance, malformed role/file combinations, malformed JSON and roots, low word count, missing fields, coordinate mismatch, malformed letters, unauthorized calls, presign failure, PUT failure, and database failure. The combined dashboard suite passed **82 tests**, with **2 opt-in live tests skipped**. The independent Python corpus suite passed **15/15** using the supplied source files.

## 2. GPU Tensor Candidate Accelerator

The accelerator at `sov_evidence_geometry_core/tensor_accelerator.py` operates on the declared rank-three final-index symmetry predicate:

\[
T_{i j k} = T_{i k j}
\]

for every in-range triple \((i,j,k)\) in a declared finite tensor. For each fixed first index \(i\), it compares the matrix slice \(T_i\) with its transpose across the final two indices. A vectorized NumPy path can screen this condition on CPU; an optional CuPy path may vectorize the same comparison on a GPU. It can report a candidate mismatch witness such as \((i,j,k,T_{ijk},T_{ikj})\).

The accelerator remains **quarantined**. A candidate success is not a receipt; a candidate mismatch is not automatically a retained failure. Any result intended for evidence retention is re-evaluated by the deterministic universal kernel using `tensor.rank3_last_indices_symmetric.v1`, which emits only `verified`, `fail`, or `unverifiable` under the core contract. The accelerator must return an unavailable candidate state when its optional GPU backend is absent rather than silently treating a changed execution path as equivalent authority.

| Stage | Permitted output | Prohibited output |
|---|---|---|
| Vector candidate screen | Candidate pass/fail/unavailable, mismatch count, candidate witness. | Receipt, admission decision, claim interpretation. |
| Deterministic CPU confirmation | Contract receipt with bounded structural result. | Domain conclusion beyond the declared tensor predicate. |

The updated offline matrix passed **65 Python and 4 Rust** tests. The repaired exploratory legacy root suite passed **770 tests with 65 transparent skips**. Its status remains descriptive of an exploratory repository, not an assurance release.

## 3. Governed Storage Wrapper and Presentation Walkthrough

The implementation introduces `server/storage.ts`, `server/corpusIntake.ts`, the `corpusSourceIntakes` table, and `LivingWordCorpusIntake.tsx`.

1. An owner selects a declared source role and the exact expected JSON filename.
2. The browser sends raw JSON bytes to `/api/corpus-sources/intake` with an ephemeral bearer token. The token is held in page memory only.
3. The Express handler checks authorization before parsing or storage.
4. `validateLivingWordUpload` checks structural form and computes SHA-256 over the original byte stream.
5. `storagePut` requests a server-side managed-storage presigned PUT URL and uploads bytes without exposing platform credentials to the browser.
6. A durable metadata row records the role, filename, managed-storage pointer, SHA-256, byte count, validation report, and owner-token actor label.
7. The response explicitly states that structural acceptance created **no publication, research verdict, or content interpretation**.

The companion deck, *Governed Source Intake & Tensor Symmetry Verification*, uses eleven slides to explain the same boundary: fail-closed intake, corpus structural gate, negative controls, final-index predicate, deterministic witness, quarantine, optional GPU screening, and authority boundary. The companion Markdown script provides the speaking narrative. Slide generation completed successfully; a subsequent archive-page visual review confirmed that the upload control and artifact-driven coverage widget render at desktop width.

**Responsive verification record.** On 2026-08-19, the `/archive` page was reviewed as a full page at **375 × 812** and **1280 × 720**. The governed source-upload control, dedicated `legacy-runtime-tensor-last-symmetric` status card, recorded pass/skip metrics, and existing archive controls rendered at both sizes without an observed overlap or horizontal overflow. The owner-only form remains collapsed until deliberately opened; no source data or token is shown in the review state.

**Presentation QA record.** The slide-state manifest reports all **11 of 11** slides in the `edited` state, covering the full sequence from source-retention decisions through GPU candidate screening and operational close. The script was reconciled with the implemented **raw JSON** owner-gated route, server-generated storage key, durable intake metadata record, and remaining owner-authorized live-upload gate. After all reviewed corrections, the final presentation artifact rendered successfully as `manus-slides://xalxjb9Sxsl3AGFz37iIZ9`.

**Rendered pages 1–2.** The cover rendered its title, bounded-scope statement, tensor notation, and finite-slice visual with no viewport overflow. The three-decision slide rendered all retain/validate/review columns at readable sizes; its source record, accepted/rejected report, and independent review wording align with the updated script.

**Rendered pages 3–4.** The browser-to-storage flow rendered all four stages inside the viewport. QA identified and corrected an overstated separate-audit label: the final stage now describes the implemented **durable intake record**. The fail-closed table was readable with all five gates present; its final row was corrected from audit linkage to **durable intake linkage**, preserving the actual storage-plus-metadata-row boundary.

**Rendered pages 5–6.** The corpus slide displayed the observed **15 / 15 pass, 0 skipped** result, individual 6/6 and 3/3 components, and the non-interpretation boundary without clipping. The negative-contract slide displayed metadata, payload, and structure rejection categories with representative error-code families; it clearly preserves the distinction between structural acceptance, publication, and verification.

**Rendered pages 7–8.** The declared predicate page rendered \(T_{ijk}=T_{ikj}\), its finite \((d_0,n,n)\) domain, mirrored-pair comparison, and explicit non-claims at readable scale. The witness page rendered the asymmetric slice and exact `2 ≠ 3` coordinate witness without suggesting a cause beyond the declared values. Both pages fit the viewport without observed overlap or clipping.

**Rendered pages 9–10.** QA detected text overlap in the original authority-cut/footer area of the quarantine slide. The slide was revised and re-rendered: the four-stage candidate-to-receipt flow, authority cut, adapter permissions, and result scope now clear one another. The GPU page rendered CPU/GPU vector screening, candidate states, deterministic CPU confirmation, and the no-receipt rule without overflow or an implied authority transfer.

**Rendered page 11.** The original close page overstated an audit record and described the storage wrapper as future work. It was corrected and re-rendered to show the implemented durable intake record, the actual next gate of one owner-authorized live managed-storage upload, and the candidate-only GPU boundary. The corrected page fit the viewport without clipping.

**Final page-by-page conclusion.** The corrected fail-closed page was re-rendered and confirmed its five gates, durable-intake-linkage wording, reject/retain states, and source-only boundary are visible without overlap. All eleven final pages were rendered and reviewed. Pages 3, 4, 9, and 11 were corrected where the initial deck overstated audit semantics, described completed work as future work, or contained overlapping text; each correction was re-rendered. The final deck aligns with the corrected Markdown script and contains no observed text clipping or viewport overflow.

## 4. Roadmap Status and Remaining Gates

The implementation now covers the core operational roadmap extension requested for this wave: authentic source installation and structural test enablement; a third legacy tensor adapter; a governed server storage route, database record, UI panel, rejection tests, refreshed ecosystem/research feeds, artifact-driven coverage display, and updated completion assessment.

The remaining gates are operational or deliberately scope-limited. One owner-authorized live managed-storage upload remains necessary to exercise the platform presign credentials end-to-end; it cannot be truthfully simulated without the owner’s token. A third-party external-adapter admission exercise and a second independently operated full-platform replay remain future evidence gates. These are not omitted features disguised as complete; they are explicit conditions for changing the reported completion estimate.

## 5. Owner-Authorized Managed-Storage Intake Exercise

On 2026-08-19, the owner completed a live dashboard upload of `Genesis_OSHB.json`. The server created intake `corpus_mszotx0m_4fccb28d` for declared role `genesis_oshb`. It retained **19,220,561 bytes**, recorded SHA-256 `ddadbb315bb13fcca64ebfabaeb3006fc5294cda50676db1d570c7f6cd8de7ef`, and returned the structural report `{ wordCount: 20630, validator: "living-word-source.v1" }`. The database record points to a server-issued governed-corpus key; a retrieval check returned the expected managed-storage redirect.

The no-promotion boundary was independently checked: no `researchArtifacts` row references this source pointer and no `artifactPublicationRequests` row contains its digest. The completed exercise therefore demonstrates protected retention and durable source metadata, **not** publication, a verification verdict, or an interpretive result.
