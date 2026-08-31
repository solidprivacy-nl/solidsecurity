# Canonical Conceptual Data Model

## Design rule

The data model must make it impossible to treat a document, customer statement, AI inference or scanner result as equivalent to verified implementation.

A second invariant is equally important after the synthetic pilots: **proof strength and control result are different dimensions**. Strong evidence may prove that a control is deficient.

## Foundation entities

### Source

Authoritative or reference material: law, regulatory guidance, framework, standard, sector guidance or approved internal source.

Key fields: `id`, `title`, `issuer`, `version`, `jurisdiction`, `url/reference`, `source_type`, `license_class`, `verified_at`.

### Framework

A named set of external requirements or assurance criteria, such as Cbw/NIS2, GDPR, NEN 7510, ISO 27001 or EU AI Act subsets.

### Requirement

An atomic external obligation/criterion.

Key fields: `id`, `framework_id`, `source_reference`, `summary`, `applicability_rule`, `effective_date`, `source_status`.

Important: store an internally authored summary/reference when redistribution rights for the full source text are restricted.

### Control

A reusable SolidSecurity control objective independent of any one framework.

Key fields: `id`, `domain`, `title`, `objective`, `control_type`, `default_evidence_classes`, `minimum_review_class`, `lifecycle_state`.

### ControlAssertion

A testable aspect beneath a stable control objective. Assertions prevent broad controls from collapsing multiple distinct operational questions into one ambiguous result.

Examples under access lifecycle: joiner approval, mover adjustment, leaver removal, periodic access recertification.

Key fields: `id`, `control_id`, `statement`, `expected_evidence_classes`, `materiality`, `lifecycle_state`.

### RequirementControlMapping

Many-to-many mapping between requirements and controls.

Key fields: `requirement_id`, `control_id`, `relationship`, `coverage`, `rationale`, `mapping_status`, `reviewed_by`, `reviewed_at`.

Mapping is evidence of analytical linkage, not proof of customer compliance.

## Client-plane entities (conceptual only in the public repo)

### ClientScope

The organization/entity/service/system perimeter being assessed.

### ApplicabilityDecision

Whether a requirement/control applies to a specific client scope and why.

Required state model:

- `APPLICABLE`
- `NOT_APPLICABLE`
- `UNDETERMINED`
- `PENDING_PROFESSIONAL_REVIEW`

A system may propose applicability, but material legal/regulatory applicability can remain unresolved until a qualified reviewer decides.

### ImplementationClaim

How the client says a control or assertion operates.

Key fields: `control_id/assertion_id`, `client_scope_id`, `description`, `owner`, `status`, `declared_at`, `source_of_claim`.

### Evidence

A document, record, observation, interview result, export, screenshot, configuration result or independent artifact that supports or contradicts an implementation claim.

Key fields:

- `id`, `type`, `source`, `collected_at`, `valid_from`, `expires_at`;
- `integrity_ref`, `sensitivity`;
- `supports`, `contradicts`;
- `coverage_scope`, `coverage_period`, `population`, `sample_basis`;
- `limitations`.

Coverage metadata is first-class: evidence for 90% of a population is not silently treated as evidence for 100%.

### Assessment

An analysis of one or more implementation claims and evidence items against a control/assertion/requirement.

Key fields: `assessor`, `actor_type`, `result`, `confidence`, `rationale`, `uncertainties`, `proposed_proof_level`, `created_at`.

`result` and `proposed_proof_level` are independent. Example: `result=GAP` with `proposed_proof_level=3` means there is evidence strong enough to demonstrate a deficiency.

AI may create assessments only as `PROPOSED` unless a future policy explicitly permits a lower-risk automated state.

### Review

Accountable review of an assessment, mapping, exception or material artifact.

Key fields: `reviewer`, `independence_class`, `decision`, `comments`, `reviewed_at`.

### ReviewQueueItem

A routing record for items that require human judgment because of materiality, uncertainty, conflict, legal interpretation, risk acceptance, customer-facing assurance or other policy triggers.

Key fields: `object_type`, `object_id`, `reason`, `priority`, `required_review_class`, `created_at`, `status`, `assigned_reviewer`.

### Decision

Governed state transition resulting from an authorized actor/review.

Examples: proof-level promotion, applicability approval, exception approval, risk acceptance.

### Finding

Gap, contradiction, missing evidence or control deficiency.

### Action

Remediation work with owner, due date, priority and verification criteria.

### Risk

Risk statement linked to assets/processes/controls, with inherent/current/target evaluation.

### Exception

Time-bounded authorized deviation from a control or expected state, including justification, compensating controls, owner and expiry.

### Vendor

Supplier/service-provider record, criticality and relevant security/privacy relationships.

### AIUseCase

AI system/use record including provider, purpose, data classes, user population, role, preliminary AI Act class, human oversight and review status.

### Artifact

Generated or approved customer-facing document/report/policy. Artifact status is separate from control implementation state.

### ApprovedAssertion

A reusable customer-facing statement/answer backed by a defined scope and evidence set. This supports the Supplier questionnaire/passport workflow.

Key fields:

- `id`, `canonical_wording`, `scope`;
- `linked_controls/assertions`;
- `evidence_ids`;
- `valid_from`, `expires_at`;
- `review_status`, `reviewer`;
- `allowed_uses`, `customer_specific_exclusions`;
- `assurance_labels`.

Semantic similarity may propose reuse but may not automatically authorize a customer-facing statement.

### AssuranceLabels

Independent dimensions for how a statement/status was established:

- `self_declared`
- `evidence_linked`
- `professionally_reviewed`
- `independently_audited`
- `certified`

These are not collapsed into one ambiguous green badge.

## Relationships

```text
Source -> Framework -> Requirement
Requirement <-> Control -> ControlAssertion
Control/Assertion -> ImplementationClaim
ImplementationClaim <-> Evidence
Control/Assertion + Claim + Evidence -> Assessment
Assessment -> ReviewQueueItem -> Review -> Decision
Assessment -> Finding -> Action
Risk <-> Control
Vendor <-> Control / Evidence / Risk
AIUseCase <-> Vendor / Data / Control / Risk
ApprovedAssertion -> Control/Assertion + Evidence + Review + AssuranceLabels
```

## Provenance invariant

Every material record must preserve enough provenance to answer:

- who/what created it;
- based on which source, claim or evidence;
- what scope/population/time period was covered;
- when;
- under which version;
- what was uncertain or excluded;
- who reviewed it;
- which state transition was authorized.
