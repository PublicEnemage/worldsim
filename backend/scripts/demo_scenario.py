"""
Milestone 1 Demo: USA Tariff Escalation 2025 Scenario.

Instantiates the USA tariff escalation scenario using the ScenarioRunner
from the Input Orchestration Layer (ADR-002). Seeds ten real countries with
2024-2025 attribute values from IMF WEO October 2024 and World Bank WDI 2024,
wires real trade relationships with weights from UN Comtrade 2023, injects
the tariff shock as a TradePolicyInput at timestep 1, and runs for ten annual
timesteps.

Data sources:
  GDP growth, debt/GDP: IMF World Economic Outlook October 2024 release
  Trade openness: World Bank World Development Indicators 2024 release
  Political stability: World Bank Worldwide Governance Indicators 2023
  Trade relationship weights: UN Comtrade 2023 bilateral trade data,
    computed as bilateral trade / source entity total trade
  All accessed 2026-04-16 for scenario vintage dating.

Limitations:
  This demo models first-round propagation through a static trade network
  only. It cannot model trade diversion, exchange rate effects, fiscal
  multipliers, or endogenous module responses. See
  docs/scenarios/module-capability-registry.md and
  docs/scenarios/proposed/USA-tariff-escalation-2025.md for full details.

Usage:
  cd backend
  python scripts/demo_scenario.py
"""

from __future__ import annotations

import os
import sys

# Ensure backend root is on the path when running as a script
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import datetime, timedelta
from decimal import Decimal

from app.simulation.engine.models import PropagationRule as _PropagationRule
from app.simulation.engine.models import (
    Relationship,
    ResolutionConfig,
    ScenarioConfig,
    SimulationEntity,
    SimulationState,
)
from app.simulation.orchestration import (
    ScenarioRunner,
    TradeInstrument,
    TradePolicyInput,
)

# ---------------------------------------------------------------------------
# Scenario parameters
# ---------------------------------------------------------------------------

SCENARIO_ID = "USA-TARIFF-2025-DEMO"
START_DATE = datetime(2025, 1, 1)
N_STEPS = 10
TIMESTEP_DELTA = timedelta(days=365)

# Tariff shock parameters (see scenario specification for calibration notes)
# value = 0.25 represents a 25% tariff rate imposed at the source entity.
# The event attribute "trade_tariff_rate_goods" propagates through the trade
# network with attenuation, showing each country's first-round tariff exposure
# relative to its trade weight with the source. This is an exposure measure,
# not a GDP impact. The Trade Module (future milestone) will translate tariff
# exposure into GDP growth changes via calibrated pass-through coefficients.
TARIFF_SHOCK_DELTA = Decimal("0.25")
TARIFF_ATTENUATION = 0.6
TARIFF_MAX_HOPS = 2

# ---------------------------------------------------------------------------
# Seed data: entity attributes
# Sources: IMF WEO Oct 2024, World Bank WDI 2024, World Bank WGI 2023
# ---------------------------------------------------------------------------

_ENTITY_SEED: dict[str, dict[str, float]] = {
    # ISO3: {attribute: value}
    # gdp_growth: annual growth rate (fraction)
    # debt_gdp_ratio: general government gross debt as fraction of GDP
    # trade_openness: (exports + imports) / GDP
    # political_stability: World Bank WGI percentile rank, normalised [0, 1]
    "USA": {
        "gdp_growth": 0.028,     # 2.8% — IMF WEO Oct 2024
        "debt_gdp_ratio": 1.22,  # 122% — IMF WEO Oct 2024
        "trade_openness": 0.27,  # 27%  — World Bank WDI 2024
        "political_stability": 0.65,  # World Bank WGI 2023
    },
    "CHN": {
        "gdp_growth": 0.049,     # 4.9% — IMF WEO Oct 2024
        "debt_gdp_ratio": 0.83,  # 83%  — IMF WEO Oct 2024
        "trade_openness": 0.37,  # 37%  — World Bank WDI 2024
        "political_stability": 0.40,
    },
    "DEU": {
        "gdp_growth": 0.001,     # 0.1% — IMF WEO Oct 2024 (Germany; EU proxy)
        "debt_gdp_ratio": 0.63,  # 63%  — IMF WEO Oct 2024
        "trade_openness": 0.89,  # 89%  — World Bank WDI 2024
        "political_stability": 0.80,
    },
    "MEX": {
        "gdp_growth": 0.015,     # 1.5% — IMF WEO Oct 2024
        "debt_gdp_ratio": 0.54,  # 54%  — IMF WEO Oct 2024
        "trade_openness": 0.78,  # 78%  — World Bank WDI 2024
        "political_stability": 0.30,
    },
    "CAN": {
        "gdp_growth": 0.012,     # 1.2% — IMF WEO Oct 2024
        "debt_gdp_ratio": 1.07,  # 107% — IMF WEO Oct 2024
        "trade_openness": 0.66,  # 66%  — World Bank WDI 2024
        "political_stability": 0.90,
    },
    "JPN": {
        "gdp_growth": 0.009,     # 0.9% — IMF WEO Oct 2024
        "debt_gdp_ratio": 2.53,  # 253% — IMF WEO Oct 2024
        "trade_openness": 0.36,  # 36%  — World Bank WDI 2024
        "political_stability": 0.80,
    },
    "GBR": {
        "gdp_growth": 0.009,     # 0.9% — IMF WEO Oct 2024
        "debt_gdp_ratio": 1.04,  # 104% — IMF WEO Oct 2024
        "trade_openness": 0.58,  # 58%  — World Bank WDI 2024
        "political_stability": 0.70,
    },
    "VNM": {
        "gdp_growth": 0.050,     # 5.0% — IMF WEO Oct 2024
        "debt_gdp_ratio": 0.37,  # 37%  — IMF WEO Oct 2024
        "trade_openness": 1.93,  # 193% — World Bank WDI 2024 (highly export-dependent)
        "political_stability": 0.40,
    },
    "BRA": {
        "gdp_growth": 0.029,     # 2.9% — IMF WEO Oct 2024
        "debt_gdp_ratio": 0.87,  # 87%  — IMF WEO Oct 2024
        "trade_openness": 0.33,  # 33%  — World Bank WDI 2024
        "political_stability": 0.30,
    },
    "IND": {
        "gdp_growth": 0.070,     # 7.0% — IMF WEO Oct 2024
        "debt_gdp_ratio": 0.84,  # 84%  — IMF WEO Oct 2024
        "trade_openness": 0.46,  # 46%  — World Bank WDI 2024
        "political_stability": 0.40,
    },
}

# ---------------------------------------------------------------------------
# Trade relationship weights
# Source: UN Comtrade 2023 bilateral trade data
# Method: bilateral trade value / source entity total trade (imports + exports)
# ---------------------------------------------------------------------------

_TRADE_RELATIONSHIPS: list[tuple[str, str, float]] = [
    # (source, target, weight)
    # USA outbound trade
    ("USA", "CHN", 0.14),  # China is ~14% of US total trade
    ("USA", "DEU", 0.06),  # Germany ~6% (EU proxy)
    ("USA", "MEX", 0.16),  # Mexico ~16% (USMCA, largest single partner by some measures)
    ("USA", "CAN", 0.15),  # Canada ~15% (USMCA)
    ("USA", "JPN", 0.05),  # Japan ~5%
    ("USA", "GBR", 0.04),  # UK ~4%
    ("USA", "VNM", 0.03),  # Vietnam ~3%
    ("USA", "BRA", 0.02),  # Brazil ~2%
    ("USA", "IND", 0.02),  # India ~2%
    # CHN outbound trade (partial — major partners only)
    ("CHN", "USA", 0.15),  # US is ~15% of China total trade
    ("CHN", "DEU", 0.08),  # Germany/EU ~8%
    ("CHN", "JPN", 0.06),  # Japan ~6%
    ("CHN", "VNM", 0.10),  # Vietnam ~10% (deep GVC integration)
    ("CHN", "BRA", 0.03),  # Brazil ~3%
]


def _build_initial_state() -> SimulationState:
    """Construct the initial simulation state from seed data.

    Returns:
        SimulationState seeded with 2024-2025 attribute values for ten
        countries and their trade relationships.
    """
    entities = {
        iso3: SimulationEntity(
            id=iso3,
            entity_type="country",
            attributes=dict(attrs),
            metadata={"iso3": iso3},
        )
        for iso3, attrs in _ENTITY_SEED.items()
    }

    relationships = [
        Relationship(
            source_id=source,
            target_id=target,
            relationship_type="trade",
            weight=weight,
        )
        for source, target, weight in _TRADE_RELATIONSHIPS
    ]

    scenario_config = ScenarioConfig(
        scenario_id=SCENARIO_ID,
        name="USA Tariff Escalation 2025",
        description=(
            "Milestone 1 demo scenario. US tariff shock propagated through "
            "static trade network. First-round effects only — no Trade Module."
        ),
        start_date=START_DATE,
        end_date=START_DATE + timedelta(days=365 * N_STEPS),
    )

    return SimulationState(
        timestep=START_DATE,
        resolution=ResolutionConfig(),
        entities=entities,
        relationships=relationships,
        events=[],
        scenario_config=scenario_config,
    )


def _build_tariff_input() -> TradePolicyInput:
    """Construct the TradePolicyInput for the US tariff shock.

    The input fires at step 1 and propagates through the trade network.
    See scenario specification for calibration notes.

    Returns:
        TradePolicyInput representing the US tariff imposition.
    """
    return TradePolicyInput(
        actor_id="usa_trade_representative",
        actor_role="president",
        target_entity="CHN",          # primary bilateral target
        source_entity="USA",          # imposing entity
        instrument=TradeInstrument.TARIFF_RATE,
        affected_sector="goods",
        value=TARIFF_SHOCK_DELTA,     # -1pp GDP growth shock proxy
        retaliation_modeled=False,    # retaliation excluded in this demo
        effective_date=datetime(2025, 4, 1),
        justification=(
            "US tariff escalation April 2025: broad tariff regime including "
            "10% baseline, 25% on USMCA partners, up to 145% on Chinese goods. "
            "Value represents aggregate GDP growth impact proxy; pending "
            "calibration by Trade Module."
        ),
        timestamp=datetime(2025, 1, 1),
        propagation_rules=[
            _PropagationRule(
                relationship_type="trade",
                attenuation_factor=TARIFF_ATTENUATION,
                max_hops=TARIFF_MAX_HOPS,
            )
        ],
    )


def _print_header() -> None:
    """Print the scenario header and data provenance notice."""
    print("\n" + "=" * 80)
    print("WorldSim — Milestone 1 Demo")
    print("Scenario: USA Tariff Escalation 2025")
    print("=" * 80)
    print(
        "\nDATA NOTICE: Seed values from IMF WEO Oct 2024, World Bank WDI 2024,"
        "\nWorld Bank WGI 2023, UN Comtrade 2023. All accessed 2026-04-16."
        "\n"
        "\nLIMITATIONS: This demo models first-round propagation through a static"
        "\ntrade network only. No Trade Module, no Macroeconomic Module, no"
        "\nendogenous dynamics. Results show network exposure structure only —"
        "\nnot calibrated economic impact magnitudes. See module-capability-registry.md."
    )
    print()


def _print_table(history: list[SimulationState]) -> None:
    """Print two tables: initial gdp_growth seed values and propagated tariff exposure.

    Table 1 shows the initial 2024 GDP growth rates for reference.
    Table 2 shows trade_tariff_rate_goods — the tariff exposure that propagates
    through the network after the shock is injected at step 1.

    Args:
        history: Complete state history from ScenarioRunner.run().
    """
    iso3_list = list(_ENTITY_SEED.keys())
    col_w = 10

    # Table 1: Initial GDP growth rates (reference, unchanged by engine without modules)
    print("Table 1: Initial GDP growth rates (2024 seed values, IMF WEO Oct 2024)")
    print("         These are unchanged during this demo — no Macroeconomic Module yet.")
    print()
    header = f"{'Entity':<8}" + "".join(f"{iso3:>{col_w}}" for iso3 in iso3_list)
    print(header)
    print("-" * len(header))
    row = f"{'gdp_grwth':<8}" + "".join(
        f"{history[0].entities[iso3].get_attribute('gdp_growth'):>{col_w}.4f}"
        for iso3 in iso3_list
    )
    print(row)
    print()

    # Table 2: Tariff exposure (trade_tariff_rate_goods) propagating through network
    print("Table 2: trade_tariff_rate_goods — tariff exposure propagated through network")
    print("         Step 0: all zeros (tariff not yet imposed).")
    print("         Step 1: USA=0.25 (tariff imposed). Partners receive attenuated signal.")
    print("         Step 2: Second-hop effects reach CHN's trading partners.")
    print()
    header2 = f"{'Step':<6} {'Year':<6}" + "".join(
        f"{iso3:>{col_w}}" for iso3 in iso3_list
    )
    print(header2)
    print("-" * len(header2))

    for step, state in enumerate(history):
        year = state.timestep.year
        row2 = f"{step:<6} {year:<6}" + "".join(
            f"{state.entities[iso3].get_attribute('trade_tariff_rate_goods'):>{col_w}.5f}"
            if iso3 in state.entities
            else f"{'N/A':>{col_w}}"
            for iso3 in iso3_list
        )
        print(row2)

    print()
    print("Interpretation:")
    print("  USA=0.25000 — tariff source (full delta, unattenuated)")
    print("  MEX, CAN, CHN — largest first-round exposure (highest trade weights to USA)")
    print("  DEU, JPN, GBR — smaller first-round exposure")
    print("  VNM, BRA, IND — smallest first-round exposure from USA")
    print("  Step 2 onwards: CHN's trade links propagate second-hop exposure")
    print()
    print("LIMITATION: This is tariff exposure, not GDP impact.")
    print("The Trade Module (future milestone) will translate exposure into GDP change.")
    print("Current magnitudes are structurally meaningful (network position) but")
    print("should not be interpreted as economic impact estimates.")


def main() -> None:
    """Run the USA tariff escalation demo scenario."""
    _print_header()

    initial_state = _build_initial_state()
    tariff_input = _build_tariff_input()

    runner = ScenarioRunner(
        initial_state=initial_state,
        scheduled_inputs=[(1, tariff_input)],
        modules=[],  # No domain modules yet — Milestone 1
        n_steps=N_STEPS,
        timestep_delta=TIMESTEP_DELTA,
        session_id="demo-session-001",
    )

    print("Running scenario...")
    history = runner.run()

    print(f"Completed {N_STEPS} annual timesteps. State history: {len(history)} entries.")
    print(f"Audit log: {len(runner.audit_log)} control input record(s).")
    print()

    _print_table(history)

    # Print audit summary
    print("\n--- Audit Log ---")
    for record in runner.audit_log.records:
        print(
            f"  [{record.timestep.strftime('%Y-%m-%d')}] "
            f"{record.input_type} | actor: {record.actor_role} | "
            f"source: {record.source.value} | "
            f"events: {record.translated_events}"
        )


if __name__ == "__main__":
    main()
