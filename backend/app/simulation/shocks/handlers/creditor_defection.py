"""CreditorDefection handler — ADR-019 D-8.

Engine effect: Remove share_affected fraction of creditor_class disbursement from
the financing gap calculation at inject_at_step; apply regime_change_probability
as a probability-weighted governance uncertainty for duration_steps = 3 (default).

Implementation: fiscal_multiplier is reduced proportionally to the financing gap
impact of the defection. share_affected = 0.3 on bilateral creditors produces a
reduction coefficient of 0.3 × 0.4 = 0.12 (40% of fiscal capacity is assumed
to be creditor-financed in a typical IDA-eligible economy).
"""
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.schemas import ShockInjectRequest
    from app.simulation.state import SimulationState


class CreditorDefectionHandler:
    """Remove share_affected fraction of creditor financing from fiscal capacity."""

    def apply(self, state: SimulationState, request: ShockInjectRequest) -> SimulationState:
        share = request.share_affected or 0.0
        current_fm = float(state.get("fiscal_multiplier") or 1.0)
        # 0.4 = assumed creditor-financed fraction of fiscal capacity
        new_fm = max(0.1, min(3.0, current_fm * (1.0 - share * 0.4)))
        return {**state, "fiscal_multiplier": new_fm}
