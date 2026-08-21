# Molecular Sequence Geometry Experiment Design v0.1

**Status:** Proposed next experiment; not yet run.  
**Decision:** **Yes—molecular sequences should become the next geometry research domain, but not through the present branch’s hash-derived “genomic manifold” or symbolic codon mappings.** The first target should be a public, non-clinical, labeled DNA sequence-classification task with documented splits.

## 1. Why molecular sequences are a better next domain

The lexical hierarchy pilot established that the research workflow can produce and retain a valid negative result. Molecular sequences offer a stronger next domain because the alphabet is finite, raw inputs can be pinned exactly, task labels can come from external benchmarks, and geometry has clear baseline literature. In contrast, natural-language “meaning” has many unresolved labeling and context problems.

This does **not** mean that DNA is “the true language” to which the kernel should be applied or that a geometric embedding uncovers a biological essence. Here, “language” means a finite ordered sequence over a biological alphabet. The next claim is strictly computational:

> **H-DNA-01.** On a named public DNA sequence-classification dataset, a declared hyperbolic representation improves held-out predictive performance over matched Euclidean and random controls under a frozen protocol.

The available literature makes this a reasonable question rather than an empty metaphor. Hyperbolic Genome Embeddings reports a hyperbolic CNN evaluation against Euclidean counterparts on genome-interpretation tasks, while GUE provides a multi-species DNA classification benchmark with declared tasks and datasets. [1] [2] Neither source validates the clean-release branch’s E8/CRT/hashing constructions.

| Property | WordNet hierarchy pilot | Proposed DNA sequence pilot | Why the DNA pilot is useful next |
|---|---|---|---|
| Public raw object | Lexical synset text | A/C/G/T sequence | Both are reproducibly pin-able. |
| External label | Direct hypernym edge | Regulatory/sequence-class label | The molecular task yields a conventional classification metric. |
| Primary risk | Overreading lexical meaning | Biological overclaim or leakage | Requires strict non-clinical scope and split checks. |
| Geometry question | Parent-ranking geometry | Representation geometry for classification | Comparable Euclidean/hyperbolic test can be stated cleanly. |
| First use | Workflow proof | Domain-validity proof | A negative result still upgrades the evidence record. |

## 2. Recommended first benchmark: DNA promoter or regulatory-element classification

The recommended first experiment is **one fixed binary DNA sequence-classification dataset from the published Genome Understanding Evaluation (GUE) corpus**, with the upstream dataset release, checksum, task name, license, and predefined train/validation/test splits captured in the experiment manifest. The exact task must be chosen only after a data-acquisition review confirms provenance and licensing; a promoter or enhancer-type task is a suitable initial class because it has clear binary labels and does not involve individual-level clinical data.

GUE is preferable to inventing a new sequence corpus because its parent work describes a standardized multi-species benchmark spanning 36 datasets and nine tasks. [2] A second, independent benchmark should be reserved for replication—not used to tune candidate geometry after looking at its test scores.

### Explicit exclusions

The v0 experiment excludes all personally identifiable, patient-derived, disease-risk, therapeutic-response, ancestry, embryo, tissue, single-cell, and clinical data. It excludes medical predictions and does not generate, recommend, or evaluate interventions. It also excludes the legacy branch’s manually assigned species “adaptation” scalars and any claimed human-longevity application.

## 3. Frozen data contract

```json
{
  "schema": "sov.molecular_sequence_dataset.v0.1",
  "dataset_id": "gue:<publisher-release>:<exact-task>",
  "organism": "<as declared by benchmark>",
  "sequence_alphabet": ["A", "C", "G", "T", "N"],
  "task_type": "binary_sequence_classification",
  "label_semantics": "<verbatim benchmark definition>",
  "source_url": "<publisher/repository URL>",
  "license": "<verified license>",
  "raw_manifest_sha256": "<digest>",
  "split_policy": "upstream frozen train/validation/test split",
  "leakage_audit": {
    "duplicates_removed_or_reported": true,
    "reverse_complement_policy": "declared",
    "near_duplicate_policy": "declared",
    "chromosome_or_homology_policy": "as supported by source"
  }
}
```

The data gate must reject an unknown alphabet, duplicated examples across splits, altered labels, missing license, missing checksum, or any attempt to substitute a manually curated species profile for a source dataset.

## 4. Representation candidates and matched controls

All representations receive exactly the same frozen sequences and splits. The initial pilot must avoid pretraining and trainable external foundation models, so a result is attributable to the declared transformation rather than undocumented model scale.

| ID | Representation | Purpose | Status if it wins |
|---|---|---|---|
| `B0.random` | Seeded random scores stratified by label prevalence. | Sanity floor. | Detects a broken task if conventional methods do not exceed it. |
| `B1.kmer_euclidean` | Normalized 6-mer frequency vector with logistic regression or linear SVM. | Strong inexpensive Euclidean baseline. | Establishes whether any candidate adds value over compositional sequence features. |
| `B2.kmer_euclidean_matched` | Same vector dimension/parameter count as candidate, with a non-hyperbolic nonlinear projection. | Capacity control. | Tests whether geometry, not extra flexibility, explains an improvement. |
| `C1.hyperbolic` | Same 6-mer features projected by a declared, trainable Poincaré/Lorentz classifier. | Main geometry candidate. | Supports only H-DNA-01 on this data/protocol. |
| `L1.legacy_e8_candidate` | A precise legacy transform over biological features, specified before evaluation. | Optional later ablation. | Must beat both B2 and C1 to support any added-value claim. |

The current branch’s `hash_codon_to_geometric_manifold` must **not** be `L1`: its SHA-256 modulo assignment is a deterministic symbolic lookup with no stated biological invariant or learnable relation to labels. The current `UniversalGenomicManifold` must also not provide features: it hashes manually assembled profile strings, so any apparent predictive score would be a function of hand-authored categories rather than a sequence-derived genomic representation. [3] [4]

## 5. Evaluation protocol and failure criteria

### Primary metric and decision rule

The primary metric is **test AUROC** for a binary task, with test average precision reported as secondary. If the selected benchmark is materially class-balanced and its standard reports accuracy, the predeclared benchmark metric may be primary instead, but it cannot be changed after validation results are inspected.

The `C1.hyperbolic` candidate supports a positive H-DNA-01 result only if all conditions hold:

1. It exceeds `B1.kmer_euclidean` and `B2.kmer_euclidean_matched` on the frozen test set.
2. A stratified bootstrap 95% confidence interval for the primary-metric difference against **each** Euclidean control has a lower bound strictly above zero.
3. The best C1 configuration was selected solely by validation data, not test data.
4. Three fixed-seed reruns reproduce the direction of the primary comparison without an unexplained evaluator or manifest discrepancy.
5. The result replicates once on a second independently pinned dataset or task, without changing the candidate family.

Failure to meet any condition returns `fail:E_NO_SUPPORTED_HYPERBOLIC_ADVANTAGE` or `unverifiable:E_REPLICATION_OR_PROVENANCE_MISSING`, not a soft passing label. A positive result still says nothing directly about molecular mechanism, gene function, disease, aging, protein folding, tissues, or intervention efficacy.

### Measurement bundle

Each evaluation bundle must include exact sample counts, class prevalence, train/validation/test hashes, model/source/image digest, hyperparameters, seed, CPU/GPU/environment record, metric code version, predictions digest, confusion threshold policy, and bootstrap code/version. The kernel checks package completeness and declared predicates; it does not replace biological peer review.

## 6. How the legacy code can participate responsibly

| Legacy component | Present condition | Required rehabilitation | Earliest valid role |
|---|---|---|---|
| `UniversalGenomicManifold` | Manually filled species attributes converted to hash vectors and fixed scores. | Replace with raw public sequence/annotation manifest, documented feature extractor, and label-blind preprocessing. | Dataset-provenance utility after rewrite. |
| Codon E8 mapper | Codon hash modulo E8/symbolic labels. | Define a sequence-derived transform with no arbitrary hash assignment; prove determinism and compare against permutation/shuffle controls. | Candidate feature ablation only. |
| ProteinFoldingNode | Amino acid bridge plus centroid/swarm heuristic. | Use a PDB/CATH/ProteinWorkshop task; define sequence encoding, predicted target, structural label, and external metric. | Separate protein experiment, not DNA pilot. |
| E8 root quantizer | Exact geometry utility, but domain meaning unestablished. | Accept a real feature vector, define its normalization, run sensitivity/permutation tests, and compare with equal-capacity projections. | `L1.legacy_e8_candidate` in a later controlled ablation. |

## 7. Implementation sequence

1. Review the chosen GUE dataset’s license, source format, labels, and upstream split; build a manifest before writing a model.
2. Implement a **pure data validator** for characters, lengths, splits, duplicates, reverse complements, and checksums.
3. Implement `B0`, `B1`, and `B2` before C1, including output schema and deterministic seed fixtures.
4. Implement `C1` using a maintained Riemannian optimization library only after a narrow dependency review; pin the package/version/container digest and independently reproduce all metric calculations.
5. Run selection and frozen evaluation with resource caps and no network access after data acquisition.
6. Run a UKG experiment gate that verifies the protocol, artifacts, baselines, test results, and non-claims.
7. Publish the full result, including a negative result, before considering any legacy E8 ablation.

## 8. Recommendation

**Proceed with the DNA sequence experiment as Experiment M0, but do not treat the existing “genetic analysis” branch as a molecular-analysis engine.** Keep M0 explicitly non-clinical, public-data-only, and sequence-label-focused. Use the branch as a source of candidate abstractions to rewrite and test—not as a valid data, feature, mechanism, or recommendation layer.

The broader project should use **three separate research tracks**, not a single blended “biology language” claim:

| Track | First valid question | Earliest evidence artifact |
|---|---|---|
| Lexical geometry | Can a candidate recover a declared lexical relation? | Existing WordNet negative-result receipt. |
| DNA geometry | Can a candidate beat matched controls on a public labeled sequence task? | M0 dataset/prediction/evaluation receipt. |
| Protein geometry | Can a candidate predict a stated structural/function target from public sequence/structure data? | Separate PDB/CATH task receipt. |

This separation keeps a result in one domain from being accidentally treated as a result in another.

## References

[1]: https://proceedings.iclr.cc/paper_files/paper/2025/hash/b63ad8c24354b0e5bcb7aea16490beab-Abstract-Conference.html "Hyperbolic Genome Embeddings, ICLR 2025"
[2]: https://proceedings.iclr.cc/paper_files/paper/2024/hash/b633e7052970b8f5aa1a69164d99e9e8-Abstract-Conference.html "DNABERT-2 and Genome Understanding Evaluation, ICLR 2024"
[3]: file:///home/ubuntu/Sovereign_Engine_v2_clean/sov_core/genomics/universal_genomic_manifold.py "UniversalGenomicManifold source"
[4]: file:///home/ubuntu/Sovereign_Engine_v2_clean/scripts/biological_e8_codon_mapper.py "Biological codon mapper source"
