# Data Resilience Architecture V1

Status: `DESIGN / NO REAL CLIENT DATA AUTHORITY`

## Purpose

Define the simplest architecture that is demonstrably secure, tenant-isolated, backed up and recoverable for the SolidSecurity managed service.

The design principle is explicit:

> Use the least complex architecture that satisfies a concrete risk or service requirement. Add isolation, redundancy or cryptography only when evidence shows the simpler design is insufficient.

## Architecture in one view

```text
GitHub Control Plane
method / schemas / software / mission
          |
          v
SolidSecurity Application
operator workspace + client dashboard
          |
          v
ONE shared client data plane
+-----------------------------------+
| PostgreSQL                        |
| - all tenants                     |
| - tenant_id on client data        |
| - server authorization + RLS      |
|                                   |
| Private object storage            |
| - evidence / attachments          |
| - tenant-scoped object keys       |
+----------------+------------------+
                 |
                 | nightly backup job
                 v
Encrypted off-site backup
cheap independent storage target
(SFTP/S3-compatible/commodity storage)
                 |
                 +--> optional third copy later
```

## 1. One shared database

SolidSecurity uses one PostgreSQL database for the normal multi-client service unless a concrete customer or regulatory requirement later justifies dedicated infrastructure.

Every tenant-owned domain record contains a `tenant_id`. Tenant context is derived from authenticated authorization context and must not be trusted solely from request parameters.

Row Level Security or an equivalent database-enforced mechanism is defense in depth. Automated negative tests must prove that a tenant cannot read or mutate another tenant's records.

Benefits of the shared model:

- one schema and migration path;
- one operational database to monitor and back up;
- lower infrastructure cost;
- simpler development and support;
- no per-customer project, secret or configuration sprawl.

## 2. One primary private object store

Large evidence files and attachments are stored in private object storage, not as Postgres blobs.

Recommended opaque object identity:

`tenants/{tenant_uuid}/evidence/{evidence_uuid}/versions/{version_uuid}.bin`

Object keys do not contain client names, personal names or descriptive sensitive filenames. Human-readable filenames and metadata live in Postgres.

Reviewed evidence is never silently overwritten. Changed content creates a new version and content hash so a prior professional conclusion remains bound to the exact evidence version it used.

## 3. Baseline encryption

V1 deliberately avoids a custom application cryptography subsystem.

Required baseline:

- TLS in transit;
- provider-managed encryption at rest for database and primary storage;
- private object access;
- encrypted backup archives before or during transfer to the off-site target;
- secrets outside GitHub and normal logs;
- least-privilege backup credentials.

Application-level envelope encryption, customer-managed keys or dedicated KMS architecture are later options only when a threat model, customer contract or regulation materially requires them.

## 4. Simple off-site backup

A single scheduled backup job is the default resilience mechanism.

Nightly flow:

1. create a consistent PostgreSQL logical backup;
2. capture new/changed evidence objects or a storage snapshot/export;
3. produce checksums/manifest metadata;
4. encrypt the backup set;
5. transfer it to an independent low-cost storage environment using a standard mechanism such as SFTP, S3-compatible sync, `rclone`, `restic` or an equivalent commodity tool;
6. record success/failure and alert when the job is late or fails.

The architecture does not require Cloudflare R2, a dedicated backup SaaS or any specific transport. Provider choice is replaceable.

An optional third copy may later be added cheaply, for example weekly or monthly, if the incremental benefit justifies the small operational cost.

## 5. Backup must be recoverable

A successful copy command is not sufficient evidence of resilience.

At minimum SolidSecurity periodically proves:

- a database backup can be restored;
- evidence objects can be restored;
- restored file hashes match the source manifest;
- a synthetic client dossier can be reconstructed;
- restoration does not expose another tenant's data.

These tests can be simple and infrequent initially. The purpose is to prove usability, not build a disaster-recovery platform.

## 6. Retention and deletion

Retention is policy/configuration driven by contract, data category and applicable obligations. No universal duration is hard-coded.

Deletion must account for both primary data and the normal backup-expiry window. A client must not be told that all recoverable copies are gone while ordinary retained backups still exist.

## 7. Provider position

Supabase/Postgres remains a reasonable candidate for the primary shared data plane because it combines PostgreSQL, Auth and private Storage with RLS-capable authorization.

The independent backup target should be selected primarily on:

- low cost;
- independent credentials/failure domain;
- EU/data-location suitability where required;
- standard automated transfer support;
- reliable retention and retrieval.

No second live database is required.

## Non-goals for V1

- database per client;
- active-active or multi-cloud database replication;
- custom KMS/envelope-encryption infrastructure;
- real-time cross-provider object replication;
- multiple RPO/RTO service tiers before customer demand exists;
- zero-data-loss claims;
- unlimited retention;
- storing client evidence in GitHub.

## Review triggers

Reconsider the simple architecture only when there is concrete evidence such as:

- tenant scale makes the shared database unsafe or operationally impractical;
- a customer contract requires dedicated infrastructure or stronger encryption;
- measured recovery requirements exceed nightly backup capability;
- a regulatory or professional requirement demands a stronger control;
- restore testing demonstrates the baseline design is inadequate.
