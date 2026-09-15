# SolidSecurity Engagement Boundary V1

Status: `INTERNAL SERVICE DESIGN / NOT CUSTOMER TERMS`

## Purpose

Define who is responsible for facts, implementation, professional judgment and external assurance in the managed-service model.

This document is a public-safe service-design boundary. It is **not** legal advice, an approved customer contract, an insurance confirmation or authority to issue customer-facing `VERIFIED` claims.

## SolidSecurity provides

Subject to the contracted package and professional scope:

- structured intake and scope preparation;
- control/evidence organization;
- evidence requests and provenance;
- AI-assisted drafting, comparison and first-pass analysis;
- proposed and professionally reviewed assessments where included;
- findings/remediation planning;
- recurring evidence/control review workflow;
- supplier/AI/privacy/security governance support;
- customer reports/passports with explicit assurance labels;
- audit/certification readiness support where contracted.

## The customer remains responsible for

- truthfulness/completeness of supplied facts and evidence;
- actual operation of its organization, systems and people;
- implementing or commissioning agreed remediation;
- approving and adopting policies/procedures;
- maintaining licenses/contracts/system configurations outside SolidSecurity control;
- management risk acceptance and business decisions;
- notifying SolidSecurity of material changes that invalidate prior evidence/statements;
- statutory/regulatory responsibilities that cannot be delegated away merely by using a service provider.

## SolidSecurity does not automatically become

- the customer's certification body;
- a regulator;
- the customer's statutory independent auditor;
- legal counsel merely by providing a compliance workflow;
- the customer's FG/DPO where independence/statutory-role requirements have not been separately contracted and satisfied;
- the operator of the customer's ICT/security controls unless separately agreed;
- an insurer or guarantor of security/compliance outcomes.

## Professional review boundary

AI and operations may prepare facts, mappings, draft assessments and proposed conclusions. Material final professional statements require a reviewer with the appropriate authority/competence.

The reviewer must see unresolved uncertainty, conflicting evidence and limitations rather than a polished AI conclusion that hides them.

Customer professional review follows the R0–R4 contract in `model/ai_authority.yaml`. Product/change B1 assurance is separate and does not grant customer-professional credentials or authority.

## Customer `VERIFIED` readiness boundary

Before customer-facing `VERIFIED` could ever be enabled, the complete fail-closed gate in `model/ai_authority.yaml` must be satisfied. At minimum that includes the applicable review class, reviewer identity/competence/credential and independence requirements, reviewer capacity and loaded-cost assumption, escalation path, liability/insurance posture, contractual/report-language readiness, post-verification incident posture, DPA/subprocessor readiness and retention/deletion readiness.

Missing or unresolved prerequisites mean `NEEDS_REVIEW`, not `VERIFIED`.

WP03 only makes those requirements explicit and ready for the appropriate professional/legal/insurance review. It does not itself approve them. Customer-facing `VERIFIED` remains disabled in the machine-readable authority model.

## Professional/business liability and insurance posture

Before any real engagement may use customer-facing `VERIFIED` language, the engagement must have documented and appropriately reviewed:

- which professional/business liability exposures arise from the offered scope;
- required insurance types/limits and material exclusions relevant to that scope;
- whether actual coverage is in force for the activity and territory at issue;
- responsibilities that remain with customer management or external professionals;
- escalation where the requested service exceeds insured/contracted professional scope.

Do not state or imply that insurance is adequate merely because this design requirement exists. Actual policy wording, limits, exclusions and broker/legal advice are restricted engagement evidence and require qualified external review.

## Contractual scope and liability-limit readiness

Before customer-facing `VERIFIED` is permitted for a real engagement, contract/DPA materials must define at least:

- exact service and assurance scope;
- exclusions and dependencies on customer-supplied facts/evidence;
- customer responsibilities and change-notification duty;
- limitation-of-liability/indemnity provisions appropriate to the agreed risk allocation;
- third-party/external-authority responsibilities;
- treatment of reliance by third parties where relevant;
- applicable termination, retention, export and deletion obligations.

This repository defines the required topics, not their final legal wording or commercial limits.

## Verified report-language boundary

A customer report may use `VERIFIED` only as the scoped Proof Ladder/decision state authorized by the applicable professional gate. Approved report language must always preserve:

- assessed entity/scope and period/as-of date;
- evidence/review basis and material limitations;
- unresolved exclusions or assumptions;
- distinction between internal professional verification and external independent assurance/certification;
- no guarantee of future compliance, absence of incidents or successful certification.

Forbidden shortcuts include “100% compliant”, “guaranteed secure”, “certified” without the actual certification authority, or language implying that internal review is independent external assurance.

## Risk acceptance

SolidSecurity may identify options and consequences. Material risk acceptance remains an explicitly authorized human/client-management decision and must record rationale, owner, expiry/review and compensating controls where relevant.

## Incident boundary

SolidSecurity may support incident triage, timeline reconstruction, evidence organization and notification preparation.

The final decision that a specific real incident must be notified to a regulator, affected persons, CSIRT or contractual counterparty is reserved for an authorized qualified human under the applicable engagement and legal context.

No AI workflow may make/send such a material notification autonomously.

### Incident/breach after prior verification

A later incident does not retroactively prove that a correctly scoped earlier `VERIFIED` decision was fraudulent, nor may the earlier decision be presented as a guarantee that incidents could not occur.

A material incident or newly discovered contrary fact must instead trigger a governed response:

1. preserve the prior evidence/review/decision record;
2. record the new incident/fact with provenance;
3. identify which earlier scope, assumptions, evidence or controls may be affected;
4. reopen/downgrade affected current assurance where its support is no longer sufficient;
5. route incident/legal notification decisions to the authorized qualified human/external authority;
6. communicate corrected scope/status to the customer where required by contract/professional duty.

No marketing or liability response may silently delete the prior record or keep an unsupported green state.

## Certification/readiness boundary

SolidSecurity may prepare an organization for an independent audit/certification process and organize the evidence trail. The independent auditor/certification body remains responsible for its own findings and formal certification decision.

External audit findings supersede marketing/readiness expectations and enter the remediation workflow as authoritative engagement evidence within their scope.

## DPO/FG boundary

Privacy/security managed services and a statutory DPO/FG role are distinct. If SolidSecurity later offers a DPO/FG service, conflicts of interest and required independence must be assessed separately; the same person/role should not independently assure controls they materially designed/operated where that would compromise required independence.

## Data-protection readiness dependency

Customer `VERIFIED` and real-client admission do not bypass the existing data-governance gates. `model/pilot_gate.yaml` and `docs/DATA_LIFECYCLE.md` remain the sources for contract/DPA, subprocessor review, retention, export and deletion readiness. WP03 consumes those gates; it does not duplicate or weaken them.

## Facts versus advice versus decision

Every material workflow item should be classifiable as:

1. `FACT` — supplied/observed evidence with provenance;
2. `PROPOSED_ANALYSIS` — AI/operations interpretation;
3. `PROFESSIONAL_OPINION` — authorized professional review within scope;
4. `CLIENT_DECISION` — management acceptance/approval/action;
5. `INDEPENDENT_ASSURANCE` — independent external/segregated assurance result;
6. `CERTIFICATION_DECISION` — authorized certification body decision.

The system must not silently promote one category into another.

## Change-of-fact rule

A material client change (system, supplier, AI use, incident, merger, major process change, regulatory scope change) can invalidate previous assertions. The managed service therefore needs explicit client-change notification plus scheduled review; “continuous” never means magical knowledge of changes the service cannot observe.
