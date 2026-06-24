---
name: M16-G9-delta-choropleth-threshold-overlay
type: implementation-intent
issues: "#153"
status: Filed — QA tests required before implementation PR opens
authored-by: PM Agent (pre-implementation spec; Frontend Architect Agent takes implementation authority at Step 3)
authored-date: 2026-06-24
implementing-agent: Frontend Architect Agent
sprint-entry: "docs/process/sprint-plans/m16-g9-sprint-entry.md — EL Approved 2026-06-24"
adr-reference: "None — enhancement within existing DeltaChoropleth component boundary; ADR gate CLEAR per sprint entry §2.2"
release-branch: release/m16
sequencing: "After G1 merges to release/m16 — DeltaChoropleth is in the geographic context zone (Zone 1C/2) but shares the primary viewport; G1 must land first to avoid primary viewport conflicts"
---

# Implementation Intent: M16-G9 — Absolute Threshold Overlay on DeltaChoropleth (#153)

> **G9 capacity-allowing.** Not Demo 6 critical path. If capacity is exhausted before G8 is
> scheduled, this issue carries to M17.
> Implementation does not begin until: (1) G1 merges to `release/m16`; (2) this intent document
> is committed to `release/m16`; (3) QA tests are authored from this document's ACs.

---

## 1. Source Authority

**Issue:** #153 — feat(frontend): absolute threshold overlay on DeltaChoropleth
**Sprint entry:** `docs/process/sprint-plans/m16-g9-sprint-entry.md` — EL Approved 2026-06-24
**ADR gate:** None — enhancement within existing DeltaChoropleth component boundary
**Date authored:** 2026-06-24
**Authored by:** PM Agent (pre-implementation spec)
**Implementing agent:** Frontend Architect Agent

---

## 2. Persona Trace Elements Targeted

**P-1 — Personas served:**
**Persona 2 — Finance Ministry Negotiator** (Aicha Mbaye archetype, `docs/ux/personas.md §Persona 2`).
The DeltaChoropleth provides geographic context — which entities are moving toward or away from
thresholds across the map. Without an absolute threshold overlay, the geographic view encodes
relative movement (delta) but not threshold proximity. A Persona 2 analyst preparing for an Article
IV consultation needs to see not only the direction of movement but whether that movement is crossing
a specific MDA threshold. The threshold overlay provides that reference point without requiring
navigation to a separate view.

**P-2 — Entry state:**
Preparatory (3-hour briefing window). The geographic view is primarily a Preparatory tool — Persona 2
uses it to orient to the scenario's spatial dimension before or between Mode 3 control sessions.
The threshold overlay is available during Preparatory exploration. It is not a Reactive-state
primary instrument.

**P-3 — Journey reference:**
Journey A (Preparatory briefing) — geographic context scan before the consultation session. The
analyst surveys the choropleth to understand the cross-entity landscape before narrowing to the
Zone 1A instrument for Mode 2/3 work.

**P-4 — Time/interaction ceiling:**
One interaction to enable the toggle (Preparatory state — no Reactive ceiling applies to this feature).
The toggle state persists for the session once enabled.

**P-7 — North star capability delivered:**
A Senegalese Finance Ministry analyst loading the Demo 6 scenario can enable the DeltaChoropleth
threshold overlay and immediately see which entities in the comparison map are at or beyond their
MDA poverty floor without navigating away from the geographic view or opening a data drawer.
The threshold boundary is visible as a geographic reference alongside the delta movement signal.

---

## 3. Observable Application State

*All states verifiable by an external observer using only the running application at 1280×800
with the Zambia 2023–2024 IMF ECF fixture (or equivalent scenario with MDA thresholds configured).
No source code reading, no CI report reference.*

### 3.1 Primary observable state

At 1280×800 with the ZMB ECF scenario loaded in **any mode**, with MDA thresholds configured in
the active scenario:

A toggle control is present in or adjacent to the DeltaChoropleth component:
`data-testid="delta-choropleth-threshold-toggle"` is visible and interactive.

After the toggle is activated (one click): `data-testid="delta-choropleth-threshold-overlay"` is
present in the DeltaChoropleth's DOM subtree with a non-zero bounding box (visible on screen).
The overlay element uses a visual encoding distinct from the delta gradient fill — specifically,
a stroke-based element (SVG path or polyline with a `stroke` attribute, or a dashed line) rather
than the filled-region gradient encoding used for the delta colouring.

### 3.2 Secondary observable states

**State A — Toggle off (default):**
On initial load (before toggle interaction): `data-testid="delta-choropleth-threshold-overlay"` is
absent from the DOM or has `display: none`. The DeltaChoropleth renders normally with only delta
colouring. No layout shift occurs in Zone 1A or Zone 1B when the toggle state changes — the
choropleth and adjacent primary viewport zones maintain their bounding boxes.

**State B — Overlay does not obstruct country labels:**
With the toggle on at 1280×800 and the ZMB ECF scenario loaded, country label elements in the
DeltaChoropleth (matching `[data-testid^="delta-choropleth-label-"]` or equivalent) remain
readable — the overlay element does not fully cover any country label text bounding box.
A partial overlap at a non-label-text pixel is acceptable; full label occlusion is not.

**State C — No overlay when no MDA thresholds configured:**
With a scenario that has no MDA thresholds configured (test fixture with empty or absent
`mda_thresholds`): `data-testid="delta-choropleth-threshold-toggle"` is either absent from the
DOM or has `aria-disabled="true"` (or equivalent disabled state). No null/NaN overlay renders.
The DeltaChoropleth displays its standard delta colouring without error.

### 3.3 Silent failure detection

**Silent failure 1 — Toggle present, overlay zero-size:**
The toggle activates but the overlay element has zero bounding box dimensions (rendered but not
visible) because the threshold value is null, NaN, or out of coordinate range. Detection:
after toggle activation, `getBoundingClientRect` of `delta-choropleth-threshold-overlay` must
have `width > 0` and `height > 0`.

**Silent failure 2 — Overlay uses same visual encoding as delta fill:**
The overlay is present but uses the same fill-gradient visual treatment as the delta colouring —
indistinguishable to the eye. Detection: the overlay element must carry a `stroke` CSS/SVG
attribute that differs from the fill-only delta encoding (AC-2).

**Silent failure 3 — Layout shift on toggle:**
Toggling causes Zone 1A or Zone 1B to resize or reflow, disrupting the primary instrument cluster.
Detection: AC-4 measures Zone 1A bounding box before and after toggle — delta must be zero.

---

## 4. Acceptance Criteria

*Each criterion verifiable by an external observer. Test file:
`frontend/tests/e2e/m16-g9-delta-choropleth-overlay.spec.ts`*

**AC-1 (toggle present, overlay visible when on):**
At 1280×800 with ZMB ECF scenario loaded in Mode 1:
`data-testid="delta-choropleth-threshold-toggle"` is present and visible in the DeltaChoropleth
component or its containing zone control bar.
After clicking the toggle once: `data-testid="delta-choropleth-threshold-overlay"` is present in
the DOM, visible (`display` is not `none`), and `getBoundingClientRect` returns `width > 0` and
`height > 0`.

**AC-2 (overlay visually distinct from delta fill):**
With toggle on at 1280×800 and ZMB ECF in Mode 1:
`data-testid="delta-choropleth-threshold-overlay"` has either (a) a `stroke` SVG attribute with a
non-transparent value, or (b) a CSS `border-color` or `outline` style distinct from the delta
gradient's fill-only encoding. The overlay does not use the same fill-gradient class as the delta
colouring. The implementing agent documents the chosen visual encoding (dashed line, solid contour,
or hatched band) in the PR description.

**AC-3 (overlay does not obstruct country labels):**
With toggle on at 1280×800 and ZMB ECF in Mode 1:
No element matching `[data-testid^="delta-choropleth-label-"]` (or the equivalent country label
test ID pattern in the existing component) has its complete text bounding box covered by the overlay
bounding box. Test: for each label, assert that at least one pixel of the label's bounding box is
not overlapped by the overlay bounding box.

**AC-4 (toggle off = no overlay; no layout shift in Zone 1A):**
At 1280×800 with ZMB ECF in Mode 1, record the bounding box of `data-testid="zone-1a-trajectory"`.
Enable the toggle. Record the bounding box again. Disable the toggle. Record the bounding box again.
All three measurements of `zone-1a-trajectory` bounding box (x, y, width, height) are identical —
zero pixel delta across both toggle state changes.
After the second toggle click: `data-testid="delta-choropleth-threshold-overlay"` is absent or
`display: none`.

**AC-5 (disabled/absent toggle when no thresholds configured):**
With a test fixture where `mda_thresholds` is empty or absent from the scenario configuration:
`data-testid="delta-choropleth-threshold-toggle"` is either absent from the DOM or has
`aria-disabled="true"` (or equivalent). No overlay element renders with null/NaN values.
The DeltaChoropleth renders its standard delta colouring without console error.

**AC-6 (overlay remains visible after step change):**
With toggle on at 1280×800 and ZMB ECF in Mode 1:
After advancing from step 0 to step 1, `data-testid="delta-choropleth-threshold-overlay"` remains
present in the DOM and visible (non-zero bounding box). The overlay does not disappear during step
transition.

---

## 4b. Visual Spec (before/after)

### AC-1 — DeltaChoropleth toggle + overlay

**AC-1 (before — default state, no overlay):**
```
Viewport: 1280×800 | Zone: 1C/2 (geographic context) | data-testid="delta-choropleth"

DeltaChoropleth with ZMB ECF, Mode 1, step 1:
┌──────────────────────────────────────────────────────────────┐
│  [MAP]                                                        │
│  Country fills: gradient — blue (neg delta) to red (pos)     │
│                                                              │
│  Country label: "ZMB"                                        │
│                                                              │
│  [No delta-choropleth-threshold-toggle visible]              │
│  [No delta-choropleth-threshold-overlay present]             │
└──────────────────────────────────────────────────────────────┘
```

**AC-1 (after — toggle visible, overlay enabled):**
```
Viewport: 1280×800 | Zone: 1C/2 (geographic context) | data-testid="delta-choropleth"

DeltaChoropleth with ZMB ECF, Mode 1, step 1, toggle ON:
┌──────────────────────────────────────────────────────────────┐
│  [MAP]                                                        │
│  Country fills: gradient delta colouring (unchanged)         │
│                                                              │
│  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │
│  ↑ data-testid="delta-choropleth-threshold-overlay"          │
│    Dashed/stroke line at MDA threshold value                 │
│    Visually distinct from delta gradient fill                │
│                                                              │
│  [●] Threshold overlay  ← delta-choropleth-threshold-toggle  │
│  Country label: "ZMB" — not occluded by overlay line        │
└──────────────────────────────────────────────────────────────┘
```

### AC-4 — No layout shift

**AC-4 (layout stability check):**
```
data-testid="zone-1a-trajectory" bounding box:
  Before toggle ON:  { x: [N], y: [N], width: [W], height: [H] }
  After toggle ON:   { x: [N], y: [N], width: [W], height: [H] }  ← identical
  After toggle OFF:  { x: [N], y: [N], width: [W], height: [H] }  ← identical

DeltaChoropleth is in Zone 1C/2; toggle state must not reflow Zone 1A.
```

---

## 5. Kryptonite Constraint Check

**Does this implementation's primary observable state require specialist mediation for Persona 2
to act on it in the Reactive entry state (90-second ceiling)?**

`[x]` **No** — with conditions.

The toggle is an opt-in Preparatory-state control. Persona 2 does not encounter it in the
Reactive 90-second ceiling unless they deliberately open the geographic view and activate it.
In Preparatory state, a finance analyst can interpret a threshold line on a choropleth
("this boundary shows the MDA floor value") with minimal explanation. The geographic context
zone (Zone 1C/2) is navigable, not primary — instruments (Zone 1A, Zone 1D) remain in the
primary viewport regardless of toggle state.

Named asymmetry gap (accepted): a well-resourced actor with multiple analysts can derive
threshold proximity for all entities from primary data without this overlay. WorldSim makes
the same information available at one toggle interaction. Multi-indicator threshold mapping in
the geographic view (overlay per indicator from a selection list) remains a capability advantage
for well-resourced actors — out of this intent's scope.

---

## 6. Out of Scope

| Scope item | Rationale for exclusion |
|---|---|
| Multi-indicator threshold toggle (per-indicator overlay selection) | #153 scope is a single configurable overlay per the MDA configuration. Per-indicator selection UI is a separate design. |
| Threshold overlay in Zone 1A trajectory chart | Zone 1A MDA floor lines were delivered in G1 (ADR-017 Phase 4). This overlay is scoped to DeltaChoropleth only. |
| Interactive threshold value editing from the overlay | Read-only display only. Threshold values come from the scenario's MDA configuration. |
| Animated threshold-crossing highlight | Static line/band only. Animation belongs to an MDA alert treatment — not this feature. |
| G1/G2 component files (Zone 1A, Zone 1B, Zone 1D) | #153 modifies the DeltaChoropleth component only. Must not touch G1 or G2 delivered surfaces. |

---

## 7. Test Authorship Obligation

**QA Lead:** QA Lead Agent
**Test authorship deadline:** Before any implementation PR is opened against `release/m16` for #153
**Test file:** `frontend/tests/e2e/m16-g9-delta-choropleth-overlay.spec.ts`
**Acceptance criteria covered:** AC-1 through AC-6

**Sequencing note:** Implementation may not begin until G1 merges to `release/m16`.
Tests must be authored from this document before implementation code is written.

**Soft-skip guard (NM-056 follow-up):** No `test.skip()` or conditional skip patterns.

**QA Lead acknowledgment:**
`[ ]` QA Lead: Tests for AC-1 through AC-6 authored and filed. [Date]

---

*Intent document authority: `docs/process/intent-template.md` (version 2026-06-17).
Sprint entry: `docs/process/sprint-plans/m16-g9-sprint-entry.md` (EL Approved 2026-06-24).
ADR authority: None (#153 within DeltaChoropleth component boundary).
Implementing agent: Frontend Architect Agent.
G9 capacity gate: Carry to M17 if capacity is exhausted before G8 is scheduled.*
