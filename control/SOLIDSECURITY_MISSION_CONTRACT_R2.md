# SolidSecurity Mission Contract R2

Status: `MISSION R2 / CANDIDATE / CONTROL-MANAGED`  
Governance work: issue #31  
Supersedes on integration: `SOLIDSECURITY_MISSION_CONTRACT_V1.md`  
Canonical orchestration target: `market-predictions/control-plane` Mission System

## Mission

SolidSecurity operates an **AI-enabled managed security and compliance service** that enables organizations to be demonstrably in control without building a full internal compliance function.

The customer outcome remains:

> **Aantoonbaar in control, zonder eigen complianceafdeling.**

SolidSecurity performs the compliance work. The customer supplies organizational knowledge, evidence, approvals and decisions where those genuinely require the customer. Software and AI exist to make professional delivery more consistent, affordable, scalable and auditable; they are not the mission themselves.

R2 changes what counts as progress: **design output is not market evidence, synthetic execution is not client evidence, and a technically complete product is not product-market validation.**

## Launch focus

### Primary launch learning track — Care

The first commercial learning track is Dutch healthcare.

The initial ICP prioritizes care organizations with enough regulatory/contractual urgency, operational complexity and budget to value a maintained security/compliance function but without a proportionate internal CISO/compliance team. A working commercial hypothesis is roughly the 50–250 FTE range, but **employee count is not a legal applicability rule and is not itself the ICP definition**.

Customer-facing regulatory positioning must be scoped accurately:

- direct Cyberbeveiligingswet/NIS2 applicability may be used only after an explicit applicability decision based on current authoritative criteria;
- for organizations outside direct Cbw scope, lead with the obligations and pressures that actually apply to them, including NEN 7510/Wabvpz, privacy, IGJ expectations, contractual/customer requirements, supply-chain pressure and responsible AI governance where relevant;
- no segment message may imply that all small healthcare organizations are directly in Cbw/NIS2 scope.

### Secondary reuse/expansion track — Supplier

Supplier Assurance / Security & Compliance Passport remains strategically useful and the synthetic Supplier work remains valid model evidence. It is not a second parallel zero-customer go-to-market program during the launch-learning phase. It may be promoted to a primary acquisition wedge only if measured market evidence outranks the Care hypothesis.

## Product definition

The three-surface product model remains unchanged:

1. **Operator Workspace** — primary professional working product;
2. **Client Dashboard** — simple customer cockpit;
3. **Interaction Layer** — low-friction evidence, question and approval participation.

However, R2 changes the build order. The first real design-partner learning cycle does **not** require the complete future Operator Workspace and Client Dashboard. The minimum safe workflow may use deliberately bounded operator tooling and secure interactions as long as the authoritative dossier, provenance and authority boundaries remain intact.

## Canonical traceability

The following separation is non-negotiable:

`Source -> Requirement -> Control -> Customer Implementation -> Evidence -> Assessment -> Professional Review -> Decision / Assurance State`

Requirement, control, implementation, evidence, assessment and review remain different objects. A generated policy is not implementation. Strong evidence may prove a gap. AI output never self-promotes to professional or independent assurance.

## Evidence hierarchy for mission claims

R2 introduces explicit evidence classes so the project cannot prove the wrong thing with the wrong evidence.

### E0 — Design evidence

Examples: architecture, schemas, policies, ADRs, validators, code that has not exercised the relevant real workflow.

Can prove: design existence, internal consistency, deterministic constraints.  
Cannot prove: customer usability, willingness to pay, actual workload, commercial viability or real-world assurance quality.

### E1 — Synthetic workflow evidence

Examples: fictional Care/Supplier dossiers and deterministic test cases.

Can prove: model fit, structural traceability, expected workflow coverage, machine-checkable invariants.  
Cannot prove: real customer behavior, evidence availability, response latency, acquisition, willingness to pay or achieved delivery economics.

### E2 — Controlled real-client workflow evidence

A bounded design-partner or client engagement under explicit data/security/contract authority.

Can prove: actual dossier friction, evidence availability, customer burden, professional review burden, real workflow defects and measured delivery effort within that scope.

### E3 — Market/commercial evidence

Examples: qualified customer interviews, proposals, design-partner conversion, paid engagements, objections, loss reasons, channel performance and willingness-to-pay observations.

Can prove: ICP/positioning/channel/pricing hypotheses to the extent of the measured sample.

### E4 — Repeated operational evidence

Multiple governed real delivery cycles showing recurring workload, review outcomes, evidence reuse, remediation patterns, retention, margin and service reliability.

Can support: scaling decisions, validated automation priorities and stronger commercial/economic claims.

**No lower evidence class may be substituted for a success criterion that requires a higher class.**

## Professional trust model

Engineering/change assurance and customer-facing assurance are distinct trust domains.

### A. Product/change assurance

Worker A / Worker B exact-head governance protects consequential project changes. It does not by itself qualify a person or system to issue customer-facing professional assurance.

### B. Customer-facing professional review

Every customer-facing review class must define:

- minimum competence/experience expectations;
- whether a professional credential or sector qualification is required or preferred;
- permitted decision/assurance classes;
- independence requirements;
- maximum manageable review load/capacity assumption;
- loaded cost assumption;
- escalation route when competence or independence is insufficient.

### C. Independent external assurance/certification

Independent audit, certification and regulated professional opinions remain external where independence or formal recognition requires it. SolidSecurity must not present internal professional review as certification or independent external assurance.

## Materiality

`material` is no longer an undefined adjective.

A matter is material when a reasonable error, omission, conflict or unsupported conclusion could meaningfully change at least one of:

- management risk acceptance or prioritization;
- a customer-facing assurance statement or assurance label;
- regulatory/framework applicability;
- a statutory incident/notification decision;
- scope of an external audit/certification decision;
- a significant security/privacy/continuity exposure;
- a contractual/tender/customer representation;
- a decision with significant financial, operational, patient/client-safety or reputational consequence.

Materiality may be refined by service-specific thresholds, but automation may not lower a required review class merely to reduce cost.

## Applicability and tailoring doctrine

External requirement applicability and the concrete client implementation expectation are separate decisions.

Every material applicability/tailoring decision must preserve:

- client scope facts used;
- source/framework version;
- rule/rationale;
- uncertainty or excluded scope;
- proposer identity/type;
- required review class;
- reviewer/decision where required;
- effective date and re-evaluation trigger/expiry where appropriate.

The system may propose applicability/tailoring; material legal/regulatory applicability remains a governed professional decision.

## Evidence conflict and expiry doctrine

Evidence is allowed to disagree.

- contradictory material evidence creates a `CONFLICT_DETECTED` review condition rather than silent averaging or newest-wins behavior;
- a material conflict blocks promotion of the affected claim beyond the last uncontested state until resolved or explicitly bounded;
- evidence validity/expiry is rule- and context-dependent; default validity periods must be explicit by evidence class/control where used;
- expiry downgrades or reopens affected assurance state according to policy rather than leaving stale green status;
- a conflict resolution must preserve both original evidence items, rationale, reviewer and resulting state transition.

## Success criteria

### SS-SC-01 — Managed-service customer experience

SolidSecurity can complete onboarding, baseline assessment, remediation planning and recurring maintenance without turning the customer into the operator of a GRC tool.

### SS-SC-02 — Professional operator leverage

A SolidSecurity professional can manage the complete client lifecycle from one coherent operating system with AI assistance, provenance and review boundaries.

### SS-SC-03 — Clear client visibility

Clients can understand current state, what is demonstrably arranged, attention points, decisions/actions and available reports without a misleading single compliance percentage.

### SS-SC-04 — Evidence-based assurance

Material claims remain reproducible from source, scope, evidence and professional review. Proof Ladder and AI Authority rules remain enforceable.

### SS-SC-05 — Simple secure client data plane

The normal runtime uses one shared tenant-aware PostgreSQL data plane, one private evidence store and simple tested backup/restore. Complexity requires evidence.

### SS-SC-06 — Reusable common-control service model

Multiple obligations reuse one common-control/evidence backbone without framework-specific duplicate client truth. A real mapping corpus must demonstrate partial coverage, multi-control mappings and coverage gaps rather than only describing the mechanism.

### SS-SC-07 — Mission-driven autonomous development

Control can reconstruct authoritative state, select eligible mission gaps, route implementation and independent assurance, and update state without chat-memory or principal relay dependence.

### SS-SC-08 — Bottom-up commercially viable quality

Pricing/package decisions treated as validated are based on measured workflow-step effort, cadence, reviewer class, loaded professional cost and observed automation/reuse outcomes. Top-down prices may remain explicit hypotheses only.

### SS-SC-09 — Real-world design-partner validation

At least one bounded real design-partner/client workflow is completed under explicit data, liability and authority gates before broad productization is treated as justified. E0/E1 evidence cannot satisfy this criterion.

### SS-SC-10 — Professional trust and liability readiness

Before customer-facing `VERIFIED` claims, SolidSecurity has an explicit professional reviewer model, competence/independence/escalation path, professional capacity/cost model, contractual scope limits, liability/insurance posture, report-language limits, breach/incident posture and DPA/subprocessor boundaries.

### SS-SC-11 — Launch-market evidence

The primary launch ICP, positioning, competitor/alternative response and acquisition/channel plan are supported by explicit market hypotheses and progressively replaced by E3 evidence. The service has a concrete answer to the incumbent MSP/IT-provider alternative.

### SS-SC-12 — Governed IP/repository posture

Public and private material are deliberately separated before proprietary mappings, evidence-sufficiency logic, private prompts, GTM/economics or accumulated operating intelligence are published. Public visibility is a deliberate distribution/open-core choice, not a default funding/economics convenience.

## Strategic defensibility doctrine

The common-control graph, mappings, evidence rules and automation are important operating capabilities but are **not assumed to be durable moats by themselves**.

Expected defensibility comes from a reinforcing system of:

- trusted professional delivery and reputation;
- distribution/customer/channel relationships;
- accumulated governed client history and evidence reuse;
- approved recurring assertions and switching costs;
- measured remediation/evidence patterns;
- operational learning and service quality;
- software/AI leverage that compounds those assets.

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

After the minimum safe/executable assurance kernel exists, obtain controlled real workflow evidence before building broad product surfaces from synthetic assumptions.

### Risk-proportionate governance

Mechanical B0 checks should be deterministic and automated/self-executed where safe. Consequential semantic/security/authority changes retain independent exact-head B1 review. Governance cost must correspond to the risk retired.

## Authority boundaries

R2 does not grant authority for:

- real-client data before explicit real-client/design-partner authorization and required contractual/security gates;
- production deployment merely because a runtime exists;
- autonomous final legal/compliance/certification/risk-acceptance/statutory-notification decisions;
- representing internal professional review as external independent assurance or certification;
- customer-environment write/remediation authority;
- publishing client dossiers/evidence/secrets in GitHub;
- publishing proprietary operating intelligence merely because the repository is currently public;
- treating a commercial hypothesis as validated without the required evidence class.

## Architecture contract

The V1 lean data architecture remains:

- one shared PostgreSQL database;
- explicit tenant ownership on tenant data;
- server-side authorization plus RLS/equivalent defense in depth;
- one private object store for client evidence/attachments;
- immutable evidence versions/hashes;
- TLS/provider encryption at rest;
- simple encrypted off-site database + object backup;
- periodic restore proof.

No database-per-client, custom KMS or active-active multi-cloud is a default.

## Mission development loop

`Mission Contract -> authoritative state -> highest-priority eligible evidence gap -> one Minimal Core task -> bounded claim / START_PROVEN -> immutable exact-run result -> at most one predefined successor -> deterministic validation and exact-head B1 where required -> governed integration -> authoritative mission-state update -> next gap`

The canonical Control queue remains the only autonomous project queue.

## R2 gap-selection rule

Select work by this order:

1. preserve hard authority/security/client-data invariants;
2. remove a blocker to safe real-world design-partner evidence;
3. establish professional trust/liability/applicability correctness;
4. make the assurance model executable/falsifiable;
5. reduce repeated operator/customer/reviewer effort observed in real delivery;
6. improve customer clarity and product surfaces;
7. automate/scale only after repeated evidence;
8. infrastructure elegance last.

## Definition of done

A mission gap is complete only when its specified exit evidence exists at the required evidence class and all applicable B0/B1/integration gates have completed.

## Terminal condition

R2 is superseded when all required R2 criteria are supported by authoritative evidence or a later governed revision explicitly replaces it.
