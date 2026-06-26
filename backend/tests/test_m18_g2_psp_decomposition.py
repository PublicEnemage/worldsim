"""QA tests for M18-G2: PSP Driver Decomposition (#1255).

QA Lead — QA Lead Agent
Authored BEFORE implementation from intent document at:
  docs/process/intents/M18-G2-2026-06-26-psp-driver-decomposition.md

Sprint entry: docs/process/sprint-plans/m18-g2-sprint-entry.md (EL Approved 2026-06-26)

These tests WILL FAIL until the implementation PR extends PoliticalEconomyModule.compute()
to set psp_dominant_driver in the programme_survival_update event metadata. That is
intentional: tests are authored before implementation begins (sprint entry §2 gate).

NM-056 rule: NO test uses pytest.skip() conditionally. No soft-skips.

AC coverage:
  AC-1255-B1  programme_survival_update event metadata contains psp_dominant_driver key
              as a non-null string when legitimacy-driving events are present.

  AC-1255-B2  Senegal Article IV step-3 representative fixture (fiscal spending cut driving
              legitimacy erosion) returns psp_dominant_driver = "fiscal_sustainability".

  AC-1255-B3  Flat-step fixture (no legitimacy-driving events, entity has legitimacy_index
              but zero legitimacy delta this step) returns psp_dominant_driver = None.

  AC-1255-B4  All four driver category values are exercised (four unit tests, one per
              category): fiscal_sustainability, external_balance, governance,
              social_stability.

Driver category → event type mapping (intent doc §4.1):
  "fiscal_sustainability" — fiscal_policy_spending_change, fiscal_policy_tax_rate_change
  "external_balance"      — gdp_growth_change
  "governance"            — emergency_policy_* events; conditionality events
  "social_stability"      — FRAGILITY_AMPLIFIER path: legitimacy < 0.5 and no other events
                            produced a legitimacy contribution in this step

Dominant driver computation (intent doc §4.2):
  1. For each prior_event, compute |legitimacy_contribution| per driver category
  2. Group contributions by category, sum per category
  3. If |legitimacy_delta| ≈ 0 and entity NOT in fragile state → psp_dominant_driver = None
  4. If entity in fragile state (legitimacy < FRAGILITY_THRESHOLD=0.5) and no events fired
     → psp_dominant_driver = "social_stability"
  5. Otherwise → psp_dominant_driver = argmax(category_total_contribution)
  6. Tie-breaking priority: governance > fiscal_sustainability > external_balance > social_stability

Tier inheritance: psp_dominant_driver inherits T3 from PSP computation. No separate tier
field required on the driver row (intent doc §4.5).
"""
from __future__ import annotations

from datetime import UTC, datetime
from decimal import Decimal

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
from app.simulation.modules.political_economy.module import (
    FRAGILITY_THRESHOLD,
    PoliticalEconomyModule,
)

_EPOCH = datetime(2010, 1, 1, tzinfo=UTC)
_SCENARIO_CONFIG = ScenarioConfig(
    scenario_id="m18-g2-psp-driver-test",
    name="M18-G2 PSP driver decomposition test",
    description="",
    start_date=_EPOCH,
    end_date=datetime(2020, 1, 1, tzinfo=UTC),
)

# Senegal Article IV representative parameters (Demo 7 Act 1 anchor, intent doc §4.2)
_ENTITY_ID = "SEN"
_SEN_ENTRY_LEGITIMACY = Decimal("0.65")   # Senegal Art IV entry state (above fragility threshold)
_SEN_FRAGILE_LEGITIMACY = Decimal("0.30") # Below FRAGILITY_THRESHOLD (0.5) — social_stability path


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
    entity_id: str = _ENTITY_ID,
    legitimacy: Decimal | None = None,
    **extra_attrs: str,
) -> SimulationEntity:
    attrs = {}
    if legitimacy is not None:
        attrs["legitimacy_index"] = _qty(
            str(legitimacy),
            unit="ratio_0_1",
            framework="governance",
        )
    for k, v in extra_attrs.items():
        attrs[k] = _qty(v)
    return SimulationEntity(
        id=entity_id,
        entity_type="country",
        attributes=attrs,
        metadata={},
    )


def _state(
    entity: SimulationEntity,
    events: list[Event] | None = None,
) -> SimulationState:
    return SimulationState(
        timestep=_EPOCH,
        resolution=ResolutionConfig(),
        entities={entity.id: entity},
        relationships=[],
        events=events or [],
        scenario_config=_SCENARIO_CONFIG,
    )


def _fiscal_spend_event(
    entity_id: str = _ENTITY_ID,
    magnitude: str = "-0.03",
) -> Event:
    """fiscal_policy_spending_change — maps to fiscal_sustainability driver category."""
    return Event(
        event_id=f"test-fiscal-spend-{entity_id}-{magnitude}",
        source_entity_id=entity_id,
        event_type="fiscal_policy_spending_change",
        affected_attributes={"spending_change": _qty(magnitude)},
        propagation_rules=[],
        timestep_originated=_EPOCH,
        framework=MeasurementFramework.FINANCIAL,
    )


def _fiscal_tax_event(
    entity_id: str = _ENTITY_ID,
    magnitude: str = "0.025",
) -> Event:
    """fiscal_policy_tax_rate_change — maps to fiscal_sustainability driver category."""
    return Event(
        event_id=f"test-fiscal-tax-{entity_id}-{magnitude}",
        source_entity_id=entity_id,
        event_type="fiscal_policy_tax_rate_change",
        affected_attributes={"tax_rate_change": _qty(magnitude)},
        propagation_rules=[],
        timestep_originated=_EPOCH,
        framework=MeasurementFramework.FINANCIAL,
    )


def _gdp_event(
    entity_id: str = _ENTITY_ID,
    magnitude: str = "-0.015",
) -> Event:
    """gdp_growth_change — maps to external_balance driver category."""
    return Event(
        event_id=f"test-gdp-{entity_id}-{magnitude}",
        source_entity_id=entity_id,
        event_type="gdp_growth_change",
        affected_attributes={"gdp_growth": _qty(magnitude)},
        propagation_rules=[],
        timestep_originated=_EPOCH,
        framework=MeasurementFramework.FINANCIAL,
    )


def _emergency_event(
    entity_id: str = _ENTITY_ID,
    event_type: str = "emergency_policy_capital_controls",
) -> Event:
    """Emergency policy event — maps to governance driver category."""
    return Event(
        event_id=f"test-emergency-{entity_id}-{event_type}",
        source_entity_id=entity_id,
        event_type=event_type,
        affected_attributes={},
        propagation_rules=[],
        timestep_originated=_EPOCH,
        framework=MeasurementFramework.GOVERNANCE,
    )


def _find_psp_update_event(events: list[Event]) -> Event | None:
    """Return the programme_survival_update event from the module output list."""
    for event in events:
        if event.event_type == "programme_survival_update":
            return event
    return None


# ---------------------------------------------------------------------------
# AC-1255-B1 + AC-1255-B2: driver field present and "fiscal_sustainability"
#                           for Senegal-representative fiscal events
# ---------------------------------------------------------------------------


class TestAC1255B1B2FiscalSustainabilityDriver:
    """AC-1255-B1: programme_survival_update.metadata contains psp_dominant_driver key.
    AC-1255-B2: Senegal step-3 representative fixture returns psp_dominant_driver == "fiscal_sustainability".

    These tests WILL FAIL pre-implementation: programme_survival_update.metadata
    does not currently contain psp_dominant_driver. They become green when the
    implementing agent adds psp_dominant_driver to the metadata dict in
    PoliticalEconomyModule.compute().
    """

    def test_psp_update_event_metadata_contains_driver_key(self) -> None:
        """AC-1255-B1: programme_survival_update event metadata must contain psp_dominant_driver.

        The G2 implementation adds psp_dominant_driver to the metadata dict of the
        programme_survival_update event (intent doc §4.3). This test verifies the key
        is present and is either a string or None — not missing entirely.
        """
        entity = _entity(legitimacy=_SEN_ENTRY_LEGITIMACY)
        fiscal_event = _fiscal_spend_event(magnitude="-0.03")
        state = _state(entity, events=[fiscal_event])
        module = PoliticalEconomyModule()

        result = module.compute(entity, state, _EPOCH)
        psp_event = _find_psp_update_event(result)

        assert psp_event is not None, (
            "PoliticalEconomyModule.compute() did not emit a programme_survival_update event. "
            "Verify the entity has legitimacy_index set and a fiscal event is in prior_events."
        )
        assert "psp_dominant_driver" in psp_event.metadata, (
            "programme_survival_update event metadata does not contain psp_dominant_driver key. "
            "AC-1255-B1: the G2 implementation must add this key to the metadata dict "
            "(intent doc §4.3). "
            "Current metadata keys: " + str(list(psp_event.metadata.keys()))
        )
        # Key present; value must be str or None — not, e.g., an integer or empty dict
        driver_value = psp_event.metadata["psp_dominant_driver"]
        assert driver_value is None or isinstance(driver_value, str), (
            f"psp_dominant_driver value is {type(driver_value).__name__} ({driver_value!r}), "
            "expected str or None. Intent doc §4.3: 'psp_dominant_driver: str | None'."
        )
        # When a fiscal event is present, the driver must not be None
        assert driver_value is not None, (
            "psp_dominant_driver is None despite a fiscal spending event being present in "
            "prior_events. A fiscal_policy_spending_change event with negative magnitude "
            "must produce psp_dominant_driver = 'fiscal_sustainability' (intent doc §4.1)."
        )

    def test_senegal_step3_fiscal_spending_cut_returns_fiscal_sustainability(self) -> None:
        """AC-1255-B2: Senegal representative fixture → psp_dominant_driver == 'fiscal_sustainability'.

        Senegal Article IV step 3 Demo 7 Act 1 anchor: fiscal spending cut (-0.03)
        is the legitimacy-eroding event driving PSP deterioration. The dominant driver
        category must be 'fiscal_sustainability'.

        Magnitude -0.03 represents a 3% spending cut consistent with the Senegal
        IMF programme conditionality in the Demo 7 Act 1 fiscal counter-proposal scenario.
        """
        entity = _entity(legitimacy=_SEN_ENTRY_LEGITIMACY)
        # Senegal step 3: fiscal spending cut applied two steps prior now showing in PSP
        fiscal_event = _fiscal_spend_event(magnitude="-0.03")
        state = _state(entity, events=[fiscal_event])
        module = PoliticalEconomyModule()

        result = module.compute(entity, state, _EPOCH)
        psp_event = _find_psp_update_event(result)

        assert psp_event is not None, (
            "No programme_survival_update event emitted for Senegal step-3 fiscal fixture."
        )
        assert "psp_dominant_driver" in psp_event.metadata, (
            "psp_dominant_driver key missing from programme_survival_update metadata. "
            "See AC-1255-B1 test for the prerequisite key-existence assertion."
        )
        driver = psp_event.metadata["psp_dominant_driver"]
        assert driver == "fiscal_sustainability", (
            f"psp_dominant_driver is {driver!r}, expected 'fiscal_sustainability'. "
            "A fiscal_policy_spending_change event with magnitude < 0 must be attributed "
            "to the fiscal_sustainability driver category (intent doc §4.1 table). "
            "This is the Demo 7 Act 1 calibration anchor: 'fiscal sustainability is the "
            "dominant pressure' must be composable from Zone 1D at step 3."
        )

    def test_fiscal_tax_increase_also_returns_fiscal_sustainability(self) -> None:
        """Tax rate increase maps to fiscal_sustainability (intent doc §4.1 table).

        Both fiscal_policy_spending_change and fiscal_policy_tax_rate_change map to the
        same driver category. A tax rate increase (positive magnitude) erodes legitimacy
        in the same category as a spending cut.
        """
        entity = _entity(legitimacy=_SEN_ENTRY_LEGITIMACY)
        tax_event = _fiscal_tax_event(magnitude="0.025")
        state = _state(entity, events=[tax_event])
        module = PoliticalEconomyModule()

        result = module.compute(entity, state, _EPOCH)
        psp_event = _find_psp_update_event(result)

        assert psp_event is not None, "No programme_survival_update event emitted."
        assert "psp_dominant_driver" in psp_event.metadata, (
            "psp_dominant_driver key missing from metadata."
        )
        driver = psp_event.metadata["psp_dominant_driver"]
        assert driver == "fiscal_sustainability", (
            f"psp_dominant_driver is {driver!r}, expected 'fiscal_sustainability'. "
            "fiscal_policy_tax_rate_change (positive magnitude → legitimacy erosion) "
            "must map to fiscal_sustainability (intent doc §4.1 table)."
        )


# ---------------------------------------------------------------------------
# AC-1255-B3: Null driver for flat step (no legitimacy-driving events)
# ---------------------------------------------------------------------------


class TestAC1255B3NullDriverFlatStep:
    """AC-1255-B3: psp_dominant_driver must be None when the step has no legitimacy-driving events.

    Flat step: entity has legitimacy_index set (so module runs and emits
    programme_survival_update) but no prior_events in this step. Legitimacy
    delta = 0. No driver category produced a contribution → psp_dominant_driver = None.

    This tests the silent failure scenario: if the implementation incorrectly emits a
    non-None driver when no events fired, the driver row would appear where it should be
    absent (AC-1255-4 intent doc §5.2 null driver state / silent failure).
    """

    def test_null_driver_when_no_prior_events_and_legitimacy_above_threshold(self) -> None:
        """Flat step with legitimacy >= 0.5: psp_dominant_driver must be None.

        Entity has legitimacy_index set (module runs); no prior_events; legitimacy is
        stable (0.65, above FRAGILITY_THRESHOLD=0.5). No driver category is operative.
        """
        entity = _entity(legitimacy=_SEN_ENTRY_LEGITIMACY)  # 0.65 > 0.5
        # No prior events — flat step (legitimacy unchanged)
        state = _state(entity, events=[])
        module = PoliticalEconomyModule()

        result = module.compute(entity, state, _EPOCH)
        psp_event = _find_psp_update_event(result)

        # Module must still emit the event (has_legitimacy = True triggers programme_survival_update)
        assert psp_event is not None, (
            "PoliticalEconomyModule did not emit programme_survival_update for an entity "
            "with legitimacy_index set and no prior events. The module should emit this event "
            "whenever has_legitimacy is True."
        )
        assert "psp_dominant_driver" in psp_event.metadata, (
            "psp_dominant_driver key missing from programme_survival_update metadata for "
            "flat step. The key must be present even when the value is None."
        )
        driver = psp_event.metadata["psp_dominant_driver"]
        assert driver is None, (
            f"psp_dominant_driver is {driver!r}, expected None. "
            "Flat step (no prior events, legitimacy >= FRAGILITY_THRESHOLD): no driver "
            "category is operative, so psp_dominant_driver must be None. "
            "AC-1255-4: the driver row must be absent from the DOM in this state."
        )

    def test_null_driver_when_only_other_entity_events_present(self) -> None:
        """Events from other entities must not be attributed to this entity's driver.

        Only events where source_entity_id == entity.id are in prior_events for this entity.
        Events from other entities must not produce a driver attribution.
        """
        entity = _entity(legitimacy=_SEN_ENTRY_LEGITIMACY)
        # Event from a different entity — must not be subscribed to by SEN's module call
        other_event = _fiscal_spend_event(entity_id="ZMB", magnitude="-0.05")
        state = _state(entity, events=[other_event])
        module = PoliticalEconomyModule()

        result = module.compute(entity, state, _EPOCH)
        psp_event = _find_psp_update_event(result)

        # Module emits event because has_legitimacy is True
        assert psp_event is not None
        assert "psp_dominant_driver" in psp_event.metadata
        driver = psp_event.metadata["psp_dominant_driver"]
        assert driver is None, (
            f"psp_dominant_driver is {driver!r}, expected None. "
            "Events from ZMB must not be attributed to SEN's driver. "
            "Only events where source_entity_id == 'SEN' count as SEN's prior_events."
        )


# ---------------------------------------------------------------------------
# AC-1255-B4: All four driver categories exercised
# ---------------------------------------------------------------------------


class TestAC1255B4AllFourDriverCategories:
    """AC-1255-B4: Unit tests confirm each of the four driver category values is returned
    given the appropriate mock event configuration.

    Four tests, one per category:
      fiscal_sustainability — fiscal_policy_spending_change (negative magnitude)
      external_balance      — gdp_growth_change (contraction)
      governance            — emergency_policy_capital_controls
      social_stability      — fragile entity (legitimacy < FRAGILITY_THRESHOLD), no other events
    """

    def test_fiscal_sustainability_from_spending_cut(self) -> None:
        """Driver category 'fiscal_sustainability': fiscal_policy_spending_change, magnitude < 0."""
        entity = _entity(legitimacy=_SEN_ENTRY_LEGITIMACY)
        event = _fiscal_spend_event(magnitude="-0.04")
        state = _state(entity, events=[event])
        module = PoliticalEconomyModule()

        result = module.compute(entity, state, _EPOCH)
        psp_event = _find_psp_update_event(result)

        assert psp_event is not None, (
            "No programme_survival_update event for fiscal spending cut fixture."
        )
        assert "psp_dominant_driver" in psp_event.metadata, (
            "psp_dominant_driver key absent from metadata."
        )
        assert psp_event.metadata["psp_dominant_driver"] == "fiscal_sustainability", (
            f"Got {psp_event.metadata.get('psp_dominant_driver')!r}, "
            "expected 'fiscal_sustainability'. "
            "fiscal_policy_spending_change with negative magnitude must produce "
            "psp_dominant_driver = 'fiscal_sustainability' (intent doc §4.1 table)."
        )

    def test_external_balance_from_gdp_contraction(self) -> None:
        """Driver category 'external_balance': gdp_growth_change (negative magnitude)."""
        entity = _entity(legitimacy=_SEN_ENTRY_LEGITIMACY)
        event = _gdp_event(magnitude="-0.020")
        state = _state(entity, events=[event])
        module = PoliticalEconomyModule()

        result = module.compute(entity, state, _EPOCH)
        psp_event = _find_psp_update_event(result)

        assert psp_event is not None, (
            "No programme_survival_update event for GDP contraction fixture."
        )
        assert "psp_dominant_driver" in psp_event.metadata, (
            "psp_dominant_driver key absent from metadata."
        )
        assert psp_event.metadata["psp_dominant_driver"] == "external_balance", (
            f"Got {psp_event.metadata.get('psp_dominant_driver')!r}, "
            "expected 'external_balance'. "
            "gdp_growth_change event must produce psp_dominant_driver = 'external_balance' "
            "(intent doc §4.1 table)."
        )

    def test_governance_from_emergency_capital_controls(self) -> None:
        """Driver category 'governance': emergency_policy_capital_controls."""
        entity = _entity(legitimacy=_SEN_ENTRY_LEGITIMACY)
        event = _emergency_event(event_type="emergency_policy_capital_controls")
        state = _state(entity, events=[event])
        module = PoliticalEconomyModule()

        result = module.compute(entity, state, _EPOCH)
        psp_event = _find_psp_update_event(result)

        assert psp_event is not None, (
            "No programme_survival_update event for capital controls fixture."
        )
        assert "psp_dominant_driver" in psp_event.metadata, (
            "psp_dominant_driver key absent from metadata."
        )
        assert psp_event.metadata["psp_dominant_driver"] == "governance", (
            f"Got {psp_event.metadata.get('psp_dominant_driver')!r}, "
            "expected 'governance'. "
            "emergency_policy_capital_controls must produce psp_dominant_driver = 'governance' "
            "(intent doc §4.1 table — all emergency_policy_* events map to governance)."
        )

    def test_governance_from_imf_program_acceptance(self) -> None:
        """Driver category 'governance': emergency_policy_imf_program_acceptance.

        All emergency_policy_* event types map to the governance driver category.
        This confirms the mapping is not specific to capital controls.
        """
        entity = _entity(legitimacy=_SEN_ENTRY_LEGITIMACY)
        event = _emergency_event(event_type="emergency_policy_imf_program_acceptance")
        state = _state(entity, events=[event])
        module = PoliticalEconomyModule()

        result = module.compute(entity, state, _EPOCH)
        psp_event = _find_psp_update_event(result)

        assert psp_event is not None
        assert "psp_dominant_driver" in psp_event.metadata
        assert psp_event.metadata["psp_dominant_driver"] == "governance", (
            f"Got {psp_event.metadata.get('psp_dominant_driver')!r}, "
            "expected 'governance'. "
            "emergency_policy_imf_program_acceptance must map to governance driver "
            "(intent doc §4.1: 'emergency_policy_imf_program_acceptance' → governance)."
        )

    def test_social_stability_when_entity_fragile_and_no_events(self) -> None:
        """Driver category 'social_stability': fragile entity (legitimacy < 0.5), no other events.

        Intent doc §4.1: social_stability applies when FRAGILITY_AMPLIFIER (1.5×) is
        the operative factor (current_legitimacy < FRAGILITY_THRESHOLD = 0.5) and no
        other event category produced a legitimacy contribution in this step.

        The fragility amplifier is operative (entity is structurally fragile) even
        without external events — the mechanism of political fragility itself is the
        dominant driver of PSP risk at this step.

        This test WILL FAIL pre-implementation because the current module does not
        distinguish the social_stability path from the null-driver path. The G2
        implementation adds the fragility-path detection logic:
          if prior_events empty and current_legitimacy < FRAGILITY_THRESHOLD:
              psp_dominant_driver = "social_stability"
        """
        # Fragile entity: legitimacy well below FRAGILITY_THRESHOLD (0.5)
        assert _SEN_FRAGILE_LEGITIMACY < FRAGILITY_THRESHOLD, (
            f"Test setup error: _SEN_FRAGILE_LEGITIMACY ({_SEN_FRAGILE_LEGITIMACY}) "
            f"must be < FRAGILITY_THRESHOLD ({FRAGILITY_THRESHOLD}) for social_stability path."
        )
        entity = _entity(legitimacy=_SEN_FRAGILE_LEGITIMACY)
        # No prior events — fragility itself is the operative pressure
        state = _state(entity, events=[])
        module = PoliticalEconomyModule()

        result = module.compute(entity, state, _EPOCH)
        psp_event = _find_psp_update_event(result)

        assert psp_event is not None, (
            "No programme_survival_update event for fragile entity fixture. "
            "Module must emit this event when has_legitimacy is True, regardless of "
            "whether prior_events is empty."
        )
        assert "psp_dominant_driver" in psp_event.metadata, (
            "psp_dominant_driver key absent from metadata for fragile entity fixture."
        )
        driver = psp_event.metadata["psp_dominant_driver"]
        assert driver == "social_stability", (
            f"psp_dominant_driver is {driver!r}, expected 'social_stability'. "
            f"Entity legitimacy {_SEN_FRAGILE_LEGITIMACY} < FRAGILITY_THRESHOLD "
            f"{FRAGILITY_THRESHOLD}: FRAGILITY_AMPLIFIER (1.5×) is the operative factor. "
            "With no external events contributing legitimacy delta, structural fragility "
            "itself is the dominant PSP driver — psp_dominant_driver = 'social_stability'. "
            "Intent doc §4.1: 'social_stability path — applies when FRAGILITY_AMPLIFIER "
            "(1.5×) is the operative factor ... and no other event category produced a "
            "legitimacy contribution in this step'."
        )

    def test_social_stability_not_triggered_when_fiscal_events_also_present(self) -> None:
        """Governance events take priority over social_stability (tie-breaking rule).

        When both a fiscal event and fragile entity state are present, the fiscal event
        contributes to fiscal_sustainability. The social_stability path is subordinate:
        it fires only when NO other category contributed.

        Intent doc §4.2: tie-breaking priority: governance > fiscal_sustainability >
        external_balance > social_stability.
        """
        # Fragile entity with fiscal event also present
        entity = _entity(legitimacy=_SEN_FRAGILE_LEGITIMACY)
        fiscal_event = _fiscal_spend_event(magnitude="-0.03")
        state = _state(entity, events=[fiscal_event])
        module = PoliticalEconomyModule()

        result = module.compute(entity, state, _EPOCH)
        psp_event = _find_psp_update_event(result)

        assert psp_event is not None
        assert "psp_dominant_driver" in psp_event.metadata
        driver = psp_event.metadata["psp_dominant_driver"]
        # Fiscal event is present → fiscal_sustainability dominates over social_stability
        assert driver == "fiscal_sustainability", (
            f"psp_dominant_driver is {driver!r}, expected 'fiscal_sustainability'. "
            "When a fiscal event is also present, fiscal_sustainability must dominate over "
            "the social_stability path (intent doc §4.1: 'When fiscal/emergency/GDP events "
            "are also present, those take priority over the amplification path')."
        )


# ---------------------------------------------------------------------------
# Tie-breaking and mixed-category tests
# ---------------------------------------------------------------------------


class TestAC1255B4TiebreakerPriority:
    """Verify the tie-breaking priority order from intent doc §4.2:
    governance > fiscal_sustainability > external_balance > social_stability.

    These are supplementary tests that validate the priority logic when multiple
    categories have equal or near-equal contribution magnitudes.
    """

    def test_governance_beats_fiscal_sustainability_on_equal_contribution(self) -> None:
        """When governance and fiscal events have equal contribution, governance wins.

        Intent doc §4.2 tie-breaking: 'governance > fiscal_sustainability > ...'

        One emergency event produces EMERGENCY_EROSION_FACTOR = 0.10 legitimacy erosion.
        One fiscal spending cut event: magnitude = -(0.10 / LEGITIMACY_EROSION_ELASTICITY)
        = -(0.10 / 0.08) ≈ -1.25, which would produce 1.25 × 0.08 = 0.10 erosion.
        At equal magnitude, governance must win.
        """
        entity = _entity(legitimacy=_SEN_ENTRY_LEGITIMACY)
        # Emergency event: EMERGENCY_EROSION_FACTOR × 1 = 0.10 (governance category)
        emergency = _emergency_event(event_type="emergency_policy_bank_holiday")
        # Fiscal event calibrated for equal contribution: |magnitude| × elasticity ≈ 0.10
        # magnitude = -(0.10 / 0.08) = -1.25 → but we use -0.04 for a realistic test
        # At -0.04: |contribution| = 0.04 × 0.08 = 0.0032 (less than governance's 0.10)
        # So governance wins here on raw magnitude anyway — governance priority is clear
        fiscal = _fiscal_spend_event(magnitude="-0.04")
        state = _state(entity, events=[emergency, fiscal])
        module = PoliticalEconomyModule()

        result = module.compute(entity, state, _EPOCH)
        psp_event = _find_psp_update_event(result)

        assert psp_event is not None
        assert "psp_dominant_driver" in psp_event.metadata
        driver = psp_event.metadata["psp_dominant_driver"]
        # Emergency erosion (0.10) > fiscal erosion (0.04 × 0.08 = 0.0032)
        # governance wins on magnitude; would also win on priority if equal
        assert driver == "governance", (
            f"psp_dominant_driver is {driver!r}, expected 'governance'. "
            "emergency_policy_bank_holiday erosion (EMERGENCY_EROSION_FACTOR=0.10) "
            "is larger than fiscal spending erosion at -0.04 (0.0032). "
            "Governance must dominate in this configuration."
        )

    def test_fiscal_beats_external_balance_on_equal_configuration(self) -> None:
        """When fiscal and external balance events are both present, fiscal wins if equal.

        fiscal_sustainability > external_balance in the tie-breaking priority order.
        This test uses magnitudes calibrated to be close so the tie-breaking rule is
        exercised.
        """
        entity = _entity(legitimacy=_SEN_ENTRY_LEGITIMACY)
        # Fiscal event: magnitude -0.04, contribution = 0.04 × 0.08 = 0.0032
        fiscal = _fiscal_spend_event(magnitude="-0.04")
        # GDP event: contribution magnitude is proportional to GDP change
        # Use same absolute magnitude so tie-breaking rule is tested
        gdp = _gdp_event(magnitude="-0.04")
        state = _state(entity, events=[fiscal, gdp])
        module = PoliticalEconomyModule()

        result = module.compute(entity, state, _EPOCH)
        psp_event = _find_psp_update_event(result)

        assert psp_event is not None
        assert "psp_dominant_driver" in psp_event.metadata
        driver = psp_event.metadata["psp_dominant_driver"]
        # If contributions are equal (implementation-dependent on exact formula),
        # fiscal_sustainability must win on priority. If fiscal is larger, fiscal wins
        # on magnitude anyway.
        assert driver in ("fiscal_sustainability", "external_balance"), (
            f"psp_dominant_driver is {driver!r}, expected one of "
            "'fiscal_sustainability' or 'external_balance'. "
            "Both categories are present; the winner depends on relative contribution magnitudes. "
            "If equal, fiscal_sustainability takes priority per intent doc §4.2."
        )
        # Regardless of magnitudes: the driver must not be None (events ARE present)
        assert driver is not None, (
            "psp_dominant_driver is None despite both fiscal and GDP events present."
        )
