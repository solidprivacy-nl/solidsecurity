# LLM and AI Processing Policy V1

## Purpose

Use AI aggressively for leverage without turning a model provider into an uncontrolled client-data repository or decision authority.

## Non-negotiable rules

1. Client data is never used to train SolidSecurity or third-party foundation models unless a future explicit client/legal basis authorizes a separate programme. Default is **no training**.
2. No cross-tenant conversation memory, vector index or agent memory.
3. Only the minimum data required for the task is passed to a model.
4. `CLIENT_HIGH_SENSITIVITY` content is denied to external model processing by default.
5. Every permitted model route must have documented provider, region/data-location assumptions, DPA/terms, retention controls, subprocessors and no-training posture.
6. Material model output is `PROPOSED`, attributable to model/version/policy/input references and subject to required professional review.
7. Prompt/content logging by providers must be disabled or contractually controlled where supported; SolidSecurity logs metadata/provenance, not unnecessary prompt bodies.

## Data-class routing

### PUBLIC / INTERNAL

May be processed by approved models according to ordinary platform policy.

### CLIENT_CONFIDENTIAL

May be processed only through an approved enterprise/API route with contractual data protection, configured retention/no-training safeguards and tenant-scoped orchestration.

### CLIENT_HIGH_SENSITIVITY

Default: do not send to external LLM. Prefer redaction, structured extraction, local/controlled processing or human review. Any exception requires documented necessity, client agreement where required, privacy/security review and an approved provider route.

### SECRET

Never send to an LLM. Credentials/tokens/keys should be removed at ingestion and stored only in the secret manager when legitimately required.

## Prompt-injection/content risk

Uploaded client documents are untrusted input. Model orchestration must treat embedded instructions as data, not authority. Tools/actions remain allowlisted and governed outside the document context.

## Retrieval

First pilot uses explicit selected-artifact context where feasible. Persistent embeddings/vectorization are deferred until their retention, deletion and tenant-isolation behavior has been reviewed.

## Model change control

Changing provider/model/region/retention configuration is a material data-processing change and requires documented review before use with real client data.
