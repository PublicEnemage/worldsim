"""
Simulation core data model — ADR-001, Amendments 1 and 2; ADR-011.

All entities, relationships, events, and measurement structures that the
simulation engine operates on. This module has no database or framework
dependencies — it is pure Python so the simulation layer can be tested
and reasoned about independently of infrastructure.

Amendment 1 (SCR-001): SimulationEntity.attributes changed from
dict[str, float] to dict[str, Quantity]. Event.affected_attributes
changed from dict[str, float] to dict[str, Quantity]. See ADR-001
Amendment 1 for the full renewal record.

Amendment 2 (Issue #28, Issue #30): CohortProfile type added for income-
quintile-level disaggregation. SimulationEntity gains optional
cohort_profiles field (None at Level 1, populated at Level 4+). AttributeType
enum added to quantity.py for economic-semantic classification. See ADR-001
Amendment 2 for the full record.

ADR-011: PropagationMode enum added. PropagationRule extended with
propagation_mode, threshold, and ceiling fields. LINEAR remains the
default — backward compatibility is preserved for all existing callers.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from decimal import Decimal
from enum import Enum
from typing import TYPE_CHECKING, Any

from app.simulation.engine.quantity import Quantity, VariableType

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


class PropagationMode(str, Enum):
    """How an event propagates through the relationship graph (ADR-011).

    LINEAR   — existing linear diffusion: delta × attenuation_factor × weight
               per hop. Appropriate for slow-moving structural shocks.
    THRESHOLD — applies delta only if the computed effect at a target entity
               exceeds the PropagationRule.threshold floor. Models tipping-point
               dynamics where small shocks are absorbed without effect.
    CASCADE  — amplifies delta at each hop using 1/attenuation_factor × weight
               instead of decaying it, capped at PropagationRule.ceiling times
               the base delta magnitude. Models self-reinforcing panics and
               bank-run contagion (Lebanon 2019, Northern Rock 2007).

    LINEAR is the default for all existing PropagationRule instances to preserve
    backward compatibility — callers that do not set propagation_mode receive
    unchanged behaviour.
    """
    LINEAR = "linear"
    THRESHOLD = "threshold"
    CASCADE = "cascade"


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

    Attributes:
        geometry_type: GeoJSON geometry primitive — 'Point', 'Polygon', or
            'MultiPolygon'.
        coordinates: GeoJSON coordinates structure. Treated as opaque by the
            engine; PostGIS consumes it in Milestone 2.
        crs: Coordinate reference system identifier. Defaults to WGS-84
            (EPSG:4326).
    """
    geometry_type: str
    coordinates: Any
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
        """Return the effective resolution level for an entity.

        Args:
            entity_id: The entity to look up.

        Returns:
            Entity-specific override if one is set, otherwise global_level.
        """
        return self.entity_overrides.get(entity_id, self.global_level)


@dataclass
class ScenarioConfig:
    """Configuration for a simulation scenario run.

    Attributes:
        scenario_id: Unique identifier for this scenario.
        name: Human-readable display name.
        description: Free-text description of the scenario.
        start_date: First timestep of the simulation run.
        end_date: Last timestep of the simulation run.
        initial_overrides: Per-entity attribute overrides applied before the
            first step. Maps entity_id → {attribute_key → override_value}.
        framework_weights: User-defined weighting across measurement frameworks.
            Keys are MeasurementFramework values; values sum to 1.0 by convention.
        metadata: Arbitrary scenario-level metadata (display tags, authorship,
            etc.) that does not participate in calculations.
    """
    scenario_id: str
    name: str
    description: str
    start_date: datetime
    end_date: datetime
    initial_overrides: dict[str, dict[str, float]] = field(default_factory=dict)
    framework_weights: dict[str, float] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class PropagationRule:
    """How an event propagates along relationships in the graph (ADR-011).

    relationship_type restricts propagation to edges of that type.
    attenuation_factor determines how much effect changes per hop:
      LINEAR mode   — decay: multiplied by attenuation_factor * weight per hop.
                      0.0 means no propagation, 1.0 means no decay.
      THRESHOLD mode — same per-hop decay as LINEAR; but the computed delta at
                      a target is only accumulated if its max |value| across all
                      affected attributes meets or exceeds `threshold`.
      CASCADE mode  — amplification: multiplied by (1/attenuation_factor) * weight
                      per hop (inverse of LINEAR), capped so that no attribute's
                      accumulated |delta| exceeds `ceiling` × |base delta|.

    propagation_mode defaults to LINEAR — all existing callers retain identical
    behaviour without modification.

    threshold: THRESHOLD mode only. Minimum |delta| (across any single attribute)
      required to apply the computed effect to the target entity. Defaults to 0.0
      (no threshold — equivalent to LINEAR for tipping-point logic).

    ceiling: CASCADE mode only. Maximum amplification factor relative to the base
      delta magnitude per attribute. Defaults to 1.0 (no amplification beyond base).
      Set > 1.0 to allow cascade amplification; e.g. 3.0 caps at 3× base magnitude.

    Attributes:
        relationship_type: Edge type that carries this event (e.g. 'trade', 'debt').
        attenuation_factor: Per-hop scale factor in [0.0, 1.0].
        max_hops: Maximum number of hops the event may travel. Defaults to 1.
        propagation_mode: LINEAR (decay), THRESHOLD (conditional decay), or
            CASCADE (amplification). Defaults to LINEAR.
        threshold: THRESHOLD mode only — minimum |delta| per attribute required
            to apply the effect at a target entity. Defaults to 0.0.
        ceiling: CASCADE mode only — maximum amplification relative to base delta
            magnitude. Defaults to 1.0 (no amplification).
    """
    relationship_type: str
    attenuation_factor: float
    max_hops: int = 1
    propagation_mode: PropagationMode = PropagationMode.LINEAR
    threshold: float = 0.0
    ceiling: float = 1.0


# ---------------------------------------------------------------------------
# Debt structure (Issue #36 — Intergenerational Advocate ARCH-REVIEW-001)
# ---------------------------------------------------------------------------


@dataclass
class DebtProfile:
    """Structured debt composition for an entity.

    Captures six dimensions that determine vulnerability profile beyond the
    simple debt/GDP ratio. Japan at 253% (yen-denominated, domestically held)
    and Vietnam at 37% (with significant foreign-currency components) have
    entirely different crisis dynamics — this dataclass makes that distinction
    computable.

    All fields are fractions (0.0 to 1.0) except where noted.

    Attributes:
        total_pct_gdp: Total public debt as fraction of GDP (e.g. 0.85 = 85%).
        foreign_currency_pct: Share of debt denominated in foreign currency.
            The 'original sin' dimension — foreign-currency debt cannot be
            inflated away and creates acute rollover risk under FX pressure.
            MDA threshold: > 0.60 flags elevated rollover risk.
        short_term_pct: Share of debt maturing within 12 months. Measures
            rollover cliff risk.
        domestic_holder_pct: Share held by domestic investors (banks,
            pension funds, central bank). Higher = less vulnerable to
            foreign capital exit.
        multilateral_pct: Share owed to multilateral creditors (IMF, World
            Bank, regional MDBs). Distinct restructuring dynamics — preferred
            creditor status limits haircut exposure.
        interest_service_pct_revenue: Debt service as fraction of government
            revenue. The fiscal sustainability measure — stock matters less
            than the income it consumes.
    """

    total_pct_gdp: Decimal
    foreign_currency_pct: Decimal
    short_term_pct: Decimal
    domestic_holder_pct: Decimal
    multilateral_pct: Decimal
    interest_service_pct_revenue: Decimal

    # Threshold at which foreign_currency_pct triggers MDA elevated rollover risk
    FOREIGN_CURRENCY_MDA_THRESHOLD: Decimal = field(
        default=Decimal("0.60"), init=False, repr=False, compare=False
    )

    def is_elevated_rollover_risk(self) -> bool:
        """Return True if foreign currency debt share exceeds MDA threshold."""
        return self.foreign_currency_pct > self.FOREIGN_CURRENCY_MDA_THRESHOLD


# ---------------------------------------------------------------------------
# Cohort disaggregation — ADR-001 Amendment 2, Issue #28
# ---------------------------------------------------------------------------


@dataclass
class CohortProfile:
    """Income-quintile or age-band level attribute container for one entity cohort.

    CohortProfile is the Level 4 sub-entity structure — it holds Quantity
    attributes measured at the cohort level rather than the national aggregate.
    The parent SimulationEntity holds national aggregates in its attributes dict;
    CohortProfile holds the disaggregated view for one cohort segment.

    Key convention (ADR-001 Amendment 2):
        Income quintiles: "Q1" (bottom 20%) through "Q5" (top 20%).
        Age bands: "youth_15_24", "prime_25_54", "older_55_64", "senior_65plus".
        Combined: compound keys are not used at Level 4 stub — use a single
        dimension per profile key for legibility.

    confidence_tier inheritance rule (ADR-001 Amendment 2):
        Each Quantity in attributes carries its own confidence_tier, sourced
        from the cohort-level data directly (not inherited from the parent
        entity's aggregate tier). Eurostat EU-SILC cohort data is Tier 2;
        synthetic cohort estimates are Tier 4.

    Attributes:
        attributes: Cohort-level simulation state variables as Quantity instances.
            Same structure as SimulationEntity.attributes — attribute key maps to
            a typed Quantity carrying value, unit, variable_type, and provenance.
    """

    attributes: dict[str, Quantity]


# ---------------------------------------------------------------------------
# Core entities
# ---------------------------------------------------------------------------

@dataclass
class SimulationEntity:
    """Base for all entities in the simulation graph.

    Countries, subnational regions, and institutions all use this class.
    The event propagation engine operates uniformly on all entity types —
    entity_type drives module selection, not branching in the engine itself.

    attributes holds current simulation state variables as Quantity instances.
    Every attribute value carries its unit, variable type, confidence tier,
    and provenance. Use get_attribute() to retrieve the typed Quantity;
    use get_attribute_value() for numeric comparisons.

    metadata holds non-simulation data (display names, ISO codes, etc.)
    that does not participate in calculations.

    Amendment 1 (SCR-001): attributes changed from dict[str, float] to
    dict[str, Quantity].

    Attributes:
        id: Unique entity identifier (ISO 3166-1 alpha-3 for country entities).
        entity_type: Entity class — 'country', 'region', or 'institution'.
        attributes: Current simulation state variables as Quantity instances.
            Every attribute carries its unit, variable type, confidence tier,
            and provenance. Use get_attribute() to retrieve typed Quantities.
        metadata: Non-simulation data (display names, ISO codes, etc.) that
            does not participate in calculations.
        parent_id: Enclosing entity for hierarchical resolution; None for
            top-level entities.
        geometry: Spatial reference for the entity; populated in Milestone 2.
        debt_profile: Structured debt composition (Issue #36). Exposes six
            debt-structure dimensions via the get_attribute() namespace.
        cohort_profiles: Income-quintile and age-band level attribute containers
            (ADR-001 Amendment 2, Issue #28). None at Level 1 (national aggregate);
            populated at Level 4+ when cohort-level data is available. Keys follow
            the convention "Q1"–"Q5" for income quintiles, "youth_15_24" for age
            bands. Stored in state_data JSONB under "_cohort_profiles" sub-key.
    """
    id: str
    entity_type: str
    attributes: dict[str, Quantity]
    metadata: dict[str, Any]
    parent_id: str | None = None
    geometry: Geometry | None = None
    debt_profile: DebtProfile | None = None
    cohort_profiles: dict[str, CohortProfile] | None = None

    # Mapping from debt_profile.* attribute keys to DebtProfile field names.
    # Used by get_attribute() to expose debt structure as Quantity attributes
    # for MDA threshold evaluation without duplicating storage.
    _DEBT_PROFILE_ATTR_MAP: dict[str, str] = field(
        default_factory=lambda: {
            "debt_profile.total_pct_gdp": "total_pct_gdp",
            "debt_profile.foreign_currency_pct": "foreign_currency_pct",
            "debt_profile.short_term_pct": "short_term_pct",
            "debt_profile.domestic_holder_pct": "domestic_holder_pct",
            "debt_profile.multilateral_pct": "multilateral_pct",
            "debt_profile.interest_service_pct_revenue": "interest_service_pct_revenue",
        },
        init=False,
        repr=False,
        compare=False,
    )

    def get_attribute(self, key: str) -> Quantity | None:
        """Return an attribute Quantity, or None if not present.

        Supports two key namespaces:
          - Direct entity attributes: keys in self.attributes.
          - Debt profile sub-keys: `"debt_profile.<field>"` keys expose
            DebtProfile fields as RATIO Quantities when debt_profile is set.
            This allows MDA thresholds to evaluate debt structure via the
            same indicator_key mechanism used for all other thresholds.

        Args:
            key: Attribute key to look up.

        Returns:
            Quantity for the key, or None if the key is absent.
            Use get_attribute_value() for numeric comparison operations.
        """
        if key in self._DEBT_PROFILE_ATTR_MAP and self.debt_profile is not None:
            field_name = self._DEBT_PROFILE_ATTR_MAP[key]
            value = getattr(self.debt_profile, field_name)
            return Quantity(
                value=value,
                unit="ratio",
                variable_type=VariableType.RATIO,
                confidence_tier=2,
            )
        return self.attributes.get(key)

    def get_attribute_value(self, key: str, default: Decimal = Decimal("0")) -> Decimal:
        """Return the numeric value of an attribute, or default if not present.

        Preferred for numeric comparisons (StateCondition.is_met, test assertions).
        Returns Decimal, which is comparable to float via standard Python
        arithmetic and pytest.approx.
        """
        q = self.get_attribute(key)
        if q is None:
            return default
        return q.value

    def set_attribute(self, key: str, value: Quantity) -> None:
        """Set an attribute to an absolute Quantity value.

        Args:
            key: Attribute key to set.
            value: Quantity to store; replaces any existing value for the key.
        """
        self.attributes[key] = value

    def apply_delta(self, key: str, delta: Quantity) -> None:
        """Apply a change to an attribute.

        For STOCK variables: replaces the current value with delta
        (delta carries the new absolute level, not an additive change).

        For FLOW, RATIO, DIMENSIONLESS variables: adds delta.value to the
        existing attribute value. Initialises the attribute from the delta
        if the key is not yet present.

        Args:
            key: Attribute key to update.
            delta: The Quantity delta to apply. For STOCK, this is the new
                absolute value. For FLOW/RATIO/DIMENSIONLESS, this is the
                additive increment.
        """
        if delta.variable_type == VariableType.STOCK:
            self.attributes[key] = delta
        else:
            existing = self.attributes.get(key)
            if existing is None:
                self.attributes[key] = delta
            else:
                self.attributes[key] = Quantity(
                    value=existing.value + delta.value,
                    unit=existing.unit,
                    variable_type=existing.variable_type,
                    measurement_framework=existing.measurement_framework,
                    observation_date=existing.observation_date or delta.observation_date,
                    source_id=existing.source_id,
                    confidence_tier=max(existing.confidence_tier, delta.confidence_tier),
                )


@dataclass
class Relationship:
    """Directed relationship between two simulation entities.

    Relationships are the edges in the simulation graph. weight encodes
    how strongly events originating at source_id affect target_id when
    they propagate along this edge.

    weight is a dimensionless propagation coefficient; it intentionally
    remains float (NumPy-compatible for matrix operations on relationship
    weight graphs). See ARCH-4 in SCR-001 for the rationale.
    attributes uses dict[str, Any] to accommodate mixed relationship data
    (Quantity values and float propagation coefficients).

    Attributes:
        source_id: ID of the originating entity.
        target_id: ID of the receiving entity.
        relationship_type: Edge type — 'trade', 'debt', 'alliance', or 'currency'.
        weight: Propagation strength in [0.0, 1.0]. Remains float for
            NumPy-compatible matrix operations (ARCH-4 in SCR-001).
        attributes: Mixed relationship data (Quantity values and float
            propagation coefficients).
    """
    source_id: str
    target_id: str
    relationship_type: str
    weight: float
    attributes: dict[str, Any] = field(default_factory=dict)


@dataclass
class Event:
    """An event that propagates through the simulation graph each timestep.

    Events are the mechanism by which modules communicate state changes.
    affected_attributes maps attribute keys to Quantity delta values —
    typed changes to be applied to any entity that receives this event.

    propagation_rules determine how far and along which relationship
    types the event travels beyond the source entity.

    framework tags which measurement dimension this event belongs to,
    enabling parallel accounting without conversion between frameworks.

    Amendment 1 (SCR-001): affected_attributes changed from dict[str, float]
    to dict[str, Quantity].

    Attributes:
        event_id: Unique identifier for this event instance.
        source_entity_id: ID of the entity that originated the event.
        event_type: Event class — 'policy_change', 'shock', or
            'threshold_crossed'.
        affected_attributes: Map of attribute key → Quantity delta. Each entry
            is a typed change to be applied to receiving entities.
        propagation_rules: Determines how far and along which relationship types
            the event travels beyond the source entity.
        timestep_originated: Simulation timestep at which this event was generated.
        framework: Measurement dimension this event belongs to (financial,
            human_development, ecological, governance).
        metadata: Arbitrary event metadata for diagnostics and audit trail.
    """
    event_id: str
    source_entity_id: str
    event_type: str
    affected_attributes: dict[str, Quantity]
    propagation_rules: list[PropagationRule]
    timestep_originated: datetime
    framework: MeasurementFramework
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
