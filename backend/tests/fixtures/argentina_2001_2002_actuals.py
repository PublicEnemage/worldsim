"""Argentina 2001–2002 currency and debt crisis — historical actuals and thresholds.

Sources:
  IMF World Economic Outlook April 2002 (2001 GDP outturn):
      gdp_growth_2001 = -4.4%  (rounded from -4.41%)
  IMF World Economic Outlook April 2003 (2002 GDP outturn):
      gdp_growth_2002 = -10.9% (rounded from -10.89%)
  INDEC EPH (Encuesta Permanente de Hogares, public historical series):
      unemployment_rate_2001 = 16.4% (May 2001 wave)
      unemployment_rate_2002 = 21.5% (May 2002 wave)

Data provenance:
  IMF WEO is public domain data published by the International Monetary Fund.
  INDEC EPH data is published under Argentine open data policy
  (Ley 27.275 of 2016, Decreto 117/2016). Both sources comply with the
  open-licensed data requirement in CLAUDE.md §Equitable Build Process.

DIRECTION_ONLY thresholds — same rationale as Greece (ADR-004 Decision 3):
magnitude calibration is deferred until DISTRIBUTION_COMBINED thresholds
(Issue #194 infrastructure) are populated with calibrated uncertainty bands.
"""
from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal

from app.simulation.repositories.quantity_serde import IA1_CANONICAL_PHRASE

IA1_DISCLOSURE: str = IA1_CANONICAL_PHRASE

PARAMETER_CALIBRATION_DISCLOSURE: str = (
    "Argentina 2001–2002 thresholds are DIRECTION_ONLY — magnitude accuracy "
    "is not asserted. DISTRIBUTION_COMBINED thresholds require calibrated "
    "parameter uncertainty bands; infrastructure is in place (Issue #194) but "
    "calibration is deferred to a future milestone. "
    "See DATA_STANDARDS.md Known Limitation."
)


@dataclass(frozen=True)
class ArgentinaActuals:
    """Historical outturn values for Argentina 2001–2002.

    GDP growth rates are expressed as ratios (e.g. -0.044 = -4.4%).
    Unemployment rates are expressed as ratios (e.g. 0.164 = 16.4%).

    Sources:
      gdp_growth_2001 — IMF WEO April 2002 outturn
      gdp_growth_2002 — IMF WEO April 2003 outturn
      unemployment_rate_2001 — INDEC EPH May 2001 wave
      unemployment_rate_2002 — INDEC EPH May 2002 wave
    """

    gdp_growth_2001: Decimal = Decimal("-0.044")
    gdp_growth_2002: Decimal = Decimal("-0.109")

    # INDEC EPH semi-annual waves (pre-2003 continuous methodology)
    unemployment_rate_2001: Decimal = Decimal("0.164")
    unemployment_rate_2002: Decimal = Decimal("0.215")


ACTUALS = ArgentinaActuals()


@dataclass(frozen=True)
class FidelityThresholds:
    """Argentina 2001–2002 DIRECTION_ONLY fidelity thresholds.

    DIRECTION_ONLY: asserts that simulated gdp_growth is negative at
    steps 1 and 2, matching the documented historical contraction in
    2001 (-4.4%) and 2002 (-10.9%).

    No magnitude accuracy is asserted. A structurally correct simulation
    must predict contraction under the combination of large pro-cyclical
    fiscal adjustment (Zero Deficit Plan), IMF program conditionality,
    and sovereign default — all of which the fixture injects.

    Threshold seeded into backtesting_thresholds as case_id='ARGENTINA_2001_2002'
    (migration c7e2a9f4d1b8).
    """

    gdp_direction_step1_correct: bool = True
    gdp_direction_step2_correct: bool = True


THRESHOLDS = FidelityThresholds()
