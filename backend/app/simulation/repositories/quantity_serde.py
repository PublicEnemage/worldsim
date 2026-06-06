"""Quantity ↔ JSONB envelope serialization — SA-09 Quantity JSONB Envelope Format.

SA-09 defines the canonical wire format for all Quantity values stored in JSONB
columns (simulation_entities.attributes, scenario.configuration.initial_attributes,
scenario_state_snapshots.state_data).

All reads go through QuantitySchema.from_jsonb() then quantity_from_schema().
All writes go through quantity_to_jsonb_envelope().

SA-12 round-trip requirement: Quantity → quantity_to_jsonb_envelope() →
QuantitySchema.from_jsonb() → quantity_from_schema() → Quantity must be lossless
for all fields: value (Decimal precision), unit, variable_type (enum), confidence_tier
(int), observation_date (date | None, not string), source_id, measurement_framework.

IA1_CANONICAL_PHRASE is the exact text required in every ia1_disclosure field on
scenario_state_snapshots. Unit tests must assert this phrase appears verbatim.

STATE_DATA_ENVELOPE_VERSION tracks the schema version of the scenario_state_snapshots
state_data JSONB top-level envelope (distinct from the per-Quantity _envelope_version).
Increment this constant when M4+ modules add structural fields to state_data that
change interpretation of snapshot contents. Version "2" adds _modules_active.
"""
from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING, Any

from app.schemas import QuantitySchema
from app.simulation.engine.quantity import AttributeType, Quantity, VariableType

if TYPE_CHECKING:
    from app.simulation.engine.models import CohortProfile, MeasurementFramework

# ---------------------------------------------------------------------------
# IA-1 canonical text — SA-01
# ---------------------------------------------------------------------------

IA1_CANONICAL_PHRASE: str = (
    "This simulation produces distributions using pre-calibration uncertainty "
    "bands. Intervals shown are NOT confidence intervals derived from calibrated "
    "parameter distributions — they are conservative defaults that widen with "
    "projection horizon and data quality. Bands will be revised when "
    "MAGNITUDE_WITHIN_20PCT validation exists for at least two independent "
    "historical cases. All outputs should be interpreted as structured reasoning "
    "tools, not predictions. Verify against current data before consequential "
    "use. "
    "Horizon degradation schedule: confidence_tier degrades by +1 for every "
    "5 projection steps beyond the baseline, capped at Tier 5. The "
    "_steps_projected field in each snapshot state_data envelope records the "
    "projection distance used when computing effective_tier at the output layer."
)


def validate_ia1_disclosure(text: str) -> str:
    """Validate that an ia1_disclosure string is non-empty and non-whitespace.

    Raises ValueError if text is empty or whitespace-only. Returns text
    unchanged on success. Call at every snapshot write path — the NOT NULL DB
    constraint prevents NULL but cannot reject an empty or placeholder string.
    See ARCH-REVIEW-003 BI3-I-01 and Issue #144.
    """
    if not text or not text.strip():
        raise ValueError(
            "ia1_disclosure must be a non-empty, non-whitespace string. "
            "Use IA1_CANONICAL_PHRASE or a substantive disclosure text. "
            "See DATA_STANDARDS.md Known Limitation IA-1."
        )
    return text


# ---------------------------------------------------------------------------
# SA-09 per-Quantity envelope format
# ---------------------------------------------------------------------------

_ENVELOPE_VERSION = "1"

# ---------------------------------------------------------------------------
# State-data envelope version — scenario_state_snapshots.state_data top level
# ---------------------------------------------------------------------------

# "2" adds _modules_active list to the top-level state_data envelope.
# "3" adds _steps_projected int to record projection horizon at write time
#     (Issue #151 — horizon degradation; resolves ADR-001 Amendment 1 IA-1).
# Increment when M4+ modules add structural fields that change snapshot
# interpretation. See ARCH-REVIEW-003 BI3-I-02 and Issue #145.
STATE_DATA_ENVELOPE_VERSION = "3"


def quantity_to_jsonb_envelope(q: Quantity) -> dict[str, Any]:
    """Convert a Quantity to a SA-09 JSONB envelope dict.

    _envelope_version is always written. value is str(Decimal) — float prohibition
    preserved. observation_date is ISO-8601 string or None. All enum fields are
    their .value strings.
    """
    from app.simulation.engine.models import MeasurementFramework  # noqa: PLC0415

    envelope: dict[str, Any] = {
        "_envelope_version": _ENVELOPE_VERSION,
        "value": str(q.value),
        "unit": q.unit,
        "variable_type": q.variable_type.value,
        "confidence_tier": q.confidence_tier,
        "observation_date": (
            q.observation_date.isoformat() if q.observation_date is not None else None
        ),
        "source_registry_id": q.source_id,
        "measurement_framework": (
            q.measurement_framework.value
            if isinstance(q.measurement_framework, MeasurementFramework)
            else None
        ),
    }
    if q.attribute_type is not None:
        envelope["attribute_type"] = q.attribute_type.value
    if q.stock_flow_identity:
        envelope["stock_flow_identity"] = True
    return envelope


def quantity_from_schema(schema: QuantitySchema) -> Quantity:
    """Convert a QuantitySchema (Pydantic) back to a Quantity engine object.

    SA-12: this is the return path of the round-trip. All field types must be
    restored exactly — Decimal not float, date not string, enum not string.
    """
    from app.simulation.engine.models import MeasurementFramework  # noqa: PLC0415

    mf: MeasurementFramework | None = None
    if schema.measurement_framework is not None:
        try:
            mf = MeasurementFramework(schema.measurement_framework)
        except ValueError:
            mf = None

    try:
        vt = VariableType(schema.variable_type)
    except ValueError:
        vt = VariableType.DIMENSIONLESS

    at: AttributeType | None = None
    if schema.attribute_type is not None:
        try:
            at = AttributeType(schema.attribute_type)
        except ValueError:
            at = None

    return Quantity(
        value=Decimal(schema.value),
        unit=schema.unit,
        variable_type=vt,
        confidence_tier=int(schema.confidence_tier),
        observation_date=schema.observation_date,
        source_id=schema.source_registry_id,
        measurement_framework=mf,
        attribute_type=at,
        stock_flow_identity=schema.stock_flow_identity,
    )


def quantity_from_jsonb(data: dict[str, Any]) -> Quantity:
    """Deserialize a JSONB envelope dict to a Quantity in one step.

    Convenience wrapper: QuantitySchema.from_jsonb() → quantity_from_schema().
    """
    return quantity_from_schema(QuantitySchema.from_jsonb(data))


# ---------------------------------------------------------------------------
# CohortProfile serde — ADR-001 Amendment 2, Issue #28
# ---------------------------------------------------------------------------


def cohort_profile_to_jsonb(profile: CohortProfile) -> dict[str, Any]:
    """Serialize a CohortProfile to a JSONB-safe dict.

    Each attribute in the profile is serialized with quantity_to_jsonb_envelope.
    The result is stored as the value of the "_cohort_profiles" sub-key within
    an entity's state_data block.

    Args:
        profile: A CohortProfile instance.

    Returns:
        Dict mapping attribute_key → SA-09 Quantity envelope.
    """
    return {
        attr_key: quantity_to_jsonb_envelope(qty)
        for attr_key, qty in profile.attributes.items()
    }


def cohort_profile_from_jsonb(data: dict[str, Any]) -> CohortProfile:
    """Deserialize a JSONB dict to a CohortProfile.

    Inverse of cohort_profile_to_jsonb. Unknown or malformed envelope keys
    are silently skipped (same defensive pattern as _reconstruct_state_from_snapshot).

    Args:
        data: Dict mapping attribute_key → SA-09 Quantity envelope.

    Returns:
        CohortProfile with deserialized attributes.
    """
    import contextlib  # noqa: PLC0415

    from app.simulation.engine.models import CohortProfile  # noqa: PLC0415

    attributes: dict[str, Quantity] = {}
    for attr_key, envelope in data.items():
        if isinstance(envelope, dict):
            with contextlib.suppress(ValueError, KeyError):
                attributes[attr_key] = quantity_from_jsonb(envelope)
    return CohortProfile(attributes=attributes)
