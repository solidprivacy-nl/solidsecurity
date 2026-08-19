# SolidSecurity Roadmap

## Roadmap doctrine

Build the **operating model before the platform**, prove the **service before the integrations**, and introduce automation only where it reduces verified work rather than creating unverified complexity.

## Phase 0 — Foundation V1

**Status: IN PROGRESS — issue #2**

Deliver:

- target positioning and service boundaries;
- common-control model;
- conceptual data model;
- Proof Ladder;
- AI authority model;
- care and supplier workflows;
- open-source adoption register;
- source/licensing registry;
- public-repo information classification;
- architecture and ADRs;
- roadmap and commercial hypotheses.

Exit gate:

- coherent candidate in PR;
- independent governance/release assurance;
- no contradiction with project assurance contract.

## Phase 1 — Service MVP / synthetic execution

Goal: prove that the full managed-service workflow works **without** building a GRC platform.

Work packages:

1. create a synthetic small home-care organization dossier;
2. define Care Baseline V1 control subset;
3. execute intake → facts → scope → assessment → evidence requests → gaps → 90-day plan → policies → professional review → baseline report;
4. create synthetic SME supplier dossier;
5. execute security questionnaire/passport workflow;
6. measure AI versus professional effort at each step;
7. capture failure modes and review burden;
8. refine common controls/evidence expectations.

No real customer data. No environment connectors.

Exit gate:

- two end-to-end synthetic cases reproducible;
- professional reviewer can reconstruct each material conclusion;
- initial unit-economics model based on measured workload.

## Phase 2 — Controlled pilot readiness

Goal: become safe enough for first real pilot customer.

Before any real client data:

- client data-plane ADR;
- tenant isolation design;
- retention/deletion rules;
- DPA/subprocessor model;
- LLM/data-processing policy;
- secrets management;
- access control and audit logging;
- incident response for SolidSecurity itself;
- client export/offboarding model;
- public/private repository transition decision.

Then run one or a few tightly bounded pilot customers with manual evidence intake.

Exit gate:

- data governance independently reviewed;
- first pilot produces an accepted baseline and recurring plan;
- measured professional hours support viable pricing.

## Phase 3 — Productize the proven workflow

Goal: remove operational friction, not recreate a broad enterprise GRC suite.

Candidate capabilities:

- secure tenant workspace;
- control/evidence register;
- action/remediation tracker;
- professional review queue;
- document generation/versioning;
- recurring review scheduler;
- customer status dashboard;
- Supplier Security & Compliance Passport;
- questionnaire ingest/reuse workflow;
- structured audit-ready export.

Decision gate: custom thin app vs Probo/hybrid.

## Phase 4 — Read-only technical evidence

Only after service-model validation.

Candidate connectors:

- Microsoft 365;
- Azure/AWS/GCP where relevant;
- GitHub;
- Cloudflare;
- Google Workspace;
- selected SaaS identity/security systems.

Evaluate Prowler as an evidence provider rather than a full SolidSecurity runtime.

Principle:

`observed configuration -> evidence -> assessment -> human-reviewed status`

Never:

`scanner pass -> automatic legal/compliance PASS`

## Phase 5 — Continuous assurance

Goal: evolve from periodic managed compliance to event- and evidence-driven maintenance.

Capabilities:

- evidence expiry/refresh;
- configuration drift signals;
- regulatory/source change monitoring;
- supplier review cycles;
- AI-use inventory drift;
- recurring control effectiveness checks;
- automated audit-pack preparation;
- exception-based professional review.

## Phase 6 — Interoperability and scale

Evaluate only when customer/partner demand justifies it:

- OSCAL/compliance-trestle interoperability;
- richer APIs/MCP;
- partner/auditor access;
- sector packs beyond care;
- benchmark/portfolio analytics;
- white-label managed-service delivery.

## Explicitly deferred

- autonomous remediation in customer systems;
- continuous write access to customer environments;
- importing 100+ frameworks because they exist;
- building a generic vulnerability-management platform;
- replacing external certification bodies;
- AI-only assurance.

## Repository-visibility gate

Public is acceptable during Foundation/Service-MVP while only public-safe methodology and synthetic material are stored. Before Phase 2 real-client processing or before proprietary mappings/evidence rubrics become material IP, perform a formal visibility/split decision:

1. keep public core + create private operations/control repo; or
2. move this repository private; or
3. establish an explicit open-core licensing strategy.

Assume anything committed publicly may remain copied or forked even after later privatization.
