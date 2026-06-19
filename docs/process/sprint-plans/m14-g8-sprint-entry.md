---
name: m14-g8-sprint-entry
type: sprint-entry
milestone: M14 — Methodology Publication and External Validation
sprint-group: G8
status: Filed — awaiting EL approval
authored-by: PM Agent
authored-date: 2026-06-19
el-approved: false
release-branch: release/m14
sop-reference: docs/process/sprint-planning-sop.md
---

# Sprint Entry — M14, G8: Demo 5 Preparation and Live Stakeholder Demo

**Status:** Filed — awaiting EL approval before agent work begins
**Date authored:** 2026-06-19
**Release branch:** `release/m14`
**Sprint plan:** `docs/process/sprint-plans/m14-sprint-plan.md` (EL Approved 2026-06-16)

*Authority: `docs/process/sprint-planning-sop.md §Sprint Entry Gate` (Phase C output).
G8 is the Demo 5 preparation and live stakeholder demo group. It is the M14 closure gate:
M14 does not exit until the live stakeholder session (Step 9) is complete, a stakeholder review
artifact is filed, and the PI Agent confirms all exit conditions are satisfied.*

*G8 is a demo cycle sprint. The governing intent document is
`docs/process/demo-preparation-standard.md`, which specifies all ten preparation steps
with named observable states, artifact paths, and gate conditions. Implementing agent:
PM Agent (orchestrates all agent-scope steps).*

---

## EL Decisions for Demo 5 (recorded 2026-06-19)

| Decision | Value |
|---|---|
| Entity | ZMB only (single entity) |
| Mode 3 | Not in Demo 5 scope |
| Challenge moment | Reserve coverage data challenged by creditor side → analyst responds with Grounding strip citation (source institution, confidence tier, vintage date at zero interaction) |
| #997 constraint status | CLOSED 2026-06-19 — reserve coverage challenge is answered from ADR-016 Grounding strip + ADR-015 Component 1 (L0 basis annotation); no scripted challenge requires Component 4 (composite score decomposition) |

These decisions are binding on all G8 deliverables. The walkthrough script (Step 5),
screenshot brief (Step 2), and Playwright spec (Step 4) must all reflect them.

---

## Section 1 — Sprint Identification

| Field | Value |
|---|---|
| Milestone | M14 — Methodology Publication and External Validation |
| GitHub Milestone | #15 |
| Sprint group | G8 — Demo 5 Preparation and Live Stakeholder Demo |
| Release branch | `release/m14` |
| Sprint plan document | `docs/process/sprint-plans/m14-sprint-plan.md` |
| Exit checklist issue | #968 (closure gate: #843) |
| Primary issue in scope | #843 — live stakeholder demo with real external participants |
| ADR gate | None |
| Implementing agent | PM Agent (all agent-scope steps) |
| Demo prep governing doc | `docs/process/demo-preparation-standard.md` |
| Target version tag | v0.14.0 (to be created by EL at milestone close) |
| DEMO-NNN namespace | Next available: DEMO-097 |

---

## Section 2 — Entry Invariants Checklist

*All items must be checked before any implementation PR is opened for G8.
An unchecked invariant blocks implementation from beginning.*

### 2.1 — Structural gates

- [x] **Release branch exists:** `release/m14` cut from `main` 2026-06-16
- [x] **CI trigger verified:** `.github/workflows/ci.yml` `pull_request: branches` includes
  `release/m*` — confirmed 2026-06-16 (Ruleset ID 17751852; 6 required checks: `changes`,
  `lint`, `test-backend`, `playwright-e2e`, `compliance-scan`, `branch-naming`)
- [x] **Sprint plan EL-approved:** `docs/process/sprint-plans/m14-sprint-plan.md`
  `el-approved: 2026-06-16`
- [x] **All preceding sprint groups complete:** G1 ✅ BPO ACCEPT 2026-06-17; G2 ✅ 2026-06-16;
  G3 ✅ BPO ACCEPT 2026-06-17; G4 ✅ BPO ACCEPT 2026-06-17; G5 ✅ BPO ACCEPT 2026-06-18;
  G6 ✅ BPO ACCEPT 2026-06-18; G6b ✅ BPO ACCEPT 2026-06-18; G6c ✅ BPO ACCEPT + PI confirmed
  2026-06-18; G7 ✅ BPO ACCEPT 2026-06-18. All merged to `release/m14`.

### 2.2 — ADR prerequisite gate

G8 is a demo cycle sprint. No new ADR gates any of its deliverables. ADR-016 (Scenario
Grounding Architecture) and ADR-015 (Evidence Thread Architecture) are both Accepted —
their implementations are the platform capabilities being demonstrated.

| Group | Required ADR | ADR status | Gate |
|---|---|---|---|
| G8 | None | N/A — demo cycle sprint | CLEAR |

- [x] No ADR prerequisite applies to G8. Gate is clear.

### 2.3 — Intent document gate

**Demo cycle sprint — governing intent document is `docs/process/demo-preparation-standard.md`.**

This document specifies all ten preparation steps with named artifact paths, observable
states, and gate conditions. It is the canonical intent document for every demo cycle
sprint. A separate per-sprint intent document would duplicate it. The demo prep standard
was authored and endorsed through M12; it has been used as the governing spec for M6, M8,
M10, and M12 demo cycles. All observable states required to author QA tests (§2.4 below)
are present in the standard.

The EL decisions recorded in the frontmatter of this document (ZMB only, no Mode 3,
reserve coverage challenge moment) augment the standard's general spec with Demo 5–specific
parameters and are the binding design inputs for all G8 deliverables.

- [x] Governing intent document on file: `docs/process/demo-preparation-standard.md`
- [x] Demo 5–specific design decisions locked and recorded in this entry document (above)
- [x] No separate per-sprint intent document required for demo cycle sprints (established
  precedent: M12 G8 demo prep)

| Deliverable class | Governing document | Demo 5–specific parameters | Filed? |
|---|---|---|---|
| All G8 agent-scope deliverables | `docs/process/demo-preparation-standard.md` | ZMB; no Mode 3; reserve coverage challenge → Grounding strip citation | ✅ This document |

### 2.4 — QA test authorship gate

**Demo cycle sprint — QA test pattern differs from feature sprints.**

The demo prep standard specifies two pre-capture quality gates (both existing test files):

1. **`demo-legibility.spec.ts`** (Step 5b gate) — runs against the live application at
   1440×900 before screenshots are captured. Must pass before Step 6 begins. This is the
   primary automated quality gate for G8 observable states.

2. **`demo-narrated.spec.ts`** (Step 4 update) — the narrated Playwright walkthrough spec is
   updated in Step 4 to reflect the ZMB scenario, no Mode 3, and the reserve coverage
   challenge frames. The archived copy (`demo-narrated-m12.spec.ts`) is created in the same
   Step 4 PR. This file is both a G8 deliverable and a test gate — it produces the screenshots
   that feed the review chain (Steps 6b, 7, 6c).

Neither test file is authored from scratch in G8 — both exist and are updated per the
demo prep standard's Step 4 requirements. The Step 5b legibility gate is the QA test
that must pass before any screenshot-dependent artifact is produced.

- [x] QA test gate pattern confirmed for demo cycle sprint

| QA gate | File | Status | Timing |
|---|---|---|---|
| Step 5b — legibility pre-capture | `frontend/tests/e2e/demo-legibility.spec.ts` | Existing — must pass before Step 6 | Before screenshots captured |
| Step 4 — narrated walkthrough spec | `frontend/tests/e2e/demo-narrated.spec.ts` | Existing — updated for ZMB / no Mode 3 / reserve challenge | Step 4 (before Step 6) |

**Step 5d (Mode 3 branch evaluation):** Does NOT apply. EL decision: Mode 3 is not in
Demo 5 scope.

---

## Section 3 — Scope Declaration

### 3.1 — Issue in scope

| Issue | Title | Group | Priority |
|---|---|---|---|
| #843 | plan: M14 closure — live stakeholder demo with real external participants | G8 | immediate — M14 gate issue |

*#968 (M14 Exit Checklist) closes when #843 closes — it is the exit gate issue, not a
separately closable deliverable.*

### 3.2 — G8 deliverables by preparation step

All artifact paths follow the demo prep standard `docs/demo/m14/` folder structure.

| Step | Deliverable | Artifact path | Gate |
|---|---|---|---|
| 1 | Demo preparation GitHub issue | New issue — `demo: M14 stakeholder demo preparation — v0.14.0 / Milestone 14` | Filed before other agent steps begin |
| 2 | Screenshot brief | `docs/demo/m14/screenshot-brief.md` | Before Step 6 |
| 3 | `demo.sh` presenter guide updated (ZMB; no Mode 3; reserve challenge honest disclosure) | `scripts/demo.sh` | `bash -n scripts/demo.sh` exits 0 before commit (NM-041 gate) |
| 4 | Narrated Playwright spec — ZMB scenario, reserve coverage challenge frames, 1440×900 viewport | `frontend/tests/e2e/demo-narrated.spec.ts` (updated); `demo-narrated-m12.spec.ts` (archive) | `__worldsim_selectEntity` app-ready sentinel present (NM-039); viewport confirmed (Issue #675) |
| 5 / 5a / 5b / 5c | Walkthrough script + narration checks + legibility gate + NARRATION-RULING-1 check | `docs/demo/m14/stakeholder-walkthrough.md` | Legibility spec passes; no choropleth quantitative narration; Umbrella + Synthesis + Transition present per step |
| 6 | Screenshots — five frames at 1440×900 | `docs/demo/m14/screenshots/frame-{a–e}-*.png` | Viewport confirmed before capture; five frames match screenshot brief |
| 6b | Internal team review — nine-agent panel | `docs/demo/m14/reviews/YYYY-MM-DD-v0.14.0-internal-review.md` | All CRITICAL findings resolved (a/b/c) and filed as issues; all HIGH findings filed — before Step 7 |
| 7 | IR review — fresh Claude instance | `docs/demo/m14/reviews/YYYY-MM-DD-v0.14.0-ir-review.md` | **GATED: `release/m14` → `main` merge by EL must precede this step** |
| 6c | Audience simulation panel — Personas 1, 2, 5 (+ Persona 3 if PSP featured) | `docs/demo/m14/reviews/YYYY-MM-DD-v0.14.0-audience-simulation.md` | **GATED: Step 7 complete; Persona 5 north star verdict PASS gates Step 9** |
| 8 | DEMO-NNN issue triage; PENDING stakeholder review placeholder | GitHub issues filed; `docs/demo/m14/reviews/PENDING-v0.14.0-stakeholder-review.md` | CRITICAL findings resolved before Step 9; placeholder created |
| 9 | Live stakeholder session + stakeholder review artifact | `docs/demo/m14/reviews/YYYY-MM-DD-v0.14.0-stakeholder-review.md` | **GATED: Persona 5 north star PASS from Step 6c; real external participants present** |
| 9b | Screen recording uploaded to GitHub release | `gh release upload v0.14.x recording.mp4` | Required — M14 is even-numbered; recorded after post-Step-9 fixes merged and main current |

**Persona 3 conditional (Step 6c):** The demo prep standard adds Persona 3 (Andreas
Stefanidis, Political Advisor) when political economy outputs are in scope.
`programme_survival_probability` (PSP) from the political economy module is visible in
Zone 1D in the ZMB scenario. PM Agent includes Persona 3 in the Step 6c panel and notes
whether PSP appears in the walkthrough script before activating the panel.

### 3.3 — Issues explicitly out of scope

| Issue | Horizon | Rationale |
|---|---|---|
| #3 — TSC formation | EL-action | Governance decision; no agent deliverable in G8; G7 produced the draft framework |
| #6 — Branch protection restoration | EL-action | Blocked on #3 Stage 2; no agent deliverable |
| ADR-015 Component 4 — cross-examination mode | M15 | EL decision 2026-06-16; #997 closed confirming Demo 5 does not require it |
| All G1–G7 deliverables | Complete | Merged to `release/m14`; BPO accepted |

---

## Section 4 — ADR Prerequisite Summary

| Group | ADR required | ADR status | Implementation may begin? |
|---|---|---|---|
| G8 | None | N/A — demo cycle sprint | After EL approval of this entry document |

**Implementation sequencing for G8:**

Phase 1 (agent-executable before `release/m14` → `main` merge):
1. EL approves this entry document
2. PM Agent files demo preparation issue (Step 1) — branch `feat/m14-g8-demo5-prep`
3. UX Designer Agent produces screenshot brief (Step 2)
4. PM Agent updates `demo.sh` and validates with `bash -n` (Step 3)
5. PM Agent archives and updates `demo-narrated.spec.ts` for ZMB / no Mode 3 / reserve challenge (Step 4)
6. PM Agent produces walkthrough script; applies narration checks 5a / 5b / 5c (Step 5)
7. PM Agent captures screenshots via `demo.sh --run` (Step 6)
8. PM Agent orchestrates nine-agent internal review panel (Step 6b)
9. All CRITICAL internal review findings resolved; all HIGH findings filed as issues

Phase 2 (gated on EL merge of `release/m14` → `main`):
10. EL merges `release/m14` → `main`
11. IR review via fresh Claude instance (Step 7)
12. Audience simulation panel — Personas 1, 2, 5, (3 conditional) (Step 6c)
13. Persona 5 north star verdict PASS — gates Step 9
14. DEMO-NNN findings triaged and filed (Step 8); PENDING placeholder created
15. EL schedules and runs live stakeholder session with real external participants (Step 9)
16. Stakeholder review artifact completed (Step 9); #843 closed
17. Post-session UI fixes merged to main if needed
18. Screen recording captured and uploaded to GitHub release v0.14.x (Step 9b)
19. SESSION_STATE.md updated; #968 Exit Checklist closed

---

## Section 5 — Near-Miss Sweep

**Near-miss sweep date:** 2026-06-19
**Sweep period:** G7 sprint exit (2026-06-18) through G8 sprint entry filing (2026-06-19)

| Finding | Category | PI Agent register call issued? | NM entry number |
|---|---|---|---|
| None | N/A | N/A | N/A |

*No process gaps identified in the sweep period. All G1–G7 sprint exit documents are filed
and PI-confirmed. Insights log open entry (CLAUDE.md extraction, 2026-06-16) remains open —
will be dispositioned at M14 HORIZON sweep or exit ceremony, not in this sprint.*

---

## EL Approval Record

**EL approval:** Pending

> {EL approval statement — to be filled at approval time}
> — @PublicEnemage ({date})
