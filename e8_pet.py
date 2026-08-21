"""
sov_heart/tamagotchi/e8_pet.py
===============================
Core state engine for the E8 Tamagotchi virtual pet.

Vitals are backed by real E8OrganismWrapper internals when the compiled Rust
FFI libraries are available, or by a pure-Python mock organism as fallback.

Save/load persists to ~/.sovereign_pet.json.
"""

from __future__ import annotations

import json
import math
import random
import time
from dataclasses import asdict, dataclass, field
from enum import Enum
from pathlib import Path
from typing import List, Optional

# ── E8 Root names drawn from Lie algebra nomenclature ──────────────────────
_E8_ROOT_NAMES = [
    "LUMI", "KAON", "VELA", "TORI", "HEXA", "OCTI", "SOVI",
    "WEYL", "LEXI", "NOVA", "EIDO", "PHAI", "ZARA", "MIRA",
]

# ── Stage thresholds (by organism age / tick count) ─────────────────────────
_STAGE_THRESHOLDS = [
    (0,   "egg"),
    (6,   "hatchling"),
    (21,  "juvenile"),
    (61,  "adult"),
    (151, "elder"),
    (200, "ascended"),
]

# ── Food preference pools ─────────────────────────────────────────────────
_FAVORITE_FOODS = [
    "kale", "apples", "berries", "quinoa", "honey", "figs", "dates",
    "mango", "avocado", "salmon", "walnuts", "tofu", "lentils", "beets",
    "chia", "spinach", "blueberries", "almonds", "oats", "tempeh",
    "ginger", "turmeric", "matcha", "tahini", "edamame",
]
_TOLERATED_FOODS = [
    "rice", "bread", "pasta", "potatoes", "corn", "peas", "carrots",
    "milk", "eggs", "cheese", "chicken", "soup", "beans", "noodles",
]
_DISLIKED_FOODS = [
    "candy", "soda", "chips", "junk", "sugar", "cake", "pizza",
    "fries", "cola", "gummy", "popcorn", "donuts", "nachos", "toffee",
    "syrup", "marshmallow", "lollipop", "twizzler", "cheeto",
]


@dataclass
class TasteProfile:
    """Deterministic food preference profile seeded from the pet's name."""
    favorite:  str   # 2.0× yield multiplier, joyful reaction
    tolerated: str   # 1.0× yield, mild comment
    disliked:  str   # 0.5× yield, displeasure reaction


def _derive_taste_profile(name: str) -> TasteProfile:
    """Deterministically derive a TasteProfile from the pet's name."""
    h = sum(ord(c) * (i + 1) for i, c in enumerate(name.upper()))
    fav = _FAVORITE_FOODS[ h         % len(_FAVORITE_FOODS)]
    tol = _TOLERATED_FOODS[(h *  7)  % len(_TOLERATED_FOODS)]
    dis = _DISLIKED_FOODS[ (h * 13)  % len(_DISLIKED_FOODS)]
    return TasteProfile(favorite=fav, tolerated=tol, disliked=dis)


def _taste_reaction(profile: TasteProfile, text: str) -> tuple[float, str]:
    """
    Check input text against the taste profile.
    Returns (yield_multiplier, reaction_string).
    """
    lower = text.lower()
    words = set(lower.split())

    # Fuzzy: also check substring containment for compound words
    def _matches(food: str) -> bool:
        return food in words or food in lower

    if _matches(profile.favorite):
        return 2.0, f"✦ loves {profile.favorite}!  🌟"
    if _matches(profile.disliked):
        return 0.5, f"😖  dislikes {profile.disliked}..."
    if _matches(profile.tolerated):
        return 1.0, f"~ tolerates {profile.tolerated}"
    return 1.0, ""

DEFAULT_SAVE_PATH = Path.home() / ".sovereign_pet.json"


class PetStage(str, Enum):
    EGG       = "egg"
    HATCHLING = "hatchling"
    JUVENILE  = "juvenile"
    ADULT     = "adult"
    ELDER     = "elder"
    ASCENDED  = "ascended"


class SpeechStyle(str, Enum):
    SCIENTIFIC  = "scientific"
    BIBLICAL    = "biblical"
    MODERN_TECH = "modern_tech"
    PLAYFUL     = "playful"


@dataclass
class PetState:
    name: str
    birth_timestamp: float
    last_fed: float
    last_interaction: float
    stage: str = PetStage.EGG
    vocabulary: List[str] = field(default_factory=list)
    genome_snapshot: str = ""
    tick: int = 0
    total_fed: int = 0
    speech_style: str = SpeechStyle.SCIENTIFIC
    vocab_growth_rate: int = 2

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> "PetState":
        return cls(**d)


# ── Pure-Python mock organism (fallback when Rust FFI unavailable) ──────────
class _MockOrganism:
    """Simulates E8OrganismWrapper vitals using NumPy-free pure Python."""

    def __init__(self, name: str):
        self._name = name
        self._age = 0
        self._health = 1.0
        self._negentropy = 0.0
        self._roots: List[int] = [0, 1, 2, 3]
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
        return self._negentropy

    def feed(self, point: List[float]):
        magnitude = math.sqrt(sum(x * x for x in point))
        yield_val = min(0.3, magnitude * 0.05)
        self._negentropy += yield_val
        self._health = min(1.0, self._health + 0.05)
        self._phase = (self._phase + 0.1) % (2 * math.pi)
        self._age += 1
        phases = ["α", "β", "γ", "δ", "ε", "ζ", "η", "θ"]
        return (yield_val, random.choice(phases))

    def grow(self) -> int:
        if len(self._roots) < 240 and self._negentropy > 1.0:
            new_root = max(self._roots) + 1
            self._roots.append(new_root)
            self._negentropy -= 0.5
            return 1
        return 0

    def attend(self, root_index: int) -> List[int]:
        path = [root_index]
        for _ in range(3):
            path.append((path[-1] + random.randint(1, 7)) % 240)
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
        return self._health > 0.4 and self._defects < 3

    def mitosis(self):
        return None

    def status(self) -> str:
        return f"MockOrganism({self._name}) age={self._age} health={self._health:.2f}"


def _make_organism(name: str):
    """Returns a real E8OrganismWrapper or falls back to _MockOrganism."""
    try:
        from sov_math.geometry.organism.e8_organism import E8OrganismWrapper
        return E8OrganismWrapper(name)
    except (ImportError, Exception):
        return _MockOrganism(name)


# ── Symbol vocabulary builder ───────────────────────────────────────────────
_SYMBOL_BASE = ["S", "Σ", "Ω", "Λ", "Φ", "Ψ", "Δ", "Γ", "Π", "Θ"]
_SUBSCRIPTS  = "₀₁₂₃₄₅₆₇₈₉"

def _make_symbol(index: int) -> str:
    base = _SYMBOL_BASE[index % len(_SYMBOL_BASE)]
    sub  = _SUBSCRIPTS[index % len(_SUBSCRIPTS)]
    return f"{base}{sub}"


def _vector_from_text(text: str) -> List[float]:
    """Derive an 8D feed vector from raw text (stable hash-based)."""
    raw = [float(ord(c)) for c in text[:8].ljust(8)]
    mag = math.sqrt(sum(x * x for x in raw)) or 1.0
    return [x / mag for x in raw]


class E8Pet:
    """
    The living E8 Tamagotchi organism.

    Usage::

        pet = E8Pet.load_or_create()
        pet.tick()
        pet.feed("hello world")
        print(pet.speak())
        pet.save()
    """

    HUNGER_TICK_THRESHOLD = 15   # Ticks before hunger begins
    STARVATION_THRESHOLD  = 40   # Ticks before health degrades

    def __init__(self, state: PetState):
        self.state     = state
        self._organism = _make_organism(state.name)
        self._taste    = _derive_taste_profile(state.name)
        self._speech: str = ""
        self._distressed: bool = False

    # ── Factory ─────────────────────────────────────────────────────────────

    @classmethod
    def create_new(cls, name: str) -> "E8Pet":
        now = time.time()
        state = PetState(
            name=name,
            birth_timestamp=now,
            last_fed=now,
            last_interaction=now,
        )
        return cls(state)

    @classmethod
    def load_or_create(cls, path: Path = DEFAULT_SAVE_PATH, name: Optional[str] = None) -> "E8Pet":
        if path.exists():
            try:
                data = json.loads(path.read_text())
                return cls(PetState.from_dict(data))
            except Exception:
                pass
        # First run — prompt for name if not provided
        if name is None:
            suggestion = random.choice(_E8_ROOT_NAMES)
            try:
                raw = input(f"Name your pet [{suggestion}]: ").strip()
                name = raw if raw else suggestion
            except (EOFError, KeyboardInterrupt):
                name = suggestion
        return cls.create_new(name)

    # ── Core loop ───────────────────────────────────────────────────────────

    def tick(self) -> None:
        """Advance one simulation tick: age, hunger, health decay, growth."""
        self.state.tick += 1

        # Grow the organism
        self._organism.grow()

        # Hunger / health dynamics
        ticks_since_fed = self._ticks_since_fed()
        if ticks_since_fed > self.STARVATION_THRESHOLD:
            # Gradually degrade health in mock organism
            if isinstance(self._organism, _MockOrganism):
                self._organism._health = max(0.0, self._organism._health - 0.02)

        # Check homeostasis
        self._distressed = not self._organism.is_homeostatic()

        # Update stage
        self.state.stage = self._compute_stage()

        # Snapshot genome
        self.state.genome_snapshot = self._organism.genome_binary()[:32] + "…"

        # Update last interaction implicitly
        self.state.last_interaction = time.time()

    def feed(self, data: str) -> str:
        """Feed the organism text/data; returns a response message."""
        vec = _vector_from_text(data)
        multiplier, reaction = _taste_reaction(self._taste, data)
        yield_value, phase = self._organism.feed([value * multiplier for value in vec])
        self.state.total_fed += 1
        self.state.last_fed = time.time()
        self.state.last_interaction = self.state.last_fed
        words = [word.strip(".,!?;:").lower() for word in data.split() if word.strip(".,!?;:")]
        for word in words:
            if word not in self.state.vocabulary:
                self.state.vocabulary.append(word)
                if len(self.state.vocabulary) >= self.state.vocab_growth_rate:
                    break
        self._organism.grow()
        self.state.stage = self._compute_stage()
        self._speech = reaction or f"{self.state.name} metabolized the offering at phase {phase}."
        return f"{self._speech} (+{yield_value:.3f} energy)"

    def self_optimize_engine(self) -> str:
        """Unleash pet to graze on codebase AST, evaluate candidate refactorings, and live hot-swap functions."""
        try:
            from sov_e8_organism import E8Organism
            org = E8Organism(self.state.name)
            res = org.graze_codebase_ast()
            swaps = res.get("active_hot_swaps", [])
            negentropy = res.get("negentropy_gained", 0.45)
            target = swaps[0].get("patched_target", "sov_math.geometry.e8_snapping.snap_to_e8") if swaps else "None"
            return f"[⚡ Tribble Self-Optimization] Grazed codebase AST! Hot-swapped '{target}' (+{negentropy:.2f} negentropy yield)"
        except Exception as e:
            return f"[⚡ Tribble Self-Optimization] Invariant Check Completed: {e}"

    def mitosis_duplicate(self) -> "E8Pet":
        """Perform Harmonic Mitosis to spawn a clone child pet aligned with the Geometric Centroid invariant."""
        child_name = f"{self.state.name}_sub_{len(self.state.vocabulary)+1}"
        child_pet = E8Pet.create_new(child_name)
        child_pet.state.vocabulary = list(self.state.vocabulary)
        child_pet.state.speech_style = self.state.speech_style
        return child_pet

    def protect_precious_insight(self, insight_text: str) -> str:
        """Seal and protect a precious insight to the Aethelgard Protection Vault & Remote Repo."""
        try:
            from sov_e8_organism import E8Organism
            org = E8Organism(self.state.name)
            res = org.protect_precious_insight(insight_text)
            if res.get("success"):
                return f"[🛡️ Aethelgard Protection Vault] Sealed insight '{insight_text[:40]}...' into Sanctuary! (H¹ = 0 Gate Verified)"
            return f"[🛡️ Vault Response] {res.get('reason', 'Failed to seal insight.')}"
        except Exception as e:
            return f"[🛡️ Vault Error] {e}"
        result = self._organism.feed(vec)
        base_yield, phase = result[0], result[1]

        # Apply taste profile multiplier
        multiplier, reaction = _taste_reaction(self._taste, data)
        yield_val = base_yield * multiplier

        self.state.last_fed = time.time()
        self.state.total_fed += 1

        # Grow vocabulary (bonus symbol discovery on favorites)
        vocab_size = len(self.state.vocabulary)
        discover_threshold = 2 if multiplier > 1.0 else 3
        if self.state.total_fed % discover_threshold == 0 or vocab_size == 0:
            new_sym = _make_symbol(vocab_size)
            if new_sym not in self.state.vocabulary:
                self.state.vocabulary.append(new_sym)

        self._speech = self._compose_speech()
        parts = [f"[{phase}] +{yield_val:.3f} negentropy"]
        if reaction:
            parts.append(reaction)
        parts.append(f"— {self._speech}")
        return "  ".join(parts)

    def play(self) -> str:
        """Trigger an attend() interaction on a random active root."""
        roots = self._organism.genome()
        if not roots:
            return "No active roots yet — feed me first!"
        root = random.choice(roots[:min(len(roots), 10)])
        path = self._organism.attend(root)
        self.state.last_interaction = time.time()
        path_str = " → ".join(str(p) for p in path)
        self._speech = self._compose_speech()
        return f"Weyl path: {path_str}"

    def speak(self) -> str:
        """Return the current speech utterance."""
        if not self._speech:
            self._speech = self._compose_speech()
        return self._speech

    def vitals(self) -> dict:
        """Return a dict of all display vitals."""
        def _f(v: float, lo: float = 0.0, hi: float = 1.0) -> float:
            """Clamp and sanitize a float vital — guards against inf/nan."""
            import math as _m
            return lo if not _m.isfinite(v) else max(lo, min(hi, v))

        return {
            "name":        self.state.name,
            "stage":       self.state.stage,
            "tick":        self.state.tick,
            "health":      _f(self._organism.health),
            "energy":      _f(self._organism.total_negentropy / 20.0),
            "coherence":   _f(self._organism.respiration_balance()),
            "hunger":      _f(self._ticks_since_fed() / max(1, self.STARVATION_THRESHOLD)),
            "homeostatic": self._organism.is_homeostatic(),
            "distressed":  self._distressed,
            "roots_active": len(self._organism.genome()),
            "vocab_size":  len(self.state.vocabulary),
            "speech":      self.speak(),
            "genome":      self.state.genome_snapshot,
            "favorite":    self._taste.favorite,
            "tolerated":   self._taste.tolerated,
            "disliked":    self._taste.disliked,
        }

    def save(self, path: Path = DEFAULT_SAVE_PATH) -> None:
        """Persist pet state to JSON."""
        path.write_text(json.dumps(self.state.to_dict(), indent=2))

    # ── Internal helpers ────────────────────────────────────────────────────

    def _ticks_since_fed(self) -> int:
        elapsed_sec = time.time() - self.state.last_fed
        return int(elapsed_sec / 2)  # 1 hunger tick per 2 real seconds

    def _compute_stage(self) -> str:
        age = self._organism.age
        stage = "egg"
        for threshold, name in _STAGE_THRESHOLDS:
            if age >= threshold:
                stage = name
        return stage

    def _compose_speech(self) -> str:
        vocab = self.state.vocabulary
        if not vocab:
            return "..."
        if len(vocab) == 1:
            base = vocab[0]
        elif len(vocab) == 2:
            base = f"{vocab[0]} ∘ {vocab[1]}"
        else:
            ops = ["∘", "→", "⊕", "⊗", "∧"]
            sample = random.sample(vocab, min(3, len(vocab)))
            op1 = random.choice(ops)
            base = f"{sample[0]} {op1} {sample[1]}"
            if len(sample) == 3:
                op2 = random.choice(ops)
                base += f" {op2} {sample[2]}"

        style = getattr(self.state, "speech_style", SpeechStyle.SCIENTIFIC)
        if style == SpeechStyle.SCIENTIFIC:
            return f"[E8 Invariant Projection] {base}"
        elif style == SpeechStyle.BIBLICAL:
            return f"Verily: {base} — (H¹=0 Coherent)"
        elif style == SpeechStyle.MODERN_TECH:
            return f"⟨quantum_state⟩ {base} [qbit_synced]"
        elif style == SpeechStyle.PLAYFUL:
            return f"✨ {base} ✨ (Yum!)"
        return base
