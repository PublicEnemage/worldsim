# WorldSim Session State

> This file is maintained by Claude Code. It is updated at the end of
> every session as the last action before closing. Do not edit manually.
> Engineering Lead decisions and context are recorded here for session
> continuity. For permanent rules and architecture, see CLAUDE.md.

**Last updated:** 2026-05-18 (post-#334 merged — demo prep structure, screenshot brief, standing process)
**Current milestone:** M8 — Ecological and Governance Frameworks

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

---

## Recently Merged PRs (last 5)

| PR | Title | Date |
|---|---|---|
| #334 | docs(demo): M8 demo preparation — milestone structure, screenshot brief, standing process | 2026-05-18 |
| #331 | chore(state): SESSION_STATE.md update — M8 feature-complete post-#328/#329/#330 | 2026-05-18 |
| #330 | chore(state): SESSION_STATE.md update — PR #329 open, M8 frontend UX four issues | 2026-05-18 |
| #329 | feat(frontend): M8 UX — display names, ecological note expandable, PMM widget, radar animation | 2026-05-18 |
| #328 | feat(demo): M8 demo scenario — Greece 2010–2015 multi-framework measurement (closes #269) | 2026-05-18 |

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
| #233 | Screenshot artifact bundle | Screenshot brief ✅ (docs/demo/m8/screenshot-brief.md) — capture + IR Agent run pending |
| #221 | Mean-reversion channel (Greece step5 MAGNITUDE) | Nothing — unblocked ✅ |
| #222 | Contemporaneous processing path | Nothing — unblocked ✅ |
| #258 | Mandatory intent blocks | #285 (merged ✅) |
| #332 | Docker image stale — Python 3.11 cached, Python 3.12 required | Nothing — `docker compose build api` fix |

**Re-milestoned to M9** (removed from M8 board this session): #286 (intent_gap_check.py), #299 (Intent Block Author Agent), #300 (Data Quality Agent), #301 (agent-raci.md)

---

## Pending Engineering Lead Decisions

| Decision | Context | Status |
|---|---|---|
| GovernanceModule promotion path | Deferred from M8 demo — five criteria not yet met — target M9 | Decided: deferred |
| M8 formal close / M9 kickoff | #233 screenshot capture + IR Agent run + M8 retrospective remain; #209 exit checklist open | Pending |

---

## Key Decisions Made — Recent Sessions

| Decision | Rationale | Date |
|---|---|---|
| M8 milestone board cleanup (this session) | Exit checklists #261–#264 and #213 were systematically off-by-one milestone; corrected. #286/#299/#301 re-milestoned to M9; #217/#95 re-milestoned to M10. #142 closed (stale). | 2026-05-18 |
| Demo preparation standard established (PR #334) | docs/process/demo-preparation-standard.md defines the biennial demo cadence. M6 artifacts archived to docs/demo/m6/. M8 screenshot brief (UX Agent) saved to docs/demo/m8/screenshot-brief.md. Thesis frame: Frame C, Step 5 (2014) — asymmetric radar. | 2026-05-18 |
| Python 3.11/3.12 mismatch (Issue #332) | api container image stale (built on 3.11); Dockerfile already specifies 3.12. Temporary workaround: `type CompositeStrategy = Callable[...]` (PEP 695 plain assignment) applied to app/api/scenarios.py. Proper fix: `docker compose build api`. | 2026-05-18 |
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

**Demo preparation standard — established ✅ (PR #334):**
- `docs/process/demo-preparation-standard.md` — nine-step biennial demo cadence; reference cases M6 (#220) and M8 (#333)
- `docs/demo/m6/` — M6 review and walkthrough archived
- `docs/demo/m8/screenshot-brief.md` — UX Agent five-frame brief for Issue #233
- Thesis frame: Frame C, Step 5 (2014) — asymmetric radar (financial partial recovery, HD depressed)
- Presentation sequence: C → A → B → D → E (lead with thesis)
- #233 remaining work: `demo.sh` update, Playwright spec, screenshot capture, IR Agent run

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
