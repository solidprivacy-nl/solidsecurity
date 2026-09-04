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

`product/change review != customer professional review != external independent assurance/certification`.

- Project/change review answers whether a repository candidate satisfies its governed change contract. It does not qualify the reviewer to issue customer assurance.
- Customer professional review is an engagement-scoped professional judgment under the applicable R2/R3/R4 routing class and customer gate.
- External independent assurance/certification is issued only by the appropriately independent/external authority. Internal customer review is not certification.

## Customer professional review classes

The public model defines the minimum authority contract; actual reviewer identity, credentials, capacity and loaded cost remain engagement/restricted operating evidence where appropriate.

The permitted claim classes below reuse the canonical identifiers from `model/claim_vocabulary.yaml`. They state what the **customer professional-review path itself** may issue. They do not grant external assurance or certification authority.

| Class | Human/authority requirement | Customer-facing `VERIFIED` authority | Permitted claim classes | Competence / credential expectation | Independence | Capacity / cost | Escalation |
| --- | --- | --- | --- | --- | --- | --- | --- |
| R0 | No human required; mechanical transformation only | Prohibited | C0, C1, C2 | Mechanical operation only; no professional judgment | N/A | No professional capacity/cost requirement | R1+ when work becomes non-mechanical/material |
| R1 | Human operational/sample reviewer | Prohibited | C0, C1, C2 | Trained internal operator for the defined process; credentials documented if the process requires them | Not independent assurance | Capacity and loaded-cost assumption required | R2 for material professional judgment |
| R2 | Qualified human professional | Permitted only after the complete customer-`VERIFIED` gate passes | C0, C1, C2, C3 | Scope competence recorded; applicable credential expectation documented and satisfied | Internal qualified review only where no material conflict compromises the review | Capacity confirmed; loaded-cost assumption recorded | Reassign to a competent/credential-satisfying reviewer, or escalate to R3 when competence, credentials, independence or material-conflict separation is insufficient |
| R3 | Qualified independent reviewer | Permitted only after the complete customer-`VERIFIED` gate passes | C0, C1, C2, C3 | Scope competence and applicable credentials recorded | Independent internal or external reviewer, separated from material design/operation/decision being assured | Capacity confirmed; loaded-cost assumption recorded | Reassign to a competent independent reviewer, or escalate to R4 when competence/credentials remain insufficient or external authority/certification is required |
| R4 | External authority/certification-body/regulator dependent routing | Internal authority is insufficient; external-authority outcome governs | C0, C1, C2, C3 | External authority's competence/credential rules | External authority | Capacity and loaded-cost assumptions are required | External authority/certification body/regulator |

Insufficient competence or unmet applicable credentials are blockers, not softer review-quality concerns. They leave the prerequisite unresolved and require reassignment/escalation; they can never be waived merely because independence is otherwise acceptable.

`C4_INDEPENDENTLY_ASSURED` and `C5_CERTIFIED` are **not** permitted claim classes of any customer professional-review class. C4 requires a separate independent-assurance result with the required independence and scope; C5 requires an authorized certification process/formal decision. R4 therefore means “route to the required external authority,” not “internal R4 may certify.”

A control/workflow may require a stronger class. A weaker actual class never substitutes for a stronger required class.

### Capacity and loaded-cost assumption record

R1–R4 capacity/cost prerequisites use one exact public-safe reference shape defined in `model/ai_authority.yaml`. The underlying numeric capacity/cost values use the existing canonical `INTERNAL` data classification from `model/data_classification.yaml`, so they remain outside public Git; this does not introduce a second classification or storage tier.

Every assumption record has the common metadata fields:

- `review_class`;
- `assumption_type` (`reviewer_capacity` or `loaded_cost`);
- `unit`;
- `evidence_status` using the current commercial evidence-status contract in `docs/COMMERCIAL_MODEL.md`;
- `mission_evidence_class` using the exact identifiers from `model/mission_operating_model_r2.yaml:evidence_classes`;
- attributable `calculation_reference`;
- `restricted_record_ref` pointing to the non-public value/evidence record.

Type-specific metadata is deliberately minimal:

- `reviewer_capacity` uses `professional_minutes_per_month` and needs no additional public field;
- `loaded_cost` uses `currency_per_professional_hour` and additionally requires `currency_code` using ISO 4217 so a rate is not ambiguous across currencies.

The public-safe contract shape is exact. It contains no numeric assumption `value`, embedded assumption-record collection, or alternative public value field. Adding such a field is a validation failure. A missing restricted reference, unit, status/evidence classification, calculation reference or required currency code leaves the prerequisite unresolved; it does not default to satisfied.

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
- R4 — route to the required external authority/certification/regulator-dependent process.

Each control, mapping and workflow step may define a minimum review class. Insufficient competence, unmet applicable credentials, material conflict or independence concerns require reassignment/escalation rather than being waived to preserve throughput.

## Prompt and model neutrality

The authority model must survive a change of LLM vendor/model. Trust is provided by workflow, evidence and review controls rather than assumed model quality.
