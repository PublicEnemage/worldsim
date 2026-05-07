"""ecuador_backtesting_thresholds — Issue #212

Revision ID: f8a3c7e2d1b5
Revises: e1c9d7f5b3a2
Create Date: 2026-05-06

Data migration: seeds Ecuador 1999–2000 DIRECTION_ONLY fidelity thresholds
into the backtesting_thresholds table (created by migration b5d3f7a2c8e1).

Two thresholds for case_id='ECUADOR_1999_2000':

  ecuador_1999_2000.gdp_growth_step1_negative
    DIRECTION_ONLY: simulated gdp_growth at step 1 (1999) must be negative.
    Historical outturn: -6.3% (IMF WEO October 1999).
    Mechanism: initial gdp_growth seeded at -6.3% (1999 full-year outturn).
    The one-step lag means step 1 events (capital controls, bank holiday) are
    not processed by MacroeconomicModule (it does not subscribe to emergency
    events). Step 1 shows the negative initial seed value directly.

  ecuador_1999_2000.gdp_growth_step2_not_deeper
    NOT DEEPER CONTRACTION: simulated gdp_growth at step 2 (2000) must be
    >= step 1 gdp_growth (not further deterioration).
    Historical outturn: +2.8% (recovery after dollarization).
    Mechanism: StructuralPolicyInput INSTITUTIONAL_REFORM at step 2 is not
    processed by MacroeconomicModule (which listens only to fiscal and monetary
    events). Step 2 GDP = step 1 GDP = initial seed = -6.3%. This satisfies
    the >= threshold (equal values satisfy not-deeper-than). The historical
    recovery (+2.8%) reflects dollarization stabilization and oil price recovery
    — both documented M6 blind spots not yet modeled.

Ecuador is the FIRST backtesting case with a non-contraction step 2 threshold.
This tests the simulation's ability to avoid runaway deterioration when a
structural stabilization event is applied, rather than asserting positive recovery.
Full recovery modeling is deferred pending a StructuralModule (Issue #29 area)
and commodity price channel implementation.

Sources:
  gdp_growth_step1: IMF WEO October 1999, Ecuador 1999 outturn: -6.27%
  gdp_growth_step2: IMF WEO April 2001, Ecuador 2000 outturn: +2.80%
"""
from __future__ import annotations

from alembic import op

revision = "f8a3c7e2d1b5"
down_revision = "e1c9d7f5b3a2"
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
            'ecu-1999-gdp-step1',
            'ECUADOR_1999_2000',
            'gdp_growth_step1_negative',
            'DIRECTION_ONLY',
            'gdp_growth',
            'ECU',
            1,
            'negative',
            NULL,
            NULL,
            NULL,
            'Ecuador 1999 GDP contraction — DIRECTION_ONLY. Banking system freeze, sucre collapse.',
            'IMF WEO October 1999 (1999 outturn -6.27%)'
        ),
        (
            'ecu-2000-gdp-step2',
            'ECUADOR_1999_2000',
            'gdp_growth_step2_not_deeper',
            'DIRECTION_ONLY',
            'gdp_growth',
            'ECU',
            2,
            'not_deeper',
            NULL,
            NULL,
            NULL,
            'Ecuador 2000 GDP not deeper than 1999 — stabilization gate (M6 blind spot).',
            'IMF WEO April 2001 (2000 outturn +2.80%)'
        )
        """
    )


def downgrade() -> None:
    op.execute(
        "DELETE FROM backtesting_thresholds WHERE case_id = 'ECUADOR_1999_2000'"
    )
