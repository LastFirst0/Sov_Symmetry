#!/usr/bin/env python3
"""Canonicalize the verified public M0 promoter archive into frozen split records."""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import shutil
from pathlib import Path

from validate_molecular_intake import digest, validate

SEED = "m0-human-nontata-validation-v0.1"


def read_class(directory: Path, label: int, split: str) -> list[dict]:
    records = []
    for path in sorted(directory.glob("*.txt")):
        sequence = path.read_text(encoding="utf-8").strip().upper()
        records.append({"id": f"{split}:{label}:{path.stem}", "sequence": sequence, "label": label})
    if not records:
        raise ValueError(f"no records in {directory}")
    return records


def choose_validation(records: list[dict], fraction: float = 0.10) -> tuple[list[dict], list[dict]]:
    by_label = {0: [], 1: []}
    for record in records:
        by_label[record["label"]].append(record)
    train, validation = [], []
    for label, group in by_label.items():
        ranked = sorted(group, key=lambda r: hashlib.sha256(f"{SEED}:{r['id']}".encode("utf-8")).hexdigest())
        count = max(1, math.floor(len(ranked) * fraction))
        validation.extend(ranked[:count])
        train.extend(ranked[count:])
    return sorted(train, key=lambda r: r["id"]), sorted(validation, key=lambda r: r["id"])


def prepare(source: Path, output: Path) -> dict:
    source_manifest = json.loads((source / "source_manifest.json").read_text(encoding="utf-8"))
    if source_manifest.get("manifest_id") != "dataset.genomic_benchmarks.human_nontata_promoters.v0":
        raise ValueError("unexpected source manifest")
    raw = source / "raw" / "human_nontata_promoters"
    all_train = read_class(raw / "train" / "negative", 0, "upstream-train") + read_class(raw / "train" / "positive", 1, "upstream-train")
    upstream_test = read_class(raw / "test" / "negative", 0, "upstream-test") + read_class(raw / "test" / "positive", 1, "upstream-test")
    train, validation = choose_validation(all_train)
    test = sorted(upstream_test, key=lambda r: r["id"])
    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True)
    records = {"train": train, "validation": validation, "test": test}
    for name, values in records.items():
        (output / f"{name}.json").write_text(json.dumps(values, sort_keys=True, separators=(",", ":")) + "\n", encoding="utf-8")
    manifest = {
        "schema": "sov.molecular_sequence_dataset",
        "schema_version": "0.1.0",
        "dataset_id": "m0.genomic_benchmarks.human_nontata_promoters.v0",
        "source_manifest_id": source_manifest["manifest_id"],
        "task": {"task_type": "binary_sequence_classification", "label_semantics": "Public benchmark labels: non-TATA promoter negative or positive class; no biological mechanism is inferred."},
        "sequence_alphabet": ["A", "C", "G", "T", "N"],
        "splits": [{"name": name, "records_sha256": digest(values), "record_count": len(values)} for name, values in records.items()],
        "split_derivation": {"upstream_train": "train", "upstream_test": "test", "validation": "10 percent label-stratified deterministic partition of upstream train", "seed": SEED},
        "limitations": ["Public non-clinical benchmark only.", "Validation is derived from upstream train and is not an upstream-provided split.", "Exact and reverse-complement cross-split checks are required before evaluation."],
    }
    (output / "dataset_manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    report = validate(manifest, records)
    (output / "intake_validation_report.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return report


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(prepare(args.source, args.output), sort_keys=True))


if __name__ == "__main__":
    main()
