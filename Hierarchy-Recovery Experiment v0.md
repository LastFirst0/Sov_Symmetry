# Hierarchy-Recovery Experiment v0

## Status

**Result:** `no_supported_hierarchy_advantage_on_this_sample`

This bounded experiment uses a selected spanning hierarchy from Open English WordNet `oewn:2025` rooted at `oewn-00015568-n`. It compares a text-only Euclidean cosine baseline with a declared text-only Poincare-ball candidate. Hypernym edges are evaluation labels only; they are not used to construct the text vectors.

| Measure | Euclidean baseline | Hyperbolic candidate |
|---|---:|---:|
| Held-out direct-hypernym edges | 11 | 11 |
| Top-1 parent recovery | 0.091 | 0.000 |
| Top-3 parent recovery | 0.364 | 0.182 |
| Mean reciprocal rank | 0.273 | 0.194 |
| Mean rank | 10.727 | 10.727 |

The candidate configuration was selected only on the deterministic training-edge split: Poincare scale `0.45` and radial penalty `0.0`. On held-out edges, the bootstrap 95% interval for candidate minus baseline Top-1 recovery is `[-0.273, 0.000]`.

## Interpretation

The result is a test of the stated candidate on this sample only. `no_supported_hierarchy_advantage_on_this_sample` means the present run did **not** meet the declared evidence threshold for a general language-geometry claim unless explicitly stated otherwise. The random Top-1 reference for this candidate set is `0.021`.

## Limits

- This is a small, English-only lexical sample rather than a broad language benchmark.
- The candidate radial coordinate is an exploratory text-derived heuristic, not a learned or theory-proven geometry.
- The experiment does not test E8, Hopf fibrations, language cognition, or a universal geometry of language.
- WordNet hypernymy is a lexical relation, not a complete model of meaning.
- The comparison is not a statistical publication-grade study; bootstrap intervals summarize only this finite held-out edge sample.

## Reproduction

Run `python3 tools/run_hierarchy_recovery_experiment.py --output-dir artifacts/hierarchy_recovery_v0` from the repository root. The artifact hashes are in `manifest.json`.

## Source

Open English WordNet, `oewn:2025`, source `https://github.com/globalwordnet/english-wordnet`, license `CC-BY 4.0`. The project describes itself as a lexical network with hypernymy relations and provides programmatic access through the `wn` library.
