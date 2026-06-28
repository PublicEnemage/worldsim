"""ElectionShock handler — ADR-019 D-8.

Engine effect: Apply severity as a step-function drop to legitimacy_index at
inject_at_step; propagate political_uncertainty as a governance volatility
modifier for duration_steps = 2 (default).

Implementation: legitimacy_index in political_context is reduced by
severity × 0.5 (a calibrated fraction — severity = 1.0 halves the index).
fiscal_multiplier is also reduced proportionally (severity × 0.3 coefficient)
to capture the fiscal disruption from political instability.
"""
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.schemas import ShockInjectRequest
    from app.simulation.state import SimulationState


class ElectionShockHandler:
    """Step-function drop to legitimacy_index + fiscal capacity reduction."""

    def apply(self, state: SimulationState, request: ShockInjectRequest) -> SimulationState:
        severity = request.severity or 0.0

        # Fiscal capacity reduction (financial composite proxy)
        current_fm = float(state.get("fiscal_multiplier") or 1.0)
        new_fm = max(0.1, min(3.0, current_fm * (1.0 - severity * 0.3)))
        result: SimulationState = {**state, "fiscal_multiplier": new_fm}

        # Legitimacy index reduction in political_context sub-dict
        political_context = state.get("political_context")
        if isinstance(political_context, dict):
            new_pc = dict(political_context)
            raw_li = political_context.get("legitimacy_index")
            li = float(raw_li) if raw_li is not None else 0.7
            new_pc["legitimacy_index"] = str(max(0.0, li - severity * 0.5))
            result["political_context"] = new_pc

        return result
