#!/usr/bin/env python3
"""Fail-closed checks for SolidSecurity customer-facing claim authority."""
from pathlib import Path
import sys
import yaml

ROOT = Path(__file__).resolve().parents[1]
path = ROOT / "model" / "claim_vocabulary.yaml"
errors = []

try:
    doc = yaml.safe_load(path.read_text(encoding="utf-8"))
except Exception as exc:
    print(f"SOLIDSECURITY_CLAIM_VALIDATION=FAIL\nERROR: {exc}")
    raise SystemExit(2)

classes = doc.get("claim_classes", {})
required_classes = {
    "C0_DESCRIPTIVE_FACT",
    "C1_PROPOSED_ASSESSMENT",
    "C2_EVIDENCE_LINKED",
    "C3_PROFESSIONALLY_REVIEWED",
    "C4_INDEPENDENTLY_ASSURED",
    "C5_CERTIFIED",
}
if set(classes) != required_classes:
    errors.append("claim classes must remain exactly C0..C5 authority classes")

for name in ("C3_PROFESSIONALLY_REVIEWED", "C4_INDEPENDENTLY_ASSURED", "C5_CERTIFIED"):
    if classes.get(name, {}).get("ai_may_produce") is not False:
        errors.append(f"AI must not produce {name}")

restricted = doc.get("restricted_claims", {})
required_restricted = {
    "compliant",
    "fully_compliant",
    "nis2_cbw_compliant",
    "nen7510_compliant",
    "iso27001_certified",
    "ai_act_compliant",
    "independently_assured",
    "guaranteed_secure",
}
missing = required_restricted - set(restricted)
if missing:
    errors.append(f"restricted claim set weakened: missing {sorted(missing)}")
for name in required_restricted & set(restricted):
    if restricted[name].get("default_allowed") is not False:
        errors.append(f"restricted claim {name} must remain default-denied")

labels = set(doc.get("assurance_labels", []))
required_labels = {
    "self_declared", "evidence_linked", "professionally_reviewed",
    "independently_audited", "certified"
}
if not required_labels.issubset(labels):
    errors.append(f"assurance labels missing: {sorted(required_labels - labels)}")

artifact_rules = doc.get("artifact_rules", {})
if artifact_rules.get("generated_policy", {}).get("initial_state") != "DRAFT":
    errors.append("generated policies must begin as DRAFT")
if artifact_rules.get("generated_policy", {}).get("max_proof_effect_without_operational_evidence") != "DESIGNED":
    errors.append("generated policy without operational evidence may not exceed DESIGNED")
if artifact_rules.get("semantic_questionnaire_match", {}).get("customer_send_authority") is not False:
    errors.append("semantic questionnaire match must not authorize customer send")

human_only = set(doc.get("human_only_decisions", []))
required_human = {
    "professional_reviewed_claim", "independently_assured_claim", "certification_claim",
    "material_risk_acceptance", "incident_notification_decision",
    "final_legal_or_regulatory_applicability"
}
if not required_human.issubset(human_only):
    errors.append(f"claim human-only boundary weakened: missing {sorted(required_human - human_only)}")

if errors:
    print("SOLIDSECURITY_CLAIM_VALIDATION=FAIL")
    for error in errors:
        print(f"ERROR: {error}")
    sys.exit(2)

print("SOLIDSECURITY_CLAIM_VALIDATION=PASS")
