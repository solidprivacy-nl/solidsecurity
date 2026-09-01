# Mission-Driven Workflow R2 / Control V3.1

## Purpose

This document keeps three flows separate:

1. the **customer service lifecycle**;
2. the **SolidSecurity product/runtime workflow**;
3. the **Control development workflow** that decides and governs what SolidSecurity builds next.

The customer never interacts with the Control development queue. Control never stores client evidence as project/runtime state.

---

# A. Customer service lifecycle

## A1. Qualification and scope

Establish organization context, actual obligations/pressures, key systems/suppliers, desired outcome, service fit and explicit unknowns. Direct Cbw/NIS2 positioning requires a real applicability basis.

## A2. Operator-led onboarding

A SolidSecurity professional leads the conversation. The customer is not handed a large self-service GRC questionnaire. AI may propose structured facts from notes/transcripts; material facts and interpretations remain reviewable.

## A3. Targeted information request

Ask only for information/evidence that is still needed. Requests map internally to a fact, control, evidence need or decision and may use email, secure upload, short questions or meeting follow-up.

## A4. Evidence inbox and extraction

Received files, answers and notes enter the client dossier. AI may classify, extract, compare, detect conflicts/expiry and propose missing information, while preserving provenance. AI output remains proposed until the applicable review/decision boundary is satisfied.

## A5. Scope and control instantiation

Confirm applicability and instantiate relevant common controls without collapsing object types:

`Requirement != Control != Implementation != Evidence != Assessment != Review != Decision`

## A6. Assessment and findings

Record what the client actually does, what evidence exists, what remains uncertain and the resulting governed assessment. A generated policy never raises proof level by itself.

## A7. Remediation and managed execution

Separate:

- work SolidSecurity can perform;
- evidence/information required from the customer;
- customer decisions;
- supplier dependencies;
- material professional-review items.

SolidSecurity performs the first category rather than returning it as customer homework.

## A8. Professional review

Material/ambiguous conclusions enter the review path. The reviewer can accept, modify, reject or escalate and must be able to reconstruct scope, evidence and provenance.

## A9. Client visibility

The customer surface shows in ordinary language:

- current state;
- what is demonstrably arranged;
- attention points;
- required actions/decisions;
- SolidSecurity work;
- available reports and review freshness.

Do not require control-ID/GRC literacy and do not present a single percentage as mathematical certainty of compliance.

## A10. Recurring managed cycle

Re-open only affected parts of the dossier when evidence expires, actions remain open, systems/suppliers/AI use change, incidents occur, scheduled reviews become due or relevant source requirements change.

---

# B. Product/runtime workflow

## B1. Operator Workspace

Primary professional work surface for client portfolio, onboarding, evidence, implementations, findings/actions, client requests, AI proposals, professional review, decisions/reports and recurring/expiry work.

## B2. Client Dashboard

A simple customer-management surface, not a GRC workbench. Default navigation should remain small and outcome-oriented.

## B3. Interaction Layer

Low-friction external actions may use scoped/expiring links for evidence upload, focused questions, fact confirmation and approvals. Every completed interaction writes back to the same authoritative dossier.

## B4. Designed data flow

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
          -> periodic actual restore proof
```

This architecture is designed but does not authorize real-client processing until the explicit R2 real-client gate is satisfied.

---

# C. Control Autonomy V3.1 development workflow

This flow determines what project capability is built next. SolidSecurity does not implement its own orchestration layer.

## C1. Mission authority

- human-readable local doctrine: `control/SOLIDSECURITY_MISSION_CONTRACT_R2.md`;
- canonical machine-readable mission: `market-predictions/control-plane/control/missions/SOLIDSECURITY.mission.json`;
- canonical runtime state: `market-predictions/control-plane@control-runtime-state`.

Chat memory and local `CURRENT_STATE.md` are never execution/completion authority.

## C2. Deterministic Feed/TICK

The single Control Kernel reconstructs current mission/repository facts and feeds only eligible dependency-satisfied gaps into the one canonical V3.1 queue. Feed/TICK creates no semantic claim and performs no semantic implementation/assurance.

## C3. A1 claim and implementation

Exactly one semantic implementation worker exists: **A1 / `implementation_operations`**.

A1 may process only a canonical `IMPLEMENTATION` or `REPAIR` task after the V3.1 kernel has persisted a current bounded claim for exact task/role/worker/run identity. Scheduler/chat invocation is not START_PROVEN.

A1 changes only authorized target-repository scope and may not self-assure.

## C4. Kernel RECORD

A semantic worker never writes canonical queue/result state directly. When A1 completes, it submits a bounded result to the Control Kernel `RECORD` command. The kernel atomically validates the current claim, stores the immutable result, terminalizes the task and creates at most the direct successor authorized by V3.1.

A successful implementation may therefore create one direct B1 assurance successor. A blocked/unavailable execution does not create a retry tree.

## C5. B1 independent assurance

Exactly one assurance worker exists: **B1 / `governance_release_assurance`**.

B1 starts only from its own current kernel claim and independently reviews the exact frozen candidate and task acceptance criteria. B1 is read-only on the candidate and cannot repair, merge, release or deploy.

The verdict is exactly one of `PASS`, `FAIL` or `INDETERMINATE` and is persisted only through kernel `RECORD`.

## C6. Post-assurance behavior

- `PASS` records authoritative independent project-change evidence;
- repository integration occurs only when current live repository authority separately permits it;
- SolidSecurity currently uses `HOLD_AFTER_PASS`, so PASS alone is not autonomous merge authority;
- `FAIL` may yield only the bounded repair behavior defined by V3.1/current mission authority;
- `INDETERMINATE` fails closed;
- infrastructure/transport unavailability is not a semantic FAIL.

There is **no semantic `PROJECT_INTEGRATION` task** in V3.1.

## C7. Hard V3.1 invariants

```text
runtime_writers=1
runtime_queue=1
semantic_workers=A1,B1
A2=false
direct_worker_runtime_write=false
semantic_PROJECT_INTEGRATION=false
provider_fallback=false
project_local_runtime_state_plane=false
principal_manual_relay_target=0
```

---

# D. Anti-overengineering / convergence rules

Before introducing a new service, table family, provider, queue, abstraction or security subsystem, ask:

1. Which mission criterion does it advance?
2. Which observed workflow/risk requires it?
3. Can an existing object/process/tool satisfy the requirement?
4. Does it reduce customer/operator/reviewer work or materially improve evidence/assurance?
5. What new failure modes does it create?
6. Can it wait until synthetic or real workflow evidence proves it is needed?

If no concrete mission/risk evidence exists, defer it.

Intentionally deferred complexity includes database-per-client by default, custom KMS/envelope encryption, active-active multi-cloud, broad framework imports, permanent embeddings for all evidence, write-capable environment connectors and competing development queues.

---

# E. Mission evidence

Mission progress should increasingly be demonstrated with evidence such as end-to-end workflow completion, actual customer/operator/reviewer effort, AI proposal acceptance/edit/rejection, evidence/assertion reuse, customer comprehension, tenant-isolation negatives, backup/restore proof, professional-review exceptions and recurring-cycle effort.

These are decision inputs, not vanity KPIs or automatic compliance claims.
