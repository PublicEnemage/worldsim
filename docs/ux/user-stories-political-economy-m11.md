# User Stories — M11 Political Economy Module

> **Owned by:** Business Product Owner Agent (R), UX Designer Agent (C)
> **Authored:** 2026-06-04 — Issue #681
> **Status:** All stories final. Implementation already delivered (G16a/G16b, PRs #703/#705).
> These stories are retrospective specification — QA test stubs should be written against
> all Given/When/Then criteria immediately. Frontend Architect consults these stories when
> surfacing political economy outputs in Zone 1 and Zone 2.
>
> **Consumers:**
> - **QA Lead** — writes acceptance test stubs from Given/When/Then criteria.
>   All G16 implementation exists; stubs validate the engine outputs conform to spec.
> - **Frontend Architect** — implements political economy instrument surface against these
>   stories. Surfacing decisions (Zone 1 vs Zone 2) are specified per story.
> - **Data Architect** — validates schema contracts against these stories before any
>   migration touching `PoliticalContext`, `InputSource.CONDITIONALITY`, or
>   `elite_capture_coefficient`.
>
> **Source documents read:**
> `docs/ux/personas.md`, `docs/ux/north-star.md`, `docs/ux/information-hierarchy.md`,
> `docs/ux/zone-coupling-atom-schema.md`, `app/simulation/modules/political_economy/module.py`,
> `app/simulation/orchestration/inputs.py`, `app/schemas.py`,
> `app/simulation/web_scenario_runner.py`
>
> **Implementation references:**
> PR #703 (G16a — input layer: `InputSource.CONDITIONALITY`, `implementation_capacity`,
> `CompoundStateCondition`), PR #705 (G16b — `PoliticalEconomyModule`, `conditionality_decomposer`,
> `PoliticalContext` schema)
>
> **Agents consulted:** PO Agent (authored), Development Economist (human cost ledger placement)

---

## How to Read These Stories

Each story uses the project standard format:

**As** [named persona] in [mode / entry state],
**I need** [specific observable capability],
**so that** [goal — traced to the north-star cognitive task for the active mode].

Acceptance criteria use Given/When/Then format. Each criterion is independently testable
without requiring interpretation of the story context. Test method noted per criterion:

- `[pytest]` — backend / engine unit or integration test
- `[Playwright]` — automated E2E assertion (when frontend surface exists)
- `[Manual]` — human verification gate (no automated test currently feasible)

All stories are M11 required (retrospective). None are deferred.

---

## Story Groups

| Group | Capability | Stories |
|---|---|---|
| 1 | Political feasibility — scenario input configuration | US-PE-001, US-PE-002 |
| 2 | Implementation capacity — ControlInput scaling | US-PE-003, US-PE-004 |
| 3 | Social legitimacy — state variable surfacing | US-PE-005, US-PE-006 |
| 4 | Social response events — legitimacy threshold crossings | US-PE-007, US-PE-008 |
| 5 | Conditionality — structured scenario inputs | US-PE-009, US-PE-010 |
| 6 | Conditionality decomposition — per-term cost attribution | US-PE-011, US-PE-012 |
| 7 | Programme abandonment probability | US-PE-013, US-PE-014 |
| 8 | Compound StateCondition — QA contract | US-PE-015 |
| 9 | Elite capture coefficient — configuration and surfacing | US-PE-016, US-PE-017 |
| 10 | Distributional divergence — Zone placement | US-PE-018 |
| 11 | Argentina backtesting — political economy validation | US-PE-019, US-PE-020 |

---

## Group 1 — Political Feasibility: Scenario Input Configuration

### US-PE-001 — Configure initial political environment via PoliticalContext

**As** Eleni Papadimitriou in Mode 2 scenario authoring,
**I need** to supply an initial `legitimacy_index` (0.0–1.0) as part of the scenario
configuration alongside GDP and unemployment seeds,
**so that** the simulation reflects the political conditions under which the programme
was implemented — enabling the engine to differentiate a high-approval government from
a fragile coalition executing the same austerity measures.

**Acceptance criteria:**

- Given a `POST /scenarios` request with `configuration.political_context.legitimacy_index=0.70`,
  when the scenario is created, then `GET /scenarios/{id}` returns the stored configuration
  with `political_context.legitimacy_index="0.70"` as a string-serialized Decimal. `[pytest]`

- Given a scenario configuration with no `political_context` field, when the scenario runs,
  then engine behaviour is identical to pre-M11 runs — no legitimacy seeding, no feasibility
  scaling, no political economy events. `[pytest]`

- Given a `political_context` with `legitimacy_index=0.70` and
  `government_approval_rating=0.39`, when the scenario runs, then only `legitimacy_index`
  is used by `PoliticalEconomyModule` — the other fields are stored but not yet consumed
  by any engine computation. `[pytest]`

- Given a `political_context` with `legitimacy_index` outside [0.0, 1.0], when the API
  receives the request, then it returns HTTP 422 (Pydantic validation error). `[pytest]`

---

### US-PE-002 — Opt into political economy resolution via modules_config

**As** Eleni Papadimitriou in Mode 2 scenario authoring,
**I need** to opt the political economy resolution in and out via `modules_config`
without re-specifying the scenario,
**so that** I can compare a baseline run (no political constraints) with a politically
constrained run using the same scenario configuration — isolating the political economy
effect on the trajectory.

**Acceptance criteria:**

- Given `modules_config.political_economy.enabled=true` and a `political_context`
  with `legitimacy_index=0.70`, when the scenario runs, then `PoliticalEconomyModule`
  fires and `programme_survival_probability` events appear in step outputs. `[pytest]`

- Given `modules_config.political_economy.enabled=false` (or field absent), when the
  scenario runs, then no `legitimacy_change`, `programme_survival_update`, or
  `elite_capture_divergence` events appear in any step output. `[pytest]`

- Given two identical scenario configurations differing only in
  `modules_config.political_economy.enabled`, when both run to completion, then
  the trajectory difference between them is attributable solely to the political
  economy module's legitimacy dynamics and implementation capacity scaling. `[pytest]`

---

## Group 2 — Implementation Capacity: ControlInput Scaling

### US-PE-003 — Political feasibility scales fiscal policy transmission

**As** Eleni Papadimitriou in Mode 2 watching a fiscal consolidation step,
**I need** the simulation to transmit less of the intended fiscal adjustment when
government legitimacy is low,
**so that** I can see that the same nominal austerity package produces different
real outcomes depending on the political environment it is implemented in — the
Greece 2010 lesson made structurally visible.

**Acceptance criteria:**

- Given `political_context.legitimacy_index=0.70`, when the runner computes
  `_political_feasibility_modifier`, then the returned modifier is `0.85`
  (formula: 0.5 + 0.5 × 0.70). `[pytest]`

- Given `political_context.legitimacy_index=0.40`, when the runner computes
  `_political_feasibility_modifier`, then the returned modifier is `0.70`. `[pytest]`

- Given `political_context.legitimacy_index=0.00`, when the runner computes
  `_political_feasibility_modifier`, then the returned modifier is `0.50` (floor —
  reflecting that even a zero-legitimacy government executes some measures under
  creditor pressure). `[pytest]`

- Given `political_context` is absent, when the runner computes
  `_political_feasibility_modifier`, then the returned modifier is `1.0` — no
  change to ControlInput magnitudes. `[pytest]`

---

### US-PE-004 — implementation_capacity field on ControlInput

**As** a QA Lead writing test stubs for conditionality scenarios,
**I need** `ControlInput.implementation_capacity` to scale event magnitudes from
`get_events()` by the specified factor,
**so that** conditionality modelling can represent partial implementation —
a spending cut mandated at 5% GDP but executed at 60% capacity produces a
3% GDP effective shock, not 5%.

**Acceptance criteria:**

- Given a `FiscalPolicyInput` with `spending_delta=-0.05` and
  `implementation_capacity=0.60`, when `get_events()` is called, then
  the returned event's `affected_attributes` magnitude is `-0.030` (Decimal). `[pytest]`

- Given `implementation_capacity=1.0` (default), when `get_events()` is called,
  then event magnitudes are identical to `to_events()` — no scaling. `[pytest]`

- Given `implementation_capacity=0.0`, when `get_events()` is called, then all
  event `affected_attributes` magnitudes are `0.0` — the policy has no
  transmitted effect. `[pytest]`

- Given a `ControlInput` instantiated without specifying `implementation_capacity`,
  then the default value is `Decimal("1.0")`. `[pytest]`

---

## Group 3 — Social Legitimacy: State Variable Surfacing

### US-PE-005 — legitimacy_index seeded from PoliticalContext at step 0

**As** Eleni Papadimitriou reviewing the initial scenario state before step 1,
**I need** the `legitimacy_index` from `PoliticalContext` to be readable as a
country entity attribute at step 0,
**so that** the initial political environment is visible in the simulation state
before any policy events have fired — enabling me to confirm the scenario was
configured correctly.

**Acceptance criteria:**

- Given `political_context.legitimacy_index=0.70` and `modules_config.political_economy.enabled=true`,
  when the runner applies `_apply_political_context` to the initial state, then
  the country entity has `legitimacy_index` attribute set to `Decimal("0.70")`. `[pytest]`

- Given `legitimacy_index` already set in `initial_attributes` (explicit override),
  when `_apply_political_context` runs, then the `initial_attributes` value is not
  overwritten — explicit seed wins. `[pytest]`

- Given no `political_context` in the configuration, when `_apply_political_context`
  runs, then no `legitimacy_index` attribute is set on any entity. `[pytest]`

---

### US-PE-006 — legitimacy_index confidence tier and measurement framework

**As** a QA Lead validating political economy output provenance,
**I need** the seeded `legitimacy_index` to carry `confidence_tier=3` and
`measurement_framework="governance"`,
**so that** the output layer correctly classifies the legitimacy stock as a
Tier 3 governance variable — consistent with the formula-based calibration
status documented in ADR-001.

**Acceptance criteria:**

- Given a seeded `legitimacy_index` Quantity from `_apply_political_context`,
  when its metadata is read, then `confidence_tier=3` and
  `measurement_framework=MeasurementFramework.GOVERNANCE`. `[pytest]`

- Given `confidence_tier=3` on `legitimacy_index`, when horizon degradation
  is applied at step 5 (5 projection steps), then `effective_tier` is clamped
  to 4 (3 + 1 degradation step, cap Tier 5). `[pytest]`

---

## Group 4 — Social Response Events: Legitimacy Threshold Crossings

### US-PE-007 — legitimacy_change event emitted on fiscal and emergency shocks

**As** Eleni Papadimitriou watching the human cost ledger,
**I need** the simulation to emit a `legitimacy_change` event whenever a prior-step
fiscal spending cut, tax increase, or emergency policy event erodes legitimacy,
**so that** I can see the political cost of austerity decisions expressed as a
trajectory — not just as an abstract coefficient.

**Acceptance criteria:**

- Given a prior-step `fiscal_policy_spending_change` event with a negative magnitude,
  when `PoliticalEconomyModule.compute()` runs at the next step, then a
  `legitimacy_change` event is emitted with `affected_attributes.legitimacy_index`
  delta negative (erosion). `[pytest]`

- Given a prior-step `emergency_policy_capital_controls` event, when
  `PoliticalEconomyModule.compute()` runs, then a `legitimacy_change` event is
  emitted with delta ≥ `−EMERGENCY_EROSION_FACTOR` (−0.10 base, amplified if
  legitimacy < 0.5). `[pytest]`

- Given no prior-step subscribed events and no `legitimacy_index` attribute,
  when `PoliticalEconomyModule.compute()` runs, then no events are emitted —
  module returns `[]`. `[pytest]`

- Given a `legitimacy_change` event, then its `measurement_framework` is
  `MeasurementFramework.GOVERNANCE` and `confidence_tier=3`. `[pytest]`

---

### US-PE-008 — Fragility amplifier doubles erosion when legitimacy < 0.5

**As** a QA Lead validating the non-linear political collapse model,
**I need** the fragility amplifier to apply a ×1.5 erosion multiplier when
current `legitimacy_index` is below 0.5,
**so that** the simulation captures the empirically documented phenomenon that
fragile governments deteriorate faster under the same austerity shock than
stable ones — preventing false confidence in high-magnitude programmes applied
to already-fragile administrations.

**Acceptance criteria:**

- Given `legitimacy_index=0.40` (below fragility threshold) and a
  `fiscal_policy_spending_change` event with magnitude `−0.05`, when
  `_compute_legitimacy_delta` runs, then the delta magnitude is
  `0.05 × 0.08 × 1.5 = 0.006` (absolute). `[pytest]`

- Given `legitimacy_index=0.60` (above fragility threshold) and the same event,
  when `_compute_legitimacy_delta` runs, then the delta magnitude is
  `0.05 × 0.08 × 1.0 = 0.004` — no amplification. `[pytest]`

- Given `legitimacy_index=0.50` (exactly at threshold), when the amplifier
  is evaluated, then no amplification applies — `FRAGILITY_THRESHOLD` is a
  strict less-than comparison. `[pytest]`

- Given cumulative erosion that would reduce `legitimacy_index` below 0.0,
  when the new legitimacy is computed, then it is clamped to `0.0` — never
  negative. `[pytest]`

---

## Group 5 — Conditionality: Structured Scenario Inputs

### US-PE-009 — IMF programme terms encoded as CONDITIONALITY-sourced ControlInputs

**As** Eleni Papadimitriou modelling an IMF structural adjustment programme,
**I need** to mark programme-mandated fiscal adjustments with
`InputSource.CONDITIONALITY`, `constraining_actor_id="IMF"`, and
`constraint_mechanism="DISBURSEMENT_SUSPENSION"`,
**so that** the audit trail distinguishes coerced decisions from voluntary
fiscal choices — a Greece finance minister can show which cuts were imposed,
not chosen.

**Acceptance criteria:**

- Given a `FiscalPolicyInput` with `source=InputSource.CONDITIONALITY`,
  `constraining_actor_id="IMF"`, and `constraint_mechanism="DISBURSEMENT_SUSPENSION"`,
  when the input is processed, then these fields are preserved and readable
  from the `ControlInputAuditRecord`. `[pytest]`

- Given a `FiscalPolicyInput` with `source=InputSource.SCENARIO_SCRIPT` (freely
  chosen), when the input is processed, then `constraining_actor_id` and
  `constraint_mechanism` default to empty strings — no conditionality attribution. `[pytest]`

- Given a scenario with mixed CONDITIONALITY and SCENARIO_SCRIPT inputs in the
  same step, when `decompose_conditionality()` is called, then only the
  CONDITIONALITY-sourced inputs appear in the decomposition output. `[pytest]`

---

### US-PE-010 — Conditionality inputs respect implementation_capacity scaling

**As** Eleni Papadimitriou modelling partial programme implementation,
**I need** conditionality-sourced inputs to apply `implementation_capacity` scaling
identically to voluntary inputs,
**so that** political resistance to programme terms is modelled correctly — a
condition mandating 3% GDP spending cuts but implemented at 60% capacity
transmits 1.8% GDP, not 3%.

**Acceptance criteria:**

- Given a CONDITIONALITY `FiscalPolicyInput` with `spending_delta=-0.03` and
  `implementation_capacity=0.60`, when `get_events()` is called, then the
  effective spending delta in the returned event is `−0.018`. `[pytest]`

- Given `implementation_capacity=1.0` on a CONDITIONALITY input, when
  `get_events()` is called, then the event magnitude equals the raw
  `to_events()` output — full conditionality transmission. `[pytest]`

---

## Group 6 — Conditionality Decomposition: Per-Term Cost Attribution

### US-PE-011 — decompose_conditionality() attributes costs per term and actor

**As** Eleni Papadimitriou reviewing programme costs,
**I need** `decompose_conditionality()` to produce one attribution record per
conditionality term showing the constraining actor, mechanism, fiscal delta,
and effective delta after capacity scaling,
**so that** I can see which creditor imposed which cost and by how much the
political resistance dampened the transmission — the conditionality audit trail
that makes coercion visible.

**Acceptance criteria:**

- Given two CONDITIONALITY inputs for entity "GRC" from "IMF" and "ECB"
  respectively, when `decompose_conditionality(inputs, "GRC")` is called,
  then two records are returned, one per actor, each containing
  `constraining_actor_id`, `constraint_mechanism`, `fiscal_delta`,
  `implementation_capacity`, and `effective_delta`. `[pytest]`

- Given `implementation_capacity=0.70` and `fiscal_delta=Decimal("-0.04")`,
  then `effective_delta=Decimal("-0.028")` in the returned record. `[pytest]`

- Given no CONDITIONALITY inputs for entity "GRC", when
  `decompose_conditionality(inputs, "GRC")` is called, then `[]` is returned. `[pytest]`

- Given a CONDITIONALITY input with `fiscal_delta=None` (event produces no
  affected_attributes magnitude), then `effective_delta=None` in the returned
  record — no division by zero, no crash. `[pytest]`

---

### US-PE-012 — summarise_by_actor() aggregates effective deltas per creditor

**As** Eleni Papadimitriou constructing a creditor cost summary,
**I need** `summarise_by_actor()` to aggregate `effective_delta` across all terms
from the same actor into a single total per creditor,
**so that** I can answer "what is the total fiscal shock attributable to IMF
conditionality in this step?" — a number that the finance minister can cite
in negotiations.

**Acceptance criteria:**

- Given two IMF terms with `effective_delta=Decimal("-0.02")` and
  `effective_delta=Decimal("-0.015")`, when `summarise_by_actor()` is called,
  then the "IMF" entry is `Decimal("-0.035")`. `[pytest]`

- Given a term with `effective_delta=None`, when `summarise_by_actor()` is
  called, then that term is excluded from aggregation — no KeyError or
  `None + Decimal` crash. `[pytest]`

- Given terms from "IMF" and "ECB", when `summarise_by_actor()` is called,
  then both keys appear in the returned dict with independent totals. `[pytest]`

---

## Group 7 — Programme Abandonment Probability

### US-PE-013 — programme_survival_probability surfaced as a Governance stock

**As** Eleni Papadimitriou monitoring programme viability,
**I need** the simulation to surface `programme_survival_probability` as a
confidence tier 4 stock in the Governance framework at each step,
**so that** I can see whether the programme's legitimacy trajectory makes
eventual collapse likely — enabling a pre-emptive design change rather than
a reactive crisis response.

**Acceptance criteria:**

- Given `legitimacy_index=0.70` and `PoliticalEconomyModule` active, when
  `compute()` runs, then a `programme_survival_update` event is emitted with
  `programme_survival_probability` in `affected_attributes`, value in
  `(0.01, 0.99)` (open interval — No False Precision gate). `[pytest]`

- Given `legitimacy_index=0.70`, when `_compute_survival_probability(0.70)`
  is called, then the result is approximately `0.81` (formula:
  `0.70 × (1 + 0.80 × 0.20) = 0.70 × 1.16 = 0.812`), clamped to `[0.01, 0.99]`. `[pytest]`

- Given `legitimacy_index=0.40`, when `_compute_survival_probability(0.40)`
  is called, then the result is approximately `0.644` (formula:
  `0.70 × (1 + 0.80 × −0.10) = 0.70 × 0.92 = 0.644`). `[pytest]`

- Given the survival probability event, then `confidence_tier=4` and
  `measurement_framework=MeasurementFramework.GOVERNANCE`. `[pytest]`

- Given the survival probability event metadata, then a `calibration_note`
  key is present stating the DIRECTION_ONLY calibration status and
  reference to Issue #44. `[pytest]`

---

### US-PE-014 — programme_survival_probability monotonically decreasing with legitimacy decline

**As** a QA Lead validating the survival probability model direction,
**I need** `programme_survival_probability` to decrease monotonically as
`legitimacy_index` decreases across a range of inputs,
**so that** the model asserts the directional correctness required by
DIRECTION_ONLY threshold — a deteriorating government is less likely to
sustain the programme, not more.

**Acceptance criteria:**

- Given `legitimacy_index` values `[0.80, 0.60, 0.40, 0.20]`, when
  `_compute_survival_probability` is called for each, then the returned values
  are strictly decreasing (each lower than the previous). `[pytest]`

- Given `legitimacy_index=0.0` (minimum), when `_compute_survival_probability`
  is called, then the result is `≥ 0.01` (lower clamp respected). `[pytest]`

- Given `legitimacy_index=1.0` (maximum), when `_compute_survival_probability`
  is called, then the result is `≤ 0.99` (upper clamp respected — no false
  certainty of survival). `[pytest]`

---

## Group 8 — Compound StateCondition: QA Contract

### US-PE-015 — CompoundStateCondition evaluates AND/OR multi-attribute triggers

**As** a QA Lead writing test stubs for conditionality trigger logic,
**I need** `CompoundStateCondition` to evaluate multi-attribute AND/OR conditions
against simulation state,
**so that** contingent conditionality can be tested — a disbursement suspension
that triggers only when BOTH gdp_growth < −0.03 AND legitimacy_index < 0.5
fires correctly and not prematurely.

**Acceptance criteria:**

- Given a `CompoundStateCondition` with `operator=LogicalOperator.AND` and two
  sub-conditions (A: `gdp_growth < -0.03`, B: `legitimacy_index < 0.5`),
  when both A and B are true in simulation state, then `evaluate(state)` returns
  `True`. `[pytest]`

- Given the same AND compound condition, when only A is true, then
  `evaluate(state)` returns `False`. `[pytest]`

- Given a `CompoundStateCondition` with `operator=LogicalOperator.OR`,
  when either A or B is true, then `evaluate(state)` returns `True`. `[pytest]`

- Given a `CompoundStateCondition` with `operator=LogicalOperator.OR`,
  when neither condition is true, then `evaluate(state)` returns `False`. `[pytest]`

- Given an empty `conditions` list in a `CompoundStateCondition`, when
  `evaluate(state)` is called, then the result is `False` for AND and `False`
  for OR (vacuously false) — no crash. `[pytest]`

---

## Group 9 — Elite Capture: Coefficient Configuration and Surfacing

### US-PE-016 — elite_capture_coefficient configured as entity attribute

**As** Eleni Papadimitriou modelling distributional effects of fiscal adjustment,
**I need** to supply `elite_capture_coefficient` as an entity attribute in
`initial_attributes`, with the default of `0.30` applying when absent,
**so that** I can calibrate the distributional distortion for specific countries —
Argentina 2001 uses `0.35` (Lustig 2001 calibration), Greece 2010 uses `0.35`
(PR #705 fixture), and a scenario without a known calibration falls back to
the conservative `0.30` default.

**Acceptance criteria:**

- Given `initial_attributes.GRC.elite_capture_coefficient=Quantity(value=0.35, ...)`,
  when `PoliticalEconomyModule.compute()` runs, then it reads `0.35` from
  `entity.get_attribute("elite_capture_coefficient")`. `[pytest]`

- Given no `elite_capture_coefficient` in `initial_attributes`, when
  `PoliticalEconomyModule.compute()` runs and a fiscal event is present, then
  the module uses `_DEFAULT_ELITE_CAPTURE_COEFFICIENT=0.30` (Argentina baseline). `[pytest]`

- Given `elite_capture_coefficient=0.0`, when an elite capture divergence event
  is computed, then `elite_capture_divergence` magnitude is `0.0` — zero capture,
  perfectly neutral distribution. `[pytest]`

---

### US-PE-017 — elite_capture_divergence emitted as Human Development event

**As** Eleni Papadimitriou reading the Human Cost Ledger,
**I need** `elite_capture_divergence` events to appear in the Human Development
measurement framework, not the Financial or Governance framework,
**so that** distributional inequality from capture is counted in the human cost
ledger alongside health and education impacts — not siloed in a financial
framework where it would be invisible to the Development Economist lens.

**Acceptance criteria:**

- Given a prior-step fiscal event with `fiscal_delta != 0` and
  `elite_capture_coefficient` set, when `PoliticalEconomyModule.compute()` runs,
  then an `elite_capture_divergence` event is emitted with
  `measurement_framework=MeasurementFramework.HUMAN_DEVELOPMENT`. `[pytest]`

- Given `fiscal_delta=Decimal("-0.04")` and `elite_capture_coefficient=0.35`,
  when the event is emitted, then `elite_capture_divergence` magnitude is
  `Decimal("-0.04") × Decimal("0.35") = Decimal("-0.014")`. `[pytest]`

- Given a positive `fiscal_delta` (fiscal stimulus), when the event is emitted,
  then `elite_capture_divergence` magnitude is positive — elite cohorts capture
  a disproportionate share of stimulus benefits. `[pytest]`

- Given the event metadata, then `interpretation` key is present explaining:
  "Positive: fiscal benefits captured by elite cohorts. Negative: fiscal costs
  borne disproportionately by non-elite." `[pytest]`

- Given `confidence_tier` on the event, then it is `4` — formula-based
  approximation, DIRECTION_ONLY calibration status. `[pytest]`

---

## Group 10 — Distributional Divergence: Zone Placement

### US-PE-018 — elite_capture_divergence placed in Zone 2 (Governance/HCL view)

**As** Eleni Papadimitriou navigating Zone 1 and Zone 2 instruments,
**I need** the `elite_capture_divergence` trajectory to surface in Zone 2 (the
Human Cost Ledger view), not Zone 1 (the primary instrument cluster),
**so that** distributional divergence is discoverable without crowding the
four primary Zone 1 instruments — it is always one navigation action away,
never hidden, but not competing with the trajectory view for Zone 1 space.

**Acceptance criteria:**

- Given a completed simulation step with `elite_capture_divergence` events,
  when the Zone 2 Human Cost Ledger view is rendered, then the
  `elite_capture_divergence` trajectory is visible as a labelled curve. `[Playwright]`

- Given `elite_capture_divergence` placed in Zone 2, when Zone 1 is viewed,
  then the `elite_capture_divergence` trajectory is not present in any Zone 1
  instrument — no Zone 1 overcrowding. `[Playwright]`

- Given `elite_capture_divergence` in Zone 2, then it is rendered alongside
  other Human Development framework outputs (health, education, cohort income)
  and labelled with a DIRECTION_ONLY confidence disclosure. `[Manual]`

- Given `confidence_tier=4` on `elite_capture_divergence`, when the Zone 2
  label renders, then a visual indicator (e.g. amber band) signals Tier 4
  confidence — not the same visual treatment as Tier 2 financial outputs. `[Manual]`

---

## Group 11 — Argentina Backtesting: Political Economy Validation

### US-PE-019 — Argentina 2001 legitimacy erosion direction matches historical record

**As** a QA Lead running the Argentina backtesting suite,
**I need** the legitimacy trajectory over the 2001–2002 crisis steps to show
monotonically declining `legitimacy_index` under Zero Deficit Plan conditionality,
**so that** the political economy module passes DIRECTION_ONLY validation against
the historical case — Lustig 2001 documents progressive legitimacy collapse
as De la Rúa's government implemented IMF-mandated austerity.

**Acceptance criteria:**

- Given the Argentina 2001–2002 backtesting fixture with `political_economy.enabled=true`,
  `legitimacy_index=0.60` (initial, pre-Zero Deficit Plan), and a CONDITIONALITY
  `FiscalPolicyInput` for the Zero Deficit Plan spending cuts, when the scenario runs
  two steps, then `legitimacy_index` at step 2 is less than at step 1. `[pytest]`

- Given the same scenario with the fragility amplifier active at step 2 (legitimacy
  below 0.5 after step 1 erosion), when step 2 runs, then the legitimacy erosion
  magnitude at step 2 is greater than at step 1 for the same fiscal shock size —
  the amplifier is observable in the trajectory. `[pytest]`

- Given the Argentina scenario output, then `programme_survival_probability` at step 2
  is lower than at step 1 — survival probability degrades with legitimacy. `[pytest]`

---

### US-PE-020 — Argentina 2001 elite capture divergence direction matches Lustig 2001

**As** a QA Lead validating the Human Cost Ledger against historical distributional data,
**I need** the `elite_capture_divergence` trajectory in the Argentina scenario to show
a positive value during the Zero Deficit Plan period (elite cohorts capturing fiscal
benefits from tax cuts while non-elite cohorts bear spending cuts),
**so that** the elite capture model passes DIRECTION_ONLY validation against the
Lustig 2001 distributional analysis — the sign of the divergence must match the
historical record before the module is trusted for forward projection.

**Acceptance criteria:**

- Given the Argentina fixture with `elite_capture_coefficient=0.35` (Lustig 2001
  calibration) and a CONDITIONALITY spending cut `fiscal_delta=Decimal("-0.065")`
  (Zero Deficit Plan), when the scenario runs, then `elite_capture_divergence`
  magnitude is `Decimal("-0.065") × Decimal("0.35") = Decimal("-0.02275")` —
  negative, confirming non-elite cohorts bear the disproportionate cost. `[pytest]`

- Given the sign of `elite_capture_divergence` is negative (costs borne by
  non-elite), when compared with Lustig 2001 finding that "the poorest quintile
  bore 2.3× their population-proportional share of the 2001 fiscal adjustment,"
  then the direction is confirmed correct — DIRECTION_ONLY threshold passes. `[Manual]`

- Given the Argentina backtesting fidelity report generated by
  `write_fidelity_artifact()`, then `elite_capture_direction_correct=True`
  appears as a passed threshold in the JSON report. `[pytest]`

---

## Calibration Notes

All political economy thresholds are **DIRECTION_ONLY** (ADR-004 Decision 3). No
MAGNITUDE_WITHIN_20PCT thresholds are asserted for political economy outputs in M11.
Full statistical calibration against historical programme failure timing, distributional
panel data, and legitimacy survey series is deferred to Issue #44 (Milestone 4).

Confidence tiers:
- `legitimacy_index` stock: Tier 3 (formula-based, single composite index)
- `programme_survival_probability`: Tier 4 (formula-based approximation,
  calibrated from 3 historical cases only)
- `elite_capture_divergence`: Tier 4 (formula-based, Lustig 2001 single-country
  calibration)

All Tier 4 outputs carry `confidence_tier=4` in their Quantity and must render with
appropriate visual uncertainty treatment when surfaced in Zone 2.

Sources: Lustig 2001 (Argentina distributional analysis), Przeworski et al. 2000
(fragility amplifier), Greece 2010 Eurobarometer 73 (initial legitimacy seed),
Ecuador 2000 / Argentina 2001 / Greece 2012 (programme failure timing).
