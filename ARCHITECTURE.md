# SolidSecurity Architecture V1

## 1. Architecture objective

The architecture supports a managed compliance service before it supports a software platform. It optimizes for traceability, controlled AI leverage, cross-framework reuse, professional accountability and the simplest safe operational design.

## 2. Logical layers

```text
Customer experience
  status / actions / reports
        ↑
Professional review and decisions
        ↑
AI operations
  extract / map / draft / compare / recommend
        ↑
Client implementation & evidence
        ↑
SolidSecurity Common Control Model
        ↑
Regulatory / standards sources
```

## 3. Non-negotiable traceability invariant

No material assurance conclusion may exist without a reconstructable chain:

`Source -> Requirement -> Control -> Customer Implementation -> Evidence -> Assessment -> Professional Review -> Decision / Assurance State`

A link may explicitly be unknown, not applicable, not evidenced or conflicting; absence may not be silently converted to compliance.

## 4. Separation of object types

- **Requirement** — external obligation or assurance criterion.
- **Control** — reusable internal objective/measure.
- **Customer Implementation** — how one customer implements the control.
- **Evidence** — artifact/observation supporting or refuting implementation.
- **Assessment** — analysis of implementation/evidence.
- **Professional Review** — accountable review of material assessment.
- **Decision** — governed transition or professional conclusion.

See [`docs/DATA_MODEL.md`](docs/DATA_MODEL.md) and canonical M1 contract [`docs/DOMAIN_MODEL_V1.md`](docs/DOMAIN_MODEL_V1.md).

## 5. Product/control plane and client data plane

### Product/control plane — this repository

May contain only public-safe strategy, architecture, generic controls, schemas, workflows, public-source references, synthetic fixtures, ADRs and roadmap material.

### Client data plane — designed, not yet authorized/deployed for real clients

The accepted V1 design is:

```text
Authenticated ingress
       |
       v
Tenant-aware application/API
       |
       +--> one shared PostgreSQL database
       |      tenant_id + server authorization + RLS/equivalent
       |
       +--> one private evidence/object store
       |      tenant-scoped keys + immutable versions/hashes
       |
       +--> audit/review/decision records
       |
       +--> minimum selected context -> AI proposal -> professional review

Nightly:
PostgreSQL logical backup + evidence sync/export
       -> checksums/manifest -> encrypted independent off-site storage
       -> periodic actual restore proof
```

This is an **architecture decision**, not a real-client-data authorization. Real processing starts only after the R2-WP04 minimum-safe-client-envelope, security/data/contract/professional gates and explicit principal authorization are satisfied.

Customer/client material never belongs in this repository.

## 6. Tenant and evidence invariants

- tenant context derives from authenticated authorization context, not user-supplied `tenant_id` alone;
- every tenant-owned domain record carries `tenant_id`;
- RLS/equivalent is defense in depth and cross-tenant negative tests must fail;
- evidence objects are private by default;
- reviewed evidence versions are immutable and integrity-bound by hash;
- changes create a new evidence version rather than silently rewriting historical review evidence;
- backup is not recovery until an actual restore succeeds.

## 7. AI architecture rule

AI is a named actor. Material AI proposals should retain relevant actor/model/policy identity, timestamp, input/source provenance, output version/hash where practical, uncertainty and required review/disposition.

AI cannot self-promote a customer state to `VERIFIED` or another human-only material decision state.

## 8. Open-source integration rule

External projects are capability sources, not automatic dependencies.

- Probo: reference/runtime option only if later evidence justifies it.
- CISO Assistant: architecture/mapping inspiration; AGPL code excluded absent explicit licensing decision.
- isms.sh / Unicis: workflow-pattern references only unless deliberately adopted.
- Prowler: possible later read-only technical evidence source.
- OSCAL/compliance-trestle: possible interoperability later, after internal workflow/model need is proven.

Do not reinvent proven primitives, but do not import a platform merely because it has more features.

## 9. Connector principle

Connectors remain deferred until real workflow evidence proves what evidence is useful. When introduced they should be read-only by default, minimum-permission, tenant-scoped, revocable, auditable and evidence-producing rather than verdict-producing.

Invariant:

`observed configuration -> Evidence -> Assessment -> professional-reviewed state`

Never `scanner pass -> compliance PASS`.

## 10. Complexity gate

The default remains one shared database, one private evidence store and simple independent backup. Database-per-client, custom KMS/envelope encryption, active-active multi-cloud, permanent embedding infrastructure and broad connector programs require a concrete security, contract, scale or measured workflow reason.

## 11. Central Control authority boundary

SolidSecurity owns its product/domain architecture, Mission R2 requirements and repository change constraints. Runtime orchestration, queue/claim mechanics, worker topology and cutover state are owned by the **current central Control authority** and must be read fresh rather than duplicated here.

This architecture therefore **does not encode a fixed Control runtime version or worker topology**. Consequential repository changes remain bound to their exact candidate/head/base and require a **fresh exact-candidate project-change review** under the currently applicable Control/project gate. **Candidate movement invalidates stale review evidence**; review success does not by itself grant integration, deployment, real-client, legal/compliance or certification authority.
