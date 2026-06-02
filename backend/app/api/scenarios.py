"""Scenario endpoints — ADR-004 Decisions 1, 2, 4, and 5; ADR-005 Decision 2.

Nine endpoints covering scenario configuration lifecycle, execution, and HCL output:
  POST   /scenarios                                        — create scenario (status: pending)
  GET    /scenarios                                        — list all scenarios (created_at desc)
  GET    /scenarios/compare         — snapshot delta; optional step alignment (ADR-004 D5)
  GET    /scenarios/{scenario_id}                          — full detail with scheduled inputs
  DELETE /scenarios/{scenario_id}                          — tombstone + cascade delete, returns 204
  POST   /scenarios/{scenario_id}/run                      — execute pending scenario to completion
  POST   /scenarios/{scenario_id}/advance                  — advance one step (ADR-004 Decision 4)
  GET    /scenarios/{scenario_id}/snapshots                — list all snapshots (ADR-004 Decision 3)
  GET    /scenarios/{scenario_id}/measurement-output — HCL output (ADR-005 Decision 2)

Validation runs at creation time (structural) — entity existence check,
n_steps bounds, step index bounds, non-empty name. Semantic validation
of ControlInput payloads runs at execution time (Issue #111).

All queries use asyncpg directly per ADR-003 Decision 2. Schema management
uses SQLAlchemy ORM via Alembic.

DELETE writes a tombstone to scenario_deleted_tombstones before the CASCADE
executes (ADR-004 Decision 1 Amendment, CONFLICT C-1 disposition). The tombstone
captures full configuration JSONB and scheduled_inputs so the scenario output can
be reconstructed from first principles (SA-11 determinism).
"""
from __future__ import annotations

import contextlib
import json
import logging
import subprocess
import uuid
from collections.abc import Callable
from datetime import datetime  # noqa: TCH003
from decimal import Decimal
from math import floor
from typing import Annotated, Any

import asyncpg  # noqa: TCH002 — used in Annotated[] resolved at runtime by FastAPI
from fastapi import APIRouter, Depends, HTTPException, Response

from app.api.deps import get_db  # noqa: TCH001 — used as Depends(get_db) at runtime
from app.schemas import (
    AdvanceResponse,
    CompareResponse,
    DeltaRecord,
    FrameworkOutput,
    MDAAlert,
    MDAFloorRecord,
    MultiFrameworkOutput,
    QuantitySchema,
    RunSummaryResponse,
    ScenarioConfigSchema,
    ScenarioCreateRequest,
    ScenarioDetailResponse,
    ScenarioResponse,
    ScheduledInputSchema,
    SnapshotRecord,
    TrajectoryFrameworkPoint,
    TrajectoryResponse,
    TrajectoryStep,
)
from app.simulation.mda_checker import alerts_from_events_snapshot
from app.simulation.repositories.quantity_serde import IA1_CANONICAL_PHRASE

_log = logging.getLogger(__name__)

# Engine version for tombstone records — must match app version in main.py.
_ENGINE_VERSION = "0.3.0"


def _resolve_git_commit_hash() -> str:
    """Return the current git commit SHA-1, or 'unknown' if unavailable.

    Called once at module load time. Fails gracefully in environments where
    git is not available (Docker runtime without .git directory, CI without
    full checkout, unit test environments).
    """
    try:
        result = subprocess.check_output(  # noqa: S603
            ["git", "rev-parse", "HEAD"],  # noqa: S607
            stderr=subprocess.DEVNULL,
            timeout=3,
        )
        return result.decode().strip()
    except Exception:  # noqa: BLE001
        return "unknown"


# Resolved once at import time. "unknown" when git is unavailable.
_GIT_COMMIT_HASH: str = _resolve_git_commit_hash()


# INTENT: Enforce engine version compatibility before tombstone reconstruction
#         by comparing the tombstone's engine_version and git_commit_hash
#         against the currently deployed engine.
# PRECONDITIONS: tombstone_engine_version is the engine_version string stored
#                in the tombstone row; tombstone_git_commit_hash is the
#                git_commit_hash stored in the tombstone row, or None for
#                pre-migration tombstones; force_audit_override is False by
#                default (safe path).
# POSTCONDITIONS: Returns None when tombstone is compatible with the live
#                 engine; the caller may proceed with reconstruction. When
#                 force_audit_override=True and a mismatch is detected, a
#                 WARNING is logged and None is returned; no exception raised.
# ERROR CASES: Version mismatch raises HTTPException(409) with both tombstone
#              and live engine_version in the detail string. Hash mismatch
#              (when both sides carry a resolved hash) raises HTTPException(409)
#              with both hashes in the detail string.
# KNOWN LIMITATIONS: NULL tombstone hash (pre-migration tombstone) or
#                    "unknown" on either side disables hash comparison and
#                    falls back to semantic version comparison alone — a hash
#                    collision between different non-git builds cannot be
#                    detected in this mode.
def check_reconstruction_compatibility(
    tombstone_engine_version: str,
    tombstone_git_commit_hash: str | None,
    *,
    force_audit_override: bool = False,
) -> None:
    """Enforce engine version compatibility before any tombstone reconstruction.

    Implements Issue #139 Layer 1: block reconstruction when the tombstone was
    written by a different engine version than is currently deployed. The
    reconstruction guarantee (ADR-004 Decision 1 Amendment, SA-11) is only valid
    for same-version use — cross-version reconstruction silently produces different
    outputs with no error under the old behaviour.

    Comparison logic:
      - Semantic version must match exactly.
      - Git hash is compared only when both sides carry a real hash (neither is
        None or "unknown"). A NULL tombstone hash (pre-migration tombstone) or an
        "unknown" live hash (non-git environment) disables hash comparison and
        falls back to semantic version comparison alone.

    Args:
        tombstone_engine_version: engine_version stored in the tombstone row.
        tombstone_git_commit_hash: git_commit_hash stored in the tombstone row,
            or None for tombstones written before migration c7f4a3e9d2b1.
        force_audit_override: When True, log a WARNING instead of raising. Only
            for explicit audit use cases where the caller accepts the discrepancy.

    Raises:
        HTTPException(409): when tombstone version does not match live engine and
            force_audit_override is False.
    """
    version_match = tombstone_engine_version == _ENGINE_VERSION

    # Hash comparison is meaningful only when both sides have a resolved hash.
    both_hashes_known = (
        tombstone_git_commit_hash is not None
        and tombstone_git_commit_hash != "unknown"
        and _GIT_COMMIT_HASH != "unknown"
    )
    hash_match = (not both_hashes_known) or (tombstone_git_commit_hash == _GIT_COMMIT_HASH)

    if version_match and hash_match:
        return

    detail = (
        f"Tombstone engine_version='{tombstone_engine_version}' "
        f"(git_commit_hash={tombstone_git_commit_hash!r}) does not match "
        f"live engine engine_version='{_ENGINE_VERSION}' "
        f"(git_commit_hash={_GIT_COMMIT_HASH!r}). "
        "Reconstruction against a different engine version may produce outputs "
        "that differ from what the user originally saw (SA-11 determinism). "
        "Pass force_audit_override=True only for explicit audit use cases where "
        "the version discrepancy is understood and accepted."
    )

    if force_audit_override:
        _log.warning("Audit override — reconstruction version mismatch: %s", detail)
        return

    raise HTTPException(status_code=409, detail=detail)

router = APIRouter(tags=["scenarios"])


# ---------------------------------------------------------------------------
# Validation helpers
# ---------------------------------------------------------------------------


def _validate_create_request(req: ScenarioCreateRequest) -> None:
    """Raise HTTPException(422) for any structural validation failure."""
    errors: list[str] = []

    if not req.name.strip():
        errors.append("name must not be empty.")

    n = req.configuration.n_steps
    if n < 1 or n > 100:
        errors.append(f"n_steps must be between 1 and 100 (got {n}).")

    # Step semantics: the engine advances n times producing states at steps 0..n.
    # Inputs at step k are injected during the advance from step k-1 → step k.
    # Step 0 (initial state) and step n (last advance) are both valid injection
    # points, so the valid range is [0, n] inclusive — NOT [0, n-1].
    invalid_steps = [
        si.step
        for si in req.scheduled_inputs
        if si.step < 0 or si.step > n
    ]
    if invalid_steps:
        errors.append(
            f"scheduled_inputs contain steps outside valid range 0–{n}: "
            f"{sorted(set(invalid_steps))}."
        )

    if errors:
        raise HTTPException(status_code=422, detail=" ".join(errors))


async def _validate_entities_exist(
    conn: asyncpg.Connection,
    entity_ids: list[str],
) -> None:
    """Raise HTTPException(422) listing any entity_ids not in simulation_entities."""
    if not entity_ids:
        return
    rows = await conn.fetch(
        "SELECT entity_id FROM simulation_entities WHERE entity_id = ANY($1::text[])",
        entity_ids,
    )
    found = {row["entity_id"] for row in rows}
    missing = sorted(set(entity_ids) - found)
    if missing:
        raise HTTPException(
            status_code=422,
            detail=f"Entity IDs not found in simulation_entities: {missing}.",
        )


# ---------------------------------------------------------------------------
# Horizon degradation — Issue #69
# ---------------------------------------------------------------------------


def effective_tier(source_tier: int, horizon_steps: int) -> int:
    """Return confidence tier degraded by projection horizon.

    Tier degrades by 1 for every 5 projection steps, capped at Tier 5.
    Applied at the output layer (get_measurement_output) so stored snapshots
    are not mutated — distribution fields stay at the output layer per ADR-006.

    Args:
        source_tier:   Original confidence_tier from the stored Quantity (1–5).
        horizon_steps: Step index of the snapshot being queried (0 = baseline).

    Returns:
        Effective tier in range [source_tier, 5].
    """
    return min(5, source_tier + floor(horizon_steps / 5))


# ---------------------------------------------------------------------------
# Response builders
# ---------------------------------------------------------------------------


def _row_to_response(row: dict[str, Any]) -> ScenarioResponse:
    created_at = row["created_at"]
    created_at_str = created_at.isoformat() if hasattr(created_at, "isoformat") else str(created_at)
    return ScenarioResponse(
        scenario_id=row["scenario_id"],
        name=row["name"],
        description=row["description"],
        status=row["status"],
        version=row["version"],
        created_at=created_at_str,
    )


def _build_detail_response(
    row: dict[str, Any],
    inputs: list[dict[str, Any]],
) -> ScenarioDetailResponse:
    created_at = row["created_at"]
    created_at_str = created_at.isoformat() if hasattr(created_at, "isoformat") else str(created_at)

    cfg_raw = row["configuration"]
    if isinstance(cfg_raw, str):
        cfg_raw = json.loads(cfg_raw)

    config = ScenarioConfigSchema(**cfg_raw)
    scheduled = [
        ScheduledInputSchema(
            step=inp["step"],
            input_type=inp["input_type"],
            input_data=inp["input_data"] if isinstance(inp["input_data"], dict)
            else json.loads(inp["input_data"]),
        )
        for inp in inputs
    ]
    return ScenarioDetailResponse(
        scenario_id=row["scenario_id"],
        name=row["name"],
        description=row["description"],
        status=row["status"],
        version=row["version"],
        created_at=created_at_str,
        configuration=config,
        scheduled_inputs=scheduled,
    )


# ---------------------------------------------------------------------------
# POST /scenarios
# ---------------------------------------------------------------------------


@router.post("/scenarios", response_model=ScenarioResponse, status_code=201)
async def create_scenario(
    req: ScenarioCreateRequest,
    conn: Annotated[asyncpg.Connection, Depends(get_db)],
) -> ScenarioResponse:
    """Create a new scenario in pending status.

    Validates structural constraints (non-empty name, n_steps bounds, step
    index bounds) and confirms all entity_ids exist in simulation_entities
    before writing. Returns 422 with a human-readable message on any failure.
    """
    _validate_create_request(req)
    await _validate_entities_exist(conn, req.configuration.entities)

    scenario_id = str(uuid.uuid4())
    config_json = req.configuration.model_dump(mode="json")

    async with conn.transaction():
        row = await conn.fetchrow(
            """
            INSERT INTO scenarios (scenario_id, name, description, status, configuration, version)
            VALUES ($1, $2, $3, 'pending', $4, 1)
            RETURNING scenario_id, name, description, status, version, created_at
            """,
            scenario_id,
            req.name,
            req.description,
            json.dumps(config_json),
        )

        for si in req.scheduled_inputs:
            await conn.execute(
                """
                INSERT INTO scenario_scheduled_inputs
                    (id, scenario_id, step, input_type, input_data)
                VALUES ($1, $2, $3, $4, $5)
                """,
                str(uuid.uuid4()),
                scenario_id,
                si.step,
                si.input_type,
                json.dumps(si.input_data),
            )

    return _row_to_response(dict(row))


# ---------------------------------------------------------------------------
# GET /scenarios
# ---------------------------------------------------------------------------


@router.get("/scenarios", response_model=list[ScenarioResponse])
async def list_scenarios(
    conn: Annotated[asyncpg.Connection, Depends(get_db)],
) -> list[ScenarioResponse]:
    """Return all scenarios ordered by created_at descending."""
    rows = await conn.fetch(
        """
        SELECT scenario_id, name, description, status, version, created_at
        FROM scenarios
        ORDER BY created_at DESC
        """
    )
    return [_row_to_response(dict(row)) for row in rows]


# ---------------------------------------------------------------------------
# GET /scenarios/compare — ADR-004 Decision 5
# ---------------------------------------------------------------------------


def _compute_delta(value_a: str, value_b: str, tier_a: int, tier_b: int) -> DeltaRecord:
    from decimal import Decimal  # noqa: PLC0415

    dec_a = Decimal(value_a)
    dec_b = Decimal(value_b)
    delta = dec_b - dec_a
    if delta > 0:
        direction = "increase"
    elif delta < 0:
        direction = "decrease"
    else:
        direction = "unchanged"
    return DeltaRecord(
        value_a=value_a,
        value_b=value_b,
        delta=str(delta),
        direction=direction,
        confidence_tier=max(tier_a, tier_b),
    )


@router.get("/scenarios/compare", response_model=CompareResponse)
async def compare_scenarios(
    conn: Annotated[asyncpg.Connection, Depends(get_db)],
    scenario_a: str,
    scenario_b: str,
    attr: str | None = None,
    step: int | None = None,
) -> CompareResponse:
    """Return attribute deltas between two scenarios.

    Computes delta = value_b - value_a for each shared entity and attribute.
    Only entities and attributes present in both snapshots are included.
    Filter to a single attribute with `attr`. ADR-004 Decision 5.

    `step` — when provided, both scenarios must have a snapshot at exactly
    that step. Returns 404 identifying which scenario is missing the step.
    When omitted, compares the final (highest-step) snapshot of each scenario.

    Returns 404 if either scenario is not found.
    Returns 404 if `step` is provided and either scenario has no snapshot at
    that step (with a message identifying the missing scenario).
    Returns 409 if `step` is omitted and either scenario has no snapshots yet.
    """
    for sid in (scenario_a, scenario_b):
        row = await conn.fetchrow(
            "SELECT scenario_id FROM scenarios WHERE scenario_id = $1", sid
        )
        if row is None:
            raise HTTPException(
                status_code=404, detail=f"Scenario '{sid}' not found."
            )

    if step is not None:
        snap_a = await conn.fetchrow(
            "SELECT step, state_data FROM scenario_state_snapshots "
            "WHERE scenario_id = $1 AND step = $2",
            scenario_a,
            step,
        )
        if snap_a is None:
            raise HTTPException(
                status_code=404,
                detail=(
                    f"Scenario '{scenario_a}' has no snapshot at step {step}. "
                    "Advance the scenario to this step before comparing."
                ),
            )
        snap_b = await conn.fetchrow(
            "SELECT step, state_data FROM scenario_state_snapshots "
            "WHERE scenario_id = $1 AND step = $2",
            scenario_b,
            step,
        )
        if snap_b is None:
            raise HTTPException(
                status_code=404,
                detail=(
                    f"Scenario '{scenario_b}' has no snapshot at step {step}. "
                    "Advance the scenario to this step before comparing."
                ),
            )
    else:
        snap_a = await conn.fetchrow(
            "SELECT step, state_data FROM scenario_state_snapshots "
            "WHERE scenario_id = $1 ORDER BY step DESC LIMIT 1",
            scenario_a,
        )
        snap_b = await conn.fetchrow(
            "SELECT step, state_data FROM scenario_state_snapshots "
            "WHERE scenario_id = $1 ORDER BY step DESC LIMIT 1",
            scenario_b,
        )
        if snap_a is None:
            raise HTTPException(
                status_code=409,
                detail=f"Scenario '{scenario_a}' has no snapshots. Run it first.",
            )
        if snap_b is None:
            raise HTTPException(
                status_code=409,
                detail=f"Scenario '{scenario_b}' has no snapshots. Run it first.",
            )

    state_a: dict[str, Any] = snap_a["state_data"]
    state_b: dict[str, Any] = snap_b["state_data"]
    if isinstance(state_a, str):
        state_a = json.loads(state_a)
    if isinstance(state_b, str):
        state_b = json.loads(state_b)

    shared_entities = set(state_a) & set(state_b)
    deltas: dict[str, dict[str, DeltaRecord]] = {}

    for eid in sorted(shared_entities):
        attrs_a: dict[str, Any] = state_a[eid]
        attrs_b: dict[str, Any] = state_b[eid]
        if not isinstance(attrs_a, dict) or not isinstance(attrs_b, dict):
            continue

        shared_attrs = set(attrs_a) & set(attrs_b)
        if attr is not None:
            shared_attrs = shared_attrs & {attr}

        entity_deltas: dict[str, DeltaRecord] = {}
        for key in sorted(shared_attrs):
            a_env = attrs_a[key]
            b_env = attrs_b[key]
            if not isinstance(a_env, dict) or not isinstance(b_env, dict):
                continue
            val_a = str(a_env.get("value", ""))
            val_b = str(b_env.get("value", ""))
            try:
                entity_deltas[key] = _compute_delta(
                    val_a,
                    val_b,
                    int(a_env.get("confidence_tier", 5)),
                    int(b_env.get("confidence_tier", 5)),
                )
            except Exception:  # noqa: BLE001 S112
                continue

        if entity_deltas:
            deltas[eid] = entity_deltas

    return CompareResponse(
        scenario_a_id=scenario_a,
        scenario_b_id=scenario_b,
        step_a=snap_a["step"],
        step_b=snap_b["step"],
        deltas=deltas,
    )


# ---------------------------------------------------------------------------
# GET /scenarios/{scenario_id}/trajectory — Issue #458
# ---------------------------------------------------------------------------

# Four frameworks output in stable order for the trajectory response.
_TRAJECTORY_FRAMEWORKS = ["financial", "human_development", "ecological", "governance"]

# Minimum confidence tier for the normalized_absolute strategy (CM-R3).
_NORMALIZED_ABSOLUTE_MIN_TIER = 3


async def _compute_trajectory_framework_point(
    entity_id: str,
    entity_indicators: dict[str, QuantitySchema],
    all_entity_attrs: dict[str, dict[str, QuantitySchema]],
    framework: str,
    is_single_entity: bool,
    db_connection: asyncpg.Connection,
    scenario_timestep: datetime | str,
) -> TrajectoryFrameworkPoint:
    """Compute one TrajectoryFrameworkPoint for an entity+framework at one step.

    Dispatch logic:
    - ecological: boundary_proximity strategy regardless of entity count.
    - governance: normalized_absolute strategy regardless of entity count
      (ADR-005 Amendment 4 — M10 promotion, Issue #556). WGI/V-Dem scores are
      country-level absolutes; percentile rank is not meaningful for a single entity.
    - financial / human_development (single-entity): normalized_absolute strategy,
      min confidence_tier = NORMALIZED_ABSOLUTE_MIN_TIER.
    - financial / human_development (multi-entity): percentile_rank strategy.
    """
    if framework == "ecological":
        context: dict[str, Any] = {
            "boundary_constants": await _fetch_active_boundary_constants(
                db_connection, scenario_timestep
            )
        }
        score = _boundary_proximity_strategy(
            entity_indicators, all_entity_attrs, framework, context
        )
        return TrajectoryFrameworkPoint(
            framework=framework,
            composite_score=str(score) if score is not None else None,
            scoring_basis="boundary_proximity",
            confidence_tier=2,
        )

    # governance — normalized_absolute regardless of entity count (ADR-005 Amendment 4).
    if framework == "governance":
        score = _normalized_absolute_strategy(
            entity_indicators, all_entity_attrs, framework, {}
        )
        indicator_min_tier = min(
            (
                qty.confidence_tier
                for qty in entity_indicators.values()
                if (qty.measurement_framework or "financial") == framework
            ),
            default=_NORMALIZED_ABSOLUTE_MIN_TIER,
        )
        tier = max(indicator_min_tier, _NORMALIZED_ABSOLUTE_MIN_TIER)
        return TrajectoryFrameworkPoint(
            framework=framework,
            composite_score=str(score) if score is not None else None,
            scoring_basis="normalized_absolute",
            confidence_tier=tier,
        )

    # financial or human_development
    if is_single_entity:
        score = _normalized_absolute_strategy(
            entity_indicators, all_entity_attrs, framework, {}
        )
        # Confidence tier is the max of Tier 3 floor and the best indicator tier.
        indicator_min_tier = min(
            (
                qty.confidence_tier
                for qty in entity_indicators.values()
                if (qty.measurement_framework or "financial") == framework
            ),
            default=_NORMALIZED_ABSOLUTE_MIN_TIER,
        )
        tier = max(indicator_min_tier, _NORMALIZED_ABSOLUTE_MIN_TIER)
        return TrajectoryFrameworkPoint(
            framework=framework,
            composite_score=str(score) if score is not None else None,
            scoring_basis="normalized_absolute",
            confidence_tier=tier,
        )

    # multi-entity percentile rank
    score = _percentile_rank_strategy(
        entity_indicators, all_entity_attrs, framework, {}
    )
    indicator_min_tier = min(
        (
            qty.confidence_tier
            for qty in entity_indicators.values()
            if (qty.measurement_framework or "financial") == framework
        ),
        default=5,
    )
    return TrajectoryFrameworkPoint(
        framework=framework,
        composite_score=str(score) if score is not None else None,
        scoring_basis="percentile_rank",
        confidence_tier=indicator_min_tier,
    )


@router.get(
    "/scenarios/{scenario_id}/trajectory",
    response_model=TrajectoryResponse,
)
async def get_trajectory(
    scenario_id: str,
    conn: Annotated[asyncpg.Connection, Depends(get_db)],
) -> TrajectoryResponse:
    """Multi-step trajectory for all four measurement frameworks.

    Returns computed steps as a dense array. Each step carries per-framework
    composite scores and optional policy inputs. mda_floors is at the response
    root (not per-step). In M9, mda_floors contains at most one entry:
    ecological WARNING at floor_value=1.0 when EcologicalModule is active.

    Composite score dispatch (Issue #458, CM consultation 2026-05-23; ADR-005 Amendment 4):
    - Single-entity: financial/HD use normalized_absolute; ecological uses
      boundary_proximity; governance uses normalized_absolute (WGI/V-Dem are country absolutes).
    - Multi-entity: financial/HD use percentile_rank; ecological uses
      boundary_proximity; governance uses normalized_absolute (entity count irrelevant).

    step_significance is sourced from scenarios.configuration->>'step_metadata'
    JSONB (ADR-010 Decision 7). Keys are 1-based step index strings. Absent key
    → ROUTINE. "STANDARD" is never emitted — only "SIGNIFICANT" or "ROUTINE".

    Returns 404 if scenario not found.
    Returns 409 if scenario has no snapshots yet (run it first).
    """
    scenario_row = await conn.fetchrow(
        "SELECT scenario_id, configuration FROM scenarios WHERE scenario_id = $1",
        scenario_id,
    )
    if scenario_row is None:
        raise HTTPException(
            status_code=404, detail=f"Scenario '{scenario_id}' not found."
        )

    cfg_raw = scenario_row["configuration"]
    if isinstance(cfg_raw, str):
        cfg_raw = json.loads(cfg_raw)
    entities: list[str] = cfg_raw.get("entities", [])
    entity_id = entities[0] if entities else ""

    # step_metadata keys are 1-based step index strings. Absent = ROUTINE.
    step_metadata: dict[str, Any] = cfg_raw.get("step_metadata", {}) or {}

    snapshot_rows = await conn.fetch(
        """
        SELECT step, timestep, state_data, events_snapshot
        FROM scenario_state_snapshots
        WHERE scenario_id = $1
        ORDER BY step ASC
        """,
        scenario_id,
    )
    if not snapshot_rows:
        raise HTTPException(
            status_code=409,
            detail=(
                f"Scenario '{scenario_id}' has no snapshots. Run it first."
            ),
        )

    policy_rows = await conn.fetch(
        "SELECT step, input_type, input_data FROM scenario_scheduled_inputs WHERE scenario_id = $1",
        scenario_id,
    )
    policy_by_step: dict[int, list[dict[str, Any]]] = {}
    for r in policy_rows:
        input_data = (
            r["input_data"]
            if isinstance(r["input_data"], dict)
            else json.loads(r["input_data"])
        )
        policy_by_step.setdefault(r["step"], []).append(
            {"input_type": r["input_type"], "input_data": input_data}
        )

    # Collect all state dicts for MDA floor detection and composite score dispatch.
    all_step_states: list[dict[str, Any]] = []
    for snap in snapshot_rows:
        state_raw = snap["state_data"]
        if isinstance(state_raw, str):
            state_raw = json.loads(state_raw)
        all_step_states.append(state_raw if isinstance(state_raw, dict) else {})

    # M9 MDA floor logic: ecological WARNING at 1.0 when EcologicalModule active.
    _ECOLOGICAL_PROXIMITY_KEYS = frozenset(
        {"planetary_boundary_co2_proximity", "planetary_boundary_land_use_proximity"}
    )
    is_ecological_active = any(
        any(k in _ECOLOGICAL_PROXIMITY_KEYS for k in state.get(entity_id, {}))
        for state in all_step_states
    )
    if is_ecological_active:
        mda_floors: list[MDAFloorRecord] = [
            MDAFloorRecord(
                framework="ecological",
                floor_value="1.0",
                severity="WARNING",
                label="Planetary boundary",
            )
        ]
    else:
        mda_floors = []

    steps: list[TrajectoryStep] = []
    for snap, state_dict in zip(snapshot_rows, all_step_states, strict=True):
        step_index: int = snap["step"]
        timestep = snap["timestep"]
        effective_from: str = (
            timestep.isoformat() if hasattr(timestep, "isoformat") else str(timestep)
        )

        # step_metadata uses 1-based string keys.
        step_meta: Any = step_metadata.get(str(step_index))
        if isinstance(step_meta, dict):
            raw_significance = step_meta.get("significance", "ROUTINE")
            raw_label: str | None = step_meta.get("label")
        elif step_meta is not None:
            raw_significance = str(step_meta)
            raw_label = None
        else:
            raw_significance = "ROUTINE"
            raw_label = None

        # Hard guarantee: never emit "STANDARD" — only "SIGNIFICANT" or "ROUTINE".
        if raw_significance == "SIGNIFICANT":
            step_significance = "SIGNIFICANT"
            # Truncate label to 32 chars if necessary (API contract).
            step_event_label: str | None = (raw_label or "")[:32] or None
        else:
            step_significance = "ROUTINE"
            step_event_label = None

        all_entity_attrs = _parse_entity_attrs(state_dict)
        entity_indicators_by_fw: dict[str, dict[str, QuantitySchema]] = {
            fw: {} for fw in _TRAJECTORY_FRAMEWORKS
        }
        target_attrs = all_entity_attrs.get(entity_id, {})
        for attr_key, qty in target_attrs.items():
            fw_tag = qty.measurement_framework or "financial"
            if fw_tag in entity_indicators_by_fw:
                entity_indicators_by_fw[fw_tag][attr_key] = qty

        is_single_entity = len(all_entity_attrs) == 1

        framework_points: list[TrajectoryFrameworkPoint] = []
        for fw in _TRAJECTORY_FRAMEWORKS:
            fw_indicators = entity_indicators_by_fw[fw]
            point = await _compute_trajectory_framework_point(
                entity_id=entity_id,
                entity_indicators=fw_indicators,
                all_entity_attrs=all_entity_attrs,
                framework=fw,
                is_single_entity=is_single_entity,
                db_connection=conn,
                scenario_timestep=timestep,
            )
            framework_points.append(point)

        steps.append(
            TrajectoryStep(
                step_index=step_index,
                effective_from=effective_from,
                step_event_label=step_event_label,
                step_significance=step_significance,
                frameworks=framework_points,
                policy_inputs=policy_by_step.get(step_index, []),
                shock_events=[],
            )
        )

    return TrajectoryResponse(
        scenario_id=scenario_id,
        entity_id=entity_id,
        step_count=len(steps),
        mda_floors=mda_floors,
        steps=steps,
    )


# ---------------------------------------------------------------------------
# GET /scenarios/{scenario_id}
# ---------------------------------------------------------------------------


@router.get("/scenarios/{scenario_id}", response_model=ScenarioDetailResponse)
async def get_scenario(
    scenario_id: str,
    conn: Annotated[asyncpg.Connection, Depends(get_db)],
) -> ScenarioDetailResponse:
    """Return full scenario detail including configuration and scheduled inputs."""
    row = await conn.fetchrow(
        """
        SELECT scenario_id, name, description, status, version, created_at, configuration
        FROM scenarios
        WHERE scenario_id = $1
        """,
        scenario_id,
    )
    if row is None:
        raise HTTPException(status_code=404, detail=f"Scenario '{scenario_id}' not found.")

    input_rows = await conn.fetch(
        """
        SELECT step, input_type, input_data
        FROM scenario_scheduled_inputs
        WHERE scenario_id = $1
        ORDER BY step, created_at
        """,
        scenario_id,
    )
    return _build_detail_response(dict(row), [dict(r) for r in input_rows])


# ---------------------------------------------------------------------------
# DELETE /scenarios/{scenario_id}
# ---------------------------------------------------------------------------


@router.delete("/scenarios/{scenario_id}", status_code=204)
async def delete_scenario(
    scenario_id: str,
    conn: Annotated[asyncpg.Connection, Depends(get_db)],
) -> Response:
    """Delete a scenario and all cascaded rows. Returns 204 No Content.

    Writes a tombstone to scenario_deleted_tombstones before the CASCADE
    executes. Tombstone and DELETE are in one transaction — atomic.
    ADR-004 Decision 1 Amendment (CONFLICT C-1 disposition).
    """
    async with conn.transaction():
        row = await conn.fetchrow(
            """
            SELECT scenario_id, name, configuration, created_at
            FROM scenarios
            WHERE scenario_id = $1
            """,
            scenario_id,
        )
        if row is None:
            raise HTTPException(
                status_code=404, detail=f"Scenario '{scenario_id}' not found."
            )

        cfg_raw = row["configuration"]
        if isinstance(cfg_raw, str):
            cfg_raw = json.loads(cfg_raw)

        input_rows = await conn.fetch(
            """
            SELECT step, input_type, input_data
            FROM scenario_scheduled_inputs
            WHERE scenario_id = $1
            ORDER BY step, created_at
            """,
            scenario_id,
        )
        scheduled_inputs_snap = [
            {
                "step": r["step"],
                "input_type": r["input_type"],
                "input_data": (
                    r["input_data"]
                    if isinstance(r["input_data"], dict)
                    else json.loads(r["input_data"])
                ),
            }
            for r in input_rows
        ]

        await conn.execute(
            """
            INSERT INTO scenario_deleted_tombstones
                (scenario_id, name, configuration, scheduled_inputs,
                 engine_version, git_commit_hash,
                 original_created_at, deleted_at, deleted_by)
            VALUES ($1, $2, $3, $4, $5, $6, $7, NOW(), $8)
            """,
            scenario_id,
            row["name"],
            json.dumps(cfg_raw),
            json.dumps(scheduled_inputs_snap),
            _ENGINE_VERSION,
            _GIT_COMMIT_HASH,
            row["created_at"],
            "api",
        )

        await conn.execute(
            "DELETE FROM scenarios WHERE scenario_id = $1",
            scenario_id,
        )

    return Response(status_code=204)


# ---------------------------------------------------------------------------
# POST /scenarios/{scenario_id}/run
# ---------------------------------------------------------------------------


@router.post("/scenarios/{scenario_id}/run", response_model=RunSummaryResponse)
async def run_scenario(
    scenario_id: str,
    conn: Annotated[asyncpg.Connection, Depends(get_db)],
) -> RunSummaryResponse:
    """Execute a pending scenario to completion.

    Validates that the scenario exists and is in 'pending' status.
    Returns 404 if not found, 409 if status is not pending.
    Delegates execution to WebScenarioRunner (ADR-004 Decision 2).
    Status transitions: pending → running → completed | failed.
    """
    status_row = await conn.fetchrow(
        "SELECT status FROM scenarios WHERE scenario_id = $1",
        scenario_id,
    )
    if status_row is None:
        raise HTTPException(
            status_code=404, detail=f"Scenario '{scenario_id}' not found."
        )
    if status_row["status"] != "pending":
        raise HTTPException(
            status_code=409,
            detail=(
                f"Scenario is in '{status_row['status']}' status. "
                "Only scenarios in 'pending' status can be run."
            ),
        )

    from app.simulation.web_scenario_runner import WebScenarioRunner  # noqa: PLC0415

    summary = await WebScenarioRunner().run(conn, scenario_id)
    return RunSummaryResponse(
        scenario_id=summary.scenario_id,
        steps_executed=summary.steps_executed,
        final_status=summary.final_status,
        duration_seconds=summary.duration_seconds,
    )


# ---------------------------------------------------------------------------
# POST /scenarios/{scenario_id}/advance — ADR-004 Decision 4
# ---------------------------------------------------------------------------


@router.post("/scenarios/{scenario_id}/advance", response_model=AdvanceResponse)
async def advance_scenario(
    scenario_id: str,
    conn: Annotated[asyncpg.Connection, Depends(get_db)],
) -> AdvanceResponse:
    """Advance a scenario by exactly one simulation step.

    Executes the next pending step, writes a snapshot, and returns the step
    index and remaining steps. Returns 404 if scenario not found, 409 if
    already completed. ADR-004 Decision 4 — step-by-step advance pattern.
    """
    status_row = await conn.fetchrow(
        "SELECT status FROM scenarios WHERE scenario_id = $1",
        scenario_id,
    )
    if status_row is None:
        raise HTTPException(
            status_code=404, detail=f"Scenario '{scenario_id}' not found."
        )
    if status_row["status"] == "completed":
        raise HTTPException(
            status_code=409,
            detail=f"Scenario '{scenario_id}' is already completed. Cannot advance further.",
        )

    from app.simulation.web_scenario_runner import WebScenarioRunner  # noqa: PLC0415

    summary = await WebScenarioRunner().run_single_step(conn, scenario_id)
    return AdvanceResponse(
        scenario_id=summary.scenario_id,
        step_executed=summary.step_executed,
        steps_remaining=summary.steps_remaining,
        final_status=summary.final_status,
        is_complete=summary.is_complete,
    )


# ---------------------------------------------------------------------------
# GET /scenarios/{scenario_id}/snapshots — ADR-004 Decision 3
# ---------------------------------------------------------------------------


@router.get("/scenarios/{scenario_id}/snapshots", response_model=list[SnapshotRecord])
async def list_snapshots(
    scenario_id: str,
    conn: Annotated[asyncpg.Connection, Depends(get_db)],
) -> list[SnapshotRecord]:
    """Return all snapshots for a scenario ordered by step ascending.

    Used by the backtesting test to evaluate fidelity thresholds against
    each simulated timestep's state_data. ADR-004 Decision 3.
    """
    scenario_row = await conn.fetchrow(
        "SELECT scenario_id FROM scenarios WHERE scenario_id = $1",
        scenario_id,
    )
    if scenario_row is None:
        raise HTTPException(
            status_code=404, detail=f"Scenario '{scenario_id}' not found."
        )

    rows = await conn.fetch(
        """
        SELECT scenario_id, step, timestep, state_data
        FROM scenario_state_snapshots
        WHERE scenario_id = $1
        ORDER BY step ASC
        """,
        scenario_id,
    )

    result = []
    for row in rows:
        state_raw = row["state_data"]
        if isinstance(state_raw, str):
            state_raw = json.loads(state_raw)
        state_dict: dict[str, Any] = state_raw if isinstance(state_raw, dict) else {}
        modules_active: list[str] = state_dict.get("_modules_active", [])
        if not isinstance(modules_active, list):
            modules_active = []
        timestep = row["timestep"]
        timestep_str = timestep.isoformat() if hasattr(timestep, "isoformat") else str(timestep)
        result.append(SnapshotRecord(
            scenario_id=row["scenario_id"],
            step=row["step"],
            timestep=timestep_str,
            state_data=state_dict,
            modules_active=modules_active,
        ))
    return result


# ---------------------------------------------------------------------------
# GET /scenarios/{scenario_id}/measurement-output — ADR-005 Decision 2
# ---------------------------------------------------------------------------

# Governance promoted to production in M10 per ADR-005 Amendment 4 (Issue #556).
_UNIMPLEMENTED_FRAMEWORKS: set[str] = set()
# ADR-005 Amendment 3 Decision M8-1 mandatory note template — must appear on every
# ecological FrameworkOutput. {n_indicators} is the count of active *_proximity
# indicators at query time. Non-compliance is an ADR violation.
_ECOLOGICAL_MANDATORY_NOTE_TEMPLATE = (
    "Ecological composite score: unweighted mean of {n_indicators} boundary "
    "proximity score(s) active at simulation time (formula: "
    "min(current_value / boundary_value, 2.0) for absolute-scale indicators; "
    "min(indicator_value, 2.0) for pre-normalized boundary-relative indicators). "
    "Score 1.0 = boundary exactly met; >1.0 = boundary exceeded; "
    "cap 2.0 = display ceiling only — entities with score 2.0 may be operating "
    "at any exceedance level ≥2× the safe boundary; simulation snapshots preserve "
    "uncapped values for analytical use. "
    "Composite range: [0.0, 2.0]. "
    "Equal weighting applied across contributing indicators — valid at current "
    "indicator count; must be re-evaluated when count exceeds five. "
    "Source: simulation_reference_constants table (effective-at-simulation-time)."
)
_ALL_FRAMEWORKS = ["financial", "human_development", "ecological", "governance"]
_SINGLE_ENTITY_NOTE = (
    "Composite score not meaningful in single-entity scenarios — "
    "percentile rank requires at least two entities for comparison."
)
# ADR-005 Amendment 3 Decision M8-2: ecological is exempt from is_single_entity guard
# because boundary proximity is physically meaningful for a single entity.
# Governance exempt per ADR-005 Amendment 4 — normalized_absolute is meaningful
# for single entities (WGI/V-Dem scores are country-level, not relative to peers).
_SINGLE_ENTITY_GUARD_EXEMPT_FRAMEWORKS: frozenset[str] = frozenset({"ecological", "governance"})
# ADR-005 Amendment 3 Decision M8-3: frameworks validated for percentile-rank composite.
# Governance is absent (M9 deferred — Decision M8-4). Unregistered frameworks fall
# through to percentile rank with a [SIM-INTEGRITY] WARNING.
_PERCENTILE_RANK_VALIDATED_FRAMEWORKS: frozenset[str] = frozenset(
    {"financial", "human_development"}
)
# Maps ecological proximity indicator keys → (boundary_constant_id, is_pre_normalized).
# Proximity indicators are produced by EcologicalModule and accumulated in entity.attributes.
# is_pre_normalized=True: formula is min(v, 2.0) — module already applied the boundary ratio.
_ECOLOGICAL_INDICATOR_BOUNDARY_CONFIG: dict[str, tuple[str, bool]] = {
    "planetary_boundary_co2_proximity": ("ECOLOGICAL_CO2_PLANETARY_BOUNDARY_PPM", True),
    "planetary_boundary_land_use_proximity": ("ECOLOGICAL_LAND_USE_PLANETARY_BOUNDARY_RATIO", True),
}


def _parse_entity_attrs(
    state_dict: dict[str, Any],
) -> dict[str, dict[str, QuantitySchema]]:
    """Extract and parse all entity attribute dicts from a state_data snapshot.

    Skips metadata keys (underscore-prefixed) and non-dict values.
    Returns entity_id → {attr_key → QuantitySchema}.
    """
    result: dict[str, dict[str, QuantitySchema]] = {}
    for key, val in state_dict.items():
        if key.startswith("_") or not isinstance(val, dict):
            continue
        parsed: dict[str, QuantitySchema] = {}
        for attr_key, envelope in val.items():
            if isinstance(envelope, dict):
                with contextlib.suppress(Exception):
                    parsed[attr_key] = QuantitySchema.from_jsonb(envelope)
        result[key] = parsed
    return result


# ---------------------------------------------------------------------------
# Composite score strategy dispatch — ADR-005 Amendment 3 Decision M8-3
# ---------------------------------------------------------------------------

# Callable signature: (entity_indicators, all_entity_attrs, framework, context) → Decimal | None
type CompositeStrategy = Callable[
    [dict[str, QuantitySchema], dict[str, dict[str, QuantitySchema]], str, dict[str, Any]],
    Decimal | None,
]


async def _fetch_active_boundary_constants(
    db_connection: asyncpg.Connection,
    scenario_timestep: datetime | str,
) -> dict[str, Decimal]:
    """Return active boundary constants at simulation time from simulation_reference_constants.

    Effective-at-simulation-time query per ADR-005 Amendment 3 Decision M8-6.
    Returns constant_id → Decimal value for constants active at scenario_timestep.
    """
    rows = await db_connection.fetch(
        """
        SELECT constant_id, value
        FROM simulation_reference_constants
        WHERE effective_from <= $1
          AND (effective_through IS NULL OR effective_through >= $1)
        """,
        scenario_timestep,
    )
    return {row["constant_id"]: Decimal(str(row["value"])) for row in rows}


def _percentile_rank_strategy(
    entity_indicators: dict[str, QuantitySchema],
    all_entity_attrs: dict[str, dict[str, QuantitySchema]],
    framework: str,
    context: dict[str, Any],
) -> Decimal | None:
    """Mean percentile rank across all entities for each framework indicator.

    ADR-005 Decision 2 §Composite score normalization. Returns [0.0, 1.0] Decimal
    or None when no numeric indicators are present.
    """
    if not entity_indicators:
        return None

    percentile_ranks: list[Decimal] = []
    for attr_key, target_qty in entity_indicators.items():
        try:
            target_val = Decimal(target_qty.value)
        except Exception:  # noqa: BLE001, S112
            continue

        all_vals: list[Decimal] = []
        for other_attrs in all_entity_attrs.values():
            qty = other_attrs.get(attr_key)
            if qty is not None and (qty.measurement_framework or "financial") == framework:
                with contextlib.suppress(Exception):
                    all_vals.append(Decimal(qty.value))

        if not all_vals:
            continue

        rank = Decimal(sum(1 for v in all_vals if v <= target_val)) / Decimal(len(all_vals))
        percentile_ranks.append(rank)

    if not percentile_ranks:
        return None

    score = sum(percentile_ranks) / Decimal(len(percentile_ranks))
    return score.quantize(Decimal("0.0001"))


def _boundary_proximity_strategy(
    entity_indicators: dict[str, QuantitySchema],
    all_entity_attrs: dict[str, dict[str, QuantitySchema]],
    framework: str,
    context: dict[str, Any],
) -> Decimal | None:
    """Unweighted mean of boundary proximity scores for ecological indicators.

    Reads context["boundary_constants"] (populated by _fetch_active_boundary_constants)
    to verify temporal validity. Indicators not in _ECOLOGICAL_INDICATOR_BOUNDARY_CONFIG
    are skipped. Missing or inactive boundary constants trigger [SIM-INTEGRITY] WARNING
    and exclude that indicator from the composite. ADR-005 Amendment 3 Decision M8-3.
    """
    boundary_constants: dict[str, Decimal] = context.get("boundary_constants", {})
    proximity_scores: list[Decimal] = []

    for indicator_key, qty in entity_indicators.items():
        config = _ECOLOGICAL_INDICATOR_BOUNDARY_CONFIG.get(indicator_key)
        if config is None:
            continue

        boundary_constant_id, is_pre_normalized = config

        if boundary_constant_id not in boundary_constants:
            _log.warning(
                "[SIM-INTEGRITY] Ecological boundary constant '%s' not active at simulation "
                "time — indicator '%s' excluded from composite score. Verify that migration "
                "c1a4e7f2d9b3 has run and simulation_reference_constants is seeded.",
                boundary_constant_id,
                indicator_key,
            )
            continue

        try:
            raw_val = Decimal(qty.value)
        except Exception:  # noqa: BLE001, S112
            continue

        if is_pre_normalized:
            score = min(raw_val, Decimal("2.0"))
        else:
            boundary_val = boundary_constants[boundary_constant_id]
            if boundary_val == Decimal("0"):
                _log.warning(
                    "[SIM-INTEGRITY] Boundary constant '%s' has zero value — "
                    "cannot compute proximity for '%s'. Skipping.",
                    boundary_constant_id,
                    indicator_key,
                )
                continue
            score = min(raw_val / boundary_val, Decimal("2.0"))

        proximity_scores.append(score)

    if not proximity_scores:
        return None

    composite = sum(proximity_scores) / Decimal(len(proximity_scores))
    return composite.quantize(Decimal("0.0001"))


# ---------------------------------------------------------------------------
# Normalized absolute strategy — Issue #458, CM consultation 2026-05-23
# ---------------------------------------------------------------------------

# Reference ranges for single-entity normalized_absolute composite score.
# health_expenditure_pct_gdp is EXCLUDED — methodologically non-monotonic (CM-R3).
# Indicators not in this dict are silently skipped (no normalizable value produced).
SINGLE_ENTITY_REFERENCE_RANGES: dict[str, dict[str, Any]] = {
    "gdp_growth": {
        "low": Decimal("-0.10"),
        "high": Decimal("0.06"),
        "direction": "higher_better",
    },
    "reserve_coverage_months": {
        "low": Decimal("0.0"),
        "high": Decimal("12.0"),
        "direction": "higher_better",
    },
    "unemployment_rate": {
        "low": Decimal("0.02"),
        "high": Decimal("0.30"),
        "direction": "lower_better",
    },
    "net_enrollment_secondary": {
        "low": Decimal("0.40"),
        "high": Decimal("1.00"),
        "direction": "higher_better",
    },
    # Governance indicators — ADR-005 Amendment 4 promotion (Issue #556).
    # rule_of_law_percentile: WGI percentile rank [0, 100]; higher = better governance.
    # Reference range covers the full WGI percentile span; normalization maps to [0, 1].
    "rule_of_law_percentile": {
        "low": Decimal("0"),
        "high": Decimal("100"),
        "direction": "higher_better",
    },
    # democratic_quality_score: V-Dem Liberal Democracy Index [0, 1]; higher = better.
    # Already in unit interval; reference range is the full LDI scale.
    "democratic_quality_score": {
        "low": Decimal("0"),
        "high": Decimal("1"),
        "direction": "higher_better",
    },
}


def _normalized_absolute_strategy(
    entity_indicators: dict[str, QuantitySchema],
    all_entity_attrs: dict[str, dict[str, QuantitySchema]],
    framework: str,
    context: dict[str, Any],
) -> Decimal | None:
    """Normalize each indicator against a declared reference range and average.

    Implements the Chief Methodologist reference-range consultation result
    (2026-05-23). Returns [0.0, 1.0] Decimal or None when no normalizable
    indicators are present. Confidence tier floor for the calling site is Tier 3.

    Only indicators in SINGLE_ENTITY_REFERENCE_RANGES tagged to `framework` are
    included. Indicators not in the reference table are skipped — the table is
    the authoritative set of normalizable indicators for this strategy.

    Clamping rule: scores below 0 are clamped to 0; scores above 1 are clamped
    to 1. A value below range is mapped to 0 (worst); above range to 1 (best).
    """
    scores: list[Decimal] = []
    for attr_key, qty in entity_indicators.items():
        if (qty.measurement_framework or "financial") != framework:
            continue
        spec = SINGLE_ENTITY_REFERENCE_RANGES.get(attr_key)
        if spec is None:
            continue
        try:
            v = Decimal(qty.value)
        except Exception:  # noqa: BLE001, S112
            continue
        low: Decimal = spec["low"]
        high: Decimal = spec["high"]
        denominator = high - low
        if denominator == Decimal("0"):
            continue
        if spec["direction"] == "higher_better":
            raw = (v - low) / denominator
        else:
            raw = (high - v) / denominator
        scores.append(max(Decimal("0"), min(Decimal("1"), raw)))

    if not scores:
        return None
    return (sum(scores) / Decimal(len(scores))).quantize(Decimal("0.0001"))


# Registered strategies keyed by framework string.
# Governance registered here per ADR-005 Amendment 4 — M10 promotion (Issue #556).
_COMPOSITE_STRATEGIES: dict[str, CompositeStrategy] = {
    "ecological": _boundary_proximity_strategy,
    "governance": _normalized_absolute_strategy,
}
_DEFAULT_COMPOSITE_STRATEGY: CompositeStrategy = _percentile_rank_strategy


async def _compute_composite_score(
    entity_indicators: dict[str, QuantitySchema],
    all_entity_attrs: dict[str, dict[str, QuantitySchema]],
    framework: str,
    db_connection: asyncpg.Connection,
    scenario_timestep: datetime | str,
) -> str | None:
    """Framework-dispatched composite score. Returns str(Decimal) or None.

    Three-branch dispatch per ADR-005 Amendment 3 Decision M8-3:
      1. Registered strategy (_COMPOSITE_STRATEGIES) — e.g. ecological boundary proximity
      2. Validated percentile-rank framework (_PERCENTILE_RANK_VALIDATED_FRAMEWORKS)
      3. Unknown framework — [SIM-INTEGRITY] WARNING, falls back to percentile rank
    """
    context: dict[str, Any] = {}

    if framework in _COMPOSITE_STRATEGIES:
        if framework == "ecological":
            context["boundary_constants"] = await _fetch_active_boundary_constants(
                db_connection, scenario_timestep
            )
        strategy = _COMPOSITE_STRATEGIES[framework]
    elif framework in _PERCENTILE_RANK_VALIDATED_FRAMEWORKS:
        strategy = _DEFAULT_COMPOSITE_STRATEGY
    else:
        _log.warning(
            "[SIM-INTEGRITY] Framework '%s' has no registered composite strategy "
            "and is not in _PERCENTILE_RANK_VALIDATED_FRAMEWORKS — "
            "falling back to percentile rank. Register a strategy or add to "
            "_PERCENTILE_RANK_VALIDATED_FRAMEWORKS.",
            framework,
        )
        strategy = _DEFAULT_COMPOSITE_STRATEGY

    result = strategy(entity_indicators, all_entity_attrs, framework, context)
    if result is None:
        return None
    return str(result)


def _alert_matches_framework(
    alert: MDAAlert,
    framework: str,
    target_attrs: dict[str, QuantitySchema],
) -> bool:
    """Return True if the alert's indicator belongs to the given framework.

    Looks up the indicator_key in target_attrs to find its measurement_framework
    tag. Untagged indicators fall into 'financial' per the backward-compatibility
    rule in CODING_STANDARDS.md §measurement_framework Tagging.
    """
    qty = target_attrs.get(alert.indicator_key)
    indicator_fw = (qty.measurement_framework or "financial") if qty is not None else "financial"
    return indicator_fw == framework


@router.get(
    "/scenarios/{scenario_id}/measurement-output",
    response_model=MultiFrameworkOutput,
)
async def get_measurement_output(
    scenario_id: str,
    entity_id: str,
    step: int,
    conn: Annotated[asyncpg.Connection, Depends(get_db)],
) -> MultiFrameworkOutput:
    """Multi-framework measurement output for one entity at a given step.

    Groups the entity's attributes by measurement_framework tag. Attributes
    with no tag are classified as FINANCIAL (M1–M3 backward-compatibility rule,
    CODING_STANDARDS.md §measurement_framework Tagging). Composite score dispatch
    is framework-specific: ecological uses boundary proximity normalization [0.0, 2.0]
    (ADR-005 Amendment 3 Decision M8-3); financial and human_development use mean
    percentile rank [0.0, 1.0]; governance uses normalized_absolute [0.0, 1.0] (ADR-005
    Amendment 4 — M10 promotion, Issue #556). Ecological and governance are exempt from the
    single-entity composite suppression guard (Decision M8-2, Amendment 4).
    ia1_disclosure is always IA1_CANONICAL_PHRASE. ADR-005 Decision 2, Amendment 3.

    Query params:
        step      — snapshot step index (required)
        entity_id — ISO 3166-1 alpha-3 entity identifier (required)
    """
    scenario_row = await conn.fetchrow(
        "SELECT scenario_id FROM scenarios WHERE scenario_id = $1",
        scenario_id,
    )
    if scenario_row is None:
        raise HTTPException(status_code=404, detail=f"Scenario '{scenario_id}' not found.")

    snap_row = await conn.fetchrow(
        """
        SELECT scenario_id, step, timestep, state_data, events_snapshot
        FROM scenario_state_snapshots
        WHERE scenario_id = $1 AND step = $2
        """,
        scenario_id,
        step,
    )
    if snap_row is None:
        raise HTTPException(
            status_code=404,
            detail=f"No snapshot at step {step} for scenario '{scenario_id}'.",
        )

    state_raw = snap_row["state_data"]
    if isinstance(state_raw, str):
        state_raw = json.loads(state_raw)
    state_dict: dict[str, Any] = state_raw if isinstance(state_raw, dict) else {}

    if entity_id not in state_dict:
        raise HTTPException(
            status_code=404,
            detail=f"Entity '{entity_id}' not found in snapshot at step {step}.",
        )

    entity_row = await conn.fetchrow(
        "SELECT metadata FROM simulation_entities WHERE entity_id = $1",
        entity_id,
    )
    metadata_str = entity_row["metadata"] if entity_row else None
    metadata_dict = json.loads(metadata_str) if metadata_str else {}
    entity_name: str = metadata_dict.get("name_en") or metadata_dict.get("name", entity_id)

    timestep = snap_row["timestep"]
    timestep_str: str = timestep.isoformat() if hasattr(timestep, "isoformat") else str(timestep)

    # Load MDA alerts from events_snapshot. Empty list for pre-M4 snapshots (events_snapshot=NULL).
    raw_events = snap_row["events_snapshot"]
    if raw_events is None:
        all_mda_alerts = []
    else:
        if isinstance(raw_events, str):
            raw_events = json.loads(raw_events)
        all_mda_alerts = alerts_from_events_snapshot(
            list(raw_events) if isinstance(raw_events, list) else [],
            entity_id=entity_id,
        )

    all_entity_attrs = _parse_entity_attrs(state_dict)
    target_attrs = all_entity_attrs.get(entity_id, {})
    is_single_entity = len(all_entity_attrs) == 1

    outputs: dict[str, FrameworkOutput] = {}
    for fw in _ALL_FRAMEWORKS:
        fw_alerts = [a for a in all_mda_alerts if _alert_matches_framework(a, fw, target_attrs)]
        has_below_floor = any(
            a.consecutive_breach_steps >= 1 for a in fw_alerts
        )

        indicators = {
            k: v.model_copy(update={"confidence_tier": effective_tier(v.confidence_tier, step)})
            for k, v in target_attrs.items()
            if (v.measurement_framework or "financial") == fw
        }
        # ADR-005 Amendment 3 Decision M8-2: ecological exempt from single-entity guard.
        if is_single_entity and fw not in _SINGLE_ENTITY_GUARD_EXEMPT_FRAMEWORKS:
            composite = None
        else:
            composite = await _compute_composite_score(
                indicators, all_entity_attrs, fw, conn, timestep
            )
        # ADR-005 Amendment 3 Decision M8-1: ecological note is mandatory regardless of
        # composite_score; {n_indicators} counts active *_proximity attributes.
        # ADR-005 Amendment 4: governance is also exempt — normalized_absolute is
        # meaningful for a single entity; the single-entity note must not be applied.
        if fw == "ecological":
            n_indicators = sum(1 for k in indicators if k.endswith("_proximity"))
            note: str | None = _ECOLOGICAL_MANDATORY_NOTE_TEMPLATE.format(
                n_indicators=n_indicators
            )
        elif is_single_entity and fw not in _SINGLE_ENTITY_GUARD_EXEMPT_FRAMEWORKS:
            note = _SINGLE_ENTITY_NOTE
        else:
            note = None
        outputs[fw] = FrameworkOutput(
            framework=fw,
            entity_id=entity_id,
            timestep=timestep_str,
            indicators=indicators,
            composite_score=composite,
            mda_alerts=fw_alerts,
            has_below_floor_indicator=has_below_floor,
            note=note,
        )

    return MultiFrameworkOutput(
        entity_id=entity_id,
        entity_name=entity_name,
        timestep=timestep_str,
        scenario_id=scenario_id,
        step_index=step,
        outputs=outputs,
        ia1_disclosure=IA1_CANONICAL_PHRASE,
        single_entity_warning=is_single_entity,
    )
