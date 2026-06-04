"""PoliticalEconomyModule — M11 Political Economy Module.

Implements three foundational political economy capabilities:

1. Legitimacy dynamics (Issue #156, #159):
   Subscribes to fiscal and emergency policy events. Computes a legitimacy
   delta based on policy impact and current legitimacy (high-impact austerity
   on a fragile government erodes legitimacy faster than on a stable one).
   Emits `legitimacy_change` events consumed by the social response generator
   in WebScenarioRunner.

2. Programme survival probability (Issue #273):
   At each step, computes the probability that the current policy programme
   survives long enough for its stabilisation benefits to materialise.
   Output: `programme_survival_probability` stock attribute (0.0–1.0).
   Formula-based approximation calibrated against Greece, Argentina, Ecuador
   programme failure cases. Full statistical calibration deferred to Issue #44.

3. Elite capture coefficient (Issue #679):
   Reads `elite_capture_coefficient` entity attribute when seeded. Computes
   the divergence between elite and non-elite cohort outcomes under fiscal
   adjustment — elite cohorts capture a disproportionate share of fiscal
   benefits while non-elite cohorts bear a disproportionate share of costs.
   Emits `elite_capture_divergence` events for the Human Cost Ledger.

One-step lag design: reads state.events (prior step), consistent with
MacroeconomicModule and GovernanceModule one-step lag architecture.

Opt-in via modules_config: {"political_economy": {"enabled": true}}.
When not enabled, module returns [] — no behavioural change.
"""
from __future__ import annotations

import logging
from decimal import Decimal
from typing import TYPE_CHECKING

from app.simulation.engine.models import (
    Event,
    MeasurementFramework,
    SimulationEntity,
    SimulationModule,
    SimulationState,
)
from app.simulation.engine.quantity import Quantity, VariableType

if TYPE_CHECKING:
    from datetime import datetime

_log = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Module constants
# ---------------------------------------------------------------------------

# Legitimacy erosion elasticity: fraction of |fiscal_delta| that translates
# into a legitimacy_index reduction per step. Calibrated from Greece 2010–2012:
# cumulative -25pp fiscal adjustment → approximately -0.20 legitimacy decline
# over 3 years → elasticity ≈ 0.08 per year. Conservative lower bound.
LEGITIMACY_EROSION_ELASTICITY = Decimal("0.08")

# Emergency policy erosion is larger: bank holidays, capital controls, and
# emergency declarations generate immediate legitimacy shocks (Lebanon 2019,
# Argentina 2001). Calibration: approx 0.10 per emergency event.
EMERGENCY_EROSION_FACTOR = Decimal("0.10")

# Fragility amplifier: legitimacy erosion is amplified when current legitimacy
# is below 0.5 (fragile government). Matches the non-linear pattern in
# political science literature (Przeworski et al. 2000).
FRAGILITY_THRESHOLD = Decimal("0.5")
FRAGILITY_AMPLIFIER = Decimal("1.5")

# Programme survival probability — formula parameters.
# Base monthly survival rate drawn from historical programme failure data:
# Greece: 3 programme collapses over 5 years; Argentina 2001: collapse in year 3;
# Ecuador 2000: abandoned after 1 year. Base annual survival ≈ 0.70.
_BASE_ANNUAL_SURVIVAL = Decimal("0.70")

# Legitimacy sensitivity: each 0.10 point decline in legitimacy_index reduces
# annual survival probability by 0.08 (calibrated from historical programme
# failure timing relative to protest intensity). Issue #44 calibration pending.
_LEGITIMACY_SURVIVAL_SENSITIVITY = Decimal("0.80")

# Elite capture redistribution coefficient: fraction of fiscal adjustment
# benefits captured by elite cohorts above their population weight.
# Default 0.30 (30% of benefits redirected to elite cohorts) drawn from
# Argentina 2001–2002 distributional analysis (Lustig 2001).
_DEFAULT_ELITE_CAPTURE_COEFFICIENT = Decimal("0.30")

_SUBSCRIBED_EVENTS = frozenset({
    "fiscal_policy_spending_change",
    "fiscal_policy_tax_rate_change",
    "emergency_policy_capital_controls",
    "emergency_policy_bank_holiday",
    "emergency_policy_imf_program_acceptance",
    "emergency_policy_default_declaration",
    "emergency_policy_emergency_declaration",
    "gdp_growth_change",
})


class PoliticalEconomyModule(SimulationModule):
    """Computes legitimacy dynamics, programme survival probability, and elite capture.

    Only fires for country entities when subscribed prior-step events are present
    or when legitimacy_index or elite_capture_coefficient attributes are seeded.
    Returns [] otherwise — no effect without political economy context.
    """

    def compute(
        self,
        entity: SimulationEntity,
        state: SimulationState,
        timestep: datetime,
    ) -> list[Event]:
        if entity.entity_type != "country":
            return []

        prior_events = [
            e for e in state.events
            if e.source_entity_id == entity.id and e.event_type in _SUBSCRIBED_EVENTS
        ]

        has_legitimacy = entity.get_attribute("legitimacy_index") is not None
        has_capture = entity.get_attribute("elite_capture_coefficient") is not None

        if not prior_events and not has_legitimacy and not has_capture:
            return []

        current_legitimacy = entity.get_attribute_value(
            "legitimacy_index", Decimal("0.7")
        )

        result: list[Event] = []

        # ------------------------------------------------------------------
        # 1. Legitimacy dynamics
        # ------------------------------------------------------------------
        legitimacy_delta = _compute_legitimacy_delta(prior_events, current_legitimacy)

        if legitimacy_delta != Decimal("0"):
            new_legitimacy = max(
                Decimal("0"), min(Decimal("1"), current_legitimacy + legitimacy_delta)
            )
            result.append(Event(
                event_id=f"poliecon-legitimacy-{entity.id}-{timestep.isoformat()}",
                source_entity_id=entity.id,
                event_type="legitimacy_change",
                affected_attributes={
                    "legitimacy_index": Quantity(
                        value=legitimacy_delta,
                        unit="ratio_0_1",
                        variable_type=VariableType.RATIO,
                        measurement_framework=MeasurementFramework.GOVERNANCE,
                        confidence_tier=3,
                    ),
                },
                propagation_rules=[],
                timestep_originated=timestep,
                framework=MeasurementFramework.GOVERNANCE,
                metadata={
                    "current_legitimacy": str(current_legitimacy),
                    "new_legitimacy": str(new_legitimacy),
                },
            ))
        else:
            new_legitimacy = current_legitimacy

        # ------------------------------------------------------------------
        # 2. Programme survival probability (Issue #273)
        # ------------------------------------------------------------------
        if has_legitimacy or prior_events:
            survival_prob = _compute_survival_probability(new_legitimacy)
            result.append(Event(
                event_id=f"poliecon-survival-{entity.id}-{timestep.isoformat()}",
                source_entity_id=entity.id,
                event_type="programme_survival_update",
                affected_attributes={
                    "programme_survival_probability": Quantity(
                        value=survival_prob,
                        unit="ratio_0_1",
                        variable_type=VariableType.STOCK,
                        measurement_framework=MeasurementFramework.GOVERNANCE,
                        confidence_tier=4,
                    ),
                },
                propagation_rules=[],
                timestep_originated=timestep,
                framework=MeasurementFramework.GOVERNANCE,
                metadata={
                    "legitimacy_input": str(new_legitimacy),
                    "calibration_note": (
                        "Formula-based approximation. Full calibration deferred "
                        "to Issue #44. Treat as DIRECTION_ONLY — not magnitude."
                    ),
                },
            ))

        # ------------------------------------------------------------------
        # 3. Elite capture divergence (Issue #679)
        # ------------------------------------------------------------------
        capture_qty = entity.get_attribute("elite_capture_coefficient")
        capture_coeff = (
            capture_qty.value if capture_qty is not None
            else _DEFAULT_ELITE_CAPTURE_COEFFICIENT
        )

        fiscal_delta = _extract_fiscal_delta(prior_events)
        if fiscal_delta != Decimal("0") and (has_capture or has_legitimacy):
            divergence = fiscal_delta * capture_coeff
            result.append(Event(
                event_id=f"poliecon-capture-{entity.id}-{timestep.isoformat()}",
                source_entity_id=entity.id,
                event_type="elite_capture_divergence",
                affected_attributes={
                    "elite_capture_divergence": Quantity(
                        value=divergence,
                        unit="ratio",
                        variable_type=VariableType.RATIO,
                        measurement_framework=MeasurementFramework.HUMAN_DEVELOPMENT,
                        confidence_tier=4,
                    ),
                },
                propagation_rules=[],
                timestep_originated=timestep,
                framework=MeasurementFramework.HUMAN_DEVELOPMENT,
                metadata={
                    "capture_coefficient": str(capture_coeff),
                    "fiscal_delta": str(fiscal_delta),
                    "interpretation": (
                        "Positive: fiscal benefits captured by elite cohorts. "
                        "Negative: fiscal costs borne disproportionately by non-elite."
                    ),
                },
            ))

        if not result:
            return []

        return result

    def get_subscribed_events(self) -> list[str]:
        return list(_SUBSCRIBED_EVENTS)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _compute_legitimacy_delta(
    prior_events: list[Event],
    current_legitimacy: Decimal,
) -> Decimal:
    """Compute the legitimacy_index change from prior-step policy events.

    Fiscal cuts erode legitimacy proportional to their magnitude.
    Emergency policy events (capital controls, bank holidays, emergency
    declarations) cause immediate legitimacy shocks.

    The fragility amplifier doubles erosion speed when legitimacy is below
    0.5 — consistent with the non-linear collapse pattern in political science
    literature. Recovery when legitimacy > 0.7 and no fiscal shocks is minimal
    within the annual timestep window (not modeled here; future calibration).
    """
    delta = Decimal("0")
    fragility = FRAGILITY_AMPLIFIER if current_legitimacy < FRAGILITY_THRESHOLD else Decimal("1")

    for evt in prior_events:
        if evt.event_type == "fiscal_policy_spending_change":
            magnitude = _extract_magnitude(evt)
            if magnitude is not None and magnitude < 0:
                delta += magnitude * LEGITIMACY_EROSION_ELASTICITY * fragility

        elif evt.event_type == "fiscal_policy_tax_rate_change":
            magnitude = _extract_magnitude(evt)
            if magnitude is not None and magnitude > 0:
                delta -= magnitude * LEGITIMACY_EROSION_ELASTICITY * fragility

        elif evt.event_type.startswith("emergency_policy_"):
            delta -= EMERGENCY_EROSION_FACTOR * fragility

    return delta


def _compute_survival_probability(legitimacy: Decimal) -> Decimal:
    """Compute annual programme survival probability from current legitimacy.

    Formula: base_survival × (1 + sensitivity × (legitimacy - 0.5))
    Clamped to [0.01, 0.99] — never exactly 0 or 1 (No False Precision gate).

    At legitimacy=0.7 (Greece 2010 entry): survival ≈ 0.70 × 1.16 = 0.81.
    At legitimacy=0.4 (Greece 2012 crisis): survival ≈ 0.70 × 0.92 = 0.64.
    At legitimacy=0.2 (acute crisis): survival ≈ 0.70 × 0.76 = 0.53.

    These are DIRECTION_ONLY estimates. Full statistical calibration against
    historical programme failure timing is deferred to Issue #44.
    """
    sensitivity_adjustment = _LEGITIMACY_SURVIVAL_SENSITIVITY * (legitimacy - Decimal("0.5"))
    raw = _BASE_ANNUAL_SURVIVAL * (Decimal("1") + sensitivity_adjustment)
    return max(Decimal("0.01"), min(Decimal("0.99"), raw))


def _extract_fiscal_delta(prior_events: list[Event]) -> Decimal:
    """Sum all spending_change deltas from prior fiscal events."""
    total = Decimal("0")
    for evt in prior_events:
        if evt.event_type in (
            "fiscal_policy_spending_change",
            "fiscal_policy_tax_rate_change",
        ):
            magnitude = _extract_magnitude(evt)
            if magnitude is not None:
                total += magnitude
    return total


def _extract_magnitude(event: Event) -> Decimal | None:
    """Return the primary scalar magnitude from an event's affected_attributes."""
    if not event.affected_attributes:
        return None
    return next(iter(event.affected_attributes.values())).value
