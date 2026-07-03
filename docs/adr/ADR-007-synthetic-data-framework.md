# ADR-007: Synthetic Data Framework

> **Reader Orientation:** This ADR defines how WorldSim generates and discloses data when
> real data is unavailable — the synthetic data framework. Read it when: adding a new synthetic
> data method, changing how confidence tiers interact with synthetic outputs, modifying what
> the tool displays or refuses to display for low-quality data, or implementing any data
> consumer that may encounter synthetic estimates. The most consequential section for most
> changes is **Section 6 (Meaninglessness Threshold)**, which specifies when the tool must
> refuse to produce an output rather than produce a misleading one. This ADR is the authority;
> `docs/DATA_STANDARDS.md §Confidence Tier System` is the companion data quality reference.

## Status
Accepted

## Validity Context

**Standards Version:** 2026-05-23 (Amendment 1: 2026-07-02)
**Valid Until:** Milestone 13 — Methodology Publication and Public Launch; Amendment 1 reviewed at M20 or on MAGNITUDE_MATCH trigger (whichever is first)
**License Status:** ACCEPTED — 2026-05-23; Amendment 1: ACCEPTED — 2026-07-03 (EL acceptance; panel conditions incorporated 2026-07-02)

**M12 exit review:** 2026-06-10 (SCAN-026). No renewal triggers fired during Milestone 12. The synthetic data framework was not implemented in M12 — ADR-007 `Quantity` schema fields (`is_synthetic`, `synthetic_method`, `comparison_group_id`, `holdout_validated`) remain unimplemented (Issue #22, now deferred to M13). No sixth method proposed, holdout validation gate unchanged, confidence tier max() arithmetic unchanged, meaninglessness threshold unchanged, anomaly detection governance constraints unchanged. Implementation pressure now carries to M13 as a first-order obligation: M13's methodology publication scope makes the synthetic data framework a pre-publication requirement — undocumented synthetic fields block the methodology transparency commitment. License renewed to Milestone 13.

**M11 exit review:** 2026-06-04 (SCAN-025). No renewal triggers fired during Milestone 11. The synthetic data framework was not implemented in M11 — ADR-007 `Quantity` schema fields (`is_synthetic`, `synthetic_method`, `comparison_group_id`, `holdout_validated`) were not added to the engine (Issue #22 deferred to M12). PoliticalEconomyModule outputs are formula-based approximations at Tier 3–4, not synthetic data per the ADR-007 method hierarchy. No sixth method proposed, holdout validation gate unchanged, meaninglessness threshold adjustments none. License renewed to Milestone 11.5. Implementation pressure carries to M12.

**M10 exit review:** 2026-06-02 (SCAN-024). No renewal triggers fired during Milestone
10. The synthetic data framework was not implemented in M10 — no sixth method proposed,
holdout validation gate unchanged, confidence tier max() arithmetic unchanged, no
meaninglessness threshold adjustments, no anomaly detection governance changes, no
`Quantity` schema field renames. The PMM endpoint and trajectory API extensions are
application-layer outputs that do not alter the `Quantity` schema fields enumerated in
the renewal triggers. License Status confirmed ACCEPTED. License renewed through
Milestone 11 — Engine Investigation and Political Economy. M11 political economy module
will be the first consumer of synthetic data framework contracts for politically sensitive
indicators — full implementation pressure expected in M11. Next scheduled review at
Milestone 11 close.

**Panel review:** 2026-05-23 — `docs/adr/reviews/ADR-007-panel-review.md`. Panel:
Chief Methodologist (consultation complete, PR #373), Data Architect (conditional ✓),
Development Economist DIC (conditional ✓), Engineering Lead (accepted ✓ 2026-05-23).
Three INCORPORATE items applied (DA-F1 comparison group registry note, DA-F2 field
clarity, DE-F1 Mode 3 rationale, DE-F2 reverse false-positive risk note).

**Proposed:** 2026-05-23 — Initial draft. Based on Chief Methodologist consultation
complete 2026-05-19 (PR #373, `docs/architecture/synthetic-data-consultation.md`).
See Issue #508.

### Renewal Triggers

This ADR must be reviewed and an amendment appended when any of the following occur:

- A sixth synthetic data method is proposed beyond the five enumerated in Section 1
- The holdout validation gate (±25% / 70%) is changed for any method
- The confidence tier arithmetic (max() rule) is changed in `docs/DATA_STANDARDS.md`
- The meaninglessness threshold conditions (Section 6) are adjusted for any interaction mode
- The anomaly detection governance constraints change — including TSC sign-off proceeding
- The `Quantity` schema fields (`is_synthetic`, `synthetic_method`, `comparison_group_id`,
  `holdout_validated`) are renamed, retyped, or removed
- The posterior calibration method (Section 8, Amendment 1) changes — see Amendment 1 §Renewal Triggers Added

---

## Context

WorldSim's primary beneficiaries — global south finance ministries and analytical agencies
operating in data-poor environments — cannot be served by a tool that requires Tier 1 data
to function. Data poverty is not a methodological edge case; it is a structural feature of
the environments where the tool's democratization value is highest. Countries most at risk
from financial and geopolitical shocks are exactly the countries least likely to have
Eurostat-quality macroeconomic and governance data.

Without a synthetic data framework, WorldSim serves only the well-resourced actors it was
designed to counter. With one, it can function as a genuine analytical instrument for the
finance minister sitting across from an IMF negotiating team with incomplete data and
generational consequences at stake.

The framework must satisfy two competing obligations: it must be useful (producing estimates
that constrain the decision space) and it must be honest (disclosing what is inferred versus
observed and refusing to generate estimates when uncertainty is so large the output misleads).

Chief Methodologist consultation source: `docs/architecture/synthetic-data-consultation.md`.
Consultation date: 2026-05-19. Issue: #361.

---

## Decision

Adopt the five-method synthetic data framework, confidence tier extension, mandatory
disclosure architecture, scenario banding specification, MDA alert interaction rules,
and anomaly detection governance constraints documented in the seven sections below.

---

## Section 1 — Synthetic Data Generation Methods

Five methods are appropriate for WorldSim's domain, ordered from highest to lowest
epistemic quality. The highest-quality applicable method is always required — methods
are not interchangeable at the implementing agent's discretion.

### Method Table

| Method | Code | Conditions for use | Min comparables | Output | Default tier |
|---|---|---|---|---|---|
| Hierarchical Bayesian inference from comparable countries | `SYNTHETIC_COMPARABLE` | ≥10 comparables, MAR missingness, holdout-validated | 10 | Full posterior distribution | Tier 3 (validated) / Tier 4 (unvalidated or group 5–9) |
| Multiple Imputation by Chained Equations (MICE) | `SYNTHETIC_COMPARABLE` | ≥80% observed data, gap ≤3 periods, bounded on both sides | 0 (within-entity) | Imputation distribution across imputed datasets | Tier 3 (short gap) / Tier 4 (longer gap or weak flanking) |
| Bootstrap resampling from regional or structural group distributions | `SYNTHETIC_MODEL` | 5–9 comparables, structural proximity unverified | 5 | Non-parametric peer distribution percentiles | Tier 4 always |
| Structural econometric model extrapolation | `SYNTHETIC_MODEL` | Validated registered equation, observed covariates, ≤5yr horizon | 0 (model-based) | Point estimate + prediction interval | Tier 4 always |
| Structural absence declaration | `STRUCTURAL_ABSENCE` | MNAR; or <3 comparables; or CI width >4× point estimate; or CI spans full feasible range | — | Absence declaration with specific reason | Tier 5 |

### Method Selection Decision Tree

```
Does the entity have ≥80% observed data and a short bounded gap (≤3 periods)?
  → YES: Method B (MICE). Tier 3 (short gap, strong flanking) or Tier 4 otherwise.

Is the missingness MNAR (absence is itself a governance or political signal)?
  → YES: Method E (Structural Absence Declaration). Never synthesize.

Does a valid comparison group exist (≥10 comparable countries with target variable data)?
  → YES: Method A (Hierarchical Bayesian). Tier 3 if holdout gate passes; Tier 4 otherwise.

Does a small peer group exist (5–9 countries)?
  → YES: Method A at Tier 4, or Method C (Bootstrap) at Tier 4.
     Prefer A if structural covariates support Bayesian inference.

Does a documented structural equation exist in the source registry with all covariates observed?
  → YES: Method D (Structural Extrapolation). Tier 4 only. Horizon ≤5 years from last observation.

No applicable method?
  → Method E (Structural Absence Declaration). Always.
```

### Holdout Validation Gate

Before a Hierarchical Bayesian model is assigned Tier 3, it must be tested on countries
where real data exists. The model is deployable at Tier 3 only if the posterior median
prediction falls within ±25% of the actual observed value for ≥70% of holdout countries
for the target variable. This gate must be documented per indicator — a global gate is
not sufficient. Models that do not pass the holdout gate are deployed at Tier 4 if any
other conditions are met, or produce a Structural Absence Declaration.

### MNAR Recognition Obligation

Missingness Not at Random is a governance and political signal, not merely a data gap.
A country's indicator data may be absent because the country expelled the measuring
organization, because the government does not publish figures that would reveal
deterioration, or because the country is in an undeclared conflict. Generating a
synthetic estimate in these cases would mask the signal of the absence itself. The
implementing agent must document the MNAR determination — it is not a default or
catch-all; it requires a specific factual basis.

---

## Section 2 — Mixed-Mode Disclosure Requirements

### Mandatory Disclosures — Never Suppressible

The following must appear in every output where any contributing indicator is synthetic,
regardless of user preference settings, display mode, dashboard configuration, or export
format. These are data attributes, not presentation choices.

**1. Per-indicator synthetic badge**
Every indicator slot in the UI — whether in the radar chart, the trajectory view, or
the data table — carries a distinct badge when its value is synthetic. The badge must be
visible without hovering, clicking, or opening a drawer. A tooltip provides the method
and comparison group on hover.

*Rationale:* A session-level or framework-level "synthetic data present" banner allows
the user to lose track of which specific numbers are inferred. Per-indicator disclosure
is the only presentation that matches the epistemic reality.

**2. Comparison group identification**
The names of the countries used in the comparison group must be accessible within one
click of any synthetic indicator. "Inferred from 14 comparable countries" is not
sufficient. The specific countries must be listed.

**3. Scenario bands labeled as inference uncertainty bands**
The pessimistic/realistic/optimistic bands from synthetic data represent inference
uncertainty across comparables — they are distinct from the BandingEngine's `ci_lower`/
`ci_upper` model uncertainty bands. These must be labeled distinctly. Presenting them as
equivalent would conflate two independent uncertainty sources.

**4. IA1_CANONICAL_PHRASE**
Already required by Known Limitation IA-1 in `docs/DATA_STANDARDS.md`. Applies without
exception to all outputs including synthetic.

**5. Holdout validation status**
`holdout_validated: True/False` must be exposed in the indicator detail. When
`holdout_validated: False`, the following text appears: "This synthetic estimate has not
been validated on countries with known data. Treat as exploratory."

### Advisory Disclosures — Context-Triggered

These appear automatically in defined conditions but are not triggered for every
synthetic indicator.

**A. High synthetic weight in composite score**
When synthetic indicators account for >40% of weighting in a framework's composite
score, the composite carries: "X% of indicator weight is synthetic. Composite score
reliability is reduced."

**B. Structural dissimilarity note**
When the target entity's structural profile score (distance from comparison group
centroid) is in the top quartile of all entities where the model has been applied:
"This entity's structural profile diverges meaningfully from its comparison group.
Synthetic estimates have higher uncertainty than typical."

**C. Extrapolation horizon compounding**
When `is_synthetic: True` and `horizon_steps > 3`: "This projection extends a synthetic
baseline. Uncertainty compounds: synthetic inference error and projection horizon error
are independent sources of uncertainty, both active here."

**D. Comparison group structural conflict**
When two or more countries in the comparison group have governance or political indicators
differing from the target entity by more than 2 standard deviations: "Comparison includes
countries with significantly different governance profiles. Review comparables before
relying on this estimate."

### Export Behavior

Synthetic flags, method metadata (`synthetic_method`, `comparison_group_id`,
`holdout_validated`), and scenario band labels travel with all data exports (CSV, JSON,
PDF). No export mode strips this metadata. There is no "clean view" export that omits
synthetic provenance.

---

## Section 3 — Scenario Banding Specification

Synthetic scenario bands represent inference uncertainty across the comparison group.
They are not BandingEngine model uncertainty bands and must not be presented as such.

| Band | Meaning | Method A source | Methods B–D source |
|---|---|---|---|
| Optimistic | Upper inference bound | Posterior P90 | Bootstrap P90 or prediction interval upper |
| Realistic | Central estimate | Posterior P50 (median) | Bootstrap P50 or model point estimate |
| Pessimistic | Lower inference bound | Posterior P10 | Bootstrap P10 or prediction interval lower |

When both synthetic inference bands and BandingEngine model uncertainty bands apply to
the same indicator in a scenario, they must be displayed as independent, additive
uncertainty sources — not collapsed into a single wider band. Label: "Total uncertainty:
synthetic inference [±X%] + projection model [±Y%]."

---

## Section 4 — Confidence Tier Extension for Synthetic Data

The integer tier system (1–5) is unchanged. `max()` rule is unchanged. Synthetic data
occupies Tiers 3–5 via named sub-labels carried in `Quantity.synthetic_method`. Sub-labels
do not affect tier arithmetic.

| Tier | Sub-label | Method | BandingEngine multiplier |
|---|---|---|---|
| Tier 3 | `SYNTHETIC_COMPARABLE` | Method A (Bayesian), holdout-validated, comparison group ≥10; or Method B (MICE), short gap ≤3 periods, strong flanking | 1.5× (existing) |
| Tier 4 | `SYNTHETIC_MODEL` | Methods A (small group or unvalidated), B (long gap or weak flanking), C (bootstrap), D (structural extrapolation) | 2.0× (existing) |
| Tier 5 | `SYNTHETIC_PROXY` | Any estimate lacking quantifiable uncertainty; structural fallback; MNAR declarations | 3.0× (existing) |

**Tier floor:** No synthetic estimate may carry Tier 1 or Tier 2. The minimum tier for
any synthetic estimate is Tier 3, achievable only via Method A (holdout-validated) or
Method B (short bounded gap).

**New required fields on `Quantity` when `is_synthetic: True`:**
- `synthetic_method: str` — one of the method codes above, or `"STRUCTURAL_ABSENCE"`
- `comparison_group_id: str | None` — reference to the documented comparison group used
- `holdout_validated: bool | None` — whether the model passed the ±25% / 70% validation gate

---

## Section 5 — MDA Alert Behavior Under Synthetic Data

### Decision Principle

MDA alerts exist to surface irreversible terrain. The relevant distinction is not
"synthetic or not" but "can we determine which side of the MDA floor this indicator
is on?" A pilot flying with a degraded altimeter should still receive a terrain warning
and should know the altimeter is degraded. Suppressing the warning because the instrument
is uncertain is the wrong failure mode.

### Alert Rules by Tier

**Tier 1–2 (Real Data): Full MDA Alert**
Existing behavior unchanged. Primary instrument cluster, BREACH or WARNING alert. Visual:
red solid indicator.

**Tier 3 SYNTHETIC_COMPARABLE: Advisory Alert in Primary Cluster**
Alert fires in the primary instrument cluster with distinct visual treatment: amber dashed
indicator. Label: "ADVISORY — Synthetic Estimate." Mandatory tooltip: "This alert is based
on a synthetic estimate inferred from [N comparison group countries]. Confidence: moderate.
Verify with official statistics before acting."

Condition: Advisory alert fires only when the CI does NOT straddle the MDA floor. If CI
straddles, the "Cannot determine MDA status" indicator replaces it.

**Tier 4 SYNTHETIC_MODEL: Exploratory Signal — Not in Primary Cluster**
Does not appear in the primary instrument cluster. Accessible via: (a) a secondary signal
panel visible in Modes 1 and 2, (b) explicit drill-down from the affected indicator's data
card. Visual when accessed: grey/outlined indicator. Label: "EXPLORATORY — Low-Confidence
Synthetic Estimate." Tooltip: "This signal is based on a model estimate with wide
uncertainty. It does not constitute an MDA alert. View to understand the data gap."

**Tier 5 SYNTHETIC_PROXY: No Alert of Any Kind**
Indicator slot shows Structural Absence Declaration only. No alert fires.

**CI Straddles MDA Floor (Any Tier): Cannot Determine MDA Status**
When the CI for an indicator includes both "safe" (above MDA floor) and "critical" (below
MDA floor) values regardless of tier: replace the alert with a "Cannot determine MDA
status" indicator (blue question mark in primary cluster). Not an alert — a data gap
signal. Text: "MDA status: Cannot determine. CI spans safe and critical values. Obtain
official data for [indicator] to resolve."

**Mode 3 Tightening**
In Mode 3 (Active Control), Tier 4 exploratory signals are suppressed from the session
entirely. Only Tier 1–3 alerts and "Cannot determine" signals are visible. This
suppression is intentional — in Mode 3, a false HD deterioration signal from a
low-confidence synthetic estimate causes worse decisions than a missing signal. Analysts
who need Tier 4 signals should shift to Mode 2 for data quality review before Mode 3
steering.

### Summary Table

| Data tier | CI relative to MDA floor | Primary cluster | Treatment |
|---|---|---|---|
| 1–2 (real) | Either side | Yes | Full BREACH or WARNING alert |
| 1–2 (real) | Spans floor | Yes | WARNING with "Floor proximity ambiguous" note |
| 3 SYNTHETIC_COMPARABLE | Above floor | Yes | Advisory alert (amber, dashed) |
| 3 SYNTHETIC_COMPARABLE | Spans floor | Yes | "Cannot determine MDA status" (blue) |
| 3 SYNTHETIC_COMPARABLE | Below floor | Yes | Advisory BREACH alert (amber, dashed) |
| 4 SYNTHETIC_MODEL | Any | No | Exploratory signal in secondary panel only |
| 5 SYNTHETIC_PROXY | Any | No | No alert; Structural Absence Declaration |

---

## Section 6 — Meaninglessness Threshold

A single statistical threshold does not capture what "directionally meaningless" means
in WorldSim's context. Three conditions — each individually sufficient — trigger a
Structural Absence Declaration:

**Condition 1 — Band Width Exceeds 4× the Point Estimate (Statistical)**
When `|ci_upper - ci_lower| > 4 × |point_estimate|`, the CI is so wide the estimate
provides no directional signal. For bounded ratio indicators [0,1], the equivalent is
CI width exceeding 0.8.

**Condition 2 — CI Spans an MDA Threshold (Domain-Specific)**
When the CI includes both "safe" and "critical" values relative to an MDA floor, the
synthetic estimate cannot support an MDA alert or MDA-safe determination. Note: this
condition does not require a full Structural Absence Declaration for all uses — the
estimate can appear in the data with appropriate disclosure, but the MDA subsystem
treats the indicator as absent for alert purposes.

**Condition 3 — Comparison Group Quality Below Minimum**
When fewer than 3 comparable countries with data exist for the target variable, no method
can produce a defensible basis for inference regardless of what CI width the model
produces. A model fit on 2 comparables produces artificially narrow CIs that do not
represent real uncertainty.

### Mode-Specific Threshold Tightening

| Mode | CI width threshold (non-MDA indicators) | CI width threshold (near MDA floor) |
|---|---|---|
| Mode 1 (Replay) | 3× (acceptable for narrative context) | 3× |
| Mode 2 (Simulation) | 3× | 2× (within 30% of MDA floor) |
| Mode 3 (Active Control) | 2× (all indicators) | 2× (all indicators) |

In Mode 3, an indicator that cannot meet the 2× threshold is declared absent for the
session and excluded from the instrument cluster until real data is available.

---

## Section 7 — Anomaly Detection Scope and Governance

### Methodological Requirements (All Five Are Necessary Conditions)

1. **Validated comparison group:** Baseline holdout gate must pass (±25% / 70%) before
   the baseline may be used for divergence flagging. A baseline that cannot predict known
   data has no standing to flag unknown data.

2. **Structural divergence screening:** The comparison group must be screened for features
   that would predict legitimate divergence (commodity boom, conflict resolution dividend,
   demographic transition). If structural explanations account for the divergence, no flag fires.

3. **Multi-indicator consistency:** A divergence flag fires only when divergence is
   consistent across ≥2 independent indicators the synthetic baseline can predict.
   Single-indicator divergence may reflect methodological differences between the
   country's statistical office and the comparison group.

4. **Temporal persistence:** The divergence must persist for ≥2 consecutive time periods.
   Single-year divergences are explained by revisions, methodological updates, or noise.

5. **Documented comparison group and methodology:** Every flag must carry: (a) the
   comparison group used, (b) the expected range, (c) the observed value, (d) the z-score
   in comparison group units, (e) the structural screening result. A user must be able to
   reproduce the flag from this information alone.

Minimum comparison group size for anomaly detection: ≥15 countries (stricter than the ≥10
general threshold, because the false positive rate is unacceptable with smaller groups).

### Governance Constraints

1. **Opt-in, never default.** Disabled unless the user explicitly enables it for a session.
   Default: suppressed.

2. **Modes 1 and 2 only for production use.** Not available in Mode 3 (Active Control).

3. **Label:** "Statistical divergence from regional comparable baseline" — never "anomaly"
   or "inconsistency." The label "anomaly" implies abnormality that may not exist.

4. **Full methodology shown before flag.** Comparison group, baseline method, holdout
   validation result, structural screening result, and z-score must be shown to the user
   before the divergence signal is displayed — not after.

5. **Session-level suppress control.** User may suppress all anomaly detection signals
   for the duration of a session. Appropriate for users preparing for or in active
   negotiations.

6. **TSC sign-off required before production deployment.** This feature has governance
   implications under CLAUDE.md's "Defense, Not Offense" principle. It requires Technical
   Steering Committee review of the dual-use risk before production deployment. It may not
   ship as part of routine milestone delivery.

7. **Governance indicators permanently excluded.** `press_freedom_index`,
   `rule_of_law_percentile`, `democratic_quality_score`, `technocratic_independence` are
   excluded from anomaly detection functionality. Flagging divergence in governance
   indicators from a synthetic baseline carries the highest risk of misuse and dignity harm.

### Dual-Use Risk (Documented)

Anomaly detection from synthetic baselines is a dual-use capability. A counterpart in a
negotiation (an IMF programme team using WorldSim) could use divergence flags against
the programme country's own data. Countries with weak data quality — exactly WorldSim's
primary users — are most likely to produce legitimate divergences from regional baselines
for non-manipulation reasons. The TSC governance gate exists precisely because this
feature requires a level of governance independence not yet present in M9.

**Open risk — reverse false-positive:** When a country's official data closely matches
the synthetic baseline, an analyst may interpret this as data quality validation. This
reading is incorrect — synthetic baseline conformance is not a certification. Close
agreement between official data and the synthetic baseline does not mean the official
data is reliable; it means the country's data falls within the estimated range for
comparable countries. The tool must not be misread as a validation instrument.

---

## Panel

| Reviewer | Role | Status |
|---|---|---|
| Chief Methodologist (DIC) | Consulted — authored the consultation document | Complete ✓ (PR #373, 2026-05-19) |
| Data Architect Agent | Consulted — `Quantity` schema fields and comparison group registry | Conditional ✓ (2026-05-23) |
| Development Economist (DIC) | Consulted — human development indicator domain validation | Conditional ✓ (2026-05-23) |
| Engineering Lead | Accountable — final acceptance authority | Accepted ✓ (2026-05-23) |

Full panel review artifact: `docs/adr/reviews/ADR-007-panel-review.md`.

---

## Alternatives Considered

**Alternative A — No synthetic data, require real data for all indicators**
Rejected. Makes WorldSim unusable for the majority of global south contexts and directly
contradicts the democratization mission. Data poverty is a structural feature of the
environments where the tool's value is highest.

**Alternative B — Synthetic data at session level with a single disclaimer**
Rejected. Session-level disclosure does not give the user enough information to distinguish
which specific estimates are synthetic. Per-indicator disclosure is the minimum
epistemically honest approach.

**Alternative C — Anomaly detection enabled by default**
Rejected. The dual-use risk, false positive rate in data-poor countries, and dignity harm
potential require opt-in governance. The feature's false positive rate is highest precisely
among the tool's primary users.

**Alternative D — Suppress all MDA alerts from synthetic data**
Rejected. Suppressing Tier 3 alerts (holdout-validated comparable inference) denies the
user potentially correct terrain warnings. Advisory alert with clear labeling is the
epistemically correct alternative.

---

## Consequences

**Schema changes:**
- `Quantity` gains four new fields (all new, none pre-existing): `is_synthetic: bool`,
  `synthetic_method: str | None`, `comparison_group_id: str | None`,
  `holdout_validated: bool | None`
- New Alembic migration required for all four fields

**New components:**
- `SyntheticDataEngine` — responsible for method selection, execution, and absence declaration
- Comparison group registry: follows the existing `source_registry` pattern in
  `docs/schema/database.yml`; a new registry table definition is required before Method A
  deployment; managed by the Data Quality Agent (Issue #300)

**Unchanged:**
- `BandingEngine` — does not change; synthetic inference bands are a separate output
  alongside model uncertainty bands
- Confidence tier `max()` arithmetic — unchanged
- Tier integer values — unchanged; sub-labels are metadata only

**Frontend:**
- Per-indicator synthetic badge requires indicator-level component update in all display
  contexts (radar chart, trajectory view, data table)
- "Cannot determine MDA status" indicator (blue question mark) is a new visual element

**Anomaly detection:**
- Requires separate TSC approval; must not be bundled into synthetic data MVP delivery

**Implementation sequence:**
1. This ADR accepted (panel review complete, Engineering Lead sign-off)
2. `Quantity` schema extension + Alembic migration
3. Comparison group registry structure
4. `SyntheticDataEngine` — Method E (structural absence) and Method B (MICE) first
5. Method A (Hierarchical Bayesian) — requires comparison group registry populated
6. Per-indicator UI disclosure component
7. Anomaly detection (separate TSC gate required — do not bundle)

---

## Amendment 1 — Bayesian Posterior Calibration Layer and Section 6 Implementation Clause

**Amendment date:** 2026-07-02
**Authority:** ARCH-016 (ADR backlog entry assigned 2026-07-02)
**Amending:** Section 6 (implementation clause appended) and new Section 8 added
**Milestone:** M19 — Constraint Search and Empirical Calibration
**Issues:** #1543 (posterior layer), #1536 (meaninglessness threshold), #1537 (BandResult fields)

**Tier:** 2 — introduces new analytical calibration capability using existing display surfaces;
`is_pre_calibration` and `band_method` surface to existing CI label component (no new zones).

**Authored by:** Architect Agent (2026-07-02)
**Panel:** CM (C — posterior calibration method), CE (C — implementation), UX Designer (C — display contract for #1537), EL (A)

---

### Amendment to Section 6 — Meaninglessness Threshold: Implementation Clause

*The following clause is appended to Section 6 as the computational specification
for what the existing design language "Structural Absence Declaration" means in the
BandingEngine. Section 6's three conditions are unchanged; this clause specifies how
`compute_band()` detects and handles them.*

**Section 6 — Implementation Clause (M19, ARCH-016)**

`compute_band()` must check Condition 1 after clipping to natural bounds. The check
fires when the resulting CI spans the full natural range — i.e., both bounds are
clipped (`clipped_lower == True AND clipped_upper == True`) and
`ci_upper_clipped - ci_lower_clipped == natural_upper - natural_lower`.

When this fires, the band is informationally empty (CI width equals the full
feasible range of the indicator). Return a suppressed `BandResult`:

```python
BandResult(
    ci_lower=None,
    ci_upper=None,
    ci_coverage=None,
    is_pre_calibration=None,
    clipped_lower=False,
    clipped_upper=False,
    is_meaningless=True,        # new field — Section 8.7
    band_method="SUPPRESSED_MEANINGLESS",  # new field — Section 8.7
    suppressed_reason="CI spans full natural range [natural_lower, natural_upper] — Condition 1",
)
```

**When does this fire in practice?**

For the financial and human_development frameworks (natural range [0.0, 1.0]):
- Condition 1 threshold: CI width > 0.8
- At T5, step_index ≥ 7: base_hw = 0.50, multiplier = 3.0 → half_width = 1.50
- For composite_score ∈ [0.4, 0.8]: raw_lower goes negative (clipped to 0.0); raw_upper
  exceeds 1.0 (clipped to 1.0) → CI = [0.0, 1.0], width = 1.0 > 0.8 → Condition 1 fires
- Suppression is correct: a [0,1] CI says nothing the user does not already know

**What does not change:**
- Condition 2 (CI spans MDA floor) is handled by the MDA alert subsystem, not `compute_band()`
- Condition 3 (comparison group < 3 countries) is handled by `SyntheticDataEngine`, not `compute_band()`
- Existing `compute_band()` callers receiving `ci_lower=None` are already null-safe (established in M18)
- The new fields `is_meaningless` and `suppressed_reason` are additive — existing callers that
  do not read them are unaffected

---

### Section 8 — CI Band Posterior Calibration

*New section. Specifies how empirical backtesting evidence updates the BandingEngine's
structural prior multipliers, and the conditions under which `is_pre_calibration` transitions
from `True` to `False`.*

#### 8.1 — Intent and Scope

The current tier multipliers (T1: 1.0, T2: 1.2, T3: 1.5, T4: 2.0, T5: 3.0) are structural
priors set without empirical evidence at M9. They encode a reasonable prior belief that
higher data uncertainty warrants wider CI bands, but they have not been validated against
historical outcomes. A CI schedule that states "80% confidence interval" without empirical
calibration is a definitional claim, not an evidential one.

G2B backtesting (SEN: DIRECTION_ONLY, ZMB: DIRECTION_ONLY) provides the first historical
comparison evidence. Section 8 defines the method for deriving posterior-updated multipliers
from this evidence and specifies the gate conditions under which the update takes effect.

The posterior is not about changing what the CI band means — it remains an 80% coverage
target — but about updating the multiplier schedule so that the band empirically achieves
that coverage rather than merely claiming it.

#### 8.2 — Coverage Measurement Protocol

Given a backtesting run with N steps, a historical reference series `{hist_i}`,
and model output series `{model_i}` with associated `{ci_lower_i, ci_upper_i}`:

**Magnitude coverage** (primary signal — requires MAGNITUDE_MATCH fidelity):
```
C_mag = (steps where ci_lower_i ≤ hist_i ≤ ci_upper_i) / N_pairs
```
where `N_pairs` is the count of steps where both `model_i` and `hist_i` are available.

**Directional coverage** (provisional signal — available from DIRECTION_ONLY fidelity):
```
C_dir = (steps where sign(hist_i - hist_0) == sign(model_i - model_0)) / N_pairs
```
where `hist_0` and `model_0` are the initial-step values. Directional coverage measures
whether the model correctly identifies the direction of change from baseline — it is
a weaker signal than magnitude coverage but available before MAGNITUDE_MATCH.

**Per-tier coverage measurement:**
Coverage is measured separately per confidence tier encountered in the backtesting run.
If a backtesting case uses mixed-tier indicators, per-tier coverage is computed over the
subset of steps where that tier is active.

#### 8.3 — MAGNITUDE_MATCH Fidelity Gate

MAGNITUDE_MATCH (referenced by `FidelityTier.MAGNITUDE_MATCH` in `mode3_harness.py`) is
achieved when:

1. ≥50% of steps satisfy: `|model_i - hist_i| / max(|hist_i|, ε) ≤ 0.20`
   where ε = Decimal("0.01") — avoids division by zero for near-zero indicators
2. The run has ≥ 5 steps with valid `(model_i, hist_i)` pairs (minimum evidence requirement)
3. No individual step produces `|model_i - hist_i| > 5 × |hist_i|` — catastrophic outliers
   prevent MAGNITUDE_MATCH regardless of aggregate statistics

`_classify_fidelity()` in `mode3_harness.py` must be updated in G3 to implement this gate.
The gate is evaluated after directional classification passes (DIRECTION_ONLY is a necessary
precondition for MAGNITUDE_MATCH — a run that fails directional fidelity cannot achieve
magnitude fidelity).

#### 8.4 — Posterior Multiplier Computation

After coverage evidence is available from ≥1 backtesting case achieving MAGNITUDE_MATCH:

**Correction factor (per tier):**
```
κ_t = clamp(sqrt(C_target / max(C_mag_t, 0.05)), 0.5, 2.0)
```
where:
- `C_target = 0.80` (the target coverage fraction)
- `max(C_mag_t, 0.05)` — floor prevents zero-coverage from consuming the full clamp budget (CM Condition A)
- Square-root dampening prevents overcorrection when a single backtesting case is available
- Clamped to [0.5, 2.0] — multiplier cannot be halved or doubled from prior in a single calibration

**Evidence insufficiency guard (CM Condition A):**
If `C_mag_t < 0.05`, the calibration evidence is insufficient. Record the registry entry
with status `EVIDENCE_INSUFFICIENT` for that tier; do not update the multiplier. Structural
prior remains in use for that tier until sufficient evidence accumulates.

**Indicator-scoped evidence (CM Condition B):**
Calibration registry entries from backtesting cases with known indicator-level limitations
(recorded in the case's `known_limitations` output) must record `affected_indicators_excluded:
list[str]` and measure coverage over the clean-indicator subset only. SEN's entry must
exclude external-sector-sensitive indicators affected by the CommodityShockConfig direction
mismatch (#1541 known gap).

**Posterior multiplier (per tier):**
```
M_posterior_t = M_prior_t × κ_t
```

**Provisional directional posterior (before MAGNITUDE_MATCH is available):**
When only DIRECTION_ONLY evidence exists, a provisional correction is computed using
directional coverage at half-weight:
```
κ_prov_t = clamp(sqrt(C_dir_t / C_target)^0.5, 0.8, 1.2)
```
The inner `^0.5` applies a second square root, giving quarter-weight influence.
Range [0.8, 1.2] — directional-only evidence permits only small adjustments.
`is_pre_calibration` remains `True` during provisional correction; `band_method`
changes to `"PRE_CALIBRATION_PROVISIONAL_DIRECTIONAL"` to distinguish from the pure prior.

**Calibration registry:** Posterior multiplier values are stored in
`docs/backtesting/calibration-registry.md`. Each entry records: case ID, fidelity tier,
empirical coverage, correction factor, posterior multiplier, calibration date, and
`affected_indicators_excluded` (empty list when no limitations apply).
The registry is append-only. The banding engine reads the most recent accepted entry
per tier at startup via module-level `_CALIBRATION_MULTIPLIERS: dict[int, Decimal]`,
overridable via `set_calibration_multipliers()` for testing (CE Condition B).
An entry is "accepted" only after Architect Agent + CM review.

#### 8.5 — is_pre_calibration Transition Protocol

| State | Condition | `is_pre_calibration` | `band_method` |
|---|---|---|---|
| Pure prior | No backtesting evidence | `True` | `"PRE_CALIBRATION_STRUCTURAL_PRIOR"` |
| Provisional | ≥1 DIRECTION_ONLY case; no MAGNITUDE_MATCH | `True` | `"PRE_CALIBRATION_PROVISIONAL_DIRECTIONAL"` |
| Calibrated | ≥1 MAGNITUDE_MATCH case; posterior multipliers accepted | `False` | `"BAYESIAN_POSTERIOR_CALIBRATED"` |
| Suppressed | Condition 1/2/3 fires | `None` | `"SUPPRESSED_MEANINGLESS"` |

**The flip from `is_pre_calibration=True` to `False` requires all three:**
1. At least one backtesting case achieving `FidelityTier.MAGNITUDE_MATCH`
2. Posterior multipliers computed and stored in `docs/backtesting/calibration-registry.md`
3. Architect Agent + CM co-sign the calibration registry entry before it is marked "accepted"

No code change alone transitions the flag — the calibration registry entry is the gate.

#### 8.6 — BandResult Field Additions

`BandResult` (in `backend/app/simulation/banding_engine.py`) gains two new fields:

```python
@dataclass(frozen=True)
class BandResult:
    ci_lower: str | None
    ci_upper: str | None
    ci_coverage: float | None
    is_pre_calibration: bool | None
    clipped_lower: bool
    clipped_upper: bool
    band_method: str | None         # NEW — see §8.5 state table
    is_meaningless: bool            # NEW — True when §6 Condition 1 fires
    suppressed_reason: str | None   # NEW — human-readable reason when is_meaningless=True
```

Existing callers that do not read `band_method`, `is_meaningless`, or `suppressed_reason`
are unaffected (dataclass fields with defaults). Default values:
- `band_method: str | None = None` (None only in null-score path)
- `is_meaningless: bool = False`
- `suppressed_reason: str | None = None`

#### 8.7 — Frontend and API Surface (Display Contract for #1537)

`BandResult` fields must be surfaced on the `TrajectoryFrameworkPoint` API response and
consumed by the CI label component. Specifically:

- `is_pre_calibration` — already on `AdvanceResponse` (M18); must remain there
- `band_method` — must be added to the per-framework-point response payload (new field)
- `is_meaningless` — must be added; when `True`, the CI label is suppressed entirely

**Label display contract (consumed by G4 #1529 — do not hardcode label text in G3):**
G3 must expose the raw `band_method` and `is_pre_calibration` fields via API. G3 must not
encode CI label text. G4 #1529 owns the label text decision. G3 and G4 must coordinate
on `band_method` enum values before either implementation PR merges. The coordination
gate is: G3 #1537 implementation PR merged → G4 #1529 reads merged field names → G4 opens PR.

**`band_method` enum stability (UX Designer Concern 1):**
The four values are frozen API from the moment G3 #1537's implementation PR merges.
Values may not be renamed post-merge; G4 #1529 hardcodes label strings keyed to these
exact strings. New values may be appended via minor amendment. Any addition requires an
amendment entry below this one.

**Suppressed CI slot display contract (UX Designer Concern 2):**
When `is_meaningless=True`, the CI slot must not be blank. It must show a brief
placeholder: "Data range too wide for confidence interval." A blank slot forces the analyst
to investigate the absence rather than understanding it at a glance. G3 #1537's intent
document must include this as a frontend acceptance criterion.

**Per-state display contract requirement (UX Designer Concern 3):**
G3 #1537's intent document must include a display contract table specifying what the CI
label component renders for each of the four `band_method` states. Label strings are
delegated to G4 #1529, but the contract (what each state must show) is a G3 deliverable.
"PRE_CALIBRATION_PROVISIONAL_DIRECTIONAL" is the state Aicha encounters at Demo 8 — it
must have defined UI treatment before Demo 8 or the north star test (§8.10) conditional
PASS becomes a FAIL.

#### 8.8 — Silent Failure Mode

**Silent failure risk:** If `_classify_fidelity()` is not updated in G3, all backtesting
cases remain `DIRECTION_ONLY` indefinitely and `is_pre_calibration` never transitions.
The band continues to claim "80% CI" without empirical validation. There is no error —
the UI simply never updates the calibration status.

**Mitigation:** The G3 acceptance test for #1543 must include an assertion that:
- A synthetic run with ≥5 within-20% steps classifies as `MAGNITUDE_MATCH`
- A run with <50% within-20% steps classifies as `DIRECTION_ONLY`
- `is_pre_calibration=False` is returned when calibration registry has an accepted entry

#### 8.9 — Asymmetry Assessment

**Direction of benefit:** The posterior calibration benefits the finance minister's team
by making the CI label an evidential claim rather than a definitional one. When the
Zambian ministry analyst cites "calibrated 80% CI" in a restructuring session, they can
back the claim with the backtesting evidence from the calibration registry.

**Direction of risk:** Premature calibration (marking `is_pre_calibration=False` before
MAGNITUDE_MATCH is achieved) would misrepresent the CI's epistemic status. The calibration
registry gate exists precisely to prevent this. The direction of asymmetric harm is false
confidence — the clamped correction factor [0.5, 2.0] and the MAGNITUDE_MATCH gate are
the primary defenses.

#### 8.10 — North Star Test

**Scenario:** Aicha, the Zambian finance ministry analyst, is presenting the WorldSim
CI bands to a World Bank evaluator at a restructuring session (Demo 8 Act 2).

**Capability being evaluated:** After G3, the CI band carries `band_method` and
`is_pre_calibration` fields. When `is_pre_calibration=True` with `band_method=
"PRE_CALIBRATION_PROVISIONAL_DIRECTIONAL"`, the UI surfaces this status — the evaluator
can see that the band is an informed estimate grounded in directional backtesting evidence
from the SEN and ZMB calibration cases, not an arbitrary prior.

**Does this change what Aicha can argue at the table?**
Yes. Before G3, the evaluator's challenge — "Is this 80% confidence interval grounded in
anything?" — has no clean answer. The interval is a structural prior with no empirical
support on record. After G3, Aicha can say: "The CI is currently in provisional calibration
— directional fidelity is confirmed from the Senegal and Zambia backtesting runs, and the
bands have been provisionally adjusted. Full magnitude calibration requires a MAGNITUDE_MATCH
case, which we do not yet have — the band label says so explicitly." This is a more
defensible position than either silence or false confidence.

**Assessment:** PASS (conditional) — the north star question is answered if the display
contract (G4 #1529) lands before Demo 8. If G4 does not land in time, the `band_method`
and `is_pre_calibration` fields exist in the API but the label remains "95% CI" — the
Demo 8 narrative must route around this gap. PI Agent tracks this as a Demo 8 open
condition until G4 #1529 merges.

#### 8.11 — Mission Impact Statement

Empirically grounded CI bands are a direct capability improvement for the tool's primary
mission. A finance minister who cannot explain where the uncertainty estimate comes from
cannot use that estimate to push back on a creditor's assumptions. Posterior calibration
makes the CI bands citable — traceable to specific historical evidence with known fidelity
limitations. This is what "No False Precision" means operationally: not suppressing
uncertainty, but grounding it in evidence.

---

### Amendment 1 — Panel Sign-offs

| Reviewer | Role | Status |
|---|---|---|
| Architect Agent | R — author | Complete ✓ (2026-07-02) |
| Chief Methodologist (DIC) | C — posterior calibration method and coverage measurement protocol | VALIDATE ✓ (2026-07-02) — conditions incorporated |
| Computation Engine Agent | C — implementation of _classify_fidelity() gate and BandResult field additions | VALIDATE ✓ (2026-07-02) — CE Condition A gated on #1543 intent doc |
| UX Designer Agent | C — display contract for is_pre_calibration and band_method (#1537) | CONSULT — no objection ✓ (2026-07-02) — Concerns 1+2 incorporated; Concern 3 gated on #1537 intent doc |
| Engineering Lead | A — final acceptance authority | **ACCEPTED ✓ (2026-07-03)** |

*Panel review artifact: `docs/adr/reviews/ADR-007-amendment-1-panel-review.md`*

---

### Amendment 1 — Renewal Triggers Added

The following trigger is appended to the Renewal Triggers list above:

> - The posterior calibration method (Section 8) is changed — including the MAGNITUDE_MATCH
>   gate threshold (currently ≥50% within ±20%), the correction factor formula, the clamp
>   bounds [0.5, 2.0], or the calibration registry review protocol
> - A new backtesting case achieves MAGNITUDE_MATCH and the resulting posterior multipliers
>   differ from the calibration registry accepted entry by >10% for any tier — this triggers
>   a calibration review, not a full ADR amendment, but the review must be recorded as a
>   minor amendment entry below this one
