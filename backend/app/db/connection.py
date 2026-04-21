"""
Database connection — SQLAlchemy async engine and asyncpg pool.

ADR-003 Decision 2: runtime queries use asyncpg directly for performance.
SQLAlchemy engine is provided for Alembic migrations and schema management.

DATABASE_URL must be a PostgreSQL URL. The module normalises it to the
postgresql+asyncpg:// scheme required by SQLAlchemy's async driver.

Environment variable: DATABASE_URL
Example: postgresql://worldsim:password@localhost:5432/worldsim
"""
from __future__ import annotations

import os
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator

import asyncpg
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)


def _async_url(url: str) -> str:
    """Normalise a postgresql:// URL to the postgresql+asyncpg:// scheme."""
    for prefix in ("postgresql://", "postgres://"):
        if url.startswith(prefix):
            return url.replace(prefix, "postgresql+asyncpg://", 1)
    return url


_DATABASE_URL: str = os.environ.get("DATABASE_URL", "")


def _get_engine() -> AsyncEngine:
    """Return the SQLAlchemy async engine, creating it on first call.

    Deferred to avoid a module-level failure when DATABASE_URL is absent
    (e.g., during test collection without a database configured).
    """
    url = _async_url(_DATABASE_URL)
    if not url:
        raise RuntimeError(
            "DATABASE_URL environment variable is not set. "
            "Set it before importing the database connection module."
        )
    return create_async_engine(url, pool_pre_ping=True, echo=False)


def _get_session_factory() -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(_get_engine(), class_=AsyncSession, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Yield a SQLAlchemy async session; roll back on exception, close on exit."""
    async with _get_session_factory()() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


# asyncpg connection pool — used by FastAPI endpoint handlers per ADR-003.
# Initialised by create_asyncpg_pool() at application startup.
_asyncpg_pool: asyncpg.Pool | None = None


async def create_asyncpg_pool() -> None:
    """Create the asyncpg connection pool from DATABASE_URL.

    Called once at FastAPI application startup (lifespan context manager).
    Raises RuntimeError if DATABASE_URL is not set.
    """
    global _asyncpg_pool  # noqa: PLW0603 — module-level pool singleton
    if not _DATABASE_URL:
        raise RuntimeError(
            "DATABASE_URL environment variable is not set. "
            "Set it to a PostgreSQL connection URL before starting the application."
        )
    _asyncpg_pool = await asyncpg.create_pool(_DATABASE_URL, min_size=2, max_size=10)


async def close_asyncpg_pool() -> None:
    """Close the asyncpg pool at application shutdown."""
    global _asyncpg_pool  # noqa: PLW0603
    if _asyncpg_pool is not None:
        await _asyncpg_pool.close()
        _asyncpg_pool = None


def get_asyncpg_pool() -> asyncpg.Pool:
    """Return the asyncpg pool. Raises RuntimeError if not yet initialised."""
    if _asyncpg_pool is None:
        raise RuntimeError(
            "asyncpg pool is not initialised. "
            "Ensure create_asyncpg_pool() was called at application startup."
        )
    return _asyncpg_pool
