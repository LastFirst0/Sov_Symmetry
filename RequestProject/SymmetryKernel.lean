/-
# Formal verification of the kernel's symmetry-checking capabilities

This file models, in Lean, the symmetry predicates implemented by the kernel and
proves the properties that the accompanying documentation claims for them.

The predicates modelled here are:

* `matrix.symmetric.v1` — `check_symmetric_matrix` (`simple.py`);
* `tensor.rank3_last_indices_symmetric.v1` — `check_rank3_last_indices_symmetric`
  (`simple.py`), described mathematically in
  *Governed Upload Code Walkthrough and Tensor Symmetry Mathematics*, §C;
* the non-authoritative GPU triangle screen
  `screen_rank3_last_indices_symmetric` (`tensor_accelerator.py`);
* `tensor.symmetry.v1` — the sparse-component symmetry/antisymmetry predicate of
  the reference interpreter (`interpreter.py`).

Entry values are modelled by an arbitrary type `α` with decidable equality,
because the implementations compare components with exact `!=` equality.  This
covers both the integer and the (finite) floating-point components the
implementations admit.  The three-valued status is modelled by `Status`.
-/
import Mathlib

set_option maxHeartbeats 1000000
set_option autoImplicit false
set_option relaxedAutoImplicit false

namespace SovKernel

/-- The three terminal statuses used by the kernel. -/
inductive Status where
  | verified
  | fail
  | unverifiable
deriving DecidableEq, Repr

variable {α : Type*} [Inhabited α] [DecidableEq α]

/-! ## 1. `matrix.symmetric.v1` -/

/-- Component `m[i][j]` of a matrix given as a list of rows. -/
def entry (m : List (List α)) (i j : ℕ) : α := (m.getD i []).getD j default

/-- The implementation's input gate: a nonempty square list-of-rows.
(Numeric, non-boolean, finite components are modelled by the component type.) -/
def isSquare (m : List (List α)) : Bool :=
  0 < m.length && m.all (fun row => row.length == m.length)

/-- The mismatch witnesses collected by `check_symmetric_matrix`: it scans only
the strict upper triangle `i < j`. -/
def symMismatches (m : List (List α)) : List (ℕ × ℕ) :=
  (List.range m.length).flatMap fun i =>
    (List.range m.length).filterMap fun j =>
      if i < j ∧ entry m i j ≠ entry m j i then some (i, j) else none

/-- The kernel's `matrix.symmetric.v1` status. -/
def checkSymmetricMatrix (m : List (List α)) : Status :=
  if isSquare m then
    (if symMismatches m = [] then Status.verified else Status.fail)
  else Status.unverifiable

/-- Mathematical symmetry of the declared components of `m`. -/
def IsSymmetricList (m : List (List α)) : Prop :=
  ∀ i < m.length, ∀ j < m.length, entry m i j = entry m j i

/-! ## 2. `tensor.rank3_last_indices_symmetric.v1` -/

/-- Component `T[i][j][k]`. -/
def tEntry (t : List (List (List α))) (i j k : ℕ) : α := entry (t.getD i []) j k

/-- The side length of the final two axes, i.e. `len(T[0])`. -/
def lastDim (t : List (List (List α))) : ℕ := (t.getD 0 []).length

/-- The implementation's input gate for rank-three tensors: nonempty, rectangular,
and with equal (positive) final two dimensions. -/
def isRank3Square (t : List (List (List α))) : Bool :=
  0 < t.length && 0 < lastDim t &&
    t.all (fun plane =>
      plane.length == lastDim t && plane.all (fun row => row.length == lastDim t))

/-- The mismatch witnesses collected by `check_rank3_last_indices_symmetric`:
for each plane `i` it scans only the strict upper triangle `j < k`. -/
def rank3Mismatches (t : List (List (List α))) : List (ℕ × ℕ × ℕ) :=
  (List.range t.length).flatMap fun i =>
    (List.range (lastDim t)).flatMap fun j =>
      (List.range (lastDim t)).filterMap fun k =>
        if j < k ∧ tEntry t i j k ≠ tEntry t i k j then some (i, j, k) else none

/-- The kernel's `tensor.rank3_last_indices_symmetric.v1` status. -/
def checkRank3LastSymmetric (t : List (List (List α))) : Status :=
  if isRank3Square t then
    (if rank3Mismatches t = [] then Status.verified else Status.fail)
  else Status.unverifiable

/-- Symmetry of the declared components in the final two indices. -/
def IsLastIndexSymmetric (t : List (List (List α))) : Prop :=
  ∀ i < t.length, ∀ j < lastDim t, ∀ k < lastDim t, tEntry t i j k = tEntry t i k j

/-- Full permutation symmetry of all three indices (for a cubical tensor), used
only to show that the kernel predicate is strictly weaker. -/
def IsFullySymmetric (t : List (List (List α))) : Prop :=
  ∀ i < t.length, ∀ j < t.length, ∀ k < t.length,
    tEntry t i j k = tEntry t i k j ∧ tEntry t i j k = tEntry t j i k

/-! ## 3. GPU triangle screen (`tensor_accelerator.py`) -/

/-- `numpy.triu_indices(n, k = 1)`, in row-major order. -/
def triuIndices (n : ℕ) : List (ℕ × ℕ) :=
  (List.range n).flatMap fun j =>
    (List.range n).filterMap fun k => if j < k then some (j, k) else none

/-- The vectorised screen: for every plane, compare the two triangles selected by
`triu_indices`. -/
def screenMismatches (t : List (List (List α))) : List (ℕ × ℕ × ℕ) :=
  (List.range t.length).flatMap fun i =>
    (triuIndices (lastDim t)).filterMap fun p =>
      if tEntry t i p.1 p.2 ≠ tEntry t i p.2 p.1 then some (i, p.1, p.2) else none

/-! ## 4. `tensor.symmetry.v1` (sparse components, reference interpreter) -/

/-- Swap positions `l` and `r` of an index tuple. -/
def swapIdx (l r : ℕ) (idx : List ℕ) : List ℕ :=
  (idx.set l (idx.getD r 0)).set r (idx.getD l 0)

/-- Value of a sparse component map; absent components are exactly `0`. -/
def sparseVal (comps : List (List ℕ × ℚ)) (idx : List ℕ) : ℚ :=
  (comps.lookup idx).getD 0

/-- The index set the interpreter actually iterates over: the declared support,
closed under the swap. -/
def sparseScan (comps : List (List ℕ × ℚ)) (l r : ℕ) : List (List ℕ) :=
  comps.map Prod.fst ++ (comps.map Prod.fst).map (swapIdx l r)

/-- `sign = 1` for a declared `symmetric` slot pair, `sign = -1` for
`antisymmetric`. -/
def sparseSymmetryHolds (comps : List (List ℕ × ℚ)) (l r : ℕ) (sign : ℚ) : Prop :=
  ∀ idx ∈ sparseScan comps l r, sparseVal comps idx = sign * sparseVal comps (swapIdx l r idx)

/-! ## 5. Claims about `matrix.symmetric.v1` -/

/-- A reported mismatch is a genuine witness: it is a strict-upper-triangle pair of
in-range coordinates at which the matrix differs from its transpose. -/
theorem mem_symMismatches {m : List (List α)} {i j : ℕ} :
    (i, j) ∈ symMismatches m ↔
      i < m.length ∧ j < m.length ∧ i < j ∧ entry m i j ≠ entry m j i := by
  simp only [symMismatches, List.mem_flatMap, List.mem_filterMap, List.mem_range]
  constructor
  · rintro ⟨a, ha, b, hb, h⟩
    by_cases hc : a < b ∧ entry m a b ≠ entry m b a
    · rw [if_pos hc] at h
      obtain ⟨rfl, rfl⟩ : a = i ∧ b = j := by simpa using h
      exact ⟨ha, hb, hc⟩
    · rw [if_neg hc] at h; exact absurd h (by simp)
  · rintro ⟨hi, hj, h⟩
    exact ⟨i, hi, j, hj, by rw [if_pos h]⟩

theorem symMismatches_sound {m : List (List α)} {i j : ℕ} (h : (i, j) ∈ symMismatches m) :
    i < m.length ∧ j < m.length ∧ i < j ∧ entry m i j ≠ entry m j i :=
  mem_symMismatches.mp h

/-- Conversely, every in-range strict-upper-triangle disagreement is reported. -/
theorem symMismatches_complete {m : List (List α)} {i j : ℕ}
    (hi : i < m.length) (hj : j < m.length) (hij : i < j)
    (hne : entry m i j ≠ entry m j i) : (i, j) ∈ symMismatches m :=
  mem_symMismatches.mpr ⟨hi, hj, hij, hne⟩

/-- Scanning one triangle suffices: an empty mismatch list is equivalent to full
symmetry of the declared components, diagonal included. -/
theorem symMismatches_eq_nil_iff {m : List (List α)} :
    symMismatches m = [] ↔ IsSymmetricList m := by
  rw [List.eq_nil_iff_forall_not_mem]
  constructor
  · intro h i hi j hj
    rcases lt_trichotomy i j with hij | rfl | hij
    · by_contra hne
      exact h (i, j) (mem_symMismatches.mpr ⟨hi, hj, hij, hne⟩)
    · rfl
    · by_contra hne
      exact h (j, i) (mem_symMismatches.mpr ⟨hj, hi, hij, fun hh => hne hh.symm⟩)
  · rintro h ⟨i, j⟩ hmem
    obtain ⟨hi, hj, -, hne⟩ := mem_symMismatches.mp hmem
    exact hne (h i hi j hj)

/-- **Soundness and completeness of `matrix.symmetric.v1`.** -/
theorem checkSymmetricMatrix_verified_iff {m : List (List α)} :
    checkSymmetricMatrix m = Status.verified ↔ isSquare m = true ∧ IsSymmetricList m := by
  rw [checkSymmetricMatrix, ← symMismatches_eq_nil_iff]
  by_cases hs : isSquare m = true <;> by_cases hm : symMismatches m = [] <;> simp [hs, hm]

/-- A `fail` status is returned exactly when the input is admissible and a genuine
counterexample pair exists. -/
theorem checkSymmetricMatrix_fail_iff {m : List (List α)} :
    checkSymmetricMatrix m = Status.fail ↔
      isSquare m = true ∧ ∃ i < m.length, ∃ j < m.length, entry m i j ≠ entry m j i := by
  have key : (¬ IsSymmetricList m) ↔
      ∃ i < m.length, ∃ j < m.length, entry m i j ≠ entry m j i := by
    unfold IsSymmetricList; push_neg; rfl
  rw [← key, checkSymmetricMatrix, ← symMismatches_eq_nil_iff]
  by_cases hs : isSquare m = true <;> by_cases hm : symMismatches m = [] <;> simp [hs, hm]

/-- `unverifiable` is returned exactly on inadmissible input, never as a verdict on
the predicate. -/
theorem checkSymmetricMatrix_unverifiable_iff {m : List (List α)} :
    checkSymmetricMatrix m = Status.unverifiable ↔ isSquare m = false := by
  rw [checkSymmetricMatrix]
  by_cases hs : isSquare m = true <;> by_cases hm : symMismatches m = [] <;> simp [hs, hm]

/-- The status is always one of the three terminal values (there is no other
outcome, and the check is a total function of the declared input). -/
theorem checkSymmetricMatrix_trichotomy (m : List (List α)) :
    checkSymmetricMatrix m = Status.verified ∨ checkSymmetricMatrix m = Status.fail ∨
      checkSymmetricMatrix m = Status.unverifiable := by
  unfold checkSymmetricMatrix; split <;> [split; skip] <;> simp

/-- The matrix of components of a square input. -/
def toMatrix (m : List (List α)) : Matrix (Fin m.length) (Fin m.length) α :=
  fun i j => entry m i j

/-- **Bridge to the mathematical notion.** For an admissible input, `verified` is
equivalent to `Aᵀ = A` for the induced matrix, in Mathlib's sense. -/
theorem checkSymmetricMatrix_verified_iff_isSymm {m : List (List α)} (hm : isSquare m = true) :
    checkSymmetricMatrix m = Status.verified ↔ (toMatrix m).IsSymm := by
  rw [checkSymmetricMatrix_verified_iff]
  constructor
  · rintro ⟨-, h⟩
    ext i j
    exact h j j.2 i i.2
  · intro h
    refine ⟨hm, fun i hi j hj => ?_⟩
    exact (congrFun (congrFun h ⟨i, hi⟩) ⟨j, hj⟩).symm

/-! ## 6. Claims about `tensor.rank3_last_indices_symmetric.v1` -/

theorem mem_rank3Mismatches {t : List (List (List α))} {i j k : ℕ} :
    (i, j, k) ∈ rank3Mismatches t ↔
      i < t.length ∧ j < lastDim t ∧ k < lastDim t ∧ j < k ∧
        tEntry t i j k ≠ tEntry t i k j := by
  simp only [rank3Mismatches, List.mem_flatMap, List.mem_filterMap, List.mem_range]
  constructor
  · rintro ⟨a, ha, b, hb, c, hc, h⟩
    by_cases hcond : b < c ∧ tEntry t a b c ≠ tEntry t a c b
    · rw [if_pos hcond] at h
      obtain ⟨rfl, rfl, rfl⟩ : a = i ∧ b = j ∧ c = k := by simpa using h
      exact ⟨ha, hb, hc, hcond.1, hcond.2⟩
    · rw [if_neg hcond] at h; exact absurd h (by simp)
  · rintro ⟨hi, hj, hk, h⟩
    exact ⟨i, hi, j, hj, k, hk, by rw [if_pos h]⟩

theorem rank3Mismatches_sound {t : List (List (List α))} {i j k : ℕ}
    (h : (i, j, k) ∈ rank3Mismatches t) :
    i < t.length ∧ j < lastDim t ∧ k < lastDim t ∧ j < k ∧ tEntry t i j k ≠ tEntry t i k j :=
  mem_rank3Mismatches.mp h

theorem rank3Mismatches_complete {t : List (List (List α))} {i j k : ℕ}
    (hi : i < t.length) (hj : j < lastDim t) (hk : k < lastDim t) (hjk : j < k)
    (hne : tEntry t i j k ≠ tEntry t i k j) : (i, j, k) ∈ rank3Mismatches t :=
  mem_rank3Mismatches.mpr ⟨hi, hj, hk, hjk, hne⟩

/-- Scanning one triangle per plane suffices: diagonal components `T[i,j,j]` need no
comparison. -/
theorem rank3Mismatches_eq_nil_iff {t : List (List (List α))} :
    rank3Mismatches t = [] ↔ IsLastIndexSymmetric t := by
  rw [List.eq_nil_iff_forall_not_mem]
  constructor
  · intro h i hi j hj k hk
    rcases lt_trichotomy j k with hjk | rfl | hjk
    · by_contra hne
      exact h (i, j, k) (mem_rank3Mismatches.mpr ⟨hi, hj, hk, hjk, hne⟩)
    · rfl
    · by_contra hne
      exact h (i, k, j) (mem_rank3Mismatches.mpr ⟨hi, hk, hj, hjk, fun hh => hne hh.symm⟩)
  · rintro h ⟨i, j, k⟩ hmem
    obtain ⟨hi, hj, hk, -, hne⟩ := mem_rank3Mismatches.mp hmem
    exact hne (h i hi j hj k hk)

/-- **Soundness and completeness of `tensor.rank3_last_indices_symmetric.v1`.** -/
theorem checkRank3_verified_iff {t : List (List (List α))} :
    checkRank3LastSymmetric t = Status.verified ↔
      isRank3Square t = true ∧ IsLastIndexSymmetric t := by
  rw [checkRank3LastSymmetric, ← rank3Mismatches_eq_nil_iff]
  by_cases hs : isRank3Square t = true <;> by_cases hm : rank3Mismatches t = [] <;> simp [hs, hm]

theorem checkRank3_fail_iff {t : List (List (List α))} :
    checkRank3LastSymmetric t = Status.fail ↔
      isRank3Square t = true ∧ ∃ i < t.length, ∃ j < lastDim t, ∃ k < lastDim t,
        tEntry t i j k ≠ tEntry t i k j := by
  have key : (¬ IsLastIndexSymmetric t) ↔
      ∃ i < t.length, ∃ j < lastDim t, ∃ k < lastDim t, tEntry t i j k ≠ tEntry t i k j := by
    unfold IsLastIndexSymmetric; push_neg; rfl
  rw [← key, checkRank3LastSymmetric, ← rank3Mismatches_eq_nil_iff]
  by_cases hs : isRank3Square t = true <;> by_cases hm : rank3Mismatches t = [] <;> simp [hs, hm]

theorem checkRank3_unverifiable_iff {t : List (List (List α))} :
    checkRank3LastSymmetric t = Status.unverifiable ↔ isRank3Square t = false := by
  rw [checkRank3LastSymmetric]
  by_cases hs : isRank3Square t = true <;> by_cases hm : rank3Mismatches t = [] <;> simp [hs, hm]

omit [Inhabited α] [DecidableEq α] in
/-- Unfolding of the rank-three input gate. -/
theorem isRank3Square_iff {t : List (List (List α))} :
    isRank3Square t = true ↔
      0 < t.length ∧ 0 < lastDim t ∧
        ∀ plane ∈ t, plane.length = lastDim t ∧ ∀ row ∈ plane, row.length = lastDim t := by
  simp [isRank3Square, List.all_eq_true, and_assoc]

/-- **Slice characterisation.** For an admissible tensor, final-index symmetry holds
exactly when every `n × n` slice is a symmetric matrix in the sense of
`matrix.symmetric.v1`. -/
theorem checkRank3_verified_iff_slices {t : List (List (List α))}
    (ht : isRank3Square t = true) :
    checkRank3LastSymmetric t = Status.verified ↔
      ∀ plane ∈ t, checkSymmetricMatrix plane = Status.verified := by
  obtain ⟨hpos, hdim, hshape⟩ := isRank3Square_iff.mp ht
  have hsq : ∀ plane ∈ t, isSquare plane = true := by
    intro plane hp
    obtain ⟨hlen, hrows⟩ := hshape plane hp
    simp only [isSquare, Bool.and_eq_true, decide_eq_true_eq, List.all_eq_true, beq_iff_eq]
    exact ⟨by omega, fun row hr => by rw [hrows row hr, hlen]⟩
  rw [checkRank3_verified_iff]
  constructor
  · rintro ⟨-, hsym⟩ plane hp
    obtain ⟨hlen, -⟩ := hshape plane hp
    obtain ⟨i, hi, hget⟩ : ∃ i, ∃ h : i < t.length, t[i] = plane := by
      obtain ⟨i, hi, hget⟩ := List.getElem_of_mem hp
      exact ⟨i, hi, hget⟩
    refine checkSymmetricMatrix_verified_iff.mpr ⟨hsq plane hp, fun j hj k hk => ?_⟩
    have hj' : j < lastDim t := by rw [hlen] at hj; exact hj
    have hk' : k < lastDim t := by rw [hlen] at hk; exact hk
    have := hsym i hi j hj' k hk'
    rwa [tEntry, tEntry, List.getD_eq_getElem _ _ hi, hget] at this
  · intro h
    refine ⟨ht, fun i hi j hj k hk => ?_⟩
    have hmem : t[i] ∈ t := List.getElem_mem hi
    obtain ⟨-, hsym⟩ := checkSymmetricMatrix_verified_iff.mp (h t[i] hmem)
    obtain ⟨hlen, -⟩ := hshape t[i] hmem
    have hj' : j < t[i].length := by rw [hlen]; exact hj
    have hk' : k < t[i].length := by rw [hlen]; exact hk
    have := hsym j hj' k hk'
    rwa [tEntry, tEntry, List.getD_eq_getElem _ _ hi]

omit [Inhabited α] [DecidableEq α] in
theorem isRank3Square_singleton {m : List (List α)} (hm : isSquare m = true) :
    isRank3Square [m] = true := by
  simp only [isSquare, Bool.and_eq_true, decide_eq_true_eq, List.all_eq_true, beq_iff_eq] at hm
  obtain ⟨hpos, hrows⟩ := hm
  refine isRank3Square_iff.mpr ⟨by simp, by simpa [lastDim] using hpos, ?_⟩
  intro plane hp
  rw [List.mem_singleton] at hp
  subst hp
  exact ⟨by simp [lastDim], fun row hr => by simp [lastDim, hrows row hr]⟩

/-- **Consistency of the two symmetry predicates.** On a square matrix, the rank-three
final-index check applied to the one-plane tensor returns exactly the matrix check's
status. -/
theorem checkRank3_singleton {m : List (List α)} (hm : isSquare m = true) :
    checkRank3LastSymmetric [m] = checkSymmetricMatrix m := by
  have h3 := isRank3Square_singleton hm
  by_cases h : checkSymmetricMatrix m = Status.verified
  · rw [h]
    refine (checkRank3_verified_iff_slices h3).mpr ?_
    intro plane hp
    rw [List.mem_singleton] at hp
    exact hp ▸ h
  · have hfail : checkSymmetricMatrix m = Status.fail := by
      rcases checkSymmetricMatrix_trichotomy m with h1 | h1 | h1
      · exact absurd h1 h
      · exact h1
      · rw [checkSymmetricMatrix_unverifiable_iff] at h1
        rw [h1] at hm
        exact absurd hm (by simp)
    have hnv : checkRank3LastSymmetric [m] ≠ Status.verified := fun hv =>
      h ((checkRank3_verified_iff_slices h3).mp hv m (by simp))
    rw [hfail]
    by_cases hm3 : rank3Mismatches [m] = [] <;>
      simp_all [checkRank3LastSymmetric]

/-! ## 7. The predicate is strictly weaker than full permutation symmetry -/

/-- A cubical tensor accepted by the kernel predicate that is *not* symmetric under
permuting the first index with a later one. -/
def weakerWitness : List (List (List ℤ)) := [[[0, 1], [1, 0]], [[0, 0], [0, 0]]]

theorem weakerWitness_verified :
    checkRank3LastSymmetric weakerWitness = Status.verified := by
  decide

theorem weakerWitness_not_fully_symmetric : ¬ IsFullySymmetric weakerWitness := by
  intro h
  have h2 := (h 0 (by decide) 1 (by decide) 0 (by decide)).2
  exact absurd h2 (by decide)

/-! ## 8. The GPU triangle screen agrees with the deterministic kernel -/

/-- The vectorised screen enumerates exactly the same mismatch witnesses, in the same
order, as the deterministic kernel; in particular the screen's first mismatch is the
kernel's first mismatch and `candidate_verified` matches `verified`. -/
theorem screenMismatches_eq_rank3Mismatches (t : List (List (List α))) :
    screenMismatches t = rank3Mismatches t := by
  unfold screenMismatches rank3Mismatches triuIndices
  refine List.flatMap_congr fun i _ => ?_
  rw [List.filterMap_flatMap]
  refine List.flatMap_congr fun j _ => ?_
  rw [List.filterMap_filterMap]
  refine List.filterMap_congr fun k _ => ?_
  by_cases hjk : j < k <;> simp [hjk]

/-! ## 9. Worked controls from the documentation -/

/-- `[[1, 2], [2, 4]]` is `verified` (walkthrough example). -/
theorem control_matrix_verified :
    checkSymmetricMatrix ([[1, 2], [2, 4]] : List (List ℤ)) = Status.verified := by decide

/-- `[[1, 3], [2, 4]]` is `fail` (walkthrough example). -/
theorem control_matrix_fail :
    checkSymmetricMatrix ([[1, 3], [2, 4]] : List (List ℤ)) = Status.fail := by decide

/-- A non-square input is `unverifiable`, not `fail`. -/
theorem control_matrix_unverifiable :
    checkSymmetricMatrix ([[1, 2]] : List (List ℤ)) = Status.unverifiable := by decide

/-- Negative control of §C: the slice `[[1,2],[3,4]]` fails. -/
theorem control_tensor_fail :
    checkRank3LastSymmetric ([[[1, 2], [3, 4]]] : List (List (List ℤ))) = Status.fail := by decide

/-- Positive control of §C: the slice `[[1,2],[2,3]]` is verified. -/
theorem control_tensor_verified :
    checkRank3LastSymmetric ([[[1, 2], [2, 3]]] : List (List (List ℤ))) = Status.verified := by
  decide

/-- The empty tensor is `unverifiable`. -/
theorem control_tensor_empty_unverifiable :
    checkRank3LastSymmetric ([] : List (List (List ℤ))) = Status.unverifiable := by decide

/-! ## 10. Claims about the sparse `tensor.symmetry.v1` predicate -/

theorem swapIdx_involutive {l r : ℕ} {idx : List ℕ} (hl : l < idx.length)
    (hr : r < idx.length) : swapIdx l r (swapIdx l r idx) = idx := by
  apply List.ext_getElem
  · simp [swapIdx]
  · intro n h1 h2
    simp only [swapIdx, List.getElem_set, List.length_set,
      List.getD_eq_getElem?_getD, List.getElem?_set]
    by_cases hlr : l = r <;> by_cases h3 : r = n <;> by_cases h4 : l = n <;>
      simp_all [Ne.symm]

/-- A component whose two swapped slots carry the same index is a fixed point of the
swap. -/
theorem swapIdx_self_of_eq {l r : ℕ} {idx : List ℕ} (hl : l < idx.length)
    (hr : r < idx.length) (h : idx.getD l 0 = idx.getD r 0) : swapIdx l r idx = idx := by
  apply List.ext_getElem
  · simp [swapIdx]
  · intro n h1 h2
    rw [List.getD_eq_getElem _ _ hl, List.getD_eq_getElem _ _ hr] at h
    simp only [swapIdx, List.getElem_set, List.getD_eq_getElem?_getD]
    by_cases h3 : r = n <;> by_cases h4 : l = n <;> simp_all

/-- A component absent from the declared sparse support has value `0`. -/
theorem sparseVal_eq_zero {comps : List (List ℕ × ℚ)} {idx : List ℕ}
    (h : idx ∉ comps.map Prod.fst) : sparseVal comps idx = 0 := by
  have : comps.lookup idx = none := by
    rw [List.lookup_eq_none_iff]
    intro p hp
    simp only [bne_iff_ne, ne_eq]
    intro he
    exact h (List.mem_map.mpr ⟨p, hp, he.symm⟩)
  simp [sparseVal, this]

theorem swapIdx_length (l r : ℕ) (idx : List ℕ) : (swapIdx l r idx).length = idx.length := by
  simp [swapIdx]

/-- **Closure completeness.** Because the interpreter closes the declared support
under the slot swap, its finite scan is equivalent to the universally quantified
symmetry statement over *all* index tuples of the tensor's rank — including the
infinitely many tuples whose components default to zero. -/
theorem sparseSymmetryHolds_iff {comps : List (List ℕ × ℚ)} {l r rank : ℕ} {sign : ℚ}
    (hl : l < rank) (hr : r < rank)
    (hkeys : ∀ p ∈ comps, p.1.length = rank) :
    sparseSymmetryHolds comps l r sign ↔
      ∀ idx : List ℕ, idx.length = rank →
        sparseVal comps idx = sign * sparseVal comps (swapIdx l r idx) := by
  have hkeys' : ∀ idx ∈ comps.map Prod.fst, idx.length = rank := by
    intro idx hidx
    obtain ⟨p, hp, rfl⟩ := List.mem_map.mp hidx
    exact hkeys p hp
  constructor
  · intro h idx hlen
    have hl' : l < idx.length := by rw [hlen]; exact hl
    have hr' : r < idx.length := by rw [hlen]; exact hr
    by_cases hmem : idx ∈ comps.map Prod.fst
    · exact h idx (List.mem_append_left _ hmem)
    by_cases hmem' : swapIdx l r idx ∈ comps.map Prod.fst
    · have : idx ∈ (comps.map Prod.fst).map (swapIdx l r) :=
        List.mem_map.mpr ⟨swapIdx l r idx, hmem', swapIdx_involutive hl' hr'⟩
      exact h idx (List.mem_append_right _ this)
    · rw [sparseVal_eq_zero hmem, sparseVal_eq_zero hmem', mul_zero]
  · intro h idx hidx
    refine h idx ?_
    rcases List.mem_append.mp hidx with hidx | hidx
    · exact hkeys' idx hidx
    · obtain ⟨key, hkey, rfl⟩ := List.mem_map.mp hidx
      rw [swapIdx_length]
      exact hkeys' key hkey

/-- For an antisymmetric declared slot pair, a `verified` outcome forces every
component whose two slots agree to be zero. -/
theorem sparse_antisymmetric_diagonal_zero {comps : List (List ℕ × ℚ)} {l r rank : ℕ}
    (hl : l < rank) (hr : r < rank) (hkeys : ∀ p ∈ comps, p.1.length = rank)
    (h : sparseSymmetryHolds comps l r (-1)) :
    ∀ idx : List ℕ, idx.length = rank → idx.getD l 0 = idx.getD r 0 →
      sparseVal comps idx = 0 := by
  intro idx hlen hdiag
  have hl' : l < idx.length := by rw [hlen]; exact hl
  have hr' : r < idx.length := by rw [hlen]; exact hr
  have key := (sparseSymmetryHolds_iff hl hr hkeys).mp h idx hlen
  rw [swapIdx_self_of_eq hl' hr' hdiag] at key
  linarith

end SovKernel
