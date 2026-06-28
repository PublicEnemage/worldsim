"""Shock handler implementations — ADR-019 D-7 + D-8.

All seven shock type handlers. Import order follows ShockType enum declaration
in schemas.py to make registration in SHOCK_REGISTRY readable.
"""
from app.simulation.shocks.handlers.contagion_shock import ContagionShockHandler
from app.simulation.shocks.handlers.creditor_defection import CreditorDefectionHandler
from app.simulation.shocks.handlers.currency_attack import CurrencyAttackHandler
from app.simulation.shocks.handlers.election_shock import ElectionShockHandler
from app.simulation.shocks.handlers.geopolitical_shock import GeopoliticalShockHandler
from app.simulation.shocks.handlers.growth_shock import GrowthShockHandler
from app.simulation.shocks.handlers.natural_disaster import NaturalDisasterHandler

__all__ = [
    "GrowthShockHandler",
    "ElectionShockHandler",
    "CurrencyAttackHandler",
    "CreditorDefectionHandler",
    "GeopoliticalShockHandler",
    "NaturalDisasterHandler",
    "ContagionShockHandler",
]
