---
name: M19-G2D-capital-controls-transmission-channels
type: implementation-intent
adr: ADR-020 §Decision 2 (Channels A/B/C) — capital controls economic transmission
issues: "#1532"
status: Filed
authored-by: PM Agent
authored-date: 2026-07-03
implementing-agent: Computation Engine Agent
sprint-entry: docs/process/sprint-plans/m19-g2d-sprint-entry.md
---

# Implementation Intent: G2D — Capital Controls Transmission Channels (#1532)

## 1. Source Issue and Architecture Authority

**Issue:** #1532 — fix(engine): capital controls economic transmission gap — ExternalSectorModule
reserve protection, MacroeconomicModule credit contraction, DemographicModule dead subscription
**ADR prerequisite:** ADR-020 (ARCH-014) §Decision 2 — ACCEPTED 2026-07-03.
**Authored by:** PM Agent
**Date:** 2026-07-03
**Implementing agent:** Computation Engine Agent

**Architecture authority:**
This deliverable implements three module-level handler changes in the simulation engine,
closing the transmission gap documented in ADR-020 §Context:

**Deliverable A — ExternalSectorModule Channel A (reserve protection):**
Subscribe `ExternalSectorModule` to `emergency_policy_capital_controls`. On receipt: reduce
`capital_account_outflow_velocity` by factor `ε` (default 0.60; ISL heterodox fixture: 0.50
per `calibration-basis.md §Capital Controls`). Downstream effect: `reserve_coverage_months`
increases relative to no-controls trajectory. Effect persists for `duration_periods` steps;
partial hysteresis on expiry (velocity reverts at 0.3× original outflow rate).

**Deliverable B — MacroeconomicModule Channel B (credit contraction + bridge event):**
Subscribe `MacroeconomicModule` to `emergency_policy_capital_controls`. On receipt: apply
credit tightening `Δcredit_growth = −β × controls_severity × implementation_capacity`
(β=0.020; γ=1.2; `γ IS A CM-SUPPLIED CONSTANT — CE cannot change γ without CM Consulted
review`). Downstream: `gdp_growth` reduced by `γ × Δcredit_growth`; `fdi_stock_pct_gdp`
step-down by `−δ × controls_severity` (δ ∈ [0.005, 0.015]). **Channel B must emit a
`credit_contraction_labour_shock` secondary event** after applying the credit contraction
— this is the bridge that activates Channel C.

**Deliverable C — DemographicModule Channel C (dead subscription fix + bridge activation):**
Current: DemographicModule subscribes to `"capital_controls_imposition"` — a string never
emitted by the input processor (NM-090 / ADR-020 §Decision 3). Fix:
1. Remove `"capital_controls_imposition"` from `_SUBSCRIBED_EVENTS`
2. Add `"credit_contraction_labour_shock"` to `_SUBSCRIBED_EVENTS`
3. Add elasticity row: `"credit_contraction_labour_shock"` → `q1_poverty_headcount_ratio`;
   `φ ∈ [0.3, 0.7]` (ISL context: φ=0.30 per `calibration-basis.md §Capital Controls §φ`)

**Channel C design note (CE audit clarification):**
ADR-020 Decision 2 Channel C text is ambiguous on the subscription string. The CE audit
(PR #1626, transmission-table rewrite) resolved this: DemographicModule subscribes to the
`credit_contraction_labour_shock` BRIDGE EVENT (emitted by MacroeconomicModule in Channel B),
NOT directly to `emergency_policy_capital_controls`. This design decouples the distributional
module from policy event names — it responds to the economic effect (labour shock from credit
contraction) rather than the policy instrument. The transmission table §capital_controls row
is the canonical implementation target. `emergency_policy_capital_controls` is NOT added
to DemographicModule `_SUBSCRIBED_EVENTS`.

**Deliverable D — known_limitations auto-emission update (ADR-020 §Decision 4):**
After this PR merges, scenarios advancing with `CAPITAL_CONTROLS` at any step must emit the
"channels active" `known_limitations` text (per ADR-020 Decision 4) — not the
"transmission incomplete" text. The text change must be made in whatever module or utility
generates the `known_limitations` block for the capital controls instrument. The G2C runs
already on `sprint/m19-g2` are not retroactively updated; this applies only to new scenario
advances after this PR lands.

**Out-of-scope boundary (GovernanceModule):**
GovernanceModule does NOT subscribe to `emergency_policy_capital_controls` in this PR —
its `_SUBSCRIBED_EVENTS` only contains 4 entries (see CE audit PR #1626 GovernanceModule
section). Adding political legitimacy erosion for capital controls is a future deliverable.
This intent document explicitly excludes it.

---

## 2. Persona Trace Elements Targeted

**P-1 — Persona served:**
Primary: Persona 2 — Finance Ministry Analyst (Eleni archetype; analytical preparation mode).
She applies `EmergencyPolicyInput(CAPITAL_CONTROLS)` at Step 1 of an ISL scenario in Mode 1
(replay) and expects to see the three economically documented channels active in the trajectory.
Secondary: Persona 5 — Institutional Observer (Aicha; Demo 8 Act 2) — sees the Iceland
heterodox run produce a reserve recovery trajectory, validating the "two-path" Demo 8 claim.

**P-2 — Entry state:**
ISL scenario loaded with October 2008 baseline attributes (Step 0). Step 1: analyst applies
`EmergencyPolicyInput(instrument=EmergencyInstrument.CAPITAL_CONTROLS, severity=0.85,
duration_periods=8, implementation_capacity=0.75)`. After advancing to Step 2, she reads the
Zone 1A trajectory. Prior to this fix, all three channels are silent.

**P-3 — Journey step:**
Mode 1 replay — analytical preparation. Analyst is reading the `reserve_coverage_months`,
`gdp_growth`, and `q1_poverty_headcount_ratio` trajectories after applying capital controls
at Step 1. The economic case for Iceland's heterodox path turns on whether the reserve
protection mechanism is visible. Prior to this fix, it is not.

**P-4 — Time/interaction ceiling:**
Analytical preparation mode — no 90-second ceiling. The analyst is deliberate; she will read
multiple indicators and cross-reference with `known_limitations`. Channel correctness is the
primary constraint, not response speed.

**P-6 — Negotiating leverage delivered:**
After this fix, the analyst's trajectory output shows: (a) `reserve_coverage_months` increasing
after Step 1 — reserve protection confirmed; (b) `gdp_growth` deteriorating at Step 2 — credit
contraction cost visible; (c) `q1_poverty_headcount_ratio` rising at Step 2 — human cost of
credit contraction honest and visible. The `known_limitations` no longer says "reserve
protection channel absent" — it says "channels active; Q2 PHC and bilateral creditor
composition not modeled." This is defensible language in a programme review context.

**P-7 — North star capability delivered:**
When the Iceland G2D fixture is run and a ministry analyst asks "does the model show that
capital controls actually protected reserves?" — the answer is now yes, with a documented
calibration anchor (Iceland 2008, ε=0.50 controls-only per IMF Article IV decomposition).
The trajectory is no longer misleading. The `known_limitations` is honest about what is
NOT modeled (Q2 PHC; bilateral creditor composition) rather than flagging that the primary
channel is absent. The heterodox path is now analytically distinguishable from the no-controls
case in the engine output — which is the condition required for Demo 8 Act 2.

---

## 3. Observable Application State

### 3.1 Deliverable A — Channel A (ExternalSectorModule)

In a unit test using a mock event bus:

```python
# Arrange: ExternalSectorModule in initial state
# initial capital_account_outflow_velocity = V0
# ε = 0.60 (default); controls_severity = 0.85; implementation_capacity = 0.75

# Act: emit emergency_policy_capital_controls
esm_handler.handle_event("emergency_policy_capital_controls", {
    "severity": 0.85,
    "implementation_capacity": 0.75,
    "duration_periods": 8,
    "epsilon": 0.60
})

# Assert:
# capital_account_outflow_velocity after handler = V0 × (1 − 0.60 × 0.85 × 0.75)
# reserve_coverage_months at step+1 > reserve_coverage_months at step (no-controls baseline)
```

**Observable:** `capital_account_outflow_velocity` is reduced. The downstream `reserve_coverage_months`
value at step+1 is strictly higher than it would be without capital controls applied.

### 3.2 Deliverable B — Channel B (MacroeconomicModule, including bridge event)

In a unit test using a mock event bus:

```python
# Arrange: MacroeconomicModule subscribed to emergency_policy_capital_controls
# β = 0.020; γ = 1.2 (CM constant, not configurable by CE)

# Act: emit emergency_policy_capital_controls
mm_handler.handle_event("emergency_policy_capital_controls", {
    "severity": 0.85,
    "implementation_capacity": 0.75
})

# Assert:
# Δcredit_growth = -β × 0.85 × 0.75 = -0.020 × 0.85 × 0.75 = -0.01275
# gdp_growth delta = γ × Δcredit_growth = 1.2 × (-0.01275) = -0.0153 (approx)
# AND: event bus received "credit_contraction_labour_shock" event from this handler
```

**Observable:** `gdp_growth` decreases and `credit_contraction_labour_shock` is emitted on
the bus. Both must be true for Channel B to be complete. A handler that produces `gdp_growth`
impact but does NOT emit the bridge event silently breaks Channel C.

**γ constraint observable:** If a test patches γ to any value other than 1.2, the test must
fail (γ is a constant from the CM-supplied calibration; the CE implementation must not accept
γ as a configurable parameter without CM Consulted review).

### 3.3 Deliverable C — Channel C (DemographicModule dead subscription fix)

In a unit test inspecting `_SUBSCRIBED_EVENTS` and elasticity registry:

```python
# Assert subscription cleanup:
assert "capital_controls_imposition" not in DemographicModule._SUBSCRIBED_EVENTS
assert "credit_contraction_labour_shock" in DemographicModule._SUBSCRIBED_EVENTS

# Assert elasticity row:
from backend.app.simulation.modules.demographic.elasticities import ELASTICITY_REGISTRY
assert "credit_contraction_labour_shock" in ELASTICITY_REGISTRY
assert "q1_poverty_headcount_ratio" in ELASTICITY_REGISTRY["credit_contraction_labour_shock"]

# Assert handler fires:
dm_handler.handle_event("credit_contraction_labour_shock", {"delta_credit_growth": -0.01275})
# q1_poverty_headcount_ratio after handler > baseline (φ = 0.30 for ISL context)
```

### 3.4 Deliverable D — known_limitations text update

```python
# After advancing a scenario step with CAPITAL_CONTROLS:
response = GET /api/v1/scenarios/{id}/trajectory
known_lims = response.json()["known_limitations"]
assert "transmission incomplete" not in known_lims  # old text absent
assert "Channel A" in known_lims or "reserve protection" in known_lims  # new text present
assert "Q2 poverty headcount not separately modeled" in known_lims  # Q2 gap disclosed
```

### 3.5 Silent failure detection

**SF-1 (Channel A not firing):** `reserve_coverage_months` flat or declining despite capital
controls applied. Detection: assert `reserve_at_step_2 > reserve_at_step_1` in any scenario
where `CAPITAL_CONTROLS` fires at Step 1 with positive `severity` and `implementation_capacity`.

**SF-2 (Channel B fires but bridge not emitted):** `gdp_growth` decreases but
`credit_contraction_labour_shock` never reaches the bus. Channel C remains silently broken
even though Channel B appears to work. Detection: assert event bus captured
`"credit_contraction_labour_shock"` after `emergency_policy_capital_controls` fires.

**SF-3 (Channel C subscription added but elasticity row missing):** `_SUBSCRIBED_EVENTS`
contains `"credit_contraction_labour_shock"` but the elasticity registry has no row for it.
Handler fires, receives the event, applies zero effect (returns `Δq1 = 0` silently). Detection:
assert `ELASTICITY_REGISTRY["credit_contraction_labour_shock"]["q1_poverty_headcount_ratio"]`
is non-zero and within [0.3, 0.7].

**SF-4 (old subscription string not removed):** `"capital_controls_imposition"` remains in
`_SUBSCRIBED_EVENTS` alongside the corrected `"credit_contraction_labour_shock"`. The dead
string produces no effect (never emitted) but leaves NM-090 open. Detection: assert
`"capital_controls_imposition" not in DemographicModule._SUBSCRIBED_EVENTS`.

**SF-5 (Channel C not subscribed to bridge; subscribed directly to capital_controls):**
DemographicModule subscribes to `"emergency_policy_capital_controls"` instead of
`"credit_contraction_labour_shock"`. This would bypass the credit contraction mechanism
and apply φ unconditionally on policy imposition rather than on the labour market effect.
Detection: assert `"emergency_policy_capital_controls" not in DemographicModule._SUBSCRIBED_EVENTS`
(DM must NOT subscribe to the capital controls event directly — it subscribes to the bridge).

---

## 4. Acceptance Criteria

**AC-1 (Channel A — subscription and outflow velocity reduction):**
`ExternalSectorModule._SUBSCRIBED_EVENTS` contains `"emergency_policy_capital_controls"`.
When the handler fires with `severity=0.85, implementation_capacity=0.75, epsilon=0.60`,
`capital_account_outflow_velocity` is reduced by `ε × severity × implementation_capacity`
factor (= 0.60 × 0.85 × 0.75 = 0.3825; velocity = V0 × (1 − 0.3825)).

**AC-2 (Channel A — reserve_coverage_months increases):**
In a scenario where `CAPITAL_CONTROLS` fires at Step 1 with positive severity and capacity:
`reserve_coverage_months` at Step 2 is strictly greater than at Step 1 (outflow reduction
produces reserve recovery). This is the Type A backtesting assertion for Iceland G2D.

**AC-3 (Channel B — credit contraction applied):**
`MacroeconomicModule._SUBSCRIBED_EVENTS` contains `"emergency_policy_capital_controls"`.
When the handler fires with `severity=0.85, implementation_capacity=0.75, beta=0.020,
gamma=1.2`, `domestic_credit_growth` decreases by `β × severity × capacity = 0.01275` and
`gdp_growth` decreases by `γ × Δcredit_growth = 0.0153` (approximately).

**AC-4 (Channel B — bridge event emitted):**
After `MacroeconomicModule` handles `"emergency_policy_capital_controls"`, the event bus
receives a `"credit_contraction_labour_shock"` event. The bridge event payload must include
the `delta_credit_growth` value so DemographicModule can apply φ correctly.

**AC-5 (Channel C — dead subscription removed):**
`"capital_controls_imposition"` is NOT present in `DemographicModule._SUBSCRIBED_EVENTS`.
(Guards SF-4.)

**AC-6 (Channel C — bridge subscription added and elasticity row present):**
`"credit_contraction_labour_shock"` IS present in `DemographicModule._SUBSCRIBED_EVENTS`.
`ELASTICITY_REGISTRY["credit_contraction_labour_shock"]["q1_poverty_headcount_ratio"]` exists
and has a value in [0.3, 0.7].

**AC-7 (Channel C — PHC increases after bridge event):**
When DemographicModule handles `"credit_contraction_labour_shock"` with a negative
`delta_credit_growth`, `q1_poverty_headcount_ratio` increases relative to baseline.

**AC-8 (Channel C — DM does NOT directly subscribe to capital_controls event):**
`"emergency_policy_capital_controls"` is NOT present in `DemographicModule._SUBSCRIBED_EVENTS`.
(Guards SF-5 — enforces bridge design.)

**AC-9 (γ constant protection):**
The `γ` multiplier (GDP-credit multiplier) used in Channel B is hard-coded or config-constant
at 1.2. No CE-authored parameter or config key allows CE to override γ without going through
CM Consulted review. A test that inspects the handler confirms `gamma == 1.2` and does not
accept a caller-supplied override.

**AC-10 (known_limitations text — channels active):**
A scenario advanced with `CAPITAL_CONTROLS` after this PR merges to `sprint/m19-g2` returns
`known_limitations` containing "reserve protection" (or equivalent Channel A language) and
"Q2 poverty headcount not separately modeled" — NOT the pre-ADR-020 "transmission incomplete
(#1532)" text.

**AC-11 (runtime validation — no SimulationError for capital_controls):**
`EmergencyPolicyInput(instrument=EmergencyInstrument.CAPITAL_CONTROLS, ...)` does not raise
`SimulationError` when processed. The event string `"emergency_policy_capital_controls"` is
in the runtime-validated canonical registry. (Guards against the pre-ADR-020 state where the
handler was absent and an unregistered-string error could fire.)

---

## 4b. Visual Spec

N/A — this deliverable is backend-only. No frontend changes. Observable application state
is verified via unit tests (AC-1 through AC-11) and integration-validated by the Iceland G2D
fixture (`test_m19_g2d_iceland_scenario_runs.py`, separate QA obligation on #1553).

---

## 5. Kryptonite Constraint Check

**Does this implementation require specialist mediation for Persona 2 to act on the result
in a 90-second ceiling?**

`[x]` No — not applicable. These are engine-internal changes; the observable state is
numeric trajectory output (`reserve_coverage_months`, `gdp_growth`, `q1_poverty_headcount_ratio`)
on existing Zone 1A display surfaces. No UX mediation required.

**Engine kryptonite (silent correctness failure):** The dangerous failure mode is a scenario
where all three channel handlers appear to execute (no exception raised, no SimulationError)
but the numeric effect is zero because of a misconfigured elasticity row, a wrong sign, or
an ε=1.0 default. AC-2, AC-7, and AC-3 assert numeric direction explicitly — passing exit
code alone is insufficient.

**Bridge kryptonite (SF-2 / SF-5):** Channel C will silently fail if either:
(a) Channel B does not emit `credit_contraction_labour_shock` — DM never receives the signal
(b) DM subscribes to `emergency_policy_capital_controls` directly instead of the bridge event

Both failure modes produce a scenario where Channels A and B appear to work but Channel C
is dead. The G2D fixture (AC-5 in #1553's intent) validates the end-to-end path; but the
unit tests here (AC-4, AC-6, AC-8) must detect these failures before the fixture is run.

---

## 6. Out of Scope

- **GovernanceModule capital_controls channel:** GovernanceModule does not subscribe to
  `emergency_policy_capital_controls`. Adding political legitimacy erosion for capital controls
  is a future deliverable — not in G2D. The transmission table explicitly marks this as
  "❌ not subscribed" (not a gap — an intentional deferral).
- **DM dead subscription cleanup for `imf_program_acceptance` and `emergency_declaration`:**
  NM-090 documents these two additional dead strings. Per ADR-020 §Decision 3 scope, they
  are NOT fixed in this PR. Fixing the strings without adding elasticity rows would produce no
  runtime behavior change; adding elasticity rows requires a separate CM advisory. These are
  a separate PR after CM review.
- **Hysteresis implementation (post-expiry):** ADR-020 Decision 2 Channel A specifies a 0.3×
  partial hysteresis factor on capital account reopening. This is noted in the ADR but is not
  a G2D acceptance criterion. If time allows, implement it; if not, document in known_limitations.
- **FDI step-down (δ parameter):** ADR-020 Decision 2 Channel B includes `fdi_stock_pct_gdp`
  step-down at `−δ × controls_severity`. Not a G2D acceptance criterion — implement if time
  allows alongside Channel B; exclude if needed to reduce scope.
- **asset_nationalization enum extension:** NM-091 documents that `asset_nationalization` has
  no matching `EmergencyInstrument` enum value (code has `NATIONALIZATION`). Do NOT create
  new enum values in this PR without EL approval. The fixture intent §3.2 references
  `instrument="asset_nationalization"` — that must be corrected to
  `EmergencyInstrument.NATIONALIZATION` in the implementing agent's fixture code.
- **Iceland entity seeding and G2D fixture code:** Covered by the separate intent document
  for #1553 (`M19-G2D-2026-07-03-iceland-2008-backtesting-fixture.md`). This intent covers
  only the engine module changes (#1532).

---

## 7. Test Authorship Obligation

**QA Lead:** QA Lead Agent (in-channel — CE Agent authors unit tests; QA Lead reviews before
implementation PR opens)
**Test authorship deadline:** Before any G2D implementation PR opens on `sprint/m19-g2`
**Test file location:** `backend/tests/unit/test_adr020_capital_controls_transmission.py`

**Test classification:** Unit tests (no `@pytest.mark.backtesting`; no `DATABASE_URL` required).
Use mock event bus and module instances in isolation. The Iceland G2D fixture scenario run
(`backend/tests/test_m19_g2d_iceland_scenario_runs.py`) provides the integration-level
end-to-end validation; these unit tests must validate each channel in isolation before the
fixture runs.

**Required test coverage:**

- **AC-1:** Instantiate ESM with mock bus; emit `emergency_policy_capital_controls`; assert
  `capital_account_outflow_velocity` is reduced by the correct ε factor.
- **AC-2:** Compute `reserve_coverage_months` at step+1 with controls active vs. no-controls;
  assert `reserve_with_controls > reserve_without_controls`.
- **AC-3:** Instantiate MM with mock bus; emit `emergency_policy_capital_controls`; assert
  `domestic_credit_growth` and `gdp_growth` decrease by expected amounts (β=0.020, γ=1.2).
- **AC-4:** After AC-3 handler fires, assert mock bus captured `"credit_contraction_labour_shock"`
  with non-zero `delta_credit_growth` payload. Write as a SEPARATE assertion block from AC-3
  so bridge failure is visible independently.
- **AC-5:** Assert `"capital_controls_imposition" not in DemographicModule._SUBSCRIBED_EVENTS`.
- **AC-6:** Assert `"credit_contraction_labour_shock" in DemographicModule._SUBSCRIBED_EVENTS`
  AND `ELASTICITY_REGISTRY["credit_contraction_labour_shock"]["q1_poverty_headcount_ratio"]`
  is in [0.3, 0.7].
- **AC-7:** Instantiate DM; emit `credit_contraction_labour_shock` with negative
  `delta_credit_growth`; assert `q1_poverty_headcount_ratio` increases.
- **AC-8:** Assert `"emergency_policy_capital_controls" not in DemographicModule._SUBSCRIBED_EVENTS`.
  (Bridge design guard — DM must NOT directly subscribe to the policy event.)
- **AC-9:** Assert the γ value in the MM handler is 1.2 and is not overridable via a caller
  parameter (inspect handler source or config constant).
- **AC-10:** Call the known_limitations generator for `CAPITAL_CONTROLS` after the channels
  are active; assert output contains "reserve protection" and "Q2 poverty headcount" and does
  NOT contain "#1532".
- **AC-11:** Assert `EmergencyPolicyInput(instrument=EmergencyInstrument.CAPITAL_CONTROLS,
  severity=0.85, duration_periods=8, implementation_capacity=0.75)` processes without raising
  `SimulationError`.
- **AC-9 regression:** Verify `ELASTICITY_REGISTRY["gdp_growth_change"]` is unchanged (Channel
  C fix must not accidentally alter existing DM elasticity rows).

**QA Lead acknowledgment:**
`[x]` QA Lead: Tests for AC-1 through AC-11 authored and filed at
`backend/tests/unit/test_adr020_capital_controls_transmission.py`. [2026-07-03]
`[x]` QA Lead: Bridge event payload schema verified — `credit_contraction_labour_shock` carries
a single affected_attribute with negative magnitude (delta_credit_growth); DM handler tests
authored against this confirmed structure. [2026-07-03]
`[x]` QA Lead: `"capital_controls_imposition"` confirmed PRESENT in DM `_SUBSCRIBED_EVENTS`
by direct inspection of `backend/app/simulation/modules/demographic/module.py:32-37` —
confirming this is the live bug that AC-5 tests detect (test currently FAILS, will PASS after fix).
[2026-07-03]
`[x]` QA Lead: Test run baseline confirmed — 19 FAILED (target-state tests; expected before
implementation) / 9 PASSED (pre-existing correct behaviors). No import or syntax errors. [2026-07-03]

---

*Intent document version: 2026-07-03. ADR prerequisite: ADR-020 (ARCH-014) accepted 2026-07-03.
Pre-implementation gates: CM (PR #1625 ✓) and CE audit (PR #1626 ✓) both CLEARED 2026-07-03.
Sprint entry: `docs/process/sprint-plans/m19-g2d-sprint-entry.md` (EL-approved 2026-07-03).
See `docs/process/agent-execution-lifecycle.md` for the five-step lifecycle this document gates.*
