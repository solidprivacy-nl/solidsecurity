# ADR 0004 — Separate product/control plane and client data plane

- Status: Accepted for Foundation V1
- Date: 2026-08-15

## Context

The project repository contains reusable methodology and governance. Real client dossiers will contain sensitive security, privacy and possibly health-related information.

## Decision

GitHub is the SolidSecurity product/control-plane source of truth. It must not become the client evidence/dossier store.

A separate secured client data plane must be designed and authorized before any real customer information is ingested.

## Consequences

The public repository can remain useful during early development without normalizing unsafe customer-data handling. A later data-plane architecture is a hard gate before controlled pilots.
