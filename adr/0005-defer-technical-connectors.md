# ADR 0005 — Defer customer-environment connectors

- Status: Accepted for Foundation V1
- Date: 2026-08-15

## Context

Tools such as Prowler can automatically inspect M365, cloud and other environments. Integrating them early adds credentials, permissions, tenant isolation, data retention and interpretation complexity before SolidSecurity knows which observed evidence is most valuable.

## Decision

No automatic customer-environment connection or scanning in Foundation or Service MVP. Validate the manual/AI-assisted evidence workflow first.

Read-only connectors may enter a later phase when evidence requirements are proven.

## Consequences

Early delivery is simpler and safer. Technical evidence automation arrives later but is more likely to solve validated problems rather than create a feature-heavy platform.
