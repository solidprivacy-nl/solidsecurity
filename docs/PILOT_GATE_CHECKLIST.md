# First Real Client — Hard Gate Checklist

A real client dossier is prohibited until every required gate is `PASS` or an explicitly authorized exception exists where policy permits one.

## Foundation

- [ ] Foundation V1 merged after independent assurance.
- [ ] Required pilot-driven model refinements accepted.
- [ ] Service scope/claims language approved.

## Repository/IP boundary

- [ ] Public-core vs private-operations decision implemented.
- [ ] No proprietary evidence rubrics/prompts/client data in public repo.
- [ ] Secret scanning and protected production-development workflow in place.

## Legal/data processing

- [ ] Client contract/service terms ready.
- [ ] DPA/role analysis completed where required.
- [ ] Subprocessor register approved.
- [ ] Actual retention schedule approved.
- [ ] AI/model processing route approved.

## Technical client data plane

- [ ] Tenant isolation implemented.
- [ ] Cross-tenant negative tests pass.
- [ ] Object storage private and tenant scoped.
- [ ] MFA/RBAC/service identities implemented.
- [ ] Secrets managed outside repo/app config.
- [ ] Encryption in transit/at rest verified.
- [ ] Audit/event logging verified without sensitive-content leakage.
- [ ] Backup/restore test passes.
- [ ] Evidence hash/version provenance works.
- [ ] Export and deletion dry run passes.

## AI/automation

- [ ] Agent identity cannot perform human-only decisions.
- [ ] No cross-tenant retrieval/memory.
- [ ] High-sensitivity external-LLM deny-by-default works.
- [ ] Prompt-injection/tool boundary tested.
- [ ] Model/provider provenance recorded for outputs.

## Operations

- [ ] Incident response contacts/runbook ready.
- [ ] Synthetic incident tabletop completed.
- [ ] Access review/joiner-leaver process active for SolidSecurity staff.
- [ ] First-pilot evidence intake support path documented.

## Independent release gate

- [ ] Security/data-governance assurance review: `PASS`.
- [ ] Principal explicitly authorizes transition from synthetic-only to first-real-client pilot.
