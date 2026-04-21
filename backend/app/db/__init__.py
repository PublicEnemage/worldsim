"""
Database package — ADR-003 PostGIS foundation.

Provides SQLAlchemy async engine, ORM models for the five ADR-003 tables,
TerritorialValidator, and seed loaders.

Runtime query access uses asyncpg directly (not ORM) per ADR-003 Decision 2.
SQLAlchemy ORM models are used for schema definition and Alembic migrations only.
"""
