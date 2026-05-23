# WorldSim Session State

> This file is maintained by Claude Code. It is updated at the end of
> every session as the last action before closing. Do not edit manually.
> Engineering Lead decisions and context are recorded here for session
> continuity. For permanent rules and architecture, see CLAUDE.md.

**Last updated: 2026-05-23 (PR #501 merged — Issue #493 closed; M9 IR review complete; M8 DEMO triage done; IR-001–IR-006 filed as M10 scope)**
**Current milestone:** M9 — Standards Foundation

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

**Step 2 — Immediate (unblocked after #359):** ✅ COMPLETE

| Issue | Title | Milestone | Blocks |
|---|---|---|---|
| #360 ✅ | Agent working agreements (15 agents) | M9 | #369 |
| #361 ✅ | Synthetic data framework — Chief Methodologist + ADR | M9 | #362 |

**Step 3 — Immediate (requires #359 + #360 + #361):** ✅ COMPLETE

| Issue | Title | Milestone | Blocks |
|---|---|---|---|
| #362 ✅ | User persona document (5 personas, marquee cases) | M9 | #363 #367 |

**Step 4 — Immediate (requires #359 + #362):** ✅ COMPLETE — PR #390 merged (closes #363)

| Issue | Title | Milestone | Blocks |
|---|---|---|---|
| #363 ✅ | UX first-principles depth — close six gaps | M9 | #364 |

**Step 5 — Near-Term (sequential from here; #365 now unblocked):**

| Issue | Title | Milestone | Blocks |
|---|---|---|---|
| #364 ✅ | EL decisions — north-star, viewport, comparison mode | M9 | #365 |
| #365 ✅ | UX document updates (north-star, info-hierarchy, journeys) | M9 | #366 #368 — PR #399 merged ✅ |
| #366 ✅ | Trajectory view ADR | M9 | ADR-010 accepted 2026-05-22 — PR #420 |
| #367 | Persona-anchored IR review re-run (Persona 2) | M9 | #368 |
| #368 | DEMO issues re-triage #342–#350 | M9 | M9 DEMO sprint scope |
| #369 ✅ | agent-raci.md — RACI chart for all 15 agents | M9 | Agent governance docs — PR #401 merged ✅ |

---

## Open PRs

No open PRs — board clear as of 2026-05-23.

## Recently Merged PRs (last 5)

| PR | Title | Date |
|---|---|---|
| #501 | docs(ir): M9 instrument cluster IR review + M8 DEMO triage (Issue #493) | 2026-05-23 |
| #491 | test(e2e): #463 PR 2 — Greece integration suite + AC-001/002 skip removed (closes #463) | 2026-05-23 |
| #490 | feat(frontend): wire InstrumentCluster into App.tsx — Zone 1 instruments live (Issue #463 PR 1) | 2026-05-23 |
| #489 | test(qa): #459 — remaining acceptance tests: ModeIndicator, AC-006 RTL, AC-013, US-026 | 2026-05-23 |
| #487 | feat(frontend): PMMWidgetZone1C + FourFrameworkZone1D — Zone 1C/1D instruments (Issue #462) | 2026-05-23 |
| #481 | chore(state): SESSION_STATE.md — session end 2026-05-23 (PRs #479–#480) | 2026-05-23 |
| #480 | test(qa): retrofit instrument cluster spec — split Type 1/Type 2 ACs, remove blanket skip (closes #473) | 2026-05-23 |
| #479 | process(nm): NM-018 — hammer-nail; panel composition principle for pre-EL consultations | 2026-05-23 |
| #468 | feat(api): GET /scenarios/{id}/trajectory endpoint (closes #458) | 2026-05-23 |
| #466 | docs(process): PM Agent pre-EL consultation — standing automatic capability (closes #464) | 2026-05-23 |
| #456 | docs(process): PM Agent issue hierarchy rule — Epic → Feature → Task, binary spawning | 2026-05-23 |
| #454 | docs(ux): resolve UX-RULING-1/2/3 — alert tense markers, null CSS class, mode labels | 2026-05-23 |
| #452 | docs(ux): US-GAP-001 resolved — Mode 1 COMPARE_VIEW placeholder; EL decision M10 (Issue #451) | 2026-05-23 |
| #449 | docs(ux): M9 instrument cluster user stories — 29 stories, QA + FA consumers (closes #441) | 2026-05-23 |
| #447 | docs(process): NM-014 systemic root cause — micro-management cycle and correct locus of specification | 2026-05-23 |
| #445 | docs(process): PR merge gate — mandatory pause + SESSION_STATE auto-merge exception | 2026-05-23 |
| #438 | docs(process): blameless continuous improvement principle — Aviation SMS in CLAUDE.md | 2026-05-23 |
| #436 | docs(process): near-miss registry — NM-008 through NM-013, agent team growth and DIC founding | 2026-05-23 |
| #435 | docs(process): near-miss registry — NM-001 through NM-007, Aviation SMS methodology | 2026-05-23 |
| #434 | chore(state): SESSION_STATE.md — PR #432 + #433 merged; Issue #431 closed | 2026-05-23 |
| #433 | docs(process): file ownership table and HORIZON file authority audit (closes #431) | 2026-05-23 |
| #432 | docs(process): file authority rule in CLAUDE.md — agents must not write to owned files without prior owner review | 2026-05-23 |
| #429 | docs(adr+schema): ADR-010 D6+D2 amendments; CM reference range consultation; api_contracts + database.yml | 2026-05-23 |
| #417 | docs(process): ADR-008 panel review artifact and panel review process standard | 2026-05-22 |
| #416 | docs(adr): ADR-008 — UX architecture: instrument cluster, viewport, and interaction model (closes #397) | 2026-05-22 |
| #409 | docs(vision): WorldSim technical concepts — 18 architectural concepts with reasoning | 2026-05-22 |
| #408 | docs(roadmap): WorldSim roadmap M9–M13 with demo arc, long-term direction, and process integration | 2026-05-22 |
| #427 | docs(frontend): EL decisions A/B/C recorded — trajectory endpoint unblocked | 2026-05-22 |
| #426 | docs(frontend): Six-agent parallel consultation — DA-F2/F4/F5 pre-implementation record | 2026-05-22 |
| #425 | docs(frontend): Architect Agent review of Data Architect findings (DA-F1–F5) | 2026-05-22 |
| #422 | docs(frontend): FA brief — three-agent review findings incorporated | 2026-05-22 |
| #421 | docs(frontend): M9 FA brief — instrument cluster implementation (ADR-008 + ADR-010) | 2026-05-22 |
| #420 | docs(adr): ADR-010 accepted — EL decision recorded with rationale; ARCH-004 → ACCEPTED | 2026-05-22 |
| #401 | docs(process): agent-raci.md — RACI chart for all 15 agents (closes #369, #301) | 2026-05-21 |
| #399 | docs(ux): UX document updates — EL Decisions 1/2/3 (north-star, information-hierarchy, user-journeys) | 2026-05-21 |
| #390 | docs(ux): UX first-principles depth — six gaps closed, revised six premises (closes #363) | 2026-05-21 |
| #388 | docs(ux): persona-grounded UX review — Case B and governing premises vs. five personas (closes #387) | 2026-05-21 |
| #385 | docs(ux): user persona document — five personas, entry state taxonomy, marquee cases (closes #362) | 2026-05-20 |
| #384 | docs(process): agent working agreements — all 15 agents (closes #360) | 2026-05-20 |
| #383 | docs(vision): WorldSim founding document — synthesized from April-May 2026 founding conversations | 2026-05-20 |
| #373 | docs(adr): Chief Methodologist consultation — synthetic data framework (closes #361) | 2026-05-19 |
| #372 | docs(claude): CLAUDE.md structural refactor — closes #359 | 2026-05-19 |
| #371 | chore(state): design foundation sequence — 12 issues #359–#370 filed | 2026-05-19 |
| #356 | docs(ux): M8 interaction model critique — panel synthesis (UX Designer, Dev Economist, Chief Methodologist) | 2026-05-18 |
| v0.8.0 | GitHub Release — Milestone 8 formal close | 2026-05-19 |
| #399 | docs(ux): UX document updates — EL Decisions 1/2/3 (north-star, information-hierarchy, user-journeys) | 2026-05-21 |
| #396 | chore(state): SESSION_STATE.md — EL Decisions 1/2/3 recorded; Issue #364 closed; Issues #392–#395 filed | 2026-05-21 |
| #391 | chore(state): SESSION_STATE.md — PR #390 merged; Issue #363 closed; Issue #364 unblocked | 2026-05-21 |
| #390 | docs(ux): UX first-principles depth — six gaps closed, revised six premises (closes #363) | 2026-05-21 |
| #388 | docs(ux): persona-grounded UX review — Case B and governing premises vs. five personas (closes #387) | 2026-05-21 |
| v0.8.0 | GitHub Release — Milestone 8 formal close | 2026-05-19 |
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

## Open Issues — M9 Horizon:Immediate (this session)

| Issue | Title | Status / Gate |
|---|---|---|
| #473 ✅ | test(qa): retrofit instrument-cluster spec — split component ACs into task scope; remove blanket skip | Closed — PR #480 merged; Type 1 ACs distributed to #460/#461/#462 via comments; integration spec created |
| #460 ✅ | feat(frontend): TrajectoryView — Zone 1A (instrument cluster) | Closed — PR #484 merged |
| #461 ✅ | feat(frontend): MDA Alert Panel — Zone 1B (instrument cluster) | Closed — PR #486 merged |
| #462 ✅ | feat(frontend): PMM + Four-Framework — Zone 1C/1D (instrument cluster) | Closed — PR #487 merged |
| #463 ✅ | test(e2e): Greece integration Playwright suite | Closed — PR #490 (App.tsx wiring) + PR #491 (Greece suite) merged |
| #367 ✅ | docs(demo): persona-anchored IR review re-run (Persona 2) | Closed — superseded by M9 instrument cluster redesign; see #493 |
| #368 ✅ | docs(demo): DEMO issues re-triage #342–#350 | Closed — superseded by M9 instrument cluster redesign; see #493 |
| #493 ✅ | M9 demo — IR review + DEMO triage against Greece fixture with M9 cluster | Closed — PR #501 merged |

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
| Trajectory endpoint implementation | FastAPI route + Pydantic model + normalized_absolute_strategy backend function. All prerequisites complete. May begin. | Ready — unblocked |
| US-GAP-001 — Andreas Mode 1 comparative case surface | **Resolved.** EL decision 2026-05-23: M10 gap. Issue #451 filed. information-hierarchy.md §COMPARE_VIEW Mode 1 placeholder added. user-stories file updated to reflect partial M9 service for Persona 3. | Complete ✅ — PR #452 |
| UX-RULING US-016 — alert text strings per mode | **Resolved.** Mode 1: `"crossed"` present; `"is projected"` + `"Caused by:"` absent. Mode 2: `"is projected to cross"`. Mode 3: ` — ` separator; starts with `"CRITICAL"` or `"WARNING"`. PR #454. | Complete ✅ — 2026-05-23 |
| UX-RULING US-022 — null vs. zero CSS class | **Resolved.** Null → `score-value--null` (opacity ≤ 60%). Numeric/zero → `score-value--numeric`. PR #454. | Complete ✅ — 2026-05-23 |
| UX-RULING US-026 — mode indicator label strings | **Resolved.** Mode 1: `"Replay"`. Mode 2: `"Simulation"`. Mode 3: `"Active Control"`. PR #454. | Complete ✅ — 2026-05-23 |
|---|---|---|
| Decision A (DA-F2): MDA floor overlays deferred to M10 | M9 trajectory view ships without MDA floor ReferenceLines except ecological WARNING at y=1.0 (boundary-crossing, defensible without backtesting). CM consultation on indicator inventory + reference ranges authorized as M10 prerequisite. M10-B schema confirmed (new mda_composite_floors table with cm_approval_reference column). ADR-010 Decision 6 amendment pending. | Complete ✅ — 2026-05-22 |
| Decision B (DA-F4): Path A selected — normalized absolute composite for single-entity trajectory | Path A: four framework curves rendered for single-entity scenarios; financial/HD use normalized absolute value composite (Tier 3 floor); strokeDasharray="8 3"; "single-country index" legend + tooltip; Zone 3 methodology note mandatory. CM reference range consultation is the hard implementation gate. ADR-010 Decision 2 amendment + Issue #193 update required. | Complete ✅ — 2026-05-22 |
| Decision C (DA-F5): step_metadata JSONB option (a) confirmed | step_metadata key in scenarios.configuration JSONB; no migration; 1-based step index keys; SIGNIFICANT or ROUTINE values (never STANDARD). ADR-010 Decision 2 minor amendment pending. | Complete ✅ — 2026-05-22 |
|---|---|---|
| ADR-010 acceptance | All 4 INCORPORATE items approved with rationale: FA-R3 (dense array contract — one null meaning only); FA-R4+UD-R1 (provisional hex values, UX Designer authority, RACI boundary correct); CM-R1 (No False Precision — deferral placeholder required); CM-R3 (composite-score floors only — indicator projection is methodologically dishonest). ADR-010 status → Accepted. ARCH-004 → ACCEPTED in backlog. M9 FA brief unblocked. | Complete ✅ — 2026-05-22 |
| ADR-008 acceptance | All 6 INCORPORATE items applied; EL decision recorded (Option A: stacked forms, ~280px); ADR-008 status → Accepted; ARCH-002 → ACCEPTED in backlog. Issue #397 closed. FA brief (FA-C1–FA-C5) deferred to M9. | Complete ✅ — 2026-05-22 |
| GovernanceModule promotion path | Deferred from M8 demo — five criteria not yet met — target M9 | Decided: deferred |
| M8 formal close / M9 kickoff | Issue #370 filed — gate: retrospective + compliance scan + Socratic Agent TEST + #209 exit checklist | Complete ✅ — v0.8.0 released, Issue #209 closed |
| M9 UX architecture — EL Decision 1 (north-star formulation) | Adopted: per-mode formulation. Mode 1: trajectory reconstruction AND historical pattern recognition. Mode 2: threshold-safe path construction. Mode 3: real-time steering within human cost constraints. All 13 marquee cases validated. | Complete ✅ — recorded on #364 (2026-05-21) |
| M9 UX architecture — EL Decision 2 (viewport architecture) | Adopted: primary viewport is the instrument cluster. Zone 1B vs 1C superseded. EntityDetailDrawer demoted to detail/methodology surface. Entity selector is persistent header element. | Complete ✅ — recorded on #364 (2026-05-21) |
| M9 UX architecture — EL Decision 3 (comparison mode conditional) | Adopted: conditional switch extended to all three modes. Single-entity Mode 2: divergence timeline. Multi-entity Mode 2: DeltaChoropleth. Mode 3: automatic live A/B (no invoke). DeltaChoropleth deprecated for single-entity and Mode 3. | Complete ✅ — recorded on #364 (2026-05-21) |

---

## Key Decisions Made — Recent Sessions

| Decision | Rationale | Date |
|---|---|---|
| Issue #493 closed — M9 IR review + M8 DEMO triage complete (PR #501) | IR review at `docs/demo/m9/reviews/2026-05-23-v0.9-instrument-cluster-ir.md`. Six findings (IR-001–IR-006) filed as #495–#500 for M10. Two root causes: (A) data layer not wired to Zone 1B/1C — mda_alerts always [], PMM always null; (B) session state and entry-state architecture not implemented — landing screen is choropleth, step annotations absent for user-created scenarios. Root Cause B from M8 (drawer legibility) fully resolved by M9 architecture. M8 DEMO triage: #344 closed (text legibility resolved); #342/#343/#346/#347/#349 transformed + re-milestoned to M10; #345/#348/#350 persist to M10. Six M10 issues: #495 (IR-001 Critical — mda_alerts wiring), #496 (IR-002 — PMM endpoint), #497 (IR-003 — persistent scenario state/demonstrative entry), #498 (IR-004 — default step labels from start year), #499 (IR-005 — governance "(in validation)" inline), #500 (IR-006 — loading state). | 2026-05-23 |
| Issue #463 fully closed — Zone 1 cluster live in App.tsx + Greece Playwright suite (PRs #489–#491) | PR #489 closed the four remaining QA acceptance test gaps (#459): ModeIndicator component + 13 Vitest tests; AC-006 RTL atomicity test (act() boundary, Vitest cleanup fix); AC-013 "(exp)" confidence badge Playwright guard; US-026 mode-indicator RTL act() test. PR #490 wired InstrumentCluster into App.tsx via ScenarioInstrumentCluster: trajectory fetch + parse (array→Record, Decimal string→number, boundary_proximity→normalized_absolute); data-testid duplication fixed in InstrumentCluster wrapper divs. PR #491 completed Issue #463 PR 2: removed test.skip() from AC-001/AC-002; added selectScenario() helper; created greece-integration.spec.ts (5 tests: smoke, mode indicator "Replay", data-current-step tracking, governance null AC-015, per-step cluster consistency + Mode 2 no-op guard). | 2026-05-23 |
| Zone 1A/1B/1C/1D instrument cluster complete (PRs #484–#487) | All four co-primary instruments shipped: `TrajectoryView.tsx` (Zone 1A — ComposedChart, 4 active + 4 ghost Lines, divergence fills, CVD-safe framework colors, Mode 1 custom tick, (exp) badge, Path A dashed curves); `MDAAlertPanelZone1B.tsx` (Zone 1B — TERMINAL→CRITICAL→WARNING sort, compact 3-line at <320px / full-density at ≥320px, mode-specific tense, negotiation labels, causal attribution Mode 3 only); `PMMWidgetZone1C.tsx` (Zone 1C — mode-specific label, direction arrow, pending state at 40% opacity); `FourFrameworkZone1D.tsx` (Zone 1D — 4 framework scores derived from Zustand atom, null→`score-value--null`+"—", numeric→`score-value--numeric`). Store extended: `Zone1BAlert`, `mda_alerts`, `pmm_value`, `pmm_direction`, `setPmmState`. 104/104 Vitest tests passing. All Playwright E2E guards use isVisible no-op pattern pending App.tsx integration (#463). | 2026-05-23 |
| TrajectoryView Zone 1A merged (PR #484, closes #460) | `TrajectoryView.tsx` (ComposedChart: 4 active Lines, 4 ghost Lines, Area divergence fills, ecological WARNING ReferenceLine, ADR-007-gated band infrastructure, Mode 1 custom tick, (exp) badge, Path A single-entity dashed curves); `InstrumentCluster.tsx` (two-column layout 480/240/280px at 1024×768, 580/400/280px at 1280×800, 280px control plane always rendered); `scenarioStepStore.ts` (Zustand atom, single-set() atomicity invariant); `frameworkColors.ts` (UX Designer ruling — teal #1A8FA0 replaces green #3A7A4B after CVD deuteranopia collision identified); DD-012–DD-015 added; FA brief CVD Validation Result recorded; MV-001 closed; 31/31 Vitest tests passing; AC-003/004/005 Playwright guards added (element not in App.tsx yet); MV-002 hardware validation pending before M9 exits. | 2026-05-23 |
| Known Issues registry established — distinct category from near-misses (PR #482) | External infrastructure limitations (GitHub Actions, third-party APIs) cannot be fixed by process redesign — filing them as near-misses produces improvement recommendations against things we cannot change. Known Issues live in `docs/process/known-issues-registry.md`; near-misses in `docs/process/near-miss-registry.md`. Categorisation rule: if the fix requires changing our own code/process → near-miss; if the fix requires waiting for an upstream vendor → Known Issue. KI-001 filed: GitHub Actions `pull_request` event silently fails to fire (workaround: empty retriggering commit). CLAUDE.md, agents.md, agent-raci.md all updated. | 2026-05-23 |
| Instrument cluster spec retrofit — blanket skip removed, Type 1/Type 2 split completed (PR #480, closes #473) | `instrument-cluster.spec.ts` deleted; `instrument-cluster-integration.spec.ts` created with only AC-001 and AC-002 (Type 2 integration-level, individual `test.skip()` per test — no file-level blanket suppression). Component-level ACs (AC-003–AC-014) distributed to implementing issues: AC-003–013 → #460 (TrajectoryView) with full test code; AC-014 + component tests → #462 (PMM + Four-Framework); component tests → #461 (MDA Alert Panel). CI green: no `test.skip(true, ...)` in any instrument cluster spec file. | 2026-05-23 |
| NM-018 filed — hammer-nail: technical panel produced engineering solutions to a process problem (PR #479) | Three technical agents (Architect, Frontend Architect, QA Lead) consulted on skip governance; all three produced engineering solutions (CI guard, skip registry, DOM-presence fixture) to what was a process problem (missing AC categorization rule). PO Agent and UX Designer Agent immediately identified the correct root cause. Root cause of the near-miss: no rule existed requiring PM Agent to evaluate whether panel composition matched the problem's root cause domain, not just its surface presentation. Standing fix: panel composition principle added to PM Agent pre-EL consultation protocol in `docs/process/agents.md §PM Agent — Pre-EL Consultation` between steps 2 and 3. | 2026-05-23 |
| PO Agent standing responsibilities — dual consumer + sequence gate (PR #477, closes #470) | Two non-negotiable standing responsibilities added to PO working agreement: (1) Stories serve QA Lead and Frontend Architect equally — a story too vague for QA to write a meaningful test, or too abstracted for FA to make the right tradeoffs, is a weak story; (2) Stories → tests → implementation sequence gate — the PO owns enforcement; a story session is not complete until the stories doc is merged, a QA test authorship issue is filed blocking implementation, and the issue hierarchy is established. RACI rows 2 and 3 updated: PO consultation trigger now explicitly names QA/FA story consumers. | 2026-05-23 |
| Type 1/Type 2 AC categorization rule — CODING_STANDARDS + QA Lead + PO working agreements (PR #476, closes #474) | Before any QA E2E spec is authored against a multi-component feature, ACs must be categorized: Type 1 (component-level — testable when one component ships alone; lives in implementation task PR scope) vs Type 2 (integration-level — testable only when all named components coexist; lives in dedicated `<feature>-integration.spec.ts`). `test.skip(true, ...)` at file scope is a process violation for any spec containing Type 1 ACs. QA Lead working agreement (new) makes categorization the first standing commitment. PO pre-authorship check added. Documented in `docs/CODING_STANDARDS.md §E2E Pre-implementation Test Categorization`. | 2026-05-23 |
| NM-017 filed — story–test–implementation decomposition mismatch (PR #475, anticipatory) | 16 instrument cluster ACs were suppressed by a blanket `test.skip(true, ...)` because zone-level and component-level ACs were bundled in a single spec file while implementation was decomposed into three Task Issues (#460/461/462). Engineering Lead identified the structural gap through governance anxiety about skip management — before any component shipped. Root cause: no AC categorization rule existed. Severity: High (CI blind spot across primary viewport ACs). Response: retrofit Issue #473 + process change Issue #474 (now complete via PR #476). | 2026-05-23 |
| NM-016 + pre-push lint gate added to CLAUDE.md (PR #472, closes #471) | Two parallel agents (Issues #458 and #459) pushed PRs without running `ruff check .` locally. Both failed CI on I001/E501 — trivially preventable in two seconds locally. Root cause: agent prompts specified `pytest` but not `ruff`. Pre-push lint gate added to CLAUDE.md constitution: `cd backend && ruff check . && mypy app/` required before any push touching Python files. Local ruff==0.7.2 is identical to CI-pinned version — no environment gap. NM-016 filed. | 2026-05-23 |
| Backend trajectory endpoint merged (PR #468, closes #458) | `GET /scenarios/{scenario_id}/trajectory` FastAPI endpoint live on main. Key contracts: `SINGLE_ENTITY_REFERENCE_RANGES` dict (gdp_growth, reserve_coverage_months, unemployment_rate, net_enrollment_secondary — health_expenditure excluded as non-monotonic); `normalized_absolute_strategy` function; ecological MDA floor (WARNING at 1.0) built in application code (no M9 DB table); `mda_floors` at response root; `step_significance` from `step_metadata` JSONB; Pydantic v2 schemas (`TrajectoryResponse`, `TrajectoryStep`, `TrajectoryFrameworkPoint`, `MDAFloorRecord`). 13 unit tests in `test_trajectory_endpoint.py`. | 2026-05-23 |
| QA pre-implementation test authorship merged (PR #469, closes #459) | `frontend/tests/e2e/instrument-cluster.spec.ts` — 16 ACs (AC-001 through AC-014) as Playwright E2E gates. All tests wrapped with `test.skip(true, ...)` pending #460/461/462 (this skip is the subject of retrofit Issue #473). `page.emulate()` Puppeteer bug fixed → CDP session (`Emulation.setCPUThrottlingRate`). `frontend/src/components/__tests__/TrajectoryView.test.ts` — Vitest unit tests for AC-010/013/015. `backend/tests/fixtures/test_greece_fixture_step_metadata.py` — 13 pytest CI gate tests for AC-012 (step_event_label ≤8 words AND ≤32 chars). `frontend/tests/manual-validation/mv-gates.md` — MV-001/002/003 procedures. | 2026-05-23 |
| Playwright test skip governance — three-agent consultation (anticipatory) | Engineering Lead asked how to prevent `test.skip()` from being abused or forgotten. Architect (skip registry — hermetic), Frontend Architect (DOM-presence fixture — self-healing), and QA Lead (test.fixme() + milestone exit gate) each assessed independently. Unanimous finding: skip must be visible and self-expiring. Key divergence: registry (auditable) vs DOM-presence (no maintenance). Recommendation: DOM-presence as runtime control + test.fixme() for visibility + Type 1/Type 2 discipline as root fix. Root fix (Type 1/Type 2 rule) eliminates the problem structurally — per NM-017, the correct fix is decomposition discipline, not skip governance tooling. | 2026-05-23 |
| PM Agent pre-EL consultation — standing automatic capability (PR #466, closes #464) | Pre-EL consultation added to PM Agent working agreement as automatic standing responsibility. Three trigger conditions: [EL-DECISION] tag in any document; pending entry in SESSION_STATE.md §Pending EL Decisions; any agent raising an EL-authority question. Four-step process: identify → activate independently → synthesize → surface recommendation. RACI framing: EL holds A; PM Agent holds R for the consultation — cold questions reaching EL without prior consultation are a PM Agent failure. Disagreement handling: PM Agent names divergence and surfaces all positions; does not resolve. | 2026-05-23 |
| Issue hierarchy rule encoded permanently (PR #456); M9 trajectory endpoint epic filed (#457–#463) | Binary three-level issue hierarchy (Epic → Feature → Task) added to PM Agent working agreement in agents.md and referenced in CLAUDE.md. Spawning rule: children created only when >1 agent OR >1 PR required — agent-count-based, not complexity-based. M9 instrument cluster epic #457 filed with six child Feature Issues: #458 (backend trajectory endpoint), #459 (QA test authorship — pre-implementation gate), #460 (TrajectoryView Zone 1A), #461 (MDA Alert Panel Zone 1B), #462 (PMM + Four-Framework Zone 1C/1D), #463 (Greece integration Playwright suite). #459 explicitly blocks #460/461/462. #463 spawns Level 3 Task Issues when prerequisites complete. Pre-EL consultation standing capability filed as #464 — PM Agent auto-coordinates before any EL decision reaches EL. | 2026-05-23 |
| UX-RULING-1/2/3 resolved — QA gate fully unblocked (PR #454) | UX Designer Agent resolved all three open Playwright assertion placeholders in the M9 instrument cluster user stories. RULING-1 (US-016): alert tense markers per mode — Mode 1 `"crossed"`, Mode 2 `"is projected to cross"`, Mode 3 ` — ` separator format; advisory language exclusions. RULING-2 (US-022): null composite score → CSS class `score-value--null` (opacity ≤ 60%); numeric/zero → `score-value--numeric`. RULING-3 (US-026): mode indicator labels — `"Replay"` / `"Simulation"` / `"Active Control"`. All 29 stories now fully testable. QA gate UNBLOCKED. | 2026-05-23 |
| US-GAP-001 — Mode 1 comparable-case comparison deferred to M10 | Pre-EL consultation: UX Design Thinking Agent, PO Agent, Architect Agent — unanimous M10 verdict. Key finding: the gap was narrower than stated. ADR-010 Decision 11 and FA brief §UD-R2 already specify the rendering layer for multi-case Mode 1 (step alignment, stacked entity dates). The missing piece is the Zone 2 entry point for selecting the second fixture — a COMPARE_VIEW architecture question, not an instrument cluster question. Mode 1 block added to `information-hierarchy.md §COMPARE_VIEW` with decision space documented. User stories file updated: US-GAP-001 converted from pending to resolved; M9 service level for Persona 3 stated explicitly (orientation sufficient; comparison M10). Issue #451 filed with full M10 deliverable spec. PR #452. | 2026-05-23 |
| M9 instrument cluster user stories — 29 stories authored (Issue #441, PR #449) | PO Agent: EXECUTE. Two consumers: QA Lead (writes acceptance tests from stories before implementation) and Frontend Architect (implements to stories as user-value specification). 29 stories across 9 groups (US-001–US-029): Zone 1 Completeness, Trajectory View, MDA Alert Panel, PMM Widget, Four-Framework Current Position, Atomicity, Persistent Header, Control Plane Reserved Zone, Performance. All stories include Given/When/Then acceptance criteria tagged by test method [Playwright], [Vitest], [RTL], [pytest], [Manual]. Three [UX-RULING] placeholders (US-016, US-022, US-026) await UX Designer observable-string rulings. One [EL-DECISION] gap finding (US-GAP-001): Andreas Mode 1 comparative-case comparison requires a surface not in M9 spec — EL to decide M9 or M10. File: `docs/ux/user-stories-instrument-cluster-m9.md`. | 2026-05-23 |
| NM-014 systemic root cause expanded — micro-management cycle named | The contributing factor section was accurate but incomplete. Expanded with a full nine-step cycle analysis: mistakes → more prescription → reduced agent reasoning → more mistakes → more prescription. Named the analogy to the tech lead failure mode. Stated the correct structural response: issues carry prescription, standing documents carry rules, agents write their plan before executing, prompts are outcome-oriented. Prescriptive prompting weight upgraded from "under investigation" to "confirmed as significant — both symptom and perpetuating mechanism." PR #447. | 2026-05-23 |
| PR merge gate rule added to CLAUDE.md — mandatory pause + SESSION_STATE.md auto-merge exception | After opening any PR, Claude Code must stop all git operations, report the PR URL, and wait for user merge confirmation before pulling main or starting the next task. Exception: SESSION_STATE.md-only PRs are pre-authorized for auto-merge once the `changes` CI status check passes. Rationale: eliminates the concurrent-terminal race condition (two processes operating git on the same local repo without coordination) while preserving the human as merge coordinator and CI gate — especially important in parallel-session scenarios. PR #445. | 2026-05-23 |
| Branch protection remediation — `changes` and `compliance-scan` added to required status checks | Root-cause analysis of the checkout@v6 CI failure revealed that `changes` (the path-filter gate job) and `compliance-scan` were absent from required status checks. Only `lint`, `test-backend`, and `playwright-e2e` were required — all downstream of `changes`. When `changes` fails, downstream jobs are skipped-due-to-dependency-failure, potentially not blocking merges. Applied immediately via GitHub API (no PR required). Required checks now: `changes`, `test-backend`, `lint`, `playwright-e2e`, `compliance-scan`. NM-015 filed. | 2026-05-23 |
| NM-014 + NM-015 filed — near-miss registry now 15 entries | NM-014: file edit reported as complete without being committed to a branch (agents.md in PO Agent EXECUTE). Process improvement: personal commit gate — a change is not reportable as done until it is on a branch and committed. NM-015: CI gate job (`changes`) was not a required status check; compliance-scan also absent. Process improvement: required checks must include the root gate job, not just its downstream dependents. Milestone exit checklist checkpoint added. PR #443. | 2026-05-23 |
| CI fix — actions/checkout@v6 → @v4 | The April 19 checkout@v6 upgrade was intentional (Node.js 20 deprecation, v6 released January 2026) and appears to have regressed recently. All 7 occurrences across ci.yml and milestone-automation.yml updated to @v4 (current stable). This unblocked PR #443. PR #444. | 2026-05-23 |
| Near-miss registry created — NM-001 through NM-013 | `docs/process/near-miss-registry.md` created using Aviation SMS epistemology: near-misses treated with same rigor as incidents because they reveal hazards without the cost of failure. 7 reactive entries (NM-001–NM-007) + 6 anticipatory entries (NM-008–NM-013). Recurring pattern identified: agent acting in domain belonging to another agent without required consultation (NM-005, NM-006, NM-007). Second pattern: six entries are anticipatory — Engineering Lead sensing structural gaps before failure. Registry maintenance section defines template, severity levels, and the key question: "caught by process or by a person?" PR #435 + PR #436. | 2026-05-23 |
| PR board cleared — all stale PRs confirmed merged | 14 PRs that appeared open in SESSION_STATE were confirmed merged via GitHub. Open PRs table cleared. Board is clean. | 2026-05-23 |
| File authority rule + ownership table — Issue #431 closed | CLAUDE.md §Architectural Principles now includes the file authority rule: agents must verify they hold R before writing any file; if another agent holds R, produce a draft and request owner review before committing. `docs/process/agent-raci.md §File Ownership` added: 24-row lookup table (file/directory, Owner R, Required Consultant C) covering all major files; §Near-Miss section documents PR #429 incident (two substantive errors caught by retroactive DA+Ar review); §What 'C' Means in Practice defines the correct draft → C review → incorporate → commit sequence. HORIZON mode in `docs/process/agents.md` expanded from one-liner to five numbered sweep steps; step 5 = FILE AUTHORITY AUDIT. PR #432 (CLAUDE.md rule) + PR #433 (table + HORIZON step). | 2026-05-23 |
| Issue #428 prerequisites complete — trajectory endpoint unblocked | (1) ADR-010 D6 amendment: M9 deferral of MDA floors; ecological WARNING at 1.0; M10-B schema. (2) CM reference range consultation: gdp_growth [-0.10, 0.06]; reserve_coverage_months [0.0, 12.0]; unemployment_rate [0.02, 0.30] inverted; net_enrollment_secondary [0.40, 1.00]; health_expenditure excluded; Tier 3 floor. (3) ADR-010 D2 amendment: scoring_basis three-value enum (percentile_rank / normalized_absolute / boundary_proximity); single-entity contract; step_metadata JSONB. DA+Ar review: scoring_basis ecological value corrected to "boundary_proximity" (was "percentile_rank" — semantically incorrect); db_reads M10 comment fix. PR #429 merged. Issue #428 closed. | 2026-05-23 |
| EL Decisions A/B/C recorded — trajectory endpoint implementation unblocked | Decision A: MDA floor overlays deferred to M10; ecological WARNING at 1.0 authorized for M9; CM consultation on reference ranges authorized; M10-B schema confirmed. Decision B: Path A selected — normalized absolute composite for single-entity trajectory; four curves; Tier 3 confidence floor; CM reference range consultation is the hard next gate. Decision C: step_metadata JSONB option (a) confirmed. All recorded on Issue #366. Issue #193 updated. PR #427. | 2026-05-22 |
| Six-agent parallel consultation — DA-F2/F4/F5 pre-implementation record | CM, UX Design Thinking, UX Designer, Data Architect, QA Lead, Frontend Architect activated simultaneously. Key rulings: (1) CM: single-entity normalized absolute composite is methodologically sound (Tier 3 floor); Path A requires pre-declared reference ranges before endpoint can compute. (2) CM: composite-score MDA floors cannot be defined without backtesting — defer to M10; ecological WARNING at 1.0 is only M9 exception. (3) UT: four-curve Mode 1 Greece is M9 exit requirement; DA-F4 is demo scope decision. (4) UD: Path A rulings (strokeDasharray="8 3", legend labels, tooltip) and Path B rulings (40px amber strip, approved text) recorded. (5) DA: step_metadata JSONB confirmed valid; scoring_basis field for Path A; single_entity_advisory at response root for Path B; mda_floors structural error in stub identified. (6) QA: AC-009 corrected (3 shock ReferenceLines, not 6+); AC-015 broadened to all four Lines. (7) FA: atom unchanged for all paths; connectNulls={false} confirmed on all 8 Lines; single_entity_advisory must not be atom field. Three EL decisions still pending. PR #426. | 2026-05-22 |
| Architect Agent review of Data Architect findings — three EL decisions required | Data Architect found 5 schema gaps (DA-F1–F5). Architect dispositions: DA-F1 stub adequate; DA-F2 defer MDA floor overlays to M10 + CM consultation; DA-F3 correct as-is; DA-F4 CRITICAL (Greece Mode 1 blocked — single-entity null; CM + ADR-010 amendment required); DA-F5 step_metadata JSONB approach confirmed. Arch-F1: "STANDARD" → "ROUTINE" correction applied. Three EL decisions pending. PR #425. | 2026-05-22 |
| UX Designer sign-off — conditional on CVD | 4/5 items confirmed (layout, stacking, compact row, badge). Colors pending MV-001. PR #423. | 2026-05-22 |
| M9 FA brief — three-agent review complete | All 10 findings INCORPORATE. Compact alert row (UD-F1), badge 11px (UD-F2), act() boundary (QA-F1), MV gates added. PR #422. | 2026-05-22 |
| M9 FA brief authored — instrument cluster | Frontend Architect Agent: EXECUTE. All 11 deferred brief items (FA-C1–FA-C5 from ADR-008; FA-R1, FA-R2, FA-R4/UD-R1, FA-R5, UD-R2, UD-R3 from ADR-010) resolved with named acceptance criteria. Key decisions: Zustand atom for Zone 1 atomicity (DD-012); merged-key `<Area>` for divergence fill (DD-013); 32-char step annotation constraint (DD-014); 280px control plane confirmed (DD-015). Layout constants: 480px trajectory / 240px co-primary / 280px control plane at 1024×768; 580/400/280 at 1280×800. CVD validation procedure specified; result pending UX Designer sign-off. Brief at `docs/frontend/fa-brief-m9-instrument-cluster.md`. | 2026-05-22 |
| ADR-010 drafted, panel-reviewed, and accepted | Architect Agent: EXECUTE. 10 decisions (Recharts SVG, GET /scenarios/{id}/trajectory endpoint, shared state atom, governance null rendering, composite-score-level MDA floors, Mode 1 step axis annotation, Mode 3 live A/B ghost curves and divergence fill, policy/shock markers, confidence tier visual, ADR-007-gated band infrastructure). 11 findings (4 INCORPORATE applied, 5 BRIEF, 1 LOG, 1 combined). EL approved all 4 INCORPORATE items with rationale recorded in `docs/adr/reviews/ADR-010-panel-review.md`. ADR-010 status: Accepted. M9 FA brief is unblocked. | 2026-05-22 |
| ADR-008 accepted — PR open | All 6 INCORPORATE items applied to ADR-008. EL decision recorded in `docs/adr/reviews/ADR-008-panel-review.md`: all 6 approved; FA-C3 ruling = Option A (stacked forms, ~280px control plane zone). ADR-008 status: Accepted. ARCH-002 in backlog: ACCEPTED. Issue #397 closed. Five FA brief items (FA-C1–FA-C5) deferred to M9 FA brief — none reverse an ADR decision. | 2026-05-22 |
| ADR-008 panel review artifact created — PR #417 | Full three-agent panel review completed and captured as `docs/adr/reviews/ADR-008-panel-review.md` (first instance of new artifact type). 12 findings registered: 4 from UX Designer (UX-F1–UX-F4), 5 from Frontend Architect (FA-C1–FA-C5), 3 from Chief Methodologist (CM-1–CM-3). Architect dispositions: 6 INCORPORATE, 3 BRIEF, 1 JOINT EL+UX RULING → BRIEF, 1 LOG, 1 BRIEF+Open Risks. FA concurrence recorded. EL decision record left blank for EL to complete. CLAUDE.md §Canonical Artifact Locations and CODING_STANDARDS.md §ADR Requirements updated to standardize panel review process for all future ADRs. | 2026-05-22 |
| ADR-008 drafted — PR #416 | Architect Agent: EXECUTE activated. Read all required documents (backlog, agent-raci, Issue #364, first-principles-depth, north-star, information-hierarchy, user-journeys). 17 decisions covering viewport inversion, zone assignments, all three modes, blue/orange cross-layer visual system, confidence tier differentiation, Mode 1 step annotation (fixture CI gate), live A/B comparison (automatic), control plane reserved zone. Status: Proposed — pending four-member panel review (UX Designer, Frontend Architect, Chief Methodologist, Engineering Lead). | 2026-05-22 |
| RACI-grounded ADR panel composition rule — added to #405 scope | ADR-008 panel omitted Frontend Architect despite FA being C on all architectural decisions per agent-raci.md row 1. Root cause: panel copied from M8 critique panel (conceptual framing question) rather than derived from the RACI. Rule added to Issue #405 scope: before naming any ADR panel, consult agent-raci.md; any R or C agent must be included or exclusion documented. Implementing agent is always required. Minimum panels by ADR type: frontend ADR → Frontend Architect; engine ADR → Chief Engineer; data ADR → Chief Methodologist; UX ADR → UX Designer. ADR-008 (Issue #397) is the first application of the corrected rule — FA already added to that panel this session. | 2026-05-22 |
| M12 renamed — "Active Control and External Sector" | Previous GitHub title "Analyst Tooling and External Sector" undersold Mode 3; roadmap doc used a third variant "Transformation and External Sector". Renamed to "Active Control and External Sector" — names the two user-facing deliverables (Mode 3 and the external sector module) without naming the matrix engine migration as the lead. GitHub milestone description field also confirmed stale. Milestone registry gap filed as #412 (M9, near-term). | 2026-05-22 |
| Board cleanup — re-milestone SA-*/backtesting family M9→M10; #394 M9→M12; 6 horizon labels added | 10 issues re-milestoned M9→M10 (#91, #103, #116, #118, #119, #122, #123, #160, #173, #393) — SA-*/backtesting standards family moves with #43 (confidence_tier split) as an engine integrity prerequisite. #394 (multi-scenario comparison >2) re-milestoned M9→M12 — roadmap explicitly places this in M12 as the TC-3 Kenya budget planning enabler. horizon:near-term added to #271, #272, #273, #274, #275; horizon:long-term added to #278. Post-cleanup: 0 open issues without milestone, 0 without horizon label. | 2026-05-22 |
| WorldSim roadmap document created — docs/roadmap/worldsim-roadmap.md | M9–M13 arc established through demo-anchored working-backwards analysis. Demo 3 at M10 (WorldSim works: all four axes, second country, instrument cluster). Demo 4 at M12 (Hormuz closure on a standard laptop — democratization mission made concrete). Long-term resolution spectrum (entity template library), two-path infrastructure model. CLAUDE.md §Milestone Roadmap compressed to two-paragraph pointer. MILESTONE_RUNBOOK.md §Roadmap Update added as mandatory exit ceremony step. milestone-roadmap-m6-m8.md archived with header note. ADR numbering registry established: ADR-007=synthetic data, ADR-008=UX architecture, ADR-009=engine computation, ADR-010=trajectory view. Architecture Backlog at docs/architecture/backlog.md prevents informal ADR number assignment. | 2026-05-22 |
| Issue #365 closed — UX document updates PR #399 | north-star.md: §1 replaced with §Primary Cognitive Tasks by Mode (three per-mode formulations; M4-era 'threshold alarm detection' superseded); §2 extended to three modes; personas.md reference added. information-hierarchy.md: Governing Principle updated to per-mode framing; Zone 1 restructured — entity selector as persistent header, trajectory view as 1A primary, MDA alert panel 1B, PMM 1C, four-framework current position 1D; radar chart moved to Zone 2 (2A); EntityDetailDrawer demoted to detail/methodology surface; COMPARE_VIEW replaced with three-mode conditional (single-entity Mode 2: divergence timeline; multi-entity Mode 2: DeltaChoropleth; Mode 3: automatic live A/B); DeltaChoropleth deprecated for single-entity and Mode 3; Control Plane Reserved Zone section added; M9 hierarchy decisions table (8 decisions). user-journeys.md: Journey A Step 3 separated into advance (3a) and inspect (3b); Journey B Step 5 reframed as Mode 3 control input; Journey C (Mode 3 active control — Eleni February 2012) and Journey D (demonstrative entry state — Aicha Mbaye) added; dependency map extended to 15 rows across all four journeys and three modes. Issues #366 and #368 unblocked. | 2026-05-21 |
| EL Decisions 1/2/3 recorded — Issue #364 closed; Issue #365 unblocked; four gap issues filed | Decision 1 (north-star): per-mode formulation adopted — Mode 1: trajectory reconstruction AND historical pattern recognition; Mode 2: threshold-safe path construction; Mode 3: real-time steering within human cost constraints. All 13 marquee cases validated. Two M11 gaps correctly surfaced (Argentina/Ukraine political economy constraint); two engineering gaps filed (#393 Mode 1→2 transition, #394 multi-scenario comparison). Decision 2 (viewport): instrument cluster as primary viewport adopted; EntityDetailDrawer demoted to detail/methodology; entity selector as persistent header element. Decision 3 (comparison): conditional switch extended to Mode 3 — automatic live A/B with no invoke required; DeltaChoropleth deprecated for single-entity and Mode 3. Four gap issues: #392 (M11 political economy), #393 (Mode 1→2 transition), #394 (multi-scenario), #395 (step_event_label mandatory). Issue #364 closed. Issue #365 (UX document updates) now unblocked. | 2026-05-21 |
| Issue #363 implemented — UX first-principles depth (PR #390 merged) | docs/ux/design-thinking/worldsim-ux-architecture-first-principles-depth.md. Six gaps closed. Gap 1A: Mode 3 walkthrough for Eleni (February 2012), 10-component Frontend Architect requirement table. Gap 1B: mandatory Mode 1 step axis annotation — three fixture fields (effective_from, step_event_label, step_significance); missing step_event_label on SIGNIFICANT steps is an incomplete fixture. Gap 2: three analogy breaks qualified (atomic simultaneous updates; entity selector always visible; Tier 4 instrument visual differentiation). Gap 3: blue/orange cross-layer visual system for policy inputs vs. exogenous shocks; causal attribution in alert text is the negotiating instrument. Gap 4: Mode 3 live A/B comparison is automatic — any control input creates the split; ghost baseline at 50% opacity with divergence fill region. Gap 5: mode transition design — persistent vs. mode-specific instruments; single modal confirmation only for unsaved state loss. Revised six governing premises: Premise 3 mandated with Mode 1 step annotation (most consequential); Premise 4 extended for multiple Mode 1 cognitive tasks; Premise 6 new (methodology as Zone 2 mandatory). Issue #364 unblocked. | 2026-05-21 |
| Issue #387 implemented — persona-grounded UX review (PR #388) | docs/ux/design-thinking/persona-grounded-ux-review.md. Three activations: UX Design Thinking Agent (Q1–Q3), Development Economist (Eleni February 2012 walkthrough), Political Economist (Andreas Preparatory state). Key finding: Case B holds for all five personas architecturally; four specification extensions required. Most consequential: step axis annotation (calendar date + event label) is mandatory in Mode 1 — without it, Premises 3 optimizes for Personas 1 and 2 while Personas 3 and 5 cannot orient. Issue #363 must accompany Persona 2 Gap 1 walkthrough with parallel Mode 1 specification for Persona 3 pattern recognition. | 2026-05-21 |
| Issue #362 implemented — user persona document | docs/ux/personas.md (1352 lines). Five personas (8 dimensions each): Programme Analyst, Finance Ministry Negotiator, Political Advisor, Academic Researcher, Institutional Decision-Maker. Six entry states with 60-sec opening screen requirements and failure conditions. Five primary marquee cases (European sovereign debt history) with testable exit criteria. Five secondary marquee cases (Argentina, Egypt, Sri Lanka, Ukraine, Zambia) with structural gap verdicts. Three tertiary use cases as ingredient specifications (Canadian steel tariffs, Hormuz closure, Kenya budget). Product scope statement. Synthetic data framework integrated for Cases E/TC-2/TC-3. Platform principle applied throughout. EL review required before canonical. PR #385. | 2026-05-20 |
| Issue #360 implemented — 15 agent working agreements | docs/process/agents.md: 15 working agreements appended (one per agent) in each agent's own voice. Five sections: understanding of the mission, unique contribution, observable behavioral commitments, where the agent asks for help, where it offers help. PR #384. | 2026-05-20 |
| Founding document committed | docs/vision/worldsim-founding-document.md created from April-May 2026 founding conversations (six parts: The Problem, The Analogy, The Principles, The Architecture, The Vision, Honest Limitations). CLAUDE.md §Founding Document reference added. PR #383. | 2026-05-20 |
| Architect Agent consultation — simulation graph mental model | EL's BST mental model is approximately correct for the administrative hierarchy (parent_id) but the propagation medium is the relationship graph, not the hierarchy. Two-graph architecture: Graph 1 (parent_id = identity/scope); Graph 2 (relationships list with relationship_type = propagation medium). Events propagate along typed edges; no rollup. Each entity computes from events it receives. | 2026-05-20 |
| Issue #370 (M8 formal close issue) — still open | Work is done (v0.8.0 released, retrospective complete) but the issue itself was not explicitly closed this session. Needs explicit close. | 2026-05-20 |
| M8 formal close complete | All six exit gates satisfied; v0.8.0 tagged and released; Issue #209 closed; CHANGELOG updated; demo recording attached to GitHub release | 2026-05-19 |
| Issue #361 Chief Methodologist consultation — synthetic data framework | docs/architecture/synthetic-data-consultation.md (41.5k chars, 560 lines). Five questions answered. Method hierarchy: Bayesian > MICE > Bootstrap > structural extrapolation > structural absence. Three-condition meaninglessness threshold. MDA tier table (full/advisory/exploratory/none). Anomaly detection requires TSC sign-off, opt-in, Mode 3 excluded, governance indicators excluded. ADR-007 outline produced. PR #373. | 2026-05-19 |
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
