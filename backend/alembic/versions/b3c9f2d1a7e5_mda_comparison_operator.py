"""mda_thresholds.comparison_operator — ADR-005 Decision 3 amendment (Issue #236)

Revision ID: b3c9f2d1a7e5
Revises: a3d9e7c2f4b1
Create Date: 2026-05-10

Adds a comparison_operator column to mda_thresholds to distinguish lower-bound
thresholds (safe when current > floor, breach when current ≤ floor) from
upper-bound thresholds (safe when current < floor, breach when current ≥ floor).

Without this column, MDAChecker treated every threshold as a lower bound. For
MDA-FIN-DEBT-GDP (debt-to-GDP) and similar upper-bound thresholds, this caused
the alert to never fire — a debt/GDP of 148% would compute a positive
approach_pct_remaining and exit without alerting. Three of five registered
thresholds were silently broken.

Values:
  "lte"  — breach when current ≤ floor_value (lower bound; default)
            Examples: reserve coverage, health index
  "gte"  — breach when current ≥ floor_value (upper bound; ceiling)
            Examples: debt/GDP ratio, poverty headcount rate, food insecurity rate

The three upper-bound thresholds are updated to 'gte' in this migration.
"""
from __future__ import annotations

import sqlalchemy as sa

from alembic import op

revision = "b3c9f2d1a7e5"
down_revision = "a3d9e7c2f4b1"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "mda_thresholds",
        sa.Column(
            "comparison_operator",
            sa.Text(),
            nullable=False,
            server_default="lte",
        ),
    )
    # Update the three upper-bound thresholds to 'gte'.
    # Lower-bound thresholds (MDA-FIN-RESERVES, MDA-HD-HEALTH-CHILD) keep the 'lte' default.
    op.execute(
        """
        UPDATE mda_thresholds
        SET comparison_operator = 'gte'
        WHERE mda_id IN ('MDA-FIN-DEBT-GDP', 'MDA-HD-POVERTY-Q1', 'MDA-HD-FOOD')
        """
    )


def downgrade() -> None:
    op.drop_column("mda_thresholds", "comparison_operator")
