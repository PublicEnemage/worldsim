---
name: m16-g6-sprint-entry
type: sprint-entry
milestone: M16 — Distributional Visibility
sprint-group: G6
status: Filed
authored-by: PM Agent
authored-date: 2026-06-24
el-approved: 2026-06-24
release-branch: release/m16
sop-reference: docs/process/sprint-planning-sop.md
---

# Sprint Entry — M16, G6: Accessibility + Performance Validation

**Status:** Filed — awaiting EL approval before validation work begins
**Date authored:** 2026-06-24
**Release branch:** `release/m16`
**Sprint plan:** `docs/process/sprint-plans/m16-sprint-plan.md` (EL Approved 2026-06-23)

*Authority: `docs/process/sprint-planning-sop.md §Sprint Entry Gate` (Phase C output).
G6 is a parallel track — no sequential dependency on any other M16 sprint group.
G6 does not gate G8; the G8 gate is already FULLY OPEN (G1 ✅ G2 ✅ G3 ✅ G4 ✅ G10 ✅,
recorded 2026-06-24). G6 must close before M16 exits (#985 exit checklist).*

**Infrastructure Sprint Declaration:** G6 is an infrastructure sprint. Its primary
deliverables are: (1) a validation report confirming hardware accessibility of the
M16 application state, and (2) a corrected AC-009 test (testid fix — test-only change,
no user-visible output). The intent document gate (§2.3) and QA test authorship gate
(§2.4) are waived under the Infrastructure Sprint Exception
(`docs/process/sprint-planning-sop.md §Infrastructure Sprint Exception`). Business PO
acceptance and Customer Agent Layer 3 assessment are not required at exit for G6
deliverables. PI Agent will review this declaration at exit and file a near-miss if
any G6 output is found to be user-visible and was incorrectly classified.

**Pattern:** M15-G6 (`docs/process/sprint-plans/m15-g6-sprint-entry.md`). Key
differences from M15-G6: MV-002 AC-009 is now IN SCOPE (Mode 3 is implemented);
M15-G6 explicitly excluded it. Accessibility re-validation covers M16 G1/G2 primary
surface additions (Zone 1A Phase 4, cohort disaggregation, political risk surface).
VC-2 extends to include 100-step scenario timing (G3 delivered 25-year trajectory).

---

## Section 1 — Sprint Identification

| Field | Value |
|---|---|
| Milestone | M16 — Distributional Visibility |
| GitHub Milestone | #17 |
| Sprint group | G6 — Accessibility + Performance Validation |
| Release branch | `release/m16` |
| Sprint plan document | `docs/process/sprint-plans/m16-sprint-plan.md` |
| Exit checklist issue | #985 |
| Sprint groups in scope | G6 only |
| ADR gate | None — validation and documentation; no new architecture |
| Implementing agents | Frontend Architect Agent (Playwright, AC-009 testid fix, VC-3/VC-4); Chief Engineer Agent (Docker stack, simulation timing, VC-1/VC-2); PM Agent (validation report authorship) |
| Wave | Parallel — no sequential dependency on any other M16 sprint group |
| Sprint type | Infrastructure Sprint — no user-facing deliverables; intent and QA gates waived |

---

## Section 2 — Entry Invariants Checklist

*All items must be checked before G6 validation work begins.
An unchecked invariant blocks the sprint from opening.*

### 2.1 — Structural gates

- [x] **Release branch exists:** `release/m16` cut from `main` at commit 07c92b8 (2026-06-23)
- [x] **CI trigger verified:** `.github/workflows/ci.yml` `pull_request: branches` includes
  `release/m*` — confirmed at M15-G6 (2026-06-20); KI-005 permanent fix applied.
- [x] **Sprint plan EL-approved:** `docs/process/sprint-plans/m16-sprint-plan.md`
  `el-approved: 2026-06-23`

### 2.2 — ADR prerequisite gate

G6 contains no items requiring a new ADR. The AC-009 testid fix is a one-line test
correction (aligning the test to the existing testid in source). If G6 uncovers
performance or accessibility failures that require architectural responses, those
responses will be filed as new issues with their own ADR assessment at filing time.

| Group | Required ADR | ADR status | Gate |
|---|---|---|---|
| G6 — #569 + accessibility re-validation | None — validation and test correction | N/A | **CLEAR** |

- [x] No ADR prerequisites for G6. Gate: **CLEAR**.

### 2.3 — Intent document gate

**Infrastructure Sprint Exception applies.**

G6 produces no user-facing deliverable. The primary output is the validation report
and a test-only testid fix. Observable states are specification-confirmable directly
from Section 3.1 below.

- [x] Infrastructure Sprint Exception declared. Intent document gate **WAIVED**.

*PI Agent note at exit gate: confirm that no G6 output is user-visible. The AC-009
testid fix modifies only `frontend/tests/e2e/trajectory-view.spec.ts` — a test file
with no production bundle output. If any output modifies frontend components, API
responses, or simulation outputs visible to end users, the Infrastructure Sprint
Exception does not apply.*

### 2.4 — QA test authorship gate

**Infrastructure Sprint Exception applies.**

G6 runs existing tests and corrects one existing test (AC-009 testid). It does not
author new test code for new user-facing deliverables.

- [x] Infrastructure Sprint Exception declared. QA test authorship gate **WAIVED**.

---

## Section 3 — Scope Declaration

### 3.1 — Validation checks and implementation tasks in scope

G6 must satisfy five observable states (VC-1 through VC-4 re-validated for M16, plus
MV-002 AC-009 hardware validation). Each must be documented in the validation report.

---

**Pre-condition — AC-009 testid fix (implementation task)**

*Observable state:*
`frontend/tests/e2e/trajectory-view.spec.ts` AC-009 test uses
`[data-testid="mode-3-activate"]`. The testid in `frontend/src/App.tsx` is
`data-testid="mode3-toggle"` (line 293). As a result, `hasMode3` is always `false`
and the AC-009 measurement is silently skipped in CI — the test passes vacuously.

*Fix:* Update the AC-009 test locator from `mode-3-activate` to `mode3-toggle` so
the measurement runs against the real Mode 3 activation control. This is a test-only
change — no production code modified.

*Pass criterion:* After the fix, AC-009 produces a non-null `renderMs` value when
run against a loaded scenario with Mode 3 visible. The CI throttled gate (4× CPU)
must pass at ≤ 100ms.

**EL Decision — 2026-06-24 (threshold amendment):** First real CI run post-fix
measured 179ms vs the 100ms threshold. Chief Engineer assessment: measurement
methodology is sound; ~40ms estimated at 1× speed; 100ms threshold was never
validated against a real Mode 3 run (NM-058 gap). CE recommendation: raise CI
throttled threshold to 200ms (179ms + 21ms headroom) to preserve regression
sensitivity while recognising the calibration gap. Optimization (Recharts
memoization, lazy ControlPlane mounting) filed as `enhancement` for M17.

CI throttled threshold amended to **200ms** for M16-G6. Approved exception
recorded at `docs/compliance/exceptions.md §EX-001` (expiry: M17 exit).
ProBook hardware target (MV-002, no throttle) remains ≤ 100ms — unchanged.

---

**VC-1 — Docker Compose stack starts and is responsive on target hardware (M16 state)**

*Observable state:*
On a machine with ≤ 8GB RAM and ≤ 4 CPU cores, `docker compose up --build` completes
without error against the M16 codebase (G1/G2 frontend additions in bundle). After startup:
- `GET /api/v1/health` returns HTTP 200
- `GET /api/v1/entities` returns HTTP 200 with at least GRC, JOR, EGY, ZMB in response
- Frontend is reachable at `http://localhost:5173` without JS error in browser console
- Peak resident memory during startup does not exceed 7GB

*Confirmation method:* Chief Engineer Agent runs `docker compose up --build` in a
resource-constrained environment (CI `--memory="7g"` Docker flag as proxy if ProBook
unavailable), captures startup log, runs HTTP checks, records peak memory from `docker stats`.

*Pass criterion:* All HTTP checks pass; no startup error in logs; peak memory ≤ 7GB.

---

**VC-2 — Simulation engine timing: 8-step and 100-step scenarios**

*Observable state (8-step):*
A full 8-step ZMB ECF scenario completes within 60 seconds on target hardware.
All 8 step responses include trajectory data across all four framework keys.

*Observable state (100-step — G3 delivered, CE Assessment Decision 4):*
A 100-step scenario (DemographicModule 25-year projection) completes within **60
seconds** on target hardware (8GB RAM, 4-core). This is the contracted ceiling per
G3 CE Assessment Decision 4 (`docs/process/sprint-plans/m16-g3-sprint-entry.md §2.5`)
and AC-F8 (`frontend/tests/e2e/m16-g3-25year-human-capital-trajectory.spec.ts:462`).
G6 is a regression confirmation — not a fresh feasibility check. G3 CE estimate was
25–50 seconds; 60 seconds is the contracted operator experience ceiling.

*Pre-check — AC-F8 guard:* Before running VC-2, verify the AC-F8 test assertion
path is live (not silently skipped via `catch(() => false)`). This is the same
failure mode as the AC-009 testid mismatch (§Pre-condition above). If the AC-F8
assertion is guarded into never executing, file a separate near-miss before G6 exits.

*Confirmation method:* Chief Engineer Agent times both runs using `curl` timing or
browser devtools. Records wall-clock times and framework key presence.

*Pass criterion:* 8-step ≤ 60s (same as M15); 100-step ≤ 60s (G3 CE Assessment
Decision 4 ceiling). If 100-step exceeds 60s, the finding is filed as a **regression
against the G3 contracted ceiling** (label `compliance:major`) before G6 exits.

---

**VC-3 — Playwright E2E has a documented path to run without full Docker Compose stack**

*Observable state:*
`docs/CONTRIBUTING.md §4` documents a lightweight local Playwright path (non-Docker).
This was CONDITIONAL PASS in M15-G6 — the lightweight path exists; the fully offline
MSW path was documented as planned for a future milestone.

*Re-validation:* Confirm the §4 documented path still works against M16 frontend
(G1/G2 added new components; confirm no new hard API dependencies broke the
lightweight path). Confirm MSW offline path status has not changed (still planned,
not shipped — document the continued limitation).

*Pass criterion:* CONDITIONAL PASS maintained — lightweight path functional; MSW
limitation still on record. If the lightweight path is broken by M16 changes, that
is a FAIL requiring a new issue before G6 exits.

---

**VC-4 — Frontend build time on target hardware**

*Observable state:*
`cd frontend && npm run build` completes in under 5 minutes from start to exit 0,
against M16 frontend (new components from G1/G2/G10 added to bundle).

*Confirmation method:* `time npm run build` on target hardware or resource-constrained
CI equivalent. Record elapsed time.

*Pass criterion:* Build exits 0 in under 5 minutes.

---

**MV-002 AC-009 — Mode 3 hardware validation (ProBook, no throttle)**

*Observable state:*
After the testid fix above, run AC-009 on ProBook (Intel i5-8265U, 4 cores, 8 GiB,
Windows 11) **without** CPU throttle. Measured render time ≤ 100ms.

*Confirmation method:* EL runs the AC-009 test on the ProBook without the 4× throttle.
Records: hardware specs, measured `renderMs`, pass/fail.

*Pass criterion:* Measured time ≤ 100ms. If exceeded: performance gap filed as a
blocking issue before G6 exits. Measurement record posted as a comment on #550.

*Dependency:* AC-009 testid fix must be merged before hardware run is performed.

---

**Validation report format:**
Single document at `docs/process/validation/m16-g6-accessibility-validation-report.md`.
Required sections: pre-condition (AC-009 testid fix — PR reference), VC-1 through
VC-4 findings (PASS/FAIL/CONDITIONAL PASS, method, observed values), MV-002 AC-009
hardware result (measured time, hardware specs), environment description, known
limitations, issues filed (if any), date.

---

**If blocking issues are found:**
If any VC check or AC-009 produces a FAIL, file a new GitHub issue against M16 before
G6 exits with label `compliance:major` (blocks launch) or `enhancement` (non-blocking
performance improvement). G6 does not fix blocking issues inline — a separate sprint
entry is required. G6 exit is CONDITIONAL if blocking issues are filed and open.

---

### 3.2 — Issues explicitly out of scope

| Issue / scope | Rationale for exclusion |
|---|---|
| Any implementation fixes for discovered VC failures | G6 is validation-only. Implementation responses require separate sprint entries. |
| #843 live external demo | G8 scope — G8 gate FULLY OPEN; not a G6 dependency |
| Any CI pipeline changes | Out of scope unless a G6 finding reveals a CI environment mismatch |
| M16 G1–G5, G9–G10 deliverables | Already closed or in separate sprint groups |

---

## Section 4 — ADR Prerequisite Summary

| Group | ADR required | ADR status | Implementation may begin? |
|---|---|---|---|
| G6 — accessibility + performance validation | None | N/A | **Yes — after EL approves this entry document** |

---

## Section 5 — Near-Miss Sweep

**Near-miss sweep date:** 2026-06-24
**Sweep period:** Since G10 sprint exit confirmed (2026-06-24)

| Finding | Category | PI Agent register call issued? | NM entry number |
|---|---|---|---|
| AC-009 test used `mode-3-activate` testid; source uses `mode3-toggle`; test has silently skipped the Mode 3 measurement since Mode 3 shipped in M12 (PR #778). Caught at G6 sprint entry authorship. Fourth recurrence of the NM-027 pattern class (silent no-op guard). | Process gap — test spec drift not caught at Mode 3 implementation time; NM-027 FA pre-PR checklist and QA post-ship activation check not executed at PR #778. | **YES — PI Agent register call issued** | **NM-058 (pending registry filing)** |

*Panel recommendation (FA + QA Lead + BPO + UX Designer, 2026-06-24): NM-058, severity **High**.
AC-009 has been cited as a passing CI gate for Mode 3 render performance in sprint exit
records for M12 through M15. Those citations are inaccurate — the test was measuring nothing.
Root cause: three-layer failure: (1) FA brief specified `mode-3-activate`; M12 implementation
used `mode3-toggle`; FA brief not updated; (2) NM-027 FA pre-PR checklist not executed at
PR #778; (3) NM-027 QA post-ship activation check not executed after Mode 3 shipped.
Prior sprint exits (M12–M15): record-and-forward — do not reopen; NM-058 is the permanent
record of inaccurate AC-009 coverage. Process improvement required: QA Lead working agreement
in `docs/process/agents.md` must add a named no-op guard locator audit step (grep-based,
run at every sprint entry) — converting a "remember to check" working agreement into a
reproducible audit. This improvement is G6 sprint work, executed alongside the testid fix PR.*

---

## EL Approval Record

**EL approval:** 2026-06-24

> G6 accessibility + performance validation sprint approved. Scope (VC-1 through VC-4,
> MV-002 AC-009 hardware validation, testid fix pre-condition), Infrastructure Sprint
> Exception, NM-058 register call, and parallel-track sequencing confirmed. Validation
> work may begin.
> — @PublicEnemage (2026-06-24)
