"""WorldSim API — FastAPI application entry point.

ADR-003 Decision 2: FastAPI layer serving entity data and choropleth variable
data to the MapLibre GL frontend.

CORS policy: all origins allowed for Milestone 2 local development scope.
This is a known limitation — production CORS policy is ADR-007 scope,
deferred until authentication is introduced in Milestone 3.
"""
from __future__ import annotations

from contextlib import asynccontextmanager
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.countries import router as countries_router
from app.api.health import router as health_router
from app.api.scenarios import router as scenarios_router
from app.db.connection import close_asyncpg_pool, create_asyncpg_pool


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Manage asyncpg connection pool lifecycle.

    Initialises the pool on startup and closes it on shutdown.
    The pool is shared across all request handlers per ADR-003 Decision 2.
    """
    await create_asyncpg_pool()
    yield
    await close_asyncpg_pool()


app = FastAPI(
    title="WorldSim API",
    version="0.3.0",
    description=(
        "Geopolitical-economic simulation platform — Milestone 3 API. "
        "Serves country entity data, choropleth attribute data, and scenario "
        "configuration for MapLibre GL."
    ),
    lifespan=lifespan,
)

# KNOWN LIMITATION: all origins permitted for Milestone 3 development.
# Production CORS policy is ADR-007 scope (post-Milestone 3).
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST", "DELETE", "PATCH"],
    allow_headers=["*"],
)

_API_PREFIX = "/api/v1"

app.include_router(health_router, prefix=_API_PREFIX)
app.include_router(countries_router, prefix=_API_PREFIX)
app.include_router(scenarios_router, prefix=_API_PREFIX)
