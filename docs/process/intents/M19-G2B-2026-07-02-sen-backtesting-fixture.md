---
name: M19-G2B-sen-backtesting-fixture
type: implementation-intent
adr: N/A — fixture is a data file over the existing harness API; no new ADR required
issues: "#1541"
status: Filed
authored-by: PM Agent
authored-date: 2026-07-02
implementing-agent: Computation Engine Agent
sprint-entry: docs/process/sprint-plans/m19-g2b-sprint-entry.md
---

# Implementation Intent: G2 Phase B — SEN Backtesting Fixture (#1541)

## 1. Source Issue and Architecture Authority

**Issue:** #1541 — feat(backtesting): SEN (Senegal) backtesting fixture — Type A harness run + CI gate
**ADR prerequisite:** None — confirmed CLEAR in `docs/process/sprint-plans/m19-g2b-sprint-entry.md §4`
**Authored by:** PM Agent
**Date:** 2026-07-02
**Implementing agent:** Computation Engine Agent

**Architecture authority:**
The SEN fixture calls `run_harness()` from `app.harness.mode3_harness` (G2A, PR #1568)
with a `build_sen_scenario()` function that constructs a scenario request from historical
Senegal data. The scenario is submitted to the existing `/api/v1/scenarios` endpoint;
the harness calls `POST /scenarios/{id}/advance` and `GET /scenarios/{id}/trajectory`.
No new endpoints, no new engine logic.

**Data sources (all approved; see `docs/data-sources/approved-sources.md`):**
- IMF World Economic Outlook (WEO) — GDP, fiscal balance, current account
- World Bank World Development Indicators (WDI) — poverty headcount, HD indicators
- IMF International Financial Statistics (IFS) — reserves, exchange rate
- African Development Bank — Senegal country data for cross-validation

---

## 2. Scenario Specification

**Country:** Senegal (ISO 3166-1 alpha-3: SEN)
**Scenario window:** 2014–2019 (6 annual steps; step 1 = 2014 initial state)
**Stress characterisation:** Commodity price shock 2015–2016 (groundnut/phosphate exports)
followed by fiscal consolidation and strong recovery phase under IMF Article IV surveillance.
**Analytical value:** SEN is a data-moderate case (Tier 2 primary indicators, Tier 3 cohort
data) with a clear directional trajectory — deterioration 2015-16, recovery 2017-19. The
model should correctly identify the direction of primary fiscal and HD indicators even without
magnitude precision, making DIRECTION_ONLY the conservative expected fidelity tier.

**Step mapping:**

| Step | Year | Key historical event |
|---|---|---|
| 1 (initial state) | 2014 | Pre-shock baseline; commodity prices at cycle peak |
| 2 | 2015 | Groundnut/phosphate price shock onset; fiscal deterioration begins |
| 3 | 2016 | Trough year; fiscal deficit peaks; HD indicator stress |
| 4 | 2017 | Recovery onset; IMF Article IV support; fiscal consolidation |
| 5 | 2018 | Recovery accelerates; primary balance improvement |
| 6 | 2019 | Pre-COVID baseline restored; convergence toward balanced position |

**Primary evaluated indicators (Type A fidelity assessment):**
- `fin_composite` — fiscal balance trajectory (deterioration → recovery)
- `hd_composite` — human development composite (poverty headcount sensitivity)
- `psp` — primary scenario probability, should remain above DIRECTION_ONLY floor

**Focal cohort (if configured):**
Bottom quintile rural population — most affected by groundnut price shock and subsistence
agriculture disruption. `monitored_focal_cohorts[0]` pointing to this cohort enables
`cohort_poverty_headcount` tracking in the harness output.

---

## 3. Observable Application State

### 3.1 Primary observable state — fixture function

```python
# backend/tests/fixtures/sen_scenario.py

def build_sen_scenario() -> ScenarioRequest:
    """Return a ScenarioRequest for SEN 2014–2019 backtesting.

    Initial state sourced from:
    - IMF WEO 2014 Senegal data
    - WDI 2014 poverty/HD indicators
    - IMF IFS 2014 reserves/exchange rate

    All Tier 2 (ESTIMATED_COMPARABLE) for primary fiscal indicators.
    HD and cohort indicators at Tier 3 (INFERRED_STRUCTURAL).
    """
    ...
```

The fixture function must be importable as `from tests.fixtures.sen_scenario import build_sen_scenario`.
It must return a `ScenarioRequest` with:
- `entity_id = "SEN"`
- `is_pre_calibration = True` (G2B runs are calibration runs)
- Initial state populated from IMF WEO 2014 and WDI 2014 data
- `monitored_focal_cohorts` configured for bottom-quintile rural cohort

### 3.2 Silent failure modes

**SF-1 (fixture returns wrong entity_id):** `scenario_req.entity_id != "SEN"` after fixture call.
Detection: assert `entity_id == "SEN"` immediately after calling `build_sen_scenario()`.

**SF-2 (harness exits with BELOW_THRESHOLD or STRUCTURAL_ONLY):** Fidelity tier below
acceptable floor, indicating data inputs are too thin to produce even directional signal.
Detection: the QA test fails; Chief Methodologist review is required before the fixture
enters CI. BELOW_THRESHOLD means the fixture is not calibration-useful — do not merge.

**SF-3 (zero cohort records in harness output):** `per_step_records[i]["cohort_poverty_headcount"]`
is null for all steps, indicating focal cohort configuration failed silently.
Detection: if `monitored_focal_cohorts` is configured in the scenario request, at least
one step record must have a non-null `cohort_poverty_headcount`.

---

## 4. Acceptance Criteria

**AC-1 (fixture importable):**
`from tests.fixtures.sen_scenario import build_sen_scenario` succeeds without error.

**AC-2 (fixture returns valid ScenarioRequest):**
`build_sen_scenario()` returns a `ScenarioRequest` with `entity_id == "SEN"` and
`is_pre_calibration == True`.

**AC-3 (scenario creation succeeds):**
`POST /api/v1/scenarios` with the fixture's request returns HTTP 201 and a `scenario_id`.

**AC-4 (Type A harness run completes):**
`run_harness(scenario_id=..., steps=6, run_type=RunType.TYPE_A, ...)` completes without
raising `HarnessValidationError` or `HarnessApiError`; `result.per_step_records` has
length 6.

**AC-5 (fidelity tier at acceptable floor):**
`result.summary["fidelity_tier"]` is one of `{FidelityTier.DIRECTION_ONLY, FidelityTier.MAGNITUDE_MATCH}`.
BELOW_THRESHOLD and STRUCTURAL_ONLY are failures — they indicate the fixture data is
insufficient for calibration purposes. Chief Methodologist review is required if this
criterion fails.

**AC-6 (fin_composite trajectory is directional):**
`result.per_step_records[1]["fin_composite"]` (step 2, shock onset) is less than
`result.per_step_records[0]["fin_composite"]` (step 1, pre-shock baseline), confirming
the model registers the commodity price shock direction correctly on fiscal composite.
Exact magnitude is not asserted — direction only.

**AC-7 (step count matches):**
`len(result.per_step_records) == 6` (SF-1 guard from G2A AC-13).

**AC-8 (known_limitations populated):**
`result.summary["known_limitations"]` is a list (may be empty for SEN if no capital
controls or stock-flow violations are in the control input sequence; if bilateral
relationships are evaluated over multiple steps, Issue #35 must appear).

**AC-9 (scenario cleanup):**
`DELETE /api/v1/scenarios/{scenario_id}` succeeds after the run, so the backtesting
session does not leave orphaned scenarios in the test database.

---

## 5. Chief Methodologist Pre-Merge Requirement

**This fixture may not merge to `sprint/m19-g2` without Chief Methodologist sign-off.**

Per `docs/process/sprint-plans/m19-g2b-sprint-entry.md §2.2`, the Chief Methodologist
must review the fidelity tier assignment before the SEN feature PR merges. The implementing
agent activates the Chief Methodologist with:

```
Chief Methodologist: VALIDATE — SEN 2014–2019 Type A backtesting fixture fidelity tier
```

providing: the fixture's initial state values and data sources, the harness run output
(JSON format, 6 steps), and the observed `fidelity_tier` from the run. The CM signs off
on the tier or requests escalation to MAGNITUDE_MATCH / demotion to STRUCTURAL_ONLY.

The CM sign-off is recorded as a comment on Issue #1541 before the feature PR is opened.

---

## 6. Out of Scope (SEN G2B)

- **SEN counter-factual Type B** — G2C scope after baseline Type A is CI-gated
- **SEN poverty headcount magnitude assertion** — cohort data is Tier 3; direction only
- **Bayesian posterior calibration from SEN results** — G3 (#1543) scope
- **ZMB fixture** — separate deliverable in this sprint (#1542); separate intent document

---

## 7. Test Authorship Obligation

**QA Lead:** QA Lead Agent
**Test authorship deadline:** Before any G2B implementation PR opens
**Test file location:** `backend/tests/backtesting/test_m19_g2b_sen_fixture.py`

*NM-078 compliance: test file at `backend/tests/backtesting/` — CI-discoverable path.*
*NM-056 compliance: `from tests.fixtures.sen_scenario import build_sen_scenario` at top
of test file — ImportError (hard RED) until fixture is implemented.*

**QA Lead acknowledgment:**
`[x]` QA Lead: Tests for AC-1 through AC-9 authored and filed. 2026-07-02
- `backend/tests/backtesting/test_m19_g2b_sen_fixture.py` — AC-1 through AC-9
  (top-level import of `build_sen_scenario` fails RED until fixture exists)

---

*Intent document version: 2026-07-02. Sprint entry: `docs/process/sprint-plans/m19-g2b-sprint-entry.md`.*
