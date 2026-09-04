# Public Repository Information Policy

## Purpose

The repository is public for collaboration, transparency and GitHub Actions economics. Public visibility must not accidentally publish client data, secrets or the highest-value proprietary operating intelligence.

## Core assumption

**Anything committed to a public repository must be treated as permanently disclosed.**

Deletion or later conversion to private does not guarantee that clones, caches, forks or prior copies disappear.

## R2 repository/IP decision

**Decision: public core + private operations/IP.**

The current `solidprivacy-nl/solidsecurity` repository remains the public-safe methodology, architecture, synthetic-validation and product-contract core. Commercially sensitive operating intelligence and private execution material belong in a separately access-controlled private operations/IP location.

This decision is effective immediately for R2. Until an approved private operations/IP location is provisioned, restricted material must **not** be created in this public repository merely to satisfy a workpackage deliverable. Public-safe contracts/templates may be committed; confidential values and operating intelligence remain blocked from publication.

The split is deliberately simple:

- **public core:** generic method, architecture, public-safe schemas/contracts, synthetic fixtures, high-level positioning and testable hypothesis structure;
- **private operations/IP:** detailed economics and margin assumptions, named prospect/partner intelligence, detailed competitor notes, proprietary mappings/rubrics/playbooks/prompts and accumulated operating learning;
- **client data plane:** real client records, evidence, assessments and other client-confidential data;
- **approved secret store:** credentials and secrets.

No open-core licensing grant is created by this decision. Public visibility and source availability remain distinct from an explicit open-source license.

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
- high-level open-source evaluations;
- public-safe commercial measurement contracts without confidential values or named pipeline intelligence.

### PROPRIETARY_RESTRICTED — do not publish here

Examples:

- detailed cross-framework mapping matrices that constitute material SolidSecurity IP;
- evidence-sufficiency rubrics and scoring recipes;
- private control test procedures;
- accumulated remediation playbooks/benchmarks;
- internal pricing algorithms, detailed rates, margin assumptions and package economics;
- named prospect, proposal, loss-reason and channel-partner intelligence;
- detailed competitor intelligence beyond deliberately public-safe positioning categories;
- production prompts/system instructions that materially encode proprietary method;
- partner contractual terms;
- unreleased security architecture details that raise exploitation risk.

These belong in the private operations/IP location.

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

1. Is it derived from or about a real customer or identifiable prospect?
2. Does it contain security-sensitive operational detail?
3. Does it contain a secret or credential?
4. Would disclosure materially reduce SolidSecurity's future competitive advantage?
5. Does it expose detailed rates, margins, pipeline intelligence or proprietary operating method?
6. Do we have redistribution rights for third-party content?

If any answer is uncertain, classify upward and do not publish until reviewed.

## Third-party standards

Do not assume that publicly accessible or zero-price standards may be redistributed. Store references and internally authored summaries unless licensing clearly permits copying.

## Repository transition triggers

Revisit the R2 decision before the earliest of:

- first real client-data processing;
- a material change in collaboration/visibility economics;
- production application source containing sensitive security logic;
- a deliberate open-source/open-core licensing decision;
- evidence that the public/private split causes material operational friction or IP leakage risk.

## Licensing posture today

Public visibility is not an open-source grant. No general open-source license is currently granted by this repository. Third-party components retain their own licenses.
