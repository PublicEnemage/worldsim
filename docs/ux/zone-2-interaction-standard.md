# Zone 2 Interaction Design Standard

**Author:** UX Designer (consulted: Frontend Architect)
**Date:** 2026-06-03
**Authority:** ARCH-REVIEW-006 AR-006-B-016
**EL sign-off:** Accepted 2026-06-03
**Closes:** Issue #612
**Prerequisite for:** All Zone 2 interactive surfaces, beginning with US-048 (X-ray
interactive graph)

---

## Purpose

US-048 is the first Zone 2 interactive surface in WorldSim. Zone 2 currently renders
static geographic context (choropleth) with no interactive model. This standard defines
the interaction patterns for Zone 2 before any US-048 component work begins, so that
US-048 does not establish an ad-hoc pattern that conflicts with future Zone 2 surfaces.

This is a design standard document, not an ADR. It defines interaction behavior —
not computation or data architecture.

---

## 1. Zone 2 Multi-View Model (EL Decision — AR-006-B-012)

**Decision: Option A — Switchable Zone 2.** Accepted 2026-06-03.

Zone 2 is a multi-view zone. The user selects between available views (Geographic View,
X-Ray View) via a control rendered at the Zone 2 panel header. Zone 2 remains a single
panel with different rendering modes.

**Rationale:** Option A is architecturally consistent with CLAUDE.md §UX Architectural
Commitment 2 ("context is navigable"). Zone 2 is the contextual navigation zone. A
switchable Zone 2 extends that model — additional context views are navigable surfaces
within the zone, not new zones. Option B (separate X-Ray Panel) would introduce a new
zone, requiring EL sign-off per CLAUDE.md §UX Architectural Commitments and potentially
warranting an ADR. Option A requires neither.

**View selector UI:** A segmented control or tab row at the Zone 2 panel header, with
labels "Geographic" and "X-Ray". Default state on scenario load: Geographic view.

---

## 2. Hover Behavior

| Surface | Hover behavior |
|---|---|
| Causal graph node (X-Ray view) | Transient highlight — node brightens, adjacent edges highlight at reduced opacity. No persistent state change. |
| Causal graph edge (X-Ray view) | Edge label and confidence tier badge appear on hover. No persistent state change. |
| Choropleth region (Geographic view) | Existing behavior unchanged — tooltip with entity name and indicator value. |

**Hover does not trigger Zone 1 interaction.** Hover is local to Zone 2. Only click
triggers cross-zone communication.

**Rationale:** Transient hover-driven Zone 1 updates would cause continuous Zone 1
repaints as the user moves the cursor across Zone 2. This creates visual noise and
competes with the Zone 1 trajectory cursor (which is already a hover-driven interaction).
Restricting Zone 1 → Zone 2 and Zone 2 → Zone 1 communication to click events gives
users deliberate control over the cross-zone highlight state.

---

## 3. Click Behavior

### 3.1 Selection Cardinality: Single-Node

**Decision: Single-node selection only (M11).** Multi-node selection is deferred to M12
or later. Rationale: multi-node selection highlights multiple trajectory curves
simultaneously — the interaction model and Zone 1 rendering behavior for multiple
simultaneous highlights are unspecified, and specifying them in M11 adds scope without
a confirmed M11 user story.

### 3.2 Click → Persistent Selection

Clicking a node in the X-ray view:
1. Sets the node as the **selected node** in the Zone 1/2 coupling atom (see
   `docs/ux/zone-coupling-atom-schema.md`).
2. The selected node state persists until: the user clicks a different node, the user
   clicks the background (deselects), or the scenario step changes.
3. The Zone 2 panel renders the selected node with a persistent highlight (filled circle,
   selection ring, or equivalent — specific visual token is an implementation detail).

### 3.3 Click → Background (Deselect)

Clicking anywhere in Zone 2 that is not a node or edge clears the selected node state.
Zone 1 returns to its default display (no trajectory curve highlighted).

### 3.4 Click on Edge

Edges are not selectable. Clicking an edge has no persistent effect. Edge click shows
a tooltip (edge weight, confidence tier, direction) that dismisses on next click.

---

## 4. Zone 1/2 Communication Protocol

### 4.1 Direction

Zone 2 → Zone 1 (primary): A node selection in Zone 2 highlights the corresponding
trajectory curve in Zone 1.

Zone 1 → Zone 2 (reverse): Moving the Zone 1 trajectory cursor (step hover) highlights
the corresponding node in Zone 2 — specifically, the node's value badge updates to
reflect the indicator value at the current cursor step.

### 4.2 Event Shape

Communication between zones occurs via the Zustand `zone2Selection` atom. The full
schema is in `docs/ux/zone-coupling-atom-schema.md`.

Zone 2 writes to `zone2Selection.selectedIndicatorKey` on node click.
Zone 1 reads `zone2Selection.selectedIndicatorKey` to determine which curve to highlight.
Zone 1 writes to `zone2Selection.cursorStep` on trajectory cursor hover.
Zone 2 reads `zone2Selection.cursorStep` to update node value badges.

### 4.3 Zone 1 Response to Zone 2 Node Selection

When `zone2Selection.selectedIndicatorKey` is non-null:

| Element | Behavior |
|---|---|
| Selected indicator curve | Full opacity, 3px stroke weight (default is 1.5px) |
| Non-selected indicator curves | Reduced to 25% opacity (ghost curves) |
| Zone 1 step cursor | Unchanged |
| Zone 1 legend | Selected indicator's legend entry is bolded |

Zone 1 does **not** scroll to the highlighted curve or show a callout. The opacity
contrast is sufficient to draw attention without mechanical scrolling, which would
disrupt the user's visual context.

### 4.4 Update Loop Prevention

See `docs/ux/zone-coupling-atom-schema.md §4. Circular Update Prevention`. Zone 1
reading `cursorStep` from the atom does not write back to the atom — the cursor position
is a read-only consumer of the step axis, not a writer. Zone 2 does not write to
`cursorStep` — only Zone 1 writes it. This asymmetry prevents circular updates.

---

## 5. Empty and Null State Behavior

| Condition | Zone 2 rendering |
|---|---|
| No scenario loaded | Zone 2 shows placeholder: "Select a scenario to view geographic and X-ray context." |
| X-Ray view selected, no causal graph data for current step | Zone 2 shows: "No causal graph data available for this step." Node list is empty. No edges rendered. |
| Geographic view, entity has no choropleth data | Existing behavior: entity renders in a neutral fill with tooltip "No data available." |
| Selected node in X-Ray view, corresponding indicator not in Zone 1 | Zone 1 does not highlight any curve. Zone 2 shows a tooltip on the selected node: "This indicator is not in the current trajectory view." |

---

## 6. Keyboard Navigation Requirements

Zone 2 interactive surfaces must meet WCAG 2.1 Level AA keyboard navigation baseline:

| Requirement | Implementation |
|---|---|
| Tab focus | All interactive nodes and the view selector are reachable via Tab. |
| Focus indicator | Visible focus ring on focused node (minimum 3px, high-contrast color). |
| Enter / Space to activate | Pressing Enter or Space on a focused node triggers the same selection behavior as click. |
| Escape to deselect | Pressing Escape while a node is selected clears the selection (equivalent to background click). |
| Arrow keys in graph | Arrow keys move focus between adjacent nodes (connected by an edge). If no adjacent node in arrow direction, focus wraps to the nearest node in that direction. |

Keyboard navigation for the choropleth (Geographic view) follows the existing
choropleth accessibility implementation.

---

## 7. Scope Boundary

This standard governs Zone 2 interactive surfaces. It does not govern:
- Zone 1 interaction model (trajectory cursor, step hover) — covered by ADR-010
- Mode 3 control plane interactions — deferred to M12
- Zone 2 in the choropleth (Geographic view), except where explicitly noted above

---

## Revision History

| Version | Date | Change | Authorised by |
|---|---|---|---|
| 1.0 | 2026-06-03 | Initial issue — closes Issue #612; includes Zone 2 multi-view EL decision (AR-006-B-012) | EL (@PublicEnemage) |
