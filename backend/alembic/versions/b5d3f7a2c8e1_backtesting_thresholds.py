"""backtesting_thresholds — Issue #194 (ADR-006 Decision 11)

Revision ID: b5d3f7a2c8e1
Revises: e9f3b2c5a1d7
Create Date: 2026-05-03

New table: backtesting_thresholds

Stores fidelity thresholds for all registered backtesting cases.
Each row defines one pass/fail criterion for a specific attribute at a
specific simulation step, compared against a historical actual.

Three threshold types (threshold_type CHECK constraint):
  DIRECTION_ONLY       — simulated value must match expected_direction sign.
                         ci_coverage = NULL. tolerance_pct = NULL.
  MAGNITUDE            — |simulated - expected| ≤ tolerance_pct × |expected|.
                         ci_coverage = NULL. expected_value and tolerance_pct required.
  DISTRIBUTION_COMBINED — M5 distribution outputs (ADR-006 Decision 11).
                         Both pass conditions must hold:
                           1. mean within ±tolerance_pct of expected_value
                           2. expected_value within the ci_coverage CI
                         ci_coverage required (e.g. 0.80 = 80th-percentile CI).

No seed data in this migration — Greece DIRECTION_ONLY rows and Argentina
DISTRIBUTION_COMBINED rows are seeded via separate data migrations (Issue #192).

Evaluation logic in Python: app.simulation.backtesting.threshold_types.
"""
from __future__ import annotations

import sqlalchemy as sa

from alembic import op

revision = "b5d3f7a2c8e1"
down_revision = "e9f3b2c5a1d7"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "backtesting_thresholds",
        sa.Column(
            "threshold_id",
            sa.Text(),
            primary_key=True,
            nullable=False,
            server_default=sa.text("gen_random_uuid()::text"),
        ),
        sa.Column("case_id", sa.Text(), nullable=False),
        sa.Column("threshold_name", sa.Text(), nullable=False),
        sa.Column("threshold_type", sa.Text(), nullable=False),
        sa.Column("attribute_key", sa.Text(), nullable=False),
        sa.Column("entity_id", sa.Text(), nullable=False),
        sa.Column("step", sa.Integer(), nullable=False),
        # DIRECTION_ONLY: 'negative' | 'positive'. NULL for other types.
        sa.Column("expected_direction", sa.Text(), nullable=True),
        # MAGNITUDE / DISTRIBUTION_COMBINED: historical actual. NULL for DIRECTION_ONLY.
        sa.Column("expected_value", sa.Numeric(), nullable=True),
        # MAGNITUDE / DISTRIBUTION_COMBINED: ±tolerance fraction. NULL for DIRECTION_ONLY.
        sa.Column("tolerance_pct", sa.Numeric(), nullable=True),
        # DISTRIBUTION_COMBINED only: required CI coverage (e.g. 0.80). NULL for others.
        sa.Column("ci_coverage", sa.Numeric(), nullable=True),
        sa.Column("description", sa.Text(), nullable=False, server_default=""),
        sa.Column("source", sa.Text(), nullable=False, server_default=""),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("NOW()"),
        ),
        sa.CheckConstraint(
            "threshold_type IN ('DIRECTION_ONLY', 'MAGNITUDE', 'DISTRIBUTION_COMBINED')",
            name="ck_backtesting_threshold_type",
        ),
        sa.UniqueConstraint("case_id", "threshold_name", name="uq_backtesting_case_threshold"),
    )
    op.create_index("idx_backtesting_case_id", "backtesting_thresholds", ["case_id"])
    op.create_index(
        "idx_backtesting_type", "backtesting_thresholds", ["threshold_type"]
    )


def downgrade() -> None:
    op.drop_index("idx_backtesting_type", table_name="backtesting_thresholds")
    op.drop_index("idx_backtesting_case_id", table_name="backtesting_thresholds")
    op.drop_table("backtesting_thresholds")
