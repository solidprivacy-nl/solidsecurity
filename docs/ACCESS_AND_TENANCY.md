# Access, Tenancy and Agent Identity V1

## Identity principle

Every action is attributable to a distinct human or agent identity. Shared accounts are prohibited for privileged or review actions.

## Minimum roles

### `platform_admin`

Operate platform/security configuration. May manage tenants and emergency access but should not routinely read client evidence.

### `professional_reviewer`

May read assigned client scope/evidence and issue governed reviews/decisions within professional authority.

### `operations_contributor`

May structure data, draft, request evidence and prepare proposed assessments; cannot issue independent assurance decisions.

### `client_admin`

Customer-designated owner; manages customer users and can approve/submit customer facts/evidence within tenant.

### `client_contributor`

Uploads/responds to assigned evidence/action requests.

### `client_reader`

Read-only access to permitted customer outputs/status.

### `agent_service`

Non-human identity with tenant-scoped, task-scoped permissions. Cannot perform human-only review/decision classes.

## Authentication

- MFA required for all internal professionals/admins and client admins;
- privileged access uses strong phishing-resistant methods where feasible;
- sessions expire and can be centrally revoked;
- service/agent secrets stored in secret manager, never Git;
- no model/provider API key exposed to client browser.

## Authorization

Deny by default. Permission checks consider actor, tenant, object, action and review class.

High-risk operations require explicit human authority: tenant export, deletion override, risk acceptance, exception approval, professional verification, legal/certification claims and emergency access.

## Break-glass

Emergency platform access must be time-bounded, reason-coded, logged, reviewed after use and unable to bypass client-data audit history silently.

## Joiner/mover/leaver

Internal access is reviewed on onboarding, role change and termination. Privileged access gets periodic recertification. Client access ends at offboarding or immediately on customer instruction where applicable.
