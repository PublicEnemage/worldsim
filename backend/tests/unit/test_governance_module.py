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
        # EmergencyPolicyInput.to_events() emits "emergency_policy_{instrument.value}",
        # so IMF_PROGRAM_ACCEPTANCE → "emergency_policy_imf_program_acceptance".
        event_type="emergency_policy_imf_program_acceptance",
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
# Test: emergency_declaration → democratic_quality_score (ADR-005 Amendment 4)
# ---------------------------------------------------------------------------


def _emergency_event(source_entity_id: str) -> object:
    from app.simulation.engine.models import Event, MeasurementFramework
    from app.simulation.engine.quantity import Quantity, VariableType

    ts = datetime(2014, 1, 1, tzinfo=timezone.utc)  # noqa: UP017
    return Event(
        event_id="test-emergency-event",
        source_entity_id=source_entity_id,
        # EmergencyPolicyInput.to_events() emits "emergency_policy_{instrument.value}",
        # so EMERGENCY_DECLARATION → "emergency_policy_emergency_declaration".
        event_type="emergency_policy_emergency_declaration",
        affected_attributes={
            "emergency_declaration": Quantity(
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


def test_emergency_declaration_triggers_democratic_quality_delta() -> None:
    """emergency_declaration → democratic_quality_score delta (ADR-005 Amendment 4)."""
    emg_ev = _emergency_event("GRC")
    state = _make_state("GRC", entity_type="country", prior_events=[emg_ev])
    module = GovernanceModule()
    ts = datetime(2015, 1, 1, tzinfo=timezone.utc)  # noqa: UP017
    events = module.compute(state.entities["GRC"], state, ts)
    assert len(events) == 1
    assert "democratic_quality_score" in events[0].affected_attributes


def test_emergency_declaration_democratic_quality_delta_is_negative() -> None:
    """Emergency declaration reduces democratic quality (elasticity = -0.05)."""
    emg_ev = _emergency_event("GRC")
    state = _make_state("GRC", entity_type="country", prior_events=[emg_ev])
    module = GovernanceModule()
    ts = datetime(2015, 1, 1, tzinfo=timezone.utc)  # noqa: UP017
    events = module.compute(state.entities["GRC"], state, ts)
    qty = events[0].affected_attributes["democratic_quality_score"]
    assert qty.value < Decimal("0"), (
        f"Expected negative delta for emergency_declaration, got {qty.value}"
    )


def test_emergency_declaration_delta_magnitude() -> None:
    """delta = +1.0 × -0.05 = -0.05 on democratic_quality_score."""
    emg_ev = _emergency_event("GRC")
    state = _make_state("GRC", entity_type="country", prior_events=[emg_ev])
    module = GovernanceModule()
    ts = datetime(2015, 1, 1, tzinfo=timezone.utc)  # noqa: UP017
    events = module.compute(state.entities["GRC"], state, ts)
    qty = events[0].affected_attributes["democratic_quality_score"]
    assert qty.value == Decimal("-0.05"), (
        f"Expected delta -0.05, got {qty.value}"
    )


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
    # Event types match EmergencyPolicyInput.to_events() output format:
    # "emergency_policy_{instrument.value}" not the bare instrument name.
    expected = {
        "gdp_growth_change",
        "fiscal_policy_spending_change",
        "emergency_policy_imf_program_acceptance",
        "emergency_policy_emergency_declaration",
    }
    module = GovernanceModule()
    assert set(module.get_subscribed_events()) == expected


def test_subscribed_events_constant_matches_decision_6() -> None:
    expected = {
        "gdp_growth_change",
        "fiscal_policy_spending_change",
        "emergency_policy_imf_program_acceptance",
        "emergency_policy_emergency_declaration",
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
    """rule_of_law_percentile must use unit='percentile_0_100'.

    WGI percentile rank 0–100; canonical unit per DATA_STANDARDS.md §Canonical Unit Registry.
    """
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


def test_registry_has_at_least_three_entries() -> None:
    """M10 promotion: registry must cover ≥ 3 event-indicator pairs (Issue #556 Criterion 2)."""
    assert len(GOVERNANCE_ELASTICITY_REGISTRY) >= 3


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


def test_registry_has_four_entries() -> None:
    """AC-1275-2: M17-G7 adds fourth entry — fiscal_policy_spending_change → institutional_capacity_index."""
    assert len(GOVERNANCE_ELASTICITY_REGISTRY) >= 4, (
        f"Expected ≥4 registry entries after M17-G7. Got {len(GOVERNANCE_ELASTICITY_REGISTRY)}. "
        "Missing: fiscal_policy_spending_change → institutional_capacity_index (Gupta 2002, T3)."
    )


def test_registry_contains_fiscal_spending_to_institutional_capacity() -> None:
    """AC-1275-2: Registry must contain CM-certified entry per M17-G7 intent doc."""
    from decimal import Decimal
    matches = [
        row for row in GOVERNANCE_ELASTICITY_REGISTRY
        if row.event_type == "fiscal_policy_spending_change"
        and row.indicator_key == "institutional_capacity_index"
    ]
    assert len(matches) == 1, (
        f"Expected exactly 1 entry for fiscal_policy_spending_change → institutional_capacity_index. "
        f"Got {len(matches)}."
    )
    row = matches[0]
    assert row.elasticity == Decimal("-0.015"), (
        f"CM-certified elasticity is Decimal('-0.015'). Got {row.elasticity!r}."
    )
    assert row.confidence_tier == 3, (
        f"Gupta 2002 SSA cross-country inference is T3. Got tier {row.confidence_tier}."
    )
    assert row.source_registry_id == "ACADEMIC_LITERATURE_GUPTA_2002_IMF_WP_INSTITUTIONAL_CAPACITY", (
        f"Source registry ID mismatch. Got {row.source_registry_id!r}."
    )


def test_indicator_units_contains_institutional_capacity_index() -> None:
    """AC-1275-5: _INDICATOR_UNITS must register institutional_capacity_index as ratio_0_1."""
    from app.simulation.modules.governance.module import _INDICATOR_UNITS
    assert "institutional_capacity_index" in _INDICATOR_UNITS, (
        "_INDICATOR_UNITS missing 'institutional_capacity_index'. "
        "CPIA normalized [0,1] — unit must be 'ratio_0_1'."
    )
    assert _INDICATOR_UNITS["institutional_capacity_index"] == "ratio_0_1", (
        f"Expected unit 'ratio_0_1' for institutional_capacity_index. "
        f"Got {_INDICATOR_UNITS['institutional_capacity_index']!r}."
    )


def test_existing_registry_entries_unchanged_after_m17_g7() -> None:
    """AC-1275-R: Existing three entries unchanged — gdp/rl, imf/dq, emergency/dq."""
    from decimal import Decimal
    existing = {
        (row.event_type, row.indicator_key): row
        for row in GOVERNANCE_ELASTICITY_REGISTRY
    }
    gdp_rl = existing.get(("gdp_growth_change", "rule_of_law_percentile"))
    assert gdp_rl is not None, "gdp_growth_change → rule_of_law_percentile entry missing"
    assert gdp_rl.elasticity == Decimal("-0.08"), (
        f"gdp→rl elasticity changed. Expected -0.08, got {gdp_rl.elasticity!r}"
    )
    assert gdp_rl.confidence_tier == 2

    imf_dq = existing.get(("emergency_policy_imf_program_acceptance", "democratic_quality_score"))
    assert imf_dq is not None, "imf_program_acceptance → democratic_quality_score entry missing"
    assert imf_dq.elasticity == Decimal("0.005"), (
        f"imf→dq elasticity changed. Expected 0.005, got {imf_dq.elasticity!r}"
    )

    emg_dq = existing.get(("emergency_policy_emergency_declaration", "democratic_quality_score"))
    assert emg_dq is not None, "emergency_declaration → democratic_quality_score entry missing"
    assert emg_dq.elasticity == Decimal("-0.05"), (
        f"emergency→dq elasticity changed. Expected -0.05, got {emg_dq.elasticity!r}"
    )


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
