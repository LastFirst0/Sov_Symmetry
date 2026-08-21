"""Legacy compatibility shim for exploratory PolyglotEngine callers.

This module provides deterministic finite transformations needed for historical import
compatibility. It is not part of the universal verification kernel and makes no
semantic, empirical, or theoretical claim.
"""
from __future__ import annotations

from math import isfinite
from typing import Sequence


class PolyglotEngine:
    def _vector(self, values: Sequence[float]) -> list[float]:
        if not isinstance(values, Sequence) or isinstance(values, (str, bytes)):
            raise ValueError("E_POLYGLOT_VECTOR_REQUIRED")
        result = [float(value) for value in values]
        if not result or not all(isfinite(value) for value in result):
            raise ValueError("E_POLYGLOT_VECTOR_FINITE_REQUIRED")
        return result

    def apply_functor(self, vector: Sequence[float], direction: str = "identity") -> list[float]:
        values = self._vector(vector)
        if direction in {"identity", "forward", "preserve"}:
            return values
        if direction in {"reverse", "dual"}:
            return list(reversed(values))
        raise ValueError("E_POLYGLOT_DIRECTION_UNSUPPORTED")

    def check_word_stability(self, word_vectors: Sequence[Sequence[float]]) -> bool:
        vectors = [self._vector(item) for item in word_vectors]
        return bool(vectors) and len({len(item) for item in vectors}) == 1

    def project_to_leech_lattice(self, vector_8d: Sequence[float], golay_codeword: int) -> list[float]:
        values = self._vector(vector_8d)
        if len(values) != 8 or not isinstance(golay_codeword, int):
            raise ValueError("E_POLYGLOT_E8_OR_CODEWORD_REQUIRED")
        bits = [float((golay_codeword >> index) & 1) for index in range(8)]
        return values + bits + [0.0] * 8

    def classify_beast_bipartite(self, vector_8d: Sequence[float]) -> str:
        values = self._vector(vector_8d)
        labels = ("Lion", "Ox", "Eagle", "Man")
        return labels[max(range(min(4, len(values))), key=lambda index: abs(values[index]))]

    def project_to_merkaba(self, vector_8d: Sequence[float]) -> list[float]:
        values = self._vector(vector_8d)
        if len(values) != 8:
            raise ValueError("E_POLYGLOT_E8_VECTOR_REQUIRED")
        return [sum(values[0:3]), sum(values[3:6]), sum(values[6:8])]

    def translate_to_domains(self, vector_8d: Sequence[float]) -> dict[str, str]:
        values = self._vector(vector_8d)
        return {"scope": "legacy compatibility only", "dna_token": str(int(abs(values[0])) % 64), "music_token": str(int(abs(values[-1])) % 12)}

    def check_invariance(self, vector_8d: Sequence[float]) -> bool:
        values = self._vector(vector_8d)
        return self.apply_functor(self.apply_functor(values, "forward"), "identity") == values
