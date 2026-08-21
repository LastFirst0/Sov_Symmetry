"""
sov_math/core/unified_geometry.py
===================================
UnifiedGeometricEngine — Unifies Riemann Sphere, Hopf Fibration, Torus SGD,
and Invariant Probes into a single, cohesive geometric interface.
"""

import math
from typing import Any, Dict, List, Tuple, Union


class UnifiedGeometricEngine:
    """
    Consolidated geometric engine bringing together:
    - Stereographic Riemann Sphere mapping (C+inf <-> S2)
    - Hopf Fibration (S3 -> S2)
    - Torus SGD Geodesic step (T^n)
    - Invariant Probe evaluations
    - Discrete E8 root slot addressing
    """

    def __init__(self, slots_count: int = 240):
        self.slots_count = slots_count

    # ── 1. Riemann Sphere Projection ──────────────────────────────────────────

    @staticmethod
    def riemann_project(z: complex) -> Tuple[float, float, float]:
        """
        Map a complex number z = x + iy onto the 2-sphere S^2 via stereographic projection.
        Returns (X, Y, Z) on S^2 where X^2 + Y^2 + Z^2 = 1.
        """
        denom = z.real**2 + z.imag**2 + 1.0
        X = (2.0 * z.real) / denom
        Y = (2.0 * z.imag) / denom
        Z = (z.real**2 + z.imag**2 - 1.0) / denom
        return (X, Y, Z)

    @staticmethod
    def riemann_unproject(X: float, Y: float, Z: float) -> complex:
        """
        Inverse stereographic projection from S^2 back to the complex plane.
        """
        denom = 1.0 - Z
        if abs(denom) < 1e-9:
            return complex(1e9, 1e9)  # Point at infinity approximation
        return complex(X / denom, Y / denom)

    @staticmethod
    def mobius_transform(z: complex, a: complex, b: complex, c: complex, d: complex) -> complex:
        """
        Möbius transformation f(z) = (az + b) / (cz + d) on the Riemann sphere.
        Represents conformal transformations, Lorentz boosts, and isometric state rotations.
        """
        denom = c * z + d
        if abs(denom) < 1e-12:
            return complex(1e12, 1e12)  # Point at infinity
        return (a * z + b) / denom

    @staticmethod
    def fubini_study_distance(z1: complex, z2: complex) -> float:
        """
        Compute the Fubini-Study metric distance on the Riemann sphere / CP^1 (Bloch sphere).
        d_FS(z1, z2) = arccos(|1 + z1 * conj(z2)| / sqrt((1 + |z1|^2) * (1 + |z2|^2)))
        Returns invariant geodesic distance in range [0, pi/2].
        """
        numerator = abs(1.0 + z1 * z2.conjugate())
        denom = math.sqrt((1.0 + abs(z1)**2) * (1.0 + abs(z2)**2))
        if denom < 1e-12:
            return 0.0
        val = min(1.0, max(-1.0, numerator / denom))
        return math.acos(val)

    @staticmethod
    def fubini_study_distance_batch(z1: Any, z2: Any, device: str = None) -> Any:
        """
        PyTorch-accelerated GPU/CPU batch Fubini-Study distance calculation.
        Computes pairwise or elementwise geodesic distances across large tensors.
        """
        try:
            import torch
            if device is None:
                device = "cuda" if torch.cuda.is_available() else ("mps" if torch.backends.mps.is_available() else "cpu")

            t1 = torch.as_tensor(z1, dtype=torch.complex64, device=device)
            t2 = torch.as_tensor(z2, dtype=torch.complex64, device=device)

            numerator = torch.abs(1.0 + t1 * torch.conj(t2))
            denom = torch.sqrt((1.0 + torch.abs(t1)**2) * (1.0 + torch.abs(t2)**2))
            val = torch.clamp(numerator / (denom + 1e-12), -1.0, 1.0)
            return torch.acos(val)
        except Exception:
            # Fallback if PyTorch is unavailable
            if isinstance(z1, (list, tuple)) and isinstance(z2, (list, tuple)):
                return [UnifiedGeometricEngine.fubini_study_distance(complex(a), complex(b)) for a, b in zip(z1, z2)]
            return UnifiedGeometricEngine.fubini_study_distance(complex(z1), complex(z2))

    # ── 2. Hopf Fibration (S3 -> S2) ─────────────────────────────────────────

    @staticmethod
    def hopf_map(q: Tuple[float, float, float, float]) -> Tuple[float, float, float]:
        """
        Hopf fibration mapping a unit 4-vector / quaternion q = (a, b, c, d) in S^3
        down to a 3D point (x, y, z) on the base 2-sphere S^2.
        """
        a, b, c, d = q
        # Normalize to ensure unit quaternion on S3
        norm = math.sqrt(a*a + b*b + c*c + d*d) or 1.0
        a, b, c, d = a/norm, b/norm, c/norm, d/norm

        x = 2.0 * (a * c + b * d)
        y = 2.0 * (b * c - a * d)
        z = (a*a + b*b) - (c*c + d*d)
        return (x, y, z)

    # ── 3. Torus SGD & Geodesics ─────────────────────────────────────────────

    @staticmethod
    def torus_sgd_step(
        theta: float,
        phi: float,
        grad_theta: float,
        grad_phi: float,
        lr: float = 0.05
    ) -> Tuple[float, float]:
        """
        Perform a geodesic gradient step on the 2-torus T^2 = S^1 x S^1.
        Wraps angles into [0, 2*pi).
        """
        two_pi = 2.0 * math.pi
        new_theta = (theta - lr * grad_theta) % two_pi
        new_phi = (phi - lr * grad_phi) % two_pi
        return (new_theta, new_phi)

    # ── 4. Invariant Probes & Evaluation ─────────────────────────────────────

    @staticmethod
    def evaluate_invariants(vec: List[float]) -> Dict[str, float]:
        """
        Compute scalar geometric invariants for a given coordinate/vector.
        Returns: norm, negentropy_score, parity, and phase_angle.
        """
        if not vec:
            return {"norm": 0.0, "negentropy": 0.0, "parity": 1.0, "phase": 0.0}

        norm = math.sqrt(sum(x * x for x in vec))
        mean = sum(vec) / len(vec)
        variance = sum((x - mean) ** 2 for x in vec) / len(vec)
        
        # Negentropy proxy: variance of components
        negentropy = round(variance * 2.5, 4)
        
        # Parity metric (+1 or -1)
        positive_count = sum(1 for x in vec if x >= 0)
        parity = 1.0 if positive_count >= len(vec) / 2 else -1.0
        
        # Phase angle in 2D projection
        v0 = vec[0] if len(vec) > 0 else 0.0
        v1 = vec[1] if len(vec) > 1 else 0.0
        phase = math.atan2(v1, v0)

        return {
            "norm": round(norm, 4),
            "negentropy": negentropy,
            "parity": parity,
            "phase": round(phase, 4)
        }

    # ── 5. E8 Lattice & C60 Vertex Addressing ────────────────────────────────

    # The 60 normalized vertices of the C60 Truncated Icosahedron on S^2
    _PHI = (1.0 + math.sqrt(5.0)) / 2.0
    _C60_RAW_VERTS = [
        (-4.8541, 0.0, -1.0), (-4.8541, 0.0, 1.0), (-4.2361, -1.6180, -2.0),
        (-4.2361, -1.6180, 2.0), (-4.2361, 1.6180, -2.0), (-4.2361, 1.6180, 2.0),
        (-3.6180, -3.2361, -1.0), (-3.6180, -3.2361, 1.0), (-3.6180, 3.2361, -1.0),
        (-3.6180, 3.2361, 1.0), (-3.2361, -1.0, -3.6180), (-3.2361, -1.0, 3.6180),
        (-3.2361, 1.0, -3.6180), (-3.2361, 1.0, 3.6180), (-2.0, -4.2361, -1.6180),
        (-2.0, -4.2361, 1.6180), (-2.0, 4.2361, -1.6180), (-2.0, 4.2361, 1.6180),
        (-1.6180, -2.0, -4.2361), (-1.6180, -2.0, 4.2361), (-1.6180, 2.0, -4.2361),
        (-1.6180, 2.0, 4.2361), (-1.0, -4.8541, 0.0), (-1.0, -3.6180, -3.2361),
        (-1.0, -3.6180, 3.2361), (-1.0, 3.6180, -3.2361), (-1.0, 3.6180, 3.2361),
        (-1.0, 4.8541, 0.0), (0.0, -1.0, -4.8541), (0.0, -1.0, 4.8541),
        (0.0, 1.0, -4.8541), (0.0, 1.0, 4.8541), (1.0, -4.8541, 0.0),
        (1.0, -3.6180, -3.2361), (1.0, -3.6180, 3.2361), (1.0, 3.6180, -3.2361),
        (1.0, 3.6180, 3.2361), (1.0, 4.8541, 0.0), (1.6180, -2.0, -4.2361),
        (1.6180, -2.0, 4.2361), (1.6180, 2.0, -4.2361), (1.6180, 2.0, 4.2361),
        (2.0, -4.2361, -1.6180), (2.0, -4.2361, 1.6180), (2.0, 4.2361, -1.6180),
        (2.0, 4.2361, 1.6180), (3.2361, -1.0, -3.6180), (3.2361, -1.0, 3.6180),
        (3.2361, 1.0, -3.6180), (3.2361, 1.0, 3.6180), (3.6180, -3.2361, -1.0),
        (3.6180, -3.2361, 1.0), (3.6180, 3.2361, -1.0), (3.6180, 3.2361, 1.0),
        (4.2361, -1.6180, -2.0), (4.2361, -1.6180, 2.0), (4.2361, 1.6180, -2.0),
        (4.2361, 1.6180, 2.0), (4.8541, 0.0, -1.0), (4.8541, 0.0, 1.0)
    ]

    @classmethod
    def _get_c60_unit_verts(cls) -> List[Tuple[float, float, float]]:
        unit_verts = []
        for v in cls._C60_RAW_VERTS:
            mag = math.sqrt(v[0]**2 + v[1]**2 + v[2]**2) or 1.0
            unit_verts.append((v[0]/mag, v[1]/mag, v[2]/mag))
        return unit_verts

    @classmethod
    def sphere_to_c60_vertex(cls, X: float, Y: float, Z: float) -> int:
        """
        Given a 3D point (X, Y, Z) on or near S^2, return the index [0..59]
        of the nearest C60 vertex.
        """
        mag = math.sqrt(X*X + Y*Y + Z*Z) or 1.0
        nx, ny, nz = X/mag, Y/mag, Z/mag
        
        best_idx = 0
        best_dist = math.inf
        
        for idx, (vx, vy, vz) in enumerate(cls._get_c60_unit_verts()):
            dist = (nx - vx)**2 + (ny - vy)**2 + (nz - vz)**2
            if dist < best_dist:
                best_dist = dist
                best_idx = idx
                
        return best_idx

    def address_to_e8_slot(self, theta: float, phi: float, sector_offset: int = 0) -> int:
        """
        Map continuous toroidal angles (theta, phi) via S2 projection onto the nearest
        C60 vertex, yielding an exact E8 root slot index in [0, 239].
        """
        # Map toroidal angles (theta, phi) to S2 coordinates
        X = math.cos(theta) * math.sin(phi)
        Y = math.sin(theta) * math.sin(phi)
        Z = math.cos(phi)
        
        v_idx = self.sphere_to_c60_vertex(X, Y, Z)
        # Each C60 vertex holds 4 slots (60 * 4 = 240 E8 root slots)
        slot = (v_idx * 4 + (sector_offset % 4)) % self.slots_count
        return slot
