---
name: m18-g4-sprint-entry
type: sprint-entry
milestone: M18 — Full Argument and Demo 7
sprint-group: G4
status: EL-approved 2026-06-28
authored-by: PM Agent
authored-date: 2026-06-27
el-approved: 2026-06-28
release-branch: release/m18
sop-reference: docs/process/sprint-planning-sop.md
---

# Sprint Entry — M18, G4: Control Plane Column + Render Optimization

**Status:** EL-approved 2026-06-28
**Date authored:** 2026-06-27
**Release branch:** `release/m18`
**Sprint plan:** `docs/process/sprint-plans/m18-sprint-plan.md` (EL-approved 2026-06-26, PR #1364)
**Sprint journal issue:** #1402

*No implementation PR may open until this entry document is EL-approved AND all
pre-implementation prerequisites (§2.3, §2.4, and the G1+G2 exit gate below) are confirmed.*

---

## ADR-019 Acceptance Citation (Required at G4 Entry)

ADR-019 confirmed accepted: PR #1393 merged 2026-06-27. UX Designer sign-off obtained in
separate EL-triggered session (NM-042 compliant). EL acceptance on merge.

| Gate | Status | Evidence |
|---|---|---|
| ADR-019 accepted | ✅ | PR #1393 merged 2026-06-27; status field: `Accepted`; separate-session UX Designer sign-off on record |
| Independent UX Designer sign-off (NM-042 compliance) | ✅ | Filed 2026-06-27 in PR #1393 — separate EL-triggered session; GA-02 UX-7 correction applied in same PR |
| GD design package complete (#1354 closed) | ✅ | All 7 GD artifacts on record; #1354 closed 2026-06-27 per SESSION_STATE.md |

ADR-019 governs: two-component architecture (`Mode2ColumnSurface` + `ControlPlaneColumn`);
Mode 2 read-only column surface; Mode 3 Form 1 (Policy Instruments) and Form 2 (Scenario
Shocks); seven-shock-type taxonomy with GrowthShock (D-6); BranchRequest extension for
legitimacy_index (D-4); inject-shock endpoint (D-5); lazy-mount optimization for EX-001
resolution (D-1 + D-10). G4 implements exactly the scope ADR-019 specifies.

## G1 + G2 Exit Gate (Required Before G4 Implementation PR Opens)

Per `docs/process/sprint-plans/m18-sprint-plan.md §Wave 2 Entry Gates`:
> "G4 (control plane) may open when: G1 and G2 have exited (to avoid InstrumentCluster.tsx
> conflicts)"

**Status at entry filing (2026-06-27):** G1 (#1367) and G2 (#1368) are still in Wave 1
with implementation PRs open. G4's sprint sub-branch may be cut and intent/test authorship
work may proceed, but the G4 implementation PR targeting `sprint/m18-g4` **may not open**
until G1 and G2 integration PRs have merged to `release/m18`.

**Conflict basis:** G1 modifies `frontend/src/components/TrajectoryView.tsx` and its test
files. G4 modifies `frontend/src/components/InstrumentCluster.tsx` (which imports
`TrajectoryView`), `frontend/src/components/ScenarioInstrumentCluster.tsx`, and adds
`frontend/src/components/Mode2ColumnSurface.tsx` and `frontend/src/components/ControlPlaneColumn.tsx`.
No direct file overlap with G1 or G2, but `InstrumentCluster.tsx` structural changes
during a concurrent G1 TrajectoryView PR create merge-churn risk. The exit gate ensures
G4 starts from a stable `release/m18` baseline with G1 and G2 changes integrated.

**Gate confirmation mechanism:** PM Agent confirms G1 and G2 integration PRs merged to
`release/m18` and records the confirmation in the G4 sprint journal issue before the
implementing agent opens the G4 feature branch.

## G3 Concurrency Determination

Per G3 sprint entry (2026-06-26), PM Agent confirmed: "G3 scope does NOT touch
`ScenarioInstrumentCluster.tsx`." The G3 comparison summary renders inside
`MDAAlertPanelZone1B.tsx` via the existing `zone1bCohortSection` prop — no structural
writes to `ScenarioInstrumentCluster.tsx`.

G4 DOES modify `ScenarioInstrumentCluster.tsx` (to manage the `controlPlane` prop slot
for Mode2ColumnSurface / ControlPlaneColumn). Since G3 does not write to this file,
**G3 and G4 may run concurrently.** PM Agent must confirm no incidental G3 writes to
`ScenarioInstrumentCluster.tsx` at G4 integration exit time.

## EX-001 Pre-Implementation Condition (PI Agent Process Condition, Artifact 5 §Decision 3)

Per Artifact 5 Decision 3 EL approval (2026-06-26) and ADR-019 §D-10, PI Agent requires:

> "Resolution path recorded in `docs/compliance/exceptions.md §EX-001` before G4 begins."

**Status at entry filing:** EX-001 remains Active in `docs/compliance/exceptions.md`
(status: Active, expiry: M17 exit). The resolution path per ADR-019 D-10 is:
- Implement lazy-mount + Recharts memoization (#1217) in same PR as column layout move
- Run MV-002 at G4 implementation PR submission
- Close EX-001 as Resolved (≤ 100ms local) or Won't Fix (> 100ms local); remove AC-009
  `test.fixme()` from CI permanently regardless of label

**Required action before G4 implementation begins:** PM Agent must update
`docs/compliance/exceptions.md §EX-001` to record the ADR-019 D-10 resolution path as
the active resolution commitment. This update must be committed to `release/m18` via a
`chore/m18-state-sync` branch before the G4 feature branch opens. EX-001 named as
explicit deliverable in §3.1 below.

---

## Section 1 — Sprint Identification

| Field | Value |
|---|---|
| Milestone | M18 — Full Argument and Demo 7 |
| GitHub Milestone | #19 (API: milestone 19) |
| Sprint group | G4 — Control Plane Column + Render Optimization (Wave 2) |
| Release branch | `release/m18` |
| Sprint sub-branch | `sprint/m18-g4` |
| Sprint plan document | `docs/process/sprint-plans/m18-sprint-plan.md` |
| Exit checklist issue | #1340 |
| Sprint journal issue | #{TBD — PM Agent creates at entry via `gh issue create`} |
| Sprint groups in scope | G4 only |
| Wave coordination tier | **Recommended coordination** — at peak (G1+G2 still in Wave 1, G3+G4 in Wave 2) = 4 concurrent groups of 5 ceiling. PM Agent coordination lane required for shared-state files at this tier. When G1+G2 exit before G4 implementation PR opens, active concurrent groups reduce to G3+G4 = 2 (Standard); tier recorded at entry filing, not at implementation open. |
| Concurrent groups at entry | G1 + G2 (Wave 1 in progress) + G3 (Wave 2, entry EL-approved) = 3 active; G4 = entry filed (no implementation PR). Max concurrent at entry: 3 of 5. |
| Cross-group dependencies | G4 is gated on G1+G2 exits (hard gate — implementation PR blocked). G4 has soft concurrent overlap with G3 (confirmed safe per §G3 Concurrency Determination above). G4 exit is a soft upstream gate for the G3 integration test if G3 scope evolves to require `ScenarioInstrumentCluster.tsx` (unlikely per G3 entry determination; PM Agent monitors at G3 exit). |

---

## Section 2 — Entry Invariants Checklist

*All items must be confirmed before any G4 implementation PR opens.*

### 2.1 — Structural gates

- [x] **Release branch exists:** `release/m18` cut from `main` 2026-06-26 (commit 8cffc86 after sync PR #1366 merged)
- [x] **CI trigger verified:** `.github/workflows/ci.yml` `pull_request: branches` includes `release/m*` and `sprint/m*` — confirmed 2026-06-26. 6 required checks: `changes`, `lint`, `test-backend`, `playwright-e2e`, `compliance-scan`, `branch-naming`.
- [x] **Sprint plan EL-approved:** `docs/process/sprint-plans/m18-sprint-plan.md` EL-approved 2026-06-26 (PR #1364 merged)

### 2.2 — ADR prerequisite gate

| Group | Required ADR | ADR status | Gate |
|---|---|---|---|
| G4 — #1217 + control plane implementation | ADR-019 (ARCH-013) | **Accepted** 2026-06-27 (PR #1393; separate-session UX Designer sign-off) | **CLEAR** |

- [x] ADR-019 accepted on record. Gate: **CLEAR.**

ADR-019 is the sole governing authority for G4's architecture. The two-component split
(Mode2ColumnSurface / ControlPlaneColumn), the form layouts, the shock taxonomy discriminated
union (D-6), the BranchRequest extension (D-4), the inject-shock endpoint (D-5), and the
EX-001 resolution path (D-10) are all specified in ADR-019. G4 implementing agent must read
ADR-019 in full before opening a feature branch — it is the implementation specification.

Additional ADRs that govern G4 incidentally:
- ADR-008 (UX Architecture) — mode-level cognitive task model; InstrumentCluster column spec
- ADR-009 (Computation Engine Model) — BranchRequest extension must honour engine boundary
- ADR-010 (Trajectory View) — Zone 1A rendering contracts unchanged by G4
- ADR-017 (Zone 1A Information Architecture) — trajectory overlay contracts unchanged by G4
- ADR-006 (Uncertainty Quantification) — HCL parity maintained (ADR-019 §Consequences)

### 2.3 — Intent document gate

G4 is user-facing (new Zone 1 column surfaces in Mode 2 and Mode 3; new interactive control
inputs; new shock injection endpoint). An intent document is required before the implementation
PR opens.

- [ ] Intent document filed: `docs/process/intents/M18-G4-{date}-control-plane-column.md` — **required before implementation PR opens**

The intent document must be derived from ADR-019 (primary source) and the GD design
artifacts (Artifacts 1–4 and Artifact 7). Specific requirements for the intent document:

**Observable application state (must be assertable without reading implementation code):**
- "At 1280×800 in Mode 2, the control plane column (280px, `data-testid="zone-control-plane"`)
  contains the scenario identity block (scenario name, entity, calibration vintage, run
  horizon) and the 'Enter Active Control' button, visible without scroll. The column uses
  subdued visual treatment (slate-50 background, slate-400 dashed border)."
- "At 1280×800 in Mode 3, the control plane column contains Form 1 (Policy Instruments,
  blue `#0284c7`) and Form 2 (Scenario Shocks, orange `#ea580c`). Both form headers are
  visible without scroll (Artifact 3 Q3 requirement). After selecting FiscalMultiplier and
  clicking 'Apply policy instrument', a counter-trajectory branch appears in Zone 1A
  simultaneously with the baseline — the analyst does not need to scroll to see it."
- "EX-001 is closed at G4 exit: either Resolved (MV-002 ≤ 100ms ProBook local) or Won't
  Fix (MV-002 > 100ms); AC-009 `test.fixme()` removed from CI regardless of resolution
  label."

**Content requirements for the intent document:**
- Component inventory and file renames: `ControlPlane.tsx` → `ControlPlaneColumn.tsx`;
  new `Mode2ColumnSurface.tsx`; new `ControlPlaneForm1PolicyInstruments.tsx` /
  `ControlPlaneForm2ScenarioShocks.tsx` (or inline in ControlPlaneColumn per ADR-019 D-3)
- `InstrumentCluster.tsx` prop extension: `controlPlane?: React.ReactNode` on
  `data-testid="zone-control-plane"` div
- `ScenarioInstrumentCluster.tsx` slot management: Mode 1 → undefined; Mode 2 →
  `<Mode2ColumnSurface />`; Mode 3 → `<ControlPlaneColumn />`
- Form 1 acceptance criteria: policy input type selector; type-driven parameter inputs
  (FiscalMultiplier slider 0.1–3.0 step 0.05; LegitimacyConstraint numeric input);
  branch_from_step selector; "Apply policy instrument" button; policy events history list
- Form 2 acceptance criteria: shock type selector (7 types per ADR-019 D-6 enum);
  type-driven parameter inputs per discriminated union; inject_at_step selector;
  "Inject scenario shock" button; injected shocks history list
- Button label constraint: "Enter Active Control" (not "Enter Mode 3") — Customer Agent
  kryptonite finding (Artifact 3; EL Decision 1 panel condition); `data-testid="enter-active-control"`
- #1217 optimization: lazy-mount `ControlPlaneColumn` (mount on Mode 3 entry, unmount on
  exit); Recharts `memo()` wrapping — must be in same PR as column layout move
- EX-001 resolution commitment: MV-002 profiling at implementation PR submission; closure
  record in `docs/compliance/exceptions.md §EX-001` at G4 exit
- Backend: BranchRequest extension (`legitimacy_index` field); inject-shock endpoint
  (`POST /api/scenarios/{id}/inject-shock`, `ShockInjectRequest` discriminated union)
- Schema prerequisite: `docs/schema/api_contracts.yml` (inject-shock endpoint) and
  `docs/schema/simulation_state.yml` (BranchRequest extension) updated in same PR as
  backend implementation
- North star test: "The Senegalese Finance Minister's team can show that under proposed
  conditionality there is no fiscal instrument configuration that avoids the bottom quintile
  crossing the 0.40 floor — or, if a configuration exists, they can name it and cite the
  specific step at which the threshold is no longer crossed."

**UX/UI design artifact gate:**

G4 introduces the Mode2ColumnSurface (new component, new layout zone content), the
ControlPlaneColumn column placement (structural change from bottom-bar to column), and
Forms 1 and 2 (new interaction patterns). This is a UX/UI-impacting deliverable.

The GD design package (Artifacts 1–4) and ADR-019 acceptance collectively satisfy the
UX mockup and UI mockup requirements for this deliverable:

| Mockup requirement | Satisfied by | Status |
|---|---|---|
| UX mockup — placement and information hierarchy | Artifact 2 (`docs/ux/information-hierarchy.md §Control Plane Reserved Zone`) + Artifact 4 (delta analysis) | ✅ On record |
| UI mockup — visual treatment (Mode 2 subdued, Mode 3 blue/orange) | ADR-019 §D-2, §D-3 exact color and border specifications | ✅ In accepted ADR |
| UX/UI panel review | GD five-agent design panel + ADR-019 panel (Frontend Architect, Customer Agent, Business PO, UX Designer independent sign-off) | ✅ Complete |
| Binding specification — referenced from intent document | Intent document must cite ADR-019 by section and Artifact 2 by section | ⬜ Required before implementation PR opens |

- [x] GD design artifacts and ADR-019 satisfy the UX mockup + UI mockup + panel review requirements.
- [ ] Intent document references panel-approved specs by section — **required before implementation PR opens**

| Deliverable | ADR reference | Intent document path | Filed? |
|---|---|---|---|
| #1217 + control plane implementation (frontend — Mode2ColumnSurface + ControlPlaneColumn) | ADR-019 (primary); ADR-008, ADR-010, ADR-017 (incidental) | `docs/process/intents/M18-G4-{date}-control-plane-column.md` | No — required before implementation PR opens |
| Shock injection endpoint (backend — 7 shock types) | ADR-019 §D-5, §D-6 | `docs/process/intents/M18-G4-{date}-control-plane-column.md` | No — required before implementation PR opens |
| BranchRequest extension (backend — legitimacy_index) | ADR-019 §D-4 | `docs/process/intents/M18-G4-{date}-control-plane-column.md` | No — required before implementation PR opens |
| EX-001 resolution (optimization + closure record) | ADR-019 §D-10 | `docs/process/intents/M18-G4-{date}-control-plane-column.md` | No — required before implementation PR opens |

### 2.4 — QA test authorship gate

- [ ] QA test files authored from intent document acceptance criteria before implementation code is written — **required before implementation PR opens**

Expected test files:

`frontend/tests/e2e/m18-g4-control-plane-column.spec.ts`
The E2E test must assert (non-exhaustive — full set derived from intent document):
- At 1280×800 in Mode 2: `data-testid="zone-control-plane"` contains scenario identity
  block text (entity name) and `data-testid="enter-active-control"` button is present
- At 1280×800 in Mode 2: no editable form inputs present in the control plane column
- On click of "Enter Active Control": mode transitions to Mode 3; Form 1 and Form 2
  headers are simultaneously visible in the column without scroll
- In Mode 3: `data-testid="policy-input-type-selector"` present; selecting FiscalMultiplier
  reveals the multiplier slider; selecting LegitimacyConstraint reveals numeric input
- In Mode 3: "Apply policy instrument" button click triggers trajectory branch in Zone 1A
  (counter-trajectory visible alongside baseline without scroll — simultaneous visibility)
- In Mode 3: `data-testid="shock-type-selector"` present with all 7 types listed
  (ElectionShock, CurrencyAttack, CreditorDefection, GeopoliticalShock, NaturalDisaster,
  ContagionShock, GrowthShock)
- In Mode 3: after shock injection, `data-testid="shock-events-history"` shows the
  injected shock entry (type + step)
- In Mode 3: GrowthShock type selected → `distribution_asymmetry` parameter input present
- AC-009 performance gate: either restored to `test()` at 100ms threshold (if MV-002 resolved),
  or `test.fixme()` removed and replaced with a comment referencing EX-001 closure record
  (if Won't Fix)

`backend/tests/test_m18_g4_shock_injection.py`
The backend test must assert:
- `POST /api/scenarios/{id}/inject-shock` with `ElectionShock` payload returns 200 with
  trajectory branch data for the Senegal fixture
- `POST /api/scenarios/{id}/inject-shock` with `GrowthShock` payload including
  `growth_rate_delta`, `duration_steps`, `distribution_asymmetry` returns 200 with
  trajectory branch data; cohort-level income trajectories at affected steps reflect the
  growth departure
- `POST /api/scenarios/{id}/inject-shock` with invalid `shock_type` returns 422
- `PUT /api/scenarios/{id}/branch` with extended BranchRequest (including `legitimacy_index`)
  returns 200 for the Senegal fixture; branch trajectory reflects legitimacy constraint
- Shock handler registry is complete: all 7 ShockType values have registered handlers

| Deliverable | Test file path | Authored before implementation? |
|---|---|---|
| Control plane column (frontend — Mode2ColumnSurface + ControlPlaneColumn + InstrumentCluster prop) | `frontend/tests/e2e/m18-g4-control-plane-column.spec.ts` | No — required before implementation PR opens |
| Shock injection endpoint (backend) | `backend/tests/test_m18_g4_shock_injection.py` | No — required before implementation PR opens |

---

## Section 3 — Scope Declaration

### 3.1 — Issues in scope

| Issue | Title | Priority | Observable application state |
|---|---|---|---|
| #1217 | Mode 3 render optimization (EX-001 expired) | High — Demo 7 Act 1; EX-001 expired M17 | Mode 3 control plane renders within column without performance degradation detectable at Demo 7. MV-002 measurement recorded at G4 exit. EX-001 closed per ADR-019 §D-10. |
| (no separate issue) | Control plane column — Mode2ColumnSurface + ControlPlaneColumn + Form 1 + Form 2 + 7 shock types | High — Demo 7 Act 1 primary deliverable | In Mode 2: control plane column populated with read-only scenario identity and "Enter Active Control" affordance. In Mode 3: Form 1 (Policy Instruments) and Form 2 (Scenario Shocks) visible simultaneously in the column without scroll at 1280×800; trajectory branch appears in Zone 1A on policy instrument apply without scroll (simultaneous visibility with column — the Demo 7 Act 1 claim). |

**EX-001 as named deliverable (per ADR-019 §D-10 and PI Agent process condition):**

EX-001 is an explicit G4 exit deliverable. The implementing agent must:
1. Implement #1217 (lazy-mount + Recharts memoization) in the same PR as the column
   layout move (before form content is added)
2. Run MV-002 at G4 implementation PR submission and record measurement
3. File EX-001 closure record in `docs/compliance/exceptions.md §EX-001` at G4 exit

The resolution path (Resolved or Won't Fix) is determined at G4 exit by the MV-002 measurement. AC-009 `test.fixme()` is removed from CI permanently regardless of label.

**Scope note — control plane column not in a separate GitHub issue:**
The control plane implementation is scoped under the G4 sprint and ADR-019 rather than a
dedicated GitHub issue. The work is tracked in the G4 sprint journal issue
(#{TBD}) and in the sprint exit document. At G4 exit, PM Agent confirms both
#1217 (render optimization) and the control plane implementation deliverables are complete.

### 3.2 — Issues explicitly out of scope

| Issue | Rationale for exclusion |
|---|---|
| #1254 — CI bands on Zone 1A | G1 (Wave 1). No G4 interaction with TrajectoryView.tsx rendering logic. |
| #1255 — PSP decomposition | G2 (Wave 1). No G4 interaction with Zone 1D. |
| #1349 — counter-scenario comparison | G3 (Wave 2). G4 does not touch MDAAlertPanelZone1B.tsx. |
| #1256 — Path 2 / proprietary data | Closed 2026-06-27 — retired on open-source-as-strategy principle. Exception required to reopen. |
| Richer Mode 2 scenario configuration editor | Out of scope per EL Decision 1 (Artifact 5). Mode 2 column is read-only scenario summary + mode transition affordance in M18. Scenario parameter adjustment deferred. |
| `CreditorDefection` bilateral linkage table (pre-populated data) | Out of scope per ADR-019 §Alternatives (Alternative 3 deferred). Analyst-specified transmission rate in M18; pre-populated linkage table post-M18. |
| `NaturalDisaster` and `ContagionShock` deferred handlers | **In scope**: ADR-019 §Alternatives (Alternative 2 rejected) — all 7 handlers must ship in M18. Deferred-handler alternative explicitly rejected. |
| HCL narration integration (#1059) | Capacity-allowing. G4 does not address narration integration. |
| Demo 7 presenter script | Not a G4 implementation deliverable. Authored in Demo 7 preparation track. |

---

## Section 4 — ADR Prerequisite Summary

| Group | ADR required | ADR status | Implementation may begin? |
|---|---|---|---|
| G4 — #1217 + control plane implementation | ADR-019 (ARCH-013) | **Accepted** 2026-06-27, PR #1393 | Yes — after EL approves this entry, G1+G2 exit confirmed, EX-001 resolution path committed, intent document filed, and QA tests authored before implementation PR opens |

**Implementation sequencing for G4:**

1. EL approves this entry document
2. PM Agent creates G4 sprint journal issue (`gh issue create --title "sprint journal: M18 G4 — Control Plane Column + Render Optimization (#1217)" --label documentation`) and records issue number in this entry
3. PM Agent updates `docs/compliance/exceptions.md §EX-001` to record ADR-019 §D-10 resolution path as the active commitment; commits via `chore/m18-state-sync` → `release/m18` before G4 feature branch opens
4. PM Agent cuts `sprint/m18-g4` from `release/m18`:
   `git checkout -b sprint/m18-g4 release/m18 && git push -u origin sprint/m18-g4`
   *(cut after G1+G2 integration PRs have merged to `release/m18`, or cut now and hold feature branch off `sprint/m18-g4` until G1+G2 exit — former preferred)*
5. Implementing agent reads ADR-019 in full before opening any feature branch
6. Frontend Architect authors intent document `docs/process/intents/M18-G4-{date}-control-plane-column.md` from ADR-019 + GD artifacts, referencing ADR-019 and Artifact 2 by section
7. QA Lead authors `frontend/tests/e2e/m18-g4-control-plane-column.spec.ts` and `backend/tests/test_m18_g4_shock_injection.py` from intent document acceptance criteria (red before implementation)
8. PM Agent confirms G1 integration PR (`sprint/m18-g1` → `release/m18`) merged and G2 integration PR (`sprint/m18-g2` → `release/m18`) merged — records in G4 sprint journal issue
9. Implementing agent opens feature branch `feat/m18-g4-column-layout` from `sprint/m18-g4`
10. **Dimension 1 (column slot + lazy-mount baseline):**
    - `InstrumentCluster.tsx`: add `controlPlane?: React.ReactNode` prop; render in `data-testid="zone-control-plane"` div
    - `ScenarioInstrumentCluster.tsx`: slot management (Mode 1 undefined / Mode 2 `<Mode2ColumnSurface />` / Mode 3 `<ControlPlaneColumn />`)
    - `ControlPlane.tsx` → `ControlPlaneColumn.tsx` rename (shell only; forms added in Dimension 2+3)
    - `Mode2ColumnSurface.tsx`: new component — scenario identity block + "Enter Active Control" button
    - Lazy-mount: `ControlPlaneColumn` mounted on Mode 3 entry, unmounted on exit (addresses #1217 — Recharts components inside do not render in Mode 1/2)
    - **Run MV-002 profiling gate at this PR** before proceeding to form content. Record measurement in PR description. Recharts memoization may be added here if measurement indicates need.
    - Pre-push gate: `cd backend && ruff check . && mypy app/`; `cd frontend && npm run build` — both exit 0
    - PR targeting `sprint/m18-g4`; set auto-merge
11. **Dimension 2 (Form 1 — Policy Instruments):**
    - Feature branch `feat/m18-g4-form1-policy` from `sprint/m18-g4` (after Dimension 1 merges)
    - Form 1 implementation in `ControlPlaneColumn.tsx`: policy input type selector (FiscalMultiplier / LegitimacyConstraint); type-driven parameter inputs; branch_from_step selector; "Apply policy instrument" button; policy events history list
    - Backend: BranchRequest extension (`legitimacy_index` field in `docs/schema/simulation_state.yml`)
    - `docs/schema/simulation_state.yml` updated in same PR
    - Pre-push gate: both exit 0
    - PR targeting `sprint/m18-g4`; set auto-merge
12. **Dimension 3 (Form 2 — Scenario Shocks + backend endpoint):**
    - Feature branch `feat/m18-g4-form2-shocks` from `sprint/m18-g4` (may run in parallel with Dimension 2 if `ControlPlaneColumn.tsx` layout is stable)
    - Form 2 implementation: shock type selector (7 types); type-driven parameter inputs per ADR-019 §D-6 discriminated union; inject_at_step selector; "Inject scenario shock" button; injected shocks history list
    - Backend: inject-shock endpoint (`POST /api/scenarios/{id}/inject-shock`); all 7 ShockHandler implementations; ShockEffect protocol and handler registry
    - `docs/schema/api_contracts.yml` updated in same PR with inject-shock endpoint shape
    - Pre-push gate: both exit 0
    - PR targeting `sprint/m18-g4`; set auto-merge
13. **EX-001 exit measurement:**
    - After all three dimension PRs merge to `sprint/m18-g4`: run MV-002 on ProBook local
    - If ≤ 100ms: restore AC-009 from `test.fixme()` to `test()` at 100ms threshold; close EX-001 as Resolved
    - If > 100ms: remove AC-009 `test.fixme()` permanently (preserve test structure with comment referencing EX-001 closure); close EX-001 as Won't Fix
    - In either case: file closure record in `docs/compliance/exceptions.md §EX-001` with MV-002 measurement and resolution label
14. Integration PR `sprint/m18-g4` → `release/m18`; PI Agent gate comment required
15. Customer Agent Layer 3 at sprint exit (Personas 2 and 5); Business PO acceptance
16. North star test artifact confirmed on record at exit (from sprint plan §Exit Conditions)

---

## Section 5 — Near-Miss Sweep

**Near-miss sweep date:** 2026-06-27
**Sweep period:** G3 sprint entry filing (2026-06-26) through G4 sprint entry filing (2026-06-27)

| Finding | Category | PI Agent register call issued? | NM entry number |
|---|---|---|---|
| NM-072 filed during GD phase (2026-06-27): Artifact 5 (scope decision gate) authored and EL-approved before prerequisite design artifacts existed; cascaded into stale delta analysis and incomplete taxonomy | near-miss | Yes — PI Agent filed during GD session | NM-072 |
| No additional process gaps identified in the G4 entry sweep period. NM-072 is the only filing since G3 entry. G4 entry incorporates the NM-072 process improvement via §2.1 structural gates and §Pre-Implementation prerequisites. | N/A | N/A | N/A |

---

## Section 6 — Sprint Group Isolation

### 6.1 — Sprint sub-branch

| Field | Value |
|---|---|
| Sprint sub-branch | `sprint/m18-g4` |
| Cut from | `release/m18` — after EL approves this entry and EX-001 resolution path is committed. Preferred: cut after G1+G2 integration PRs merge to `release/m18` so the sub-branch starts from a stable baseline. |
| Sprint journal issue | #{TBD — PM Agent creates at entry} |

**PM Agent sprint sub-branch cut command:**
```bash
git checkout -b sprint/m18-g4 release/m18 && git push -u origin sprint/m18-g4
```

*G4 implementation has three sequential-but-parallelisable dimensions. Feature branches
are cut from `sprint/m18-g4`, not from `release/m18` directly.*

### 6.2 — File-conflict risk assessment

| File | Lane required | Trigger |
|---|---|---|
| `frontend/src/components/InstrumentCluster.tsx` | Sprint sub-branch | Add `controlPlane?: React.ReactNode` prop + render in zone-control-plane div (Dimension 1) |
| `frontend/src/components/ScenarioInstrumentCluster.tsx` | Sprint sub-branch | Slot management — passes `Mode2ColumnSurface` or `ControlPlaneColumn` as `controlPlane` prop based on mode (Dimension 1) |
| `frontend/src/components/ControlPlane.tsx` → `ControlPlaneColumn.tsx` | Sprint sub-branch | File rename + refactor into column-mounted component; lazy-mount on Mode 3 entry/exit (Dimension 1) |
| `frontend/src/components/Mode2ColumnSurface.tsx` (new) | Sprint sub-branch | New read-only orientation surface for Mode 2 column (Dimension 1) |
| `frontend/src/components/ControlPlaneForm1PolicyInstruments.tsx` (new, or inline in ControlPlaneColumn) | Sprint sub-branch | Form 1 — Policy Instruments (FiscalMultiplier + LegitimacyConstraint) (Dimension 2) |
| `frontend/src/components/ControlPlaneForm2ScenarioShocks.tsx` (new, or inline in ControlPlaneColumn) | Sprint sub-branch | Form 2 — Scenario Shocks (7 types, discriminated union) (Dimension 3) |
| `frontend/src/stores/` | Sprint sub-branch | BranchRequest type extension (legitimacy_index); ShockInjectRequest type |
| `backend/app/simulation/` (shock handler module) | Sprint sub-branch | 7 ShockHandler implementations; ShockEffect protocol; handler registry |
| `backend/app/api/routes/` (inject-shock route) | Sprint sub-branch | New `POST /api/scenarios/{id}/inject-shock` endpoint |
| `docs/schema/api_contracts.yml` | Sprint sub-branch (same PR as backend implementation) | Inject-shock endpoint shape — mandatory schema-first per CLAUDE.md §Schema registry |
| `docs/schema/simulation_state.yml` | Sprint sub-branch (same PR as backend BranchRequest extension) | BranchRequest `legitimacy_index` field extension |
| `docs/compliance/exceptions.md` | **PM Agent coordination lane** | EX-001 resolution path committed before G4 begins; closure record at G4 exit |
| `SESSION_STATE.md` | PM Agent coordination lane | Sprint exit cockpit update |
| `docs/process/near-miss-registry.md` | PM Agent coordination lane (PI Agent authors) | If NM identified |
| `docs/compliance/scan-registry.md` | PM Agent coordination lane | If compliance scan produced |

**File area analysis — no conflict with G3:**

G4 primary files: `InstrumentCluster.tsx`, `ScenarioInstrumentCluster.tsx`,
`ControlPlane.tsx` → `ControlPlaneColumn.tsx`, `Mode2ColumnSurface.tsx`, new Form
components, backend shock module and route.

G3 primary files: `MDAAlertPanelZone1B.tsx` (CohortImpactSection), new
`DistributionalComparisonSummary.tsx`, backend comparison module.

These file sets do not overlap. G4 does NOT write to `MDAAlertPanelZone1B.tsx` or any
G3 comparison component. G3 does NOT write to `ScenarioInstrumentCluster.tsx`,
`InstrumentCluster.tsx`, or any G4 column component. Concurrent operation confirmed safe.

**G1+G2 temporal conflict window:**

G1 writes to `TrajectoryView.tsx` and associated test files. G4 writes to
`InstrumentCluster.tsx` (which renders `TrajectoryView.tsx`). Direct file overlap is
limited to `InstrumentCluster.tsx` only — G1 does not modify `InstrumentCluster.tsx`
itself. The gate requirement (G1+G2 exit before G4 implementation PR) is a sequencing
precaution rather than a direct file conflict. PM Agent may reassess this gate at
implementation time if G1+G2 exit is confirmed before G4 Dimension 1 PR opens.

### 6.3 — Infrastructure dependency declaration

- [x] No DS-owned file changes required. All G4 writes are to implementation code, test
  files, schema files, and documentation.

#### 6.3a — New output paths declaration (NM-069 process improvement)

- [x] No new output directories introduced by G4. `backend/test-results/` and
  `frontend/test-results/` are already covered by `.gitignore` (PR #1346 from M18 kickoff prep).

No new output paths introduced by this sprint group.

### 6.4 — Cross-group dependency declaration

- [x] Yes — hard dependency on G1+G2 exit (implementation PR gate, not entry gate)

**Dependency 1 — G1 + G2 exit (hard gate, implementation PR level):**
G4 implementation PR for Dimension 1 (column layout) must not open until G1 (`sprint/m18-g1`
→ `release/m18`) and G2 (`sprint/m18-g2` → `release/m18`) integration PRs have merged.
PM Agent confirms and records in G4 sprint journal issue before Dimension 1 feature branch
opens.

**Dependency 2 — G3 concurrency (soft, file-level monitoring):**
G3 and G4 may run concurrently (confirmed by G3 entry ScenarioInstrumentCluster.tsx
determination and §G3 Concurrency Determination above). PM Agent monitors G3 scope at
G3 exit to confirm no incidental writes to `ScenarioInstrumentCluster.tsx` were introduced
during implementation.

**G4 as upstream for Demo 7 Act 1:**
G4 exit is required for Demo 7 Act 1 minimum viable demo (Mode 3 column populated; Form 1
apply triggers counter-trajectory; simultaneous visibility of column and Zone 1A). Demo 7
session schedule depends on G4 exit — PM Agent does not schedule Demo 7 until G4 PI Agent
exit confirmation is on record.

### 6.5 — Prior NM verification (NM-068 process improvement)

**NM verification sweep date:** 2026-06-27
**Sweep period:** G3 sprint entry (2026-06-26) through G4 sprint entry (2026-06-27)

| NM entry | Process improvement required | Applied in this sprint? |
|---|---|---|
| NM-068 | Prior NM verification field in sprint entry | Yes — this section (§6.5) |
| NM-069 | New output directories covered by `.gitignore` in same PR or DS infra lane | Yes — no new output directories; §6.3a confirmed |
| NM-070 | Pre-push hook enforcing ruff + mypy + npm build | Yes — `.githooks/pre-push` active; §4 implementation sequencing requires both gates exit 0 before any push (steps 10–12) |
| NM-071 | Wave concurrency ceiling check at wave kickoff | Yes — G4 filing brings max concurrent to 4 of 5 ceiling (G1+G2+G3+G4); Recommended coordination tier recorded in §1. G4 implementation PR gate (G1+G2 exit required) prevents G4 from exceeding Standard tier when implementation opens. |
| NM-072 | Artifact 5 (EL scope gate) must not be submitted for EL review until prerequisite design artifacts are filed and confirmed on record; PI Agent holds R for verifying upstream gate | Yes — G4 is an implementation sprint; no equivalent gate risk. Applied as awareness context: schema files (`api_contracts.yml`, `simulation_state.yml`) must be updated in the same PR as the implementation that uses them, not after. |

---

## EL Approval Record

**EL approval:** 2026-06-28

> Approved. G4 scope as filed: control plane column (Mode2ColumnSurface + ControlPlaneColumn
> + Form 1 + Form 2 + 7 shock types) plus render optimization (#1217) and EX-001 closure.
> ADR-019 accepted 2026-06-27 — CLEAR. Sprint journal issue #1402 created. Pre-implementation
> prerequisites apply before implementation PR opens: G1+G2 exit confirmed; EX-001 resolution
> path committed to exceptions.md; intent document filed; QA tests authored.
> — @PublicEnemage (2026-06-28)
