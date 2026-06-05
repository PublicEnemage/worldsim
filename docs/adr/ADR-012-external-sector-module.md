# ADR-012: External Sector Module — BilateralTradeShock and CommodityPriceShock

> **Reader Orientation:** This ADR governs the external sector module boundary introduced
> in M12 G5. Read it before: adding new trade or commodity shock input types, modifying
> import dependency data representation, extending human cost linkage for external shocks,
> or designing multi-entity commodity cascade scenarios. The external sector module is the
> primary entry point for Strait of Hormuz class scenarios and bilateral sanctions modelling.

## Status
ACCEPTED

## Validity Context

**Standards Version:** 2026-06-05
**Valid Until:** See Renewal Triggers below
**License Status:** CURRENT — Accepted 2026-06-05

**Panel review:** 2026-06-05 — `docs/adr/reviews/ADR-012-panel-review.md`
Panel: Architect Agent (author), Chief Engineer (C — propagation routing for bilateral
shocks), Chief Methodologist (C — import dependency estimation for data-poor entities),
Development Economist (C — human cost channel design), Engineering Lead (A).

**Proposed:** 2026-06-05. Based on M12 sprint plan G5 scope (#751, #752) and Demo 4
Strait of Hormuz scenario requirements.

### Renewal Triggers

This ADR must be reviewed and an amendment appended when any of the following occur:

- A third external sector shock type is proposed (neither bilateral nor commodity-global)
- Import dependency data representation moves from entity attributes to a dedicated table
- The human cost channel mapping (commodity category → HCL attribute) is extended or changed
- The `commodity_import_dependency_{category}` attribute naming convention changes
- The step-from-timestep computation in `ExternalSectorModule` is replaced by an explicit
  step counter passed from the runner

---

## Context

### Why the External Sector Is a New Module Boundary

The existing module architecture (Macroeconomic, Demographic, Ecological, Governance,
Political Economy) covers internal policy dynamics: fiscal choices, monetary levers,
demographic responses, ecological feedbacks, and political feasibility constraints.
It does not model the mechanism by which a shock originating outside the sovereign boundary
enters the domestic economy.

The Strait of Hormuz Demo 4 scenario makes this gap concrete: a Jordanian finance ministry
analyst needs to model the effect of a strait closure on Jordan's economy. Jordan cannot
control the strait. The shock is exogenous. Its transmission mechanism is: global crude oil
price rise → Jordan's fuel import cost rises proportional to Jordan's fuel import dependency
→ transportation and energy costs rise → bottom-quintile consumption falls.

This transmission chain requires two new capabilities:
1. A bilateral shock type that routes from a source entity through a trade relationship to
   a target entity — `BilateralTradeShock`.
2. A global commodity shock that distributes simultaneously to all scenario entities
   proportional to their import dependency for the affected commodity — `CommodityPriceShock`.

Neither capability fits cleanly into existing module responsibilities. Both require a new
module boundary.

### Why Two Shock Types, Not One

Bilateral trade shocks (e.g. sanctions, bilateral tariff escalation, Canada steel tariff)
and commodity price shocks (e.g. Hormuz closure, 2008 oil price spike, food price crisis)
have fundamentally different propagation topology:

- **Bilateral:** Source entity → target entity, attenuated by the relationship weight between
  them. Effect magnitude depends on the strength of the bilateral relationship. Other scenario
  entities are unaffected unless the event propagates further through the relationship graph.
- **Commodity (global):** All scenario entities simultaneously, proportional to each entity's
  commodity import dependency coefficient. No bilateral relationship required. Entities with
  higher import dependency receive proportionally larger shocks.

Collapsing these into one shock type requires either a routing flag that changes the
fundamental propagation topology (violating the single responsibility principle) or
special-casing in the propagation engine (coupling the engine to external sector logic).
Two distinct shock types, each with appropriate topology, is the correct boundary.

---

## Decisions

### Decision 1 — BilateralTradeShock as ControlInput Subclass

**Chosen: New `ControlInput` subclass in `orchestration/inputs.py`.**

`BilateralTradeShock` follows the existing `ControlInput` pattern:
- Injected via the `scenario_scheduled_inputs` mechanism at a specific step
- Accepted by `_deserialize_control_input()` under the key `"BilateralTradeShock"`
- `to_events()` generates events on the target entity for the financial and human
  development frameworks
- `propagation_rules` on the generated events govern further graph traversal

**Fields:**
- `source_entity_id: str` — the entity originating the trade disruption
- `target_entity: str` — the entity receiving the shock (inherited from ControlInput)
- `commodity_category: CommodityCategory` — FUEL, FOOD, METALS, OTHER
- `magnitude: Decimal` — positive = import cost increase (price shock or volume reduction)
- `trade_channel: str` — "import_price" or "export_revenue" (default: "import_price")

**Events generated (per `to_events()`):**
1. Financial Event on target entity: `import_price_inflation` attribute delta,
   `framework=MeasurementFramework.FINANCIAL`
2. Human development Event on target entity: `bottom_quintile_consumption_capacity` delta,
   scaled by `_HCL_TRANSMISSION_FACTOR` (0.3 — 30% of import price shock reaches
   bottom-quintile consumption within 1 step), `framework=MeasurementFramework.HUMAN_DEVELOPMENT`

**Alternative rejected: New `ExternalSectorModule` method for bilateral shocks.**

Making bilateral shocks a module responsibility requires the module to know which entity
pairs have active shocks at each step — this couples module state to the scheduler.
ControlInput subclasses cleanly encode "what fires at what step" without coupling.

---

### Decision 2 — CommodityPriceShock as ExternalSectorModule

**Chosen: `ExternalSectorModule(SimulationModule)` with `commodity_price_shocks` from
`ScenarioConfigSchema`.**

A commodity price shock is a global scenario parameter, not an entity-targeted scheduled
input. Its distribution is determined by each entity's import dependency — a property of
the entity, not a bilateral relationship. Encoding this as a `ControlInput` with
`target_entity=""` would require special-casing in the orchestration layer and violates
the ControlInput invariant that every input targets a specific entity.

**Implementation:**
- `CommodityShockConfig` Pydantic model: `commodity_category: str`, `magnitude: Decimal`,
  `start_step: int = 0`, `duration_steps: int = 1`
- `commodity_price_shocks: list[CommodityShockConfig] = []` added to `ScenarioConfigSchema`
- `ExternalSectorModule.__init__(commodity_price_shocks, start_date)` constructed in
  `_build_external_sector_module()` and added to active modules when shocks are non-empty
- `compute(entity, state, timestep)` determines the current step as:
  `round((timestep - start_date_as_datetime).days / 365)` — appropriate for annual resolution
- For each active shock at the current step, looks up
  `entity.get_attribute(f"commodity_import_dependency_{shock.commodity_category}")`
- If non-zero dependency, generates financial and human development events proportional to
  `dependency_coefficient × shock.magnitude`

**Events generated per active shock, per entity with non-zero dependency:**
1. Financial Event: `import_price_inflation` attribute delta, `FINANCIAL` framework
2. Human development Event: `bottom_quintile_consumption_capacity` delta,
   `HUMAN_DEVELOPMENT` framework; scaled by `_HCL_TRANSMISSION_FACTOR`

---

### Decision 3 — Import Dependency Representation as Entity Attributes

**Chosen: `commodity_import_dependency_{category}` as `Quantity` attributes on
`SimulationEntity`.**

Import dependency coefficients are properties of each entity. Representing them as entity
attributes means they are:
- Seedable from the source registry at scenario creation time (same path as all other
  entity attributes)
- Overridable via `initial_attributes` in `ScenarioConfigSchema` (for per-scenario
  dependency adjustments)
- Accessible to the `ExternalSectorModule` via `entity.get_attribute()` with zero
  schema changes to the propagation layer

**Convention:** `commodity_import_dependency_{category}` where `{category}` is the
lowercase commodity category string: `fuel`, `food`, `metals`, `other`. Value is a
`RATIO` Quantity (0.0–1.0 representing fraction of GDP or import basket).

**Data quality:** Real-world import dependency data for Demo 4 entities (Jordan) may
require synthetic estimation. All synthetic estimates must be flagged at the indicator
level as Tier 3 per DATA_STANDARDS.md §Confidence Tier System.

**Alternative rejected: Dedicated `commodity_dependency_coefficients` table.**

A dedicated table introduces a new DB schema surface, a new repository, and a new
query on every scenario execution. Entity attributes are already in the state repository
path. The additional schema complexity is not justified at current scenario scale.

---

### Decision 4 — Human Cost Linkage: Two-Event Pattern

**Chosen: `to_events()` and `compute()` generate separate financial and human development
Events, not a single cross-framework Event.**

Generating two separate Events — one per framework — preserves the measurement framework
invariant established in ADR-001: no conversion rates exist between frameworks. A single
Event with effects on both frameworks would imply a defined exchange rate between financial
impact and human development impact, which is architecturally prohibited.

**Transmission factor (`_HCL_TRANSMISSION_FACTOR = Decimal("0.3")`):** The 30% factor
represents the fraction of an import price shock that reaches bottom-quintile consumption
within one simulation step. Empirical basis: food price transmission elasticities from
World Bank food price crisis analysis (2007–2008) and fuel price pass-through studies
for fuel-importing developing economies. Full calibration deferred to Issue #275 rider;
this factor is explicitly flagged as a simplified approximation in the module docstring.

**Renewal trigger:** If the transmission factor is revised based on Issue #275 calibration,
this ADR must be amended with the new empirical basis.

---

## Module Structure

```
backend/app/simulation/modules/external_sector/
    __init__.py
    module.py    — ExternalSectorModule (CommodityPriceShock distribution)

backend/app/simulation/orchestration/inputs.py (existing)
    + CommodityCategory (enum)
    + BilateralTradeShock (ControlInput subclass)

backend/app/schemas.py (existing)
    + CommodityShockConfig (Pydantic model)
    + ScenarioConfigSchema.commodity_price_shocks field

backend/app/simulation/web_scenario_runner.py (existing)
    + _build_external_sector_module()
    + BilateralTradeShock case in _deserialize_control_input()
```

---

## Consequences

**Positive:**
- Hormuz/Jordan Demo 4 scenario is fully configurable without engine changes
- Bilateral sanctions modelling (Canada steel tariff, Ukraine export channel) works via
  `BilateralTradeShock` with appropriate relationship graph
- CommodityPriceShock naturally extends to multi-entity scenarios (G6a): every entity
  in the scenario receives the shock proportional to its dependency, with no additional
  configuration
- Human cost ledger receives external sector shocks within 2 steps (meets AC requirement)

**Negative:**
- `ExternalSectorModule` step-from-timestep computation assumes annual resolution (365 days).
  If sub-annual timestep resolution is introduced, this calculation must be updated.
- Import dependency coefficients must be seeded in the entity registry before external sector
  scenarios run; entities with missing coefficients silently receive zero shock (no error).

**Risks:**
- Jordan dependency coefficients are synthetic Tier 3 for Demo 4 — directional validation
  only; magnitude is not empirically grounded until real WTO/IMF data is sourced
- `_HCL_TRANSMISSION_FACTOR` is a simplified constant; actual pass-through varies by
  commodity, country, and domestic market structure (Issue #275 calibration tracks this)

---

## References

- Issue #751 — BilateralTradeShock implementation
- Issue #752 — CommodityPriceShock implementation
- Issue #27 — Propagation attenuation calibration documentation (G5 rider)
- Issue #92 — Greece 2010 fixture investment climate (G5 rider)
- Issue #275 — Ecological-to-financial transmission calibration (G5 rider)
- Demo 4 Strait of Hormuz / Jordan scenario
- ADR-001 (measurement framework invariant — no cross-framework conversion)
- ADR-009 (matrix engine — propagation engine that processes generated Events)
- DATA_STANDARDS.md §Confidence Tier System — synthetic Tier 3 flagging requirement
