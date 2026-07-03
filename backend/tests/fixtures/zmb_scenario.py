"""Zambia 2014–2019 copper price crash — backtesting calibration fixture (#1542).

Defines the scenario configuration for the Zambia 2014–2019 Type A backtesting
run. ZMB is the primary Demo 8 calibration country. The fidelity tier produced
here grounds the empirical credibility of CI intervals presented at Demo 8 Act 2
("+342K cohort effect" with sourcing to IMF restructuring table).

Chief Methodologist sign-off on fidelity tier is required before this fixture
merges to sprint/m19-g2. A MAGNITUDE_MATCH tier significantly strengthens
the Bayesian posterior for Demo 8; DIRECTION_ONLY is the minimum acceptable.

Also delivers: focal_cohort_poverty_headcount in AdvanceResponse via
_focal_cohort_phc() helper added to app/api/scenarios.py (#1541/#1542 enabler).
The G2A harness already reads this field from the advance response; this PR
populates it for scenarios with monitored_focal_cohorts configured.

Scenario narrative:
  Step 1 (2014): Near-peak copper prices; first Eurobond ($750M, 5.375%);
    fiscal deficit manageable (~3.5% GDP); kwacha stable.
  Step 2 (2015): Copper crash accelerates (−26% annual avg); kwacha depreciates
    ~45%; reserve drawdown begins; fiscal revenue shortfall materialises.
  Step 3 (2016): Fiscal deficit peaks (>7% GDP); IMF Staff Monitored Program
    discussions begin; power shortages compound copper shock; trough year.
  Step 4 (2017): $1B Eurobond issued; copper partial recovery; deficit reduction
    attempt; external financing buys time.
  Step 5 (2018): Debt service pressure rising; IMF Article IV warns on debt
    trajectory; growth improving but fiscal position fragile.
  Step 6 (2019): Pre-default trajectory established; spreads widening toward
    2020 restructuring; IMF programme stalls.

Initial state data sources (2014 vintage):
  IMF_WEO_APR2015   — IMF WEO April 2015, Zambia data:
                       gdp_growth (4.7% — 2014 outturn)
  WDI_ZMB_2014      — WDI 2014 vintage: unemployment_rate, health expenditure,
                       net_enrollment_secondary, poverty_headcount_ratio
  IMF_IFS_ZMB_2014  — IMF IFS 2014: reserve_coverage_months (~3.0 months)
  WB_IDS_ZMB_2014   — World Bank IDS 2014: external debt composition
  UNCTAD_FDI_ZMB_2014 — UNCTAD 2014: fdi_stock_pct_gdp (~45% GDP)
  SP_ZMB_2014       — Moody's B1 / S&P B+ (2014): credit_rating_score 30.0

Intent document: docs/process/intents/M19-G2B-2026-07-02-zmb-backtesting-fixture.md
Sprint entry: docs/process/sprint-plans/m19-g2b-sprint-entry.md
CM activation: Chief Methodologist: VALIDATE — ZMB 2014–2019 Type A backtesting
  fixture fidelity tier; Demo 8 Act 2 calibration credibility depends on this.

build_zmb_scenario() returns a _ZmbCalibrationRequest — a Pydantic subclass of
ScenarioCreateRequest that adds entity_id, is_pre_calibration, and a
monitored_focal_cohorts @property delegating to configuration.monitored_focal_cohorts.
"""
from __future__ import annotations

from datetime import date

from app.schemas import (
    FocalCohortConfig,
    QuantitySchema,
    ScenarioConfigSchema,
    ScenarioCreateRequest,
    ScheduledInputSchema,
)


class _ZmbCalibrationRequest(ScenarioCreateRequest):
    """ScenarioCreateRequest with G2B backtesting fixture metadata for ZMB.

    Adds entity_id and is_pre_calibration as top-level Pydantic fields.
    monitored_focal_cohorts is exposed as a @property delegating to
    configuration.monitored_focal_cohorts — visible to getattr() but excluded
    from model_dump() to avoid duplicate fields in the API POST body.
    """

    entity_id: str
    is_pre_calibration: bool

    @property
    def monitored_focal_cohorts(self) -> list[FocalCohortConfig]:
        return self.configuration.monitored_focal_cohorts


def build_zmb_scenario() -> _ZmbCalibrationRequest:
    """Build the Zambia 2014–2019 copper price crash backtesting fixture.

    Returns a _ZmbCalibrationRequest ready to POST to /api/v1/scenarios.
    The scenario runs 6 annual steps covering Zambia's full commodity shock arc:
      Step 1 (2014): Near-peak copper baseline (4.7% growth, Eurobond fresh)
      Step 2 (2015): Copper crash onset + kwacha -45% + reserve drawdown
      Step 3 (2016): Fiscal deficit >7% GDP + IMF SMP discussions
      Step 4 (2017): $1B Eurobond rescue financing
      Step 5 (2018): Debt service pressure escalates
      Step 6 (2019): Pre-default trajectory established

    Focal cohort: Copperbelt/Lusaka bottom-quintile (poverty_headcount_ratio).
    This is the Demo 8 Act 2 "+342K cohort effect" anchor — cohort_poverty_headcount
    must be non-null for the fixture to serve as Demo 8 CI calibration evidence (SF-3).

    Fidelity target: MAGNITUDE_MATCH preferred; DIRECTION_ONLY minimum.
    CM advises on tier classification at pre-merge review.
    """
    # IMF WEO April 2015, Zambia 2014 outturn: 4.7% GDP growth.
    # Copper sector strong; diversification progress limited. Fiscal position
    # sustained by mining tax receipts at near-peak copper prices.
    initial_gdp_growth = QuantitySchema(
        value="0.047",
        unit="ratio",
        variable_type="ratio",
        confidence_tier=2,
        observation_date=date(2015, 4, 1),
        source_registry_id="IMF_WEO_APR2015",
        measurement_framework="financial",
    )

    # WDI 2014 (ILO-modelled) — Zambia national unemployment ~13.3%.
    # High informal employment in agriculture and artisanal mining; formal
    # rate understates total joblessness. Confidence tier 3: ILO model estimate.
    initial_unemployment_rate = QuantitySchema(
        value="0.133",
        unit="ratio",
        variable_type="ratio",
        confidence_tier=3,
        observation_date=date(2015, 1, 1),
        source_registry_id="WDI_ZMB_2014",
        measurement_framework="human_development",
    )

    # WDI 2014 — Zambia health expenditure ~5.3% of GDP.
    # Includes government (4.3%) and private/NGO funding; HIV/AIDS
    # programme costs inflate health share relative to income level.
    initial_health_expenditure = QuantitySchema(
        value="0.053",
        unit="ratio",
        variable_type="ratio",
        confidence_tier=2,
        observation_date=date(2015, 1, 1),
        source_registry_id="WDI_ZMB_2014",
        measurement_framework="human_development",
    )

    # WDI 2014 — Zambia secondary net enrollment ~28%.
    # Low secondary completion rate reflects distance-to-school barriers and
    # household income constraints in rural Copperbelt communities.
    initial_net_enrollment_secondary = QuantitySchema(
        value="0.280",
        unit="ratio",
        variable_type="ratio",
        confidence_tier=2,
        observation_date=date(2015, 1, 1),
        source_registry_id="WDI_ZMB_2014",
        measurement_framework="human_development",
    )

    # IMF IFS 2014 / Bank of Zambia Annual Report 2014 — approximately 3.0 months
    # import coverage. Reserves adequate pre-crash but exposed to rapid drawdown
    # once copper revenues declined. The 2015–2016 drawdown was significant.
    initial_reserve_coverage_months = QuantitySchema(
        value="3.0",
        unit="months",
        variable_type="ratio",
        confidence_tier=2,
        observation_date=date(2015, 1, 1),
        source_registry_id="IMF_IFS_ZMB_2014",
        measurement_framework="financial",
    )

    # IMF Article IV Zambia 2014 — long-run structural growth estimate ~5.0%.
    # Resource-led potential; copper export base underpins fiscal and external
    # position. Diversification trajectory implied but thin outside copper.
    initial_trend_growth = QuantitySchema(
        value="0.050",
        unit="ratio",
        variable_type="ratio",
        confidence_tier=3,
        observation_date=date(2014, 1, 1),
        source_registry_id="IMF_ARTIVZMB2014",
        measurement_framework="financial",
    )

    # EMBI spread Zambia 2014 — 2012 Eurobond issued at 5.375% (10Y).
    # By 2014, secondary spreads had widened as copper prices began softening;
    # EMBI+ spread ~540bps over UST 10Y (~2.50% → total yield ~7.9%).
    # Confidence tier 2: EMBI secondary market data, 2014 annual average.
    initial_sovereign_risk_premium = QuantitySchema(
        value="0.054",
        unit="ratio",
        variable_type="ratio",
        attribute_type="rate",
        confidence_tier=2,
        observation_date=date(2014, 6, 1),
        source_registry_id="EMBI_ZMB_2014",
        measurement_framework="financial",
    )

    # UNCTAD World Investment Report 2014 — Zambia inward FDI stock / GDP.
    # Dominated by copper mining investment; stock reflects capital-intensive
    # extraction sector (~45% of GDP — high for the income level).
    initial_fdi_stock_pct_gdp = QuantitySchema(
        value="0.450",
        unit="ratio",
        variable_type="stock",
        attribute_type="stock",
        confidence_tier=2,
        observation_date=date(2014, 1, 1),
        source_registry_id="UNCTAD_FDI_ZMB_2014",
        measurement_framework="financial",
    )

    # IMF BOP Statistics 2014 — Zambia net portfolio investment / GDP.
    # First Eurobond (2012) and FDI inflows produced modest positive portfolio
    # balance in 2014. Copper-linked outflows accelerated from 2015.
    initial_portfolio_flow_velocity = QuantitySchema(
        value="0.015",
        unit="ratio",
        variable_type="ratio",
        attribute_type="flow",
        confidence_tier=3,
        observation_date=date(2014, 1, 1),
        source_registry_id="IMF_BOP_ZMB_2014",
        measurement_framework="financial",
    )

    # Moody's B1 / S&P B+ Zambia 2014 (issued $750M Eurobond successfully).
    # Mapped to 0–100 index using 21-notch linear scale (AAA=100, D=0).
    # B1/B+ at this vintage; confidence tier 1: direct rating observation.
    # Rated slightly below SEN at same nominal level due to commodity concentration.
    initial_credit_rating_score = QuantitySchema(
        value="30.0",
        unit="index_0_100",
        variable_type="stock",
        attribute_type="structural_index",
        confidence_tier=1,
        observation_date=date(2014, 1, 1),
        source_registry_id="SP_ZMB_2014",
        measurement_framework="financial",
    )

    # WDI 2015 (2015 vintage, first available post-2015 survey) — Zambia national
    # poverty headcount ratio ~64.7% at the national poverty line. Zambia exhibits
    # high poverty despite upper-middle income aspirations ("copper paradox").
    # Copperbelt communities face both commodity employment shock exposure AND
    # food price inflation via kwacha depreciation. Confidence tier 2: survey-based.
    initial_poverty_headcount_ratio = QuantitySchema(
        value="0.647",
        unit="ratio",
        variable_type="ratio",
        confidence_tier=2,
        observation_date=date(2016, 1, 1),
        source_registry_id="WDI_ZMB_2014",
        measurement_framework="human_development",
    )

    # Copperbelt/Lusaka bottom-quintile focal cohort — Demo 8 load-bearing.
    # indicator_key = poverty_headcount_ratio: the advance endpoint reads this
    # from the step snapshot to produce cohort_poverty_headcount in the harness.
    # floor_value = 0.60: recovery floor below which improvement is meaningful
    # (Zambia Human Development Report 2022 target corridor reference).
    copperbelt_focal_cohort = FocalCohortConfig(
        indicator_key="poverty_headcount_ratio",
        floor_value=0.60,
        floor_label="Copperbelt/Lusaka bottom-quintile poverty floor",
        framework="human_development",
        recovery_horizon_years=10,
    )

    return _ZmbCalibrationRequest(
        entity_id="ZMB",
        is_pre_calibration=True,
        name="Zambia 2014-2019 Copper Price Crash Backtesting Fixture",
        description=(
            "G2B backtesting calibration fixture — Issue #1542 (Demo 8 load-bearing). "
            "Reproduces Zambia's 2014–2019 copper price crash episode (copper ≈ 70% "
            "of export earnings): fiscal deficit peak >7% GDP (2016), kwacha -45% "
            "(2015), $1B Eurobond (2017), pre-default trajectory (2019). "
            "Copperbelt/Lusaka bottom-quintile focal cohort provides cohort_poverty_"
            "headcount trajectory for Demo 8 Act 2 '+342K cohort effect' anchor. "
            "Chief Methodologist sign-off required before merge — fidelity tier "
            "classification governs CI interval credibility claim at Demo 8. "
            "Initial state: IMF WEO April 2015 + WDI 2014 + IMF IFS 2014 "
            "+ UNCTAD 2014 + Moody's B1/S&P B+ (2014) + EMBI spread 2014."
        ),
        configuration=ScenarioConfigSchema(
            entities=["ZMB"],
            n_steps=6,
            timestep_label="annual",
            start_date=date(2014, 1, 1),
            step_metadata={
                "1": {"significance": "SIGNIFICANT", "label": "Near-peak copper / Eurobond"},
                "2": {"significance": "CRITICAL",    "label": "Copper crash / kwacha -45%"},
                "3": {"significance": "CRITICAL",    "label": "Fiscal deficit >7% GDP"},
                "4": {"significance": "SIGNIFICANT", "label": "Eurobond $1B rescue"},
                "5": {"significance": "SIGNIFICANT", "label": "Debt service pressure"},
                "6": {"significance": "SIGNIFICANT", "label": "Pre-default trajectory"},
            },
            monitored_focal_cohorts=[copperbelt_focal_cohort],
            initial_attributes={
                "ZMB": {
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
                },
            },
        ),
        scheduled_inputs=[
            # Step 2 (2015): Copper crash — LME copper fell from $6,200/t (2014)
            # to $4,600/t (2015), a 26% annual average decline. Zambia copper
            # exports ≈ 70% of goods exports → major fiscal revenue shortfall.
            ScheduledInputSchema(
                step=2,
                input_type="FiscalPolicyInput",
                input_data={
                    "instrument": "spending_change",
                    "target_entity": "ZMB",
                    "sector": "government",
                    "value": "-0.040",
                    "duration_years": 1,
                },
            ),
            # Step 2 (2015): Direct GDP growth shock from copper sector contraction.
            # Mining sector GDP contribution ~12%; copper production also fell.
            ScheduledInputSchema(
                step=2,
                input_type="gdp_growth_change",
                input_data={
                    "target_entity": "ZMB",
                    "magnitude": "-0.015",
                },
            ),
            # Step 3 (2016): Fiscal deficit peaks (>7% GDP). Copper prices
            # bottomed; power shortages compounded by drought (Kariba hydro down).
            # Forced spending cuts but revenue still below breakeven.
            ScheduledInputSchema(
                step=3,
                input_type="FiscalPolicyInput",
                input_data={
                    "instrument": "spending_change",
                    "target_entity": "ZMB",
                    "sector": "government",
                    "value": "-0.050",
                    "duration_years": 1,
                },
            ),
            # Step 3 (2016): Continued growth drag — second full copper shock year.
            ScheduledInputSchema(
                step=3,
                input_type="gdp_growth_change",
                input_data={
                    "target_entity": "ZMB",
                    "magnitude": "-0.010",
                },
            ),
            # Step 3 (2016): IMF Staff Monitored Program discussions — not a
            # full programme, but signals external anchor engagement begins.
            ScheduledInputSchema(
                step=3,
                input_type="EmergencyPolicyInput",
                input_data={
                    "instrument": "imf_program_acceptance",
                    "target_entity": "ZMB",
                    "expected_duration": 1,
                    "program_size_gdp_ratio": "0.00",
                },
            ),
            # Step 4 (2017): $1B Eurobond issued at elevated spread (~7.6%).
            # Buys fiscal time; deficit reduction attempt; copper partially recovers.
            ScheduledInputSchema(
                step=4,
                input_type="FiscalPolicyInput",
                input_data={
                    "instrument": "debt_issuance",
                    "target_entity": "ZMB",
                    "sector": "",
                    "value": "0.030",
                    "duration_years": 7,
                },
            ),
            # Step 4 (2017): Fiscal consolidation attempt on expenditure side.
            ScheduledInputSchema(
                step=4,
                input_type="FiscalPolicyInput",
                input_data={
                    "instrument": "spending_change",
                    "target_entity": "ZMB",
                    "sector": "government",
                    "value": "-0.025",
                    "duration_years": 1,
                },
            ),
            # Step 5 (2018): Debt service pressure — Eurobond coupon payments
            # plus domestic debt rollover constrain fiscal space.
            ScheduledInputSchema(
                step=5,
                input_type="FiscalPolicyInput",
                input_data={
                    "instrument": "spending_change",
                    "target_entity": "ZMB",
                    "sector": "government",
                    "value": "-0.030",
                    "duration_years": 1,
                },
            ),
            # Step 6 (2019): Pre-default trajectory — spreads widening rapidly.
            # IMF programme stalls; debt sustainability concerns public.
            ScheduledInputSchema(
                step=6,
                input_type="FiscalPolicyInput",
                input_data={
                    "instrument": "spending_change",
                    "target_entity": "ZMB",
                    "sector": "government",
                    "value": "-0.030",
                    "duration_years": 1,
                },
            ),
        ],
    )
