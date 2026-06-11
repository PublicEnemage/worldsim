"""Regression tests for cohort entity injection after snapshot reconstruction (Issue #793).

Root cause: _inject_cohort_entities was called at step-0 initialisation but NOT
after _reconstruct_state_from_snapshot, so cohort entities were silently absent
from SimulationState at step 1 onward. DemographicModule had no cohort entities
to operate on, producing zero cohort-level trajectory data after the first step.

Fix: _inject_cohort_entities is now called immediately after reconstruction,
mirroring the initialisation path (web_scenario_runner.py line 270).

These tests exercise _inject_cohort_entities directly (no DB required).
"""
from __future__ import annotations

from datetime import datetime, timezone

from app.schemas import ScenarioConfigSchema
from app.simulation.engine.models import (
    ResolutionConfig,
    ScenarioConfig,
    SimulationEntity,
    SimulationState,
)
from app.simulation.modules.demographic.cohort import generate_cohort_specs
from app.simulation.web_scenario_runner import _inject_cohort_entities

_TS = datetime(2010, 1, 1, tzinfo=timezone.utc)  # noqa: UP017


def _make_state(entity_ids: list[str]) -> SimulationState:
    return SimulationState(
        timestep=_TS,
        resolution=ResolutionConfig(),
        entities={
            eid: SimulationEntity(id=eid, entity_type="country", attributes={}, metadata={})
            for eid in entity_ids
        },
        relationships=[],
        events=[],
        scenario_config=ScenarioConfig(
            scenario_id="test-sid",
            name="Test",
            description="",
            start_date=_TS,
            end_date=_TS,
        ),
    )


def _demo_config(enabled: bool, country_ids: list[str]) -> ScenarioConfigSchema:
    return ScenarioConfigSchema(
        entities=country_ids,
        n_steps=2,
        timestep_label="annual",
        modules_config={
            "demographic": {
                "enabled": enabled,
                "cohort_resolution_entity_ids": country_ids,
            },
        },
    )


class TestInjectCohortEntities:
    """_inject_cohort_entities correctly populates cohort entities."""

    def test_injects_100_cohort_entities_for_one_country(self) -> None:
        state = _make_state(["GRC"])
        config = _demo_config(enabled=True, country_ids=["GRC"])
        _inject_cohort_entities(state, config)
        cohort_ids = [eid for eid in state.entities if eid.startswith("GRC:CHT:")]
        assert len(cohort_ids) == 100  # 5 quintiles × 5 age bands × 4 sectors

    def test_cohort_entities_have_correct_type(self) -> None:
        state = _make_state(["GRC"])
        config = _demo_config(enabled=True, country_ids=["GRC"])
        _inject_cohort_entities(state, config)
        for eid, entity in state.entities.items():
            if eid.startswith("GRC:CHT:"):
                assert entity.entity_type == "cohort"

    def test_cohort_entities_carry_parent_id_in_metadata(self) -> None:
        state = _make_state(["GRC"])
        config = _demo_config(enabled=True, country_ids=["GRC"])
        _inject_cohort_entities(state, config)
        for eid, entity in state.entities.items():
            if eid.startswith("GRC:CHT:"):
                assert entity.metadata.get("parent_id") == "GRC"

    def test_country_entity_still_present_after_injection(self) -> None:
        state = _make_state(["GRC"])
        config = _demo_config(enabled=True, country_ids=["GRC"])
        _inject_cohort_entities(state, config)
        assert "GRC" in state.entities
        assert state.entities["GRC"].entity_type == "country"

    def test_no_injection_when_demographic_disabled(self) -> None:
        state = _make_state(["GRC"])
        config = _demo_config(enabled=False, country_ids=["GRC"])
        _inject_cohort_entities(state, config)
        cohort_ids = [eid for eid in state.entities if eid.startswith("GRC:CHT:")]
        assert len(cohort_ids) == 0

    def test_no_injection_when_modules_config_absent(self) -> None:
        state = _make_state(["GRC"])
        config = ScenarioConfigSchema(entities=["GRC"], n_steps=2, timestep_label="annual")
        _inject_cohort_entities(state, config)
        cohort_ids = [eid for eid in state.entities if eid.startswith("GRC:CHT:")]
        assert len(cohort_ids) == 0


class TestInjectCohortEntitiesIdempotence:
    """Calling _inject_cohort_entities twice does not create duplicates.

    Regression guard: the reconstruction path now calls _inject_cohort_entities
    after every snapshot load. Step 0 may have already injected some cohort
    entities via the initialisation path. Re-injection must be idempotent.
    """

    def test_double_injection_produces_same_count(self) -> None:
        state = _make_state(["GRC"])
        config = _demo_config(enabled=True, country_ids=["GRC"])
        _inject_cohort_entities(state, config)
        count_after_first = len([e for e in state.entities if e.startswith("GRC:CHT:")])
        _inject_cohort_entities(state, config)
        count_after_second = len([e for e in state.entities if e.startswith("GRC:CHT:")])
        assert count_after_first == count_after_second == 100

    def test_triple_injection_produces_same_count(self) -> None:
        state = _make_state(["GRC"])
        config = _demo_config(enabled=True, country_ids=["GRC"])
        for _ in range(3):
            _inject_cohort_entities(state, config)
        cohort_ids = [e for e in state.entities if e.startswith("GRC:CHT:")]
        assert len(cohort_ids) == 100

    def test_entity_object_identity_stable_after_double_injection(self) -> None:
        state = _make_state(["GRC"])
        config = _demo_config(enabled=True, country_ids=["GRC"])
        _inject_cohort_entities(state, config)
        sample_key = next(e for e in state.entities if e.startswith("GRC:CHT:"))
        first_entity = state.entities[sample_key]
        _inject_cohort_entities(state, config)
        assert state.entities[sample_key] is first_entity


class TestInjectCohortEntitiesMultiCountry:
    """Injection works correctly for multi-country scenarios."""

    def test_injects_200_cohort_entities_for_two_countries(self) -> None:
        state = _make_state(["GRC", "ARG"])
        config = _demo_config(enabled=True, country_ids=["GRC", "ARG"])
        _inject_cohort_entities(state, config)
        grc_cohorts = [e for e in state.entities if e.startswith("GRC:CHT:")]
        arg_cohorts = [e for e in state.entities if e.startswith("ARG:CHT:")]
        assert len(grc_cohorts) == 100
        assert len(arg_cohorts) == 100

    def test_skips_country_absent_from_state(self) -> None:
        state = _make_state(["GRC"])
        config = _demo_config(enabled=True, country_ids=["GRC", "ARG"])
        _inject_cohort_entities(state, config)
        arg_cohorts = [e for e in state.entities if e.startswith("ARG:CHT:")]
        assert len(arg_cohorts) == 0

    def test_all_100_cohort_specs_present_for_country(self) -> None:
        state = _make_state(["GRC"])
        config = _demo_config(enabled=True, country_ids=["GRC"])
        _inject_cohort_entities(state, config)
        specs = generate_cohort_specs()
        for spec in specs:
            assert spec.entity_id("GRC") in state.entities, (
                f"Missing cohort entity {spec.entity_id('GRC')}"
            )
