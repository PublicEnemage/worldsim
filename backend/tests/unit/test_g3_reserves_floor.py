"""Unit tests for G3: reserves non-negativity floor.

Issue #799 — reserve_coverage_months dropped to −0.04 months at Demo 4 step 7.
The propagation engine now enforces a non-negativity floor via _ATTRIBUTE_FLOORS.

Coverage:
  _build_next_state — FLOW delta drives reserve below zero
    1.  reserve_coverage_months floored at 0.0 when FLOW delta produces negative.
    2.  reserve_coverage_months unchanged when FLOW delta produces positive.
    3.  reserve_coverage_months floored at 0.0 when FLOW delta exactly nullifies.
    4.  bottom_quintile_consumption_capacity floored at 0.0 (second registered attr).
    5.  Unregistered attribute (trade_balance_pct_gdp) allowed to go negative.
    6.  STOCK replacement that sets reserve negative is also floored.
    7.  Floor preserves all other Quantity fields (unit, confidence_tier).
    8.  Multiple entities: only the entity with negative reserves is floored.
"""

from datetime import datetime
from decimal import Decimal

from app.simulation.engine.models import (
    Event,
    MeasurementFramework,
    ResolutionConfig,
    ScenarioConfig,
    SimulationEntity,
    SimulationState,
)
from app.simulation.engine.propagation import propagate
from app.simulation.engine.quantity import Quantity, VariableType

# ---------------------------------------------------------------------------
# Helpers — mirror pattern in test_propagation.py
# ---------------------------------------------------------------------------

_NOW = datetime(2020, 1, 1)


def _qty(
    value: float,
    vtype: VariableType = VariableType.FLOW,
    unit: str = "months",
    framework: MeasurementFramework = MeasurementFramework.FINANCIAL,
    tier: int = 3,
) -> Quantity:
    return Quantity(
        value=Decimal(str(value)),
        unit=unit,
        variable_type=vtype,
        measurement_framework=framework,
        confidence_tier=tier,
    )


def _entity(entity_id: str, attrs: dict[str, Quantity]) -> SimulationEntity:
    return SimulationEntity(
        id=entity_id,
        entity_type="nation",
        attributes=attrs,
        metadata={"name": entity_id},
    )


def _state(entities: dict[str, SimulationEntity]) -> SimulationState:
    return SimulationState(
        timestep=_NOW,
        resolution=ResolutionConfig(),
        entities=entities,
        relationships=[],
        events=[],
        scenario_config=ScenarioConfig(
            scenario_id="test",
            name="Test",
            description="",
            start_date=_NOW,
            end_date=datetime(2025, 1, 1),
        ),
    )


def _reserve_event(entity_id: str, delta: float) -> Event:
    return Event(
        event_id=f"{entity_id}-rsv",
        source_entity_id=entity_id,
        event_type="commodity_price_shock_oil_reserve",
        affected_attributes={"reserve_coverage_months": _qty(delta)},
        propagation_rules=[],
        timestep_originated=_NOW,
        framework=MeasurementFramework.FINANCIAL,
    )


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


def test_reserve_floored_when_flow_drives_negative() -> None:
    """AC-2: initial=0.5, delta=-2.0 → value=0.0 (not -1.5)."""
    state = _state({"JOR": _entity("JOR", {"reserve_coverage_months": _qty(0.5)})})
    next_state = propagate(state, [_reserve_event("JOR", -2.0)])
    result = next_state.entities["JOR"].attributes["reserve_coverage_months"].value
    assert result == Decimal("0"), f"Expected 0, got {result}"


def test_reserve_unchanged_when_flow_positive() -> None:
    """Reserve increases when FLOW delta is positive — floor does not interfere."""
    state = _state({"JOR": _entity("JOR", {"reserve_coverage_months": _qty(2.0)})})
    next_state = propagate(state, [_reserve_event("JOR", 0.5)])
    result = next_state.entities["JOR"].attributes["reserve_coverage_months"].value
    assert result == Decimal("2.5")


def test_reserve_floored_at_exact_nullification() -> None:
    """initial=1.0, delta=-1.0 → value=0.0 (boundary: exactly zero after accumulation)."""
    state = _state({"JOR": _entity("JOR", {"reserve_coverage_months": _qty(1.0)})})
    next_state = propagate(state, [_reserve_event("JOR", -1.0)])
    result = next_state.entities["JOR"].attributes["reserve_coverage_months"].value
    assert result == Decimal("0")


def test_bottom_quintile_consumption_floored() -> None:
    """bottom_quintile_consumption_capacity is also in _ATTRIBUTE_FLOORS."""
    bqcc_qty = _qty(0.1, unit="dimensionless", framework=MeasurementFramework.HUMAN_DEVELOPMENT)
    state = _state({"JOR": _entity("JOR", {"bottom_quintile_consumption_capacity": bqcc_qty})})
    event = Event(
        event_id="JOR-bqcc",
        source_entity_id="JOR",
        event_type="commodity_price_shock_hcl",
        affected_attributes={
            "bottom_quintile_consumption_capacity": _qty(
                -5.0, unit="dimensionless", framework=MeasurementFramework.HUMAN_DEVELOPMENT
            )
        },
        propagation_rules=[],
        timestep_originated=_NOW,
        framework=MeasurementFramework.HUMAN_DEVELOPMENT,
    )
    next_state = propagate(state, [event])
    result = next_state.entities["JOR"].attributes["bottom_quintile_consumption_capacity"].value
    assert result == Decimal("0"), f"Expected 0, got {result}"


def test_unregistered_attribute_can_go_negative() -> None:
    """Attributes not in _ATTRIBUTE_FLOORS are not constrained — signed flows are valid."""
    tb_qty = _qty(0.5, vtype=VariableType.RATIO, unit="ratio")
    state = _state({"JOR": _entity("JOR", {"trade_balance_pct_gdp": tb_qty})})
    event = Event(
        event_id="JOR-trade",
        source_entity_id="JOR",
        event_type="trade_shock",
        affected_attributes={
            "trade_balance_pct_gdp": _qty(-2.0, vtype=VariableType.RATIO, unit="ratio")
        },
        propagation_rules=[],
        timestep_originated=_NOW,
        framework=MeasurementFramework.FINANCIAL,
    )
    next_state = propagate(state, [event])
    result = next_state.entities["JOR"].attributes["trade_balance_pct_gdp"].value
    assert result == Decimal("-1.5"), f"Expected -1.5, got {result}"


def test_stock_replacement_negative_is_floored() -> None:
    """A STOCK delta with a negative absolute value is also floored at 0."""
    state = _state({"JOR": _entity("JOR", {"reserve_coverage_months": _qty(5.0)})})
    negative_stock = Quantity(
        value=Decimal("-3"),
        unit="months",
        variable_type=VariableType.STOCK,
        measurement_framework=MeasurementFramework.FINANCIAL,
        confidence_tier=3,
    )
    event = Event(
        event_id="JOR-stock-reset",
        source_entity_id="JOR",
        event_type="stock_reset",
        affected_attributes={"reserve_coverage_months": negative_stock},
        propagation_rules=[],
        timestep_originated=_NOW,
        framework=MeasurementFramework.FINANCIAL,
    )
    next_state = propagate(state, [event])
    result = next_state.entities["JOR"].attributes["reserve_coverage_months"].value
    assert result == Decimal("0"), f"STOCK replacement of -3 should be floored to 0, got {result}"


def test_floor_preserves_quantity_metadata() -> None:
    """After flooring, unit and confidence_tier are preserved from the accumulated Quantity."""
    initial = Quantity(
        value=Decimal("0.5"),
        unit="months",
        variable_type=VariableType.FLOW,
        measurement_framework=MeasurementFramework.FINANCIAL,
        confidence_tier=3,
    )
    state = _state({"JOR": _entity("JOR", {"reserve_coverage_months": initial})})
    event = Event(
        event_id="JOR-rsv",
        source_entity_id="JOR",
        event_type="reserve_shock",
        affected_attributes={"reserve_coverage_months": _qty(-2.0)},
        propagation_rules=[],
        timestep_originated=_NOW,
        framework=MeasurementFramework.FINANCIAL,
    )
    next_state = propagate(state, [event])
    floored = next_state.entities["JOR"].attributes["reserve_coverage_months"]
    assert floored.value == Decimal("0")
    assert floored.unit == "months"
    assert floored.confidence_tier == 3


def test_only_negative_entity_is_floored() -> None:
    """With two entities, only the entity with a large negative delta is floored."""
    state = _state({
        "JOR": _entity("JOR", {"reserve_coverage_months": _qty(0.5)}),
        "EGY": _entity("EGY", {"reserve_coverage_months": _qty(3.0)}),
    })
    next_state = propagate(state, [
        _reserve_event("JOR", -5.0),   # would produce -4.5 → floored to 0
        _reserve_event("EGY", -0.5),   # produces 2.5 → not floored
    ])
    assert next_state.entities["JOR"].attributes["reserve_coverage_months"].value == Decimal("0")
    assert next_state.entities["EGY"].attributes["reserve_coverage_months"].value == Decimal("2.5")
