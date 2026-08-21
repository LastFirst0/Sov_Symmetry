"""Fail closed on missing canonical docs, archive leakage, or invalid claim governance."""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

from validate_governance_register import validate

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
EXCLUDED = {DOCS / "research-archive", DOCS / "archive"}
MANAGED = {DOCS / name for name in ("start-here", "concepts", "how-to", "reference", "assurance", "adapters", "empirical-evidence", "governance", "research-archive", "release-evidence")}


def main() -> None:
    manifest = ROOT / "artifacts" / "documentation_manifest.json"
    if not manifest.exists():
        raise SystemExit("E_DOCS_MANIFEST_MISSING")
    records = json.loads(manifest.read_text(encoding="utf-8"))
    if records.get("schema") != "sov.documentation_manifest":
        raise SystemExit("E_DOCS_MANIFEST_SCHEMA")
    for entry in records.get("entries", []):
        if not str(entry.get("id", "")).startswith("docs:"):
            continue
        source = ROOT / entry["path"]
        digest = hashlib.sha256(source.read_bytes()).hexdigest() if source.exists() else None
        if digest != entry.get("sha256"):
            raise SystemExit(f"E_DOCS_MANIFEST_TAMPER:{entry.get('id')}")
    for path in DOCS.rglob("*.md"):
        if not any(folder in path.parents for folder in MANAGED):
            continue
        if any(parent in path.parents for parent in EXCLUDED):
            continue
        text = path.read_text(encoding="utf-8")
        if re.search(r"Geometric\s+Unity", text, re.IGNORECASE):
            raise SystemExit(f"E_DOCS_ARCHIVE_LEAK:{path.relative_to(ROOT)}")
        for target in re.findall(r"\[[^\]]+\]\(([^)#]+)(?:#[^)]+)?\)", text):
            if "://" in target or target.startswith("/"):
                continue
            if not (path.parent / target).resolve().exists():
                raise SystemExit(f"E_DOCS_BROKEN_LINK:{path.relative_to(ROOT)}:{target}")
    validate()
    print("DOCS_AND_GOVERNANCE=PASS")


if __name__ == "__main__":
    main()
