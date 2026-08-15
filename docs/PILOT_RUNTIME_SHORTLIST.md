# Pilot Runtime Shortlist V1

Status: `DESIGN EVALUATION / CONDITIONAL PREFERENCE / NO DEPLOYMENT AUTHORITY`

Last source verification: 2026-08-15.

## Decision in one sentence

**Conditional preference: Supabase-first, initially with stronger project-per-client isolation, because it removes more custom security code from the first regulated pilot.** Cloudflare remains the preferred public/edge platform and a credible low-cost alternative data plane, but a Cloudflare-only client data plane currently requires more application-auth/tenant-isolation engineering than the pilot should carry.

This is not final provider authorization. The upstream Pilot Readiness gate, DPA/subprocessor review, exact security design and independent security/data-governance review remain mandatory before real client data.

## Why only two candidates

The target is not to optimize the cloud architecture. It is to obtain the smallest credible runtime for:

- structured client compliance state;
- private evidence objects;
- attributable human/agent access;
- tenant isolation;
- AI-assisted proposed output;
- professional review;
- export/deletion/auditability.

Adding AWS/Azure plus separate auth/storage products at this point would increase operating surface without solving an unmet pilot requirement.

---

# Candidate A — Supabase-first

## Proposed shape

```text
Public website/static assets (may remain Cloudflare)
                 |
                 | no client evidence bodies required here
                 v
         SolidSecurity application
                 |
      approved server/client path
                 v
        Supabase EU project(s)
  ┌──────────────┼──────────────┐
  v              v              v
Postgres       Auth/MFA      Private Storage
  |                              |
  +------ application audit -----+
                 |
                 v
        explicit AI selection
                 |
                 v
          PROPOSED output
                 |
                 v
        professional review
```

### Recommended early-tenancy pattern

For the first small number of real customers, prefer **one Supabase project per client** rather than immediately optimizing for a shared multi-tenant database.

Even with project-per-client isolation:

- keep `tenant_id` on client-plane objects for portability and application invariants;
- enable RLS on every exposed table as defense in depth;
- use private Storage buckets and RLS;
- use tenant/project-scoped service credentials;
- maintain a separate private operations registry containing only project/tenant routing metadata, not client evidence.

A shared multi-tenant Supabase project can be reconsidered after automated cross-tenant tests and real operating economics justify consolidation.

## Fit against requirements

### Strong fit

**Relational and authorization model.** Supabase provides Postgres RLS. This directly matches the Foundation's deny-by-default tenant model and allows authorization rules to live in the database as defense in depth.

**Evidence objects.** Supabase Storage buckets are private by default and Storage access can be governed with Postgres RLS. Signed time-limited download URLs are available.

**Identity.** Supabase Auth integrates with RLS and supports application MFA, including TOTP/phone factors and AAL claims that can be enforced in database/API authorization.

**EU deployment.** Projects can be created in explicit European AWS regions including Frankfurt (`eu-central-1`), Paris, Ireland, Stockholm and others.

**Portability.** Core structured state remains Postgres. Storage exposes common S3-compatible patterns. This is materially less proprietary than designing the core around provider-specific state primitives.

**Provider assurance.** Supabase states that the platform is SOC 2 Type 2 compliant and announced ISO/IEC 27001:2022 certification across Database, Auth, Storage, Realtime, Edge Functions and Data API.

## Material caveats

### 1. Pro versus Team is a real business/security decision

Current public pricing starts at approximately:

- Pro: `$25/month`, first project included; additional default-size projects from about `$10/month`;
- Team: `$599/month`, first project included; additional projects from about `$10/month`.

Pro includes daily database backups retained for 7 days and 7-day platform log retention. Team adds, among other things, Platform Audit Logs, longer log/backup retention, more organization access controls and access to SOC 2 / ISO 27001 compliance materials in the pricing offering.

**Pilot rule:** Pro is suitable for synthetic/development work. It is **not automatically approved for real client data** merely because it is inexpensive. Before the first real dossier, the security/data-governance review must decide whether Team-level provider administrative auditability and assurance evidence are mandatory or whether explicit compensating controls on Pro are sufficient.

No AI/implementation actor may make that risk acceptance itself.

### 2. Database backups do not back up Storage objects

Supabase's database-backup documentation explicitly notes that database backups contain Storage metadata, not the underlying stored objects. Therefore SolidSecurity must define evidence-object recovery/versioning/export separately and test it. A green database restore is not a green evidence-store restore.

### 3. RLS is powerful but configuration-sensitive

RLS must be enabled on every exposed table; an authenticated role alone is not tenant authorization. Service-role keys bypass RLS and therefore belong only in server-side secret management with narrowly controlled use. Views/functions require their own security review.

### 4. Provider certification is not SolidSecurity certification

Provider SOC 2/ISO status is supplier evidence. It does not transfer compliance to SolidSecurity or its clients.

## Indicative low-volume economics

Using currently published list pricing and default-size projects, before usage/add-ons/tax:

| Client projects | Pro organization | Team organization |
|---:|---:|---:|
| 1 | about $25/mo | about $599/mo |
| 10 | about $115/mo | about $689/mo |
| 50 | about $515/mo | about $1,089/mo |

These figures are architecture comparisons, **not a budget commitment**. They assume one default-size project per client, one organization, the current included compute credit/first-project economics and no material overages/PITR/add-ons. Actual billing must be revalidated before purchase.

At 10 clients, a Team base becomes roughly $69/client/month before usage; at 50 roughly $22/client/month. This makes stronger provider-governance features economically more plausible as the managed service scales.

---

# Candidate B — Cloudflare-partitioned client data plane

## Proposed shape

```text
Cloudflare Access (internal professionals)
                 |
                 v
             Workers
        ┌────────┴────────┐
        v                 v
   D1 metadata         R2 evidence
 EU jurisdiction      EU jurisdiction
        |                 |
        +------ audit ----+
                 |
                 v
        explicit AI boundary
```

The first pilot would deliberately avoid building a full customer account/portal system. Client evidence ingress would need a tightly scoped upload/request mechanism; internal professional workspace access can be protected by Cloudflare Access. A broader external-user identity model would be a later product requirement.

## Strong fit

**EU storage jurisdiction.** Both D1 and R2 currently support an `eu` jurisdiction that constrains where the database/object data runs/is stored. This is stronger than relying on a best-effort Western Europe location hint.

**Low idle cost.** Workers Paid currently starts at `$5/month`; D1 scales to zero and includes substantial read/write allowances on Paid. R2 standard storage is `$0.015/GB-month` with a 10 GB monthly free tier and no Internet egress charges.

**Evidence-object economics.** R2 is attractive for compliance evidence because storage is inexpensive, objects can be large, and bucket capacity/object count is effectively not a small-pilot constraint. Current account limit is up to 1,000,000 buckets.

**Isolation options.** D1 Paid supports up to 50,000 databases, each currently up to 10 GB. R2 allows very large numbers of buckets. This makes per-client physical/logical partitioning conceptually possible.

**Internal identity.** Cloudflare Access/Zero Trust can protect internal operator applications and supports service-token identities for automation.

## Material caveats

### 1. D1 does not give us Postgres RLS

D1 uses SQLite semantics. A shared D1 database would therefore place more tenant-authorization responsibility in application code than the Foundation preference.

Per-client D1 databases/buckets reduce blast radius, but dynamic resource routing and credential scope must be designed carefully. A broad account token that can reach every tenant resource would reintroduce a large blast radius.

This makes Cloudflare-only less attractive for the **first** client-data implementation unless the runtime is deliberately per-tenant/deployment-partitioned and negative isolation testing proves the routing boundary.

### 2. Customer identity is not solved by D1/R2

Cloudflare Access is excellent for workforce/internal access but is not by itself the complete customer-portal authorization model specified in `ACCESS_AND_TENANCY.md`. Avoid solving this by inventing our own password/authentication system in the first pilot.

### 3. EU D1/R2 does not automatically mean all request processing/logging is EU-only

D1/R2 jurisdiction controls those data stores. Cloudflare documentation separately describes Regional Services and Customer Metadata Boundary for restricting request processing/TLS inspection and customer logs. Entitlements/configuration must be verified before making an end-to-end EU-processing claim.

### 4. More security behavior becomes our code

Tenant routing, external-user authorization, object authorization and some audit semantics are more bespoke than in the Supabase-first option. Cheap infrastructure is not cheaper if it creates material security engineering/review burden.

## Indicative low-volume economics

At current public rates, Workers Paid begins at $5/month; D1 Paid includes the first 25 billion rows read, 50 million rows written and 5 GB storage per month before usage pricing; R2 includes 10 GB-month of Standard storage, 1 million Class A operations and 10 million Class B operations before usage charges.

For a low-volume pilot, base platform cost could therefore remain in the low tens of dollars monthly. **This estimate excludes any Data Localization Suite entitlement, external identity/provider cost, support tier, AI/model usage and security/compliance commercial requirements.**

---

# Weighted decision

Weights reflect a regulated managed-service pilot, not a generic SaaS app.

| Criterion | Weight | Supabase-first | Cloudflare-partitioned |
|---|---:|---:|---:|
| Tenant isolation / authorization fit | 25 | 5 | 3.5 |
| EU data-location controllability | 15 | 4.5 | 4.5 |
| Identity/MFA fit | 10 | 5 | 3 |
| Evidence-object access/lifecycle | 10 | 4.5 | 4 |
| Auditability/provenance fit | 15 | 4 on Team / 3 on Pro | 3.5 |
| Operational simplicity for first pilot | 10 | 4.5 | 3 |
| First-tenants infrastructure economics | 10 | 3 Pro / 1.5 Team | 5 |
| Portability / avoidance of bespoke lock-in | 5 | 4 | 3 |

Qualitative conclusion: **Supabase-first wins on security primitives and implementation simplicity; Cloudflare-partitioned wins decisively on raw infrastructure cost.** For SolidSecurity, reducing custom authorization/security code is worth more in Phase 2 than minimizing a few hundred dollars of fixed cloud spend.

---

# Conditional architecture recommendation

## Preferred first-pilot path

1. Use Supabase as the **client data plane** candidate.
2. Choose an explicit EU project region; Frankfurt is the default evaluation assumption, not yet an authorized deployment.
3. Start with **project-per-client** isolation for the first regulated pilots.
4. Keep RLS on all exposed tables anyway.
5. Use private Storage with tenant/project-scoped policy.
6. Require application MFA for privileged/reviewer/client-admin roles.
7. Keep an application-level immutable/append-oriented audit/event model independent of provider platform logs.
8. Keep Cloudflare for public website/edge functions that do not need client evidence bodies; do not automatically proxy sensitive evidence through Cloudflare merely because the website is hosted there.
9. Before real client data, decide Pro vs Team through the explicit readiness/risk-review gate.
10. Do not introduce embeddings/vector storage in the first pilot.

## Why project-per-client first

This is intentionally conservative. It gives each early client a separate database/Auth/Storage boundary while the service model is still changing. The incremental default-project cost is low compared with professional service fees. It also reduces the consequence of an RLS policy defect.

Later, if 50+ tenants make project operations cumbersome, SolidSecurity can evaluate a shared Postgres tenancy model with mature automated RLS/isolation tests. The canonical domain objects retain `tenant_id`, so this does not require changing the business model.

---

# Go / no-go proof tests

No provider wins based on a paper comparison. Before final selection, a **synthetic deployment proof** must pass the same functional security scenarios.

## Supabase candidate proof

- create two synthetic client projects and prove cross-project credentials cannot retrieve the other project;
- within one synthetic project, deliberately create two tenant IDs and prove RLS negative tests for every client-plane table;
- prove private Storage object isolation, signed-link expiration and unauthorized list/read denial;
- prove MFA/AAL enforcement for a protected reviewer action;
- prove service-role credentials never enter browser/client logs and are scope-controlled in server runtime;
- prove evidence object version/hash + export/delete flow;
- prove database restore and separately prove evidence-object recovery/export because DB backups do not restore objects;
- verify actual region and DPA/subprocessor/retention settings;
- decide and document Pro-vs-Team auditability before real-data authorization.

## Cloudflare candidate proof

- create two synthetic tenant partitions and prove no shared credential/routing path can read/write both without an explicitly audited platform-admin action;
- prove D1 and R2 resources were created with `eu` jurisdiction rather than location hints;
- prove R2 object access is private and capability/upload links cannot be replayed/escalated outside scope;
- prove internal Access identity and agent service tokens are attributable/revocable;
- prove D1/R2 backup/recovery/export/delete lifecycle;
- demonstrate tenant-routing negative tests under concurrency/background jobs;
- determine exact Regional Services/Customer Metadata Boundary needs and commercial entitlement before any end-to-end EU-processing statement;
- demonstrate how future client-admin authentication is added without a custom password system.

Failure of a material isolation/data-location/audit test is `NO-GO`, not an invitation to weaken the Pilot Readiness requirements.

---

# Official source snapshot

Sources are not embedded requirements and must be reverified before implementation/purchase.

## Supabase

- Regions: `https://supabase.com/docs/guides/platform/regions`
- Pricing: `https://supabase.com/pricing`
- RLS: `https://supabase.com/docs/guides/database/postgres/row-level-security`
- Storage access: `https://supabase.com/docs/guides/storage/security/access-control`
- Private buckets: `https://supabase.com/docs/guides/storage/buckets/fundamentals`
- Auth MFA: `https://supabase.com/docs/guides/auth/auth-mfa`
- Platform audit logs: `https://supabase.com/docs/guides/security/platform-audit-logs`
- Database backups: `https://supabase.com/docs/guides/platform/backups`
- SOC 2: `https://supabase.com/docs/guides/security/soc-2-compliance`
- ISO 27001 announcement: `https://supabase.com/blog/supabase-is-now-iso-27001-certified`

## Cloudflare

- Workers pricing: `https://developers.cloudflare.com/workers/platform/pricing/`
- D1 pricing: `https://developers.cloudflare.com/d1/platform/pricing/`
- D1 limits: `https://developers.cloudflare.com/d1/platform/limits/`
- D1 data location: `https://developers.cloudflare.com/d1/configuration/data-location/`
- R2 pricing: `https://developers.cloudflare.com/r2/pricing/`
- R2 limits: `https://developers.cloudflare.com/r2/platform/limits/`
- R2 data location: `https://developers.cloudflare.com/r2/reference/data-location/`
- Data Localization: `https://developers.cloudflare.com/data-localization/`
- Access service tokens: `https://developers.cloudflare.com/cloudflare-one/access-controls/service-credentials/service-tokens/`
- GDPR / trust: `https://www.cloudflare.com/trust-hub/gdpr/`
