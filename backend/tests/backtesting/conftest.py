"""Backtesting conftest — asyncpg pool lifecycle.

httpx.ASGITransport does not trigger the FastAPI lifespan startup handler, so
the asyncpg pool is never initialised when tests use ASGITransport directly.
This conftest fills that gap: it calls create_asyncpg_pool() once at session
start and close_asyncpg_pool() at session end, matching the behaviour of the
production lifespan handler in app/main.py.

The fixture is async with loop_scope="session" so the pool is created in the
same event loop that test functions run in. The original sync implementation
(asyncio.run()) created the pool in a temporary loop that was immediately
closed — asyncpg's eager min_size connections were then bound to that closed
loop, causing "Future attached to a different loop" errors at test run time.
"""
from __future__ import annotations

import os
from typing import TYPE_CHECKING

import pytest
import pytest_asyncio

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator

_DATABASE_URL = os.environ.get("DATABASE_URL", "")


@pytest_asyncio.fixture(scope="session", loop_scope="session", autouse=True)
async def _asyncpg_pool_lifecycle() -> AsyncGenerator[None, None]:
    """Initialize the asyncpg pool before the backtesting session.

    Skips the entire session when DATABASE_URL is not set, so backtesting
    tests continue to skip gracefully in environments without a database.
    """
    if not _DATABASE_URL:
        pytest.skip("DATABASE_URL not set — skipping backtesting session")
        return

    from app.db.connection import close_asyncpg_pool, create_asyncpg_pool

    await create_asyncpg_pool()
    yield
    await close_asyncpg_pool()
