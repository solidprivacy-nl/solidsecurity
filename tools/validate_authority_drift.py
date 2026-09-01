#!/usr/bin/env python3
"""Fail closed if current SolidSecurity authority regresses to superseded Control/Mission doctrine."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]

CURRENT_FILES = [
    ROOT / "README.md",
    ROOT / "control" / "CURRENT_STATE.md",
    ROOT / "control" / "PROJECT_GOVERNANCE_BOOTSTRAP.md",
    ROOT / "control" / "SOLIDSECURITY_MISSION_CONTRACT_R2.md",
    ROOT / "docs" / "MISSION_DRIVEN_WORKFLOW.md",
    ROOT / "ROADMAP.md",
]

BANNED_EXACT = [
    "MISSION_SYSTEM_V1 / CANDIDATE",
    "Control Minimal Core V1",
    "agent/mission-system-v1",
    "A1/A2 perform implementation",
    "PROJECT_INTEGRATION successor",
]

errors = []
for path in CURRENT_FILES:
    text = path.read_text(encoding="utf-8")
    for banned in BANNED_EXACT:
        if banned in text:
            errors.append(f"{path.relative_to(ROOT)} contains superseded authority phrase: {banned!r}")

readme = (ROOT / "README.md").read_text(encoding="utf-8")
workflow = (ROOT / "docs" / "MISSION_DRIVEN_WORKFLOW.md").read_text(encoding="utf-8")
current = (ROOT / "control" / "CURRENT_STATE.md").read_text(encoding="utf-8")
mission = (ROOT / "control" / "SOLIDSECURITY_MISSION_CONTRACT_R2.md").read_text(encoding="utf-8")

required = {
    "README.md": (readme, ["Mission R2 / canonical", "Control Autonomy V3.1", "no A2"]),
    "docs/MISSION_DRIVEN_WORKFLOW.md": (workflow, ["Control Autonomy V3.1", "Exactly one semantic implementation worker exists", "There is **no semantic `PROJECT_INTEGRATION` task**"]),
    "control/CURRENT_STATE.md": (current, ["Snapshot only", "CONTROL_AUTONOMY_V3_1", "no A2"]),
    "control/SOLIDSECURITY_MISSION_CONTRACT_R2.md": (mission, ["MISSION R2 / CANONICAL", "CONTROL_AUTONOMY_V3_1", "no A2"]),
}

for name, (text, markers) in required.items():
    for marker in markers:
        if marker not in text:
            errors.append(f"{name} missing canonical authority marker: {marker!r}")

if errors:
    print("SOLIDSECURITY_AUTHORITY_DRIFT=FAIL")
    for error in errors:
        print(f"ERROR: {error}")
    sys.exit(2)

print("SOLIDSECURITY_AUTHORITY_DRIFT=PASS")
print(f"current_files_checked={len(CURRENT_FILES)}")
