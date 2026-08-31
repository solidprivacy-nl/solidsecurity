# ADR 0009 — Conditionally prefer Supabase-first for the first client-data pilot

Status: `SUPERSEDED_IN_PART_BY_ADR_0011 / PROVIDER_COMPARISON_REMAINS_CONDITIONAL / NOT_DEPLOYMENT_AUTHORITY`

> **Current architecture note:** ADR 0011 supersedes the tenancy portion of this decision. The active V1 default is one shared multi-tenant PostgreSQL data plane with explicit `tenant_id`, server-side authorization and RLS/equivalent defense in depth. The earlier project-per-client preference below is retained only as decision history and must not be treated as current architecture.

## Context

Pilot Readiness requires a small client data plane with strong tenant isolation, private evidence objects, identity/MFA, auditability, lifecycle controls and a governed AI boundary. Raw infrastructure cost matters, but custom authorization/security implementation increases both delivery cost and risk.

Two minimal candidates were compared using current official provider documentation: Supabase-first and Cloudflare Workers + EU-jurisdiction D1/R2.

## Decision

Subject to upstream independent assurance and synthetic deployment proof, **Supabase-first remains the conditionally preferred provider candidate for the first real client-data pilot**.

The original tenancy preference in this ADR was project-per-client. That portion is now superseded by ADR 0011. If Supabase is selected, the current V1 architecture uses one shared PostgreSQL data plane for normal clients, with explicit tenant ownership and RLS/application authorization.

Provider-level design preferences that remain applicable:

- explicit EU Supabase region;
- private Storage;
- Supabase Auth/MFA;
- application-level audit/provenance;
- no permanent vector store;
- Cloudflare remains suitable for public/edge delivery that does not require client evidence content.

## Why

Supabase maps directly to the Foundation's Postgres/RLS, private object and identity requirements and therefore requires less bespoke security code. Cloudflare's D1/R2 economics and EU jurisdiction controls are strong, but a Cloudflare-only client data plane would currently place more responsibility on SolidSecurity for external-user authentication and tenant authorization/routing.

ADR 0011 later established that separate provider projects/databases per client add avoidable operational complexity for the intended managed service unless a concrete customer, risk, scale or isolation requirement justifies dedicated tenancy.

## Important unresolved gate

Supabase Pro is inexpensive but does not provide organization Platform Audit Logs; those are currently a Team/Enterprise capability. Team pricing is materially higher. Before real client data, independent security/data-governance review must determine whether Team-level provider administration auditability/assurance evidence is required or whether documented compensating controls on a lower plan are acceptable.

This ADR does not make that risk-acceptance decision.

## Revisit triggers

- synthetic shared-tenant isolation/storage/MFA proof fails;
- provider DPA/region/retention review is unacceptable;
- Team-level operating cost materially breaks validated unit economics and compensating controls are not acceptable;
- a concrete customer or threat model requires dedicated infrastructure;
- Cloudflare obtains/proves a materially simpler customer-identity/tenant authorization architecture for this use case;
- portability/export or regulatory requirements change.
