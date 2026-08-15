# ADR 0011 — Shared data plane with simple off-site backup

Status: `PROPOSED`

## Context

SolidSecurity needs secure storage for multiple client dossiers, evidence objects and operational state. The earlier design considered a separate Supabase project per client, application-level envelope encryption, a dedicated KMS boundary, multiple recovery profiles and a fixed secondary recovery provider.

For the intended managed service this creates avoidable operational complexity before a concrete risk or customer requirement justifies it.

## Decision

1. Use one shared PostgreSQL database for normal SolidSecurity tenants.
2. Put `tenant_id` on client-owned records and enforce tenant isolation through authenticated server context plus RLS or equivalent defense in depth.
3. Store evidence bytes in one private object store using opaque tenant/evidence/version keys; do not store large files as Postgres blobs.
4. Do not silently overwrite reviewed evidence; changed content creates a new version/hash.
5. Use TLS and provider-managed encryption at rest as the V1 encryption baseline.
6. Do not build application-level envelope encryption or a dedicated KMS subsystem by default.
7. Run a simple nightly backup job that creates a PostgreSQL logical backup and backs up/synchronizes evidence objects.
8. Encrypt portable backup material and transfer it to an independent inexpensive storage target using a standard mechanism such as SFTP or S3-compatible sync tooling.
9. Make a third low-frequency copy optional rather than mandatory.
10. Periodically prove database and evidence restoration. A successful backup job alone is not recovery proof.
11. Add dedicated infrastructure, shorter RPO, stronger cryptography or more redundancy only when a concrete risk, customer contract, scale limit or recovery test justifies it.

## Why

This design minimizes moving parts while retaining the controls that materially matter:

- strong tenant isolation;
- private evidence access;
- evidence integrity/versioning;
- encrypted off-site backup;
- independence from the primary failure domain;
- tested restoration;
- low operational cost.

It also avoids multiplying schemas, migrations, credentials and provider projects as the customer base grows.

## Consequences

### Positive

- one schema and migration path;
- substantially simpler operations;
- low idle infrastructure cost;
- easier monitoring and backup;
- conventional SaaS tenancy model;
- clear escalation path when a future customer genuinely needs more isolation.

### Risks

- a shared database creates a larger blast radius if tenant authorization is defective;
- therefore cross-tenant negative tests and RLS/authorization review are mandatory;
- a nightly backup implies a recovery point that may be insufficient for some future service commitments.

## Rejected as V1 defaults

- database/project per client;
- active-active multi-cloud databases;
- custom KMS/envelope-encryption stack;
- real-time cross-provider replication;
- several recovery tiers before demand exists;
- one fixed backup provider as an architectural dependency.

## Review triggers

Revisit this ADR when a customer requires dedicated infrastructure, recovery requirements become materially shorter than nightly, scale makes shared tenancy unsuitable, a threat model requires stronger cryptographic separation, or restore testing exposes a material weakness.
