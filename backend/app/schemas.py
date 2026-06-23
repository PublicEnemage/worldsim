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

from pydantic import BaseModel, ConfigDict, Field, field_serializer, field_validator

# ---------------------------------------------------------------------------
# Output disclaimer constants — Issue #98, #100, #158
# ---------------------------------------------------------------------------

# Level 1 resolution disclaimer: static for all current scenarios.
# Subnational / community impacts are structurally invisible at nation-state
# aggregation. ARCH-REVIEW-002 BI2-N-09, ARCH-REVIEW-003 BI3-N-08.
RESOLUTION_DISCLAIMER_L1: str = (
    "Outputs represent national-level aggregates (Level 1 resolution). "
    "Subnational, community, and regional impacts are not representable "
    "at this resolution. Differential impact across regions, income cohorts, "
    "or demographic groups requires Level 2–4 resolution, which is not "
    "available in this scenario. "
    "See docs/scenarios/module-capability-registry.md for interpretation guidance."
)

RESOLUTION_LEVEL_CURRENT: int = 1


def build_temporal_scope_note(n_steps: int, timestep_label: str, start_date: object) -> str:
    """Generate temporal scope note from scenario config. Issue #98."""
    start_str = str(start_date) if start_date is not None else "the configured start date"
    return (
        f"This scenario models {n_steps} {timestep_label} timestep(s) from {start_str}. "
        "Consequences that compound over longer time horizons — including intergenerational "
        "capability losses, long-run debt sustainability, and ecological system responses — "
        "are outside the modeled window and are not represented in this output."
    )


# ---------------------------------------------------------------------------
# Trajectory endpoint schemas — Issue #458
# ---------------------------------------------------------------------------


class MDAFloorRecord(BaseModel):
    """One composite-score-level MDA floor line for the trajectory view Y-axis.

    floor_value is a Decimal serialised as string (float prohibition applies).
    In M9, at most one entry is produced: ecological WARNING at floor_value="1.0"
    when EcologicalModule is active. All other framework floors are deferred to M10.
    """

    model_config = ConfigDict(from_attributes=True)

    framework: str
    floor_value: str
    severity: str
    label: str

    @field_validator("floor_value", mode="before")
    @classmethod
    def _coerce(cls, v: object) -> str:
        if isinstance(v, int | float | Decimal):
            return str(Decimal(str(v)))
        return str(v)


class TrajectoryFrameworkPoint(BaseModel):
    """Per-framework composite score for one trajectory step.

    ci_lower, ci_upper, ci_coverage, and is_pre_calibration are always null
    pending ADR-007. composite_score is Decimal-as-string or null.
    scoring_basis disambiguates null sources:
      - "normalized_absolute" — single-entity financial/HD; null when no normalizable indicators
      - "percentile_rank"     — multi-entity financial/HD, or governance (always null)
      - "boundary_proximity"  — ecological only
    """

    model_config = ConfigDict(from_attributes=True)

    framework: str
    composite_score: str | None
    scoring_basis: str
    confidence_tier: int
    ci_lower: None = None
    ci_upper: None = None
    ci_coverage: None = None
    is_pre_calibration: None = None


class PMMRecord(BaseModel):
    """Per-step Policy Maneuver Margin — Zone 1C (ADR-008 Decision 6, Issue #496).

    value in [0, 1]: 0.0 = at or below an MDA floor; 1.0 = outside all approach zones.
    direction: "up" | "down" | "flat" relative to the previous step.
    Both fields are present when any 'all'-scoped MDA threshold has a matching
    indicator in entity state. Null when no thresholds can be evaluated.
    """

    model_config = ConfigDict(from_attributes=True)

    value: str
    direction: str

    @field_validator("value", mode="before")
    @classmethod
    def _coerce(cls, v: object) -> str:
        if isinstance(v, int | float | Decimal):
            return str(Decimal(str(v)))
        return str(v)


class TrajectoryStep(BaseModel):
    """One computed step in the trajectory response.

    step_significance is ALWAYS "SIGNIFICANT" or "ROUTINE" — never "STANDARD".
    step_event_label is null when step_significance is ROUTINE.
    policy_inputs lists ControlInput events applied at this step.
    shock_events is empty for M9.
    pmm is null when no 'all'-scoped MDA thresholds have indicator data for this step.
    """

    model_config = ConfigDict(from_attributes=True)

    step_index: int
    effective_from: str
    step_event_label: str | None
    step_significance: str
    frameworks: list[TrajectoryFrameworkPoint]
    policy_inputs: list[dict[str, Any]]
    shock_events: list[dict[str, Any]] = []
    pmm: PMMRecord | None = None


class TrajectoryResponse(BaseModel):
    """Full trajectory for all four measurement frameworks across all computed steps.

    mda_floors is at the response root, not per-step (ADR-010 Decision 2).
    entity_id is the first entity in scenario configuration.entities.
    steps is a dense array of computed steps only.
    Each step carries pmm (Policy Maneuver Margin) derived from MDA thresholds (Issue #496).
    """

    model_config = ConfigDict(from_attributes=True)

    scenario_id: str
    entity_id: str
    step_count: int
    mda_floors: list[MDAFloorRecord]
    steps: list[TrajectoryStep]


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
    attribute_type: str | None = None
    stock_flow_identity: bool = False
    reversibility: str | None = None

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
            attribute_type=data.get("attribute_type"),
            stock_flow_identity=bool(data.get("stock_flow_identity", False)),
            reversibility=data.get("reversibility"),
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


class PoliticalContext(BaseModel):
    """Initial political environment for a scenario (Issue #156).

    Encodes the political conditions that govern implementation feasibility.
    When present, WebScenarioRunner reads legitimacy_index to compute a
    political_feasibility_modifier that scales ControlInput magnitudes —
    a government with 40% approval implementing 8% GDP cuts transmits
    less of the intended policy than one with 70% approval.

    All fields are optional for backward compatibility. When absent, no
    political feasibility modifier is applied and behaviour is identical
    to pre-M11 runs.

    Sources for Greece 2010 values: Eurobarometer 73 (Spring 2010) for
    government_approval_rating; ELSTAT/Kathimerini for coalition_seat_margin;
    IDEA electoral calendar for months_to_next_election; CIVICUS Civil
    Society Index for civil_society_organization_strength.
    """

    government_approval_rating: Decimal | None = None     # 0.0–1.0
    coalition_seat_margin: int | None = None              # legislative majority margin
    months_to_next_election: int | None = None
    civil_society_organization_strength: Decimal | None = None  # 0.0–1.0
    legitimacy_index: Decimal | None = None               # composite 0.0–1.0


class CommodityShockConfig(BaseModel):
    """A global commodity price shock applied to all scenario entities (Issue #752, ADR-012).

    Effects are distributed proportionally to each entity's
    `commodity_import_dependency_{commodity_category}` attribute value.
    Entities with no dependency attribute receive zero shock.

    All synthetic dependency coefficients must be flagged at indicator level
    as Tier 3 per DATA_STANDARDS.md §Confidence Tier System.
    """

    model_config = ConfigDict(from_attributes=True)

    commodity_category: str
    magnitude: Decimal
    start_step: int = 0
    duration_steps: int = 1

    @field_serializer("magnitude")
    def _serialize_magnitude(self, v: Decimal) -> str:
        return str(v)


class ScenarioConfigSchema(BaseModel):
    """Scenario configuration payload.

    `entities` — list of entity_ids in scope for this scenario run.
    `initial_attributes` — optional per-entity attribute overrides at step 0.
    `n_steps` — number of simulation timesteps to execute (1–100).
    `timestep_label` — human-readable timestep unit label.
    `start_date` — optional calendar start date for step 0 (ISO 8601, e.g.
        "2010-01-01"). When absent the runner defaults to 2000-01-01. Supply
        this for historical backtesting scenarios so displayed step dates match
        the historical period.
    `step_metadata` — optional per-step annotation dict keyed by 1-based step
        index string. Each value is a dict with `significance` ("SIGNIFICANT" |
        "ROUTINE") and optional `label` (str, max 32 chars). Absent keys default
        to ROUTINE. Consumed by the trajectory endpoint for step_significance and
        step_event_label fields (ADR-010 Decision 7).
    `political_context` — optional initial political environment (Issue #156).
        When present, legitimacy_index scales ControlInput implementation
        capacity and social response events are generated for high-impact
        ControlInputs when social_response_enabled is set in modules_config.
    `n_runs` — number of Monte Carlo runs (Issue #89). Default 1 (deterministic).
        Values > 1 signal distributional output; the schema accepts the field so
        MC support can be added without a breaking schema change. MC sampling
        itself is not yet implemented — n_runs > 1 is recorded but produces
        a single deterministic trajectory until ADR-007 MC support ships.
    `fiscal_multiplier` — Mode 2 parameter (Issue #746). Scales the regime-dependent
        fiscal multiplier applied in MacroeconomicModule. Default 1.0 (no scaling).
        Range 0.1–3.0; values outside this range are rejected at validation.
    `commodity_price_shocks` — global commodity shocks distributed to all entities by
        import dependency (Issue #752, ADR-012). Default empty (no shocks).
    `projection_steps` — optional long-run projection horizon (1–100, M16-G3 #274).
        When set, overrides n_steps as the total step count. projection_steps > 8
        enables the 25-year human capital depletion trajectory (quarterly timestep,
        DemographicModule auto-enabled, adaptive_resolution disabled).
        Default None → programme-length behaviour (n_steps governs).
    """

    model_config = ConfigDict(from_attributes=True)

    entities: list[str]
    initial_attributes: dict[str, dict[str, QuantitySchema]] = {}
    n_steps: int
    timestep_label: str = "annual"
    modules_config: dict[str, Any] = {}
    start_date: date | None = None
    step_metadata: dict[str, Any] = {}
    political_context: PoliticalContext | None = None
    n_runs: int = 1
    fiscal_multiplier: float = Field(default=1.0, ge=0.1, le=3.0)
    commodity_price_shocks: list[CommodityShockConfig] = []
    projection_steps: int | None = Field(default=None, ge=1, le=100)


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


class ScenarioRestoreRequest(BaseModel):
    """Request body for POST /scenarios/restore (Issue #155)."""

    model_config = ConfigDict(from_attributes=True)

    tombstone_id: str


class ScenarioRestoreResponse(BaseModel):
    """Response from POST /scenarios/restore."""

    model_config = ConfigDict(from_attributes=True)

    scenario_id: str
    name: str
    status: str
    restored_from_tombstone_id: str


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
    """Full scenario record including configuration and scheduled inputs.

    `temporal_scope_note` is generated from scenario configuration and surfaces
    the intergenerational / long-horizon limitation per ARCH-REVIEW-002 BI2-N-07
    (Issue #98). Computed at response time — not stored in the database.
    """

    model_config = ConfigDict(from_attributes=True)

    scenario_id: str
    name: str
    description: str | None
    status: str
    version: int
    created_at: str
    configuration: ScenarioConfigSchema
    scheduled_inputs: list[ScheduledInputSchema]
    temporal_scope_note: str
    engine_version_hash: str | None = None


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

    `resolution_disclaimer` surfaces the Level 1 resolution limitation per
    ARCH-REVIEW-002 BI2-N-09 (Issue #100, #158). Static for all current scenarios.
    """

    model_config = ConfigDict(from_attributes=True)

    scenario_id: str
    step: int
    timestep: str
    state_data: dict[str, Any]
    modules_active: list[str] = []
    resolution_disclaimer: str = RESOLUTION_DISCLAIMER_L1


class AdvanceResponse(BaseModel):
    """Response from POST /scenarios/{id}/advance — ADR-004 Decision 4.

    `resolution_level` and `resolution_disclaimer` surface the Level 1
    resolution limitation per ARCH-REVIEW-002 BI2-N-09 and ARCH-REVIEW-003
    BI3-N-08 (Issue #158). Static for all current scenarios.
    """

    model_config = ConfigDict(from_attributes=True)

    scenario_id: str
    step_executed: int
    steps_remaining: int
    final_status: str
    is_complete: bool
    resolution_level: int = RESOLUTION_LEVEL_CURRENT
    resolution_disclaimer: str = RESOLUTION_DISCLAIMER_L1


# ---------------------------------------------------------------------------
# Comparative scenario schemas — ADR-004 Decision 5
# ---------------------------------------------------------------------------


class DeltaRecord(BaseModel):
    """Delta between the same attribute across two scenario snapshots.

    `delta` = str(Decimal(value_b) - Decimal(value_a)).
    `direction` is 'increase', 'decrease', or 'unchanged'.
    `confidence_tier` is max(tier_a, tier_b) — lower-of-two rule.
    `threshold_crossed` is True when the delta crosses a caller-supplied absolute
    threshold (i.e. value_a is on one side and value_b is on the other), None when
    no threshold was requested (Issue #153, G6a rider).
    """

    model_config = ConfigDict(from_attributes=True)

    value_a: str
    value_b: str
    delta: str
    direction: str
    confidence_tier: int
    threshold_crossed: bool | None = None


class CompareResponse(BaseModel):
    """Comparative output across two scenario final snapshots — ADR-004 Decision 5.

    `deltas` maps entity_id → attribute_key → DeltaRecord.
    Only entities and attributes present in both snapshots are included.
    When `attr` is omitted, ALL shared attributes across all shared entities are
    returned in a single call (Issue #90). Pass `attr` to filter to one key.
    """

    model_config = ConfigDict(from_attributes=True)

    scenario_a_id: str
    scenario_b_id: str
    step_a: int
    step_b: int
    deltas: dict[str, dict[str, DeltaRecord]]


# ---------------------------------------------------------------------------
# Trajectory comparison schemas — Issue #99
# ---------------------------------------------------------------------------


class TrajectoryCompareStep(BaseModel):
    """One aligned step in a trajectory comparison.

    `value_a` and `value_b` are the attribute values (Decimal as string) at
    this step for scenario_a and scenario_b respectively. `delta` = value_b -
    value_a as a Decimal string. `direction` is 'increase', 'decrease', or
    'unchanged'. All fields are None when the attribute is absent in either
    snapshot at this step.
    """

    model_config = ConfigDict(from_attributes=True)

    step: int
    value_a: str | None = None
    value_b: str | None = None
    delta: str | None = None
    direction: str | None = None


class TrajectoryCompareResponse(BaseModel):
    """Per-step attribute trajectory delta between two scenarios — Issue #99.

    `steps` contains one entry per shared step (both scenarios have a snapshot),
    sorted ascending by step number. Only steps where both scenarios have a
    snapshot AND the attribute is present in at least one entity are included.
    `attribute` is the attribute key that was queried.
    """

    model_config = ConfigDict(from_attributes=True)

    scenario_a_id: str
    scenario_b_id: str
    attribute: str
    steps: list[TrajectoryCompareStep]


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
    comparison_operator: str = "lte"
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

    indicator_name is always populated — title-case of indicator_key.
    Frontend display-name registries may override this with more precise labels.

    recovery_horizon_years: None means the threshold models an irreversible
    transition; an integer means recovery is possible within that many years
    given appropriate intervention. Source: mda_thresholds.recovery_horizon_years.
    Rider #271 — reversibility classification.
    """

    model_config = ConfigDict(from_attributes=True)

    mda_id: str
    entity_id: str
    indicator_key: str
    indicator_name: str
    severity: MDASeverity
    floor_value: str
    current_value: str
    approach_pct_remaining: str
    consecutive_breach_steps: int
    recovery_horizon_years: int | None = None


class FrameworkOutput(BaseModel):
    """One measurement framework's indicators and composite score for an entity.

    composite_score is a Decimal-as-string or None. Range and computation are
    framework-dependent: [0.0, 1.0] percentile rank for financial and human_development;
    [0.0, 2.0] boundary proximity for ecological (1.0 = at boundary, cap 2.0 for display).
    None for governance (deferred to M9) and for financial/human_development in
    single-entity scenarios (percentile rank is meaningless with a population of one).
    Ecological is exempt from the single-entity suppression — boundary proximity is
    physically meaningful for a single entity. note is always populated for ecological.
    ADR-005 Decision 2, Amendment 3 Decisions M8-1/M8-2/M8-3. Issue #193.
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
        from app.simulation.repositories.quantity_serde import (
            validate_ia1_disclosure,  # noqa: PLC0415
        )
        return validate_ia1_disclosure(v)


# ---------------------------------------------------------------------------
# Mode 3 branch schemas — G6b (Issue #753)
# ---------------------------------------------------------------------------


class BranchRequest(BaseModel):
    """Request body for POST /scenarios/{id}/branch.

    Creates a new branch scenario from an existing baseline at a specific step,
    with an updated fiscal_multiplier. The baseline's snapshots up to
    branch_from_step are copied to the branch; the branch then advances forward.
    """

    fiscal_multiplier: float = Field(
        default=1.0,
        ge=0.1,
        le=3.0,
        description="New fiscal multiplier for the branch scenario.",
    )
    branch_from_step: int = Field(
        ge=0,
        description="Step from which to branch. A snapshot must exist at this step.",
    )


class BranchResponse(BaseModel):
    """Response for POST /scenarios/{id}/branch."""

    branch_scenario_id: str
    branch_from_step: int
    n_steps: int


class RebranchRequest(BaseModel):
    """Request body for POST /scenarios/{id}/rebranch.

    Applies a new parameter change to an existing branch scenario. Deletes
    snapshots from from_step onward so the branch can re-run from that step
    with an updated fiscal_multiplier. Implements the re-branch accumulation
    model from mode3-interaction-spec.md §5.
    """

    fiscal_multiplier: float = Field(
        default=1.0,
        ge=0.1,
        le=3.0,
        description="Updated fiscal multiplier for the re-branch.",
    )
    from_step: int = Field(
        ge=0,
        description=(
            "Step from which to restart recompute."
            " Snapshots from this step forward are deleted."
        ),
    )
