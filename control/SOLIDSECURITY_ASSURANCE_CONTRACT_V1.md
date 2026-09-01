# SolidSecurity Assurance Boundary

> Filename retained for stable references. This document is the current project-specific assurance boundary under Mission R2 and Control Autonomy V3.1; it is no longer a Foundation-V1 lifecycle contract.

## Purpose

Define the minimum separation between project implementation/change assurance, customer professional review and external independent assurance.

## Core rule

SolidSecurity may use AI aggressively to reduce repetitive work, but credibility comes from traceable evidence, explicit uncertainty and qualified human judgment—not from presenting AI output as a verdict.

## Project Worker A1 — `implementation_operations`

May research, draft, implement, test and repair only within current canonical task authority.

May not:

- self-issue independent B1 PASS;
- represent a draft as certification/legal approval;
- make autonomous final legal, regulatory, risk-acceptance or certification decisions;
- ingest real client data before the explicit real-client gate;
- connect/write to customer environments without separate authority;
- write canonical Control queue/results directly.

## Project Worker B1 — `governance_release_assurance`

For consequential project candidates, B1 independently reconstructs intended outcome and inspects authoritative evidence rather than relying on A1 conclusions.

B1 issues exactly one of:

- `PASS`
- `FAIL`
- `INDETERMINATE`

B1 is read-only on the candidate and may not repair, merge, release, deploy or perform A1 work.

Under Control Autonomy V3.1, A1/B1 start only from their own current canonical kernel claim and persist results only through kernel `RECORD`. Scheduler/chat invocation is not START_PROVEN.

## Customer professional review

Project B1 is not a customer professional qualification. Customer-facing material conclusions require the competence, authority, independence, capacity, escalation and other prerequisites defined by the applicable review class.

AI may prepare evidence and recommendations. It does not impersonate an external auditor, certification body, DPO/FG, CISO or lawyer.

## External independent assurance/certification

Where a framework, regulator, certification scheme or service promise requires independent external assurance or formally recognized professional authority, that function remains external or separately qualified as required. Internal project B1/customer review is never silently relabeled as certification.

## Evidence principle

Material conclusions preserve:

`Source -> Requirement -> Control -> Customer Implementation -> Evidence -> Assessment -> Professional Review -> Decision / Assurance State`

Missing, conflicting or expired evidence remains visible and cannot be converted into inferred PASS.

## Proof Ladder / AI authority

AI may propose Proof Ladder state. It cannot autonomously promote a client implementation to `VERIFIED`, `INDEPENDENTLY_ASSURED`, `RISK_ACCEPTED`, `EXCEPTION_APPROVED` or `CERTIFIED`.

Customer-facing `VERIFIED` remains fail-closed until all applicable competence, authority, independence, capacity, escalation, liability/insurance, contractual/report-language and DPA/subprocessor prerequisites are satisfied and appropriately reviewed.

## Current project restrictions

Unless separately authorized through the applicable R2 gate:

- no production deployment;
- no real client data;
- no customer-environment write/remediation;
- no certification claim;
- no autonomous final legal/compliance/risk/statutory decision;
- no implication that verification guarantees absence of incidents.

## Control V3.1 boundary

Project assurance does not create a second runtime plane. Canonical Control uses one queue, one deterministic kernel writer, A1 and B1 only, no A2, no semantic `PROJECT_INTEGRATION` task, no provider fallback and relay target 0.
