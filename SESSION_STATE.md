# WorldSim Session State — Cockpit Card

> **Protocol:** This file is the program-level cockpit card for the current milestone.
> It must remain ≤ 200 lines — enforced by CI (`session-state-size-check` job).
> Intra-sprint status lives in each group's sprint journal issue (see §Cockpit below).
> Historical state lives in `docs/process/session-archives/`.
> Authority: `docs/process/sprint-group-isolation.md §SESSION_STATE.md Cockpit Card Protocol`.

**Last updated:** 2026-07-06 (M19 exit ceremony complete — reference docs updated, SCAN-029 clean, M20 cockpit card filed; prerequisite: EL admin bypass release/m19 → main pending)
**Current milestone:** M20 — Interactive Constraint Search and Demo 9

---

## Cockpit

| Field | Value |
|---|---|
| Milestone | M20 — Interactive Constraint Search and Demo 9 |
| GitHub Milestone | #22 — created 2026-07-06 |
| Exit checklist issue | #1773 (M20 Exit Checklist — blocks milestone closure) |
| Release branch | `release/m20` — to be cut from main at M20 kickoff (after EL merges release/m19 → main) |
| Sprint plan | `docs/process/sprint-plans/m20-sprint-plan.md` — to be filed at M20 kickoff |
| Active wave | None — M19 exit ceremony; M20 sprint planning pending EL merge |
| Active sprint journal issues | None |

---

## Open EL Decisions

| Decision | Status |
|---|---|
| M19 exit: release/m19 → main admin bypass | **PENDING** — EL must merge `release/m19 → main` before M20 can begin |

---

## M19 Exit Ceremony Status

| Step | Status |
|---|---|
| Step 1 — Open issue audit | **PASS** — `gh issue list --milestone "Milestone 19"` returned [] (only #1535 open) |
| Step 2 — Reference document audit | **COMPLETE** — README.md badge→v0.19.0, M19 Complete/M20 row; CLAUDE.md M19→complete M20→current; roadmap M19 *(complete)* + M20 section + Where We Are |
| SCAN-029 | **Clean** — ruff 0 violations, mypy 73 files no issues, frontend build clean |
| Session state archive | **Filed** — `docs/process/session-archives/session-state-pre-m20.md` |
| Step 3 — Consistency check | **PASS** — #1544 closed; #1535 open (gate); M20 #1773 listed; no stale notes |
| Step 4 — Fresh session test | **Pending** — run after EL merges release/m19 → main |
| Retrospective | **Filed as comment on #1535** |
| M20 milestone | **Created** — #22 (2026-07-06) |
| M20 exit checklist | **Filed** — #1773 (2026-07-06) |

---

## M20 Open Issues

| Issue | Title | Priority |
|---|---|---|
| #1773 | M20 Exit Checklist | Milestone exit gate |
| #1759 | fix: asgi_client pool ordering (test_m19_cm_b) | Carry-forward NM-099; low severity |

---

## Carry-Forward Context

- **Process model:** Sprint group isolation (Option E hybrid) + SESSION_STATE.md cockpit (≤ 200 lines). Protocol: `docs/process/sprint-group-isolation.md`. Shared state via `chore/m{N}-state-sync-NNN` → `release/m{N}` (PM Agent).
- **Pre-push hook:** `.githooks/pre-push` enforces ruff + mypy (backend) and `npm run build` (frontend). Install: `git config core.hooksPath .githooks`. NM-092 fix merged PR #1646.
- **M19 complete (v0.19.0, 2026-07-06):** G1–G8 + CM-A–D delivered; Demo 8 PASS (constraint-derived boundary); SCAN-029 Clean. Archive: `docs/process/session-archives/session-state-pre-m20.md`.
- **Demo 8 north star (2026-07-06):** "The constraint-floor boundary is 0.83. Your proposed programme, which assumes a multiplier above 0.83, embeds the poverty crossing as a structural consequence." Next available DEMO-237.
- **M20 primary deliverable:** Live interactive constraint-floor search (real-time boundary on floor adjustment). Instrument polish: DEMO-217 (in-viewport Act 1→Act 2 link), DEMO-233 (WARNING alongside CLEAR), DEMO-234 (±0.01 vs CI label), DEMO-235 (PSP multi-scenario comparison).
- **ADR-008 renewal carry-forward:** SCAN-029 finding — no M19 changes triggered ADR-008; must complete before M20 close.
- **NM-099/Issue #1759:** asgi_client pool ordering in test_m19_cm_b; fix deferred to next sprint touching the file (EL decision 2026-07-05).
- **sprint-branch-ci-gate Ruleset:** Node ID `RRS_lACqUmVwb3NpdG9yecc5IKi2kzgEV92A`. Requires `changes`, `lint`, `test-backend`, `compliance-scan`.
- **stash backlog (active):** 26 entries remain. Key: stash@{7} (M18 chore + G1 orphans), stash@{8}/{9} (M18-G2 duplicates, likely superseded PR #1387).
- **GA-02 / Path 2 retired (PR #1393):** No implementation without EL-approved governance exception.
