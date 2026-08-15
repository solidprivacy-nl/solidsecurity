# SolidSecurity

**Aantoonbaar in control. Zonder eigen complianceafdeling.**

SolidSecurity is an AI-native managed security & compliance operating model for small healthcare organizations and compliance-exposed SMEs. It combines a reusable control backbone, structured evidence, AI-assisted operations and explicit professional review.

> **Automation lowers the work, not the standard.**

## Target market

SolidSecurity is designed primarily for organizations that are too small for a full internal security/compliance function but increasingly need to demonstrate control because of:

- Dutch Cybersecurity Act (Cbw) / NIS2 obligations or supply-chain pressure;
- NEN 7510 and healthcare information-security expectations;
- ISO 27001 readiness or certification ambitions;
- GDPR/privacy governance;
- responsible AI / EU AI Act governance;
- customer questionnaires, tenders and assurance requests.

## Foundation status

`FOUNDATION_IMPLEMENTATION / CANDIDATE`

Authoritative work contract: [issue #2](https://github.com/solidprivacy-nl/solidsecurity/issues/2)

The project is deliberately **model-first, service-first and evidence-first**. We are not building or importing a full GRC platform before the managed-service workflow has been validated.

## Core doctrine

1. **One control, multiple obligations.** Common controls are mapped to multiple external frameworks instead of maintaining isolated checklists.
2. **Requirement is not control; control is not evidence.** External obligations, internal controls, client implementations, evidence, assessments and assurance decisions are separate objects.
3. **AI proposes; humans remain accountable.** AI may extract, map, draft, compare and recommend. Material assurance, legal interpretation and risk acceptance require qualified human judgment.
4. **No paper compliance.** A generated policy is only a designed artifact, never proof that a control operates effectively.
5. **Traceability over confidence theater.** Material conclusions must be reconstructable from source to requirement to control to implementation to evidence to review.
6. **Start lean.** No automatic customer-environment scanning in the initial service model.
7. **Client data is not project data.** This repository is the product/control-plane source of truth, never a client dossier store.

## Repository map

- [`STRATEGY.md`](STRATEGY.md) — market, product and differentiation doctrine
- [`ARCHITECTURE.md`](ARCHITECTURE.md) — target architecture and trust boundaries
- [`ROADMAP.md`](ROADMAP.md) — staged realization plan and decision gates
- [`docs/POSITIONING.md`](docs/POSITIONING.md) — messaging and credibility rules
- [`docs/OPERATING_MODEL.md`](docs/OPERATING_MODEL.md) — managed-service operating system
- [`docs/DATA_MODEL.md`](docs/DATA_MODEL.md) — canonical conceptual entities
- [`docs/COMMON_CONTROL_MODEL.md`](docs/COMMON_CONTROL_MODEL.md) — cross-framework control backbone
- [`docs/AI_AUTHORITY_MODEL.md`](docs/AI_AUTHORITY_MODEL.md) — AI/human authority boundaries
- [`docs/OPEN_SOURCE_ADOPTION.md`](docs/OPEN_SOURCE_ADOPTION.md) — selective reuse decisions
- [`docs/PUBLIC_REPO_POLICY.md`](docs/PUBLIC_REPO_POLICY.md) — what may and may not live in this public repo
- [`docs/workflows/`](docs/workflows/) — client lifecycle, care and supplier workflows
- [`model/`](model/) — machine-readable foundation seeds
- [`adr/`](adr/) — architectural decisions
- [`control/`](control/) — project governance and assurance contract

## Public repository notice

This repository is currently public for collaboration and GitHub Actions economics. Public visibility does **not** mean that client data, secrets, proprietary evidence rubrics, private prompts or confidential operating material belong here. See [`docs/PUBLIC_REPO_POLICY.md`](docs/PUBLIC_REPO_POLICY.md).

No open-source license is granted by this repository unless a file or component explicitly says otherwise.
