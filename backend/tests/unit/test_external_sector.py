"""External sector module tests — ADR-012, Issues #751 and #752.

Covers:
  - BilateralTradeShock.to_events() generates financial and HCL events
  - BilateralTradeShock zero-magnitude produces zero-effect events
  - BilateralTradeShock: no dependency relationship required (direct bilateral)
  - ExternalSectorModule: shock distributes proportionally to import dependency
  - ExternalSectorModule: entity with zero dependency receives no shock
  - ExternalSectorModule: entity with missing dependency attribute receives no shock
  - ExternalSectorModule: shock fires only within start_step to start_step+duration range
  - ExternalSectorModule: empty shocks list produces no events
  - ExternalSectorModule: human cost effect appears within 2 steps (AC #751/#752)
  - Deserialization: BilateralTradeShock round-trips through _deserialize_control_input
"""
from __future__ import annotations

from datetime import UTC, datetime, timedelta
from decimal import Decimal

import pytest

from app.schemas import CommodityShockConfig, ScenarioConfigSchema
from app.simulation.engine.models import (
    MeasurementFramework,
    ResolutionConfig,
    ScenarioConfig,
    SimulationEntity,
    SimulationState,
)
from app.simulation.engine.quantity import Quantity, VariableType
from app.simulation.modules.external_sector.module import ExternalSectorModule
from app.simulation.orchestration.inputs import (
    BilateralTradeShock,
    CommodityCategory,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_BASE_DATE = datetime(2010, 1, 1, tzinfo=UTC)
_STEP_DELTA = timedelta(days=365)


def _q(value: float, tier: int = 3) -> Quantity:
    return Quantity(
        value=Decimal(str(value)),
        unit="dimensionless",
        variable_type=VariableType.RATIO,
        confidence_tier=tier,
    )


def _entity(entity_id: str, **attrs: float) -> SimulationEntity:
    return SimulationEntity(
        id=entity_id,
        entity_type="country",
        attributes={k: _q(v) for k, v in attrs.items()},
        metadata={},
    )


def _state(entities: dict[str, SimulationEntity], step: int = 1) -> SimulationState:
    return SimulationState(
        entities=entities,
        relationships=[],
        events=[],
        timestep=_BASE_DATE + _STEP_DELTA * step,
        scenario_config=ScenarioConfig(
            scenario_id="test",
            name="test",
            description="",
            start_date=_BASE_DATE,
            end_date=_BASE_DATE + _STEP_DELTA * 10,
        ),
        resolution=ResolutionConfig(),
    )


# ---------------------------------------------------------------------------
# BilateralTradeShock tests
# ---------------------------------------------------------------------------


def test_bilateral_shock_generates_financial_event() -> None:
    shock = BilateralTradeShock(
        target_entity="JOR",
        source_entity_id="SAU",
        commodity_category=CommodityCategory.FUEL,
        magnitude=Decimal("0.20"),
    )
    events = shock.to_events(_BASE_DATE)
    fin_events = [e for e in events if e.framework == MeasurementFramework.FINANCIAL]
    assert len(fin_events) == 1
    assert "import_price_inflation" in fin_events[0].affected_attributes
    assert fin_events[0].affected_attributes["import_price_inflation"].value == Decimal("0.20")


def test_bilateral_shock_generates_hcl_event() -> None:
    shock = BilateralTradeShock(
        target_entity="JOR",
        source_entity_id="SAU",
        commodity_category=CommodityCategory.FUEL,
        magnitude=Decimal("0.20"),
    )
    events = shock.to_events(_BASE_DATE)
    hcl_events = [e for e in events if e.framework == MeasurementFramework.HUMAN_DEVELOPMENT]
    assert len(hcl_events) == 1
    attr = hcl_events[0].affected_attributes["bottom_quintile_consumption_capacity"]
    assert attr.value < Decimal("0")
    # 30% transmission factor: -0.20 * 0.3 = -0.06
    assert attr.value == Decimal("-0.06")


def test_bilateral_shock_zero_magnitude_produces_zero_effect() -> None:
    shock = BilateralTradeShock(
        target_entity="GRC",
        source_entity_id="DEU",
        commodity_category=CommodityCategory.FOOD,
        magnitude=Decimal("0"),
    )
    events = shock.to_events(_BASE_DATE)
    assert len(events) == 2
    for evt in events:
        for qty in evt.affected_attributes.values():
            assert qty.value == Decimal("0")


def test_bilateral_shock_event_type_includes_commodity_category() -> None:
    shock = BilateralTradeShock(
        target_entity="JOR",
        source_entity_id="IRQ",
        commodity_category=CommodityCategory.METALS,
        magnitude=Decimal("0.10"),
    )
    events = shock.to_events(_BASE_DATE)
    assert all("metals" in e.event_type for e in events)


def test_bilateral_shock_confidence_tier_is_3() -> None:
    shock = BilateralTradeShock(
        target_entity="JOR",
        source_entity_id="SAU",
        commodity_category=CommodityCategory.FUEL,
        magnitude=Decimal("0.15"),
    )
    events = shock.to_events(_BASE_DATE)
    for evt in events:
        for qty in evt.affected_attributes.values():
            assert qty.confidence_tier == 3


# ---------------------------------------------------------------------------
# ExternalSectorModule — commodity price shock distribution
# ---------------------------------------------------------------------------


def _module(shocks: list[CommodityShockConfig]) -> ExternalSectorModule:
    from datetime import date  # noqa: PLC0415
    return ExternalSectorModule(
        commodity_price_shocks=shocks,
        start_date=date(2010, 1, 1),
    )


def _shock(
    category: str = "fuel",
    magnitude: float = 0.20,
    start_step: int = 1,
    duration_steps: int = 1,
) -> CommodityShockConfig:
    return CommodityShockConfig(
        commodity_category=category,
        magnitude=Decimal(str(magnitude)),
        start_step=start_step,
        duration_steps=duration_steps,
    )


def test_commodity_shock_distributes_to_entity_with_dependency() -> None:
    mod = _module([_shock(category="fuel", magnitude=0.20, start_step=1)])
    entity = _entity("JOR", commodity_import_dependency_fuel=0.40)
    state = _state({"JOR": entity}, step=1)
    events = mod.compute(entity, state, state.timestep)
    fin = [e for e in events if e.framework == MeasurementFramework.FINANCIAL]
    assert len(fin) == 1
    # 0.40 dependency × 0.20 shock = 0.08
    assert fin[0].affected_attributes["import_price_inflation"].value == pytest.approx(
        Decimal("0.08"), abs=Decimal("0.001")
    )


def test_commodity_shock_hcl_effect_within_2_steps() -> None:
    """HCL event fires at step 1 — within 2 steps of shock (AC #751/#752)."""
    mod = _module([_shock(category="fuel", magnitude=0.20, start_step=1)])
    entity = _entity("JOR", commodity_import_dependency_fuel=0.40)
    state = _state({"JOR": entity}, step=1)
    events = mod.compute(entity, state, state.timestep)
    hcl = [e for e in events if e.framework == MeasurementFramework.HUMAN_DEVELOPMENT]
    assert len(hcl) == 1
    # 0.08 × 0.3 = 0.024 negative
    assert hcl[0].affected_attributes["bottom_quintile_consumption_capacity"].value < Decimal("0")


def test_commodity_shock_proportional_to_dependency() -> None:
    mod = _module([_shock(category="fuel", magnitude=0.10, start_step=1)])
    low_dep = _entity("A", commodity_import_dependency_fuel=0.20)
    high_dep = _entity("B", commodity_import_dependency_fuel=0.60)
    state_a = _state({"A": low_dep}, step=1)
    state_b = _state({"B": high_dep}, step=1)

    events_a = mod.compute(low_dep, state_a, state_a.timestep)
    events_b = mod.compute(high_dep, state_b, state_b.timestep)

    fin_a = next(e for e in events_a if e.framework == MeasurementFramework.FINANCIAL)
    fin_b = next(e for e in events_b if e.framework == MeasurementFramework.FINANCIAL)

    val_a = fin_a.affected_attributes["import_price_inflation"].value
    val_b = fin_b.affected_attributes["import_price_inflation"].value
    assert val_b > val_a
    assert val_b == pytest.approx(val_a * 3, rel=Decimal("0.01"))


def test_commodity_shock_zero_dependency_no_events() -> None:
    mod = _module([_shock(category="fuel", magnitude=0.20, start_step=1)])
    entity = _entity("GRC", commodity_import_dependency_fuel=0.0)
    state = _state({"GRC": entity}, step=1)
    assert mod.compute(entity, state, state.timestep) == []


def test_commodity_shock_missing_dependency_no_events() -> None:
    mod = _module([_shock(category="fuel", magnitude=0.20, start_step=1)])
    entity = _entity("GRC")  # no dependency attribute
    state = _state({"GRC": entity}, step=1)
    assert mod.compute(entity, state, state.timestep) == []


def test_commodity_shock_fires_only_within_step_range() -> None:
    mod = _module([_shock(category="food", magnitude=0.15, start_step=2, duration_steps=2)])
    entity = _entity("JOR", commodity_import_dependency_food=0.30)

    # Step 1: before shock
    state_1 = _state({"JOR": entity}, step=1)
    assert mod.compute(entity, state_1, state_1.timestep) == []

    # Step 2: shock active
    state_2 = _state({"JOR": entity}, step=2)
    assert len(mod.compute(entity, state_2, state_2.timestep)) > 0

    # Step 3: last active step
    state_3 = _state({"JOR": entity}, step=3)
    assert len(mod.compute(entity, state_3, state_3.timestep)) > 0

    # Step 4: after shock
    state_4 = _state({"JOR": entity}, step=4)
    assert mod.compute(entity, state_4, state_4.timestep) == []


def test_commodity_shock_empty_shocks_no_events() -> None:
    mod = _module([])
    entity = _entity("JOR", commodity_import_dependency_fuel=0.40)
    state = _state({"JOR": entity}, step=1)
    assert mod.compute(entity, state, state.timestep) == []


# ---------------------------------------------------------------------------
# Deserialization — BilateralTradeShock round-trip
# ---------------------------------------------------------------------------


def test_deserialize_bilateral_trade_shock() -> None:
    from app.simulation.web_scenario_runner import _deserialize_control_input  # noqa: PLC0415

    ctrl = _deserialize_control_input(
        "BilateralTradeShock",
        {
            "target_entity": "JOR",
            "source_entity_id": "IRQ",
            "commodity_category": "fuel",
            "magnitude": "0.25",
            "trade_channel": "import_price",
        },
        ["JOR"],
    )
    assert isinstance(ctrl, BilateralTradeShock)
    assert ctrl.target_entity == "JOR"
    assert ctrl.source_entity_id == "IRQ"
    assert ctrl.commodity_category == CommodityCategory.FUEL
    assert ctrl.magnitude == Decimal("0.25")


def test_deserialize_bilateral_shock_defaults() -> None:
    from app.simulation.web_scenario_runner import _deserialize_control_input  # noqa: PLC0415

    ctrl = _deserialize_control_input(
        "BilateralTradeShock",
        {"commodity_category": "food", "magnitude": "0.10"},
        ["GRC"],
    )
    assert isinstance(ctrl, BilateralTradeShock)
    assert ctrl.target_entity == "GRC"
    assert ctrl.commodity_category == CommodityCategory.FOOD
    assert ctrl.trade_channel == "import_price"


# ---------------------------------------------------------------------------
# ScenarioConfigSchema — commodity_price_shocks field
# ---------------------------------------------------------------------------


def test_scenario_config_commodity_shocks_default_empty() -> None:
    cfg = ScenarioConfigSchema(entities=["JOR"], n_steps=3)
    assert cfg.commodity_price_shocks == []


def test_scenario_config_commodity_shock_accepted() -> None:
    cfg = ScenarioConfigSchema(
        entities=["JOR"],
        n_steps=5,
        commodity_price_shocks=[
            CommodityShockConfig(
                commodity_category="fuel",
                magnitude=Decimal("0.30"),
                start_step=1,
                duration_steps=2,
            )
        ],
    )
    assert len(cfg.commodity_price_shocks) == 1
    assert cfg.commodity_price_shocks[0].commodity_category == "fuel"
    assert cfg.commodity_price_shocks[0].magnitude == Decimal("0.30")
