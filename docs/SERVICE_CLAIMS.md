# SolidSecurity Service Claims V1

Status: `INTERNAL CLAIMS CONTROL / DRAFT FOR PROFESSIONAL REVIEW`

## Purpose

Define what SolidSecurity may say about a client state without turning evidence, AI output or a professional review into a stronger assurance statement than has actually been established.

This document is a product/governance control, not legal advice or customer contract language.

## Core claim rule

A customer-facing statement must be no stronger than the **weakest material prerequisite** behind that statement.

Examples:

- a generated policy can support `DESIGNED`, not `IMPLEMENTED`;
- a customer declaration can support an implementation claim, not `VERIFIED`;
- evidence can support `EVIDENCE_LINKED`, including evidence that proves a GAP;
- professional review can support `PROFESSIONALLY_REVIEWED`, not automatically `INDEPENDENTLY_AUDITED`;
- only a legitimate independent assurance process may support `INDEPENDENTLY_AUDITED`;
- only an authorized certification body/process may support a certification claim.

## Claim classes

### C0 — Descriptive fact

Examples:

- “The organization supplied an incident procedure dated …”
- “MFA evidence was supplied for the following systems/population …”
- “The AI register contains three identified use cases.”

Requirements:

- source/provenance;
- client scope;
- date/freshness where material;
- limitations/coverage where material.

### C1 — Proposed assessment

Examples:

- “Proposed assessment: PARTIAL.”
- “Evidence gap identified for restore testing.”
- “Applicability remains UNDETERMINED pending professional review.”

May be produced by AI/operations but must be labelled `PROPOSED` and may not be represented as professional assurance.

### C2 — Evidence-linked statement

Examples:

- “This statement is linked to evidence items E-14 and E-19, valid through …”
- “The supplied evidence supports implementation for the stated population/time period.”

Evidence-linked does not imply satisfactory control result. The evidence may prove a deficiency.

### C3 — Professionally reviewed statement

A qualified authorized human has reviewed the relevant scope, claims, evidence, limitations and assessment and issued the recorded conclusion.

Allowed wording should identify:

- review scope;
- reviewer/review class;
- review date;
- evidence validity/limitations;
- whether the conclusion is an internal professional review or independent assurance.

### C4 — Independently assured/audited statement

Requires a legitimately independent reviewer/auditor and an assurance engagement/process appropriate to the claim. The implementation role cannot create this state for its own work.

### C5 — Certified statement

Requires a current certificate/decision from an authorized certification body for the exact organization/scope/version represented.

SolidSecurity readiness/support work does not itself create certification.

## Assurance labels remain independent

Customer-facing objects use separate labels rather than one “green compliant” badge:

- `self_declared`
- `evidence_linked`
- `professionally_reviewed`
- `independently_audited`
- `certified`

A statement may be evidence-linked and professionally reviewed without being independently audited or certified.

## Restricted claim families

The following wording requires explicit prerequisites and may never be generated as an unconditional default:

### “Compliant” / “fully compliant”

Requires a defined framework/version/scope, applicable requirements, current evidence and the review/decision authority appropriate to the context. For broad legal regimes this wording may remain inappropriate even when many controls are satisfactory.

Default product language should prefer precise states such as:

- “aligned to”;
- “readiness assessed against”;
- “evidence available for”;
- “professionally reviewed for the stated scope”;
- “open findings remain …”.

### “NIS2/Cbw compliant”

Never infer from organization size, an ISO/NEN alignment score or a questionnaire. Direct legal applicability and material conclusions require current authoritative-source and professional review.

### “NEN 7510 compliant”

Never infer merely from control mapping or policy presence. If discussing alignment/readiness, state exact scope and review status. Do not reproduce protected norm text without rights.

### “ISO 27001 certified”

Only with a current certificate for the exact certified scope. `Audit-ready` or `certification-ready` is a service outcome hypothesis, not certification.

### “AI Act compliant”

Never infer merely from having an AI register/policy. Use-case role/risk/applicability can remain pending professional review.

### “Independently assured”

Only when independence criteria are actually met and the assurance result is bound to the exact object/scope/evidence state.

### “No risk” / “secure” / “guaranteed safe”

Prohibited as absolute statements. Security and compliance are risk-management states, not guarantees.

## Expiry rule

A reusable customer-facing assertion cannot remain current beyond the earliest material expiry among:

- supporting evidence;
- professional review validity;
- certificate/audit validity where invoked;
- material framework/source version change;
- material client environment/process change known to SolidSecurity.

A statement that becomes stale transitions to `EXPIRED` or review-pending; it does not remain green because it was true once.

## Generated artifact rule

AI/generated policies, procedures and registers begin as `DRAFT` artifacts. Their existence cannot by itself change a control to implemented/effective.

Implementation requires, as applicable, accountable approval, communication, operational use, training, records and evidence of effectiveness.

## Questionnaire rule

A semantic match from a new customer question to an ApprovedAssertion is a **reuse proposal**, not authorization to send the answer. Contract-specific wording, SLA/notification commitments, data-location guarantees and material security claims route to review according to policy.

## Marketing rule

Marketing may explain the service model (“AI-assisted, professionally controlled”, “evidence-linked”, “continuous managed compliance”) but may not imply:

- regulator endorsement;
- certification authority;
- guaranteed compliance;
- legal advice by default;
- that AI autonomously determines compliance;
- that all customer controls are continuously technically monitored before connectors exist.
