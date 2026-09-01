# SolidSecurity Project Governance Bootstrap

```text
project_repository=solidprivacy-nl/solidsecurity
project_risk_class=HIGH_SECURITY_PRIVACY_COMPLIANCE
adoption_status=MISSION_R2_CANONICAL_CONTROL_V3_1
implementation_role=implementation_operations/A1
assurance_role=governance_release_assurance/B1
project_specific_assurance_boundary=control/SOLIDSECURITY_ASSURANCE_CONTRACT_V1.md
production_action=NOT_AUTHORIZED
real_client_data=NOT_AUTHORIZED
customer_environment_write=NOT_AUTHORIZED
principal_manual_relay_target=0
```

## Purpose

This file defines the minimum local startup boundary for consequential SolidSecurity work. It is not a second Control state plane and contains no live routing state.

## Canonical authority order

Before consequential work, read authoritative sources in this order:

1. current `market-predictions/control-plane@main` Control Autonomy V3.1 architecture and runtime/repository authority;
2. current `market-predictions/control-plane@control-runtime-state` canonical queue/result facts when execution state matters;
3. `control/SOLIDSECURITY_MISSION_CONTRACT_R2.md`;
4. the active SolidSecurity GitHub issue/workpackage and exact repository facts;
5. `control/SOLIDSECURITY_ASSURANCE_CONTRACT_V1.md`;
6. `STRATEGY.md`, `ARCHITECTURE.md`, `ROADMAP.md` and relevant machine-readable models/tests.

`control/CURRENT_STATE.md` is a convenience snapshot only. It must never override live Control/runtime/repository evidence.

## V3.1 execution boundary

SolidSecurity uses central Control Autonomy V3.1 exactly as designed:

- one canonical private runtime queue;
- one deterministic Control Kernel runtime writer;
- A1 for implementation/repair;
- B1 for independent assurance;
- no A2;
- no semantic `PROJECT_INTEGRATION` task;
- no local intake/handover/retry runtime plane;
- no semantic-worker direct writes to canonical queue/results;
- no provider fallback.

Execution or assurance starts only after a current canonical V3.1 kernel claim proves exact task, role, worker and run identity. A scheduler/chat invocation is not START_PROVEN.

## Project authority boundaries

- GitHub is source of truth for project strategy, architecture, code, models and governed work facts.
- AI-generated analysis/documentation is never by itself a customer professional assurance conclusion.
- Real client data is prohibited until the explicit real-client security/data/contract/professional gate is satisfied and principal authorization exists.
- Autonomous final legal, certification, statutory, risk-acceptance or compliance decisions are not authorized.
- Production deployment and customer-system write/remediation require separate governed authority.
- Consequential project candidates retain independent B1 exact-candidate review where required.

## Public repository boundary

Only `PUBLIC_SAFE` material under `docs/PUBLIC_REPO_POLICY.md` may be committed here. Client data, secrets and proprietary restricted operating intelligence must stay outside the public repository.
