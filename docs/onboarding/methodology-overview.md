# Methodology Overview

> **Purpose:** This guide explains what WorldSim models, how it models it,
> and — equally important — what it does not model and why. Understanding
> the model's boundaries is a prerequisite for using its outputs correctly.

---

## What This Simulation Is

WorldSim is a **structured reasoning tool**, not a prediction engine. This
distinction matters for how you use the outputs.

A prediction engine attempts to forecast what *will* happen. WorldSim does
not do this. Instead, it shows you what *would* happen — given a specific
set of starting conditions and parameter choices — if the modeled relationships
hold. The simulation is a way to reason through policy trajectories before they
are executed, not a way to remove uncertainty about the future.

**Outputs are distributions over scenarios, not point forecasts.** When the
simulation shows a reserve coverage trajectory, it is showing what the model
produces under the configured assumptions. The confidence tier system
(T1–T5) tells you how well-grounded those assumptions are in historical data.
A T3 output is a model estimate, not a measurement.

---

## What the Model Covers

WorldSim models sovereign governance across four measurement framework axes,
all active simultaneously:

**Financial framework:**
GDP, fiscal balance, external reserves, debt service coverage, current account,
exchange rate dynamics under capital flow shocks. Fiscal multipliers are
regime-dependent: the standard multiplier (0.8) applies in healthy conditions;
an elevated multiplier (1.5) applies when unemployment exceeds 15%, consistent
with post-2008 evidence on fiscal multiplier heterogeneity.

**Human development framework:**
HDI-adjacent indicators disaggregated by demographic cohort — income quintile,
age band, and employment sector. Distributional effects of policy shocks are
tracked separately from aggregate indicators. A fiscal consolidation that
improves the headline fiscal balance while worsening outcomes for the bottom
income quintile will show both effects simultaneously.

**Ecological framework:**
Planetary boundary proximity scoring against CO2 concentration (Rockström 2009,
350 ppm boundary) and land-use pressure (Richardson 2023 boundaries). Ecological
outputs feed into the sovereign risk computation when ecological degradation
affects agricultural output or water security — a channel frequently absent
from IMF debt sustainability analyses.

**Governance framework:**
Institutional capacity indicators derived from V-Dem data. Programme survival
probability, legitimacy dynamics, and elite capture coefficient are modeled
through the PoliticalEconomyModule when enabled. These variables capture the
political feasibility constraint on economic programmes — the question of
whether a technically sound programme can survive its implementation environment.

**MDA threshold system:**
Hard floors (Minimum Descent Altitudes) define irreversible thresholds for
key indicators. When an indicator crosses its MDA floor, the simulation fires
a WARNING, CRITICAL, or TERMINAL alert. The simulation does not recommend any
pathway that crosses below an MDA floor.

---

## What This Model Does Not Claim

### Known Model Boundaries and Blindspots

The following limitations are documented characteristics of the current model,
not temporary gaps waiting to be filled. Using WorldSim outputs without
understanding these boundaries risks drawing conclusions the model cannot
support.

**Ecological-to-financial transmission pathways are not fully modeled.**
The current ecological module tracks boundary proximity and land-use pressure
but does not model the transmission mechanisms from ecological degradation to
financial indicators — how a prolonged drought affects agricultural export
revenue, or how coastal flooding affects property values and banking sector
exposure. These pathways matter for small open economies where natural capital
is a primary export. Users analyzing small island states or arid-economy
entities should treat ecological and financial outputs as parallel tracks
rather than fully integrated projections.

**Political feasibility at sub-national and factional levels is not captured.**
The PoliticalEconomyModule models aggregate programme survival probability and
legitimacy dynamics at the sovereign level. It does not model sub-national
political dynamics — regional separatist pressures, factional splits within
governing coalitions, or differential programme support across geographic
regions. A programme that is feasible in the aggregate can collapse due to a
regional political constraint the model does not see.

**Informal economy dynamics are absent from sovereign financial indicators.**
All monetary and fiscal indicators in the financial module are based on official
statistics. In economies where the informal sector constitutes 30–60% of
economic activity (common across Sub-Saharan Africa and parts of Latin America
and South Asia), the official indicators capture a subset of the actual economy.
Fiscal multiplier estimates calibrated on formal-sector dynamics may overstate
or understate actual effects in high-informality contexts.

**Intra-household distributional effects are not disaggregated below cohort
level.**
The human development module disaggregates by income quintile, age band, and
employment sector. It does not disaggregate by gender, household type, or
disability status within those cohorts. A fiscal shock that disproportionately
affects women's labor force participation — a documented pattern in austerity
programmes — appears in the model as a uniform cohort effect.

**Bilateral debt opacity is treated as a data gap, not a model gap.**
Chinese bilateral lending to sovereign borrowers is frequently non-public.
The simulation handles missing bilateral debt data as a Structural Absence
Declaration — the absence is declared, with a note that the data structure
exists but the values are not observable. This is methodologically honest but
means that debt sustainability analyses for economies with significant opaque
bilateral debt (several African sovereigns) are working from an incomplete
picture the model cannot resolve.

**Financial contagion and cross-border spillover channels are not modeled.**
The simulation models single-entity scenarios. Contagion dynamics — how a
sovereign default in one country triggers capital outflows in another, or how
a currency crisis propagates through a regional currency union — are outside
the current scope. Multi-entity scenario support (comparing two entities on
the same choropleth) exists but does not model interdependence between them.

---

## Backtesting as Epistemic Standard

Every model relationship in WorldSim is validated against historical cases
before being used for forward projection. The gap between model prediction and
historical outcome is not a failure — it is the primary signal for improvement.

**Current validated cases:**

| Case | Period | Status | Calibration level |
|---|---|---|---|
| Greece 2010–2015 | 5-year fiscal adjustment | Validated | DIRECTION_ONLY (most indicators); fiscal multiplier frame |
| Argentina 2001–2002 | Zero Deficit Plan + default | Validated | MAGNITUDE (year 1: −10.55% vs. −10.9% historical) |
| Jordan 2023 | Current state seeding | Data quality validated | T2 initial state; forward projection T3–T4 |

Cases with DIRECTION_ONLY calibration status mean the model correctly
predicts whether an indicator improves or worsens, but the magnitude of the
change has not been validated against measured historical outcomes. Citing
specific magnitudes from DIRECTION_ONLY-calibrated outputs in a negotiating
context requires disclosing the calibration status.

---

## How to Read the Calibration Status

**MAGNITUDE:** The model's predicted value was within a documented tolerance of
the actual historical value at the validation step. These outputs can be cited
with their confidence tiers.

**DIRECTION_ONLY:** The model correctly predicts the direction of change but the
magnitude has not been validated. Use for directional arguments; do not cite
specific values as predictions.

**UNVALIDATED:** The indicator is modeled but has not been backtested. This
appears for new indicators added without a complete backtesting case. Treat
these as model-internal estimates, not validated outputs.

---

## Uncertainty Quantification

WorldSim does not suppress uncertainty — it quantifies and displays it.

**Confidence tier system (T1–T5):** See the [Data Provenance Guide](data-provenance.md)
for the full tier specification. A lower tier number means better-grounded data;
a higher number means more uncertainty. Tiers degrade automatically when:
- Forward projection extends beyond the data coverage window
- Synthetic methods are used to fill gaps
- Multiple inputs are combined (tier propagation takes the maximum, not minimum)

**When uncertainty is too large to produce a meaningful output:**
If the uncertainty band for a key indicator is so wide that it spans the full
feasible range — directionally meaningless — the simulation will declare a
Structural Absence rather than generate an uninterpretable band. A model that
says "we cannot compute this" is more useful than one that produces a number
that cannot support any conclusion.

---

## What the Simulation Is Not

- **Not a recommendation engine.** WorldSim does not recommend a policy path.
  It shows what different paths imply. The decision is the user's.
- **Not a substitute for domain expertise.** A simulation that produces
  plausible numbers does not validate the assumptions that generated them.
  Domain expertise — a debt analyst who knows the Jordan case, a development
  economist who knows the distributional dynamics in Zambia — is the check on
  model assumptions.
- **Not evidence that a crisis is inevitable.** A TERMINAL alert means the
  current trajectory reaches an irreversible threshold; it does not mean the
  trajectory cannot be changed. Mode 3 Active Control exists to show what
  different policy choices imply.

---

*For technical methodology details, see [`docs/methodology/`](../methodology/)
and the relevant Architecture Decision Records in [`docs/adr/`](../adr/).
The calibration basis for each backtesting case is in
[`docs/methodology/calibration-basis.md`](../methodology/calibration-basis.md).*
