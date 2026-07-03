# WorldSim Session State — Cockpit Card

> **Protocol:** This file is the program-level cockpit card for the current milestone.
> It must remain ≤ 200 lines — enforced by CI (`session-state-size-check` job).
> Intra-sprint status lives in each group's sprint journal issue (see §Cockpit below).
> Historical state lives in `docs/process/session-archives/`.
> Authority: `docs/process/sprint-group-isolation.md §SESSION_STATE.md Cockpit Card Protocol`.

**Last updated:** 2026-07-03 (DS infra review: NM-092/093/094 filed; PR #1646 hook fix; G2C test recovery PR #1649; stash/worktree cleanup; G2D confirmed; PR #1641 merged)
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
| Active wave | Wave 2 — G2D confirmed; Ecuador regression fixed (PR #1642); integration PR #1641 pending CI re-run |
| Active sprint groups | None — G2D exit confirmed; integration PR #1641 sprint/m19-g2 → release/m19 pending (CI re-running after conflict fix PR #1643) |
| Active sprint journal issues | None — #1621 closed at G2D PI Agent confirmation |

---

## Open EL Decisions

| Decision | Status |
|---|---|
| ARCH-014 scope: capital controls full fix M19 or defer to M20? | **RESOLVED 2026-07-03** — ADR-020 accepted; Iceland (#1553) stays in M19. G2D sprint entry EL-approved; implementation branches open (channel-impl, dm-audit, cm-calibration). G2C integration PR defers to G2D exit. |

---

## Sprint Status (Wave 1 + Wave 2)

| Group | Sprint | Issues | Exit status |
|---|---|---|---|
| G1 | Mode 3 constraint-floor search | #1540 ✓, #1563 ✓, #1564 ✓ | Confirmed — integrated to release/m19 (PR #1582, 2026-07-03) |
| G2A | Headless battle-testing harness | #1546 ✓ | Confirmed — PI confirm retroactively filed PR #1580/#1583 |
| G2B | SEN + ZMB backtesting fixtures | #1541 ✓, #1542 ✓ | Confirmed — exit doc PR #1578 |
| G2C | Battle-testing 7-country suite | #1547 ✓, #1548 ✓, #1549 ✓, #1550 ✓, #1551 ✓, #1552 ✓, #1554 ✓ | Confirmed — exit doc `m19-g2c-sprint-exit.md`; integration PR defers to G2D exit |
| G2D | Iceland 2008–11 (capital controls) | #1532 ✓, #1553 ✓ | **Confirmed** — BPO 2×ACCEPT; north star PASS; journal #1621 closed; integration PR pending (sprint/m19-g2 → release/m19) |
| G3 | Bayesian posterior calibration | #1543 ✓, #1536 ✓, #1537 ✓ | Confirmed — integration PR #1617 merged; exit doc `m19-g3-sprint-exit.md`; journal #1587 closed retroactively |
| G4 | PSP driver arc + CI label precision | #1528 ✓, #1529 ✓ | Confirmed — integration PR #1637 merged; journal #1624 closed; sprint exit `docs/process/sprint-plans/m19-g4-sprint-exit.md` |

---

## M19 Open Issues (Wave 2+)

| Issue | Title | Group | Priority |
|---|---|---|---|
| #1535 | M19 Exit Checklist | — (gate) | Milestone exit gate |
| #1544 | Demo 8 — live stakeholder session | — (exit gate) | Primary deliverable |
| #1532 | Capital controls transmission gap | G2D ✓ | **Closed** — PR #1635 merged; BPO ACCEPT 2026-07-03 |
| #1553 | Iceland 2008–11 Type A+B | G2D ✓ | **Closed** — PR #1639 merged; BPO ACCEPT 2026-07-03 |
| #1456 | MDAAlertPanel Zone1B: scenarioId crash | Pre-wave | Immediate — crash risk |
| #1538 | Focal cohort floor validation | Pre-wave | Immediate — #1540 prerequisite |
| #1528 | PSP driver arc + auditability panel (DEMO-165) | G4 | **G4 confirmed** — PR #1633 merged |
| #1529 | '95% CI' label precision fix | G4 | **G4 confirmed** — PR #1634 merged; Demo 8 Act 2 gate cleared |
| #1632 | api_contracts.yml §trajectory missing band_method — G3 delivery gap | G5 | Low — schema-only fix; non-blocking |
| #1522 | View model layer retrofit — Zone 1 composition logic extraction | Wave 3+ | High — EL-added to M19 |
| #1524 | Zone 1A TrajectoryView: pinch-zoom, thumbwheel zoom, pan | Wave 3+ | High — EL-added to M19 |
| #1623 | ELASTICITY_REGISTRY — non-SSA entity family calibration gap | CM Wave 2–3 | High — CM Sprint A (GRC/Euro area) M19 priority; unblocks Greece counter-factual |
| #1629 | Zone 1A ZMB y-axis not tight-scoped — curves collapse | Demo 8 risk | High — Demo 8 Act 2 display fidelity; `computeYDomain` fix required |
| #1630 | Demo 8 Act 1 narration: HD line implied but not rendered in Zone 1A | Demo 8 risk | High — Demo 8 Act 1; narration correction or per-framework lines (EL decision) |
| #1647 | G2C test file missing from release/m19 — NM-094 recovery | Demo 8 risk | **High** — test_m19_g2c_scenario_runs.py (1394 lines, all 7 G2C scenarios) absent; CI has no G2C backtesting coverage |

---

## Demo 8 Open Conditions (tracked from sprint exits)

| Condition | Source | Blocking |
|---|---|---|
| Tolerance band (±0.01) visible in FOUND state UI | Customer Agent L3 on #1540 | Demo 8 Act 1 |
| AC-12: resolve structural-absence indicator key (replace `__structural_absence__` placeholder) | Customer Agent L3 on #1540 | Demo 8 Act 1 |

---

## Carry-Forward Context

- **Process model (M19 onward):** Sprint group isolation (Option E hybrid) + SESSION_STATE.md cockpit card (≤ 200 lines). Full protocol: `docs/process/sprint-group-isolation.md`. Shared state via `chore/m{N}-state-sync-NNN` → `release/m{N}` (PM Agent). Auto-merge: `gh pr merge --auto`.
- **Pre-push hook:** `.githooks/pre-push` enforces ruff + mypy (backend) and `npm run build` (frontend). Install: `git config core.hooksPath .githooks`. NM-092 fix (worktree path resolution) in PR #1646 — pending merge.
- **NM-092/093/094 (DS infra review 2026-07-03):** NM-092: pre-push hook relative paths silently bypass gates in worktrees (fix: PR #1646). NM-093: chore/state-sync-025 carried sprint implementation commits — bidirectional lane rule now explicit. NM-094: G2C QA test file missing from release/m19 (Issue #1647 — Demo 8 risk). 4 prunable M18 worktrees cleared. 4 confirmed-safe stash entries dropped (stash@{0}/{1}/{2}/{10}).
- **Stash backlog (active):** 26 entries remain. Key items requiring EL triage: stash@{7} (M18-era chore + G1 orphans), stash@{8}/{9} (duplicate M18-G2 pair on feat/m18-g2-psp-impl — likely superseded by PR #1387).
- **GA-02 / Path 2 retirement (PR #1393):** Proprietary ministry data upload retired on open-source-as-strategy principle. No implementation without EL-approved governance exception.
- **sprint-branch-ci-gate Ruleset:** Node ID `RRS_lACqUmVwb3NpdG9yecc5IKi2kzgEV92A`. Requires `changes`, `lint`, `test-backend`, `compliance-scan`. (playwright-e2e not required — NM-076 context.)
- **NM-075:** git worktrees must be allocated per sprint group (`git worktree add /tmp/<name> <branch>`) to prevent branch switches overwriting in-progress work.
- **NM-076:** Before any testid rename, grep the full E2E corpus for the old testid; update E2E tests in the same PR. Rule in CODING_STANDARDS.md (PR #1439).
- **G3 complete (2026-07-03):** ARCH-016 (ADR-007 Amendment 1) accepted; all three issues (#1543, #1536, #1537) implemented; BPO 3×ACCEPT; north star test CONDITIONAL PASS (G4 #1529 needed for Demo 8 Act 2 — now RESOLVED). Integration PR #1617 merged.
- **NM-084/NM-085:** CM sign-off ordering gap + co-dependent fixture CI sequencing (G2B). SOP improvements filed. G3 NM-084 gate satisfied correctly (CM sign-off on issue before PI gate comment before auto-merge).
- **G2D complete (2026-07-03):** ADR-020 channels A/B/C implemented (PR #1635; 28/28 unit tests). Iceland 2008–11 fixture (PR #1639; heterodox vs orthodox counter-factual). BPO 2×ACCEPT; north star PASS (Zambia restructuring scenario; heterodox path analytically distinguishable). Journal #1621 closed. Ecuador regression fix (PR #1642 — implementation_capacity=0 for salvazo; Channel B was firing via one-step lag). Merge conflict resolved on sprint/m19-g2 (PR #1643). Integration PR #1641 `sprint/m19-g2 → release/m19` pending auto-merge — CI re-running after conflict resolution. Demo 8 condition: DIRECTION_ONLY qualifier required on Iceland direction verdict at Demo 8 Act 2.
- **ADR-020 (ARCH-014) calibration constants (frozen):** Channel A ε=0.60 (ISL controls-only), β=0.020, γ=1.2 (CM constant — CE cannot change without CM Consulted), φ=−0.30 (ISL Q1 informal PHC). Sources: `calibration-basis.md §Capital Controls` (PR #1625).
- **NM-086:** E2E mock routes must be verified against `api_contracts.yml` before the implementation PR opens (G1, filed 2026-07-03). Process: QA Lead mock-helper verification is a blocking checklist item on intent authorship.
- **G4 forward condition (G5 scope):** Issue #1632 (`band_method` missing from `api_contracts.yml §trajectory` — G3 delivery gap). Schema-only fix. Must resolve before G5 closes. NM-086 gate left open in G4 QA ack block.
- **M18 complete (v0.18.0, 2026-07-02):** G1–G7 delivered; Demo 7 PASS (unconditional); release/m18 → main via PR #1534. Archive: `docs/process/session-archives/session-state-pre-m19.md`.
- **Demo 7 north star (2026-07-02):** Aicha presents Zambia +342K cohort effect with CI bounds and sourcing to IMF restructuring table. Next available DEMO-167.
