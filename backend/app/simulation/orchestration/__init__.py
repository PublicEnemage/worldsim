"""
Input Orchestration Layer — ADR-002, Amendment 1.

Single entry point for all exogenous control inputs into the simulation.
Module-generated events are endogenous (computed from internal logic).
ControlInputs are exogenous (human decisions injected regardless of what
modules would compute). Both become Events in the propagation engine.

The distinction is enforced architecturally: every exogenous input passes
through InputOrchestrator.inject(), which validates, translates, and records
it before it reaches the propagation engine. Scenarios are reproducible by
replaying their audit logs.

Amendment 1 (SCR-001 / ADR-002 Amendment 1):
MonetaryInstrument split into MonetaryRateInstrument and
MonetaryVolumeInstrument. MonetaryPolicyInput split into
MonetaryRateInput and MonetaryVolumeInput.
"""

from app.simulation.orchestration.audit import AuditLog, ControlInputAuditRecord
from app.simulation.orchestration.inputs import (
    ComparisonOperator,
    ContingentInput,
    ControlInput,
    EmergencyInstrument,
    EmergencyPolicyInput,
    FiscalInstrument,
    FiscalPolicyInput,
    InputSource,
    MonetaryRateInput,
    MonetaryRateInstrument,
    MonetaryVolumeInput,
    MonetaryVolumeInstrument,
    StateCondition,
    StructuralInstrument,
    StructuralPolicyInput,
    TradeInstrument,
    TradePolicyInput,
)
from app.simulation.orchestration.runner import InputOrchestrator, ScenarioRunner

__all__ = [
    # Audit
    "AuditLog",
    "ControlInputAuditRecord",
    # Inputs — base
    "ControlInput",
    "InputSource",
    # Inputs — monetary (rate)
    "MonetaryRateInstrument",
    "MonetaryRateInput",
    # Inputs — monetary (volume)
    "MonetaryVolumeInstrument",
    "MonetaryVolumeInput",
    # Inputs — fiscal
    "FiscalInstrument",
    "FiscalPolicyInput",
    # Inputs — trade
    "TradeInstrument",
    "TradePolicyInput",
    # Inputs — emergency
    "EmergencyInstrument",
    "EmergencyPolicyInput",
    # Inputs — structural
    "StructuralInstrument",
    "StructuralPolicyInput",
    # Inputs — contingent
    "ComparisonOperator",
    "StateCondition",
    "ContingentInput",
    # Runner
    "InputOrchestrator",
    "ScenarioRunner",
]
