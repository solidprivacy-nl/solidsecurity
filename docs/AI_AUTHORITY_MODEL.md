# AI Authority Model

## Principle

**AI is leverage, not the source of trust.**

AI may reduce repetitive work aggressively, but authority increases only through explicit policy and review. AI confidence is not equivalent to professional assurance.

## Authority classes

### GREEN — autonomous preparation allowed

Examples:

- inventory uploaded documents;
- extract candidate systems, suppliers and processes;
- summarize public regulatory sources;
- draft policies/procedures from approved templates;
- propose requirement/control mappings;
- identify inconsistencies or missing fields;
- organize evidence;
- pre-fill questionnaires from approved evidence;
- generate draft management reports;
- compare versions and flag changes.

Outputs remain attributable and reversible.

### AMBER — AI recommends, authorized human decides

Examples:

- client/framework applicability;
- Cbw/NIS2 scope interpretation;
- AI Act use-case classification;
- DPIA trigger recommendation;
- risk score/treatment recommendation;
- evidence sufficiency;
- control maturity/proof-level promotion;
- material finding severity;
- exception proposal;
- legal/regulatory interpretation with client impact.

### RED — human/professional authority required

AI must not autonomously:

- issue a final compliance/legal verdict;
- accept material residual risk;
- approve a material security exception;
- decide final regulator/incident-reporting obligations;
- sign management accountability statements;
- claim independent audit/certification;
- impersonate a DPO/FG, CISO, lawyer, auditor or certification body;
- make destructive/write changes in a customer environment under the current architecture.

## State transition constraints

AI may create:

`DRAFT`, `PROPOSED`, `NEEDS_REVIEW`, `CONFLICT_DETECTED`.

AI may not independently create:

`VERIFIED`, `RISK_ACCEPTED`, `EXCEPTION_APPROVED`, `CERTIFIED`, `INDEPENDENTLY_ASSURED`.

## Agent identity

A future runtime should distinguish human and AI actors explicitly. Material AI actions should be logged with actor/model, source provenance, timestamp and review disposition.

## Review routing

Review intensity is risk-based:

- R0 — no human review needed for purely mechanical/public-safe transformations;
- R1 — sample/operational review;
- R2 — mandatory qualified professional review;
- R3 — independent reviewer required;
- R4 — external authority/certification/regulator-dependent.

Each control, mapping and workflow step may define a minimum review class.

## Prompt and model neutrality

The authority model must survive a change of LLM vendor/model. Trust is provided by workflow, evidence and review controls rather than assumed model quality.
