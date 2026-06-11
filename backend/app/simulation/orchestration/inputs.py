"""
Control input types for the Input Orchestration Layer — ADR-002, Amendment 1.
Political economy extensions: Issue #96 (CONDITIONALITY InputSource),
Issue #93 (implementation_capacity), Issue #157 (CompoundStateCondition).
Issue #31 (multi-step duration_periods + decay_function on ControlInput base).
Issue #33 (CapitalFlowInput, DFICommitmentInput, ActorType enum).

ControlInput is the abstract base class for all exogenous inputs injected
into the simulation. Each concrete subclass represents one category of
policy instrument. Every ControlInput translates itself to one or more
Events for the propagation engine via to_events().

The endogenous/exogenous distinction is architecturally enforced here:
module-generated events flow through SimulationModule.compute(); all
human-authorised policy decisions flow through ControlInput subclasses
and the InputOrchestrator.inject() method.

Amendment 1 (SCR-001 / ADR-002 Amendment 1):
- MonetaryPolicyInput replaced by MonetaryRateInput (rate instruments:
  POLICY_RATE, RESERVE_REQUIREMENT) and MonetaryVolumeInput (volume
  instruments: ASSET_PURCHASE, EXCHANGE_RATE_INTERVENTION).
- MonetaryInstrument split into MonetaryRateInstrument and
  MonetaryVolumeInstrument correspondingly.
- All to_events() implementations produce Quantity deltas in
  affected_attributes (dict[str, Quantity]), not float deltas.

Political economy extensions (Issue #96, #93, #157):
- InputSource.CONDITIONALITY encodes externally coerced decisions.
- ControlInput.implementation_capacity scales event magnitudes to model
  partial implementation, political feasibility constraints.
- CompoundStateCondition enables AND/OR multi-attribute trigger logic.
"""

from __future__ import annotations

import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass, field, replace
from decimal import Decimal
from enum import Enum
from typing import TYPE_CHECKING, Any

from app.simulation.engine.quantity import MonetaryValue, Quantity, VariableType

if TYPE_CHECKING:
    from datetime import datetime

    from app.simulation.engine.models import Event, PropagationRule, SimulationState


# ---------------------------------------------------------------------------
# Enumerations
# ---------------------------------------------------------------------------


class ActorType(Enum):
    """Type of actor authorising a ControlInput (Issue #33).

    Extends the actor model beyond government and central bank actors to
    include private capital, development finance, and sovereign investment
    — the primary channels through which capital flows into and out of
    developing economies.
    """

    GOVERNMENT = "government"
    CENTRAL_BANK = "central_bank"
    PRIVATE_INVESTOR = "private_investor"
    DFI = "dfi"
    SOVEREIGN_INVESTOR = "sovereign_investor"
    MULTILATERAL = "multilateral"


class CapitalFlowType(Enum):
    """Category of private capital flow for CapitalFlowInput (Issue #33)."""

    FDI = "fdi"
    PORTFOLIO_INVESTMENT = "portfolio_investment"
    SOVEREIGN_DEBT = "sovereign_debt"
    REMITTANCE = "remittance"


class DFIInstrumentType(Enum):
    """Development Finance Institution instrument types (Issue #33)."""

    GUARANTEE = "guarantee"
    EQUITY_INVESTMENT = "equity_investment"
    TECHNICAL_ASSISTANCE = "technical_assistance"
    CONCESSIONAL_LOAN = "concessional_loan"
    MDB_BUDGET_SUPPORT = "mdb_budget_support"


class InputSource(Enum):
    """The channel through which a ControlInput entered the simulation.

    Recorded in every ControlInputAuditRecord so the provenance of every
    exogenous decision is traceable to its source channel.

    CONDITIONALITY (Issue #96): the decision was made under binding external
    constraint imposed by another actor (IMF, ECB, creditor bloc). Distinguished
    from SCENARIO_SCRIPT to record that the policy was not freely chosen.
    Use constraining_actor_id and constraint_mechanism on the ControlInput to
    record who imposed the constraint and by what mechanism.
    """

    UI = "ui"
    API = "api"
    CLI = "cli"
    BULK_FEED = "bulk_feed"
    SCENARIO_SCRIPT = "scenario_script"
    CONTINGENT_TRIGGER = "contingent_trigger"
    CONDITIONALITY = "conditionality"


class MonetaryRateInstrument(Enum):
    """Rate-based monetary policy instruments.

    These instruments adjust dimensionless rates or fractions. value is
    always a Decimal fraction (e.g. 0.005 for a 50 basis point change).
    Use MonetaryRateInput to carry these.
    """

    POLICY_RATE = "policy_rate"
    RESERVE_REQUIREMENT = "reserve_requirement"


class MonetaryVolumeInstrument(Enum):
    """Volume-based monetary policy instruments.

    These instruments specify a monetary volume (an asset purchase amount
    or intervention size). value is a MonetaryValue in canonical units.
    Use MonetaryVolumeInput to carry these.
    """

    ASSET_PURCHASE = "asset_purchase"
    EXCHANGE_RATE_INTERVENTION = "exchange_rate_intervention"


class FiscalInstrument(Enum):
    """Fiscal policy instruments available to a finance ministry."""

    SPENDING_CHANGE = "spending_change"
    TAX_RATE_CHANGE = "tax_rate_change"
    DEFICIT_TARGET = "deficit_target"
    DEBT_ISSUANCE = "debt_issuance"


class CommodityCategory(Enum):
    """Commodity categories for external sector shocks (ADR-012, Issue #751/#752)."""

    FUEL = "fuel"
    FOOD = "food"
    METALS = "metals"
    OTHER = "other"


class TradeInstrument(Enum):
    """Trade policy instruments affecting cross-border flows."""

    TARIFF_RATE = "tariff_rate"
    TRADE_AGREEMENT = "trade_agreement"
    SANCTIONS = "sanctions"
    EXPORT_CONTROL = "export_control"
    CURRENCY_SWAP = "currency_swap"


class EmergencyInstrument(Enum):
    """Emergency policy instruments invoked under crisis conditions.

    These represent responses outside normal policy parameters — the
    simulation's equivalent of emergency aircraft procedures. They are
    typically irreversible or carry structural costs.
    """

    CAPITAL_CONTROLS = "capital_controls"
    BANK_HOLIDAY = "bank_holiday"
    DEBT_MORATORIUM = "debt_moratorium"
    NATIONALIZATION = "nationalization"
    IMF_PROGRAM_ACCEPTANCE = "imf_program_acceptance"
    DEFAULT_DECLARATION = "default_declaration"
    EMERGENCY_DECLARATION = "emergency_declaration"


class StructuralInstrument(Enum):
    """Structural policy instruments with long implementation horizons.

    These change the economy's underlying architecture rather than its
    cyclical position. Effects phase in over implementation_years.
    """

    PRIVATIZATION = "privatization"
    NATIONALIZATION = "nationalization"
    REGULATORY_CHANGE = "regulatory_change"
    CONSTITUTIONAL_CHANGE = "constitutional_change"
    INSTITUTIONAL_REFORM = "institutional_reform"


class ComparisonOperator(Enum):
    """Comparison operators for StateCondition evaluation."""

    LT = "<"
    GT = ">"
    LTE = "<="
    GTE = ">="
    EQ = "=="


class LogicalOperator(Enum):
    """Logical operators for CompoundStateCondition evaluation (Issue #157)."""

    AND = "and"
    OR = "or"


# ---------------------------------------------------------------------------
# Control input base class
# ---------------------------------------------------------------------------


@dataclass(kw_only=True)
class ControlInput(ABC):
    """Abstract base class for all exogenous inputs to the simulation.

    ControlInputs represent human decisions injected into the simulation
    from outside the model's own logic. Unlike module-generated events
    (endogenous — computed from internal state equations), ControlInputs
    are exogenous: they are injected regardless of what modules would
    compute on their own.

    Both paths produce Events that the propagation engine applies. The
    distinction is enforced architecturally so that every exogenous decision
    is auditable and scenarios are reproducible by replaying their audit logs.

    Attributes:
        input_id: Unique identifier for this input instance.
        actor_id: Identifier of the actor authorising this input.
        actor_role: Role of the actor (e.g. 'finance_minister', 'central_bank').
        target_entity: Entity ID that is the primary target of this input.
        effective_date: When this input takes effect in simulation time.
        justification: Human-readable rationale for this decision.
        source: Channel through which this input entered the simulation.
        timestamp: Wall-clock time when this input was created.
        propagation_rules: Rules governing how generated Events propagate
            through the relationship graph. Empty list means the effect
            applies only to the source entity with no graph propagation.
        implementation_capacity: Political feasibility multiplier in [0.0, 1.0]
            (Issue #93). Scales event magnitudes from to_events() to model partial
            implementation, political constraints, and watered-down execution.
            Default 1.0 preserves existing behaviour — full implementation.
            0.5 means 50% of the intended policy magnitude is actually transmitted.
        constraining_actor_id: For InputSource.CONDITIONALITY — the external actor
            that imposed the constraint (e.g. 'IMF', 'ECB', 'US_TREASURY').
            Empty string for freely chosen decisions (Issue #96).
        constraint_mechanism: For InputSource.CONDITIONALITY — how the constraint
            was applied (e.g. 'ELA_WITHDRAWAL_THREAT', 'DISBURSEMENT_SUSPENSION',
            'SANCTIONS'). Empty string for non-conditionality inputs (Issue #96).
        duration_periods: Number of simulation timesteps this input remains active
            (Issue #31). Default 1 (one-shot). Values > 1 cause the orchestrator
            to re-inject the input for the subsequent `duration_periods - 1` steps.
            The ScenarioRunner expands multi-duration inputs at run() time;
            the WebScenarioRunner requires duration rows pre-created in
            scenario_scheduled_inputs.
        decay_function: How the effect magnitude changes across duration_periods
            (Issue #31). One of:
              "constant"           — same magnitude every period (default)
              "linear_decay"       — linearly decreasing: scale = 1 - (p-1)/n
              "exponential_decay"  — halves each period: scale = 0.5^(p-1)
            Ignored when duration_periods == 1.
        actor_type: Structured actor category from ActorType enum (Issue #33).
            Complements the free-text actor_role field.
    """

    input_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    actor_id: str = ""
    actor_role: str = ""
    actor_type: ActorType | None = None
    target_entity: str = ""
    effective_date: datetime = field(default=None)  # type: ignore[assignment]
    justification: str = ""
    source: InputSource = InputSource.SCENARIO_SCRIPT
    timestamp: datetime = field(default=None)  # type: ignore[assignment]
    propagation_rules: list[PropagationRule] = field(default_factory=list)
    implementation_capacity: Decimal = Decimal("1.0")
    constraining_actor_id: str = ""
    constraint_mechanism: str = ""
    duration_periods: int = 1
    decay_function: str = "constant"

    @abstractmethod
    def to_events(self, timestep: datetime) -> list[Event]:
        """Translate this control input into simulation Events.

        The InputOrchestrator calls this during inject() to convert the
        policy decision into Events the propagation engine can apply.
        Subclasses must implement this method — do not call it directly;
        use get_events() to benefit from implementation_capacity scaling.

        Args:
            timestep: Current simulation timestep at which the input fires.

        Returns:
            List of Events representing this input's effect on simulation state.
            May return multiple Events (e.g. TradePolicyInput with retaliation).
        """

    def get_events(self, timestep: datetime) -> list[Event]:
        """Return scaled events for this control input (Issue #93).

        Calls to_events() and multiplies every affected_attributes Quantity
        value by implementation_capacity. This models partial implementation,
        political feasibility constraints, and watered-down policy execution.

        implementation_capacity=1.0 (default) returns events unchanged.
        implementation_capacity=0.5 halves all event magnitudes.
        implementation_capacity=0.0 produces zero-magnitude events (no effect).

        Args:
            timestep: Current simulation timestep at which the input fires.

        Returns:
            Events with magnitudes scaled by implementation_capacity.
        """
        raw_events = self.to_events(timestep)
        if self.implementation_capacity == Decimal("1.0"):
            return raw_events
        scale = self.implementation_capacity
        scaled: list[Event] = []
        for evt in raw_events:
            scaled_attrs = {
                k: Quantity(
                    value=q.value * scale,
                    unit=q.unit,
                    variable_type=q.variable_type,
                    measurement_framework=q.measurement_framework,
                    observation_date=q.observation_date,
                    source_id=q.source_id,
                    confidence_tier=q.confidence_tier,
                )
                for k, q in evt.affected_attributes.items()
            }
            scaled.append(replace(evt, affected_attributes=scaled_attrs))
        return scaled


# ---------------------------------------------------------------------------
# Concrete subclasses
# ---------------------------------------------------------------------------


@dataclass(kw_only=True)
class MonetaryRateInput(ControlInput):
    """A central bank rate-based monetary policy action.

    Applies to instruments that adjust dimensionless rates or fractions:
    POLICY_RATE and RESERVE_REQUIREMENT. value is the change as a Decimal
    fraction (e.g. Decimal("0.005") for a 50 basis point increase).

    The generated Event delta is a RATIO Quantity — the rate change is
    dimensionless and accumulates additively on the target attribute.

    Attributes:
        instrument: The rate instrument being adjusted.
        value: Magnitude and direction of the change as a Decimal fraction.
    """

    instrument: MonetaryRateInstrument = MonetaryRateInstrument.POLICY_RATE
    value: Decimal = Decimal("0")

    def to_events(self, timestep: datetime) -> list[Event]:
        """Translate to a monetary rate Event targeting the source entity.

        Args:
            timestep: Simulation timestep at which this input fires.

        Returns:
            Single-element list containing the monetary rate Event.
        """
        from app.simulation.engine.models import Event, MeasurementFramework

        delta = Quantity(
            value=self.value,
            unit="dimensionless",
            variable_type=VariableType.RATIO,
            measurement_framework=MeasurementFramework.FINANCIAL,
            confidence_tier=1,
        )
        return [
            Event(
                event_id=f"{self.input_id}-monetary-0",
                source_entity_id=self.target_entity,
                event_type=f"monetary_policy_{self.instrument.value}",
                affected_attributes={self.instrument.value: delta},
                propagation_rules=self.propagation_rules,
                timestep_originated=timestep,
                framework=MeasurementFramework.FINANCIAL,
                metadata={
                    "control_input_id": self.input_id,
                    "actor_id": self.actor_id,
                    "duration_periods": self.duration_periods,
                },
            )
        ]


@dataclass(kw_only=True)
class MonetaryVolumeInput(ControlInput):
    """A central bank volume-based monetary policy action.

    Applies to instruments that specify a monetary volume:
    ASSET_PURCHASE and EXCHANGE_RATE_INTERVENTION. value is a MonetaryValue
    in canonical units (constant 2015 USD).

    The generated Event delta carries the MonetaryValue directly as the
    Quantity delta — MonetaryValue is a Quantity subclass and carries full
    provenance metadata.

    Attributes:
        instrument: The volume instrument being adjusted.
        value: Monetary volume of the action as a MonetaryValue.
    """

    instrument: MonetaryVolumeInstrument = MonetaryVolumeInstrument.ASSET_PURCHASE
    value: MonetaryValue = field(default=None)  # type: ignore[assignment]

    def to_events(self, timestep: datetime) -> list[Event]:
        """Translate to a monetary volume Event targeting the source entity.

        Args:
            timestep: Simulation timestep at which this input fires.

        Returns:
            Single-element list containing the monetary volume Event.
        """
        from app.simulation.engine.models import Event, MeasurementFramework

        return [
            Event(
                event_id=f"{self.input_id}-monetary-0",
                source_entity_id=self.target_entity,
                event_type=f"monetary_policy_{self.instrument.value}",
                affected_attributes={self.instrument.value: self.value},
                propagation_rules=self.propagation_rules,
                timestep_originated=timestep,
                framework=MeasurementFramework.FINANCIAL,
                metadata={
                    "control_input_id": self.input_id,
                    "actor_id": self.actor_id,
                    "duration_periods": self.duration_periods,
                },
            )
        ]


@dataclass(kw_only=True)
class FiscalPolicyInput(ControlInput):
    """A government fiscal policy action.

    Represents a discrete change to a fiscal instrument, optionally
    targeting a specific economic sector. sector is the affected
    segment ('health', 'infrastructure', 'defence', 'social_transfers',
    etc.). An empty string means economy-wide.

    Attributes:
        instrument: The fiscal instrument being adjusted.
        sector: Economic sector targeted. Empty string means economy-wide.
        value: Magnitude of the change in canonical units. Decimal.
        duration_years: Annual timesteps this input spans.
    """

    instrument: FiscalInstrument = FiscalInstrument.SPENDING_CHANGE
    sector: str = ""
    value: Decimal = Decimal("0")
    duration_years: int = 1

    def to_events(self, timestep: datetime) -> list[Event]:
        """Translate to a fiscal policy Event targeting the source entity.

        The attribute key is sector-qualified when a sector is specified:
        'fiscal_spending_change_health' vs 'fiscal_spending_change'.

        Args:
            timestep: Simulation timestep at which this input fires.

        Returns:
            Single-element list containing the fiscal policy Event.
        """
        from app.simulation.engine.models import Event, MeasurementFramework

        attribute_key = (
            f"fiscal_{self.instrument.value}_{self.sector}"
            if self.sector
            else f"fiscal_{self.instrument.value}"
        )
        delta = Quantity(
            value=self.value,
            unit="dimensionless",
            variable_type=VariableType.FLOW,
            measurement_framework=MeasurementFramework.FINANCIAL,
            confidence_tier=1,
        )
        return [
            Event(
                event_id=f"{self.input_id}-fiscal-0",
                source_entity_id=self.target_entity,
                event_type=f"fiscal_policy_{self.instrument.value}",
                affected_attributes={attribute_key: delta},
                propagation_rules=self.propagation_rules,
                timestep_originated=timestep,
                framework=MeasurementFramework.FINANCIAL,
                metadata={
                    "control_input_id": self.input_id,
                    "actor_id": self.actor_id,
                    "sector": self.sector,
                    "duration_years": self.duration_years,
                },
            )
        ]


@dataclass(kw_only=True)
class TradePolicyInput(ControlInput):
    """A trade or external-sector policy action.

    Represents a discrete change to a bilateral or sector-level trade
    policy instrument. source_entity imposes the policy; target_entity
    (inherited from ControlInput) is the primary counterpart.

    If retaliation_modeled is True, a second Event is generated on
    target_entity representing the counterpart's retaliation. Both events
    carry the same propagation_rules. This is a Milestone 1 simplification:
    a full trade module will model retaliation dynamics endogenously.

    Attributes:
        instrument: The trade policy instrument.
        source_entity: Entity imposing the policy. May differ from
            target_entity (which is the primary counterpart).
        affected_sector: Sector targeted ('goods', 'services', etc.).
        value: Magnitude (tariff rate as fraction, volume, etc.). Decimal.
        retaliation_modeled: Whether to generate a retaliation Event.
    """

    instrument: TradeInstrument = TradeInstrument.TARIFF_RATE
    source_entity: str = ""
    affected_sector: str = ""
    value: Decimal = Decimal("0")
    retaliation_modeled: bool = False

    def to_events(self, timestep: datetime) -> list[Event]:
        """Translate to trade policy Events.

        Produces one primary Event on source_entity. If retaliation_modeled
        is True, adds a second retaliation Event on target_entity with
        negated value (retaliation reduces the initiator's trade).

        Args:
            timestep: Simulation timestep at which this input fires.

        Returns:
            One or two Events depending on retaliation_modeled.
        """
        from app.simulation.engine.models import Event, MeasurementFramework

        attribute_key = (
            f"trade_{self.instrument.value}_{self.affected_sector}"
            if self.affected_sector
            else f"trade_{self.instrument.value}"
        )
        primary_delta = Quantity(
            value=self.value,
            unit="dimensionless",
            variable_type=VariableType.RATIO,
            measurement_framework=MeasurementFramework.FINANCIAL,
            confidence_tier=1,
        )
        events: list[Event] = [
            Event(
                event_id=f"{self.input_id}-trade-0",
                source_entity_id=self.source_entity,
                event_type=f"trade_policy_{self.instrument.value}",
                affected_attributes={attribute_key: primary_delta},
                propagation_rules=self.propagation_rules,
                timestep_originated=timestep,
                framework=MeasurementFramework.FINANCIAL,
                metadata={
                    "control_input_id": self.input_id,
                    "actor_id": self.actor_id,
                    "target_entity": self.target_entity,
                    "affected_sector": self.affected_sector,
                    "retaliation_modeled": self.retaliation_modeled,
                },
            )
        ]
        if self.retaliation_modeled:
            retaliation_delta = Quantity(
                value=-self.value,
                unit="dimensionless",
                variable_type=VariableType.RATIO,
                measurement_framework=MeasurementFramework.FINANCIAL,
                confidence_tier=1,
            )
            events.append(
                Event(
                    event_id=f"{self.input_id}-trade-retaliation-0",
                    source_entity_id=self.target_entity,
                    event_type=f"trade_policy_{self.instrument.value}_retaliation",
                    affected_attributes={attribute_key: retaliation_delta},
                    propagation_rules=self.propagation_rules,
                    timestep_originated=timestep,
                    framework=MeasurementFramework.FINANCIAL,
                    metadata={
                        "control_input_id": self.input_id,
                        "is_retaliation": True,
                        "retaliating_against": self.source_entity,
                    },
                )
            )
        return events


@dataclass(kw_only=True)
class EmergencyPolicyInput(ControlInput):
    """An emergency policy measure invoked under crisis conditions.

    Emergency instruments are the simulation's equivalent of emergency
    descent procedures. They represent responses outside normal parameters,
    typically irreversible or carrying significant structural costs.

    parameters is a dict with instrument-specific keys. All instruments
    accept 'magnitude' (float, default 1.0) which scales the Event delta.
    Additional keys are preserved in Event metadata for domain modules.

    Attributes:
        instrument: The emergency instrument being invoked.
        parameters: Instrument-specific parameters dict.
        expected_duration: Timesteps the emergency measure is expected
            to remain in force.
    """

    instrument: EmergencyInstrument = EmergencyInstrument.CAPITAL_CONTROLS
    parameters: dict[str, Any] = field(default_factory=dict)
    expected_duration: int = 1

    def to_events(self, timestep: datetime) -> list[Event]:
        """Translate to an emergency policy Event on the target entity.

        Args:
            timestep: Simulation timestep at which this input fires.

        Returns:
            Single-element list containing the emergency policy Event.
        """
        from app.simulation.engine.models import Event, MeasurementFramework

        magnitude = self.parameters.get("magnitude", 1.0)
        delta = Quantity(
            value=Decimal(str(magnitude)),
            unit="dimensionless",
            variable_type=VariableType.DIMENSIONLESS,
            measurement_framework=MeasurementFramework.GOVERNANCE,
            confidence_tier=1,
        )
        return [
            Event(
                event_id=f"{self.input_id}-emergency-0",
                source_entity_id=self.target_entity,
                event_type=f"emergency_policy_{self.instrument.value}",
                affected_attributes={self.instrument.value: delta},
                propagation_rules=self.propagation_rules,
                timestep_originated=timestep,
                framework=MeasurementFramework.GOVERNANCE,
                metadata={
                    "control_input_id": self.input_id,
                    "actor_id": self.actor_id,
                    "parameters": self.parameters,
                    "expected_duration": self.expected_duration,
                },
            )
        ]


@dataclass(kw_only=True)
class StructuralPolicyInput(ControlInput):
    """A structural reform or institutional change.

    Structural inputs represent long-horizon changes to the economy's
    underlying architecture. Unlike cyclical inputs, these have long
    implementation periods and path-dependent effects. The
    implementation_years field signals to future domain modules that
    effects should phase in gradually.

    Attributes:
        instrument: The structural instrument.
        affected_sector: Sector undergoing structural change.
        parameters: Instrument-specific parameters. Accepts 'magnitude'
            (float, default 1.0) to scale the generated Event delta.
        implementation_years: Annual timesteps for full implementation.
    """

    instrument: StructuralInstrument = StructuralInstrument.REGULATORY_CHANGE
    affected_sector: str = ""
    parameters: dict[str, Any] = field(default_factory=dict)
    implementation_years: int = 1

    def to_events(self, timestep: datetime) -> list[Event]:
        """Translate to a structural policy Event on the target entity.

        Args:
            timestep: Simulation timestep at which this input fires.

        Returns:
            Single-element list containing the structural policy Event.
        """
        from app.simulation.engine.models import Event, MeasurementFramework

        magnitude = self.parameters.get("magnitude", 1.0)
        delta = Quantity(
            value=Decimal(str(magnitude)),
            unit="dimensionless",
            variable_type=VariableType.DIMENSIONLESS,
            measurement_framework=MeasurementFramework.GOVERNANCE,
            confidence_tier=1,
        )
        return [
            Event(
                event_id=f"{self.input_id}-structural-0",
                source_entity_id=self.target_entity,
                event_type=f"structural_policy_{self.instrument.value}",
                affected_attributes={self.instrument.value: delta},
                propagation_rules=self.propagation_rules,
                timestep_originated=timestep,
                framework=MeasurementFramework.GOVERNANCE,
                metadata={
                    "control_input_id": self.input_id,
                    "actor_id": self.actor_id,
                    "affected_sector": self.affected_sector,
                    "parameters": self.parameters,
                    "implementation_years": self.implementation_years,
                },
            )
        ]


# ---------------------------------------------------------------------------
# Private capital inputs (Issue #33 — Investment Agent RISK-TOLERANT)
# ---------------------------------------------------------------------------


@dataclass(kw_only=True)
class CapitalFlowInput(ControlInput):
    """A private or sovereign capital flow event.

    Models the capital movements that are the primary transmission mechanism
    for financial shocks in developing economies: FDI, portfolio flows, and
    sovereign debt market transactions. Unlike government policy instruments,
    these flows originate from actors outside the sovereign government.

    Attributes:
        flow_type: Category of capital movement (FDI, portfolio, sovereign debt,
            remittance).
        volume: Signed Decimal — positive = inflow, negative = outflow. Units
            are % of GDP (RATIO) for cross-country comparability.
        counterpart_entity: Optional ISO entity ID of the counterpart actor
            (e.g. the investing country or institution).
    """

    flow_type: CapitalFlowType = CapitalFlowType.FDI
    volume: Decimal = Decimal("0")
    counterpart_entity: str = ""

    def to_events(self, timestep: datetime) -> list[Event]:
        """Translate to capital flow Events affecting fdi_stock, portfolio_flows,
        or reserve_adequacy depending on flow_type.

        Args:
            timestep: Simulation timestep at which this input fires.

        Returns:
            Single-element list containing the capital flow Event.
        """
        from app.simulation.engine.models import Event, MeasurementFramework

        # Attribute targets per flow type
        _ATTR_MAP: dict[CapitalFlowType, str] = {
            CapitalFlowType.FDI: "fdi_stock",
            CapitalFlowType.PORTFOLIO_INVESTMENT: "portfolio_flows",
            CapitalFlowType.SOVEREIGN_DEBT: "reserve_adequacy",
            CapitalFlowType.REMITTANCE: "portfolio_flows",
        }
        attribute_key = _ATTR_MAP[self.flow_type]

        delta = Quantity(
            value=self.volume,
            unit="pct_gdp",
            variable_type=VariableType.FLOW,
            measurement_framework=MeasurementFramework.FINANCIAL,
            confidence_tier=2,
        )
        return [
            Event(
                event_id=f"{self.input_id}-capital-0",
                source_entity_id=self.target_entity,
                event_type=f"capital_flow_{self.flow_type.value}",
                affected_attributes={attribute_key: delta},
                propagation_rules=self.propagation_rules,
                timestep_originated=timestep,
                framework=MeasurementFramework.FINANCIAL,
                metadata={
                    "control_input_id": self.input_id,
                    "actor_id": self.actor_id,
                    "flow_type": self.flow_type.value,
                    "counterpart_entity": self.counterpart_entity,
                },
            )
        ]


@dataclass(kw_only=True)
class DFICommitmentInput(ControlInput):
    """A Development Finance Institution commitment.

    Covers IFC, MIGA, bilateral DFI, and MDB instruments — the concessional
    and guarantee mechanisms through which public development finance is
    channelled. Distinguished from private capital flows by the actor type
    (DFI) and the instrument type (guarantee, equity, concessional loan, etc.).

    Attributes:
        instrument: DFI instrument type (guarantee, equity, concessional loan, etc.).
        volume: Committed amount as % of GDP (RATIO). Positive = commitment inflow.
        dfi_actor: Optional ISO or institution ID of the DFI (e.g. 'IFC', 'AfDB').
        disbursement_schedule_years: Number of years over which the commitment
            is expected to disburse. Informational — does not drive re-injection
            (use duration_periods for sustained multi-step effects).
    """

    instrument: DFIInstrumentType = DFIInstrumentType.GUARANTEE
    volume: Decimal = Decimal("0")
    dfi_actor: str = ""
    disbursement_schedule_years: int = 1

    def to_events(self, timestep: datetime) -> list[Event]:
        """Translate to DFI commitment Events affecting fdi_stock and
        infrastructure-related attributes.

        Args:
            timestep: Simulation timestep at which this input fires.

        Returns:
            Single-element list containing the DFI commitment Event.
        """
        from app.simulation.engine.models import Event, MeasurementFramework

        delta = Quantity(
            value=self.volume,
            unit="pct_gdp",
            variable_type=VariableType.FLOW,
            measurement_framework=MeasurementFramework.FINANCIAL,
            confidence_tier=2,
        )
        return [
            Event(
                event_id=f"{self.input_id}-dfi-0",
                source_entity_id=self.target_entity,
                event_type=f"dfi_commitment_{self.instrument.value}",
                affected_attributes={"fdi_stock": delta},
                propagation_rules=self.propagation_rules,
                timestep_originated=timestep,
                framework=MeasurementFramework.FINANCIAL,
                metadata={
                    "control_input_id": self.input_id,
                    "actor_id": self.actor_id,
                    "dfi_actor": self.dfi_actor,
                    "instrument": self.instrument.value,
                    "disbursement_schedule_years": self.disbursement_schedule_years,
                },
            )
        ]


# ---------------------------------------------------------------------------
# Contingent inputs
# ---------------------------------------------------------------------------


@dataclass(kw_only=True)
class StateCondition:
    """A condition on an entity attribute that triggers a ContingentInput.

    This is the watchdog structure that monitors simulation state and
    fires contingent inputs when thresholds are crossed. It is where
    regime-switching and tipping point dynamics are represented in
    the orchestration layer.

    Attributes:
        entity_id: Entity whose attribute is monitored.
        attribute: Attribute key to compare against the threshold.
        operator: Comparison direction.
        threshold: Value to compare against (float for StateCondition interface).
    """

    entity_id: str
    attribute: str
    operator: ComparisonOperator
    threshold: float

    def is_met(self, state: SimulationState) -> bool:
        """Evaluate whether this condition holds in the given state.

        Returns False if the entity or attribute is absent — no entity
        means no threshold crossing. Absence is treated as condition not met
        rather than raising, because the entity may be outside the active
        resolution scope.

        Uses get_attribute_value() to obtain the Decimal attribute value,
        then converts to float for comparison against self.threshold.

        Args:
            state: Simulation state to evaluate the condition against.

        Returns:
            True if the condition holds in the given state.
        """
        entity = state.get_entity(self.entity_id)
        if entity is None:
            return False
        current_value = float(entity.get_attribute_value(self.attribute))
        results: dict[ComparisonOperator, bool] = {
            ComparisonOperator.LT: current_value < self.threshold,
            ComparisonOperator.GT: current_value > self.threshold,
            ComparisonOperator.LTE: current_value <= self.threshold,
            ComparisonOperator.GTE: current_value >= self.threshold,
            ComparisonOperator.EQ: current_value == self.threshold,
        }
        return results[self.operator]


@dataclass(kw_only=True)
class CompoundStateCondition:
    """Multi-attribute AND/OR trigger logic for ContingentInput (Issue #157).

    Enables crisis-realistic compound conditions that single-attribute
    StateCondition cannot express:
      - Capital controls fire when BOTH reserves < 3 months AND outflow > 15%
      - Bank runs accelerate when depositor_confidence < 0.3 OR bank_holiday > 0.5
      - IMF Article IV intervention when reserves AND current_account AND debt_service
        all breach thresholds simultaneously

    Conditions are evaluated recursively — a CompoundStateCondition may nest
    StateCondition instances or other CompoundStateCondition instances.

    Attributes:
        operator: LogicalOperator.AND (all sub-conditions must hold) or
                  LogicalOperator.OR (at least one must hold).
        conditions: List of conditions to evaluate. Must not be empty.
    """

    operator: LogicalOperator
    conditions: list[StateCondition | CompoundStateCondition] = field(
        default_factory=list
    )

    def is_met(self, state: SimulationState) -> bool:
        """Evaluate whether this compound condition holds.

        AND: all sub-conditions must return True.
        OR: at least one sub-condition must return True.

        Short-circuits: AND stops at first False; OR stops at first True.
        Empty conditions list returns False (conservative — no conditions means
        unknown state, not satisfied).

        Args:
            state: Simulation state to evaluate the conditions against.

        Returns:
            True if the compound condition holds.
        """
        if not self.conditions:
            return False
        if self.operator == LogicalOperator.AND:
            return all(c.is_met(state) for c in self.conditions)
        return any(c.is_met(state) for c in self.conditions)


@dataclass(kw_only=True)
class ContingentInput:
    """A ControlInput that fires automatically when a state condition is met.

    ContingentInputs encode regime-switching behaviour: when a monitored
    variable crosses a threshold, the wrapped ControlInput fires as if a
    human actor had submitted it (with source set to CONTINGENT_TRIGGER).

    cooldown_periods prevents repeated firing: after a trigger, the
    contingent will not fire again for at least cooldown_periods timesteps.
    The empirical_basis field documents the historical cases that support
    the threshold value and cooldown assumption.

    Attributes:
        contingent_id: Unique identifier for this contingent.
        condition: The state condition to monitor.
        input: The ControlInput to inject when condition is met.
        cooldown_periods: Minimum timesteps between firings.
        documented_rationale: Why this contingent exists in the scenario.
        empirical_basis: Historical cases supporting the trigger parameters.
    """

    contingent_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    # condition accepts StateCondition (single attribute) or CompoundStateCondition
    # (multi-attribute AND/OR logic — Issue #157). Backward compatible: existing
    # callers using StateCondition continue to work unchanged.
    condition: StateCondition | CompoundStateCondition = field(
        default=None  # type: ignore[assignment]
    )
    input: ControlInput = field(default=None)  # type: ignore[assignment]
    cooldown_periods: int = 1
    documented_rationale: str = ""
    empirical_basis: str = ""


# ---------------------------------------------------------------------------
# External sector inputs (ADR-012, Issue #751)
# ---------------------------------------------------------------------------

# Fraction of import price shock that reaches bottom-quintile consumption
# within one simulation step. Approximation calibrated against World Bank
# food/fuel price transmission studies (2007–2008 crisis). Full calibration
# deferred to Issue #275.
_HCL_TRANSMISSION_FACTOR = Decimal("0.3")


@dataclass(kw_only=True)
class BilateralTradeShock(ControlInput):
    """A bilateral trade disruption injected at a specific simulation step (ADR-012, #751).

    Models: sanctions, bilateral tariff escalation, export channel closures,
    and any shock originating from a named source entity and landing on a named
    target entity via their trade relationship.

    Generates two Events:
      1. Financial: `import_price_inflation` delta on target_entity, FINANCIAL framework.
      2. Human development: `bottom_quintile_consumption_capacity` delta on target_entity,
         HUMAN_DEVELOPMENT framework; magnitude = shock * _HCL_TRANSMISSION_FACTOR.

    Attributes:
        source_entity_id: Entity originating the disruption (e.g. the sanctioning state).
        commodity_category: Affected commodity category (FUEL, FOOD, METALS, OTHER).
        magnitude: Positive = import cost increase (price up or volume down).
            Decimal fraction of baseline import value.
        trade_channel: "import_price" (default) or "export_revenue".
    """

    source_entity_id: str = ""
    commodity_category: CommodityCategory = CommodityCategory.FUEL
    magnitude: Decimal = Decimal("0")
    trade_channel: str = "import_price"

    def to_events(self, timestep: datetime) -> list[Event]:
        from app.simulation.engine.models import Event, MeasurementFramework  # noqa: PLC0415

        fin_delta = Quantity(
            value=self.magnitude,
            unit="dimensionless",
            variable_type=VariableType.FLOW,
            measurement_framework=MeasurementFramework.FINANCIAL,
            confidence_tier=3,
        )
        hcl_delta = Quantity(
            value=-(self.magnitude * _HCL_TRANSMISSION_FACTOR),
            unit="dimensionless",
            variable_type=VariableType.FLOW,
            measurement_framework=MeasurementFramework.HUMAN_DEVELOPMENT,
            confidence_tier=3,
        )
        category = self.commodity_category.value
        return [
            Event(
                event_id=f"{self.input_id}-trade-shock-fin-0",
                source_entity_id=self.source_entity_id or self.target_entity,
                event_type=f"bilateral_trade_shock_{category}",
                affected_attributes={"import_price_inflation": fin_delta},
                propagation_rules=self.propagation_rules,
                timestep_originated=timestep,
                framework=MeasurementFramework.FINANCIAL,
                metadata={
                    "control_input_id": self.input_id,
                    "source_entity_id": self.source_entity_id,
                    "commodity_category": category,
                    "trade_channel": self.trade_channel,
                },
            ),
            Event(
                event_id=f"{self.input_id}-trade-shock-hcl-0",
                source_entity_id=self.source_entity_id or self.target_entity,
                event_type=f"bilateral_trade_shock_{category}_hcl",
                affected_attributes={"bottom_quintile_consumption_capacity": hcl_delta},
                propagation_rules=self.propagation_rules,
                timestep_originated=timestep,
                framework=MeasurementFramework.HUMAN_DEVELOPMENT,
                metadata={
                    "control_input_id": self.input_id,
                    "commodity_category": category,
                },
            ),
        ]
