"""Validate a local external-adapter candidate against the published eight gates.

The validator never imports a callback from a claim packet. Reference execution is
opt-in and intended only for locally authored candidate packages.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path


REQUIRED_MANIFEST = {"adapter_id", "version", "predicate_id", "object_schema", "claimed_domain", "maintainer", "license", "source_refs", "assumptions", "dimensions", "tolerance_policy", "framework_neutral", "entrypoint", "fixture_pack", "fixture_manifest", "review_records", "release", "non_claims"}
REQUIRED_CLASSES = {"positive", "negative", "malformed", "boundary", "mutation", "neutrality"}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def evaluate(package: Path, entrypoint: str, packet: dict) -> dict:
    result = subprocess.run([sys.executable, str(package / entrypoint)], input=json.dumps(packet), text=True, capture_output=True, check=True, cwd=package)
    return json.loads(result.stdout)


def check(package: Path, execute_reference: bool) -> dict:
    manifest_path = package / "adapter_manifest.json"
    manifest = load(manifest_path)
    gates: list[dict] = []
    def gate(number: int, name: str, passed: bool, evidence: dict | str) -> None:
        gates.append({"gate": number, "name": name, "decision": "pass" if passed else "block", "evidence": evidence})

    missing = sorted(REQUIRED_MANIFEST - set(manifest))
    gate(0, "intent", not missing and bool(manifest.get("non_claims")) and bool(manifest.get("claimed_domain")), {"missing": missing})
    semantic_fields = ("object_schema", "assumptions", "dimensions", "tolerance_policy", "predicate_id")
    gate(1, "semantics", all(manifest.get(field) for field in semantic_fields), {"fields": semantic_fields})
    fixtures_path = package / manifest.get("fixture_pack", "fixtures.json")
    fixtures = load(fixtures_path) if fixtures_path.exists() else {"cases": []}
    classes = {case.get("class") for case in fixtures.get("cases", [])}
    fixture_manifest_path = package / manifest.get("fixture_manifest", "fixture_manifest.json")
    fixture_manifest = load(fixture_manifest_path) if fixture_manifest_path.exists() else {}
    frozen = fixture_manifest.get("sha256") == sha256(fixtures_path) if fixtures_path.exists() else False
    gate(2, "evidence", REQUIRED_CLASSES <= classes and frozen, {"classes": sorted(classes), "fixture_sha256": fixture_manifest.get("sha256"), "frozen": frozen})
    reference_results = []
    reference_pass = False
    if execute_reference and (package / manifest.get("entrypoint", "")).exists():
        try:
            for case in fixtures.get("cases", []):
                if case.get("class") != "neutrality":
                    result = evaluate(package, manifest["entrypoint"], {"check": manifest["predicate_id"], "framework_id": "framework:neutral", "input": case.get("input")})
                    reference_results.append({"id": case.get("id"), "status": result.get("status"), "expected": case.get("expected")})
            reference_pass = all(item["status"] == item["expected"] for item in reference_results)
        except (subprocess.CalledProcessError, json.JSONDecodeError):
            reference_pass = False
    gate(3, "reference", reference_pass, {"executed": execute_reference, "results": reference_results})
    neutrality = next((case for case in fixtures.get("cases", []) if case.get("class") == "neutrality"), {})
    neutrality_results = []
    if execute_reference and manifest.get("framework_neutral") is True:
        try:
            for framework_id in neutrality.get("framework_ids", []):
                result = evaluate(package, manifest["entrypoint"], {"check": manifest["predicate_id"], "framework_id": framework_id, "input": neutrality.get("input")})
                neutrality_results.append({"framework_id": framework_id, "status": result.get("status"), "receipt_id": result.get("receipt_id")})
        except (subprocess.CalledProcessError, json.JSONDecodeError):
            neutrality_results = []
    unique_results = {(item["status"], item["receipt_id"]) for item in neutrality_results}
    gate(4, "neutrality", len(neutrality_results) >= 3 and len(unique_results) == 1, {"results": neutrality_results})
    assurance_pass = reference_pass and all("receipt_id" in evaluate(package, manifest["entrypoint"], {"input": case.get("input")}) for case in fixtures.get("cases", []) if case.get("class") != "neutrality") if execute_reference else False
    gate(5, "assurance", assurance_pass, {"local_only": True, "recorded_layers": ["receipt_id"] if assurance_pass else []})
    reviews = manifest.get("review_records", [])
    review_scopes = {review.get("scope") for review in reviews if review.get("decision") == "approved"}
    gate(6, "review", {"semantics", "implementation"} <= review_scopes, {"approved_scopes": sorted(review_scopes)})
    release = manifest.get("release", {})
    gate(7, "release", bool(release.get("version_identifier")) and bool(release.get("rollback_point")) and bool(release.get("public_scope_statement")), release)
    decision = "candidate" if all(gate_result["decision"] == "pass" for gate_result in gates) else "quarantine"
    report = {"schema": "sov.external_adapter_admission_report", "schema_version": "0.1.0", "adapter_id": manifest.get("adapter_id"), "version": manifest.get("version"), "decision": decision, "gates": gates, "scope": "Local candidate validation only; this report does not admit runtime dispatch."}
    (package / "admission_report.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate a local third-party adapter candidate against the eight admission gates.")
    parser.add_argument("package", type=Path)
    parser.add_argument("--execute-reference", action="store_true", help="execute a locally authored candidate evaluator; never use for untrusted packages")
    args = parser.parse_args()
    print(json.dumps(check(args.package.resolve(), args.execute_reference), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
