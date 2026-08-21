"""Freeze a JSON fixture pack into a minimal SHA-256 manifest."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a SHA-256 fixture manifest for a local JSON fixture pack.")
    parser.add_argument("--fixture", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    content = args.fixture.read_bytes()
    json.loads(content)
    result = {"schema": "sov.fixture_manifest", "schema_version": "0.1.0", "fixture_pack": args.fixture.name, "sha256": hashlib.sha256(content).hexdigest(), "bytes": len(content)}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(args.output)


if __name__ == "__main__":
    main()
