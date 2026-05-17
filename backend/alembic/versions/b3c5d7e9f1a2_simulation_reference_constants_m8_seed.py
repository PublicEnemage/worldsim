"""simulation_reference_constants M8 seed — STD-REVIEW-004 Gap 4

Revision ID: b3c5d7e9f1a2
Revises: a2b4c6d8e0f1
Create Date: 2026-05-16

Seeds two planetary boundary reference constants required for M8 ecological
composite score boundary normalization (ADR-005 Amendment B M8 obligation):

1. ECOLOGICAL_CO2_PLANETARY_BOUNDARY_PPM = 350 ppm
   Source: Rockström et al. 2009 — "A safe operating space for humanity"
   Nature 461: 472–475. doi:10.1038/461472a
   effective_from: 2009-09-24 (Nature publication date)

2. ECOLOGICAL_LAND_USE_PLANETARY_BOUNDARY_RATIO = 0.25 (ratio_0_1)
   Source: Richardson et al. 2023 — "Earth beyond six of nine planetary boundaries"
   Science Advances 9(37). doi:10.1126/sciadv.adh2458
   effective_from: 2023-09-13 (Science Advances publication date)

Normalization formula (DATA_STANDARDS.md §Simulation Reference Constants):
  boundary_score = min(current_value / boundary_value, 2.0)
  > 1.0 = boundary crossed; = 1.0 = boundary met; < 1.0 = safe operating space
  Cap at 2.0 = "double the safe boundary" as display ceiling.
"""
from __future__ import annotations

import sqlalchemy as sa

from alembic import op

revision = "b3c5d7e9f1a2"
down_revision = "a2b4c6d8e0f1"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.bulk_insert(
        sa.table(
            "simulation_reference_constants",
            sa.column("constant_id", sa.Text),
            sa.column("constant_name", sa.Text),
            sa.column("value", sa.Numeric),
            sa.column("unit", sa.Text),
            sa.column("source_citation", sa.Text),
            sa.column("doi_or_url", sa.Text),
            sa.column("effective_from", sa.Date),
            sa.column("effective_through", sa.Date),
            sa.column("registered_by", sa.Text),
        ),
        [
            {
                "constant_id": "ECOLOGICAL_CO2_PLANETARY_BOUNDARY_PPM",
                "constant_name": "Atmospheric CO2 planetary boundary (safe operating space)",
                "value": 350,
                "unit": "ppm",
                "source_citation": (
                    "Rockström, J. et al. (2009). A safe operating space for humanity. "
                    "Nature, 461(7263), 472–475."
                ),
                "doi_or_url": "doi:10.1038/461472a",
                "effective_from": "2009-09-24",
                "effective_through": None,
                "registered_by": "std-review-004-gap4",
            },
            {
                "constant_id": "ECOLOGICAL_LAND_USE_PLANETARY_BOUNDARY_RATIO",
                "constant_name": "Land-system change planetary boundary (safe threshold fraction)",
                "value": "0.25",
                "unit": "ratio_0_1",
                "source_citation": (
                    "Richardson, K. et al. (2023). Earth beyond six of nine planetary boundaries. "
                    "Science Advances, 9(37), eadh2458."
                ),
                "doi_or_url": "doi:10.1126/sciadv.adh2458",
                "effective_from": "2023-09-13",
                "effective_through": None,
                "registered_by": "std-review-004-gap4",
            },
        ],
    )


def downgrade() -> None:
    op.execute(
        "DELETE FROM simulation_reference_constants "
        "WHERE constant_id IN ("
        "  'ECOLOGICAL_CO2_PLANETARY_BOUNDARY_PPM',"
        "  'ECOLOGICAL_LAND_USE_PLANETARY_BOUNDARY_RATIO'"
        ")"
    )
