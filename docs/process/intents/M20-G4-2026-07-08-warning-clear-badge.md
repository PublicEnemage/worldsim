---
name: M20-G4-warning-clear-badge
type: implementation-intent
adr: N/A — enhancement to existing CohortImpactSection focal row display (Zone 1B)
issues: "#1775, DEMO-233"
status: Filed
authored-by: PM Agent
authored-date: 2026-07-08
implementing-agent: Frontend Architect Agent
sprint-entry: docs/process/sprint-plans/m20-g4-sprint-entry.md
---

# Implementation Intent: G4 — WARNING Badge Alongside CLEAR (#1775 / DEMO-233)

## 1. Source Issue and Architecture Authority

**Finding:** DEMO-233 Medium — Demo 8 audience simulation Step 6c (Aicha Mbaye, Persona 5).
Confirmed by stakeholder Q2: "Can I see both the CLEAR badge and a warning if the margin
is narrow?"

**Problem:** When the focal cohort indicator is above its MDA floor, the
`focal-cohort-row` displays a CLEAR badge (green). No additional signal is shown when
the indicator is close to — but not past — the floor. A constraint-floor boundary of 0.83
can represent very different risk profiles depending on whether the indicator is at 0.90
(comfortably CLEAR) or at 0.831 (barely CLEAR, one adverse step from breaching). The
current display treats both identically.

**Architecture authority:** `CohortImpactSection` in `MDAAlertPanelZone1B.tsx`.
The focal row state logic (line 905–906) computes `state: "CLEAR" | "CRITICAL" | "UNKNOWN"`.
The fix adds a margin-narrowness check alongside the CLEAR state — it does not modify
the CRITICAL or UNKNOWN paths. The `FOCAL_BADGE_COLOR` map (line 862–866) is extended
for the WARNING case.

**Margin threshold:** `above_floor_pct < 0.05` defines "narrow margin" — i.e. the
indicator is within 5% of the floor value (`(numValue - floor_value) / floor_value < 0.05`).
This mirrors the WARNING severity threshold already used in `cohort_threshold_crossings`
(`crossing.severity = "WARNING"`). Using the same threshold maintains internal
consistency.

**Authored by:** PM Agent  
**Date:** 2026-07-08  
**Implementing agent:** Frontend Architect Agent

---

## 2. Persona Trace Elements Targeted

**P-1 — Persona served:**
Primary: Persona 5 (Aicha Mbaye, Community Resilience practitioner) — raised DEMO-233:
"Can I see both the CLEAR badge and a warning if the margin is narrow?" Aicha is the
persona who needs to understand whether a CLEAR result is confident or fragile.

Secondary: Persona 2 (Eleni, Ministry of Finance analyst) — presenting the constraint
result to creditors. "CLEAR with narrow margin" is a different claim than "CLEAR" —
it changes the negotiating stance (requesting a wider buffer vs claiming safety).

**P-2 — Entry state:**
Mode 3 Active Control. Constraint-floor search has returned FOUND. Zone 1B
`CohortImpactSection` is visible with at least one focal cohort row showing CLEAR
state. The indicator value is above the floor but within 5%.

**P-3 — Journey step:**
Scenario Exploration / Community Impact Assessment. Aicha has seen the CLEAR badge
and is asking: "Is this CLEAR comfortable, or is it on the edge?" She cannot tell
from the current display.

**P-4 — Time/interaction ceiling:**
Zero additional interaction — the WARNING badge alongside CLEAR must be visible
immediately when the focal cohort row is rendered with narrow margin. No hover or
click required to surface the signal.

**P-6 — Negotiating leverage delivered:**
Persona 2 (Eleni) can tell creditors: "The indicator clears the floor, but the margin
is narrow — we are requesting a 7% buffer, not a 5% one, because a single adverse
step would breach." The WARNING badge makes this claim visually auditable.

**P-7 — North star capability delivered:**
A Zambian finance ministry analyst can see, in a single glance at Zone 1B, whether
a CLEAR result represents a comfortable margin or a fragile one — and can cite the
narrow margin in a programme review without requiring the IMF team to extract the
raw numbers from the detail panel.

---

## 3. Observable Application State

### 3.1 — Focal row display: CLEAR with comfortable margin

When `numValue > focal.floor_value` AND `(numValue - focal.floor_value) / focal.floor_value ≥ 0.05`:

```
data-testid="focal-cohort-row"
  ├── data-testid="focal-badge"           text: "CLEAR"   background: #2e7d32 (green)
  └── (no warning badge)
```

Behaviour unchanged from current implementation.

### 3.2 — Focal row display: CLEAR with narrow margin (NEW)

When `numValue > focal.floor_value` AND `(numValue - focal.floor_value) / focal.floor_value < 0.05`:

```
data-testid="focal-cohort-row"
  ├── data-testid="focal-badge"           text: "CLEAR"   background: #2e7d32 (green)
  ├── data-testid="focal-warning-badge"   text: "WARNING" background: #a06000 (amber)
  └── (indicator value and floor display unchanged)
```

Both badges visible simultaneously in the focal row, in-line with the indicator label.

### 3.3 — Focal row display: CRITICAL (unchanged)

When `numValue ≤ focal.floor_value`:
```
data-testid="focal-cohort-row"
  ├── data-testid="focal-badge"   text: "CRITICAL"   background: #c62828 (red)
  └── (no warning badge)
```
Unchanged.

### 3.4 — Margin computation

`above_floor_pct = (numValue - floor_value) / floor_value`

Where:
- `numValue` = current indicator value at the active step (already computed in `focalRows`)
- `floor_value` = `focal.floor_value`

The `above_floor_pct < 0.05` check is computed at render time from existing data.
No new API fields required — all values are available in `currentStepData` and
`monitoredFocalCohorts`.

### 3.5 — Silent failure detection

**SF-1 (WARNING badge absent when margin is narrow):** `numValue` is within 5% of
`floor_value` but `focal-warning-badge` is not rendered. Detection: assert
`focal-warning-badge` is present when `(numValue - floor_value) / floor_value < 0.05`
and state is CLEAR.

**SF-2 (WARNING badge present when margin is not narrow):** `focal-warning-badge` is
rendered even when the margin is ≥ 5%. Detection: assert `focal-warning-badge` is
absent when `above_floor_pct ≥ 0.05`.

**SF-3 (WARNING badge present in CRITICAL state):** The margin check fires for
sub-floor values. Detection: assert `focal-warning-badge` is absent when `state ===
"CRITICAL"` (below floor — the concept of margin does not apply).

---

## 4. Acceptance Criteria

**AC-1 (CLEAR + WARNING — narrow margin):**
When a focal cohort row is in CLEAR state and `(numValue - floor_value) / floor_value < 0.05`,
then `data-testid="focal-warning-badge"` is present within `data-testid="focal-cohort-row"`
and has text content `"WARNING"`.

**AC-2 (CLEAR only — comfortable margin):**
When a focal cohort row is in CLEAR state and `(numValue - floor_value) / floor_value ≥ 0.05`,
then `data-testid="focal-warning-badge"` is absent from the focal row.

**AC-3 (CRITICAL — no warning badge):**
When a focal cohort row is in CRITICAL state (numValue ≤ floor_value), then
`data-testid="focal-warning-badge"` is absent.

**AC-4 (CLEAR badge unchanged — regression):**
`data-testid="focal-badge"` still shows `"CLEAR"` (text and color) when state is CLEAR
with narrow margin. The WARNING badge is additive; it does not replace the CLEAR badge.

**AC-5 (boundary case — exactly 5%):**
When `above_floor_pct === 0.05` exactly, `focal-warning-badge` is absent (< 0.05 is
the threshold, not ≤ 0.05). This boundary case makes the threshold unambiguous.

**AC-6 (SF-1 guard):**
For a focal row with `numValue = floor_value * 1.03` (3% above floor), assert
`focal-warning-badge` is present.

**AC-7 (SF-2 guard):**
For a focal row with `numValue = floor_value * 1.10` (10% above floor), assert
`focal-warning-badge` is absent.

**AC-8 (SF-3 guard):**
For a focal row with `numValue = floor_value * 0.97` (below floor — CRITICAL state),
assert `focal-warning-badge` is absent.

---

## 4b. Visual Spec (before/after)

**Focal row — CLEAR, comfortable margin (before and after — unchanged):**
```
Zone 1B | data-testid="focal-cohort-row"

[CLEAR]  q1_poverty_headcount_ratio — 20% MDA floor
         0.156 / floor 0.200
```

**Focal row — CLEAR, narrow margin (before):**
```
Zone 1B | data-testid="focal-cohort-row"

[CLEAR]  q1_poverty_headcount_ratio — 20% MDA floor
         0.193 / floor 0.200                ← 3.5% above floor, but no visual signal
```

**Focal row — CLEAR, narrow margin (after):**
```
Zone 1B | data-testid="focal-cohort-row"

[CLEAR] [WARNING]  q1_poverty_headcount_ratio — 20% MDA floor
                   0.193 / floor 0.200
```

Badge colors: CLEAR = #2e7d32 (green, existing), WARNING = #a06000 (amber, consistent
with HIST row color and Warning severity in `COHORT_SEVERITY_COLOR`).

---

## 5. Kryptonite Constraint Check

**Does this implementation's primary observable state require specialist mediation for
Persona 5 to act on it in the Reactive entry state (zero interaction ceiling)?**

`[x]` No — "WARNING" alongside "CLEAR" is interpretable by a community practitioner
without statistical training. The combination reads as: "we cleared the threshold, but
we're close." No mediating explanation required to act on this signal.

**Rationale:** The WARNING badge uses established UX vocabulary (warning = proceed with
caution). Persona 5 understands CLEAR (safe) and WARNING (caution) without needing
to know the 5% threshold definition. The raw numbers (`0.193 / floor 0.200`) are
available in the row for those who want the precise distance.

---

## 6. Out of Scope

- **Margin percentage display:** Showing the exact `above_floor_pct` value in the focal
  row (e.g. "3.5% above floor") is out of scope. The raw values are already shown
  (`numValue / floor floor_value`). A percentage label is a separate UX enhancement.
- **Configurable threshold:** The 5% threshold is hardcoded. A configuration UI for
  the margin threshold is out of scope for G4.
- **WARNING badge on crossing rows:** The `renderCrossingRow` function already uses
  `crossing.severity` (WARNING/CRITICAL/WATCH) from the API — those rows are unchanged.
  This deliverable affects only focal rows (rows computed from `monitoredFocalCohorts`).
- **UNKNOWN state warning:** When state is UNKNOWN (no value available), no WARNING
  badge is shown. The UNKNOWN case is already handled and unchanged.
- **Backend changes:** No backend changes required — all data needed is already
  available in the existing trajectory response.

---

## 7. Test Authorship Obligation

**QA Lead:** QA Lead Agent  
**Test authorship deadline:** Before any G4 implementation PR opens on `sprint/m20-g4`  
**Test file location:** `frontend/tests/e2e/m20-g4-warning-clear-badge.spec.ts`

**Required test coverage (Playwright E2E):**

- **AC-1:** Mock focal cohort with `numValue = floor_value * 1.03`; assert
  `focal-warning-badge` present with text "WARNING".
- **AC-2:** Mock focal cohort with `numValue = floor_value * 1.10`; assert
  `focal-warning-badge` absent.
- **AC-3:** Mock focal cohort with `numValue = floor_value * 0.97` (CRITICAL); assert
  `focal-warning-badge` absent.
- **AC-4 (regression — CLEAR badge):** With narrow margin (AC-1 setup), assert
  `focal-badge` text is still "CLEAR" (WARNING is additive, not replacing).
- **AC-5 (boundary):** Mock `numValue = floor_value * 1.05` exactly; assert
  `focal-warning-badge` absent (< 0.05 threshold, not ≤).
- **AC-6 (SF-1 guard):** Same as AC-1 — explicit assertion. Write as a separate block.
- **AC-7 (SF-2 guard):** Same as AC-2 — explicit assertion. Write as a separate block.
- **AC-8 (SF-3 guard):** Same as AC-3 — explicit assertion. Write as a separate block.

**QA Lead acknowledgment:**
`[ ]` QA Lead: Tests for AC-1 through AC-8 authored and filed before first implementation PR.

---

*Intent document version: 2026-07-08. Sprint entry: `docs/process/sprint-plans/m20-g4-sprint-entry.md`.
See `docs/process/agent-execution-lifecycle.md` for the five-step lifecycle this document gates.*
