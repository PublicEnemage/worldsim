# Module Capability Registry

This document is the Domain Intelligence Council's reference for what the
WorldSim simulation can and cannot currently model. Every council review
and every scenario specification should consult this registry before
generating expectations about simulation behaviour.

This is a living document. It is updated whenever a new module is implemented
or an existing module's capabilities change. The registry is dated so that
readers can assess whether it reflects the current codebase.

**Last updated:** 2026-06-04 (Amendment 8 — ADR-011 non-linear propagation)
**Current milestone:** Milestone 11 — Engine Investigation and Political Economy

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

### Event Propagation (ADR-001, Amendment 1; ADR-011)

The simulation can propagate typed `Quantity` attribute deltas through the
relationship graph (SCR-001). All event deltas are `Quantity` instances carrying
`variable_type`, `confidence_tier`, and optional provenance fields.

**Can model:**
- Hop-by-hop attenuation: `delta × attenuation_factor × weight` per hop (LINEAR mode)
- Compound attenuation across multiple hops
- Additive accumulation from multiple propagation paths to the same entity
  (FLOW, RATIO, DIMENSIONLESS variable types)
- STOCK delta semantics: STOCK deltas replace the existing value (no accumulation)
- Multiple propagation rules per event (different relationship types, different
  attenuation factors, different propagation modes)
- Events that propagate along specific relationship types only
- Max_hops limiting propagation depth
- Confidence tier propagation: lower-of-two rule (max tier) through accumulation
- **THRESHOLD propagation** (ADR-011, Issue #29): tipping-point dynamics — delta is
  only applied to a target entity if its |magnitude| meets or exceeds a configurable
  threshold. Models legitimacy collapse, reserve adequacy tipping points.
- **CASCADE propagation** (ADR-011, Issue #29): self-reinforcing amplification — delta
  amplifies by `(1/attenuation_factor) × weight` per hop (inverse of LINEAR), capped
  at `ceiling × |base delta|` per attribute. Models bank-run contagion, currency-peg
  collapse, and debt spiral dynamics. Default `ceiling=1.0` requires explicit opt-in.

**Cannot currently model:**
- Asymmetric propagation (different behaviour in different directions)
- Relationship weight updating based on event history
- Feedback loops within a single timestep (propagation is one-pass)
- Multi-entity CASCADE calibrated parameters (Lebanon, Thailand multi-entity graphs
  are M12 deliverables — see `docs/backtesting/cascade-validation-report.md §5`)

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

- **Domain module contributions:** `WebScenarioRunner` since Milestone 4 wires
  active domain modules. As of M6 exit, four modules are implemented:
  `DemographicModule` (M4, ADR-005 Decision 1), `MacroeconomicModule` (M5,
  regime-dependent multipliers), `EcologicalModule` (M6, initial — planetary
  boundary proximity), `GovernanceModule` (M6, initial — institutional quality).
  Snapshots carry `modules_active` in the v2 envelope (Issue #145). Endogenous
  dynamics are now present; "Interpreting Results" details the remaining
  limitations.

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
- Five historical backtesting cases, all enforced as CI build gate:
  Greece 2010–2012, Argentina 2001–2002, Thailand 1997–2000,
  Lebanon 2019–2020, Ecuador 1999–2000
- DIRECTION_ONLY fidelity thresholds per case (sign checks on key indicators)
- MAGNITUDE thresholds on Greece (gdp_growth step 3) and Argentina (step 2)
  calibrated against historical outturns (Issues #208, #210)
- `fidelity_report.py` — structured fidelity report printed to CI logs on
  every backtesting run; accepts `deferred_thresholds` dict for HCL indicators
  not yet produced endogenously (Issue #87)
- Deferred HCL thresholds in Greece fixture: `unemployment_rising_step1_to_step2`
  and `health_expenditure_declining_step1_to_step2` computed and reported in
  CI output; not a CI gate (no endogenous module produces these — Issue #87)
- Actuals fixtures with IA-1 and parameter calibration disclosures for all five
  cases
- Session-scoped asyncio lifecycle for asyncpg pool (documented in
  `docs/CONTRIBUTING.md §Testing Patterns`)
- `FidelityDashboard.tsx` — React frontend component surfacing per-case
  pass/fail status (M6, Issue #206)

**Cannot currently model:**

- **Magnitude validation on three cases** — Argentina step 2 and Greece step 3
  have MAGNITUDE thresholds; Lebanon, Thailand, and Ecuador remain DIRECTION_ONLY.
  "Backtesting pass" on those cases means the model gets the sign right, not
  that it is quantitatively accurate. See ARCH-REVIEW-003 BI3-N-10 (Issue #160)
  for the required statistical power statement.

- **Human development initial state** — the GRC entity initial state contains
  no WDI-sourced human development attributes. Issue #149 tracks the required
  WDI seed.

- **Machine-readable fidelity artifact** — fidelity report is printed text
  to stdout only; cross-run fidelity trending is not possible (Issue #154)

- **Endogenous HCL backtesting thresholds** — unemployment and health
  expenditure thresholds are deferred (no module produces these endogenously);
  tracked in `deferred_thresholds` param rather than CI gate (Issue #87)

---

## Implemented Modules — Capability Summary

These modules have initial implementations as of M6 exit. Each has a
`compute()` method, an elasticity registry, and unit tests. See the sections
below for what each module can and cannot yet model.

### Macroeconomic Module (Implemented — Milestone 5)

**Can model:**
- Fiscal multiplier effect on GDP growth: regime-dependent (standard 0.5,
  recession 1.5) — responds to `fiscal_policy_spending_change` events
- Inflation dynamics: spending-driven inflation coefficient (`_SPENDING_INFLATION_COEFF`)
  and interest-rate suppression (`_RATE_INFLATION_COEFF`)
- Monetary policy rate change: responds to `monetary_policy_rate_change` events

**Cannot currently model:**
- Debt sustainability analysis (debt service ratios, rollover risk)
- Output gap and potential growth
- Interest rate transmission to investment
- Regime detection is threshold-based (gdp_growth ≥ 0 = standard); does not
  model transition dynamics between regimes

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

### Ecological Module (Implemented — Initial, Milestone 6)

**Can model:**
- CO₂ concentration trajectory response to GDP growth changes
  (`gdp_growth_change` events via `co2_concentration_trajectory` elasticity)
- Planetary boundary proximity response to fiscal spending changes
  (`fiscal_policy_spending_change` events)
- Elasticity registry with `ACADEMIC_LITERATURE_*` source provenance
- `ecological` framework axis in `MultiFrameworkOutput` API response

**Cannot currently model:**
- Climate forcing from IPCC scenario data (full Climate Module planned M8)
- Agricultural stress indices
- Water stress and extreme event modelling
- Climate-driven migration
- Natural capital depletion rate as a separate tracked stock
- Ecological attributes (agricultural productivity, water stress) remain absent
  from `simulation_entities.attributes` initial state — see ARCH-REVIEW-003
  BI3-L-01. Ecological scenarios have no empirically grounded initial conditions.

### Governance Module (Implemented — Initial, Milestone 6)

**Can model:**
- Rule of law percentile response to GDP growth changes (`gdp_growth_change`
  events — `rule_of_law_percentile` elasticity)
- Democratic quality score response to IMF program acceptance
  (`imf_program_acceptance` events)
- Subscribes to: `gdp_growth_change`, `fiscal_policy_spending_change`,
  `imf_program_acceptance`, `emergency_declaration` (ADR-005 Decision 6)
- `governance` framework axis in `MultiFrameworkOutput` API response
- All emitted quantities carry `MeasurementFramework.GOVERNANCE` tag

**Cannot currently model:**
- Institutional Cognitive Integrity Index (planned — M8)
- Policy-reality divergence tracking
- Ghost flight detection (institution executing outdated programming)
- Press freedom and leadership insularity indices
- Full governance composite score (partial elasticities only)

### Climate Module (Planned — Milestone 8)

**Cannot currently model:**
- Climate forcing from IPCC scenario data
- Agricultural stress indices
- Water stress and extreme event modelling
- Climate-driven migration

**Note:** The initial Ecological Module (M6) covers CO₂ trajectory and
planetary boundary proximity. Full climate dynamics remain planned for M8.

### Demographic and Human Cost Module (Implemented — Milestone 4)

**Can model:**
- Poverty headcount ratio response to fiscal spending changes via
  `fiscal_policy_spending_change` events (elasticity-based)
- Cohort entities (`entity_type='cohort'`) with `parent_id` pointing to
  country — ADR-005 Decision 1
- MDA (Minimum Descent Altitude) breach detection across all frameworks
  via `MDAChecker` (M4, extended M5)
- Human Cost Ledger composite scores in `MultiFrameworkOutput` API response
  (`human_development` framework axis)
- MDA alerts surfaced in frontend `RadarChart.tsx` and `MDAAlertPanel.tsx`

**Cannot currently model:**
- Population dynamics beyond poverty headcount (no fertility/mortality model)
- Health system capacity and stress (no health expenditure module)
- Education attainment dynamics
- Migration flows
- Intergenerational effects (annual timesteps; long-horizon consequences
  of policy decisions are outside the modelled window)

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

### What M6/M7 scenario outputs represent

**Scenario outputs since M4 include endogenous module contributions.**
`WebScenarioRunner` since M4 wires active domain modules: `DemographicModule`
(M4), `MacroeconomicModule` (M5), `EcologicalModule` (M6, initial),
`GovernanceModule` (M6, initial). Snapshots carry `modules_active` in the v2
envelope — inspect this field to confirm which modules contributed to any
given snapshot.

Remaining limitation: module contributions are elasticity-based approximations
calibrated to academic literature. Multipliers are regime-dependent but static
within each regime. Dynamic feedback loops, social response, and non-linear
threshold effects are not yet modelled.

### Any scenario run against the current simulation is modelling:
1. The first-round direct effect of the injected ControlInput on the source entity
2. Propagation of that effect through static relationship edges
3. Endogenous module responses: fiscal multiplier (Macroeconomic), poverty
   headcount (Demographic), CO₂ trajectory and planetary boundary pressure
   (Ecological), rule of law and democratic quality (Governance)
4. Multi-step sequences of the above (via `POST /advance`)

### The simulation is NOT modelling:
- Dynamic relationship weight evolution (weights set at scenario initialisation)
- Non-linear threshold effects and regime transitions within a single module
- Social response to policy inputs (strikes, electoral shifts, legitimacy collapse)
- Bilateral trade flows, exchange rate dynamics, capital flows
- Full climate forcing (only initial ecological proxies active)
- Full governance composite (partial elasticities only)

### Safe conclusions from current simulation output:
- Direction of multi-step propagation with active macroeconomic multipliers
- Endogenous poverty and demographic responses to fiscal shocks (direction)
- Initial ecological and governance indicator responses to macro shocks (direction)
- Relative magnitude of first-round exposure across entities
- Direction of change between two scenarios on a single attribute (from `GET /compare`)
- Geographic distribution of scenario divergence (from `DeltaChoropleth`)
- MDA breach detection across financial, human_development, ecological,
  governance framework axes (with partial ecological/governance coverage)

### Conclusions that should not be drawn from current output:
- Precise magnitudes — elasticities are calibrated approximations, not
  verified causal estimates; backtesting confirms direction, not quantity
- Policy optimisation — endogenous response is partial; social and political
  feedback absent
- Crisis threshold predictions — no threshold dynamics within current engine
- **Subnational or community-level impacts** — Level 1 nation-state resolution
  only; country averages conceal regional and community differentiation.
  All scenario API outputs carry a `resolution_disclaimer` field stating this
  limitation explicitly (Issue #100, #158 / ARCH-REVIEW-002 BI2-N-09,
  ARCH-REVIEW-003 BI3-N-08). Rural clinic closures, island emigration,
  regional unemployment differentials — these dynamics are structurally
  invisible at Level 1 and cannot be inferred from national aggregates.
- **Intergenerational and long-horizon effects** — annual-timestep scenarios
  model N steps from a start date; consequences compounding over 20–30 years
  (education truncation, working-age emigration, pension restructuring) are
  outside the modeled window. All scenario detail responses carry a
  `temporal_scope_note` field stating the modeled window explicitly (Issue #98
  / ARCH-REVIEW-002 BI2-N-07).
- Risk-adjusted scenario comparison (no variance or distributional output;
  `DeltaRecord.delta` is a point estimate only)
- Full ecological or governance composite scores — both modules are initial
  implementations with partial elasticity coverage

### Known architectural gaps accepted by Engineering Lead

Resolved from ARCH-REVIEW-003 in M4–M6: ia1_disclosure validation (#144),
snapshot envelope v2 with _modules_active (#145, #146), step-alignment
validation on GET /compare (#150). Open gaps:

| Finding | Status | Issue |
|---|---|---|
| Tombstone excludes entity state at scenario creation | ACCEPTED — SA-11 guarantee incomplete | #147 |
| Greece fixture has no WDI human development initial state | OPEN — WDI seed required | #149 |
| Subnational resolution absent | OPEN — Level 1 only until M8+ | — |
| Full ecological composite score | OPEN — initial module only | M8 |
| Full governance composite score | OPEN — initial module only | M8 |

This registry will be updated with each milestone. Domain Intelligence Council
agents should re-read this registry before completing their scenario review
sections as the simulation's capabilities evolve.
