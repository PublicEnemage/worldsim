# Chief Methodologist Consultation — Reference Ranges for Single-Entity Composite Scoring

> **Artifact type:** Chief Methodologist consultation
> **Activation:** `Chief Methodologist: VALIDATE — financial and HD indicator reference
> ranges for Path A single-entity normalized absolute composite scoring`
> **Date:** 2026-05-23
> **Requested by:** EL Decision B (2026-05-22, PR #427, Issue #428)
> **Status:** Complete — implementation contract at §7
> **Related:** ADR-010 Decision 2 amendment (blocked on this consultation)

---

## 1. Scope and What I Was Asked

EL Decision B selected Path A: single-entity trajectory scenarios (where N < 2 entities
makes percentile-rank composite scoring unavailable) will use normalized absolute value
composite scoring. The score is entity-intrinsic — measured against pre-declared reference
ranges rather than a comparison population.

I was asked to define:

1. Reference ranges for the financial framework indicators present in the Greece fixture
2. Reference ranges for the human development framework indicators present in the Greece fixture
3. The aggregation function for per-indicator normalized scores → framework composite
4. The confidence tier floor for all single-entity normalized scores

**What I am not defining:** Reference ranges for the ecological or governance frameworks.
Ecological uses boundary proximity scoring (already entity-intrinsic — no change needed).
Governance null rendering is handled separately by Decision 5. This consultation covers
financial and human development only.

---

## 2. Financial Framework Indicators — Greece Fixture

The Greece fixture includes two financial indicators:

| Indicator | Unit | Direction | Source | Greece 2010 value |
|---|---|---|---|---|
| `gdp_growth` | ratio (e.g., -0.054) | Higher is better | IMF WEO Apr 2010 | -0.054 |
| `reserve_coverage_months` | months | Higher is better | IMF CR10/110 | 2.0 |

The MDA threshold table also includes `debt_gdp_ratio` (financial, floor: 1.20 gte) but
this indicator does not appear in the Greece fixture's `initial_attributes`. I address it
in §6 (open question).

### 2a. gdp_growth — Reference Range

**Economic grounding:** IMF sustainability literature and historical crisis episodes
establish the following bands:
- Below -0.10 (−10%): severe contraction; the bottom 5th percentile of outcomes in
  the post-WWII advanced economy dataset
- 0.0: stagnation boundary
- 0.02–0.05 (2–5%): healthy growth corridor for advanced economies
- Above 0.06: strong growth; sustainable for middle-income economies but rare in
  advanced economies over multi-year windows

**Reference range decision:** [-0.10, 0.06]

Rationale: -0.10 anchors the worst plausible sustained outcome (not the extreme
tail — Greek GDP contracted 7% in 2011, the year after the baseline). 0.06 anchors
strong but credible growth. Values below -0.10 are clamped to 0.0 on the normalized
scale; values above 0.06 are clamped to 1.0.

**Normalization:** Linear interpolation within the reference range.

```
normalized_gdp_growth = clamp((value - (-0.10)) / (0.06 - (-0.10)), 0.0, 1.0)
                      = clamp((value + 0.10) / 0.16, 0.0, 1.0)
```

At Greece 2010 (-0.054): (0.046) / 0.16 = **0.288** (in lower third of range —
consistent with a country in fiscal crisis but not at the most extreme contractionary
point)

**Confidence tier for this range:** Tier 2 for the range boundaries themselves (IMF
and World Bank literature provides empirical backing). The Tier 3 floor for the
composite output is set by the single-entity scoring method, not the range quality.

### 2b. reserve_coverage_months — Reference Range

**Economic grounding:** IMF reserve adequacy framework (2011, revised 2013) and the
ARA (Assessing Reserve Adequacy) metric establish:
- Below 2.0 months: CRITICAL — insufficient to cover import demands under stress
- 2.5 months: MDA CRITICAL floor (already defined in mda_thresholds)
- 3.0 months: minimum safe corridor for most economies
- 6.0+ months: comfortable; the modal recommendation for emerging markets under
  the IMF's ARA framework
- 12.0+ months: robust; characteristic of export-surplus economies (China, Norway)

**Reference range decision:** [0.0, 12.0] months

Rationale: 0.0 is the lower bound by definition (cannot hold negative reserves in
this metric). 12.0 represents robust adequacy for any economy — values above 12
exist but represent extreme reserve accumulation (e.g., oil exporters with sovereign
wealth funds) that is not the target population for this normalization. Values above
12.0 are clamped to 1.0.

**Normalization:**

```
normalized_reserve_coverage = clamp(value / 12.0, 0.0, 1.0)
```

At Greece 2010 (2.0 months): 2.0 / 12.0 = **0.167** (in CRITICAL zone — consistent
with the Greece fixture's MDA CRITICAL alert from step 1 onward)

**Confidence tier for this range:** Tier 2 (IMF ARA framework documentation).

---

## 3. Human Development Framework Indicators — Greece Fixture

The Greece fixture includes three HD indicators:

| Indicator | Unit | Direction | Source | Greece 2010 value |
|---|---|---|---|---|
| `unemployment_rate` | ratio | Lower is better | Eurostat LFS Q1 2010 | 0.127 |
| `health_expenditure_pct_gdp` | ratio | Non-monotonic (see §3b) | WDI 2010 | 0.095 |
| `net_enrollment_secondary` | ratio | Higher is better | WDI 2010 | 0.991 |

### 3a. unemployment_rate — Reference Range

**Economic grounding:** Labour economics literature and OECD employment outlook data:
- 0.02–0.04 (2–4%): structural minimum in modern economies (frictional unemployment)
- 0.05–0.07 (5–7%): within normal range for most advanced economies
- 0.10 (10%): elevated; triggers automatic stabilizer responses in most OECD systems
- 0.20 (20%): severe; characteristic of crisis-era youth unemployment in Southern Europe
- 0.30 (30%): extreme; Greece's youth unemployment peak (2013) approached this level

**Reference range decision:** [0.02, 0.30]; normalized as "lower is better" (inverted)

Rationale: 0.02 is the frictional minimum — the best plausible value. 0.30 represents
severe crisis conditions; values above this exist but are historically rare for total
(not youth) unemployment rates over sustained periods.

**Normalization:**

```
normalized_unemployment = clamp((0.30 - value) / (0.30 - 0.02), 0.0, 1.0)
                        = clamp((0.30 - value) / 0.28, 0.0, 1.0)
```

At Greece 2010 (0.127): (0.30 - 0.127) / 0.28 = 0.173 / 0.28 = **0.618** (above
midpoint — consistent with 12.7% being elevated but not yet at the crisis peak that
Greece would reach by 2012)

**Confidence tier for this range:** Tier 2 (OECD and Eurostat empirical literature).

### 3b. health_expenditure_pct_gdp — Methodological Flag

I am flagging this indicator as **methodologically problematic for normalized absolute
scoring** and recommending it be **excluded from the financial/HD composite normalization
until an outcome-based indicator is substituted**.

**Reason:** `health_expenditure_pct_gdp` is a spending indicator, not a health outcome
indicator. The relationship between health spending and health outcomes is non-monotonic
in a cross-country comparison, and the relationship is particularly distorted for:

1. **Crisis contexts:** Spending may decline sharply due to austerity while population
   health outcomes (life expectancy, infant mortality) lag and may not deteriorate as
   quickly. Conversely, spending may drop while still being well-allocated.
2. **High-income vs middle-income:** 9.5% of GDP (Greece 2010) is comparable to the
   EU-15 average; in a low-income economy 5% of GDP would represent strong commitment.
   Without a comparison population, the normalization has no anchor.
3. **The "is more better?" problem:** Above ~10% of GDP, marginal health spending
   exhibits diminishing returns in the OECD literature. A country spending 15% of GDP
   on health is not necessarily in better health than one spending 9%.

**Recommended substitution (M10):** The correct HD outcome indicators for health
are `life_expectancy_at_birth` or `under_5_mortality_rate` — both have internationally
validated reference ranges (WHO global standards) and unambiguous directionality. Issue
for M10 backlog: add at least one health outcome indicator to the HD framework for the
Greece fixture; retire `health_expenditure_pct_gdp` as a composite scoring input.

**For M9:** Exclude `health_expenditure_pct_gdp` from the single-entity normalized
absolute composite calculation. The Greece single-entity HD composite will be computed
over `unemployment_rate` and `net_enrollment_secondary` only (two indicators). This
is explicitly flagged in the trajectory view methodology note (Zone 3).

### 3c. net_enrollment_secondary — Reference Range

**Economic grounding:** UNESCO Institute for Statistics and World Bank data:
- 0.40 (40%): low — characteristic of low-income countries with structural barriers
  to secondary enrollment
- 0.75 (75%): middle — the global median for upper-middle-income countries
- 0.90 (90%): high — characteristic of high-income OECD countries
- 1.00 (100%): full enrollment; achieved in some high-income countries with compulsory
  secondary education

**Reference range decision:** [0.40, 1.00]

Rationale: 0.40 represents the low end of middle-income trajectories; 1.00 represents
full enrollment. Values below 0.40 are clamped to 0.0; values above 1.00 are not
possible (rate is bounded by definition).

**Normalization:**

```
normalized_net_enrollment = clamp((value - 0.40) / (1.00 - 0.40), 0.0, 1.0)
                          = clamp((value - 0.40) / 0.60, 0.0, 1.0)
```

At Greece 2010 (0.991): (0.991 - 0.40) / 0.60 = 0.591 / 0.60 = **0.985** (near the
top of the range — consistent with Greece's strong secondary enrollment rates; this
is the one positive indicator in the M9 HD picture)

**Confidence tier for this range:** Tier 2 (UNESCO and World Bank education data).

---

## 4. Aggregation Function

**Decision: Unweighted arithmetic mean of the non-excluded indicators.**

All indicators that pass the inclusion criteria (numeric, not flagged for exclusion,
reference range defined) receive equal weight. The unweighted mean is the defensible
default for the following reasons:

1. **No validated differential weights exist for these frameworks.** Weighting schemes
   that assign more importance to one indicator over another require empirical validation
   that we do not have for the M9 indicator set. Inventing weights implies precision that
   does not exist — a No False Precision violation.
2. **Equal weighting is transparently auditable.** Users can compute the aggregate from
   the per-indicator scores without knowing a hidden weighting schema.
3. **The set is small.** With 2–3 indicators per framework at M9, differential weighting
   has limited effect and adds no analytical value.

**Aggregation formula:**

```python
def normalized_absolute_composite(normalized_scores: list[Decimal]) -> Decimal | None:
    """Unweighted mean of normalized indicator scores. Returns None if empty."""
    if not normalized_scores:
        return None
    return sum(normalized_scores) / Decimal(len(normalized_scores))
```

**Example for Greece 2010 financial framework:**
- `gdp_growth`: 0.288
- `reserve_coverage_months`: 0.167
- Composite: (0.288 + 0.167) / 2 = **0.228**

**Example for Greece 2010 HD framework (two indicators — health expenditure excluded):**
- `unemployment_rate`: 0.618
- `net_enrollment_secondary`: 0.985
- Composite: (0.618 + 0.985) / 2 = **0.802**

These are plausible values: Greece's financial position was severely stressed (0.228) while
HD indicators, though deteriorating, had not yet reached crisis-level suppression by 2010.
The 0.802 HD composite reflects this — high enrollment, elevated but not catastrophic
unemployment at programme entry.

---

## 5. Confidence Tier Floor

All single-entity normalized absolute composite scores carry a **Tier 3 confidence floor**,
regardless of the confidence tier of the individual indicator observations.

**Rationale:** The Tier 3 floor applies because:

1. **The reference ranges are methodologically uncertain.** The ranges defined in §2
   and §3 are grounded in literature but are not empirically validated for the specific
   simulation engine's scoring scale. A range that is slightly wrong produces a systematic
   bias in the composite score that cannot be detected from the output alone.
2. **The aggregation function is unweighted by methodological necessity, not by evidence.**
   A weighting scheme that more accurately reflects domain knowledge might change the
   composite materially; we cannot know by how much.
3. **Single-entity scores are not comparable across scenarios.** A Greece financial
   composite of 0.228 is not comparable to an Argentina financial composite of 0.35
   computed via percentile rank — the scoring bases are different. The Tier 3 floor
   signals this comparability limitation to users.

The Tier 3 floor does not mean the output is unreliable — it means it carries
acknowledged methodological uncertainty that the user should factor into their
interpretation. This is consistent with the No False Precision principle.

---

## 6. Open Questions for M10

**OQ-1: debt_gdp_ratio.** This indicator has an MDA threshold but does not appear in
the Greece fixture's initial_attributes. If it is added to the Greece fixture in a
future PR, the reference range is: [0.0, 2.0]; lower is better; normalization:
`1 - clamp(value / 2.0, 0.0, 1.0)`. Tier 2 confidence for the range (IMF DSA framework).
This is not an M9 prerequisite.

**OQ-2: health outcome indicator.** §3b recommends replacing `health_expenditure_pct_gdp`
with a health outcome indicator (`life_expectancy_at_birth` or `under_5_mortality_rate`)
for M10. Reference ranges:
- `life_expectancy_at_birth` in years: [40.0, 85.0], higher is better,
  normalization: `(value - 40.0) / 45.0`. Source: WHO global health statistics.
- `under_5_mortality_rate` per 1000: [3.0, 150.0], lower is better,
  normalization: `1 - ((value - 3.0) / 147.0)`. Source: UNICEF/WHO joint estimates.
Not M9 scope — backlog item.

**OQ-3: food_insecurity_rate and poverty_headcount_ratio.** These appear in the MDA
threshold table (HD framework) but not in the Greece fixture. If added in future
scenarios, reference ranges are:
- `food_insecurity_rate`: [0.0, 0.50]; lower is better; normalization: `1 - (value / 0.50)`.
- `poverty_headcount_ratio`: [0.0, 0.70]; lower is better; normalization: `1 - (value / 0.70)`.
These are estimates; empirical validation against FAOSTAT and World Bank poverty data
required before M10 deployment. Not M9 scope.

**OQ-4: Step-level indicator availability.** The Greece fixture provides initial
attributes; step-level attribute updates are driven by the simulation engine. The
trajectory endpoint must query step-level attributes (not just initial_attributes)
to compute normalized absolute scores for each step. This is an implementation
question, not a methodology question — but the CM flags it to ensure the backend
implementation reads step-state snapshots, not only the scenario initial_attributes.

---

## 7. Implementation Contract

This consultation produces the following formal contract for the trajectory endpoint
implementation. All items are M9 scope unless marked M10.

### 7a. Reference Ranges Table

| Framework | Indicator | Range low | Range high | Direction | Formula |
|---|---|---|---|---|---|
| financial | `gdp_growth` | -0.10 | 0.06 | higher better | `clamp((v + 0.10) / 0.16, 0, 1)` |
| financial | `reserve_coverage_months` | 0.0 | 12.0 | higher better | `clamp(v / 12.0, 0, 1)` |
| human_development | `unemployment_rate` | 0.02 | 0.30 | lower better | `clamp((0.30 - v) / 0.28, 0, 1)` |
| human_development | `net_enrollment_secondary` | 0.40 | 1.00 | higher better | `clamp((v - 0.40) / 0.60, 0, 1)` |
| human_development | `health_expenditure_pct_gdp` | — | — | EXCLUDED | Do not include in composite |

### 7b. Composite Score Contract

```python
SINGLE_ENTITY_REFERENCE_RANGES: dict[str, dict] = {
    "gdp_growth": {
        "low": Decimal("-0.10"), "high": Decimal("0.06"), "direction": "higher_better"
    },
    "reserve_coverage_months": {
        "low": Decimal("0.0"), "high": Decimal("12.0"), "direction": "higher_better"
    },
    "unemployment_rate": {
        "low": Decimal("0.02"), "high": Decimal("0.30"), "direction": "lower_better"
    },
    "net_enrollment_secondary": {
        "low": Decimal("0.40"), "high": Decimal("1.00"), "direction": "higher_better"
    },
    # health_expenditure_pct_gdp: EXCLUDED — methodologically non-monotonic
    # See cm-reference-range-consultation-2026-05-23.md §3b
}

SINGLE_ENTITY_COMPOSITE_TIER_FLOOR = 3  # All normalized absolute scores: min Tier 3


def _normalized_absolute_strategy(
    entity_indicators: dict[str, QuantitySchema],
    framework: str,
) -> Decimal | None:
    """Entity-intrinsic composite from pre-declared reference ranges.

    Used when N < 2 entities makes percentile-rank scoring unavailable.
    Returns [0.0, 1.0] Decimal or None if no normalizable indicators.
    Excludes indicators not in SINGLE_ENTITY_REFERENCE_RANGES.
    """
    scores: list[Decimal] = []
    for attr_key, qty in entity_indicators.items():
        if (qty.measurement_framework or "financial") != framework:
            continue
        spec = SINGLE_ENTITY_REFERENCE_RANGES.get(attr_key)
        if spec is None:
            continue  # indicator excluded or not yet defined
        try:
            v = Decimal(qty.value)
        except Exception:  # noqa: BLE001
            continue
        low, high = spec["low"], spec["high"]
        if spec["direction"] == "higher_better":
            score = (v - low) / (high - low)
        else:  # lower_better
            score = (high - v) / (high - low)
        scores.append(max(Decimal("0"), min(Decimal("1"), score)))
    if not scores:
        return None
    return (sum(scores) / Decimal(len(scores))).quantize(Decimal("0.0001"))
```

### 7c. Mandatory Zone 3 Methodology Note

When `scoring_basis == "normalized_absolute"` for any curve, the trajectory view's
Zone 3 panel must display:

> "Scores for [country_name] reflect absolute indicator position against declared
> reference ranges, not ranking against a comparison population. Cross-scenario
> comparison is not valid. Two indicators excluded from HD composite in this
> scenario: health expenditure (spending proxy, not outcome indicator)."

The parenthetical after "health expenditure" is mandatory if and only if
`health_expenditure_pct_gdp` is present in the scenario's indicator set but
excluded from the composite. The "[country_name]" slot is populated from the
entity's display name.

### 7d. api_contracts.yml additions required

The trajectory endpoint stub (DA-F1, PR #424) must be updated to include:

```yaml
scoring_basis:
  type: string
  enum: ["percentile_rank", "normalized_absolute", "boundary_proximity"]
  description: >
    Scoring method for this framework curve at this step.
    "percentile_rank" — cross-entity composite; financial and human_development in
    multi-entity scenarios; governance (null when in-validation).
    "normalized_absolute" — entity-intrinsic against declared reference ranges;
    financial and human_development in single-entity scenarios. Tier 3 floor.
    "boundary_proximity" — ecological only; distance from planetary boundary;
    always entity-intrinsic. Scale [0.0, 2.0]. Amended from two-value to three-value
    enum per DA review (DA-R3, PR #429): "percentile_rank" on ecological was
    semantically incorrect — ecological is never a cross-entity percentile rank.
```

---

## 8. Epistemic Limitations — What This Consultation Does Not Resolve

I am flagging these explicitly so they appear in the institutional record:

1. **Reference ranges are not backtested.** The ranges in §2 and §3 are grounded in
   published economic literature and IMF/World Bank frameworks. They have not been
   validated by running the simulation against the Greece fixture and checking that the
   composite scores match historical assessments of Greece's financial/HD position.
   Backtesting validation is a Tier 2 confidence requirement — until it runs, these
   ranges carry Tier 3 confidence. This is why the single-entity composite floor is Tier 3.

2. **The exclusion of health_expenditure_pct_gdp reduces the HD indicator set to two.**
   An unweighted mean of two indicators is sensitive to outliers in a way that a
   larger set would not be. The Greece 2010 baseline happens to have a clean picture
   (unemployment elevated, enrollment high), but a scenario where both indicators move
   in the same direction will produce composite scores near the extremes [0, 1] with
   no moderating third indicator. This is flagged, not remedied, in M9.

3. **Step-level indicator availability is engine-dependent.** The trajectory endpoint
   reads step-state snapshots for each computed step. If the simulation engine does not
   update `gdp_growth` or `unemployment_rate` at every step (because the module that
   drives these attributes is not active), the normalized absolute composite for that
   step will be computed over fewer indicators than expected — potentially zero, which
   produces `null`. This is a correct null (no normalizable indicators computed at that
   step), not an error.

4. **These ranges are provisional pending backtesting.** The Architect Agent should
   add backtesting gates (similar to existing Greece DIRECTION_ONLY thresholds) that
   verify the normalized absolute composite at each historical step falls within
   plausible historical assessment ranges. This is M10 work.

---

*Chief Methodologist — 2026-05-23*
*Consultation reference: cm-reference-range-consultation-2026-05-23*
*This document gates ADR-010 Decision 2 amendment and the trajectory endpoint implementation.*
