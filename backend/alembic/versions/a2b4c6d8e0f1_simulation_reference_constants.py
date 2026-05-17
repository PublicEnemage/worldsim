"""simulation_reference_constants — STD-REVIEW-004 Gap 4

Revision ID: a2b4c6d8e0f1
Revises: f8a3c7e2d1b5
Create Date: 2026-05-16

Adds the simulation_reference_constants table for storing fixed scientific
thresholds used as normalization denominators in framework composite score
computation (e.g., planetary boundary values from Rockström et al. 2009).

Reference constants differ from time-series source data in access pattern
(single-value lookup at normalization time) and authority (peer-reviewed
scientific consensus, not periodic data release). Mixing them in source_registry
creates query complexity without benefit — Data Architect recommendation adopted
in Gap 4 disposition (STD-REVIEW-004).

Historical simulation reproducibility: the effective_from / effective_through
date range on each row allows any historical run to resolve which constant value
was in effect at run time. Never delete rows; insert new rows when scientific
consensus is revised.

Schema:
  constant_id       — text PK, naming convention {FRAMEWORK}_{INDICATOR}_{QUALIFIER}
  constant_name     — human-readable name
  value             — NUMERIC, the constant value
  unit              — text, canonical unit from DATA_STANDARDS.md §Canonical Unit Registry
  source_citation   — full bibliographic citation
  doi_or_url        — DOI preferred
  effective_from    — date when this value became operative
  effective_through — date NULL = currently in effect
  registered_by     — who registered
  registered_at     — when registered (timestamptz)

Unique partial index on (constant_id) WHERE effective_through IS NULL enforces
that only one value per constant is active at any time.
"""
from __future__ import annotations

import sqlalchemy as sa

from alembic import op

revision = "a2b4c6d8e0f1"
down_revision = "f8a3c7e2d1b5"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "simulation_reference_constants",
        sa.Column("constant_id", sa.Text(), nullable=False, primary_key=True),
        sa.Column("constant_name", sa.Text(), nullable=False),
        sa.Column("value", sa.Numeric(), nullable=False),
        sa.Column("unit", sa.Text(), nullable=False),
        sa.Column("source_citation", sa.Text(), nullable=False),
        sa.Column("doi_or_url", sa.Text(), nullable=False),
        sa.Column("effective_from", sa.Date(), nullable=False),
        sa.Column("effective_through", sa.Date(), nullable=True),
        sa.Column("registered_by", sa.Text(), nullable=False, server_default="agent"),
        sa.Column(
            "registered_at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
    )
    # Enforce one active value per constant at any time.
    op.create_index(
        "uix_simulation_reference_constants_active",
        "simulation_reference_constants",
        ["constant_id"],
        unique=True,
        postgresql_where=sa.text("effective_through IS NULL"),
    )


def downgrade() -> None:
    op.drop_index(
        "uix_simulation_reference_constants_active",
        table_name="simulation_reference_constants",
    )
    op.drop_table("simulation_reference_constants")
