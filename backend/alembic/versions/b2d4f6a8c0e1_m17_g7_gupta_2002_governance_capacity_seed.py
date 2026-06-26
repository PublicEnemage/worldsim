# ruff: noqa: E501
"""M17-G7: seed ACADEMIC_LITERATURE_GUPTA_2002_IMF_WP_INSTITUTIONAL_CAPACITY in source_registry

Revision ID: b2d4f6a8c0e1
Revises: a3b5d7f9e2c1
Create Date: 2026-06-26

Registers the Gupta et al. (2002) IMF WP/02/77 source introduced by the M17-G7
GovernanceElasticity entry for fiscal_policy_spending_change →
institutional_capacity_index (#1275). Also adds SEN governance coverage row to
entity_data_quality_coverage (T2 CPIA, 2023).

Gupta, S., Clements, B., Baldacci, E. and Mulas-Granados, C. (2002):
Expenditure Composition, Fiscal Adjustment, and Growth in Low-Income Countries.
IMF Working Paper WP/02/77.

CM position: M17-G1 Governance Sensitivity Specification §Question 2 (2026-06-25).
Sprint: M17-G7 | Issue: #1275 | CM: Chief Methodologist 2026-06-26
"""
from __future__ import annotations

from alembic import op

revision = "b2d4f6a8c0e1"
down_revision = "a3b5d7f9e2c1"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ── 1. Seed Gupta 2002 in source_registry ────────────────────────────────
    op.execute(
        """
        INSERT INTO source_registry (
            source_id, name, provider, dataset_name, version,
            permanent_url, access_date, license,
            coverage_start, coverage_end, coverage_countries,
            quality_tier, simulation_variables, known_limitations
        ) VALUES (
            'ACADEMIC_LITERATURE_GUPTA_2002_IMF_WP_INSTITUTIONAL_CAPACITY',
            'Gupta et al. (2002): Expenditure Composition, Fiscal Adjustment, and Growth in LICs',
            'IMF Research Department',
            'Expenditure Composition, Fiscal Adjustment, and Growth in Low-Income Countries',
            'IMF Working Paper WP/02/77',
            'https://www.imf.org/en/Publications/WP/Issues/2016/12/30/Expenditure-Composition-Fiscal-Adjustment-and-Growth-in-Low-Income-Countries-15820',
            '2026-06-26',
            'open-access',
            '1985-01-01',
            '2000-12-31',
            ARRAY['BEN', 'BFA', 'CMR', 'CIV', 'ETH', 'GHA', 'GIN', 'KEN',
                  'MDG', 'MLI', 'MOZ', 'MWI', 'NER', 'NGA', 'RWA', 'SEN',
                  'SLE', 'TGO', 'TZA', 'UGA', 'ZMB', 'ZWE'],
            3,
            ARRAY['institutional_capacity_index'],
            'Tier 3: Cross-country SSA LIC panel (1985-2000). Institutional capacity '
            'response to fiscal adjustment — Table 3 elasticity estimates. Point '
            'estimate -0.015 per 1pp fiscal spending change on World Bank CPIA '
            'institutional capacity index normalized [0,1]. T3 confidence: '
            'cross-country inference; Senegal-specific upgrade to T2 requires '
            'CPIA time-series validation (deferred to M18). '
            'CM approval: M17-G1 Governance Sensitivity Specification §Question 2 (2026-06-25).'
        )
        ON CONFLICT (source_id) DO NOTHING
        """
    )

    # ── 2. Seed SEN governance coverage in entity_data_quality_coverage ──────
    # World Bank CPIA score 3.3/6 (published 2023) normalized to [0,1] = 0.55.
    # T2 because it is a World Bank published score, not a synthetic estimate.
    # Coverage from 2023 (the vintage year) onward with NULL end (ongoing).
    op.execute(
        """
        INSERT INTO entity_data_quality_coverage (
            entity_id, measurement_framework,
            coverage_year_from, coverage_year_to,
            confidence_tier, source_institution, data_vintage,
            is_synthetic, synthetic_basis
        ) VALUES (
            'SEN', 'governance', 2023, NULL, 2, 'World Bank CPIA', '2023', false, NULL
        )
        ON CONFLICT DO NOTHING
        """
    )


def downgrade() -> None:
    op.execute(
        """
        DELETE FROM source_registry
        WHERE source_id = 'ACADEMIC_LITERATURE_GUPTA_2002_IMF_WP_INSTITUTIONAL_CAPACITY'
        """
    )
    op.execute(
        """
        DELETE FROM entity_data_quality_coverage
        WHERE entity_id = 'SEN' AND measurement_framework = 'governance'
        """
    )
