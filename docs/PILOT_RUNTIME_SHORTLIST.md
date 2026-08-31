# Pilot Runtime Shortlist V1

Status: `CONDITIONAL EVALUATION / NO DEPLOYMENT AUTHORITY`

Last source verification: 2026-08-15. Provider facts and pricing must be reverified before purchase or deployment.

## Current decision

SolidSecurity has two credible first-pilot runtime candidates:

1. **Supabase-first — conditionally preferred provider candidate.**
2. **Cloudflare-partitioned — credible low-cost alternative.**

The tenancy decision is **not** part of this provider choice anymore. ADR 0011 is authoritative for V1 tenancy:

- one shared multi-tenant PostgreSQL database for normal clients;
- explicit `tenant_id` ownership;
- server-side authorization plus RLS/equivalent defense in depth;
- one private evidence/object store;
- no database/project per customer by default.

ADR 0009 records the earlier project-per-client preference as superseded decision history.

No provider is selected for real client data by this document. Pilot Readiness, DPA/subprocessor review, synthetic security proof, independent security/data-governance review and explicit real-pilot authorization remain mandatory.

## Evaluation principles

Choose the smallest runtime that demonstrably supports:

- tenant-isolated structured client state;
- private evidence objects;
- attributable human and agent identities;
- MFA for material reviewer actions;
- governed AI proposals and professional review;
- export, deletion, backup and restore;
- audit/provenance;
- explicit EU data-location requirements where applicable.

Do not optimize raw cloud cost at the expense of bespoke security code. Do not add providers or services unless they solve a demonstrated requirement better.

## Candidate A — Supabase-first

### Why it currently leads

Supabase maps closely to the required V1 primitives:

- PostgreSQL;
- RLS;
- integrated Auth/MFA;
- private object storage;
- explicit EU regions;
- conventional SQL portability;
- less custom tenant/authentication security code than a Cloudflare-only data plane.

If selected, SolidSecurity uses the shared-tenancy architecture from ADR 0011 rather than the superseded project-per-client approach.

### Material unresolved gates

- confirm exact EU region and contractual/data-processing fit;
- prove RLS and application authorization with at least two synthetic tenants;
- prove private Storage isolation and expiring access;
- prove MFA/AAL enforcement for material reviewer actions;
- prove evidence-object recovery separately from database recovery;
- decide whether Pro-level provider administration auditability is sufficient or Team-level capabilities are required;
- verify secrets/service-role handling;
- obtain independent security/data-governance PASS before real client data.

### Cost position

Supabase is not selected on list price alone. Pro is low-cost; Team is materially more expensive. Exact pricing and required plan features must be revalidated when a real pilot is ready. Shared tenancy avoids multiplying provider projects merely because customer count grows.

## Candidate B — Cloudflare-partitioned

### Why it remains credible

Cloudflare offers:

- very low idle-cost Workers/D1/R2 economics;
- EU-jurisdiction controls for D1/R2;
- strong public/edge hosting;
- private object storage;
- Cloudflare Access for internal operator identity.

### Why it does not currently lead

A Cloudflare-only client data plane requires more SolidSecurity-owned security behavior:

- D1 does not provide PostgreSQL RLS;
- tenant authorization/routing becomes more application-specific;
- broad customer identity is not solved by D1/R2 or workforce Access;
- end-to-end EU-processing claims require more than D1/R2 jurisdiction alone.

Cheap infrastructure is not simpler if it creates more custom authentication, authorization or tenant-routing code.

### Material unresolved gates

- prove tenant-routing negative tests under foreground and background execution;
- prove least-privileged D1/R2 access and private evidence access;
- define bounded customer ingress/authentication without inventing a password system;
- verify exact Regional Services/log-boundary requirements;
- verify DPA/subprocessor fit;
- obtain independent security/data-governance PASS before real client data.

## Comparative view

| Dimension | Supabase-first | Cloudflare-partitioned |
|---|---|---|
| Shared relational model | Strong — PostgreSQL | Weaker — D1/SQLite semantics |
| Tenant authorization | Strong — RLS + application | More application-owned |
| Identity/MFA | Strong integrated fit | Strong for operators; client identity incomplete |
| Evidence storage | Strong private Storage fit | Strong R2 fit |
| EU data-location control | Explicit EU regions | D1/R2 EU jurisdiction |
| Auditability | Plan-dependent + application provenance | More application/configuration dependent |
| Operational simplicity | Better current fit | More custom security/routing work |
| Raw infrastructure cost | Higher | Lower |
| Current position | **Conditionally preferred** | **Alternative** |

## Provider-neutral go/no-go proof

No provider wins on paper. Before a final selection, the exact synthetic deployment candidate must prove the existing Runtime Acceptance Contract, including at minimum:

1. cross-tenant metadata read/write denial;
2. private evidence-object isolation and scoped/expiring access;
3. MFA for material reviewer actions;
4. agent denial from human-only decisions;
5. evidence version/hash integrity;
6. high-sensitivity external-LLM deny-by-default;
7. no cross-tenant retrieval or memory;
8. export and deletion lifecycle;
9. database and evidence-object recovery;
10. secret/log minimization;
11. background-job tenant context;
12. actual region/jurisdiction verification;
13. synthetic incident/tabletop evidence.

A material FAIL or INDETERMINATE blocks real client data. Provider documentation never substitutes for implementation evidence.

## Authority boundaries

This shortlist authorizes none of the following:

- provider project/resource creation for production;
- real client data;
- DPA or provider-contract acceptance;
- final legal/data-residency conclusions;
- production deployment;
- autonomous compliance, certification or security verdicts.

## Source snapshot

The 2026-08-15 comparison used official Supabase and Cloudflare documentation for regions/jurisdiction, pricing, RLS/storage, MFA, audit logs, backups, D1/R2 limits and data-location controls. Those facts are implementation inputs, not permanent architecture. Reverify them at the real provider-selection gate.
