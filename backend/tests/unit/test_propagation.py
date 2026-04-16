"""
Unit tests for the event propagation engine — ADR-001.

Tests cover: source-entity application, hop-by-hop graph traversal,
attenuation arithmetic, additive delta accumulation across events and
converging propagation paths, State[T] immutability, edge cases
(empty events, max_hops=0, zero attenuation, unknown entities, wrong
relationship types), and multiple propagation rules per event.

The numeric scenario in TestPropagateFullDiagramScenario directly
reproduces the example in docs/architecture/ADR-001-flowchart-event-propagation.mmd.
"""

from datetime import datetime

import pytest

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

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


def _entity(entity_id: str, **attrs: float) -> SimulationEntity:
    return SimulationEntity(
        id=entity_id,
        entity_type="country",
        attributes=dict(attrs),
        metadata={"name": entity_id},
    )


def _state(
    entities: dict[str, SimulationEntity],
    relationships: list[Relationship] | None = None,
) -> SimulationState:
    return SimulationState(
        timestep=datetime(2020, 1, 1),
        resolution=ResolutionConfig(),
        entities=entities,
        relationships=relationships or [],
        events=[],
        scenario_config=ScenarioConfig(
            scenario_id="test",
            name="Test",
            description="",
            start_date=datetime(2020, 1, 1),
            end_date=datetime(2025, 1, 1),
        ),
    )


def _event(
    source: str,
    attrs: dict[str, float],
    rules: list[PropagationRule] | None = None,
) -> Event:
    return Event(
        event_id="evt-1",
        source_entity_id=source,
        event_type="shock",
        affected_attributes=attrs,
        propagation_rules=rules or [],
        timestep_originated=datetime(2020, 1, 1),
        framework=MeasurementFramework.FINANCIAL,
    )


def _rule(
    relationship_type: str = "trade",
    attenuation_factor: float = 0.5,
    max_hops: int = 1,
) -> PropagationRule:
    return PropagationRule(
        relationship_type=relationship_type,
        attenuation_factor=attenuation_factor,
        max_hops=max_hops,
    )


def _rel(
    source: str,
    target: str,
    relationship_type: str = "trade",
    weight: float = 1.0,
) -> Relationship:
    return Relationship(
        source_id=source,
        target_id=target,
        relationship_type=relationship_type,
        weight=weight,
    )


# ---------------------------------------------------------------------------
# Empty events
# ---------------------------------------------------------------------------


class TestPropagateEmptyEvents:
    def test_empty_events_returns_new_state_object(self) -> None:
        state = _state({"BOL": _entity("BOL", gdp=100.0)})
        result = propagate(state, [])
        assert result is not state

    def test_empty_events_preserves_all_entity_attributes(self) -> None:
        state = _state({"BOL": _entity("BOL", gdp=100.0, debt_gdp_ratio=0.60)})
        result = propagate(state, [])
        assert result.entities["BOL"].attributes == pytest.approx(
            {"gdp": 100.0, "debt_gdp_ratio": 0.60}
        )

    def test_empty_events_preserves_multiple_entities(self) -> None:
        state = _state({
            "BOL": _entity("BOL", gdp=44.0),
            "BRA": _entity("BRA", gdp=2200.0),
        })
        result = propagate(state, [])
        assert result.entities["BOL"].get_attribute("gdp") == pytest.approx(44.0)
        assert result.entities["BRA"].get_attribute("gdp") == pytest.approx(2200.0)

    def test_empty_events_state_t_not_mutated(self) -> None:
        state = _state({"BOL": _entity("BOL", gdp=100.0)})
        original_attrs = dict(state.entities["BOL"].attributes)
        propagate(state, [])
        assert state.entities["BOL"].attributes == original_attrs


# ---------------------------------------------------------------------------
# Source-entity application (no propagation rules)
# ---------------------------------------------------------------------------


class TestPropagateSourceOnly:
    def test_source_entity_receives_full_delta(self) -> None:
        state = _state({"BOL": _entity("BOL", debt_gdp_ratio=0.50)})
        event = _event("BOL", {"debt_gdp_ratio": 0.15})
        result = propagate(state, [event])
        assert result.entities["BOL"].get_attribute("debt_gdp_ratio") == pytest.approx(0.65)

    def test_source_event_initialises_missing_attribute_from_zero(self) -> None:
        state = _state({"BOL": _entity("BOL")})
        event = _event("BOL", {"reserves": 5.0e9})
        result = propagate(state, [event])
        assert result.entities["BOL"].get_attribute("reserves") == pytest.approx(5.0e9)

    def test_source_event_negative_delta_subtracts(self) -> None:
        state = _state({"BOL": _entity("BOL", gdp_growth=0.03)})
        event = _event("BOL", {"gdp_growth": -0.05})
        result = propagate(state, [event])
        assert result.entities["BOL"].get_attribute("gdp_growth") == pytest.approx(-0.02)

    def test_non_source_entities_unchanged_when_no_rules(self) -> None:
        state = _state({
            "BOL": _entity("BOL", gdp=100.0),
            "BRA": _entity("BRA", gdp=2200.0),
        })
        event = _event("BOL", {"gdp": -10.0})
        result = propagate(state, [event])
        assert result.entities["BRA"].get_attribute("gdp") == pytest.approx(2200.0)

    def test_source_not_in_state_entities_produces_unchanged_state(self) -> None:
        # The event's source entity is not tracked in this state. The delta
        # accumulates for an entity that doesn't exist, and is dropped at
        # _build_next_state. All present entities are returned unchanged.
        state = _state({"BRA": _entity("BRA", gdp=2200.0)})
        event = _event("BOL", {"debt_gdp_ratio": 0.15})
        result = propagate(state, [event])
        assert result.entities["BRA"].get_attribute("gdp") == pytest.approx(2200.0)
        assert "BOL" not in result.entities


# ---------------------------------------------------------------------------
# One-hop propagation
# ---------------------------------------------------------------------------


class TestPropagateOneHop:
    def test_direct_neighbor_receives_attenuated_delta(self) -> None:
        state = _state(
            entities={
                "BOL": _entity("BOL", debt_gdp_ratio=0.50),
                "BRA": _entity("BRA", debt_gdp_ratio=0.80),
            },
            relationships=[_rel("BOL", "BRA", "trade", weight=0.30)],
        )
        event = _event("BOL", {"debt_gdp_ratio": 0.15}, rules=[_rule("trade", 0.4, 1)])
        result = propagate(state, [event])
        # BOL: +0.15 (full)
        # BRA: +0.15 * 0.4 * 0.30 = +0.018
        assert result.entities["BOL"].get_attribute("debt_gdp_ratio") == pytest.approx(0.65)
        assert result.entities["BRA"].get_attribute("debt_gdp_ratio") == pytest.approx(0.818)

    def test_only_matching_relationship_type_propagates(self) -> None:
        state = _state(
            entities={
                "BOL": _entity("BOL"),
                "BRA": _entity("BRA", gdp_growth=0.02),
                "IMF": _entity("IMF", gdp_growth=0.00),
            },
            relationships=[
                _rel("BOL", "BRA", "trade", weight=1.0),
                _rel("BOL", "IMF", "debt", weight=1.0),
            ],
        )
        event = _event("BOL", {"gdp_growth": -0.02}, rules=[_rule("trade", 0.5, 1)])
        result = propagate(state, [event])
        # BRA receives trade propagation
        expected_bra = pytest.approx(0.02 + (-0.02 * 0.5 * 1.0))
        assert result.entities["BRA"].get_attribute("gdp_growth") == expected_bra
        # IMF has a debt relationship, not trade — unchanged
        assert result.entities["IMF"].get_attribute("gdp_growth") == pytest.approx(0.00)

    def test_multiple_direct_neighbors_all_receive_proportional_delta(self) -> None:
        state = _state(
            entities={
                "BOL": _entity("BOL"),
                "BRA": _entity("BRA"),
                "ARG": _entity("ARG"),
                "PER": _entity("PER"),
            },
            relationships=[
                _rel("BOL", "BRA", "trade", weight=0.30),
                _rel("BOL", "ARG", "trade", weight=0.20),
                _rel("BOL", "PER", "trade", weight=0.15),
            ],
        )
        event = _event("BOL", {"debt_gdp_ratio": 0.15}, rules=[_rule("trade", 0.4, 1)])
        result = propagate(state, [event])
        assert result.entities["BRA"].get_attribute("debt_gdp_ratio") == pytest.approx(
            0.15 * 0.4 * 0.30
        )
        assert result.entities["ARG"].get_attribute("debt_gdp_ratio") == pytest.approx(
            0.15 * 0.4 * 0.20
        )
        assert result.entities["PER"].get_attribute("debt_gdp_ratio") == pytest.approx(
            0.15 * 0.4 * 0.15
        )

    def test_max_hops_one_does_not_reach_second_degree_neighbors(self) -> None:
        state = _state(
            entities={
                "BOL": _entity("BOL"),
                "BRA": _entity("BRA"),
                "URY": _entity("URY"),
            },
            relationships=[
                _rel("BOL", "BRA", "trade", weight=1.0),
                _rel("BRA", "URY", "trade", weight=1.0),
            ],
        )
        event = _event("BOL", {"gdp_growth": -0.02}, rules=[_rule("trade", 0.5, max_hops=1)])
        result = propagate(state, [event])
        # BRA receives hop-1 delta; URY is hop-2 and should not be reached
        assert result.entities["BRA"].get_attribute("gdp_growth") != pytest.approx(0.0)
        assert result.entities["URY"].get_attribute("gdp_growth") == pytest.approx(0.0)


# ---------------------------------------------------------------------------
# Full ADR-001 diagram scenario (two hops, converging paths)
# ---------------------------------------------------------------------------


class TestPropagateFullDiagramScenario:
    """Reproduces the exact numeric example from ADR-001-flowchart-event-propagation.mmd.

    Bolivia fiscal shock:
        Event: source=BOL, debt_gdp_ratio +0.15
        Rule:  relationship_type=trade, attenuation_factor=0.4, max_hops=2

    Graph:
        BOL → BRA  weight=0.30
        BOL → ARG  weight=0.20
        BOL → PER  weight=0.15
        BRA → URY  weight=0.50
        ARG → URY  weight=0.40

    Expected deltas:
        BOL  +0.15          (source, full)
        BRA  +0.018         (0.15 * 0.4 * 0.30)
        ARG  +0.012         (0.15 * 0.4 * 0.20)
        PER  +0.009         (0.15 * 0.4 * 0.15)
        URY  +0.00552       (0.018 * 0.4 * 0.50) + (0.012 * 0.4 * 0.40)
                            = 0.0036 + 0.00192
    """

    def _build_state(self) -> SimulationState:
        return _state(
            entities={
                "BOL": _entity("BOL", debt_gdp_ratio=0.0),
                "BRA": _entity("BRA", debt_gdp_ratio=0.0),
                "ARG": _entity("ARG", debt_gdp_ratio=0.0),
                "PER": _entity("PER", debt_gdp_ratio=0.0),
                "URY": _entity("URY", debt_gdp_ratio=0.0),
            },
            relationships=[
                _rel("BOL", "BRA", "trade", weight=0.30),
                _rel("BOL", "ARG", "trade", weight=0.20),
                _rel("BOL", "PER", "trade", weight=0.15),
                _rel("BRA", "URY", "trade", weight=0.50),
                _rel("ARG", "URY", "trade", weight=0.40),
            ],
        )

    def test_source_bolivia_receives_full_delta(self) -> None:
        state = self._build_state()
        event = _event("BOL", {"debt_gdp_ratio": 0.15}, rules=[_rule("trade", 0.4, 2)])
        result = propagate(state, [event])
        assert result.entities["BOL"].get_attribute("debt_gdp_ratio") == pytest.approx(0.15)

    def test_brazil_receives_hop_one_delta(self) -> None:
        state = self._build_state()
        event = _event("BOL", {"debt_gdp_ratio": 0.15}, rules=[_rule("trade", 0.4, 2)])
        result = propagate(state, [event])
        assert result.entities["BRA"].get_attribute("debt_gdp_ratio") == pytest.approx(0.018)

    def test_argentina_receives_hop_one_delta(self) -> None:
        state = self._build_state()
        event = _event("BOL", {"debt_gdp_ratio": 0.15}, rules=[_rule("trade", 0.4, 2)])
        result = propagate(state, [event])
        assert result.entities["ARG"].get_attribute("debt_gdp_ratio") == pytest.approx(0.012)

    def test_peru_receives_hop_one_delta(self) -> None:
        state = self._build_state()
        event = _event("BOL", {"debt_gdp_ratio": 0.15}, rules=[_rule("trade", 0.4, 2)])
        result = propagate(state, [event])
        assert result.entities["PER"].get_attribute("debt_gdp_ratio") == pytest.approx(0.009)

    def test_uruguay_receives_additive_hop_two_delta_from_both_paths(self) -> None:
        state = self._build_state()
        event = _event("BOL", {"debt_gdp_ratio": 0.15}, rules=[_rule("trade", 0.4, 2)])
        result = propagate(state, [event])
        ury_from_bra = 0.018 * 0.4 * 0.50   # 0.0036
        ury_from_arg = 0.012 * 0.4 * 0.40   # 0.00192
        expected_ury = ury_from_bra + ury_from_arg  # 0.00552
        assert result.entities["URY"].get_attribute("debt_gdp_ratio") == pytest.approx(expected_ury)

    def test_all_five_entities_correct_simultaneously(self) -> None:
        state = self._build_state()
        event = _event("BOL", {"debt_gdp_ratio": 0.15}, rules=[_rule("trade", 0.4, 2)])
        result = propagate(state, [event])
        assert result.entities["BOL"].get_attribute("debt_gdp_ratio") == pytest.approx(0.15)
        assert result.entities["BRA"].get_attribute("debt_gdp_ratio") == pytest.approx(0.018)
        assert result.entities["ARG"].get_attribute("debt_gdp_ratio") == pytest.approx(0.012)
        assert result.entities["PER"].get_attribute("debt_gdp_ratio") == pytest.approx(0.009)
        assert result.entities["URY"].get_attribute("debt_gdp_ratio") == pytest.approx(0.00552)


# ---------------------------------------------------------------------------
# Additive accumulation
# ---------------------------------------------------------------------------


class TestPropagateAdditive:
    def test_two_events_on_same_attribute_accumulate(self) -> None:
        state = _state({"BOL": _entity("BOL", debt_gdp_ratio=0.50)})
        events = [
            _event("BOL", {"debt_gdp_ratio": 0.10}),
            _event("BOL", {"debt_gdp_ratio": 0.05}),
        ]
        result = propagate(state, events)
        assert result.entities["BOL"].get_attribute("debt_gdp_ratio") == pytest.approx(0.65)

    def test_two_events_on_different_attributes_both_applied(self) -> None:
        state = _state({"BOL": _entity("BOL", gdp_growth=0.03, debt_gdp_ratio=0.50)})
        events = [
            _event("BOL", {"gdp_growth": -0.02}),
            _event("BOL", {"debt_gdp_ratio": 0.15}),
        ]
        result = propagate(state, events)
        assert result.entities["BOL"].get_attribute("gdp_growth") == pytest.approx(0.01)
        assert result.entities["BOL"].get_attribute("debt_gdp_ratio") == pytest.approx(0.65)

    def test_two_events_accumulate_across_different_source_entities(self) -> None:
        state = _state({
            "BOL": _entity("BOL"),
            "BRA": _entity("BRA"),
            "URY": _entity("URY", gdp_growth=0.02),
        })
        # Both BOL and BRA propagate to URY via trade
        relationships = [
            _rel("BOL", "URY", "trade", weight=1.0),
            _rel("BRA", "URY", "trade", weight=1.0),
        ]
        state = _state(
            entities=state.entities,
            relationships=relationships,
        )
        events = [
            _event("BOL", {"gdp_growth": -0.01}, rules=[_rule("trade", 1.0, 1)]),
            _event("BRA", {"gdp_growth": -0.01}, rules=[_rule("trade", 1.0, 1)]),
        ]
        result = propagate(state, events)
        # URY receives -0.01 from BOL and -0.01 from BRA
        assert result.entities["URY"].get_attribute("gdp_growth") == pytest.approx(0.00)

    def test_propagated_and_direct_deltas_accumulate_on_same_entity(self) -> None:
        # BOL both directly produces an event AND receives a propagated delta
        state = _state(
            entities={
                "BRA": _entity("BRA"),
                "BOL": _entity("BOL", debt_gdp_ratio=0.0),
            },
            relationships=[_rel("BRA", "BOL", "trade", weight=0.5)],
        )
        events = [
            _event("BOL", {"debt_gdp_ratio": 0.10}),
            _event("BRA", {"debt_gdp_ratio": 0.20}, rules=[_rule("trade", 1.0, 1)]),
        ]
        result = propagate(state, events)
        # BOL direct: +0.10; BOL from BRA propagation: +0.20 * 1.0 * 0.5 = +0.10
        assert result.entities["BOL"].get_attribute("debt_gdp_ratio") == pytest.approx(0.20)


# ---------------------------------------------------------------------------
# State[T] immutability
# ---------------------------------------------------------------------------


class TestPropagateImmutability:
    def test_source_entity_attributes_dict_not_mutated(self) -> None:
        entity = _entity("BOL", debt_gdp_ratio=0.50)
        state = _state({"BOL": entity})
        original_attrs = dict(entity.attributes)
        propagate(state, [_event("BOL", {"debt_gdp_ratio": 0.15})])
        assert entity.attributes == original_attrs

    def test_state_entities_dict_not_mutated(self) -> None:
        state = _state({"BOL": _entity("BOL", gdp=100.0)})
        original_entity_ids = set(state.entities.keys())
        propagate(state, [_event("BOL", {"gdp": -10.0})])
        assert set(state.entities.keys()) == original_entity_ids

    def test_propagated_entity_attributes_not_mutated(self) -> None:
        neighbor = _entity("BRA", debt_gdp_ratio=0.80)
        state = _state(
            entities={"BOL": _entity("BOL"), "BRA": neighbor},
            relationships=[_rel("BOL", "BRA", "trade", weight=1.0)],
        )
        original_bra_attrs = dict(neighbor.attributes)
        propagate(state, [_event("BOL", {"debt_gdp_ratio": 0.15}, rules=[_rule("trade", 0.4, 1)])])
        assert neighbor.attributes == original_bra_attrs

    def test_result_entity_is_not_same_object_as_input_entity(self) -> None:
        entity = _entity("BOL", gdp=100.0)
        state = _state({"BOL": entity})
        result = propagate(state, [_event("BOL", {"gdp": -10.0})])
        assert result.entities["BOL"] is not entity

    def test_result_attributes_dict_is_not_same_object(self) -> None:
        entity = _entity("BOL", gdp=100.0)
        state = _state({"BOL": entity})
        result = propagate(state, [])
        assert result.entities["BOL"].attributes is not entity.attributes


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------


class TestPropagateEdgeCases:
    def test_max_hops_zero_means_no_propagation(self) -> None:
        state = _state(
            entities={"BOL": _entity("BOL"), "BRA": _entity("BRA")},
            relationships=[_rel("BOL", "BRA", "trade", weight=1.0)],
        )
        event = _event("BOL", {"gdp_growth": -0.02}, rules=[_rule("trade", 0.5, max_hops=0)])
        result = propagate(state, [event])
        assert result.entities["BOL"].get_attribute("gdp_growth") == pytest.approx(-0.02)
        assert result.entities["BRA"].get_attribute("gdp_growth") == pytest.approx(0.0)

    def test_zero_attenuation_factor_produces_zero_propagated_delta(self) -> None:
        state = _state(
            entities={"BOL": _entity("BOL"), "BRA": _entity("BRA")},
            relationships=[_rel("BOL", "BRA", "trade", weight=1.0)],
        )
        event = _event(
            "BOL", {"gdp_growth": -0.02}, rules=[_rule("trade", attenuation_factor=0.0, max_hops=1)]
        )
        result = propagate(state, [event])
        # Source still receives full delta; propagated delta is zero
        assert result.entities["BOL"].get_attribute("gdp_growth") == pytest.approx(-0.02)
        assert result.entities["BRA"].get_attribute("gdp_growth") == pytest.approx(0.0)

    def test_full_attenuation_factor_preserves_delta(self) -> None:
        state = _state(
            entities={"BOL": _entity("BOL"), "BRA": _entity("BRA")},
            relationships=[_rel("BOL", "BRA", "trade", weight=1.0)],
        )
        event = _event(
            "BOL", {"gdp_growth": -0.02}, rules=[_rule("trade", attenuation_factor=1.0, max_hops=1)]
        )
        result = propagate(state, [event])
        assert result.entities["BRA"].get_attribute("gdp_growth") == pytest.approx(-0.02)

    def test_zero_relationship_weight_produces_zero_propagated_delta(self) -> None:
        state = _state(
            entities={"BOL": _entity("BOL"), "BRA": _entity("BRA")},
            relationships=[_rel("BOL", "BRA", "trade", weight=0.0)],
        )
        event = _event("BOL", {"gdp_growth": -0.02}, rules=[_rule("trade", 0.5, 1)])
        result = propagate(state, [event])
        assert result.entities["BRA"].get_attribute("gdp_growth") == pytest.approx(0.0)

    def test_relationship_target_not_in_state_delta_dropped(self) -> None:
        # BRA appears as a relationship target but is not in state.entities.
        # Its delta accumulates internally but is silently dropped at build time.
        state = _state(
            entities={"BOL": _entity("BOL")},
            relationships=[_rel("BOL", "BRA", "trade", weight=1.0)],
        )
        event = _event("BOL", {"gdp_growth": -0.02}, rules=[_rule("trade", 1.0, 1)])
        result = propagate(state, [event])
        assert "BRA" not in result.entities
        assert result.entities["BOL"].get_attribute("gdp_growth") == pytest.approx(-0.02)

    def test_no_relationships_in_state_only_source_affected(self) -> None:
        state = _state({"BOL": _entity("BOL"), "BRA": _entity("BRA")})
        event = _event("BOL", {"debt_gdp_ratio": 0.15}, rules=[_rule("trade", 0.4, 2)])
        result = propagate(state, [event])
        assert result.entities["BOL"].get_attribute("debt_gdp_ratio") == pytest.approx(0.15)
        assert result.entities["BRA"].get_attribute("debt_gdp_ratio") == pytest.approx(0.0)

    def test_wrong_relationship_type_not_traversed(self) -> None:
        state = _state(
            entities={"BOL": _entity("BOL"), "IMF": _entity("IMF")},
            relationships=[_rel("BOL", "IMF", "debt", weight=1.0)],
        )
        # Rule specifies 'trade' but only 'debt' relationship exists
        event = _event("BOL", {"debt_gdp_ratio": 0.15}, rules=[_rule("trade", 0.4, 1)])
        result = propagate(state, [event])
        assert result.entities["IMF"].get_attribute("debt_gdp_ratio") == pytest.approx(0.0)

    def test_multiple_attribute_delta_propagates_all_attributes(self) -> None:
        state = _state(
            entities={"BOL": _entity("BOL"), "BRA": _entity("BRA")},
            relationships=[_rel("BOL", "BRA", "trade", weight=1.0)],
        )
        event = _event(
            "BOL",
            {"gdp_growth": -0.02, "inflation": 0.05},
            rules=[_rule("trade", 0.5, 1)],
        )
        result = propagate(state, [event])
        assert result.entities["BRA"].get_attribute("gdp_growth") == pytest.approx(-0.01)
        assert result.entities["BRA"].get_attribute("inflation") == pytest.approx(0.025)


# ---------------------------------------------------------------------------
# Multiple propagation rules per event
# ---------------------------------------------------------------------------


class TestPropagateMultipleRules:
    def test_two_rules_different_relationship_types_propagate_independently(self) -> None:
        state = _state(
            entities={
                "BOL": _entity("BOL"),
                "BRA": _entity("BRA"),
                "IMF": _entity("IMF"),
            },
            relationships=[
                _rel("BOL", "BRA", "trade", weight=1.0),
                _rel("BOL", "IMF", "debt", weight=1.0),
            ],
        )
        event = _event(
            "BOL",
            {"gdp_growth": -0.02},
            rules=[
                _rule("trade", attenuation_factor=0.5, max_hops=1),
                _rule("debt", attenuation_factor=0.8, max_hops=1),
            ],
        )
        result = propagate(state, [event])
        assert result.entities["BRA"].get_attribute("gdp_growth") == pytest.approx(
            -0.02 * 0.5 * 1.0
        )
        assert result.entities["IMF"].get_attribute("gdp_growth") == pytest.approx(
            -0.02 * 0.8 * 1.0
        )

    def test_two_rules_same_type_different_attenuation_accumulate(self) -> None:
        # Two propagation rules of the same type on the same event is unusual
        # but valid — both traverse the same graph and their deltas accumulate.
        state = _state(
            entities={"BOL": _entity("BOL"), "BRA": _entity("BRA")},
            relationships=[_rel("BOL", "BRA", "trade", weight=1.0)],
        )
        event = _event(
            "BOL",
            {"gdp_growth": -0.02},
            rules=[
                _rule("trade", attenuation_factor=0.5, max_hops=1),
                _rule("trade", attenuation_factor=0.3, max_hops=1),
            ],
        )
        result = propagate(state, [event])
        expected = (-0.02 * 0.5 * 1.0) + (-0.02 * 0.3 * 1.0)
        assert result.entities["BRA"].get_attribute("gdp_growth") == pytest.approx(expected)


# ---------------------------------------------------------------------------
# State structure preservation
# ---------------------------------------------------------------------------


class TestPropagateStateStructure:
    def test_result_preserves_timestep(self) -> None:
        ts = datetime(2023, 6, 15)
        state = SimulationState(
            timestep=ts,
            resolution=ResolutionConfig(),
            entities={"BOL": _entity("BOL")},
            relationships=[],
            events=[],
            scenario_config=ScenarioConfig(
                scenario_id="s1",
                name="Test",
                description="",
                start_date=ts,
                end_date=datetime(2025, 1, 1),
            ),
        )
        result = propagate(state, [_event("BOL", {"gdp": -1.0})])
        assert result.timestep == ts

    def test_result_preserves_relationships(self) -> None:
        rels = [_rel("BOL", "BRA", "trade", weight=0.5)]
        state = _state(
            entities={"BOL": _entity("BOL"), "BRA": _entity("BRA")},
            relationships=rels,
        )
        result = propagate(state, [])
        assert result.relationships is state.relationships

    def test_result_preserves_scenario_config(self) -> None:
        state = _state({"BOL": _entity("BOL")})
        result = propagate(state, [])
        assert result.scenario_config is state.scenario_config

    def test_result_contains_all_entities_from_state(self) -> None:
        state = _state({
            "BOL": _entity("BOL"),
            "BRA": _entity("BRA"),
            "GRC": _entity("GRC"),
        })
        result = propagate(state, [_event("BOL", {"gdp": -1.0})])
        assert set(result.entities.keys()) == {"BOL", "BRA", "GRC"}
