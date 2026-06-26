# WorldSim Session State — Cockpit Card

> **Protocol:** This file is the program-level cockpit card for the current milestone.
> It must remain ≤ 200 lines — enforced by CI (`session-state-size-check` job).
> Intra-sprint status lives in each group's sprint journal issue (see §Cockpit below).
> Historical state lives in `docs/process/session-archives/`.
> Authority: `docs/process/sprint-group-isolation.md §SESSION_STATE.md Cockpit Card Protocol`.

**Last updated:** 2026-06-26 (M17 CLOSED — v0.17.0 released; M18 entry blockers in progress; #1328/#1329 resolved this session)
**Current milestone:** M18 — Full Argument and Demo 7 (GitHub Milestone 19)

---

## Cockpit

| Field | Value |
|---|---|
| Milestone | M18 — Full Argument and Demo 7 |
| GitHub Milestone | #19 |
| Exit checklist issue | #1340 |
| Release branch | ⏳ NOT YET CUT (entry blockers in progress) |
| Sprint plan | ⏳ NOT YET FILED |
| Active wave | None — pre-Wave 1 |
| Active sprint groups | None |
| Active sprint journal issues | None |

---

## M18 Entry Blockers

All must be resolved before `release/m18` is cut and the sprint entry gate opens.

| Issue | NM | Title | Status |
|---|---|---|---|
| #1328 | NM-066 | SESSION_STATE.md size exceeds Claude Code read ceiling | ✅ RESOLVED 2026-06-26 — cockpit card + archive implemented (this session) |
| #1329 | NM-067 | No sprint group isolation protocol for parallel workstreams | ✅ RESOLVED 2026-06-26 — Option E hybrid + DS amendment implemented (this session) |
| #1332 | NM-068 | Sprint entry gate: prior NM verification field missing | ⏳ PENDING |
| #1333 | NM-069 | .gitignore missing Playwright/test artifact directories | ⏳ PENDING |
| #1334 | NM-070 | Pre-push gates: git hook enforcement non-functional | ⏳ PENDING |
| #1335 | NM-071 | Sprint planning SOP: wave-level concurrency ceiling | ⏳ PENDING |

---

## Open EL Decisions

None open. #1328 and #1329 resolved 2026-06-26 (DS consultation; Option E hybrid; EL approved).

---

## M18 Open Issues

| Issue | Title | Wave / Priority |
|---|---|---|
| #1340 | M18 Exit Checklist — blocks milestone closure | Gate issue |
| #843 | Demo 7 — live external session (Senegal Mode 3 + Zambia 3-scenario) | Primary deliverable |
| #1254 | CI bands on Zone 1A trajectories (ADR-007 full implementation) | Wave 1 |
| #1255 | PSP driver decomposition | Wave 1 |
| #1256 | Path 2 / counter-scenario comparison | Wave 1 |
| #394 | Multi-scenario comparison Phase 2 | Wave 1 |
| #1217 | Mode 3 render optimization | Deferred |
| #1238 | DEMO6-009 narration layer | Deferred |
| #1059 | HCL demo narration | Deferred |

---

## Carry-Forward Context

- **Process redesign (M18):** Sprint group isolation (Option E hybrid) + SESSION_STATE.md cockpit card model now active from M18 onward. Full documentation: `docs/process/sprint-group-isolation.md`.
- **Auto-merge protocol (PR #1344):** CLAUDE.md updated — `gh pr merge --auto` replaces polling loop; `gh run watch` for observation. KI-007 filed (GraphQL rate limit). Active from M18.
- **Agent roster (PR #1342/#1343):** Chief Engineer renamed → Computation Engine Agent. DevSecOps Agent (DS) added — owns `.github/`, `.githooks/`, `.gitignore`, sprint isolation process doc.
- **M17 archive:** Full M1–M17 session state at `docs/process/session-archives/session-state-pre-m18.md`.
