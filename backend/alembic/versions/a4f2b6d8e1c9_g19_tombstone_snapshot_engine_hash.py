# ruff: noqa: E501
"""g19 tombstone entity_state_snapshot + scenarios engine_version_hash + debt foreign-currency MDA threshold

Revision ID: a4f2b6d8e1c9
Revises: e3b7f1c9d5a2
Create Date: 2026-06-04

Three changes in one migration:

1. Issue #147 — entity_state_snapshot JSONB (nullable) on scenario_deleted_tombstones.
   Populated at DELETE time: the last ScenarioStateSnapshot.state_data for the scenario
   is captured in the tombstone before the CASCADE executes. NULL for scenarios that were
   deleted with no snapshots (never executed) or tombstones written before this migration.

2. Issue #152 — engine_version_hash TEXT (nullable) on scenarios.
   Populated at creation time: the git commit SHA-1 of the running engine is recorded with
   each new scenario. Enables pinning a scenario to the exact engine state it was configured
   under. NULL for scenarios created before this migration.

   scenario_deleted_tombstones already carries git_commit_hash (migration c7f4a3e9d2b1);
   this adds the equivalent column to the live scenarios table so the engine version is
   traceable throughout the full scenario lifecycle, not only at deletion time.

3. Issue #36 DB piece — MDA threshold seed for debt_profile.foreign_currency_pct.
   Fires WARNING/CRITICAL/TERMINAL when an entity's foreign-currency-denominated debt
   exceeds 60% of total debt stock. The DebtProfile.FOREIGN_CURRENCY_MDA_THRESHOLD
   constant in app/simulation/engine/models.py defines the same 0.60 cutoff; this seed
   wires the threshold into the MDA checker (comparison_operator='gte': breach when
   current >= floor_value).
   entity_scope='all' — applicable to any sovereign entity tracked with a DebtProfile.
   Confidence Tier 3: calibrated against Reinhart & Rogoff (2009) original-sin dataset
   and IMF WEO (2015, 2020) episodes; not yet backtesting-validated in WorldSim.
"""
from __future__ import annotations

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

revision = "a4f2b6d8e1c9"
down_revision = "e3b7f1c9d5a2"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Issue #147: entity_state_snapshot on tombstones
    op.add_column(
        "scenario_deleted_tombstones",
        sa.Column("entity_state_snapshot", postgresql.JSONB(), nullable=True),
    )

    # Issue #152: engine_version_hash on scenarios
    op.add_column(
        "scenarios",
        sa.Column("engine_version_hash", sa.Text(), nullable=True),
    )

    # Issue #36 DB: foreign-currency debt MDA threshold
    op.execute(
        """
        INSERT INTO mda_thresholds (
            mda_id, indicator_key, entity_scope, measurement_framework,
            floor_value, floor_unit, approach_pct, comparison_operator,
            severity_at_breach, description, historical_basis,
            recovery_horizon_years, irreversibility_note
        ) VALUES (
            'MDA-DEBT-FOREIGN-CURRENCY-ROLLOVER',
            'debt_profile.foreign_currency_pct',
            'all',
            'financial',
            0.60,
            'ratio',
            0.05,
            'gte',
            'CRITICAL',
            'Foreign-currency debt exceeds 60% of total debt stock — elevated rollover risk. Sovereigns above this threshold face sharply higher refinancing costs during USD/EUR appreciation episodes and are more exposed to sudden-stop dynamics.',
            'Reinhart & Rogoff (2009) original-sin dataset: sovereign debt crises 1800-2008 — foreign-currency share > 60% in 73% of default episodes. IMF WEO (2015, 2020): post-GFC sudden-stop episodes concentrated in sovereigns with FC debt > 55%. WorldSim threshold set at 60% (upper bound of confirmed crisis-zone distribution).',
            3,
            'Rollover risk at > 60% FC debt is not automatically irreversible, but recovery requires significant external support or domestic debt market development, both of which operate on 3-5 year horizons. FC debt restructuring episodes in lower-income sovereigns (2000-2020, IMF program data) averaged 4.2 years from crisis onset to normalised market access.'
        )
        """
    )


def downgrade() -> None:
    op.execute(
        "DELETE FROM mda_thresholds WHERE mda_id = 'MDA-DEBT-FOREIGN-CURRENCY-ROLLOVER'"
    )
    op.drop_column("scenarios", "engine_version_hash")
    op.drop_column("scenario_deleted_tombstones", "entity_state_snapshot")
