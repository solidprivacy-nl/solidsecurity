# ADR 0008 — Minimize model context and prohibit cross-tenant AI memory

Status: proposed

## Decision

AI receives only task-required client content through tenant-scoped orchestration. Cross-tenant model memory/retrieval is prohibited. External processing of high-sensitivity client content is denied by default. Permanent embeddings are not required for the first pilot.

## Rationale

The economic leverage comes from structured analysis/drafting, not from sending every client dossier wholesale to a model provider. Minimization reduces confidentiality, privacy, deletion and prompt-injection risk while preserving most early value.

## Consequence

The initial AI pipeline favors explicit document selection, redaction/structured extraction and provenance. Future vector/RAG architecture requires a separate security/data-governance decision.
