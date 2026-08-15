# ADR 0009 — Conditionally prefer Supabase-first for the first client-data pilot

Status: `PROPOSED / CONDITIONAL / NOT DEPLOYMENT AUTHORITY`

## Context

Pilot Readiness requires a small client data plane with strong tenant isolation, private evidence objects, identity/MFA, auditability, lifecycle controls and a governed AI boundary. Raw infrastructure cost matters, but custom authorization/security implementation increases both delivery cost and risk.

Two minimal candidates were compared using current official provider documentation: Supabase-first and Cloudflare Workers + EU-jurisdiction D1/R2.

## Decision

Subject to upstream independent assurance and synthetic deployment proof, **prefer Supabase-first for the first real client-data pilot**.

Initial design preference:

- explicit EU Supabase region;
- project-per-client for the first small regulated customer set;
- RLS as defense in depth even with project separation;
- private Storage;
- Supabase Auth/MFA;
- application-level audit/provenance;
- no permanent vector store;
- Cloudflare remains suitable for public/edge delivery that does not require client evidence content.

## Why

Supabase maps directly to the Foundation's Postgres/RLS, private object and identity requirements and therefore requires less bespoke security code. Cloudflare's D1/R2 economics and EU jurisdiction controls are strong, but a Cloudflare-only client data plane would currently place more responsibility on SolidSecurity for external-user authentication and tenant authorization/routing.

## Important unresolved gate

Supabase Pro is inexpensive but does not provide organization Platform Audit Logs; those are currently a Team/Enterprise capability. Team pricing is materially higher. Before real client data, independent security/data-governance review must determine whether Team-level provider administration auditability/assurance evidence is required or whether documented compensating controls on a lower plan are acceptable.

This ADR does not make that risk-acceptance decision.

## Revisit triggers

- synthetic Supabase tenant/isolation/storage/MFA proof fails;
- provider DPA/region/retention review is unacceptable;
- Team-level operating cost materially breaks validated unit economics and compensating controls are not acceptable;
- client/project count makes project-per-client operations unreasonable;
- Cloudflare obtains/proves a materially simpler customer-identity/tenant authorization architecture for this use case;
- portability/export or regulatory requirements change.
