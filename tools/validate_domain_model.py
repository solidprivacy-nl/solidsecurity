#!/usr/bin/env python3
"""Fail-closed structural checks for the SolidSecurity M1 domain-model contract."""
from pathlib import Path
import re
import sys
import yaml

ROOT = Path(__file__).resolve().parents[1]
MODEL = yaml.safe_load((ROOT / "model/domain_model_v1.yaml").read_text(encoding="utf-8"))
COVERAGE = yaml.safe_load((ROOT / "spec/m1_workflow_coverage.yaml").read_text(encoding="utf-8"))
SQL = (ROOT / "spec/postgres_schema_contract_v1.sql").read_text(encoding="utf-8")
errors = []

def require(condition, message):
    if not condition:
        errors.append(message)

require(MODEL.get("version") == 1, "domain model version must be 1")
require(MODEL.get("status") == "M1_CANONICAL", "domain model status must remain M1_CANONICAL")
rt = MODEL.get("runtime_topology", {})
require(rt.get("relational_store") == "shared_postgresql", "V1 topology must be shared_postgresql")
require(rt.get("tenant_boundary") == "tenant_id", "tenant boundary must be tenant_id")
require(rt.get("database_per_client_default") is False, "database-per-client must not become the V1 default")
require(rt.get("file_bytes_in_postgresql") is False, "file bytes must remain outside PostgreSQL")

catalog = MODEL.get("catalog_entities", {})
identity = MODEL.get("identity_entities", {})
client = MODEL.get("client_entities", {})
all_entities = {**catalog, **identity, **client}
required = {
    "Tenant", "Organization", "OrganizationalScope", "UserIdentity", "Membership", "Engagement",
    "Source", "Requirement", "Control", "ControlAssertion", "RequirementControlMap",
    "ApplicabilityDecision", "ClientImplementation", "Evidence", "EvidenceVersion", "Assessment",
    "Finding", "Action", "ClientRequest", "ClientResponse", "AIProposal", "ReviewQueueItem",
    "ProfessionalReview", "Decision", "Approval", "Report", "ApprovedAssertion",
    "ApprovedAssertionControlLink", "ApprovedAssertionEvidenceLink", "AuditEvent", "RecurringReview",
    "Vendor", "AIUseCase"
}
require(required.issubset(all_entities), f"missing required entities: {sorted(required - set(all_entities))}")

user_identity = identity.get("UserIdentity", {})
require(user_identity.get("supports_nonhuman_service_identity") is True,
        "UserIdentity must support governed non-human service identities")
require("identity_type" in user_identity.get("fields", []), "UserIdentity must carry identity_type")

for name, definition in catalog.items():
    require(definition.get("tenant_owned") is False, f"catalog entity {name} must not be tenant-owned customer truth")
for name, definition in client.items():
    if name == "Tenant":
        require(definition.get("tenant_root") is True, "Tenant must be the tenant root")
        continue
    require(definition.get("tenant_owned") is True, f"client entity {name} must be tenant_owned")
    require("tenant_id" in definition.get("fields", []), f"client entity {name} must carry tenant_id")

separations = {tuple(pair) for pair in MODEL.get("required_separations", [])}
for pair in [
    ("Requirement", "Control"),
    ("Control", "ClientImplementation"),
    ("ClientImplementation", "Evidence"),
    ("Evidence", "Assessment"),
    ("Assessment", "ProfessionalReview"),
    ("AIProposal", "ProfessionalReview"),
    ("AIProposal", "Decision"),
]:
    require(pair in separations, f"missing required separation {pair}")

version = client.get("EvidenceVersion", {})
require(version.get("immutable_after_ingest") is True, "EvidenceVersion must be immutable_after_ingest")
require(version.get("immutable_object_locator") is True, "EvidenceVersion must use an immutable object locator")
for field in ["object_key", "sha256", "byte_size", "media_type", "coverage_scope", "limitations"]:
    require(field in version.get("fields", []), f"EvidenceVersion missing {field}")
require(client.get("AIProposal", {}).get("authoritative") is False, "AIProposal must be non-authoritative")
require(client.get("ProfessionalReview", {}).get("human_authority_required") is True, "ProfessionalReview must require human authority")
require(client.get("Decision", {}).get("human_authority_for_material_decisions") is True, "material Decision must require human authority")
approved_fields = set(client.get("ApprovedAssertion", {}).get("fields", []))
require("review_id" in approved_fields, "ApprovedAssertion must retain exact professional review provenance")
require("reviewer_membership_id" not in approved_fields,
        "ApprovedAssertion reviewer provenance must derive from ProfessionalReview, not a duplicate reviewer field")
link_fields = set(client.get("ApprovedAssertionControlLink", {}).get("fields", []))
require({"approved_assertion_id", "control_id", "assertion_id"}.issubset(link_fields),
        "ApprovedAssertionControlLink must bind statement to control and optional assertion")

prohibited = set(MODEL.get("prohibited_v1_tables", []))
for value in ["per_framework_client_checklist", "ai_final_compliance_verdict", "evidence_blob_bytes", "customer_database_registry", "autonomous_risk_acceptance"]:
    require(value in prohibited, f"prohibited V1 table guard missing: {value}")

require("NOT A MIGRATION" in SQL, "SQL contract must state that it is not a migration")
require("bytea" not in SQL.lower(), "SQL contract must not store evidence bytes")
require("identity_type text not null" in SQL and "('human','service')" in SQL,
        "SQL identity root must distinguish human and service identities")
require("create table solidsecurity_contract.evidence_version" in SQL, "SQL missing evidence_version")
require("object_key text not null" in SQL and "sha256 char(64) not null" in SQL,
        "SQL evidence version must bind object key and SHA-256")
require("unique(tenant_id, object_key)" in SQL,
        "SQL evidence object locator must not be reusable within a tenant")
require("create table solidsecurity_contract.ai_proposal" in SQL, "SQL missing ai_proposal")
require("create table solidsecurity_contract.professional_review" in SQL, "SQL missing professional_review")
require("create table solidsecurity_contract.decision" in SQL, "SQL missing decision")
require("create table solidsecurity_contract.approved_assertion_control_link" in SQL,
        "SQL missing approved_assertion_control_link")
require("review_id uuid references solidsecurity_contract.professional_review(review_id)" in SQL,
        "SQL ApprovedAssertion must bind professional review")
require("unique(control_id, assertion_id)" in SQL,
        "ControlAssertion must expose a composite key for hierarchy-safe references")
require("foreign key (control_id, assertion_id)" in SQL and
        "references solidsecurity_contract.control_assertion(control_id, assertion_id)" in SQL,
        "ApprovedAssertionControlLink must enforce assertion-to-control hierarchy")

approved_match = re.search(r"create table solidsecurity_contract\.approved_assertion \((.*?)\n\);", SQL, re.S | re.I)
require(approved_match is not None, "SQL missing approved_assertion")
if approved_match:
    require("reviewer_membership_id" not in approved_match.group(1),
            "SQL ApprovedAssertion must not duplicate reviewer identity outside ProfessionalReview")

def snake(name):
    step1 = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", step1).lower()

for name, definition in client.items():
    if name == "Tenant":
        continue
    table = snake(name)
    match = re.search(rf"create table solidsecurity_contract\.{re.escape(table)} \((.*?)\n\);", SQL, re.S | re.I)
    require(match is not None, f"SQL contract missing table {table}")
    if match:
        require("tenant_id uuid not null" in match.group(1).lower(), f"SQL table {table} must have non-null tenant_id")

require(COVERAGE.get("source_status") == "CANDIDATE_EVIDENCE_NOT_INTEGRATED",
        "synthetic pilot evidence must remain explicitly non-authoritative until separately integrated")
expected_sources = {
    "care_alpha": (8, "a032c22a9b9a0e264d8be88e6671c8a09c8d19c2"),
    "supplier_beta": (10, "763ead05ebd4b21eeb152f6ddcb2d652d1ce7562"),
}
canonical_chain = {"Requirement", "Control", "ClientImplementation", "Evidence", "Assessment", "ProfessionalReview", "Decision"}
for case_name, case in COVERAGE.get("cases", {}).items():
    refs = set(case.get("required_entities", []))
    unknown = refs - set(all_entities)
    require(not unknown, f"{case_name} references unknown entities: {sorted(unknown)}")
    tenant_chain = canonical_chain - {"Requirement", "Control"}
    require(tenant_chain.issubset(refs), f"{case_name} does not cover tenant traceability chain: {sorted(tenant_chain - refs)}")
    source = case.get("source", {})
    require(source.get("kind") == "pull_request_candidate", f"{case_name} source must be an exact PR candidate")
    require(source.get("integration_status") == "not_in_authoritative_main", f"{case_name} must not imply integrated pilot evidence")
    expected = expected_sources.get(case_name)
    require(expected is not None, f"unexpected synthetic coverage case: {case_name}")
    if expected:
        require(source.get("pr") == expected[0], f"{case_name} must bind PR #{expected[0]}")
        require(source.get("head_sha") == expected[1], f"{case_name} candidate SHA drift")

supplier_refs = set(COVERAGE.get("cases", {}).get("supplier_beta", {}).get("required_entities", []))
require("ApprovedAssertionControlLink" in supplier_refs and "ApprovedAssertionEvidenceLink" in supplier_refs,
        "Supplier coverage must retain both control/assertion and evidence provenance links")

if errors:
    print("SOLIDSECURITY_DOMAIN_MODEL_V1=FAIL")
    for error in errors:
        print(f"ERROR: {error}")
    sys.exit(2)

print("SOLIDSECURITY_DOMAIN_MODEL_V1=PASS")
print(f"entities={len(all_entities)} client_entities={len(client)} cases={len(COVERAGE.get('cases', {}))}")
