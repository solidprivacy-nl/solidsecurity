# ADR 0011 — Independent encrypted recovery copy

Status: `PROPOSED`

## Context

SolidSecurity will hold sensitive compliance evidence and governed client state. Primary-provider encryption and replication reduce some risks but do not by themselves provide an independent recovery path for account/provider failure, malicious deletion or incomplete object backup. Supabase database backups also do not contain the underlying Storage object bytes.

The service must remain economical for small care organizations and SMEs, so always-on multi-cloud databases and premium PITR for every tenant would be disproportionate at the first-pilot stage.

## Decision

1. Retain the conditional Supabase-first, project-per-client design for early regulated clients.
2. Store structured state in Postgres and evidence bytes in private object storage; do not store large evidence blobs in Postgres.
3. Treat evidence versions as immutable and content-addressed by recorded SHA-256 integrity metadata.
4. Require provider encryption at rest and TLS for all client-data stores.
5. Require encrypted independent logical database backups outside the primary provider/failure domain.
6. Maintain an independent secondary copy of persisted evidence versions outside the primary provider/failure domain; Cloudflare R2 is the current recovery-store candidate.
7. Keep cryptographic key-management as a separate provider-neutral service boundary. Higher-sensitivity evidence must support application-layer authenticated/envelope encryption unless an equivalent governed architecture is approved.
8. Use configurable retention and limited bucket-lock/WORM protection where appropriate; never default to undisclosed indefinite retention.
9. Consider a backup valid only after integrity verification and periodic restore testing.
10. Use recovery profiles so more expensive PITR/continuous recovery is purchased only when a proven/contracted RPO requires it.

## Consequences

### Positive

- reduces primary-provider/account blast radius;
- protects evidence bytes independently from database backup behavior;
- improves ransomware/malicious-deletion recovery;
- preserves provider portability;
- keeps the baseline economically small;
- makes recovery an auditable tested property rather than a vendor checkbox.

### Costs / complexity

- requires backup orchestration and monitoring;
- requires retention/deletion coordination across primary and recovery stores;
- envelope encryption introduces key lifecycle/recovery obligations;
- project-per-client isolation creates migration/operations automation needs as tenant count grows.

## Rejected alternatives

**Primary provider only.** Rejected as the sole recovery strategy because it does not provide an independent failure domain and does not separately solve object recovery.

**Active-active multi-cloud database.** Rejected for V1 as disproportionate operational complexity and cost.

**PITR for every client by default.** Rejected as a blanket rule; enable only where RPO/business impact justifies it.

**One shared multi-tenant database immediately.** Rejected for the early regulated pilot because reducing blast radius is worth the modest project overhead while authorization code and service workflows are still maturing.

## Review trigger

Revisit this ADR when:

- early-client project operations become materially burdensome;
- a customer requires a different RPO/RTO or dedicated infrastructure;
- the chosen KMS/storage provider changes materially;
- restore testing shows the architecture cannot meet the intended recovery profile;
- consolidation into a shared multi-tenant runtime is proposed.
