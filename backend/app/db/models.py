"""
SQLAlchemy ORM models — ADR-003 PostGIS schema.

Five tables following the ADR-003 Decision 1 schema:
  Entity                → simulation_entities
  Relationship          → relationships
  TerritorialDesignation → territorial_designations
  SourceRegistration    → source_registry
  AuditLogRecord        → control_input_audit_log

These models are used for schema definition and Alembic migrations.
Runtime query access uses asyncpg directly per ADR-003 Decision 2.

JSONB attribute storage: Entity.attributes stores Dict[str, Quantity] as
JSONB. The value field of each Quantity is stored as a string (Decimal
serialised to str) to preserve precision. See ADR-003 § Quantity JSONB
Envelope for the wire format specification.
"""
from __future__ import annotations

from datetime import date, datetime  # noqa: TCH003
from typing import Any

from geoalchemy2 import Geometry
from sqlalchemy import (
    ARRAY,
    CheckConstraint,
    Date,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    Numeric,
    String,
    Text,
    func,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Entity(Base):
    """A simulation entity — country, region, or institution.

    Corresponds to the simulation_entities table in ADR-003.

    attributes is a JSONB column storing Dict[str, Quantity] where each
    Quantity's value field is serialised as a string (Decimal → str) to
    enforce the float prohibition from DATA_STANDARDS.md. The full Quantity
    envelope (value, unit, variable_type, confidence_tier, observation_date,
    source_registry_id, measurement_framework) is stored per attribute key.
    """

    __tablename__ = "simulation_entities"

    entity_id: Mapped[str] = mapped_column(String, primary_key=True)
    entity_type: Mapped[str] = mapped_column(String, nullable=False)
    parent_id: Mapped[str | None] = mapped_column(
        String, ForeignKey("simulation_entities.entity_id"), nullable=True
    )
    # GEOGRAPHY stores coordinates on the WGS-84 spheroid; great-circle
    # distance and area calculations are correct without projection transforms.
    geometry: Mapped[Any | None] = mapped_column(
        Geometry(geometry_type="MULTIPOLYGON", srid=4326, spatial_index=False),
        nullable=True,
    )
    # JSONB attribute store — see module docstring for envelope format.
    attributes: Mapped[dict[str, Any]] = mapped_column(
        JSONB, nullable=False, server_default="{}"
    )
    metadata_: Mapped[dict[str, Any]] = mapped_column(
        "metadata", JSONB, nullable=False, server_default="{}"
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    # Relationships
    children: Mapped[list[Entity]] = relationship(
        "Entity", back_populates="parent", foreign_keys=[parent_id]
    )
    parent: Mapped[Entity | None] = relationship(
        "Entity", back_populates="children", remote_side="Entity.entity_id"
    )
    territorial_designations: Mapped[list[TerritorialDesignation]] = relationship(
        "TerritorialDesignation", back_populates="entity"
    )
    source_relationships: Mapped[list[Relationship]] = relationship(
        "Relationship",
        back_populates="source_entity",
        foreign_keys="Relationship.source_id",
    )
    target_relationships: Mapped[list[Relationship]] = relationship(
        "Relationship",
        back_populates="target_entity",
        foreign_keys="Relationship.target_id",
    )

    __table_args__ = (
        # GiST spatial index — required for ST_Intersects, ST_DWithin,
        # spatial joins in the choropleth endpoint.
        Index("idx_entities_geometry", "geometry", postgresql_using="gist"),
        # B-tree index — hierarchy traversal (parent → children lookups).
        Index(
            "idx_entities_parent_id",
            "parent_id",
            postgresql_where="parent_id IS NOT NULL",
        ),
        # B-tree index — entity type filter ("all countries").
        Index("idx_entities_type", "entity_type"),
        # GIN index — JSONB attribute key access (@>, ?, ?| operators).
        Index(
            "idx_entities_attributes_gin",
            "attributes",
            postgresql_using="gin",
        ),
    )


class Relationship(Base):
    """A directed weighted relationship between two entities.

    Corresponds to the relationships table in ADR-003. Carries propagation
    weight and relationship-specific attributes as JSONB.
    """

    __tablename__ = "relationships"

    relationship_id: Mapped[str] = mapped_column(String, primary_key=True)
    source_id: Mapped[str] = mapped_column(
        String, ForeignKey("simulation_entities.entity_id"), nullable=False
    )
    target_id: Mapped[str] = mapped_column(
        String, ForeignKey("simulation_entities.entity_id"), nullable=False
    )
    relationship_type: Mapped[str] = mapped_column(String, nullable=False)
    # NUMERIC not float — propagation weights are model parameters; NUMERIC
    # preserves the value exactly without IEEE 754 rounding.
    weight: Mapped[float] = mapped_column(Numeric, nullable=False)
    attributes: Mapped[dict[str, Any]] = mapped_column(
        JSONB, nullable=False, server_default="{}"
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    source_entity: Mapped[Entity] = relationship(
        "Entity", back_populates="source_relationships", foreign_keys=[source_id]
    )
    target_entity: Mapped[Entity] = relationship(
        "Entity", back_populates="target_relationships", foreign_keys=[target_id]
    )

    __table_args__ = (
        Index("idx_relationships_source", "source_id"),
        Index("idx_relationships_target", "target_id"),
        Index("idx_relationships_type", "relationship_type"),
    )


class TerritorialDesignation(Base):
    """Declared territorial position for a disputed or high-risk entity.

    Corresponds to the territorial_designations table in ADR-003.
    Every entity identified in DATA_STANDARDS.md § High-Risk Specific Cases
    must have a row here before its Entity record can be inserted — enforced
    by TerritorialValidator.

    Composite primary key (entity_id, effective_date) supports historical
    territorial changes (e.g., Crimea administrative change 2014).
    """

    __tablename__ = "territorial_designations"

    entity_id: Mapped[str] = mapped_column(
        String, ForeignKey("simulation_entities.entity_id"), primary_key=True
    )
    de_facto_admin: Mapped[str] = mapped_column(String, nullable=False)
    de_jure_claimants: Mapped[list[str]] = mapped_column(
        ARRAY(String), nullable=False
    )
    dispute_status: Mapped[str] = mapped_column(String, nullable=False)
    effective_date: Mapped[date] = mapped_column(Date, primary_key=True, nullable=False)
    source: Mapped[str] = mapped_column(Text, nullable=False)
    display_note: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    entity: Mapped[Entity] = relationship(
        "Entity", back_populates="territorial_designations"
    )


class SourceRegistration(Base):
    """Provenance record for a data source used in the simulation.

    Corresponds to the source_registry table in ADR-003.
    Every ingestion pipeline must register its source here before writing
    any simulation data — enforced at the pipeline boundary.

    See DATA_STANDARDS.md § Data Provenance Requirements for the full
    SourceRegistration contract.
    """

    __tablename__ = "source_registry"

    source_id: Mapped[str] = mapped_column(String, primary_key=True)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    provider: Mapped[str] = mapped_column(Text, nullable=False)
    dataset_name: Mapped[str] = mapped_column(Text, nullable=False)
    version: Mapped[str] = mapped_column(Text, nullable=False)
    permanent_url: Mapped[str] = mapped_column(Text, nullable=False)
    access_date: Mapped[date] = mapped_column(Date, nullable=False)
    license: Mapped[str] = mapped_column(Text, nullable=False)
    coverage_start: Mapped[date] = mapped_column(Date, nullable=False)
    coverage_end: Mapped[date | None] = mapped_column(Date, nullable=True)
    coverage_countries: Mapped[list[str]] = mapped_column(
        ARRAY(String), nullable=False, server_default="{}"
    )
    quality_tier: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        info={"check": "quality_tier BETWEEN 1 AND 5"},
    )
    simulation_variables: Mapped[list[str]] = mapped_column(
        ARRAY(String), nullable=False, server_default="{}"
    )
    known_limitations: Mapped[str] = mapped_column(
        Text, nullable=False, server_default=""
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    __table_args__ = (
        CheckConstraint("quality_tier BETWEEN 1 AND 5", name="ck_source_quality_tier"),
    )


class AuditLogRecord(Base):
    """Persistent record of a control input processed by the orchestrator.

    Corresponds to the control_input_audit_log table in ADR-003.
    Pays the ADR-002 deferred debt: in Milestone 1 the AuditLog was
    in-memory only. This table makes it persistent.

    Scenarios are reproducible by replaying their audit logs in
    (scenario_id, timestep) order. The raw_input JSONB carries the full
    serialised ControlInput. translated_events carries the event_ids of
    generated Events.
    """

    __tablename__ = "control_input_audit_log"

    record_id: Mapped[str] = mapped_column(String, primary_key=True)
    scenario_id: Mapped[str] = mapped_column(String, nullable=False)
    session_id: Mapped[str] = mapped_column(String, nullable=False)
    timestep: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    input_type: Mapped[str] = mapped_column(String, nullable=False)
    source: Mapped[str] = mapped_column(String, nullable=False)
    actor_id: Mapped[str] = mapped_column(String, nullable=False)
    actor_role: Mapped[str] = mapped_column(String, nullable=False)
    justification: Mapped[str] = mapped_column(Text, nullable=False)
    raw_input: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False)
    translated_events: Mapped[list[str]] = mapped_column(
        ARRAY(String), nullable=False, server_default="{}"
    )
    wall_clock_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    __table_args__ = (
        Index(
            "idx_audit_scenario_timestep",
            "scenario_id",
            "timestep",
        ),
    )


# Expose all models so Alembic env.py can discover them via Base.metadata.
__all__ = [
    "Base",
    "Entity",
    "Relationship",
    "TerritorialDesignation",
    "SourceRegistration",
    "AuditLogRecord",
]
