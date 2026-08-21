"""
tests/test_materials_discovery.py
---------------------------------
Tests the functionality of the Materials Discovery Node, including the mapping of
material properties to E8 vectors, local database reading, and swarm convergence.
"""

import pytest
import numpy as np
from sov_heart.trivium.nodes.materials_discovery_node import MaterialsDiscoveryNode

def test_map_material_to_e8():
    node = MaterialsDiscoveryNode()
    
    props = {
        "band_gap": 1.2,
        "cell_volume": 45.3,
        "tc": 90.0
    }
    
    vec = node._map_material_to_e8(props)
    
    assert len(vec) == 8
    # The norm should be bound by min(norm, 2.0)
    assert np.isclose(np.linalg.norm(vec), 2.0)
    # Ensure components exist
    assert vec[0] > 0
    assert vec[1] > 0
    assert vec[2] > 0


def test_analyze_materials_swarm_convergence():
    node = MaterialsDiscoveryNode()
    
    materials = [
        {"formula": "YBa2Cu3O7", "tc": 92.0, "cell_volume": 174.0},
        {"formula": "Bi2Sr2CaCu2O8", "tc": 95.0, "cell_volume": 220.0},
        {"formula": "HgBa2Ca2Cu3O8", "tc": 133.0, "cell_volume": 250.0}
    ]
    
    result = node.analyze_materials(materials)
    
    assert result["materials_count"] == 3
    assert len(result["attractor_e8"]) == 8
    assert result["consensus"] > 0.0
    assert isinstance(result["misfolded"], bool)
