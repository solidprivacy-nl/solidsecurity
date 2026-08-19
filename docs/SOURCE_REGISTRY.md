# Source and Rights Registry

## Purpose

Track authoritative regulatory inputs, framework references and external code sources with version/freshness/licensing awareness.

This file does not grant redistribution rights for any source.

## Regulatory / standards sources

| Source | Role | Current handling |
|---|---|---|
| Dutch Cybersecurity Act (Cbw) and implementing material | primary Dutch NIS2 legal source | cite official government/NCSC sources; requirements modeled from authoritative text/guidance |
| EU NIS2 Directive 2022/2555 | European legal source | cite EUR-Lex; use primarily for context where Dutch Cbw is controlling |
| ADR/NOREA Cbw (NIS2) Control Framework | practical evaluation/mapping reference | use as analytical reference; verify redistribution rights before importing any matrix/content |
| NEN 7510:2024 / current amendments | healthcare information-security standard | reference identifiers and internally authored controls/summaries; do not assume zero-price access permits republication |
| ISO/IEC 27001:2022 | certification/ISMS standard | reference only unless licensed content use is explicitly authorized; avoid verbatim publication |
| GDPR / Regulation (EU) 2016/679 | privacy legal source | cite official EUR-Lex/authority sources |
| EU AI Act / Regulation (EU) 2024/1689 | AI governance legal source | cite official EUR-Lex/Commission sources; applicability/classification requires professional review |

## Current regulatory timing notes

- Dutch Cbw enters into force on **15 August 2026** according to Dutch government/NCSC announcements.
- The EU AI Act generally applies from **2 August 2026**, with staged exceptions and later applicability for specified provisions.
- NEN 7510:2024 is the current healthcare information-security norm family; always verify latest amendments/version before client assessment.

These notes are navigation aids, not a substitute for current legal verification during an engagement.

## Open-source references

| Project | Repository | License status verified for evaluation |
|---|---|---|
| Probo | `getprobo/probo` | MIT |
| CISO Assistant Community | `intuitem/ciso-assistant-community` | AGPLv3 outside commercially licensed enterprise directory |
| isms.sh | `unidoc/isms` | Apache-2.0 |
| Unicis Platform CE | `UnicisTech/unicis-platform-ce` | Apache-2.0 |
| Prowler | `prowler-cloud/prowler` | Apache-2.0 |
| compliance-trestle | `oscal-compass/compliance-trestle` | Apache-2.0 |

## Freshness rule

Each production/client engagement must resolve the current authoritative source/version rather than assuming the repository's last known reference is still current.

## Rights rule

Separate three questions:

1. Is the source accessible?
2. May SolidSecurity use it internally?
3. May SolidSecurity redistribute/copy it in a public or commercial product?

Do not infer (3) from (1) or (2).
