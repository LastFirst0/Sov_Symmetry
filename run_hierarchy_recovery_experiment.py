"""Run a bounded language-hierarchy recovery experiment on Open English WordNet.

This is an exploratory, reproducible benchmark—not a claim that language has a
universal geometry. The candidate uses only synset lemmas and definitions to
form document vectors; it does not use the WordNet hierarchy as an embedding
feature. The WordNet hypernym links serve only as evaluation labels.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
from collections import Counter, deque
from pathlib import Path
from typing import Any

import numpy as np
import wn


LEXICON_ID = "oewn:2025"
ROOT_ID = "oewn-00015568-n"
SOURCE_URL = "https://github.com/globalwordnet/english-wordnet"
SOURCE_LICENSE = "CC-BY 4.0"
TOKEN_RE = re.compile(r"[a-z]+")


def sha256_json(value: Any) -> str:
    text = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def get_lexicon() -> wn.Wordnet:
    try:
        return wn.Wordnet(LEXICON_ID)
    except wn.Error:
        wn.download(LEXICON_ID)
        return wn.Wordnet(LEXICON_ID)


def synset_text(synset: Any) -> str:
    lemmas = " ".join(word.lemma().replace("_", " ") for word in synset.words())
    return f"{lemmas} {synset.definition()}".strip()


def sample_spanning_hierarchy(lexicon: wn.Wordnet, max_nodes: int, max_children: int, max_depth: int) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    root = lexicon.synset(ROOT_ID)
    nodes: dict[str, dict[str, str]] = {
        root.id: {"id": root.id, "label": root.words()[0].lemma(), "text": synset_text(root), "depth": "0"}
    }
    edges: list[dict[str, str]] = []
    queue: deque[tuple[Any, int]] = deque([(root, 0)])
    while queue and len(nodes) < max_nodes:
        parent, depth = queue.popleft()
        if depth >= max_depth:
            continue
        children = sorted(parent.hyponyms(), key=lambda item: (-len(item.hyponyms()), item.id))
        selected = 0
        for child in children:
            if selected >= max_children or len(nodes) >= max_nodes:
                break
            if child.id in nodes:
                continue
            nodes[child.id] = {
                "id": child.id,
                "label": child.words()[0].lemma(),
                "text": synset_text(child),
                "depth": str(depth + 1),
            }
            edges.append({"parent": parent.id, "child": child.id})
            queue.append((child, depth + 1))
            selected += 1
    if len(nodes) < 12 or len(edges) < 11:
        raise RuntimeError("The public hierarchy sample is too small for the declared experiment.")
    return sorted(nodes.values(), key=lambda item: item["id"]), sorted(edges, key=lambda item: (item["child"], item["parent"]))


def tfidf_vectors(nodes: list[dict[str, str]], dimensions: int = 8) -> tuple[np.ndarray, list[str], np.ndarray]:
    token_docs = [TOKEN_RE.findall(node["text"].lower()) for node in nodes]
    document_frequency: Counter[str] = Counter()
    for tokens in token_docs:
        document_frequency.update(set(tokens))
    vocabulary = sorted(token for token, count in document_frequency.items() if count >= 2)
    if len(vocabulary) < 3:
        raise RuntimeError("Sample text vocabulary is too small for the declared text-only representation.")
    index = {token: position for position, token in enumerate(vocabulary)}
    matrix = np.zeros((len(nodes), len(vocabulary)), dtype=float)
    for row, tokens in enumerate(token_docs):
        counts = Counter(tokens)
        for token, count in counts.items():
            if token in index:
                idf = math.log((len(nodes) + 1) / (document_frequency[token] + 1)) + 1.0
                matrix[row, index[token]] = count * idf
    row_norm = np.linalg.norm(matrix, axis=1, keepdims=True)
    matrix = matrix / np.where(row_norm == 0.0, 1.0, row_norm)
    _, _, right = np.linalg.svd(matrix, full_matrices=False)
    rank = min(dimensions, right.shape[0])
    reduced = matrix @ right[:rank].T
    reduced_norm = np.linalg.norm(reduced, axis=1, keepdims=True)
    unit = reduced / np.where(reduced_norm == 0.0, 1.0, reduced_norm)
    mean_idf = np.zeros(len(nodes), dtype=float)
    for row, tokens in enumerate(token_docs):
        known = [math.log((len(nodes) + 1) / (document_frequency[token] + 1)) + 1.0 for token in tokens if token in index]
        mean_idf[row] = float(np.mean(known)) if known else 0.0
    return unit, vocabulary, mean_idf


def poincare_points(unit: np.ndarray, mean_idf: np.ndarray, scale: float) -> np.ndarray:
    low, high = float(np.min(mean_idf)), float(np.max(mean_idf))
    normalized_specificity = (mean_idf - low) / (high - low) if high > low else np.full_like(mean_idf, 0.5)
    radii = 0.12 + (0.78 * normalized_specificity)
    return unit * (scale * radii)[:, None]


def cosine_scores(vectors: np.ndarray, child: int) -> np.ndarray:
    return vectors @ vectors[child]


def poincare_scores(points: np.ndarray, child: int, radial_penalty: float) -> np.ndarray:
    child_point = points[child]
    differences = points - child_point
    squared_distance = np.sum(differences * differences, axis=1)
    denominator = (1.0 - np.sum(points * points, axis=1)) * (1.0 - np.sum(child_point * child_point))
    argument = 1.0 + (2.0 * squared_distance / np.maximum(denominator, 1e-12))
    distance = np.arccosh(np.maximum(argument, 1.0))
    radii = np.linalg.norm(points, axis=1)
    child_radius = radii[child]
    return -distance - radial_penalty * np.maximum(0.0, radii - child_radius)


def rank_metrics(nodes: list[dict[str, str]], edges: list[dict[str, str]], score_function: Any) -> dict[str, float]:
    index = {node["id"]: position for position, node in enumerate(nodes)}
    ranks: list[int] = []
    for edge in edges:
        child = index[edge["child"]]
        parent = index[edge["parent"]]
        scores = score_function(child)
        candidates = [candidate for candidate in range(len(nodes)) if candidate != child]
        ordered = sorted(candidates, key=lambda candidate: (-float(scores[candidate]), nodes[candidate]["id"]))
        ranks.append(ordered.index(parent) + 1)
    return {
        "edge_count": float(len(ranks)),
        "top1": float(sum(rank == 1 for rank in ranks) / len(ranks)),
        "top3": float(sum(rank <= 3 for rank in ranks) / len(ranks)),
        "mrr": float(sum(1.0 / rank for rank in ranks) / len(ranks)),
        "mean_rank": float(sum(ranks) / len(ranks)),
    }


def deterministic_split(edges: list[dict[str, str]]) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    training = [edge for edge in edges if int(hashlib.sha256(edge["child"].encode("utf-8")).hexdigest()[:8], 16) % 10 < 7]
    testing = [edge for edge in edges if edge not in training]
    if len(training) < 4 or len(testing) < 3:
        midpoint = max(4, len(edges) * 2 // 3)
        training, testing = edges[:midpoint], edges[midpoint:]
    return training, testing


def bootstrap_delta(nodes: list[dict[str, str]], test_edges: list[dict[str, str]], candidate: Any, baseline: Any, seed: int = 20260818, samples: int = 1000) -> dict[str, float]:
    rng = np.random.default_rng(seed)
    deltas: list[float] = []
    for _ in range(samples):
        chosen = [test_edges[index] for index in rng.integers(0, len(test_edges), len(test_edges))]
        candidate_score = rank_metrics(nodes, chosen, candidate)["top1"]
        baseline_score = rank_metrics(nodes, chosen, baseline)["top1"]
        deltas.append(candidate_score - baseline_score)
    return {
        "bootstrap_samples": float(samples),
        "top1_delta_p2_5": float(np.percentile(deltas, 2.5)),
        "top1_delta_p50": float(np.percentile(deltas, 50)),
        "top1_delta_p97_5": float(np.percentile(deltas, 97.5)),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", default="artifacts/hierarchy_recovery_v0", help="Directory for deterministic experiment artifacts.")
    parser.add_argument("--max-nodes", type=int, default=48)
    parser.add_argument("--max-children", type=int, default=4)
    parser.add_argument("--max-depth", type=int, default=3)
    args = parser.parse_args()
    output = Path(args.output_dir)
    output.mkdir(parents=True, exist_ok=True)

    lexicon = get_lexicon()
    nodes, edges = sample_spanning_hierarchy(lexicon, args.max_nodes, args.max_children, args.max_depth)
    vectors, vocabulary, mean_idf = tfidf_vectors(nodes)
    training, testing = deterministic_split(edges)

    baseline = lambda child: cosine_scores(vectors, child)
    candidate_choices: list[tuple[float, float, dict[str, float]]] = []
    for scale in (0.45, 0.65, 0.85):
        points = poincare_points(vectors, mean_idf, scale)
        for penalty in (0.0, 0.25, 0.5, 1.0):
            candidate = lambda child, p=points, r=penalty: poincare_scores(p, child, r)
            candidate_choices.append((scale, penalty, rank_metrics(nodes, training, candidate)))
    selected_scale, selected_penalty, selection_metrics = max(candidate_choices, key=lambda item: (item[2]["mrr"], item[2]["top1"], -item[0], -item[1]))
    selected_points = poincare_points(vectors, mean_idf, selected_scale)
    candidate = lambda child: poincare_scores(selected_points, child, selected_penalty)

    baseline_test = rank_metrics(nodes, testing, baseline)
    candidate_test = rank_metrics(nodes, testing, candidate)
    bootstrap = bootstrap_delta(nodes, testing, candidate, baseline)
    expected_random_top1 = 1.0 / (len(nodes) - 1)
    verdict = "no_supported_hierarchy_advantage_on_this_sample"
    if candidate_test["top1"] > baseline_test["top1"] and bootstrap["top1_delta_p2_5"] > 0.0:
        verdict = "candidate_advantage_observed_on_this_sample_only"

    sample = {
        "source": {"lexicon": LEXICON_ID, "root_synset": ROOT_ID, "source_url": SOURCE_URL, "license": SOURCE_LICENSE},
        "selection_policy": {"max_nodes": args.max_nodes, "max_children_per_node": args.max_children, "max_depth": args.max_depth, "spanning_tree_policy": "breadth-first; lexicographic synset-id child selection; repeated nodes omitted"},
        "nodes": nodes,
        "edges": edges,
    }
    design = {
        "hypothesis": "A text-only hyperbolic candidate improves direct hypernym recovery over a text-only Euclidean cosine baseline on the held-out sample edges.",
        "representation": "TF-IDF of synset lemmas plus definitions, reduced by SVD; hierarchy labels are evaluation-only.",
        "baseline": "Cosine similarity in the reduced text representation.",
        "candidate": "Poincare-ball distance using a text-derived radial coordinate from mean IDF and a declared radial-parent penalty.",
        "selection": {"training_edges": [edge["child"] for edge in training], "selected_scale": selected_scale, "selected_radial_penalty": selected_penalty, "selection_metrics": selection_metrics},
        "test": {"test_edges": [edge["child"] for edge in testing], "baseline_metrics": baseline_test, "candidate_metrics": candidate_test, "random_top1_expectation": expected_random_top1, "bootstrap_top1_delta": bootstrap},
        "verdict": verdict,
        "limitations": [
            "This is a small, English-only lexical sample rather than a broad language benchmark.",
            "The candidate radial coordinate is an exploratory text-derived heuristic, not a learned or theory-proven geometry.",
            "The experiment does not test E8, Hopf fibrations, language cognition, or a universal geometry of language.",
            "WordNet hypernymy is a lexical relation, not a complete model of meaning.",
            "The comparison is not a statistical publication-grade study; bootstrap intervals summarize only this finite held-out edge sample.",
        ],
        "execution": {"python": __import__("sys").version.split()[0], "numpy": np.__version__, "wn": wn.__version__},
    }
    manifest = {
        "schema": "sov.hierarchy_recovery_experiment_manifest",
        "schema_version": "0.1.0",
        "sample_sha256": sha256_json(sample),
        "design_sha256": sha256_json(design),
        "artifacts": ["sample.json", "result.json", "EXPERIMENT_REPORT.md"],
    }
    (output / "sample.json").write_text(json.dumps(sample, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (output / "result.json").write_text(json.dumps(design, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (output / "manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    report = f"""# Hierarchy-Recovery Experiment v0

## Status

**Result:** `{verdict}`

This bounded experiment uses a selected spanning hierarchy from Open English WordNet `{LEXICON_ID}` rooted at `{ROOT_ID}`. It compares a text-only Euclidean cosine baseline with a declared text-only Poincare-ball candidate. Hypernym edges are evaluation labels only; they are not used to construct the text vectors.

| Measure | Euclidean baseline | Hyperbolic candidate |
|---|---:|---:|
| Held-out direct-hypernym edges | {int(baseline_test['edge_count'])} | {int(candidate_test['edge_count'])} |
| Top-1 parent recovery | {baseline_test['top1']:.3f} | {candidate_test['top1']:.3f} |
| Top-3 parent recovery | {baseline_test['top3']:.3f} | {candidate_test['top3']:.3f} |
| Mean reciprocal rank | {baseline_test['mrr']:.3f} | {candidate_test['mrr']:.3f} |
| Mean rank | {baseline_test['mean_rank']:.3f} | {candidate_test['mean_rank']:.3f} |

The candidate configuration was selected only on the deterministic training-edge split: Poincare scale `{selected_scale}` and radial penalty `{selected_penalty}`. On held-out edges, the bootstrap 95% interval for candidate minus baseline Top-1 recovery is `[{bootstrap['top1_delta_p2_5']:.3f}, {bootstrap['top1_delta_p97_5']:.3f}]`.

## Interpretation

The result is a test of the stated candidate on this sample only. `{verdict}` means the present run did **not** meet the declared evidence threshold for a general language-geometry claim unless explicitly stated otherwise. The random Top-1 reference for this candidate set is `{expected_random_top1:.3f}`.

## Limits

{chr(10).join(f'- {item}' for item in design['limitations'])}

## Reproduction

Run `python3 tools/run_hierarchy_recovery_experiment.py --output-dir artifacts/hierarchy_recovery_v0` from the repository root. The artifact hashes are in `manifest.json`.

## Source

Open English WordNet, `{LEXICON_ID}`, source `{SOURCE_URL}`, license `{SOURCE_LICENSE}`. The project describes itself as a lexical network with hypernymy relations and provides programmatic access through the `wn` library.
"""
    (output / "EXPERIMENT_REPORT.md").write_text(report, encoding="utf-8")
    print(json.dumps({"output_dir": str(output), "verdict": verdict, "manifest_sha256": sha256_json(manifest)}, sort_keys=True))


if __name__ == "__main__":
    main()
