# Tensor-state simulation result

**Status:** `verified`

## Fixture

| Field | Value |
|---|---|
| `manifold` | `X4` |
| `metric` | `diag(-1,1,1,1)` |
| `connection` | `Levi-Civita` |
| `gauge_potential` | `[0.25, -0.5, 0.75, 1.0]` |
| `tolerance` | `1e-12` |

## Numerical outputs

| Quantity | Maximum absolute value / value |
|---|---:|
| `christoffel_max_abs` | `0` |
| `riemann_max_abs` | `0` |
| `ricci_max_abs` | `0` |
| `scalar_curvature` | `0` |
| `einstein_max_abs` | `0` |
| `torsion_max_abs` | `0` |
| `gauge_curvature_max_abs` | `0` |

## Invariant checks

| Check | Result | Residual | Tolerance |
|---|---|---:|---:|
| `manifold.dimension.v1` | `True` | `0` | `1e-12` |
| `metric.symmetry.v1` | `True` | `0` | `1e-12` |
| `metric.inverse.v1` | `True` | `0` | `1e-12` |
| `connection.metric_compatibility.v1` | `True` | `0` | `1e-12` |
| `connection.torsion_free.v1` | `True` | `0` | `1e-12` |
| `curvature.definition.v1` | `True` | `0` | `1e-12` |
| `curvature.ricci.v1` | `True` | `0` | `1e-12` |
| `curvature.einstein.v1` | `True` | `0` | `1e-12` |
| `einstein.bianchi.v1` | `True` | `0` | `1e-12` |
| `gauge.curvature.v1` | `True` | `0` | `1e-12` |
| `gauge.bianchi.v1` | `True` | `0` | `1e-12` |

## Interpretation

The flat Minkowski fixture verifies that the deterministic kernel can carry a Lorentzian metric, derive a zero Levi-Civita connection, compute zero Riemann/Ricci/Einstein curvature, and preserve the torsion-free and gauge-Bianchi invariants under a constant abelian potential. It does not test the unresolved Geometric Unity claims; it tests the software contract and status machinery on a controlled fixture.

## Limitations

- This is a flat numerical fixture, not a validation of Geometric Unity physics.
- The Bianchi checks are zero here because the chosen connection and gauge field are flat.
- A non-flat fixture is required to test nonzero curvature, contractions, and residual behavior.
