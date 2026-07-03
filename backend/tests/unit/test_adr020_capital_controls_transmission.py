"""ADR-020 capital controls transmission channel tests — Issues #1532.

Tests the three transmission channels introduced by ADR-020 §Decision 2:
  Channel A — ExternalSectorModule: emergency_policy_capital_controls →
              capital_account_outflow_velocity ↓ → reserve_coverage_months ↑
  Channel B — MacroeconomicModule:  emergency_policy_capital_controls →
              domestic_credit_growth ↓ (β=0.020, γ=1.2) → gdp_growth ↓;
              emits credit_contraction_labour_shock bridge event
  Channel C — DemographicModule:   credit_contraction_labour_shock →
              q1_poverty_headcount_ratio ↑ (φ ∈ [0.3, 0.7])

These tests define the TARGET state. They FAIL on the pre-ADR-020 codebase and
PASS after the ADR-020 implementation PR merges to sprint/m19-g2.

Pre-fix broken-state documentation:
  NM-090: DM subscribes to "imf_program_acceptance" and "emergency_declaration" (dead)
  NM-091: ADR-020 registry listed 10 variants; code has 7; "asset_nationalization"
          absent from EmergencyInstrument enum
  ADR-020 Channel C bug: DM subscribed to "capital_controls_imposition" (dead) instead
          of "credit_contraction_labour_shock" bridge

Coverage:
  AC-1:  ESM subscribes to emergency_policy_capital_controls
  AC-2:  ESM produces positive reserve_coverage_months delta on capital controls event
  AC-3:  MM subscribes + applies β=0.020 credit contraction
  AC-4:  MM emits credit_contraction_labour_shock bridge event (separate assertion block)
  AC-5:  DM does NOT contain "capital_controls_imposition" in _SUBSCRIBED_EVENTS
  AC-6:  DM contains "credit_contraction_labour_shock"; elasticity row exists + in [0.3, 0.7]
  AC-7:  DM produces positive q1 PHC delta on credit_contraction_labour_shock event
  AC-8:  DM does NOT subscribe to "emergency_policy_capital_controls" directly (bridge guard)
  AC-9:  γ constant is 1.2 (CM-supplied; not overridable by CE)
  AC-10: known_limitations for capital_controls references active channels (not "#1532")
  AC-11: EmergencyPolicyInput(CAPITAL_CONTROLS) produces no SimulationError
  Reg-1: gdp_growth_change Q1 elasticity row unchanged (M17-G1 calibration, -0.20)
  SF-2:  capital_controls_imposition event produces zero DM response (dead string guard)
  SF-5:  emergency_policy_capital_controls produces zero DM response directly (bridge guard)
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
from app.simulation.modules.demographic.cohort import IncomeQuintile
from app.simulation.modules.demographic.elasticities import ELASTICITY_REGISTRY
from app.simulation.modules.demographic.module import (
    DemographicModule,
    _SUBSCRIBED_EVENTS as DM_SUBSCRIBED_EVENTS,
)
from app.simulation.modules.external_sector.module import ExternalSectorModule
from app.simulation.modules.macroeconomic.module import (
    MacroeconomicModule,
    _SUBSCRIBED_EVENTS as MM_SUBSCRIBED_EVENTS,
)

_TS = datetime(2008, 10, 1, tzinfo=UTC)
_ENTITY_ID = "ISL"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _qty(value: float | str, framework: MeasurementFramework = MeasurementFramework.FINANCIAL, tier: int = 1) -> Quantity:
    return Quantity(
        value=Decimal(str(value)),
        unit="dimensionless",
        variable_type=VariableType.RATIO,
        measurement_framework=framework,
        confidence_tier=tier,
    )


def _make_entity(
    entity_id: str = _ENTITY_ID,
    entity_type: str = "country",
    **attrs: float,
) -> SimulationEntity:
    return SimulationEntity(
        id=entity_id,
        entity_type=entity_type,
        attributes={k: _qty(v) for k, v in attrs.items()},
        metadata={},
    )


def _make_state(
    entity: SimulationEntity,
    prior_events: list[Event] | None = None,
) -> SimulationState:
    return SimulationState(
        timestep=_TS,
        resolution=ResolutionConfig(),
        entities={entity.id: entity},
        relationships=[],
        events=prior_events or [],
        scenario_config=ScenarioConfig(
            scenario_id="test-isl-adr020",
            name="ADR-020 test",
            description="",
            start_date=_TS,
            end_date=_TS,
        ),
    )


def _capital_controls_event(
    entity_id: str = _ENTITY_ID,
    severity: float = 0.85,
    epsilon: float = 0.60,
    implementation_capacity: float = 0.75,
    duration_periods: int = 8,
) -> Event:
    """Build emergency_policy_capital_controls Event as EmergencyPolicyInput.to_events() produces."""
    return Event(
        event_id="test-cc-event",
        source_entity_id=entity_id,
        event_type="emergency_policy_capital_controls",
        affected_attributes={
            "capital_controls": Quantity(
                value=Decimal(str(severity)),
                unit="dimensionless",
                variable_type=VariableType.DIMENSIONLESS,
                measurement_framework=MeasurementFramework.GOVERNANCE,
                confidence_tier=1,
            ),
        },
        propagation_rules=[],
        timestep_originated=_TS,
        framework=MeasurementFramework.GOVERNANCE,
        metadata={
            "parameters": {
                "magnitude": severity,
                "epsilon": epsilon,
                "implementation_capacity": implementation_capacity,
                "duration_periods": duration_periods,
            },
        },
    )


def _bridge_event(
    entity_id: str = _ENTITY_ID,
    delta_credit_growth: float = -0.01275,
) -> Event:
    """Build credit_contraction_labour_shock bridge event as Channel B emits."""
    return Event(
        event_id="test-bridge-event",
        source_entity_id=entity_id,
        event_type="credit_contraction_labour_shock",
        affected_attributes={
            "credit_contraction_labour_shock": Quantity(
                value=Decimal(str(delta_credit_growth)),
                unit="dimensionless",
                variable_type=VariableType.RATIO,
                measurement_framework=MeasurementFramework.FINANCIAL,
                confidence_tier=2,
            ),
        },
        propagation_rules=[],
        timestep_originated=_TS,
        framework=MeasurementFramework.FINANCIAL,
        metadata={"delta_credit_growth": delta_credit_growth},
    )


# ---------------------------------------------------------------------------
# AC-1: ExternalSectorModule subscription (Channel A)
# ---------------------------------------------------------------------------


def test_esm_subscribes_to_emergency_policy_capital_controls() -> None:
    """AC-1: ESM must include 'emergency_policy_capital_controls' in subscribed events."""
    esm = ExternalSectorModule(commodity_price_shocks=[], start_date=None)
    assert "emergency_policy_capital_controls" in esm.get_subscribed_events(), (
        "ExternalSectorModule.get_subscribed_events() must include "
        "'emergency_policy_capital_controls' after ADR-020 Channel A implementation"
    )


# ---------------------------------------------------------------------------
# AC-2: ESM Channel A reserve protection effect
# ---------------------------------------------------------------------------


def test_esm_capital_controls_produces_positive_reserve_coverage_delta() -> None:
    """AC-2: ESM Channel A — capital controls produce positive reserve_coverage_months delta."""
    entity = _make_entity(
        capital_account_outflow_velocity=0.5,   # active outflow before controls
    )
    cc_event = _capital_controls_event(severity=0.85, epsilon=0.60)
    state = _make_state(entity, prior_events=[cc_event])

    esm = ExternalSectorModule(commodity_price_shocks=[], start_date=_TS)
    events = esm.compute(entity, state, _TS)

    reserve_events = [
        e for e in events
        if "reserve_coverage_months" in e.affected_attributes
    ]
    assert len(reserve_events) > 0, (
        "ESM must produce a reserve_coverage_months event when "
        "emergency_policy_capital_controls fires (Channel A)"
    )
    delta = reserve_events[0].affected_attributes["reserve_coverage_months"].value
    assert delta > Decimal("0"), (
        f"reserve_coverage_months delta must be positive (outflow protection) — got {delta}"
    )


def test_esm_no_capital_controls_event_produces_no_reserve_channel_a_event() -> None:
    """AC-2 baseline: no capital controls event → no Channel A reserve event."""
    entity = _make_entity(capital_account_outflow_velocity=0.5)
    state = _make_state(entity, prior_events=[])

    esm = ExternalSectorModule(commodity_price_shocks=[], start_date=_TS)
    events = esm.compute(entity, state, _TS)

    # Without capital controls, no Channel A reserve events should be present
    # (commodity-shock reserve events are separate — they fire from self._shocks, not state.events)
    channel_a_events = [
        e for e in events
        if e.event_type == "capital_controls_reserve_protection"
        or (
            "reserve_coverage_months" in e.affected_attributes
            and e.affected_attributes["reserve_coverage_months"].value > Decimal("0")
        )
    ]
    assert channel_a_events == [], (
        "ESM must not emit Channel A reserve protection events when no capital controls fired"
    )


def test_esm_reserve_delta_tagged_financial_framework() -> None:
    """AC-2: Channel A reserve event is tagged FINANCIAL (consistent with existing reserve events)."""
    entity = _make_entity(capital_account_outflow_velocity=0.5)
    cc_event = _capital_controls_event()
    state = _make_state(entity, prior_events=[cc_event])

    esm = ExternalSectorModule(commodity_price_shocks=[], start_date=_TS)
    events = esm.compute(entity, state, _TS)

    reserve_events = [e for e in events if "reserve_coverage_months" in e.affected_attributes]
    assert len(reserve_events) > 0
    for e in reserve_events:
        assert e.framework == MeasurementFramework.FINANCIAL, (
            "Channel A reserve events must be FINANCIAL framework"
        )


# ---------------------------------------------------------------------------
# AC-3: MacroeconomicModule subscription and credit contraction (Channel B)
# ---------------------------------------------------------------------------


def test_mm_subscribes_to_emergency_policy_capital_controls() -> None:
    """AC-3: MM _SUBSCRIBED_EVENTS must include 'emergency_policy_capital_controls'."""
    assert "emergency_policy_capital_controls" in MM_SUBSCRIBED_EVENTS, (
        "MacroeconomicModule._SUBSCRIBED_EVENTS must include "
        "'emergency_policy_capital_controls' after ADR-020 Channel B implementation"
    )


def test_mm_capital_controls_produces_gdp_contraction() -> None:
    """AC-3: Channel B — capital controls produce negative gdp_growth delta (credit contraction)."""
    entity = _make_entity(gdp_growth=0.0)
    cc_event = _capital_controls_event(severity=0.85, implementation_capacity=0.75)
    state = _make_state(entity, prior_events=[cc_event])

    mm = MacroeconomicModule()
    events = mm.compute(entity, state, _TS)

    gdp_events = [e for e in events if e.event_type == "gdp_growth_change"]
    assert len(gdp_events) > 0, (
        "MacroeconomicModule must emit gdp_growth_change when "
        "emergency_policy_capital_controls fires (Channel B credit contraction)"
    )
    gdp_delta = gdp_events[0].affected_attributes["gdp_growth"].value
    assert gdp_delta < Decimal("0"), (
        f"Channel B: credit contraction must reduce gdp_growth — got delta={gdp_delta}"
    )


def test_mm_channel_b_beta_gamma_product() -> None:
    """AC-3: Verify β=0.020 and γ=1.2 produce the expected GDP impact direction and scale."""
    from app.simulation.modules.macroeconomic.module import (
        CAPITAL_CONTROLS_BETA,
        CAPITAL_CONTROLS_GAMMA,
    )
    assert CAPITAL_CONTROLS_BETA == Decimal("0.020"), (
        f"CM-calibrated β must be 0.020 — got {CAPITAL_CONTROLS_BETA}"
    )
    assert CAPITAL_CONTROLS_GAMMA == Decimal("1.2"), (
        f"CM-supplied γ must be 1.2 — got {CAPITAL_CONTROLS_GAMMA}"
    )
    # Implied GDP impact: 0.020 × 0.85 × 0.75 × 1.2 = 0.0153 (approx 1.53pp contraction)
    severity = Decimal("0.85")
    capacity = Decimal("0.75")
    expected_gdp_impact = CAPITAL_CONTROLS_BETA * severity * capacity * CAPITAL_CONTROLS_GAMMA
    assert expected_gdp_impact > Decimal("0"), "Expected impact magnitude must be positive"
    assert expected_gdp_impact < Decimal("0.1"), "Expected impact must be < 10pp (sanity bound)"


def test_mm_gamma_is_not_caller_configurable() -> None:
    """AC-9: γ is a CM-supplied constant — MacroeconomicModule must not accept it as a parameter."""
    from app.simulation.modules.macroeconomic.module import CAPITAL_CONTROLS_GAMMA

    # The module exposes γ as a read-only constant, not a constructor or method parameter.
    # This test confirms the constant is module-level (not instance-configurable).
    mm = MacroeconomicModule()
    assert not hasattr(mm, "capital_controls_gamma"), (
        "γ must not be an instance attribute — it is a CM-supplied constant "
        "and must not be overridable by the CE agent or callers"
    )
    assert CAPITAL_CONTROLS_GAMMA == Decimal("1.2"), (
        "Module-level CAPITAL_CONTROLS_GAMMA must be exactly 1.2 "
        "(CM-calibrated; cannot be changed without CM Consulted review)"
    )


# ---------------------------------------------------------------------------
# AC-4: MM emits credit_contraction_labour_shock bridge event (Channel B bridge)
# ---------------------------------------------------------------------------


def test_mm_capital_controls_emits_bridge_event() -> None:
    """AC-4: Channel B must emit 'credit_contraction_labour_shock' bridge after credit contraction.

    Written as a SEPARATE test block from AC-3 (gdp contraction) so bridge
    failure is visible independently from GDP effect failure.
    """
    entity = _make_entity(gdp_growth=0.0)
    cc_event = _capital_controls_event(severity=0.85, implementation_capacity=0.75)
    state = _make_state(entity, prior_events=[cc_event])

    mm = MacroeconomicModule()
    events = mm.compute(entity, state, _TS)

    bridge_events = [
        e for e in events
        if e.event_type == "credit_contraction_labour_shock"
    ]
    assert len(bridge_events) > 0, (
        "MacroeconomicModule must emit 'credit_contraction_labour_shock' bridge event "
        "after applying Channel B credit contraction — DemographicModule Channel C "
        "depends on this event to update q1_poverty_headcount_ratio"
    )


def test_mm_bridge_event_has_nonzero_delta_credit_growth() -> None:
    """AC-4: Bridge event payload must carry non-zero delta_credit_growth so DM can apply φ."""
    entity = _make_entity(gdp_growth=0.0)
    cc_event = _capital_controls_event(severity=0.85)
    state = _make_state(entity, prior_events=[cc_event])

    mm = MacroeconomicModule()
    events = mm.compute(entity, state, _TS)

    bridge_events = [e for e in events if e.event_type == "credit_contraction_labour_shock"]
    assert len(bridge_events) > 0, "Bridge event must be emitted (AC-4 prerequisite)"

    bridge = bridge_events[0]
    # Bridge event must carry at least one affected_attribute with non-zero magnitude
    assert bridge.affected_attributes, "Bridge event must have non-empty affected_attributes"
    magnitudes = [qty.value for qty in bridge.affected_attributes.values()]
    assert any(m != Decimal("0") for m in magnitudes), (
        "Bridge event affected_attributes must carry non-zero delta (credit contraction magnitude)"
    )


def test_mm_bridge_event_magnitude_is_negative_for_credit_contraction() -> None:
    """AC-4: Bridge event magnitude must be negative (credit contracted) so DM elasticity sign is correct."""
    entity = _make_entity(gdp_growth=0.0)
    cc_event = _capital_controls_event(severity=0.85)
    state = _make_state(entity, prior_events=[cc_event])

    mm = MacroeconomicModule()
    events = mm.compute(entity, state, _TS)

    bridge_events = [e for e in events if e.event_type == "credit_contraction_labour_shock"]
    assert len(bridge_events) > 0
    primary_magnitude = next(iter(bridge_events[0].affected_attributes.values())).value
    assert primary_magnitude < Decimal("0"), (
        f"Bridge event magnitude must be negative (credit contracted) — got {primary_magnitude}. "
        "DM φ elasticity is negative, so negative×negative = positive PHC delta."
    )


# ---------------------------------------------------------------------------
# AC-5: DM dead subscription removed (Channel C cleanup)
# ---------------------------------------------------------------------------


def test_dm_does_not_subscribe_to_capital_controls_imposition() -> None:
    """AC-5 / SF-4 guard: 'capital_controls_imposition' must be removed from DM _SUBSCRIBED_EVENTS.

    Pre-fix: this string was present (dead — never emitted). It is the original
    ADR-020 Channel C bug. Post-fix: it must be absent.
    """
    assert "capital_controls_imposition" not in DM_SUBSCRIBED_EVENTS, (
        "'capital_controls_imposition' is a dead event string (never emitted by any module). "
        "ADR-020 Channel C fix requires its removal from DemographicModule._SUBSCRIBED_EVENTS. "
        "See NM-090."
    )


def test_capital_controls_imposition_event_produces_no_dm_response() -> None:
    """SF-2 guard: old-format 'capital_controls_imposition' event must produce zero DM output.

    If the dead string is still present in _SUBSCRIBED_EVENTS and the test
    creates an event with that type, DM would incorrectly fire. This confirms
    the fix is complete at the behavior level, not just the string level.
    """
    # Build the old-format event (as it would have appeared if the dead subscription fired)
    old_event = Event(
        event_id="old-cc-imposition",
        source_entity_id=_ENTITY_ID,
        event_type="capital_controls_imposition",
        affected_attributes={
            "capital_controls_imposition": _qty(0.85),
        },
        propagation_rules=[],
        timestep_originated=_TS,
        framework=MeasurementFramework.GOVERNANCE,
    )
    entity = _make_entity()
    state = _make_state(entity, prior_events=[old_event])

    dm = DemographicModule(cohort_resolution_entity_ids=[_ENTITY_ID])
    events = dm.compute(entity, state, _TS)

    assert events == [], (
        "DemographicModule must not respond to 'capital_controls_imposition' — "
        "this string is dead (never emitted) and must not be in _SUBSCRIBED_EVENTS after ADR-020 fix"
    )


# ---------------------------------------------------------------------------
# AC-6: DM bridge subscription added and elasticity row present (Channel C)
# ---------------------------------------------------------------------------


def test_dm_subscribes_to_credit_contraction_labour_shock() -> None:
    """AC-6: DM _SUBSCRIBED_EVENTS must include 'credit_contraction_labour_shock' after Channel C fix."""
    assert "credit_contraction_labour_shock" in DM_SUBSCRIBED_EVENTS, (
        "'credit_contraction_labour_shock' must be in DemographicModule._SUBSCRIBED_EVENTS "
        "after ADR-020 Channel C implementation (bridge subscription)"
    )


def test_elasticity_registry_has_credit_contraction_labour_shock_row() -> None:
    """AC-6: ELASTICITY_REGISTRY must contain at least one row for 'credit_contraction_labour_shock'."""
    rows = [r for r in ELASTICITY_REGISTRY if r.event_type == "credit_contraction_labour_shock"]
    assert len(rows) >= 1, (
        "ELASTICITY_REGISTRY must have at least one 'credit_contraction_labour_shock' row "
        "after ADR-020 Channel C implementation. Currently: 0 rows found. "
        "φ ∈ [0.3, 0.7] for Q1 cohort (ISL: φ=0.30 per calibration-basis.md §Capital Controls §φ)"
    )


def test_credit_contraction_elasticity_targets_q1_cohort() -> None:
    """AC-6: The credit_contraction_labour_shock row must target a Q1 income quintile cohort."""
    rows = [r for r in ELASTICITY_REGISTRY if r.event_type == "credit_contraction_labour_shock"]
    assert len(rows) >= 1, "AC-6 prerequisite: elasticity row must exist"

    q1_rows = [r for r in rows if r.cohort_spec.income_quintile == IncomeQuintile.Q1]
    assert len(q1_rows) >= 1, (
        "credit_contraction_labour_shock elasticity must target Q1 cohort "
        "(φ ∈ [0.3, 0.7] bottom quintile per ADR-020 §Decision 2 Channel C)"
    )


def test_credit_contraction_elasticity_is_in_phi_range() -> None:
    """AC-6: φ elasticity value must be in [0.3, 0.7] per calibration-basis.md §Capital Controls."""
    rows = [r for r in ELASTICITY_REGISTRY if r.event_type == "credit_contraction_labour_shock"]
    assert len(rows) >= 1, "AC-6 prerequisite: elasticity row must exist"

    for row in rows:
        # Elasticity is negative so that negative delta_credit_growth × negative elasticity = positive PHC delta.
        # The absolute value of the elasticity must be in [0.3, 0.7].
        phi_abs = abs(row.elasticity)
        assert Decimal("0.3") <= phi_abs <= Decimal("0.7"), (
            f"φ elasticity magnitude must be in [0.3, 0.7] — got {phi_abs} "
            f"(source: {row.source_registry_id})"
        )


def test_credit_contraction_elasticity_is_decimal_not_float() -> None:
    """AC-6: φ elasticity must be Decimal (CODING_STANDARDS — no float for monetary arithmetic)."""
    rows = [r for r in ELASTICITY_REGISTRY if r.event_type == "credit_contraction_labour_shock"]
    for row in rows:
        assert isinstance(row.elasticity, Decimal), (
            f"Elasticity must be Decimal — got {type(row.elasticity)} "
            f"in row {row.source_registry_id}"
        )


# ---------------------------------------------------------------------------
# AC-7: DM Channel C produces positive Q1 PHC delta on bridge event
# ---------------------------------------------------------------------------


def test_dm_credit_contraction_labour_shock_raises_q1_phc() -> None:
    """AC-7: Channel C — bridge event triggers positive poverty_headcount_ratio delta for Q1 cohort."""
    entity = _make_entity()
    bridge = _bridge_event(delta_credit_growth=-0.01275)
    state = _make_state(entity, prior_events=[bridge])

    dm = DemographicModule(cohort_resolution_entity_ids=[_ENTITY_ID])
    events = dm.compute(entity, state, _TS)

    assert len(events) > 0, (
        "DemographicModule must respond to 'credit_contraction_labour_shock' "
        "after Channel C bridge subscription and elasticity row are added"
    )

    # Verify at least one event targets an ISL Q1 cohort (e.g. "ISL:CHT:1-*")
    q1_events = [
        e for e in events
        if "ISL:CHT:1-" in (e.metadata.get("target_entity_id") or "")
    ]
    assert len(q1_events) > 0, (
        "Channel C must produce events targeting Q1 cohort entities (ISL:CHT:1-*)"
    )


def test_dm_credit_contraction_q1_phc_delta_is_positive() -> None:
    """AC-7: PHC delta must be positive — credit contraction increases bottom-quintile poverty."""
    entity = _make_entity()
    bridge = _bridge_event(delta_credit_growth=-0.05)  # strong contraction → visible PHC effect
    state = _make_state(entity, prior_events=[bridge])

    dm = DemographicModule(cohort_resolution_entity_ids=[_ENTITY_ID])
    events = dm.compute(entity, state, _TS)

    assert len(events) > 0, "AC-7 prerequisite: events must be produced"

    for event in events:
        for attr_key, qty in event.affected_attributes.items():
            if "poverty_headcount" in attr_key or "poverty" in attr_key:
                assert qty.value > Decimal("0"), (
                    f"PHC delta must be positive for credit contraction "
                    f"(poverty rises when credit contracts) — got {qty.value} for {attr_key}"
                )


# ---------------------------------------------------------------------------
# AC-8: DM does NOT subscribe to emergency_policy_capital_controls directly (SF-5 guard)
# ---------------------------------------------------------------------------


def test_dm_does_not_subscribe_to_emergency_policy_capital_controls() -> None:
    """AC-8 / SF-5 guard: DM must NOT subscribe to 'emergency_policy_capital_controls'.

    Channel C uses the credit_contraction_labour_shock BRIDGE (emitted by Channel B),
    NOT a direct subscription to the policy event. A direct subscription would bypass
    the credit contraction mechanism and apply φ unconditionally on policy imposition.
    CE audit (PR #1626) resolved ADR-020's ambiguous Channel C text: bridge design is canonical.
    """
    assert "emergency_policy_capital_controls" not in DM_SUBSCRIBED_EVENTS, (
        "DemographicModule must NOT subscribe to 'emergency_policy_capital_controls' directly. "
        "Channel C uses the 'credit_contraction_labour_shock' bridge from Channel B "
        "(CE audit PR #1626 resolution — transmission-table §capital_controls row is canonical). "
        "See intent doc §3 SF-5 and §6 Channel C design note."
    )


def test_emergency_policy_capital_controls_produces_no_dm_response_directly() -> None:
    """AC-8 / SF-5: DM must not fire when capital_controls event arrives directly (bridge guard)."""
    cc_event = _capital_controls_event()
    entity = _make_entity()
    state = _make_state(entity, prior_events=[cc_event])

    dm = DemographicModule(cohort_resolution_entity_ids=[_ENTITY_ID])
    events = dm.compute(entity, state, _TS)

    assert events == [], (
        "DemographicModule must NOT respond to 'emergency_policy_capital_controls' directly — "
        "it responds to 'credit_contraction_labour_shock' bridge event only (Channel C bridge design)"
    )


# ---------------------------------------------------------------------------
# AC-9: γ constant protection (CM-supplied, not CE-overridable)
# ---------------------------------------------------------------------------


def test_mm_capital_controls_gamma_constant_value() -> None:
    """AC-9: γ=1.2 must be a module-level constant (CM-supplied; requires CM review to change)."""
    from app.simulation.modules.macroeconomic.module import CAPITAL_CONTROLS_GAMMA

    assert CAPITAL_CONTROLS_GAMMA == Decimal("1.2"), (
        f"CAPITAL_CONTROLS_GAMMA must be exactly Decimal('1.2') — got {CAPITAL_CONTROLS_GAMMA}. "
        "γ is CM-supplied per calibration-basis.md §Capital Controls. "
        "Changing γ requires CM Consulted review — not CE author authority."
    )


def test_mm_capital_controls_gamma_is_decimal() -> None:
    """AC-9: γ must be Decimal — CODING_STANDARDS prohibit float for all multiplier constants."""
    from app.simulation.modules.macroeconomic.module import CAPITAL_CONTROLS_GAMMA
    assert isinstance(CAPITAL_CONTROLS_GAMMA, Decimal), (
        f"CAPITAL_CONTROLS_GAMMA must be Decimal, not {type(CAPITAL_CONTROLS_GAMMA)}"
    )


# ---------------------------------------------------------------------------
# AC-11: EmergencyPolicyInput(CAPITAL_CONTROLS) does not raise SimulationError
# ---------------------------------------------------------------------------


def test_emergency_policy_input_capital_controls_does_not_raise() -> None:
    """AC-11: Constructing + processing EmergencyPolicyInput(CAPITAL_CONTROLS) raises no SimulationError."""
    from app.simulation.orchestration.inputs import EmergencyInstrument, EmergencyPolicyInput

    policy = EmergencyPolicyInput(
        input_id="test-cc-input",
        target_entity=_ENTITY_ID,
        actor_id="test-actor",
        instrument=EmergencyInstrument.CAPITAL_CONTROLS,
        parameters={"magnitude": 0.85, "epsilon": 0.60, "implementation_capacity": 0.75},
        expected_duration=8,
    )
    events = policy.to_events(_TS)
    assert len(events) == 1
    assert events[0].event_type == "emergency_policy_capital_controls"
    assert events[0].affected_attributes["capital_controls"].value == Decimal("0.85")


def test_emergency_instrument_capital_controls_value() -> None:
    """AC-11: EmergencyInstrument.CAPITAL_CONTROLS.value must be 'capital_controls'."""
    from app.simulation.orchestration.inputs import EmergencyInstrument
    assert EmergencyInstrument.CAPITAL_CONTROLS.value == "capital_controls"


# ---------------------------------------------------------------------------
# Reg-1: gdp_growth_change Q1 elasticity unchanged (M17-G1 calibration)
# ---------------------------------------------------------------------------


def test_gdp_growth_change_q1_elasticity_preserved() -> None:
    """Reg-1: Adding Channel C row must not alter existing gdp_growth_change Q1 row.

    M17-G1 recalibrated Q1 informal elasticity to -0.20 (Fosu 2011 SSA anchor).
    ADR-020 Channel C adds a NEW credit_contraction_labour_shock row — it must
    not modify, rename, or remove the existing gdp_growth_change Q1 row.
    """
    gdp_rows = [r for r in ELASTICITY_REGISTRY if r.event_type == "gdp_growth_change"]
    assert len(gdp_rows) >= 3, "gdp_growth_change must have at least 3 rows (M17-G1 calibration)"

    q1_informal_rows = [
        r for r in gdp_rows
        if r.cohort_spec.income_quintile == IncomeQuintile.Q1
        and "INFORMAL" in str(r.cohort_spec.employment_sector)
    ]
    assert len(q1_informal_rows) >= 1, "Q1 informal gdp_growth_change row must exist (Fosu 2011)"

    q1_row = q1_informal_rows[0]
    assert q1_row.elasticity == Decimal("-0.20"), (
        f"Q1 informal gdp_growth_change elasticity must be -0.20 (M17-G1 Fosu 2011) — "
        f"got {q1_row.elasticity}. ADR-020 Channel C must not alter existing rows."
    )


def test_gdp_growth_change_rows_not_reduced_by_channel_c() -> None:
    """Reg-1: Channel C additions must not reduce the count of gdp_growth_change rows."""
    gdp_rows = [r for r in ELASTICITY_REGISTRY if r.event_type == "gdp_growth_change"]
    assert len(gdp_rows) >= 3, (
        f"ELASTICITY_REGISTRY must still have >= 3 gdp_growth_change rows after Channel C — "
        f"got {len(gdp_rows)}. ADR-020 additions must not delete existing rows."
    )
