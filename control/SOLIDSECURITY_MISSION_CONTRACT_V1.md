# SolidSecurity Mission Contract V1

Status: `MISSION CANDIDATE / CONTROL-MANAGED`
Governance work: issue #25
Canonical orchestration: `market-predictions/control-plane` Mission System V1

## Mission

SolidSecurity operates an **AI-enabled managed security and compliance service** for small and mid-sized organizations, initially with a strong focus on care organizations and compliance-exposed suppliers.

The customer outcome is:

> **Aantoonbaar in control, zonder een eigen complianceafdeling.**

SolidSecurity does the compliance work. The customer supplies organizational knowledge, evidence and decisions where those genuinely require the customer. Software and AI exist to make that managed service more consistent, affordable, scalable and auditable; they are not the mission themselves.

## Desired end state

A SolidSecurity professional can onboard and maintain many client organizations through one governed operating system in which:

- the operator sees the complete control/evidence/review reality;
- the client sees a simple, understandable status and only the actions/decisions relevant to them;
- AI prepares repetitive analytical and drafting work;
- professional review remains authoritative for material conclusions;
- every material statement is traceable to source and evidence;
- recurring compliance maintenance is cheaper and more dependable than traditional consultancy-heavy delivery.

## Product definition

SolidSecurity consists of three cooperating product surfaces.

### 1. Operator Workspace — primary working product

Used by SolidSecurity professionals to manage:

- organization/scope;
- common controls and client implementations;
- evidence and evidence versions;
- assessments and findings;
- client information requests;
- actions/remediation;
- AI proposals;
- professional review queues;
- approvals and reports;
- recurring review state.

### 2. Client Dashboard — simple customer cockpit

The customer must be able to understand quickly:

- where the organization stands;
- what is demonstrably arranged;
- what still needs attention;
- what SolidSecurity is currently doing;
- what SolidSecurity needs from the customer;
- which management decisions require approval;
- which reports/assurance artifacts are available.

The customer dashboard is outcome-centric and uses ordinary business language, not GRC/control jargon.

### 3. Interaction Layer — low-friction participation

The customer does not need to navigate the dashboard for every interaction. SolidSecurity can use:

- email;
- secure upload links;
- short targeted question forms;
- approval/sign-off links;
- meetings/calls captured into the dossier.

The customer may always return to the dashboard for the complete current picture.

## Canonical traceability

The following separation is non-negotiable:

`Source -> Requirement -> Control -> Customer Implementation -> Evidence -> Assessment -> Professional Review -> Decision / Assurance State`

Requirement, control, implementation, evidence, assessment and review are different objects. A policy draft is not implementation evidence. Strong evidence may prove a gap. AI output does not self-promote assurance state.

## Success criteria

### SS-SC-01 — Managed-service customer experience

The service can complete onboarding, baseline assessment, remediation planning and recurring maintenance without turning the customer into the operator of a GRC tool. Customer effort is limited to knowledge, evidence, approvals and decisions that cannot reasonably be performed by SolidSecurity.

### SS-SC-02 — Professional operator leverage

A SolidSecurity operator can manage the full client lifecycle from one coherent workspace, with repetitive extraction, mapping, request drafting, document drafting and reporting substantially AI-assisted while retaining provenance and review boundaries.

### SS-SC-03 — Clear client visibility

Every client can see a plain-language dashboard showing current status, outstanding actions, decisions, SolidSecurity work in progress, completed work and available reports without relying on a misleading single compliance percentage.

### SS-SC-04 — Evidence-based assurance

Material claims remain reproducible from authoritative evidence and professional review. The Proof Ladder and AI Authority Matrix remain enforced. SolidSecurity never represents itself as a certification body and never lets AI issue a final compliance/legal/certification verdict.

### SS-SC-05 — Simple secure client data plane

The normal runtime uses one shared multi-tenant PostgreSQL database, one private evidence-object store and a simple nightly encrypted off-site backup. Tenant isolation, evidence integrity and restore ability are proven. Additional infrastructure complexity requires a concrete risk, contract, scale or recovery-test justification.

### SS-SC-06 — Reusable common-control service model

One common-control backbone supports multiple external obligations/frameworks without maintaining duplicate static client checklists. Care and Supplier variants reuse the same underlying client/control/evidence model.

### SS-SC-07 — Mission-driven autonomous development

The canonical Control Mission System can reconstruct current authoritative project state, select the highest-priority eligible unsatisfied SolidSecurity mission gap, create a governed implementation intake, route it through Worker A / independent Worker B assurance and update mission state without relying on chat memory or principal relay.

### SS-SC-08 — Commercially viable quality

The service demonstrates that AI/software reduce repetitive professional effort while quality and assurance remain credible. Pricing, scope and automation are refined from measured delivery work rather than assumed efficiency.

## Guiding principles

### Customer outcome over software output

A feature is useful only when it reduces client burden, operator effort, risk or uncertainty, or improves demonstrable assurance.

### Managed service before self-service

Do not optimize for the customer completing long questionnaires or maintaining controls themselves. SolidSecurity owns the process and asks the customer only for necessary inputs and decisions.

### Evidence over declarations

A statement of implementation is not the same as objective evidence or professional verification.

### AI proposes; humans assure

AI may inventory, extract, map, draft, summarize and suggest. Material applicability, effectiveness, risk, evidence sufficiency, legal/compliance verdicts, exceptions and certification/assurance decisions remain governed human decisions.

### One common model; many obligations

Avoid separate NEN/ISO/Cbw/AVG/AI Act product silos when the same organizational control can satisfy multiple requirements.

### Simplest safe architecture first

Choose conventional shared infrastructure and commodity tooling until a concrete requirement proves the need for more. Security engineering is a risk-control activity, not an architecture-complexity contest.

### Convergence before canonicalization

When the service model is still uncertain, validate it through workflows and synthetic/controlled pilots before freezing large schemas, framework imports or platform abstractions. Once a recurring distinction is proven material, canonicalize it deliberately.

### Product quality over work-package completion

Closing an issue or producing a PR is never itself evidence that the mission advanced. Mission criteria are satisfied only by authoritative outcome evidence.

## Authority boundaries

This mission contract does not grant authority for:

- processing real client data before the real-client gate is explicitly passed;
- production deployment merely because code exists;
- autonomous final legal/compliance/certification verdicts;
- autonomous risk acceptance or statutory notification decisions;
- external certification claims;
- customer-environment write access or autonomous remediation;
- paid/provider/infrastructure expansion outside separately governed authority;
- storing client dossiers/evidence/secrets in the public GitHub control plane.

## Architecture contract

### Control plane

GitHub/Control stores product methodology, schemas, code, mission/roadmap state, public-safe controls, synthetic tests and governance. It does not store real client dossiers.

### Client data plane

Default runtime:

- one shared PostgreSQL database;
- `tenant_id` on tenant-owned records;
- server-side authorization plus RLS/equivalent defense in depth;
- one private object store for evidence/attachments;
- immutable reviewed evidence versions with hashes;
- provider encryption at rest and TLS;
- nightly encrypted off-site database + object backup using standard inexpensive tooling;
- periodic restore proof.

No database-per-client, custom KMS, active-active multi-cloud or real-time backup replication is a V1 default.

## Mission-driven development loop

The project-development loop is:

`Mission Contract -> current authoritative state -> highest-priority eligible mission gap -> PROJECT_INTAKE_V1 -> canonical DISPATCH_QUEUE -> Worker A implementation -> frozen candidate -> Worker B independent assurance -> governed integration -> authoritative mission-state update -> next gap`

The Control queue remains the only runtime work queue. SolidSecurity must not create a competing autonomous project scheduler.

## Gap-selection rule

Select work by the following order:

1. protects a hard authority/safety invariant;
2. removes a blocker to an end-to-end customer workflow;
3. reduces repeated operator/customer work materially;
4. improves evidence/assurance quality;
5. improves customer clarity;
6. improves scalability/automation;
7. infrastructure elegance only after one of the above requires it.

Among otherwise eligible gaps, use the canonical Control numeric priority and deterministic tie-breaking.

## Definition of done for mission gaps

A mission gap is not satisfied because documentation or code was created. It is satisfied only when its acceptance evidence demonstrates the relevant mission criterion and all required independent assurance/integration gates have completed.

## Terminal condition

The mission itself is intentionally long-lived. A revision becomes terminal when:

- all required success criteria for that revision are satisfied by authoritative evidence; or
- a later governed SolidSecurity mission revision explicitly supersedes it.
