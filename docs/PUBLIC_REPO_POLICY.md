# Public Repository Information Policy

## Purpose

The repository is temporarily public for collaboration, transparency and GitHub Actions economics. Public visibility must not accidentally publish client data, secrets or the highest-value proprietary operating intelligence.

## Core assumption

**Anything committed to a public repository must be treated as permanently disclosed.**

Deletion or later conversion to private does not guarantee that clones, caches, forks or prior copies disappear.

## Classification

### PUBLIC_SAFE — allowed

Examples:

- high-level strategy and positioning;
- generic architecture;
- generic internally authored controls;
- public-source references;
- generic workflows;
- public ADRs;
- synthetic test data;
- non-sensitive roadmap;
- public-safe schemas;
- high-level open-source evaluations.

### PROPRIETARY_RESTRICTED — do not publish here

Examples:

- detailed cross-framework mapping matrices that constitute material SolidSecurity IP;
- evidence-sufficiency rubrics and scoring recipes;
- private control test procedures;
- accumulated remediation playbooks/benchmarks;
- internal pricing algorithms/margin models;
- production prompts/system instructions that materially encode proprietary method;
- partner contractual terms;
- unreleased security architecture details that raise exploitation risk.

These belong in a later private control/operations repository.

### CLIENT_CONFIDENTIAL — prohibited

Examples:

- client identities unless explicitly public and necessary;
- client policies/contracts;
- system, supplier and asset inventories;
- vulnerabilities;
- incidents;
- implementation claims;
- client assessments/evidence;
- staff/patient/client personal data;
- customer credentials or architecture.

These belong only in the approved client data plane.

### SECRET — prohibited everywhere except approved secret store

- API keys;
- passwords;
- tokens;
- private keys;
- signing material;
- database credentials;
- production secrets.

Never store secrets in Git, including private repositories.

## Pre-commit/publication test

Before committing material to this public repository ask:

1. Is it derived from or about a real customer?
2. Does it contain security-sensitive operational detail?
3. Does it contain a secret or credential?
4. Would disclosure materially reduce SolidSecurity's future competitive advantage?
5. Do we have redistribution rights for third-party content?

If any answer is uncertain, classify upward and do not publish until reviewed.

## Third-party standards

Do not assume that publicly accessible or zero-price standards may be redistributed. Store references and internally authored summaries unless licensing clearly permits copying.

## Repository transition triggers

Perform a formal public/private/open-core decision before the earliest of:

- first real client-data processing;
- material proprietary mapping/evidence rubric development;
- production application source containing sensitive security logic;
- commercial launch where competitors have a clear incentive to monitor the repository.

## Visibility options later

1. **Public core + private operations/IP** — preferred if public development remains strategically useful.
2. **Private repository** — simplest confidentiality model.
3. **Explicit open-core** — only after deliberate licensing/business-model decision.

## Licensing posture today

Public visibility is not an open-source grant. No general open-source license is currently granted by this repository. Third-party components retain their own licenses.
