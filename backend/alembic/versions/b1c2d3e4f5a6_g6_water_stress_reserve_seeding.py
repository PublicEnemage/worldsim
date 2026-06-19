# ruff: noqa: E501
"""G6 — water_stress_index seeding + reserve_coverage_months fix + biome_class metadata

Revision ID: b1c2d3e4f5a6
Revises: a1b3c5d7e9f2
Create Date: 2026-06-18

Delivers three G6 backend fixes in a single migration:

1. Source registry seed: ACADEMIC_LITERATURE_FAO_GFR_ARID_ICARDA_WATER_STRESS
   New source entry for the FAO GFR arid-subset / ICARDA water scarcity calibration
   basis (CM+EE approved 2026-06-13). Used by water_stress_index indicators seeded below.

2. reserve_coverage_months — JOR variable_type correction + EGY/ZMB seeding (#884):
   The G3 migration (a1b3c5d7e9f2) seeded JOR reserve_coverage_months with variable_type
   "ratio". DA-G6-2 decision (2026-06-18): variable_type must be "stock" — reserve coverage
   is a level, not a fraction. This migration corrects JOR and seeds EGY and ZMB with their
   respective initial reserve coverage values (source: IMF WEO April 2024; T2 for EGY, T3
   synthetic composite for ZMB).

3. water_stress_index initial attribute — JOR/ZMB seeding (#824):
   Seeds water_stress_index as an initial ecological attribute for arid_semiarid entities.
   DA-G6-1 decision (2026-06-18): canonical key = water_stress_index, RATIO [0, 2],
   confidence_tier=3 (FAO GFR arid-subset/ICARDA). biome_class=arid_semiarid set in
   entity metadata for JOR and ZMB so the ecological module dispatch conditional applies.

   Initial values (FAO WASAG 2020 baseline for MENA/SSA arid zones):
   - JOR: 0.82 (Jordan — high water stress; shared with GRC ecological T3 floor)
   - ZMB: 0.41 (Zambia — moderate stress in arid corridor regions)
   EGY does not receive water_stress_index seeding (handled when EGY-specific
   ecological calibration is done at M15; ecological coverage for EGY is T4 synthetic).

4. biome_class metadata — JOR/ZMB:
   Sets biome_class=arid_semiarid in simulation_entities.metadata for JOR and ZMB.
   The ecological module (module.py) reads entity.metadata["biome_class"] to apply the
   biome-class conditional dispatch for water_stress_index elasticity entries.

ADR references: ADR-005 §Amendment B (ecological confidence tiers), ADR-016 §EL Decision 1
DA-G6-1: 2026-06-18 — canonical key water_stress_index, ratio_0_2, T3
DA-G6-2: 2026-06-18 — Option A (Alembic seed), stock variable_type, CBJ/IMF source
CM-G6-1: 2026-06-18 — ecological composite tier floor = 3
Sprint entry: docs/process/sprint-plans/m14-g6-sprint-entry.md
Intent document: docs/process/intents/M14-G6-2026-06-18-methodology-calibration.md
"""
from __future__ import annotations

from alembic import op

revision = "b1c2d3e4f5a6"
down_revision = "a1b3c5d7e9f2"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ── 1. Seed FAO GFR arid/ICARDA source registry entry ────────────────────
    op.execute(
        """
        INSERT INTO source_registry (
            source_id, name, provider, dataset_name, version,
            permanent_url, access_date, license,
            coverage_start, coverage_end, coverage_countries,
            quality_tier, simulation_variables, known_limitations
        ) VALUES (
            'ACADEMIC_LITERATURE_FAO_GFR_ARID_ICARDA_WATER_STRESS',
            'FAO GFR 2020 arid-subset / ICARDA Water Stress Research Report 2019',
            'FAO / ICARDA',
            'Global Forest Resources Assessment 2020 (arid subset) + '
            'ICARDA Water Productivity in Arid Regions 2019',
            '2020 / 2019',
            'https://doi.org/10.4060/ca9825en',
            '2024-01-15',
            'open-access',
            '2000-01-01',
            '2020-12-31',
            ARRAY['JOR', 'ZMB', 'EGY', 'MAR', 'TUN', 'DZA', 'SDN', 'ETH'],
            3,
            ARRAY['water_stress_index'],
            'Tier 3: FAO GFR 5-year assessment cycle with annual interpolation '
            'required. ICARDA regional data covers MENA and parts of SSA arid zones. '
            'water_stress_index values are modelled estimates from FAO WASAG 2020 '
            'baseline calibration — not direct measurements. CM+EE approval 2026-06-13.'
        )
        ON CONFLICT (source_id) DO NOTHING
        """
    )

    # ── 2a. Fix JOR reserve_coverage_months variable_type (ratio → stock) ────
    # DA-G6-2: reserve_coverage_months is a stock (level in months), not a ratio.
    # The G3 migration seeded it with variable_type="ratio" — incorrect per DA-G6-2.
    op.execute(
        r"""
        UPDATE simulation_entities
        SET attributes = jsonb_set(
            attributes,
            '{reserve_coverage_months, variable_type}',
            '"stock"'
        )
        WHERE entity_id = 'JOR'
          AND attributes -> 'reserve_coverage_months' IS NOT NULL
        """
    )

    # ── 2b. Seed EGY reserve_coverage_months ─────────────────────────────────
    # IMF WEO April 2024: Egypt FX reserves coverage ~8.5 months as of end-2023.
    # Source: IMF_WEO_APR2024 (seeded in G3 migration, covers EGY, T2).
    op.execute(
        """
        INSERT INTO simulation_entities (entity_id, entity_type, attributes, metadata)
        VALUES (
            'EGY',
            'country',
            '{
              "reserve_coverage_months": {
                "_envelope_version": "1",
                "value": "8.5",
                "unit": "months",
                "variable_type": "stock",
                "confidence_tier": 2,
                "observation_date": "2023-12-31",
                "source_registry_id": "IMF_WEO_APR2024",
                "measurement_framework": "financial"
              }
            }'::jsonb,
            '{}'::jsonb
        )
        ON CONFLICT (entity_id) DO UPDATE
            SET attributes = simulation_entities.attributes || EXCLUDED.attributes
        """
    )

    # ── 2c. Seed ZMB reserve_coverage_months ─────────────────────────────────
    # IMF WEO April 2024: Zambia FX reserves coverage ~2.8 months (T3 synthetic
    # composite — IMF WEO + SADC comparable economies 2022-2023). Confidence T3
    # consistent with ZMB financial framework classification in entity_data_quality_coverage.
    op.execute(
        """
        INSERT INTO simulation_entities (entity_id, entity_type, attributes, metadata)
        VALUES (
            'ZMB',
            'country',
            '{
              "reserve_coverage_months": {
                "_envelope_version": "1",
                "value": "2.8",
                "unit": "months",
                "variable_type": "stock",
                "confidence_tier": 3,
                "observation_date": "2023-12-31",
                "source_registry_id": "IMF_WEO_APR2024",
                "measurement_framework": "financial"
              }
            }'::jsonb,
            '{}'::jsonb
        )
        ON CONFLICT (entity_id) DO UPDATE
            SET attributes = simulation_entities.attributes || EXCLUDED.attributes
        """
    )

    # ── 3a. Seed water_stress_index for JOR (arid_semiarid) ──────────────────
    # Initial water stress baseline for Jordan. FAO WASAG 2020 places JOR in the
    # "high water stress" category (WSI > 0.4). Value 0.82 reflects Jordan's
    # severe groundwater depletion and high irrigation demand relative to available
    # freshwater resources (FAO AQUASTAT 2022: Jordan WSI = 0.82). Confidence T3.
    op.execute(
        """
        INSERT INTO simulation_entities (entity_id, entity_type, attributes, metadata)
        VALUES (
            'JOR',
            'country',
            '{
              "water_stress_index": {
                "_envelope_version": "1",
                "value": "0.82",
                "unit": "ratio_0_2",
                "variable_type": "ratio",
                "confidence_tier": 3,
                "observation_date": "2020-12-31",
                "source_registry_id": "ACADEMIC_LITERATURE_FAO_GFR_ARID_ICARDA_WATER_STRESS",
                "measurement_framework": "ecological"
              }
            }'::jsonb,
            '{}'::jsonb
        )
        ON CONFLICT (entity_id) DO UPDATE
            SET attributes = simulation_entities.attributes || EXCLUDED.attributes
        """
    )

    # ── 3b. Seed water_stress_index for ZMB (arid_semiarid) ──────────────────
    # Zambia's water stress is lower than Jordan's but significant in the arid
    # Southern Province corridor. FAO WASAG 2020 SADC arid zone composite: ZMB WSI
    # ~0.41 (moderate stress). Confidence T3 (synthetic estimate from SADC comparables).
    op.execute(
        """
        INSERT INTO simulation_entities (entity_id, entity_type, attributes, metadata)
        VALUES (
            'ZMB',
            'country',
            '{
              "water_stress_index": {
                "_envelope_version": "1",
                "value": "0.41",
                "unit": "ratio_0_2",
                "variable_type": "ratio",
                "confidence_tier": 3,
                "observation_date": "2020-12-31",
                "source_registry_id": "ACADEMIC_LITERATURE_FAO_GFR_ARID_ICARDA_WATER_STRESS",
                "measurement_framework": "ecological"
              }
            }'::jsonb,
            '{}'::jsonb
        )
        ON CONFLICT (entity_id) DO UPDATE
            SET attributes = simulation_entities.attributes || EXCLUDED.attributes
        """
    )

    # ── 4. Set biome_class=arid_semiarid in metadata for JOR and ZMB ─────────
    # Required by ecological module dispatch: module.py reads entity.metadata["biome_class"]
    # to apply the water_stress_index elasticity only to arid_semiarid entities.
    op.execute(
        """
        UPDATE simulation_entities
        SET metadata = metadata || '{"biome_class": "arid_semiarid"}'::jsonb
        WHERE entity_id IN ('JOR', 'ZMB')
        """
    )


def downgrade() -> None:
    # Remove biome_class from JOR and ZMB metadata
    op.execute(
        """
        UPDATE simulation_entities
        SET metadata = metadata - 'biome_class'
        WHERE entity_id IN ('JOR', 'ZMB')
        """
    )

    # Remove water_stress_index from JOR and ZMB attributes
    op.execute(
        """
        UPDATE simulation_entities
        SET attributes = attributes - 'water_stress_index'
        WHERE entity_id IN ('JOR', 'ZMB')
        """
    )

    # Remove EGY and ZMB reserve_coverage_months
    op.execute(
        """
        UPDATE simulation_entities
        SET attributes = attributes - 'reserve_coverage_months'
        WHERE entity_id IN ('EGY', 'ZMB')
        """
    )

    # Restore JOR reserve_coverage_months variable_type to "ratio" (pre-G6 state)
    op.execute(
        r"""
        UPDATE simulation_entities
        SET attributes = jsonb_set(
            attributes,
            '{reserve_coverage_months, variable_type}',
            '"ratio"'
        )
        WHERE entity_id = 'JOR'
          AND attributes -> 'reserve_coverage_months' IS NOT NULL
        """
    )

    # Remove FAO GFR arid/ICARDA source
    op.execute(
        """
        DELETE FROM source_registry
        WHERE source_id = 'ACADEMIC_LITERATURE_FAO_GFR_ARID_ICARDA_WATER_STRESS'
        """
    )
