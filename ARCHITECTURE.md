# SolidSecurity Architecture V1

## 1. Architecture objective

The architecture must support a managed compliance service before it supports a software platform. It optimizes for traceability, controlled AI leverage, cross-framework reuse and professional accountability.

## 2. Logical layers

```text
┌──────────────────────────────────────────────┐
│ 6. Customer experience                      │
│ status / actions / reports / passport        │
└──────────────────────────────────────────────┘
                      ↑
┌──────────────────────────────────────────────┐
│ 5. Professional assurance                    │
│ review / exceptions / approval / sign-off    │
└──────────────────────────────────────────────┘
                      ↑
┌──────────────────────────────────────────────┐
│ 4. AI operations                             │
│ extract / map / draft / compare / recommend  │
└──────────────────────────────────────────────┘
                      ↑
┌──────────────────────────────────────────────┐
│ 3. Client implementation & evidence          │
│ claims / evidence / findings / actions        │
└──────────────────────────────────────────────┘
                      ↑
┌──────────────────────────────────────────────┐
│ 2. SolidSecurity Common Control Model        │
│ controls / evidence expectations / mappings  │
└──────────────────────────────────────────────┘
                      ↑
┌──────────────────────────────────────────────┐
│ 1. Regulatory / standards source layer       │
│ Cbw/NIS2 / NEN / ISO / GDPR / EU AI Act      │
└──────────────────────────────────────────────┘
```

## 3. Non-negotiable traceability invariant

No material assurance conclusion may exist without a reconstructable chain:

`source -> requirement -> control -> implementation claim -> evidence -> assessment -> review -> decision`

A link may explicitly be `unknown`, `not applicable`, `not evidenced` or `conflicting`; absence may not be silently converted to compliance.

## 4. Separation of object types

The architecture deliberately separates:

- **Requirement** — an external obligation or assurance criterion.
- **Control** — a reusable internal objective/measure.
- **Implementation claim** — how one customer says the control is implemented.
- **Evidence** — an artifact or observation supporting/refuting the claim.
- **Assessment** — an analysis of the implementation/evidence.
- **Review** — an accountable human review of a material assessment.
- **Decision** — a governed state transition or professional conclusion.

See [`docs/DATA_MODEL.md`](docs/DATA_MODEL.md).

## 5. Initial implementation architecture

Foundation and Service MVP require no dedicated GRC platform.

```text
GitHub product/control plane
  ├─ methodology
  ├─ control definitions
  ├─ mappings metadata
  ├─ templates
  ├─ workflows
  ├─ roadmap / ADR / change control
  └─ synthetic test fixtures only

Secure client workspace (future, separate)
  ├─ customer facts
  ├─ evidence
  ├─ implementation claims
  ├─ risks / findings / actions
  ├─ generated client artifacts
  └─ review / decision records

AI execution boundary
  ├─ reads only authorized source/client context
  ├─ outputs suggestions / drafts / assessments
  └─ cannot self-promote to verified assurance

Professional review boundary
  └─ approves, rejects, edits or escalates material conclusions
```

## 6. Product/control plane vs client data plane

### Product/control plane — this repository

May contain public-safe:

- strategy and architecture;
- generic controls;
- schemas;
- generic workflows;
- public-source references;
- synthetic fixtures;
- ADRs and roadmap.

### Client data plane — never this repository

Will contain:

- customer contracts and policies;
- system and supplier inventories;
- vulnerabilities and incidents;
- personnel or patient information;
- implementation details;
- evidence;
- client-specific risk/assessment records.

A future client data plane requires an explicit data-governance and security architecture decision before the first real dossier is ingested.

## 7. AI architecture rule

AI is a named actor, not an invisible implementation detail. Every AI-originated material suggestion should eventually carry:

- actor/model identity where relevant;
- timestamp;
- input/source provenance;
- output version/hash where practical;
- confidence/uncertainty where useful;
- required review class;
- reviewer and disposition.

AI cannot change a control from `EVIDENCED` to `VERIFIED` without an authorized human review event.

## 8. Open-source integration architecture

External projects are treated as **capability sources**, not automatic platform dependencies.

- Probo: reference model now; runtime decision later.
- CISO Assistant: architecture/mapping inspiration only; AGPL code excluded absent explicit licensing decision.
- isms.sh: human/AI suggestion and review patterns; no runtime dependency yet.
- Unicis: privacy workflow patterns; no runtime dependency yet.
- Prowler: candidate read-only technical evidence provider in a later phase.
- compliance-trestle/OSCAL: candidate interoperability layer only after internal model stability.

See [`docs/OPEN_SOURCE_ADOPTION.md`](docs/OPEN_SOURCE_ADOPTION.md).

## 9. Connector principle

Technical connectors are explicitly deferred until the manual/AI-assisted service model proves what evidence is actually valuable.

When introduced, connectors should be:

1. read-only by default;
2. minimum-permission;
3. tenant-scoped;
4. evidence-producing rather than verdict-producing;
5. revocable;
6. observable/auditable;
7. conflict-aware (declared state versus observed state).

## 10. Platform decision gate

After Service MVP/pilots, choose deliberately among:

- thin custom application over the SolidSecurity model;
- Probo as a backend/runtime;
- another permissively licensed component;
- hybrid architecture.

The decision must be based on validated workflow needs, not feature-count attraction.
