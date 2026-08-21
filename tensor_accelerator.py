"""Optional GPU candidate screening for rank-three final-index symmetry.

This module is explicitly non-authoritative: it accelerates candidate triage only.
Any candidate result intended for a receipt must be re-evaluated by
``check_rank3_last_indices_symmetric`` in the deterministic universal kernel.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal, Sequence

import numpy as np

from .simple import check_rank3_last_indices_symmetric

Backend = Literal["auto", "cpu", "gpu"]


@dataclass(frozen=True)
class TensorCandidateScreen:
    status: Literal["candidate_verified", "candidate_failed", "unavailable"]
    backend: str
    shape: tuple[int, int, int] | None
    mismatch_count: int = 0
    first_mismatch: dict[str, Any] | None = None
    reason_code: str | None = None


def screen_rank3_last_indices_symmetric(tensor: Sequence[Sequence[Sequence[int | float]]], *, backend: Backend = "auto") -> TensorCandidateScreen:
    """Vector-screen a finite tensor, returning a non-authoritative candidate state."""
    try:
        array = np.asarray(tensor)
    except (TypeError, ValueError):
        return TensorCandidateScreen("unavailable", "cpu", None, reason_code="E_INPUT_NOT_ARRAY")
    if array.ndim != 3 or not all(dimension > 0 for dimension in array.shape) or array.shape[1] != array.shape[2]:
        return TensorCandidateScreen("unavailable", "cpu", tuple(array.shape) if array.ndim == 3 else None, reason_code="E_INPUT_NOT_RANK3_NUMERIC_SQUARE_LAST_INDICES")
    if array.dtype == np.bool_ or not np.issubdtype(array.dtype, np.number) or not np.isfinite(array).all():
        return TensorCandidateScreen("unavailable", "cpu", tuple(array.shape), reason_code="E_INPUT_NOT_RANK3_NUMERIC_SQUARE_LAST_INDICES")
    xp, selected = _select_backend(backend)
    if xp is None:
        return TensorCandidateScreen("unavailable", "gpu", tuple(array.shape), reason_code="E_GPU_BACKEND_UNAVAILABLE")
    device = xp.asarray(array)
    upper_j, upper_k = xp.triu_indices(device.shape[1], k=1)
    unequal = device[:, upper_j, upper_k] != device[:, upper_k, upper_j]
    mismatch_count = int(xp.count_nonzero(unequal).item())
    if mismatch_count == 0:
        return TensorCandidateScreen("candidate_verified", selected, tuple(array.shape))
    first = xp.argwhere(unequal)[0]
    i, pair = (int(value) for value in first.tolist())
    j, k = int(upper_j[pair].item()), int(upper_k[pair].item())
    return TensorCandidateScreen("candidate_failed", selected, tuple(array.shape), mismatch_count, {"at": [i, j, k], "mirror_at": [i, k, j], "value": array[i, j, k].item(), "mirror_value": array[i, k, j].item()})


def confirm_rank3_last_indices_symmetric(tensor: Sequence[Sequence[Sequence[int | float]]]) -> dict[str, Any]:
    """Return the authoritative deterministic receipt; use after any GPU screen."""
    return check_rank3_last_indices_symmetric(tensor)


def _select_backend(requested: Backend):
    if requested == "cpu":
        return np, "cpu-numpy"
    try:
        import cupy as cp  # optional production GPU dependency, intentionally lazy
        return cp, "gpu-cupy"
    except ImportError:
        return (np, "cpu-numpy") if requested == "auto" else (None, "gpu-unavailable")
