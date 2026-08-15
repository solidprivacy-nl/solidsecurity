# Lessons from Synthetic Care Alpha

## 1. Proof level and assessment result must remain independent

The pilot confirms a crucial design rule: strong evidence can prove a bad state. `SS-ACCESS-001` has Level-3-quality synthetic evidence for only part of the access population and still results in a GAP. A single maturity/compliance score would hide this distinction.

## 2. Evidence needs explicit coverage metadata

`freshness` alone is insufficient. Evidence needs fields for population/systems/time-period covered, exclusions and sampling basis. Future model refinement should add `coverage_scope`, `coverage_period`, `population`, `sample_basis` and `limitations` as first-class fields.

## 3. Controls need testable assertions or aspects

Broad controls such as access lifecycle contain multiple aspects: approval, change, removal and recertification. A single result becomes ambiguous. Keep a stable common control objective, but allow `control_assertions`/`test_points` beneath it.

## 4. Applicability must support UNDETERMINED

Legal/regulatory applicability cannot be forced into yes/no during intake. `APPLICABLE`, `NOT_APPLICABLE`, `UNDETERMINED`, `PENDING_PROFESSIONAL_REVIEW` are needed.

## 5. Contradictory evidence is valuable

Evidence should explicitly support or contradict a claim. The AI interview note proving unmanaged AI use is evidence of a control deficiency, not evidence that the AI governance control is implemented.

## 6. Professional review should be queue-based and materiality-driven

The reviewer should not reread everything equally. Critical gaps, legal applicability, AI classification, exceptions, risk acceptance, evidence coverage conflicts and customer-facing conclusions should automatically enter a high-priority review queue.

## 7. Generated policies are implementation artifacts, not evidence of operation

The pilot can generate concise draft policies quickly, but their mere existence must never increase the Proof Ladder beyond `Designed`. Approval, communication, training and operational records are separate evidence.

## 8. Customer-facing reporting should show counts and critical exceptions

Avoid a single percentage such as “82% compliant”. Show result counts, Proof Ladder counts, unresolved critical findings, evidence freshness and review status.

## 9. AI-use governance fits naturally into the same control/evidence model

No separate AI-compliance product is needed for basic use. AI use cases become assets/activities linked to vendors, data classes, risks, controls and professional classification decisions.

## 10. Phase 3 product requirements are becoming concrete

A future thin application should prioritize: structured intake, control/assertion register, evidence coverage/freshness, findings/actions, professional review queue, recurring calendar and audit-ready export. A broad enterprise GRC suite is still not justified by this pilot.

## Proposed follow-up

After independent Foundation assurance, fold the evidence-coverage, control-assertion and applicability-state refinements into the canonical data model before a real customer pilot.
