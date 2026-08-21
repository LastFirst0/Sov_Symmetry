"""
tests/test_colony.py
======================
Unit tests for the E8 Colony swarm.
All tests use pure-Python mock organisms — no Rust FFI required.
"""

from __future__ import annotations

import json
import sys
import types

# Stub Rust FFI
for mod_name in ("sov_e8_organism", "polyglot_functor",
                  "sov_math.geometry.organism.e8_organism"):
    if mod_name not in sys.modules:
        stub = types.ModuleType(mod_name)
        sys.modules[mod_name] = stub

import math
import pytest

from sov_heart.colony.organism_node import (
    OrganismNode, NodeState, Sector, OrganismPacket,
    _ColonyMockOrganism, _classify_sector, Caste, InstructionPacket
)
from sov_heart.colony.migration import MigrationRouter
from sov_heart.colony.topology import ColonyTopology
from sov_heart.colony.colony import Colony, _text_to_vec, _emit_vec


# ── Helpers ───────────────────────────────────────────────────────────────────

def _node(slot: int = 0) -> OrganismNode:
    return OrganismNode(root_slot=slot, name=f"test-{slot}", seed=slot)


def _seeded_colony(n: int = 6) -> Colony:
    c = Colony()
    c.seed(n)
    return c


# ── Sector enum ───────────────────────────────────────────────────────────────

class TestSector:
    def test_from_beast_string_lion(self):
        assert Sector.from_beast_string("lion") == Sector.LION

    def test_from_beast_string_case_insensitive(self):
        assert Sector.from_beast_string("Eagle") == Sector.EAGLE

    def test_from_beast_string_unknown_defaults_man(self):
        assert Sector.from_beast_string("unknown") == Sector.MAN

    def test_glyph_present(self):
        for s in Sector:
            assert len(s.glyph) > 0

    def test_letter_is_first_char(self):
        assert Sector.LION.letter == "L"
        assert Sector.OX.letter == "O"
        assert Sector.EAGLE.letter == "E"
        assert Sector.MAN.letter == "M"


# ── Mock organism ─────────────────────────────────────────────────────────────

class TestColonyMockOrganism:
    def test_initial_health_1(self):
        org = _ColonyMockOrganism("test", seed=42)
        assert org.health == 1.0

    def test_feed_increases_negentropy(self):
        org = _ColonyMockOrganism("test", seed=0)
        before = org.total_negentropy
        org.feed([0.5] * 8)
        assert org.total_negentropy > before

    def test_genome_binary_length(self):
        org = _ColonyMockOrganism("test", seed=0)
        assert len(org.genome_binary()) == 240

    def test_attend_returns_path(self):
        org = _ColonyMockOrganism("test", seed=0)
        path = org.attend(0)
        assert len(path) >= 2

    def test_mitosis_requires_negentropy(self):
        org = _ColonyMockOrganism("test", seed=0)
        # Without enough negentropy, mitosis should return None
        assert org.mitosis() is None

    def test_mitosis_succeeds_with_enough_neg(self):
        org = _ColonyMockOrganism("test", seed=0)
        org._neg = 4.0
        child = org.mitosis()
        assert child is not None
        # Parent loses some negentropy
        assert org._neg < 4.0

    def test_respiration_balance_finite(self):
        org = _ColonyMockOrganism("test", seed=0)
        bal = org.respiration_balance()
        assert math.isfinite(bal)
        assert 0.0 <= bal <= 1.0


# ── OrganismNode ──────────────────────────────────────────────────────────────

class TestOrganismNode:
    def test_creates_with_slot(self):
        node = _node(slot=5)
        assert node.root_slot == 5
        assert node.state == NodeState.ALIVE

    def test_node_id_is_string(self):
        node = _node()
        assert isinstance(node.node_id, str)
        assert len(node.node_id) > 0

    def test_sector_is_valid(self):
        node = _node()
        assert node.sector in list(Sector)

    def test_tick_returns_event(self):
        node = _node()
        event = node.tick()
        assert isinstance(event, dict)
        assert "event" in event

    def test_feed_returns_float(self):
        node = _node()
        y = node.feed([0.5] * 8)
        assert isinstance(y, float)
        assert y >= 0.0

    def test_dormant_node_returns_dormant_event(self):
        node = _node()
        node.state = NodeState.DORMANT
        node._dormant_since = 0
        event = node.tick()
        assert event["event"] == "dormant"

    def test_weyl_path_is_list(self):
        node = _node()
        path = node.weyl_path()
        assert isinstance(path, list)
        assert len(path) > 0

    def test_vitals_keys(self):
        node = _node()
        v = node.vitals()
        for key in ["node_id", "slot", "sector", "state", "health",
                    "negentropy", "age", "roots", "homeostatic", "defects"]:
            assert key in v, f"Missing vital: {key}"

    def test_vitals_health_finite(self):
        node = _node()
        v = node.vitals()
        assert math.isfinite(v["health"])
        assert 0.0 <= v["health"] <= 1.0

    def test_should_migrate_returns_bool(self):
        node = _node()
        assert isinstance(node.should_migrate(), bool)

# ── Castes ────────────────────────────────────────────────────────────────────

class TestCastes:
    def test_caste_enum(self):
        assert Caste.QUEEN.value == "Queen"
        assert Caste.DRONE.value == "Drone"
        
    def test_decoy_yields_zero_negentropy(self):
        node = OrganismNode(root_slot=10, caste=Caste.DECOY)
        yield_val = node.feed([1.0]*8)
        assert yield_val == 0.0
        
    def test_decoy_no_decay(self):
        node = OrganismNode(root_slot=10, caste=Caste.DECOY)
        node._organism._health = 1.0
        node._organism._neg = 0.0  # Below threshold
        node.tick()
        assert node._organism.health == 1.0  # No decay
        
    def test_mimic_reports_as_queen(self):
        node = OrganismNode(root_slot=10, caste=Caste.MIMIC)
        node._organism._neg = 1.0
        vitals = node.vitals()
        assert vitals["caste"] == Caste.QUEEN.value
        assert vitals["negentropy"] >= 9.99

class TestInstructionPacket:
    def test_packet_creation(self):
        pkt = InstructionPacket(tactic="TEST", origin_id="xyz")
        assert pkt.tactic == "TEST"
        assert pkt.origin_id == "xyz"


# ── OrganismPacket serialization ──────────────────────────────────────────────

class TestOrganismPacket:
    def test_to_packet_roundtrip(self):
        node   = _node(slot=7)
        packet = node.to_packet()
        assert packet.node_id     == node.node_id
        assert packet.origin_slot == 7
        assert len(packet.genome_binary) == 240

    def test_packet_json_roundtrip(self):
        packet = OrganismPacket(
            node_id="n1", origin_slot=0, genome_binary="1"*240,
            negentropy=1.5, health=0.9, age=10,
            active_roots=[1, 2, 3],
            sector="Lion",
            caste="Queen",
            vocabulary=["hello"],
        )
        j = packet.to_json()
        restored = OrganismPacket.from_json(j)
        assert restored.node_id == "n1"
        assert restored.sector == "Lion"
        assert restored.caste == "Queen"

    def test_from_packet_preserves_identity(self):
        packet = OrganismPacket(
            node_id="n1", origin_slot=0, genome_binary="1"*240,
            negentropy=1.5, health=0.9, age=10,
            active_roots=[], sector="Ox", caste="Drone", vocabulary=[],
        )
        rebuilt = OrganismNode.from_packet(packet, target_slot=20)
        assert rebuilt.node_id   == "n1"    # Identity preserved
        assert rebuilt.root_slot == 20              # Slot updated
        assert rebuilt.sector    == Sector.OX

    def test_from_packet_restores_negentropy(self):
        node = _node(slot=5)
        # Give it some negentropy
        for _ in range(10):
            node.feed([0.5] * 8)
        packet  = node.to_packet()
        rebuilt = OrganismNode.from_packet(packet, target_slot=99)
        assert abs(rebuilt._organism.total_negentropy - node._organism.total_negentropy) < 1e-6


# ── ColonyTopology ────────────────────────────────────────────────────────────

class TestColonyTopology:
    def test_place_and_retrieve(self):
        topo = ColonyTopology()
        node = _node(slot=10)
        topo.place(node)
        assert topo.node_at(10) is node

    def test_remove_node(self):
        topo = ColonyTopology()
        node = _node(slot=15)
        topo.place(node)
        removed = topo.remove(15)
        assert removed is node
        assert topo.node_at(15) is None

    def test_alive_nodes_excludes_dormant(self):
        topo  = ColonyTopology()
        alive = _node(slot=1)
        dorm  = _node(slot=2)
        dorm.state = NodeState.DORMANT
        topo.place(alive)
        topo.place(dorm)
        assert alive in topo.alive_nodes()
        assert dorm  not in topo.alive_nodes()

    def test_find_empty_slot(self):
        topo = ColonyTopology()
        topo.place(_node(slot=0))
        slot = topo.find_empty_slot(near=0)
        assert slot is not None
        assert slot != 0

    def test_sector_counts_sums_alive(self):
        topo = ColonyTopology()
        for i in range(8):
            topo.place(_node(slot=i * 5))
        sc = topo.sector_counts()
        total = sum(sc.values())
        assert total == len(topo.alive_nodes())

    def test_collective_health_in_range(self):
        topo = ColonyTopology()
        for i in range(4):
            topo.place(_node(slot=i))
        h = topo.collective_health()
        assert 0.0 <= h <= 1.0

    def test_balance_score_perfect_with_one_per_sector(self):
        topo = ColonyTopology()
        for i, s in enumerate(Sector):
            n = _node(slot=i * 10)
            n.sector = s
            topo.place(n)
        bal = topo.balance_score()
        assert 0.0 <= bal <= 1.0

    def test_ascii_map_length(self):
        topo = ColonyTopology()
        topo.place(_node(slot=0))
        m = topo.ascii_map(width=40)
        # Should have ceil(240 / 40) = 6 rows
        rows = m.split("\n")
        assert len(rows) == 6

    def test_summary_keys(self):
        topo = ColonyTopology()
        for i in range(4):
            topo.place(_node(slot=i))
        s = topo.summary()
        for key in ["total_alive", "total_dormant", "sector_counts", "health", "balance"]:
            assert key in s


# ── MigrationRouter ───────────────────────────────────────────────────────────

class TestMigrationRouter:
    def test_plan_route_returns_int_or_none(self):
        topo   = ColonyTopology()
        node   = _node(slot=5)
        topo.place(node)
        router = MigrationRouter(topo)
        result = router.plan_route(node)
        assert result is None or isinstance(result, int)

    def test_execute_migration_moves_node(self):
        topo   = ColonyTopology()
        node   = _node(slot=5)
        topo.place(node)
        router   = MigrationRouter(topo)
        slot_map = topo.slot_map()
        new_node, event = router.execute_migration(node, target_slot=99, slot_map=slot_map)
        assert new_node.root_slot == 99
        assert node.state == NodeState.DORMANT
        assert event["event"] == "migration"

    def test_migration_preserves_node_id(self):
        topo   = ColonyTopology()
        node   = _node(slot=10)
        topo.place(node)
        router   = MigrationRouter(topo)
        slot_map = topo.slot_map()
        new_node, _ = router.execute_migration(node, target_slot=50, slot_map=slot_map)
        assert new_node.node_id == node.node_id

    def test_recent_migrations_logged(self):
        topo   = ColonyTopology()
        node   = _node(slot=3)
        topo.place(node)
        router   = MigrationRouter(topo)
        slot_map = topo.slot_map()
        router.execute_migration(node, target_slot=77, slot_map=slot_map)
        recent = router.recent_migrations(n=1)
        assert len(recent) == 1
        assert recent[0]["target_slot"] == 77


# ── Colony ────────────────────────────────────────────────────────────────────

class TestColony:
    def test_seed_creates_organisms(self):
        c = Colony()
        nodes = c.seed(6)
        assert len(nodes) == 6
        assert len(c.topology.alive_nodes()) == 6

    def test_seed_distributes_slots(self):
        c     = Colony()
        nodes = c.seed(8)
        slots = [n.root_slot for n in nodes]
        # All slots should be unique
        assert len(set(slots)) == len(slots)

    def test_tick_returns_list(self):
        c = _seeded_colony(4)
        events = c.tick()
        assert isinstance(events, list)

    def test_feed_stream_returns_dict(self):
        c = _seeded_colony(8)
        result = c.feed_stream("sovereign geometric intelligence")
        assert isinstance(result, dict)
        # Should have keys for all 4 sectors
        for sector in ["Lion", "Ox", "Eagle", "Man"]:
            assert sector in result

    def test_feed_stream_yields_positive_negentropy(self):
        c = _seeded_colony(8)
        result = c.feed_stream("data flows through the lattice")
        assert any(v > 0.0 for v in result.values())

    def test_tick_advances_count(self):
        c = _seeded_colony(4)
        assert c._tick_count == 0
        c.tick()
        assert c._tick_count == 1

    def test_report_keys(self):
        c = _seeded_colony(6)
        c.tick()
        r = c.report()
        for key in ["tick", "organisms", "dormant", "sectors", "health",
                    "negentropy", "balance", "lattice_map"]:
            assert key in r

    def test_report_organisms_matches_alive(self):
        c = _seeded_colony(6)
        r = c.report()
        assert r["organisms"] == len(c.topology.alive_nodes())

    def test_multiple_ticks_stable(self):
        c = _seeded_colony(8)
        c.feed_stream("test data")
        for _ in range(20):
            c.tick()
        # Colony should still have some living organisms
        assert len(c.topology.alive_nodes()) > 0

    def test_node_reports_list(self):
        c = _seeded_colony(4)
        reports = c.node_reports()
        assert len(reports) == 4
        for r in reports:
            assert "slot" in r
            assert "health" in r

    def test_max_population_respected(self):
        c = Colony()
        # Seed max + a few more via direct placement
        c.seed(Colony.MAX_POPULATION)
        # Attempting more ticks shouldn't exceed MAX_POPULATION
        for _ in range(10):
            c.tick()
        assert len(c.topology.alive_nodes()) <= Colony.MAX_POPULATION


# ── Data helpers ──────────────────────────────────────────────────────────────

class TestDataHelpers:
    def test_text_to_vec_length(self):
        vec = _text_to_vec("hello")
        assert len(vec) == 8

    def test_text_to_vec_unit_norm(self):
        vec = _text_to_vec("sovereign engine")
        norm = math.sqrt(sum(x * x for x in vec))
        assert abs(norm - 1.0) < 1e-6

    def test_emit_vec_finite(self):
        vec = _emit_vec(0.5, slot=10)
        assert all(math.isfinite(x) for x in vec)
        assert len(vec) == 8

    def test_emit_vec_unit_norm(self):
        vec = _emit_vec(1.0, slot=5)
        norm = math.sqrt(sum(x * x for x in vec))
        assert abs(norm - 1.0) < 1e-6
