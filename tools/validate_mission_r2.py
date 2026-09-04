#!/usr/bin/env python3
"""Fail-closed validation for canonical SolidSecurity Mission R2 operating model/workpackages."""
from pathlib import Path
import sys
import yaml

ROOT = Path(__file__).resolve().parents[1]
MODEL = yaml.safe_load((ROOT / "model/mission_operating_model_r2.yaml").read_text(encoding="utf-8"))
WPS = yaml.safe_load((ROOT / "model/workpackages_r2.yaml").read_text(encoding="utf-8"))
REVIEW = yaml.safe_load((ROOT / "model/review_source_r2.yaml").read_text(encoding="utf-8"))
ROADMAP = (ROOT / "ROADMAP.md").read_text(encoding="utf-8")
MISSION = (ROOT / "control/SOLIDSECURITY_MISSION_CONTRACT_R2.md").read_text(encoding="utf-8")
errors = []


def require(condition, message):
    if not condition:
        errors.append(message)


require(MODEL.get("version") == 2, "mission operating model version must be 2")
require(MODEL.get("status") == "MISSION_R2_CANONICAL", "R2 model status must remain MISSION_R2_CANONICAL")
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
project_review = trust.get("product_change_assurance", {})
require(project_review.get("mechanism") == "current_control_exact_candidate_review_contract",
        "product/change review must delegate runtime mechanics to current central Control")
require(project_review.get("exact_candidate_binding_required") is True,
        "product/change review must retain exact-candidate binding")
require(project_review.get("stale_review_after_candidate_movement_forbidden") is True,
        "candidate movement must invalidate stale project-change review")
require(project_review.get("external_independent_review_when_applicable_gate_requires") is True,
        "external/independent review must remain mandatory when an applicable gate requires it")
require(project_review.get("local_fixed_worker_topology_required") is False,
        "Mission R2 must not require a duplicated local Control worker topology")
require(project_review.get("customer_assurance_qualification") is False,
        "product/change review must not imply customer professional qualification")
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
    "orphan_requirement_detection", "orphan_control_detection",
    "common_control_or_evidence_reuse_across_obligations",
}
require(required_mapping.issubset(set(mapping.get("required_demonstrations", []))),
        "mapping kernel must exercise multi-control/partial/gap/orphan/common-reuse cases")
require(mapping.get("canonical_traceability_chain_required") is True,
        "mapping kernel must preserve the canonical source-to-decision traceability chain")
require(mapping.get("proof_ladder_and_ai_authority_enforced") is True,
        "mapping kernel must enforce Proof Ladder and AI authority")

commercial = MODEL.get("commercial_validation", {})
require(commercial.get("prices_are_hypotheses_until_measured") is True,
        "prices must remain hypotheses until measured")
require(commercial.get("validated_package_requires_real_measurement") is True,
        "validated commercial packages must require real measurement")
require(commercial.get("bounded_price_package_requires_observed_willingness_to_pay_or_commitment") is True,
        "bounded pricing validation must require observed willingness-to-pay or commercial commitment")

repo = MODEL.get("repository_ip", {})
require(repo.get("public_repo_is_default_safe_for_proprietary_operating_ip") is False,
        "public repo must not be default-safe for proprietary operating IP")
require(repo.get("create_separate_private_storage_only_when_first_restricted_artifact_exists") is True,
        "private storage must be demand-driven, not speculative infrastructure")

criteria = MODEL.get("success_criteria_additions", {})
for cid in ["SS-SC-09", "SS-SC-10", "SS-SC-11", "SS-SC-12"]:
    require(cid in criteria, f"missing R2 success criterion {cid}")

require(MODEL.get("completed_predecessor") == "R2-00_CURRENT_M1_CONVERGENCE",
        "R2 must retain explicit completed M1/convergence provenance")
require(MODEL.get("active_sequence", [None])[0] == "R2-01_EXECUTABLE_ASSURANCE_KERNEL",
        "R2 active sequence must start with executable assurance kernel")

require(WPS.get("status") == "R2_WORKPACKAGES_CANONICAL",
        "R2 workpackage status must remain canonical")
wps = WPS.get("workpackages", {})
expected = ["R2-WP01", "R2-WP02", "R2-WP03", "R2-WP04", "R2-WP05"]
require(list(wps.keys()) == expected, "R2 workpackages must remain the bounded five-package sequence")
expected_issues = {"R2-WP01": 32, "R2-WP02": 33, "R2-WP03": 34, "R2-WP04": 35, "R2-WP05": 36}
for wp_id, issue_no in expected_issues.items():
    require(wps.get(wp_id, {}).get("github_issue") == issue_no,
            f"{wp_id} must remain bound to GitHub issue #{issue_no}")

expected_authority = {
    "R2-WP01": {
        "real_client_data": False,
        "production_deployment": False,
        "final_legal_compliance_verdict": False,
    },
    "R2-WP02": {
        "real_client_data": False,
        "production_deployment": False,
        "pricing_commitment": False,
    },
    "R2-WP03": {
        "real_client_data": False,
        "customer_verified_claims": False,
        "legal_contract_approval": False,
    },
    "R2-WP04": {
        "real_client_data": "PRINCIPAL_EXPLICIT_GATE_REQUIRED",
        "production_scale": False,
        "customer_environment_write": False,
        "final_legal_compliance_verdict": False,
    },
    "R2-WP05": {
        "production_deployment": "SEPARATE_GATE_REQUIRED",
        "real_client_expansion": "SEPARATE_GATE_REQUIRED",
    },
}
for wp_id, authority in expected_authority.items():
    require(wps.get(wp_id, {}).get("authority") == authority,
            f"{wp_id} authority boundary drifted from the governed R2 contract")

wp01_exit = set(wps.get("R2-WP01", {}).get("exit_evidence", []))
for required in [
    "common_control_or_evidence_reused_across_multiple_obligations_without_duplicate_client_truth",
    "canonical_source_to_decision_traceability_is_reconstructable",
    "proof_ladder_and_ai_authority_boundaries_fail_closed",
    "exact_head_ci_pass",
    "fresh_exact_candidate_project_change_review_pass",
]:
    require(required in wp01_exit, f"R2-WP01 missing executable/review evidence: {required}")
require("independent_b1_pass" not in wp01_exit,
        "R2-WP01 must not hard-code retired Control B1 lane semantics")

wp03 = wps.get("R2-WP03", {})
require("distinction_project_change_review_vs_customer_professional_vs_external_assurance" in set(wp03.get("deliverables", [])),
        "R2-WP03 must distinguish project-change review from customer/external assurance without worker-lane coupling")
wp03_exit = set(wp03.get("exit_evidence", []))
require(
    "verified_claims_fail_closed_until_all_applicable_competence_authority_independence_capacity_escalation_liability_insurance_contract_report_dpa_subprocessor_prerequisites_are_satisfied_and_reviewed" in wp03_exit,
    "R2-WP03 must fail-close customer VERIFIED until all professional/contract/data prerequisites are satisfied",
)

wp04 = wps.get("R2-WP04", {})
require(wp04.get("authority", {}).get("real_client_data") == "PRINCIPAL_EXPLICIT_GATE_REQUIRED",
        "real design partner must retain explicit principal real-data gate")
require(set(wp04.get("depends_on", [])) >= {"R2-WP01", "R2-WP02", "R2-WP03", "MINIMUM_SAFE_REAL_CLIENT_ENVELOPE"},
        "real design partner must depend on kernel, launch, professional readiness and safe client envelope")
entry = set(wp04.get("entry_evidence", []))
for required in [
    "minimum_safe_shared_tenant_aware_postgresql_runtime_proven",
    "tenant_isolation_negative_test_pass",
    "private_evidence_store_access_boundary_proven",
    "immutable_evidence_version_hash_integrity_proven",
    "encrypted_offsite_backup_and_actual_restore_proof_pass",
    "applicable_security_contract_professional_gates_pass",
    "principal_real_client_data_authorization",
]:
    require(required in entry, f"R2-WP04 missing minimum safe real-client entry proof: {required}")
wp04_exit = set(wp04.get("exit_evidence", []))
require("at_least_one_bounded_price_package_has_observed_willingness_to_pay_or_commercial_commitment" in wp04_exit,
        "R2-WP04 must require commercial evidence for at least one bounded price/package")
require("rejected_or_inconclusive_pricing_remains_open_for_retest" in wp04_exit,
        "R2-WP04 must not relabel rejected/inconclusive pricing as validated")

wp05 = wps.get("R2-WP05", {})
require(wp05.get("depends_on") == ["R2-WP04"],
        "productization must follow real design-partner evidence")
wp05_exit = set(wp05.get("exit_evidence", []))
require("client_can_understand_current_state_arranged_controls_attention_points_actions_decisions_and_reports_without_grc_or_control_id_literacy" in wp05_exit,
        "R2-WP05 must implement plain-language client visibility")
require("client_surface_does_not_use_misleading_single_compliance_percentage" in wp05_exit,
        "R2-WP05 must prohibit misleading aggregate compliance percentage")

require(REVIEW.get("adoption_status") == "CURATED_NOT_WHOLESALE", "review adoption must remain curated, not wholesale")
require(REVIEW.get("reviewed_snapshot") == "0300142", "review snapshot provenance must remain explicit")
require(len(REVIEW.get("accepted", [])) >= 10, "review decision register must preserve material accepted findings")
require(len(REVIEW.get("not_adopted", [])) >= 1, "review decision register must preserve explicit non-adoptions")

for required_phrase in [
    "scanner pass -> compliance PASS",
    "database/project per customer as default",
    "bounded real design partner",
    "bottom-up unit-economics",
    "fresh exact-candidate project-change review",
]:
    require(required_phrase.lower() in ROADMAP.lower(), f"roadmap missing R2 invariant: {required_phrase}")

for phrase in [
    "design output is not market evidence",
    "Synthetic workflow evidence",
    "Professional trust model",
    "Materiality",
    "Applicability and tailoring doctrine",
    "current governed Control architecture",
]:
    require(phrase.lower() in MISSION.lower(), f"Mission R2 missing required doctrine: {phrase}")

if errors:
    print("SOLIDSECURITY_MISSION_R2=FAIL")
    for error in errors:
        print(f"ERROR: {error}")
    sys.exit(2)

print("SOLIDSECURITY_MISSION_R2=PASS")
print(f"evidence_classes={len(classes)} workpackages={len(wps)} criteria_additions={len(criteria)} accepted_review_findings={len(REVIEW.get('accepted', []))}")
