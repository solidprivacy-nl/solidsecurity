# Runtime Acceptance Contract V1

Status: `SPECIFIED / NOT EXECUTED / REAL CLIENT DATA PROHIBITED`

## Purpose

A provider feature is not implementation evidence. This contract defines the minimum provider-neutral synthetic tests the exact first-pilot runtime must pass before SolidSecurity may ask for authorization to process a real client dossier.

The contract complements `PILOT_GATE_CHECKLIST.md`. It does not replace an independent security/data-governance review.

## Test rule

Every mandatory scenario is evaluated against an **exact deployed candidate** with versioned configuration and synthetic tenants/data.

Allowed results:

- `PASS` — observed evidence satisfies all expected outcomes;
- `FAIL` — one or more expected outcomes are contradicted;
- `INDETERMINATE` — test could not establish the outcome.

`INDETERMINATE` blocks the real-client gate exactly like `FAIL` for mandatory scenarios.

No test may be marked PASS from architecture diagrams, provider documentation or code review alone when the scenario requires runtime evidence.

## Mandatory scenario families

### Tenant isolation

Prove both read **and write** denial across synthetic tenants. Include normal API requests, object storage and asynchronous/background work. A correct UI is not evidence of backend isolation.

### Identity and authority

Prove MFA/assurance level is enforced for material reviewer actions and prove an `agent_service` identity cannot perform human-only decisions even if it knows the endpoint/tool name.

### Evidence integrity

Prove accepted evidence cannot be silently overwritten after use in an assessment/review. New content creates a new version/hash/provenance relationship.

### AI data boundary

Prove `CLIENT_HIGH_SENSITIVITY` external-LLM routing is denied by default, cross-tenant retrieval/memory is absent and uploaded prompt-injection text cannot grant tool/system authority.

### Lifecycle

Prove export, deletion and recovery operate across both structured metadata and evidence objects. Database recovery alone is insufficient.

### Independent recovery

Prove an encrypted logical database backup and the required evidence versions exist in a separate provider/failure domain and can reconstruct the intended dossier without depending on the original primary project remaining available.

### Cryptographic separation

Where the approved data classification requires application-layer encryption, prove the ciphertext/key boundary works: unauthorized users cannot invoke decryption, plaintext master key material is not co-located with backups, and failures do not leak plaintext or key material into logs.

### Recovery objectives

Measure achieved recovery point and recovery time during synthetic restoration. Configuration or provider marketing does not prove RPO/RTO. A recovery profile remains unproven when the measured result exceeds the target.

### Logging/secrets

Prove ordinary logs do not capture document bodies, raw sensitive prompts or secrets; prove service credentials remain server-side/secret-managed and can be revoked.

### Region/jurisdiction

Prove the actual deployed resources/configuration use the approved region/jurisdiction. A provider's general EU capability is not enough.

### Incident readiness

Execute one synthetic incident/tabletop that exercises tenant isolation, credential revocation, evidence preservation, escalation and notification-decision handoff without sending a real statutory notification.

## Evidence packet per test

Each result should record:

- test ID and contract version;
- candidate/deployment/configuration version;
- date/time;
- actor/test runner;
- synthetic tenants/data used;
- exact steps;
- expected outcomes;
- observed outcomes;
- immutable/log references;
- PASS/FAIL/INDETERMINATE;
- reviewer where required;
- open findings.

## Gate

`real_client_data_allowed` remains `false` until every mandatory scenario is PASS, the broader Pilot Readiness checklist is satisfied, independent security/data-governance assurance is PASS and the principal explicitly authorizes the first real-client transition.
