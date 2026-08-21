import subprocess
import sys
from pathlib import Path

from sov_evidence_geometry_core.empirical import parse_empirical_claim_packet


ROOT = Path(__file__).resolve().parents[2]
CLI = ROOT / "tools" / "sov_kernel.py"


def test_cli_writes_a_parseable_draft_empirical_template(tmp_path):
    output = tmp_path / "packet.json"
    subprocess.run([sys.executable, str(CLI), "empirical-template", "--output", str(output)], cwd=ROOT, check=True, capture_output=True, text=True)
    import json
    packet = parse_empirical_claim_packet(json.loads(output.read_text(encoding="utf-8")))
    assert packet["state"] == "draft"
    assert packet["governance"]["template"] is True
