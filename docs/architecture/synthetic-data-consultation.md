# Chief Methodologist Consultation — Synthetic Data Framework

**Activation:** `Chief Methodologist: CONSULTATION — synthetic data framework`
**Date:** 2026-05-19
**Issue:** #361 — Synthetic data framework — Chief Methodologist consultation and ADR authoring
**Status:** Consultation complete. ADR outline at §ADR Outline.

**Documents read before answering:**
- `CLAUDE.md` — §Synthetic Data and the Data Inference Layer, §The Platform Principle, §Guiding Principles
- `docs/architecture/simulation-framework.md` — Three Interaction Modes, failure mode architecture, MDA system
- `docs/DATA_STANDARDS.md` — Confidence tier system, BandingEngine, gap-fill standards, Known Limitation IA-1

---

## Methodologist's Framing Note

Before answering the five questions, I record the frame through which I read them.

WorldSim exists to serve a finance minister who has limited time, limited staff, and generational consequences riding on the next 90 minutes. The synthetic data framework is not an engineering optimization — it is the feature that determines whether the tool can serve that person at all, given that the countries most at risk are exactly the countries least likely to have Eurostat-quality data.

That framing imposes a constraint on every answer below: synthetic data must be honest, but it must also be useful. A framework that responds to data poverty by refusing to produce estimates provides the same service as no tool at all. The goal is calibrated honesty — knowing what we know, knowing what we inferred, and knowing where the difference matters.

Where a method produces uncertainty so large that the output misleads more than it helps, the correct answer is to say so — and to say it specifically, not vaguely. "We cannot produce a meaningful estimate for this indicator in this context because no country with comparable debt-to-GDP ratios and governance scores has reported this variable in the past 15 years" is more useful than a band that spans the entire indicator range.

---

## Question 1 — Appropriate Methods

**What statistical methods are appropriate for synthetic data generation in WorldSim's domain? Under what conditions is each appropriate, and what data requirements does each method impose?**

### Method Hierarchy

Five methods are appropriate for WorldSim's domain, ordered from highest to lowest epistemic quality. Selection follows this order — the highest-quality applicable method is used.

---

**Method A: Hierarchical Bayesian Inference from Comparable Countries**

*What it does:* Estimates a missing country's indicator value by drawing on the posterior distribution of comparable countries, with a prior informed by regional and structural group membership. Comparables are selected on structural proximity (income group, regional bloc, institutional profile, openness, resource dependence), not geographic adjacency alone.

*When it is appropriate:*
- The country's structural profile has at least one plausible comparison group of ≥10 countries
- At least one comparable country has data for the target variable at the target time period
- Missingness is plausibly MAR (missing at random conditional on observed covariates) — not MNAR (see Method E for MNAR handling)

*What it produces:* A full posterior distribution. The pessimistic/realistic/optimistic scenario bands map directly to the 10th, 50th, and 90th percentiles of this posterior. This is the only method that produces statistically interpretable bands.

*Data requirements:*
- Comparison group: ≥10 countries with the target variable observed at the target period
- Structural covariates: ≥5 observed covariates for the target entity (income level, population, trade openness, a governance indicator, a fiscal variable) to compute structural proximity
- Prior specification: regional group membership (World Bank region or structural analog group) documented in the comparison group registry

*Confidence tier assignment:* **Tier 3 (SYNTHETIC_COMPARABLE)** when comparison group ≥10 and holdout validation passes (see §Quality Gate below). **Tier 4 (SYNTHETIC_MODEL)** when comparison group 5–9 or holdout validation is unavailable.

*Validation gate:* Before deployment, the model must be validated by running it on countries where real data exists (holdout set). The model is considered deployable only if posterior median prediction falls within ±25% of the actual value for ≥70% of holdout countries for the target variable. This gate must be documented per indicator, not globally.

---

**Method B: Multiple Imputation by Chained Equations (MICE)**

*What it does:* Imputes missing values for a specific entity at specific time points by regressing the missing variable on all observed variables for that entity across time, and on cross-sectional variation at those time points. Produces multiple imputed datasets whose variance captures imputation uncertainty.

*When it is appropriate:*
- The entity has substantial observed data for most time periods (≥80% of the time series is observed)
- The gap is short (≤3 consecutive periods) and bounded by observed values before and after
- Missingness is plausibly MCAR or MAR — the missing values are from a country that normally reports but had a reporting gap (e.g., conflict period, statistical capacity breakdown)

*What it produces:* Multiple imputed values with variance reflecting uncertainty. Scenario bands are derived from the distribution across imputations.

*Data requirements:*
- The entity must have ≥15 observed time periods for the target variable
- ≥5 other observed variables for the same entity at the same time period (for the chain)
- The gap period must be bounded on both sides by observed values

*Confidence tier assignment:* **Tier 3 (SYNTHETIC_COMPARABLE)** for short gaps (≤3 periods) with strong flanking observations. **Tier 4 (SYNTHETIC_MODEL)** for longer gaps or weak flanking observations.

*Note:* MICE is appropriate for the gap-filling use case, not for structural data absence. A country that has never reported an indicator cannot be gap-filled — it requires Method A or C.

---

**Method C: Bootstrap Resampling from Regional or Structural Group Distributions**

*What it does:* Generates synthetic observations by resampling from the empirical distribution of a defined peer group (regional or structural), without fitting a model. The target entity is treated as a draw from that empirical distribution.

*When it is appropriate:*
- Method A is unavailable because the comparison group is too small (<10) for Bayesian inference
- A plausible peer group exists, but the country's specific structural position within that group is unknown
- The user needs a rough range estimate for scenario construction, not a precise estimate for negotiation support

*What it produces:* Non-parametric bootstrap distribution. Bands represent percentiles of the peer group distribution, not uncertainty about the target entity specifically. This distinction must be disclosed: "Range reflects peer group distribution, not entity-specific estimation."

*Data requirements:*
- Peer group: ≥5 countries with data for the target variable
- Peer group must be documented and defensible (not arbitrary)

*Confidence tier assignment:* **Tier 4 (SYNTHETIC_MODEL)** always. Bootstrap resampling assumes the target entity is interchangeable with the peer group — an assumption that is stronger than Bayesian inference and less defensible.

---

**Method D: Structural Econometric Model Extrapolation**

*What it does:* Uses a fitted structural equation (e.g., fiscal balance as a function of GDP growth, commodity prices, and interest rate) to extrapolate a missing value from known relationships and observed covariates.

*When it is appropriate:*
- The structural relationship is validated and registered in the source registry
- The extrapolation horizon is short (≤5 years forward from the last observed value)
- The covariates used in the model are themselves observed (not synthetic)

*What it produces:* A point estimate with model-derived uncertainty from the fitted equation's residuals. Bands are the prediction interval of the model.

*Data requirements:*
- Fitted structural equation registered in the source registry as ACADEMIC_LITERATURE or SIMULATION_REFERENCE_CONSTANT type
- All covariates must be observed (Tier 1 or 2) for the target entity
- The model must have been fit on a dataset that includes countries comparable to the target entity

*Confidence tier assignment:* **Tier 4 (SYNTHETIC_MODEL)** always. Forward extrapolation from structural models degrades rapidly — IA-1 applies.

---

**Method E: Structural Absence Declaration (Refusal to Estimate)**

*What it does:* Declares that no synthetic estimate can be produced that would be meaningfully informative, and states why.

*When it is required:*
1. Missingness is MNAR — data absence is itself a governance or political signal. Examples: a country's press freedom data is absent because it expelled the measuring organization; a country's fiscal data is absent because it is in an undeclared conflict. Generating a synthetic estimate would mask the signal of the absence itself.
2. No comparison group of ≥3 countries exists with structural proximity and observed target variable data.
3. The BandingEngine would produce a band width exceeding 4× the absolute value of the point estimate (for ratio indicators) or spanning the entire feasible range (for bounded indicators).
4. The structural covariates needed to locate the entity in the comparison group are themselves absent.

*Output:* A structured absence declaration: `is_synthetic: True`, `synthetic_method: "STRUCTURAL_ABSENCE"`, `absence_reason: <specific text>`, `confidence_tier: 5`. The UI shows the absence explicitly — the indicator slot is not blank but shows an explicit "Estimate not available: [reason]" message.

*The honest answer is still an answer.* Structural absence declarations provide diagnostic value — they tell the analyst exactly what data would be needed to produce an estimate, and why the absence matters.

---

### Method Selection Decision Tree

```
Does the entity have ≥80% observed data and a short bounded gap (≤3 periods)?
  → YES: Method B (MICE). Tier 3 or 4 depending on gap length.

Is the missingness MNAR (absence is itself a signal)?
  → YES: Method E (Structural Absence Declaration). Never synthesize.

Does a valid comparison group exist (≥10 comparable countries with data)?
  → YES: Method A (Hierarchical Bayesian). Tier 3 if holdout gate passes, Tier 4 otherwise.

Does a small peer group exist (5–9 countries)?
  → YES: Method A at Tier 4, or Method C (Bootstrap) at Tier 4.
     Prefer A if structural covariates support Bayesian inference.

Does a documented structural equation exist with observed covariates?
  → YES: Method D (Structural Extrapolation). Tier 4 only.

No applicable method?
  → Method E (Structural Absence Declaration). Always.
```

---

## Question 2 — Epistemically Honest Presentation

**What is the correct way to present synthetic data alongside real data? What disclosures are mandatory, advisory, and never suppressible? How does the confidence tier system extend?**

### Confidence Tier Extension

The existing tier system extends to synthetic data as follows. The existing tiers (DATA_STANDARDS.md §Data Quality Tier System) are unchanged. Three new named sub-tiers within Tier 3–5 label the synthetic method:

| Tier | Sub-label | Method | BandingEngine multiplier |
|---|---|---|---|
| Tier 3 | SYNTHETIC_COMPARABLE | Method A (Bayesian), holdout-validated, comparison group ≥10 | 1.5× (existing) |
| Tier 4 | SYNTHETIC_MODEL | Methods A (small group), B (long gap), C (bootstrap), D (structural) | 2.0× (existing) |
| Tier 5 | SYNTHETIC_PROXY | Any estimate lacking quantifiable uncertainty; structural fallback | 3.0× (existing) |

Sub-labels are carried as `synthetic_method` metadata — they do not replace the integer tier and do not affect existing tier arithmetic. `confidence_tier(output) = max(inputs)` rule is unchanged.

A new required field is added to `Quantity` when `is_synthetic: True`:
- `synthetic_method: str` — one of the five method codes above
- `comparison_group_id: str | None` — reference to the documented comparison group used
- `holdout_validated: bool` — whether the model passed the ±25% / 70% validation gate

### Mandatory Disclosures — Never Suppressible

The following must appear in every output where any contributing indicator is synthetic, regardless of user preference settings, display mode, or dashboard configuration. These are data attributes, not presentation choices.

**1. Per-indicator synthetic badge (indicator level, not framework or session level)**
Every indicator slot in the UI — whether in the radar chart, the trajectory view, or the data table — carries a distinct badge when its value is synthetic. The badge must be visible without hovering, clicking, or opening a drawer. A tooltip provides the method and comparison group on hover.

*Rationale:* A session-level or framework-level "synthetic data present" banner allows the user to lose track of which specific numbers are real. Per-indicator disclosure is the only presentation that matches the epistemic reality.

**2. Comparison group identification**
The names of the countries used in the comparison group must be accessible — not buried in documentation, but one click from the indicator. A user cannot assess the quality of an inference without knowing who the comparables are. "Inferred from 14 comparable countries" is not sufficient. "Inferred from 14 countries in the Sub-Saharan Africa structural group, including Kenya, Ghana, Senegal..." is.

**3. Scenario bands labeled as synthetic bands, not model uncertainty bands**
The pessimistic/realistic/optimistic bands from synthetic data are not the same as the BandingEngine's `ci_lower`/`ci_upper`. They represent inference uncertainty (across comparables), not model uncertainty (across simulation runs). These must be labeled distinctly. Presenting them as equivalent would conflate two independent sources of uncertainty.

**4. The IA1_CANONICAL_PHRASE**
Already required by Known Limitation IA-1. Applies without exception to all outputs including synthetic.

**5. Holdout validation status**
If `holdout_validated: False`, this must appear in the disclosure: "This synthetic estimate has not been validated on countries with known data. Treat as exploratory."

### Advisory Disclosures — Appear When Contextually Relevant

These appear automatically in defined conditions but are not triggered for every synthetic indicator.

**A. High synthetic weight in composite score**
When synthetic indicators account for >40% of the weighting in a framework's composite score, the framework composite carries a flag: "X% of indicator weight is synthetic. Composite score reliability is reduced."

**B. Structural dissimilarity note**
When the target entity's structural profile score (distance from comparison group centroid) is in the top quartile of distances across all entities where the model has been applied, add: "This entity's structural profile diverges meaningfully from its comparison group. Synthetic estimates have higher uncertainty than typical."

**C. Extrapolation horizon warning (IA-1 interaction)**
When a synthetic estimate is used as a simulation seed and the scenario runs forward, the projection horizon degradation of IA-1 compounds with synthetic uncertainty. When `is_synthetic: True` and `horizon_steps > 3`, an advisory appears: "This projection extends a synthetic baseline. Uncertainty compounds: synthetic inference error and projection horizon error are independent sources of uncertainty, both active here."

**D. Comparison group structural conflict**
When two or more countries in the comparison group have governance or political indicators that differ from the target entity by more than 2 standard deviations, flag this in the comparison group disclosure. "Comparison includes countries with significantly different governance profiles. Review comparables before relying on this estimate."

### What Must Never Be Suppressed

The per-indicator synthetic badge, comparison group identification, scenario band labels, and holdout validation status listed as mandatory above may not be hidden by any user setting, dashboard configuration, "clean view" mode, or export format. When WorldSim exports data (CSV, PDF, JSON), synthetic flags and method metadata travel with the data. There is no export mode that strips this metadata.

---

## Question 3 — The Meaninglessness Threshold

**When does uncertainty in synthetic data become so large that the output is directionally meaningless? What is the threshold, how is it determined, and is it statistical, domain-specific, or user-context-dependent?**

### The Threshold Is Composite, Not Single

A single statistical threshold does not capture what "directionally meaningless" means in WorldSim's context. Three conditions — each individually sufficient — trigger a Structural Absence Declaration rather than a synthetic estimate:

---

**Condition 1 — Band Width Exceeds 4× the Point Estimate (Statistical)**

When `|ci_upper - ci_lower| > 4 × |point_estimate|`, the uncertainty interval is so wide relative to the estimate's magnitude that the estimate provides no directional signal. This applies for signed indicators; for ratio indicators bounded [0,1], the equivalent is when the CI width exceeds 0.8 (spanning 80% of the feasible range).

*Example:* A synthetic estimate of GDP growth = 2.1% with a CI of [−8.0%, +12.0%] has CI width = 20 percentage points, 4.8× the point estimate of 4.2 percentage points (absolute magnitude). This is meaningless — it encompasses severe recession and strong growth simultaneously.

*Rationale:* At 4×, the estimate cannot answer even a binary question (positive or negative growth?) with confidence. Below 4×, the estimate may not be precise, but it constrains the answer space.

---

**Condition 2 — CI Spans an MDA Threshold (Domain-Specific)**

When the CI for an indicator includes both "safe" (above MDA floor) and "critical" (below MDA floor) values, the synthetic estimate cannot support an MDA alert or MDA-safe determination. This is a domain-specific threshold that applies regardless of CI width: even a narrow CI that straddles an MDA floor is ambiguous for MDA purposes.

*Example:* MDA floor for `rule_of_law_percentile` is <25. A synthetic estimate of 28 with CI [21, 35] straddles the floor. Neither "alert" nor "safe" is defensible. Structural Absence Declaration is correct for MDA purposes — but the estimate may still be shown for narrative context with explicit straddling disclosure.

*Distinction:* This condition triggers a "cannot support MDA determination" declaration, not necessarily a full Structural Absence Declaration. The synthetic estimate can still appear in the data with appropriate disclosure, but the MDA subsystem treats this indicator as absent for alert purposes.

---

**Condition 3 — Comparison Group Quality Below Minimum (Statistical + Domain)**

When fewer than 3 comparable countries with data exist for the target variable, no method can produce a defensible basis for inference. This is a minimum requirement regardless of what CI width the model produces — a model fit on 2 comparables produces artificially narrow CIs that do not represent real uncertainty.

---

### The "Cannot Produce a Meaningful Estimate" Declaration

When any of the three conditions is met, the output is:

```
is_synthetic: True
synthetic_method: "STRUCTURAL_ABSENCE"
absence_reason: "<specific condition>: <specific explanation>"
confidence_tier: 5
```

The UI renders this as an explicit indicator slot — not blank, not zero, not interpolated. The slot shows:

> **Estimate not available.** [Specific reason, e.g., "Fewer than 3 comparable countries have reported this indicator in the past 10 years. Generating a synthetic estimate would not be epistemically defensible. To enable this indicator, provide at least one observed value for [country] or three comparable country observations."]

This format is more useful than a blank field because it tells the analyst exactly what would unblock the estimate.

### User Context Adjustment

The threshold is tighter for Mode 2 and Mode 3 than for Mode 1:

- **Mode 1 (Replay):** Historical exploration. A Tier 4 synthetic estimate with CI width up to 3× is acceptable for narrative context. The user is investigating the past, not navigating the present.
- **Mode 2 (Simulation):** Scenario construction. CI width threshold is 3× for indicators not near an MDA floor; 2× for indicators within 30% of an MDA floor.
- **Mode 3 (Active Control):** Real-time steering decisions. CI width threshold is 2× for all indicators. Any indicator that cannot meet this threshold in Mode 3 is declared absent for that session — it is excluded from the instrument cluster until real data is available.

This tightening reflects the cognitive stakes: in Mode 3, an analyst making real-time decisions cannot afford to track indicator reliability simultaneously with navigating policy choices.

---

## Question 4 — MDA Alert Interaction

**How should an MDA alert that fires on synthetic data be presented differently from one based on Tier 1 real data? Should synthetic-data-derived alerts fire in the primary instrument cluster?**

### The Epistemically Correct Position

MDA alerts exist to surface irreversible terrain. The question is: does uncertain knowledge of terrain still warrant an alert? The answer is yes, but the alert must accurately represent the nature of the uncertainty.

A pilot flying with a degraded altimeter that reports 900 feet when the truth is between 700 and 1100 feet should still receive a terrain warning. They should also know the altimeter is degraded. Suppressing the warning because the altimeter is uncertain would be the wrong failure mode.

The relevant distinction is not "synthetic or not" but "can we determine which side of the MDA floor this indicator is on?"

### Alert Presentation Rules by Tier

**Tier 1–2 (Real Data): Full MDA Alert**
Existing behavior unchanged. Appears in the primary instrument cluster as a BREACH or WARNING alert. Visual: red solid indicator.

**Tier 3 SYNTHETIC_COMPARABLE: Advisory Alert in Primary Cluster**
The alert fires in the primary instrument cluster with distinct visual treatment. Visual: amber dashed indicator. Label: "ADVISORY — Synthetic Estimate." Mandatory tooltip: "This alert is based on a synthetic estimate inferred from [comparison group countries]. Confidence: moderate. Verify with official statistics before acting."

*Rationale:* A Tier 3 estimate has passed holdout validation and has a defensible comparison group. The inference is the best available estimate for this country. Suppressing the alert would deprive the user of a potentially correct warning. Showing it with clear advisory treatment respects both the signal and the uncertainty.

*Condition:* The advisory alert only fires if Condition 2 (CI straddles MDA) is NOT triggered. If the CI straddles the MDA floor, neither a full alert nor an advisory alert fires — instead, a "Cannot determine MDA status" indicator appears.

**Tier 4 SYNTHETIC_MODEL: Exploratory Signal — Not in Primary Cluster**
Does not appear in the primary instrument cluster. Accessible via: (a) a secondary signal panel visible in Modes 1 and 2, (b) explicit drill-down from the affected indicator's data card. Visual when accessed: grey/outlined indicator. Label: "EXPLORATORY — Low-Confidence Synthetic Estimate." Tooltip: "This signal is based on a model estimate with wide uncertainty. It does not constitute an MDA alert. View to understand the data gap."

*Rationale:* Tier 4 estimates have wide uncertainty and have not been holdout-validated at meaningful accuracy. Placing them in the primary instrument cluster alongside real alerts would dilute the alert system's credibility — it trains users to dismiss alerts.

**Tier 5 SYNTHETIC_PROXY: No Alert of Any Kind**
Tier 5 estimates are too uncertain to support any directional signal. The indicator slot shows Structural Absence Declaration. No alert fires. An informational note in the data card explains the absence.

**CI Straddles MDA Floor (Any Tier): Cannot Determine MDA Status**
When Condition 2 is triggered regardless of tier, replace the alert with a distinct indicator: "MDA status: Cannot determine. CI spans safe and critical values. Obtain official data for [indicator] to resolve." Visual: blue question-mark indicator in the primary cluster. This is not an alert — it is a data gap signal. It communicates that terrain awareness is degraded, which is itself critical information.

### Summary Table

| Data tier | CI relative to MDA floor | Primary cluster | Treatment |
|---|---|---|---|
| 1–2 (real) | Either side | Yes | Full BREACH or WARNING alert |
| 1–2 (real) | Spans floor | Yes | WARNING with note "Floor proximity ambiguous" |
| 3 SYNTHETIC_COMPARABLE | Above floor | Yes | Advisory alert (amber, dashed) |
| 3 SYNTHETIC_COMPARABLE | Spans floor | Yes | "Cannot determine MDA status" (blue) |
| 3 SYNTHETIC_COMPARABLE | Below floor | Yes | Advisory BREACH alert (amber, dashed) |
| 4 SYNTHETIC_MODEL | Any | No | Exploratory signal in secondary panel only |
| 5 SYNTHETIC_PROXY | Any | No | No alert; Structural Absence Declaration |

---

## Question 5 — Anomaly Detection

**Can synthetic baseline data flag when a country's published official data diverges implausibly? What are the methodological requirements? What are the risks of false positives in active negotiation contexts?**

### The Methodological Case For and Against

Anomaly detection from synthetic baselines is technically possible and has legitimate analytical uses. It has also significant risks specific to WorldSim's use case. I address the requirements first, then the risks, and conclude with a governance recommendation.

### Methodological Requirements for Epistemic Defensibility

Before a divergence flag from a synthetic baseline can be called epistemically defensible, five conditions must be met. These are not suggestions — each is a necessary condition.

**Requirement 1 — Validated comparison group (mandatory)**
The synthetic baseline must first be tested on countries where real data exists. The baseline is defensible for anomaly detection only if its posterior median falls within ±25% of actual observed values for ≥70% of holdout countries. This is the same holdout gate as Method A's general deployment gate. A baseline that cannot predict known data has no standing to flag unknown data.

**Requirement 2 — Explicit structural divergence screening (mandatory)**
The comparison group must be screened for structural features that would predict legitimate divergence. A country undergoing a commodity boom, a conflict resolution dividend, or a demographic transition may legitimately diverge from the regional baseline without data manipulation. If structural explanations can account for the divergence, no flag fires.

**Requirement 3 — Multi-indicator consistency (mandatory)**
A divergence flag fires only when the divergence is consistent across ≥2 independent indicators that the synthetic baseline can predict. A single-indicator divergence may be explained by indicator-specific methodological differences between the country's statistical office and the comparison group methodology. Cross-indicator consistency is the minimum threshold for calling a divergence "implausible."

**Requirement 4 — Temporal persistence (mandatory)**
The divergence must persist for ≥2 consecutive time periods. Single-year divergences are explained by revisions, methodological updates, or statistical noise. A flag based on one data point is a false positive waiting to happen.

**Requirement 5 — Documented comparison group and methodology (mandatory)**
The divergence flag must carry: (a) the comparison group used, (b) the expected range from the baseline, (c) the observed value, (d) the z-score in comparison group units, (e) the structural screening result. A user must be able to reproduce the flag from this information alone.

### Minimum Comparison Group Size

The minimum for anomaly detection is stricter than for general synthetic estimation: ≥15 countries with the target variable observed in the comparison group. With fewer, the baseline distribution is too uncertain to reliably characterize "plausible." The false positive rate is unacceptable below this threshold.

### The Risks in Active Negotiation Contexts

I must be direct here. The risks of anomaly detection are qualitatively different from the risks of other synthetic data features, and they warrant separate treatment.

**Risk 1 — False positive undermines the user's own confidence**
A finance ministry analyst using WorldSim in session preparation may see a divergence flag on their own country's published statistics. If the flag is a false positive, the analyst may enter the negotiation with reduced confidence in their own data. This is a harm to the tool's primary beneficiary caused by the tool itself.

**Risk 2 — The flag is a dual-use capability**
WorldSim's mission is to serve vulnerable actors. Anomaly detection, if available to counterparts in a negotiation (an IMF programme team also using WorldSim), provides the counterpart with a synthetic-baseline argument for questioning the programme country's data. This is an asymmetric capability when counterparts have more analytical resources and can contextualize the flag; the ministry team may not have time to rebut it in the room.

**Risk 3 — The flag implies data manipulation where none may exist**
"Your GDP growth diverges from our synthetic baseline for comparable countries" is a factual statistical statement. In a negotiation room, it reads as an accusation of data manipulation. Even carefully framed language cannot fully mitigate this reading under adversarial conditions.

**Risk 4 — Governance deficit indicator**
Countries with weak data quality (the countries WorldSim most needs to serve) are also countries where official data is most likely to diverge from regional comparables for legitimate reasons: informal economy size, different methodological conventions, capacity limitations. The false positive rate is highest precisely among the tool's primary users.

### Governance Recommendation

Anomaly detection from synthetic baselines should be implemented under the following constraints:

1. **Opt-in, never default.** The feature is disabled unless the user explicitly enables it for a session.

2. **Mode 1 only for production use.** Available in Mode 1 (historical analysis) and Mode 2 (internal scenario construction). Not available in Mode 3 (active control during real-time decisions). The cognitive demands of Mode 3 make simultaneous assessment of data quality flags impractical and potentially harmful.

3. **User-facing label: "Statistical divergence signal" not "anomaly."** The label "anomaly" implies abnormality that may not exist. "Statistical divergence from regional comparable baseline" is accurate without implication.

4. **Full methodology exposure before flag display.** The comparison group, baseline method, holdout validation result, structural screening result, and z-score must be shown to the user before the divergence signal is displayed — not after. The user must have the context to assess the signal before they see it.

5. **Suppress on user request.** A session-level control allows the user to suppress all anomaly detection signals for the duration of the session. This is appropriate for users who are in or preparing for active negotiations.

6. **TSC sign-off required before production deployment.** This feature has governance implications under CLAUDE.md's "Defense, Not Offense" principle. It requires Technical Steering Committee review of the dual-use risk before production deployment. It may not be shipped as part of routine feature development.

7. **No anomaly detection on governance indicators.** Flagging divergence in governance indicators (press freedom, rule of law, democratic quality) from a synthetic baseline carries the highest risk of misuse and dignity harm. These indicators are excluded from anomaly detection functionality.

---

## ADR Outline

*This outline is the input for the full ADR to be authored subsequently (Issue #361 continuation).*

---

### Proposed ADR: ADR-007 — Synthetic Data Framework

**Status:** Proposed
**Decider:** Engineering Lead + Chief Methodologist consultation
**Date proposed:** 2026-05-19
**Issue:** #361

---

**Problem Statement**

WorldSim's primary beneficiaries — global south finance ministries and agencies operating in data-poor environments — cannot be served by a tool that requires Tier 1 data to function. Data poverty is not a methodological edge case; it is a structural feature of the environments where the tool's democratization value is highest. Without a synthetic data framework, the tool serves only the well-resourced actors it was designed to counter.

**Decision**

Adopt the five-method synthetic data framework specified in this consultation, with the confidence tier extensions, mandatory disclosure architecture, MDA alert interaction rules, and anomaly detection governance constraints documented here.

---

**Section 1 — Synthetic Data Generation Methods**

| Method | Code | Conditions | Min comparables | Output | Default tier |
|---|---|---|---|---|---|
| Hierarchical Bayesian inference | `SYNTHETIC_COMPARABLE` | ≥10 comparables, MAR missingness, holdout-validated | 10 | Full posterior | Tier 3 (validated) / Tier 4 (unvalidated) |
| MICE imputation | `SYNTHETIC_COMPARABLE` | ≥80% observed, gap ≤3 periods, bounded | 0 (within-entity) | Imputation distribution | Tier 3 (short gap) / Tier 4 (longer gap) |
| Bootstrap resampling | `SYNTHETIC_MODEL` | 5–9 comparables, structural proximity unverified | 5 | Non-parametric peer distribution | Tier 4 |
| Structural extrapolation | `SYNTHETIC_MODEL` | Validated equation, observed covariates, ≤5yr horizon | 0 (model-based) | Prediction interval | Tier 4 |
| Structural absence declaration | `STRUCTURAL_ABSENCE` | MNAR, <3 comparables, band >4× estimate, CI spans full range | — | Absence declaration | Tier 5 |

Holdout validation gate: posterior median within ±25% of actual for ≥70% of holdout countries for the target variable. Required before Tier 3 assignment.

Selection order: Apply the decision tree from §Question 1. Highest-quality applicable method is required.

---

**Section 2 — Mixed-Mode Disclosure Requirements**

Mandatory (never suppressible):
1. Per-indicator synthetic badge visible without hover in all display modes
2. Comparison group identification accessible within one click of any synthetic indicator
3. Scenario bands labeled as inference uncertainty bands (distinct from BandingEngine model uncertainty bands)
4. IA1_CANONICAL_PHRASE (existing obligation, unchanged)
5. Holdout validation status: `holdout_validated: True/False` exposed in indicator detail

Advisory (context-triggered):
- Synthetic weight >40% in framework composite
- Structural dissimilarity flag (top quartile distance from comparison group centroid)
- Synthetic baseline + projection horizon compounding (synthetic seed + horizon_steps > 3)
- Comparison group structural conflict (>2 SD governance divergence)

Export behavior: Synthetic flags, method metadata, and comparison group IDs travel with all data exports (CSV, JSON, PDF). No export mode strips this metadata.

---

**Section 3 — Scenario Banding Specification**

Synthetic scenario bands represent inference uncertainty across the comparison group — they are distinct from BandingEngine model uncertainty bands.

| Band | Meaning | Method A source | Methods B–D source |
|---|---|---|---|
| Optimistic | 90th percentile of posterior / peer distribution | Posterior P90 | Bootstrap P90 or prediction interval upper |
| Realistic | 50th percentile (posterior median) | Posterior P50 | Posterior median or model point estimate |
| Pessimistic | 10th percentile of posterior / peer distribution | Posterior P10 | Bootstrap P10 or prediction interval lower |

When both synthetic inference bands and BandingEngine model uncertainty bands apply to the same indicator in a scenario, they must be displayed as independent, additive uncertainty sources — not collapsed into a single wider band. The label for the combined output: "Total uncertainty: synthetic inference [±X%] + projection model [±Y%]."

---

**Section 4 — Confidence Tier Extension for Synthetic Data**

The integer tier system (1–5) is unchanged. Synthetic data occupies Tiers 3–5 via named sub-labels carried in `Quantity.synthetic_method`. Sub-labels do not affect tier arithmetic (`max()` rule is unchanged). New required fields when `is_synthetic: True`: `synthetic_method`, `comparison_group_id`, `holdout_validated`.

Tier floor for synthetic data: no synthetic estimate may carry Tier 1 or Tier 2. The minimum tier for any synthetic estimate is Tier 3, achievable only via Method A with holdout validation passing.

---

**Section 5 — MDA Alert Behavior Under Synthetic Data**

Full MDA alerts (primary cluster, red solid): Tier 1–2 real data only.

Advisory MDA alerts (primary cluster, amber dashed): Tier 3 SYNTHETIC_COMPARABLE, when CI does not straddle the MDA floor.

"Cannot determine MDA status" signal (primary cluster, blue question mark): Any tier, when CI straddles the MDA floor. Not an alert — a data gap signal.

Exploratory signals (secondary panel only, not primary cluster): Tier 4 SYNTHETIC_MODEL.

No alert or signal (Structural Absence Declaration only): Tier 5 SYNTHETIC_PROXY.

Mode tightening: In Mode 3 (Active Control), Tier 4 exploratory signals are suppressed from the session entirely. Only Tier 1–3 alerts and "Cannot determine" signals are visible.

---

**Section 6 — Anomaly Detection Scope and Limitations**

**In scope:**
- Statistical divergence of published official data from synthetic baseline, available as opt-in feature in Modes 1 and 2
- Applies to financial and human development indicators meeting all five methodological requirements
- Requires ≥15 countries in comparison group

**Out of scope:**
- Governance indicators (excluded permanently): `press_freedom_index`, `rule_of_law_percentile`, `democratic_quality_score`, `democratic_quality_score`, `technocratic_independence`
- Mode 3 (Active Control): anomaly detection not available
- Default-on use: anomaly detection is always opt-in

**Mandatory governance gate:** TSC sign-off required before production deployment. Feature may not ship as part of routine milestone delivery.

**User controls:**
- Session-level suppress control (removes all anomaly detection signals for the session)
- Default: suppressed. User must explicitly enable.

**Display constraints:**
- Full methodology exposure (comparison group, z-score, structural screening result) must be shown before divergence signal is displayed, not after
- Label: "Statistical divergence from regional comparable baseline" — never "anomaly" or "inconsistency"

---

**Alternatives Considered**

*Alternative A: No synthetic data, require real data for all indicators*
Rejected. This makes WorldSim unusable for the majority of global south contexts and directly contradicts the democratization mission.

*Alternative B: Synthetic data at session level with a single disclaimer*
Rejected. Session-level disclosure does not give the user enough information to distinguish which specific estimates are synthetic and to what degree. Per-indicator disclosure is the minimum epistemically honest approach.

*Alternative C: Anomaly detection enabled by default*
Rejected. The dual-use risk, false positive rate in data-poor countries, and dignity harm potential require opt-in governance. See §Question 5 for full analysis.

*Alternative D: Suppress all MDA alerts from synthetic data*
Rejected. Suppressing Tier 3 alerts (holdout-validated comparable inference) denies the user potentially correct terrain warnings. Advisory alert with clear labeling is the epistemically correct alternative.

---

**Consequences**

- `Quantity` schema gains three new fields: `is_synthetic: bool`, `synthetic_method: str | None`, `comparison_group_id: str | None`, `holdout_validated: bool | None`
- New comparison group registry (managed by Data Quality Agent, Issue #300) needed before Method A deployment
- New `SyntheticDataEngine` component responsible for method selection and execution
- BandingEngine does not change; synthetic inference bands are a separate output alongside model uncertainty bands
- Per-indicator synthetic badge requires frontend indicator-level component update
- Anomaly detection requires separate TSC approval; do not bundle into synthetic data MVP

**Implementation sequence:**
1. ADR-007 accepted (this ADR)
2. `Quantity` schema extension + migration
3. Comparison group registry structure
4. `SyntheticDataEngine` — Method E (structural absence) and Method B (MICE) first
5. Method A (Bayesian) requires comparison group registry to be populated
6. Per-indicator UI disclosure (Issue TBD)
7. Anomaly detection (TSC gate required — separate issue)
