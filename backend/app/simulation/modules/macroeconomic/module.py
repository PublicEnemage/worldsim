"""MacroeconomicModule — ADR-006 Decisions 8 and 10; Amendment 1 (mean-reversion).

Subscribes to fiscal and monetary policy events from the previous step
(one-step lag design). Computes GDP growth using regime-dependent fiscal
multipliers, tracks inflation and fiscal balance, and emits
gdp_growth_change and regime_change events.

Regime-dependent fiscal multipliers (ADR-006 Decision 8):
  standard  (gdp_growth >= 0):         0.5
  depressed (-0.03 <= growth < 0):     1.5
  zlb       (growth < -0.03):          2.0

Mean-reversion channel (ADR-006 Amendment 1 — Issue #221):
  When an entity has a `trend_growth` attribute seeded, the module applies
  a reversion term toward that trend at every step, even in the absence of
  fiscal events. The reversion speed is modulated by regime — deep crisis
  regimes recover more slowly (Reinhart-Rogoff 2009; Cerra-Saxena 2008).

  reversion_term = REVERSION_SPEED × (trend_growth − gdp_growth) × regime_dampener

  If `trend_growth` is not seeded, the channel is inactive and module
  behaviour is unchanged from the pre-Amendment-1 design.

Decision 10 constraint: this module is wired in the same commit that
removes the DemographicModule legacy fiscal_spending_change subscription.
Once gdp_growth_change events are emitted here, that subscription becomes
the single GDP→demographic path.
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
# Module constants (ADR-006 Decision 1 / Decision 8)
# ---------------------------------------------------------------------------

FISCAL_MULTIPLIERS: dict[str, Decimal] = {
    "standard": Decimal("0.5"),
    "depressed": Decimal("1.5"),
    "zlb": Decimal("2.0"),
}

# Regime thresholds for GDP growth rate.
_THRESHOLD_DEPRESSED = Decimal("0")     # growth below this → depressed
_THRESHOLD_ZLB = Decimal("-0.03")       # growth below this → ZLB

# Tax multiplier is ~60% of spending multiplier (standard macro result).
_TAX_MULTIPLIER_RATIO = Decimal("0.6")

# Inflation transmission: spending change → mild demand-side pressure;
# tax change → mild cost-push pressure.
_SPENDING_INFLATION_COEFF = Decimal("0.5")
_TAX_INFLATION_COEFF = Decimal("0.3")

# Mean-reversion channel — ADR-006 Amendment 1 (Issue #221).
# Reversion speed (α): 10% per year — Cerra-Saxena (2008) estimate for
# developed economies. Calibration to individual country trajectories is
# deferred to Issue #44 (parameter calibration tier system).
REVERSION_SPEED = Decimal("0.10")

# Regime dampener: reduces recovery speed in crisis regimes.
# ZLB = 0.25 — sovereign debt crises have very slow output recovery
#   (Reinhart-Rogoff 2009: median recovery to pre-crisis output ~7 years).
# Depressed = 0.50 — moderate crisis, partial recovery channel active.
# Standard = 1.00 — normal regime, full reversion speed.
REGIME_DAMPENER: dict[str, Decimal] = {
    "standard": Decimal("1.00"),
    "depressed": Decimal("0.50"),
    "zlb": Decimal("0.25"),
}

_SUBSCRIBED_EVENTS = frozenset({
    "fiscal_policy_spending_change",
    "fiscal_policy_tax_rate_change",
    "monetary_policy_policy_rate",
})


def _detect_regime(gdp_growth: Decimal) -> str:
    """Return the fiscal multiplier regime for the given GDP growth rate."""
    if gdp_growth < _THRESHOLD_ZLB:
        return "zlb"
    if gdp_growth < _THRESHOLD_DEPRESSED:
        return "depressed"
    return "standard"


class MacroeconomicModule(SimulationModule):
    """Computes GDP growth, inflation, and fiscal balance for country entities.

    Processes fiscal and monetary policy events from the prior step.
    Applies regime-dependent fiscal multipliers and emits gdp_growth_change
    and (on regime transition) regime_change events.
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

        # Mean-reversion channel (ADR-006 Amendment 1): active only when
        # `trend_growth` is explicitly seeded on the entity. Without it,
        # behaviour is identical to the pre-Amendment-1 design.
        trend_growth_qty = entity.get_attribute("trend_growth")

        if not prior_events and trend_growth_qty is None:
            _log.debug(
                "%s: no subscribed events for entity_id=%r at timestep=%r — returning []",
                type(self).__name__,
                entity.id,
                timestep,
            )
            return []

        current_gdp_growth = entity.get_attribute_value("gdp_growth", Decimal("0"))
        current_regime = _detect_regime(current_gdp_growth)

        gdp_delta = Decimal("0")
        fiscal_balance_delta = Decimal("0")
        inflation_delta = Decimal("0")
        confidence_tier = 2

        for event in prior_events:
            magnitude = _extract_magnitude(event)
            if magnitude is None:
                continue
            event_tier = _event_confidence_tier(event)
            confidence_tier = max(confidence_tier, event_tier)

            if event.event_type == "fiscal_policy_spending_change":
                multiplier = FISCAL_MULTIPLIERS[current_regime]
                gdp_delta += magnitude * multiplier
                fiscal_balance_delta -= magnitude
                inflation_delta += magnitude * _SPENDING_INFLATION_COEFF

            elif event.event_type == "fiscal_policy_tax_rate_change":
                multiplier = FISCAL_MULTIPLIERS[current_regime] * _TAX_MULTIPLIER_RATIO
                gdp_delta -= magnitude * multiplier
                fiscal_balance_delta += magnitude
                inflation_delta += magnitude * _TAX_INFLATION_COEFF

            elif event.event_type == "monetary_policy_policy_rate":
                # Rate cut (negative magnitude) → mild upward inflation pressure.
                inflation_delta -= magnitude * Decimal("0.1")

        # Apply mean-reversion when trend_growth is seeded (ADR-006 Amendment 1).
        if trend_growth_qty is not None:
            dampener = REGIME_DAMPENER[current_regime]
            reversion_term = (
                REVERSION_SPEED * (trend_growth_qty.value - current_gdp_growth) * dampener
            )
            gdp_delta += reversion_term
            confidence_tier = max(confidence_tier, trend_growth_qty.confidence_tier)

        if gdp_delta == Decimal("0") and fiscal_balance_delta == Decimal("0"):
            return []

        new_gdp_growth = current_gdp_growth + gdp_delta
        new_regime = _detect_regime(new_gdp_growth)

        gdp_event = Event(
            event_id=f"macro-gdp-{entity.id}-{timestep.isoformat()}",
            source_entity_id=entity.id,
            event_type="gdp_growth_change",
            affected_attributes=_build_macro_attributes(
                gdp_delta, fiscal_balance_delta, inflation_delta, confidence_tier
            ),
            propagation_rules=[],
            timestep_originated=timestep,
            framework=MeasurementFramework.FINANCIAL,
            metadata={"regime": current_regime},
        )

        result: list[Event] = [gdp_event]

        if new_regime != current_regime:
            threshold = (
                _THRESHOLD_ZLB if new_regime == "zlb" else _THRESHOLD_DEPRESSED
            )
            result.append(Event(
                event_id=f"macro-regime-{entity.id}-{timestep.isoformat()}",
                source_entity_id=entity.id,
                event_type="regime_change",
                affected_attributes={},
                propagation_rules=[],
                timestep_originated=timestep,
                framework=MeasurementFramework.FINANCIAL,
                metadata={
                    "regime_previous": current_regime,
                    "regime_new": new_regime,
                    "trigger_attribute": "gdp_growth_rate",
                    "trigger_value": str(new_gdp_growth),
                    "threshold": str(threshold),
                },
            ))

        return result

    def get_subscribed_events(self) -> list[str]:
        return list(_SUBSCRIBED_EVENTS)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _build_macro_attributes(
    gdp_delta: Decimal,
    fiscal_delta: Decimal,
    inflation_delta: Decimal,
    confidence_tier: int,
) -> dict[str, Quantity]:
    attrs: dict[str, Quantity] = {
        "gdp_growth": Quantity(
            value=gdp_delta,
            unit="ratio",
            variable_type=VariableType.RATIO,
            measurement_framework=MeasurementFramework.FINANCIAL,
            confidence_tier=confidence_tier,
        ),
    }
    if fiscal_delta != Decimal("0"):
        attrs["fiscal_balance_pct_gdp"] = Quantity(
            value=fiscal_delta,
            unit="ratio",
            variable_type=VariableType.RATIO,
            measurement_framework=MeasurementFramework.FINANCIAL,
            confidence_tier=confidence_tier,
        )
    if inflation_delta != Decimal("0"):
        attrs["inflation_rate"] = Quantity(
            value=inflation_delta,
            unit="ratio",
            variable_type=VariableType.RATIO,
            measurement_framework=MeasurementFramework.FINANCIAL,
            confidence_tier=confidence_tier,
        )
    return attrs


def _extract_magnitude(event: Event) -> Decimal | None:
    """Return the primary scalar magnitude from an event's affected_attributes."""
    if not event.affected_attributes:
        return None
    return next(iter(event.affected_attributes.values())).value


def _event_confidence_tier(event: Event) -> int:
    """Return the max confidence_tier across an event's affected_attributes."""
    if not event.affected_attributes:
        return 2
    return max(q.confidence_tier for q in event.affected_attributes.values())
