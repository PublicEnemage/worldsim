"""scenario_deleted_tombstones — ADR-004 Decision 1 Amendment (CONFLICT C-1 disposition)

Revision ID: 8b2c4e6f1a3d
Revises: 3a9f2c1d8e47
Create Date: 2026-04-24

Tombstone table for deleted scenarios. Written by DELETE /scenarios/{id} before
CASCADE removes scenario_scheduled_inputs and scenario_state_snapshots. Satisfies
the C-1 disposition: full configuration and scheduled_inputs JSONB preserved so
scenario output can be reconstructed from first principles (SA-11 determinism).

Fields:
  scenario_id          — original PK, preserved as tombstone identifier
  name                 — display name at time of deletion
  configuration        — full ScenarioConfigSchema JSONB
  scheduled_inputs     — full scheduled_inputs array in step order
  engine_version       — WorldSim API version string at deletion time
  original_created_at  — original scenario creation timestamp
  deleted_at           — deletion timestamp (default NOW())
  deleted_by           — actor identifier ('api' for M3; authenticated identity in M4+)
"""
from __future__ import annotations

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB

from alembic import op

revision = "8b2c4e6f1a3d"
down_revision = "3a9f2c1d8e47"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "scenario_deleted_tombstones",
        sa.Column("scenario_id", sa.Text(), primary_key=True, nullable=False),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("configuration", JSONB(), nullable=False),
        sa.Column("scheduled_inputs", JSONB(), nullable=False),
        sa.Column("engine_version", sa.Text(), nullable=False),
        sa.Column(
            "original_created_at",
            sa.DateTime(timezone=True),
            nullable=False,
        ),
        sa.Column(
            "deleted_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("NOW()"),
        ),
        sa.Column("deleted_by", sa.Text(), nullable=False),
    )
    op.create_index(
        "idx_tombstones_deleted_at",
        "scenario_deleted_tombstones",
        ["deleted_at"],
    )


def downgrade() -> None:
    op.drop_index("idx_tombstones_deleted_at", table_name="scenario_deleted_tombstones")
    op.drop_table("scenario_deleted_tombstones")
