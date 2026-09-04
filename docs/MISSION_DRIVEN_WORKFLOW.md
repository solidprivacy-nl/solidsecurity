# Mission-Driven Workflow R2

## Purpose

This document keeps three flows separate:

1. the **customer service lifecycle**;
2. the **SolidSecurity product/runtime workflow**;
3. the **central Control development boundary** that governs what SolidSecurity builds next.

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

# C. Central Control development boundary

This flow determines what project capability is built next. SolidSecurity does not implement or mirror its own orchestration layer.

## C1. Authority

- human-readable local doctrine: `control/SOLIDSECURITY_MISSION_CONTRACT_R2.md`;
- canonical machine-readable mission: current SolidSecurity mission in `market-predictions/control-plane`;
- canonical Control architecture/index and runtime state: current central Control sources.

Chat memory and local `CURRENT_STATE.md` are never execution/completion authority.

## C2. Work eligibility

Central Control reconstructs authoritative mission/repository/runtime facts and selects only eligible dependency-satisfied work under its current canonical architecture.

SolidSecurity supplies the workpackage purpose, evidence class, dependencies, acceptance criteria and authority boundaries. It does not prescribe a permanent Control worker topology, claim protocol, transport or scheduler.

## C3. Bounded implementation

Implementation changes only authorized target-repository scope and remains bound to the exact task/purpose and current Control authority. A scheduler/chat invocation is not START_PROVEN or completion evidence by itself.

No project worker may bypass central Control by creating a project-local queue, claim store, handover plane or direct canonical runtime mutation path.

## C4. Fresh exact-candidate review

Consequential changes are reviewed against the exact candidate/head/base and applicable acceptance criteria.

- deterministic tests/CI cover mechanical invariants;
- review is fresh and evidence-first rather than a restatement of implementation claims;
- candidate movement invalidates stale review;
- `PASS`, `FAIL` and `INDETERMINATE` remain the bounded project-change verdicts;
- `INDETERMINATE` fails closed;
- repair changes create a new candidate that must be reviewed again;
- external/organizationally independent exact-candidate review is mandatory whenever the workpackage, material risk, current repository policy or central Control gate requires it.

Central Control may implement fresh critical review with its current runner architecture; SolidSecurity does not create a permanent second assurance lane to achieve review separation.

## C5. Post-review behavior

A PASS proves only the review gate. Integration, release, deployment and customer authority remain separate and require the current applicable authority.

Central Control may hold, integrate, repair or continue only according to its current governed state and repository authority. SolidSecurity does not create a semantic integration task or other local continuation mechanism merely to mirror one Control version.

## C6. Hard project invariants

```text
central_control_authority=1
project_local_runtime_state_plane=false
project_local_scheduler=false
direct_control_runtime_bypass=false
exact_candidate_binding=true
stale_review_after_candidate_movement=false
deterministic_validation_where_mechanical=true
external_review_when_required=true
provider_fallback_introduced_locally=false
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
