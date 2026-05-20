# WorldSim Changelog

Each entry corresponds to a completed milestone. Entries follow the milestone
closure ceremony defined in `docs/MILESTONE_RUNBOOK.md`.

---

## v0.8.0 — Milestone 8: Ecological and Governance Frameworks (2026-05-19)

### Summary

Three live radar axes for the first time. Honest-null governance axis. Greece 2010–2015
six-step scenario as the primary backtesting and demo fixture. Case B UX architecture
verdict — rethink warranted before M9 implementation. Synthetic data framework
consultation complete. CLAUDE.md structural refactor with satellite simulation-framework.md.

### Delivered

**EcologicalModule expansion (Issues #312, #313, #314 — PR #324)**
- `_compute_composite_score()` three-branch strategy dispatch: ecological →
  `_boundary_proximity_strategy` (boundary-normalized, absolute); financial/human_development
  → validated percentile rank; unregistered → `[SIM-INTEGRITY]` WARNING + percentile rank fallback
- Planetary boundary proximity indicators: `planetary_boundary_co2_proximity` (min(ppm/350, 2.0)),
  `planetary_boundary_land_use_proximity` (min(index, 2.0) — no double-normalization per Decision M8-6)
- `_SINGLE_ENTITY_GUARD_EXEMPT_FRAMEWORKS = frozenset({"ecological"})` — ecological exempt
  because boundary proximity is physically meaningful for a single entity (Decision M8-2)
- STOCK delta path contract: emit `current + elasticity_delta` (absolute level), not raw delta —
  propagation engine replaces STOCK attributes; raw delta would corrupt all subsequent proximity
  computations (PR #328 fix)
- `simulation_reference_constants` table seeded: CO2 boundary 350 ppm (Rockström 2009),
  land-use boundary 0.25 (Richardson 2023); temporal guards enforce effective_from dates
- Migrations: `c1a4e7f2d9b3` (confidence_tier), `d2b5f8a3e6c4` (ecological MDA thresholds),
  `b3c5d7e9f1a2` (reference constants seed)

**ADR-005 Amendment 3 (Issue #218 — PR #309)**
- Ecological Framework Completion: eight M8 decisions (M8-1 through M8-8)
- Governs composite strategy dispatch, single-entity exemption, null axis rendering,
  STOCK delta path contract, land-use double-normalization prevention

**Greece fixture extension (Issues #284, #316 — PR #321)**
- Steps 4–6 (2013–2015) actuals: capital controls, privatization, DIRECTION_ONLY thresholds
- `ECOLOGICAL_COMPOSITE_DISCLOSURE` — honest disclosure of CO2-only composite for Greece
  (land-use boundary constant effective 2023-09-13, post-dates scenario period)
- CO2 seed: `co2_concentration_ppm = 388.0 ppm` (NOAA MLO 2010) in `initial_attributes`
- `gdp_direction_step5_positive` moved to `deferred_thresholds` — mean-reversion channel
  absent from MacroeconomicModule; deferred Issue #221 (M10)

**Null governance axis (Issue #315 — PR #323)**
- `RadarAxisDatum.composite_score: number | null` live on main
- `GOVERNANCE_IN_VALIDATION_LABEL = "Governance — in validation"` (em dash — ADR-required constant)
- `GOVERNANCE_IN_VALIDATION_TOOLTIP` — promotion criteria: 0 of 5 met at M8, target M9
- `computeFinalScore(null, weight) → null` — honest null propagates to Recharts polygon gap
- Null axis: dashed hollow SVG circle (`strokeDasharray="2 2"`, `fill="none"`); polygon vertex absent
- Animation guard: `isAnimationActive = false` when any axis is null (undefined interpolation prevention)
- DD-011 sentinel in `docs/frontend/design-decisions.md`
- 10 Vitest tests

**Frontend UX Areas 2–5 (Issues #317, #318, #319, #320 — PR #329)**
- `INDICATOR_DISPLAY_NAMES` registry — human-readable labels for all M8 indicators
- Zone 3A expandable ecological methodology note (`EcologicalNoteDrawer`)
- PMM Zone 1C placeholder widget (`PolicyManoeuvreMeter`) — null at M8, live at M9
- Radar 250ms CSS transition animation with `prefers-reduced-motion` guard

**Demo scenario assembly (Issue #269 — PR #328)**
- `build_greece_demo_scenario()` in `tests/fixtures/greece_2010_scenario.py`
- Six steps, EcologicalModule enabled, eight scheduled programme inputs
- 5 backtesting tests in `tests/backtesting/test_greece_m8_demo.py`
- CLI demo: `backend/scripts/demo_greece_2010_2015.py`

**Demo infrastructure (PRs #334, #338, #339, #340)**
- `docs/process/demo-preparation-standard.md` — nine-step biennial demo cadence
- `demo-narrated.spec.ts` — narrated Playwright spec, M8 rewrite; excluded from CI
  via `@demo` tag and `grep: /^(?!.*@demo)/`; uses `playwright.demo.config.ts` for
  `headless: false`, `slowMo: 800`, `--start-fullscreen` (screen-recording mode)
- `__worldsim_selectEntity` / `__worldsim_setAttributeName` window globals — DEV-only
  test seam in `App.tsx` (`import.meta.env.DEV` guard); bypasses WebGL canvas for
  reliable entity selection in headless Chromium
- Five screenshots captured: frames A–E per UX Agent brief (Issue #233)
- TTS voice: macOS "Zoe (Enhanced)" at 175 WPM
- Independent Review Agent: 9 findings (DEMO-001–009), 2 CRITICAL, 4 SIGNIFICANT, 3 MINOR;
  issues #342–#350 filed; Root Cause B (drawer density) explains DEMO-002/003/005/006

**UX Design Thinking work stream (PRs #354, #355, #356)**
- UX Design Thinking Agent activated — first activation, persona added to `agents.md`
- M8 critique: `docs/ux/design-thinking/m8-interaction-model-critique.md`
  — core diagnosis: WorldSim is a spatial comparison tool applied to a temporal problem
- Panel synthesis: three-agent panel (UX Designer, Development Economist, Chief Methodologist)
  — nine cross-cutting concerns; three EL decisions required
- First-principles derivation: `docs/ux/design-thinking/worldsim-ux-architecture-first-principles.md`
  — **Case B verdict**: current UI inverts instrument/context relationship;
  architecture rethink warranted before M9 implementation
- Five M9 governing premises codified; control plane zone reserved in layout

**CLAUDE.md structural refactor (Issue #359 — PR #372)**
- `docs/architecture/simulation-framework.md` extracted (mandatory reading for all agents)
- Platform Principle, Synthetic Data framework, UX Architectural Commitments added
- Role-based mandatory reading table (UX, Data/Backend, Architecture, Standards/Compliance)
- Three-mode architecture (Mode 1: Replay, Mode 2: Simulation, Mode 3: Active Control) formalised

**Synthetic data framework (Issue #361 — PR #373)**
- Chief Methodologist consultation: `docs/architecture/synthetic-data-consultation.md` (560 lines)
- Five-method hierarchy: Bayesian > MICE > Bootstrap > structural extrapolation > structural absence
- Three-condition meaninglessness threshold; MDA tier table (full/advisory/exploratory/none)
- Anomaly detection: requires TSC sign-off, opt-in, Mode 3 excluded, governance indicators excluded
- ADR-007 outline produced

**M8 exit compliance (PR #380)**
- SCAN-022: 0 violations across all M8 changes

### Deferred to M9

- GovernanceModule composite score — five promotion criteria not yet met (Decision M8-4);
  null axis and validation label are the M8 resolution
- PMM live computation — placeholder at M8; target M9
- Mean-reversion channel — Issue #221; `gdp_direction_step5_positive` in `deferred_thresholds`
- DEMO issues #342–#350 — re-milestoned to M9

### Compliance Posture

- SCAN-022 — Milestone 8 exit gate: **Clean** (0 violations)
- ADR license status at milestone close: ADR-001 CURRENT, ADR-002 CURRENT, ADR-005 CURRENT
  (Amendment 3 merged PR #309)
- GovernanceModule deferred per Decision M8-4: exception recorded with single-principal
  governance acknowledgement per CLAUDE.md §Governance
- Known limitation: `gdp_direction_step5_positive` at step 5 — model produces −0.434 vs
  historical +0.007; mean-reversion channel absent; deferred to M10 (Issue #221)

---

## v0.3.0 — Milestone 3: Scenario Engine (2026-04-24)

### Delivered

**Scenario Configuration (ADR-004 Decision 1)**
- Three new database tables via Alembic migration: `scenarios`
  (configuration JSONB, status, engine_version), `scenario_state_snapshots`
  (step-indexed state JSONB, `ia1_disclosure` NOT NULL enforced at DB level),
  `scenario_deleted_tombstones` (deleted scenario config + scheduled_inputs JSONB for
  reconstruction from first principles)
- Four API endpoints: `POST /scenarios`, `GET /scenarios/{id}`,
  `GET /scenarios/{id}/snapshots`, `DELETE /scenarios/{id}`
- `ScenarioConfig` Pydantic schema with full validation; `AdvanceResponse`
  and `SnapshotResponse` schemas with float prohibition enforced end-to-end

**Simulation Execution Layer (ADR-004 Decision 2)**
- `WebScenarioRunner` — async scenario executor wiring `SimulationStateRepository`
  (read/write `SimulationState` from DB) and `ScenarioSnapshotRepository`
  (write step snapshots with SA-09 envelope format)
- `SimulationStateRepository` builds `SimulationState` from PostGIS entities
  with GRC entity required for backtesting fixture
- `ScenarioSnapshotRepository` persists `state_data` as JSONB with
  `_envelope_version: "1"` and `value: str` (float prohibition)
- SA-11 determinism guarantee: same configuration + same scheduled inputs +
  same engine version → identical snapshot outputs

**Greece 2010–2012 Backtesting Fixture (ADR-004 Decision 3)**
- `tests/backtesting/test_greece_2010_2012.py` — four tests marked `backtesting`;
  enforced in CI as a build gate (a failure here is a build failure)
- `DIRECTION_ONLY` fidelity thresholds: gdp_growth negative at steps 1–3;
  unemployment rising step 1 → step 3
- `fidelity_report.py` — structured fidelity report printed to CI logs on
  every backtesting run
- `greece_2010_2012_actuals.py` — historical actuals fixture with IA-1
  and parameter calibration disclosures
- `natural_earth_loader.py` seed script runs in CI before backtesting suite
  to ensure GRC entity exists
- Session-scoped asyncpg pool lifecycle fix: `loop_scope="session"` on
  lifecycle fixture, client fixture, and `pytestmark` — prevents
  "Future attached to a different loop" errors (commits `6c35cab`, `89e2caa`)

**Time Acceleration Controls (ADR-004 Decision 4)**
- `POST /scenarios/{id}/advance` — advances scenario by configurable steps;
  returns `AdvanceResponse` with `steps_completed`, `final_status`, and
  `snapshots` array
- Step-aware choropleth: `GET /choropleth/{attribute}` accepts optional
  `scenario_id` and `step` query parameters; geometry from
  `simulation_entities` (stable), attribute values from
  `scenario_state_snapshots` (step-specific); 422 if only one of the pair
  provided

**Comparative Scenario Output (ADR-004 Decision 5)**
- `GET /scenarios/compare` — returns `CompareResponse` with per-entity,
  per-attribute `DeltaRecord` (value_a, value_b, delta, direction,
  confidence_tier); registered before `/{scenario_id}` to avoid FastAPI path
  collision
- `GET /choropleth/{attribute}/delta` — delta choropleth endpoint joining
  geometry with Decimal delta computation; returns `GeoJSONFeatureCollection`
  with `delta_direction` and both base values
- `DeltaChoropleth.tsx` — diverging colour scale (crimson → white → navy);
  percentile-based step computation for negative and positive halves
  separately; legend overlay; hover popup with delta direction icon
- `DeltaRecord` and `CompareResponse` Pydantic schemas; 12 unit tests and
  10 integration tests

**Scenario Tombstones (ADR-004 Decision 1)**
- `DELETE /scenarios/{id}` writes a tombstone capturing name, configuration
  JSONB, scheduled_inputs JSONB, engine_version, and original_created_at
  before deleting the scenario; enables reconstruction from first principles
  under the SA-11 determinism guarantee
- Snapshots are derived data and are not tombstoned — they are reproducible
  from the tombstone given the same engine version

**CI and Governance**
- `ci-failure-notify.yml` — GitHub Actions workflow notifying on CI failures
- `admin-bypass-audit.yml` — GitHub Actions workflow auditing branch
  protection bypasses
- ADR-004 Known Limitation (engine_version gap): `engine_version` is a
  semantic version string declaration, not a verifiable pointer; no
  block-on-mismatch control exists at M3; conservative posture is to block
  unconditionally on mismatch; tracked in Issue #139 for M4 resolution

### Deferred

- **Issues #69** — `ia1_disclosure` compliance exception: time-horizon
  confidence degradation not yet applied to projected attributes; compliance
  exception documented; moved to Milestone 4
- **Issues #86, #87, #91, #92** — human cost indicators and time-horizon
  degradation; moved to Milestone 4
- **Issues #22, #23, #24, #26** — uncertainty quantification, distribution
  selection, correlation structure modelling, and related standards work;
  moved to Milestone 4
- Standards documentation cluster (SA-02 through SA-17 subset, Issues #42
  #43 #46 #47 #49) — moved to Milestone 4 with scope update incorporating
  Whatsonyourmind external contributor corrections to Issue #49

### Compliance Posture

- SCAN-009 — Scenario configuration: **Clean** (0 violations)
- SCAN-010 — SimulationStateRepository and snapshot layer: **Clean**
  (0 violations)
- SCAN-011 — WebScenarioRunner execution layer: **Clean** (0 violations)
- SCAN-012 — Greece backtesting fixture: **Clean** (0 violations)
- SCAN-013 — Comparative scenario output: **Clean** (0 violations)
- SCAN-014 — Milestone 3 exit gate: **Clean** (59 files, 0 violations,
  2 pre-accepted warnings — ARCH-4 `Relationship.attributes: dict[str, Any]`
  and `Relationship.weight: float` propagation coefficient)
- Open compliance exception: **Issue #69** — `ia1_disclosure` time-horizon
  degradation; exception documented with single-principal governance
  acknowledgement per CLAUDE.md §Governance
- Open architectural gap: **Issue #139** — `engine_version` is a declaration,
  not a verifiable pointer; documented as Known Limitation in ADR-004
- ADR license status at milestone close: ADR-001 CURRENT, ADR-002 CURRENT,
  ADR-003 CURRENT, ADR-004 CURRENT (all renewed to Milestone 4)

---

## v0.2.0 — Milestone 2: Geospatial Foundation (2026-04-21)

### Delivered

**PostGIS Database Schema (ADR-003 Decision 1)**
- Five-table PostGIS schema via Alembic migration `126eb2fd0afd`:
  `simulation_entities` (MULTIPOLYGON SRID 4326, JSONB attributes, GiST + GIN
  indexes), `relationships`, `territorial_designations`, `source_registry`,
  `control_input_audit_log`
- `TerritorialValidator` hard gate — enforces all five `POLICY.md` territorial
  positions (TWN, PSE, XKX, ESH, CRIMEA) before any INSERT; 30/30 unit tests
- Natural Earth 110m boundary loader — 177 country entities loaded with 10
  Level 1 attributes (population_total, gdp_usd_millions, pop_rank,
  economy_tier, income_group, continent_code, un_region_code, subregion_code,
  map_color_group, ne_scale_rank); cache-first GeoJSON fetch

**FastAPI Layer (ADR-003 Decision 2)**
- Six endpoints: `GET /health`, `GET /countries/geojson/{attribute}`,
  `GET /countries/{entity_id}`, `GET /countries`, `GET /attributes/available`,
  `POST /countries/seed`
- asyncpg direct queries for runtime (no ORM overhead); SQLAlchemy retained
  for Alembic migrations only
- Float prohibition enforced at API boundary: `QuantitySchema.value` is `str`;
  `from_jsonb()` converts via `str(Decimal(str(v)))`
- 251 unit tests passing; 16 integration tests skip gracefully without DB
- `backend/Dockerfile` and `.env.example` added

**MapLibre GL Choropleth Frontend (ADR-003 Decision 3)**
- Vite + React + TypeScript frontend at `http://localhost:5173`
- `ChoroplethMap` — five-step quantile scale (p0/p25/p50/p75/p100);
  hover popup showing attribute value, confidence tier, territorial note
- `AttributeSelector` — populated from `GET /attributes/available`; runtime
  attribute switching without map remount
- Float prohibition enforced in TypeScript: `attribute_value: string` and
  `QuantitySchema.value: string`; numeric conversion only inside MapLibre
  `["to-number", ["get", "attribute_value"]]` paint expression
- `frontend` service added to `docker-compose.yml` (node:20-slim, port 5173)

**Process and Governance**
- Pre-PR checklist added to CLAUDE.md Implementation Agent section
- `.github/pull_request_template.md` created
- ADR license review framework deployed: ADR-001, ADR-002, ADR-003 all CURRENT
- ADR-004 (Scenario Engine — DRAFT) written and merged as M3 architectural
  pre-work; covers scenario configuration, backtesting, time controls, and
  comparative output
- PM Agent added to CLAUDE.md Agent Team Workflow (in M2 session)

### Deferred

- **Issue #82** — `economy_tier` choropleth hover renders raw ordinal digit
  instead of label; moved to Milestone 3 (`horizon:near-term`)
- **Issues #42, #43, #46, #47, #49** — standards amendments (SA-02 through
  SA-17 subset) moved to Milestone 4 (`horizon:near-term`)
- **Issues #38–#41** — ADRs for Uncertainty Quantification, MeasurementFramework
  Tagging, Non-Linear Propagation, Stock vs. Flow Architecture — remain deferred
  pending STD-REVIEW-001 disposition
- ARCH-REVIEW-002 and STD-REVIEW-002 — governance review cycle due at M2→M3
  boundary; deferred to run in parallel with M3 implementation

### Compliance Posture

- SCAN-005 — PostGIS foundation: **Clean** (0 violations after remediation)
- SCAN-006 — FastAPI layer: **Clean** (0 violations)
- SCAN-007 — MapLibre GL frontend: **Clean** (TypeScript build clean, 0 errors)
- SCAN-008 — Milestone 2 exit gate: **Clean** (0 violations, 2 expected
  warnings — both pre-accepted: ARCH-4 `Relationship.attributes: dict[str, Any]`
  and `Relationship.weight: float` propagation coefficient)
- Open compliance findings carried into M3: **0 Major**, **0 Minor** (Issue #12
  CF-001-F05 minor docstring finding from M1 remains open, no milestone assigned)
- ADR license status at milestone close: ADR-001 CURRENT, ADR-002 CURRENT,
  ADR-003 CURRENT

---

## v0.1.0 — Milestone 1: Simulation Core (2026-04-19)

### Delivered

**Simulation Core Data Model (ADR-001 + Amendment 1 SCR-001)**
- `SimulationEntity` with JSONB-typed `dict[str, Quantity]` attribute store
  (upgraded from `dict[str, float]` via SCR-001)
- `SimulationState`, `Relationship`, `Event` core structures
- `MeasurementFramework` enum (FINANCIAL, HUMAN_DEVELOPMENT, ECOLOGICAL,
  GOVERNANCE) — parallel measurement, no cross-framework conversion
- `ResolutionConfig` with per-entity level overrides
- `Quantity` type system: `value: Decimal`, `unit`, `variable_type`
  (STOCK/FLOW/RATIO/DIMENSIONLESS), `confidence_tier` (1–5),
  `observation_date`, `source_id`, `measurement_framework`
- `MonetaryValue` as `Quantity` subclass with `currency_code`, `price_basis`,
  `exchange_rate_type`
- `propagate_confidence()` — lower-of-two rule (max tier number)
- `SimulationModule` ABC — all modules implement `compute()` and
  `get_subscribed_events()`

**Input Orchestration Layer (ADR-002 + Amendment 1 SCR-001)**
- `ControlInput` ABC with full provenance fields
- Six concrete subclasses: `MonetaryRateInput`, `MonetaryVolumeInput`
  (formerly `MonetaryPolicyInput` — split per SCR-001), `FiscalPolicyInput`,
  `TradePolicyInput`, `EmergencyPolicyInput`, `StructuralPolicyInput`
- `InputOrchestrator` ABC
- `ScenarioRunner` — synchronous in-process orchestrator; complete audit trail
  via in-memory `AuditLog`; contingent inputs with cooldown tracking;
  calendar-year timestep arithmetic (leap-year safe)
- `ContingentInput` with `StateCondition` threshold triggers and
  `empirical_basis` documentation field

**Event Propagation Engine (ADR-001)**
- Hop-by-hop attenuation through directed relationship graph
- Compound attenuation across multiple hops
- STOCK delta semantics (replace) vs. FLOW/RATIO/DIMENSIONLESS (accumulate)
- Confidence tier propagation through accumulation

**Data and Demo**
- `scripts/demo_scenario.py` — runnable demo seeding real country data from
  IMF WEO Oct 2024, World Bank WDI 2024, World Bank WGI 2023, UN Comtrade 2023
- USA tariff escalation scenario specification with Domain Intelligence Council
  review (Development Economist, Political Economist, Geopolitical Analyst)
- 210 tests passing (unit + integration)

**Governance and Standards**
- ARCH-REVIEW-001 — full architecture review, 24 blindspots across 9 council
  agents; Issues #22–#36, #38–#41 opened
- STD-REVIEW-001 — full standards review, 32 findings; 10 immediate issues
  created; ADR-001 and ADR-002 Validity Context sections added; Architecture
  License Framework established in MILESTONE_RUNBOOK.md
- SCR-001 — Material Standards Change Review: Quantity type system and
  MonetaryInput split; ADR-001 and ADR-002 amended
- PM Agent added to CLAUDE.md Agent Team Workflow

### Deferred

- Persistent database seed loader (PostGIS/Alembic) — moved to Milestone 2
- Any web UI — moved to Milestone 2
- Issues #9–#14 (compliance findings from SCAN-001) — various dispositions:
  #9 accepted exception, #10 remediated, #11–#14 minor/deferred
- Issues #22–#36 (ARCH-REVIEW-001 blindspots) — near-term and long-term horizon
- Issues #38–#41 (four deferred ADRs) — pending STD-REVIEW-001 disposition

### Compliance Posture

- SCAN-001 — Initial ADR-001 implementation: **2 Major, 5 Minor** findings
  (#9 accepted exception ARCH-4, #10 remediated, #11–#14 minor/open)
- SCAN-002 — ARCH-REVIEW-001: **24 blindspots** (6 immediate, 9 near-term,
  8 long-term)
- SCAN-003 — STD-REVIEW-001: **32 findings** (5 CONVERGENT, 14 COMPATIBLE,
  1 CONFLICT disposed Option A, 2 DEPENDENCY)
- SCAN-004 — SCR-001 implementation exit: **Clean** (0 violations, 2 expected
  warnings — ARCH-4 and `Relationship.weight: float`)
- ADR license status at milestone close: ADR-001 CURRENT, ADR-002 CURRENT
