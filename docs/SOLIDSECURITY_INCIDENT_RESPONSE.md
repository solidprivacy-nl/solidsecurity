# SolidSecurity Incident Response V1

## Scope

Security, privacy, availability and AI/automation incidents affecting the SolidSecurity service itself.

## Severity

- `SEV1`: confirmed/suspected cross-tenant disclosure, credential compromise with material access, destructive compromise or major sensitive-data breach.
- `SEV2`: material single-tenant exposure/availability/security event with credible impact.
- `SEV3`: contained weakness/event with limited impact.
- `SEV4`: observation/no demonstrated impact.

## Process

1. Record incident and time of awareness.
2. Preserve evidence and contain without destroying necessary forensic state.
3. Identify tenants/data/systems/providers potentially affected.
4. Revoke/rotate compromised access where applicable.
5. Escalate to accountable security/privacy professional.
6. Determine contractual/legal/regulatory notification obligations through authorized human review; AI may prepare timelines/facts but may not make the notification decision.
7. Recover and verify tenant isolation/integrity.
8. Communicate through approved channels.
9. Complete root cause, lessons and corrective actions.
10. Verify corrective-action effectiveness and close through governed review.

## Minimum operational prerequisites

- 24/7-capable security contact mechanism appropriate to pilot SLA;
- current provider/subprocessor incident contacts;
- ability to revoke sessions/tokens and isolate tenant/service access;
- restorable backups;
- audit/event history sufficient to reconstruct material access/actions;
- synthetic tabletop before first client.
