# WorldSim Session State

> This file is maintained by Claude Code. It is updated at the end of
> every session as the last action before closing. Do not edit manually.
> Engineering Lead decisions and context are recorded here for session
> continuity. For permanent rules and architecture, see CLAUDE.md.

**Last updated:** 2026-05-19 (Issue #361 Chief Methodologist consultation complete — synthetic-data-consultation.md, five questions answered, ADR-007 outline produced)
**Current milestone:** M8 → M9 transition — design foundation sequence in progress

---

## Active Work Streams

| Stream | Issues | Status | Gate |
|---|---|---|---|
| ADR-005 Amendment 3 | #218 ✅ | Merged ✅ (PR #309) | None |
| Greece fixture extension | #284 ✅ #316 ✅ | Merged ✅ (PR #321) | None |
| EcologicalModule expansion | #312 ✅ #313 ✅ #314 ✅ | Merged ✅ (PR #324) | None |
| UI/UX — Area 1 (null governance axis) | #315 ✅ | Merged ✅ (PR #323) | None |
| UI/UX — Areas 2, 3, 4, 5 | #317 ✅ #318 ✅ #319 ✅ #320 ✅ | Merged ✅ (PR #329) | None |
| Demo scenario assembly | #269 ✅ | Merged ✅ (PR #328) | None |
| Intent block retrofit | #287 ✅ | Merged ✅ (PR #291) | None |
| Frontend Architect M8 brief | #298 ✅ | Merged ✅ (PR #307) | None |

**M8 is feature-complete.** All eight work streams closed. Remaining open items are Near-Term horizon.

## Design Foundation Sequence — M9 Gate (Issues #359–#370)

Twelve issues filed 2026-05-19. Must complete before M9 UX implementation begins.

**Step 1 — Immediate (unblocked, runs first):**

| Issue | Title | Milestone | Blocks |
|---|---|---|---|
| #359 | CLAUDE.md structural refactor | M9 | #360 #361 #362 #363 |
| #370 | M8 formal close — retrospective, compliance scan, #209 | M8 | v0.8.0 tag, M9 kickoff |

**Step 2 — Immediate (unblocked after #359):**

| Issue | Title | Milestone | Blocks |
|---|---|---|---|
| #360 | Agent working agreements (15 agents) | M9 | #369 |
| #361 | Synthetic data framework — Chief Methodologist + ADR | M9 | #362 |

**Step 3 — Immediate (requires #359 + #360 + #361):**

| Issue | Title | Milestone | Blocks |
|---|---|---|---|
| #362 | User persona document (5 personas, marquee cases) | M9 | #363 #367 |

**Step 4 — Immediate (requires #359 + #362):**

| Issue | Title | Milestone | Blocks |
|---|---|---|---|
| #363 | UX first-principles depth — close six gaps | M9 | #364 |

**Step 5 — Near-Term (sequential from here):**

| Issue | Title | Milestone | Blocks |
|---|---|---|---|
| #364 | EL decisions — north-star, viewport, comparison mode | M9 | #365 |
| #365 | UX document updates (north-star, info-hierarchy, journeys) | M9 | #366 #368 |
| #366 | Trajectory view ADR | M9 | M9 Frontend Architect brief |
| #367 | Persona-anchored IR review re-run (Persona 2) | M9 | #368 |
| #368 | DEMO issues re-triage #342–#350 | M9 | M9 DEMO sprint scope |
| #369 | agent-raci.md — RACI chart for all 15 agents | M9 | Agent governance docs |

---

## Open PRs

| PR | Title | Date |
|---|---|---|
| #356 | docs(ux): M8 interaction model critique — panel synthesis (UX Designer, Dev Economist, Chief Methodologist) | 2026-05-18 |
| #371 | chore(state): design foundation sequence — 12 issues #359–#370 filed | 2026-05-19 |
| #372 | docs(claude): CLAUDE.md structural refactor — closes #359 | 2026-05-19 |

## Recently Merged PRs (last 5)

| PR | Title | Date |
|---|---|---|
| #355 | docs(ux): M8 interaction model critique — UX Design Thinking Agent first activation (closes #353) | 2026-05-18 |
| #354 | docs(process): add UX Design Thinking Agent to agents.md (closes #353) | 2026-05-18 |
| #352 | chore(state): update SESSION_STATE.md — PR #351 open (IR issues #342–#350 + M8 walkthrough) | 2026-05-18 |
| #351 | docs(demo): M8 IR review issues filed (#342–#350) + M8 stakeholder walkthrough | 2026-05-18 |
| #340 | fix(demo): three demo polish fixes + M8 IR Agent stakeholder review | 2026-05-18 |
| #339 | docs(demo): M8 demo — updated demo.sh, narrated spec, five screenshots captured (closes #233) | 2026-05-18 |
| #338 | chore(demo): switch TTS voice to Zoe (Enhanced) | 2026-05-18 |
| #336 | fix(dev): Python 3.12 Docker image rebuild — startup version guard, CONTRIBUTING docs | 2026-05-18 |
| #335 | chore(state): SESSION_STATE.md update — PR #334 merged, demo prep standard, board cleanup | 2026-05-18 |

---

## Open Issues — M8 Horizon:Immediate

All Horizon:Immediate issues are now closed. M8 feature-complete.

| Issue | Title | Status |
|---|---|---|
| #269 | Demo scenario — Greece 2010–2015 | Closed ✅ — merged PR #328 |
| #317 | Indicator display name mapping layer | Closed ✅ — merged PR #329 |
| #318 | Mandatory ecological note → Zone 3 expandable | Closed ✅ — merged PR #329 |
| #319 | Radar chart transition animation | Closed ✅ — merged PR #329 |
| #320 | Coffin Corner / PMM Zone 1 widget | Closed ✅ — merged PR #329 |

---

## Open Issues — M8 Horizon:Near-Term

| Issue | Title | Blocked by |
|---|---|---|
| #233 | Screenshot artifact bundle | Closed ✅ — merged PR #339 (five frames), PR #340 (polish + IR review) |
| #221 | Mean-reversion channel (Greece step5 MAGNITUDE) | Nothing — unblocked ✅ |
| #222 | Contemporaneous processing path | Nothing — unblocked ✅ |
| #258 | Mandatory intent blocks | #285 (merged ✅) |
| #332 | Docker image stale — Python 3.11 cached, Python 3.12 required | Closed ✅ — merged PR #336 |

**Re-milestoned to M9** (removed from M8 board this session): #286 (intent_gap_check.py), #299 (Intent Block Author Agent), #300 (Data Quality Agent), #301 (agent-raci.md)

---

## Pending Engineering Lead Decisions

| Decision | Context | Status |
|---|---|---|
| GovernanceModule promotion path | Deferred from M8 demo — five criteria not yet met — target M9 | Decided: deferred |
| M8 formal close / M9 kickoff | Issue #370 filed — gate: retrospective + compliance scan + Socratic Agent TEST + #209 exit checklist | Pending — see #370 |
| M9 UX architecture — EL Decision 1 (north-star formulation) | Five options incl. per-mode tasks (Mode 1: trajectory reconstruction; Mode 2: threshold-safe path construction; Mode 3: real-time steering). Load-bearing for all hierarchy changes. | Pending — see #364, gates after #363 |
| M9 UX architecture — EL Decision 2 (viewport architecture) | Wrong question was Zone 1B vs 1C; correct question is primary viewport vs. drawer. Gates after #363 Gap 2. | Pending — see #364, gates after #363 |
| M9 UX architecture — EL Decision 3 (comparison mode conditional) | Conditional (single→divergence timeline; multi→DeltaChoropleth) vs. supplemental. Mode 3 always temporal. | Pending — see #364, gates after #363 |

---

## Key Decisions Made — Recent Sessions

| Decision | Rationale | Date |
|---|---|---|
| Issue #361 Chief Methodologist consultation — synthetic data framework | docs/architecture/synthetic-data-consultation.md (41.5k chars, 560 lines). Five questions answered. Method hierarchy: Bayesian > MICE > Bootstrap > structural extrapolation > structural absence. Three-condition meaninglessness threshold. MDA tier table (full/advisory/exploratory/none). Anomaly detection requires TSC sign-off, opt-in, Mode 3 excluded, governance indicators excluded. ADR-007 outline produced. PR TBD. | 2026-05-19 |
| Issue #359 implemented — CLAUDE.md structural refactor | docs/architecture/simulation-framework.md created (7.7k chars); CLAUDE.md reduced to 28,375 chars; role-based mandatory reading table added; three new principle sections (Platform Principle, Synthetic Data, UX Architectural Commitments); three-mode architecture referenced. PR #372. | 2026-05-19 |
| Design foundation sequence filed — 12 issues #359–#370 | PM Agent: EXECUTE — all 12 design foundation issues filed in dependency order. Issues #359–#363 are Immediate horizon; #364–#369 are Near-Term; #370 (M8 formal close) is Immediate and runs in parallel. | 2026-05-19 |
| UX first principles review completed — Case B verdict (PR #356) | docs/ux/design-thinking/worldsim-ux-architecture-first-principles.md. Root finding: current UI inverts instrument/context relationship (choropleth primary, instruments in drawer). Mode 3 active control requires instruments always visible — current architecture fails this. Case B: rethink warranted before M9. Minimum rethink = three document changes + reserved control plane zone. Five M9 governing premises produced. Highest-priority action: update information-hierarchy.md governing principle. Decision 2 (timeline zone assignment) reframed as wrong question — defer and address as viewport architecture question. | 2026-05-18 |
| M8 UX panel synthesis completed (PR #356) | Three-agent panel (UX Designer, Development Economist, Chief Methodologist) independently reviewed Design Thinking Agent M8 critique (PR #355). Nine cross-cutting concerns; three EL decisions required; four premises revised/rejected; six premises unanimously confirmed; six additive findings. Highest-priority EL decision: north-star.md Primary Cognitive Task formulation — load-bearing for all hierarchy changes. | 2026-05-18 |
| UX Design Thinking Agent activated (PR #353/#354/#355) | Issue #353 filed; agent persona added to agents.md (PR #354); M8 critique produced at docs/ux/design-thinking/m8-interaction-model-critique.md (PR #355). Core diagnosis: WorldSim is a spatial comparison tool applied to a temporal problem; trajectory view should be Zone 1B primary instrument. | 2026-05-18 |
| M8 DEMO issues filed (PR #351) | All nine IR findings filed as GitHub issues #342–#350; assigned to M8 milestone. Root Cause B (#343 DEMO-002) is highest-priority: resolves DEMO-002/003/005/006 simultaneously. IR review updated with issue numbers. | 2026-05-18 |
| M8 stakeholder walkthrough created (PR #351) | docs/demo/m8/stakeholder-walkthrough.md — v0.8.0 presenter guide; six-step Greece narration; Honest Disclosures section; governance honest-null Q&A; root redirect updated. | 2026-05-18 |
| M8 IR Agent review completed (PR #340) | Nine findings (DEMO-001–009); 2 CRITICAL, 4 SIGNIFICANT, 3 MINOR. Root Cause B (drawer too narrow/dense) explains DEMO-002/003/005/006 simultaneously — highest-priority fix. docs/demo/m8/reviews/2026-05-18-v0.8.0-stakeholder-review.md. | 2026-05-18 |
| M8 demo polish fixes merged (PR #340) | gdp_growth choropleth error fixed (switch after step 1); drawer opened at step 4 for primary surplus narration; compare scenario extended to 6 steps with matching initial_attributes so DeltaChoropleth has step 6 data. | 2026-05-18 |
| M8 milestone board cleanup (this session) | Exit checklists #261–#264 and #213 were systematically off-by-one milestone; corrected. #286/#299/#301 re-milestoned to M9; #217/#95 re-milestoned to M10. #142 closed (stale). | 2026-05-18 |
| Demo preparation standard established (PR #334) | docs/process/demo-preparation-standard.md defines the biennial demo cadence. M6 artifacts archived to docs/demo/m6/. M8 screenshot brief (UX Agent) saved to docs/demo/m8/screenshot-brief.md. Thesis frame: Frame C, Step 5 (2014) — asymmetric radar. | 2026-05-18 |
| Python 3.12 Docker fix merged (PR #336, closes #332) | Rebuilt image on python:3.12-slim (confirmed 3.12.13 in container). Added `sys.version_info < (3, 12)` startup guard to app/main.py (# noqa: UP036 — ruff UP036 fires because target-version=py312, guard is operationally needed for stale images). Documented `docker compose build api` in CONTRIBUTING.md Step 3. | 2026-05-18 |
| EcologicalModule delta path bug fixed (PR #328) | For STOCK indicators, emit new absolute value (current + elasticity_delta) not the raw delta. The propagation engine replaces STOCK attributes — emitting the raw ~-0.08 elasticity value would overwrite the 388 ppm seed with a tiny negative, corrupting all subsequent proximity computations. | 2026-05-18 |
| gdp_direction_step5_positive deferred to Issue #221 | MacroeconomicModule has no endogenous recovery mechanism; fiscal consolidation accumulates without rebound channel. Engine produces -0.434 at step 5 vs historical +0.007. Moved from blocking CI gate to deferred_thresholds. | 2026-05-18 |
| co2_concentration_ppm seed (388 ppm, NOAA MLO 2010) required for demo scenario | Without seed, EcologicalModule stock path has no attribute at step 1 → null proximity. Added to build_greece_demo_scenario() initial_attributes. | 2026-05-18 |
| M8 frontend UX four issues implemented (PR #329 ✅) | #317 display name registry + #318 ecological note → Zone 3A + #320 PMM Zone 1C widget (null placeholder M8) + #319 radar 250ms animation + prefers-reduced-motion guard + null-axis animation guard; tsc clean, 10/10 tests | 2026-05-18 |
| Null governance axis merged (Issue #315, PR #323 ✅) | `RadarAxisDatum.composite_score: number \| null` live on main; null = dashed hollow dot; `GOVERNANCE_IN_VALIDATION_LABEL`/`TOOLTIP` constants + `computeFinalScore()` pure function; DD-011 sentinel; 10 Vitest tests | 2026-05-18 |
| M8 ecological backend merged (Issues #312–#314, PR #324 ✅) | Strategy dispatch, proximity indicators, migrations. land_use_pressure_index is pre-normalized (no division by 0.25). Ecological exempt from single-entity guard. | 2026-05-18 |
| Greece fixture 2015 merged (Issue #316, PR #321 ✅) | Steps 4–6 actuals, DIRECTION_ONLY thresholds, capital controls, ECOLOGICAL_COMPOSITE_DISCLOSURE. | 2026-05-18 |
| M9–M13 milestone sequence approved | M9 Standards Foundation → M10 Engine Integrity → M11 Political Economy → M12 Analyst Tooling → M13 Methodology Publication | 2026-05-11 |

---

## Architectural State — Key Facts for Session Continuity

**ADR-005 Amendment 3 — merged ✅ (PR #309). Now live in `docs/adr/ADR-005-human-cost-ledger.md`.**

**M8 demo scenario — merged ✅ (PR #328). Implements Issue #269:**
- `build_greece_demo_scenario()` in `tests/fixtures/greece_2010_scenario.py`
- EcologicalModule enabled via `modules_config: {ecological: {enabled: True}}`
- CO2 seed: `co2_concentration_ppm = 388.0 ppm` (NOAA MLO 2010) in initial_attributes
- 5 backtesting tests in `tests/backtesting/test_greece_m8_demo.py`
- CLI demo: `backend/scripts/demo_greece_2010_2015.py`
- `gdp_direction_step5_positive` moved to deferred_thresholds (Issue #221)
- EcologicalModule STOCK delta path: emits `current + elasticity_delta` (not raw delta)

**M8 ecological backend — merged ✅ (PR #324). Implements Issues #312, #313, #314:**
- `_compute_composite_score` now async with three-branch dispatch; ecological uses `_boundary_proximity_strategy`
- `_ECOLOGICAL_MANDATORY_NOTE_TEMPLATE` with `{n_indicators}` slot
- `_SINGLE_ENTITY_GUARD_EXEMPT_FRAMEWORKS = frozenset({"ecological"})` — ecological not suppressed for single-entity scenarios
- Migrations: `c1a4e7f2d9b3` (confidence_tier), `d2b5f8a3e6c4` (ecological MDA thresholds)
- EcologicalModule: stock-path proximity computation from `entity.attributes`; temporal guards per `effective_from`
- `land_use_pressure_index` proximity uses `min(v, 2.0)` — no division by 0.25 (double-normalization prevention)

**M8 frontend UX — merged ✅ (PR #329). Implements Issues #317, #318, #319, #320:**
- `INDICATOR_DISPLAY_NAMES` registry in `RadarChart.tsx` — human-readable labels for all M8 indicators
- Zone 3A expandable ecological note — `EcologicalNoteDrawer` component
- PMM Zone 1C widget — `PolicyManoeuvreMeter` null placeholder (M8 scope)
- Radar chart 250ms CSS transition animation — `prefers-reduced-motion` + null-axis guard

**Frontend — null governance axis (Issue #315, PR #323 ✅ merged):**
- `RadarAxisDatum.composite_score: number | null` live on main
- `GOVERNANCE_IN_VALIDATION_LABEL` + `GOVERNANCE_IN_VALIDATION_TOOLTIP` exported constants
- `computeFinalScore(composite_score: number | null, weight: number): number | null` exported pure function
- Null axis: dashed hollow SVG circle (`strokeDasharray="2 2"`, `fill="none"`); Recharts polygon gap
- DD-011 in `docs/frontend/design-decisions.md` with sentinel

**M8 UX Design Thinking work stream — complete (PRs #355, #356):**
- Critique: `docs/ux/design-thinking/m8-interaction-model-critique.md` — six ranked premise changes; core diagnosis: WorldSim is spatial comparison tool applied to temporal problem
- Panel synthesis: `docs/ux/design-thinking/m8-critique-panel-synthesis.md` — three-agent panel; nine cross-cutting concerns; three EL decisions
- First principles review: `docs/ux/design-thinking/worldsim-ux-architecture-first-principles.md` — supersedes synthesis on conflicts
  - Case B verdict: architecture rethink before M9 implementation
  - Root finding: choropleth (context) occupies primary viewport; instruments (radar, PMM, MDA alerts) are in 25% drawer — inverted
  - Four primary flight instruments named (trajectory view, PMM, MDA alerts, four-framework current position) — all must be always visible without drawer
  - Decision 1 (north-star formulation): extend to per-mode tasks, not single formulation
  - Decision 2 (timeline zone assignment): wrong question — defer, reframe as viewport architecture question
  - Decision 3 (compare mode conditional): correct question — add Mode 3 case (always temporal, never choropleth)
  - Five M9 governing premises: (1) instruments in primary viewport, (2) instruments always visible without drawer, (3) step axis is shared frame for all instruments, (4) primary cognitive task per mode, (5) control plane reserved in layout before built
  - Highest-priority action: update information-hierarchy.md governing principle
- UX Design Thinking Agent persona: `docs/process/agents.md` — activation: `UX Design Thinking Agent: CRITIQUE — [scope]`

**Demo preparation standard — established ✅ (PR #334):**
- `docs/process/demo-preparation-standard.md` — nine-step biennial demo cadence; reference cases M6 (#220) and M8 (#333)
- `docs/demo/m6/` — M6 review and walkthrough archived
- `docs/demo/m8/screenshot-brief.md` — UX Agent five-frame brief for Issue #233
- Thesis frame: Frame C, Step 5 (2014) — asymmetric radar (financial partial recovery, HD depressed)
- Presentation sequence: C → A → B → D → E (lead with thesis)
- #233 closed ✅ — demo.sh updated, spec rewritten (M8), five frames captured, IR Agent review filed
- IR review: `docs/demo/m8/reviews/2026-05-18-v0.8.0-stakeholder-review.md` — 9 findings, issues TBF
- `docs/demo/stakeholder-walkthrough.md` is M6-era — needs M8 update before next review cycle

**Standards state:**
- Canonical unit registry: in DATA_STANDARDS.md §Canonical Unit Registry (PR #282)
- Field-level certification standard: in DATA_STANDARDS.md §Field-Level Data Certification (PR #282)
- simulation_reference_constants table: migrations a2b4c6d8e0f1 + b3c5d7e9f1a2 (PR #282)
- Intent block format: ratified in CODING_STANDARDS.md §Intent Blocks (PR #288)
- Framework promotion protocol: in CODING_STANDARDS.md §Framework Promotion Protocol (PR #282)
- [SIM-INTEGRITY] monitoring contract: in CODING_STANDARDS.md §Simulation Integrity Monitoring (PR #282)
- Disposition review standard: docs/process/disposition-review-standard.md (PR #283)

**Legibility baseline:**
- M7 baseline mean audit score: 6.8/10
- Lowest scoring function: `_reconstruct_state_from_snapshot` — 5/10 (fixed in PR #289)
- Baseline document: docs/standards/legibility-baseline-m7.md
- Blind audit prompt: docs/process/blind-code-audit-prompt.md

**M8 gate status (all clear):**
- #235 DIC blind interviews ✅
- #255 Legibility metrics baseline ✅
- #256 North Star CODING_STANDARDS ✅
- #257 Blind code audit ✅

---

## Session Update Instructions

At the end of every Claude Code session, update this file:
1. Update "Last updated" date
2. Move completed streams to Recently Merged PRs
3. Add any new open issues to the appropriate horizon section
4. Record any Engineering Lead decisions made
5. Update ADR-005 amendment scope if decisions were made
6. If a new agent was activated or defined this session, verify `docs/process/agents.md` is current before closing
7. This update is the **last action** of every session before closing
