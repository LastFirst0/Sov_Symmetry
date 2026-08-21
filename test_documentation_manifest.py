import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "tools" / "build_docs_manifest.py"
MANIFEST = ROOT / "artifacts" / "documentation_manifest.json"


def test_documentation_manifest_is_generated_with_canonical_and_archival_entries():
    subprocess.run([sys.executable, str(SCRIPT)], cwd=ROOT, check=True, capture_output=True, text=True)
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    entries = {entry["id"]: entry for entry in manifest["entries"]}
    assert manifest["schema"] == "sov.documentation_manifest"
    assert entries["docs:start-here"]["source_of_truth"] is True
    assert entries["docs:research-archive"]["status"] == "archival"
    archive_entries = [entry for entry in manifest["entries"] if entry["classification"] == "archival_research"]
    assert archive_entries
    assert all(entry["replacement"] == "docs/research-archive/README.md" for entry in archive_entries)
