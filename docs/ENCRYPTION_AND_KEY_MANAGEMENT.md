# Encryption and Key Management V1

Status: `DESIGN / PROVIDER-NEUTRAL REQUIREMENTS`

## Principle

Encryption is layered. SolidSecurity must not describe provider encryption at rest as end-to-end encryption or as protection against every storage-provider or credential-compromise scenario.

## Mandatory baseline

For every real client-data environment:

- TLS for data in transit;
- provider-managed encryption at rest for database, primary object storage and provider-managed backups;
- private-by-default evidence objects;
- no secret/key material in GitHub, source code, object names or ordinary logs;
- role-scoped access to decryption-capable services;
- key and credential rotation/revocation procedures;
- encrypted independent logical database backups before they are written to a secondary recovery provider.

## Data-classification-driven profiles

### STANDARD / INTERNAL

Provider encryption at rest plus application authorization may be sufficient when approved by the data classification and threat model.

### CLIENT_CONFIDENTIAL

Provider encryption is mandatory. Application-layer envelope encryption is available where the threat model, customer contract or evidence sensitivity justifies stronger separation.

### CLIENT_HIGH_SENSITIVITY

The runtime design must support application-layer authenticated encryption before persistent object storage unless a documented security/data-governance decision approves an equivalent architecture.

High-sensitivity content remains deny-by-default for unapproved external AI processing regardless of storage encryption.

## Envelope encryption model

Do not invent cryptography. Use a standard authenticated-encryption implementation from a reviewed cryptographic library.

Conceptual flow:

```text
Evidence bytes
    |
    | generate random data-encryption key (DEK)
    v
Authenticated encryption (e.g. approved AEAD)
    |
    +---- encrypted object ----> primary/secondary object storage
    |
    +---- wrapped DEK ---------> controlled metadata store
                                  |
                                  | unwrap only through
                                  v
                         Key Management Service
                         master/key-encryption key
```

Rules:

- unique random DEK per evidence version or recovery package;
- master/key-encryption key is never stored next to the plaintext DEK;
- only wrapped/encrypted DEKs may be stored with dossier metadata;
- authenticated additional data should bind ciphertext to stable context such as tenant/evidence/version identifiers;
- rotation of the key-encryption key should normally re-wrap DEKs rather than re-encrypt every large object;
- decryption is a server-side authorized operation and is auditable;
- customer-facing direct object URLs must not bypass decryption authorization.

## KMS boundary

The architecture requires a `KeyManagementService` abstraction but does not select the final KMS in this design stage.

A production KMS must provide, directly or through an approved service boundary:

- strong managed key protection/HSM-backed controls where available;
- access control distinct from ordinary object-store credentials;
- rotation and revocation;
- auditability of key use/administration;
- EU/data-location suitability where material;
- recovery/escrow procedure that does not put plaintext master keys into the same backup archive as encrypted data.

A general secrets store can hold API credentials but is not automatically a cryptographic KMS suitable for bulk envelope-encryption operations.

## Database encryption

The baseline database is provider-encrypted at rest. Do not introduce transparent column encryption by default: it creates query, indexing, key-rotation and operational complexity and may add little protection if the same application identity can transparently decrypt all rows.

Use targeted application-level field encryption only for narrowly identified fields whose confidentiality threat justifies it.

Passwords and authentication secrets follow the identity provider's approved storage mechanisms rather than custom encryption.

## Backup encryption

Independent logical database dumps and recovery packages must be encrypted before leaving the trusted backup process.

The recovery store may also encrypt at rest; this is defense in depth, not a substitute for backup-package encryption when independent-provider compromise is in scope.

Backup encryption metadata records algorithm/profile/key reference and creation time, but never plaintext keys.

## Crypto-shredding

Where contractually and legally appropriate, tenant-specific wrapped-key design may support cryptographic erasure after normal retention/deletion conditions are met. This is not used to evade documented backup-expiry behavior and does not replace required deletion from active stores.

## Prohibited patterns

- one static encryption key committed to environment files or source control;
- client names or sensitive labels in object keys;
- storing plaintext master keys with backups;
- home-grown encryption algorithms;
- logging plaintext evidence during encryption/decryption errors;
- treating a hash as encryption;
- automatic AI access to a KMS because the AI can request document analysis.
