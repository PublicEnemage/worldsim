"""simulation_reference_constants — add confidence_tier column (ADR-005 Amendment 3 Decision M8-6)

Revision ID: c1a4e7f2d9b3
Revises: 5eec5d75c103
Create Date: 2026-05-17

Adds a confidence_tier INTEGER NOT NULL DEFAULT 2 column to
simulation_reference_constants (Decision M8-6 Implementation obligation 4).

The column carries the epistemic confidence tier of the boundary constant
itself — distinct from the confidence tier of the indicator that uses it.
Derived indicator tiers propagate via max(source_indicator_tier,
boundary_constant_tier) per the lower-of-two rule (ADR-001 Amendment 1 §Quantity type).

Tier assignments for existing rows:
  ECOLOGICAL_CO2_PLANETARY_BOUNDARY_PPM        → 2
    Rockström 2009 peer-reviewed consensus; scientifically contested —
    boundary represents a scientific judgment, not a physical constant.
  ECOLOGICAL_LAND_USE_PLANETARY_BOUNDARY_RATIO → 2
    Richardson 2023 revision; higher uncertainty than CO2 boundary given
    data availability constraints for global land-system assessment.

These tiers are queried by _fetch_active_boundary_constants() in scenarios.py.
"""
from __future__ import annotations

import sqlalchemy as sa

from alembic import op

revision = "c1a4e7f2d9b3"
down_revision = "5eec5d75c103"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "simulation_reference_constants",
        sa.Column(
            "confidence_tier",
            sa.Integer(),
            nullable=False,
            server_default="2",
        ),
    )
    op.execute(
        """
        UPDATE simulation_reference_constants
        SET confidence_tier = 2
        WHERE constant_id IN (
            'ECOLOGICAL_CO2_PLANETARY_BOUNDARY_PPM',
            'ECOLOGICAL_LAND_USE_PLANETARY_BOUNDARY_RATIO'
        )
        """
    )


def downgrade() -> None:
    op.drop_column("simulation_reference_constants", "confidence_tier")
