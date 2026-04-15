"""
Unit tests for simulation core data model — ADR-001.

Tests cover: SimulationEntity, Relationship, Event, SimulationState,
MeasurementFramework, ResolutionConfig, ScenarioConfig, PropagationRule,
Geometry, and the SimulationModule abstract interface.
"""
import pytest
from datetime import datetime
from typing import List

from app.simulation.engine.models import (
    Event,
    Geometry,
    MeasurementFramework,
    PropagationRule,
    Relationship,
    ResolutionConfig,
    ResolutionLevel,
    ScenarioConfig,
    SimulationEntity,
    SimulationModule,
    SimulationState,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

def make_entity(
    id: str = "BOL",
    entity_type: str = "country",
    attributes: dict | None = None,
    metadata: dict | None = None,
    parent_id: str | None = None,
) -> SimulationEntity:
    return SimulationEntity(
        id=id,
        entity_type=entity_type,
        attributes=attributes if attributes is not None else {},
        metadata=metadata if metadata is not None else {"name": id},
        parent_id=parent_id,
    )


def make_scenario(
    scenario_id: str = "s1",
    start: datetime | None = None,
    end: datetime | None = None,
) -> ScenarioConfig:
    return ScenarioConfig(
        scenario_id=scenario_id,
        name="Test scenario",
        description="Unit test scenario",
        start_date=start or datetime(2020, 1, 1),
        end_date=end or datetime(2025, 1, 1),
    )


def make_state(
    entities: dict | None = None,
    relationships: list | None = None,
    events: list | None = None,
    timestep: datetime | None = None,
) -> SimulationState:
    return SimulationState(
        timestep=timestep or datetime(2020, 1, 1),
        resolution=ResolutionConfig(),
        entities=entities or {},
        relationships=relationships or [],
        events=events or [],
        scenario_config=make_scenario(),
    )


def make_event(
    event_id: str = "evt-1",
    source_entity_id: str = "BOL",
    event_type: str = "shock",
    affected_attributes: dict | None = None,
    propagation_rules: list | None = None,
    timestep: datetime | None = None,
    framework: MeasurementFramework = MeasurementFramework.FINANCIAL,
) -> Event:
    return Event(
        event_id=event_id,
        source_entity_id=source_entity_id,
        event_type=event_type,
        affected_attributes=affected_attributes or {"gdp_growth": -0.02},
        propagation_rules=propagation_rules or [],
        timestep_originated=timestep or datetime(2020, 1, 1),
        framework=framework,
    )


# ---------------------------------------------------------------------------
# MeasurementFramework
# ---------------------------------------------------------------------------

class TestMeasurementFramework:
    def test_all_four_frameworks_present(self):
        values = {f.value for f in MeasurementFramework}
        assert values == {"financial", "human_development", "ecological", "governance"}

    def test_no_implicit_conversion_between_frameworks(self):
        # frameworks are distinct enum members — equality only holds with itself
        assert MeasurementFramework.FINANCIAL != MeasurementFramework.HUMAN_DEVELOPMENT
        assert MeasurementFramework.ECOLOGICAL != MeasurementFramework.GOVERNANCE


# ---------------------------------------------------------------------------
# ResolutionLevel & ResolutionConfig
# ---------------------------------------------------------------------------

class TestResolutionLevel:
    def test_nation_state_is_level_1(self):
        assert ResolutionLevel.NATION_STATE.value == 1

    def test_individual_is_level_6(self):
        assert ResolutionLevel.INDIVIDUAL.value == 6

    def test_levels_are_ordered(self):
        levels = list(ResolutionLevel)
        values = [level.value for level in levels]
        assert values == sorted(values)


class TestResolutionConfig:
    def test_defaults_to_nation_state(self):
        config = ResolutionConfig()
        assert config.global_level == ResolutionLevel.NATION_STATE

    def test_level_for_returns_global_when_no_override(self):
        config = ResolutionConfig(global_level=ResolutionLevel.NATION_STATE)
        assert config.level_for("BOL") == ResolutionLevel.NATION_STATE

    def test_entity_override_takes_precedence(self):
        config = ResolutionConfig(
            global_level=ResolutionLevel.NATION_STATE,
            entity_overrides={"SAU": ResolutionLevel.URBAN_RURAL},
        )
        assert config.level_for("SAU") == ResolutionLevel.URBAN_RURAL
        assert config.level_for("BOL") == ResolutionLevel.NATION_STATE

    def test_multiple_overrides_are_independent(self):
        config = ResolutionConfig(
            global_level=ResolutionLevel.NATION_STATE,
            entity_overrides={
                "SAU": ResolutionLevel.URBAN_RURAL,
                "GRC": ResolutionLevel.SUBNATIONAL,
            },
        )
        assert config.level_for("SAU") == ResolutionLevel.URBAN_RURAL
        assert config.level_for("GRC") == ResolutionLevel.SUBNATIONAL
        assert config.level_for("BOL") == ResolutionLevel.NATION_STATE


# ---------------------------------------------------------------------------
# Geometry
# ---------------------------------------------------------------------------

class TestGeometry:
    def test_point_geometry(self):
        g = Geometry(geometry_type="Point", coordinates=[-65.0, -17.0])
        assert g.geometry_type == "Point"
        assert g.crs == "EPSG:4326"

    def test_polygon_geometry(self):
        coords = [[[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]]]
        g = Geometry(geometry_type="Polygon", coordinates=coords, crs="EPSG:3857")
        assert g.geometry_type == "Polygon"
        assert g.crs == "EPSG:3857"


# ---------------------------------------------------------------------------
# SimulationEntity
# ---------------------------------------------------------------------------

class TestSimulationEntity:
    def test_minimal_construction(self):
        entity = make_entity()
        assert entity.id == "BOL"
        assert entity.entity_type == "country"
        assert entity.parent_id is None
        assert entity.geometry is None

    def test_get_attribute_returns_value(self):
        entity = make_entity(attributes={"gdp": 44.2e9})
        assert entity.get_attribute("gdp") == pytest.approx(44.2e9)

    def test_get_attribute_returns_default_for_missing_key(self):
        entity = make_entity(attributes={})
        assert entity.get_attribute("nonexistent") == 0.0
        assert entity.get_attribute("nonexistent", default=99.0) == 99.0

    def test_set_attribute_stores_value(self):
        entity = make_entity(attributes={})
        entity.set_attribute("inflation", 0.08)
        assert entity.attributes["inflation"] == pytest.approx(0.08)

    def test_set_attribute_overwrites_existing(self):
        entity = make_entity(attributes={"inflation": 0.05})
        entity.set_attribute("inflation", 0.12)
        assert entity.attributes["inflation"] == pytest.approx(0.12)

    def test_apply_delta_adds_to_existing(self):
        entity = make_entity(attributes={"debt_gdp_ratio": 0.60})
        entity.apply_delta("debt_gdp_ratio", 0.10)
        assert entity.attributes["debt_gdp_ratio"] == pytest.approx(0.70)

    def test_apply_delta_initialises_missing_key_at_zero(self):
        entity = make_entity(attributes={})
        entity.apply_delta("reserves", 5.0e9)
        assert entity.attributes["reserves"] == pytest.approx(5.0e9)

    def test_apply_delta_negative(self):
        entity = make_entity(attributes={"reserves": 10.0e9})
        entity.apply_delta("reserves", -3.0e9)
        assert entity.attributes["reserves"] == pytest.approx(7.0e9)

    def test_parent_id_for_subnational_entity(self):
        region = make_entity(
            id="BOL-SANTA-CRUZ",
            entity_type="region",
            parent_id="BOL",
        )
        assert region.parent_id == "BOL"

    def test_entity_with_geometry(self):
        geom = Geometry(geometry_type="Point", coordinates=[-65.0, -17.0])
        entity = SimulationEntity(
            id="BOL",
            entity_type="country",
            attributes={},
            metadata={},
            geometry=geom,
        )
        assert entity.geometry.geometry_type == "Point"

    def test_metadata_is_separate_from_attributes(self):
        entity = make_entity(
            attributes={"gdp": 1.0},
            metadata={"name": "Bolivia", "iso_a3": "BOL"},
        )
        assert "name" not in entity.attributes
        assert entity.metadata["iso_a3"] == "BOL"


# ---------------------------------------------------------------------------
# Relationship
# ---------------------------------------------------------------------------

class TestRelationship:
    def test_basic_construction(self):
        rel = Relationship(
            source_id="BOL",
            target_id="BRA",
            relationship_type="trade",
            weight=0.3,
        )
        assert rel.source_id == "BOL"
        assert rel.target_id == "BRA"
        assert rel.weight == pytest.approx(0.3)
        assert rel.attributes == {}

    def test_relationship_is_directed(self):
        rel_forward = Relationship("BOL", "BRA", "trade", 0.3)
        rel_backward = Relationship("BRA", "BOL", "trade", 0.1)
        assert rel_forward.source_id != rel_backward.source_id
        assert rel_forward.weight != rel_backward.weight

    def test_relationship_attributes(self):
        rel = Relationship(
            source_id="GRC",
            target_id="IMF",
            relationship_type="debt",
            weight=0.9,
            attributes={"principal_usd": 86e9, "interest_rate": 0.025},
        )
        assert rel.attributes["principal_usd"] == pytest.approx(86e9)

    def test_all_relationship_types_representable(self):
        for rtype in ("trade", "debt", "alliance", "currency"):
            rel = Relationship("A", "B", rtype, 0.5)
            assert rel.relationship_type == rtype


# ---------------------------------------------------------------------------
# PropagationRule
# ---------------------------------------------------------------------------

class TestPropagationRule:
    def test_defaults(self):
        rule = PropagationRule(relationship_type="trade", attenuation_factor=0.5)
        assert rule.max_hops == 1

    def test_custom_hops(self):
        rule = PropagationRule(
            relationship_type="debt",
            attenuation_factor=0.8,
            max_hops=3,
        )
        assert rule.max_hops == 3
        assert rule.attenuation_factor == pytest.approx(0.8)

    def test_zero_attenuation_means_no_propagation(self):
        rule = PropagationRule(relationship_type="alliance", attenuation_factor=0.0)
        assert rule.attenuation_factor == 0.0

    def test_full_attenuation_means_no_loss(self):
        rule = PropagationRule(relationship_type="trade", attenuation_factor=1.0)
        assert rule.attenuation_factor == 1.0


# ---------------------------------------------------------------------------
# Event
# ---------------------------------------------------------------------------

class TestEvent:
    def test_basic_construction(self):
        evt = make_event()
        assert evt.event_id == "evt-1"
        assert evt.source_entity_id == "BOL"
        assert evt.event_type == "shock"
        assert evt.framework == MeasurementFramework.FINANCIAL

    def test_default_framework_is_financial(self):
        evt = make_event()
        assert evt.framework == MeasurementFramework.FINANCIAL

    def test_human_development_framework(self):
        evt = make_event(framework=MeasurementFramework.HUMAN_DEVELOPMENT)
        assert evt.framework == MeasurementFramework.HUMAN_DEVELOPMENT

    def test_affected_attributes(self):
        evt = make_event(affected_attributes={"gdp_growth": -0.05, "unemployment": 0.02})
        assert evt.affected_attributes["gdp_growth"] == pytest.approx(-0.05)
        assert evt.affected_attributes["unemployment"] == pytest.approx(0.02)

    def test_propagation_rules_stored(self):
        rule = PropagationRule(relationship_type="trade", attenuation_factor=0.4)
        evt = make_event(propagation_rules=[rule])
        assert len(evt.propagation_rules) == 1
        assert evt.propagation_rules[0].relationship_type == "trade"

    def test_event_types_representable(self):
        for etype in ("policy_change", "shock", "threshold_crossed"):
            evt = make_event(event_type=etype)
            assert evt.event_type == etype

    def test_metadata_defaults_to_empty(self):
        evt = make_event()
        assert evt.metadata == {}

    def test_metadata_stores_arbitrary_data(self):
        evt = make_event()
        evt.metadata["source"] = "IMF Article IV consultation"
        assert evt.metadata["source"] == "IMF Article IV consultation"


# ---------------------------------------------------------------------------
# ScenarioConfig
# ---------------------------------------------------------------------------

class TestScenarioConfig:
    def test_basic_construction(self):
        scenario = make_scenario()
        assert scenario.scenario_id == "s1"
        assert scenario.initial_overrides == {}
        assert scenario.framework_weights == {}
        assert scenario.metadata == {}

    def test_initial_overrides(self):
        scenario = ScenarioConfig(
            scenario_id="imf-program",
            name="IMF program",
            description="",
            start_date=datetime(2010, 1, 1),
            end_date=datetime(2015, 1, 1),
            initial_overrides={"GRC": {"debt_gdp_ratio": 1.46}},
        )
        assert scenario.initial_overrides["GRC"]["debt_gdp_ratio"] == pytest.approx(1.46)

    def test_framework_weights(self):
        scenario = ScenarioConfig(
            scenario_id="welfare-focused",
            name="Welfare focused",
            description="",
            start_date=datetime(2020, 1, 1),
            end_date=datetime(2025, 1, 1),
            framework_weights={"human_development": 0.6, "financial": 0.4},
        )
        assert scenario.framework_weights["human_development"] == pytest.approx(0.6)


# ---------------------------------------------------------------------------
# SimulationState
# ---------------------------------------------------------------------------

class TestSimulationState:
    def _make_populated_state(self):
        bol = make_entity("BOL", "country", {"gdp": 44e9})
        bra = make_entity("BRA", "country", {"gdp": 2.2e12})

        rel_bol_bra = Relationship("BOL", "BRA", "trade", 0.3)
        rel_bra_bol = Relationship("BRA", "BOL", "trade", 0.1)

        evt_bol = make_event("e1", "BOL", "shock")
        evt_bra = make_event("e2", "BRA", "policy_change")

        return make_state(
            entities={"BOL": bol, "BRA": bra},
            relationships=[rel_bol_bra, rel_bra_bol],
            events=[evt_bol, evt_bra],
        )

    def test_get_entity_returns_entity(self):
        state = self._make_populated_state()
        entity = state.get_entity("BOL")
        assert entity is not None
        assert entity.id == "BOL"

    def test_get_entity_returns_none_for_missing(self):
        state = make_state()
        assert state.get_entity("MISSING") is None

    def test_get_relationships_from(self):
        state = self._make_populated_state()
        rels = state.get_relationships_from("BOL")
        assert len(rels) == 1
        assert rels[0].target_id == "BRA"

    def test_get_relationships_from_empty_when_none(self):
        state = make_state(entities={"BOL": make_entity("BOL")})
        assert state.get_relationships_from("BOL") == []

    def test_get_relationships_to(self):
        state = self._make_populated_state()
        rels = state.get_relationships_to("BOL")
        assert len(rels) == 1
        assert rels[0].source_id == "BRA"

    def test_get_relationships_to_empty_when_none(self):
        state = make_state(entities={"BOL": make_entity("BOL")})
        assert state.get_relationships_to("BOL") == []

    def test_get_events_for_entity(self):
        state = self._make_populated_state()
        events = state.get_events_for_entity("BOL")
        assert len(events) == 1
        assert events[0].event_id == "e1"

    def test_get_events_for_entity_empty_when_none(self):
        state = make_state()
        assert state.get_events_for_entity("BOL") == []

    def test_multiple_relationships_of_different_types(self):
        rel_trade = Relationship("BOL", "BRA", "trade", 0.3)
        rel_debt = Relationship("BOL", "IMF", "debt", 0.9)
        state = make_state(relationships=[rel_trade, rel_debt])
        rels_from_bol = state.get_relationships_from("BOL")
        assert len(rels_from_bol) == 2
        types = {r.relationship_type for r in rels_from_bol}
        assert types == {"trade", "debt"}

    def test_multiple_events_for_same_entity(self):
        e1 = make_event("e1", "BOL", "shock")
        e2 = make_event("e2", "BOL", "policy_change")
        state = make_state(events=[e1, e2])
        events = state.get_events_for_entity("BOL")
        assert len(events) == 2

    def test_state_holds_scenario_config(self):
        scenario = make_scenario("my-scenario")
        state = SimulationState(
            timestep=datetime(2020, 1, 1),
            resolution=ResolutionConfig(),
            entities={},
            relationships=[],
            events=[],
            scenario_config=scenario,
        )
        assert state.scenario_config.scenario_id == "my-scenario"


# ---------------------------------------------------------------------------
# SimulationModule abstract interface
# ---------------------------------------------------------------------------

class TestSimulationModule:
    def test_cannot_instantiate_abstract_class(self):
        with pytest.raises(TypeError):
            SimulationModule()  # type: ignore[abstract]

    def test_concrete_module_must_implement_compute(self):
        class IncompleteModule(SimulationModule):
            def get_subscribed_events(self) -> List[str]:
                return []
            # compute() not implemented

        with pytest.raises(TypeError):
            IncompleteModule()

    def test_concrete_module_must_implement_get_subscribed_events(self):
        class IncompleteModule(SimulationModule):
            def compute(self, entity, state, timestep) -> List[Event]:
                return []
            # get_subscribed_events() not implemented

        with pytest.raises(TypeError):
            IncompleteModule()

    def test_fully_implemented_module_instantiates(self):
        class ConcreteModule(SimulationModule):
            def compute(
                self,
                entity: SimulationEntity,
                state: SimulationState,
                timestep: datetime,
            ) -> List[Event]:
                return []

            def get_subscribed_events(self) -> List[str]:
                return ["shock", "policy_change"]

        module = ConcreteModule()
        assert module is not None

    def test_module_compute_returns_events(self):
        class PassThroughModule(SimulationModule):
            def compute(
                self,
                entity: SimulationEntity,
                state: SimulationState,
                timestep: datetime,
            ) -> List[Event]:
                return [make_event(source_entity_id=entity.id)]

            def get_subscribed_events(self) -> List[str]:
                return []

        module = PassThroughModule()
        entity = make_entity("BOL")
        state = make_state()
        events = module.compute(entity, state, datetime(2020, 1, 1))
        assert len(events) == 1
        assert events[0].source_entity_id == "BOL"

    def test_module_returns_empty_list_when_no_changes(self):
        class QuietModule(SimulationModule):
            def compute(self, entity, state, timestep) -> List[Event]:
                return []

            def get_subscribed_events(self) -> List[str]:
                return ["shock"]

        module = QuietModule()
        result = module.compute(make_entity(), make_state(), datetime(2020, 1, 1))
        assert result == []

    def test_module_subscribed_events_are_strings(self):
        class TradeModule(SimulationModule):
            def compute(self, entity, state, timestep) -> List[Event]:
                return []

            def get_subscribed_events(self) -> List[str]:
                return ["shock", "policy_change", "threshold_crossed"]

        module = TradeModule()
        subscriptions = module.get_subscribed_events()
        assert all(isinstance(s, str) for s in subscriptions)
        assert "shock" in subscriptions
