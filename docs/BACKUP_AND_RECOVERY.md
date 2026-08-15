# Backup and Recovery V1

Status: `DESIGN / NO CUSTOMER SLA CLAIM`

## Principle

SolidSecurity uses a deliberately simple backup design: one scheduled job, one independent off-site copy, clear monitoring and periodic restore proof.

A backup command that exited successfully is not yet proof that the service is recoverable.

## Nightly backup flow

The default V1 process runs once per night:

1. create a consistent PostgreSQL logical backup (`pg_dump` or provider-equivalent);
2. export/sync the primary evidence-object store, preferably incrementally;
3. generate a small manifest with timestamp, schema/release version and checksums;
4. encrypt the database dump and backup package before or during transfer;
5. copy the backup set to an independent low-cost storage environment;
6. write a success/failure record and alert on failure or lateness.

The transfer mechanism is intentionally ordinary. Suitable implementations include SFTP, S3-compatible sync, `rclone`, `restic` or equivalent standard tooling. The architecture does not depend on one product.

## Backup target

The secondary target should be:

- independent from the primary database/object-store account or provider where practical;
- inexpensive at low volume;
- private;
- accessible through standard automation;
- protected with separate least-privilege credentials;
- capable of retaining enough history to recover from accidental deletion or a bad deployment.

A third storage copy is optional. It may be added later as a low-frequency weekly/monthly copy when the cost/benefit is clear; it is not a V1 requirement.

## What is backed up

### PostgreSQL

The logical database backup contains the shared multi-tenant structured state for all customers. Because one database contains all tenants, the backup is protected as highly sensitive operational data.

### Evidence objects

All persistent evidence/attachment objects that are part of client dossiers are included in the object-store backup/sync. Database backup alone is not enough when object bytes live outside PostgreSQL.

### Configuration needed for recovery

The backup process records enough non-secret version information to know which schema/migrations/application release belong to the backup. Secrets themselves are not copied into GitHub or ordinary manifests.

## Integrity

Use normal cryptographic checksums such as SHA-256 for backup artifacts or manifests. The goal is straightforward corruption/change detection, not a custom cryptographic protocol.

Reviewed evidence versions remain immutable in the primary application model; the backup process copies those versions rather than rewriting history.

## Restore proof

At a sensible periodic interval, perform a small controlled recovery test:

- restore the latest database backup into an isolated recovery/test database;
- retrieve a sample of backed-up evidence objects;
- compare hashes to the expected manifest/source metadata;
- confirm a synthetic tenant dossier can be reconstructed;
- confirm tenant isolation still holds in the restored environment.

Record date, backup used, outcome and any corrective action.

There is no need for continuous DR exercises or several recovery tiers in V1.

## Retention and deletion

Retention periods are configuration/contract driven and are not hard-coded as universal legal rules.

When client data is removed from production, ordinary retained backups may still contain it until those backups expire. This must be documented accurately. Legal/contractual hold, when needed, is explicit rather than implicit indefinite retention.

## Monitoring

Minimum signals:

- last successful database backup;
- last successful object backup/sync;
- last successful off-site transfer;
- backup age;
- transfer or encryption errors;
- last successful restore test.

This can initially be implemented with a cron/scheduled job plus simple alerting rather than a dedicated backup platform.

## Escalation triggers

Only add more expensive or complex recovery mechanisms when a concrete requirement exists, such as:

- a required recovery point materially shorter than one night;
- contractual need for dedicated infrastructure;
- measured restore time is unacceptable;
- higher data volume makes nightly transfer impractical;
- restore testing exposes a material weakness.

## Prohibited shortcuts

- backing up only PostgreSQL while forgetting evidence objects;
- keeping the only backup under the exact same credentials/failure domain as production;
- unencrypted portable database dumps on a secondary server;
- treating an untested backup as proven recovery;
- storing backup credentials or customer data in GitHub;
- introducing active-active replication or bespoke backup infrastructure without a demonstrated need.
