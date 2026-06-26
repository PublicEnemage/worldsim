---
name: m18-gd-sprint-entry
type: sprint-entry
milestone: M18 — Full Argument and Demo 7
sprint-group: GD
status: Filed — coordination artifact; GD Phase 1 authorized to begin immediately per sprint plan EL approval
authored-by: PM Agent
authored-date: 2026-06-26
el-approved: false
release-branch: release/m18
sop-reference: docs/process/sprint-planning-sop.md
---

# Sprint Entry — M18, GD: Control Plane Design Package

**Status:** Filed — coordination artifact (see SOP exception note below)
**Date authored:** 2026-06-26
**Release branch:** `release/m18`
**Sprint plan:** `docs/process/sprint-plans/m18-sprint-plan.md` (EL-approved 2026-06-26, PR #1364)

**SOP exception note:** Per `docs/process/sprint-plans/m18-sprint-plan.md §Sprint Entry Gate Requirements`, GD design phases are exempt from the sprint entry requirement — "these are design work only — no implementation code. Artifacts are committed to `docs/` branches and filed via PRs targeting `release/m18`. The EL gate is Artifact 5 (#1359) approval." This document is a voluntary coordination artifact that records scope, phase sequencing, NM sweep, and EL acknowledgment. It does not gate or block any GD phase.

**The binding GD gate is Artifact 5 (#1359):** EL must approve the scope decision document before ADR-019 may be authored and before any G4 implementation sprint entry may be filed.

---

## Section 1 — Sprint Identification

| Field | Value |
|---|---|
| Milestone | M18 — Full Argument and Demo 7 |
| GitHub Milestone | #19 |
| Sprint group | GD — Control Plane Design Package (Pre-wave design) |
| Release branch | `release/m18` |
| Sprint sub-branch | N/A — design artifact branches target `release/m18` directly; no sprint sub-branch |
| Sprint plan document | `docs/process/sprint-plans/m18-sprint-plan.md` |
| Exit checklist issue | #1340 |
| Sprint journal issue | N/A — pre-wave design phase; no journal issue required |
| Sprint groups in scope | GD only |
| Wave coordination tier | **Standard** — GD + GR pre-wave + G1 + G2 Wave 1 = 4 of 5 concurrent groups; Standard tier |
| Concurrent groups at entry | 2 of 5 at pre-wave entry (GD + GR); 4 of 5 when Wave 1 opens (GD + GR + G1 + G2) |
| Cross-group dependencies | GD outputs gate G4: ADR-019 accepted (Artifact 6, #1360) and EL scope decision (Artifact 5, #1359) must precede G4 sprint entry. GD does not block G1, G2, or GR. |

---

## Section 2 — Entry Invariants Checklist

*GD is a design-only phase — no implementation PRs open under this entry.
Sections 2.3 and 2.4 are inapplicable; see notes.*

### 2.1 — Structural gates

- [x] **Release branch exists:** `release/m18` cut from `main` 2026-06-26 (commit 8cffc86 after sync PR #1366 merged)
- [x] **CI trigger verified:** `.github/workflows/ci.yml` `pull_request: branches` includes `release/m*` — confirmed 2026-06-26. GD artifact PRs target `release/m18` directly; CI triggers on those PRs.
- [x] **Sprint plan EL-approved:** `docs/process/sprint-plans/m18-sprint-plan.md` EL-approved 2026-06-26 (PR #1364). GD Phase 1 (#1355 + #1357) authorized to begin immediately per EL approval note.

### 2.2 — ADR prerequisite gate

GD produces ADR-019 (Artifact 6, #1360) — it does not consume one. No ADR gates any GD design phase.

| Group | Required ADR | ADR status | Gate |
|---|---|---|---|
| GD — all design phases | None | N/A — ADR-019 is a GD output, not a prerequisite | **CLEAR** |

- [x] No ADR prerequisites for GD. Gate: **CLEAR**.

**Internal sequencing constraint on ADR-019 authorship:** ADR-019 (ARCH-013, ASSIGNED in backlog) may not be authored until Artifacts 2 (#1356), 4 (#1358), and 5 (#1359) are on record and EL has approved Artifact 5. This is an internal GD sequencing constraint, not a gate at entry.

### 2.3 — Intent document gate

**N/A — Design sprint.** GD produces design artifacts only (audit, specification, scope decision, ADR, journey updates). Intent documents are required for implementation deliverables. No intent documents are required for GD's 7 artifacts.

*Exception: Artifact 5 (#1359) is filed at `docs/process/intents/M18-GD-{date}-control-plane-scope-decision.md` — it uses the intents directory by convention as a scope decision document, not as an implementation intent. The agent-execution-lifecycle Step 1 obligation does not apply to design-phase artifacts.*

### 2.4 — QA test authorship gate

**N/A — Design sprint.** GD produces no implementation code. QA test authorship applies to G4 (the implementation group enabled by GD outputs) and will be addressed in the G4 sprint entry.

---

## Section 3 — Scope Declaration

### 3.1 — Issues in scope

GD operates in four sequential phases. All 8 issues are in GD scope.

| Issue | Title | Phase | Priority | Observable deliverable |
|---|---|---|---|---|
| #1354 | Control Plane Design Package (parent) | All phases | Immediate | Parent issue closed when all 7 artifacts filed and Artifact 5 EL-approved |
| #1355 | Artifact 1 — Current State Audit | Phase 1 (immediate) | **Immediate** | Filed at `docs/architecture/reviews/ARCH-REVIEW-008-m18-control-plane-current-state.md`; gaps between current `InstrumentCluster.tsx` column 3, `ControlPlane.tsx`, and `TrajectoryView.tsx` documented against the reserved column specification |
| #1357 | Artifact 3 — Customer Agent Layer 3 Assessment | Phase 1 (immediate) | **Immediate** | Filed at `docs/ux/usability-sessions/synthesis/`; Personas 2 (Eleni) and 5 (Aicha) evaluated against the current control plane gap; kryptonite check on record |
| #1356 | Artifact 2 — Target State Specification | Phase 2 (after #1355) | Near-term | Update to `docs/ux/information-hierarchy.md §Control Plane Reserved Zone`; full column vision for Mode 2 + Mode 3 specified; blue/orange visual system documented; form layouts, history list, and shock taxonomy defined |
| #1358 | Artifact 4 — Delta Analysis and Dependency Map | Phase 2 (after #1355) | Near-term | Named analysis document filed at `docs/architecture/`; gap between current and target quantified; implementation sequencing and ADR-019 scope boundary defined |
| #1359 | Artifact 5 — Scope Decision Document (EL gate) | Phase 3 (after #1356 + #1358) | Near-term | Filed at `docs/process/intents/M18-GD-{date}-control-plane-scope-decision.md`; EL records Mode 2 column scope decision, shock taxonomy M18 vs. deferred decision, and EX-001 disposition |
| #1360 | Artifact 6 — ADR-019: Control Plane Column | Phase 4 (after EL approves #1359) | Near-term — gates G4 | `docs/adr/ADR-019-control-plane-column.md` authored and accepted; Tier 1 — requires independent UX Designer sign-off in EL-triggered separate session (NM-042 compliance) |
| #1361 | Artifact 7 — Journey C update + Journey A GA-02 resolution | Phase 4 (after ADR-019 initiated) | Near-term | Update to `docs/ux/user-journeys.md §Journey C: Active Control` and `§Journey A GA-02`; journey updated to reflect ADR-019 scope decisions |

**Note on ARCH-REVIEW-008 numbering:** The current `docs/architecture/reviews/` directory has a numbering collision at 007 (`ARCH-REVIEW-007-m17-n3-assessment.md` and `ARCH-REVIEW-007-milestone15.md`). Artifact 1 uses 008 as the next sequential number. The implementing agent must confirm this number has not been taken before filing.

### 3.2 — Issues explicitly out of scope

| Issue | Title | Rationale for exclusion |
|---|---|---|
| #1217 | Mode 3 render optimization | G4 (Wave 2 implementation) — blocked until ADR-019 accepted |
| Any control plane implementation code | — | GD produces design artifacts only; code implementation is G4 scope |
| #1254 | CI bands on Zone 1A | G1 — Wave 1 independent group |
| #1255 | PSP driver decomposition | G2 — Wave 1 independent group |
| #1349 | Counter-scenario comparison | G3 — Wave 2 group blocked on GR close |
| #1352 | Requirements phase for #1349 | GR — separate pre-wave group |

---

## Section 4 — ADR Prerequisite Summary

| Group | ADR required | ADR status | Design may begin? |
|---|---|---|---|
| GD — all design phases | None | N/A | Yes — authorized immediately per sprint plan EL approval 2026-06-26 |

**GD outputs that are ADR prerequisites for downstream groups:**

| Downstream group | GD output required | ADR gate detail |
|---|---|---|
| G4 (Wave 2 implementation) | ADR-019 accepted (Artifact 6, #1360) | G4 implementation PR may not open until ADR-019 is accepted with independent UX Designer sign-off in separate EL-triggered session |

**Internal GD phase sequencing:**

| Phase | Precondition | Status |
|---|---|---|
| Phase 1 (#1355 + #1357) | Sprint plan EL-approved | **Authorized — begin immediately** |
| Phase 2 (#1356 + #1358) | Artifact 1 (#1355) filed | After Artifact 1 complete |
| Phase 3 (#1359) | Artifacts 2 (#1356) + 4 (#1358) both filed | After Artifacts 2 + 4 complete |
| Phase 4 (#1360 + #1361) | EL approves Artifact 5 (#1359) | After EL scope decision |

---

## Section 5 — Near-Miss Sweep

**Near-miss sweep date:** 2026-06-26
**Sweep period:** M17 exit ceremony (2026-06-26) through GD sprint entry filing (2026-06-26)

| Finding | Category | PI Agent register call issued? | NM entry number |
|---|---|---|---|
| No new process gaps identified. NM-066 through NM-071 all resolved before M18 kickoff. M18 entry blockers cleared. GD is design-only — implementation risk patterns (lint gate, output path coverage) do not apply to this phase. | N/A | N/A | N/A |

---

## Section 6 — Sprint Group Isolation (M18 onward)

*GD operates under modified isolation rules per the pre-wave design exception in the sprint plan.*

### 6.1 — Sprint sub-branch

GD does not use a sprint sub-branch. Design artifacts are committed on short-lived feature branches targeting `release/m18` directly, one per artifact (or grouped where sequencing permits). Branch naming convention: `docs/m18-gd-artifact-N-short-name`.

| Field | Value |
|---|---|
| Sprint sub-branch | N/A — GD artifact branches target `release/m18` directly |
| Branch naming convention | `docs/m18-gd-artifact-N-short-name` |
| Sprint journal issue | N/A — pre-wave design phase |

### 6.2 — File-conflict risk assessment

GD writes to documentation files only. No conflict risk with G1 (TrajectoryView.tsx / banding engine), G2 (Zone 1D / PSP module), or GR (requirements artifacts in `docs/ux/`).

| File | Lane required | Trigger |
|---|---|---|
| `docs/architecture/reviews/ARCH-REVIEW-008-m18-control-plane-current-state.md` (new) | GD docs branch | Artifact 1 |
| `docs/ux/usability-sessions/synthesis/` (new file) | GD docs branch | Artifact 3 |
| `docs/ux/information-hierarchy.md` | GD docs branch | Artifact 2 — §Control Plane Reserved Zone update |
| `docs/architecture/` (new named delta analysis document) | GD docs branch | Artifact 4 |
| `docs/process/intents/M18-GD-{date}-control-plane-scope-decision.md` (new) | GD docs branch | Artifact 5 |
| `docs/adr/ADR-019-control-plane-column.md` (new) | GD docs branch | Artifact 6 |
| `docs/ux/user-journeys.md` | GD docs branch | Artifact 7 — Journey C + GA-02 update |
| `SESSION_STATE.md` | PM Agent coordination lane | Sprint exit cockpit update |
| `docs/process/near-miss-registry.md` | PM Agent coordination lane (PI Agent authors) | If NM identified during GD phases |
| `docs/compliance/scan-registry.md` | PM Agent coordination lane | If compliance scan produced |

**Read-only access (no conflict risk):**

| File | Purpose |
|---|---|
| `frontend/src/components/InstrumentCluster.tsx` | Artifact 1 audit — read to document current column 3 state |
| `frontend/src/components/ControlPlane.tsx` | Artifact 1 audit — read to document current Mode 3 bottom-bar implementation |
| `frontend/src/components/TrajectoryView.tsx` | Artifact 1 audit — read to document current trajectory marker gaps |

**Potential write conflict:** `docs/ux/information-hierarchy.md` is also referenced by GR (#1352 requirements phase). PM Agent must coordinate if GR and GD Phase 2 both need to update this file in the same window. GR's write (if any) should target requirements capture sections; GD Artifact 2 targets §Control Plane Reserved Zone. Conflict risk is low but must be confirmed before both branches open.

### 6.3 — Infrastructure dependency declaration

- [x] No DS-owned file changes required. All GD writes are to documentation files.

#### 6.3a — New output paths declaration

- [x] No new output directories introduced by GD. GD produces `docs/` files only — no generated artifacts, no test outputs.

### 6.4 — Cross-group dependency declaration

- [x] GD does not depend on any active sprint group's output to begin Phase 1.

**GD outputs that gate downstream groups (non-blocking to GD itself):**

| Downstream group | GD artifact required | When needed |
|---|---|---|
| G4 (Wave 2) | Artifact 5 EL-approved (#1359) | Before G4 sprint entry is filed |
| G4 (Wave 2) | ADR-019 accepted (#1360) | Before G4 implementation PR opens |

### 6.5 — Prior NM verification

**NM verification sweep date:** 2026-06-26
**Sweep period:** M17 exit through GD sprint entry

| NM entry | Process improvement required | Applied in this sprint? |
|---|---|---|
| NM-069 | New output directories covered by `.gitignore` in same PR or DS infra lane | Yes — GD produces `docs/` files only; no new output directories; §6.3a confirmed |
| NM-070 | Pre-push hook enforcing ruff + mypy + npm build | N/A — GD produces no code; pre-push hook not exercised by design artifact commits. Applies to G4 implementation and will be verified in G4 sprint entry. |
| NM-071 | Wave concurrency ceiling check at wave kickoff | Yes — 4 concurrent groups at peak (GD + GR + G1 + G2) = Standard tier; ceiling confirmed in §1 |
| NM-068 | Prior NM verification field in sprint entry | Yes — this section (§6.5) |

---

## EL Approval Record

**EL approval:** Pending — acknowledgment of coordination artifact

*Per sprint plan §Sprint Entry Gate Requirements, EL approval of this document is not a gate for GD Phase 1 — the sprint plan EL approval (PR #1364, 2026-06-26) already authorizes all GD phases to begin. The binding EL gate for GD is Artifact 5 (#1359) approval. This record acknowledges the scope as filed.*

> {EL acknowledgment — or "Acknowledged: GD scope and phase sequencing as filed. GD Phase 1 (#1355 + #1357) may proceed."}
> — @PublicEnemage ({date})
