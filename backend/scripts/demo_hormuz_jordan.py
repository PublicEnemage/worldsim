"""Demo 4: Jordan/Egypt Strait of Hormuz Disruption — ExternalSectorModule showcase.

Demonstrates the WorldSim M12 milestone deliverable: ExternalSectorModule (ADR-012)
distributing global commodity price shocks across a multi-entity MENA scenario.
The Jordan/Egypt Hormuz disruption is the Demo 4 case — the first two-entity scenario
where all four framework composite scores are simultaneously live.

Primary visual argument:
  Jordan faces the highest fuel import dependency in the MENA region (42% — nearly
  all energy imported from Gulf states via Hormuz). Egypt faces the world's highest
  wheat import dependence (12m tonnes annually). A sustained Hormuz disruption hits
  both economies through different transmission channels: Jordan through fuel price
  inflation depleting reserves; Egypt through food price pressure triggering social
  unrest and governance deterioration.

  The divergence is the WorldSim thesis made visible: a finance minister in Amman
  and a minister in Cairo face the same external shock with radically different
  exposure profiles. The tool surfaces that difference — and the policy choices
  available to each government — before the crisis reaches irreversible thresholds.

Framework status at M12:
  Financial        — composite live (percentile rank; JOR + EGY ≥2 entities)
  Human Development — composite live (percentile rank; ≥2 entities)
  Ecological       — composite live (CO2 boundary proximity; [0.0, 2.0])
  Governance       — composite live (normalized_absolute; WGI + V-Dem; ADR-005 Am.4)

ExternalSectorModule demonstration (ADR-012):
  Fuel shock magnitude 0.25 distributed by import dependency:
    JOR (0.42 fuel dep): effect = 0.42 × 0.25 = 0.105 per step (steps 1–6)
    EGY (0.23 fuel dep): effect = 0.23 × 0.25 = 0.058 per step (steps 1–6)
  Food shock magnitude 0.15 distributed by import dependency:
    JOR (0.28 food dep): effect = 0.28 × 0.15 = 0.042 per step (steps 2–6)
    EGY (0.35 food dep): effect = 0.35 × 0.15 = 0.053 per step (steps 2–6)
  HCL transmission factor 0.3 → bottom-quintile consumption capacity reduced by
  30% of gross shock effect in human_development framework.

Mode 3 steering scenario:
  Begin at step 3 — what if Jordan secures emergency GCC reserve support?
  Mode 3 branch: increase fiscal multiplier to 1.3 (demand stimulus via Gulf aid)
  Branch trajectory shows the reserve pathway with vs. without the intervention.

Platform principle demonstration:
  The engine, instruments, and UX are invariant between Greece, Argentina, and Jordan.
  Only data inputs change. This is a platform, not a MENA-specific tool.

Usage:
  cd backend
  DATABASE_URL=postgresql://... python scripts/demo_hormuz_jordan.py

  Without DATABASE_URL the script skips gracefully with an explanation.
"""
from __future__ import annotations

import asyncio
import os
import sys
from typing import Any

# Ensure backend root is on path when running as a script
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import httpx

_DATABASE_URL = os.environ.get("DATABASE_URL", "")

_STEP_YEARS = {
    1: "2024", 2: "2025", 3: "2026", 4: "2027",
    5: "2028", 6: "2029", 7: "2030", 8: "2031",
}

_STEP_LABELS = {
    1: "Hormuz disruption / fuel shock",
    2: "Food supply chain disruption",
    3: "Dual shock peak / IMF program",
    4: "IMF conditionality austerity",
    5: "Reserve drawdown critical",
    6: "Hormuz resolution begins",
    7: "Post-shock recovery",
    8: "Stabilization assessment",
}


def _require_db() -> bool:
    if not _DATABASE_URL:
        print(
            "\nDATABASE_URL not set — skipping live demo.\n"
            "\nTo run the full Demo 4 walkthrough:\n"
            "  cd backend\n"
            "  DATABASE_URL=postgresql://user:pass@host:5432/worldsim \\\n"
            "      python scripts/demo_hormuz_jordan.py\n"
            "\nThe database must have the natural_earth_loader seed applied "
            "(JOR and EGY must exist in simulation_entities) and all Alembic "
            "migrations applied.\n"
        )
        return False
    return True


def _print_header() -> None:
    print("\n" + "=" * 80)
    print("WorldSim — Demo 4 (Milestone 12)")
    print("Scenario: Jordan/Egypt Strait of Hormuz Disruption")
    print("=" * 80)
    print(
        "\nSCENARIO OVERVIEW"
        "\n  Step 1 (2024): Hormuz disruption — fuel price shock begins."
        "\n    Jordan bears the highest fuel import dependency in MENA (42%)."
        "\n    Fuel shock effect: JOR 0.105 / EGY 0.058 per step."
        "\n  Step 2 (2025): Food supply chain disruption joins."
        "\n    Egypt faces the highest food import exposure (35% — world's largest wheat importer)."
        "\n    Food shock effect: EGY 0.053 / JOR 0.042 per step."
        "\n  Step 3 (2026): Dual shock peak."
        "\n    Jordan: IMF program engagement triggered by reserve drawdown."
        "\n    Egypt: Emergency declaration — bread subsidy pressure beyond fiscal capacity."
        "\n  Step 4 (2027): IMF conditionality — Jordan austerity during peak shock."
        "\n  Step 5 (2028): Reserve drawdown critical — both economies under stress."
        "\n  Step 6 (2029): Hormuz resolution begins — shocks end."
        "\n  Steps 7–8 (2030–2031): Post-shock recovery and stabilization."
        "\n"
        "\nFRAMEWORK STATUS AT M12"
        "\n  Financial         — composite live (percentile rank; JOR + EGY)"
        "\n  Human Development — composite live (percentile rank; JOR + EGY)"
        "\n  Ecological        — composite live (CO2 boundary proximity; [0.0, 2.0])"
        "\n  Governance        — composite live (normalized_absolute; WGI/V-Dem)"
        "\n"
        "\n  Note: All four composite scores live because scenario has ≥2 entities."
        "\n  This is the first Demo with financial and human_development composites active."
        "\n  (Issue #193 percentile-rank guard lifted for multi-entity scenarios)"
        "\n"
        "\nEXTERNAL SECTOR MODULE (ADR-012)"
        "\n  Fuel shock magnitude 0.25, steps 1–6:"
        "\n    JOR commodity_import_dependency_fuel = 0.42 → shock effect 0.105/step"
        "\n    EGY commodity_import_dependency_fuel = 0.23 → shock effect 0.058/step"
        "\n  Food shock magnitude 0.15, steps 2–6:"
        "\n    JOR commodity_import_dependency_food = 0.28 → shock effect 0.042/step"
        "\n    EGY commodity_import_dependency_food = 0.35 → shock effect 0.053/step"
        "\n  HCL transmission factor 0.3 → bottom-quintile consumption capacity reduced."
        "\n"
        "\nPLATFORM PRINCIPLE"
        "\n  This is the same engine as the Greece and Argentina scenarios."
        "\n  Only data inputs changed. A platform, not a MENA-specific tool."
    )
    print()


def _format_percent(value_str: str | None) -> str:
    if value_str is None:
        return "—"
    try:
        return f"{float(value_str) * 100:+.2f}%"
    except (ValueError, TypeError):
        return "—"


def _format_decimal(value_str: str | None, suffix: str = "") -> str:
    if value_str is None:
        return "—"
    try:
        return f"{float(value_str):.4f}{suffix}"
    except (ValueError, TypeError):
        return "—"


def _format_months(value_str: str | None) -> str:
    if value_str is None:
        return "—"
    try:
        # Floor at 0: negative reserves mean depleted (reserves exhausted, not negative).
        # Engine does not enforce non-negativity — Issue #803.
        return f"{max(0.0, float(value_str)):.1f}mo"
    except (ValueError, TypeError):
        return "—"


def _print_main_table(
    outputs_jor: list[dict[str, Any]],
    outputs_egy: list[dict[str, Any]],
) -> None:
    print("MULTI-FRAMEWORK OUTPUT — Jordan (JOR) and Egypt (EGY) across 8 steps")
    print()
    print("Jordan (JOR) — high fuel import dependency (0.42)")
    print(
        f"  {'Step':<5} {'Year':<6} {'GDP Growth':>12} {'Unemployment':>13} "
        f"{'Reserves':>10} {'Eco Comp':>10} {'Gov Comp':>10}"
    )
    print("  " + "-" * 68)
    for output in outputs_jor:
        _print_entity_row(output)

    print()
    print("Egypt (EGY) — high food import dependency (0.35)")
    print(
        f"  {'Step':<5} {'Year':<6} {'GDP Growth':>12} {'Unemployment':>13} "
        f"{'Reserves':>10} {'Eco Comp':>10} {'Gov Comp':>10}"
    )
    print("  " + "-" * 68)
    for output in outputs_egy:
        _print_entity_row(output)

    print()
    print("Column notes:")
    print("  GDP Growth / Unemployment: raw indicator values")
    print("  Reserves: reserve_coverage_months (MDA CRITICAL floor: 2.5 months)")
    print("  Eco Composite: CO2 boundary proximity [0.0–2.0]. 1.0 = at boundary.")
    print("  Gov Composite: normalized_absolute [0.0–1.0] (WGI Rule of Law + V-Dem LDI).")
    print()


def _print_entity_row(output: dict[str, Any]) -> None:
    step = output["step_index"]
    year = _STEP_YEARS.get(step, f"step{step}")
    label = _STEP_LABELS.get(step, "")

    fin = output["outputs"].get("financial", {})
    hd = output["outputs"].get("human_development", {})
    eco = output["outputs"].get("ecological", {})
    gov = output["outputs"].get("governance", {})

    gdp_val = fin.get("indicators", {}).get("gdp_growth", {}).get("value")
    gdp_str = _format_percent(gdp_val)

    unemp_val = hd.get("indicators", {}).get("unemployment_rate", {}).get("value")
    unemp_str = _format_percent(unemp_val)

    res_val = fin.get("indicators", {}).get("reserve_coverage_months", {}).get("value")
    res_str = _format_months(res_val)

    eco_composite = eco.get("composite_score")
    eco_str = _format_decimal(eco_composite)

    gov_composite = gov.get("composite_score")
    gov_str = _format_decimal(gov_composite)

    suffix = f"  ← {label}" if label else ""
    print(
        f"  {step:<5} {year:<6} {gdp_str:>12} {unemp_str:>13} "
        f"{res_str:>10} {eco_str:>10} {gov_str:>10}{suffix}"
    )


def _print_mda_summary(
    outputs_jor: list[dict[str, Any]],
    outputs_egy: list[dict[str, Any]],
) -> None:
    has_alerts = False

    for entity_label, outputs in [("JOR", outputs_jor), ("EGY", outputs_egy)]:
        for output in outputs:
            step = output["step_index"]
            year = _STEP_YEARS.get(step, f"step{step}")
            all_alerts: list[dict[str, Any]] = []
            for fw_name in ("financial", "human_development", "ecological", "governance"):
                fw_out = output["outputs"].get(fw_name, {})
                all_alerts.extend(fw_out.get("mda_alerts", []))

            if all_alerts:
                if not has_alerts:
                    print("MDA THRESHOLD BREACHES")
                    print("-" * 80)
                    has_alerts = True
                for alert in all_alerts:
                    severity = alert.get("severity", "?")
                    indicator = alert.get("indicator_key", "?")
                    current = alert.get("current_value", "?")
                    floor = alert.get("floor_value", "?")
                    consecutive = alert.get("consecutive_breach_steps", 0)
                    print(
                        f"  Step {step} ({year}) [{entity_label}] [{severity}] {indicator}: "
                        f"current={current} floor={floor} "
                        f"(consecutive: {consecutive} step(s))"
                    )

    if not has_alerts:
        print("MDA THRESHOLD BREACHES")
        print("-" * 80)
        print("  None detected across all 8 steps for JOR and EGY.")

    print()


def _print_divergence_narrative(
    outputs_jor: list[dict[str, Any]],
    outputs_egy: list[dict[str, Any]],
) -> None:
    jor_by_step = {o["step_index"]: o for o in outputs_jor}
    egy_by_step = {o["step_index"]: o for o in outputs_egy}

    print("PRIMARY VISUAL ARGUMENT — Divergent Shock Transmission")
    print("-" * 80)
    print(
        "  [Zone 1A trajectory curves show the crisis arc — point there, not the choropleth."
        "\n   The choropleth anchors the scenario geographically: JOR and EGY in MENA context.]"
    )
    print()

    print("  Step 3 — Dual shock peak (2026):")
    for entity_label, by_step in [("JOR", jor_by_step), ("EGY", egy_by_step)]:
        if 3 not in by_step:
            continue
        output = by_step[3]
        fin = output["outputs"].get("financial", {})
        hd = output["outputs"].get("human_development", {})

        gdp_val = fin.get("indicators", {}).get("gdp_growth", {}).get("value")
        res_val = fin.get("indicators", {}).get("reserve_coverage_months", {}).get("value")
        unemp_val = hd.get("indicators", {}).get("unemployment_rate", {}).get("value")

        print(f"    {entity_label}: GDP {_format_percent(gdp_val)} | "
              f"Reserves {_format_months(res_val)} | "
              f"Unemployment {_format_percent(unemp_val)}")

    print()
    print(
        "  The divergence is the WorldSim thesis:"
        "\n    Jordan (fuel-exposed): reserve drawdown is the primary risk signal."
        "\n    Egypt (food-exposed): unemployment and governance deterioration"
        " are the primary signals."
        "\n    The same external shock reaches different populations through different channels."
        "\n    A finance minister in Amman and a minister in Cairo need different policy responses."
    )
    print()
    print(
        "  Platform principle demonstrated: the Jordan/Egypt arc uses the same engine,"
        "\n  instruments, and UX as the Greece and Argentina fixtures. Only data inputs changed."
    )
    print()


async def _run_demo() -> None:
    from app.db.connection import create_asyncpg_pool
    from app.main import app as _app

    await create_asyncpg_pool()

    _print_header()

    scenario_req_module = __import__(
        "tests.fixtures.jordan_hormuz_scenario",
        fromlist=["build_jordan_hormuz_demo_scenario"],
    )
    build_fn = scenario_req_module.build_jordan_hormuz_demo_scenario
    scenario_req = build_fn()

    print("Creating Demo 4 scenario (JOR + EGY, 8 steps, ExternalSectorModule active)...")
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=_app),
        base_url="http://demo",
    ) as client:
        create_resp = await client.post(
            "/api/v1/scenarios",
            json=scenario_req.model_dump(mode="json"),
        )
        if create_resp.status_code != 201:
            print(
                f"ERROR: Scenario creation failed: "
                f"{create_resp.status_code} {create_resp.text}"
            )
            return

        scenario_id: str = create_resp.json()["scenario_id"]
        print(f"Created scenario: {scenario_id}")

        print("Running 8 steps (fuel shock steps 1–6, food shock steps 2–6)...")
        run_resp = await client.post(f"/api/v1/scenarios/{scenario_id}/run")
        if run_resp.status_code != 200:
            print(
                f"ERROR: Scenario run failed: "
                f"{run_resp.status_code} {run_resp.text}"
            )
            return
        print(f"Status: {run_resp.json()['final_status']}")
        print()

        outputs_jor: list[dict[str, Any]] = []
        outputs_egy: list[dict[str, Any]] = []

        for step in range(1, 9):
            for entity_id, output_list in [("JOR", outputs_jor), ("EGY", outputs_egy)]:
                mf_resp = await client.get(
                    f"/api/v1/scenarios/{scenario_id}/measurement-output",
                    params={"entity_id": entity_id, "step": step},
                )
                if mf_resp.status_code != 200:
                    print(
                        f"WARNING: Measurement output unavailable at step {step} "
                        f"for {entity_id}: {mf_resp.status_code}"
                    )
                    continue
                output_list.append(mf_resp.json())

        _print_main_table(outputs_jor, outputs_egy)
        _print_mda_summary(outputs_jor, outputs_egy)
        _print_divergence_narrative(outputs_jor, outputs_egy)

        all_outputs = outputs_jor + outputs_egy
        if all_outputs:
            eco_note = all_outputs[0]["outputs"].get("ecological", {}).get("note", "")
            if eco_note:
                print("ECOLOGICAL DISCLOSURE")
                print("-" * 80)
                print(f"  {eco_note}")
                print()
            ia1 = all_outputs[0].get("ia1_disclosure", "")
            if ia1:
                print("IA-1 DISCLOSURE")
                print("-" * 80)
                print(f"  {ia1}")
                print()

        print("Cleaning up demo scenario...")
        await client.delete(f"/api/v1/scenarios/{scenario_id}")
        print("Done.")


def main() -> None:
    """Run the Jordan/Egypt Demo 4 Strait of Hormuz disruption walkthrough."""
    if not _require_db():
        return
    asyncio.run(_run_demo())


if __name__ == "__main__":
    main()
