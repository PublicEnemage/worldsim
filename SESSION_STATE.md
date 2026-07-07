# WorldSim Session State — Cockpit Card

> **Protocol:** This file is the program-level cockpit card for the current milestone.
> It must remain ≤ 200 lines — enforced by CI (`session-state-size-check` job).
> Intra-sprint status lives in each group's sprint journal issue (see §Cockpit below).
> Historical state lives in `docs/process/session-archives/`.
> Authority: `docs/process/sprint-group-isolation.md §SESSION_STATE.md Cockpit Card Protocol`.

**Last updated:** 2026-07-07 (AEA D1/D2 merged; D3 Coverage Audit filed; AEA commissioned session complete pending EL review of D3)
**Current milestone:** M20 — Interactive Constraint Search and Demo 9

---

## Cockpit

| Field | Value |
|---|---|
| Milestone | M20 — Interactive Constraint Search and Demo 9 |
| GitHub Milestone | #22 — created 2026-07-06 |
| Exit checklist issue | #1773 (M20 Exit Checklist — blocks milestone closure) |
| Release branch | `release/m20` — to be cut from main at M20 kickoff |
| Sprint plan | `docs/process/sprint-plans/m20-sprint-plan.md` — to be filed at M20 kickoff |
| Active wave | None — M20 sprint planning pending |
| Active sprint journal issues | None |

---

## Open EL Decisions

| Decision | Status |
|---|---|
| AEA D3 — Coverage Audit (`docs/evidence/coverage-audit.md`) | **PENDING EL REVIEW** — on `docs/aea-d3-coverage-audit`; commissioned session complete pending EL review |

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

## Carry-Forward Context

- **Process model:** Sprint group isolation (Option E hybrid) + SESSION_STATE.md cockpit (≤ 200 lines). Protocol: `docs/process/sprint-group-isolation.md`. Shared state via `chore/m{N}-state-sync-NNN` → `release/m{N}` (PM Agent).
- **Pre-push hook:** `.githooks/pre-push` enforces ruff + mypy (backend) and `npm run build` (frontend). Install: `git config core.hooksPath .githooks`.
- **M19 complete (v0.19.0, 2026-07-06):** G1–G8 + CM-A–D delivered; Demo 8 PASS (constraint-derived boundary); SCAN-029 Clean. Archive: `docs/process/session-archives/session-state-pre-m20.md`.
- **Demo 8 north star (2026-07-06):** "The constraint-floor boundary is 0.83. Your proposed programme, which assumes a multiplier above 0.83, embeds the poverty crossing as a structural consequence." Next available DEMO-237.
- **M20 primary deliverable:** Live interactive constraint-floor search (real-time boundary on floor adjustment). Instrument polish: DEMO-217 (in-viewport Act 1→Act 2 link), DEMO-233/#1775 (WARNING alongside CLEAR), DEMO-234/#1776 (±0.01 vs CI label), DEMO-235/#1777 (PSP multi-scenario comparison).
- **ADR-008 renewal carry-forward:** SCAN-029 finding — must complete before M20 close.
- **NM-099/Issue #1759:** asgi_client pool ordering in test_m19_cm_b; fix deferred to next sprint touching the file (EL decision 2026-07-05).
- **sprint-branch-ci-gate Ruleset:** Node ID `RRS_lACqUmVwb3NpdG9yecc5IKi2kzgEV92A`. Requires `changes`, `lint`, `test-backend`, `compliance-scan`.
- **stash backlog (active):** 26 entries remain. Key: stash@{7} (M18 chore + G1 orphans), stash@{8}/{9} (M18-G2 duplicates, likely superseded PR #1387).
- **GA-02 / Path 2 retired (PR #1393):** No implementation without EL-approved governance exception.
