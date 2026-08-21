# Governed Source Intake and Tensor Symmetry Verification

**Audience:** research operators, reviewers, and technical stakeholders.  
**Duration:** approximately 10–12 minutes.  
**Core message:** source handling, parallel candidate screening, and deterministic verification have distinct responsibilities; no layer silently promotes its output into a broader claim.

## Cover

**On-slide title:** Governed Source Intake & Tensor Symmetry  
**On-slide subtitle:** From source bytes to a bounded, replayable structural receipt

**Speaker notes:** This presentation concerns a narrow infrastructure question: how a research system should accept a large structured source file, preserve its provenance, and test a declared finite tensor relation. The goal is not to interpret corpus content or to infer a theory. It is to make the operational boundary inspectable and repeatable.

## Slide 1 — One file, three distinct decisions

**On-slide content:**

| Decision | Owner | Output |
|---|---|---|
| Can we retain these bytes? | Governed intake | Source record |
| Does the source match its declared schema? | Validator | Accepted / rejected report |
| Can this source support a research claim? | Review process | Separate review decision |

**Speaker notes:** The most important rule is separation. Storage accepts protected bytes. Validation checks a declared structure. Review examines whether a proposed record is fit for publication. None of those operations are a scientific verdict by themselves.

## Slide 2 — Browser-to-storage boundary

**On-slide content:**

```text
Browser file selection
  → owner-gated raw JSON route
  → byte and JSON validation
  → SHA-256 digest
  → server-generated object key
  → managed object storage
  → durable intake metadata record
```

**Speaker notes:** The browser never receives an object-store credential and never chooses the final key. The server computes the digest from received bytes, validates before storage, then returns the durable intake metadata and a validation report. This protects against client-side path manipulation and unsupported content being treated as an admitted source.

## Slide 3 — Fail closed before retention

**On-slide content:**

| Reject condition | Why it matters |
|---|---|
| Unauthorized owner request | Prevents ungoverned source intake |
| Wrong role, filename, MIME, or size | Prevents source substitution and resource abuse |
| Invalid JSON or wrong top-level form | Prevents opaque/unreadable payloads |
| Invalid words, letters, URIs, coordinates | Preserves declared data grammar |
| Storage or database failure | Avoids an untracked source reference |

**Speaker notes:** Failure should be explicit and non-destructive. A rejected source should not create a public record. A source object without a linked audited record should not appear in the archive. This is why the application distinguishes source acceptance from publication.

## Slide 4 — Corpus gate: what passed

**On-slide content:**

| Dataset | Structural result |
|---|---|
| Genesis OSHB | 6 source tests passed |
| John SBLGNT | 6 source tests passed |
| URI protocol | 3 deterministic tests passed |
| **Total** | **15 / 15 passed** |

**Speaker notes:** These results validate file availability, JSON parseability, conservative word floors, required fields, URI grammar, position fields, non-empty surfaces, letter structure, surface-letter count consistency, opening-record anchors, and URI protocol round trips. They do not establish an interpretive conclusion about the source texts.

## Slide 5 — Negative tests turn the gate into a contract

**On-slide content:**

* Metadata rejects unsupported roles, unsafe filenames, role-file mismatches, and empty payloads.
* Content rejects malformed JSON, a non-array root, insufficient words, invalid URIs, bad coordinates, malformed letters, and full-record count mismatches.
* The new validator suite runs alongside the historical corpus suite.

**Speaker notes:** Positive tests prove supplied sources pass. Negative tests prove the admission boundary actually refuses defined classes of invalid input. The new suite checks the validator’s error codes rather than merely expecting a generic failure, which makes behavior stable for the dashboard and audits.

## Slide 6 — The declared tensor predicate

**On-slide content:**

\[
T_{ijk} = T_{ikj}
\]

For every fixed first index \(i\), the \(j,k\) slice is a symmetric matrix.

**Speaker notes:** This is rank-three symmetry only in the final two index positions. It does not assert symmetry in the first index, full permutation symmetry, a coordinate transformation property, or a physical model. The predicate is exact equality on a finite supplied array.

## Slide 7 — A witness makes failure inspectable

**On-slide content:**

\[
T_0 = \begin{bmatrix}1 & 2\\3 & 4\end{bmatrix}
\]

\[
T_{0,0,1}=2 \ne 3=T_{0,1,0}
\]

**Speaker notes:** The negative control fails because a specific mirrored pair differs. A receipt can record the coordinate pair and both values. This is a useful model of evidence-bounded failure: the system says exactly what finite equality was violated, not why a broader generator produced the values.

## Slide 8 — Quarantine preserves verification authority

**On-slide content:**

```text
Legacy candidate → adapter → neutral structural packet → universal kernel → receipt
```

| Layer | Allowed action | Not allowed |
|---|---|---|
| Legacy runtime | Produce candidate values | Authorize verification |
| Adapter | Package declared finite input | Import legacy conclusions |
| Universal kernel | Evaluate predicate | Establish a theory |

**Speaker notes:** The framework label is provenance, not authority. The adapter cannot transform a legacy conclusion into an accepted truth. It can only package declared input for a universal finite predicate.

## Slide 9 — GPU screening is a speed layer, not a verdict

**On-slide content:**

```text
GPU/CPU vector screen → candidate result → deterministic CPU kernel confirmation → receipt
```

**Speaker notes:** The accelerator evaluates off-diagonal pairs in parallel. It can locate the first mismatch and count mismatches efficiently. Because GPU execution may differ in availability, device state, and numerical path, its result is deliberately labeled candidate-only. Any receipt must be re-evaluated by the deterministic CPU kernel over the declared values.

## Slide 10 — Operational close

**On-slide content:**

**Retain sources safely.**  
**Reject malformed structure explicitly.**  
**Accelerate screening without moving authority.**

**Speaker notes:** The protected storage wrapper and durable corpus-intake table are implemented. The immediate operational gate is one owner-authorized live upload through managed storage. The accelerator remains optional, must return unavailable if no GPU backend exists, and must receive deterministic kernel confirmation before any result appears as a receipt.
