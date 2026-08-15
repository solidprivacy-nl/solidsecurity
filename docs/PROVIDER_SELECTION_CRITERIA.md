# Pilot Runtime Provider Selection Criteria

## Decision rule

Choose the smallest managed stack that satisfies the proven workflow and security/data requirements. Familiarity alone is not a selection criterion.

## Mandatory capabilities

### Data/database

- EU/appropriate region option and contractual data-processing terms;
- relational model suitable for tenant-scoped structured records;
- row-level authorization/RLS or equivalent strong isolation;
- encrypted transport/storage;
- backup/restore;
- point-in-time/recovery options proportionate to risk;
- auditable administrative access.

### Object/evidence storage

- private buckets/objects;
- tenant authorization;
- signed short-lived access;
- lifecycle/deletion/version support;
- encryption and integrity metadata;
- provider DPA/security documentation.

### Identity

- MFA/SSO capability;
- role/tenant integration;
- service identity/token scoping;
- session revocation.

### Secrets

- managed encrypted secret store;
- rotation/access logging;
- no secrets in repository or ordinary application database fields.

### Application/API

- server-side authorization enforcement;
- safe file ingestion path;
- audit/event logging;
- environment separation;
- export/delete jobs.

### AI provider

- enterprise/API contractual route;
- no-training posture;
- documented retention configuration;
- acceptable data region/transfer posture;
- ability to use minimal/transient context;
- provider/subprocessor register entry.

## Evaluation dimensions

Security fit, data protection, operational simplicity, cost at first 10/50/100 tenants, exportability/lock-in, observability, backup/recovery, developer velocity and ability to keep the product thin.

## Explicitly defer

- multi-cloud architecture;
- Kubernetes;
- dedicated infrastructure per small tenant unless risk/customer requires it;
- permanent vector database unless workflow evidence justifies it;
- real-time customer-environment collectors.

## Next decision

Run a short architecture selection against 2–3 credible stacks only after these requirements receive independent review. The provider decision becomes its own ADR and work package.
