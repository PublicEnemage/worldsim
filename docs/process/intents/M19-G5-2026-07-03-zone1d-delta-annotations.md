---
name: M19-G5-zone1d-delta-annotations
type: implementation-intent
adr: ADR-017 §Zone 1D Integration (Mode 3) — per-framework delta annotations (required companion)
issues: "#1630"
status: Filed
authored-by: PM Agent
authored-date: 2026-07-03
implementing-agent: Frontend Architect Agent
sprint-entry: docs/process/sprint-plans/m19-g5-sprint-entry.md
---

# Implementation Intent: G5 — Zone 1D Delta Annotations (Mode 3) (#1630)

## 1. Source Issue and Architecture Authority

**Issue:** #1630 — Demo 8 Act 1 narration implies separate HD line in Zone 1A — Mode 3
renders single composite only
**ADR authority:** ADR-017 §Zone 1D Integration (Mode 3) — this deliverable is the
implementation of a required companion mandated in ADR-017, not a new design decision.
**Authored by:** PM Agent
**Date:** 2026-07-03
**Implementing agent:** Frontend Architect Agent

**Background (Architect panel finding, 2026-07-03):**
ADR-017 §Zone 1D Integration (Mode 3) states:

> *"In Mode 3, Zone 1D must display delta annotations per framework row showing the
> divergence from baseline at the current step: `Financial: 0.71 (+0.04 vs baseline)`."*
>
> *"Phase 4 implementation of Zone 1D delta annotations is a required companion to the
> Zone 1A composite encoding — implementing Zone 1A composite without Zone 1D delta
> annotations removes per-framework information without providing a substitute. This is
> a silent failure mode."*

These delta annotations were mandated by ADR-017 (accepted 2026-06-22) but never
implemented. `FourFrameworkZone1D.tsx` currently has no `baseline` prop and no
`(+Δ vs baseline)` display.

The Demo 8 Act 1 narration issue (#1630 original) says "the human development composite
is higher at every step from three onward" — implying a per-framework signal that is
not visible in Zone 1A (composite-only) or Zone 1D (no delta annotations). The correct
fix is to implement the ADR-017-mandated Zone 1D delta annotations, then update the
narration to reference Zone 1D.

**EL decision (Path B, 2026-07-03):** Implement Zone 1D delta annotations per ADR-017.

---

## 2. Scope

**What changes:**

**Deliverable A — `FourFrameworkZone1D` Mode 3 delta annotations**
`FourFrameworkZone1D.tsx`: add a `baselineFrameworkScores` prop (see below) and render
`(+Δ)` annotation next to each framework score row when in Mode 3 and baseline data is
available.

Display format (per ADR-017 §Zone 1D Integration example):
```
Financial:          0.71 (+0.04)
Human Development:  0.62 (+0.07)
Ecological:         0.58 (+0.01)
Governance:         0.51 (±0.00)
```

Annotation rules:
- Positive delta: green `(+N.NN)` — framework improved vs. baseline
- Negative delta: amber/warning `(−N.NN)` — framework declined vs. baseline
- Zero/near-zero (|Δ| < 0.005): gray `(±0.00)` — no meaningful change
- Annotation absent: when `baselineFrameworkScores` prop is null/undefined, or when
  `mode !== "MODE_3"`, the delta is not shown (no change to Mode 1/2 display)

**Deliverable B — Pass baseline framework scores from caller**
The component that renders `FourFrameworkZone1D` in Mode 3 (identified in §4 below)
must extract the per-framework composite scores from the baseline trajectory at the
`current_step` index and pass them as `baselineFrameworkScores`.

**Deliverable C — Narration update**
`frontend/tests/e2e/demo-narrated.spec.ts` line ~892: update the Act 1 narration line
to reference Zone 1D rather than implying Zone 1A per-framework lines. The narration
must accurately describe what is rendered. Example corrected narration:

> *"And Zone 1D shows the human development dimension up from its baseline at every
> step from three onward."*

(Exact wording is the implementing agent's choice; it must reference Zone 1D explicitly
and must be consistent with what Zone 1D renders after Deliverable A is implemented.)

**What does NOT change:**
- Zone 1A rendering (CompositeChartSVG — composite-only per ADR-017)
- Any backend code
- Any other Zone 1A/1B/1C behavior

---

## 3. Acceptance Criteria

**AC-1 — Zone 1D delta annotations in Mode 3 (primary)**
When `FourFrameworkZone1D` is rendered in Mode 3 with baseline data available, each
framework row displays a `(+Δ)` annotation next to the current-step score.

**Observable state (data-testid targets):**
- `data-testid="framework-delta-financial"` — shows `(+0.04)` or `(−0.02)` or `(±0.00)`
  depending on delta magnitude and sign
- `data-testid="framework-delta-human_development"` — similarly
- `data-testid="framework-delta-ecological"` — similarly
- `data-testid="framework-delta-governance"` — similarly

**AC-2 — Delta absent in Mode 1/2**
When `mode` is `"MODE_1"` or `"MODE_2"`, or when `baselineFrameworkScores` prop is null,
no delta annotation elements are rendered.

**Observable state:** `data-testid="framework-delta-financial"` element is absent from
the DOM in Mode 1/2.

**AC-3 — Color coding**
- Positive delta (Δ > 0.005): text color `#16A34A` (green — improvement)
- Negative delta (Δ < −0.005): text color `#D97706` (amber — decline matches warning tone)
- Near-zero (|Δ| ≤ 0.005): text color `#9CA3AF` (gray — no change)

**AC-4 — Narration accuracy**
`demo-narrated.spec.ts` Act 1 narration contains no text that implies a separate HD line
in Zone 1A. The narration referencing human development trajectory direction must reference
Zone 1D (not Zone 1A).

**Observable state:** Playwright narration test passes without the "HD line implied but
not rendered" issue that would fail audience scrutiny.

**AC-5 — Mode 1/2 regression**
Existing E2E and unit tests for `FourFrameworkZone1D` pass without modification (delta
feature is additive; Mode 1/2 display is unchanged).

---

## 4. File-Level Change Plan

| File | Change | Why |
|---|---|---|
| `frontend/src/components/FourFrameworkZone1D.tsx` | Add `baselineFrameworkScores?: Record<string, number \| null>` prop to `FourFrameworkZone1DProps`; add delta computation and `(+Δ)` annotation spans in framework score rows, gated on `mode === "MODE_3" && baselineFrameworkScores != null` | Deliverable A |
| `frontend/src/components/ScenarioInstrumentCluster.tsx` (or wherever `FourFrameworkZone1D` is called in the Mode 3 flow) | Extract per-framework composite scores from `baseline_trajectory.steps[currentStepIndex].frameworks`; pass as `baselineFrameworkScores` to `FourFrameworkZone1D` | Deliverable B |
| `frontend/tests/e2e/demo-narrated.spec.ts` | Update Act 1 narration line ~892 to reference Zone 1D instead of implying Zone 1A HD line | Deliverable C |
| `frontend/tests/e2e/m19-g5-zone1d-delta-annotations.spec.ts` | New E2E test for AC-1 through AC-5 | QA gate |
| `frontend/src/components/__tests__/FourFrameworkZone1D.test.ts` | Add unit test cases for Mode 3 delta display; assert delta annotation testids, color coding, and Mode 1/2 absence | QA gate (unit) |

**Implementing agent must first:**
1. `grep -n "FourFrameworkZone1D" frontend/src/components/ScenarioInstrumentCluster.tsx`
   to confirm the call site and understand what trajectory data is available
2. Verify `baseline_trajectory.steps[stepIndex].frameworks[key].composite_score` is the
   correct field name (read `docs/schema/simulation_state.yml` first per CLAUDE.md schema
   read requirement)

---

## 5. QA Notes (NM-086 compliance)

This deliverable reads existing trajectory data — no new API calls introduced. The
`FourFrameworkZone1D` component already receives trajectory data via its caller; the
change only adds a new prop passing baseline framework scores already in scope.

**NM-086 check:** No new E2E mock routes introduced. If the E2E test for AC-1 uses a
mock trajectory response, the mock must include `frameworks[key].composite_score` fields
in both active and baseline trajectory objects — verify these exist in `api_contracts.yml`
§trajectory.steps[].frameworks before authoring the mock.

---

## 6. Visual Spec (before / after)

**Before (current Mode 3 Zone 1D):**
```
Financial           0.71
Human Development   0.62
Ecological          0.58
Governance          0.51
```

**After (Mode 3 Zone 1D with delta annotations):**
```
Financial           0.71  (+0.04)   ← green
Human Development   0.62  (+0.07)   ← green
Ecological          0.58  (+0.01)   ← green
Governance          0.51  (±0.00)   ← gray
```

Delta annotation is placed to the right of the framework score, same row, smaller font
(9px), aligned right within the row or after a fixed-width spacer. Color per AC-3.
