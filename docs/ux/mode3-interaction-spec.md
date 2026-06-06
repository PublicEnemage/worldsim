# Mode 3 Interaction Spec — Parameter Change → Recompute → Trajectory Update

**Issue:** #614
**Author:** UX Designer Agent
**Consulted:** Chief Engineer Agent (latency budget, #613), Frontend Architect Agent
**Date:** 2026-06-05
**Status:** ACCEPTED — unblocks G6b (Mode 3 Active Control) implementation

> **Scope:** This document specifies the interaction design for the Mode 3
> parameter-change flow. It answers the four questions posed in Issue #614
> and establishes the Zustand store contract that Mode 3 implementation must
> satisfy. It does not specify the control plane layout or the set of
> configurable parameters — those are G6b implementation decisions.

---

## 1. Latency Budget

"Real-time" in US-039 is replaced with an explicit latency budget derived from
hardware measurements on the ProBook i5-8265U (the Equitable Build Process
target — 4 cores, 8 GiB RAM).

**Measured engine throughput (Phase 1 benchmarks, Issue #514):**
- Pure compute per step, 1 entity, sparse graph: ~0.07 ms on ProBook
- Pure compute per step, 5 entities, moderate graph: ~1.5 ms on ProBook

**Branch recompute budget (including DB I/O):**
The branch operation (`POST /scenarios/{id}/branch`) creates a new scenario
row and copies existing snapshots. Each subsequent `run_single_step()` call
on the branch includes snapshot read + propagate + snapshot write.

| Phase | Estimated latency (ProBook) |
|---|---|
| Branch creation (snapshot copy + new row) | ≤ 200 ms |
| Per-step recompute (DB I/O + propagation, 1–5 entities) | ≤ 250 ms/step |
| Total for 4 remaining steps (branch at step 4 of 8) | ≤ 1200 ms |
| Total for 7 remaining steps (branch at step 1 of 8) | ≤ 1950 ms |

**Ruling:** Mode 3 recompute is a **sub-2-second batch operation**, not a
sub-100ms interactive update. The UX must never imply instant feedback —
the instrument cluster must remain navigable during the full recompute window
without showing a blocking state.

This replaces "real-time" in US-039 with: *"parameter change triggers a
branch recompute that completes within 2 seconds on the ProBook target
hardware for scenarios up to 8 steps and 5 entities."*

---

## 2. Interaction Model Overview

Mode 3 uses the **new-scenario-object** model confirmed by the CE assessment
(#613). A parameter change creates a new branch scenario in the database and
recomputes forward from the branch point. The frontend holds two scenario IDs
simultaneously: `baselineScenarioId` and `branchScenarioId`.

**Session lifecycle:**

```
User opens Mode 3 (scenario at step T, all steps complete or in progress)
   │
   ├─ No control input yet → single trajectory, 100% opacity, no ghost curves
   │
   └─ User applies first parameter change
         │
         ├─ POST /scenarios/{baselineId}/branch → branchScenarioId created
         │
         ├─ LOADING STATE begins (see §3)
         │
         ├─ run_single_step() × (n_steps − branch_step) on branchScenarioId
         │
         └─ ACTIVE STATE: baseline ghost (50% opacity) + active curves (100%)
               │
               └─ User applies additional parameter change
                     │
                     └─ New input added to branchScenarioId at changed step
                           run_single_step() from changed step forward
                           LOADING STATE restarts (see §5 — Re-branch)
```

The baseline scenario is never mutated. `baselineScenarioId` is set once
when the user enters Mode 3 and does not change for the session.

---

## 3. Recompute Loading State

### 3a. What the instrument cluster shows during recompute

The instrument cluster must remain **fully navigable** during recompute.
No blank state, no blocking spinner, no instrument lockout.

| Element | During recompute | After recompute |
|---|---|---|
| Trajectory view | Baseline curves at 100% opacity; no ghost curves | Baseline ghost (50% opacity); active branch curves (100%) |
| Recompute badge | Visible in instrument cluster header: "Recomputing…" with animated pulse indicator | Hidden |
| Step progress indicator | "Computing step X of N…" below badge | Hidden |
| Advance step button | Disabled | Re-enabled (if branch is not yet complete) |
| MDA alert panel | Shows baseline alerts (last completed step) | Shows branch alerts |
| PMM widget | Shows baseline PMM value | Shows branch PMM value |
| Four-framework zone | Shows baseline framework scores | Shows branch framework scores |

**Rationale:** The baseline trajectory is authoritative data. The user needs
to be able to read it — MDA alerts, threshold crossings, PMM score — while
the branch is computing. Graying out or hiding instruments during recompute
defeats the purpose of the comparison: the user cannot evaluate the delta if
they cannot see the baseline state.

### 3b. Streaming step reveal

As each `run_single_step()` call completes on the branch scenario, the
frontend should update the branch trajectory incrementally — not wait for
all steps to complete before rendering.

Implementation: the frontend polls `GET /scenarios/{branchId}` on a 500ms
interval during recompute. When `max_step` on the branch advances, the
trajectory view extends the active branch curves to the new step. This gives
a "growing trajectory" visual that confirms recompute is progressing.

**Polling must stop** when branch `status == "completed"` or `status ==
"failed"`.

---

## 4. Ghost Baseline Visual Specification

Formalizes ADR-008 Decision 10 with Mode 3-specific extensions.

**Before any control input (observation mode):**
- Single trajectory set at 100% opacity, 2px stroke
- No ghost curves
- No comparison state
- Instrument cluster instruments show baseline values

**After branch recompute completes (active comparison mode):**

| Visual element | Specification |
|---|---|
| Baseline curves (ghost) | Same hue as active curve per framework; 50% opacity; 1px stroke; dashed line style |
| Active branch curves | 100% opacity; 2px stroke; solid line style |
| Divergence fill | Area between baseline and active curves; 8% opacity fill in the framework's primary color; appears when `abs(delta) > 0.01`; disappears if trajectories re-converge |
| MDA floor lines | Overlaid on both baseline and active curves as horizontal dashed threshold lines; color per severity (CRITICAL: red, WARNING: amber) |
| Ghost curve interactivity | Hover/tap on ghost curve shows baseline value tooltip: `"Baseline: {value} at Step {n}"` |

**Dashed style for ghost curves** (amendment to ADR-008 D10 which specified
`1px stroke` without line style): The confidence tier visual system uses
`strokeDasharray` to indicate projected vs. historical data. Ghost baseline
curves are neither — they are confirmed historical baseline values. Use a
distinct dash pattern: `strokeDasharray="4 2"` (short dash, narrow gap).
This is visually distinct from the `strokeDasharray="8 3"` used for projected
confidence-degraded data.

---

## 5. Re-Branch Behavior

**Definition:** The user applies a second parameter change after a branch is
already active.

**Decision: accumulate into the existing branch.**

The existing `branchScenarioId` is preserved. The new parameter change is:
1. Added as a new `scenario_scheduled_input` on the branch scenario at the
   relevant step
2. The branch scenario's snapshots from that step onward are deleted
3. `run_single_step()` runs from the changed step forward on the existing
   branch scenario

**Rationale:**
- Consistent with ADR-008 D10: "the active trajectory accumulates all control
  inputs. The comparison always answers: what is the total effect of all my
  control inputs?"
- The baseline does not change between parameter changes — the ghost curves
  remain anchored to the original unmodified scenario
- Avoids proliferating scenario records (one branch per session, not one per
  parameter change)

**Re-branch loading state:** Identical to §3 — the LOADING STATE restarts
from the changed step. Branch curves up to the changed step remain visible;
curves from the changed step onward clear and rebuild as steps complete.

**Session boundary:** The branch scenario is abandoned (but not deleted) when
the user exits Mode 3 or selects a different scenario. The user is not
prompted to save — branches are persisted automatically in the DB and can be
retrieved by `branchScenarioId`. No explicit "save branch" action is required
for M12; a named-branch workflow is deferred.

---

## 6. Error State

If `branchScenarioId` transitions to `status == "failed"` during recompute:

| Element | Error state |
|---|---|
| Recompute badge | Changes to: "Recompute failed" with error icon (red); remains until dismissed |
| Trajectory view | Baseline curves restore to 100% opacity; branch curves cleared |
| Ghost curves | Cleared — no partial ghost display |
| MDA alerts, PMM, frameworks | Restore to baseline values |
| Advance button | Re-enabled on baseline scenario |
| Dismiss action | User taps/clicks the error badge to clear it; resets to pre-branch observation mode |

**No blocking modal.** The error badge is inline in the instrument cluster
header. The baseline scenario remains fully navigable. The user can attempt
another parameter change, which will create a new branch.

---

## 7. Zustand Store Contract

The Mode 3 store extension required by this spec. Frontend Architect Agent
owns the canonical store design; these are the fields and types this spec
requires to be present.

```typescript
interface Mode3State {
  // Set when user enters Mode 3; immutable for the session
  baselineScenarioId: string | null;

  // Created by POST /scenarios/{baselineId}/branch on first parameter change
  branchScenarioId: string | null;

  // Step from which the branch was created
  branchFromStep: number | null;

  // Steps computed on the branch so far (for streaming reveal)
  branchStepsComputed: number;

  // Recompute lifecycle
  recomputeStatus: 'idle' | 'pending' | 'computing' | 'complete' | 'failed';

  // Actions
  initBranch: (baselineId: string, branchId: string, fromStep: number) => void;
  updateBranchProgress: (stepsComputed: number) => void;
  setBranchComplete: () => void;
  setBranchFailed: () => void;
  resetBranch: () => void;
}
```

**State transitions:**

```
idle ──(first parameter change)──► pending
pending ──(POST /branch returns 201)──► computing
computing ──(all steps complete)──► complete
computing ──(scenario status == failed)──► failed
complete ──(second parameter change)──► computing  (re-branch)
failed ──(user dismisses error badge)──► idle
idle / complete / failed ──(user exits Mode 3)──► idle (resetBranch)
```

---

## 8. Open Questions Deferred to G6b Implementation

The following questions are out of scope for this spec and must be resolved
by the Frontend Architect Agent during G6b implementation:

- **Control plane layout:** Which parameters are exposed in `zone-control-plane`
  and in what order. This is a data decision (what parameters the engine
  supports), not a UX flow decision.
- **Branch persistence UI:** Whether completed branches are listed anywhere
  (e.g., in the Scenarios panel). Deferred — no named-branch workflow in M12.
- **Multi-user branch conflicts:** Out of scope for M12 (single-user sessions).
- **Step axis annotation in Mode 3:** Whether step markers show baseline or
  branch calendar dates when the two trajectories diverge. Default: show
  baseline calendar dates (the step axis is shared; the branch does not change
  the timeline, only the trajectory values).
