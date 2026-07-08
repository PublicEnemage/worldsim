---
name: m20-sprint-g4-entry
type: sprint-entry
milestone: M20 — Analytical Evidence Portfolio and Demo 9
sprint-group: G4
status: EL-approved
authored-by: PM Agent
authored-date: 2026-07-08
el-approved: 2026-07-08
release-branch: release/m20
sop-reference: docs/process/sprint-planning-sop.md
---

# Sprint Entry — M20 G4 — DEMO Maintenance and Test Fix

**Status:** EL-approved — implementation authorised (in-session 2026-07-08 — EL directive "agreed")
**Date authored:** 2026-07-08
**Release branch:** `release/m20`
**Sprint plan:** `docs/process/sprint-plans/m20-sprint-plan.md`

*Authority: `docs/process/sprint-planning-sop.md §Sprint Entry Gate` (Phase C output).*

---

## Section 1 — Sprint Identification

| Field | Value |
|---|---|
| Milestone | M20 — Analytical Evidence Portfolio and Demo 9 |
| GitHub Milestone | #22 |
| Sprint number | G4 |
| Release branch | `release/m20` |
| Sprint plan document | `docs/process/sprint-plans/m20-sprint-plan.md` |
| Exit checklist issue | #1773 |
| Sprint groups in scope | G4 |
| Wave coordination tier | Standard — small engineering sprint; four independent issues; no cross-group dependencies |
| Concurrent groups at entry | 0 — G3 closed 2026-07-07 |
| Cross-group dependencies | None — G4 is independent of G1–G3 documentation work |

---

## Section 2 — Entry Invariants Checklist

### 2.1 — Structural gates

- [x] **Release branch exists:** `release/m20` — confirmed; G3 integration PR merged 2026-07-07; state-sync-009 (PR #1833) merged 2026-07-08
- [x] **CI trigger verified:** `.github/workflows/ci.yml` `pull_request: branches` includes `release/m*`
- [x] **Sprint plan EL-approved:** `docs/process/sprint-plans/m20-sprint-plan.md` EL-approved in session 2026-07-07

### 2.2 — ADR prerequisite gate

**N/A — Demo 8 backlog maintenance sprint.** G4 deliverables are fixes to existing UI components and a test isolation defect. No new architectural capability is introduced; no new ADR is required. All three DEMO fixes operate within the existing Zone 1B / Mode 3 instrument architecture (ADR-015 through ADR-020 as applicable). The asgi_client pool ordering fix (#1759) is a test infrastructure repair.

| Group | Required ADR | ADR status | Gate |
|---|---|---|---|
| G4 | None | N/A | CLEAR |

### 2.3 — Intent document gate

**Process judgment — Demo 8 backlog fixes with full issue specification.** Each G4 deliverable has a detailed defect description or stakeholder-confirmed acceptance criterion in the referenced GitHub issue and Demo 8 review documents. For small, well-scoped backlog fixes, the combination of (a) DEMO-NNN audience simulation finding, (b) stakeholder review confirmation, and (c) GitHub issue acceptance criterion constitutes the functional specification.

Formal intent documents at `docs/process/intents/` are filed before implementation begins (before first PR is opened on each item). PM Agent files them at sprint kick-off, using the issue descriptions and Demo 8 review findings as inputs.

| Deliverable | Functional specification source | Intent document | Gate |
|---|---|---|---|
| DEMO-217 (Act 1 → Act 2 link) | Demo 8 stakeholder review Q7 (DEMO-217 CRITICAL finding) | To be filed at sprint kick-off — before first PR | PENDING |
| #1775 / DEMO-233 (WARNING alongside CLEAR) | Issue #1775 body + Demo 8 Step 6c DEMO-233 finding | To be filed at sprint kick-off — before first PR | PENDING |
| #1776 / DEMO-234 (precision vs CI label) | Issue #1776 body + Demo 8 Step 9 DEMO-234 finding | To be filed at sprint kick-off — before first PR | PENDING |
| #1759 / NM-099 (asgi_client pool ordering) | NM-099 registry entry + Issue #1759 defect description | Not required — test infrastructure fix, not user-facing | CLEAR |
| #1791 / NM-101 (G2C Type B baseline pre-run) | NM-101 registry entry + Issue #1791 defect description | Not required — test logic fix, not user-facing | CLEAR |

### 2.4 — QA test authorship gate

Engineering sprint — QA tests required for user-facing deliverables.

| Deliverable | Test type | Test file path | Authored before implementation? |
|---|---|---|---|
| DEMO-217 (Act 1 → Act 2 link) | E2E | `frontend/tests/e2e/m20-g4-act-navigation-link.spec.ts` | To be authored at sprint kick-off — before implementation PR |
| #1775 / DEMO-233 (WARNING + CLEAR) | E2E | `frontend/tests/e2e/m20-g4-warning-clear-badge.spec.ts` | To be authored at sprint kick-off — before implementation PR |
| #1776 / DEMO-234 (precision vs CI label) | E2E | `frontend/tests/e2e/m20-g4-precision-label.spec.ts` | To be authored at sprint kick-off — before implementation PR |
| #1759 / NM-099 (asgi_client pool ordering) | Unit/integration | `backend/tests/test_m19_cm_b_elasticity_calibration.py` (existing — fix is in conftest scope) | N/A — the fix itself constitutes the test repair; verify via `pytest -m backtesting -k test_m19_cm_b` run in isolation |
| #1791 / NM-101 (G2C Type B baseline pre-run) | Backtesting integration | `backend/tests/backtesting/test_m19_g2c_scenario_runs.py` (existing — 7 methods get one-line insertion) | N/A — the fix itself constitutes the test repair; post-fix verdicts recorded from CI run as new known-good values |

### 2.5 — Normative assumption adversarial test

**N/A — no composite normalization changes.** G4 makes no changes to `SINGLE_ENTITY_REFERENCE_RANGES` or any composite normalization table. Gate does not apply.

- [x] This sprint makes no changes to composite normalization tables — gate N/A

---

## Section 3 — Scope Declaration

### 3.0 — Scope lock confirmation

- [x] All ADR decisions affecting this sprint's scope are EL-approved and merged to `release/m20`

**No scope uncertainty.** All five G4 deliverables are defect fixes or backlog closures with well-established acceptance criteria. #1791 scope confirmed by EL 2026-07-08.

### 3.1 — Issues in scope

| Issue | Title | Group | Priority |
|---|---|---|---|
| DEMO-217 | In-viewport Act 1 → Act 2 navigation link | G4 | High — Demo 8 CRITICAL structural finding; presenter risk |
| #1775 / DEMO-233 | WARNING badge not displayed alongside CLEAR in Zone 1B | G4 | Medium — stakeholder Q2 expectation gap |
| #1776 / DEMO-234 | Binary-search precision label (±0.01) vs CI label (0.08 width) | G4 | High — numerically literate stakeholder confusion (Lucas Q1) |
| #1759 / NM-099 | asgi_client fixture pool ordering fix in test_m19_cm_b | G4 | High — test suite fails in isolation; masks real failures |
| #1791 / NM-101 | G2C Type B tests — add baseline pre-run before baseline_run_id | G4 | High — all 7 Type B direction verdicts are INDISTINGUISHABLE (false negative); one-line fix per method |

### 3.2 — Issues explicitly out of scope

| Issue | Title | Horizon | Rationale |
|---|---|---|---|
| #1777 / DEMO-235 | PSP driver arc missing in multi-scenario view | M21 | Assessed as more substantial than G4 DEMO fixes; deferred per sprint plan to preserve M20 bandwidth |
| DEMO-235 / #1777 | PSP driver arc missing in multi-scenario view | M21 | Assessed as more substantial; deferred per sprint plan |
| #1797 | Failure mode non-detection (EURO-AREA rapid-onset) | M21+ | Engine gap; no implementation in M20 |
| #1824 | fiscal_balance Zone 1D annotation | M21 | Filed this session; out of M20 scope |
| #1825 | Debt-stabilising balance layer | M22+ | Long-term; requires CM computation spec first |
| ADR-008 renewal | SCAN-029 carry-forward | M20 | Not G4; assign to Architect Agent separately |

---

## Section 4 — Deliverable Specifications

### DEMO-217 — Act 1 → Act 2 in-viewport navigation link

**Problem (from Demo 8 stakeholder review Q7):** The constraint-floor result (Act 1, Mode 3 Active Control) and the distributional comparison (Act 2, Replay mode) live in separate scenario views. Navigation between them required 38 seconds with preparation. The demo requires pre-configured scenarios and a rehearsed path. Cold navigation is not achievable.

**Acceptance criterion:** An in-viewport link or button on the constraint-floor result display navigates directly to the associated distributional comparison scenario without requiring the user to manually select from the scenario list. The link is visible without scrolling when the constraint-floor result is displayed.

**Scope:** Frontend only — no backend changes required.

### #1775 / DEMO-233 — WARNING badge alongside CLEAR

**Problem (from Issue #1775):** When the constraint-floor search returns CLEAR, Zone 1B does not simultaneously display a WARNING badge for indicators near (within 5% of) the MDA floor. Stakeholder Q2: "Can I see both the CLEAR badge and a warning if the margin is narrow?"

**Acceptance criterion:** When CLEAR with narrow margin (margin < 5% of MDA floor), a WARNING badge is displayed alongside the CLEAR badge in Zone 1B. Behavior is consistent with existing MDA alert behavior in non-constraint-search context.

**Scope:** Frontend only — Zone 1B badge display logic.

### #1776 / DEMO-234 — Precision label vs CI label

**Problem (from Issue #1776):** The ±0.01 binary-search tolerance band and the CI interval (e.g. 0.08 width) are displayed without clear differentiation. A numerically literate stakeholder immediately asks if they are the same quantity. They are not: ±0.01 is the search stopping criterion; 0.08 is distributional uncertainty on the poverty headcount estimate.

**Acceptance criterion:** The tolerance band is labelled as "search precision ±0.01" (or equivalent unambiguous label) and the CI band is labelled distinctly (e.g. "95% CI: [lower, upper]"). The two quantities are visually distinct and their different meanings are evident without tooltip or documentation reference.

**Scope:** Frontend display and label text. Possible backend label field if the tolerance value is returned from the constraint search API response.

### #1759 / NM-099 — asgi_client pool ordering fix

**Problem (from NM-099):** The `asgi_client` fixture in `backend/tests/test_m19_cm_b_elasticity_calibration.py` does not call `create_asyncpg_pool()`. Pool initialization is provided by `_asyncpg_pool_lifecycle` autouse fixture in `tests/backtesting/conftest.py` — which only applies within `tests/backtesting/`. The test passes in the full suite by ordering accident (backtesting conftest loaded first alphabetically) and fails when run in isolation.

**Acceptance criterion:** `pytest -m backtesting -k test_m19_cm_b` passes when invoked without the full pytest suite — i.e. when `tests/backtesting/` tests are not collected first. The fix must not alter test semantics.

**Scope:** Test infrastructure only — `backend/tests/test_m19_cm_b_elasticity_calibration.py` fixture or conftest adjustment.

### #1791 / NM-101 — G2C Type B baseline pre-run

**Problem (from NM-101):** All 7 Type B test methods in `test_m19_g2c_scenario_runs.py` (GRC, ARG, LKA, PAK, TUR, EGY, GHA) create a baseline scenario via `POST /api/v1/scenarios` but never run it before passing its ID as `baseline_run_id` to `run_harness`. `_fetch_trajectory(baseline_run_id)` returns empty steps; `_classify_direction` computes all-zero `per_step_diff` and returns `INDISTINGUISHABLE`. GRC confirmed correct verdict with pre-run baseline: `COUNTER_FACTUAL_BETTER`.

**Fix:** One-line insertion in each of the 7 affected methods, immediately after `baseline_id = ...json()["scenario_id"]`:
```python
await asgi_client.post(f"/api/v1/scenarios/{baseline_id}/run")
```

**Acceptance criterion:** `pytest -m backtesting -k "TypeB or type_b"` produces real direction verdicts (not `INDISTINGUISHABLE`) for all 7 classes. GRC asserts `COUNTER_FACTUAL_BETTER`. Remaining 6 post-fix verdicts are recorded from the CI run as new known-good values.

**Scope:** Test logic only — `backend/tests/backtesting/test_m19_g2c_scenario_runs.py`, 7 method insertions.

---

## Section 5 — Near-Miss Sweep

**Near-miss sweep date:** 2026-07-08
**Sweep period:** Since G3 sprint entry (2026-07-07)

| Finding | Category | PI Agent register call issued? | NM entry number |
|---|---|---|---|
| No new findings | — | — | — |

Scope discrepancy (#1791 in cockpit but absent from sprint plan deliverables table) resolved by EL confirmation 2026-07-08 — #1791 confirmed in G4 scope.

---

## Section 6 — Sprint Group Isolation (M18 onward)

### 6.1 — Sprint sub-branch

| Field | Value |
|---|---|
| Sprint sub-branch | `sprint/m20-g4` |
| Cut from | `release/m20` (at state-sync-009 tip — post PR #1833 merge) |
| Sprint journal issue | #1834 |

**PM Agent sprint sub-branch cut command (at EL approval):**
```bash
git checkout -b sprint/m20-g4 release/m20 && git push -u origin sprint/m20-g4
```

### 6.2 — File-conflict risk assessment

| File | Lane required | Trigger |
|---|---|---|
| `SESSION_STATE.md` | PM Agent coordination lane (chore/m20-state-sync) | Sprint exit cockpit update — NOT on sprint branch |
| `docs/process/near-miss-registry.md` | Sprint sub-branch (PI Agent authors in same PR) | If new NM identified during implementation |
| `docs/compliance/scan-registry.md` | Sprint sub-branch | Only if compliance scan produced at G4 exit |
| Frontend source files (`frontend/src/`) | Sprint sub-branch | DEMO-217, DEMO-233, DEMO-234 implementation |
| `backend/tests/test_m19_cm_b_elasticity_calibration.py` | Sprint sub-branch | #1759 fix |
| `backend/tests/backtesting/test_m19_g2c_scenario_runs.py` | Sprint sub-branch | #1791 fix (7 method insertions) |
| Backend API source (if #1776 requires label field) | Sprint sub-branch | DEMO-234 — confirm at implementation |

### 6.3 — Infrastructure dependency declaration

- [x] No DS-owned file changes required

**Pre-push gate applies:** `.githooks/pre-push` enforces ruff + mypy (backend) and `npm run build` (frontend). G4 touches both backend (`backend/tests/`) and frontend (`frontend/src/`). Both gate checks will fire on push.

#### 6.3a — New output paths declaration

- [x] No new output directories. E2E test files go to `frontend/tests/e2e/` — existing path. No `.gitignore` changes needed.

### 6.4 — Cross-group dependency declaration

- [x] No cross-group dependencies. G4 is independent of G1–G3.

### 6.5 — Prior NM verification

| NM entry | Process improvement required | Applied in this sprint? |
|---|---|---|
| NM-099 | asgi_client fixture must initialise asyncpg pool independently of test ordering | Yes — #1759 is the fix issue; addressed as G4 primary deliverable |
| NM-100 | Run `git diff HEAD --name-only` and verify every file named in PR description appears before opening any multi-file PR | Yes — will apply before each PR in G4 |
| NM-101 | Pre-run baseline via `POST /api/v1/scenarios/{baseline_id}/run` before `run_harness(run_type=TYPE_B, baseline_run_id=X)` | Yes — #1791 is the fix issue; addressed as G4 primary deliverable |

---

## EL Approval Record

**EL approval:** Confirmed in session — "agreed"

> "agreed" — #1791 confirmed in G4 scope.
> — @PublicEnemage (2026-07-08)
