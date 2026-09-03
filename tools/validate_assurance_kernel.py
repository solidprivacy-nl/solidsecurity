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
GOLDEN_PATH = ROOT / "spec/assurance_kernel_v1_dossier.md"
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
PROOF_LEVEL = {
    "UNKNOWN": 0,
    "DESIGNED": 1,
    "IMPLEMENTED": 2,
    "EVIDENCED": 3,
    "VERIFIED": 4,
    "INDEPENDENTLY_ASSURED": 5,
}
REVIEW_CLASS = {"R0": 0, "R1": 1, "R2": 2, "R3": 3, "R4": 4}


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


def _iso_date(value: object) -> str:
    parsed = _as_date(value)
    return parsed.isoformat() if parsed else "INVALID_DATE"


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


def validate_model(model: dict[str, Any]) -> tuple[list[str], dict[str, Any]]:
    errors: list[str] = []

    def require(condition: bool, message: str) -> None:
        if not condition:
            errors.append(message)

    require(model.get("version") == 1, "assurance kernel version must be 1")
    require(model.get("status") == "R2_WP01_CANDIDATE", "assurance kernel must remain an R2-WP01 candidate")
    require(model.get("mission_gap") == "SS-R2-GAP-01", "assurance kernel must remain bound to SS-R2-GAP-01")
    as_of = _as_date(model.get("as_of"))
    require(as_of is not None, "as_of must be a valid date")
    if as_of is None:
        as_of = date.min

    sources = _index(model.get("sources"), "source_id", errors)
    requirements = _index(model.get("requirements"), "requirement_id", errors)
    controls = _index(model.get("controls"), "control_id", errors)
    mappings = _index(model.get("requirement_control_maps"), "mapping_id", errors)
    applicability = _index(model.get("applicability_decisions"), "applicability_id", errors)
    implementations = _index(model.get("client_implementations"), "implementation_id", errors)
    evidence = _index(model.get("evidence"), "evidence_id", errors)
    assessments = _index(model.get("assessments"), "assessment_id", errors)
    reviews = _index(model.get("professional_reviews"), "review_id", errors)
    decisions = _index(model.get("decisions"), "decision_id", errors)
    ai_proposals = _index(model.get("ai_proposals"), "ai_proposal_id", errors)

    for requirement_id, requirement in requirements.items():
        source_id = requirement.get("source_id")
        require(source_id in sources, f"requirement {requirement_id} references unknown source")

    maps_by_requirement: dict[str, list[dict[str, Any]]] = {rid: [] for rid in requirements}
    requirements_by_control: dict[str, set[str]] = {cid: set() for cid in controls}
    for mapping_id, mapping in mappings.items():
        requirement_id = mapping.get("requirement_id")
        control_id = mapping.get("control_id")
        require(requirement_id in requirements, f"mapping {mapping_id} references unknown requirement")
        require(control_id in controls, f"mapping {mapping_id} references unknown control")
        require(mapping.get("coverage") in {"FULL", "PARTIAL"}, f"mapping {mapping_id} coverage must be FULL or PARTIAL")
        require(isinstance(mapping.get("rationale"), str) and bool(mapping.get("rationale")), f"mapping {mapping_id} requires rationale")
        if requirement_id in maps_by_requirement and control_id in controls:
            maps_by_requirement[requirement_id].append(mapping)
            requirements_by_control[control_id].add(requirement_id)

    applicability_by_requirement: dict[str, list[dict[str, Any]]] = {rid: [] for rid in requirements}
    for applicability_id, item in applicability.items():
        requirement_id = item.get("requirement_id")
        require(requirement_id in requirements, f"applicability {applicability_id} references unknown requirement")
        require(item.get("status") == "APPLICABLE", f"synthetic kernel applicability {applicability_id} must be APPLICABLE")
        if requirement_id in requirements:
            applicability_by_requirement[requirement_id].append(item)
            requirement = requirements[requirement_id]
            source = sources.get(requirement.get("source_id"), {})
            require(item.get("source_id") == requirement.get("source_id"), f"applicability {applicability_id} source provenance mismatch")
            require(item.get("source_version") == source.get("version"), f"applicability {applicability_id} source version mismatch")
        require(isinstance(item.get("rationale"), str) and bool(item.get("rationale")), f"applicability {applicability_id} requires rationale")
        require(bool(item.get("reviewed_by")) and bool(item.get("reviewed_at")), f"applicability {applicability_id} requires governed review provenance")
    for requirement_id, items in applicability_by_requirement.items():
        require(len(items) == 1, f"requirement {requirement_id} must have exactly one applicability decision")

    for implementation_id, implementation in implementations.items():
        require(implementation.get("control_id") in controls, f"implementation {implementation_id} references unknown control")
        if implementation.get("source_of_claim") == "generated_policy":
            require(implementation.get("implementation_status") == "DESIGNED", f"generated policy {implementation_id} must remain DESIGNED")

    for evidence_id, item in evidence.items():
        require(SHA256_RE.fullmatch(str(item.get("sha256", ""))) is not None, f"evidence {evidence_id} must have a lowercase SHA-256 digest")
        valid_from = _as_date(item.get("valid_from"))
        expires_at = _as_date(item.get("expires_at"))
        require(valid_from is not None and expires_at is not None, f"evidence {evidence_id} requires valid dates")
        if valid_from and expires_at:
            require(valid_from <= expires_at, f"evidence {evidence_id} validity window is inverted")

    assessments_by_requirement: dict[str, list[dict[str, Any]]] = {rid: [] for rid in requirements}
    assessment_evidence_users: dict[str, set[str]] = {eid: set() for eid in evidence}
    for assessment_id, assessment in assessments.items():
        requirement_id = assessment.get("requirement_id")
        control_id = assessment.get("control_id")
        implementation_id = assessment.get("implementation_id")
        require(requirement_id in requirements, f"assessment {assessment_id} references unknown requirement")
        require(control_id in controls, f"assessment {assessment_id} references unknown control")
        require(implementation_id in implementations, f"assessment {assessment_id} references unknown implementation")
        if implementation_id in implementations:
            require(implementations[implementation_id].get("control_id") == control_id, f"assessment {assessment_id} implementation/control mismatch")
        if requirement_id in requirements and control_id in controls:
            mapped_controls = {item.get("control_id") for item in maps_by_requirement.get(requirement_id, [])}
            require(control_id in mapped_controls, f"assessment {assessment_id} control is not mapped to its requirement")
            assessments_by_requirement[requirement_id].append(assessment)
        evidence_ids = assessment.get("evidence_ids")
        require(isinstance(evidence_ids, list) and len(evidence_ids) > 0, f"assessment {assessment_id} requires evidence")
        resolved_evidence: list[dict[str, Any]] = []
        if isinstance(evidence_ids, list):
            for evidence_id in evidence_ids:
                require(evidence_id in evidence, f"assessment {assessment_id} references unknown evidence {evidence_id}")
                if evidence_id in evidence:
                    resolved_evidence.append(evidence[evidence_id])
                    assessment_evidence_users[evidence_id].add(assessment_id)
        require(assessment.get("proposed_proof_level") in PROOF_LEVEL, f"assessment {assessment_id} has invalid proof level")
        review_class = assessment.get("required_review_class")
        require(review_class in REVIEW_CLASS, f"assessment {assessment_id} has invalid review class")
        if control_id in controls and controls[control_id].get("materiality") in {"high", "critical"}:
            require(REVIEW_CLASS.get(review_class, -1) >= REVIEW_CLASS["R2"], f"material assessment {assessment_id} must route to R2 or stronger review")
        if assessment.get("evidence_conflict") is True:
            require(assessment.get("state") == "CONFLICT_DETECTED", f"conflicted assessment {assessment_id} must remain CONFLICT_DETECTED")
        if resolved_evidence and all((_as_date(item.get("expires_at")) or date.min) < as_of for item in resolved_evidence):
            require(assessment.get("state") == "REOPENED", f"assessment {assessment_id} with only expired evidence must be REOPENED")
            proof = PROOF_LEVEL.get(assessment.get("proposed_proof_level"), 99)
            require(proof <= PROOF_LEVEL["IMPLEMENTED"], f"assessment {assessment_id} with only expired evidence cannot remain evidentially green")

    reviews_by_assessment: dict[str, list[dict[str, Any]]] = {aid: [] for aid in assessments}
    for review_id, review in reviews.items():
        assessment_id = review.get("assessment_id")
        require(assessment_id in assessments, f"professional review {review_id} references unknown assessment")
        require(review.get("reviewer_actor_type") == "HUMAN", f"professional review {review_id} requires human authority")
        if assessment_id in assessments:
            reviews_by_assessment[assessment_id].append(review)

    decisions_by_assessment: dict[str, list[dict[str, Any]]] = {aid: [] for aid in assessments}
    for decision_id, decision in decisions.items():
        assessment_id = decision.get("assessment_id")
        review_id = decision.get("review_id")
        state = decision.get("assurance_state")
        require(assessment_id in assessments, f"decision {decision_id} references unknown assessment")
        require(review_id in reviews, f"decision {decision_id} references unknown professional review")
        require(state in {"VERIFIED", "INDEPENDENTLY_ASSURED"}, f"decision {decision_id} has unsupported assurance state")
        require(decision.get("authorized_actor_type") == "HUMAN", f"{state} decision {decision_id} requires human authority")
        if assessment_id in assessments and review_id in reviews:
            assessment = assessments[assessment_id]
            review = reviews[review_id]
            require(review.get("assessment_id") == assessment_id, f"decision {decision_id} review/assessment mismatch")
            require(review.get("decision") == "ACCEPT", f"decision {decision_id} requires an accepted professional review")
            require(review.get("reviewer_actor_type") == "HUMAN", f"decision {decision_id} requires human professional review")
            require(assessment.get("evidence_conflict") is not True, f"conflicted assessment {assessment_id} cannot have assurance decision")
            require(assessment.get("state") == "REVIEWED", f"assurance decision {decision_id} requires REVIEWED assessment state")
            evidence_ids = assessment.get("evidence_ids", [])
            for evidence_id in evidence_ids if isinstance(evidence_ids, list) else []:
                expires_at = _as_date(evidence.get(evidence_id, {}).get("expires_at"))
                require(expires_at is not None and expires_at >= as_of, f"assurance decision {decision_id} relies on expired evidence")
            if state == "INDEPENDENTLY_ASSURED":
                require(review.get("independence_class") == "INDEPENDENT_EXTERNAL", f"decision {decision_id} requires independent external review")
            decisions_by_assessment[assessment_id].append(decision)

    for assessment_id, assessment in assessments.items():
        if assessment.get("evidence_conflict") is True:
            require(len(decisions_by_assessment.get(assessment_id, [])) == 0, f"conflicted assessment {assessment_id} must not be promoted")

    for proposal_id, proposal in ai_proposals.items():
        require(proposal.get("target_implementation_id") in implementations, f"AI proposal {proposal_id} references unknown implementation")
        require(proposal.get("authoritative") is False, f"AI proposal {proposal_id} must remain non-authoritative")
        require(proposal.get("proposed_proof_level") in PROOF_LEVEL, f"AI proposal {proposal_id} has invalid proof level")
        target = implementations.get(proposal.get("target_implementation_id"), {})
        if target.get("source_of_claim") == "generated_policy":
            require(PROOF_LEVEL.get(proposal.get("proposed_proof_level"), 99) <= PROOF_LEVEL["DESIGNED"], f"generated-policy AI proposal {proposal_id} cannot imply operating proof")

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
    expected_orphans = sorted(model.get("expected_orphans", [])) if isinstance(model.get("expected_orphans"), list) else []
    require(orphan_requirements == expected_orphans, "derived orphan requirements do not match expected_orphans")
    orphan_controls = sorted(cid for cid, requirement_ids in requirements_by_control.items() if not requirement_ids)

    multi_control_requirements = sorted(rid for rid, items in maps_by_requirement.items() if len({item.get("control_id") for item in items}) > 1)
    shared_controls = {
        cid: sorted(requirement_ids)
        for cid, requirement_ids in requirements_by_control.items()
        if len(requirement_ids) > 1
    }
    shared_evidence = {
        evidence_id: sorted(assessment_ids)
        for evidence_id, assessment_ids in assessment_evidence_users.items()
        if len(assessment_ids) > 1
    }
    require(bool(multi_control_requirements), "kernel must demonstrate one requirement mapped to multiple controls")
    require(bool(shared_controls), "kernel must demonstrate common-control reuse across requirements")
    require(bool(shared_evidence), "kernel must demonstrate evidence reuse across assessments")
    require(any(value == "FULL" for value in derived_coverage.values()), "kernel must demonstrate FULL coverage")
    require(any(value == "PARTIAL" for value in derived_coverage.values()), "kernel must demonstrate PARTIAL coverage")
    require(any(value == "GAP" for value in derived_coverage.values()), "kernel must demonstrate GAP coverage")

    derived = {
        "as_of": as_of,
        "sources": sources,
        "requirements": requirements,
        "controls": controls,
        "mappings": mappings,
        "maps_by_requirement": maps_by_requirement,
        "applicability_by_requirement": applicability_by_requirement,
        "implementations": implementations,
        "evidence": evidence,
        "assessments": assessments,
        "assessments_by_requirement": assessments_by_requirement,
        "reviews": reviews,
        "reviews_by_assessment": reviews_by_assessment,
        "decisions": decisions,
        "decisions_by_assessment": decisions_by_assessment,
        "coverage": derived_coverage,
        "orphan_requirements": orphan_requirements,
        "orphan_controls": orphan_controls,
        "multi_control_requirements": multi_control_requirements,
        "shared_controls": shared_controls,
        "shared_evidence": shared_evidence,
    }
    return errors, derived


def _assurance_state(requirement_id: str, derived: dict[str, Any]) -> str:
    if derived["coverage"].get(requirement_id) == "GAP":
        return "GAP"
    assessments = derived["assessments_by_requirement"].get(requirement_id, [])
    for assessment in assessments:
        decisions = derived["decisions_by_assessment"].get(assessment["assessment_id"], [])
        if decisions:
            return str(decisions[0]["assurance_state"])
    if any(item.get("state") == "CONFLICT_DETECTED" for item in assessments):
        return "BLOCKED_CONFLICT"
    if any(item.get("state") == "REOPENED" for item in assessments):
        return "REOPENED"
    return "PENDING_REVIEW"


def _trace(requirement_id: str, derived: dict[str, Any]) -> str:
    requirement = derived["requirements"][requirement_id]
    source_id = requirement["source_id"]
    if derived["coverage"][requirement_id] == "GAP":
        return f"{source_id} -> {requirement_id} -> GAP(no control mapping)"
    assessments = derived["assessments_by_requirement"].get(requirement_id, [])
    if not assessments:
        controls = sorted({item["control_id"] for item in derived["maps_by_requirement"].get(requirement_id, [])})
        return f"{source_id} -> {requirement_id} -> {','.join(controls)} -> PENDING_ASSESSMENT"
    assessment = sorted(assessments, key=lambda item: item["assessment_id"])[0]
    implementation = derived["implementations"][assessment["implementation_id"]]
    chain = [
        source_id,
        requirement_id,
        assessment["control_id"],
        implementation["implementation_id"],
        ",".join(sorted(assessment["evidence_ids"])),
        assessment["assessment_id"],
    ]
    reviews = derived["reviews_by_assessment"].get(assessment["assessment_id"], [])
    decisions = derived["decisions_by_assessment"].get(assessment["assessment_id"], [])
    if reviews:
        chain.append(sorted(reviews, key=lambda item: item["review_id"])[0]["review_id"])
    if decisions:
        decision = sorted(decisions, key=lambda item: item["decision_id"])[0]
        chain.extend([decision["decision_id"], decision["assurance_state"]])
    else:
        chain.append(str(assessment["state"]))
    return " -> ".join(chain)


def render_dossier(model: dict[str, Any], derived: dict[str, Any]) -> str:
    lines = [
        "# SolidSecurity Synthetic Assurance Kernel Dossier",
        "",
        "Source: `model/assurance_kernel_v1.yaml`",
        f"As-of: {_iso_date(model.get('as_of'))}",
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
        lines.append(
            f"| {requirement_id} | {applicability_text} | {derived['coverage'][requirement_id]} | {control_text} | {_assurance_state(requirement_id, derived)} |"
        )

    lines.extend(["", "## Traceability", ""])
    for requirement_id in sorted(derived["requirements"]):
        lines.append(f"- `{requirement_id}`: `{_trace(requirement_id, derived)}`")

    multi = derived["multi_control_requirements"]
    first_multi = multi[0] if multi else "none"
    first_multi_controls = sorted({item["control_id"] for item in derived["maps_by_requirement"].get(first_multi, [])}) if multi else []
    shared_control_lines = [f"`{cid}` -> {', '.join(f'`{rid}`' for rid in rids)}" for cid, rids in sorted(derived["shared_controls"].items())]
    shared_evidence_lines = [f"`{eid}` -> {', '.join(f'`{aid}`' for aid in aids)}" for eid, aids in sorted(derived["shared_evidence"].items())]
    conflict_ids = sorted(aid for aid, item in derived["assessments"].items() if item.get("state") == "CONFLICT_DETECTED")
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
        f"- Evidence conflicts: {', '.join(f'`{aid}`' for aid in conflict_ids) if conflict_ids else 'none'}",
        f"- Reopened after evidence expiry: {', '.join(f'`{aid}`' for aid in reopened_ids) if reopened_ids else 'none'}",
        f"- Generated-policy design-only implementations: {', '.join(f'`{iid}`' for iid in generated_ids) if generated_ids else 'none'}",
        "",
        "This dossier is synthetic validation evidence. It is not a legal/compliance verdict, certification, independent assurance statement, or real-client assessment.",
        "",
    ])
    return "\n".join(lines)


def _expect_regression_failure(base: dict[str, Any], mutate, expected: str, failures: list[str]) -> None:
    candidate = deepcopy(base)
    mutate(candidate)
    errors, _ = validate_model(candidate)
    if not any(expected in error for error in errors):
        failures.append(f"regression did not fail closed: {expected}")


def run_regressions(model: dict[str, Any]) -> list[str]:
    failures: list[str] = []

    _expect_regression_failure(
        model,
        lambda value: value["decisions"][0].update({"authorized_actor_type": "AI"}),
        "requires human authority",
        failures,
    )
    _expect_regression_failure(
        model,
        lambda value: value["evidence"][0].update({"expires_at": date(2026, 8, 31)}),
        "relies on expired evidence",
        failures,
    )

    def promote_conflict(value: dict[str, Any]) -> None:
        value["professional_reviews"].append({
            "review_id": "REV-SUPPLIER-BAD",
            "assessment_id": "ASM-SUPPLIER",
            "reviewer_id": "reviewer-02",
            "reviewer_actor_type": "HUMAN",
            "independence_class": "INTERNAL_QUALIFIED",
            "decision": "ACCEPT",
            "reviewed_at": "2026-09-01T11:00:00Z",
        })
        value["decisions"].append({
            "decision_id": "DEC-SUPPLIER-BAD",
            "assessment_id": "ASM-SUPPLIER",
            "review_id": "REV-SUPPLIER-BAD",
            "assurance_state": "VERIFIED",
            "authorized_by": "reviewer-02",
            "authorized_actor_type": "HUMAN",
            "effective_at": "2026-09-01T11:05:00Z",
        })

    _expect_regression_failure(model, promote_conflict, "cannot have assurance decision", failures)
    _expect_regression_failure(
        model,
        lambda value: value["expected_coverage"].update({"REQ-SUPPLIER-GOV": "FULL"}),
        "derived coverage does not match expected_coverage",
        failures,
    )
    _expect_regression_failure(
        model,
        lambda value: value["client_implementations"][-1].update({"implementation_status": "OPERATING"}),
        "must remain DESIGNED",
        failures,
    )
    return failures


def main() -> int:
    try:
        model = yaml.safe_load(MODEL_PATH.read_text(encoding="utf-8"))
    except Exception as exc:
        print("SOLIDSECURITY_ASSURANCE_KERNEL=FAIL")
        print(f"ERROR: assurance kernel model unreadable: {type(exc).__name__}")
        return 2
    if not isinstance(model, dict):
        print("SOLIDSECURITY_ASSURANCE_KERNEL=FAIL")
        print("ERROR: assurance kernel root must be a mapping")
        return 2

    errors, derived = validate_model(model)
    if errors:
        print("SOLIDSECURITY_ASSURANCE_KERNEL=FAIL")
        for error in errors:
            print(f"ERROR: {error}")
        return 2

    regressions = run_regressions(model)
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
    print(
        "coverage=" + ",".join(f"{key}:{derived['coverage'][key]}" for key in sorted(derived["coverage"]))
        + f" orphan_requirements={len(derived['orphan_requirements'])} shared_controls={len(derived['shared_controls'])} shared_evidence={len(derived['shared_evidence'])}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
