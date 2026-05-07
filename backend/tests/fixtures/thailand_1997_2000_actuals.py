"""Thailand 1997–2000 Asian financial crisis — historical actuals and thresholds.

Sources:
  IMF World Economic Outlook October 1998 (1997 GDP outturn):
      gdp_growth_1997 = -1.4%  (rounded from -1.37%)
  IMF World Economic Outlook April 1999 (1998 GDP outturn):
      gdp_growth_1998 = -10.5% (rounded from -10.51%)
  World Bank World Development Indicators (1997 vintage, ILO-modelled estimate):
      unemployment_rate_1997 = 1.5%
  World Bank World Development Indicators (1998 vintage, ILO-modelled estimate):
      unemployment_rate_1998 = 3.4%

Data provenance:
  IMF WEO data is public domain data published by the International Monetary Fund.
  World Bank WDI unemployment figures use ILO-modelled estimates, published under
  the CC BY 4.0 International license. Both sources comply with the open-licensed
  data requirement in CLAUDE.md §Equitable Build Process.

Known limitation on unemployment actuals:
  Thailand's official unemployment figures are structurally low relative to actual
  labour market distress. During the 1997–1998 crisis, displaced urban workers
  returned to the agricultural sector (subsistence fallback), which absorbed
  much of the shock invisibly in formal unemployment statistics. The ILO-modelled
  figures (1.5%→3.4%) significantly understate the effective labour market damage.
  This is a known feature of Thailand's dual-sector labour market structure and
  is documented as a model blind spot.

DIRECTION_ONLY thresholds — same rationale as Greece, Argentina, and Lebanon:
magnitude calibration is deferred until DISTRIBUTION_COMBINED thresholds
(Issue #194 infrastructure) are populated with calibrated uncertainty bands.

Thailand exhibits herding and contagion dynamics (speculative currency attack
followed by regional contagion across the Asian Tigers) that make it a future
CASCADE propagation validation case (#29). See test_thailand_1997_2000.py.
"""
from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal

from app.simulation.repositories.quantity_serde import IA1_CANONICAL_PHRASE

IA1_DISCLOSURE: str = IA1_CANONICAL_PHRASE

PARAMETER_CALIBRATION_DISCLOSURE: str = (
    "Thailand 1997–2000 thresholds are DIRECTION_ONLY — magnitude accuracy "
    "is not asserted. DISTRIBUTION_COMBINED thresholds require calibrated "
    "parameter uncertainty bands; infrastructure is in place (Issue #194) but "
    "calibration is deferred to a future milestone. "
    "The 1998 GDP collapse (-10.5%) reflects cascading dynamics not yet fully "
    "modeled: speculative currency attack → peg abandonment → banking system "
    "stress → corporate balance-sheet recession → regional contagion. "
    "See DATA_STANDARDS.md Known Limitation."
)


@dataclass(frozen=True)
class ThailandActuals:
    """Historical outturn values for Thailand 1997–2000.

    GDP growth rates are expressed as ratios (e.g. -0.014 = -1.4%).
    Unemployment rates are expressed as ratios (e.g. 0.015 = 1.5%).

    Sources:
      gdp_growth_1997        — IMF WEO October 1998 outturn (-1.37%)
      gdp_growth_1998        — IMF WEO April 1999 outturn (-10.51%)
      unemployment_rate_1997 — World Bank WDI 1997 vintage (ILO-modelled, 1.5%)
      unemployment_rate_1998 — World Bank WDI 1998 vintage (ILO-modelled, 3.4%;
                               see known limitation note above re: understatement)
    """

    gdp_growth_1997: Decimal = Decimal("-0.014")
    gdp_growth_1998: Decimal = Decimal("-0.105")

    # WDI ILO-modelled estimates — structural undercount documented above
    unemployment_rate_1997: Decimal = Decimal("0.015")
    unemployment_rate_1998: Decimal = Decimal("0.034")


ACTUALS = ThailandActuals()


@dataclass(frozen=True)
class FidelityThresholds:
    """Thailand 1997–2000 DIRECTION_ONLY fidelity thresholds.

    DIRECTION_ONLY: asserts that simulated gdp_growth is negative at
    steps 1 and 2, matching the documented historical contraction in
    1997 (-1.4%) and 1998 (-10.5%).

    No magnitude accuracy is asserted. A structurally correct simulation
    must predict contraction under the combination of currency peg
    abandonment (capital controls, July 2, 1997), fiscal tightening,
    and IMF program acceptance — all of which the fixture injects.

    Threshold seeded into backtesting_thresholds as case_id='THAILAND_1997_2000'
    (migration e1c9d7f5b3a2).
    """

    gdp_direction_step1_correct: bool = True
    gdp_direction_step2_correct: bool = True


THRESHOLDS = FidelityThresholds()
