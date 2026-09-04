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
- `mission_evidence_class`: one or more canonical Mission classes from `E0_DESIGN`, `E1_SYNTHETIC`, `E2_CONTROLLED_REAL_CLIENT`, `E3_MARKET_COMMERCIAL`, `E4_REPEATED_OPERATIONAL`, but only where the underlying observation actually proves that class.

Required package-level fields:

- `calculation_currency`: one ISO 4217 currency code used for **all** monetary calculations in that package;
- `revenue_mode`: exactly one of `ONE_TIME`, `RECURRING`, or `UPFRONT_PLUS_RECURRING`;
- `upfront_price_hypothesis`: the one-time package price or onboarding/upfront fee, normalized to `calculation_currency`;
- `recurring_price_hypothesis`: the recurring package price for its declared period, normalized to `calculation_currency`;
- `recurring_price_period_months`: the recurring price period in months when recurring revenue exists.

The three revenue modes are mutually exclusive and have fail-closed invariants:

| `revenue_mode` | `upfront_price_hypothesis` | `recurring_price_hypothesis` | `recurring_price_period_months` |
| --- | --- | --- | --- |
| `ONE_TIME` | `> 0` | exactly `0` | `NOT_APPLICABLE` |
| `RECURRING` | exactly `0` | `> 0` | `> 0` |
| `UPFRONT_PLUS_RECURRING` | `> 0` | `> 0` | `> 0` |

A package that does not satisfy the row for its declared mode is invalid rather than reinterpreted. This prevents identical cash streams from being labeled differently and prevents one-time revenue from leaking into recurring economics.

Revenue mode must also match the package's workflow phases:

- `ONE_TIME` requires at least one onboarding/one-time row and **zero recurring rows**;
- `RECURRING` requires at least one recurring row; onboarding rows may exist and are treated as unrecovered onboarding cost because upfront price is zero;
- `UPFRONT_PLUS_RECURRING` requires at least one onboarding/one-time row and at least one recurring row.

A package with a mismatched revenue mode/workflow shape is invalid. Recurring work can therefore never disappear from cost calculations merely because a package was labeled `ONE_TIME`, and a recurring price can never produce a fictitious 100% margin when no recurring work exists.

`evidence_status` and `mission_evidence_class` are independent. A measured pilot workload is not automatically market/commercial evidence, and repeated operational evidence is not automatically market evidence.

### Currency normalization

**Cross-currency arithmetic is prohibited.** Before any cost, contribution, margin or payback formula is evaluated, every monetary input must be expressed in the package's single `calculation_currency`.

This applies to at least:

- loaded operator and professional rates;
- external-specialist costs;
- fixed and variable provider/tooling costs;
- upfront and recurring price hypotheses;
- any other monetary amount entering a derived package result.

When a source value is denominated in another currency, the restricted economics record preserves:

- original amount and ISO 4217 source currency;
- `calculation_currency`;
- conversion rate;
- attributable exchange-rate source;
- `fx_as_of` date/time or applicable conversion period;
- resulting normalized amount used by the calculation.

Only the normalized amount may enter the formulas below. A missing source currency, conversion rate/source/as-of, or normalized package-currency amount makes the affected calculation unresolved rather than permitting raw amounts in different currencies to be added.

### Calculation contract

The calculation method is intentionally conventional and auditable. **Month is the common recurring model period.** Mixed cadences are normalized before they are summed.

`operator_minutes`, `professional_review_minutes`, `customer_minutes`, `external_specialist_cost` and `variable_provider_tooling_cost` are **expected per-occurrence values inclusive of the ordinary rework/exception burden represented by that row**. `rework_or_exception_rate` is retained as a diagnostic/segmentation driver explaining those expected values; it is not multiplied into them a second time. If source measurements exclude rework or exception effort, that effort must first be added as separate work rows or converted into inclusive expected per-occurrence values before package economics are calculated. This keeps exceptions economically visible without double-counting them.

All monetary terms below mean their already-normalized amount in `calculation_currency`.

`operator_cost = operator_minutes / 60 * loaded_operator_rate`

`professional_cost = professional_review_minutes / 60 * loaded_professional_rate`

`unit_step_cost = operator_cost + professional_cost + external_specialist_cost + fixed_provider_tooling_cost_allocation + variable_provider_tooling_cost`

Every cost term in `unit_step_cost` is the amount allocated to **one occurrence** of that row. A periodic fixed provider/tooling cost that is not occurrence-driven is modeled as its own recurring row, preventing it from being multiplied once as a fixed period cost and again by another workflow's cadence.

Onboarding rows are one-time work units; repeated onboarding actions are represented as separate rows rather than hidden in a cadence multiplier:

`onboarding_delivery_cost = sum(onboarding unit_step_cost)`

`upfront_contribution_before_overhead = upfront_price_hypothesis - onboarding_delivery_cost`

`upfront_gross_margin_sensitivity = upfront_contribution_before_overhead / upfront_price_hypothesis` when `upfront_price_hypothesis > 0`; otherwise `NOT_APPLICABLE`.

`unrecovered_onboarding_cost = max(0, onboarding_delivery_cost - upfront_price_hypothesis)`

For each recurring row:

`monthly_frequency = expected_occurrences / cadence_period_months`

`recurring_monthly_step_cost = unit_step_cost * monthly_frequency`

`recurring_monthly_delivery_cost = sum(recurring recurring_monthly_step_cost)`

`recurring_customer_minutes_per_month = sum(customer_minutes * monthly_frequency)`

For `RECURRING` and `UPFRONT_PLUS_RECURRING`, the mode invariants guarantee a positive recurring-price denominator and at least one recurring work row:

`recurring_price_month = recurring_price_hypothesis / recurring_price_period_months`

`monthly_recurring_contribution_before_overhead = recurring_price_month - recurring_monthly_delivery_cost`

`recurring_gross_margin_sensitivity = monthly_recurring_contribution_before_overhead / recurring_price_month`

Onboarding payback is defined without dividing by a nonpositive contribution:

- if `revenue_mode == ONE_TIME`: `onboarding_payback_months = NOT_APPLICABLE`;
- else if `unrecovered_onboarding_cost == 0`: `onboarding_payback_months = 0`;
- else if `monthly_recurring_contribution_before_overhead > 0`: `onboarding_payback_months = unrecovered_onboarding_cost / monthly_recurring_contribution_before_overhead`;
- else: `onboarding_payback_months = NOT_RECOVERABLE`.

A zero or negative recurring contribution is therefore a valid adverse sensitivity result, not a division error and not silently treated as eventual payback.

For a `ONE_TIME` package, recurring rows are prohibited and all recurring revenue, recurring margin and recurring-payback outputs are `NOT_APPLICABLE`; its economics are represented by the upfront contribution/margin against the actual onboarding/one-time delivery cost.

`recurring_professional_minutes_per_client_month = sum(professional_review_minutes * monthly_frequency)`

`professional_client_capacity = available_professional_minutes_per_month / recurring_professional_minutes_per_client_month` when recurring professional minutes are positive; otherwise `NOT_APPLICABLE`.

`expected_occurrences` and `cadence_period_months` must be positive for recurring work rows. The package-level revenue-mode table plus workflow-phase invariants govern price/period positivity, exclusivity and the required presence/absence of recurring work. This prevents zero denominators, one-time/recurring ambiguity, phantom recurring margin and mixed-period summation.

These are calculation definitions, not published commercial values. Classification follows the data owner, not merely the metric name:

- identifiable real-client measurements (including client-linked minutes, workload, review burden, costs or outcomes) are `CLIENT_CONFIDENTIAL` and remain only in the approved client data plane;
- named prospect/proposal/channel observations, internal loaded rates, package-price hypotheses, margins, named provider costs and de-identified/aggregated operating economics are `PROPRIETARY_RESTRICTED` and belong in the private operations/IP location;
- public-safe synthetic/model minute examples may remain public when explicitly labeled `HYPOTHESIS` / `E0_DESIGN` or, for actually timed synthetic runs, `E1_SYNTHETIC`, contain no client/prospect identity and disclose no restricted pricing or margin assumptions.

Derived outputs:

- onboarding/one-time delivery cost;
- upfront contribution and upfront gross-margin sensitivity where an upfront/one-time price exists;
- recurring monthly delivery cost where recurring service exists;
- recurring monthly contribution and gross-margin sensitivity where recurring revenue exists;
- unrecovered onboarding cost and recurring-payback months or `NOT_RECOVERABLE` where applicable;
- professional minutes per client/month;
- customer minutes per onboarding and recurring month;
- client capacity per professional monthly minute envelope where a professional-minute denominator exists;
- margin impact of external review/assurance requirements.

## Evidence rules

### Design assumptions

Untimed design/model assumptions are `HYPOTHESIS` with `mission_evidence_class: E0_DESIGN`.

### Measured synthetic workflow

Actually executed/timed synthetic workflows are represented as `HYPOTHESIS` or another appropriately bounded maturity status with `mission_evidence_class: E1_SYNTHETIC`. E1 may improve the mechanics or workload estimate but cannot substitute for E2 real-client delivery, E3 market/commercial proof or E4 repeated governed operations.

### Market observation

Real market-interaction observations that are not controlled pilot measurements are labeled `OBSERVED_MARKET` with `mission_evidence_class: E3_MARKET_COMMERCIAL`; they do not become pricing facts merely because a prospect stated or accepted a number.

### Controlled real design partner

Actual delivery time, follow-up, evidence availability, review burden and customer effort are captured as `MEASURED_PILOT` with `mission_evidence_class: E2_CONTROLLED_REAL_CLIENT`.

Commercial observations arising during a controlled design partner, such as willingness-to-pay or proposal outcome, are E3 only when separately attributable commercial evidence supports that conclusion. A record may cite both E2 and E3 only when it preserves the distinct underlying observations; E2 workload cannot substitute for E3 market proof.

### Repeated governed operations

Repeated governed delivery cycles may support `mission_evidence_class: E4_REPEATED_OPERATIONAL` for recurring workload, capacity, reliability and margin behavior when the repeated-operation criteria are actually met. E4 strengthens operational confidence; it does not itself prove market demand or willingness-to-pay, which remain E3 claims.

### Validated bounded commercial assumption

A workload, capacity, cost or margin assumption may be labeled `VALIDATED_BOUNDED` only when the supporting Mission evidence class(es), sample and scope are stated and the conclusion does not generalize beyond what the evidence supports.

A **sell-price assumption** (`upfront_price_hypothesis`, `recurring_price_hypothesis`, package price or equivalent) may be labeled `VALIDATED_BOUNDED` only when relevant bounded **E3_MARKET_COMMERCIAL pricing/value evidence** supports that price or price boundary. E1 synthetic cost, E2 delivery workload or E4 repeated operating evidence can support cost, capacity and margin claims but **cannot by themselves validate what the market will pay**. A cost-derived price without relevant E3 evidence remains a hypothesis even when its underlying cost model is well measured.

Conversely, E3 willingness-to-pay evidence does not by itself validate workload, capacity or margin; those retain the evidence classes that actually support them. E1, E2, E3 and E4 are not interchangeable.

## Storage and source-of-truth boundary

This public document is the **calculation and evidence-class contract**, not the confidential value ledger.

The private operations/IP economics ledger may retain only non-client-confidential operating/commercial values. For every retained value it records:

- value and unit;
- source currency and `calculation_currency` for monetary values;
- FX conversion rate/source/as-of and normalized amount when currencies differ;
- workflow/package context;
- normalized model period where applicable;
- revenue mode and whether price is upfront or recurring;
- `evidence_status`;
- `mission_evidence_class`;
- source/date or measurement period;
- sample/boundary;
- last review date;
- supersession history where the assumption changes.

Identifiable client measurements are never copied into that ledger: they remain `CLIENT_CONFIDENTIAL` in the approved client data plane. Only a deliberately de-identified/aggregated derived value may enter the private operations/IP economics ledger when its source boundary and evidence class remain reconstructable without exposing the client record.

Do not store the restricted ledger, detailed internal rates, price hypotheses, margins, identifiable client/prospect measurements or other commercially sensitive operating intelligence in this public repository. Public-safe synthetic E0/E1 examples remain permitted under `PUBLIC_REPO_POLICY.md` and do not become restricted merely because they contain a minute estimate.

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

1. the bottom-up model is populated with identified evidence status and canonical Mission evidence class;
2. professional trust/cost assumptions are explicit;
3. at least one bounded real engagement supplies measured E2 workload evidence;
4. every price treated as `VALIDATED_BOUNDED` has relevant bounded E3 pricing/value/willingness-to-pay evidence; E1/E2/E4 cost/workload evidence alone cannot validate a sell price;
5. ICP/channel conclusions use separate E3 evidence rather than inferred E1/E2/E4 workload;
6. hypothesis, observed-market, measured-pilot, repeated-operational and validated-bounded values remain distinguishable by their retained evidence metadata;
7. the declared revenue mode satisfies its mutually exclusive price invariants **and** its workflow-phase shape;
8. every monetary input is normalized to one declared ISO-4217 `calculation_currency` before cost/contribution/margin/payback arithmetic, with attributable FX provenance where conversion is required;
9. all recurring costs/prices are normalized to the declared monthly model period before recurring margin/payback calculations;
10. upfront contribution, unrecovered onboarding cost, applicable onboarding payback/`NOT_RECOVERABLE` status and recurring capacity are visible;
11. pricing has an identified ICP/scope boundary;
12. identifiable client measurements remain in the approved client data plane while only de-identified/aggregated commercial economics enter the private operations/IP ledger;
13. detailed internal economics are stored in the approved private/restricted location.

A public-safe formula or empty template does not satisfy this gate by itself.
