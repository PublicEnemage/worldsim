---
name: m15-g6-sprint-entry
type: sprint-entry
milestone: M15 — Human Cost Architecture
sprint-group: G6
status: Filed — awaiting EL approval before validation work begins
authored-by: PM Agent
authored-date: 2026-06-22
el-approved: false
release-branch: release/m15
sop-reference: docs/process/sprint-planning-sop.md
---

# Sprint Entry — M15, G6: Accessibility Validation

**Status:** Filed — awaiting EL approval before validation work begins
**Date authored:** 2026-06-22
**Release branch:** `release/m15`
**Sprint plan:** `docs/process/sprint-plans/m15-sprint-plan.md` (EL Approved 2026-06-20; amended 2026-06-21)

*Authority: `docs/process/sprint-planning-sop.md §Sprint Entry Gate` (Phase C output).
This entry gates G6 specifically. G6 is a parallel track — no sequential dependency on
G2, G3, G4, G5, G7, or G8. G6 does not gate G8; the G8 sprint entry is already open
and G8 is UNBLOCKED (G1 Step 5 Validate and G5 G8-gate conditions both satisfied
2026-06-22).*

**Infrastructure Sprint Declaration:** G6 is an infrastructure sprint. Its primary
deliverable is a validation report confirming hardware accessibility of the test suite
and Docker stack — not a user-facing capability. The intent document gate (§2.3) and QA
test authorship gate (§2.4) are waived under the Infrastructure Sprint Exception
(`docs/process/sprint-planning-sop.md §Infrastructure Sprint Exception`). Business PO
acceptance and Customer Agent Layer 3 assessment are not required at exit for G6
deliverables. PI Agent will review this declaration at exit and file a near-miss if
any G6 output is found to be user-visible and was incorrectly classified.

**Note on sprint plan exception:** The M15 sprint plan (`docs/process/sprint-plans/m15-sprint-plan.md
§Sprint Entry Gate Requirements`) listed G6 as an exception to the sprint entry document
requirement ("accessibility validation — testing and documentation only, no implementation
PR unless issues found"). This sprint entry is filed at EL direction to formalize the
scope, observable states, and exit conditions before validation begins — applying the same
rigor to infrastructure validation that the process requires for implementation sprints.

---

## Section 1 — Sprint Identification

| Field | Value |
|---|---|
| Milestone | M15 — Human Cost Architecture |
| GitHub Milestone | #16 |
| Sprint group | G6 — Accessibility Validation |
| Release branch | `release/m15` |
| Sprint plan document | `docs/process/sprint-plans/m15-sprint-plan.md` |
| Exit checklist issue | #984 |
| Sprint groups in scope | G6 only |
| ADR gate | None — validation and documentation; no new architecture |
| Implementing agents | Frontend Architect Agent (Playwright path validation); Chief Engineer Agent (Docker stack + simulation engine timing); PM Agent (validation report authorship) |
| Wave | Parallel — no sequential dependency on any other M15 sprint group |
| Sprint type | Infrastructure Sprint — no user-facing deliverables; intent and QA gates waived |

---

## Section 2 — Entry Invariants Checklist

*All items must be checked before G6 validation work begins.
An unchecked invariant blocks the sprint from opening.*

### 2.1 — Structural gates

- [x] **Release branch exists:** `release/m15` cut from `main` 2026-06-20 (commit 500e50d)
- [x] **CI trigger verified:** `.github/workflows/ci.yml` `pull_request: branches` includes
  `release/m*` — confirmed 2026-06-20 (line 5: `branches: [ main, develop, release/m* ]`;
  line 7: `branches: [ main, release/m* ]`). Ruleset ID 17751852 with 6 required checks:
  `changes`, `lint`, `test-backend`, `playwright-e2e`, `compliance-scan`, `branch-naming`.
  KI-005 permanent fix (`do_not_enforce_on_create: true`) applied 2026-06-20.
- [x] **Sprint plan EL-approved:** `docs/process/sprint-plans/m15-sprint-plan.md`
  `el-approved: 2026-06-20` (EL approval recorded 2026-06-20)

### 2.2 — ADR prerequisite gate

G6 contains no items requiring a new ADR. Accessibility validation is a testing and
documentation activity that does not introduce new application surfaces, new data contracts,
or new architectural patterns. If G6 uncovers performance or accessibility failures that
require architectural responses, those responses will be filed as new issues with their
own ADR assessment at filing time — they are not in G6 scope.

| Group | Required ADR | ADR status | Gate |
|---|---|---|---|
| G6 — #990 (accessibility validation) | None — validation and documentation only | N/A | **CLEAR** |

- [x] No ADR prerequisites for G6. Gate: **CLEAR**.

### 2.3 — Intent document gate

**Infrastructure Sprint Exception applies.**

G6 produces no user-facing deliverable. The primary output is a validation report
(a documentation artifact). Observable states for validation deliverables are
specification-confirmable directly from Section 3.1 below — a QA Lead can author
file-existence and exit-code checks from this entry document without a separate
intent document.

- [x] Infrastructure Sprint Exception declared in sprint entry frontmatter.
  Intent document gate **WAIVED** for G6 under `docs/process/sprint-planning-sop.md
  §Infrastructure Sprint Exception`.

*PI Agent note at exit gate: confirm that no G6 output is user-visible. If any
output modifies frontend components, API responses, or simulation outputs visible
to end users, the Infrastructure Sprint Exception does not apply and the exit gate
is blocked until intent and QA gates are retroactively satisfied.*

### 2.4 — QA test authorship gate

**Infrastructure Sprint Exception applies.**

G6 validation runs the existing test suite — it does not author new test code
for new deliverables. The three Playwright path checks in Section 3.1 (observable
state VC-3) are verified by running existing tests in a modified environment, not
by writing new test code. If blocking issues are found and implementation work is
required (per Section 3.1 §If blocking issues are found), those implementation groups
will require their own sprint entries with standard intent and QA gates.

- [x] Infrastructure Sprint Exception declared. QA test authorship gate **WAIVED** for G6.

---

## Section 3 — Scope Declaration

### 3.1 — Validation checks in scope

G6 must confirm four observable states, each corresponding to one of the four acceptance
criteria in issue #990. These are labelled VC-1 through VC-4 (Validation Checks). Each
observable state must be confirmed by an agent other than the EL and documented in the
validation report.

---

**VC-1 — Docker Compose stack starts and is responsive on target hardware**

*Observable state (pre-validation specification):*
On a machine with ≤ 8GB RAM and ≤ 4 CPU cores (or a CI equivalent with equivalent
resource constraints), `docker compose up --build` completes without error. After startup:
- `GET /api/v1/health` returns HTTP 200
- `GET /api/v1/entities` returns HTTP 200 with at least the four supported entities
  (GRC, JOR, EGY, ZMB) in the response body
- The frontend is reachable at `http://localhost:5173` (or the configured port) and the
  root page renders without a JavaScript error in the browser console
- Peak resident memory usage during startup does not exceed 7GB (leaving headroom for
  the OS on an 8GB machine)

*Confirmation method:* Chief Engineer Agent runs `docker compose up --build` on target
hardware or in a resource-constrained CI environment, captures startup log output, runs
the three HTTP checks, and records peak memory from `docker stats`. If a physical
ProBook or equivalent is available, run there; otherwise, use a GitHub Actions job with
`--memory="7g"` Docker flag as a proxy.

*Pass criterion:* All three HTTP checks return expected responses; no startup error in
API or frontend container logs; peak resident memory ≤ 7GB.

---

**VC-2 — Simulation engine completes an 8-step run within 60 seconds**

*Observable state (pre-validation specification):*
Starting from a clean application state on target hardware (8GB RAM, 4-core), a full
scenario run of 8 steps using the ZMB ECF fixture completes within 60 seconds of
`POST /api/v1/scenarios` returning 201. The timing is measured from the first step
advancement call (`POST /api/v1/scenarios/{id}/advance-step`) to the final step
result returning HTTP 200. All 8 step responses include `outputs.financial`,
`outputs.human_development`, `outputs.ecological`, and `outputs.governance` framework keys.

*Confirmation method:* Chief Engineer Agent or Frontend Architect Agent times the 8-step
run using `curl` or the frontend timer observable in browser devtools. Records wall-clock
time from first advance call to last advance response. Records whether all four framework
keys are present in the final step response.

*Pass criterion:* Wall-clock time ≤ 60 seconds. All four framework keys present in each
step response. If time exceeds 60s, the finding is filed as a new performance issue before
G6 exits.

---

**VC-3 — Playwright E2E suite has a documented path to run without the full Docker Compose stack**

*Observable state (pre-validation specification):*
`CLAUDE.md §Equitable Build Process` requires "a documented path to run without the full
Docker Compose stack so that contributors on modest hardware can run the complete test
suite locally." A document exists — or the existing `CONTRIBUTING.md` or `frontend/README`
contains a section — specifying how to run the Playwright E2E suite against a locally
started frontend dev server (without Docker). The path must be executable by a contributor
who does not have Docker installed.

Minimum required documentation:
1. Command to start the frontend dev server without Docker (e.g., `npm run dev` in `frontend/`)
2. Command to run the Playwright suite targeting the local dev server
3. Any backend mock or fixture requirement for the E2E tests to pass without the full stack
4. Known limitations or test coverage gaps when running without Docker (if any)

*Confirmation method:* Frontend Architect Agent follows the documented path on the host
machine (no Docker) and confirms the Playwright suite runs. Records which tests pass,
which skip, and which fail when Docker is absent. If no documented path exists, this is
a BLOCKING finding — G6 cannot exit until the path is documented.

*Pass criterion:* A documented non-Docker path exists in `CONTRIBUTING.md` or equivalent;
a contributor following it can run at least the non-API-dependent Playwright tests without
Docker. If the current test suite requires Docker for all tests, the documentation must
state this limitation and the issue #990 acceptance criterion is conditionally met (with
the limitation on record).

---

**VC-4 — Frontend build completes in under 5 minutes on target hardware**

*Observable state (pre-validation specification):*
On target hardware (8GB RAM, 4-core; or resource-constrained CI equivalent), `cd frontend
&& npm run build` completes in under 5 minutes from start to exit 0. The build produces
a `dist/` directory with the compiled frontend assets.

*Confirmation method:* Chief Engineer Agent or Frontend Architect Agent runs `time npm run build`
on target hardware or in a resource-constrained environment, records the elapsed time.

*Pass criterion:* Build exits 0 in under 5 minutes. If it exceeds 5 minutes, the finding
is documented in the validation report with the actual time, and a new issue is filed for
build optimisation before G6 exits.

---

**Validation report format:** A single document filed at
`docs/process/validation/m15-g6-accessibility-validation-report.md`.
Required sections: VC-1 through VC-4 findings (PASS/FAIL/CONDITIONAL PASS, confirmation
method used, observed values), hardware or CI environment description, known limitations,
issues filed (if any), and date of validation. The document is authored by the PM Agent
from Chief Engineer and Frontend Architect evidence; it is not authored by the Engineering Lead.

---

**If blocking issues are found:**
If any VC check produces a FAIL (not CONDITIONAL PASS), the implementing agent files a
new GitHub issue against the M15 milestone before G6 exits, with label `compliance:major`
if it blocks public launch or `enhancement` if it is a performance improvement not blocking
launch. G6 does not attempt to fix blocking issues inline — a separate sprint entry is
required for any implementation response. G6 exit is CONDITIONAL if blocking issues are
filed and open; PI Agent notes the condition in the sprint exit document.

---

### 3.2 — Issues explicitly out of scope

| Issue / scope | Rationale for exclusion |
|---|---|
| #569 — MV-002 Mode 3 hardware validation | Mode 3 (Active Control) is not implemented. AC-009 ("Full Mode 3 component set ≤ 100ms") requires the `mode-3-activate` data-testid, which does not exist. #569 remains blocked on Mode 3 delivery. Not in G6 scope. |
| Any implementation fixes for discovered issues | G6 is validation-only. If VC checks reveal blocking issues, implementation responses are separate sprint groups requiring their own sprint entries. |
| #845 Phase 4 Zone 1A implementation | G2 / G2-Phase 4 scope |
| #975 Path 1 backend + frontend | G4 scope — COMPLETE (BPO ACCEPT pending as of entry authorship) |
| #843 live external demo | G8 scope — G8 UNBLOCKED; not a G6 dependency |
| Any CI pipeline changes | Out of scope unless a G6 finding reveals a CI environment mismatch |

---

## Section 4 — ADR Prerequisite Summary

| Group | ADR required | ADR status | Implementation may begin? |
|---|---|---|---|
| G6 — accessibility validation | None | N/A | **Yes — after EL approves this entry document** |

G6 is purely validation and documentation work. No new architecture is introduced.
If G6 uncovers a need for architectural changes (e.g., build optimisation requiring a
new build pipeline), that work will be scoped in a separate sprint entry with an ADR
assessment at filing time.

---

## Section 5 — Near-Miss Sweep

**Near-miss sweep date:** 2026-06-22
**Sweep period:** Since M15-G5 sprint entry filed and G5 BPO ACCEPT confirmed (2026-06-22)

| Finding | Category | PI Agent register call issued? | NM entry number |
|---|---|---|---|
| No new process gaps identified in the sweep period. G5 exited clean; G4 Step 5 Validate pending BPO (not a near-miss — expected state). G8 UNBLOCKED 2026-06-22 as previously recorded. No deviation in G6 sprint entry authorship. | N/A | N/A | N/A |

*The Infrastructure Sprint Exception applied to G6 is not itself a near-miss — it is a
documented and SOP-compliant classification. PI Agent confirms the classification is
correct at exit: if any G6 output modifies user-visible application state, the PI Agent
files a near-miss for incorrect infrastructure classification.*

---

## EL Approval Record

**EL approval:** Pending

> {EL approval statement — to be filled at approval time}
> — @PublicEnemage (2026-06-22)
