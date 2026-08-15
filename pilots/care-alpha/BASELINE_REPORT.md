# SolidSecurity Care Baseline — Synthetic Draft

**Organization:** Fictieve Thuiszorgorganisatie Aurora  
**Status:** synthetic demonstration only  
**Assessment authority:** implementation proposal; no professional assurance performed

## Executive view

The synthetic organization has basic security/privacy practices but operates them largely through informal ownership, outsourced ICT and scattered documents. The most material weaknesses are incomplete authentication coverage, unproven recovery, unmanaged AI use, stale incident/risk governance and absence of a recurring control-effectiveness cycle.

A 90-day stabilization programme is practical without first deploying a GRC platform. The service can operate from structured inventories, evidence, findings and governed professional review.

## Proposed control state

15 SolidSecurity controls were assessed from synthetic claims/evidence:

- `SATISFACTORY_WITH_MINOR_ACTION`: 1
- `PARTIAL`: 8
- `GAP`: 6

Proposed Proof Ladder distribution:

- Level 0 — Unknown/not implemented as required: 3
- Level 1 — Designed: 2
- Level 2 — Implementation declared: 1
- Level 3 — Evidenced: 9
- Level 4 — Professionally verified: **0**
- Level 5 — Independently assured: **0**

A Level 3 item can still be `PARTIAL` or `GAP`: evidence can prove a deficiency. Proof level and control result are deliberately separate.

## Critical findings

1. MFA coverage across all material access paths has not been established.
2. Restore/recovery effectiveness for critical information is not evidenced.
3. AI tools/features are in use without an approved inventory, rules or classification process.
4. Incident response is documented but stale and untested.

## High-priority findings

- security risk assessment is stale;
- periodic access recertification is absent;
- critical supplier governance lacks active review;
- processing register is outdated;
- recurring control/management review is absent.

## 90-day direction

First stabilize authentication, recovery, AI use, incident readiness and the risk register. Then formalize assets/access/supplier/privacy governance, followed by practical exercises and management review. Detailed actions are in `REMEDIATION_90D.md`.

## Framework interpretation boundary

This draft does **not** conclude that the organization is or is not compliant with NEN 7510, Cbw/NIS2, GDPR, ISO 27001 or the EU AI Act. Those conclusions depend on authoritative-source applicability, professional interpretation, evidence quality and—where applicable—independent audit/certification authority.

## Professional review queue

A qualified reviewer should at minimum determine:

- final scope/applicability;
- whether authentication gaps are material and what compensating controls are acceptable;
- whether recovery evidence is sufficient;
- AI-use legal/risk classification, especially the care-note feature;
- whether evidence coverage/freshness justifies proposed assessment results;
- final prioritization and any risk acceptance.
