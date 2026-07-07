# WorldSim Session State — Cockpit Card

> **Protocol:** This file is the program-level cockpit card for the current milestone.
> It must remain ≤ 200 lines — enforced by CI (`session-state-size-check` job).
> Intra-sprint status lives in each group's sprint journal issue (see §Cockpit below).
> Historical state lives in `docs/process/session-archives/`.
> Authority: `docs/process/sprint-group-isolation.md §SESSION_STATE.md Cockpit Card Protocol`.

**Last updated:** 2026-07-07 (M20 kickoff — scope confirmed; release/m20 cut; sprint plan filed; DEMO-235 deferred to M21)
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
| Active wave | None — G1 entry pending |
| Active sprint journal issues | None |

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
| Next AEP entries | To be commissioned — first entries will use SSA-1 (SEN), SSA-2 (ZMB), EUR-1 (GRC) per coverage audit |

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
