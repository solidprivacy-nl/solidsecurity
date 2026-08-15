# SolidSecurity Mission-Driven Roadmap

## Doctrine

The roadmap is subordinate to `control/SOLIDSECURITY_MISSION_CONTRACT_V1.md` and the canonical Control Mission Contract.

The roadmap does not exist to maximize delivered features. It exists to close the highest-value unsatisfied mission gaps with the smallest coherent change.

Core rules:

- customer outcome over software output;
- managed service before self-service;
- evidence and professional assurance before green status;
- service workflow before integrations;
- simplest safe architecture first;
- one common-control backbone rather than duplicated framework products;
- mission evidence, not issue closure, determines progress.

## Current completed/advanced foundation

The existing foundation and synthetic work has already established substantial reusable doctrine:

- positioning for Care and compliance-exposed suppliers;
- common-control backbone;
- Proof Ladder;
- AI Authority Matrix;
- requirement/control/implementation/evidence/review separation;
- synthetic Care and Supplier workflow findings;
- provider-neutral pilot-readiness/security boundaries;
- runtime acceptance contract;
- service-claim authority boundaries;
- lean shared data-resilience decision.

These are inputs to the mission. They are not themselves the finished product.

---

# Mission sequence

The central machine-readable Control contract determines the exact eligible gap and work order. The sequence below is the human-readable product roadmap.

## M1 — Freeze the minimum domain/data model

**Mission focus:** SS-SC-02, SS-SC-04, SS-SC-05, SS-SC-06.

Goal: define the smallest relational model that can run the managed-service workflow without later forcing avoidable data migrations.

Must define at minimum:

- tenant/organization/legal entity/organizational scope;
- user/membership/role;
- engagement/service variant;
- source/requirement/control/control assertion;
- client implementation;
- evidence/evidence version;
- assessment/finding/action;
- client request/response;
- AI proposal/provenance;
- professional review/decision/approval;
- report/approved assertion;
- audit event;
- recurring review/expiry state.

Design constraint:

`one shared Postgres + tenant_id + private object storage`.

Exit evidence:

- ER/domain model is coherent against Care + Supplier synthetic workflows;
- no entity merges concepts prohibited by the canonical traceability model;
- tenant isolation and lifecycle fields are explicit;
- no speculative enterprise entity families without workflow evidence.

## M2 — Prove the operator-led service workflow as the primary UX

**Mission focus:** SS-SC-01, SS-SC-02.

Goal: make the full concierge workflow executable from an operator perspective before polishing SaaS surfaces.

Prototype/workflow capabilities:

- operator-led intake;
- structured facts with provenance;
- evidence inbox;
- targeted client requests;
- controls/implementations/assessments;
- findings and remediation;
- AI proposal/review flow;
- professional review queue;
- baseline/recurring report generation.

Exit evidence:

- one synthetic Care dossier and one Supplier dossier can be executed end to end using the intended product flow;
- customer work is limited to required facts/evidence/decisions;
- professional reviewer can reconstruct material conclusions.

## M3 — Build the minimum secure runtime

**Mission focus:** SS-SC-04, SS-SC-05.

Goal: implement only the runtime primitives needed by M2.

Minimum runtime:

- shared PostgreSQL;
- Auth + memberships/roles;
- RLS/tenant authorization;
- private object storage;
- evidence hashes/versioning;
- audit events;
- scoped upload/action capabilities where required;
- nightly encrypted off-site database + object backup;
- simple monitoring;
- existing runtime acceptance tests.

Exit evidence:

- synthetic cross-tenant read/write/object tests fail closed;
- backup and restore work for structured state and evidence objects;
- no client data has been admitted before the broader real-client gate.

## M4 — Build the SolidSecurity Operator Workspace

**Mission focus:** SS-SC-02.

Goal: turn the service workflow into a coherent professional cockpit.

Primary views:

- client portfolio/status;
- intake and evidence inbox;
- control/implementation assessment;
- requests waiting on customer;
- actions/remediation;
- AI proposals;
- professional review queue;
- reports/approvals;
- recurring/expiry queue.

Exit evidence:

- operator can execute the full baseline without using GitHub or ad-hoc spreadsheets as the client dossier;
- the UI exposes provenance and authority state rather than hiding it.

## M5 — Build the Client Dashboard and Interaction Layer

**Mission focus:** SS-SC-01, SS-SC-03.

Goal: give the customer transparency without transferring the compliance workload to them.

Dashboard minimum:

- overview/current status;
- what is demonstrably arranged;
- attention points;
- actions and decisions required from customer;
- what SolidSecurity is working on;
- recently completed work;
- reports/evidence packs.

Interaction minimum:

- secure upload;
- short targeted questions;
- confirmations;
- approvals/sign-offs;
- email/link entry into those actions.

Exit evidence:

- a non-GRC customer user can identify current state and next required action without explanation of control IDs;
- all interaction writes back to the authoritative dossier.

## M6 — Controlled end-to-end pilot readiness

**Mission focus:** SS-SC-01 through SS-SC-07.

Before real client data:

- existing pilot/runtime gates are satisfied;
- tenancy, object access, AI boundaries, export/deletion and restore are tested;
- DPA/subprocessor/retention decisions are complete;
- professional authority roles are operational;
- repository/public-private/IP boundary is appropriate;
- explicit principal authorization for first real-client transition exists.

Then run a tightly bounded real pilot with high professional oversight.

Exit evidence:

- accepted baseline and recurring plan;
- customer can use dashboard/actions;
- measured delivery effort supports or falsifies the commercial model;
- no material authority or tenant-isolation failure.

## M7 — Improve unit economics from measured friction

**Mission focus:** SS-SC-08.

Automate only repeated work observed in pilots, for example:

- evidence extraction/classification;
- reusable approved assertions/questionnaire answers;
- evidence expiry/reminders;
- document/report drafting;
- request drafting;
- recurring review preparation.

Track professional effort and AI acceptance/modification/rejection so automation is chosen from evidence.

## M8 — Read-only technical evidence and continuous assurance

Only after managed-service workflow and real pilot value are proven.

Candidate connectors:

- Microsoft 365;
- Azure/AWS/GCP;
- GitHub;
- Cloudflare;
- Google Workspace;
- selected identity/security SaaS;
- Prowler as an evidence source where useful.

Invariant:

`observed configuration -> evidence -> assessment -> human-reviewed status`

Never:

`scanner pass -> automatic legal/compliance PASS`.

## M9 — Interoperability and scale

Only when customer/partner demand justifies it:

- auditor/partner access;
- APIs/MCP;
- OSCAL/compliance-as-code interoperability;
- sector packs beyond Care/Supplier;
- benchmark analytics using appropriately governed non-identifying data;
- white-label managed-service delivery.

---

# Explicitly deferred until mission evidence exists

- separate database/project per customer;
- active-active multi-cloud database;
- custom KMS/envelope-encryption platform;
- autonomous remediation/write access in client environments;
- broad framework imports because they exist;
- generic vulnerability-management platform;
- permanent vector memory for all evidence;
- multiple competing workflow/orchestration queues;
- AI-only assurance;
- replacement of external certification bodies.

## Repository visibility gate

Assume anything committed publicly may remain copied permanently. Public-safe methodology may remain public; real client information, secrets, proprietary evidence-sufficiency logic, private operating prompts and commercially sensitive accumulated intelligence do not belong in the public repo.

Before real-client processing or publication of material proprietary operating IP, perform the explicit public/private/open-core decision.
