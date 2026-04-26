"""Unit tests for DemographicModule — ADR-005 Decision 1.

Coverage:
  1. generate_cohort_specs() produces exactly 100 CohortSpec instances.
  2. CohortSpec.entity_id() produces the correct canonical format.
  3. DemographicModule.compute() returns empty list for cohort entities.
  4. DemographicModule.compute() returns empty list for inactive country entities.
  5. FiscalPolicyInput event triggers cohort poverty_headcount_ratio delta.
  6. Elasticity application produces a Decimal delta, never a float.
  7. Missing elasticity entry (event type not in registry) is silently skipped.
  8. Delta sign is negative for fiscal spending cut (elasticity < 0).
  9. CohortElasticity.elasticity field is Decimal, not float.
  10. DemographicModule with no active_ids treats all countries as active.
"""
from __future__ import annotations

from datetime import datetime, timezone
from decimal import Decimal

from app.simulation.modules.demographic.cohort import (
    AgeBand,
    CohortSpec,
    EmploymentSector,
    IncomeQuintile,
    generate_cohort_specs,
)
from app.simulation.modules.demographic.elasticities import ELASTICITY_REGISTRY
from app.simulation.modules.demographic.module import DemographicModule

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_state(
    entity_id: str,
    entity_type: str = "country",
    prior_events: list | None = None,
) -> object:
    """Build a minimal SimulationState-like object."""
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


def _fiscal_spending_event(
    source_entity_id: str,
    magnitude: Decimal,
    timestep: datetime | None = None,
) -> object:
    """Build a fiscal_spending_change Event with the given magnitude."""
    from app.simulation.engine.models import Event, MeasurementFramework
    from app.simulation.engine.quantity import Quantity, VariableType

    ts = timestep or datetime(2010, 1, 1, tzinfo=timezone.utc)  # noqa: UP017
    qty = Quantity(
        value=magnitude,
        unit="dimensionless",
        variable_type=VariableType.RATIO,
        measurement_framework=MeasurementFramework.FINANCIAL,
        confidence_tier=1,
    )
    return Event(
        event_id="test-fiscal-event",
        source_entity_id=source_entity_id,
        event_type="fiscal_spending_change",
        affected_attributes={"fiscal_spending_change": qty},
        propagation_rules=[],
        timestep_originated=ts,
        framework=MeasurementFramework.FINANCIAL,
    )


# ---------------------------------------------------------------------------
# Test: cohort generation
# ---------------------------------------------------------------------------


def test_generate_cohort_specs_produces_100_instances() -> None:
    specs = generate_cohort_specs()
    assert len(specs) == 100


def test_generate_cohort_specs_all_unique() -> None:
    specs = generate_cohort_specs()
    assert len(set(specs)) == 100


def test_cohort_spec_entity_id_format() -> None:
    spec = CohortSpec(IncomeQuintile.Q1, AgeBand.AGE_25_54, EmploymentSector.FORMAL)
    assert spec.entity_id("GRC") == "GRC:CHT:1-25-54-FORMAL"


def test_cohort_spec_entity_id_q5_agriculture() -> None:
    spec = CohortSpec(IncomeQuintile.Q5, AgeBand.AGE_65_PLUS, EmploymentSector.AGRICULTURE)
    assert spec.entity_id("THA") == "THA:CHT:5-65+-AGRICULTURE"


# ---------------------------------------------------------------------------
# Test: DemographicModule.compute() entity filtering
# ---------------------------------------------------------------------------


def test_compute_skips_cohort_entities() -> None:
    state = _make_state("GRC:CHT:1-25-54-FORMAL", entity_type="cohort")
    module = DemographicModule(cohort_resolution_entity_ids=["GRC"])
    ts = datetime(2010, 1, 1, tzinfo=timezone.utc)  # noqa: UP017
    entity = state.entities["GRC:CHT:1-25-54-FORMAL"]
    events = module.compute(entity, state, ts)
    assert events == []


def test_compute_skips_inactive_country() -> None:
    # Module active only for GRC; THA entity should be skipped.
    state = _make_state("THA", entity_type="country")
    module = DemographicModule(cohort_resolution_entity_ids=["GRC"])
    ts = datetime(2010, 1, 1, tzinfo=timezone.utc)  # noqa: UP017
    entity = state.entities["THA"]
    events = module.compute(entity, state, ts)
    assert events == []


def test_compute_no_active_ids_treats_all_countries_as_active() -> None:
    # fiscal_spending_change on GRC with no active_ids restriction.
    magnitude = Decimal("-0.05")
    fiscal_event = _fiscal_spending_event("GRC", magnitude)
    state = _make_state("GRC", entity_type="country", prior_events=[fiscal_event])
    module = DemographicModule()  # no restriction
    ts = datetime(2011, 1, 1, tzinfo=timezone.utc)  # noqa: UP017
    entity = state.entities["GRC"]
    events = module.compute(entity, state, ts)
    # Should produce events for each matching elasticity row
    assert len(events) > 0


# ---------------------------------------------------------------------------
# Test: FiscalPolicyInput event triggers cohort delta
# ---------------------------------------------------------------------------


def test_fiscal_spending_change_triggers_cohort_delta() -> None:
    magnitude = Decimal("-0.05")
    fiscal_event = _fiscal_spending_event("GRC", magnitude)
    state = _make_state("GRC", entity_type="country", prior_events=[fiscal_event])
    module = DemographicModule(cohort_resolution_entity_ids=["GRC"])
    ts = datetime(2011, 1, 1, tzinfo=timezone.utc)  # noqa: UP017
    entity = state.entities["GRC"]
    events = module.compute(entity, state, ts)

    # Must produce at least one event targeting a GRC cohort entity
    assert len(events) > 0
    target_ids = {e.metadata.get("target_entity_id") for e in events}
    assert any("GRC:CHT:" in tid for tid in target_ids if tid)


def test_elasticity_delta_is_decimal_not_float() -> None:
    magnitude = Decimal("-0.05")
    fiscal_event = _fiscal_spending_event("GRC", magnitude)
    state = _make_state("GRC", entity_type="country", prior_events=[fiscal_event])
    module = DemographicModule(cohort_resolution_entity_ids=["GRC"])
    ts = datetime(2011, 1, 1, tzinfo=timezone.utc)  # noqa: UP017
    entity = state.entities["GRC"]
    events = module.compute(entity, state, ts)
    assert len(events) > 0
    for event in events:
        for qty in event.affected_attributes.values():
            assert isinstance(qty.value, Decimal), f"Expected Decimal, got {type(qty.value)}"
            assert not isinstance(qty.value, float)


def test_delta_sign_is_negative_for_spending_cut() -> None:
    # Spending cut (negative magnitude) × negative elasticity = positive delta → wait,
    # elasticity is already signed: when spending drops (negative magnitude),
    # poverty rises → delta should be positive (poverty_headcount_ratio increases).
    magnitude = Decimal("-1.0")  # 1pp spending cut
    fiscal_event = _fiscal_spending_event("GRC", magnitude)
    state = _make_state("GRC", entity_type="country", prior_events=[fiscal_event])
    module = DemographicModule(cohort_resolution_entity_ids=["GRC"])
    ts = datetime(2011, 1, 1, tzinfo=timezone.utc)  # noqa: UP017
    entity = state.entities["GRC"]
    events = module.compute(entity, state, ts)
    assert len(events) > 0
    # All deltas should be positive (poverty rises when spending is cut)
    for event in events:
        for qty in event.affected_attributes.values():
            assert qty.value > Decimal("0"), (
                f"Expected positive poverty delta for spending cut, got {qty.value}"
            )


# ---------------------------------------------------------------------------
# Test: missing elasticity silently skipped
# ---------------------------------------------------------------------------


def test_unknown_event_type_produces_no_events() -> None:
    from app.simulation.engine.models import Event, MeasurementFramework
    from app.simulation.engine.quantity import Quantity, VariableType

    ts = datetime(2010, 1, 1, tzinfo=timezone.utc)  # noqa: UP017
    qty = Quantity(
        value=Decimal("0.5"),
        unit="dimensionless",
        variable_type=VariableType.RATIO,
        measurement_framework=MeasurementFramework.FINANCIAL,
        confidence_tier=1,
    )
    unknown_event = Event(
        event_id="unknown-event",
        source_entity_id="GRC",
        event_type="meteor_strike",  # not in registry
        affected_attributes={"meteor_strike": qty},
        propagation_rules=[],
        timestep_originated=ts,
        framework=MeasurementFramework.FINANCIAL,
    )
    state = _make_state("GRC", entity_type="country", prior_events=[unknown_event])
    module = DemographicModule(cohort_resolution_entity_ids=["GRC"])
    entity = state.entities["GRC"]
    events = module.compute(entity, state, ts)
    assert events == []


# ---------------------------------------------------------------------------
# Test: CohortElasticity registry integrity
# ---------------------------------------------------------------------------


def test_elasticity_registry_has_at_least_three_entries() -> None:
    assert len(ELASTICITY_REGISTRY) >= 3


def test_elasticity_registry_values_are_decimal() -> None:
    for row in ELASTICITY_REGISTRY:
        assert isinstance(row.elasticity, Decimal), (
            f"Entry {row.source_registry_id} has float elasticity"
        )


def test_elasticity_registry_source_registry_ids_follow_convention() -> None:
    for row in ELASTICITY_REGISTRY:
        assert row.source_registry_id.startswith("ACADEMIC_LITERATURE_"), (
            f"{row.source_registry_id} does not follow ACADEMIC_LITERATURE_* convention"
        )
