# Module Capability Registry

This document is the Domain Intelligence Council's reference for what the
WorldSim simulation can and cannot currently model. Every council review
and every scenario specification should consult this registry before
generating expectations about simulation behaviour.

This is a living document. It is updated whenever a new module is implemented
or an existing module's capabilities change. The registry is dated so that
readers can assess whether it reflects the current codebase.

**Last updated:** 2026-04-24 (Amendment 4 — ADR-004 Scenario Engine)
**Current milestone:** Milestone 3 — Scenario Engine

---

## What the Simulation Can Currently Model

### Entity State Representation

The simulation can represent any entity (country, institution, region) as a
collection of named `Quantity` attributes (SCR-001 / ADR-001 Amendment 1).
Each attribute carries a value, unit, variable type, confidence tier, and
optional provenance fields.

**Can model:**
- Any numerical indicator expressible as a `Quantity` (Decimal value + unit +
  variable_type + confidence_tier)
- STOCK variables (level at a point in time — reserves, debt outstanding)
- FLOW variables (period changes — GDP, exports, deficit)
- RATIO variables (dimensionless fractions — debt/GDP, inflation rate)
- DIMENSIONLESS variables (indexes and scores — HDI, capability indexes)
- Entity metadata (name, ISO codes, etc.) stored separately from simulation
  attributes
- Hierarchical entity relationships (parent_id field)
- Basic spatial reference (geometry field — MULTIPOLYGON SRID 4326, PostGIS schema live in Milestone 2)
- PostGIS persistence: 5-table schema (`simulation_entities`, `relationships`,
  `territorial_designations`, `source_registry`, `control_input_audit_log`) via
  Alembic migration `126eb2fd0afd` — ADR-003 Decision 1
- Territorial validation hard gate (TerritorialValidator) enforces all 5 POLICY.md
  positions before any INSERT: TWN, PSE, XKX, ESH, CRIMEA
- Natural Earth 110m boundary loader: 10 Level 1 attributes from NE properties,
  POLYGON→MULTIPOLYGON promotion, cache-first GeoJSON fetch, source registry check
- Confidence tier tracking: `confidence_tier` 1–5 on every attribute,
  propagated via the lower-of-two rule (max tier number)
- MapLibre GL React frontend available at http://localhost:5173 in development,
  consuming `GET /api/v1/choropleth/{attr}` and `GET /api/v1/attributes/available`.
  Renders country polygons colored by simulation attribute values in a five-step
  blue choropleth. Hover popup surfaces attribute value, confidence tier, and
  territorial position notes for disputed entities. Attribute selector populated
  from available attributes endpoint. Default attribute: `ne_pop_est`.
  Docker Compose service: `frontend` (node:20-slim, port 5173).

**Cannot currently model:**
- Categorical attributes (regime type, currency peg status)
- Time series within an entity (only current-period state is held in
  `simulation_entities`; per-step state is held in scenario snapshots — see
  Scenario Engine section)
- Confidence tier degradation by projection horizon — IA-1 compliance exception
  (Issue #69, deferred to Milestone 4). All scenario projection outputs carry
  the `confidence_tier` of their historical input data regardless of how many
  steps forward the projection extends. This is an accepted limitation; the
  `ia1_disclosure` field on all snapshots is the disclosure mechanism, but it
  is currently enforced as NOT NULL only — see ARCH-REVIEW-003 BI3-I-01.

### Bilateral Relationships

The simulation can represent directed weighted relationships between pairs
of entities.

**Can model:**
- Directional trade relationships with weights reflecting coupling strength
- Debt relationships
- Alliance relationships
- Any other relationship type expressible as a directed edge with a float weight
- Multiple relationship types between the same entity pair

**Cannot currently model:**
- Dynamic relationship weights (weights are set at scenario initialisation
  and do not change during a run)
- Relationship attributes beyond weight (e.g. tariff rate, debt maturity profile)
- Relationship-level metadata (data source, vintage date)

### Event Propagation (ADR-001, Amendment 1)

The simulation can propagate typed `Quantity` attribute deltas through the
relationship graph (SCR-001). All event deltas are `Quantity` instances carrying
`variable_type`, `confidence_tier`, and optional provenance fields.

**Can model:**
- Hop-by-hop attenuation: `delta.value × attenuation_factor × edge.weight` per hop
- Compound attenuation across multiple hops
- Additive accumulation from multiple propagation paths to the same entity
  (FLOW, RATIO, DIMENSIONLESS variable types)
- STOCK delta semantics: STOCK deltas replace the existing value (no accumulation)
- Multiple propagation rules per event (different relationship types, different
  attenuation factors)
- Events that propagate along specific relationship types only
- Max_hops limiting propagation depth
- Confidence tier propagation: lower-of-two rule (max tier) through accumulation

**Cannot currently model:**
- Non-linear propagation (threshold effects, saturation)
- Asymmetric propagation (different behaviour in different directions)
- Relationship weight updating based on event history
- Feedback loops within a single timestep (propagation is one-pass)

### Input Orchestration (ADR-002)

The simulation can accept exogenous control inputs through the orchestration
layer.

**Can model:**
- Six input types: MonetaryRateInput, MonetaryVolumeInput, FiscalPolicyInput,
  TradePolicyInput, EmergencyPolicyInput, StructuralPolicyInput (SCR-001:
  former MonetaryPolicyInput split into MonetaryRateInput and MonetaryVolumeInput)
- Scheduled inputs at specific timesteps
- Contingent inputs triggered by single-attribute threshold conditions
- Cooldown periods preventing repeated triggering
- Complete audit trail of all injected inputs
- Multi-step scenario execution with state history (via WebScenarioRunner — see
  Scenario Engine section)

**Cannot currently model:**
- Input validation against feasible policy space (political feasibility not
  modelled — ARCH-REVIEW-003 BI3-N-06)
- Compound contingent triggers requiring multi-attribute AND/OR conditions
  (ARCH-REVIEW-003 BI3-N-07, Issue #157)
- Multi-stage inputs (inputs that unfold over multiple timesteps automatically)
- Input interactions (two simultaneous inputs whose effects depend on each other)
- Coercive dynamics — IMF conditionality, sanctions, external pressure modelled
  as unilateral sovereign decisions (ARCH-REVIEW-003 BI3-L-03)
- Social response feedback — policy inputs do not generate endogenous backlash
  events in subsequent timesteps (ARCH-REVIEW-003 BI3-N-09, Issue #159)

### Scenario Engine (ADR-004)

Added in Milestone 3. The scenario engine enables persistent, multi-step,
web-accessible scenario execution with snapshot storage and comparative output.

**Can model:**

*Scenario configuration and persistence:*
- `ScenarioConfig` Pydantic schema with full validation: entity scope,
  modules config, initial attribute overrides, engine version declaration
- Three new database tables via Alembic migration:
  - `scenarios` — configuration JSONB, status, engine_version
  - `scenario_state_snapshots` — step-indexed state JSONB with `_envelope_version: "1"`
    and `ia1_disclosure NOT NULL`; float prohibition enforced (`value: str`)
  - `scenario_deleted_tombstones` — deleted scenario config JSONB + scheduled_inputs
    JSONB for reconstruction from first principles (SA-11 determinism guarantee)
- Four scenario API endpoints:
  - `POST /scenarios` — create scenario from ScenarioConfig
  - `GET /scenarios/{id}` — retrieve scenario configuration and status
  - `GET /scenarios/{id}/snapshots` — retrieve all step snapshots
  - `DELETE /scenarios/{id}` — soft-delete with tombstone write

*Execution:*
- `WebScenarioRunner` — async scenario executor wiring `SimulationStateRepository`
  (reads/writes `SimulationState` from PostGIS DB) and `ScenarioSnapshotRepository`
  (writes step snapshots with SA-09 envelope format)
- `SimulationStateRepository` builds `SimulationState` from PostGIS entities
- SA-11 determinism guarantee: same configuration + same scheduled inputs +
  same engine version → identical snapshot outputs

*Time acceleration:*
- `POST /scenarios/{id}/advance` — advances scenario by configurable number of
  steps; returns `AdvanceResponse` with `steps_completed`, `final_status`, and
  `snapshots` array
- Step-aware choropleth: `GET /choropleth/{attribute}?scenario_id={id}&step={N}` —
  geometry from `simulation_entities` (stable), attribute values from
  `scenario_state_snapshots` (step-specific); returns 422 if only one of
  scenario_id / step is provided

*Comparative scenario output:*
- `GET /scenarios/compare?scenario_a={id}&scenario_b={id}&attribute={attr}&step={N}` —
  returns `CompareResponse` with per-entity `DeltaRecord` (value_a, value_b,
  delta, direction, confidence_tier); registered before `/{scenario_id}` to
  avoid FastAPI path collision
- `GET /choropleth/{attribute}/delta?scenario_a={id}&scenario_b={id}` — delta
  choropleth returning `GeoJSONFeatureCollection` with `delta_direction` and
  both base values; Decimal delta computation (no float)
- `DeltaChoropleth.tsx` — diverging colour scale (crimson → white → navy);
  percentile-based step computation for negative and positive halves separately;
  legend overlay; hover popup with delta direction icon

*Tombstone design:*
- `DELETE /scenarios/{id}` writes tombstone capturing name, configuration JSONB,
  scheduled_inputs JSONB, engine_version, and original_created_at before
  CASCADE delete of the scenario and its snapshots
- Snapshots are derived data and are not tombstoned — reproducible from the
  tombstone given the same engine version under SA-11

**Cannot currently model:**

- **Domain module contributions:** `WebScenarioRunner` in Milestone 3 executes
  scenarios against an empty module list — no domain modules (Macroeconomic,
  Trade, Demographic, Climate) are implemented. All scenario outputs reflect
  first-round ControlInput propagation through static relationship weights
  only. There are no endogenous dynamics, no multiplier effects, no feedback
  loops. Every M3 snapshot carries `modules_active: []` (see Issue #145, #146).
  **This is the most important limitation of M3 scenario outputs.** See
  "Interpreting Results" for the full safe/unsafe conclusion list.

- **Confidence tier degradation with projection horizon** — IA-1 compliance
  exception applies to all snapshot outputs (Issue #69, Issue #144)

- **Multi-attribute simultaneous comparison** — `GET /compare` is single-attribute
  per call; comparing N attributes requires N serial API calls with no structured
  relationship between results

- **Step-alignment validation** — `GET /compare` does not validate that both
  scenarios have been advanced to the requested step; if one scenario has fewer
  snapshots, the behavior is undefined (Issue #150)

- **Absolute color scale on DeltaChoropleth** — color scale is percentile-
  relative to the current comparison set; global downturns appear as mixed
  winners/losers; threshold crossings are visually indistinguishable from
  marginal changes (ARCH-REVIEW-003 BI3-N-03, Issue #153)

- **Tombstone entity state capture** — tombstone records configuration and
  scheduled inputs but not the entity attribute state at scenario creation time;
  SA-11 reconstruction after a Natural Earth loader update starts from a
  different baseline (ARCH-REVIEW-003 BI3-I-04, Issue #147)

- **Scenario restore API** — no `POST /scenarios/restore` endpoint; tombstone
  reconstruction is a manual multi-step operation (Issue #155)

- **Distributional comparison** — `DeltaRecord.delta` is a Decimal point
  estimate; no variance, percentile range, or confidence interval on deltas

- **Political context in scenario configuration** — no legitimacy initial state,
  electoral calendar, or coalition stability fields (Issue #156)

### Backtesting Infrastructure (ADR-004 Decision 3)

Added in Milestone 3. Backtesting is a CI build gate — a failure in the
backtesting suite is a build failure.

**Can model:**
- Greece 2010–2012 backtesting case (`tests/backtesting/test_greece_2010_2012.py`),
  4 tests marked `backtesting`, enforced as CI build gate
- DIRECTION_ONLY fidelity thresholds: gdp_growth negative at steps 1–3;
  unemployment rising step 1 → step 3 (6 sign checks total)
- `fidelity_report.py` — structured fidelity report printed to CI logs on
  every backtesting run
- `greece_2010_2012_actuals.py` — historical actuals fixture with IA-1 and
  parameter calibration disclosures
- `natural_earth_loader.py` seed script runs in CI before backtesting suite
  to ensure GRC entity exists
- Session-scoped asyncio lifecycle for asyncpg pool (three-place `loop_scope=
  "session"` pattern — documented in `docs/CONTRIBUTING.md §Testing Patterns`)

**Cannot currently model:**

- **Magnitude validation** — DIRECTION_ONLY thresholds are sign checks only.
  A model producing GDP growth of −0.01% passes identically to one producing
  −8.9%. "Backtesting pass" means the model gets the sign right on 6 binary
  tests. It does not mean the model is quantitatively accurate. See
  ARCH-REVIEW-003 BI3-N-10 (Issue #160) for the required statistical power
  statement to accompany all fidelity reports.

- **Human development initial state** — the GRC entity initial state contains
  no WDI-sourced human development attributes (unemployment stock, health
  expenditure, net enrollment). The unemployment direction threshold tests
  movement of an attribute with no empirically grounded initial value.
  Issue #149 tracks the required WDI seed.

- **Machine-readable fidelity artifact** — fidelity report is printed text
  to stdout only; cross-run fidelity trending is not possible (Issue #154)

- **Human development or ecological backtesting thresholds** — all current
  thresholds are financial/macroeconomic indicators; no HCL or ecological
  fidelity checks exist

---

## What the Simulation Cannot Currently Model

The modules listed here are specified in CLAUDE.md and planned for future
milestones. Until a module is implemented, its domain of effects cannot be
modelled endogenously. Exogenous ControlInputs can inject point-in-time
shocks as proxies, but the module's endogenous dynamics (multipliers, feedback
loops, regime-switching behaviour) are absent.

### Macroeconomic Module (Planned — Milestone X)

**Cannot currently model:**
- GDP growth rate dynamics (fiscal multiplier, consumption function)
- Inflation dynamics (Phillips curve, monetary transmission)
- Debt sustainability analysis (debt service ratios, rollover risk)
- Fiscal multiplier (including inversion in depressed demand regimes)
- Interest rate dynamics and monetary transmission mechanism
- Output gap and potential growth

**Impact on scenario outputs:** Scenarios involving fiscal consolidation,
monetary policy, or debt dynamics are missing their primary endogenous engine.
ControlInput shocks can inject first-round effects but compounding dynamics
and feedback loops are absent.

### Trade and Currency Module (Planned — Milestone X)

**Cannot currently model:**
- Bilateral trade flows and their evolution under tariff shocks
- Exchange rate dynamics (pass-through, J-curve effects)
- Terms of trade dynamics
- Trade balance and current account dynamics
- Trade diversion and deflection patterns
- Dynamic relationship weights reflecting evolving trade patterns

**Impact on scenario outputs:** Trade policy scenarios (tariffs, sanctions)
can inject first-round shocks but cannot model the rebalancing and diversion
dynamics that typically follow. The simulation has no mechanism to update
trade weights in response to policy changes.

### Monetary System Module (Planned — Milestone X)

**Cannot currently model:**
- Reserve currency dynamics
- SWIFT/payment network exposure
- Sovereign debt holdings matrix
- Currency confidence indices
- De-dollarisation dynamics
- Capital flight and sudden stop dynamics

### Capital Flow Module (Planned — Milestone X)

**Cannot currently model:**
- Foreign direct investment flows
- Portfolio flow dynamics
- Hot money and capital flight
- Illicit financial flows

### Geopolitical Module (Planned — Milestone X)

**Cannot currently model:**
- Alliance relationship dynamics
- Military capability indices
- Diplomatic channel quality
- Information environment integrity
- Escalation and de-escalation dynamics

### Climate Module (Planned — Milestone X)

**Cannot currently model:**
- Climate forcing from IPCC scenario data
- Agricultural stress indices
- Water stress and extreme event modelling
- Climate-driven migration

**Note:** Ecological attributes (agricultural productivity, water stress,
carbon trajectory, deforestation rate) are entirely absent from
`simulation_entities.attributes`. Ecological scenarios have no initial
conditions to run from — see ARCH-REVIEW-003 BI3-L-01.

### Demographic and Health Module (Planned — Milestone 4)

**Cannot currently model:**
- Population dynamics and cohort modelling
- Health system capacity and stress
- Education attainment dynamics
- Migration flows

**Note:** ADR-005 (Accepted, 2026-04-24) specifies the cohort data model
and Human Cost Ledger output for Milestone 4. Cohort entities will reuse the
existing `simulation_entities` table with `entity_type='cohort'` and
`parent_id` pointing to the country.

### Financial Warfare Module (Planned — Milestone X)

**Cannot currently model:**
- Currency attack vulnerability indices
- Sanctions exposure modelling
- Cyber infrastructure vulnerability
- Information environment manipulation

### Institutional Cognition Module (Planned — Milestone X)

**Cannot currently model:**
- Institutional Cognitive Integrity Index
- Policy-reality divergence tracking
- Ghost flight detection (institution executing outdated programming)

---

## Interpreting Results Given Current Limitations

### What M3 scenario outputs represent

**All M3 scenario outputs are ControlInput-propagation-only results.**
`WebScenarioRunner` in Milestone 3 executes with an empty module list. No
domain modules are active. Every attribute delta in every M3 snapshot originates
from either (a) a directly injected ControlInput or (b) that input's propagation
through static relationship weights. There are no endogenous dynamics.

This will change in Milestone 4 when domain modules (DemographicModule from
ADR-005) are wired into `WebScenarioRunner`. M4 snapshots will contain
endogenous module contributions that M3 snapshots do not. M3 and M4 snapshots
will be structurally distinguishable via `_modules_active` envelope metadata
once Issue #145 and #146 are implemented — until then, they are not.

### Any scenario run against the current simulation is modelling:
1. The first-round direct effect of the injected ControlInput on the source entity
2. Propagation of that effect through static relationship edges
3. Accumulation across multiple ControlInputs at each step (where present)
4. Multi-step sequences of the above (via `POST /advance`)

### The simulation is NOT modelling:
- Endogenous module responses to changed state
- Dynamic relationship weight evolution
- Multiplier and feedback loop effects
- Regime-switching behaviour
- Social response to policy inputs (strikes, electoral shifts, legitimacy collapse)
- Any of the module domains listed above as absent

### Safe conclusions from current simulation output:
- Direction of multi-step propagation through scripted ControlInput sequences
- Relative magnitude of first-round exposure across entities (which countries
  are more or less connected to the shock source)
- Structural network properties (which entities are hubs, which are peripheral)
- Direction of change between two scenarios on a single attribute at a specific
  step (from `GET /compare`)
- Geographic distribution of scenario divergence (from `DeltaChoropleth`)

### Conclusions that should not be drawn from current output:
- Precise magnitudes (no calibrated multipliers or feedback loops)
- Dynamic trajectories representing endogenous economic adjustment (only scripted
  input sequences, not model-computed responses)
- Policy optimisation (no endogenous response to simulate the counterfactual)
- Crisis threshold predictions (no threshold dynamics in current engine)
- Subnational or community-level impacts (Level 1 nation-state resolution only;
  country averages conceal regional and community differentiation — see
  ARCH-REVIEW-003 BI3-N-08)
- Intergenerational effects (annual timesteps; long-horizon consequences of
  policy decisions are outside the modelled window)
- Confidence in projection magnitude (IA-1 compliance exception — all projection
  outputs carry input data confidence tier regardless of projection distance)
- Risk-adjusted scenario comparison (no variance or distributional output;
  `DeltaRecord.delta` is a point estimate only)

### Known architectural gaps accepted by Engineering Lead (ARCH-REVIEW-003)

These findings are tracked in GitHub Issues and will be addressed in Milestone 4.
Council agents should not re-discover them as new findings:

| Finding | Status | Issue |
|---|---|---|
| `ia1_disclosure` NOT NULL but semantically void | ACCEPTED — M4 fix required before projection outputs | #144 |
| Snapshot envelope has no migration path for M4 module additions | ACCEPTED — `_modules_active` metadata required before M4 wiring | #145 |
| M3 snapshots carry no signal that domain modules are absent | ACCEPTED — `modules_active` in SnapshotResponse required | #146 |
| Tombstone excludes entity state at scenario creation | ACCEPTED — SA-11 guarantee is incomplete until resolved | #147 |
| Greece fixture has no WDI human development initial state | ACCEPTED — WDI seed required before Issue #142 begins | #149 |
| `GET /compare` has no step-alignment validation | ACCEPTED — 422 required; silent misalignment is a correctness bug | #150 |

This registry will be updated with each milestone. Domain Intelligence Council
agents should re-read this registry before completing their scenario review
sections as the simulation's capabilities evolve.
