"""Greece 2010–2012 IMF Program — scenario configuration fixture.

Defines the scenario configuration for the Greece 2010–2012 backtesting run
as a Python object. This fixture is consumed by the backtesting test in
tests/backtesting/test_greece_2010_2012.py.

Design follows ADR-004 Decision 3. The ControlInput sequence approximates
the documented historical program:
  - Step 1 (2010): IMF program acceptance + fiscal spending cuts
  - Step 2 (2011): Second austerity package + deficit target

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
    """Build the Greece 2010–2012 backtesting scenario configuration.

    Returns a ScenarioCreateRequest ready to POST to /api/v1/scenarios.
    The scenario runs 3 steps (annual: 2010→2011→2012→2013 projection window)
    starting from Greece's 2010 initial economic conditions.

    Scheduled inputs represent the IMF/EU program conditionality:
      Step 1: IMF program acceptance (May 2010) + primary spending cuts
      Step 2: Second austerity package (June 2011) + deficit target

    Initial state attributes — Issue #149 (WDI human development seed):
      gdp_growth              — IMF WEO April 2010, -5.4% outturn
      unemployment_rate       — Eurostat LFS Q1 2010, 12.7%
      health_expenditure_pct_gdp — World Bank WDI 2010, 9.5% of GDP
      net_enrollment_secondary   — World Bank WDI 2010, 99.1%

    References: ADR-004 Decision 3; Issue #112; Issue #149.
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

    return ScenarioCreateRequest(
        name="Greece 2010-2012 IMF Program Backtesting Fixture",
        description=(
            "Backtesting fixture for ADR-004 Decision 3, Issue #112. "
            "Reproduces the Greece 2010–2012 sovereign debt crisis and IMF/EU "
            "program conditionality to validate DIRECTION_ONLY fidelity thresholds. "
            "Initial state: IMF WEO April 2010 + Eurostat LFS 2010 + WDI 2010."
        ),
        configuration=ScenarioConfigSchema(
            entities=["GRC"],
            n_steps=3,
            timestep_label="annual",
            initial_attributes={
                "GRC": {
                    "gdp_growth": initial_gdp_growth,
                    "unemployment_rate": initial_unemployment_rate,
                    "health_expenditure_pct_gdp": initial_health_expenditure,
                    "net_enrollment_secondary": initial_net_enrollment_secondary,
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
        ],
    )
