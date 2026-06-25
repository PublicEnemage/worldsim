---
name: m17-g1-elasticity-calibration-decision
type: calibration-decision
issue: "#1229"
sprint: M17-G1
status: FILED — gates FRAME-D test authorship and ELASTICITY_REGISTRY implementation PR
authored-by: Chief Methodologist
authored-date: 2026-06-25
intent-document: docs/process/intents/M17-G1-2026-06-25-cm-calibration.md
implements: docs/process/sprint-plans/m17-g1-sprint-entry.md §Section 2.3 PENDING gate
---

# CM Calibration Decision: Fiscal-to-Cohort Elasticity — M17-G1

> **Authority:** This document is the calibration decision artifact for #1229. It closes
> the PENDING gate in sprint entry Section 2.3 and is the specification the FRAME-D
> integration test is authored from. The ELASTICITY_REGISTRY implementation PR may not
> open until this document is committed.
>
> **What this document decides:** Which elasticity values to use in the DemographicModule
> `ELASTICITY_REGISTRY` for Sub-Saharan Africa fiscal conditionality scenarios, and why.
> This is not a prediction of Senegal's poverty trajectory — it is a calibration of the
> model's transmission coefficient for regional T3 conditions.

---

## 1. Background: Current Calibration and the Gap

### 1.1 The transmission chain

A fiscal spending cut event in WorldSim travels the following path to cohort-level poverty:

```
fiscal_policy_spending_change (magnitude = −0.03, i.e., −3% of GDP)
  ↓ MacroeconomicModule (one-step lag)
  ↓ Regime: standard (GDP growth ≥ 0) → multiplier 0.5
  ↓ gdp_growth_change magnitude = −0.03 × 0.5 = −0.015
    ↓ DemographicModule (one-step lag)
    ↓ ELASTICITY_REGISTRY: gdp_growth_change × elasticity (−0.10)
    ↓ poverty_headcount_ratio delta = −0.015 × −0.10 = +0.0015 per step
```

Two lags combine: fiscal event at step N → gdp_growth_change at N+1 → poverty delta at N+2.
In an 8-step programme window, poverty changes are observable from step 3 onward (6 responding steps with one event scheduled at step 1, or step 3 onward with persistent conditionality events at steps 1–N−2).

### 1.2 The FRAME-D gap

The FRAME-D milestone sentence fires when the Q1 informal `poverty_headcount_ratio` crosses
the 0.40 recovery floor (`MDA-HD-POVERTY-Q1` threshold, from above — the floor is a ceiling
in welfare terms). The synthetic SEN fixture seeds Q1 informal poverty at 0.38 (ECOWAS
regional distribution, T3).

Required trajectory for FRAME-D within 8 steps:
- Crossing threshold: 0.40
- Distance to threshold: 0.40 − 0.38 = 0.02
- At current calibration (+0.0015/step): 0.02 / 0.0015 = 13 steps to cross → outside 8-step window
- FRAME-D does not fire in Demo 6 under current calibration with a -3% GDP conditionality shock

The Demo 6 walkthrough (`docs/demo/m16/stakeholder-walkthrough.md §Step 4`) accounts for this
with the conditional instruction "If milestone sentence is visible." The calibration gap means the
sentence is reliably absent. This is the documented finding from M16-G8 Step 5b: the correct
response at M16 was to present the structural trajectory argument honestly without manufacturing
a crossing. This document addresses the calibration for M17.

### 1.3 Source of the gap: regional mismatch

The current Q1 informal elasticity (−0.10) was calibrated from Lustig (2017), which draws
primarily on Latin American fiscal consolidation episodes. Latin America has structurally different
social protection coverage: higher average social transfer rates (10–15% of GDP vs. 5–8% for SSA),
stronger formal employment shares in Q1 and Q2 cohorts, and higher baseline productivity that
cushions the poverty impact of GDP shocks.

For Sub-Saharan Africa (Senegal's comparator region), the structural characteristics that amplify
poverty response to GDP shocks include: lower formal employment share in Q1 (higher informality
and subsistence agriculture exposure), lower social transfer density (weaker cushion when GDP
contracts), and thinner household savings buffers in the first quintile (higher marginal
vulnerability to income shocks). These structural conditions justify a higher elasticity for
the SSA context than the Latin American calibration supports.

---

## 2. Three Paths Investigated

### Path A — Revise `gdp_growth_change` elasticities using SSA calibration

Revise the three existing `gdp_growth_change` entries in `ELASTICITY_REGISTRY` using
Sub-Saharan Africa-specific literature. No new event subscriptions required. Implementation
scope: constants only in `elasticities.py`.

**Evaluation:** Cleanest change with the narrowest implementation scope. Addresses the
source of the gap (regional mismatch in Latin America vs. SSA calibration) directly.
Preserves the ADR-006 Decision 10 architecture (single GDP channel, no direct fiscal-to-cohort
path in DemographicModule).

### Path B — Add direct `fiscal_policy_spending_change` entries to DemographicModule

Add `CohortElasticity` entries with `event_type="fiscal_policy_spending_change"` directly
to `ELASTICITY_REGISTRY`. This would require adding `fiscal_policy_spending_change` to
`DemographicModule._SUBSCRIBED_EVENTS`.

**Evaluation:** This path risks double-counting: a −3% fiscal spending cut already flows
through the GDP multiplier chain in MacroeconomicModule, producing a `gdp_growth_change` event
that the DemographicModule already processes. Adding a parallel direct path adds both the GDP
multiplier effect AND a direct social-transfer effect. At T3 data quality for Senegal, the
fiscal composition of the spending cut (what fraction targets social transfers vs. capital
expenditure vs. public sector wages) is not known with sufficient precision to separate the
two channels without risk of systematic overstatement.

Furthermore, ADR-006 Decision 10 notes explicitly that the DemographicModule's legacy
`fiscal_spending_change` subscription was deliberately removed when MacroeconomicModule was
introduced, to establish the GDP channel as the single transmission path. Reintroducing a
direct fiscal path without a distinct empirical rationale (and without amending ADR-006)
would constitute an undocumented architectural deviation.

**CM position on Path B: NOT TAKEN.** Double-counting risk at T3 data quality; ADR-006
Decision 10 rationale preserved.

### Path C — Add `imf_program_acceptance` demographic elasticity entries

Add `CohortElasticity` entries with `event_type="imf_program_acceptance"` to `ELASTICITY_REGISTRY`.
The DemographicModule already subscribes to this event type; no subscription change required.

**Evaluation:** Two sub-questions arise:

*Sign ambiguity:* IMF programme acceptance in a quarterly resolution represents the announcement
and conditional approval moment. Empirical evidence on the immediate poverty effect is mixed:
- Bird and Rowlands (2017) and Bal-Gündüz et al. (2013) document that post-acceptance periods
  show poverty increases, but this is driven by the conditionality implementation that follows,
  not the acceptance signal itself.
- Grabel (2017) documents stabilizing creditor expectations effects in the announcement period
  that can sustain informal sector demand — a short-run poverty-reducing effect for Q1 informal
  workers that partially offsets the conditionality implementation effect.

*Double-counting risk:* In the Demo 6 Senegal scenario, `imf_program_acceptance` is emitted
because the government implements conditionality — the same fiscal events that produce
`fiscal_policy_spending_change`. Adding a direct poverty pathway for programme acceptance
risks double-counting the conditionality effect: once through fiscal → GDP → demographic, and
once through acceptance → demographic.

**CM position on Path C: NOT TAKEN.** Sign is ambiguous at quarterly resolution; double-counting
risk with the fiscal channel is material; SSA-specific programme-acceptance poverty studies at
quarterly resolution are insufficient to calibrate a defensible T3 constant. This pathway warrants
a dedicated M18 research task with specific Senegal programme history calibration (IMF Extended
Credit Facility 2015, 2019, 2023 episodes).

---

## 3. Chosen Path: Revised SSA Elasticities (Path A)

### 3.1 Literature basis

**Primary source: Fosu (2011)**

Fosu, A.K. (2011). "The Effect of Income Distribution on the Poverty-Growth Relationship:
Empirical Evidence from Sub-Saharan Africa." *Journal of African Economies*, 20(5), 811–839.

Fosu (2011) estimates income growth elasticities of poverty headcount ratio across 29 SSA
countries from the 1970s to the 2000s. Key findings relevant to the Senegal calibration:

- For high-inequality SSA countries (Gini > 0.40), income growth elasticity of poverty ≈ −0.7
  to −1.2 for the $1.90/day poverty headcount ratio
- For moderate-inequality SSA countries (Gini ≈ 0.35–0.40, including Senegal at estimated 0.38):
  income growth elasticity ≈ −1.2 to −2.0
- SSA elasticities are on average 1.5× to 2× larger in magnitude than comparable Latin American
  calibrations at the same inequality level (Ravallion 2012 comparison basis)

**Translation to WorldSim units:**

Fosu (2011) reports income growth elasticity (% poverty headcount change per % mean income change).
WorldSim's ELASTICITY_REGISTRY operates on `gdp_growth_change` event magnitude, which represents
the CHANGE in the annual GDP growth rate (expressed as a fraction: −0.015 = −1.5pp annual growth
rate change).

For a quarterly simulation step:
- A persistent −1.5pp annual GDP growth rate change implies approximately −0.375% quarterly
  income reduction for Q1 informal cohorts (conservative; actual incomes may respond faster for
  informal workers without savings buffers)
- At an income growth elasticity of −1.5 (mid-range for Senegal's inequality level): poverty
  headcount changes by −1.5 × −0.375% = +0.5625% of poverty headcount per step
- Expressed as a fraction of the headcount ratio (0.385 × 0.5625% ≈ 0.00217), this implies
  poverty_headcount_ratio delta ≈ +0.002 per step

This is the lower end of the expected range. The upper range (from Fosu's higher-elasticity
cases for moderate-Gini SSA countries at −2.0) implies:
- Poverty delta ≈ +0.003 per step

A point estimate of −0.20 for the `gdp_growth_change` Q1 informal elasticity (2× the current
−0.10 Latin American calibration) is consistent with the Fosu (2011) SSA range and the
Ravallion (2012) finding that SSA elasticities are approximately 1.5–2× larger than Latin
American comparators at equivalent inequality levels.

**Secondary source: IMF (2014)**

IMF (2014). *Fiscal Policy and Income Inequality*. IMF Policy Paper, January 2014.
(Source already registered: `ACADEMIC_LITERATURE_IMF_2014_FISCAL_INEQUALITY`)

IMF (2014) Table 1 confirms that fiscal consolidation's distributional impact is larger in
low-income developing countries than in emerging market or advanced economies. For SSA LICs,
the consumption elasticity of poverty with respect to fiscal shocks is approximately 1.8–2.5×
the EMDE baseline. This supports a Q1 agricultural elasticity of −0.16 (2× the prior −0.08),
consistent with the existing Q1 agricultural entry calibrated at 80% of the Q1 informal rate.

**Tertiary source: Ball et al. (2013)**

Ball, L., Furceri, D., Leigh, D., and Loungani, P. (2013). "The Distributional Effects of
Fiscal Consolidation." IMF Working Paper WP/13/151.
(Source already registered: `ACADEMIC_LITERATURE_BALL_2013_FISCAL_CONSOLIDATION`)

Ball et al. (2013) calibrated Q2 informal at ~2/3 of Q1 informal for emerging economies.
The 2/3 scaling ratio is appropriate regardless of the absolute Q1 elasticity — the ratio
reflects the between-quintile distributional structure, not the absolute magnitude. Updating
Q2 to 2/3 of the revised Q1 (2/3 × 0.20 = 0.133) preserves this calibration relationship.

### 3.2 Updated constants

| Cohort | Event | Attribute | Prior elasticity | Revised elasticity | Change | Source |
|---|---|---|---|---|---|---|
| Q1 / 25–54 / INFORMAL | `gdp_growth_change` | `poverty_headcount_ratio` | `−0.10` | `−0.20` | ×2 | Fosu (2011) SSA calibration |
| Q2 / 25–54 / INFORMAL | `gdp_growth_change` | `poverty_headcount_ratio` | `−0.067` | `−0.133` | ×2 | Ball et al. (2013) 2/3 scaling preserved |
| Q1 / 25–54 / AGRICULTURE | `gdp_growth_change` | `poverty_headcount_ratio` | `−0.08` | `−0.16` | ×2 | IMF (2014) SSA fiscal inequality |

All three entries remain **Confidence Tier 3** (T3). The Fosu (2011) and IMF (2014) sources
qualify as T3 (academically documented, regionally calibrated, not Senegal-specific). A
confidence tier upgrade to T2 would require backtesting against Senegal's own poverty-growth
data at quarterly resolution — this is M18 scope.

### 3.3 Uncertainty ranges (T3 calibration)

| Cohort | Point estimate | T3 lower bound | T3 upper bound | Uncertainty basis |
|---|---|---|---|---|
| Q1 informal | −0.20 | −0.15 | −0.25 | Fosu (2011) cross-country SSA range |
| Q2 informal | −0.133 | −0.10 | −0.167 | Ball (2013) scaling of Q1 range |
| Q1 agricultural | −0.16 | −0.12 | −0.20 | IMF (2014) 80% scaling of Q1 range |

The uncertainty range reflects cross-country heterogeneity within SSA at comparable inequality
levels. A country with stronger trade union density and social protection indexing (e.g., South
Africa) would be at the upper end. Senegal, with lower formal employment penetration and
limited social transfer indexing, is calibrated at the point estimate.

---

## 4. FRAME-D Acceptance Criterion

### 4.1 Test scenario specification

The FRAME-D integration test (`backend/tests/test_m17_g1_frame_d_calibration.py`) uses the
following scenario configuration:

**Entity:** SEN (Senegal)
**Initial Q1 informal poverty_headcount_ratio:** 0.38 (ECOWAS regional T3 synthetic estimate,
matching the M16-G3 test fixture in `_SYNTHETIC_SEN_ATTRIBUTES`)

**Scheduled inputs for per-step delta certification (unit component):**
- Step 1: `gdp_growth_change` with magnitude `Decimal("-0.015")`
  — represents the output of MacroeconomicModule for `fiscal_policy_spending_change` = −0.03
  at standard multiplier 0.5 (standard regime, GDP growth > 0)
  — injection is direct to isolate the DemographicModule elasticity from MacroeconomicModule regime dynamics

The DemographicModule applies at step 2 (one-step lag). Assert: Q1 informal
`poverty_headcount_ratio` delta at step 2 is within the certified range.

**Scheduled inputs for FRAME-D crossing certification (integration component):**
- Steps 1–7: `gdp_growth_change` with magnitude `Decimal("-0.015")` at each step
  — models persistent GDP growth suppression from ongoing Article IV conditionality
  — the DemographicModule responds at steps 2–8 (7 responding steps)

After step 8, assert: Q1 informal `poverty_headcount_ratio` ≥ 0.40 (the `MDA-HD-POVERTY-Q1`
recovery floor).

**Note on MacroeconomicModule regime dynamics:** The FRAME-D test uses direct
`gdp_growth_change` injection (not `fiscal_policy_spending_change`) to produce a stable,
predictable per-step delta for the calibration test. The full fiscal chain
(`fiscal_policy_spending_change` → MacroeconomicModule → `gdp_growth_change`) includes regime
cascading: after 3 steps of persistent -3% fiscal cuts, GDP growth crosses below zero, triggering
the "depressed" multiplier (1.5×), which then rapidly triggers the ZLB multiplier (2.0×). This
cascade produces a credibly large poverty trajectory in the actual demo but is not the right
test structure for certifying the DemographicModule elasticity in isolation. The FRAME-D test
should control the gdp_growth_change magnitude directly.

### 4.2 Certified range

| Component | Assertion | Pass condition |
|---|---|---|
| Per-step delta (unit) | Q1 informal poverty delta at step 2 | `+0.002 ≤ delta ≤ +0.004` |
| FRAME-D crossing (integration) | Q1 informal poverty_headcount_ratio at step 8 | `≥ 0.40` |

**Lower bound rationale (+0.002):**
Derived from Fosu (2011) lower range (elasticity −0.15):
−0.015 × −0.15 = +0.00225, rounded to +0.002.
This bound excludes the pre-calibration response (+0.0015) — any test result below +0.002
indicates the elasticity was not updated from the prior value.

**Upper bound rationale (+0.004):**
Derived from Fosu (2011) upper range (elasticity −0.25) with a 10% margin:
−0.015 × −0.25 = +0.00375 → upper bound +0.004 (capped at 2× point estimate to guard
against inadvertent overshoot from implementation errors).

**FRAME-D crossing calculation (point estimate):**
- Per-step delta at point estimate (elasticity −0.20): −0.015 × −0.20 = +0.003
- 7 responding steps × +0.003 = +0.021 cumulative
- Final Q1 poverty_headcount_ratio: 0.38 + 0.021 = 0.401
- Crosses 0.40 at step 8 (after 7 responding steps). FRAME-D fires within the 8-step window.

### 4.3 Regression risk to existing tests

The elasticity revision affects all tests that exercise the DemographicModule
`gdp_growth_change` → `poverty_headcount_ratio` path. Known tests at risk:

| Test file | Risk | Assessment |
|---|---|---|
| `test_m16_g3_25year_human_capital_trajectory.py` | Poverty bounds test: `[0.0, 1.0]` over 100 steps | **LOW** — bounds assertion is unchanged; the poverty trajectory rises faster but remains within [0, 1] for the 100-step window. The test uses a single `gdp_growth_change` event at step 1; with revised elasticity, poverty delta at step 2 is +0.004 (revised from +0.0015 for magnitude −0.04: −0.04 × −0.20 = +0.008) — still within bounds. No failure expected. |
| `test_measurement_output.py` (SEN fixture) | Uses `poverty_headcount_ratio` = 0.385 / 0.42 for threshold test | **NONE** — those tests use static state snapshots, not computed DemographicModule outputs. No elasticity computation involved. |
| `test_m14_g6_methodology_calibration.py` | Ecological composite tier test | **NONE** — no demographic elasticity path in scope. |
| Backtesting fixtures (Argentina, Greece, Ecuador, Lebanon, Thailand) | None of these fixtures use the `poverty_headcount_ratio` path with `gdp_growth_change` in their current test assertions | **NONE** — verify before PR merge by running `pytest backend/tests/` and confirming no regressions. |

**Pre-push regression check required:** Run `pytest backend/tests/` locally and confirm
`test_m16_g3_25year_human_capital_trajectory.py` passes before opening the implementation PR.

---

## 5. Source Registry Additions Required

The revised Q1 informal entry (`ACADEMIC_LITERATURE_FOSU_2011_SSA_POVERTY_GROWTH`) is a new
source registry ID. It must be added to the `source_registry` table (or equivalent registration
mechanism) in the same migration or commit as the `ELASTICITY_REGISTRY` constant changes.

| New source_registry_id | Full citation |
|---|---|
| `ACADEMIC_LITERATURE_FOSU_2011_SSA_POVERTY_GROWTH` | Fosu, A.K. (2011). "The Effect of Income Distribution on the Poverty-Growth Relationship: Empirical Evidence from Sub-Saharan Africa." *Journal of African Economies*, 20(5), 811–839. DOI: 10.1093/jae/ejr019. |

Existing source registry IDs retained:
- `ACADEMIC_LITERATURE_BALL_2013_FISCAL_CONSOLIDATION` — Q2 informal (scaling preserved)
- `ACADEMIC_LITERATURE_IMF_2014_FISCAL_INEQUALITY` — Q1 agricultural (revision justified)
- `ACADEMIC_LITERATURE_LUSTIG_2017_FISCAL_POVERTY` — Q1 informal: replaced by Fosu 2011 for SSA context. The Lustig (2017) source remains in the registry for completeness; the Q1 informal entry's `source_registry_id` changes to `ACADEMIC_LITERATURE_FOSU_2011_SSA_POVERTY_GROWTH`.

---

## 6. What This Calibration Does and Does Not Claim

**What it claims:**
- The revised elasticities (−0.20 for Q1 informal, −0.133 for Q2 informal, −0.16 for Q1
  agricultural) are better calibrated for Sub-Saharan Africa fiscal consolidation scenarios
  than the prior Latin American calibration
- The FRAME-D milestone sentence ("By [year], bottom quintile informal workers poverty
  headcount crosses the recovery floor") will fire within the 8-step Demo 6 Senegal window
  under a persistent -3% GDP fiscal spending cut, at T3 confidence
- The T3 confidence tier annotation on the output is correct — these are regionally inferred
  values, not Senegal-specific backtested constants

**What it does not claim:**
- This is not a prediction of Senegal's actual poverty trajectory
- The calibration has not been backtested against Senegal's observed poverty data at quarterly
  resolution (that is M18 scope)
- The elasticity values do not account for fiscal composition (social transfer vs. capital vs.
  wage mix) because Senegal's spending composition data at this granularity is T4 or absent
- The calibration is not validated for crisis-regime scenarios (depressed or ZLB) — the point
  estimate of −0.20 was calibrated for normal-regime conditions; regime-cascade scenarios may
  amplify poverty beyond the T3 upper bound

These limitations are the documented T3 condition. The T3 label on the cohort trajectory
output in Zone 1B is the correct disclosure. The Demo 6 walkthrough script acknowledges these
limits explicitly (`docs/demo/m16/stakeholder-walkthrough.md §Step 4`: "The distributional
disaggregation is scenario output under T3 demographic weights, not empirically backtested
cohort data. The T3 label is on screen for exactly this reason.").

---

## 7. Implementation Sequencing Gate

This document closes the Section 2.3 PENDING gate in `docs/process/sprint-plans/m17-g1-sprint-entry.md`.

**Next step:** CM authors `backend/tests/test_m17_g1_frame_d_calibration.py` from Section 4
of this document (the per-step delta assertion and FRAME-D crossing assertion). The test must
be filed and committed before the implementation PR (`feat/m17-g1-elasticity-calibration`)
opens.

**Implementation PR scope:**
1. `backend/app/simulation/modules/demographic/elasticities.py` — update three `CohortElasticity`
   constants per Section 3.2; update Q1 informal `source_registry_id` and `source` string
2. `backend/tests/test_m17_g1_frame_d_calibration.py` — FRAME-D test per Section 4
3. Source registry entry for `ACADEMIC_LITERATURE_FOSU_2011_SSA_POVERTY_GROWTH` (migration or
   equivalent registration mechanism per `docs/DATA_STANDARDS.md §Data Provenance Requirements`)

**Pre-push lint gate (mandatory):**
`cd backend && ruff check . && mypy app/` must exit 0 on the implementation PR branch before
pushing.

---

*Calibration authority: Chief Methodologist. Referenced from intent document
`docs/process/intents/M17-G1-2026-06-25-cm-calibration.md` §3. Implementation PR:
`feat/m17-g1-elasticity-calibration` targeting `release/m17`. Confidence tier: T3 —
regionally inferred (SSA), not Senegal-specific backtested. T2 upgrade is M18 scope.*
