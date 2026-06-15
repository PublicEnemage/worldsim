# ruff: noqa: E501
"""mda_thresholds — seed PE-001 programme survival critical floor (ADR-013 Decision 1)

Revision ID: f2a5c8e3d1b7
Revises: a4f2b6d8e1c9
Create Date: 2026-06-12

Seeds one MDA threshold for the political economy module (ADR-013 Decision 1):

  PE-001-programme-survival-critical — programme_survival_probability ≤ 0.25
    Fires CRITICAL when the entity's formula-calibrated programme survival
    probability falls to or below 0.25 on the [0.01, 0.99] scale.

    The 0.25 floor corresponds to conditions observed in historically failed
    IMF programmes: Greece 2015 (Syriza referendum context), Argentina 2001
    (default declaration), Ecuador 2000 (programme abandonment). At survival
    probability below 0.25, historical precedent shows programme collapse
    becomes the dominant outcome.

    comparison_operator='lte': breach when probability ≤ 0.25.
    approach_pct=0.10: approach window begins at 0.275 (10% above floor).

    Disclosure (Layer 3 requirement): "Programme survival probability is a
    formula-calibrated estimate (Tier 3) based on historical programme failure
    patterns. It is not a prediction. A value below 0.25 indicates conditions
    similar to historically failed programmes."

Confidence Tier 3 (formula-calibrated on three historical cases; not yet
backtesting-validated against a larger dataset).

The PROGRAMME_SURVIVAL_FLOOR constant (0.25) must not change without an
ADR-013 amendment per ADR-013 §Decision 1.
"""
from __future__ import annotations

from alembic import op

revision = "f2a5c8e3d1b7"
down_revision = "a4f2b6d8e1c9"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        """
        INSERT INTO mda_thresholds (
            mda_id, indicator_key, entity_scope, measurement_framework,
            floor_value, floor_unit, approach_pct, comparison_operator,
            severity_at_breach, description, historical_basis,
            recovery_horizon_years, irreversibility_note
        ) VALUES
        (
            'PE-001-programme-survival-critical',
            'programme_survival_probability',
            'all',
            'political_economy',
            0.25,
            'ratio_0_1',
            0.10,
            'lte',
            'CRITICAL',
            'Programme survival probability critical floor ≤ 0.25 — conditions historically associated with programme collapse. Formula-calibrated estimate (Tier 3). Disclosure: "Programme survival probability is a formula-calibrated estimate (Tier 3) based on historical programme failure patterns. It is not a prediction. A value below 0.25 indicates conditions similar to historically failed programmes."',
            'Greece 2015: programme survival probability estimated below 0.25 at time of Syriza referendum (July 2015), preceding capital controls and eventual third bailout negotiation. Argentina 2001: fiscal adjustment programme collapsed with default declaration in December 2001 following legitimacy collapse. Ecuador 2000: IMF programme abandoned within 1 year of signing. All three cases: programme_survival_probability < 0.25 estimated retrospectively using the ADR-013 formula at programme collapse. ADR-013 Decision 1. Calibration basis: docs/methodology/calibration-basis.md §PROGRAMME_SURVIVAL_FLOOR.',
            3,
            'Programme collapse at survival probability < 0.25 has historically been followed by multi-year creditor relationship deterioration, loss of market access, and restructuring negotiations averaging 3-5 years resolution time (Greece: 2010-2018, Argentina: 2001-2005, Ecuador: 2000-2008). Recovery of programme viability to pre-crisis conditions requires both economic stabilisation and legitimacy restoration.'
        )
        """
    )


def downgrade() -> None:
    op.execute(
        """
        DELETE FROM mda_thresholds
        WHERE mda_id = 'PE-001-programme-survival-critical'
        """
    )
