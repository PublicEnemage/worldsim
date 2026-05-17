"""Unit tests for GovernanceModule — ADR-005 Decision 6.

Coverage:
  1. Non-country entity returns [].
  2. Country entity with no prior events returns [].
  3. gdp_growth_change triggers rule_of_law_percentile delta.
  4. All emitted events have framework=MeasurementFramework.GOVERNANCE (Issue #42).
  5. get_subscribed_events() matches Decision 6 exactly.
  6. Elasticity delta is Decimal, never float.
  7. imf_program_acceptance triggers democratic_quality_score delta.
  8. Unknown event type produces no events.
  9. GovernanceElasticity.elasticity fields are Decimal, not float.
  10. GOVERNANCE_ELASTICITY_REGISTRY source_registry_id convention.
"""
from __future__ import annotations

import logging
from datetime import datetime, timezone
from decimal import Decimal
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import pytest

from app.simulation.modules.governance.elasticities import GOVERNANCE_ELASTICITY_REGISTRY
from app.simulation.modules.governance.module import _SUBSCRIBED_EVENTS, GovernanceModule

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_state(
    entity_id: str,
    entity_type: str = "country",
    prior_events: list | None = None,
) -> object:
    from app.simulation.engine.models import (
        ResolutionConfig,
        ScenarioConfig,
        SimulationEntity,
        SimulationState,
    )

    ts = datetime(2010, 1, 1, tzinfo=timezone.utc)  # noqa: UP017
    entity = SimulationEntity(
        id=entity_id,
        entity_type=entity_type,
        attributes={},
        metadata={},
    )
    return SimulationState(
        timestep=ts,
        resolution=ResolutionConfig(),
        entities={entity_id: entity},
        relationships=[],
        events=prior_events or [],
        scenario_config=ScenarioConfig(
            scenario_id="test-sid",
            name="Test",
            description="",
            start_date=ts,
            end_date=ts,
        ),
    )


def _gdp_event(source_entity_id: str, magnitude: Decimal) -> object:
    from app.simulation.engine.models import Event, MeasurementFramework
    from app.simulation.engine.quantity import Quantity, VariableType

    ts = datetime(2010, 1, 1, tzinfo=timezone.utc)  # noqa: UP017
    return Event(
        event_id="test-gdp-event",
        source_entity_id=source_entity_id,
        event_type="gdp_growth_change",
        affected_attributes={
            "gdp_growth": Quantity(
                value=magnitude,
                unit="ratio",
                variable_type=VariableType.RATIO,
                measurement_framework=MeasurementFramework.FINANCIAL,
                confidence_tier=2,
            )
        },
        propagation_rules=[],
        timestep_originated=ts,
        framework=MeasurementFramework.FINANCIAL,
    )


def _imf_event(source_entity_id: str) -> object:
    from app.simulation.engine.models import Event, MeasurementFramework
    from app.simulation.engine.quantity import Quantity, VariableType

    ts = datetime(2010, 1, 1, tzinfo=timezone.utc)  # noqa: UP017
    return Event(
        event_id="test-imf-event",
        source_entity_id=source_entity_id,
        event_type="imf_program_acceptance",
        affected_attributes={
            "imf_program_acceptance": Quantity(
                value=Decimal("1.0"),
                unit="dimensionless",
                variable_type=VariableType.DIMENSIONLESS,
                measurement_framework=MeasurementFramework.FINANCIAL,
                confidence_tier=2,
            )
        },
        propagation_rules=[],
        timestep_originated=ts,
        framework=MeasurementFramework.FINANCIAL,
    )


# ---------------------------------------------------------------------------
# Test: entity filtering
# ---------------------------------------------------------------------------


def test_non_country_entity_returns_empty() -> None:
    state = _make_state("GRC:CHT:1-25-54-FORMAL", entity_type="cohort")
    module = GovernanceModule()
    ts = datetime(2011, 1, 1, tzinfo=timezone.utc)  # noqa: UP017
    entity = state.entities["GRC:CHT:1-25-54-FORMAL"]
    assert module.compute(entity, state, ts) == []


def test_country_with_no_prior_events_returns_empty() -> None:
    state = _make_state("GRC", entity_type="country")
    module = GovernanceModule()
    ts = datetime(2011, 1, 1, tzinfo=timezone.utc)  # noqa: UP017
    assert module.compute(state.entities["GRC"], state, ts) == []


# ---------------------------------------------------------------------------
# Test: gdp_growth_change → rule_of_law_percentile
# ---------------------------------------------------------------------------


def test_gdp_contraction_triggers_rule_of_law_delta() -> None:
    gdp_ev = _gdp_event("GRC", Decimal("-0.05"))
    state = _make_state("GRC", entity_type="country", prior_events=[gdp_ev])
    module = GovernanceModule()
    ts = datetime(2011, 1, 1, tzinfo=timezone.utc)  # noqa: UP017
    events = module.compute(state.entities["GRC"], state, ts)
    assert len(events) == 1
    assert "rule_of_law_percentile" in events[0].affected_attributes


def test_gdp_contraction_rule_of_law_delta_sign() -> None:
    # GDP contraction (negative) × negative elasticity → positive delta
    # means rule_of_law worsens (score decreases — positive delta applied downward).
    # elasticity is -0.08, magnitude is -0.05: delta = (-0.05 * -0.08) = +0.004
    gdp_ev = _gdp_event("GRC", Decimal("-0.05"))
    state = _make_state("GRC", entity_type="country", prior_events=[gdp_ev])
    module = GovernanceModule()
    ts = datetime(2011, 1, 1, tzinfo=timezone.utc)  # noqa: UP017
    events = module.compute(state.entities["GRC"], state, ts)
    qty = events[0].affected_attributes["rule_of_law_percentile"]
    assert qty.value > Decimal("0"), (
        f"Expected positive delta for GDP contraction, got {qty.value}"
    )


# ---------------------------------------------------------------------------
# Test: imf_program_acceptance → democratic_quality_score
# ---------------------------------------------------------------------------


def test_imf_acceptance_triggers_democratic_quality_delta() -> None:
    imf_ev = _imf_event("GRC")
    state = _make_state("GRC", entity_type="country", prior_events=[imf_ev])
    module = GovernanceModule()
    ts = datetime(2011, 1, 1, tzinfo=timezone.utc)  # noqa: UP017
    events = module.compute(state.entities["GRC"], state, ts)
    assert len(events) == 1
    assert "democratic_quality_score" in events[0].affected_attributes


# ---------------------------------------------------------------------------
# Test: MeasurementFramework.GOVERNANCE tagging (Issue #42)
# ---------------------------------------------------------------------------


def test_all_emitted_events_have_governance_framework() -> None:
    from app.simulation.engine.models import MeasurementFramework
    gdp_ev = _gdp_event("GRC", Decimal("-0.03"))
    state = _make_state("GRC", entity_type="country", prior_events=[gdp_ev])
    module = GovernanceModule()
    ts = datetime(2011, 1, 1, tzinfo=timezone.utc)  # noqa: UP017
    events = module.compute(state.entities["GRC"], state, ts)
    assert len(events) > 0
    assert all(e.framework == MeasurementFramework.GOVERNANCE for e in events)


def test_all_affected_attributes_have_governance_framework() -> None:
    from app.simulation.engine.models import MeasurementFramework
    gdp_ev = _gdp_event("GRC", Decimal("-0.03"))
    state = _make_state("GRC", entity_type="country", prior_events=[gdp_ev])
    module = GovernanceModule()
    ts = datetime(2011, 1, 1, tzinfo=timezone.utc)  # noqa: UP017
    events = module.compute(state.entities["GRC"], state, ts)
    for event in events:
        for qty in event.affected_attributes.values():
            assert qty.measurement_framework == MeasurementFramework.GOVERNANCE


# ---------------------------------------------------------------------------
# Test: get_subscribed_events matches Decision 6
# ---------------------------------------------------------------------------


def test_get_subscribed_events_matches_decision_6() -> None:
    expected = {
        "gdp_growth_change",
        "fiscal_policy_spending_change",
        "imf_program_acceptance",
        "emergency_declaration",
    }
    module = GovernanceModule()
    assert set(module.get_subscribed_events()) == expected


def test_subscribed_events_constant_matches_decision_6() -> None:
    expected = {
        "gdp_growth_change",
        "fiscal_policy_spending_change",
        "imf_program_acceptance",
        "emergency_declaration",
    }
    assert expected == _SUBSCRIBED_EVENTS


# ---------------------------------------------------------------------------
# Test: Decimal type enforcement
# ---------------------------------------------------------------------------


def test_elasticity_delta_is_decimal_not_float() -> None:
    gdp_ev = _gdp_event("GRC", Decimal("-0.05"))
    state = _make_state("GRC", entity_type="country", prior_events=[gdp_ev])
    module = GovernanceModule()
    ts = datetime(2011, 1, 1, tzinfo=timezone.utc)  # noqa: UP017
    events = module.compute(state.entities["GRC"], state, ts)
    assert len(events) > 0
    for event in events:
        for qty in event.affected_attributes.values():
            assert isinstance(qty.value, Decimal), f"Expected Decimal, got {type(qty.value)}"
            assert not isinstance(qty.value, float)


def test_rule_of_law_uses_canonical_percentile_0_100_unit() -> None:
    """rule_of_law_percentile must use unit='percentile_0_100' (DATA_STANDARDS.md §Canonical Unit Registry)."""
    gdp_ev = _gdp_event("GRC", Decimal("-0.05"))
    state = _make_state("GRC", entity_type="country", prior_events=[gdp_ev])
    module = GovernanceModule()
    ts = datetime(2011, 1, 1, tzinfo=timezone.utc)  # noqa: UP017
    events = module.compute(state.entities["GRC"], state, ts)
    assert len(events) == 1
    qty = events[0].affected_attributes["rule_of_law_percentile"]
    assert qty.unit == "percentile_0_100", (
        f"rule_of_law_percentile must use unit='percentile_0_100', got {qty.unit!r}"
    )


def test_democratic_quality_score_uses_canonical_ratio_0_1_unit() -> None:
    """democratic_quality_score must use unit='ratio_0_1' (V-Dem LDI is 0–1 scale)."""
    imf_ev = _imf_event("GRC")
    state = _make_state("GRC", entity_type="country", prior_events=[imf_ev])
    module = GovernanceModule()
    ts = datetime(2011, 1, 1, tzinfo=timezone.utc)  # noqa: UP017
    events = module.compute(state.entities["GRC"], state, ts)
    assert len(events) == 1
    qty = events[0].affected_attributes["democratic_quality_score"]
    assert qty.unit == "ratio_0_1", (
        f"democratic_quality_score must use unit='ratio_0_1', got {qty.unit!r}"
    )


def test_registry_elasticities_are_decimal() -> None:
    for row in GOVERNANCE_ELASTICITY_REGISTRY:
        assert isinstance(row.elasticity, Decimal), (
            f"Entry {row.source_registry_id} has non-Decimal elasticity"
        )


# ---------------------------------------------------------------------------
# Test: unknown event type produces no events
# ---------------------------------------------------------------------------


def test_unknown_event_type_produces_no_events() -> None:
    from app.simulation.engine.models import Event, MeasurementFramework
    from app.simulation.engine.quantity import Quantity, VariableType

    ts = datetime(2010, 1, 1, tzinfo=timezone.utc)  # noqa: UP017
    unknown_event = Event(
        event_id="unknown-event",
        source_entity_id="GRC",
        event_type="meteor_strike",
        affected_attributes={
            "meteor_strike": Quantity(
                value=Decimal("1.0"),
                unit="dimensionless",
                variable_type=VariableType.DIMENSIONLESS,
                measurement_framework=MeasurementFramework.FINANCIAL,
                confidence_tier=1,
            )
        },
        propagation_rules=[],
        timestep_originated=ts,
        framework=MeasurementFramework.FINANCIAL,
    )
    state = _make_state("GRC", entity_type="country", prior_events=[unknown_event])
    module = GovernanceModule()
    assert module.compute(state.entities["GRC"], state, ts) == []


# ---------------------------------------------------------------------------
# Test: elasticity registry integrity
# ---------------------------------------------------------------------------


def test_registry_has_at_least_two_entries() -> None:
    assert len(GOVERNANCE_ELASTICITY_REGISTRY) >= 2


def test_registry_source_registry_ids_follow_convention() -> None:
    for row in GOVERNANCE_ELASTICITY_REGISTRY:
        assert row.source_registry_id.startswith("ACADEMIC_LITERATURE_"), (
            f"{row.source_registry_id} does not follow ACADEMIC_LITERATURE_* convention"
        )


def test_registry_event_types_are_subscribed() -> None:
    for row in GOVERNANCE_ELASTICITY_REGISTRY:
        assert row.event_type in _SUBSCRIBED_EVENTS, (
            f"Registry entry event_type '{row.event_type}' not in _SUBSCRIBED_EVENTS"
        )


# ---------------------------------------------------------------------------
# DEBUG log on empty prior_events — Issue #245
# ---------------------------------------------------------------------------


def test_governance_module_logs_debug_on_no_prior_events(caplog: pytest.LogCaptureFixture) -> None:
    """GovernanceModule must emit a DEBUG log when prior_events is empty (Issue #245)."""
    ts = datetime(2010, 1, 1, tzinfo=timezone.utc)  # noqa: UP017
    state = _make_state("GRC", prior_events=[])
    module = GovernanceModule()
    entity = state.entities["GRC"]
    with caplog.at_level(logging.DEBUG, logger="app.simulation.modules.governance.module"):
        result = module.compute(entity, state, ts)

    assert result == []
    assert any(
        "no subscribed events" in r.message and "GRC" in r.message
        for r in caplog.records
        if r.levelno == logging.DEBUG
    ), f"Expected DEBUG log naming 'GRC'. Got: {[r.message for r in caplog.records]}"
