"""GeopoliticalShock handler — ADR-019 D-8.

Engine effect: Same engine effect as ElectionShock (severity + political_uncertainty);
distinct shock type for causal attribution: MDA alert shows "Caused by: geopolitical
shock" vs. "Caused by: political transition".

Implementation: identical coefficient structure to ElectionShockHandler. The
distinction is in the shock_type label used for causal attribution in TrajectoryStep
shock_events — not in the numeric effect on the config.
"""
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.schemas import ShockInjectRequest
    from app.simulation.state import SimulationState


class GeopoliticalShockHandler:
    """Political uncertainty via geopolitical event — same fiscal/legitimacy effect as election."""

    def apply(self, state: SimulationState, request: ShockInjectRequest) -> SimulationState:
        severity = request.severity or 0.0

        current_fm = float(state.get("fiscal_multiplier") or 1.0)
        new_fm = max(0.1, min(3.0, current_fm * (1.0 - severity * 0.25)))
        result: SimulationState = {**state, "fiscal_multiplier": new_fm}

        political_context = state.get("political_context")
        if isinstance(political_context, dict):
            new_pc = dict(political_context)
            raw_li = political_context.get("legitimacy_index")
            li = float(raw_li) if raw_li is not None else 0.7
            new_pc["legitimacy_index"] = str(max(0.0, li - severity * 0.4))
            result["political_context"] = new_pc

        return result
