# SolidSecurity

**Aantoonbaar in control. Zonder eigen complianceafdeling.**

SolidSecurity is an AI-enabled managed security & compliance service model for small healthcare organizations and compliance-exposed SMEs. It combines a reusable control backbone, structured evidence, AI-assisted operations and explicit professional review.

> **Automation lowers the work, not the standard.**

## Mission status

`MISSION_SYSTEM_V1 / CANDIDATE`

Project mission/governance work: [issue #25](https://github.com/solidprivacy-nl/solidsecurity/issues/25)

The governing project doctrine is [`control/SOLIDSECURITY_MISSION_CONTRACT_V1.md`](control/SOLIDSECURITY_MISSION_CONTRACT_V1.md). Development is controlled through the existing Control Minimal Core lifecycle and its single authoritative dispatch queue.

Development is deliberately **mission-first, service-first, evidence-first and simplest-safe-architecture-first**. Software is built only where it advances a measurable customer/service/assurance outcome.

## Product model

SolidSecurity is not primarily a self-service GRC portal.

1. **Operator Workspace** — the professional cockpit where SolidSecurity performs the compliance work.
2. **Client Dashboard** — a simple customer view of current status, what is arranged, attention points, actions/decisions, SolidSecurity work and reports.
3. **Interaction Layer** — email, secure uploads, targeted questions and approvals for low-friction customer participation.

The customer supplies knowledge, evidence and decisions that genuinely require them; SolidSecurity owns and executes the process.

## Target market

SolidSecurity is designed primarily for organizations that are too small for a full internal security/compliance function but increasingly need to demonstrate control because of:

- Dutch Cybersecurity Act (Cbw) / NIS2 obligations or supply-chain pressure;
- NEN 7510 and healthcare information-security expectations;
- ISO 27001 readiness or certification ambitions;
- GDPR/privacy governance;
- responsible AI / EU AI Act governance;
- customer questionnaires, tenders and assurance requests.

## Core doctrine

1. **One control, multiple obligations.** Common controls are mapped to multiple external frameworks instead of maintaining isolated checklists.
2. **Requirement is not control; control is not evidence.** External obligations, internal controls, client implementations, evidence, assessments and assurance decisions are separate objects.
3. **AI proposes; humans remain accountable.** AI may extract, map, draft, compare and recommend. Material assurance, legal interpretation and risk acceptance require qualified human judgment.
4. **No paper compliance.** A generated policy is only a designed artifact, never proof that a control operates effectively.
5. **Traceability over confidence theater.** Material conclusions must be reconstructable from source to requirement to control to implementation to evidence to review.
6. **Managed service before self-service.** Do not transfer long compliance workflows to the customer when SolidSecurity can perform them.
7. **Simplest safe architecture first.** Additional providers, databases, cryptographic subsystems or abstractions require a concrete risk/workflow/customer need.
8. **Client data is not project data.** This repository is the product/control-plane source of truth, never a client dossier store.

## Data-plane direction

The V1 target is deliberately conventional:

- one shared multi-tenant PostgreSQL database;
- `tenant_id` plus server-side authorization/RLS defense in depth;
- one private evidence/object store;
- immutable reviewed evidence versions with hashes;
- TLS and provider encryption at rest;
- simple nightly encrypted off-site database + object backup using commodity tooling;
- periodic restore proof.

Database-per-client, custom KMS/envelope encryption and active-active multi-cloud are not V1 defaults.

## Mission-driven development

The current development lifecycle is intentionally small:

`Mission Contract -> authoritative state -> eligible work -> one Minimal Core task -> bounded claim / START_PROVEN -> immutable result -> at most one predefined successor -> exact-head B1 where required -> governed integration -> mission-state update`

`control/DISPATCH_QUEUE.json` remains the single execution authority. SolidSecurity does not create its own intake state plane, retry lineage, scheduler or competing queue.

## Repository map

- [`control/SOLIDSECURITY_MISSION_CONTRACT_V1.md`](control/SOLIDSECURITY_MISSION_CONTRACT_V1.md) — governing project mission, success criteria and authority boundaries
- [`ROADMAP.md`](ROADMAP.md) — mission-driven product roadmap and exit evidence
- [`docs/MISSION_DRIVEN_WORKFLOW.md`](docs/MISSION_DRIVEN_WORKFLOW.md) — customer, runtime and Control development workflows
- [`STRATEGY.md`](STRATEGY.md) — market, product and differentiation doctrine
- [`ARCHITECTURE.md`](ARCHITECTURE.md) — target architecture and trust boundaries
- [`docs/OPERATING_MODEL.md`](docs/OPERATING_MODEL.md) — managed-service operating system
- [`docs/DATA_MODEL.md`](docs/DATA_MODEL.md) — canonical conceptual entities
- [`docs/COMMON_CONTROL_MODEL.md`](docs/COMMON_CONTROL_MODEL.md) — cross-framework control backbone
- [`docs/AI_AUTHORITY_MODEL.md`](docs/AI_AUTHORITY_MODEL.md) — AI/human authority boundaries
- [`docs/DATA_RESILIENCE_ARCHITECTURE.md`](docs/DATA_RESILIENCE_ARCHITECTURE.md) — lean shared data-plane and resilience doctrine
- [`docs/PUBLIC_REPO_POLICY.md`](docs/PUBLIC_REPO_POLICY.md) — what may and may not live in this public repo
- [`docs/workflows/`](docs/workflows/) — detailed care/supplier workflow material
- [`model/`](model/) — machine-readable project models
- [`adr/`](adr/) — architectural decisions
- [`control/`](control/) — project governance and assurance state

## Public repository notice

This repository is currently public during the early phase. Public visibility does **not** mean that client data, secrets, proprietary evidence rubrics, private prompts or confidential operating material belong here. See [`docs/PUBLIC_REPO_POLICY.md`](docs/PUBLIC_REPO_POLICY.md).

No open-source license is granted by this repository unless a file or component explicitly says otherwise.
