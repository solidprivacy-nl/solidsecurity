# Commercial Model R2 — Validation Contract

## Principle

Sell maintained outcomes and credible assurance capability, not AI tokens or bundles of unbounded consultant hours.

Pricing should reflect actual scope, evidence burden, review intensity, cadence and professional cost. Employee count can be a segmentation proxy but is not a sufficient pricing formula.

## Status of historical price ranges

Earlier repository versions contained indicative price ranges. They were explicitly hypotheses, were not based on measured real-client workload and are **not treated as validated R2 pricing**.

R2 deliberately does not publish a new price list before bottom-up economics and real design-partner evidence exist. Future detailed pricing/economics are commercially sensitive operating information and are stored in the private operations/IP location selected by `PUBLIC_REPO_POLICY.md`.

## Offer hypotheses

### Care Baseline

A bounded onboarding/current-state engagement producing scoped applicability, evidence-backed baseline findings and a prioritized improvement plan.

### Care Managed

Recurring managed control/evidence maintenance with targeted follow-up and professional review according to materiality/review class.

### Supplier Assurance

Maintained security/compliance passport and governed reuse of approved evidence-backed assertions for customer questionnaires/tenders. Secondary launch track until market evidence justifies promotion.

### Audit Ready

A bounded readiness engagement preparing management-system/evidence state for an external audit or certification outcome. External certification remains independent.

## Bottom-up economics model

Every commercial package hypothesis must be decomposed into measurable work units.

Required fields per workflow step:

- `workflow_step`;
- `phase`: onboarding or recurring;
- `trigger_or_cadence`;
- `operator_minutes`;
- `professional_review_minutes`;
- `review_class`;
- `loaded_operator_rate`;
- `loaded_professional_rate`;
- `external_specialist_cost` where applicable;
- `customer_minutes`;
- `ai_proposal_count`;
- `ai_accept_modify_reject_rate`;
- `evidence_reuse_ratio`;
- `approved_assertion_reuse_ratio` where applicable;
- `rework_or_exception_rate`;
- `fixed_provider_tooling_cost_allocation`;
- `variable_provider_tooling_cost`;
- for recurring rows, `expected_occurrences` and `cadence_period_months`;
- `evidence_status` (`HYPOTHESIS`, `OBSERVED_MARKET`, `MEASURED_PILOT`, or `VALIDATED_BOUNDED`);
- `mission_evidence_class` (`E0_DESIGN`, `E2_CONTROLLED_REAL_CLIENT`, `E3_MARKET_COMMERCIAL`, or an explicitly justified combination).

`evidence_status` and `mission_evidence_class` are independent. A measured pilot workload is not automatically market/commercial evidence.

### Calculation contract

The calculation method is intentionally conventional and auditable. **Month is the common recurring model period.** Mixed cadences are normalized before they are summed.

`operator_cost = operator_minutes / 60 * loaded_operator_rate`

`professional_cost = professional_review_minutes / 60 * loaded_professional_rate`

`unit_step_cost = operator_cost + professional_cost + external_specialist_cost + fixed_provider_tooling_cost_allocation + variable_provider_tooling_cost`

Onboarding rows are one-time work units; repeated onboarding actions are represented as separate rows rather than hidden in a cadence multiplier:

`onboarding_delivery_cost = sum(onboarding unit_step_cost)`

For each recurring row:

`monthly_frequency = expected_occurrences / cadence_period_months`

`recurring_monthly_step_cost = unit_step_cost * monthly_frequency`

`recurring_monthly_delivery_cost = sum(recurring recurring_monthly_step_cost)`

Every package-price hypothesis must declare its price period in months:

`P_month = package_price_hypothesis / package_price_period_months`

`monthly_contribution_before_overhead = P_month - recurring_monthly_delivery_cost`

`gross_margin_sensitivity = monthly_contribution_before_overhead / P_month`

`onboarding_payback_months = onboarding_delivery_cost / positive monthly_contribution_before_overhead`

`recurring_professional_minutes_per_client_month = sum(professional_review_minutes * monthly_frequency)`

`professional_client_capacity = available_professional_minutes_per_month / recurring_professional_minutes_per_client_month`

`expected_occurrences`, `cadence_period_months` and `package_price_period_months` must be positive. This prevents monthly, quarterly and annual amounts from being added without normalization.

These are calculation definitions, not published commercial values. Real-client/prospect minutes, internal loaded rates, package-price hypotheses, margins, named provider costs and identifiable measured commercial observations are `PROPRIETARY_RESTRICTED`. Public-safe synthetic/model minute examples may remain public when explicitly labeled `HYPOTHESIS` / `E0_DESIGN`, contain no client/prospect identity and do not disclose restricted pricing or margin assumptions.

Derived outputs:

- onboarding delivery cost;
- recurring monthly delivery cost;
- professional minutes per client/month;
- customer minutes per onboarding/recurring cycle;
- gross-margin sensitivity by monthly-normalized package-price hypothesis;
- onboarding payback in months;
- client capacity per professional monthly minute envelope;
- margin impact of external review/assurance requirements.

## Evidence rules

### Before real delivery

Synthetic/model measurements may be used for scenario planning only and must be marked `HYPOTHESIS` with `mission_evidence_class: E0_DESIGN`.

### Market observation

Real market-interaction observations that are not controlled pilot measurements are labeled `OBSERVED_MARKET` with `mission_evidence_class: E3_MARKET_COMMERCIAL`; they do not become pricing facts merely because a prospect stated or accepted a number.

### Controlled real design partner

Actual delivery time, follow-up, evidence availability, review burden and customer effort are captured as `MEASURED_PILOT` with `mission_evidence_class: E2_CONTROLLED_REAL_CLIENT`.

Commercial observations arising during a controlled design partner, such as willingness-to-pay or proposal outcome, are E3 only when separately attributable commercial evidence supports that conclusion. A record may cite both E2 and E3 only when it preserves the distinct underlying observations; E2 workload cannot substitute for E3 market proof.

### Validated bounded commercial assumption

A price, workload or capacity assumption may be labeled `VALIDATED_BOUNDED` only when the supporting Mission evidence class(es), sample and scope are stated and the conclusion does not generalize beyond what the evidence supports.

## Storage and source-of-truth boundary

This public document is the **calculation and evidence-class contract**, not the confidential value ledger.

The restricted economics ledger must retain, for every value:

- value and unit;
- workflow/package context;
- normalized model period where applicable;
- `evidence_status`;
- `mission_evidence_class`;
- source/date or measurement period;
- sample/boundary;
- last review date;
- supersession history where the assumption changes.

Do not store the restricted ledger, detailed internal rates, price hypotheses, margins, identifiable client/prospect measurements or other commercially sensitive operating intelligence in this public repository. Public-safe synthetic E0 examples remain permitted under `PUBLIC_REPO_POLICY.md` and do not become restricted merely because they contain a minute estimate.

## Commercial optimization order

R2 does not claim that price advantage, maximum gross margin and maximum professional review can all be optimized simultaneously.

Priority order during early validation:

1. **credible review quality and authority boundaries**;
2. **commercially sustainable gross margin/capacity**;
3. **customer price/value advantage created by automation and reuse**.

If the service cannot support both credible professional quality and sustainable economics at a given package price, the scope/price/segment must change; review quality may not be silently reduced to preserve the package.

## Complexity drivers

Track at minimum:

- number of legal entities/scopes;
- number and criticality of systems/suppliers;
- actual applicable obligations/frameworks;
- health/personal-data sensitivity;
- evidence volume/quality/freshness;
- review/materiality burden;
- certification/independent-assurance ambitions;
- questionnaire/tender volume;
- AI use cases;
- remediation backlog;
- customer responsiveness and follow-up burden.

## Pricing decision gate

Before any new price list is treated as commercial source of truth:

1. the bottom-up model is populated with identified evidence status and Mission evidence class;
2. professional trust/cost assumptions are explicit;
3. at least one bounded real engagement supplies measured E2 workload evidence;
4. any ICP/channel/willingness-to-pay conclusion uses separate E3 evidence rather than inferred E2 workload;
5. hypothesis, observed-market, measured-pilot and validated-bounded values are separated;
6. all recurring costs and package prices are normalized to the declared monthly model period before margin/payback calculations;
7. onboarding payback and recurring capacity are visible;
8. pricing has an identified ICP/scope boundary;
9. detailed internal economics are stored in the approved private/restricted location.

A public-safe formula or empty template does not satisfy this gate by itself.
