"""SHOCK_REGISTRY — maps ShockType enum values to handler classes (ADR-019 D-7).

Adding a new shock type requires:
  1. New ShockType value in app.schemas
  2. New handler module in handlers/
  3. One new entry here

No changes to the ShockEffect protocol or the inject-shock endpoint.
"""
from __future__ import annotations

from typing import TYPE_CHECKING

from app.schemas import ShockType
from app.simulation.shocks.handlers import (
    ContagionShockHandler,
    CreditorDefectionHandler,
    CurrencyAttackHandler,
    ElectionShockHandler,
    GeopoliticalShockHandler,
    GrowthShockHandler,
    NaturalDisasterHandler,
)

if TYPE_CHECKING:
    from app.simulation.shocks.protocol import ShockEffect

SHOCK_REGISTRY: dict[ShockType, type[ShockEffect]] = {
    ShockType.GrowthShock: GrowthShockHandler,
    ShockType.ElectionShock: ElectionShockHandler,
    ShockType.CurrencyAttack: CurrencyAttackHandler,
    ShockType.CreditorDefection: CreditorDefectionHandler,
    ShockType.GeopoliticalShock: GeopoliticalShockHandler,
    ShockType.NaturalDisaster: NaturalDisasterHandler,
    ShockType.ContagionShock: ContagionShockHandler,
}
