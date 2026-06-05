"""SimulationStateRepository — loads initial SimulationState from PostGIS.

ADR-004 Decision 2. Reads simulation_entities rows and converts JSONB attribute
envelopes to Quantity objects (SA-09 format), building a SimulationState for the
ScenarioRunner.

Relationship loading (G6a, Issue #754): when multiple entities are in scope, all
directed edges between them are loaded from the `relationships` table. For each
ordered pair of distinct entities with no real edge, a synthetic Tier 4 "trade"
relationship is injected (weight=0.1, attributes["confidence_tier"]=4,
attributes["synthetic"]=True) so propagation can occur at low confidence.

Follows the asyncpg direct-query pattern from ADR-003 Decision 2.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any

import asyncpg  # noqa: TCH002 — used in method signatures at runtime

from app.simulation.engine.models import (
    Relationship,
    ResolutionConfig,
    ScenarioConfig,
    SimulationEntity,
    SimulationState,
)
from app.simulation.repositories.quantity_serde import quantity_from_jsonb

_SYNTHETIC_RELATIONSHIP_WEIGHT: float = 0.1
_SYNTHETIC_RELATIONSHIP_TYPE: str = "trade"


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

        relationships = await _load_relationships(conn, entity_ids)

        return SimulationState(
            timestep=timestep,
            resolution=ResolutionConfig(),
            entities=entities,
            relationships=relationships,
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


async def _load_relationships(
    conn: asyncpg.Connection,
    entity_ids: list[str],
) -> list[Relationship]:
    """Load directed edges between scenario entities; inject synthetics for missing pairs.

    Queries the `relationships` table for all edges where both source and target
    are in entity_ids. For each ordered pair (a, b) with a ≠ b that has no real
    edge in either direction, a synthetic Tier 4 trade relationship is created in
    both directions (a→b and b→a) at weight 0.1.

    Single-entity scenarios return an empty list (no pairs to fill).
    """
    if len(entity_ids) < 2:
        return []

    rows = await conn.fetch(
        """
        SELECT source_id, target_id, relationship_type, weight, attributes
        FROM relationships
        WHERE source_id = ANY($1::text[]) AND target_id = ANY($1::text[])
        """,
        entity_ids,
    )

    real: list[Relationship] = []
    real_pairs: set[tuple[str, str]] = set()
    for row in rows:
        attrs_raw = row["attributes"]
        if isinstance(attrs_raw, str):
            import json as _json  # noqa: PLC0415
            attrs_raw = _json.loads(attrs_raw)
        real.append(Relationship(
            source_id=row["source_id"],
            target_id=row["target_id"],
            relationship_type=row["relationship_type"],
            weight=float(row["weight"]),
            attributes=attrs_raw if isinstance(attrs_raw, dict) else {},
        ))
        real_pairs.add((row["source_id"], row["target_id"]))

    synthetic: list[Relationship] = []
    for src in entity_ids:
        for tgt in entity_ids:
            if src == tgt:
                continue
            if (src, tgt) not in real_pairs:
                synthetic.append(Relationship(
                    source_id=src,
                    target_id=tgt,
                    relationship_type=_SYNTHETIC_RELATIONSHIP_TYPE,
                    weight=_SYNTHETIC_RELATIONSHIP_WEIGHT,
                    attributes={"confidence_tier": 4, "synthetic": True},
                ))

    return real + synthetic


def _default_timestep() -> datetime:
    """Return the M3 default base timestep (2000-01-01 UTC).

    Used when no explicit base_date is provided in the scenario configuration.
    A fixed sentinel ensures SA-11 determinism: two runs with the same config
    and no explicit date always start from the same timestep.
    """
    return datetime(2000, 1, 1, tzinfo=timezone.utc)  # noqa: UP017
