---
name: m17-g5-sprint-entry
type: sprint-entry
milestone: M17 — Calibration and Comparative Infrastructure
sprint-group: G5 — Infrastructure Fixes
status: Filed — awaiting EL approval before implementation begins
authored-by: PM Agent
authored-date: 2026-06-25
el-approved: false
release-branch: release/m17
sop-reference: docs/process/sprint-planning-sop.md
---

# Sprint Entry — M17, G5: Infrastructure Fixes

**Status:** Filed — awaiting EL approval before implementation begins
**Date authored:** 2026-06-25
**Release branch:** `release/m17`
**Sprint plan:** `docs/process/sprint-plans/m17-sprint-plan.md` (EL Approved 2026-06-25)

*Authority: `docs/process/sprint-planning-sop.md §Sprint Entry Gate` (Phase C output).
G5 covers three infrastructure and capacity-allowing issues: #1220 (E2E test soft-skip
remediation — NM-061 upstream), #1214 (startup observability — NM-060 upstream), and #1251
(adaptive y-axis audit — capacity-allowing). None are demo critical-path. G5 runs after Wave 1
exit is confirmed (✅ confirmed 2026-06-25) and may run in parallel with G3 Phase 3 and G4 —
no dependency on G4 completion per the Wave 2 sequencing diagram. Implementation may not begin
on any G5 issue until this entry is EL-approved.*

*Sprint classification: #1220 and #1214 are infrastructure fixes (no user-facing persona impact;
modified intent document and QA test gate — see §2.3 and §2.4). #1251 is a conditional
UX-adjacent audit: if the audit produces no visible Zone 1A change, no intent document or
implementation PR is required; if it produces a visible change, a scoped intent document and
QA test must be filed before the implementation PR opens.*

---

## Section 1 — Sprint Identification

| Field | Value |
|---|---|
| Milestone | M17 — Calibration and Comparative Infrastructure |
| GitHub Milestone | #18 |
| Sprint group | G5 — Infrastructure Fixes |
| Release branch | `release/m17` |
| Sprint plan document | `docs/process/sprint-plans/m17-sprint-plan.md` |
| Exit checklist issue | #982 |
| Sprint groups in scope | G5 only |
| Issues in scope | #1220, #1214, #1251 |
| ADR gate | N/A — infrastructure fixes and zone audit within existing architecture (no structural decisions required) |
| Implementing agents | QA Lead (#1220 — E2E fix); Backend Engineer (#1214 — startup WARNING); Frontend Engineer (#1251 — if audit produces changes) |
| Wave | Wave 2 (Wave 1 exit confirmed 2026-06-25 — `docs/process/sprint-plans/m17-g1-sprint-exit.md`) |
| Demo dependency | None — no G5 issue is required before the Demo 7 session (#843, M18) is scheduled |
| Sequencing | Capacity-allowing — runs after Wave 1 exit; no dependency on G4 completion; may run in parallel with G3 Phase 3 and G4 |

**Issue classification summary:**

| Issue | Title | Classification | BPO acceptance required? |
|---|---|---|---|
| #1220 | fix(e2e): G3 spec AC-F1–AC-F7 soft-skip — NM-061 upstream | Infrastructure (E2E test fix) | No — test infrastructure; not user-facing |
| #1214 | feat(observability): startup WARNING if simulation_entities empty | Infrastructure (backend observability) | No — developer-facing diagnostic; not a persona-impacting feature |
| #1251 | ux(zone-1a): adaptive y-axis extension audit | Conditional — capacity-allowing UX-adjacent audit | If audit produces visible Zone 1A change: Yes; if audit-only finding or test-only gap: No |

---

## Section 2 — Entry Invariants Checklist

*All structural gates must be confirmed before any G5 implementation begins.
Per-issue conditions for #1251 (if the audit produces changes) apply before the implementation PR opens.*

### 2.1 — Structural gates

- [x] **Release branch exists:** `release/m17` cut from `main` 2026-06-25 (commit d806957)
- [x] **CI trigger verified:** `.github/workflows/ci.yml` `pull_request: branches` includes
  `release/m*` — confirmed at M17 kickoff 2026-06-25. Required checks: `changes`, `lint`,
  `test-backend`, `playwright-e2e`, `compliance-scan`, `branch-naming`.
  KI-005 permanent fix (`do_not_enforce_on_create: true`) applied 2026-06-20 — no Ruleset
  workaround required.
- [x] **Sprint plan EL-approved:** `docs/process/sprint-plans/m17-sprint-plan.md`
  `el-approved: 2026-06-25` (recorded 2026-06-25)
- [x] **Wave 1 exit gate confirmed:** G1 sprint exit document at
  `docs/process/sprint-plans/m17-g1-sprint-exit.md`; PI Agent confirmation on record
  2026-06-25; Wave 2 implementation sprint entries unblocked

**Structural gates: CLEAR.** All four checked.

### 2.2 — ADR prerequisite gate

*G5 issues are infrastructure fixes and a capacity-allowing audit within the existing zone
architecture established by ADR-017 (Zone 1A information architecture, ARCH-011, accepted M16).
No G5 issue introduces a new zone, a new data contract, a new encoding scheme, or a new
component boundary.*

- **#1220** (E2E test soft-skip remediation): modifies test files only. No production code
  change. No architectural implication. No ADR required.

- **#1214** (startup WARNING if simulation_entities empty): adds a backend startup log
  statement. No API contract change, no schema change, no simulation state change. No ADR
  required. Read `docs/schema/database.yml` and `docs/schema/api_contracts.yml` before
  writing any code that accesses `simulation_entities` — schema reads are mandatory
  pre-implementation steps per CLAUDE.md §Schema registry.

- **#1251** (adaptive y-axis extension audit): reviews `computeYDomain()` in Zone 1A
  rendering. If the audit concludes the existing implementation is correct and only test
  coverage needs extension: no structural change, no ADR required. If the audit reveals
  a visible Zone 1A y-axis behavior change is required — e.g., a change to the domain
  extension thresholds or the extension condition — assess whether this is an encoding
  refinement within the ADR-017 Zone 1A boundary (presumed: no new ADR) or a structural
  change to the composite encoding path (escalate to Architect before proceeding).
  **Presumption: no ADR required.** If the implementing agent determines an escalation is
  needed, stop and route to Architect and PM Agent before opening any implementation PR.

**ADR prerequisite status:**

| Issue | Required ADR | ADR status | Gate |
|---|---|---|---|
| #1220 — E2E test soft-skip remediation | None — test infrastructure | N/A | **CLEAR** |
| #1214 — Startup WARNING | None — backend observability; no contract change | N/A | **CLEAR** |
| #1251 — Adaptive y-axis audit | None presumed — audit-first; escalation path documented above | N/A (presumed) | **CLEAR — conditional escalation documented** |

- [x] **ADR prerequisite gate: CLEAR.** No new ADR required for any G5 issue under the
  presumed scope. Escalation path documented for #1251 if audit reveals structural scope.

### 2.3 — Intent document gate

*#1220 and #1214 are infrastructure fixes: they serve no named persona, produce no
user-observable state change, and have no acceptance criteria from a user journey. The
sprint entry template rule applies: infrastructure fixes where the test artifact IS the
deliverable do not require a separately authored intent document.*

*#1251 is an audit with conditional implementation. If the audit produces no visible Zone 1A
change (audit-finding only, or test-only coverage addition), no intent document is required.
If the audit reveals a visible change is needed, an intent document must be filed before the
implementation PR opens — the observable Zone 1A state after the change must be specifiable
from the audit output, not inferred from implementation.*

- [x] **Intent document gate for #1220:** Infrastructure — no intent document required.
  The fix is a test file correction. The observable state is that corrected assertions are
  hard-fail (not soft-skip) and green in CI after the fix.

- [x] **Intent document gate for #1214:** Infrastructure — no intent document required.
  The fix is a backend startup log addition. The observable state is that the WARNING log
  line appears in backend startup output when `simulation_entities` is empty.
  Developer-facing diagnostic; no persona interaction.

- [ ] **Intent document gate for #1251 (conditional):** Not required unless the audit
  produces a visible Zone 1A change. If changes are needed:
  - Intent document path: `docs/process/intents/M17-G5-{YYYY-MM-DD}-adaptive-y-axis-extension.md`
  - Must specify: the `computeYDomain()` extension condition being changed, the observable
    Zone 1A y-axis behavior before and after, and the persona acceptance criterion
    (Lucas Ferreira, Persona 1 — Zone 1A y-axis scale readable and non-misleading
    during threshold-crossing steps).
  - Must be filed before the implementation PR opens. **BLOCKING if audit produces a
    visible change.**

**Intent document status:**

| Deliverable | Classification | Intent document path | Filed? |
|---|---|---|---|
| #1220 — E2E test soft-skip remediation | Infrastructure | N/A — infrastructure classification | Not required |
| #1214 — Startup WARNING | Infrastructure | N/A — infrastructure classification | Not required |
| #1251 — Adaptive y-axis (if production change) | Conditional UX | `docs/process/intents/M17-G5-{YYYY-MM-DD}-adaptive-y-axis-extension.md` | No — conditional on audit outcome; **BLOCKING if audit produces visible change** |

### 2.4 — QA test authorship gate

*Infrastructure classifications for #1220 and #1214 modify the standard gate: the corrected
E2E spec IS the deliverable for #1220, and a backend unit test asserting the WARNING log line
IS the deliverable for #1214. In both cases the test is written as the fix — not gated on a
prior intent document for the same reason an intent document is not required. #1251 follows
the conditional gate: if no production change, no QA test required beyond any coverage
additions discovered by the audit; if a production change, QA test before implementation PR.*

**#1220 — E2E test soft-skip remediation:**

The deliverable is the corrected `frontend/tests/e2e/m16-g3-25year-human-capital-trajectory.spec.ts`.
The following must be confirmed before the #1220 fix PR merges:

1. **AC-1220-1 (AC-F1–AC-F7 soft-skip resolved):** All AC-F1 through AC-F7 assertions in
   the G3 spec are hard-fail — no `test.skip()`, `test.fixme()`, `.catch(() => false)`,
   or `isVisible().catch` guards that silently convert failures to passes. Audit command:
   `grep -rn "isVisible().catch\|test\.skip\|test\.fixme" frontend/tests/e2e/m16-g3-25year-human-capital-trajectory.spec.ts`
   must return no matches after the fix.

2. **AC-1220-2 (AC-F8 setup completeness — NM-061 resolution):** AC-F8 selects the created
   scenario in the UI before checking `human-capital-trajectory-panel` visibility. The fix
   follows the pattern in `mode3-active-control.spec.ts` and the AC-009 fix (PR #1211):
   after `createSen100StepScenario()` returns `scenario_id`, the Scenarios panel UI selects
   the scenario as primary before the visibility assertion runs.

3. **AC-1220-R (NM-056 + NM-061 guard):** No assertion in the corrected G3 spec uses a
   soft-skip pattern of either failure mode:
   - NM-058 pattern: `isVisible().catch(() => false)` guard where testid does not exist
   - NM-061 pattern: scenario created via API but never selected in UI before conditional
     render check

**Red-before-green requirement:** The fix PR description must document which assertion(s)
were confirmed to soft-skip (pass silently without asserting) before the change. This
confirms the failure mode existed and the fix is substantive, not cosmetic.

**#1214 — Startup WARNING if simulation_entities empty:**

Test file: `backend/tests/test_m17_g5_startup_warning.py`

1. **AC-1214-1 (WARNING emitted when empty):** Backend unit test asserts that when
   `simulation_entities` is empty at lifespan startup, the backend emits a structured
   `WARNING` log line containing the correct fix command
   (`python -m app.db.seed.natural_earth_loader`).

2. **AC-1214-2 (no WARNING when populated):** Same test asserts that when
   `simulation_entities` contains at least one row, no WARNING is emitted. Confirms
   the observability signal is not spurious on healthy stacks.

3. **AC-1214-R (startup not disrupted):** Backend startup completes normally in both cases.
   The WARNING is informational, not a fatal exception. Existing startup behavior — health
   endpoint returns 200, lifespan completes — is unaffected.

*Read `docs/schema/database.yml` before writing any code that accesses `simulation_entities`.*

**#1251 — Adaptive y-axis audit (conditional):**

The audit proceeds in two stages before any QA test is authored:

1. **Audit stage:** Review `computeYDomain()` in Zone 1A. Document the current extension
   condition, the scenarios where it fires, and whether existing Zone 1A test assertions
   cover the extension behavior. File an audit finding on GitHub issue #1251.

2. **Implementation stage (conditional on audit finding):**
   - "Current implementation correct, no change needed" → close audit; no test or
     implementation PR. The audit finding is the G5 #1251 deliverable.
   - "Test coverage gap only" → QA Lead adds assertions to the existing Zone 1A test suite
     without changing production code. Intent document not required.
   - "Production change needed (visible Zone 1A behavior change)" → file intent document;
     author QA test from intent document acceptance criteria; then open implementation PR.
     BPO acceptance required at exit.

**QA test file summary:**

| Issue | Test file | Gate |
|---|---|---|
| #1220 | `frontend/tests/e2e/m16-g3-25year-human-capital-trajectory.spec.ts` (corrected) | Red-before-green confirmation required in PR description |
| #1214 | `backend/tests/test_m17_g5_startup_warning.py` (new) | Authored before #1214 implementation PR opens |
| #1251 (if production change) | Existing Zone 1A test suite or `frontend/tests/e2e/m17-g5-adaptive-y-axis.spec.ts` (TBD at audit stage) | If production change: authored before implementation PR; if test-only or audit-only: not required |

**No soft-skip patterns permitted** (NM-056/NM-061 guard): The purpose of #1220 is to
eliminate soft-skip patterns from the G3 spec. No G5 test file may introduce the pattern
elsewhere. Any `test.skip()`, `test.fixme()`, or `.catch(() => false)` guard in a G5 PR
requires an NM entry authorizing it.

### 2.5 — Wave 2 dependency gate

- [x] **Wave 1 exit gate: CONFIRMED 2026-06-25**
  G1 sprint exit document: `docs/process/sprint-plans/m17-g1-sprint-exit.md`
  PI Agent confirmation: CONFIRMED — all Wave 1 exit conditions satisfied
  Session state: "Wave 2 implementation sprint entries now unblocked" (SESSION_STATE.md 2026-06-25)

**G5 has no dependency on G4 completion** — G5 runs in parallel with G4 and G3 Phase 3 per
the Wave 2 sequencing diagram (`m17-sprint-plan.md §Wave 2 sequencing diagram`). The only
prerequisite is Wave 1 exit, which is confirmed.

**Wave 2 gate: CLEAR.**

---

## Section 3 — Scope Declaration

### 3.1 — Issues in scope

| Issue | Title | Priority | Observable application state / deliverable |
|---|---|---|---|
| #1220 | fix(e2e): G3 spec AC-F1–AC-F7 soft-skip — NM-061 upstream | Bug / infrastructure | `frontend/tests/e2e/m16-g3-25year-human-capital-trajectory.spec.ts` contains no soft-skip patterns; all AC-F1 through AC-F8 assertions are hard-fail; AC-F8 selects the scenario via UI before checking `human-capital-trajectory-panel` visibility; CI `playwright-e2e` passes with all G3 assertions live (not silently skipped). |
| #1214 | feat(observability): startup WARNING if simulation_entities empty | Infrastructure | When the backend starts with `simulation_entities` empty, the startup log contains a structured `WARNING` line with the fix command (`python -m app.db.seed.natural_earth_loader`). When `simulation_entities` is populated, no WARNING is emitted. Backend startup and health endpoint behavior are unaffected in both cases. |
| #1251 | ux(zone-1a): adaptive y-axis extension audit | Capacity-allowing | Audit finding on #1251 documenting `computeYDomain()` current behavior and whether the extension condition is visually tested. If no production change: audit finding is the deliverable. If test-only gap: corrected test coverage with no production change. If production change: observable Zone 1A y-axis behavior per intent document. |

**Near-miss upstream traceability:**
- **#1220 ← NM-061** (AC-F8 silent no-op — scenario created via API, never selected in UI; 60-second ceiling gate measuring nothing since G3). Fix is the process improvement required by NM-061 §Immediate.
- **#1220 ← NM-056** (broader soft-skip pattern — NM-061 extends with the setup-completeness check). NM-058 testid-correctness audit + NM-061 setup-completeness audit together close the soft-skip failure mode family.
- **#1214 ← NM-060** (startup observability gap — empty `simulation_entities` produces silent 422 with no diagnostic signal). Fix is the process improvement required by NM-060 §Process improvement #1.

**M17 exit condition contribution (per sprint plan §Exit Conditions #5):**
- #1220: "demo script testid discipline (#1220/#1249 scope)"
- #1251: "visual distinguishability assertion extension (#1251 scope)"
- #1214: M16 retrospective testing improvements — observability gap closed (NM-060)

### 3.2 — Issues explicitly out of scope

| Issue / scope | Rationale for exclusion |
|---|---|
| #1249/#1250/#1253/#1239 — DEMO6 CRITICAL Polish (G4) | G4 sprint group; separate implementation PRs; Zone 1A, 1B, 1D changes. FA-recommended G4 sequence (#1249 → #1253 → #1250 → #1239) is G4-internal. |
| #1252 — Zone 1B proportional allocation (G3) | G3 sprint group; ADR-gated; Phase 1/2 must complete before Phase 3 implementation PR. |
| #394 — Multi-scenario comparison Phase 3 (G2) | G2 sprint group; gated on Phase 1/2 completion and #1249 merge. |
| Full G3 spec test coverage extension | #1220 is scoped to the identified soft-skip patterns (AC-F1–AC-F7 + AC-F8 per NM-061). A broader G3 spec coverage audit is not in scope — only the NM-056 + NM-061 remediation. |
| CONTRIBUTING.md further cleanup (NM-060) | NM-060 §Fix already records the CONTRIBUTING.md correction made in the originating commit. #1214 is the observability enhancement (startup WARNING), not additional documentation cleanup. |
| `computeYDomain()` refactor or Zone 1A algorithmic redesign | #1251 is scoped to an audit with a targeted fix if needed. A full algorithmic redesign is out of scope; if the audit reveals redesign is needed, a finding is filed on #1251 and escalated to the Architect as a separate issue. |
| #1275 — SEN institutional_capacity_index seed + GovernanceElasticity | Separate issue; unassigned G-group; Wave 2. No G5 overlap. |
| #1276 — Zone 1D governance horizon disclosure | Separate issue; unassigned G-group; Wave 2. No G5 overlap. |

---

## Section 4 — ADR Prerequisite Summary

| Group | ADR required | ADR status | Implementation may begin? |
|---|---|---|---|
| G5 — #1220 (E2E test fix) | None | N/A | Yes — after EL approves this entry |
| G5 — #1214 (startup WARNING) | None | N/A | Yes — after EL approves this entry; backend test authored before PR opens |
| G5 — #1251 (y-axis audit) | None presumed; conditional escalation documented in §2.2 | N/A | Audit begins after EL approval; implementation (if any) begins after audit finding and conditional intent document + test |

**No ARCH entry required.** All G5 deliverables are within existing architectural boundaries:
#1220 is test-only; #1214 is a backend logging addition with no schema or contract impact;
#1251 is within the Zone 1A rendering path established by ADR-017. If #1251 audit reveals
scope outside ADR-017, the §2.2 escalation path applies.

---

## Section 5 — Near-Miss Sweep

**Near-miss sweep date:** 2026-06-25
**Sweep period:** G4 sprint entry filing (2026-06-25) through G5 sprint entry filing (2026-06-25)

| Finding | Category | PI Agent register call issued? | NM entry number |
|---|---|---|---|
| No new process gaps identified in the sweep period. G4 and G5 are filed on the same day (2026-06-25). G5 issues (#1220, #1214) are the documented process improvements for NM-061 and NM-060 respectively — already on record. The infrastructure sprint classification for #1220 and #1214 (intent document not required where the test IS the deliverable) is consistent with the sprint entry template §2.3 rule and the precedent of not requiring intent documents for fixes whose observable state is the corrected test itself. No SOP deviations in this entry filing. | N/A | N/A | N/A |

**Pre-push gates (mandatory per issue type):**

- **#1220** (modifies `frontend/tests/e2e/` — test files, not `frontend/src/`): The frontend
  pre-push build gate (`cd frontend && npm run build`) applies to `frontend/src/` changes
  (CLAUDE.md §Frontend pre-push build gate). If #1220 modifies only test files, the build gate
  does not apply. Confirm before pushing: does the PR touch any `frontend/src/` file? If yes,
  build gate is mandatory. The `playwright-e2e` CI check is the primary verification gate.

- **#1214** (Python backend change): Backend pre-push lint gate is mandatory:
  `cd backend && ruff check . && mypy app/`
  Both must exit 0 before the #1214 branch is pushed. `ruff check . --fix` resolves most
  violations; fix any remaining before pushing (CLAUDE.md §Backend pre-push lint gate; NM-016).

- **#1251** (Zone 1A — conditional): If the audit produces a production change in `frontend/src/`,
  the frontend pre-push build gate applies: `cd frontend && npm run build` must exit 0.

---

## EL Approval Record

**EL approval:** Pending

> {EL approval statement — to be filled at approval time}
> — @PublicEnemage ({date})
