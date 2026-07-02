# G7-0 Root Cause Analysis — Demo 7 Step 6b Findings

**Date:** 2026-06-29
**Milestone:** M18 — Full Argument and Demo 7
**Sprint group:** G7 — Demo 7 Continuation
**Authority:** `docs/process/sprint-plans/m18-g7-sprint-entry.md §G7 Entry Preconditions`
**Source reviewed:** `docs/demo/m18/reviews/2026-06-29-v0.18.0-internal-review.md` (24 findings, DEMO-130–DEMO-153)
**Files read:** `demo-narrated.spec.ts`, `TrajectoryView.tsx`, `FourFrameworkZone1D.tsx`, `MDAAlertPanelZone1B.tsx` (contains `DistributionalComparisonSummary`, `CohortImpactSection`), `ScenarioInstrumentCluster.tsx` (psp_dominant_driver extraction), backend `schemas.py` + `module.py` + `scenarios.py`

**EL sign-off:** Required before any fix intent documents are authored.

---

## Executive summary

The 24 Step 6b findings reduce to **five root causes** across five distinct implementation layers. Three of the seven CRITICAL findings share a single root cause (spec capture sequence). Two CRITICAL findings share a second root cause (Zone 1B height budget / sticky-bottom clipping). One CRITICAL finding has a backend mock root cause (missing psp_dominant_driver in Act 1 mock). One CRITICAL finding has a component design root cause (CohortImpactSection alert-only surface).

The HIGH CI band geometry finding (DEMO-137) is an independent bug — the wrong mathematical formula in `computeCompositeCIBounds` — and it cascades into four other findings (DEMO-138 y-axis compression, DEMO-145 prominence inversion, and the visual illegibility of Frames A–E generally).

No finding has an architectural root cause that calls the platform principle into question. All fixes are within the boundaries of existing ADRs or require narrow amendments.

---

## Root Cause 1 — CI band geometry: multiplicative formula; y-axis includes CI bounds

**Findings:** DEMO-137 (HIGH), DEMO-138 (HIGH cascade), DEMO-145 (HIGH cascade)
**File:** `frontend/src/components/TrajectoryView.tsx`
**Cluster:** A

### Finding

`computeCompositeCIBounds` (line 164–173 of `TrajectoryView.tsx`) uses a **multiplicative** formula:
```
upper: Math.min(1.0, score * (1 + halfWidth))
lower: Math.max(0.0, score * (1 - halfWidth))
```

The Step 6b panel review specifies the correct geometry as `[mean - halfWidth, mean + halfWidth]` — an **additive** formula. At T3, step > 5: `halfWidth = 0.50 × 1.5 = 0.75`. With score ≈ 0.50, the multiplicative formula gives upper = 0.875, lower = 0.125 — a band spanning 75% of [0,1] chart space.

Compound bug: `CompositeChartSVG`'s yDomain computation (lines 411–434) includes `ci_upper` values in the values array:
```tsx
const { upper } = computeCompositeCIBounds(step);
if (upper !== null && !isNaN(upper)) values.push(upper);
```
This drives yMax to ≈ 0.88 + padding ≈ 0.97, compressing trajectory values (0.50–0.54) to occupy ≤ 5% of chart height (DEMO-138 visual indistinguishability). Mode 3 opacity constant `CI_BAND_OPACITY_MODE3 = 0.05` is correctly defined but the band is so geometrically large that 5% opacity over 75% chart height is visually dominant.

DEMO-145 (CI band prominence inverted) follows: SEN Mode 3 at T3 step > 5 produces large absolute CI area even at 5% opacity; ZMB Mode 1/2 uses the Recharts path which reads `ci_lower`/`ci_upper` from the trajectory API — null for real scenarios, so Mode 1/2 bands are effectively invisible. The prominence ordering is reversed from the intended spec.

### Fix

1. Change `computeCompositeCIBounds` to additive formula: `upper = Math.min(1.0, score + halfWidth)`, `lower = Math.max(0.0, score - halfWidth)`.
2. Remove `ci_upper` from `CompositeChartSVG` yDomain values — scale y-axis to trajectory range only; CI bands clip at chart boundary (acceptable for semi-transparent fills).
3. Verify `CI_BAND_OPACITY = 0.12` and `CI_BAND_OPACITY_MODE3 = 0.05` are applied correctly in the SVG path. (The SVG path currently hard-codes `opacity={0.10}` at lines 542 and 557 — this should use the exported constants.)

**ADR impact:** Bug fix within ADR-007 spec — no ADR amendment required.

---

## Root Cause 2 — Zone 1B height budget insufficient; DistributionalComparisonSummary clips at Zone 1C boundary

**Findings:** DEMO-133 (CRITICAL), DEMO-131 (CRITICAL), DEMO-141 (HIGH cascade)
**File:** `frontend/src/components/MDAAlertPanelZone1B.tsx`
**Cluster:** B

### Finding

`DistributionalComparisonSummary` renders with `position: sticky; bottom: 0` inside `CohortImpactSection`'s scroll container (`overflowY: auto`, `flex: "1 1 0"`, line 856). Sticky-bottom within an overflow-auto container attaches to the **scroll container's bottom**, not the viewport bottom. At 1440×900, Zone 1B's total flex allocation is insufficient to render the full `DistributionalComparisonSummary` row above the Zone 1C boundary.

Contributing factor: `MDAAlertPanelZone1B` renders first in Zone 1B DOM order, followed by `CohortImpactSection` (which contains `DistributionalComparisonSummary`). When `sorted[0]` (topAlert) is a TERMINAL alert, it occupies maximum vertical space at the top of Zone 1B — pushing `CohortImpactSection` and therefore `DistributionalComparisonSummary` below the visible boundary (DEMO-141 headline hierarchy inversion).

For Zone 3 panel expansion (DEMO-131): `panelOpen && summary.methodology_detail && (...)` renders a `<div>` with four content rows inside `DistributionalComparisonSummary`. This content renders below the sticky-bottom panel within the scroll container — but if the container itself is clipped at Zone 1C boundary and has insufficient height to scroll, the content is simply not visible. The 4-byte Frame D/E difference confirms only the toggle glyph changed (`▶` → `▼`), not the content visibility.

### Fix

1. **Zone 1B DOM reorder:** Render `DistributionalComparisonSummary` first in Zone 1B (above MDA alerts and cohort rows) for comparison sessions. This implements human cost parity: the distributional finding is the primary Act 2 surface, not a secondary element beneath financial alerts. The TERMINAL alert moves below.
2. **Zone 1B minimum height:** Specify an explicit `minHeight` for Zone 1B that guarantees the full `DistributionalComparisonSummary` (six content elements: number, CI bounds, 95% CI marker, direction-stability, T3 badge, reference label) is visible at 1440×900 without scroll. Derived constraint: at least 160px for the summary row alone.
3. **Zone 3 expanded panel:** Add `scrollIntoView({ block: "nearest" })` on the panel content container after `setPanelOpen(true)`. Also ensure Zone 3 expanded panel has its own `overflowY: auto` if content exceeds Zone 1B height.

**ADR impact:** ADR-008 amendment required to add Zone 1B minimum height specification and Zone 1B DOM ordering rule for comparison sessions. Architect Agent determination: **AMENDMENT REQUIRED**. UX Designer sign-off required before Cluster B implementation PR opens.

---

## Root Cause 3 — CohortImpactSection is an alert-only surface; cleared thresholds are invisible

**Findings:** DEMO-134 (CRITICAL), DEMO-140 (HIGH)
**File:** `frontend/src/components/MDAAlertPanelZone1B.tsx` (lines 844–955)
**Cluster:** C

### Finding

`CohortImpactSection` renders only from `crossings` — the `cohort_threshold_crossings` Zustand store field. The store populates this array only for indicators that have **crossed** a threshold. The Demo 7 Act 1 narrative is constructed around a **cleared threshold** finding: "the bottom quintile informal workers poverty headcount remains at 0.450 — ten points above the 0.40 recovery floor."

At step 6 with the counter-proposal branch active, the informal workers threshold is NOT crossed — it is the finding of safety that Act 1 is designed to demonstrate. But `crossings` contains only the two cohorts that DID breach (agricultural workers, formal sector workers at step 1). The informal workers row — the designated focal indicator — is simply absent.

DEMO-140 (temporal contradiction): The two CRITICAL rows in `crossings` display `crossing.severity = "CRITICAL"` in red with `Threshold crossed at step 1`. At step 6, this historical breach is shown with the same visual weight as a current-step violation. The `headerLabel` only switches to `"COHORT IMPACT (HISTORICAL)"` when `isCompleted=true` — not when the current step is beyond the historical crossing step.

### Fix

1. Add **monitored row state** to `CohortImpactSection`: the store (or API) designates certain indicators as "monitored focal" for the current scenario. These render at every step regardless of breach status, showing current value, recovery floor, T3 badge, and a "CLEAR" or "BREACHED" state indicator. For Demo 7, the monitored focal indicator is `bottom_quintile_informal_workers_poverty_headcount` with floor 0.40.
2. **Temporal scope disambiguation** (DEMO-140): Use amber (`#a06000`) for historical breaches (step < current step) rather than red. Prefix historical rows with "Breached at step N —" to make temporal scope explicit. Reserve red `CRITICAL` for current-step violations.

**ADR impact:** Adding monitored-row state constitutes a new instrument behavior not covered by ADR-010's current spec. **ADR-010 amendment required.** UX Designer sign-off required on monitored-row design before Cluster C implementation PR opens.

---

## Root Cause 4 — Act 1 mock trajectory missing psp_dominant_driver; HCL indicator key mismatch

**Findings:** DEMO-132 (CRITICAL), DEMO-143 (HIGH)
**Files:** `frontend/tests/e2e/demo-narrated.spec.ts`, `frontend/src/components/FourFrameworkZone1D.tsx`, `frontend/src/components/ScenarioInstrumentCluster.tsx`
**Cluster:** D

### DEMO-132: psp-driver-row absent

`FourFrameworkZone1D.tsx` line 556 renders `psp-driver-row` only when:
```tsx
{pspDominantDriver != null && DRIVER_LABELS[pspDominantDriver] && (...)}
```

`ScenarioInstrumentCluster.tsx` line 646 sets this state:
```tsx
setPspDominantDriver(entry.psp_dominant_driver ?? null);
```

The Act 1 Playwright mock (`makeAct1BaselineMock` and `makeAct1BranchMock` in `demo-narrated.spec.ts`) includes the `political_economy` framework with:
```js
indicators: {
  programme_survival_probability: { value: "0.58", ... }
}
```

No `psp_dominant_driver` field. When the mock is fulfilled, `entry.psp_dominant_driver` is `undefined → null`, so `pspDominantDriver` state is always null, and the row never renders. The backend implementation is correct (see `schemas.py:188`, `module.py:229`, `scenarios.py:2668`) — the mock simply doesn't model the field.

**Fix:** Add `psp_dominant_driver: "fiscal_sustainability"` to `programme_survival_probability` in both `makeAct1BaselineMock` and `makeAct1BranchMock` at all steps ≥ `BRANCH_FROM_STEP`. Verify `ScenarioInstrumentCluster` reads the field from the correct location in the trajectory response (the extraction at line 2652 in `scenarios.py` reads from programme_survival_update event metadata, not from framework indicators — check whether `ScenarioInstrumentCluster`'s extraction path at line 641 matches the actual API response shape for this field).

### DEMO-143: Human Cost Ledger bottom quintile em dash

The SEN and ZMB scenario `initial_attributes` in `demo-narrated.spec.ts` include `poverty_headcount_ratio` but not a cohort-level `bottom_quintile_informal_workers_poverty_headcount` attribute. The HCL component reads the cohort-specific indicator key. If the backend doesn't derive the cohort-level indicator from `poverty_headcount_ratio`, the field is unpopulated and the HCL shows `—`.

**Fix:** Verify the backend's cohort indicator API for both SEN and ZMB scenarios at each step populates `bottom_quintile_informal_workers_poverty_headcount`. If the backend derives this from `poverty_headcount_ratio` (expected behavior), determine why the derived indicator isn't populating. If it requires an explicit `initial_attributes` entry, add it to both `createSenScenario` and `createZMBScenario` in `demo-narrated.spec.ts`.

**ADR impact:** None — both are data pipeline / mock fixture fixes.

---

## Root Cause 5 — Screenshot capture sequence: Frames A and B captured at same step; Frame C at wrong step; choropleth not centered

**Findings:** DEMO-130 (CRITICAL), DEMO-135 (CRITICAL), DEMO-136 (CRITICAL), DEMO-139 (HIGH)
**File:** `frontend/tests/e2e/demo-narrated.spec.ts`
**Cluster:** E

### DEMO-130 + DEMO-135 + DEMO-136: Frame capture step misalignment

The spec creates the SEN scenario and pre-advances it to `BRANCH_FROM_STEP = 3`. Frame A is captured immediately after branch trajectory renders (same UI state as step 3). Frame B is captured after a narration speech (no step advance) — same state as Frame A → byte-for-byte identical (DEMO-130). Frame C is captured at step 6 (three `nextStep` clicks from step 3), but Step 5d confirmed maximum divergence at step 8 — branch delta at step 6 is 0.00 because the divergence dissipates by step 6 in the mock trajectory values (DEMO-136).

The mock branch trajectory computes `composite_score = 0.51 - i * 0.003 + 0.04` for financial (branched), `0.51 - i * 0.003` for baseline. At step i=5 (step_index=6): branch = 0.51 - 0.015 + 0.04 = 0.535; baseline = 0.51 - 0.015 = 0.495. Delta = +0.04. This is NOT zero — the DEMO-136 finding that Frame C shows "Branch: 0.49, 0.00 (green)" implies either the display is computing delta from the wrong baseline step or the mock values aren't matching.

More likely cause for DEMO-136: Zone 1D displays the **composite** across frameworks (financial + HD + governance). The HD composite at step 5 is: branch = 0.44 + 0.010 + 0.02 = 0.470; baseline = 0.44 + 0.010 = 0.450. Financial branch = 0.535; baseline = 0.495. The composite means are each averaged. If governance (0.55) dominates, the composite delta might be small. However, Step 5d specified max divergence at step 8 — so the correct fix is to capture Frame A AND Frame C at step 8 (consistent with the step 5d panel guidance).

**Fix:**
1. Advance to step 8 before Frame A screenshot (three more `nextStep` clicks beyond step 6 loop).
2. Frame B: capture at step 3 (before advancing further to step 8) — this provides natural distinction from Frame A without any code complexity.
3. Frame C: capture at step 8 (same as Frame A) — at maximum divergence, Zone 1D shows the branch/baseline delta at its peak.

Corrected capture sequence in spec:
```
Step 3: Apply policy input → Frame B ("the uncertainty envelope", PSP driver visible)
Step 3→8: Advance 5 more steps
Step 8: Frame A ("the instrument", maximum divergence)
Step 8: Frame C ("the Act 1 finding", Zone 1B cohort section)
```

### DEMO-139: Choropleth centered on North America

In `demo-narrated.spec.ts`, after navigation to ZMB Option C (`page.goto(/?scenario=${zmbCId})`), no explicit choropleth pan/center command is issued. The choropleth retains its last pan state (centered on North America from app initialization or prior navigation).

**Fix:** After ZMB navigation and before Frame D capture, add:
```ts
await page.evaluate(() => {
  const fn = (window as Record<string, unknown>).__worldsim_centerOnEntity as ((id: string) => void) | undefined;
  if (fn) fn('ZMB');
});
await page.waitForTimeout(800); // allow pan animation
```

**ADR impact:** Spec/doc fixes only — no ADR impact.

---

## Remaining MEDIUM/LOW findings — disposition

Per EL note 2 in G7 sprint entry, all MEDIUM/LOW findings require explicit disposition.

| DEMO | Severity | Disposition | Rationale |
|---|---|---|---|
| DEMO-142 | HIGH | **G7 Cluster E, first fix** | "Policy Malevolent Margin" jargon — BPO escalated to operational priority; must fix before any screenshot recapture. Replace display label in `DistributionalComparisonSummary`. |
| DEMO-144 | HIGH | **G7 Cluster E** | Update walkthrough value from "340,000" to "approximately 342,700" + presenter note to read exact figure from screen. |
| DEMO-146 | MEDIUM | **G7 Cluster E, first doc fix** | Screenshot Reference table filenames. BPO escalated. Update walkthrough table. |
| DEMO-147 | MEDIUM | **G7 Cluster E — determination needed** | T3→T4 tier degradation step 3→6. Root cause analysis: the mock trajectory assigns T3 to all steps. The degradation observed in screenshots implies the real backend assigns T4 at step 6. Determination: if T4 at step 6 is the BandingEngine step-depth rule (intended), add one acknowledgment sentence to Frame C narration. If it's a bug, fix tier propagation. Determination at G7-0 EL review. |
| DEMO-148 | MEDIUM | **G7 Cluster E** | Eight NARRATION-RULING-1 transitions. Priority: Frame C→D act-break. Add eight transition sentences. |
| DEMO-149 | MEDIUM | **G7 Cluster B** | Zone 1D PSP section clipped by governance horizon disclosure text. Fix: governance horizon note as tooltip disclosure in Act 2 frames, or reduce font size. |
| DEMO-150 | MEDIUM | **Enhancement gap → M19 scope** | Ecological module explicitly disabled in both SEN and ZMB configs (`ecological: { enabled: false }`). The `—` is expected; display should say "Not modelled" rather than `—`. Trivial display fix acceptable in G7 Cluster D. Module output itself is M19 scope. |
| DEMO-151 | MEDIUM | **Enhancement gap → M19 scope** | HD trajectory absent from Zone 1A in Mode 1/2 comparison mode. Root cause: Zone 1A composite path shows multi-scenario composite means (not per-framework). Adding a separate HD trajectory in Zone 1A for Mode 3 is a meaningful UX enhancement but not required for Demo 7. M19 scope. |
| DEMO-152 | LOW | **G7 Cluster E — presenter note** | Breadcrumb shows "OptionC". Add presenter note: "Breadcrumb shows the reference scenario — all three are loaded." No code change needed. |
| DEMO-153 | LOW | **G7 Cluster E** | Add one sentence to Act 1 narration with people-count translation for the 0.40 floor. |

---

## ADR determinations

| Fix cluster | ADR impact | Determination | Gate |
|---|---|---|---|
| A — CI band geometry | **None** | Bug fix within ADR-007 `computeCompositeCIBounds` spec | CLEAR |
| B — Zone 1B layout | **ADR-008 amendment required** | Zone 1B minimum height + DOM order for comparison sessions constitutes new layout constraint not in current ADR-008 | BLOCKED pending ADR-008 amendment acceptance + UX Designer sign-off |
| C — CohortImpactSection monitored-row | **ADR-010 amendment required** | Monitored-row state is a new instrument behavior: designated focal indicators visible regardless of breach status. Not currently specified in ADR-010. | BLOCKED pending ADR-010 amendment acceptance + UX Designer sign-off |
| D — Data pipeline | **None** | Mock fixture update + backend indicator key fix | CLEAR |
| E — Capture/narration/labels | **None** | Spec, walkthrough doc, and component label fixes | CLEAR |

---

## Cross-cutting pattern

Reading across the five root causes, a single structural gap recurs: **contract completeness between the demo spec and component contracts**.

- DEMO-132: the mock doesn't include a field (`psp_dominant_driver`) that the component requires.
- DEMO-130/135/136: the spec captures screenshots at steps that don't match the contract established by the Step 5d panel.
- DEMO-134: the component has no contract for non-breaching focal indicators.
- DEMO-137: the math formula doesn't match the `[mean ± halfWidth]` contract stated in the ADR-007 spec.
- DEMO-133/131: the Zone 1B layout has no explicit height-budget contract to guarantee visibility.

The systematic fix is to add **contract-level acceptance tests** before implementation (the QA-first gate). Tests that assert `psp-driver-row` is visible, that `frame-a` and `frame-b` MD5s differ, that `distributional-comparison-summary` is fully in-viewport at 1440×900 — these would have caught every CRITICAL finding before the G6 screenshot capture ran. The QA authorship gate in G7 is the structural response to this pattern.

NM-082 (filed at G6 exit) covers the CI geometry finding. DEMO-132 through DEMO-136 collectively point to a **demo-spec ↔ component-contract** integration gap that should be added to the NM registry as NM-083 if the EL determines the pattern is novel enough to warrant a separate near-miss entry beyond NM-082.

---

## Sequencing recommendation

Implement clusters in this order to minimize re-work:

1. **Cluster E first** (DEMO-142 label fix): Do this before any screenshot recapture so the jargon exposure is gone before new frames are taken.
2. **Cluster D** (psp-driver-row mock + HCL indicator): Data pipeline fixes that recapture will demonstrate.
3. **Cluster A** (CI band geometry): Fix before recapture so zones scale correctly.
4. **Cluster B** (after ADR-008 amendment accepted): Zone 1B layout — ADR gate must clear first.
5. **Cluster C** (after ADR-010 amendment accepted): Monitored-row state — ADR gate must clear first.
6. **Cluster E remainder** (capture sequence + narration): After all code fixes confirmed, re-run `demo-narrated.spec.ts` to recapture all five frames; then update walkthrough with actual values.

---

## EL sign-off required

This document must be reviewed and signed off by EL before any fix intent documents are authored. Per the G7 sprint entry, EL sign-off on G7-0 is the gate that unlocks intent document authorship for all clusters.

**EL sign-off block:**

| Field | Value |
|---|---|
| Reviewing | EL (@PublicEnemage) |
| Date | ___ |
| DEMO-147 determination | T3→T4 at step 6: [intentional / bug] |
| NM-083 call | [File as new NM / Absorb under NM-082] |
| Cluster B ADR-008 amendment | [Confirm required / Waive] |
| Cluster C ADR-010 amendment | [Confirm required / Waive] |
| DEMO-150 display fix in G7 | [Include in Cluster D / Defer to M19] |
| DEMO-151 | [Confirmed M19 scope] |
| Sign-off verdict | [APPROVED / APPROVED WITH NOTES / REVISION REQUIRED] |
