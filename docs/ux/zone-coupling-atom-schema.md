# Zone 1/2 Coupling Zustand Atom Schema

**Author:** Frontend Architect (consulted: Chief Engineer, UX Designer)
**Date:** 2026-06-03
**Authority:** ARCH-REVIEW-006 AR-006-B-011, AR-006-B-015
**EL sign-off:** Accepted 2026-06-03
**Closes:** Issue #609
**Prerequisite for:** All Zone 1 and Zone 2 US-048 implementation work

---

## Purpose

US-048 (X-ray interactive graph) requires bidirectional coupling between Zone 1
(trajectory view) and Zone 2 (X-ray graph). This document specifies the Zustand atom
schema that serves as the shared contract between the two zones, including update
semantics and circular-update prevention approach.

No Zone 1 or Zone 2 component may be modified for US-048 until this atom schema is
agreed and this document is accepted.

---

## 1. Atom Name and Location

**Atom name:** `zone2Selection`

**File location:** `frontend/src/store/zone2SelectionAtom.ts`

This atom is a new addition to the Zustand store. It must not be embedded in an existing
atom (e.g., `useSimStore`) — it is a cross-zone bridge atom and must be independently
importable by both Zone 1 and Zone 2 components.

---

## 2. TypeScript Type Definition

```typescript
/** Indicator key as used in the simulation attribute map (e.g., "gdp_growth_rate"). */
type IndicatorKey = string;

/** Simulation step index (0-based integer matching the scenario step axis). */
type StepIndex = number;

interface Zone2SelectionState {
  /**
   * The indicator key of the node currently selected in Zone 2 (X-ray view).
   * null means no node is selected — Zone 1 renders all curves at full opacity.
   */
  selectedIndicatorKey: IndicatorKey | null;

  /**
   * The step index currently under the Zone 1 trajectory cursor.
   * null means the cursor is not active (user is not hovering over Zone 1).
   * Zone 2 uses this to update node value badges for the current step.
   */
  cursorStep: StepIndex | null;
}

interface Zone2SelectionActions {
  setSelectedIndicatorKey: (key: IndicatorKey | null) => void;
  setCursorStep: (step: StepIndex | null) => void;
  clearSelection: () => void;
}

type Zone2SelectionSlice = Zone2SelectionState & Zone2SelectionActions;
```

### 2.1 Initial State

```typescript
const initialZone2SelectionState: Zone2SelectionState = {
  selectedIndicatorKey: null,
  cursorStep: null,
};
```

---

## 3. Update Semantics

### 3.1 Who writes `selectedIndicatorKey`

| Writer | Condition | Action |
|---|---|---|
| Zone 2 component | User clicks a causal graph node | `setSelectedIndicatorKey(node.indicatorKey)` |
| Zone 2 component | User clicks background (deselect) | `setSelectedIndicatorKey(null)` |
| Zone 2 component | Scenario step changes | `setSelectedIndicatorKey(null)` — clear stale selection |

Zone 1 **reads** `selectedIndicatorKey`. It does not write it.

### 3.2 Who writes `cursorStep`

| Writer | Condition | Action |
|---|---|---|
| Zone 1 component | User hovers over trajectory view | `setCursorStep(stepIndex)` |
| Zone 1 component | User moves cursor out of trajectory view | `setCursorStep(null)` |

Zone 2 **reads** `cursorStep`. It does not write it.

### 3.3 `clearSelection`

`clearSelection` is a convenience action that sets both fields to null. It is called
when the user navigates away from a scenario or a new scenario is loaded.

---

## 4. Circular Update Prevention

The circular update risk is:

```
Zone 2 writes selectedIndicatorKey
  → Zone 1 highlights curve (read, no write)
  → Zone 1 writes cursorStep (on hover, not triggered by Zone 2 action)
  → Zone 2 updates badge (read, no write)
```

**There is no circular update risk** because:

1. Zone 2 writes `selectedIndicatorKey`. Zone 1 reads it but does not write back.
2. Zone 1 writes `cursorStep`. Zone 2 reads it but does not write back.
3. The two write paths are triggered by independent user actions (click in Zone 2 vs.
   hover in Zone 1). Neither write path is triggered by a read of the other field.

The atom schema enforces this asymmetry: `selectedIndicatorKey` is written only by
Zone 2 event handlers; `cursorStep` is written only by Zone 1 event handlers. No
subscriber to either field writes to the other field in its update callback.

**Chief Engineer review note:** The asymmetry is structural — Zone 2 has no
`setCursorStep` call site; Zone 1 has no `setSelectedIndicatorKey` call site. A code
review check (or a lint rule disallowing cross-zone atom writes) can enforce this
invariant mechanically.

---

## 5. Interaction Model Decisions (AR-006-B-015)

These decisions feed directly into the component implementations that use this atom.

| Dimension | Decision | Rationale |
|---|---|---|
| Trigger | **Click for persistent selection; hover for transient local highlight only** | See `docs/ux/zone-2-interaction-standard.md §2. Hover Behavior` |
| Selection cardinality | **Single-node (M11)** | Multi-node deferred; single-node schema (`IndicatorKey | null`) is sufficient |
| Zone 1 feedback | **Opacity contrast** (selected: 100%; non-selected: 25%) | Draws attention without mechanical scrolling; see Zone 2 interaction standard §4.3 |
| Zone 1 does not scroll | Confirmed | Scrolling would disrupt user visual context |
| Zone 1 does not show callout | Confirmed | Opacity contrast is sufficient |

---

## 6. Migration from Existing Store

The `zone2Selection` atom is a new slice. It does not modify any existing Zustand atom
or store slice. Zone 1 and Zone 2 components that currently have no cross-zone state
dependency may import this atom independently without modifying shared store structure.

---

## 7. Testing Requirements

| Test | Type | Assertion |
|---|---|---|
| `setSelectedIndicatorKey` updates state | Unit | State transitions from null → key; key → null; key → different key |
| `setCursorStep` updates state | Unit | State transitions from null → step index; step index → null |
| `clearSelection` resets both fields | Unit | Both fields are null after clearSelection |
| Zone 1 renders ghost curves when `selectedIndicatorKey` is non-null | Component | Opacity of non-selected curves is 25% |
| Zone 1 renders all curves at full opacity when `selectedIndicatorKey` is null | Component | All curves at 100% opacity |
| Zone 2 does not write `cursorStep` | Static / code review | No `setCursorStep` call in Zone 2 component files |
| Zone 1 does not write `selectedIndicatorKey` | Static / code review | No `setSelectedIndicatorKey` call in Zone 1 component files |

---

## 8. Cross-References

- `docs/ux/zone-2-interaction-standard.md` — Zone 2 interaction model (trigger,
  cardinality, feedback) that this atom schema implements
- `docs/architecture/reviews/ARCH-REVIEW-006-milestone10.md §AR-006-B-011` — originating
  blindspot
- `frontend/src/store/` — existing Zustand store for reference on slice conventions
