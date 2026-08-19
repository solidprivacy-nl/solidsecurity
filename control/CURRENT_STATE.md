# SolidSecurity Current State

## Status

`FOUNDATION_IMPLEMENTATION / CANDIDATE`

Control-managed: **yes**

Concept/onboarding contract: issue #1

Active foundation work contract: **issue #2**

Working branch: `agent/foundation-v1`

## Authority transition

On 2026-08-15 the principal explicitly accepted the discussion-ready strategy and authorized autonomous realization of the agreed strategy, architecture, model, workflows and roadmap.

This lifts the concept-stage hold on **foundation implementation only**.

It does not authorize:

- production deployment;
- real client data;
- customer-environment scanning;
- autonomous final legal/compliance/certification decisions;
- certification claims;
- bypass of independent assurance for consequential work.

## Current objective

Produce SolidSecurity Foundation V1 as a coherent source-of-truth backbone for an AI-native managed security & compliance service for small healthcare organizations and compliance-exposed SMEs.

## Current architecture stance

1. Model/service first; platform later.
2. Common controls are separate from external requirements.
3. Client implementation claims and evidence are separate from generic controls.
4. AI works through attributable suggestions/analysis and cannot self-authorize professional assurance.
5. GitHub is the product/control plane, not the client data plane.
6. Technical environment connectors are deferred until after workflow validation.
7. External open-source projects are selectively adopted by capability/pattern, never wholesale by feature count.

## Repository visibility

Repository remains public by principal choice during the early foundation phase.

Only `PUBLIC_SAFE` project material is authorized here. Secrets, real client data, sensitive implementation details, proprietary evidence-sufficiency rubrics, private prompts and commercially sensitive accumulated operating intelligence are prohibited from the public repo.

See `docs/PUBLIC_REPO_POLICY.md`.

## Next gates

1. Complete Foundation V1 candidate on `agent/foundation-v1`.
2. Submit PR against `main`.
3. Obtain independent assurance under `control/SOLIDSECURITY_ASSURANCE_CONTRACT_V1.md`.
4. After acceptance/merge, execute Phase 1 synthetic Service MVP work packages.
