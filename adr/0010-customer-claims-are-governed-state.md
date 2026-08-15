# ADR 0010 — Treat customer-facing assurance language as governed state

Status: proposed

## Context

The SolidSecurity business model depends on producing reports, passports, questionnaire answers and readiness statements quickly. AI makes wording cheap. That creates a specific risk: polished language can become stronger than the evidence/review state behind it.

## Decision

Customer-facing material claims are governed objects with explicit class, scope, provenance, evidence validity and assurance labels.

`evidence_linked`, `professionally_reviewed`, `independently_audited` and `certified` remain distinct dimensions. Restricted terms such as broad “compliant” or “certified” are denied by default unless their exact prerequisites are present.

Generated policies begin as drafts and do not prove operation. Semantic questionnaire mapping creates a proposed reusable answer, not authority to send a customer assurance statement.

## Consequences

A future report/passport generator must consume approved claim objects rather than free-form AI conclusions for material assertions. Human-only authority boundaries can be tested in CI and enforced in runtime later.
