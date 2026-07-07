# WorldSim Analytical Evidence Portfolio — Coverage Audit

> **Authority:** Analytical Evidence Agent (AEA), External Intelligence Layer  
> **Status:** DRAFT — awaiting EL review  
> **Scope:** All four registered calibration families; all backtesting fixtures present in `backend/tests/fixtures/` as of v0.19.0  
> **Reference:** `docs/evidence/analytical-framework.md` — calibration family definitions, fidelity tiers, error envelope principle  
> **Audit date:** 2026-07-07 (M20, post-M19-close)

This document audits what the WorldSim engine can currently demonstrate, entity by entity, within each calibration family. It maps what exists (fixture files, calibration entries, data tiers) to what is immediately runnable and what the fidelity ceiling is. It concludes with regional benchmarking pairs — the comparison configurations that are valid within the error envelope.

The audit is honest about gaps. Entries with no fixture, entities outside registered families, and indicators where fidelity is capped at DIRECTION_ONLY regardless of data quality — these are documented, not minimised.

---

## Family 1 — SSA-LIC (Sub-Saharan Africa Low Income Countries)

**Calibration basis:** Fosu (2011) + IMF AFRO/REO. All fiscal multiplier estimates T3. See `docs/evidence/analytical-framework.md §1 Family 1`.

---

### (a) Entities covered — data tier assessment

| Entity | Common name | Fixture file | Data tier (fiscal) | Data tier (human dev.) | Data tier (external balance) | Calibration model |
|---|---|---|---|---|---|---|
| `SEN` | Senegal | `sen_scenario.py` ✓ | T3 — Fosu 2011 regional | T2 — World Bank WDI (2000–2015) | T3 — IMF AFRO range | SSA-LIC general |
| `ZMB` | Zambia | `zmb_scenario.py` ✓ | T3 — Fosu 2011 regional | T2 — World Bank WDI; Copperbelt cohort data | T2 — copper price from IMF WEO | SSA-LIC general; ILO 2020 COVID informal sector |
| `GHA` | Ghana | `ghana_2022_scenario.py` ✓ | T3 — Fosu 2011 regional | T2 — World Bank WDI (2022) | T2 — IMF Article IV 2022 | SSA-LIC general |
| `ETH` | Ethiopia | No fixture | T3 — structural analogue | T3 — partial WDI coverage | T3 — AFRO range | SSA-LIC structural analogue only |
| `KEN` | Kenya | No fixture | T3 — structural analogue | T3 — partial WDI coverage | T3 — AFRO range | SSA-LIC structural analogue only |

**ELASTICITY_REGISTRY entries for this family:**  
- Q1 INFORMAL (all entities): `ACADEMIC_LITERATURE_FOSU_2011_SSA_POVERTY_GROWTH`, confidence_tier=3  
- Q2 FORMAL credit-contraction channel: `ACADEMIC_LITERATURE_ICELAND_2008_CREDIT_CONTRACTION_PHC`, confidence_tier=3  
- IMF 2014 fiscal-inequality channel: `ACADEMIC_LITERATURE_IMF_2014_FISCAL_INEQUALITY`, confidence_tier=3  
- ZMB-specific COVID informal sector channel: `ACADEMIC_LITERATURE_ILO_2020_COVID_WORLD_OF_WORK`, confidence_tier=3

---

### (b) Fidelity ceiling — current calibration state

| Indicator | Fidelity ceiling | Limiting factor |
|---|---|---|
| GDP trajectory direction | DIRECTION_ONLY | T3 fiscal multiplier (Fosu 2011 regional range) |
| Fiscal balance direction | DIRECTION_ONLY | Linked to T3 multiplier |
| Human development trajectory | MAGNITUDE (SEN, ZMB, GHA conditional) | WDI T2 data enables Fosu growth-poverty elasticity application; per-step magnitude ordering valid within family |
| Poverty headcount direction | DIRECTION_ONLY (general); MAGNITUDE (conditional on T2 WDI vintage for SEN/ZMB/GHA) | See above |
| Current account direction | DIRECTION_ONLY | IMF AFRO range only; no entity-specific trade elasticities |
| Commodity channel (ZMB) | MAGNITUDE (copper price direction and first-order fiscal impact) | IMF WEO copper price at T2 for 2005–2015 period; ZMB fiscal copper linkage documented |
| Ecological costs | DIRECTION_ONLY | LULC global estimates; no entity-specific carbon intensity |
| Governance trajectory | DIRECTION_ONLY | GOVERNANCE_ELASTICITY_REGISTRY T3 for all SSA entities |

---

### (c) Immediately runnable backtesting scenarios

**Scenario SSA-1 — Senegal structural adjustment and growth recovery (Type A)**  
*Fixture:* `backend/tests/fixtures/sen_scenario.py`  
*Entity:* SEN | *Period:* 2000–2015 | *Steps:* 6 | *Type:* A (historical replay)  
*Historical context:* Senegal's 2000–2015 period encompassed post-HIPC debt relief (2004), sustained growth under PRSP frameworks, and commodity price volatility. GDP per capita grew at ~3–4% annually on average, though distributional improvements were uneven.  
*Question posed:* Does the engine correctly identify the direction of Senegal's human development trajectory following post-HIPC debt relief and structural adjustment compliance?  
*Known historical outcome:* HDI improved from approximately 0.38 (2000) to 0.47 (2015); poverty headcount fell; fiscal balance improved with debt relief but remained constrained by low revenue base.  
*Expected fidelity tier:* DIRECTION_ONLY (fiscal); MAGNITUDE conditional (human development if WDI T2)  

**Scenario SSA-2 — Zambia copper boom, consolidation, and debt ceiling (Type A)**  
*Fixture:* `backend/tests/fixtures/zmb_scenario.py`  
*Entity:* ZMB | *Period:* 2005–2015 | *Steps:* 6 | *Type:* A (historical replay)  
*Historical context:* Zambia's 2005–2015 period was shaped by the copper boom (2005–2008), global financial crisis shock (2009), recovery, and eventual fiscal deterioration as copper prices fell from 2011. The Copperbelt cohort experienced the sharpest welfare swings.  
*Question posed:* Does the engine correctly find that the Copperbelt cohort's poverty headcount trajectory tracks the copper price cycle — improving through the boom and reversing from 2011?  
*Known historical outcome:* ZMB poverty headcount broadly declining 2005–2010; rising again from 2011–2014 as commodity prices fell and fiscal space contracted; fin_composite step 3 direction downward relative to step 1.  
*Expected fidelity tier:* DIRECTION_ONLY (fiscal multiplier); MAGNITUDE (commodity-poverty channel via copper price, ZMB-specific calibration)  

**Scenario SSA-3 — Ghana 2022 IMF programme entry (Type A or Type B)**  
*Fixture:* `backend/tests/fixtures/ghana_2022_scenario.py`  
*Entity:* GHA | *Period:* 2022–2023 | *Steps:* 6 | *Type:* A (historical replay) or Type B (debt restructuring counter-factual)  
*Historical context:* Ghana entered an IMF Extended Credit Facility programme in May 2023 following unsustainable debt levels, currency depreciation of ~55% in 2022, and loss of market access. Debt restructuring concluded in 2023.  
*Question posed:* Does the engine find consistent downward human development direction from the fiscal shock step onward, with the MDA poverty headcount threshold breached?  
*Known historical outcome:* GDP contracted, poverty indicators worsened significantly in 2022; debt restructuring eventually stabilised fiscal trajectory.  
*Expected fidelity tier:* DIRECTION_ONLY  

---

### (d) Known gaps

- `ETH` and `KEN` have no backtesting fixtures. Both are structural analogues only — the engine will run them with SSA-LIC elasticities but no historical comparison is available to validate direction verdicts.
- No fixture for SSA entities in the 1980s–1990s structural adjustment era (a key historical period for the tool's core use case). The AFRO evidence base has a temporal gap: all current SSA fixtures are 2000-onward.
- The Fosu (2011) elasticity applies to aggregate poverty headcount. Sub-national distributional dynamics (e.g., urban vs. rural divergence, women-headed households) are not separately calibrated for any SSA entity.
- No ecological intensity data at entity level — all SSA ecological outputs are DIRECTION_ONLY from global LULC estimates regardless of data quality on other indicators.

---

## Family 2 — EURO-AREA (Euro Area — Advanced Economy Fixed Exchange Rate Regime)

**Calibration basis:** Ilzetzki, Mendoza, and Végh (2013). GRC at CM-A (T2, confidence_tier=2 in ELASTICITY_REGISTRY). Other entities at T2 literature (no dedicated fixture calibration). See `docs/evidence/analytical-framework.md §1 Family 2`.

---

### (a) Entities covered — data tier assessment

| Entity | Common name | Fixture file | Data tier (fiscal) | Data tier (human dev.) | Data tier (external balance) | Calibration model |
|---|---|---|---|---|---|---|
| `GRC` | Greece | `greece_2010_scenario.py` ✓ (T/A + T/B); `greece_2010_2012_actuals.py` ✓ | T2 — Ilzetzki et al. 2013; Blanchard & Leigh 2013; confidence_tier=2 in registry | T2 — Eurostat SILC 2010–2013; AROPE data | T2 — Eurostat BOP; IMF WEO | CM-A (M19): GRC-scoped FORMAL Q1/Q2 entries |
| `ISL` | Iceland | `isl_2008_heterodox.py` ✓; `isl_2008_orthodox_counterfactual.py` ✓ | T2 (structural) — advanced Nordic economy; Batini et al. 2012 | T2 — Statistics Iceland; OECD | T2 — BIS; IMF Article IV | ADR-020 capital controls channel (M19) |
| `PRT` | Portugal | No dedicated fixture | T2 (literature) — Ilzetzki et al. 2013 applicable | T2 (WDI/Eurostat available) | T2 (Eurostat BOP available) | EURO-AREA general; no CM calibration |
| `IRL` | Ireland | No dedicated fixture | T2 (literature) — Ilzetzki et al. 2013 applicable | T2 (Eurostat available) | T2 (Eurostat BOP available) | EURO-AREA general; no CM calibration |
| `CYP` | Cyprus | No dedicated fixture | T2 (literature) — Ilzetzki et al. 2013 applicable | T2 (Eurostat available) | T2 (Eurostat BOP available) | EURO-AREA general; no CM calibration |

**Note on Iceland (ISL):** Iceland is not a Euro-area member but is classified here as the closest structural analogue: advanced, small, open economy; 2008–2011 crisis period is the engine's canonical capital controls scenario (ADR-020). The Ilzetzki et al. (2013) advanced economy estimates are applicable. ISL-specific fixture is the only non-GRC Euro-area fixture in the current portfolio.

**ELASTICITY_REGISTRY entries for GRC (CM-A):**  
- Q1 FORMAL: `ACADEMIC_LITERATURE_BLANCHARD_LEIGH_2013_FISCAL_MULTIPLIERS`, confidence_tier=2, entity_families={"GRC"}  
- Q2 FORMAL: `ACADEMIC_LITERATURE_BALL_2013_FISCAL_CONSOLIDATION`, confidence_tier=2, entity_families={"GRC"}

---

### (b) Fidelity ceiling — current calibration state

| Indicator | Fidelity ceiling (GRC) | Fidelity ceiling (ISL) | Fidelity ceiling (PRT/IRL/CYP) | Limiting factor |
|---|---|---|---|---|
| GDP trajectory direction | CALIBRATED_CI (ADR-007 posterior) | MAGNITUDE | MAGNITUDE | GRC: Bayesian posterior available; others: T2 literature, no posterior |
| Fiscal balance | MAGNITUDE | MAGNITUDE | MAGNITUDE | Eurostat/IMF data at T2 for all; multiplier T2 for GRC/ISL |
| Human development direction | MAGNITUDE | MAGNITUDE | DIRECTION_ONLY | SILC T2 for GRC; Statistics Iceland T2; thinner data for PRT/IRL/CYP without dedicated fixture |
| Unemployment trajectory | MAGNITUDE | MAGNITUDE | MAGNITUDE | Eurostat LFS at T2 for all registered entities |
| Current account | MAGNITUDE | MAGNITUDE | DIRECTION_ONLY | Eurostat BOP T2 for GRC/ISL; PRT/IRL/CYP need fixture calibration |
| Capital controls channel (ISL only) | MAGNITUDE | — | N/A | ADR-020 transmits as MAGNITUDE; no CI posterior |
| Ecological costs | DIRECTION_ONLY | DIRECTION_ONLY | DIRECTION_ONLY | EEA estimates; global uncertainty dominates |

---

### (c) Immediately runnable backtesting scenarios

**Scenario EUR-1 — Greece Troika adjustment, orthodox path (Type A + Type B)**  
*Fixture:* `backend/tests/fixtures/greece_2010_scenario.py`; actuals: `greece_2010_2012_actuals.py`  
*Entity:* GRC | *Period:* 2010–2015 | *Steps:* 6 | *Types:* A (historical replay) and B (counter-factual alternative path)  
*Historical context:* Greece accepted a Troika (EU/ECB/IMF) adjustment programme in May 2010, implementing severe fiscal consolidation (primary surplus targets: -8.1% → +4.5% of GDP by 2014) under a fixed exchange rate. GDP fell ~25% cumulatively by 2013. Unemployment reached 27.5%. The exercise is the engine's most thoroughly validated scenario and the basis for Demo 8 (2026-07-06).  
*Question posed (Type B):* If Greece had negotiated a slower fiscal adjustment path (lower primary surplus targets, debt restructuring front-loaded), would the engine find a different human development trajectory direction over the 2010–2015 period?  
*Known historical outcome:* GDP contracted severely under the orthodox path; poverty and unemployment rose sharply; eventual restructuring (PSI 2012) occurred after the steepest contraction.  
*Expected fidelity tier:* CALIBRATED_CI on fiscal multiplier output (ADR-007); MAGNITUDE on human development and labour market; DIRECTION_ONLY on ecological

**Scenario EUR-2 — Iceland 2008 heterodox vs orthodox (Type B)**  
*Fixtures:* `backend/tests/fixtures/isl_2008_heterodox.py`; `backend/tests/fixtures/isl_2008_orthodox_counterfactual.py`  
*Entity:* ISL | *Period:* 2008–2011 | *Steps:* 6 | *Type:* B (counter-factual branch)  
*Historical context:* Iceland experienced a catastrophic banking collapse in October 2008 (bank assets ~10× GDP). Unlike most Troika-programme countries, Iceland imposed capital controls, allowed its banks to fail, and maintained social spending. Recovery by 2011 was faster than contemporaneous Euro-area adjustment programmes.  
*Question posed:* Does the engine find that the heterodox path (capital controls + social spending maintenance + bank failure) shows better human development trajectory direction than the orthodox counter-factual (EU-style bail-in of depositors + immediate fiscal consolidation)?  
*Known historical outcome:* Iceland recovered faster than Ireland or Greece; unemployment peaked at ~8% vs 27% in GRC; poverty headcount rose but returned to pre-crisis levels by 2012.  
*Expected fidelity tier:* MAGNITUDE (capital controls channel via ADR-020); DIRECTION_ONLY for cross-country comparison with GRC

---

### (d) Known gaps

- `PRT`, `IRL`, `CYP` are in the EURO-AREA family but have no dedicated backtesting fixtures. The engine can run them using EURO-AREA general elasticities, but no historical comparison exists to validate direction verdicts.
- Portugal 2010–2014 is a natural next fixture: contemporaneous with GRC Troika; independently verifiable; would allow within-family cross-entity validation of the error envelope principle.
- The ADR-007 Bayesian posterior CI is currently calibrated for the GRC fiscal multiplier channel only. Extending it to ISL, PRT, or IRL would require separate posterior estimation against those entities' historical data.
- No fixture for Ireland 2010–2013 (bank bailout + Troika programme) — Ireland is structurally important as a counter-example where fiscal adjustment was accompanied by export-led recovery, testing the engine's ability to distinguish fiscal consolidation with and without export growth.
- Cyprus 2013 bail-in is not yet modelled — the depositor haircut represents a distinct transmission mechanism not currently in the ELASTICITY_REGISTRY.

---

## Family 3 — LATAM-EM (Latin American Emerging Market)

**Calibration basis:** Ilzetzki et al. (2013) LAC range + Céspedes and Velasco (2012). All multiplier estimates T3. ARG has CM-B (general LAC) and CM-D (Kirchner recovery-specific inputs). See `docs/evidence/analytical-framework.md §1 Family 3`.

---

### (a) Entities covered — data tier assessment

| Entity | Common name | Fixture file | Data tier (fiscal) | Data tier (human dev.) | Data tier (external balance) | Calibration model |
|---|---|---|---|---|---|---|
| `ARG` | Argentina | `argentina_2001_2002_scenario.py` ✓; `argentina_2001_2002_actuals.py` ✓ | T3 — Ilzetzki et al. LAC range | T3 — SEDLAC partial; MECON household survey partial coverage | T2 — MECON/IMF WEO; Céspedes & Velasco commodity linkage | CM-B (LAC general) + CM-D (Kirchner inputs) |
| `ECU` | Ecuador | `ecuador_1999_2000_scenario.py` ✓; `ecuador_1999_2000_actuals.py` ✓ | T3 — Ilzetzki et al. LAC range | T3 — partial WDI | T3 — IMF WHDR range | CM-B (LAC general) |
| `BOL` | Bolivia | No dedicated fixture | T3 — structural analogue | T3 — partial WDI | T3 — WHDR range | CM-B (LAC general) structural analogue |
| `PER` | Peru | No dedicated fixture | T3 — structural analogue | T3 — partial WDI | T3 — WHDR range | CM-B (LAC general) structural analogue |

**ELASTICITY_REGISTRY entries for this family:**  
- Q1 FORMAL: `ACADEMIC_LITERATURE_LUSTIG_2014_CEQ_LAC_POVERTY`, confidence_tier=3, entity_families={"ARG","ECU","BOL","PER"}  
- Q2 FORMAL (Ball 2013 fiscal consolidation): confidence_tier=3, entity_families={"ARG","ECU","BOL","PER"}

**Note on CM-D (ARG Kirchner recovery inputs):**  
CM-D provides 2003–2007 Kirchner-era control inputs calibrated against MECON and IMF observed data. This improves the realism of the recovery-period scenario configuration but does not raise the fiscal multiplier tier above T3. The CM-D contribution is to input accuracy, not multiplier confidence.

---

### (b) Fidelity ceiling — current calibration state

| Indicator | Fidelity ceiling (ARG) | Fidelity ceiling (ECU) | Fidelity ceiling (BOL/PER) | Limiting factor |
|---|---|---|---|---|
| GDP trajectory direction | DIRECTION_ONLY | DIRECTION_ONLY | DIRECTION_ONLY | T3 LAC fiscal multiplier (wide range: negative to near-zero on impact) |
| Fiscal balance direction | DIRECTION_ONLY | DIRECTION_ONLY | DIRECTION_ONLY | Linked to T3 multiplier |
| External balance direction | MAGNITUDE (conditional, ARG) | DIRECTION_ONLY | DIRECTION_ONLY | Céspedes & Velasco (2012) TOT framework; ARG-specific trade data at T2 for some periods |
| Poverty/inequality direction | DIRECTION_ONLY | DIRECTION_ONLY | DIRECTION_ONLY | SEDLAC distributional data partial; elasticity T3 |
| Commodity channel (ARG, ECU) | MAGNITUDE (conditional) | MAGNITUDE (conditional) | DIRECTION_ONLY | Céspedes & Velasco applicable where commodity exposure documented; oil/soy for ARG, oil for ECU |
| Dollarisation channel (ECU 2000) | DIRECTION_ONLY | — | N/A | Engine models the fiscal transmission but not full dollarisation pass-through |
| Ecological costs | DIRECTION_ONLY | DIRECTION_ONLY | DIRECTION_ONLY | Global estimates only |

---

### (c) Immediately runnable backtesting scenarios

**Scenario LAT-1 — Argentina 2001 default and dollarisation exit (Type A + Type B)**  
*Fixtures:* `backend/tests/fixtures/argentina_2001_2002_scenario.py`; `argentina_2001_2002_actuals.py`  
*Entity:* ARG | *Period:* 2001–2002 | *Steps:* ≥3 | *Types:* A (historical) + B (Zero Deficit Plan counter-factual)  
*Historical context:* Argentina's 2001 crisis saw sovereign default ($100bn), abandonment of the Convertibility Plan (dollar peg), mass unemployment (21%), and a poverty headcount that reached ~57%. The Zero Deficit Law of July 2001 attempted radical fiscal retrenchment before the December default. The Duhalde government devalued and defaulted in January 2002; the Kirchner recovery began in 2003.  
*Question posed (Type B):* Does the engine find that the Zero Deficit Plan counter-factual (sustained primary surplus via spending cuts) would have worsened the human development trajectory relative to default and devaluation?  
*Known historical outcome:* Zero Deficit Plan failed within months; default and devaluation produced severe short-term contraction followed by strong recovery under the Kirchner debt restructuring framework (2005 PSI).  
*Expected fidelity tier:* DIRECTION_ONLY (fiscal multiplier); MAGNITUDE conditional (external balance via Céspedes & Velasco commodity linkage)

**Scenario LAT-2 — Argentina Kirchner recovery (Type A)**  
*Fixture:* CM-D inputs (from ELASTICITY_REGISTRY CM-D calibration; no separate fixture file — requires configuration using CM-D parameters)  
*Entity:* ARG | *Period:* 2003–2007 | *Steps:* 4–6 | *Type:* A (historical replay)  
*Historical context:* The 2003–2007 recovery under Presidents Duhalde (2002–2003) and Kirchner (2003–2007) achieved rapid GDP growth (~8–9% annually) driven by commodity exports, debt restructuring, and heterodox domestic demand expansion. Poverty fell from ~57% to ~21% by 2007.  
*Question posed:* Does the engine correctly find upward direction on human development indicators during the Kirchner recovery period, consistent with the documented poverty decline?  
*Known historical outcome:* Poverty headcount fell sharply; HDI improved; GDP grew at high single/double-digit rates; fiscal balance improved with commodity revenues.  
*Expected fidelity tier:* DIRECTION_ONLY (fiscal channel); MAGNITUDE conditional (external balance/commodity; poverty direction)

**Scenario LAT-3 — Ecuador 1999 dollarisation crisis (Type A)**  
*Fixtures:* `backend/tests/fixtures/ecuador_1999_2000_scenario.py`; `ecuador_1999_2000_actuals.py`  
*Entity:* ECU | *Period:* 1999–2000 | *Type:* A (historical replay)  
*Historical context:* Ecuador experienced a severe banking crisis in 1999, froze bank deposits (corralito-style banking freeze), defaulted on Brady bonds, and dollarised in January 2000 after the sucre depreciated ~200%. GDP contracted ~6% in 1999.  
*Question posed:* Does the engine correctly identify the direction of GDP contraction and human development deterioration in the crisis year, with the fin_composite showing downward direction in the crisis step?  
*Known historical outcome:* GDP contracted; poverty worsened significantly in 1999; partial recovery began post-dollarisation 2001.  
*Expected fidelity tier:* DIRECTION_ONLY

---

### (d) Known gaps

- `BOL` and `PER` have no backtesting fixtures. Both are structural analogues only.
- Brazil (`BRA`) is absent from the registered family entirely. This is a significant gap: Brazil is the obvious regional comparator for Argentina but is not in the CM-B/D calibration family. Brazil's larger domestic demand, different exchange rate regime history, and distinct political-economy context make it a poor fit for the Ilzetzki et al. LAC range without separate literature calibration.
- No fixture for Latin American debt restructuring in the 1980s (Brady era) — the historical predecessor to the 2001 Argentine case is not currently modelled.
- Egypt (`EGY`) has a fixture (`egypt_2016_scenario.py`) but is not in any registered calibration family. Egypt is MENA-context, not LAC. The engine can run EGY scenarios but without a registered family, fidelity claims are unanchored. This is a gap requiring a fifth family registration (MENA-EM) or explicit gap declaration.
- Turkey (`TUR`) similarly has `turkey_2018_scenario.py` but no registered family. Turkey is a large open emerging market that fits neither LAC nor South/SE Asian frameworks.
- The engine does not currently model capital flight dynamics explicitly — a key channel in the Argentina 2001 case. The MDA threshold for capital flight is not in the ELASTICITY_REGISTRY.

---

## Family 4 — SOUTH-SE-ASIAN (South and Southeast Asian)

**Calibration basis:** Batini, Callegari, and Melina (2012) + IMF APAC REO. All multiplier estimates T3. PAK, LKA, BGD all CM-C. See `docs/evidence/analytical-framework.md §1 Family 4`.

---

### (a) Entities covered — data tier assessment

| Entity | Common name | Fixture file | Data tier (fiscal) | Data tier (human dev.) | Data tier (external balance) | Calibration model |
|---|---|---|---|---|---|---|
| `PAK` | Pakistan | `pakistan_2022_scenario.py` ✓ | T3 — Batini et al. 2012 / APAC REO | T2 — PBS household survey; World Bank WDI | T2 — IMF Article IV 2022; SBP data | CM-C |
| `LKA` | Sri Lanka | `sri_lanka_2022_scenario.py` ✓ | T3 — Batini et al. 2012 / APAC REO | T2 — DCS household survey; WDI | T2 — IMF Article IV 2022; CBSL data | CM-C |
| `BGD` | Bangladesh | No dedicated fixture | T3 — structural analogue | T3 — partial WDI (BBS partial) | T3 — APAC range | CM-C structural analogue |

**ELASTICITY_REGISTRY entries for this family:**  
- Q1 FORMAL (IMF programme formal-sector channel): `ACADEMIC_LITERATURE_ILZETZKI_2013_FISCAL_MULTIPLIERS`, confidence_tier=3, entity_families={"PAK","LKA","BGD"}  
- Q2 FORMAL (Ball 2013): confidence_tier=3, entity_families={"PAK","LKA","BGD"}  
- LKA-specific Coffin Corner/fuel shortage FORMAL channel: `ACADEMIC_LITERATURE_IMF_IEO_2018_IMF_SOCIAL_PROTECTION`, confidence_tier=3  
- ZMB/SSA informal sector entry also fires on all entities (entity_families=None) as Q1 INFORMAL base

---

### (b) Fidelity ceiling — current calibration state

| Indicator | Fidelity ceiling (PAK) | Fidelity ceiling (LKA) | Fidelity ceiling (BGD) | Limiting factor |
|---|---|---|---|---|
| GDP trajectory direction | DIRECTION_ONLY | DIRECTION_ONLY | DIRECTION_ONLY | T3 multiplier (APAC range wide) |
| Fiscal balance direction | DIRECTION_ONLY | DIRECTION_ONLY | DIRECTION_ONLY | Linked to T3 multiplier |
| External balance (BOP) direction | DIRECTION_ONLY | DIRECTION_ONLY | DIRECTION_ONLY | T2 balance data available but T3 multiplier propagation |
| Human development direction | DIRECTION_ONLY | DIRECTION_ONLY | DIRECTION_ONLY | T2 household data available; linkage model T3 prevents MAGNITUDE |
| Debt sustainability direction | DIRECTION_ONLY | DIRECTION_ONLY | DIRECTION_ONLY | DSA-trajectory produces direction; T3 multiplier propagates throughout |
| Fuel/supply chain disruption (LKA) | DIRECTION_ONLY | DIRECTION_ONLY | N/A | LKA Coffin Corner fuel shortage channel modelled but T3 |
| Remittance channel | DIRECTION_ONLY | DIRECTION_ONLY | DIRECTION_ONLY | Not separately calibrated in ELASTICITY_REGISTRY for any SOUTH-SE-ASIAN entity; major structural gap for BGD and PAK |
| Ecological costs | DIRECTION_ONLY | DIRECTION_ONLY | DIRECTION_ONLY | Global estimates only |

---

### (c) Immediately runnable backtesting scenarios

**Scenario SEA-1 — Pakistan 2022 SBA compliance programme (Type A + Type B)**  
*Fixture:* `backend/tests/fixtures/pakistan_2022_scenario.py`  
*Entity:* PAK | *Period:* 2022–2023 | *Type:* A (SBA compliance path) + B (programme deviation counter-factual)  
*Historical context:* Pakistan entered a Stand-By Arrangement with the IMF in 2023 following severe balance-of-payments stress, fuel subsidy crisis, and political instability. The programme required front-loaded fiscal consolidation and energy price reforms. Pakistan avoided sovereign default (contrast with Sri Lanka 2022).  
*Question posed (Type B):* Does the engine find that the programme-deviation counter-factual (fuel subsidy maintenance, delayed consolidation) leads to worse external balance direction and earlier threshold breach than the SBA compliance path?  
*Known historical outcome:* Pakistan maintained IMF programme compliance with difficulty; currency depreciated significantly; poverty worsened in the short term; default avoided. Sri Lanka's simultaneous default provides the within-family comparator.  
*Expected fidelity tier:* DIRECTION_ONLY

**Scenario SEA-2 — Sri Lanka 2022 Coffin Corner entry and EFF programme (Type A)**  
*Fixture:* `backend/tests/fixtures/sri_lanka_2022_scenario.py`  
*Entity:* LKA | *Period:* 2022–2023 | *Type:* A (Coffin Corner entry replay)  
*Historical context:* Sri Lanka's 2022 crisis was the most severe in the current fixture set: sovereign default (May 2022, first in its history), fuel shortages, medicine scarcity, power outages of up to 13 hours/day, and mass public protests that led to the President's resignation (July 2022). The Extended Fund Facility with the IMF was agreed in March 2023 after bilateral debt restructuring with China and India.  
*Question posed:* Does the engine correctly identify the Coffin Corner entry — simultaneous downward pressure on fiscal balance, external balance, human development, and governance legitimacy — from the fuel shortage step onward?  
*Known historical outcome:* All four framework dimensions deteriorated simultaneously 2022 Q1–Q3; governance failure (presidential resignation) confirmed the Coffin Corner characterisation; MDA thresholds for poverty and external balance both breached.  
*Expected fidelity tier:* DIRECTION_ONLY (all dimensions); note that simultaneous multi-dimension directional convergence is itself a DIRECTION_ONLY claim with high evidential value

---

### (d) Known gaps

- `BGD` has no backtesting fixture. Bangladesh's 2022–2023 reserve depletion episode (foreign reserves fell from $46bn to $20bn) is a natural next fixture: within-family contemporary with PAK/LKA; would enable three-entity within-family comparison.
- **Remittance channel is absent from the ELASTICITY_REGISTRY for all three entities.** Remittances are critical for PAK (~8% GDP), LKA (~8% GDP), and BGD (~6–7% GDP). The engine does not model remittance inflows as a stabilising channel or their disruption as a downside shock. This is a structural gap that ceilings the human development fidelity: the poverty headcount direction verdict is systematically missing a major income buffer.
- No Southeast Asian entity (THA, VNM, IDN, PHL) is in the registered family. Thailand (`THA`) has a fixture (`thailand_1997_2000_scenario.py`) for the Asian financial crisis but is not in any registered calibration family. The Batini et al. (2012) framework covers South Asian SBA-context scenarios well but does not extend naturally to Southeast Asian open economy crises.
- India (`IND`) is absent. Given India's weight in South Asian regional dynamics, this is a structural gap for any scenario involving Pakistani or Sri Lankan contagion or regional spillovers.
- No entity in this family achieves MAGNITUDE tier at current calibration. Upgrading any SOUTH-SE-ASIAN entity to MAGNITUDE would require either: (a) a country-specific multiplier study at T2 quality, or (b) IMF-endorsed fiscal multiplier estimates for the specific episode (not currently available in the literature).

---

## Regional Benchmarking Section

Regional benchmarking pairs allow within-family cross-entity directional comparisons. Per the Error Envelope Principle (`docs/evidence/analytical-framework.md §2`), entities sharing a calibration family can be compared for directional ordering — which shows worse/better direction on a given indicator — but not for magnitude.

---

### Pair 1 — Ghana vs Côte d'Ivoire (SSA-LIC family)

| Dimension | Assessment |
|---|---|
| **GHA data availability** | Fixture present (`ghana_2022_scenario.py`); IMF Article IV 2022 at T2 for fiscal/external; WDI T2 for human development |
| **CIV data availability** | No fixture; WDI data available at T2+ for some indicators (cocoa price linkage documented); IMF Article IV available |
| **Shared error envelope** | Yes — both SSA-LIC (Fosu 2011 regional elasticities apply to both); cross-entity comparison is valid for directional ordering |
| **Shared error envelope confirmation** | Both entities use SSA Q1 INFORMAL (entity_families=None); neither has entity-specific formal sector overrides; the calibration uncertainty is identical for both |
| **Directional statement (DIRECTION_ONLY)** | Both GHA (2022) and CIV (comparable commodity-dependent structural profile) would show downward fiscal direction under primary balance shock. GHA shows earlier threshold breach timing due to documented higher initial debt burden (>90% GDP in 2022 vs CIV ~60%). Directional ordering valid; magnitude comparison invalid. |
| **Gap** | CIV has no fixture — cannot currently run the comparison. Fixture creation would require CIV scenario configuration using Fosu 2011 SSA calibration and the 2020–2023 cocoa price cycle as the primary external driver |

---

### Pair 2 — Greece vs Portugal (EURO-AREA family)

| Dimension | Assessment |
|---|---|
| **GRC data availability** | Full fixture + CM-A calibration + ADR-007 posterior; Eurostat T2 for fiscal, human development, labour market, external balance |
| **PRT data availability** | No dedicated fixture; Eurostat T2 data available for all primary indicators; Ilzetzki et al. 2013 applies directly; IMF/Troika programme data at T2 |
| **Shared error envelope** | Yes — both EURO-AREA (Ilzetzki et al. 2013); same multiplier literature; fixed exchange rate regime (Euro) for both 2010–2014 period |
| **Shared error envelope confirmation** | GRC uses CM-A confidence_tier=2 entries; PRT would use EURO-AREA general (same literature, no dedicated calibration). The Ilzetzki et al. estimate is the same for both — error envelope shared |
| **Directional statement (MAGNITUDE)** | Both GRC and PRT show downward GDP and human development direction under Troika fiscal consolidation. GRC shows more severe trajectory direction than PRT by MAGNITUDE (GDP contraction ~25% vs ~8% cumulative). The within-family ordering is valid: GRC fiscal shock was larger in absolute terms and the starting debt burden was higher. A Portugal fixture would allow the engine to reproduce this within-family ordering directly. |
| **Gap** | PRT fixture does not yet exist. Creating it would allow the EURO-AREA family's first within-family cross-entity MAGNITUDE comparison — directly testing the error envelope principle claim that GRC outperforms PRT is not in the current evidence portfolio |

---

### Pair 3 — Argentina vs Brazil (LATAM-EM family)

| Dimension | Assessment |
|---|---|
| **ARG data availability** | Full fixture + CM-B + CM-D; MECON/IMF T2 for external balance; T3 fiscal |
| **BRA data availability** | No fixture; **Brazil is not in the registered LATAM-EM calibration family** |
| **Shared error envelope** | **No — BRA is not in any registered calibration family** |
| **Directional statement** | **Invalid — no shared error envelope; cross-entity comparison not currently supported** |
| **Structural reason for exclusion** | Brazil's domestic demand-driven economy, larger manufacturing base, and distinct exchange rate regime history mean the Ilzetzki et al. LAC multiplier range does not apply with the same structural grounding as for ARG, ECU, BOL, PER. A separate Brazil calibration (CM-E or similar) would require its own literature basis |
| **Gap** | This is the largest missing comparator in the LATAM-EM family. An ARG vs BRA comparison is the most natural policy question in Latin American fiscal analysis — "did Argentina's heterodox path outperform Brazil's orthodox approach?" — and the current engine cannot answer it within a shared error envelope. Brazil family registration is a medium-priority gap for the AEP |

---

### Pair 4 — Pakistan vs Sri Lanka (SOUTH-SE-ASIAN family)

| Dimension | Assessment |
|---|---|
| **PAK data availability** | Fixture present (`pakistan_2022_scenario.py`); IMF Article IV 2022 T2; SBP data T2 for external balance |
| **LKA data availability** | Fixture present (`sri_lanka_2022_scenario.py`); IMF Article IV 2022 T2; CBSL data T2 for external balance |
| **Shared error envelope** | Yes — both SOUTH-SE-ASIAN, CM-C; same Batini et al. 2012 / APAC REO multiplier range; same confidence_tier=3 elasticities in registry |
| **Shared error envelope confirmation** | Both use LATAM-EM LAC Q1 FORMAL and Q2 FORMAL entries at confidence_tier=3 with entity_families={"PAK","LKA","BGD"} — identical calibration uncertainty applies to both |
| **Directional statement (DIRECTION_ONLY)** | Both PAK and LKA show downward direction on fiscal, external balance, and human development under their respective 2022 crises. The directional ordering: LKA shows earlier and more severe threshold breach (Coffin Corner entry including governance collapse), while PAK maintained programme compliance and avoided default. This directional ordering — LKA worse than PAK on timing of threshold breach — is valid within the shared error envelope and represents the most immediately demonstrable within-family comparison in the current portfolio |
| **Gap** | The remittance channel is absent for both (major structural gap noted above). The PAK/LKA comparison currently underestimates the stabilising role of remittances in both cases. Adding a remittance elasticity would change the quantitative direction of the external balance channel for both entities equally — preserving the relative ordering claim but changing the absolute direction verdict for individual steps |

---

## Summary: Coverage Gaps Requiring Action

| Gap | Family | Priority | Suggested action |
|---|---|---|---|
| PRT backtesting fixture | EURO-AREA | High — enables first EURO-AREA within-family cross-entity comparison | Create `prt_2010_scenario.py` using Eurostat Troika-era data |
| BGD backtesting fixture | SOUTH-SE-ASIAN | High — completes the CM-C family's three registered entities | Create `bgd_2022_scenario.py` using IMF reserve depletion episode |
| Remittance channel in ELASTICITY_REGISTRY | SOUTH-SE-ASIAN | High — structural gap affecting PAK/LKA/BGD human development fidelity | Add remittance-inflow elasticity and disruption channel to registry |
| BRA calibration family registration | LATAM-EM | Medium — unlocks most natural LAC cross-entity comparison | Requires CM-E or literature identification; separate AEA session |
| CIV backtesting fixture | SSA-LIC | Medium — enables SSA-LIC within-family comparison for GHA | Create `civ_2022_scenario.py` using cocoa price cycle |
| ETH, KEN fixtures | SSA-LIC | Low — structural analogues, limited priority | Would expand the SSA fixture library; not blocking for evidence quality |
| IRL, CYP fixtures | EURO-AREA | Low — Euro-area crisis covered by GRC/ISL | Would round out the EURO-AREA family; PRT is higher priority |
| MENA-EM family registration | None currently | Medium — EGY, JOR, LBN have fixtures but no family | Requires new calibration family with appropriate literature source (IMF MENA REO + Cerra & Saxena 2008?) |
| Southeast Asia (THA, IDN, PHL, VNM) | None currently | Medium — THA has fixture, no family | Separate from South Asian CM-C; would require Ramey (2016) or IMF ASEAN estimates |
| Capital flight channel | LATAM-EM | Medium — key in ARG 2001; not in ELASTICITY_REGISTRY | Would require Ilzetzki et al. plus BIS capital flow data |

---

*Audit authored by: AEA*  
*Status: `DRAFT — awaiting EL review`*  
*Next audit: M20 close, after any new fixture or calibration family is registered*
