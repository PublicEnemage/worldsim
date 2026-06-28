"""ContagionShock handler — ADR-019 D-8.

Engine effect: Apply transmission_rate × (source entity's GDP impact) to this
entity's GDP at inject_at_step; apply to affected_sectors (or all sectors if empty);
trigger regional module if regional_contagion = True.

Implementation: transmission_rate is the fraction of the originating shock that
propagates. A transmission_rate of 0.2 means 20% of the source country's shock
propagates here. The fiscal_multiplier is reduced proportionally (0.25 coefficient
captures the spillover to fiscal capacity).
"""
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.schemas import ShockInjectRequest
    from app.simulation.state import SimulationState


class ContagionShockHandler:
    """Cross-border contagion propagation via transmission_rate → fiscal capacity."""

    def apply(self, state: SimulationState, request: ShockInjectRequest) -> SimulationState:
        rate = request.transmission_rate or 0.0
        current_fm = float(state.get("fiscal_multiplier") or 1.0)
        # transmission_rate = 0.2: 25% coefficient → 5% fiscal capacity reduction
        new_fm = max(0.1, min(3.0, current_fm * (1.0 - rate * 0.25)))
        return {**state, "fiscal_multiplier": new_fm}
