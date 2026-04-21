# WorldSim Changelog

Each entry corresponds to a completed milestone. Entries follow the milestone
closure ceremony defined in `docs/MILESTONE_RUNBOOK.md`.

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
