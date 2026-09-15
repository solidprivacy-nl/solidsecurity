#!/usr/bin/env python3
"""Fail-closed validation and deterministic rendering for SolidSecurity R2-WP01."""
from __future__ import annotations

from copy import deepcopy
from datetime import date, datetime, timezone
from pathlib import Path
import re
import sys
from typing import Any, Callable

import yaml

ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = ROOT / "model/assurance_kernel_v1.yaml"
CONTROLS_PATH = ROOT / "model/sample_controls.yaml"
PROOF_PATH = ROOT / "model/proof_ladder.yaml"
AUTHORITY_PATH = ROOT / "model/ai_authority.yaml"
ENUMS_PATH = ROOT / "model/foundation_enums.yaml"
M1_SCHEMA_PATH = ROOT / "spec/postgres_schema_contract_v1.sql"
GOLDEN_PATH = ROOT / "spec/assurance_kernel_v1_dossier.md"
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


class UniqueKeyLoader(yaml.SafeLoader):
    pass


def _construct_mapping(loader: yaml.SafeLoader, node: yaml.nodes.MappingNode, deep: bool = False) -> dict[Any, Any]:
    result: dict[Any, Any] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in result:
            raise ValueError(f"duplicate YAML key: {key!r}")
        result[key] = loader.construct_object(value_node, deep=deep)
    return result


UniqueKeyLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _construct_mapping)


def load_yaml(path: Path) -> dict[str, Any]:
    value = yaml.load(path.read_text(encoding="utf-8"), Loader=UniqueKeyLoader)
    if not isinstance(value, dict):
        raise ValueError(f"{path.name} root must be a mapping")
    return value


def as_date(value: object) -> date | None:
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    if isinstance(value, str):
        try:
            return date.fromisoformat(value)
        except ValueError:
            return None
    return None


def as_dt(value: object) -> datetime | None:
    if isinstance(value, datetime):
        return value if value.tzinfo is not None else None
    if isinstance(value, str):
        try:
            parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError:
            return None
        return parsed if parsed.tzinfo is not None else None
    return None


def clean_id(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip()) and value == value.strip()


def nonempty_string(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def index(items: object, key: str, errors: list[str]) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    if not isinstance(items, list):
        errors.append(f"{key} collection must be a list")
        return result
    for item in items:
        if not isinstance(item, dict):
            errors.append(f"{key} collection contains non-object item")
            continue
        ident = item.get(key)
        if not clean_id(ident):
            errors.append(f"{key} must be a clean non-empty string")
            continue
        if ident in result:
            errors.append(f"duplicate {key}: {ident}")
            continue
        result[ident] = item
    return result


def evidence_valid(item: dict[str, Any], on_date: date) -> bool:
    start = as_date(item.get("valid_from"))
    end = as_date(item.get("expires_at"))
    return start is not None and end is not None and start <= on_date <= end


def authority_fields_ok(
    *,
    review_class: object,
    independence_class: object,
    reviewer_id: object,
    review_rank: dict[str, int],
    errors: list[str],
    label: str,
    separated_from: list[object] | None = None,
    external_authority_ref: object = None,
) -> None:
    def require(condition: bool, message: str) -> None:
        if not condition:
            errors.append(message)

    require(review_class in review_rank, f"{label} review class invalid")
    require(clean_id(reviewer_id), f"{label} requires clean reviewer identity")
    allowed = {"INTERNAL_QUALIFIED", "INDEPENDENT_INTERNAL", "INDEPENDENT_EXTERNAL"}
    require(independence_class in allowed, f"{label} independence class invalid")
    if review_class not in review_rank:
        return
    rank = review_rank[review_class]
    if rank >= review_rank["R3"]:
        require(independence_class in {"INDEPENDENT_INTERNAL", "INDEPENDENT_EXTERNAL"}, f"{label} R3+ requires independent reviewer")
        for other in separated_from or []:
            if clean_id(other) and clean_id(reviewer_id):
                require(reviewer_id != other, f"{label} R3+ reviewer must be separated from claimant/proposer/assessor authority")
    if rank >= review_rank["R4"]:
        require(independence_class == "INDEPENDENT_EXTERNAL", f"{label} R4 requires external independence")
        require(clean_id(external_authority_ref), f"{label} R4 requires external authority provenance")


def validate(
    model: dict[str, Any],
    controls_doc: dict[str, Any],
    proof_doc: dict[str, Any],
    authority_doc: dict[str, Any],
    enums_doc: dict[str, Any],
    schema_text: str,
) -> tuple[list[str], dict[str, Any]]:
    errors: list[str] = []

    def require(condition: bool, message: str) -> None:
        if not condition:
            errors.append(message)

    require(model.get("version") == 1, "kernel version must be 1")
    require(model.get("status") == "R2_WP01_CANDIDATE", "kernel status must remain R2_WP01_CANDIDATE")
    require(model.get("mission_gap") == "SS-R2-GAP-01", "kernel must remain bound to SS-R2-GAP-01")
    require(model.get("semantic_projection_only") is True, "kernel must remain a semantic projection")
    require(model.get("customer_facing") is False, "synthetic kernel must not be customer-facing")
    require(model.get("mission_evidence_class") == "E1_SYNTHETIC", "kernel must remain E1 synthetic evidence")
    as_of = as_date(model.get("as_of"))
    require(as_of is not None, "kernel as_of must be a complete ISO date")
    if as_of is None:
        as_of = date.min
    max_validity_days = model.get("max_evidence_validity_days")
    require(isinstance(max_validity_days, int) and not isinstance(max_validity_days, bool) and max_validity_days > 0,
            "max_evidence_validity_days must be a positive integer")

    require("proposed_proof_level between 0 and 3" in schema_text,
            "M1 assessment proposal range must remain 0..3")
    proof_states = proof_doc.get("states", []) if isinstance(proof_doc, dict) else []
    proof_levels = {
        item.get("id"): item.get("level")
        for item in proof_states
        if isinstance(item, dict) and isinstance(item.get("id"), str) and isinstance(item.get("level"), int)
    }
    required_proof = {
        "UNKNOWN": 0,
        "DESIGNED": 1,
        "IMPLEMENTED": 2,
        "EVIDENCED": 3,
        "VERIFIED": 4,
        "INDEPENDENTLY_ASSURED": 5,
    }
    require(proof_levels == required_proof, "canonical Proof Ladder drifted")

    review_classes = authority_doc.get("review_classes", {}) if isinstance(authority_doc, dict) else {}
    review_rank = {
        name: int(name[1:])
        for name in review_classes
        if isinstance(name, str) and re.fullmatch(r"R[0-4]", name)
    }
    require(set(review_rank) == {"R0", "R1", "R2", "R3", "R4"}, "canonical R0..R4 review classes missing")
    verified_gate = authority_doc.get("customer_verified_gate", {}) if isinstance(authority_doc, dict) else {}
    require(isinstance(verified_gate, dict) and verified_gate.get("fail_closed") is True,
            "customer VERIFIED gate must remain fail-closed")
    require(isinstance(verified_gate, dict) and verified_gate.get("customer_verified_currently_enabled") is False,
            "WP01 must not enable customer VERIFIED")

    canonical_results = set(enums_doc.get("assessment_result", [])) if isinstance(enums_doc, dict) else set()
    applicability_statuses = set(enums_doc.get("applicability_status", [])) if isinstance(enums_doc, dict) else set()
    require(applicability_statuses == {"APPLICABLE", "NOT_APPLICABLE", "UNDETERMINED", "PENDING_PROFESSIONAL_REVIEW"},
            "canonical applicability status set drifted")
    materiality_min = {"low": "R1", "medium": "R2", "high": "R3", "critical": "R4"}

    sources = index(model.get("sources"), "source_id", errors)
    scopes = index(model.get("scopes"), "scope_id", errors)
    requirements = index(model.get("requirements"), "requirement_id", errors)
    catalog = index(controls_doc.get("controls"), "id", errors)
    mappings = index(model.get("requirement_control_maps"), "mapping_id", errors)
    applicability = index(model.get("applicability_decisions"), "applicability_id", errors)
    implementations = index(model.get("client_implementations"), "implementation_id", errors)
    evidence = index(model.get("evidence"), "evidence_id", errors)
    links = index(model.get("implementation_evidence_links"), "link_id", errors)
    assessments = index(model.get("assessments"), "assessment_id", errors)
    conflicts = index(model.get("evidence_conflicts"), "conflict_id", errors)
    reviews = index(model.get("professional_reviews"), "review_id", errors)
    decisions = index(model.get("decisions"), "decision_id", errors)

    for source_id, source in sources.items():
        require(source.get("source_type") == "internal_synthetic_requirement_set",
                f"source {source_id} must remain synthetic")
        require(nonempty_string(source.get("version")), f"source {source_id} requires version")

    scoped_controls = model.get("control_scope")
    require(isinstance(scoped_controls, list) and bool(scoped_controls), "control_scope must be non-empty")
    scoped_ids = [item for item in scoped_controls if clean_id(item)] if isinstance(scoped_controls, list) else []
    require(len(scoped_ids) == len(scoped_controls or []), "control_scope IDs must be clean strings")
    require(len(scoped_ids) == len(set(scoped_ids)), "control_scope must not contain duplicates")
    controls: dict[str, dict[str, Any]] = {}
    for control_id in scoped_ids:
        control = catalog.get(control_id)
        require(control is not None, f"unknown canonical control {control_id}")
        if control is not None:
            require(control.get("lifecycle_state") == "active", f"control {control_id} must be active")
            require(control.get("minimum_review_class") in review_rank,
                    f"control {control_id} has invalid review class")
            controls[control_id] = control

    for requirement_id, requirement in requirements.items():
        require(requirement.get("source_id") in sources,
                f"requirement {requirement_id} references unknown source")

    maps_by_req: dict[str, list[dict[str, Any]]] = {rid: [] for rid in requirements}
    reqs_by_control: dict[str, set[str]] = {cid: set() for cid in controls}
    mapping_review_times: dict[tuple[str, str], datetime] = {}
    for mapping_id, mapping in mappings.items():
        rid = mapping.get("requirement_id")
        cid = mapping.get("control_id")
        require(rid in requirements, f"mapping {mapping_id} references unknown requirement")
        require(cid in controls, f"mapping {mapping_id} references control outside control_scope")
        req = requirements.get(str(rid), {})
        source_id = req.get("source_id")
        source = sources.get(str(source_id), {})
        require(mapping.get("framework_ref") == source_id,
                f"mapping {mapping_id} source reference mismatch")
        require(nonempty_string(mapping.get("framework_version")),
                f"mapping {mapping_id} requires framework version")
        require(mapping.get("framework_version") == source.get("version"),
                f"mapping {mapping_id} source version mismatch")
        require(mapping.get("source_requirement_ref") == rid,
                f"mapping {mapping_id} requirement provenance mismatch")
        require(mapping.get("relationship") in {"primary", "partial", "supporting"},
                f"mapping {mapping_id} relationship invalid")
        require(mapping.get("coverage") in {"FULL", "PARTIAL"},
                f"mapping {mapping_id} coverage invalid")
        require(mapping.get("mapping_status") == "approved",
                f"mapping {mapping_id} must be approved")
        require(mapping.get("reviewer_actor_type") == "HUMAN",
                f"mapping {mapping_id} requires human review")
        require(clean_id(mapping.get("reviewer_id")),
                f"mapping {mapping_id} requires clean reviewer identity")
        version = mapping.get("mapping_version")
        require(isinstance(version, int) and not isinstance(version, bool) and version > 0,
                f"mapping {mapping_id} requires positive mapping version")
        reviewed_at = as_dt(mapping.get("reviewed_at"))
        require(reviewed_at is not None, f"mapping {mapping_id} requires reviewed_at")
        require(nonempty_string(mapping.get("rationale")), f"mapping {mapping_id} requires rationale")
        if reviewed_at is not None:
            require(reviewed_at.date() <= as_of, f"mapping {mapping_id} review occurs after dossier as_of")
        if rid in requirements and cid in controls and mapping.get("mapping_status") == "approved" and reviewed_at is not None:
            pair = (str(rid), str(cid))
            require(pair not in mapping_review_times, f"duplicate approved mapping for {pair[0]}->{pair[1]}")
            if pair not in mapping_review_times:
                mapping_review_times[pair] = reviewed_at
                maps_by_req[str(rid)].append(mapping)
                reqs_by_control[str(cid)].add(str(rid))

    apps_by_req: dict[str, list[dict[str, Any]]] = {rid: [] for rid in requirements}
    app_review_times: dict[str, datetime] = {}
    app_effective_dates: dict[str, date] = {}
    for app_id, app in applicability.items():
        rid = app.get("requirement_id")
        require(rid in requirements, f"applicability {app_id} references unknown requirement")
        require(app.get("scope_id") in scopes, f"applicability {app_id} references unknown scope")
        require(app.get("status") in applicability_statuses,
                f"applicability {app_id} status is outside canonical enum")
        req = requirements.get(str(rid), {})
        source = sources.get(str(req.get("source_id")), {})
        require(app.get("source_id") == req.get("source_id"),
                f"applicability {app_id} source mismatch")
        require(nonempty_string(app.get("source_framework_version")),
                f"applicability {app_id} requires source framework version")
        require(app.get("source_framework_version") == source.get("version"),
                f"applicability {app_id} source version mismatch")
        require(isinstance(app.get("scope_facts"), list) and bool(app.get("scope_facts")),
                f"applicability {app_id} requires scope facts")
        require(isinstance(app.get("uncertainty_or_exclusions"), list) and bool(app.get("uncertainty_or_exclusions")),
                f"applicability {app_id} requires exclusions/uncertainty")
        require(nonempty_string(app.get("rationale")), f"applicability {app_id} requires rationale")
        require(app.get("proposer_actor_type") in {"AI", "HUMAN"},
                f"applicability {app_id} proposer actor invalid")
        require(clean_id(app.get("proposer_id")), f"applicability {app_id} requires proposer identity")
        required_class = app.get("required_review_class")
        actual_class = app.get("review_class")
        require(required_class in review_rank and review_rank.get(required_class, -1) >= review_rank.get("R2", 2),
                f"applicability {app_id} requires R2+ review")
        require(actual_class in review_rank and review_rank.get(actual_class, -1) >= review_rank.get(required_class, 99),
                f"applicability {app_id} actual review class too weak")
        require(app.get("reviewer_actor_type") == "HUMAN",
                f"applicability {app_id} requires human review")
        authority_fields_ok(
            review_class=actual_class,
            independence_class=app.get("independence_class"),
            reviewer_id=app.get("reviewer_id"),
            review_rank=review_rank,
            errors=errors,
            label=f"applicability {app_id}",
            separated_from=[app.get("proposer_id")],
            external_authority_ref=app.get("external_authority_ref"),
        )
        require(app.get("review_decision") == "ACCEPT",
                f"applicability {app_id} requires explicit accepted review decision")
        reviewed_at = as_dt(app.get("reviewed_at"))
        effective = as_date(app.get("effective_date"))
        expires = as_date(app.get("expires_at"))
        require(reviewed_at is not None, f"applicability {app_id} requires reviewed_at")
        require(effective is not None and expires is not None and effective <= as_of <= expires,
                f"applicability {app_id} effective window invalid")
        if reviewed_at is not None and effective is not None:
            require(reviewed_at.date() <= effective,
                    f"applicability {app_id} review must not occur after effective date")
        require(nonempty_string(app.get("reevaluation_trigger")),
                f"applicability {app_id} requires reevaluation trigger")
        if rid in requirements:
            apps_by_req[str(rid)].append(app)
            if reviewed_at is not None:
                app_review_times[str(rid)] = reviewed_at
            if effective is not None:
                app_effective_dates[str(rid)] = effective
    for rid, items in apps_by_req.items():
        require(len(items) == 1, f"requirement {rid} must have exactly one applicability decision")

    implementation_declared_times: dict[str, datetime] = {}
    for impl_id, impl in implementations.items():
        require(impl.get("control_id") in controls,
                f"implementation {impl_id} references unknown/out-of-scope control")
        require(impl.get("scope_id") in scopes,
                f"implementation {impl_id} references unknown scope")
        require(impl.get("source_of_claim") in {"accepted_human_statement", "generated_policy"},
                f"implementation {impl_id} source_of_claim invalid")
        require(impl.get("implementation_status") in {"DESIGNED", "OPERATING"},
                f"implementation {impl_id} status invalid")
        if impl.get("source_of_claim") == "generated_policy":
            require(impl.get("implementation_status") == "DESIGNED",
                    f"generated policy {impl_id} must remain DESIGNED")
        else:
            require(impl.get("implementation_status") == "OPERATING",
                    f"accepted implementation {impl_id} must be OPERATING")
            require(impl.get("declared_by_actor_type") == "HUMAN",
                    f"accepted implementation {impl_id} requires human declarer")
            require(clean_id(impl.get("declared_by")),
                    f"accepted implementation {impl_id} requires declarer identity")
            require(clean_id(impl.get("owner_membership_id")),
                    f"accepted implementation {impl_id} requires owner identity")
            require(nonempty_string(impl.get("acceptance_ref")),
                    f"accepted implementation {impl_id} requires acceptance provenance")
            declared_at = as_dt(impl.get("declared_at"))
            require(declared_at is not None, f"accepted implementation {impl_id} requires declared_at")
            if declared_at is not None:
                require(declared_at.date() <= as_of,
                        f"accepted implementation {impl_id} declared after dossier as_of")
                implementation_declared_times[impl_id] = declared_at

    evidence_capture_times: dict[str, datetime] = {}
    for evidence_id, item in evidence.items():
        require(item.get("source_type") == "internal_synthetic_evidence",
                f"evidence {evidence_id} must remain synthetic")
        require(item.get("mission_evidence_class") == model.get("mission_evidence_class") == "E1_SYNTHETIC",
                f"evidence {evidence_id} Mission evidence class mismatch")
        require(nonempty_string(item.get("source_ref")), f"evidence {evidence_id} requires source provenance")
        require(SHA256_RE.fullmatch(str(item.get("sha256", ""))) is not None,
                f"evidence {evidence_id} requires SHA-256")
        require(item.get("scope_id") in scopes, f"evidence {evidence_id} references unknown scope")
        require(item.get("coverage_scope") == item.get("scope_id") and item.get("coverage_scope") in scopes,
                f"evidence {evidence_id} coverage scope must match governed evidence scope")
        require(item.get("captured_by_actor_type") in {"HUMAN", "SYSTEM"},
                f"evidence {evidence_id} captured actor invalid")
        require(clean_id(item.get("captured_by")),
                f"evidence {evidence_id} requires clean capture identity")
        captured_at = as_dt(item.get("captured_at"))
        require(captured_at is not None, f"evidence {evidence_id} captured_at invalid")
        if captured_at is not None:
            require(captured_at.date() <= as_of, f"evidence {evidence_id} captured after dossier as_of")
            evidence_capture_times[evidence_id] = captured_at
        start = as_date(item.get("valid_from"))
        end = as_date(item.get("expires_at"))
        require(start is not None and end is not None and start <= end,
                f"evidence {evidence_id} validity window invalid")
        if start is not None and end is not None and isinstance(max_validity_days, int):
            require((end - start).days <= max_validity_days,
                    f"evidence {evidence_id} validity window exceeds explicit kernel policy")

    linked_evidence: set[tuple[str, str]] = set()
    for link_id, link in links.items():
        impl_id = link.get("implementation_id")
        evidence_id = link.get("evidence_id")
        require(impl_id in implementations, f"evidence link {link_id} references unknown implementation")
        require(evidence_id in evidence, f"evidence link {link_id} references unknown evidence")
        pair = (str(impl_id), str(evidence_id))
        require(pair not in linked_evidence, f"duplicate implementation/evidence link {pair[0]}->{pair[1]}")
        linked_evidence.add(pair)
        if impl_id in implementations and evidence_id in evidence:
            require(implementations[str(impl_id)].get("scope_id") == evidence[str(evidence_id)].get("coverage_scope"),
                    f"evidence link {link_id} crosses governed scopes")

    assessments_by_pair: dict[tuple[str, str], list[dict[str, Any]]] = {}
    assessment_times: dict[str, datetime] = {}
    evidence_users: dict[str, set[str]] = {eid: set() for eid in evidence}
    for assessment_id, assessment in assessments.items():
        rid = assessment.get("requirement_id")
        cid = assessment.get("control_id")
        impl_id = assessment.get("implementation_id")
        require(rid in requirements, f"assessment {assessment_id} references unknown requirement")
        require(cid in controls, f"assessment {assessment_id} references unknown/out-of-scope control")
        require(any(m.get("control_id") == cid for m in maps_by_req.get(str(rid), [])),
                f"assessment {assessment_id} lacks governed requirement-control mapping")
        impl = implementations.get(str(impl_id))
        require(impl is not None, f"assessment {assessment_id} references unknown implementation")
        app_items = apps_by_req.get(str(rid), [])
        app = app_items[0] if len(app_items) == 1 else {}
        require(app.get("status") == "APPLICABLE",
                f"assessment {assessment_id} requires current APPLICABLE determination")
        if impl is not None:
            require(impl.get("control_id") == cid,
                    f"assessment {assessment_id} implementation/control mismatch")
            require(impl.get("scope_id") == app.get("scope_id"),
                    f"assessment {assessment_id} implementation scope mismatch")
            require(impl.get("source_of_claim") != "generated_policy",
                    f"assessment {assessment_id} cannot promote generated policy")
            require(impl.get("implementation_status") == "OPERATING",
                    f"assessment {assessment_id} requires operating implementation")
        require(assessment.get("result") in canonical_results,
                f"assessment {assessment_id} result invalid")
        require(assessment.get("state") in {"REVIEWED", "REOPENED", "CONFLICT_DETECTED"},
                f"assessment {assessment_id} state invalid")
        proposed = assessment.get("proposed_proof_level")
        require(proposed in proof_levels, f"assessment {assessment_id} proposed proof level invalid")
        if proposed in proof_levels:
            require(proof_levels[proposed] <= proof_levels["EVIDENCED"],
                    f"assessment {assessment_id} proposal must stay at or below EVIDENCED")
        require(assessment.get("assessor_actor_type") in {"AI", "HUMAN"},
                f"assessment {assessment_id} assessor actor invalid")
        require(clean_id(assessment.get("assessor_id")),
                f"assessment {assessment_id} requires assessor identity")
        version = assessment.get("assessment_version")
        require(isinstance(version, int) and not isinstance(version, bool) and version > 0,
                f"assessment {assessment_id} requires positive assessment version")
        materiality = assessment.get("materiality")
        required_class = assessment.get("required_review_class")
        require(materiality in materiality_min, f"assessment {assessment_id} materiality invalid")
        require(required_class in review_rank, f"assessment {assessment_id} review class invalid")
        if materiality in materiality_min and required_class in review_rank:
            require(review_rank[required_class] >= review_rank[materiality_min[materiality]],
                    f"assessment {assessment_id} review class below materiality minimum")
        if cid in controls and required_class in review_rank:
            canonical_min = controls[str(cid)].get("minimum_review_class")
            require(canonical_min in review_rank and review_rank[required_class] >= review_rank[canonical_min],
                    f"assessment {assessment_id} review class below control minimum")
        assessed_at = as_dt(assessment.get("assessed_at"))
        require(assessed_at is not None, f"assessment {assessment_id} assessed_at invalid")
        if assessed_at is not None:
            require(assessed_at.date() <= as_of, f"assessment {assessment_id} occurs after dossier as_of")
            assessment_times[assessment_id] = assessed_at
            declared_at = implementation_declared_times.get(str(impl_id))
            if declared_at is not None:
                require(assessed_at >= declared_at,
                        f"assessment {assessment_id} predates implementation declaration")
            app_reviewed = app_review_times.get(str(rid))
            if app_reviewed is not None:
                require(assessed_at >= app_reviewed,
                        f"assessment {assessment_id} predates applicability review")
            app_effective = app_effective_dates.get(str(rid))
            if app_effective is not None:
                require(assessed_at.date() >= app_effective,
                        f"assessment {assessment_id} predates applicability effective date")
            mapping_reviewed = mapping_review_times.get((str(rid), str(cid)))
            if mapping_reviewed is not None:
                require(assessed_at >= mapping_reviewed,
                        f"assessment {assessment_id} predates mapping review")
        evidence_ids = assessment.get("evidence_ids")
        require(isinstance(evidence_ids, list) and bool(evidence_ids),
                f"assessment {assessment_id} requires evidence")
        if isinstance(evidence_ids, list):
            for eid in evidence_ids:
                item = evidence.get(eid)
                require(item is not None, f"assessment {assessment_id} references unknown evidence {eid}")
                if item is not None:
                    require((str(impl_id), str(eid)) in linked_evidence,
                            f"assessment {assessment_id} evidence {eid} is not linked to implementation {impl_id}")
                    require(item.get("coverage_scope") == app.get("scope_id"),
                            f"assessment {assessment_id} evidence scope mismatch")
                    captured_at = evidence_capture_times.get(str(eid))
                    if captured_at is not None and assessed_at is not None:
                        require(captured_at <= assessed_at,
                                f"assessment {assessment_id} uses evidence captured after assessment")
                    evidence_users[str(eid)].add(assessment_id)
        if rid in requirements and cid in controls:
            assessments_by_pair.setdefault((str(rid), str(cid)), []).append(assessment)

    current_by_pair: dict[tuple[str, str], dict[str, Any]] = {}
    for pair, items in assessments_by_pair.items():
        versions = [item.get("assessment_version") for item in items]
        require(len(versions) == len(set(versions)),
                f"assessment history {pair[0]}->{pair[1]} requires unique versions")
        timestamps = [as_dt(item.get("assessed_at")) for item in items]
        require(None not in timestamps and len(timestamps) == len(set(timestamps)),
                f"assessment history {pair[0]}->{pair[1]} requires unique timestamps")
        ordered = sorted(
            items,
            key=lambda item: as_dt(item.get("assessed_at")) or datetime.min.replace(tzinfo=timezone.utc),
        )
        current_by_pair[pair] = ordered[-1]

    open_conflict_by_assessment: dict[str, list[dict[str, Any]]] = {aid: [] for aid in assessments}
    for conflict_id, conflict in conflicts.items():
        aid = conflict.get("assessment_id")
        assessment = assessments.get(str(aid))
        require(assessment is not None, f"conflict {conflict_id} references unknown assessment")
        ids = conflict.get("evidence_ids")
        require(isinstance(ids, list) and len(ids) >= 2,
                f"conflict {conflict_id} requires at least two evidence records")
        resolved = [evidence.get(eid) for eid in ids] if isinstance(ids, list) else []
        require(all(item is not None for item in resolved),
                f"conflict {conflict_id} references unknown evidence")
        if all(item is not None for item in resolved) and resolved:
            require(len({item.get("source_ref") for item in resolved}) >= 2,
                    f"conflict {conflict_id} requires distinct evidence sources")
            require(len({item.get("sha256") for item in resolved}) >= 2,
                    f"conflict {conflict_id} requires distinct evidence artifacts")
        require(conflict.get("status") == "OPEN",
                f"WP01 fixture models only unresolved OPEN conflicts")
        require(nonempty_string(conflict.get("rationale")),
                f"conflict {conflict_id} requires rationale")
        detected_at = as_dt(conflict.get("detected_at"))
        require(detected_at is not None, f"conflict {conflict_id} detected_at invalid")
        if assessment is not None:
            pair = (str(assessment.get("requirement_id")), str(assessment.get("control_id")))
            require(current_by_pair.get(pair, {}).get("assessment_id") == aid,
                    f"conflict {conflict_id} must bind to current assessment")
            require(assessment.get("state") == "CONFLICT_DETECTED",
                    f"open conflict {conflict_id} requires CONFLICT_DETECTED current assessment")
            assessed_at = assessment_times.get(str(aid))
            if detected_at is not None and assessed_at is not None:
                require(detected_at <= assessed_at,
                        f"conflict {conflict_id} detection must precede conflict assessment state")
            if isinstance(ids, list) and detected_at is not None:
                for eid in ids:
                    captured_at = evidence_capture_times.get(str(eid))
                    if captured_at is not None:
                        require(detected_at >= captured_at,
                                f"conflict {conflict_id} predates supporting evidence capture")
            open_conflict_by_assessment[str(aid)].append(conflict)

    reviews_by_assessment: dict[str, list[dict[str, Any]]] = {aid: [] for aid in assessments}
    for review_id, review in reviews.items():
        aid = review.get("assessment_id")
        assessment = assessments.get(str(aid))
        require(assessment is not None, f"review {review_id} references unknown assessment")
        require(review.get("reviewer_actor_type") == "HUMAN",
                f"review {review_id} requires human reviewer")
        actual_class = review.get("review_class")
        impl = implementations.get(str(assessment.get("implementation_id")), {}) if assessment is not None else {}
        authority_fields_ok(
            review_class=actual_class,
            independence_class=review.get("independence_class"),
            reviewer_id=review.get("reviewer_id"),
            review_rank=review_rank,
            errors=errors,
            label=f"review {review_id}",
            separated_from=[
                assessment.get("assessor_id") if assessment else None,
                impl.get("declared_by"),
                impl.get("owner_membership_id"),
            ],
            external_authority_ref=review.get("external_authority_ref"),
        )
        require(review.get("decision") == "ACCEPT", f"review {review_id} must be ACCEPT")
        reviewed_at = as_dt(review.get("reviewed_at"))
        require(reviewed_at is not None, f"review {review_id} reviewed_at invalid")
        if assessment is not None:
            pair = (str(assessment.get("requirement_id")), str(assessment.get("control_id")))
            require(current_by_pair.get(pair, {}).get("assessment_id") == aid,
                    f"review {review_id} must bind to current assessment")
            required_class = assessment.get("required_review_class")
            if actual_class in review_rank and required_class in review_rank:
                require(review_rank[actual_class] >= review_rank[required_class],
                        f"review {review_id} class below requirement")
            assessed_at = assessment_times.get(str(aid))
            if reviewed_at is not None and assessed_at is not None:
                require(reviewed_at >= assessed_at, f"review {review_id} predates assessment")
            for eid in assessment.get("evidence_ids", []):
                captured_at = evidence_capture_times.get(str(eid))
                if reviewed_at is not None and captured_at is not None:
                    require(captured_at <= reviewed_at,
                            f"review {review_id} relies on evidence captured after review")
                item = evidence.get(str(eid), {})
                if reviewed_at is not None:
                    require(evidence_valid(item, reviewed_at.date()),
                            f"review {review_id} relies on evidence outside its validity window: {eid}")
            reviews_by_assessment[str(aid)].append(review)

    decisions_by_assessment: dict[str, list[dict[str, Any]]] = {aid: [] for aid in assessments}
    for decision_id, decision in decisions.items():
        aid = decision.get("assessment_id")
        review_id = decision.get("review_id")
        assessment = assessments.get(str(aid))
        review = reviews.get(str(review_id))
        require(assessment is not None, f"decision {decision_id} references unknown assessment")
        require(review is not None and review.get("assessment_id") == aid,
                f"decision {decision_id} review/assessment mismatch")
        require(decision.get("assurance_state") == "VERIFIED",
                f"WP01 decision {decision_id} may demonstrate VERIFIED only")
        require(decision.get("authorized_actor_type") == "HUMAN",
                f"decision {decision_id} requires human authority")
        require(clean_id(decision.get("authorized_by")),
                f"decision {decision_id} requires clean authorizer identity")
        effective = as_dt(decision.get("effective_at"))
        require(effective is not None, f"decision {decision_id} effective_at invalid")
        if assessment is not None:
            pair = (str(assessment.get("requirement_id")), str(assessment.get("control_id")))
            require(current_by_pair.get(pair, {}).get("assessment_id") == aid,
                    f"decision {decision_id} must bind to current assessment")
            app = apps_by_req.get(str(assessment.get("requirement_id")), [{}])[0]
            require(app.get("status") == "APPLICABLE",
                    f"decision {decision_id} requires current APPLICABLE determination")
            require(assessment.get("state") == "REVIEWED",
                    f"decision {decision_id} requires REVIEWED current assessment")
            require(assessment.get("proposed_proof_level") == "EVIDENCED",
                    f"decision {decision_id} requires an EVIDENCED assessment proposal; human review performs VERIFIED promotion")
            require(not open_conflict_by_assessment.get(str(aid)),
                    f"decision {decision_id} blocked by open evidence conflict")
            for eid in assessment.get("evidence_ids", []):
                item = evidence.get(str(eid), {})
                require(evidence_valid(item, as_of),
                        f"decision {decision_id} relies on evidence not valid at as_of: {eid}")
            if review is not None and effective is not None:
                reviewed_at = as_dt(review.get("reviewed_at"))
                if reviewed_at is not None:
                    require(effective >= reviewed_at,
                            f"decision {decision_id} predates human review")
            decisions_by_assessment[str(aid)].append(decision)

    for pair, current in current_by_pair.items():
        evidence_ids = current.get("evidence_ids", []) if isinstance(current.get("evidence_ids"), list) else []
        any_valid = any(evidence_valid(evidence.get(str(eid), {}), as_of) for eid in evidence_ids)
        if not any_valid:
            require(current.get("state") == "REOPENED",
                    f"current assessment {current.get('assessment_id')} with expired evidence must be REOPENED")
            proposed = current.get("proposed_proof_level")
            if proposed in proof_levels:
                require(proof_levels[proposed] <= proof_levels["IMPLEMENTED"],
                        f"current assessment {current.get('assessment_id')} with expired evidence cannot remain green")
        require(len(decisions_by_assessment.get(str(current.get("assessment_id")), [])) <= 1,
                f"current assessment {current.get('assessment_id')} has multiple decisions")

    coverage: dict[str, str] = {}
    for rid in requirements:
        req_maps = maps_by_req.get(rid, [])
        if not req_maps:
            coverage[rid] = "GAP"
        elif any(item.get("coverage") == "FULL" for item in req_maps):
            coverage[rid] = "FULL"
        else:
            coverage[rid] = "PARTIAL"
    require(coverage == model.get("expected_coverage"),
            "derived coverage differs from expected_coverage")
    orphan_requirements = sorted(rid for rid in requirements if not maps_by_req.get(rid))
    orphan_controls = sorted(cid for cid in controls if not reqs_by_control.get(cid))
    require(orphan_requirements == sorted(model.get("expected_orphan_requirements", [])),
            "orphan requirement result drifted")
    require(orphan_controls == sorted(model.get("expected_orphan_controls", [])),
            "orphan control result drifted")
    shared_controls = {cid: sorted(rids) for cid, rids in reqs_by_control.items() if len(rids) > 1}
    shared_evidence = {eid: sorted(aids) for eid, aids in evidence_users.items() if len(aids) > 1}
    require(any(len({item.get("control_id") for item in maps_by_req.get(rid, [])}) > 1 for rid in requirements),
            "fixture must demonstrate one requirement mapped to multiple controls")
    require(bool(shared_controls), "fixture must demonstrate common-control reuse")
    require(bool(shared_evidence), "fixture must demonstrate evidence reuse")
    require(set(coverage.values()) == {"FULL", "PARTIAL", "GAP"},
            "fixture must demonstrate FULL/PARTIAL/GAP")

    return errors, {
        "as_of": as_of,
        "requirements": requirements,
        "maps_by_req": maps_by_req,
        "apps_by_req": apps_by_req,
        "implementations": implementations,
        "evidence": evidence,
        "assessments": assessments,
        "reviews": reviews,
        "current_by_pair": current_by_pair,
        "open_conflict_by_assessment": open_conflict_by_assessment,
        "decisions_by_assessment": decisions_by_assessment,
        "coverage": coverage,
        "orphan_requirements": orphan_requirements,
        "orphan_controls": orphan_controls,
        "shared_controls": shared_controls,
        "shared_evidence": shared_evidence,
    }


def assurance_state(requirement_id: str, derived: dict[str, Any]) -> str:
    app = derived["apps_by_req"][requirement_id][0]
    status = app.get("status")
    if status == "NOT_APPLICABLE":
        return "NOT_APPLICABLE"
    if status in {"UNDETERMINED", "PENDING_PROFESSIONAL_REVIEW"}:
        return str(status)
    coverage = derived["coverage"][requirement_id]
    if coverage == "GAP":
        return "GAP"
    pairs = [pair for pair in derived["current_by_pair"] if pair[0] == requirement_id]
    current = [derived["current_by_pair"][pair] for pair in sorted(pairs)]
    if any(derived["open_conflict_by_assessment"].get(item["assessment_id"]) for item in current):
        return "BLOCKED_CONFLICT"
    if any(item.get("state") == "REOPENED" for item in current):
        return "REOPENED"
    if any(not derived["decisions_by_assessment"].get(item["assessment_id"]) for item in current):
        return "PENDING_REVIEW"
    return "VERIFIED" if coverage == "FULL" else "PARTIAL_COVERAGE"


def current_results(requirement_id: str, derived: dict[str, Any]) -> str:
    pairs = [pair for pair in derived["current_by_pair"] if pair[0] == requirement_id]
    values = sorted({str(derived["current_by_pair"][pair].get("result")) for pair in pairs})
    return ", ".join(values) if values else "none"


def trace_lines(derived: dict[str, Any]) -> list[str]:
    lines: list[str] = []
    for pair in sorted(derived["current_by_pair"]):
        assessment = derived["current_by_pair"][pair]
        aid = str(assessment["assessment_id"])
        impl_id = str(assessment["implementation_id"])
        evidence_ids = ",".join(sorted(str(item) for item in assessment.get("evidence_ids", [])))
        linked_decisions = derived["decisions_by_assessment"].get(aid, [])
        if linked_decisions:
            decision = linked_decisions[0]
            review = derived["reviews"].get(str(decision.get("review_id")), {})
            review_text = f"{review.get('review_id')}[{review.get('review_class')}]"
            decision_text = str(decision.get("assurance_state"))
        else:
            review_text = "none"
            decision_text = "none"
        lines.append(
            f"- `{pair[0]} -> {pair[1]} -> {impl_id} -> [{evidence_ids}] -> "
            f"{aid}[result={assessment.get('result')},proposal={assessment.get('proposed_proof_level')}] -> "
            f"{review_text} -> {decision_text}`"
        )
    return lines


def render(model: dict[str, Any], derived: dict[str, Any]) -> str:
    lines = [
        "# SolidSecurity Synthetic Assurance Kernel Dossier",
        "",
        "Source: `model/assurance_kernel_v1.yaml`",
        "As-of: 2026-09-02",
        "Customer-facing: no; synthetic validation only.",
        "",
        "## Coverage",
        "",
        "| Requirement | Applicability | Coverage | Current result | Controls | Assurance state |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for rid in sorted(derived["requirements"]):
        app = derived["apps_by_req"][rid][0]
        controls = sorted({item["control_id"] for item in derived["maps_by_req"].get(rid, [])})
        lines.append(
            f"| {rid} | {app['applicability_id']}@{app['scope_id']}:{app['status']} | "
            f"{derived['coverage'][rid]} | {current_results(rid, derived)} | "
            f"{', '.join(controls) if controls else 'none'} | {assurance_state(rid, derived)} |"
        )
    history = sorted(
        aid
        for aid, item in derived["assessments"].items()
        if item.get("state") == "REOPENED"
        and derived["current_by_pair"].get((item.get("requirement_id"), item.get("control_id")), {}).get("assessment_id") != aid
    )
    lines.extend([
        "",
        "## Current trace paths",
        "",
        *trace_lines(derived),
        "",
        "## Kernel demonstrations",
        "",
        "- Multi-control obligation: `REQ-ACCESS-LIFECYCLE` -> `SS-ACCESS-002`, `SS-SUP-002`",
        "- Shared control reuse: `SS-SUP-002` -> `REQ-ACCESS-LIFECYCLE`, `REQ-SUPPLIER-GOV`",
        "- Shared evidence reuse: `EVID-GOV-REVIEW` is linked to and used by multiple assessment paths",
        f"- Orphan requirements: {', '.join(f'`{item}`' for item in derived['orphan_requirements'])}",
        f"- Orphan controls: {', '.join(f'`{item}`' for item in derived['orphan_controls'])}",
        "- Open conflict blocks promotion: `CONFLICT-SUPPLIER-01`",
        f"- Historical reopened assessment retained but not treated as current: {', '.join(f'`{item}`' for item in history)}",
        "- Current recovery assessment: `ASM-RECOVERY-V2` -> human review -> `VERIFIED` decision",
        "- Assessment proposals stop at `EVIDENCED`; only the attributable human decision performs `VERIFIED` promotion.",
        "- Canonical unresolved applicability statuses are accepted by the validator but cannot enter downstream assurance until `APPLICABLE`.",
        "",
        "This dossier is synthetic validation evidence. It is not a legal/compliance verdict, customer-facing VERIFIED claim, certification, independent assurance statement, or real-client assessment.",
        "",
    ])
    return "\n".join(lines)


def regressions(
    model: dict[str, Any],
    authorities: tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any], str],
) -> list[str]:
    failures: list[str] = []

    def expect_failure(mutator: Callable[[dict[str, Any]], None], needle: str) -> None:
        candidate = deepcopy(model)
        mutator(candidate)
        errors, _ = validate(candidate, *authorities)
        if not any(needle in error for error in errors):
            failures.append(f"regression did not fail closed: {needle}")

    def expect_success(mutator: Callable[[dict[str, Any]], None], check: Callable[[dict[str, Any]], bool], label: str) -> None:
        candidate = deepcopy(model)
        mutator(candidate)
        errors, derived = validate(candidate, *authorities)
        if errors or not check(derived):
            failures.append(f"regression did not preserve governed behavior: {label}; errors={errors}")

    base_errors, derived = validate(model, *authorities)
    if base_errors:
        failures.append("baseline fixture does not validate")
    else:
        if assurance_state("REQ-RECOVERY-TEST", derived) != "VERIFIED":
            failures.append("fresh recovery reassessment did not supersede historical REOPENED state")
        if not any(item.get("state") == "REOPENED" for item in derived["assessments"].values()):
            failures.append("fixture no longer preserves historical REOPENED assessment")

    expect_failure(lambda value: value["assessments"][0].update({"proposed_proof_level": "VERIFIED"}),
                   "proposal must stay at or below EVIDENCED")
    expect_failure(lambda value: value["applicability_decisions"][0].update({"reviewer_id": True}),
                   "requires clean reviewer identity")
    expect_failure(lambda value: value["decisions"][0].update({"authorized_actor_type": "AI"}),
                   "requires human authority")
    expect_failure(lambda value: value["evidence"][2].update({"expires_at": "2026-09-01"}),
                   "current assessment ASM-RECOVERY-V2 with expired evidence must be REOPENED")
    expect_failure(lambda value: value["evidence"][4].update({"source_ref": "synthetic_internal_governance_review"}),
                   "requires distinct evidence sources")
    expect_failure(lambda value: value["assessments"][0].update({"implementation_id": "IMP-GENERATED-POLICY"}),
                   "cannot promote generated policy")
    expect_failure(lambda value: value.update({"customer_facing": True}),
                   "synthetic kernel must not be customer-facing")
    expect_failure(lambda value: value["implementation_evidence_links"].pop(0),
                   "evidence EVID-ACCESS-RECERT is not linked to implementation IMP-ACCESS")
    expect_failure(lambda value: value["professional_reviews"][0].update({"reviewed_at": "2026-06-01T10:00:00Z"}),
                   "predates assessment")
    expect_failure(lambda value: value["evidence"][0].update({"captured_at": "2026-09-01T09:50:00Z"}),
                   "uses evidence captured after assessment")
    expect_failure(lambda value: value["requirement_control_maps"][0].update({"mapping_version": 0}),
                   "requires positive mapping version")
    expect_failure(lambda value: value["evidence"][0].update({"expires_at": "2028-12-31"}),
                   "validity window exceeds explicit kernel policy")

    def make_review_r3(value: dict[str, Any]) -> None:
        value["assessments"][0]["materiality"] = "high"
        value["assessments"][0]["required_review_class"] = "R3"
        value["professional_reviews"][0]["review_class"] = "R3"
    expect_failure(make_review_r3, "R3+ requires independent reviewer")

    def make_app_r3(value: dict[str, Any]) -> None:
        value["applicability_decisions"][0]["required_review_class"] = "R3"
        value["applicability_decisions"][0]["review_class"] = "R3"
    expect_failure(make_app_r3, "R3+ requires independent reviewer")

    def pending_orphan(value: dict[str, Any]) -> None:
        value["applicability_decisions"][3]["status"] = "PENDING_PROFESSIONAL_REVIEW"
    expect_success(
        pending_orphan,
        lambda d: assurance_state("REQ-ORPHAN-MONITORING", d) == "PENDING_PROFESSIONAL_REVIEW",
        "canonical pending applicability remains representable and fail-closed",
    )

    def not_applicable_orphan(value: dict[str, Any]) -> None:
        value["applicability_decisions"][3]["status"] = "NOT_APPLICABLE"
    expect_success(
        not_applicable_orphan,
        lambda d: assurance_state("REQ-ORPHAN-MONITORING", d) == "NOT_APPLICABLE",
        "canonical NOT_APPLICABLE remains representable and fail-closed",
    )

    try:
        yaml.load("a: 1\na: 2\n", Loader=UniqueKeyLoader)
        failures.append("duplicate YAML key regression did not fail closed")
    except ValueError:
        pass
    return failures


def main() -> int:
    try:
        model = load_yaml(MODEL_PATH)
        authorities = (
            load_yaml(CONTROLS_PATH),
            load_yaml(PROOF_PATH),
            load_yaml(AUTHORITY_PATH),
            load_yaml(ENUMS_PATH),
            M1_SCHEMA_PATH.read_text(encoding="utf-8"),
        )
        errors, derived = validate(model, *authorities)
    except Exception as exc:
        print("SOLIDSECURITY_ASSURANCE_KERNEL=FAIL")
        print(f"ERROR: {type(exc).__name__}: {exc}")
        return 2

    if errors:
        print("SOLIDSECURITY_ASSURANCE_KERNEL=FAIL")
        for error in errors:
            print(f"ERROR: {error}")
        return 2

    regression_errors = regressions(model, authorities)
    if regression_errors:
        print("SOLIDSECURITY_ASSURANCE_KERNEL=FAIL")
        for error in regression_errors:
            print(f"ERROR: {error}")
        return 2

    rendered = render(model, derived)
    if "--write-golden" in sys.argv:
        GOLDEN_PATH.write_text(rendered, encoding="utf-8")
    else:
        try:
            golden = GOLDEN_PATH.read_text(encoding="utf-8")
        except OSError:
            print("SOLIDSECURITY_ASSURANCE_KERNEL=FAIL")
            print("ERROR: deterministic dossier golden file missing")
            return 2
        if rendered != golden:
            print("SOLIDSECURITY_ASSURANCE_KERNEL=FAIL")
            print("ERROR: deterministic dossier rendering differs from committed golden output")
            return 2

    print("SOLIDSECURITY_ASSURANCE_KERNEL=PASS")
    print("coverage=" + ",".join(f"{rid}:{derived['coverage'][rid]}" for rid in sorted(derived["coverage"])))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
