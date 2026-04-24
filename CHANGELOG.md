# WorldSim Changelog

Each entry corresponds to a completed milestone. Entries follow the milestone
closure ceremony defined in `docs/MILESTONE_RUNBOOK.md`.

---

## v0.3.0 — Milestone 3: Scenario Engine (2026-04-24)

### Delivered

**Scenario Configuration (ADR-004 Decision 1)**
- Three new database tables via Alembic migration: `scenarios`
  (configuration JSONB, status, engine_version), `scenario_state_snapshots`
  (step-indexed state JSONB, `ia1_disclosure` NOT NULL enforced at DB level),
  `scenario_tombstones` (deleted scenario config + scheduled_inputs JSONB for
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
