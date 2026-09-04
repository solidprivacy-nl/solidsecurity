# SolidSecurity Project Governance Bootstrap

```text
project_repository=solidprivacy-nl/solidsecurity
project_risk_class=HIGH_SECURITY_PRIVACY_COMPLIANCE
adoption_status=MISSION_R2_CANONICAL_CONTROL_MANAGED
central_control_authority=market-predictions/control-plane
project_specific_assurance_boundary=control/SOLIDSECURITY_ASSURANCE_CONTRACT_V1.md
production_action=NOT_AUTHORIZED
real_client_data=NOT_AUTHORIZED
customer_environment_write=NOT_AUTHORIZED
principal_manual_relay_target=0
```

## Purpose

This file defines the minimum local startup boundary for consequential SolidSecurity work. It is not a second Control state plane and contains no live routing state, worker topology or Control protocol version.

## Canonical authority order

Before consequential work, read authoritative sources in this order:

1. current `market-predictions/control-plane@main` canonical Control architecture/index/repository authority;
2. current canonical Control runtime-state facts when execution state matters;
3. `control/SOLIDSECURITY_MISSION_CONTRACT_R2.md`;
4. the active SolidSecurity GitHub issue/workpackage and exact repository facts;
5. `control/SOLIDSECURITY_ASSURANCE_CONTRACT_V1.md`;
6. `STRATEGY.md`, `ARCHITECTURE.md`, `ROADMAP.md` and relevant machine-readable models/tests.

`control/CURRENT_STATE.md` is a convenience snapshot only. It must never override live Control/runtime/repository evidence.

## Central Control execution boundary

SolidSecurity owns Mission/evidence requirements, not the orchestration implementation. Therefore:

- there is one central Control authority and no project-local queue/state plane;
- current Control runtime version, task/lock model, worker topology, scheduling and cutover phase are read fresh rather than copied here;
- a consequential candidate is bound to its exact head/base and applicable acceptance criteria;
- deterministic validation is used for mechanical checks;
- consequential changes receive fresh exact-candidate critical review, with external/independent exact-candidate review when current project/Control policy requires it;
- candidate movement invalidates stale review evidence;
- review PASS is not by itself integration authority when current repository/Control policy still requires a separate gate;
- project workers do not bypass central Control by writing canonical runtime state directly;
- no local intake/handover/retry runtime plane or provider fallback is authorized.

A scheduler/chat invocation or local progress statement is never execution/completion authority by itself.

## Project authority boundaries

- GitHub is source of truth for project strategy, architecture, code, models and governed work facts.
- AI-generated analysis/documentation is never by itself a customer professional assurance conclusion.
- Real client data is prohibited until the explicit real-client security/data/contract/professional gate is satisfied and principal authorization exists.
- Autonomous final legal, certification, statutory, risk-acceptance or compliance decisions are not authorized.
- Production deployment and customer-system write/remediation require separate governed authority.
- Consequential project candidates must satisfy every currently applicable project-change review and integration gate.

## Public repository boundary

Only public-safe material under `docs/PUBLIC_REPO_POLICY.md` may be committed here. Client data, secrets and proprietary restricted operating intelligence must stay outside the public repository.
