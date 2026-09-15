# SolidSecurity Domain Model V1

Status: **M1 canonical / schema contract only**  
Historical mission gap provenance: `SS-GAP-01`

## Purpose

Define the smallest relational model required by the accepted managed-service workflow before real database migrations or UI implementation. M1 is canonical as a **contract**; it is not a production migration and does not authorize real-client processing.

Machine-readable authority: `model/domain_model_v1.yaml`  
Non-migration PostgreSQL contract: `spec/postgres_schema_contract_v1.sql`

## Non-negotiable traceability

`Source -> Requirement -> Control -> ClientImplementation -> Evidence -> Assessment -> ProfessionalReview -> Decision / Assurance State`

These concepts are separate records. A generated document is not implementation. Evidence may prove a gap. An AI proposal is not a professional review or decision.

## Plane split

### Global public-safe catalog

Shared methodology maintained once:

- Source / Framework / Requirement;
- Control / ControlAssertion;
- RequirementControlMap.

These contain no customer truth and therefore are not tenant-owned.

### Identity root

`UserIdentity` supports both human and governed service identities. `Membership` joins an identity to one tenant/role. Authorization derives from authenticated identity plus active membership, never a client-supplied `tenant_id` alone.

Service identities cannot acquire human-only professional review, approval or material-decision authority.

### Tenant dossier

Tenant-owned state includes organization/scope/engagement, applicability decisions, client implementations, vendors/AI use cases, evidence/evidence versions, assessments, findings/actions, client requests/responses, AI proposals, professional reviews/decisions/approvals, reports, approved assertions and recurring reviews.

Every tenant-owned entity carries `tenant_id`.

## Evidence model

`Evidence` identifies the logical evidence object. `EvidenceVersion` identifies immutable ingested content/observation state and carries at minimum:

- tenant/evidence identity;
- object locator;
- SHA-256;
- size/media type;
- source/actor/timestamp;
- validity/expiry;
- coverage and limitations;
- sensitivity.

A reviewed version is never silently overwritten. New content creates a new version.

## AI / professional authority

`AIProposal` is explicitly non-authoritative. Material professional review and decision objects require human authority according to the applicable review class. Proof Ladder/AI Authority rules remain separate policy enforcement and may not be bypassed by database state.

## Approved assertion provenance

Approved reusable assertions bind to the exact professional review and to the controls/assertions/evidence versions they represent. Reviewer identity derives from the professional review rather than being duplicated as a second source of truth.

## Runtime topology contract

The designed normal topology is:

- one shared PostgreSQL relational store;
- tenant boundary = `tenant_id`;
- one private shared evidence object store;
- evidence bytes outside PostgreSQL;
- server authorization + RLS/equivalent defense in depth;
- no database-per-client registry/default.

The SQL file is intentionally a contract and states `NOT A MIGRATION`.

## Deliberately prohibited V1 shortcuts

- per-framework client checklist as duplicate truth;
- AI final compliance verdict table;
- evidence blob bytes in PostgreSQL;
- database-per-customer registry as default architecture;
- autonomous risk acceptance.

## Synthetic coverage provenance

The existing Care/Supplier synthetic candidates remain useful non-authoritative workflow evidence. Their exact candidate provenance is retained in `spec/m1_workflow_coverage.yaml`; they do not become real-client or integrated operational evidence merely because M1 itself is canonical.

## Change rule

Future migrations/runtime code must implement this contract or explicitly supersede it through governed change. Do not fork a second model for individual frameworks/customers unless real evidence proves the common model insufficient.
