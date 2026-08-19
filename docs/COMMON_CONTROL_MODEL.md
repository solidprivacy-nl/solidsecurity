# SolidSecurity Common Control Model

## Purpose

Create one reusable set of control objectives that can support multiple laws, standards, customer requirements and assurance contexts.

The Common Control Model (CCM) is the central normalization layer between external requirements and client implementations.

## Why

Separate checklists create duplicate work:

`NEN control -> evidence A`

`ISO control -> evidence A again`

`Cbw requirement -> evidence A again`

SolidSecurity instead models:

`external requirements -> SS control -> one client implementation -> reusable evidence`

## Control domains V1

| Code | Domain | Intent |
|---|---|---|
| GOV | Governance & accountability | ownership, policy, management responsibility |
| RISK | Risk management | identify, assess, treat and review risk |
| ASSET | Assets & information | know systems, information and critical dependencies |
| ACCESS | Identity & access | authenticated, least-privilege and reviewed access |
| OPS | Secure operations | configuration, vulnerability, change and operational hygiene |
| INC | Incident management | detect, respond, report and learn |
| RES | Resilience & continuity | backup, restore, continuity and recovery |
| SUP | Supplier & chain security | identify and manage third-party risk |
| PRIV | Privacy & data governance | lawful/controlled personal-data processing and security |
| AI | AI governance | inventory, classify, govern and oversee AI use |
| PEOPLE | People & awareness | competence, training and responsibilities |
| ASSURE | Assurance & improvement | evidence, review, audit, effectiveness and corrective action |

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
- `implementation_guidance_public`
- `default_evidence_classes`
- `minimum_review_class`
- `lifecycle_state`

Private/controlled fields later may include:

- detailed evidence-sufficiency rubric;
- proprietary test procedure;
- accumulated remediation recipes;
- customer benchmarking;
- commercially sensitive crosswalk weighting.

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

Do not copy protected ISO/NEN or third-party framework text into public controls unless redistribution is explicitly permitted. Prefer:

- public legal requirement references;
- clause/control identifiers;
- internally authored summaries;
- internally authored generic control objectives.

Cost-free access to a standard is not assumed to equal redistribution rights.

## Proof relationship

Control existence alone proves nothing about a customer.

For a client, the control must progress through the Proof Ladder using implementation claims, evidence and review. See `model/proof_ladder.yaml`.

## V1 scope rule

Start with the smallest control set that can support the Care and Supplier service workflows. Do not import every control from every framework. Add a control only when it represents a distinct operational objective that cannot be cleanly covered by an existing control.
