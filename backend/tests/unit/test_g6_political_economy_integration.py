"""Tests for ADR-013 G6 political economy integration.

Covers acceptance criteria AC-1 through AC-6 from
docs/process/intents/ADR-013-2026-06-12-political-economy-integration.md

AC-1: programme_survival_probability appears in political_economy framework indicators
AC-2: conditionality_term_* indicators appear when CONDITIONALITY events present
AC-3: PE-001 MDA alert in events_snapshot when probability < 0.25
AC-4: elite_capture_divergence_index appears when elite_capture_coefficient seeded
AC-5: political_economy is a top-level framework key in measurement output
AC-6: conditionality_term_* absent when no CONDITIONALITY events
"""
from __future__ import annotations

from datetime import UTC, datetime
from decimal import Decimal

from app.simulation.engine.models import (
    Event,
    MeasurementFramework,
    ResolutionConfig,
    ScenarioConfig,
    SimulationEntity,
    SimulationState,
)
from app.simulation.engine.quantity import Quantity, VariableType
from app.simulation.modules.political_economy.module import (
    PROGRAMME_SURVIVAL_FLOOR,
    PoliticalEconomyModule,
    _aggregate_conditionality_terms,
    _compute_composite_score,
    _compute_elite_capture_indicators,
    _compute_survival_probability,
)

_EPOCH = datetime(2010, 1, 1, tzinfo=UTC)
_SCENARIO_CONFIG = ScenarioConfig(
    scenario_id="test-g6",
    name="G6 Test",
    description="",
    start_date=_EPOCH,
    end_date=datetime(2020, 1, 1, tzinfo=UTC),
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _qty(
    value: str,
    unit: str = "ratio",
    framework: str = "financial",
    variable_type: VariableType = VariableType.RATIO,
    confidence_tier: int = 2,
) -> Quantity:
    return Quantity(
        value=Decimal(value),
        unit=unit,
        variable_type=variable_type,
        measurement_framework=MeasurementFramework(framework),
        confidence_tier=confidence_tier,
    )


def _entity(
    entity_id: str = "GRC",
    entity_type: str = "country",
    **attrs: str,
) -> SimulationEntity:
    return SimulationEntity(
        id=entity_id,
        entity_type=entity_type,
        attributes={k: _qty(v) for k, v in attrs.items()},
        metadata={},
    )


def _state(entity: SimulationEntity, events: list[Event] | None = None) -> SimulationState:
    return SimulationState(
        timestep=_EPOCH,
        resolution=ResolutionConfig(),
        entities={entity.id: entity},
        relationships=[],
        events=events or [],
        scenario_config=_SCENARIO_CONFIG,
    )


def _fiscal_event(
    entity_id: str = "GRC",
    event_type: str = "fiscal_policy_spending_change",
    value: str = "-0.08",
) -> Event:
    return Event(
        event_id=f"test-fiscal-{entity_id}-{value}",
        source_entity_id=entity_id,
        event_type=event_type,
        affected_attributes={"spending_change": _qty(value)},
        propagation_rules=[],
        timestep_originated=_EPOCH,
        framework=MeasurementFramework.FINANCIAL,
    )


def _conditionality_event(
    entity_id: str = "GRC",
    actor_id: str = "IMF",
    mechanism: str = "FISCAL_CONSOLIDATION",
    fiscal_delta: str = "-0.05",
    event_type: str = "fiscal_policy_spending_change",
) -> Event:
    """Simulate an event injected by a CONDITIONALITY ControlInput (with metadata)."""
    return Event(
        event_id=f"test-cond-{entity_id}-{actor_id}-{mechanism}",
        source_entity_id=entity_id,
        event_type=event_type,
        affected_attributes={"spending_change": _qty(fiscal_delta)},
        propagation_rules=[],
        timestep_originated=_EPOCH,
        framework=MeasurementFramework.FINANCIAL,
        metadata={
            "input_source": "conditionality",
            "constraining_actor_id": actor_id,
            "constraint_mechanism": mechanism,
            "implementation_capacity": "1.0",
        },
    )


# ---------------------------------------------------------------------------
# AC-1: programme_survival_probability in political_economy framework
# ---------------------------------------------------------------------------


def test_ac1_programme_survival_probability_emitted_for_entity_with_legitimacy() -> None:
    """AC-1: programme_survival_probability in political_economy framework indicators."""
    entity = _entity("GRC", legitimacy_index="0.4")
    fiscal_evt = _fiscal_event("GRC", value="-0.08")
    state = _state(entity, [fiscal_evt])
    module = PoliticalEconomyModule()
    events = module.compute(entity, state, _EPOCH)

    survival_events = [
        e for e in events if "programme_survival_probability" in e.affected_attributes
    ]
    assert survival_events, "No programme_survival_probability event emitted"

    evt = survival_events[0]
    qty = evt.affected_attributes["programme_survival_probability"]

    assert qty.measurement_framework == MeasurementFramework.POLITICAL_ECONOMY, (
        f"Expected POLITICAL_ECONOMY, got {qty.measurement_framework}"
    )
    assert qty.variable_type == VariableType.PROBABILITY, (
        f"Expected PROBABILITY, got {qty.variable_type}"
    )
    assert qty.confidence_tier == 3
    assert Decimal("0.01") <= qty.value <= Decimal("0.99"), (
        f"programme_survival_probability out of [0.01, 0.99]: {qty.value}"
    )


def test_ac1_survival_probability_formula_values() -> None:
    """programme_survival_probability is computed from legitimacy via the formula."""
    prob_high_legitimacy = _compute_survival_probability(Decimal("0.8"))
    prob_low_legitimacy = _compute_survival_probability(Decimal("0.2"))

    assert prob_high_legitimacy > prob_low_legitimacy, (
        "Higher legitimacy should yield higher survival probability"
    )
    assert Decimal("0.01") <= prob_low_legitimacy <= Decimal("0.99")
    assert Decimal("0.01") <= prob_high_legitimacy <= Decimal("0.99")


# ---------------------------------------------------------------------------
# AC-2: conditionality_term_* indicators when CONDITIONALITY events present
# ---------------------------------------------------------------------------


def test_ac2_conditionality_term_indicator_emitted() -> None:
    """AC-2: conditionality_term_IMF_FISCAL_CONSOLIDATION indicator present."""
    entity = _entity("GRC", legitimacy_index="0.4")
    cond_evt = _conditionality_event("GRC", "IMF", "FISCAL_CONSOLIDATION", "-0.05")
    state = _state(entity, [cond_evt])
    module = PoliticalEconomyModule()
    events = module.compute(entity, state, _EPOCH)

    cond_events = [
        e for e in events if e.event_type == "conditionality_term_attribution"
    ]
    assert cond_events, "No conditionality attribution event emitted"

    indicator_keys = set()
    for e in cond_events:
        indicator_keys.update(e.affected_attributes.keys())

    assert "conditionality_term_IMF_FISCAL_CONSOLIDATION" in indicator_keys, (
        f"Expected conditionality_term_IMF_FISCAL_CONSOLIDATION, got {indicator_keys}"
    )


def test_ac2_two_conditionality_terms_both_attributed() -> None:
    """Two different conditionality terms produce two separate indicators."""
    entity = _entity("GRC", legitimacy_index="0.4")
    evt1 = _conditionality_event("GRC", "IMF", "FISCAL_CONSOLIDATION", "-0.05")
    evt2 = _conditionality_event("GRC", "IMF", "PENSION_CUT", "-0.03")
    state = _state(entity, [evt1, evt2])
    module = PoliticalEconomyModule()
    events = module.compute(entity, state, _EPOCH)

    cond_attr_keys: set[str] = set()
    for e in events:
        if e.event_type == "conditionality_term_attribution":
            cond_attr_keys.update(e.affected_attributes.keys())

    assert "conditionality_term_IMF_FISCAL_CONSOLIDATION" in cond_attr_keys
    assert "conditionality_term_IMF_PENSION_CUT" in cond_attr_keys


def test_ac2_conditionality_values_are_absolute_effective_delta() -> None:
    """Conditionality indicator values are absolute (non-negative) effective deltas."""
    entity = _entity("GRC", legitimacy_index="0.4")
    cond_evt = _conditionality_event("GRC", "IMF", "FISCAL_CONSOLIDATION", "-0.05")
    state = _state(entity, [cond_evt])
    module = PoliticalEconomyModule()
    events = module.compute(entity, state, _EPOCH)

    for e in events:
        if e.event_type == "conditionality_term_attribution":
            for qty in e.affected_attributes.values():
                assert qty.value >= Decimal("0"), (
                    f"Conditionality indicator value must be non-negative: {qty.value}"
                )


# ---------------------------------------------------------------------------
# AC-3: PE-001 MDA fires when programme_survival_probability < 0.25
# ---------------------------------------------------------------------------


def test_ac3_programme_survival_floor_constant() -> None:
    """PROGRAMME_SURVIVAL_FLOOR is 0.25 per ADR-013 Decision 1."""
    assert Decimal("0.25") == PROGRAMME_SURVIVAL_FLOOR, (
        "PROGRAMME_SURVIVAL_FLOOR must be 0.25 — cannot change without ADR amendment"
    )


def test_ac3_survival_probability_below_floor_for_acute_crisis() -> None:
    """Survival probability computation produces value below 0.25 for acute crisis conditions.

    This verifies that the formula can produce sub-floor values.
    The MDA alert itself is verified by the mda_checker integration tests.
    """
    prob = _compute_survival_probability(Decimal("0.0"))
    assert prob < PROGRAMME_SURVIVAL_FLOOR, (
        f"At legitimacy=0, survival {prob} should be < floor {PROGRAMME_SURVIVAL_FLOOR}"
    )


def test_ac3_survival_probability_above_floor_for_stable_government() -> None:
    """Survival probability is above 0.25 for a legitimacy-stable government."""
    prob = _compute_survival_probability(Decimal("0.8"))
    assert prob > PROGRAMME_SURVIVAL_FLOOR


# ---------------------------------------------------------------------------
# AC-4: elite_capture_divergence_index when elite_capture_coefficient seeded
# ---------------------------------------------------------------------------


def test_ac4_elite_capture_divergence_index_emitted() -> None:
    """AC-4: elite_capture_divergence_index present when elite_capture_coefficient seeded."""
    entity = SimulationEntity(
        id="GRC",
        entity_type="country",
        attributes={
            "legitimacy_index": _qty("0.5"),
            "elite_capture_coefficient": _qty("0.3"),
        },
        metadata={},
    )
    fiscal_evt = _fiscal_event("GRC", value="-0.08")
    state = _state(entity, [fiscal_evt])
    module = PoliticalEconomyModule()
    events = module.compute(entity, state, _EPOCH)

    capture_events = [
        e for e in events if e.event_type == "elite_capture_update"
    ]
    assert capture_events, "No elite_capture_update event emitted"

    attr_keys: set[str] = set()
    for e in capture_events:
        attr_keys.update(e.affected_attributes.keys())

    assert "elite_capture_divergence_index" in attr_keys, (
        f"Missing elite_capture_divergence_index in {attr_keys}"
    )
    assert "elite_capture_divergence_top_quintile" in attr_keys
    assert "elite_capture_divergence_bottom_quintile" in attr_keys


def test_ac4_elite_capture_index_framework_and_tier() -> None:
    """Elite capture indicators use POLITICAL_ECONOMY framework, tier 3."""
    entity = SimulationEntity(
        id="GRC",
        entity_type="country",
        attributes={
            "legitimacy_index": _qty("0.5"),
            "elite_capture_coefficient": _qty("0.3"),
        },
        metadata={},
    )
    fiscal_evt = _fiscal_event("GRC", value="-0.08")
    state = _state(entity, [fiscal_evt])
    module = PoliticalEconomyModule()
    events = module.compute(entity, state, _EPOCH)

    for evt in events:
        if evt.event_type == "elite_capture_update":
            for key, qty in evt.affected_attributes.items():
                assert qty.measurement_framework == MeasurementFramework.POLITICAL_ECONOMY, (
                    f"{key}: expected POLITICAL_ECONOMY, got {qty.measurement_framework}"
                )
                assert qty.confidence_tier == 3, (
                    f"{key}: expected tier 3, got {qty.confidence_tier}"
                )


def test_ac4_elite_capture_index_no_divergence_at_population_share() -> None:
    """Index = 1.0 when capture_coeff equals elite population share (0.20)."""
    index, top_q, bottom_q = _compute_elite_capture_indicators(Decimal("0.20"))
    assert index == Decimal("1.0"), f"Expected 1.0, got {index}"
    assert top_q == Decimal("0.20")


def test_ac4_elite_capture_index_below_one_not_possible() -> None:
    """Index cannot be below 1.0 per ADR-013 Decision 3 known limitation."""
    index, _, _ = _compute_elite_capture_indicators(Decimal("0.05"))
    assert index >= Decimal("1.0"), f"Index {index} is below 1.0 — violates ADR constraint"


def test_ac4_elite_capture_index_double_at_twice_population_share() -> None:
    """Index = 2.0 when top quintile captures 40% of benefits (twice 20% share)."""
    index, top_q, _ = _compute_elite_capture_indicators(Decimal("0.40"))
    assert index == Decimal("2.0"), f"Expected 2.0, got {index}"
    assert top_q == Decimal("0.40")


# ---------------------------------------------------------------------------
# AC-5: political_economy is a top-level framework key
# ---------------------------------------------------------------------------


def test_ac5_political_economy_framework_in_measurement_framework_enum() -> None:
    """MeasurementFramework.POLITICAL_ECONOMY exists and has value 'political_economy'."""
    fw = MeasurementFramework.POLITICAL_ECONOMY
    assert fw.value == "political_economy"


def test_ac5_probability_variable_type_exists() -> None:
    """VariableType.PROBABILITY exists and has value 'probability'."""
    vt = VariableType.PROBABILITY
    assert vt.value == "probability"


def test_ac5_political_economy_indicators_use_correct_framework() -> None:
    """All political_economy module indicators use POLITICAL_ECONOMY framework."""
    entity = SimulationEntity(
        id="GRC",
        entity_type="country",
        attributes={
            "legitimacy_index": _qty("0.4"),
            "elite_capture_coefficient": _qty("0.3"),
        },
        metadata={},
    )
    fiscal_evt = _fiscal_event("GRC", value="-0.08")
    cond_evt = _conditionality_event("GRC", "IMF", "FISCAL_CONSOLIDATION", "-0.05")
    state = _state(entity, [fiscal_evt, cond_evt])
    module = PoliticalEconomyModule()
    events = module.compute(entity, state, _EPOCH)

    pe_events = [
        e for e in events
        if e.framework == MeasurementFramework.POLITICAL_ECONOMY
    ]
    pe_attr_keys: set[str] = set()
    for e in pe_events:
        pe_attr_keys.update(e.affected_attributes.keys())

    assert "programme_survival_probability" in pe_attr_keys
    assert "political_economy_composite_score" in pe_attr_keys
    assert any(k.startswith("conditionality_term_") for k in pe_attr_keys)


# ---------------------------------------------------------------------------
# AC-6: conditionality_term_* absent when no CONDITIONALITY events
# ---------------------------------------------------------------------------


def test_ac6_no_conditionality_indicators_without_conditionality_events() -> None:
    """AC-6: no conditionality_term_* indicators for non-conditionality scenarios."""
    entity = _entity("GRC", legitimacy_index="0.4")
    fiscal_evt = _fiscal_event("GRC", value="-0.08")  # plain fiscal, not conditionality
    state = _state(entity, [fiscal_evt])
    module = PoliticalEconomyModule()
    events = module.compute(entity, state, _EPOCH)

    cond_attr_keys = [
        k
        for e in events
        for k in e.affected_attributes
        if k.startswith("conditionality_term_")
    ]
    assert cond_attr_keys == [], (
        f"Conditionality indicators must be absent without CONDITIONALITY inputs: {cond_attr_keys}"
    )


def test_ac6_non_conditionality_event_without_metadata_produces_no_attribution() -> None:
    """Events without conditionality metadata are not attributed as conditionality terms."""
    entity = _entity("GRC", legitimacy_index="0.4")
    plain_evt = Event(
        event_id="plain-fiscal",
        source_entity_id="GRC",
        event_type="fiscal_policy_spending_change",
        affected_attributes={"spending_change": _qty("-0.05")},
        propagation_rules=[],
        timestep_originated=_EPOCH,
        framework=MeasurementFramework.FINANCIAL,
        metadata={},  # no input_source key
    )
    state = _state(entity, [plain_evt])
    module = PoliticalEconomyModule()
    events = module.compute(entity, state, _EPOCH)

    cond_attr_keys = [
        k
        for e in events
        for k in e.affected_attributes
        if k.startswith("conditionality_term_")
    ]
    assert cond_attr_keys == []


# ---------------------------------------------------------------------------
# Conditionality metadata injection via ControlInput.get_events()
# ---------------------------------------------------------------------------


def test_conditionality_metadata_injected_into_events() -> None:
    """CONDITIONALITY inputs inject metadata into events (ADR-013 Decision 2 prerequisite)."""
    from datetime import UTC, datetime

    from app.simulation.orchestration.inputs import (
        FiscalInstrument,
        FiscalPolicyInput,
        InputSource,
    )

    inp = FiscalPolicyInput(
        actor_id="IMF",
        actor_role="creditor",
        target_entity="GRC",
        effective_date=datetime(2010, 1, 1, tzinfo=UTC),
        source=InputSource.CONDITIONALITY,
        constraining_actor_id="IMF",
        constraint_mechanism="PENSION_CUT",
        instrument=FiscalInstrument.SPENDING_CHANGE,
        value=Decimal("-0.03"),
    )

    events = inp.get_events(inp.effective_date)
    assert events, "FiscalPolicyInput should produce at least one event"

    for evt in events:
        assert evt.metadata.get("input_source") == "conditionality", (
            f"Expected input_source='conditionality' in metadata, got {evt.metadata}"
        )
        assert evt.metadata.get("constraining_actor_id") == "IMF"
        assert evt.metadata.get("constraint_mechanism") == "PENSION_CUT"


def test_non_conditionality_events_no_conditionality_metadata() -> None:
    """Non-CONDITIONALITY inputs do not inject conditionality metadata."""
    from datetime import UTC, datetime

    from app.simulation.orchestration.inputs import (
        FiscalInstrument,
        FiscalPolicyInput,
        InputSource,
    )

    inp = FiscalPolicyInput(
        actor_id="MOF",
        actor_role="ministry",
        target_entity="GRC",
        effective_date=datetime(2010, 1, 1, tzinfo=UTC),
        source=InputSource.SCENARIO_SCRIPT,
        instrument=FiscalInstrument.SPENDING_CHANGE,
        value=Decimal("-0.03"),
    )

    events = inp.get_events(inp.effective_date)
    for evt in events:
        assert evt.metadata.get("input_source") != "conditionality"
        assert "constraining_actor_id" not in evt.metadata


# ---------------------------------------------------------------------------
# Composite score (Decision 4)
# ---------------------------------------------------------------------------


def test_composite_score_range() -> None:
    """Political economy composite score is in [0.0, 1.0]."""
    for survival in ["0.1", "0.5", "0.9"]:
        for legitimacy in ["0.1", "0.5", "0.9"]:
            for capture_coeff in ["0.2", "0.4", "0.8"]:
                elite_idx, _, _ = _compute_elite_capture_indicators(Decimal(capture_coeff))
                score = _compute_composite_score(
                    Decimal(survival), elite_idx, Decimal(legitimacy)
                )
                assert Decimal("0") <= score <= Decimal("1"), (
                    f"Composite score {score} out of [0,1] for "
                    f"survival={survival}, legitimacy={legitimacy}, capture={capture_coeff}"
                )


def test_composite_score_higher_with_better_inputs() -> None:
    """Composite score is higher with higher survival, lower capture, higher legitimacy."""
    elite_high_capture, _, _ = _compute_elite_capture_indicators(Decimal("0.8"))
    elite_low_capture, _, _ = _compute_elite_capture_indicators(Decimal("0.25"))

    score_good = _compute_composite_score(Decimal("0.9"), elite_low_capture, Decimal("0.9"))
    score_bad = _compute_composite_score(Decimal("0.1"), elite_high_capture, Decimal("0.1"))
    assert score_good > score_bad


# ---------------------------------------------------------------------------
# Conditionality aggregation helper
# ---------------------------------------------------------------------------


def test_aggregate_conditionality_terms_groups_by_actor_and_mechanism() -> None:
    """_aggregate_conditionality_terms groups by (actor_id, mechanism)."""
    evt1 = _conditionality_event("GRC", "IMF", "FISCAL_CONSOLIDATION", "-0.05")
    evt2 = _conditionality_event("GRC", "IMF", "PENSION_CUT", "-0.03")
    evt3 = _conditionality_event("GRC", "IMF", "FISCAL_CONSOLIDATION", "-0.02")  # same as evt1

    result = _aggregate_conditionality_terms([evt1, evt2, evt3])

    assert ("IMF", "FISCAL_CONSOLIDATION") in result
    assert ("IMF", "PENSION_CUT") in result
    assert abs(result[("IMF", "FISCAL_CONSOLIDATION")] - Decimal("-0.07")) < Decimal("0.001")
    assert abs(result[("IMF", "PENSION_CUT")] - Decimal("-0.03")) < Decimal("0.001")


def test_aggregate_conditionality_terms_ignores_missing_actor() -> None:
    """Events without constraining_actor_id in metadata are skipped."""
    plain_evt = Event(
        event_id="plain",
        source_entity_id="GRC",
        event_type="fiscal_policy_spending_change",
        affected_attributes={"spending_change": _qty("-0.05")},
        propagation_rules=[],
        timestep_originated=_EPOCH,
        framework=MeasurementFramework.FINANCIAL,
        metadata={"input_source": "conditionality"},  # no constraining_actor_id
    )
    result = _aggregate_conditionality_terms([plain_evt])
    assert result == {}


# ---------------------------------------------------------------------------
# Non-country entity skip
# ---------------------------------------------------------------------------


def test_non_country_entity_returns_empty() -> None:
    """PoliticalEconomyModule returns [] for non-country entities."""
    entity = SimulationEntity(
        id="sector-GRC",
        entity_type="sector",
        attributes={"legitimacy_index": _qty("0.5")},
        metadata={},
    )
    state = _state(entity, [_fiscal_event("sector-GRC")])
    module = PoliticalEconomyModule()
    events = module.compute(entity, state, _EPOCH)
    assert events == []


# ---------------------------------------------------------------------------
# No political economy context → no output
# ---------------------------------------------------------------------------


def test_no_political_context_returns_empty() -> None:
    """Module returns [] when entity has no legitimacy_index, capture, or conditionality."""
    entity = _entity("GRC")  # no legitimacy_index or elite_capture_coefficient
    state = _state(entity)
    module = PoliticalEconomyModule()
    events = module.compute(entity, state, _EPOCH)
    assert events == []
