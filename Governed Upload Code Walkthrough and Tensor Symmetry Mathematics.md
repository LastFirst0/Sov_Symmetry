# Governed Upload Code Walkthrough and Tensor Symmetry Mathematics

## A. Exact governed storage implementation

The implementation should be a **three-part server path**: a small storage wrapper, a pure corpus validator, and an owner-protected multipart route. The browser has no object-store credentials and cannot select the final storage key. The database records source metadata and the validation report, while object storage retains the raw JSON bytes.

### A.1 `server/storage.ts`: the only storage boundary

This module centralizes the platform request. The exact transport URL can be set from the injected forge environment; its important contract is that it accepts server-side bytes and returns the provider-issued `{ key, url }` pair. No React file imports this module.

```ts
// server/storage.ts
import { env } from "./_core/env";

export type StoredObject = { key: string; url: string };

export async function storagePut(
  key: string,
  bytes: Uint8Array,
  contentType: string,
): Promise<StoredObject> {
  const response = await fetch(`${env.BUILT_IN_FORGE_API_URL}/storage/objects`, {
    method: "PUT",
    headers: {
      Authorization: `Bearer ${env.BUILT_IN_FORGE_API_KEY}`,
      "Content-Type": contentType,
      "X-Storage-Key": key,
    },
    body: bytes,
  });
  if (!response.ok) throw new Error("E_STORAGE_PUT_FAILED");
  const body = (await response.json()) as { key?: unknown; url?: unknown };
  if (typeof body.key !== "string" || typeof body.url !== "string") {
    throw new Error("E_STORAGE_RESPONSE_INVALID");
  }
  return { key: body.key, url: body.url };
}
```

> The deployment-specific storage endpoint shape must be confirmed against the configured platform helper before coding. If the platform exposes `storagePut` directly—as its project guidance indicates—the wrapper should import that helper rather than recreate the HTTP request. The boundary and return contract above remain the same.

### A.2 `server/livingWordValidation.ts`: pure, replayable source gate

This module should share the production acceptance logic with the test suite. It returns a report; it does not determine a research verdict.

```ts
import { createHash } from "node:crypto";

export type CorpusRole = "genesis_oshb" | "john_sblgnt";
const rules = {
  genesis_oshb: { language: "hebrew", book: "genesis", minWords: 8086 },
  john_sblgnt: { language: "greek", book: "john", minWords: 15438 },
} as const;

const wordUri = /^sov:\/\/text\/(hebrew|greek)\/[a-z]+\/[a-z]+\/\d+\/\d+\/w\d+$/;
const letterUri = /^sov:\/\/text\/(hebrew|greek)\/[a-z]+\/[a-z]+\/\d+\/\d+\/w\d+\/l\d+$/;

export function validateLivingWordBytes(role: CorpusRole, bytes: Buffer) {
  const rule = rules[role];
  const sha256 = createHash("sha256").update(bytes).digest("hex");
  let sequence: unknown;
  try { sequence = JSON.parse(bytes.toString("utf8")); }
  catch { return { status: "rejected" as const, code: "E_CORPUS_JSON_INVALID", sha256 }; }
  if (!Array.isArray(sequence) || sequence.length < rule.minWords) {
    return { status: "rejected" as const, code: "E_CORPUS_WORD_COUNT", sha256 };
  }
  for (let n = 0; n < sequence.length; n += 100) {
    const word = sequence[n] as Record<string, unknown>;
    if (!word || typeof word.word_uri !== "string" || !wordUri.test(word.word_uri)
      || !word.word_uri.includes(`/${rule.language}/`) || typeof word.surface !== "string"
      || !word.surface || !Number.isInteger(word.chapter) || (word.chapter as number) < 1
      || !Number.isInteger(word.verse) || (word.verse as number) < 1
      || !Number.isInteger(word.word_index) || (word.word_index as number) < 1
      || !Array.isArray(word.letters) || word.letters.length === 0) {
      return { status: "rejected" as const, code: "E_CORPUS_WORD_SCHEMA", index: n, sha256 };
    }
    for (const letter of word.letters as Record<string, unknown>[]) {
      if (typeof letter.letter_uri !== "string" || !letterUri.test(letter.letter_uri)
        || typeof letter.char !== "string" || [...letter.char].length !== 1) {
        return { status: "rejected" as const, code: "E_CORPUS_LETTER_SCHEMA", index: n, sha256 };
      }
    }
  }
  for (let n = 0; n < sequence.length; n++) {
    const word = sequence[n] as { surface: string; letters: unknown[] };
    if ([...word.surface].length !== word.letters.length) {
      return { status: "rejected" as const, code: "E_CORPUS_SURFACE_LETTER_MISMATCH", index: n, sha256 };
    }
  }
  return { status: "accepted" as const, sha256, wordCount: sequence.length, validator: "living-word.v1" };
}
```

**Unicode note.** The legacy test uses Python `len`, while TypeScript’s `string.length` counts UTF-16 code units. The implementation uses `[...surface].length` to count Unicode code points consistently for the supplied Hebrew and Greek strings. Before replacing the legacy test, the team should formalize whether combining marks are intended to count as separate letters; the provided source files do so, and the test validates exactly that representation.

### A.3 `server/corpusRoutes.ts`: owner-only multipart intake

```ts
import { createHash, randomUUID } from "node:crypto";
import { storagePut } from "./storage";
import { validateLivingWordBytes, type CorpusRole } from "./livingWordValidation";
import { isAuthorizedOwnerToken, insertCorpusSourceIntake } from "./db";

const MAX_CORPUS_BYTES = 25 * 1024 * 1024;
const roles = new Set<CorpusRole>(["genesis_oshb", "john_sblgnt"]);

export async function intakeCorpusSource(request: Request) {
  const token = request.headers.get("x-sovereign-ingestion-token");
  if (!isAuthorizedOwnerToken(token)) return Response.json({ code: "E_FORBIDDEN" }, { status: 403 });
  const form = await request.formData();
  const role = form.get("sourceRole");
  const file = form.get("file");
  if (typeof role !== "string" || !roles.has(role as CorpusRole) || !(file instanceof File)) {
    return Response.json({ code: "E_UPLOAD_INPUT_INVALID" }, { status: 400 });
  }
  if (file.type !== "application/json" || file.size === 0 || file.size > MAX_CORPUS_BYTES) {
    return Response.json({ code: "E_UPLOAD_MEDIA_OR_SIZE" }, { status: 400 });
  }
  const bytes = Buffer.from(await file.arrayBuffer());
  const report = validateLivingWordBytes(role as CorpusRole, bytes);
  if (report.status !== "accepted") return Response.json({ report }, { status: 422 });

  const sha256 = createHash("sha256").update(bytes).digest("hex");
  const key = `governed-corpus/${role}/${sha256}-${randomUUID()}.json`;
  const stored = await storagePut(key, bytes, "application/json");
  const record = await insertCorpusSourceIntake({
    sourceRole: role as CorpusRole, originalFilename: file.name, storageKey: stored.key,
    storageUrl: stored.url, sha256, byteLength: bytes.byteLength,
    validationStatus: "accepted", validationReport: report,
  });
  return Response.json({ intake: record, publicationState: "source_accepted_not_published" }, { status: 201 });
}
```

The calling browser flow is: file selection → explicit role selection → request submission → report display → optional existing **stage-for-review** action. It must never automatically turn `accepted` into `verified`, publish the source, or silently overwrite an earlier source record.

## B. Failure modes and edge cases covered by the 15/15 suite

The passing suite uses affirmative fixtures, so it proves these constraints held for the supplied files. It does **not** include separately named mutation tests for every failure code. The following table distinguishes actual enforced conditions from recommended new negative tests for the upload validator.

| Current test / assertion | Failure or edge condition it catches if violated | What passed for supplied sources |
|---|---|---|
| `test_file_exists` (both sources) | Missing expected file | Both corpus files existed in `data/living_word/` |
| `test_is_valid_json` | Invalid JSON / unreadable UTF-8 | Both parsed successfully |
| `test_minimum_word_count` | Truncated or wrong corpus | Genesis met ≥8,086; John met ≥15,438 |
| `test_structure_and_uris` | Missing `word_uri`, surface, chapter, verse, word index, or letters | Required word records occurred in sampled positions |
| `test_structure_and_uris` | Word URI malformed, wrong grammar, or wrong language segment | Sampled Hebrew and Greek URIs matched required structure |
| `test_structure_and_uris` | Empty surface / zero or non-integer coordinates | Sampled records were nonempty and positive-integer addressed |
| `test_structure_and_uris` | Missing/malformed letter URI or non-single-character letter | Sampled letter records passed required fields and URI grammar |
| `test_structure_and_uris` | Surface/letter count mismatch anywhere in a corpus | Entire corpus held the exact legacy representation count invariant |
| `test_structure_and_uris` | URI chapter/verse differs from declared field | Sampled every-500th URI agreed with fields |
| `test_first_word_bereshit` | Wrong source ordering, start location, or implausible Genesis opening | Genesis began chapter 1, verse 1, word 1 with a required root character |
| `test_first_word_en` | Wrong source ordering, start location, or implausible John opening | John began chapter 1, verse 1, word 1 with epsilon or nu |
| `test_no_empty_surfaces` | A blank surface anywhere outside the sample | No blank surface strings in either entire corpus |
| `test_text_uri_roundtrip` | Protocol creator/parser disagreement on Hebrew text URI | Constructed URI parsed to the original chapter/verse |
| `test_letter_uri_roundtrip` | Protocol creator/parser disagreement on Greek letter URI | Constructed URI parsed to original chapter/letter index |
| `test_fingerprint_determinism` | Nondeterministic source-URI fingerprint | Same URI gave the same 64-character hex digest twice |

### Recommended new negative upload tests

The governed intake feature should add these tests before release: unauthorized owner token; omitted role; unsupported role; two files; filename/role mismatch; empty, oversized, malformed, or non-JSON file; top-level object rather than array; threshold-minus-one word count; a missing required field; invalid language segment; malformed word/letter URI; empty letters; non-string or multi-code-point letter; negative, zero, or non-integer coordinate; a full-corpus surface/letter mismatch; URI/field coordinate mismatch; duplicate same-digest behavior; storage failure; invalid storage response; database failure after storage; and an assertion that a rejected upload creates neither a published artifact nor a source-intake record.

## C. Mathematical formulation: rank-three final-index symmetry

Let `T` be a finite rank-three array with shape `(d₀, n, n)`. Its components are written

\[
T_{i j k}, \quad 0 \le i < d_0,\; 0 \le j,k < n.
\]

The universal predicate is **symmetry in the final two indices**:

\[
\forall i,j,k:\quad T_{i j k} = T_{i k j}.
\]

For each fixed first index `i`, the `n × n` slice `T_i` must be a symmetric matrix. The first axis is not permuted, and no claim is made about symmetry involving it. This is weaker than full permutation symmetry of all three indices.

The code tests only one triangle of each slice:

\[
\forall i,\; 0 \le j < k < n:\quad T_{i j k} = T_{i k j}.
\]

Diagonal terms `T_{i j j}` require no separate comparison because swapping the final indices leaves them unchanged. A violation produces a mismatch witness containing both coordinates and values. For the negative control

\[
T_0 = \begin{bmatrix} 1 & 2 \\ 3 & 4 \end{bmatrix},
\]

the required equality would be `T_{0,0,1} = T_{0,1,0}`, but `2 ≠ 3`, so the status is `fail`. For the positive control

\[
T_0 = \begin{bmatrix}1 & 2 \\ 2 & 3\end{bmatrix},
\]

the sole off-diagonal pair agrees, so the status is `verified`.

The predicate returns `unverifiable` rather than `fail` when the input is empty, not rank three, ragged, has unequal final dimensions, contains booleans, contains non-numeric values, or contains non-finite float values such as `NaN` or infinity. These are malformed/inadequate inputs, not counterexamples to a defined predicate.

The adapter only packages the tensor under `tensor.rank3_last_indices_symmetric.v1` and adds provenance identifying the legacy candidate. The mathematical check itself happens in the universal kernel. Therefore, a verified receipt means only that the supplied finite components satisfy the displayed equality; it does not establish a physical tensor field, coordinate invariance, a legacy-runtime conclusion, or any theory-level proposition.
