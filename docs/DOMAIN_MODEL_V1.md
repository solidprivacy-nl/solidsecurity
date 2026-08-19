# SolidSecurity Domain Model V1

Status: **M1 candidate / schema contract only**  
Mission gap: `SS-GAP-01`  
Work contract: issue #28

## Purpose

Freeze the smallest relational model that can execute the accepted managed-service workflow before database migrations or UI code become canonical.

This is not a production migration. It is the contract future PostgreSQL migrations must implement or explicitly supersede.

## Non-negotiable separation

```text
Source -> Requirement -> Control -> ClientImplementation -> Evidence
       -> Assessment -> ProfessionalReview -> Decision / Assurance State
```

These concepts are separate records. A generated document is not implementation. Evidence can demonstrate a gap. An AI proposal is not a professional review or decision.

## Plane split

### Global catalog

Shared, public-safe methodology maintained once:

- `source`
- `framework`
- `requirement`
- `control`
- `control_assertion`
- `requirement_control_map`

These records have no customer truth and therefore no `tenant_id`.

### Identity root

`user_identity` is the authentication/principal root for either a human or a governed non-human service identity. `identity_type` distinguishes those cases. A `membership` joins that identity to one tenant and role.

One human may legitimately belong to more than one tenant. A service/agent identity may also receive a narrowly scoped `agent_service` membership. Authorization is derived from the authenticated identity plus the active membership, never from a client-supplied `tenant_id` alone. Non-human identities remain unable to exercise human-only review, approval or material-decision authority.

### Tenant dossier

Every customer-owned state record carries `tenant_id`, including:

- organization and organizational scope;
- engagement;
- applicability decisions;
- client control implementations;
- vendors and AI use cases;
- evidence and immutable evidence versions;
- implementation/evidence links;
- assessments and assessment/evidence links;
- findings and actions;
- client requests/responses;
- AI proposals;
- review queue, professional review, decision and approval;
- reports and approved assertions;
- approved-assertion links to controls/assertions and evidence versions;
- audit events;
- recurring/expiry review state.

## Core entities

### Tenant

Security boundary and customer dossier root. A tenant can contain one or more legal organizations/scopes without requiring a separate database.

### Organization / OrganizationalScope

`organization` represents a legal/operating entity. `organizational_scope` represents the bounded service/system/process perimeter being assessed. An engagement can cover one or more scopes.

### UserIdentity / Membership

`user_identity` stores an authenticated principal with `identity_type` (`human` or governed `service`). `membership` binds that principal to a tenant and bounded role. V1 roles are data, not separate schema families: `platform_admin`, `professional_reviewer`, `operations_contributor`, `client_admin`, `client_contributor`, `client_reader`, `agent_service`.

### Engagement

A SolidSecurity service relationship and variant (`baseline`, `care_managed`, `supplier_passport`, `audit_ready`). It anchors lifecycle state and reporting cadence without creating a separate schema per service product.

### Requirement / Control / ControlAssertion

Requirements are external obligations/criteria. Controls are reusable SolidSecurity objectives. Assertions are testable aspects under a stable control. `requirement_control_map` records analytical linkage only; it never proves client compliance.

### ApplicabilityDecision

Tenant/scope-specific applicability state for a requirement/control/assertion. Supports unresolved and professional-review states.

### ClientImplementation

How a control operates for a tenant/scope. This is distinct from evidence and from assessment.

### Evidence / EvidenceVersion

`evidence` is the logical artifact identity. `evidence_version` is an immutable captured version.

PostgreSQL stores metadata only:

- private object-store key;
- SHA-256;
- byte size/media type;
- source/capture actor/time;
- validity/expiry;
- coverage/population/sample/limitations;
- sensitivity.

Large file bytes are never stored in the relational row. A new upload creates a new version; reviewed historical versions are not overwritten.

### Assessment

Analysis against a control/assertion/implementation. Result and proof strength are separate dimensions. Assessments can reference multiple evidence versions through `assessment_evidence_link`.

### Finding / Action

A finding records a gap, contradiction or missing evidence. Actions are remediation/verification work and have ownership/due-state independently from the assessment.

### ClientRequest / ClientResponse

Targeted information/evidence/approval requests. They support low-friction email/link interactions while writing back to one authoritative dossier.

### AIProposal

Stores proposed analytical/drafting output with provenance metadata: model/provider identifier, policy version and input references. It is always non-authoritative. The record does not contain a capability to issue a human-only decision.

### ReviewQueueItem / ProfessionalReview / Decision / Approval

`review_queue_item` routes material judgment. `professional_review` records accountable human review. `decision` records a governed state transition. `approval` records explicit approval/sign-off when a separate approval event is required.

The separation prevents an AI assessment from becoming a professional decision merely because it is displayed in the same UI.

### Report / ApprovedAssertion

Reports are generated/approved output artifacts. Approved assertions are reusable customer-facing statements with scope, expiry, exact professional-review provenance, linked control/assertion provenance and exact evidence-version provenance.

`approved_assertion_control_link` binds a reusable statement to one control and optionally one subordinate assertion. `approved_assertion_evidence_link` binds it to exact evidence versions. This allows a Supplier Passport statement to be reconstructed as:

```text
ApprovedAssertion -> Control[/ControlAssertion] -> EvidenceVersion -> ProfessionalReview
```

Semantic similarity can propose a reusable assertion but cannot create either link or authorize customer-facing use by itself. The existence of a report or approved assertion never changes a client control implementation state.

### AuditEvent

Append-oriented metadata event: tenant, actor, action, object reference, timestamp and safe metadata. Raw evidence/document bodies and secrets are prohibited from event metadata.

### RecurringReview

Schedules expiry/periodic review for an object such as evidence, approved assertion, vendor or control implementation without creating duplicated copies of that object.

## Proven workflow additions

Two entities are included beyond the literal M1 minimum because synthetic Care/Supplier execution already demonstrated their distinct lifecycle:

- `vendor`
- `ai_use_case`

The approved-assertion control/evidence links are likewise retained because the Supplier candidate explicitly demonstrated questionnaire/passport reuse with provenance.

Risk/exception/asset enterprise families are **not frozen as separate V1 tables** here. They may be added only when the operator workflow proves a distinct persistent lifecycle that cannot be represented by findings/actions/decisions without loss.

## Tenant-isolation invariant

Every tenant-owned table contains a non-null `tenant_id`. Every relationship between tenant-owned rows must be same-tenant. The runtime must enforce this at the server authorization layer and with PostgreSQL RLS/equivalent defense in depth.

The schema contract intentionally does not encode a database-per-customer topology.

## Evidence integrity invariant

`evidence_version` is append-only from the application perspective after ingestion. Correction means a new version. A review or decision binds the exact version/hash it saw.

## AI authority invariant

AI may create `ai_proposal` and proposed `assessment` records. It cannot create an authoritative `professional_review`, risk/legal/compliance/certification decision, or independently assured state. Human/service authority is enforced outside prompt text and is represented explicitly in identity/membership/review/decision records.

## Deletion and retention

Tenant-owned objects carry lifecycle timestamps. Deletion/retention is policy/configuration driven; no universal legal duration is hard-coded. Audit and evidence version deletion must respect the separately governed retention/legal-hold design.

## Portability

The model assumes PostgreSQL capabilities but avoids Supabase-specific table names or Cloudflare-specific storage semantics. Auth provider subject and object-store key are adapter-facing fields.

## Exit check

M1 is complete only when:

1. `model/domain_model_v1.yaml` validates;
2. `spec/postgres_schema_contract_v1.sql` remains a non-migration contract consistent with this model;
3. both synthetic Care and Supplier coverage maps resolve against declared entities and exact candidate provenance;
4. B0 exact-head checks pass;
5. required independent B1 accepts the exact candidate before it is integrated/canonicalized.
