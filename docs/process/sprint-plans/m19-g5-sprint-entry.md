---
name: m19-g5-sprint-entry
type: sprint-entry
milestone: M19 — Constraint Search and Empirical Calibration
sprint-group: G5 — Demo 8 display fidelity + Zone 1 view model
status: Filed
authored-by: PM Agent
authored-date: 2026-07-03
el-approved: false
release-branch: release/m19
sop-reference: docs/process/sprint-planning-sop.md
---

# Sprint Entry — M19, G5: Demo 8 Display Fidelity + Zone 1 View Model

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
| Sprint number | 6 (G5 — Wave 3) |
| Release branch | `release/m19` |
| Sprint plan document | `docs/process/sprint-plans/m19-sprint-plan.md` |
| Exit checklist issue | #1535 |
| Sprint groups in scope | G5 |
| Wave coordination tier | Standard (G4 integration PR #1637 merged to `release/m19`; G5 is sole active implementation group at entry) |
| Concurrent groups at entry | 1 (G5 only; #1657 DemographicModule fix deferred — no implementation PR open; CM Sprint A #1623 runs on a separate CM-managed branch and does not overlap G5 file areas) |
| Cross-group dependencies | G4 integration PR #1637 merged to `release/m19` (2026-07-03) — CLEARED. G2D integration PR #1641 `sprint/m19-g2 → release/m19` pending auto-merge (no file-area overlap with G5). |

---

## Section 2 — Entry Invariants Checklist

*All items must be checked before any implementation PR is opened for this sprint.
An unchecked invariant blocks the sprint from opening.*

### 2.1 — Structural gates

- [x] **Release branch exists:** `release/m19` cut from `main` 2026-07-02 at 1bf1ecc
- [x] **CI trigger verified:** `.github/workflows/ci.yml` `pull_request: branches` includes `release/m*` (verified at M19 kickoff; sprint-branch-ci-gate Ruleset active)
- [x] **Sprint plan EL-approved:** `docs/process/sprint-plans/m19-sprint-plan.md` — EL-approved 2026-07-02

### 2.2 — ADR prerequisite gate

*G5 contains one ADR-gated deliverable: #1630 (Option 2 — per-framework lines in Mode 3 Zone 1A). This change modifies what CompositeChartSVG renders in Mode 3, which is a Tier 1 UX change to the primary instrument viewport. Architect + UX Designer must determine at the UX panel review whether this requires a new ADR or an amendment to an existing ADR (candidates: ADR-007 §trajectory display contract; ADR-019 §Zone 1A Mode 3 scope) before the intent document for #1630 can be filed.*

*#1629, #1632, #1522, and #1524 have no ADR prerequisites (see §4).*

- [ ] **#1630 ADR determination complete** — Architect + UX Designer panel to determine ADR requirement; gate BLOCKED_UX_PANEL until UX panel review concludes. If ADR required, it must be accepted before the #1630 implementation PR opens.
- [x] **All other groups** — CLEAR: no BLOCKED_ADR conditions for #1629, #1632, #1522, #1524

**ADR prerequisite status:**

| Group | Required ADR | ADR status | Gate |
|---|---|---|---|
| #1629 — ZMB Zone 1A y-axis tight-scoping | N/A — `computeYDomain` fix within existing ADR-007 display contract | N/A | CLEAR |
| #1630 — Per-framework lines in Mode 3 Zone 1A (EL Option 2) | TBD — Architect + UX Designer determine at panel review | BLOCKED_UX_PANEL | **BLOCKED_UX_PANEL** — implementation PR must not open until panel review complete and (if required) ADR accepted |
| #1632 — api_contracts.yml band_method schema gap | N/A — schema correction only; no architectural change | N/A | CLEAR |
| #1522 — View model layer retrofit (capacity-conditional) | N/A — code architecture refactor; no user-visible design decision | N/A | CLEAR (if capacity permits) |
| #1524 — Zone 1A TrajectoryView interaction layer (capacity-conditional) | N/A — interaction gesture layer within existing Zone 1A viewport contract | N/A | CLEAR (if capacity permits) |

### 2.3 — Intent document gate

*User-facing deliverables require intent documents filed before implementation PRs open.
Infrastructure deliverables (NM codification, schema fixes) are exempt per `docs/process/sprint-planning-sop.md §Infrastructure Sprint Exception`.*

- [ ] Intent document filed for #1629 — to be filed after EL approves this entry
- [ ] Intent document filed for #1630 — **BLOCKED_UX_PANEL**: intent document may not be filed until UX panel review is complete and ADR determination is recorded
- [ ] Intent document filed for #1524 — to be filed if capacity confirmed after Demo 8 display work; may defer to M20
- [ ] Intent document filed for #1522 — to be filed if capacity confirmed; may defer to M20

**Intent document status:**

| Deliverable | ADR reference | Intent document path | Filed? |
|---|---|---|---|
| ZMB Zone 1A y-axis tight-scoping (#1629) | ADR-007 (CI band display contract; `computeYDomain` is within Zone 1A display contract) | `docs/process/intents/M19-G5-2026-07-03-zmb-yaxis-tight-scoping.md` | Pending — to be filed after EL entry approval |
| Per-framework lines in Mode 3 (#1630, Option 2) | TBD at UX panel review | `docs/process/intents/M19-G5-YYYY-MM-DD-mode3-per-framework-lines.md` | **BLOCKED_UX_PANEL** — requires UX panel review + ADR determination first |
| Zone 1A interaction layer (#1524) | ADR-019 scope check required at intent authorship | `docs/process/intents/M19-G5-YYYY-MM-DD-zone1a-interaction.md` | Conditional — filed if capacity confirmed |
| View model layer retrofit (#1522) | N/A — code architecture | `docs/process/intents/M19-G5-YYYY-MM-DD-view-model-retrofit.md` | Conditional — filed if capacity confirmed |

*#1632 (api_contracts.yml schema fix) is an infrastructure deliverable — no intent document required. NM codification (#1650–#1656, PR #1658) was an infrastructure sprint — already delivered.*

### 2.4 — QA test authorship gate

*QA tests must be authored from the intent document's acceptance criteria before implementation
code is written. Gate follows from the intent document gate above.*

- [ ] QA test file authored for #1629 — to be filed with or before the implementation PR
- [ ] QA test file authored for #1630 — **BLOCKED_UX_PANEL**: same gate as intent document; no test authorship until panel review complete
- [ ] QA test file authored for #1524 — conditional on capacity confirmation
- [ ] QA test file authored for #1522 — conditional on capacity confirmation

**QA test status:**

| Deliverable | Intent document | Test file path | Authored before implementation? |
|---|---|---|---|
| ZMB Zone 1A y-axis tight-scoping (#1629) | `docs/process/intents/M19-G5-…-zmb-yaxis-tight-scoping.md` | `frontend/tests/e2e/m19-g5-zmb-yaxis-tight-scoping.spec.ts` | Pending — after intent document filed |
| Per-framework lines in Mode 3 (#1630) | Blocked — see §2.3 | `frontend/tests/e2e/m19-g5-mode3-per-framework-lines.spec.ts` | **BLOCKED_UX_PANEL** |
| Zone 1A interaction (#1524) | Conditional | `frontend/tests/e2e/m19-g5-zone1a-interaction.spec.ts` | Conditional |
| View model retrofit (#1522) | Conditional | `backend/tests/test_m19_g5_view_model_retrofit.py` or equivalent | Conditional |

*NM-086 process requirement: QA Lead must verify any E2E mock routes added for #1629 or #1524
against `api_contracts.yml` before the intent document is approved. This is a blocking checklist
item on the test authorship gate for those deliverables.*

---

## Section 3 — Scope Declaration

### 3.0 — Scope lock confirmation (NM-081; sprint-planning-sop.md §Scope lock precondition)

*#1630 represents an open scope decision that has been resolved at sprint entry: EL selected
Option 2 (per-framework lines in Mode 3 Zone 1A) on 2026-07-03. The ADR determination for
Option 2 is delegated to the UX panel review (Architect + UX Designer). Scope for #1629,
#1632, #1522, and #1524 is fully locked.*

- [x] All ADR decisions affecting locked scope are EL-approved and merged to `release/m19`

**Scope uncertainty:** #1630 (EL selected Option 2 — RESOLVED). ADR determination pending at
UX panel review (whether amendment to ADR-007/ADR-019 or new ADR is required). This
determination does not change the scope decision — Option 2 is confirmed — but may add an
ADR acceptance gate before the implementation PR for #1630 can open.

### 3.1 — Issues in scope

**Phase A — NM process codification (COMPLETE)**

| Issue | Title | Group | Priority | Status |
|---|---|---|---|---|
| #1650 | NM-086: E2E mock helper authorship rule — CODING_STANDARDS.md | G5 Phase A | Process | PR #1658 MERGED (sprint/m19-g5) |
| #1651 | NM-084: CM sign-off pre-PR-open gate — sprint-planning-sop.md | G5 Phase A | Process | PR #1658 MERGED (sprint/m19-g5) |
| #1652 | NM-085: co-dependent fixture CI ordering rule — sprint-planning-sop.md | G5 Phase A | Process | PR #1658 MERGED (sprint/m19-g5) |
| #1653 | NM-092: worktree setup symlink checklist — sprint-group-isolation.md | G5 Phase A | Process | PR #1658 MERGED (sprint/m19-g5) |
| #1654 | NM-089: shared-state commit gate — sprint-group-isolation.md | G5 Phase A | Process | PR #1658 MERGED (sprint/m19-g5) |
| #1655 | NM-093: bidirectional lane rule — sprint-group-isolation.md | G5 Phase A | Process | PR #1658 MERGED (sprint/m19-g5) |
| #1656 | NM-094: PI Agent test-file presence check — sprint-group-isolation.md | G5 Phase A | Process | PR #1658 MERGED (sprint/m19-g5) |

**Phase B — Demo 8 display fidelity and schema gap**

| Issue | Title | Group | Priority |
|---|---|---|---|
| #1629 | Zone 1A ZMB y-axis not tight-scoped — curves collapse | G5 Phase B | High — Demo 8 Act 2 display fidelity |
| #1630 | Demo 8 Act 1 narration: add per-framework lines to Mode 3 Zone 1A (EL: Option 2) | G5 Phase B | High — Demo 8 Act 1 credibility; BLOCKED_UX_PANEL at entry |
| #1632 | api_contracts.yml §trajectory missing band_method/is_meaningless/suppressed_reason | G5 Phase B | Low — schema-only fix; non-blocking; G4 forward condition |

**Phase C — Zone 1 view model (capacity-conditional; defer to M20 if Demo 8 prep consumes capacity)**

| Issue | Title | Group | Priority |
|---|---|---|---|
| #1522 | View model layer retrofit — Zone 1 composition logic extraction | G5 Phase C | Medium — capacity-conditional |
| #1524 | Zone 1A TrajectoryView: pinch-zoom, thumbwheel zoom, pan | G5 Phase C | Medium — capacity-conditional |

**Parallel track — NOT on sprint/m19-g5 (CM-managed branch)**

| Issue | Title | Notes |
|---|---|---|
| #1623 | ELASTICITY_REGISTRY — non-SSA calibration (CM Sprint A: GRC/Euro area) | CM Sprint A; separate branch; NM-084 CM sign-off gate applies before any CM fixture PR merges |

### 3.2 — Issues explicitly out of scope

| Issue | Title | Horizon | Rationale for exclusion |
|---|---|---|---|
| #1657 | NM-090/091: DemographicModule dead event subscriptions + missing elasticity rows | Deferred | CM sign-off required before implementation PR opens; CM gate not yet cleared; separate PR when gate clears |
| #1544 | Demo 8 — live stakeholder session | Wave 3 (exit gate) | Post-G5 deliverable; milestone exit gate |
| #1535 | M19 Exit Checklist | Gate issue | Milestone exit gate — not an implementation deliverable |
| #1456 | MDAAlertPanel Zone1B: scenarioId crash | Pre-wave (standalone) | Addressed pre-wave |
| #1538 | Focal cohort floor validation | Pre-wave (standalone) | G1 prerequisite — delivered pre-wave |

---

## Section 4 — ADR Prerequisite Summary

| Group | ADR required | ADR status | Implementation may begin? |
|---|---|---|---|
| #1629 — ZMB y-axis fix | None — `computeYDomain` fix is within ADR-007 Zone 1A display contract; no new design decision | N/A | Yes — after EL approves entry and intent document is filed |
| #1630 — per-framework lines in Mode 3 (Option 2) | TBD — Architect + UX Designer to determine at panel review | BLOCKED_UX_PANEL | **No — UX panel review must conclude; ADR determination (amendment or new ADR) must be on record before implementation PR opens** |
| #1632 — api_contracts.yml schema gap | None — schema correction; no architectural change | N/A | Yes — no intent document or test required (infrastructure fix) |
| #1522 — view model retrofit | None — code architecture refactor | N/A | Yes — after EL approves entry and intent document is filed (if capacity confirmed) |
| #1524 — Zone 1A interaction | None — interaction gesture layer | N/A | Yes — after EL approves entry and intent document is filed (if capacity confirmed) |

---

## Section 5 — Near-Miss Sweep

**Near-miss sweep date:** 2026-07-03
**Sweep period:** Since G4 sprint entry (2026-07-03)

| Finding | Category | PI Agent register call issued? | NM entry number |
|---|---|---|---|
| CM sign-off ordering gap (G2B) — no process gate required CM sign-off before fixture PR merged | Near-miss | Yes — PR #1658 | NM-084 |
| Co-dependent fixture CI sequencing — no SOP rule on ordering when two fixtures in same sprint | Near-miss | Yes — PR #1658 | NM-085 |
| E2E mock routes not verified against api_contracts.yml before implementation PR opened (G1) | Near-miss | Yes — PR #1658 | NM-086 |
| git stash --include-untracked used as recovery action without EL authorization (G2C context) | Near-miss | Yes — filed 2026-07-02 | NM-087 |
| Parallel CC sessions sharing main working tree — branch displacement caused lost files | Near-miss | Yes — filed 2026-07-03 | NM-088 |
| Shared-state commit gate — shared files not committed before branch switch | Near-miss | Yes — PR #1658 | NM-089 |
| DemographicModule dead event subscriptions (wrong event string; elasticity entries never trigger) | Near-miss | Yes — Issue #1657 filed; NM-090 | NM-090 |
| DemographicModule missing elasticity rows for two subscribed events | Near-miss | Yes — Issue #1657 filed; NM-091 | NM-091 |
| Worktree allocated without symlink setup — venv absent inside worktree causing silent failures | Near-miss | Yes — PR #1658 | NM-092 |
| State-sync branch contained code changes as well as shared-state files (bidirectional lane violation) | Near-miss | Yes — PR #1658 | NM-093 |
| Integration PR opened without PI Agent test-file presence check — test file missing from sprint branch | Near-miss | Yes — PR #1658 | NM-094 |

*NM-084 through NM-094 were codified in PR #1658 (merged to sprint/m19-g5 2026-07-03). All
applicable process improvements are now in the process docs and sprint isolation protocol.*

---

## Section 6 — Sprint Group Isolation (M18 onward)

*Required for every sprint group under the sprint group isolation protocol.
Authority: `docs/process/sprint-group-isolation.md`.*

### 6.1 — Sprint sub-branch

| Field | Value |
|---|---|
| Sprint sub-branch | `sprint/m19-g5` |
| Cut from | `release/m19` |
| Sprint journal issue | #1660 |

*`sprint/m19-g5` was cut from `release/m19` at milestone kickoff and is 2 commits ahead as
of this sprint entry: PR #1658 (NM codification) is already merged. The branch is ready for
Phase B implementation.*

**NM-087/NM-088 compliance note:** Any agent beginning work on a feature branch from
`sprint/m19-g5` must:
1. Run `git status --porcelain` before any checkout — stop and report if dirty
2. If another CC session is simultaneously active on this repository, allocate a dedicated
   git worktree before any branch operations (`git worktree add /tmp/m19-g5-<task> sprint/m19-g5`)
3. Follow worktree symlink setup from `docs/process/sprint-group-isolation.md §Worktree Setup`

### 6.2 — File-conflict risk assessment

| File | Lane required | Trigger |
|---|---|---|
| `SESSION_STATE.md` | PM Agent coordination lane | Sprint exit cockpit update |
| `docs/process/near-miss-registry.md` | PM Agent coordination lane (PI Agent authors) | If NM identified during sprint |
| `docs/compliance/scan-registry.md` | PM Agent coordination lane | If compliance scan produced at sprint exit |
| `frontend/src/components/CompositeChartSVG.tsx` | Sprint sub-branch | Primary implementation file for #1629 and #1630 |
| `frontend/tests/e2e/demo-narrated.spec.ts` | Sprint sub-branch | Narration update for #1630 (per-framework lines) |
| `docs/schema/api_contracts.yml` | Sprint sub-branch | Schema gap fix for #1632 |
| `frontend/src/components/TrajectoryView.tsx` | Sprint sub-branch | Zone 1A interaction layer for #1524 |
| `frontend/src/` (Zone 1 component tree) | Sprint sub-branch | View model retrofit for #1522 |
| `frontend/tests/e2e/m19-g5-*.spec.ts` | Sprint sub-branch | QA test files for all deliverables |
| `docs/process/intents/M19-G5-*.md` | Sprint sub-branch | Intent documents |

**No file-area overlap with G2D (`sprint/m19-g2`):** G2D touches backend simulation and
backtesting fixtures only. G5 is primarily frontend (`CompositeChartSVG`, `TrajectoryView`)
plus `api_contracts.yml`. Risk: None.

**No file-area overlap with CM Sprint A (#1623):** CM Sprint A touches `backend/app/simulation/demographic_module.py` (ELASTICITY_REGISTRY). G5's frontend scope does not overlap. Risk: None.

### 6.3 — Infrastructure dependency declaration

- [x] No DS-owned file changes required

No changes to `.github/workflows/`, `.githooks/`, or `.gitignore` are anticipated. G5
introduces no new backend modules and no new output directories.

#### 6.3a — New output paths declaration (NM-069)

- [x] No new output directories — all generated paths are already covered by `.gitignore`

### 6.4 — Cross-group dependency declaration

- [x] G4 dependency CLEARED — integration PR #1637 merged to `release/m19` (2026-07-03)

**G5 cross-group dependencies:**

1. **G4 → G5 (#1629/#1630):** G4 changes to `TrajectoryView.tsx` (CI label in G4 #1529) and
   Zone 1D must be stable before G5 modifies `CompositeChartSVG.tsx`. Status: CLEARED — G4
   integration PR #1637 merged to `release/m19`. G5 sprint branch inherits G4 changes.

2. **G2D (#1641) → G5:** G2D integration PR #1641 targets `release/m19` and touches backend
   simulation files only — no overlap with G5 frontend scope. G5 may begin implementation
   before #1641 merges. Status: No dependency.

### 6.5 — Prior NM verification (NM-068 process improvement)

**NM verification sweep date:** 2026-07-03
**Sweep period:** Since G4 sprint entry (2026-07-03)

| NM entry | Process improvement required | Applied in this sprint? |
|---|---|---|
| NM-084 | CM sign-off on fixture/calibration PRs must precede auto-merge; PI Agent posts gate comment before implementing agent sets auto-merge | N/A for G5 core (#1629, #1630, #1632, #1522, #1524 are not fixture PRs). Applies to CM Sprint A (#1623) — codified in `sprint-planning-sop.md §Pre-Merge CM Review` (PR #1658) |
| NM-085 | Sprint entry §6.2 must document co-dependent fixture CI sequencing risk | N/A — G5 has no co-dependent fixture pairs |
| NM-086 | QA Lead must verify E2E mock routes against `api_contracts.yml` before intent document is approved | Yes — declared in §2.4 as blocking checklist item for #1629 and #1524 |
| NM-087 | Pre-checkout dirty-tree guard: `git status --porcelain` before any branch operation | Yes — declared in §6.1 compliance note |
| NM-088 | Parallel CC session worktree requirement | Yes — declared in §6.1 compliance note |
| NM-089 | Shared-state commit gate before branch switch | Yes — `docs/process/sprint-group-isolation.md §Commit gate` (PR #1658); applies at any state-file write during sprint |
| NM-090 | DemographicModule dead subscriptions fix (wrong event string) | N/A for G5 scope; deferred to separate PR (#1657) — CM gate required first |
| NM-091 | DemographicModule missing elasticity rows for imf_program_acceptance + programme_window_close | N/A for G5 scope; deferred to separate PR (#1657) — CM gate required first |
| NM-092 | Worktree setup symlink checklist | Yes — declared in §6.1 compliance note; implementing agent must follow `sprint-group-isolation.md §Worktree Setup` |
| NM-093 | Bidirectional lane rule — state-sync branches may contain ONLY shared-state files | Yes — applies to any PM Agent state-sync PRs opened during G5; pre-open diff check required |
| NM-094 | PI Agent test-file presence check before integration PR | Yes — applies at G5 integration PR; PI Agent must run `git diff release/m19...sprint/m19-g5 | grep -E "test_|\.spec\.ts"` before opening integration PR |

---

## UX Panel Gate — #1630 Option 2

*This gate is required before the intent document for #1630 may be filed.*

**Trigger:** EL selected Option 2 (add per-framework lines to Mode 3 Zone 1A) on 2026-07-03.
Per CLAUDE.md §UX Architectural Commitments, any UX proposal affecting the primary viewport
instrument in Mode 3 requires UX Designer sign-off. CompositeChartSVG currently renders a
single composite line; adding four per-framework lines (HD, FIN, GOV, ECO) changes the Zone 1A
visual contract for Mode 3 stakeholders.

**Panel composition required:**
- Architect Agent (R — ADR determination; if amendment required, authors the ADR)
- UX Designer Agent (R — sign-off; separate EL-triggered session per NM-042)
- Design Thinking Agent (C — cognitive task impact: does the 4-line render support Mode 3 "active control" cognitive task or increase visual noise?)
- Frontend Architect (C — technical feasibility; line rendering in CompositeChartSVG)
- Business PO (C — Demo 8 Act 1 stakeholder legibility)

**Panel output required:**
1. ADR determination: (a) amendment to existing ADR (ADR-007 §trajectory display contract or ADR-019 §Zone 1A Mode 3 scope), (b) new ADR, or (c) no ADR required (Tier 2 design decision)
2. UX Designer attestation (NM-042 compliant — named fields: reviewing agent, session context, governing documents reviewed with named sections, concerns found count)
3. If new/amended ADR: ADR accepted before #1630 implementation PR opens

**EL activation required:**
`Architect: CHALLENGE — Does per-framework lines in Mode 3 CompositeChartSVG (#1630 Option 2) require an ADR amendment or new ADR? Panel: Architect (R), UX Designer (separate session), Design Thinking (C), Frontend Architect (C), Business PO (C).`

---

## EL Approval Record

*EL reviews this entry document before any implementation PR opens. Approval is recorded here
or as a comment on the exit checklist issue #1535.*

**EL approval:** Approved — 2026-07-03

> G5 sprint entry approved. EL decision for #1630 confirmed: Option 2 (per-framework lines
> in Mode 3 Zone 1A). UX panel gate activated immediately — Architect + UX Designer panel
> to run concurrently with Phase B #1629/#1632 implementation work. Phase B implementation
> PRs for #1629 and #1632 may open now. #1630 implementation PR remains BLOCKED_UX_PANEL
> until panel review concludes and ADR determination is on record.
> — @PublicEnemage (2026-07-03)
