# WorldSim Analytical Evidence Portfolio — Analytical Framework

> **Authority:** Analytical Evidence Agent (AEA), with Chief Methodologist review  
> **Panel:** AEA (lead), Chief Methodologist (calibration and uncertainty), Political Economist (scenario framing validity)  
> **Status:** ACTIVE — supersedes any prior informal calibration notes  
> **Cross-reference:** `docs/evidence/TEMPLATE.md` (entry template), `docs/DATA_STANDARDS.md §Confidence Tier System` (data tier definitions), `docs/architecture/simulation-framework.md` (engine specification)

This document governs how WorldSim Analytical Evidence Portfolio (AEP) entries are calibrated, categorised, compared, and cited. It is the epistemic foundation for the AEP — every fidelity claim in every entry references this framework. Read it before populating any entry template.

---

## 1. Calibration Family Taxonomy

WorldSim's fiscal and macroeconomic channels rely on literature-derived elasticity estimates. The confidence tier and fidelity ceiling of any AEP entry depend on which calibration family governs the entity being run, and whether country-specific data is available to move beyond the literature range.

Four calibration families are currently registered. Each family is defined by its primary literature source, the entities it covers, the typical confidence tier for fiscal multiplier estimates, and the resulting per-indicator fidelity ceiling.

---

### Family 1 — SSA-LIC (Sub-Saharan Africa Low Income Countries)

**Primary literature source:**  
Fosu, A.K. (2011). Growth, Inequality, and Poverty Reduction in Developing Countries: Regional and Time Dimensions. *African Development Review*, 23(4), 434–456. Growth-poverty elasticity linkages for SSA; IMF *Africa Regional Economic Outlook* (AFRO/REO) for fiscal multiplier range calibration.

**Registered entities:**  
`SEN` (Senegal), `ZMB` (Zambia), `GHA` (Ghana), `ETH` (Ethiopia — structural analogue, no dedicated fixture), `KEN` (Kenya — structural analogue, no dedicated fixture)

**Backtesting fixtures available (M19 onward):**  
SEN — 2000–2015 structural adjustment and growth recovery period  
ZMB — 2005–2015 copper boom, fiscal consolidation, and debt ceiling period  
GHA — 2022–2023 IMF programme entry (G2E)

**Confidence tier for fiscal multiplier estimates:** T3 — synthetic, derived from AFRO literature range; no country-specific multiplier studies at the resolution required for T2 classification.

**Per-indicator fidelity ceiling:**

| Indicator category | Fidelity ceiling | Basis |
|---|---|---|
| GDP trajectory direction | DIRECTION_ONLY | T3 multiplier; cross-country synthesis |
| Fiscal balance direction | DIRECTION_ONLY | Linked to GDP via T3 multiplier |
| Human development trajectory direction | MAGNITUDE (conditional) | Fosu (2011) growth-poverty elasticities provide T2 linkage where World Bank WDI data at T2+ quality |
| Poverty headcount direction | DIRECTION_ONLY (general); MAGNITUDE (conditional on T2 WDI data) | |
| Current account direction | DIRECTION_ONLY | IMF AFRO range; no entity-specific trade elasticities |
| Ecological cost direction | DIRECTION_ONLY | LULC + NOAA global estimates; no country-specific intensity data |

**When MAGNITUDE is achievable within this family — two-condition rule (CM-endorsed, 2026-07-07):**  
Human development and poverty indicators can reach MAGNITUDE tier only when **both** of the following conditions are satisfied:

1. **T2 WDI data:** World Bank WDI data for the specific entity and scenario period is classified T2 or higher, enabling the Fosu (2011) growth-poverty elasticity to be applied to grounded inputs rather than inferred regional averages.
2. **Fixture direction validation:** A backtesting fixture exists for that entity and includes at least one step where the engine's human development direction verdict has been confirmed to agree with historical actuals. This validates that the Fosu (2011) regional elasticity produces directionally correct outputs for that entity's structural context — a necessary condition before per-step magnitude ordering claims are made.

**Condition 1 alone is not sufficient.** The Fosu (2011) elasticity is a regional SSA cross-country estimate. Without fixture validation (condition 2), T2 data supports the *application* of the elasticity but not *magnitude ordering* claims — because an unvalidated regional elasticity could be systematically wrong in direction for a specific entity, which would invalidate any ordering derived from it.

**Current status:** SEN, ZMB, and GHA satisfy both conditions (T2 WDI data + dedicated fixture). ETH and KEN do not satisfy either condition (partial WDI at T3; no dedicated fixture) and remain DIRECTION_ONLY on human development indicators regardless of any future improvement in WDI data quality until a fixture is created and direction-validated.

---

### Family 2 — EURO-AREA (Euro Area — Advanced Economy Fixed Exchange Rate Regime)

**Primary literature source:**  
Ilzetzki, E., Mendoza, E.G., and Végh, C.A. (2013). How Big (Small?) are Fiscal Multipliers? *Journal of Monetary Economics*, 60(2), 239–254. Impact multiplier estimates for advanced economies under fixed exchange rate regimes; high-debt-regime estimates applied for 2010-era crisis scenarios.

**Registered entities:**  
`GRC` (Greece — full T2 calibration, CM-A), `PRT` (Portugal), `IRL` (Ireland), `CYP` (Cyprus)

**Backtesting fixtures available (M19 onward):**  
GRC — 2010–2015 Troika adjustment programme (G2A); primary fixture with Ilzetzki et al. high-debt-regime multiplier range

**Confidence tier for fiscal multiplier estimates:**  
`GRC`: T2 — Ilzetzki et al. (2013) directly applicable; IMF WEO and Eurostat data at T2 quality for the 2010–2015 period. CM-A calibration (M19) validated against historical actuals.  
`PRT`, `IRL`, `CYP`: T2 literature estimate applicable; dedicated fixture calibration not yet validated.

**Per-indicator fidelity ceiling:**

| Indicator category | Fidelity ceiling (GRC, CM-A) | Fidelity ceiling (other EURO-AREA) | Basis |
|---|---|---|---|
| GDP trajectory direction | CALIBRATED_CI | MAGNITUDE | CM-A: Bayesian posterior from ADR-007; others: T2 literature without country posterior |
| Fiscal balance | MAGNITUDE | MAGNITUDE | IMF consolidation path data at T2 |
| Human development direction | MAGNITUDE | DIRECTION_ONLY | EUROSTAT SILC at T2 for GRC; thinner data for others |
| Unemployment trajectory | MAGNITUDE | MAGNITUDE | Eurostat LFS at T2 for all registered entities |
| Current account | MAGNITUDE | DIRECTION_ONLY | EUROSTAT BOP at T2 for GRC; country fixture needed for others |
| Ecological cost direction | DIRECTION_ONLY | DIRECTION_ONLY | EEA land use estimates; global uncertainty dominates |

**Note on GRC CALIBRATED_CI ceiling:**  
ADR-007 Bayesian posterior layer (M19) established the CALIBRATED_CI tier for GRC fiscal multiplier outputs. This is the only currently registered entry-level CALIBRATED_CI ceiling. Other indicators within the GRC fixture may remain at MAGNITUDE tier; the CI label applies only to the fiscal multiplier channel and its directly linked outputs.

---

### Family 3 — LATAM-EM (Latin American Emerging Market — Open Economy, Managed Float or Currency Board)

**Primary literature sources:**  
Ilzetzki, E., Mendoza, E.G., and Végh, C.A. (2013) — LAC developing country range (impact multiplier estimates substantially lower than advanced economy estimates, typically negative to near-zero on impact for high-debt open economies).  
Céspedes, L.F. and Velasco, A. (2012). Macroeconomic Performance During Commodity Price Booms and Busts. *IMF Economic Review*, 60(4), 570–599. External adjustment dynamics and commodity terms-of-trade sensitivity for LAC.

**Registered entities:**  
`ARG` (Argentina — T3 fiscal, CM-B general + CM-D Kirchner recovery specific), `ECU` (Ecuador), `BOL` (Bolivia), `PER` (Peru)

**Backtesting fixtures available (M19 onward):**  
ARG — 2001–2002 default and dollarisation exit (G2B); 2003–2007 Kirchner recovery (CM-D inputs)

**Confidence tier for fiscal multiplier estimates:** T3 for all — Ilzetzki et al. LAC range is wide; no country-specific multiplier studies at T2 quality for the scenario periods covered. CM-D provides ARG-specific recovery-period calibration inputs but remains T3 in confidence (synthetic from Kirchner-era observed data without formal posterior estimation).

**Per-indicator fidelity ceiling:**

| Indicator category | Fidelity ceiling (ARG, CM-D period) | Fidelity ceiling (other LATAM-EM) | Basis |
|---|---|---|---|
| GDP trajectory direction | DIRECTION_ONLY | DIRECTION_ONLY | T3 multiplier; LAC range too wide for MAGNITUDE |
| Fiscal balance direction | DIRECTION_ONLY | DIRECTION_ONLY | Linked to T3 multiplier |
| External balance direction | MAGNITUDE (conditional) | DIRECTION_ONLY | Céspedes & Velasco (2012) TOT framework; ARG-specific trade data at T2 for some periods |
| Poverty/inequality direction | DIRECTION_ONLY | DIRECTION_ONLY | SEDLAC data partial; distributional linkage T3 |
| Commodity channel direction | MAGNITUDE (conditional) | MAGNITUDE (conditional) | Céspedes & Velasco (2012) directly applicable where commodity exposure is documented |
| Ecological cost direction | DIRECTION_ONLY | DIRECTION_ONLY | Global estimates only |

**Note on ARG Kirchner recovery (CM-D):**  
CM-D provides specific control input values for the 2003–2007 period calibrated against MECON and IMF data. These inputs improve scenario configuration accuracy but do not raise the fiscal multiplier tier above T3 — the multiplier remains a range estimate from Ilzetzki et al. LAC. The CM-D contribution is to the control input realism, not to the multiplier confidence.

---

### Family 4 — SOUTH-SE-ASIAN (South and Southeast Asian — Open Economy, IMF Programme Context)

**Primary literature sources:**  
Batini, N., Callegari, G., and Melina, G. (2012). Successful Austerity in the United States, Europe and Japan. IMF Working Paper WP/12/190. Provides cross-country austerity multiplier estimates including emerging market comparators.  
IMF *Asia and Pacific Regional Economic Outlook* (APAC REO) — annual; fiscal multiplier range estimates for South and Southeast Asian emerging markets.

**Registered entities:**  
`PAK` (Pakistan — CM-C), `LKA` (Sri Lanka — CM-C), `BGD` (Bangladesh — CM-C)

**Backtesting fixtures available (M19 onward):**  
PAK — 2022–2023 SBA IMF programme compliance scenario (G2F)  
LKA — 2022–2023 Coffin Corner entry and EFF programme (G2G)

**Confidence tier for fiscal multiplier estimates:** T3 for all — Batini et al. (2012) and APAC REO provide ranges rather than country-specific estimates; no T2 country-specific multiplier study available for the scenario periods covered.

**Per-indicator fidelity ceiling:**

| Indicator category | Fidelity ceiling | Basis |
|---|---|---|
| GDP trajectory direction | DIRECTION_ONLY | T3 multiplier; APAC range wide |
| Fiscal balance direction | DIRECTION_ONLY | Linked to T3 multiplier |
| External balance (BOP) direction | DIRECTION_ONLY | IMF APAC data at T2 for some periods but multiplier linkage T3 |
| Human development direction | DIRECTION_ONLY | WHO/UNDP data often T2; linkage model T3 |
| Debt sustainability direction | DIRECTION_ONLY | DSA-like trajectory; T3 multiplier propagates through |
| Ecological cost direction | DIRECTION_ONLY | Global estimates only |

---

## 2. Error Envelope Principle

The error envelope is the set of calibration uncertainties that affect a given harness run. Understanding which entries share an error envelope is the foundation for valid comparison.

**Within-family, same-scenario-type comparisons are valid for relative ordering.**  
When two branches of the same scenario use the same calibration family and the same multiplier estimate, the calibration uncertainty affects both branches equally. The relative ordering of branch outcomes — which path performs better on a given indicator — is therefore robust to the shared calibration uncertainty. This cancellation of shared error is the primary methodological strength of within-family branch comparison.

*Example valid comparison:* GRC orthodox Troika adjustment path vs GRC heterodox alternative — both branches use Ilzetzki et al. Euro-area multiplier. The relative ordering of their GDP trajectory directions is MAGNITUDE-valid because the error cancels in the comparison.

*Example invalid comparison:* GRC orthodox GDP trajectory vs ARG heterodox GDP trajectory stated as a magnitude comparison — these use different calibration families (EURO-AREA vs LATAM-EM), different multiplier estimates, and different data tiers. The error envelopes do not overlap in a way that permits magnitude comparison.

**Cross-family comparisons are DIRECTION_ONLY on relative ordering.**  
An analyst may state that both GRC and ARG scenarios show downward GDP direction under fiscal consolidation — this is a directional claim that survives cross-family comparison. An analyst may not state that GRC shows a 3× larger contraction than ARG based on AEP harness outputs — this magnitude comparison crosses error envelopes and is invalid.

**Cross-type comparisons (Type A vs Type B) require explicit methodological note.**  
A Type A (historical replay) output and a Type B (counter-factual branch) output from the same entity and period may be compared, but the comparison must be explicit about which is the observed path and which is the modelled alternative. Direction comparisons are valid; magnitude comparisons are only valid where both paths are within the same calibration family and the counter-factual branch uses only pre-branch-point data.

**Within-family, cross-entity comparisons are valid for directional ordering only.**  
Two entities within the same calibration family (e.g. SEN and ZMB, both SSA-LIC) may be compared for direction ordering — "SEN shows earlier downward human development inflection than ZMB under equivalent fiscal consolidation pressure." Magnitude comparisons between entities are not valid even within the same family, because entity-specific data quality varies.

---

## 3. Fidelity Tiers

Three tiers govern what an AEP entry may claim. The tier declared in an entry's header is the entry-level ceiling — the lowest tier across all primary indicators in that entry. Per-indicator tier may be higher, but no claim in the entry may exceed the entry-level ceiling declared in §1 (Header) of the entry.

---

### DIRECTION_ONLY

**What the analyst can state:**
- The simulation finds sustained [upward / downward / flat] direction on [indicator] under [path] over [step range]
- Path A shows [better / worse] trajectory direction than Path B on [indicator] over [step range]
- The simulation finds that [threshold] is [breached / not breached] under [path] at approximately [step / year]
- Across both paths, [indicator] direction is consistently [direction] — no path avoids it

**What the analyst cannot state:**
- The magnitude of any change (percentage points, absolute values, multiplier-derived magnitudes)
- Cross-family magnitude comparisons of any kind
- Predictions ("will" language — use "the simulation finds" or "the harness shows" instead)
- Claims about confidence intervals or posterior distributions

**Appropriate citation language:**  
> "WorldSim directional analysis (v[X.X.X], [calibration family] family) finds [specific directional claim]. This assessment is based on direction-of-movement outputs only; magnitude interpretation requires country-specific calibration data not available at this stage of the evidence portfolio."

**When to use DIRECTION_ONLY:**  
Any entry where the primary fiscal multiplier or key linkage elasticity is T3 (synthetic, literature-range). This includes all LATAM-EM and SOUTH-SE-ASIAN family entries by default, and SSA-LIC entries for fiscal and external balance indicators. When in doubt, default to DIRECTION_ONLY — upgrading tier requires explicit justification in §6 of the entry.

---

### MAGNITUDE

**What the analyst can state:**
- All DIRECTION_ONLY claims, plus:
- Within-family relative magnitude comparisons: "Path A shows approximately [N]× the rate of deterioration of Path B on [indicator]"
- Ordering of branch outcomes by magnitude within the shared error envelope
- Step-timing comparisons: "The threshold is breached [N] steps earlier under Path A than Path B"

**What the analyst cannot state:**
- Absolute predictions ("GDP will contract by X%")
- Cross-family magnitude comparisons
- Claims that exceed the calibration family's error envelope width

**Appropriate citation language:**  
> "WorldSim trajectory analysis (v[X.X.X], [calibration family] calibration — [primary literature source]) finds [directional + ordering claim] within the [family name] error envelope. Direct magnitude comparison with scenarios from other calibration families is not supported at this fidelity tier."

**When MAGNITUDE tier is valid:**  
An entry may claim MAGNITUDE tier on a specific indicator when: (a) the calibration family is EURO-AREA or SSA-LIC (conditional), (b) country-specific data for the indicator is T2 or higher, and (c) the literature source directly supports the elasticity estimate used. Document the justification explicitly in §6 of the entry.

---

### CALIBRATED_CI

**What the analyst can state:**
- All MAGNITUDE claims, plus:
- Confidence interval bounds on fiscal multiplier-derived outputs with explicit posterior basis
- Quantified uncertainty ranges: "[Indicator] trajectory falls within [lower bound, upper bound] at [CI level]% posterior probability under [path]"
- The ADR-007 Bayesian posterior layer result is valid for GRC fiscal multiplier outputs at CALIBRATED_CI tier

**What the analyst cannot state:**
- Predictions beyond the CI bounds as if they were impossible
- That other calibration families achieve equivalent CI precision without separate posterior estimation
- That CI bounds are frequentist confidence intervals — they are Bayesian credible intervals

**Appropriate citation language:**  
> "WorldSim calibrated analysis (v[X.X.X], [calibration family] calibration, ADR-007 Bayesian posterior, [CI level]% credible interval) finds [quantitative claim] with uncertainty range [[lower], [upper]]. This CI is conditional on the [primary literature source] prior and the [entity] data vintage."

**When CALIBRATED_CI tier is valid:**  
Currently, only GRC fiscal multiplier outputs from the ADR-007 posterior layer. Any future entry claiming CALIBRATED_CI tier must document the Bayesian prior, likelihood model, and posterior estimation process in §6 of the entry. Claims of CALIBRATED_CI without a documented posterior are treated as MAGNITUDE tier for citation purposes.

---

## 4. Temporal Blindfold Protocol

The temporal blindfold protocol applies to all Type B (counter-factual branch) entries. It is the mechanism that ensures the entry has evidential value — that the harness output constitutes a genuine test of the engine's analytical capability rather than a retrodiction fitted to known outcomes.

**Why the protocol exists:**  
Counter-factual entries compare a modelled alternative path against a known historical outcome. If the analyst consults the known outcome before configuring the scenario, the configuration can be (consciously or unconsciously) calibrated to match — producing an entry that appears to validate the engine when it does not. The temporal blindfold protocol prevents this by sealing the configuration before the output is read.

---

### Step 1 — Configuration Lock

Before running any Type B counter-factual entry:

1. **Identify the branch point year.** This is the year at which the counter-factual path diverges from historical actuals. All input data used in the configuration must have a vintage date on or before 31 December of the year preceding the branch point year.

2. **Verify data vintages.** For each input parameter, confirm its data source vintage against `docs/DATA_STANDARDS.md §Vintage Dating`. Parameters using data with vintage dates after the branch point cutoff must be replaced with pre-branch-point estimates or excluded.

3. **Commit the configuration.** Write the complete scenario configuration — including all control inputs, branch parameters, calibration family, and data source references — as a committed file in the repository. The commit hash is the tamper-evident timestamp seal.

4. **Record the commit hash in the entry header.** The `Temporal blindfold status` field must read: `BLINDED — config committed [YYYY-MM-DD] before run`.

The harness run may not begin until Step 1 is complete and the configuration is committed.

---

### Step 2 — Output Reading and Comparison

After the configuration is committed:

1. **Run the harness** against the committed configuration.

2. **Read the output** and populate §5 (Harness Output Summary) of the entry template. Do not consult historical actuals at this stage — read the harness output first.

3. **Compare to historical actuals.** After §5 is populated, open the historical record and compare. Document the direction agreement or disagreement in §6 (Fidelity Assessment) and §7 (Known Limitations).

4. **Record the comparison result honestly.** A harness output that diverges from historical actuals is not a failed entry — it is evidence about the engine's current fidelity boundary. The entry must document the divergence, its magnitude, and what the divergence implies about the model's limitations.

---

### Unblinded Entries

An entry is unblinded if:
- The historical outcome was consulted before the configuration was committed, or
- The configuration was modified after the initial run in response to observed output, or
- The data vintage cutoff was not enforced (i.e., post-branch-point data was used in configuration)

Unblinded entries are recorded as: `UNBLINDED — acknowledged; weight reduced`

Unblinded entries are valid AEP members. They may represent the best available evidence for a given scenario and should be retained. However:
- They are explicitly excluded from any claim that the engine produced a genuine prospective validation
- Their evidentiary weight in calibration discussions is reduced relative to blinded entries
- An unblinded entry that achieves high fidelity with historical actuals confirms model coherence, not predictive power

---

## 5. Defensive Posture Boundary

The WorldSim Analytical Evidence Portfolio exists to serve the same mission as the engine itself: to give vulnerable actors the same quality of scenario analysis that sophisticated institutions reserve for themselves. This section documents what the AEP is designed to do and — explicitly — what it is not.

**Grounding:**  
WorldSim founding document (`docs/vision/worldsim-founding-document.md`): "The tool builds situational awareness and defensive capability for vulnerable actors. It is not designed to help anyone execute financial attacks, identify exploitable vulnerabilities in adversaries, or amplify power asymmetries. The asymmetry we are correcting runs one direction. So does the tool."

This is not a constraint added to the AEA from outside — it is the founding design choice. The AEP is the tool's analytical record, and the defensive posture boundary applies to it as fully as to the engine.

---

**What the AEP is designed to support:**

- **Situational awareness** — giving a finance ministry analyst a structured view of where their economy sits relative to historical analogues, and what trajectory patterns have preceded threshold breaches in comparable cases
- **Scenario exploration** — running and documenting alternative policy paths so decision-makers can see the trajectory implications of choices before committing to them
- **Historical pattern recognition via backtesting** — documenting what the engine finds when run against historical cases, so analysts can assess where the engine's fidelity is strong and where it requires supplementation by domain expertise
- **Structured reasoning with explicit uncertainty** — replacing false confidence with calibrated directional assessments that analysts can cite with appropriate qualification

**What the AEP is not designed to support:**

- **Point prediction** — the engine is not a forecast, and AEP entries may not be cited as forecasts ("WorldSim predicts that GDP will contract by X%")
- **Investment return optimization** — AEP entries do not rank sovereign debt instruments, project bond spreads, or generate trade recommendations
- **Identifying exploitable vulnerabilities in adversary economies** — any use of AEP entries to identify crisis-inducing pressure points in a foreign government's policy space is outside scope and contrary to mission
- **Cross-country investment ranking** — cross-family magnitude comparisons are invalid (§2); AEP entries cannot be aggregated into sovereign ranking tables
- **Substituting for country-specific expert analysis** — the AEP is a structured complement to expert judgment, not a replacement for it. A DIRECTION_ONLY entry from a T3 calibration family is meaningful input to an expert's assessment; it is not a substitute for that assessment

**AEA scope boundaries (operative constraints):**

The AEA does not:
- Publish investment recommendations or cross-country rankings in AEP entries
- Make magnitude comparisons across calibration families
- Claim precision beyond the declared fidelity tier
- Modify the engine to improve entry outcomes
- Represent WorldSim's analytical capabilities externally without EL knowledge

These are not aspirational constraints. They are the operating boundaries within which the AEP maintains its integrity. An AEP entry that violates them is not a failed entry — it is an entry with an invalid claim that must be corrected before the portfolio is cited.

---

*Framework authored by: AEA (lead), with Chief Methodologist review*  
*Status: `DRAFT — awaiting EL review`*  
*Next review: M20 close, or when a new calibration family is registered*
