"""mda_thresholds — ADR-005 Decision 3

Revision ID: e9f3b2c5a1d7
Revises: 8b2c4e6f1a3d
Create Date: 2026-04-26

Two schema changes for the MDA threshold system:

1. New table: mda_thresholds
   Stores registered Minimum Descent Altitude (MDA) indicator floors. Each row
   defines one threshold: an indicator key, the entity scope it applies to, the
   floor value below which the simulation flags terrain, and the approach
   percentage at which WARNING fires. Thresholds are stored in the database
   (not in code constants) so they can be queried for trend analysis, updated
   as empirical evidence evolves, and reviewed in the audit trail without code
   changes. ADR-005 Decision 3.

2. New nullable column: scenario_state_snapshots.events_snapshot (JSONB)
   Stores MDA breach events produced by MDAChecker after each timestep advance,
   as a list of breach event dicts. Kept separate from state_data to avoid
   mixing simulation state (entity attributes) with post-processing classification
   (threshold breach detection). NULL for all pre-M4 snapshots.

Seed data: minimum viable MDA set for M4 entry (5 thresholds). These are Tier 3
confidence (calibrated from research literature, not yet from backtesting runs).
Seeded here rather than in a separate data migration to keep the schema and its
initial state coupled in one reviewable transaction. See ADR-005 Decision 3 table
for historical basis and irreversibility notes.

Fields in mda_thresholds:
  mda_id                — unique threshold identifier, human-readable (MDA-HD-POVERTY-Q1)
  indicator_key         — attribute key in simulation entity attributes
  entity_scope          — 'all' | ISO 3166-1 alpha-3 | fnmatch glob pattern
  measurement_framework — MeasurementFramework enum value
  floor_value           — floor below which breach is detected (NUMERIC)
  floor_unit            — unit label for the floor_value
  approach_pct          — fraction of floor_value above which WARNING fires
  severity_at_breach    — base MDASeverity for single-step breach (always CRITICAL)
  description           — human-readable threshold description
  historical_basis      — documented historical calibration sources
  recovery_horizon_years — estimated years to recover once floor is crossed; NULL if unknown
  irreversibility_note  — capability loss that becomes irreversible below this floor
"""
from __future__ import annotations

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB

from alembic import op

revision = "e9f3b2c5a1d7"
down_revision = "8b2c4e6f1a3d"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "mda_thresholds",
        sa.Column("mda_id", sa.Text(), primary_key=True, nullable=False),
        sa.Column("indicator_key", sa.Text(), nullable=False),
        sa.Column("entity_scope", sa.Text(), nullable=False, server_default="all"),
        sa.Column("measurement_framework", sa.Text(), nullable=False),
        sa.Column("floor_value", sa.Numeric(), nullable=False),
        sa.Column("floor_unit", sa.Text(), nullable=False),
        sa.Column(
            "approach_pct",
            sa.Numeric(),
            nullable=False,
            server_default="0.10",
        ),
        sa.Column("severity_at_breach", sa.Text(), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("historical_basis", sa.Text(), nullable=False),
        sa.Column("recovery_horizon_years", sa.Integer(), nullable=True),
        sa.Column("irreversibility_note", sa.Text(), nullable=False),
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
    )
    op.create_index("idx_mda_indicator", "mda_thresholds", ["indicator_key"])
    op.create_index("idx_mda_framework", "mda_thresholds", ["measurement_framework"])

    # events_snapshot stores MDA breach events per step, separate from state_data.
    op.add_column(
        "scenario_state_snapshots",
        sa.Column("events_snapshot", JSONB(), nullable=True),
    )

    # Seed: minimum viable MDA set for M4 entry. Tier 3 confidence (literature-calibrated).
    op.execute(
        """
        INSERT INTO mda_thresholds (
            mda_id, indicator_key, entity_scope, measurement_framework,
            floor_value, floor_unit, approach_pct, severity_at_breach,
            description, historical_basis, recovery_horizon_years, irreversibility_note
        ) VALUES
        (
            'MDA-HD-POVERTY-Q1',
            'poverty_headcount_ratio',
            '*:CHT:1-*-*',
            'human_development',
            0.40,
            'ratio',
            0.15,
            'CRITICAL',
            'Bottom quintile poverty headcount ratio over 40% — structural poverty trap threshold.',
            'UNDP poverty trap literature; Stuckler and Basu on austerity and poverty headcount.',
            10,
            'Multi-generational capability loss; child cohort education permanently impaired.'
        ),
        (
            'MDA-HD-HEALTH-CHILD',
            'health_index',
            '*:CHT:*-0-14-*',
            'human_development',
            0.30,
            'index',
            0.10,
            'CRITICAL',
            'Child cohort (0-14) health index below 0.30 — severe health system degradation.',
            'WHO child mortality threshold; MDG and SDG floor definitions.',
            15,
            'Permanent stunting and cognitive development impairment in the affected birth cohort.'
        ),
        (
            'MDA-FIN-RESERVES',
            'reserve_coverage_months',
            'all',
            'financial',
            2.5,
            'months',
            0.20,
            'CRITICAL',
            'Reserve coverage below 2.5 months of imports — IMF Article IV minimum threshold.',
            'IMF Article IV conventional 3-month floor; Thailand 1997 reserve depletion dynamics.',
            3,
            'Reserve depletion triggers currency defence failure; critical import capacity loss.'
        ),
        (
            'MDA-FIN-DEBT-GDP',
            'debt_gdp_ratio',
            'all',
            'financial',
            1.20,
            'ratio',
            0.10,
            'CRITICAL',
            'Debt-to-GDP exceeds 120% — IMF debt distress threshold for emerging markets.',
            'IMF debt distress literature; Greece 2010-2015 debt sustainability analysis.',
            NULL,
            'Market access closed; primary balance adjustment incompatible with growth recovery.'
        ),
        (
            'MDA-HD-FOOD',
            'food_insecurity_rate',
            'all',
            'human_development',
            0.35,
            'ratio',
            0.15,
            'CRITICAL',
            'Food insecurity rate over 35% — consistent with FAO food crisis classification.',
            'FAO food crisis threshold; WFP IPC Phase 3 Plus classification standards.',
            5,
            'Acute malnutrition in vulnerable cohorts; permanent developmental consequences.'
        )
        """
    )


def downgrade() -> None:
    op.drop_column("scenario_state_snapshots", "events_snapshot")
    op.drop_index("idx_mda_framework", table_name="mda_thresholds")
    op.drop_index("idx_mda_indicator", table_name="mda_thresholds")
    op.drop_table("mda_thresholds")
