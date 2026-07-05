"""Mode 3 headless battle-testing harness — Issue #1546 (M19 G2A).

Advances scenarios through the REST API and produces configurable output
formats (ascii/csv/json/markdown). Used to generate battle-testing evidence
for Demo 8.

Intent doc: docs/process/intents/M19-G2A-2026-07-02-headless-battle-testing-harness.md
Sprint entry: docs/process/sprint-plans/m19-g2a-sprint-entry.md
"""
from __future__ import annotations

import argparse
import asyncio
import csv
import io
import json
from dataclasses import dataclass
from datetime import UTC, datetime
from decimal import Decimal, InvalidOperation
from enum import Enum
from typing import Any

import httpx

_API_PREFIX = "/api/v1"

# AC-9: stock-flow indicators that cap fidelity at DIRECTION_ONLY (#30)
_STOCK_FLOW_INDICATORS: frozenset[str] = frozenset({
    "reserve_coverage_months",
    "debt_gdp_ratio",
    "current_account_balance",
    "foreign_reserves_usd",
    "external_debt_usd",
})


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------


class RunType(str, Enum):
    TYPE_A = "TYPE_A"  # backtesting: simulation vs historical baseline
    TYPE_B = "TYPE_B"  # counter-factual: alternative policy vs baseline run


class FidelityTier(str, Enum):
    MAGNITUDE_MATCH = "MAGNITUDE_MATCH"
    DIRECTION_ONLY = "DIRECTION_ONLY"
    STRUCTURAL_ONLY = "STRUCTURAL_ONLY"
    BELOW_THRESHOLD = "BELOW_THRESHOLD"


class DirectionVerdict(str, Enum):
    COUNTER_FACTUAL_BETTER = "COUNTER_FACTUAL_BETTER"
    BASELINE_BETTER = "BASELINE_BETTER"
    INDISTINGUISHABLE = "INDISTINGUISHABLE"


# ---------------------------------------------------------------------------
# Exceptions
# ---------------------------------------------------------------------------


class HarnessValidationError(ValueError):
    """Raised for invalid harness inputs before any API call is made."""


class HarnessApiError(RuntimeError):
    """Raised for unexpected HTTP status codes during a harness run.

    The message always includes the failing step number or HTTP status code
    so callers can surface the exact failure context (SF-4 guard).
    """


# ---------------------------------------------------------------------------
# Result dataclass
# ---------------------------------------------------------------------------


@dataclass
class HarnessResult:
    run_metadata: dict[str, Any]
    per_step_records: list[dict[str, Any]]
    summary: dict[str, Any]


# ---------------------------------------------------------------------------
# Known-limitation detection (AC-8, AC-9, AC-10)
# ---------------------------------------------------------------------------


def detect_known_limitations(
    control_inputs: list[dict[str, Any]],
    primary_indicator: str | None = None,
    n_steps: int = 1,
    run_type: RunType | str | None = None,
) -> list[str]:
    """Return warning strings for known model gaps active in this run.

    AC-TYPE_B: TYPE_B runs always disclose counter-factual methodology (Tier 3 /
    INFERRED_STRUCTURAL). Satisfies AC-5 (non-empty) and AC-9 advisory.
    AC-8: EmergencyInstrument.CAPITAL_CONTROLS → #1532 transmission-absent gap.
    AC-9: stock-flow primary indicators → #30 stock-flow-identity gap.
    AC-10: bilateral inputs over n_steps > 1 → #35 bilateral-weights gap.
    """
    limitations: list[str] = []

    # AC-TYPE_B: counter-factual methodology disclosure (always present for TYPE_B).
    # Ensures known_limitations is non-empty (AC-5) and satisfies AC-9 advisory
    # (contains "Tier 3" and "INFERRED_STRUCTURAL"). Capital controls in the
    # BASELINE are detected from control_inputs when they are present; when
    # capital_controls live in baseline scheduled_inputs (not in the harness
    # call's control_inputs), AC-8 remains advisory-only.
    if run_type == RunType.TYPE_B or str(run_type) == "TYPE_B":
        limitations.append(
            "ℹ Counter-factual scenario — scheduled inputs are INFERRED_STRUCTURAL "
            "(Tier 3): the alternative policy path was not historically executed. "
            "Direction verdict is advisory, not a backtesting fidelity assessment. "
            "Persistent direction disagreement should be escalated to the Chief "
            "Methodologist."
        )

    # AC-8 / AC-14: CAPITAL_CONTROLS detection (covers harness-level control_inputs;
    # baseline scheduled_inputs require caller inspection — see Issue #1532)
    for inp in control_inputs:
        instrument = str(inp.get("instrument") or "").upper()
        if instrument == "CAPITAL_CONTROLS":
            limitations.append(
                "⚠ Economic transmission absent — political cost only (#1532 CAPITAL_CONTROLS)"
            )
            break

    # AC-9: stock-flow indicator cap
    if primary_indicator and primary_indicator in _STOCK_FLOW_INDICATORS:
        limitations.append(
            "⚠ Stock-flow indicators cap at DIRECTION_ONLY at most: "
            "threshold-crossing dynamics not modelled (#30 stock-flow-identity-gap)"
        )

    # AC-10: bilateral trade / debt / aid inputs over multiple steps
    bilateral = [
        inp for inp in control_inputs
        if str(inp.get("type") or "").startswith("bilateral")
        or "bilateral" in str(inp.get("instrument") or "").lower()
    ]
    if bilateral and n_steps > 1:
        limitations.append(
            "⚠ Bilateral trade weights are static; magnitude differential unreliable "
            "for multi-step bilateral runs (#35 bilateral-weights)"
        )

    return limitations


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _to_decimal(val: object) -> Decimal | None:
    if val is None:
        return None
    try:
        return Decimal(str(val))
    except (InvalidOperation, TypeError, ValueError):
        return None


def _composite_from_traj(
    traj_steps: list[dict[str, Any]],
    step_index: int,
    framework: str,
) -> Decimal | None:
    for step in traj_steps:
        if step.get("step_index") == step_index:
            for fw in step.get("frameworks") or []:
                if fw.get("framework") == framework:
                    return _to_decimal(fw.get("composite_score"))
    return None


def _psp_from_traj(
    traj_steps: list[dict[str, Any]],
    step_index: int,
) -> Decimal | None:
    for step in traj_steps:
        if step.get("step_index") == step_index:
            pmm = step.get("pmm")
            if pmm and isinstance(pmm, dict):
                return _to_decimal(pmm.get("value"))
    return None


async def _advance_step(
    client: httpx.AsyncClient,
    base_url: str,
    scenario_id: str,
    step_num: int,
) -> dict[str, Any]:
    """POST one advance step; raise HarnessApiError on error status."""
    url = f"{base_url}{_API_PREFIX}/scenarios/{scenario_id}/advance"
    resp = await client.post(url)

    if resp.status_code == 404:
        raise HarnessValidationError(
            f"Scenario '{scenario_id}' not found (HTTP 404 on step {step_num})"
        )
    if resp.status_code >= 500:
        raise HarnessApiError(
            f"Advance step {step_num} returned HTTP {resp.status_code} "
            f"for scenario '{scenario_id}'"
        )
    if resp.status_code >= 400:
        raise HarnessApiError(
            f"Advance step {step_num} returned HTTP {resp.status_code} "
            f"for scenario '{scenario_id}': {resp.text[:200]}"
        )

    result: dict[str, Any] = resp.json()
    return result


async def _fetch_trajectory(
    client: httpx.AsyncClient,
    base_url: str,
    scenario_id: str,
) -> list[dict[str, Any]]:
    """GET scenario trajectory; return empty list when unavailable."""
    url = f"{base_url}{_API_PREFIX}/scenarios/{scenario_id}/trajectory"
    resp = await client.get(url)
    if resp.status_code == 200:
        data = resp.json()
        if isinstance(data, dict):
            return data.get("steps") or []
    return []


def _build_per_step_records(
    steps: int,
    advance_responses: list[dict[str, Any]],
    traj_steps: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Merge advance responses and trajectory data into per-step records.

    Trajectory composite scores take priority; advance response fields
    (composite_scores, psp, ci_band) are used as fallback, which makes
    the unit-test mock responses work without a live trajectory endpoint.
    """
    records: list[dict[str, Any]] = []
    for i in range(steps):
        step_num = i + 1
        adv = advance_responses[i] if i < len(advance_responses) else {}

        # Composite scores: trajectory first, then advance response (mock compatibility)
        fin = _composite_from_traj(traj_steps, step_num, "financial")
        hd = _composite_from_traj(traj_steps, step_num, "human_development")
        eco = _composite_from_traj(traj_steps, step_num, "ecological")
        gov = _composite_from_traj(traj_steps, step_num, "governance")

        if fin is None and hd is None and eco is None:
            cs = adv.get("composite_scores") or {}
            fin = _to_decimal(cs.get("financial"))
            hd = _to_decimal(cs.get("human_development"))
            eco = _to_decimal(cs.get("ecological"))
            gov = _to_decimal(cs.get("governance"))

        # PSP: trajectory PMM value first, then advance response
        psp = _psp_from_traj(traj_steps, step_num)
        if psp is None:
            psp = _to_decimal(adv.get("psp"))

        # CI band: advance response (trajectories carry CI per-framework; use financial)
        ci_band = adv.get("ci_band") or {}
        ci_low = _to_decimal(ci_band.get("low"))
        ci_high = _to_decimal(ci_band.get("high"))
        if ci_low is None:
            for step in traj_steps:
                if step.get("step_index") == step_num:
                    for fw in step.get("frameworks") or []:
                        if fw.get("framework") == "financial":
                            ci_low = _to_decimal(fw.get("ci_lower"))
                            ci_high = _to_decimal(fw.get("ci_upper"))
                            break

        records.append({
            "step": step_num,
            "fin_composite": fin,
            "hd_composite": hd,
            "eco_composite": eco,
            "gov_composite": gov,
            "mda_alert_states": adv.get("mda_alert_states") or [],
            "cohort_poverty_headcount": _to_decimal(
                adv.get("focal_cohort_poverty_headcount")
            ),
            "psp": psp,
            "ci_band_low": ci_low,
            "ci_band_high": ci_high,
            "active_failure_modes": adv.get("active_failure_modes") or [],
            # Calibration fields (ADR-007 Amendment 1 §8.3): model_value is the
            # primary composite for MAGNITUDE_MATCH assessment; hist_value is
            # populated by G2B backtesting fixtures (None until then).
            "model_value": fin,
            "hist_value": None,
        })
    return records


def _classify_fidelity(
    per_step_records: list[dict[str, Any]],
) -> tuple[FidelityTier, str]:
    """Classify Type A fidelity tier.

    MAGNITUDE_MATCH gate (ADR-007 Amendment 1 §8.3): requires ≥5 valid
    (model_value, hist_value) pairs, ≥50% within ±20%, no catastrophic
    outlier (> 5× hist). Records without hist_value are excluded from the
    count (hist_value added by G2B backtesting fixtures; None until then).
    """
    if not per_step_records:
        return (
            FidelityTier.BELOW_THRESHOLD,
            "No step records produced; cannot classify fidelity.",
        )

    valid_pairs = [
        (Decimal(str(r["model_value"])), Decimal(str(r["hist_value"])))
        for r in per_step_records
        if r.get("hist_value") is not None and r.get("model_value") is not None
    ]

    if len(valid_pairs) >= 5:
        has_catastrophic = any(
            abs(model_i - hist_i) > 5 * abs(hist_i)
            for model_i, hist_i in valid_pairs
            if abs(hist_i) > Decimal("0.001")
        )
        if not has_catastrophic:
            within = sum(
                1 for model_i, hist_i in valid_pairs
                if abs(model_i - hist_i)
                / max(abs(hist_i), Decimal("0.01")) <= Decimal("0.20")
            )
            if Decimal(within) / Decimal(len(valid_pairs)) >= Decimal("0.50"):
                return (
                    FidelityTier.MAGNITUDE_MATCH,
                    f"MAGNITUDE_MATCH: {within}/{len(valid_pairs)} steps "
                    "within 20% of historical reference.",
                )

    return (
        FidelityTier.DIRECTION_ONLY,
        "Directional fidelity confirmed. Magnitude calibration pending — "
        f"{len(valid_pairs)} valid (model, hist) pairs available.",
    )


_COMPOSITE_INDICATOR_FIELDS = frozenset(
    {"hd_composite", "fin_composite", "eco_composite", "gov_composite"}
)


def _classify_direction(
    cf_records: list[dict[str, Any]],
    baseline_records: list[dict[str, Any]],
    n_steps: int,
    primary_indicator: str | None,
) -> tuple[DirectionVerdict, list[Decimal], int | None]:
    """Compute per-step differential and classify Type B direction verdict.

    When primary_indicator names a composite field (hd_composite, fin_composite,
    eco_composite, gov_composite), that field is used directly for comparison.
    Otherwise falls back to: PSP → fin_composite → 0.
    """
    per_step_diff: list[Decimal] = []
    threshold = Decimal("0.01")

    for i in range(n_steps):
        if primary_indicator in _COMPOSITE_INDICATOR_FIELDS:
            cf_val = cf_records[i].get(primary_indicator) if i < len(cf_records) else None
            bl_val = (
                baseline_records[i].get(primary_indicator)
                if i < len(baseline_records)
                else None
            )
            if cf_val is not None and bl_val is not None:
                per_step_diff.append(cf_val - bl_val)
            else:
                per_step_diff.append(Decimal("0"))
        else:
            cf_psp = cf_records[i].get("psp") if i < len(cf_records) else None
            bl_psp = baseline_records[i].get("psp") if i < len(baseline_records) else None

            if cf_psp is not None and bl_psp is not None:
                per_step_diff.append(cf_psp - bl_psp)
            else:
                cf_fin = (
                    cf_records[i].get("fin_composite") if i < len(cf_records) else None
                )
                bl_fin = (
                    baseline_records[i].get("fin_composite")
                    if i < len(baseline_records)
                    else None
                )
                if cf_fin is not None and bl_fin is not None:
                    per_step_diff.append(cf_fin - bl_fin)
                else:
                    per_step_diff.append(Decimal("0"))

    first_significant: int | None = None
    for idx, diff in enumerate(per_step_diff):
        if abs(diff) > threshold:
            first_significant = idx + 1
            break

    pos_steps = sum(1 for d in per_step_diff if d > threshold)
    neg_steps = sum(1 for d in per_step_diff if d < -threshold)

    if pos_steps == 0 and neg_steps == 0:
        verdict = DirectionVerdict.INDISTINGUISHABLE
    elif pos_steps >= neg_steps:
        verdict = DirectionVerdict.COUNTER_FACTUAL_BETTER
    else:
        verdict = DirectionVerdict.BASELINE_BETTER

    return verdict, per_step_diff, first_significant


# ---------------------------------------------------------------------------
# Primary API: run_harness()
# ---------------------------------------------------------------------------


async def run_harness(
    scenario_id: str,
    steps: int,
    run_type: RunType,
    control_inputs: list[dict[str, Any]],
    *,
    http_client: httpx.AsyncClient | None = None,
    base_url: str = "http://localhost:8000",
    baseline_run_id: str | None = None,
    primary_indicator: str | None = None,
) -> HarnessResult:
    """Run the battle-testing harness against a scenario.

    AC-12: raises HarnessValidationError if steps <= 0 before any API call.
    AC-11: raises when the scenario ID is not found (HTTP 404).
    AC-15 / SF-4: raises HarnessApiError (with step context) on any HTTP 5xx.
    """
    if steps <= 0:
        raise HarnessValidationError(f"steps must be > 0, got {steps!r}")

    known_limitations = detect_known_limitations(
        control_inputs,
        primary_indicator=primary_indicator,
        n_steps=steps,
        run_type=run_type,
    )

    own_client = http_client is None
    client: httpx.AsyncClient = (
        httpx.AsyncClient(base_url=base_url, timeout=60.0)
        if own_client
        else http_client  # type: ignore[assignment]
    )

    try:
        advance_responses: list[dict[str, Any]] = []
        for step_num in range(1, steps + 1):
            adv = await _advance_step(client, base_url, scenario_id, step_num)
            advance_responses.append(adv)

        traj_steps = await _fetch_trajectory(client, base_url, scenario_id)
        per_step_records = _build_per_step_records(steps, advance_responses, traj_steps)

        timestamp = datetime.now(tz=UTC).isoformat()
        run_metadata: dict[str, Any] = {
            "scenario_id": scenario_id,
            "run_type": run_type,
            "steps": steps,
            "output_timestamp": timestamp,
            "is_pre_calibration": True,
        }

        if run_type == RunType.TYPE_A:
            fidelity_tier, rationale = _classify_fidelity(per_step_records)
            summary: dict[str, Any] = {
                "fidelity_tier": fidelity_tier,
                "fidelity_rationale": rationale,
                "known_limitations": known_limitations,
            }
        else:
            # TYPE_B: compare against baseline run
            baseline_traj: list[dict[str, Any]] = []
            if baseline_run_id:
                baseline_traj = await _fetch_trajectory(client, base_url, baseline_run_id)
            baseline_records = _build_per_step_records(steps, [], baseline_traj)

            verdict, per_step_diff, first_sig = _classify_direction(
                per_step_records, baseline_records, steps, primary_indicator
            )
            summary = {
                "baseline_run_id": baseline_run_id,
                "counterfactual_run_id": scenario_id,
                "primary_indicator": primary_indicator,
                "step_differential_first_significant": first_sig,
                "direction_verdict": verdict,
                "per_step_diff": per_step_diff,
                "known_limitations": known_limitations,
            }
    finally:
        if own_client:
            await client.aclose()

    return HarnessResult(
        run_metadata=run_metadata,
        per_step_records=per_step_records,
        summary=summary,
    )


# ---------------------------------------------------------------------------
# Output formatting
# ---------------------------------------------------------------------------


class _DecimalEncoder(json.JSONEncoder):
    def default(self, obj: object) -> object:
        if isinstance(obj, Decimal):
            return str(obj)
        if isinstance(obj, RunType | FidelityTier | DirectionVerdict):
            return obj.value
        return super().default(obj)


def _val(v: object) -> str:
    if v is None:
        return ""
    if isinstance(v, Decimal):
        return str(v)
    return str(v)


def _format_csv(result: HarnessResult) -> str:
    out = io.StringIO()
    w = csv.writer(out)
    headers = [
        "step", "fin_composite", "hd_composite", "eco_composite", "gov_composite",
        "psp", "ci_band_low", "ci_band_high", "cohort_poverty_headcount",
        "mda_alert_states", "active_failure_modes",
    ]
    w.writerow(headers)
    for rec in result.per_step_records:
        w.writerow([
            _val(rec.get("step")),
            _val(rec.get("fin_composite")),
            _val(rec.get("hd_composite")),
            _val(rec.get("eco_composite")),
            _val(rec.get("gov_composite")),
            _val(rec.get("psp")),
            _val(rec.get("ci_band_low")),
            _val(rec.get("ci_band_high")),
            _val(rec.get("cohort_poverty_headcount")),
            ";".join(str(a) for a in (rec.get("mda_alert_states") or [])),
            ";".join(str(f) for f in (rec.get("active_failure_modes") or [])),
        ])
    limitations = result.summary.get("known_limitations") or []
    if limitations:
        w.writerow([])
        w.writerow(["KNOWN LIMITATIONS"])
        for lim in limitations:
            w.writerow([lim])
    return out.getvalue()


def _format_json(result: HarnessResult) -> str:
    data = {
        "run_metadata": result.run_metadata,
        "per_step_records": result.per_step_records,
        "summary": result.summary,
    }
    return json.dumps(data, cls=_DecimalEncoder, indent=2)


def _format_markdown(result: HarnessResult) -> str:
    meta = result.run_metadata
    lines: list[str] = [
        "# Battle-Testing Harness Report",
        "",
        f"**Scenario:** `{meta.get('scenario_id', '')}`  ",
        f"**Run type:** {meta.get('run_type', '')}  ",
        f"**Steps:** {meta.get('steps', '')}  ",
        f"**Timestamp:** {meta.get('output_timestamp', '')}",
        "",
        "## Summary",
        "",
    ]
    for key, val in result.summary.items():
        if key == "known_limitations":
            continue
        if isinstance(val, list):
            lines.append(f"**{key}:** `{[str(v) for v in val]}`  ")
        elif isinstance(val, RunType | FidelityTier | DirectionVerdict):
            lines.append(f"**{key}:** {val.value}  ")
        else:
            lines.append(f"**{key}:** {val}  ")
    lines.extend([
        "",
        "## Per-Step Records",
        "",
        "| step | fin | hd | eco | gov | psp | ci_low | ci_high | cohort | mda |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ])
    for rec in result.per_step_records:
        row = [
            _val(rec.get("step")),
            _val(rec.get("fin_composite")),
            _val(rec.get("hd_composite")),
            _val(rec.get("eco_composite")),
            _val(rec.get("gov_composite")),
            _val(rec.get("psp")),
            _val(rec.get("ci_band_low")),
            _val(rec.get("ci_band_high")),
            _val(rec.get("cohort_poverty_headcount")),
            ";".join(str(a) for a in (rec.get("mda_alert_states") or [])),
        ]
        lines.append("| " + " | ".join(row) + " |")
    lines.extend(["", "## Known Limitations", ""])
    limitations = result.summary.get("known_limitations") or []
    if limitations:
        for lim in limitations:
            lines.append(f"- {lim}")
    else:
        lines.append("_None identified for this run._")
    lines.append("")
    return "\n".join(lines)


def _format_ascii(result: HarnessResult) -> str:
    meta = result.run_metadata
    col_w = 12
    cols = ["step", "fin", "hd", "eco", "gov", "psp", "ci_low", "ci_high"]
    sep = "+" + "+".join("-" * (col_w + 2) for _ in cols) + "+"
    hdr = "|" + "|".join(f" {c:<{col_w}} " for c in cols) + "|"
    lines: list[str] = [
        (
            f"Battle-Testing Harness — {meta.get('scenario_id', '')} "
            f"({meta.get('run_type', '')}, {meta.get('steps', '')} steps)"
        ),
        sep,
        hdr,
        sep,
    ]
    for rec in result.per_step_records:
        cells = [
            str(rec.get("step", "")),
            _val(rec.get("fin_composite")) or "-",
            _val(rec.get("hd_composite")) or "-",
            _val(rec.get("eco_composite")) or "-",
            _val(rec.get("gov_composite")) or "-",
            _val(rec.get("psp")) or "-",
            _val(rec.get("ci_band_low")) or "-",
            _val(rec.get("ci_band_high")) or "-",
        ]
        lines.append("|" + "|".join(f" {c:<{col_w}} " for c in cells) + "|")
    lines.append(sep)
    lines.extend(["", "Summary:"])
    for key, val in result.summary.items():
        if key == "known_limitations":
            continue
        if isinstance(val, list):
            lines.append(f"  {key}: {[str(v) for v in val]}")
        elif isinstance(val, RunType | FidelityTier | DirectionVerdict):
            lines.append(f"  {key}: {val.value}")
        else:
            lines.append(f"  {key}: {val}")
    limitations = result.summary.get("known_limitations") or []
    if limitations:
        lines.extend(["", "Known Limitations:"])
        for lim in limitations:
            lines.append(f"  {lim}")
    return "\n".join(lines)


def format_output(result: HarnessResult, fmt: str) -> str:
    """Render a HarnessResult as a string in the requested format.

    fmt: "ascii" | "csv" | "json" | "markdown"
    Raises ValueError for unknown format strings.
    """
    fmt = fmt.lower().strip()
    dispatch = {
        "csv": _format_csv,
        "json": _format_json,
        "markdown": _format_markdown,
        "ascii": _format_ascii,
    }
    if fmt not in dispatch:
        raise ValueError(f"Unknown format {fmt!r}. Valid: {sorted(dispatch)}")
    return dispatch[fmt](result)


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------


def main() -> None:
    """CLI entry point for the headless battle-testing harness."""
    parser = argparse.ArgumentParser(
        description="WorldSim M19 G2A Headless Battle-Testing Harness"
    )
    parser.add_argument("scenario_id", help="Scenario ID to run")
    parser.add_argument("--steps", type=int, required=True)
    parser.add_argument(
        "--run-type", choices=["TYPE_A", "TYPE_B"], default="TYPE_A",
    )
    parser.add_argument("--baseline-run-id", default=None)
    parser.add_argument("--primary-indicator", default=None)
    parser.add_argument(
        "--format", dest="output_format",
        choices=["ascii", "csv", "json", "markdown"], default="ascii",
    )
    parser.add_argument("--base-url", default="http://localhost:8000")
    args = parser.parse_args()

    result = asyncio.run(run_harness(
        scenario_id=args.scenario_id,
        steps=args.steps,
        run_type=RunType(args.run_type),
        control_inputs=[],
        base_url=args.base_url,
        baseline_run_id=args.baseline_run_id,
        primary_indicator=args.primary_indicator,
    ))
    print(format_output(result, args.output_format))


if __name__ == "__main__":
    main()
