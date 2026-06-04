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

**Standards Version:** 2026-05-23
**Valid Until:** Milestone 11.5 — Usability Validation and Experience Audit
**License Status:** ACCEPTED — 2026-05-23

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
