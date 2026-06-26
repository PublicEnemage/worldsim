# WorldSim Session State — Cockpit Card

> **Protocol:** This file is the program-level cockpit card for the current milestone.
> It must remain ≤ 200 lines — enforced by CI (`session-state-size-check` job).
> Intra-sprint status lives in each group's sprint journal issue (see §Cockpit below).
> Historical state lives in `docs/process/session-archives/`.
> Authority: `docs/process/sprint-group-isolation.md §SESSION_STATE.md Cockpit Card Protocol`.

**Last updated:** 2026-06-26 (M18 kicked off — sprint plan EL-approved PR #1364; release/m18 cut at 151904d; G1+G2 sprint entries next)
**Current milestone:** M18 — Full Argument and Demo 7 (GitHub Milestone 19)

---

## Cockpit

| Field | Value |
|---|---|
| Milestone | M18 — Full Argument and Demo 7 |
| GitHub Milestone | #19 |
| Exit checklist issue | #1340 |
| Release branch | ✅ `release/m18` — cut 2026-06-26 at commit 151904d |
| Sprint plan | ✅ EL-approved 2026-06-26 — `docs/process/sprint-plans/m18-sprint-plan.md` (PR #1364) |
| Active wave | Pre-wave (GD + GR may begin; Wave 1 entries pending) |
| Active sprint groups | None — G1+G2 sprint entries not yet filed |
| Active sprint journal issues | None |

---

## M18 Entry Blockers — All Resolved

All blockers resolved before `release/m18` was cut.

| Issue | NM | Title | Status |
|---|---|---|---|
| #1328 | NM-066 | SESSION_STATE.md size exceeds Claude Code read ceiling | ✅ RESOLVED 2026-06-26 — cockpit card + archive implemented (this session) |
| #1329 | NM-067 | No sprint group isolation protocol for parallel workstreams | ✅ RESOLVED 2026-06-26 — Option E hybrid + DS amendment implemented (this session) |
| #1332 | NM-068 | Sprint entry gate: prior NM verification field missing | ✅ RESOLVED 2026-06-26 — sprint entry template §6.5 (PR #1345) |
| #1333 | NM-069 | .gitignore missing Playwright/test artifact directories | ✅ RESOLVED 2026-06-26 — .gitignore + sprint entry template §6.3a (PR #1346) |
| #1334 | NM-070 | Pre-push gates: git hook enforcement non-functional | ✅ RESOLVED 2026-06-26 — .githooks/pre-push + CONTRIBUTING.md Step 7 (PR #1346) |
| #1335 | NM-071 | Sprint planning SOP: wave-level concurrency ceiling | ✅ RESOLVED 2026-06-26 — sprint-planning-sop.md §Wave Kickoff Coordination Check (PR #1347) |

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
| #1349 | Counter-scenario comparison — distributional number differential with CI bands | G3 Wave 2 (blocked: GR #1352) |
| #1352 | Requirements phase for #1349 — UX journeys, Customer Agent, BPO requirements | GR Pre-wave / ready to begin |
| #1354 | Control Plane Column Design Package — Mode 2 + Mode 3 (7 artifacts #1355–#1361) | GD Pre-wave / ready to begin |
| #1256 | Path 2 / proprietary data integration | Capacity-allowing |
| #1217 | Mode 3 render optimization (EX-001 expired) | G4 Wave 2 — sequenced via GD/ADR-019 |
| #1238 | DEMO6-009 TTS narration fix | Capacity-allowing |
| #1059 | HCL narration integration | Capacity-allowing |

---

## Carry-Forward Context

- **Process redesign (M18):** Sprint group isolation (Option E hybrid) + SESSION_STATE.md cockpit card model now active from M18 onward. Full documentation: `docs/process/sprint-group-isolation.md`.
- **Auto-merge protocol (PR #1344):** CLAUDE.md updated — `gh pr merge --auto` replaces polling loop; `gh run watch` for observation. KI-007 filed (GraphQL rate limit). Active from M18.
- **Agent roster (PR #1342/#1343):** Chief Engineer renamed → Computation Engine Agent. DevSecOps Agent (DS) added — owns `.github/`, `.githooks/`, `.gitignore`, sprint isolation process doc.
- **Pre-push hook (PR #1346):** `.githooks/pre-push` active — enforces ruff + mypy (backend) and npm run build (frontend). Install: `git config core.hooksPath .githooks`. EL has installed this locally.
- **Wave concurrency ceiling (PR #1347):** Hard ceiling of 5 concurrent sprint groups per wave. Coordination tier table in `docs/process/sprint-planning-sop.md §Wave Kickoff Coordination Check`. PM Agent runs check before wave kickoff.
- **M17 archive:** Full M1–M17 session state at `docs/process/session-archives/session-state-pre-m18.md`.
