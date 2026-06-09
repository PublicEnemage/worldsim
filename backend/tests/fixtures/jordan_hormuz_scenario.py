"""Jordan/Egypt 2024–2031 Strait of Hormuz Disruption — scenario configuration fixture.

Demo 4 (Milestone 12) case study demonstrating ExternalSectorModule (ADR-012) and
multi-entity composite scoring. The Hormuz disruption scenario models Jordan (JOR)
and Egypt (EGY) — two energy-import-dependent MENA economies — facing a sustained
fuel and food price shock through a six-step disruption arc (steps 1–6), followed
by a two-step recovery window.

Two entities activate the financial and human_development composite scores
(percentile rank requires ≥2 entities — Issue #193 guard lifted). Jordan's high
fuel import dependency (0.42) and Egypt's high food import dependency (0.35)
produce divergent shock transmission pathways across the four framework axes.

Mode 3 demonstration: the EL's steering scenario begins at step 3 — what if
Jordan increases reserve coverage through emergency GCC aid? The Mode 3 branch
trajectory shows the reserve pathway with vs. without the intervention.

Simulation structure:
  build_jordan_hormuz_scenario(): n_steps=8 (annual: 2024→2031).
    Base fixture with ExternalSectorModule commodity shocks. Two entities.
  build_jordan_hormuz_demo_scenario(): Demo 4 variant.
    Extends base with EcologicalModule, GovernanceModule, governance seeds,
    and political context for JOR. All four framework axes live.

Commodity shocks:
  Steps 1–6: Fuel price shock — magnitude +25% (disruption + insurance premium)
  Steps 2–6: Food price shock — magnitude +15% (supply chain disruption via Hormuz)

Scheduled inputs:
  Step 3: JOR IMF program acceptance (reserve pressure triggers IFI engagement)
  Step 3: EGY emergency declaration (food protest escalation from step-2 food shock)
  Step 4: JOR fiscal spending cut (IMF conditionality)

Initial state sources (2024 vintage):
  JOR: IMF WEO April 2024; DOS LFS Q1 2024; WDI 2022 (health, enrollment);
       CBJ Annual Report 2023 (reserves); WB 2023 energy trade + WFP 2024 food basket
  EGY: IMF WEO April 2024; CAPMAS LFS Q1 2024; WDI 2022; CBE/IMF 2024 (reserves);
       WB 2023 energy trade + WFP 2024 food basket

All import dependency coefficients are Tier 3 synthetic estimates per
DATA_STANDARDS.md §Confidence Tier System. Governance seeds sourced from
WB WGI 2022 (rule of law) and V-Dem v14 2023 (democratic quality) in the
demo scenario.

References: ADR-012; Issue #752 (ExternalSectorModule); Issue #793 (Demo 4 scope).
"""
from __future__ import annotations

from datetime import date
from decimal import Decimal

from app.schemas import (
    CommodityShockConfig,
    PoliticalContext,
    QuantitySchema,
    ScenarioConfigSchema,
    ScenarioCreateRequest,
    ScheduledInputSchema,
)


def build_jordan_hormuz_scenario() -> ScenarioCreateRequest:
    """Build the Jordan/Egypt Strait of Hormuz disruption base scenario.

    Two entities: JOR (Jordan) + EGY (Egypt).
    ExternalSectorModule distributes fuel and food shocks by import dependency.
    Financial and human_development composite scores are live (≥2 entities).

    Returns a ScenarioCreateRequest ready to POST to /api/v1/scenarios.
    8 steps (annual: 2024→2031). Commodity shocks active steps 1–6 (fuel) and
    2–6 (food). Scheduled IMF engagement at step 3; austerity at step 4.

    References: ADR-012; Issue #752; Issue #793.
    """
    # ── Jordan (JOR) initial state ────────────────────────────────────────────

    # IMF WEO April 2024 — Jordan calendar year 2024 GDP growth forecast: +2.5%
    jor_gdp_growth = QuantitySchema(
        value="0.025",
        unit="ratio",
        variable_type="ratio",
        confidence_tier=2,
        observation_date=date(2024, 4, 1),
        source_registry_id="IMF_WEO_APR2024",
        measurement_framework="financial",
    )

    # Jordan Department of Statistics Labour Force Survey Q1 2024 — 17.8%
    # Jordan maintains persistently high unemployment driven by demographic pressure
    # and structural barriers to female labour force participation (36% LFPR).
    jor_unemployment = QuantitySchema(
        value="0.178",
        unit="ratio",
        variable_type="ratio",
        confidence_tier=2,
        observation_date=date(2024, 3, 1),
        source_registry_id="DOS_LFS_Q1_2024",
        measurement_framework="human_development",
    )

    # World Bank WDI 2022 (most recent vintage) — Jordan health expenditure 7.8% GDP
    jor_health_expenditure = QuantitySchema(
        value="0.078",
        unit="ratio",
        variable_type="ratio",
        confidence_tier=2,
        observation_date=date(2023, 12, 1),
        source_registry_id="WDI_2022",
        measurement_framework="human_development",
    )

    # World Bank WDI 2022 — Jordan net secondary enrollment 83.0%
    jor_net_enrollment = QuantitySchema(
        value="0.830",
        unit="ratio",
        variable_type="ratio",
        confidence_tier=2,
        observation_date=date(2023, 12, 1),
        source_registry_id="WDI_2022",
        measurement_framework="human_development",
    )

    # Central Bank of Jordan (CBJ) Annual Report 2023 — reserve coverage 7.1 months.
    # Jordan is above the SIGNIFICANT threshold (4.0 months) at scenario entry. The
    # Hormuz fuel shock depletes reserves as import costs rise without offsetting
    # hydrocarbon export revenue (Jordan has negligible energy exports).
    jor_reserves = QuantitySchema(
        value="7.1",
        unit="months",
        variable_type="ratio",
        confidence_tier=2,
        observation_date=date(2023, 12, 31),
        source_registry_id="CBJ_ANNUAL_2023",
        measurement_framework="financial",
    )

    # IMF Article IV 2024 — Jordan medium-term potential growth 3.0%.
    # Mean-reversion channel seed (ADR-006 Amendment 1 — Issue #221).
    jor_trend_growth = QuantitySchema(
        value="0.030",
        unit="ratio",
        variable_type="ratio",
        confidence_tier=3,
        observation_date=date(2024, 1, 1),
        source_registry_id="IMF_WEO_APR2024",
        measurement_framework="financial",
    )

    # Jordan fuel import dependency — Tier 3 synthetic estimate.
    # Jordan imports ~96% of energy needs from Gulf states via Hormuz-routed supply
    # chains. The 0.42 coefficient captures fuel's share of total import exposure to
    # commodity price shocks (World Bank 2023 energy trade; WFP 2024 basket). Cape of
    # Good Hope routing adds 18–25% cost premium per disruption event.
    jor_fuel_dep = QuantitySchema(
        value="0.42",
        unit="ratio",
        variable_type="stock",
        confidence_tier=3,
        observation_date=date(2024, 1, 1),
        source_registry_id="WB_2023_JOR_ENERGY_DEP",
        measurement_framework="financial",
    )

    # Jordan food import dependency — Tier 3 synthetic estimate.
    # Jordan imports ~90% of food requirements. The 0.28 coefficient represents the
    # share of food import costs sensitive to Hormuz shipping route pricing (WFP 2024
    # basket analysis). Wheat, rice, and sugar are primary Gulf-routed commodities.
    jor_food_dep = QuantitySchema(
        value="0.28",
        unit="ratio",
        variable_type="stock",
        confidence_tier=3,
        observation_date=date(2024, 1, 1),
        source_registry_id="WFP_2024_JOR_FOOD_DEP",
        measurement_framework="human_development",
    )

    # ── Egypt (EGY) initial state ────────────────────────────────────────────

    # IMF WEO April 2024 — Egypt calendar year 2024 GDP growth projection: +2.9%
    # FY2024 (July 2023–June 2024) IMF projection 3.8%; calendar year adjusted
    # downward to 2.9% reflecting Q1 2024 currency devaluation and IMF program drag.
    egy_gdp_growth = QuantitySchema(
        value="0.029",
        unit="ratio",
        variable_type="ratio",
        confidence_tier=2,
        observation_date=date(2024, 4, 1),
        source_registry_id="IMF_WEO_APR2024",
        measurement_framework="financial",
    )

    # CAPMAS (Central Agency for Public Mobilization and Statistics) Q1 2024 — 7.1%
    # Official unemployment understates underemployment in the informal sector, which
    # absorbs ~55% of Egypt's labour force. Confidence tier 2 (official statistics;
    # methodology diverges from ILO definitions).
    egy_unemployment = QuantitySchema(
        value="0.071",
        unit="ratio",
        variable_type="ratio",
        confidence_tier=2,
        observation_date=date(2024, 3, 1),
        source_registry_id="CAPMAS_LFS_Q1_2024",
        measurement_framework="human_development",
    )

    # World Bank WDI 2022 — Egypt health expenditure 4.8% of GDP
    egy_health_expenditure = QuantitySchema(
        value="0.048",
        unit="ratio",
        variable_type="ratio",
        confidence_tier=2,
        observation_date=date(2023, 12, 1),
        source_registry_id="WDI_2022",
        measurement_framework="human_development",
    )

    # World Bank WDI 2022 — Egypt net secondary enrollment 79.0%
    egy_net_enrollment = QuantitySchema(
        value="0.790",
        unit="ratio",
        variable_type="ratio",
        confidence_tier=2,
        observation_date=date(2023, 12, 1),
        source_registry_id="WDI_2022",
        measurement_framework="human_development",
    )

    # Central Bank of Egypt (CBE) + IMF 2024 estimate — reserve coverage 5.3 months
    # Egypt rebuilt reserves following the March 2024 IMF EFF disbursement ($8bn).
    # Positioned below Jordan due to structural current account deficit and wider
    # import basket exposure to commodity price pressure.
    egy_reserves = QuantitySchema(
        value="5.3",
        unit="months",
        variable_type="ratio",
        confidence_tier=2,
        observation_date=date(2024, 3, 1),
        source_registry_id="CBE_IMF_2024",
        measurement_framework="financial",
    )

    # IMF Article IV 2024 — Egypt medium-term potential growth 4.5%
    egy_trend_growth = QuantitySchema(
        value="0.045",
        unit="ratio",
        variable_type="ratio",
        confidence_tier=3,
        observation_date=date(2024, 1, 1),
        source_registry_id="IMF_WEO_APR2024",
        measurement_framework="financial",
    )

    # Egypt fuel import dependency — Tier 3 synthetic estimate.
    # Egypt has domestic oil and gas production but became a net energy importer in
    # 2023–2024 as gas production declined. The 0.23 coefficient reflects refined
    # petroleum product import exposure to Hormuz-linked pricing (WB 2023 energy trade;
    # CAPMAS 2024). Lower than Jordan (0.42) because Egypt has partial domestic capacity.
    egy_fuel_dep = QuantitySchema(
        value="0.23",
        unit="ratio",
        variable_type="stock",
        confidence_tier=3,
        observation_date=date(2024, 1, 1),
        source_registry_id="WB_2023_EGY_ENERGY_DEP",
        measurement_framework="financial",
    )

    # Egypt food import dependency — Tier 3 synthetic estimate.
    # Egypt is the world's largest wheat importer (~12m tonnes annually). Gulf
    # transshipment hubs (Dubai, Abu Dhabi) handle ~35% of Egyptian food imports.
    # Hormuz disruption raises these commodities' effective prices through shipping
    # cost inflation. The 0.35 coefficient captures food import exposure to
    # Hormuz-linked pricing (WFP 2024 basket analysis).
    egy_food_dep = QuantitySchema(
        value="0.35",
        unit="ratio",
        variable_type="stock",
        confidence_tier=3,
        observation_date=date(2024, 1, 1),
        source_registry_id="WFP_2024_EGY_FOOD_DEP",
        measurement_framework="human_development",
    )

    return ScenarioCreateRequest(
        name="Jordan/Egypt 2024 Strait of Hormuz Disruption — Demo 4 Fixture",
        description=(
            "Demo 4 base fixture (Issue #793, ADR-012). "
            "Demonstrates ExternalSectorModule commodity price shock distribution "
            "across two MENA economies with divergent import dependency profiles. "
            "Jordan (JOR): high fuel dependency (0.42), moderate food dependency (0.28). "
            "Egypt (EGY): moderate fuel dependency (0.23), high food dependency (0.35). "
            "Two-entity scenario activates financial and human_development composite scores "
            "(Issue #193 guard lifted — percentile rank live). "
            "Fuel shock: magnitude 0.25, steps 1–6. Food shock: magnitude 0.15, steps 2–6. "
            "Initial state: IMF WEO April 2024 + DOS LFS Q1 2024 (JOR) "
            "+ CAPMAS LFS Q1 2024 (EGY) + WDI 2022 + CBJ 2023 + CBE/IMF 2024 "
            "+ WB 2023 energy trade + WFP 2024 food basket."
        ),
        configuration=ScenarioConfigSchema(
            entities=["JOR", "EGY"],
            n_steps=8,
            timestep_label="annual",
            start_date=date(2024, 1, 1),
            commodity_price_shocks=[
                CommodityShockConfig(
                    commodity_category="fuel",
                    magnitude=Decimal("0.25"),
                    start_step=1,
                    duration_steps=6,
                ),
                CommodityShockConfig(
                    commodity_category="food",
                    magnitude=Decimal("0.15"),
                    start_step=2,
                    duration_steps=5,
                ),
            ],
            initial_attributes={
                "JOR": {
                    "gdp_growth": jor_gdp_growth,
                    "unemployment_rate": jor_unemployment,
                    "health_expenditure_pct_gdp": jor_health_expenditure,
                    "net_enrollment_secondary": jor_net_enrollment,
                    "reserve_coverage_months": jor_reserves,
                    "trend_growth": jor_trend_growth,
                    "commodity_import_dependency_fuel": jor_fuel_dep,
                    "commodity_import_dependency_food": jor_food_dep,
                },
                "EGY": {
                    "gdp_growth": egy_gdp_growth,
                    "unemployment_rate": egy_unemployment,
                    "health_expenditure_pct_gdp": egy_health_expenditure,
                    "net_enrollment_secondary": egy_net_enrollment,
                    "reserve_coverage_months": egy_reserves,
                    "trend_growth": egy_trend_growth,
                    "commodity_import_dependency_fuel": egy_fuel_dep,
                    "commodity_import_dependency_food": egy_food_dep,
                },
            },
        ),
        scheduled_inputs=[
            # Step 3 (2026): Jordan IMF program acceptance.
            # Two years of fuel shock depletes reserves below the SIGNIFICANT threshold
            # (4.0 months), triggering IFI engagement. Jordan GDP ~$50bn;
            # program ~8% of GDP ($4bn emergency facility via IMF EFF/SBA).
            ScheduledInputSchema(
                step=3,
                input_type="EmergencyPolicyInput",
                input_data={
                    "instrument": "imf_program_acceptance",
                    "target_entity": "JOR",
                    "expected_duration": 3,
                    "program_size_gdp_ratio": "0.08",
                },
            ),
            # Step 3 (2026): Egypt emergency declaration.
            # Step 2 food shock drives bread subsidy pressure beyond fiscal capacity.
            # GovernanceModule applies one-step lag: democratic quality erodes at step 4.
            ScheduledInputSchema(
                step=3,
                input_type="EmergencyPolicyInput",
                input_data={
                    "instrument": "emergency_declaration",
                    "target_entity": "EGY",
                    "expected_duration": 1,
                },
            ),
            # Step 4 (2027): Jordan fiscal spending cut — IMF conditionality.
            # Pro-cyclical austerity applied during peak dual-shock pressure.
            # Duration 2 years (2027–2028) reflects standard IMF program conditionality arc.
            ScheduledInputSchema(
                step=4,
                input_type="FiscalPolicyInput",
                input_data={
                    "instrument": "spending_change",
                    "target_entity": "JOR",
                    "sector": "government",
                    "value": "-0.03",
                    "duration_years": 2,
                },
            ),
        ],
    )


def build_jordan_hormuz_demo_scenario() -> ScenarioCreateRequest:
    """Build the Jordan/Egypt Hormuz Demo 4 scenario with all four axes live.

    Extends build_jordan_hormuz_scenario() with:
      - modules_config enabling EcologicalModule and GovernanceModule
      - co2_concentration_ppm initial seed (421.0 ppm — NOAA Mauna Loa 2024)
      - rule_of_law_percentile seeds (JOR: 52.4; EGY: 29.3 — WB WGI 2022)
      - democratic_quality_score seeds (JOR: 0.21; EGY: 0.07 — V-Dem v14 2023)
      - elite_capture_coefficient seeds (JOR: 0.45; EGY: 0.62 — Tier 4 synthetic)
      - political_context for JOR (constitutional monarchy context)
      - step_metadata with SIGNIFICANT/CRITICAL labels for steps 1–6
      - GCC emergency budget support at step 3 (+6% GDP — Mode 3 demo anchor)

    Composite score status (M12):
      Financial       — live (percentile rank; JOR + EGY ≥2 entities, Issue #193)
      Human Dev       — live (percentile rank; ≥2 entities)
      Ecological      — live (CO2 boundary proximity; [0.0, 2.0])
      Governance      — live (normalized_absolute; WGI + V-Dem; ADR-005 Amendment 4)

    Step arc:
      Step 1 (2024): Hormuz disruption — fuel shock starts (SIGNIFICANT)
      Step 2 (2025): Food supply chain disruption joins (SIGNIFICANT)
      Step 3 (2026): Dual shock peak — JOR IMF program + GCC emergency support /
                     EGY emergency declaration (CRITICAL)
      Step 4 (2027): IMF conditionality — austerity during shock (SIGNIFICANT)
      Step 5 (2028): Reserve drawdown critical — both countries stressed (CRITICAL)
      Step 6 (2029): Hormuz resolution begins — shocks end (SIGNIFICANT)
      Step 7 (2030): Post-shock recovery (ROUTINE — no label)
      Step 8 (2031): Stabilization assessment (ROUTINE — no label)

    Mode 3 demo (Issue #817):
      Branch from step 3 at fiscal_multiplier=1.30.
      Baseline: Jordan secures initial GCC emergency disbursement (+6% GDP) alongside
      the IMF program. Mode 3 question: "What if Jordan had negotiated 30% more effective
      fiscal support?" The branch trajectory shows the reserve arc under 1.30x GCC aid
      and without the step-4 IMF conditionality austerity cut (not copied to branch since
      it is at step 4 > branch_from_step=3). This produces a visible trajectory divergence:
      the financial composite curve lifts away from the baseline in the Zone 1A chart.

    References: ADR-012; Issue #793; Issue #817; build_jordan_hormuz_scenario() (base).
    """
    base = build_jordan_hormuz_scenario()

    # NOAA Mauna Loa Observatory 2024 annual mean (preliminary): 421.0 ppm.
    # Global value applied to both JOR and EGY — atmospheric CO2 is uniform at
    # national scale. Confidence tier 1 (direct atmospheric measurement, NOAA).
    initial_co2 = QuantitySchema(
        value="421.0",
        unit="ppm",
        variable_type="stock",
        confidence_tier=1,
        observation_date=date(2024, 1, 1),
        source_registry_id="NOAA_MLO_2024",
        measurement_framework="ecological",
    )

    # World Bank WGI 2022 — Rule of Law Percentile Rank for Jordan: 52.4
    # Jordan sits at the 52nd percentile — above the MENA average (38th) but
    # below OECD median (70th). Confidence tier 2 (official multilateral statistics).
    jor_rule_of_law = QuantitySchema(
        value="52.4",
        unit="percentile_0_100",
        variable_type="stock",
        confidence_tier=2,
        observation_date=date(2022, 1, 1),
        source_registry_id="WB_WGI_JOR_2022_RULE_OF_LAW",
        measurement_framework="governance",
    )

    # V-Dem v14 Liberal Democracy Index for Jordan 2023: 0.21
    # Jordan is a constitutional monarchy with elected parliament but significant
    # royal prerogative. Limited political pluralism, constrained civil liberties.
    # Confidence tier 3 (expert-coded survey — high credibility, not official stats).
    jor_democratic_quality = QuantitySchema(
        value="0.21",
        unit="ratio_0_1",
        variable_type="stock",
        confidence_tier=3,
        observation_date=date(2023, 1, 1),
        source_registry_id="VDEM_V14_JOR_2023_LDI",
        measurement_framework="governance",
    )

    # Jordan elite capture coefficient — Tier 4 synthetic estimate.
    # Significant political-economic elite capture in public procurement, energy
    # import contracts, and phosphate/potash export monopolies.
    # Methodology: Lustig (2001) capture decomposition calibrated to Transparency
    # International CPI + World Bank enterprise survey data for Jordan 2022.
    jor_elite_capture = QuantitySchema(
        value="0.45",
        unit="ratio",
        variable_type="ratio",
        confidence_tier=4,
        observation_date=date(2022, 1, 1),
        source_registry_id="ACADEMIC_LITERATURE_LUSTIG_2001",
        measurement_framework="governance",
    )

    # World Bank WGI 2022 — Rule of Law Percentile Rank for Egypt: 29.3
    # Egypt's rule of law deteriorated post-2013 under military governance.
    # At the 29th percentile — near the bottom quartile of global distribution.
    # Confidence tier 2 (official multilateral statistics).
    egy_rule_of_law = QuantitySchema(
        value="29.3",
        unit="percentile_0_100",
        variable_type="stock",
        confidence_tier=2,
        observation_date=date(2022, 1, 1),
        source_registry_id="WB_WGI_EGY_2022_RULE_OF_LAW",
        measurement_framework="governance",
    )

    # V-Dem v14 Liberal Democracy Index for Egypt 2023: 0.07
    # Egypt has sustained minimal democratic space since the 2013 military takeover.
    # 0.07 puts Egypt in the bottom 5% of global democratic quality. The emergency
    # declaration at step 3 will drive this further below the MDA-GOV-DEMOCRACY-FLOOR
    # (0.70 threshold — already far below; governance alert fires from step 1).
    # Confidence tier 3 (expert-coded survey).
    egy_democratic_quality = QuantitySchema(
        value="0.07",
        unit="ratio_0_1",
        variable_type="stock",
        confidence_tier=3,
        observation_date=date(2023, 1, 1),
        source_registry_id="VDEM_V14_EGY_2023_LDI",
        measurement_framework="governance",
    )

    # Egypt elite capture coefficient — Tier 4 synthetic estimate.
    # The Supreme Council of the Armed Forces (SCAF) military-economic complex
    # controls an estimated 25–40% of Egypt's formal economy through military-owned
    # enterprises (National Service Products Organization, military-affiliated
    # construction conglomerates, consumer goods production).
    # Higher than Jordan (0.45) — one of the highest capture coefficients in MENA.
    egy_elite_capture = QuantitySchema(
        value="0.62",
        unit="ratio",
        variable_type="ratio",
        confidence_tier=4,
        observation_date=date(2022, 1, 1),
        source_registry_id="ACADEMIC_LITERATURE_LUSTIG_2001",
        measurement_framework="governance",
    )

    updated_jor_attrs = {
        **base.configuration.initial_attributes.get("JOR", {}),
        "co2_concentration_ppm": initial_co2,
        "rule_of_law_percentile": jor_rule_of_law,
        "democratic_quality_score": jor_democratic_quality,
        "elite_capture_coefficient": jor_elite_capture,
    }

    updated_egy_attrs = {
        **base.configuration.initial_attributes.get("EGY", {}),
        "co2_concentration_ppm": initial_co2,
        "rule_of_law_percentile": egy_rule_of_law,
        "democratic_quality_score": egy_democratic_quality,
        "elite_capture_coefficient": egy_elite_capture,
    }

    # step_metadata: 1-based string keys → significance + label.
    # Steps 1, 2, 4, 6 are SIGNIFICANT; steps 3 and 5 are CRITICAL.
    # Steps 7–8 are ROUTINE — absent keys default to ROUTINE per trajectory contract.
    # Labels ≤32 chars per DATA_STANDARDS.md §Scenario Fixture Step Annotation.
    step_metadata = {
        "1": {"significance": "SIGNIFICANT", "label": "Hormuz disruption / fuel shock"},
        "2": {"significance": "SIGNIFICANT", "label": "Food supply chain disruption"},
        "3": {"significance": "CRITICAL", "label": "Dual shock peak / IMF + GCC"},
        "4": {"significance": "SIGNIFICANT", "label": "IMF conditionality austerity"},
        "5": {"significance": "CRITICAL", "label": "Reserve drawdown critical"},
        "6": {"significance": "SIGNIFICANT", "label": "Hormuz resolution begins"},
    }

    # Jordan political context (2024 — constitutional monarchy).
    # Government approval: Arab Barometer Wave VII 2023 — trust in government ~38%
    # for Jordan; used as proxy for approval rating.
    # Coalition seat margin: 2024 parliamentary elections (Sept 10, 2024) —
    # ruling coalition held 65 of 138 seats (47.1%); narrow plurality, not majority.
    # Months to next election: next elections ~2028 (4-year term) → ~48 months.
    # Civil society: CIVICUS 2024 Jordan — civic space "narrowed"; index 0.38.
    # Legitimacy index: composite estimate from WGI Voice and Accountability
    # (percentile ~25) + Eurobarometer MENA equivalent; calibrated to 0.50.
    jor_political_context = PoliticalContext(
        government_approval_rating=Decimal("0.38"),
        coalition_seat_margin=None,
        months_to_next_election=48,
        civil_society_organization_strength=Decimal("0.38"),
        legitimacy_index=Decimal("0.50"),
    )

    demo_config = base.configuration.model_copy(
        update={
            "modules_config": {
                "ecological": {"enabled": True},
                "governance": {"enabled": True},
            },
            "initial_attributes": {
                "JOR": updated_jor_attrs,
                "EGY": updated_egy_attrs,
            },
            "step_metadata": step_metadata,
            "political_context": jor_political_context,
        }
    )

    # GCC emergency budget support — Mode 3 demo anchor (Issue #817).
    # Saudi Arabia and Gulf states historically provide multi-billion emergency packages
    # to Jordan in sovereign debt stress episodes. $3bn ≈ 6% of Jordan's 2024 GDP ($50bn).
    # Fires at step 3 alongside IMF program acceptance — the dual support represents the
    # policy response available to a well-connected MENA sovereign under external pressure.
    # Confidence tier 4: constructed scenario assumption (no real-data source for this event).
    # Mode 3 use: branch from step 3 at 1.30x fiscal multiplier amplifies the GCC aid.
    # The step-4 austerity cut is NOT in the branch (step 4 > branch_from_step=3),
    # so the branch shows both more GCC support AND no IMF conditionality — the
    # "negotiated-better-deal" counterfactual. See Issue #817 for the investigation.
    gcc_emergency_input = ScheduledInputSchema(
        step=3,
        input_type="FiscalPolicyInput",
        input_data={
            "instrument": "spending_change",
            "target_entity": "JOR",
            "value": "0.06",
            "duration_years": 1,
        },
    )

    return base.model_copy(update={
        "name": "Jordan/Egypt 2024 Hormuz Demo 4 — Multi-Framework ExternalSector",
        "description": (
            "Demo 4 scenario (Issue #793, ADR-012). "
            "EcologicalModule and GovernanceModule enabled — all four framework axes live. "
            "ExternalSectorModule active via commodity_price_shocks (fuel + food). "
            "Governance composite: normalized_absolute (WGI/V-Dem; ADR-005 Amendment 4). "
            "Composite scores live for all four axes (JOR + EGY ≥2 entities, Issue #193). "
            "Egypt (EGY) governance already below MDA-GOV-DEMOCRACY-FLOOR (0.07 < 0.70) "
            "— alert fires from step 1; emergency_declaration at step 3 deepens it. "
            "Jordan (JOR) reserve pressure drives IMF engagement at step 3; GCC emergency "
            "budget support (+6% GDP) also fires at step 3 (bilateral sovereign support). "
            "Mode 3 demo (Issue #817): branch from step 3 at 1.30x fiscal multiplier — "
            "'what if Jordan secured 30% more GCC support and avoided IMF austerity?' "
            "Produces visible trajectory divergence from step 4 onward. "
            "Initial state: IMF WEO April 2024 + DOS LFS Q1 2024 (JOR) "
            "+ CAPMAS LFS Q1 2024 (EGY) + WDI 2022 + CBJ 2023 + CBE/IMF 2024 "
            "+ WB 2023 energy trade + WFP 2024 food basket "
            "+ NOAA MLO 2024 (co2=421.0 ppm) "
            "+ WB WGI 2022 (rule_of_law: JOR=52.4, EGY=29.3) "
            "+ V-Dem v14 2023 (democratic_quality: JOR=0.21, EGY=0.07)."
        ),
        "configuration": demo_config,
        "scheduled_inputs": list(base.scheduled_inputs) + [gcc_emergency_input],
    })
