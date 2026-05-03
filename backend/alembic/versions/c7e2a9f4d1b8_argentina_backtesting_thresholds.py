"""argentina_backtesting_thresholds — Issue #192

Revision ID: c7e2a9f4d1b8
Revises: b5d3f7a2c8e1
Create Date: 2026-05-03

Data migration: seeds Argentina 2001–2002 DIRECTION_ONLY fidelity thresholds
into the backtesting_thresholds table (created by migration b5d3f7a2c8e1).

Two thresholds for case_id='ARGENTINA_2001_2002':

  argentina_2001_2002.gdp_growth_step1_negative
    DIRECTION_ONLY: simulated gdp_growth at step 1 (2001) must be negative.
    Historical outturn: -4.4% (IMF WEO April 2002).
    Mechanism: step 1 seeds the initial gdp_growth of -0.8% (2000 recession
    baseline) which is already negative. The one-step lag means the Zero
    Deficit Plan fiscal shock has not yet resolved at step 1.

  argentina_2001_2002.gdp_growth_step2_negative
    DIRECTION_ONLY: simulated gdp_growth at step 2 (2002) must be negative.
    Historical outturn: -10.9% (IMF WEO April 2003).
    Mechanism: at step 2, MacroeconomicModule processes the step 1 fiscal
    spending cut (Zero Deficit Plan, -6.5% of GDP) with depressed-regime
    multiplier (1.5), generating a large negative gdp_growth_change delta.

DIRECTION_ONLY is the appropriate threshold type at this calibration stage.
DISTRIBUTION_COMBINED thresholds (infrastructure from Issue #194) require
calibrated uncertainty bands; deferred to a future milestone per ADR-006.

Sources:
  gdp_growth_step1: IMF WEO April 2002, Argentina 2001 outturn: -4.41%
  gdp_growth_step2: IMF WEO April 2003, Argentina 2002 outturn: -10.89%
"""
from __future__ import annotations

from alembic import op

revision = "c7e2a9f4d1b8"
down_revision = "b5d3f7a2c8e1"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        """
        INSERT INTO backtesting_thresholds (
            threshold_id,
            case_id,
            threshold_name,
            threshold_type,
            attribute_key,
            entity_id,
            step,
            expected_direction,
            expected_value,
            tolerance_pct,
            ci_coverage,
            description,
            source
        ) VALUES
        (
            'arg-2001-gdp-step1',
            'ARGENTINA_2001_2002',
            'gdp_growth_step1_negative',
            'DIRECTION_ONLY',
            'gdp_growth',
            'ARG',
            1,
            'negative',
            NULL,
            NULL,
            NULL,
            'Argentina 2001 GDP contraction — DIRECTION_ONLY check.',
            'IMF WEO April 2002 (2001 outturn -4.41%)'
        ),
        (
            'arg-2001-gdp-step2',
            'ARGENTINA_2001_2002',
            'gdp_growth_step2_negative',
            'DIRECTION_ONLY',
            'gdp_growth',
            'ARG',
            2,
            'negative',
            NULL,
            NULL,
            NULL,
            'Argentina 2002 GDP contraction (deeper) — DIRECTION_ONLY check.',
            'IMF WEO April 2003 (2002 outturn -10.89%)'
        )
        """
    )


def downgrade() -> None:
    op.execute(
        "DELETE FROM backtesting_thresholds WHERE case_id = 'ARGENTINA_2001_2002'"
    )
