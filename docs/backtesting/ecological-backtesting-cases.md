# Ecological Backtesting Case Planning

> **Status:** Planning document — implementation deferred to post-M12 sprint (see Issue #95)
> **Origin:** ARCH-REVIEW-002 Finding BI2-N-04 (Ecological Economist Agent)
> **Purpose:** Define candidate historical cases where ecological dynamics are central
> and well-documented, so that the ecological framework has testable fidelity thresholds
> in at least one backtesting run before the framework is considered validated.
> **Related ADR:** ADR-005 (Ecological Module); `docs/architecture/reviews/ARCH-REVIEW-002-milestone2.md`

---

## Why This Document Exists

The Greece 2010–2012 backtesting case — the first empirical validation of WorldSim —
tests only financial indicators. No ecological attributes appear in the initial state
fixture, and no ecological fidelity thresholds appear in `backtesting_runs`. The
risk identified in ARCH-REVIEW-002 (Finding BI2-N-04) is that a backtesting case
template without ecological dimensions produces descendants without ecological
dimensions. The ecological framework remains perpetually unvalidated by default.

This document identifies three candidate cases and specifies — for each — the data
sources, initial state ecological attributes, fidelity thresholds, and ControlInput
sequence that would constitute a well-formed ecological backtesting case. One of
these cases must be implemented as an ecological validation run before the
simulation's backtesting suite can be described as multi-framework.

---

## Case 1 — Brazil Amazon Deforestation and GDP Impact (2000–2010)

### Geography

| Field | Value |
|---|---|
| Entity | Brazil |
| ISO alpha-3 | BRA |
| Level | Nation-state (Level 1) |
| Subnational notes | Deforestation concentrated in Pará, Mato Grosso, Rondônia states; not representable at Level 1 — documented limitation |

### Time Period

**Start:** 2000
**End:** 2010
**Timestep:** Annual
**Steps:** 10
**Crisis threshold:** Peak deforestation rate in 2004 (~27,000 km²/year); Policy Action Plan for the Prevention and Control of Deforestation in the Legal Amazon (PPCDAm) enacted 2004.

### Rationale for Case Selection

The 2000–2010 period contains a measurable policy intervention (PPCDAm 2004) with
a documented deforestation response: annual deforestation fell from ~27,000 km² in
2004 to ~7,000 km² by 2010. GDP continued to grow across the same period. The case
provides a ControlInput sequence (deforestation regulation policy) with an ecological
outcome that moved in the expected direction on a documented timeline. The
agricultural and timber-sector economic feedback loops are partially documented.
The case is long enough (10 steps) to give the backtesting validation statistical
credibility beyond the 2-step Greece case.

### Initial State Parameters (Year 2000)

| Attribute | Value | Source | Tier |
|---|---|---|---|
| `gdp_growth` | 4.4% (2000) | World Bank WDI | Tier 1 |
| `debt_gdp_ratio` | 65.0% (2000) | IMF WEO | Tier 1 |
| `land_use_pressure_index` | 0.72 (estimated from FRA 2000 forest cover vs. safe land-system boundary) | FAO Global Forest Resources Assessment (FRA 2000) | Tier 3 (5-year data; annual interpolation required) |
| `co2_trajectory` | 1.03 Gt CO2/year (2000, land-use change component) | Global Carbon Project CO2 Budget | Tier 1 |
| `co2_concentration_ppm` | 369.5 ppm (2000 global atmospheric) | NASA/NOAA Mauna Loa | Tier 1 |
| `deforestation_rate_km2_yr` | ~19,800 km²/year (2000) | FAO FRA 2000 / INPE PRODES | Tier 2 |
| `agricultural_gdp_share` | 5.6% of GDP (2000) | World Bank WDI | Tier 1 |
| `poverty_headcount_ratio` | 31.6% (2001, $5.50/day line) | World Bank PovcalNet | Tier 2 |

**Confidence tier note:** `land_use_pressure_index` is Tier 3 because FAO FRA data
is published on 5-year cycles. Annual interpolation between FRA 1990, 2000, and 2005
data points introduces synthetic data uncertainty per `docs/DATA_STANDARDS.md §Confidence Tier System`.
The synthetic interpolation must be flagged at indicator level, not session level.

### Data Sources

| Source | Category | License | Access |
|---|---|---|---|
| FAO Global Forest Resources Assessment (FRA 2000, 2005, 2010) | Ecological | CC BY-NC-SA 3.0 IGO | https://www.fao.org/forest-resources-assessment/en/ |
| Global Carbon Project — CO2 Budget Data | Ecological | CC BY 4.0 | https://globalcarbonproject.org/carbonbudget/ |
| NASA/NOAA Mauna Loa CO2 Measurements | Ecological | Public domain (US Gov) | NOAA GML API |
| Stockholm Resilience Centre Planetary Boundary Calibrations | Ecological | CC BY 4.0 | DOI 10.1126/science.abn2458 |
| World Bank WDI | Economic | CC BY 4.0 | https://data.worldbank.org/ |
| IMF World Economic Outlook | Economic | CC BY 4.0 | https://www.imf.org/en/Publications/WEO |
| INPE PRODES deforestation monitoring | Ecological | Public (Brazil gov) | http://www.obt.inpe.br/OBT/assuntos/programas/amazonia/prodes |

All sources above are registered in the `source_registry` or are candidates for
registration before data is loaded. INPE PRODES is not yet in `docs/data-sources/approved-sources.md`
and requires registration before use.

### ControlInput Sequence

| Step (Year) | Input type | Input | Actor |
|---|---|---|---|
| 5 (2004) | `StructuralPolicyInput` | `REGULATORY_CHANGE` — PPCDAm policy activation; deforestation monitoring system, enforcement increase | BRA Ministry of Environment |
| 6 (2005) | `StructuralPolicyInput` | `REGULATORY_CHANGE` — expanded monitoring, Soy Moratorium negotiation | BRA / Industry |
| 7 (2006) | `StructuralPolicyInput` | `REGULATORY_CHANGE` — Soy Moratorium enacted; cattle ranching embargo added | BRA / Industry |

**Conditionality note:** PPCDAm was a sovereign Brazilian policy, not externally
coerced. `InputSource` should be recorded as `DOMESTIC_POLICY`, not
`EXTERNAL_PRESSURE`.

### Fidelity Thresholds

| Step | Attribute | Direction | Threshold type | Calibration tier | Historical basis |
|---|---|---|---|---|---|
| 5 (2004) | `deforestation_rate_km2_yr` | UP (peak before policy) | DIRECTION_ONLY | Tier 3 | INPE PRODES; peak ~27,000 km² |
| 6 (2005) | `deforestation_rate_km2_yr` | DOWN (policy response begins) | DIRECTION_ONLY | Tier 3 | INPE PRODES; drop begins 2005 |
| 10 (2010) | `deforestation_rate_km2_yr` | DOWN (vs. 2000 baseline) | MAGNITUDE ±40% | Tier 3 | INPE PRODES; ~7,000 km² by 2010 |
| 10 (2010) | `co2_trajectory` | DOWN (vs. 2004 peak) | DIRECTION_ONLY | Tier 2 | Global Carbon Project; LUC emissions fell with deforestation |
| 10 (2010) | `gdp_growth` | UP | DIRECTION_ONLY | Tier 1 | World Bank WDI; Brazil maintained positive growth throughout |

**Statistical validity note:** 10 steps, 5 thresholds. This provides substantially
stronger statistical validation than the 2-step Greece case (see ARCH-REVIEW-002
Finding BI2-N-12 / Chief Methodologist). DIRECTION_ONLY thresholds on a 10-year
series with known policy inflection have a false-positive probability significantly
below 25%.

### Evaluation Criteria

1. Simulation produces increasing `deforestation_rate_km2_yr` at step 5 (pre-policy peak)
2. Simulation produces decreasing `deforestation_rate_km2_yr` at steps 6–10 following ControlInput
3. Simulation `co2_trajectory` falls proportionally with deforestation rate reduction
4. GDP growth remains positive (>0%) across all 10 steps
5. `land_use_pressure_index` trends down from year 5 onward
6. No MDA (Minimum Descent Altitude) breach on `land_use_pressure_index` during the run
7. Backtesting pass/fail determination: 4 of 5 fidelity thresholds must be met (80% pass threshold)

---

## Case 2 — Ethiopia Drought and Food Security Crisis (2002–2004)

### Geography

| Field | Value |
|---|---|
| Entity | Ethiopia |
| ISO alpha-3 | ETH |
| Level | Nation-state (Level 1) |
| Subnational notes | Drought most severe in Tigray, Afar, SNNPR; Level 1 averaging masks subnational distribution — documented limitation |

### Time Period

**Start:** 2002
**End:** 2004
**Timestep:** Annual
**Steps:** 3
**Crisis threshold:** 2002–2003 drought affecting approximately 14 million people, requiring emergency food assistance.

### Rationale for Case Selection

The 2002–2004 Ethiopian drought provides a case where an ecological exogenous shock
(rainfall deficit) generates documented fiscal, human development, and governance
consequences on a short, well-bounded timeline. The case tests the simulation's
ability to model ecological-shock-to-economic-impact transmission. It also requires
humanitarian aid ControlInputs from external actors — testing the `EXTERNAL_PRESSURE`
/ multilateral response pathway. The case is deliberately short (3 steps) so that
it can be implemented as a minimal ecological validation run even with limited
data availability.

### Initial State Parameters (Year 2002)

| Attribute | Value | Source | Tier |
|---|---|---|---|
| `gdp_growth` | 1.6% (2002) | World Bank WDI | Tier 1 |
| `agricultural_gdp_share` | 47.0% of GDP (2002) | World Bank WDI | Tier 1 |
| `poverty_headcount_ratio` | 55.3% ($1.90/day, 2000 base year) | World Bank PovcalNet | Tier 2 |
| `rainfall_anomaly_pct` | −35% vs. 1980–2000 mean (2002 Belg season failure) | ERA5 Reanalysis (Copernicus) | Tier 1 |
| `food_production_index` | 82 (FAO FPI, 2002; 2014–2016 = 100 baseline) | FAO FAOSTAT | Tier 2 |
| `aid_dependency_ratio` | 14.8% of GNI (2002) | World Bank WDI | Tier 1 |
| `co2_concentration_ppm` | 373.2 ppm (2002 global) | NASA/NOAA Mauna Loa | Tier 1 |

**Data availability note:** Ethiopia 2002 subnational food security data is sparse.
`rainfall_anomaly_pct` uses ERA5 Reanalysis as the primary source; country-level
averaging masks subnational severity. All sub-national variability is treated as
Tier 3 synthetic data with scenario bands per the Synthetic Data Framework.

### Data Sources

| Source | Category | License | Access |
|---|---|---|---|
| ERA5 Reanalysis (Copernicus) | Climate | Copernicus License (free for research) | https://cds.climate.copernicus.eu/ |
| FAO FAOSTAT food production index | Economic/Ecological | CC BY-NC-SA 3.0 IGO | https://www.fao.org/faostat/ |
| World Bank WDI | Economic | CC BY 4.0 | https://data.worldbank.org/ |
| NASA/NOAA Mauna Loa CO2 | Ecological | Public domain (US Gov) | NOAA GML API |
| WHO Global Health Observatory | Health | CC BY-NC-SA 3.0 IGO | https://www.who.int/data/gho |
| NOAA Climate Data Online | Climate | Public domain (US Gov) | https://www.ncdc.noaa.gov/cdo-web/ |

### ControlInput Sequence

| Step (Year) | Input type | Input | Actor |
|---|---|---|---|
| 1 (2002) | `EmergencyPolicyInput` | `EMERGENCY_DECLARATION` — drought emergency, international appeal | ETH Government |
| 2 (2003) | `FiscalPolicyInput` | External humanitarian aid disbursement (World Food Programme, USAID OFDA, EU) | WFP / Multilateral |
| 3 (2004) | `StructuralPolicyInput` | `REGULATORY_CHANGE` — Productive Safety Net Programme initiation | ETH Government / World Bank |

**Actor note:** Step 2 involves external actors (WFP, USAID) delivering aid. The
`actor_id` should reference external entity IDs where they exist in the simulation
database. The `InputSource` for step 2 should be `EXTERNAL_HUMANITARIAN` (a new
enum value that does not currently exist — see Implementation Note below).

**Implementation note:** `EXTERNAL_HUMANITARIAN` does not yet exist in the
`InputSource` enum. The implementing team must either add it or use the closest
existing value and document the limitation. This is a known schema gap for
humanitarian-actor ControlInputs.

### Fidelity Thresholds

| Step | Attribute | Direction | Threshold type | Calibration tier | Historical basis |
|---|---|---|---|---|---|
| 1 (2002) | `gdp_growth` | DOWN (drought shock) | DIRECTION_ONLY | Tier 1 | World Bank WDI; GDP growth fell to 1.6% |
| 2 (2003) | `food_production_index` | DOWN (continued drought) | DIRECTION_ONLY | Tier 2 | FAO FPI; continued food production deficit |
| 3 (2004) | `gdp_growth` | UP (recovery begins) | DIRECTION_ONLY | Tier 1 | World Bank WDI; 13.6% GDP growth in 2004 recovery |
| 3 (2004) | `food_production_index` | UP (recovery with PSNP) | DIRECTION_ONLY | Tier 2 | FAO FPI; production recovery with safety net |

### Evaluation Criteria

1. Simulation `gdp_growth` falls at step 1 (drought shock)
2. Simulation `food_production_index` falls at step 2 (continued shock)
3. Simulation shows economic recovery at step 3 following humanitarian aid ControlInput
4. `food_production_index` rises at step 3 following PSNP structural input
5. Poverty headcount ratio does not fall during steps 1–2 (drought worsens poverty before recovery)
6. Backtesting pass/fail: 3 of 4 thresholds must be met (75% pass threshold, reflecting data quality constraints)

---

## Case 3 — Philippines Typhoon Haiyan Economic Impact and Recovery (2013–2015)

### Geography

| Field | Value |
|---|---|
| Entity | Philippines |
| ISO alpha-3 | PHL |
| Level | Nation-state (Level 1) |
| Subnational notes | Haiyan impact concentrated in Region VIII (Eastern Visayas), Region VI (Western Visayas); Level 1 dilutes impact severity — documented limitation |

### Time Period

**Start:** 2013
**End:** 2015
**Timestep:** Annual
**Steps:** 3
**Event:** Typhoon Haiyan landfall November 8, 2013; classified as one of the strongest tropical cyclones ever recorded.

### Rationale for Case Selection

Typhoon Haiyan (2013) provides a sudden-onset ecological shock — distinct from the
gradual deforestation and drought cases above — with well-documented immediate
economic damage ($12.9 billion estimated damage) and a documented international
humanitarian response. The Philippines case tests the simulation's response to
a high-magnitude, one-step shock followed by reconstruction ControlInputs. It
also tests whether the ecological-economic transmission pathway works for
disaster-type events, not just slow-accumulation ecological pressures. The
3-step timeline is short but the shock magnitude and data quality make it
tractable.

### Initial State Parameters (Year 2013)

| Attribute | Value | Source | Tier |
|---|---|---|---|
| `gdp_growth` | 7.2% (2013, pre-Haiyan full year) | World Bank WDI | Tier 1 |
| `debt_gdp_ratio` | 36.4% (2013) | IMF WEO | Tier 1 |
| `disaster_damage_gdp_pct` | 4.3% of GDP (Haiyan damage estimate; mid-range of $12.9B) | World Bank PDNA 2013 | Tier 2 |
| `agricultural_gdp_share` | 10.1% of GDP (2013) | World Bank WDI | Tier 1 |
| `poverty_headcount_ratio` | 25.2% ($3.20/day, 2012 base) | World Bank PovcalNet | Tier 2 |
| `co2_concentration_ppm` | 396.5 ppm (2013 global) | NASA/NOAA Mauna Loa | Tier 1 |
| `rainfall_anomaly_pct` | Not applicable for typhoon case — see note | ERA5 | — |

**Rainfall note:** Typhoon Haiyan is a discrete extreme weather event, not a
rainfall anomaly. The triggering ecological condition is best encoded as a
`disaster_damage_gdp_pct` STOCK shock at step 1, not as a continuous `rainfall_anomaly_pct`
flow. The implementing team must confirm the appropriate Quantity type and attribute
key before writing the initial state fixture.

### Data Sources

| Source | Category | License | Access |
|---|---|---|---|
| World Bank Post-Disaster Needs Assessment (PDNA) 2013 | Economic/Damage | Public (World Bank) | https://www.worldbank.org/ |
| ERA5 Reanalysis (Copernicus) | Climate | Copernicus License | https://cds.climate.copernicus.eu/ |
| NOAA Climate Data Online | Climate | Public domain (US Gov) | https://www.ncdc.noaa.gov/cdo-web/ |
| World Bank WDI | Economic | CC BY 4.0 | https://data.worldbank.org/ |
| IMF WEO | Economic | CC BY 4.0 | https://www.imf.org/en/Publications/WEO |
| OCHA Financial Tracking Service | Humanitarian | Public (UN) | https://fts.unocha.org/ |
| NASA/NOAA Mauna Loa CO2 | Ecological | Public domain | NOAA GML API |

### ControlInput Sequence

| Step (Year) | Input type | Input | Actor |
|---|---|---|---|
| 1 (2013) | `EmergencyPolicyInput` | `EMERGENCY_DECLARATION` — national disaster declaration; state of calamity | PHL Government |
| 1 (2013) | `FiscalPolicyInput` | `SPENDING_CHANGE` — emergency reconstruction appropriation (PHP 14.6B Yolanda Fund) | PHL Government |
| 2 (2014) | `FiscalPolicyInput` | `SPENDING_CHANGE` — international aid disbursement ($788M ODA per OCHA FTS) | Multilateral / Bilateral |
| 2 (2014) | `StructuralPolicyInput` | `REGULATORY_CHANGE` — Comprehensive Rehabilitation and Recovery Plan (CRRP) | PHL Government |

**Actor note:** Step 2 international aid uses `actor_id` for donor entities where
available. Same `EXTERNAL_HUMANITARIAN` InputSource gap applies as in Case 2.

### Fidelity Thresholds

| Step | Attribute | Direction | Threshold type | Calibration tier | Historical basis |
|---|---|---|---|---|---|
| 1 (2013) | `gdp_growth` | DOWN (Haiyan shock — note: shock arrives late in year; full-year GDP may be partially insulated) | DIRECTION_ONLY | Tier 1 | World Bank WDI; growth moderated but Philippines maintained positive growth in 2013 full year |
| 2 (2014) | `gdp_growth` | UP (reconstruction boom) | DIRECTION_ONLY | Tier 1 | World Bank WDI; 6.3% growth in 2014 with reconstruction spending |
| 3 (2015) | `gdp_growth` | POSITIVE (≥ 0%) | MAGNITUDE ≥ 0% | Tier 1 | World Bank WDI; Philippines sustained growth trajectory |

**Timing note:** Haiyan made landfall in November 2013. Full-year GDP data for 2013
(7.2% growth) reflects strong pre-Haiyan momentum. The step-1 threshold is
DIRECTION_ONLY (not magnitude) because the annual timestep cannot isolate the
Q4 2013 shock from the Q1–Q3 2013 pre-shock performance. This is a known
temporal resolution limitation per ARCH-REVIEW-002 Finding BI2-N-07. A fidelity
threshold based on annual GDP growth for a Q4 event is directionally indicative
only.

### Evaluation Criteria

1. Simulation produces a GDP growth deceleration at step 1 (relative to trend)
2. Simulation produces GDP growth recovery at step 2 following reconstruction ControlInputs
3. Simulation maintains positive GDP growth at step 3
4. Fiscal balance deteriorates at step 1 (emergency spending)
5. Backtesting pass/fail: 2 of 3 thresholds must be met (67% pass threshold, reflecting
   annual-timestep limitations for a Q4 shock event)

---

## Implementation Priority

| Case | Ecological type | Data availability | Statistical strength | Recommended priority |
|---|---|---|---|---|
| Case 1 — BRA Amazon deforestation | Slow accumulation (land-use change) | Good — INPE PRODES + FAO FRA | Strong (10 steps, 5 thresholds) | **Highest** |
| Case 2 — ETH drought 2002–2004 | Climatic shock (drought) | Moderate — ERA5 + FAO FPI | Adequate (3 steps, 4 thresholds) | Medium |
| Case 3 — PHL Typhoon Haiyan | Sudden onset disaster | Good — World Bank PDNA + WDI | Limited (3 steps, 3 thresholds; timing constraint) | Lower |

**Recommendation:** Implement Case 1 (BRA Amazon) first. It provides the strongest
statistical validity, the clearest policy intervention timeline, and exercises the
`land_use_pressure_index` and `co2_trajectory` ecological attributes that the
ecological module currently supports. Cases 2 and 3 introduce ecological shock types
(climate drought, disaster) that may require new attribute keys and ControlInput
enum values; these schema extensions should follow Case 1, not precede it.

---

## Open Schema Questions

Before implementing any case, the following schema questions must be resolved:

1. **`deforestation_rate_km2_yr`** — Does this attribute exist in `docs/schema/simulation_state.yml`? If not, it requires an ADR amendment before use.
2. **`rainfall_anomaly_pct` and `food_production_index`** — Same question. These are not in the currently approved attribute list.
3. **`EXTERNAL_HUMANITARIAN` InputSource** — Does not exist in the `InputSource` enum. Must be added or a documented workaround committed.
4. **`disaster_damage_gdp_pct`** — Novel attribute for typhoon case. Requires schema registration.

Resolving these questions is the first implementation task before writing any fixture
file. Read `docs/schema/simulation_state.yml` and `docs/schema/database.yml` before
proceeding.

---

*Planned by PM Agent — Issue #95. See ARCH-REVIEW-002 Finding BI2-N-04 for the
architectural root cause this document addresses.*
