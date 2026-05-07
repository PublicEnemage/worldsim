"""argentina_magnitude_threshold — partial #208/#210

Revision ID: a3d9e7c2f4b1
Revises: f8a3c7e2d1b5
Create Date: 2026-05-06

Data migration: adds one MAGNITUDE threshold row for Argentina 2001–2002 step 2
to the backtesting_thresholds table (created by migration b5d3f7a2c8e1).

Argentina step 2 (2002) achieves MAGNITUDE calibration at 3.2% deviation:
  Model:  −10.55%
    Mechanism: depressed-regime multiplier 1.5 × Zero Deficit Plan (−6.5% of GDP)
    applied to initial gdp_growth of −0.8% via MacroeconomicModule one-step lag.
  Actual: −10.90% (IMF WEO April 2003)
  Deviation: |−0.1055 − (−0.109)| / |−0.109| = 3.2% — within 20% tolerance

Tolerance: expected_value = −0.109, tolerance_pct = 0.20
Tolerance band (informational): ±20% of |−0.109| = ±0.0218 → [−0.1308, −0.0872]

Structural gaps deferred to M7 (see feasibility assessment preceding this commit):

  ARG step 1 (2001) — structural gap, Issue #222:
    Model: −0.8% (initial seed). Actual: −4.4%. Deviation: 82%.
    Cause: one-step lag — Zero Deficit Plan fires at step 1 but is processed
    at step 2. Model reports pre-shock baseline. Not fixable by parameter
    calibration. M7 decision required: contemporaneous processing path (Option A),
    revised seeding (Option B), or formal DIRECTION_ONLY permanence (Option C).

  GRC steps 2 and 3 — structural gap, Issue #221:
    GRC step 2: model −21.4% vs actual −8.9% (140% deviation).
    GRC step 3: model −31.4% vs actual −6.6% (376% deviation).
    Cause: gdp_growth is a pure accumulation stock — it only moves when a fiscal
    event fires and never receives endogenous recovery impulse. The Greek economy
    improved from −8.9% to −6.6% without a positive fiscal shock. Requires a
    mean-reversion channel in MacroeconomicModule (Chief Methodologist + Chief
    Engineer joint ADR-006 amendment before implementation).

Sources:
  gdp_growth_step2: IMF WEO April 2003, Argentina 2002 outturn −10.89%
  Multiplier calibration: MacroeconomicModule depressed-regime multiplier 1.5
    (ADR-006 Decision 8; Blanchard-Leigh 2013 empirical foundation)
"""
from __future__ import annotations

from alembic import op

revision = "a3d9e7c2f4b1"
down_revision = "f8a3c7e2d1b5"
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
            'arg-2002-gdp-step2-mag',
            'ARGENTINA_2001_2002',
            'gdp_growth_step2_magnitude',
            'MAGNITUDE',
            'gdp_growth',
            'ARG',
            2,
            'negative',
            -0.109,
            0.20,
            NULL,
            'Argentina 2002 GDP contraction — MAGNITUDE within 20% of actual −10.9%. '
            'Model produces −10.55% via depressed-regime multiplier 1.5 on Zero '
            'Deficit Plan (−6.5% of GDP). Deviation: 3.2%. '
            'ARG step 1 and GRC steps 2–3 deferred to M7 Issues #222 and #221.',
            'IMF WEO April 2003 (2002 outturn −10.89%)'
        )
        """
    )


def downgrade() -> None:
    op.execute(
        "DELETE FROM backtesting_thresholds WHERE threshold_id = 'arg-2002-gdp-step2-mag'"
    )
