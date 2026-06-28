"""NaturalDisaster handler — ADR-019 D-8.

Engine effect: Apply gdp_impact (negative fraction) to GDP at inject_at_step;
distribute across affected_sectors proportionally if specified.

Implementation: gdp_impact is a negative fraction (e.g., -0.05 = -5% of GDP).
The fiscal_multiplier absorbs this as a reduced capacity multiplier. A -0.05
gdp_impact (1+(-0.05) = 0.95 multiplier) reduces fiscal capacity proportionally.
"""
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.schemas import ShockInjectRequest
    from app.simulation.state import SimulationState


class NaturalDisasterHandler:
    """GDP impact from natural event (negative fraction) → fiscal capacity scaling."""

    def apply(self, state: SimulationState, request: ShockInjectRequest) -> SimulationState:
        gdp_impact = request.gdp_impact or 0.0
        current_fm = float(state.get("fiscal_multiplier") or 1.0)
        # gdp_impact is negative (e.g. -0.05); (1 + gdp_impact) = 0.95 → 5% reduction
        new_fm = max(0.1, min(3.0, current_fm * (1.0 + gdp_impact)))
        return {**state, "fiscal_multiplier": new_fm}
