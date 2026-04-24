"""Backtesting conftest — asyncpg pool lifecycle.

httpx.ASGITransport does not trigger the FastAPI lifespan startup handler, so
the asyncpg pool is never initialised when tests use ASGITransport directly.
This conftest fills that gap: it calls create_asyncpg_pool() once at session
start and close_asyncpg_pool() at session end, matching the behaviour of the
production lifespan handler in app/main.py.

asyncpg 0.30 pools are not bound to the event loop in which they were created.
Connections acquired by function-scoped test loops work correctly against a
pool initialised in a separate asyncio.run() call. Issue #136.
"""
from __future__ import annotations

import asyncio
import os
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from collections.abc import Generator

_DATABASE_URL = os.environ.get("DATABASE_URL", "")


@pytest.fixture(scope="session", autouse=True)
def _asyncpg_pool_lifecycle() -> Generator[None, None, None]:
    """Initialize the asyncpg pool before the backtesting session.

    Skips the entire session when DATABASE_URL is not set, so backtesting
    tests continue to skip gracefully in environments without a database.
    """
    if not _DATABASE_URL:
        pytest.skip("DATABASE_URL not set — skipping backtesting session")
        return  # unreachable; satisfies type checker

    from app.db.connection import close_asyncpg_pool, create_asyncpg_pool

    asyncio.run(create_asyncpg_pool())
    yield
    asyncio.run(close_asyncpg_pool())
