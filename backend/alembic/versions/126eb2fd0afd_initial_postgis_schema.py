"""initial PostGIS schema

Revision ID: 126eb2fd0afd
Revises:
Create Date: 2026-04-20

ADR-003 Decision 1 — five tables:
  simulation_entities       (Entity)
  relationships             (Relationship)
  territorial_designations  (TerritorialDesignation)
  source_registry           (SourceRegistration)
  control_input_audit_log   (AuditLogRecord)

PostGIS extension is required on the target database before this migration
runs. Create it manually or via a superuser script:
  CREATE EXTENSION IF NOT EXISTS postgis;

GeoAlchemy2 renders GEOGRAPHY columns as native PostGIS geography types.
"""
from __future__ import annotations

import sqlalchemy as sa
from geoalchemy2 import Geometry
from sqlalchemy.dialects.postgresql import ARRAY, JSONB

from alembic import op

# revision identifiers
revision = "126eb2fd0afd"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ------------------------------------------------------------------
    # simulation_entities
    # ------------------------------------------------------------------
    op.create_table(
        "simulation_entities",
        sa.Column("entity_id", sa.String(), nullable=False),
        sa.Column("entity_type", sa.String(), nullable=False),
        sa.Column("parent_id", sa.String(), nullable=True),
        sa.Column(
            "geometry",
            Geometry(geometry_type="MULTIPOLYGON", srid=4326, spatial_index=False),
            nullable=True,
        ),
        sa.Column("attributes", JSONB(), nullable=False, server_default="{}"),
        sa.Column("metadata", JSONB(), nullable=False, server_default="{}"),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("NOW()"),
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("NOW()"),
        ),
        sa.ForeignKeyConstraint(
            ["parent_id"],
            ["simulation_entities.entity_id"],
            name="fk_entities_parent",
        ),
        sa.PrimaryKeyConstraint("entity_id"),
    )
    # GiST spatial index on geometry — required for choropleth endpoint
    op.create_index(
        "idx_entities_geometry",
        "simulation_entities",
        ["geometry"],
        postgresql_using="gist",
    )
    # B-tree on parent_id for hierarchy traversal (filtered — NULLs excluded)
    op.create_index(
        "idx_entities_parent_id",
        "simulation_entities",
        ["parent_id"],
        postgresql_where=sa.text("parent_id IS NOT NULL"),
    )
    op.create_index(
        "idx_entities_type",
        "simulation_entities",
        ["entity_type"],
    )
    # GIN index on JSONB attributes — enables @>, ?, ?| operators
    op.create_index(
        "idx_entities_attributes_gin",
        "simulation_entities",
        ["attributes"],
        postgresql_using="gin",
    )

    # ------------------------------------------------------------------
    # relationships
    # ------------------------------------------------------------------
    op.create_table(
        "relationships",
        sa.Column("relationship_id", sa.String(), nullable=False),
        sa.Column("source_id", sa.String(), nullable=False),
        sa.Column("target_id", sa.String(), nullable=False),
        sa.Column("relationship_type", sa.String(), nullable=False),
        sa.Column("weight", sa.Numeric(), nullable=False),
        sa.Column("attributes", JSONB(), nullable=False, server_default="{}"),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("NOW()"),
        ),
        sa.ForeignKeyConstraint(
            ["source_id"],
            ["simulation_entities.entity_id"],
            name="fk_relationships_source",
        ),
        sa.ForeignKeyConstraint(
            ["target_id"],
            ["simulation_entities.entity_id"],
            name="fk_relationships_target",
        ),
        sa.PrimaryKeyConstraint("relationship_id"),
    )
    op.create_index("idx_relationships_source", "relationships", ["source_id"])
    op.create_index("idx_relationships_target", "relationships", ["target_id"])
    op.create_index("idx_relationships_type", "relationships", ["relationship_type"])

    # ------------------------------------------------------------------
    # territorial_designations
    # ------------------------------------------------------------------
    op.create_table(
        "territorial_designations",
        sa.Column("entity_id", sa.String(), nullable=False),
        sa.Column("de_facto_admin", sa.String(), nullable=False),
        sa.Column("de_jure_claimants", ARRAY(sa.String()), nullable=False),
        sa.Column("dispute_status", sa.String(), nullable=False),
        sa.Column("effective_date", sa.Date(), nullable=False),
        sa.Column("source", sa.Text(), nullable=False),
        sa.Column("display_note", sa.Text(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("NOW()"),
        ),
        sa.ForeignKeyConstraint(
            ["entity_id"],
            ["simulation_entities.entity_id"],
            name="fk_territorial_entity",
        ),
        sa.PrimaryKeyConstraint("entity_id", "effective_date"),
    )

    # ------------------------------------------------------------------
    # source_registry
    # ------------------------------------------------------------------
    op.create_table(
        "source_registry",
        sa.Column("source_id", sa.String(), nullable=False),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("provider", sa.Text(), nullable=False),
        sa.Column("dataset_name", sa.Text(), nullable=False),
        sa.Column("version", sa.Text(), nullable=False),
        sa.Column("permanent_url", sa.Text(), nullable=False),
        sa.Column("access_date", sa.Date(), nullable=False),
        sa.Column("license", sa.Text(), nullable=False),
        sa.Column("coverage_start", sa.Date(), nullable=False),
        sa.Column("coverage_end", sa.Date(), nullable=True),
        sa.Column(
            "coverage_countries", ARRAY(sa.String()), nullable=False, server_default="{}"
        ),
        sa.Column("quality_tier", sa.Integer(), nullable=False),
        sa.Column(
            "simulation_variables", ARRAY(sa.String()), nullable=False, server_default="{}"
        ),
        sa.Column("known_limitations", sa.Text(), nullable=False, server_default=""),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("NOW()"),
        ),
        sa.CheckConstraint(
            "quality_tier BETWEEN 1 AND 5", name="ck_source_quality_tier"
        ),
        sa.PrimaryKeyConstraint("source_id"),
    )

    # ------------------------------------------------------------------
    # control_input_audit_log
    # Pays the ADR-002 deferred persistence debt — in-memory AuditLog
    # from Milestone 1 is now persisted to PostgreSQL.
    # ------------------------------------------------------------------
    op.create_table(
        "control_input_audit_log",
        sa.Column("record_id", sa.String(), nullable=False),
        sa.Column("scenario_id", sa.String(), nullable=False),
        sa.Column("session_id", sa.String(), nullable=False),
        sa.Column("timestep", sa.DateTime(timezone=True), nullable=False),
        sa.Column("input_type", sa.String(), nullable=False),
        sa.Column("source", sa.String(), nullable=False),
        sa.Column("actor_id", sa.String(), nullable=False),
        sa.Column("actor_role", sa.String(), nullable=False),
        sa.Column("justification", sa.Text(), nullable=False),
        sa.Column("raw_input", JSONB(), nullable=False),
        sa.Column(
            "translated_events", ARRAY(sa.String()), nullable=False, server_default="{}"
        ),
        sa.Column(
            "wall_clock_time",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("NOW()"),
        ),
        sa.PrimaryKeyConstraint("record_id"),
    )
    op.create_index(
        "idx_audit_scenario_timestep",
        "control_input_audit_log",
        ["scenario_id", "timestep"],
    )


def downgrade() -> None:
    op.drop_table("control_input_audit_log")
    op.drop_table("source_registry")
    op.drop_table("territorial_designations")
    op.drop_index("idx_relationships_type", table_name="relationships")
    op.drop_index("idx_relationships_target", table_name="relationships")
    op.drop_index("idx_relationships_source", table_name="relationships")
    op.drop_table("relationships")
    op.drop_index("idx_entities_attributes_gin", table_name="simulation_entities")
    op.drop_index("idx_entities_type", table_name="simulation_entities")
    op.drop_index("idx_entities_parent_id", table_name="simulation_entities")
    op.drop_index("idx_entities_geometry", table_name="simulation_entities")
    op.drop_table("simulation_entities")
