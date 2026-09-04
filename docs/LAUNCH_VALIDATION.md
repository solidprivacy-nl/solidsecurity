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

- `E0_DESIGN` — design assumption;
- `E1_SYNTHETIC` — measured synthetic workflow evidence;
- `E2_CONTROLLED_REAL_CLIENT` — controlled real-client delivery/workflow fact;
- `E3_MARKET_COMMERCIAL` — market, ICP, channel, willingness-to-pay, proposal or commercial-outcome evidence;
- `E4_REPEATED_OPERATIONAL` — repeated governed operating evidence.

Evidence status never substitutes for Mission evidence class. Delivery minutes from a design partner are E2; they do not become E3 merely because they were measured in a pilot. A single record may cite multiple Mission classes only when separately attributable observations genuinely support each class. Never promote a lower evidence class into a higher-class claim.

`HYPOTHESIS` records are normally E0. Measured synthetic workflow evidence is E1. `OBSERVED_MARKET` records are E3. `MEASURED_PILOT` records declare E2 and/or E3 according to the actual observation. Repeated governed delivery evidence may reach E4 without becoming E3 commercial evidence. `VALIDATED_BOUNDED` records must preserve the supporting Mission evidence class(es), sample and scope.

Never promote `HYPOTHESIS` to `VALIDATED_BOUNDED` without the underlying records.

Storage follows the identity/data owner:

- named **non-client prospects**, partner names, proposal terms, detailed loss reasons and internal commercial values are `PROPRIETARY_RESTRICTED` and belong in the private operations/IP location selected by `PUBLIC_REPO_POLICY.md`;
- a controlled design partner or existing client identity and any interaction/outcome/willingness-to-pay record still linked to that client are `CLIENT_CONFIDENTIAL` and remain only in the approved client data plane;
- only deliberately de-identified/aggregated E3 learnings may be copied from client-linked observations into the private commercial/operations ledger, with their source boundary and evidence class still reconstructable without exposing the client record.

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
- treatment hypothesis and comparator;
- treatment-arm metric definition, including exact numerator/denominator or duration definition;
- comparator-arm metric definition using the same outcome semantics;
- arm allocation rule and minimum denominator/sample **per arm**;
- `comparison_metric`: the exact treatment-vs-comparator contrast used for the decision, normally `treatment_rate - comparator_rate` or an explicitly defined ratio/duration difference;
- observation window and one `decision_at` / registered stopping point;
- `decision_direction`: exactly `HIGHER_IS_BETTER` or `LOWER_IS_BETTER` for the declared comparison metric;
- numeric `support_threshold`;
- numeric `reject_threshold`;
- confounders/exclusions known at start;
- `registered_at` timestamp.

The decision metric must be a **contrast between treatment and comparator**, not a treatment-arm rate interpreted in isolation. A comparative hypothesis can never be marked `SUPPORTED` merely because the treatment arm clears an absolute threshold while the comparator performs better.

Thresholds must be mutually exclusive by construction:

- for `HIGHER_IS_BETTER`, `support_threshold > reject_threshold`;
- for `LOWER_IS_BETTER`, `support_threshold < reject_threshold`.

A registration with equal or overlapping/contradictory outcome predicates is invalid and cannot yield a directional result. After the first observation, changing comparator, arm metric, allocation, comparison metric, window, stopping point, direction or thresholds requires a new `experiment_id`; the old experiment remains intact.

Outcome is mechanical **only at the pre-registered `decision_at` / end of the observation window**:

- both arms must satisfy their pre-registered minimum denominator/sample; otherwise outcome is `INCONCLUSIVE`;
- `HIGHER_IS_BETTER`: `SUPPORTED` when the comparison metric `>= support_threshold`; `NOT_SUPPORTED` when it `<= reject_threshold`; otherwise `INCONCLUSIVE`;
- `LOWER_IS_BETTER`: `SUPPORTED` when the comparison metric `<= support_threshold`; `NOT_SUPPORTED` when it `>= reject_threshold`; otherwise `INCONCLUSIVE`;
- an incomplete/invalid pre-registration is `INCONCLUSIVE`.

Intermediate results before `decision_at` are provisional diagnostics only and **cannot** authorize track promotion, strategy adoption or experiment termination. If genuine early stopping is required, its complete statistical/decision rule and admissible stopping boundaries must be pre-registered before the first observation; otherwise early stopping is prohibited.

Because the threshold ordering and stopping point are part of registration validity, one completed experiment can never satisfy both `SUPPORTED` and `NOT_SUPPORTED`, and an early transient result cannot become a promotion decision.

An `INCONCLUSIVE` result may guide another experiment but cannot be used as evidence that a channel or segment won.

Any **additional commercial-value condition used for a track-promotion decision** is governed by the same rule. It must be a separately identifiable pre-registered E3 experiment (or explicitly pre-registered second contrast metric) with its own comparator arms, commercial comparison metric, allocation, observation window/stopping point, per-arm minimum sample, direction and mutually exclusive support/reject thresholds. An anecdotal willingness-to-pay statement, one proposal outcome or an unregistered qualitative judgment cannot satisfy that promotion gate.

For **Supplier track promotion specifically**, that E3 commercial-value gate is not an arbitrary Supplier-versus-no-offer comparison: its treatment arm is Supplier and its comparator arm is the primary **Care** track, using the **same pre-registered commercial-value outcome semantics** for both arms. The promotion conclusion must therefore show Supplier outperforming Care on the declared bounded commercial-value contrast; a Supplier-only absolute threshold cannot promote the secondary track while Care has stronger value evidence.

## First-10 acquisition hypotheses

The “first 10” is a learning target, not a forecast or commitment. The initial comparisons are:

| Hypothesis | Comparator | Pre-registered comparison metric |
| --- | --- | --- |
| Warm domain introductions produce more qualified substantive conversations | Problem-triggered direct outreach | treatment qualified-conversation rate minus comparator qualified-conversation rate |
| Applicability-grounded, problem-triggered outreach produces more qualified substantive conversations | Generic outcome-led outreach that makes no unsupported regulatory claim | treatment qualified-conversation rate minus comparator qualified-conversation rate |
| Trusted advisor/referral outreach produces more qualified next steps | Direct outreach | treatment qualified-next-step rate minus comparator qualified-next-step rate |
| Supplier/questionnaire-trigger outreach may be a stronger acquisition wedge than the Care primary track | Care primary-track outreach | treatment qualified-next-step rate minus comparator qualified-next-step rate, plus a separate pre-registered Supplier-versus-Care E3 commercial-value contrast on the same outcome semantics required for any track-promotion decision |

These comparisons do not have universal hard-coded thresholds because direction, thresholds, arm allocation, minimum samples and stopping point are part of each pre-registered experiment and must be frozen before observations. A missing/invalid rule makes the result `INCONCLUSIVE`; it does not permit narrative interpretation after the fact.

Supplier remains secondary while tested. It is promoted only when the completed pre-registered Supplier-versus-Care acquisition experiment is `SUPPORTED` **and** the separately completed pre-registered Supplier-versus-Care E3 commercial-value gate is also `SUPPORTED`; delivery-effort E2 evidence, interim metrics, Supplier-only absolute value evidence or anecdotal commercial observations can never promote the track.

Do not scale a channel because it produces conversations; compare the pre-registered treatment-vs-comparator metric, ICP fit, burden, commercial evidence and learning quality.

## Channel hypothesis scorecard

For each channel/experiment, capture at minimum:

- `experiment_id` and treatment/comparator category;
- `evidence_status`;
- `mission_evidence_class`;
- arm allocation and per-arm approached organizations;
- per-arm substantive conversations;
- per-arm number meeting primary ICP;
- per-arm number explicitly disqualified and reason category;
- per-arm next-step/proposal and outcome counts;
- treatment-arm metric, comparator-arm metric and resulting pre-registered comparison metric;
- pre-registered direction/threshold/window/`decision_at` reference;
- whether the decision point has been reached;
- mechanical experiment outcome (`SUPPORTED`, `NOT_SUPPORTED`, `INCONCLUSIVE`) only when eligible for final evaluation;
- dominant objection categories;
- median/typical sales-cycle observations when enough data exists;
- customer-acquisition effort/cost only in the appropriately restricted record;
- date range and sample limitations.

No rate is called validated when either arm's denominator/sample is too small to support the pre-registered decision rule.

## Interview / proposal / loss-reason capture

Each substantive market interaction produces an attributable restricted record, but its storage plane depends on the organization relationship:

- for a non-client prospect, the record may live in the private operations/IP commercial store as `PROPRIETARY_RESTRICTED`;
- for an existing client or controlled design partner, the attributable record is `CLIENT_CONFIDENTIAL` and remains in the approved client data plane; it is **not copied** into the operations/IP commercial store;
- only a deliberately de-identified/aggregated E3 derivative may enter the commercial store from a client-linked interaction.

The attributable source record captures as applicable:

- interaction date and channel;
- organization identity in its permitted storage plane;
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

- Care remains the primary launch track until a **completed** pre-registered E3 comparison supports a change.
- Supplier remains secondary until both the completed pre-registered Supplier-versus-Care acquisition experiment and the separately completed pre-registered Supplier-versus-Care E3 commercial-value gate on the same outcome semantics are `SUPPORTED`.
- Interim/provisional observations never authorize promotion.
- Direct Cyberbeveiligingswet/NIS2 positioning requires explicit applicability basis; generic market urgency is insufficient.
- A channel, ICP rule, objection response or offer becomes current strategy only after evidence is summarized and the bounded conclusion is intentionally adopted into `STRATEGY.md` / `POSITIONING.md`.
- Detailed market records stay in their permitted private/client storage plane; only deliberately public-safe aggregate learnings may flow back into this repository.

## WP02 public-safe exit contribution

This contract proves the launch hypotheses are falsifiable, comparative, pre-registered and protected against post-hoc/early-stopping promotion; Mission evidence classes cannot be silently substituted. It does **not** prove market demand, channel performance, willingness-to-pay or validated economics. Those require the correct E3/E2/E4 evidence in the approved restricted/client locations.
