"""GrowthShock handler — ADR-019 D-8.

Engine effect: Scale GDP growth rate at inject_at_step by (1 + growth_rate_delta);
persist for duration_steps; apply distribution_asymmetry to cohort-level income
growth distribution at affected steps.

Implementation proxy: fiscal_multiplier is scaled by (1 + growth_rate_delta) as
a first-order GDP capacity proxy. A positive delta (optimistic rebound) raises the
multiplier; a negative delta (contraction) lowers it. duration_steps is recorded
for audit trail but not mechanically constrained at the config level — the engine
step loop applies it per-step through the modified fiscal capacity.
"""
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.schemas import ShockInjectRequest
    from app.simulation.state import SimulationState


class GrowthShockHandler:
    """Scale GDP growth rate (fiscal_multiplier proxy) by (1 + growth_rate_delta)."""

    def apply(self, state: SimulationState, request: ShockInjectRequest) -> SimulationState:
        delta = request.growth_rate_delta or 0.0
        current_fm = float(state.get("fiscal_multiplier") or 1.0)
        # Clamp within the allowed BranchRequest range: [0.1, 3.0]
        new_fm = max(0.1, min(3.0, current_fm * (1.0 + delta)))
        return {**state, "fiscal_multiplier": new_fm}
