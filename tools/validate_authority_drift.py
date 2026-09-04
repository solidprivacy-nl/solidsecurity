#!/usr/bin/env python3
"""Fail closed if current SolidSecurity authority regresses to stale Mission or duplicated Control-runtime doctrine."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]

CURRENT_FILES = [
    ROOT / "README.md",
    ROOT / "STRATEGY.md",
    ROOT / "control" / "CURRENT_STATE.md",
    ROOT / "control" / "PROJECT_GOVERNANCE_BOOTSTRAP.md",
    ROOT / "control" / "SOLIDSECURITY_ASSURANCE_CONTRACT_V1.md",
    ROOT / "control" / "SOLIDSECURITY_MISSION_CONTRACT_R2.md",
    ROOT / "docs" / "MISSION_DRIVEN_WORKFLOW.md",
    ROOT / "docs" / "WORKPACKAGES_R2.md",
    ROOT / "ROADMAP.md",
    ROOT / "model" / "mission_operating_model_r2.yaml",
    ROOT / "model" / "workpackages_r2.yaml",
]

BANNED_EXACT = [
    "MISSION_SYSTEM_V1 / CANDIDATE",
    "Control Minimal Core V1",
    "agent/mission-system-v1",
    "Control Autonomy V3.1",
    "CONTROL_AUTONOMY_V3_1",
    "semantic_workers=A1,B1",
    "implementation_role=implementation_operations/A1",
    "assurance_role=governance_release_assurance/B1",
    "independent_b1_pass",
    "PROJECT_INTEGRATION successor",
    "product/change B1 assurance",
    "E0/E1 + B1",
    "independent B1",
]

errors = []
for path in CURRENT_FILES:
    text = path.read_text(encoding="utf-8")
    for banned in BANNED_EXACT:
        if banned in text:
            errors.append(f"{path.relative_to(ROOT)} contains superseded/duplicated authority phrase: {banned!r}")

readme = (ROOT / "README.md").read_text(encoding="utf-8")
strategy = (ROOT / "STRATEGY.md").read_text(encoding="utf-8")
workflow = (ROOT / "docs" / "MISSION_DRIVEN_WORKFLOW.md").read_text(encoding="utf-8")
workpackage_index = (ROOT / "docs" / "WORKPACKAGES_R2.md").read_text(encoding="utf-8")
current = (ROOT / "control" / "CURRENT_STATE.md").read_text(encoding="utf-8")
bootstrap = (ROOT / "control" / "PROJECT_GOVERNANCE_BOOTSTRAP.md").read_text(encoding="utf-8")
mission = (ROOT / "control" / "SOLIDSECURITY_MISSION_CONTRACT_R2.md").read_text(encoding="utf-8")
assurance = (ROOT / "control" / "SOLIDSECURITY_ASSURANCE_CONTRACT_V1.md").read_text(encoding="utf-8")
roadmap = (ROOT / "ROADMAP.md").read_text(encoding="utf-8")
workpackages = (ROOT / "model" / "workpackages_r2.yaml").read_text(encoding="utf-8")

required = {
    "README.md": (
        readme,
        [
            "Mission R2 / canonical",
            "central Control-managed",
            "does **not** duplicate Control runtime versions",
            "fresh critical exact-candidate review",
        ],
    ),
    "STRATEGY.md": (
        strategy,
        [
            "current-Control exact-candidate project/change review",
            "candidate movement invalidates stale review evidence",
            "does not encode a fixed worker lane or role topology",
        ],
    ),
    "docs/MISSION_DRIVEN_WORKFLOW.md": (
        workflow,
        [
            "Central Control development boundary",
            "Fresh exact-candidate review",
            "project_local_runtime_state_plane=false",
            "candidate movement invalidates stale review",
        ],
    ),
    "docs/WORKPACKAGES_R2.md": (
        workpackage_index,
        [
            "fresh exact-candidate project-change review under current Control",
            "candidate movement invalidates stale review evidence",
            "does not encode a fixed Control worker lane count",
        ],
    ),
    "control/CURRENT_STATE.md": (
        current,
        [
            "Snapshot only",
            "owned centrally; read fresh from current Control authority",
            "Central Control boundary",
            "candidate movement invalidates stale review",
        ],
    ),
    "control/PROJECT_GOVERNANCE_BOOTSTRAP.md": (
        bootstrap,
        [
            "adoption_status=MISSION_R2_CANONICAL_CONTROL_MANAGED",
            "central_control_authority=market-predictions/control-plane",
            "current Control runtime version",
            "candidate movement invalidates stale review evidence",
        ],
    ),
    "control/SOLIDSECURITY_MISSION_CONTRACT_R2.md": (
        mission,
        [
            "MISSION R2 / CANONICAL / CONTROL-MANAGED",
            "current governed Control architecture",
            "does not require or own a particular Control worker topology",
            "fresh exact-candidate critical review",
        ],
    ),
    "control/SOLIDSECURITY_ASSURANCE_CONTRACT_V1.md": (
        assurance,
        [
            "Mission R2",
            "Central Control boundary",
            "exact candidate/head/base",
            "Candidate movement invalidates stale review",
        ],
    ),
    "ROADMAP.md": (
        roadmap,
        [
            "current central Control authority",
            "fresh exact-candidate project-change review",
            "does not encode a fixed lane count or worker-role topology locally",
        ],
    ),
    "model/workpackages_r2.yaml": (
        workpackages,
        ["fresh_exact_candidate_project_change_review_pass"],
    ),
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
