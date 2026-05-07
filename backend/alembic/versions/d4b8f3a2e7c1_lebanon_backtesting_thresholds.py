"""lebanon_backtesting_thresholds — Issue #207

Revision ID: d4b8f3a2e7c1
Revises: c7e2a9f4d1b8
Create Date: 2026-05-06

Data migration: seeds Lebanon 2019–2020 DIRECTION_ONLY fidelity thresholds
into the backtesting_thresholds table (created by migration b5d3f7a2c8e1).

Two thresholds for case_id='LEBANON_2019_2020':

  lebanon_2019_2020.gdp_growth_step1_negative
    DIRECTION_ONLY: simulated gdp_growth at step 1 (2019) must be negative.
    Historical outturn: -6.9% (IMF WEO April 2020).
    Mechanism: initial gdp_growth is seeded at -2.0% (early-2019 tracking
    estimate, pre-protest). The one-step lag means step 1 events (bank
    deposit freeze, fiscal spending cut) are not yet processed by
    MacroeconomicModule. Step 1 shows the negative initial seed value.

  lebanon_2019_2020.gdp_growth_step2_negative
    DIRECTION_ONLY: simulated gdp_growth at step 2 (2020) must be negative.
    Historical outturn: -21.4% (IMF WEO April 2021).
    Mechanism: at step 2, MacroeconomicModule processes the step 1 fiscal
    spending cut (-10% of GDP) under the depressed regime (multiplier 1.5),
    generating a large negative gdp_growth_change delta. The compound 2020
    crisis (sovereign default + Beirut port explosion) is represented within
    this step's modeled shock.

DIRECTION_ONLY is the appropriate threshold type at this calibration stage.
DISTRIBUTION_COMBINED thresholds (infrastructure from Issue #194) require
calibrated uncertainty bands; deferred to a future milestone per ADR-006.

Lebanon exhibits CASCADE propagation dynamics not yet fully modeled. Full
cascade validation is deferred to Issue #29 (CASCADE propagation mode).

Sources:
  gdp_growth_step1: IMF WEO April 2020, Lebanon 2019 outturn: -6.92%
  gdp_growth_step2: IMF WEO April 2021, Lebanon 2020 outturn: -21.40%
"""
from __future__ import annotations

from alembic import op

revision = "d4b8f3a2e7c1"
down_revision = "c7e2a9f4d1b8"
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
            'lbn-2019-gdp-step1',
            'LEBANON_2019_2020',
            'gdp_growth_step1_negative',
            'DIRECTION_ONLY',
            'gdp_growth',
            'LBN',
            1,
            'negative',
            NULL,
            NULL,
            NULL,
            'Lebanon 2019 GDP contraction — DIRECTION_ONLY. Bank deposit freeze, fiscal collapse.',
            'IMF WEO April 2020 (2019 outturn -6.92%)'
        ),
        (
            'lbn-2020-gdp-step2',
            'LEBANON_2019_2020',
            'gdp_growth_step2_negative',
            'DIRECTION_ONLY',
            'gdp_growth',
            'LBN',
            2,
            'negative',
            NULL,
            NULL,
            NULL,
            'Lebanon 2020 GDP contraction — DIRECTION_ONLY. Sovereign default + Beirut explosion.',
            'IMF WEO April 2021 (2020 outturn -21.40%)'
        )
        """
    )


def downgrade() -> None:
    op.execute(
        "DELETE FROM backtesting_thresholds WHERE case_id = 'LEBANON_2019_2020'"
    )
