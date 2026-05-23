# M9 Frontend Architect Brief — Instrument Cluster Implementation

> **Document type:** Frontend Architect Implementation Brief
> **Agent:** Frontend Architect Agent
> **Authored:** 2026-05-22
> **Status:** Awaiting UX Designer sign-off before implementation begins
> **Implements:** ADR-008 (UX Architecture), ADR-010 (Trajectory View Component Architecture)
> **Gates:** M9 instrument cluster implementation; Mode 1 CI annotation gate

---

## RACI Authority and Boundaries

The Frontend Architect Agent holds **R** on frontend component architecture briefs (RACI Row 1:
C on ADR decisions; R on briefs). This document makes implementation decisions within the
boundaries established by ADR-008 and ADR-010. Decisions that exceed brief authority are
flagged explicitly with the approval required.

**What this brief decides (FA authority):**

- Layout constants (column widths, row heights, zone sizing) within the ADR-established
  minimum constraints
- State management implementation approach (Zustand vs. useState)
- Divergence fill implementation technique
- Character-count constraint on step annotation labels
- CVD validation tool and procedure
- Acceptance criteria for all named brief requirements from ADR-008 and ADR-010 panel reviews

**What this brief confirms (records EL or UX Designer rulings):**

- Control plane zone width = 280px (EL ruling, 2026-05-22, FA-C3 disposition in
  `docs/adr/reviews/ADR-008-panel-review.md`)
- UX Designer authority over specific framework color hex values (ADR-010 Decision 3)
- Multi-case Mode 1 tick format: dual entity dates stacked per tick (required, not optional —
  UX Designer ruling UD-R2)
- Confidence badge on curve face for Tier 4-5 curves (UX Designer ruling UD-R3)

**What this brief does not decide:**

- Framework color hex value revisions (UX Designer authority — see §Framework Colors)
- ADR-007 band width constants (Chief Methodologist authority, gates band rendering)
- Zone assignment changes (EL decision required, recorded in `design-decisions.md`)

---

## Source Documents Read

Before writing this brief, the Frontend Architect Agent read:

1. `docs/adr/ADR-008-ux-architecture.md` — all 17 decisions
2. `docs/adr/ADR-010-trajectory-view.md` — all 10 decisions
3. `docs/adr/reviews/ADR-008-panel-review.md` — FA-C1 through FA-C5, all findings
4. `docs/adr/reviews/ADR-010-panel-review.md` — FA-R1 through FA-R5, UD-R2, UD-R3, all findings
5. `docs/process/agent-raci.md` — Row 1 (Architectural), Row 2/3 (UX decisions)

---

## Deferred Items Addressed by This Brief

This brief closes every item explicitly deferred to the "M9 Frontend Architect brief" in the
two ADR panel reviews.

| ID | Source | Status in this brief |
|---|---|---|
| FA-C1 | ADR-008 panel — Zone 1 layout at 1024×768 | §Layout and Viewport |
| FA-C2 | ADR-008 panel — State management atomicity design decision | §Shared State Architecture |
| FA-C3 | ADR-008 panel — Control plane zone width (EL ruling) | §Layout and Viewport |
| FA-C4 | ADR-008 panel — Uncertainty bands linked to ADR-006 | §Uncertainty Band Infrastructure |
| FA-C5 | ADR-008 panel — Step annotation character validation at 1024px | §Mode 1 Step Axis Annotation |
| FA-R1 | ADR-010 panel — Mode 3 ComposedChart performance acceptance criterion | §Performance Acceptance Criteria |
| FA-R2 | ADR-010 panel — Divergence fill implementation approach | §Divergence Fill Implementation |
| FA-R4/UD-R1 | ADR-010 panel — CVD validation before implementation | §Framework Colors |
| FA-R5 | ADR-010 panel — Named minimum trajectory view dimensions | §Layout and Viewport |
| UD-R2 | ADR-010 panel — Multi-case Mode 1 dual entity dates (UX ruling) | §Mode 1 Step Axis Annotation |
| UD-R3 | ADR-010 panel — Curve-face confidence badge on Tier 4-5 (UX ruling) | §Confidence Tier Visual |

---

## Named Acceptance Criteria

Every criterion here is testable before M9 implementation is considered complete.

| ID | Criterion | How tested |
|---|---|---|
| AC-001 | All four Zone 1 instruments visible without scroll at 1024×768 | Playwright screenshot at 1024×768 viewport |
| AC-002 | All four Zone 1 instruments visible without scroll at 1280×800 | Playwright screenshot at 1280×800 viewport |
| AC-003 | Trajectory view minimum width ≥ 480px at 1024×768 | Computed width assertion in Playwright |
| AC-004 | Trajectory view minimum width ≥ 580px at 1280×800 | Computed width assertion in Playwright |
| AC-005 | Trajectory view minimum height ≥ 300px at any supported viewport | Computed height assertion in Playwright |
| AC-006 | All four Zone 1 instruments update in a single render cycle on step advance | React Testing Library: wrap step-advance in `act()`; assert all four instrument DOM nodes reflect new `current_step` within the same `act()` call before it resolves |
| AC-007 | ComposedChart initial render ≤ 100ms on CI throttled profile | `performance.measure` in Playwright; 4× CPU throttle (`page.emulate({cpuThrottling:4})`); see also hardware validation note in §Performance Acceptance Criteria |
| AC-008 | ComposedChart step navigation ≤ 100ms on CI throttled profile | `performance.measure` in Playwright; same throttle as AC-007 |
| AC-009 | Full Mode 3 component set (8 Lines + 4 Areas + 6+ ReferenceLines) ≤ 100ms on CI throttled profile | `performance.measure` at Mode 3 full activation; same throttle |
| AC-010 | Divergence fill disappears when \|active - baseline\| ≤ 0.01 at every step | Vitest unit test: assert no `<Area>` fill rendered when delta ≤ 0.01 |
| AC-011 | Mode 1 step annotation renders three-line tick at ≥ 1024px viewport | Playwright screenshot; verify three text nodes per SIGNIFICANT step tick |
| AC-012 | Step annotation event label: ≤ 8 words AND ≤ 32 characters; fixture CI gate rejects violations | `pytest tests/fixtures/` schema validation; runs on every PR |
| AC-013 | Tier 4-5 curves show "(exp)" label adjacent to most recent data point in chart body | Playwright screenshot; assert `<text>` element present in SVG adjacent to rightmost data point on Tier 4-5 curve |
| AC-014 | Control plane reserved zone = 280px width at 1280×800; trajectory view width ≥ 580px | Computed width assertions in Playwright |
| AC-015 | Null governance composite score renders as curve gap, not zero | Vitest unit test: mount `TrajectoryView` with fixture having `composite_score: null` at step 3; assert governance `<Line>` has `connectNulls={false}` prop; assert no rendered data-point element at step 3 x-position for governance line |

---

## Manual Validation Gates

These gates cannot be automated in CI. Each must be completed and recorded before M9 exits.

| ID | Gate | How completed |
|---|---|---|
| MV-001 | Four framework colors pass CVD check (deuteranopia + protanopia) | Color Oracle or equivalent; procedure in §Framework Colors; result recorded in §CVD Validation Result |
| MV-002 | Performance ≤ 100ms on actual target hardware (8GB/4-core laptop) | Developer runs `performance.measure` test on target machine; documents result in PR description |
| MV-003 | UX Designer sign-off on component layout decisions | Sign-off section completed in this brief before first implementation PR |

MV-002 exists because Playwright's 4× CPU throttle (`cpuThrottling`) applies a slowdown to the
JS thread on the test machine — it is not a simulation of a 4-core CPU. On high-core-count CI
runners, 4× throttling may produce a faster effective runtime than an actual 4-core laptop. AC-007
through AC-009 are the CI gate; MV-002 is the hardware confirmation before M9 closes.

---

## Layout and Viewport

### Minimum Supported Viewports

| Viewport | Classification | Source |
|---|---|---|
| 1280×800 | Desktop minimum | ADR-008 Decision 1 |
| 1024×768 | Tablet minimum | ADR-008 Decision 1 |

Browser chrome (OS UI bars, browser navigation) is assumed to consume ~80px vertical height.
Effective viewport heights: 1280×800 → ~720px usable; 1024×768 → ~640–680px usable.

### Zone 1 Layout — Two-Column Instrument Cluster (FA-C1 Resolution)

At all supported viewports, the instrument cluster uses a two-column layout:

- **Left column:** Zone 1A (trajectory view) — primary instrument, full column height
- **Right column:** Zones 1B, 1C, 1D (MDA alert panel, PMM widget, four-framework current
  position) — stacked vertically, each occupying one third of the right column height

**Column width constants (binding for implementation):**

| Viewport | Trajectory view (left) | Co-primary cluster (right) | Control plane zone |
|---|---|---|---|
| 1024×768 | 480px | 240px | 280px (reserved) |
| 1280×800 | 580px | 400px | 280px |

Total at 1024×768: 480 + 240 + 280 = 1000px, leaving 24px for layout padding and scrollbars.
Total at 1280×800: 580 + 400 + 280 = 1260px, leaving 20px for layout padding and scrollbars.

**Why 480px trajectory view minimum at 1024×768 (not 560px as initially proposed in FA-C1):**
FA-C1 proposed 560px without accounting for the 280px control plane zone reservation (EL ruled
Option A, 2026-05-22). At 1024×768, 560px trajectory + 240px co-primary + 280px control plane
= 1080px — exceeds the viewport. The correct minimum is 480px, which maintains instrument
legibility while satisfying the control plane zone reservation. The 480px minimum is confirmed
against the step annotation render test (see §Mode 1 Step Axis Annotation) and the four-curve
trajectory view (see §Performance Acceptance Criteria).

**MDA alert panel compact row format at 240px (UD-F1 — UX Designer ruling):**

At 240px column width (1024×768), the four fields required by ADR-008 Decision 5 cannot render
at full density without overflow or expansion. The compact row format at this width is:

- **Line 1:** Severity pill (8px × 6px colored circle) + severity abbreviation ("WARN" / "CRIT"
  / "TERM") + framework source abbreviation ("FIN" / "HDI" / "ECO" / "GOV")
- **Line 2:** Indicator name, truncated at 22 characters with ellipsis (e.g.,
  `poverty_headcount` → "poverty headcount...")
- **Line 3:** "Step N • [cohort abbreviation, ≤ 10 characters]"

This satisfies "visible without expansion" at 240px. Three lines per alert row; no scroll
within the MDA panel for the top 1–3 alerts.

At 400px column width (1280×800), the full-density format from ADR-008 Decision 5 applies:
all four fields untruncated on separate lines.

**Right column vertical stacking order (1B / 1C / 1D):**

MDA alert panel (1B) is the highest-priority co-primary instrument — severity ordering governs
arrangement, not framework ordering (UX-F1 from ADR-008 panel review). Vertical order top to
bottom:

1. **1B — MDA Alert Panel** (~45% of column height) — top position, largest allocation
2. **1C — PMM Widget** (~25% of column height) — middle position
3. **1D — Four-Framework Current Position** (~30% of column height) — bottom position

At 640px usable height (1024×768): 1B ≈ 290px, 1C ≈ 160px, 1D ≈ 190px.
At 720px usable height (1280×800): 1B ≈ 324px, 1C ≈ 180px, 1D ≈ 216px.

The three co-primary instruments must be simultaneously scannable — no instrument is below the
fold at either supported viewport.

### Control Plane Zone — 280px Reserved (FA-C3 Resolution)

**EL ruling (2026-05-22, FA-C3 disposition):** Option A — stacked forms, ~280px reserved zone.
"Simultaneously visible" means both form headers visible without scroll, not all form fields.

The 280px zone is reserved from M9 onward as a persistent layout column adjacent to the
instrument cluster. In Mode 1 and Mode 2, the zone is empty whitespace — it is not collapsed,
hidden, or filled with other content. In Mode 3, the zone is populated with:

- Policy instruments form (blue visual treatment)
- Scenario shocks form (orange visual treatment)

Both form **headers** are visible without scroll at ~800px usable height. Form fields scroll
within the 280px column. The stacked arrangement (policy instruments above, shocks below)
preserves the blue/orange visual separation required by ADR-008 Decision 12.

**Implementation:** The 280px column is a persistent CSS grid column, always rendered.
A CSS class `mode-3-active` populates it with form content. In Mode 1 and Mode 2, the column
renders empty (`aria-hidden="true"` is not appropriate here — the reserved zone is a legitimate
layout element, not decorative). A subtle label "Control plane (Mode 3)" is acceptable as a
placeholder at Mode 1/Mode 2 entry state, but must not be visually prominent.

---

## Shared State Architecture

### Decision: Zustand Atom at Scenario View Level (FA-C2 Resolution)

**Design decision recorded here; must be copied to `docs/frontend/design-decisions.md`
as DD-012 before the first implementation PR is opened.**

All four Zone 1 instruments derive from a single Zustand store atom scoped to the active
scenario session. This is the implementation of the atomicity requirement in ADR-008 Decision 14
and ADR-010 Decision 4.

**Why Zustand over `useState` at top-level component:**

React's `useState` at a top-level component passes state as props to all four Zone 1 instruments.
This works mechanically, but introduces prop-drilling through component tree layers if the
instrument components are not direct children of the scenario view. Zustand's hook-based
subscription allows each Zone 1 instrument to subscribe to the shared atom directly without
prop-drilling — while still deriving from the same state update and batching within the same
React render cycle.

**Why not `useQuery` per instrument:**

Independent `useQuery` hooks per instrument cannot guarantee simultaneous re-renders. Even with
React Query's shared cache, two components subscribed to the same query key may re-render in
separate cycles depending on their position in the tree. ADR-010 Decision 4 Alternative 2
documents this explicitly. The shared Zustand atom updated in a single `set()` call, combined
with React 18 automatic batching, is the mechanically correct approach.

**State atom shape (from ADR-010 Decision 4):**

```typescript
interface ScenarioStepState {
  scenario_id: string;
  current_step: number;
  step_count: number;
  trajectory: TrajectoryResponse | null;
  baseline_trajectory: TrajectoryResponse | null;
  computation_state: "idle" | "computing" | "complete";
  mode: "MODE_1" | "MODE_2" | "MODE_3";
}
```

**Atomicity enforcement:** All four Zone 1 instruments call `useScenarioStepStore()` to subscribe
to this atom. The store is updated with a single `set()` call — never field by field across
multiple `set()` calls. Any pattern that calls `set({ current_step: N })` in one event handler
and `set({ trajectory: newData })` in a separate event handler is a violation of the atomicity
contract.

**Computation state propagation (Mode 3):**

`computation_state` transitions `idle → computing → complete` in a single `set()` call when a
control input is applied. The `complete` transition carries the new `trajectory` data in the
same `set()` call — the instruments receive the new data and the `complete` state in one update.
Stale data flash is structurally prevented: the instruments never see `complete` without the
new trajectory data.

**Baseline freezing (Mode 3):**

On the first applied control input: copy the current `trajectory` to `baseline_trajectory` in
the same `set()` call that initiates the computation. Subsequent `trajectory` updates reflect
the active (modified) trajectory. `baseline_trajectory` is never updated again for the session
unless the user explicitly resets (a future Mode 3 capability, not in M9 scope).

---

## Performance Acceptance Criteria (FA-R1 Resolution)

**Named acceptance criterion (required in this brief per FA-R1):**

Render time at initial load and on step navigation must not exceed 100ms, measured on a 4-core
machine at the full Mode 3 component activation state.

**Component set at full Mode 3 activation (worst-case SVG DOM):**

| Component type | Count |
|---|---|
| `<Line>` — active curves | 4 |
| `<Line>` — baseline ghost curves | 4 |
| `<Area>` — divergence fills | 4 |
| `<ReferenceLine>` — MDA floors (estimated) | 8 (2 per framework at WARNING/CRITICAL) |
| `<ReferenceLine>` — shock events (estimated) | 3 |
| `<Dot>` — policy inflection markers (estimated) | 6 |

**Measurement approach:**

Use `performance.measure("trajectory-render-start", "trajectory-render-end")` wrapping the
Zustand `set()` call that triggers the trajectory update and the subsequent React re-render
completion (measured via `useLayoutEffect` in the TrajectoryView component). Playwright test
runs this at the worst-case component configuration.

**If 100ms is not met:** Before any optimization, validate that the component configuration
matches the worst-case spec above — extra Line or ReferenceLine components are a first-order
suspect. If the spec is met and performance still fails, surface the constraint to the
Engineering Lead — a Canvas fallback for Mode 3 only is the escalation path (requires ADR-010
amendment, not a brief decision).

---

## Divergence Fill Implementation (FA-R2 Resolution)

**Selected approach: merged data key strategy with `<Area>` component**

**Decision:** Merge baseline and active trajectory arrays by `step_index` before rendering.
Each step entry in the merged data array has two composite score keys per framework:
`{framework}_active` and `{framework}_baseline`. The `<Area>` component renders between these
two keys.

```typescript
// Merged data shape for one step
interface MergedStepDatum {
  step_index: number;
  financial_active: number | null;
  financial_baseline: number | null;
  human_development_active: number | null;
  human_development_baseline: number | null;
  ecological_active: number | null;
  ecological_baseline: number | null;
  governance_active: number | null;
  governance_baseline: number | null;
}
```

**Why this over `<defs>` + `<clipPath>`:**

The clipPath approach clips the active curve's area fill using the baseline curve as the clip
boundary. It requires generating SVG path strings manually from the data, and the clipping
behavior when active and baseline re-converge requires careful path management. The `<Area>`
with merged data keys stays within Recharts' component model — the library handles path
generation, and the fill naturally disappears when both keys share the same value (delta = 0).

**Step count mismatch handling:**

If the active trajectory has computed 4 of 6 steps and the baseline has 6 steps, steps 5 and 6
in the merged array have `{framework}_active: null` and `{framework}_baseline: <value>`. The
`<Area>` renders fill only where both keys are non-null and have a delta > 0.01. No special
handling is needed — the null propagates through Recharts' data handling as a gap in the
Area path.

**Proof-of-concept requirement before committing to this approach:** Before the first Mode 3
implementation PR is opened, a standalone Recharts sandbox must validate the merged key approach
renders correctly at: (a) full 8-curve configuration, (b) re-convergence case (fill disappears),
(c) step count mismatch case (partial active trajectory). The proof-of-concept must be committed
to `frontend/sandbox/trajectory-divergence-poc.tsx` and referenced in the PR.

---

## Mode 1 Step Axis Annotation (FA-C5 and UD-R2 Resolution)

### Character-Count Constraint (FA-C5 Resolution)

**Validation at 480px trajectory view width with 6 steps:**

Each step marker has **480 / 6 = 80px** horizontal space.

Three lines stacked (from ADR-010 Decision 7):
1. Step index: "Step 6" — ~36px at 11px font, 6.0px/char
2. Calendar date: "Dec 2001" — ~48px at 11px font — within 80px ✓
3. Event label: wraps at 80px max width, 2 lines max

Event label character validation: the ≤ 8-word constraint alone is insufficient — "Structural
adjustment programme second phase begins announced" is 8 words but ~54 chars wide (~324px at
6px/char), requiring 4 lines at 80px width. This violates legibility.

**Binding constraint (FA decision, recorded here and in design-decisions.md DD-012):**

```
Event label: ≤ 8 words AND ≤ 32 characters (including spaces)
```

At 11px font / 6px average char width: 32 chars = ~192px, which wraps into 2–3 lines at 80px
max width. Two lines is the design target; 3 lines is the permitted maximum before the tick
cell degrades. The fixture CI gate enforces both constraints at schema validation time.

**Fixture CI gate (binding):** Any Mode 1 scenario fixture with a SIGNIFICANT step whose
`step_event_label` exceeds 8 words OR 32 characters must fail CI. The gate is a schema
validation step, not a render-time check. Implementation: a pytest schema validator that
checks every fixture JSON file, located in `tests/fixtures/` and run as part of the standard
`pytest tests/fixtures/` suite on every PR (QA-F6).

### Multi-Case Mode 1 Tick Format (UD-R2 Resolution — UX Designer Ruling)

**UX Designer ruling (UD-R2, 2026-05-22):** When two historical entities are compared in
Mode 1 on the same step axis, each tick must display **both** entities' calendar dates —
stacked, not optional. The ADR-010 Decision 7 text read "may appear" — this ruling changes it
to "must appear."

**Implementation:**

In multi-case Mode 1 (two entities, aligned by programme step), the custom XAxis tick renders:

```
Step 1
ARG: Mar 2001
ICE: Feb 2008
Deposit freeze
announced
```

Field order: step index → entity A date → entity B date → event label (SIGNIFICANT steps only).
Each date line is prefixed with the entity ISO 3166-1 alpha-3 code (3 chars + colon + space =
5 chars overhead). At 80px tick width this remains within 2-line wrap for date lines.

The entity code is the three-letter ISO code from the scenario fixture — it is not a
user-configurable label. If a multi-case scenario has entities with very long names, the ISO
code provides a compact but unambiguous identifier in the constrained tick space.

**When both entities share the same calendar date at a step** (rare but possible): merge to a
single date line: "MMM YYYY (both)".

---

## Framework Colors

### CVD Validation Procedure (FA-R4 Resolution)

**Required before any implementation PR introduces framework colors into code.**

**Provisional hex values (from ADR-010 Decision 3):**

| Framework | Hex |
|---|---|
| Financial | `#2D6A8B` |
| Human Development | `#C67C2E` |
| Ecological | `#3A7A4B` |
| Governance | `#5C4A8A` |

These are provisional — no CVD simulation has been run. The UX Designer holds authority over
the specific hex values (ADR-010 Decision 3, incorporating UD-R1). The FA brief's responsibility
is to run the validation and surface the result.

**Validation procedure:**

1. Use Color Oracle (free, macOS/Windows) or the Figma accessibility plugin (Able or Stark)
2. Run all four framework colors through deuteranopia simulation
3. Run all four framework colors through protanopia simulation
4. Test distinguishability of each framework color against:
   - The other three framework colors (4×3 = 12 pairs)
   - Policy input blue (`#1A6BAF`) — must be distinguishable from all frameworks
   - Shock orange (`#C45C00`) — must be distinguishable from all frameworks
5. Minimum distinguishability threshold: any two colors that appear more similar than 20% ΔE
   (CIELAB) under simulated CVD fail

**Outcomes:**

- **All pairs pass:** Provisional hex values become canonical. UX Designer confirms in writing.
  Colors are committed to `frontend/src/constants/frameworkColors.ts`.
- **Any pair fails:** FA documents which pair failed and under which CVD type. UX Designer
  issues revised hex values satisfying the criteria. No ADR amendment required — the ADR
  commits to the criteria, not the specific values (ADR-010 Decision 3). Revised values go
  directly into `frameworkColors.ts` with UX Designer written ruling in the PR description.

**Timeline:** CVD validation must be completed and the outcome recorded in this brief
(§CVD Validation Result, below) before the TrajectoryView component is implemented. Framework
colors must not appear in code with a "TODO: validate" comment — they are implemented once, as
the validated values.

### UX Designer Authority Confirmation

The UX Designer holds authority over the specific hex values for all four framework colors.
This authority extends to:
- Revising any hex value after CVD validation without requiring an ADR amendment
- Issuing revised values for any subsequent milestone if accessibility standards change
- Overriding provisional values with no requirement to justify the revision against the
  Architect's proposed alternatives

A UX Designer ruling on framework colors is implemented by the FA Agent without further review.
The ruling must be written (this brief, design-decisions.md, or a GitHub issue comment) and
referenced in the implementing PR.

### CVD Validation Result

*To be completed by the Frontend Architect Agent before TrajectoryView implementation.*

**Date:** ___________
**Tool used:** ___________
**Outcome:** ☐ All pairs pass — provisional values confirmed ☐ Revision required

**If revision required:**

| Framework | Original hex | Revised hex | UX Designer ruling reference |
|---|---|---|---|
| | | | |

**UX Designer sign-off on final colors:** ___________

---

## Confidence Tier Visual

### Curve-Face Badge for Tier 4-5 (UD-R3 Resolution — UX Designer Ruling)

**UX Designer ruling (UD-R3, 2026-05-22):** ADR-010 Decision 10 places the confidence badge
only in the Recharts Legend. In Mode 3, the user's focus is on the chart body — a Tier 4-5
curve activating during real-time steering must carry a badge visible on the curve face, not
only in the legend.

**Implementation:**

For each Tier 4-5 framework curve, render a small SVG `<text>` element positioned adjacent to
the most recent data point on the curve:

```
Text content: "(exp)"
Position: 4px to the right of the rightmost non-null data point
Font size: 11px minimum (UX Designer ruling UD-F2 — informational text, not decorative)
Color: framework color at 80% opacity (matches the curve's strokeOpacity=0.60 tier treatment)
Visibility: only when confidence_tier ∈ {4, 5} for the framework's most recent step
```

This is a custom SVG element rendered inside the `<ComposedChart>` via Recharts' `customized`
prop or a positioned `<text>` in the chart's SVG namespace. It is **not** the legend badge —
it is an additional label on the chart face.

**When no data point exists at the final step** (partial computation): the badge renders
adjacent to the rightmost available data point, not at the step axis end.

**In Mode 1:** The badge appears at the final step of the historical trajectory (the last
computed step in the fixture). It is static in Mode 1 — it does not update during step
navigation.

### Deferral Placeholder in Legend (ADR-010 Decision 10)

During the ADR-007 deferral period, Tier 3-5 curves display in the Recharts Legend:

```
"[Framework name] (exploratory — band pending)"    // Tier 4-5
"[Framework name] (moderate — band pending)"       // Tier 3
```

This placeholder is **in addition to** the `"(exp)"` curve-face badge for Tier 4-5 — they serve
different purposes: the legend placeholder explains the missing band; the curve-face badge
communicates tier during active steering.

When ADR-007 is accepted and the BandingEngine populates non-null `ci_lower`/`ci_upper` values
in the trajectory response, the `"— band pending"` suffix is removed from the legend label
automatically. No code change is required at that point — the label is conditional on
`ci_lower === null`.

---

## Uncertainty Band Infrastructure (FA-C4 Resolution)

### ADR-006 Band Schedule

The uncertainty band infrastructure is built to accept ADR-007's Tier 3-5 width constants.
The base band schedule from ADR-006 Decision 1 is:

| Horizon | Pre-calibration band width |
|---|---|
| 1 year | ±10% |
| 3–5 years | ±35% |

These are the Tier 1-2 (MEASURED) band widths. ADR-007 will define Tier 3, 4, and 5 multipliers
that widen the bands for synthetic data (e.g., Tier 3 ×1.5, Tier 4 ×2.5, Tier 5 ×3.0 — these
are not yet defined; the multipliers are ADR-007's domain).

**What the FA brief commits to:**

The `<Area>` component rendering bands is built and mounted in Mode 1 and Mode 2 for all
frameworks. It is parameterized to accept `ci_lower` and `ci_upper` fields from the
`FrameworkCurvePoint` (ADR-010 Decision 2 data contract). Until the BandingEngine populates
these fields (pending ADR-007), the Area renders nothing — `ci_lower === null` gates rendering.

**Implementation shape:**

```typescript
// In TrajectoryView: one <Area> per framework, always mounted
<Area
  dataKey={`${framework}_ci_upper`}
  baseLine={`${framework}_ci_lower`}
  fillOpacity={ci_lower_for_framework !== null ? 0.08 : 0}
  stroke="none"
  fill={FRAMEWORK_COLORS[framework]}
  isAnimationActive={false}
/>
```

The `fillOpacity` conditional means no visual output until ADR-007 is accepted. The Area
component is in the DOM — there is no "ADR-007 accepted" code path that wires it up. The
BandingEngine delivering non-null `ci_lower` and `ci_upper` is the only activation event
required.

**No frontend change is required at ADR-007 acceptance.** This is the correct implementation of
"ADR-007-gated band infrastructure" (ADR-010 Decision 10).

---

## Governance Null Curve Rendering

The governance `<Line>` component must have `connectNulls={false}`. This is not configurable —
it is a hard requirement derived from ADR-010 Decision 5.

**Implementation guard:** A unit test must assert that the governance `<Line>` rendered by
TrajectoryView has `connectNulls={false}` regardless of the data passed. This test must not
be conditional on the scenario having null governance values — it validates the component
configuration, not the data.

The test assertion:

```typescript
const governanceLine = screen.getByTestId("trajectory-line-governance");
expect(governanceLine).toHaveAttribute("connectNulls", "false"); // or equivalent prop assertion
```

---

## Design Decisions Required in `design-decisions.md`

Before any implementation PR is opened, the following entries must be added to
`docs/frontend/design-decisions.md`:

**DD-012 — Shared State Management: Zustand Atom for Zone 1 Instrument Atomicity**

Record the rationale documented in §Shared State Architecture above. Key content: why Zustand
over `useState`, why not `useQuery` per instrument, and the invariant: all four Zone 1
instruments update from a single `set()` call in the same React render cycle.

**DD-013 — Divergence Fill: Merged Key `<Area>` Approach**

Record the decision and proof-of-concept requirement documented in §Divergence Fill
Implementation above. Reference the proof-of-concept file path.

**DD-014 — Step Annotation Character Constraint: ≤ 8 Words AND ≤ 32 Characters**

Record the validation and rationale from §Mode 1 Step Axis Annotation. The 480px trajectory
view width and 6-step scenario are the worst-case parameters that govern this constraint.

**DD-015 — Control Plane Zone: 280px Stacked Forms (EL Ruling)**

Record the EL ruling reference (ADR-008 panel review FA-C3, 2026-05-22) and confirm the
trajectory view width satisfies the remaining space (480px at 1024×768, 580px at 1280×800).

---

## UX Designer Sign-Off Required

Per RACI Row 3 (UX component decisions: UX Designer R) and the standing consultation
obligation ("Before a brief is produced, bring me the proposed component structure" —
`agents.md §UX Designer — Working Agreement`), this brief requires UX Designer sign-off before
implementation begins.

**Specific items requiring UX Designer confirmation:**

1. Zone 1 two-column layout (480px trajectory + 240px co-primary at 1024×768) — confirm the
   240px right column satisfies simultaneous scannability with the compact row format (UD-F1)
2. Right column vertical stacking order (1B → 1C → 1D, top to bottom) — confirm MDA primacy
3. MDA compact row format at 240px (UD-F1 ruling above) — confirm the 3-line compact spec
4. CVD validation outcome — confirm framework colors once validation is complete (MV-001)
5. Curve-face `"(exp)"` badge — confirm 11px font size (UD-F2) and 4px right-of-datapoint
   placement at minimum trajectory view width

**UX Designer sign-off:**

*UX Designer Agent: REVIEW — 2026-05-22. Documents read: `information-hierarchy.md` Zone 1,
`agents.md` authority boundaries.*

**Sign-off date:** 2026-05-22
**Confirmed items:** ☑ Zone 1 layout ☑ Right column stacking ☑ Compact alert row format (UD-F1) ☐ Framework colors (conditional — pending MV-001 CVD result) ☑ Badge font 11px (UD-F2) ☑ Badge positioning (conditional — FA Agent must verify no SVG clip at 480px; may offset above-left if right placement clips)

**Ruling on each item:**

1. **Zone 1 two-column layout (480px / 240px at 1024×768) — Confirmed.** 480px is sufficient
   for legible four-curve trajectory comparison. The UD-F1 compact row format satisfies
   information-hierarchy.md 1B requirements at 240px: severity, framework source, indicator
   name (truncated), step + cohort all visible without expansion.

2. **Right column stacking (1B → 1C → 1D) — Confirmed.** MDA alerts at top: threshold safety
   signal is the highest-priority co-primary read in all three modes, most critical in Mode 3.
   PMM above four-framework current position: margin status is a higher cognitive priority than
   the absolute value readout.

3. **Compact alert row format at 240px (UD-F1) — Confirmed.** Line 1 (severity pill +
   abbreviation + framework source) satisfies the information-hierarchy.md requirement that
   framework source be visible per alert without a tab. Ruling stands as issued in the
   three-agent review.

4. **Framework colors — Conditional sign-off.** Cannot confirm specific hex values until MV-001
   CVD validation result is reported. Once the FA Agent completes CVD validation, I will issue
   a color ruling within the same session: either (a) confirm provisional values, or (b) issue
   revised hex values satisfying the ADR-010 Decision 3 criteria. Implementation must not
   proceed with framework colors in code until this ruling is recorded in this section.

5. **"(exp)" badge, 11px font, placement — Confirmed with condition.** 11px minimum confirmed
   (UD-F2). Placement: FA Agent must verify the `<text>` element is not clipped at 480px
   trajectory width before committing the implementation. If right-of-datapoint placement clips,
   offset above-left instead. What matters: badge visible on the curve face during Mode 3
   steering. The precise direction of offset is FA authority.

**Additional ruling — Control plane zone placeholder text:** The "Control plane (Mode 3)"
label in the reserved zone during Mode 1/2 is confirmed as acceptable, with one styling
requirement added: ≤ 11px font, ≤ 30% opacity, non-interactive. It must read as a system
annotation, not a navigation affordance. No button treatment, no collapse indicator, no chevron.

**Pending:** UX Designer color ruling after MV-001 completion. FA Agent to return CVD result
to this section; UX Designer will update item 4 in the same PR that records the result.

---

## Implementation Sequencing

The following sequencing ensures no blocking dependency is encountered mid-implementation.

**Pre-implementation (before first PR) — blocking gates:**

0. **UX Designer sign-off** (MV-003) — sign-off section completed in this document; no
   implementation PR may open until this is recorded
1. Complete CVD validation for framework colors; record result in §CVD Validation Result
2. Add DD-012 through DD-015 to `docs/frontend/design-decisions.md`
4. Build and validate divergence fill proof-of-concept at `frontend/sandbox/trajectory-divergence-poc.tsx`
5. Update `docs/schema/api_contracts.yml` with `GET /scenarios/{id}/trajectory` endpoint

**Backend prerequisite (blocks frontend trajectory data):**

- `GET /scenarios/{id}/trajectory` endpoint implemented with `TrajectoryResponse` shape
- Dense array contract: only computed steps returned; null `composite_score` means governance-in-validation
- `MDAFloor.floor_value` is composite-score-level (not indicator-level projection)

**Implementation order:**

1. Shared Zustand atom (`useScenarioStepStore`) + acceptance test for atomic updates (AC-006)
2. TrajectoryView shell: ComposedChart with four `<Line>` components, Mode 1 custom XAxis tick
3. Mode 1 step annotation validation tests (AC-011, AC-012) and Greece fixture audit
4. Zone 1 layout: two-column at 1024×768 and 1280×800, control plane zone reservation
5. Acceptance tests AC-001 through AC-005, AC-015
6. Mode 3 additions: ghost curves, divergence fill, policy/shock markers
7. Performance validation at Mode 3 full component set (AC-007, AC-008, AC-009)
8. Confidence tier visual: opacity + dashed curves + curve-face badge + legend placeholder
9. Uncertainty band `<Area>` infrastructure (ADR-007-gated, zero visible output)
10. Full Playwright screenshot suite at both supported viewports

---

## Appendix — Brief Completeness Checklist

| Deferred item | Brief section | Status |
|---|---|---|
| FA-C1: Zone 1 layout at 1024×768 | §Layout and Viewport | ✓ Named constants: 480/240/280; compact alert format (UD-F1) |
| FA-C2: State management design decision | §Shared State Architecture | ✓ Zustand atom; DD-012 required |
| FA-C3: Control plane zone width | §Layout and Viewport | ✓ 280px confirmed (EL ruling) |
| FA-C4: Bands linked to ADR-006 | §Uncertainty Band Infrastructure | ✓ Base schedule cited; Tier 3-5 multipliers ADR-007-gated |
| FA-C5: Step annotation at 1024px | §Mode 1 Step Axis Annotation | ✓ 32-char constraint; 80px tick cell validated |
| FA-R1: ComposedChart performance | §Performance Acceptance Criteria | ✓ ≤ 100ms CI gate; hardware validation MV-002 |
| FA-R2: Divergence fill approach | §Divergence Fill Implementation | ✓ Merged key `<Area>`; POC required |
| FA-R4/UD-R1: CVD validation | §Framework Colors | ✓ Procedure specified; result pending (MV-001) |
| FA-R5: Named trajectory view dimensions | §Layout and Viewport | ✓ AC-003/004/005 |
| UD-R2: Multi-case tick format | §Mode 1 Step Axis Annotation | ✓ Stacked dates; must appear |
| UD-R3: Curve-face badge | §Confidence Tier Visual | ✓ "(exp)" at rightmost data point; 11px min (UD-F2) |

## Appendix — Architect Agent Review of Data Architect Findings

Architect Agent: REVIEW — 2026-05-22. Documents read: ADR-010 Decisions 2, 5, 6, 7;
RACI Row 4 (data/schema decisions); FA brief §Data Architect Review Findings; ADR-006 Decision 2.

**Scope:** Disposition of DA-F1 through DA-F5; identification of further agent involvement
required; proposed remedies. The Architect holds C on data/schema decisions (RACI Row 4);
EL is A on all decisions that require scope change or methodology input.

---

### Arch-F1 — Terminology Discrepancy: "STANDARD" vs. "ROUTINE" (Blocking Correction)

Before any other finding: the FA brief uses `step_significance: "SIGNIFICANT" | "STANDARD"`
throughout (§Mode 1 Step Axis Annotation, §Named Acceptance Criteria AC-012). ADR-010
Decision 7 defines `step_significance: "SIGNIFICANT" | "ROUTINE"`. The ADR is authoritative.
"STANDARD" and "ROUTINE" are not equivalent — the fixture CI gate will enforce whichever
term is in the schema validator. Using the wrong term means either valid fixtures fail CI,
or invalid fixtures pass CI silently.

**Required correction:** All instances of `"STANDARD"` in the FA brief's step_significance
context must be changed to `"ROUTINE"` before the fixture CI gate is implemented. This is
a brief error, not an ADR discrepancy.

**No EL decision required.** Applied below in this same PR.

---

### DA-F1 — Trajectory Endpoint Absent from api_contracts.yml

**Architect disposition: ADEQUATE AS STUB.** The partial stub added by the Data Architect is
the correct interim state. The full endpoint specification is defined in ADR-010 Decision 2 —
the stub is incomplete only because DA-F2, DA-F4, and DA-F5 are unresolved. The stub serves
its purpose: it registers the endpoint so no implementation agent can call it without a schema
contract.

**No further agent involvement required for DA-F1 itself.** The stub completes when the three
blocking findings are resolved. At that point, the Data Architect updates `api_contracts.yml`
in the same PR that implements the backend endpoint.

---

### DA-F2 — No Composite-Score-Level MDA Floor Storage

**Architect disposition: DEFER MDA FLOOR OVERLAYS TO M10, WITH CM CONSULTATION REQUIRED.**

The root issue is methodological, not merely a schema gap. Composite-score-level MDA floors
cannot be mechanically derived from indicator-level floors (CM-R3 rules this out; ADR-010
Decision 6 records the ruling). They must be independently defined at the composite score
level. Who defines them, and how, is a Chief Methodologist question — not an Architect
question and not an EL decision alone.

**What the Architect recommends:**

1. **Activate Chief Methodologist** — with the following question: "Can composite-score-level
   MDA floors be defined for the four measurement frameworks, and if so, by what methodology?
   The trajectory view Y-axis is the composite score [0.0, 1.0] for financial and
   human_development, [0.0, 2.0] for ecological, and [0.0, 1.0] for governance. What
   composite score values constitute WARNING / CRITICAL / TERMINAL floor levels per framework?"
   This is a methodology question; the Chief Methodologist's output is the input to the
   schema and ADR-010 amendment.

2. **Pending CM consultation: defer MDA floor overlays in M9.** The trajectory view ships
   without `<ReferenceLine>` floor lines. Zone 1B MDA alerts fire correctly (indicator-level,
   which is the right place for them per Decision 6's Zone 1B relationship). The trajectory
   view is not silent about MDA state — Zone 1B carries it. What is deferred is the
   floor-line visual overlay on the trajectory curves.

3. **M10 entry gate:** CM methodology answer + schema design (new column on `mda_thresholds`,
   or a new `mda_composite_floors` table, determined after CM output) + ADR-010 amendment to
   Decision 6 recording the concrete floor values and storage approach.

**ADR-010 amendment required:** If MDA floor overlays are deferred, Decision 6's implementation
is partially suspended. An ADR-010 amendment is not required for the deferral itself — the ADR
permits the trajectory view to not render floor lines during the M9 implementation phase. But
when composite-score-level floors are defined and implemented in M10, a Decision 6 amendment is
required to add the concrete `floor_value` semantics and source schema.

**EL decision required:** Authorize the CM consultation and confirm the M9 deferral of MDA
floor overlays as the implementation path.

**Agent involvement:** Chief Methodologist (consultation on composite-score floor methodology).
EL (decision to defer + authorize CM activation).

---

### DA-F3 — ci_lower / ci_upper Absent from Schema Files

**Architect disposition: CORRECT AS-IS. No action until ADR-007.**

The partial stub correctly registers these as pending-ADR-007 fields. Note for completeness:
ADR-006 Decision 2 defines the BandedOutput contract (`ci_lower`, `ci_upper`, `ci_coverage`,
`is_pre_calibration`, `clipped_lower`, `clipped_upper`). When the Data Architect updates
`api_contracts.yml` at ADR-007 acceptance, they must reference ADR-006 Decision 2 as the
authority for field names and types — do not derive them from the FA brief's `<Area>`
component shape.

The `fillOpacity` conditional in the brief (`ci_lower !== null ? 0.08 : 0`) is the correct
zero-output guard. The infrastructure is in place; there is nothing to implement here in M9.

**No further agent involvement required.**

---

### DA-F4 — Single-Entity Null Handling: Mode 1 Greece Trajectory View Blocked

**Architect disposition: CRITICAL GAP. Chief Methodologist consultation required. EL decision
required. This finding has the highest severity of the five.**

**The core problem:** ADR-010 Decision 2 defines `composite_score: null` as meaning
"governance-in-validation only." But the existing composite score computation returns null for
financial and human_development in single-entity scenarios (Issue #193 — percentile rank
requires ≥2 entities). The Greece fixture is a single-entity scenario. The trajectory view for
Mode 1 Greece would render one curve (ecological, which is boundary-proximity-based and exempt
from the single-entity null rule per ADR-005 Amendment 3 Decision M8-2). Financial and
human_development would be empty. Governance would be null for a different reason (in-validation).

A trajectory view with one meaningful curve is not the "multi-framework trajectory comparison
legible at a glance" that ADR-008 defines as the Zone 1A requirement. This is a demo-breaking
gap, not a corner case.

**What the Architect recommends:**

The trajectory endpoint must use a **different composite score methodology for single-entity
scenarios** — one that produces non-null financial and human_development values without
requiring a comparison entity. The percentile rank approach is correct for multi-entity
comparison; it is wrong for single-entity trajectory display, where the meaningful question
is not "how does this entity rank?" but "how does this entity's own trajectory evolve over
time?"

A normalized absolute value composite — averaging normalized indicator values within each
framework using the same normalization scales used for percentile rank computation — is the
leading candidate. This is a methodological decision that the Chief Methodologist must approve.

**What the Architect does NOT recommend:** Changing the measurement-output endpoint to return
non-null single-entity scores. That endpoint's null behavior is documented, and changing it
would break the single_entity_warning contract. The trajectory endpoint is a new endpoint
whose data contract is not yet fully established — the right place to resolve this.

**Required ADR-010 amendment:** Decision 2 must be amended to define the trajectory endpoint's
composite score computation methodology for single-entity scenarios, including:
- What scoring approach is used (pending CM approval)
- That `single_entity_warning` is NOT propagated to the trajectory response (the trajectory
  response has no `single_entity_warning` field — it has curves or it does not)
- That null financial/HD composite_score on the trajectory endpoint means something different
  than null financial/HD on the measurement-output endpoint — the disambiguation must be
  documented explicitly

**Agent involvement required:**
1. **Chief Methodologist** — methodology consultation on single-entity composite score for
   trajectory view. Question: "What composite scoring approach is appropriate for single-entity
   Mode 1 trajectory display, where percentile rank requires N≥2 entities? The goal is a
   meaningful [0.0, 1.0] score that tracks a single entity's trajectory over time."
2. **EL** — decision to authorize CM consultation; confirm ADR-010 amendment scope.
3. **Architect Agent** — amend ADR-010 Decision 2 after CM output.

**Until this is resolved, Mode 1 trajectory view for single-entity scenarios is not
implementable per the current ADR-010 contract.** Recommend filing a GitHub issue to track
this (updating Issue #193 with "trajectory view dependency" label or filing a new issue).

---

### DA-F5 — step_event_label / step_significance Have No Schema Home

**Architect disposition: RECOMMEND OPTION (a) — scenario configuration JSONB extension.
EL confirmation required (minor). ADR-010 Decision 2 must record the storage approach.**

The fields are already specified in ADR-010 Decision 2's `TrajectoryStep` interface. The gap
is purely storage: where does the backend read `step_event_label` and `step_significance` from?

**Architect recommendation: add a `step_metadata` key to `scenarios.configuration` JSONB.**

Schema extension (no migration required — JSONB):

```json
"step_metadata": {
  "1": {
    "step_event_label": "Deposit freeze announced",
    "step_significance": "SIGNIFICANT"
  },
  "3": {
    "step_event_label": "Troika agreement signed",
    "step_significance": "SIGNIFICANT"
  }
}
```

- Keys are 1-based step index strings (matching `TrajectoryStep.step_index`)
- Entries are absent for ROUTINE steps (not `"step_significance": "ROUTINE"` — absence implies ROUTINE)
- The trajectory endpoint reads `scenarios.configuration->'step_metadata'->step_index::text`
  to populate `step_event_label` and `step_significance` on each `TrajectoryStep`
- The fixture CI gate validates `step_event_label` against the ≤ 8 words AND ≤ 32 characters
  constraint on every fixture JSON file — the JSONB path is predictable

**Why option (a) over (b) (new table):** Step annotations are scenario-configuration data,
not operational data. They are authored once at fixture creation, never updated during
simulation execution, and always read together with the scenario. JSONB embedding is the
correct storage pattern for infrequently-updated configuration data. A dedicated table would
be appropriate if step annotations were queried independently of their scenario or if they
needed separate write access — neither applies here.

**ADR-010 Decision 2 amendment required:** Add the storage contract for `step_event_label`
and `step_significance` — `scenarios.configuration.step_metadata` JSONB key, keyed by
step_index string. This is a minor clarification amendment, not a decision reversal.

**api_contracts.yml update required:** The POST /scenarios request body schema must document
`step_metadata` as an optional key in `configuration`. The Data Architect adds this when the
feature is implemented.

**Terminology correction** (Arch-F1 resolution): change `step_significance` value from
`"STANDARD"` → `"ROUTINE"` throughout the FA brief, consistent with ADR-010 Decision 7.

**Agent involvement:** None beyond EL confirmation of option (a). Architect amends ADR-010
Decision 2 in the same PR as EL confirmation.

---

### Summary — Architect Recommended Actions

| Finding | Disposition | EL Decision Required? | Agent consultation required | ADR change? |
|---|---|---|---|---|
| Arch-F1 | CORRECT — "STANDARD" → "ROUTINE" in FA brief | No | None | No — brief correction |
| DA-F1 | ADEQUATE AS STUB — completes when blockers resolved | No | None | No |
| DA-F2 | DEFER overlays to M10; CM consultation on composite-score floor methodology | Yes — authorize CM + deferral | Chief Methodologist | Yes — ADR-010 Decision 6 amendment at M10 |
| DA-F3 | CORRECT AS-IS — pending ADR-007 | No | None | No |
| DA-F4 | CRITICAL — CM consultation on single-entity trajectory scoring; ADR-010 Decision 2 amendment required | Yes — authorize CM + amendment scope | Chief Methodologist (primary), then Architect (amendment) | Yes — ADR-010 Decision 2 amendment |
| DA-F5 | RECOMMEND option (a): `step_metadata` JSONB in `scenarios.configuration`; no migration | Yes — confirm option | None | Yes — ADR-010 Decision 2 minor amendment |

**Immediate actions (before any trajectory view implementation):**

1. **EL decision on DA-F2:** Authorize deferral of MDA floor overlays + Chief Methodologist
   consultation on composite-score floor methodology
2. **EL decision on DA-F4:** Authorize Chief Methodologist consultation on single-entity
   trajectory scoring; confirm ADR-010 Decision 2 amendment is required
3. **EL decision on DA-F5:** Confirm option (a) for step annotation storage
4. **Correct Arch-F1:** Apply "STANDARD" → "ROUTINE" throughout FA brief (applied below)
5. **File / update GitHub issue for DA-F4:** Update Issue #193 with trajectory view
   dependency, or file a new issue. DA-F4 is a demo blocker, not a near-term horizon item.

**No trajectory endpoint implementation may begin until DA-F2, DA-F4, and DA-F5
dispositions are confirmed by the EL.**

---

## Appendix — Data Architect Review Findings

Data Architect Agent: REVIEW — 2026-05-22. Schema files read: `api_contracts.yml` v1.0,
`database.yml` v1.1, `simulation_state.yml` v1.0.

**Five findings. Three require EL decisions before the trajectory endpoint can be implemented.**

| ID | Finding | Severity | Status |
|---|---|---|---|
| DA-F1 | `GET /scenarios/{id}/trajectory` absent from `api_contracts.yml` | Schema gap | Partial stub added 2026-05-22 — full spec blocked by DA-F2 and DA-F4 |
| DA-F2 | No composite-score-level MDA floor storage in current schema | Blocking — EL decision required | Pending |
| DA-F3 | `ci_lower`/`ci_upper` absent from all schema files | Schema gap | Registered as pending-ADR-007 in stub — no action required until ADR-007 |
| DA-F4 | Single-entity null handling for financial/human_development undefined | Blocking — EL decision required | Pending |
| DA-F5 | `step_event_label`/`step_significance` have no schema home | Blocking schema design | Pending |

### DA-F1 — Trajectory Endpoint Absent from api_contracts.yml

`GET /scenarios/{scenario_id}/trajectory` did not exist in `api_contracts.yml`. A partial
schema stub has been added (2026-05-22) documenting the known fields and flagging the three
open EL decisions as PENDING. The stub prevents implementation agents from calling or
implementing the endpoint without a schema contract, and registers the pending gaps so they
are visible in the schema file.

**Action taken:** Partial entry added to `docs/schema/api_contracts.yml` with PENDING tags
on DA-F2, DA-F3, DA-F4, DA-F5 elements.

### DA-F2 — No Composite-Score-Level MDA Floor Storage (EL Decision Required)

`mda_thresholds.floor_value` (`database.yml`) stores indicator-level breach thresholds
(e.g., `poverty_headcount_ratio < 0.40`, `reserve_coverage_months < 2.5`). The trajectory
view's Y-axis is the composite score. MDA floor lines on the trajectory view must be at the
composite-score level (ADR-010 Decision 6, CM-R3 disposition). Projecting indicator-level
floors to composite-score-level floors is explicitly prohibited by CM-R3 ("implies false
precision; projection is methodologically dishonest"). There is no composite-score-level floor
field or table in the current schema.

**Two options for EL decision:**

(a) **Add `composite_floor_value` field to `mda_thresholds`** — populated by a separate
    process (not derived from `floor_value` projection). Requires Alembic migration.
    Establishes a schema-native location for composite-score-level MDA floors.
    New `mda_thresholds` rows can carry both `floor_value` (indicator-level, for Zone 2B)
    and `composite_floor_value` (composite-level, for Zone 1A trajectory view).

(b) **Defer MDA floor overlays on the trajectory view** — do not render MDA floor
    `<ReferenceLine>` elements until a composite-score-level threshold table or field is
    defined. Trajectory view renders without floor lines; Zone 2B retains indicator-level
    MDA alert rows. MDA floor overlays are added in a future PR once the schema is resolved.

**Implementation must not proceed on MDA floor overlays until EL chooses (a) or (b).**

### DA-F3 — ci_lower / ci_upper Not in Any Schema File

`ci_lower` and `ci_upper` fields appear in the FA brief's uncertainty band `<Area>` component
and in the `TrajectoryResponse.FrameworkCurvePoint` shape. They do not exist in `database.yml`,
`api_contracts.yml`, or `simulation_state.yml`. These fields will be populated by the
BandingEngine (pending ADR-007). They are registered as PENDING in the trajectory endpoint
stub added under DA-F1.

**No immediate action required** — they are correctly gated on ADR-007 acceptance. The schema
stub registration prevents silent addition without schema contract. When ADR-007 is accepted,
update `api_contracts.yml` and `database.yml` in the same PR that implements the BandingEngine.

### DA-F4 — Single-Entity Null: Trajectory View Undefined for Mode 1 Greece (EL Decision Required)

In the existing `measurement-output` endpoint, `composite_score` is null for financial and
human_development frameworks when `single_entity_warning=true` (Issue #193). The Greece demo
fixture is a single-entity scenario. If the trajectory endpoint propagates this null, the
trajectory view for Greece Mode 1 would show no financial or human_development curves —
defeating the purpose of the primary demo scenario.

The FA brief's null governance guard (`connectNulls={false}` on the governance `<Line>`) is
correct. But it does not address the separate null case for financial/human_development in
single-entity Mode 1.

**Two options for EL decision:**

(a) **Trajectory endpoint uses raw indicator signal for single-entity scenarios** — instead of
    percentile rank composite score (which requires ≥2 entities), the trajectory endpoint
    returns a single-entity-specific composite score derivation. Requires an ADR or EL
    decision on the methodology. Unblocks Mode 1 Greece demo trajectory view.

(b) **Mode 1 single-entity trajectory view shows "single-entity advisory" overlay** — financial
    and human_development curves are suppressed; a user-visible label explains that composite
    percentile rank requires a comparison entity. Trajectory view shows ecological and
    governance curves only (both of which have different null reasons).

**Issue #193 is a prerequisite for Mode 1 single-entity trajectory rendering.** The FA brief's
implementation sequencing must note this dependency.

### DA-F5 — step_event_label and step_significance Have No Schema Home

The FA brief references `step_event_label` (≤ 8 words AND ≤ 32 characters) and
`step_significance` ("SIGNIFICANT" | "ROUTINE" — per ADR-010 Decision 7; "STANDARD" is incorrect) as mandatory fields for Mode 1 step
annotation. `effective_from` maps to `scenario_state_snapshots.timestep`. The other two
fields have no schema home.

**Three candidate storage approaches for EL/Architect decision:**

(a) **Per-step metadata in scenario configuration JSONB** — add a `step_annotations` key to
    `scenarios.configuration` with structure `{step_index: {label, significance}}`. Populated
    at scenario creation. No migration needed (JSONB extension). Query: read from
    `scenarios.configuration->'step_annotations'` in the trajectory endpoint.

(b) **New `step_annotations` table** — one row per (scenario_id, step_index), columns:
    `step_event_label text nullable`, `step_significance text nullable`. Alembic migration
    required. More structured; supports future step-level metadata.

(c) **Embedded in fixture JSON only; not DB-persisted** — fixture files carry the annotation
    fields as configuration metadata; the trajectory endpoint derives them from the scenario
    configuration at request time. No migration needed for historical fixtures.

**Recommendation:** Option (a) for M9 (minimum viable; no migration). Option (b) if
step-level metadata grows beyond two fields. The FA brief's fixture CI gate
(`pytest tests/fixtures/`) enforces the character constraints; the storage schema question
is orthogonal to validation.

**The trajectory endpoint cannot return `step_event_label` or `step_significance` until
this storage design is decided.**

---

## Appendix — Review Findings Log

Three-agent review conducted 2026-05-22 (UX Design Thinking, UX Designer, QA Lead).
All 10 findings incorporated; brief updated before PR merge.

| ID | Source | Finding summary | Resolution |
|---|---|---|---|
| UT-F1 | UX Design Thinking | 240px column: MDA compact row format unspecified | INCORPORATED — §Layout and Viewport |
| UT-F2 | UX Design Thinking | Choropleth navigation affordance out of brief scope | LOG — M9 implementation planning item |
| UD-F1 | UX Designer | Compact alert row ruling at 240px: 3-line spec | INCORPORATED — §Layout and Viewport |
| UD-F2 | UX Designer | Badge font 11px minimum (WCAG informational text) | INCORPORATED — §Confidence Tier Visual |
| QA-F1 | QA Lead | AC-006: "before next paint" → `act()` call boundary | INCORPORATED — §Named Acceptance Criteria |
| QA-F2 | QA Lead | Playwright throttle ≠ hardware; supplement with MV-002 | INCORPORATED — §Manual Validation Gates |
| QA-F3 | QA Lead | AC-013 CVD cannot be automated | INCORPORATED — moved to §Manual Validation Gates |
| QA-F4 | QA Lead | AC-017 sign-off is process gate, not acceptance criterion | INCORPORATED — moved to §Implementation Sequencing |
| QA-F5 | QA Lead | AC-016 Playwright SVG assertion fragile → Vitest unit test | INCORPORATED — §Named Acceptance Criteria |
| QA-F6 | QA Lead | Fixture CI gate: clarify `pytest tests/fixtures/` suite | INCORPORATED — §Mode 1 Step Axis Annotation |
