#!/usr/bin/env python3
"""
ABE Provenance Verifier (NON-EXECUTING)

- Validates provenance.json against schemas/provenance.schema.json
- Recomputes SHA-256 hashes for referenced artifacts
- Fails closed on any error
"""

import json
import sys
import hashlib
from pathlib import Path

try:
    from jsonschema import validate
except ImportError:
    print("ERROR: jsonschema not installed", file=sys.stderr)
    sys.exit(1)

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schemas" / "provenance.schema.json"

def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

def main(prov_path: Path):
    if not SCHEMA.exists():
        print("ERROR: provenance schema missing", file=sys.stderr)
        sys.exit(1)

    data = json.loads(prov_path.read_text(encoding="utf-8"))
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    validate(instance=data, schema=schema)

    checks = [
        ("execution_output.json", data["output_integrity"]["execution_output_hash"]),
        ("report.json", data["output_integrity"]["report_json_hash"]),
    ]

    md_hash = data["output_integrity"].get("report_md_hash")
    if md_hash:
        checks.append(("report.md", md_hash))

    for fname, expected in checks:
        p = ROOT / fname
        if not p.exists():
            print(f"ERROR: missing artifact {fname}", file=sys.stderr)
            sys.exit(1)
        actual = sha256(p)
        if actual != expected:
            print(f"ERROR: hash mismatch for {fname}", file=sys.stderr)
            sys.exit(1)

    print("OK: provenance verified")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("USAGE: verify_provenance.py <path/to/provenance.json>", file=sys.stderr)
        sys.exit(1)
    main(Path(sys.argv[1]).resolve())
