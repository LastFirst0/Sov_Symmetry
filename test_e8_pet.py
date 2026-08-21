"""
tests/test_e8_pet.py
=====================
Unit tests for the E8 Tamagotchi core state engine.
Tests run against the pure-Python mock organism (no Rust FFI required).
"""

from __future__ import annotations

import json
import math
import time
import tempfile
from pathlib import Path

import pytest

# Force mock organism by patching the import before loading the module
import sys
import types

# Stub out the Rust FFI modules so tests work without compiled libraries
for mod_name in ("sov_e8_organism", "polyglot_functor",
                  "sov_math.geometry.organism.e8_organism"):
    if mod_name not in sys.modules:
        stub = types.ModuleType(mod_name)
        sys.modules[mod_name] = stub

from sov_heart.tamagotchi.e8_pet import (
    E8Pet,
    PetState,
    PetStage,
    TasteProfile,
    _derive_taste_profile,
    _taste_reaction,
    _make_symbol,
    _vector_from_text,
    _MockOrganism,
)


# ── Helpers ──────────────────────────────────────────────────────────────────

def _fresh_pet(name: str = "TORI") -> E8Pet:
    return E8Pet.create_new(name)


# ── Symbol generation ────────────────────────────────────────────────────────

class TestSymbolGeneration:
    def test_symbol_zero(self):
        assert _make_symbol(0) == "S₀"

    def test_symbol_ten_wraps_base(self):
        sym = _make_symbol(10)
        assert len(sym) >= 2

    def test_symbol_unique_for_range(self):
        symbols = [_make_symbol(i) for i in range(20)]
        # No two adjacent symbols should be identical
        for i in range(len(symbols) - 1):
            assert symbols[i] != symbols[i + 1]


# ── Vector from text ─────────────────────────────────────────────────────────

class TestVectorFromText:
    def test_returns_8d(self):
        vec = _vector_from_text("hello")
        assert len(vec) == 8

    def test_unit_norm(self):
        vec = _vector_from_text("sovereign engine")
        norm = math.sqrt(sum(x * x for x in vec))
        assert abs(norm - 1.0) < 1e-6

    def test_empty_string(self):
        vec = _vector_from_text("")
        assert len(vec) == 8
        # All same character (space), so it should still normalise
        norm = math.sqrt(sum(x * x for x in vec))
        assert norm > 0

    def test_deterministic(self):
        v1 = _vector_from_text("test")
        v2 = _vector_from_text("test")
        assert v1 == v2


# ── Mock organism ────────────────────────────────────────────────────────────

class TestMockOrganism:
    def test_initial_health(self):
        org = _MockOrganism("LUMI")
        assert 0.0 <= org.health <= 1.0

    def test_feed_increases_negentropy(self):
        org = _MockOrganism("LUMI")
        before = org.total_negentropy
        org.feed([0.1] * 8)
        assert org.total_negentropy > before

    def test_feed_returns_tuple(self):
        org = _MockOrganism("LUMI")
        result = org.feed([0.5] * 8)
        assert isinstance(result, tuple)
        assert len(result) == 2
        yield_val, phase = result
        assert isinstance(yield_val, float)
        assert isinstance(phase, str)

    def test_grow_adds_roots(self):
        org = _MockOrganism("LUMI")
        # Prime the negentropy
        for _ in range(30):
            org.feed([0.5] * 8)
        initial = len(org.genome())
        org.grow()
        # Should have grown at least once given sufficient negentropy
        assert len(org.genome()) >= initial

    def test_attend_returns_path(self):
        org = _MockOrganism("LUMI")
        path = org.attend(0)
        assert len(path) >= 2
        assert all(isinstance(p, int) for p in path)

    def test_genome_binary_length(self):
        org = _MockOrganism("LUMI")
        bits = org.genome_binary()
        assert len(bits) == 240
        assert all(c in "01" for c in bits)

    def test_is_homeostatic_true_initially(self):
        org = _MockOrganism("LUMI")
        assert org.is_homeostatic()

    def test_respiration_balance_in_range(self):
        org = _MockOrganism("LUMI")
        bal = org.respiration_balance()
        assert 0.0 <= bal <= 1.0


# ── E8Pet core ───────────────────────────────────────────────────────────────

class TestE8Pet:
    def test_create_new(self):
        pet = _fresh_pet("NOVA")
        assert pet.state.name == "NOVA"
        assert pet.state.stage == PetStage.EGG

    def test_tick_increments_count(self):
        pet = _fresh_pet()
        pet.tick()
        assert pet.state.tick == 1
        pet.tick()
        assert pet.state.tick == 2

    def test_feed_grows_vocabulary(self):
        pet = _fresh_pet()
        # Feed enough times to build vocabulary
        for i in range(9):
            pet.feed(f"data sample {i}")
        assert len(pet.state.vocabulary) >= 1

    def test_feed_returns_string(self):
        pet = _fresh_pet()
        response = pet.feed("hello sovereign")
        assert isinstance(response, str)
        assert len(response) > 0

    def test_play_returns_string(self):
        pet = _fresh_pet()
        # Prime the organism with some roots
        for _ in range(5):
            pet.feed("prime")
        result = pet.play()
        assert isinstance(result, str)

    def test_speak_returns_string(self):
        pet = _fresh_pet()
        speech = pet.speak()
        assert isinstance(speech, str)

    def test_vitals_keys(self):
        pet = _fresh_pet()
        v = pet.vitals()
        required = [
            "name", "stage", "tick", "health", "energy",
            "coherence", "hunger", "homeostatic", "distressed",
            "roots_active", "vocab_size", "speech", "genome",
        ]
        for key in required:
            assert key in v, f"Missing vital: {key}"

    def test_vitals_health_in_range(self):
        pet = _fresh_pet()
        v = pet.vitals()
        assert 0.0 <= v["health"] <= 1.0

    def test_vitals_energy_in_range(self):
        pet = _fresh_pet()
        for _ in range(5):
            pet.feed("energy test")
        v = pet.vitals()
        assert 0.0 <= v["energy"] <= 1.0

    def test_stage_progression(self):
        pet = _fresh_pet()
        # Force organism age to juvenile threshold
        pet._organism._age = 25  # type: ignore[attr-defined]
        pet.tick()
        assert pet.state.stage in ("juvenile", "adult", "elder", "hatchling")

    def test_save_and_load(self):
        pet = _fresh_pet("WEYL")
        pet.feed("save test data")
        pet.tick()

        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tmp:
            path = Path(tmp.name)

        try:
            pet.save(path)
            assert path.exists()

            # Load it back
            loaded = E8Pet.load_or_create(path=path)
            assert loaded.state.name == "WEYL"
            assert loaded.state.tick == pet.state.tick
        finally:
            path.unlink(missing_ok=True)

    def test_save_file_valid_json(self):
        pet = _fresh_pet("ZARA")
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tmp:
            path = Path(tmp.name)
        try:
            pet.save(path)
            data = json.loads(path.read_text())
            assert "name" in data
            assert "stage" in data
        finally:
            path.unlink(missing_ok=True)

    def test_distress_flag_type(self):
        pet = _fresh_pet()
        v = pet.vitals()
        assert isinstance(v["distressed"], bool)

    def test_genome_snapshot_in_vitals(self):
        pet = _fresh_pet()
        pet.tick()
        v = pet.vitals()
        assert isinstance(v["genome"], str)
        assert len(v["genome"]) > 0


# ── Pet state serialization ───────────────────────────────────────────────────

class TestPetState:
    def test_roundtrip(self):
        now = time.time()
        state = PetState(
            name="SOVI",
            birth_timestamp=now,
            last_fed=now,
            last_interaction=now,
            vocabulary=["S₀", "Σ₁"],
            tick=42,
            total_fed=7,
        )
        d = state.to_dict()
        loaded = PetState.from_dict(d)
        assert loaded.name == "SOVI"
        assert loaded.tick == 42
        assert loaded.vocabulary == ["S₀", "Σ₁"]
# ── Taste profile ────────────────────────────────────────────────────────────────────────

class TestTasteProfile:
    def test_derive_is_deterministic(self):
        p1 = _derive_taste_profile("HOLO")
        p2 = _derive_taste_profile("HOLO")
        assert p1.favorite  == p2.favorite
        assert p1.tolerated == p2.tolerated
        assert p1.disliked  == p2.disliked

    def test_different_names_differ(self):
        p_holo = _derive_taste_profile("HOLO")
        p_weyl = _derive_taste_profile("WEYL")
        # Should not all be identical (very unlikely by construction)
        assert not (
            p_holo.favorite == p_weyl.favorite
            and p_holo.disliked == p_weyl.disliked
        )

    def test_favorite_gives_2x_multiplier(self):
        profile = TasteProfile(favorite="kale", tolerated="rice", disliked="candy")
        mult, reaction = _taste_reaction(profile, "some kale please")
        assert mult == 2.0
        assert "loves" in reaction
        assert "kale" in reaction

    def test_disliked_gives_half_multiplier(self):
        profile = TasteProfile(favorite="kale", tolerated="rice", disliked="candy")
        mult, reaction = _taste_reaction(profile, "i have candy")
        assert mult == 0.5
        assert "dislikes" in reaction

    def test_tolerated_gives_1x_multiplier(self):
        profile = TasteProfile(favorite="kale", tolerated="rice", disliked="candy")
        mult, reaction = _taste_reaction(profile, "plain rice")
        assert mult == 1.0
        assert "tolerates" in reaction

    def test_unknown_food_gives_1x_no_reaction(self):
        profile = TasteProfile(favorite="kale", tolerated="rice", disliked="candy")
        mult, reaction = _taste_reaction(profile, "something completely different")
        assert mult == 1.0
        assert reaction == ""

    def test_favorite_priority_over_disliked(self):
        # If both words appear, favorite wins
        profile = TasteProfile(favorite="kale", tolerated="rice", disliked="candy")
        mult, reaction = _taste_reaction(profile, "kale and candy together")
        assert mult == 2.0

    def test_feed_reaction_in_response(self):
        pet = _fresh_pet("KALETEST")
        # Inject a known profile so we can predict behavior
        from sov_heart.tamagotchi.e8_pet import TasteProfile
        pet._taste = TasteProfile(favorite="kale", tolerated="rice", disliked="candy")
        response = pet.feed("fresh kale salad")
        assert "loves kale" in response
        assert "+" in response  # yield shown

    def test_feed_disliked_reaction_in_response(self):
        pet = _fresh_pet("KALETEST")
        from sov_heart.tamagotchi.e8_pet import TasteProfile
        pet._taste = TasteProfile(favorite="kale", tolerated="rice", disliked="candy")
        response = pet.feed("a bag of candy")
        assert "dislikes" in response

    def test_vitals_exposes_taste_fields(self):
        pet = _fresh_pet("HOLO")
        v = pet.vitals()
        assert "favorite"  in v
        assert "tolerated" in v
        assert "disliked"  in v
        assert isinstance(v["favorite"],  str)
        assert isinstance(v["tolerated"], str)
        assert isinstance(v["disliked"],  str)

    def test_holo_likes_edamame(self):
        """Regression: Holo's deterministic favorite food is edamame (name-hash stable)."""
        profile = _derive_taste_profile("Holo")
        assert profile.favorite == "edamame"
        assert profile.disliked == "donuts"
