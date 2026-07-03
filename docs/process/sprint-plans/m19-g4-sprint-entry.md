---
name: m19-g4-sprint-entry
type: sprint-entry
milestone: M19 — Constraint Search and Empirical Calibration
sprint-group: G4 — PSP Driver Arc + CI Label Polish
status: Filed
authored-by: PM Agent
authored-date: 2026-07-03
el-approved: 2026-07-03
release-branch: release/m19
sop-reference: docs/process/sprint-planning-sop.md
---

# Sprint Entry — M19, G4: PSP Driver Arc + CI Label Polish

**Status:** Filed — awaiting EL approval before implementation begins
**Date authored:** 2026-07-03
**Release branch:** `release/m19`
**Sprint plan:** `docs/process/sprint-plans/m19-sprint-plan.md`

*Authority: `docs/process/sprint-planning-sop.md §Sprint Entry Gate` (Phase C output).
Changes to this template require PM Agent authorship and EL endorsement.*

---

## Section 1 — Sprint Identification

| Field | Value |
|---|---|
| Milestone | M19 — Constraint Search and Empirical Calibration |
| GitHub Milestone | #21 |
| Sprint number | 5 (G4 — Wave 2–3) |
| Release branch | `release/m19` |
| Sprint plan document | `docs/process/sprint-plans/m19-sprint-plan.md` |
| Exit checklist issue | #1535 |
| Sprint groups in scope | G4 |
| Wave coordination tier | Standard (coordination gate with G3 cleared; G4 is sole active implementation group at entry) |
| Concurrent groups at entry | 1 (G4 only; G2D in pre-gate pending ADR-020 acceptance — no implementation PRs open) |
| Cross-group dependencies | G3 #1537 merged to `sprint/m19-g3` — coordination gate CLEARED (SESSION_STATE.md 2026-07-03) |

---

## Section 2 — Entry Invariants Checklist

*All items must be checked before any implementation PR is opened for this sprint.
An unchecked invariant blocks the sprint from opening.*

### 2.1 — Structural gates

- [x] **Release branch exists:** `release/m19` cut from `main` 2026-07-02 at 1bf1ecc
- [x] **CI trigger verified:** `.github/workflows/ci.yml` `pull_request: branches` includes `release/m*` (verified at M19 kickoff; sprint-branch-ci-gate Ruleset active)
- [x] **Sprint plan EL-approved:** `docs/process/sprint-plans/m19-sprint-plan.md` — EL-approved 2026-07-02

### 2.2 — ADR prerequisite gate

*G4 has no ADR prerequisite. Neither #1528 (PSP driver auditability panel) nor #1529 (CI label
precision fix) requires a new ADR: both are frontend-only changes that implement within the
bounds of existing ADR-007 (CI band display contract) and ADR-019 (control plane column).
The coordination gate that applied to G4 at sprint plan time — G3 #1537 `band_method` field
terminology settled — is CLEARED as of 2026-07-03 (SESSION_STATE.md: G3 confirmed; G3 #1537 ✓).*

- [x] All groups with `BLOCKED_ADR` status have their required ADR accepted — **CLEAR: no BLOCKED_ADR for G4**

**ADR prerequisite status:**

| Group | Required ADR | ADR status | Gate |
|---|---|---|---|
| G4 — PSP driver auditability panel (#1528) | N/A | N/A | CLEAR |
| G4 — CI label precision fix (#1529) | N/A | N/A | CLEAR — coordination gate with G3 #1537 satisfied |

### 2.3 — Intent document gate

*Both #1528 and #1529 are user-facing deliverables — they produce visible changes in the
instrument (Zone 1D expand panel; CI label/tooltip in DistributionalComparisonSummary).
Intent documents must be filed before implementation PRs open. The gate is not blocked — no
BLOCKED_ADR condition applies — so intent documents are filed after EL approves this entry,
before the first implementation PR opens.*

- [x] Intent document filed for every user-facing deliverable in this sprint

**Intent document status:**

| Deliverable | ADR reference | Intent document path | Filed? |
|---|---|---|---|
| PSP driver auditability panel — Zone 1D expand affordance (#1528) | ADR-019 (control plane column; Zone 1D scope) | `docs/process/intents/M19-G4-2026-07-03-psp-driver-auditability-panel.md` | Yes — 2026-07-03 |
| '95% CI' label precision fix (#1529) | ADR-007 (CI band display contract; `band_method` field from G3 #1537) | `docs/process/intents/M19-G4-2026-07-03-ci-label-precision.md` | Yes — 2026-07-03 |

*The #1529 intent document must reference the `band_method` enum values settled in G3 #1537
(now merged). The implementing agent must read the merged #1537 PR before filing the intent
document — the label text depends on which `band_method` values G3 defined.*

### 2.4 — QA test authorship gate

*QA tests must be authored from the intent document's acceptance criteria before implementation
code is written. The test authorship gate is not independently blocked — it follows from the
intent document gate above.*

- [x] QA test file authored for every user-facing deliverable in this sprint

**QA test status:**

| Deliverable | Intent document | Test file path | Authored before implementation? |
|---|---|---|---|
| PSP driver auditability panel (#1528) | `docs/process/intents/M19-G4-2026-07-03-psp-driver-auditability-panel.md` | `frontend/tests/e2e/m19-g4-psp-driver-auditability.spec.ts` | Yes — 2026-07-03 |
| CI label precision fix (#1529) | `docs/process/intents/M19-G4-2026-07-03-ci-label-precision.md` | `frontend/tests/e2e/m19-g4-ci-label-precision.spec.ts` | Yes — 2026-07-03 |

*NM-086 process requirement: QA Lead must verify any E2E mock routes against `api_contracts.yml`
before the intent document is approved. This is a blocking checklist item on the test authorship
gate for both deliverables. #1528 may introduce a new API call to retrieve PSP driver attribution
data — any mock helper for that call must match the contract-declared response shape.*

---

## Section 3 — Scope Declaration

### 3.0 — Scope lock confirmation (NM-081)

- [x] All ADR decisions affecting this sprint's scope are EL-approved and merged to `release/m19`

**Scope uncertainty:** None. ARCH-016 (ADR-007 amendment) accepted 2026-07-03 and G3 integration
PR #1617 auto-merging to `release/m19`. G4 scope depends only on: (1) ADR-007 band display
contract (stable), (2) ADR-019 Zone 1D scope (stable), (3) G3 #1537 `band_method` field
terminology (settled — field names confirmed in the merged PR). No pending EL decisions affect G4.

### 3.1 — Issues in scope

| Issue | Title | Group | Priority |
|---|---|---|---|
| #1528 | PSP driver arc across programme window + in-viewport auditability panel (DEMO-165) | G4 | High — Zone 1D completeness; Demo 8 auditability parity with Zone 3 |
| #1529 | '95% CI' label precision fix on DistributionalComparisonSummary | G4 | High — Demo 8 Act 2 label credibility under Lucas (Persona 1) scrutiny; G3 north star CONDITIONAL PASS condition |

### 3.2 — Issues explicitly out of scope

| Issue | Title | Horizon | Rationale for exclusion |
|---|---|---|---|
| #1553 | Iceland 2008–11 orthodox vs heterodox Type A+B | G2D (Wave 2, pre-gate) | Blocked — ADR-020 (ARCH-014) not yet accepted; separate sprint group |
| #1544 | Demo 8 — live stakeholder session | Wave 3 (exit gate) | Post-G4 deliverable; milestone exit gate |
| #1535 | M19 Exit Checklist | Gate issue | Milestone exit gate — not an implementation deliverable |
| #1456 | MDAAlertPanel Zone1B: scenarioId crash | Pre-wave (standalone) | Standalone crash fix not in G4 scope; addressed pre-wave |
| #1538 | Focal cohort floor validation | Pre-wave (standalone) | G1 prerequisite — already delivered pre-wave |

---

## Section 4 — ADR Prerequisite Summary

| Group | ADR required | ADR status | Implementation may begin? |
|---|---|---|---|
| G4 — #1528 (PSP driver auditability panel) | None — within ADR-019 Zone 1D scope | N/A | Yes — after EL approves entry and intent document is filed |
| G4 — #1529 (CI label precision fix) | None — within ADR-007 band display contract | N/A | Yes — after EL approves entry, intent document is filed, and #1529 intent references G3 #1537 `band_method` enum values |

*Neither G4 deliverable extends into territory requiring a new ADR. The PSP driver auditability
panel is a Zone 1D expansion fully within the ADR-019 layout reservation. The CI label fix
is a display-contract refinement within ADR-007 — the band_method field that enables the fix
was already accepted in ARCH-016.*

---

## Section 5 — Near-Miss Sweep

**Near-miss sweep date:** 2026-07-03
**Sweep period:** Since G3 sprint entry (2026-07-02)

| Finding | Category | PI Agent register call issued? | NM entry number |
|---|---|---|---|
| Agent used `git stash --include-untracked` as recovery action; stashed EL in-progress G2C work without authorization | Near-miss | Yes — filed 2026-07-02 | NM-087 |
| Parallel Claude Code sessions sharing main working tree; branch displacement caused lost files and misrouted commits | Near-miss | Yes — filed 2026-07-03 | NM-088 |

*Both NM-087 and NM-088 are process improvements that apply directly to G4 implementation
sessions. See §6.5 for how each applies.*

---

## Section 6 — Sprint Group Isolation (M18 onward)

### 6.1 — Sprint sub-branch

| Field | Value |
|---|---|
| Sprint sub-branch | `sprint/m19-g4` |
| Cut from | `release/m19` |
| Sprint journal issue | #1624 |

**PM Agent sprint sub-branch cut command (run after EL approval):**
```bash
git checkout -b sprint/m19-g4 release/m19 && git push -u origin sprint/m19-g4
```

*Note: per NM-087 and NM-088, the agent cutting the sprint branch must run
`git status --porcelain` before any checkout. If the main working tree is dirty, stop and
report to EL before proceeding. If another CC session is active on the same repository, a
dedicated worktree must be allocated before branch operations begin.*

### 6.2 — File-conflict risk assessment

| File | Lane required | Trigger |
|---|---|---|
| `SESSION_STATE.md` | PM Agent coordination lane | Sprint exit cockpit update |
| `docs/process/near-miss-registry.md` | PM Agent coordination lane (PI Agent authors) | If NM identified during sprint |
| `docs/compliance/scan-registry.md` | PM Agent coordination lane | If compliance scan produced at sprint exit |
| `frontend/src/components/FourFrameworkZone1D.tsx` | Sprint sub-branch | Primary implementation file for #1528 PSP driver panel |
| `frontend/src/components/DistributionalComparisonSummary.tsx` (or Zone 1B render path) | Sprint sub-branch | CI label change for #1529 |
| `frontend/tests/e2e/m19-g4-*.spec.ts` | Sprint sub-branch | QA test files for both deliverables |
| `docs/process/intents/M19-G4-*.md` | Sprint sub-branch | Intent documents for both deliverables |

**No file-area overlap with G2D:** G2D (#1553 Iceland) touches `backend/app/simulation/` and
backtesting fixture files — no overlap with G4's frontend-only scope. If G2D begins
implementation in parallel with G4, file-conflict risk is Low.

**G3 integration PR (#1617) merged (2026-07-03):** G3 integration PR #1617 confirmed merged
to `release/m19`. The sprint branch `sprint/m19-g4` may now be cut from `release/m19` and
will include G3 #1537 `band_method` field. Branch-cut precondition CLEARED.

### 6.3 — Infrastructure dependency declaration

- [x] No DS-owned file changes required

No changes to `.github/workflows/`, `.githooks/`, or `.gitignore` are anticipated. G4
introduces no new backend modules, no new output directories, and no new CI configuration.

#### 6.3a — New output paths declaration (NM-069)

- [x] No new output directories — all generated paths are already covered by `.gitignore`

*G4 is a pure frontend change — Zone 1D panel expansion and a label fix. No new output
directories are introduced by either deliverable.*

### 6.4 — Cross-group dependency declaration

- [x] Resolved — coordination gate with G3 CLEARED

**G4 #1529 coordination gate status:**
> The coordination requirement declared in G3 sprint entry §6.4 — "G3 #1537 implementation
> PR must be merged to `sprint/m19-g3` before G4 #1529 implementation PR opens" — is now
> SATISFIED. G3 is confirmed (2026-07-03). G3 #1537 (BandResult visible fields, `band_method`
> enum) is merged. The `band_method` field values and `is_pre_calibration` display contract
> are settled in the merged PR.
>
> G4 implementing agent must read the merged #1537 PR before authoring the #1529 intent
> document, to ensure the label text references the correct `band_method` enum values.
>
> No remaining cross-group merge ordering constraints apply to G4.

### 6.5 — Prior NM verification (NM-068 process improvement)

**NM verification sweep date:** 2026-07-03
**Sweep period:** Since G3 sprint entry (2026-07-02)

| NM entry | Process improvement required | Applied in this sprint? |
|---|---|---|
| NM-084 | CM sign-off on calibration/fixture PRs must precede auto-merge; PI Agent posts gate comment before implementing agent sets auto-merge | N/A — G4 has no calibration or fixture PRs; CM sign-off gate does not apply |
| NM-085 | Sprint entry §6.2 must document co-dependent fixture sequencing risk | N/A — G4 is not fixture work; no co-dependent test shells anticipated |
| NM-086 | QA Lead mock-helper verification against `api_contracts.yml` is a blocking checklist item on intent authorship; E2E mock routes must match contract before implementation PR opens | Yes — declared in §2.4 as a blocking condition on the test authorship gate for both deliverables. Particularly relevant to #1528 if a new backend call is introduced for PSP driver attribution retrieval |
| NM-087 | Pre-checkout dirty-tree guard: `git status --porcelain` before any `git checkout` or `git checkout -b`; if dirty, stop and report to EL; no `git stash` as recovery action without EL authorization | Yes — declared in §6.1 branch-cut note; implementing agent must run dirty-tree check before any branch operation in this sprint |
| NM-088 | Parallel CC session worktree requirement: if another CC session is active on this repository simultaneously, each session must operate in a dedicated git worktree; main working tree must not be shared | Yes — declared in §6.1 branch-cut note; if a G2D CC session opens in parallel with G4 (possible, as G2D may begin once ADR-020 accepts), both sessions must allocate dedicated worktrees before any branch operations |

---

## EL Approval Record

*EL reviews this entry document before any implementation PR opens. Approval is recorded here
or as a comment on the exit checklist issue #1535.*

**EL approval:** Approved — 2026-07-03

> G4 sprint entry approved. Coordination gate with G3 #1537 confirmed cleared. Sprint branch
> `sprint/m19-g4` cut from `release/m19` (post #1617 merge). Sprint journal issue opened.
> Intent documents and QA tests to be filed before implementation PRs open. NM-087/NM-088
> process requirements active for this sprint.
> — @PublicEnemage (2026-07-03)
