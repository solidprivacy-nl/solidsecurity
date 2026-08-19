#!/usr/bin/env python3
"""Fail-closed validation for SolidSecurity Mission R2 operating model/workpackages."""
from pathlib import Path
import sys
import yaml

ROOT = Path(__file__).resolve().parents[1]
MODEL = yaml.safe_load((ROOT / "model/mission_operating_model_r2.yaml").read_text(encoding="utf-8"))
WPS = yaml.safe_load((ROOT / "model/workpackages_r2.yaml").read_text(encoding="utf-8"))
ROADMAP = (ROOT / "ROADMAP.md").read_text(encoding="utf-8")
MISSION = (ROOT / "control/SOLIDSECURITY_MISSION_CONTRACT_R2.md").read_text(encoding="utf-8")
errors = []


def require(condition, message):
    if not condition:
        errors.append(message)


require(MODEL.get("version") == 2, "mission operating model version must be 2")
require(MODEL.get("status") == "MISSION_R2_CANDIDATE", "R2 model must remain candidate before integration")
mission = MODEL.get("mission", {})
require(mission.get("primary_launch_track") == "care", "Care must be the primary launch track")
require(mission.get("secondary_reuse_track") == "supplier", "Supplier must remain the secondary reuse track")

primary = MODEL.get("launch_icp", {}).get("primary", {})
positioning = primary.get("regulatory_positioning", {})
require(positioning.get("direct_cbw_claim_requires_explicit_applicability_decision") is True,
        "direct Cbw positioning must require explicit applicability")

classes = MODEL.get("evidence_classes", {})
required_classes = {
    "E0_DESIGN", "E1_SYNTHETIC", "E2_CONTROLLED_REAL_CLIENT",
    "E3_MARKET_COMMERCIAL", "E4_REPEATED_OPERATIONAL"
}
require(required_classes.issubset(classes), f"missing R2 evidence classes: {sorted(required_classes - set(classes))}")
sub = MODEL.get("proof_substitution_rules", {})
for key in [
    "synthetic_cannot_satisfy_real_client_criterion",
    "design_cannot_satisfy_market_criterion",
    "lower_evidence_class_cannot_replace_required_higher_class",
]:
    require(sub.get(key) is True, f"proof substitution guard must remain true: {key}")

trust = MODEL.get("professional_trust_domains", {})
require(trust.get("product_change_assurance", {}).get("customer_assurance_qualification") is False,
        "product/change B1 must not imply customer professional qualification")
require(trust.get("external_independent_assurance", {}).get("internal_review_is_equivalent") is False,
        "internal review must not equal external independent assurance")

materiality = MODEL.get("materiality", {})
require(materiality.get("automation_may_lower_required_review_class") is False,
        "automation must not lower material review class")

applicability = MODEL.get("applicability_tailoring", {})
require(applicability.get("material_legal_regulatory_applicability_requires_governed_human_decision") is True,
        "material applicability must remain a governed human decision")

sem = MODEL.get("evidence_semantics", {})
require(sem.get("conflict_state") == "CONFLICT_DETECTED", "evidence conflict state must be explicit")
require(sem.get("conflict_behavior", {}).get("material_conflict_blocks_promotion") is True,
        "material evidence conflict must block promotion")
require(sem.get("expiry_behavior", {}).get("stale_green_status_forbidden") is True,
        "evidence expiry must not leave stale green status")

mapping = MODEL.get("mapping_kernel", {})
required_mapping = {
    "one_requirement_to_multiple_controls", "partial_mapping", "coverage_gap",
    "orphan_requirement_detection", "orphan_control_detection"
}
require(required_mapping.issubset(set(mapping.get("required_demonstrations", []))),
        "mapping kernel must exercise multi-control/partial/gap/orphan cases")

commercial = MODEL.get("commercial_validation", {})
require(commercial.get("prices_are_hypotheses_until_measured") is True,
        "prices must remain hypotheses until measured")
require(commercial.get("validated_package_requires_real_measurement") is True,
        "validated commercial packages must require real measurement")

repo = MODEL.get("repository_ip", {})
require(repo.get("public_repo_is_default_safe_for_proprietary_operating_ip") is False,
        "public repo must not be default-safe for proprietary operating IP")

criteria = MODEL.get("success_criteria_additions", {})
for cid in ["SS-SC-09", "SS-SC-10", "SS-SC-11", "SS-SC-12"]:
    require(cid in criteria, f"missing R2 success criterion {cid}")

wps = WPS.get("workpackages", {})
expected = ["R2-WP01", "R2-WP02", "R2-WP03", "R2-WP04", "R2-WP05"]
require(list(wps.keys()) == expected, "R2 workpackages must remain the bounded five-package sequence")
require(wps.get("R2-WP04", {}).get("authority", {}).get("real_client_data") == "PRINCIPAL_EXPLICIT_GATE_REQUIRED",
        "real design partner must retain explicit principal real-data gate")
require(set(wps.get("R2-WP04", {}).get("depends_on", [])) >= {"R2-WP01", "R2-WP02", "R2-WP03"},
        "real design partner must depend on kernel, launch and professional readiness")
require(wps.get("R2-WP05", {}).get("depends_on") == ["R2-WP04"],
        "productization must follow real design-partner evidence")

for forbidden in ["scanner pass -> compliance PASS", "database/project per customer as default"]:
    require(forbidden in ROADMAP, f"roadmap must retain explicit deferred/invariant phrase: {forbidden}")

for phrase in [
    "design output is not market evidence",
    "Synthetic workflow evidence",
    "Professional trust model",
    "Materiality",
    "Applicability and tailoring doctrine",
]:
    require(phrase.lower() in MISSION.lower(), f"Mission R2 missing required doctrine: {phrase}")

if errors:
    print("SOLIDSECURITY_MISSION_R2=FAIL")
    for error in errors:
        print(f"ERROR: {error}")
    sys.exit(2)

print("SOLIDSECURITY_MISSION_R2=PASS")
print(f"evidence_classes={len(classes)} workpackages={len(wps)} criteria_additions={len(criteria)}")
