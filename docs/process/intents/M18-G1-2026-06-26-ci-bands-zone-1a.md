---
name: M18-G1-ci-bands-zone-1a
type: implementation-intent
issue: "#1254"
status: Filed — QA tests must be authored before implementation PR opens
authored-by: Frontend Architect Agent
authored-date: 2026-06-26
implementing-agent: Frontend Engineer + Computation Engine Agent
sprint-entry: "docs/process/sprint-plans/m18-g1-sprint-entry.md — EL Approved 2026-06-26"
adr-reference: "ADR-007 (synthetic data framework / BandingEngine methodology) + ADR-017 (Zone 1A information architecture)"
release-branch: release/m18
bpo-acceptance-required: "Yes — new visual element on Zone 1A primary instrument"
ux-mockup-required: true
ui-mockup-required: true
panel-review-required: true
---

# Implementation Intent: M18-G1 — CI Bands on Zone 1A (#1254)

> **Intent document gate (sprint entry §2.3).** This document must exist and the UX/UI
> panel review must record ACCEPT before the implementation PR opens. QA tests must be
> authored from the acceptance criteria in §5 before implementation code is written.
>
> **ADR authority:** ADR-007 (DATA_STANDARDS.md §Epistemic Band Labeling Standards)
> governs the `BandingEngine` computation — band schedule, tier multipliers, clipping
> rules, and required response fields. ADR-017 (Zone 1A Information Architecture,
> §Decision table) governs the visual encoding — CI ribbons are an addition to the
> existing framework-line and composite-line encoding in Zone 1A.
>
> **Demo 7 anchor:** Act 2 — Zambia three-scenario comparison. CI bands are the
> epistemic foundation for the claim "confidence band on the 340,000 vs. 80,000
> differential." Without bands visible on Zone 1A trajectories, the comparison
> differential (G3) has no visual uncertainty grounding.

---

## 1. Source

**Issue:** #1254 — ux(zone-1a): CI bands on Zone 1A trajectory curves — ADR-007
implementation

**Root cause (current state):** The `BandingEngine` (DATA_STANDARDS.md §Epistemic
Band Labeling Standards) has not been implemented. The backend `TrajectoryFrameworkPoint`
schema (`backend/app/schemas.py:92–95`) carries `ci_lower: None = None`, `ci_upper:
None = None`, `ci_coverage: None = None`, `is_pre_calibration: None = None` — always
null, explicitly marked "pending ADR-007." The frontend `TrajectoryFrameworkPoint` in
`frontend/src/store/scenarioStepStore.ts:15–16` already declares `ci_lower: number |
null` and `ci_upper: number | null`, and `TrajectoryView.tsx:978–991` already renders
an ADR-007-gated uncertainty band `Area` with `fillOpacity={0}` — the scaffolding is
in place, waiting for non-null backend data.

**The implementation:** Two parallel tracks.

- **Backend:** Implement `backend/app/simulation/banding_engine.py` per
  DATA_STANDARDS.md §Band Schedule and Tier Multipliers; update `schemas.py` to
  populate `ci_lower`/`ci_upper`/`ci_coverage`/`is_pre_calibration` on every
  `TrajectoryFrameworkPoint`; update the trajectory endpoint to call the banding engine.

- **Frontend:** Add `{fw}_ci_lower` / `{fw}_ci_upper` fields to `MergedStepDatum`
  (recharts N=1 path); update `mergeTrajectories`; change `fillOpacity={0}` to `0.12`;
  add per-trajectory CI ribbon paths to `CompositeChartSVG` (SVG composite path for
  multi-entity and N=3 scenario comparison).

---

## 2. Persona Trace

**Primary — Eleni Papadimitriou (Persona 2 — Finance Ministry Negotiator)**

- **Entry state:** Preparatory — building the Zambia counter-proposal evidence base
  the evening before the restructuring session.
- **Journey:** Journey A Step 3 (Validate uncertainty). Three Zambia scenarios loaded
  in N=3 COMPARE_VIEW. Eleni sees three composite score curves in Zone 1A.
- **Question:** "Is the difference between Option A and Option C stable under model
  uncertainty?" Zone 1A CI ribbons answer this directly — if the ribbons overlap
  across the three curves, the difference is not visually stable; if they do not
  overlap, the direction is visually confirmed.
- **Before G1:** Eleni must trust that the engine's point estimates are reliable
  without any visual uncertainty signal. She cannot confirm "direction stable" from
  Zone 1A alone.
- **After G1:** The CI ribbons show the uncertainty envelope around each composite
  curve. When the envelopes do not overlap at the terminal step, Eleni can state
  "the model uncertainty ranges are non-overlapping — the direction is stable across
  the full uncertainty range." This is the visual precondition for the Zone 1B
  direction-stability statement that G3 surfaces as text.

**Secondary — Lucas Ferreira (Persona 1 — Programme Analyst)**

- **Entry state:** Preparatory — reading Zone 1A for the Senegal Article IV scenario.
- **Question:** "How wide is the uncertainty on this trajectory, and does it change
  my reading of the floor headroom?"
- **P-4 — Time ceiling:** 4 minutes (Preparatory). The CI ribbon must be legible
  without interaction — opacity, color, and geometry must convey "uncertainty envelope"
  without explanation.
- **P-6 — Negotiating leverage:** Lucas can state the tier and the approximate
  uncertainty width from the ribbon geometry. "This projection carries a ±35% T3
  envelope at step 4 — the floor headroom is real but not certain."

**P-7 — North star capability:**
CI bands make the Zone 1A trajectory self-disclosing about its own uncertainty. The
Zambia Ministry analyst can show that CI ribbons on all three scenario curves do not
overlap at the terminal step, which grounds the Zone 1B distributional differential
claim (G3) as direction-stable rather than a point-estimate artifact.

---

## 3. BandingEngine Computation Specification

> This section is binding for the Computation Engine Agent implementing the backend.
> Authority: DATA_STANDARDS.md §Band Schedule and Tier Multipliers, §BandingEngine
> Is the Sole Source, §Attribute Boundary Classification.

### 3.1 — Band schedule

The BandingEngine computes an 80% confidence interval from three inputs:
`composite_score` (Decimal), `confidence_tier` (int 1–5), and `step_index` (int).

`step_index` maps to `horizon_steps` as follows: `horizon_steps = step_index` (the
trajectory response uses 1-indexed steps; step 1 = 1-year horizon from baseline).

**Base half-width by horizon:**

| step_index | horizon category | base half-width |
|---|---|---|
| 1 | 1 year | 0.10 (±10%) |
| 2 | 2 years | 0.20 (±20%) |
| 3, 4, 5 | 3–5 years | 0.35 (±35%) |
| > 5 | > 5 years | 0.50 (±50%) |

**Confidence tier multiplier:**

| Confidence tier | Multiplier |
|---|---|
| 1 | 1.0 |
| 2 | 1.2 |
| 3 | 1.5 |
| 4 | 2.0 |
| 5 | 3.0 |

**Combined half-width:**
```
half_width = base_half_width(step_index) × tier_multiplier(confidence_tier)
```

**Applied to composite score (±percentage of point estimate):**
```
raw_lower = composite_score × (1 - half_width)
raw_upper = composite_score × (1 + half_width)
```

**Boundary clipping by framework type:**

| Framework | Natural lower | Natural upper | Notes |
|---|---|---|---|
| financial | 0.0 | 1.0 | Bounded index [0, 1] |
| human_development | 0.0 | 1.0 | Bounded index [0, 1] |
| ecological | 0.0 | 2.0 | Boundary proximity [0, 2] |
| governance | null | null | composite_score = null throughout M18; no band produced |

Clipping:
```
ci_lower = max(natural_lower, raw_lower)   # clipped_lower = True if max fires
ci_upper = min(natural_upper, raw_upper)   # clipped_upper = True if min fires
```

**Required fields on every banded `TrajectoryFrameworkPoint`:**
- `ci_lower: str | None` — Decimal-as-string; None only when `composite_score` is None
- `ci_upper: str | None` — Decimal-as-string; None only when `composite_score` is None
- `ci_coverage: float | None` — `0.80` throughout M18; None only when composite_score is None
- `is_pre_calibration: bool | None` — `True` throughout M18 (MAGNITUDE_WITHIN_20PCT
  validation has not been confirmed for at least two independent historical cases);
  None only when composite_score is None

### 3.2 — Examples (Zambia scenario, step 4, T3)

```
composite_score = 0.62, confidence_tier = 3, step_index = 4

base_hw = 0.35 (step 3–5 range)
multiplier = 1.5 (T3)
half_width = 0.35 × 1.5 = 0.525

raw_lower = 0.62 × (1 - 0.525) = 0.62 × 0.475 = 0.2945
raw_upper = 0.62 × (1 + 0.525) = 0.62 × 1.525 = 0.9455

ci_lower = max(0.0, 0.2945) = "0.2945"   clipped_lower = False
ci_upper = min(1.0, 0.9455) = "0.9455"   clipped_upper = False
ci_coverage = 0.80
is_pre_calibration = True
```

### 3.3 — Backend schema change (`backend/app/schemas.py`)

The `TrajectoryFrameworkPoint` class must be updated:

```python
# Before:
ci_lower: None = None
ci_upper: None = None
ci_coverage: None = None
is_pre_calibration: None = None

# After:
ci_lower: str | None = None       # Decimal-as-string or None when composite_score is None
ci_upper: str | None = None       # Decimal-as-string or None when composite_score is None
ci_coverage: float | None = None  # 0.80 or None when composite_score is None
is_pre_calibration: bool | None = None  # True throughout M18 or None when score is None
```

Remove the existing docstring note "ci_lower, ci_upper, ci_coverage, and
is_pre_calibration are always null pending ADR-007." Replace with:
"ci_lower/ci_upper: 80% CI from BandingEngine (banding_engine.py). ci_coverage: 0.80.
is_pre_calibration: True until MAGNITUDE_WITHIN_20PCT achieved for ≥2 historical cases."

---

## 4. Data Contract — API and Schema Updates

> Both schema files must be updated in the same PR as the implementation.
> Authority: CLAUDE.md §Standards and Conventions "Schema reads are mandatory
> pre-implementation steps"; schema drift is a compliance violation.

### 4.1 — `docs/schema/api_contracts.yml`

In the `/scenarios/{scenario_id}/trajectory` GET response, the `frameworks` array
items must be updated to remove the "ci_lower/ci_upper remain pending ADR-007" note
and add the field specifications:

```yaml
ci_lower:
  type: "string|null"
  description: >
    Lower bound of 80% CI for this framework composite score at this step.
    Decimal-as-string. Null when composite_score is null (governance or
    single-entity financial/HD without normalizable indicators).
    Computed by BandingEngine from step_index, confidence_tier, and composite_score.
    Not a synthetic inference band — see ADR-007 §Section 3 for distinction.
ci_upper:
  type: "string|null"
  description: >
    Upper bound of 80% CI. Clipped at natural boundary (0.0–1.0 for
    financial/HD; 0.0–2.0 for ecological). Null under same conditions as ci_lower.
ci_coverage:
  type: "number|null"
  description: "0.80 throughout M18. Null when composite_score is null."
is_pre_calibration:
  type: "boolean|null"
  description: >
    True until MAGNITUDE_WITHIN_20PCT validation is achieved for ≥2 independent
    historical cases. True throughout M18. Null when composite_score is null.
```

### 4.2 — `docs/schema/simulation_state.yml`

No change required. CI bands are computed at query time by the BandingEngine from
`composite_score`, `confidence_tier`, and `step_index`. They are not stored in
`scenario_state_snapshots`.

---

## 5. Frontend Rendering Specification

> This section is binding for the Frontend Engineer implementing Zone 1A CI ribbons.
> Authority: ADR-017 §Decision table encoding specifications; DATA_STANDARDS.md §Band
> Schedule.

### 5.1 — Recharts mode (N=1 single-entity, non-composite path)

**`MergedStepDatum` interface additions** (`TrajectoryView.tsx:151–170`):

```typescript
financial_ci_lower: number | null;
financial_ci_upper: number | null;
human_development_ci_lower: number | null;
human_development_ci_upper: number | null;
ecological_ci_lower: number | null;
ecological_ci_upper: number | null;
governance_ci_lower: number | null;
governance_ci_upper: number | null;
```

**`mergeTrajectories` additions** (`TrajectoryView.tsx:176–222`):

Add a `ci` helper alongside the existing `get` helper:
```typescript
const ci = (fw: string, bound: "ci_lower" | "ci_upper"): number | null =>
  step.frameworks[fw]?.[bound] ?? null;
```

Return object additions:
```typescript
financial_ci_lower: ci("financial", "ci_lower"),
financial_ci_upper: ci("financial", "ci_upper"),
// ... (all four frameworks, both bounds)
```

**fillOpacity change** (`TrajectoryView.tsx:985`):

```typescript
// Before:
fillOpacity={0}

// After:
fillOpacity={CI_BAND_OPACITY}
```

Add constant at the top of the file with other exported constants:
```typescript
export const CI_BAND_OPACITY = 0.12;
```

**Interaction:** No hover tooltip in G1. The band is a background geometry layer —
the existing recharts `Tooltip` for point values remains unchanged. Tooltip-on-hover
for CI bounds is out of scope for G1 (see §7).

### 5.2 — Composite SVG mode (ADR-017 N>1 entities and N=3 scenario comparison)

CI ribbons must also be rendered in `CompositeChartSVG` for both per-entity
trajectories and per-scenario comparison trajectories. The recharts path at §5.1
covers only the N=1 single-entity recharts mode; the SVG composite mode has no
existing CI rendering.

**Composite CI computation in the SVG path:**

The composite score is a mean of non-null per-framework scores. The composite CI
bounds are computed using the worst confidence tier at the step (consistent with
`getEntityWorstTier`, which already exists at `TrajectoryView.tsx:134`):

```typescript
function computeCompositeCIBounds(step: TrajectoryStep): {
  lower: number | null;
  upper: number | null;
} {
  const score = computeEntityCompositeScore(step);
  if (score === null) return { lower: null, upper: null };
  const worstTier = getEntityWorstTier(step);
  const halfWidth = computeCompositeHalfWidth(step.step_index, worstTier);
  return {
    lower: Math.max(0.0, score * (1 - halfWidth)),
    upper: Math.min(1.0, score * (1 + halfWidth)),
  };
}

function computeCompositeHalfWidth(stepIndex: number, tier: number): number {
  const baseHW = stepIndex === 1 ? 0.10
    : stepIndex === 2 ? 0.20
    : stepIndex <= 5 ? 0.35
    : 0.50;
  const multiplier = [1.0, 1.0, 1.2, 1.5, 2.0, 3.0][Math.min(tier, 5)];
  return baseHW * multiplier;
}
```

**CI ribbon SVG polygon:** Build a closed polygon path tracing upper bounds forward
and lower bounds backward (same pattern as existing divergence fill at
`TrajectoryView.tsx:463–494`):

```typescript
function buildCIRibbonPath(steps: TrajectoryStep[]): string {
  const upperPts: string[] = [];
  const lowerPts: string[] = [];
  for (const step of steps) {
    const { lower, upper } = computeCompositeCIBounds(step);
    if (lower === null || upper === null) continue;
    upperPts.push(`${xScale(step.step_index).toFixed(1)},${yScale(upper).toFixed(1)}`);
    lowerPts.unshift(`${xScale(step.step_index).toFixed(1)},${yScale(lower).toFixed(1)}`);
  }
  if (upperPts.length < 2) return "";
  return "M " + upperPts.join(" L ") + " L " + lowerPts.join(" L ") + " Z";
}
```

**Rendering position:** CI ribbons are rendered BEFORE the trajectory path lines in
`CompositeChartSVG` so the line renders on top of the ribbon. Insertion point: between
the "Y-axis grid and labels" block and the "Divergence fills" block in the JSX.

**Visual spec:**
- `fill`: same color as the entity / scenario trajectory line (`ENTITY_PALETTE[i]` for
  entities; `SCENARIO_COMPARISON_PALETTE[sc.paletteIndex].color` for comparison scenarios)
- `opacity`: `0.10` (slightly lower than divergence fill `0.08` — set at `0.10` so the
  ribbon is visible but does not compete with the divergence fill geometry)
- `stroke`: `none`
- `data-testid` for per-entity: `zone-1a-ci-ribbon-{code}` (e.g., `zone-1a-ci-ribbon-ZMB`)
- `data-testid` for comparison scenarios: `zone-1a-ci-ribbon-scenario-{slug}` (e.g.,
  `zone-1a-ci-ribbon-scenario-option-a`)

**`yDomain` extension:** The CI ribbon upper bound may exceed the current trajectory's
y-domain. The `computeYDomain` call in `CompositeChartSVG` at `TrajectoryView.tsx:362–381`
must include CI upper bound values alongside composite scores and MDA floor values. Add
a `computeCompositeCIBounds(step).upper` call alongside `computeEntityCompositeScore`
in the values collection loop.

---

## 6. Observable Application State

### 6.1 — Primary observable state

**Recharts N=1 mode (single-entity, per-framework lines):**

At 1280×800 with the Zambia baseline scenario loaded in Mode 1 or Mode 2, Zone 1A
renders four framework lines. Each line has a semi-transparent filled ribbon area
between the CI lower and upper bounds. The ribbon is visible without hover or
interaction. Ribbon opacity is 0.12 (same color as the framework line).

Observable without source code: The area between a framework line and the lower/upper
CI bounds is visibly shaded in the framework color at approximately the same saturation
as the divergence fill (which uses 0.08 opacity for reference). The ribbon is wider at
later steps than at step 1, reflecting the horizon-dependent band schedule. At step 1,
the ribbon is narrowest; at step 5, it is widest.

**Composite SVG mode (N=3 comparison or multi-entity):**

With three Zambia restructuring scenarios loaded in N=3 COMPARE_VIEW, Zone 1A renders
three palette-colored composite score curves. Each curve has a CI ribbon polygon in the
same color at 0.10 opacity. The ribbons do not overlap each other at the terminal step
(if the scenario differentiation is sufficient for Demo 7 Act 2). The ribbon geometry
widens step-by-step, visible as expanding shaded areas around each curve.

Observable without source code: The `data-testid="zone-1a-ci-ribbon-scenario-{slug}"`
SVG `<path>` elements are present in the DOM with `fill` matching the scenario palette
color and `opacity="0.1"`. The path data (`d` attribute) forms a closed polygon.

### 6.2 — Secondary observable states

**State B — Graceful degradation (no CI data):**
When `ci_lower` and `ci_upper` are null in the trajectory response (e.g., governance
framework, or legacy scenario without banding engine data), the CI ribbon path is absent
for that framework/entity. The trajectory line renders normally without a ribbon. No
error, no placeholder. This is the current behavior; G1 does not change it.

**State C — Clipped bands:**
When the Tier 4 (or worse) + long-horizon combination clips the upper band to 1.0
(natural boundary), the ribbon polygon's upper edge is flat at the boundary value.
This is visible as a straight horizontal upper edge on the ribbon at y=yScale(1.0).
No special disclosure required for G1 — the `is_pre_calibration: True` context applies.

### 6.3 — Silent failure detection

**Silent failure — fillOpacity zero:** If `fillOpacity={0}` is not changed to
`fillOpacity={CI_BAND_OPACITY}`, the bands exist in the DOM but are invisible.
AC-1254-1 (E2E DOM assertion on `fill-opacity`) catches this directly.

**Silent failure — null CI data in SVG path:** If the backend populates `ci_lower`/
`ci_upper` but `mergeTrajectories` does not extract them, the recharts bands render
with null data and fall back to baseline behavior (no band). AC-1254-2 (unit test
on `mergeTrajectories` output) catches this by asserting non-null `financial_ci_lower`
given non-null input.

**Silent failure — SVG CI ribbon absent:** If `buildCIRibbonPath` is not called for
comparison scenario trajectories, the SVG path element with the expected `data-testid`
is absent. AC-1254-3 (E2E assertion on `data-testid` presence) catches this.

**Silent failure — yDomain not extended:** If CI upper bounds are not included in
`computeYDomain` values, ribbons that exceed the natural data range are clipped by
the `yScale` clamp. The ribbon upper edge appears flat at the chart top rather than
at the correct proportional position. AC-1254-4 (unit test on `computeYDomain`)
catches this by asserting `yMax ≥ max(ci_upper values)`.

---

## 7. Acceptance Criteria

**AC-1254-1 (E2E — recharts CI band opacity):**
In a Zone 1A render with a single-entity scenario (Zambia baseline, Mode 1) at
1280×800:
- The recharts `<Area>` elements with `key="financial-band"`, `"human_development-band"`,
  `"ecological-band"` are present in the rendered output.
- The DOM `fill-opacity` attribute on the band `<path>` elements is `"0.12"` (or the
  numeric equivalent from recharts rendering). A value of `"0"` is a hard-fail.
- At least one framework's band has a non-zero vertical extent (the `d` path attribute
  contains a non-degenerate polygon, not a zero-height line).

**AC-1254-2 (unit — mergeTrajectories CI extraction):**
Given a mock `TrajectoryResponse` where `step.frameworks["financial"].ci_lower = 0.45`
and `ci_upper = 0.65`, `mergeTrajectories(trajectory, null)` returns a datum where
`financial_ci_lower = 0.45` and `financial_ci_upper = 0.65`. Given a null ci_lower
input, the datum has `financial_ci_lower = null`.

**AC-1254-3 (E2E — SVG composite CI ribbon present):**
In a Zone 1A render with N=3 comparison scenarios loaded (Zambia Option A, B, C at
1280×800, Mode 2):
- `data-testid="zone-1a-ci-ribbon-scenario-option-a"` is present in the DOM (or the
  slug equivalent for the first scenario).
- The element is an SVG `<path>` with a non-empty `d` attribute.
- The `opacity` attribute is `"0.1"` (or equivalent rendered value).

**AC-1254-4 (unit — yDomain extended for CI bounds):**
Given values `[0.60, 0.70, 0.80]` for composite scores and an `upper_ci` of `0.95`
for one step, `computeYDomain` (updated with CI upper values included) returns
`[yMin, yMax]` where `yMax >= 0.95`. A `yMax` of `0.85` (computed from scores alone)
is a hard-fail.

**AC-1254-5 (backend integration — CI fields populated):**
A GET to `/scenarios/{zambia_baseline_id}/trajectory` returns a response where
`steps[3].frameworks["financial"].ci_lower` is a non-null Decimal-as-string,
`ci_upper` is non-null, `ci_coverage = 0.8`, and `is_pre_calibration = true`.
The `ci_lower` value satisfies `0 ≤ ci_lower ≤ composite_score ≤ ci_upper ≤ 1.0`
for `financial` and `human_development` frameworks. For `ecological`,
`ci_upper ≤ 2.0`.

**AC-1254-6 (backend unit — BandingEngine schedule):**
For `composite_score = Decimal("0.62")`, `confidence_tier = 3`, `step_index = 4`:
`ci_lower ≈ "0.2945"` and `ci_upper ≈ "0.9455"` (within Decimal precision tolerance).
For `composite_score = Decimal("0.90")`, `confidence_tier = 4`, `step_index = 6`:
`half_width = 0.50 × 2.0 = 1.0`; `raw_upper = 1.80`; `ci_upper = "1.0"` (clipped,
`clipped_upper = True`).

**AC-1254-R1 (regression — N=1 recharts unchanged behavior):**
For a single-entity scenario where all framework `ci_lower`/`ci_upper` return null
(governance framework, or legacy scenario), Zone 1A renders the four framework lines
without any visible ribbon — no rendering artifacts, no console errors.

**AC-1254-R2 (regression — ADR-015 Zone 1D unchanged):**
Zone 1D renders normally after G1 implementation. The PSP and basis annotations from
ADR-015 are unaffected by the CI band changes in Zone 1A.

---

## 8. Kryptonite Constraint Check

**Does the CI ribbon require economist interpretation for Persona 2 to use Zone 1A?**

`[x]` **No — the ribbon is self-interpreting as "uncertainty envelope" without
explanation.**

The ribbon is a standard uncertainty visualization pattern (shaded area around a
central line). The width changing with step distance is proportionally legible: "the
further out, the wider the band." Persona 2 does not need to know the specific ±35%
formula to use the visual signal. The Tier badge (already present from ADR-017 at
`zone-1a-tier-badge-{code}`) provides the epistemic grade for users who want it.

**Does the CI ribbon introduce false precision for Persona 1?**

`[x]` **No — the ribbon discloses that bands are pre-calibration (`is_pre_calibration:
True`).** Lucas can read the Tier badge and the band width as a proxy for the
`is_pre_calibration` state. The ribbon is wider than a calibrated interval would be,
intentionally overstating uncertainty per DATA_STANDARDS.md §Band Schedule ("Conservative
by design — overstates uncertainty, never understates").

**Does the ribbon make Zone 1A harder to read at the 15-second Mode 3 ceiling?**

`[!]` **Risk — to be confirmed at panel review.** In Mode 3 with two entities
(baseline ghost + active composite), adding CI ribbons to both paths potentially adds
4 ribbon polygons (2 entities × upper/lower). At `opacity=0.10`, the risk is visual
noise in the divergence fill region.

**Panel review mandate:** The UX/UI panel (§mandatory §2.3 gates) must assess
Mode 3 N=2 rendering with ribbons at opacity 0.10 against both the active composite
line and the baseline ghost. If ribbons make the divergence fill illegible, the panel
must resolve: (a) suppress CI ribbons in Mode 3, showing them only in Mode 1/2; or
(b) reduce ribbon opacity in Mode 3 to 0.05. This determination must be recorded in
the panel review artifact.

---

## 9. Out of Scope

| Item | Rationale |
|---|---|
| Hover tooltip showing exact CI bound values | Deferred — adds interaction complexity to a background geometry layer; out of scope for G1 |
| Per-framework CI badge in Zone 1A | ADR-007 synthetic badge is a Zone 3 disclosure; CI ribbons are the Zone 1 visualization |
| Synthetic inference bands (ADR-007 §Section 3) | Distinct from BandingEngine model uncertainty bands; not implemented in M18 |
| `clipped_lower`/`clipped_upper` field in API response | BandingEngine computes internally; not surfaced in API response for M18 (disclosure text deferred) |
| CI bands in Zone 1B, 1C, or 1D | G1 scope is Zone 1A and the backend banding engine only |
| Anomaly detection (ADR-007 §Section 7) | TSC gate required; not in M18 |
| CI bands in Mode 3 CI suppression logic (ADR-007 §Section 5 Mode 3 tightening) | Governance indicators only; composite score CI bands are not subject to Mode 3 suppression |
| `SyntheticDataEngine` implementation (ADR-007 §Consequences) | Independent implementation track; G1 is BandingEngine only |

---

## 10. Test Authorship Obligation

**Implementing agents:** Frontend Engineer (frontend tests); Computation Engine Agent
(backend tests)

**Test files to be authored before implementation PR opens:**

| Test file | Coverage | Authored before impl? |
|---|---|---|
| `frontend/tests/e2e/m18-g1-ci-bands.spec.ts` | AC-1254-1, AC-1254-3 | Required |
| `frontend/src/components/__tests__/TrajectoryView.test.ts` | AC-1254-2, AC-1254-4 (unit) | Required |
| `backend/tests/test_m18_g1_ci_bands.py` | AC-1254-5, AC-1254-6 (backend) | Required |

**Regression tests:** AC-1254-R1 and AC-1254-R2 may be authored alongside the
implementation but must be red-green verified before the PR merges.

**Pre-push gate:** `cd backend && ruff check . && mypy app/` must exit 0 before any
push touching backend files. `cd frontend && npm run build` must exit 0 before any
push touching frontend files. Both gates enforced by `.githooks/pre-push`.

**No soft-skip patterns (NM-056 guard):** All acceptance criteria must be hard-fail.
If the Zambia baseline scenario fixture is not available in the Playwright session for
AC-1254-1, the E2E test uses a synthetic `TrajectoryResponse` mock with pre-populated
`ci_lower`/`ci_upper` values — not a skipped assertion.

---

## 11. Implementation Sequencing

The recommended implementation order avoids pushing untested backend changes before
the frontend is ready to exercise them:

1. Backend: author `backend/tests/test_m18_g1_ci_bands.py` (red)
2. Backend: implement `backend/app/simulation/banding_engine.py`
3. Backend: update `backend/app/schemas.py` `TrajectoryFrameworkPoint` fields
4. Backend: wire banding engine into trajectory computation in `web_scenario_runner.py`
5. Backend: run tests — all three ACs must green before frontend begins
6. Update schema files: `docs/schema/api_contracts.yml`
7. Frontend: author test files (red)
8. Frontend: update `MergedStepDatum`, `mergeTrajectories`, `fillOpacity`
9. Frontend: implement `CompositeChartSVG` CI ribbon rendering
10. Frontend: extend `computeYDomain` call to include CI upper values
11. Pre-push gate: both backend (ruff + mypy) and frontend (npm run build) exit 0
12. PR targeting `sprint/m18-g1`; set auto-merge

---

*Intent document authority: `docs/process/sprint-plans/m18-g1-sprint-entry.md §2.3`
(intent document gate — UX/UI-impacting implementation). Issue: #1254 (CI bands on
Zone 1A — ADR-007 implementation). Implementing agents: Frontend Engineer + Computation
Engine Agent. Sprint sub-branch: `sprint/m18-g1`. EL-approved sprint entry: 2026-06-26.
Pre-push gate: backend ruff + mypy AND frontend npm run build must exit 0.*
