"""
sov_heart/trivium/nodes/protein_folding_node.py
------------------------------------------------
Office 6 / Biomimetic Node for analyzing amino acid sequences.
Maps amino acids to E8/D4 geometry and tracks folding dynamics via KernelCoordinator.
"""
from typing import Dict, Any, List
import numpy as np
import uuid

from sov_proto.schema.septivium.biology_amino_bridge import BiologyAminoBridge
from sov_heart.trivium.nodes.kernel_coordinator import KernelCoordinator
from sov_heart.trivium.nodes.centroid_engine import EnhancedCentroidEngine

class ProteinFoldingNode:
    """
    Maps amino acid sequences -> E8 trajectories -> stable fold prediction.
    
    Each residue = one WeightedSample in E8 space.
    Backbone path = InferenceChain in KernelCoordinator.
    Folded state = pso_global_best (energy minimum attractor).
    Misfolding = hollow 1-cycle in detect_bifurcation.
    """

    def __init__(self):
        # We instantiate local instances to track the folding state for a particular session
        self.coordinator = KernelCoordinator()
        self.centroid_engine = EnhancedCentroidEngine(enable_lattice_snap=True)

    def fold_sequence(self, sequence: List[str]) -> Dict[str, Any]:
        """
        Takes a sequence of amino acid names (e.g. ['Alanine', 'Glycine', ...])
        and simulates folding using the Sovereign Engine's centroid convergence geometry.
        """
        chain_id = f"protein_chain_{uuid.uuid4().hex[:8]}"
        
        # Determine initial root based on the first amino acid if possible
        init_coord = np.zeros(8)
        if sequence:
            init_coord = BiologyAminoBridge.amino_to_e8(sequence[0])
            
        self.coordinator.register_chain(chain_id, agent_id="folding_node", initial_coordinate=init_coord)
        
        # Traverse backbone
        for residue in sequence:
            coord = BiologyAminoBridge.amino_to_e8(residue)
            # Use hydrophobicity as "gravitational" weight for the centroid engine
            weight = BiologyAminoBridge.HYDROPHOBICITY_WEIGHTS.get(residue, 0.1)
            # Ensure weight is strictly positive to prevent inverse centroid collapse (unless specifically modeled)
            weight = max(weight, 0.01) 
            
            self.coordinator.update_chain(chain_id, coordinate=coord, weight=weight)
            
        # 3. PSO convergence = folding funnel
        swarm_state = self.coordinator.compute_swarm_state()
        
        # 4. Check for topological misfolding (amyloid/prion structures = hollow 1-cycles)
        chain = self.coordinator.get_chain(chain_id)
        bifurcation_info = self.centroid_engine.detect_bifurcation(chain.centroid_history)
        
        is_misfolded = bifurcation_info.get("detected", False)
        misfold_type = bifurcation_info.get("type", "none")
        
        # 5. Extract native fold coordinate
        native_fold = swarm_state.pso_global_best
        if native_fold is None:
            # Fallback to standard centroid if PSO hasn't converged
            native_fold = chain.current_centroid
            
        return {
            "chain_id": chain_id,
            "sequence_length": len(sequence),
            "native_fold_e8": native_fold.tolist() if native_fold is not None else [],
            "misfolded": is_misfolded,
            "misfold_type": misfold_type,
            "swarm_consensus": swarm_state.consensus_strength
        }

