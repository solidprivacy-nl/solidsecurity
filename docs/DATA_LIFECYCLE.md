# Client Data Lifecycle, Retention and Offboarding V1

## Principle

No indefinite retention by default. Retention is defined by data category, engagement need, contract and applicable legal/professional requirements, then enforced technically.

## Lifecycle

### 1. Pre-ingestion

- client/tenant contract and DPA active where required;
- data classification guidance supplied;
- evidence request asks for the minimum necessary artifact;
- customer is instructed to redact unrelated patient/client/personnel content where possible.

### 2. Ingestion

- authenticate actor/tenant;
- validate file type/size;
- malware/safety check;
- classify sensitivity;
- generate integrity hash and evidence metadata;
- reject detected secrets/high-risk content where policy requires a safer path.

### 3. Active processing

- access is role/tenant scoped;
- AI processing follows `LLM_DATA_POLICY.md`;
- derivatives retain provenance to source evidence;
- evidence validity/expiry is tracked.

### 4. Archive/engagement closure

Client receives agreed export of approved reports, registers/actions and evidence references/objects as contractually defined. Access narrows after engagement close.

### 5. Deletion

Deletion schedule is contract/configuration driven and covers primary store, object store, search/vector stores if later used, caches and recoverable backups according to documented expiry mechanics.

A deletion event records object/category, tenant, requested/required date, execution date, actor/system and exceptions/legal hold.

## Pilot retention decision

Before first real client, a written retention schedule with actual durations is mandatory. This V1 deliberately does not invent a universal legal duration. The system must support configurable expiry rather than hard-coding indefinite storage.

## Offboarding acceptance

A client can:

- obtain agreed export;
- have user access revoked;
- receive confirmation of deletion lifecycle initiation/completion;
- understand any documented backup/legal-hold delay;
- close the relationship without needing SolidSecurity proprietary internal data to interpret their own approved compliance artifacts.
