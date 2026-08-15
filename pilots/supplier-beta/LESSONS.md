# Lessons from Synthetic Supplier Beta

## 1. Questionnaire reuse is a credible acquisition wedge

A small supplier feels the pain directly: security questionnaires consume sales, engineering and management time and can block deals. The same evidence can answer many differently worded questions. This is a more concrete buying trigger than “buy a GRC platform”.

## 2. Add an Answer/Assertion entity

The Foundation data model has ImplementationClaim and Artifact but a repeatable questionnaire service needs an `ApprovedAssertion` (or `ReusableAnswer`) object with: canonical wording, scope, linked controls, evidence, validity window, reviewer, approved uses and customer-specific exclusions.

## 3. Semantic mapping needs confidence plus a human boundary

AI can map a new question to likely controls/answers, but ambiguous or contract-sensitive questions must surface for review. Never silently convert semantic similarity into a customer assurance statement.

## 4. Passport claims need expiry inheritance

A passport statement should expire when its critical supporting evidence expires. “Current” must be computable, not a static PDF label.

## 5. The 15-control seed is sufficient for Care discovery but not for a technology supplier

The supplier case exposes missing dedicated controls for:

- secure software development;
- cryptography/key management;
- security logging/monitoring;
- independent application assurance/penetration testing.

Do not force these into unrelated controls just to make the mapping complete.

## 6. Customer-contract questions form a separate answer class

Incident-notification commitments, data-location promises, SLA and indemnity questions depend on the contract/customer context. They should never be globally reusable without qualifiers.

## 7. Early product opportunity is thinner than GRC

A questionnaire parser + reusable answer/provenance store + evidence validity + review queue can deliver a large part of the Supplier value proposition before building full GRC software.

## 8. Assurance labels must be explicit

Passport UI/data should separately expose: self-declared, evidence-linked, professionally reviewed, independently audited and certified. One green “compliant” badge would be misleading.
