"""M8 Demo: Greece 2010–2015 Multi-Framework Measurement.

Demonstrates the WorldSim M8 milestone deliverable: all four radar chart
axes rendered simultaneously for a real historical scenario. The Greece
2010–2015 IMF program is the end-of-milestone demo case.

Primary visual argument:
  GDP growth turns positive at step 5 (2014 brief recovery) while
  unemployment remains at historically elevated levels — financial
  "recovery" is not the same as recovery. The divergence between
  financial and human development indicators is the WorldSim thesis
  made visible. No single-axis lens can see both simultaneously.

Framework status at M8:
  Financial        — indicators live; composite null (single-entity scenario)
  Human Development — indicators live; composite null (single-entity scenario)
  Ecological       — composite live (CO2 boundary proximity; land-use not active
                     before 2023-09-13, per ADR-005 Amendment 3 Q1 disposition)
  Governance       — null / "in validation" (deferred to M9, Decision M8-4)

Single-entity note (Issue #193, ADR-005 M8-2):
  The Greece scenario contains exactly one entity (GRC). The percentile-rank
  composite strategy requires ≥2 entities to be meaningful, so financial and
  human_development composite scores are null with single_entity_warning=True.
  This is correct behaviour, not a bug. The ecological composite is exempt from
  this guard because boundary proximity is physically meaningful for a single
  entity regardless of population size.

Usage:
  cd backend
  DATABASE_URL=postgresql://... python scripts/demo_greece_2010_2015.py

  Without DATABASE_URL the script skips gracefully with an explanation.
"""
from __future__ import annotations

import asyncio
import os
import sys
from decimal import Decimal
from typing import Any

# Ensure backend root is on path when running as a script
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import httpx

_DATABASE_URL = os.environ.get("DATABASE_URL", "")


def _require_db() -> bool:
    if not _DATABASE_URL:
        print(
            "\nDATABASE_URL not set — skipping live demo.\n"
            "\nTo run the full M8 demo:\n"
            "  cd backend\n"
            "  DATABASE_URL=postgresql://user:pass@host:5432/worldsim \\\n"
            "      python scripts/demo_greece_2010_2015.py\n"
            "\nThe database must have the natural_earth_loader seed applied "
            "(GRC must exist in simulation_entities) and the Alembic migrations "
            "through c1a4e7f2d9b3 and d2b5f8a3e6c4 must be applied.\n"
        )
        return False
    return True


def _print_header() -> None:
    print("\n" + "=" * 80)
    print("WorldSim — Milestone 8 Demo")
    print("Scenario: Greece 2010–2015 IMF Program — Multi-Framework Measurement")
    print("=" * 80)
    print(
        "\nSCENARIO OVERVIEW"
        "\n  Steps 1–3 (2010–2012): acute crisis — fiscal consolidation,"
        "\n    GDP contraction, MDA threshold breach on reserve coverage."
        "\n  Steps 4–6 (2013–2015): stabilization divergence — financial"
        "\n    indicators recover toward primary surplus target while human"
        "\n    development indicators remain depressed or continue falling."
        "\n"
        "\nFRAMEWORK STATUS AT M8"
        "\n  Financial         — indicators live (gdp_growth, reserve_coverage_months)"
        "\n  Human Development — indicators live (unemployment_rate, health_expenditure,"
        "\n                      net_enrollment_secondary)"
        "\n  Ecological        — composite live (CO2 boundary proximity; [0.0, 2.0])"
        "\n  Governance        — null / 'in validation' (deferred to M9)"
        "\n"
        "\n  Note: financial and human_development composites are null because"
        "\n  GRC is a single-entity scenario. Percentile rank requires ≥2 entities."
        "\n  (Issue #193, ADR-005 Decision M8-2)"
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
    step_years = {1: "2010", 2: "2011", 3: "2012", 4: "2013", 5: "2014", 6: "2015"}

    print("MULTI-FRAMEWORK OUTPUT — Greece (GRC) across 6 steps")
    print()
    print(
        f"{'Step':<5} {'Year':<6} {'GDP Growth':>12} {'Unemployment':>13} "
        f"{'Eco Composite':>14} {'Gov':>9}"
    )
    print("-" * 64)

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

        gov_str = "— (M9)"

        print(
            f"{step:<5} {year:<6} {gdp_str:>12} {unemp_str:>13} "
            f"{eco_str:>14} {gov_str:>9}"
        )

    print()
    print("Column notes:")
    print("  GDP Growth / Unemployment: raw indicator values (not composite scores)")
    print(
        "  Eco Composite: mean CO2 boundary proximity [0.0–2.0]."
        " 1.0 = at boundary; >1.0 = boundary exceeded."
    )
    print("  Gov: null — GovernanceModule deferred to M9")
    print()


def _print_mda_summary(outputs: list[dict[str, Any]]) -> None:
    step_years = {1: "2010", 2: "2011", 3: "2012", 4: "2013", 5: "2014", 6: "2015"}
    has_alerts = False

    for output in outputs:
        step = output["step_index"]
        year = step_years.get(step, f"step{step}")
        all_alerts: list[dict[str, Any]] = []
        for fw_name in ("financial", "human_development", "ecological"):
            fw_out = output["outputs"].get(fw_name, {})
            all_alerts.extend(fw_out.get("mda_alerts", []))

        if all_alerts:
            if not has_alerts:
                print("MDA THRESHOLD BREACHES")
                print("-" * 64)
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
        print("-" * 64)
        print("  None detected across all 6 steps.")

    print()


def _print_divergence_narrative(outputs: list[dict[str, Any]]) -> None:
    outputs_by_step = {o["step_index"]: o for o in outputs}

    print("PRIMARY VISUAL ARGUMENT — The Divergence")
    print("-" * 64)

    for step in [3, 5, 6]:
        year = {3: "2012", 5: "2014", 6: "2015"}.get(step, f"step{step}")
        if step not in outputs_by_step:
            continue
        output = outputs_by_step[step]
        fin = output["outputs"].get("financial", {})
        hd = output["outputs"].get("human_development", {})

        gdp_val = fin.get("indicators", {}).get("gdp_growth", {}).get("value")
        unemp_val = hd.get("indicators", {}).get("unemployment_rate", {}).get("value")

        gdp_str = _format_percent(gdp_val)
        unemp_str = _format_percent(unemp_val).lstrip("+")

        label = {
            3: "Trough (2012 step 3)",
            5: "Brief recovery (2014 step 5)",
            6: "Capital controls (2015 step 6)",
        }.get(step, f"Step {step}")

        print(f"  {label}:")
        print(f"    GDP growth:       {gdp_str}")
        print(f"    Unemployment:     {unemp_str}")
        try:
            if gdp_val and unemp_val:
                gdp_f = float(gdp_val)
                unemp_f = float(unemp_val)
                if step == 5 and gdp_f > 0 and unemp_f > 0.2:
                    print(
                        "    → Financial indicator positive while unemployment "
                        "remains above 20%."
                    )
                    print(
                        "      This is the divergence: financial 'recovery' is not the "
                        "same as recovery."
                    )
        except (ValueError, TypeError):
            pass
        print()

    print(
        "The flight simulator thesis: a finance minister needs both axes visible"
        "\nsimultaneously. A single-axis instrument misses half the picture."
    )
    print()


async def _run_demo() -> None:
    from app.main import app as _app

    _print_header()

    scenario_req_module = __import__(
        "tests.fixtures.greece_2010_scenario",
        fromlist=["build_greece_demo_scenario"],
    )
    build_fn = scenario_req_module.build_greece_demo_scenario
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

        print("Running 6 steps...")
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
        for step in range(1, 7):
            mf_resp = await client.get(
                f"/api/v1/scenarios/{scenario_id}/measurement-output",
                params={"entity_id": "GRC", "step": step},
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
                print("-" * 64)
                print(f"  {eco_note}")
                print()
            ia1 = outputs[0].get("ia1_disclosure", "")
            if ia1:
                print("IA-1 DISCLOSURE")
                print("-" * 64)
                print(f"  {ia1}")
                print()

        print("Cleaning up demo scenario...")
        await client.delete(f"/api/v1/scenarios/{scenario_id}")
        print("Done.")


def main() -> None:
    """Run the Greece 2010–2015 M8 multi-framework demo."""
    if not _require_db():
        return
    asyncio.run(_run_demo())


if __name__ == "__main__":
    main()
