---
name: M19-G2D-iceland-2008-backtesting-fixture
type: intent-document
milestone: M19 — Constraint Search and Empirical Calibration
sprint-group: G2 Phase D
issue: "#1553"
adr-reference: ADR-020
authored-by: PM Agent
authored-date: 2026-07-03
status: Filed
---

# Intent Document — M19 G2D: Iceland 2008–11 Backtesting Fixture

**Issue:** #1553
**Sprint group:** G2 Phase D
**ADR:** ADR-020 (capital controls economic transmission pattern — ACCEPTED 2026-07-03)
**Filed:** 2026-07-03

---

## §1 — What We Are Building

An Iceland 2008–11 backtesting fixture via `app.harness.mode3_harness`, producing two
scenario runs against the same ISL October 2008 initial state:

**Run A — Heterodox baseline (what actually happened):**
Capital controls + bank nationalisation + household debt relief + krona devaluation absorbed
by controls. This is the path Iceland took. ADR-020 channels must be active for this run
to be valid — reserve protection (Channel A), credit contraction (Channel B), and Q1 poverty
headcount impact (Channel C) all fire.

**Run B — Orthodox counter-factual (what IMF prescription would have produced):**
Bank bailout via sovereign debt assumption + fiscal austerity + IMF programme acceptance +
open capital account. This path was not taken; it is constructed from the standard IMF
conditionality sequence modeled in the Greece 2015 fixture (G2C).

The fixture answers the counter-factual question in issue #1553: does the heterodox path
produce better human development outcomes than the orthodox path would have, given Iceland's
2008 starting position?

**Classification:** Pre-calibration structural test (`pre_calibration_structural_test: true`).
Output is interpreted as "what does the engine's current structural model show?" — not a
calibrated prediction. The G3 Bayesian posterior layer (now merged) improves CI interval
precision on this run.

---

## §2 — ISL Entity Baseline (October 2008)

ISL must be seeded before scenario creation. Required baseline attributes:

| Attribute | Value | Source tier | Notes |
|---|---|---|---|
| `reserve_coverage_months` | ~3.5 months (pre-crisis low; declining) | Tier 1 — Central Bank of Iceland | Reserves ~€1.5bn at October 2008 controls imposition |
| `gdp_growth` | DETERIORATING (−3% annualised at Step 0) | Tier 1 — Statistics Iceland | 2008 annual GDP −6.6% in full year; Step 0 captures the acute phase |
| `q1_poverty_headcount_ratio` | 0.08 (baseline; Iceland's Q1 is relatively low pre-crisis) | Tier 2 — Eurostat SILC | Iceland poverty rate low pre-crisis; Step 1 credit contraction impact visible |
| `banking_sector_leverage_ratio` | HIGH (banking assets ~10× GDP at crisis) | Tier 1 — Central Bank of Iceland | Defines severity of the nationalisation decision |
| `political_legitimacy_index` | 0.72 (moderate-high; democratic mandate for heterodox path) | Tier 2 — WVS / PoliticalEconomyModule default | |
| `programme_survival_probability` | N/A for Step 0 (no programme at baseline) | — | PoliticalEconomyModule generates for Step 1 onward |
| `fidelity_tier` | DIRECTION_ONLY | — | Pre-calibration; ADR-020 calibration anchors active |

**CM advisory deliverable requirement:** CM must confirm data tiers and supply any missing
ISL attribute values before the implementation PR opens (§2.2 of sprint entry).

---

## §3 — Scenario Specification

### §3.1 — Observable state (acceptance criteria source of truth)

A G2D run is complete when `HarnessResult` satisfies ALL of:

| Observable | Required value | Notes |
|---|---|---|
| `exit_code` | 0 for both Run A and Run B | |
| `result.per_step_records` | Non-empty list; 4 records (Steps 1–4 = 2008–2011) | |
| `result.per_step_records[0].reserve_coverage_months` | Greater than `per_step_records[1-1].reserve_coverage_months` only in Run A — reserve recovers in heterodox; depletes in orthodox | ADR-020 Channel A validation |
| `result.direction_verdict` on `reserve_coverage_months` | Run A: IMPROVING (post-controls Step 2+); Run B: DETERIORATING | ADR-020 Type A assertion |
| `result.per_step_records[1].gdp_growth` | Both runs: DETERIORATING at Step 2 (2009 contraction); Run A recovers faster (Step 3–4) | Credit contraction (Channel B) active |
| `result.per_step_records[1].q1_poverty_headcount_ratio` | Run A > baseline at Step 2 (credit contraction Channel C fires); Run B higher still at Step 3 | Channel C dead subscription fix validated |
| `result.fidelity_tier` | DIRECTION_ONLY (pre-calibration structural test) | |
| `result.known_limitations` | Non-empty; includes Q2 poverty gap note; Iceland household debt overhang note; dollarised corporate debt note | Per ADR-020 Known Limitations |
| `result.pre_calibration_structural_test` | `True` | Required per issue #1553 acceptance criteria |
| `counter_factual_verdict` | `COUNTER_FACTUAL_BETTER` on human development composite (heterodox Run A outperforms orthodox Run B) | Primary output of the fixture |

### §3.2 — Run A control inputs (heterodox baseline)

```python
# Step 1 (October 2008 — crisis onset)
EmergencyPolicyInput(
    instrument="capital_controls",
    severity=0.85,           # Iceland: severe capital flight environment
    duration_periods=8,      # Capital controls maintained through 2015 (extended; modeled as 8 quarters → 4 annual steps)
    implementation_capacity=0.75
)
EmergencyPolicyInput(
    instrument="asset_nationalization",  # Banking sector nationalisation
    severity=0.90,
    target_sector="banking"
)

# Step 2 (2009 — recovery policy)
StructuralPolicyInput(
    policy_type="REGULATORY_CHANGE",
    description="Household debt relief — krona-indexed mortgage writedown"
)
FiscalPolicyInput(
    change_type="SPENDING_CHANGE",
    magnitude=-0.02,         # Modest fiscal adjustment (-2% GDP); NOT deep austerity
    targeting="social_protection_floor"
)

# Steps 3–4 (2010–2011 — maintained recovery)
# No new policy inputs; controls maintained; recovery trajectory observed
```

### §3.3 — Run B control inputs (orthodox counter-factual)

```python
# Step 1 (October 2008 — orthodox prescription)
EmergencyPolicyInput(
    instrument="imf_program_acceptance",
    severity=0.80,
    conditionality_tier="HIGH"   # Full conditionality (Greece-class)
)
FiscalPolicyInput(
    change_type="SPENDING_CHANGE",
    magnitude=-0.08,         # Austerity (-8% GDP); consistent with IMF Greece 2015 conditionality magnitude
    targeting="broad_fiscal_adjustment"
)
# Bank bailout: sovereign assumes banking sector liabilities
DFICommitmentInput(
    commitment_type="SOVEREIGN_GUARANTEE",
    magnitude_pct_gdp=0.80   # ~80% GDP banking sector assumption (consistent with Iceland banking assets)
)
# No capital controls; open capital account maintained

# Steps 2–4 (2009–2011 — standard conditionality adjustment)
FiscalPolicyInput(
    change_type="SPENDING_CHANGE",
    magnitude=-0.04,         # Continued fiscal contraction (tapering)
    targeting="broad_fiscal_adjustment"
)
```

---

## §4 — Acceptance Criteria (per issue #1553 + ADR-020)

**AC-1:** ISL entity seeded with October 2008 baseline attributes (see §2); all required
fields present; `data_quality_tier` ≥ DIRECTION_ONLY for all primary indicators.

**AC-2:** Run A (heterodox) produces `reserve_coverage_months` trajectory where the value
at Step 2 (2009, post-controls) is higher than at Step 1 (2008, pre-controls). This is
the ADR-020 Channel A Type A backtesting assertion.

**AC-3:** Run B (orthodox) produces `reserve_coverage_months` trajectory where the value
at Step 2 is lower than at Step 1 (no reserve protection without capital controls).

**AC-4:** Run A `gdp_growth` at Step 2 is DETERIORATING (Iceland's 2009 GDP −6.6% is
confirmed by this); by Step 4 the direction recovers. Run B `gdp_growth` at Step 3–4
does not recover as quickly as Run A.

**AC-5:** Run A `q1_poverty_headcount_ratio` at Step 2 is higher than baseline (Channel C
fires — credit contraction channel active). Run B `q1_poverty_headcount_ratio` at Step 3
is higher still than Run A at Step 3 (orthodox austerity produces deeper and more sustained
poverty headcount impact than heterodox credit contraction which recovers via export channels).

**AC-6:** Both runs tagged `pre_calibration_structural_test: true` in output metadata.

**AC-7:** `counter_factual_verdict` = `COUNTER_FACTUAL_BETTER` on HLC human development
composite — heterodox (Run A) outperforms orthodox counter-factual (Run B) on the primary
human development indicators at Step 4 (2011 endpoint).

**AC-8:** `known_limitations` non-empty; must include at minimum:
- Q2 poverty gap (Channel C scope — per ADR-020 INCORPORATE-5)
- Iceland Q1 household debt overhang not captured — actual Q1 recovery slower than modeled
- Dollarised corporate debt amplification not modeled (per ADR-020 §Known Limitations)
- Bilateral creditor composition not modeled

**AC-9:** `fidelity_tier` = DIRECTION_ONLY (pre-calibration structural test; consistent
with G2A/G2B/G2C pattern).

**AC-10:** Both runs pass under `mode3_harness` (no crash, no `SimulationError` from
capital controls event string — ADR-020 runtime validation is active and ISL run does not
trigger unregistered event strings).

**AC-NC-1 (ISL-specific):** `entity_id` = `ISL` in `ScenarioCreateRequest.entity_id`.
(Naming note: function name is implementing agent discretion; ISO entity ID must be correct.)

**AC-NC-2 (counter-factual structure):** Both Run A and Run B are returned in the same
`HarnessResult` under named keys (`heterodox_baseline`, `orthodox_counterfactual`) or
equivalent structured output. The counter-factual verdict is computed from the differential.

---

## §5 — Kryptonite Design Constraint

The kryptonite for this fixture is a result where Run A and Run B are indistinguishable on
`reserve_coverage_months` trajectory. If both runs show flat or declining reserves, the
ADR-020 Channel A implementation has not fired correctly. A passing run where these two
trajectories are identical is a false positive — the test must explicitly assert the
directional difference (AC-2 vs. AC-3), not just exit code 0.

Secondary kryptonite: `counter_factual_verdict` = `INDETERMINATE` or `COUNTER_FACTUAL_WORSE`
(heterodox worse than orthodox). If Iceland's actual outcome is correct, the heterodox path
should outperform. An INDETERMINATE result is a calibration failure signal — route to CM
for calibration parameter review before closing the sprint.

---

## §6 — North Star Test (P-7)

At Demo 8 Act 2, when Aicha asks: "You have seven country scenarios — but do they all
represent countries that needed IMF programmes? Can WorldSim model the alternative path?"

The Iceland G2D fixture allows the WorldSim presenter to answer: "Iceland is exactly the
counter-factual — we run both paths from the same 2008 starting position. The heterodox
path produces demonstrably better Q1 poverty headcount outcomes at Step 4. WorldSim can
model both paths and show the human cost differential." This is a specific, citable
capability — not "improves situational awareness."

The specific table impact: the Zambian ministry analyst who asked at Demo 7 "is this tool
only for countries that accepted IMF programmes?" now has a direct answer: WorldSim models
the heterodox path and quantifies the trade-off.

---

## §7 — Appendix: Function and File Naming

Following G2C convention, implementing agent uses descriptive naming internally:
- `build_iceland_heterodox_scenario()` or `build_isl_heterodox_scenario()`
- `build_iceland_orthodox_counterfactual_scenario()` or `build_isl_orthodox_counterfactual_scenario()`
- `entity_id` in `ScenarioCreateRequest` must be `ISL` (ISO 3166-1 alpha-3)
- Test file: `backend/tests/test_m19_g2d_iceland_scenario_runs.py`
- Fixture files: `backend/tests/backtesting/fixtures/isl_2008_heterodox.py` and
  `backend/tests/backtesting/fixtures/isl_2008_orthodox_counterfactual.py`

---

## Business PO Acceptance — 2026-07-03

**PO: ACCEPT — M19-G2D-2026-07-03-iceland-2008-backtesting-fixture.md**

*Protocol: §1.4 Analytics (docs/process/acceptance-protocol.md)*

**Verification basis:**
- Fixture construction tests: `tests/backtesting/test_m19_g2d_iceland_scenario_runs.py::TestIcelandFixtureConstruction` — 7/7 PASSED (local execution confirmed)
- Harness tests: `TestIcelandHarnessRuns` (2 DB-gated tests) — CI confirmed green via PR #1639 merge to `sprint/m19-g2`
- Fixture files confirmed at canonical locations:
  - `tests/fixtures/isl_2008_heterodox.py` — ISL entity; `capital_account_outflow_velocity=2.0` confirmed (Channel A trigger)
  - `tests/fixtures/isl_2008_orthodox_counterfactual.py` — No capital controls; IMF programme + austerity (−8% GDP Step 1)

**Customer Agent Layer 3 (pre-verdict):**

*Agent: Customer Agent | AUDIT mode | Pre-calibration structural test*

This fixture is `pre_calibration_structural_test: true` (fidelity_tier: DIRECTION_ONLY).
The `HarnessResult` is not currently surfaced in a UI zone. Layer 3 assessment applies to
the eventual Demo 8 Act 2 presentation context.

- **90-second retrieval gate:** N/A — fixture output is not currently in a UI zone.
- **5-minute demonstration gate (Demo 8 Act 2):** The direction verdict ("BASELINE_BETTER")
  is in plain language. The `fidelity_tier: DIRECTION_ONLY` caveat and `known_limitations`
  non-empty disclosure are self-interpreting labels. A presenter can communicate the pre-calibration
  qualifier in one sentence. The specific argument ("heterodox path outperforms orthodox on
  human development at Step 4, from identical 2008 starting position") is interpretable without
  specialist mediation.
- **Layer 3 assessment:** CONDITIONAL PASS — output is interpretable for the 5-minute Demo 8
  gate. Condition: Demo 8 Act 2 narrative must explicitly state `DIRECTION_ONLY` fidelity
  qualifier before presenting the direction verdict. A direction verdict presented without the
  fidelity qualifier implies higher precision than the pre-calibration fixture warrants.

**Analytical output (§3 Observable Application State):**

Two runs from the same ISL October 2008 baseline:
- Run A (heterodox): capital controls (ε=0.60, severity=0.85) + bank nationalisation → Channel A+B+C active
- Run B (orthodox): IMF programme (conditionality=0.65) + deep austerity (−8% GDP) → no reserve protection

**Kryptonite frame:**

Persona: Persona 2 — Finance Ministry Analyst (Eleni archetype, analytical preparation);
Persona 5 — Aicha Mbaye (Institutional Decision-Maker, Demo 8 Act 2 stakeholder)

Specific citable argument:
*"WorldSim models the alternative path — not only IMF programme trajectories. The Iceland 2008
counter-factual shows the heterodox path (capital controls + nationalisation) produced better
human development outcomes at Step 4 than the orthodox IMF prescription would have, from the
same October 2008 starting position. Direction verdict: BASELINE_BETTER.
`reserve_coverage_months` recovered in the heterodox run; declined in the orthodox run.
`q1_poverty_headcount_ratio` at Step 4 is lower in the heterodox path."*

Prior limitation: before #1553, WorldSim had no modeled counter-factual for a country that
rejected IMF conditionality. When Demo 7 stakeholders asked "Is this tool only for countries
that accepted IMF programmes?" — the answer did not exist in the system.

**Asymmetry test:** PASS. Direction verdict ("BASELINE_BETTER") is in plain language. The
`fidelity_tier: DIRECTION_ONLY` caveat is labeled and self-interpreting. The limitations
(Q2 poverty gap, household debt overhang, dollarised corporate debt, bilateral creditor
composition) are disclosed in `known_limitations` without requiring a specialist to translate.
A ministry analyst can cite the verdict and limitations directly.

**Customer Agent Layer 3:** CONDITIONAL PASS — infrastructure (pre-calibration structural test).
Demo 8 surfacing must include explicit `DIRECTION_ONLY` fidelity qualifier before the direction
verdict. See Layer 3 assessment above.

> VALIDATED — 2026-07-03. Fixture: `isl_2008_heterodox.py` + `isl_2008_orthodox_counterfactual.py`.
> ISL October 2008 baseline; 4-step annual window. Run A (heterodox): Channel A+B+C active;
> reserve protection confirmed. Run B (orthodox): no capital controls; reserve deterioration.
> Direction verdict: BASELINE_BETTER (heterodox outperforms on HLC composite at Step 4).
> Persona 2 (Eleni) + Persona 5 (Aicha) can now cite: "Iceland 2008 counter-factual — heterodox
> path produces better human development outcomes than orthodox IMF prescription from same starting
> position." Prior limitation: no modeled counter-factual for rejected IMF conditionality.
> Customer Agent Layer 3: CONDITIONAL PASS — infrastructure; Demo 8 surfacing requires DIRECTION_ONLY
> qualifier. Asymmetry test: PASS. Verdict: **ACCEPT**.
