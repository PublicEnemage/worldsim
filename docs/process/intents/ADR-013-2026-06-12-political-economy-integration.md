---
name: ADR-013-political-economy-integration
type: intent
adr: ADR-013
authored-by: Architect Agent
date: 2026-06-12
implementing-agent: Architect Agent (backend); QA Lead Agent (tests)
---

# Implementation Intent: ADR-013 — Political Economy Integration

## 1. Source ADR

**ADR:** ADR-013 — Political Economy Module — Conditionality Modelling, Elite Capture, and Political Feasibility
**Status at time of authorship:** Accepted
**Authored by:** Architect Agent
**Date:** 2026-06-12
**Implementing agent:** Architect Agent

---

## 2. Persona Trace Elements Targeted

**P-1 — Persona served:**
Primary: Persona 2 — Finance Ministry Negotiator (Eleni Papadimitriou archetype).
Secondary: Persona 3 — Political Advisor (Andreas Stefanidis archetype).

**P-2 — Entry state:**
Reactive entry state (90-second ceiling) for programme survival alert (Decision 1).
Preparatory entry state (20–40 minutes) for conditionality attribution (Decision 2) and elite capture (Decision 3).

**P-3 — Journey step:**
Primary: Journey A Step 5 — "Drill down: identify the argument components."
Decision 2 closes the `[Near-Term-Gap]`: "which specific conditionality term drove the threshold crossing."
Secondary: Journey B Step 3 — "Scan: read the top MDA alert." Decision 1 surfaces in Zone 1B.

**P-4 — Time/interaction ceiling:**
- Decision 1 (programme survival alert): visible in Zone 1B within 5 seconds of scenario selection when `programme_survival_probability < 0.25`.
- Decision 2 (conditionality attribution): accessible via `GET /measurement-output` in ≤ 2 API calls.
- Decision 3 (elite capture): same as Decision 2.
- Decision 4 (composite score): in trajectory API response without additional calls.

**P-6 — Negotiating leverage delivered:**
"The IMF's FISCAL_CONSOLIDATION conditionality term accounts for an effective delta of 3.2% of GDP in year 2, which is the primary driver of the poverty headcount CRITICAL alert at step 2. Our counter-proposal removes this term and replaces it with a revenue measure that achieves the same fiscal target without triggering the alert. Programme survival probability at that threshold is 0.18 — lower than any historically completed IMF programme in this region."

**P-7 — North star capability delivered:**
After this implementation, the finance minister's specialist can identify which specific conditionality term drives a threshold crossing and can cite programme survival probability as evidence that the programme is already at political viability risk — two arguments that were analytically unavailable before.

---

## 3. Observable Application State

### 3.1 Primary observable state

With a scenario fixture containing Greece entity (GRC) with `legitimacy_index=0.4` and
two CONDITIONALITY inputs (constraining_actor_id="IMF", constraint_mechanism="FISCAL_CONSOLIDATION"
and constraining_actor_id="IMF", constraint_mechanism="PENSION_CUT") seeded as prior-step events,
at step 2:

**Backend API:**
`GET /api/v1/scenarios/{hellenic_scenario_id}/measurement-output?entity_id=GRC&step=2`
returns a JSON object where `outputs.political_economy.indicators` contains:
- `programme_survival_probability` with a non-null value in [0.01, 0.99]
- At least one key matching `conditionality_term_IMF_FISCAL_CONSOLIDATION` with a non-null value
- At least one key matching `conditionality_term_IMF_PENSION_CUT` with a non-null value
- `elite_capture_divergence_index` with a non-null value (requires `elite_capture_coefficient` seeded on entity)
- `elite_capture_divergence_top_quintile` with a non-null value
- `elite_capture_divergence_bottom_quintile` with a non-null value

The `outputs.political_economy` key must exist in the response.

### 3.2 Secondary observable states

**MDA alert visible in Zone 1B (reactive state):**
With a scenario where entity GRC has `programme_survival_probability < 0.25` after step advance,
the events_snapshot stored for that step must contain an MDA breach event with:
- `mda_id = "PE-001-programme-survival-critical"`
- `severity = "CRITICAL"`
- `indicator_key = "programme_survival_probability"`

This is confirmed by `GET /api/v1/scenarios/{id}/measurement-output?entity_id=GRC&step=N`
returning `outputs.political_economy.mda_alerts` with at least one entry matching the above.

**Composite score in trajectory response:**
`GET /api/v1/scenarios/{id}/trajectory?entity_id=GRC` returns trajectory steps where
the political economy composite score is available as a non-null float in the measurement
output API for the entity, computed as the arithmetic mean of three normalized inputs
(programme_survival_probability, normalized elite_capture_divergence_index, legitimacy_index).

### 3.3 Silent failure detection

**Silent failure 1 — no programme_survival_probability in political_economy indicators:**
Observable indicator: `outputs.political_economy.indicators` in the measurement output response
is empty or contains no `programme_survival_probability` key for an entity with `legitimacy_index`
seeded. This indicates the module did not emit the attribute or the measurement output layer
did not classify it under `political_economy`.
**How to distinguish from genuine output:** a genuine output has `programme_survival_probability`
present and non-null. A silent failure shows either an empty indicators dict or the key absent.

**Silent failure 2 — conditionality terms absent despite CONDITIONALITY inputs:**
Observable indicator: `outputs.political_economy.indicators` in the measurement output response
has no keys matching `conditionality_term_*` even when the scenario has CONDITIONALITY inputs.
**How to distinguish:** query with a scenario that has at least one CONDITIONALITY input; if
`conditionality_term_*` keys are absent, the decomposer was not called or conditionality
metadata was not propagated through events.

**Silent failure 3 — programme_survival MDA alert not in events_snapshot:**
Observable indicator: `outputs.political_economy.mda_alerts` is empty even when
`programme_survival_probability < 0.25` is present in the indicators.
**How to distinguish:** PE-001 threshold must be seeded in `mda_thresholds`; if the alert
is absent with probability < 0.25, the threshold row is missing or the MDAChecker is not
checking the `political_economy` framework.

---

## 4. Acceptance Criteria

**AC-1:** In a test scenario with entity GRC seeded with `legitimacy_index=0.4` and at
least one CONDITIONALITY input (constraining_actor_id="IMF", constraint_mechanism="FISCAL_CONSOLIDATION"),
when the scenario is advanced one step, then `GET /measurement-output?entity_id=GRC&step=1`
returns `outputs.political_economy.indicators.programme_survival_probability` as a non-null
Decimal value in (0.01, 0.99).

**AC-2:** In the same scenario as AC-1, when the scenario is advanced one step, then
`GET /measurement-output?entity_id=GRC&step=1` returns
`outputs.political_economy.indicators.conditionality_term_IMF_FISCAL_CONSOLIDATION`
as a non-null Decimal value.

**AC-3:** In a scenario where `programme_survival_probability` falls below 0.25 after
step advance (achievable with `legitimacy_index=0.2`), when the step snapshot is written,
then the events_snapshot for that step contains an `mda_breach` event with
`mda_id = "PE-001-programme-survival-critical"` and `severity = "CRITICAL"`.

**AC-4:** In a scenario with entity GRC seeded with `elite_capture_coefficient=0.3` and
a prior-step fiscal spending event, when advanced one step, then
`GET /measurement-output?entity_id=GRC&step=1` returns
`outputs.political_economy.indicators.elite_capture_divergence_index` as a non-null Decimal.

**AC-5:** In a scenario with the political economy module enabled, when
`GET /measurement-output?entity_id=GRC&step=1` is called, the response contains
`outputs.political_economy` as a top-level framework key alongside `outputs.financial`,
`outputs.human_development`, `outputs.ecological`, and `outputs.governance`.

**AC-6:** In a scenario with no CONDITIONALITY inputs, when advanced and measurement
output queried, then `outputs.political_economy.indicators` contains no keys matching
`conditionality_term_*` (conditionality attribution must not appear for non-conditionality scenarios).

---

## 5. Kryptonite Constraint Check

**Does this implementation's primary observable state require specialist mediation for Persona 2
to act on it in the Reactive entry state (90-second ceiling)?**

`[x]` No — the observable state is interpretable by Persona 2 without an analyst translating it.

**Rationale:** The programme survival probability alert fires in Zone 1B with "Programme Survival
Probability — CRITICAL" text and a Tier 3 disclosure. The probability value (e.g., 0.21) with the
disclosure "below 0.25 indicates historically failed programme conditions" gives Persona 2 a
specific, citable argument without specialist mediation. The conditionality attribution (Decision 2)
is preparatory-state output — it lives in the measurement output API and requires the analyst to
read it, which is appropriate for the 20–40 minute preparation window.

---

## 6. Out of Scope

- **Zone 1D integration of political economy composite score** — Decision 4 explicitly defers
  this to a follow-on ADR. The composite score is available in the API but NOT rendered in Zone 1D.
- **Frontend visualization of conditionality term breakdown** — the attribution is available in
  the measurement output API for programmatic access; a visualization component is not in scope
  for this implementation.
- **Political economy as a fifth Zone 1D row** — explicitly deferred per ADR-013 Decision 4.
- **Country-specific calibration** — all estimates remain Tier 3 (formula-based). Full
  backtesting calibration is tracked in Issue #44.

---

## 7. Test Authorship Obligation

**QA Lead:** QA Lead Agent
**Test authorship deadline:** Before implementation PR is opened
**Test file location:** `backend/tests/unit/test_g6_political_economy_integration.py`
**Relevant ADR acceptance criteria:** AC-1 through AC-6 above

**QA Lead acknowledgment:**
`[x]` QA Lead: Tests for AC-1 through AC-6 authored and filed. [2026-06-12]

---

*Intent document version: 2026-06-12. Phase A encoded. Implements ADR-013 G6 Wave 2.*
*Calibration-basis.md political economy section must be present before implementation PR opens.*
