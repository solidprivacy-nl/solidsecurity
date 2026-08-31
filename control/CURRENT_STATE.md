# SolidSecurity Current State

## Status

`MISSION_SYSTEM_V1 / CANDIDATE`

Control-managed: **yes**

Mission/governance work: **issue #25**

Current mission branch: `agent/mission-system-v1`

Canonical project mission doctrine: `control/SOLIDSECURITY_MISSION_CONTRACT_V1.md`

Canonical execution lifecycle: Control Minimal Core V1 on `market-predictions/control-plane`.

## Authority

On 2026-08-15 the principal authorized autonomous realization of the agreed SolidSecurity strategy, architecture, model, workflows and roadmap, and subsequently directed that development become mission-driven under central Control.

This does not authorize:

- production deployment;
- real client data before the explicit real-client gate;
- customer-environment scanning/write access by default;
- autonomous final legal/compliance/certification decisions;
- certification claims;
- bypass of independent assurance for consequential work.

## Mission

Deliver an AI-enabled managed security/compliance service that makes small and mid-sized organizations demonstrably in control without requiring their own compliance department.

Software and AI are leverage for the managed service, not the end product.

## Product stance

1. **Operator Workspace** is the primary working product for SolidSecurity professionals.
2. **Client Dashboard** gives the customer a simple plain-language status, actions, decisions, SolidSecurity work and reports.
3. **Interaction Layer** supports email, secure upload, targeted questions and approvals without forcing constant portal navigation.
4. SolidSecurity owns and executes the compliance process; the customer supplies facts, evidence and decisions that genuinely require them.
5. AI prepares repetitive work; professionals remain authoritative for material assessment/assurance/legal decisions.

## Canonical traceability

`Source -> Requirement -> Control -> Customer Implementation -> Evidence -> Assessment -> Professional Review -> Decision / Assurance State`

These states/entities must not be collapsed.

## Data architecture stance

The accepted V1 direction is deliberately lean:

- one shared multi-tenant PostgreSQL database;
- tenant-owned records carry `tenant_id`;
- server authorization plus RLS/equivalent defense in depth;
- one private primary evidence/object store;
- immutable reviewed evidence versions with hashes;
- TLS + provider-managed encryption at rest;
- simple nightly logical DB + evidence backup;
- encrypted off-site transfer to an inexpensive independent storage target using commodity tooling;
- periodic restore proof;
- no database-per-client or custom KMS subsystem by default.

## Mission-driven development

The current Control loop is:

`Mission Contract -> authoritative state -> eligible work -> one Minimal Core task -> bounded claim / START_PROVEN -> immutable result -> at most one predefined successor -> exact-head B1 where required -> governed integration -> mission-state update`

`control/DISPATCH_QUEUE.json` is the single execution authority. No SolidSecurity-specific intake state plane, retry tree, handover lifecycle or competing autonomous queue is authorized.

## Current next product objective

After Mission System V1 becomes authoritative, freeze the minimum relational/domain model required by the accepted managed-service workflow before migrations or UI implementation create avoidable lock-in.

See `ROADMAP.md` and `docs/MISSION_DRIVEN_WORKFLOW.md`.

## Repository visibility

The repository remains public by principal choice during the early phase. Only public-safe project material belongs here.

Secrets, real client data, sensitive implementation details, proprietary evidence-sufficiency rubrics, private prompts and commercially sensitive accumulated operating intelligence are prohibited from the public repo.

See `docs/PUBLIC_REPO_POLICY.md`.

## Current gates

1. Cumulative foundation/runtime convergence is authoritative on `main` through governed PR #24 integration.
2. This Mission System V1 candidate is reconciled onto that authoritative base; the current gate is fresh exact-head independent B1 assurance of the repaired candidate, followed by governed integration on PASS.
3. After Mission System V1 is authoritative, reconcile and independently assure M1 PR #29 against current `main` before integration.
4. After M1 is authoritative, reconcile and independently assure Mission R2 PR #37 in dependency order before starting its executable assurance-kernel work.
5. Keep real client data prohibited until the pilot/runtime/data-governance/professional gate is explicitly satisfied and authorized.
