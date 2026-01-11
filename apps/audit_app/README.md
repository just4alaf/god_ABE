# Audit / Compliance App

## Purpose
Consumes GOD Engine artifacts and provenance to produce a deterministic
**PASS / FAIL audit report** with explicit reasons.

This app is **read-only** with respect to GOD outputs.

## Inputs (Required)
- `provenance.json`
- Artifacts referenced by provenance:
  - `execution_output.json`
  - `report.json`
  - `report.md` (optional)

## Verification Rules
- Validate provenance against `schemas/provenance.schema.json`
- Recompute and compare SHA-256 hashes for all referenced artifacts
- Enforce determinism declaration:
  - deterministic = true
  - external_calls = false
  - side_effects = false
- Fail closed on any violation

## Output
- `audit_report.json`
  - Deterministic
  - Machine-parseable
  - Human-readable
  - Contains PASS/FAIL and reasons

## Authority & Scope
- No execution authority
- No modification of GOD artifacts
- No reinterpretation of constraints
- External to GOD by design

If this app conflicts with GOD authority documents,
this app is wrong by definition.
