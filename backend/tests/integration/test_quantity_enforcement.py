"""
Integration tests for the Quantity type contract — SCR-001 / QA-1.

These tests assert that all entity attribute values in a simulation run are
Quantity instances, not raw floats or any other type. The contract is that
SimulationEntity.attributes is dict[str, Quantity] throughout the propagation
lifecycle — at initialisation, after event application, and after multi-step
scenario runs.

These are integration tests (not unit tests) because they exercise the full
propagation engine and orchestration runner, not isolated units.
"""

from __future__ import annotations

from datetime import datetime, timedelta
from decimal import Decimal

from app.simulation.engine.models import (
    Event,
    MeasurementFramework,
    PropagationRule,
    Relationship,
    ResolutionConfig,
    ScenarioConfig,
    SimulationEntity,
    SimulationState,
)
from app.simulation.engine.propagation import propagate
from app.simulation.engine.quantity import Quantity, VariableType
from app.simulation.orchestration import (
    FiscalInstrument,
    FiscalPolicyInput,
    MonetaryRateInput,
    MonetaryRateInstrument,
    ScenarioRunner,
    TradeInstrument,
    TradePolicyInput,
)

_BASE_DATE = datetime(2025, 1, 1)


def _make_quantity(value: float, vtype: VariableType = VariableType.RATIO) -> Quantity:
    return Quantity(
        value=Decimal(str(value)),
        unit="dimensionless",
        variable_type=vtype,
    )


def _make_entity(entity_id: str, **attrs: float) -> SimulationEntity:
    return SimulationEntity(
        id=entity_id,
        entity_type="country",
        attributes={k: _make_quantity(v) for k, v in attrs.items()},
        metadata={},
    )


def _make_state(
    entities: dict[str, SimulationEntity],
    relationships: list[Relationship] | None = None,
) -> SimulationState:
    return SimulationState(
        timestep=_BASE_DATE,
        resolution=ResolutionConfig(),
        entities=entities,
        relationships=relationships or [],
        events=[],
        scenario_config=ScenarioConfig(
            scenario_id="test",
            name="Test",
            description="",
            start_date=_BASE_DATE,
            end_date=_BASE_DATE + timedelta(days=3650),
        ),
    )


def _assert_all_quantities(state: SimulationState, label: str) -> None:
    """Assert every attribute value in every entity is a Quantity instance."""
    for entity_id, entity in state.entities.items():
        for attr_key, attr_value in entity.attributes.items():
            assert isinstance(attr_value, Quantity), (
                f"{label}: entity '{entity_id}' attribute '{attr_key}' "
                f"has type {type(attr_value).__name__}, expected Quantity"
            )


class TestQuantityContractAfterPropagation:
    """All attribute values remain Quantity after propagate()."""

    def test_initial_state_attributes_are_quantities(self) -> None:
        state = _make_state({"BOL": _make_entity("BOL", gdp_growth=0.02, debt_gdp=0.55)})
        _assert_all_quantities(state, "initial state")

    def test_propagate_with_no_events_preserves_quantity_contract(self) -> None:
        state = _make_state({"BOL": _make_entity("BOL", gdp_growth=0.02)})
        result = propagate(state, [])
        _assert_all_quantities(result, "after propagate([]) ")

    def test_propagate_with_event_preserves_quantity_contract(self) -> None:
        state = _make_state({"BOL": _make_entity("BOL", gdp_growth=0.02)})
        event = Event(
            event_id="e1",
            source_entity_id="BOL",
            event_type="shock",
            affected_attributes={
                "gdp_growth": _make_quantity(-0.05, VariableType.RATIO)
            },
            propagation_rules=[],
            timestep_originated=_BASE_DATE,
            framework=MeasurementFramework.FINANCIAL,
        )
        result = propagate(state, [event])
        _assert_all_quantities(result, "after event application")

    def test_propagation_hop_preserves_quantity_contract(self) -> None:
        state = _make_state(
            {"BOL": _make_entity("BOL", trade_balance=0.0), "ARG": _make_entity("ARG")},
            relationships=[
                Relationship(
                    source_id="BOL",
                    target_id="ARG",
                    relationship_type="trade",
                    weight=0.5,
                )
            ],
        )
        event = Event(
            event_id="e1",
            source_entity_id="BOL",
            event_type="trade_shock",
            affected_attributes={"trade_balance": _make_quantity(0.10, VariableType.FLOW)},
            propagation_rules=[PropagationRule(relationship_type="trade", attenuation_factor=0.5)],
            timestep_originated=_BASE_DATE,
            framework=MeasurementFramework.FINANCIAL,
        )
        result = propagate(state, [event])
        _assert_all_quantities(result, "after propagation hop to ARG")


class TestQuantityContractAfterScenarioRun:
    """All attribute values remain Quantity through a multi-step ScenarioRunner."""

    def _run(
        self,
        entities: dict[str, SimulationEntity],
        inputs: list,
        n_steps: int = 3,
    ) -> list[SimulationState]:
        runner = ScenarioRunner(
            initial_state=_make_state(entities),
            scheduled_inputs=inputs,
            modules=[],
            n_steps=n_steps,
        )
        return runner.run()

    def test_no_inputs_run_preserves_quantity_contract(self) -> None:
        history = self._run({"USA": _make_entity("USA", gdp_growth=0.02)}, [])
        for i, state in enumerate(history):
            _assert_all_quantities(state, f"step {i}")

    def test_monetary_rate_input_preserves_quantity_contract(self) -> None:
        inp = MonetaryRateInput(
            target_entity="USA",
            instrument=MonetaryRateInstrument.POLICY_RATE,
            value=Decimal("0.005"),
            effective_date=_BASE_DATE,
            timestamp=_BASE_DATE,
        )
        history = self._run({"USA": _make_entity("USA")}, [(1, inp)])
        for i, state in enumerate(history):
            _assert_all_quantities(state, f"step {i}")

    def test_fiscal_input_preserves_quantity_contract(self) -> None:
        inp = FiscalPolicyInput(
            target_entity="GRC",
            instrument=FiscalInstrument.SPENDING_CHANGE,
            sector="health",
            value=Decimal("0.02"),
            effective_date=_BASE_DATE,
            timestamp=_BASE_DATE,
        )
        history = self._run({"GRC": _make_entity("GRC")}, [(2, inp)], n_steps=3)
        for i, state in enumerate(history):
            _assert_all_quantities(state, f"step {i}")

    def test_trade_input_with_retaliation_preserves_quantity_contract(self) -> None:
        inp = TradePolicyInput(
            target_entity="CHN",
            source_entity="USA",
            instrument=TradeInstrument.TARIFF_RATE,
            affected_sector="goods",
            value=Decimal("0.25"),
            retaliation_modeled=True,
            effective_date=_BASE_DATE,
            timestamp=_BASE_DATE,
        )
        history = self._run(
            {"USA": _make_entity("USA"), "CHN": _make_entity("CHN")},
            [(1, inp)],
        )
        for i, state in enumerate(history):
            _assert_all_quantities(state, f"step {i}")


class TestQuantityValueTypes:
    """Attribute values are Quantity with Decimal values, never float."""

    def test_attribute_value_is_decimal_not_float(self) -> None:
        entity = _make_entity("BOL", gdp_growth=0.02)
        q = entity.get_attribute("gdp_growth")
        assert q is not None
        assert isinstance(q.value, Decimal)

    def test_get_attribute_value_returns_decimal(self) -> None:
        entity = _make_entity("BOL", reserves=5.0e9)
        val = entity.get_attribute_value("reserves")
        assert isinstance(val, Decimal)

    def test_propagated_attribute_value_is_decimal(self) -> None:
        state = _make_state({"BOL": _make_entity("BOL", gdp_growth=0.02)})
        event = Event(
            event_id="e1",
            source_entity_id="BOL",
            event_type="shock",
            affected_attributes={"gdp_growth": _make_quantity(-0.01)},
            propagation_rules=[],
            timestep_originated=_BASE_DATE,
            framework=MeasurementFramework.FINANCIAL,
        )
        result = propagate(state, [event])
        q = result.entities["BOL"].get_attribute("gdp_growth")
        assert q is not None
        assert isinstance(q.value, Decimal)
