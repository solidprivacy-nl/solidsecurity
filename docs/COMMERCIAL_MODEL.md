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
- `expected_frequency_per_month_or_year`;
- evidence label (`HYPOTHESIS`, `OBSERVED_MARKET`, `MEASURED_PILOT`, or `VALIDATED_BOUNDED`).

### Calculation contract

The calculation method is intentionally conventional and auditable:

`operator_cost = operator_minutes / 60 * loaded_operator_rate`

`professional_cost = professional_review_minutes / 60 * loaded_professional_rate`

`step_delivery_cost = (operator_cost + professional_cost + external_specialist_cost + fixed_provider_tooling_cost_allocation + variable_provider_tooling_cost) * expected_frequency`

`onboarding_delivery_cost = sum(onboarding step_delivery_cost)`

`recurring_period_delivery_cost = sum(recurring step_delivery_cost)`

For a package-price hypothesis `P`:

`contribution_before_overhead = P - recurring_period_delivery_cost`

`gross_margin_sensitivity = contribution_before_overhead / P`

`onboarding_payback_period = onboarding_delivery_cost / positive recurring contribution per equivalent period`

`professional_client_capacity = available professional minutes per period / professional minutes required per client per period`

These are calculation definitions, not published commercial values. Rates, minutes, package-price hypotheses, margins, named provider costs and measured client observations are `PROPRIETARY_RESTRICTED`.

Derived outputs:

- onboarding delivery cost;
- recurring monthly/annual delivery cost;
- professional minutes per client/month;
- customer minutes per onboarding/recurring cycle;
- gross-margin sensitivity by package-price hypothesis;
- onboarding payback period;
- client capacity per professional FTE/minute envelope;
- margin impact of external review/assurance requirements.

## Evidence rules

### Before real delivery

Synthetic/model measurements may be used for scenario planning only and must be marked `HYPOTHESIS`.

### Market observation

Real market-interaction observations that are not controlled pilot measurements are labeled `OBSERVED_MARKET`; they do not become pricing facts merely because a prospect stated or accepted a number.

### Controlled real design partner

Actual time, follow-up, evidence availability, review burden and customer effort are captured as `MEASURED_PILOT` for the bounded engagement.

### Validated bounded commercial assumption

A price, workload or capacity assumption may be labeled `VALIDATED_BOUNDED` only when the evidence class, sample and scope are stated and the conclusion does not generalize beyond what the measured data supports.

## Storage and source-of-truth boundary

This public document is the **calculation and evidence-label contract**, not the confidential value ledger.

The restricted economics ledger must retain, for every value:

- value and unit;
- workflow/package context;
- evidence label;
- source/date or measurement period;
- sample/boundary;
- last review date;
- supersession history where the assumption changes.

Do not store the restricted ledger, detailed rates, prices, margins or identifiable customer/prospect economics in this public repository. Until the approved private operations/IP location exists, those values remain unrecorded here rather than being leaked for convenience.

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

1. the bottom-up model is populated with identified evidence labels;
2. professional trust/cost assumptions are explicit;
3. at least one bounded real engagement supplies measured workload evidence;
4. hypothesis, observed-market, measured-pilot and validated-bounded values are separated;
5. onboarding payback and recurring capacity are visible;
6. pricing has an identified ICP/scope boundary;
7. detailed internal economics are stored in the approved private/restricted location.

A public-safe formula or empty template does not satisfy this gate by itself.
