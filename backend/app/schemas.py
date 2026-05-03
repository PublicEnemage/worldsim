"""Pydantic response schemas — ADR-003 Decision 2.

All monetary / simulation values carry `value` as `str` (Decimal serialized
as string). Pydantic v2 serializes Decimal to float by default; this module
overrides that explicitly. A float on the wire is an architectural regression
against the DATA_STANDARDS.md float prohibition.
"""
from __future__ import annotations

from datetime import date
from decimal import Decimal
from enum import Enum
from typing import Any

from pydantic import BaseModel, ConfigDict, field_serializer, field_validator


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
    modules_config: dict[str, Any] = {}


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
    """One step snapshot from scenario_state_snapshots — ADR-004 Decision 3.

    `modules_active` lists the domain modules that contributed to this snapshot.
    Empty list for all M3 snapshots (no domain modules implemented). Populated
    in M4+ from the `_modules_active` key in state_data. See Issue #145, #146.
    """

    model_config = ConfigDict(from_attributes=True)

    scenario_id: str
    step: int
    timestep: str
    state_data: dict[str, Any]
    modules_active: list[str] = []


class AdvanceResponse(BaseModel):
    """Response from POST /scenarios/{id}/advance — ADR-004 Decision 4."""

    model_config = ConfigDict(from_attributes=True)

    scenario_id: str
    step_executed: int
    steps_remaining: int
    final_status: str
    is_complete: bool


# ---------------------------------------------------------------------------
# Comparative scenario schemas — ADR-004 Decision 5
# ---------------------------------------------------------------------------


class DeltaRecord(BaseModel):
    """Delta between the same attribute across two scenario snapshots.

    `delta` = str(Decimal(value_b) - Decimal(value_a)).
    `direction` is 'increase', 'decrease', or 'unchanged'.
    `confidence_tier` is max(tier_a, tier_b) — lower-of-two rule.
    """

    model_config = ConfigDict(from_attributes=True)

    value_a: str
    value_b: str
    delta: str
    direction: str
    confidence_tier: int


class CompareResponse(BaseModel):
    """Comparative output across two scenario final snapshots — ADR-004 Decision 5.

    `deltas` maps entity_id → attribute_key → DeltaRecord.
    Only entities and attributes present in both snapshots are included.
    """

    model_config = ConfigDict(from_attributes=True)

    scenario_a_id: str
    scenario_b_id: str
    step_a: int
    step_b: int
    deltas: dict[str, dict[str, DeltaRecord]]


# ---------------------------------------------------------------------------
# Human Cost Ledger schemas — ADR-005 Decisions 2 and 3
# ---------------------------------------------------------------------------


class MDASeverity(str, Enum):
    """Minimum Descent Altitude alert severity — ADR-005 Decision 3."""

    WARNING = "WARNING"
    CRITICAL = "CRITICAL"
    TERMINAL = "TERMINAL"


class MDAThresholdRecord(BaseModel):
    """One row from the mda_thresholds table — ADR-005 Decision 3.

    floor_value and approach_pct are NUMERIC in the database; they are
    serialized as str here to maintain the float prohibition (ADR-003 Decision 2).
    The field_validator coerces Decimal/float DB values to str on construction.
    """

    model_config = ConfigDict(from_attributes=True)

    mda_id: str
    indicator_key: str
    entity_scope: str
    measurement_framework: str
    floor_value: str
    floor_unit: str
    approach_pct: str
    severity_at_breach: str
    description: str
    historical_basis: str
    recovery_horizon_years: int | None = None
    irreversibility_note: str

    @field_validator("floor_value", "approach_pct", mode="before")
    @classmethod
    def _coerce_numeric(cls, v: object) -> str:
        if isinstance(v, int | float | Decimal):
            return str(Decimal(str(v)))
        return str(v)


class MDAAlert(BaseModel):
    """A single MDA threshold breach or approach — ADR-005 Decision 3.

    floor_value, current_value, and approach_pct_remaining are strings
    (Decimal serialized as str) — consistent with the float prohibition
    throughout the API layer (ADR-003 Decision 2).
    """

    model_config = ConfigDict(from_attributes=True)

    mda_id: str
    entity_id: str
    indicator_key: str
    severity: MDASeverity
    floor_value: str
    current_value: str
    approach_pct_remaining: str
    consecutive_breach_steps: int


class FrameworkOutput(BaseModel):
    """One measurement framework's indicators and composite score for an entity.

    composite_score is a Decimal-as-string (0.0–1.0 percentile rank) or None
    when the module producing this framework's indicators is not yet implemented,
    or when the scenario has only one entity (percentile rank is meaningless with
    a population of one). note is populated when composite_score is None.
    mda_alerts is empty pending ADR-005 Decision 3 (MDAChecker) implementation.
    ADR-005 Decision 2. Issue #193.
    """

    model_config = ConfigDict(from_attributes=True)

    framework: str
    entity_id: str
    timestep: str
    indicators: dict[str, QuantitySchema]
    composite_score: str | None
    mda_alerts: list[MDAAlert]
    has_below_floor_indicator: bool
    note: str | None


class MultiFrameworkOutput(BaseModel):
    """Multi-framework measurement output for one entity at one step.

    All four MeasurementFramework values are present in outputs; unimplemented
    frameworks carry composite_score=None and a note field. ia1_disclosure is
    required with no default — validated non-empty by validate_ia1_disclosure.
    single_entity_warning is True when the snapshot contains exactly one entity —
    composite_score is null in that case because percentile rank requires at least
    two entities for comparison. ADR-005 Decision 2. Issue #193.
    """

    model_config = ConfigDict(from_attributes=True)

    entity_id: str
    entity_name: str
    timestep: str
    scenario_id: str
    step_index: int
    outputs: dict[str, FrameworkOutput]
    ia1_disclosure: str
    single_entity_warning: bool = False

    @field_validator("ia1_disclosure")
    @classmethod
    def _check_ia1_disclosure(cls, v: str) -> str:
        from app.simulation.repositories.quantity_serde import validate_ia1_disclosure
        return validate_ia1_disclosure(v)
