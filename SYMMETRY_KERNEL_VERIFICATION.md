# Machine-checked verification of the kernel's symmetry-checking capabilities

All statements below are formalised and proved in `RequestProject/SymmetryKernel.lean`.
The file builds with no `sorry` and no added axioms (only Lean's standard
`propext`, `Classical.choice`, `Quot.sound`).

## What was modelled

The Lean file transcribes the symmetry logic of the kernel:

| Kernel code | Lean model |
|---|---|
| `check_symmetric_matrix` (`matrix.symmetric.v1`) | `SovKernel.checkSymmetricMatrix` |
| `check_rank3_last_indices_symmetric` (`tensor.rank3_last_indices_symmetric.v1`) | `SovKernel.checkRank3LastSymmetric` |
| `screen_rank3_last_indices_symmetric` (vectorised triangle screen) | `SovKernel.screenMismatches` |
| `tensor.symmetry.v1` sparse predicate of the reference interpreter | `SovKernel.sparseSymmetryHolds` |

Inputs are modelled as lists of lists (of lists) exactly as the implementations
receive them, and component values by an arbitrary type with decidable equality,
matching the implementations' exact `!=` comparison. The three terminal statuses
`verified` / `fail` / `unverifiable` are modelled by `SovKernel.Status`.

## Claims that were verified

1. **Soundness and completeness of the matrix check.**
   `checkSymmetricMatrix_verified_iff`: the check returns `verified` exactly when
   the input passes the structural gate and *every* declared component satisfies
   `A[i][j] = A[j][i]`. In particular, scanning only the strict upper triangle
   loses nothing: the diagonal and the lower triangle follow
   (`symMismatches_eq_nil_iff`).
2. **Genuine witnesses.** `symMismatches_sound` / `symMismatches_complete`: every
   reported mismatch is a real in-range disagreement with its transpose partner,
   and every such disagreement is reported.
3. **`fail` and `unverifiable` are used as documented.**
   `checkSymmetricMatrix_fail_iff` (a real counterexample exists) and
   `checkSymmetricMatrix_unverifiable_iff` (inadmissible input only — never a
   verdict about symmetry). `checkSymmetricMatrix_trichotomy`: no other outcome
   is possible, and the status is a function of the declared input.
4. **Bridge to the standard mathematical notion.**
   `checkSymmetricMatrix_verified_iff_isSymm`: on admissible input, `verified` is
   equivalent to `Aᵀ = A` for the induced matrix in Mathlib's sense.
5. **Rank-three final-index symmetry.** `checkRank3_verified_iff`,
   `checkRank3_fail_iff`, `checkRank3_unverifiable_iff`, and
   `rank3Mismatches_sound` / `_complete` give the same guarantees for
   `tensor.rank3_last_indices_symmetric.v1`, including that the per-plane
   triangle scan is exactly equivalent to `∀ i, j, k: T[i][j][k] = T[i][k][j]`.
6. **Slice characterisation** (documentation §C, "for each fixed first index the
   slice must be a symmetric matrix"): `checkRank3_verified_iff_slices` proves the
   tensor check verifies exactly when every slice passes the matrix check, and
   `checkRank3_singleton` proves the two predicates agree on a one-plane tensor.
7. **The predicate is strictly weaker than full permutation symmetry**, as the
   documentation states: `weakerWitness_verified` together with
   `weakerWitness_not_fully_symmetric` exhibits a 2×2×2 tensor that the kernel
   verifies but that is not symmetric under exchanging the first index with a
   later one.
8. **The GPU screen cannot disagree with the deterministic kernel.**
   `screenMismatches_eq_rank3Mismatches`: the vectorised `triu_indices` screen
   enumerates exactly the same witnesses in exactly the same order, so its
   candidate verdict and its reported first mismatch always coincide with the
   authoritative check.
9. **Worked controls from the documentation reproduce.** `[[1,2],[2,4]]`
   verifies, `[[1,3],[2,4]]` fails, a non-square input is `unverifiable`; the §C
   negative control `[[1,2],[3,4]]` fails and the positive control `[[1,2],[2,3]]`
   verifies; the empty tensor is `unverifiable`.
10. **The sparse interpreter predicate is complete despite scanning a finite set.**
    `sparseSymmetryHolds_iff`: because the declared support is closed under the
    slot swap, and absent components are exactly zero (`sparseVal_eq_zero`), the
    finite scan is equivalent to the symmetry (or antisymmetry) statement over
    *all* index tuples of the tensor's rank. Corollary
    `sparse_antisymmetric_diagonal_zero`: for a declared antisymmetric slot pair,
    a passing outcome forces every component whose two slots agree to be zero.

## Scope and limitations of the verification

* The verification concerns the *mathematical content* of the checks: which
  inputs are accepted, which verdict is produced, and whether the reported
  witnesses are genuine. It does not model receipt hashing, canonicalisation,
  provenance, storage, or transport.
* The numeric admissibility part of the input gate (rejecting booleans,
  non-numeric values, and non-finite floats) is represented by the choice of an
  abstract component type with exact equality, rather than being re-derived; the
  *structural* part of the gate (non-empty, rectangular, square/equal final
  dimensions) is modelled explicitly and is what the `unverifiable` theorems
  characterise.
* Component equality is exact. Nothing here licenses a tolerance-based reading of
  a `verified` status, and — as the kernel's own scope note says — a `verified`
  receipt establishes only the displayed finite component equality, not any
  physical or theory-level proposition.
