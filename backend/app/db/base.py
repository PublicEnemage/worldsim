"""SQLAlchemy declarative base for all WorldSim ORM models."""
from __future__ import annotations

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Common base class for all ORM models.

    All five ADR-003 table models inherit from this base so that
    Alembic autogenerate can discover them via Base.metadata.
    """
