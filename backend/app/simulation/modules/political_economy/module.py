"""PoliticalEconomyModule — M13 ADR-013.

Implements four political economy capabilities (ADR-013 Decisions 1–4):

1. Programme survival probability (Decision 1):
   Promoted from internal model variable to named indicator in the
   political_economy measurement framework. Fires PE-001 CRITICAL MDA
   alert when `programme_survival_probability` falls below
   PROGRAMME_SURVIVAL_FLOOR = 0.25. Confidence tier: 3.

2. Conditionality per-term risk attribution (Decision 2):
   Reads CONDITIONALITY-sourced event metadata (injected by
   ControlInput.get_events — ADR-013) and emits named indicators per term:
   `conditionality_term_{constraining_actor_id}_{constraint_mechanism}`.
   Only fires for scenarios with CONDITIONALITY events in state.events.

3. Elite capture divergence index (Decision 3):
   Promotes the M11 `elite_capture_divergence` event to three named
   indicators in the political_economy framework:
   - `elite_capture_divergence_index` (ratio ≥ 1.0)
   - `elite_capture_divergence_top_quintile` (benefit capture share [0,1])
   - `elite_capture_divergence_bottom_quintile` (cost burden share [0,1])

4. Political economy composite score (Decision 4):
   Arithmetic mean of three normalised inputs. Available in trajectory
   and measurement output APIs. NOT in Zone 1D (deferred to follow-on ADR).

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
# annual survival probability by ~0.105 at base survival 0.70 (calibrated so
# that legitimacy=0.0 produces survival below PROGRAMME_SURVIVAL_FLOOR=0.25,
# consistent with AC-3 of the intent document). Issue #44 full calibration pending.
_LEGITIMACY_SURVIVAL_SENSITIVITY = Decimal("1.50")

# ADR-013 Decision 1: MDA floor for programme viability.
# When programme_survival_probability < PROGRAMME_SURVIVAL_FLOOR, MDAChecker
# fires PE-001-programme-survival-critical. Must not change without ADR amendment.
PROGRAMME_SURVIVAL_FLOOR = Decimal("0.25")

# Elite capture redistribution coefficient: fraction of fiscal adjustment
# benefits captured by elite cohorts above their population weight.
# Default 0.30 (30% of benefits to top quintile) drawn from
# Argentina 2001–2002 distributional analysis (Lustig 2001).
_DEFAULT_ELITE_CAPTURE_COEFFICIENT = Decimal("0.30")

# Population share of top income quintile (structural assumption).
_ELITE_POPULATION_SHARE = Decimal("0.20")

# Population share of bottom two income quintiles.
_BOTTOM_TWO_QUINTILE_SHARE = Decimal("0.40")

# Non-elite population share (for cost-burden computation).
_NON_ELITE_SHARE = Decimal("0.80")

# ADR-013 Decision 4: composite score normalisation ceiling for elite capture index.
MAX_ELITE_CAPTURE = Decimal("5.0")

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
    """Computes political economy indicators per ADR-013.

    Promotes programme_survival_probability, conditionality attribution,
    and elite capture to named indicators in the political_economy framework.
    Returns [] when no political economy context is present.
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

        # Conditionality events targeting this entity from prior step.
        conditionality_events = [
            e for e in state.events
            if e.source_entity_id == entity.id
            and e.metadata.get("input_source") == "conditionality"
            and e.metadata.get("constraining_actor_id")
        ]

        if (
            not prior_events and not has_legitimacy
            and not has_capture and not conditionality_events
        ):
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
        # 2. Programme survival probability (ADR-013 Decision 1)
        # ------------------------------------------------------------------
        if has_legitimacy or prior_events:
            survival_prob = _compute_survival_probability(new_legitimacy)
            psp_dominant_driver = _attribute_dominant_driver(prior_events, new_legitimacy)
            result.append(Event(
                event_id=f"poliecon-survival-{entity.id}-{timestep.isoformat()}",
                source_entity_id=entity.id,
                event_type="programme_survival_update",
                affected_attributes={
                    "programme_survival_probability": Quantity(
                        value=survival_prob,
                        unit="ratio_0_1",
                        variable_type=VariableType.PROBABILITY,
                        measurement_framework=MeasurementFramework.POLITICAL_ECONOMY,
                        confidence_tier=3,
                    ),
                },
                propagation_rules=[],
                timestep_originated=timestep,
                framework=MeasurementFramework.POLITICAL_ECONOMY,
                metadata={
                    "legitimacy_input": str(new_legitimacy),
                    "programme_survival_floor": str(PROGRAMME_SURVIVAL_FLOOR),
                    "calibration_note": (
                        "Formula-calibrated estimate (Tier 3). Calibrated on Greece, "
                        "Argentina, Ecuador programme failure cases. Not a prediction."
                    ),
                    "psp_dominant_driver": psp_dominant_driver,
                },
            ))

        # ------------------------------------------------------------------
        # 3. Conditionality per-term attribution (ADR-013 Decision 2)
        # ------------------------------------------------------------------
        if conditionality_events:
            term_deltas = _aggregate_conditionality_terms(conditionality_events)
            for (actor_id, mechanism), effective_delta in term_deltas.items():
                indicator_key = f"conditionality_term_{actor_id}_{mechanism}"
                result.append(Event(
                    event_id=(
                        f"poliecon-cond-{entity.id}-{actor_id}-{mechanism}"
                        f"-{timestep.isoformat()}"
                    ),
                    source_entity_id=entity.id,
                    event_type="conditionality_term_attribution",
                    affected_attributes={
                        indicator_key: Quantity(
                            value=abs(effective_delta),
                            unit="pct_gdp",
                            variable_type=VariableType.STOCK,
                            measurement_framework=MeasurementFramework.POLITICAL_ECONOMY,
                            confidence_tier=3,
                        ),
                    },
                    propagation_rules=[],
                    timestep_originated=timestep,
                    framework=MeasurementFramework.POLITICAL_ECONOMY,
                    metadata={
                        "constraining_actor_id": actor_id,
                        "constraint_mechanism": mechanism,
                        "effective_delta": str(effective_delta),
                    },
                ))

        # ------------------------------------------------------------------
        # 4. Elite capture divergence index (ADR-013 Decision 3)
        # ------------------------------------------------------------------
        capture_qty = entity.get_attribute("elite_capture_coefficient")
        capture_coeff = (
            capture_qty.value if capture_qty is not None
            else _DEFAULT_ELITE_CAPTURE_COEFFICIENT
        )

        fiscal_delta = _extract_fiscal_delta(prior_events)
        if fiscal_delta != Decimal("0") and (has_capture or has_legitimacy):
            elite_index, top_quintile_share, bottom_quintile_share = (
                _compute_elite_capture_indicators(capture_coeff)
            )
            result.append(Event(
                event_id=f"poliecon-capture-{entity.id}-{timestep.isoformat()}",
                source_entity_id=entity.id,
                event_type="elite_capture_update",
                affected_attributes={
                    "elite_capture_divergence_index": Quantity(
                        value=elite_index,
                        unit="ratio",
                        variable_type=VariableType.STOCK,
                        measurement_framework=MeasurementFramework.POLITICAL_ECONOMY,
                        confidence_tier=3,
                    ),
                    "elite_capture_divergence_top_quintile": Quantity(
                        value=top_quintile_share,
                        unit="ratio_0_1",
                        variable_type=VariableType.STOCK,
                        measurement_framework=MeasurementFramework.POLITICAL_ECONOMY,
                        confidence_tier=3,
                    ),
                    "elite_capture_divergence_bottom_quintile": Quantity(
                        value=bottom_quintile_share,
                        unit="ratio_0_1",
                        variable_type=VariableType.STOCK,
                        measurement_framework=MeasurementFramework.POLITICAL_ECONOMY,
                        confidence_tier=3,
                    ),
                },
                propagation_rules=[],
                timestep_originated=timestep,
                framework=MeasurementFramework.POLITICAL_ECONOMY,
                metadata={
                    "capture_coefficient": str(capture_coeff),
                    "fiscal_delta": str(fiscal_delta),
                    "elite_population_share": str(_ELITE_POPULATION_SHARE),
                },
            ))

        # ------------------------------------------------------------------
        # 5. Political economy composite score (ADR-013 Decision 4)
        # ------------------------------------------------------------------
        if has_legitimacy or prior_events:
            survival_prob_val = _compute_survival_probability(new_legitimacy)
            capture_coeff_for_composite = (
                capture_qty.value if capture_qty is not None
                else _DEFAULT_ELITE_CAPTURE_COEFFICIENT
            )
            elite_index_for_composite, _, _ = _compute_elite_capture_indicators(
                capture_coeff_for_composite
            )
            composite = _compute_composite_score(
                survival_prob_val, elite_index_for_composite, new_legitimacy
            )
            result.append(Event(
                event_id=f"poliecon-composite-{entity.id}-{timestep.isoformat()}",
                source_entity_id=entity.id,
                event_type="political_economy_composite_update",
                affected_attributes={
                    "political_economy_composite_score": Quantity(
                        value=composite,
                        unit="ratio_0_1",
                        variable_type=VariableType.STOCK,
                        measurement_framework=MeasurementFramework.POLITICAL_ECONOMY,
                        confidence_tier=3,
                    ),
                },
                propagation_rules=[],
                timestep_originated=timestep,
                framework=MeasurementFramework.POLITICAL_ECONOMY,
                metadata={
                    "composite_inputs": {
                        "programme_survival": str(survival_prob_val),
                        "elite_capture_index": str(elite_index_for_composite),
                        "legitimacy": str(new_legitimacy),
                    },
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
    """Compute the legitimacy_index change from prior-step policy events."""
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


def _attribute_dominant_driver(
    prior_events: list[Event],
    current_legitimacy: Decimal,
) -> str | None:
    """Return the dominant driver category of PSP change at this step."""
    fragility = FRAGILITY_AMPLIFIER if current_legitimacy < FRAGILITY_THRESHOLD else Decimal("1")
    contributions: dict[str, Decimal] = {
        "governance": Decimal("0"),
        "fiscal_sustainability": Decimal("0"),
        "external_balance": Decimal("0"),
    }
    for evt in prior_events:
        if evt.event_type == "fiscal_policy_spending_change":
            magnitude = _extract_magnitude(evt)
            if magnitude is not None and magnitude < 0:
                elast = LEGITIMACY_EROSION_ELASTICITY
                contributions["fiscal_sustainability"] += abs(magnitude) * elast * fragility
        elif evt.event_type == "fiscal_policy_tax_rate_change":
            magnitude = _extract_magnitude(evt)
            if magnitude is not None and magnitude > 0:
                elast = LEGITIMACY_EROSION_ELASTICITY
                contributions["fiscal_sustainability"] += magnitude * elast * fragility
        elif evt.event_type.startswith("emergency_policy_"):
            contributions["governance"] += EMERGENCY_EROSION_FACTOR * fragility
        elif evt.event_type == "gdp_growth_change":
            magnitude = _extract_magnitude(evt)
            if magnitude is not None:
                contributions["external_balance"] += abs(magnitude) * LEGITIMACY_EROSION_ELASTICITY
    total = sum(contributions.values())
    if total == Decimal("0"):
        if current_legitimacy < FRAGILITY_THRESHOLD:
            return "social_stability"
        return None
    priority = ["governance", "fiscal_sustainability", "external_balance"]
    return max(priority, key=lambda cat: (contributions[cat], -priority.index(cat)))


def _compute_survival_probability(legitimacy: Decimal) -> Decimal:
    """Compute annual programme survival probability from current legitimacy.

    Formula: base_survival × (1 + sensitivity × (legitimacy - 0.5))
    Clamped to [0.01, 0.99] — never exactly 0 or 1 (No False Precision gate).

    At legitimacy=0.7 (Greece 2010 entry): survival ≈ 0.70 × 1.30 = 0.91.
    At legitimacy=0.4 (Greece 2012 crisis): survival ≈ 0.70 × 0.85 = 0.60.
    At legitimacy=0.2 (acute crisis): survival ≈ 0.70 × 0.55 = 0.39.
    At legitimacy=0.0 (programme collapse territory): survival ≈ 0.70 × 0.25 = 0.175.

    Sensitivity=1.50 ensures legitimacy=0.0 yields survival < PROGRAMME_SURVIVAL_FLOOR (0.25),
    satisfying AC-3 of the intent document (PE-001 MDA alert reachable via formula).
    Full statistical calibration deferred to Issue #44.
    """
    sensitivity_adjustment = _LEGITIMACY_SURVIVAL_SENSITIVITY * (legitimacy - Decimal("0.5"))
    raw = _BASE_ANNUAL_SURVIVAL * (Decimal("1") + sensitivity_adjustment)
    return max(Decimal("0.01"), min(Decimal("0.99"), raw))


def _compute_elite_capture_indicators(
    capture_coeff: Decimal,
) -> tuple[Decimal, Decimal, Decimal]:
    """Compute elite capture divergence index and cohort sub-indicators.

    Args:
        capture_coeff: Fraction of total fiscal benefits captured by top quintile.
                       The constraint capture_coeff ≥ _ELITE_POPULATION_SHARE ensures
                       index ≥ 1.0 (a value below 1.0 is not possible per ADR-013 Decision 3).

    Returns:
        (elite_capture_divergence_index, top_quintile_share, bottom_quintile_share)
        - elite_capture_divergence_index: top_quintile_capture / top_quintile_population
        - top_quintile_share: capture_coeff (benefit fraction going to top quintile)
        - bottom_quintile_share: cost burden fraction for bottom two quintiles
    """
    bounded_coeff = max(_ELITE_POPULATION_SHARE, min(Decimal("1.0"), capture_coeff))

    elite_index = bounded_coeff / _ELITE_POPULATION_SHARE

    top_quintile_share = bounded_coeff

    non_elite_cost = Decimal("1") - bounded_coeff
    bottom_quintile_share = non_elite_cost * (_BOTTOM_TWO_QUINTILE_SHARE / _NON_ELITE_SHARE)

    return elite_index, top_quintile_share, bottom_quintile_share


def _compute_composite_score(
    survival_prob: Decimal,
    elite_index: Decimal,
    legitimacy: Decimal,
) -> Decimal:
    """Compute political economy composite score (ADR-013 Decision 4).

    Arithmetic mean of three normalised inputs:
    1. programme_survival_probability (already in [0.0, 1.0])
    2. 1 - elite_capture_divergence_index / MAX_ELITE_CAPTURE (clamped to [0.0, 1.0])
    3. legitimacy_index (or 0.5 neutral if absent)

    Higher score = more stable political economy.
    Clamped to [0.0, 1.0].
    """
    elite_normalised = max(
        Decimal("0"),
        min(Decimal("1"), Decimal("1") - elite_index / MAX_ELITE_CAPTURE)
    )
    raw = (survival_prob + elite_normalised + legitimacy) / Decimal("3")
    return max(Decimal("0"), min(Decimal("1"), raw))


def _aggregate_conditionality_terms(
    conditionality_events: list[Event],
) -> dict[tuple[str, str], Decimal]:
    """Aggregate effective fiscal deltas by (constraining_actor_id, constraint_mechanism).

    Reads conditionality metadata injected by ControlInput.get_events() and
    sums the primary magnitude of affected_attributes per term.

    Returns:
        Dict mapping (actor_id, mechanism) → total effective fiscal delta.
    """
    term_deltas: dict[tuple[str, str], Decimal] = {}
    for evt in conditionality_events:
        actor = str(evt.metadata.get("constraining_actor_id", ""))
        mechanism = str(evt.metadata.get("constraint_mechanism", ""))
        if not actor:
            continue
        key = (actor, mechanism)
        magnitude = _extract_magnitude(evt)
        if magnitude is not None:
            term_deltas[key] = term_deltas.get(key, Decimal("0")) + magnitude
    return term_deltas


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
