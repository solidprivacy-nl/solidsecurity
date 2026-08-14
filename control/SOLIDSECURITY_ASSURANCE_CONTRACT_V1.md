# SolidSecurity Assurance Contract V1

## Purpose

Define the minimum project-specific separation between AI-assisted implementation/operations and independent professional or governance assurance.

## Core rule

SolidSecurity may use AI aggressively to reduce repetitive compliance work, but credibility must come from traceable evidence, explicit uncertainty and qualified human judgment—not from presenting AI output as a verdict.

## Role A — implementation_operations

May:

- perform research and structured analysis;
- draft policies, registers, assessments, mappings and remediation proposals;
- organize supplied evidence;
- maintain project documentation and workflows;
- implement software and automation after authorization;
- test and repair implementation candidates.

May not:

- issue an independent assurance PASS on its own work;
- represent a draft as certification or legal approval;
- make autonomous final legal, regulatory, risk-acceptance or certification decisions;
- ingest real client data unless explicitly authorized under a later data-governance contract.

## Role B — governance_release_assurance

For consequential candidates, Role B must independently reconstruct the intended outcome and inspect authoritative evidence rather than relying on Role A's conclusion.

Role B may issue only:

- `PASS`
- `FAIL`
- `INDETERMINATE`

Role B may not silently modify the candidate it assures.

## Professional assurance boundary

Where a service claim requires professional judgment, legal interpretation, NEN/ISO assessment independence, certification-body authority or regulator-facing responsibility, an appropriately qualified human professional remains the final decision authority.

AI and internal assurance may prepare and challenge the evidence, but they do not impersonate an external auditor, certification body, DPO/FG, CISO or lawyer.

## Independence

Where a framework, regulator or service promise requires an independent assessment, the reviewer must not be the same person or role that designed or implemented the material control being independently assessed. SolidSecurity must preserve that separation in both workflow and evidence.

## Evidence principle

Material conclusions should be traceable, where applicable, through:

`obligation/framework -> control -> implementation claim -> evidence -> analysis -> review -> decision`

Missing or contradictory evidence must remain visible and may not be converted into an inferred PASS.

## Concept-stage restrictions

During the current concept stage:

- no production deployment is authorized;
- no customer-environment connection or continuous scanning is authorized;
- no real client data is authorized;
- no certification claim is authorized;
- no autonomous final legal/compliance decision is authorized.

## Evolution

The enforcement maturity may increase from `LEVEL_1_CHECKLIST` as the product becomes executable. Any later hard CI/release gate, client-data processing, environment connector, or post-action verification requirement must be explicitly added to project governance before use.
