# First-Pilot Threat Model V1

## Protected assets

- client evidence and sensitive organizational/security information;
- personal data contained in evidence;
- professional reviews/decisions;
- credentials/secrets;
- proprietary SolidSecurity operating intelligence;
- tenant isolation and audit history.

## Priority threats and required mitigations

### Cross-tenant data leakage

Mitigate with tenant-derived authorization context, RLS/equivalent, tenant-scoped object storage, agent/retrieval isolation and automated negative tests.

### Public-repository disclosure

No client data or secrets in public GitHub. Pre-commit/CI secret scanning should be added before production code. Private operations plane for proprietary/client-adjacent material.

### Compromised reviewer/admin account

MFA, least privilege, session revocation, audit logging, periodic access review and break-glass controls.

### Agent/LLM overreach

Separate agent identity, task/tenant-scoped permissions, human-only actions for material decisions, tool allowlists and no cross-tenant memory.

### Prompt injection from uploaded evidence

Treat document instructions as untrusted content; system/tool authority is outside retrieved document context; no arbitrary tool execution from evidence text.

### Malicious or unsafe file upload

File allowlist, size limits, malware scanning/sandboxing where appropriate, no execution of active content/macros, safe extraction pipeline.

### Evidence tampering or silent replacement

Hash/version provenance, audit trail, immutable review references and no silent overwrite of evidence already used in a decision.

### Model-provider retention/training leakage

Approved enterprise/API routes, no-training terms, retention controls, data minimization and high-sensitivity deny-by-default.

### Secret leakage in evidence

Detect/reject/redact likely credentials; secrets never passed to LLM; secure secret manager for legitimate service credentials.

### Excessive logging/observability leakage

Logs contain IDs/metadata and security events, not document bodies, raw prompts or unnecessary personal data.

### Incomplete deletion

Central lifecycle state covers object, metadata, derivative, cache/search/vector and backups; deletion evidence/audit record retained at non-content level.

## Required security tests before pilot

- cross-tenant API/storage negative tests;
- RBAC authorization matrix tests;
- signed-link expiry/access tests;
- file-upload abuse tests;
- evidence version/hash tests;
- agent permission boundary tests;
- deletion/export dry run;
- backup/restore test;
- synthetic incident tabletop;
- secret/log-content inspection.
