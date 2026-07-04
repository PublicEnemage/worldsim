# WorldSim Session State — Cockpit Card

> **Protocol:** This file is the program-level cockpit card for the current milestone.
> It must remain ≤ 200 lines — enforced by CI (`session-state-size-check` job).
> Intra-sprint status lives in each group's sprint journal issue (see §Cockpit below).
> Historical state lives in `docs/process/session-archives/`.
> Authority: `docs/process/sprint-group-isolation.md §SESSION_STATE.md Cockpit Card Protocol`.

**Last updated:** 2026-07-04 (CM Sprint C integrated; 5 Demo 8 clearance issues filed #1709–#1713; G6 Wave 4 added to sprint plan)
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
| Active wave | Wave 4 — G5/CM-A/CM-B/CM-C all integrated; G6 (Demo 8 clearance) is next sprint group |
| Active sprint groups | None — next: G6 (Demo 8 clearance: #1456, #1538, #1709, #1710) |
| Active sprint journal issues | None — #1700 closes at CM Sprint C PI Agent confirmation |

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
| G5 | Demo 8 display fidelity + Zone 1 view model | #1629 ✓, #1630 ✓, #1522 ✓, #1524 ✓ | **Integrated** — BPO ACCEPT all 4; PI Agent NM-094 PASS; integration PR #1684 merged 2026-07-04 |
| CM-A | ELASTICITY_REGISTRY Euro area calibration | #1623 ✓ | **Confirmed** — BPO ACCEPT; north star PASS; journal #1671 closed; integration PR #1683 merged 2026-07-03 |
| CM-B | ELASTICITY_REGISTRY LAC calibration (ARG/ECU/BOL/PER) | #1623 ✓ | **Confirmed** — BPO ACCEPT; north star PASS; journal #1688 closed; integration PR #1698 merged 2026-07-04 |
| CM-C | ELASTICITY_REGISTRY SEA calibration (PAK/LKA/BGD) | #1623 ✓ | **Confirmed** — BPO ACCEPT; north star PASS (PAK 2023 SBA); journal #1700 closed; integration PR #1707 auto-merging 2026-07-04 |

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
| #1632 | api_contracts.yml §trajectory missing band_method — G3 delivery gap | G5 ✓ | **Closed** — PR #1668 merged (G5 Phase B) |
| #1522 | View model layer retrofit — Zone 1 composition logic extraction | G5 ✓ | **Closed** — PR #1679 merged; trajectoryViewModel.ts + sliceToStepRange; 33 unit tests GREEN |
| #1524 | Zone 1A TrajectoryView: trackwheel zoom (desktop, reduced scope) | G5 ✓ | **Closed** — PR #1681 merged; visibleStepRange state + non-passive wheel listener |
| #1623 | ELASTICITY_REGISTRY — non-SSA entity family calibration gap | CM Sprint A+B+C ✓ | **All 3 gaps closed** — GRC T2 (PR #1683); LAC T3 (PR #1696); SEA T3 PAK/LKA/BGD (PR #1705 merged 2026-07-04); 10-entry registry complete |
| #1629 | Zone 1A ZMB y-axis not tight-scoped — curves collapse | G5 ✓ | **Closed** — PR #1666 merged; BPO ACCEPT 2026-07-03 |
| #1630 | Zone 1D delta annotations Mode 3 (ADR-017 §Zone 1D Integration) | G5 ✓ | **Closed** — PR #1669 merged; BPO ACCEPT 2026-07-03 |
| #1647 | G2C test file missing from release/m19 — NM-094 recovery | Demo 8 risk | **Closed** — PR #1649 merged; test_m19_g2c_scenario_runs.py (1394 lines) restored |
| #1650–#1656 | NM-084/085/086/089/092/093/094 process codification | G5 Phase A | **Closed** — PR #1658 MERGED (sprint/m19-g5) |
| #1657 | NM-090/091: DemographicModule dead subscriptions fix | Deferred (CM gate) | **Unblocked** — CM Sprint A confirmed; `entity_families` field syntax available; CM sign-off required before implementation PR opens |
| #1709 | FOUND state: tolerance band (±0.01) not displayed | G6 | Immediate — Demo 8 Act 1 blocker (Customer Agent L3 on #1540) |
| #1710 | AC-12: resolve `__structural_absence__` placeholder | G6 | Immediate — Demo 8 Act 1 blocker (Customer Agent L3 on #1540) |
| #1711 | Demo 8 Act 2 verification: GRC AC-1 live harness run | Act 2 verification | DATABASE_URL prerequisite — no code changes |
| #1712 | Demo 8 Act 2 verification: ARG AC-1 live harness run | Act 2 verification | DATABASE_URL prerequisite — no code changes |
| #1713 | Demo 8 Act 2 verification: PAK AC-1 live harness run | Act 2 verification | DATABASE_URL prerequisite — no code changes |

---

## Demo 8 Open Conditions (tracked from sprint exits)

| Condition | Source | Blocking |
|---|---|---|
| Tolerance band (±0.01) visible in FOUND state UI | Customer Agent L3 on #1540 → **#1709** | Demo 8 Act 1 |
| AC-12: resolve structural-absence indicator key (replace `__structural_absence__` placeholder) | Customer Agent L3 on #1540 → **#1710** | Demo 8 Act 1 |
| AC-1 harness live run (GRC orthodox vs heterodox): `per_step_diff[3] ∈ [0.010, 0.20]` | CM Sprint A exit §4 → **#1711** | Demo 8 Act 2 |
| AC-1 harness live run (ARG Type B `hd_composite` divergence): `per_step_diff[2] ∈ [0.003, 0.050]` | CM Sprint B exit §4 → **#1712** | Demo 8 Act 2 |
| AC-1 harness live run (PAK Type B `hd_composite` divergence): `per_step_diff[2] ∈ [0.002, 0.035]` | CM Sprint C exit §4 → **#1713** | Demo 8 Act 2 |

---

## Carry-Forward Context

- **Process model (M19 onward):** Sprint group isolation (Option E hybrid) + SESSION_STATE.md cockpit card (≤ 200 lines). Full protocol: `docs/process/sprint-group-isolation.md`. Shared state via `chore/m{N}-state-sync-NNN` → `release/m{N}` (PM Agent). Auto-merge: `gh pr merge --auto`.
- **Pre-push hook:** `.githooks/pre-push` enforces ruff + mypy (backend) and `npm run build` (frontend). Install: `git config core.hooksPath .githooks`. NM-092 fix (worktree path resolution) — merged PR #1646. Worktree symlink setup now in `sprint-group-isolation.md §Worktree Setup`.
- **NM-084–094 codification (G5 pre-flight, 2026-07-03):** Issues #1650–#1657 filed; PR #1658 carries 7 process doc additions (CODING_STANDARDS §E2E Mock Helper Authorship; sprint-planning-sop §Pre-Merge CM Review + §Co-Dependent Fixture; sprint-group-isolation §Worktree Setup + §Bidirectional lane rule + §Commit gate + §Test-file presence check). NM-090/091 DemographicModule fix deferred to separate PR (Issue #1657 — CM sign-off required first).
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
- **G5 complete + integrated (2026-07-03/04):** Phase A (NM codification), Phase B (#1629 ZMB y-axis + #1630 Zone 1D delta), Phase C (#1522 view model retrofit + #1524 trackwheel zoom). BPO ACCEPT all 4 user-facing deliverables. Integration PR #1684 `sprint/m19-g5 → release/m19` merged 2026-07-04. Sprint exit `docs/process/sprint-plans/m19-g5-sprint-exit.md`. ESM rule: use `import.meta.dirname` not `__dirname` in all E2E spec files (caught by release-branch-ci-gate — PR #1693).
- **G5 Zone 1A zoom (#1524, 2026-07-03):** Desktop trackwheel zoom only (EL decision: mobile pinch/pan deferred). `visibleStepRange` state in `TrajectoryView`; non-passive wheel listener; midpoint-centered 20% zoom; double-click reset; `data-visible-step-min/max` DOM attributes. Prerequisite #1522 merged first.
- **G5 #1630 scope (2026-07-03):** ADR-017 §Zone 1D Integration (Mode 3) mandates per-framework `(+Δ vs baseline)` annotations in Zone 1D. `formatDelta`/`getDeltaColor` exported from `FourFrameworkZone1D`. Intent: `docs/process/intents/M19-G5-2026-07-03-zone1d-delta-annotations.md`.
- **M18 complete (v0.18.0, 2026-07-02):** G1–G7 delivered; Demo 7 PASS (unconditional); release/m18 → main via PR #1534. Archive: `docs/process/session-archives/session-state-pre-m19.md`.
- **CM Sprint A complete (2026-07-03):** GRC Euro area ELASTICITY_REGISTRY calibration — `entity_families` scoping field on `CohortElasticity`; GRC Q1 FORMAL (−0.25, T2, B&L 2013) + Q2 FORMAL (−0.15, T2, Ball 2013). Greece 2010 counter-factual upgrades from DIRECTION_ONLY advisory to calibrated MAGNITUDE basis. 20/20 unit tests GREEN. BPO ACCEPT; north star PASS. Integration PR #1683 merged to release/m19.
- **CM Sprint B complete (2026-07-04):** LAC ELASTICITY_REGISTRY calibration — ARG/ECU/BOL/PER `entity_families`; LAC Q1 FORMAL (−0.22, T3, Lustig 2014 CEQ WP/13) + Q2 FORMAL (−0.13, T3, Ball 2013 0.60 scaling). FORMAL-only (Option a) avoids double-counting with SSA Q1 INFORMAL. Argentina/Ecuador/Bolivia/Peru scenarios now use LAC-calibrated formal-sector channel not SSA proxy. 23/23 unit tests GREEN. BPO ACCEPT; north star PASS (Bolivia IMF negotiation scenario). Integration PR #1698 merged to release/m19.
- **CM Sprint C complete (2026-07-04):** SEA ELASTICITY_REGISTRY calibration — PAK/LKA/BGD `entity_families`; SEA Q1 FORMAL (−0.17, T3, Ilzetzki et al. 2013 developing-country multiplier 0.35–0.40; Q1 concentration 1.35× with BISP/Samurdhi discount) + Q2 FORMAL (−0.10, T3, Ball 2013 0.60 scaling). FORMAL-only (Option a). 26/26 unit tests GREEN. BPO ACCEPT; north star PASS (PAK 2023 IMF SBA negotiation scenario). Integration PR #1707 auto-merging to release/m19. Issue #1623 fully resolved — all three gaps (GRC T2, LAC T3, SEA T3). Known limitation: SSA INFORMAL proxy overstates informal channel for SEA — Option (d) suppression deferred beyond M19. Batini 2012 reference corrected to Ilzetzki 2013 in calibration decision.
- **Demo 7 north star (2026-07-02):** Aicha presents Zambia +342K cohort effect with CI bounds and sourcing to IMF restructuring table. Next available DEMO-167.
