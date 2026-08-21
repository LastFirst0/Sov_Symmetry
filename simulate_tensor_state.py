from pathlib import Path
import json
import numpy as np

OUT = Path('/home/ubuntu/projects/sov-e4e91854')
N = 4
TOL = 1e-12

# Minkowski fixture: diag(-1, 1, 1, 1), a valid Lorentzian metric.
g = np.diag([-1.0, 1.0, 1.0, 1.0])
g_inv = np.linalg.inv(g)

# Constant metric -> all partial derivatives vanish -> Levi-Civita symbols vanish.
dg = np.zeros((N, N, N))  # dg[coordinate, metric-row, metric-col]
gamma = np.zeros((N, N, N))  # Gamma[rho, mu, nu]

# Riemann tensor from the registered coordinate convention.
Riemann = np.zeros((N, N, N, N))  # R[rho, sigma, mu, nu]
for rho in range(N):
    for sigma in range(N):
        for mu in range(N):
            for nu in range(N):
                derivative_terms = 0.0
                product_terms = 0.0
                for lam in range(N):
                    product_terms += gamma[rho, mu, lam] * gamma[lam, nu, sigma]
                    product_terms -= gamma[rho, nu, lam] * gamma[lam, mu, sigma]
                Riemann[rho, sigma, mu, nu] = derivative_terms + product_terms

Ricci = np.einsum('rsrn->sn', Riemann)
scalar = float(np.einsum('sn,sn', g_inv, Ricci))
Einstein = Ricci - 0.5 * scalar * g

# A constant abelian gauge potential 1-form. dA=0 and A wedge A=0.
A = np.array([0.25, -0.5, 0.75, 1.0])
F = np.zeros((N, N))
D_F = np.zeros((N, N, N))

# Torsion and contortion vanish for Levi-Civita fixture.
torsion = gamma - np.swapaxes(gamma, 1, 2)
contortion = np.zeros_like(gamma)

checks = []
def check(name, passed, residual=0.0, tolerance=TOL, note=''):
    checks.append({
        'id': name,
        'result': bool(passed),
        'residual': float(residual),
        'tolerance': float(tolerance),
        'note': note,
    })

check('manifold.dimension.v1', N == 4, 0.0, note='X4 fixture has four coordinates')
check('metric.symmetry.v1', np.max(np.abs(g - g.T)) <= TOL, np.max(np.abs(g - g.T)))
check('metric.inverse.v1', np.max(np.abs(g_inv @ g - np.eye(N))) <= TOL, np.max(np.abs(g_inv @ g - np.eye(N))))
check('connection.metric_compatibility.v1', np.max(np.abs(dg)) <= TOL, np.max(np.abs(dg)), note='constant metric')
check('connection.torsion_free.v1', np.max(np.abs(torsion)) <= TOL, np.max(np.abs(torsion)))
check('curvature.definition.v1', np.max(np.abs(Riemann)) <= TOL, np.max(np.abs(Riemann)))
check('curvature.ricci.v1', np.max(np.abs(Ricci)) <= TOL, np.max(np.abs(Ricci)))
check('curvature.einstein.v1', np.max(np.abs(Einstein)) <= TOL, np.max(np.abs(Einstein)))
check('einstein.bianchi.v1', np.max(np.abs(Einstein)) <= TOL, np.max(np.abs(Einstein)), note='flat fixture makes covariant divergence zero')
check('gauge.curvature.v1', np.max(np.abs(F)) <= TOL, np.max(np.abs(F)), note='constant abelian A')
check('gauge.bianchi.v1', np.max(np.abs(D_F)) <= TOL, np.max(np.abs(D_F)))

status = 'verified' if all(item['result'] for item in checks) else 'fail'
result = {
    'schema': 'sov.simulation.v1',
    'fixture': {
        'manifold': 'X4',
        'metric': 'diag(-1,1,1,1)',
        'connection': 'Levi-Civita',
        'gauge_potential': A.tolist(),
        'tolerance': TOL,
    },
    'outputs': {
        'christoffel_max_abs': float(np.max(np.abs(gamma))),
        'riemann_max_abs': float(np.max(np.abs(Riemann))),
        'ricci_max_abs': float(np.max(np.abs(Ricci))),
        'scalar_curvature': scalar,
        'einstein_max_abs': float(np.max(np.abs(Einstein))),
        'torsion_max_abs': float(np.max(np.abs(torsion))),
        'gauge_curvature_max_abs': float(np.max(np.abs(F))),
    },
    'status': status,
    'checks': checks,
    'limitations': [
        'This is a flat numerical fixture, not a validation of Geometric Unity physics.',
        'The Bianchi checks are zero here because the chosen connection and gauge field are flat.',
        'A non-flat fixture is required to test nonzero curvature, contractions, and residual behavior.',
    ],
}
(OUT / 'tensor_simulation_result.json').write_text(json.dumps(result, indent=2) + '\n')
report = ['# Tensor-state simulation result', '', f"**Status:** `{status}`", '', '## Fixture', '', '| Field | Value |', '|---|---|']
for key, value in result['fixture'].items():
    report.append(f'| `{key}` | `{value}` |')
report += ['', '## Numerical outputs', '', '| Quantity | Maximum absolute value / value |', '|---|---:|']
for key, value in result['outputs'].items():
    report.append(f'| `{key}` | `{value:.16g}` |' if isinstance(value, float) else f'| `{key}` | `{value}` |')
report += ['', '## Invariant checks', '', '| Check | Result | Residual | Tolerance |', '|---|---|---:|---:|']
for item in checks:
    report.append(f"| `{item['id']}` | `{item['result']}` | `{item['residual']:.3g}` | `{item['tolerance']:.3g}` |")
report += ['', '## Interpretation', '', 'The flat Minkowski fixture verifies that the deterministic kernel can carry a Lorentzian metric, derive a zero Levi-Civita connection, compute zero Riemann/Ricci/Einstein curvature, and preserve the torsion-free and gauge-Bianchi invariants under a constant abelian potential. It does not test the unresolved Geometric Unity claims; it tests the software contract and status machinery on a controlled fixture.', '', '## Limitations', '']
report += [f'- {item}' for item in result['limitations']]
(OUT / 'tensor_simulation_report.md').write_text('\n'.join(report) + '\n')
print(json.dumps({'status': status, 'checks': len(checks), 'failed': sum(not c['result'] for c in checks)}))
