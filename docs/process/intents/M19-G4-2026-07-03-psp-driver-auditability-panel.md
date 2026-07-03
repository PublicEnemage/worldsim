---
name: M19-G4-psp-driver-auditability-panel
type: implementation-intent
adr: ADR-019 (Zone 1D scope — control plane column) + ADR-015 §Component 3 (PSP row)
issues: "#1528"
status: Filed
authored-by: PM Agent
authored-date: 2026-07-03
implementing-agent: Frontend Architect Agent
sprint-entry: docs/process/sprint-plans/m19-g4-sprint-entry.md
---

# Implementation Intent: G4 — PSP Driver Arc + In-Viewport Auditability Panel (#1528)

## 1. Source Issue and Architecture Authority

**Issue:** #1528 — feat(zone1d): PSP driver methodology disclosure panel — in-viewport auditability
for political economy claims (DEMO-165)
**ADR prerequisite:** None — confirmed CLEAR in `docs/process/sprint-plans/m19-g4-sprint-entry.md §4`.
Implementation is within ADR-019 Zone 1D scope (control plane column) and ADR-015 §Component 3
(political risk sub-section). No new ADR required.
**Authored by:** PM Agent
**Date:** 2026-07-03
**Implementing agent:** Frontend Architect Agent

**Architecture authority:**
ADR-019 reserves the Zone 1D column for political economy display. ADR-015 §Component 3 governs
the PSP row. This deliverable adds two features to the Zone 1D political risk sub-section within
those existing reservations:

1. **PSP driver arc** — a compact step-indexed display showing the dominant driver at each step
   across the programme window. Data source: `psp_dominant_driver` is already present per-step in
   the trajectory response (`TrajectoryStepResponse.psp_dominant_driver`). No new API endpoint or
   backend change required.

2. **Driver auditability expand panel** — a click-expand affordance on the driver row that opens
   an in-viewport methodology disclosure panel. Content is static methodology description plus
   per-step fragility status (derivable from `legitimacyValue` and `legitimacyFloor` props already
   passed to `FourFrameworkZone1D`). No new API endpoint required.

**Completes the Zone 3 auditability parity:** Zone 3 (DistributionalComparisonSummary) has the
`▶ Methodology` expand panel for distributional claims (#1422, PR #1439). Zone 1D has no
equivalent for political economy claims. DEMO-165 (Persona 3, Andreas Stefanidis) raised this
gap explicitly: "How is 'Driver: fiscal sustainability' computed?" The only current answer
is to direct the stakeholder out of the application.

---

## 2. Persona Trace Elements Targeted

**P-1 — Persona served:**
Primary: Persona 3 (Andreas Stefanidis, Political Advisor) — asked "How is 'Driver: fiscal
sustainability' computed?" at Demo 7 Q&A. Needs to answer that question without leaving Zone 1D.
Secondary: Persona 1 (Lucas Ferreira, IMF Senior Economist) — will probe the driver attribution
logic during programme review; needs to inspect the computation under scrutiny.

**P-2 — Entry state:**
A scenario is loaded in Mode 2 or Mode 3; PE module is enabled; `pspDominantDriver` is non-null
at the current step; Zone 1D is visible in the instrument cluster. The political risk sub-section
shows "Driver: fiscal sustainability" (or another driver label). The stakeholder or analyst asks
about the driver methodology mid-session — they are already looking at the Zone 1D panel.

**P-3 — Journey step:**
Programme Review journey (Persona 3 — active session). Andreas sees the PSP drop and the driver
label change; he wants to explain to the minister what "fiscal sustainability" means as a driver
and how it was computed at this step. The expand panel answers this without navigation away from
the instrument.

**P-4 — Time/interaction ceiling:**
30-second ceiling from driver label click to full methodology panel visible. The expand panel
opens in-viewport — no navigation, no drawer, no scroll to a different zone. One click, immediate
result.

**P-6 — Negotiating leverage delivered:**
Andreas can say: "The dominant driver attribution at step 4 is fiscal sustainability — computed
from the spending-cut events at this step applying the legitimacy erosion elasticity, amplified
by the fragility factor because current legitimacy is below the 0.45 threshold. Here is the
methodology in the panel." He is answering the creditor's challenge in real time with the
calculation visible on screen.

**P-7 — North star capability delivered:**
Andreas can answer "how is the driver computed?" without leaving Zone 1D. The political advisor
on the finance ministry team — who previously had to reference external documentation or ask the
model operator — now has in-viewport auditability parity with Zone 3 distributional claims.

---

## 3. Observable Application State

### 3.1 Primary observable state — driver arc

With PE enabled and a trajectory loaded, the Zone 1D political risk sub-section displays a
compact driver arc: a row of step-indexed driver labels showing the dominant driver at each
step of the programme window.

At `1440×900` viewport with the ZMB scenario loaded (PE enabled, 8 steps computed):
- A row with `data-testid="psp-driver-arc"` is visible below the current-step driver row
- The arc row contains one driver badge per step, with `data-testid="psp-driver-arc-step-{N}"`
  for each step N (1-indexed)
- Each badge shows a 2–4 character abbreviated driver label:
  - `"fiscal_sustainability"` → "FISC"
  - `"external_balance"` → "EXT"
  - `"governance"` → "GOV"
  - `"social_stability"` → "SOC"
  - `null` (no driver attributed) → "—"
- The badge for the current step is visually differentiated (bold or outlined) from prior steps

### 3.2 Secondary observable states

**State A — driver expand panel:**
When the driver row (`data-testid="psp-driver-row"`) is clicked:
- A panel with `data-testid="psp-driver-methodology-panel"` appears immediately below the driver row
- Panel content (all visible without scroll within Zone 1D):
  - Section header: "How the driver is attributed"
  - Four category rows (one per driver category) with `data-testid="psp-driver-category-{category}"`:
    - `"fiscal_sustainability"` — "spending cuts or tax increases in this step (legitimacy erosion)"
    - `"external_balance"` — "GDP growth change in this step (erosion via output shortfall)"
    - `"governance"` — "emergency policy actions in this step (immediate fragility response)"
    - `"social_stability"` — "legitimacy below fragility threshold at step start (baseline erosion)"
  - Fragility status row with `data-testid="psp-driver-fragility-status"`:
    - If legitimacy below threshold: "⚠ Fragility amplifier active — contributions amplified by
      fragility factor at current legitimacy"
    - If legitimacy above threshold: "Fragility amplifier inactive — contributions at base weight"
  - Attribution note: "The dominant driver is the category with the largest event-weighted
    contribution at this step. Ties resolved in priority order: governance > fiscal sustainability
    > external balance."

**State B — panel collapse:**
Clicking the driver row again (or the close affordance within the panel) collapses the panel.
`data-testid="psp-driver-methodology-panel"` is no longer in the DOM (or `hidden`).

### 3.3 Silent failure detection

**SF-1 (driver arc present but all badges show "—"):** `psp_dominant_driver` is null at every
step — no driver was attributed. This is a legitimate state (can occur when no political economy
events fire). Detection: confirm the arc row (`psp-driver-arc`) is present with `data-testid`
anchors; a row of "—" badges is correct output, not a silent failure.

**SF-2 (driver expand panel opens but shows blank content):** The methodology panel renders with
empty category rows — the event-type mapping text is absent. Detection: after clicking the driver
row, assert that at least one `psp-driver-category-{category}` element has non-empty text content.

**SF-3 (driver arc not rendered when pspDominantDriver is null on current step):** If all
`psp_dominant_driver` values across the trajectory are null, the arc row should still render
(showing "—" badges) because the arc is trajectory-length, not current-step-gated. Detection:
load a fixture where PSP is disabled (peEnabled=false) and confirm the arc row is NOT rendered;
load a PE-enabled fixture with all-null drivers and confirm the arc row IS rendered with "—" badges.

**SF-4 (methodology panel not collapsing):** After a second click on the driver row, the panel
remains in the DOM expanded. Detection: assert `psp-driver-methodology-panel` is not present
(or has `hidden` attribute) after a second click.

---

## 4. Acceptance Criteria

**AC-1 (driver arc rendered when PE enabled and trajectory loaded):**
In the ZMB Mode 2 scenario (PE enabled) at step 3, when the trajectory is fully loaded,
then `data-testid="psp-driver-arc"` is visible in Zone 1D and contains at least one
`data-testid="psp-driver-arc-step-{N}"` badge element for each step 1 through 3.

**AC-2 (driver arc badge abbreviations correct):**
In the ZMB Mode 2 scenario with `psp_dominant_driver="fiscal_sustainability"` at step 2,
then `data-testid="psp-driver-arc-step-2"` displays "FISC". Similarly: "EXT" for
`"external_balance"`, "GOV" for `"governance"`, "SOC" for `"social_stability"`, and "—"
for `null`.

**AC-3 (current step badge is visually differentiated):**
At step 3 of the ZMB scenario, `data-testid="psp-driver-arc-step-3"` has a distinct visual
treatment from step 1 and step 2 badges (bold text weight or border — observable by font-weight
or border CSS, not by colour alone, for accessibility).

**AC-4 (expand panel appears on driver row click):**
In the ZMB Mode 2 scenario at step 3 with `pspDominantDriver="fiscal_sustainability"`,
when `data-testid="psp-driver-row"` is clicked, then `data-testid="psp-driver-methodology-panel"`
appears in the DOM and all four `data-testid="psp-driver-category-{category}"` elements
have non-empty text content.

**AC-5 (fragility amplifier active state):**
In a fixture where `legitimacyValue` is below `legitimacyFloor`, when the driver row is clicked,
then `data-testid="psp-driver-fragility-status"` text contains "amplifier active".

**AC-6 (fragility amplifier inactive state):**
In a fixture where `legitimacyValue` is above `legitimacyFloor`, when the driver row is clicked,
then `data-testid="psp-driver-fragility-status"` text contains "amplifier inactive" or
"Fragility amplifier inactive".

**AC-7 (expand panel collapses on second click):**
In the ZMB scenario, after clicking the driver row to open the panel, when the driver row is
clicked again, then `data-testid="psp-driver-methodology-panel"` is no longer visible (not
present in DOM or has `hidden` attribute).

**AC-8 (driver arc absent when PE disabled):**
In a fixture where `peEnabled=false`, then `data-testid="psp-driver-arc"` is not present in the DOM.

**AC-9 (driver arc absent when pspValue is undefined):**
In a fixture where PE is enabled but `pspValue === undefined` (scenario loaded but PSP not yet
computed), then `data-testid="psp-driver-arc"` is not present in the DOM and
`data-testid="psp-driver-row"` is not present (consistent with existing conditional rendering).

**AC-10 (SF-3 — arc rendered with all-null drivers):**
In a PE-enabled fixture where all `psp_dominant_driver` values across the trajectory steps are
null, then `data-testid="psp-driver-arc"` is present and all step badges show "—".

**AC-11 (expand affordance present on driver row):**
In the ZMB scenario with `pspDominantDriver` non-null, the driver row renders a clickable
expand affordance (button or clickable element) with `data-testid="psp-driver-expand"` visible
alongside the driver label text.

---

## 4b. Visual Spec (before/after)

**AC-1/AC-4/AC-11 (before — current state):**
```
Viewport: 1440×900 | Zone: Zone 1D (political risk sub-section) | data-testid="zone-1d-political-risk"

POLITICAL RISK
Programme survival: WARNING (48%) — DECLINING
Driver: fiscal sustainability               ← single row, no expand affordance
Comparable: Zambia 2015 ECF — abandoned Step 3 (PSP 38%). Board review failed.
Legitimacy index: 0.42 — declining (floor: 0.45)
0.03 below fragility threshold
Elite capture divergence: widening — fiscal benefits concentrating
```

**AC-1/AC-4/AC-11 (after — target state):**
```
Viewport: 1440×900 | Zone: Zone 1D (political risk sub-section) | data-testid="zone-1d-political-risk"

POLITICAL RISK
Programme survival: WARNING (48%) — DECLINING
▶ Driver: fiscal sustainability  [data-testid="psp-driver-expand"]   ← clickable
Step arc: FISC FISC GOV FISC ...  [data-testid="psp-driver-arc"]
Comparable: Zambia 2015 ECF — abandoned Step 3 (PSP 38%). Board review failed.
Legitimacy index: 0.42 — declining (floor: 0.45)
0.03 below fragility threshold
Elite capture divergence: widening — fiscal benefits concentrating

[After click on driver row:]
▼ Driver: fiscal sustainability
────────────────────────────────────────────────────────
How the driver is attributed:     [data-testid="psp-driver-methodology-panel"]
  fiscal sustainability  — spending cuts or tax increases in this step (legitimacy erosion)
  external balance       — GDP growth change in this step (erosion via output shortfall)
  governance             — emergency policy actions in this step (immediate fragility response)
  social stability       — legitimacy below fragility threshold at step start (baseline erosion)
⚠ Fragility amplifier active — contributions amplified by fragility factor at current legitimacy
Dominant driver: largest event-weighted contribution. Ties: governance > fiscal > external.
```

---

## 5. Kryptonite Constraint Check

**Does this implementation's primary observable state require specialist mediation for Persona 3
to act on it in the Reactive entry state (30-second ceiling)?**

`[x]` No — the observable state is interpretable by Persona 3 without an analyst translating it.

**Rationale:** The driver arc and methodology panel use plain English category labels and
event-type descriptions ("spending cuts or tax increases", "GDP growth change", "emergency
policy actions"). Persona 3 (Political Advisor) is a domain expert in political economy — these
descriptions are within their baseline literacy. The fragility amplifier status is surfaced as a
plain-language indicator, not a model parameter. No specialist mediation required.

The "attribution note" (priority order: governance > fiscal > external) is a tiebreaker rule —
a one-line disclosure that is interpretable without model knowledge. It does not require an
analyst to translate.

---

## 6. Out of Scope

- **Quantitative contribution values per category at the current step** — showing the exact
  Decimal contribution of each category (e.g., "fiscal_sustainability: 0.0432") requires the
  backend to expose per-step contribution breakdown in the API response. This is deferred to
  M20 if demanded by Demo 8 stakeholder feedback. The M19 implementation shows the category
  mapping (qualitative) and fragility status, not numeric per-category weights at the current step.
- **Arc visualisation beyond text badges** — no sparkline, no SVG chart, no colour-coded bars
  in M19. Compact text badges in a single row. A richer arc visualisation is a future enhancement.
- **Driver arc in Mode 1 (Replay)** — the arc is active in Mode 2 and Mode 3 only. Mode 1
  shows the full trajectory; the arc is redundant there. If `mode === "MODE_1"` and the arc
  renders anyway, it is not a Verify failure — but the E2E fixture should use Mode 2.
- **Auto-open panel on driver change** — the panel does not auto-open when the dominant driver
  changes between steps. It is expand-on-click only. Auto-open is deferred as a future UX enhancement.
- **PSP driver API changes** — the `psp_dominant_driver` field is already in the per-step
  trajectory response. No backend changes are introduced by this deliverable.

---

## 7. Test Authorship Obligation

**QA Lead:** QA Lead Agent
**Test authorship deadline:** Before any G4 implementation PR opens on `sprint/m19-g4`
**Test file location:** `frontend/tests/e2e/m19-g4-psp-driver-auditability.spec.ts`

**NM-086 gate:** #1528 is frontend-only and reads only existing trajectory API fields
(`psp_dominant_driver` per step). No new mock routes are introduced. QA Lead must confirm
against `docs/schema/api_contracts.yml §trajectory` that `psp_dominant_driver` is already
declared as a field in the per-step response before filing the QA acknowledgment below.

**Required test coverage (Playwright E2E):**

- **AC-1:** Load ZMB PE-enabled scenario; navigate to step 3; assert `psp-driver-arc` visible
  and contains `psp-driver-arc-step-1`, `psp-driver-arc-step-2`, `psp-driver-arc-step-3`.
- **AC-2:** With ZMB fixture having `fiscal_sustainability` at step 2; assert
  `psp-driver-arc-step-2` text is "FISC". Repeat for "EXT", "GOV", "SOC", "—".
- **AC-3:** At step 3 (current step); assert `psp-driver-arc-step-3` has font-weight 700 (or
  CSS border property); assert other step badges do not have that font-weight.
- **AC-4:** Click `psp-driver-row`; assert `psp-driver-methodology-panel` present;
  assert all four `psp-driver-category-{cat}` elements have non-empty `.textContent`.
- **AC-5:** Use fixture with `legitimacyValue < legitimacyFloor`; click driver row;
  assert `psp-driver-fragility-status` text contains "amplifier active".
- **AC-6:** Use fixture with `legitimacyValue > legitimacyFloor`; click driver row;
  assert `psp-driver-fragility-status` text contains "inactive".
- **AC-7:** Click driver row to open; click again; assert `psp-driver-methodology-panel`
  not visible (not in DOM or `hidden`).
- **AC-8:** Render with `peEnabled=false`; assert `psp-driver-arc` not in DOM.
- **AC-9:** Render with `pspValue=undefined`; assert `psp-driver-arc` and `psp-driver-row`
  not in DOM.
- **AC-10:** Load fixture where all trajectory steps have `psp_dominant_driver=null`; assert
  `psp-driver-arc` present and all step badge text is "—".
- **AC-11:** At step 3 with `pspDominantDriver` non-null; assert `psp-driver-expand` present
  in DOM alongside the driver label text.

**QA Lead acknowledgment:**
`[x]` QA Lead: Tests for AC-1 through AC-11 authored and filed. 2026-07-03
`[x]` QA Lead: `psp_dominant_driver` confirmed in `api_contracts.yml` (line ~809, measurement-output
endpoint; also declared per-step in trajectory per intent doc §1). Mock helpers use existing field.
NM-086 note: trajectory endpoint declaration not explicitly confirmed — implementing agent to verify
`TrajectoryStepResponse.psp_dominant_driver` is documented in api_contracts.yml §trajectory. 2026-07-03

---

*Intent document version: 2026-07-03. ADR prerequisite: None (within ADR-019 + ADR-015 scope).
Sprint entry: `docs/process/sprint-plans/m19-g4-sprint-entry.md`.
See `docs/process/agent-execution-lifecycle.md` for the five-step lifecycle this document gates.*
