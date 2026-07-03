"""Senegal 2014–2019 commodity shock — backtesting calibration fixture (#1541).

Defines the scenario configuration for the Senegal 2014–2019 Type A backtesting
run. This fixture is the primary SEN calibration input for ADR-007 Bayesian
posterior layer (G3, #1543). Chief Methodologist sign-off on fidelity tier
classification is required before this fixture merges to sprint/m19-g2.

Scenario narrative:
  Step 1 (2014): Stable initial conditions — near 4-year growth high (4.7%);
    CFA franc peg provides monetary anchor; phosphate and groundnut export base
    underpins external balance; first Eurobond ($500M, June 2014) successful.
  Step 2 (2015): Global commodity price decline hits phosphate and groundnut
    export revenues; fiscal revenue shortfall begins; growth slows.
  Step 3 (2016): Trough year — combined commodity, fiscal adjustment, and
    donor-conditionality pressures; growth dips to ~6.5% (PSE uplift partially
    offsets). Financial composite at its weakest relative to 2014.
  Step 4 (2017): Recovery onset — PSE infrastructure projects gain traction;
    fiscal adjustment moderates; oil exploration signals positive.
  Step 5 (2018): Continued recovery; reserves rebuild; sovereign spreads narrow.
  Step 6 (2019): Stabilization — growth re-accelerates toward 5%+ trend.

Initial state data sources (2014 vintage):
  IMF_WEO_APR2015   — IMF World Economic Outlook April 2015, Senegal data:
                       gdp_growth (4.7% — 2014 outturn)
  WDI_SEN_2014      — World Bank World Development Indicators 2014 vintage:
                       unemployment_rate, health_expenditure_pct_gdp,
                       net_enrollment_secondary, poverty_headcount_ratio
  IMF_IFS_SEN_2014  — IMF International Financial Statistics 2014:
                       reserve_coverage_months (~3.2 months BCEAO pooled)
  UNCTAD_FDI_SEN_2014 — UNCTAD World Investment Report 2014: fdi_stock_pct_gdp
  SP_SEN_2014       — S&P sovereign credit rating Senegal 2014: B+ (~33/100)

ADR authority: N/A — fixture is data over the existing harness API (intent doc).
Intent document: docs/process/intents/M19-G2B-2026-07-02-sen-backtesting-fixture.md
Sprint entry: docs/process/sprint-plans/m19-g2b-sprint-entry.md

CM consultation activation:
  Chief Methodologist: VALIDATE — SEN 2014–2019 Type A backtesting fixture
  fidelity tier; required before this fixture merges to sprint/m19-g2.

build_sen_scenario() returns a _SenCalibrationRequest — a Pydantic subclass of
ScenarioCreateRequest that adds entity_id and is_pre_calibration metadata fields.
The API endpoint ignores these extra fields (Pydantic v2 default extra="ignore").
"""
from __future__ import annotations

from datetime import date
from decimal import Decimal

from app.schemas import (
    CommodityShockConfig,
    FocalCohortConfig,
    QuantitySchema,
    ScenarioConfigSchema,
    ScenarioCreateRequest,
    ScheduledInputSchema,
)


class _SenCalibrationRequest(ScenarioCreateRequest):
    """ScenarioCreateRequest with G2B backtesting fixture metadata for SEN.

    Adds entity_id and is_pre_calibration as top-level fields so test assertions
    can read them directly. model_dump(mode='json') includes these fields; the
    API endpoint silently ignores unknown fields (Pydantic v2 extra='ignore').
    """

    entity_id: str
    is_pre_calibration: bool


def build_sen_scenario() -> _SenCalibrationRequest:
    """Build the Senegal 2014–2019 commodity shock backtesting fixture.

    Returns a _SenCalibrationRequest ready to POST to /api/v1/scenarios.
    The scenario runs 6 annual steps starting from Senegal's 2014 baseline:
      Step 1 (2014): Pre-shock stable baseline (4.7% GDP growth, CFA peg stable)
      Step 2 (2015): Commodity shock onset (phosphate + groundnut price decline)
      Step 3 (2016): Fiscal trough (revenue shortfall + adjustment peak)
      Step 4 (2017): Recovery onset (PSE infrastructure + oil signals)
      Step 5 (2018): Recovery continuation
      Step 6 (2019): Stabilization (growth re-accelerates)

    Fidelity target: DIRECTION_ONLY minimum; Chief Methodologist advises on
    MAGNITUDE_MATCH eligibility based on output (pre-merge review required).

    Data sources: IMF WEO April 2015 (gdp_growth), WDI 2014 (HD indicators),
    IMF IFS 2014 (reserves), UNCTAD 2014 (FDI), S&P 2014 (rating).
    """
    # IMF WEO April 2015, Senegal 2014 outturn: 4.7% GDP growth.
    # Strong year driven by construction + services; agriculture modest.
    initial_gdp_growth = QuantitySchema(
        value="0.047",
        unit="ratio",
        variable_type="ratio",
        confidence_tier=2,
        observation_date=date(2015, 4, 1),
        source_registry_id="IMF_WEO_APR2015",
        measurement_framework="financial",
    )

    # WDI 2014 vintage (ILO-modelled national estimate) — ~10% national rate.
    # Senegal's formal labour market is thin; informal sector dominates.
    # Confidence tier 3: ILO model inference from partial coverage.
    initial_unemployment_rate = QuantitySchema(
        value="0.100",
        unit="ratio",
        variable_type="ratio",
        confidence_tier=3,
        observation_date=date(2015, 1, 1),
        source_registry_id="WDI_SEN_2014",
        measurement_framework="human_development",
    )

    # WDI 2014 vintage — Senegal health expenditure ~4.7% of GDP.
    # Includes government and private spending; WHO/WB joint estimate.
    initial_health_expenditure = QuantitySchema(
        value="0.047",
        unit="ratio",
        variable_type="ratio",
        confidence_tier=2,
        observation_date=date(2015, 1, 1),
        source_registry_id="WDI_SEN_2014",
        measurement_framework="human_development",
    )

    # WDI 2014 vintage — Senegal secondary net enrollment ~40%.
    # Sub-Saharan Africa regional context: below WAEMU median at this period.
    # Confidence tier 2: official national education survey, WB harmonised.
    initial_net_enrollment_secondary = QuantitySchema(
        value="0.400",
        unit="ratio",
        variable_type="ratio",
        confidence_tier=2,
        observation_date=date(2015, 1, 1),
        source_registry_id="WDI_SEN_2014",
        measurement_framework="human_development",
    )

    # IMF IFS 2014 / BCEAO Annual Report 2014 — WAEMU pooled reserves distributed
    # to Senegal's import base: approximately 3.2 months. WAEMU member states
    # pool reserves at the regional central bank (BCEAO); Senegal's share
    # reflects its import weight within the zone.
    # Confidence tier 3: regional pooling makes per-country attribution synthetic.
    initial_reserve_coverage_months = QuantitySchema(
        value="3.2",
        unit="months",
        variable_type="ratio",
        confidence_tier=3,
        observation_date=date(2015, 1, 1),
        source_registry_id="IMF_IFS_SEN_2014",
        measurement_framework="financial",
    )

    # IMF Article IV Senegal 2014 — long-run potential growth estimate ~4.0%.
    # Structural factors: agriculture base (40% employment), services growth,
    # thin manufacturing base. Pre-PSE: potential below realised growth rate.
    initial_trend_growth = QuantitySchema(
        value="0.040",
        unit="ratio",
        variable_type="ratio",
        confidence_tier=3,
        observation_date=date(2014, 1, 1),
        source_registry_id="IMF_ARTIVSEN2014",
        measurement_framework="financial",
    )

    # EMBI spread Senegal 2014 — first Eurobond (June 2014, $500M, 6.25%, 10Y).
    # US 10Y Treasury mid-2014 ~2.50–2.75%; SEN spread ~350bps → premium ~0.035.
    # Reflects frontier market access; CFA anchor provides partial creditor comfort.
    # Confidence tier 2: observable secondary market spread; mid-year observation.
    initial_sovereign_risk_premium = QuantitySchema(
        value="0.035",
        unit="ratio",
        variable_type="ratio",
        attribute_type="rate",
        confidence_tier=2,
        observation_date=date(2014, 6, 1),
        source_registry_id="EMBI_SEN_2014",
        measurement_framework="financial",
    )

    # UNCTAD World Investment Report 2014 — Senegal inward FDI stock / GDP.
    # Driven by telecoms, infrastructure, and early mining exploration (~22%).
    # Confidence tier 2: official multilateral statistics, annual vintage.
    initial_fdi_stock_pct_gdp = QuantitySchema(
        value="0.220",
        unit="ratio",
        variable_type="stock",
        attribute_type="stock",
        confidence_tier=2,
        observation_date=date(2014, 1, 1),
        source_registry_id="UNCTAD_FDI_SEN_2014",
        measurement_framework="financial",
    )

    # IMF BOP Statistics 2014 — Senegal net portfolio investment / GDP.
    # First Eurobond attracted moderate portfolio inflows; net positive in 2014.
    # Confidence tier 3: portfolio flows thin for frontier markets; estimate.
    initial_portfolio_flow_velocity = QuantitySchema(
        value="0.004",
        unit="ratio",
        variable_type="ratio",
        attribute_type="flow",
        confidence_tier=3,
        observation_date=date(2014, 1, 1),
        source_registry_id="IMF_BOP_SEN_2014",
        measurement_framework="financial",
    )

    # S&P sovereign credit rating Senegal 2014: B+.
    # Mapped to 0–100 index using 21-notch linear scale (AAA=100, D=0).
    # Reference: Argentina BB = 38 (argentina_2001_2002_scenario.py, pre-crisis);
    # B+ is one notch below BB → B+ ≈ 33. Confidence tier 1: direct observation.
    initial_credit_rating_score = QuantitySchema(
        value="33.0",
        unit="index_0_100",
        variable_type="stock",
        attribute_type="structural_index",
        confidence_tier=1,
        observation_date=date(2014, 1, 1),
        source_registry_id="SP_SEN_2014",
        measurement_framework="financial",
    )

    # WDI 2011 / PovcalNet — Senegal national poverty line headcount ratio ~46.8%.
    # Most recent available estimate closest to 2014; 2013/2014 survey data
    # not yet published at 2014 vintage. Confidence tier 3: non-vintage year;
    # interpolated from 2011 survey against GDP path.
    initial_poverty_headcount_ratio = QuantitySchema(
        value="0.468",
        unit="ratio",
        variable_type="ratio",
        confidence_tier=3,
        observation_date=date(2012, 1, 1),
        source_registry_id="WDI_SEN_2014",
        measurement_framework="human_development",
    )

    return _SenCalibrationRequest(
        entity_id="SEN",
        is_pre_calibration=True,
        name="Senegal 2014-2019 Commodity Shock Backtesting Fixture",
        description=(
            "G2B backtesting calibration fixture — Issue #1541. "
            "Reproduces Senegal's 2014–2019 commodity price shock episode "
            "(phosphate + groundnut export revenue decline, 2015–2016) to "
            "validate DIRECTION_ONLY fidelity on a moderate Sub-Saharan Africa "
            "stress case. CFA franc peg insulates monetary channel; fiscal "
            "transmission via revenue shortfall is the primary pathway. "
            "Chief Methodologist sign-off on fidelity tier required before merge. "
            "Initial state: IMF WEO April 2015 + WDI 2014 + IMF IFS 2014 "
            "+ UNCTAD 2014 + S&P B+ (2014) + EMBI spread June 2014."
        ),
        configuration=ScenarioConfigSchema(
            entities=["SEN"],
            n_steps=6,
            timestep_label="annual",
            start_date=date(2014, 1, 1),
            step_metadata={
                "1": {"significance": "SIGNIFICANT", "label": "Pre-shock stable baseline"},
                "2": {"significance": "SIGNIFICANT", "label": "Commodity shock onset"},
                "3": {"significance": "SIGNIFICANT", "label": "Fiscal trough / adjustment"},
                "4": {"significance": "SIGNIFICANT", "label": "Recovery onset / PSE"},
                "5": {"significance": "ROUTINE", "label": "Recovery continuation"},
                "6": {"significance": "ROUTINE", "label": "Stabilization"},
            },
            commodity_price_shocks=[
                # Phosphate price decline 2015–2016: global oversupply, falling
                # Chinese demand. SEN phosphate exports ~15% of goods exports.
                # commodity_import_dependency_other set in initial_attributes.
                CommodityShockConfig(
                    commodity_category="other",
                    magnitude=Decimal("-0.12"),
                    start_step=2,
                    duration_steps=2,
                ),
                # Groundnut price decline 2015–2016: broad agricultural soft
                # commodity correction. Groundnut oil + cake ~10% of goods exports.
                CommodityShockConfig(
                    commodity_category="food",
                    magnitude=Decimal("-0.08"),
                    start_step=2,
                    duration_steps=2,
                ),
            ],
            # Rural bottom-quintile focal cohort — optional for SEN, included
            # for methodological completeness (AC-7 is ZMB-only in G2B).
            monitored_focal_cohorts=[
                FocalCohortConfig(
                    indicator_key="poverty_headcount_ratio",
                    floor_value=0.40,
                    floor_label="SEN rural bottom-quintile recovery floor",
                    framework="human_development",
                    recovery_horizon_years=10,
                ),
            ],
            initial_attributes={
                "SEN": {
                    "gdp_growth": initial_gdp_growth,
                    "unemployment_rate": initial_unemployment_rate,
                    "health_expenditure_pct_gdp": initial_health_expenditure,
                    "net_enrollment_secondary": initial_net_enrollment_secondary,
                    "reserve_coverage_months": initial_reserve_coverage_months,
                    "trend_growth": initial_trend_growth,
                    "sovereign_risk_premium": initial_sovereign_risk_premium,
                    "fdi_stock_pct_gdp": initial_fdi_stock_pct_gdp,
                    "portfolio_flow_velocity": initial_portfolio_flow_velocity,
                    "credit_rating_score": initial_credit_rating_score,
                    "poverty_headcount_ratio": initial_poverty_headcount_ratio,
                    # Export commodity dependency coefficients — required for
                    # ExternalSectorModule commodity_price_shocks transmission.
                    # Senegal exports phosphate (other) and groundnuts (food);
                    # import dependency coefficients are set here as synthetic
                    # export-side proxies per DATA_STANDARDS.md §Confidence Tier 3.
                    "commodity_import_dependency_other": QuantitySchema(
                        value="0.15",
                        unit="ratio",
                        variable_type="ratio",
                        confidence_tier=3,
                        observation_date=date(2014, 1, 1),
                        source_registry_id="WDI_SEN_2014",
                        measurement_framework="financial",
                    ),
                    "commodity_import_dependency_food": QuantitySchema(
                        value="0.10",
                        unit="ratio",
                        variable_type="ratio",
                        confidence_tier=3,
                        observation_date=date(2014, 1, 1),
                        source_registry_id="WDI_SEN_2014",
                        measurement_framework="financial",
                    ),
                },
            },
        ),
        scheduled_inputs=[
            # Step 2 (2015): Fiscal revenue shortfall — commodity export decline
            # reduces government receipts. Spending adjustment announced.
            ScheduledInputSchema(
                step=2,
                input_type="FiscalPolicyInput",
                input_data={
                    "instrument": "spending_change",
                    "target_entity": "SEN",
                    "sector": "government",
                    "value": "-0.020",
                    "duration_years": 1,
                },
            ),
            # Step 2 (2015): GDP growth slowdown from commodity sector contraction.
            ScheduledInputSchema(
                step=2,
                input_type="gdp_growth_change",
                input_data={
                    "target_entity": "SEN",
                    "magnitude": "-0.010",
                },
            ),
            # Step 3 (2016): Fiscal trough — peak adjustment pressure.
            # Government spending cuts deepen as donor conditionality tightens.
            ScheduledInputSchema(
                step=3,
                input_type="FiscalPolicyInput",
                input_data={
                    "instrument": "spending_change",
                    "target_entity": "SEN",
                    "sector": "government",
                    "value": "-0.018",
                    "duration_years": 1,
                },
            ),
            # Step 3 (2016): Continued growth drag — second commodity shock year.
            ScheduledInputSchema(
                step=3,
                input_type="gdp_growth_change",
                input_data={
                    "target_entity": "SEN",
                    "magnitude": "-0.008",
                },
            ),
            # Step 4 (2017): Recovery onset — PSE infrastructure projects active.
            # Adjustment eases; fiscal position improving as revenues recover.
            ScheduledInputSchema(
                step=4,
                input_type="FiscalPolicyInput",
                input_data={
                    "instrument": "spending_change",
                    "target_entity": "SEN",
                    "sector": "government",
                    "value": "-0.008",
                    "duration_years": 1,
                },
            ),
            # Step 5 (2018): PSE traction — institutional reform programme active.
            ScheduledInputSchema(
                step=5,
                input_type="StructuralPolicyInput",
                input_data={
                    "instrument": "institutional_reform",
                    "target_entity": "SEN",
                    "affected_sector": "public_infrastructure",
                    "implementation_years": 3,
                },
            ),
        ],
    )
