---
name: M16-G4-distributional-infrastructure
type: implementation-intent
issues: "#22 (scoped), #275, #102"
status: Filed 2026-06-24 — QA tests not yet authored; Ecological Economist DIC review on #275 required before EE-PENDING ACs finalize
authored-by: PM Agent
authored-date: 2026-06-24
implementing-agents:
  - "Chief Engineer Agent — backend: Quantity schema migration, SyntheticDataEngine (Methods E + B), ecological-to-financial transmission coefficient, comparison API distribution extension"
  - "Frontend Architect Agent — frontend: synthetic tier badge wiring in Zone 1B and Zone 1D, comparison variance band in Zone 1A"
sprint-entry: "docs/process/sprint-plans/m16-g4-sprint-entry.md — EL approval pending"
adr-reference: "ADR-007 (Synthetic Data Framework, ACCEPTED 2026-05-23) for #22; ADR-012 (External Sector Module, ACCEPTED 2026-06-05) for #275; None (#102 API extension)"
ee-review-gate: "PENDING — Ecological Economist DIC review on #275 required before AC-EE-1 and AC-EE-2 finalize (EE-PENDING pattern; see §4 EE-PENDING block)"
release-branch: release/m16
---

# Implementation Intent: M16-G4 — Distributional Infrastructure

> **Three issues, one PR target.** G4 delivers backend infrastructure across three independent
> feature areas: synthetic data schema + engine (#22 scoped), ecological transmission (#275),
> and comparison distribution API (#102). A single implementation PR is recommended; if the
> implementing agent determines #275 requires a separate coordination step with the Ecological
> Economist DIC, it may be split into G4a (backend + #22 + #102) and G4b (#275) — but no
> split may create a "test-only" follow-up PR.
>
> **EE-PENDING ACs.** The implementing agent may begin on #22 and #102 immediately. #275
> backend implementation may begin but the PR may not merge until the Ecological Economist
> DIC review comment on #275 is on record and the EE-PENDING ACs (AC-EE-1 and AC-EE-2)
> are confirmed. QA tests for all non-EE-PENDING ACs may be authored from this document now.
>
> **Capacity-allowing designation.** G4 is the first scope cut target per the sprint plan
> BPO consultation. If schedule pressure forces a cut before G4 is complete: #102 and #275
> are lower priority than #22 (scoped); the `Quantity` schema migration is the foundation
> all three depend on and should be delivered first. If the PR window closes before #102
> and #275 are complete, the schema migration and SyntheticDataEngine (Methods E + B) may
> ship without the frontend badge wiring or the comparison API extension — provided the
> non-regression ACs pass and no partial state is visible to the user.

---

## 1. Source Authority

**ADR — #22 (scoped):** ADR-007 — Synthetic Data Framework
**Status:** Accepted 2026-05-23. Coverage confirmed in G4 sprint entry §2.2.
ADR-007 §Consequences §Implementation Sequence steps 1 and 3 (partial):
step 1 = Quantity schema extension + Alembic migration;
step 3 (partial) = SyntheticDataEngine Methods E + B. Method A and comparison group registry are out of G4 scope.

**ADR — #275:** ADR-012 — External Sector Module (ARCH-006)
**Status:** Accepted 2026-06-05. #275 is within the ExternalSectorModule module boundary.
Ecological coefficient is a new shock parameter within the existing module — no new module boundary ADR required.

**ADR — #102:** None. API extension within existing `/compare` endpoint pattern.
Architect consultation (sprint plan §ADR Prerequisites): CLEAR.

**Binding decisions from sprint entry §2.2 (ADR-007 coverage assessment):**

| Decision source | Requirement | AC enforcing |
|---|---|---|
| ADR-007 §Consequences step 1 | `Quantity` table gains 4 new columns: `is_synthetic BOOL NOT NULL DEFAULT FALSE`, `synthetic_method VARCHAR`, `comparison_group_id VARCHAR`, `holdout_validated BOOL`; Alembic migration required | AC-1, AC-2 |
| ADR-007 §Section 1 Method E | Method E fires when MNAR, <3 comparables, or CI > 4× point estimate; sets `is_synthetic=True`, `synthetic_method="STRUCTURAL_ABSENCE"`, `value=None` | AC-3 |
| ADR-007 §Section 1 Method B | Method B (MICE) fires for ≥80% observed data, gap ≤3 periods, bounded on both sides; sets `is_synthetic=True`, `synthetic_method="SYNTHETIC_COMPARABLE"` | AC-4 |
| ADR-007 §Section 2 | Per-indicator badge visible without hover, click, or drawer in all display contexts where the indicator appears | AC-F1, AC-F2, AC-F3, AC-F4, AC-F5 |
| ADR-007 §Section 3 | Synthetic inference bands distinct from BandingEngine model uncertainty bands; labeled separately when both apply | AC-F8 |
| ADR-012 §ExternalSectorModule boundary | Ecological coefficient is a shock input to the existing ExternalSectorModule transmission chain; no new module boundary | AC-6, AC-EE-1 |

**Ecological Economist DIC pre-condition for #275:**
The Ecological Economist DIC review comment on #275 is required before AC-EE-1 and AC-EE-2 finalize. The EE must confirm: (a) the soil-degradation → agricultural-export → fiscal-revenue transmission pathway is the correct ecological-to-financial channel for the scenarios in scope; (b) the Zimbabwe 2005 land reform case is an appropriate historical calibration anchor; (c) the ±30% tolerance band and 4-step validation horizon are methodologically defensible. This review gates calibration AC finalization, not sprint entry or #22/#102 implementation.

**Issues in scope:** #22 (scoped), #275, #102

**Authored by:** PM Agent (pre-implementation spec; Chief Engineer Agent takes implementation authority at Step 3)
**Date:** 2026-06-24

---

## 2. Persona Trace Elements Targeted

*G4 is capacity-allowing infrastructure. It does not independently complete a new Demo 6
argument — it makes existing data more accurate (#22), extends analytical comparison
capability (#102), and adds an ecological pathway (#275). Persona trace is derived from
the downstream Demo 6 capabilities G4 supports.*

**P-1 — Personas served:**
- **Persona 2 — Finance Ministry Negotiator** (`docs/ux/personas.md §Persona 2`). Operational
  user. #22 ensures cohort tier labels (Zone 1B) reflect actual data quality — not hardcoded
  values — so Persona 2 can correctly assess confidence when citing the bottom-quintile
  threshold argument. #102 extends comparison capability for multi-scenario distributional
  analysis in Preparatory state. #275 enables ecological-shock-transmission analysis for
  resource-dependent economies (e.g., climate-linked fiscal risk assessment).
- **Persona 1 — Methodologist / Data Quality Steward** (`docs/ux/personas.md §Persona 1`,
  if present; otherwise as a role). The `Quantity` schema extension (#22) is the foundational
  data quality improvement that makes methodological honesty operationally real — synthetic
  flags are stored in the database and travel with exports rather than being implicit in
  source tier labels.

**P-2 — Entry state:**
Preparatory (3-hour briefing window). G4 is a Preparatory tool. None of the three issues
produces Reactive-state-usable output directly — they improve the accuracy of outputs
produced by G1/G2/G3 (#22) and extend analytical depth (#102, #275). The primary
Reactive-state outputs remain the G2 political risk summary (Zone 1D) and G3 milestone
sentence — G4 makes the metadata behind those outputs more accurate.

**P-3 — Journey reference:**
G4 contributes to the Demo 6 Senegalese Finance Minister scenario (Article IV consultation
preparation) by ensuring that: (a) zone 1B cohort tier labels accurately reflect whether SEN
data is real or synthetic, enabling the ministry team to correctly caveat their citations;
(b) multi-scenario distributional comparison is available if the ministry team wants to compare
the programme proposal to an alternative path (#102); (c) ecological shock transmission is
available for resource-dependent scenario analysis (#275, future scenarios beyond SEN/Demo 6).

**P-4 — Time/interaction ceiling:**
- Badge wiring (#22 frontend): The tier label is already visible at L0 from G2; G4 makes
  it accurate. No new interaction required. Zero additional time cost for Persona 2.
- Variance band (#102 frontend): Opt-in toggle — one additional interaction to enable.
  Acceptable for Preparatory state.

**P-6 — Negotiating leverage delivered (Persona 2):**

*#22:* Persona 2 can now state "the bottom quintile poverty headcount figure carries a Tier 3
confidence badge reflecting synthetic MICE imputation from comparable economies — not primary
statistics" and be correct, because the tier sub-label in Zone 1B is data-driven from the
actual `Quantity.is_synthetic` and `Quantity.synthetic_method` fields. Before G4, the "T3"
label was hardcoded and could silently misrepresent data quality for SEN indicators where no
World Bank primary data exists and Method E (Structural Absence) should fire.

*#102:* Persona 2 can compare the distributional outcome of Programme A vs Programme B at the
percentile level — "under Programme B, P90 of bottom quintile poverty headcount remains 12
points lower at step 4" — not just the mean delta. This distributional argument is not
available from the existing `/compare` endpoint.

*#275:* Finance ministries in resource-dependent economies (agricultural export reliance >40%
of fiscal revenue) can model an ecological shock as an additional stress on the programme
pathway — making the IMF scenario analysis more complete for climate-exposed contexts.

**P-7 — North Star capability delivered:**
Before G4: Zone 1B cohort rows displayed "T3" for all SEN cohort indicators regardless of
whether the underlying `Quantity` carried real data or synthetic inference — the tier label was
a confidence-tier assignment from the source, not a synthetic-method disclosure.
After G4: The tier sub-label in Zone 1B (and Zone 1D) is connected to `Quantity.is_synthetic`
and `Quantity.synthetic_method`; a Structural Absence Declaration produces "SAD" (not "T3"),
and a MICE estimate produces the correct tier sub-label. The finance minister's analyst can
accurately tell the negotiating team what kind of data quality underlies each cohort figure
without reading documentation or opening a data card.

---

## 3. Observable Application State

*All states verifiable by an external observer using only the running application.
No source code reading, no CI report reference, no implementation knowledge required.*

### 3.1 — #22 (scoped): Quantity schema + SyntheticDataEngine

**State 1 — Schema migration:**
`alembic upgrade head` applied to a fresh database instance completes without error. The
`quantity` table contains exactly the four new columns: `is_synthetic`, `synthetic_method`,
`comparison_group_id`, `holdout_validated`. A `GET /scenarios/{id}/trajectory` response for
a ZMB ECF scenario (existing data, no synthetic inference required) returns `is_synthetic:
false` (or omits the field per backwards-compatible schema) on all Quantity values — no
synthetic flags applied to real-data indicators. The ZMB 8-step run completes in unchanged
wall time (migration non-regression).

**State 2 — Method E (Structural Absence Declaration):**
When the SyntheticDataEngine is invoked for a DemographicModule indicator on an entity where
fewer than 3 comparable country observations exist in the source registry for that indicator,
the returned Quantity carries `is_synthetic: true`, `synthetic_method: "STRUCTURAL_ABSENCE"`,
and `value: null`. Zone 1B (if that indicator is displayed) shows the cohort row with a
"SAD" badge (or "T5") rather than a numeric value. No alert fires for this indicator —
ADR-007 §Section 5: Tier 5 shows Structural Absence Declaration only, no alert.

**State 3 — Method B (MICE):**
When the SyntheticDataEngine is invoked for an indicator with ≥80% observed data and a gap
≤3 periods bounded on both sides, the returned Quantity carries `is_synthetic: true`,
`synthetic_method: "SYNTHETIC_COMPARABLE"`, and a numeric `value` within [0.0, 1.0]
(for bounded ratio indicators). The tier sub-label reflects the gap length: T3 for short gap /
strong flanking, T4 for longer gap or weak flanking (ADR-007 §Section 4).

**State 4 — Non-regression (ZMB real-data path):**
A ZMB ECF scenario run produces no `is_synthetic: true` Quantity values on any indicator
sourced from World Bank primary statistics (poverty_headcount_ratio Q1/Q2 from WB → Tier 3
real data, not synthetic). Zone 1B cohort rows for ZMB display "T3" with no change from
pre-G4 — because the "T3" label now derives from the Quantity confidence tier (real data,
tier 3) rather than from `is_synthetic` being true.

### 3.2 — #275: Ecological-to-financial transmission

**State 5 — Coefficient accepted:**
A `SimulationRequest` with `ecological_shock_coefficient: 0.35` (for example) succeeds
(HTTP 200 or equivalent). The trajectory output reflects the reduced fiscal revenue pathway.
A request with `ecological_shock_coefficient: 0.0` (default) produces trajectory output
identical to a request with no `ecological_shock_coefficient` field at all (non-regression).
A request with `ecological_shock_coefficient: 1.1` returns a validation error (422).

**State 6 — Historical validation (EE-PENDING):**
[EE-PENDING — Ecological Economist DIC review on #275 required. Observable state to be
specified after EE confirms: (a) Zimbabwe 2005 land-reform coefficient value; (b) ±N%
tolerance band and step-horizon for validation; (c) which fiscal revenue indicator the
comparison is measured on. EE-PENDING state: when the EE-confirmed coefficient is applied
to ZMB, the fiscal revenue trajectory delta at step 4 is within ±EE-confirmed% of the
documented historical Zimbabwe 2005 outcome.]

**State 7 — api_contracts.yml currency:**
`docs/schema/api_contracts.yml` documents `ecological_shock_coefficient` as an optional
field on the simulation request schema, updated in the same commit as the backend
implementation (schema drift compliance — CLAUDE.md §Schema registry).

### 3.3 — #102: Distributional comparison API

**State 8 — Distribution fields in compare response:**
`GET /compare?scenario_a={valid_id}&scenario_b={valid_id}` returns a response body where
each compared indicator includes a `distribution` object: `{"variance": float, "p10":
float, "p50": float, "p90": float}`. Existing `delta` and `baseline` fields are present
and unchanged.

**State 9 — Insufficient data → null fields:**
When the comparison window has fewer than 3 comparable data points for an indicator, the
`distribution` object contains `{"variance": null, "p10": null, "p50": null, "p90": null}`.
The response is not an error.

**State 10 — Zone 1A comparison variance band (opt-in):**
In Zone 1A, when multi-entity or multi-branch comparison rendering is active and the
variance band toggle is enabled (not default), a shaded P10/P90 band is visible around
each trajectory curve. The band is labeled "Distributional range" — not "confidence
interval," not "uncertainty band" (ADR-007 §Section 3 distinction: synthetic inference bands
are distinct from BandingEngine model uncertainty bands).

**State 11 — api_contracts.yml currency:**
`docs/schema/api_contracts.yml` documents the `distribution` field in the compare response
schema, in the same commit as the backend implementation.

### 3.4 — Silent failure detection

**Silent failure 1 — Hardcoded tier label survives migration:**
If the frontend badge wiring is not implemented, Zone 1B cohort rows will continue to show
"T3" for all indicators regardless of `is_synthetic` state — the same behavior as pre-G4.
This is silent because: (a) for ZMB real-data scenarios it is correct, (b) only SEN or
other entities with synthetic data will reveal the gap. Detection: AC-F3 (Structural Absence
case) — the test must supply a fixture where `is_synthetic=True`, `synthetic_method=
"STRUCTURAL_ABSENCE"`, and assert the badge shows "SAD" not "T3". If the badge is hardcoded,
this test fails.

**Silent failure 2 — Method selection decision tree not followed:**
If the SyntheticDataEngine implements only Method E (fallback) and never dispatches Method B,
all indicators with partial data coverage will receive Structural Absence Declarations
instead of MICE imputation — degrading data quality silently. Detection: AC-4 explicitly
supplies an indicator meeting Method B conditions and asserts Method B fires (not Method E).

**Silent failure 3 — ecological_shock_coefficient silently ignored:**
If the coefficient is accepted in the schema but not applied in the engine, the trajectory
with `ecological_shock_coefficient=0.35` will be identical to `coefficient=0.0`. Detection:
AC-EE-1 (historical validation) catches this; AC-6 (non-regression with `coefficient=0.0`)
alone does not detect the silent no-op.

**Silent failure 4 — distribution fields conflated with BandingEngine bands:**
If the frontend labels the P10/P90 comparison band as "uncertainty band" or "confidence
interval" (BandingEngine terminology), it violates ADR-007 §Section 3 separation requirement.
Detection: AC-F8 explicit label assertion.

---

## 4. Acceptance Criteria

*Each criterion verifiable by an external observer using only the running application.
"CI passes" is not an AC.*

---

### Backend ACs — #22 (Quantity schema + SyntheticDataEngine)

*Test file: `backend/tests/test_m16_g4_distributional_infrastructure.py`, describe block `#22`*

**AC-1 — Quantity schema migration applies cleanly:**
`alembic upgrade head` against a fresh test database completes without error. `inspect(engine).get_columns("quantity")` returns a column list containing: `is_synthetic` (Boolean, not null, default False), `synthetic_method` (String, nullable), `comparison_group_id` (String, nullable), `holdout_validated` (Boolean, nullable).

**AC-2 — Non-regression: ZMB 8-step run unaffected by migration:**
Integration: a ZMB ECF scenario at default step count runs to completion post-migration. All Quantity values in the trajectory response have `is_synthetic == False` (or field absent per backward-compatible serialization). No Structural Absence Declarations appear for World Bank-sourced indicators.

**AC-3 — Method E fires for indicator with <3 comparables:**
Unit test: `SyntheticDataEngine.infer(entity_id="SYNTHETIC_TEST", indicator_key="test_no_comparables", source_registry=mock_registry_with_0_comparables)` returns a Quantity with `is_synthetic=True`, `synthetic_method="STRUCTURAL_ABSENCE"`, `value=None`. Method E is the only method that fires — Method B is not attempted when the comparable count is below 3.

**AC-4 — Method B fires for indicator meeting MICE conditions:**
Unit test: `SyntheticDataEngine.infer(entity_id="SYNTHETIC_TEST", indicator_key="test_mice_conditions", source_registry=mock_registry_with_valid_mice_conditions)` where the mock provides ≥80% observed data, gap ≤3 periods, bounded values. Returns a Quantity with `is_synthetic=True`, `synthetic_method="SYNTHETIC_COMPARABLE"`, `value` in [0.0, 1.0]. Method E is not invoked.

**AC-5 — Method selection order: B before E when B conditions are met:**
Unit test: when both Method B and Method E conditions could nominally apply (edge case: ≥80% observed data but MNAR flag set), the MNAR flag takes precedence and Method E fires. When MNAR flag is absent and B conditions are met, Method B fires before Method E is evaluated. Decision tree order follows ADR-007 §Section 1.

**AC-6 — api_contracts.yml documents is_synthetic field:**
`docs/schema/api_contracts.yml` contains the string `"is_synthetic"` within the trajectory response Quantity schema definition. Schema updated in the same commit as the backend implementation.

---

### Backend ACs — #275 (Ecological-to-financial transmission)

*Test file: `backend/tests/test_m16_g4_distributional_infrastructure.py`, describe block `#275`*

**AC-7 — ecological_shock_coefficient field accepted:**
`SimulationRequest(entities=["ZMB"], n_steps=8, ecological_shock_coefficient=0.35)` instantiates without validation error. `ecological_shock_coefficient=0.0` instantiates without error. `ecological_shock_coefficient=-0.01` raises `ValidationError`. `ecological_shock_coefficient=1.01` raises `ValidationError`.

**AC-8 — Non-regression: coefficient=0.0 produces identical trajectory to no coefficient:**
Integration: ZMB ECF scenario with `ecological_shock_coefficient=0.0` produces a trajectory
numerically identical to the same scenario with no `ecological_shock_coefficient` field.
Delta between fiscal revenue values at each step: exactly 0.0.

**AC-9 — api_contracts.yml documents ecological_shock_coefficient:**
`docs/schema/api_contracts.yml` contains `"ecological_shock_coefficient"` in the simulation request schema, documented as optional (default 0.0, range [0.0, 1.0]), in the same commit as the backend implementation.

**AC-EE-1 — Historical validation (EE-PENDING):**
*EE review required on #275 before this AC finalizes. Placeholder:*
Integration: ZMB scenario with `ecological_shock_coefficient={EE-confirmed value}` applied.
At step 4, the fiscal revenue trajectory delta from the baseline (no-coefficient) run is
within ±{EE-confirmed tolerance}% of the documented historical Zimbabwe 2005 land-reform
fiscal impact. EE must confirm: (a) coefficient value, (b) tolerance percentage, (c) step
horizon for comparison, (d) fiscal indicator key to compare. Implementing agent records the
validation result in the Step 4 Verify verdict.

**AC-EE-2 — Ecological Economist DIC review on record (gate):**
*EE review required before this AC can be checked.*
A comment from the Ecological Economist DIC agent on GitHub issue #275 is on record,
confirming: (a) transmission pathway correctness; (b) Zimbabwe 2005 calibration anchor
appropriateness; (c) tolerance parameters from AC-EE-1. The comment must be filed before
the implementation PR merges — not before it opens.

---

### Backend ACs — #102 (Comparison distribution API)

*Test file: `backend/tests/test_m16_g4_distributional_infrastructure.py`, describe block `#102`*

**AC-10 — distribution fields present in compare response:**
`GET /compare?scenario_a={id_a}&scenario_b={id_b}` returns a response body where each
compared indicator includes `distribution.variance` (float), `distribution.p10` (float),
`distribution.p50` (float), `distribution.p90` (float). Existing fields `delta` and
`baseline` are present and unchanged — this is additive only.

**AC-11 — Insufficient data → null distribution:**
When the comparison window for an indicator has fewer than 3 data points, the distribution
object contains `{"variance": null, "p10": null, "p50": null, "p90": null}`. The response
is HTTP 200, not an error.

**AC-12 — api_contracts.yml documents distribution fields:**
`docs/schema/api_contracts.yml` contains `"distribution"` with `variance`, `p10`, `p50`,
`p90` fields in the compare response schema, updated in the same commit as the backend
implementation.

---

### Frontend ACs — #22 (Synthetic tier badge wiring)

*Test file: `frontend/tests/e2e/m16-g4-distributional-infrastructure.spec.ts`, describe block `#22`*

**AC-F1 — Structural Absence badge ("SAD") on Zone 1B cohort row:**
With a fixture where a cohort row's underlying Quantity has `is_synthetic=True`,
`synthetic_method="STRUCTURAL_ABSENCE"`: `data-testid="cohort-tier-badge-{key}"` is
present and contains text `"SAD"` (or `"T5/SAD"` — implementing agent chooses; document
the choice; QA tests use the same value). The cohort row's value cell shows `"—"` (em dash
or equivalent null indicator), not a numeric value.

**AC-F2 — SYNTHETIC_COMPARABLE badge ("T3") on Zone 1B cohort row:**
With a fixture where a cohort row's underlying Quantity has `is_synthetic=True`,
`synthetic_method="SYNTHETIC_COMPARABLE"`, `holdout_validated=True`: the tier badge text
is `"T3"`. This is now data-driven from `synthetic_method`, not hardcoded.

**AC-F3 — SYNTHETIC_MODEL badge ("T4") on Zone 1B cohort row:**
With a fixture where a cohort row's underlying Quantity has `is_synthetic=True`,
`synthetic_method="SYNTHETIC_MODEL"`: the tier badge text is `"T4"`.

**AC-F4 — Real-data badge unchanged on Zone 1B cohort row:**
With a fixture where a cohort row's underlying Quantity has `is_synthetic=False`
(World Bank real data at Tier 3): the tier badge text is `"T3"`. Behavior is unchanged
from pre-G4. This is the ZMB ECF non-regression case.

**AC-F5 — Badge visible without hover, click, or drawer:**
In all three cases (AC-F1/F2/F3), `data-testid="cohort-tier-badge-{key}"` has a non-zero
`getBoundingClientRect` (visible, not hidden) without any user gesture. ADR-007 §Section 2
mandatory: badge must be visible without hover. The badge is not tooltip-only.

**AC-F6 — Zone 1D indicator badge wiring (same rules):**
Zone 1D indicators (PSP, legitimacy index, elite capture divergence) that carry synthetic
Quantity values display the same badge wiring as Zone 1B. Specifically: an indicator row
in Zone 1D with `is_synthetic=True`, `synthetic_method="STRUCTURAL_ABSENCE"` shows "SAD"
rather than a numeric value. If no Zone 1D indicators are synthetic in the current test
fixtures, this AC is deferred to a future sprint when SEN Zone 1D data is populated.

---

### Frontend ACs — #102 (Variance band in Zone 1A)

*Test file: `frontend/tests/e2e/m16-g4-distributional-infrastructure.spec.ts`, describe block `#102`*

**AC-F7 — Variance band not visible by default:**
In Zone 1A with multi-entity comparison rendering active (two entities loaded), the P10/P90
variance band is not visible by default. `data-testid="zone-1a-variance-band-{entityKey}"`
is absent from the DOM or has `display: none` without user interaction.

**AC-F8 — Variance band visible when toggled, labeled distinctly:**
After the variance band toggle is enabled (one user interaction), `data-testid=
"zone-1a-variance-band-{entityKey}"` is visible (non-zero bounding box). An element
with `data-testid="variance-band-label"` is present with text containing "Distributional
range" — not "uncertainty" and not "confidence interval." (ADR-007 §Section 3: synthetic
inference bands distinct from BandingEngine model uncertainty bands.)

**AC-F9 — Variance band toggle visible in Zone 1A controls:**
`data-testid="variance-band-toggle"` is present and visible in Zone 1A when comparison
mode is active. The toggle is not present when only a single entity is loaded (no
comparison active).

---

## 4b. Visual Spec (before/after)

*Required per `docs/process/intent-template.md §4b`. G4 introduces badge text changes
and a new opt-in UI element (variance band toggle). Both are specified below.*

### AC-F1/F2/F3/F4 — Zone 1B cohort tier badge wiring

**Before (pre-G4, ZMB scenario, World Bank real data):**
```
Zone 1B COHORT IMPACT sub-section at 1280×800:

┌──────────────────────────────────────────────────────────────────┐
│ COHORT IMPACT                                                    │
│ ─────────────────────────────────────────────────────────────── │
│ CRITICAL · Bottom income quintile — Poverty headcount           │
│           · Threshold crossed at step 2                         │
│           · was 8.3% above floor · [T3] · [World Bank]         │
│                                    ↑                            │
│                    Tier badge: text "T3" (hardcoded pre-G4)    │
└──────────────────────────────────────────────────────────────────┘
```

**After (G4, ZMB scenario — real data, no change):**
```
Zone 1B COHORT IMPACT sub-section at 1280×800:

┌──────────────────────────────────────────────────────────────────┐
│ COHORT IMPACT                                                    │
│ ─────────────────────────────────────────────────────────────── │
│ CRITICAL · Bottom income quintile — Poverty headcount           │
│           · Threshold crossed at step 2                         │
│           · was 8.3% above floor · [T3] · [World Bank]         │
│                                    ↑                            │
│       Tier badge: text "T3" (now data-driven: is_synthetic=F,  │
│       confidence_tier=3; result unchanged from pre-G4 ✓)       │
└──────────────────────────────────────────────────────────────────┘
```

**After (G4, SEN scenario — Structural Absence Declaration for an indicator):**
```
Zone 1B COHORT IMPACT sub-section at 1280×800:

┌──────────────────────────────────────────────────────────────────┐
│ COHORT IMPACT                                                    │
│ ─────────────────────────────────────────────────────────────── │
│ STRUCTURAL ABSENCE · Bottom income quintile — [indicator name]  │
│                    · Data unavailable for this entity           │
│                    · [SAD] · [Structural Absence Declaration]   │
│                       ↑                                         │
│       Tier badge: text "SAD" (is_synthetic=T,                   │
│       synthetic_method="STRUCTURAL_ABSENCE", value=null)        │
│       Numeric value replaced with "—"                           │
└──────────────────────────────────────────────────────────────────┘
```

**After (G4, SEN scenario — MICE imputation for an indicator):**
```
Zone 1B COHORT IMPACT sub-section at 1280×800:

┌──────────────────────────────────────────────────────────────────┐
│ COHORT IMPACT                                                    │
│ ─────────────────────────────────────────────────────────────── │
│ CRITICAL · Bottom income quintile — [indicator name]            │
│          · Threshold crossed at step 3                          │
│          · was 4.1% above floor · [T3] · [synthetic estimate]  │
│                                    ↑                            │
│       Tier badge: text "T3" (is_synthetic=T,                    │
│       synthetic_method="SYNTHETIC_COMPARABLE",                  │
│       holdout_validated=True → Tier 3)                         │
│       Badge visible at L0 — no hover required ✓                │
└──────────────────────────────────────────────────────────────────┘
```

### AC-F7/F8/F9 — Zone 1A variance band (comparison mode)

**Before (pre-G4, comparison mode active, two entities):**
```
Zone 1A at 1280×800, multi-entity Mode 1/2 comparison:

┌──────────────────────────────────────────────────────────────────┐
│ Zone 1A trajectory — entity A solid line, entity B dashed line  │
│                                                                  │
│   [No variance band visible]                                    │
│   [No toggle control]                                           │
└──────────────────────────────────────────────────────────────────┘
```

**After (G4, comparison mode, band toggle NOT yet activated — default):**
```
Zone 1A at 1280×800, multi-entity Mode 1/2 comparison:

┌──────────────────────────────────────────────────────────────────┐
│ Zone 1A trajectory — entity A solid, entity B dashed            │
│                                                                  │
│   [data-testid="variance-band-toggle"] ○ Distributional range   │
│   (toggle OFF by default — band not visible)                    │
└──────────────────────────────────────────────────────────────────┘
```

**After (G4, comparison mode, band toggle ON):**
```
Zone 1A at 1280×800, multi-entity Mode 1/2 comparison, toggle ON:

┌──────────────────────────────────────────────────────────────────┐
│ Zone 1A trajectory                                               │
│                                                                  │
│   ▓▓▓▓▓▓▓▓ P90 ─────────────────────────────────               │
│   ████████ trajectory curve A (solid)                          │
│   ▓▓▓▓▓▓▓▓ P10 ─────────────────────────────────               │
│                                                                  │
│   [data-testid="variance-band-label"] "Distributional range"    │
│   NOT "uncertainty band" — NOT "confidence interval"            │
│   [data-testid="variance-band-toggle"] ● ON                    │
└──────────────────────────────────────────────────────────────────┘
```

---

## 5. Kryptonite Constraint Check

*Authority: `docs/process/agent-execution-lifecycle.md §Kryptonite Design Constraint (FD-3)`.*

**Does any G4 deliverable's primary observable state require specialist mediation for Persona 2
to act on it in the Reactive entry state (90-second ceiling)?**

`[x]` **No** — with the conditions noted below.

**#22 (badge wiring):** The tier badge change (T3 → SAD for Structural Absence) is visible
at L0 and the badge text "SAD" is an abbreviation. The abbreviation alone is not self-
interpreting for a non-specialist. However: (a) G4 does not add a new interaction — it
corrects badge accuracy; (b) the "SAD" badge appears in Zone 1B only when data is absent,
which is a less common case in the ZMB/SEN scenarios used in Demo 6; (c) in the primary
Demo 6 scenarios, poverty_headcount_ratio has World Bank coverage — the SAD case will not
appear for the Q1/Q2 cohort rows in the Demo 6 rehearsal. The kryptonite constraint is
satisfied for Demo 6. A forward gap exists: a Persona 5 encountering "SAD" for the first
time without context may not understand it. Resolution: a tooltip or expanded label
("SADˣ — Data unavailable for this entity") is a pre-Demo 6 polish item, not a G4 blocker.

**#102 (variance band):** The band is opt-in — not visible by default. Persona 2 in
Reactive state will not encounter it unless they toggle it. In Preparatory state (3-hour
window), Persona 2 can enable the band and interpret "P10" and "P90" labels in a finance
context — these are standard distributional notation understood by financial analysts.
Constraint satisfied.

**#275 (ecological transmission):** The `ecological_shock_coefficient` is a scenario
configuration parameter, not a visible UI element. Persona 2 sets it during scenario
preparation in Preparatory state. No Reactive-state impact. Constraint satisfied.

**Named asymmetry gap (accepted):** A well-resourced analytical team can interpret the
full distributional variance band (#102) and extract percentile-level arguments beyond what
a finance ministry team using WorldSim for the first time can. The P10/P90 band provides
useful signal without requiring full statistical training. The gap is documented.

---

## 6. Out of Scope

| Scope item | Rationale for exclusion |
|---|---|
| Comparison group registry structure (ADR-007 §Consequences step 2) | Required for Method A (Hierarchical Bayesian); G4 implements Methods E and B only. Registry may be scaffolded (schema only) if time allows, but population is a data-architecture task requiring Data Architect sign-off. |
| Method A (Hierarchical Bayesian, `SYNTHETIC_COMPARABLE` from ≥10 comparables) | Requires populated comparison group registry. Out of G4 scope. |
| Full scenario banding display (P10/P50/P90 from synthetic inference, ADR-007 §Section 3) | Requires Method A and populated registry. Not Demo 6 critical. |
| Anomaly detection (ADR-007 §Section 7) | Requires TSC sign-off. Permanently excluded from routine milestone delivery. |
| MDA advisory alert visual treatment under synthetic data (ADR-007 §Section 5 amber dashed indicator) | Requires per-indicator tier sub-label from G4 engine. If the Frontend Architect Agent can deliver this within G4 scope it may be included; otherwise it is a separate post-G4 deliverable. |
| #275 Mode 2 ecological control input (user-steerable coefficient) | G4 delivers a fixed calibrated coefficient. Mode 2 steering UI is Mode 3-adjacent — separate deliverable. |
| #102 multi-scenario comparison (N > 2 entities) | `/compare` extension covers pairwise. N > 2 is a separate API design decision. |
| #102 cohort-level comparison distribution (requires G2 cohort data in compare response) | The compare endpoint extension adds distribution to the existing indicator-level response. Cohort-level comparison distribution requires G2 cohort data to be included in the compare response — a separate API extension. |
| G2 deliverables (#986, #987, #1163) | CLOSED 2026-06-24. G4 must not modify G2 component files. |
| G3 deliverable (#274) | CLOSED 2026-06-24. G4 must not modify the human-capital-trajectory-panel component. |

---

## 7. Test Authorship Obligation

**QA Lead:** QA Lead Agent
**Test authorship deadline (non-EE-PENDING ACs):** Before any G4 implementation PR opens against `release/m16`
**Test authorship deadline (EE-PENDING ACs):** After Ecological Economist DIC review comment is filed on #275

**Test file locations:**
- Backend pytest: `backend/tests/test_m16_g4_distributional_infrastructure.py`
- Frontend E2E: `frontend/tests/e2e/m16-g4-distributional-infrastructure.spec.ts`

**ACs available for immediate QA test authorship:**
Backend: AC-1, AC-2, AC-3, AC-4, AC-5, AC-6 (#22); AC-7, AC-8, AC-9 (#275 structural); AC-10, AC-11, AC-12 (#102)
Frontend: AC-F1, AC-F2, AC-F3, AC-F4, AC-F5, AC-F6, AC-F7, AC-F8, AC-F9

**ACs blocked pending Ecological Economist DIC review on #275:**
AC-EE-1, AC-EE-2

**Soft-skip guard (NM-056 follow-up, sprint entry §2.4):**
Neither test file may contain `test.skip()` or conditional skip patterns. The Quantity
schema migration test (AC-1) and the SyntheticDataEngine dispatch tests (AC-3, AC-4) must
not soft-skip on database startup failure — the G4 implementation PR must not merge until
these tests run and pass in CI. M16 exit checklist (#985) confirms no active soft-skip
patterns before it closes.

**Pre-push gates (from CLAUDE.md):**
- Backend: `cd backend && ruff check . && mypy app/` — exits 0 before any push modifying `backend/`
- Frontend: `cd frontend && npm run build` — exits 0 before any push modifying `frontend/src/`

**QA Lead acknowledgment:**
`[ ]` QA Lead: Tests for AC-1 through AC-12 and AC-F1 through AC-F9 authored and filed.
`[ ]` QA Lead: Tests for AC-EE-1 and AC-EE-2 authored and filed (after EE review on #275).

---

## 8. Step 4 Verify Record

*To be completed by the implementing agent before marking the implementation PR ready for review.*

**Verify date:** [pending]
**Verifier:** [Chief Engineer Agent / Frontend Architect Agent]
**PR:** [pending]

*Required verify elements for #275 (prior to PR ready):*
- Confirm Ecological Economist DIC review comment is on record on #275 (AC-EE-2)
- Record the EE-confirmed coefficient value, tolerance, and step-horizon applied in AC-EE-1
- Confirm fiscal revenue trajectory delta vs historical baseline is within confirmed tolerance

*Required verify elements for #22 (prior to PR ready):*
- Confirm `alembic upgrade head` against production-schema-equivalent database applies cleanly
- Confirm ZMB ECF scenario produces no `is_synthetic=True` flags on World Bank-sourced indicators

---

## 9. Step 5 Validate Record

*To be completed by the Business PO Agent at Step 5 Validate.*

**Validate date:** [pending]
**Validator (Business PO):** [pending]

---

*Intent document authority: `docs/process/intent-template.md` (version 2026-06-12).
Sprint entry: `docs/process/sprint-plans/m16-g4-sprint-entry.md` (EL approval pending).
ADR authority: ADR-007 (§22 scoped); ADR-012 (§275); None (§102).
Implementing agents: Chief Engineer Agent (backend); Frontend Architect Agent (frontend).
EE-PENDING pattern: follows G3 CM-PENDING pattern (G3 intent §4 CM-PENDING block).*
