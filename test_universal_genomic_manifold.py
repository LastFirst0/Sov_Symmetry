"""
tests/test_universal_genomic_manifold.py
========================================
Unit tests for UniversalGenomicManifold and cross-species longevity mappings.
"""

import pytest
from sov_core.genomics.universal_genomic_manifold import (
    UniversalGenomicManifold,
    SpeciesGenomicProfile,
    LongevityArchetype
)


def test_manifold_initialization():
    manifold = UniversalGenomicManifold()
    assert len(manifold.species_registry) >= 8
    assert "Homo sapiens" in manifold.species_registry
    assert "Turritopsis dohrnii" in manifold.species_registry
    assert "Heterocephalus glaber" in manifold.species_registry
    assert "Balaena mysticetus" in manifold.species_registry


def test_species_e8_and_crt_snapping():
    manifold = UniversalGenomicManifold()
    turrit = manifold.species_registry["Turritopsis dohrnii"]
    
    assert turrit.e8_root_index is not None
    assert isinstance(turrit.e8_root_index, int)
    assert 0 <= turrit.e8_root_index < 240
    assert turrit.e8_root_vector is not None
    assert len(turrit.e8_root_vector) == 8
    assert turrit.monster_crt_coordinates is not None
    assert len(turrit.monster_crt_coordinates) == 3


def test_custom_species_registration():
    manifold = UniversalGenomicManifold()
    custom_species = SpeciesGenomicProfile(
        taxon_id=999999,
        scientific_name="Tardigrada syntheticus",
        common_name="Synthetic Water Bear",
        ncbi_assembly="GCA_999999999.1",
        max_lifespan_years=100.0,
        senescence_type="EXTENDED",
        cancer_resistance_index=1.0,
        regeneration_capacity_index=0.9,
        dna_repair_amplification_score=0.99,
        key_adaptations=["Dsup radiation protection protein"],
        ortholog_genes={"DSUP": "ATGGCCAAGAAACCGGCC"}
    )
    
    manifold.register_species(custom_species)
    assert "Tardigrada syntheticus" in manifold.species_registry
    
    registered = manifold.species_registry["Tardigrada syntheticus"]
    assert registered.evolutionary_adaptation_index is not None
    assert registered.evolutionary_adaptation_index > 0.90


def test_manifold_report_generation():
    manifold = UniversalGenomicManifold()
    report = manifold.generate_manifold_report()
    
    assert report["total_registered_species"] >= 8
    assert "species_profiles" in report
    assert len(report["top_translational_recommendations"]) == 5
    
    # Verify distance to human baseline is computed
    human_profile = [p for p in report["species_profiles"] if p["scientific_name"] == "Homo sapiens"][0]
    assert human_profile["distance_to_human_manifold"] == 0.0
