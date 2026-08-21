#!/usr/bin/env python3
"""Run the non-clinical M0 public DNA sequence geometry benchmark.

The candidate is deliberately modest: a Poincaré-distance class-prototype
classifier over a fixed random projection of 5-mer TF-IDF features. Its matched
Euclidean control uses the exact same projected inputs and class prototypes.
This is an experiment, not a biological model or a clinical tool.
"""
from __future__ import annotations

import argparse
import json
import platform
import shutil
from pathlib import Path

import numpy as np
import sklearn
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import average_precision_score, roc_auc_score
from sklearn.random_projection import GaussianRandomProjection

from validate_molecular_intake import load, validate

SEEDS = (17, 43, 97)
KMER_SIZE = 5
PROJECTION_DIMENSIONS = 16
BALL_RADIUS = 0.90


def _metric(y: np.ndarray, score: np.ndarray) -> dict[str, float]:
    return {"auroc": float(roc_auc_score(y, score)), "average_precision": float(average_precision_score(y, score))}


def _project_to_ball(matrix: np.ndarray) -> np.ndarray:
    norms = np.linalg.norm(matrix, axis=1, keepdims=True)
    limit = max(float(norms.max()), 1e-12)
    return matrix / limit * BALL_RADIUS


def poincare_distance(points: np.ndarray, prototype: np.ndarray) -> np.ndarray:
    numerator = 2.0 * np.sum((points - prototype) ** 2, axis=1)
    denominator = np.clip((1.0 - np.sum(points**2, axis=1)) * (1.0 - np.sum(prototype**2)), 1e-12, None)
    return np.arccosh(np.maximum(1.0 + numerator / denominator, 1.0 + 1e-12))


def class_scores(train_matrix: np.ndarray, train_labels: np.ndarray, evaluation_matrix: np.ndarray, shuffled_seed: int) -> dict[str, np.ndarray]:
    rng = np.random.default_rng(shuffled_seed)
    positive = train_matrix[train_labels == 1].mean(axis=0)
    negative = train_matrix[train_labels == 0].mean(axis=0)
    euclidean = np.linalg.norm(evaluation_matrix - negative, axis=1) - np.linalg.norm(evaluation_matrix - positive, axis=1)
    ball_train, ball_eval = _project_to_ball(train_matrix), _project_to_ball(evaluation_matrix)
    hyper_positive = ball_train[train_labels == 1].mean(axis=0)
    hyper_negative = ball_train[train_labels == 0].mean(axis=0)
    hyperbolic = poincare_distance(ball_eval, hyper_negative) - poincare_distance(ball_eval, hyper_positive)
    shuffled_labels = rng.permutation(train_labels)
    shuffled_positive = train_matrix[shuffled_labels == 1].mean(axis=0)
    shuffled_negative = train_matrix[shuffled_labels == 0].mean(axis=0)
    random_control = np.linalg.norm(evaluation_matrix - shuffled_negative, axis=1) - np.linalg.norm(evaluation_matrix - shuffled_positive, axis=1)
    return {"hyperbolic_poincare_prototype": hyperbolic, "matched_euclidean_prototype": euclidean, "shuffled_label_control": random_control}


def paired_bootstrap(y: np.ndarray, candidate: np.ndarray, control: np.ndarray, seed: int, rounds: int) -> dict[str, dict[str, float]]:
    rng = np.random.default_rng(seed)
    differences = {"auroc": [], "average_precision": []}
    for _ in range(rounds):
        index = rng.integers(0, len(y), len(y))
        candidate_metrics, control_metrics = _metric(y[index], candidate[index]), _metric(y[index], control[index])
        for name in differences:
            differences[name].append(candidate_metrics[name] - control_metrics[name])
    return {name: {"mean_difference": float(np.mean(values)), "ci95_low": float(np.quantile(values, 0.025)), "ci95_high": float(np.quantile(values, 0.975))} for name, values in differences.items()}


def records(path: Path) -> tuple[list[str], np.ndarray]:
    values = load(path)
    return [entry["sequence"] for entry in values], np.array([entry["label"] for entry in values], dtype=np.int8)


def run(input_dir: Path, output: Path, bootstrap_rounds: int = 200) -> dict:
    manifest = load(input_dir / "dataset_manifest.json")
    source_records = {name: load(input_dir / f"{name}.json") for name in ("train", "validation", "test")}
    intake = validate(manifest, source_records)
    train_sequences, train_y = records(input_dir / "train.json")
    validation_sequences, validation_y = records(input_dir / "validation.json")
    test_sequences, test_y = records(input_dir / "test.json")
    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True)
    protocol = {
        "schema": "sov.molecular_experiment_protocol",
        "schema_version": "0.1.0",
        "protocol_id": "m0.genomic_benchmarks.human_nontata_promoters.v0",
        "hypothesis_id": "H-DNA-01",
        "dataset_id": manifest["dataset_id"],
        "primary_metric": "auroc",
        "candidates": [{"id": "hyperbolic_poincare_prototype", "family": "hyperbolic", "parameter_budget": 32}],
        "controls": [{"id": "matched_euclidean_prototype", "family": "matched_euclidean", "parameter_budget": 32}, {"id": "shuffled_label_control", "family": "random", "parameter_budget": 32}],
        "selection_policy": "No post-hoc selection. K-mer size, dimensions, radius, and seeds are constants in this script. Validation metrics are recorded but do not select a candidate.",
        "replication_policy": "Three fixed projection seeds; a future independent rerun must rebuild inputs from the source manifest in a separate environment.",
        "non_claims": ["This is not a gene-function, disease, longevity, therapeutic, tissue, or personal-genomic inference.", "A classification score does not establish biological mechanism or validate hyperbolic geometry as a property of DNA."],
    }
    (output / "protocol.json").write_text(json.dumps(protocol, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    runs = []
    test_predictions = {}
    for seed in SEEDS:
        vectorizer = TfidfVectorizer(analyzer="char", ngram_range=(KMER_SIZE, KMER_SIZE), lowercase=False, norm="l2", dtype=np.float64)
        train_features = vectorizer.fit_transform(train_sequences)
        projection = GaussianRandomProjection(n_components=PROJECTION_DIMENSIONS, random_state=seed)
        train_matrix = projection.fit_transform(train_features)
        validation_matrix = projection.transform(vectorizer.transform(validation_sequences))
        test_matrix = projection.transform(vectorizer.transform(test_sequences))
        validation_scores = class_scores(train_matrix, train_y, validation_matrix, seed)
        test_scores = class_scores(train_matrix, train_y, test_matrix, seed)
        run_metrics = {"seed": seed, "validation": {name: _metric(validation_y, score) for name, score in validation_scores.items()}, "test": {name: _metric(test_y, score) for name, score in test_scores.items()}, "paired_bootstrap_hyperbolic_minus_euclidean": paired_bootstrap(test_y, test_scores["hyperbolic_poincare_prototype"], test_scores["matched_euclidean_prototype"], seed, bootstrap_rounds)}
        runs.append(run_metrics)
        test_predictions[str(seed)] = {name: [round(float(value), 12) for value in score] for name, score in test_scores.items()}
    aggregate = {}
    for split in ("validation", "test"):
        aggregate[split] = {}
        for model in ("hyperbolic_poincare_prototype", "matched_euclidean_prototype", "shuffled_label_control"):
            aggregate[split][model] = {metric: float(np.mean([run[split][model][metric] for run in runs])) for metric in ("auroc", "average_precision")}
    ci_lows = [run["paired_bootstrap_hyperbolic_minus_euclidean"]["auroc"]["ci95_low"] for run in runs]
    verdict = "fail" if max(ci_lows) <= 0 else "inconclusive"
    report = {"schema": "sov.molecular_evaluation_bundle", "schema_version": "0.1.0", "status": "verified", "verdict": verdict, "verdict_reason": "The declared hyperbolic candidate did not show a positive 95% paired-bootstrap AUROC lower bound over its matched Euclidean control on any fixed seed." if verdict == "fail" else "At least one seed has a positive lower bound, but no independent rerun has occurred.", "intake": intake, "dataset_manifest_sha256": __import__("hashlib").sha256((input_dir / "dataset_manifest.json").read_bytes()).hexdigest(), "environment": {"python": platform.python_version(), "numpy": np.__version__, "scikit_learn": sklearn.__version__}, "constants": {"kmer_size": KMER_SIZE, "projection_dimensions": PROJECTION_DIMENSIONS, "ball_radius": BALL_RADIUS, "seeds": list(SEEDS), "bootstrap_rounds": bootstrap_rounds}, "runs": runs, "aggregate": aggregate, "limitations": protocol["non_claims"] + ["The Poincare class prototype uses an approximate Euclidean mean in ball coordinates.", "This first run uses one public promoter benchmark and is not an independent replication." ]}
    (output / "evaluation_bundle.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (output / "test_predictions.json").write_text(json.dumps({"labels": test_y.tolist(), "scores": test_predictions}, separators=(",", ":"), sort_keys=True) + "\n", encoding="utf-8")
    return report


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--bootstrap-rounds", type=int, default=200)
    args = parser.parse_args()
    print(json.dumps(run(args.input, args.output, args.bootstrap_rounds), sort_keys=True))


if __name__ == "__main__":
    main()
