#!/usr/bin/env python3
"""
scripts/analysis/run_universal_genomic_manifold.py
=================================================
SOVEREIGN ENGINE: UNIVERSAL COMPARATIVE GENOMICS & LONGEVITY RUNNER

Executes high-throughput cross-species longevity mining across extremophile and
negligibly senescent organisms, mapping each to E8/CRT/Poincaré manifold spaces.

Outputs:
  artifacts/universal_genomic_manifold_report.json
"""

import sys
import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from sov_core.genomics.universal_genomic_manifold import UniversalGenomicManifold

OUTPUT_REPORT = PROJECT_ROOT / "artifacts" / "universal_genomic_manifold_report.json"


def main():
    print("================================================================================")
    print("SOVEREIGN ENGINE: UNIVERSAL COMPARATIVE GENOMIC & LONGEVITY MANIFOLD")
    print("================================================================================")

    manifold = UniversalGenomicManifold()
    report = manifold.generate_manifold_report()

    print(f"\n[*] Total Species Registered: {report['total_registered_species']}")
    print("\n[+] Cross-Species Evolutionary Longevity Ranking (by Adaptation Index EAI):")
    print("-" * 88)
    print(f"{'Species':<25} | {'Lifespan':<10} | {'EAI':<6} | {'E8 Root':<8} | {'Dist to Human':<14} | {'Archetype'}")
    print("-" * 88)

    for sp in report["species_profiles"]:
        lifespan_str = f"{sp['max_lifespan_years']:.0f} yrs" if sp['max_lifespan_years'] < 1000 else "IMMORTAL"
        dist_str = f"{sp['distance_to_human_manifold']:.4f}" if sp['distance_to_human_manifold'] is not None else "BASELINE"
        print(f"{sp['common_name']:<25} | {lifespan_str:<10} | {sp['evolutionary_adaptation_index']:<6.3f} | #{sp['e8_root_index']:<7} | {dist_str:<14} | {sp['longevity_archetype'][:25]}")

    print("\n[+] Top 5 Evolutionary Solutions for Human Senescence Reversal:")
    for i, rec in enumerate(report["top_translational_recommendations"], 1):
        print(f"\n  {i}. [{rec['source_organism']}] - {rec['archetype']}")
        print(f"     • Target Mechanism:  {rec['target_mechanism']}")
        print(f"     • Human Translation: {rec['human_application']}")

    OUTPUT_REPORT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_REPORT, "w") as f:
        json.dump(report, f, indent=2)
    print(f"\n[✓] Manifold Report saved to: {OUTPUT_REPORT}")


if __name__ == "__main__":
    main()
