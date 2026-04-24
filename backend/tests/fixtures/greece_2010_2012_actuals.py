"""Greece 2010–2012 IMF Program — historical actuals and fidelity thresholds.

Sources:
  - IMF World Economic Outlook April 2013 (outturn data for 2010–2012)
  - Eurostat National Accounts, April 2013 vintage

These actuals define the benchmark against which backtesting fidelity is
measured. ADR-004 Decision 3: M3 ships DIRECTION_ONLY thresholds only.
MAGNITUDE thresholds are deferred to Milestone 4 (Issue #44).
"""
from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal

# ---------------------------------------------------------------------------
# IA-1 disclosure — must match IA1_CANONICAL_PHRASE in quantity_serde.py
# ---------------------------------------------------------------------------

IA1_DISCLOSURE: str = (
    "Forward projections carry inherited confidence tier without time-horizon "
    "degradation. Confidence tiers reflect data quality at observation date, not "
    "projection reliability. See DATA_STANDARDS.md Known Limitation IA-1."
)

PARAMETER_CALIBRATION_DISCLOSURE: str = (
    "Parameter calibration tier system not yet implemented (Issue #44, deferred "
    "to Milestone 4). Fidelity thresholds are DIRECTION_ONLY — magnitude accuracy "
    "is not asserted. See DATA_STANDARDS.md Known Limitation and STD-REVIEW-002 SA-02."
)

# ---------------------------------------------------------------------------
# Historical actuals
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class GreeceActuals:
    """IMF-reported outturn values for Greece 2010–2012.

    GDP growth rates are expressed as ratios (e.g. -0.054 = -5.4%).
    Unemployment rates are also expressed as ratios (e.g. 0.126 = 12.6%).

    Sources: IMF World Economic Outlook April 2013; Eurostat.
    """

    gdp_growth_2010: Decimal = Decimal("-0.054")
    gdp_growth_2011: Decimal = Decimal("-0.089")
    gdp_growth_2012: Decimal = Decimal("-0.066")
    unemployment_rate_2010: Decimal = Decimal("0.126")
    unemployment_rate_2011: Decimal = Decimal("0.178")
    unemployment_rate_2012: Decimal = Decimal("0.244")


ACTUALS = GreeceActuals()

# ---------------------------------------------------------------------------
# Fidelity thresholds — DIRECTION_ONLY (ADR-004 Decision 3)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class FidelityThresholds:
    """M3 DIRECTION_ONLY fidelity thresholds for Greece 2010–2012.

    DIRECTION_ONLY: asserts that the simulated value is negative (contracting)
    for gdp_growth and positive (rising) for unemployment, matching the
    documented historical direction. No magnitude accuracy is asserted.

    Threshold type rationale: parameter calibration tier system not yet
    implemented (Issue #44). MAGNITUDE thresholds require calibration tier A/B
    per STD-REVIEW-002 SA-02 and are deferred to Milestone 4.
    """

    gdp_direction_correct: bool = True
    unemployment_direction_correct: bool = True


THRESHOLDS = FidelityThresholds()
