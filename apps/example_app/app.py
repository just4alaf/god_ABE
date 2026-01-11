#!/usr/bin/env python3
"""
Minimal Example App

- Verifies GOD provenance via ABE
- Produces a trivial confirmation output
"""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
VERIFY = ROOT / "abe" / "verify_provenance.py"

def main(prov_path: Path):
    if not VERIFY.exists():
        print("ERROR: verifier missing", file=sys.stderr)
        sys.exit(1)

    # Run verifier (read-only, fail-closed)
    result = subprocess.run(
        [sys.executable, str(VERIFY), str(prov_path)],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print(result.stderr.strip(), file=sys.stderr)
        sys.exit(1)

    out = Path(__file__).parent / "output.txt"
    out.write_text("OK: GOD provenance verified. Example app completed.\n", encoding="utf-8")
    print("SUCCESS: example app output written")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("USAGE: app.py <path/to/provenance.json>", file=sys.stderr)
        sys.exit(1)
    main(Path(sys.argv[1]).resolve())
