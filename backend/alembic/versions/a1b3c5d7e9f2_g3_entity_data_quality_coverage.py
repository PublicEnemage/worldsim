# ruff: noqa: E501
"""G3 — ADR-016 Scenario Grounding: entity_data_quality_coverage table + source registry seed

Revision ID: a1b3c5d7e9f2
Revises: f2a5c8e3d1b7
Create Date: 2026-06-17

This migration delivers the database layer for ADR-016 (Scenario Grounding Architecture),
Sprint M14-G3. Three changes:

1. New table: entity_data_quality_coverage
   Per-(entity, measurement_framework, year-range) data quality metadata. Queried by
   GET /api/v1/entities/{entity_id}/data-quality?year={year} to produce the pre-creation
   data quality preview (ADR-016 Component 1).

2. source_registry seed: five sources used by GRC, JOR, EGY, ZMB initial conditions.
   Inserts are ON CONFLICT DO NOTHING — safe on databases that already have these entries.
   Sources seeded:
     CBJ_ANNUAL_2023   — Central Bank of Jordan Annual Report 2023 (T2, reserves)
     IMF_WEO_APR2024   — IMF WEO April 2024 (T2, GDP growth, trend growth)
     DOS_LFS_Q1_2024   — Jordan Dept of Statistics LFS Q1 2024 (T2, unemployment)
     NE_110M_2024_SRC  — Natural Earth 110m, if not already seeded by the loader
     IMF_WB_GRC_2010   — IMF / World Bank consolidated Greece 2010 source (T2, backtesting)

3. simulation_entities UPSERT for JOR: adds reserve_coverage_months, gdp_growth,
   unemployment_rate, and trend_growth in the SA-09 JSONB envelope format.
   Uses JSONB merge (||) so existing attributes (e.g. Natural Earth Level 1 data)
   are preserved. These three attributes are required for AC-6 and AC-7 — the
   /initial-state endpoint reads from the step-0 snapshot which is seeded from
   simulation_entities.

4. entity_data_quality_coverage seed rows for GRC, JOR, EGY, ZMB covering Financial
   and Human Development frameworks at the year ranges for which data was available.

ADR reference: ADR-016 §Component 1 and §Component 2, §EL Decision 1 (entity scope).
Sprint entry: docs/process/sprint-plans/m14-g3-sprint-entry.md
Intent document: docs/process/intents/M14-G3-2026-06-17-adr016-backend.md
"""
from __future__ import annotations

import sqlalchemy as sa

from alembic import op

revision = "a1b3c5d7e9f2"
down_revision = "f2a5c8e3d1b7"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ── 1. Create entity_data_quality_coverage table ─────────────────────────
    op.create_table(
        "entity_data_quality_coverage",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("entity_id", sa.Text(), nullable=False),
        sa.Column("measurement_framework", sa.Text(), nullable=False),
        sa.Column("coverage_year_from", sa.Integer(), nullable=False),
        sa.Column("coverage_year_to", sa.Integer(), nullable=True),
        sa.Column("confidence_tier", sa.Integer(), nullable=False),
        sa.Column("source_institution", sa.Text(), nullable=True),
        sa.Column("data_vintage", sa.Text(), nullable=True),
        sa.Column("is_synthetic", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("synthetic_basis", sa.Text(), nullable=True),
        sa.CheckConstraint(
            "confidence_tier BETWEEN 1 AND 5",
            name="ck_edqc_confidence_tier",
        ),
    )
    op.create_index(
        "idx_edqc_entity_framework_year",
        "entity_data_quality_coverage",
        ["entity_id", "measurement_framework", "coverage_year_from"],
    )

    # ── 2. Seed source_registry entries ─────────────────────────────────────
    # ON CONFLICT DO NOTHING — safe on databases where these sources already exist
    # (e.g., if the natural earth loader seeded NE_110M_2024 before this migration).
    op.execute(
        """
        INSERT INTO source_registry (
            source_id, name, provider, dataset_name, version,
            permanent_url, access_date, license,
            coverage_start, coverage_end, coverage_countries,
            quality_tier, simulation_variables, known_limitations
        ) VALUES
        (
            'CBJ_ANNUAL_2023',
            'Central Bank of Jordan Annual Report 2023',
            'CBJ',
            'Annual Report',
            '2023',
            'https://www.cbj.gov.jo/EchoBusV3.0/SystemAssets/PDFs/AR/Annual%20Report%202023.pdf',
            '2024-01-15',
            'government-open',
            '2023-01-01',
            '2023-12-31',
            ARRAY['JOR'],
            2,
            ARRAY['reserve_coverage_months'],
            'Published by the Central Bank of Jordan. Covers domestic reserve position. '
            'Confidence T2: official government statistics, annual vintage.'
        ),
        (
            'IMF_WEO_APR2024',
            'IMF World Economic Outlook April 2024',
            'IMF WEO',
            'World Economic Outlook',
            'April 2024',
            'https://www.imf.org/en/Publications/WEO/Issues/2024/04/16/world-economic-outlook-april-2024',
            '2024-04-16',
            'imf-open',
            '2000-01-01',
            '2024-03-31',
            ARRAY['GRC', 'JOR', 'EGY', 'ZMB'],
            2,
            ARRAY['gdp_growth', 'trend_growth'],
            'IMF WEO April 2024 macroeconomic projections. T2: IMF institutional forecast '
            'with cross-country methodology. Growth projections may diverge from final '
            'outturn; calendar-year vs fiscal-year alignment required for some countries.'
        ),
        (
            'DOS_LFS_Q1_2024',
            'Jordan Department of Statistics Labour Force Survey Q1 2024',
            'DOS',
            'Labour Force Survey',
            'Q1 2024',
            'https://www.dos.gov.jo/dos_home_a/main/linked-html/labor_force.htm',
            '2024-06-01',
            'government-open',
            '2024-01-01',
            '2024-03-31',
            ARRAY['JOR'],
            2,
            ARRAY['unemployment_rate'],
            'Jordan official unemployment statistics. T2: official LFS with documented '
            'ILO methodology. Understates informal sector underemployment (est. 20-25% '
            'of labour force in informal arrangements not captured as unemployed).'
        ),
        (
            'IMF_WB_GRC_2010',
            'IMF / World Bank consolidated Greece 2010 macroeconomic data',
            'IMF / World Bank',
            'WEO + WDI consolidated',
            '2010',
            'https://www.imf.org/external/pubs/ft/weo/2010/02/weodata/index.aspx',
            '2024-01-01',
            'imf-open',
            '2000-01-01',
            '2015-12-31',
            ARRAY['GRC'],
            2,
            ARRAY['gdp_growth', 'reserve_coverage_months', 'unemployment_rate'],
            'Consolidated IMF WEO and World Bank WDI data for Greece backtesting period '
            '2000-2015. T2: IMF/WB institutional statistics with documented methodology. '
            'Used as calibration basis for Greek sovereign debt crisis validation.'
        ),
        (
            'WORLD_BANK_WDI_2023',
            'World Bank World Development Indicators 2023',
            'World Bank WDI',
            'World Development Indicators',
            '2023',
            'https://databank.worldbank.org/source/world-development-indicators',
            '2024-01-01',
            'cc-by-4.0',
            '1960-01-01',
            '2023-12-31',
            ARRAY['GRC', 'JOR', 'EGY', 'ZMB'],
            2,
            ARRAY['unemployment_rate', 'health_expenditure_pct_gdp', 'net_enrollment_rate'],
            'World Bank WDI annual data. T2: institutional statistics with documented '
            'methodology. Some indicators have 2-3 year reporting lag (most recent '
            'observation may be 2021-2022 for some countries / indicators).'
        )
        ON CONFLICT (source_id) DO NOTHING
        """
    )

    # ── 3. Upsert JOR simulation entity attributes ────────────────────────────
    # Adds simulation-specific initial condition attributes to JOR in
    # simulation_entities. Uses JSONB merge (||) to preserve existing attributes
    # (e.g., Natural Earth Level 1: population_total, gdp_usd_millions, geometry).
    #
    # These three attributes are required for the /initial-state endpoint tests:
    #   reserve_coverage_months — AC-7 (Persona 2 north star indicator)
    #   gdp_growth              — AC-6 (at least one financial indicator)
    #   unemployment_rate       — AC-6 (at least one human_development indicator)
    #   trend_growth            — supports MacroeconomicModule mean-reversion channel
    #
    # SA-09 JSONB envelope: _envelope_version, value (str), unit, variable_type,
    # confidence_tier, observation_date (ISO-8601), source_registry_id,
    # measurement_framework. See quantity_serde.py for the canonical format.
    op.execute(
        """
        INSERT INTO simulation_entities (entity_id, entity_type, attributes, metadata)
        VALUES (
            'JOR',
            'country',
            '{
              "reserve_coverage_months": {
                "_envelope_version": "1",
                "value": "7.1",
                "unit": "months",
                "variable_type": "ratio",
                "confidence_tier": 2,
                "observation_date": "2023-12-31",
                "source_registry_id": "CBJ_ANNUAL_2023",
                "measurement_framework": "financial"
              },
              "gdp_growth": {
                "_envelope_version": "1",
                "value": "0.025",
                "unit": "ratio",
                "variable_type": "ratio",
                "confidence_tier": 2,
                "observation_date": "2024-04-01",
                "source_registry_id": "IMF_WEO_APR2024",
                "measurement_framework": "financial"
              },
              "trend_growth": {
                "_envelope_version": "1",
                "value": "0.030",
                "unit": "ratio",
                "variable_type": "ratio",
                "confidence_tier": 3,
                "observation_date": "2024-01-01",
                "source_registry_id": "IMF_WEO_APR2024",
                "measurement_framework": "financial"
              },
              "unemployment_rate": {
                "_envelope_version": "1",
                "value": "0.178",
                "unit": "ratio",
                "variable_type": "ratio",
                "confidence_tier": 2,
                "observation_date": "2024-03-01",
                "source_registry_id": "DOS_LFS_Q1_2024",
                "measurement_framework": "human_development"
              }
            }'::jsonb,
            '{}'::jsonb
        )
        ON CONFLICT (entity_id) DO UPDATE
            SET attributes = simulation_entities.attributes || EXCLUDED.attributes
        """
    )

    # ── 4. Seed entity_data_quality_coverage rows ─────────────────────────────
    # Coverage rows for GRC, JOR, EGY, ZMB per ADR-016 §EL Decision 1.
    # Year ranges:
    #   GRC: 2000–2015 financial/HD at T2 (IMF/WB observed data — Greece crisis period)
    #   JOR: 2020–ongoing financial T2 (CBJ/IMF), HD T2 (ILO/WB), ecological T4 synthetic
    #   EGY: 2020–ongoing financial T2 (CBE/IMF), HD T2 (WB), ecological T4 synthetic
    #   ZMB: 2020–ongoing financial T3 synthetic (IMF WEO + SADC comparables), HD T2 (WB), ecological T4 synthetic
    #
    # The /data-quality endpoint selects WHERE coverage_year_from <= year AND
    # (coverage_year_to IS NULL OR coverage_year_to >= year).
    # Returning empty list for unsupported years is correct behaviour (SF-1 guard).
    op.execute(
        """
        INSERT INTO entity_data_quality_coverage (
            entity_id, measurement_framework,
            coverage_year_from, coverage_year_to,
            confidence_tier, source_institution, data_vintage,
            is_synthetic, synthetic_basis
        ) VALUES
        -- GRC: IMF/World Bank observed data 2000–2015 (backtesting period)
        ('GRC', 'financial',         2000, 2015, 2, 'IMF / World Bank', '2015-Q4', false, NULL),
        ('GRC', 'human_development', 2000, 2015, 2, 'ILO / World Bank', '2015-Q4', false, NULL),
        ('GRC', 'ecological',        2000, 2015, 3, 'IEA',              '2015-Q4', false, NULL),

        -- JOR: IMF / CBJ observed data 2020–ongoing
        ('JOR', 'financial',         2020, NULL, 2, 'IMF WEO / CBJ',   '2024-Q1', false, NULL),
        ('JOR', 'human_development', 2020, NULL, 2, 'World Bank WDI',  '2023-Q4', false, NULL),
        ('JOR', 'ecological',        2020, NULL, 4, NULL,               NULL,      true,  'MENA comparable economies 2022-2023'),
        ('JOR', 'governance',        2020, NULL, 3, 'V-Dem / WB WGI',  '2023-Q4', false, NULL),
        ('JOR', 'political_economy', 2020, NULL, 3, 'V-Dem',           '2023-Q4', false, NULL),

        -- EGY: IMF / CBE observed data 2020–ongoing
        ('EGY', 'financial',         2020, NULL, 2, 'IMF WEO / CBE',   '2024-Q1', false, NULL),
        ('EGY', 'human_development', 2020, NULL, 2, 'World Bank WDI',  '2023-Q4', false, NULL),
        ('EGY', 'ecological',        2020, NULL, 4, NULL,               NULL,      true,  'MENA comparable economies 2022-2023'),
        ('EGY', 'governance',        2020, NULL, 3, 'V-Dem / WB WGI',  '2023-Q4', false, NULL),

        -- ZMB: IMF WEO + SADC synthetic composites 2020–ongoing
        ('ZMB', 'financial',         2020, NULL, 3, 'IMF WEO',         '2023-Q4', true,  'SADC comparable economies 2022-2023'),
        ('ZMB', 'human_development', 2020, NULL, 2, 'World Bank WDI',  '2023-Q3', false, NULL),
        ('ZMB', 'ecological',        2020, NULL, 4, NULL,               NULL,      true,  'SADC comparable economies 2022-2023'),
        ('ZMB', 'governance',        2020, NULL, 4, NULL,               NULL,      true,  'SSA comparable governance proxies 2022')
        """
    )


def downgrade() -> None:
    op.execute(
        "DELETE FROM entity_data_quality_coverage WHERE entity_id IN ('GRC', 'JOR', 'EGY', 'ZMB')"
    )
    op.execute(
        """
        UPDATE simulation_entities
        SET attributes = attributes - 'reserve_coverage_months' - 'gdp_growth' - 'trend_growth' - 'unemployment_rate'
        WHERE entity_id = 'JOR'
        """
    )
    op.execute(
        """
        DELETE FROM source_registry
        WHERE source_id IN (
            'CBJ_ANNUAL_2023', 'IMF_WEO_APR2024', 'DOS_LFS_Q1_2024',
            'IMF_WB_GRC_2010', 'WORLD_BANK_WDI_2023'
        )
        """
    )
    op.drop_index("idx_edqc_entity_framework_year", table_name="entity_data_quality_coverage")
    op.drop_table("entity_data_quality_coverage")
