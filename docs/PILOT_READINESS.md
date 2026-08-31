# Pilot Readiness V1

## Objective

Define the minimum safe operating boundary before SolidSecurity may ingest the first real client dossier.

This phase does **not** authorize production or real client data. It converts the service concept into explicit preconditions that can later be independently verified.

## Core principle

SolidSecurity should process **compliance evidence, not business data by default**.

For a care organization, proof should normally be obtained from policies, registers, configuration exports, screenshots, training records, contracts, test records and aggregated system evidence. Raw care records, patient/client notes or other special-category content are not required merely because the customer works in healthcare.

If high-sensitivity content is genuinely necessary, it follows a separately approved route with stronger minimization, access and model-processing restrictions.

## Three-plane architecture

### 1. Public product/control plane

May contain public-safe methodology, schemas, generic controls, ADRs, source references and synthetic examples.

Must never contain real client data, credentials, proprietary detailed evidence rubrics or sensitive operational intelligence.

### 2. Private operations plane

Holds proprietary mappings/rubrics, internal runbooks, prompts/agent policies, pricing/economics, reviewer playbooks and operational configuration.

It should reference client objects by opaque identifiers and avoid duplicating raw client evidence.

### 3. Client data plane

Holds real client scope, claims, vendors, risks, evidence, assessments, reviews, decisions and approved artifacts.

Tenant isolation, access control, encryption, audit logging, lifecycle/deletion and model-processing controls are mandatory.

## Pilot runtime philosophy

The first real pilot does not need a broad GRC product. Minimum runtime capabilities are:

- authenticated evidence intake;
- encrypted object/evidence storage;
- structured metadata/state store;
- tenant-scoped professional workspace;
- AI-assisted extraction/drafting against explicitly selected client artifacts;
- professional review/decision recording;
- export/offboarding/deletion.

No customer-environment scanner or write connector is required.

## Mandatory gates before real data

1. Foundation and model dependencies independently accepted.
2. Public/private repository split decision implemented.
3. Threat model completed and reviewed.
4. Tenant boundary technically implemented and tested.
5. Human and agent identity/RBAC/MFA implemented.
6. Encryption, secret management and backup/recovery implemented.
7. Evidence integrity/provenance and audit logging implemented.
8. Client contract/DPA/subprocessor register ready.
9. Retention/deletion/export policy implemented.
10. LLM provider/data policy approved and technically enforceable.
11. Incident response exercised with synthetic data.
12. End-to-end synthetic deployment dry run passes.
13. Independent security/data-governance review issues PASS.

Until all gates pass, real client data is prohibited.
