"""
sov_heart/trivium/nodes/materials_discovery_node.py
---------------------------------------------------
A node for querying the NOMAD API and local Supercon datasets to find 
geometric attractors in crystalline structures. It translates material 
properties (band gaps, densities, elements) into E8 vectors for swarm processing.
"""

import os
import csv
import json
import uuid
import logging
import urllib.request
import urllib.parse
import numpy as np
from typing import Dict, Any, List
from pathlib import Path

from sov_heart.trivium.nodes.kernel_coordinator import KernelCoordinator
from sov_heart.trivium.nodes.centroid_engine import EnhancedCentroidEngine

logger = logging.getLogger(__name__)

class MaterialsDiscoveryNode:
    def __init__(self):
        project_root = Path(__file__).parent.parent.parent.parent
        self.coordinator = KernelCoordinator()
        self.centroid_engine = EnhancedCentroidEngine(enable_lattice_snap=True)
        self.supercon_path = str(project_root / "data" / "Supercon_data.csv")
        self.nomad_base_url = "https://nomad-lab.eu/prod/v1/api/v1"
        self.mp_base_url = "https://api.materialsproject.org/materials/summary/"
        
        # Load API key directly from environment if not passed explicitly, or attempt to read .env
        self.mp_api_key = os.getenv("MP_API_KEY")
        if not self.mp_api_key:
            # Fallback for when the background task hasn't re-sourced .env
            env_path = str(project_root / ".env")
            if os.path.exists(env_path):
                with open(env_path, "r") as f:
                    for line in f:
                        if line.startswith("MP_API_KEY="):
                            self.mp_api_key = line.split("=", 1)[1].strip().strip('"').strip("'")
                            break

    def _map_material_to_e8(self, properties: Dict[str, Any]) -> np.ndarray:
        """
        Translates raw physical material properties into an E8 vector.
        This uses basic dimensionality embedding for structural parameters.
        """
        vec = np.zeros(8, dtype=float)
        
        # 1. Band gap (if available) maps to dimension 0
        bg = properties.get("band_gap", 0.0)
        vec[0] = float(bg) if bg is not None else 0.0
        
        # 2. Lattice volume / density maps to dimension 1
        vol = properties.get("cell_volume", 0.0)
        vec[1] = float(vol) if vol is not None else 0.0
        
        # 3. Superconducting Tc maps to dimension 2 (for Supercon data)
        tc = properties.get("tc", 0.0)
        vec[2] = float(tc) if tc is not None else 0.0
        
        # Normalize to prevent explosion, but keep scale relative
        norm = np.linalg.norm(vec)
        if norm > 0:
            # We scale it back down so it doesn't break E8 snapping thresholds
            vec = (vec / norm) * min(norm, 2.0)
            
        return vec

    def query_nomad(self, query_params: Dict[str, Any], max_results: int = 10) -> List[Dict[str, Any]]:
        """
        Queries the public NOMAD API for crystal structures matching the params.
        """
        url = f"{self.nomad_base_url}/entries/query"
        payload = {
            "owner": "public",
            "query": query_params,
            "pagination": {"page_size": max_results}
        }
        
        req = urllib.request.Request(url, method="POST")
        req.add_header('Content-Type', 'application/json')
        req.add_header('Accept', 'application/json')
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
        
        data = json.dumps(payload).encode('utf-8')
        
        materials = []
        try:
            with urllib.request.urlopen(req, data=data) as response:
                result = json.loads(response.read().decode('utf-8'))
                for entry in result.get('data', []):
                    results = entry.get('results', {})
                    props = results.get('properties', {})
                    elec = props.get('electronic', {})
                    mat = results.get('material', {})
                    
                    bg = elec.get('band_gap', [{}])[0].get('value', 0.0) if elec.get('band_gap') else 0.0
                    vol = mat.get('topology', [{}])[0].get('cell', {}).get('volume', 0.0) if mat.get('topology') else 0.0
                    formula = mat.get('formula_hill', 'Unknown')
                    
                    materials.append({
                        "formula": formula,
                        "band_gap": bg,
                        "cell_volume": vol,
                        "source": "NOMAD"
                    })
        except Exception as e:
            logger.error(f"Failed to query NOMAD API: {e}")
            
        return materials

    def query_supercon_local(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Reads local Supercon_data.csv for high-Tc superconductors.
        """
        materials = []
        if not os.path.exists(self.supercon_path):
            logger.warning(f"Supercon database not found at {self.supercon_path}")
            return materials

        try:
            with open(self.supercon_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for i, row in enumerate(reader):
                    if i >= limit:
                        break
                    
                    try:
                        tc = float(row.get('Tc', 0.0))
                    except ValueError:
                        tc = 0.0
                        
                    materials.append({
                        "formula": row.get('name', 'Unknown'),
                        "tc": tc,
                        "source": "Supercon"
                    })
        except Exception as e:
            logger.error(f"Failed to read Supercon database: {e}")
            
        return materials

    def query_materials_project(self, elements: List[str], max_results: int = 10) -> List[Dict[str, Any]]:
        """
        Queries the Materials Project API for crystalline summaries.
        Requires self.mp_api_key to be set.
        """
        materials = []
        if not self.mp_api_key:
            logger.warning("MP_API_KEY is not set. Skipping Materials Project query.")
            return materials
            
        try:
            # Format elements for query: e.g. "Fe,O"
            elements_str = ",".join(elements)
            url = f"{self.mp_base_url}?elements={elements_str}&_limit={max_results}&_fields=formula_pretty,band_gap,volume,energy_above_hull"
            
            req = urllib.request.Request(url, method="GET")
            req.add_header('X-API-KEY', self.mp_api_key)
            req.add_header('Accept', 'application/json')
            req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
            
            with urllib.request.urlopen(req) as response:
                result = json.loads(response.read().decode('utf-8'))
                for entry in result.get('data', []):
                    materials.append({
                        "formula": entry.get("formula_pretty", "Unknown"),
                        "band_gap": float(entry.get("band_gap", 0.0) or 0.0),
                        "cell_volume": float(entry.get("volume", 0.0) or 0.0),
                        # Use energy_above_hull to influence geometric weight (lower is more stable)
                        "tc": max(0.0, 1.0 - float(entry.get("energy_above_hull", 1.0) or 1.0)), 
                        "source": "MaterialsProject"
                    })
        except Exception as e:
            logger.error(f"Failed to query Materials Project API: {e}")
            
        return materials

    def analyze_materials(self, materials: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Feeds a list of materials into the swarm coordinator to find
        the 'geometric center' or 'attractor' of the group.
        """
        if not materials:
            return {"chain_id": None, "attractor_e8": [], "consensus": 0.0, "misfolded": False}
            
        chain_id = f"materials_chain_{uuid.uuid4().hex[:8]}"
        
        # Initialize chain
        init_vec = self._map_material_to_e8(materials[0])
        self.coordinator.register_chain(chain_id, agent_id="materials_node", initial_coordinate=init_vec)
        
        for mat in materials:
            vec = self._map_material_to_e8(mat)
            # Use Tc or band gap to influence the weight (gravitational pull)
            weight = max(0.1, mat.get("tc", 0.0) / 100.0) if "tc" in mat else 1.0
            self.coordinator.update_chain(chain_id, coordinate=vec, weight=weight)
            
        swarm_state = self.coordinator.compute_swarm_state()
        
        chain = self.coordinator.get_chain(chain_id)
        bifurcation = self.centroid_engine.detect_bifurcation(chain.centroid_history)
        
        attractor = swarm_state.pso_global_best
        if attractor is None:
            attractor = chain.current_centroid
            
        return {
            "chain_id": chain_id,
            "materials_count": len(materials),
            "attractor_e8": attractor.tolist() if attractor is not None else [],
            "consensus": swarm_state.consensus_strength,
            "misfolded": bifurcation.get("detected", False)
        }
