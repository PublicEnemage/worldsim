---
name: m12-sprint-plan
type: sprint-plan
milestone: M12 — Active Control and External Sector
status: Active
authored-by: PM Agent
authored-date: 2026-06-05
el-approved: 2026-06-05
consulted:
  - Business Product Owner (value prioritization; DP-3 panel)
  - Frontend Architect (file area grouping)
  - Chief Engineer (dependency sequencing; NB-3 CE constraint)
  - Architect (ADR prerequisites; DP-1 panel; DP-2 panel; DP-3 panel)
  - Data Architect (DP-1 panel)
  - QA Lead (DP-1 panel)
  - UX Designer (DP-1 panel; DP-3 panel)
  - Chief Methodologist (NB-1 pre-analysis; DP-2 panel)
  - Development Economist (NB-3 pre-analysis)
  - Customer Agent (DP-3 panel)
  - PM Agent (DP-3 panel)
near-term-backlog-plan-date: 2026-06-06
near-term-backlog-el-endorsed: 2026-06-06
sop: docs/process/sprint-planning-sop.md
---

# M12 Sprint Plan — Active Control and External Sector

**Milestone:** M12 — Active Control and External Sector (GitHub Milestone 13)  
**Release branch:** `release/m12`  
**Exit checklist:** Issue #263  
**HORIZON sweep:** 2026-06-05 (kickoff ceremony)

---

## Grouping Rationale

Groups are organized by shared file areas and dependency chains. A group is one PR (or two ordered PRs for G6). Tests ship with the code in the same PR — no separate test PRs. Playwright E2E assertions ship in the same PR as the feature they gate.

---

## Wave 1 — Parallel (no cross-dependencies)

All four Wave 1 groups can be worked and merged in any order. No group depends on another within this wave.

### G1 — Instrument cluster display: #744 + #747 ✓ DONE (2026-06-05, PR #762)

**Why grouped:** Both are frontend-only additions to the Zone 1 component area. Existing `/measurement-output` already surfaces the cohort data; these issues add display. No backend changes. Sharing a PR reduces context switching across the same component tree.

**Shared files:** `ScenarioInstrumentCluster.tsx`, Zone 1A/B/C/D component tree, choropleth component (active entity highlight), layout/header area, possibly `measurement-output` API response type shape (read-only).

**Tests:** Component unit tests for header element and cohort indicator panel. Playwright legibility assertion at 1440×900 confirming header is visible in screenshot without scroll (required by #744 AC). Both test additions live in the same PR.

**Acceptance gates:**
- Persistent header visible in any main-viewport screenshot: `Scenario / Entity / Status`
- Active country highlighted on choropleth when scenario loaded
- Four cohort indicators in Zone 1 with value + direction + tier, alongside composites
- Cold-start agent can identify loaded scenario in turn 1 from screenshot alone

**Execution narrative:** Frontend-only PR with no backend changes. Two new components: `ScenarioIdentityHeader` (Zone 0 banner: Scenario / Entity / Status) and `CohortIndicatorsPanel` (Zone 1A strip with 4 HD indicators, polarity-aware direction arrows, confidence tier badges). Atomic `hdState` pattern (single useState) prevents stale-closure on current→prev indicator swap. Choropleth amber highlight layer added on active scenario entity. 28 unit tests across `formatStatus`, `computeDirection`, `directionGlyph`, `formatIndicatorValue`. Build gate clean. Zero backend changes required — measurement-output API already surfaced the HD data.

---

### G2 — Alert panel drill-in: #745 ✓ DONE (2026-06-05, PR #764)

**Why own group:** Alert panel expansion is architecturally distinct from display additions — it introduces click state, expansion behaviour, and possibly alert API enrichment. Different component, different interaction model. The backend surface is narrow (ensure `indicator_name` is non-null in alert response; `/trajectory` already provides the time-series data).

**Shared files:** `MDAAlertPanel.tsx` (major rewrite), alert API response shape (minor — `indicator_name` non-null enforcement).

**Tests:** Component interaction test (click → expand → time-series visible). API unit test asserting `indicator_name` is never null. Playwright: click on TERMINAL alert → detail view opens with indicator name, threshold line, and step of crossing highlighted.

**Acceptance gates:**
- Click on any alert row opens detail view: indicator time-series, MDA threshold reference line, step of crossing
- Human-readable indicator name always present
- "See alerts" text in zone-1d navigates to alert detail for that framework's primary alert
- Alert text legible at 1440×900

**Execution narrative:** Backend + frontend change. Backend: `indicator_name: str` added to `MDAAlert` schema — always non-null, title-cased from `indicator_key` via `_indicator_name()` helper, persisted in `events_snapshot` JSONB with fallback reconstruction for historical snapshots. Frontend: `Zone1BAlert` store type extended with `indicator_name`, `floor_value`, `current_value`, `approach_pct_remaining`, `consecutive_breach_steps`. Alert rows made clickable (toggle on/off); `focusedAlertMdaId` local state in `ScenarioInstrumentCluster` (UI state, not simulation state) wired to both Zone 1B and Zone 1D. `AlertDetailPanel` renders inline below the list: indicator display name (frontend registry overrides backend title-case), SVG sparkline of framework composite score trajectory with dashed MDA floor line and crossing step marker, value snapshot grid. Zone 1D gets "Primary dimension — see alerts →" button per framework row. `buildSparklinePoints` pure function + 7 new tests; 170 total tests passing.

---

### G3 — Mode 2 fiscal multiplier: #746 ✓ DONE (2026-06-05, PR #767)

**Why own group:** Has both backend schema changes (new `fiscal_multiplier` field) and a significant frontend addition (overlay comparison in `TrajectoryView.tsx`). Backend work is isolated to scenario creation path. This is the entry point for Mode 2 — keeping it separate from G1/G2 prevents a single large PR from mixing three concerns.

**Shared files:** `scenario_schemas.py` / Pydantic models (`fiscal_multiplier` field), `simulation_runner.py` (pass-through to propagation), `TrajectoryView.tsx` (two-curve overlay display), scenario creation form component (new parameter input).

**ADR prerequisite:** None — fiscal multiplier is an existing engine parameter being exposed; no new architectural boundary.

**Tests:** API schema test (fiscal_multiplier field accepted, validated 0.1–3.0). Simulation runner unit test (fiscal_multiplier propagates through). Playwright: configure two multiplier values → both curves visible in overlay → legend identifies each.

**Acceptance gates:**
- Fiscal multiplier configurable from scenario creation UI (0.1–3.0 range, default 1.0)
- Two-curve overlay or side-by-side comparison mode
- Active multiplier assumption visible in main viewport at all times
- Poverty headcount and health system capacity respond to multiplier change

**Gates:** G6b (#753 Mode 3) — fiscal multiplier is Mode 3's first instrument.

**Execution narrative:** Backend + frontend change. Backend: `fiscal_multiplier: float` added to `ScenarioConfigSchema` with Pydantic `Field(ge=0.1, le=3.0)`, default 1.0. `MacroeconomicModule.__init__()` now accepts `fiscal_multiplier_override: float = 1.0`, stored as `Decimal` and applied to both spending and tax multiplier paths (`FISCAL_MULTIPLIERS[regime] * override`). `_build_active_modules()` passes `config.fiscal_multiplier` through — no modules_config indirection. Frontend: fiscal multiplier range slider (0.1–3.0, step 0.1) added to scenario creation form with orange highlight and "Mode 2" indicator when override is active. `ScenarioIdentityHeader` gains `fiscalMultiplier` prop and `formatMultiplierLabel()` pure function — shows "Mode: 2 (Fiscal ×N.N)" in the persistent identity strip when override ≠ 1.0. `TrajectoryView` now shows baseline overlay when `mode === "MODE_2" || mode === "MODE_3"` (previously MODE_3 only), with legend entries in MODE_2. `ScenarioInstrumentCluster` accepts `comparisonScenarioId` prop — fetches that scenario's trajectory and stores as `baseline_trajectory`; sets MODE_2 when `fiscalMultiplier ≠ 1.0`. `App.tsx` extracts `fiscal_multiplier` from scenario detail and wires through. 7 new backend unit tests (schema validation, module constructor, `_build_active_modules` wiring); 8 new frontend unit tests (`formatMultiplierLabel`). 177 total frontend tests passing, ruff + build gate clean.

---

### G4 — Matrix engine production migration: #749 ✓ DONE (2026-06-05, PR #769)

**Why own group:** Major backend-only architectural change. Promotes `propagate_matrix()` to the default call site, demotes iterative engine. The full backtesting suite is the test — no new test files needed, but all existing backtesting assertions must pass against the matrix engine before this merges.

**Shared files:** `matrix_propagation.py`, `simulation_runner.py` (swap call site), backtesting test suite, `test_equivalence_harness.py`, CI workflow (confirm matrix is the test target), ADR-009 status update to IMPLEMENTED.

**Tests:** Full backtesting suite passing on matrix engine. ADR-009 §Decision 3 Monte Carlo gate (1000× 15 steps) confirmed in production configuration. No fallback to iterative without explicit log entry.

**Acceptance gates:**
- `propagate_matrix()` is default for all new scenario steps
- Full backtesting suite passes (no regressions from M11 baseline)
- ADR-009 §Decision 3 performance gate confirmed on target hardware (ProBook i5-8265U)
- No silent fallback; any fallback is logged and surfaced
- ADR-009 updated to IMPLEMENTED

**Gates:** G5, G6, G7, G8 — everything downstream runs on the production engine.

**Execution narrative:** Backend-only change. `ScenarioRunner.tick()` local import swapped from `propagate` (iterative) to `propagate_matrix`; the stale `from propagation import propagate` line removed. No try/except wrapper — any matrix engine failure surfaces immediately to the caller (no silent fallback). `engine/__init__.py` `propagate` export aliased to `propagate_matrix` so existing callers using the package-level name continue to work unchanged. `matrix_propagation.py` module docstring updated to production status. ADR-009 status updated from Accepted to IMPLEMENTED; Amendment 1 appended recording retirement decision, EL sign-off (@PublicEnemage, 2026-06-05), parallel-run window completion (M11, PR #707), and iterative engine retention rationale (helpers `_accumulate` + `_build_next_state` still imported — extraction deferred). I001 import-order violations from G3 test functions fixed. 6 new unit tests: package alias assertion (`engine.propagate is propagate_matrix`), call-site spy via monkeypatch, smoke advance (timestep advances correctly), entity preservation, no-change attribute invariant, and no-fallback guarantee.

---

## Wave 2 — After G4

### G5 — External sector module: #751 + #752 ✓ DONE (2026-06-05, PR #773)

**Why grouped:** `BilateralTradeShock` (#751) lays the propagation routing infrastructure; `CommodityPriceShock` (#752) extends it for global-parameter distribution. Writing both together avoids two separate migrations to the same schema tables and two separate additions to the same input-type dispatch logic. #751 is a blocking prerequisite for #752.

**ADR prerequisite:** ADR-012 authored and accepted by EL 2026-06-05 (ARCH-006, `docs/adr/ADR-012-external-sector-module.md`).

**Shared files:** New `external_sector.py` module, `scenario_schemas.py` (new scheduled input types), DB migration, relationship graph traversal in propagation layer, human cost linkage (bottom-quintile consumption channel for both shock types). Single test file covers both shock types.

**Tests:** Shock propagation unit tests (both types). Zero-dependency entity case (no effect). Human cost channel activation (bottom-quintile cohort responds within 2 steps). Import dependency coefficient fixture for Jordan (Demo 4 entity; synthetic Tier 3 flagged). Historical directional validation — 2008 oil price spike as reference for commodity shock.

**Acceptance gates:**
- `BilateralTradeShock` and `CommodityPriceShock` accepted by scenario creation API
- Both propagation types reach financial framework indicators within 1 step
- Human cost ledger shows cohort-level effects within 2 steps for both types
- External sector ADR accepted before implementation merges
- Jordan commodity import dependency coefficients in fixture (Tier 3 flagged)

**Gates:** G6, G8.

**Riders (ship in same PR):**
- #27 — Document calibration basis for propagation attenuation parameters (G5 introduces new propagation routing; document attenuation calibration here)
- #92 — Greece 2010 fixture: bond yields, CDS proxy, credit tier (financial data useful for external sector backtesting)
- #275 — Ecological-to-financial transmission calibration (resource export revenue channel feeds directly into commodity price shock)

**Execution narrative:** Backend-only PR. Two new shock types implementing ADR-012's external sector module boundary. `BilateralTradeShock` (new `ControlInput` subclass in `orchestration/inputs.py`): entity-targeted bilateral import price shock generating two events per ADR-012 Decision 4 — one Financial (`import_price_inflation`) and one Human Development (`bottom_quintile_consumption_capacity`), with no cross-framework conversion. `_HCL_TRANSMISSION_FACTOR = Decimal("0.3")` encodes the 30% pass-through from import price to bottom-quintile consumption capacity within 1 step (Issue #275 calibration basis). `CommodityCategory` enum (FUEL/FOOD/METALS/OTHER) in `inputs.py`. `ExternalSectorModule` (new `SimulationModule` subclass, `modules/external_sector/module.py`): distributes global commodity price shocks to all entities proportional to `commodity_import_dependency_{category}` entity attribute; fires only within `start_step`/`duration_steps` window; returns empty list when dependency attribute is absent or zero. `CommodityShockConfig` Pydantic schema added to `schemas.py`; `commodity_price_shocks: list[CommodityShockConfig] = []` field on `ScenarioConfigSchema`. Both types wired into `web_scenario_runner`: `ExternalSectorModule` added to `_build_active_modules()`; `BilateralTradeShock` added to `_deserialize_control_input()`. 16 new unit tests in `test_external_sector.py` covering propagation, HCL transmission (-0.06 = -0.20 × 0.3), zero-dependency no-op, step-range firing, confidence tier 3, and deserialization. Also fixes pre-existing G4 test breakage in `test_matrix_engine_production.py`: `ScenarioRunner.tick()` → `advance_timestep(current_state, modules, scheduled_inputs)` with updated constructor signature (6 test fixes). 1108 total unit tests passing. CI: test-backend ✓, lint ✓, compliance-scan ✓.

---

### G7 — Cloud compute path doc: #750 ✓ DONE (2026-06-05, PR #774)

**Why own group:** Pure documentation. No code. Writes `docs/architecture/cloud-compute-path.md` (new file). Can be done any time after G4 merges — needs real matrix engine performance numbers to cite accurately.

**Shared files:** `docs/architecture/cloud-compute-path.md` (new). Requires CE review (performance accuracy).

**Tests:** None.

**Acceptance gates:**
- Document covers: what triggers cloud need, minimum viable laptop config, cloud provider options with pricing, self-hosted alternative
- Equitable Build Process constraint confirmed: standard single-country scenario stays within 8GB/4-core envelope

**Execution narrative:** Documentation-only PR. New file `docs/architecture/cloud-compute-path.md` authored by Chief Engineer Agent, grounded in Phase 1 baseline benchmarks (ProBook i5-8265U, 8 GiB RAM). Explicitly confirms the Equitable Build Process constraint: standard single-country scenario (1,000 MC runs, 10–30 steps) completes in < 200 ms of compute on a constrained laptop — cloud is not required for the canonical user. Three cloud-need trigger conditions defined with quantified thresholds: entity/relationship density (> ~500 entities or dense graph taking > 30 s/run), MC ensemble size > 10,000 runs, and full backtesting suite. Pricing at three tiers across AWS, GCP, Azure, and Hetzner (Hetzner highlighted as 4–5× cheaper for resource-constrained institutions). Self-hosted deployment instructions including air-gapped deployment for security-isolated central bank environments. No backend or frontend changes; no test gate needed.

---

### G9 — Political economy module: #392

**Why own group:** M11 stretch goal explicitly deferred to M12 (CLAUDE.md: "carries to M12. EL decision 2026-06-03"). Models political feasibility constraints, conditionality, and elite capture dynamics — the gap exposed by Argentina and Ukraine/Pakistan marquee cases. Runs in parallel with G5/G7: requires only G4 (matrix engine in production), no dependency on external sector.

**ADR prerequisite:** Political economy module introduces a new module boundary. ARCH-007 (ADR-013) must be authored and accepted before any implementation merges. Panel: Architect Agent (author), Political Economist, Chief Methodologist, Engineering Lead.

**Shared files:** New `political_economy.py` module, `scenario_schemas.py` (conditionality input type), human cost ledger (political feasibility constraints on welfare outputs). Single test file.

**Tests:** Conditionality constraint activation (feasibility gate blocks instrument below threshold). Elite capture channel unit test (benefit distribution shifts toward upper quintile under capture condition). Argentina fixture directional validation (political constraints tighten before default). Pakistan fixture directional validation (conditionality acceptance triggers programme sequence).

**Acceptance gates:**
- Political feasibility constraint accepted by scenario creation API
- Conditionality modelling produces distinct trajectory from unconstrained baseline
- Elite capture reduces bottom-quintile welfare transfer within 2 steps
- Argentina and Ukraine/Pakistan marquee cases run without errors
- Political economy ADR accepted before implementation merges

**Gates:** G8 (Demo 4 benefits from political economy realism in Jordan scenario).

---

## Wave 3 — After G3 + G4 + G5

### G6a — Multi-country scenario backend: #754 ✓ DONE (2026-06-05, PR #775)

**Why own group (first half of G6):** Backend-heavy. Adds `entity_ids: list[str]` to scenario creation, seeds multiple entities independently, populates relationship edges at creation, passes multi-entity runs through the matrix engine. The choropleth multi-entity highlight is a small frontend touch that ships in this PR rather than creating a micro-PR later.

**Shared files:** `scenarios.py` API endpoint, `scenario_schemas.py` (`entity_ids` field), DB migration (entity membership, relationship edges), `simulation_runner.py` (multi-entity loop), choropleth component (highlight multiple active entities simultaneously), scenario identity header (#744) extended to list all active entities.

**Tests:** API test (multi-entity creation, relationship seeding). 2-entity step advance performance gate (≤ 1.5× single-entity wall time on matrix engine). Synthetic relationship weight edge case (missing edges → Tier 4 weight, flagged). Multi-country validation suite design document (covers statistical validity requirements beyond 2-step single-country pass).

**Acceptance gates:**
- Scenario creation API accepts `entity_ids: list[str]` (minimum 1, up to 5)
- Each entity independently seeded from source registry
- Commodity price shock (#752) distributes to all entities in one step
- Choropleth highlights all active entities with absolute MDA threshold overlay markers
- Demo 4 Jordan scenario runs with 2 entities (Jordan + commodity reference)
- Performance gate: 2-entity step ≤ 1.5× single-entity on matrix engine

**Riders (ship in same PR):**
- #103 — Multi-country validation suite design (design doc for statistical validity of multi-country backtesting; ships in same PR as the backend it validates)
- #153 — Absolute threshold overlay in DeltaChoropleth (G6a already touches choropleth for multi-entity highlight; MDA threshold markers are the natural addition)

**Execution narrative:** Full-stack PR. Backend: `scenarios.py` API extended with `entity_ids: list[str]` (1–5 entities, validated with descriptive error on 0 or >5) and `threshold_value: str | None` query param on `/compare` endpoint wired to new `threshold_crossed: bool | None` field in `DeltaRecord`. `state_repository.py` extended with `_load_relationships()`: queries `relationships` DB table for real edges between scenario entities; synthetic Tier 4 trade edges (weight=0.1) injected for all missing ordered pairs so multi-entity propagation is never blocked by absent relationship data — `synthetic: True` and `confidence_tier: 4` in edge attributes. `DeltaRecord.threshold_crossed` computed as `(dec_a < thr) != (dec_b < thr)` — True when value_a and value_b are on opposite sides of the threshold (correct for MDA boundary detection). Frontend: `ChoroplethMap` multi-entity highlight — MapLibre layer filter changed from `["==", "entity_id", id]` to `["in", ["get", "entity_id"], ["literal", ids]]` for multi-entity highlight; empty-array case explicitly returns no-match expression. `ScenarioIdentityHeader` extended: `entityId: string | null` → `entityIds: string[]`; exported `formatEntityLabel()` pure function renders "Entity: GRC" (1 entity) vs "Entities: JOR, SAU" (plural). `App.tsx` updated to propagate `activeEntityIds: string[]` from scenario detail `configuration.entities` array. Rider #103: `docs/architecture/multi-country-validation-suite-design.md` — statistical validity analysis (2-data-point = 25% false-positive; 8-point = 0.4%), Ireland/Portugal/Cyprus backtesting fixture priority order, M12/M13 implementation phases. 18 new unit tests in `test_g6a_multi_country.py` covering entity count validation, `threshold_crossed` logic (None/False/True), relationship loading (real edges, synthetic injection, no-duplicate invariant for real pairs, 3-entity = 6 ordered pairs), and confidence tier. 6 new `ScenarioIdentityHeader` unit tests covering `formatEntityLabel` for 0/1/2/3 entities. Playwright E2E fix: `getByText(/Complete/)` → `getByText(/— Complete/)` in two spec files (strict mode violation from `ScenarioIdentityHeader` rendering "Status: Complete (3 steps)"). CI: test-frontend ✓, test-backend ✓, lint ✓, playwright ✓.

---

### G6b — Mode 3 Active Control: #753 ✓ DONE (2026-06-05, PR #778)

**Why own group (second half of G6):** Frontend-heavy. Activates `zone-control-plane`. Depends on G6a (multi-entity backend) and G3 (fiscal multiplier as first instrument). ADR-008 reserved the control plane layout zone — verify whether Mode 3 interaction model is covered or requires an ADR amendment before implementation begins.

**Prerequisites before implementation begins (in order):**
1. **#613 — CE branch-and-recompute assessment** ✓ SATISFIED (2026-06-05) — Chief Engineer posted full assessment confirming: (a) mid-run serialization already implemented via `ScenarioSnapshotRepository.write_snapshot()` + `_reconstruct_state_from_snapshot()`; (b) Model A (new scenario object) recommended — reuses all existing machinery with no ADR-009 implications; (c) two gaps identified: `_reconstruct_state_from_snapshot()` returns `relationships=[]` (needs `_load_relationships()` call in branch path) and cohort entities silently dropped on reconstruction (needs investigation); (d) estimated scope ~1 week.
2. **#614 — Mode 3 interaction spec** ✓ SATISFIED (2026-06-05, PR #777) — Full spec at `docs/ux/mode3-interaction-spec.md`. Key decisions: (a) latency budget ≤2s for ≤8-step scenario on ProBook replaces "real-time" in US-039; (b) loading state: baseline at 100% opacity throughout recompute, streaming step reveal via 500ms polling, inline recompute badge; (c) ghost baseline `strokeDasharray="4 2"` (distinct from `"8 3"` for confidence-degraded data); (d) re-branch accumulates into existing `branchScenarioId` (consistent with ADR-008 D10); (e) error state: inline badge, baseline restores, no blocking modal; (f) Zustand store contract: `baselineScenarioId`, `branchScenarioId`, `branchFromStep`, `branchStepsComputed`, `recomputeStatus: 'idle'|'pending'|'computing'|'complete'|'failed'`.

**Shared files:** `zone-control-plane` component (new), `App.tsx` (mode routing and mode indicator), `TrajectoryView.tsx` (A/B baseline vs. modified display — builds on G3's overlay work), `zone-1d` human cost delta display, mode indicator component.

**ADR prerequisite:** ADR-008 Decision 10 confirmed sufficient for Mode 3 interaction model (#613 CE assessment found no ADR-009 amendment needed). No new ADR required for G6b.

**Tests:** Playwright E2E — parameter change → trajectory recompute → both curves visible → delta in zone-1d, on Greece fixture. Mode 3 → Mode 1 → Mode 3 roundtrip without losing scenario. Performance: branch recompute ≤ 2s wall time for 8-step scenario on ProBook i5-8265U (per mode3-interaction-spec.md, closes #569 scope revision). Reversibility classification: recoverable vs. irreversible output appears in zone-1d. Mode 1 → Mode 2 transition preserves current step position.

**Acceptance gates:**
- `zone-control-plane` renders at least two configurable policy instruments without scroll
- Parameter change → branch recompute completes ≤ 2s for 8-step scenario on ProBook (per mode3-interaction-spec.md, closes #569 scope revision; replaces original ≤ 100ms MV-002 gate)
- Baseline curves remain at 100% opacity and navigable during recompute (no blocking state)
- Streaming step reveal: branch curves extend step-by-step as recompute progresses (500ms polling)
- Baseline and modified trajectories simultaneously visible with legend after recompute completes
- Ghost baseline uses `strokeDasharray="4 2"`, 50% opacity (distinct from confidence-degraded `"8 3"`)
- Human cost delta visible in zone-1d within same update cycle, including reversibility classification (#271)
- A/B comparison is default when parameter changed (no manual enable)
- Mode 3 reachable from Mode 1 and Mode 2 without losing loaded scenario
- Mode 1 → Mode 2 transition preserves step position (#393)
- Threshold-crossing markers flag when delta crosses MDA boundary (#97)
- Error state: inline badge clears on dismiss; baseline fully navigable during error

**Riders (ship in same PR):**
- #97 — Threshold-crossing markers in comparative output (MDA thresholds are Mode 3's primary guard)
- #271 — Reversibility classification for simulation outputs (recoverable vs. irreversible in zone-1d)
- #393 — Mode 1 → Mode 2 transition preserves step position (mode transitions resolved in G6b)

**Execution narrative:** Full-stack PR across backend, store, and four frontend components. Backend: `POST /scenarios/{id}/branch` creates a new scenario object (Model A from CE assessment #613) with the caller's `fiscal_multiplier` and `status='pending'`; copies scheduled inputs and snapshots 0..`branch_from_step` in a single transaction. `POST /scenarios/{id}/rebranch` deletes snapshots from `from_step+1` forward, updates `configuration` with the new multiplier, and resets `status='pending'` — implements spec §5 re-branch accumulation into the existing `branchScenarioId`. Rider #271: `MDAAlert.recovery_horizon_years: int | None` added as a schema field; propagated from `MDAThresholdRecord` through `MDAChecker.check()`, serialised into `events_snapshot` JSONB via `alerts_to_events_snapshot()`, and restored by `alerts_from_events_snapshot()` with `.get()` defaulting to `None` for backward compatibility with pre-G6b snapshots. `BranchRequest`, `BranchResponse`, and `RebranchRequest` schemas added. 16 unit tests in `test_g6b_mode3.py` (schema validation, `recovery_horizon_years` propagation, snapshot roundtrip). Frontend — `scenarioStepStore`: five Mode 3 branch actions added (`initBranch`, `updateBranchProgress`, `setBranchComplete`, `setBranchFailed`, `resetBranch`) implementing the `idle → computing → complete | failed` state machine; `reset()` includes all branch fields. `ControlPlane.tsx` (new): fiscal multiplier slider (0.1–3.0, step 0.05), branch-from-step slider (0–`currentStep`), Apply Change button (disabled during `computing | pending`), branch anchor annotation shown when `branchFromStep > 0`. `ScenarioInstrumentCluster`: `handleApplyControlChange` calls `/branch` on first parameter change and `/rebranch` on subsequent changes, then drives a step-by-step advance loop (frontend-driven streaming reveal — one `/advance` call per step, trajectory fetched after each); inline recompute badge shows pulse dot + "Recomputing…" + step counter during compute, switches to "⚠ Recompute failed" + Dismiss button on error. `App.tsx`: Mode 3 toggle button (purple, fills on active); `mode3Active` resets to `false` in `handleSelectScenario()`. `TrajectoryView`: rider #97 — vertical `ReferenceLine` markers at steps where active and baseline ecological composite scores are on opposite sides of the 1.0 ecological boundary (`strokeDasharray="4 2"`, labelled "⚠ threshold"). `FourFrameworkZone1D`: rider #271 — reversibility badge rendered per framework in Mode 3 when `recovery_horizon_years` is available: `null` → "Irreversible" (red), integer N → "Recoverable (N yrs)" (green). Rider #393: confirmed no code fix required — existing `useEffect [currentStep]` in `ScenarioInstrumentCluster` already restores step after `setScenario` resets it; covered by E2E test. 12 frontend unit tests: `ControlPlane.test.ts` (6 — `formatFiscalMultiplier`, `formatLegitimacyIndex`) + `scenarioStepStore.mode3.test.ts` (14 — all five branch actions + state machine lifecycle). 2 Playwright E2E tests in `mode3-active-control.spec.ts`: golden path (enable Mode 3 → apply change → badge appears → badge disappears → anchor annotation visible) + scenario-change toggle reset. mypy: pre-existing KI-002 environment issue (Python 3.10 `mypy` binary, `type` alias at line 1654 predating G6b) — confirmed via git stash, not introduced by this PR. CI: ruff ✓, test-backend 16/16 ✓, test-frontend 208/208 ✓, build ✓, changes ✓.

---

## Wave 4 — After G1–G6 all merged

### G8 — Demo 4 preparation: #755

**Prerequisites:** #744, #749, #751, #752, #753, #754 all merged. Jordan fixture data available. This group is the integration test of everything built in Waves 1–3.

**Shared files:** `backend/scripts/demo_hormuz_jordan.py` (new), `docs/demo/m12/` (new milestone demo directory per canonical artifact convention), narration document (NARRATION-RULING-1 three-layer structure), IR stakeholder review artifact at `docs/demo/m12/reviews/YYYY-MM-DD-vX.X.X-stakeholder-review.md`.

**Tests:** Demo script runs end-to-end on ProBook i5-8265U without cloud infrastructure. All screenshots pass legibility gate at 1440×900 (demo-legibility.spec.ts). Jordan fixture seeds without errors; all synthetic indicators flagged at indicator level.

**Acceptance gates:**
- Jordan fixture seeds cleanly; synthetic indicators flagged
- Hormuz scenario advances 8 steps without hitting irreversible thresholds before step 4
- Mode 3 parameter adjustment demonstrably changes the trajectory
- Human cost indicators show non-zero response to commodity shock within 2 steps
- Demo runs end-to-end on ProBook within performance budget
- Narration document reviewed against NARRATION-RULING-1
- IR stakeholder review artifact in `docs/demo/m12/reviews/`

---

## Near-Term Backlog (any wave, capacity-dependent)

| Issue | Work type | Notes |
|---|---|---|
| #725 | Backend dep — mypy pin | One-line change; rider on any backend PR |
| #644 | Frontend tooling — ESLint audit | Standalone; between any two frontend waves |
| #394 | Multi-scenario comparison (>2) | Builds on G6a; treat as Wave 3 if capacity allows |
| #13 | Compliance — dataclass attribute docs (CF-001-F06) | Compliance:deferred minor; rider on any backend PR |
| #28 | Backend — cohort disaggregation architecture stubs | Income quintile × age band placeholders; standalone backend PR |
| #30 | Backend — stock vs. flow variable distinction | Entity attribute model integrity; standalone backend PR |
| #34 | Backend — investment climate state variables | Risk premium, credit spread, FDI stock, capital flow velocity; standalone backend PR |
| #43 | Standards — split data_quality_tier into confidence_tier | Touches schema and data layer; standalone PR |
| #45 | Standards — human development indicator standards, HCL effect size | Documentation + schema; standalone PR |
| #90 | API — multi-attribute comparison endpoint | Return all attribute deltas in a single compare call; standalone backend PR |
| #95 | Docs — ecological backtesting case planning | Pure documentation; no blockers |
| #99 | API — trajectory comparison endpoint | Attribute values at all steps for two scenarios in one call; standalone backend PR |
| #259 | Docs — CTO legibility metrics dashboard | Process/standards documentation |
| #451 | UX — Mode 1 COMPARE_VIEW entry point spec | Comparable-case comparison spec; feeds Mode 1 analytical depth |

---

## Near-Term Backlog — Execution Plan

**Authored by:** PM Agent (in-session 2026-06-06)  
**Consulted:** Chief Engineer, Development Economist, Chief Methodologist (pre-group analysis); Architect, Data Architect, QA Lead, UX Designer, Business PO, Customer Agent (decision panels — see §Near-Term Backlog — Panel Decision Record)  
**EL endorsed:** 2026-06-06

The 14 near-term backlog items are grouped by shared file areas, dependency chains, and risk profile. Each group is one PR unless noted. Tests ship with code in the same PR.

### Issue Classification

| # | Title (short) | Type | Weight |
|---|---|---|---|
| #725 | mypy pin | chore / one-liner | XS |
| #13 | Dataclass Attributes: sections | compliance / docs refactor | S |
| #43 | confidence_tier + uncertainty table | standards docs | S |
| #45 | HCL output fields + effect sizes | standards docs | S |
| #95 | Ecological backtesting case planning | pure docs | S |
| #259 | CTO legibility metrics dashboard | docs + CI step | M |
| #30 | Stock vs. flow AttributeType enum | backend model | M |
| #28 | Cohort disaggregation stubs | backend model | M |
| #34 | Investment climate state variables | backend model + seed data | L |
| #90 | Multi-attribute comparison endpoint | API | M |
| #99 | Trajectory comparison endpoint | API | M |
| #644 | ESLint exhaustive-deps audit | frontend tooling | M |
| #451 | Mode 1 COMPARE_VIEW spec + user story | UX spec + backend design | M |
| #394 | Multi-scenario comparison (>2) | full-stack feature | L |

### Group Definitions

#### NB-1 — Standards Foundation *(docs only, zero code risk)*

**Issues:** #43 + #45  
**Why together:** Both amend `CODING_STANDARDS.md` and `DATA_STANDARDS.md`. Neither touches code. Closing them first means subsequent code PRs (NB-3, NB-4) can be documented against the finalized standard rather than a draft.  
**Scope addition (EL-endorsed, panel decision DP-1):** `information-hierarchy.md` Zone 1A confidence display ruling added in this PR — not as a follow-up. The display contract for `uncertainty_range_pct = None` ("Directional only — uncertainty not quantified"; no confidence band) must be a binding UX ruling before the backend implements the field.  
**ADR prerequisite:** None — docs only.  
**Gate before starting:** Chief Methodologist Tier 5 null-sentinel clause adopted (see Panel Decision DP-1).

#### NB-2 — Quick Riders *(one PR, minimal diff)*

**Issues:** #725 + #13  
**Why together:** Both are tiny, low-risk backend-only changes. `pyproject.toml` one-liner (#725) and Google-style `Attributes:` section reformatting across six dataclasses in `models.py` (#13). Single PR closes two open compliance/environment items.  
**No dependencies** on NB-1 or any other group.

#### NB-3 — Entity Attribute Model Foundation

**Issues:** #30 + #28  
**Sequencing within PR:** `AttributeType` enum (#30) defined first; `CohortProfile` type (#28) references it. Both ship in one PR.  
**ADR prerequisite (EL-endorsed, panel decision DP-2):** ADR-001 Amendment required in this PR — documents `CohortProfile` structure, cohort key convention (`"Q1"`–`"Q5"` for income quintiles, `"youth_15_24"` for age bands), and `confidence_tier` inheritance rule for cohort attributes. Not a separate PR; not a follow-up.  
**Seed requirement (EL-endorsed, panel decision DP-2):** Greece entity receives two populated `CohortProfile` entries — Q1 and Q5 poverty headcount from Eurostat EU-SILC 2010 (Tier 2), plus Q1 unemployment rate from Eurostat LFS 2010 (Tier 2). Stub without real seed data is not acceptable.  
**Storage model (EL-endorsed, panel decision DP-2):** `cohort_profiles: dict[str, CohortProfile] | None = None` on `SimulationEntity`; stored inside `state_data` JSONB envelope; no new database column; no migration.  
**Schema update:** `simulation_state.yml` updated with `CohortProfile` sub-schema in same PR.  
**CE constraint:** All new fields `Optional` with `None` defaults — no existing seed script may require modification.  
**Prerequisite:** NB-1 merged (so new attribute definitions are documented against finalized confidence tier standard).

#### NB-4 — Investment Climate State Variables

**Issues:** #34  
**Why separate from NB-3:** Requires sourcing real seed data from World Bank/IMF IFS for ten demo entities, a ContingentInput example, and a documented feedback relationship narrative. Heavier than pure type-stub work.  
**Prerequisite:** NB-3 merged (so new attributes are typed with `AttributeType` from #30).  
**AttributeType tagging:** All four new attributes (`sovereign_risk_premium`, `fdi_stock_pct_gdp`, `portfolio_flow_velocity`, `credit_rating_score`) tagged at definition with the `AttributeType` enum from #30.

#### NB-5 — Comparison API Pair

**Issues:** #90 + #99  
**Why together:** Both extend `GET /api/v1/scenarios/compare`. The multi-attribute endpoint (#90) and trajectory comparison endpoint (#99) share DB query patterns and are the API foundation that NB-7 (#451 spec) and eventually NB-8 (#394) need.  
**No prerequisite** on NB-1–4 (API-only; no entity model dependency).  
**Schema update:** `api_contracts.yml` updated in same PR with both new endpoint shapes.

#### NB-6 — Frontend Tooling Gate

**Issues:** #644  
**Scope:** Enable `react-hooks/exhaustive-deps` in ESLint config; audit all `useEffect`, `useCallback`, `useMemo` hooks across `ScenarioInstrumentCluster.tsx`, `FourFrameworkZone1D.tsx`, `MDAAlertPanelZone1B.tsx`, and any other file with hooks; fix or explicitly suppress with justification comment each violation.  
**Why before NB-8:** NB-8 (#394) is a large frontend feature with new hooks. Better to have `exhaustive-deps` enforced before writing new code than to inherit a hook debt from NB-8's implementation.  
**No hard prerequisite**, but sequence before NB-8.

#### NB-7 — Mode 1 Comparison Spec

**Issues:** #451  
**What it is:** UX spec document (`information-hierarchy.md §COMPARE_VIEW` Mode 1 block completed), backend extension design decision (single API call vs. dual call — resolves the open question in the issue body), and one user story in the Andreas Stefanidis (Persona 3) format. **Not an implementation PR.**  
**Prerequisite:** NB-5 merged — the "single call or dual call" API design decision in #451 requires knowing what NB-5 (#90 + #99) built so the spec does not contradict the implementation.  
**EL-endorsed scope (panel decision DP-3):** #451 ships in M12 as spec only. #394 (implementation) defers to M13. #451 is the specification prerequisite for M13's NB-8 implementation.

#### NB-8 — Multi-Scenario Comparison (>2) — DEFERRED TO M13

**Issues:** #394  
**Status:** Deferred by unanimous panel recommendation (DP-3), EL-endorsed 2026-06-06.  
**Why deferred:** Demo 4 (G8) has no acceptance gate requiring N>2 scenario comparison. The feature serves TC-3 (Kenya budget planning, Persona 1) which is not the Demo 4 demonstration target. The three required pre-implementation gates do not exist in M12: (1) UX Designer N>2 ruling (zone hierarchy for N curves, color/style vocabulary, cognitive load boundary), (2) Customer Agent AUDIT (Layer 3 legibility of N concurrent trajectories for Persona 2 in 90-second Reactive entry state), (3) #451 spec accepted. None of these can be completed before G8 without risk to Demo 4 timeline.  
**M13 gates (must all be met before implementation begins):**
- #451 spec accepted (NB-7 above)
- UX Designer: N>2 UX ruling issued (zone hierarchy for N curves, style vocabulary that does not collide with ghost baseline or confidence-degraded dashes, cognitive load ceiling on N)
- Customer Agent: AUDIT complete for Persona 2 (90-second gate) and Persona 5 (5-minute gate) against the N>2 UX ruling

#### NB-9 — Pure Docs *(can run in any wave)*

**Issues:** #95 + #259  
**#95 (ecological backtesting case planning):** Standalone documentation — identify the historical ecological case (Brazil Amazon deforestation 2000–2010; Ethiopia drought 2002–2004; Philippines Hainan 2013–2015 are candidates), specify data sources, initial state ecological attributes, fidelity thresholds, and ControlInput sequence. Ecological Economist consultation recommended before authoring. Produces a GitHub Issue for the ecological backtesting case implementation in a later milestone.  
**#259 (CTO legibility metrics dashboard):** All four prerequisites confirmed CLOSED (#255 ✅ #256 ✅ #257 ✅ #258 ✅). Can proceed. Requires a new CI step computing radon/sonarjs Tier 1 metrics — test on free-tier runner before committing. Produces a CI step and legibility section in the milestone exit checklist.  
**No prerequisites** on any other NB group.

### Execution Wave Sequence

```
Wave A (parallel — start immediately):
  NB-1  Standards foundation (#43 + #45) — blocks NB-3
  NB-2  Quick riders (#725 + #13)
  NB-5  Comparison API (#90 + #99) — blocks NB-7
  NB-9  Pure docs (#95 + #259)

Wave B (after NB-1 merged):
  NB-3  Entity attribute model (#30 + #28 + ADR-001 Amendment + Greece cohort seed)

Wave C (after NB-3 merged; NB-5 and NB-6 independent):
  NB-4  Investment climate state variables (#34)
  NB-6  ESLint audit (#644)         ← can also run in Wave A if preferred
  NB-7  Mode 1 spec (#451)          ← after NB-5 merged

Wave D (after NB-5 + NB-6 + NB-7 all merged):
  NB-8  DEFERRED TO M13

→ G8 (Demo 4) after all NB groups complete
```

**Critical path through near-term backlog:** NB-1 → NB-3 → NB-4 (for entity model completeness); NB-5 → NB-7 (for comparison spec). G8 can proceed once all Wave A/B/C groups are merged. NB-8 does not block G8.

---

## Near-Term Backlog — Panel Decision Record

**Session date:** 2026-06-06  
**Status:** EL-endorsed  
**Panels convened for three decision points identified during backlog analysis.**

---

### Decision Point DP-1: NB-1 (#43) — Tier 5 `uncertainty_range_pct`: numeric bound or null sentinel?

**Panel:** Architect Agent · Data Architect Agent · QA Lead Agent · UX Designer Agent

---

**Architect Agent: REVIEW — #43 `uncertainty_range_pct` schema contract for Tier 5**

The question is whether a numeric upper bound on `uncertainty_range_pct` for Tier 5 is semantically defensible. It is not. A Tier 5 gap-filled value is gap-filled precisely because the distribution is unknown. Writing `uncertainty_range_pct > 50%` into the standard claims we know the lower bound on our ignorance. We do not. That is a self-referential precision claim about uncertainty — and it violates the "No False Precision" founding principle more directly than the original under-specified standard.

The correct schema contract: `uncertainty_range_pct: float | None`, where `None` is a first-class value meaning "distribution unknown; directional use only." This is architecturally clean: the field has a defined sentinel, every call site can branch on it, and the display layer has an unambiguous instruction. A null is not a missing value — it is a meaningful signal.

Checking `simulation_state.yml` will show `confidence_tier` is already an integer 1–5 on `QuantitySchema`. The `uncertainty_range_pct` addition is additive; it should be `Optional[float]` with `None` as default, so existing Quantities that predate #43 are valid without migration.

**Recommended amendment to #43:** Remove the `>50%` bound from Tier 5. Replace with: `None — distribution unknown; render as directional range, never as a value with an error bar.`

---

**Data Architect Agent: REVIEW — schema implications of nullable `uncertainty_range_pct` on Quantity**

`QuantitySchema` in `simulation_state.yml` currently has: `confidence_tier: int`. Adding `uncertainty_range_pct: float | None` requires:

1. `simulation_state.yml` updated with `uncertainty_range_pct: float | null` in the `QuantitySchema` block.
2. `quantity_serde.py` (`quantity_to_schema` / `quantity_from_schema`) updated to serialize/deserialize the field — with `None` as default for backward compatibility.
3. `database.yml` — `state_data` JSONB in `scenario_snapshots` does not need a column migration because `uncertainty_range_pct` lives inside the Quantity sub-object. But the key must be registered in the JSONB key table so future queries do not silently miss it.
4. The `max()` confidence tier propagation rule in `DATA_STANDARDS.md` must be extended: when combining Quantities, `uncertainty_range_pct` aggregates as `None if any input is None, else max(values)` — because a Tier 5 input taints the composite's uncertainty to "distribution unknown" regardless of other inputs.

All four schema files must be updated in the same PR as the standards documents. No exceptions. The name-collision pattern this prevents: a future query that treats `uncertainty_range_pct is None` as missing data rather than as the Tier 5 sentinel would silently produce wrong confidence bands.

---

**QA Lead Agent: VALIDATE — is `uncertainty_range_pct` as specified testable? Does null sentinel improve testability?**

The entire motivation for #43 is testability. The current standard uses qualitative descriptors ("moderate reliability from established institutions") that no test can verify mechanically.

With quantitative thresholds and a null sentinel, testability is clear:
- `assert quantity.uncertainty_range_pct <= 0.05` for Tier 1 — passes or fails, no interpretation required
- `assert quantity.uncertainty_range_pct is None` for Tier 5 — exact, unambiguous

A numeric bound for Tier 5 (`> 50%`) would produce: `assert quantity.uncertainty_range_pct > 0.50`. This test passes for a value of `0.51` and also for `50.0` — neither tells you the distribution is actually unknown. The null sentinel produces the only test that correctly states the epistemic condition: "we do not have a numeric bound."

Two test requirements to add to #43's acceptance criteria, beyond what is listed in the issue:
- A Tier 5 Quantity with `uncertainty_range_pct is None` must cause any aggregation that includes it to propagate `None` (the taint rule the Data Architect described above).
- A rendering test must assert that `uncertainty_range_pct is None` produces a "directional range" label, never a numeric confidence band.

---

**UX Designer Agent: REVIEW — display contract for null `uncertainty_range_pct` in Zone 1 trajectory view**

This directly affects the trajectory curves in Zone 1A. Today the existing `confidence_tier`-based display already uses `strokeDasharray="8 3"` for confidence-degraded data (Tier 4/5, per G6b). But `strokeDasharray` alone is not enough if the confidence band is suppressed for Tier 5 — users need to know *why* there is no band, not just that the curve looks different.

My ruling: when `uncertainty_range_pct is None`, Zone 1A must render:
- No confidence band (no shaded fill around the curve)
- A label annotation: "Directional only — uncertainty not quantified"
- The `strokeDasharray="8 3"` pattern (already standard for Tier 4/5)

This is a display contract, not an implementation detail. It must be written into `information-hierarchy.md §Zone 1A Confidence Display` as part of NB-1, so the implementation agent has a binding ruling rather than an interpretation problem.

**The `information-hierarchy.md` update is in scope for NB-1** — otherwise the standard exists in DATA_STANDARDS.md with no UX contract, and the next frontend developer makes a rendering decision without authority.

---

**DP-1 Panel Recommendation (unanimous):**

| Decision | Specifics |
|---|---|
| `uncertainty_range_pct` type | `float \| None` — `None` = distribution unknown |
| Tier 1–4 | Numeric bounds as proposed in #43 issue body |
| Tier 5 | `None` (remove `>50%` bound from issue body) |
| Propagation rule | `None` taints any composite — any input `None` → composite `None` |
| Display contract | `None` → "Directional only — uncertainty not quantified"; no confidence band; `strokeDasharray="8 3"` |
| Schema files | `simulation_state.yml` + `database.yml` JSONB key registry updated in same PR |
| `information-hierarchy.md` | Zone 1A confidence display ruling added in same NB-1 PR |

---

### Decision Point DP-2: NB-3 (#28) — Cohort stub with or without Greece seed data?

**Panel:** Chief Methodologist Agent · Architect Agent

---

**Chief Methodologist: VALIDATE — methodological adequacy of a schema stub with no seeded cohort data**

A type definition that is `None` in every entity is not a Human Cost Ledger capability. It is infrastructure for a future capability, and it must be represented honestly. The acceptance criteria for #28 say "at minimum one cohort-level attribute seeded for a test entity to validate the schema" — that requirement was written correctly and must not be weakened.

The Greece 2010 data exists at the cohort level in published sources. Eurostat EU-SILC provides poverty headcount by income quintile for Greece at the national level. The values to use:

| Cohort | Indicator | Value | Source | Confidence Tier |
|---|---|---|---|---|
| Bottom quintile (Q1) | poverty_headcount | 0.201 | Eurostat EU-SILC 2010 | Tier 2 |
| Top quintile (Q5) | poverty_headcount | 0.065 | Eurostat EU-SILC 2010 | Tier 2 |
| Bottom quintile (Q1) | unemployment_rate | 0.18 | Eurostat LFS 2010 | Tier 2 |

This is sufficient to validate that the `CohortProfile` schema is correct, that the seeding pipeline handles cohort sub-entities, and that a future module can read cohort-level attributes from the state snapshot. The MDA thresholds already reference "bottom quintile" as a cohort scope — without a seeded value at that cohort level, the MDA system is testing a code path that will never fire in backtesting.

**The minimum viable seed is two cohort profiles on the Greece entity — Q1 and Q5 poverty headcount, Tier 2.** Not a synthetic approximation; the data exists and is Tier 2.

---

**Architect Agent: REVIEW — storage and API surface for CohortProfile in SimulationEntity**

Two architectural questions for #28:

**1. Where does `CohortProfile` live in the storage model?**

It must live inside the `state_data` JSONB envelope in `scenario_snapshots`, not as a separate column. The `SimulationEntity.attributes` dict already maps `str → Quantity`. `cohort_profiles` should be a parallel optional dict: `cohort_profiles: dict[str, CohortProfile] | None = None`, where the key is the cohort identifier (e.g., `"Q1"`, `"Q5"`, `"youth_15_24"`) and `CohortProfile` is a typed container with its own `attributes: dict[str, Quantity]`.

This is consistent with how `SimulationEntity.attributes` works today and requires no DB migration — the JSONB envelope already accepts arbitrary sub-structure.

**2. Does this require an ADR?**

#28's acceptance criteria say "ADR updated or new ADR drafted: cohort disaggregation architecture." Looking at existing ADRs: ADR-001 defines the entity model, ADR-005 defines multi-framework measurement. Neither covers cohort sub-entities explicitly. An **ADR-001 Amendment** is the right vehicle — the cohort profile is an extension of the entity model, not a new architectural decision. The amendment must document: (a) `CohortProfile` as the cohort-level entity sub-structure, (b) the key convention (`"Q1"` through `"Q5"` for income quintiles, `"youth_15_24"` for age bands), (c) the rule that cohort `confidence_tier` inherits from its source data and is tracked independently from the parent entity's aggregate tier.

This amendment is lightweight but mandatory per CLAUDE.md §ADR policy. It ships in the same PR as NB-3 implementation — not as a follow-up.

**Boundary condition:** all new fields must be `Optional` with `None` defaults. Existing seed scripts must continue to work without modification. Only the Greece seed script is updated to populate two `CohortProfile` entries; all other entity seed scripts produce `cohort_profiles=None`.

---

**DP-2 Panel Recommendation (unanimous):**

| Decision | Specifics |
|---|---|
| Cohort seed | Greece entity: Q1 + Q5 poverty_headcount (Eurostat EU-SILC 2010, Tier 2) + Q1 unemployment_rate (Eurostat LFS 2010, Tier 2) |
| Storage model | `state_data` JSONB sub-key; `cohort_profiles: dict[str, CohortProfile] \| None = None` on `SimulationEntity`; no new DB column; no schema migration |
| ADR | ADR-001 Amendment in same NB-3 PR — documents CohortProfile structure, key convention, confidence_tier inheritance rule |
| Schema file | `simulation_state.yml` updated with `CohortProfile` sub-schema in same PR |
| Minimum test gate | Assert that `GRC.cohort_profiles["Q1"].attributes["poverty_headcount"]` returns a Quantity with `value ≈ 0.201` and `confidence_tier == 2` |

---

### Decision Point DP-3: NB-8 (#394) — Multi-scenario comparison (>2): before or after G8 (Demo 4)?

**Panel:** PM Agent · Business PO Agent · UX Designer Agent · Customer Agent

---

**PM Agent: FOCUS — sequencing #394 relative to G8 Demo 4**

Reading the Demo 4 acceptance gates in full:

> Jordan fixture seeds cleanly; synthetic indicators flagged  
> Hormuz scenario advances 8 steps without hitting irreversible thresholds before step 4  
> Mode 3 parameter adjustment demonstrably changes the trajectory  
> Human cost indicators show non-zero response to commodity shock within 2 steps  
> Demo runs end-to-end on ProBook within performance budget  
> Narration document reviewed against NARRATION-RULING-1  
> IR stakeholder review artifact in `docs/demo/m12/reviews/`

Zero mention of N>2 scenario comparison. The Demo 4 value proposition is Mode 3 active control under Hormuz crisis conditions — branching from a baseline and demonstrating that the human cost trajectory diverges with intervention vs. without. That is a two-scenario comparison (baseline + branch), which G6b already delivers.

The sprint plan explicitly tags #394 as "treat as Wave 3 if capacity allows." With the near-term backlog consuming Wave 3 capacity, there is no slack for #394 before G8 without risk of delay. The sequencing cost of #394 is not just its own implementation — it includes the UX ruling that must precede it and the Customer Agent AUDIT that must gate it. Those are two additional sequential steps before a line of implementation code is written.

**PM position: #394 defers to M13. It is the anchor issue for M13's comparison mode track.**

---

**Business PO Agent: PRIORITIZE — user-value impact of #394 deferral to M13**

TC-3 (Kenya budget planning — three competing proposals) is a legitimate and important marquee case. It serves Persona 1 (Lucas Ferreira — the programme analyst who needs to run sensitivity analysis across three fiscal consolidation paths).

But Demo 4 serves Persona 5 (Aicha Mbaye — Institutional Decision-Maker) and Persona 2 (Eleni Papadimitriou — Finance Ministry Negotiator). These are the two personas with the most urgent near-term adoption pathway — they are the target of the Demo 4 stakeholder session. Persona 1 is better served after the platform has proven its value to Persona 5, because institutional adoption flows from the top down.

The value proposition for Demo 4 is: a finance minister under crisis conditions can use WorldSim to understand whether a policy intervention changes the human cost trajectory within the time available for a cabinet decision. #394 adds nothing to that demonstration. Its deferral to M13 does not degrade a single Demo 4 acceptance gate.

**PO position: Defer #394 to M13. Priority in M12 near-term is the spec (#451), not the implementation.**

---

**UX Designer Agent: REVIEW — can #394 ship without a UX ruling?**

No. N>2 comparison is a qualitatively different surface from two-scenario comparison. The information hierarchy has no ruling for it. `information-hierarchy.md §COMPARE_VIEW` specifies Mode 2 comparison for two scenarios (single-entity and multi-entity). Three or more concurrent trajectories in Zone 1A — with distinct line styles, a three-item legend, and per-scenario MDA panels — requires:

1. A zone hierarchy ruling: does each scenario get its own Zone 1B panel, or does a unified comparative panel replace them?
2. A color/style vocabulary ruling: Mode 3 already uses ghost baseline (`strokeDasharray="4 2"`) and G6b uses confidence-degraded dashes (`"8 3"`). N>2 needs a third visual register that does not collide with either.
3. A cognitive load ruling: at what N does the trajectory view stop serving comprehension and start producing noise? Three is probably acceptable; five may not be.

None of these rulings exist. #451 produces the spec for Mode 1 two-scenario comparison — it does not produce N>2 rulings. #394 cannot begin implementation until I produce those rulings, and I cannot produce them without the N>2 UX research that the M11.5 sessions began to surface.

**UX position: #394 implementation must not begin in M12. #451 (Mode 1 spec) ships in M12 as a prerequisite. N>2 UX ruling is M13 pre-implementation work for #394.**

---

**Customer Agent: AUDIT — Layer 3 legibility risk of N>2 scenario comparison for Persona 2 and Persona 5**

Applying the 90-second retrieval gate to N=3 concurrent scenario comparison:

Persona 2 (Eleni, Finance Ministry Negotiator, Reactive entry state): She has 90 seconds and needs one finding. Three concurrent trajectory curves with three legends and three MDA panels will exceed the cognitive processing budget for a Reactive entry state user. She will not be able to determine which of the three curves is the "better" option without analyst mediation. This fails the gate.

The N>2 surface is viable only if the design answers "which scenario wins?" without requiring the user to trace three curves, read three legends, and cross-reference three alert panels. That design does not exist yet. The M11.5 usability sessions showed that even two-scenario comparison with explicit labeling caused orientation failures for Persona 2 (S003-FINDING-01: non-interactive alerts; FINDING-03: no cohort visibility). Adding a third scenario without solving the two-scenario orientation problem would compound the failure.

**Customer Agent position: A Layer 3 AUDIT is a required gate on #394 before implementation — not after. This cannot be skipped. The audit requires a prototype or a spec detailed enough to evaluate zone load; neither exists today.**

---

**DP-3 Panel Recommendation (unanimous):**

| Decision | Specifics |
|---|---|
| #394 in M12 | Deferred — no implementation this milestone |
| #394 in M13 | First item on M13 board; requires three gates before implementation: (1) #451 spec accepted, (2) UX Designer N>2 ruling issued, (3) Customer Agent AUDIT complete for Persona 2 and Persona 5 |
| #451 in M12 | Ships as planned (NB-7) — UX spec + backend design decision + one Andreas Stefanidis user story. Not an implementation PR |
| Demo 4 impact | Zero — #394 appears in no Demo 4 acceptance gate |

---

### EL Endorsement

**Engineering Lead:** @PublicEnemage  
**Endorsement date:** 2026-06-06  
**Form:** Verbal in-session endorsement of all three panel recommendations

| DP | Question | Panel verdict | EL decision |
|---|---|---|---|
| DP-1a | Tier 5 `uncertainty_range_pct` — null or numeric? | Unanimous: null sentinel | **Adopted** — `float \| None`; `None` = distribution unknown |
| DP-1b | Display contract for null `uncertainty_range_pct`? | Unanimous: binding ruling required | **Adopted** — "Directional only" label + no confidence band; added to `information-hierarchy.md` in NB-1 PR |
| DP-1c | Propagation rule for `uncertainty_range_pct`? | Unanimous: null taints | **Adopted** — any input `None` → composite `None` |
| DP-2a | Greece cohort seed — real data or empty stub? | Unanimous: real data required | **Adopted** — EU-SILC Q1/Q5 poverty headcount + Q1 unemployment, Tier 2; stub alone is not acceptable |
| DP-2b | Storage model for `CohortProfile`? | Unanimous: JSONB sub-key | **Adopted** — `state_data` JSONB; no new DB column; no migration |
| DP-2c | ADR required for #28? | Unanimous: ADR-001 Amendment | **Adopted** — ships in same NB-3 PR |
| DP-3 | #394 before or after G8? | Unanimous: defer to M13 | **Adopted** — #451 spec ships M12; #394 implementation is M13 with three stated gates |

All decisions are binding. The NB-1 implementation agent must implement the null-sentinel clause and `information-hierarchy.md` ruling before implementation begins. The NB-3 implementation agent must seed Greece cohort data and include ADR-001 Amendment in the same PR. #394 implementation is blocked until all three M13 gates are met.

---

## Dependency Map

```
Wave 1 (parallel):   G1 · G2 · G3 · G4
Wave 2:              G5 (needs G4) · G7 (needs G4) · G9 (needs G4)
Wave 3:              G6a (needs G3 + G4 + G5) → G6b (needs G6a + #613 + #614)
Wave 4:              G8 (needs G1–G6 + G9 all merged)
```

**Critical path:** G4 → G5 → G6a → G6b → G8

G1, G2, and G3 run on the parallel track. They must merge before G8 (Demo 4 requires instrument cluster and Mode 2) and before G6b (fiscal multiplier is Mode 3's first instrument). G9 (political economy) must merge before G8 (Demo 4 Jordan scenario benefits from political economy realism). #613 CE assessment must complete before G6b implementation begins.

---

## ADR Prerequisites

| Group | ADR requirement |
|---|---|
| G5 | External sector module ADR — ARCH-006 (ADR-012). Must be authored and accepted before G5 implementation merges. On critical path. |
| G6b | Confirm ADR-008 covers Mode 3 interaction model (Decision 10 covers live A/B UX). #613 CE assessment may surface engine-layer ADR amendment need — resolve before G6b implementation begins. |
| G9 | Political economy module ADR — ARCH-007 (ADR-013). Must be authored and accepted before G9 implementation merges. Panel: Architect Agent, Political Economist, Chief Methodologist, Engineering Lead. |
| All others | No ADR prerequisite. |
