"""Root conftest — session-wide guards applied before any test is collected.

Python version guard (Issue #131):
  The project requires Python 3.11+ because datetime.UTC was introduced in
  3.11 and ruff's UP017 rule (enabled via target-version = "py312") rewrites
  timezone.utc to datetime.UTC. Running pytest under Python 3.10 or earlier
  produces ImportError at collection time. This guard surfaces a clear error
  immediately rather than a confusing import traceback.

Shared client fixture (Issue #1451):
  httpx.ASGITransport does not trigger the FastAPI lifespan handler, so
  per-file client fixtures that skip pool initialisation fail with
  "asyncpg pool is not initialised" when DATABASE_URL is set.
  This conftest provides a single authoritative client fixture that
  initialises and tears down the pool within each test function's event loop.
  Per-file client fixtures have been removed; this definition takes effect
  for all test_m*.py and tests/integration/ files.
"""
from __future__ import annotations

import os
import sys
from typing import TYPE_CHECKING

import httpx
import pytest
import pytest_asyncio

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator


def pytest_configure(config: object) -> None:  # noqa: ARG001
    if sys.version_info < (3, 11):  # noqa: UP036 — intentional guard for misconfigured envs
        pytest.exit(
            f"\n\nPython 3.11+ is required — current interpreter is {sys.version}.\n"
            "The project uses datetime.UTC (3.11+) and targets Python 3.12.\n"
            "See docs/CONTRIBUTING.md §'Step 2: Python Environment' for setup instructions.\n"
            "Quick fix: cd backend && python3.12 -m venv .venv && source .venv/bin/activate\n",
            returncode=3,
        )


@pytest_asyncio.fixture()
async def client() -> AsyncGenerator[httpx.AsyncClient, None]:
    """httpx AsyncClient backed by ASGITransport with the asyncpg pool lifecycle.

    Initialises the asyncpg pool before yielding the client and closes it on
    teardown. Each test function gets its own pool instance (function-scoped
    event loop per pytest.ini asyncio_default_fixture_loop_scope = function).
    Skips the test when DATABASE_URL is not set.
    """
    if not os.environ.get("DATABASE_URL"):
        pytest.skip("DATABASE_URL not set — integration test requires a live database")
    from app.db.connection import close_asyncpg_pool, create_asyncpg_pool
    from app.main import app

    await create_asyncpg_pool()
    try:
        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app),
            base_url="http://test",
            timeout=180.0,
        ) as ac:
            yield ac
    finally:
        await close_asyncpg_pool()
