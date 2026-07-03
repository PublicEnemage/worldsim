"""ExternalSectorModule — ADR-012, Issue #752.

Distributes global CommodityPriceShock events to all scenario entities
proportional to their commodity import dependency coefficients.

Commodity price shocks are configured at scenario level via
ScenarioConfigSchema.commodity_price_shocks (list[CommodityShockConfig]).
Each entity's exposure is read from its
`commodity_import_dependency_{category}` attribute at compute() time.
Entities with no dependency attribute receive zero shock (no error raised).

Ecological-to-financial transmission (Issue #275, ADR-012 §ecological boundary):
When ecological_shock_coefficient > 0, the module applies a per-step FINANCIAL
framework delta to fiscal_balance_pct_gdp via the soil-degradation → agricultural
export → fiscal revenue pathway:

  per_step_delta = -(coefficient
                     × base_agricultural_export_share
                     × arable_land_degradation_rate
                     × _ECO_FISCAL_CALIBRATION_FACTOR)

_ECO_FISCAL_CALIBRATION_FACTOR = 0.3 normalises to the Zimbabwe 2000 land reform
calibration anchor (EE DIC review 2026-06-24): ±30% tolerance around 1.0–1.5%
GDP cumulative fiscal reduction at step 4 (agricultural-channel-attributable
portion only; not the full 4% total fiscal decline which includes monetary
dysfunction).

Entities missing either attribute are silently skipped — no error raised.

One-step lag design: consistent with MacroeconomicModule — effects generated
at step N are applied to entity state at step N+1 via the propagation engine.

Step determination: current step is derived from (timestep - start_date) / 365
days. This assumes annual resolution. If sub-annual resolution is introduced,
this module must be updated (ADR-012 renewal trigger).

All generated events are flagged confidence_tier=3 for Jordan Demo 4 where
import dependency coefficients are synthetic estimates. When real import
dependency data is available, the entity attribute's own confidence_tier
should propagate to the generated event (deferred to Issue #275 calibration).

Per commodity shock, three events are emitted per entity per active step:
  1. import_price_inflation (FINANCIAL) — trade balance pressure indicator.
  2. bottom_quintile_consumption_capacity (HUMAN_DEVELOPMENT) — HCL transmission.
  3. reserve_coverage_months (FINANCIAL) — reserve depletion channel.

Reserve depletion channel: higher import costs increase foreign exchange
outflows, depleting the central bank's import-cover reserve buffer.
The _RESERVE_BURN_RATE coefficient maps import-cost pressure (dep × magnitude)
to months of reserve drawdown per annual step. Calibrated to produce the Demo 4
narrative arc (JOR reserves approach CRITICAL floor by step 5). This is a
simplified linear approximation; full calibration per Issue #275.
"""
from __future__ import annotations

import logging
from datetime import UTC
from datetime import datetime as _datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from app.simulation.engine.models import (
    Event,
    MeasurementFramework,
    SimulationModule,
)
from app.simulation.engine.quantity import Quantity, VariableType

if TYPE_CHECKING:
    from datetime import datetime

    from app.schemas import CommodityShockConfig
    from app.simulation.engine.models import SimulationEntity, SimulationState

_log = logging.getLogger(__name__)

# Fraction of global commodity price shock that reaches bottom-quintile
# consumption within one step. Consistent with BilateralTradeShock constant.
# Calibration basis: Issue #275. Simplified constant until calibrated.
_HCL_TRANSMISSION_FACTOR = Decimal("0.3")

# Months of reserve drawdown per unit of commodity import cost pressure per step.
# Formula: reserve_depletion = dep_coefficient × shock_magnitude × _RESERVE_BURN_RATE
# Calibrated so JOR (dep=0.42, fuel shock 0.25) crosses the CRITICAL floor (2.5 months)
# from 7.1 months by step 5 (Demo 4 narrative: "Reserve drawdown critical" at step 5).
# One-step lag: events generated at step N apply to state N+1; coefficient 8.5 is derived
# from the constraint reserves_step5 < 2.5 with JOR fuel+food dual-shock from steps 1-4.
_RESERVE_BURN_RATE = Decimal("8.5")

# Ecological-to-fiscal calibration factor (Issue #275, EE DIC review 2026-06-24).
# Normalises the raw formula (coefficient × base_agri_share × degradation_rate = ~1%/step)
# to the agricultural-channel-attributable portion of the Zimbabwe 2000 historical record.
# Full formula gives ~4.2% cumulative over 4 steps; the historical attributable portion
# (separating from monetary dysfunction) is ~1.0–1.5% GDP at step 4. Factor 0.3 produces
# 0.35 × 0.20 × 0.15 × 0.3 × 4 = 1.26% GDP cumulative — within the ±30% tolerance band.
_ECO_FISCAL_CALIBRATION_FACTOR = Decimal("0.3")

_DAYS_PER_STEP = 365


class ExternalSectorModule(SimulationModule):
    """Distributes global commodity price shocks to entities by import dependency.

    Also applies the ecological-to-financial transmission pathway when
    ecological_shock_coefficient > 0 (Issue #275).

    Args:
        commodity_price_shocks: List of CommodityShockConfig from scenario config.
        start_date: Scenario start date (step 0). None defaults to 2000-01-01.
        ecological_shock_coefficient: Scalar [0, 1] from ScenarioConfigSchema.
            Controls intensity of soil-degradation → agricultural export →
            fiscal revenue pathway. 0.0 (default) disables the pathway entirely.
    """

    def __init__(
        self,
        commodity_price_shocks: list[CommodityShockConfig],
        start_date: object | None,
        ecological_shock_coefficient: Decimal = Decimal("0"),
    ) -> None:
        self._shocks = commodity_price_shocks
        self._eco_coeff = ecological_shock_coefficient
        if start_date is not None:
            from datetime import date  # noqa: PLC0415
            if isinstance(start_date, date):
                self._start_dt = _datetime(
                    start_date.year, start_date.month, start_date.day, tzinfo=UTC
                )
            else:
                self._start_dt = _datetime(2000, 1, 1, tzinfo=UTC)
        else:
            self._start_dt = _datetime(2000, 1, 1, tzinfo=UTC)

    def get_subscribed_events(self) -> list[str]:
        return ["emergency_policy_capital_controls"]

    def compute(
        self,
        entity: SimulationEntity,
        state: SimulationState,
        timestep: datetime,
    ) -> list[Event]:
        cc_events = [
            e for e in state.events
            if e.source_entity_id == entity.id
            and e.event_type == "emergency_policy_capital_controls"
        ]
        if not self._shocks and self._eco_coeff == Decimal("0") and not cc_events:
            return []

        ts = timestep if timestep.tzinfo else timestep.replace(tzinfo=UTC)
        start = self._start_dt
        current_step = max(0, round((ts - start).days / _DAYS_PER_STEP))

        events: list[Event] = []
        for shock in self._shocks:
            if not (shock.start_step <= current_step < shock.start_step + shock.duration_steps):
                continue

            dep_key = f"commodity_import_dependency_{shock.commodity_category}"
            dep_qty = entity.get_attribute(dep_key)
            if dep_qty is None or dep_qty.value == Decimal("0"):
                continue

            effect = dep_qty.value * shock.magnitude
            import uuid  # noqa: PLC0415
            base_id = str(uuid.uuid4())

            fin_delta = Quantity(
                value=effect,
                unit="dimensionless",
                variable_type=VariableType.FLOW,
                measurement_framework=MeasurementFramework.FINANCIAL,
                confidence_tier=3,
            )
            hcl_delta = Quantity(
                value=-(effect * _HCL_TRANSMISSION_FACTOR),
                unit="dimensionless",
                variable_type=VariableType.FLOW,
                measurement_framework=MeasurementFramework.HUMAN_DEVELOPMENT,
                confidence_tier=3,
            )
            # Reserve depletion: higher import costs drain foreign exchange reserves.
            # Negative FLOW delta on reserve_coverage_months (additive per propagation
            # engine FLOW semantics — reduces the existing stock each step).
            reserve_delta = Quantity(
                value=-(effect * _RESERVE_BURN_RATE),
                unit="months",
                variable_type=VariableType.FLOW,
                measurement_framework=MeasurementFramework.FINANCIAL,
                confidence_tier=3,
            )

            events.append(
                Event(
                    event_id=f"{base_id}-cps-fin",
                    source_entity_id=entity.id,
                    event_type=f"commodity_price_shock_{shock.commodity_category}",
                    affected_attributes={"import_price_inflation": fin_delta},
                    propagation_rules=[],
                    timestep_originated=timestep,
                    framework=MeasurementFramework.FINANCIAL,
                    metadata={
                        "commodity_category": shock.commodity_category,
                        "dependency_coefficient": str(dep_qty.value),
                        "shock_magnitude": str(shock.magnitude),
                        "synthetic_tier3": True,
                    },
                )
            )
            events.append(
                Event(
                    event_id=f"{base_id}-cps-hcl",
                    source_entity_id=entity.id,
                    event_type=f"commodity_price_shock_{shock.commodity_category}_hcl",
                    affected_attributes={"bottom_quintile_consumption_capacity": hcl_delta},
                    propagation_rules=[],
                    timestep_originated=timestep,
                    framework=MeasurementFramework.HUMAN_DEVELOPMENT,
                    metadata={
                        "commodity_category": shock.commodity_category,
                        "dependency_coefficient": str(dep_qty.value),
                    },
                )
            )
            events.append(
                Event(
                    event_id=f"{base_id}-cps-rsv",
                    source_entity_id=entity.id,
                    event_type=f"commodity_price_shock_{shock.commodity_category}_reserve",
                    affected_attributes={"reserve_coverage_months": reserve_delta},
                    propagation_rules=[],
                    timestep_originated=timestep,
                    framework=MeasurementFramework.FINANCIAL,
                    metadata={
                        "commodity_category": shock.commodity_category,
                        "dependency_coefficient": str(dep_qty.value),
                        "reserve_burn_rate": str(_RESERVE_BURN_RATE),
                        "synthetic_tier3": True,
                    },
                )
            )
            _log.debug(
                "[ExternalSector] entity=%s shock=%s step=%d effect=%s",
                entity.id,
                shock.commodity_category,
                current_step,
                effect,
            )

        # Ecological-to-financial transmission (Issue #275).
        # Fires every step when coefficient > 0 and both entity attributes are present.
        # Pathway: soil degradation → reduced agricultural exports → fiscal revenue loss.
        if self._eco_coeff > Decimal("0"):
            agri_share_qty = entity.get_attribute("base_agricultural_export_share")
            degradation_qty = entity.get_attribute("arable_land_degradation_rate")
            if agri_share_qty is not None and degradation_qty is not None:
                fiscal_impact = (
                    self._eco_coeff
                    * agri_share_qty.value
                    * degradation_qty.value
                    * _ECO_FISCAL_CALIBRATION_FACTOR
                )
                import uuid  # noqa: PLC0415
                fiscal_delta = Quantity(
                    value=-fiscal_impact,
                    unit="ratio",
                    variable_type=VariableType.FLOW,
                    measurement_framework=MeasurementFramework.FINANCIAL,
                    confidence_tier=3,
                )
                events.append(
                    Event(
                        event_id=str(uuid.uuid4()),
                        source_entity_id=entity.id,
                        event_type="ecological_fiscal_transmission",
                        affected_attributes={"fiscal_balance_pct_gdp": fiscal_delta},
                        propagation_rules=[],
                        timestep_originated=timestep,
                        framework=MeasurementFramework.FINANCIAL,
                        metadata={
                            "ecological_shock_coefficient": str(self._eco_coeff),
                            "base_agricultural_export_share": str(agri_share_qty.value),
                            "arable_land_degradation_rate": str(degradation_qty.value),
                            "calibration_factor": str(_ECO_FISCAL_CALIBRATION_FACTOR),
                            "calibration_anchor": "Zimbabwe 2000 land reform — EE DIC 2026-06-24",
                        },
                    )
                )
                _log.debug(
                    "[ExternalSector] entity=%s eco_fiscal step=%d impact=%s",
                    entity.id,
                    current_step,
                    fiscal_impact,
                )

        # ADR-020 Channel A: capital controls → reserve protection.
        # Reduces outflow velocity (ε fraction) → positive reserve_coverage_months delta.
        outflow_attr = entity.get_attribute("capital_account_outflow_velocity")
        outflow_velocity = outflow_attr.value if outflow_attr is not None else Decimal("0")
        for cc_event in cc_events:
            cc_qty = cc_event.affected_attributes.get("capital_controls")
            if cc_qty is None:
                continue
            params = cc_event.metadata.get("parameters", {})
            epsilon = Decimal(str(params.get("epsilon", "0.50")))
            impl_cap = Decimal(str(params.get("implementation_capacity", "0.75")))
            reserve_delta_val = outflow_velocity * epsilon * abs(cc_qty.value) * impl_cap
            import uuid  # noqa: PLC0415
            events.append(Event(
                event_id=str(uuid.uuid4()),
                source_entity_id=entity.id,
                event_type="capital_controls_reserve_protection",
                affected_attributes={
                    "reserve_coverage_months": Quantity(
                        value=reserve_delta_val,
                        unit="months",
                        variable_type=VariableType.FLOW,
                        measurement_framework=MeasurementFramework.FINANCIAL,
                        confidence_tier=2,
                    ),
                },
                propagation_rules=[],
                timestep_originated=timestep,
                framework=MeasurementFramework.FINANCIAL,
                metadata={"channel": "A_capital_controls"},
            ))

        return events
