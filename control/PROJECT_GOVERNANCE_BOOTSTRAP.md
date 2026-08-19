# SolidSecurity Project Governance Bootstrap

```text
charter_id=CROSS_PROJECT_PRINCIPAL_AGENT_OPERATING_CHARTER_V1
canonical_charter_location=https://github.com/market-predictions/control-plane/blob/main/control/CROSS_PROJECT_PRINCIPAL_AGENT_OPERATING_CHARTER_V1.md
standard_id=CROSS_PROJECT_TWO_ROLE_GOVERNANCE_V1
canonical_standard_location=https://github.com/market-predictions/control-plane/blob/main/control/CROSS_PROJECT_TWO_ROLE_GOVERNANCE_STANDARD_V1.md
project_repository=solidprivacy-nl/solidsecurity
project_risk_class=HIGH_SECURITY_PRIVACY_COMPLIANCE
adoption_status=ACTIVE_FOUNDATION_IMPLEMENTATION
enforcement_maturity=LEVEL_1_CHECKLIST
implementation_role=implementation_operations
assurance_role=governance_release_assurance
project_specific_assurance_contract=control/SOLIDSECURITY_ASSURANCE_CONTRACT_V1.md
production_action=NOT_AUTHORIZED
real_client_data=NOT_AUTHORIZED
customer_environment_connection=NOT_AUTHORIZED
post_action_confirmation=REQUIRED_WHEN_PRODUCTION_ACTIONS_ARE_LATER_AUTHORIZED
```

## Local scope

SolidSecurity is an AI-native managed security & compliance project for small healthcare organizations and SMEs facing security, privacy, AI-governance, certification-readiness and NIS2/Cybersecurity Act direct or supply-chain pressure.

The project deliberately starts with a small control and workflow backbone. Customer-environment scanning, automated technical evidence collection and broad platform implementation remain outside the current foundation scope.

## Authority boundaries

- GitHub is source of truth for project strategy, state, decisions, roadmap and governed work.
- Consequential implementation and assurance remain separated under the canonical Control standard.
- AI-generated analysis or documentation is never by itself a professional assurance conclusion.
- Real client data is not authorized until a later client data-plane contract is explicitly approved.
- Autonomous final legal, certification, risk-acceptance or compliance decisions are not authorized.
- Issue #2 authorizes foundation realization following principal acceptance of the concept on 2026-08-15.
- Production runtime and customer-system connections require separate governed authorization.

## Public repository boundary

While the repository is public, only information classified `PUBLIC_SAFE` under `docs/PUBLIC_REPO_POLICY.md` may be committed. Public visibility is not authorization to disclose client, secret, privileged or commercially restricted material.

## Required project-local reads

Before consequential work, read at minimum:

1. canonical Control mandatory sources;
2. this bootstrap;
3. `control/CURRENT_STATE.md`;
4. `control/SOLIDSECURITY_ASSURANCE_CONTRACT_V1.md`;
5. the active GitHub issue/work contract;
6. `STRATEGY.md`, `ARCHITECTURE.md`, `ROADMAP.md`;
7. relevant ADRs, schemas, tests and evidence for the active work package.
