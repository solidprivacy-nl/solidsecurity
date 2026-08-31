# Mission-Driven Workflow V1

## Purpose

This document connects three different flows without mixing their authority:

1. the **customer service lifecycle**;
2. the **SolidSecurity product/runtime workflow**;
3. the **Control mission-development workflow** that decides what SolidSecurity builds next.

The customer never interacts with the Control development queue. The Control plane never stores client evidence.

---

# A. Customer service lifecycle

## A1. Qualification and scope

SolidSecurity speaks with the prospective customer and establishes organization type, business context, existing obligations, key systems/suppliers, desired outcome and service fit.

Output:

- provisional organization profile;
- likely framework/obligation scope;
- service proposition (for example Care or Supplier);
- explicit unknowns.

## A2. Operator-led onboarding

A SolidSecurity professional leads the onboarding conversation. The customer is not handed a large self-service questionnaire.

The operator records structured facts while the customer explains the organization. AI may turn notes/transcripts into proposed structured facts, but facts requiring confidence or interpretation are validated by a professional.

## A3. Targeted information request

From the known facts and gaps, SolidSecurity generates a short customer-friendly request containing only what is still needed.

Possible channels:

- email;
- secure upload link;
- short question form;
- meeting follow-up.

Every request maps internally to the relevant fact, control, evidence need or decision.

## A4. Evidence inbox and extraction

Received files, answers and notes enter the client dossier.

AI may:

- classify documents;
- extract relevant facts/passages;
- identify candidate controls/requirements;
- detect contradictions/expired evidence;
- propose missing information.

Every material extraction retains source/provenance. AI output remains proposed until governed acceptance where required.

## A5. Scope and control instantiation

SolidSecurity confirms applicable scope and instantiates the relevant common controls for the client.

Canonical separation remains:

`Requirement != Control != Implementation != Evidence != Assessment != Review`

## A6. Assessment and findings

For each applicable control, SolidSecurity records what the customer actually does, what evidence exists, what remains uncertain and what the professional assessment is.

Strong evidence can prove a gap. Generated policy text does not raise proof level by itself.

## A7. Remediation and managed execution

SolidSecurity converts findings into a prioritized plan.

The system explicitly separates:

- work SolidSecurity can perform;
- information/evidence needed from the customer;
- decisions the customer must make;
- work waiting on an external supplier;
- material items requiring professional review.

SolidSecurity should perform the first category rather than turning it back into customer homework.

## A8. Professional review

Material/ambiguous conclusions enter the review queue. AI cannot self-verify them.

The reviewer can accept, modify or reject proposed conclusions and must be able to reconstruct the evidence/provenance behind them.

## A9. Client dashboard and baseline output

The dashboard translates internal control state into ordinary language.

It shows at minimum:

- overall management status by recognizable domain;
- what is demonstrably arranged;
- attention points;
- actions/decisions required from the customer;
- work currently performed by SolidSecurity;
- recently completed SolidSecurity work;
- available reports and last review date.

Avoid a single percentage that implies mathematical certainty of compliance.

## A10. Recurring managed cycle

The client dossier remains alive after baseline delivery.

Recurring triggers include:

- evidence expiry;
- outstanding actions;
- new suppliers/systems/AI use;
- incidents/material changes;
- scheduled control reviews;
- relevant requirement/source changes.

The cycle repeats only the affected parts rather than restarting a full audit.

---

# B. Product/runtime workflow

## B1. Operator Workspace

This is the primary professional interface and exposes full domain detail.

Core work queues/views:

- client portfolio;
- onboarding/intake;
- evidence inbox;
- controls/implementations;
- findings/actions;
- client requests;
- AI proposals;
- professional review queue;
- approvals/reports;
- recurring/expiry queue.

## B2. Client Dashboard

This is a customer-management interface, not a GRC workbench.

Default navigation should stay small, for example:

- Overzicht;
- Wat is geregeld;
- Acties & besluiten;
- Rapportages/bewijs.

## B3. Interaction Layer

Low-friction external actions may be completed through expiring/scoped links where appropriate:

- upload evidence;
- answer one or a few questions;
- confirm a fact;
- approve/sign off a document/decision.

The completed interaction writes back into the same authoritative dossier; there is no separate questionnaire truth.

## B4. Data flow

```text
Client / SolidSecurity operator
          |
          v
Application authorization
          |
          v
Shared PostgreSQL <----> Private evidence object store
          |
          +---- selected minimum context ----> AI proposal path
          |                                      |
          |                                      v
          |                                PROPOSED output
          |                                      |
          +<----------- professional review -----+

Nightly:
PostgreSQL logical backup + evidence object sync/export
          -> checksum/manifest -> encrypted off-site backup
```

---

# C. Mission-driven development workflow

This flow determines what product/service capability is built next. It uses the current Control Minimal Core lifecycle; no SolidSecurity-specific orchestration layer exists.

## C1. Authoritative mission

The canonical machine-readable SolidSecurity mission resides in `market-predictions/control-plane/control/missions/SOLIDSECURITY.mission.json` when that revision is independently assured and integrated.

The local human-readable contract is `control/SOLIDSECURITY_MISSION_CONTRACT_V1.md`.

## C2. State reconstruction

Before deriving work, Control reads authoritative repository/project/runtime state. Chat memory is context only and cannot establish completion, execution or assurance.

## C3. Work selection

Choose the highest-priority eligible unsatisfied mission work whose dependencies are satisfied.

One Minimal Core task should represent one immutable purpose/operation. Do not combine unrelated implementation objectives merely to reduce issue count.

## C4. Single authoritative queue

Authorized work is materialized directly as one validated task in the existing `control/DISPATCH_QUEUE.json` authority. There is no separate project intake state plane, handover lifecycle, retry lineage or SolidSecurity scheduler.

The task reserves only its immediate predefined successor.

## C5. Worker claim / START_PROVEN

A scheduler or chat wake-up is not execution evidence. A bounded authoritative claim proves execution start.

- A1/A2 perform implementation, repair or project integration work.
- B1 performs independent exact-head assurance.
- role capacity and repository exclusivity remain enforced by Control.

## C6. Immutable result and successor

Each execution produces an exact-task/exact-run immutable result.

- implementation `COMPLETED` may materialize exactly one ASSURANCE successor;
- implementation `BLOCKED` creates no semantic successor;
- assurance `PASS` may materialize exactly one PROJECT_INTEGRATION successor;
- assurance `FAIL` may materialize exactly one REPAIR successor;
- assurance `INDETERMINATE` creates no semantic successor;
- infrastructure/transport failure is not a semantic verdict and does not create a retry tree.

## C7. Governed integration and mission-state update

After exact-head PASS and governed integration, authoritative outcome evidence is evaluated against the mission criterion. A gap is SATISFIED only when the evidence is sufficient, not merely because a PR merged.

Control can then select or materialize the next eligible mission work.

## C8. Exact-head rule

Consequential candidates are frozen to their exact candidate SHA for B1. If the candidate changes, assurance must be refreshed. B1 is read-only and cannot repair, merge, release or deploy.

---

# D. Anti-overengineering / convergence rules

Before introducing a new service, table family, provider, queue, abstraction or security subsystem, ask:

1. Which mission criterion does it advance?
2. Which observed workflow/risk requires it?
3. Can the same outcome be achieved with an existing object/process/tool?
4. Does it reduce customer burden or operator work, or materially improve evidence/assurance?
5. What new operational failure modes does it create?
6. Can it be deferred until a synthetic/real workflow proves the distinction matters?

If no concrete mission/risk evidence exists, defer it.

Examples of intentionally deferred complexity:

- separate database per customer;
- custom KMS/envelope-encryption system;
- active-active multi-cloud database;
- broad enterprise framework import;
- permanent embeddings/vector memory for all evidence;
- environment write/remediation connectors;
- multiple autonomous development queues.

---

# E. Mission evidence

Mission progress should increasingly be demonstrated by operational evidence such as:

- end-to-end workflow completion;
- customer inputs/actions required per onboarding;
- professional minutes/hours per client step;
- percentage of AI proposals accepted/modified/rejected;
- number of evidence items reused across requirements/questionnaires;
- customer dashboard comprehension/action completion;
- cross-tenant negative test results;
- backup/restore results;
- number and materiality of professional review exceptions;
- recurring cycle effort versus initial baseline effort.

These measures are inputs to product decisions, not vanity KPIs or automatic compliance claims.
