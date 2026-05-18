# ruff: noqa: E501
"""mda_thresholds — seed M8 ecological planetary boundary thresholds (ADR-005 Amendment 3 M8-1)

Revision ID: d2b5f8a3e6c4
Revises: c1a4e7f2d9b3
Create Date: 2026-05-17

Seeds two MDA thresholds for the M8 ecological indicator expansion:

  MDA-ECO-CO2-BOUNDARY  — planetary_boundary_co2_proximity ≥ 1.0
    Fires WARNING when the entity's CO2 concentration crosses the
    Rockström 2009 boundary (350 ppm). Proximity score 1.0 = at boundary.
    comparison_operator='gte': breach when proximity ≥ 1.0.

  MDA-ECO-LAND-BOUNDARY — planetary_boundary_land_use_proximity ≥ 1.0
    Fires WARNING when land-use pressure index crosses the Richardson 2023
    revision boundary. Proximity score 1.0 = at boundary.
    comparison_operator='gte': breach when proximity ≥ 1.0.

Confidence Tier 2 for both thresholds (literature-calibrated; not yet
validated by backtesting runs). Tier assignment consistent with confidence_tier
column added by c1a4e7f2d9b3 for ECOLOGICAL_CO2_PLANETARY_BOUNDARY_PPM (Tier 2)
and ECOLOGICAL_LAND_USE_PLANETARY_BOUNDARY_RATIO (Tier 2 by default).

These thresholds activate the MDA breach detection path in alerts_from_events_snapshot
for ecological indicators once EcologicalModule produces proximity attributes.
"""
from __future__ import annotations

from alembic import op

revision = "d2b5f8a3e6c4"
down_revision = "c1a4e7f2d9b3"
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
            'MDA-ECO-CO2-BOUNDARY',
            'planetary_boundary_co2_proximity',
            'all',
            'ecological',
            1.0,
            'ratio_0_1',
            0.10,
            'gte',
            'WARNING',
            'CO2 planetary boundary proximity ≥ 1.0 — Rockström 2009 boundary (350 ppm) met or exceeded.',
            'Rockström et al. 2009 (Nature) — nine planetary boundaries; 350 ppm CO2 boundary.',
            NULL,
            'Atmospheric CO2 accumulation is irreversible on century timescales; exceedance commits future generations to warming trajectories.'
        ),
        (
            'MDA-ECO-LAND-BOUNDARY',
            'planetary_boundary_land_use_proximity',
            'all',
            'ecological',
            1.0,
            'ratio_0_1',
            0.10,
            'gte',
            'WARNING',
            'Land-use planetary boundary proximity ≥ 1.0 — Richardson 2023 land-system boundary met or exceeded.',
            'Richardson et al. 2023 (Science Advances) — updated planetary boundaries; land-system revision.',
            NULL,
            'Biodiversity loss from land-system change can be irreversible at species and habitat level.'
        )
        """
    )


def downgrade() -> None:
    op.execute(
        """
        DELETE FROM mda_thresholds
        WHERE mda_id IN ('MDA-ECO-CO2-BOUNDARY', 'MDA-ECO-LAND-BOUNDARY')
        """
    )
