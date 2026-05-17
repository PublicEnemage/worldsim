"""Unit tests for EcologicalModule — Issue #204.

Covers:
  - Non-country entity returns []
  - No prior events returns []
  - gdp_growth_change triggers co2_concentration_ppm delta
  - fiscal_policy_spending_change triggers land_use_pressure_index delta
  - All emitted events have framework=MeasurementFramework.ECOLOGICAL (Issue #42)
  - All emitted events have event_type='ecological_indicator_update'
  - get_subscribed_events matches _SUBSCRIBED_EVENTS
  - _SUBSCRIBED_EVENTS constant matches implementation spec
  - Decimal enforcement (no float in affected_attributes)
  - Unknown event type produces no delta
  - Registry has >= 2 entries
  - Registry source_registry_ids follow ACADEMIC_LITERATURE_* convention
  - Registry event types are all in _SUBSCRIBED_EVENTS
  - co2_concentration_ppm uses VariableType.STOCK
  - land_use_pressure_index uses VariableType.RATIO
  - mandatory ecological note present in scenarios._ECOLOGICAL_MANDATORY_NOTE
  - mandatory note text matches ADR-005 Amendment B verbatim requirement

All tests run without a database connection.
"""
from __future__ import annotations

import logging
from datetime import UTC, datetime
from decimal import Decimal
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import pytest

from app.simulation.engine.models import (
    Event,
    MeasurementFramework,
    ResolutionConfig,
    ScenarioConfig,
    SimulationEntity,
    SimulationState,
)
from app.simulation.engine.quantity import Quantity, VariableType
from app.simulation.modules.ecological.elasticities import (
    ECOLOGICAL_ELASTICITY_REGISTRY,
)
from app.simulation.modules.ecological.module import (
    _SUBSCRIBED_EVENTS,
    EcologicalModule,
)

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


def _country_entity(entity_id: str = "GRC") -> SimulationEntity:
    return SimulationEntity(
        id=entity_id,
        entity_type="country",
        attributes={},
        metadata={},
    )


def _cohort_entity() -> SimulationEntity:
    return SimulationEntity(
        id="GRC:CHT:1-25-54-FORMAL",
        entity_type="cohort",
        attributes={},
        metadata={},
    )


_TS = datetime(2010, 1, 1, tzinfo=UTC)


def _make_state(events: list[Event] | None = None) -> SimulationState:
    return SimulationState(
        timestep=_TS,
        resolution=ResolutionConfig(),
        entities={},
        relationships=[],
        events=events or [],
        scenario_config=ScenarioConfig(
            scenario_id="test-sid",
            name="Test",
            description="",
            start_date=_TS,
            end_date=_TS,
        ),
    )


def _gdp_event(entity_id: str = "GRC", magnitude: str = "-0.025") -> Event:
    return Event(
        event_id=f"macro-gdp-{entity_id}-2010",
        source_entity_id=entity_id,
        event_type="gdp_growth_change",
        affected_attributes={
            "gdp_growth": Quantity(
                value=Decimal(magnitude),
                unit="dimensionless",
                variable_type=VariableType.RATIO,
                measurement_framework=MeasurementFramework.FINANCIAL,
                confidence_tier=1,
            ),
        },
        propagation_rules=[],
        timestep_originated=datetime(2010, 1, 1, tzinfo=UTC),
        framework=MeasurementFramework.FINANCIAL,
        metadata={},
    )


def _fiscal_event(entity_id: str = "GRC", magnitude: str = "-0.05") -> Event:
    return Event(
        event_id=f"fiscal-{entity_id}-2010",
        source_entity_id=entity_id,
        event_type="fiscal_policy_spending_change",
        affected_attributes={
            "fiscal_policy_spending_change": Quantity(
                value=Decimal(magnitude),
                unit="dimensionless",
                variable_type=VariableType.RATIO,
                measurement_framework=MeasurementFramework.FINANCIAL,
                confidence_tier=2,
            ),
        },
        propagation_rules=[],
        timestep_originated=datetime(2010, 1, 1, tzinfo=UTC),
        framework=MeasurementFramework.FINANCIAL,
        metadata={},
    )


def _emergency_event(entity_id: str = "GRC") -> Event:
    return Event(
        event_id=f"emrg-{entity_id}-2010",
        source_entity_id=entity_id,
        event_type="emergency_declaration",
        affected_attributes={
            "emergency_declaration": Quantity(
                value=Decimal("1"),
                unit="dimensionless",
                variable_type=VariableType.DIMENSIONLESS,
                measurement_framework=MeasurementFramework.FINANCIAL,
                confidence_tier=2,
            ),
        },
        propagation_rules=[],
        timestep_originated=datetime(2010, 1, 1, tzinfo=UTC),
        framework=MeasurementFramework.FINANCIAL,
        metadata={},
    )


TIMESTEP = datetime(2011, 1, 1, tzinfo=UTC)

# ---------------------------------------------------------------------------
# Non-country entity
# ---------------------------------------------------------------------------


def test_non_country_entity_returns_empty() -> None:
    """EcologicalModule must return [] for cohort entities."""
    module = EcologicalModule()
    state = _make_state([_gdp_event()])
    events = module.compute(_cohort_entity(), state, TIMESTEP)
    assert events == []


def test_non_country_institution_returns_empty() -> None:
    """EcologicalModule must return [] for institution-type entities."""
    institution = SimulationEntity(
        id="GRC:CENTRAL_BANK",
        entity_type="institution",
        attributes={},
        metadata={},
    )
    module = EcologicalModule()
    events = module.compute(institution, _make_state([_gdp_event()]), TIMESTEP)
    assert events == []


# ---------------------------------------------------------------------------
# No prior events
# ---------------------------------------------------------------------------


def test_no_prior_events_returns_empty() -> None:
    """EcologicalModule returns [] when state has no prior events."""
    module = EcologicalModule()
    events = module.compute(_country_entity(), _make_state([]), TIMESTEP)
    assert events == []


def test_events_for_different_entity_returns_empty() -> None:
    """Events from a different entity must not trigger output for GRC."""
    module = EcologicalModule()
    state = _make_state([_gdp_event(entity_id="ARG")])
    events = module.compute(_country_entity("GRC"), state, TIMESTEP)
    assert events == []


# ---------------------------------------------------------------------------
# GDP growth → co2_concentration_ppm
# ---------------------------------------------------------------------------


def test_gdp_growth_change_triggers_co2_delta() -> None:
    """gdp_growth_change must produce a co2_concentration_ppm delta."""
    module = EcologicalModule()
    state = _make_state([_gdp_event(magnitude="-0.025")])
    events = module.compute(_country_entity(), state, TIMESTEP)
    assert len(events) == 1
    assert "co2_concentration_ppm" in events[0].affected_attributes


def test_co2_delta_sign_negative_for_contraction() -> None:
    """GDP contraction (negative magnitude) → co2 decreases (negative delta)."""
    module = EcologicalModule()
    state = _make_state([_gdp_event(magnitude="-0.025")])
    events = module.compute(_country_entity(), state, TIMESTEP)
    co2_delta = events[0].affected_attributes["co2_concentration_ppm"].value
    # magnitude=-0.025, elasticity=+0.5 → delta = -0.025 * 0.5 = -0.0125 < 0
    assert co2_delta < Decimal("0"), (
        f"GDP contraction should decrease co2_concentration_ppm; got {co2_delta}"
    )


def test_co2_delta_sign_positive_for_growth() -> None:
    """GDP growth (positive magnitude) → co2 increases (positive delta)."""
    module = EcologicalModule()
    state = _make_state([_gdp_event(magnitude="0.03")])
    events = module.compute(_country_entity(), state, TIMESTEP)
    co2_delta = events[0].affected_attributes["co2_concentration_ppm"].value
    assert co2_delta > Decimal("0"), (
        f"GDP growth should increase co2_concentration_ppm; got {co2_delta}"
    )


def test_co2_uses_stock_variable_type() -> None:
    """co2_concentration_ppm must use VariableType.STOCK (ADR-005 Amendment B)."""
    module = EcologicalModule()
    state = _make_state([_gdp_event()])
    events = module.compute(_country_entity(), state, TIMESTEP)
    co2_qty = events[0].affected_attributes["co2_concentration_ppm"]
    assert co2_qty.variable_type == VariableType.STOCK


def test_co2_uses_canonical_ppm_unit() -> None:
    """co2_concentration_ppm must use unit='ppm' (DATA_STANDARDS.md §Canonical Unit Registry)."""
    module = EcologicalModule()
    state = _make_state([_gdp_event()])
    events = module.compute(_country_entity(), state, TIMESTEP)
    co2_qty = events[0].affected_attributes["co2_concentration_ppm"]
    assert co2_qty.unit == "ppm", (
        f"co2_concentration_ppm must use unit='ppm', got {co2_qty.unit!r}"
    )


# ---------------------------------------------------------------------------
# Fiscal spending → land_use_pressure_index
# ---------------------------------------------------------------------------


def test_fiscal_spending_change_triggers_land_use_delta() -> None:
    """fiscal_policy_spending_change must produce a land_use_pressure_index delta."""
    module = EcologicalModule()
    state = _make_state([_fiscal_event(magnitude="-0.05")])
    events = module.compute(_country_entity(), state, TIMESTEP)
    assert len(events) == 1
    assert "land_use_pressure_index" in events[0].affected_attributes


def test_land_use_pressure_increases_on_fiscal_cut() -> None:
    """Fiscal cut (negative magnitude) → land use pressure increases (positive delta)."""
    module = EcologicalModule()
    state = _make_state([_fiscal_event(magnitude="-0.05")])
    events = module.compute(_country_entity(), state, TIMESTEP)
    land_delta = events[0].affected_attributes["land_use_pressure_index"].value
    # magnitude=-0.05, elasticity=-0.1 → delta = -0.05 * -0.1 = +0.005 > 0
    assert land_delta > Decimal("0"), (
        f"Fiscal cut should increase land_use_pressure_index; got {land_delta}"
    )


def test_land_use_pressure_decreases_on_fiscal_increase() -> None:
    """Fiscal increase (positive magnitude) → land use pressure decreases (negative delta)."""
    module = EcologicalModule()
    state = _make_state([_fiscal_event(magnitude="0.05")])
    events = module.compute(_country_entity(), state, TIMESTEP)
    land_delta = events[0].affected_attributes["land_use_pressure_index"].value
    assert land_delta < Decimal("0"), (
        f"Fiscal increase should decrease land_use_pressure_index; got {land_delta}"
    )


def test_land_use_uses_ratio_variable_type() -> None:
    """land_use_pressure_index must use VariableType.RATIO (ADR-005 Amendment B)."""
    module = EcologicalModule()
    state = _make_state([_fiscal_event()])
    events = module.compute(_country_entity(), state, TIMESTEP)
    land_qty = events[0].affected_attributes["land_use_pressure_index"]
    assert land_qty.variable_type == VariableType.RATIO


def test_land_use_uses_canonical_ratio_0_1_unit() -> None:
    """land_use_pressure_index must use unit='ratio_0_1'.

    Boundary fraction 0–1; ratio_0_1 per DATA_STANDARDS.md §Canonical Unit Registry Gap 1.
    """
    module = EcologicalModule()
    state = _make_state([_fiscal_event()])
    events = module.compute(_country_entity(), state, TIMESTEP)
    land_qty = events[0].affected_attributes["land_use_pressure_index"]
    assert land_qty.unit == "ratio_0_1", (
        f"land_use_pressure_index must use unit='ratio_0_1', got {land_qty.unit!r}"
    )


# ---------------------------------------------------------------------------
# MeasurementFramework.ECOLOGICAL enforcement — Issue #42
# ---------------------------------------------------------------------------


def test_all_emitted_events_have_ecological_framework() -> None:
    """All events emitted by EcologicalModule must carry ECOLOGICAL framework."""
    module = EcologicalModule()
    state = _make_state([_gdp_event(), _fiscal_event()])
    events = module.compute(_country_entity(), state, TIMESTEP)
    assert len(events) >= 1
    for event in events:
        assert event.framework == MeasurementFramework.ECOLOGICAL, (
            f"Expected ECOLOGICAL framework, got {event.framework}"
        )


def test_all_affected_attributes_have_ecological_framework() -> None:
    """All Quantity values in affected_attributes must carry ECOLOGICAL framework."""
    module = EcologicalModule()
    state = _make_state([_gdp_event(), _fiscal_event()])
    events = module.compute(_country_entity(), state, TIMESTEP)
    for event in events:
        for key, qty in event.affected_attributes.items():
            assert qty.measurement_framework == MeasurementFramework.ECOLOGICAL, (
                f"affected_attributes[{key!r}] has framework "
                f"{qty.measurement_framework!r}, expected ECOLOGICAL"
            )


def test_emitted_event_type_is_ecological_indicator_update() -> None:
    """All EcologicalModule events must have event_type='ecological_indicator_update'."""
    module = EcologicalModule()
    state = _make_state([_gdp_event()])
    events = module.compute(_country_entity(), state, TIMESTEP)
    for event in events:
        assert event.event_type == "ecological_indicator_update"


# ---------------------------------------------------------------------------
# get_subscribed_events
# ---------------------------------------------------------------------------


def test_get_subscribed_events_matches_subscribed_events_constant() -> None:
    """get_subscribed_events() must return the same set as _SUBSCRIBED_EVENTS."""
    module = EcologicalModule()
    returned = set(module.get_subscribed_events())
    assert returned == _SUBSCRIBED_EVENTS


def test_subscribed_events_contains_gdp_growth_change() -> None:
    assert "gdp_growth_change" in _SUBSCRIBED_EVENTS


def test_subscribed_events_contains_fiscal_policy_spending_change() -> None:
    assert "fiscal_policy_spending_change" in _SUBSCRIBED_EVENTS


def test_subscribed_events_contains_emergency_declaration() -> None:
    assert "emergency_declaration" in _SUBSCRIBED_EVENTS


def test_subscribed_events_does_not_subscribe_to_monetary_events() -> None:
    """Monetary events are not in scope for EcologicalModule at M6."""
    assert "monetary_policy_policy_rate" not in _SUBSCRIBED_EVENTS


# ---------------------------------------------------------------------------
# Decimal enforcement (no float in affected_attributes)
# ---------------------------------------------------------------------------


def test_co2_delta_value_is_decimal() -> None:
    """co2_concentration_ppm delta must be Decimal, never float."""
    module = EcologicalModule()
    state = _make_state([_gdp_event()])
    events = module.compute(_country_entity(), state, TIMESTEP)
    co2_qty = events[0].affected_attributes["co2_concentration_ppm"]
    assert isinstance(co2_qty.value, Decimal)


def test_land_use_delta_value_is_decimal() -> None:
    """land_use_pressure_index delta must be Decimal, never float."""
    module = EcologicalModule()
    state = _make_state([_fiscal_event()])
    events = module.compute(_country_entity(), state, TIMESTEP)
    land_qty = events[0].affected_attributes["land_use_pressure_index"]
    assert isinstance(land_qty.value, Decimal)


# ---------------------------------------------------------------------------
# Unknown event type produces no delta
# ---------------------------------------------------------------------------


def test_unknown_event_type_produces_no_output() -> None:
    """Events not in ECOLOGICAL_ELASTICITY_REGISTRY produce no indicators."""
    module = EcologicalModule()
    unknown_event = Event(
        event_id="unknown-GRC-2010",
        source_entity_id="GRC",
        event_type="emergency_declaration",  # subscribed but no registry entry
        affected_attributes={
            "emergency_declaration": Quantity(
                value=Decimal("1"),
                unit="dimensionless",
                variable_type=VariableType.DIMENSIONLESS,
                measurement_framework=MeasurementFramework.FINANCIAL,
                confidence_tier=2,
            ),
        },
        propagation_rules=[],
        timestep_originated=datetime(2010, 1, 1, tzinfo=UTC),
        framework=MeasurementFramework.FINANCIAL,
        metadata={},
    )
    state = _make_state([unknown_event])
    events = module.compute(_country_entity(), state, TIMESTEP)
    # emergency_declaration is subscribed but has no registry entry → no output
    assert events == []


# ---------------------------------------------------------------------------
# Elasticity registry
# ---------------------------------------------------------------------------


def test_registry_has_at_least_two_entries() -> None:
    assert len(ECOLOGICAL_ELASTICITY_REGISTRY) >= 2


def test_registry_source_ids_follow_academic_literature_convention() -> None:
    """All source_registry_ids must follow ACADEMIC_LITERATURE_* naming convention."""
    for row in ECOLOGICAL_ELASTICITY_REGISTRY:
        assert row.source_registry_id.startswith("ACADEMIC_LITERATURE_"), (
            f"source_registry_id {row.source_registry_id!r} does not follow"
            f" ACADEMIC_LITERATURE_* convention"
        )


def test_registry_event_types_are_in_subscribed_events() -> None:
    """All registry event types must be in _SUBSCRIBED_EVENTS."""
    for row in ECOLOGICAL_ELASTICITY_REGISTRY:
        assert row.event_type in _SUBSCRIBED_EVENTS, (
            f"Registry event_type {row.event_type!r} not in _SUBSCRIBED_EVENTS"
        )


def test_registry_elasticities_are_decimal() -> None:
    """All registry elasticity values must be Decimal (float prohibition)."""
    for row in ECOLOGICAL_ELASTICITY_REGISTRY:
        assert isinstance(row.elasticity, Decimal), (
            f"elasticity for {row.indicator_key!r} is {type(row.elasticity).__name__}"
        )


def test_registry_confidence_tiers_are_valid() -> None:
    """All registry confidence tiers must be 1–5."""
    for row in ECOLOGICAL_ELASTICITY_REGISTRY:
        assert 1 <= row.confidence_tier <= 5


def test_registry_co2_entry_uses_tier_1() -> None:
    """co2_concentration_ppm entry must have confidence_tier=1 (NASA/NOAA direct measurement)."""
    co2_rows = [
        r for r in ECOLOGICAL_ELASTICITY_REGISTRY
        if r.indicator_key == "co2_concentration_ppm"
    ]
    assert co2_rows, "No co2_concentration_ppm entry in registry"
    for row in co2_rows:
        assert row.confidence_tier == 1, (
            f"co2_concentration_ppm confidence_tier is {row.confidence_tier}, expected 1"
        )


def test_registry_land_use_entry_uses_tier_3() -> None:
    """land_use_pressure_index entry must have confidence_tier=3 (FAO GFR 5-year data)."""
    land_rows = [
        r for r in ECOLOGICAL_ELASTICITY_REGISTRY
        if r.indicator_key == "land_use_pressure_index"
    ]
    assert land_rows, "No land_use_pressure_index entry in registry"
    for row in land_rows:
        assert row.confidence_tier == 3, (
            f"land_use_pressure_index confidence_tier is {row.confidence_tier}, expected 3"
        )


# ---------------------------------------------------------------------------
# Mandatory ecological note — ADR-005 Amendment B
# ---------------------------------------------------------------------------


def test_ecological_mandatory_note_is_defined() -> None:
    """_ECOLOGICAL_MANDATORY_NOTE must be defined in scenarios.py."""
    from app.api.scenarios import _ECOLOGICAL_MANDATORY_NOTE
    assert _ECOLOGICAL_MANDATORY_NOTE
    assert len(_ECOLOGICAL_MANDATORY_NOTE) > 50


def test_ecological_mandatory_note_references_percentile_rank() -> None:
    """Mandatory note must reference 'percentile rank' per ADR-005 Amendment B."""
    from app.api.scenarios import _ECOLOGICAL_MANDATORY_NOTE
    assert "percentile rank" in _ECOLOGICAL_MANDATORY_NOTE


def test_ecological_mandatory_note_references_m6_scope() -> None:
    """Mandatory note must reference 'M6 scope' per ADR-005 Amendment B."""
    from app.api.scenarios import _ECOLOGICAL_MANDATORY_NOTE
    assert "M6 scope" in _ECOLOGICAL_MANDATORY_NOTE


def test_ecological_mandatory_note_references_m8_deferral() -> None:
    """Mandatory note must reference M8 deferral per ADR-005 Amendment B."""
    from app.api.scenarios import _ECOLOGICAL_MANDATORY_NOTE
    assert "M8" in _ECOLOGICAL_MANDATORY_NOTE


def test_ecological_mandatory_note_references_planetary_boundary() -> None:
    """Mandatory note must reference planetary boundary normalization."""
    from app.api.scenarios import _ECOLOGICAL_MANDATORY_NOTE
    assert "Planetary boundary" in _ECOLOGICAL_MANDATORY_NOTE or \
           "planetary boundary" in _ECOLOGICAL_MANDATORY_NOTE


def test_ecological_not_in_unimplemented_frameworks() -> None:
    """'ecological' must NOT be in _UNIMPLEMENTED_FRAMEWORKS after EcologicalModule ships."""
    from app.api.scenarios import _UNIMPLEMENTED_FRAMEWORKS
    assert "ecological" not in _UNIMPLEMENTED_FRAMEWORKS, (
        "'ecological' is still in _UNIMPLEMENTED_FRAMEWORKS — "
        "must be removed when EcologicalModule is wired in"
    )


# ---------------------------------------------------------------------------
# DEBUG log on empty prior_events — Issue #245
# ---------------------------------------------------------------------------


def test_ecological_module_logs_debug_on_no_prior_events(caplog: pytest.LogCaptureFixture) -> None:
    """EcologicalModule must emit a DEBUG log when prior_events is empty (Issue #245)."""
    from app.simulation.engine.models import ResolutionConfig, ScenarioConfig, SimulationState
    from app.simulation.modules.ecological.module import EcologicalModule

    entity = SimulationEntity(
        id="GRC",
        entity_type="country",
        attributes={},
        metadata={},
    )
    state = SimulationState(
        timestep=datetime(2010, 1, 1, tzinfo=UTC),
        resolution=ResolutionConfig(),
        entities={"GRC": entity},
        relationships=[],
        events=[],  # no prior events
        scenario_config=ScenarioConfig(
            scenario_id="test",
            name="Test",
            description="",
            start_date=datetime(2010, 1, 1, tzinfo=UTC),
            end_date=datetime(2013, 1, 1, tzinfo=UTC),
        ),
    )
    module = EcologicalModule()
    with caplog.at_level(logging.DEBUG, logger="app.simulation.modules.ecological.module"):
        result = module.compute(entity, state, datetime(2010, 1, 1, tzinfo=UTC))

    assert result == []
    assert any(
        "no subscribed events" in r.message and "GRC" in r.message
        for r in caplog.records
        if r.levelno == logging.DEBUG
    ), f"Expected DEBUG log naming 'GRC'. Got: {[r.message for r in caplog.records]}"
