# ADR-001: Simulation Core Data Model

## Status
Accepted

## Validity Context

**Standards Version:** 2026-04-15 (date standards documents were established)
**Valid Until:** Milestone 2 completion
**License Status:** CURRENT

**Last Reviewed:** 2026-04-17 — STD-REVIEW-001 completed. All renewal triggers
checked; none fired. STD-REVIEW-001 created issues tracking standards amendments
(#42–#51) but did not apply amendments to standards documents. The standards
documents as they stand did not change in ways that activate any trigger below.
Next scheduled review at Milestone 2 completion.

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
