---
name: m16-g8-sprint-entry
type: sprint-entry
milestone: M16 — Distributional Visibility
sprint-group: G8
status: Filed and EL Approved — 2026-06-24
authored-by: PM Agent
authored-date: 2026-06-24
el-approved: 2026-06-24
release-branch: release/m16
sop-reference: docs/process/sprint-planning-sop.md
---

# Sprint Entry — M16, G8: Demo 6 Preparation and Live Stakeholder Demo

**Status:** Filed — awaiting EL approval before agent work begins
**Date authored:** 2026-06-24
**Release branch:** `release/m16`
**Sprint plan:** `docs/process/sprint-plans/m16-sprint-plan.md` (EL Approved 2026-06-23)

*Authority: `docs/process/sprint-planning-sop.md §Sprint Entry Gate` (Phase C output).
G8 is the Demo 6 preparation and live stakeholder demo group. It is the M16 closure gate:
M16 does not exit until the live stakeholder session (Step 9) is complete, a stakeholder
review artifact is filed, and the PI Agent confirms all exit conditions are satisfied.*

*G8 is a demo cycle sprint. The governing intent document is
`docs/process/demo-preparation-standard.md`, which specifies all preparation steps with
named observable states, artifact paths, and gate conditions. Implementing agent:
PM Agent (orchestrates all agent-scope steps).*

---

## EL Decisions for Demo 6 (confirmed 2026-06-24)

| Decision | Value |
|---|---|
| Entity | SEN (Senegal) — distributional human cost argument |
| Mode 3 | Not in Demo 6 scope (Step 5d does NOT apply) |
| Demo 6 primary argument | "This cohort, at this step, for this long" — bottom-quintile threshold crossing at step 2; 25-year human capital trajectory; PSP trajectory with plain-language interpretation — all visible in the primary viewport without drawer navigation |
| Challenge moment | Cohort distribution methodology challenged by creditor side → analyst responds with confidence tier T3 Inferred, synthetic flag visible, demographic weight source (ECOWAS comparable economy weighting) |
| Persona 3 inclusion (Step 6c) | YES (confirmed) — Andreas Stefanidis included; Zone 1D political risk section (#987) is his primary frame; PSP severity label + plain-language interpretation are the Demo 6 capability Andreas evaluates |
| Step 5b additional gate | Before Step 6 screenshots: verify SEN 100-step scenario produces bottom-quintile threshold crossing at step 2 AND milestone sentence reads with calendar year anchor (not step reference as primary) — see §2.5 pre-checks |

*These decisions are binding on all G8 deliverables. Confirmed by EL 2026-06-24.*

---

## Section 1 — Sprint Identification

| Field | Value |
|---|---|
| Milestone | M16 — Distributional Visibility |
| GitHub Milestone | #17 |
| Sprint group | G8 — Demo 6 Preparation and Live Stakeholder Demo |
| Release branch | `release/m16` |
| Sprint plan document | `docs/process/sprint-plans/m16-sprint-plan.md` |
| Exit checklist issue | #985 (closure gate: #843) |
| Primary issue in scope | #843 — live stakeholder demo with real external participants |
| ADR gate | None |
| Implementing agent | PM Agent (all agent-scope steps) |
| Demo prep governing doc | `docs/process/demo-preparation-standard.md` |
| Target version tag | v0.16.0 (to be created by EL at milestone close) |
| DEMO-NNN namespace | Next available: PM Agent checks last assigned DEMO-NNN before Step 6b aggregation |

---

## Section 2 — Entry Invariants Checklist

*All items must be checked before any implementation PR is opened for G8.
An unchecked invariant blocks implementation from beginning.*

### 2.1 — Structural gates

- [x] **Release branch exists:** `release/m16` cut from `main` 2026-06-23 (commit 07c92b8)
- [x] **CI trigger verified:** `.github/workflows/ci.yml` `pull_request: branches` includes
  `release/m*` — confirmed at M16 kickoff (Ruleset — 6 required checks: `changes`,
  `lint`, `test-backend`, `playwright-e2e`, `compliance-scan`, `branch-naming`)
- [x] **Sprint plan EL-approved:** `docs/process/sprint-plans/m16-sprint-plan.md`
  `el-approved: 2026-06-23` (PR #1148)
- [x] **G8 gate conditions confirmed — all cleared 2026-06-24:**
  - G1 ✅ BPO ACCEPT 2026-06-23 (#845 + #1147; PR #1160)
  - G2 ✅ BPO ACCEPT 2026-06-24 (#986 + #987 + #1163; PR #1173)
  - G3 ✅ BPO ACCEPT 2026-06-24 (#274; PR #1172)
  - G4 ✅ BPO ACCEPT 2026-06-24 (#22 + #102 + #275; PRs #1182/#1187/#1190)
  - G10 ✅ BPO ACCEPT 2026-06-24 (#1162/#1177/#1178/#1179/#1184; PR #1199; fresh-session)
  - G6 ✅ Infrastructure validation COMPLETE 2026-06-24 (VC-1–VC-4 PASS; MV-002 50.5ms PASS)

### 2.2 — ADR prerequisite gate

G8 is a demo cycle sprint. No new ADR gates any of its deliverables. ADR-017 (Zone 1A
Information Architecture), ADR-016 (Scenario Grounding Architecture), ADR-015 (Evidence
Thread Architecture) are all Accepted — their implementations are the platform capabilities
being demonstrated in Demo 6.

| Group | Required ADR | ADR status | Gate |
|---|---|---|---|
| G8 | None | N/A — demo cycle sprint | CLEAR |

- [x] No ADR prerequisite applies to G8. Gate is clear.

### 2.3 — Intent document gate

**Demo cycle sprint — governing intent document is `docs/process/demo-preparation-standard.md`.**

This document specifies all preparation steps with named artifact paths, observable states,
and gate conditions. It is the canonical intent document for every demo cycle sprint. A
separate per-sprint intent document would duplicate it. The demo prep standard has been used
as the governing spec for M6, M8, M10, M12, and M14 demo cycles. All observable states
required to author QA tests (§2.4 below) are present in the standard.

The EL decisions recorded in this document augment the general spec with Demo 6–specific
parameters and are the binding design inputs for all G8 deliverables.

- [x] Governing intent document on file: `docs/process/demo-preparation-standard.md`
- [x] Demo 6–specific design decisions recorded in this entry document (pending EL confirmation at approval)
- [x] No separate per-sprint intent document required for demo cycle sprints (established precedent: M12 and M14 G8 demo prep)

| Deliverable class | Governing document | Demo 6–specific parameters | Filed? |
|---|---|---|---|
| All G8 agent-scope deliverables | `docs/process/demo-preparation-standard.md` | SEN; no Mode 3; distributional human cost argument; cohort bottom-quintile + 25-year trajectory + PSP | ✅ This document |

### 2.4 — QA test authorship gate

**Demo cycle sprint — QA test pattern differs from feature sprints.**

The demo prep standard specifies two pre-capture quality gates (both existing test files):

1. **`demo-legibility.spec.ts`** (Step 5b gate) — runs against the live application at
   1440×900 before screenshots are captured. Must pass before Step 6 begins. This is the
   primary automated quality gate for G8 observable states.

2. **`demo-narrated.spec.ts`** (Step 4 update) — the narrated Playwright walkthrough spec is
   updated in Step 4 to reflect the SEN scenario, no Mode 3, and the Demo 6 argument frames.
   The archived copy (`demo-narrated-m14.spec.ts`) is created in the same Step 4 PR. This
   file is both a G8 deliverable and a test gate — it produces the screenshots that feed
   the review chain (Steps 6b, 7, 6c).

Neither test file is authored from scratch in G8 — both exist and are updated per the demo
prep standard's Step 4 requirements. The Step 5b legibility gate is the QA test that must
pass before any screenshot-dependent artifact is produced.

- [x] QA test gate pattern confirmed for demo cycle sprint

| QA gate | File | Status | Timing |
|---|---|---|---|
| Step 5b — legibility pre-capture | `frontend/tests/e2e/demo-legibility.spec.ts` | Existing — must pass before Step 6 | Before screenshots captured |
| Step 4 — narrated walkthrough spec | `frontend/tests/e2e/demo-narrated.spec.ts` | Existing — updated for SEN / no Mode 3 / distributional frames | Step 4 (before Step 6) |

**Step 5d (Mode 3 branch evaluation):** Does NOT apply. EL decision: Mode 3 is not in
Demo 6 scope.

**NM-061 setup completeness audit (mandatory — NM-061 process improvement):** Before
updating `demo-narrated.spec.ts`, the QA Lead audit step (added to `docs/process/agents.md`)
must be applied: identify any test that creates scenario or entity data via direct `fetch`
API calls AND then checks for conditional UI component visibility. For each such test,
verify the setup satisfies the component render condition through the UI — not just through
API state. The `HumanCapitalTrajectoryPanel` requires `activeScenarioDetail?.configuration?.projection_steps > 8` — the SEN 100-step scenario must be UI-selected before the panel check.
Reference: NM-061 (`docs/process/near-miss-registry.md`); fix in PR #1221.

**AC-F1–F7 soft-skip note (#1220):** The broader G3 spec soft-skip gap (NM-061 family, AC-F1–AC-F7) is tracked as #1220. That issue is not in G8 scope — it requires a separate sprint entry. G8 is not blocked by it: the Demo 6 narrated spec is distinct from the G3 acceptance spec. The legibility gate (Step 5b) provides the automated quality coverage for the demo walkthrough.

### 2.5 — Pre-checks for G8

The following named pre-conditions must be verified at sprint entry before any G8 demo artifacts are created. PI Agent records the result of each check before G8 implementation begins.

| Pre-check | Expected result | Result |
|---|---|---|
| Demo 6 stubs exist at canonical paths | `docs/demo/m16/stakeholder-walkthrough.md` and `docs/demo/m16/screenshot-brief.md` both exist as stubs | Confirmed — stubs created at G5 (PR #1156 2026-06-23) |
| `demo.sh --milestone 16` runs without error | Script exits without file-not-found warning | Verify at Step 3 after walkthrough is complete |
| NM-061 audit step added to agents.md | QA Lead working agreement includes setup completeness audit | Confirmed — PR #1221 merged 2026-06-24 |
| DEMO-NNN namespace current number | Last assigned DEMO-NNN number is known before Step 6b | To check at Step 6b; last known: DEMO-096 (M14 audience simulation) |
| Step 2 threshold crossing (EL 2026-06-24) | SEN 100-step quarterly scenario produces Q1 cohort poverty headcount ≥ 0.40 at step 2 — bottom-quintile threshold crossing is the Demo 6 thesis frame | Verify before Step 6 by running `demo-narrated.spec.ts` and checking the scenario state; calibrate initial attributes if step 2 crossing is not achieved |
| Milestone sentence calendar year anchor (EL 2026-06-24) | Milestone sentence in `HumanCapitalTrajectoryPanel` reads with 4-digit calendar year as the primary element — not "[step N]" as primary (G10/#1177 fix confirmed this; verify with SEN demo scenario specifically) | Verify during Step 5b legibility gate against the live scenario |

**Step 5b additional gate criteria (EL 2026-06-24 addition):**

Before capturing screenshots in Step 6:
1. Run the SEN demo scenario with `projection_steps=100` and advance to step 2
2. Confirm Zone 1B cohort impact section shows Q1 informal workers poverty headcount at or above the recovery floor (0.40) — the bottom-quintile threshold crossing that is the Demo 6 thesis frame
3. Confirm `projection-milestone-sentence` text leads with `"by [YYYY]"` format — calendar year anchor is prominent; "[step N]" is secondary
4. If step 2 crossing is not achieved, adjust SEN initial `poverty_headcount_ratio` upward (toward 0.39) and re-run before proceeding to screenshots

These are scenario-calibration verification steps, not new automated test assertions. They are manual checks in the `demo-narrated.spec.ts` run (Step 4 outputs the scenario and the PM Agent reads the state).

---

## Section 3 — Scope Declaration

### 3.1 — Issue in scope

| Issue | Title | Group | Priority |
|---|---|---|---|
| #843 | plan: live stakeholder demo with real external participants | G8 | immediate — M16 gate issue |

*#985 (M16 Exit Checklist) closes when #843 closes — it is the exit gate issue, not a
separately closable deliverable.*

### 3.2 — G8 deliverables by preparation step

All artifact paths follow the demo prep standard `docs/demo/m16/` folder structure.

| Step | Deliverable | Artifact path | Gate |
|---|---|---|---|
| 1 | Demo preparation GitHub issue | New issue — `demo: M16 stakeholder demo preparation — v0.16.0 / Milestone 16` | Filed before other agent steps begin |
| 2 | Screenshot brief | `docs/demo/m16/screenshot-brief.md` (complete — stub exists) | Before Step 6 |
| 3 | Verify `demo.sh --milestone 16` renders without error | `scripts/demo.sh` (config-driven; no edits required per #837) | `bash -n scripts/demo.sh` exits 0; `demo.sh --milestone 16` finds walkthrough file |
| 5 | Complete walkthrough script | `docs/demo/m16/stakeholder-walkthrough.md` (complete — stub exists) | Section 2 narration + Honest Disclosures + Section 4 roadmap; legibility spec passes; no choropleth quantitative narration; Umbrella + Synthesis + Transition present per step |
| 4 | Archive and update narrated Playwright spec — SEN scenario, distributional + 25-year trajectory + PSP frames, 1440×900 viewport | `frontend/tests/e2e/demo-narrated.spec.ts` (updated); `demo-narrated-m14.spec.ts` (archive) | `__worldsim_selectEntity` app-ready sentinel present (NM-039); viewport confirmed (Issue #675); NM-061 setup audit applied |
| 5a | Narration instrument check | `docs/demo/m16/stakeholder-walkthrough.md` | No choropleth quantitative narration (UX-RULING-4) |
| 5b | Legibility validation at 1440×900 | `frontend/tests/e2e/demo-legibility.spec.ts` + `demo-advancement-flow.spec.ts` | Both pass before screenshots captured |
| 5c | Narration structure self-check | `docs/demo/m16/stakeholder-walkthrough.md` | Umbrella + Synthesis + Transitions present per step (NARRATION-RULING-1) |
| 6 | Screenshots — five frames at 1440×900 | `docs/demo/m16/screenshots/frame-{a–e}-*.png` | Viewport confirmed before capture; five frames match screenshot brief |
| 6b | Internal team review — nine-agent panel (incl. Customer Agent solo-use gate #951) | `docs/demo/m16/reviews/YYYY-MM-DD-v0.16.0-internal-review.md` | All CRITICAL findings resolved (a/b/c) and filed as issues; all HIGH findings filed — before Step 7 |
| 7 | IR review — fresh Claude instance | `docs/demo/m16/reviews/YYYY-MM-DD-v0.16.0-ir-review.md` | **GATED: `release/m16` → `main` merge by EL must precede this step** |
| 6c | Audience simulation panel — Personas 1, 2, 5 (+ Persona 3 — conditional on PSP walkthrough inclusion) | `docs/demo/m16/reviews/YYYY-MM-DD-v0.16.0-audience-simulation.md` | **GATED: Step 7 complete; Persona 5 north star verdict PASS gates Step 9** |
| 8 | DEMO-NNN issue triage; PENDING stakeholder review placeholder | GitHub issues filed; `docs/demo/m16/reviews/PENDING-v0.16.0-stakeholder-review.md` | CRITICAL findings resolved before Step 9; placeholder created; GitHub release page completeness check |
| 9 | Live stakeholder session + stakeholder review artifact | `docs/demo/m16/reviews/YYYY-MM-DD-v0.16.0-stakeholder-review.md` | **GATED: Persona 5 north star PASS from Step 6c; real external participants present** |
| 9b | Screen recording uploaded to GitHub release | `gh release upload v0.16.x recording.mp4` | Required — M16 is even-numbered; recorded after post-Step-9 fixes merged and main current |

**Step order note:** The demo prep standard numbers Step 3 (walkthrough) before Step 4
(Playwright spec) and Step 5 (self-checks). The order here follows the standard's logic:
walkthrough is authored (Step 5 in standard = Step 3+5 above), then spec is updated to
match the walkthrough's frames (Step 4 in standard). The stub at
`docs/demo/m16/stakeholder-walkthrough.md` was created at G5 — completing it is the
first substantive agent action in G8.

**Persona 3 conditional (Step 6c):** Andreas Stefanidis (Political Advisor) is included
when the demo features governance or political economy outputs. Demo 6 includes the political
risk summary surface (#987, Zone 1D) and PSP trajectory — both directly relevant to Andreas.
Preliminary EL decision: Persona 3 is included. Final confirmation at EL approval of this
entry document.

### 3.3 — Issues explicitly out of scope

| Issue | Horizon | Rationale |
|---|---|---|
| #1220 — G3 spec AC-F1–F7 soft-skip | M17 | Separate sprint entry required; does not gate G8 or Demo 6 legibility |
| #1217 — Mode 3 render optimization | Before M17 exit | EX-001 tracking; G8 not blocked |
| #3, #6 — Governance (G7) | Parking Lot | EL decision 2026-06-24; deferred to GitHub Milestone #20 |
| All G1–G6/G9/G10 deliverables | Complete | Merged to `release/m16`; BPO accepted |

---

## Section 4 — ADR Prerequisite Summary

| Group | ADR required | ADR status | Implementation may begin? |
|---|---|---|---|
| G8 | None | N/A — demo cycle sprint | After EL approval of this entry document |

**Implementation sequencing for G8:**

Phase 1 (agent-executable before `release/m16` → `main` merge):
1. EL approves this entry document
2. PM Agent files demo preparation issue (Step 1) — branch `feat/m16-g8-demo6-prep`
3. UX Designer Agent produces screenshot brief (Step 2) — completing stub at `docs/demo/m16/screenshot-brief.md`
4. PM Agent completes walkthrough script (Steps 3 + 5) — completing stub at `docs/demo/m16/stakeholder-walkthrough.md`; verifies `demo.sh --milestone 16` renders
5. PM Agent archives and updates `demo-narrated.spec.ts` for SEN / no Mode 3 / distributional frames (Step 4); NM-061 audit applied
6. PM Agent applies narration checks 5a / 5b / 5c (Steps 5a–5c)
7. PM Agent captures screenshots via `demo.sh --run` (Step 6)
8. PM Agent orchestrates nine-agent internal review panel, including Customer Agent solo-use evaluation (Step 6b)
9. All CRITICAL internal review findings resolved; all HIGH findings filed as issues

Phase 2 (gated on EL merge of `release/m16` → `main`):
10. EL merges `release/m16` → `main` (mid-milestone sync or final merge at M16 close)
11. IR review via fresh Claude instance (Step 7)
12. Audience simulation panel — Personas 1, 2, 5, 3 (Step 6c)
13. Persona 5 north star verdict PASS — gates Step 9; also serves as sprint-level north star test artifact
14. DEMO-NNN findings triaged and filed (Step 8); PENDING placeholder created; GitHub release page completeness check
15. EL schedules and runs live stakeholder session with real external participants (Step 9)
16. Stakeholder review artifact completed (Step 9); #843 closed
17. Post-session UI fixes merged to main if needed
18. Screen recording captured and uploaded to GitHub release v0.16.x (Step 9b)
19. SESSION_STATE.md updated; #985 Exit Checklist closed

---

## Section 5 — Near-Miss Sweep

**Near-miss sweep date:** 2026-06-24
**Sweep period:** G6 sprint exit (2026-06-24) through G8 sprint entry filing (2026-06-24)

| Finding | Category | PI Agent register call issued? | NM entry number |
|---|---|---|---|
| NM-061 — AC-F8 silent no-op since G3 | Process: E2E setup gap | Yes — filed PR #1221 | NM-061 |

*NM-061 was filed during G6 exit review and carries forward as the primary process improvement
entering G8. The G8 QA gate (§2.4) requires the NM-061 audit step be applied to any new
conditional-render test in `demo-narrated.spec.ts`. No additional near-misses identified in
the sweep period.*

**Insights log review:** `docs/insights-log.md` reviewed at sweep time. No open entries
identified that require disposition at G8 sprint entry. (Last HORIZON sweep 2026-06-23
dispositioned the single open entry to #1145.)

---

## EL Approval Record

**EL approval:** 2026-06-24

> G8 sprint entry approved. Design decisions confirmed: entity SEN; no Mode 3; challenge moment
> is cohort distribution methodology → T3 Inferred response; Persona 3 (Andreas) included in
> Step 6c for Zone 1D political risk frame. Additional Step 5b gate: verify SEN step-2 Q1
> threshold crossing and milestone sentence calendar year anchor before screenshots.
> Demo prep issue #1225 to be filed.
> — @PublicEnemage (2026-06-24)
