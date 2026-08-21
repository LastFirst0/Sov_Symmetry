# Kernel Clarity Audit and Product Model

## The simple purpose

The kernel should answer a concrete question in a reproducible way:

> “Given these declared inputs, does this named check hold, fail, or lack enough information—and what exact evidence supports that answer?”

It is **not** a machine for declaring a worldview, solving every mathematical problem, or turning incomplete ideas into certainty.

## Keep, simplify, or move out of the public surface

| Current idea | Decision | Plain-language form | Reason |
|---|---|---|---|
| Deterministic input and receipt ID | Keep | “The same input gives the same receipt.” | Makes results replayable and exposes changes. |
| `verified` / `fail` / `unverifiable` | Keep, translate | “holds in this check” / “does not hold” / “cannot be checked yet” | These are three useful, non-mystical terminal states. |
| Canonical JSON and scalar policy | Keep internally | “The system uses one stable representation before hashing.” | Necessary for replay; not a front-door concept. |
| 17-case fixture distribution | Keep in release evidence | “The release is checked against a published test pack.” | Valuable engineering evidence, not user workflow. |
| DSSE, Ed25519, quorum, Merkle | Move to assurance layer | “Who signed or witnessed this receipt?” | Valuable when sharing/handing off receipts, not required for a first check. |
| Long negative lists / “must not” language | Replace in public guide | “Not supported yet; here is the next useful action.” | Avoids defensive vagueness while staying honest. |
| GU physics language | Keep in research layer | “Hypothesis, not a kernel result.” | Prevents a small check from being misread as a scientific verdict. |

## Public kernel model

| Step | What a person supplies or sees | Kernel behavior | Useful result |
|---|---|---|---|
| 1. Ask | A named check and concrete declared input | Selects a code-owned check | “Check whether this matrix is symmetric.” |
| 2. Check | Exact values and declared conventions where needed | Evaluates one bounded predicate | No hidden assumptions or callbacks. |
| 3. Receive | A readable receipt | Creates a stable receipt ID and records outcome | Status, explanation, mismatches, and scope. |
| 4. Decide | The receipt plus context | Leaves the human to act or request a stronger check | “Fix entries [0,1] and [1,0]” or “supply a missing assumption.” |

## First practical interface

`check_symmetric_matrix([[1,2],[2,4]])` returns a receipt that says what was checked, whether it held, why, the exact mismatches if any, a stable ID, a next action, and an explicit scope boundary. This is a model for future checks: **one question, one predicate, one receipt, one next action**.

## Essential release scope

The usable offline kernel release should include: deterministic receipts; a small published set of checks; readable result mapping; fixture/replay tests; optional provenance/audit attachments; and a clear library/CLI API. Ed25519, quorum, and Merkle proofs should remain optional assurance modules until a user needs shared or adversarial handoff evidence.

## Release checklist

- [ ] At least three useful checks are exposed through the same receipt pattern.
- [ ] Every check explains its input requirements, result, mismatch/residual, scope, and next action.
- [ ] Stable receipt replay and one-character tamper rejection pass.
- [ ] Public examples run without legacy-repository imports.
- [ ] Audit/signature/quorum modules are optional attachments, not prerequisites for ordinary use.
- [ ] Documentation uses plain meanings first and implementation labels second.
