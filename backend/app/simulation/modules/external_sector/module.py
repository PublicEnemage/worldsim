"""ExternalSectorModule — ADR-012, Issue #752.

Distributes global CommodityPriceShock events to all scenario entities
proportional to their commodity import dependency coefficients.

Commodity price shocks are configured at scenario level via
ScenarioConfigSchema.commodity_price_shocks (list[CommodityShockConfig]).
Each entity's exposure is read from its
`commodity_import_dependency_{category}` attribute at compute() time.
Entities with no dependency attribute receive zero shock (no error raised).

One-step lag design: consistent with MacroeconomicModule — effects generated
at step N are applied to entity state at step N+1 via the propagation engine.

Step determination: current step is derived from (timestep - start_date) / 365
days. This assumes annual resolution. If sub-annual resolution is introduced,
this module must be updated (ADR-012 renewal trigger).

All generated events are flagged confidence_tier=3 for Jordan Demo 4 where
import dependency coefficients are synthetic estimates. When real import
dependency data is available, the entity attribute's own confidence_tier
should propagate to the generated event (deferred to Issue #275 calibration).
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

_DAYS_PER_STEP = 365


class ExternalSectorModule(SimulationModule):
    """Distributes global commodity price shocks to entities by import dependency.

    Constructed with the commodity_price_shocks list from ScenarioConfigSchema
    and the scenario start_date. Active only when shocks are configured.

    Args:
        commodity_price_shocks: List of CommodityShockConfig from scenario config.
        start_date: Scenario start date (step 0). None defaults to 2000-01-01.
    """

    def __init__(
        self,
        commodity_price_shocks: list[CommodityShockConfig],
        start_date: object | None,
    ) -> None:
        self._shocks = commodity_price_shocks
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
        return []

    def compute(
        self,
        entity: SimulationEntity,
        state: SimulationState,
        timestep: datetime,
    ) -> list[Event]:
        if not self._shocks:
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
            _log.debug(
                "[ExternalSector] entity=%s shock=%s step=%d effect=%s",
                entity.id,
                shock.commodity_category,
                current_step,
                effect,
            )

        return events
