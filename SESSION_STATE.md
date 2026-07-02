# WorldSim Session State — Cockpit Card

> **Protocol:** This file is the program-level cockpit card for the current milestone.
> It must remain ≤ 200 lines — enforced by CI (`session-state-size-check` job).
> Intra-sprint status lives in each group's sprint journal issue (see §Cockpit below).
> Historical state lives in `docs/process/session-archives/`.
> Authority: `docs/process/sprint-group-isolation.md §SESSION_STATE.md Cockpit Card Protocol`.

**Last updated:** 2026-07-02 (M18 EXIT CEREMONY in progress — reference docs updated; Vitest 332/332 PASS; SCAN-028, Socratic Agent TEST, EL sign-off pending; M19 kickoff pending EL)
**Current milestone:** M19 — Constraint Search and Empirical Calibration

---

## Cockpit

| Field | Value |
|---|---|
| Milestone | M19 — Constraint Search and Empirical Calibration |
| GitHub Milestone | #21 — created 2026-07-02 |
| Exit checklist issue | TBD (M19) |
| Release branch | `release/m19` — to be cut at M19 kickoff |
| Sprint plan | Pending — M19 kickoff requires EL sign-off on M18 exit |
| Active wave | None — M18 complete; M19 kickoff pending EL |
| Active sprint groups | None |
| Active sprint journal issues | None |

---

## M18 Entry Blockers — All Resolved

All blockers resolved before `release/m18` was cut 2026-06-26. Full table in `docs/process/session-archives/session-state-pre-m19.md`.

---

## Open EL Decisions

**M18 exit ceremony — EL-gated items outstanding:**

| Item | Status |
|---|---|
| SCAN-028 — M18 exit compliance scan | Pending EL |
| Socratic Agent TEST session on M18 architecture | Pending EL |
| Admin bypass audit (M18 merges without required reviews) | Pending EL |
| EL architectural sign-off | Pending EL |
| M19 creation ceremony (milestone #20, `release/m19`, sprint plan) | Pending EL (after sign-off) |
| EL admin bypass: `release/m18` → `main` | Pending EL (after all above) |

---

## M19 Open Issues

| Issue | Title | Priority |
|---|---|---|
| #1340 | M18 Exit Checklist — EL-gated items pending | Gate issue |
| #1528 | PSP driver methodology disclosure panel (DEMO-165) | M19 scope |
| #1529 | '95% CI' label overstates precision on DistributionalComparisonSummary (DEMO-163) | M19 scope |
| #1456 | MDAAlertPanel Zone1B: scenarioId unguarded at line 1121 | M19 scope — undelivered M18 |

---

## Carry-Forward Context

- **Process model (M18 onward):** Sprint group isolation (Option E hybrid) + SESSION_STATE.md cockpit card (≤ 200 lines). Full protocol: `docs/process/sprint-group-isolation.md`. Shared state via `chore/m{N}-state-sync-NNN` → `release/m{N}` (PM Agent). Auto-merge: `gh pr merge --auto`; observe with `gh run watch`.
- **Pre-push hook:** `.githooks/pre-push` enforces ruff + mypy (backend) and `npm run build` (frontend). Install: `git config core.hooksPath .githooks`.
- **GA-02 / Path 2 retirement (PR #1393):** Proprietary ministry data upload retired on open-source-as-strategy principle. No implementation without EL-approved governance exception.
- **sprint-branch-ci-gate Ruleset:** Node ID `RRS_lACqUmVwb3NpdG9yec5IKi2kzgEV92A`. Requires `changes`, `lint`, `test-backend`, `compliance-scan`. (playwright-e2e not required — NM-076 context.)
- **NM-075:** git worktrees must be allocated per sprint group (`git worktree add /tmp/<name> <branch>`) to prevent branch switches overwriting in-progress work.
- **NM-076:** Before any testid rename, grep the full E2E corpus for the old testid; update E2E tests in the same PR. Rule in CODING_STANDARDS.md (PR #1439).
- **G1–G5 CLOSED (2026-06-28):** CI bands (#1254), PSP driver decomposition (#1255), counter-scenario comparison (#1349), control plane column ADR-019 (#1354), Zone 3 auditability panel (#1422). Integration PRs #1411/#1408/#1417/#1433/#1443 MERGED to release/m18.
- **G6 CLOSED (2026-07-01):** Demo 7 remediation — 7 CRITICAL + 9 HIGH findings from internal review resolved (PRs #1482–#1500). Sprint journal #1475 CLOSED. Integration PR #1500 MERGED to release/m18.
- **G7 CLOSED (2026-07-02):** Demo 7 QA-first — Clusters A–E test assertions green; all AC-A1/A2/B1-B5/C1-C5/D1-D5/E1-E7 pass. Sprint journal #1495 CLOSED. Integration PR #1526 MERGED to release/m18.
- **Demo 7 — PASS (unconditional) 2026-07-02:** Simulated stakeholder session (Lucas P1, Aicha P5, Andreas P3, Eleni P2). North star: PASS (unconditional) — Aicha can present Zambia +342K cohort effect with CI bounds and sourcing to IMF restructuring table. Artifact: `docs/demo/m18/reviews/2026-07-02-v0.18.0-stakeholder-review.md`. Issue #843 CLOSED. DEMO-161–DEMO-166 filed; next available DEMO-167.
- **M19 primary scope (carry-forward from Demo 7 findings):** Mode 3 constraint-floor search capability (Lucas + Aicha gap); SEN/ZMB backtesting; empirically grounded CI intervals (ADR-007 Bayesian posterior layer); PSP driver arc across programme window (#1528); CI label precision fix (#1529); scenarioId guard (#1456); walkthrough updates: DEMO-161 (CI band opacity), DEMO-164 (PSP driver terminal step narration), DEMO-165 (PSP driver arc). Demo 8 at M19 close.
- **M18 archive:** Full M1–M18 session state at `docs/process/session-archives/session-state-pre-m19.md`.
