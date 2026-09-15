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

## R2 operating-IP application

The R2 launch work applies the existing boundary rather than creating a second storage architecture:

- the **public core** may contain generic method, public-safe schemas/contracts, synthetic fixtures, high-level positioning and testable commercial-measurement structures without confidential values;
- **private operations/IP** is the classification destination for detailed internal rates, package economics, margin assumptions, named non-client prospect/proposal/loss/channel intelligence, detailed competitor notes, proprietary mappings/rubrics/playbooks/prompts and accumulated operating learning;
- **client data plane** remains the only permitted destination for identifiable client or controlled design-partner records, evidence, assessments and attributable client interaction/outcome records;
- **approved secret store** remains the only permitted destination for credentials and secrets.

A private operations/IP location is provisioned only when the first restricted artifact actually needs durable persistence. Until then, restricted material is withheld rather than committed to this public repository. Deliberately de-identified or aggregated client-derived commercial learning may enter private operations/IP only when the source boundary and evidence class remain reconstructable without exposing the client record.

Public visibility and source availability do not create an open-source licensing grant.

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
- high-level open-source evaluations;
- public-safe commercial measurement contracts without confidential values, named pipeline intelligence, internal rates or margins.

### PROPRIETARY_RESTRICTED — prohibited here unless explicitly released

Examples:

- detailed cross-framework mapping matrices constituting material SolidSecurity IP;
- evidence-sufficiency rubrics/scoring recipes;
- private control test procedures;
- accumulated remediation playbooks/benchmarks;
- detailed internal pricing/margin models, loaded rates and package economics;
- named non-client prospect, proposal, loss-reason and channel-partner intelligence;
- detailed competitor intelligence beyond deliberately public-safe positioning categories;
- production prompts/system instructions materially encoding proprietary method;
- partner contractual terms;
- unreleased exploit-relevant security detail;
- accumulated real operational intelligence.

### CLIENT_CONFIDENTIAL — prohibited

Examples include client identities where unnecessary, controlled design-partner identities, policies/contracts, asset/system/supplier inventories, vulnerabilities/incidents, implementation claims, client assessments/evidence, attributable client interaction/outcome or willingness-to-pay records, and personal data.

These belong only in the approved client data plane.

### SECRET — prohibited in Git

API keys, passwords, tokens, private keys, signing material, database credentials and production secrets belong only in an approved secret store.

## Publication test

Before public commit ask:

1. Is it derived from or about a real customer, controlled design partner or identifiable prospect?
2. Does it contain security-sensitive operational detail?
3. Does it contain a secret or credential?
4. Would disclosure materially reduce SolidSecurity's future competitive advantage?
5. Does it expose detailed rates, margins, package economics, pipeline intelligence or proprietary operating method?
6. Do we have redistribution rights for third-party content?

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

## Decision review triggers

Revisit this public-core/private-operating-IP decision when a concrete business or risk requirement justifies it, including a material change in collaboration economics, an explicit open-source/open-core licensing decision, demonstrated operational friction, or evidence of IP leakage risk. Real-client processing remains separately governed by the client-data and security gates; it does not silently change this repository policy.

## Licensing posture

Public visibility is not an open-source grant. No general open-source license is granted by this repository unless a component explicitly states otherwise. Third-party components retain their own licenses.
