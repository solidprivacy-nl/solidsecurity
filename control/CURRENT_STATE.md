# SolidSecurity Current State

> **Snapshot only — never routing or execution authority.** Live execution/cutover state must be read from the current canonical sources in `market-predictions/control-plane` and current repository/runtime facts.

## Canonical project status

- Mission: **R2 / canonical**
- Domain model: **M1 / canonical schema contract**
- Control-managed: **yes**
- Control runtime/protocol: **owned centrally; read fresh from current Control authority**
- Local mission doctrine: `control/SOLIDSECURITY_MISSION_CONTRACT_R2.md`
- Active R2 sequence starts with `R2-WP01 — Executable assurance kernel`

SolidSecurity does not mirror a Control version, worker topology, queue protocol or cutover phase in this file. A Control architecture change therefore cannot silently make this project snapshot authoritative or stale the Mission itself.

## Mission

Deliver an AI-enabled managed security/compliance service that makes organizations demonstrably in control without requiring their own compliance department.

Software and AI are leverage for the managed service, not the end product.

## Product stance

1. **Operator Workspace** is the primary professional work surface.
2. **Client Dashboard** gives a plain-language view of current state, arranged controls, attention points, actions/decisions and reports.
3. **Interaction Layer** supports low-friction evidence, questions and approvals.
4. SolidSecurity owns and executes the compliance process; the customer supplies facts, evidence and decisions that genuinely require them.
5. AI prepares repetitive work; qualified humans remain authoritative for material assessment, assurance and legal/compliance decisions.

## Canonical traceability

`Source -> Requirement -> Control -> Customer Implementation -> Evidence -> Assessment -> Professional Review -> Decision / Assurance State`

These states/entities must not be collapsed.

## Data architecture stance

The designed V1 direction is deliberately lean:

- one shared multi-tenant PostgreSQL database;
- tenant-owned records carry `tenant_id`;
- server authorization plus RLS/equivalent defense in depth;
- one private primary evidence/object store;
- immutable reviewed evidence versions with hashes;
- TLS + provider-managed encryption at rest;
- simple nightly encrypted off-site backup;
- periodic restore proof;
- no database-per-client or custom KMS subsystem by default.

This design does **not** authorize real-client data or production deployment.

## Central Control boundary

- central Control is the sole development-runtime authority; SolidSecurity creates no competing queue/state plane;
- current Control runtime version, locks, scheduling, worker topology and integration state are external live facts and must be read fresh;
- consequential project candidates retain exact candidate/head/base binding and fresh critical review;
- external/independent exact-candidate review remains required whenever the current project or Control gate requires it;
- **candidate movement invalidates stale review**; review evidence never follows a moved candidate;
- no direct project worker writes to canonical Control state outside the current central contract;
- no SolidSecurity-specific scheduler, intake/handover runtime plane or provider fallback;
- `principal_manual_relay_count=0` remains the target/invariant.

## Authority boundaries

Current project authority does not by itself authorize:

- production deployment;
- real-client data before the explicit real-client gate;
- customer-environment write/remediation access;
- autonomous final legal/compliance/certification/risk-acceptance decisions;
- certification claims;
- bypass of a review/assurance gate that is currently applicable to a consequential change.

## Repository visibility

Only public-safe project material belongs here. Client data, secrets, proprietary evidence-sufficiency logic, private prompts, detailed commercial operating intelligence and restricted mappings stay outside the public repository unless deliberately released.

See `docs/PUBLIC_REPO_POLICY.md`.
