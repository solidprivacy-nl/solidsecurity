# SolidSecurity Mission Contract R2

Status: `MISSION R2 / CANONICAL / CONTROL-MANAGED`  
Governance provenance: issue #31  
Supersedes: `SOLIDSECURITY_MISSION_CONTRACT_V1.md`  
Canonical development authority: current governed Control architecture and runtime in `market-predictions/control-plane`; Control implementation versions/topology are external live authority and are not duplicated in this Mission contract.

## Mission

SolidSecurity operates an **AI-enabled managed security and compliance service** that enables organizations to be demonstrably in control without building a full internal compliance function.

> **Aantoonbaar in control, zonder eigen complianceafdeling.**

SolidSecurity performs the compliance work. The customer supplies organizational knowledge, evidence, approvals and decisions where those genuinely require the customer. Software and AI exist to make professional delivery more consistent, affordable, scalable and auditable; they are not the mission themselves.

R2 changes what counts as progress: **design output is not market evidence, synthetic execution is not client evidence, and a technically complete product is not product-market validation.**

## Launch focus

### Primary launch learning track — Care

The first commercial learning track is Dutch healthcare. The initial ICP prioritizes care organizations with enough regulatory/contractual urgency, operational complexity and budget to value a maintained security/compliance function but without a proportionate internal CISO/compliance team. Roughly 50–250 FTE remains a commercial hypothesis, not a legal applicability rule.

Customer-facing regulatory positioning must be scoped accurately:

- direct Cyberbeveiligingswet/NIS2 applicability may be used only after an explicit applicability decision based on current authoritative criteria;
- outside direct Cbw scope, lead with obligations and pressures that actually apply, including NEN 7510/Wabvpz, privacy, IGJ expectations, contractual/customer requirements, supply-chain pressure and responsible AI governance where relevant;
- no segment message may imply that all small healthcare organizations are directly in Cbw/NIS2 scope.

### Secondary reuse/expansion track — Supplier

Supplier Assurance / Security & Compliance Passport remains strategically useful and synthetic Supplier work remains valid model evidence. It is not a second parallel zero-customer GTM program. Market evidence may later promote it.

## Product definition

1. **Operator Workspace** — primary professional working product;
2. **Client Dashboard** — simple customer cockpit;
3. **Interaction Layer** — low-friction evidence, question and approval participation.

The first real design-partner learning cycle does not require the complete future product surfaces. The minimum safe workflow may use bounded tooling as long as authoritative dossier, provenance and authority boundaries remain intact.

## Canonical traceability

`Source -> Requirement -> Control -> Customer Implementation -> Evidence -> Assessment -> Professional Review -> Decision / Assurance State`

Requirement, control, implementation, evidence, assessment, review and decision remain different objects. A generated policy is not implementation. Strong evidence may prove a gap. AI output never self-promotes to professional or independent assurance.

## Evidence hierarchy for mission claims

### E0 — Design evidence

Can prove design existence, internal consistency and deterministic constraints. Cannot prove customer usability, willingness-to-pay, actual workload, commercial viability or real-world assurance quality.

### E1 — Synthetic workflow evidence

**Synthetic workflow evidence** can prove model fit, structural traceability, expected workflow coverage and machine-checkable invariants. It cannot prove real customer behavior, evidence availability, acquisition, willingness-to-pay or achieved delivery economics.

### E2 — Controlled real-client workflow evidence

A bounded engagement under explicit data/security/contract authority can prove actual dossier friction, evidence availability, customer/reviewer burden, real workflow defects and measured delivery effort within scope.

### E3 — Market/commercial evidence

Qualified interviews, proposals, conversions, paid engagements, objections, loss reasons, channel performance and willingness-to-pay observations support ICP/positioning/channel/pricing hypotheses to the extent of the measured sample.

### E4 — Repeated operational evidence

Repeated governed real delivery can support scaling decisions, automation priorities and stronger commercial/economic claims.

**No lower evidence class may substitute for a success criterion that requires a higher class.**

## Professional trust model

Engineering/change assurance and customer-facing assurance are distinct trust domains.

### A. Product/change review

Consequential project changes require fresh evidence-first review bound to the exact candidate/head/base and applicable acceptance criteria. Candidate movement invalidates stale review. Central Control may perform fresh critical review and may call an external exact-candidate reviewer. External/organizationally independent review remains mandatory whenever the project workpackage, risk or current Control/repository gate requires it.

Project-change review does not qualify a person or system to issue customer-facing professional assurance.

### B. Customer-facing professional review

Every customer-facing review class must define minimum competence/experience, credential expectation where applicable, permitted decisions/claims, independence requirements, manageable capacity, loaded cost and escalation route.

### C. Independent external assurance/certification

Independent audit, certification and regulated professional opinions remain external where independence or formal recognition requires it. Internal professional review may not be presented as external independent assurance.

## Materiality

A matter is material when a reasonable error, omission, conflict or unsupported conclusion could meaningfully change at least one of:

- management risk acceptance or prioritization;
- a customer-facing assurance statement or label;
- regulatory/framework applicability;
- a statutory incident/notification decision;
- external audit/certification scope;
- significant security/privacy/continuity exposure;
- a contractual/tender/customer representation;
- a significant financial, operational, patient/client-safety or reputational decision.

Automation may not lower a required review class merely to reduce cost.

## Applicability and tailoring doctrine

Every material applicability/tailoring decision preserves scope facts, source/framework version, rule/rationale, uncertainty/exclusions, proposer, required review class, reviewer/decision where required, effective date and re-evaluation trigger/expiry.

AI may propose. Material legal/regulatory applicability remains a governed human decision.

## Evidence conflict and expiry doctrine

- contradictory material evidence creates `CONFLICT_DETECTED` rather than silent averaging/newest-wins;
- a material conflict blocks promotion beyond the last uncontested state until resolved or explicitly bounded;
- validity/expiry rules must be explicit where used;
- expiry downgrades or reopens affected assurance state rather than leaving stale green;
- conflict resolution preserves original evidence, rationale, reviewer and resulting transition.

## Success criteria

### SS-SC-01 — Managed-service customer experience

SolidSecurity can complete onboarding, baseline assessment, remediation planning and recurring maintenance without turning the customer into the operator of a GRC tool.

### SS-SC-02 — Professional operator leverage

A professional can manage the client lifecycle from one coherent operating system with AI assistance, provenance and review boundaries.

### SS-SC-03 — Clear client visibility

Clients can understand current state, what is demonstrably arranged, attention points, decisions/actions and reports without GRC/control-ID literacy and without a misleading single compliance percentage.

### SS-SC-04 — Evidence-based assurance

Material claims are reproducible across the full canonical traceability chain. Proof Ladder and AI Authority rules remain enforceable; generated policies cannot masquerade as operating implementation and AI cannot self-promote assurance state.

### SS-SC-05 — Simple secure client data plane

The normal runtime uses one shared tenant-aware PostgreSQL data plane, one private evidence store, immutable evidence versions/hashes and simple tested backup/restore. Tenant isolation and actual restore proof are required before real-client admission. Complexity requires evidence.

### SS-SC-06 — Reusable common-control service model

Multiple obligations reuse one common-control/evidence backbone without framework-specific duplicate client truth. A real mapping corpus demonstrates partial coverage, multi-control mappings, common-control/evidence reuse and coverage gaps.

### SS-SC-07 — Mission-driven autonomous development

Central Control can reconstruct authoritative state, select eligible mission gaps, execute the governed build/review/repair/integration-or-hold lifecycle and update canonical state without chat-memory or principal relay dependence. SolidSecurity does not require or own a particular Control worker topology to satisfy this criterion.

### SS-SC-08 — Bottom-up commercially viable quality

Pricing/package decisions treated as validated are based on measured workflow-step effort, cadence, reviewer class, loaded professional cost and observed automation/reuse outcomes. Top-down prices remain hypotheses until supported by evidence.

### SS-SC-09 — Real-world design-partner validation

At least one bounded real design-partner/client workflow is completed under explicit data, liability and authority gates before broad productization is treated as justified. E0/E1 cannot satisfy this criterion.

### SS-SC-10 — Professional trust and liability readiness

Before customer-facing `VERIFIED`, SolidSecurity has an explicit reviewer model, competence/independence/escalation path, capacity/cost model, contractual limits, liability/insurance posture, report-language limits, breach/incident posture and DPA/subprocessor boundaries.

### SS-SC-11 — Launch-market evidence

The primary launch ICP, positioning, competitor/alternative response and acquisition/channel plan progressively replace hypotheses with E3 evidence. The service has a concrete answer to the incumbent MSP/IT-provider alternative.

### SS-SC-12 — Governed IP/repository posture

Public/private material is deliberately separated before proprietary mappings, evidence-sufficiency logic, private prompts, GTM/economics or accumulated operating intelligence are published.

## Strategic defensibility doctrine

Crosswalks, mappings, prompts and base-model access are capabilities, not assumed durable moats. Expected defensibility compounds through trusted professional delivery, customer/channel relationships, accumulated governed history, evidence/assertion reuse, switching costs, measured remediation/evidence patterns, operational learning and software/AI leverage.

## Guiding principles

### Customer reality over internal completion
A PR, document, green CI run or synthetic dossier proves only the class of evidence it actually contains.

### Managed service before self-service
SolidSecurity owns the process and requests only necessary customer inputs/decisions.

### Evidence over declarations
Implementation claims, evidence and professional verification remain distinct.

### AI proposes; qualified humans assure
AI may extract, map, draft, compare and suggest. Material applicability, effectiveness, evidence sufficiency, risk acceptance, legal/compliance conclusions and customer-facing professional assurance remain governed human decisions.

### One common model; many obligations
Avoid framework silos and duplicated client truth.

### Simplest safe architecture first
Infrastructure complexity follows demonstrated risk/workflow/contract/scale needs.

### Real-world validation before broad productization
After the minimum executable/safe assurance kernel exists, obtain controlled real evidence before building broad product surfaces from synthetic assumptions.

### Risk-proportionate project governance
Mechanical checks should be deterministic. Consequential changes require fresh exact-candidate critical review; external/independent review is added when required by the project workpackage, material risk or current Control/repository gate rather than by a permanently duplicated local lane architecture.

## Authority boundaries

R2 does not grant authority for:

- real-client data before explicit real-client/design-partner authorization and security/data/contract/professional gates;
- production deployment merely because a runtime exists;
- autonomous final legal/compliance/certification/risk-acceptance/statutory-notification decisions;
- representing internal professional review as external independent assurance/certification;
- customer-environment write/remediation;
- publishing client dossiers/evidence/secrets in GitHub;
- publishing proprietary operating intelligence merely because the repository is public;
- treating a commercial hypothesis as validated without the required evidence class.

## Architecture contract

The lean data architecture remains:

- one shared PostgreSQL database;
- explicit tenant ownership on tenant data;
- server-side authorization plus RLS/equivalent defense in depth;
- one private object store for client evidence/attachments;
- immutable evidence versions/hashes;
- TLS/provider encryption at rest;
- simple encrypted off-site database + object backup;
- periodic actual restore proof.

No database-per-client, custom KMS or active-active multi-cloud is a default.

## Mission development boundary — central Control managed

SolidSecurity defines mission gaps, dependencies, evidence requirements and authority constraints. Central Control owns the current runtime implementation.

Conceptual lifecycle:

`Mission -> current central Control authority -> eligible bounded work -> implementation -> fresh exact-candidate review -> repair/re-review when needed -> governed integration or hold -> authoritative mission evidence -> next eligible gap`

Hard project rules:

- one central Control authority; no project-local queue/state plane;
- current Control protocol, lock model, scheduling and worker topology are read fresh and are not frozen into Mission R2;
- exact candidate/head/base and acceptance criteria remain bound through review;
- candidate movement invalidates stale review;
- deterministic validation is required where checks are mechanical;
- external/independent exact-candidate review remains required when an applicable project/Control gate says so;
- no direct project-worker bypass of canonical Control runtime state;
- no project-local intake/handover runtime plane;
- no provider fallback introduced by SolidSecurity;
- scheduler/chat invocation alone is never completion or assurance evidence;
- `principal_manual_relay_count=0` remains the target.

## R2 gap-selection rule

Select work by this order:

1. preserve hard authority/security/client-data invariants;
2. remove a blocker to safe real-world design-partner evidence;
3. establish professional trust/liability/applicability correctness;
4. make the assurance model executable/falsifiable;
5. reduce repeated operator/customer/reviewer effort observed in real delivery;
6. improve customer clarity/product surfaces;
7. automate/scale only after repeated evidence;
8. infrastructure elegance last.

## Definition of done

A mission gap is complete only when its specified exit evidence exists at the required evidence class and all applicable deterministic validation, exact-candidate project-change review, integration/hold and separately authorized authority gates are satisfied.

## Terminal condition

R2 is superseded when all required R2 criteria are supported by authoritative evidence or a later governed revision explicitly replaces it.
