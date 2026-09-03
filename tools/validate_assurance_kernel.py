#!/usr/bin/env python3
"""Fail-closed validation and deterministic rendering for SolidSecurity R2-WP01."""
from __future__ import annotations

from copy import deepcopy
from datetime import date, datetime
from pathlib import Path
import re
import sys
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = ROOT / "model/assurance_kernel_v1.yaml"
CONTROL_CATALOG_PATH = ROOT / "model/sample_controls.yaml"
PROOF_LADDER_PATH = ROOT / "model/proof_ladder.yaml"
AI_AUTHORITY_PATH = ROOT / "model/ai_authority.yaml"
GOLDEN_PATH = ROOT / "spec/assurance_kernel_v1_dossier.md"
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


class _UniqueKeyLoader(yaml.SafeLoader):
    """Safe YAML loader that rejects duplicate mapping keys."""


def _construct_unique_mapping(loader: yaml.SafeLoader, node: yaml.nodes.MappingNode, deep: bool = False) -> dict[Any, Any]:
    mapping: dict[Any, Any] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in mapping:
            raise ValueError(f"duplicate YAML key: {key!r}")
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


_UniqueKeyLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _construct_unique_mapping)


def _load_yaml_text(text: str, label: str) -> dict[str, Any]:
    value = yaml.load(text, Loader=_UniqueKeyLoader)
    if not isinstance(value, dict):
        raise ValueError(f"{label} root must be a mapping")
    return value


def _load_yaml(path: Path) -> dict[str, Any]:
    return _load_yaml_text(path.read_text(encoding="utf-8"), path.name)


def _as_date(value: object) -> date | None:
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    if isinstance(value, str):
        try:
            return date.fromisoformat(value[:10])
        except ValueError:
            return None
    return None


def _as_datetime(value: object) -> datetime | None:
    if isinstance(value, datetime):
        parsed = value
    elif isinstance(value, str):
        try:
            parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError:
            return None
    else:
        return None
    return parsed if parsed.tzinfo is not None else None


def _evidence_valid_at(item: dict[str, Any], as_of: date) -> bool:
    valid_from = _as_date(item.get("valid_from"))
    expires_at = _as_date(item.get("expires_at"))
    return valid_from is not None and expires_at is not None and valid_from <= as_of <= expires_at


def _index(items: object, key: str, errors: list[str]) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    if not isinstance(items, list):
        errors.append(f"{key} collection must be a list")
        return result
    for item in items:
        if not isinstance(item, dict):
            errors.append(f"{key} collection contains non-object item")
            continue
        value = item.get(key)
        if not isinstance(value, str) or not value:
            errors.append(f"{key} must be a non-empty string")
            continue
        if value in result:
            errors.append(f"duplicate {key}: {value}")
            continue
        result[value] = item
    return result


def _string_list(value: object, label: str, errors: list[str], *, nonempty: bool = True) -> list[str]:
    if not isinstance(value, list):
        errors.append(f"{label} must be a list")
        return []
    result: list[str] = []
    for item in value:
        if not isinstance(item, str) or not item:
            errors.append(f"{label} entries must be non-empty strings")
            continue
        result.append(item)
    if nonempty and not result:
        errors.append(f"{label} must not be empty")
    if len(result) != len(set(result)):
        errors.append(f"{label} must not contain duplicates")
    return result


def _proof_levels(proof_ladder: dict[str, Any], errors: list[str]) -> dict[str, int]:
    result: dict[str, int] = {}
    states = proof_ladder.get("states")
    if not isinstance(states, list):
        errors.append("canonical proof ladder states must be a list")
        return result
    for state in states:
        if not isinstance(state, dict):
            errors.append("canonical proof ladder contains non-object state")
            continue
        state_id = state.get("id")
        level = state.get("level")
        if not isinstance(state_id, str) or not isinstance(level, int) or isinstance(level, bool):
            errors.append("canonical proof ladder state identity invalid")
            continue
        if state_id in result:
            errors.append(f"duplicate canonical proof state: {state_id}")
            continue
        result[state_id] = level
    required = {"UNKNOWN", "DESIGNED", "IMPLEMENTED", "EVIDENCED", "VERIFIED", "INDEPENDENTLY_ASSURED"}
    if not required.issubset(result):
        errors.append(f"canonical proof ladder missing states: {sorted(required - set(result))}")
    return result


def _review_classes(ai_authority: dict[str, Any], errors: list[str]) -> dict[str, int]:
    classes = ai_authority.get("review_classes")
    if not isinstance(classes, dict):
        errors.append("canonical AI authority review_classes must be a mapping")
        return {}
    result: dict[str, int] = {}
    for key in classes:
        if not isinstance(key, str) or re.fullmatch(r"R[0-9]+", key) is None:
            errors.append(f"canonical review class invalid: {key!r}")
            continue
        result[key] = int(key[1:])
    required = {"R0", "R1", "R2", "R3", "R4"}
    if not required.issubset(result):
        errors.append(f"canonical AI authority missing review classes: {sorted(required - set(result))}")
    return result


def validate_model(
    model: dict[str, Any],
    control_catalog: dict[str, Any],
    proof_ladder: dict[str, Any],
    ai_authority: dict[str, Any],
) -> tuple[list[str], dict[str, Any]]:
    errors: list[str] = []

    def require(condition: bool, message: str) -> None:
        if not condition:
            errors.append(message)

    proof_levels = _proof_levels(proof_ladder, errors)
    review_classes = _review_classes(ai_authority, errors)

    require(model.get("version") == 1, "assurance kernel version must be 1")
    require(model.get("status") == "R2_WP01_CANDIDATE", "assurance kernel must remain an R2-WP01 candidate")
    require(model.get("mission_gap") == "SS-R2-GAP-01", "assurance kernel must remain bound to SS-R2-GAP-01")
    require(model.get("semantic_projection_only") is True, "assurance kernel must remain an explicit semantic projection, not a persistence schema")
    as_of = _as_date(model.get("as_of"))
    require(as_of is not None, "as_of must be a valid date")
    if as_of is None:
        as_of = date.min

    sources = _index(model.get("sources"), "source_id", errors)
    scopes = _index(model.get("scopes"), "scope_id", errors)
    requirements = _index(model.get("requirements"), "requirement_id", errors)
    catalog_controls = _index(control_catalog.get("controls"), "id", errors)
    mappings = _index(model.get("requirement_control_maps"), "mapping_id", errors)
    applicability = _index(model.get("applicability_decisions"), "applicability_id", errors)
    implementations = _index(model.get("client_implementations"), "implementation_id", errors)
    validity_policies = _index(model.get("evidence_validity_policies"), "policy_id", errors)
    evidence = _index(model.get("evidence"), "evidence_id", errors)
    assessments = _index(model.get("assessments"), "assessment_id", errors)
    conflicts = _index(model.get("evidence_conflicts"), "conflict_id", errors)
    reviews = _index(model.get("professional_reviews"), "review_id", errors)
    decisions = _index(model.get("decisions"), "decision_id", errors)
    ai_proposals = _index(model.get("ai_proposals"), "ai_proposal_id", errors)

    scoped_ids = _string_list(model.get("control_scope"), "control_scope", errors)
    controls: dict[str, dict[str, Any]] = {}
    for control_id in scoped_ids:
        control = catalog_controls.get(control_id)
        require(control is not None, f"control_scope references unknown canonical control {control_id}")
        if control is None:
            continue
        require(control.get("lifecycle_state") == "active", f"scoped canonical control {control_id} must be active")
        require(control.get("minimum_review_class") in review_classes, f"canonical control {control_id} has invalid minimum_review_class")
        controls[control_id] = control

    for requirement_id, requirement in requirements.items():
        require(requirement.get("source_id") in sources, f"requirement {requirement_id} references unknown source")

    maps_by_requirement: dict[str, list[dict[str, Any]]] = {rid: [] for rid in requirements}
    requirements_by_control: dict[str, set[str]] = {cid: set() for cid in controls}
    for mapping_id, mapping in mappings.items():
        requirement_id = mapping.get("requirement_id")
        control_id = mapping.get("control_id")
        require(requirement_id in requirements, f"mapping {mapping_id} references unknown requirement")
        require(control_id in controls, f"mapping {mapping_id} references control outside canonical control_scope")
        require(mapping.get("coverage") in {"FULL", "PARTIAL"}, f"mapping {mapping_id} coverage must be FULL or PARTIAL")
        require(isinstance(mapping.get("rationale"), str) and bool(mapping.get("rationale")), f"mapping {mapping_id} requires rationale")
        if requirement_id in maps_by_requirement and control_id in controls:
            maps_by_requirement[requirement_id].append(mapping)
            requirements_by_control[control_id].add(requirement_id)

    applicability_by_requirement: dict[str, list[dict[str, Any]]] = {rid: [] for rid in requirements}
    for applicability_id, item in applicability.items():
        requirement_id = item.get("requirement_id")
        require(requirement_id in requirements, f"applicability {applicability_id} references unknown requirement")
        require(item.get("scope_id") in scopes, f"applicability {applicability_id} references unknown scope")
        require(bool(_string_list(item.get("scope_facts"), f"applicability {applicability_id} scope_facts", errors)), f"applicability {applicability_id} requires scope facts")
        require(bool(_string_list(item.get("uncertainty_or_exclusions"), f"applicability {applicability_id} uncertainty_or_exclusions", errors)), f"applicability {applicability_id} requires uncertainty/exclusion provenance")
        require(item.get("status") == "APPLICABLE", f"synthetic kernel applicability {applicability_id} must be APPLICABLE")
        if requirement_id in requirements:
            applicability_by_requirement[requirement_id].append(item)
            requirement = requirements[requirement_id]
            source = sources.get(requirement.get("source_id"), {})
            require(item.get("source_id") == requirement.get("source_id"), f"applicability {applicability_id} source provenance mismatch")
            require(item.get("source_framework_version") == source.get("version"), f"applicability {applicability_id} source framework version mismatch")
        require(isinstance(item.get("rationale"), str) and bool(item.get("rationale")), f"applicability {applicability_id} requires rationale")
        require(item.get("proposer_actor_type") in {"AI", "HUMAN"}, f"applicability {applicability_id} proposer actor type invalid")
        required_class = item.get("required_review_class")
        actual_class = item.get("review_class")
        require(required_class in review_classes, f"applicability {applicability_id} required review class invalid")
        require(actual_class in review_classes, f"applicability {applicability_id} actual review class invalid")
        if required_class in review_classes and "R2" in review_classes:
            require(review_classes[required_class] >= review_classes["R2"], f"applicability {applicability_id} material decision requires R2 or stronger review")
        if required_class in review_classes and actual_class in review_classes:
            require(review_classes[actual_class] >= review_classes[required_class], f"applicability {applicability_id} actual review class is below required review class")
        require(bool(item.get("reviewer_id")), f"applicability {applicability_id} requires reviewer identity")
        require(item.get("reviewer_actor_type") == "HUMAN", f"applicability {applicability_id} requires human review authority")
        require(item.get("review_decision") == "ACCEPT", f"applicability {applicability_id} requires explicit accepted review decision")
        reviewed_at = _as_datetime(item.get("reviewed_at"))
        effective = _as_date(item.get("effective_date"))
        expires = _as_date(item.get("expires_at"))
        require(reviewed_at is not None, f"applicability {applicability_id} reviewed_at must be a timezone-aware ISO timestamp")
        require(effective is not None and expires is not None and effective <= as_of <= expires, f"applicability {applicability_id} effective/expiry window invalid for as_of")
        if reviewed_at is not None and effective is not None:
            require(reviewed_at.date() <= effective, f"applicability {applicability_id} review must not occur after effective date")
        require(isinstance(item.get("reevaluation_trigger"), str) and bool(item.get("reevaluation_trigger")), f"applicability {applicability_id} requires reevaluation trigger")
    for requirement_id, items in applicability_by_requirement.items():
        require(len(items) == 1, f"requirement {requirement_id} must have exactly one applicability decision")

    for implementation_id, implementation in implementations.items():
        require(implementation.get("control_id") in controls, f"implementation {implementation_id} references control outside canonical control_scope")
        require(implementation.get("scope_id") in scopes, f"implementation {implementation_id} references unknown scope")
        if implementation.get("source_of_claim") == "generated_policy":
            require(implementation.get("implementation_status") == "DESIGNED", f"generated policy {implementation_id} must remain DESIGNED")

    for policy_id, policy in validity_policies.items():
        days = policy.get("max_validity_days")
        require(isinstance(days, int) and not isinstance(days, bool) and days > 0, f"evidence validity policy {policy_id} max_validity_days invalid")

    for evidence_id, item in evidence.items():
        require(SHA256_RE.fullmatch(str(item.get("sha256", ""))) is not None, f"evidence {evidence_id} must have a lowercase SHA-256 digest")
        require(isinstance(item.get("source_ref"), str) and bool(item.get("source_ref")), f"evidence {evidence_id} requires source provenance")
        require(item.get("captured_by_actor_type") in {"HUMAN", "SYSTEM"}, f"evidence {evidence_id} captured actor type invalid")
        require(bool(item.get("captured_by")), f"evidence {evidence_id} requires capture identity")
        captured_at = _as_datetime(item.get("captured_at"))
        require(captured_at is not None, f"evidence {evidence_id} captured_at must be a timezone-aware ISO timestamp")
        if captured_at is not None:
            require(captured_at.date() <= as_of, f"evidence {evidence_id} capture must not occur after dossier as_of")
        policy = validity_policies.get(item.get("validity_policy_id"))
        require(policy is not None, f"evidence {evidence_id} references unknown validity policy")
        valid_from = _as_date(item.get("valid_from"))
        expires_at = _as_date(item.get("expires_at"))
        require(valid_from is not None and expires_at is not None and valid_from <= expires_at, f"evidence {evidence_id} validity window invalid")
        if policy and valid_from and expires_at and isinstance(policy.get("max_validity_days"), int):
            require((expires_at - valid_from).days <= policy["max_validity_days"], f"evidence {evidence_id} validity window exceeds explicit policy")

    assessments_by_requirement: dict[str, list[dict[str, Any]]] = {rid: [] for rid in requirements}
    assessments_by_requirement_control: dict[tuple[str, str], list[dict[str, Any]]] = {}
    assessment_evidence_users: dict[str, set[str]] = {eid: set() for eid in evidence}
    for assessment_id, assessment in assessments.items():
        requirement_id = assessment.get("requirement_id")
        control_id = assessment.get("control_id")
        implementation_id = assessment.get("implementation_id")
        require(requirement_id in requirements, f"assessment {assessment_id} references unknown requirement")
        require(control_id in controls, f"assessment {assessment_id} references control outside canonical control_scope")
        require(implementation_id in implementations, f"assessment {assessment_id} references unknown implementation")
        require(isinstance(assessment.get("result"), str) and bool(assessment.get("result")), f"assessment {assessment_id} requires explicit result")
        if implementation_id in implementations:
            implementation = implementations[implementation_id]
            require(implementation.get("control_id") == control_id, f"assessment {assessment_id} implementation/control mismatch")
            apps = applicability_by_requirement.get(requirement_id, [])
            if len(apps) == 1:
                require(implementation.get("scope_id") == apps[0].get("scope_id"), f"assessment {assessment_id} implementation scope does not match requirement applicability scope")
        if requirement_id in requirements and control_id in controls:
            mapped_controls = {item.get("control_id") for item in maps_by_requirement.get(requirement_id, [])}
            require(control_id in mapped_controls, f"assessment {assessment_id} control is not mapped to its requirement")
            assessments_by_requirement[requirement_id].append(assessment)
            assessments_by_requirement_control.setdefault((requirement_id, control_id), []).append(assessment)

        evidence_ids = _string_list(assessment.get("evidence_ids"), f"assessment {assessment_id} evidence_ids", errors)
        resolved_evidence: list[dict[str, Any]] = []
        for evidence_id in evidence_ids:
            require(evidence_id in evidence, f"assessment {assessment_id} references unknown evidence {evidence_id}")
            if evidence_id in evidence:
                resolved_evidence.append(evidence[evidence_id])
                assessment_evidence_users[evidence_id].add(assessment_id)
        proof_level = assessment.get("proposed_proof_level")
        require(proof_level in proof_levels, f"assessment {assessment_id} has invalid proof level")
        require(assessment.get("state") in {"REVIEWED", "REOPENED", "CONFLICT_DETECTED"}, f"assessment {assessment_id} has invalid state")
        required_class = assessment.get("required_review_class")
        require(required_class in review_classes, f"assessment {assessment_id} has invalid review class")
        if control_id in controls:
            minimum_review = controls[control_id].get("minimum_review_class")
            if minimum_review in review_classes and required_class in review_classes:
                require(review_classes[required_class] >= review_classes[minimum_review], f"assessment {assessment_id} review class is below canonical control minimum")
        if resolved_evidence and not any(_evidence_valid_at(item, as_of) for item in resolved_evidence):
            require(assessment.get("state") == "REOPENED", f"assessment {assessment_id} with no evidence valid at as_of must be REOPENED")
            require(proof_levels.get(proof_level, 99) <= proof_levels.get("IMPLEMENTED", 2), f"assessment {assessment_id} with no evidence valid at as_of cannot remain evidentially green")

    for requirement_id, requirement_maps in maps_by_requirement.items():
        for control_id in {item.get("control_id") for item in requirement_maps if item.get("control_id") in controls}:
            require(bool(assessments_by_requirement_control.get((requirement_id, control_id))), f"mapped control {control_id} for requirement {requirement_id} lacks assessment trace")

    conflicts_by_assessment: dict[str, list[dict[str, Any]]] = {aid: [] for aid in assessments}
    open_conflicts_by_assessment: dict[str, list[dict[str, Any]]] = {aid: [] for aid in assessments}
    latest_resolution_by_assessment: dict[str, datetime] = {}
    for conflict_id, conflict in conflicts.items():
        assessment_id = conflict.get("assessment_id")
        require(assessment_id in assessments, f"conflict {conflict_id} references unknown assessment")
        conflict_evidence_ids = _string_list(conflict.get("evidence_ids"), f"conflict {conflict_id} evidence_ids", errors)
        require(len(conflict_evidence_ids) >= 2, f"conflict {conflict_id} requires at least two evidence records")
        if assessment_id in assessments:
            assessment_evidence_ids = set(_string_list(assessments[assessment_id].get("evidence_ids"), f"assessment {assessment_id} evidence_ids", errors))
            require(set(conflict_evidence_ids).issubset(assessment_evidence_ids), f"conflict {conflict_id} evidence must belong to its assessment")
        resolved_evidence = [evidence[eid] for eid in conflict_evidence_ids if eid in evidence]
        require(len(resolved_evidence) == len(conflict_evidence_ids), f"conflict {conflict_id} references unknown evidence")
        if len(resolved_evidence) >= 2:
            require(len({item.get("source_ref") for item in resolved_evidence}) >= 2, f"conflict {conflict_id} requires distinct evidence source provenance")
            require(len({item.get("sha256") for item in resolved_evidence}) >= 2, f"conflict {conflict_id} requires distinct evidence artifacts")
        require(isinstance(conflict.get("rationale"), str) and bool(conflict.get("rationale")), f"conflict {conflict_id} requires rationale")
        detected_at = _as_datetime(conflict.get("detected_at"))
        require(detected_at is not None, f"conflict {conflict_id} detected_at must be a timezone-aware ISO timestamp")
        if detected_at is not None:
            require(detected_at.date() <= as_of, f"conflict {conflict_id} detection must not occur after dossier as_of")
        status = conflict.get("status")
        require(status in {"OPEN", "RESOLVED"}, f"conflict {conflict_id} status invalid")
        if assessment_id in assessments:
            conflicts_by_assessment[assessment_id].append(conflict)
        if status == "OPEN":
            require(conflict.get("resolution") is None, f"open conflict {conflict_id} must not contain resolution")
            if assessment_id in assessments:
                require(assessments[assessment_id].get("state") == "CONFLICT_DETECTED", f"open conflict {conflict_id} requires CONFLICT_DETECTED assessment state")
                open_conflicts_by_assessment[assessment_id].append(conflict)
        elif status == "RESOLVED":
            resolution = conflict.get("resolution")
            require(isinstance(resolution, dict), f"resolved conflict {conflict_id} requires governed resolution")
            if isinstance(resolution, dict):
                require(isinstance(resolution.get("rationale"), str) and bool(resolution.get("rationale")), f"resolved conflict {conflict_id} requires resolution rationale")
                require(bool(resolution.get("reviewer_id")), f"resolved conflict {conflict_id} requires reviewer identity")
                require(resolution.get("reviewer_actor_type") == "HUMAN", f"resolved conflict {conflict_id} requires human reviewer")
                resolution_class = resolution.get("review_class")
                require(resolution_class in review_classes, f"resolved conflict {conflict_id} review class invalid")
                if assessment_id in assessments and resolution_class in review_classes:
                    required_class = assessments[assessment_id].get("required_review_class")
                    if required_class in review_classes:
                        require(review_classes[resolution_class] >= review_classes[required_class], f"resolved conflict {conflict_id} review class is below assessment requirement")
                resolved_at = _as_datetime(resolution.get("resolved_at"))
                require(resolved_at is not None, f"resolved conflict {conflict_id} resolved_at must be a timezone-aware ISO timestamp")
                if detected_at is not None and resolved_at is not None:
                    require(resolved_at >= detected_at, f"resolved conflict {conflict_id} resolution must not precede detection")
                    require(resolved_at.date() <= as_of, f"resolved conflict {conflict_id} resolution must not occur after dossier as_of")
                    if assessment_id in assessments:
                        previous = latest_resolution_by_assessment.get(assessment_id)
                        if previous is None or resolved_at > previous:
                            latest_resolution_by_assessment[assessment_id] = resolved_at
                transition = resolution.get("state_transition")
                require(transition in {"REVIEWED", "REOPENED"}, f"resolved conflict {conflict_id} state transition invalid")
                if assessment_id in assessments:
                    require(assessments[assessment_id].get("state") == transition, f"resolved conflict {conflict_id} assessment state does not match resolution")

    for assessment_id, assessment in assessments.items():
        if assessment.get("state") == "CONFLICT_DETECTED":
            require(bool(open_conflicts_by_assessment.get(assessment_id)), f"assessment {assessment_id} CONFLICT_DETECTED lacks open conflict record")

    reviews_by_assessment: dict[str, list[dict[str, Any]]] = {aid: [] for aid in assessments}
    review_times: dict[str, datetime] = {}
    for review_id, review in reviews.items():
        assessment_id = review.get("assessment_id")
        require(assessment_id in assessments, f"professional review {review_id} references unknown assessment")
        require(review.get("reviewer_actor_type") == "HUMAN", f"professional review {review_id} requires human authority")
        require(bool(review.get("reviewer_id")), f"professional review {review_id} requires reviewer identity")
        actual_class = review.get("review_class")
        require(actual_class in review_classes, f"professional review {review_id} actual review class invalid")
        require(review.get("independence_class") in {"INTERNAL_QUALIFIED", "INDEPENDENT_INTERNAL", "INDEPENDENT_EXTERNAL"}, f"professional review {review_id} independence class invalid")
        reviewed_at = _as_datetime(review.get("reviewed_at"))
        require(reviewed_at is not None, f"professional review {review_id} reviewed_at must be a timezone-aware ISO timestamp")
        if reviewed_at is not None:
            require(reviewed_at.date() <= as_of, f"professional review {review_id} must not occur after dossier as_of")
            review_times[review_id] = reviewed_at
        if assessment_id in assessments:
            required_class = assessments[assessment_id].get("required_review_class")
            if actual_class in review_classes and required_class in review_classes:
                require(review_classes[actual_class] >= review_classes[required_class], f"professional review {review_id} actual review class is below assessment requirement")
                if review_classes[actual_class] >= review_classes.get("R3", 3):
                    require(review.get("independence_class") != "INTERNAL_QUALIFIED", f"professional review {review_id} R3+ review requires independence")
                if review_classes[actual_class] >= review_classes.get("R4", 4):
                    require(review.get("independence_class") == "INDEPENDENT_EXTERNAL", f"professional review {review_id} R4 review requires external independence")
            reviews_by_assessment[assessment_id].append(review)

    decisions_by_assessment: dict[str, list[dict[str, Any]]] = {aid: [] for aid in assessments}
    for decision_id, decision in decisions.items():
        assessment_id = decision.get("assessment_id")
        review_id = decision.get("review_id")
        state = decision.get("assurance_state")
        require(state != "INDEPENDENTLY_ASSURED", f"decision {decision_id} INDEPENDENTLY_ASSURED is outside R2-WP01 authority")
        require(state == "VERIFIED", f"decision {decision_id} has unsupported assurance state")
        require(assessment_id in assessments, f"decision {decision_id} references unknown assessment")
        require(review_id in reviews, f"decision {decision_id} references unknown professional review")
        require(decision.get("authorized_actor_type") == "HUMAN", f"VERIFIED decision {decision_id} requires human authority")
        require(bool(decision.get("authorized_by")), f"decision {decision_id} requires attributable human authorization")
        effective_at = _as_datetime(decision.get("effective_at"))
        require(effective_at is not None, f"decision {decision_id} effective_at must be a timezone-aware ISO timestamp")
        if effective_at is not None:
            require(effective_at.date() <= as_of, f"decision {decision_id} must not occur after dossier as_of")
        if assessment_id in assessments and review_id in reviews:
            assessment = assessments[assessment_id]
            review = reviews[review_id]
            require(review.get("assessment_id") == assessment_id, f"decision {decision_id} review/assessment mismatch")
            require(review.get("decision") == "ACCEPT", f"decision {decision_id} requires an accepted professional review")
            require(review.get("reviewer_actor_type") == "HUMAN", f"decision {decision_id} requires human professional review")
            require(not open_conflicts_by_assessment.get(assessment_id), f"assessment {assessment_id} with open evidence conflict cannot have assurance decision")
            require(assessment.get("state") == "REVIEWED", f"assurance decision {decision_id} requires REVIEWED assessment state")
            review_time = review_times.get(review_id)
            if effective_at is not None and review_time is not None:
                require(effective_at >= review_time, f"decision {decision_id} must not precede its professional review")
            resolution_time = latest_resolution_by_assessment.get(assessment_id)
            if effective_at is not None and resolution_time is not None:
                require(effective_at >= resolution_time, f"decision {decision_id} must not precede latest conflict resolution")
            for evidence_id in _string_list(assessment.get("evidence_ids"), f"assessment {assessment_id} evidence_ids", errors):
                item = evidence.get(evidence_id, {})
                require(_evidence_valid_at(item, as_of), f"assurance decision {decision_id} relies on evidence {evidence_id} not valid at dossier as_of")
            decisions_by_assessment[assessment_id].append(decision)

    for assessment_id, assessment_decisions in decisions_by_assessment.items():
        require(len(assessment_decisions) <= 1, f"assessment {assessment_id} must have at most one current assurance decision")

    for proposal_id, proposal in ai_proposals.items():
        require(proposal.get("target_implementation_id") in implementations, f"AI proposal {proposal_id} references unknown implementation")
        require(proposal.get("authoritative") is False, f"AI proposal {proposal_id} must remain non-authoritative")
        proof_level = proposal.get("proposed_proof_level")
        require(proof_level in proof_levels, f"AI proposal {proposal_id} has invalid proof level")
        target = implementations.get(proposal.get("target_implementation_id"), {})
        if target.get("source_of_claim") == "generated_policy":
            require(proof_levels.get(proof_level, 99) <= proof_levels.get("DESIGNED", 1), f"generated-policy AI proposal {proposal_id} cannot imply operating proof")

    derived_coverage: dict[str, str] = {}
    for requirement_id in requirements:
        requirement_maps = maps_by_requirement.get(requirement_id, [])
        if not requirement_maps:
            derived_coverage[requirement_id] = "GAP"
        elif any(item.get("coverage") == "FULL" for item in requirement_maps):
            derived_coverage[requirement_id] = "FULL"
        else:
            derived_coverage[requirement_id] = "PARTIAL"
    expected_coverage = model.get("expected_coverage")
    require(isinstance(expected_coverage, dict), "expected_coverage must be a mapping")
    if isinstance(expected_coverage, dict):
        require(derived_coverage == expected_coverage, "derived coverage does not match expected_coverage")

    orphan_requirements = sorted(rid for rid, items in maps_by_requirement.items() if not items)
    expected_orphans = sorted(_string_list(model.get("expected_orphans"), "expected_orphans", errors))
    require(orphan_requirements == expected_orphans, "derived orphan requirements do not match expected_orphans")
    orphan_controls = sorted(cid for cid, requirement_ids in requirements_by_control.items() if not requirement_ids)
    expected_orphan_controls = sorted(_string_list(model.get("expected_orphan_controls"), "expected_orphan_controls", errors))
    require(orphan_controls == expected_orphan_controls, "derived orphan controls do not match expected_orphan_controls")

    multi_control_requirements = sorted(rid for rid, items in maps_by_requirement.items() if len({item.get("control_id") for item in items}) > 1)
    shared_controls = {cid: sorted(requirement_ids) for cid, requirement_ids in requirements_by_control.items() if len(requirement_ids) > 1}
    shared_evidence = {evidence_id: sorted(assessment_ids) for evidence_id, assessment_ids in assessment_evidence_users.items() if len(assessment_ids) > 1}
    require(bool(multi_control_requirements), "kernel must demonstrate one requirement mapped to multiple controls")
    require(bool(shared_controls), "kernel must demonstrate common-control reuse across requirements")
    require(bool(shared_evidence), "kernel must demonstrate evidence reuse across assessments")
    require(bool(orphan_requirements), "kernel must demonstrate orphan requirement detection")
    require(bool(orphan_controls), "kernel must demonstrate orphan control detection")
    require(any(value == "FULL" for value in derived_coverage.values()), "kernel must demonstrate FULL coverage")
    require(any(value == "PARTIAL" for value in derived_coverage.values()), "kernel must demonstrate PARTIAL coverage")
    require(any(value == "GAP" for value in derived_coverage.values()), "kernel must demonstrate GAP coverage")

    derived = {
        "as_of": as_of,
        "sources": sources,
        "scopes": scopes,
        "requirements": requirements,
        "controls": controls,
        "maps_by_requirement": maps_by_requirement,
        "implementations": implementations,
        "evidence": evidence,
        "assessments": assessments,
        "assessments_by_requirement": assessments_by_requirement,
        "assessments_by_requirement_control": assessments_by_requirement_control,
        "conflicts_by_assessment": conflicts_by_assessment,
        "open_conflicts_by_assessment": open_conflicts_by_assessment,
        "reviews": reviews,
        "reviews_by_assessment": reviews_by_assessment,
        "decisions_by_assessment": decisions_by_assessment,
        "applicability_by_requirement": applicability_by_requirement,
        "coverage": derived_coverage,
        "orphan_requirements": orphan_requirements,
        "orphan_controls": orphan_controls,
        "multi_control_requirements": multi_control_requirements,
        "shared_controls": shared_controls,
        "shared_evidence": shared_evidence,
    }
    return errors, derived


def _assurance_state(requirement_id: str, derived: dict[str, Any]) -> str:
    coverage = derived["coverage"].get(requirement_id)
    if coverage == "GAP":
        return "GAP"
    mapped_controls = {item["control_id"] for item in derived["maps_by_requirement"].get(requirement_id, [])}
    assessments = derived["assessments_by_requirement"].get(requirement_id, [])
    assessed_controls = {item["control_id"] for item in assessments}
    if mapped_controls - assessed_controls:
        return "PENDING_ASSESSMENT"
    if any(derived["open_conflicts_by_assessment"].get(item["assessment_id"]) for item in assessments):
        return "BLOCKED_CONFLICT"
    if any(item.get("state") == "REOPENED" for item in assessments):
        return "REOPENED"
    if any(item.get("state") != "REVIEWED" for item in assessments):
        return "PENDING_REVIEW"
    if any(not derived["decisions_by_assessment"].get(item["assessment_id"]) for item in assessments):
        return "PENDING_REVIEW"
    if coverage == "PARTIAL":
        return "PARTIAL_COVERAGE"
    return "VERIFIED"


def _traces(requirement_id: str, derived: dict[str, Any]) -> list[str]:
    requirement = derived["requirements"][requirement_id]
    source_id = requirement["source_id"]
    if derived["coverage"][requirement_id] == "GAP":
        return [f"{source_id} -> {requirement_id} -> GAP(no control mapping)"]

    traces: list[str] = []
    mapped_controls = sorted({item["control_id"] for item in derived["maps_by_requirement"].get(requirement_id, [])})
    for control_id in mapped_controls:
        assessments = sorted(derived["assessments_by_requirement_control"].get((requirement_id, control_id), []), key=lambda item: item["assessment_id"])
        if not assessments:
            traces.append(f"{source_id} -> {requirement_id} -> {control_id} -> PENDING_ASSESSMENT")
            continue
        for assessment in assessments:
            assessment_id = assessment["assessment_id"]
            implementation = derived["implementations"][assessment["implementation_id"]]
            chain = [source_id, requirement_id, control_id, implementation["implementation_id"], ",".join(sorted(assessment["evidence_ids"])), assessment_id, f"RESULT={assessment['result']}"]
            conflict_records = sorted(derived["conflicts_by_assessment"].get(assessment_id, []), key=lambda item: item["conflict_id"])
            if conflict_records:
                chain.append(",".join(f"{item['conflict_id']}:{item['status']}" for item in conflict_records))
            decisions = derived["decisions_by_assessment"].get(assessment_id, [])
            if decisions:
                decision = decisions[0]
                review = derived["reviews"].get(decision["review_id"])
                if review is not None:
                    chain.append(review["review_id"])
                chain.extend([decision["decision_id"], decision["assurance_state"]])
            elif not derived["open_conflicts_by_assessment"].get(assessment_id):
                review_ids = sorted(item["review_id"] for item in derived["reviews_by_assessment"].get(assessment_id, []))
                if review_ids:
                    chain.append(",".join(review_ids))
                chain.append(str(assessment["state"]))
            traces.append(" -> ".join(chain))
    return traces


def render_dossier(model: dict[str, Any], derived: dict[str, Any]) -> str:
    lines = [
        "# SolidSecurity Synthetic Assurance Kernel Dossier",
        "",
        "Source: `model/assurance_kernel_v1.yaml`",
        "Canonical control catalog: `model/sample_controls.yaml`",
        f"As-of: {(_as_date(model.get('as_of')) or date.min).isoformat()}",
        "Data class: synthetic only; no real client data.",
        "",
        "## Coverage",
        "",
        "| Requirement | Applicability | Coverage | Controls | Assurance state |",
        "| --- | --- | --- | --- | --- |",
    ]
    for requirement_id in sorted(derived["requirements"]):
        controls = sorted({item["control_id"] for item in derived["maps_by_requirement"].get(requirement_id, [])})
        control_text = ", ".join(controls) if controls else "none"
        applicability = derived["applicability_by_requirement"].get(requirement_id, [])
        applicability_text = applicability[0]["status"] if applicability else "MISSING"
        lines.append(f"| {requirement_id} | {applicability_text} | {derived['coverage'][requirement_id]} | {control_text} | {_assurance_state(requirement_id, derived)} |")

    lines.extend(["", "## Traceability", ""])
    for requirement_id in sorted(derived["requirements"]):
        for trace in _traces(requirement_id, derived):
            lines.append(f"- `{requirement_id}`: `{trace}`")

    multi = derived["multi_control_requirements"]
    first_multi = multi[0] if multi else "none"
    first_multi_controls = sorted({item["control_id"] for item in derived["maps_by_requirement"].get(first_multi, [])}) if multi else []
    shared_control_lines = [f"`{cid}` -> {', '.join(f'`{rid}`' for rid in rids)}" for cid, rids in sorted(derived["shared_controls"].items())]
    shared_evidence_lines = [f"`{eid}` -> {', '.join(f'`{aid}`' for aid in aids)}" for eid, aids in sorted(derived["shared_evidence"].items())]
    open_conflict_ids = sorted(item["conflict_id"] for items in derived["open_conflicts_by_assessment"].values() for item in items)
    reopened_ids = sorted(aid for aid, item in derived["assessments"].items() if item.get("state") == "REOPENED")
    generated_ids = sorted(iid for iid, item in derived["implementations"].items() if item.get("source_of_claim") == "generated_policy")

    lines.extend([
        "",
        "## Kernel demonstrations",
        "",
        f"- Multi-control obligation: `{first_multi}` -> {', '.join(f'`{cid}`' for cid in first_multi_controls) if first_multi_controls else 'none'}",
        f"- Shared control reuse: {'; '.join(shared_control_lines) if shared_control_lines else 'none'}",
        f"- Shared evidence reuse: {'; '.join(shared_evidence_lines) if shared_evidence_lines else 'none'}",
        f"- Orphan requirements: {', '.join(f'`{rid}`' for rid in derived['orphan_requirements']) if derived['orphan_requirements'] else 'none'}",
        f"- Orphan controls: {', '.join(f'`{cid}`' for cid in derived['orphan_controls']) if derived['orphan_controls'] else 'none'}",
        f"- Open evidence conflicts: {', '.join(f'`{cid}`' for cid in open_conflict_ids) if open_conflict_ids else 'none'}",
        f"- Reopened after evidence expiry: {', '.join(f'`{aid}`' for aid in reopened_ids) if reopened_ids else 'none'}",
        f"- Generated-policy design-only implementations: {', '.join(f'`{iid}`' for iid in generated_ids) if generated_ids else 'none'}",
        "",
        "This dossier is synthetic validation evidence. It is not a legal/compliance verdict, certification, independent assurance statement, or real-client assessment.",
        "",
    ])
    return "\n".join(lines)


def _expect_regression_failure(base: dict[str, Any], authorities: tuple[dict[str, Any], dict[str, Any], dict[str, Any]], mutate, expected: str, failures: list[str]) -> None:
    candidate = deepcopy(base)
    mutate(candidate)
    errors, _ = validate_model(candidate, *authorities)
    if not any(expected in error for error in errors):
        failures.append(f"regression did not fail closed: {expected}")


def run_regressions(model: dict[str, Any], authorities: tuple[dict[str, Any], dict[str, Any], dict[str, Any]]) -> list[str]:
    failures: list[str] = []

    def expect(mutate, expected: str) -> None:
        _expect_regression_failure(model, authorities, mutate, expected, failures)

    expect(lambda value: value["decisions"][0].update({"authorized_actor_type": "AI"}), "requires human authority")
    expect(lambda value: value["evidence"][0].update({"expires_at": date(2027, 12, 31)}), "validity window exceeds explicit policy")
    expect(lambda value: value["evidence"][0].update({"expires_at": date(2026, 8, 31)}), "not valid at dossier as_of")
    expect(lambda value: value["evidence"][0].update({"valid_from": date(2026, 10, 1), "expires_at": date(2026, 12, 31)}), "not valid at dossier as_of")
    expect(lambda value: value["evidence"][0].update({"captured_at": "2026-09-03T08:00:00Z"}), "capture must not occur after dossier as_of")
    expect(lambda value: value["professional_reviews"][0].update({"review_class": "R1"}), "actual review class is below assessment requirement")
    expect(lambda value: value["applicability_decisions"][0].update({"review_class": "R1"}), "actual review class is below required review class")
    expect(lambda value: value["applicability_decisions"][0].update({"review_decision": "REJECT"}), "requires explicit accepted review decision")
    expect(lambda value: value["applicability_decisions"][0].update({"reviewed_at": "not-a-timestamp"}), "reviewed_at must be a timezone-aware ISO timestamp")
    expect(lambda value: value["professional_reviews"][0].update({"reviewed_at": "not-a-timestamp"}), "reviewed_at must be a timezone-aware ISO timestamp")
    expect(lambda value: value["decisions"][0].update({"effective_at": "2026-09-01T09:59:00Z"}), "must not precede its professional review")
    expect(lambda value: value["decisions"][0].update({"effective_at": "2026-09-03T10:05:00Z"}), "must not occur after dossier as_of")

    def promote_conflict(value: dict[str, Any]) -> None:
        value["assessments"][-1]["state"] = "REVIEWED"
        value["professional_reviews"].append({"review_id": "REV-SUPPLIER-BAD", "assessment_id": "ASM-SUPPLIER", "reviewer_id": "reviewer-02", "reviewer_actor_type": "HUMAN", "review_class": "R2", "independence_class": "INTERNAL_QUALIFIED", "decision": "ACCEPT", "reviewed_at": "2026-09-01T11:00:00Z"})
        value["decisions"].append({"decision_id": "DEC-SUPPLIER-BAD", "assessment_id": "ASM-SUPPLIER", "review_id": "REV-SUPPLIER-BAD", "assurance_state": "VERIFIED", "authorized_by": "reviewer-02", "authorized_actor_type": "HUMAN", "effective_at": "2026-09-01T11:05:00Z"})

    expect(promote_conflict, "open evidence conflict cannot have assurance decision")
    expect(lambda value: value["evidence_conflicts"][0].update({"status": "RESOLVED"}), "requires governed resolution")
    expect(lambda value: value["evidence_conflicts"][0].update({"evidence_ids": ["EVID-GOV-REVIEW"]}), "requires at least two evidence records")
    expect(lambda value: value["evidence"][-1].update({"source_ref": "synthetic_internal_governance_review"}), "requires distinct evidence source provenance")
    expect(lambda value: value["expected_coverage"].update({"REQ-SUPPLIER-GOV": "FULL"}), "derived coverage does not match expected_coverage")
    expect(lambda value: value["client_implementations"][-1].update({"implementation_status": "OPERATING"}), "must remain DESIGNED")
    expect(lambda value: value["assessments"][0].update({"required_review_class": "R1"}), "below canonical control minimum")
    expect(lambda value: value["control_scope"].append("SS-NOT-A-CONTROL"), "references unknown canonical control")
    expect(lambda value: value["applicability_decisions"][0].update({"reviewer_actor_type": "AI"}), "requires human review authority")
    expect(lambda value: value["applicability_decisions"][0].pop("reevaluation_trigger"), "requires reevaluation trigger")
    expect(lambda value: value["decisions"][0].update({"assurance_state": "INDEPENDENTLY_ASSURED"}), "outside R2-WP01 authority")

    def cross_scope(value: dict[str, Any]) -> None:
        value["scopes"].append({"scope_id": "SCOPE-SYNTH-OTHER", "name": "Synthetic other scope"})
        value["client_implementations"][0]["scope_id"] = "SCOPE-SYNTH-OTHER"

    expect(cross_scope, "implementation scope does not match requirement applicability scope")

    def duplicate_decision(value: dict[str, Any]) -> None:
        extra = deepcopy(value["decisions"][0])
        extra["decision_id"] = "DEC-ACCESS-SECOND"
        extra["effective_at"] = "2026-09-01T10:07:00Z"
        value["decisions"].append(extra)

    expect(duplicate_decision, "must have at most one current assurance decision")

    def stale_recovery(value: dict[str, Any]) -> None:
        for assessment in value["assessments"]:
            if assessment["assessment_id"] == "ASM-RECOVERY":
                assessment["state"] = "REVIEWED"
                assessment["proposed_proof_level"] = "EVIDENCED"
                break

    expect(stale_recovery, "with no evidence valid at as_of must be REOPENED")

    aggregate = deepcopy(model)
    aggregate["assessments"][1]["evidence_ids"] = ["EVID-GOV-REVIEW", "EVID-SUPPLIER-ATTESTATION"]
    aggregate["assessments"][1]["state"] = "CONFLICT_DETECTED"
    aggregate["professional_reviews"] = [item for item in aggregate["professional_reviews"] if item["assessment_id"] != "ASM-ACCESS-SUPPLIER"]
    aggregate["decisions"] = [item for item in aggregate["decisions"] if item["assessment_id"] != "ASM-ACCESS-SUPPLIER"]
    aggregate["evidence_conflicts"].append({"conflict_id": "CONFLICT-ACCESS-SUPPLIER", "assessment_id": "ASM-ACCESS-SUPPLIER", "evidence_ids": ["EVID-GOV-REVIEW", "EVID-SUPPLIER-ATTESTATION"], "status": "OPEN", "rationale": "Synthetic aggregation blocker", "detected_at": "2026-09-01T11:00:00Z", "resolution": None})
    aggregate_errors, aggregate_derived = validate_model(aggregate, *authorities)
    if aggregate_errors or _assurance_state("REQ-ACCESS-LIFECYCLE", aggregate_derived) != "BLOCKED_CONFLICT":
        failures.append("requirement assurance aggregation did not preserve blocker across assessments")

    partial = deepcopy(model)
    partial["assessments"][-1]["state"] = "REVIEWED"
    partial["evidence_conflicts"][0] = {
        **partial["evidence_conflicts"][0],
        "status": "RESOLVED",
        "resolution": {"rationale": "Synthetic conflict resolved after evidence reconciliation", "reviewer_id": "reviewer-02", "reviewer_actor_type": "HUMAN", "review_class": "R2", "resolved_at": "2026-09-01T11:00:00Z", "state_transition": "REVIEWED"},
    }
    partial["professional_reviews"].append({"review_id": "REV-SUPPLIER", "assessment_id": "ASM-SUPPLIER", "reviewer_id": "reviewer-02", "reviewer_actor_type": "HUMAN", "review_class": "R2", "independence_class": "INTERNAL_QUALIFIED", "decision": "ACCEPT", "reviewed_at": "2026-09-01T11:05:00Z"})
    partial["decisions"].append({"decision_id": "DEC-SUPPLIER", "assessment_id": "ASM-SUPPLIER", "review_id": "REV-SUPPLIER", "assurance_state": "VERIFIED", "authorized_by": "reviewer-02", "authorized_actor_type": "HUMAN", "effective_at": "2026-09-01T11:10:00Z"})
    partial_errors, partial_derived = validate_model(partial, *authorities)
    if partial_errors or _assurance_state("REQ-SUPPLIER-GOV", partial_derived) != "PARTIAL_COVERAGE":
        failures.append("PARTIAL requirement coverage incorrectly became full VERIFIED assurance")

    bad_resolution = deepcopy(partial)
    bad_resolution["evidence_conflicts"][0]["resolution"]["resolved_at"] = "2026-09-01T09:00:00Z"
    bad_resolution_errors, _ = validate_model(bad_resolution, *authorities)
    if not any("resolution must not precede detection" in error for error in bad_resolution_errors):
        failures.append("conflict resolution chronology regression did not fail closed")

    early_decision = deepcopy(partial)
    early_decision["decisions"][-1]["effective_at"] = "2026-09-01T10:30:00Z"
    early_decision_errors, _ = validate_model(early_decision, *authorities)
    if not any("must not precede latest conflict resolution" in error for error in early_decision_errors):
        failures.append("post-conflict decision chronology regression did not fail closed")

    base_errors, base_derived = validate_model(model, *authorities)
    access_traces = _traces("REQ-ACCESS-LIFECYCLE", base_derived) if not base_errors else []
    if len(access_traces) != 2 or not all(marker in "\n".join(access_traces) for marker in ("ASM-ACCESS", "ASM-ACCESS-SUPPLIER", "RESULT=EFFECTIVE")):
        failures.append("multi-control requirement trace does not render every assessment path and result")

    linked_review = deepcopy(model)
    linked_review["professional_reviews"].append({"review_id": "AAA-NON-AUTHORITATIVE", "assessment_id": "ASM-ACCESS", "reviewer_id": "reviewer-03", "reviewer_actor_type": "HUMAN", "review_class": "R2", "independence_class": "INTERNAL_QUALIFIED", "decision": "REJECT", "reviewed_at": "2026-09-01T09:55:00Z"})
    linked_errors, linked_derived = validate_model(linked_review, *authorities)
    linked_traces = _traces("REQ-ACCESS-LIFECYCLE", linked_derived) if not linked_errors else []
    first_trace = next((trace for trace in linked_traces if "ASM-ACCESS ->" in trace), "")
    if "REV-ACCESS -> DEC-ACCESS" not in first_trace or "AAA-NON-AUTHORITATIVE" in first_trace:
        failures.append("trace did not use the professional review referenced by the assurance decision")

    try:
        _load_yaml_text("a: 1\na: 2\n", "duplicate-key-regression")
        failures.append("duplicate YAML key regression did not fail closed")
    except ValueError as exc:
        if "duplicate YAML key" not in str(exc):
            failures.append("duplicate YAML key regression failed for the wrong reason")

    return failures


def main() -> int:
    try:
        model = _load_yaml(MODEL_PATH)
        authorities = (_load_yaml(CONTROL_CATALOG_PATH), _load_yaml(PROOF_LADDER_PATH), _load_yaml(AI_AUTHORITY_PATH))
        errors, derived = validate_model(model, *authorities)
    except Exception as exc:
        print("SOLIDSECURITY_ASSURANCE_KERNEL=FAIL")
        print(f"ERROR: assurance kernel validation exception: {type(exc).__name__}: {exc}")
        return 2

    if errors:
        print("SOLIDSECURITY_ASSURANCE_KERNEL=FAIL")
        for error in errors:
            print(f"ERROR: {error}")
        return 2

    regressions = run_regressions(model, authorities)
    if regressions:
        print("SOLIDSECURITY_ASSURANCE_KERNEL=FAIL")
        for error in regressions:
            print(f"ERROR: {error}")
        return 2

    rendered = render_dossier(model, derived)
    if "--write-golden" in sys.argv:
        GOLDEN_PATH.parent.mkdir(parents=True, exist_ok=True)
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
            print("ERROR: synthetic dossier rendering differs from committed golden output")
            return 2

    print("SOLIDSECURITY_ASSURANCE_KERNEL=PASS")
    print("coverage=" + ",".join(f"{key}:{derived['coverage'][key]}" for key in sorted(derived["coverage"])) + f" orphan_requirements={len(derived['orphan_requirements'])} orphan_controls={len(derived['orphan_controls'])} shared_controls={len(derived['shared_controls'])} shared_evidence={len(derived['shared_evidence'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())