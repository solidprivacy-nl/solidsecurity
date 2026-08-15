# Canonical Conceptual Data Model

## Design rule

The data model must make it impossible to treat a document, a customer statement or an AI inference as equivalent to verified implementation.

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

Key fields: `id`, `domain`, `title`, `objective`, `control_type`, `default_evidence_classes`, `review_class`.

### RequirementControlMapping

Many-to-many mapping between requirements and controls.

Key fields: `requirement_id`, `control_id`, `relationship`, `coverage`, `rationale`, `mapping_status`, `reviewed_by`, `reviewed_at`.

Mapping is evidence of analytical linkage, not proof of customer compliance.

## Client-plane entities (conceptual only in the public repo)

### ClientScope

The organization/entity/service/system perimeter being assessed.

### ApplicabilityDecision

Whether a requirement/control applies to a specific client scope and why.

### ImplementationClaim

How the client says a control operates.

Key fields: `control_id`, `client_scope_id`, `description`, `owner`, `status`, `declared_at`, `source_of_claim`.

### Evidence

A document, record, observation, interview result, export, screenshot, configuration result or independent artifact that supports or contradicts an implementation claim.

Key fields: `id`, `type`, `source`, `collected_at`, `valid_from`, `expires_at`, `integrity_ref`, `sensitivity`, `supports`, `contradicts`.

### Assessment

An analysis of one or more implementation claims and evidence items against a control/requirement.

Key fields: `assessor`, `actor_type`, `result`, `confidence`, `rationale`, `uncertainties`, `proposed_proof_level`, `created_at`.

AI may create assessments only as `PROPOSED` unless a policy explicitly allows a lower-risk automated state.

### Review

Accountable review of an assessment, mapping, exception or material artifact.

Key fields: `reviewer`, `independence_class`, `decision`, `comments`, `reviewed_at`.

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

## Relationships

```text
Source -> Framework -> Requirement
Requirement <-> Control
Control -> ImplementationClaim
ImplementationClaim <-> Evidence
Control + Claim + Evidence -> Assessment
Assessment -> Review -> Decision
Assessment -> Finding -> Action
Risk <-> Control
Vendor <-> Control / Evidence / Risk
AIUseCase <-> Vendor / Data / Control / Risk
```

## Provenance invariant

Every material record must preserve enough provenance to answer:

- who/what created it;
- based on which source or evidence;
- when;
- under which version;
- what was uncertain;
- who reviewed it;
- which state transition was authorized.
