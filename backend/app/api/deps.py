"""FastAPI dependency injection — database connection provider."""
from __future__ import annotations

from typing import TYPE_CHECKING

import asyncpg  # noqa: TCH002

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator

from app.db.connection import get_asyncpg_pool


async def get_db() -> AsyncGenerator[asyncpg.Connection, None]:
    """Yield an asyncpg connection from the shared pool.

    Acquires a connection at request start and releases it on completion.
    Per ADR-003 Decision 2: asyncpg is used directly for all runtime queries;
    SQLAlchemy ORM is reserved for schema management and Alembic migrations.
    """
    pool = get_asyncpg_pool()
    async with pool.acquire() as conn:
        yield conn
