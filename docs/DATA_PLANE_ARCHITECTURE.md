# Client Data Plane Architecture — Requirements V1

## Scope

Provider-neutral requirements for a minimal first-pilot runtime.

## Logical components

```text
Authenticated ingress
      |
      v
Tenant-aware service/API
  |        |        |
  v        v        v
Metadata  Evidence  Audit/event
store     objects   log
  |        |
  +--- explicit selection ---> AI processing boundary
                      |
                      v
               PROPOSED outputs
                      |
                      v
              professional review
```

## Tenant invariant

Every client-plane object is owned by exactly one `tenant_id`. Cross-tenant object references are invalid unless a separately governed platform-admin operation explicitly supports them without exposing data.

Required controls:

- tenant id derived from authenticated authorization context, not trusted from user-supplied request fields alone;
- database row-level isolation (RLS or equivalent defense-in-depth);
- object storage isolation by tenant namespace plus authorization enforcement;
- background jobs carry explicit tenant context;
- agent tokens are tenant-scoped;
- search/retrieval indexes cannot mix tenant content;
- logs must not contain raw document bodies or sensitive evidence content;
- automated tests attempt cross-tenant reads/writes and must fail.

## Metadata/state store

Must support at minimum:

- tenant/client scope;
- implementation claims;
- evidence metadata and integrity hash;
- assessments;
- findings/actions;
- review queue/reviews/decisions;
- vendors and AI use cases;
- approved customer artifacts/assertions;
- retention/deletion state.

## Evidence object store

Requirements:

- encryption in transit and at rest;
- private-by-default objects; no public object URLs;
- short-lived signed access where needed;
- malware/file-type controls at ingestion;
- size/type allowlist;
- immutable content hash at ingestion;
- version/change provenance rather than silent overwrite;
- tenant-aware lifecycle/delete controls;
- backup/recovery consistent with agreed retention.

## Evidence integrity

On ingestion record at minimum:

`tenant + evidence_id + source + actor + timestamp + hash + size + media_type + classification + coverage + validity/expiry`.

Changes create a new version/reference. They do not rewrite historical review evidence silently.

## AI boundary

AI access is not blanket database access. The orchestration layer passes only the minimum selected text/metadata necessary for the requested task and records which artifacts/model/policy produced the output.

All material AI outputs enter as `PROPOSED` and cannot self-promote to professional verification.

## No embeddings by default

Vectorization/embedding of client evidence is opt-in after provider/data-residency/retention review. The first pilot can use explicit document selection and transient extraction rather than a permanent vector store.

## Deployment separation

At minimum separate development/synthetic and real-pilot environments. Synthetic/test data must never share the production/pilot tenant store merely for convenience.
