"""Pydantic response schemas — ADR-003 Decision 2.

All monetary / simulation values carry `value` as `str` (Decimal serialized
as string). Pydantic v2 serializes Decimal to float by default; this module
overrides that explicitly. A float on the wire is an architectural regression
against the DATA_STANDARDS.md float prohibition.
"""
from __future__ import annotations

from datetime import date
from decimal import Decimal
from typing import Any

from pydantic import BaseModel, ConfigDict, field_serializer


class QuantitySchema(BaseModel):
    """Serialized form of a Quantity value stored in the JSONB attribute store.

    `value` is always a string — the Decimal representation without IEEE 754
    rounding. Consumers that need a numeric value for visualization (e.g.,
    MapLibre color scale) must parse this string explicitly at the rendering
    boundary.
    """

    model_config = ConfigDict(from_attributes=True)

    value: str
    unit: str
    variable_type: str
    confidence_tier: int
    observation_date: date | None = None
    source_registry_id: str | None = None
    measurement_framework: str | None = None

    @field_serializer("observation_date")
    def _serialize_date(self, v: date | None) -> str | None:
        return v.isoformat() if v is not None else None

    @classmethod
    def from_jsonb(cls, data: dict[str, Any]) -> QuantitySchema:
        """Build a QuantitySchema from a JSONB attribute envelope dict.

        Handles the observation_date field being stored as an ISO string
        in the JSONB column.
        """
        obs = data.get("observation_date")
        if isinstance(obs, str) and obs:
            try:
                obs_date: date | None = date.fromisoformat(obs)
            except ValueError:
                obs_date = None
        elif isinstance(obs, date):
            obs_date = obs
        else:
            obs_date = None

        value = data.get("value", "")
        if isinstance(value, int | float | Decimal):
            value = str(Decimal(str(value)))

        return cls(
            value=str(value),
            unit=str(data.get("unit", "")),
            variable_type=str(data.get("variable_type", "")),
            confidence_tier=int(data.get("confidence_tier", 5)),
            observation_date=obs_date,
            source_registry_id=data.get("source_registry_id"),
            measurement_framework=data.get("measurement_framework"),
        )


class CountrySummary(BaseModel):
    """Lightweight country summary — list endpoint, no geometry or attributes."""

    model_config = ConfigDict(from_attributes=True)

    entity_id: str
    entity_type: str
    name: str
    iso_a2: str
    iso_a3: str


class CountryDetail(BaseModel):
    """Full country record with attributes — single entity endpoint."""

    model_config = ConfigDict(from_attributes=True)

    entity_id: str
    entity_type: str
    name: str
    iso_a2: str
    iso_a3: str
    metadata: dict[str, Any]
    attributes: dict[str, QuantitySchema]


class GeoJSONFeature(BaseModel):
    """GeoJSON Feature — single entity geometry endpoint."""

    model_config = ConfigDict(from_attributes=True)

    type: str = "Feature"
    geometry: dict[str, Any]
    properties: dict[str, Any]


class GeoJSONFeatureCollection(BaseModel):
    """GeoJSON FeatureCollection — choropleth endpoint."""

    model_config = ConfigDict(from_attributes=True)

    type: str = "FeatureCollection"
    features: list[GeoJSONFeature]


class AttributeSummary(BaseModel):
    """One available attribute key with its unit and variable_type."""

    model_config = ConfigDict(from_attributes=True)

    attribute_key: str
    unit: str
    variable_type: str


class HealthResponse(BaseModel):
    """Health check response."""

    status: str
    version: str
    db: str


# ---------------------------------------------------------------------------
# Scenario schemas — ADR-004 Decision 1
# ---------------------------------------------------------------------------


class ScenarioConfigSchema(BaseModel):
    """Scenario configuration payload.

    `entities` — list of entity_ids in scope for this scenario run.
    `initial_attributes` — optional per-entity attribute overrides at step 0.
    `n_steps` — number of simulation timesteps to execute (1–100).
    `timestep_label` — human-readable timestep unit label.
    """

    model_config = ConfigDict(from_attributes=True)

    entities: list[str]
    initial_attributes: dict[str, dict[str, QuantitySchema]] = {}
    n_steps: int
    timestep_label: str = "annual"


class ScheduledInputSchema(BaseModel):
    """A ControlInput record bound to a specific simulation step."""

    model_config = ConfigDict(from_attributes=True)

    step: int
    input_type: str
    input_data: dict[str, Any]


class ScenarioCreateRequest(BaseModel):
    """Request body for POST /scenarios."""

    model_config = ConfigDict(from_attributes=True)

    name: str
    description: str | None = None
    configuration: ScenarioConfigSchema
    scheduled_inputs: list[ScheduledInputSchema] = []


class ScenarioResponse(BaseModel):
    """Scenario summary — list and create responses."""

    model_config = ConfigDict(from_attributes=True)

    scenario_id: str
    name: str
    description: str | None
    status: str
    version: int
    created_at: str


class ScenarioDetailResponse(BaseModel):
    """Full scenario record including configuration and scheduled inputs."""

    model_config = ConfigDict(from_attributes=True)

    scenario_id: str
    name: str
    description: str | None
    status: str
    version: int
    created_at: str
    configuration: ScenarioConfigSchema
    scheduled_inputs: list[ScheduledInputSchema]


class RunSummaryResponse(BaseModel):
    """Response from POST /scenarios/{id}/run — ADR-004 Decision 2."""

    model_config = ConfigDict(from_attributes=True)

    scenario_id: str
    steps_executed: int
    final_status: str
    duration_seconds: float


class SnapshotRecord(BaseModel):
    """One step snapshot from scenario_state_snapshots — ADR-004 Decision 3."""

    model_config = ConfigDict(from_attributes=True)

    scenario_id: str
    step: int
    timestep: str
    state_data: dict[str, Any]
