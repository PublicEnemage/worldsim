"""SimulationState type alias for shock handlers (ADR-019 D-7).

Shock handlers operate on the scenario configuration dict (flat key-value
mapping) rather than the engine's runtime dataclass. This alias makes
the handler signatures self-documenting and keeps the dependency on
engine internals minimal.
"""
from __future__ import annotations

from typing import Any

# Config dict alias used by all ShockEffect handlers.
# Keys are scenario configuration fields (fiscal_multiplier, legitimacy_index, etc.)
# Values are the Python types stored in the scenario's configuration JSONB column.
SimulationState = dict[str, Any]
