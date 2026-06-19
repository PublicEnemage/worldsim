# WorldSim Confidence Tier Assignment Methodology

> **M14 scope:** This document covers how confidence tiers T1–T5 are assigned to
> each indicator family. Full distributional confidence intervals (CI bounds via
> bootstrap / Monte Carlo — the `ci_lower`/`ci_upper` fields) are deferred to M16
> per sprint plan §G6 out-of-scope note. This document is the methodology publication
> goal for Issue #22 in M14.
>
> **Audience:** Finance ministry economists, domain expert reviewers, TSC members.
> This document is designed to be navigated from the calibration index without
> specialist mediation.

---

## What confidence tiers mean

WorldSim assigns each indicator a confidence tier from T1 (highest confidence) to
T5 (lowest confidence). The tier is displayed in the Zone 1B alert detail slot as a
negotiation-defensibility label — it tells the ministry analyst what they can safely
cite in a session and what they should verify first.

| Tier | Label in Zone 1B | What it means |
|------|-----------------|---------------|
| T1 | High confidence — cite directly | Direct measurement from an institutional primary source (e.g., NASA/NOAA Mauna Loa CO2 series, Central Bank official statistics). Methodology is documented, peer-reviewed, and internationally standardized. |
| T2 | High confidence — cite directly | Official statistics from an institutional source (e.g., IMF WEO, World Bank WDI, Central Bank annual report). Published with documented methodology. Calendar-year vs. fiscal-year alignment may require notation. |
| T3 | Moderate confidence — cite with caveat | Model estimate or interpolated series. Derived from institutional data using a documented methodology, but not a direct observation. Examples: 5-year FAO data with annual interpolation; synthetic composites from regional comparables. |
| T4 | Model estimate — verify before citing | Computed output of the WorldSim simulation model. The indicator value is an engine-derived estimate, not a sourced data point. Methodology is transparent (documented in this repository) but has not been independently calibrated for the specific country context. |
| T5 | Synthetic extrapolation — do not cite | Statistical extrapolation from a regional or comparable-economy distribution. No country-specific source data. Suitable for scenario direction and internal planning — not for citation in external negotiations without further verification. |

The tier label system is defined in ADR-015 §UX-5. The Zone 1B detail slot
displays the negotiation-defensibility label for the indicator in the active MDA
alert — Persona 2 uses this label to decide whether to cite the figure in the
current session.

---

## T1 indicators

**co2_concentration_ppm**
- Source: NASA/NOAA Mauna Loa Observatory CO2 measurement series
- Tier rationale: Direct atmospheric measurement; longest continuous CO2 record in
  existence; internationally recognized and peer-reviewed.
- Source registry ID: N/A (boundary constant, not entity indicator)
- ADR reference: ADR-005 Amendment B §confidence tier table

No other T1 indicators are currently implemented. T1 is reserved for direct
physical measurements from internationally recognized observatories.

---

## T2 indicators

T2 indicators are official statistics from institutional primary sources. They are
citable directly in ministry briefings and external negotiations. The main caveat
is vintage: IMF/WB data may have 2–3 year reporting lag for some countries and
indicators.

**reserve_coverage_months**
- Source: Central Bank of Jordan Annual Report 2023 (CBJ_ANNUAL_2023) for JOR;
  IMF WEO April 2024 (IMF_WEO_APR2024) for EGY
- Tier rationale: Official central bank statistics published annually with
  documented methodology. FX reserves are primary balance of payments data.
- Source registry IDs: `CBJ_ANNUAL_2023`, `IMF_WEO_APR2024`

**gdp_growth**
- Source: IMF World Economic Outlook April 2024 (IMF_WEO_APR2024)
- Tier rationale: IMF institutional forecast with cross-country methodology.
  Calendar vs. fiscal year alignment noted in source registry limitations.
- Source registry ID: `IMF_WEO_APR2024`

**unemployment_rate**
- Source: Jordan Department of Statistics LFS Q1 2024 (DOS_LFS_Q1_2024);
  World Bank WDI 2023 (WORLD_BANK_WDI_2023) for EGY/ZMB
- Tier rationale: Official labour force surveys with documented ILO methodology.
  Limitation: understates informal sector underemployment.
- Source registry IDs: `DOS_LFS_Q1_2024`, `WORLD_BANK_WDI_2023`

**rule_of_law_percentile**
- Source: World Bank Worldwide Governance Indicators (WGI)
- Tier rationale: Institutional composite score with documented methodology.
  WGI is an aggregate of multiple underlying surveys.

**democratic_quality_score**
- Source: V-Dem Liberal Democracy Index
- Tier rationale: V-Dem documented aggregation methodology; standardized
  cross-country scale [0, 1].

---

## T3 indicators

T3 indicators are model estimates or interpolated series derived from institutional
data. They should be cited with a caveat ("this is a WorldSim model estimate based
on IMF/FAO data — we can share the methodology") in external negotiations.

**trend_growth**
- Source: IMF WEO April 2024 with HP filter smoothing (annual interpolation)
- Tier rationale: Derived from WEO data using the Hodrick-Prescott filter;
  interpolation from annual data.

**land_use_pressure_index**
- Source: FAO Global Forest Resources Assessment 2020 (5-year cycle)
- Tier rationale: FAO data is authoritative but measured on a 5-year assessment
  cycle. Annual values require interpolation.
- Source registry ID: `ACADEMIC_LITERATURE_FAO_GFR_2020_FISCAL_LAND_USE`

**water_stress_index** (arid_semiarid entities: JOR, ZMB)
- Source: FAO WASAG 2020 baseline / ICARDA Water Productivity in Arid Regions 2019
- Tier rationale: Modelled estimate from FAO arid-zone areal assessment with
  ICARDA regional calibration. Not a direct per-country measurement.
- CM+EE approval: 2026-06-13 (M13 G8a deliberation)
- Source registry ID: `ACADEMIC_LITERATURE_FAO_GFR_ARID_ICARDA_WATER_STRESS`
- Biome restriction: only computed for entities with biome_class=arid_semiarid

**reserve_coverage_months** (ZMB only)
- Source: IMF WEO April 2024 with SADC comparable economies composite
- Tier rationale: Zambia's reserve data quality is T3 (synthetic composite)
  per entity_data_quality_coverage table.

**Composite scores — governance framework**
- Tier floor: T3 (per `_NORMALIZED_ABSOLUTE_MIN_TIER = 3` in scenarios.py)
- Tier derivation: max(min indicator tier across governance indicators, T3)

**Composite scores — ecological framework**
- Tier floor: T3 (per `_ECOLOGICAL_MIN_TIER = 3` in scenarios.py — CM-G6-1)
- Tier derivation: max(min indicator tier across ecological indicators, T3)
- Rationale (CM-G6-1, 2026-06-18): land_use_pressure_index and water_stress_index
  are both T3. A composite combining T3 proxies with planetary boundary constants
  cannot be T2 without misrepresenting the data quality chain.

---

## T4 indicators

T4 indicators are computed outputs of the WorldSim simulation model. They are
produced by the engine's propagation and module logic, not sourced from external
data. They can be cited as model estimates — "WorldSim estimates that at this
trajectory, bottom-quintile consumption capacity falls below the threshold" — but
the ministry team should be prepared to explain the model methodology if challenged.

**bottom_quintile_consumption_capacity** (after external sector shock application)
- Produced by: ExternalSector module via HCL transmission factor
- Confidence_tier = 3 in initial seed, degrades to T4 with projection horizon
  (effective_tier() function: +1 tier per 5 projection steps)

**political_economy composite indicators** (programme_survival_probability, composite_score)
- Source: PoliticalEconomyModule engine computation
- Confidence tier: T4 (programme_survival_probability is DIRECTION_ONLY, documented
  in ADR-013 §CM constraint)

**All engine-computed indicators** beyond the first 5 projection steps
- Tier degradation: effective_tier(source_tier, horizon_steps) = min(5, source_tier + floor(horizon_steps / 5))
- Rationale: Projection uncertainty accumulates with horizon. A T2 indicator at step 0
  becomes T3 after 5 steps, T4 after 10 steps, T5 after 15 steps.

---

## T5 indicators

T5 indicators are statistical extrapolations from regional or comparable-economy
distributions. They should not be cited in external negotiations without
substantial additional verification. They are provided for internal scenario
direction and planning only.

**Ecological indicators** (ZMB, EGY — when no entity-specific data exists)
- Source: SADC / MENA comparable economies 2022-2023
- Coverage classification: T4–T5 depending on indicator; entity_data_quality_coverage
  records the framework-level tier

**Any indicator beyond 15 projection steps**
- Tier degradation applies: source T2 → T5 at step 15+

---

## Tier assignment rules

1. **Source tier** is assigned at data ingestion time based on the source_registry entry's
   `quality_tier` field (1–5 per DATA_STANDARDS.md §Confidence Tier System).

2. **Indicator tier** = max(source_tier, any input event's tier)
   When an indicator is updated by a simulation event, the indicator tier is the
   maximum of its own source tier and the triggering event's confidence tier.
   This prevents a T2 source indicator from being reported as T2 when it has been
   updated by a T4 model event.

3. **Framework composite tier** = max(min(indicator tiers), framework_floor)
   - Financial: no floor
   - Human development: no floor
   - Governance: floor T3 (normalized_absolute methodology, CM-R3)
   - Ecological: floor T3 (boundary proximity methodology, CM-G6-1)
   - Political economy: T4 (DIRECTION_ONLY, ADR-013)

4. **Effective tier at output** = min(5, source_tier + floor(horizon_steps / 5))
   Applied at the output layer only. Stored snapshots retain the source tier.

5. **Mixed-mode outputs** (real data + synthetic fill): the composite tier is the
   max of all constituent indicator tiers, not the average. One T5 synthetic fill
   pulls the composite to T5.

---

## Known limitations and blindspots

- **Ecological tiers** are currently T3 for all ecological indicators in the M14
  entity scope. Tier 2 ecological calibration requires ADR-007 acceptance and full
  planetary boundary calibration against observed data. No T1 ecological composite
  exists; the methodology does not support it until observational measurement series
  replace model proxies.

- **Political economy indicators** are T4 by design. The political feasibility
  methodology (ADR-013) is a simulation output, not a sourced measurement. External
  validation of the political economy module is in scope for M14.

- **Projection uncertainty** is modelled by tier degradation, not by statistical
  confidence intervals. The `ci_lower`/`ci_upper` fields in TrajectoryFrameworkPoint
  are currently null. Monte Carlo or bootstrap confidence intervals are deferred to
  M16 (ADR-007-gated).

- **Entity scope**: confidence tier assignments above cover GRC, JOR, EGY, ZMB
  (ADR-016 §EL Decision 1 entity scope). Other entities may have different tier
  profiles when their data is onboarded.

---

*Document version: M14 — 2026-06-18. Issue #22 (M14 scope).*
*Full distributional bands (CI intervals) deferred to M16.*
*Authored by Chief Methodologist Agent for M14 G6 — Methodology, Calibration,*
*and Instrument Legibility.*
