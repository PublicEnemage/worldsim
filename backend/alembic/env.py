"""Alembic migration environment — ADR-003.

Reads DATABASE_URL from the environment. Imports all ORM models so that
autogenerate can discover the full schema via Base.metadata.

Sync (offline) and async (online) migration modes are both supported.
The online mode uses asyncpg via SQLAlchemy's async engine.
"""
from __future__ import annotations

import asyncio
import os
from logging.config import fileConfig
from typing import TYPE_CHECKING

from sqlalchemy import pool
from sqlalchemy.ext.asyncio import async_engine_from_config

import app.db.models  # noqa: F401 — registers all table metadata on Base
from alembic import context
from app.db.base import Base  # noqa: F401

if TYPE_CHECKING:
    from sqlalchemy.engine import Connection

target_metadata = Base.metadata

# Alembic config object
config = context.config

# Override sqlalchemy.url with DATABASE_URL environment variable.
# This keeps credentials out of alembic.ini and version control.
_db_url = os.environ.get("DATABASE_URL")
if _db_url:
    # Alembic needs a sync psycopg2 URL; strip async scheme if present.
    _sync_url = _db_url
    for prefix in ("postgresql+asyncpg://", "postgres+asyncpg://"):
        if _db_url.startswith(prefix):
            _sync_url = _db_url.replace(prefix, "postgresql://", 1)
            break
    config.set_main_option("sqlalchemy.url", _sync_url)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)


def run_migrations_offline() -> None:
    """Run migrations in offline mode — generates SQL without a DB connection."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        include_schemas=True,
    )
    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        include_schemas=True,
    )
    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)
    await connectable.dispose()


def run_migrations_online() -> None:
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
