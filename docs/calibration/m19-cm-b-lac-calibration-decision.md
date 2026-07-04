---
name: m19-cm-b-lac-calibration-decision
type: calibration-decision
issue: "#1623"
sprint: M19-CM-B
status: FILED — closes §2.4 PENDING gate; gates test authorship and implementation PR
authored-by: Chief Methodologist
authored-date: 2026-07-03
intent-document: docs/process/intents/M19-CMB-2026-07-03-lac-elasticity-calibration.md
implements: docs/process/sprint-plans/m19-cm-b-sprint-entry.md §Section 2.4 PENDING gate
---

# CM Calibration Decision: LAC Entity Family — M19 CM Sprint B

> **Authority:** This document is the calibration decision artifact for #1623 Gap 2.
> It closes the PENDING gate in sprint entry §2.4 and is the specification from which
> `backend/tests/test_m19_cm_b_elasticity_calibration.py` is authored. The ELASTICITY_REGISTRY
> implementation PR may not open until this document is committed.
>
> **What this document decides:** Which elasticity values to use for Latin American and Caribbean
> programme countries (ARG, ECU, BOL, PER entity families) in the DemographicModule
> `ELASTICITY_REGISTRY`, and how to scope them relative to the existing SSA entries.
> This is not a prediction of Argentina's or Ecuador's unemployment trajectory — it is a
> calibration of the model's cohort transmission coefficient for LAC crisis conditions.

---

## 1. Background: The Gap and its Consequence

### 1.1 Current state

The ELASTICITY_REGISTRY (CM Sprint A state) contains:
- SSA entries (entity_families=None): Q1 INFORMAL (-0.20), Q2 INFORMAL (-0.133),
  Q1 AGRICULTURE (-0.16), Channel C credit contraction (-0.30). Fire on ALL entities.
- GRC entries (entity_families=frozenset({"GRC"})): Q1 FORMAL (-0.25), Q2 FORMAL (-0.15).

For LAC countries (ARG, ECU, BOL, PER) this produces:
1. **SSA INFORMAL entries fire at SSA-calibrated magnitude.** The SSA Q1 INFORMAL entry
   at -0.20 was explicitly doubled from the prior -0.10 LAC-derived calibration (see
   `elasticities.py` comment: "2x prior Latin American calibration (Lustig 2017) per
   Fosu/Ravallion SSA-vs-LAC finding"). Applying the doubled SSA value back to the LAC
   population reverses the calibration reasoning.

2. **No FORMAL sector entries for LAC.** LAC programme episodes — particularly Bolivia
   and Peru structural adjustment (1985–92), Argentina 2001–02 currency crisis, Ecuador
   1999–2000 banking/dollarization crisis — transmitted poverty primarily through FORMAL
   sector workers. Public sector employment cuts in BOL/PER fiscal consolidation hit
   formal-sector Q1 workers. Argentina's corralito and pesification wiped formal-sector
   savings. Ecuador's bank freeze directly froze formal-sector depositors. None of these
   transmission channels are captured by the SSA Q1 INFORMAL entry.

Consequence: LAC Type B counter-factuals produce human development trajectories driven by
the wrong cohort at the wrong magnitude. The direction verdict on `hd_composite` is advisory
because no LAC-specific formal-sector entries exist.

### 1.2 Design question resolution: Option (a) — FORMAL-only entries

The intent document (§3) identified three options. **CM position: Option (a).**

Adding FORMAL-only entries for LAC means:
- SSA Q1 INFORMAL (entity_families=None) continues to fire on LAC Q1 INFORMAL at -0.20.
  This is accepted as a known overestimate for the informal sector in LAC fiscal
  consolidation episodes — the same acceptance applied in CM Sprint A for GRC informal workers.
  The informal sector poverty response in LAC IS meaningful; the SSA calibration is simply
  a rough upper bound rather than a LAC-specific estimate.
- New LAC Q1/Q2 FORMAL entries fire only on ARG, ECU, BOL, PER, adding the formal-sector
  channel that is absent from the registry for these entities.
- No double-counting arises: FORMAL and INFORMAL are distinct cohort_spec values; they
  target different cohort entities and do not sum to an overcounted total.

Option (b) (additive INFORMAL) was rejected: it would produce double-counted Q1 INFORMAL
responses for LAC entities without a mechanism to cap the sum.
Option (c) (excluding SSA entries from LAC) was rejected: it requires modifying existing
entries or adding module-level exclusion logic, which is beyond calibration-sprint scope.

---

## 2. Literature Basis

### 2.1 Primary source: Lustig et al. (2014) CEQ LAC Assessment

Lustig, N., Pessino, C., & Scott, J. (2014). "The Impact of Taxes and Social Spending on
Inequality and Poverty in Argentina, Bolivia, Brazil, Mexico, Peru and Uruguay: An Overview."
*CEQ Working Paper No. 13*, Commitment to Equity Project, Tulane University.
`ACADEMIC_LITERATURE_LUSTIG_2014_CEQ_LAC_POVERTY`

Lustig et al. (2014) provide the Commitment to Equity (CEQ) distributional framework for
LAC programme countries. Key results relevant to LAC calibration:

- Fiscal incidence assessments for Bolivia and Peru show that the bottom quintile formal-sector
  workers bear disproportionate burdens from fiscal consolidation episodes (direct taxes plus
  reduced transfers). In Bolivia (2009 assessment) and Peru (2009), Q1 formal-sector households
  experience welfare losses of 1.5–2.5× the aggregate per unit fiscal adjustment when transfers
  are cut.
- Argentina CEQ assessment: formal-sector Q1 workers (those just above the informal-poverty
  threshold) are most exposed to labour market contraction. Their poverty headcount response
  in fiscal consolidation is approximately 1.5–2.0× the aggregate response.
- Cross-country LAC average: Q1 formal-sector poverty-growth elasticity from CEQ episodes
  is approximately -0.18 to -0.28, with -0.22 as the central estimate for fiscal consolidation
  (not currency crisis) episodes.

**Distinction from currency/banking crises:** The CEQ framework measures responses to fiscal
policy changes (taxes and transfers). Argentina 2001 and Ecuador 1999 are primarily financial
crises; the fiscal-consolidation elasticity is a lower bound for those episodes. This calibration
intentionally uses the fiscal-consolidation basis, which is the conservative estimate:
- The GDP channel in WorldSim captures fiscal-adjustment-induced demand reduction
- The credit contraction channel (ADR-020 Channel C) captures the financial crisis transmission
- Together they provide a richer picture; this calibration governs only the GDP channel

### 2.2 Secondary source: Gasparini & Lustig (2011)

Gasparini, L., & Lustig, N. (2011). "The Rise and Fall of Income Inequality in Latin America."
In J.A. Ocampo & J. Ros (Eds.), *The Oxford Handbook of Latin American Economics*
(pp. 691–714). Oxford University Press.
`ACADEMIC_LITERATURE_GASPARINI_LUSTIG_2011_LAC_INEQUALITY`

Gasparini & Lustig (2011) document the distributional structure of LAC fiscal and economic
crises from the 1980s through the 2000s. Key calibration-relevant finding:

- During Latin American fiscal adjustment episodes (Bolivia 1985–87, Peru 1990–92, Ecuador
  2000 stabilisation), formal-sector Q1 workers experienced poverty headcount increases
  approximately 1.4–1.8× the national average per unit GDP contraction.
- The formal sector concentration factor in LAC (1.4–1.8×) is lower than the Euro area
  factor used in GRC calibration (~2×), reflecting LAC's higher informal sector buffer and
  more flexible informal wage adjustment.

This 1.4–1.8× concentration factor, applied to a LAC aggregate elasticity of approximately
-0.15 to -0.16 per unit GDP (IMF REO LAC data), gives Q1 FORMAL point estimate:
0.16 × 1.6 ≈ 0.256 → dampened for per-step dynamics → **-0.22** (conservative, T3).

### 2.3 Supporting: Ball et al. (2013)

Ball et al. (2013) — registered, provides the between-quintile scaling ratio.
Q2 FORMAL = 0.60 × Q1 FORMAL: 0.60 × 0.22 = 0.132, rounded to **-0.13**.
The 0.60 ratio reflects stronger UI coverage and employment tenure in Q2 vs Q1 —
the same structural logic as in GRC calibration.

### 2.4 Known limitation: financial vs fiscal crisis calibration mismatch

**Important:** ARG 2001–02 and ECU 1999–2000 are financial/currency crises. The primary
poverty transmission was through devaluation (real wage destruction) and banking system
failure (savings freeze), not through fiscal consolidation. Using a fiscal-consolidation
elasticity calibrated from CEQ data understates the actual poverty response for these
entities in their historical crisis episodes.

This is a **documented model limitation** for the ARG and ECU scenarios:
- The `known_limitations` field in G2C Type B counter-factual outputs should include:
  "LAC FORMAL sector elasticity calibrated from fiscal-consolidation episodes (Lustig 2014 CEQ).
  Actual poverty response in ARG 2001 and ECU 1999 was amplified by currency devaluation and
  banking crisis transmission channels not captured by this entry. DIRECTION verdict may be
  more reliable than MAGNITUDE for these entities."
- Bolivia and Peru (fiscal consolidation episodes) are the better-fit cases for this calibration.

---

## 3. Chosen Calibration

### 3.1 Calibration path

**LAC Q1 FORMAL, AGE_25_54 — primary calibration:**
GDP growth change → `poverty_headcount_ratio` change for LAC Q1 formal sector workers

- **Point estimate:** `elasticity = Decimal("-0.22")`, `entity_families = frozenset({"ARG", "ECU", "BOL", "PER"})`
- **Uncertainty range:** −0.15 to −0.30 (Lustig 2014 CEQ Q1 formal range; concentration
  factor 1.4–1.8× from Gasparini & Lustig 2011; dampened lower from financial-crisis-only
  high-end estimates for ARG/ECU)
- **Confidence tier:** T3 (regional LAC inference; not country-specific backtested)
  T2 upgrade requires country-specific backtesting in Bolivia or Peru fiscal consolidation
  episodes (not in scope for M19)
- **Why -0.22 vs GRC -0.25:** (1) Lower formal-sector concentration factor in LAC vs Euro area
  (1.6× vs 2×); (2) T3 confidence vs T2; (3) Fiscal-conservative basis is appropriate given
  documented mismatch for ARG/ECU financial-crisis episodes.

**LAC Q2 FORMAL, AGE_25_54 — secondary calibration:**
- **Point estimate:** `elasticity = Decimal("-0.13")`, `entity_families = frozenset({"ARG", "ECU", "BOL", "PER"})`
- **Derivation:** 0.60 × (-0.22) = -0.132 → round to -0.13 (Ball et al. 2013 scaling)
- **Uncertainty range:** −0.09 to −0.18
- **Confidence tier:** T3

### 3.2 What is NOT calibrated in CM Sprint B

- **LAC Q1 INFORMAL override:** SSA Q1 INFORMAL entry (entity_families=None) continues to
  fire on LAC entities at -0.20 (the SSA-calibrated value, which is approximately 2× the
  Lustig 2017 LAC baseline). This is an accepted overestimate — see §1.2 Option (a) rationale.
  A future sprint could add LAC Q1 INFORMAL at -0.10 with an exclusion mechanism.

- **ARG/ECU currency-crisis transmission:** The devaluation and bank-freeze channels are
  not modelled by this entry. ADR-020 Channel C (credit_contraction_labour_shock) provides
  partial coverage. Full financial-crisis calibration is deferred.

- **BOL/PER individual calibration:** The frozenset includes all four entities using the
  same constants. Bolivia and Peru may warrant individually calibrated entries after
  country-specific backtesting fixtures are created (beyond M19).

### 3.3 Scoping

| Entry | entity_families | SSA Q1 INFORMAL also fires? |
|---|---|---|
| LAC Q1 FORMAL (new) | `frozenset({"ARG","ECU","BOL","PER"})` | Yes — different cohort, no conflict |
| LAC Q2 FORMAL (new) | `frozenset({"ARG","ECU","BOL","PER"})` | Yes — different cohort, no conflict |
| SSA Q1 INFORMAL | `None` (unchanged) | Yes — fires on LAC Q1 INFORMAL cohort |

---

## 4. MAGNITUDE Acceptance Criterion

### 4.1 Test assertion specification

**Primary assertion (AC-1) — `hd_composite` divergence at step 3 (Argentina Type B):**

```python
# Heterodox path better: hd_composite divergence (heterodox - orthodox) at step 2 (index 2)
# Step 3 = mid-crisis year (2002 in ARG fixture, GDP decline at maximum)
lower_bound = Decimal("0.003")   # 0.3pp HD composite — minimum calibrated response
upper_bound = Decimal("0.050")   # 5.0pp HD composite — cap against overfit
```

**Rationale for lower_bound = 0.003:**
- ARG orthodox fiscal path vs heterodox: differential fiscal adjustment ~2-3pp primary surplus
- At MacroeconomicModule default multiplier ~0.5: ~1-1.5pp GDP growth differential per step
- At Q1 FORMAL elasticity -0.22: ~0.22-0.33pp poverty_headcount_ratio change per cohort per step
- hd_composite scale normalization: Q1 FORMAL contribution ~0.003-0.008 per step
- Lower bound 0.003 is achievable and represents a genuinely detectable divergence

**Rationale for upper_bound = 0.050:**
- At step 3, cumulative HD divergence for a 2-3pp fiscal differential should not exceed 5pp
  hd_composite for a formal-sector T3 calibration — a 5pp+ divergence would suggest overfit

### 4.2 Non-regression assertion specification

The existing entries must be unchanged:

```python
# SSA entries
EXPECTED_SSA_Q1_INFORMAL = Decimal("-0.20")
EXPECTED_SSA_Q2_INFORMAL = Decimal("-0.133")
EXPECTED_SSA_Q1_AGRI = Decimal("-0.16")
EXPECTED_CHANNEL_C = Decimal("-0.30")
# GRC entries (CM Sprint A)
EXPECTED_GRC_Q1_FORMAL = Decimal("-0.25")
EXPECTED_GRC_Q2_FORMAL = Decimal("-0.15")
```

### 4.3 Cross-contamination guard

```python
# LAC entries must not fire on SSA or GRC entities
for entity_id in ("SEN", "ZMB", "GHA", "GRC"):
    lac_firing = [
        e for e in ELASTICITY_REGISTRY
        if e.entity_families is not None and entity_id in e.entity_families
        and e.elasticity in (Decimal("-0.22"), Decimal("-0.13"))
    ]
    assert len(lac_firing) == 0
```

---

## 5. Source Registry IDs

| source_registry_id | Source | Status |
|---|---|---|
| `ACADEMIC_LITERATURE_LUSTIG_2014_CEQ_LAC_POVERTY` | Lustig, Pessino, Scott (2014) CEQ WP/13 | New — must be added |
| `ACADEMIC_LITERATURE_GASPARINI_LUSTIG_2011_LAC_INEQUALITY` | Gasparini & Lustig (2011) OUP | New — must be added |
| `ACADEMIC_LITERATURE_BALL_2013_FISCAL_CONSOLIDATION` | Ball et al. (2013) IMF WP/13/151 | Registered (M17-G1) |

Both new source registry IDs must be added to `source_registry` in the same PR as the
implementation. The `source_registry` table is in the database seed; verify the naming
convention matches `DATA_STANDARDS.md §Data Provenance Requirements`.

---

## 6. Issue #1657 Coordination

Same note as CM Sprint A: #1657 implementation PR may open while CM Sprint B is active.
The `entity_families` field is already available. CM Sprint B entries follow the same
pattern as Sprint A entries; no coordination issue is expected. If #1657 modifies
`module.py` (adding elasticity entries for dead event types), that is a different file
from `elasticities.py` and the PRs do not conflict.

---

*Calibration decision document authority: sprint entry §2.4 PENDING gate.
Sprint entry: `docs/process/sprint-plans/m19-cm-b-sprint-entry.md` (EL-approved 2026-07-03).
This document gates: (1) test authorship, (2) implementation PR opening.
Author: Chief Methodologist. Date: 2026-07-03.*
