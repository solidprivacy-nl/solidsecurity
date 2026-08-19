# Selective Open-Source Adoption Register

## Decision rule

Evaluate external projects at the level of **specific capabilities and patterns**, not repository size or framework count.

No third-party runtime dependency enters SolidSecurity merely because it already implements many GRC features.

## Current decisions

| Project | License signal | Decision now | Adopt/reference now | Explicitly defer |
|---|---|---|---|---|
| `getprobo/probo` | MIT | REFERENCE / RUNTIME DEFERRED | control/measure/evidence separation, document approval, immutable/auditable workflow ideas, API/MCP-ready model | full deployment/fork; 270+ MCP surface; broad GRC UI |
| `intuitem/ciso-assistant-community` | AGPLv3 outside commercial `enterprise/` | CONCEPTUAL REFERENCE ONLY | requirement/control decoupling, reusable mappings, assessment object separation | code copying, bundled framework imports, runtime dependency without license strategy |
| `unidoc/isms` | Apache-2.0 | PATTERN REFERENCE / CODE DEFERRED | AI-as-suggestion, explicit agent identity, round-based human review, Git-backed document history | runtime adoption until service workflow is validated |
| `UnicisTech/unicis-platform-ce` | Apache-2.0 | WORKFLOW REFERENCE | privacy workflow patterns (RoPA/TIA/PIA), task and MCP concepts | platform import; broad trust-management runtime |
| `prowler-cloud/prowler` | Apache-2.0 | PHASE 4 CANDIDATE | later read-only technical evidence for cloud/M365/GitHub/etc. | MVP scanning or automatic compliance verdicts |
| `oscal-compass/compliance-trestle` | Apache-2.0 | PHASE 6 CANDIDATE | machine-readable compliance and Git-governed artifact concepts | OSCAL complexity before internal model stabilizes |
| `ComplianceAsCode/content` | verify before reuse | DEFERRED | conceptual compliance-as-code research only | importing technical control content into initial care/MKB service |

## Probo

Why relevant:

- clear risk/control/evidence primitives;
- self-hosting and permissive MIT license;
- strong MCP/API architecture;
- audit/evidence/document workflows.

Why not now:

- brings a full Go/Postgres/React/GraphQL/MCP GRC product before SolidSecurity has validated its own service workflow;
- would bias the product model toward existing software objects and UI;
- creates operational surface we do not yet need.

Decision gate after pilots: compare thin custom app vs Probo backend/hybrid against validated requirements.

## CISO Assistant

Most valuable pattern: decoupling compliance requirements from reusable controls and implementations.

License boundary: community code outside the enterprise directory is AGPLv3. Use architecture concepts and independent implementation only unless a deliberate legal/licensing decision authorizes more.

Do not bulk-copy its framework library.

## isms.sh

Most valuable pattern: AI is an explicit participant whose suggestions enter a human review/approval workflow with audit history. This is aligned with the SolidSecurity assurance model.

Apache-2.0 makes later targeted code reuse legally simpler than AGPL, but no code is needed during Foundation/Service MVP.

## Unicis

Useful mainly as a reference for privacy process objects and AI/MCP interaction with GRC tasks. Its breadth is not a reason to adopt the full platform.

## Prowler

Potential future role:

`read-only customer configuration -> technical observation -> evidence object`

Not:

`Prowler result -> automatic SolidSecurity compliance PASS`.

Connector access and evidence interpretation require separate data/security architecture.

## compliance-trestle / OSCAL

Potential later role: portable machine-readable interchange between controls, plans, assessments and external partners/auditors. Defer until SolidSecurity's own model is stable enough that an interchange standard solves a real problem.

## Third-party code admission checklist

Before any code/content reuse:

1. exact repository/tag/commit recorded;
2. exact license verified;
3. NOTICE/attribution obligations recorded;
4. copyleft implications reviewed;
5. security/maintenance health assessed;
6. capability maps to a validated SolidSecurity need;
7. exit/replacement path understood;
8. independent assurance reviews the adoption candidate.
