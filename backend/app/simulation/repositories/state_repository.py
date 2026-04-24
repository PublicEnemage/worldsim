"""SimulationStateRepository — loads initial SimulationState from PostGIS.

ADR-004 Decision 2. Reads simulation_entities rows and converts JSONB attribute
envelopes to Quantity objects (SA-09 format), building a SimulationState for the
ScenarioRunner.

For M3, relationships are not loaded (empty list). The engine propagation graph
operates on whatever relationships are present — an empty list means no propagation
across entities, which is correct for single-entity Greece backtesting scenarios.

Follows the asyncpg direct-query pattern from ADR-003 Decision 2.
"""
from __future__ import annotations

import json
from datetime import UTC, datetime
from typing import Any

import asyncpg  # noqa: TCH002 — used in method signatures at runtime

from app.simulation.engine.models import (
    ResolutionConfig,
    ScenarioConfig,
    SimulationEntity,
    SimulationState,
)
from app.simulation.repositories.quantity_serde import quantity_from_jsonb


class SimulationStateRepository:
    """Loads initial simulation state from the PostGIS database.

    The loaded state is a pure Python SimulationState — no database references
    remain after construction. The ScenarioRunner operates entirely on the
    in-memory objects returned here.
    """

    async def load_initial_state(
        self,
        conn: asyncpg.Connection,
        entity_ids: list[str],
        scenario_id: str,
        scenario_name: str,
        timestep: datetime,
    ) -> SimulationState:
        """Load entities from simulation_entities and build SimulationState.

        Args:
            conn: asyncpg connection. Not closed by this method.
            entity_ids: List of entity_id values to load. Empty list returns
                a state with no entities.
            scenario_id: Used to populate ScenarioConfig.scenario_id.
            scenario_name: Used to populate ScenarioConfig.name.
            timestep: Initial simulation timestep for this state.

        Returns:
            SimulationState with entities populated from DB attributes.

        Raises:
            ValueError: If any entity_id in entity_ids is absent from
                simulation_entities.
        """
        entities: dict[str, SimulationEntity] = {}

        if entity_ids:
            rows = await conn.fetch(
                """
                SELECT entity_id, entity_type, attributes, metadata
                FROM simulation_entities
                WHERE entity_id = ANY($1::text[])
                """,
                entity_ids,
            )
            found_ids = {row["entity_id"] for row in rows}
            missing = sorted(set(entity_ids) - found_ids)
            if missing:
                raise ValueError(
                    f"Entity IDs not found in simulation_entities: {missing}. "
                    "Ensure these entities were seeded before running the scenario."
                )

            for row in rows:
                entities[row["entity_id"]] = _build_entity(row)

        scenario_config = ScenarioConfig(
            scenario_id=scenario_id,
            name=scenario_name,
            description="",
            start_date=timestep,
            end_date=timestep,
        )

        return SimulationState(
            timestep=timestep,
            resolution=ResolutionConfig(),
            entities=entities,
            relationships=[],
            events=[],
            scenario_config=scenario_config,
        )


# ---------------------------------------------------------------------------
# Private helpers
# ---------------------------------------------------------------------------


def _build_entity(row: Any) -> SimulationEntity:  # noqa: ANN401 — asyncpg Record
    """Construct a SimulationEntity from an asyncpg row dict."""
    import contextlib  # noqa: PLC0415

    from app.simulation.engine.quantity import Quantity  # noqa: PLC0415, TCH001

    attrs_raw = row["attributes"]
    if isinstance(attrs_raw, str):
        attrs_raw = json.loads(attrs_raw)

    attributes: dict[str, Quantity] = {}
    if isinstance(attrs_raw, dict):
        for key, val in attrs_raw.items():
            if isinstance(val, dict):
                with contextlib.suppress(ValueError, KeyError):
                    attributes[key] = quantity_from_jsonb(val)

    meta_raw = row["metadata"]
    if isinstance(meta_raw, str):
        meta_raw = json.loads(meta_raw)

    return SimulationEntity(
        id=row["entity_id"],
        entity_type=row["entity_type"],
        attributes=attributes,
        metadata=meta_raw if isinstance(meta_raw, dict) else {},
    )


def _default_timestep() -> datetime:
    """Return the M3 default base timestep (2000-01-01 UTC).

    Used when no explicit base_date is provided in the scenario configuration.
    A fixed sentinel ensures SA-11 determinism: two runs with the same config
    and no explicit date always start from the same timestep.
    """
    return datetime(2000, 1, 1, tzinfo=UTC)
