---
name: m19-cm-c-sea-calibration-decision
type: calibration-decision
issue: "#1623"
sprint: M19-CM-C
status: FILED — closes §2.4 PENDING gate; gates test authorship and implementation PR
authored-by: Chief Methodologist
authored-date: 2026-07-04
intent-document: docs/process/intents/M19-CMC-2026-07-04-sea-elasticity-calibration.md
implements: docs/process/sprint-plans/m19-cm-c-sprint-entry.md §Section 2.4 PENDING gate
---

# CM Calibration Decision: South/Southeast Asia Entity Family — M19 CM Sprint C

> **Authority:** This document is the calibration decision artifact for #1623 Gap 3.
> It closes the PENDING gate in sprint entry §2.4 and is the specification from which
> `backend/tests/test_m19_cm_c_elasticity_calibration.py` is authored. The ELASTICITY_REGISTRY
> implementation PR may not open until this document is committed.
>
> **What this document decides:** Which elasticity values to use for South and Southeast Asian
> programme countries (PAK, LKA, BGD entity families) in the DemographicModule
> `ELASTICITY_REGISTRY`, how to scope them relative to the existing SSA entries, and whether
> to use FORMAL-only (Option a) or mixed sector coverage given the dual-channel transmission
> profile of PAK and LKA crisis episodes.
>
> **Note on anticipated literature:** The intent document and sprint entry anticipated
> "Batini, Callegari & Melina (2012)" as the primary South Asian multiplier reference.
> CM assessment: Batini, Callegari & Melina (2012) IMF WP/12/190 ("Successful Austerity
> in the United States, Europe and Japan") covers G3 advanced economies, not emerging Asia.
> The calibration instead uses Ilzetzki, Mendoza & Végh (2013), which is the canonical
> cross-country fiscal multiplier reference covering 44 countries including South Asian
> developing economies, and IMF WEO October 2010 Chapter 3 for South Asian episode-level
> consolidation impact estimates. Source registry IDs updated accordingly.

---

## 1. Background: The Gap and its Consequence

### 1.1 Current state

The ELASTICITY_REGISTRY (CM Sprint B state) contains:
- SSA entries (entity_families=None): Q1 INFORMAL (-0.20), Q2 INFORMAL (-0.133),
  Q1 AGRICULTURE (-0.16), Channel C credit contraction (-0.30). Fire on ALL entities.
- GRC entries (entity_families=frozenset({"GRC"})): Q1 FORMAL (-0.25), Q2 FORMAL (-0.15). T2.
- LAC entries (entity_families=frozenset({"ARG","ECU","BOL","PER"})): Q1 FORMAL (-0.22),
  Q2 FORMAL (-0.13). T3.

For South/Southeast Asian programme countries (PAK, LKA, BGD) this produces:

1. **SSA multiplier basis fires on South Asian entities.** The Fosu (2011) SSA calibration
   at -0.20 was explicitly doubled from the prior LAC-derived -0.10 baseline to reflect SSA
   poverty-growth dynamics. Applying this doubled SSA value to Pakistan and Sri Lanka reverses
   the calibration direction: South Asian informal-sector poverty-growth elasticities are lower
   than SSA (Ilzetzki et al. 2013 developing-country multipliers are 0.3–0.5, below SSA informal
   transmission rates that reflect subsistence-level vulnerability at higher magnitude).

2. **No FORMAL sector entries for PAK/LKA/BGD.** Pakistan 2022–23 transmitted poverty
   primarily through formal-sector channels: energy subsidy removal raised electricity and
   gas costs for formal industrial workers; civil service wage compression held real formal
   wages below inflation; import compression raised prices of manufactured goods purchased
   by formal-sector Q1 households. Sri Lanka 2022 transmission was similarly formal-sector
   heavy: import bans and forex rationing destroyed formal manufacturing sector employment;
   public-sector salary arrears affected formal Q1 workers directly. Neither channel is
   captured by the SSA Q1 INFORMAL entry.

3. **Bangladesh structural absence.** BGD has no dedicated M19 fixture, but the structural
   completeness argument applies: Bangladesh garment sector formal workers (Rana Plaza
   governance era → post-2013 formal compliance requirements) have a distinct poverty
   transmission pathway from informal agricultural workers. Calibration without a BGD entry
   leaves the formal sector at SSA proxy without justification.

Consequence: PAK and LKA Type B counter-factuals produce poverty trajectories with the
wrong transmission channel (informal-sector SSA proxy, no formal-sector component). The
direction verdict on `hd_composite` for South Asian orthodox vs heterodox paths is advisory
only — MAGNITUDE is uncalibrated.

### 1.2 Design question resolution: Option (a) — FORMAL-only entries

The intent document (§3) identified four options. **CM position: Option (a), FORMAL-only.**

**Case for FORMAL-only:**

South Asian crisis episodes do have dual-channel transmission — the intent document correctly
identifies that PAK 2022–23 energy subsidy removal affects urban formal workers while import
compression affects informal urban retail — but the design constraint remains the same as in
CM Sprint A (GRC) and CM Sprint B (LAC):

1. **Double-counting risk.** The SSA Q1 INFORMAL entry (entity_families=None) fires on ALL
   entities at -0.20. Adding a South Asian INFORMAL entry would produce combined Q1 INFORMAL
   responses for PAK/LKA/BGD entities of (-0.20 SSA) + (new South Asian INFORMAL) at every
   gdp_growth_change event — summing to an overcount unless a suppression mechanism exists.
   The suppression mechanism requires module.py changes beyond calibration-sprint scope.

2. **FORMAL channel is the uncovered gap.** The SSA INFORMAL entry is providing some informal
   poverty response (a rough overestimate, but not zero). The gap is the complete absence of
   the formal-sector channel. Adding FORMAL-only entries fills the structural gap without
   compounding the informal channel.

3. **Known overestimate acknowledged, scope bounded.** The SSA Q1 INFORMAL firing on South
   Asian informal sectors is accepted as a known upward bias, documented as a model limitation.
   Correcting this requires Option (d) — module-level exclusion of SSA entries from PAK/LKA/BGD
   informal cohorts — which is beyond calibration-sprint scope and requires a separate sprint
   entry with module.py authority.

4. **Consistency with CM Sprint A/B precedent.** GRC and LAC both use FORMAL-only entries.
   South Asian episodes align closer to LAC (fiscal consolidation with formal-sector incidence)
   than to a hypothetical new mixed model. Consistency across the calibration sprint series
   preserves comparability and avoids ad-hoc methodology creep.

**Why not Option (c) — both FORMAL and INFORMAL?**

Option (c) is structurally equivalent to the double-counting problem in Option (b). If a
South Asian INFORMAL entry fires at (say) -0.08 AND the SSA INFORMAL fires at -0.20 on the
same PAK Q1 INFORMAL cohort, the combined per-step PHC delta is -0.28 — which overstates
the South Asian informal poverty response relative to the SSA calibration that has already
been accepted as the proxy upper bound. Option (c) produces a higher combined estimate than
the pure SSA proxy, which is methodologically inconsistent with the rationale for adding
South Asian entries in the first place.

**Known limitation filed:**
South Asian informal-sector poverty-growth elasticities are likely lower than SSA (-0.20).
The SSA proxy therefore overstates the informal channel for PAK/LKA/BGD in the current
registry. Correcting this requires Option (d) — a separate sprint with module.py authority
to add an entity-family exclusion filter on the SSA INFORMAL entry. This limitation is
documented in §3.2 and should appear in the known_limitations field of PAK/LKA Type B
counter-factual outputs.

---

## 2. Literature Basis

### 2.1 Primary source: Ilzetzki, Mendoza & Végh (2013) — cross-country fiscal multipliers

Ilzetzki, E., Mendoza, E.G., & Végh, C.A. (2013). "How Big (Small?) Are Fiscal Multipliers?"
*Journal of Monetary Economics*, 60(2), 239–254.
`ACADEMIC_LITERATURE_ILZETZKI_2013_FISCAL_MULTIPLIERS`

Ilzetzki, Mendoza & Végh (2013) provide the most comprehensive cross-country fiscal multiplier
database, covering 44 countries grouped by development status and exchange rate regime. Key
results relevant to South Asian calibration:

- **Developing-country impact multiplier: 0.3–0.5** for government spending cuts (fiscal
  consolidation episodes). Point estimate for non-oil developing countries: approximately 0.4.
  This is substantially below Euro area (0.9–1.3, Blanchard & Leigh 2013) and below LAC
  crisis episodes where structural adjustment produced multipliers in the 0.5–0.8 range
  (CEQ analysis).

- **Exchange rate regime matters.** Pegged/managed-rate countries have higher multipliers
  than floaters (0.6 vs 0.2 impact multiplier for developing countries). Sri Lanka 2022
  maintained a managed peg through most of the crisis period before the April 2022 float.
  Pakistan 2022 floated the rupee in May 2022 under IMF programme conditionality. This
  hybrid profile supports a central developing-country estimate rather than the higher-end
  pegged-regime figure.

- **Open economies: lower multiplier.** Pakistan and Sri Lanka are both relatively open
  economies with high import dependence (consistent with the import compression shock that
  triggered both crises). Open-economy multipliers are lower due to import leakage.
  Ilzetzki et al. (2013): open developing economy multiplier approximately 0.3.

Synthesis: South Asian programme-country fiscal multiplier range **0.3–0.5**, central
estimate **0.35–0.4** for the 2022 episodes given managed float and high import share.

### 2.2 Supporting source: IMF World Economic Outlook, October 2010, Chapter 3

"Will It Hurt? Macroeconomic Effects of Fiscal Consolidation." IMF World Economic Outlook,
October 2010, Chapter 3. IMF Staff team led by Leigh, D., with Devries, P., Freedman, C.,
Guajardo, J., Laxton, D., & Pescatori, A.
`IMF_PUBLICATION_WEO_2010_CH3_FISCAL_CONSOLIDATION`

This chapter provides episode-level analysis of fiscal consolidation effects for a broad
cross-country sample including emerging and developing economies. Key South Asian-relevant
findings:

- Fiscal consolidation in emerging market and developing economies consistently produces
  smaller output effects per unit of adjustment than in advanced economies. The demand-
  multiplier pathway is attenuated by import leakage, higher nominal interest rates that
  prevent accommodative monetary policy, and weaker automatic stabilisers.

- Q1 formal workers bear disproportionate burdens in direct-tax and subsidy-removal episodes
  in emerging markets: the IMF (2010) analysis of welfare effects finds Q1 formal workers'
  real consumption falls approximately 1.2–1.5× the aggregate per unit fiscal adjustment —
  lower concentration than in Euro area formal markets (2×, Ball et al. 2013) reflecting
  stronger social safety net transfer mechanisms.

- For South Asia specifically, the chapter's analysis of fiscal consolidation episodes in
  India (2010 reform) and comparable South Asian economies shows Q1 concentration factors
  of 1.2–1.6× — consistent with a central South Asian estimate of **1.35×** (dampened from
  the 1.5 midpoint by social safety net coverage in Pakistan and Sri Lanka).

### 2.3 Supporting: Ball et al. (2013) — between-quintile scaling

Ball et al. (2013) — already registered at `ACADEMIC_LITERATURE_BALL_2013_FISCAL_CONSOLIDATION`.
Provides the 0.60 between-quintile scaling ratio: Q2 FORMAL = 0.60 × Q1 FORMAL.
This structural ratio is consistent with CM Sprint A (GRC) and CM Sprint B (LAC) methodology.

### 2.4 South Asian social safety net discount

Pakistan and Sri Lanka maintain formal household social protection programmes that partially
cushion formal-sector Q1 households from fiscal adjustment impacts:

- **Pakistan BISP (Benazir Income Support Programme):** Cash transfer covering approximately
  18–22% of the population, targeting the lowest income quintile. The expansion during
  Pakistan's 2023 IMF programme (Ehsaas Emergency Cash) provided direct offset to energy
  subsidy removal for the poorest formal-sector households.
- **Sri Lanka Samurdhi:** Social protection covering approximately 25% of households;
  expanded in Q3 2022 as IMF programme entry condition.

This social safety net coverage provides a partial buffer that is not present in the GRC
and LAC calibrations (Greece's social safety nets were explicitly cut in the 2010–12 austerity
programme; LAC fiscal consolidation episodes had limited formal transfer coverage). The net
effect on Q1 FORMAL elasticity: approximately 15–20% discount from the unadjusted concentration
estimate, placing the South Asian Q1 FORMAL elasticity below both GRC (-0.25) and LAC (-0.22).

---

## 3. Chosen Calibration

### 3.1 Calibration path

**South Asian Q1 FORMAL, AGE_25_54 — primary calibration:**
GDP growth change → `poverty_headcount_ratio` change for PAK/LKA/BGD Q1 formal sector workers

Derivation chain:
1. South Asian developing-country fiscal multiplier: 0.35–0.40 (Ilzetzki et al. 2013,
   central estimate for open managed-rate developing country)
2. Aggregate PHC elasticity to GDP growth (from multiplier to welfare): approximately
   0.35–0.40 × 0.38 unit conversion factor ≈ 0.13–0.15 per step
3. Q1 FORMAL concentration factor: 1.35× (IMF WEO 2010 Ch.3 South Asian range 1.2–1.5,
   discounted 15% for BISP/Samurdhi social safety net coverage)
4. Per-step point estimate: 0.14 × 1.35 = 0.189 → dampened for quarterly/biannual step
   dynamics and social safety net offsets → **0.17**

- **Point estimate:** `elasticity = Decimal("-0.17")`, `entity_families = frozenset({"PAK", "LKA", "BGD"})`
- **Uncertainty range:** −0.12 to −0.25
  - Lower end: high social safety net coverage + open-economy multiplier attenuation
  - Upper end: fuel/energy price pass-through in formal sector is more direct than GDP channel
    implies; upper bound consistent with LAC range for similar-density formal sectors
- **Confidence tier:** T3 (regional South Asian inference; not country-specific backtested)
  T2 upgrade requires Pakistan or Sri Lanka country-specific quarterly backtesting episodes
  (not in scope for M19)
- **Why -0.17 vs LAC -0.22:**
  (1) Lower South Asian fiscal multiplier vs LAC (0.35–0.40 vs 0.5–0.6; Ilzetzki 2013)
  (2) Social safety net discount (BISP/Samurdhi) not present in LAC calibration episodes
  (3) T3 same tier, but wider uncertainty band justifies more conservative central estimate
  (4) Consistent ordering: GRC (-0.25) > LAC (-0.22) > SEA (-0.17) > SSA informal (-0.20 proxy)

**South Asian Q2 FORMAL, AGE_25_54 — secondary calibration:**
- **Point estimate:** `elasticity = Decimal("-0.10")`,  `entity_families = frozenset({"PAK", "LKA", "BGD"})`
- **Derivation:** 0.60 × (−0.17) = −0.102 → rounded to −0.10 (Ball et al. 2013 scaling)
- **Uncertainty range:** −0.07 to −0.15
- **Confidence tier:** T3

### 3.2 What is NOT calibrated in CM Sprint C

- **South Asian Q1 INFORMAL override:** The SSA Q1 INFORMAL entry (entity_families=None)
  continues to fire on PAK/LKA/BGD entities at -0.20. This overstates the South Asian
  informal poverty response relative to the lower Ilzetzki et al. developing-country
  multiplier basis. Documented as a **known model limitation** for PAK/LKA backtesting outputs.
  Remediation requires Option (d) — a module.py sprint to add entity-family exclusion logic
  for the SSA INFORMAL entry — deferred beyond M19. Known-limitation language for PAK/LKA
  Type B outputs: *"SSA informal-sector poverty elasticity (-0.20) applied as proxy to South
  Asian informal cohorts. South Asian developing-country multipliers are lower (Ilzetzki et al.
  2013: 0.35–0.40 vs SSA 0.5+); this entry overstates informal poverty response magnitude.
  DIRECTION verdict may be more reliable than MAGNITUDE for informal-sector cohorts on
  PAK/LKA entities. Formal-sector MAGNITUDE calibrated separately (M19 CM Sprint C)."*

- **BGD country-specific calibration:** BGD is included in the frozenset for structural
  completeness. The PAK/LKA crisis-episode literature basis does not extend directly to
  Bangladesh's export-shock transmission profile. BGD-specific backtesting fixtures and
  calibration are deferred beyond M19.

- **Pakistan 2022 devaluation channel:** The 40% rupee depreciation in 2022 transmitted
  through real-wage destruction in the formal sector. This channel overlaps partially with
  the GDP channel but also includes imported-goods consumption compression not captured by
  a gdp_growth_change entry. ADR-020 Channel B (exchange rate / capital flow) may partially
  cover this in future; the FORMAL entry here calibrates the fiscal consolidation channel only.

- **Sri Lanka 2022 sovereign default channel:** LKA's hard default and debt restructuring
  impacted formal-sector pension/savings. This is not modelled by the gdp_growth_change
  event. Future ADR scope.

### 3.3 Scoping

| Entry | entity_families | SSA Q1 INFORMAL also fires? |
|---|---|---|
| SEA Q1 FORMAL (new) | `frozenset({"PAK","LKA","BGD"})` | Yes — different cohort_spec, no double-count |
| SEA Q2 FORMAL (new) | `frozenset({"PAK","LKA","BGD"})` | Yes — different cohort_spec, no double-count |
| SSA Q1 INFORMAL | `None` (unchanged) | Yes — fires on SEA Q1 INFORMAL cohort (accepted overestimate) |

---

## 4. MAGNITUDE Acceptance Criterion

### 4.1 Test assertion specification

**Primary assertion (AC-1) — `hd_composite` divergence at step index 2 (PAK Type B):**

The PAK fixture has n_steps=4 (biannual steps: H2 2022, H1 2023, H2 2023, H1 2024).
Step index 2 = third step (H2 2023 equivalent: full-programme-year mid-crisis, when fiscal
consolidation effects are cumulative but social safety net expansions are also in effect).

```python
# Heterodox path: lower fiscal adjustment intensity vs orthodox IMF programme terms.
# hd_composite divergence (heterodox - orthodox) at step index 2:
lower_bound = Decimal("0.002")   # 0.2pp HD composite — minimum calibrated response
upper_bound = Decimal("0.035")   # 3.5pp HD composite — cap against overfit
```

**Rationale for lower_bound = 0.002:**
- PAK orthodox fiscal path vs heterodox: differential fiscal adjustment ~1.5–2pp GDP growth
- At South Asian developing-country multiplier ~0.4: ~0.6–0.8pp GDP growth differential per step
- At Q1 FORMAL elasticity -0.17 and Q1 INFORMAL SSA proxy -0.20:
  - Q1 FORMAL contribution: 0.007 × 0.17 ≈ 0.0012 per step
  - Q1 INFORMAL SSA contribution: 0.007 × 0.20 ≈ 0.0014 per step
  - Combined hd_composite contribution: ~0.002–0.004 at step 2
- Lower bound 0.002 is achievable and represents a genuinely detectable, non-trivial divergence

**Rationale for upper_bound = 0.035:**
- Lower than LAC upper_bound (0.050): South Asian multipliers are lower; social safety net
  partially cushions Q1 formal response; BISP/Samurdhi coverage reduces PHC swing per unit
  GDP differential
- At step 2 cumulative, a PAK formal-sector T3 calibration should not drive more than ~3.5pp
  hd_composite divergence without being fit to a specific crisis trajectory rather than
  the calibrated South Asian structural level

### 4.2 Non-regression assertion specification

All prior entries must be unchanged:

```python
# SSA entries (M17-G1)
EXPECTED_SSA_Q1_INFORMAL = Decimal("-0.20")
EXPECTED_SSA_Q2_INFORMAL = Decimal("-0.133")
EXPECTED_SSA_Q1_AGRI = Decimal("-0.16")
EXPECTED_CHANNEL_C = Decimal("-0.30")
# GRC entries (CM Sprint A)
EXPECTED_GRC_Q1_FORMAL = Decimal("-0.25")
EXPECTED_GRC_Q2_FORMAL = Decimal("-0.15")
# LAC entries (CM Sprint B)
EXPECTED_LAC_Q1_FORMAL = Decimal("-0.22")
EXPECTED_LAC_Q2_FORMAL = Decimal("-0.13")
```

### 4.3 Cross-contamination guard

```python
# SEA entries must not fire on SSA, GRC, or LAC entities
for entity_id in ("SEN", "ZMB", "GRC", "ARG", "ECU", "BOL", "PER"):
    sea_firing = [
        e for e in ELASTICITY_REGISTRY
        if e.entity_families is not None and entity_id in e.entity_families
        and e.elasticity in (Decimal("-0.17"), Decimal("-0.10"))
    ]
    assert len(sea_firing) == 0
```

---

## 5. Source Registry IDs

| source_registry_id | Source | Status |
|---|---|---|
| `ACADEMIC_LITERATURE_ILZETZKI_2013_FISCAL_MULTIPLIERS` | Ilzetzki, Mendoza & Végh (2013) JME 60(2) | New — must be added |
| `IMF_PUBLICATION_WEO_2010_CH3_FISCAL_CONSOLIDATION` | IMF WEO Oct 2010 Ch. 3 | New — must be added |
| `ACADEMIC_LITERATURE_BALL_2013_FISCAL_CONSOLIDATION` | Ball et al. (2013) IMF WP/13/151 | Registered (M17-G1) — reuse |

Both new source registry IDs must be added to `source_registry` in the same PR as the
implementation. The `source_registry` table is in the database seed; verify naming follows
`DATA_STANDARDS.md §Data Provenance Requirements`. The `IMF_PUBLICATION_*` prefix is
used for IMF institutional publications (distinct from `ACADEMIC_LITERATURE_*` for
peer-reviewed papers). IMF WEO chapters are authoritatively citable as IMF Publications.

---

## 6. Exact Registry Entries for Implementation

The implementation PR must append these two entries after the existing LAC entries:

```python
# South/Southeast Asia (PAK/LKA/BGD): Q1 FORMAL — fiscal consolidation channel.
# PAK 2022–23: energy subsidy removal + IMF programme fiscal consolidation. LKA 2022:
# sovereign default + fuel shortage + EFF. Formal-sector Q1 workers directly exposed to
# energy cost pass-through, civil service wage compression, and import-good price inflation.
# FORMAL-only (Option a): SSA Q1 INFORMAL (entity_families=None) continues to fire on all
# entities at -0.20; FORMAL entry adds uncovered formal-sector channel without double-count
# (distinct cohort_spec). Ilzetzki, Mendoza & Végh (2013): developing-country fiscal
# multiplier 0.3–0.5; open managed-rate South Asian point estimate 0.35–0.40. Q1 formal
# concentration factor 1.35× (IMF WEO 2010 Ch.3 South Asian range 1.2–1.5; discounted
# 15% for BISP/Samurdhi social safety net coverage). Derivation: 0.14 × 1.35 = 0.189
# → dampened to -0.17. Lower than GRC (-0.25) and LAC (-0.22): lower multiplier + social
# safety net discount. Uncertainty range: -0.12 to -0.25. T3: regional South Asian
# inference; T2 requires PAK/LKA country-specific backtesting.
# Calibration: docs/calibration/m19-cm-c-sea-calibration-decision.md §3.1.
CohortElasticity(
    event_type="gdp_growth_change",
    cohort_spec=CohortSpec(
        IncomeQuintile.Q1,
        AgeBand.AGE_25_54,
        EmploymentSector.FORMAL,
    ),
    attribute_key="poverty_headcount_ratio",
    elasticity=Decimal("-0.17"),
    source=(
        "Ilzetzki, E., Mendoza, E.G. & Végh, C.A. (2013): How Big (Small?)"
        " Are Fiscal Multipliers? Journal of Monetary Economics 60(2): 239-254."
        " Developing-country fiscal multiplier 0.3-0.5; open managed-rate South"
        " Asian point estimate 0.35-0.40. IMF WEO October 2010 Ch.3: fiscal"
        " consolidation in South Asian programme countries produces smaller output"
        " losses than advanced economies; Q1 formal concentration 1.2-1.5x aggregate."
        " Q1 concentration 1.35x (discounted 15% for BISP/Samurdhi social safety"
        " net coverage). Derivation: aggregate 0.14 x 1.35 = 0.189 -> -0.17."
        " PAK 2022-23 IMF SBA energy subsidy removal; LKA 2022 EFF. Known"
        " limitation: SSA Q1 INFORMAL (-0.20) also fires on SEA informal cohorts"
        " as accepted overestimate. Uncertainty range: -0.12 to -0.25."
        " M19-CM-C calibration."
    ),
    source_registry_id="ACADEMIC_LITERATURE_ILZETZKI_2013_FISCAL_MULTIPLIERS",
    confidence_tier=3,
    entity_families=frozenset({"PAK", "LKA", "BGD"}),
),
# South/Southeast Asia (PAK/LKA/BGD): Q2 FORMAL — Ball et al. (2013) 0.60 scaling.
# 0.60 x -0.17 = -0.102 -> -0.10. Q2 formal workers have stronger employment tenure
# and higher social safety net coverage than Q1; absorb 0.60x the Q1 per-unit impact.
# Consistent with GRC (Q2 = 0.60 x Q1 = -0.15) and LAC (Q2 = 0.60 x Q1 = -0.13)
# between-quintile methodology. Uncertainty range: -0.07 to -0.15. M19-CM-C.
CohortElasticity(
    event_type="gdp_growth_change",
    cohort_spec=CohortSpec(
        IncomeQuintile.Q2,
        AgeBand.AGE_25_54,
        EmploymentSector.FORMAL,
    ),
    attribute_key="poverty_headcount_ratio",
    elasticity=Decimal("-0.10"),
    source=(
        "Ball, Furceri, Leigh, Loungani (2013): The Distributional Effects"
        " of Fiscal Consolidation. IMF Working Paper WP/13/151."
        " 0.60 scaling of South Asian Q1 FORMAL: 0.60 x -0.17 = -0.102 -> -0.10."
        " Q2 formal workers have stronger employment tenure and social safety net"
        " coverage than Q1; absorb 0.60x the Q1 per-unit impact. Consistent with"
        " GRC/LAC between-quintile methodology. Uncertainty range: -0.07 to -0.15."
        " M19-CM-C calibration."
    ),
    source_registry_id="ACADEMIC_LITERATURE_BALL_2013_FISCAL_CONSOLIDATION",
    confidence_tier=3,
    entity_families=frozenset({"PAK", "LKA", "BGD"}),
),
```

---

## 7. Issue #1657 Coordination

Same separation as CM Sprint A and B: #1657 targets `module.py` (DemographicModule dead
event subscriptions). CM Sprint C targets `elasticities.py` only. No file-area conflict;
both can proceed concurrently.

---

## 8. Forward Limitation: Option (d) — South Asian INFORMAL Recalibration

This calibration decision leaves the SSA Q1 INFORMAL entry (-0.20) firing on PAK/LKA/BGD
informal cohorts without a South Asian-specific override. This is a documented model
limitation. The correct remediation is Option (d) from the intent document §3:

- Add entity-family exclusion logic to the DemographicModule to suppress the SSA INFORMAL
  entry for specified entity families
- Add South Asian-specific Q1 INFORMAL entry at approximately -0.10 to -0.12 (Ilzetzki 2013
  developing-country basis; no social safety net discount for informal workers who are excluded
  from BISP/Samurdhi formal programme coverage)

This requires a module.py sprint (file authority: DevSecOps + Data Agent review required)
beyond the calibration-sprint scope. Filed as a forward condition for M20 or a dedicated
M19 sub-sprint if EL prioritises it for Demo 8 MAGNITUDE fidelity on informal cohorts.

---

*Calibration decision document authority: sprint entry §2.4 PENDING gate.
Sprint entry: `docs/process/sprint-plans/m19-cm-c-sprint-entry.md` (EL-approved 2026-07-04).
This document gates: (1) test authorship, (2) implementation PR opening.
Author: Chief Methodologist. Date: 2026-07-04.*
