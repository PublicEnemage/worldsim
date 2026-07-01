---
name: M18-G7-A-ci-band-geometry
type: implementation-intent
issues:
  - "#1466 — DEMO-137: CI band geometry bug (fills to chart ceiling)"
  - "#1467 — DEMO-138: Zone 1A trajectories indistinguishable (y-axis compression)"
  - "#1474 — DEMO-145: CI band prominence inverted (Mode 3 > Mode 1/2)"
status: Filed — all gates CLEAR
authored-by: Frontend Architect Agent
authored-date: 2026-06-29
implementing-agent: Frontend Architect Agent
sprint-entry: docs/process/sprint-plans/m18-g7-sprint-entry.md
adr-reference: "ADR-007 (CI band spec — bug fix within existing spec, no amendment required)"
governing-adrs:
  - "ADR-007 — Synthetic data and CI band framework"
  - "ADR-010 — Trajectory view component architecture; CI band rendering (Decision 10)"
root-cause-reference: docs/demo/m18/reviews/2026-06-29-g7-root-cause-analysis.md
release-branch: release/m18
bpo-acceptance-required: "No — bug fix restoring spec-correct behaviour"
customer-agent-l3-required: "No — rendering correctness fix, not a new capability"
---

# Implementation Intent: M18-G7-A — CI Band Geometry Fix

> **Pre-implementation prerequisites (all required before implementation PR opens):**
> - [x] G7-0 root cause analysis filed and EL-approved (2026-06-29)
> - [x] ADR gate: no amendment required (bug fix within ADR-007/ADR-010 spec)
> - [ ] QA tests authored and committed (red) before implementation code

---

## 0. Implementation Constraints

*Authority: G7-0 root cause analysis §Root Cause 1. These are not design decisions — they are corrections to deviations from the existing ADR-007/ADR-010 specification.*

1. **Formula correction is additive, not multiplicative.** The CI band formula `score ± halfWidth` is specified in the ADR-007/ADR-010 contract. The current implementation uses `score * (1 ± halfWidth)`. The multiplicative formula is wrong. The fix is exactly one word: `score + halfWidth` and `score - halfWidth`.

2. **yDomain must exclude CI bounds.** `CompositeChartSVG` yDomain computation must derive from trajectory `composite_score` values only. CI band values (`ci_upper`, `ci_lower`) are excluded from the yDomain. CI fills clip at the chart boundary — this is correct and expected for semi-transparent fills.

3. **Opacity constants must be used, not hard-coded values.** The exported constants `CI_BAND_OPACITY` and `CI_BAND_OPACITY_MODE3` must be applied to the SVG ribbon path. The current hard-coded `opacity={0.10}` at lines ~542 and ~557 must be replaced with the correct constant reference.

4. **Do not modify the geometric path construction (`buildCIRibbonPath`).** The root cause analysis confirms the polygon geometry (upper forward + lower reversed + close) is correct. Only the coordinate inputs are wrong.

5. **No other `TrajectoryView.tsx` changes in this PR.** Cluster A touches only the three issues listed above. Do not refactor surrounding code, change data binding, or modify Mode 1/2 rendering paths.

---

## 1. Source

**Issues:** #1466 (DEMO-137), #1467 (DEMO-138), #1474 (DEMO-145)

**Root cause document:** `docs/demo/m18/reviews/2026-06-29-g7-root-cause-analysis.md §Root Cause 1`

**Governing ADR:** ADR-010 Decision 10 (confidence tier visual implementation, CI band infrastructure). ADR-007 (CI band schedule — defines halfWidth contract).

**Demo 7 anchor:** Act 1 (Senegal Mode 3). CI bands in Zone 1A must form a visible but non-dominant envelope around the trajectory curves at T3 confidence. Before this fix: bands fill to the chart ceiling and compress trajectories to the bottom 5% of chart height. After this fix: bands form a correctly-centred `[score ± halfWidth]` envelope and the y-axis scales to the trajectory range.

---

## 2. Persona Trace (abbreviated — bug fix)

**Personas affected:** Persona 2 (Eleni, Finance Ministry Negotiator — reads Zone 1A trajectory for counter-proposal divergence); Persona 5 (Aicha, Finance Minister — observes trajectory legibility during live session).

**Capability before fix:** Zone 1A trajectory curves are compressed to the bottom 5% of chart height. The CI band fills the entire chart area. Baseline and counter-proposal trajectories are visually indistinguishable.

**Capability after fix:** Zone 1A trajectory curves occupy their natural range in chart space. CI band is a visible semi-transparent envelope (Mode 3: 5% opacity) around each curve — present but not dominant.

**North star relevance:** The Senegalese finance ministry analyst demonstrating the counter-proposal divergence in Mode 3 cannot read a trajectory that occupies 5% of the chart. This is a blocking legibility failure at the negotiating table.

---

## 3. Observable Application State

### 3.1 Primary observable state

**In Mode 3 with the SEN demo scenario at T3 confidence, step 6:**

Zone 1A (`[data-testid="zone-1a-trajectory"]`) shows four trajectory curves that together occupy the majority of the chart height. The curves are visually distinguishable from one another. The CI band (semi-transparent fill around each curve) does NOT occlude the trajectory lines. The y-axis tick labels correspond to the trajectory value range (approximately 0.48–0.56), not to the CI bound range (0–1).

### 3.2 Secondary observable states

**State A — CI band envelope shape:** At any step with T3 composite data, the CI fill region is centred on the trajectory curve with approximately equal space above and below. The fill region is not a solid block from the curve to the chart top.

**State B — y-axis scale:** The y-axis maximum tick value is close to the maximum trajectory composite score (not 0.97 or 1.0 when trajectory range is 0.48–0.56).

### 3.3 Silent failure detection

**Silent failure — formula regression:** CI band still extends above or below the trajectory curve asymmetrically (multiplicative not additive). Observable via unit test: `computeCompositeCIBounds(step=6, tier=3)` with score=0.50 returns upper ≤ 0.50 + halfWidth, not 0.50 * (1 + halfWidth).

**Silent failure — yDomain regression:** y-axis maximum is driven up to ~0.97 by CI upper bound inclusion. Observable via unit test: yDomain computation from trajectory values [0.48, 0.50, 0.52, 0.54] returns yMax ≤ 0.60 (with padding), not ≥ 0.90.

**Silent failure — opacity regression:** CI band renders at 0.10 opacity in Mode 3 instead of 0.05. Observable via unit test: ribbon path `opacity` attribute equals `CI_BAND_OPACITY_MODE3` value (0.05) in Mode 3, not 0.10.

---

## 4. Acceptance Criteria

**AC-A1 (unit — additive formula):**
`computeCompositeCIBounds(step, tier)` with `score = 0.50` and any step/tier combination returns `upper = Math.min(1.0, score + halfWidth)` and `lower = Math.max(0.0, score - halfWidth)`. Specifically: for T3 at step 6 (halfWidth = 0.75), `upper = 1.0` (capped), `lower = 0.0` (capped). For T3 at step 1 (baseHW = 0.10, multiplier = 1.5, halfWidth = 0.15), `upper = 0.65`, `lower = 0.35`. No result should satisfy `upper = score * (1 + halfWidth)`.
*Source: §0 Constraint 1 + root cause analysis §Root Cause 1 §Fix item 1*

**AC-A2 (unit — yDomain excludes CI bounds):**
`CompositeChartSVG` yDomain computation with trajectory values `[0.48, 0.50, 0.52, 0.54]` and T3 CI bounds (upper ≈ 0.88 at step 6 from multiplicative formula; or 1.0 from additive+cap) returns `yMax ≤ 0.65` (trajectory max + standard padding). The `ci_upper` value of 0.88 or 1.0 does NOT appear in the values array used for `Math.max(...values)`.
*Source: §0 Constraint 2 + root cause analysis §Root Cause 1 §Fix item 2*

**AC-A3 (unit — opacity constant applied):**
The `buildCIRibbonPath` SVG element in `CompositeChartSVG` renders with `opacity = CI_BAND_OPACITY_MODE3` (0.05) in Mode 3, not the hard-coded value 0.10. In Mode 1/2, the standard `CI_BAND_OPACITY` constant is applied. Neither path hard-codes an opacity literal in the JSX `opacity` attribute.
*Source: §0 Constraint 3 + root cause analysis §Root Cause 1 §Fix item 3*

**AC-A4 (E2E — trajectory curves legible at 1440×900):**
In the SEN Mode 3 demo at T3 step 6, `[data-testid="zone-1a-trajectory"]` contains SVG path elements for all four framework curves. Each curve path's `d` attribute includes y-coordinates in the range corresponding to 40–70% of chart height (not compressed to the bottom 5%). CI band fill elements are present but have opacity ≤ 0.06. No CI fill element has a bounding box height greater than 80% of the chart height.
*Source: §3.1 + persona trace*

---

## 5. Kryptonite Constraint Check

No kryptonite risk for Persona 2 or 5 from this fix. The fix restores spec-correct rendering — it cannot introduce a legibility failure worse than the current state (trajectory curves compressed to 5% of chart height). Risk of regression: yDomain change might over-compress in edge cases where trajectory range is very narrow. The implementing agent must verify that the y-axis still shows a readable range (minimum 0.20 span) even when trajectory values are very close together.

---

## 6. Out of Scope

- ADR-007 band width multiplier changes (these are the correct values; the formula was wrong)
- Mode 1/2 Recharts path CI band changes (Recharts `<Area>` reads `ci_lower`/`ci_upper` from trajectory API — null for real scenarios; no change needed)
- Any other `TrajectoryView.tsx` changes
- Confidence tier visual changes (opacity, dashed curves) beyond the opacity constant fix

---

## 7. Test Authorship Obligation

**QA file:** `frontend/src/components/TrajectoryView.test.tsx` (add unit test block for CI geometry)

**Test authorship deadline:** Unit tests authored and committed to `feat/m18-g7-cluster-a` BEFORE implementation code changes. Tests must run red before fix, green after.

| AC | Test type | Description |
|---|---|---|
| AC-A1 | Unit | `computeCompositeCIBounds` returns additive bounds; specific numeric assertions for T3 step 1 and step 6 |
| AC-A2 | Unit | `CompositeChartSVG` yDomain computation excludes CI bound values; yMax ≤ trajectory_max + padding |
| AC-A3 | Unit | CI ribbon opacity attribute equals `CI_BAND_OPACITY_MODE3` in Mode 3 (not 0.10) |
| AC-A4 | E2E (optional) | Zone 1A trajectory curves not compressed at 1440×900 — verify path y-coordinate range |

AC-A4 E2E is lower priority than the unit tests — if the unit tests for A1/A2/A3 pass, the visual outcome follows mechanically. The E2E test is a belt-and-suspenders check.

**Pre-push gates:** `cd frontend && npm run build` must exit 0. TypeScript errors are a compliance finding.

*Filed: 2026-06-29. Authority: docs/process/agents.md §Frontend Architect Agent.*
