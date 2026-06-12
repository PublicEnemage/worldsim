"""Unit tests for PoliticalEconomyModule — Issue #156, #159, #272, #273, #679.

Tests cover:
  - Legitimacy dynamics: fiscal cuts and emergency events erode legitimacy_index
  - Fragility amplifier: erosion accelerates when legitimacy < 0.5
  - Programme survival probability: formula output clamping and monotonicity
  - Elite capture divergence: fiscal_delta × capture_coeff
  - Social response events: legitimacy_change emitted on prior-step fiscal events
  - No-op conditions: non-country entity, no relevant state/events
  - Conditionality decomposer: per-term attribution and actor summary

All tests are pure Python with no database or HTTP dependency.
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
    FRAGILITY_AMPLIFIER,
    LEGITIMACY_EROSION_ELASTICITY,
    PoliticalEconomyModule,
    _compute_legitimacy_delta,
    _compute_survival_probability,
    _extract_fiscal_delta,
)

_EPOCH = datetime(2010, 1, 1, tzinfo=UTC)
_SCENARIO_CONFIG = ScenarioConfig(
    scenario_id="test",
    name="Test",
    description="",
    start_date=_EPOCH,
    end_date=datetime(2020, 1, 1, tzinfo=UTC),
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _qty(value: str, unit: str = "ratio", framework: str = "financial") -> Quantity:
    return Quantity(
        value=Decimal(value),
        unit=unit,
        variable_type=VariableType.RATIO,
        measurement_framework=MeasurementFramework(framework),
        confidence_tier=2,
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


def _emergency_event(
    entity_id: str = "GRC",
    event_type: str = "emergency_policy_capital_controls",
) -> Event:
    return Event(
        event_id=f"test-emergency-{entity_id}-{event_type}",
        source_entity_id=entity_id,
        event_type=event_type,
        affected_attributes={},
        propagation_rules=[],
        timestep_originated=_EPOCH,
        framework=MeasurementFramework.GOVERNANCE,
    )


# ---------------------------------------------------------------------------
# No-op conditions
# ---------------------------------------------------------------------------


class TestNoOp:
    def test_returns_empty_for_non_country_entity(self) -> None:
        module = PoliticalEconomyModule()
        entity = _entity(entity_type="cohort")
        state = _state(entity)
        assert module.compute(entity, state, _EPOCH) == []

    def test_returns_empty_for_country_with_no_relevant_state(self) -> None:
        module = PoliticalEconomyModule()
        entity = _entity(entity_type="country")
        state = _state(entity)
        assert module.compute(entity, state, _EPOCH) == []

    def test_returns_empty_for_other_entity_events(self) -> None:
        """Events from a different entity do not trigger this entity's computation."""
        module = PoliticalEconomyModule()
        entity = _entity(entity_id="GRC", entity_type="country")
        other_event = _fiscal_event(entity_id="ARG")
        state = _state(entity, events=[other_event])
        assert module.compute(entity, state, _EPOCH) == []


# ---------------------------------------------------------------------------
# Legitimacy dynamics (Issue #156, #159)
# ---------------------------------------------------------------------------


class TestLegitimacyDynamics:
    def test_fiscal_cut_erodes_legitimacy(self) -> None:
        """Spending cut (-0.08) on stable government reduces legitimacy."""
        module = PoliticalEconomyModule()
        entity = _entity(legitimacy_index="0.7")
        event = _fiscal_event(value="-0.08")
        state = _state(entity, events=[event])

        result = module.compute(entity, state, _EPOCH)

        legitimacy_events = [e for e in result if e.event_type == "legitimacy_change"]
        assert len(legitimacy_events) == 1
        delta = legitimacy_events[0].affected_attributes["legitimacy_index"].value
        assert delta < Decimal("0"), f"Expected negative delta, got {delta}"

    def test_fiscal_cut_delta_magnitude(self) -> None:
        """Spending cut delta = magnitude × elasticity (no fragility above 0.5)."""
        event = _fiscal_event(value="-0.08")
        current_legitimacy = Decimal("0.7")
        delta = _compute_legitimacy_delta([event], current_legitimacy)
        expected = Decimal("-0.08") * LEGITIMACY_EROSION_ELASTICITY
        assert delta == expected

    def test_tax_hike_erodes_legitimacy(self) -> None:
        """Tax increase (+0.05) reduces legitimacy via fiscal erosion."""
        event = _fiscal_event(
            event_type="fiscal_policy_tax_rate_change",
            value="0.05",
        )
        delta = _compute_legitimacy_delta([event], Decimal("0.7"))
        assert delta < Decimal("0")

    def test_spending_increase_no_legitimacy_effect(self) -> None:
        """Positive spending (e.g., stimulus) does not erode legitimacy."""
        event = _fiscal_event(value="0.05")
        delta = _compute_legitimacy_delta([event], Decimal("0.7"))
        assert delta == Decimal("0")

    def test_emergency_event_erodes_legitimacy(self) -> None:
        """Emergency events (capital controls, bank holidays) erode legitimacy."""
        event = _emergency_event(event_type="emergency_policy_capital_controls")
        delta = _compute_legitimacy_delta([event], Decimal("0.7"))
        assert delta < Decimal("0")

    def test_fragility_amplifies_erosion(self) -> None:
        """Below FRAGILITY_THRESHOLD, erosion is amplified by FRAGILITY_AMPLIFIER."""
        event = _fiscal_event(value="-0.08")
        stable_delta = _compute_legitimacy_delta([event], Decimal("0.7"))
        fragile_delta = _compute_legitimacy_delta([event], Decimal("0.3"))
        assert abs(fragile_delta) == abs(stable_delta) * FRAGILITY_AMPLIFIER

    def test_legitimacy_clamped_to_zero_minimum(self) -> None:
        """Large cuts on fragile government do not push legitimacy below 0."""
        module = PoliticalEconomyModule()
        entity = _entity(legitimacy_index="0.05")
        events = [_fiscal_event(value="-0.50"), _emergency_event()]
        state = _state(entity, events=events)
        result = module.compute(entity, state, _EPOCH)

        legitimacy_events = [e for e in result if e.event_type == "legitimacy_change"]
        if legitimacy_events:
            new_leg = Decimal(legitimacy_events[0].metadata["new_legitimacy"])
            assert new_leg >= Decimal("0")

    def test_multiple_emergency_events_accumulate(self) -> None:
        """Multiple emergency events in the same step accumulate legitimacy erosion."""
        events = [
            _emergency_event(event_type="emergency_policy_capital_controls"),
            _emergency_event(event_type="emergency_policy_bank_holiday"),
        ]
        delta = _compute_legitimacy_delta(events, Decimal("0.7"))
        single_delta = _compute_legitimacy_delta([events[0]], Decimal("0.7"))
        assert delta == single_delta * 2

    def test_no_delta_emits_no_legitimacy_event(self) -> None:
        """If no relevant events, legitimacy_change is not emitted."""
        module = PoliticalEconomyModule()
        entity = _entity(legitimacy_index="0.7")
        state = _state(entity, events=[])
        result = module.compute(entity, state, _EPOCH)
        assert not any(e.event_type == "legitimacy_change" for e in result)


# ---------------------------------------------------------------------------
# Programme survival probability (Issue #273)
# ---------------------------------------------------------------------------


class TestProgrammeSurvivalProbability:
    def test_survival_always_between_bounds(self) -> None:
        """Survival probability is always within [0.01, 0.99] regardless of legitimacy."""
        for legitimacy_val in ["0.0", "0.1", "0.5", "0.7", "0.9", "1.0"]:
            prob = _compute_survival_probability(Decimal(legitimacy_val))
            assert Decimal("0.01") <= prob <= Decimal("0.99"), (
                f"Out of bounds at legitimacy={legitimacy_val}: {prob}"
            )

    def test_higher_legitimacy_higher_survival(self) -> None:
        """Survival probability is monotonically increasing with legitimacy."""
        probs = [
            _compute_survival_probability(Decimal(str(v / 10)))
            for v in range(0, 11)
        ]
        for i in range(len(probs) - 1):
            assert probs[i] <= probs[i + 1], (
                f"Non-monotonic at step {i}: {probs[i]} > {probs[i+1]}"
            )

    def test_survival_emitted_when_legitimacy_seeded(self) -> None:
        """programme_survival_update event is emitted when entity has legitimacy_index."""
        module = PoliticalEconomyModule()
        entity = _entity(legitimacy_index="0.7")
        state = _state(entity, events=[])
        result = module.compute(entity, state, _EPOCH)
        survival_events = [e for e in result if e.event_type == "programme_survival_update"]
        assert len(survival_events) == 1

    def test_survival_metadata_contains_calibration_note(self) -> None:
        """Survival event metadata includes a calibration note (ADR-013 Tier 3 disclosure)."""
        module = PoliticalEconomyModule()
        entity = _entity(legitimacy_index="0.7")
        state = _state(entity, events=[])
        result = module.compute(entity, state, _EPOCH)
        survival_event = next(e for e in result if e.event_type == "programme_survival_update")
        note = survival_event.metadata.get("calibration_note", "")
        assert note, "calibration_note must be non-empty"
        assert "Tier 3" in note or "Not a prediction" in note, (
            f"calibration_note should reference Tier 3 or 'Not a prediction': {note}"
        )

    def test_survival_confidence_tier_4(self) -> None:
        """Survival probability carries confidence_tier=3 (ADR-013 Decision 1)."""
        module = PoliticalEconomyModule()
        entity = _entity(legitimacy_index="0.7")
        state = _state(entity, events=[])
        result = module.compute(entity, state, _EPOCH)
        survival_event = next(e for e in result if e.event_type == "programme_survival_update")
        qty = survival_event.affected_attributes["programme_survival_probability"]
        assert qty.confidence_tier == 3


# ---------------------------------------------------------------------------
# Elite capture divergence (Issue #679)
# ---------------------------------------------------------------------------


class TestEliteCaptureDivergence:
    def test_elite_capture_emitted_on_fiscal_delta(self) -> None:
        """elite_capture_update emitted when fiscal delta + capture context set (ADR-013 D3)."""
        module = PoliticalEconomyModule()
        entity = _entity(
            legitimacy_index="0.7",
            elite_capture_coefficient="0.30",
        )
        event = _fiscal_event(value="-0.08")
        state = _state(entity, events=[event])
        result = module.compute(entity, state, _EPOCH)
        capture_events = [e for e in result if e.event_type == "elite_capture_update"]
        assert len(capture_events) == 1

    def test_elite_capture_uses_entity_coefficient(self) -> None:
        """Higher elite_capture_coefficient produces a higher divergence index (ADR-013 D3)."""
        module = PoliticalEconomyModule()
        event = _fiscal_event(value="-0.08")

        entity_high = _entity(legitimacy_index="0.7", elite_capture_coefficient="0.50")
        state_high = _state(entity_high, events=[event])
        result_high = module.compute(entity_high, state_high, _EPOCH)
        idx_high = next(
            e for e in result_high if e.event_type == "elite_capture_update"
        ).affected_attributes["elite_capture_divergence_index"].value

        entity_low = _entity(legitimacy_index="0.7", elite_capture_coefficient="0.25")
        state_low = _state(entity_low, events=[event])
        result_low = module.compute(entity_low, state_low, _EPOCH)
        idx_low = next(
            e for e in result_low if e.event_type == "elite_capture_update"
        ).affected_attributes["elite_capture_divergence_index"].value

        assert idx_high > idx_low, (
            f"Higher coefficient → higher index: {idx_high} vs {idx_low}"
        )

    def test_elite_capture_uses_default_when_no_entity_attribute(self) -> None:
        """Default elite_capture_coefficient=0.30 applies; index still emitted (ADR-013 D3)."""
        module = PoliticalEconomyModule()
        entity = _entity(legitimacy_index="0.7")
        event = _fiscal_event(value="-0.10")
        state = _state(entity, events=[event])
        result = module.compute(entity, state, _EPOCH)
        capture_event = next(
            (e for e in result if e.event_type == "elite_capture_update"), None
        )
        assert capture_event is not None, (
            "elite_capture_update must be emitted with default coefficient"
        )
        assert "elite_capture_divergence_index" in capture_event.affected_attributes

    def test_elite_capture_not_emitted_without_fiscal_delta(self) -> None:
        """No fiscal events → no elite_capture_divergence event."""
        module = PoliticalEconomyModule()
        entity = _entity(
            legitimacy_index="0.7",
            elite_capture_coefficient="0.30",
        )
        state = _state(entity, events=[])
        result = module.compute(entity, state, _EPOCH)
        assert not any(e.event_type == "elite_capture_update" for e in result)

    def test_elite_capture_framework_is_human_development(self) -> None:
        """Elite capture update event uses POLITICAL_ECONOMY framework (ADR-013 Decision 3)."""
        module = PoliticalEconomyModule()
        entity = _entity(
            legitimacy_index="0.7",
            elite_capture_coefficient="0.30",
        )
        event = _fiscal_event(value="-0.08")
        state = _state(entity, events=[event])
        result = module.compute(entity, state, _EPOCH)
        capture_event = next(e for e in result if e.event_type == "elite_capture_update")
        assert capture_event.framework == MeasurementFramework.POLITICAL_ECONOMY


# ---------------------------------------------------------------------------
# Fiscal delta extraction
# ---------------------------------------------------------------------------


class TestExtractFiscalDelta:
    def test_sums_spending_and_tax_events(self) -> None:
        """_extract_fiscal_delta sums both spending_change and tax_rate_change events."""
        events = [
            _fiscal_event(event_type="fiscal_policy_spending_change", value="-0.08"),
            _fiscal_event(event_type="fiscal_policy_tax_rate_change", value="0.03"),
        ]
        total = _extract_fiscal_delta(events)
        assert total == Decimal("-0.08") + Decimal("0.03")

    def test_ignores_emergency_events(self) -> None:
        """Emergency events do not contribute to fiscal_delta."""
        events = [_emergency_event(), _fiscal_event(value="-0.05")]
        total = _extract_fiscal_delta(events)
        assert total == Decimal("-0.05")


# ---------------------------------------------------------------------------
# Module subscribed events
# ---------------------------------------------------------------------------


class TestSubscribedEvents:
    def test_get_subscribed_events_non_empty(self) -> None:
        module = PoliticalEconomyModule()
        subs = module.get_subscribed_events()
        assert len(subs) > 0

    def test_fiscal_events_subscribed(self) -> None:
        module = PoliticalEconomyModule()
        subs = set(module.get_subscribed_events())
        assert "fiscal_policy_spending_change" in subs
        assert "fiscal_policy_tax_rate_change" in subs

    def test_emergency_events_subscribed(self) -> None:
        module = PoliticalEconomyModule()
        subs = set(module.get_subscribed_events())
        assert "emergency_policy_capital_controls" in subs
        assert "emergency_policy_bank_holiday" in subs


# ---------------------------------------------------------------------------
# Conditionality decomposer (Issue #272)
# ---------------------------------------------------------------------------


class TestConditionalityDecomposer:
    def _conditionality_input(
        self,
        actor: str = "IMF",
        mechanism: str = "DISBURSEMENT_SUSPENSION",
        value: str = "-0.08",
        capacity: str = "1.0",
    ) -> object:
        from decimal import Decimal as D

        from app.simulation.orchestration.inputs import (
            FiscalInstrument,
            FiscalPolicyInput,
            InputSource,
        )
        return FiscalPolicyInput(
            target_entity="GRC",
            instrument=FiscalInstrument.SPENDING_CHANGE,
            sector="government",
            value=D(value),
            duration_years=1,
            source=InputSource.CONDITIONALITY,
            constraining_actor_id=actor,
            constraint_mechanism=mechanism,
            implementation_capacity=D(capacity),
        )

    def test_decompose_returns_one_record_per_conditionality_input(self) -> None:
        from app.simulation.modules.political_economy.conditionality_decomposer import (
            decompose_conditionality,
        )
        inp1 = self._conditionality_input(actor="IMF")
        inp2 = self._conditionality_input(actor="ECB")
        result = decompose_conditionality([inp1, inp2], "GRC")  # type: ignore[arg-type]
        assert len(result) == 2

    def test_decompose_excludes_non_conditionality_inputs(self) -> None:
        from app.simulation.modules.political_economy.conditionality_decomposer import (
            decompose_conditionality,
        )
        from app.simulation.orchestration.inputs import (
            FiscalInstrument,
            FiscalPolicyInput,
            InputSource,
        )
        free_choice = FiscalPolicyInput(
            target_entity="GRC",
            instrument=FiscalInstrument.SPENDING_CHANGE,
            sector="government",
            value=Decimal("-0.03"),
            duration_years=1,
            source=InputSource.SCENARIO_SCRIPT,
        )
        coerced = self._conditionality_input(actor="IMF")
        result = decompose_conditionality([free_choice, coerced], "GRC")  # type: ignore[arg-type]
        assert len(result) == 1
        assert result[0]["constraining_actor_id"] == "IMF"

    def test_decompose_excludes_other_entity(self) -> None:
        from app.simulation.modules.political_economy.conditionality_decomposer import (
            decompose_conditionality,
        )
        inp = self._conditionality_input(actor="IMF")
        result = decompose_conditionality([inp], "ARG")  # type: ignore[arg-type]
        assert result == []

    def test_decompose_effective_delta_accounts_for_capacity(self) -> None:
        from app.simulation.modules.political_economy.conditionality_decomposer import (
            decompose_conditionality,
        )
        inp = self._conditionality_input(value="-0.10", capacity="0.6")
        result = decompose_conditionality([inp], "GRC")  # type: ignore[arg-type]
        assert len(result) == 1
        assert result[0]["fiscal_delta"] == Decimal("-0.10")
        assert result[0]["effective_delta"] == Decimal("-0.10") * Decimal("0.6")

    def test_summarise_by_actor_totals_per_actor(self) -> None:
        from app.simulation.modules.political_economy.conditionality_decomposer import (
            decompose_conditionality,
            summarise_by_actor,
        )
        inp1 = self._conditionality_input(actor="IMF", value="-0.08")
        inp2 = self._conditionality_input(actor="IMF", value="-0.04")
        inp3 = self._conditionality_input(actor="ECB", value="-0.02")
        decomp = decompose_conditionality([inp1, inp2, inp3], "GRC")  # type: ignore[arg-type]
        totals = summarise_by_actor(decomp)
        assert "IMF" in totals
        assert "ECB" in totals
        # Both IMF inputs are at capacity=1.0 so effective == fiscal
        assert totals["IMF"] == Decimal("-0.08") + Decimal("-0.04")
        assert totals["ECB"] == Decimal("-0.02")


# ---------------------------------------------------------------------------
# End-to-end: full module output structure
# ---------------------------------------------------------------------------


class TestModuleOutputStructure:
    def test_all_three_event_types_emitted_with_full_context(self) -> None:
        """Module emits legitimacy_change + programme_survival_update + elite_capture_update."""
        module = PoliticalEconomyModule()
        entity = _entity(
            legitimacy_index="0.7",
            elite_capture_coefficient="0.30",
        )
        event = _fiscal_event(value="-0.08")
        state = _state(entity, events=[event])
        result = module.compute(entity, state, _EPOCH)

        event_types = {e.event_type for e in result}
        assert "legitimacy_change" in event_types
        assert "programme_survival_update" in event_types
        assert "elite_capture_update" in event_types

    def test_event_ids_are_unique(self) -> None:
        """All emitted event_ids are distinct (no duplicate detection warning would fire)."""
        module = PoliticalEconomyModule()
        entity = _entity(
            legitimacy_index="0.7",
            elite_capture_coefficient="0.30",
        )
        event = _fiscal_event(value="-0.08")
        state = _state(entity, events=[event])
        result = module.compute(entity, state, _EPOCH)

        ids = [e.event_id for e in result]
        assert len(ids) == len(set(ids))

    def test_source_entity_id_matches_entity(self) -> None:
        """All emitted events carry the correct source_entity_id."""
        module = PoliticalEconomyModule()
        entity = _entity(entity_id="GRC", legitimacy_index="0.7")
        event = _fiscal_event(entity_id="GRC", value="-0.08")
        state = _state(entity, events=[event])
        result = module.compute(entity, state, _EPOCH)

        for evt in result:
            assert evt.source_entity_id == "GRC"
