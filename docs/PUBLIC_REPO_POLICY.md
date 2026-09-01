# Public Repository Information Policy

## Current decision

SolidSecurity uses a **public-safe product/model/schema/synthetic core with private/restricted operating IP by default**.

This is the canonical repository boundary before R2-WP01 produces material mapping/evidence logic:

- this public repository may contain deliberately public-safe methodology, generic internally authored controls, architecture, schemas, code, synthetic fixtures and non-sensitive roadmap material;
- proprietary detailed mappings, evidence-sufficiency rules, private prompts, detailed GTM/economics and accumulated operating intelligence are `PROPRIETARY_RESTRICTED` by default;
- client data is never product-repository data;
- secrets are never stored in Git;
- do **not** create a separate private repository/service speculatively: create the smallest private durable store/repository when the first restricted artifact actually needs to be persisted.

A later open-core/private-repo decision may supersede this boundary, but publication of restricted material always requires an explicit release decision.

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
- public-safe schemas/code;
- high-level open-source evaluations.

### PROPRIETARY_RESTRICTED — prohibited here unless explicitly released

Examples:

- detailed cross-framework mapping matrices constituting material SolidSecurity IP;
- evidence-sufficiency rubrics/scoring recipes;
- private control test procedures;
- accumulated remediation playbooks/benchmarks;
- detailed internal pricing/margin models;
- production prompts/system instructions materially encoding proprietary method;
- partner contractual terms;
- unreleased exploit-relevant security detail;
- accumulated real operational intelligence.

### CLIENT_CONFIDENTIAL — prohibited

Examples include client identities where unnecessary, policies/contracts, asset/system/supplier inventories, vulnerabilities/incidents, implementation claims, client assessments/evidence and personal data.

These belong only in the approved client data plane.

### SECRET — prohibited in Git

API keys, passwords, tokens, private keys, signing material, database credentials and production secrets belong only in an approved secret store.

## Publication test

Before public commit ask:

1. Is it derived from or about a real customer?
2. Does it contain security-sensitive operational detail?
3. Does it contain a secret or credential?
4. Would disclosure materially reduce SolidSecurity's future competitive advantage?
5. Do we have redistribution rights for third-party content?

If uncertain, classify upward and do not publish until reviewed.

## Third-party standards

Do not assume publicly accessible or zero-price standards may be redistributed. Store references and internally authored summaries unless licensing clearly permits copying.

## Storage decision when restricted material first appears

Use the simplest proven option that meets the need:

1. private Git repository for versioned operating IP/code/config where Git is appropriate;
2. approved private object/document storage for non-code artifacts;
3. approved client data plane for customer data;
4. approved secret store for credentials.

Do not create a new database, service, encryption subsystem or multi-repo topology merely to anticipate future restricted material.

## Licensing posture

Public visibility is not an open-source grant. No general open-source license is granted by this repository unless a component explicitly states otherwise. Third-party components retain their own licenses.
