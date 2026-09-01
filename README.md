# SolidSecurity

**Aantoonbaar in control. Zonder eigen complianceafdeling.**

SolidSecurity is an AI-enabled managed security & compliance service for healthcare organizations and other compliance-exposed SMEs. It combines a reusable control backbone, structured evidence, AI-assisted operations and explicit professional review.

> **Automation lowers the work, not the standard.**

## Canonical status

- project mission: **Mission R2 / canonical**;
- domain model: **M1 / canonical schema contract**;
- central execution protocol: **Control Autonomy V3.1**;
- current active product sequence starts with **R2-WP01 — Executable assurance kernel**;
- production deployment and real-client data remain separately gated.

The local mission doctrine is [`control/SOLIDSECURITY_MISSION_CONTRACT_R2.md`](control/SOLIDSECURITY_MISSION_CONTRACT_R2.md). The canonical machine-readable mission and execution authority live in `market-predictions/control-plane`.

Development is deliberately **mission-first, service-first, evidence-first and simplest-safe-architecture-first**. Software is built only where it advances a measurable customer, service or assurance outcome.

## Product model

SolidSecurity is not primarily a self-service GRC portal.

1. **Operator Workspace** — the professional cockpit where SolidSecurity performs the compliance work.
2. **Client Dashboard** — a simple customer view of current state, what is arranged, attention points, actions/decisions, SolidSecurity work and reports.
3. **Interaction Layer** — email, secure uploads, targeted questions and approvals for low-friction customer participation.

The customer supplies knowledge, evidence and decisions that genuinely require them; SolidSecurity owns and executes the process.

## Core doctrine

1. **One control, multiple obligations.** Common controls and evidence are reused where scope and validity allow; client truth is not duplicated per framework.
2. **Requirement is not control; control is not evidence.** Requirements, controls, implementations, evidence, assessments, reviews and decisions are separate objects.
3. **AI proposes; humans remain accountable.** AI may extract, map, draft, compare and recommend. Material assurance, legal interpretation and risk acceptance require qualified human judgment.
4. **No paper compliance.** A generated policy is a designed artifact, not proof that a control operates.
5. **Traceability over confidence theater.** Material conclusions must be reconstructable through `Source -> Requirement -> Control -> Customer Implementation -> Evidence -> Assessment -> Professional Review -> Decision / Assurance State`.
6. **Managed service before self-service.** Do not transfer long compliance workflows to the customer when SolidSecurity can perform them.
7. **Simplest safe architecture first.** Additional providers, databases, cryptographic subsystems or abstractions require a concrete risk, workflow or customer need.
8. **Client data is not project data.** This repository is a public-safe product/control-plane source of truth, never a client dossier store.

## Data-plane direction

The designed V1 data plane is deliberately conventional and is **not yet a real-client deployment authorization**:

- one shared multi-tenant PostgreSQL database;
- `tenant_id` plus server-side authorization and RLS/equivalent defense in depth;
- one private evidence/object store;
- immutable reviewed evidence versions with hashes;
- TLS and provider encryption at rest;
- simple nightly encrypted off-site database + object backup using commodity tooling;
- periodic restore proof.

Database-per-client, custom KMS/envelope encryption and active-active multi-cloud are not V1 defaults.

## Control Autonomy V3.1 development loop

The development authority is intentionally small:

`Mission -> deterministic Feed/TICK -> one canonical V3.1 task -> A1 CLAIM -> bounded implementation/repair -> kernel RECORD -> direct B1 successor -> B1 CLAIM -> independent assurance -> kernel RECORD -> HOLD_AFTER_PASS or separately authorized next action`

Hard execution rules:

- one canonical private runtime queue in `market-predictions/control-plane@control-runtime-state`;
- one deterministic Control Kernel writer;
- semantic workers are exactly **A1** and **B1**;
- no A2;
- no semantic `PROJECT_INTEGRATION` task;
- no direct worker writes to the queue or canonical worker-result store;
- no provider fallback or SolidSecurity-specific scheduler/state plane;
- chat memory is never execution or assurance authority.

## Repository map

- [`control/SOLIDSECURITY_MISSION_CONTRACT_R2.md`](control/SOLIDSECURITY_MISSION_CONTRACT_R2.md) — canonical local project mission doctrine
- [`ROADMAP.md`](ROADMAP.md) — active R2 roadmap and evidence gates
- [`docs/MISSION_DRIVEN_WORKFLOW.md`](docs/MISSION_DRIVEN_WORKFLOW.md) — customer, product/runtime and Control V3.1 workflows
- [`STRATEGY.md`](STRATEGY.md) — market, product and differentiation doctrine
- [`ARCHITECTURE.md`](ARCHITECTURE.md) — target architecture and trust boundaries
- [`docs/OPERATING_MODEL.md`](docs/OPERATING_MODEL.md) — managed-service operating system
- [`docs/DATA_MODEL.md`](docs/DATA_MODEL.md) — conceptual entities
- [`docs/DOMAIN_MODEL_V1.md`](docs/DOMAIN_MODEL_V1.md) — canonical M1 schema contract
- [`docs/COMMON_CONTROL_MODEL.md`](docs/COMMON_CONTROL_MODEL.md) — cross-framework control backbone
- [`docs/AI_AUTHORITY_MODEL.md`](docs/AI_AUTHORITY_MODEL.md) — AI/human authority boundaries
- [`docs/DATA_RESILIENCE_ARCHITECTURE.md`](docs/DATA_RESILIENCE_ARCHITECTURE.md) — lean shared data-plane and resilience doctrine
- [`docs/PUBLIC_REPO_POLICY.md`](docs/PUBLIC_REPO_POLICY.md) — explicit public/private information boundary
- [`model/`](model/) — machine-readable canonical project models
- [`adr/`](adr/) — architectural decisions
- [`control/`](control/) — local project governance doctrine; live Control runtime state remains central

## Public repository notice

This repository currently contains only deliberately public-safe product, model, schema and synthetic material. Client data, secrets and proprietary operating intelligence are prohibited. Proprietary mapping detail, evidence-sufficiency logic, private prompts, detailed GTM/economics and accumulated operating intelligence are private/restricted by default.

No open-source license is granted by this repository unless a file or component explicitly says otherwise.
