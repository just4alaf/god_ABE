# Example App — GOD → ABE → Output

## Purpose
Demonstrates the minimal, safe flow:
1. Read GOD artifacts (read-only)
2. Verify provenance using ABE
3. Produce a trivial downstream output

## Inputs (Read-Only)
- `provenance.json` (from GOD)
- Referenced artifacts (e.g., `execution_output.json`, `report.json`)

## Verification
- Uses `abe/verify_provenance.py`
- Fails closed on any schema or hash mismatch

## Output
- Writes a trivial file confirming verification success
- No side effects beyond local file creation

## Authority
This app has **no execution authority**.
It does not modify GOD or reinterpret constraints.
