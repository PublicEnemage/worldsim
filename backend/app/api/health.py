"""Health check endpoint — GET /health."""
from __future__ import annotations

from typing import Annotated

import asyncpg  # noqa: TCH002 — used in Annotated[] resolved at runtime by FastAPI
from fastapi import APIRouter, Depends

from app.api.deps import get_db  # noqa: TCH001 — used as Depends(get_db) at runtime
from app.schemas import HealthResponse

router = APIRouter(prefix="/health", tags=["health"])

_VERSION = "0.2.0"


@router.get("/", response_model=HealthResponse)
async def health(
    conn: Annotated[asyncpg.Connection, Depends(get_db)],
) -> HealthResponse:
    """Return API health status and database connectivity.

    The `db` field is `connected` when a SELECT 1 succeeds, `error` otherwise.
    """
    try:
        await conn.fetchval("SELECT 1")
        db_status = "connected"
    except Exception:  # noqa: BLE001
        db_status = "error"

    return HealthResponse(status="ok", version=_VERSION, db=db_status)
