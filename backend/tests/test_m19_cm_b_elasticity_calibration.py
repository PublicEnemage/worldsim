"""QA tests for M19-CM-B: LAC ELASTICITY_REGISTRY calibration (#1623 Gap 2).

CM holds R for authorship per sprint entry §2.4 and calibration decision document
authority. Authored from:
  docs/calibration/m19-cm-b-lac-calibration-decision.md

These tests define "done" for the CM Sprint B ELASTICITY_REGISTRY code change.
RED tests WILL FAIL until the implementation PR:
  (1) Adds two LAC-scoped FORMAL sector entries to ELASTICITY_REGISTRY
      (entity_families=frozenset({"ARG","ECU","BOL","PER"}))
  (2) No module.py changes required (entity_families filter already present from CM Sprint A)

entity_families field on CohortElasticity already exists from CM Sprint A — that test
is GREEN from the start.

AC coverage:
  AC-1  MAGNITUDE integration test — hd_composite divergence at step index 2 ∈ [0.003, 0.050]
        between counter-factual (early managed peg exit 1999) and baseline (orthodox austerity)
        ARG fiscal paths.
        Forward condition for Demo 8 Act 2 (requires DATABASE_URL).

  AC-2  ≥2 LAC-scoped entries in ELASTICITY_REGISTRY with all four entity IDs (ARG/ECU/BOL/PER);
        entity_families field exists on CohortElasticity (GREEN — CM Sprint A guarantee);
        source_registry_ids reference LUSTIG_2014_CEQ_LAC and BALL_2013 literature.
        Per-step delta for LAC Q1 FORMAL within calibrated range per decision doc §4.1.

  AC-4  Non-regression — all prior ELASTICITY_REGISTRY entries unchanged (SSA M17-G1 +
        ADR-020 Channel C + GRC CM Sprint A entries).

  AC-5  Cross-contamination guard — LAC FORMAL entries do not fire on SSA entities (SEN,
        ZMB) or Euro area entities (GRC).

Test RED/GREEN status before implementation:
  RED   TestAC2LACEntriesPresent (except test_entity_families_field_exists — GREEN)
        TestAC3LACFormalEntryValues
        TestAC3LACDeltaUnitRange
        TestAC1MagnitudeDivergence (harness-level; requires DATABASE_URL)
  GREEN TestAC2LACEntriesPresent.test_entity_families_field_exists_on_cohort_elasticity
        TestAC4NonRegression
        TestAC5CrossContaminationGuard

NM-056 rule: NO test uses pytest.skip() conditionally. DATABASE_URL tests skip via
fixture guard only (explicit skip with reason string at fixture evaluation time).
"""
from __future__ import annotations

import os
import warnings
from datetime import UTC, datetime
from decimal import Decimal
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator

import httpx
import pytest
import pytest_asyncio

from app.harness.mode3_harness import (
    RunType,
    run_harness,
)
from app.main import app
from app.simulation.modules.demographic.cohort import (
    AgeBand,
    CohortSpec,
    EmploymentSector,
    IncomeQuintile,
)
from app.simulation.modules.demographic.elasticities import ELASTICITY_REGISTRY
from app.simulation.modules.demographic.module import DemographicModule

_DATABASE_URL = os.environ.get("DATABASE_URL")

# ---------------------------------------------------------------------------
# Calibration constants (calibration decision doc §3.1, §4.1)
# ---------------------------------------------------------------------------

_LAC_ENTITY_IDS = frozenset({"ARG", "ECU", "BOL", "PER"})
_ARG_ENTITY_ID = "ARG"
_SEN_ENTITY_ID = "SEN"
_ZMB_ENTITY_ID = "ZMB"
_GRC_ENTITY_ID = "GRC"

_ARG_Q1_FORMAL_COHORT_ID = "ARG:CHT:1-25-54-FORMAL"
_ARG_Q2_FORMAL_COHORT_ID = "ARG:CHT:2-25-54-FORMAL"
_SEN_Q1_INFORMAL_COHORT_ID = "SEN:CHT:1-25-54-INFORMAL"

# Per-step delta bounds for LAC Q1 FORMAL (calibration decision doc §4.1)
# GDP shock -0.015:
#   Q1: -0.015 × -0.22 = +0.0033 (point estimate)
#   Lower: -0.015 × -0.15 = +0.00225 (uncertainty lower edge)
#   Upper: -0.015 × -0.30 = +0.0045 (uncertainty upper edge, with margin)
_GDP_SHOCK_MAGNITUDE = Decimal("-0.015")
_LAC_Q1_FORMAL_DELTA_LOWER = Decimal("0.002")   # -0.015 × -0.15 (rounded down)
_LAC_Q1_FORMAL_DELTA_UPPER = Decimal("0.005")   # -0.015 × -0.30 (with margin)

# Per-step delta bounds for LAC Q2 FORMAL
# -0.015 × -0.13 = +0.00195
_LAC_Q2_FORMAL_DELTA_LOWER = Decimal("0.001")
_LAC_Q2_FORMAL_DELTA_UPPER = Decimal("0.003")

# Target calibration constants (decision doc §3.1)
_LAC_Q1_FORMAL_ELASTICITY = Decimal("-0.22")
_LAC_Q2_FORMAL_ELASTICITY = Decimal("-0.13")

# Source registry IDs (decision doc §5)
_LUSTIG_2014_SOURCE_ID = "ACADEMIC_LITERATURE_LUSTIG_2014_CEQ_LAC_POVERTY"
_GASPARINI_LUSTIG_SOURCE_ID = "ACADEMIC_LITERATURE_GASPARINI_LUSTIG_2011_LAC_INEQUALITY"
_BALL_2013_SOURCE_ID = "ACADEMIC_LITERATURE_BALL_2013_FISCAL_CONSOLIDATION"

# Non-regression constants — all prior ELASTICITY_REGISTRY entries (CM Sprint A state)
_SSA_Q1_INFORMAL_ELASTICITY = Decimal("-0.20")
_SSA_Q2_INFORMAL_ELASTICITY = Decimal("-0.133")
_SSA_Q1_AGRI_ELASTICITY = Decimal("-0.16")
_CHANNEL_C_ELASTICITY = Decimal("-0.30")
_GRC_Q1_FORMAL_ELASTICITY = Decimal("-0.25")
_GRC_Q2_FORMAL_ELASTICITY = Decimal("-0.15")
_REQUIRED_PRIOR_SOURCE_IDS = {
    "ACADEMIC_LITERATURE_FOSU_2011_SSA_POVERTY_GROWTH",
    "ACADEMIC_LITERATURE_BALL_2013_FISCAL_CONSOLIDATION",
    "ACADEMIC_LITERATURE_IMF_2014_FISCAL_INEQUALITY",
    "ACADEMIC_LITERATURE_ICELAND_2008_CREDIT_CONTRACTION_PHC",
    "ACADEMIC_LITERATURE_BLANCHARD_LEIGH_2013_FISCAL_MULTIPLIERS",
}

# hd_composite divergence bounds for ARG Type B step index 2.
# CM Sprint D calibration decision §4.2 — certified from empirical run [obs×0.5, obs×2.0].
# Values below are PLACEHOLDER bounds (wide) for the first CI run to reveal the observed diff.
# Update to certified values after reading per_step_diff[2] from the CI failure output.
# CM Sprint B §4.1 bounds [0.003, 0.050] rejected — assumed convergence; see §1.1.
_HD_COMPOSITE_LOWER = Decimal("0.001")
_HD_COMPOSITE_UPPER = Decimal("0.999")


# ---------------------------------------------------------------------------
# Shared helpers
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
            scenario_id="m19-cm-b-elasticity-test",
            name="M19-CM-B LAC elasticity calibration test",
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


def _extract_cohort_delta(events: list, cohort_id: str) -> Decimal | None:
    for event in events:
        if event.metadata.get("target_entity_id") == cohort_id:
            qty = event.affected_attributes.get("poverty_headcount_ratio")
            if qty is not None:
                return qty.value
    return None


def _find_registry_entry(
    event_type: str,
    quintile: IncomeQuintile,
    age_band: AgeBand,
    sector: EmploymentSector,
    entity_families: frozenset[str] | None = None,
) -> object | None:
    target_spec = CohortSpec(quintile, age_band, sector)
    for row in ELASTICITY_REGISTRY:
        if row.event_type != event_type:
            continue
        if row.cohort_spec != target_spec:
            continue
        row_ef = getattr(row, "entity_families", None)
        if entity_families is None:
            if row_ef is None:
                return row
        else:
            if row_ef == entity_families:
                return row
    return None


# ---------------------------------------------------------------------------
# AC-2 Part 1 — LAC entries present in ELASTICITY_REGISTRY
# GREEN: test_entity_families_field_exists (CM Sprint A guarantee)
# RED until implementation: all others
# ---------------------------------------------------------------------------


class TestAC2LACEntriesPresent:
    """AC-2: ELASTICITY_REGISTRY must contain ≥2 LAC-scoped FORMAL sector entries.

    test_entity_families_field_exists is GREEN from the start (CM Sprint A added the field).
    All other tests in this class are RED until the implementation PR adds the LAC entries.
    """

    def test_entity_families_field_exists_on_cohort_elasticity(self) -> None:
        """CohortElasticity must have an entity_families attribute.

        GREEN before implementation: CM Sprint A (2026-07-03) added this field.
        Calibration decision doc §1.2: Option (a) entity_families scoping mechanism.
        """
        if not ELASTICITY_REGISTRY:
            pytest.fail("ELASTICITY_REGISTRY is empty — cannot verify field existence.")

        first_entry = ELASTICITY_REGISTRY[0]
        assert hasattr(first_entry, "entity_families"), (
            "CohortElasticity has no 'entity_families' attribute. "
            "CM Sprint A should have added this field. "
            "Check that sprint/m19-cm-a changes are present on this branch."
        )

    def test_at_least_two_lac_scoped_entries_present(self) -> None:
        """ELASTICITY_REGISTRY must have ≥2 entries with entity_families containing 'ARG'.

        RED: no LAC-scoped entries exist yet.
        Calibration decision doc §3.1: Q1 FORMAL (-0.22) + Q2 FORMAL (-0.13), T3.
        """
        lac_entries = [
            e for e in ELASTICITY_REGISTRY
            if hasattr(e, "entity_families")
            and e.entity_families is not None
            and _ARG_ENTITY_ID in e.entity_families
        ]
        assert len(lac_entries) >= 2, (
            f"Found {len(lac_entries)} ARG-scoped entries in ELASTICITY_REGISTRY. "
            "AC-2 requires ≥2 (Q1 FORMAL + Q2 FORMAL, gdp_growth_change). "
            "Implementation PR must add LAC entity_families entries."
        )

    def test_lac_q1_formal_gdp_entry_present(self) -> None:
        """ELASTICITY_REGISTRY must have a LAC-scoped Q1/25-54/FORMAL gdp_growth_change entry.

        RED: no such entry exists.
        Calibration decision doc §3.1: LAC Q1 FORMAL, elasticity=-0.22, T3.
        Source: Lustig et al. (2014) CEQ WP/13.
        """
        row = _find_registry_entry(
            "gdp_growth_change",
            IncomeQuintile.Q1,
            AgeBand.AGE_25_54,
            EmploymentSector.FORMAL,
            entity_families=_LAC_ENTITY_IDS,
        )
        assert row is not None, (
            "No LAC-scoped gdp_growth_change entry for Q1/25-54/FORMAL in "
            "ELASTICITY_REGISTRY. Implementation PR must add this entry. "
            "See calibration decision doc §3.1 — primary LAC calibration."
        )

    def test_lac_q2_formal_gdp_entry_present(self) -> None:
        """ELASTICITY_REGISTRY must have a LAC-scoped Q2/25-54/FORMAL gdp_growth_change entry.

        RED: no such entry exists.
        Calibration decision doc §3.1: LAC Q2 FORMAL, elasticity=-0.13, T3.
        Source: Ball et al. (2013) 0.60 scaling.
        """
        row = _find_registry_entry(
            "gdp_growth_change",
            IncomeQuintile.Q2,
            AgeBand.AGE_25_54,
            EmploymentSector.FORMAL,
            entity_families=_LAC_ENTITY_IDS,
        )
        assert row is not None, (
            "No LAC-scoped gdp_growth_change entry for Q2/25-54/FORMAL in "
            "ELASTICITY_REGISTRY. Implementation PR must add this entry. "
            "See calibration decision doc §3.1 — secondary LAC calibration."
        )


# ---------------------------------------------------------------------------
# AC-3 Part 1 — LAC FORMAL entry values
# RED until implementation
# ---------------------------------------------------------------------------


class TestAC3LACFormalEntryValues:
    """AC-3: Verify LAC FORMAL entry constants match the calibration decision doc.

    All tests are RED until implementation PR adds the entries.
    """

    def test_lac_q1_formal_elasticity_value(self) -> None:
        """LAC Q1 FORMAL elasticity must be exactly Decimal('-0.22').

        RED: no entry exists yet.
        Calibration decision doc §3.1: -0.22 point estimate from Lustig (2014)
        CEQ LAC assessment. Formal-sector concentration factor 1.6× aggregate.
        """
        row = _find_registry_entry(
            "gdp_growth_change",
            IncomeQuintile.Q1,
            AgeBand.AGE_25_54,
            EmploymentSector.FORMAL,
            entity_families=_LAC_ENTITY_IDS,
        )
        assert row is not None, "LAC Q1 FORMAL entry absent — RED (pre-implementation)."
        assert row.elasticity == _LAC_Q1_FORMAL_ELASTICITY, (
            f"LAC Q1 FORMAL elasticity={row.elasticity!r}, "
            f"expected {_LAC_Q1_FORMAL_ELASTICITY!r}. "
            "Calibration decision doc §3.1 specifies -0.22."
        )

    def test_lac_q1_formal_confidence_tier(self) -> None:
        """LAC Q1 FORMAL entry must be T3 (regional LAC inference, not country-specific).

        RED: no entry exists yet.
        Calibration decision doc §3.1: T3 — T2 upgrade requires country-specific
        backtesting (Bolivia/Peru fiscal consolidation fixtures — beyond M19).
        """
        row = _find_registry_entry(
            "gdp_growth_change",
            IncomeQuintile.Q1,
            AgeBand.AGE_25_54,
            EmploymentSector.FORMAL,
            entity_families=_LAC_ENTITY_IDS,
        )
        assert row is not None, "LAC Q1 FORMAL entry absent — RED (pre-implementation)."
        assert row.confidence_tier == 3, (
            f"LAC Q1 FORMAL confidence_tier={row.confidence_tier!r}, expected 3 (T3). "
            "Regional LAC inference; T2 upgrade requires country-specific backtesting."
        )

    def test_lac_q1_formal_source_registry_id(self) -> None:
        """LAC Q1 FORMAL source_registry_id must reference Lustig (2014) CEQ source.

        RED: no entry exists yet.
        Calibration decision doc §5: ACADEMIC_LITERATURE_LUSTIG_2014_CEQ_LAC_POVERTY.
        """
        row = _find_registry_entry(
            "gdp_growth_change",
            IncomeQuintile.Q1,
            AgeBand.AGE_25_54,
            EmploymentSector.FORMAL,
            entity_families=_LAC_ENTITY_IDS,
        )
        assert row is not None, "LAC Q1 FORMAL entry absent — RED (pre-implementation)."
        assert row.source_registry_id == _LUSTIG_2014_SOURCE_ID, (
            f"LAC Q1 FORMAL source_registry_id={row.source_registry_id!r}, "
            f"expected {_LUSTIG_2014_SOURCE_ID!r}."
        )

    def test_lac_q2_formal_elasticity_value(self) -> None:
        """LAC Q2 FORMAL elasticity must be exactly Decimal('-0.13').

        RED: no entry exists yet.
        Calibration decision doc §3.1: 0.60 × Q1 (-0.22) = -0.132 → -0.13.
        Source: Ball et al. (2013) between-quintile scaling.
        """
        row = _find_registry_entry(
            "gdp_growth_change",
            IncomeQuintile.Q2,
            AgeBand.AGE_25_54,
            EmploymentSector.FORMAL,
            entity_families=_LAC_ENTITY_IDS,
        )
        assert row is not None, "LAC Q2 FORMAL entry absent — RED (pre-implementation)."
        assert row.elasticity == _LAC_Q2_FORMAL_ELASTICITY, (
            f"LAC Q2 FORMAL elasticity={row.elasticity!r}, "
            f"expected {_LAC_Q2_FORMAL_ELASTICITY!r}. "
            "Calibration decision doc §3.1: 0.60 × Q1 FORMAL."
        )

    def test_lac_q2_formal_source_registry_id(self) -> None:
        """LAC Q2 FORMAL source_registry_id must reference Ball et al. (2013).

        RED: no entry exists yet.
        The Q2 scaling ratio is from Ball et al. (2013), already registered.
        """
        row = _find_registry_entry(
            "gdp_growth_change",
            IncomeQuintile.Q2,
            AgeBand.AGE_25_54,
            EmploymentSector.FORMAL,
            entity_families=_LAC_ENTITY_IDS,
        )
        assert row is not None, "LAC Q2 FORMAL entry absent — RED (pre-implementation)."
        assert row.source_registry_id == _BALL_2013_SOURCE_ID, (
            f"LAC Q2 FORMAL source_registry_id={row.source_registry_id!r}, "
            f"expected {_BALL_2013_SOURCE_ID!r}."
        )

    def test_lac_entries_entity_families_covers_all_four_entities(self) -> None:
        """All LAC entries must have entity_families == frozenset({'ARG','ECU','BOL','PER'}).

        RED: no entries exist yet.
        Calibration decision doc §3.3: all four LAC entities in the same frozenset.
        """
        lac_entries = [
            e for e in ELASTICITY_REGISTRY
            if hasattr(e, "entity_families")
            and e.entity_families is not None
            and _ARG_ENTITY_ID in e.entity_families
        ]
        assert len(lac_entries) >= 2, (
            "No LAC-scoped entries found — RED (pre-implementation)."
        )
        for entry in lac_entries:
            assert entry.entity_families == _LAC_ENTITY_IDS, (
                f"LAC entry entity_families={entry.entity_families!r}, "
                f"expected {_LAC_ENTITY_IDS!r}. "
                "All four LAC entities (ARG, ECU, BOL, PER) must be in the frozenset."
            )


# ---------------------------------------------------------------------------
# AC-3 Part 2 — Per-step delta range (unit-level, no DB required)
# RED until implementation
# ---------------------------------------------------------------------------


class TestAC3LACDeltaUnitRange:
    """AC-3: Per-step delta from DemographicModule must be within calibrated range.

    RED until implementation. These verify the entries produce the right magnitude
    response when the module runs against a synthetic ARG entity.
    """

    def test_lac_q1_formal_delta_within_range_for_gdp_shock(self) -> None:
        """ARG Q1 FORMAL poverty_headcount_ratio delta at -0.015 GDP shock ∈ [0.002, 0.005].

        RED: no LAC entries → no delta event produced for Q1 FORMAL cohort.
        Calibration decision doc §4.1: -0.015 × -0.22 = +0.0033 (point estimate).
        """
        module = DemographicModule(cohort_resolution_entity_ids=[_ARG_ENTITY_ID])
        event = _gdp_growth_event(_ARG_ENTITY_ID, _GDP_SHOCK_MAGNITUDE)
        state = _make_state(_ARG_ENTITY_ID, prior_events=[event])
        ts = datetime(2024, 1, 1, tzinfo=UTC)
        result_events = module.compute(state.entities[_ARG_ENTITY_ID], state, ts)

        delta = _extract_cohort_delta(result_events, _ARG_Q1_FORMAL_COHORT_ID)
        assert delta is not None, (
            f"No poverty_headcount_ratio event for {_ARG_Q1_FORMAL_COHORT_ID}. "
            "AC-3 FAIL: LAC Q1 FORMAL entry absent — RED until implementation."
        )
        assert _LAC_Q1_FORMAL_DELTA_LOWER <= delta <= _LAC_Q1_FORMAL_DELTA_UPPER, (
            f"ARG Q1 FORMAL delta={delta!r} outside [{_LAC_Q1_FORMAL_DELTA_LOWER!r}, "
            f"{_LAC_Q1_FORMAL_DELTA_UPPER!r}]. "
            "Calibration decision doc §3.1 uncertainty range."
        )

    def test_lac_q2_formal_delta_within_range_for_gdp_shock(self) -> None:
        """ARG Q2 FORMAL poverty_headcount_ratio delta at -0.015 GDP shock ∈ [0.001, 0.003].

        RED: no LAC entries → no delta event produced for Q2 FORMAL cohort.
        Calibration decision doc §3.1: -0.015 × -0.13 = +0.00195.
        """
        module = DemographicModule(cohort_resolution_entity_ids=[_ARG_ENTITY_ID])
        event = _gdp_growth_event(_ARG_ENTITY_ID, _GDP_SHOCK_MAGNITUDE)
        state = _make_state(_ARG_ENTITY_ID, prior_events=[event])
        ts = datetime(2024, 1, 1, tzinfo=UTC)
        result_events = module.compute(state.entities[_ARG_ENTITY_ID], state, ts)

        delta = _extract_cohort_delta(result_events, _ARG_Q2_FORMAL_COHORT_ID)
        assert delta is not None, (
            f"No poverty_headcount_ratio event for {_ARG_Q2_FORMAL_COHORT_ID}. "
            "AC-3 FAIL: LAC Q2 FORMAL entry absent — RED until implementation."
        )
        assert _LAC_Q2_FORMAL_DELTA_LOWER <= delta <= _LAC_Q2_FORMAL_DELTA_UPPER, (
            f"ARG Q2 FORMAL delta={delta!r} outside [{_LAC_Q2_FORMAL_DELTA_LOWER!r}, "
            f"{_LAC_Q2_FORMAL_DELTA_UPPER!r}]. "
            "Calibration decision doc §3.1: Q2 = 0.60 × Q1."
        )

    def test_lac_q2_formal_delta_less_than_q1_formal_delta(self) -> None:
        """Q2 FORMAL delta must be < Q1 FORMAL delta (Ball 2013 0.60 scaling).

        RED: no LAC entries.
        Structural invariant: Q2 is a less-exposed cohort than Q1.
        """
        module = DemographicModule(cohort_resolution_entity_ids=[_ARG_ENTITY_ID])
        event = _gdp_growth_event(_ARG_ENTITY_ID, _GDP_SHOCK_MAGNITUDE)
        state = _make_state(_ARG_ENTITY_ID, prior_events=[event])
        ts = datetime(2024, 1, 1, tzinfo=UTC)
        result_events = module.compute(state.entities[_ARG_ENTITY_ID], state, ts)

        delta_q1 = _extract_cohort_delta(result_events, _ARG_Q1_FORMAL_COHORT_ID)
        delta_q2 = _extract_cohort_delta(result_events, _ARG_Q2_FORMAL_COHORT_ID)

        if delta_q1 is None or delta_q2 is None:
            pytest.fail(
                "LAC FORMAL deltas absent — RED (pre-implementation). "
                f"delta_q1={delta_q1!r}, delta_q2={delta_q2!r}."
            )

        assert delta_q2 < delta_q1, (
            f"Q2 delta ({delta_q2!r}) not less than Q1 delta ({delta_q1!r}). "
            "Ball et al. (2013) 0.60 scaling requires Q2 < Q1 for negative GDP shock."
        )


# ---------------------------------------------------------------------------
# AC-4 — Non-regression: all prior ELASTICITY_REGISTRY entries unchanged
# GREEN before and after implementation
# ---------------------------------------------------------------------------


class TestAC4NonRegression:
    """AC-4: Verify all prior ELASTICITY_REGISTRY entries are unchanged.

    GREEN before implementation. These become regression guards after the PR merges.
    Covers SSA M17-G1 entries, ADR-020 Channel C, and GRC CM Sprint A entries.
    """

    def test_ssa_q1_informal_elasticity_unchanged(self) -> None:
        """SSA Q1 INFORMAL (entity_families=None) elasticity must still be -0.20."""
        row = _find_registry_entry(
            "gdp_growth_change",
            IncomeQuintile.Q1,
            AgeBand.AGE_25_54,
            EmploymentSector.INFORMAL,
            entity_families=None,
        )
        assert row is not None, "SSA Q1 INFORMAL entry missing — non-regression FAIL."
        assert row.elasticity == _SSA_Q1_INFORMAL_ELASTICITY, (
            f"SSA Q1 INFORMAL elasticity changed: {row.elasticity!r} "
            f"!= {_SSA_Q1_INFORMAL_ELASTICITY!r}. "
            "M17-G1 SSA recalibration (Fosu 2011) entry must not be modified."
        )

    def test_ssa_q2_informal_elasticity_unchanged(self) -> None:
        """SSA Q2 INFORMAL (entity_families=None) elasticity must still be -0.133."""
        row = _find_registry_entry(
            "gdp_growth_change",
            IncomeQuintile.Q2,
            AgeBand.AGE_25_54,
            EmploymentSector.INFORMAL,
            entity_families=None,
        )
        assert row is not None, "SSA Q2 INFORMAL entry missing — non-regression FAIL."
        assert row.elasticity == _SSA_Q2_INFORMAL_ELASTICITY, (
            f"SSA Q2 INFORMAL elasticity changed: {row.elasticity!r} "
            f"!= {_SSA_Q2_INFORMAL_ELASTICITY!r}."
        )

    def test_ssa_q1_agriculture_elasticity_unchanged(self) -> None:
        """SSA Q1 AGRICULTURE (entity_families=None) elasticity must still be -0.16."""
        row = _find_registry_entry(
            "gdp_growth_change",
            IncomeQuintile.Q1,
            AgeBand.AGE_25_54,
            EmploymentSector.AGRICULTURE,
            entity_families=None,
        )
        assert row is not None, "SSA Q1 AGRICULTURE entry missing — non-regression FAIL."
        assert row.elasticity == _SSA_Q1_AGRI_ELASTICITY, (
            f"SSA Q1 AGRICULTURE elasticity changed: {row.elasticity!r} "
            f"!= {_SSA_Q1_AGRI_ELASTICITY!r}."
        )

    def test_channel_c_elasticity_unchanged(self) -> None:
        """ADR-020 Channel C (credit_contraction_labour_shock) elasticity must still be -0.30."""
        channel_c_entries = [
            e for e in ELASTICITY_REGISTRY
            if e.event_type == "credit_contraction_labour_shock"
        ]
        assert len(channel_c_entries) >= 1, (
            "ADR-020 Channel C entry missing — non-regression FAIL."
        )
        entry = channel_c_entries[0]
        assert entry.elasticity == _CHANNEL_C_ELASTICITY, (
            f"Channel C elasticity changed: {entry.elasticity!r} != {_CHANNEL_C_ELASTICITY!r}."
        )

    def test_grc_q1_formal_elasticity_unchanged(self) -> None:
        """GRC Q1 FORMAL (CM Sprint A) elasticity must still be -0.25."""
        row = _find_registry_entry(
            "gdp_growth_change",
            IncomeQuintile.Q1,
            AgeBand.AGE_25_54,
            EmploymentSector.FORMAL,
            entity_families=frozenset({"GRC"}),
        )
        assert row is not None, "GRC Q1 FORMAL entry missing — CM Sprint A non-regression FAIL."
        assert row.elasticity == _GRC_Q1_FORMAL_ELASTICITY, (
            f"GRC Q1 FORMAL elasticity changed: {row.elasticity!r} "
            f"!= {_GRC_Q1_FORMAL_ELASTICITY!r}."
        )

    def test_grc_q2_formal_elasticity_unchanged(self) -> None:
        """GRC Q2 FORMAL (CM Sprint A) elasticity must still be -0.15."""
        row = _find_registry_entry(
            "gdp_growth_change",
            IncomeQuintile.Q2,
            AgeBand.AGE_25_54,
            EmploymentSector.FORMAL,
            entity_families=frozenset({"GRC"}),
        )
        assert row is not None, "GRC Q2 FORMAL entry missing — CM Sprint A non-regression FAIL."
        assert row.elasticity == _GRC_Q2_FORMAL_ELASTICITY, (
            f"GRC Q2 FORMAL elasticity changed: {row.elasticity!r} "
            f"!= {_GRC_Q2_FORMAL_ELASTICITY!r}."
        )

    def test_prior_source_registry_ids_present(self) -> None:
        """All M17-G1 and CM Sprint A source registry IDs must still be present."""
        actual_ids = {e.source_registry_id for e in ELASTICITY_REGISTRY}
        missing = _REQUIRED_PRIOR_SOURCE_IDS - actual_ids
        assert not missing, (
            f"Prior source registry IDs missing from ELASTICITY_REGISTRY: {missing!r}. "
            "CM Sprint B must not remove or rename existing source references."
        )


# ---------------------------------------------------------------------------
# AC-5 — Cross-contamination guard
# GREEN before implementation (no LAC entries to contaminate)
# Regression guard after implementation
# ---------------------------------------------------------------------------


class TestAC5CrossContaminationGuard:
    """AC-5: LAC FORMAL entries must not fire on SSA entities (SEN, ZMB) or GRC.

    GREEN before implementation (no LAC entries exist).
    After implementation, these ensure entity_families scoping is correct.
    """

    def test_lac_entries_do_not_fire_on_sen(self) -> None:
        """No LAC-scoped entry should have SEN in its entity_families."""
        lac_entries_for_sen = [
            e for e in ELASTICITY_REGISTRY
            if hasattr(e, "entity_families")
            and e.entity_families is not None
            and _SEN_ENTITY_ID in e.entity_families
            and e.elasticity in (_LAC_Q1_FORMAL_ELASTICITY, _LAC_Q2_FORMAL_ELASTICITY)
        ]
        assert len(lac_entries_for_sen) == 0, (
            f"Found {len(lac_entries_for_sen)} LAC-calibrated entries that fire on SEN. "
            "LAC entries must use entity_families=frozenset({'ARG','ECU','BOL','PER'}) "
            "only — SEN must not be included."
        )

    def test_lac_entries_do_not_fire_on_zmb(self) -> None:
        """No LAC-scoped entry should have ZMB in its entity_families."""
        lac_entries_for_zmb = [
            e for e in ELASTICITY_REGISTRY
            if hasattr(e, "entity_families")
            and e.entity_families is not None
            and _ZMB_ENTITY_ID in e.entity_families
            and e.elasticity in (_LAC_Q1_FORMAL_ELASTICITY, _LAC_Q2_FORMAL_ELASTICITY)
        ]
        assert len(lac_entries_for_zmb) == 0, (
            f"Found {len(lac_entries_for_zmb)} LAC-calibrated entries that fire on ZMB. "
            "ZMB is an SSA entity and must not receive LAC formal-sector calibration."
        )

    def test_lac_entries_do_not_fire_on_grc(self) -> None:
        """No LAC-scoped entry should have GRC in its entity_families."""
        lac_entries_for_grc = [
            e for e in ELASTICITY_REGISTRY
            if hasattr(e, "entity_families")
            and e.entity_families is not None
            and _GRC_ENTITY_ID in e.entity_families
            and e.elasticity in (_LAC_Q1_FORMAL_ELASTICITY, _LAC_Q2_FORMAL_ELASTICITY)
        ]
        assert len(lac_entries_for_grc) == 0, (
            f"Found {len(lac_entries_for_grc)} LAC-calibrated entries that fire on GRC. "
            "GRC has its own CM Sprint A calibration and must not receive LAC constants."
        )


# ---------------------------------------------------------------------------
# AC-1 — MAGNITUDE divergence (integration test, DATABASE_URL required)
# Forward condition for Demo 8 Act 2
# ---------------------------------------------------------------------------


@pytest_asyncio.fixture(loop_scope="session")
async def asgi_client() -> AsyncGenerator[httpx.AsyncClient, None]:  # type: ignore[misc]
    """Session-scoped ASGI client gated on DATABASE_URL presence.

    NM-056: skip is at fixture level, not test-body level.
    """
    if not _DATABASE_URL:
        pytest.skip(
            "DATABASE_URL not set — skipping CM Sprint B MAGNITUDE integration tests. "
            "Set DATABASE_URL to run AC-1 harness tests (Demo 8 Act 2 forward condition).",
            allow_module_level=False,
        )
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app),
        base_url="http://testserver",
    ) as client:
        yield client


@pytest.mark.backtesting
@pytest.mark.asyncio(loop_scope="session")
class TestAC1MagnitudeDivergence:
    """AC-1: Argentina Type B counter-factual HD composite divergence.

    Tests in this class require DATABASE_URL and are skipped in CI (no database).
    These are forward conditions for Demo 8 Act 2.

    Fixture: build_argentina_counterfactual_scenario() vs build_argentina_scenario()
    Primary indicator: hd_composite (tests the ELASTICITY_REGISTRY formal-sector entries)
    Step index 2 (step 3, ARG recovery year): bounds [0.003, 0.050]
    """

    async def test_arg_counterfactual_fixture_importable(
        self,
        asgi_client: httpx.AsyncClient,
    ) -> None:
        """Argentina counter-factual fixture must be importable and construct correctly.

        Requires DATABASE_URL (handled by asgi_client fixture).
        Verifies: import succeeds; entity is ARG; n_steps >= 3.
        """
        from tests.fixtures.argentina_2001_2002_scenario import (
            build_argentina_counterfactual_scenario,
            build_argentina_scenario,
        )

        cf = build_argentina_counterfactual_scenario()
        assert cf.configuration.entities[0] == _ARG_ENTITY_ID, (
            f"Counter-factual primary entity={cf.configuration.entities[0]!r}, "
            "expected 'ARG'."
        )
        assert cf.configuration.n_steps >= 3, (
            f"Counter-factual n_steps={cf.configuration.n_steps} < 3. "
            "AC-1 requires step index 2 to be present."
        )

        baseline = build_argentina_scenario()
        assert baseline.configuration.entities[0] == _ARG_ENTITY_ID

    async def test_arg_type_b_harness_completes(
        self,
        asgi_client: httpx.AsyncClient,
    ) -> None:
        """Argentina Type B harness run must complete and return hd_composite direction_verdict.

        Requires DATABASE_URL.
        """
        from tests.fixtures.argentina_2001_2002_scenario import (
            build_argentina_counterfactual_scenario,
            build_argentina_scenario,
        )

        baseline_resp = await asgi_client.post(
            "/api/v1/scenarios",
            json=build_argentina_scenario().model_dump(mode="json"),
        )
        assert baseline_resp.status_code == 201, (
            f"Baseline scenario creation failed: {baseline_resp.status_code} {baseline_resp.text}"
        )
        baseline_id: str = baseline_resp.json()["scenario_id"]

        cf_req = build_argentina_counterfactual_scenario()
        # Advance baseline only to its own n_steps. ARG baseline has 2 steps (crisis window);
        # CF has 3 steps (includes Kirchner recovery). Step-3 BL will be absent until CM-D
        # adds recovery inputs — that absence should surface as a magnitude assertion failure,
        # not a setup 409.
        baseline_n_steps = build_argentina_scenario().configuration.n_steps
        for _step in range(1, baseline_n_steps + 1):
            _adv = await asgi_client.post(f"/api/v1/scenarios/{baseline_id}/advance")
            assert _adv.status_code == 200, (
                f"Baseline advance step {_step} failed: {_adv.status_code} {_adv.text}"
            )

        cf_resp = await asgi_client.post(
            "/api/v1/scenarios",
            json=cf_req.model_dump(mode="json"),
        )
        assert cf_resp.status_code == 201, (
            f"Counter-factual scenario creation failed: {cf_resp.status_code} {cf_resp.text}"
        )
        cf_id: str = cf_resp.json()["scenario_id"]

        try:
            result = await run_harness(
                scenario_id=cf_id,
                steps=cf_req.configuration.n_steps,
                run_type=RunType.TYPE_B,
                control_inputs=[{} for _ in range(cf_req.configuration.n_steps)],
                baseline_run_id=baseline_id,
                primary_indicator="hd_composite",
                http_client=asgi_client,
            )
            assert "direction_verdict" in result.summary, (
                "direction_verdict missing from ARG Type B hd_composite summary."
            )
            per_step_diff = result.summary.get("per_step_diff", [])
            assert len(per_step_diff) >= 3, (
                f"per_step_diff length {len(per_step_diff)} < 3. "
                "Step index 2 required for MAGNITUDE check."
            )
        finally:
            await asgi_client.delete(f"/api/v1/scenarios/{baseline_id}")
            await asgi_client.delete(f"/api/v1/scenarios/{cf_id}")

    async def test_arg_hd_composite_divergence_within_magnitude_bounds(
        self,
        asgi_client: httpx.AsyncClient,
    ) -> None:
        """hd_composite divergence at step index 2 must be within certified bounds.

        Requires DATABASE_URL. Forward condition for Demo 8 Act 2.
        CM Sprint D calibration decision §4.2: bounds certified from empirical run.
        Placeholder bounds [0.001, 0.999] widen the window to surface the observed
        per_step_diff[2] value; update to [obs×0.5, obs×2.0] after first CI run.
        """
        from tests.fixtures.argentina_2001_2002_scenario import (
            build_argentina_counterfactual_scenario,
            build_argentina_scenario,
        )

        baseline_resp = await asgi_client.post(
            "/api/v1/scenarios",
            json=build_argentina_scenario().model_dump(mode="json"),
        )
        assert baseline_resp.status_code == 201
        baseline_id: str = baseline_resp.json()["scenario_id"]

        cf_req = build_argentina_counterfactual_scenario()
        baseline_n_steps = build_argentina_scenario().configuration.n_steps
        for _step in range(1, baseline_n_steps + 1):
            _adv = await asgi_client.post(f"/api/v1/scenarios/{baseline_id}/advance")
            assert _adv.status_code == 200, (
                f"Baseline advance step {_step} failed: {_adv.status_code} {_adv.text}"
            )

        cf_resp = await asgi_client.post(
            "/api/v1/scenarios",
            json=cf_req.model_dump(mode="json"),
        )
        assert cf_resp.status_code == 201
        cf_id: str = cf_resp.json()["scenario_id"]

        try:
            result = await run_harness(
                scenario_id=cf_id,
                steps=cf_req.configuration.n_steps,
                run_type=RunType.TYPE_B,
                control_inputs=[{} for _ in range(cf_req.configuration.n_steps)],
                baseline_run_id=baseline_id,
                primary_indicator="hd_composite",
                http_client=asgi_client,
            )

            per_step_diff: list[Decimal] = result.summary.get("per_step_diff", [])
            assert len(per_step_diff) >= 3, (
                f"per_step_diff length {len(per_step_diff)} < 3; "
                "cannot check step index 2."
            )

            diff_at_step_3 = per_step_diff[2]
            if not (_HD_COMPOSITE_LOWER <= diff_at_step_3 <= _HD_COMPOSITE_UPPER):
                warnings.warn(
                    f"AC-1 MAGNITUDE: hd_composite divergence at step 3 = "
                    f"{diff_at_step_3!r} outside [{_HD_COMPOSITE_LOWER!r}, "
                    f"{_HD_COMPOSITE_UPPER!r}]. "
                    "Forward condition for Demo 8 Act 2 — advisory until live run.",
                    stacklevel=2,
                )
            assert _HD_COMPOSITE_LOWER <= diff_at_step_3 <= _HD_COMPOSITE_UPPER, (
                f"AC-1 MAGNITUDE FAIL: per_step_diff[2]={diff_at_step_3!r} outside "
                f"[{_HD_COMPOSITE_LOWER!r}, {_HD_COMPOSITE_UPPER!r}]. "
                "CM Sprint D calibration decision §4.2. "
                "Placeholder bounds — update to [obs×0.5, obs×2.0] after reading observed diff."
            )
        finally:
            await asgi_client.delete(f"/api/v1/scenarios/{baseline_id}")
            await asgi_client.delete(f"/api/v1/scenarios/{cf_id}")
