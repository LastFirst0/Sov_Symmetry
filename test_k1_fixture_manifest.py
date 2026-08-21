import json
import os
from pathlib import Path
import pytest
from sov_evidence_geometry_core import verify_fixture_manifest
from sov_evidence_geometry_core.errors import CoreContractError
ROOT = Path(__file__).resolve().parents[2]
PROJECT_DOCS = Path(os.environ.get("SOV_PROJECT_DOCS", ROOT.parent / "projects" / "sov-e4e91854"))
MANIFEST = PROJECT_DOCS / "K1_FIXTURE_MANIFEST_CANDIDATE.json"
def test_k1_manifest_verifies_published_fixture_pack():
    result = verify_fixture_manifest(MANIFEST, ROOT)
    assert result["fixture_count"] == 17 and result["categories"]["valid_object"] == 8
def test_k1_manifest_fails_closed_when_digest_is_mutated(tmp_path):
    manifest = json.loads(MANIFEST.read_text()); manifest["entries"][0]["sha256"] = "0" * 64
    path = tmp_path / "manifest.json"; path.write_text(json.dumps(manifest))
    with pytest.raises(CoreContractError) as error: verify_fixture_manifest(path, ROOT)
    assert error.value.code == "E_AUDIT_TAMPER"
