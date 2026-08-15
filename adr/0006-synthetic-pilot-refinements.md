# ADR 0006 — Refine the Foundation only where synthetic workflows expose concrete need

Status: proposed

## Context

Care Alpha and Supplier Beta executed the Foundation model in two different workflows without a GRC runtime. Both cases exposed recurring data/model limitations, while Supplier Beta additionally exposed four distinct technical control objectives missing from the original 15-control seed.

## Decision

Adopt the following limited refinements:

1. Evidence gets explicit scope/population/period/sample/limitations metadata.
2. Assessment result remains independent from Proof Ladder level.
3. Stable controls may have subordinate ControlAssertions/test points.
4. Applicability supports unresolved/professional-review states.
5. Material/ambiguous items route through ReviewQueueItem.
6. Reusable customer claims/questionnaire answers use ApprovedAssertion with scope, evidence, validity and assurance labels.
7. Add exactly four tech-supplier control objectives: secure development, cryptographic protection, security logging/monitoring and independent technical testing.

## Rejected alternatives

- importing a broad ISO/NIST/CIS control library;
- turning every questionnaire question into a control;
- treating evidence presence as a positive control result;
- creating a full GRC runtime in response to synthetic workflow friction.

## Consequences

The Foundation becomes more precise but remains small. Future controls must still be justified by observed workflow need. Proprietary evidence-sufficiency rubrics and external-framework mappings remain outside the public foundation.
