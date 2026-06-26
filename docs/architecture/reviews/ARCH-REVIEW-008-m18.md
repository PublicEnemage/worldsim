# ARCH-REVIEW-008 — Control Plane Column Current State Audit

> **Type:** Architecture Review — Current State Audit (GD Artifact 1, Issue #1355)
> **Parent:** #1354 — Control Plane Column Design Package
> **Date:** 2026-06-26
> **Owning agents:** CE Agent (Computation Engine Agent) — engine/backend scope; Frontend Architect Agent — `frontend/src/components/` scope
> **Filing location:** `docs/architecture/reviews/ARCH-REVIEW-008-m18.md`
> **Status:** Filed

---

## Scope

This audit compares the specified behaviour of the 280px control plane column
(per `docs/ux/information-hierarchy.md §Control Plane Reserved Zone`,
`docs/ux/user-stories-instrument-cluster-m9.md §Group 8 US-027/US-028`, and
the M9 FA brief layout constants) against what exists in the codebase at the
time GD begins. It is a factual inventory only — design recommendations belong
in Artifact 4 (Delta Analysis).

---

## 1. Column Layout — All Three Breakpoints

**Specification:** 280px right column (`gridColumn: 3`) at all supported viewports;
always rendered (not collapsed or `display: none`) in Mode 1, Mode 2, and Mode 3.
Width = 280px confirmed by Playwright AC-014.

**Finding:**

`InstrumentCluster.tsx` exports the `LAYOUT` constant:

```ts
// InstrumentCluster.tsx:16–20
export const LAYOUT = {
  1024: { trajectory: 480, coPrimary: 240, controlPlane: 280, chartHeight: 300 },
  1280: { trajectory: 580, coPrimary: 400, controlPlane: 280, chartHeight: 320 },
  1440: { trajectory: 680, coPrimary: 400, controlPlane: 280, chartHeight: 380 },
} as const;
```

The grid is set at `InstrumentCluster.tsx:91`:
```ts
gridTemplateColumns: `${layout.trajectory}px ${layout.coPrimary}px ${layout.controlPlane}px`
```

The control plane div (`data-testid="zone-control-plane"`) is at `InstrumentCluster.tsx:183–211`:
- `gridColumn: 3`, `gridRow: 1`, `minWidth: layout.controlPlane` (280px at all three breakpoints)
- Not `display: none` in any mode; always present in the DOM

**Verdict: PRESENT** — 280px column is rendered at all three breakpoints (1024, 1280, 1440). US-027 column-width criterion is satisfied.

---

## 2. Mode 1 / Mode 2 Placeholder Behaviour

**Specification (US-027):** In Mode 1 and Mode 2, the control plane zone contains no
interactive elements. Any placeholder label uses subdued styling (not competing with Zone 1).

**Finding:**

`InstrumentCluster.tsx:194–210`:
```tsx
{!isMode3 && (
  <div
    aria-label="Control plane reserved zone"
    style={{
      position: "absolute",
      bottom: 16,
      left: 8,
      fontSize: 11,
      color: "rgba(0,0,0,0.25)",   // ← subdued
      fontFamily: "monospace",
      pointerEvents: "none",
      userSelect: "none",
    }}
  >
    Control plane (Mode 3)
  </div>
)}
```

No form fields, no buttons, no interactive elements in this div. Font size 11px
(smaller than any Zone 1 label — Zone 1B compact format uses 12px). Color
`rgba(0,0,0,0.25)` — 25% opacity black on white background — is visually subdued.
Mode indicator "Mode 3" watermark text does not contain modal headings or visual
weight competing with Zone 1.

**Verdict: PRESENT** — US-027 placeholder behaviour is satisfied.

---

## 3. Mode 3: Location of ControlPlane Component Render

**Specification (US-028, information-hierarchy.md §Control Plane Reserved Zone):**
The `ControlPlane` component must render inside the 280px reserved column
(`gridColumn: 3` of `InstrumentCluster`). Both policy instruments form and
scenario shocks form must be visible simultaneously within that column without scroll.

**Finding:**

The 280px column (`zone-control-plane`) in `InstrumentCluster` renders **nothing** in
Mode 3. The `InstrumentCluster` component has no slot for control plane content — it
does not accept a `controlPlane` prop and does not conditionally render the `ControlPlane`
component inside `gridColumn: 3`.

The `ControlPlane` component is instead rendered **outside and below** `InstrumentCluster`
in `ScenarioInstrumentCluster.tsx:983–989`:

```tsx
{/* ControlPlane — rendered in Mode 3 only (G6b, Issue #753). */}
{mode === "MODE_3" && (
  <ControlPlane
    onApplyChange={handleApplyControlChange}
    currentStep={currentStep}
  />
)}
```

`ScenarioInstrumentCluster.tsx` renders in a `<div>` wrapper (the root return at
~line 870). The `InstrumentCluster` is one child of this wrapper. The `ControlPlane`
is a sibling rendered after `InstrumentCluster` and after the `HumanCapitalTrajectoryPanel`
conditional. This produces a vertical stack:

```
[ScenarioInstrumentCluster root div]
  ├── [entity selector / comparison controls]
  ├── [InstrumentCluster] ← 280px column here is EMPTY in Mode 3
  ├── [HumanCapitalTrajectoryPanel] (conditional on projection_steps > 8)
  └── [ControlPlane] ← rendered here as full-width bottom bar
```

`ControlPlane.tsx:31–38` confirms the full-width bottom-bar layout:
```ts
const PANEL_STYLE: React.CSSProperties = {
  padding: "10px 12px",
  background: "#f8f4ff",
  borderTop: "2px solid #8b5cf6",
  display: "flex",
  flexDirection: "column",
  gap: 10,
};
```

No `width`, no `maxWidth`, no `position: absolute` — this div stretches full-width
of its parent, which is the full `ScenarioInstrumentCluster` root div.

**Verdict: ABSENT** — The `ControlPlane` component does not render inside the 280px
reserved column. The column is empty in Mode 3. The `ControlPlane` renders as a
full-width horizontal bar below the instrument cluster. This is the root divergence
from the US-028 and information-hierarchy specification.

---

## 4. Policy Instruments Form (US-028 Acceptance Criteria)

Assessment of each US-028 acceptance criterion element against what exists in
`ControlPlane.tsx`:

| Element | Specification | Finding | Verdict |
|---|---|---|---|
| Control input type selector | User selects policy input *type* before entering parameters | Not present. The form directly exposes `fiscal_multiplier` and `branch_from_step` sliders — no type selection step exists | ABSENT |
| Parameter field(s) | One or more parameter fields for the selected type | `fiscal_multiplier` slider (range 0.1–3.0, step 0.05) is present. No additional parameter fields. | PARTIAL |
| Step selector | Selects which step the input applies to | `branch_from_step` slider (range 0–currentStep) is present but functions as a global recompute anchor ("recompute forward from step"), not a per-input step selector | PARTIAL |
| "Apply policy input" button | Labelled apply action | Present as "Apply Change" (`data-testid="apply-control-change"`). Label differs from the specified "Apply policy input" phrasing. | PARTIAL |
| Applied inputs history list | List of applied inputs within current session | Not present. No history rendering in `ControlPlane.tsx`. | ABSENT |
| Blue visual treatment throughout | Blue color (#0ea5e9 or equivalent) used for all policy form elements | Purple (#8b5cf6) is used throughout for all form elements, label text, and the Apply button. No blue color appears in `ControlPlane.tsx`. | ABSENT |

**Summary for policy instruments form:** 0 PRESENT / 3 PARTIAL / 3 ABSENT out of 6 elements.

---

## 5. Scenario Shocks Form (US-028 Acceptance Criteria)

**Specification:** A separate form with orange visual treatment, containing:
step selector, shock type selector from taxonomy, "Inject scenario shock" button,
injected shocks history list.

**Shock taxonomy specified (Issue #1354):** `ElectionShock`, `CurrencyAttack`,
`CreditorDefection`, `GeopoliticalShock`, `NaturalDisaster`, `ContagionShock`.

**Finding:**

No scenario shocks form exists anywhere in the frontend codebase. Searching
`frontend/src/components/` for "shock" in component files:
- `ControlPlane.tsx` — no shock reference
- `ScenarioInstrumentCluster.tsx` — no shock injection logic
- `MDAAlertPanelZone1B.tsx` — causal attribution string rendered as-is (field passthrough)
- No file in `frontend/src/components/` implements shock injection, a shock taxonomy
  selector, or a shocks history list

**Verdict: ABSENT** — Complete absence. No element of the scenario shocks form exists.

---

## 6. Blue/Orange Visual System

**Specification (information-hierarchy.md §Control Plane Reserved Zone, US-009):**
- Policy inputs: blue visual treatment throughout — form elements, trajectory inflection
  markers, and MDA causal attribution all use blue
- Exogenous shocks: orange visual treatment throughout — form elements, trajectory
  vertical markers, and MDA causal attribution all use orange
- Distinction must be visually scannable without reading alert text

**Finding — ControlPlane.tsx colors:**
All styling in `ControlPlane.tsx` uses purple `#8b5cf6`:
- `PANEL_STYLE.borderTop: "2px solid #8b5cf6"`
- `APPLY_BTN_STYLE.background: "#8b5cf6"`
- `VALUE_STYLE.color: "#8b5cf6"`
- Panel header: `color: "#8b5cf6"`
- Slider `accentColor: "#8b5cf6"`

No blue or orange color value appears anywhere in `ControlPlane.tsx`.

**Finding — Trajectory markers:**
`TrajectoryView.tsx` is the Zone 1A chart component. Searching for policy input
and shock markers:
- No `<ReferenceLine>` elements for policy input step markers in Mode 3
- No orange vertical line elements for shock event markers
- US-009 acceptance criteria (blue marker at control input step; orange vertical
  spanning full chart at shock step) — both ABSENT

**Finding — MDA alert causal attribution (`MDAAlertPanelZone1B.tsx:599–605`):**
```tsx
{mode === "MODE_3" && alert.causal_attribution && (
  <div
    data-testid="detail-causal-attribution"
    ...
  >
    Caused by: {alert.causal_attribution}
  </div>
)}
```

The `causal_attribution` field is rendered when present. There is no logic to:
- Distinguish a policy-input attribution from a shock-input attribution by color
- Render "Caused by: Multiple inputs (see trajectory view)" for multi-cause alerts
- Apply blue/orange color treatment to the attribution text itself

The causal attribution field is a pass-through string — backend returns whatever
string it generates; the frontend renders it without color treatment.

**Verdict: ABSENT** — Blue/orange visual system is completely absent. The policy
form uses purple. Trajectory markers for both policy inputs and shocks are absent.
Causal attribution has no color distinction between policy and shock causes.

---

## 7. Mode 2 Column Content (Issue #746)

**Specification (information-hierarchy.md §Control Plane Reserved Zone, Issue #1354):**
In Mode 2, the column should contain a "scenario configuration surface — fiscal
multiplier parameter input, scenario setup controls — visible alongside the
trajectory view without navigating away." Issue #746 was filed to specify and
build the Mode 2 fiscal multiplier parameter input in the column.

**Finding:**

Issue #746 was never built. The `InstrumentCluster` control plane column renders
only the subdued watermark placeholder in Mode 2 — identical to Mode 1 behaviour.
No fiscal multiplier parameter, no scenario setup controls, no Mode 2-specific
content exists in the 280px column.

The `ScenarioControls.tsx` component provides the fiscal multiplier and other
scenario setup controls — but it renders in the scenario detail panel (`App.tsx`
scenario configuration flow), not in the control plane column of the instrument
cluster. Reaching it in Mode 2 requires navigating out of the instrument cluster.

This is Journey A Gap GA-02: "Fiscal multiplier input not accessible from within
the instrument cluster view. She has to leave the trajectory to configure the
parameter that changes the trajectory."

**Verdict: ABSENT** — Mode 2 column content has never been designed or implemented
at the form level. Issue #746 (Mode 2 fiscal multiplier parameter input) is open.

---

## 8. Performance Baseline

**Specification (US-029):** Trajectory view renders within 100ms on CI 4× throttled
profile. Manual validation target MV-002 ≤ 100ms on 8GB/4-core hardware without throttle.

**Finding:**

- **EX-001 status:** ACTIVE. EX-001 raised the AC-009 CI throttled threshold from
  100ms to 200ms. Expiry condition was "M17 exit." M17 has closed; EX-001 has not
  been renewed, closed, or replaced. At M18 start, EX-001 is in an expired-but-no-decision
  state — the exception remains Active in the registry (`docs/compliance/exceptions.md:25`)
  with a note that a new EL decision is required.

- **Last measured CI throttled performance:** 179ms (GitHub Actions ubuntu-latest,
  2-core, 4× CPU throttle, measured 2026-06-24 per `docs/compliance/exceptions.md:72`).
  This is Mode 3 full component set (8 `<Line>` + 4 `<Area>` + 3 shock `<ReferenceLine>`
  per AC-009 definition — though the `<ReferenceLine>` components for shocks do not
  yet exist; the 179ms measurement reflects the current reduced component set).

- **Hardware validation (MV-002):** Completed at M10 (ProBook hardware). The
  hardware target ≤ 100ms has not been re-validated after subsequent Mode 3
  component additions in M11–M17.

- **Issue #1217:** Mode 3 render optimization is filed as G4 Wave 2, sequenced
  via GD/ADR-019. This issue explicitly notes EX-001 expiry.

**Verdict:** Performance baseline is at 179ms CI throttled / hardware target unverified
at current component count. EX-001 requires an M18 EL decision: renew, replace with
optimization, or close as Won't Fix. This is a GD dependency — any new Mode 3
components (scenario shocks form, policy type selector, history lists) will increase
render time from the 179ms baseline.

---

## 9. Summary Table — US-027 and US-028 Acceptance Criteria Status

| AC | Criterion | Status |
|---|---|---|
| US-027-AC-1 | Control plane zone width = 280px in Mode 1/2 at all breakpoints | **PRESENT** |
| US-027-AC-2 | No interactive elements in Mode 1/2 control plane | **PRESENT** |
| US-027-AC-3 | Subdued placeholder styling (font, color) | **PRESENT** |
| US-028-AC-1 | Both form headers (blue + orange) visible without scroll in Mode 3 | **ABSENT** |
| US-028-AC-2 | Blue/orange visual distinction, CVD (MV-001) pending | **ABSENT** |
| US-028-AC-3 | Applied inputs history list in policy form (Mode 3, ≥1 input) | **ABSENT** |
| US-028-AC-4 | Injected shocks history list in shock form (Mode 3, ≥1 shock) | **ABSENT** |
| US-009-AC-1 | Blue marker at policy input step (trajectory view) | **ABSENT** |
| US-009-AC-2 | Orange vertical marker at shock step spanning all curves | **ABSENT** |
| US-017-AC-1 | "Caused by:" present in Mode 3 alert row (policy type) | **PARTIAL** |
| US-017-AC-2 | "Caused by: [shock type]" for shock-caused alerts | **ABSENT** |
| US-017-AC-3 | "Caused by: Multiple inputs" for multi-cause alerts | **ABSENT** |

---

## 10. Filing Completion Declaration

This audit satisfies the Artifact 1 acceptance criteria (Issue #1355):

- [x] Every US-027 and US-028 acceptance criterion has a corresponding PRESENT /
  ABSENT / PARTIAL finding in this audit
- [x] Column layout at all three breakpoints confirmed with pixel measurements from
  codebase constants (LAYOUT const in `InstrumentCluster.tsx:16–20`)
- [x] Location of current `ControlPlane` component render explicitly confirmed
  (outside the 280px column — full-width bar below InstrumentCluster)
- [x] Mode 2 column state addressed (Issue #746 not built; ABSENT)
- [x] No design recommendations included — factual inventory only

Closes: Artifact 1 prerequisite for Artifacts 2 (#1356) and 4 (#1358).
