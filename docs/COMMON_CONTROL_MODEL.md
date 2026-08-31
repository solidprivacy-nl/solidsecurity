# SolidSecurity Common Control Model

## Purpose

Create one reusable set of control objectives that can support multiple laws, standards, customer requirements and assurance contexts.

The Common Control Model (CCM) is the normalization layer between external requirements and client implementations.

## Why

Separate checklists create duplicate work:

`NEN requirement -> evidence A`

`ISO requirement -> evidence A again`

`Cbw requirement -> evidence A again`

SolidSecurity instead models:

`external requirements -> SS control -> client implementation -> reusable evidence`

The synthetic Care and Supplier executions added an important refinement:

`SS control -> testable assertions -> client claims/evidence`

The control remains stable and reusable; assertions let us assess distinct aspects without inventing a new top-level control for every questionnaire wording.

## Control domains V1.1

| Code | Domain | Intent |
|---|---|---|
| GOV | Governance & accountability | ownership, policy, management responsibility |
| RISK | Risk management | identify, assess, treat and review risk |
| ASSET | Assets & information | know systems, information and critical dependencies |
| ACCESS | Identity & access | authenticated, least-privilege and reviewed access |
| OPS | Secure operations | vulnerability, update and operational hygiene |
| DEV | Secure development | security in software/change lifecycle |
| CRYPTO | Cryptographic protection | risk-appropriate protection and key practices |
| MON | Security logging & monitoring | record and detect material security events |
| INC | Incident management | detect, respond, report and learn |
| RES | Resilience & continuity | backup, restore, continuity and recovery |
| SUP | Supplier & chain security | identify and manage third-party risk |
| PRIV | Privacy & data governance | controlled personal-data processing and safeguards |
| AI | AI governance | inventory, classify, govern and oversee AI use |
| PEOPLE | People & awareness | competence, training and responsibilities |
| ASSURE | Assurance & improvement | evidence, review, testing, audit and corrective action |

## Control identifier

`SS-<DOMAIN>-<NNN>`

Example: `SS-ACCESS-001`.

## Control fields

Required public-safe fields:

- `id`
- `domain`
- `title`
- `objective`
- `control_type`
- `default_evidence_classes`
- `minimum_review_class`
- `lifecycle_state`

Private/controlled fields later may include:

- detailed evidence-sufficiency rubric;
- proprietary test procedure;
- accumulated remediation recipes;
- customer benchmarking;
- commercially sensitive crosswalk weighting.

## Control assertions

Assertions are subordinate test points, not new framework obligations. They are useful when a control has multiple independently testable aspects.

Example `SS-ACCESS-002 Access lifecycle` assertions:

- joiner access is approved;
- mover access is adjusted;
- leaver access is removed promptly;
- access is periodically recertified.

A control result may aggregate assertion results, but unresolved material assertions remain visible.

## Mapping fields

A requirement-to-control mapping must include:

- framework/version;
- source requirement reference;
- SolidSecurity control ID;
- relationship (`supports`, `primary`, `partial`, `contextual`);
- coverage estimate where useful;
- rationale;
- mapping status (`proposed`, `reviewed`, `approved`, `superseded`);
- reviewer/version/date.

## Intellectual-property/copyright rule

Do not copy protected ISO/NEN or third-party framework text into public controls unless redistribution is explicitly permitted. Prefer public legal references, clause/control identifiers, internally authored summaries and internally authored generic control objectives.

## Proof relationship

Control or policy existence alone proves nothing about a customer. For a client, controls/assertions progress through claims, evidence, assessment and review. A generated policy can at most help show `Designed`; it does not establish operational effectiveness.

## Scope rule

Keep the smallest control set that covers distinct operational objectives in the target workflows. Add a control only when a real workflow exposes a materially distinct objective that cannot be cleanly represented by an existing control/assertion.

The Supplier Beta synthetic case justified exactly four additions: secure development, cryptography, logging/monitoring and independent technical testing. No broad framework import follows from that finding.
