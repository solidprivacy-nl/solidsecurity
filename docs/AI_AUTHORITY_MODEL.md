# AI Authority Model

## Principle

**AI is leverage, not the source of trust.**

AI may reduce repetitive work aggressively, but authority increases only through explicit policy and review. AI confidence is not equivalent to professional assurance.

`model/ai_authority.yaml` is the machine-readable authority source. This document explains that contract; it does not create a parallel authority model.

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

## Trust-domain separation

These are different authorities and must never be silently equated:

`product/change B1 assurance != customer professional review != external independent assurance/certification`.

- Project B1 answers whether a repository candidate satisfies its governed change contract. It does not qualify the reviewer to issue customer assurance.
- Customer professional review is an engagement-scoped professional judgment under the applicable R2/R3 review class and customer gate.
- External independent assurance/certification is issued only by the appropriately independent/external authority. Internal R2/R3 review is not certification.

## Customer professional review classes

The public model defines the minimum authority contract; actual reviewer identity, credentials, capacity and loaded cost remain engagement/restricted operating evidence where appropriate.

| Class | Human/authority requirement | Customer-facing `VERIFIED` authority | Competence / credential expectation | Independence | Capacity / cost | Escalation |
| --- | --- | --- | --- | --- | --- | --- |
| R0 | No human required; mechanical transformation only | Prohibited | Mechanical operation only; no professional judgment | N/A | No professional capacity/cost requirement | R1+ when work becomes non-mechanical/material |
| R1 | Human operational/sample reviewer | Prohibited | Trained internal operator for the defined process; credentials documented if the process requires them | Not independent assurance | Capacity and loaded-cost assumption required | R2 for material professional judgment |
| R2 | Qualified human professional | Permitted only after the complete customer-`VERIFIED` gate passes | Scope competence recorded; applicable credential expectation documented and satisfied | Internal qualified review only where no material conflict compromises the review | Capacity confirmed; loaded-cost assumption recorded | R3 when independence/material conflict requires separation |
| R3 | Qualified independent reviewer | Permitted only after the complete customer-`VERIFIED` gate passes | Scope competence and applicable credentials recorded | Independent internal or external reviewer, separated from material design/operation/decision being assured | Capacity confirmed; loaded-cost assumption recorded | R4 where external authority/certification is required |
| R4 | External authority/certification-body/regulator dependent | Internal authority is insufficient; external-authority outcome governs | External authority's competence/credential rules | External authority | Engagement capacity/cost assumption recorded where relevant | External authority/certification body/regulator |

A control/workflow may require a stronger class. A weaker actual class never substitutes for a stronger required class.

## Customer `VERIFIED` fail-closed gate

WP03 defines readiness requirements but **does not enable customer-facing `VERIFIED` claims**. The machine-readable gate remains `DESIGN_ONLY` and `customer_verified_currently_enabled: false`.

Before a customer-facing `VERIFIED` state can ever be created, every applicable prerequisite must be recorded as satisfied:

- required review class;
- reviewer identity and scope competence;
- applicable credential expectation;
- independence requirement;
- reviewer capacity;
- loaded-cost assumption;
- escalation path;
- liability/insurance posture;
- contractual scope and liability limits;
- approved report language;
- post-verification incident/breach posture;
- customer contract/DPA;
- subprocessor review;
- retention/deletion schedule.

Missing, unknown, expired or unresolved prerequisites fail closed to `NEEDS_REVIEW`; they never default to `VERIFIED`.

The legal/insurance/contract prerequisites are readiness items for qualified external review. This workpackage does not approve legal terms, declare insurance coverage adequate, or create customer authority.

## Review routing

Review intensity is risk-based:

- R0 — no human review needed for purely mechanical/public-safe transformations;
- R1 — sample/operational review;
- R2 — mandatory qualified professional review;
- R3 — independent reviewer required;
- R4 — external authority/certification/regulator-dependent.

Each control, mapping and workflow step may define a minimum review class. Material conflict or independence concerns escalate rather than being waived to preserve throughput.

## Prompt and model neutrality

The authority model must survive a change of LLM vendor/model. Trust is provided by workflow, evidence and review controls rather than assumed model quality.
