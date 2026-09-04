#!/usr/bin/env python3
"""Fail-closed structural validation for the public SolidSecurity foundation."""

from __future__ import annotations

from pathlib import Path
import re
import sys

import yaml

ROOT = Path(__file__).resolve().parents[1]
MODEL = ROOT / "model"
errors: list[str] = []


def fail(message: str) -> None:
    errors.append(message)


def load_yaml(name: str):
    path = MODEL / name
    if not path.exists():
        fail(f"missing model file: model/{name}")
        return {}
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8"))
    except Exception as exc:  # fail closed on malformed YAML
        fail(f"invalid YAML model/{name}: {exc}")
        return {}


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


domains_doc = load_yaml("control_domains.yaml")
controls_doc = load_yaml("sample_controls.yaml")
assertions_doc = load_yaml("sample_control_assertions.yaml")
proof_doc = load_yaml("proof_ladder.yaml")
ai_doc = load_yaml("ai_authority.yaml")
enums_doc = load_yaml("foundation_enums.yaml")
classification_doc = load_yaml("data_classification.yaml")
roles_doc = load_yaml("roles.yaml")
pilot_gate_doc = load_yaml("pilot_gate.yaml")
entities_doc = load_yaml("entities.yaml")

# Common controls.
domains = domains_doc.get("domains", {}) if isinstance(domains_doc, dict) else {}
require(isinstance(domains, dict) and bool(domains), "control_domains.yaml must define domains")

controls = controls_doc.get("controls", []) if isinstance(controls_doc, dict) else []
require(isinstance(controls, list) and bool(controls), "sample_controls.yaml must define controls")
control_ids: set[str] = set()
control_pattern = re.compile(r"^SS-([A-Z]+)-([0-9]{3})$")
valid_review_classes = {"R0", "R1", "R2", "R3", "R4"}

for index, control in enumerate(controls):
    prefix = f"control[{index}]"
    require(isinstance(control, dict), f"{prefix} must be an object")
    if not isinstance(control, dict):
        continue
    cid = control.get("id")
    match = control_pattern.fullmatch(str(cid or ""))
    require(match is not None, f"{prefix} has invalid id: {cid!r}")
    if not match:
        continue
    require(cid not in control_ids, f"duplicate control id: {cid}")
    control_ids.add(cid)
    domain = control.get("domain")
    require(domain == match.group(1), f"{cid} id/domain mismatch: {domain!r}")
    require(domain in domains, f"{cid} uses undeclared domain {domain!r}")
    require(isinstance(control.get("title"), str) and bool(control["title"].strip()), f"{cid} missing title")
    require(isinstance(control.get("objective"), str) and bool(control["objective"].strip()), f"{cid} missing objective")
    evidence_classes = control.get("default_evidence_classes")
    require(isinstance(evidence_classes, list) and bool(evidence_classes), f"{cid} needs default_evidence_classes")
    require(control.get("minimum_review_class") in valid_review_classes, f"{cid} has invalid minimum_review_class")
    require(control.get("lifecycle_state") in {"active", "draft", "retired"}, f"{cid} has invalid lifecycle_state")

# Assertions must point to a declared stable control and retain deterministic IDs.
assertions = assertions_doc.get("assertions", []) if isinstance(assertions_doc, dict) else []
require(isinstance(assertions, list), "sample_control_assertions.yaml assertions must be an array")
assertion_ids: set[str] = set()
for index, assertion in enumerate(assertions):
    prefix = f"assertion[{index}]"
    require(isinstance(assertion, dict), f"{prefix} must be an object")
    if not isinstance(assertion, dict):
        continue
    aid = assertion.get("id")
    cid = assertion.get("control_id")
    require(cid in control_ids, f"{aid!r} references unknown control {cid!r}")
    require(isinstance(aid, str) and re.fullmatch(re.escape(str(cid)) + r"-A[0-9]+", aid) is not None,
            f"assertion id {aid!r} must extend its control id")
    require(aid not in assertion_ids, f"duplicate assertion id: {aid}")
    assertion_ids.add(str(aid))
    require(assertion.get("materiality") in {"low", "medium", "high", "critical"}, f"{aid} invalid materiality")
    require(isinstance(assertion.get("statement"), str) and bool(assertion["statement"].strip()), f"{aid} missing statement")

# Proof Ladder is an authority boundary, not a presentation preference.
states = proof_doc.get("states", []) if isinstance(proof_doc, dict) else []
require(isinstance(states, list), "proof_ladder.yaml states must be an array")
levels = [state.get("level") for state in states if isinstance(state, dict)]
require(levels == [0, 1, 2, 3, 4, 5], f"Proof Ladder levels must be exactly 0..5, got {levels!r}")
proof_by_id = {state.get("id"): state for state in states if isinstance(state, dict)}
for protected in ("VERIFIED", "INDEPENDENTLY_ASSURED"):
    require(protected in proof_by_id, f"Proof Ladder missing {protected}")
    if protected in proof_by_id:
        require(proof_by_id[protected].get("ai_can_assign") is False, f"AI must not assign {protected}")

# AI authority must retain red-line actions and prohibited state transitions.
authority = ai_doc.get("authority_classes", {}) if isinstance(ai_doc, dict) else {}
require(set(authority) == {"GREEN", "AMBER", "RED"}, "ai_authority.yaml must define GREEN/AMBER/RED exactly")
red_examples = set(authority.get("RED", {}).get("examples", [])) if isinstance(authority.get("RED"), dict) else set()
required_red = {
    "final_compliance_verdict",
    "material_risk_acceptance",
    "security_exception_approval",
    "final_incident_reporting_decision",
    "certification_claim",
    "independent_assurance",
}
require(required_red.issubset(red_examples), f"RED authority missing: {sorted(required_red - red_examples)}")
prohibited = set(ai_doc.get("prohibited_ai_state_transitions", [])) if isinstance(ai_doc, dict) else set()
required_prohibited = {"VERIFIED", "INDEPENDENTLY_ASSURED", "RISK_ACCEPTED", "EXCEPTION_APPROVED", "CERTIFIED"}
require(required_prohibited.issubset(prohibited), f"AI transition deny-list missing: {sorted(required_prohibited - prohibited)}")

# Customer professional trust remains explicit and fail-closed.
review_descriptions = ai_doc.get("review_classes", {}) if isinstance(ai_doc, dict) else {}
require(isinstance(review_descriptions, dict) and set(review_descriptions) == valid_review_classes,
        "ai_authority.yaml review_classes must define R0..R4 exactly")
customer_reviews = ai_doc.get("customer_professional_review_classes", {}) if isinstance(ai_doc, dict) else {}
require(isinstance(customer_reviews, dict) and set(customer_reviews) == valid_review_classes,
        "ai_authority.yaml customer_professional_review_classes must define R0..R4 exactly")
if isinstance(customer_reviews, dict):
    required_fields = {
        "human_reviewer_required", "customer_verified_authority", "competence_expectation",
        "credential_expectation", "independence_requirement", "capacity_assumption_required",
        "loaded_cost_assumption_required", "escalation",
    }
    for review_class in sorted(valid_review_classes):
        item = customer_reviews.get(review_class, {})
        require(isinstance(item, dict), f"customer professional review {review_class} must be an object")
        if not isinstance(item, dict):
            continue
        require(required_fields.issubset(item), f"customer professional review {review_class} missing required fields")
        for field in ("customer_verified_authority", "competence_expectation", "credential_expectation", "independence_requirement", "escalation"):
            require(isinstance(item.get(field), str) and bool(item.get(field)), f"customer professional review {review_class} invalid {field}")
        for field in ("human_reviewer_required", "capacity_assumption_required", "loaded_cost_assumption_required"):
            require(isinstance(item.get(field), bool), f"customer professional review {review_class} invalid {field}")
    for review_class in ("R0", "R1"):
        require(customer_reviews.get(review_class, {}).get("customer_verified_authority") == "prohibited",
                f"{review_class} must not issue customer VERIFIED")
    for review_class in ("R2", "R3"):
        item = customer_reviews.get(review_class, {})
        require(item.get("human_reviewer_required") is True, f"{review_class} requires human reviewer")
        require(item.get("customer_verified_authority") == "permitted_only_when_customer_verified_gate_passes",
                f"{review_class} customer VERIFIED must remain gate-dependent")
        require(item.get("capacity_assumption_required") is True, f"{review_class} requires reviewer capacity assumption")
        require(item.get("loaded_cost_assumption_required") is True, f"{review_class} requires loaded-cost assumption")
    require(customer_reviews.get("R3", {}).get("independence_requirement") == "independent_internal_or_external",
            "R3 must require independent review")
    require(customer_reviews.get("R4", {}).get("customer_verified_authority") == "external_authority_dependent",
            "R4 must remain external-authority dependent")
    require(customer_reviews.get("R4", {}).get("independence_requirement") == "external_authority",
            "R4 must require external authority")

separation = ai_doc.get("trust_domain_separation", {}) if isinstance(ai_doc, dict) else {}
for boundary in (
    "product_change_b1_is_customer_professional_review",
    "customer_professional_review_is_external_independent_assurance",
    "internal_review_may_claim_certification",
):
    require(isinstance(separation, dict) and separation.get(boundary) is False,
            f"trust-domain separation weakened: {boundary}")

verified_gate = ai_doc.get("customer_verified_gate", {}) if isinstance(ai_doc, dict) else {}
require(isinstance(verified_gate, dict), "customer_verified_gate must be an object")
if isinstance(verified_gate, dict):
    require(verified_gate.get("readiness_status") == "DESIGN_ONLY", "customer VERIFIED gate must remain DESIGN_ONLY")
    require(verified_gate.get("fail_closed") is True, "customer VERIFIED gate must fail closed")
    require(verified_gate.get("customer_verified_currently_enabled") is False,
            "WP03 must not enable customer VERIFIED claims")
    require(verified_gate.get("legal_contract_approval_currently_enabled") is False,
            "WP03 must not approve legal contract terms")
    require(verified_gate.get("missing_or_unresolved_state") == "NEEDS_REVIEW",
            "missing customer VERIFIED prerequisite must resolve to NEEDS_REVIEW")
    prerequisites = set(verified_gate.get("required_prerequisites", [])) if isinstance(verified_gate.get("required_prerequisites"), list) else set()
    required_prerequisites = {
        "applicable_review_class_satisfied",
        "reviewer_identity_and_scope_competence_recorded",
        "credential_expectation_addressed",
        "independence_requirement_satisfied",
        "reviewer_capacity_confirmed",
        "loaded_cost_assumption_recorded",
        "escalation_path_available",
        "liability_and_insurance_posture_reviewed",
        "contractual_scope_and_liability_limits_reviewed",
        "verified_report_language_approved",
        "post_verification_incident_posture_defined",
        "client_contract_and_dpa_ready",
        "subprocessor_review_ready",
        "retention_and_deletion_schedule_ready",
    }
    require(required_prerequisites.issubset(prerequisites),
            f"customer VERIFIED gate missing prerequisites: {sorted(required_prerequisites - prerequisites)}")
    require(isinstance(verified_gate.get("transition_rule"), str) and bool(verified_gate.get("transition_rule", "").strip()),
            "customer VERIFIED gate requires transition rule")

# Applicability must preserve unresolved/professional-review states.
applicability = set(enums_doc.get("applicability_status", [])) if isinstance(enums_doc, dict) else set()
required_applicability = {"APPLICABLE", "NOT_APPLICABLE", "UNDETERMINED", "PENDING_PROFESSIONAL_REVIEW"}
require(required_applicability.issubset(applicability), "foundation_enums.yaml weakens applicability state model")

# Client/secret material must remain impossible to classify as public-repo-safe.
classes = classification_doc.get("classes", {}) if isinstance(classification_doc, dict) else {}
for name in ("CLIENT_CONFIDENTIAL", "CLIENT_HIGH_SENSITIVITY", "SECRET"):
    require(name in classes, f"data classification missing {name}")
    if name in classes:
        require(classes[name].get("public_github") == "prohibited", f"{name} must be prohibited in public GitHub")
require(classes.get("CLIENT_HIGH_SENSITIVITY", {}).get("external_llm") == "deny_by_default",
        "CLIENT_HIGH_SENSITIVITY must be deny_by_default for external LLM")
require(classes.get("SECRET", {}).get("external_llm") == "prohibited", "SECRET must be prohibited for external LLM")

# Agent role cannot acquire human-only decision authority through model drift.
roles = roles_doc.get("roles", {}) if isinstance(roles_doc, dict) else {}
agent = roles.get("agent_service", {}) if isinstance(roles, dict) else {}
require(agent.get("human") is False, "agent_service must remain non-human")
require(agent.get("human_only_decisions") == "prohibited", "agent_service must prohibit human-only decisions")
human_only = set(roles_doc.get("human_only_actions", [])) if isinstance(roles_doc, dict) else set()
required_human_only = {
    "professional_verification",
    "independent_assurance",
    "risk_acceptance",
    "exception_approval",
    "final_legal_or_regulatory_applicability",
    "certification_claim",
    "material_incident_notification_decision",
}
require(required_human_only.issubset(human_only), f"human-only actions missing: {sorted(required_human_only - human_only)}")

# Real client data remains fail-closed during design.
require(pilot_gate_doc.get("real_client_data_allowed") is False, "pilot_gate must keep real_client_data_allowed=false")
require(pilot_gate_doc.get("state") == "DESIGN_ONLY", "pilot_gate state must remain DESIGN_ONLY before separately authorized transition")
required_gate_names = {
    "foundation_assurance",
    "client_contract_and_dpa",
    "subprocessor_review",
    "retention_schedule",
    "tenant_isolation_test",
    "export_delete_test",
    "llm_processing_policy_test",
    "independent_security_data_governance_assurance",
    "principal_real_pilot_authorization",
}
gates = pilot_gate_doc.get("gates", {}) if isinstance(pilot_gate_doc, dict) else {}
require(required_gate_names.issubset(set(gates)), f"pilot gate missing: {sorted(required_gate_names - set(gates))}")

# Foundation traceability entities must remain present.
entities = entities_doc.get("entities", {}) if isinstance(entities_doc, dict) else {}
required_entities = {
    "Requirement", "Control", "ControlAssertion", "ImplementationClaim", "Evidence",
    "Assessment", "ReviewQueueItem", "Review", "Decision", "ApprovedAssertion", "AssuranceLabels"
}
require(required_entities.issubset(set(entities)), f"entity model missing: {sorted(required_entities - set(entities))}")

if errors:
    print("SOLIDSECURITY_FOUNDATION_VALIDATION=FAIL")
    for error in errors:
        print(f"ERROR: {error}")
    sys.exit(2)

print("SOLIDSECURITY_FOUNDATION_VALIDATION=PASS")
print(f"controls={len(control_ids)} assertions={len(assertion_ids)} domains={len(domains)}")
