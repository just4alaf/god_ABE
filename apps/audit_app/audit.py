#!/usr/bin/env python3
"""
Audit / Compliance App (READ-ONLY)

- Verifies GOD provenance using ABE verifier
- Performs deterministic checks
- Emits audit_report.json matching audit_schema.json
- No side effects beyond file creation
"""

import json
import sys
import subprocess
import uuid
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
VERIFY = ROOT / "abe" / "verify_provenance.py"
SCHEMA = Path(__file__).parent / "audit_schema.json"

def fail(msg: str):
    print(f"FAIL: {msg}", file=sys.stderr)
    sys.exit(1)

def run_verifier(prov_path: Path):
    if not VERIFY.exists():
        fail("ABE verifier missing")
    result = subprocess.run(
        [sys.executable, str(VERIFY), str(prov_path)],
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        fail(result.stderr.strip() or "Provenance verification failed")

def load_json(p: Path):
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception as e:
        fail(f"Invalid JSON at {p.name}: {e}")

def main(prov_path: Path):
    if not prov_path.exists():
        fail("provenance.json not found")

    # 1) Verify provenance (schema + hashes)
    run_verifier(prov_path)

    # 2) Load provenance and perform deterministic checks
    prov = load_json(prov_path)

    checks = []

    # Check determinism declaration (schema enforces consts; reassert here)
    det = prov.get("determinism_declaration", {})
    if det.get("deterministic") is True and det.get("external_calls") is False and det.get("side_effects") is False:
        checks.append({"name": "Determinism declaration", "status": "PASS", "message": "Determinism flags valid"})
    else:
        checks.append({"name": "Determinism declaration", "status": "FAIL", "message": "Determinism flags invalid"})

    # Check engine identity presence
    eng = prov.get("engine_identity", {})
    if eng.get("engine_name") == "GOD Engine" and eng.get("engine_version"):
        checks.append({"name": "Engine identity", "status": "PASS", "message": "Engine identity present"})
    else:
        checks.append({"name": "Engine identity", "status": "FAIL", "message": "Engine identity missing or invalid"})

    overall = "PASS" if all(c["status"] == "PASS" for c in checks) else "FAIL"
    summary = "All audit checks passed." if overall == "PASS" else "One or more audit checks failed."

    report = {
        "audit_id": str(uuid.uuid4()),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "result": overall,
        "summary": summary,
        "checks": checks
    }

    out = Path(__file__).parent / "audit_report.json"
    out.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"{overall}: audit_report.json written")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("USAGE: audit.py <path/to/provenance.json>", file=sys.stderr)
        sys.exit(1)
    main(Path(sys.argv[1]).resolve())
