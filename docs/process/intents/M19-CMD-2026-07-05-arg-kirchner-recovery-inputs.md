---
name: M19-CMD-2026-07-05-arg-kirchner-recovery-inputs
type: intent
sprint: M19 CM Sprint D
issue: "#1750"
status: Filed — gates implementation PR
authored-by: Chief Methodologist
authored-date: 2026-07-05
sprint-entry: docs/process/sprint-plans/m19-cm-d-sprint-entry.md
calibration-decision: docs/calibration/m19-cm-d-arg-kirchner-calibration-decision.md
---

# Intent: ARG Baseline Kirchner 2003 Recovery Inputs — CM Sprint D

*Authority: `docs/process/sprint-plans/m19-cm-d-sprint-entry.md §2.3`.
This document closes the §2.3 PENDING gate. Implementation PR may not open until
§2.4 (calibration decision) is also filed.*

---

## 1. What We Are Doing and Why

`build_argentina_scenario()` currently has `n_steps=2`, covering the 2001–02 crisis window.
The CM Sprint B AC-1 test asserts `hd_composite` divergence at step 3 between the
heterodox counter-factual (managed 1999 peg exit) and the orthodox baseline (continued
austerity + default). After the G8 primary_indicator fix, the step-3 baseline trajectory
is absent — `hd_composite=None` for the baseline at step 3 → `per_step_diff[2]=0` → test fails.

The fix is to extend `build_argentina_scenario()` to `n_steps=3` and add Kirchner 2003
recovery inputs at step 3 representing Argentina's actual post-default trajectory.

## 2. Historical Context: Argentina 2003

Argentina's step 3 is calendar year 2003 — the Kirchner recovery:

- **GDP growth:** +8.8% (2003), recovering from -10.9% (2002). Among the fastest
  post-crisis recoveries in EM history. Driven by: peso undervaluation boosting exports,
  export tax revenue enabling social spending, and pent-up domestic demand release.
- **Unemployment:** Peaked at ~21.5% (May 2002). By end-2003, declined to ~14–15%.
  Still elevated relative to pre-crisis (2000: 14.7%) but sharply off the trough.
- **Government fiscal stance:** Kirchner maintained the PJJHD emergency employment
  program and normalised government service delivery. Primary surplus of +0.5% GDP
  in 2003 — revenue-driven (export taxes ~1.5% GDP), with spending normalising upward
  from the 2002 austerity trough. Net fiscal impulse to demand: +2.5–3.5% GDP equivalent
  spending capacity restored relative to the 2002 emergency.

## 3. What Is Being Implemented

**Change 1 — Extend `build_argentina_scenario()` to `n_steps=3`:**
```python
configuration=ScenarioConfigSchema(
    entities=["ARG"],
    n_steps=3,   # was n_steps=2
    ...
)
```

**Change 2 — Add Kirchner 2003 scheduled input at step 3:**
```python
ScheduledInputSchema(
    step=3,
    input_type="FiscalPolicyInput",
    input_data={
        "instrument": "spending_change",
        "target_entity": "ARG",
        "sector": "government",
        "value": "0.030",   # +3.0% GDP — Kirchner social program expansion
        "duration_years": 1,
    },
),
```

Source: MECON Budget Execution 2003 (public) + IMF WEO April 2004.
Confidence tier: T3 (regional inference; direct MECON data available but
mapping to single spending_change parameter requires assumptions).

**Change 3 — Update `test_m19_cm_b_elasticity_calibration.py` bounds:**
Replace [0.003, 0.050] with empirically certified bounds from live harness run.
The bounds are specified in the calibration decision after the empirical run.

## 4. Acceptance Criteria

- **AC-1:** `build_argentina_scenario()` has `n_steps=3`; step 3 has `spending_change=+0.030`
  with `source_registry_id="MECON_BUDGET_2003"` in a fixture comment
- **AC-2:** CM Agent sign-off comment on #1750 (APPROVED verdict) before implementation PR opens
- **AC-3:** Live harness run produces `per_step_diff[2] > 0` — non-zero BL step-3 trajectory
- **AC-4:** `test_m19_cm_b_elasticity_calibration.py` AC-1 test passes with certified bounds
- **AC-5:** `backtesting` CI job green on `release/m19` after integration PR merges
- **AC-6:** #1712 live harness verification confirms `per_step_diff[2] ∈ [lower, upper]`

## 5. Out of Scope

- Adding `net_enrollment_secondary` to the initial ARG attributes (changes all steps; deferred)
- Individual-country calibration for BOL, PER, ECU within the LAC elasticity entries (deferred to M20)
- ARG/ECU currency-crisis-specific elasticity calibration (beyond CM-D scope)
- Modelling peso undervaluation channel directly (export competitiveness is captured implicitly via GDP multiplier)

## 6. Files Modified

| File | Change |
|---|---|
| `backend/tests/fixtures/argentina_2001_2002_scenario.py` | `n_steps=2 → 3`; step-3 `spending_change` added |
| `backend/tests/test_m19_cm_b_elasticity_calibration.py` | AC-1 bounds replaced with CM-certified values |

No API, schema, or frontend changes. No new test files — the existing test is the QA artifact.
