import runpy
import sys
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
MODULE = runpy.run_path(str(ROOT / "tools" / "run_m0_sequence_geometry.py"))


def test_poincare_distance_is_nonnegative_and_zero_for_same_point():
    points = np.array([[0.1, 0.2], [0.2, 0.1]])
    same = MODULE["poincare_distance"](points, np.array([0.1, 0.2]))
    assert same[0] >= 0.0
    assert same[0] < 1e-5
    assert same[1] > same[0]


def test_projection_stays_inside_declared_ball():
    matrix = np.array([[1.0, 2.0], [3.0, 4.0]])
    projected = MODULE["_project_to_ball"](matrix)
    assert np.linalg.norm(projected, axis=1).max() <= MODULE["BALL_RADIUS"] + 1e-12
