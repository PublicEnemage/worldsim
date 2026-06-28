"""ShockEffect protocol (ADR-019 D-7).

All shock handler classes must satisfy this structural protocol.
Using Protocol (not ABC) keeps handlers lightweight and avoids
import cycles — handlers import schemas, not engine internals.
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from app.schemas import ShockInjectRequest
    from app.simulation.state import SimulationState


class ShockEffect(Protocol):
    """Structural protocol for all shock handlers.

    A ShockEffect implementation receives the current scenario
    configuration dict (SimulationState) and a ShockInjectRequest,
    applies the shock's engine effect to the config, and returns
    the modified config dict. The caller persists the result.

    Handlers must be stateless — multiple calls with the same
    arguments must produce the same result.
    """

    def apply(
        self,
        state: SimulationState,
        request: ShockInjectRequest,
    ) -> SimulationState:
        """Apply shock engine effect to config state.

        Args:
            state: Scenario configuration dict (fiscal_multiplier, etc.)
            request: Validated ShockInjectRequest with typed parameters.

        Returns:
            Modified configuration dict. The original dict is not mutated.
        """
        ...
