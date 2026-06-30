# ADR-010: Trajectory View Component Architecture

## Status
Accepted

## Validity Context

**Standards Version:** 2026-05-22
**Valid Until:** Milestone 13 — Methodology Publication and Public Launch
**License Status:** ACCEPTED — 2026-05-22

**M12 exit review:** 2026-06-10 (SCAN-026). Renewal trigger fired: live A/B comparison visual specification changed. Mode 3 adds a ghost curve for the pre-branch trajectory alongside the active branch trajectory. Ghost curve specification: `strokeOpacity: 0.3`, `strokeDasharray: "4 4"`, same color as active framework curve; divergence fill region between ghost and active (blue/orange per ADR-008 Decision 12, 0.12 opacity). Amendment 1 appended with full ghost curve specification. Renewal trigger text in §Renewal Triggers updated to reflect current invocation model. Rendering technology (Recharts/SVG), trajectory data contract, shared state architecture, confidence tier visual rules, governance null rendering, MDA floor overlay architecture, and policy/shock marker visual all unchanged. License renewed to Milestone 13.

**Previously reviewed:** 2026-06-04 — M11 exit review (SCAN-025). No renewal triggers fired during Milestone 11. No TrajectoryView component changes in M11. Matrix engine proof-of-concept runs alongside the iterative engine — no streaming trajectory update architecture introduced; shared Zustand atom state architecture unchanged. `_steps_projected` field is in the backend snapshot envelope, not in the trajectory API response. ADR-009 Decision 4 defers matrix production use to M12; the streaming trigger noted at M10 exit still does not apply. License renewed to Milestone 11.5. M11.5 usability audit may surface trajectory legibility findings — evaluate at M11.5 exit.

**M10 exit review:** 2026-06-02 (SCAN-024). No renewal triggers fired during Milestone
10. TrajectoryView was fully implemented in M10 per ADR-010 decisions — implementation
of the spec is not a trigger. Recharts/SVG rendering technology unchanged. The
trajectory API endpoint (`GET /scenarios/{id}/trajectory`) was extended with
`pmm_value` and `pmm_direction` fields for Zone 1C — these fields are not consumed by
TrajectoryView and do not change the Zone 1A data contract (trajectory curves,
confidence tiers, step annotations). Shared Zustand atom state architecture unchanged.
Confidence tier visual rules (strokeDasharray, strokeOpacity) unchanged. Governance
null rendered as absent curve, unchanged. No MDA floor overlay, A/B comparison, or
policy/shock marker changes introduced. Minimum trajectory view width constants
unchanged. License Status confirmed ACCEPTED. License renewed through Milestone 11 —
Engine Investigation and Political Economy. If ADR-009 (computation model) results in
streaming trajectory updates, the shared state architecture trigger must be evaluated.
Next scheduled review at Milestone 11 close.

**Panel (required for acceptance):**
- Frontend Architect Agent (C — implementing agent, required per panel composition rule)
- UX Designer Agent (C — Zone 1A component decisions)
- Chief Methodologist (C — confidence tier visual contracts, uncertainty band obligations)
- Engineering Lead (A — accountable on all ADR decisions)

**Renewal Triggers** — any of the following fires the CURRENT → UNDER-REVIEW transition:
- Rendering technology changed from Recharts/SVG to Canvas, WebGL, or a
  different charting library
- Trajectory data contract changed: endpoint path, response shape, or
  the `confidence_tier` → `visual_tier` field mapping revised
- Shared state architecture changed: trajectory view moves to independent
  data fetching rather than shared step state atom
- Confidence tier visual rules changed (strokeDasharray, strokeOpacity,
  badge adjacency) — note: band width changes are ADR-007-gated and are not
  themselves a renewal trigger for this ADR once ADR-007 is accepted
- Governance null rendering changed (absent curve → zero-value curve or
  vice versa)
- MDA floor overlay architecture changed (ReferenceLine → alternative)
- Live A/B comparison visual specification changed (ghost curve opacity,
  divergence fill approach, or explicit branch invocation model)
- Policy/shock marker visual changed (blue filled circle → other policy
  marker; orange vertical line → other shock marker)
- Minimum trajectory view width constants revised

## Date
2026-05-22

## Context

### Background

ADR-008 (UX Architecture, accepted 2026-05-22) establishes the trajectory view
as Zone 1A — the primary instrument in the instrument cluster primary viewport.
ADR-008 specifies what the trajectory view must do across all three interaction
modes. This ADR specifies how it is built: the component boundary, data contract,
rendering architecture, and state management pattern.

ADR-008 defers the following questions explicitly to this ADR:

- Data streaming: how does trajectory view data reach the component?
- Rendering performance: how are four animated framework curves rendered on
  the target hardware (8GB RAM, 4-core laptop per equitable build requirement)?
- Step axis state management: how does step navigation coordinate across all
  four Zone 1 instruments?
- Confidence tier visual implementation: what Recharts primitives implement
  ADR-008 Decision 13?
- Governance null curve treatment: how is null rendered differently from zero
  in the trajectory view?
- Live A/B rendering: what rendering approach produces ghost curves and the
  divergence fill region in Mode 3?
- Marker architecture: how are policy inflection markers and shock event
  markers rendered on the shared step axis?

### What ADR-006 Establishes That This ADR Must Honor

ADR-006 Decision 1 defines the pre-calibration band schedule (±10% at 1yr,
±35% at 3-5yr) and the BandingEngine contract. ADR-006 Decision 2 defines the
BandedOutput fields (`ci_lower`, `ci_upper`, `ci_coverage`, `is_pre_calibration`,
`clipped_lower`, `clipped_upper`) in the API response via QuantitySchema.

ADR-008 Decision 13 (incorporating panel finding CM-2 / FA-C4) establishes that
Tier 3-5 uncertainty band widths are gated on ADR-007 acceptance. Until ADR-007
is accepted, the visual differentiation (opacity + dashed curve + confidence
badge) is implemented but band width rendering is deferred. This ADR honors that
constraint: the band rendering infrastructure is architected to accept ADR-007's
width constants when they are defined, but does not produce visible bands in
the meantime.

### Governing Constraints From Source Documents

The six governing premises from the first-principles depth document
(`docs/ux/design-thinking/worldsim-ux-architecture-first-principles-depth.md`)
apply to all decisions in this ADR:

**Premise 3** — the step axis is the shared frame for all instruments. In Mode 1,
step axis annotation (calendar date + event label) is mandatory. All instruments
update simultaneously when a step advances or computation completes.

**Premise 2** — confidence tier is a primary instrument attribute, visible on
the instrument face. A Tier 4 trajectory curve does not visually resemble a
Tier 1 curve.

**Equitable Build** — the trajectory view must perform acceptably on 8GB RAM,
4-core laptop. Rendering choice is an equity requirement.

---

## Decision

### Decision 1 — Rendering Technology: Recharts SVG

The trajectory view is built on Recharts (already in `frontend/package.json`),
rendered as SVG. No new charting library is introduced.

**Why Recharts over Canvas or WebGL:**

Four composite score curves across 6–12 steps is a modest data volume. The
equitable build requirement (8GB RAM, 4-core laptop) constrains the rendering
approach — Canvas and WebGL have higher initialization overhead and do not
provide meaningful performance advantage over SVG at this data volume. SVG
also provides accessibility-compatible DOM elements (ARIA roles, tab focus,
screen reader traversal) that Canvas cannot.

**Why Recharts over bare D3:**

Recharts wraps D3 and provides React lifecycle integration — state updates
trigger re-renders rather than requiring manual DOM mutation. The existing
radar chart (`RadarChart.tsx`) uses Recharts; the trajectory view shares
the same rendering paradigm and can share utility functions, theming constants,
and animation configuration.

**Recharts component composition:**

```
<ComposedChart data={steps}>
  <CartesianGrid />
  <XAxis — custom tick (Decision 7) />
  <YAxis />
  <Line per framework curve (Decision 3) />
  <Line per baseline ghost curve, Mode 3 only (Decision 8) />
  <Area divergence fill, Mode 3 only (Decision 8) />
  <ReferenceLine per MDA floor (Decision 6) />
  <ReferenceLine vertical per shock event (Decision 9) />
  <Dot per policy inflection marker (Decision 9) />
</ComposedChart>
```

The `ComposedChart` type (Recharts) supports the mix of `Line`, `Area`, and
`ReferenceLine` components required by the full Mode 3 visual specification.

**Animation:** Recharts animation is disabled on initial render and enabled on
step-advance transitions. Duration: 200–300ms ease-in-out per ADR-008 Decision
4. Animation is disabled when `prefers-reduced-motion` is set (existing pattern
from radar chart implementation).

---

### Decision 2 — Trajectory Data Contract

The trajectory view requires data for all computed steps, not only the current
step. The existing `GET /scenarios/{id}/measurement-output` endpoint returns
data for the current step only. A dedicated trajectory data endpoint is required.

**New endpoint: `GET /scenarios/{id}/trajectory`**

Response shape (per-framework, per-step array):

```typescript
interface TrajectoryResponse {
  scenario_id: string;
  entity_id: string;
  steps: TrajectoryStep[];
  mda_floors: MDAFloor[];                    // one per threshold, all frameworks
  step_count: int;
}

interface TrajectoryStep {
  step_index: number;                         // 1-based
  effective_from: string;                     // ISO 8601 date
  step_event_label: string | null;            // null for ROUTINE steps
  step_significance: "SIGNIFICANT" | "ROUTINE";
  frameworks: FrameworkCurvePoint[];
}

interface FrameworkCurvePoint {
  framework: string;                          // "financial" | "human_development" |
                                              //   "ecological" | "governance"
  composite_score: number | null;             // null = governance in validation
  confidence_tier: 1 | 2 | 3 | 4 | 5;
  scoring_basis: "percentile_rank" | "normalized_absolute" | "boundary_proximity";  // Amendment 2026-05-23
  // ADR-006 banding fields (present when BandingEngine is invoked)
  ci_lower: number | null;
  ci_upper: number | null;
  ci_coverage: number | null;                 // 0.80
  is_pre_calibration: boolean | null;
}

interface MDAFloor {
  framework: string;
  floor_value: number;
  severity: "WARNING" | "CRITICAL" | "TERMINAL";
  label: string;                              // e.g. "Planetary boundary"
}
```

**Partial computation:** The trajectory endpoint returns only computed steps.
If a scenario has computed 3 of 6 steps, the response contains 3 `TrajectoryStep`
entries and `step_count: 3`. Uncomputed steps are absent — not represented as
sparse null entries. A null `composite_score` within a returned step means
governance-in-validation, not an uncomputed step. These are distinct states
and must not be conflated: absent step = computation not yet run; null
composite_score = instrument in validation.

**API contract registration:** `docs/schema/api_contracts.yml` must be updated
with this endpoint in the same commit that implements it. Schema drift is a
compliance violation.

**Query pattern:** The trajectory view fetches the full trajectory once on
scenario load and on step count change (new steps computed in Mode 2/3).
It does not refetch on each step navigation — step navigation is a client-side
state update within the already-fetched trajectory data.

**Mode 3 baseline freezing:** When the first control input is applied in Mode 3,
the current trajectory response is frozen as the baseline state in the shared
step atom (Decision 4). Subsequent trajectory fetches return the active
(modified) trajectory. The baseline is held in client state, not re-fetched.

**Amendment — single-entity scoring and step_metadata storage (2026-05-23, EL
Decisions B and C, Issue #428):**

**Single-entity composite scoring (Path A).** When a scenario contains fewer than
two entities, percentile-rank composite scores are unavailable for the financial and
human_development frameworks (ecological uses boundary-proximity scoring, which is
entity-intrinsic; governance null is handled by Decision 5). In single-entity scenarios,
the trajectory endpoint uses normalized absolute value composite scoring for financial
and human_development, as specified in the Chief Methodologist consultation
`docs/architecture/cm-reference-range-consultation-2026-05-23.md`.

Key properties of the normalized absolute composite:

- **Score range:** [0.0, 1.0] — same as percentile-rank composite; ecological [0.0, 2.0]
  scale unchanged
- **Confidence tier floor:** Tier 3 minimum for all normalized absolute scores,
  regardless of the individual indicator confidence tiers
- **Scoring basis field:** `FrameworkCurvePoint.scoring_basis` distinguishes
  `"percentile_rank"` from `"normalized_absolute"` from `"boundary_proximity"`. This
  field is mandatory on every `FrameworkCurvePoint` — it is never absent. Values by
  framework in multi-entity scenarios: financial → `"percentile_rank"`;
  human_development → `"percentile_rank"`; ecological → `"boundary_proximity"` (always
  entity-intrinsic, calibrated to planetary boundary); governance → `"percentile_rank"`
  (null composite_score when in-validation). In single-entity scenarios: financial and
  human_development → `"normalized_absolute"`; ecological and governance unchanged.
- **`null` composite_score semantics in single-entity scenarios:** A null
  `composite_score` on a financial or HD curve in a single-entity scenario means
  zero normalizable indicators were present for that framework at that step — not
  governance-in-validation and not an uncomputed step. The three null sources remain
  semantically distinct: (1) absent step = uncomputed; (2) null governance = in
  validation; (3) null financial/HD in single-entity = no normalizable indicators
  at that step. The `scoring_basis` field disambiguates cases (2) and (3) at render
  time.

**Step metadata storage (Decision C).** The `step_event_label` and `step_significance`
fields on `TrajectoryStep` are sourced from the `step_metadata` key in
`scenarios.configuration` JSONB. Structure:

```json
{
  "step_metadata": {
    "1": { "step_event_label": "Capital controls imposed", "step_significance": "SIGNIFICANT" },
    "3": { "step_event_label": "ESM programme begins", "step_significance": "SIGNIFICANT" }
  }
}
```

Keys are 1-based step index strings. Absence of a key means the step is ROUTINE —
`step_event_label` returns `null` and `step_significance` returns `"ROUTINE"` in the
response. The value `"STANDARD"` is incorrect and must be rejected by fixture
validation (see Decision 7). No database migration is required — `scenarios.configuration`
is an unconstrained JSONB column.

---

### Decision 3 — Four-Framework Composite Score Curve Layer

The primary rendering layer produces four `<Line>` components — one per
framework — using the shared `TrajectoryStep[]` data array.

**Framework color assignment (invariant):**

| Framework | Stroke color | Hex |
|---|---|---|
| Financial | Deep teal | `#2D6A8B` |
| Human Development | Warm amber | `#C67C2E` |
| Ecological | Forest green | `#3A7A4B` |
| Governance | Slate purple | `#5C4A8A` |

These are provisional hex values — the ADR-level commitment is to the color
criteria (not the specific hex codes): (a) distinguishable from blue/orange
policy-input/shock colors (Decision 9); (b) accessible for common CVD types
(deuteranopia, protanopia) when combined with the shape differentiation from
the confidence tier visual system; (c) sufficient contrast against both light
and dark backgrounds. The UX Designer holds authority over the specific hex
values. If the FA brief's CVD simulation reveals any pair is indistinguishable
under deuteranopia or protanopia, the UX Designer issues revised hex values
satisfying the criteria — no ADR amendment required. If the proposed values
pass CVD validation, they become the canonical ruling.

**Data point handling:**

- `composite_score: null` → no data point for that step. Recharts `connectNulls`
  must be `false` on all `<Line>` components — a null value produces a visible
  gap in the curve, not a zero or a connected line through zero (see Decision 5
  for rationale).
- `composite_score: 0.0` → a real zero-value data point. This must render as a
  dot on the curve at y=0, not as null. The distinction between null and zero is
  load-bearing.

**Curve stroke thickness:** 2px for active curves; 1px for baseline ghost curves
in Mode 3 (Decision 8).

---

### Decision 4 — Shared Step State Architecture

All four Zone 1 instruments (trajectory view, MDA alert panel, PMM widget,
four-framework current position) derive from a single shared step state atom.
This is the implementation of ADR-008 Decision 14's atomicity requirement.

**State shape:**

```typescript
interface ScenarioStepState {
  scenario_id: string;
  current_step: number;
  step_count: number;
  trajectory: TrajectoryResponse | null;        // full trajectory, all steps
  baseline_trajectory: TrajectoryResponse | null; // frozen on first Mode 3 control input
  computation_state: "idle" | "computing" | "complete";
  mode: "MODE_1" | "MODE_2" | "MODE_3";
}
```

**Location:** A single `useState` or Zustand atom in the top-level scenario
view component. All four Zone 1 instruments receive this state as props —
they do not independently fetch trajectory data.

**Why not independent per-instrument data fetching:** If each instrument manages
its own data fetching, React cannot guarantee they resolve in the same render
cycle. Partial updates (trajectory view shows new step, MDA alert panel shows
previous step) violate the shared step axis invariant (ADR-008 Premise 3). A
single state atom updated in one `setState` call, combined with React 18
automatic batching, guarantees all four instruments derive from the same state
in the same render cycle.

**Computation state propagation:** The `computation_state` field transitions
`idle → computing → complete` when a Mode 3 control input is applied. All four
instruments subscribe to this field to show their respective pending states
(trajectory curve pulse, PMM greyed out, alert panel "updating").

**Baseline freezing (Mode 3):** On the first applied control input in Mode 3,
the current `trajectory` is copied to `baseline_trajectory`. Subsequent
`trajectory` values reflect the modified (active) trajectory. The baseline
is never updated again for the session unless the user explicitly resets.

---

### Decision 5 — Governance Null Curve Rendering

When the governance framework's `composite_score` is `null` at a step, the
trajectory view renders no curve segment for governance at that step.

**Implementation:** `connectNulls={false}` on the governance `<Line>` component.
A null step creates a gap in the SVG path. The gap is visible and intentional.

**What must not happen:** A null governance value rendered as a zero-value data
point (a curve that drops to y=0 and back up). This would misrepresent the
epistemic state — null means "this instrument is in validation, no value exists,"
not "the governance composite score is zero." These are categorically different
claims (ADR-008 Decision 7; existing Zone 1D null treatment in M8 frontend).

**When governance is null for all steps:** No governance curve renders. The
curve label in the legend shows a "—" indicator (consistent with the Zone 1D
four-framework readout treatment). The Y-axis scale is determined by the three
non-null frameworks. The absence of the governance curve is itself information —
it is the correct display of the "governance in validation" state.

**Partial null sequences:** If governance is null for steps 1-3 and has values
for steps 4-6, a partial curve renders starting at step 4. A visual gap precedes
it. The gap communicates the validation period.

---

### Decision 6 — MDA Floor Overlay Architecture

Each active MDA threshold is overlaid on the trajectory view as a horizontal
`<ReferenceLine>` at `y = floor_value`, per framework, per threshold.

**Visual specification:**

| Attribute | Value |
|---|---|
| Stroke | Framework color (Decision 3), 50% opacity |
| Stroke pattern | Dashed (4px dash, 4px gap) |
| Stroke width | 1.5px |
| Label | Threshold severity abbreviation right-aligned at line end (e.g., "WARN", "CRIT", "TERM") |
| Hover state | Tooltip showing threshold name, floor value, indicator key |

**Composite-score-level floors only:** MDA floor lines in the trajectory view
are defined at the composite score level — not projected from indicator-level
thresholds. The `MDAFloor.floor_value` in the trajectory response is a
composite score value (matching the Y-axis of the trajectory view). Projecting
indicator-level MDA thresholds onto the composite score axis would require
deriving which composite score value corresponds to a specific indicator crossing
— a mapping that implies a precision in the projection that does not exist.
Indicator-level MDA threshold detail belongs in Zone 2B (Framework Panels),
not in the trajectory view. The trajectory view's floor lines are the composite
score floor references, not per-indicator threshold projections.

**Multiple thresholds per framework:** Multiple MDA composite score floors may
exist for one framework at different severity levels (WARNING, CRITICAL, TERMINAL).
Each renders as a separate `<ReferenceLine>` at its `floor_value`. Lines do not
merge.

**Mode 3 live A/B:** MDA floor lines overlay both the baseline (ghost) curves
and the active curves simultaneously. They do not change when the baseline is
frozen. A baseline curve descending below a floor line is visually significant —
it means the pre-intervention trajectory crossed a threshold.

**Zone 1B relationship:** The trajectory view floor line and the Zone 1B MDA
alert panel are complementary surfaces for the same threshold crossing. The
trajectory view shows the crossing in spatial context (which step, how deep
below the floor); Zone 1B shows the crossing with causal attribution and cohort
detail. Both must be consistent — the same step and the same threshold.

**Amendment — M9 deferral (2026-05-23, EL Decision A, Issue #428):**

Composite-score-level MDA floor values cannot be defined responsibly for M9.
Defining them requires: (1) a complete indicator inventory per framework, (2)
backtesting evidence showing historical composite score values at which MDA
threshold violations co-occurred, and (3) a validated mapping function from
indicator-level thresholds to composite score space. None of these conditions
are satisfied at M9. Rendering invented floor values as authoritative
`<ReferenceLine>` elements violates the No False Precision principle.

**M9 trajectory view ships with `mda_floors: []` (empty array) for all
frameworks** — except the ecological exception below. The `mda_floors.map()`
render loop produces no SVG elements for an empty array; no conditional render
guard or placeholder is needed.

**Ecological exception — WARNING floor at y=1.0 authorized for M9:** An
ecological composite score of 1.0 means the entity is at the planetary boundary
for at least one indicator. This is a boundary-crossing event by definition.
No backtesting is required to establish this floor value — it is inherent to the
ecological scoring scale. The M9 trajectory endpoint may include:

```typescript
{ framework: "ecological", floor_value: 1.0, severity: "WARNING",
  label: "Planetary boundary" }
```

in `mda_floors` when the ecological framework is active in the scenario.
All other framework floors remain deferred.

**M10 schema path — M10-B confirmed:** A new `mda_composite_floors` table
(separate from `mda_thresholds`) is the correct M10 home for composite-score-level
floors. The `mda_thresholds` table stores indicator-level thresholds; mixing
composite-level floors into it blurs the Zone 1A / Zone 2B architectural boundary.
The new table must include a non-null `cm_approval_reference` column — no composite
floor value may be seeded without a traceable Chief Methodologist consultation
reference. The `MDAFloor` response interface (above) remains correct; the backend
will read from `mda_composite_floors` rather than `mda_thresholds` when that table
exists.

---

### Decision 7 — Mode 1 Step Axis Annotation

The step axis in Mode 1 renders a custom XAxis tick component displaying three
fields per step marker per ADR-008 Decision 11 and Gap 1B in the first-principles
depth document.

**Custom tick component contract:**

```typescript
interface StepTickProps {
  step_index: number;
  effective_from: string;            // ISO 8601; rendered as "MMM YYYY"
  step_event_label: string | null;   // null for ROUTINE steps
  step_significance: "SIGNIFICANT" | "ROUTINE";
  viewport_width: number;            // determines rendering mode
}
```

**Rendering modes:**

*Standard (≥ 1024px):*
```
Step 1
Dec 2001
Deposit freeze
announced
```
Three lines stacked below the step axis. Event label only on SIGNIFICANT steps.
Label wraps at 80px max width per tick cell.

*Narrow (< 768px):*
Step index + calendar date only. Event label suppressed to a tooltip accessible
via tap/hover on the step marker. The tooltip is the only place event labels
appear at narrow viewport — they are not truncated in-line (truncated labels
at this density are illegible).

**Mode 2 and Mode 3:** The custom tick component is not active. The XAxis
uses standard Recharts default tick rendering: step index + projected calendar
date only. Event labels have no source in forward scenarios.

**Multi-case Mode 1 alignment:** When two historical entities are compared,
step indices are aligned by programme step — the `step_significance = SIGNIFICANT`
key event is always Step 1 for each entity. The XAxis renders step indices, not
calendar dates, as the primary label when two entities with different calendar
bases are on the same axis. A secondary "entity A: MMM YYYY / entity B: MMM YYYY"
annotation may appear per tick. The implementation detail is a Frontend Architect
brief decision; this ADR establishes the alignment principle.

---

### Decision 8 — Mode 3 Live A/B Rendering

After the first control input is applied in Mode 3, the trajectory view renders
two curve sets simultaneously.

**Ghost baseline curves:**

Each framework has a second `<Line>` component rendered from `baseline_trajectory`
data. Ghost curve visual specification:

| Attribute | Active curve | Ghost curve |
|---|---|---|
| Stroke | Framework color, 100% opacity | Framework color, 50% opacity |
| Stroke width | 2px | 1px |
| Stroke pattern | Solid | Solid |
| Interactive | Hover tooltip: active value | Hover tooltip: baseline value |
| Data source | `trajectory` | `baseline_trajectory` |

Ghost curves are fully interactive — hovering or tapping shows the baseline
composite score at that step. This allows the user to see exactly what they
changed at each step without reading a table.

**Divergence fill region:**

The area between the baseline and active curves is filled with semi-transparent
shading where they diverge. Implementation: a `<defs>` + `<clipPath>` SVG
pattern, or a custom `<Area>` component with the baseline as the `baseLine`
prop. Fill specification:

| Attribute | Value |
|---|---|
| Fill color | Framework color (Decision 3) of the active curve |
| Fill opacity | 5–10% |
| Visibility | Appears when `|active_score - baseline_score| > 0.01` per step |
| Disappears | When trajectories re-converge below the 0.01 threshold |

A separate divergence fill renders for each framework. All four fills may be
simultaneously visible if all four frameworks diverge.

**Before first control input (observation mode):** Single trajectory set only.
No ghost curves. No divergence fill. `baseline_trajectory` is null. The
trajectory view renders exactly as in Mode 2 — projected curves only.

**Re-convergence:** If the active trajectory re-converges with the baseline
(because a later control input reversed an earlier one's effect), the divergence
fill disappears for the steps where they re-converge. The ghost curves remain
visible even when the active trajectory returns to the baseline.

---

### Decision 9 — Policy Inflection and Shock Event Markers

The trajectory view displays two categories of markers in Mode 3 (and in Mode 1
for historical reconstruction of applied policies):

**Policy inflection markers (blue, per affected curve):**

A filled circle (`●`) rendered at the step where a policy input was applied, on
the specific framework curve(s) the input affects.

| Attribute | Value |
|---|---|
| Shape | Filled circle, 12px diameter |
| Color | `#1A6BAF` (WorldSim policy blue — consistent with control plane) |
| Position | On the affected framework curve(s) at the input step's x-coordinate |
| Label | Short inline label below the marker: "−2% spending cut" (max 5 words) |
| Interactivity | Click/tap: tooltip showing full ControlInput parameters |
| Not rendered on | Unaffected framework curves at that step |

Implementation: custom `dot` prop on the `<Line>` component, rendering conditionally
for steps matching the applied control input's `step_index`.

**Shock event markers (orange, across all curves):**

A vertical line at the step where an exogenous shock was injected, extending
across all four framework curves.

| Attribute | Value |
|---|---|
| Shape | Vertical `<ReferenceLine>` at x = shock step |
| Color | `#C45C00` (WorldSim shock orange — consistent with control plane) |
| Stroke width | 1.5px |
| Label | Orange label at top of line: "SHOCK: [shock type], step N" |
| Interactivity | Click/tap: tooltip showing shock type and parameters |
| Extends across | All four framework curves simultaneously |

Implementation: `<ReferenceLine>` at the chart level (not per-curve), with
`stroke={SHOCK_ORANGE}` and `label` prop.

**Co-location rule:** When a policy input and a shock occur at the same step,
both markers render. The blue filled circle on affected curves and the orange
vertical line across all curves appear simultaneously and must not merge. The
vertical orange line and the blue dots are visually distinct by shape and by
color even when at the same x-coordinate. The cross-layer color contract
(ADR-008 Decision 12) applies: blue = policy input, orange = shock, in the
trajectory view as in the control plane and alert panel.

---

### Decision 10 — Confidence Tier Visual Implementation

ADR-008 Decision 13 specifies the confidence tier visual differentiation rules.
This decision specifies the Recharts implementation of those rules.

**Per-tier Recharts attributes on `<Line>` components:**

| Tier | Recharts stroke pattern | strokeOpacity | strokeDasharray |
|---|---|---|---|
| Tier 1–2 | Solid | 1.0 | None |
| Tier 3 | Solid | 0.75 | None |
| Tier 4–5 | Dashed | 0.60 | "6 4" |

`strokeDasharray="6 4"` produces a 6px dash, 4px gap pattern — visually
distinct from MDA floor lines (Decision 6, "4 4") and shock event markers
(Decision 9, solid).

**Confidence badge (Tier 4–5):**

A small text label rendered adjacent to the curve label in the Recharts
`Legend` component:
`"Governance (exploratory)"` — where "exploratory" is the badge text.

The badge is not rendered on the chart face (curve label inline with the curve
is visually cluttered at small widths). It appears in the legend entry only.
In Mode 2 and Mode 3, the badge in Zone 2B Framework Panels is interactive
(tapping opens the methodology note) — this is not in scope for the trajectory
view's own legend, but must not be blocked by the legend implementation.

**Uncertainty band infrastructure (ADR-007-gated):**

The trajectory data contract (Decision 2) includes `ci_lower` and `ci_upper`
fields. The rendering infrastructure for bands is built but produces no visible
output until ADR-007 defines the band width constants for Tier 3-5.

Implementation: an `<Area>` component with `dataKey={ci_upper_key}` and
`baseLine={ci_lower_key}` at very low `fillOpacity` (0.08), rendered only when
`ci_lower` and `ci_upper` are non-null in the TrajectoryStep data. Until ADR-007
is accepted, the BandingEngine does not populate ci values for composite scores
in the trajectory endpoint, so the Area component renders nothing. When ADR-007
is accepted and its width constants are implemented in the BandingEngine, the
band visualization activates without further frontend changes.

**Deferral period placeholder:** During the ADR-007 deferral period, Tier 3-5
curves display a small label adjacent to the curve label in the Legend:
`"Governance (exploratory — band pending)"`. This makes the deferral visible
rather than invisible. A user who notices the absence of bands on a Tier 4 curve
must be able to understand why — the placeholder label provides the signal.
When ADR-007 is accepted and bands activate, the "(band pending)" suffix is
removed from the legend label automatically (conditional on `ci_lower !== null`
in the trajectory data).

---

## Alternatives Considered

### Alternative 1: Canvas-Based Rendering (D3 + Canvas)

**Description:** Use D3 directly against a `<canvas>` element for trajectory
view rendering. Canvas provides higher performance ceiling for dense data.

**Why rejected:** At 6–12 steps and four curves, the performance difference
between SVG and Canvas is negligible on the target hardware. Canvas requires
manual DOM management for interactivity (hover, tap, tooltip) — each interaction
requires hit-testing against manually tracked element positions. Accessibility
is not native to Canvas (no ARIA, no tab focus). The existing radar chart uses
Recharts SVG; introducing Canvas would create two rendering paradigms for
adjacent instruments. The equitable build requirement does not motivate Canvas.

### Alternative 2: Independent Per-Instrument Data Fetching

**Description:** Each Zone 1 instrument fetches its own data independently
using separate `useQuery` hooks per component.

**Why rejected:** Independent data fetching cannot guarantee simultaneous
updates. React may render four components in four separate cycles if their
queries resolve at different times, even with React 18 automatic batching.
The shared step axis invariant (ADR-008 Decision 14, Premise 3) requires
a single state update that propagates to all four instruments atomically.
Independent fetching is the architecture that produces "trajectory view shows
step 3 while MDA panel shows step 2" — the exact violation the atomicity
contract is designed to prevent.

### Alternative 3: Step-by-Step Data Fetching (No Trajectory Endpoint)

**Description:** Fetch data for each step individually as the user navigates,
reusing the existing `GET /scenarios/{id}/measurement-output` endpoint with
a `?step=N` parameter.

**Why rejected:** Step-by-step fetching introduces network latency on each
step navigation. In Mode 1 (trajectory reconstruction), the user navigates
steps sequentially and must be able to move quickly through the programme
timeline. A per-step network round-trip produces a visible delay that breaks
the trajectory reconstruction flow. The dedicated `GET /scenarios/{id}/trajectory`
endpoint fetches all steps once; subsequent step navigation is instantaneous
(client-side state update from the cached trajectory data).

### Alternative 4: Horizontal Bar Chart for Uncertainty Bands

**Description:** Render uncertainty bands as horizontal extent bars rather
than shaded areas around the curve.

**Why rejected:** Horizontal bars obscure curve-to-curve comparison — the primary
purpose of the trajectory view. The trajectory view communicates trajectory
shape (slope, acceleration, reversal), not point estimates at each step. Shaded
bands around the curve preserve the curve's trajectory signal while adding the
uncertainty dimension as a visual envelope. Horizontal bars make the uncertainty
visible at the cost of the trajectory signal.

### Alternative 5: Full-Screen MDA Floor Lines (All Thresholds Always Visible)

**Description:** Render all MDA floor lines (all frameworks, all thresholds)
simultaneously at all times.

**Why rejected:** For a scenario with thresholds across all four frameworks at
multiple severity levels, full-time rendering produces visual clutter that
undermines trajectory legibility. The current design renders only the floors
for MDA thresholds active in the scenario. At the viewport minimum (1024×768),
the trajectory view height may be ~300-340px — rendering 8+ threshold lines at
that height would make the chart unreadable. The Zone 1B MDA alert panel handles
the threshold crossing summary; the trajectory view's floor lines serve as
contextual floor references, not a complete threshold inventory.

### Alternative 6: User-Invoked Mode 3 A/B Comparison

**Description:** A "Show baseline" toggle the user must activate to see ghost
curves in Mode 3.

**Why rejected:** ADR-008 Decision 10 establishes that live A/B is automatic.
The rationale is in ADR-008: in Mode 3, "baseline vs. active" is the cognitive
task — it is not an optional view. A toggle at the moment of first control input
application introduces an action at the highest-cognitive-load moment of the
interaction. The ghost curves appearing automatically on first control input is
the correct design.

---

## Consequences

### Positive

**Recharts reuse eliminates a new dependency.** The trajectory view and radar
chart share one charting library, one animation configuration, and one theming
pattern. No Canvas or WebGL dependency is introduced. The equitable build
requirement is satisfied.

**The dedicated trajectory endpoint enables instantaneous step navigation.**
Once the TrajectoryResponse is fetched on scenario load, all step navigation is
a client-side state transition. Latency is bounded by the initial fetch, not
repeated per step.

**The shared state atom makes the atomicity contract mechanically enforceable.**
A single `setState` call propagates to all four Zone 1 instruments in one React
render cycle. The partial-update violation (trajectory view at step N, MDA panel
at step N-1) becomes structurally impossible given correct implementation.

**ADR-007-gated band infrastructure is built without activating bands.**
The frontend is ready to display uncertainty bands when ADR-007 defines the
width constants. No frontend change is required at ADR-007 acceptance — the
BandingEngine populates `ci_lower`/`ci_upper` in the trajectory response, and
the `<Area>` component activates automatically.

**Governance null rendering is honest.** A null composite score produces a
visible curve gap — not a zero, not a connected line through absent data. The
governance-in-validation state is visible and informative in Zone 1A, consistent
with Zone 1D's "—" treatment.

### Negative

**The trajectory endpoint is a new API surface.** A new GET endpoint requires:
FastAPI route, Pydantic response model, BandingEngine integration for composite
score banding, `docs/schema/api_contracts.yml` update. This is non-trivial
backend work that must precede or accompany frontend implementation.

**ComposedChart supports mixed component types but is more complex than
LineChart.** The `<ComposedChart>` type is necessary to mix `<Line>`, `<Area>`,
and `<ReferenceLine>` in one chart. The radar chart uses `<RadarChart>` — the
patterns do not directly transfer. The Frontend Architect must validate
ComposedChart behavior with the full component set before committing to the
approach.

**Mode 3 ghost curves double the Line component count.** At four frameworks,
Mode 3 requires eight `<Line>` components plus four `<Area>` divergence fills
plus potentially many `<ReferenceLine>` floor overlays and markers. At 1024×768
this is a heavier SVG DOM. The FA brief must include a rendering performance
validation on the target hardware (8GB/4-core) with all Mode 3 components active.

**Framework color assignment requires CVD validation before implementation.**
The four framework colors specified in Decision 3 are a new commitment. The FA
brief must run them through a CVD simulation tool (e.g., Color Oracle or
equivalent) and confirm distinguishability before the colors are used in code.
If any color pair is indistinguishable under deuteranopia or protanopia, the
palette must be revised in the brief before implementation begins.

**Custom XAxis tick in Mode 1 requires careful height allocation.** Three-line
step markers (step index, date, event label) require more vertical space than
standard single-line ticks. At 1024×768, the available height for the trajectory
view is constrained. The FA brief must allocate axis space explicitly and
confirm the three-line tick is legible at the minimum trajectory view height
without truncation.

### Open Risks

**Recharts ComposedChart performance with full Mode 3 component set at 1024×768:**
Eight `<Line>` components, four `<Area>` components, and variable `<ReferenceLine>`
counts is an untested configuration on the target hardware. The FA brief must
include a performance baseline: render time at initial load and on step navigation
must not exceed 100ms (to stay within the 200-300ms animation window without
visible lag before animation begins).

**Divergence fill implementation:** The "area between two line curves" is not
a native Recharts pattern. The `<Area>` component with `baseLine` requires
matching data keys between the baseline and active trajectories at each step
index. If the baseline and active trajectories have different numbers of computed
steps (Mode 3 mid-computation), the fill algorithm must handle missing steps
gracefully. The FA brief must specify the fill implementation approach and
validate it handles step count mismatches.

**Trajectory endpoint query timing:** In Mode 3, the `trajectory` data updates
after each control input computation completes. The shared state atom must
handle the transition from `computing` to `complete` without producing a
flash of stale data. The FA brief must specify the loading state treatment
during trajectory re-fetch.

---

## Dependency Map

| Depends On | Why |
|---|---|
| ADR-008 Decision 1 | Trajectory view is Zone 1A — primary viewport placement |
| ADR-008 Decision 4 | Trajectory view core requirements: four curves, shared step axis, MDA floor overlay, Mode 3 ghost curves |
| ADR-008 Decision 11 | Step axis annotation schema: `effective_from`, `step_event_label`, `step_significance` |
| ADR-008 Decision 12 | Blue/orange color contract for policy markers and shock markers |
| ADR-008 Decision 13 | Confidence tier visual rules (solid/dashed, opacity, badge) |
| ADR-008 Decision 14 | Simultaneous instrument update contract — motivates shared state atom |
| ADR-006 Decision 1 | Pre-calibration band schedule — governs `ci_lower`/`ci_upper` values in trajectory response |
| ADR-006 Decision 2 | BandedOutput fields in API response — trajectory endpoint must include these |
| ADR-007 (pending) | Tier 3-5 band width multipliers — gates visible uncertainty band rendering |
| Issue #366 | This ADR — blocks M9 Frontend Architect brief |
| Greece fixture | Must include `step_event_label` on SIGNIFICANT steps before Mode 1 CI gate activates |

---

## Diagram

Trajectory view component architecture: `docs/architecture/ADR-010-trajectory-view-architecture.mmd`

---

## Amendment 1 — M12 Mode 3: Ghost Curve Visual Specification

**Date:** 2026-06-10
**Trigger:** Live A/B comparison visual specification changed (§Renewal Triggers)
**Implemented in:** M12 Mode 3 Active Control — branch/baseline ghost curve display in Zone 1A

### Context

Mode 3 introduces a branch scenario (created via `POST /scenarios/{id}/branch`, see ADR-008 Amendment 1). When a branch is active, Zone 1A must render two trajectories simultaneously: the pre-branch baseline (ghost curve) and the active branch trajectory (primary curve). This amendment specifies the Recharts rendering contract for both curves and the divergence fill region between them.

### Ghost Curve Specification

**Baseline (ghost) trajectory — Recharts `<Line>` props:**

| Prop | Value | Rationale |
|---|---|---|
| `strokeOpacity` | `0.3` | Same opacity reduction as Tier 4 confidence — reuses the existing "secondary / lower-confidence" visual register |
| `strokeDasharray` | `"4 4"` | Same dashed pattern as Tier 3–5 confidence curves — reuses the "uncertainty / non-primary" visual register |
| `stroke` | Same as active framework curve color | Ghost reads as the same indicator, not a different one |
| `dot` | `false` | No step markers on ghost curve — reduces visual noise against the primary trajectory |
| Band fill | Not rendered | Pre-branch uncertainty bands are not shown in Mode 3 — active branch trajectory has primary claim on band visual space |

**Active branch trajectory — Recharts `<Line>` props:**

| Prop | Value | Rationale |
|---|---|---|
| `strokeOpacity` | `1.0` | Full opacity — primary curve |
| `strokeDasharray` | `none` (solid) | Primary trajectory |
| `stroke` | Framework curve color | Identical to Mode 1/2 rendering |

### Divergence Fill Region

The divergence fill renders between the ghost curve and the active branch trajectory for each framework using a Recharts `<Area>` component with `baseLine` pointing to the ghost curve data series.

**Fill color rules (consistent with ADR-008 Decision 12 blue/orange contract):**

| Branch direction | Fill color | Opacity | Meaning |
|---|---|---|---|
| Branch > ghost (improvement) | `#1565C0` (blue) | `0.12` | Branch trajectory above baseline — condition improving |
| Branch < ghost (deterioration) | `#E65100` (orange) | `0.12` | Branch trajectory below baseline — condition worsening |
| Branch = ghost (no divergence) | No fill | — | Trajectories identical at this step |

**Temporal scope of fill:**
- Steps before `branch_from_step`: ghost and active trajectories are identical — no fill rendered
- Steps at and after `branch_from_step`: fill renders between the two trajectories wherever both have data
- If the active branch trajectory has fewer computed steps than the ghost: fill stops at the last computed branch step

**Step count mismatch handling:** If the ghost and branch trajectories have different computed step counts (e.g., branch computation is in progress), the `<Area>` fill clips at whichever trajectory ends first. No interpolation — missing steps produce no fill.

### Invocation and Session Lifecycle

- Ghost curve appears when `branch_scenario_id` is present in the session Zustand atom (set by the branch action in the Mode 3 control plane)
- Ghost curve disappears when the user resets to baseline (branch scenario deleted, `branch_scenario_id` cleared from atom)
- No ghost curve in Mode 1 or Mode 2 — branch action is Mode 3 only

---

## Amendment 2 — Zone 1B CohortImpactSection: Monitored-Row State and Temporal Disambiguation

**Date:** 2026-06-29
**Trigger:** G7 Step 6b root cause analysis (2026-06-29) identified that `CohortImpactSection` renders only breach rows — threshold-cleared focal indicators are invisible (DEMO-134 CRITICAL). Demo 7 Act 1's primary argument is a CLEARED threshold finding ("informal workers poverty headcount remains at 0.450 — ten points above the 0.40 recovery floor"), which was structurally invisible in the current design. DEMO-140 (HIGH) further identified that historical breaches display with the same visual weight as current-step violations, creating a temporal contradiction.
**Source document:** `docs/demo/m18/reviews/2026-06-29-g7-root-cause-analysis.md §Root Cause 3`
**Implemented in:** M18 G7 Cluster C — `MDAAlertPanelZone1B.tsx`

### Rationale for Extension of ADR-010 Scope

`CohortImpactSection` is a Zone 1B surface. This amendment extends ADR-010 to cover its state behavior because the monitored-row derivation depends on the **shared step state atom** (Decision 4):

- **CLEAR/BREACHED status** at any row is derived from `current_step` (from shared atom)
- **Temporal disambiguation** (current breach vs. historical breach) requires comparing `crossing.step_index` against `current_step` — a computation over the shared state
- **Monitored focal current value** reads from `trajectory` at `current_step` (from shared atom)

These are Zone 1 instrument behaviors rooted in the shared state architecture. ADR-010 is the canonical home for "how Zone 1 instruments derive state from the shared atom" (Decision 4). Placing this in ADR-008 would fragment the state architecture specification across two ADRs.

### What Changes

**New section: CohortImpactSection Monitored-Row State**

#### Monitored Focal Indicators

**Monitored focal indicators** are scenario-designated cohort indicators that render in `CohortImpactSection` at every step regardless of breach status. They represent the focal human cost argument of the scenario — indicators the analyst is tracking even when no threshold crossing has occurred.

**Data source — `scenarios.configuration` JSONB key `monitored_focal_cohorts`:**

```json
{
  "monitored_focal_cohorts": [
    {
      "indicator_key": "bottom_quintile_informal_workers_poverty_headcount",
      "floor_value": 0.40,
      "floor_label": "Recovery floor",
      "framework": "human_development"
    }
  ]
}
```

Key `monitored_focal_cohorts` is optional. Absence means no designated focal indicators — `CohortImpactSection` renders breach-only rows from the `crossings` store, unchanged from current behavior.

**Monitored-row states:**

| State | Condition | Badge label | Badge color | Row prefix |
|---|---|---|---|---|
| CLEAR | `current_value > floor_value` at `current_step`, no prior breach | CLEAR | Green (#2e7d32) | None |
| BREACHED (current) | `current_value ≤ floor_value` at `current_step` | CRITICAL | Red (#c62828) | None |
| PRIOR BREACH, NOW CLEAR | `current_value > floor_value` at `current_step`, but crossed threshold at prior step N | HIST | Amber (#a06000) | "Breached at step N —" |

Each monitored-row displays without expansion:
- Indicator display name (human-readable, per Zone 2B label standard)
- Current value (3 decimal places)
- Floor value
- Status badge (CLEAR / CRITICAL / HIST)
- T3 confidence badge when data tier ≥ 3

**Monitored focal rows render first in `CohortImpactSection`**, above breach-only rows from the `crossings` store.

#### Temporal Disambiguation for All Rows

All `CohortImpactSection` rows — including breach-only rows from the `crossings` store — apply temporal disambiguation based on `current_step`:

- **Current-step breach:** `crossing.step_index === current_step` — red CRITICAL badge, no prefix (existing behavior, unchanged)
- **Historical breach:** `crossing.step_index < current_step` — amber (#a06000) HIST badge, prefix "Breached at step N —"
- `headerLabel` appends "(including historical)" when any historical-breach rows are present, not only when `isCompleted === true`

#### State Derivation (Shared Step Atom)

All monitored-row and temporal disambiguation state is derived from the shared `ScenarioStepState` (Decision 4):

```typescript
const currentStep = state.current_step;                                    // shared atom
const historicalCrossings = crossings.filter(c => c.step_index < currentStep);
const currentCrossings = crossings.filter(c => c.step_index === currentStep);
const monitoredRows = monitoredFocalCohorts.map(focal => ({
  ...focal,
  currentValue: getValueAtStep(focal.indicator_key, currentStep, state.trajectory),
  rowState: deriveFocalRowState(focal, currentStep, crossings)
}));
```

No new network requests are required. All data derives from the existing shared atom fields (`current_step`, `trajectory`, `crossings`).

### Impact on Other Decisions

ADR-010 Decisions 1–10 (trajectory view component architecture) are unchanged. This amendment adds a new section covering Zone 1B `CohortImpactSection` state behavior insofar as it depends on the shared step state atom (Decision 4). The trajectory view itself (Zone 1A) is unaffected. ADR-008 Decision 5 §MDA Alert Panel Specification is unchanged at the ADR level; this amendment specifies the implementation contract for monitored-row state within the Zone 1B surface.

### Renewal Trigger Assessment

No listed renewal trigger fires. The shared state architecture (single atom, shared across Zone 1 instruments) is unchanged — this amendment extends what is consumed from the atom, not the atom's architecture or sharing contract. Rendering technology, trajectory data contract, confidence tier visual rules, governance null rendering, MDA floor overlay, live A/B comparison visual specification, policy/shock marker visual, and minimum trajectory view width constants are all unchanged.

### Panel Sign-Off

**Architect Agent:** The monitored-row state belongs in ADR-010 because it is a state-derivation behavior rooted in Decision 4 (shared step atom). The data source (JSONB `monitored_focal_cohorts`) is the correct location — it co-locates the designation with the scenario configuration rather than hardcoding it in the component. The temporal disambiguation (red/amber) eliminates the DEMO-140 temporal contradiction without removing historical breach information. The "PRIOR BREACH, NOW CLEAR" state (HIST amber) is a meaningful new communicative state: it tells the analyst the indicator was dangerous and is now safe — a different claim from "CLEAR with no prior breach" and a different claim from "BREACHED."

☑ Architect Agent sign-off — 2026-06-29

**UX Designer Agent sign-off:**

Per EL determination 2026-06-29 (G7-0 root cause analysis sign-off block): **separate-session UX Designer sign-off is required** before Cluster C implementation PR opens. This amendment is gated until that sign-off is obtained. EL must trigger a separate UX Designer session to review the monitored-row state design before this amendment is accepted.

- Reviewing agent: UX Designer Agent
- Session context: Separate session, EL-triggered 2026-06-29
- Governing documents reviewed: `north-star.md §Primary Cognitive Tasks by Mode` (Mode 3 cognitive task definition; capability analysis framing for declarative alert language); `user-journeys.md §Journey C Step 3` (Mode 3 causal attribution reading; requirement that ghost curves and alert panel confirm same finding); `information-hierarchy.md §Zone 1 — Primary §1B — MDA Alert Panel` (severity ordering rule: TERMINAL before CRITICAL before WARNING; top-1-3 alerts without scroll); `information-hierarchy.md §CVD (Colour Vision Deficiency) Color Specification` (MV-001 gate applies to alert panel treatment); `docs/ux/design-thinking/worldsim-ux-architecture-first-principles.md §Five Design Premises for M9` (Premises 2 and 3 — primary instruments always visible; step axis as shared frame)
- Concerns found: 2 concerns, both non-blocking. (1) CVD — green `#2e7d32` (CLEAR) vs. red `#c62828` (CRITICAL) are indistinguishable under deuteranopia. Text labels are the primary signal and mitigate this adequately per the governing capability-analysis framing. Implementation PR must document that the new Zone 1B badge pair is included in the MV-001 CVD validation gate per `information-hierarchy.md §CVD Color Specification`. No redesign required. (2) Ordering — `information-hierarchy.md §1B` specifies severity ordering (TERMINAL before CRITICAL before WARNING). Placing all monitored focal rows before all breach-only rows is correct and intentional for Demo 7's specific fixture (CLEAR focal row is the primary argument). In the general case, a CLEAR-state focal row appearing before a CRITICAL breach-only row may suppress a critical finding from the first-scan zone. Implementation brief should specify: focal rows in CRITICAL/TERMINAL state render at the top of CohortImpactSection; CLEAR-state focal rows render after all CRITICAL/TERMINAL rows (focal or breach-only) but before WARNING rows. This preserves severity ordering while honoring focal designation.

☑ UX Designer sign-off — 2026-06-29

**Engineering Lead acceptance:** Pending — UX Designer sign-off received 2026-06-29 (separate session, EL-triggered). EL must verify governing document citations and accept before Cluster C implementation may begin.
