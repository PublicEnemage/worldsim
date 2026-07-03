# WorldSim Session State — Cockpit Card

> **Protocol:** This file is the program-level cockpit card for the current milestone.
> It must remain ≤ 200 lines — enforced by CI (`session-state-size-check` job).
> Intra-sprint status lives in each group's sprint journal issue (see §Cockpit below).
> Historical state lives in `docs/process/session-archives/`.
> Authority: `docs/process/sprint-group-isolation.md §SESSION_STATE.md Cockpit Card Protocol`.

**Last updated:** 2026-07-03 (G2C confirmed — 7-country battle-testing suite complete; G2D next: ADR-020 required before entry; G3 BLOCKED_ADR on ARCH-016)
**Current milestone:** M19 — Constraint Search and Empirical Calibration

---

## Cockpit

| Field | Value |
|---|---|
| Milestone | M19 — Constraint Search and Empirical Calibration |
| GitHub Milestone | #21 — created 2026-07-02 |
| Exit checklist issue | #1535 (M19 Exit Checklist — blocks milestone closure) |
| Release branch | `release/m19` — cut from `main` 2026-07-02 at 1bf1ecc |
| Sprint plan | `docs/process/sprint-plans/m19-sprint-plan.md` — EL-approved 2026-07-02 |
| Active wave | Wave 2 — G2C confirmed; G2D pending ADR-020; G3 BLOCKED_ADR (ARCH-016); G4 next |
| Active sprint groups | G3 — BLOCKED_ADR (ADR-007 amendment ARCH-016); G2D — pre-gate (ADR-020 required) |
| Active sprint journal issues | None active — G2C journal #1589 closed 2026-07-03 |

---

## Open EL Decisions

| Decision | Status |
|---|---|
| ARCH-014 scope: capital controls full fix M19 or defer to M20? | RESOLVED 2026-07-03 — G2D stays in M19. ADR-020 authorship (ARCH-014 number assigned) required before G2D sprint entry. Architect Agent must be activated. |

---

## Wave 1 Sprint Status

| Group | Sprint | Issues | Exit status |
|---|---|---|---|
| G1 | Mode 3 constraint-floor search | #1540 ✓, #1563 ✓, #1564 ✓ | Confirmed — integrated to release/m19 (PR #1582, 2026-07-03) |
| G2A | Headless battle-testing harness | #1546 ✓ | Confirmed — PI confirm retroactively filed PR #1580/#1583 |
| G2B | SEN + ZMB backtesting fixtures | #1541 ✓, #1542 ✓ | Confirmed — exit doc PR #1578 |

## Wave 2 Sprint Status

| Group | Sprint | Issues | Exit status |
|---|---|---|---|
| G2C | Battle-testing scenario runs | #1547 ✓, #1548 ✓, #1549 ✓, #1550 ✓, #1551 ✓, #1552 ✓, #1554 ✓ | Confirmed 2026-07-03 — exit doc `m19-g2c-sprint-exit.md`; integration PR deferred to G2D exit |
| G2D | Iceland 2008–11 orthodox vs heterodox | #1553 | Pre-gate — ADR-020 required (Architect Agent) |
| G3 | ADR-007 Bayesian posterior + BandResult | #1543, #1536, #1537 | BLOCKED_ADR — awaiting ARCH-016 acceptance |
| G4 | PSP driver arc + CI label precision | #1528, #1529 | Not yet entered |

---

## M19 Open Issues (Wave 2+)

| Issue | Title | Group | Priority |
|---|---|---|---|
| #1535 | M19 Exit Checklist | — (gate) | Milestone exit gate |
| #1544 | Demo 8 — live stakeholder session | — (exit gate) | Primary deliverable |
| #1532 | Capital controls transmission gap | Pre-wave/known-gap | Immediate — blocks Iceland (#1553) |
| #1456 | MDAAlertPanel Zone1B: scenarioId crash | Pre-wave | Immediate — crash risk |
| #1538 | Focal cohort floor validation | Pre-wave | Immediate — #1540 prerequisite |
| #1553 | Iceland 2008–11 Type A+B | G2D Wave 2 | Medium — blocked pending ADR-020 acceptance |
| #1543 | ADR-007 Bayesian posterior layer | G3 Wave 2 | High — Demo 8 Act 2 CI; BLOCKED_ADR (ARCH-016) |
| #1536 | ADR-007 meaninglessness threshold | G3 Wave 2 | High — coord #1543 |
| #1537 | BandResult visible fields | G3 Wave 2 | High — posterior UX prereq |
| #1528 | PSP driver arc + auditability panel (DEMO-165) | G4 Wave 2–3 | High |
| #1529 | '95% CI' label precision fix | G4 Wave 2–3 | High — coord G3 |

---

## Demo 8 Open Conditions (tracked from sprint exits)

| Condition | Source | Blocking |
|---|---|---|
| Tolerance band (±0.01) visible in FOUND state UI | Customer Agent L3 on #1540 | Demo 8 Act 1 |
| AC-12: resolve structural-absence indicator key (replace `__structural_absence__` placeholder) | Customer Agent L3 on #1540 | Demo 8 Act 1 |

---

## Carry-Forward Context

- **Process model (M19 onward):** Sprint group isolation (Option E hybrid) + SESSION_STATE.md cockpit card (≤ 200 lines). Full protocol: `docs/process/sprint-group-isolation.md`. Shared state via `chore/m{N}-state-sync-NNN` → `release/m{N}` (PM Agent). Auto-merge: `gh pr merge --auto`.
- **Pre-push hook:** `.githooks/pre-push` enforces ruff + mypy (backend) and `npm run build` (frontend). Install: `git config core.hooksPath .githooks`.
- **GA-02 / Path 2 retirement (PR #1393):** Proprietary ministry data upload retired on open-source-as-strategy principle. No implementation without EL-approved governance exception.
- **sprint-branch-ci-gate Ruleset:** Node ID `RRS_lACqUmVwb3NpdG9yecc5IKi2kzgEV92A`. Requires `changes`, `lint`, `test-backend`, `compliance-scan`. (playwright-e2e not required — NM-076 context.)
- **NM-075:** git worktrees must be allocated per sprint group (`git worktree add /tmp/<name> <branch>`) to prevent branch switches overwriting in-progress work.
- **NM-076:** Before any testid rename, grep the full E2E corpus for the old testid; update E2E tests in the same PR. Rule in CODING_STANDARDS.md (PR #1439).
- **ARCH-016:** ADR-007 amendment — Bayesian posterior layer (Section 8, new) + meaninglessness threshold implementation (Section 6). G3 BLOCKED_ADR until accepted. Panel: CM (C), CE (C), UX Designer (C — is_pre_calibration display), EL (A). Backlog entry filed 2026-07-02.
- **NM-084/NM-085:** CM sign-off ordering gap + co-dependent fixture CI sequencing (G2B). SOP improvements filed: §Pre-Merge CM Review Gate + §Co-Dependent Fixture Sprint Entry Requirements.
- **G2C complete (2026-07-03):** 7-country battle-testing suite on `sprint/m19-g2`; Business PO ACCEPT + Customer Agent L3 PASS at #1589; north star test artifact on record; integration PR deferred to G2D exit. Exit: `m19-g2c-sprint-exit.md`.
- **G2D pre-gate:** ADR-020 (ARCH-014 — capital controls economic transmission gap) must be authored and accepted before G2D sprint entry. Architect Agent activation is the next step. ADR number 020 reserved for this ADR.
- **NM-086:** E2E mock routes must be verified against `api_contracts.yml` before the implementation PR opens (G1, filed 2026-07-03). Process: QA Lead mock-helper verification is a blocking checklist item on intent authorship.
- **M18 complete (v0.18.0, 2026-07-02):** G1–G7 delivered; Demo 7 PASS (unconditional); release/m18 → main via PR #1534. Archive: `docs/process/session-archives/session-state-pre-m19.md`.
- **Demo 7 north star (2026-07-02):** Aicha presents Zambia +342K cohort effect with CI bounds and sourcing to IMF restructuring table. Next available DEMO-167.
- **Socratic TEST gaps (M19 scope):** #1536 (meaninglessness threshold), #1537 (BandResult visible fields), #1538 (focal cohort floor validation) — all filed 2026-07-02, assigned M19.
