"""Greece 2010–2015 IMF Program — scenario configuration fixture.

Defines the scenario configuration for the Greece 2010–2015 backtesting run
as a Python object. This fixture is consumed by the backtesting test in
tests/backtesting/test_greece_2010_2012.py.

Also exports build_greece_demo_scenario() for the M8 end-of-milestone demo
(Issue #269), which enables EcologicalModule via modules_config.

Design follows ADR-004 Decision 3. The ControlInput sequence approximates
the documented historical program:
  - Step 1 (2010): IMF program acceptance + fiscal spending cuts
  - Step 2 (2011): Second austerity package + deficit target
  - Step 3 (2012): Continued fiscal consolidation (third memorandum preparation)
  - Step 4 (2013): Primary surplus conditionality + fiscal adjustment
  - Step 5 (2014): Privatisation programme (ESM conditionality)
  - Step 6 (2015): Capital controls imposed 26 June 2015

ControlInput types are restricted to those implemented in
WebScenarioRunner._deserialize_control_input(). Instrument enum values must
match the ControlInput dataclass definitions in orchestration/inputs.py.

All Quantity values are strings per DATA_STANDARDS.md float prohibition.

Initial state sources — Issue #149:
  IMF_WEO_APR2010   — IMF World Economic Outlook April 2010, gdp_growth
  EUROSTAT_LFS_2010 — Eurostat Labour Force Survey Q1 2010, unemployment_rate
  WDI_2010          — World Bank World Development Indicators 2010 vintage
                      (published Dec 2011), health_expenditure_pct_gdp and
                      net_enrollment_secondary
"""
from __future__ import annotations

from datetime import date

from app.schemas import (
    QuantitySchema,
    ScenarioConfigSchema,
    ScenarioCreateRequest,
    ScheduledInputSchema,
)


def build_greece_scenario() -> ScenarioCreateRequest:
    """Build the Greece 2010–2015 backtesting scenario configuration.

    Returns a ScenarioCreateRequest ready to POST to /api/v1/scenarios.
    The scenario runs 6 steps (annual: 2010→2011→2012→2013→2014→2015→2016
    projection window) starting from Greece's 2010 initial economic conditions.

    Scheduled inputs represent the IMF/EU program conditionality:
      Step 1: IMF program acceptance (May 2010) + primary spending cuts
      Step 2: Second austerity package (June 2011) + deficit target
      Step 3: Third memorandum fiscal consolidation (2012)
      Step 4: Primary surplus target + fiscal adjustment (2013)
      Step 5: ESM privatisation programme (2014)
      Step 6: Capital controls (26 June 2015)

    Initial state attributes — Issue #149 (WDI human development seed):
      gdp_growth              — IMF WEO April 2010, -5.4% outturn
      unemployment_rate       — Eurostat LFS Q1 2010, 12.7%
      health_expenditure_pct_gdp — World Bank WDI 2010, 9.5% of GDP
      net_enrollment_secondary   — World Bank WDI 2010, 99.1%

    References: ADR-004 Decision 3; Issue #112; Issue #149; Issue #316.
    """
    initial_gdp_growth = QuantitySchema(
        value="-0.054",
        unit="ratio",
        variable_type="ratio",
        confidence_tier=3,
        observation_date=date(2010, 4, 1),
        source_registry_id="IMF_WEO_APR2010",
        measurement_framework="financial",
    )

    # Eurostat LFS Q1 2010 — 12.7%; confidence_tier=2 (calibrated from
    # official national statistics). vintage_date = Q2 2010 release.
    initial_unemployment_rate = QuantitySchema(
        value="0.127",
        unit="ratio",
        variable_type="ratio",
        confidence_tier=2,
        observation_date=date(2010, 7, 1),
        source_registry_id="EUROSTAT_LFS_2010",
        measurement_framework="human_development",
    )

    # World Bank WDI 2010 (published Dec 2011) — 9.5% of GDP
    initial_health_expenditure = QuantitySchema(
        value="0.095",
        unit="ratio",
        variable_type="ratio",
        confidence_tier=2,
        observation_date=date(2011, 12, 1),
        source_registry_id="WDI_2010",
        measurement_framework="human_development",
    )

    # World Bank WDI 2010 (published Dec 2011) — 99.1% net enrollment
    initial_net_enrollment_secondary = QuantitySchema(
        value="0.991",
        unit="ratio",
        variable_type="ratio",
        confidence_tier=2,
        observation_date=date(2011, 12, 1),
        source_registry_id="WDI_2010",
        measurement_framework="human_development",
    )

    # IMF Country Report 10/110 (May 2010) — Greece's effective import coverage
    # at programme entry was approximately 2.0 months (central government
    # liquidity position, pre-first-disbursement).  Below the MDA-FIN-RESERVES
    # CRITICAL floor (2.5 months), producing a persistent CRITICAL alert from
    # step 1 onward throughout the programme window.
    initial_reserve_coverage_months = QuantitySchema(
        value="2.0",
        unit="months",
        variable_type="ratio",
        confidence_tier=2,
        observation_date=date(2010, 5, 1),
        source_registry_id="IMF_CR10_110",
        measurement_framework="financial",
    )

    return ScenarioCreateRequest(
        name="Greece 2010-2015 IMF Program Backtesting Fixture",
        description=(
            "Backtesting fixture for ADR-004 Decision 3, Issue #112, Issue #316. "
            "Reproduces the Greece 2010–2015 sovereign debt crisis, IMF/EU program "
            "conditionality, and capital controls episode to validate DIRECTION_ONLY "
            "fidelity thresholds across the full stabilization period. "
            "Initial state: IMF WEO April 2010 + Eurostat LFS 2010 + WDI 2010 "
            "+ IMF CR10/110 (reserve_coverage_months)."
        ),
        configuration=ScenarioConfigSchema(
            entities=["GRC"],
            n_steps=6,
            timestep_label="annual",
            start_date=date(2010, 1, 1),
            initial_attributes={
                "GRC": {
                    "gdp_growth": initial_gdp_growth,
                    "unemployment_rate": initial_unemployment_rate,
                    "health_expenditure_pct_gdp": initial_health_expenditure,
                    "net_enrollment_secondary": initial_net_enrollment_secondary,
                    "reserve_coverage_months": initial_reserve_coverage_months,
                },
            },
        ),
        scheduled_inputs=[
            # Step 1 (2010): IMF program acceptance — €110bn ESM/IMF program, May 2010
            ScheduledInputSchema(
                step=1,
                input_type="EmergencyPolicyInput",
                input_data={
                    "instrument": "imf_program_acceptance",
                    "target_entity": "GRC",
                    "expected_duration": 3,
                    "program_size_gdp_ratio": "0.48",
                },
            ),
            # Step 1 (2010): Fiscal spending cuts — 2010 Memorandum primary cuts
            ScheduledInputSchema(
                step=1,
                input_type="FiscalPolicyInput",
                input_data={
                    "instrument": "spending_change",
                    "target_entity": "GRC",
                    "sector": "government",
                    "value": "-0.08",
                    "duration_years": 1,
                },
            ),
            # Step 2 (2011): Second austerity package — June 2011 Medium-Term Fiscal Strategy
            ScheduledInputSchema(
                step=2,
                input_type="FiscalPolicyInput",
                input_data={
                    "instrument": "spending_change",
                    "target_entity": "GRC",
                    "sector": "government",
                    "value": "-0.05",
                    "duration_years": 1,
                },
            ),
            # Step 2 (2011): Deficit target — Medium-Term Fiscal Strategy 2011–2015
            ScheduledInputSchema(
                step=2,
                input_type="FiscalPolicyInput",
                input_data={
                    "instrument": "deficit_target",
                    "target_entity": "GRC",
                    "sector": "",
                    "value": "-0.03",
                    "duration_years": 4,
                },
            ),
            # Step 3 (2012): Third memorandum fiscal consolidation
            ScheduledInputSchema(
                step=3,
                input_type="FiscalPolicyInput",
                input_data={
                    "instrument": "spending_change",
                    "target_entity": "GRC",
                    "sector": "government",
                    "value": "-0.04",
                    "duration_years": 1,
                },
            ),
            # Step 4 (2013): Primary surplus conditionality — +1.5% GDP achieved
            ScheduledInputSchema(
                step=4,
                input_type="FiscalPolicyInput",
                input_data={
                    "instrument": "spending_change",
                    "target_entity": "GRC",
                    "sector": "government",
                    "value": "-0.02",
                    "duration_years": 1,
                },
            ),
            ScheduledInputSchema(
                step=4,
                input_type="FiscalPolicyInput",
                input_data={
                    "instrument": "deficit_target",
                    "target_entity": "GRC",
                    "sector": "",
                    "value": "0.015",
                    "duration_years": 2,
                },
            ),
            # Step 5 (2014): ESM privatisation programme conditionality
            ScheduledInputSchema(
                step=5,
                input_type="StructuralPolicyInput",
                input_data={
                    "instrument": "privatization",
                    "target_entity": "GRC",
                    "affected_sector": "public_assets",
                    "implementation_years": 3,
                },
            ),
            # Step 6 (2015): Capital controls — imposed 26 June 2015 by Greek government
            ScheduledInputSchema(
                step=6,
                input_type="EmergencyPolicyInput",
                input_data={
                    "instrument": "capital_controls",
                    "target_entity": "GRC",
                    "expected_duration": 2,
                },
            ),
        ],
    )


def build_greece_demo_scenario() -> ScenarioCreateRequest:
    """Build the Greece 2010–2015 M8 demo scenario with EcologicalModule enabled.

    Extends build_greece_scenario() with:
      - modules_config enabling EcologicalModule (planetary boundary proximity)
      - co2_concentration_ppm initial seed (388.0 ppm — Mauna Loa 2010 annual mean)

    The CO2 seed is required so the EcologicalModule stock path can compute
    boundary proximity at step 1 (before any GDP-driven delta arrives via the
    one-step-lag delta path). Without it, co2_concentration_ppm is absent from
    entity.attributes at step 1 and the stock path skips with [SIM-INTEGRITY]
    WARNING. Source: NOAA_MLO_2010 (Mauna Loa Observatory, 388.0 ppm annual mean).

    The ecological composite score is the only non-null composite in this
    single-entity scenario — financial and human_development composites are null
    because percentile rank requires ≥2 entities (single_entity_warning=True,
    Issue #193, ADR-005 Decision M8-2). Governance composite is null pending M9.

    References: Issue #269; ADR-005 Amendment 3 Decisions M8-2/M8-3/M8-6.
    """
    base = build_greece_scenario()

    # NOAA Mauna Loa Observatory 2010 annual mean: 388.0 ppm (confidence_tier=1).
    # Provides the initial stock value for the EcologicalModule stock path so that
    # planetary_boundary_co2_proximity is non-null at step 1.
    initial_co2_concentration = QuantitySchema(
        value="388.0",
        unit="ppm",
        variable_type="stock",
        confidence_tier=1,
        observation_date=date(2010, 1, 1),
        source_registry_id="NOAA_MLO_2010",
        measurement_framework="ecological",
    )

    updated_grc_attrs = {
        **base.configuration.initial_attributes.get("GRC", {}),
        "co2_concentration_ppm": initial_co2_concentration,
    }
    demo_config = base.configuration.model_copy(
        update={
            "modules_config": {"ecological": {"enabled": True}},
            "initial_attributes": {"GRC": updated_grc_attrs},
        }
    )
    return base.model_copy(update={
        "name": "Greece 2010-2015 M8 Demo — Multi-Framework Measurement",
        "description": (
            "M8 end-of-milestone demo scenario (Issue #269). "
            "EcologicalModule enabled — produces planetary boundary "
            "proximity scores at all six steps. Financial and human_development "
            "composite scores are null in this single-entity scenario "
            "(percentile rank requires ≥2 entities, Issue #193). "
            "Governance composite is null pending Milestone 9 promotion criteria. "
            "Initial state: IMF WEO April 2010 + Eurostat LFS 2010 + WDI 2010 "
            "+ IMF CR10/110 (reserve_coverage_months) + NOAA MLO 2010 (co2_concentration_ppm)."
        ),
        "configuration": demo_config,
    })
