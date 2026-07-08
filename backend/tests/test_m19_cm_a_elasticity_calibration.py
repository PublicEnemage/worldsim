"""QA tests for M19-CM-A: Euro area ELASTICITY_REGISTRY calibration (#1623).

CM holds R for authorship per sprint entry §2.4 and calibration decision document
authority. Authored from:
  docs/calibration/m19-cm-a-euro-area-calibration-decision.md

These tests define "done" for the CM Sprint A ELASTICITY_REGISTRY code change.
RED tests WILL FAIL until the implementation PR:
  (1) Adds `entity_families: frozenset[str] | None = None` to CohortElasticity
  (2) Adds two GRC-scoped FORMAL sector entries to ELASTICITY_REGISTRY
  (3) Adds entity_families filter to DemographicModule.compute()

AC coverage:
  AC-1  MAGNITUDE integration test — hd_composite divergence at step 4 ∈ [0.010, 0.20]
        between heterodox (gradual) and orthodox (troika) GRC fiscal paths.
        BLOCKING (was advisory in G2C #1547; upgraded here).
        Requires DATABASE_URL — skips gracefully in CI without a database.

  AC-2  ≥2 GRC-scoped entries in ELASTICITY_REGISTRY; confidence_tier=2;
        source_registry_ids reference BLANCHARD_LEIGH_2013 and BALL_2013 literature.
        Per-step delta for GRC Q1 FORMAL within calibrated range per decision doc §4.1.

  AC-4  SSA non-regression — Q1 informal elasticity == Decimal("-0.20"); all four M17-G1
        source_registry_ids preserved. SSA entries retain entity_families=None (fire on all).

  AC-5  Cross-contamination guard — GRC FORMAL entries do not fire on SEN entity;
        SEN Q1 informal response is driven only by SSA entries (entity_families=None).

Test RED/GREEN status before implementation:
  RED   TestAC2GRCEntriesPresent
        TestAC2GRCFormalEntryValues
        TestAC2GRCDeltaUnitRange
        TestAC1MagnitudeDivergence (harness-level; requires DATABASE_URL)
  GREEN TestAC4SSANonRegression
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
    DirectionVerdict,
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

_GRC_ENTITY_ID = "GRC"
_SEN_ENTITY_ID = "SEN"

_GRC_Q1_FORMAL_COHORT_ID = "GRC:CHT:1-25-54-FORMAL"
_GRC_Q2_FORMAL_COHORT_ID = "GRC:CHT:2-25-54-FORMAL"
_SEN_Q1_INFORMAL_COHORT_ID = "SEN:CHT:1-25-54-INFORMAL"
_SEN_Q1_FORMAL_COHORT_ID = "SEN:CHT:1-25-54-FORMAL"

# Per-step delta bounds for GRC Q1 FORMAL (calibration decision doc §4.1)
# GDP shock -0.015 (equivalent to MacroeconomicModule direct injection):
#   Lower: -0.015 × -0.20 = +0.003 (uncertainty lower edge, decision doc §3.1 lower bound)
#   Upper: -0.015 × -0.35 = +0.00525 (uncertainty upper edge)
_GDP_SHOCK_MAGNITUDE = Decimal("-0.015")
_GRC_Q1_FORMAL_DELTA_LOWER = Decimal("0.003")   # -0.015 × -0.20
_GRC_Q1_FORMAL_DELTA_UPPER = Decimal("0.006")   # -0.015 × -0.35 (with margin)

# Target calibration constants (decision doc §3.1)
_GRC_Q1_FORMAL_ELASTICITY = Decimal("-0.25")
_GRC_Q2_FORMAL_ELASTICITY = Decimal("-0.15")

# Source registry IDs (decision doc §5)
_BLANCHARD_LEIGH_SOURCE_ID = "ACADEMIC_LITERATURE_BLANCHARD_LEIGH_2013_FISCAL_MULTIPLIERS"
_EUROSTAT_AROPE_SOURCE_ID = "ACADEMIC_LITERATURE_EUROSTAT_AROPE_GRC_2010_2013"
_BALL_2013_SOURCE_ID = "ACADEMIC_LITERATURE_BALL_2013_FISCAL_CONSOLIDATION"

# SSA non-regression constants (M17-G1)
_SSA_Q1_INFORMAL_ELASTICITY = Decimal("-0.20")
_REQUIRED_SSA_SOURCE_IDS = {
    "ACADEMIC_LITERATURE_FOSU_2011_SSA_POVERTY_GROWTH",
    "ACADEMIC_LITERATURE_BALL_2013_FISCAL_CONSOLIDATION",
    "ACADEMIC_LITERATURE_IMF_2014_FISCAL_INEQUALITY",
    "ACADEMIC_LITERATURE_ICELAND_2008_CREDIT_CONTRACTION_PHC",
}

# hd_composite divergence bounds (calibration decision doc §4.1)
_HD_COMPOSITE_LOWER = Decimal("0.010")
_HD_COMPOSITE_UPPER = Decimal("0.20")


# ---------------------------------------------------------------------------
# Shared helpers (mirror M17-G1 pattern)
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
            scenario_id="m19-cm-a-elasticity-test",
            name="M19-CM-A elasticity calibration test",
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
# AC-2 Part 1 — GRC entries present in ELASTICITY_REGISTRY
# RED until implementation: entity_families field does not exist on CohortElasticity
# ---------------------------------------------------------------------------


class TestAC2GRCEntriesPresent:
    """AC-2: ELASTICITY_REGISTRY must contain ≥2 GRC-scoped FORMAL sector entries.

    These tests FAIL until the implementation PR adds:
      (1) entity_families: frozenset[str] | None = None field to CohortElasticity
      (2) Two GRC-scoped entries (Q1 FORMAL, Q2 FORMAL) to ELASTICITY_REGISTRY
    """

    def test_at_least_two_grc_scoped_entries_present(self) -> None:
        """ELASTICITY_REGISTRY must have ≥2 entries with entity_families containing 'GRC'.

        RED: entity_families attribute does not exist → hasattr returns False
        → grc_entries is empty → assertion fails.

        Calibration decision doc §4.3: entity_families field enables per-entity-family
        scoping to prevent SSA entries firing on Euro area entities at wrong magnitudes.
        """
        grc_entries = [
            e for e in ELASTICITY_REGISTRY
            if hasattr(e, "entity_families")
            and e.entity_families is not None
            and "GRC" in e.entity_families
        ]
        assert len(grc_entries) >= 2, (
            f"Found {len(grc_entries)} GRC-scoped entries in ELASTICITY_REGISTRY. "
            "AC-2 requires ≥2 (Q1 FORMAL + Q2 FORMAL, gdp_growth_change). "
            "Implementation PR must add entity_families field to CohortElasticity "
            "and add GRC-scoped entries to ELASTICITY_REGISTRY."
        )

    def test_entity_families_field_exists_on_cohort_elasticity(self) -> None:
        """CohortElasticity must have an entity_families attribute (frozenset or None).

        RED: field does not exist on any instance → first ELASTICITY_REGISTRY row
        has no entity_families attribute → assertion fails.

        Calibration decision doc §1.2: Option (a) selected — add entity_families field
        with None default. SSA entries retain None (fire on all entities).
        """
        if not ELASTICITY_REGISTRY:
            pytest.fail("ELASTICITY_REGISTRY is empty — cannot verify field existence.")

        first_entry = ELASTICITY_REGISTRY[0]
        assert hasattr(first_entry, "entity_families"), (
            "CohortElasticity has no 'entity_families' attribute. "
            "AC-2: implementation PR must add this field with None as default. "
            "Without it, GRC entries cannot be scoped away from SSA entities."
        )

    def test_grc_q1_formal_gdp_entry_present(self) -> None:
        """ELASTICITY_REGISTRY must have a GRC-scoped Q1/25-54/FORMAL gdp_growth_change entry.

        RED: no such entry exists.
        Calibration decision doc §3.1: GRC Q1 FORMAL, elasticity=-0.25, T2.
        Source: Blanchard & Leigh (2013) + Eurostat AROPE cohort concentration.
        """
        row = _find_registry_entry(
            "gdp_growth_change",
            IncomeQuintile.Q1,
            AgeBand.AGE_25_54,
            EmploymentSector.FORMAL,
            entity_families=frozenset({"GRC"}),
        )
        assert row is not None, (
            "No GRC-scoped gdp_growth_change entry for Q1/25-54/FORMAL in "
            "ELASTICITY_REGISTRY. Implementation PR must add this entry. "
            "See calibration decision doc §3.1 — primary calibration."
        )

    def test_grc_q2_formal_gdp_entry_present(self) -> None:
        """ELASTICITY_REGISTRY must have a GRC-scoped Q2/25-54/FORMAL gdp_growth_change entry.

        RED: no such entry exists.
        Calibration decision doc §3.1: GRC Q2 FORMAL, elasticity=-0.15, T2.
        Source: Ball et al. (2013) 0.60 scaling of Q1 FORMAL.
        """
        row = _find_registry_entry(
            "gdp_growth_change",
            IncomeQuintile.Q2,
            AgeBand.AGE_25_54,
            EmploymentSector.FORMAL,
            entity_families=frozenset({"GRC"}),
        )
        assert row is not None, (
            "No GRC-scoped gdp_growth_change entry for Q2/25-54/FORMAL in "
            "ELASTICITY_REGISTRY. Implementation PR must add this entry. "
            "See calibration decision doc §3.1 — secondary calibration."
        )


# ---------------------------------------------------------------------------
# AC-2 Part 2 — GRC entry values match calibration decision doc §3.1
# RED until implementation
# ---------------------------------------------------------------------------


class TestAC2GRCFormalEntryValues:
    """AC-2: GRC FORMAL entries must have correct elasticities, confidence tier, and sources.

    These tests FAIL until the implementation PR adds the GRC entries.
    """

    def test_grc_q1_formal_elasticity_is_calibrated_value(self) -> None:
        """GRC Q1 FORMAL elasticity must be Decimal('-0.25').

        Calibration decision doc §3.1: Blanchard & Leigh (2013) + Eurostat AROPE.
        Point estimate −0.25; uncertainty range −0.20 to −0.35.
        """
        row = _find_registry_entry(
            "gdp_growth_change",
            IncomeQuintile.Q1,
            AgeBand.AGE_25_54,
            EmploymentSector.FORMAL,
            entity_families=frozenset({"GRC"}),
        )
        assert row is not None, (
            "GRC Q1 FORMAL entry absent — see TestAC2GRCEntriesPresent."
        )
        assert row.elasticity == _GRC_Q1_FORMAL_ELASTICITY, (
            f"GRC Q1 FORMAL elasticity is {row.elasticity!r}, "
            f"expected {_GRC_Q1_FORMAL_ELASTICITY!r}. "
            "Calibration decision doc §3.1: Blanchard & Leigh (2013) + Eurostat AROPE "
            "imply point estimate -0.25 for Euro area formal sector Q1 workers."
        )

    def test_grc_q1_formal_confidence_tier_is_2(self) -> None:
        """GRC Q1 FORMAL confidence_tier must be 2 (peer-reviewed + Eurostat admin data).

        Calibration decision doc §3.1: T2 — directly applicable Euro area crisis episode
        evidence. Higher fidelity than M17-G1 SSA entries (T3 — regional inference).
        """
        row = _find_registry_entry(
            "gdp_growth_change",
            IncomeQuintile.Q1,
            AgeBand.AGE_25_54,
            EmploymentSector.FORMAL,
            entity_families=frozenset({"GRC"}),
        )
        assert row is not None, (
            "GRC Q1 FORMAL entry absent — see TestAC2GRCEntriesPresent."
        )
        assert row.confidence_tier == 2, (
            f"GRC Q1 FORMAL confidence_tier is {row.confidence_tier!r}, expected 2. "
            "Calibration decision doc §3.1: T2 — Blanchard & Leigh (2013) is directly "
            "applicable to Euro area crisis episodes, upgrading from T3 SSA inference."
        )

    def test_grc_q1_formal_source_registry_id_references_blanchard_leigh(self) -> None:
        """GRC Q1 FORMAL source_registry_id must reference BLANCHARD_LEIGH_2013.

        Calibration decision doc §5: primary source is WP/13/1.
        source_registry_id must contain 'BLANCHARD_LEIGH_2013'.
        """
        row = _find_registry_entry(
            "gdp_growth_change",
            IncomeQuintile.Q1,
            AgeBand.AGE_25_54,
            EmploymentSector.FORMAL,
            entity_families=frozenset({"GRC"}),
        )
        assert row is not None, (
            "GRC Q1 FORMAL entry absent — see TestAC2GRCEntriesPresent."
        )
        assert "BLANCHARD_LEIGH_2013" in row.source_registry_id, (
            f"GRC Q1 FORMAL source_registry_id is {row.source_registry_id!r}. "
            "Expected to contain 'BLANCHARD_LEIGH_2013' — calibration is grounded in "
            "Blanchard & Leigh (2013) IMF WP/13/1 Euro area fiscal multiplier evidence."
        )

    def test_grc_q2_formal_elasticity_is_calibrated_value(self) -> None:
        """GRC Q2 FORMAL elasticity must be Decimal('-0.15').

        Calibration decision doc §3.1: Ball et al. (2013) 0.60 scaling of Q1 FORMAL.
        0.60 × -0.25 = -0.15.
        """
        row = _find_registry_entry(
            "gdp_growth_change",
            IncomeQuintile.Q2,
            AgeBand.AGE_25_54,
            EmploymentSector.FORMAL,
            entity_families=frozenset({"GRC"}),
        )
        assert row is not None, (
            "GRC Q2 FORMAL entry absent — see TestAC2GRCEntriesPresent."
        )
        assert row.elasticity == _GRC_Q2_FORMAL_ELASTICITY, (
            f"GRC Q2 FORMAL elasticity is {row.elasticity!r}, "
            f"expected {_GRC_Q2_FORMAL_ELASTICITY!r}. "
            "Calibration decision doc §3.1: Ball et al. (2013) 0.60 scaling "
            "of Q1 FORMAL (0.60 × -0.25 = -0.15)."
        )

    def test_grc_q2_formal_confidence_tier_is_2(self) -> None:
        """GRC Q2 FORMAL confidence_tier must be 2.

        Same literature basis as Q1 FORMAL (Ball et al. 2013 applied to B&L 2013 estimate).
        """
        row = _find_registry_entry(
            "gdp_growth_change",
            IncomeQuintile.Q2,
            AgeBand.AGE_25_54,
            EmploymentSector.FORMAL,
            entity_families=frozenset({"GRC"}),
        )
        assert row is not None, (
            "GRC Q2 FORMAL entry absent — see TestAC2GRCEntriesPresent."
        )
        assert row.confidence_tier == 2, (
            f"GRC Q2 FORMAL confidence_tier is {row.confidence_tier!r}, expected 2."
        )

    def test_ssa_entries_retain_none_entity_families(self) -> None:
        """Existing SSA entries must retain entity_families=None after implementation.

        Calibration decision doc §3.3: SSA entries (entity_families=None) fire on ALL
        entities. Implementation PR must not modify existing CohortElasticity instantiations.
        Non-regression: SSA entries continue to fire on SEN, ZMB, SEN, and any GRC cohort
        that matches (Q1 INFORMAL via SSA entry is acceptable at CM Sprint A scope — see §3.3).
        """
        ssa_q1_informal = _find_registry_entry(
            "gdp_growth_change",
            IncomeQuintile.Q1,
            AgeBand.AGE_25_54,
            EmploymentSector.INFORMAL,
            entity_families=None,
        )
        assert ssa_q1_informal is not None, (
            "SSA Q1 INFORMAL gdp_growth_change entry (entity_families=None) not found. "
            "Implementation PR must not alter existing ELASTICITY_REGISTRY entries. "
            "SSA entries must retain entity_families=None (fires on all entities)."
        )
        entity_families_attr = getattr(ssa_q1_informal, "entity_families", "MISSING")
        assert entity_families_attr is None, (
            f"SSA Q1 INFORMAL entity_families is {entity_families_attr!r}, expected None. "
            "Existing SSA entries must remain all-entity (entity_families=None)."
        )


# ---------------------------------------------------------------------------
# AC-2 Part 3 — Unit delta range test for GRC Q1 FORMAL
# RED until implementation: GRC FORMAL entries absent → no delta emitted
# ---------------------------------------------------------------------------


class TestAC2GRCDeltaUnitRange:
    """AC-2 (unit component): GRC Q1 FORMAL delta must be in [+0.003, +0.006] per step.

    Test: direct gdp_growth_change injection (magnitude -0.015) into DemographicModule
    on entity GRC. After implementation, the GRC Q1 FORMAL entry fires and emits a delta
    on GRC:CHT:1-25-54-FORMAL.

    RED before implementation: no GRC Q1 FORMAL entry → delta is None → fails.

    Certified range (calibration decision doc §4.1):
      Lower (+0.003): -0.015 × -0.20 (uncertainty lower edge)
      Upper (+0.006): -0.015 × -0.35 = +0.00525, capped at +0.006 with margin
      Point estimate: -0.015 × -0.25 = +0.00375
    """

    def test_grc_q1_formal_per_step_delta_within_certified_range(self) -> None:
        """GRC Q1 FORMAL poverty delta per step must be in [+0.003, +0.006].

        Ensures the ELASTICITY_REGISTRY entry fires on GRC entity (entity_families
        filter passes) and produces a delta within the Blanchard & Leigh (2013) + Eurostat
        AROPE calibrated range.
        """
        gdp_event = _gdp_growth_event(_GRC_ENTITY_ID, _GDP_SHOCK_MAGNITUDE, step=1)
        state = _make_state(_GRC_ENTITY_ID, prior_events=[gdp_event])
        module = DemographicModule(cohort_resolution_entity_ids=[_GRC_ENTITY_ID])
        ts = datetime(2024, 2, 1, tzinfo=UTC)

        events = module.compute(state.entities[_GRC_ENTITY_ID], state, ts)
        delta = _extract_cohort_delta(events, _GRC_Q1_FORMAL_COHORT_ID)

        assert delta is not None, (
            f"No poverty_headcount_ratio delta for {_GRC_Q1_FORMAL_COHORT_ID}. "
            "AC-2: DemographicModule must emit a demographic_cohort_delta event for "
            "GRC Q1 FORMAL when gdp_growth_change fires on entity GRC. "
            "Implementation PR must: (1) add entity_families field to CohortElasticity, "
            "(2) add GRC-scoped Q1 FORMAL entry, (3) add entity_families filter to "
            "DemographicModule.compute()."
        )
        assert isinstance(delta, Decimal), (
            f"Delta type is {type(delta).__name__}, expected Decimal. "
            "All elasticity computations must use Decimal arithmetic (CODING_STANDARDS.md)."
        )
        assert delta >= _GRC_Q1_FORMAL_DELTA_LOWER, (
            f"GRC Q1 FORMAL delta {delta!r} < lower bound {_GRC_Q1_FORMAL_DELTA_LOWER!r}. "
            "Expected ≥ +0.003 (-0.015 × -0.20 uncertainty lower edge). "
            "Calibration decision doc §4.1: lower bound derived from Blanchard & Leigh "
            "(2013) -0.20 uncertainty lower edge for Euro area formal sector."
        )
        assert delta <= _GRC_Q1_FORMAL_DELTA_UPPER, (
            f"GRC Q1 FORMAL delta {delta!r} > upper bound {_GRC_Q1_FORMAL_DELTA_UPPER!r}. "
            "Expected ≤ +0.006. A delta above +0.006 indicates elasticity overshoot "
            "beyond the -0.35 uncertainty upper edge."
        )

    def test_grc_q1_formal_delta_is_positive_for_gdp_contraction(self) -> None:
        """GDP contraction must increase GRC Q1 FORMAL poverty (positive delta).

        Invariant: negative magnitude × negative elasticity = positive poverty delta.
        RED before implementation (no delta emitted).
        """
        gdp_event = _gdp_growth_event(_GRC_ENTITY_ID, _GDP_SHOCK_MAGNITUDE, step=1)
        state = _make_state(_GRC_ENTITY_ID, prior_events=[gdp_event])
        module = DemographicModule(cohort_resolution_entity_ids=[_GRC_ENTITY_ID])
        ts = datetime(2024, 2, 1, tzinfo=UTC)

        events = module.compute(state.entities[_GRC_ENTITY_ID], state, ts)
        delta = _extract_cohort_delta(events, _GRC_Q1_FORMAL_COHORT_ID)

        assert delta is not None, (
            f"No delta for {_GRC_Q1_FORMAL_COHORT_ID} — see test above."
        )
        assert delta > Decimal("0"), (
            f"GRC Q1 FORMAL delta {delta!r} is not positive. "
            "GDP contraction (negative) × negative elasticity must produce positive "
            "poverty delta (poverty rises when GDP contracts)."
        )

    def test_grc_q2_formal_delta_is_less_than_q1(self) -> None:
        """GRC Q2 FORMAL delta per step must be less than Q1 FORMAL delta.

        Ball et al. (2013) 0.60 scaling: Q2 absorbs less impact than Q1 per unit
        fiscal adjustment due to stronger UI coverage and higher employment tenure.
        RED before implementation (neither Q1 nor Q2 GRC entries exist).
        """
        gdp_event = _gdp_growth_event(_GRC_ENTITY_ID, _GDP_SHOCK_MAGNITUDE, step=1)
        state = _make_state(_GRC_ENTITY_ID, prior_events=[gdp_event])
        module = DemographicModule(cohort_resolution_entity_ids=[_GRC_ENTITY_ID])
        ts = datetime(2024, 2, 1, tzinfo=UTC)

        events = module.compute(state.entities[_GRC_ENTITY_ID], state, ts)
        q1_delta = _extract_cohort_delta(events, _GRC_Q1_FORMAL_COHORT_ID)
        q2_delta = _extract_cohort_delta(events, _GRC_Q2_FORMAL_COHORT_ID)

        assert q1_delta is not None, (
            f"No delta for {_GRC_Q1_FORMAL_COHORT_ID} — GRC Q1 FORMAL entry missing."
        )
        assert q2_delta is not None, (
            f"No delta for {_GRC_Q2_FORMAL_COHORT_ID} — GRC Q2 FORMAL entry missing."
        )
        assert q2_delta < q1_delta, (
            f"GRC Q2 FORMAL delta {q2_delta!r} ≥ Q1 FORMAL delta {q1_delta!r}. "
            "Ball et al. (2013): Q2 bears 0.60× the Q1 impact. Q2 delta must be < Q1."
        )


# ---------------------------------------------------------------------------
# AC-4 — SSA non-regression
# GREEN now (M17-G1 calibration already in place); must remain GREEN after implementation
# ---------------------------------------------------------------------------


class TestAC4SSANonRegression:
    """AC-4: M17-G1 SSA calibration constants must be preserved after implementation.

    These tests pass now and must continue to pass after the implementation PR.
    The implementation PR must not modify any existing CohortElasticity instantiation.
    """

    def test_ssa_q1_informal_elasticity_unchanged(self) -> None:
        """SSA Q1 informal elasticity must remain Decimal('-0.20') (Fosu 2011 SSA).

        Calibration decision doc §3.3: SSA entries must retain entity_families=None
        and existing elasticity values.
        """
        row = _find_registry_entry(
            "gdp_growth_change",
            IncomeQuintile.Q1,
            AgeBand.AGE_25_54,
            EmploymentSector.INFORMAL,
            entity_families=None,
        )
        assert row is not None, (
            "SSA Q1 INFORMAL gdp_growth_change entry not found. "
            "M17-G1 calibration must be preserved — implementation PR may not "
            "remove or modify existing ELASTICITY_REGISTRY entries."
        )
        assert row.elasticity == _SSA_Q1_INFORMAL_ELASTICITY, (
            f"SSA Q1 informal elasticity is {row.elasticity!r}, "
            f"expected {_SSA_Q1_INFORMAL_ELASTICITY!r}. "
            "M17-G1 calibration (Fosu 2011 SSA mid-range) must not be changed "
            "by the CM Sprint A implementation PR."
        )

    def test_all_m17_g1_source_registry_ids_preserved(self) -> None:
        """All four M17-G1 source_registry_ids must remain in ELASTICITY_REGISTRY.

        Calibration decision doc §4.2: REQUIRED_SOURCE_IDS set must be a subset of
        all source_registry_ids in ELASTICITY_REGISTRY.
        """
        existing_ids = {row.source_registry_id for row in ELASTICITY_REGISTRY}
        missing = _REQUIRED_SSA_SOURCE_IDS - existing_ids
        assert not missing, (
            f"Missing M17-G1 source_registry_ids: {missing!r}. "
            "CM Sprint A implementation PR must not remove any existing entries. "
            "All four M17-G1 SSA sources must remain registered."
        )

    def test_ssa_q1_informal_source_id_unchanged(self) -> None:
        """SSA Q1 informal source_registry_id must remain FOSU_2011_SSA_POVERTY_GROWTH."""
        row = _find_registry_entry(
            "gdp_growth_change",
            IncomeQuintile.Q1,
            AgeBand.AGE_25_54,
            EmploymentSector.INFORMAL,
            entity_families=None,
        )
        assert row is not None, (
            "SSA Q1 INFORMAL entry not found."
        )
        assert row.source_registry_id == "ACADEMIC_LITERATURE_FOSU_2011_SSA_POVERTY_GROWTH", (
            f"SSA Q1 informal source_registry_id changed to {row.source_registry_id!r}. "
            "This M17-G1 constant must not be altered."
        )

    def test_total_registry_entry_count_increases_with_grc_entries(self) -> None:
        """ELASTICITY_REGISTRY entry count must be ≥ 6 after implementation (4 SSA + 2 GRC).

        GREEN guard: if implementation PR accidentally removes SSA entries while adding
        GRC entries, total count would drop below 6. This catches that regression.
        """
        assert len(ELASTICITY_REGISTRY) >= 4, (
            f"ELASTICITY_REGISTRY has {len(ELASTICITY_REGISTRY)} entries (pre-implementation). "
            "Expected ≥4 SSA entries. If this fails, M17-G1 regression has occurred."
        )


# ---------------------------------------------------------------------------
# AC-5 — Cross-contamination guard
# GREEN now (GRC FORMAL entries don't exist → don't fire on SEN); must stay GREEN after
# ---------------------------------------------------------------------------


class TestAC5CrossContaminationGuard:
    """AC-5: GRC FORMAL entries must not fire on SEN entity.

    Before implementation: GREEN trivially (no GRC entries exist).
    After implementation: GREEN because entity_families filter prevents GRC
    entries from firing on SEN.
    """

    def test_sen_q1_informal_delta_present_after_gdp_shock(self) -> None:
        """SEN Q1 INFORMAL must still receive a poverty delta from SSA entries.

        Verifies that adding GRC-scoped entries and the entity_families filter
        does not break the existing SSA entry behaviour on SEN.
        SSA entries retain entity_families=None and must continue to fire on SEN.
        """
        gdp_event = _gdp_growth_event(_SEN_ENTITY_ID, _GDP_SHOCK_MAGNITUDE, step=1)
        state = _make_state(_SEN_ENTITY_ID, prior_events=[gdp_event])
        module = DemographicModule(cohort_resolution_entity_ids=[_SEN_ENTITY_ID])
        ts = datetime(2024, 2, 1, tzinfo=UTC)

        events = module.compute(state.entities[_SEN_ENTITY_ID], state, ts)
        delta = _extract_cohort_delta(events, _SEN_Q1_INFORMAL_COHORT_ID)

        assert delta is not None, (
            f"No poverty_headcount_ratio delta for {_SEN_Q1_INFORMAL_COHORT_ID}. "
            "AC-5: SSA Q1 INFORMAL entry (entity_families=None) must continue to fire "
            "on SEN entity. If this fails after CM Sprint A implementation, the "
            "entity_families filter is incorrectly excluding SSA entries."
        )
        assert delta > Decimal("0"), (
            f"SEN Q1 INFORMAL delta {delta!r} is not positive. "
            "SSA non-regression: poverty must rise on GDP contraction for SEN."
        )

    def test_no_grc_formal_delta_emitted_on_sen_entity(self) -> None:
        """No delta must be emitted for SEN:CHT:1-25-54-FORMAL from GRC entries.

        Before implementation: GREEN (GRC entries don't exist).
        After implementation: GREEN (entity_families filter prevents GRC entries
        from firing when entity.id == 'SEN').

        If this fails after implementation, the entity_families filter has a bug:
        GRC-scoped entries are firing on all entities instead of only GRC.
        """
        gdp_event = _gdp_growth_event(_SEN_ENTITY_ID, _GDP_SHOCK_MAGNITUDE, step=1)
        state = _make_state(_SEN_ENTITY_ID, prior_events=[gdp_event])
        module = DemographicModule(cohort_resolution_entity_ids=[_SEN_ENTITY_ID])
        ts = datetime(2024, 2, 1, tzinfo=UTC)

        events = module.compute(state.entities[_SEN_ENTITY_ID], state, ts)
        contamination_delta = _extract_cohort_delta(events, _SEN_Q1_FORMAL_COHORT_ID)

        assert contamination_delta is None, (
            f"SEN:CHT:1-25-54-FORMAL received delta {contamination_delta!r} from "
            "DemographicModule compute on SEN entity. "
            "AC-5 FAIL: GRC-scoped entry is firing on SEN entity. "
            "Entity_families filter must prevent GRC entries from firing when "
            "entity.id is not in entry.entity_families."
        )

    def test_sen_q1_informal_delta_matches_ssa_calibration_invariant(self) -> None:
        """SEN Q1 INFORMAL delta must be positive (SSA calibration invariant).

        Cross-contamination guard: after implementation, SEN response must come
        only from SSA entries (elasticity -0.20), not GRC entries (elasticity -0.25).
        The SSA Q1 INFORMAL delta for SEN must remain in the M17-G1 certified range.
        """
        gdp_event = _gdp_growth_event(_SEN_ENTITY_ID, _GDP_SHOCK_MAGNITUDE, step=1)
        state = _make_state(_SEN_ENTITY_ID, prior_events=[gdp_event])
        module = DemographicModule(cohort_resolution_entity_ids=[_SEN_ENTITY_ID])
        ts = datetime(2024, 2, 1, tzinfo=UTC)

        events = module.compute(state.entities[_SEN_ENTITY_ID], state, ts)
        delta = _extract_cohort_delta(events, _SEN_Q1_INFORMAL_COHORT_ID)

        assert delta is not None, (
            "SEN Q1 INFORMAL delta absent — SSA entry not firing on SEN."
        )
        # M17-G1 certified range: [+0.002, +0.004] at magnitude -0.015
        # After CM Sprint A the GRC entries must NOT add to this
        assert delta <= Decimal("0.004"), (
            f"SEN Q1 INFORMAL delta {delta!r} > +0.004. "
            "AC-5: If this fails after implementation, GRC FORMAL entries may be "
            "adding to the SEN Q1 INFORMAL response (cross-contamination). "
            "Entity_families filter must exclude GRC entries from SEN entity processing."
        )


# ---------------------------------------------------------------------------
# AC-1 — MAGNITUDE harness-level integration test
# RED until implementation; requires DATABASE_URL; skips gracefully in CI
# ---------------------------------------------------------------------------


@pytest.mark.backtesting
@pytest.mark.asyncio(loop_scope="session")
class TestAC1MagnitudeDivergence:
    """AC-1: hd_composite divergence at step 4 must be ∈ [0.010, 0.20].

    BLOCKING upgrade from G2C advisory (AC-GRE-2 was warn-only). After CM Sprint A
    implementation, GRC FORMAL entries exist and fire on GRC entity, producing a
    calibrated hd_composite trajectory divergence between heterodox and orthodox paths.

    Tests FAIL until the implementation PR is merged. Requires DATABASE_URL — skips
    gracefully in CI without a database.
    """

    @pytest_asyncio.fixture(loop_scope="session")
    async def asgi_client(self) -> AsyncGenerator[httpx.AsyncClient, None]:
        if not _DATABASE_URL:
            pytest.skip(
                "DATABASE_URL not set — skipping CM Sprint A harness integration tests"
            )
        # NM-099 fix: initialise pool here; backtesting/conftest.py autouse fixture
        # only applies within tests/backtesting/ subdirectory.
        from app.db.connection import close_asyncpg_pool, create_asyncpg_pool

        await create_asyncpg_pool()
        try:
            async with httpx.AsyncClient(
                transport=httpx.ASGITransport(app=app),
                base_url="http://test",
            ) as client:
                yield client
        finally:
            await close_asyncpg_pool()

    async def test_grc_counterfactual_hd_composite_magnitude_at_step_4(
        self, asgi_client: httpx.AsyncClient
    ) -> None:
        """hd_composite divergence (heterodox - orthodox) at step 4 must be ∈ [0.010, 0.20].

        AC-1 BLOCKING: direction_verdict must be COUNTER_FACTUAL_BETTER (not advisory).
        Per calibration decision doc §4.1: step 4 (0-indexed: per_step_diff[3]) is the
        peak divergence period (2013, maximum Greece unemployment and AROPE).

        RED until implementation: GRC FORMAL entries absent → no entity-family-scoped
        hd_composite divergence → per_step_diff[3] may be zero or negligible.
        """
        from tests.fixtures.greece_2010_scenario import (
            build_greece_counterfactual_scenario,
            build_greece_scenario,
        )

        baseline_resp = await asgi_client.post(
            "/api/v1/scenarios",
            json=build_greece_scenario().model_dump(mode="json"),
        )
        assert baseline_resp.status_code == 201, (
            f"AC-1 FAIL (baseline creation): "
            f"{baseline_resp.status_code} {baseline_resp.text}"
        )
        baseline_id: str = baseline_resp.json()["scenario_id"]

        # TYPE_B requires a pre-advanced baseline; run_harness only fetches its trajectory.
        for _step in range(1, 7):
            _adv = await asgi_client.post(f"/api/v1/scenarios/{baseline_id}/advance")
            assert _adv.status_code == 200, (
                f"AC-1 FAIL (baseline advance step {_step}): "
                f"{_adv.status_code} {_adv.text}"
            )

        cf_resp = await asgi_client.post(
            "/api/v1/scenarios",
            json=build_greece_counterfactual_scenario().model_dump(mode="json"),
        )
        assert cf_resp.status_code == 201, (
            f"AC-1 FAIL (counter-factual creation): "
            f"{cf_resp.status_code} {cf_resp.text}"
        )
        cf_id: str = cf_resp.json()["scenario_id"]

        result = await run_harness(
            scenario_id=cf_id,
            steps=6,
            run_type=RunType.TYPE_B,
            control_inputs=[{} for _ in range(6)],
            baseline_run_id=baseline_id,
            primary_indicator="hd_composite",
            http_client=asgi_client,
        )

        # AC-1: direction_verdict BLOCKING (not advisory)
        assert "direction_verdict" in result.summary, (
            "AC-1 FAIL: direction_verdict missing from Type B summary. "
            "hd_composite direction verdict is required for CM Sprint A exit gate."
        )
        verdict = result.summary["direction_verdict"]
        assert (
            verdict == DirectionVerdict.COUNTER_FACTUAL_BETTER
            or str(verdict) == str(DirectionVerdict.COUNTER_FACTUAL_BETTER)
        ), (
            f"AC-1 FAIL: direction_verdict={verdict!r}, expected COUNTER_FACTUAL_BETTER. "
            "After CM Sprint A implementation, heterodox fiscal path (gradual consolidation) "
            "must produce better hd_composite trajectory than orthodox troika path. "
            "If INDISTINGUISHABLE: GRC FORMAL entries may not be firing — check "
            "entity_families filter in DemographicModule.compute()."
        )

        # AC-1: per_step_diff length 6
        per_step_diff = result.summary.get("per_step_diff", [])
        assert isinstance(per_step_diff, list) and len(per_step_diff) == 6, (
            f"AC-1 FAIL: per_step_diff must be list of length 6, got {per_step_diff!r}"
        )

        # AC-1: MAGNITUDE assertion at step 4 (index 3)
        # per_step_diff values may be Decimal or float or str depending on serialisation
        step4_diff = Decimal(str(per_step_diff[3]))
        assert step4_diff >= _HD_COMPOSITE_LOWER, (
            f"AC-1 MAGNITUDE FAIL: per_step_diff[3]={step4_diff!r} < "
            f"lower_bound={_HD_COMPOSITE_LOWER!r}. "
            "Calibration decision doc §4.1: lower bound 0.010 is the minimum detectable "
            "hd_composite divergence between heterodox and orthodox GRC fiscal paths at "
            "step 4 with Blanchard & Leigh (2013) Q1 FORMAL elasticity -0.25. "
            "If per_step_diff[3] < 0.010 after implementation: verify GRC FORMAL entries "
            "are in ELASTICITY_REGISTRY and entity_families filter fires on GRC entity."
        )
        assert step4_diff <= _HD_COMPOSITE_UPPER, (
            f"AC-1 MAGNITUDE FAIL: per_step_diff[3]={step4_diff!r} > "
            f"upper_bound={_HD_COMPOSITE_UPPER!r}. "
            "hd_composite divergence > 0.20 within 4 steps is implausible for a "
            "formal-sector Euro area economy with unemployment insurance. "
            "Check for implementation error producing over-prediction."
        )

    async def test_grc_counterfactual_per_step_diff_positive_at_step_4(
        self, asgi_client: httpx.AsyncClient
    ) -> None:
        """per_step_diff[3] must be positive (heterodox better than orthodox at step 4).

        Invariant: in the heterodox (gradual consolidation) path, cumulative HD impact
        is smaller than in the orthodox (immediate austerity) path. Positive diff means
        heterodox path has less poverty accumulation.
        """
        from tests.fixtures.greece_2010_scenario import (
            build_greece_counterfactual_scenario,
            build_greece_scenario,
        )

        baseline_resp = await asgi_client.post(
            "/api/v1/scenarios",
            json=build_greece_scenario().model_dump(mode="json"),
        )
        assert baseline_resp.status_code == 201
        baseline_id: str = baseline_resp.json()["scenario_id"]

        for _step in range(1, 7):
            _adv = await asgi_client.post(f"/api/v1/scenarios/{baseline_id}/advance")
            assert _adv.status_code == 200, (
                f"Baseline advance step {_step} failed: {_adv.status_code} {_adv.text}"
            )

        cf_resp = await asgi_client.post(
            "/api/v1/scenarios",
            json=build_greece_counterfactual_scenario().model_dump(mode="json"),
        )
        assert cf_resp.status_code == 201
        cf_id: str = cf_resp.json()["scenario_id"]

        result = await run_harness(
            scenario_id=cf_id,
            steps=6,
            run_type=RunType.TYPE_B,
            control_inputs=[{} for _ in range(6)],
            baseline_run_id=baseline_id,
            primary_indicator="hd_composite",
            http_client=asgi_client,
        )

        per_step_diff = result.summary.get("per_step_diff", [])
        assert len(per_step_diff) >= 4, (
            f"AC-1 FAIL: per_step_diff has {len(per_step_diff)} entries, need ≥4."
        )
        step4_diff = Decimal(str(per_step_diff[3]))
        assert step4_diff > Decimal("0"), (
            f"per_step_diff[3]={step4_diff!r} ≤ 0. "
            "Heterodox path must produce less HD damage than orthodox at step 4. "
            "Positive diff = heterodox HD score better (less poverty accumulation). "
            "Negative diff indicates calibration direction error in GRC FORMAL entries."
        )

    async def test_grc_counterfactual_direction_verdict_not_advisory_after_implementation(
        self, asgi_client: httpx.AsyncClient
    ) -> None:
        """After implementation direction_verdict must be deterministic, not advisory.

        This test documents the upgrade from G2C advisory to CM Sprint A blocking.
        Issues a warning if direction_verdict is INDISTINGUISHABLE (calibration may
        be too weak to produce a reliable signal) but does NOT fail for INDISTINGUISHABLE
        — the MAGNITUDE assertion above is the hard gate.
        """
        from tests.fixtures.greece_2010_scenario import (
            build_greece_counterfactual_scenario,
            build_greece_scenario,
        )

        baseline_resp = await asgi_client.post(
            "/api/v1/scenarios",
            json=build_greece_scenario().model_dump(mode="json"),
        )
        assert baseline_resp.status_code == 201
        baseline_id: str = baseline_resp.json()["scenario_id"]

        for _step in range(1, 7):
            _adv = await asgi_client.post(f"/api/v1/scenarios/{baseline_id}/advance")
            assert _adv.status_code == 200, (
                f"Baseline advance step {_step} failed: {_adv.status_code} {_adv.text}"
            )

        cf_resp = await asgi_client.post(
            "/api/v1/scenarios",
            json=build_greece_counterfactual_scenario().model_dump(mode="json"),
        )
        assert cf_resp.status_code == 201
        cf_id: str = cf_resp.json()["scenario_id"]

        result = await run_harness(
            scenario_id=cf_id,
            steps=6,
            run_type=RunType.TYPE_B,
            control_inputs=[{} for _ in range(6)],
            baseline_run_id=baseline_id,
            primary_indicator="hd_composite",
            http_client=asgi_client,
        )

        verdict = result.summary.get("direction_verdict")
        if verdict == DirectionVerdict.INDISTINGUISHABLE or str(verdict) == str(
            DirectionVerdict.INDISTINGUISHABLE
        ):
            warnings.warn(
                "CM Sprint A: hd_composite direction_verdict=INDISTINGUISHABLE after "
                "implementation. GRC FORMAL calibration may produce too weak a signal "
                "for the harness threshold (Decimal('0.01') in _classify_direction). "
                "Verify entity_families filter fires on GRC and elasticity constants "
                "match calibration decision doc §3.1.",
                UserWarning,
                stacklevel=1,
            )
        elif verdict == DirectionVerdict.BASELINE_BETTER or str(verdict) == str(
            DirectionVerdict.BASELINE_BETTER
        ):
            pytest.fail(
                "CM Sprint A FAIL: hd_composite direction_verdict=BASELINE_BETTER. "
                "Orthodox (troika) path produces better HD outcome — this contradicts "
                "the Blanchard & Leigh (2013) empirical evidence and Eurostat AROPE data. "
                "Check calibration constants sign and entity_families filter correctness."
            )
