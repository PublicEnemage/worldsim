"""Fidelity report formatter for WorldSim backtesting runs.

Produces a human-readable report for CI log output. The report is printed
regardless of pass/fail so that fidelity data appears in every CI execution
and can be tracked across milestones.
"""
from __future__ import annotations

from datetime import datetime, timezone
from decimal import Decimal
from typing import Any


def format_fidelity_report(
    scenario_name: str,
    actuals: Any,  # noqa: ANN401 — accepts any actuals dataclass
    snapshots: list[dict[str, Any]],
    thresholds_met: dict[str, bool],
    ia1_disclosure: str,
    parameter_calibration_disclosure: str,
    entity_id: str = "GRC",
) -> str:
    """Return a formatted fidelity report string for CI log output.

    Args:
        scenario_name: Human-readable name of the backtesting scenario.
        actuals: Historical actuals dataclass (any object with gdp_growth_* attrs).
        snapshots: List of snapshot dicts from GET /scenarios/{id}/snapshots.
            Each dict has 'step', 'timestep', and 'state_data'.
        thresholds_met: Dict mapping threshold_name → bool for each checked
            threshold. All thresholds are reported regardless of result.
        ia1_disclosure: Canonical IA-1 text from quantity_serde.
        parameter_calibration_disclosure: Calibration limitation text.
        entity_id: ISO 3166-1 alpha-3 entity to read from snapshots. Default "GRC".

    Returns:
        Multi-line string suitable for print() or sys.stdout.write().
    """
    now = datetime.now(timezone.utc).isoformat()  # noqa: UP017
    lines: list[str] = [
        "=" * 72,
        "WORLDSIM BACKTESTING FIDELITY REPORT",
        "=" * 72,
        f"Scenario : {scenario_name}",
        f"Run at   : {now}",
        f"Snapshots: {len(snapshots)} steps",
        "",
        "THRESHOLD TYPE: DIRECTION_ONLY",
        "(Magnitude accuracy not asserted — see Known Limitations below)",
        "",
        "-" * 72,
        "SIMULATED VALUES vs HISTORICAL ACTUALS",
        "-" * 72,
    ]

    snapshots_by_step = {s["step"]: s for s in snapshots}

    # Determine step range from snapshots (exclude step 0 / initial state)
    sim_steps = sorted(k for k in snapshots_by_step if k > 0)

    for step_num in sim_steps:
        snap = snapshots_by_step.get(step_num)
        lines.append(f"\nStep {step_num}:")

        if snap is None:
            lines.append("  [no snapshot at this step]")
            continue

        state_data = snap.get("state_data", {})
        entity_attrs = state_data.get(entity_id, {})

        gdp_envelope = entity_attrs.get("gdp_growth", {})
        sim_gdp = gdp_envelope.get("value", "N/A")
        lines.append(f"  gdp_growth   simulated={sim_gdp:>10}")

        unemp_envelope = entity_attrs.get("unemployment_rate", {})
        if unemp_envelope:
            sim_unemp = unemp_envelope.get("value", "N/A")
            lines.append(f"  unemployment simulated={sim_unemp:>10}")

    lines += [
        "",
        "-" * 72,
        "THRESHOLD RESULTS",
        "-" * 72,
    ]

    all_passed = True
    for threshold_name, passed in sorted(thresholds_met.items()):
        status = "PASS" if passed else "FAIL"
        if not passed:
            all_passed = False
        lines.append(f"  [{status}] {threshold_name}")

    overall = "PASS" if all_passed else "FAIL"
    lines += [
        "",
        f"Overall: {overall} ({sum(thresholds_met.values())}/{len(thresholds_met)} thresholds met)",
        "",
        "-" * 72,
        "KNOWN LIMITATIONS",
        "-" * 72,
        f"IA-1: {ia1_disclosure}",
        "",
        f"Calibration: {parameter_calibration_disclosure}",
        "=" * 72,
    ]

    return "\n".join(lines)


def _extract_gdp_value(
    snapshot: dict[str, Any], entity_id: str = "GRC"
) -> Decimal | None:
    """Extract the gdp_growth Decimal value for entity_id from a snapshot dict."""
    try:
        val = snapshot["state_data"][entity_id]["gdp_growth"]["value"]
        return Decimal(str(val))
    except (KeyError, TypeError, ValueError):
        return None


def _extract_unemployment_value(
    snapshot: dict[str, Any], entity_id: str = "GRC"
) -> Decimal | None:
    """Extract the unemployment_rate Decimal value for entity_id from a snapshot dict."""
    try:
        val = snapshot["state_data"][entity_id]["unemployment_rate"]["value"]
        return Decimal(str(val))
    except (KeyError, TypeError, ValueError):
        return None
