# WorldSim Session State — Cockpit Card

> **Protocol:** This file is the program-level cockpit card for the current milestone.
> It must remain ≤ 200 lines — enforced by CI (`session-state-size-check` job).
> Intra-sprint status lives in each group's sprint journal issue (see §Cockpit below).
> Historical state lives in `docs/process/session-archives/`.
> Authority: `docs/process/sprint-group-isolation.md §SESSION_STATE.md Cockpit Card Protocol`.

**Last updated:** 2026-07-02 (pre-wave in flight — #1456 PR #1558 + #1538 PR #1559 open auto-merge; #1532 scoped (ARCH-014 filed PENDING_NUMBER, Iceland stays blocked); Architect deliberation on constraint-floor search: new ADR-021 required (ARCH-015 ASSIGNED), not ADR-019 amendment — awaiting EL confirmation; next action: EL confirms ADR-021 gate, then Architect authors ADR-021, then G1 sprint entry)
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
| Active wave | Pre-wave — #1456 PR #1558 ✓, #1538 PR #1559 ✓, #1532 scoped; ADR-021 gate pending EL |
| Active sprint groups | None |
| Active sprint journal issues | None |

---

## Open EL Decisions

| Decision | Status |
|---|---|
| ADR-021 gate: confirm Architect recommendation — new ADR-021 for constraint-floor search (not ADR-019 amendment) | Architect deliberation filed 2026-07-02; awaiting EL confirmation. Once confirmed, Architect authors ADR-021; G1 sprint entry blocked until ADR-021 accepted. |
| ARCH-014 scope: capital controls full fix M19 or defer to M20? | Pre-wave assessment complete: full fix requires ADR (ARCH-014 PENDING_NUMBER). Iceland (#1553) stays blocked. EL decision needed on whether to scope ADR authorship in M19 Wave 2 or defer to M20. |

---

## M19 Open Issues (22 total)

| Issue | Title | Group | Priority |
|---|---|---|---|
| #1535 | M19 Exit Checklist | — (gate) | Milestone exit gate |
| #1544 | Demo 8 — live stakeholder session | — (exit gate) | Primary deliverable |
| #1532 | Capital controls transmission gap | Pre-wave/known-gap | Immediate — blocks Iceland (#1553) |
| #1456 | MDAAlertPanel Zone1B: scenarioId crash | Pre-wave | Immediate — crash risk |
| #1538 | Focal cohort floor validation | Pre-wave | Immediate — #1540 prerequisite |
| #1540 | Mode 3 constraint-floor search | G1 Wave 1 | High — Demo 8 Act 1 |
| #1546 | Headless battle-testing harness | G2A Wave 1 | High — all scenario runs depend on this |
| #1541 | SEN backtesting fixture | G2B Wave 1 | High — Bayesian gate |
| #1542 | ZMB backtesting fixture | G2B Wave 1 | High — Bayesian gate |
| #1547 | Greece 2010–15 counter-factual Type B | G2C Wave 1–2 | Medium |
| #1548 | Argentina 2001 counter-factual Type B | G2C Wave 1–2 | Medium |
| #1549 | Sri Lanka 2022–23 Type A+B | G2C Wave 1–2 | Medium |
| #1550 | Pakistan 2022–23 Type B | G2C Wave 1–2 | Medium |
| #1551 | Turkey 2018–19 Type B | G2C Wave 1–2 | Medium |
| #1552 | Egypt 2016 Type B | G2C Wave 1–2 | Medium |
| #1554 | Ghana 2022–23 Type A+B | G2C Wave 1–2 | Medium |
| #1553 | Iceland 2008–11 Type A+B | G2D Wave 2 | Medium — blocked: #1532 |
| #1543 | ADR-007 Bayesian posterior layer | G3 Wave 2 | High — Demo 8 Act 2 CI |
| #1536 | ADR-007 meaninglessness threshold | G3 Wave 2 | High — coord #1543 |
| #1537 | BandResult visible fields | G3 Wave 2 | High — posterior UX prereq |
| #1528 | PSP driver arc + auditability panel (DEMO-165) | G4 Wave 2–3 | High |
| #1529 | '95% CI' label precision fix | G4 Wave 2–3 | High — coord G3 |

---

## Carry-Forward Context

- **Process model (M19 onward):** Sprint group isolation (Option E hybrid) + SESSION_STATE.md cockpit card (≤ 200 lines). Full protocol: `docs/process/sprint-group-isolation.md`. Shared state via `chore/m{N}-state-sync-NNN` → `release/m{N}` (PM Agent). Auto-merge: `gh pr merge --auto`.
- **Pre-push hook:** `.githooks/pre-push` enforces ruff + mypy (backend) and `npm run build` (frontend). Install: `git config core.hooksPath .githooks`.
- **GA-02 / Path 2 retirement (PR #1393):** Proprietary ministry data upload retired on open-source-as-strategy principle. No implementation without EL-approved governance exception.
- **sprint-branch-ci-gate Ruleset:** Node ID `RRS_lACqUmVwb3NpdG9yec5IKi2kzgEV92A`. Requires `changes`, `lint`, `test-backend`, `compliance-scan`. (playwright-e2e not required — NM-076 context.)
- **NM-075:** git worktrees must be allocated per sprint group (`git worktree add /tmp/<name> <branch>`) to prevent branch switches overwriting in-progress work.
- **NM-076:** Before any testid rename, grep the full E2E corpus for the old testid; update E2E tests in the same PR. Rule in CODING_STANDARDS.md (PR #1439).
- **M18 complete (v0.18.0, 2026-07-02):** G1–G7 delivered; Demo 7 PASS (unconditional); release/m18 → main via PR #1534. Archive: `docs/process/session-archives/session-state-pre-m19.md`.
- **Demo 7 north star (2026-07-02):** Aicha presents Zambia +342K cohort effect with CI bounds and sourcing to IMF restructuring table. Next available DEMO-167.
- **Socratic TEST gaps (M19 scope):** #1536 (meaninglessness threshold), #1537 (BandResult visible fields), #1538 (focal cohort floor validation) — all filed 2026-07-02, assigned M19.
