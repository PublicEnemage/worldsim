# ruff: noqa: E501
"""M17-G1: seed ACADEMIC_LITERATURE_FOSU_2011_SSA_POVERTY_GROWTH in source_registry

Revision ID: a3b5d7f9e2c1
Revises: a2c4e6f8b0d1
Create Date: 2026-06-25

Registers the Fosu (2011) SSA poverty-growth elasticity source introduced by the
M17-G1 ELASTICITY_REGISTRY recalibration (#1229). The new source_registry_id
ACADEMIC_LITERATURE_FOSU_2011_SSA_POVERTY_GROWTH replaces
ACADEMIC_LITERATURE_LUSTIG_2017_FISCAL_POVERTY as the citation basis for the
Q1 informal gdp_growth_change → poverty_headcount_ratio elasticity entry in
DemographicModule.

Fosu, A.K. (2011). "The Effect of Income Distribution on the Poverty-Growth
Relationship: Empirical Evidence from Sub-Saharan Africa."
Journal of African Economies, 20(5), 811-839. DOI: 10.1093/jae/ejr019.

Calibration basis: M17-G1 CM calibration decision document
  docs/calibration/m17-g1-elasticity-calibration-decision.md §3.1
Sprint: M17-G1 | Issue: #1229 | CM: Chief Methodologist 2026-06-25
"""
from __future__ import annotations

from alembic import op

revision = "a3b5d7f9e2c1"
down_revision = "a2c4e6f8b0d1"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        """
        INSERT INTO source_registry (
            source_id, name, provider, dataset_name, version,
            permanent_url, access_date, license,
            coverage_start, coverage_end, coverage_countries,
            quality_tier, simulation_variables, known_limitations
        ) VALUES (
            'ACADEMIC_LITERATURE_FOSU_2011_SSA_POVERTY_GROWTH',
            'Fosu (2011): Poverty-Growth Relationship in Sub-Saharan Africa',
            'Journal of African Economies / Oxford University Press',
            'The Effect of Income Distribution on the Poverty-Growth Relationship: '
            'Empirical Evidence from Sub-Saharan Africa',
            '2011',
            'https://doi.org/10.1093/jae/ejr019',
            '2026-06-25',
            'open-access',
            '1970-01-01',
            '2007-12-31',
            ARRAY['BEN', 'BFA', 'CMR', 'CIV', 'ETH', 'GHA', 'GIN', 'KEN',
                  'MDG', 'MLI', 'MOZ', 'MWI', 'NER', 'NGA', 'RWA', 'SEN',
                  'SLE', 'TAN', 'TGO', 'UGA', 'ZMB', 'ZWE'],
            3,
            ARRAY['poverty_headcount_ratio'],
            'Tier 3: Cross-country SSA panel (29 countries, 1970s-2000s). '
            'Income growth elasticity of poverty headcount ratio — not a '
            'direct quarterly-resolution estimate. M17-G1 calibration translates '
            'annual income growth elasticity to gdp_growth_change units via '
            'MacroeconomicModule quarterly-to-annual income approximation. '
            'Point estimate (-0.20) is SSA moderate-inequality mid-range (Gini '
            '0.35-0.40); T3 uncertainty bounds -0.15 to -0.25 reflect '
            'cross-country heterogeneity. T2 upgrade requires Senegal-specific '
            'backtesting against quarterly poverty data (M18 scope). '
            'CM approval: M17-G1 calibration decision doc §3.1 (2026-06-25).'
        )
        ON CONFLICT (source_id) DO NOTHING
        """
    )


def downgrade() -> None:
    op.execute(
        """
        DELETE FROM source_registry
        WHERE source_id = 'ACADEMIC_LITERATURE_FOSU_2011_SSA_POVERTY_GROWTH'
        """
    )
