---
name: m19-cm-a-euro-area-calibration-decision
type: calibration-decision
issue: "#1623"
sprint: M19-CM-A
status: FILED — gates test authorship and ELASTICITY_REGISTRY implementation PR
authored-by: Chief Methodologist
authored-date: 2026-07-03
intent-document: docs/process/intents/M19-CMA-2026-07-03-euro-area-elasticity-calibration.md
implements: docs/process/sprint-plans/m19-cm-a-sprint-entry.md §Section 2.4 PENDING gate
---

# CM Calibration Decision: Euro Area Entity Family — M19 CM Sprint A

> **Authority:** This document is the calibration decision artifact for #1623 Gap 1.
> It closes the PENDING gate in sprint entry §2.4 and is the specification from which
> `backend/tests/test_m19_cm_a_elasticity_calibration.py` is authored. The ELASTICITY_REGISTRY
> implementation PR may not open until this document is committed.
>
> **What this document decides:** Which elasticity values to use for Euro area programme
> countries (GRC entity family) in the DemographicModule `ELASTICITY_REGISTRY`, and how to
> scope them so they do not fire on SSA entities. This is not a prediction of Greece's
> unemployment trajectory — it is a calibration of the model's cohort transmission coefficient
> for Euro area crisis conditions.

---

## 1. Background: The Gap and its Consequence

### 1.1 Current state

The ELASTICITY_REGISTRY (M17-G1 calibration) contains entries for SSA entity families
calibrated from Fosu (2011) and Ball et al. (2013). These fire on ALL entities because
`CohortElasticity` has no entity-family filter. This produces two problems for GRC:

1. **Wrong cohort:** The SSA entries target Q1 INFORMAL and Q1 AGRICULTURE workers —
   the primary vulnerable cohorts in a low-income SSA economy. Greece's primary vulnerable
   cohorts during the 2010–2013 crisis were Q1–Q2 FORMAL workers who faced unemployment as
   fiscal consolidation reduced public sector payrolls and private sector demand.

2. **Wrong magnitude:** SSA poverty-growth elasticities (Fosu 2011: −0.20 for Q1 informal)
   were calibrated against SSA structural conditions (minimal formal safety nets, subsistence
   exposure). Euro area workers have formal unemployment insurance, reducing the per-unit GDP
   impact on poverty headcount in the short run — but the impact concentrates on those who
   exhaust UI or are ineligible.

Consequence: Greece 2010 Type B counter-factual (G2C #1547) produces an HD trajectory
response from the wrong cohorts at the wrong magnitudes. The direction verdict on `hd_composite`
is advisory because no entity-family scoping exists to produce a calibrated GRC response.

### 1.2 Structural choice at issue: entity-family scoping mechanism

The intent document declared an architectural decision point: **option (a)** or **option (b)**
for entity-family scoping. This document resolves that choice.

**CM position: Option (a) — add `entity_families: frozenset[str] | None` field to
`CohortElasticity`.**

Rationale:
- Option (b) (event_type routing via entity-family-specific event keys like
  `gdp_growth_change__euro_area_fixed_fx`) would require the MacroeconomicModule to emit
  entity-family-aware event types. This is a cross-module architectural change not in scope
  for CM Sprint A and would risk disrupting G2D/ADR-020 Channel implementations.
- Option (a) adds one field to the `CohortElasticity` dataclass with `None` as default,
  preserving all existing entries (they remain with `entity_families=None`, meaning all
  entities). The DemographicModule adds a two-line filter. Scope is minimal and isolated.
- The `frozenset[str]` type allows the filter to be extended to multiple entity families
  without further dataclass changes (e.g., `frozenset({"GRC", "PRT", "IRL", "CYP"})` for
  the full Euro area programme country family once CM Sprint A exits and data permits).

**Implementation note:** The `entity_families` field uses `None` for "fires on all entities"
(current behaviour for all SSA entries, unchanged). A populated `frozenset` restricts firing
to listed entity IDs. The DemographicModule filter:
```python
if row.entity_families is not None and entity.id not in row.entity_families:
    continue
```
This must be added to the inner loop in `DemographicModule.compute()` after the event_type
check. The SSA entries remain with `entity_families=None` — their behaviour is unchanged.

---

## 2. Literature Basis

### 2.1 Primary source: Blanchard & Leigh (2013)

Blanchard, O., & Leigh, D. (2013). "Growth Forecast Errors and Fiscal Multipliers."
IMF Working Paper WP/13/1. International Monetary Fund.
`ACADEMIC_LITERATURE_BLANCHARD_LEIGH_2013_FISCAL_MULTIPLIERS`

Blanchard & Leigh (2013) is the authoritative empirical finding on fiscal multipliers
during the European crisis. Key results relevant to GRC calibration:

- Forecast errors in IMF/EC growth projections for 2010–2011 were systematically related to
  planned fiscal consolidation. Countries with larger planned consolidation had larger output
  surprises — consistent with actual multipliers materially exceeding the assumed 0.5.
- Estimated actual multiplier range: **0.9 to 1.7** (Table 1, "Actual vs. Predicted Growth").
  The midpoint of 1.3 is the B&L point estimate for European crisis-period consolidation.
- Greece specifically: GDP declined approximately 25% between 2010 and 2013 against a
  cumulative fiscal adjustment of ~17% of GDP (troika programme). This implies a multiplier
  in the 1.3–1.5 range for the programme period.

**Role in calibration:** B&L (2013) establishes that the effective fiscal multiplier in
Euro area crisis conditions was approximately 2.5× the IMF's assumed value (1.3 vs 0.5).
In WorldSim, the MacroeconomicModule applies the fiscal multiplier — this is NOT adjusted
by the ELASTICITY_REGISTRY. However, B&L (2013) is the primary empirical evidence that
**fiscal consolidation in Euro area crisis conditions produces larger cohort welfare impacts
per unit fiscal adjustment than comparable SSA LIC programmes**, validating a distinct Euro
area calibration set rather than applying SSA constants.

### 2.2 Secondary source: Ball et al. (2013)

Ball, L., Furceri, D., Leigh, D., & Loungani, P. (2013). "The Distributional Effects of
Fiscal Consolidation." IMF Working Paper WP/13/151.
`ACADEMIC_LITERATURE_BALL_2013_FISCAL_CONSOLIDATION`

Ball et al. (2013) — already cited in the M17-G1 calibration for the between-quintile
scaling ratio — provides the cross-quintile structure for formal-sector consolidation episodes.
Key result relevant to GRC:

- Fiscal consolidation raises unemployment and reduces real wages. The unemployment effect
  is larger and more persistent than the real wage effect.
- In advanced economies, **the bottom quintile (Q1)** bears approximately twice the income
  loss per unit fiscal adjustment compared to the middle quintiles, even with formal
  unemployment insurance, due to shorter UI benefit duration and higher separation rates.
- The **Q2 FORMAL** sector bears approximately 0.60× the Q1 FORMAL impact (vs 0.667 for
  SSA scaling) — reflecting higher formal employment tenure in Q2 and stronger UI coverage.

### 2.3 Supporting data: Eurostat AROPE (At-Risk-of-Poverty Rate), Greece 2010–2013

Eurostat. (2014). "At-Risk-of-Poverty Rate (AROPE) — Greece 2008–2013." Eurostat
Statistics Explained. `ACADEMIC_LITERATURE_EUROSTAT_AROPE_GRC_2010_2013`

Greek AROPE data:
- 2010: 27.7%
- 2011: 31.0% (+3.3pp)
- 2012: 34.6% (+3.6pp)
- 2013: 35.7% (+1.1pp)
- Total increase: +8.0pp over 2010–2013

Cumulative Greek GDP decline 2010–2013: approximately 26% (OECD Annual National Accounts).

AROPE poverty-growth elasticity (AROPE change / GDP decline):
- Per 1pp GDP decline: AROPE rose by approximately 8pp / 26pp = 0.31 per unit GDP decline
- Annual (not quarterly) basis; quarterly dynamics concentrate in the 2011–2012 deepening

**Note on cohort vs aggregate:** AROPE is an aggregate at-risk-of-poverty rate. WorldSim
calibrates at the cohort level. The bottom quintile's poverty headcount ratio response is
approximately 2× the aggregate AROPE response (Ball et al. 2013 distributional concentration).
This gives a Q1 cohort elasticity estimate of approximately 0.62 per unit GDP growth decline.

---

## 3. Chosen Calibration

### 3.1 Calibration path

**Euro area Q1 FORMAL, AGE_25_54 — primary calibration:**
GDP growth change → `poverty_headcount_ratio` change for GRC Q1 formal sector workers

- **Point estimate:** `elasticity = Decimal("-0.25")`, `entity_families = frozenset({"GRC"})`
- **Uncertainty range:** −0.20 to −0.35 (from Eurostat AROPE lower/upper quarterly
  concentration; aggregate AROPE 0.31 × Q1 2× factor = 0.62 upper; dampened by formal
  sector UI (50% benefit coverage at crisis depth); conservative lower end from B&L (2013)
  advanced economy baseline)
- **Confidence tier:** T2 (peer-reviewed academic literature + Eurostat AROPE administrative
  data; directly applicable to Euro area crisis episode)
- **Note:** This is deliberately lower than the Eurostat AROPE-implied 0.62 to account for
  UI benefit coverage and the multi-quarter distribution of the adjustment. The Eurostat
  figure is a 3-year aggregate; quarterly dynamics show more concentrated response in
  quarters 4–8 of the programme. This calibration applies to the per-step dynamics.

**Euro area Q2 FORMAL, AGE_25_54 — secondary calibration:**
- **Point estimate:** `elasticity = Decimal("-0.15")`, `entity_families = frozenset({"GRC"})`
- **Uncertainty range:** −0.12 to −0.20 (Ball et al. 2013 60% scaling of Q1; full UI coverage
  in Q2 provides stronger initial buffer; 0.60 × 0.25 = 0.15 point estimate)
- **Confidence tier:** T2 (Ball et al. 2013 scaling applied to Euro area calibration above)

### 3.2 What is NOT calibrated in CM Sprint A

- **Country-level unemployment_rate:** The DemographicModule updates cohort-level
  `poverty_headcount_ratio`, not country-level `unemployment_rate`. The country entity's
  unemployment_rate attribute is set from the WDI seed data and is not currently updated
  by any module. Adding a country-level unemployment transmission pathway would require
  an ADR (new module capability) — out of scope for CM Sprint A. The cohort-level
  poverty_headcount_ratio is the appropriate ELASTICITY_REGISTRY target and is what drives
  the `hd_composite` score in the harness.

- **Euro area Q1 INFORMAL:** In Greece, the informal sector is smaller (estimated 20–25% of
  GDP vs 35–45% for SSA comparators; OECD 2014). Q1 informal workers in Greece face different
  structural risk than in SSA. Calibrating Q1 INFORMAL for GRC is deferred to a future CM
  sprint when sufficient data is available. CM Sprint A removes the SSA Q1 INFORMAL entry
  from firing on GRC (via entity_families filter) without replacing it — the cohort exists
  but its poverty_headcount_ratio is not updated by the ELASTICITY_REGISTRY for GRC.

- **Euro area Q1 AGRICULTURE:** Greece has a small agricultural sector; this cohort is not
  a primary crisis transmission channel. Deferred.

### 3.3 Scoping: what entities are affected

| Entry | entity_families | Effect |
|---|---|---|
| SSA Q1 informal (M17-G1) | `None` → remains all-entities BUT GRC Q1 INFORMAL is not updated once GRC is filtered | **The entity_families field on existing SSA entries MUST remain None.** Filtering is applied by NEW GRC entries targeting FORMAL cohorts. The SSA entries continue to fire on SSA entities. |
| GRC Q1 FORMAL (new) | `frozenset({"GRC"})` | Fires only on GRC |
| GRC Q2 FORMAL (new) | `frozenset({"GRC"})` | Fires only on GRC |

**Important:** The SSA entries (with `entity_families=None`) will still fire on GRC Q1 INFORMAL
and GRC Q2 INFORMAL cohorts. This is acceptable for CM Sprint A: the informal sector in Greece
is not the primary crisis transmission channel, and the SSA elasticity (−0.20) provides a
reasonable lower-bound estimate for Greek informal sector poverty response. A full GRC calibration
would add GRC-scoped informal sector entries (deferred). The priority is the formal sector
calibration, which is absent entirely without CM Sprint A.

**Non-regression commitment:** The SSA entries' `entity_families=None` must not change. The
field defaults to `None` and existing entries have no keyword for this field — the
`@dataclass(frozen=True)` default handles it. The implementation PR must not modify any
existing `CohortElasticity` instantiation.

---

## 4. MAGNITUDE Acceptance Criterion

### 4.1 Test assertion specification

The integration test `test_m19_cm_a_elasticity_calibration.py` asserts:

**Primary assertion (AC-1) — `hd_composite` divergence at step 4:**

```python
# Heterodox path better: hd_composite divergence (heterodox - orthodox) at step 4 (index 3)
# This is the peak divergence period (2013, maximum Greece unemployment and AROPE)
lower_bound = Decimal("0.010")  # 1.0 pp HD composite scale — minimum calibrated response
upper_bound = Decimal("0.20")   # 20 pp HD composite scale — cap against overfit
```

**Rationale for lower_bound = 0.010:**
- At step 4, cumulative fiscal differential between paths is approximately 2pp primary surplus
  × 4 steps = 8pp-step fiscal differential (order of magnitude)
- At MacroeconomicModule default multiplier ~0.5: ~4pp GDP growth rate differential
- At Q1 FORMAL elasticity −0.25: ~1.0pp poverty_headcount_ratio change per cohort
- The hd_composite score normalizes cohort poverty across the HD framework; 1.0pp poverty
  for Q1 FORMAL translates to approximately 0.01–0.05 on the hd_composite 0–1 scale
- Lower_bound = 0.010 is achievable with the calibrated constants and represents a genuine,
  detectable divergence on the composite scale

**Rationale for upper_bound = 0.20:**
- HD composite changes > 20pp between two fiscal scenarios within 4 steps would represent
  an implausible sensitivity for a formal-sector Euro area economy with unemployment insurance
- Upper bound guards against implementation errors that produce dramatic over-prediction

### 4.2 Non-regression assertion specification

```python
# SSA Q1 INFORMAL elasticity unchanged
from decimal import Decimal
EXPECTED_SSA_Q1_INFORMAL_ELASTICITY = Decimal("-0.20")

# FRAME-D source registry IDs unchanged
REQUIRED_SOURCE_IDS = {
    "ACADEMIC_LITERATURE_FOSU_2011_SSA_POVERTY_GROWTH",
    "ACADEMIC_LITERATURE_BALL_2013_FISCAL_CONSOLIDATION",
    "ACADEMIC_LITERATURE_IMF_2014_FISCAL_INEQUALITY",
    "ACADEMIC_LITERATURE_ICELAND_2008_CREDIT_CONTRACTION_PHC",
}
```

### 4.3 Entity-family scoping assertion specification

```python
# At least two GRC-scoped FORMAL sector entries must be present
grc_entries = [
    e for e in ELASTICITY_REGISTRY
    if hasattr(e, "entity_families")
    and e.entity_families is not None
    and "GRC" in e.entity_families
]
assert len(grc_entries) >= 2
```

This assertion is RED before implementation: `entity_families` attribute does not exist
on `CohortElasticity` (AttributeError, caught by `hasattr`) → `grc_entries = []` → assertion fails.

---

## 5. Source Registry IDs

New source registry IDs to be added (per `docs/DATA_STANDARDS.md §Data Provenance Requirements`):

| source_registry_id | Source |
|---|---|
| `ACADEMIC_LITERATURE_BLANCHARD_LEIGH_2013_FISCAL_MULTIPLIERS` | Blanchard & Leigh (2013) IMF WP/13/1 |
| `ACADEMIC_LITERATURE_EUROSTAT_AROPE_GRC_2010_2013` | Eurostat AROPE Greece 2010–2013 |

`ACADEMIC_LITERATURE_BALL_2013_FISCAL_CONSOLIDATION` is already registered (M17-G1).

---

## 6. Issue #1657 Coordination Note

Issue #1657 (DemographicModule dead event subscriptions) requires adding missing elasticity
entries for currently subscribed event types that have no registry entries. CM Sprint A adds
the `entity_families` field to `CohortElasticity`. The #1657 implementation PR must use
the new field syntax; CM Sprint A must not close before #1657's CM sign-off obligation is
assessed. This is a coordination point, not a blocking dependency: #1657 can proceed after
CM Sprint A is confirmed.

---

*Calibration decision document authority: intent document §3 PENDING gate.
Sprint entry: `docs/process/sprint-plans/m19-cm-a-sprint-entry.md` (EL Approved 2026-07-03).
This document gates: (1) test authorship, (2) implementation PR opening.
Author: Chief Methodologist. Date: 2026-07-03.*
