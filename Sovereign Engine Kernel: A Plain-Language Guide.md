# Sovereign Engine Kernel: A Plain-Language Guide

## What it does

The kernel is a **receipt maker for well-defined checks**. You give it a concrete input and a named question. It returns a stable receipt saying whether the check holds, fails, or cannot be evaluated from the information provided.

> A receipt answers one declared question. It does not automatically validate a broader model, intent, theory, or physical claim.

## The four-step workflow

| Step | Human question | Kernel response | What to do next |
|---|---|---|---|
| Ask | “What exactly do I want to check?” | Select one supported check. | Name one concrete predicate. |
| Supply | “What values and context does that check need?” | Validate required input shape. | Correct missing or incompatible input. |
| Receive | “What happened?” | Return a readable receipt and stable ID. | Read the explanation and mismatch list. |
| Decide | “What should I change or share?” | Provide a bounded next action and scope. | Fix the input, ask a stronger check, or attach assurance evidence. |

## The three possible answers

| Kernel status | Plain wording | Meaning |
|---|---|---|
| `verified` | **Holds in this check** | The named predicate held for the supplied input. |
| `fail` | **Does not hold in this check** | The predicate did not hold; the receipt identifies the mismatch. |
| `unverifiable` | **Cannot be checked from this input** | A required condition or supported representation was missing. This is not a failure claim. |

## Worked examples

### 1. Is this matrix symmetric?

```python
from sov_evidence_geometry_core import check_symmetric_matrix
receipt = check_symmetric_matrix([[1, 2], [2, 4]])
```

The question is `Aᵀ = A`. The receipt says **holds in this check** because paired off-diagonal entries match. If the input were `[[1, 3], [2, 4]]`, the receipt would say **does not hold in this check** and point to `[0, 1]` as the mismatch.

### 2. Is this the identity matrix?

```python
from sov_evidence_geometry_core import check_identity_matrix
receipt = check_identity_matrix([[1, 0], [0, 1]])
```

The receipt checks the direct expectation: diagonal entries must be `1`; off-diagonal entries must be `0`.

### 3. Does this inverse candidate work?

```python
from sov_evidence_geometry_core import check_matrix_inverse
receipt = check_matrix_inverse([[2, 0], [0, 3]], [[0.5, 0], [0, 1/3]])
```

The kernel multiplies the declared matrix by the declared inverse candidate and checks whether the product is identity. It exposes the product and any mismatching entries.

## What stays internal unless needed

Canonical JSON, content hashes, fixtures, Rust parity, signatures, quorum, and Merkle proofs are real assurance mechanisms. Most users should see them only when they need to replay, share, or independently audit a receipt. They support the answer; they should not obscure the question.

## Essential offline release checklist

- [ ] The public interface exposes at least three concrete checks through one receipt format.
- [ ] Each receipt says what was checked, the outcome, why, exact mismatches or missing input, scope, and next action.
- [ ] Receipts remain stable for identical input and change on tampering.
- [ ] Public examples run from the isolated kernel package without legacy runtime imports.
- [ ] Optional audit/signature/quorum layers can be attached without blocking ordinary single-user checks.
- [ ] Documentation distinguishes a tested check from a hypothesis or physical interpretation.

## Boundaries that matter

The kernel should be strict about **what it has actually checked**. It should not be strict about style, jargon, or unnecessary metadata. If a user needs a more advanced check, the right answer is: “Here is the next supported check or the missing input,” not a cloud of unexplained prohibitions.

## References

[1] `SOV_CORE_CONTRACT_v0.1.md`, §§2, 9, and 12, local project evidence workspace.  
[2] `sov_evidence_geometry_core/simple.py`, public bounded-check implementation.  
[3] `tests/core_contract/test_simple_kernel.py`, executable examples and outcome tests.

## Theory neutrality

This kernel does not belong to any named theory. A framework label records where a claim came from; it does not change the check or turn a successful receipt into an endorsement of a theory, interpretation, or model of reality.
