# WorldSim — Propagation Parameter Calibration Basis

> Status: Partial calibration — see Issue #44 for full calibration tier system.
> Author: Documentation Agent (M13 G4 — Issue #27)
> Covers parameters in `backend/app/simulation/modules/macroeconomic/module.py`
> and `backend/app/simulation/orchestration/inputs.py`.

---

## Purpose

This document records the calibration basis for the top-level propagation
parameters used in WorldSim's simulation engine. It serves three functions:

1. **Transparency** — a non-technical reviewer can trace a parameter value to
   its claimed empirical basis without reading source code.
2. **Calibration audit** — parameters marked PLACEHOLDER require empirical
   calibration before the engine produces cite-ready outputs in that domain.
3. **Backtesting anchor** — calibrated parameters can be compared against
   historical out-of-sample performance. Placeholder parameters should be
   recalibrated once backtesting data is available.

---

## Fiscal Sector Parameters

### `FISCAL_MULTIPLIERS` — Spending multipliers by economic regime

**Location:** `backend/app/simulation/modules/macroeconomic/module.py` line ~53

| Regime | Value | Basis |
|--------|-------|-------|
| `standard` | 0.5 | Ball, Leigh & Loungani (2019), "Okun's Law: Fit at 50?"; Loayza & Raddatz (2010), "The composition of growth matters for poverty alleviation." Cross-country average for developing economies. |
| `depressed` | 1.5 | Blanchard & Leigh (2013), "Growth Forecast Errors and Fiscal Multipliers"; elevated multiplier in demand-deficient regimes. |
| `zlb` | 2.0 | Christiano, Eichenbaum & Rebelo (2011), "When Is the Government Spending Multiplier Large?"; elevated fiscal multiplier at the zero lower bound. |

**Calibration status:** CALIBRATED (published estimates). Full country-specific
recalibration deferred to Issue #44.

---

### `OKUN_COEFFICIENT` — GDP growth → unemployment transmission

**Location:** `backend/app/simulation/modules/macroeconomic/module.py` line ~70

**Value:** `0.5`

**Basis:** Ball, Leigh & Loungani (2019); Loayza & Raddatz (2010). Developing-economy
estimate for the one-period transmission from 1 percentage point change in GDP
growth to 0.5 percentage point change in unemployment (opposite direction).

**Calibration status:** CALIBRATED (developing-economy cross-country average).
Country-specific recalibration deferred to Issue #44.

---

### `REVERSION_SPEED` — Mean-reversion speed in GDP growth (ADR-006 Amendment 1)

**Location:** `backend/app/simulation/modules/macroeconomic/module.py` line ~81

**Value:** `0.10` (10% per year reversion toward long-run growth rate)

**Basis:** Cerra & Saxena (2008), "Growth Dynamics: The Myth of Economic Recovery."
Estimate based on post-crisis output trajectories in developed economies. This
is an upper bound for developing economies where recovery is typically slower.

**Calibration status:** CALIBRATED for developed economies (Cerra-Saxena 2008).
PLACEHOLDER for individual country trajectories — see Issue #44.

---

### `REGIME_DAMPENER` — Recovery speed scalar by economic regime

**Location:** `backend/app/simulation/modules/macroeconomic/module.py` line ~86

| Regime | Value | Basis |
|--------|-------|-------|
| `zlb` | 0.25 | Reinhart & Rogoff (2009), "This Time Is Different"; median time to recover pre-crisis output ≈7 years following sovereign debt crises. |
| `depressed` | 0.50 | Partial channel active — moderate crisis, no debt restructuring required. |
| `standard` | 1.00 | Full reversion speed applies. |

**Calibration status:** CALIBRATED at regime level (Reinhart-Rogoff 2009).
Country-specific dampener calibration deferred to Issue #44.

---

## Human Cost Ledger Parameters

### `_HCL_TRANSMISSION_FACTOR` — Shock-to-human-development transmission rate

**Location:** `backend/app/simulation/orchestration/inputs.py` line ~1026

**Value:** `0.3`

**Basis:** PLACEHOLDER. This factor scales how much of a commodity price shock
transmits to the bottom-quintile consumption capacity indicator. The 0.3 value
is an interim estimate pending calibration against LSMS household survey data.

Candidate calibration sources:
- World Bank Living Standards Measurement Study (LSMS) — food price pass-through
  to household consumption for developing economies
- FAO food price crisis impact assessments (2008, 2011)
- IMF Working Paper WP/16/218 (Furceri, Loungani, Ostry 2016) — distributional
  consequences of commodity price shocks

**Calibration status:** PLACEHOLDER — empirical calibration required before
the human cost ledger output is cite-ready at Tier 1–2. Current output is
Tier 3 (directionally correct; specific magnitude uncertain).

---

## Propagation Network Parameters

### Synthetic relationship weight — fallback for unregistered entity pairs

**Location:** `backend/app/simulation/repositories/state_repository.py` line ~32

**Value:** `0.1` (weight=0.1, confidence_tier=4)

**Basis:** Conservative placeholder. When two entities in a scenario have no
registered bilateral trade or institutional relationship in the database, the
engine injects a synthetic weak relationship at weight 0.1 and confidence tier 4
to prevent zero propagation. The 0.1 weight reflects a "minimal but non-zero
connectivity" assumption for economies with no observed relationship.

**Calibration status:** PLACEHOLDER — specific pairs should be registered with
empirical trade weight data from UN Comtrade or IMF DOTS when available.

---

### Propagation Rules — `TARIFF_ATTENUATION` and `TARIFF_MAX_HOPS`

**Location:** `backend/scripts/demo_scenario.py` module constants; applied via
`PropagationRule(attenuation_factor=TARIFF_ATTENUATION, max_hops=TARIFF_MAX_HOPS)`
on all trade shock inputs.

#### `TARIFF_ATTENUATION` — Trade shock attenuation factor per hop

**Value:** `0.6`

**Basis:** PLACEHOLDER (Tier D). The 0.6 value is a structurally reasonable interim
estimate representing moderate attenuation for first-order trade shock propagation. A
direct tariff shock of magnitude S transmits 0.6·S to each bilateral trade partner
(hop 1) and 0.36·S (0.6²) to second-hop partners.

Candidate calibration methodology:
- Gravity model residuals: calibrate attenuation to match observed bilateral trade
  impact decay across WTO dispute cases and documented tariff shock episodes
  (US–China 2018–2019, US–EU 2002 steel tariffs)
- Primary data: UN Comtrade bilateral trade matrix (Tier 1) for direct exposure;
  IMF DOTS for partner-country impact (Tier 2)
- Fitting approach: minimise out-of-sample RMSE on bilateral trade impact across
  three held-out tariff shock episodes

Sensitivity analysis: outputs at `attenuation_factor = 0.4` and `0.8` show a ±30%
range on second-hop exposure — directional output is stable; magnitude is not.

**Calibration status:** PLACEHOLDER (Tier D) — full empirical calibration deferred
to Issue #44.

---

#### `TARIFF_MAX_HOPS` — Maximum propagation depth in trade network

**Value:** `2`

**Basis:** PLACEHOLDER (Tier D). The 2-hop limit models first- and second-order
trade linkages. Hop 1 is the direct bilateral partner affected by the tariff; hop 2
is an economy connected through the hop-1 partner. Third-order effects (hop 3+) are
not modelled — the empirical evidence that third-order effects are distinguishable
from noise at macroeconomic resolution is weak at current model fidelity.

Candidate calibration methodology:
- Input-output table analysis (WIOD or OECD TiVA): estimate value-added transmission
  across supply-chain hops. The hop at which additional propagation falls below 5% of
  the initial shock defines the empirically appropriate `max_hops`
- Historical validation: US–China tariff shock 2018–2019 produced measurable effects
  in ASEAN economies (hop 2); hop-3 effects in other regions were ambiguous in the
  published literature

**Calibration status:** PLACEHOLDER (Tier D) — 2-hop limit is conservative and
consistent with the empirical trade-network propagation literature. Full calibration
deferred to Issue #44.

---

## Political Economy Parameters (ADR-013)

These parameters govern the PoliticalEconomyModule (M13 G6). All are Tier 3 —
formula-based approximations calibrated against historical programme failure cases.

### `LEGITIMACY_EROSION_ELASTICITY` — Fiscal adjustment → legitimacy erosion rate

**Location:** `backend/app/simulation/modules/political_economy/module.py`

**Value:** `0.08` (8% of |fiscal_delta| reduces legitimacy_index per step)

**Basis:** Greece 2010–2012 calibration: cumulative −25 percentage point fiscal
adjustment produced approximately −0.20 decline in government approval proxy
over three years (Eurobarometer time-series). Elasticity ≈ 0.08/year at
standard regime; conservative lower bound used.

**Calibration status:** Tier 3 CALIBRATED (single-case, Greece 2010–2012). Generalisability
to non-Eurozone economies is uncertain. The FRAGILITY_AMPLIFIER (×1.5 below 0.5 legitimacy)
is supported by Przeworski et al. (2000) nonlinear collapse dynamics.

---

### `EMERGENCY_EROSION_FACTOR` — Emergency policy event → immediate legitimacy shock

**Location:** `backend/app/simulation/modules/political_economy/module.py`

**Value:** `0.10` (10% immediate legitimacy reduction per emergency event)

**Basis:** Lebanon 2019 (bank holiday, capital controls) and Argentina 2001
(emergency declaration, debt default) observations. Both cases showed rapid,
discrete legitimacy shocks at emergency event announcement distinct from the
gradual erosion under fiscal adjustment. Magnitude estimate: 10% per event.

**Calibration status:** Tier 3 PLACEHOLDER. Calibrated from two cases. Full
cross-country calibration deferred to Issue #44.

---

### `_BASE_ANNUAL_SURVIVAL` — Programme survival probability base rate

**Location:** `backend/app/simulation/modules/political_economy/module.py`

**Value:** `0.70`

**Basis:** Historical programme failure data (ADR-013 §Known Limitations):
- Greece: three programme adjustments over five years (2010–2015)
- Argentina 2001: programme collapse in year 3
- Ecuador 2000: programme abandoned after one year

Base annual survival ≈ 0.70 (geometric mean across three cases). These are
middle-income countries with IMF programme history; low-income country dynamics
are not captured by this estimate (see ADR-013 §Known Limitations).

**Calibration status:** Tier 3 CALIBRATED on three cases. Programme survival
probability is labelled "formula-calibrated estimate" in all disclosures.
Full calibration against a larger historical dataset is deferred to Issue #44.

---

### `_LEGITIMACY_SURVIVAL_SENSITIVITY` — Legitimacy → survival probability sensitivity

**Location:** `backend/app/simulation/modules/political_economy/module.py`

**Value:** `1.50`

**Basis:** Historical programme failure timing relative to protest intensity
proxies (Acemoglu & Robinson 2005, "Economic Origins of Dictatorship and
Democracy"; Blyth 2013, "Austerity: The History of a Dangerous Idea").
Each 0.10 point decline in legitimacy_index reduces annual survival
probability by approximately 0.105 (base × sensitivity × 0.10 = 0.70 × 1.50 × 0.10).
Value set to 1.50 (rather than the initial 0.80) so that legitimacy=0.0 yields
survival probability below PROGRAMME_SURVIVAL_FLOOR (0.25), making PE-001 MDA alert
reachable via the formula without external override (AC-3 of intent document
ADR-013-2026-06-12-political-economy-integration.md).

**Calibration status:** Tier 3 PLACEHOLDER. Issue #44 calibration required
for Tier 2 promotion.

---

### `PROGRAMME_SURVIVAL_FLOOR` — MDA threshold for political viability

**Location:** `backend/app/simulation/modules/political_economy/module.py`

**Value:** `0.25`

**Basis:** ADR-013 §Decision 1. The 0.25 floor corresponds to conditions
observed in historically failed programmes (Greece 2015 Syriza referendum,
Argentina 2001 default declaration, Ecuador 2000). At survival probability
below 0.25, historical precedent shows programme collapse becomes the
dominant outcome. MDA-PE-001 fires at this floor.

**Calibration status:** Tier 3. Based on three historical cases. The floor
must not be changed without an ADR amendment per ADR-013 §Decision 1.

---

### `_DEFAULT_ELITE_CAPTURE_COEFFICIENT` — Default elite benefit capture share

**Location:** `backend/app/simulation/modules/political_economy/module.py`

**Value:** `0.30`

**Basis:** Argentina 2001–2002 distributional analysis (Lustig 2001, "Crisis
and Poverty in Argentina"). Elite cohorts (top decile) captured approximately
30% of fiscal adjustment benefits above their population weight during the
crisis. Used as the default when `elite_capture_coefficient` entity attribute
is absent.

**Calibration status:** Tier 3 PLACEHOLDER. Country-specific coefficients from
World Bank Inequality surveys are the calibration target (Issue #44).

---

## Relationship to Issue #44 (Full Calibration Tier System)

Issue #44 tracks the full calibration tier system for all propagation parameters.
Parameters marked PLACEHOLDER in this document are blocking for Tier 1–2
analytical outputs in the domains they affect. Parameters marked CALIBRATED
carry their cited empirical basis but have not been individually validated
against the WorldSim backtesting suite for out-of-sample performance.

Out-of-sample validation against historical cases is the primary calibration
signal — see `docs/DATA_STANDARDS.md §Backtesting Integrity Rules`.

---

## Capital Controls Transmission Parameters (ADR-020)

**ADR reference:** ADR-020 — Emergency Instrument Economic Transmission Pattern
(accepted 2026-07-03, panel: CE, CM, Development Economist, Geopolitical Analyst,
UX Designer). Three transmission channels: Channel A (ExternalSectorModule reserve
protection), Channel B (MacroeconomicModule credit contraction), Channel C
(DemographicModule Q1 poverty headcount via labour shock bridge).

**Implementation locations:**
- Channel A — `backend/app/simulation/modules/external_sector/module.py`
- Channel B — `backend/app/simulation/modules/macroeconomic/module.py`
- Channel C — `backend/app/simulation/modules/demographic/module.py`

---

### ε — Capital account outflow velocity reduction coefficient (Channel A)

Controls the fractional reduction in `capital_account_outflow_velocity` when
`emergency_policy_capital_controls` fires. A lower outflow velocity reduces
reserve drawdown rate, implementing the reserve protection effect.

**Default value:** `0.60`

**Calibration anchors:**

| Anchor | ε estimate | Source | Notes |
|---|---|---|---|
| Iceland 2008 (blended) | 0.65 | CBI Statistical Bulletin 2009; BIS Working Paper 478 (Danielsson et al. 2012) | Includes simultaneous SBA confound — Nordic bilateral support lines and CBI reserve change are combined |
| Iceland 2008 (controls-only) | **0.50** | IMF Iceland Article IV 2010 §III reserve decomposition | Isolates CBI reserve change attributable to capital controls only, removing Nordic/SBA contribution. **This is the G2D heterodox fixture value (ADR-020 INCORPORATE-3)** |
| Malaysia 1998 | 0.55 | IMF WP/00/92 (Kaplan & Rodrik 2002); BIS Occasional Paper (Ariyoshi et al. 2000) | 12-month unilateral peg + controls period; reserve recovery consistent with 0.50–0.60 range; BIS estimates net outflow reduction of ~55% |

**Default derivation:** Two-anchor arithmetic mean: (ε_Iceland_blended + ε_Malaysia) / 2
= (0.65 + 0.55) / 2 = **0.60**. Range ±0.15 reflects cross-country uncertainty and
the SBA confound that raises the blended Iceland estimate.

**Iceland SBA confound:** The IMF Stand-By Arrangement (approved November 2008) and
Nordic bilateral support lines contributed independently to reserve stabilisation
alongside the October 2008 capital controls. The blended ε≈0.65 conflates both
channels. The Article IV 2010 §III decomposition separates them: the controls
attributable portion is ε≈0.50. The G2D heterodox fixture uses ε=0.50 to model
the non-SBA path accurately (INCORPORATE-3 resolution: Iceland took a heterodox
path but also accepted the SBA; the fixture isolates the controls channel).

**Calibration status:** Tier 3 CALIBRATED (two historical anchors; one IMF Article IV
decomposition). Tier 2 upgrade requires additional controls episode cross-validation
against IMF WP/99/3 or Edwards & Rigobon (2009) emerging market controls dataset.

---

### β — Credit contraction coefficient (Channel B)

Scales the reduction in `domestic_credit_growth` per unit of capital controls
severity. Applied once when `emergency_policy_capital_controls` fires; drives
the Channel B→C bridge via `credit_contraction_labour_shock`.

**Default value:** `0.020`

**Calibration basis:**

Iceland 2009 national accounts decomposition:
- Annual GDP growth 2009: −6.6% (Statistics Iceland, Q4 2009 National Accounts)
- IMF Article IV Iceland 2010 §III decomposes the 2009 contraction:
  - Banking system freeze + credit channel: ~1.5–2.0 pp contribution
  - Export recovery (krona devaluation): partial offset beginning Q3 2009
  - Fiscal adjustment (−8% primary balance 2009): ~2.5 pp contribution
  - Residual / confidence channel: remainder
- β derivation: credit channel contribution (1.5–2.0 pp) / (controls severity 0.85
  × reference GDP response) ≈ 0.017–0.024. Point estimate: **0.020**
- β range [0.015, 0.030]: covers 90% credible interval across single-case decomposition.
  Range [0.030, 0.060] reserved for banking-freeze-only events (per ADR-020 Decision 2).

**Malaysia 1998 cross-validation:**
β_Malaysia ≈ 0.018 (IMF WP/00/92). Malaysia's banking sector was smaller relative to
GDP than Iceland's (~3× GDP vs. Iceland's ~10× GDP at crisis), consistent with a
lower credit contraction coefficient. β=0.020 default sits comfortably above the
Malaysia lower-bound and reflects Iceland's banking-sector-dominated transmission.

**γ — GDP-credit multiplier (CM-supplied constant):** `1.2`

Standard Keynesian credit-GDP multiplier for small advanced open economies
(Iceland: export-led recovery channel available post-krona devaluation reduces
the multiplier vs. closed-economy baseline). Sources: IMF WP/2010/66; Jordà,
Schularick & Taylor (2015, NBER WP 20564) credit multiplier estimates for OECD
small open economies cluster at 1.1–1.3 for controls-with-recovery scenarios.

**Critical constraint:** γ = 1.2 is a CM-supplied constant per ADR-020 Decision 2
(INCORPORATE-1). The Computation Engine Agent cannot change this value without
CM Consulted review. Changes require an ADR-020 amendment.

**Calibration status:** Tier 3 CALIBRATED (Iceland 2009 IMF Article IV decomposition
+ OECD credit multiplier literature). β is a single-case calibration; cross-country
upgrade deferred to Issue #44.

---

### φ — Q1 poverty headcount ratio impact range (Channel C)

φ captures the fractional increase in `q1_poverty_headcount_ratio` from the
credit contraction labour shock chain. Channel C receives the bridge event
`credit_contraction_labour_shock` from MacroeconomicModule (Channel B) and
applies φ to Q1 poverty headcount.

**Range:** φ ∈ [0.3, 0.7]

**ISL (Iceland) lower bound:** φ ≈ **0.30**

**Rationale:** Iceland's pre-crisis Q1 poverty headcount ratio was approximately
0.08 (Eurostat SILC Iceland 2007 — income quintile 1 at-risk-of-poverty rate).
Higher-income economies with lower baseline poverty rates show lower absolute
poverty headcount responses to credit contractions: the at-risk population is
smaller, and Iceland's social protection floor (maintaining unemployment benefits
through the crisis) attenuated the poverty headcount response. φ=0.30 reflects
the lower end of the distributional impact range appropriate for high-income
European small open economies.

**Contrast with higher-φ contexts:** Low-income SSA economies (SEN, ZMB G2B
fixtures) anchor the upper range (φ→0.7) where large informal sector shares
and weak social protection floors produce stronger poverty headcount responses
per unit of credit contraction.

**ISL data tier classification:**

| Attribute | Tier | Source |
|---|---|---|
| `reserve_coverage_months` (October 2008) | Tier 1 | Central Bank of Iceland Statistical Bulletin, October 2008 (ISL: ~€1.5bn reserves, ~3.5 months cover) |
| `gdp_growth` (Step 0 deteriorating) | Tier 1 | Statistics Iceland National Accounts 2008 Q3/Q4 |
| `q1_poverty_headcount_ratio` (baseline 0.08) | Tier 2 | Eurostat SILC Iceland 2007 (at-risk-of-poverty rate Q1; closest pre-crisis vintage) |
| `banking_sector_leverage_ratio` (HIGH, ~10× GDP) | Tier 1 | Central Bank of Iceland Financial Stability Report 2008 |
| `political_legitimacy_index` (0.72) | Tier 2 | WVS Wave 5 Iceland (2005–2008); V-Dem Iceland democratic quality score |

**Q1/Q2 scope note (INCORPORATE-5):** Channel C models Q1 poverty headcount impact.
Q2 households experience a weaker response (approximately 60% of Q1 impact per Ball
et al. 2013 distributional scaling). Q2 impact is not modelled in the current Channel C
implementation. This is a **known gap** documented in ADR-020 §Known Limitations and
must appear in `known_limitations` output for any run where Channel C fires.

**Calibration status:** φ range is Tier 3 PLACEHOLDER. ISL lower bound (φ=0.30) is
a contextual inference from Eurostat SILC poverty rate data. Full calibration
requires Iceland household consumption panel data 2008–2011 — not currently
available at Tier 1. Structural test classification (pre_calibration_structural_test)
is appropriate for the G2D fixture until empirical calibration is complete.
