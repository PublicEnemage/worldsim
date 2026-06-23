---
name: m16-g3-sprint-entry
type: sprint-entry
milestone: M16 — Distributional Visibility
sprint-group: G3
status: EL Approved 2026-06-23 — intent document and QA tests must be filed before implementation PR opens
authored-by: PM Agent
authored-date: 2026-06-23
el-approved: 2026-06-23
release-branch: release/m16
sop-reference: docs/process/sprint-planning-sop.md
---

# Sprint Entry — M16, G3: 25-Year Human Capital Depletion Trajectory

**Status:** EL Approved 2026-06-23 — intent document and QA tests must be filed before implementation PR opens
**Date authored:** 2026-06-23
**Release branch:** `release/m16`
**Sprint plan:** `docs/process/sprint-plans/m16-sprint-plan.md` (EL Approved 2026-06-23)

*Authority: `docs/process/sprint-planning-sop.md §Sprint Entry Gate` (Phase C output).
This entry gates G3 specifically. G3 delivers the 25-year human capital depletion trajectory
(#274) — the DemographicModule extension that closes the "for this long" argument in Demo 6
("this cohort, at this step, for this long"). G3 backend work may begin in parallel with
G2 frontend work once the CE Assessment (§2.5) and this entry document are EL-approved.
G3 BPO-acceptance is a prerequisite for G8 (live stakeholder demo #843 — M16 exit gate).*

---

## Section 1 — Sprint Identification

| Field | Value |
|---|---|
| Milestone | M16 — Distributional Visibility |
| GitHub Milestone | #17 |
| Sprint group | G3 — 25-Year Human Capital Depletion Trajectory |
| Release branch | `release/m16` |
| Sprint plan document | `docs/process/sprint-plans/m16-sprint-plan.md` |
| Exit checklist issue | #985 |
| Sprint groups in scope | G3 only |
| ADR gate | None — DemographicModule M4 extension within existing module boundary (Architect consultation, sprint plan §ADR Prerequisites) |
| CE assessment gate | §2.5 — embedded in this entry document (sprint plan §G3 additional gate) |
| Implementing agents | Chief Engineer Agent (backend DemographicModule extension + API parameter); Frontend Architect Agent (trajectory display — Zone placement per intent document) |
| Wave | Wave 2 — parallel with G2 backend; G8 gate (#843) requires G3 BPO-accepted |

---

## Section 2 — Entry Invariants Checklist

*All items must be checked before any implementation PR is opened for G3.
An unchecked invariant blocks implementation from beginning.*

### 2.1 — Structural gates

- [x] **Release branch exists:** `release/m16` cut from `main` 2026-06-23 (commit 07c92b8)
- [x] **CI trigger verified:** `.github/workflows/ci.yml` `pull_request: branches` includes
  `release/m*` — confirmed at M16 kickoff 2026-06-23. Required checks: `changes`, `lint`,
  `test-backend`, `playwright-e2e`, `compliance-scan`, `branch-naming`. KI-005 permanent fix
  (`do_not_enforce_on_create: true`) applied 2026-06-20 — no Ruleset workaround required.
- [x] **Sprint plan EL-approved:** `docs/process/sprint-plans/m16-sprint-plan.md`
  `el-approved: 2026-06-23` (PR #1148 merged 2026-06-23)

### 2.2 — ADR prerequisite gate

Per the Architect's consultation in the sprint plan: G3 (#274) requires no new ADR. The
DemographicModule extension remains within the M4 module boundary — #274 extends existing
per-step indicator computation without introducing a new module boundary, a new architectural
pattern, or a new inter-module dependency chain. No new ARCH backlog entry is required.

| Group | Required ADR | ADR status | Gate |
|---|---|---|---|
| G3 — #274 (25-year human capital trajectory) | None | N/A — M4 module boundary | **CLEAR** |

- [x] No ADR prerequisite for G3. Gate: **CLEAR**.

### 2.3 — Intent document gate

*An intent document must be filed before any G3 implementation PR opens.
(Authority: `docs/process/agent-execution-lifecycle.md` Step 1)*

- [x] Intent document filed for G3 deliverable — **FILED 2026-06-23**

| Deliverable | ADR reference | Intent document path | Filed? |
|---|---|---|---|
| #274 — 25-year human capital depletion trajectory | None (DemographicModule M4 boundary); CE Assessment §2.5 decisions are binding design inputs | `docs/process/intents/M16-G3-2026-06-23-25year-human-capital-trajectory.md` | **Yes — FILED 2026-06-23** |

**Completeness gate:** The QA Lead must be able to write backend and E2E tests for all G3
acceptance criteria from the intent document without reading implementation code. The intent
document must specify: (a) the API response shape for 100-step projection output (SimulationRequest
extension per CE Assessment Decision 2); (b) the Zone placement for the trajectory display in
the primary viewport — the BPO requirement is that the 25-year view is visible without drawer
navigation at 1280×800; (c) Layer 3 self-interpreting milestone sentence format and trigger
condition (first step where an indicator crosses its MDA floor); (d) the adaptive temporal
resolution override behavior (CE Assessment Decision 1: `adaptive_resolution: false` when
`projection_steps > 8`); (e) the Section 4b Visual Spec per `docs/process/sprint-planning-sop.md`
naming specific DemographicModule indicators and their milestone sentence templates.

**CM review pre-condition for intent document finalization (not sprint entry):** Per CE Assessment
Decision 3, a Chief Methodologist review comment on #274 is required before the intent document
finalizes its acceptance criteria for indicator selection. The CM must confirm: (a) which
DemographicModule indicators produce meaningful 25-year trajectories (not degenerate/bounded
monotone collapse); (b) whether the MDA-derived floor methodology from M15-G3 cohort design
applies directly to long-run projection, or requires a long-run calibration adjustment. This
review does not block sprint entry — it blocks intent document acceptance criteria finalization.

### 2.4 — QA test authorship gate

*QA tests must be authored from the intent document's acceptance criteria before
implementation code is written. (Authority: `docs/process/agent-execution-lifecycle.md` Step 2)*

- [x] QA test files authored for G3 before implementation begins — **AUTHORED 2026-06-23**

| Deliverable | Intent document | Test file path | Authored before implementation? |
|---|---|---|---|
| #274 — backend (100-step projection; indicator bounds; adaptive resolution override) | `docs/process/intents/M16-G3-2026-06-23-25year-human-capital-trajectory.md` | `backend/tests/test_m16_g3_25year_human_capital_trajectory.py` | **Yes — AUTHORED 2026-06-23** |
| #274 — frontend (trajectory display; step axis; Layer 3 milestone sentences) | (same intent document) | `frontend/tests/e2e/m16-g3-25year-human-capital-trajectory.spec.ts` | **Yes — AUTHORED 2026-06-23** |

*Soft-skip guard (NM-056 follow-up, M15 retrospective action 3a): neither test file may contain
`test.skip()` or conditional skip patterns. The 100-step backend projection test must not
soft-skip on backend startup failure — the G3 implementation PR must not merge until this test
runs and passes in CI. The M16 exit checklist (#985) confirms no active soft-skip patterns
before it closes.*

### 2.5 — Chief Engineer Assessment Gate (G3-specific)

*Required by `docs/process/sprint-plans/m16-sprint-plan.md §G3 additional gate`:
"CE assessment of 25-year projection feasibility (#274) must be filed (as a comment on #274
or a decision in the G3 sprint entry) before implementation begins."*

*Authored by the Chief Engineer Agent and embedded in the G3 sprint entry per the sprint plan
alternative to a separate #274 comment.*

---

**Chief Engineer Assessment — 25-Year Human Capital Projection Feasibility**
**Authored:** 2026-06-23
**Scope:** Issue #274 — DemographicModule extension for 100-step quarterly projection

#### CE-1 — Computation Feasibility on Target Hardware

Target hardware: 8GB RAM, 4-core CPU (GitHub Actions free-tier runner; local contributor floor
per CLAUDE.md §Equitable Build Process).

Current baseline: The ZMB ECF scenario runs ~8 steps. Per-step computation includes event-driven
feedback graph resolution across registered modules and DemographicModule per-step indicator
computation, O(indicators) per step, with trajectory state serialization.

At 100 quarterly steps (25 years):

- **Memory:** Trajectory state is a list of per-step snapshots. At 100 steps × ~40 indicators
  × 4 frameworks × `Decimal` values ≈ ~16,000 Decimal values per entity. Single-entity SEN
  scenario: well within 8GB budget. Multi-entity long-run projection is out of G3 scope —
  Demo 6 is single-entity (Senegal only).

- **CPU:** Extrapolating current per-step compute time to 100 steps gives an estimated wall
  time of 25–50 seconds end-to-end on 4-core hardware, within the 60-second operator
  experience ceiling.

- **Adaptive temporal resolution (PRIMARY FEASIBILITY RISK — HIGH):** The simulation engine
  auto-switches to daily resolution during crisis events. At daily resolution over a 25-year
  projection, a sustained crisis period could produce up to 9,125 daily steps, blowing both
  the memory budget and the 60-second ceiling. This must be addressed before implementation.

**Decision 1:** The 100-step projection mode must override adaptive temporal resolution.
The simulation engine must accept an `adaptive_resolution: false` flag when
`projection_steps > 8`. Quarterly resolution is fixed for the full 100-step run — no daily
resolution switching is permitted in long-run projection mode. This flag must be an explicit
parameter, not inferred; the implementing agent must not silently disable it via a constant.

**VERDICT: FEASIBLE** on target hardware for single-entity SEN projection at 100 steps,
subject to Decision 1.

#### CE-2 — Endpoint Architecture

Two options evaluated:

**Option A — Extend existing `/simulate` endpoint with `projection_steps` parameter.**
- Add `projection_steps: int | None` to `SimulationRequest` (default `None` → programme-length
  behaviour unchanged; no regression in existing scenarios)
- If `projection_steps` is provided and exceeds the programme-length default, the engine
  extends the step horizon and applies Decision 1 (adaptive resolution override)
- No new API endpoint; `api_contracts.yml` change is minimal: one optional integer field
  on `SimulationRequest`, capped at 100

**Option B — New `/project` endpoint.**
- Separate endpoint optimized for long-run demographic projection
- Higher implementation cost; API surface grows; new `api_contracts.yml` schema section
  required; no meaningful technical advantage over Option A for the G3 scope

**Decision 2:** Option A — extend existing `/simulate` endpoint with an optional
`projection_steps` parameter (integer, `1 ≤ projection_steps ≤ 100`). The computation is
identical to existing simulation; only the step horizon and adaptive resolution flag differ.
A new endpoint is not justified. `api_contracts.yml` must be updated in the same commit as
the backend implementation (schema drift rule — CLAUDE.md §Schema registry).

**VERDICT: No new endpoint required.** Existing `/simulate` endpoint extended with
`projection_steps` parameter.

#### CE-3 — DemographicModule Readiness and Indicator Bounds

DemographicModule (M4) covers human capital indicators: education enrollment, healthcare worker
retention, labor force participation, and income quintile distribution. Two concerns for
long-run projection:

1. **Indicator bounds at 100 steps:** If any indicator decay function is unbounded — i.e., not
   guaranteed to remain in [0.0, 1.0] across all 100 steps — long-run projection will produce
   degenerate outputs (negative values, super-unitary values, or runaway monotonic collapse).
   This must be validated before the implementation PR opens.

2. **SEN data availability:** SEN is seeded in `source_registry` (M15-G4, PR #1116, migration
   `2b821063ef81`). Human capital indicator values for SEN in the 100-step projection must be
   either real data (Path 1 approved source — World Bank) or synthetic (Tier 3 with per-indicator
   flag, per `docs/DATA_STANDARDS.md §Confidence Tier System`). Data preparation for the live SEN
   scenario is covered by #843 demo preparation and is not a G3 deliverable. G3 implementation
   tests must use a dedicated synthetic SEN fixture, not ZMB values transposed.

**Decision 3:** A Chief Methodologist review comment on #274 is required before the G3 intent
document finalizes its acceptance criteria. The CM must confirm: (a) which DemographicModule
indicators produce meaningful (non-degenerate, bounded) 25-year trajectories for the SEN
austerity scenario; (b) whether the MDA-derived floor methodology (from M15-G3 cohort design)
applies directly to 100-step projection or requires long-run calibration adjustment. This
review gates intent document AC finalization, not sprint entry.

**Decision 4:** The G3 intent document must require the implementing agent to perform a
dry-run of the SEN scenario at `projection_steps=100` before marking the implementation PR
ready for review, and to record: (a) end-to-end wall time on target hardware; (b) min/max
of each DemographicModule indicator across all 100 steps. Both must appear in the Step 4
Verify verdict. If any indicator is outside [0.0, 1.0] or wall time exceeds 60 seconds,
the Step 4 Verify verdict is FAIL and the implementation PR must not be marked ready.

**CE Assessment status: COMPLETE.** All four decisions are recorded. Implementation is feasible
subject to the four decisions above. This assessment satisfies the G3 sprint entry additional
gate per `docs/process/sprint-plans/m16-sprint-plan.md §G3 additional gate`.

---

## Section 3 — Scope Declaration

### 3.1 — Issues in scope

| Issue | Title | Priority | Observable application state (pre-implementation specification) |
|---|---|---|---|
| #274 | feat(simulation): 25-year human capital depletion trajectory | immediate / CRITICAL | At 1280×800 with the SEN scenario loaded in Mode 1, with `projection_steps=100` set in the simulation request: a 25-year human capital trajectory panel is visible in the primary viewport — accessible without opening a drawer, a tab, or navigating away from the instrument cluster (UX Architectural Commitment 2). The panel displays ≥3 DemographicModule indicators over 100 quarterly steps, each as a trajectory curve. At the first step where an indicator crosses its MDA floor, a Layer 3 self-interpreting milestone sentence is visible at L0 without hover or interaction (e.g., "by 2032 [step 24], education sector staffing in the bottom quintile falls below the recovery floor"). The panel labels the projection time horizon in human-readable terms ("25-year projection · quarterly resolution"). Any indicator derived from synthetic data carries a Tier 3 confidence badge adjacent to its curve endpoint. The Zone 1B step axis (or a dedicated sub-panel step axis) accommodates 100 steps at 1280×800 without content overflow — scroll or zoom within the panel is acceptable; displacement of Zone 1A, Zone 1C, or Zone 1D from the primary viewport is not. Projection run time from scenario load to panel render: ≤ 60 seconds on 4-core hardware. ADR-017 non-regression: the existing single-entity ZMB 8-step rendering path is not affected — Mode 1 with default step count loads and renders identically to pre-G3. Backend: `GET /simulate` with `projection_steps=100` returns a trajectory array of 100 step objects; with `projection_steps` omitted or ≤ programme-length, existing behaviour is unchanged. |

### 3.2 — Issues explicitly out of scope

| Issue / scope | Rationale for exclusion |
|---|---|
| Multi-entity long-run projection (N > 1 at 100 steps) | Demo 6 is single-entity (Senegal); multi-entity at 100 steps adds layout risk and memory risk not assessed in the CE Assessment; deferred to post-G3 or later milestone |
| SEN scenario data preparation (real human capital indicator values) | Covered by #843 demo preparation; G3 implementation tests use a synthetic SEN fixture; real-data integration is a demo prep task, not a G3 deliverable |
| Adaptive temporal resolution in long-run mode — new design | CE Assessment Decision 1 specifies disable-only (`adaptive_resolution: false`); designing an adaptive-resolution-aware long-run mode is out of scope; the flag is a simple override parameter |
| #986 — Cohort disaggregation on primary surface | G2 scope; G3 trajectory display is a separate primary-viewport element from G2's cohort rows |
| #987 — Political risk summary surface | G2 scope; Zone 1D is unchanged by G3 |
| #102, #275, #22 — Distributional infrastructure | G4 scope; capacity-allowing; not Demo 6 critical path |
| Zone 1D integration with 25-year trajectory | G3's human capital trajectory is a Zone 1B extension or primary-viewport sub-panel; Zone 1D (PSP evidence thread) is unaffected by G3 |
| Mode 2 or Mode 3 long-run projection | Mode 1 replay at extended horizon is the Demo 6 requirement; Mode 2/3 long-run projection involves control-plane interaction not assessed for 100-step depth; deferred |

**G3 is complete when:** All observable application states in Section 3.1 are confirmed in
the running SEN scenario at Step 4 Verify — including the 60-second performance ceiling
on target hardware, indicator bounds [0.0, 1.0] at all 100 steps (CE Assessment Decision 4
dry-run), Layer 3 milestone sentence visible at L0, and ADR-017 non-regression (ZMB 8-step
path unchanged); the Customer Agent Layer 3 assessment is on record; and the Business PO
has confirmed at Step 5 Validate that the Demo 6 argument "this cohort, at this step, for
this long" is completeable with the 25-year trajectory visible in the primary viewport
without drawer navigation.

---

## Section 4 — ADR Prerequisite Summary

| Group | ADR required | ADR status | Implementation may begin? |
|---|---|---|---|
| G3 — #274 (25-year human capital trajectory) | None — M4 DemographicModule extension; within existing module boundary per Architect consultation | N/A | Yes — after EL approves this entry, the intent document is filed incorporating the CE Assessment decisions (§2.5), and QA tests are authored |

No ADR prerequisite for G3. The CE Assessment (§2.5) is the G3-specific implementation gate.
Its four decisions are binding design inputs for the intent document.

---

## Section 5 — Near-Miss Sweep

**Near-miss sweep date:** 2026-06-23
**Sweep period:** M16 G1 BPO ACCEPT (2026-06-23) through G3 sprint entry filing (2026-06-23)

| Finding | Category | PI Agent register call issued? | NM entry number |
|---|---|---|---|
| No new process gaps identified in the sweep period. G1 BPO ACCEPT and #1162/#1163 filing completed in the same session with no SOP deviations. NM-056 follow-up (soft-skip prevention) addressed in §2.4. G2 pre-conditions remain open (CM/DA/ARF/FA sign-offs on #986/#987) — these are planned pre-conditions, not gaps. No new NM entry required. | N/A | N/A | N/A |

---

## EL Approval Record

**EL approval:** 2026-06-23

> G3 sprint entry approved. CE Assessment decisions (§2.5) accepted: adaptive resolution override required for `projection_steps > 8`; extend existing `/simulate` endpoint with `projection_steps` parameter; CM review on #274 required before intent ACs finalize; dry-run wall-time and indicator-bounds check required at Step 4 Verify. Structural gates clear. No ADR prerequisite. Intent document and QA test files must be filed before the implementation PR opens — these remain blocking conditions. G8 gate dependency (#843 may not open until G3 is BPO-accepted) noted. Implementation may proceed once the intent and QA gates are satisfied.
> — @PublicEnemage (2026-06-23)
