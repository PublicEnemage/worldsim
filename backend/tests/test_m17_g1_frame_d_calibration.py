"""QA tests for M17-G1: FRAME-D elasticity calibration (#1229).

QA Lead — Chief Methodologist (CM holds R for both implementation and FRAME-D test
authorship per sprint entry §2.4). Authored from calibration decision document at:
  docs/calibration/m17-g1-elasticity-calibration-decision.md

These tests define "done" for the G1 ELASTICITY_REGISTRY code change. AC-2 and AC-1
tests WILL FAIL until the implementation PR updates the three constants in
`backend/app/simulation/modules/demographic/elasticities.py`. That is intentional:
these tests are authored before the implementation PR opens (sprint entry §2.4 gate).

NM-056 rule: NO test uses pytest.skip() conditionally. No soft-skips.

AC coverage:
  AC-1  FRAME-D integration test — two components:
        (a) Per-step delta: Q1 informal poverty delta ∈ [+0.002, +0.004] per step
            under gdp_growth_change magnitude -0.015 (certified range per calibration
            decision doc §4.2).
        (b) FRAME-D crossing: Q1 informal poverty_headcount_ratio ≥ 0.40 after
            7 responding steps from initial 0.38 (MDA-HD-POVERTY-Q1 recovery floor
            crossed within 8-step programme window).

  AC-2  ELASTICITY_REGISTRY entries revised to SSA calibration (Path A):
        - Q1 informal elasticity == Decimal("-0.20") (Fosu 2011 SSA mid-range)
        - Q2 informal elasticity == Decimal("-0.133") (Ball 2013 2/3 scaling preserved)
        - Q1 agricultural elasticity == Decimal("-0.16") (IMF 2014 80% scaling revised)
        - Q1 informal source_registry_id updated to
          ACADEMIC_LITERATURE_FOSU_2011_SSA_POVERTY_GROWTH

Certified range derivation (calibration decision doc §4.2):
  Lower bound (+0.002): Fosu (2011) lower range (elasticity -0.15):
    -0.015 × -0.15 = +0.00225; bound excludes pre-calibration response (+0.0015).
  Upper bound (+0.004): Fosu (2011) upper range (elasticity -0.25):
    -0.015 × -0.25 = +0.00375 → capped at +0.004.
  Point estimate (+0.003): -0.015 × -0.20 = +0.003 (7 steps → +0.021 cumulative
    → 0.38 + 0.021 = 0.401 ≥ 0.40; FRAME-D fires within 8-step window).

Regression risk: see calibration decision doc §4.3. test_m16_g3_25year_human_capital_trajectory.py
uses bounds assertion [0.0, 1.0] — unaffected by elasticity revision.
"""
from __future__ import annotations

from datetime import UTC, datetime
from decimal import Decimal

from app.simulation.modules.demographic.cohort import (
    AgeBand,
    CohortSpec,
    EmploymentSector,
    IncomeQuintile,
)
from app.simulation.modules.demographic.elasticities import ELASTICITY_REGISTRY
from app.simulation.modules.demographic.module import DemographicModule

# ---------------------------------------------------------------------------
# Constants from calibration decision doc §4.2
# ---------------------------------------------------------------------------

_INITIAL_Q1_POVERTY = Decimal("0.38")        # ECOWAS regional T3 synthetic (SEN fixture)
_MDA_HD_POVERTY_Q1_FLOOR = Decimal("0.40")   # MDA recovery floor — FRAME-D trigger threshold
# MacroeconomicModule output: -3% fiscal × 0.5 multiplier
_GDP_SHOCK_MAGNITUDE = Decimal("-0.015")
_FRAME_D_DELTA_LOWER = Decimal("0.002")    # Fosu 2011 lower range (elasticity -0.15)
_FRAME_D_DELTA_UPPER = Decimal("0.004")    # Fosu 2011 upper range (elasticity -0.25)
# Pre-revision response — must be excluded by lower bound
_PRE_CALIBRATION_DELTA = Decimal("0.0015")
_FRAME_D_RESPONDING_STEPS = 7                 # Steps 2–8: DemographicModule responds 7 times
_ENTITY_ID = "SEN"
_Q1_INFORMAL_COHORT_ID = "SEN:CHT:1-25-54-INFORMAL"

# Target SSA constants (Path A, calibration decision doc §3.2)
_Q1_INFORMAL_ELASTICITY_SSA = Decimal("-0.20")
_Q2_INFORMAL_ELASTICITY_SSA = Decimal("-0.133")
_Q1_AGRICULTURAL_ELASTICITY_SSA = Decimal("-0.16")
_Q1_INFORMAL_SOURCE_REGISTRY_ID = "ACADEMIC_LITERATURE_FOSU_2011_SSA_POVERTY_GROWTH"


# ---------------------------------------------------------------------------
# Helpers (mirror test_demographic_module.py style)
# ---------------------------------------------------------------------------


def _make_state(
    entity_id: str,
    prior_events: list | None = None,
) -> object:
    from app.simulation.engine.models import (
        ResolutionConfig,
        ScenarioConfig,
        SimulationEntity,
        SimulationState,
    )

    ts = datetime(2024, 1, 1, tzinfo=UTC)
    entity = SimulationEntity(
        id=entity_id,
        entity_type="country",
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
            scenario_id="m17-g1-frame-d-test",
            name="M17-G1 FRAME-D calibration test",
            description="",
            start_date=ts,
            end_date=ts,
        ),
    )


def _gdp_growth_event(
    entity_id: str,
    magnitude: Decimal,
    step: int = 1,
) -> object:
    """Build a gdp_growth_change Event as emitted by MacroeconomicModule."""
    from app.simulation.engine.models import Event, MeasurementFramework
    from app.simulation.engine.quantity import Quantity, VariableType

    ts = datetime(2024, step, 1, tzinfo=UTC)
    qty = Quantity(
        value=magnitude,
        unit="ratio",
        variable_type=VariableType.RATIO,
        measurement_framework=MeasurementFramework.FINANCIAL,
        confidence_tier=3,
    )
    return Event(
        event_id=f"test-gdp-event-step{step}",
        source_entity_id=entity_id,
        event_type="gdp_growth_change",
        affected_attributes={"gdp_growth_change": qty},
        propagation_rules=[],
        timestep_originated=ts,
        framework=MeasurementFramework.FINANCIAL,
    )


def _q1_informal_delta_from_events(events: list) -> Decimal | None:
    """Extract the poverty_headcount_ratio delta for the Q1 informal cohort."""
    for event in events:
        if event.metadata.get("target_entity_id") == _Q1_INFORMAL_COHORT_ID:
            qty = event.affected_attributes.get("poverty_headcount_ratio")
            if qty is not None:
                return qty.value
    return None


def _find_registry_entry(
    event_type: str,
    quintile: IncomeQuintile,
    age_band: AgeBand,
    sector: EmploymentSector,
) -> object | None:
    target_spec = CohortSpec(quintile, age_band, sector)
    for row in ELASTICITY_REGISTRY:
        if row.event_type == event_type and row.cohort_spec == target_spec:
            return row
    return None


# ---------------------------------------------------------------------------
# AC-2 — ELASTICITY_REGISTRY revised to SSA calibration (Path A)
# Calibration decision doc §3.2
# ---------------------------------------------------------------------------


class TestAC2ElasticityRegistrySSACalibration:
    """AC-2: ELASTICITY_REGISTRY must reflect the Path A SSA revision.

    These tests will FAIL until the implementation PR updates elasticities.py.
    Each assertion corresponds to a row in calibration decision doc Table §3.2.
    """

    def test_q1_informal_elasticity_revised_to_ssa_value(self) -> None:
        """Q1 informal gdp_growth_change elasticity must be -0.20 (Fosu 2011 SSA mid-range).

        Prior value: -0.10 (Lustig 2017 Latin American calibration — regional mismatch).
        Revision factor: ×2, per Fosu (2011) finding that SSA elasticities are 1.5–2×
        larger than Latin American comparators at equivalent inequality levels.
        """
        row = _find_registry_entry(
            "gdp_growth_change",
            IncomeQuintile.Q1,
            AgeBand.AGE_25_54,
            EmploymentSector.INFORMAL,
        )
        assert row is not None, (
            "No gdp_growth_change entry for Q1/25-54/INFORMAL found in ELASTICITY_REGISTRY. "
            "AC-2: implementation PR must retain this cohort entry."
        )
        assert row.elasticity == _Q1_INFORMAL_ELASTICITY_SSA, (
            f"Q1 informal elasticity is {row.elasticity!r}, "
            f"expected {_Q1_INFORMAL_ELASTICITY_SSA!r}. "
            "AC-2: Path A SSA revision (Fosu 2011) sets Q1 informal to -0.20. "
            "If still -0.10, the implementation PR has not been applied."
        )

    def test_q1_informal_source_registry_id_updated_to_fosu_2011(self) -> None:
        """Q1 informal source_registry_id must cite Fosu (2011), not Lustig (2017).

        Fosu (2011) replaces Lustig (2017) as the calibration basis for the Q1 informal
        entry in the SSA context (calibration decision doc §5).
        """
        row = _find_registry_entry(
            "gdp_growth_change",
            IncomeQuintile.Q1,
            AgeBand.AGE_25_54,
            EmploymentSector.INFORMAL,
        )
        assert row is not None, (
            "No gdp_growth_change entry for Q1/25-54/INFORMAL found."
        )
        assert row.source_registry_id == _Q1_INFORMAL_SOURCE_REGISTRY_ID, (
            f"Q1 informal source_registry_id is {row.source_registry_id!r}, "
            f"expected {_Q1_INFORMAL_SOURCE_REGISTRY_ID!r}. "
            "AC-2: implementation PR must update source attribution from Lustig (2017) "
            "to Fosu (2011) for the SSA calibration."
        )

    def test_q2_informal_elasticity_revised_to_ssa_value(self) -> None:
        """Q2 informal gdp_growth_change elasticity must be -0.133 (2/3 × Q1 SSA value).

        The 2/3 scaling ratio from Ball et al. (2013) is preserved; only the absolute
        Q1 base changes (calibration decision doc §3.2).
        """
        row = _find_registry_entry(
            "gdp_growth_change",
            IncomeQuintile.Q2,
            AgeBand.AGE_25_54,
            EmploymentSector.INFORMAL,
        )
        assert row is not None, (
            "No gdp_growth_change entry for Q2/25-54/INFORMAL found in ELASTICITY_REGISTRY. "
            "AC-2: implementation PR must retain this cohort entry."
        )
        assert row.elasticity == _Q2_INFORMAL_ELASTICITY_SSA, (
            f"Q2 informal elasticity is {row.elasticity!r}, "
            f"expected {_Q2_INFORMAL_ELASTICITY_SSA!r}. "
            "AC-2: Path A revision scales Q2 to 2/3 × -0.20 = -0.133 "
            "(Ball 2013 ratio preserved). "
            "If still -0.067, the implementation PR has not been applied."
        )

    def test_q1_agricultural_elasticity_revised_to_ssa_value(self) -> None:
        """Q1 agricultural gdp_growth_change elasticity must be -0.16 (IMF 2014 80% scaling).

        The 80% scaling of Q1 informal is preserved; only the absolute Q1 base changes
        (calibration decision doc §3.2).
        """
        row = _find_registry_entry(
            "gdp_growth_change",
            IncomeQuintile.Q1,
            AgeBand.AGE_25_54,
            EmploymentSector.AGRICULTURE,
        )
        assert row is not None, (
            "No gdp_growth_change entry for Q1/25-54/AGRICULTURE found in ELASTICITY_REGISTRY. "
            "AC-2: implementation PR must retain this cohort entry."
        )
        assert row.elasticity == _Q1_AGRICULTURAL_ELASTICITY_SSA, (
            f"Q1 agricultural elasticity is {row.elasticity!r}, "
            f"expected {_Q1_AGRICULTURAL_ELASTICITY_SSA!r}. "
            "AC-2: Path A revision sets Q1 agricultural to 80% × -0.20 = -0.16 (IMF 2014). "
            "If still -0.08, the implementation PR has not been applied."
        )

    def test_all_three_revised_entries_remain_tier_3(self) -> None:
        """All three revised entries must remain Confidence Tier 3.

        T3 = regionally inferred (SSA), not Senegal-specific backtested.
        T2 upgrade requires Senegal backtesting against quarterly poverty data — M18 scope.
        Calibration decision doc §3.2: 'All three entries remain Confidence Tier 3.'
        """
        specs = [
            (IncomeQuintile.Q1, EmploymentSector.INFORMAL, "Q1 informal"),
            (IncomeQuintile.Q2, EmploymentSector.INFORMAL, "Q2 informal"),
            (IncomeQuintile.Q1, EmploymentSector.AGRICULTURE, "Q1 agricultural"),
        ]
        for quintile, sector, label in specs:
            row = _find_registry_entry(
                "gdp_growth_change",
                quintile,
                AgeBand.AGE_25_54,
                sector,
            )
            assert row is not None, f"No entry found for {label}."
            assert row.confidence_tier == 3, (
                f"{label} confidence_tier is {row.confidence_tier}, expected 3. "
                "T3 is the correct tier for regionally-inferred SSA calibration. "
                "A tier upgrade to T2 requires Senegal-specific backtesting (M18 scope)."
            )


# ---------------------------------------------------------------------------
# AC-1 (unit component) — per-step delta in certified range
# Calibration decision doc §4.1 (unit component) and §4.2
# ---------------------------------------------------------------------------


class TestAC1FrameDPerStepDeltaUnit:
    """AC-1 (unit component): Q1 informal poverty delta must be in [+0.002, +0.004] per step.

    Test structure: direct gdp_growth_change injection (magnitude -0.015) into DemographicModule,
    bypassing MacroeconomicModule regime dynamics to isolate the elasticity under test.
    This matches the test design in calibration decision doc §4.1: "injection is direct to
    isolate the DemographicModule elasticity from MacroeconomicModule regime dynamics."

    These tests FAIL until the ELASTICITY_REGISTRY constants are revised.
    """

    def test_q1_informal_per_step_delta_within_certified_range(self) -> None:
        """Q1 informal poverty delta per step must be in [+0.002, +0.004].

        Certified range per calibration decision doc §4.2:
          Lower (+0.002): Fosu (2011) lower (elasticity -0.15): -0.015 × -0.15 = +0.00225
          Upper (+0.004): Fosu (2011) upper (elasticity -0.25): -0.015 × -0.25 = +0.00375
          Point estimate (elasticity -0.20): -0.015 × -0.20 = +0.003
        """
        gdp_event = _gdp_growth_event(_ENTITY_ID, _GDP_SHOCK_MAGNITUDE, step=1)
        state = _make_state(_ENTITY_ID, prior_events=[gdp_event])
        module = DemographicModule(cohort_resolution_entity_ids=[_ENTITY_ID])
        ts = datetime(2024, 2, 1, tzinfo=UTC)

        events = module.compute(state.entities[_ENTITY_ID], state, ts)

        delta = _q1_informal_delta_from_events(events)
        assert delta is not None, (
            f"No poverty_headcount_ratio delta found for {_Q1_INFORMAL_COHORT_ID}. "
            "AC-1: DemographicModule must emit a demographic_cohort_delta event for Q1 informal "
            "when gdp_growth_change fires. Check that ELASTICITY_REGISTRY still has a "
            "Q1/25-54/INFORMAL gdp_growth_change entry."
        )
        assert isinstance(delta, Decimal), (
            f"Delta type is {type(delta).__name__}, expected Decimal. "
            "All elasticity computations must use Decimal arithmetic (CODING_STANDARDS.md)."
        )
        assert delta >= _FRAME_D_DELTA_LOWER, (
            f"Q1 informal delta {delta!r} < lower bound {_FRAME_D_DELTA_LOWER!r}. "
            "Calibration decision doc §4.2: lower bound is +0.002 (Fosu 2011 lower range). "
            "A delta below +0.002 indicates the elasticity was not updated from the prior "
            "Latin American calibration (pre-calibration response was +0.0015 per step)."
        )
        assert delta <= _FRAME_D_DELTA_UPPER, (
            f"Q1 informal delta {delta!r} > upper bound {_FRAME_D_DELTA_UPPER!r}. "
            "Calibration decision doc §4.2: upper bound is +0.004 (Fosu 2011 upper range). "
            "A delta above +0.004 suggests an elasticity overshoot beyond the T3 upper range."
        )

    def test_q1_informal_delta_exceeds_pre_calibration_response(self) -> None:
        """Q1 informal per-step delta must exceed the pre-calibration response of +0.0015.

        The lower bound (+0.002) already enforces this, but this test makes the
        regression guard explicit: if the ELASTICITY_REGISTRY was not updated, the
        pre-implementation response (+0.0015 per step at elasticity -0.10) would
        fail the lower bound assertion above. This guard documents that intent.

        Calibration decision doc §4.2: 'Lower bound rationale: This bound excludes the
        pre-calibration response (+0.0015) — any test result below +0.002 indicates the
        elasticity was not updated from the prior value.'
        """
        gdp_event = _gdp_growth_event(_ENTITY_ID, _GDP_SHOCK_MAGNITUDE, step=1)
        state = _make_state(_ENTITY_ID, prior_events=[gdp_event])
        module = DemographicModule(cohort_resolution_entity_ids=[_ENTITY_ID])
        ts = datetime(2024, 2, 1, tzinfo=UTC)

        events = module.compute(state.entities[_ENTITY_ID], state, ts)
        delta = _q1_informal_delta_from_events(events)

        assert delta is not None, (
            f"No delta for {_Q1_INFORMAL_COHORT_ID} — see AC-1 unit component test above."
        )
        assert delta > _PRE_CALIBRATION_DELTA, (
            f"Q1 informal delta {delta!r} ≤ pre-calibration response {_PRE_CALIBRATION_DELTA!r}. "
            "The ELASTICITY_REGISTRY has not been updated from the prior Latin American value "
            "(-0.10). Implementation PR has not been applied."
        )

    def test_q1_informal_delta_is_positive_for_gdp_contraction(self) -> None:
        """GDP contraction must increase Q1 informal poverty (positive delta).

        Invariant: negative magnitude × negative elasticity = positive poverty delta.
        This holds regardless of the magnitude of the revision.
        """
        gdp_event = _gdp_growth_event(_ENTITY_ID, _GDP_SHOCK_MAGNITUDE, step=1)
        state = _make_state(_ENTITY_ID, prior_events=[gdp_event])
        module = DemographicModule(cohort_resolution_entity_ids=[_ENTITY_ID])
        ts = datetime(2024, 2, 1, tzinfo=UTC)

        events = module.compute(state.entities[_ENTITY_ID], state, ts)
        delta = _q1_informal_delta_from_events(events)

        assert delta is not None
        assert delta > Decimal("0"), (
            f"Q1 informal delta {delta!r} is not positive. "
            "GDP contraction (negative magnitude) × negative elasticity must produce "
            "a positive poverty delta (poverty rises when GDP contracts)."
        )

    def test_q2_informal_delta_within_expected_range_at_ssa_calibration(self) -> None:
        """Q2 informal per-step delta must reflect the revised Q2 elasticity (-0.133).

        Expected: -0.015 × -0.133 = +0.001995 ≈ +0.002 (within [+0.001, +0.003]).
        The Q2 range is 2/3 of the Q1 range per Ball (2013) scaling.
        """
        _Q2_INFORMAL_COHORT_ID = "SEN:CHT:2-25-54-INFORMAL"
        q2_delta_lower = Decimal("0.001")
        q2_delta_upper = Decimal("0.003")

        gdp_event = _gdp_growth_event(_ENTITY_ID, _GDP_SHOCK_MAGNITUDE, step=1)
        state = _make_state(_ENTITY_ID, prior_events=[gdp_event])
        module = DemographicModule(cohort_resolution_entity_ids=[_ENTITY_ID])
        ts = datetime(2024, 2, 1, tzinfo=UTC)

        events = module.compute(state.entities[_ENTITY_ID], state, ts)

        q2_delta = None
        for event in events:
            if event.metadata.get("target_entity_id") == _Q2_INFORMAL_COHORT_ID:
                qty = event.affected_attributes.get("poverty_headcount_ratio")
                if qty is not None:
                    q2_delta = qty.value
                    break

        assert q2_delta is not None, (
            f"No poverty_headcount_ratio delta for {_Q2_INFORMAL_COHORT_ID}. "
            "Q2 informal elasticity entry must remain in ELASTICITY_REGISTRY after revision."
        )
        assert q2_delta >= q2_delta_lower, (
            f"Q2 informal delta {q2_delta!r} < {q2_delta_lower!r}. "
            "Expected -0.015 × -0.133 ≈ +0.002. ELASTICITY_REGISTRY Q2 entry not updated."
        )
        assert q2_delta <= q2_delta_upper, (
            f"Q2 informal delta {q2_delta!r} > {q2_delta_upper!r}. "
            "Unexpected overshoot in Q2 informal elasticity revision."
        )


# ---------------------------------------------------------------------------
# AC-1 (integration component) — FRAME-D threshold crossing within 8-step window
# Calibration decision doc §4.1 (integration component) and §4.2
# ---------------------------------------------------------------------------


class TestAC1FrameDCrossing:
    """AC-1 (integration component): Q1 informal poverty must cross 0.40 within 8-step window.

    Test simulates 7 consecutive responding steps (steps 2–8 in the programme window):
    each step processes a gdp_growth_change event of magnitude -0.015 via
    DemographicModule.compute(). Poverty accumulates from initial 0.38.

    Point estimate trajectory (calibration decision doc §4.2):
      +0.003/step × 7 steps = +0.021 cumulative
      0.38 + 0.021 = 0.401 ≥ 0.40 (MDA-HD-POVERTY-Q1 recovery floor crossed)

    Direct gdp_growth_change injection bypasses MacroeconomicModule regime cascades
    (depressed/ZLB multipliers) to produce a controlled per-step delta for this test.
    The full fiscal chain produces larger poverty deltas in the demo scenario; this
    test certifies the elasticity alone.

    These tests FAIL until the ELASTICITY_REGISTRY constants are revised.
    """

    def test_q1_informal_poverty_crosses_mda_floor_within_8_step_window(self) -> None:
        """Q1 informal poverty must reach ≥ 0.40 after 7 responding steps from 0.38.

        MDA-HD-POVERTY-Q1 recovery floor is 0.40 (crossed from below — floor is a
        ceiling in welfare terms). FRAME-D milestone sentence fires when this threshold
        is crossed within the Demo 6 Senegal 8-step programme window.
        """
        module = DemographicModule(cohort_resolution_entity_ids=[_ENTITY_ID])
        cumulative_poverty = _INITIAL_Q1_POVERTY

        for step in range(1, _FRAME_D_RESPONDING_STEPS + 1):
            gdp_event = _gdp_growth_event(_ENTITY_ID, _GDP_SHOCK_MAGNITUDE, step=step)
            state = _make_state(_ENTITY_ID, prior_events=[gdp_event])
            ts = datetime(2024, step + 1, 1, tzinfo=UTC)

            events = module.compute(state.entities[_ENTITY_ID], state, ts)
            step_delta = _q1_informal_delta_from_events(events)

            assert step_delta is not None, (
                f"No Q1 informal poverty delta at responding step {step}. "
                f"DemographicModule must emit a delta for {_Q1_INFORMAL_COHORT_ID} "
                "on each gdp_growth_change event."
            )
            cumulative_poverty += step_delta

        assert cumulative_poverty >= _MDA_HD_POVERTY_Q1_FLOOR, (
            f"Q1 informal poverty after {_FRAME_D_RESPONDING_STEPS} responding steps: "
            f"{cumulative_poverty!r}. Expected ≥ {_MDA_HD_POVERTY_Q1_FLOOR!r} "
            f"(MDA-HD-POVERTY-Q1 recovery floor). "
            f"Initial poverty: {_INITIAL_Q1_POVERTY!r}. "
            f"FRAME-D milestone sentence cannot fire in the 8-step Demo 6 window. "
            f"Calibration decision doc §4.2: point estimate trajectory reaches 0.401 "
            f"at 7 responding steps with Q1 informal elasticity -0.20."
        )

    def test_q1_informal_poverty_trajectory_is_monotonically_increasing(self) -> None:
        """Under persistent GDP contraction, Q1 informal poverty must rise at each step.

        Each responding step processes an identical gdp_growth_change event (magnitude -0.015),
        so the per-step delta must be positive and constant. A zero or negative delta at any
        step indicates an elasticity sign error or a missing registry entry.
        """
        module = DemographicModule(cohort_resolution_entity_ids=[_ENTITY_ID])
        prior_poverty = _INITIAL_Q1_POVERTY

        for step in range(1, _FRAME_D_RESPONDING_STEPS + 1):
            gdp_event = _gdp_growth_event(_ENTITY_ID, _GDP_SHOCK_MAGNITUDE, step=step)
            state = _make_state(_ENTITY_ID, prior_events=[gdp_event])
            ts = datetime(2024, step + 1, 1, tzinfo=UTC)

            events = module.compute(state.entities[_ENTITY_ID], state, ts)
            step_delta = _q1_informal_delta_from_events(events)

            assert step_delta is not None, (
                f"No Q1 informal delta at responding step {step}."
            )
            assert step_delta > Decimal("0"), (
                f"Responding step {step}: delta {step_delta!r} is not positive. "
                "Persistent GDP contraction must produce strictly positive poverty deltas "
                "at every responding step."
            )
            prior_poverty += step_delta

    def test_cumulative_delta_consistent_with_per_step_delta_range(self) -> None:
        """Cumulative Q1 informal poverty increase over 7 steps must be in [+0.014, +0.028].

        This range is derived from the certified per-step bounds:
          Lower: 7 steps × +0.002 = +0.014
          Upper: 7 steps × +0.004 = +0.028

        A cumulative delta outside this range indicates the per-step delta drifted
        beyond the Fosu (2011) T3 uncertainty bounds.
        """
        cumulative_lower = Decimal("0.014")  # 7 × 0.002
        cumulative_upper = Decimal("0.028")  # 7 × 0.004

        module = DemographicModule(cohort_resolution_entity_ids=[_ENTITY_ID])
        cumulative_delta = Decimal("0")

        for step in range(1, _FRAME_D_RESPONDING_STEPS + 1):
            gdp_event = _gdp_growth_event(_ENTITY_ID, _GDP_SHOCK_MAGNITUDE, step=step)
            state = _make_state(_ENTITY_ID, prior_events=[gdp_event])
            ts = datetime(2024, step + 1, 1, tzinfo=UTC)

            events = module.compute(state.entities[_ENTITY_ID], state, ts)
            step_delta = _q1_informal_delta_from_events(events)

            assert step_delta is not None, f"No Q1 informal delta at step {step}."
            cumulative_delta += step_delta

        assert cumulative_delta >= cumulative_lower, (
            f"Cumulative Q1 informal poverty increase over 7 steps: {cumulative_delta!r}. "
            f"Expected ≥ {cumulative_lower!r} (7 × lower bound {_FRAME_D_DELTA_LOWER!r}). "
            "Calibration has not been revised to SSA values."
        )
        assert cumulative_delta <= cumulative_upper, (
            f"Cumulative Q1 informal poverty increase over 7 steps: {cumulative_delta!r}. "
            f"Expected ≤ {cumulative_upper!r} (7 × upper bound {_FRAME_D_DELTA_UPPER!r}). "
            "Unexpected overshoot beyond Fosu (2011) T3 upper bound."
        )
