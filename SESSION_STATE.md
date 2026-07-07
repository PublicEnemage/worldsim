# WorldSim Session State — Cockpit Card

> **Protocol:** This file is the program-level cockpit card for the current milestone.
> It must remain ≤ 200 lines — enforced by CI (`session-state-size-check` job).
> Intra-sprint status lives in each group's sprint journal issue (see §Cockpit below).
> Historical state lives in `docs/process/session-archives/`.
> Authority: `docs/process/sprint-group-isolation.md §SESSION_STATE.md Cockpit Card Protocol`.

**Last updated:** 2026-07-07 (M20-G2 closed — AEP-004–009 EL-REVIEWED; integration PR #1809 merged; G3 pending entry)
**Current milestone:** M20 — Analytical Evidence Portfolio and Demo 9

---

## Cockpit

| Field | Value |
|---|---|
| Milestone | M20 — Analytical Evidence Portfolio and Demo 9 |
| GitHub Milestone | #22 |
| Exit checklist issue | #1773 (M20 Exit Checklist — blocks milestone closure) |
| Release branch | `release/m20` — cut 2026-07-07 from main `5fadd00` |
| Sprint plan | `docs/process/sprint-plans/m20-sprint-plan.md` — filed 2026-07-07 |
| Active wave | G3 — AEP SOUTH-SE-ASIAN (AEP-010–011) + gap closure issues; pending sprint entry |
| Active sprint journal issues | None (G2 closed 2026-07-07; G3 not yet opened) |

---

## Open EL Decisions

None.

---

## M19 Exit Ceremony Status — COMPLETE

| Step | Status |
|---|---|
| Step 1 — Open issue audit | **PASS** — all M19 issues dispositioned |
| Step 2 — Reference document audit | **COMPLETE** — README.md, CLAUDE.md, roadmap all updated |
| SCAN-029 | **Clean** — ruff 0 violations, mypy 73 files, frontend build clean |
| Session state archive | **Filed** — `docs/process/session-archives/session-state-pre-m20.md` |
| Step 3 — Consistency check | **PASS** |
| Step 4 — Fresh session test | **PASS** — stale status notes cleared; no critical gaps |
| Retrospective | **Filed** — comment on #1535 |
| release/m19 → main | **MERGED** — PR #1778, 2026-07-07 |
| #1535 | **CLOSED** — 2026-07-07 |

---

## M20 Open Issues

| Issue | Title | Priority |
|---|---|---|
| #1773 | M20 Exit Checklist | Milestone exit gate |
| #1791 | fix: G2C Type B tests — pre-run baseline before baseline_run_id (NM-101) | High — M20-G4 scope |
| #1796 | engine: fin_composite path insensitivity in CF scenarios | M21+ implementation |
| #1797 | engine: failure mode non-detection in EURO-AREA rapid-onset crises | M21+ implementation |
| #1759 | fix: asgi_client pool ordering (test_m19_cm_b) | Carry-forward NM-099; low severity |
| #1775 | DEMO-233: WARNING badge not displayed alongside CLEAR | Medium — M20 instrument polish |
| #1776 | DEMO-234: Binary search precision label vs CI label | High — M20 instrument polish |
| #1777 | DEMO-235: PSP driver arc missing in multi-scenario view | High — M20 instrument polish |

---

## AEA Evidence Foundation — Status

| Artifact | Status |
|---|---|
| `docs/evidence/TEMPLATE.md` | MERGED — PR #1780 |
| `docs/evidence/analytical-framework.md` | MERGED + EL-APPROVED — PR #1781 (body), #1783 (CM two-condition rule) |
| `docs/evidence/coverage-audit.md` | MERGED — PR #1782 |
| `docs/process/agents.md §External Intelligence Layer` | MERGED — PR #1781 (corrected NM-100) |
| `CLAUDE.md §External Intelligence Layer` | MERGED — PR #1781 (corrected NM-100) |
| G1 sprint entry | `docs/process/sprint-plans/m20-g1-sprint-entry.md` — EL-approved 2026-07-07 |
| G1 sprint exit | `docs/process/sprint-plans/m20-g1-sprint-exit.md` — PI Agent confirmed 2026-07-07 |
| AEP-001-GRC-2010 | MERGED — PR #1788; EL-REVIEWED; DIRECTION_ONLY; Type A; 5/6 PASS |
| AEP-002-GRC-2010-B | MERGED — PR #1790; EL-REVIEWED; DIRECTION_ONLY; Type B; COUNTER_FACTUAL_BETTER |
| AEP-003-ISL-2008 | MERGED — PR #1792; EL-REVIEWED; DIRECTION_ONLY; Type B; BASELINE_BETTER |
| G2 sprint entry | `docs/process/sprint-plans/m20-g2-sprint-entry.md` — EL-approved 2026-07-07 |
| G2 sprint exit | `docs/process/sprint-plans/m20-g2-sprint-exit.md` — PI Agent confirmed 2026-07-07 |
| AEP-004-ZMB-2014 | MERGED — PR #1800; EL-REVIEWED; DIRECTION_ONLY; Type A; SSA-LIC |
| AEP-005-SEN-2014 | MERGED — PR #1801; EL-REVIEWED; DIRECTION_ONLY; Type A; SSA-LIC |
| AEP-006-GHA-2022 | MERGED — PR #1802/#1807; EL-REVIEWED; DIRECTION_ONLY; Type A; SSA-LIC |
| AEP-007-ARG-2001 | MERGED — PR #1803; EL-REVIEWED; DIRECTION_ONLY; Type A+B; LATAM-EM |
| AEP-008-ARG-2003 | MERGED — PR #1804; EL-REVIEWED; DIRECTION_ONLY; Type A CM-D; LATAM-EM |
| AEP-009-ECU-1999 | MERGED — PR #1805/#1807; EL-REVIEWED; DIRECTION_ONLY; Type A; LATAM-EM |
| Next AEP entries | AEP-010–011 (SOUTH-SE-ASIAN) — G3 pending sprint entry |

---

## Carry-Forward Context

- **Process model:** Sprint group isolation (Option E hybrid) + SESSION_STATE.md cockpit (≤ 200 lines). Protocol: `docs/process/sprint-group-isolation.md`. Shared state via `chore/m{N}-state-sync-NNN` → `release/m{N}` (PM Agent).
- **Pre-push hook:** `.githooks/pre-push` enforces ruff + mypy (backend) and `npm run build` (frontend). Install: `git config core.hooksPath .githooks`.
- **M19 complete (v0.19.0, 2026-07-06):** G1–G8 + CM-A–D delivered; Demo 8 PASS (constraint-derived boundary); SCAN-029 Clean. Archive: `docs/process/session-archives/session-state-pre-m20.md`.
- **Demo 8 north star (2026-07-06):** "The constraint-floor boundary is 0.83. Your proposed programme, which assumes a multiplier above 0.83, embeds the poverty crossing as a structural consequence." Next available DEMO-237.
- **M20 primary deliverable:** AEP — 11 entries across all four calibration families (G1: EUR AEP-001–003; G2: SSA/LAT AEP-004–009; G3: SEA AEP-010–011 + gap issues). Instrument polish: DEMO-217, DEMO-233/#1775, DEMO-234/#1776 (G4). Live constraint search and DEMO-235 → M21.
- **ADR-008 renewal carry-forward:** SCAN-029 finding — must complete before M20 close.
- **NM-099/Issue #1759:** asgi_client pool ordering in test_m19_cm_b; fix deferred to next sprint touching the file (EL decision 2026-07-05).
- **sprint-branch-ci-gate Ruleset:** Node ID `RRS_lACqUmVwb3NpdG9yecc5IKi2kzgEV92A`. Requires `changes`, `lint`, `test-backend`, `compliance-scan`.
- **stash backlog (active):** 26 entries remain. Key: stash@{7} (M18 chore + G1 orphans), stash@{8}/{9} (M18-G2 duplicates, likely superseded PR #1387).
- **GA-02 / Path 2 retired (PR #1393):** No implementation without EL-approved governance exception.
