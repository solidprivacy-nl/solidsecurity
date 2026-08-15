# ADR 0001 — Foundation before platform

- Status: Accepted for Foundation V1
- Date: 2026-08-15

## Context

Mature open-source GRC platforms already exist, especially Probo, CISO Assistant, isms.sh and Unicis. Adopting a full platform now would force premature implementation and operational complexity before SolidSecurity has validated its managed-service workflow.

## Decision

Build and validate the SolidSecurity operating model, control model, data model and service workflows before choosing a production GRC runtime.

Phase 1 may be executed with simple structured artifacts and AI/professional workflow rather than a dedicated application.

## Consequences

Positive: lower complexity, preserves architectural choice, reveals actual product requirements.

Negative: some early workflow remains manual and later migration may be required.
