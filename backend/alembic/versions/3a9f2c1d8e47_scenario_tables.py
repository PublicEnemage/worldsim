"""scenario tables — ADR-004 Decision 1

Revision ID: 3a9f2c1d8e47
Revises: 126eb2fd0afd
Create Date: 2026-04-23

Three tables introduced for Milestone 3 scenario engine:
  scenarios                 — scenario configuration record
  scenario_scheduled_inputs — ControlInput records bound to a scenario step
  scenario_state_snapshots  — simulation state snapshots per step

All cascade deletes flow from scenarios outward. Snapshots carry
ia1_disclosure as NOT NULL — enforces the IA-1 Known Limitation text at
the database level (application code cannot omit it).
"""
from __future__ import annotations

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB

from alembic import op

revision = "3a9f2c1d8e47"
down_revision = "126eb2fd0afd"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "scenarios",
        sa.Column(
            "scenario_id",
            sa.Text,
            primary_key=True,
            server_default=sa.text("gen_random_uuid()::text"),
        ),
        sa.Column("name", sa.Text, nullable=False),
        sa.Column("description", sa.Text, nullable=True),
        sa.Column(
            "status",
            sa.Text,
            nullable=False,
            server_default="pending",
        ),
        sa.Column("configuration", JSONB, nullable=False),
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
        sa.Column("version", sa.Integer, nullable=False, server_default="1"),
        sa.CheckConstraint(
            "status IN ('pending', 'running', 'completed', 'failed')",
            name="ck_scenarios_status",
        ),
    )
    op.create_index("idx_scenarios_status", "scenarios", ["status"])

    op.create_table(
        "scenario_scheduled_inputs",
        sa.Column(
            "id",
            sa.Text,
            primary_key=True,
            server_default=sa.text("gen_random_uuid()::text"),
        ),
        sa.Column(
            "scenario_id",
            sa.Text,
            sa.ForeignKey("scenarios.scenario_id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("step", sa.Integer, nullable=False),
        sa.Column("input_type", sa.Text, nullable=False),
        sa.Column("input_data", JSONB, nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("NOW()"),
        ),
    )
    op.create_index(
        "idx_ssi_scenario_step",
        "scenario_scheduled_inputs",
        ["scenario_id", "step"],
    )

    op.create_table(
        "scenario_state_snapshots",
        sa.Column(
            "id",
            sa.Text,
            primary_key=True,
            server_default=sa.text("gen_random_uuid()::text"),
        ),
        sa.Column(
            "scenario_id",
            sa.Text,
            sa.ForeignKey("scenarios.scenario_id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("step", sa.Integer, nullable=False),
        sa.Column("timestep", sa.DateTime(timezone=True), nullable=False),
        sa.Column("state_data", JSONB, nullable=False),
        sa.Column("ia1_disclosure", sa.Text, nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("NOW()"),
        ),
        sa.UniqueConstraint("scenario_id", "step", name="uq_snapshots_scenario_step"),
    )
    op.create_index(
        "idx_sss_scenario_step",
        "scenario_state_snapshots",
        ["scenario_id", "step"],
    )


def downgrade() -> None:
    op.drop_table("scenario_state_snapshots")
    op.drop_table("scenario_scheduled_inputs")
    op.drop_table("scenarios")
