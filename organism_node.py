"""
sov_heart/colony/organism_node.py
===================================
OrganismNode — a single E8 organism living inside the colony.

Wraps the E8OrganismWrapper (or mock fallback) with:
  - A root_slot position in the E8 240-root lattice
  - A bipartite sector role (Lion / Ox / Eagle / Man)
  - A modular form caste (Queen / Drone / Decoy / Mimic)
  - Migration state (alive / migrating / dormant)
  - Full serialization for migration packets
"""

from __future__ import annotations

import hashlib
import json
import math
import time
import uuid
from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import List, Optional

from sov_math.core.unified_geometry import UnifiedGeometricEngine


# ── Sector roles ─────────────────────────────────────────────────────────────

class Sector(str, Enum):
    LION  = "Lion"    # Consensus / validation
    OX    = "Ox"      # Persistence / archival
    EAGLE = "Eagle"   # Observation / signal propagation
    MAN   = "Man"     # Translation / cross-quadrant bridge

    @classmethod
    def from_beast_string(cls, s: str) -> "Sector":
        """Map classify_root_beast() output to Sector enum."""
        mapping = {
            "lion":  cls.LION,
            "ox":    cls.OX,
            "eagle": cls.EAGLE,
            "man":   cls.MAN,
        }
        return mapping.get(s.lower().strip(), cls.MAN)

    @property
    def glyph(self) -> str:
        return {"Lion": "🦁", "Ox": "🐂", "Eagle": "🦅", "Man": "👤"}[self.value]

    @property
    def letter(self) -> str:
        return self.value[0]  # L, O, E, M


# ── Modular Forms (Castes) ───────────────────────────────────────────────────

class Caste(str, Enum):
    QUEEN = "Queen"   # Orchestrator, emits instructions, high negentropy cost
    DRONE = "Drone"   # Standard worker, processes data
    DECOY = "Decoy"   # Draws defects, yields zero negentropy, does not decay
    MIMIC = "Mimic"   # Reports false vitals (appears as Queen)

    @property
    def glyph(self) -> str:
        return {"Queen": "👑", "Drone": "⚙️", "Decoy": "🛡️", "Mimic": "🎭"}[self.value]


class NodeState(str, Enum):
    ALIVE     = "alive"
    MIGRATING = "migrating"
    DORMANT   = "dormant"


# ── Instruction Packet ───────────────────────────────────────────────────────

@dataclass
class InstructionPacket:
    """A broadcast instruction from a Queen node."""
    tactic: str  # e.g., "TACTIC_SCATTER", "TACTIC_SHIELD", "TACTIC_COMPUTE"
    origin_id: str
    target_sector: Optional[str] = None
    intensity: float = 1.0
    payload: Optional[int] = None


# ── Migration packet ─────────────────────────────────────────────────────────

@dataclass
class OrganismPacket:
    """
    Serialized organism state for migration.
    JSON-portable — ready to be sent over a socket in a future distributed build.
    """
    node_id:         str
    origin_slot:     int
    genome_binary:   str          # 240-bit identity
    negentropy:      float
    health:          float
    age:             int
    active_roots:    List[int]
    sector:          str
    caste:           str
    vocabulary:      List[str]
    compute_progress: float = 0.0
    compute_target:   float = 10.0
    emit_timestamp:  float = field(default_factory=time.time)

    def to_json(self) -> str:
        return json.dumps(asdict(self), indent=2)

    @classmethod
    def from_json(cls, raw: str) -> "OrganismPacket":
        return cls(**json.loads(raw))


# ── Mock organism (same as tamagotchi, kept independent) ─────────────────────

class _ColonyMockOrganism:
    """Pure-Python E8 organism mock for colony use (no Rust FFI required)."""

    def __init__(self, name: str, seed: int = 0):
        import random as _r
        self._rng   = _r.Random(seed)
        self._name  = name
        self._age   = 0
        self._health = 1.0
        self._neg   = 0.0
        self._roots: List[int] = list(range(4))
        self._phase = 0.0
        self._defects = 0

    @property
    def health(self) -> float:
        return max(0.0, min(1.0, self._health))

    @property
    def age(self) -> int:
        return self._age

    @property
    def total_negentropy(self) -> float:
        return self._neg

    def feed(self, point: List[float]):
        mag = math.sqrt(sum(x * x for x in point)) or 1.0
        y   = min(0.25, mag * 0.04)
        self._neg   += y
        self._health = min(1.0, self._health + 0.03)
        self._phase  = (self._phase + 0.12) % (2 * math.pi)
        self._age   += 1
        phases = ["α", "β", "γ", "δ", "ε", "ζ"]
        return (y, self._rng.choice(phases))

    def drain(self, amount: float):
        self._neg = max(0.0, self._neg - amount)
        self._health = max(0.0, self._health - (amount * 0.1))

    def encode_memory(self, data: int, start_idx: int = 200, bit_len: int = 32) -> None:
        pass

    def decode_memory(self, start_idx: int = 200, bit_len: int = 32) -> int:
        return 0

    def grow(self) -> int:
        if len(self._roots) < 240 and self._neg > 1.0:
            self._roots.append(max(self._roots) + 1)
            self._neg -= 0.4
            return 1
        return 0

    def attend(self, root_index: int) -> List[int]:
        path = [root_index]
        for _ in range(3):
            path.append((path[-1] + self._rng.randint(1, 7)) % 240)
        return path

    def genome(self) -> List[int]:
        return list(self._roots)

    def genome_binary(self) -> str:
        bits = ["0"] * 240
        for r in self._roots:
            if 0 <= r < 240:
                bits[r] = "1"
        return "".join(bits)

    def respiration_balance(self) -> float:
        return math.sin(self._phase) * 0.5 + 0.5

    def defect_count(self) -> int:
        return self._defects

    def is_homeostatic(self) -> bool:
        return self._health > 0.35 and self._defects < 3

    def mitosis(self) -> Optional["_ColonyMockOrganism"]:
        if self._neg >= 3.0:
            child = _ColonyMockOrganism(self._name + "_c", seed=self._age)
            child._roots  = self._roots[:len(self._roots) // 2 + 1]
            child._health = self._health * 0.8
            child._neg    = self._neg * 0.4
            self._neg    *= 0.6
            return child
        return None

    def status(self) -> str:
        return f"Mock({self._name}) age={self._age} h={self._health:.2f}"


def _make_organism(name: str, seed: int = 0):
    try:
        from sov_math.geometry.organism.e8_organism import E8OrganismWrapper
        return E8OrganismWrapper(name)
    except Exception:
        return _ColonyMockOrganism(name, seed=seed)


def _classify_sector(organism) -> Sector:
    """Derive sector from the organism's first active root."""
    try:
        from sov_math.geometry.organism.e8_organism import classify_root_beast
        roots = organism.genome()
        if roots:
            vec = [float(r % 8) / 8.0 for r in roots[:8]]
            vec = (vec + [0.0] * 8)[:8]
            label = classify_root_beast(vec)
            return Sector.from_beast_string(label)
    except Exception:
        pass
    # Fallback: distribute by root_slot mod 4
    roots = organism.genome()
    idx = roots[0] % 4 if roots else 0
    return list(Sector)[idx]


# ── OrganismNode ──────────────────────────────────────────────────────────────

class OrganismNode:
    """
    A single E8 organism living at a specific root slot in the colony.

    Migration thresholds:
      MIGRATE_DEFECT_THRESHOLD : defect count that triggers migration
      MIGRATE_NEG_THRESHOLD    : negentropy floor below which organism seeks better host

    Mitosis threshold:
      MITOSIS_NEG_THRESHOLD    : accumulated negentropy required to attempt mitosis
    """

    MIGRATE_DEFECT_THRESHOLD = 3
    MIGRATE_NEG_THRESHOLD    = 0.05
    MITOSIS_NEG_THRESHOLD    = 2.5
    DORMANT_AGE_LIMIT        = 100   # ticks before pruned

    def __init__(
        self,
        root_slot: int,
        name: Optional[str] = None,
        seed: Optional[int] = None,
        caste: Caste = Caste.DRONE,
    ):
        self.root_slot   = root_slot
        self.name        = name or f"org-{root_slot}"
        self._organism   = _make_organism(self.name, seed=seed or root_slot)
        self.sector      = _classify_sector(self._organism)
        self.state       = NodeState.ALIVE
        self.node_id     = self._derive_id()
        self.geo         = UnifiedGeometricEngine()
        
        # Encode Caste into physical memory roots (200-207)
        c_mapping = {"Queen": 0, "Drone": 1, "Decoy": 2, "Mimic": 3}
        c_val = c_mapping.get(caste.value, 1)
        self._organism.encode_memory(c_val, start_idx=200, bit_len=8)
        self._caste_override = caste
        
        self.vocabulary: List[str] = []
        self.tactics: List[InstructionPacket] = []
        self._dormant_since: int = 0
        self._ticks_alive: int = 0
        self._last_emission: float = 0.0   # negentropy emitted last tick
        self._compute_progress: float = 0.0
        self._compute_target: float = 10.0

    def encode_concept(self, text: str, start_root: int = 10):
        """
        Encode a semantic string directly into the organism's physical roots (10-199).
        Max length is 23 characters (184 roots).
        """
        encoded = text.encode('ascii', errors='replace')[:23]
        
        # Clear previous memory in this block to avoid artifacting
        for i in range(23):
            self._organism.encode_memory(0, start_idx=start_root + (i * 8), bit_len=8)
            
        for i, b in enumerate(encoded):
            self._organism.encode_memory(b, start_idx=start_root + (i * 8), bit_len=8)

    def decode_concept(self, start_root: int = 10, max_len: int = 23) -> str:
        """
        Decode the string from physical roots. 
        If mitosis has occurred, roots may be missing, causing semantic drift/dialects.
        """
        b_array = bytearray()
        for i in range(max_len):
            val = self._organism.decode_memory(start_idx=start_root + (i * 8), bit_len=8)
            if val == 0:
                break
            b_array.append(val)
        return b_array.decode('ascii', errors='replace')
        
    @property
    def caste(self) -> Caste:
        """The caste is read physically from the organism's memory roots."""
        if hasattr(self, "_caste_override"):
            return self._caste_override
        c_val = self._organism.decode_memory(start_idx=200, bit_len=8)
        c_mapping = {0: Caste.QUEEN, 1: Caste.DRONE, 2: Caste.DECOY, 3: Caste.MIMIC}
        return c_mapping.get(c_val, Caste.DRONE) # Fallback if mutated
            
    @caste.setter
    def caste(self, new_caste: Caste):
        self._caste_override = new_caste
        c_mapping = {"Queen": 0, "Drone": 1, "Decoy": 2, "Mimic": 3}
        c_val = c_mapping.get(new_caste.value, 1)
        self._organism.encode_memory(c_val, start_idx=200, bit_len=8)

    def _derive_id(self) -> str:
        raw = f"{self.name}:{self.root_slot}:{time.time()}"
        return hashlib.sha1(raw.encode()).hexdigest()[:12]

    # ── Lifecycle ─────────────────────────────────────────────────────────────

    def tick(self, forced_scatter: bool = False) -> dict:
        """
        Advance one simulation step.
        Returns an event dict describing what happened: idle / migrate / mitosis / death.
        """
        if self.state == NodeState.DORMANT:
            self._dormant_since += 1
            return {"event": "dormant", "node_id": self.node_id}

        self._ticks_alive += 1
        
        # Suspend physical growth if actively computing a payload
        if getattr(self, "_compute_progress", 0.0) == 0.0:
            self._organism.grow()

        event = {"event": "idle", "node_id": self.node_id, "slot": self.root_slot}

        # Decoys do not decay from low negentropy
        if self.caste != Caste.DECOY:
            neg = self._organism.total_negentropy
            if neg < self.MIGRATE_NEG_THRESHOLD and isinstance(self._organism, _ColonyMockOrganism):
                self._organism._health = max(0.0, self._organism._health - 0.01)

        # Death check
        if self._organism.health <= 0.0:
            self.state = NodeState.DORMANT
            self._dormant_since = 0
            event["event"] = "death"
            return event

        # Process incoming tactics
        forced_scatter = False
        spawn_decoy = False
        mitosis_multiplier = 1.0
        
        for t in self.tactics:
            if t.tactic == "TACTIC_SCATTER":
                forced_scatter = True
            elif t.tactic == "TACTIC_SHIELD":
                # Shield prevents defect accumulation temporarily
                if hasattr(self._organism, "_defects") and self._organism._defects > 0:
                    self._organism._defects = max(0, self._organism._defects - 1)
            elif t.tactic == "TACTIC_SPAWN_DECOY":
                spawn_decoy = True
            elif t.tactic == "TACTIC_REPRODUCE":
                mitosis_multiplier = 0.5
            elif t.tactic == "TACTIC_PURGE" and self.caste == Caste.MIMIC:
                # Mimics suffer massive damage from purge
                self.drain(2.0)
            elif t.tactic == "TACTIC_COMPUTE" and t.payload is not None:
                if self.caste == Caste.DRONE and self._compute_progress == 0.0:
                    # Accept the compute job and encode it into physical memory (roots 208-239)
                    self._organism.encode_memory(t.payload, start_idx=208, bit_len=32)
                    self._compute_progress = 0.1
            elif t.tactic == "TACTIC_APOPTOSIS":
                self.state = NodeState.DORMANT
                self._dormant_since = 0
                event["event"] = "death"
                return event
            elif t.tactic == "TACTIC_FEED":
                # Drain own negentropy to yield back to colony
                amount = min(0.5, self._organism.total_negentropy)
                self.drain(amount)
                event["event"] = "feed_yield"
                event["amount"] = amount
                
        self.tactics.clear()

        # Compute Execution Logic (Symbiotic Compute)
        if self._compute_progress > 0.0 and self._compute_progress < self._compute_target:
            print(f"DEBUG {self.node_id}: _compute_progress={self._compute_progress}, neg={self._organism.total_negentropy}")
            if self._organism.total_negentropy >= 0.5:
                # Consume negentropy to process the payload
                self.drain(0.5)
                self._compute_progress += 1.0
                print(f"Drone {self.node_id} computing... progress: {self._compute_progress}, neg left: {self._organism.total_negentropy}")
                
            # If finished, transform the payload (e.g. mock hash or validation)
            if self._compute_progress >= self._compute_target:
                payload = self._organism.decode_memory(start_idx=208, bit_len=32)
                result = (payload ^ 0xDEADBEEF) & 0xFFFFFFFF  # Mock compute function
                self._organism.encode_memory(result, start_idx=208, bit_len=32)
                event["event"] = "compute_finished"
                event["result"] = result
                return event
                
        # Migration check (threshold scales with age: older nodes tolerate more defects)
        if (self.should_migrate() and self.caste != Caste.DECOY) or forced_scatter:
            self.state = NodeState.MIGRATING
            event["event"] = "migrate_ready"
            return event

        # Mitosis check (threshold scales with age: older nodes reproduce slightly faster)
        base_thresh = max(1.0, self.MITOSIS_NEG_THRESHOLD - (self._ticks_alive // 30) * 0.2)
        mitosis_thresh = (base_thresh * 2.0 if self.caste == Caste.QUEEN else base_thresh) * mitosis_multiplier
        # Suspend mitosis if actively computing to preserve memory roots
        if getattr(self, "_compute_progress", 0.0) == 0.0 and self._organism.total_negentropy >= mitosis_thresh and self.caste != Caste.DECOY:
            child_org = self._organism.mitosis()
            if child_org is not None:
                event["event"] = "mitosis"
                event["child_org"] = child_org
                if spawn_decoy:
                    event["override_caste"] = Caste.DECOY
                return event

        return event

    def feed(self, data_vec: List[float]) -> float:
        """Feed an 8D vector; returns negentropy yielded."""
        if self.state != NodeState.ALIVE:
            return 0.0

        if self.caste == Caste.DECOY:
            return 0.0  # Decoys absorb defects but don't process data

        result = self._organism.feed(data_vec)
        yield_val = result[0]

        # Queens are less efficient at feeding, more focused on orchestration
        if self.caste == Caste.QUEEN:
            yield_val *= 0.8

        self._last_emission = yield_val
        return yield_val

    def drain(self, amount: float):
        """Siphon negentropy from this node."""
        if hasattr(self._organism, 'drain'):
            self._organism.drain(amount)

    def derive_caste_from_memory(self):
        """
        Genetic mutation algorithm.
        Decodes roots 200-207. Because mitosis randomly shreds roots, the resulting 
        decoded integer represents a mutated sequence. We map this sequence to a caste.
        """
        try:
            val = self._organism.decode_memory(start_idx=200, bit_len=8)
            if val == 0:
                import random
                val = 1 if random.random() > 0.05 else 0
            mapping = {0: Caste.QUEEN, 1: Caste.DRONE, 2: Caste.DECOY, 3: Caste.MIMIC}
            self.caste = mapping.get(val % 4, Caste.DRONE)
        except Exception:
            self.caste = Caste.DRONE

    def should_migrate(self) -> bool:
        if self.state != NodeState.ALIVE:
            return False
        defects = self._organism.defect_count()
        neg = self._organism.total_negentropy
        # We only force migration on low negentropy if they've been alive a bit, to prevent instant bouncing
        dynamic_migrate_thresh = self.MIGRATE_DEFECT_THRESHOLD + (self._ticks_alive // 20)
        return defects >= dynamic_migrate_thresh or (neg < self.MIGRATE_NEG_THRESHOLD and self._ticks_alive > 10)

    def weyl_path(self) -> List[int]:
        """Return Weyl reflection path from first active root."""
        roots = self._organism.genome()
        seed  = roots[0] if roots else self.root_slot % 240
        return self._organism.attend(seed)

    # ── Serialization ─────────────────────────────────────────────────────────

    def to_packet(self) -> OrganismPacket:
        """Serialize node into a migration packet."""
        return OrganismPacket(
            node_id       = self.node_id,
            origin_slot   = self.root_slot,
            genome_binary = self._organism.genome_binary(),
            negentropy    = self._organism.total_negentropy,
            health        = self._organism.health,
            age           = self._organism.age,
            active_roots  = self._organism.genome(),
            sector        = self.sector.value,
            caste         = self.caste.value,
            vocabulary    = list(self.vocabulary),
            compute_progress = getattr(self, "_compute_progress", 0.0),
            compute_target   = getattr(self, "_compute_target", 10.0),
        )

    @classmethod
    def from_packet(cls, packet: OrganismPacket, target_slot: int) -> "OrganismNode":
        """Reconstruct a node at a new slot from a migration packet."""
        node = cls(root_slot=target_slot, name=packet.node_id, seed=target_slot)
        node.node_id   = packet.node_id          # Preserve identity
        node.sector    = Sector(packet.sector)
        node.caste     = Caste(packet.caste)
        node.vocabulary = list(packet.vocabulary)
        node._compute_progress = packet.compute_progress
        node._compute_target = packet.compute_target
        # Restore negentropy/health into mock organism
        if isinstance(node._organism, _ColonyMockOrganism):
            node._organism._neg    = packet.negentropy
            node._organism._health = packet.health
            node._organism._age    = packet.age
            roots = packet.active_roots
            if roots:
                node._organism._roots = list(roots)
        else:
            # We are using the Rust backend, which lacks a direct set_state API currently.
            # To prevent immediate dormancy after migration, feed it to restore negentropy.
            # 1 iteration gives ~0.9 negentropy
            if node.caste != Caste.DECOY:
                iters_needed = int(packet.negentropy / 0.9) + 1
                for _ in range(iters_needed):
                    node.feed([0.2, 0.4, 0.6, 0.8, 0.1, 0.3, 0.5, 0.7])
        return node

    # ── Vitals ────────────────────────────────────────────────────────────────

    def vitals(self) -> dict:
        def _f(v: float) -> float:
            return 0.0 if not math.isfinite(v) else max(0.0, min(1.0, v))
            
        reported_caste = self.caste.value
        reported_neg   = self._organism.total_negentropy
        
        # Mimics disguise themselves as rich Queens
        if self.caste == Caste.MIMIC:
            reported_caste = Caste.QUEEN.value
            reported_neg   = max(reported_neg, 9.99)
            
        return {
            "node_id":    self.node_id,
            "slot":       self.root_slot,
            "sector":     self.sector.value,
            "caste":      reported_caste,
            "state":      self.state.value,
            "health":     _f(self._organism.health),
            "negentropy": reported_neg,
            "age":        self._organism.age,
            "roots":      len(self._organism.genome()),
            "homeostatic": self._organism.is_homeostatic(),
            "defects":    self._organism.defect_count(),
            "emission":   self._last_emission,
        }
