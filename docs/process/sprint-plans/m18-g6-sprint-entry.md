---
name: m18-g6-sprint-entry
type: sprint-entry
milestone: M18 — Full Argument and Demo 7
sprint-group: G6
status: Filed — EL verbal authorization on record; awaiting formal EL approval
authored-by: PM Agent
authored-date: 2026-06-28
el-approved: false
release-branch: release/m18
sop-reference: docs/process/sprint-planning-sop.md
---

# Sprint Entry — M18, G6: Demo 7 Preparation and Live Stakeholder Demo

**Status:** Filed — EL verbal authorization on record (see §Process Timing Note);
awaiting formal EL approval before integration PR opens.
**Date authored:** 2026-06-28
**Release branch:** `release/m18`
**Sprint plan:** `docs/process/sprint-plans/m18-sprint-plan.md` (EL Approved 2026-06-26)

*Authority: `docs/process/sprint-planning-sop.md §Sprint Entry Gate` (Phase C output).
G6 is the Demo 7 preparation and live stakeholder demo group. It is the M18 closure gate:
M18 does not exit until the live stakeholder session (Step 9 — #843) is complete, a
stakeholder review artifact is filed, and the PI Agent confirms all exit conditions are satisfied.*

*G6 is a demo cycle sprint. The governing intent document is
`docs/process/demo-preparation-standard.md`, which specifies all preparation steps with
named observable states, artifact paths, and gate conditions. Implementing agent: PM Agent
(orchestrates all agent-scope steps). Two-agent panel: Development Economist + Chief
Methodologist (Step 5d Mode 3 branch configuration evaluation).*

---

## Process Timing Note (Same-Session Disclosure)

**EL verbal authorization preceded sprint entry authorship — disclosed per process integrity.**

The EL directed work to begin with the words "Start with Step 1, and then follow the logical
order you have outlined above" in the same session as this entry was authored. This direction
preceded the filing of this sprint entry document. The following artifacts were produced before
this entry was committed to the repository:

- `docs/demo/m18/stakeholder-walkthrough.md` (Step 5, logical order)
- `docs/demo/m18/screenshot-brief.md` (Step 2, logical order)
- GitHub issue #1445 (Step 1)

**No implementation PR was opened before this entry was filed.** The sprint branch
(`sprint/m18-g6`) and feature branch (`feat/m18-g6-demo7-prep`) were cut in the same session
as this entry, and this entry will be committed in the first PR targeting `sprint/m18-g6`.
The EL's verbal directive functions as the authorization equivalent; this entry formalizes
the scope, artifacts, and gate conditions of that directive.

PI Agent notation: this timing pattern does not require a near-miss entry. The entry gate
rule is triggered by opening an implementation PR before the entry is filed — no PR was
opened. The verbal authorization is on record. The sprint entry is filed before the first
commit to the feature branch. Process compliant.

---

## EL Decisions for Demo 7 (confirmed 2026-06-28)

| Decision | Value |
|---|---|
| Act 1 entity | SEN (Senegal) — Article IV consultation, Mode 3 active control |
| Act 2 entity | ZMB (Zambia) — debt restructuring, three-scenario comparison |
| Act 1 mode | Mode 3 Active Control — `ControlPlaneColumn` Form 1 |
| Act 1 instrument | FiscalMultiplier slider (range 0.1–3.0); demo evaluation range 0.5–2.0 |
| Act 1 question | "Is there a configuration that avoids the bottom quintile crossing the 0.40 floor before step 6?" |
| Act 1 outcome | Both YES and NO are valid findings |
| Act 2 scenarios | Option A (EFF Front-Loaded, IMF-proposed), Option B (EFF Gradual), Option C (Homegrown Programme, reference — last in comparison list) |
| Step 5d | APPLIES — two-agent panel (Development Economist + Chief Methodologist); live simulation required before screenshots |
| Persona 1 (Lucas) | Included in Step 6c — Zone 3 auditability panel is his primary evaluation frame |
| Persona 3 (Andreas) | Included in Step 6c — PSP driver label is his primary evaluation frame |
| ExternalSectorModule | Disclose reserve depletion invariant if SEN scenario uses ESM in Mode 3 (Step 3 mandatory disclosure) |
| DEMO-NNN namespace | Next available: PM Agent checks last assigned number before Step 6b (last known: see DEMO-NNN scan at Step 6b) |

*These decisions are binding on all G6 deliverables. EL verbal confirmation on record 2026-06-28; formal entry approval required before integration PR.*

---

## Section 1 — Sprint Identification

| Field | Value |
|---|---|
| Milestone | M18 — Full Argument and Demo 7 |
| GitHub Milestone | #19 |
| Sprint group | G6 — Demo 7 Preparation and Live Stakeholder Demo |
| Release branch | `release/m18` |
| Sprint plan document | `docs/process/sprint-plans/m18-sprint-plan.md` |
| Exit checklist issue | #1340 (closure gate: #843) |
| Primary issue in scope | #843 — live stakeholder demo with real external participants |
| ADR gate | None |
| Implementing agent | PM Agent (all agent-scope steps); Development Economist + Chief Methodologist (Step 5d) |
| Demo prep governing doc | `docs/process/demo-preparation-standard.md` |
| Target version tag | v0.18.0 (to be created by EL at milestone close) |
| DEMO-NNN namespace | Next available: confirm at Step 6b (last known: DEMO-096, M14; check against M16 and M17 assignments) |
| Wave coordination tier | Standard (Wave 3 sole group — no concurrent sprint groups) |
| Concurrent groups at entry | 0 (G1–G5 all closed at entry) |

---

## Section 2 — Entry Invariants Checklist

*All items must be checked before any implementation PR is opened for G6.
An unchecked invariant blocks the sprint from opening.*

### 2.1 — Structural gates

- [x] **Release branch exists:** `release/m18` cut from `main` 2026-06-26 (commit 151904d)
- [x] **CI trigger verified:** `.github/workflows/ci.yml` `pull_request: branches` includes
  `release/m*` — confirmed at M18 kickoff; sprint-branch-ci-gate Ruleset active on
  `sprint/m*` branches (Node ID `RRS_lACqUmVwb3NpdG9yec5IKi2kzgEV92A`)
- [x] **Sprint plan EL-approved:** `docs/process/sprint-plans/m18-sprint-plan.md`
  `el-approved: 2026-06-26` (PR #1364)
- [x] **G6 gate conditions confirmed — all M18 implementation groups closed at G6 entry:**
  - G1 ✅ Integration PR #1411 MERGED 2026-06-28 (CI bands, #1254)
  - G2 ✅ Integration PR #1408 MERGED 2026-06-28 (PSP driver, #1255)
  - G3 ✅ Integration PR #1417 MERGED 2026-06-28 (counter-scenario comparison, #1349)
  - G4 ✅ Integration PR #1433 MERGED 2026-06-28 (control plane column, #1354)
  - G5 ✅ Integration PR #1443 MERGED 2026-06-28 (Zone 3 auditability, #1422)

### 2.2 — ADR prerequisite gate

G6 is a demo cycle sprint. No new ADR gates any of its deliverables. ADR-019 (Control Plane
Column) is Accepted (PR #1393, 2026-06-27) — its implementation is a primary platform
capability demonstrated in Demo 7 Act 1.

| Group | Required ADR | ADR status | Gate |
|---|---|---|---|
| G6 | None | N/A — demo cycle sprint | CLEAR |

- [x] No ADR prerequisite applies to G6. Gate is clear.

### 2.3 — Intent document gate

**Demo cycle sprint — governing intent document is `docs/process/demo-preparation-standard.md`.**

This document specifies all preparation steps with named artifact paths, observable states,
and gate conditions. It is the canonical intent document for every demo cycle sprint. A
separate per-sprint intent document would duplicate it. The demo prep standard has been used
as the governing spec for M6, M8, M10, M12, M14, and M16 demo cycles. All observable states
required to author QA tests (§2.4 below) are present in the standard.

The EL decisions recorded in this document augment the general spec with Demo 7–specific
parameters and are the binding design inputs for all G6 deliverables.

- [x] Governing intent document on file: `docs/process/demo-preparation-standard.md`
- [x] Demo 7–specific design decisions recorded in this entry (EL verbal confirmation on record 2026-06-28)
- [x] No separate per-sprint intent document required for demo cycle sprints (established precedent: M12, M14, M16 G8 demo prep)

| Deliverable class | Governing document | Demo 7–specific parameters | Filed? |
|---|---|---|---|
| All G6 agent-scope deliverables | `docs/process/demo-preparation-standard.md` | Act 1: SEN Mode 3, FiscalMultiplier evaluation range 0.5–2.0, Step 5d required; Act 2: ZMB three-scenario comparison (A/B/C) | ✅ This document |

### 2.4 — QA test authorship gate

**Demo cycle sprint — QA test pattern differs from feature sprints.**

The demo prep standard specifies pre-capture quality gates (existing test files) plus one
new file in Step 4 (narrated spec update):

1. **`demo-legibility.spec.ts`** (Step 5b gate) — runs against the live application at
   1440×900 before screenshots are captured. **Status: PASS — 16/16 tests pass (2026-06-28).**

2. **`demo-narrated.spec.ts`** (Step 4 update) — the narrated Playwright walkthrough spec
   must be updated to reflect: SEN scenario with Mode 3, Mode2ColumnSurface → ControlPlaneColumn
   transition, five frames (Act 1 Frames A/B/C + Act 2 Frames D/E), 1440×900 viewport, Zambia
   three-scenario setup. Archive: `demo-narrated-m16.spec.ts`. **Step 4 is NOT yet complete —
   spec update is a G6 deliverable.**

3. **`demo-advancement-flow.spec.ts`** (Step 5b gate) — **Status: PASS — all tests pass
   (2026-06-28).**

| QA gate | File | Status | Timing |
|---|---|---|---|
| Step 5b — legibility pre-capture | `frontend/tests/e2e/demo-legibility.spec.ts` | ✅ PASS 16/16 — 2026-06-28 | Before screenshots captured |
| Step 5b — advancement flow | `frontend/tests/e2e/demo-advancement-flow.spec.ts` | ✅ PASS — 2026-06-28 | Before screenshots captured |
| Step 4 — narrated walkthrough spec | `frontend/tests/e2e/demo-narrated.spec.ts` | ⏳ Pending — G6 deliverable; archive `demo-narrated-m16.spec.ts` | Step 4 (before Step 6) |

**Step 5d (Mode 3 branch evaluation): APPLIES.** Demo 7 Act 1 uses Mode 3. The two-agent
panel (Development Economist + Chief Methodologist) must evaluate live simulation output at
candidate FiscalMultiplier configurations from the demo evaluation range (0.5–2.0) and file:
- Deliberation: `docs/demo/m18/reviews/scenario-evaluation-mode3-deliberation.md`
- Recommendation: `docs/demo/m18/reviews/scenario-evaluation-mode3-recommendation.md`

This is gated on EL activation of the panel. Filed before screenshots (Step 6) are captured.

### 2.5 — Prior NM verification (§6.5 of sprint entry template)

*Checklist of prior NMs relevant to this sprint type, confirmed resolved or documented.*

| NM | Title | Relevance to G6 | Status |
|---|---|---|---|
| NM-032 | Demo screenshots captured at 1280×720 — mismatches 1440×900 legibility gate | Viewport gate in `demo-narrated.spec.ts` Step 4 | ✅ Resolved — `page.setViewportSize({ width: 1440, height: 900 })` required before first `page.goto()` |
| NM-039 | App-ready sentinel missing from demo spec | `__worldsim_selectEntity` sentinel in Step 4 spec | ✅ Resolved — sentinel required in all demo specs from M14 forward |
| NM-041 | demo.sh syntax error made startup sequence inaccessible | `bash -n scripts/demo.sh` gate in Step 3 | ✅ Resolved — syntax validation gate active; confirmed PASS 2026-06-28 |
| NM-061 | Setup completeness audit: QA tests checking UI state must set it via API AND UI | Applies to `demo-narrated.spec.ts` Step 4 spec authorship | ✅ Documented — QA Lead working agreement updated (PR #1221); must apply NM-061 audit before `demo-narrated.spec.ts` update |
| NM-076 | testid rename not crosschecked against E2E corpus | Applies if Step 4 spec introduces new testids | ✅ Rule in CODING_STANDARDS.md (PR #1439) — apply crosscheck before Step 4 PR |

### 2.6 — Pre-checks for G6

| Pre-check | Expected result | Result |
|---|---|---|
| `docs/demo/m18/` directory exists | `stakeholder-walkthrough.md`, `screenshot-brief.md`, `screenshots/`, `reviews/` present | ✅ Confirmed — created 2026-06-28 (this session) |
| `demo.sh --milestone 18` renders without error | Presenter guide prints; stack starts | ✅ PASS — confirmed 2026-06-28 |
| Step 5a UX-RULING-4 check | No choropleth quantitative narration in walkthrough | ✅ PASS — no violations found 2026-06-28 |
| Step 5b legibility gate (1440×900) | 16/16 tests pass | ✅ PASS — 2026-06-28 |
| Step 5c NARRATION-RULING-1 check | All 5 Section 2 steps: Umbrella + Synthesis + Transition present | ✅ PASS — 2026-06-28 |
| Step 5d panel activated | Development Economist + Chief Methodologist two-agent panel running | ⏳ PENDING — EL activated 2026-06-28; panel in progress |
| DEMO-NNN namespace scan | Last assigned DEMO-NNN known before Step 6b begins | ⏳ Pending — to be confirmed at Step 6b |

---

## Section 3 — Scope Declaration

### 3.1 — Issues in scope

| Issue | Title | Group | Priority |
|---|---|---|---|
| #843 | plan: Demo 7 — live stakeholder demo with real external participants | G6 | immediate — M18 gate issue |
| #1445 | demo: M18 stakeholder demo preparation — v0.18.0 / Milestone 18 | G6 | immediate |

*#1340 (M18 Exit Checklist) closes when #843 closes — it is the exit gate issue, not a
separately closable deliverable.*

### 3.2 — G6 deliverables by preparation step (logical order)

All artifact paths follow the demo prep standard `docs/demo/m18/` folder structure.

| Step | Deliverable | Artifact path | Gate | Status |
|---|---|---|---|---|
| 1 | Demo preparation GitHub issue | #1445 | Filed before other agent steps | ✅ DONE |
| 5 | Walkthrough script | `docs/demo/m18/stakeholder-walkthrough.md` | Section 2 narration + Honest Disclosures + Section 4 roadmap complete | ✅ DONE (2026-06-28) |
| 3 | Verify `demo.sh --milestone 18` renders | `scripts/demo.sh` (no edits) | `bash -n` passes; walkthrough file found; presenter guide prints | ✅ DONE |
| 5a | Narration instrument check | `docs/demo/m18/stakeholder-walkthrough.md` | UX-RULING-4: no choropleth quantitative narration | ✅ PASS |
| 5b | Legibility gate at 1440×900 | `demo-legibility.spec.ts` + `demo-advancement-flow.spec.ts` | Both pass before screenshots | ✅ PASS 16/16 |
| 5c | Narration structure self-check | `docs/demo/m18/stakeholder-walkthrough.md` | NARRATION-RULING-1: Umbrella + Synthesis + Transitions | ✅ PASS |
| 5d | Mode 3 branch configuration evaluation | `docs/demo/m18/reviews/scenario-evaluation-mode3-deliberation.md` + `scenario-evaluation-mode3-recommendation.md` | Two-agent panel PASS before screenshots | ⏳ IN PROGRESS |
| 2 | Screenshot brief | `docs/demo/m18/screenshot-brief.md` | Five frames specified; Step 5d TBD for Frame A step/multiplier | ✅ DONE (pending Step 5d confirmation) |
| 4 | Archive and update narrated Playwright spec | `frontend/tests/e2e/demo-narrated.spec.ts` (updated); `demo-narrated-m16.spec.ts` (archive) | Two-act SEN+ZMB; Mode 3 transition; five frames; 1440×900; NM-061 audit applied | ⏳ PENDING |
| 6 | Screenshots — five frames at 1440×900 | `docs/demo/m18/screenshots/frame-{a–e}-*.png` | Viewport confirmed; Step 5d complete; five frames match brief | ⏳ PENDING |
| 6b | Internal team review — nine-agent panel (incl. Customer Agent solo-use gate) | `docs/demo/m18/reviews/YYYY-MM-DD-v0.18.0-internal-review.md` | All CRITICAL findings resolved; all HIGH findings filed | ⏳ PENDING |
| 7 | IR review — fresh Claude instance | `docs/demo/m18/reviews/YYYY-MM-DD-v0.18.0-ir-review.md` | **GATED: `release/m18` → `main` merge by EL must precede this step** | ⏳ PENDING |
| 6c | Audience simulation panel — Personas 1, 2, 5, 3 | `docs/demo/m18/reviews/YYYY-MM-DD-v0.18.0-audience-simulation.md` | **GATED: Step 7 complete; Persona 5 north star verdict PASS gates Step 9** | ⏳ PENDING |
| 8 | DEMO-NNN issue triage; PENDING stakeholder review placeholder | GitHub issues; `docs/demo/m18/reviews/PENDING-v0.18.0-stakeholder-review.md` | CRITICAL findings resolved before Step 9; placeholder filed; GitHub release page check | ⏳ PENDING |
| 9 | Live stakeholder session + stakeholder review artifact | `docs/demo/m18/reviews/YYYY-MM-DD-v0.18.0-stakeholder-review.md` | **GATED: Persona 5 north star PASS from Step 6c; real external participants present** | ⏳ PENDING — #843 gate |
| 9b | Screen recording uploaded to GitHub release | `gh release upload v0.18.0 recording.mp4` | Required — M18 is even-numbered | ⏳ PENDING |

---

## Section 4 — Prior NM Open Items

No open near-miss entries block G6 entry.

---

## Section 5 — Sprint Branch

| Field | Value |
|---|---|
| Sprint sub-branch | `sprint/m18-g6` — cut from `release/m18` 2026-06-28 |
| Feature branch | `feat/m18-g6-demo7-prep` — cut from `sprint/m18-g6` 2026-06-28 |
| First PR target | `sprint/m18-g6` |
| Integration PR target | `release/m18` |

---

## Section 6 — Customer Agent and North Star

| Field | Value |
|---|---|
| Customer Agent L3 required | Yes — Persona 5 (Aicha, Finance Minister) north star PASS required at Step 6c before live session. Persona 1 (Lucas) Zone 3 auditability assessment also required. |
| North star test | Authored by Business PO at sprint exit; specific Zambia counter-proposal scenario naming the finance minister scenario, the capability evaluated, and whether the 340,000 differential changes what the ministry team can argue at the table. |
| Serves Personas | 2 (Eleni — Finance Ministry Negotiator), 5 (Aicha — Finance Minister), 1 (Lucas — Analytical Economist), 3 (Andreas — Political Advisor) |

---

*Sprint entry authored by PM Agent, 2026-06-28. Process timing note: see §Process Timing Note above.*
*Sprint plan: `docs/process/sprint-plans/m18-sprint-plan.md`. EL approval required before integration PR.*
