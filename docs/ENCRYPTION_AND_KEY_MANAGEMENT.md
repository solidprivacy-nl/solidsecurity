# Encryption and Key Management V1

Status: `DESIGN / SIMPLE BASELINE`

## Principle

SolidSecurity should use strong standard provider encryption and good secret handling before building custom cryptography.

The V1 rule is:

> Do not create an application-level encryption subsystem unless a concrete threat, contract or regulatory requirement demonstrates that provider encryption plus access control is insufficient.

## Mandatory baseline

For every real client-data environment:

- TLS for data in transit;
- provider-managed encryption at rest for PostgreSQL and primary object storage;
- private-by-default evidence objects;
- secrets outside GitHub, source code and ordinary logs;
- least-privilege credentials;
- MFA for material privileged/reviewer actions as defined elsewhere;
- encrypted portable database/backup archives before or during off-site transfer;
- separate credentials for the off-site backup target.

## Database

Use the selected PostgreSQL provider's encryption at rest and normal database authorization/RLS.

Do not introduce transparent column encryption by default. It complicates queries, migrations, indexing and operations while often providing little additional protection when the same application identity must transparently decrypt every value.

Targeted field encryption is a later exception for specifically identified high-value fields when justified.

## Evidence objects

Evidence remains in private object storage with tenant-scoped authorization. Provider-managed encryption at rest is the V1 default.

Reviewed evidence versions are immutable at the application level and have an integrity hash. A hash provides integrity checking, not confidentiality.

## Backup encryption

Portable database dumps and off-site backup packages must not be stored as readable plaintext on the secondary target.

Use a mature standard encryption capability supplied by the backup/sync tool or an established cryptographic utility. Do not design a SolidSecurity encryption algorithm.

Backup decryption material is kept separately from the backup archive and is stored through normal secret-management practices.

## Future escalation

Application-level envelope encryption, customer-managed keys, dedicated KMS/HSM services or per-customer cryptographic keys may be introduced only when justified by one of the following:

- explicit customer contract;
- regulator/professional requirement;
- materially higher data classification;
- threat-model finding not adequately mitigated by the baseline;
- demonstrated need for cryptographic separation from the storage provider.

Such an escalation requires its own ADR and recovery design because stronger encryption can also make data unrecoverable when key management fails.

## Prohibited patterns

- secrets or encryption keys committed to GitHub;
- plaintext portable database backups on the secondary server;
- public evidence buckets/URLs as the default access model;
- client names or sensitive labels unnecessarily exposed in object keys;
- home-grown cryptography;
- describing provider encryption at rest as end-to-end encryption;
- adding a KMS or envelope-encryption stack merely because it is theoretically stronger.
