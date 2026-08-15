# Data Resilience Architecture V1

Status: `DESIGN / NO REAL CLIENT DATA AUTHORITY`

## Purpose

Define the minimum durable architecture for SolidSecurity client dossiers before implementation. The design separates confidentiality, integrity, availability and disaster recovery so that a single provider feature is never treated as solving all four.

## Architecture in one view

```text
                      GitHub Control Plane
                 method / schema / software
                           | releases
                           v
                SolidSecurity Application Layer
             operator workspace + client dashboard
                           |
               server-side tenant routing
                           |
          +----------------+----------------+
          |                                 |
          v                                 v
  Client Project / Tenant A          Client Project / Tenant B
  Supabase EU candidate              Supabase EU candidate
  +----------------------+           +----------------------+
  | Postgres structured  |           | Postgres structured  |
  | state                |           | state                |
  | Auth / RLS           |           | Auth / RLS           |
  | Private evidence     |           | Private evidence     |
  | storage              |           | storage              |
  +----------+-----------+           +----------+-----------+
             |                                  |
             | independent encrypted backup    |
             +------------------+---------------+
                                v
                    Secondary Recovery Store
                    separate provider/failure domain
                    Cloudflare R2 candidate
                    - DB logical backups
                    - evidence replicas
                    - audit manifests
                    - retention/bucket locks

                 Keys / secrets are separate from
                 evidence objects and backup objects.
```

## Design decisions

### 1. Three authoritative stores

**GitHub control plane** is authoritative for SolidSecurity methodology, schemas, migrations, release definitions and non-client-specific product logic.

**Structured client state** is authoritative for the current governed state of a client dossier: scope, implementations, assessments, findings, actions, requests, reviews, approvals and evidence metadata.

**Evidence object storage** is authoritative for the immutable bytes of evidence versions. Large files are not stored as Postgres blobs.

A backup is never an authoritative working store.

### 2. Early tenancy: project-per-client

For the first regulated clients, retain the conditional project-per-client Supabase design. Each client receives a separate database/Auth/Storage boundary. `tenant_id` remains present in client-plane entities for portability and defense in depth.

The private operations registry may contain routing metadata such as opaque tenant id, runtime project reference, region, service status and schema version. It must not become a duplicate evidence repository.

A future shared multi-tenant Postgres model requires a new ADR, proven RLS/isolation tests and an explicit blast-radius/economics justification.

### 3. Evidence versions are immutable

No reviewed evidence object is overwritten in place.

Recommended opaque object identity:

`tenants/{tenant_uuid}/evidence/{evidence_uuid}/versions/{version_uuid}.bin`

Object keys must not contain client names, personal names, filenames, system names or other meaningful sensitive identifiers.

The controlled database stores the client-visible filename and metadata.

Each `evidence_version` records at minimum:

- tenant id;
- evidence id and version id;
- primary object key;
- content SHA-256 hash;
- byte size;
- media type;
- classification;
- source/provenance;
- actor and ingestion timestamp;
- encryption profile/reference;
- backup state;
- retention state;
- validity/expiry where applicable.

A changed file creates a new evidence version and new content hash. Historical reviews keep their original version reference.

### 4. Independent secondary recovery store

A copy inside the same primary service is useful redundancy but does not satisfy the independent recovery-copy requirement.

SolidSecurity maintains a secondary recovery store in a separate provider/failure domain. Cloudflare R2 is the current candidate because it provides inexpensive S3-compatible object storage, strong durability, encryption at rest and bucket retention locks.

The secondary store contains only recovery artifacts:

- encrypted logical database exports;
- evidence-object replicas or encrypted recovery packages;
- backup manifests and integrity results;
- exported/tamper-evident audit batches.

It is not used as a second live application database.

### 5. Resilience state is visible

Evidence ingestion and resilience are separate states. A document can be successfully received but not yet independently backed up.

Suggested operational states:

`RECEIVED -> HASH_VERIFIED -> PRIMARY_STORED -> SECONDARY_VERIFIED -> AVAILABLE_FOR_REVIEW`

Failure to reach `SECONDARY_VERIFIED` creates an operational alert. Material professional review can proceed only according to the approved service profile; client-facing assurance must never imply a recovery copy exists when it does not.

### 6. Backup without restore is not a control

Every backup class has a restore acceptance test. Backup monitoring checks creation; restore tests prove usability.

At minimum:

- automated manifest/hash verification after backup;
- periodic sample object restore and hash comparison;
- periodic synthetic tenant database restore;
- periodic full synthetic dossier reconstruction including structured state plus evidence;
- restore-test result stored as governed operational evidence.

### 7. Retention and deletion are one lifecycle

Primary and backup retention are driven by data category, contract and applicable obligations. No universal legal period is hard-coded here.

Deletion state distinguishes:

- active;
- scheduled for deletion;
- removed from primary;
- retained temporarily in protected backup window;
- legal/contractual hold;
- fully expired/purged.

Client deletion confirmation must accurately describe any remaining protected backup window. Bucket locks must never create an undisclosed indefinite copy.

### 8. Recovery targets are profiles, not untested promises

V1 defines engineering target classes. They become customer commitments only after runtime proof and explicit service-contract approval.

| Profile | Structured-state RPO target | Evidence-copy RPO target | RTO target | Typical mechanism |
|---|---:|---:|---:|---|
| Baseline | <= 24h | <= 24h | <= 8h | managed daily backup + daily offsite export |
| Enhanced | <= 4h | <= 1h | <= 4h | more frequent logical export/replication |
| Critical | minutes | minutes | <= 2h | PITR/continuous mechanisms after commercial approval |

The default early service should use the least expensive profile that satisfies the contracted risk requirement. Expensive PITR is not enabled merely because it exists.

## Provider-specific current candidate

The current conditional pilot architecture remains:

- Supabase EU project per early client for Postgres/Auth/private Storage;
- provider-managed encryption at rest and TLS as baseline;
- Cloudflare R2 as candidate independent recovery store;
- provider-neutral application interfaces for evidence storage, backup and key management;
- no provider selection becomes production authority without the existing real-client gate.

## Required implementation abstractions

Keep these interfaces explicit so storage/provider choices remain replaceable:

- `StructuredStateRepository`
- `EvidenceObjectStore`
- `EvidenceCryptoService`
- `KeyManagementService`
- `BackupService`
- `RecoveryStore`
- `AuditEventStore`
- `TenantRuntimeRouter`

Business/domain code must not embed provider bucket names, project references or secret material.

## Non-goals

- active-active multi-cloud database replication;
- zero-data-loss claims;
- bespoke cryptography;
- permanent duplicate live databases per client;
- unlimited retention;
- storing client evidence in GitHub;
- treating provider certification as SolidSecurity assurance.
