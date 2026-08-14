# SolidSecurity Current State

## Status

`CONCEPT / OPERATING MODEL DESIGN`

Control-managed: **yes**

Authoritative work contract: issue #1

## Current objective

Produce and discuss a coherent SolidSecurity concept and operating model before committing to product implementation.

The proposal must integrate:

- target positioning for small healthcare organizations and SMEs;
- Cybersecurity Act / NIS2 direct and supply-chain pressure;
- NEN 7510 / ISO 27001 readiness;
- GDPR/privacy and AI Act governance where relevant;
- AI leverage with credible professional review and assurance;
- a minimal cross-framework control/data backbone;
- selective reuse of external open-source functions and patterns;
- a simple initial architecture and staged roadmap;
- explicit deferral of automatic customer-environment scanning.

## Current hard constraints

1. Do not overengineer the MVP.
2. Do not import whole external repositories merely because they are feature-rich.
3. Select reusable functions/patterns only when they form part of a coherent workflow.
4. Do not connect to or automatically scan customer environments in the initial phase.
5. Keep later technical evidence connectors on the roadmap if they materially improve the model.
6. Keep implementation and independent assurance separated for consequential work.
7. AI output does not equal professional assurance.
8. No real client data during concept/bootstrap.
9. No autonomous final legal/certification/compliance decisions.
10. Discuss the concept proposal before product implementation begins.

## External projects currently under selective evaluation

- `getprobo/probo` — MIT; GRC primitives and AI/API patterns.
- `unidoc/isms` — Apache-2.0; lean management-system, Git document and human/AI review patterns.
- `intuitem/ciso-assistant-community` — control/framework decoupling and mapping inspiration; AGPL code reuse requires explicit licensing analysis.
- `prowler-cloud/prowler` — technical evidence/scanning candidate for a later roadmap phase, not MVP.
- `oscal-compass/compliance-trestle` — machine-readable compliance/interoperability concepts, likely later-stage.

## Queue state

No implementation queue intent is authorized yet.

The concept proposal is the next deliverable for principal discussion. After the concept is accepted, implementation work packages may be created and routed through Control.
