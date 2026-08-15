#!/usr/bin/env python3
"""Validate the immutable minimum shape of the pilot runtime acceptance contract."""
from pathlib import Path
import sys
import yaml

ROOT = Path(__file__).resolve().parents[1]
path = ROOT / "spec" / "runtime_acceptance.yaml"
errors = []

try:
    doc = yaml.safe_load(path.read_text(encoding="utf-8"))
except Exception as exc:
    print(f"SOLIDSECURITY_RUNTIME_ACCEPTANCE_VALIDATION=FAIL\nERROR: {exc}")
    raise SystemExit(2)

if doc.get("status") != "SPECIFIED_NOT_EXECUTED":
    errors.append("acceptance contract must not claim execution before a deployed candidate exists")
if doc.get("real_client_gate_effect") != "BLOCK_IF_ANY_MANDATORY_NOT_PASS":
    errors.append("mandatory runtime tests must fail-close the real-client gate")
if set(doc.get("allowed_results", [])) != {"PASS", "FAIL", "INDETERMINATE"}:
    errors.append("allowed test results must be PASS/FAIL/INDETERMINATE")

scenarios = doc.get("scenarios", [])
ids = [item.get("id") for item in scenarios if isinstance(item, dict)]
if len(ids) != len(set(ids)):
    errors.append("runtime acceptance scenario IDs must be unique")
required_ids = {f"RTA-{i:03d}" for i in range(1, 22)}
missing = required_ids - set(ids)
if missing:
    errors.append(f"mandatory scenario set weakened: missing {sorted(missing)}")

required_families = {
    "tenant_isolation",
    "evidence_integrity",
    "ai_data_boundary",
    "lifecycle",
    "resilience",
    "independent_recovery",
    "cryptographic_separation",
    "recovery_objectives",
}
actual_families = {
    item.get("family") for item in scenarios if isinstance(item, dict)
}
missing_families = required_families - actual_families
if missing_families:
    errors.append(f"mandatory security family set weakened: missing {sorted(missing_families)}")

for item in scenarios:
    if not isinstance(item, dict):
        errors.append("every scenario must be an object")
        continue
    sid = item.get("id", "UNKNOWN")
    if item.get("mandatory") is not True:
        errors.append(f"{sid} must remain mandatory in V1")
    if item.get("severity") not in {"critical", "high"}:
        errors.append(f"{sid} invalid severity")
    expected = item.get("expected")
    if not isinstance(expected, list) or not expected:
        errors.append(f"{sid} must define expected outcomes")

if errors:
    print("SOLIDSECURITY_RUNTIME_ACCEPTANCE_VALIDATION=FAIL")
    for error in errors:
        print(f"ERROR: {error}")
    sys.exit(2)

print("SOLIDSECURITY_RUNTIME_ACCEPTANCE_VALIDATION=PASS")
print(f"mandatory_scenarios={len(scenarios)}")
