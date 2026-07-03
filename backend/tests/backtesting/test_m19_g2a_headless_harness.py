"""QA tests for M19 G2 Phase A — Headless Battle-Testing Harness (#1546).

Authored BEFORE implementation per intent document:
  docs/process/intents/M19-G2A-2026-07-02-headless-battle-testing-harness.md

Sprint entry: docs/process/sprint-plans/m19-g2a-sprint-entry.md

These tests are RED until the harness is implemented at:
  backend/app/harness/mode3_harness.py

NM-078 guard: this file is placed at backend/tests/backtesting/ — not at
backend/tests/ root — to ensure CI test discovery includes it. Verify that
pytest.ini testpaths (or equivalent discovery config) covers
backend/tests/backtesting/ before committing.

NM-056 rule: NO pytest.skip() or soft-skip patterns. Tests fail RED until
the implementation module exists at the import path above.

AC coverage:
  AC-1   run_harness() returns HarnessResult for valid input
  AC-2   format_output("csv") parses with csv.reader(); header + data rows present
  AC-3   format_output("json") is valid JSON; run_metadata / per_step_records /
         summary keys present; per_step_records length == steps
  AC-4   format_output("markdown") contains GFM table header, separator row,
         and ## Known Limitations heading
  AC-5   format_output("ascii") contains column headers and data rows; not raw JSON
  AC-6   Type A Greece 2010–12 → fidelity_tier == DIRECTION_ONLY (backtesting mark)
  AC-7   Type B summary contains direction_verdict (one of three valid values)
         and per_step_diff list of length == steps
  AC-8   CAPITAL_CONTROLS in control inputs → known_limitations references #1532
  AC-9   reserve_coverage_months / debt_gdp_ratio as primary_indicator → #30 label
  AC-10  bilateral relationship run (n_steps > 1) → #35 / bilateral weights label
  AC-11  Unknown scenario ID → exception raised; not silent HarnessResult
  AC-12  steps=0 → HarnessValidationError before any API call
  AC-13  SF-1 guard: len(per_step_records) == steps for valid run (also via AC-3)
  AC-14  SF-2 guard: CAPITAL_CONTROLS → len(known_limitations) >= 1
  AC-15  SF-4 guard: HTTP 500 on step 3 → exception raised (not silent exit 0)
"""
from __future__ import annotations

import csv
import io
import json
import os
from decimal import Decimal
from typing import TYPE_CHECKING, Any
from unittest.mock import AsyncMock, MagicMock

import httpx
import pytest
import pytest_asyncio

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator

# RED until implemented. See intent doc §7 for the required module surface:
#   HarnessResult  — dataclass with run_metadata, per_step_records, summary
#   HarnessValidationError — raised on invalid inputs (steps=0, bad scenario, etc.)
#   RunType        — enum: TYPE_A | TYPE_B
#   FidelityTier   — enum: MAGNITUDE_MATCH | DIRECTION_ONLY | STRUCTURAL_ONLY | BELOW_THRESHOLD
#   DirectionVerdict — enum: COUNTER_FACTUAL_BETTER | BASELINE_BETTER | INDISTINGUISHABLE
#   detect_known_limitations(control_inputs, primary_indicator, n_steps) -> list[str]
#   format_output(result: HarnessResult, fmt: str) -> str
#   run_harness(scenario_id, steps, run_type, control_inputs, *, http_client, ...) -> HarnessResult
from app.harness.mode3_harness import (
    DirectionVerdict,
    FidelityTier,
    HarnessResult,
    HarnessValidationError,
    RunType,
    detect_known_limitations,
    format_output,
    run_harness,
)
from app.main import app

_DATABASE_URL = os.environ.get("DATABASE_URL", "")

pytestmark = pytest.mark.asyncio(loop_scope="function")


# ---------------------------------------------------------------------------
# Fixtures and helpers
# ---------------------------------------------------------------------------


def _make_step_record(step: int) -> dict[str, Any]:
    """Minimal valid per-step record per intent doc §3.1 Section B."""
    return {
        "step": step,
        "fin_composite": Decimal("0.55"),
        "hd_composite": Decimal("0.60"),
        "eco_composite": Decimal("0.70"),
        "gov_composite": Decimal("0.50"),
        "mda_alert_states": [],
        "cohort_poverty_headcount": None,
        "psp": Decimal("0.52"),
        "ci_band_low": Decimal("0.45"),
        "ci_band_high": Decimal("0.65"),
        "active_failure_modes": [],
    }


FIXTURE_RESULT_TYPE_A = HarnessResult(
    run_metadata={
        "scenario_id": "test_fixture_type_a",
        "run_type": RunType.TYPE_A,
        "steps": 3,
        "output_timestamp": "2026-07-02T00:00:00+00:00",
        "is_pre_calibration": False,
    },
    per_step_records=[_make_step_record(i) for i in range(1, 4)],
    summary={
        "fidelity_tier": FidelityTier.DIRECTION_ONLY,
        "fidelity_rationale": "GDP direction correct; magnitude error exceeds threshold",
        "known_limitations": [],
    },
)

FIXTURE_RESULT_TYPE_B = HarnessResult(
    run_metadata={
        "scenario_id": "test_fixture_type_b",
        "run_type": RunType.TYPE_B,
        "steps": 3,
        "output_timestamp": "2026-07-02T00:00:00+00:00",
        "is_pre_calibration": False,
    },
    per_step_records=[_make_step_record(i) for i in range(1, 4)],
    summary={
        "baseline_run_id": "baseline_fixture_001",
        "counterfactual_run_id": "test_fixture_type_b",
        "primary_indicator": "q1_poverty_headcount_ratio",
        "step_differential_first_significant": 2,
        "direction_verdict": DirectionVerdict.COUNTER_FACTUAL_BETTER,
        "per_step_diff": [Decimal("0.05"), Decimal("0.10"), Decimal("0.15")],
        "known_limitations": [],
    },
)

FIXTURE_RESULT_WITH_CAPITAL_CONTROLS = HarnessResult(
    run_metadata={
        "scenario_id": "test_fixture_capital_controls",
        "run_type": RunType.TYPE_A,
        "steps": 2,
        "output_timestamp": "2026-07-02T00:00:00+00:00",
        "is_pre_calibration": False,
    },
    per_step_records=[_make_step_record(i) for i in range(1, 3)],
    summary={
        "fidelity_tier": FidelityTier.DIRECTION_ONLY,
        "fidelity_rationale": "Capital controls in use; #1532 applies",
        "known_limitations": [
            "⚠ Economic transmission absent — political cost only (#1532 CAPITAL_CONTROLS)"
        ],
    },
)


def _make_advance_response(step: int, status_code: int = 200) -> MagicMock:
    """Mock httpx.Response for POST /api/v1/scenarios/{id}/advance."""
    resp = MagicMock(spec=httpx.Response)
    resp.status_code = status_code
    resp.json.return_value = {
        "step": step,
        "composite_scores": {
            "financial": "0.55",
            "human_development": "0.60",
            "ecological": "0.70",
            "governance": None,
        },
        "psp": "0.52",
        "ci_band": {"low": "0.45", "high": "0.65"},
        "focal_cohort_poverty_headcount": None,
        "mda_alert_states": [],
        "active_failure_modes": [],
    }
    return resp


def _make_mock_client(
    steps: int,
    *,
    fail_on_step: int | None = None,
    scenario_exists: bool = True,
) -> AsyncMock:
    """Return an AsyncMock httpx.AsyncClient for run_harness() unit tests.

    Args:
        steps: number of /advance calls to mock successfully.
        fail_on_step: 1-indexed step at which /advance returns HTTP 500.
        scenario_exists: if False, all calls return 404 (unknown scenario).
    """
    client = AsyncMock(spec=httpx.AsyncClient)
    call_count: list[int] = [0]

    async def _post(url: str, **kwargs: object) -> MagicMock:
        if not scenario_exists:
            resp = MagicMock(spec=httpx.Response)
            resp.status_code = 404
            resp.json.return_value = {"detail": "Scenario not found"}
            return resp
        if "/advance" in str(url):
            call_count[0] += 1
            current_step = call_count[0]
            if fail_on_step is not None and current_step == fail_on_step:
                return _make_advance_response(current_step, status_code=500)
            return _make_advance_response(current_step, status_code=200)
        resp = MagicMock(spec=httpx.Response)
        resp.status_code = 200
        resp.json.return_value = {}
        return resp

    async def _get(url: str, **kwargs: object) -> MagicMock:
        if not scenario_exists:
            resp = MagicMock(spec=httpx.Response)
            resp.status_code = 404
            resp.json.return_value = {"detail": "Scenario not found"}
            return resp
        resp = MagicMock(spec=httpx.Response)
        resp.status_code = 200
        resp.json.return_value = {}
        return resp

    client.post = _post  # type: ignore[method-assign]
    client.get = _get    # type: ignore[method-assign]
    return client


# ---------------------------------------------------------------------------
# AC-2: format_output("csv")
# ---------------------------------------------------------------------------


class TestFormatOutputCsv:
    """AC-2: format_output("csv") produces Excel-parseable CSV."""

    def test_csv_parses_without_error(self) -> None:
        """AC-2: csv.reader() accepts output without parse error."""
        output = format_output(FIXTURE_RESULT_TYPE_A, "csv")
        rows = list(csv.reader(io.StringIO(output)))
        assert rows, "csv.reader() returned no rows"

    def test_csv_first_row_is_header(self) -> None:
        """AC-2: first row contains column headers, not numeric step data."""
        output = format_output(FIXTURE_RESULT_TYPE_A, "csv")
        reader = csv.reader(io.StringIO(output))
        header = next(reader)
        lower_headers = [h.lower().strip() for h in header]
        assert "step" in lower_headers, (
            f"'step' not found in CSV header row: {header}"
        )

    def test_csv_data_row_count_matches_steps(self) -> None:
        """AC-2 / AC-13 (SF-1): per-step data rows == steps (excluding header/limitations)."""
        output = format_output(FIXTURE_RESULT_TYPE_A, "csv")
        reader = csv.reader(io.StringIO(output))
        next(reader)  # skip header
        step_rows = [r for r in reader if r and r[0].strip().isdigit()]
        expected = FIXTURE_RESULT_TYPE_A.run_metadata["steps"]
        assert len(step_rows) == expected, (
            f"SF-1: expected {expected} data rows, got {len(step_rows)}"
        )

    def test_csv_no_unescaped_newlines_in_step_rows(self) -> None:
        """AC-2: step-data cells contain no unescaped newline characters."""
        output = format_output(FIXTURE_RESULT_TYPE_A, "csv")
        reader = csv.reader(io.StringIO(output))
        next(reader)
        for row in reader:
            if not row or not row[0].strip().isdigit():
                continue
            for cell in row:
                assert "\n" not in cell, (
                    f"Unescaped newline in CSV cell '{cell}' at row {row}"
                )

    def test_csv_known_limitations_present_when_active(self) -> None:
        """AC-2 / AC-8: KNOWN LIMITATIONS section appears in CSV when limitations are active."""
        output = format_output(FIXTURE_RESULT_WITH_CAPITAL_CONTROLS, "csv")
        assert (
            "KNOWN LIMITATIONS" in output.upper()
            or "known_limitations" in output.lower()
        ), "Expected KNOWN LIMITATIONS section in CSV output when limitations are active"


# ---------------------------------------------------------------------------
# AC-3: format_output("json")
# ---------------------------------------------------------------------------


class TestFormatOutputJson:
    """AC-3: format_output("json") produces valid JSON with required keys."""

    def test_json_parses_without_error(self) -> None:
        """AC-3: json.loads() accepts output without raising."""
        output = format_output(FIXTURE_RESULT_TYPE_A, "json")
        data = json.loads(output)
        assert isinstance(data, dict)

    def test_json_has_run_metadata(self) -> None:
        """AC-3: top-level 'run_metadata' key present."""
        data = json.loads(format_output(FIXTURE_RESULT_TYPE_A, "json"))
        assert "run_metadata" in data, (
            f"'run_metadata' missing from JSON output; keys: {list(data.keys())}"
        )

    def test_json_has_per_step_records_as_list(self) -> None:
        """AC-3: top-level 'per_step_records' key present and is a list."""
        data = json.loads(format_output(FIXTURE_RESULT_TYPE_A, "json"))
        assert "per_step_records" in data
        assert isinstance(data["per_step_records"], list)

    def test_json_per_step_records_length_matches_steps(self) -> None:
        """AC-3 / AC-13 (SF-1): len(per_step_records) == run_metadata.steps."""
        data = json.loads(format_output(FIXTURE_RESULT_TYPE_A, "json"))
        expected = FIXTURE_RESULT_TYPE_A.run_metadata["steps"]
        assert len(data["per_step_records"]) == expected, (
            f"SF-1: expected {expected} per_step_records, "
            f"got {len(data['per_step_records'])}"
        )

    def test_json_summary_has_known_limitations_list(self) -> None:
        """AC-3: summary.known_limitations is a JSON array."""
        data = json.loads(format_output(FIXTURE_RESULT_TYPE_A, "json"))
        assert "summary" in data
        assert "known_limitations" in data["summary"]
        assert isinstance(data["summary"]["known_limitations"], list)

    def test_json_type_b_direction_verdict_present(self) -> None:
        """AC-7: Type B JSON summary contains direction_verdict field."""
        data = json.loads(format_output(FIXTURE_RESULT_TYPE_B, "json"))
        assert "direction_verdict" in data["summary"], (
            "direction_verdict missing from Type B JSON summary"
        )

    def test_json_type_b_direction_verdict_is_valid_value(self) -> None:
        """AC-7: direction_verdict is one of the three valid enum values."""
        data = json.loads(format_output(FIXTURE_RESULT_TYPE_B, "json"))
        valid_values = {
            DirectionVerdict.COUNTER_FACTUAL_BETTER,
            DirectionVerdict.BASELINE_BETTER,
            DirectionVerdict.INDISTINGUISHABLE,
        }
        # Accept either the enum member itself or its string representation
        verdict = data["summary"]["direction_verdict"]
        assert verdict in valid_values or str(verdict) in {str(v) for v in valid_values}, (
            f"Unexpected direction_verdict: {verdict!r}. Valid: {valid_values}"
        )

    def test_json_type_b_per_step_diff_list_length(self) -> None:
        """AC-7: per_step_diff list length == steps."""
        data = json.loads(format_output(FIXTURE_RESULT_TYPE_B, "json"))
        assert "per_step_diff" in data["summary"]
        expected = FIXTURE_RESULT_TYPE_B.run_metadata["steps"]
        assert len(data["summary"]["per_step_diff"]) == expected, (
            f"per_step_diff length {len(data['summary']['per_step_diff'])} "
            f"!= steps {expected}"
        )


# ---------------------------------------------------------------------------
# AC-4: format_output("markdown")
# ---------------------------------------------------------------------------


class TestFormatOutputMarkdown:
    """AC-4: format_output("markdown") produces GFM-renderable output."""

    def _lines(self, result: HarnessResult) -> list[str]:
        return format_output(result, "markdown").splitlines()

    def test_markdown_contains_gfm_table_header(self) -> None:
        """AC-4: output contains a pipe-delimited header row with 'step' column."""
        lines = self._lines(FIXTURE_RESULT_TYPE_A)
        table_headers = [
            line for line in lines
            if line.strip().startswith("|") and "step" in line.lower()
        ]
        assert table_headers, (
            "No GFM table header row found in markdown output "
            "(expected a pipe-delimited row containing 'step')"
        )

    def test_markdown_contains_table_separator_row(self) -> None:
        """AC-4: GFM separator row (| --- |) present immediately after header."""
        lines = self._lines(FIXTURE_RESULT_TYPE_A)
        separator_rows = [
            line for line in lines
            if line.strip().startswith("|") and "---" in line
        ]
        assert separator_rows, (
            "GFM table separator row (| --- |) not found in markdown output"
        )

    def test_markdown_contains_known_limitations_heading(self) -> None:
        """AC-4: ## Known Limitations heading present in all outputs."""
        output = format_output(FIXTURE_RESULT_TYPE_A, "markdown")
        assert (
            "## Known Limitations" in output
            or "## known limitations" in output.lower()
        ), "'## Known Limitations' heading missing from markdown output"

    def test_markdown_active_limitations_rendered_as_bullets(self) -> None:
        """AC-4: active limitations appear as Markdown list items."""
        lines = self._lines(FIXTURE_RESULT_WITH_CAPITAL_CONTROLS)
        bullet_lines = [
            line for line in lines
            if line.strip().startswith("- ") or line.strip().startswith("* ")
        ]
        assert bullet_lines, (
            "No bulleted list items found in markdown output "
            "when known_limitations is non-empty"
        )


# ---------------------------------------------------------------------------
# AC-5: format_output("ascii")
# ---------------------------------------------------------------------------


class TestFormatOutputAscii:
    """AC-5: format_output("ascii") produces terminal-readable output."""

    def test_ascii_contains_step_column_header(self) -> None:
        """AC-5: 'step' appears in column headers."""
        output = format_output(FIXTURE_RESULT_TYPE_A, "ascii")
        assert "step" in output.lower(), (
            "Column header 'step' not found in ASCII output"
        )

    def test_ascii_contains_at_least_one_data_row(self) -> None:
        """AC-5: output contains lines with numeric step data."""
        output = format_output(FIXTURE_RESULT_TYPE_A, "ascii")
        lines = output.splitlines()
        data_rows = [line for line in lines if any(ch.isdigit() for ch in line)]
        assert data_rows, "No data rows found in ASCII output"

    def test_ascii_is_not_raw_json(self) -> None:
        """AC-5: ASCII output is not a raw JSON blob starting with '{'."""
        output = format_output(FIXTURE_RESULT_TYPE_A, "ascii")
        assert not output.strip().startswith("{"), (
            "ASCII format returned raw JSON — expected human-readable columnar output"
        )


# ---------------------------------------------------------------------------
# AC-8, AC-9, AC-10, AC-14 — detect_known_limitations()
# ---------------------------------------------------------------------------


class TestDetectKnownLimitations:
    """Tests for detect_known_limitations(control_inputs, primary_indicator, n_steps)."""

    def test_capital_controls_references_1532(self) -> None:
        """AC-8: CAPITAL_CONTROLS in inputs → limitation string references #1532."""
        inputs = [{"instrument": "CAPITAL_CONTROLS", "value": 1}]
        limitations = detect_known_limitations(inputs, primary_indicator=None)
        matches = [
            line for line in limitations
            if "1532" in line
            or "CAPITAL_CONTROLS" in line.upper()
            or "transmission absent" in line.lower()
        ]
        assert matches, (
            f"Expected #1532 / CAPITAL_CONTROLS limitation when CAPITAL_CONTROLS in inputs. "
            f"Got: {limitations}"
        )

    def test_capital_controls_list_is_non_empty(self) -> None:
        """AC-14 (SF-2 guard): known_limitations non-empty for CAPITAL_CONTROLS."""
        inputs = [{"instrument": "CAPITAL_CONTROLS", "value": 1}]
        limitations = detect_known_limitations(inputs, primary_indicator=None)
        assert len(limitations) >= 1, (
            "known_limitations must be non-empty when CAPITAL_CONTROLS is in inputs"
        )

    def test_reserve_coverage_months_references_30(self) -> None:
        """AC-9: reserve_coverage_months as primary_indicator → #30 / DIRECTION_ONLY label."""
        limitations = detect_known_limitations(
            [], primary_indicator="reserve_coverage_months"
        )
        matches = [
            line for line in limitations
            if "#30" in line
            or "DIRECTION_ONLY at most" in line
            or "threshold-crossing" in line.lower()
        ]
        assert matches, (
            f"Expected #30 / stock-flow limitation for reserve_coverage_months. "
            f"Got: {limitations}"
        )

    def test_debt_gdp_ratio_references_30(self) -> None:
        """AC-9: debt_gdp_ratio as primary_indicator → #30 label."""
        limitations = detect_known_limitations([], primary_indicator="debt_gdp_ratio")
        matches = [
            line for line in limitations
            if "#30" in line or "DIRECTION_ONLY at most" in line
        ]
        assert matches, (
            f"Expected #30 / stock-flow limitation for debt_gdp_ratio. Got: {limitations}"
        )

    def test_bilateral_relationship_references_35(self) -> None:
        """AC-10: bilateral relationship over > 1 step → #35 / bilateral weights label."""
        inputs = [
            {"type": "bilateral_trade", "partner": "CHN", "value": 0.3},
            {"type": "bilateral_trade", "partner": "CHN", "value": 0.3},
        ]
        limitations = detect_known_limitations(
            inputs, primary_indicator=None, n_steps=2
        )
        matches = [
            line for line in limitations
            if "#35" in line
            or "bilateral weights" in line.lower()
            or "magnitude differential" in line.lower()
        ]
        assert matches, (
            f"Expected #35 / bilateral weights limitation for multi-step bilateral run. "
            f"Got: {limitations}"
        )

    def test_returns_list_type(self) -> None:
        """detect_known_limitations always returns a list (never None or str)."""
        result = detect_known_limitations([], primary_indicator=None)
        assert isinstance(result, list), (
            f"detect_known_limitations must return list, got {type(result)}"
        )


# ---------------------------------------------------------------------------
# AC-1, AC-7, AC-11, AC-12, AC-13, AC-15 — run_harness() async unit tests
# ---------------------------------------------------------------------------


class TestRunHarness:
    """Unit tests for run_harness() with mocked HTTP client."""

    async def test_valid_input_returns_harness_result(self) -> None:
        """AC-1: run_harness() returns a HarnessResult instance for valid input."""
        client = _make_mock_client(steps=3)
        result = await run_harness(
            scenario_id="test_valid_ac1",
            steps=3,
            run_type=RunType.TYPE_A,
            control_inputs=[{} for _ in range(3)],
            http_client=client,
        )
        assert isinstance(result, HarnessResult), (
            f"Expected HarnessResult, got {type(result)}"
        )

    async def test_per_step_records_length_matches_steps(self) -> None:
        """AC-13 (SF-1 guard): len(per_step_records) == steps for valid run."""
        n = 4
        client = _make_mock_client(steps=n)
        result = await run_harness(
            scenario_id="test_sf1_ac13",
            steps=n,
            run_type=RunType.TYPE_A,
            control_inputs=[{} for _ in range(n)],
            http_client=client,
        )
        assert len(result.per_step_records) == n, (
            f"SF-1: expected {n} per_step_records, got {len(result.per_step_records)}"
        )

    async def test_type_b_summary_contains_direction_verdict(self) -> None:
        """AC-7: Type B run → summary.direction_verdict is one of three valid values."""
        client = _make_mock_client(steps=3)
        result = await run_harness(
            scenario_id="test_type_b_ac7",
            steps=3,
            run_type=RunType.TYPE_B,
            control_inputs=[{} for _ in range(3)],
            baseline_run_id="baseline_ac7",
            primary_indicator="q1_poverty_headcount_ratio",
            http_client=client,
        )
        assert "direction_verdict" in result.summary, (
            "direction_verdict missing from Type B HarnessResult.summary"
        )
        valid_verdicts = {
            DirectionVerdict.COUNTER_FACTUAL_BETTER,
            DirectionVerdict.BASELINE_BETTER,
            DirectionVerdict.INDISTINGUISHABLE,
        }
        assert result.summary["direction_verdict"] in valid_verdicts, (
            f"Unexpected direction_verdict: {result.summary['direction_verdict']!r}"
        )

    async def test_type_b_summary_per_step_diff_length(self) -> None:
        """AC-7: Type B summary.per_step_diff length == steps."""
        n = 3
        client = _make_mock_client(steps=n)
        result = await run_harness(
            scenario_id="test_type_b_diff_len",
            steps=n,
            run_type=RunType.TYPE_B,
            control_inputs=[{} for _ in range(n)],
            baseline_run_id="baseline_diff_len",
            primary_indicator="q1_poverty_headcount_ratio",
            http_client=client,
        )
        assert "per_step_diff" in result.summary
        assert isinstance(result.summary["per_step_diff"], list)
        assert len(result.summary["per_step_diff"]) == n, (
            f"per_step_diff length {len(result.summary['per_step_diff'])} != steps {n}"
        )

    async def test_zero_steps_raises_validation_error(self) -> None:
        """AC-12: steps=0 raises HarnessValidationError before any API call."""
        client = _make_mock_client(steps=0)
        with pytest.raises(HarnessValidationError):
            await run_harness(
                scenario_id="test_zero_steps_ac12",
                steps=0,
                run_type=RunType.TYPE_A,
                control_inputs=[],
                http_client=client,
            )

    async def test_unknown_scenario_raises(self) -> None:
        """AC-11: unknown scenario ID → exception; not silent HarnessResult.

        The harness must not return a populated HarnessResult when the scenario
        does not exist. If the harness receives a 404, it must raise rather than
        silently returning an empty or partial result.
        """
        client = _make_mock_client(steps=3, scenario_exists=False)
        with pytest.raises(HarnessValidationError):
            await run_harness(
                scenario_id="nonexistent-scenario-ac11",
                steps=3,
                run_type=RunType.TYPE_A,
                control_inputs=[{} for _ in range(3)],
                http_client=client,
            )

    async def test_mid_run_500_raises_with_step_context(self) -> None:
        """AC-15 (SF-4 guard): HTTP 500 on step 3 → exception referencing step 3 or 500.

        The harness must not swallow mid-run API errors and exit with a full or
        partial HarnessResult. Any HTTP 5xx during the advance loop must produce
        an exception whose message references the failing step or status code.
        """
        client = _make_mock_client(steps=5, fail_on_step=3)
        with pytest.raises(Exception) as exc_info:
            await run_harness(
                scenario_id="test_mid_run_500_ac15",
                steps=5,
                run_type=RunType.TYPE_A,
                control_inputs=[{} for _ in range(5)],
                http_client=client,
            )
        exc_text = str(exc_info.value)
        assert "3" in exc_text or "500" in exc_text, (
            f"SF-4: exception must reference step 3 or status 500. Got: {exc_text!r}"
        )


# ---------------------------------------------------------------------------
# AC-6 — Greece 2010–12 regression (backtesting mark; live DB required)
# ---------------------------------------------------------------------------


@pytest.mark.backtesting
@pytest.mark.asyncio(loop_scope="session")
class TestGreeceTypeARegressionFidelity:
    """AC-6: Type A Greece 2010–12 run → DIRECTION_ONLY fidelity tier.

    Regression gate: if the harness produces a different fidelity tier on the
    canonical Greece fixture after any G2A refactoring, this test will fail.
    Chief Methodologist review is required before the tier floor changes.

    Requires DATABASE_URL — the conftest skips the session when it is absent.
    Uses httpx.ASGITransport to call the FastAPI app in-process.
    """

    @pytest_asyncio.fixture(loop_scope="session")
    async def asgi_client(self) -> AsyncGenerator[httpx.AsyncClient, None]:
        if not _DATABASE_URL:
            pytest.skip("DATABASE_URL not set — skipping Greece Type A harness regression")
        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app),
            base_url="http://test",
        ) as client:
            yield client

    async def test_greece_type_a_produces_direction_only(
        self, asgi_client: httpx.AsyncClient
    ) -> None:
        """AC-6: Greece 2010–12 harness run → fidelity_tier == DIRECTION_ONLY.

        This complements test_greece_2010_2012.py: that test validates the raw
        simulation snapshots; this test validates that the harness correctly
        classifies the same run as DIRECTION_ONLY. A fidelity tier mismatch
        between the two tests indicates a bug in the harness classification logic.
        """
        from tests.fixtures.greece_2010_scenario import build_greece_scenario

        scenario_req = build_greece_scenario()
        create_resp = await asgi_client.post(
            "/api/v1/scenarios",
            json=scenario_req.model_dump(mode="json"),
        )
        assert create_resp.status_code == 201, (
            f"Scenario creation failed: {create_resp.status_code} {create_resp.text}"
        )
        scenario_id: str = create_resp.json()["scenario_id"]

        try:
            result = await run_harness(
                scenario_id=scenario_id,
                steps=6,
                run_type=RunType.TYPE_A,
                control_inputs=[{} for _ in range(6)],
                http_client=asgi_client,
            )

            assert result.summary.get("fidelity_tier") == FidelityTier.DIRECTION_ONLY, (
                f"AC-6 regression FAIL: Greece 2010–12 Type A expected DIRECTION_ONLY, "
                f"got {result.summary.get('fidelity_tier')!r}. "
                "Chief Methodologist review required before G2B calibration fixtures are filed."
            )
        finally:
            await asgi_client.delete(f"/api/v1/scenarios/{scenario_id}")
