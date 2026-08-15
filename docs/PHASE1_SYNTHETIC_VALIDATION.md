# Phase 1 Synthetic Validation — Cross-Case Findings

Status: `SYNTHETIC EVIDENCE / NOT CUSTOMER VALIDATION`

This record summarizes lessons from the Care Alpha and Supplier Beta synthetic service executions. It must not be used to claim achieved customer savings, legal compliance, product-market fit or production readiness.

## Care Alpha

The fictitious small home-care case executed intake -> scope -> 15-control assessment -> evidence request -> findings -> 90-day plan -> draft policies -> baseline report.

Observed model behavior:

- 15 controls could be handled without a GRC platform;
- proposed results separated from proof strength cleanly;
- 9 controls reached proposed Proof Level 3 because evidence existed, while several still had PARTIAL/GAP results;
- generated policy drafts did not raise proof state;
- critical review topics were identifiable for a professional queue.

Modelled effort hypothesis (not measured customer performance): AI-assisted production 245 min, customer input 330 min, professional review 435 min.

## Supplier Beta

The fictitious 18-FTE SaaS supplier processed a 20-question internally authored healthcare security questionnaire from reusable claims/evidence.

Observed model behavior:

- 18/20 questions could reuse existing backbone information to some degree;
- 11 answers still carried professional-review flags because of qualifications, contracts, missing coverage or assurance wording;
- two questions exposed missing common-control categories instead of being forced into poor mappings;
- reusable passport/answer statements require validity and assurance metadata.

Modelled effort hypothesis (not measured customer performance): AI-assisted production 110 min, supplier input 120 min, professional review 200 min.

## Cross-case conclusions

### Confirmed

1. Service-first before platform remains justified.
2. Requirement, control, implementation claim, evidence, assessment, review and decision must remain separate.
3. Proof strength and assessment result are independent dimensions.
4. Evidence coverage/period/population/limitations need first-class fields.
5. Applicability requires unresolved states until professional review.
6. Broad controls need subordinate testable assertions.
7. AI can prepare high-volume structured work while material customer claims remain reviewable.
8. The Supplier questionnaire/passport workflow is a plausible thin-product wedge.

### Not yet proven

- actual percentage reduction in professional hours;
- customer willingness to pay at proposed price points;
- actual questionnaire reuse rate across real customers;
- external auditor acceptance of generated artifacts/evidence structure;
- production data-plane safety;
- legal applicability conclusions for any real organization.

## Foundation changes justified by both cases

- richer Evidence metadata;
- ControlAssertion entity;
- ApplicabilityDecision state enum;
- ReviewQueueItem;
- ApprovedAssertion/reusable answer concept;
- AssuranceLabels dimensions;
- four tech-supplier controls only.

## Next validation gate

Before real client data, complete Phase 2 pilot-readiness design and independently review the data governance/security boundary. When a real pilot begins, instrument actual elapsed customer/professional time, rework cycles, evidence-request completion, assessment changes by reviewer and customer outcome.
