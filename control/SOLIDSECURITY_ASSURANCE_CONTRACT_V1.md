# SolidSecurity Assurance Boundary

> Filename retained for stable references. This document is the current project-specific assurance boundary under Mission R2; it does not define or duplicate the central Control runtime implementation.

## Purpose

Define the minimum separation between project implementation/change review, customer professional review and external independent assurance.

## Core rule

SolidSecurity may use AI aggressively to reduce repetitive work, but credibility comes from traceable evidence, explicit uncertainty and qualified human judgment—not from presenting AI output as a verdict.

## Project implementation/change review

A project implementation function may research, draft, implement, test and repair only within current governed authority.

It may not:

- represent its own first-pass conclusion as sufficient review evidence for a consequential change;
- represent a draft as certification/legal approval;
- make autonomous final legal, regulatory, risk-acceptance or certification decisions;
- ingest real client data before the explicit real-client gate;
- connect/write to customer environments without separate authority;
- bypass the current central Control runtime contract.

For consequential project candidates, review is evidence-first and bound to the exact candidate/head/base and applicable acceptance criteria. The reviewer function must reconstruct the intended outcome and inspect authoritative repository/test/runtime evidence rather than relying on implementation claims.

A project-change review verdict is exactly one of:

- `PASS`
- `FAIL`
- `INDETERMINATE`

Candidate movement invalidates stale review. `INDETERMINATE` fails closed. A PASS does not silently grant merge, release, deployment or customer authority when a separate current gate applies.

Central Control may perform fresh same-runner critical review or call an external exact-candidate reviewer according to its current governed architecture. When the SolidSecurity workpackage, risk, or current Control/repository policy requires external or organizationally independent review, that requirement remains mandatory; this project does not weaken it by naming a local worker lane.

## Customer professional review

Project-change review is not a customer professional qualification. Customer-facing material conclusions require the competence, authority, independence, capacity, escalation and other prerequisites defined by the applicable review class.

AI may prepare evidence and recommendations. It does not impersonate an external auditor, certification body, DPO/FG, CISO or lawyer.

## External independent assurance/certification

Where a framework, regulator, certification scheme or service promise requires independent external assurance or formally recognized professional authority, that function remains external or separately qualified as required. Internal project/customer review is never silently relabeled as certification.

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

## Central Control boundary

Project assurance does not create a second runtime plane. SolidSecurity follows the current canonical central Control authority for scheduling, locks, queue mutation, runtime state and integration. Local project documentation must not freeze a Control version, worker topology, claim protocol or transport mechanism.

Project invariants remain: exact-candidate binding, deterministic mechanical validation, fresh critical review, required external/independent review when applicable, stale-review invalidation, no runtime bypass, no provider fallback introduced locally and zero principal relay as the target.
