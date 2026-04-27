# ARCH-REVIEW-004: Milestone 5 Entry Blindspot Inventory

**Review type:** Targeted — five-domain blindspot inventory before ADR-006 authoring
**Scope:** ADR-001 through ADR-005, all schema registry files, all frontend architecture
documents, Issues #189–193, CLAUDE.md M5 scope
**Facilitated by:** Architecture Review Facilitator
**Date:** 2026-04-26
**Status:** Complete — feeds into ADR-006 authoring; GitHub Issues created where noted

---

## Purpose

This review is not a council challenge session. Its purpose is narrower and more
specific: before ADR-006 (Uncertainty Quantification and Distribution Outputs) is
written, inventory every architectural blindspot that the ADR must resolve. The five
domains are the five areas where the existing M1–M4 architecture will break, become
ambiguous, or produce false confidence when distribution outputs replace point estimates.

Each domain section names the blindspot precisely, identifies which existing ADR
decision or schema contract is affected, and states what ADR-006 (or an amendment to
an existing ADR) must decide. This is a pre-authoring checklist, not a design
document.

---

## Domain 1: Data Model — The Quantity Contract Under Distributions

### Current state

`Quantity` (ADR-001 Amendment 1) carries:
`value: Decimal`, `unit: str`, `variable_type: VariableType`, `confidence_tier: int`,
`measurement_framework`, `observation_date`, `source_id`.

The JSONB serialization contract (`quantity_to_jsonb` / `quantity_from_jsonb`)
treats `value` as a string-serialized `Decimal`. The `_envelope_version` field
is "1" on per-Quantity envelopes inside `scenario_state_snapshots.state_data`,
and "2" on the `state_data` container itself (per `database.yml`, added at SCAN-015).

### Blindspot 1-A: Conflating data quality with model uncertainty

`confidence_tier` is a data quality signal — how well we know the historical or
observed value on a scale of 1–5. It degrades by `max()` of contributing tiers
as values propagate through the calculation graph (the lower-of-two rule from
ADR-001 Amendment 1).

A distribution width (standard deviation, confidence interval bounds) is a model
uncertainty signal — how uncertain the simulation is about the projected value
given the model's equations and their calibration state.

These are categorically different and have different provenance:
- `confidence_tier` originates from source data quality (IMF WEO is Tier 1;
  estimated parameters are Tier 3). It is a property of the *observation*.
- Distribution width originates from model uncertainty (parameter uncertainty,
  stochastic forcing, ensemble spread). It is a property of the *projection*.

**The blindspot:** Any design that encodes distribution width *as* a confidence tier,
or that conflates the two into a single field, produces outputs that users cannot
correctly interpret. A Tier 1 observation with wide uncertainty bounds (highly
reliable data, uncertain model) and a Tier 3 observation with narrow bounds (poor
data, well-constrained model) would be rendered identically under conflation.

**What ADR-006 must decide:** Name the fields that carry distribution parameters
explicitly and separately from `confidence_tier`. The envelope must preserve both:
`confidence_tier` continues to carry data quality; new fields carry model uncertainty.
The two must not share a field.

### Blindspot 1-B: The backward-compatibility break in `quantity_from_jsonb`

Every existing scenario snapshot — including the Greece 2010–2012 backtesting
fixture at `tests/fixtures/backtesting/greece_2010_initial_state.json` — uses
the M1–M4 Quantity envelope format (no distribution fields). Every call to
`quantity_from_jsonb` that encounters a pre-M5 envelope must continue to work.

Every call that encounters a post-M5 envelope must populate the new distribution
fields. If `quantity_from_jsonb` is updated naively to expect the new fields, all
existing fixtures and snapshots break silently — they return `None` for distribution
parameters rather than raising an error, and callers receive objects that look valid.

**The blindspot:** The serialization layer has no version-aware dispatch. The
per-Quantity `_envelope_version: "1"` exists in `database.yml` but is not
currently used by `quantity_from_jsonb` to select a deserialization path.

**What ADR-006 must decide:** Whether to use `_envelope_version` on the Quantity
envelope to gate deserialization paths (version "1" → point-estimate only,
version "2" → includes distribution fields), or to make all new distribution
fields optional with `None` defaults so old envelopes deserialize without version
dispatch. The decision determines whether M4 snapshots remain readable by M5 code
without migration.

### Blindspot 1-C: The federation-compatible envelope (from memory `project_adr006_framing.md`)

The Socratic Agent TEACH session of 2026-04-26 established that the distribution
envelope must be designed with federated simulation compatibility as an explicit
constraint. Future remote domain-specialist nodes will produce Quantity objects
with their own distribution parameters. The envelope arriving from a remote node
must be:
- Self-describing: a downstream consumer must be able to read distribution
  parameters without querying the originating node.
- Provenance-carrying: distribution parameters must carry their own source
  (which model, which calibration run, which node produced the distribution).
- Version-detectable: `_envelope_version` on the Quantity envelope must be
  used by downstream deserializers to identify the schema generation.

**The blindspot:** The current `_envelope_version: "1"` on Quantity envelopes
is present in `database.yml` but is described as "not used by quantity_from_jsonb
for dispatch." It exists but does not function as a version gate. For federated
compatibility, it must function as one.

**What ADR-006 must decide:** The specific field names in the distribution
envelope, their provenance requirements (does each distribution parameter carry
its own source_id?), and the `_envelope_version` transition from "1" to "2" on
Quantity objects that carry distribution fields.

### Blindspot 1-D: MDA threshold comparison against a distribution

The MDA system (ADR-005 Decision 3) compares `current_value: Decimal` against
`floor_value: Decimal`. `MDAChecker.check()` evaluates `current_value < floor_value`.

With distribution outputs, `current_value` is a distribution, not a point. The
MDA breach semantics become ambiguous: does the alert fire when the mean is below
the floor? When the 5th percentile crosses the floor? When the floor is within the
90% confidence interval?

**The blindspot:** The MDA system is defined for point comparisons. No decision
exists about what a floor breach means for a distribution. This is not a minor
detail — it is the primary alerting mechanism for terminal threshold detection.
A system that alerts when the *mean* of the poverty distribution crosses 40%
headcount is fundamentally different from one that alerts when the *5th percentile*
crosses 40%. The former is more conservative; the latter allows the floor to be
breached in expectation while the system remains silent.

**What ADR-006 must decide:** The comparison semantics for MDA checks against
distribution-valued attributes. The most defensible choice (consistent with "No
False Precision" and human cost primacy) is to fire the alert when the lower
bound of the 80% confidence interval is below the floor — meaning the system
alerts when a floor breach is plausible even if not expected. This must be
explicitly decided, not left implicit.

---

## Domain 2: Macroeconomic Module — Regime Detection, Event Contract, Calibration

### Current state

ADR-005 documents a known gap: `DemographicModule` subscribes to
`gdp_growth_change` events that no module currently produces. The Macroeconomic
Module is M5 scope (Issue #191) and is the producer of these events. Until M5,
DemographicModule operates with a one-step lag and no real feedback from GDP
dynamics.

### Blindspot 2-A: Regime detection is not endogenous in the current architecture

ADR-002 provides `ContingentInput` — a threshold-triggered exogenous control
input that fires when `StateCondition` is met. This is the only existing
mechanism for state-conditional behavior.

Fiscal multiplier regime changes are not exogenous control inputs. They are
endogenous dynamics: the multiplier changes because the economy is in recession
or at the zero lower bound, not because a policy-maker decided to change the
multiplier. The distinction matters architecturally.

**The blindspot:** If regime detection is implemented using `ContingentInput`,
it is classified as exogenous and enters the `control_input_audit_log`. This is
wrong: the audit log records human decisions, not model state transitions. Regime
changes belong in the module's endogenous logic — the `MacroeconomicModule.process()`
method reads current state, detects the regime, and applies the appropriate
multiplier, all without creating a `ControlInput`.

The current architecture has no explicit type for endogenous regime transitions.
`SimulationModule.process()` returns `list[Event]`. A regime transition is a
state-change event the module fires. But there is no `RegimeChangeEvent` type,
no convention for how regime transitions appear in the event log, and no mechanism
for downstream modules (DemographicModule) to subscribe to regime changes
independently of the GDP growth event they produce.

**What ADR-006 (or an ADR-004 amendment) must decide:** Whether regime
transitions are standard Events (with `event_type: "regime_change"`) that modules
can subscribe to, or whether regime detection is internal to each module with no
cross-module visibility. If the former, the Event type taxonomy must be extended.

### Blindspot 2-B: The DemographicModule event subscription gap must be closed by M5

ADR-005 Decision 1 documents: "DemographicModule subscribes to
`fiscal_adjustment_event` and `gdp_growth_change` from endogenous event sources.
Neither is produced at M4 close — Macroeconomic Module is M5 scope."

The one-step lag workaround (DemographicModule reads the previous step's GDP
growth directly from entity state rather than from an event) is a documented
temporary measure. It produces a timing asymmetry: fiscal inputs fire at step N,
GDP adjusts at step N (via the MacroeconomicModule's direct output), but
demographic elasticities apply the GDP response at step N+1.

**The blindspot:** When the MacroeconomicModule is added and begins producing
`gdp_growth_change` events at step N, DemographicModule will receive *both* the
direct event (new path) and will continue to read state from step N-1 (old path)
unless the workaround is explicitly removed. If both paths are active simultaneously,
the demographic elasticities will be applied twice — once from the event and once
from the legacy state read. This is a silent double-count, not an error that raises
an exception.

**What must happen before MacroeconomicModule and DemographicModule are both active:**
Explicitly remove the one-step lag workaround from DemographicModule at the same
time the MacroeconomicModule is wired in. These must be a single commit. The
schema registry `simulation_state.yml` must be updated to reflect the removal.

### Blindspot 2-C: Calibration data exists but magnitude thresholds require explicit justification

ADR-004 Decision 3 documents Greece 2010–2012 actuals from IMF WEO Oct 2013:
- GDP growth: 2011 = -8.9%, 2012 = -6.6% (later corrected to -8.9%→-8.9% sequence;
  ADR-004 shows -8.9% then -6.6%)
- Debt/GDP: 127% (2010) → 172% (2011) → 159% (2012, post-PSI restructuring)

M5 exit requires MAGNITUDE_WITHIN_20PCT for these values (Issue #189, ADR-006
scope). To produce GDP contraction of -8.9% given the documented fiscal inputs
(~€24bn austerity 2010-2011), the Macroeconomic Module's fiscal multiplier must
be calibrated to the Greek recession regime.

The empirical literature (Blanchard & Leigh 2013) estimated fiscal multipliers of
~1.5 for Greece 2010-2012, versus the pre-crisis IMF assumption of ~0.5. A
multiplier of 1.5 applied to ~16% fiscal adjustment (primary spending cuts +
tax increases as a share of GDP) produces ~24% cumulative GDP reduction — roughly
consistent with the historical -8.9%, -6.6% over two years.

**The blindspot:** The calibration data is available and the empirical basis is
documented. But MAGNITUDE_WITHIN_20PCT is defined in the backtesting schema as
a point-to-point check (simulated value within ±20% of historical actual). With
distribution outputs, this definition is ambiguous. If the MacroeconomicModule
produces GDP growth distributions, the threshold check must specify: is it
comparing the distribution *mean* to the historical actual, or asserting the
historical actual falls *within* the distribution?

**What ADR-006 must decide:** The precise definition of MAGNITUDE_WITHIN_20PCT
for a distribution output. The recommended position: compare the distribution
mean to the historical actual within ±20%. Additionally require that the
historical actual falls within the 80% confidence interval. Both conditions
must pass. This is stricter than mean-only comparison and prevents a wide
distribution from passing the interval check while its mean is far from actuals.

---

## Domain 3: Propagation and Feedback — Uncertainty Compounding Failure Modes

### Current state

The propagation engine applies `Event.affected_attributes` deltas to
`SimulationState` using `PropagationRule` weights across relationship edges.
Confidence tier propagates as `max()` of contributing tiers. There is no
mechanism for propagating distribution width.

### Blindspot 3-A: Naive uncertainty compounding produces uninterpretable ranges

The canonical failure mode: if each propagation step adds independent Gaussian
uncertainty with standard deviation σ, after N steps the uncertainty on a derived
attribute grows as √N × σ (random walk) or faster (correlated). For a debt-to-GDP
ratio with initial std_dev of 5 percentage points and 10 annual steps, naive
propagation produces std_dev of ~16 percentage points — spanning most of the
plausible range for any sovereign.

Worse: attributes are correlated. GDP growth and debt-to-GDP are negatively
correlated under fiscal adjustment (lower growth → higher ratio numerator pressure,
higher ratio denominator pressure). Propagating them as independent distributions
produces a joint distribution that is internally inconsistent — it assigns positive
probability to combinations that cannot co-occur under the model's own equations.

**The blindspot:** There is no uncertainty propagation rule in the current
architecture. ADR-006 must make a fundamental choice about uncertainty propagation
method before any implementation begins. The three main approaches:

1. **Monte Carlo ensemble:** Run N scenario copies with perturbed initial conditions
   and parameters. Collect the ensemble of outputs at each step. Distribution is
   the empirical distribution of the ensemble. Computationally expensive (N×runtime),
   but handles correlations correctly by construction. Does not require any changes
   to the propagation engine — the engine runs as-is, the distribution is assembled
   from outputs.

2. **Analytical moment propagation:** Track mean and variance analytically through
   the propagation equations. Fast, but requires linearization around the current
   state (first-order Taylor approximation). Nonlinear feedback loops cause
   approximation error that grows over long horizons. Correlations can be tracked
   in a covariance matrix, which grows as N² with the number of attributes.

3. **Epistemic banding:** Do not propagate distributions through the feedback graph.
   Instead, attach uncertainty bands to outputs at the point of measurement (the
   `get_measurement_output` endpoint) based on confidence tier, horizon length, and
   a model-calibration quality score. The bands widen with horizon by a documented
   schedule (e.g., ±5% at 1 year, ±15% at 5 years, ±30% at 10 years). This is
   the least computationally expensive approach and aligns with the "No False
   Precision" principle — it makes the simulation's calibration state visible
   without implying false precision from analytically propagated distributions.

**What ADR-006 must decide:** Which approach, and why. The choice affects every
subsequent implementation decision: whether Quantity carries distribution parameters
through the feedback graph (Approaches 1 and 2) or only at output time (Approach 3).

### Blindspot 3-B: Ratio and bounded-attribute distributions need explicit constraints

`debt_gdp_ratio`, `poverty_headcount_ratio`, and similar attributes are bounded.
A debt-to-GDP ratio cannot be negative; a poverty headcount cannot exceed 1.0.
A normal distribution centered on 0.3 with std_dev 0.4 assigns meaningful
probability to values below 0 and above 1 — which are nonsensical.

**The blindspot:** The current architecture has no mechanism for expressing
distributional constraints on bounded attributes. ADR-001's `variable_type`
enum distinguishes stocks, flows, ratios, and dimensionless values — but this
does not constrain the distribution type used to represent uncertainty.

**What ADR-006 must decide:** Whether bounded attributes require a specific
distribution family (Beta distribution for ratios, log-normal for strictly positive
stocks), or whether truncated normal distributions are acceptable with a documented
truncation convention, or whether the simulation simply reports the unconditional
distribution with a user-facing note that tails below 0 or above 1 should be
interpreted as probability mass at the boundary.

### Blindspot 3-C: The relationship weight is a float, not a distribution

ADR-001 documents an ARCH-4 exception: `Relationship.weight` is stored as float
for NumPy matrix compatibility (SCR-001). This is a single-point propagation
strength coefficient.

Under distribution propagation, the propagation strength itself is uncertain —
especially for international trade and debt channels where bilateral flow data
is imprecise (Tier 3 or 4 sources). A propagation weight of 0.6 ± 0.2 produces
materially different uncertainty in downstream attributes than a weight of 0.6
(point estimate).

**The blindspot:** No mechanism exists for uncertain propagation weights.
The ARCH-4 float exception was documented as acceptable because the weight
is a model parameter (not a simulation output). But if distribution outputs
require propagating uncertainty through the relationship graph, the propagation
weight itself becomes a source of uncertainty that must be either sampled
(in Monte Carlo) or represented analytically.

**What ADR-006 must decide:** Whether relationship weight uncertainty is in M5
scope or explicitly deferred. Given that M5 is already the most complex milestone
in the roadmap, the recommended position is to defer weight uncertainty to M6
and document it explicitly as a known limitation in ADR-006 itself. Point-estimate
weights propagate the simulation engine's output uncertainty, not the input
uncertainty. This is a declared scope boundary, not an architectural gap.

---

## Domain 4: Backtesting — Infrastructure Readiness for Distribution Outputs

### Current state

The backtesting infrastructure (ADR-004 Decision 3) provides three tables:
`backtesting_cases`, `backtesting_thresholds`, `backtesting_runs`. The threshold
schema supports two `threshold_type` values: `DIRECTION_ONLY` and `MAGNITUDE`.
The `MAGNITUDE` type has `expected_value NUMERIC` and `tolerance_pct NUMERIC`
columns — a point-to-point comparison.

Greece 2010–2012 currently passes DIRECTION_ONLY thresholds in CI.
MAGNITUDE_WITHIN_20PCT is the M5 target (Issue #192).

### Blindspot 4-A: The MAGNITUDE threshold type is point-to-point, not distribution-aware

`backtesting_thresholds.expected_value` stores a single historical actual value.
`backtesting_thresholds.tolerance_pct` stores ±20%. The comparison is
`|simulated_value - expected_value| / |expected_value| ≤ tolerance_pct`.

With distribution outputs, `simulated_value` is a distribution. The comparison
as currently specified is undefined.

**The blindspot:** The schema must be extended, not just the application logic.
Three options:

1. **Mean comparison (simplest):** Compare distribution mean to `expected_value`.
   Schema unchanged; comparison logic changes. Passes if `|mean - expected| /
   |expected| ≤ tolerance_pct`. Weakness: a wide distribution centered on the
   right mean passes even if the actual falls in the extreme tail of the distribution.

2. **New threshold type `DISTRIBUTION_INTERVAL`:** Assert historical actual falls
   within the Nth percentile interval of the distribution. Requires a new
   `ci_coverage NUMERIC` column (e.g., 0.80 for 80% CI). The historical actual
   must fall within the `[10th percentile, 90th percentile]` of the simulated
   distribution. This is the most principled approach — it tests whether the
   simulation's uncertainty is calibrated, not just whether the mean is close.

3. **Combined:** Both conditions must pass — mean within ±20% AND historical
   actual within 80% CI. Most stringent.

**What ADR-006 must decide:** Which threshold semantics apply to M5 distribution
output backtesting. Recommendation: Option 3 (combined), which is recorded as a
new `threshold_type: DISTRIBUTION_COMBINED` requiring both mean proximity and CI
inclusion. This requires a schema amendment to `backtesting_thresholds` to add
`ci_coverage NUMERIC NULL` (null for non-distribution thresholds).

### Blindspot 4-B: The Greece fixture file is pinned to the M1–M4 Quantity envelope

`tests/fixtures/backtesting/greece_2010_initial_state.json` carries Quantity
envelopes in the M1–M4 format (no distribution fields). The backtesting CI test
reads this fixture via `quantity_from_jsonb`.

If `quantity_from_jsonb` is updated to expect or require distribution fields,
the fixture breaks. If distribution fields are optional with `None` defaults,
the fixture loads but produces a distribution-less initial state — which means
the M5 backtesting run starts from a point-estimate state and produces
distribution outputs only through the forward simulation.

**The blindspot:** Whether the Greece fixture needs to be migrated (adding
distribution parameters to initial-state attributes) before M5 backtesting
can be meaningful. If the initial state is a point estimate but the forward
simulation produces distributions, the initial distribution is implicitly
a Dirac delta. This is defensible — the initial state is the observed 2010
data, which has measurement uncertainty (captured by `confidence_tier`) but
no model uncertainty (it is not a projection). Starting from a point estimate
and growing the distribution forward is epistemically correct.

**What ADR-006 must confirm:** That initial-state attributes (step 0) may
remain as point-estimate Quantities, and that distributions only emerge from
forward simulation steps. This is consistent with Approach 3 (epistemic banding)
and Approach 1 (Monte Carlo) but requires explicit statement.

### Blindspot 4-C: Second country case selection must be decided at M5 start

Issue #192 defers the second country case selection to "M5 start." CLAUDE.md
M5 scope requires "one additional country case selected at M5 start" at
MAGNITUDE_WITHIN_20PCT threshold.

Feasibility analysis against available infrastructure:

| Case | Data availability | Module requirement | Crisis type | Assessment |
|---|---|---|---|---|
| Argentina 2001–2002 | IMF WEO vintages archived; actuals in IMF WEO 2003 | Macroeconomic (fiscal + currency) | Default + currency collapse | **Strongest candidate** |
| Thailand 1997 | BoP data available; actuals in IMF WEO 1999 | Trade + Capital Flow Modules (not M5 scope) | External-sector-driven | Too module-dependent |
| Lebanon 2019–2020 | Data quality lower (Tier 3–4); no IMF program | Institutional degradation-heavy | Bank run + fiscal | No clean program ControlInput sequence |
| Iceland 2008 | IMF WEO archived; clean program dates | Banking sector + IMF | Banking collapse | Banking sector not in M5 modules |

**Recommendation: Argentina 2001–2002.** A documented fiscal crisis with an IMF
ControlInput sequence (four separate programs 1998–2001), GDP contraction of -10.9%
in 2002, and debt default that matches Macroeconomic Module dynamics. The
EmergencyPolicyInput `DEFAULT_DECLARATION` type already exists in ADR-002. The
case tests the Macroeconomic Module against extreme austerity outcomes and validates
that the module can detect coffin-corner dynamics without active Trade or Capital
Flow modules (Argentina's trade channel was secondary to its fiscal crisis).

**What must be decided at M5 start:** Argentina confirmed as second case, or an
alternative with documented rationale. This decision gates `backtesting_cases`
database seeding.

---

## Domain 5: Frontend — Distribution Rendering Requirements

### Current state

The frontend renders point-estimate outputs throughout:
- `FrameworkPanel` renders `QuantitySchema.value: string` in indicator rows
- `RadarChart` renders `composite_score: string` as a point on each axis
- `EntityDetailDrawer` renders the `ia1_disclosure` limitation disclosure
- `useMultiFrameworkOutput` returns `MultiFrameworkOutput` typed with
  point-estimate `composite_score: string | null` and `indicators`
  containing `QuantitySchema` or cohort block shapes

### Blindspot 5-A: RadarChart has no native uncertainty visualization capability

`RadarChart` (247 lines, Recharts) renders 4 axes with a single point per axis.
Recharts' RadarChart component does not natively support uncertainty bands (shaded
areas showing the distribution range). Displaying uncertainty on the radar requires
either:
1. Rendering multiple overlapping Radar traces (one at mean, one at lower CI,
   one at upper CI) with different fill opacities — achievable in Recharts but
   requires a specific data shape change.
2. Custom SVG rendering within the Recharts chart — complex, fragile against
   Recharts version updates.
3. Replacing Recharts for the RadarChart — CLAUDE.md explicitly states "Recharts
   is not being replaced" in the modularization strategy.

**The blindspot:** Option 1 (multiple overlapping traces) requires changing the
`RadarAxisDatum[]` data shape that EntityDetailDrawer computes from
`composite_score`. A single `{ axis, value }` datum must become
`{ axis, value, lower, upper }`. This is a TypeScript type change that propagates
from `EntityDetailDrawer` through `RadarChart` — a two-component change.

A second blindspot: the radar uncertainty visualization must have an
`uncertaintyVisible` toggle (per `ScenarioViewContext` design in
`modularization-strategy.md`). This toggle does not yet exist. If the toggle is
introduced in M5 without `ScenarioViewContext`, it requires another state
variable in `App.tsx`.

**What must be designed before implementation:** The `RadarAxisDatum` type
extension and the toggle state location (App.tsx direct vs. ScenarioViewContext
trigger criteria check).

### Blindspot 5-B: FrameworkPanel's isCohortBlock heuristic is fragile against new envelope shapes

`isCohortBlock()` in `FrameworkPanel` distinguishes flat `QuantitySchema` entries
from cohort-block entries by checking for the *absence* of a `"value"` key at
the top level. If the distribution envelope adds fields *alongside* `"value"` in
a flat QuantitySchema (e.g., `value`, `mean`, `std_dev`, `ci_lower`, `ci_upper`),
the heuristic continues to work — the `"value"` key is still present.

But if the distribution format *replaces* `"value"` with a nested distribution
object (e.g., `distribution: { mean, std_dev, lower, upper }` with no top-level
`"value"` key), then `isCohortBlock()` would misclassify distribution-valued
indicators as cohort blocks — silently rendering them in the cohort block renderer
instead of the indicator row renderer.

**The blindspot:** The fragility of `isCohortBlock()` has already been documented
in `design-decisions.md` DD-009. The distribution format decision made in ADR-006
determines whether this fragility becomes a bug. If distribution fields are added
*alongside* `"value"` in the existing envelope (backward-compatible extension),
the heuristic holds. If distribution fields *replace* `"value"`, the heuristic
must be updated to a more robust discriminator (explicit type tag).

**What ADR-006 must decide:** Whether the distribution envelope extends the
existing `value` field (preserving `isCohortBlock()`) or replaces it
(requiring heuristic update). This decision directly affects two frontend
components and the TypeScript type definitions in `types.ts`.

### Blindspot 5-C: useMultiFrameworkOutput return type must evolve but the hook architecture need not

The `useMultiFrameworkOutput` hook is a fetch-and-return pattern: given
`(scenarioId, entityId, step)`, fetch `GET /scenarios/{id}/measurement-output`
and return the parsed response. The hook does not transform the data — it returns
what the API returns.

If the API response shape evolves (distribution fields added to indicators and
composite_score), the hook's TypeScript types must evolve, but the hook's
*implementation* does not change. The cancellation pattern, the loading/error
state management, and the useEffect dependency array are all independent of the
data shape returned.

**The non-blindspot:** The hook does not need redesign. Type updates only.

**The actual blindspot:** The `MultiFrameworkOutput` TypeScript type is defined in
`types.ts` (from M4 baseline: `composite_score: string | null`). When M5 adds
distribution fields, `types.ts` is the single file that must change, and it will
propagate TypeScript errors to every consumer of the type. Those errors are:
- `RadarChart` (uses `composite_score` as a number after `parseFloat`)
- `MDAAlertPanel` (does not use `composite_score` — unaffected)
- `FrameworkPanel` (uses indicator `value` field)
- `EntityDetailDrawer` (derives `RadarAxisDatum[]` from `composite_score`)

All four changes are mechanical type updates if the distribution envelope extends
rather than replaces `value` and `composite_score`. If distribution fields replace
them, the changes are structural.

**What must be decided:** Whether `composite_score` becomes a distribution object
or gains sibling fields (`composite_score_mean`, `composite_score_ci_lower`,
`composite_score_ci_upper`). The sibling-fields approach is a cleaner TypeScript
migration — it avoids breaking changes in component code that reads
`composite_score` as a string today.

### Blindspot 5-D: Playwright tests must precede distribution visualization, not follow it

`testing-standards.md` and the M4 retrospective establish a hard rule:
the Playwright E2E suite (Issue #190) is a blocking gate for M5 exit. The
three required flows test the point-estimate UI.

If distribution visualization components are added to `EntityDetailDrawer`,
`RadarChart`, and `FrameworkPanel` *before* the Playwright suite is written,
the suite must be authored against the distribution UI — which is harder to
assert against (uncertainty bands, toggle states) than the simpler point-estimate
display.

**The blindspot:** The correct implementation sequence is:
1. Write Playwright tests against the M4 point-estimate UI (testing-standards.md §3 flows).
2. Upgrade TypeScript types for distribution fields (backward-compatible, no rendering change).
3. Add distribution rendering behind the `uncertaintyVisible = false` default.
4. Write Playwright tests for uncertainty toggle on/off.

If step 3 precedes step 1, the three required Playwright flows are authored
against a richer UI than necessary, making them harder to write and more likely
to be flaky (uncertainty band positioning is harder to assert than plain text).

**What the implementation plan for Issue #190 must specify:** Playwright tests
are written and passing against the point-estimate UI *before* any M5 distribution
visualization components are merged.

---

## Consolidated Decisions Required from ADR-006

The following decisions are required before any M5 implementation begins. Each
is a pre-condition for Issue #191 (MacroeconomicModule), Issue #190 (Playwright),
or Issue #193 (single-entity composite score warning).

| Decision | Domain | Blocking |
|---|---|---|
| Distribution fields added alongside or replacing `value` in Quantity envelope | 1 | All |
| `_envelope_version` on Quantity objects advanced to "2" for distribution-capable envelopes | 1 | All |
| Explicit separation of `confidence_tier` (data quality) from distribution width fields (model uncertainty) | 1 | All |
| MDA comparison semantics for distribution-valued attributes (mean vs. lower CI vs. both) | 1 | #191 |
| Uncertainty propagation approach (Monte Carlo, analytical moment, or epistemic banding) | 3 | #191 |
| Distribution type constraints for bounded attributes (ratios, headcounts) | 3 | #191 |
| Relationship weight uncertainty: in M5 scope or deferred with documented rationale | 3 | #191 |
| MAGNITUDE_WITHIN_20PCT for distributions: mean-only, CI-inclusion, or combined | 4 | #192 |
| `backtesting_thresholds` schema amendment for distribution-aware threshold type | 4 | #192 |
| Second backtesting case: Argentina confirmed or alternative with rationale | 4 | #192 |
| Distribution envelope backward compatibility: optional new fields or version-dispatch | 1 | #190, #191 |
| `composite_score` field shape: distribution object or sibling fields | 5 | #190 |
| `uncertaintyVisible` toggle: App.tsx state or ScenarioViewContext trigger | 5 | #190 |
| Playwright test sequence: E2E against point-estimate UI before distribution UI merges | 5 | #190 |
| Regime change events: endogenous Event type or ContingentInput | 2 | #191 |
| DemographicModule lag workaround removal: same commit as MacroeconomicModule wire-up | 2 | #191 |

---

## Known Limitations of This Review

This review was conducted from ADR-001 through ADR-005, the schema registry,
the frontend architecture documents, and Issues #189–193. It did not include:

- The `WebScenarioRunner` source code (not read) — implementation-level gaps
  may exist beyond the architectural gaps documented here.
- The `DemographicModule` elasticity matrix source code — the precise mechanism
  for the one-step lag workaround is assumed from ADR-005 description, not
  verified from code.
- The Recharts version in use — the multiple-trace option for RadarChart
  uncertainty assumes a Recharts version that supports multiple `<Radar>`
  components on one `<RadarChart>`. Version compatibility should be confirmed.

These gaps do not change the ADR-006 decisions required. They are
implementation-verification tasks, not architectural decisions.

---

## Issues to File

The following GitHub Issues are created from or updated based on this review.
Each maps to a specific decision above.

| Issue | Action |
|---|---|
| #189 (ADR-006 authoring) | Update with the 16 required decisions from this review; confirm federation-compatible framing from memory file |
| #191 (Macroeconomic Module) | Add: regime detection must use endogenous Events not ContingentInput; DemographicModule lag removal must be same commit |
| #192 (Second backtesting case) | Recommend Argentina 2001–2002; add schema amendment requirement for `backtesting_thresholds` |
| #190 (Playwright tests) | Add: tests must precede distribution visualization; document implementation sequence |
| New: schema amendment for distribution-aware backtesting threshold | File enhancement with `horizon:immediate`; amends `backtesting_thresholds` with `ci_coverage NUMERIC NULL` and new `threshold_type: DISTRIBUTION_COMBINED` |
