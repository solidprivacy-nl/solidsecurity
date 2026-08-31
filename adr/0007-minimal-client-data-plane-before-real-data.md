# ADR 0007 — Build a minimal secure client data plane before any real client dossier

Status: proposed

## Decision

Real client data will not be placed in GitHub or ad-hoc collaboration folders. Before first pilot, SolidSecurity requires a tenant-aware client data plane with encrypted structured metadata, private evidence objects, access control, audit history, lifecycle/delete and governed AI processing.

The first runtime remains deliberately thin: secure intake + evidence/state + professional review. A full GRC platform is not required.

## Rationale

Compliance/security evidence contains sensitive business, infrastructure and sometimes personal information. The AI/service model cannot safely scale if client dossiers live in uncontrolled documents or public/private Git history.

## Consequence

Provider selection and deployment become explicit gated work before a real pilot, but broad product features and environment scanning remain deferred.
