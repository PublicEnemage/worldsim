"""m16_g4_quantity_synthetic_fields — ADR-007 §Consequences step 1, Issue #22 (scoped)

Revision ID: a2c4e6f8b0d1
Revises: 2b821063ef81
Create Date: 2026-06-24

Creates the `quantity` table with four synthetic-data disclosure fields required by
ADR-007 §Consequences §Implementation Sequence step 1:

  is_synthetic        BOOLEAN NOT NULL DEFAULT FALSE
  synthetic_method    VARCHAR nullable — STRUCTURAL_ABSENCE | SYNTHETIC_COMPARABLE | SYNTHETIC_MODEL
  comparison_group_id VARCHAR nullable — reserved for Method A (Hierarchical Bayesian, G4+ scope)
  holdout_validated   BOOLEAN nullable — True when SYNTHETIC_COMPARABLE estimate holdout-validated

The table is a structured companion to the simulation_entities.attributes JSONB store.
JSONB remains the primary ephemeral state carrier during scenario execution; the quantity
table provides a relational anchor for synthetic-data metadata that must persist across
sessions and be queryable independently of snapshot state_data blobs.

Non-regression guarantee: existing scenario runs are unaffected. The migration only
creates a new table — no columns are added to existing tables, no existing data is altered.
The `is_synthetic` default (FALSE) ensures all existing Quantity values are treated as
non-synthetic until the SyntheticDataEngine assigns inference results.
"""
from __future__ import annotations

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "a2c4e6f8b0d1"
down_revision = "2b821063ef81"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "quantity",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("entity_id", sa.String(), nullable=True),
        sa.Column("scenario_id", sa.String(), nullable=True),
        sa.Column("indicator_key", sa.String(), nullable=True),
        sa.Column("value", sa.String(), nullable=True),
        sa.Column("unit", sa.String(), nullable=True),
        sa.Column("variable_type", sa.String(), nullable=True),
        sa.Column("confidence_tier", sa.Integer(), nullable=True),
        # ADR-007 §Consequences step 1 — four synthetic-data disclosure fields
        sa.Column(
            "is_synthetic",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("FALSE"),
        ),
        sa.Column("synthetic_method", sa.String(), nullable=True),
        sa.Column("comparison_group_id", sa.String(), nullable=True),
        sa.Column("holdout_validated", sa.Boolean(), nullable=True),
    )


def downgrade() -> None:
    op.drop_table("quantity")
