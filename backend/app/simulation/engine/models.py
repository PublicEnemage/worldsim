"""
Simulation core data model — ADR-001.

All entities, relationships, events, and measurement structures that the
simulation engine operates on. This module has no database or framework
dependencies — it is pure Python so the simulation layer can be tested
and reasoned about independently of infrastructure.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from datetime import datetime

# ---------------------------------------------------------------------------
# Enumerations
# ---------------------------------------------------------------------------

class MeasurementFramework(Enum):
    """Parallel accounting units for simulation outputs.

    No conversion rates exist between frameworks. Outputs are displayed
    simultaneously — a single aggregate score that hides a catastrophic
    failure in one dimension is architecturally prohibited.
    """
    FINANCIAL = "financial"
    HUMAN_DEVELOPMENT = "human_development"
    ECOLOGICAL = "ecological"
    GOVERNANCE = "governance"


class ResolutionLevel(Enum):
    """Hierarchical resolution levels from the architecture.

    Variable resolution is a first-class feature, not a future enhancement.
    Run Level 1 globally; activate higher levels for specific entities
    when the question demands finer granularity.
    """
    NATION_STATE = 1         # foundational, always active
    SUBNATIONAL = 2          # activated per scenario requirement
    URBAN_RURAL = 3          # urban/rural sector distinction within regions
    DEMOGRAPHIC_COHORT = 4   # income quintiles × age bands × employment sector
    INSTITUTIONAL = 5        # key actors: central bank, finance ministry, military
    INDIVIDUAL = 6           # archetypes — future Agent-Based Modeling territory


# ---------------------------------------------------------------------------
# Supporting structures
# ---------------------------------------------------------------------------

@dataclass
class Geometry:
    """Spatial reference for a simulation entity.

    Holds GeoJSON-compatible geometry data. The simulation engine treats
    this as an opaque data holder. PostGIS integration is introduced in
    Milestone 2 — keeping it decoupled here avoids tying the simulation
    layer to the database layer during Milestone 1.
    """
    geometry_type: str    # 'Point', 'Polygon', 'MultiPolygon'
    coordinates: Any      # GeoJSON coordinates structure
    crs: str = "EPSG:4326"


@dataclass
class ResolutionConfig:
    """Which resolution levels are active for a simulation run.

    entity_overrides maps entity_id to a resolution level that applies
    to that entity and its subtree, overriding global_level.

    Example: Level 1 globally, Level 2 for Middle East entities,
    Level 3 for Saudi Arabia specifically.
    """
    global_level: ResolutionLevel = ResolutionLevel.NATION_STATE
    entity_overrides: dict[str, ResolutionLevel] = field(default_factory=dict)

    def level_for(self, entity_id: str) -> ResolutionLevel:
        """Return the effective resolution level for an entity."""
        return self.entity_overrides.get(entity_id, self.global_level)


@dataclass
class ScenarioConfig:
    """Configuration for a simulation scenario run."""
    scenario_id: str
    name: str
    description: str
    start_date: datetime
    end_date: datetime
    # entity_id -> {attribute_key -> override_value}
    initial_overrides: dict[str, dict[str, float]] = field(default_factory=dict)
    # user-defined weighting across measurement frameworks
    # keys are MeasurementFramework values; values sum to 1.0 by convention
    framework_weights: dict[str, float] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class PropagationRule:
    """How an event propagates along relationships in the graph.

    relationship_type restricts propagation to edges of that type.
    attenuation_factor determines how much effect diminishes per hop —
    0.0 means no propagation, 1.0 means no attenuation.
    max_hops limits propagation depth.
    """
    relationship_type: str   # which edge types carry this event
    attenuation_factor: float  # effect multiplier per hop, in [0.0, 1.0]
    max_hops: int = 1


# ---------------------------------------------------------------------------
# Core entities
# ---------------------------------------------------------------------------

@dataclass
class SimulationEntity:
    """Base for all entities in the simulation graph.

    Countries, subnational regions, and institutions all use this class.
    The event propagation engine operates uniformly on all entity types —
    entity_type drives module selection, not branching in the engine itself.

    attributes holds current simulation state variables as floats.
    metadata holds non-simulation data (display names, ISO codes, etc.)
    that does not participate in calculations.
    """
    id: str
    entity_type: str                      # 'country', 'region', 'institution'
    attributes: dict[str, float]          # current state variables
    metadata: dict[str, Any]             # non-simulation data
    parent_id: str | None = None      # enclosing entity for hierarchical resolution
    geometry: Geometry | None = None  # spatial reference, populated in Milestone 2

    def get_attribute(self, key: str, default: float = 0.0) -> float:
        """Return an attribute value, or default if not present."""
        return self.attributes.get(key, default)

    def set_attribute(self, key: str, value: float) -> None:
        """Set an attribute to an absolute value."""
        self.attributes[key] = value

    def apply_delta(self, key: str, delta: float) -> None:
        """Apply an additive change to an attribute.

        Initialises the attribute to 0.0 before applying delta if the
        key is not yet present, rather than raising KeyError.
        """
        self.attributes[key] = self.attributes.get(key, 0.0) + delta


@dataclass
class Relationship:
    """Directed relationship between two simulation entities.

    Relationships are the edges in the simulation graph. weight encodes
    how strongly events originating at source_id affect target_id when
    they propagate along this edge.
    """
    source_id: str
    target_id: str
    relationship_type: str               # 'trade', 'debt', 'alliance', 'currency'
    weight: float                        # propagation strength, in [0.0, 1.0]
    attributes: dict[str, float] = field(default_factory=dict)


@dataclass
class Event:
    """An event that propagates through the simulation graph each timestep.

    Events are the mechanism by which modules communicate state changes.
    affected_attributes maps attribute keys to delta values — additive
    changes to be applied to any entity that receives this event.

    propagation_rules determine how far and along which relationship
    types the event travels beyond the source entity.

    framework tags which measurement dimension this event belongs to,
    enabling parallel accounting without conversion between frameworks.
    """
    event_id: str
    source_entity_id: str
    event_type: str                          # 'policy_change', 'shock', 'threshold_crossed'
    affected_attributes: dict[str, float]    # attribute key -> delta
    propagation_rules: list[PropagationRule]
    timestep_originated: datetime
    framework: MeasurementFramework = MeasurementFramework.FINANCIAL
    metadata: dict[str, Any] = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Simulation state
# ---------------------------------------------------------------------------

@dataclass
class SimulationState:
    """Complete state of the simulation at a single timestep.

    Passed read-only to every module on each tick. Modules must not
    mutate state directly — all state changes are expressed as Events
    returned from SimulationModule.compute(). The engine applies events
    to produce the next state.
    """
    timestep: datetime
    resolution: ResolutionConfig
    entities: dict[str, SimulationEntity]
    relationships: list[Relationship]
    events: list[Event]
    scenario_config: ScenarioConfig

    def get_entity(self, entity_id: str) -> SimulationEntity | None:
        """Return an entity by id, or None if not present."""
        return self.entities.get(entity_id)

    def get_relationships_from(self, entity_id: str) -> list[Relationship]:
        """Return all outbound relationships from entity_id."""
        return [r for r in self.relationships if r.source_id == entity_id]

    def get_relationships_to(self, entity_id: str) -> list[Relationship]:
        """Return all inbound relationships to entity_id."""
        return [r for r in self.relationships if r.target_id == entity_id]

    def get_events_for_entity(self, entity_id: str) -> list[Event]:
        """Return all events that originated from entity_id this timestep."""
        return [e for e in self.events if e.source_entity_id == entity_id]


# ---------------------------------------------------------------------------
# Module interface
# ---------------------------------------------------------------------------

class SimulationModule(ABC):
    """Abstract base class for all simulation modules.

    Every module (Macroeconomic, Geopolitical, Trade, Climate, etc.)
    implements this interface. Modules register with the engine at startup.
    The engine calls compute() for each entity each timestep and collects
    the resulting Events for propagation.

    Contract:
    - Modules MUST NOT mutate SimulationState.
    - All state changes are expressed as returned Events.
    - compute() is called once per entity per timestep.
    - The engine routes incoming events to modules via get_subscribed_events().
    """

    @abstractmethod
    def compute(
        self,
        entity: SimulationEntity,
        state: SimulationState,
        timestep: datetime,
    ) -> list[Event]:
        """Compute this module's contribution for one entity at one timestep.

        Args:
            entity: The entity being computed. Read the entity's current
                    attributes to inform calculations.
            state:  Full simulation state. Read-only. Use state query
                    methods to access relationships and other entities.
            timestep: Current simulation time.

        Returns:
            List of Events to propagate this timestep. Return an empty
            list if this entity produces no state changes this tick.
        """

    @abstractmethod
    def get_subscribed_events(self) -> list[str]:
        """Return the event types this module reacts to.

        The engine uses this to route incoming events to the correct
        modules. Return an empty list if this module generates events
        from its own equations independently rather than reacting to
        incoming events from other modules.
        """
