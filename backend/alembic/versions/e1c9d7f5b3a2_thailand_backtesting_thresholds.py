"""thailand_backtesting_thresholds — Issue #141

Revision ID: e1c9d7f5b3a2
Revises: d4b8f3a2e7c1
Create Date: 2026-05-06

Data migration: seeds Thailand 1997–2000 DIRECTION_ONLY fidelity thresholds
into the backtesting_thresholds table (created by migration b5d3f7a2c8e1).

Two thresholds for case_id='THAILAND_1997_2000':

  thailand_1997_2000.gdp_growth_step1_negative
    DIRECTION_ONLY: simulated gdp_growth at step 1 (1997) must be negative.
    Historical outturn: -1.4% (IMF WEO October 1998).
    Mechanism: initial gdp_growth is seeded at -1.0% (early-1997 tracking
    estimate, pre-peg-abandonment). The one-step lag means step 1 events
    (capital controls + fiscal tightening) are not yet processed by
    MacroeconomicModule. Step 1 shows the negative initial seed value.

  thailand_1997_2000.gdp_growth_step2_negative
    DIRECTION_ONLY: simulated gdp_growth at step 2 (1998) must be negative.
    Historical outturn: -10.5% (IMF WEO April 1999).
    Mechanism: at step 2, MacroeconomicModule processes the step 1 fiscal
    spending cut (-6% of GDP) under the depressed regime (multiplier 1.5),
    generating a large negative gdp_growth_change delta. The IMF program
    conditionality (pro-cyclical austerity) compounds the contraction.

DIRECTION_ONLY is the appropriate threshold type at this calibration stage.
DISTRIBUTION_COMBINED thresholds (infrastructure from Issue #194) require
calibrated uncertainty bands; deferred to a future milestone per ADR-006.

Thailand exhibits herding and contagion CASCADE dynamics not yet fully modeled.
Full cascade validation (speculative attack contagion + balance-sheet cascade)
is deferred to Issue #29 (CASCADE propagation mode).

Sources:
  gdp_growth_step1: IMF WEO October 1998, Thailand 1997 outturn: -1.37%
  gdp_growth_step2: IMF WEO April 1999, Thailand 1998 outturn: -10.51%
"""
from __future__ import annotations

from alembic import op

revision = "e1c9d7f5b3a2"
down_revision = "d4b8f3a2e7c1"
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
            'tha-1997-gdp-step1',
            'THAILAND_1997_2000',
            'gdp_growth_step1_negative',
            'DIRECTION_ONLY',
            'gdp_growth',
            'THA',
            1,
            'negative',
            NULL,
            NULL,
            NULL,
            'Thailand 1997 GDP contraction — DIRECTION_ONLY check. Currency peg abandonment and fiscal tightening onset.',
            'IMF WEO October 1998 (1997 outturn -1.37%)'
        ),
        (
            'tha-1998-gdp-step2',
            'THAILAND_1997_2000',
            'gdp_growth_step2_negative',
            'DIRECTION_ONLY',
            'gdp_growth',
            'THA',
            2,
            'negative',
            NULL,
            NULL,
            NULL,
            'Thailand 1998 GDP contraction (deep) — DIRECTION_ONLY check. IMF program pro-cyclical austerity + balance-sheet recession.',
            'IMF WEO April 1999 (1998 outturn -10.51%)'
        )
        """
    )


def downgrade() -> None:
    op.execute(
        "DELETE FROM backtesting_thresholds WHERE case_id = 'THAILAND_1997_2000'"
    )
