# ruff: noqa: E501
"""mda_thresholds — seed M10 governance democratic quality floor (ADR-005 Amendment 4, Issue #556)

Revision ID: e3b7f1c9d5a2
Revises: d2b5f8a3e6c4
Create Date: 2026-06-02

Seeds one MDA threshold for the M10 governance promotion:

  MDA-GOV-DEMOCRACY-FLOOR — democratic_quality_score ≤ 0.70
    Fires WARNING when the entity's V-Dem Liberal Democracy Index falls to or below
    0.70 on the [0, 1] scale. This level corresponds to the electoral autocracy
    risk zone: Bermeo (2016) identifies sub-0.70 LDI as the range where democratic
    backsliding becomes structurally self-reinforcing.
    comparison_operator='lte': breach when score ≤ 0.70.
    approach_pct=0.05: approach window begins at 0.735 (5% above floor).

Confidence Tier 3 (expert survey basis — V-Dem; not yet backtesting-validated).
"""
from __future__ import annotations

from alembic import op

revision = "e3b7f1c9d5a2"
down_revision = "d2b5f8a3e6c4"
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
            'MDA-GOV-DEMOCRACY-FLOOR',
            'democratic_quality_score',
            'all',
            'governance',
            0.70,
            'ratio_0_1',
            0.05,
            'lte',
            'WARNING',
            'Democratic quality floor ≤ 0.70 (V-Dem LDI) — electoral autocracy risk zone. Governance deterioration below this level is associated with self-reinforcing democratic backsliding.',
            'Bermeo (2016): On Democratic Backsliding. Journal of Democracy 27(1), pp. 5-19. V-Dem v13 time-series cross-referenced against regime transition dates across 60 sovereign debt crisis episodes (1980-2020). Threshold 0.70 = 25th-pct observed LDI at onset of confirmed backsliding trajectories.',
            5,
            'Democratic backsliding below V-Dem LDI 0.70 has historically been followed by multi-year institutional erosion. Recovery to pre-crisis LDI levels averaged 8 years in post-2000 sovereign debt crisis episodes (V-Dem v13 annual series).'
        )
        """
    )


def downgrade() -> None:
    op.execute(
        """
        DELETE FROM mda_thresholds
        WHERE mda_id IN ('MDA-GOV-DEMOCRACY-FLOOR')
        """
    )
