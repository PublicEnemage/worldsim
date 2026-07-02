---
name: M19-G2B-zmb-backtesting-fixture
type: implementation-intent
adr: N/A — fixture is a data file over the existing harness API; no new ADR required
issues: "#1542"
status: Filed
authored-by: PM Agent
authored-date: 2026-07-02
implementing-agent: Computation Engine Agent
sprint-entry: docs/process/sprint-plans/m19-g2b-sprint-entry.md
---

# Implementation Intent: G2 Phase B — ZMB Backtesting Fixture (#1542)

## 1. Source Issue and Architecture Authority

**Issue:** #1542 — feat(backtesting): ZMB (Zambia) backtesting fixture — Type A harness run + CI gate
**ADR prerequisite:** None — confirmed CLEAR in `docs/process/sprint-plans/m19-g2b-sprint-entry.md §4`
**Authored by:** PM Agent
**Date:** 2026-07-02
**Implementing agent:** Computation Engine Agent

**Architecture authority:**
The ZMB fixture calls `run_harness()` from `app.harness.mode3_harness` (G2A, PR #1568)
with a `build_zmb_scenario()` function that constructs a scenario request from historical
Zambia data. The scenario is submitted to the existing `/api/v1/scenarios` endpoint;
the harness calls `POST /scenarios/{id}/advance` and `GET /scenarios/{id}/trajectory`.
No new endpoints, no new engine logic.

**Data sources (all approved; see `docs/data-sources/approved-sources.md`):**
- IMF World Economic Outlook (WEO) — GDP, fiscal balance, current account
- World Bank World Development Indicators (WDI) — poverty headcount, HD indicators
- IMF International Financial Statistics (IFS) — reserves, exchange rate, external debt
- World Bank IDS (International Debt Statistics) — Zambia external debt composition

**Why ZMB is the highest-priority G2B fixture:**
The Demo 7 north star (2026-07-02) is: "Aicha presents Zambia +342K cohort effect with CI
bounds and sourcing to IMF restructuring table." Demo 8 Act 2 must show that the Zambia
CI bounds used in that presentation are empirically grounded. ZMB backtesting evidence is
the direct empirical anchor for that credibility claim. If CI intervals are calibrated from
Bayesian posterior (G3) and the ZMB fixture is the primary calibration input, the ZMB
fidelity tier is load-bearing for Demo 8.

---

## 2. Scenario Specification

**Country:** Zambia (ISO 3166-1 alpha-3: ZMB)
**Scenario window:** 2014–2019 (6 annual steps; step 1 = 2014 initial state)
**Stress characterisation:** Copper price crash 2015–2016 (copper = ~70% of export earnings)
→ fiscal deterioration, foreign reserve drawdown, eurobond issuance at rising spreads,
IMF Staff Monitored Program discussions. Progressive deterioration case: the model should
correctly identify the downward directional trajectory through the full 6-step window.
**Analytical value:** ZMB is the canonical Demo 8 country. It is data-moderate (Tier 2
primary indicators) with strong directional signal. A DIRECTION_ONLY classification on
ZMB 2014–2019 is the minimum acceptable calibration evidence for the Demo 8 CI credibility
claim. A MAGNITUDE_MATCH classification (if data supports it) strengthens the Bayesian
posterior significantly — the Chief Methodologist determines this at pre-merge review.

**Step mapping:**

| Step | Year | Key historical event |
|---|---|---|
| 1 (initial state) | 2014 | Near-peak copper price; eurobond issuance (750M USD); fiscal deficit manageable |
| 2 | 2015 | Copper price crash accelerates; kwacha depreciates 45%; reserve drawdown begins |
| 3 | 2016 | Fiscal deficit peaks (>7% GDP); IMF SMP discussions begin; power shortages compound shock |
| 4 | 2017 | Eurobond 1B USD; deficit reduction attempt; copper partial recovery |
| 5 | 2018 | Debt service pressure rising; IMF Article IV warning on debt trajectory |
| 6 | 2019 | Pre-default trajectory established; spreads widening; IMF programme stalls |

**Primary evaluated indicators (Type A fidelity assessment):**
- `fin_composite` — fiscal balance trajectory (progressive deterioration 2014→2019)
- `gov_composite` — governance/external balance composite (debt-to-GDP rising)
- `psp` — primary scenario probability, should fall across the window

**Focal cohort (required — load-bearing for Demo 8):**
Bottom quintile urban-peri-urban population (Lusaka metro and Copperbelt) — most exposed
to both commodity-linked employment shock and food price inflation via kwacha depreciation.
`monitored_focal_cohorts[0]` pointing to this cohort enables `cohort_poverty_headcount`
tracking. This is the cohort behind the "+342K cohort effect" in Demo 7 north star.
The fixture must configure this cohort — a null `cohort_poverty_headcount` across all
steps is a hard failure (SF-3).

---

## 3. Observable Application State

### 3.1 Primary observable state — fixture function

```python
# backend/tests/fixtures/zmb_scenario.py

def build_zmb_scenario() -> ScenarioRequest:
    """Return a ScenarioRequest for ZMB 2014–2019 backtesting.

    Initial state sourced from:
    - IMF WEO 2014 Zambia data
    - WDI 2014 poverty/HD indicators (copper belt cohort)
    - IMF IFS 2014 reserves/exchange rate/external debt
    - World Bank IDS 2014 debt composition

    All Tier 2 (ESTIMATED_COMPARABLE) for primary fiscal/external indicators.
    Cohort indicators at Tier 3 (INFERRED_STRUCTURAL) — direction only.
    """
    ...
```

The fixture function must be importable as `from tests.fixtures.zmb_scenario import build_zmb_scenario`.
It must return a `ScenarioRequest` with:
- `entity_id = "ZMB"`
- `is_pre_calibration = True` (G2B runs are calibration runs)
- Initial state populated from IMF WEO 2014 and WDI 2014 data
- `monitored_focal_cohorts` configured for bottom-quintile Copperbelt/Lusaka cohort (required)

### 3.2 Silent failure modes

**SF-1 (fixture returns wrong entity_id):** `scenario_req.entity_id != "ZMB"`.
Detection: assert `entity_id == "ZMB"` immediately after calling `build_zmb_scenario()`.

**SF-2 (harness exits with BELOW_THRESHOLD or STRUCTURAL_ONLY):** Fidelity tier below
acceptable floor. ZMB is the Demo 8 primary calibration country — BELOW_THRESHOLD means
the fixture cannot serve as CI calibration evidence. Do not merge; escalate to Engineering Lead.

**SF-3 (null cohort records — Demo 8 load-bearing failure):** All `per_step_records[i]["cohort_poverty_headcount"]`
are null. The Copperbelt/Lusaka bottom-quintile cohort poverty headcount is the "+342K
cohort effect" number that appears in Demo 7 north star. If it is null in the harness
output, the calibration fixture does not support Demo 8's CI credibility narrative.
Detection: assert at least one step record has `cohort_poverty_headcount` that is not null.
This is a hard failure — do not merge if SF-3 fires.

**SF-4 (monotone trajectory not detected):** `fin_composite` values are flat or increasing
across all 6 steps, indicating the copper price shock transmission is not reaching the
fiscal composite. Detection: assert `fin_composite` at step 3 (2016 trough) is strictly
less than `fin_composite` at step 1 (2014 baseline).

---

## 4. Acceptance Criteria

**AC-1 (fixture importable):**
`from tests.fixtures.zmb_scenario import build_zmb_scenario` succeeds without error.

**AC-2 (fixture returns valid ScenarioRequest with correct entity and cohort):**
`build_zmb_scenario()` returns a `ScenarioRequest` with `entity_id == "ZMB"`,
`is_pre_calibration == True`, and `monitored_focal_cohorts` is non-empty (Copperbelt cohort configured).

**AC-3 (scenario creation succeeds):**
`POST /api/v1/scenarios` with the fixture's request returns HTTP 201 and a `scenario_id`.

**AC-4 (Type A harness run completes):**
`run_harness(scenario_id=..., steps=6, run_type=RunType.TYPE_A, ...)` completes without
raising `HarnessValidationError` or `HarnessApiError`; `result.per_step_records` has
length 6.

**AC-5 (fidelity tier at acceptable floor):**
`result.summary["fidelity_tier"]` is one of `{FidelityTier.DIRECTION_ONLY, FidelityTier.MAGNITUDE_MATCH}`.
BELOW_THRESHOLD or STRUCTURAL_ONLY → do not merge; escalate to Chief Methodologist and EL.

**AC-6 (fiscal deterioration direction correct):**
`result.per_step_records[2]["fin_composite"]` (step 3 = 2016 trough) is strictly less than
`result.per_step_records[0]["fin_composite"]` (step 1 = 2014 baseline). This asserts the
copper price crash fiscal transmission is captured in the correct direction.

**AC-7 (cohort headcount non-null — SF-3 guard):**
At least one entry in `result.per_step_records` has `cohort_poverty_headcount` that is not
null. This confirms the Copperbelt/Lusaka cohort is correctly configured and producing output.

**AC-8 (step count matches):**
`len(result.per_step_records) == 6` (SF-1 guard from G2A AC-13).

**AC-9 (known_limitations populated for bilateral weights):**
`result.summary["known_limitations"]` is a list. Since the ZMB scenario exercises
multi-step bilateral trade/debt relationships (copper export links, eurobond creditor
composition), at least one entry should reference Issue #35 or `"bilateral weights frozen"`.
If the control inputs do not activate bilateral relationship tracking, this criterion is
advisory — document the finding in the Chief Methodologist consultation.

**AC-10 (scenario cleanup):**
`DELETE /api/v1/scenarios/{scenario_id}` succeeds after the run.

---

## 5. Chief Methodologist Pre-Merge Requirement

**This fixture may not merge to `sprint/m19-g2` without Chief Methodologist sign-off.**

Per `docs/process/sprint-plans/m19-g2b-sprint-entry.md §2.2`, the Chief Methodologist
must review the ZMB fidelity tier assignment before the ZMB feature PR merges. Given
that ZMB is the Demo 8 primary calibration country, the CM's review is especially
consequential: a MAGNITUDE_MATCH tier on ZMB significantly strengthens the Bayesian
posterior for Demo 8 Act 2; DIRECTION_ONLY is the minimum acceptable but may require
a hedged framing of the CI interval credibility claim at Demo 8.

The implementing agent activates the Chief Methodologist with:

```
Chief Methodologist: VALIDATE — ZMB 2014–2019 Type A backtesting fixture fidelity tier;
Demo 8 Act 2 calibration credibility depends on this assessment
```

providing: the fixture's initial state values and data sources, the harness run output
(JSON format, 6 steps), the observed `fidelity_tier`, and the cohort headcount trajectory.
The CM advises on tier classification and on whether the CI interval credibility claim
in Demo 8 Act 2 should be framed as "grounded in DIRECTION_ONLY fidelity" or "grounded in
MAGNITUDE_MATCH fidelity."

The CM sign-off is recorded as a comment on Issue #1542 before the feature PR is opened.

---

## 6. Out of Scope (ZMB G2B)

- **ZMB counter-factual Type B (default 2020 avoidance)** — G2C scope after Type A CI-gated
- **ZMB cohort poverty headcount magnitude match** — Tier 3 data; direction only
- **Bayesian posterior calibration from ZMB results** — G3 (#1543) scope
- **SEN fixture** — separate deliverable in this sprint (#1541); separate intent document

---

## 7. Test Authorship Obligation

**QA Lead:** QA Lead Agent
**Test authorship deadline:** Before any G2B implementation PR opens
**Test file location:** `backend/tests/backtesting/test_m19_g2b_zmb_fixture.py`

*NM-078 compliance: test file at `backend/tests/backtesting/` — CI-discoverable path.*
*NM-056 compliance: `from tests.fixtures.zmb_scenario import build_zmb_scenario` at top
of test file — ImportError (hard RED) until fixture is implemented.*

**QA Lead acknowledgment:**
`[x]` QA Lead: Tests for AC-1 through AC-10 authored and filed. 2026-07-02
- `backend/tests/backtesting/test_m19_g2b_zmb_fixture.py` — AC-1 through AC-10
  (top-level import of `build_zmb_scenario` fails RED until fixture exists)

---

*Intent document version: 2026-07-02. Sprint entry: `docs/process/sprint-plans/m19-g2b-sprint-entry.md`.*
