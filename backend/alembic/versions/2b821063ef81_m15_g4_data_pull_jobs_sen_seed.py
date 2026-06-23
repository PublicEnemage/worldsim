# ruff: noqa: E501
"""M15-G4 — data_pull_jobs table + SEN source_registry seed

Revision ID: 2b821063ef81
Revises: b1c2d3e4f5a6
Create Date: 2026-06-22

This migration delivers the database layer for M15-G4 (Path 1: approved source
network query at scenario creation), DA-G4-1 and DA-G4-2:

1. New table: data_pull_jobs
   Tracks the lifecycle of async data pull requests triggered from the
   scenario creation form when a user selects a non-preloaded registered-source
   entity. Status lifecycle: queued → running → complete | failed.

2. source_registry seed: SEN (Senegal) — World Bank WDI 2022 coverage.
   Provides a non-preloaded entity with registered source coverage to exercise
   the Path 1 loadable=True / load_action_available=True code path.
   INSERT is ON CONFLICT DO NOTHING — safe on databases that already have
   this entry.

ADR reference: M15 G4 sprint entry (docs/process/sprint-plans/m15-g4-sprint-entry.md)
Intent document: docs/process/intents/M15-G4-2026-06-22-path1-fidelity-contextualisation.md
"""
from __future__ import annotations

import sqlalchemy as sa

from alembic import op

revision = "2b821063ef81"
down_revision = "b1c2d3e4f5a6"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ── 1. Create data_pull_jobs table ────────────────────────────────────────
    op.create_table(
        "data_pull_jobs",
        sa.Column("job_id", sa.Text(), nullable=False),
        sa.Column("entity_id", sa.Text(), nullable=False),
        sa.Column("year", sa.Integer(), nullable=False),
        sa.Column("status", sa.Text(), nullable=False, server_default="queued"),
        sa.Column("frameworks_loaded", sa.ARRAY(sa.String()), nullable=False, server_default="{}"),
        sa.Column("error", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.PrimaryKeyConstraint("job_id"),
        sa.CheckConstraint(
            "status IN ('queued', 'running', 'complete', 'failed')",
            name="ck_data_pull_jobs_status",
        ),
    )
    op.create_index("idx_data_pull_jobs_entity_year", "data_pull_jobs", ["entity_id", "year"])

    # ── 2. Seed SEN in source_registry ───────────────────────────────────────
    # SEN = Senegal — World Bank WDI coverage for financial + human_development frameworks.
    # Provides a non-preloaded entity with registered source coverage for Path 1 testing.
    # ON CONFLICT DO NOTHING — safe on databases where this entry already exists.
    op.execute("""
        INSERT INTO source_registry (
            source_id, name, provider, dataset_name, version, permanent_url,
            access_date, license, coverage_start, coverage_end, coverage_countries,
            quality_tier, simulation_variables, known_limitations
        )
        SELECT
            'wb_wdi_sen_2022',
            'World Bank WDI — Senegal 2022',
            'World Bank WDI 2022',
            'World Development Indicators',
            '2022',
            'https://databank.worldbank.org/source/world-development-indicators',
            '2023-01-01',
            'CC-BY 4.0',
            '2000-01-01',
            '2022-12-31',
            ARRAY['SEN'],
            3,
            ARRAY['gdp_growth', 'inflation_rate', 'debt_to_gdp', 'reserve_coverage_months',
                  'health_expenditure_pct_gdp', 'net_enrollment_rate'],
            'Coverage limited to WDI 2022 vintage. Senegal macroeconomic data has a 1-2 year reporting lag.'
        WHERE NOT EXISTS (SELECT 1 FROM source_registry WHERE source_id = 'wb_wdi_sen_2022')
    """)


def downgrade() -> None:
    op.drop_index("idx_data_pull_jobs_entity_year", table_name="data_pull_jobs")
    op.drop_table("data_pull_jobs")
    op.execute("DELETE FROM source_registry WHERE source_id = 'wb_wdi_sen_2022'")
