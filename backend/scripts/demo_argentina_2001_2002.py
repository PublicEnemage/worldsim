"""Demo 3: Argentina 2001–2002 Crisis Arc and Kirchner Recovery.

Demonstrates the WorldSim M10 milestone deliverable: all four Zone 1 axes live
with a second country fixture. The Argentina 2001–2002 sovereign default is the
Demo 3 case, complementing the Greece 2010–2015 Demo 2 case.

Primary visual argument:
  Argentina's IMF program and Zero Deficit Plan produced the largest sovereign
  default in history at the time (December 2001, USD 81.8bn). Unemployment
  peaked at 21.5% in 2002 while the economy contracted 10.9%. The Kirchner
  recovery (2003+) restored GDP growth without restoring governance quality —
  the divergence between financial recovery and institutional resilience is
  the WorldSim thesis made visible across a second geopolitical context.

Framework status at M10:
  Financial        — indicators live; composite null (single-entity scenario, Issue #193)
  Human Development — indicators live; composite null (single-entity scenario, Issue #193)
  Ecological       — composite live (CO2 boundary proximity; [0.0, 2.0])
  Governance       — composite live (normalized_absolute; WGI + V-Dem; ADR-005 Amendment 4)

Platform principle demonstration:
  The engine, instruments, and UX are invariant between the Greece and Argentina
  fixtures. Only data inputs change. This is a platform, not a Greece-specific tool.

Usage:
  cd backend
  DATABASE_URL=postgresql://... python scripts/demo_argentina_2001_2002.py

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


def _require_db() -> bool:
    if not _DATABASE_URL:
        print(
            "\nDATABASE_URL not set — skipping live demo.\n"
            "\nTo run the full Demo 3 walkthrough:\n"
            "  cd backend\n"
            "  DATABASE_URL=postgresql://user:pass@host:5432/worldsim \\\n"
            "      python scripts/demo_argentina_2001_2002.py\n"
            "\nThe database must have the natural_earth_loader seed applied "
            "(ARG must exist in simulation_entities) and all Alembic migrations applied.\n"
        )
        return False
    return True


def _print_header() -> None:
    print("\n" + "=" * 80)
    print("WorldSim — Demo 3 (Milestone 10)")
    print("Scenario: Argentina 2001–2002 Crisis Arc and Kirchner Recovery")
    print("=" * 80)
    print(
        "\nSCENARIO OVERVIEW"
        "\n  Step 1 (2001): Zero Deficit Plan — pro-cyclical fiscal adjustment."
        "\n    Finance Minister Cavallo cuts federal spending ~6.5% of GDP."
        "\n    IMF Blindaje (USD 39.7bn) fails to restore market confidence."
        "\n  Step 2 (2002): Default declaration (December 2001, USD 81.8bn)."
        "\n    Pesification and devaluation end the convertibility era."
        "\n    Unemployment peaks at 21.5%."
        "\n  Step 3 (2003): Kirchner recovery begins."
        "\n    GDP rebounds 8.8% under heterodox policies."
        "\n  Step 4 (2004): Growth consolidation — 9.0% GDP growth."
        "\n"
        "\nFRAMEWORK STATUS AT M10"
        "\n  Financial         — indicators live (gdp_growth, unemployment_rate)"
        "\n  Human Development — indicators live (unemployment_rate)"
        "\n  Ecological        — composite live (CO2 boundary proximity; [0.0, 2.0])"
        "\n  Governance        — composite live (normalized_absolute; WGI/V-Dem)"
        "\n"
        "\n  Note: financial and human_development composites are null because"
        "\n  ARG is a single-entity scenario. Percentile rank requires ≥2 entities."
        "\n  (Issue #193, ADR-005 Decision M8-2)"
        "\n"
        "\nPLATFORM PRINCIPLE"
        "\n  This is the same engine as the Greece scenario. Only data inputs changed."
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


def _print_main_table(outputs: list[dict[str, Any]]) -> None:
    step_years = {1: "2001", 2: "2002", 3: "2003", 4: "2004"}
    step_labels = {
        1: "Zero Deficit Plan / Blindaje",
        2: "Default / Peso devaluation",
        3: "Kirchner recovery begins",
        4: "Growth consolidation",
    }

    print("MULTI-FRAMEWORK OUTPUT — Argentina (ARG) across 4 steps")
    print()
    print(
        f"{'Step':<5} {'Year':<6} {'GDP Growth':>12} {'Unemployment':>13} "
        f"{'Eco Composite':>14} {'Gov Composite':>14}"
    )
    print("-" * 70)

    for output in outputs:
        step = output["step_index"]
        year = step_years.get(step, f"step{step}")

        fin = output["outputs"].get("financial", {})
        hd = output["outputs"].get("human_development", {})
        eco = output["outputs"].get("ecological", {})
        gov = output["outputs"].get("governance", {})

        gdp_val = fin.get("indicators", {}).get("gdp_growth", {}).get("value")
        gdp_str = _format_percent(gdp_val)

        unemp_val = hd.get("indicators", {}).get("unemployment_rate", {}).get("value")
        unemp_str = _format_percent(unemp_val)

        eco_composite = eco.get("composite_score")
        eco_str = _format_decimal(eco_composite)

        gov_composite = gov.get("composite_score")
        gov_str = _format_decimal(gov_composite)

        label = step_labels.get(step, "")
        print(
            f"{step:<5} {year:<6} {gdp_str:>12} {unemp_str:>13} "
            f"{eco_str:>14} {gov_str:>14}  ← {label}"
        )

    print()
    print("Column notes:")
    print("  GDP Growth / Unemployment: raw indicator values (not composite scores)")
    print(
        "  Eco Composite: CO2 boundary proximity [0.0–2.0]."
        " 1.0 = at boundary; >1.0 = boundary exceeded."
    )
    print("  Gov Composite: normalized_absolute [0.0–1.0] (WGI Rule of Law + V-Dem LDI).")
    print()


def _print_mda_summary(outputs: list[dict[str, Any]]) -> None:
    step_years = {1: "2001", 2: "2002", 3: "2003", 4: "2004"}
    has_alerts = False

    for output in outputs:
        step = output["step_index"]
        year = step_years.get(step, f"step{step}")
        all_alerts: list[dict[str, Any]] = []
        for fw_name in ("financial", "human_development", "ecological", "governance"):
            fw_out = output["outputs"].get(fw_name, {})
            all_alerts.extend(fw_out.get("mda_alerts", []))

        if all_alerts:
            if not has_alerts:
                print("MDA THRESHOLD BREACHES")
                print("-" * 70)
                has_alerts = True
            for alert in all_alerts:
                severity = alert.get("severity", "?")
                indicator = alert.get("indicator_key", "?")
                current = alert.get("current_value", "?")
                floor = alert.get("floor_value", "?")
                consecutive = alert.get("consecutive_breach_steps", 0)
                print(
                    f"  Step {step} ({year}) [{severity}] {indicator}: "
                    f"current={current} floor={floor} "
                    f"(consecutive: {consecutive} step(s))"
                )

    if not has_alerts:
        print("MDA THRESHOLD BREACHES")
        print("-" * 70)
        print("  None detected across all 4 steps.")

    print()


def _print_divergence_narrative(outputs: list[dict[str, Any]]) -> None:
    # Narration discipline (UX-RULING-4 / Issue #628):
    # The choropleth is a geographic anchor — do NOT narrate it as the change instrument.
    # Route quantitative change to Zone 1A trajectory curves and Zone 1D composite scores.
    # Correct:   "Watch the trajectory curves — governance composite declining at step 3"
    # Incorrect: "Watch Argentina shift in the choropleth as the crisis accumulates"
    outputs_by_step = {o["step_index"]: o for o in outputs}

    print("PRIMARY VISUAL ARGUMENT — The Divergence")
    print("-" * 70)
    print("  [Zone 1A trajectory curves show the crisis arc — point there, not the choropleth.")
    print("   The choropleth anchors the scenario geographically: ARG in the global distribution.]")
    print()

    for step in [2, 3, 4]:
        if step not in outputs_by_step:
            continue
        output = outputs_by_step[step]
        fin = output["outputs"].get("financial", {})
        hd = output["outputs"].get("human_development", {})
        gov = output["outputs"].get("governance", {})

        gdp_val = fin.get("indicators", {}).get("gdp_growth", {}).get("value")
        unemp_val = hd.get("indicators", {}).get("unemployment_rate", {}).get("value")
        gov_composite = gov.get("composite_score")

        gdp_str = _format_percent(gdp_val)
        unemp_str = (_format_percent(unemp_val) or "—").lstrip("+")
        gov_str = _format_decimal(gov_composite)

        label = {
            2: "Default (2002 step 2)",
            3: "Kirchner recovery (2003 step 3)",
            4: "Consolidation (2004 step 4)",
        }.get(step, f"Step {step}")

        print(f"  {label}:")
        print(f"    GDP growth:         {gdp_str}")
        print(f"    Unemployment:       {unemp_str}")
        print(f"    Gov composite:      {gov_str}")
        try:
            if gdp_val and unemp_val:
                gdp_f = float(gdp_val)
                unemp_f = float(unemp_val)
                if step == 3 and gdp_f > 0 and unemp_f > 0.15:
                    print(
                        "    → Financial recovery positive while unemployment"
                        " remains above 15%."
                    )
                    print(
                        "      GDP growth is not the same as recovery."
                        " The human cost ledger tells a different story."
                    )
        except (ValueError, TypeError):
            pass
        print()

    print(
        "Platform principle demonstrated: the Argentina arc uses the same engine,"
        "\ninstruments, and UX as the Greece fixture. Only data inputs changed."
    )
    print()


async def _run_demo() -> None:
    from app.db.connection import create_asyncpg_pool
    from app.main import app as _app

    await create_asyncpg_pool()

    _print_header()

    scenario_req_module = __import__(
        "tests.fixtures.argentina_2001_2002_scenario",
        fromlist=["build_argentina_demo_scenario"],
    )
    build_fn = scenario_req_module.build_argentina_demo_scenario
    scenario_req = build_fn()

    print("Creating demo scenario...")
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

        print("Running 4 steps...")
        run_resp = await client.post(f"/api/v1/scenarios/{scenario_id}/run")
        if run_resp.status_code != 200:
            print(
                f"ERROR: Scenario run failed: "
                f"{run_resp.status_code} {run_resp.text}"
            )
            return
        print(f"Status: {run_resp.json()['final_status']}")
        print()

        outputs: list[dict[str, Any]] = []
        for step in range(1, 5):
            mf_resp = await client.get(
                f"/api/v1/scenarios/{scenario_id}/measurement-output",
                params={"entity_id": "ARG", "step": step},
            )
            if mf_resp.status_code != 200:
                print(
                    f"WARNING: Measurement output unavailable at step {step}: "
                    f"{mf_resp.status_code}"
                )
                continue
            outputs.append(mf_resp.json())

        _print_main_table(outputs)
        _print_mda_summary(outputs)
        _print_divergence_narrative(outputs)

        if outputs:
            eco_note = outputs[0]["outputs"].get("ecological", {}).get("note", "")
            if eco_note:
                print("ECOLOGICAL DISCLOSURE")
                print("-" * 70)
                print(f"  {eco_note}")
                print()
            ia1 = outputs[0].get("ia1_disclosure", "")
            if ia1:
                print("IA-1 DISCLOSURE")
                print("-" * 70)
                print(f"  {ia1}")
                print()

        print("Cleaning up demo scenario...")
        await client.delete(f"/api/v1/scenarios/{scenario_id}")
        print("Done.")


def main() -> None:
    """Run the Argentina 2001–2002 Demo 3 crisis arc walkthrough."""
    if not _require_db():
        return
    asyncio.run(_run_demo())


if __name__ == "__main__":
    main()
