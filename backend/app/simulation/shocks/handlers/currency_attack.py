"""CurrencyAttack handler — ADR-019 D-8.

Engine effect: Apply attack_magnitude as a fractional depreciation to the FX rate
parameter in the fiscal module at inject_at_step; propagate through debt service
calculation for foreign-denominated obligations.

Implementation: fiscal_multiplier is reduced by attack_magnitude × 0.5 coefficient
to capture the fiscal capacity loss from FX depreciation (higher debt service costs
in domestic currency terms reduce the effective fiscal space).
"""
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.schemas import ShockInjectRequest
    from app.simulation.state import SimulationState


class CurrencyAttackHandler:
    """FX depreciation → reduced effective fiscal capacity."""

    def apply(self, state: SimulationState, request: ShockInjectRequest) -> SimulationState:
        magnitude = request.attack_magnitude or 0.0
        current_fm = float(state.get("fiscal_multiplier") or 1.0)
        # 15% FX depreciation (magnitude=0.15) reduces fiscal multiplier by 0.075
        new_fm = max(0.1, min(3.0, current_fm * (1.0 - magnitude * 0.5)))
        return {**state, "fiscal_multiplier": new_fm}
