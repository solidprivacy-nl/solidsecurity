# R2 Launch Validation Contract

## Purpose

Turn the Care launch thesis into falsifiable E3 market/commercial learning without publishing named pipeline intelligence or pretending hypotheses are validated facts.

`STRATEGY.md` remains the strategic source of truth. `POSITIONING.md` owns public-safe ICP/positioning. `COMMERCIAL_MODEL.md` owns economics semantics. This document owns only the **launch experiments and evidence-capture contract**.

## Evidence status and Mission class

Every record keeps two independent dimensions:

1. `evidence_status` — how mature the recorded claim is;
2. `mission_evidence_class` — what kind of Mission evidence the underlying observation actually proves.

Allowed `evidence_status` values are:

- `HYPOTHESIS` — design assumption, not market proof;
- `OBSERVED_MARKET` — real market observation with source/date/context;
- `MEASURED_PILOT` — measurement from an authorized bounded design partner;
- `VALIDATED_BOUNDED` — conclusion supported by stated evidence/sample and bounded to that scope.

Allowed Mission evidence classes used here are:

- `E0_DESIGN` — design/synthetic assumption;
- `E2_CONTROLLED_REAL_CLIENT` — controlled real-client delivery/workflow fact;
- `E3_MARKET_COMMERCIAL` — market, ICP, channel, willingness-to-pay, proposal or commercial-outcome evidence.

Evidence status never substitutes for Mission evidence class. Delivery minutes from a design partner are E2; they do not become E3 merely because they were measured in a pilot. A single record may cite both E2 and E3 only when separately attributable observations in that record genuinely support both classes. Never promote a lower evidence class into a higher-class claim.

`HYPOTHESIS` records are E0. `OBSERVED_MARKET` records are E3. `MEASURED_PILOT` records declare E2 and/or E3 according to the actual observation. `VALIDATED_BOUNDED` records must preserve the supporting Mission evidence class(es), sample and scope.

Never promote `HYPOTHESIS` to `VALIDATED_BOUNDED` without the underlying records.

Named prospects, partner names, proposal terms, detailed loss reasons and internal commercial values are `PROPRIETARY_RESTRICTED` and belong in the private operations/IP location selected by `PUBLIC_REPO_POLICY.md`.

## Alternative landscape — launch hypotheses

The relevant alternatives to test are categories, not presumed inferior competitors:

| Alternative | Why customer may prefer it | SolidSecurity hypothesis to test | Disconfirming evidence |
| --- | --- | --- | --- |
| Incumbent MSP / IT provider | Existing trust, technical access, bundled services | Governance/evidence/professional-review lifecycle is incomplete or fragmented | Incumbent already provides the full managed lifecycle credibly at acceptable burden/cost |
| Specialist security/compliance consultant | Expertise and personal accountability | One-off/manual delivery creates recurring maintenance cost and weak reuse | Consultant already provides repeatable managed evidence maintenance with strong reuse/economics |
| GRC SaaS / self-service platform | Structured tooling and broad feature set | Target ICP lacks capacity/desire to operate another tool | Customer has internal staff and explicitly prefers self-service ownership |
| Internal spreadsheets/shared drives | Low cash cost and familiar process | Hidden staff effort, freshness and traceability burden justify managed service | Existing process remains current, auditable and low-burden without external help |
| Auditor/certification-readiness provider | Strong assurance/audit knowledge | Customer also needs continuous pre-audit maintenance outside audit cycle | Provider already supplies the recurring managed capability without independence conflict |
| Do nothing / defer | No immediate spend or change burden | Recurring evidence/customer/regulatory pressure creates a timing trigger | No material pain, urgency, budget or consequence emerges |

The purpose is to learn where SolidSecurity is genuinely better fit, not to prove every alternative wrong.

## Pre-registered acquisition decision rule

Comparative acquisition hypotheses are not judged retrospectively from whatever numbers happen to appear. Before the first observation for an experiment, the restricted experiment record must freeze:

- `experiment_id`;
- hypothesis and comparator;
- primary metric and exact numerator/denominator or duration definition;
- observation window;
- minimum denominator/sample required for a decision;
- `support_threshold`;
- `reject_threshold`;
- confounders/exclusions known at start;
- `registered_at` timestamp.

After the first observation, changing comparator, metric, window or thresholds requires a new `experiment_id`; the old experiment remains intact.

Outcome is mechanical:

- `SUPPORTED` — minimum sample reached and the pre-registered support threshold is met;
- `NOT_SUPPORTED` — minimum sample reached and the pre-registered reject threshold is met;
- `INCONCLUSIVE` — neither condition is met, the window ends below minimum sample, or the decision rule was not pre-registered.

An `INCONCLUSIVE` result may guide another experiment but cannot be used as evidence that a channel or segment won.

## First-10 acquisition hypotheses

The “first 10” is a learning target, not a forecast or commitment. The initial comparisons are:

| Hypothesis | Comparator | Primary metric |
| --- | --- | --- |
| Warm domain introductions produce more qualified substantive conversations | Problem-triggered direct outreach | qualified substantive conversations / approached organizations |
| Applicability-grounded, problem-triggered outreach produces more qualified substantive conversations | Generic outcome-led outreach that makes no unsupported regulatory claim | qualified substantive conversations / approached organizations |
| Trusted advisor/referral outreach produces more qualified next steps | Direct outreach | qualified next steps / substantive conversations |
| Supplier/questionnaire-trigger outreach may be a stronger acquisition wedge than the Care primary track | Care primary-track outreach | qualified next steps / substantive conversations, with separate E3 commercial evidence required for any track-promotion decision |

These comparisons do not have universal hard-coded thresholds because the threshold is part of each pre-registered experiment and must be frozen before observations. A missing threshold makes the result `INCONCLUSIVE`; it does not permit narrative interpretation after the fact.

Supplier remains secondary while tested. It is promoted only when a pre-registered supplier-versus-Care experiment is `SUPPORTED` **and** separately attributable E3 evidence supports the commercial-value conclusion; delivery-effort E2 evidence alone can never promote the track.

Do not scale a channel because it produces conversations; compare the pre-registered metric, ICP fit, burden, commercial evidence and learning quality.

## Channel hypothesis scorecard

For each channel/experiment, capture at minimum:

- `experiment_id` and channel/category;
- `evidence_status`;
- `mission_evidence_class`;
- number of approached organizations;
- number of substantive conversations;
- number meeting primary ICP;
- number explicitly disqualified and reason category;
- next-step/proposal count;
- outcome count;
- primary-metric numerator, denominator and resulting value;
- pre-registered threshold/window reference;
- mechanical experiment outcome (`SUPPORTED`, `NOT_SUPPORTED`, `INCONCLUSIVE`);
- dominant objection categories;
- median/typical sales-cycle observations when enough data exists;
- customer-acquisition effort/cost only in the restricted commercial record;
- date range and sample limitations.

No rate is called validated when the denominator/sample is too small to support the pre-registered decision rule.

## Interview / proposal / loss-reason capture

Each substantive market interaction should produce a restricted record with:

- interaction date and channel;
- organization/prospect identity (restricted);
- role(s) interviewed;
- ICP-fit signals and disqualifiers;
- actual current alternative (MSP, consultant, SaaS, internal, none, other);
- recurring evidence/compliance tasks that create burden;
- concrete trigger/urgency and whether it is legally/applicability grounded;
- current owner of security/compliance work;
- customer minutes/effort they report where obtainable;
- incumbent MSP objection and response;
- perceived value of managed versus self-service approach;
- willingness-to-pay evidence **without treating an offered price as validated pricing**;
- proposal/next step/outcome;
- loss/no-decision reason category;
- free-text evidence/quote stored only where permitted;
- `evidence_status`, `mission_evidence_class`, confidence and sample limitation.

## Loss/no-decision taxonomy

Use a small stable taxonomy before adding categories:

- `NO_MATERIAL_PAIN`
- `NO_BUDGET`
- `NO_URGENCY`
- `INCUMBENT_SUFFICIENT`
- `SELF_SERVICE_PREFERRED`
- `SCOPE_TOO_COMPLEX`
- `TRUST_OR_CREDENTIAL_GAP`
- `PRICE_VALUE_MISMATCH`
- `TIMING`
- `OTHER_EVIDENCED`

Do not create a new category for every anecdote; use notes for nuance and change taxonomy only when repeated evidence warrants it.

## Promotion rules

- Care remains the primary launch track until a pre-registered E3 comparison supports a change.
- Supplier remains secondary until the supplier-versus-Care experiment is `SUPPORTED` and the required separate E3 commercial evidence exists.
- Direct Cyberbeveiligingswet/NIS2 positioning requires explicit applicability basis; generic market urgency is insufficient.
- A channel, ICP rule, objection response or offer becomes current strategy only after evidence is summarized and the bounded conclusion is intentionally adopted into `STRATEGY.md` / `POSITIONING.md`.
- Detailed market records stay private; only deliberately public-safe aggregate learnings may flow back into this repository.

## WP02 public-safe exit contribution

This contract proves the launch hypotheses are falsifiable, the pre-registration/decision rule is defined and Mission evidence classes cannot be silently substituted. It does **not** prove market demand, channel performance, willingness-to-pay or validated economics. Those require the correct E3/E2 evidence in the approved restricted locations.
