---
name: m12-sprint-plan
type: sprint-plan
milestone: M12 — Active Control and External Sector
status: Active
authored-by: PM Agent
authored-date: 2026-06-05
el-approved: 2026-06-05
consulted:
  - Business Product Owner (value prioritization)
  - Frontend Architect (file area grouping)
  - Chief Engineer (dependency sequencing)
  - Architect (ADR prerequisites)
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
