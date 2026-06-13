# ADR-001: Simulation Core Data Model

## Status
Accepted

## Validity Context

**Standards Version:** 2026-04-15 (date standards documents were established)
**Valid Until:** Milestone 13 — Methodology Publication and Public Launch
**License Status:** CURRENT

**M12 exit review:** 2026-06-10 (SCAN-026). No additional triggers fired after M12 Wave B. ExternalSectorModule generates events on existing `MeasurementFramework.FINANCIAL` and `HUMAN_DEVELOPMENT` Quantity attributes (`reserve_coverage_months`, `bottom_quintile_consumption_capacity`) — no `MeasurementFramework` taxonomy modification. `CohortProfile` fields added in Amendment 2 (Wave B) remain the complete M12 cohort representation change. No `DATA_STANDARDS.md` unit standard changes. License renewed to Milestone 13. Propagation attenuation parameters (`TARIFF_ATTENUATION=0.6`, `TARIFF_MAX_HOPS=2`) are documented as PLACEHOLDER (Tier D) in `docs/methodology/calibration-basis.md §Propagation Rules`; empirical calibration deferred to Issue #44.

**Previously reviewed:** 2026-06-06 — M12 Wave B (Amendment 2). Renewal trigger fired: `SimulationEntity` gains `cohort_profiles` field; `Quantity` gains `attribute_type` and `stock_flow_identity` fields; new `AttributeType` enum and `CohortProfile` dataclass added. Amendment 2 applied — see Amendment 2 section below. License Status renewed to CURRENT. License renewed to Milestone 11.5.

**Previously reviewed:** 2026-06-04 — M11 exit review (SCAN-025). No renewal triggers fired during Milestone 11. PoliticalEconomyModule uses existing `MeasurementFramework.GOVERNANCE` and `HUMAN_DEVELOPMENT` enum values; `legitimacy_index` and `elite_capture_coefficient` are standard Quantity attributes on `SimulationEntity.attributes`. `_steps_projected` field added to state_data envelope (snapshot JSONB — application layer, not Quantity type). Matrix engine uses identical Quantity types and Event contracts — equivalence harness confirms 1e-10 agreement. `InputSource.CONDITIONALITY` and `CompoundStateCondition` extend the orchestration layer (ADR-002 territory), not the core data model. No `MeasurementFramework` taxonomy modifications, no `DATA_STANDARDS.md` unit standard changes affecting attribute store design. License renewed to Milestone 11.5.

**Previously reviewed:** 2026-06-02 — M10 exit review (SCAN-024). No renewal triggers fired
during Milestone 10. GovernanceModule promotion (`"governance"` removed from
`_UNIMPLEMENTED_FRAMEWORKS`) is within the existing `MeasurementFramework` taxonomy
(GOVERNANCE enum value existed since M6) and uses the existing Quantity-delta Event
contract. Argentina 2000–2002 fixture uses existing `initial_attributes` wire format.
PMM endpoint adds `pmm_value`/`pmm_direction` to the trajectory API response — these
are application-layer fields, not `SimulationEntity.attributes` or `Quantity` type
changes. Phase 1 benchmark script is a read-only measurement tool with no schema
changes. No `MeasurementFramework` taxonomy modifications, no `DATA_STANDARDS.md` unit
standard changes affecting attribute store design, no backtesting integrity rule changes
requiring state representation changes. License Status confirmed CURRENT. License
renewed through Milestone 11 — Engine Investigation and Political Economy. Next
scheduled review at Milestone 11 close.

**Previously reviewed:** 2026-05-23 — M9 exit review. No renewal triggers fired during
Milestone 9. M9 was a documentation, standards, and process milestone — no simulation
core data model changes, no `MeasurementFramework` taxonomy changes, no
`DATA_STANDARDS.md` unit standard changes affecting attribute store design, no
backtesting integrity rule changes requiring state representation changes. License
Status confirmed CURRENT. License renewed through Milestone 10 — Engine Integrity and
Instrument Delivery.

**Previously reviewed:** 2026-05-19 — M8 exit review (SCAN-022). No renewal triggers
fired during Milestone 8. M8 EcologicalModule boundary proximity normalization
(`_boundary_proximity_strategy()`) is within the existing `MeasurementFramework`
taxonomy (ECOLOGICAL is an existing enum value) and produces outputs via the existing
Quantity-delta Event contract. No structural changes to `SimulationEntity.attributes`
required. No `MeasurementFramework` taxonomy modifications, no `DATA_STANDARDS.md` unit
standard changes affecting attribute store design. License Status confirmed CURRENT.
License renewed for Milestone 9.

**Previously reviewed:** 2026-05-10 — Milestone 7 exit review. No renewal triggers
fired during Milestone 7. License Status confirmed CURRENT. M7 delivered:
Defensive Programming section added to `CODING_STANDARDS.md` (Issue #224) —
no changes to `MeasurementFramework` taxonomy, `DATA_STANDARDS.md §Units and
Measurements`, or state representation contracts. `[SIM-INTEGRITY]` logging
added to `propagation.py` and all four modules (Issues #243–#245) — engine-
internal additions that do not alter the `Quantity` type structure,
`SimulationEntity.attributes` store design, or `propagate_confidence`
lower-of-two rule. `computeSteps()` collapsed-quantile fix (Issue #82) is a
frontend rendering fix with no state representation changes. HCL deferred
thresholds in Greece fixture (Issue #87) use the existing `deferred_thresholds`
parameter — no backtesting integrity rule or schema change. License renewed
for Milestone 8. Next scheduled review at Milestone 8 — Ecological and
Governance Frameworks completion.

**Previously reviewed:** 2026-05-07 — Milestone 6 exit review. No renewal triggers
fired during Milestone 6. License Status confirmed CURRENT. EcologicalModule
and GovernanceModule (new in M6) produce Quantity-delta Events within the
existing `affected_attributes` contract and do not alter the `Quantity` type
structure, `SimulationEntity.attributes` store design, or
`propagate_confidence` lower-of-two rule. Three additional backtesting cases
(Lebanon, Thailand, Ecuador) and the MAGNITUDE calibration rows use the
existing initial_attributes wire format. FidelityDashboard is a static
frontend component with no changes to simulation state representation.
License renewed for Milestone 7. Next scheduled review at Milestone 7 —
Technical Foundation completion.

**Previously reviewed:** 2026-05-03 — Milestone 5 exit review. No renewal triggers
fired during Milestone 5. License Status confirmed CURRENT. No changes to
`MeasurementFramework` taxonomy, `DATA_STANDARDS.md §Units and Measurements`,
or backtesting integrity rules that affect state representation. The M5
MacroeconomicModule adds `gdp_growth`, `unemployment_rate`, and
`inflation_rate` attributes to `SimulationEntity` but does not alter the
`Quantity` type structure, `SimulationEntity.attributes` store design, or
`propagate_confidence` lower-of-two rule. The Argentina 2001-2002 fixture
(Issue #192) uses existing initial_attributes wire format. License renewed
for Milestone 6.

**Previously reviewed:** 2026-04-26 — Milestone 4 exit review. No renewal triggers
fired during Milestone 4. License Status confirmed CURRENT. No changes to
`MeasurementFramework` taxonomy, `DATA_STANDARDS.md §Units and Measurements`,
or backtesting integrity rules that affect state representation. The M4
DemographicModule adds cohort entities to `SimulationState` but does not
alter `SimulationEntity.attributes` structure — the CohortSpec identity
encoding (colon-delimited string) is additive and does not constitute a
structural change to the attribute store. License renewed for Milestone 5.

**Previously reviewed:** 2026-04-24 — Milestone 3 exit review. No renewal triggers
fired during Milestone 3. License Status confirmed CURRENT. No standards
amendments to `DATA_STANDARDS.md §Units and Measurements` or
`MeasurementFramework` taxonomy occurred during this milestone. License
renewed for Milestone 4.

**Previously reviewed:** 2026-04-21 — Milestone 2 exit review. No renewal
triggers fired. License Status confirmed CURRENT. \
2026-04-19 — Amendment 1 (SCR-001) applied. See Amendment 1 section below.
License Status renewed to CURRENT after implementation verified by 210 passing
tests and SCAN-004 (0 violations).

**Renewal Triggers** — any of the following fires the CURRENT → UNDER-REVIEW
transition:
- `MeasurementFramework` taxonomy modified in any standards document
- Data model unit standard changes in `DATA_STANDARDS.md` that affect
  attribute store design (e.g., stock vs. flow distinction added to `Quantity`)
- Backtesting integrity rules changed in ways that affect state representation
  (e.g., requiring state snapshots to carry data-lineage metadata)
- Stock vs. flow variable distinction added to `DATA_STANDARDS.md §
  Units and Measurements` in ways that require structural changes to
  `SimulationEntity.attributes`

## Date
2026-04-14

## Context
The simulation engine requires a foundational data model that represents
the entities, relationships, and state that the simulation operates on.
This model must support:
- Multiple levels of geographic resolution (country to subnational)
- Temporal state tracking across simulation timesteps
- Event propagation between interconnected entities
- Multiple measurement frameworks simultaneously (financial, human, ecological)
- Extensibility — new modules plug in without restructuring core

The data model is the most consequential early decision. It either
enables or constrains everything built on top of it.

## Decision

### Core Entity: SimulationEntity
All entities in the simulation (countries, regions, institutions) inherit
from a common base. This allows the event propagation engine to operate
uniformly regardless of entity type.

```python
class SimulationEntity:
    id: str                    # unique identifier
    entity_type: str           # 'country', 'region', 'institution'
    parent_id: Optional[str]   # for hierarchical relationships
    geometry: Optional[Geometry]  # PostGIS spatial reference
    attributes: Dict[str, float]  # current state variables
    metadata: Dict[str, Any]   # non-simulation data (name, codes, etc.)
```

### Core Structure: SimulationState
The complete state of the simulation at a single timestep.

```python
class SimulationState:
    timestep: datetime
    resolution: ResolutionConfig   # which levels are active
    entities: Dict[str, SimulationEntity]
    relationships: List[Relationship]  # trade, alliance, debt, etc.
    events: List[Event]            # events active this timestep
    scenario_config: ScenarioConfig
```

### Core Structure: Relationship
Directed relationships between entities carry the propagation weights.

```python
class Relationship:
    source_id: str
    target_id: str
    relationship_type: str     # 'trade', 'debt', 'alliance', 'currency'
    weight: float              # propagation strength
    attributes: Dict[str, float]  # relationship-specific data
```

### Core Structure: Event
Events propagate through the relationship graph each timestep.

```python
class Event:
    event_id: str
    source_entity_id: str
    event_type: str            # 'policy_change', 'shock', 'threshold_crossed'
    affected_attributes: Dict[str, float]  # what changes and by how much
    propagation_rules: List[PropagationRule]
    timestep_originated: datetime
```

### Measurement Frameworks
State variables are tagged with their measurement framework.
No conversion rates between frameworks. Outputs are parallel, not aggregated.

```python
class MeasurementFramework(Enum):
    FINANCIAL = "financial"
    HUMAN_DEVELOPMENT = "human_development"
    ECOLOGICAL = "ecological"
    GOVERNANCE = "governance"
```

### Module Interface
Every simulation module implements this interface.
Modules register with the engine. The engine calls them each timestep.

```python
class SimulationModule(ABC):
    @abstractmethod
    def compute(
        self,
        entity: SimulationEntity,
        state: SimulationState,
        timestep: datetime
    ) -> List[Event]:
        """
        Given current entity state and global simulation state,
        compute this module's contribution and return events
        to propagate.
        """
        pass

    @abstractmethod
    def get_subscribed_events(self) -> List[str]:
        """
        Which event types does this module respond to?
        """
        pass
```

## Alternatives Considered

**Relational tables only (no graph)**
Simpler to query. But relationship traversal for event propagation
becomes expensive SQL joins. The graph structure is the simulation's
core operation — it should be a first-class architectural concept,
not an emergent property of table joins.

**Single measurement framework with conversion**
Simpler outputs. But false aggregation hides exactly the information
that matters most — a country that is financially stable but in a
human development crisis looks fine in a single metric. The parallel
framework approach is non-negotiable given the project's mission.

**Agent-based from the start**
More realistic emergence. But computational cost at global scale
is prohibitive for initial build and the questions we're answering
in early milestones don't require individual-level agents.
Architecture supports adding this layer later at Level 6.

## Consequences

**Positive**
- Event propagation engine operates uniformly across all entity types
- New modules plug in by implementing SimulationModule interface
- Measurement framework separation is enforced architecturally
- Hierarchical resolution is native to the entity model
- Temporal state tracking supports backtesting naturally

**Negative**
- More abstract than a simple table-per-concept approach
- Requires discipline to maintain module interface contracts
- Graph operations require careful performance management at scale

## Next ADR
ADR-002 will address the database schema and PostGIS spatial data model.

---

## Amendment 1 — SCR-001: Quantity Type System

**Date:** 2026-04-19
**Closes:** #51 (Quantity type system), #65 (variable_type enforcement),
#66 (confidence_tier propagation), #67 (MonetaryValue as Quantity subclass),
#68 (ingestion pipeline requirements)
**Implemented in:** PR closing #51, #58, #65–#68

### What Changed

`SimulationEntity.attributes` changed from `dict[str, float]` to
`dict[str, Quantity]`. `Event.affected_attributes` changed from
`dict[str, float]` to `dict[str, Quantity]`.

The `Quantity` type now carries:
- `value: Decimal` — numeric amount, never float
- `unit: str` — canonical unit string
- `variable_type: VariableType` — new required field (STOCK, FLOW, RATIO, DIMENSIONLESS)
- `confidence_tier: int` — data quality tier 1–5
- `measurement_framework`, `observation_date`, `source_id` — optional provenance fields

`MonetaryValue` is now a `Quantity` subclass, adding `currency_code`,
`price_basis`, and `exchange_rate_type`. The former `amount` field is replaced
by the inherited `value` field.

`propagate_confidence(*quantities) -> int` is the canonical function for
computing output `confidence_tier` from input quantities. It uses the
lower-of-two rule: `max(q.confidence_tier for q in quantities)` — the highest
tier number (= lowest confidence quality) wins.

`SimulationEntity.get_attribute(key) -> Quantity | None` and
`get_attribute_value(key, default=Decimal("0")) -> Decimal` replace the former
`get_attribute(key, default)` float accessor.

`apply_delta(key, delta: Quantity)` semantics: STOCK delta replaces the
existing value; FLOW/RATIO/DIMENSIONLESS deltas accumulate additively.

`Relationship.attributes` remains `dict[str, Any]` — relationship metadata is
mixed-type (ARCH-4 disposition from SCR-001, approved by Engineering Lead).

### Known Limitations at Amendment Time

**IA-1 — RESOLVED (M11, Issue #151):** Confidence tier horizon degradation is
implemented at the output layer via `effective_tier(source_tier, horizon_steps)`
in `app/api/scenarios.py` and recorded in each snapshot's `_steps_projected`
envelope field. Schedule: +1 tier per 5 projection steps, capped at Tier 5.
`IA1_CANONICAL_PHRASE` in `quantity_serde.py` documents the schedule verbatim.
The `_steps_projected` key was added in state_data envelope version "3"
(`STATE_DATA_ENVELOPE_VERSION`). Closed by Issue #151 (ARCH-REVIEW-003 BI3-N-01).

**CM-1:** The lower-of-two rule overstates uncertainty when inputs are
independent and mutually corroborating. This is accepted — overstatement
is the preferred failure mode for a sovereign policy tool.

### Renewal Triggers Added

In addition to original triggers, this amendment adds:
- `VariableType` enum values modified (STOCK/FLOW/RATIO/DIMENSIONLESS)
- `propagate_confidence` rule changed to anything other than lower-of-two
- `Quantity` field contract broken (required fields removed or type changed)

---

## Amendment 2 — Issue #28, Issue #30: CohortProfile and AttributeType

**Date:** 2026-06-06
**Closes:** Issue #28 (CohortProfile dataclass), Issue #30 (AttributeType enum)
**Implemented in:** PR closing #28 + #30 (M12 Wave B, branch feat/nb3-entity-model)

### What Changed

**`AttributeType` enum** added to `app/simulation/engine/quantity.py`:

```python
class AttributeType(str, Enum):
    STOCK = "stock"
    FLOW = "flow"
    STRUCTURAL_INDEX = "structural_index"
    RATE = "rate"
```

Economic-semantic classification — complementary to `VariableType`. `VariableType`
drives propagation behaviour (STOCK replaces, FLOW accumulates). `AttributeType`
records what the quantity *means* economically (balance-sheet stock, income-statement
flow, headcount rate, composite index). Both fields can coexist on the same Quantity.

**Two new optional fields on `Quantity`:**
- `attribute_type: AttributeType | None = None` — economic classification; None when not yet assigned
- `stock_flow_identity: bool = False` — when True, engine warns if `stock[t+1] ≠ stock[t] + net_flow[t]`

Both fields are **backwards-compatible** — all existing Quantity instances remain valid
with `attribute_type=None, stock_flow_identity=False`.

**`CohortProfile` dataclass** added to `app/simulation/engine/models.py`:

```python
@dataclass
class CohortProfile:
    attributes: dict[str, Quantity]
```

Income-quintile or age-band level attribute container for one entity cohort.
Not a sub-entity — cohort profiles do not participate in the propagation graph.

**`cohort_profiles: dict[str, CohortProfile] | None = None`** field added to
`SimulationEntity`. Cohort key convention: `"Q1"`–`"Q5"` for income quintiles,
`"youth_15_24"` etc. for age bands.

**Cohort key convention** (canonical):
- Income quintiles: `"Q1"` (lowest) through `"Q5"` (highest)
- Age bands: `"youth_15_24"`, `"prime_25_54"`, `"older_55_64"`, `"senior_65plus"`
- Cross-dimension: `"Q1_youth_15_24"` (underscore separator)

**JSONB storage path:**
- `attribute_type` and `stock_flow_identity` added to the SA-09 Quantity envelope.
  `attribute_type` omitted when None; `stock_flow_identity` omitted when False
  (wire-space optimisation preserving backwards compatibility with v1 snapshots).
- `cohort_profiles` stored as `"_cohort_profiles"` sub-key within the entity's block
  in `scenario_state_snapshots.state_data`. Underscore prefix marks it as metadata,
  invisible to the compare endpoint's attribute key iteration.
- Serialised via `cohort_profile_to_jsonb` / `cohort_profile_from_jsonb` in
  `app/simulation/repositories/quantity_serde.py`.
- NOT stored in `simulation_entities.attributes` (that column holds entity baseline
  attributes, not distributional cohort data).

**Snapshot reconstruction** (`web_scenario_runner.py` `_reconstruct_state_from_snapshot`):
- `_cohort_profiles` popped from `attr_data` before quantity iteration
- All underscore-prefixed keys skipped in quantity loop (defensive, future-proof)
- `cohort_profile_from_jsonb` called per cohort; result passed as `cohort_profiles=`
  to `SimulationEntity` constructor

**Greece M12 seed fixture** (EU-SILC 2010, Tier 2, `source_registry_id="EU_SILC_2010_GRC"`):
- `Q1.poverty_headcount = 0.201` (RATE, dimensionless)
- `Q5.poverty_headcount = 0.065` (RATE, dimensionless)
- `Q1.unemployment_rate = 0.18` (RATE, dimensionless)

### Known Limitations at Amendment Time

**CP-1:** `CohortProfile` is a distributional data container only. Cohort profiles
do not participate in the propagation graph — modules cannot emit Events that target
a cohort profile, only cohort entities (the existing `GRC:CHT:...` entity injection
pattern from ADR-005). Full distributional-level propagation (Q1 attributes respond
differently to fiscal shocks than Q5) is deferred to a future amendment.

**CP-2:** `stock_flow_identity` flag records intent but enforcement (the actual
engine warning) is not yet wired into the propagation engine. Flag is stored and
round-trips through JSONB; engine enforcement is an M13 obligation.

### Renewal Triggers Added

In addition to triggers from Amendments 1 and original ADR, this amendment adds:
- `AttributeType` enum values modified or removed
- `CohortProfile.attributes` field contract broken
- Cohort key convention changed without migration path
- `_cohort_profiles` JSONB storage key renamed without migration
