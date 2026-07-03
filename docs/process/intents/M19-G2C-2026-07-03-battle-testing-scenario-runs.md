---
name: M19-G2C-battle-testing-scenario-runs
type: implementation-intent
adr: N/A — scenario runs use the established harness API (G2A, #1546); no new ADR required (see §1)
issues: "#1547, #1548, #1549, #1550, #1551, #1552, #1554"
status: Filed
authored-by: PM Agent
authored-date: 2026-07-03
implementing-agent: Computation Engine Agent
sprint-entry: docs/process/sprint-plans/m19-g2c-sprint-entry.md
---

# Implementation Intent: G2 Phase C — Battle-Testing Scenario Runs

## 1. Source Issues and Architecture Authority

**Issues:**
- #1547 — Greece 2010–15 primary surplus programme counter-factual (Type B)
- #1548 — Argentina 2001 convertibility exit counter-factual (Type B)
- #1549 — Sri Lanka 2022–23 Coffin Corner (Type A+B)
- #1550 — Pakistan 2022–23 IMF programme survival (Type B)
- #1551 — Turkey 2018–19 Backside of Power Curve (Type B)
- #1552 — Egypt 2016 devaluation and subsidy reform (Type B)
- #1554 — Ghana 2022–23 IMF programme (Type A+B)

**ADR prerequisite:** None — confirmed CLEAR in `docs/process/sprint-plans/m19-g2c-sprint-entry.md §4`
**Authored by:** PM Agent
**Date:** 2026-07-03
**Implementing agent:** Computation Engine Agent

**Architecture authority:**

All G2C scenarios run through `run_harness()` from `app.harness.mode3_harness` (G2A, PR #1568, `sprint/m19-g2`). The harness calls existing API endpoints:
- `POST /api/v1/scenarios` — create scenario
- `POST /scenarios/{id}/advance` — advance step
- `GET /scenarios/{id}/trajectory` — retrieve trajectory output

No new endpoints and no new simulation engine logic are introduced by G2C. Each scenario is a fixture function (or pair of functions for Type A+B) that constructs a `ScenarioCreateRequest` from historical data, plus a harness call that produces structured output.

**Existing fixture files reused or extended by G2C:**

| Country | Existing fixture | G2C action |
|---|---|---|
| Greece | `backend/tests/fixtures/greece_2010_scenario.py` — `build_greece_scenario()` (6 steps, 2010–2015 Type A) | Add `build_greece_counterfactual_scenario()` in same file — Type B baseline; see Appendix A |
| Argentina | `backend/tests/fixtures/argentina_2001_2002_scenario.py` — `build_argentina_scenario()` (2 steps, 2001–2002 Type A) | Add `build_argentina_counterfactual_scenario()` in same file — Type B baseline extended to 1999–2002; see Appendix B |
| Sri Lanka | None — new | New `backend/tests/fixtures/lka_scenario.py`; see Appendix C |
| Pakistan | None — new | New `backend/tests/fixtures/pak_scenario.py`; see Appendix D |
| Turkey | None — new | New `backend/tests/fixtures/tur_scenario.py`; see Appendix E |
| Egypt | None — new | New `backend/tests/fixtures/egy_scenario.py`; see Appendix F |
| Ghana | None — new | New `backend/tests/fixtures/gha_scenario.py`; see Appendix G |

**All data sources must be registered in `source_registry` before their data is loaded.**
See `docs/data-sources/approved-sources.md` for the approved source list. Per-country sourcing details and data tier assessments are in each appendix. The Chief Methodologist advisory (sprint entry §2.2) is the gate on data tier determination for all five new-country scenarios before each country's feature PR opens.

---

## 2. Persona Trace Elements

**P-1 — Persona served:**

Primary: Ministry Analyst archetype (Persona 2 analytical preparation mode). The analyst uses G2C battle-testing evidence to answer a creditor challenge: "How do we know this model produces defensible outputs on well-documented historical crises?" She can point to seven cases: two with established Type A fidelity records (Greece, Argentina) now run counter-factually, and five new-country Type A/B runs spanning Sub-Saharan Africa, South Asia, the Middle East, and MENA. Cross-regional coverage is the argument.

Secondary: Business PO and Chief Methodologist — reviewing qualitative output for model fidelity signal and `known_limitations` disclosure accuracy before Demo 8.

Tertiary: Persona 5 (Stakeholder Observer — Aicha, World Bank evaluation team) who may hear "we tested this model against seven sovereign crisis cases" at Demo 8, and may ask which failure modes were correctly identified.

**P-2 — Entry state:**

The ministry analyst has a running WorldSim instance and a scenario configuration built from historical data. She invokes the harness from the command line — the same invocation pattern as G2A:

```
python -m app.harness.mode3_harness \
  --scenario-id <id> \
  --run-type TYPE_B \
  --baseline-scenario-id <baseline_id> \
  --format markdown
```

For Type A+B scenarios (Sri Lanka, Ghana), she runs Type A first (producing a replay of the actual crisis), then Type B using the Type A run as the baseline:

```
# Step 1: Type A (replay)
python -m app.harness.mode3_harness \
  --scenario-id lka_2020_actual \
  --run-type TYPE_A \
  --format json > lka_actual_output.json

# Step 2: Type B (counter-factual, using Type A's scenario as baseline)
python -m app.harness.mode3_harness \
  --scenario-id lka_2020_early_imf \
  --baseline-scenario-id lka_2020_actual \
  --run-type TYPE_B \
  --format markdown
```

**P-3 — Journey reference:**

G2C battle-testing runs do not map to a single user journey step. Their functional role in the Demo 8 arc:

- Demo 8 Act 2 introduction: before showing the Bayesian posterior CI intervals (#1543, G3), the presenter cites battle-testing coverage as the evidence base — "We ran this against seven real-world cases." G2C is the material that makes that sentence defensible.
- Pre-Demo 8 qualitative review: Business PO and Chief Methodologist review harness output for each country to confirm failure mode identification, `known_limitations` disclosure, and directional fidelity before the Demo 8 walkthrough is finalised.

**P-4 — Time/interaction ceiling:**

No real-time ceiling for preparation-mode analyst work. Expected completion windows (equitable build target — free-tier runner, 2-core, 7GB RAM):
- Type A run, 4–6 steps: ≤ 60 seconds
- Type B run (baseline + counter-factual), 4–6 steps each: ≤ 120 seconds total
- Type A+B sequence: ≤ 180 seconds total

If a run exceeds 200 seconds on a free-tier runner, document in `known_limitations` and notify the Chief Methodologist.

**P-5 — Data tier requirement:**

Greece and Argentina: primary fiscal indicators at Tier 2 (ESTIMATED_COMPARABLE) — established by prior Type A backtesting. Extension to counter-factual does not lower the data tier of the baseline; the counter-factual control input sequence may be Tier 3 (INFERRED_STRUCTURAL) for hypothetical policy choices.

New-country scenarios: data tier determined by Chief Methodologist advisory before each country's feature PR opens (sprint entry §2.2). DIRECTION_ONLY is the minimum acceptable fidelity tier for a G2C run to count as battle-testing evidence. BELOW_THRESHOLD or STRUCTURAL_ONLY → do not merge; Chief Methodologist and EL must determine whether the fixture can be respecified or must be deferred.

**P-6 — Calibration evidence delivered:**

By Demo 8, the ministry team can say: "We have tested WorldSim against sovereign crises on four continents, spanning commodity shocks (Zambia, Ghana), convertibility exits (Argentina), austerian tipping points (Greece), emergency IMF programmes (Pakistan, Sri Lanka, Egypt), and currency crises under unorthodox monetary policy (Turkey). On each well-documented case, the model correctly identifies the dominant failure mode direction. The CI bounds in this analysis are calibrated against that empirical record."

This is a qualitative argument from breadth — it does not require MAGNITUDE_MATCH on every case. What it requires is correct failure mode identification across diverse economic structures and crisis types, and honest `known_limitations` disclosure where the model's structural gaps are material.

**P-7 — North star capability delivered:**

At Demo 8 Act 2, when Aicha (World Bank evaluation team) asks: "The CI bounds look reasonable for Zambia — but does the model only work for Sub-Saharan commodity economies? How would it perform on a structurally different crisis?" The ministry team can point to: Greece (European sovereign debt, fiscal multiplier inversion), Argentina (convertibility system collapse), Turkey (currency crisis under monetary policy unorthodoxy), Egypt (devaluation under IMF programme). The model's cross-structural breadth is now a citable fact, not an assertion.

Prior limitation: before G2C, WorldSim's battle-testing evidence was anchored on two countries (SEN, ZMB). A World Bank evaluation team credibly questions whether that is generalizable. After G2C, the question shifts from "is this generalizable?" to "on which structural cases does the model's DIRECTION_ONLY fidelity degrade?" — which is a more productive conversation, and one the `known_limitations` block is designed to answer.

---

## 3. Observable Application State

### 3.1 Common observable state (all seven scenarios)

A successful harness run for any G2C scenario produces:
1. Exit code 0
2. A `HarnessResult` with `per_step_records` of the expected length (per appendix §Step count)
3. `summary.known_limitations` populated with at least the structural gaps relevant to the country's active modules and instruments
4. `summary.fidelity_tier` (Type A and Type A+B): one of `{DIRECTION_ONLY, MAGNITUDE_MATCH, STRUCTURAL_ONLY, BELOW_THRESHOLD}`
5. `summary.direction_verdict` (Type B): one of `{COUNTER_FACTUAL_BETTER, BASELINE_BETTER, INDISTINGUISHABLE}`

### 3.2 Type B observable state

For all seven G2C scenarios (all have a Type B component), the Type B run requires a `baseline_scenario_id` — the scenario created from the existing or new Type A fixture. The Type B scenario uses a modified `ScenarioCreateRequest` reflecting the counter-factual policy path. The harness produces a `direction_verdict` by comparing `primary_indicator` values across baseline and counter-factual trajectories at each step.

**Critical**: for Greece and Argentina where counter-factual control inputs represent a *hypothetical* policy path, the `fidelity_rationale` must explicitly note: "Counter-factual control inputs are Tier 3 (INFERRED_STRUCTURAL) — this represents an analytical hypothesis, not a validated historical path."

### 3.3 Type A+B observable state (Sri Lanka, Ghana)

For Sri Lanka (#1549) and Ghana (#1554), G2C runs:
1. A Type A replay of the actual crisis trajectory (initial state from historical data, control inputs matching actual policies implemented)
2. A Type B counter-factual (initial state same, control inputs modified for the earlier-intervention hypothesis) with the Type A run as baseline

The Type A run establishes fidelity tier for the *actual* crisis path. The Type B direction verdict reflects whether the counter-factual would have produced better primary indicator outcomes than the actual path. Both outputs appear in the test assertions.

### 3.4 Silent failure modes (common to all G2C scenarios)

**SF-C1 (wrong run type in summary):** Type B run produces a `fidelity_tier` field (Type A field) instead of `direction_verdict`. Detection: assert `summary` contains `direction_verdict` for TYPE_B runs, not `fidelity_tier`.

**SF-C2 (INDISTINGUISHABLE verdict on a structurally decisive counter-factual):** A Type B run where the historical record clearly shows the counter-factual path had better outcomes (e.g., earlier peg exit for Argentina) returns `INDISTINGUISHABLE`. Detection: per-country threshold assertions in appendices. For any scenario where `|step_differential_first_significant|` is expected, assert it is not null.

**SF-C3 (capital controls `known_limitations` absent):** Scenarios exercising `EmergencyInstrument.CAPITAL_CONTROLS` (Greece Step 6, Sri Lanka, Egypt) produce an empty `known_limitations` list. Detection: per-country assertion that `known_limitations` contains a capital-controls entry when the instrument is active. See G2A AC-8.

**SF-C4 (fixture constructs wrong entity_id):** `build_xxx_counterfactual_scenario()` returns a `ScenarioCreateRequest` with the wrong `entity_id`. Detection: assert `entity_id` at fixture construction time before any API call.

---

## 4. Acceptance Criteria

### Common structural ACs (all seven scenarios)

**AC-1 (fixture importable — all seven):**
Each of the following imports succeeds without error:
- `from tests.fixtures.greece_2010_scenario import build_greece_counterfactual_scenario`
- `from tests.fixtures.argentina_2001_2002_scenario import build_argentina_counterfactual_scenario`
- `from tests.fixtures.lka_scenario import build_lka_scenario, build_lka_counterfactual_scenario`
- `from tests.fixtures.pak_scenario import build_pak_scenario, build_pak_counterfactual_scenario`
- `from tests.fixtures.tur_scenario import build_tur_scenario, build_tur_counterfactual_scenario`
- `from tests.fixtures.egy_scenario import build_egy_scenario, build_egy_counterfactual_scenario`
- `from tests.fixtures.gha_scenario import build_gha_scenario, build_gha_counterfactual_scenario`

**AC-2 (scenario creation succeeds — all seven):**
`POST /api/v1/scenarios` with each fixture's `ScenarioCreateRequest` returns HTTP 201 and a `scenario_id`. Entity IDs: GRC, ARG, LKA, PAK, TUR, EGY, GHA.

**AC-3 (Type B harness run completes — all seven):**
`run_harness(scenario_id=..., baseline_scenario_id=..., run_type=RunType.TYPE_B, ...)` completes without raising `HarnessValidationError` or `HarnessApiError` for each scenario. `result.per_step_records` length matches the scenario step count (per appendix).

**AC-4 (Type B direction verdict present — all seven):**
`result.summary["direction_verdict"]` is one of `{COUNTER_FACTUAL_BETTER, BASELINE_BETTER, INDISTINGUISHABLE}` for every Type B run. `result.summary["per_step_diff"]` is a list of Decimals of the correct length. AC-4 catches SF-C1.

**AC-5 (known_limitations populated — all seven):**
`result.summary["known_limitations"]` is a non-empty list for every run. The `known_limitations` must contain at least one entry — minimum: the stock-flow accounting gap (#30) which is always active for fiscal composite evaluation.

**AC-6 (Greece existing Type A regression — non-regression):**
`build_greece_scenario()` still produces `fidelity_tier == DIRECTION_ONLY` in a Type A harness run after G2C adds `build_greece_counterfactual_scenario()` to the same file. The existing test `backend/tests/backtesting/test_greece_2010_2012.py` must still pass. Adding to a fixture file must not break the existing fixture function.

**AC-7 (Argentina existing Type A regression — non-regression):**
`build_argentina_scenario()` still produces a valid scenario creation response after G2C adds `build_argentina_counterfactual_scenario()` to the same file. The existing test `backend/tests/backtesting/test_argentina_2001_2002.py` must still pass.

**AC-8 (capital controls known_limitations — Greece Step 6, applicable countries):**
For any scenario that applies `EmergencyInstrument.CAPITAL_CONTROLS` (Greece Step 6; Sri Lanka if applicable; Egypt if applicable), `result.summary["known_limitations"]` contains at least one entry whose text references `"#1532"` or `"CAPITAL_CONTROLS"` or `"Economic transmission absent"`. AC-8 catches SF-C3. See per-country appendix for which scenarios activate capital controls.

**AC-9 (counter-factual Tier 3 disclosure):**
For all Type B runs, `result.summary.get("fidelity_rationale", "")` OR `result.summary["known_limitations"]` contains a string noting that counter-factual control inputs are hypothetical (contains `"hypothetical"` or `"Tier 3"` or `"INFERRED_STRUCTURAL"`). This documents §3.2 transparency obligation.

**AC-10 (scenario cleanup — all seven):**
`DELETE /api/v1/scenarios/{scenario_id}` succeeds (HTTP 204 or 200) for each scenario created during testing.

### Greece-specific ACs (#1547, Appendix A)

**AC-GRE-1 (counter-factual has more gradual fiscal path):**
`build_greece_counterfactual_scenario()` returns a `ScenarioCreateRequest` for GRC with `scheduled_inputs` that apply a smaller fiscal consolidation shock at Step 1 than `build_greece_scenario()`. Specifically: the primary surplus target in the counter-factual control input is no larger than 2.5% of GDP at Step 1 (vs the actual troika target of ~4.5%). Verify at fixture construction, not at harness output.

**AC-GRE-2 (direction verdict — counter-factual expected better on human development):**
For the Type B Greece run, `result.summary["direction_verdict"]` is `COUNTER_FACTUAL_BETTER` when the primary evaluated indicator is `hd_composite` (human development composite — the gradual path is expected to avoid the depth of the Greek unemployment/austerity-driven social deterioration). This is the structural prediction: fiscal multiplier effects mean a gentler primary surplus path should produce less human cost.

If `hd_composite` direction is `INDISTINGUISHABLE` or `BASELINE_BETTER`, this is not a test failure — it is a notable finding. The test should log the actual verdict and the `per_step_diff` values; the test assertion is advisory (record the verdict, do not fail the CI run). See §2.4 note: G2C results are reviewed but not CI-gated; direction assertions are informational.

**AC-GRE-3 (step count — 6 steps, 2010–2015):**
`len(result.per_step_records) == 6` for both Type A baseline and Type B counter-factual runs.

**AC-GRE-4 (capital controls active at Step 6):**
The Type A baseline run (using `build_greece_scenario()`) produces `mda_alert_states` that are non-empty at Step 6 (capital controls step, 26 June 2015). Advisory — record what MDA alerts are active.

**AC-GRE-5 (Coffin Corner failure mode identified):**
The Type A baseline run identifies at least one active failure mode from `{Coffin_Corner, Backside_of_Power_Curve}` in `active_failure_modes` at Step 2 or Step 3 (the period when fiscal consolidation was accelerating debt/GDP). Advisory — record the active failure modes.

### Argentina-specific ACs (#1548, Appendix B)

**AC-ARG-1 (counter-factual extends to earlier window):**
`build_argentina_counterfactual_scenario()` returns a `ScenarioCreateRequest` for ARG with `n_steps >= 3` (allowing representation of the earlier-intervention window starting in 1999–2000, before the convertibility system reached Coffin Corner). The existing `build_argentina_scenario()` has `n_steps=2` (2001–2002 only). The counter-factual begins from an earlier initial state (1999 or 2000 baseline) to allow the counter-factual intervention point to appear within the simulation window.

**AC-ARG-2 (direction verdict — counter-factual expected better on financial composite):**
For the Type B Argentina run, `result.summary["direction_verdict"]` is `COUNTER_FACTUAL_BETTER` when the primary evaluated indicator is `fin_composite` (financial composite — earlier managed devaluation is expected to produce less financial system collapse than the corralito). Advisory, as per AC-GRE-2.

**AC-ARG-3 (step count — 3–4 steps, 1999/2000–2002):**
`len(result.per_step_records) >= 3` for the counter-factual run. The exact step count is determined by the implementing agent based on data availability for the 1999 baseline state — Chief Methodologist advisory not required for Argentina (extends existing fixture), but implementing agent must confirm with the INDEC and IMF WEO sources available at `docs/data-sources/approved-sources.md`.

**AC-ARG-4 (Coffin Corner identified at crisis step):**
The Type A baseline run (using `build_argentina_scenario()`) identifies `Coffin_Corner` in `active_failure_modes` at the default step (Step 2 = 2002). Advisory — record.

**AC-ARG-5 (non-regression — existing Argentina demo variant unaffected):**
`build_argentina_demo_scenario()` (4-step demo variant documented in the fixture file header) continues to import and construct without error after the counter-factual function is added to the same file.

### New-country common ACs (#1549, #1550, #1551, #1552, #1554)

The following ACs apply to all five new-country scenarios. Country-specific direction assertions are in appendices C–G.

**AC-NC-1 (CM advisory on record before PR opens):**
The implementing agent must confirm that the Chief Methodologist advisory comment is present on the corresponding GitHub issue before opening the feature PR for each new-country scenario. This is a process gate, not a software assertion. AC-NC-1 is not a pytest AC — it is a pre-PR-open checklist item enforced by the implementing agent. Failure to check this is a sprint entry §2.2 violation.

**AC-NC-2 (fidelity tier at or above minimum floor for new countries):**
`result.summary["fidelity_tier"]` is one of `{DIRECTION_ONLY, MAGNITUDE_MATCH}` for Type A runs in each new-country scenario. `BELOW_THRESHOLD` or `STRUCTURAL_ONLY` → do not merge; escalate to Chief Methodologist and EL. Advisory for G2C (not a CI-gating assertion) — but log the tier and the rationale in the test output.

**AC-NC-3 (new fixture file importable and returns correct entity_id):**
`build_xxx_scenario()` and `build_xxx_counterfactual_scenario()` for each new country return `ScenarioCreateRequest` with the correct ISO alpha-3 entity_id:
- LKA (Sri Lanka), PAK (Pakistan), TUR (Turkey), EGY (Egypt), GHA (Ghana)

---

## 5. Kryptonite Constraint Check

**Does this implementation's primary observable state require specialist mediation for the intended user to act on it within their operational context?**

`[x]` Partial — same boundary as G2A (see below).

**Rationale:** G2C battle-testing outputs are designed for the Ministry Analyst archetype (Persona 2, analytical preparation mode). The outputs — harness reports with `fidelity_tier`, `direction_verdict`, `known_limitations`, per-step composite trajectories — require calibration literacy. They are NOT designed for direct Finance Minister consumption at a negotiating table.

The kryptonite boundary is identical to G2A: harness output feeds Demo 8 background evidence, not negotiation-table instruments. The instrument panel (G1, G3, G4) is the negotiation-table artifact; G2C provides the empirical grounding that gives those artifacts credibility.

The `known_limitations` block is by design interpretable by a calibration-literate analyst: "⚠ DIRECTION_ONLY at most — stock-flow accounting not enforced" is self-describing for a Persona 2 user. No specialist translation is required for this audience.

If Demo 8 narrative attempts to present raw harness output directly to a non-analyst stakeholder without interpretation, Customer Agent must flag this at the internal review stage.

---

## 6. Out of Scope (G2C)

- **Iceland 2008–11 (G2D, #1553)** — blocked by capital controls gap (#1532)
- **CI-gated calibration from G2C results** — G2C runs are battle-testing runs (qualitative review), not Bayesian posterior inputs (G3 scope). G2C fidelity tiers do not feed #1543 directly — only SEN and ZMB (G2B) are the Bayesian posterior calibration inputs
- **Automated sweep across counter-factual parameter ranges** — G2C uses fixed counter-factual control input sequences; parameter sweeps are G1 / constraint-floor search scope (#1540)
- **UI rendering of harness output** — harness output is CLI/file; panel display is future scope
- **Country policy analysis beyond fixture scope** — G2C implements the simulation; it does not produce policy recommendations. `known_limitations` and `direction_verdict` are model outputs, not WorldSim-endorsed policy prescriptions
- **Ecuador, Lebanon, Thailand** — these have existing Type A fixtures but are not in the G2C issue roster; they are not in scope

---

## 7. Test Authorship Obligation

**QA Lead:** QA Lead Agent
**Test authorship deadline:** Before any G2C implementation PR opens on `sprint/m19-g2`
**Test file:** `backend/tests/backtesting/test_m19_g2c_scenario_runs.py`

*NM-078 compliance: test file at `backend/tests/backtesting/` — CI-discoverable path.*

**Test file structure — additive approach (preferred, per sprint entry §2.4):**

The test file is authored with Greece and Argentina functions initially. Sri Lanka, Pakistan, Turkey, Egypt, and Ghana test functions are added in each country's feature PR. This avoids the NM-056 tension (no skip stubs) while accommodating the sequential PR landing pattern.

```
# Initial authorship (before any G2C PR opens):
test_greece_counterfactual_type_b()  — AC-1, AC-2, AC-3, AC-4, AC-5, AC-6, AC-GRE-1..5, AC-9, AC-10
test_argentina_counterfactual_type_b() — AC-1, AC-2, AC-3, AC-4, AC-5, AC-7, AC-ARG-1..5, AC-9, AC-10

# Added with Sri Lanka PR (#1549):
test_sri_lanka_type_a_and_b()       — AC-1, AC-2, AC-3, AC-4, AC-5, AC-8, AC-NC-2, AC-NC-3, AC-LKA-1..4, AC-9, AC-10

# Added with Pakistan PR (#1550):
test_pakistan_type_b()              — AC-1, AC-2, AC-3, AC-4, AC-5, AC-NC-2, AC-NC-3, AC-PAK-1..3, AC-9, AC-10

# Added with Turkey PR (#1551):
test_turkey_type_b()                — AC-1, AC-2, AC-3, AC-4, AC-5, AC-NC-2, AC-NC-3, AC-TUR-1..3, AC-9, AC-10

# Added with Egypt PR (#1552):
test_egypt_type_b()                 — AC-1, AC-2, AC-3, AC-4, AC-5, AC-8, AC-NC-2, AC-NC-3, AC-EGY-1..3, AC-9, AC-10

# Added with Ghana PR (#1554):
test_ghana_type_a_and_b()           — AC-1, AC-2, AC-3, AC-4, AC-5, AC-NC-2, AC-NC-3, AC-GHA-1..4, AC-9, AC-10
```

**Direction verdict assertions are advisory (log, not fail):** Per sprint plan and §3.2, G2C direction verdict assertions (AC-GRE-2, AC-ARG-2, and equivalent per-country ACs) must NOT cause pytest failures if the model disagrees with the expected direction. Use `pytest.warns` or a custom advisory assertion wrapper:
```python
def assert_direction_advisory(actual, expected, country, indicator):
    if actual != expected:
        warnings.warn(
            f"G2C advisory: {country} {indicator} direction_verdict={actual}, expected={expected}. "
            "Review harness output — not a CI failure.",
            stacklevel=2,
        )
```
Hard assertions (that DO fail CI if violated) are: AC-1 (importability), AC-2 (scenario creation), AC-3 (run completes), AC-4 (verdict field present), AC-5 (known_limitations non-empty), AC-6/AC-7 (non-regression), AC-8 (capital controls disclosure), AC-10 (cleanup).

**QA Lead acknowledgment:**
`[x]` QA Lead: Initial test file with Greece and Argentina test functions authored at `backend/tests/backtesting/test_m19_g2c_scenario_runs.py` — filed 2026-07-03

---

## Appendix A — Greece 2010–15 Counter-factual (#1547, Type B)

**ISO 3166-1 alpha-3:** GRC
**Scenario window:** 2010–2015 (6 annual steps — uses existing `build_greece_scenario()` as baseline)
**Existing fixture:** `backend/tests/fixtures/greece_2010_scenario.py`

**Baseline (Type A):** Actual IMF/EC/ECB troika programme — Step 1 (2010) IMF programme acceptance + large primary surplus targets (4.5% GDP by 2012–13); Step 6 (2015) capital controls.

**Counter-factual:** A more gradual fiscal adjustment path — primary surplus target of ≤ 2.5% GDP at Step 1 (rather than the troika's aggressive front-loading). The counter-factual represents the debate that surrounded the 2010 programme design: were the conditionality targets too severe given the Greek fiscal multiplier environment, driving a deeper GDP contraction and steeper debt/GDP trajectory than the fiscal adjustment would save?

**New function:** `build_greece_counterfactual_scenario() -> ScenarioCreateRequest`
- Same initial state as `build_greece_scenario()` (Greece 2009 baseline values)
- Same `entity_id = "GRC"`, same step count (6), same `is_pre_calibration = False` (not a calibration run)
- Modified `scheduled_inputs`: Step 1 fiscal consolidation shock is reduced (smaller spending cut / smaller deficit target). The implementing agent selects the specific control input values with reference to the academic literature on the Greek fiscal multiplier debate (Blanchard-Leigh 2013 IMF WP is the canonical reference). Tier 3 (INFERRED_STRUCTURAL) for counter-factual inputs.

**Primary evaluated indicator:** `hd_composite` (direction verdict AC-GRE-2 is advisory)

**Known limitations expected:**
- Stock-flow accounting (#30) — always present
- Capital controls transmission (#1532) — active at Step 6 in baseline
- Bilateral trade weights frozen (#35) — active given Greece's deep eurozone trade linkage

**Data sources (established):** Eurostat, IMF WEO, ECB Statistical Data Warehouse — already in `source_registry` from prior Greece fixture work.

---

## Appendix B — Argentina 2001 Counter-factual (#1548, Type B)

**ISO 3166-1 alpha-3:** ARG
**Scenario window:** 1999–2002 (4 annual steps for counter-factual; existing `build_argentina_scenario()` is 2001–2002 at 2 steps)
**Existing fixture:** `backend/tests/fixtures/argentina_2001_2002_scenario.py`

**Baseline:** Existing `build_argentina_scenario()` run through the harness as TYPE_B baseline — the convertibility peg maintained until forced default (December 2001), with the corralito (banking restriction) and pesification (January 2002).

**Counter-factual:** Managed peg exit in 1999–2000, before the convertibility system reached Coffin Corner. Argentina's fiscal position was already deteriorating by 1999 (Recession, Tequila hangover). A managed crawling peg or outright float in late 1999/early 2000 is the counter-factual — avoids the IMF Blindaje (2000, $39.7B) and avoids the corralito and default. The counter-factual requires an extended scenario window (starting 1999) that the existing 2-step fixture does not cover.

**New function:** `build_argentina_counterfactual_scenario() -> ScenarioCreateRequest`
- Initial state: Argentina 1999 economic baseline (earlier than existing fixture)
- `entity_id = "ARG"`, `n_steps = 4` (1999, 2000, 2001, 2002)
- Scheduled inputs: Step 1 (1999) — begin managed crawl-down of the peg + introduce gradual fiscal adjustment; Step 2 (2000) — controlled exchange rate adjustment; Step 3 (2001) — no corralito, managed float underway; Step 4 (2002) — recovery baseline post-devaluation
- `is_pre_calibration = False`

**Data sourcing note:** Argentina 1999 initial state requires IMF WEO 1999 vintage and INDEC historical data. INDEC data quality caveats (statistical reliability post-2007 are well-documented, but 1999–2001 data is generally accepted). Chief Methodologist advisory NOT required for Argentina (extends existing fixture — sprint entry §2.2) but implementing agent must confirm 1999 data is available in approved sources before constructing initial state.

**Primary evaluated indicator:** `fin_composite` (direction verdict AC-ARG-2 is advisory)

**Known limitations expected:**
- Stock-flow accounting (#30) — always present
- Bilateral trade weights frozen (#35) — Argentina's Mercosur + US trade linkage is structurally important for the devaluation counter-factual magnitude
- Counter-factual control inputs Tier 3 — crawling peg exit path is a modelling assumption

**Data sources (established):** INDEC, IMF WEO, World Bank WDI — in or appendable to `source_registry`.

---

## Appendix C — Sri Lanka 2022–23 (#1549, Type A+B)

**ISO 3166-1 alpha-3:** LKA
**Scenario window:** 2020–2023 (4 annual steps)
**Run classification:** Type A+B
**CM advisory required before feature PR opens:** Yes (new country)

**Type A (replay):** Sri Lanka's actual crisis trajectory — 2020 COVID shock + pre-existing debt vulnerability, 2021 failed organic farming mandate + foreign reserve collapse, 2022 default (first in Sri Lanka's history, $51B debt), 2022–23 IMF programme negotiation and approval (March 2023).

**Type B (counter-factual):** Earlier IMF approach — what if Sri Lanka had approached the IMF in mid-2021 (when foreign reserves fell below 2 months of imports) rather than waiting until April 2022? The counter-factual avoids the March 2022 default and the acute 2022 social crisis (fuel queues, power cuts, food shortages).

**New functions:**
- `build_lka_scenario() -> ScenarioCreateRequest` — Type A, initial state 2019 Sri Lanka baseline
- `build_lka_counterfactual_scenario() -> ScenarioCreateRequest` — Type B, same initial state, modified scheduled inputs (Step 2 = IMF programme acceptance in 2021 rather than default)

**Primary failure mode:** Coffin Corner — external balance and political feasibility constraints made both tightening (reserves) and loosening (inflation) lethal by 2022. The 2021 organic farming mandate that eliminated foreign exchange spending on fertiliser imports is a concrete Coffin Corner input that accelerated the reserve collapse.

**Primary evaluated indicator (Type B):** `fin_composite` or `gov_composite` — Chief Methodologist advisory determines which indicator has sufficient data quality for the direction verdict.

**CM advisory scope:**
1. Confirm Tier 2 primary sources available for LKA 2019 initial state (Central Bank of Sri Lanka Statistical Data, IMF WEO 2019 vintage)
2. Confirm fidelity ceiling achievable (DIRECTION_ONLY expected — LKA data is Tier 2-3 for HD indicators)
3. Advise on whether `EmergencyInstrument.CAPITAL_CONTROLS` should be active (Sri Lanka imposed unofficial capital restrictions in late 2021)
4. Confirm whether 4 steps (annual) is appropriate or whether 3 steps (2020–2022) captures the crisis more cleanly

**Known limitations expected:**
- Stock-flow accounting (#30) — always present
- Capital controls transmission (#1532) — likely active (Sri Lanka's 2021-22 capital restrictions)
- Demographic module not enabled — Sri Lanka's human cost includes significant educated youth emigration during the 2022 crisis; not captured

**Data sources (pending CM advisory for approval):** Central Bank of Sri Lanka, IMF WEO, World Bank WDI, CBSL Annual Reports

---

## Appendix D — Pakistan 2022–23 (#1550, Type B)

**ISO 3166-1 alpha-3:** PAK
**Scenario window:** 2019–2023 (5 annual steps)
**Run classification:** Type B
**CM advisory required before feature PR opens:** Yes (new country)

**Type A baseline:** Constructed from `build_pak_scenario()` — initial state 2019 Pakistan (IMF EFF programme entry, July 2019, $6B); Step-by-step progression through COVID fiscal shock (2020), political instability (2021–22 Imran Khan government + PTI crisis), 9th IMF review delay (2022), flood crisis compounding the balance of payments shock (August 2022), IMF standby arrangement approval (July 2023).

**Type B (counter-factual):** Completed 9th IMF review on schedule (expected March 2022) rather than the 14-month delay driven by political unwillingness to implement subsidy reforms and fuel price increases. Counter-factual avoids the near-default spiral of H1 2023, which required a bridge loan from Saudi Arabia and UAE to avoid Zambia-style arrears.

**Primary failure mode:** Get-There-Itis — Pakistan's political leadership was committed to a populist policy path (subsidy retention, fuel subsidies) that was incompatible with IMF programme conditions, leading to repeated programme suspensions despite recognising the eventual reckoning.

**Primary evaluated indicator:** `fin_composite` (direction verdict advisory)

**CM advisory scope:**
1. Confirm Tier 2 primary sources for PAK 2018 initial state (SBP Statistical Bulletin, IMF WEO 2019)
2. Confirm achievable fidelity tier (DIRECTION_ONLY expected — political instability module represents major structural gap)
3. Advise whether the Political Economy module captures programme conditionality compliance dynamics sufficiently for this counter-factual to produce a directionally meaningful result
4. Advise on step count — 5 annual steps (2019–2023) or a subset covering the acute 2022–23 period

**Known limitations expected:**
- Stock-flow accounting (#30) — always present
- Political economy granularity — Pakistan's multi-party coalition breakdown is not modeled at sub-annual resolution
- External sector capital flows — bilateral IMF/GCC lending relationships may not be fully captured

**Data sources (pending CM advisory):** State Bank of Pakistan, IMF WEO, World Bank, IMF Article IV reports

---

## Appendix E — Turkey 2018–19 (#1551, Type B)

**ISO 3166-1 alpha-3:** TUR
**Scenario window:** 2017–2019 (3 annual steps)
**Run classification:** Type B
**CM advisory required before feature PR opens:** Yes (new country)

**Type A baseline:** Constructed from `build_tur_scenario()` — initial state 2017 Turkey (pre-crisis: high growth, but widening current account deficit + dollarised corporate debt + growing political pressure on TCMB); 2018 Step: lira crisis (August 2018, 40% lira depreciation); TCMB resists rate hikes under presidential pressure; 2019 Step: recession, rate cuts resume under political pressure despite inflation above 15%.

**Type B (counter-factual):** TCMB raises policy rate to defend the lira at the start of the August 2018 crisis (a conventional central bank response). The counter-factual asks: does the orthodox response produce better `fin_composite` and `gov_composite` outcomes than the actual path of prolonged unorthodoxy? The counter-factual also carries political economy cost (rate hikes are politically unpopular under Erdogan) — the model should reflect the governance tension.

**Primary failure mode:** Backside of the Power Curve — cutting rates to stimulate growth when the structural constraint (lira stability, inflation, dollarised debt) required the opposite response accelerated the crisis rather than averted it.

**Primary evaluated indicator:** `fin_composite` (direction verdict advisory)

**CM advisory scope:**
1. Confirm Tier 2 data availability for TUR 2017 initial state (TCMB data, Turkstat, IMF WEO 2017)
2. Confirm whether the Political Economy module adequately models the political cost of the counter-factual (rate hike against presidential preference)
3. Advise on fidelity tier achievable for Turkey (DIRECTION_ONLY expected — Turkey's economy has complex internal political economy dynamics)
4. Confirm 3 steps (annual, 2017–2019) is sufficient to capture the Backside of the Power Curve pattern

**Known limitations expected:**
- Stock-flow accounting (#30) — always present
- Dollarised corporate debt amplification — Turkey's corporate foreign-currency debt exposure is a key transmission channel not fully captured at current model resolution
- Political Economy module political cost representation

**Data sources (pending CM advisory):** TCMB Electronic Data Delivery System, Turkstat, IMF WEO

---

## Appendix F — Egypt 2016 (#1552, Type B)

**ISO 3166-1 alpha-3:** EGY
**Scenario window:** 2016–2018 (3 annual steps)
**Run classification:** Type B
**CM advisory required before feature PR opens:** Yes (new country)

**Type A baseline:** Constructed from `build_egy_scenario()` — initial state 2015 Egypt (pre-programme: widening current account deficit, subsidised fuel/food consuming ~7% GDP, foreign reserves under pressure, multiple exchange rate windows); 2016 Step: IMF programme acceptance (November 2016 $12B EFF) + full float of EGP (50% depreciation on float) + energy subsidy reform phase 1; 2017 Step: inflation spike (32% peak July 2017) + continued subsidy reform; 2018 Step: inflation normalisation + GDP growth recovery to ~5%.

**Type B (counter-factual):** Managed float rather than full float in November 2016 — a crawling peg or managed depreciation path rather than the shock full float. Egypt's 2016 programme is one of the more "successful" IMF programme cases; the counter-factual asks whether the managed float would have produced worse or similar outcomes (less inflation shock, slower reserves replenishment, delayed programme credibility).

*Note: This is an unusual Type B scenario where the baseline (what Egypt actually did) may be assessed as BETTER than the counter-factual — a managed float may have produced a worse inflation-credibility trade-off. The direction verdict should be interpreted as a model stress test, not a policy prescription.*

**Primary failure mode:** N/A — Egypt 2016 is not a crisis case in the failure mode taxonomy. This run tests WorldSim's ability to model a programme that worked, with the counter-factual testing the robustness of that outcome. The `known_limitations` should note that Egypt 2016 sits outside the primary WorldSim failure mode framework.

**Primary evaluated indicator:** `fin_composite` (direction verdict advisory; result may be `BASELINE_BETTER` — this is correct for the Egypt case)

**CM advisory scope:**
1. Confirm Tier 2 data for EGY 2015 initial state (Central Bank of Egypt, CAPMAS, IMF WEO 2016)
2. Confirm whether Egypt 2016 is modellable as a meaningful Direction Verdict case, or whether `INDISTINGUISHABLE` is the expected result given the model's inability to capture the inflation-credibility trade-off
3. Advise on energy subsidy representation in the fiscal composite (subsidy reform is a major policy lever not uniformly represented across modules)
4. Confirm whether `EmergencyInstrument.CAPITAL_CONTROLS` was technically active (Egypt maintained capital controls informally through 2016 despite the formal float)

**Known limitations expected:**
- Stock-flow accounting (#30) — always present
- Energy subsidy representation — fiscal composite may understate the GDP impact of subsidy reform
- Capital controls (#1532) if active
- Egypt 2016 outside primary failure mode framework — note in `known_limitations`

**Data sources (pending CM advisory):** Central Bank of Egypt, CAPMAS, IMF WEO, World Bank WDI

---

## Appendix G — Ghana 2022–23 (#1554, Type A+B)

**ISO 3166-1 alpha-3:** GHA
**Scenario window:** 2020–2023 (4 annual steps)
**Run classification:** Type A+B
**CM advisory required before feature PR opens:** Yes (new country)

**Type A (replay):** Ghana's actual crisis trajectory — 2020 COVID fiscal shock (deficit reached ~11.7% GDP); 2021 continued fiscal expansion + rising inflation; 2022 global rate rise environment + domestic debt spiral (domestic interest payments exceeded total tax revenue); July 2022 debt default (domestic + external); IMF programme approved May 2023 ($3B ECF/EFF/RSF).

**Type B (counter-factual):** Earlier IMF approach in 2021 — what if Ghana had approached the IMF when domestic interest costs exceeded 40% of tax revenue (mid-2021), rather than waiting until the acute July 2022 default? The counter-factual avoids the worst of the 2022 domestic debt crisis and the associated banking system capital shortfall.

**New functions:**
- `build_gha_scenario() -> ScenarioCreateRequest` — Type A, initial state 2019 Ghana baseline (pre-COVID)
- `build_gha_counterfactual_scenario() -> ScenarioCreateRequest` — Type B, same initial state, modified scheduled inputs (Step 2 = 2021 IMF programme acceptance; domestic debt restructuring begins before default)

**Primary failure mode:** Backside of the Power Curve — fiscal expansion financed by domestic debt at rising yields accelerated the debt/revenue spiral, making the eventual adjustment more painful. The 2020–21 fiscal choices (COVID spending + recurrent spending growth) consumed the fiscal space that could have accommodated a managed adjustment.

**Primary evaluated indicator (Type B):** `fin_composite` (direction verdict advisory — earlier IMF is expected to produce COUNTER_FACTUAL_BETTER)

**CM advisory scope:**
1. Confirm Tier 2 primary sources for GHA 2019 initial state (Bank of Ghana Statistical Bulletin, IMF WEO 2019, SDFP data)
2. Confirm achievable fidelity tier (DIRECTION_ONLY expected — Ghana's domestic debt restructuring dynamics are complex)
3. Advise on domestic debt representation in `fin_composite` (Ghana's crisis was driven by domestic instrument yields, not external debt directly)
4. Confirm whether 4 steps (2020–2023 annual) captures the trajectory meaningfully or whether a tighter 2021–2023 window is more data-reliable

**Known limitations expected:**
- Stock-flow accounting (#30) — always present
- Domestic debt yield spiral not fully captured at current resolution
- Banking sector capital adequacy — banks holding >50% of domestic debt are impaired by restructuring; this second-order effect may not be captured
- Bilateral creditor composition — Ghana's external creditors include China, Eurobond holders, and Paris Club; multilateral vs bilateral restructuring dynamics not modeled

**Data sources (pending CM advisory):** Bank of Ghana, IMF WEO, World Bank WDI, IMF Article IV reports

---

*Intent document version: 2026-07-03. Sprint entry: `docs/process/sprint-plans/m19-g2c-sprint-entry.md`.
See `docs/process/agent-execution-lifecycle.md` for the five-step lifecycle this document gates.*
