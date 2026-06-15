---
name: m13-sprint-1-entry
type: sprint-entry
milestone: M13 — Political Economy and Instrument Credibility
sprint-group: G1, G2, G3, G4, G5, G6, G7 (all M13 groups)
status: Approved — implementation of Wave 1 groups may begin
authored-by: PM Agent
authored-date: 2026-06-12
el-approved: 2026-06-12
release-branch: release/m13
sop-reference: docs/process/sprint-planning-sop.md
---

# Sprint Entry — M13, Sprint 1

**Status:** Approved — Wave 1 implementation may begin
**Date authored:** 2026-06-12
**Release branch:** `release/m13`
**Sprint plan:** `docs/process/sprint-plans/m13-sprint-plan.md`

*Authority: `docs/process/sprint-planning-sop.md §Sprint Entry Gate` (Phase C output).
Changes to this template require PM Agent authorship and EL endorsement.*

---

## Section 1 — Sprint Identification

| Field | Value |
|---|---|
| Milestone | M13 — Political Economy and Instrument Credibility |
| GitHub Milestone | #9 |
| Sprint number | 1 (full-milestone sprint) |
| Release branch | `release/m13` |
| Sprint plan document | `docs/process/sprint-plans/m13-sprint-plan.md` |
| Exit checklist issue | #264 |
| Sprint groups in scope | G1, G2, G3, G4, G5, G6 (G7 blocked — alert panel ADR pending) |

---

## Section 2 — Entry Invariants Checklist

*All items must be checked before any implementation PR is opened for this sprint.
An unchecked invariant blocks the sprint from opening.*

### 2.1 — Structural gates

- [x] **Release branch exists:** `release/m13` cut from `main` at 2026-06-12
- [x] **CI trigger verified:** `.github/workflows/ci.yml` `pull_request: branches` includes
  `release/m*` — confirmed 2026-06-12 (pre-existing fix from NM-035)
- [x] **Sprint plan EL-approved:** `docs/process/sprint-plans/m13-sprint-plan.md` approved 2026-06-12

### 2.2 — ADR prerequisite gate

| Group | Required ADR | ADR status | Gate |
|---|---|---|---|
| G1 | None | N/A | CLEAR |
| G2 | None | N/A | CLEAR |
| G3 | None | N/A | CLEAR |
| G4 | None | N/A | CLEAR |
| G5 | ADR-013 (this IS the ADR) | ASSIGNED | CLEAR to author |
| G6 | ADR-013 | ASSIGNED — not yet accepted | **BLOCKED_ADR** |
| G7 | Alert panel ADR | PENDING_NUMBER | **BLOCKED_ADR** |

- [x] All groups with `BLOCKED_ADR` status are documented above with clear gate conditions.
  G1–G5 are clear to proceed once EL approves this entry document.
  G6 may not open its implementation PR until ADR-013 is accepted.
  G7 may not open any PR until the alert panel ADR is accepted.

### 2.3 — Intent document gate

Intent documents are filed per user-facing deliverable before each group's implementation
PR opens. They are not required at entry document filing — they are required before
implementation begins. Status below reflects kickoff state; each group must update this
section when intent documents are filed.

- [ ] Intent document filed for every user-facing deliverable in this sprint

| Deliverable | ADR reference | Intent document path | Filed? |
|---|---|---|---|
| G1 — DEMO legibility (#872, #874) | None — bug fix | `docs/process/intents/DEMO-060-061-YYYY-MM-DD-legibility.md` | No — must file before G1 PR opens |
| G2 — DEMO trajectory/Mode 3 (#871, #873, #875, #876) | None — bug fix | `docs/process/intents/DEMO-059-062-063-064-YYYY-MM-DD-trajectory.md` | No — must file before G2 PR opens |
| G3 — Reserves non-negativity (#799) | None — bug fix | `docs/process/intents/G3-YYYY-MM-DD-reserves-floor.md` | No — must file before G3 PR opens |
| G4 — Documentation (#27, #822, #847) | None | `docs/process/intents/G4-YYYY-MM-DD-documentation.md` | No — must file before G4 PR opens |
| G5 — ADR-013 (#792) | ADR-013 (being authored) | Infrastructure sprint exception — see Section 2.5 | N/A |
| G6 — Political economy (#392) | ADR-013 (required, not yet accepted) | `docs/process/intents/ADR-013-YYYY-MM-DD-political-economy.md` | No — must file after ADR-013 accepted, before G6 PR opens |
| G7 — Alert panel (#852) | Alert panel ADR (pending) | `docs/process/intents/alert-panel-ADR-NNN-YYYY-MM-DD.md` | No — BLOCKED_ADR |

### 2.4 — QA test authorship gate

QA tests are authored from intent document acceptance criteria before implementation begins,
per the Phase A execution lifecycle. Same timing rule as intent documents: before each
group's implementation PR opens, not at sprint entry time.

- [ ] QA test file authored for every user-facing deliverable in this sprint

| Deliverable | Intent document | Test file path | Authored before implementation? |
|---|---|---|---|
| G1 — DEMO legibility | (to be filed) | `frontend/tests/` — legibility Playwright spec | No — pending intent document |
| G2 — DEMO trajectory/Mode 3 | (to be filed) | `frontend/tests/` — trajectory display + Mode 3 spec | No — pending intent document |
| G3 — Reserves floor | (to be filed) | `backend/tests/` — non-negativity unit + regression | No — pending intent document |
| G4 — Documentation | (to be filed) | Business PO navigability check (not a test file) | No — pending intent document |
| G5 — ADR-013 | N/A | Infrastructure sprint exception | N/A |
| G6 — Political economy | (blocked on ADR-013) | `backend/tests/` + `frontend/tests/` | No — BLOCKED_ADR |
| G7 — Alert panel | (blocked on alert panel ADR) | `frontend/tests/` | No — BLOCKED_ADR |

### 2.5 — Infrastructure sprint exception declaration

G5 (ADR-013 authorship, #792) is an architecture document deliverable with no user-facing
runtime output. Intent document gate (condition 4) and QA test authorship gate (condition 5)
do not apply to G5. Business PO acceptance is not required at sprint exit for G5 — the
acceptance gate is ADR-013 status = ACCEPTED with EL sign-off on the ADR itself.

PI Agent note: if ADR-013 acceptance produces any user-visible change not captured by a
subsequent group's intent document, PI Agent files a near-miss retroactively.

---

## Section 3 — Scope Declaration

### 3.1 — Issues in scope

| Issue | Title | Group | Priority |
|---|---|---|---|
| #872 | fix(demo): DEMO-060 — CRITICAL FIN alert clipped | G1 | immediate |
| #874 | fix(demo): DEMO-061 — unreadable at presentation scale | G1 | immediate |
| #871 | fix(demo): DEMO-059 — PMM displays 1.00 at step 5 | G2 | immediate |
| #873 | fix(demo): DEMO-062 — Zone 1D entity divergence absent | G2 | immediate |
| #875 | fix(demo): DEMO-063 — no inline entity labels | G2 | immediate |
| #876 | fix(demo): DEMO-064 — Mode 3 no quantitative comparison | G2 | immediate |
| #799 | engine: reserves can go negative | G3 | near-term |
| #27 | docs: calibration basis | G4 | near-term |
| #822 | docs: ecological composite disclosure | G4 | near-term |
| #847 | ux: DEMO-046 Irreversible label | G4 | near-term |
| #792 | docs(adr): ADR-013 political economy boundary | G5 | immediate |
| #392 | arch(m11): political economy constraint modeling | G6 | near-term |
| #852 | ux: alert panel master-detail layout | G7 | near-term |

### 3.2 — Issues explicitly out of scope (Wave 1/2)

Deferred to near-term backlog; will be revisited at M13 midpoint HORIZON sweep.

| Issue | Title | Rationale |
|---|---|---|
| #22 | Uncertainty quantification | Major architectural scope; ADR required; M14 likely |
| #35 | Dynamic relationship weight updating | Significant engine change; ADR required |
| #45 | Human development indicator standards | Can fit mid-milestone; not Wave 1 prerequisite |
| #102 | Distributional scenario comparison | Architecture change + significant frontend |
| #271 | Reversibility classification | Depends on uncertainty quantification direction |
| #274 | 25-year human capital trajectory | M14 scope |
| #393 | Mode 1→2 step preservation | Low complexity; may fit between G2 and G6 waves |
| #394 | Multi-scenario comparison (>2) | Architecture change; ADR required |
| #823 | Ecological composite denominator fix | Methodological correctness; mid-milestone |
| #824 | MENA elasticity calibration | Engine calibration; mid-milestone |
| #837 | Configuration-driven demo scripts | Lowest user-value priority |

---

## Section 4 — ADR Prerequisite Summary

| Group | ADR required | ADR status | Implementation may begin? |
|---|---|---|---|
| G1 | None | N/A | Yes — after EL approves this entry doc |
| G2 | None | N/A | Yes — after EL approves this entry doc |
| G3 | None | N/A | Yes — after EL approves this entry doc |
| G4 | None | N/A | Yes — after EL approves this entry doc |
| G5 | ADR-013 (self) | ASSIGNED | Yes — authoring begins immediately |
| G6 | ADR-013 | ASSIGNED, not yet accepted | **No — awaiting ADR-013 acceptance** |
| G7 | Alert panel ADR | PENDING_NUMBER, no issue filed | **No — awaiting ADR authorship and acceptance** |

---

## Section 5 — Near-Miss Sweep

**Near-miss sweep date:** 2026-06-12
**Sweep period:** Since M12 close (2026-06-11)

| Finding | Category | PI Agent register call issued? | NM entry number |
|---|---|---|---|
| Alert panel ADR has no GitHub issue and no backlog entry — gates #852, which is on the M13 board as a named deliverable | scope-gap:untracked | Pending — PM Agent flags to PI Agent; PI Agent determines near-miss vs. known-issue classification | TBD |

**Scope gap detail:** The EL decision (2026-06-11) on #852 requires an ADR before
implementation. That ADR has no issue filed and no backlog entry at M13 kickoff. Actions
taken this session: (1) Flagged in sprint plan §HORIZON Sweep; (2) Backlog entry to be
added (PENDING_NUMBER) at kickoff commit. GitHub issue to be filed for the alert panel ADR.

---

## EL Approval Record

**EL approval:** Recorded 2026-06-12

*EL review checklist:*
- [x] Groupings are reasonable
- [x] Sequencing and wave assignments are correct
- [x] No scope items missing from the plan (verify against roadmap and CLAUDE.md)
- [x] Structural gates in Section 2.1 are satisfied

> Sprint plan and entry document approved. Wave 1 groups (G1–G5) may proceed immediately
> once intent documents are filed per the Phase A execution lifecycle. G6 is blocked on
> ADR-013 acceptance; G7 is blocked on alert panel ADR (#908) acceptance.
> — @PublicEnemage (2026-06-12)
