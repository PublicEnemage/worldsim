"""QA tests for M17-G5 #1214: startup WARNING when simulation_entities is empty.

Authored from sprint entry acceptance criteria at:
  docs/process/sprint-plans/m17-g5-sprint-entry.md §2.4 #1214

NM-060 upstream (M16-G6): startup observability gap — empty simulation_entities
produces a silent 422 on scenario creation with no diagnostic signal. Fix is
process improvement #1 from NM-060: the backend must log a structured WARNING
at lifespan startup when simulation_entities is empty, including the correct
fix command.

These tests WILL FAIL until the implementation PR adds _check_startup_entities()
to app/main.py and calls it from the lifespan after create_asyncpg_pool().

Schema reference: docs/schema/database.yml (simulation_entities table).

NM-056 rule: NO pytest.skip() conditionally. No soft-skips.

AC coverage:
  AC-1214-1  WARNING log emitted when simulation_entities count is 0 at startup
  AC-1214-2  No WARNING emitted when simulation_entities count is ≥ 1
  AC-1214-R  Startup not disrupted — function completes normally in both cases,
             queries simulation_entities specifically, WARNING is at WARNING level
"""
from __future__ import annotations

import logging
from unittest.mock import AsyncMock

import pytest

from app.main import _check_startup_entities  # Added by implementation PR

# ---------------------------------------------------------------------------
# AC-1214-1 — WARNING emitted when simulation_entities is empty
# ---------------------------------------------------------------------------


class TestAC12141WarningWhenEmpty:
    """AC-1214-1: structured WARNING log emitted when simulation_entities count is 0.

    NM-060 §Process improvement 1: the startup log must make an empty entity table
    self-diagnosable without source inspection.
    """

    @pytest.mark.asyncio
    async def test_warning_emitted_when_entity_count_is_zero(
        self, caplog: pytest.LogCaptureFixture
    ) -> None:
        """WARNING is logged when simulation_entities returns 0 rows.

        A developer who runs the stack with an unseeded database must see the
        WARNING immediately in startup output — not discover the empty table
        by inspecting source code after receiving a 422 on scenario creation.
        """
        mock_pool = AsyncMock()
        mock_pool.fetchval.return_value = 0

        with caplog.at_level(logging.WARNING, logger="app.main"):
            await _check_startup_entities(mock_pool)

        warning_records = [r for r in caplog.records if r.levelname == "WARNING"]
        assert len(warning_records) >= 1, (
            "AC-1214-1: no WARNING logged when simulation_entities count is 0. "
            "Implementation PR must add a WARNING log in _check_startup_entities() "
            "when the entity count is 0. "
            "NM-060: a zero-entity stack produces silent 422s — the startup log must say so."
        )

    @pytest.mark.asyncio
    async def test_warning_contains_fix_command(self, caplog: pytest.LogCaptureFixture) -> None:
        """WARNING log must contain the correct fix command.

        NM-060 §Three-layer failure #2: CONTRIBUTING.md previously listed the wrong
        fix command. The WARNING in the startup log must cite the correct invocation
        so developers can self-diagnose from the log alone.
        """
        mock_pool = AsyncMock()
        mock_pool.fetchval.return_value = 0

        with caplog.at_level(logging.WARNING, logger="app.main"):
            await _check_startup_entities(mock_pool)

        fix_command = "python -m app.db.seed.natural_earth_loader"
        warning_records = [r for r in caplog.records if r.levelname == "WARNING"]
        assert any(fix_command in r.message for r in warning_records), (
            f"AC-1214-1: WARNING log must contain the fix command '{fix_command}'. "
            "NM-060: the correct command was absent from prior diagnostics. "
            "The log message must be self-contained — developers must not need to read "
            "source or CONTRIBUTING.md to find the fix."
        )

    @pytest.mark.asyncio
    async def test_warning_logged_at_warning_level_not_info_or_error(
        self, caplog: pytest.LogCaptureFixture
    ) -> None:
        """Diagnostic log must be at WARNING level — not INFO, ERROR, or CRITICAL.

        INFO is invisible at default log filters; ERROR/CRITICAL implies a fatal
        condition. WARNING is the correct level for a degraded-but-functional state.
        """
        mock_pool = AsyncMock()
        mock_pool.fetchval.return_value = 0

        with caplog.at_level(logging.DEBUG, logger="app.main"):
            await _check_startup_entities(mock_pool)

        levels = {r.levelname for r in caplog.records}
        assert "WARNING" in levels, (
            "AC-1214-1: startup diagnostic must be logged at WARNING level. "
            f"Levels found: {levels}. "
            "INFO is not visible at default log filters; "
            "ERROR/CRITICAL level would imply a fatal startup condition."
        )
        non_warning_levels = levels - {"WARNING"}
        fatal_levels = {"ERROR", "CRITICAL"} & non_warning_levels
        assert not fatal_levels, (
            "AC-1214-1: startup check must not emit ERROR or CRITICAL log entries "
            "when entities are empty — empty entities is a setup gap, not a fatal error. "
            f"Unexpected levels: {fatal_levels}"
        )


# ---------------------------------------------------------------------------
# AC-1214-2 — No WARNING emitted when simulation_entities is populated
# ---------------------------------------------------------------------------


class TestAC12142NoWarningWhenPopulated:
    """AC-1214-2: no WARNING emitted when simulation_entities has ≥ 1 row.

    The observability signal must be silent on a healthy stack. Spurious WARNINGs
    on populated databases would mask real issues and erode signal credibility.
    """

    @pytest.mark.asyncio
    async def test_no_warning_when_one_entity_row(self, caplog: pytest.LogCaptureFixture) -> None:
        """No WARNING when simulation_entities has exactly 1 row."""
        mock_pool = AsyncMock()
        mock_pool.fetchval.return_value = 1

        with caplog.at_level(logging.WARNING, logger="app.main"):
            await _check_startup_entities(mock_pool)

        warning_records = [r for r in caplog.records if r.levelname == "WARNING"]
        assert len(warning_records) == 0, (
            "AC-1214-2: WARNING emitted when simulation_entities has 1 row. "
            "The observability signal must be silent on a populated stack. "
            f"Unexpected WARNING records: {[r.message for r in warning_records]}"
        )

    @pytest.mark.asyncio
    async def test_no_warning_when_full_natural_earth_entity_set(
        self, caplog: pytest.LogCaptureFixture
    ) -> None:
        """No WARNING when simulation_entities has Natural Earth entity count (249 typical).

        249 is the approximate number of entities seeded by the Natural Earth loader.
        A healthy stack must not emit any WARNING on startup.
        """
        mock_pool = AsyncMock()
        mock_pool.fetchval.return_value = 249

        with caplog.at_level(logging.WARNING, logger="app.main"):
            await _check_startup_entities(mock_pool)

        warning_records = [r for r in caplog.records if r.levelname == "WARNING"]
        assert len(warning_records) == 0, (
            "AC-1214-2: WARNING emitted when simulation_entities has 249 rows. "
            "A fully-seeded stack (Natural Earth) must not emit this WARNING. "
            f"Unexpected WARNING records: {[r.message for r in warning_records]}"
        )


# ---------------------------------------------------------------------------
# AC-1214-R — Startup not disrupted
# ---------------------------------------------------------------------------


class TestAC1214RStartupNotDisrupted:
    """AC-1214-R: _check_startup_entities completes normally in all cases.

    The WARNING is informational. It must not raise an exception, must not
    disrupt the lifespan, and must not cause the health endpoint to fail.
    Existing startup behaviour — lifespan completes, health endpoint returns 200
    — is unaffected by whether entities are empty or populated.
    """

    @pytest.mark.asyncio
    async def test_no_exception_when_empty(self) -> None:
        """Function completes without raising when simulation_entities is empty."""
        mock_pool = AsyncMock()
        mock_pool.fetchval.return_value = 0

        # Must complete without raising — startup must not be disrupted.
        await _check_startup_entities(mock_pool)

    @pytest.mark.asyncio
    async def test_no_exception_when_populated(self) -> None:
        """Function completes without raising when simulation_entities is populated."""
        mock_pool = AsyncMock()
        mock_pool.fetchval.return_value = 249

        await _check_startup_entities(mock_pool)

    @pytest.mark.asyncio
    async def test_queries_simulation_entities_table(self) -> None:
        """Function must query simulation_entities — not any other table.

        Per docs/schema/database.yml: simulation_entities is the canonical entities
        table. The check must query this specific table to correctly detect the
        NM-060 root cause (unseeded Natural Earth data).
        """
        mock_pool = AsyncMock()
        mock_pool.fetchval.return_value = 0

        await _check_startup_entities(mock_pool)

        mock_pool.fetchval.assert_called_once()
        call_args_list = mock_pool.fetchval.call_args_list
        assert len(call_args_list) == 1, (
            "AC-1214-R: _check_startup_entities must issue exactly one query to the pool."
        )
        query_str = (call_args_list[0].args[0] if call_args_list[0].args else "").lower()
        assert "simulation_entities" in query_str, (
            "AC-1214-R: _check_startup_entities must query 'simulation_entities'. "
            f"Actual query: '{query_str}'. "
            "Per docs/schema/database.yml: simulation_entities is the entities table "
            "seeded by the Natural Earth loader. Querying any other table will not "
            "detect the NM-060 root cause."
        )

    @pytest.mark.asyncio
    async def test_pool_called_exactly_once_regardless_of_result(self) -> None:
        """Pool is queried exactly once whether entities are empty or populated.

        The check must not issue multiple queries or retry on failure. One COUNT(*)
        query at startup is the full scope of this observability addition.
        """
        for entity_count in (0, 1, 249):
            mock_pool = AsyncMock()
            mock_pool.fetchval.return_value = entity_count

            await _check_startup_entities(mock_pool)

            assert mock_pool.fetchval.call_count == 1, (
                f"AC-1214-R: _check_startup_entities issued {mock_pool.fetchval.call_count} "
                f"pool queries when entity count = {entity_count}, expected exactly 1. "
                "The startup check must not retry or issue additional queries."
            )
