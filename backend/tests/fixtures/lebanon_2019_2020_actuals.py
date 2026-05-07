"""Lebanon 2019–2020 financial collapse — historical actuals and thresholds.

Sources:
  IMF World Economic Outlook April 2020 (2019 GDP outturn):
      gdp_growth_2019 = -6.9%  (rounded from -6.92%)
  IMF World Economic Outlook April 2021 (2020 GDP outturn):
      gdp_growth_2020 = -21.4% (rounded from -21.40%)
  World Bank World Development Indicators (2019 vintage, ILO-modelled estimate):
      unemployment_rate_2019 = 11.4%
  World Bank World Development Indicators (2020 vintage, ILO-modelled estimate):
      unemployment_rate_2020 = 11.7%

Data provenance:
  IMF WEO data is public domain data published by the International Monetary Fund.
  World Bank WDI unemployment figures use ILO-modelled estimates, published under
  the CC BY 4.0 International license. Both sources comply with the open-licensed
  data requirement in CLAUDE.md §Equitable Build Process.

Known limitation on unemployment actuals:
  Official ILO-modelled unemployment figures (11.4%–11.7%) significantly
  understate the labour market collapse in Lebanon 2020. The informal sector,
  which accounts for a large share of Lebanese employment, is structurally
  undercounted in formal statistics. ESCWA (2020) estimates effective
  unemployment and underemployment combined exceeded 40% in 2020. The official
  WDI figures are retained here for source consistency; users should interpret
  the unemployment rate with this caveat.

DIRECTION_ONLY thresholds — same rationale as Greece and Argentina (ADR-004 Decision 3):
magnitude calibration is deferred until DISTRIBUTION_COMBINED thresholds
(Issue #194 infrastructure) are populated with calibrated uncertainty bands.

Lebanon exhibits cascade dynamics (banking → currency → economic → social)
that make it a future validation case for the CASCADE propagation mode (#29)
once implemented. See test_lebanon_2019_2020.py for the forward-reference note.
"""
from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal

from app.simulation.repositories.quantity_serde import IA1_CANONICAL_PHRASE

IA1_DISCLOSURE: str = IA1_CANONICAL_PHRASE

PARAMETER_CALIBRATION_DISCLOSURE: str = (
    "Lebanon 2019–2020 thresholds are DIRECTION_ONLY — magnitude accuracy "
    "is not asserted. DISTRIBUTION_COMBINED thresholds require calibrated "
    "parameter uncertainty bands; infrastructure is in place (Issue #194) but "
    "calibration is deferred to a future milestone. "
    "The 2020 GDP collapse (-21.4%) is among the worst in modern economic history "
    "and involves cascade dynamics (banking system → currency → real economy → "
    "social fabric) that the M6 simulation does not yet fully model. "
    "See DATA_STANDARDS.md Known Limitation."
)


@dataclass(frozen=True)
class LebanonActuals:
    """Historical outturn values for Lebanon 2019–2020.

    GDP growth rates are expressed as ratios (e.g. -0.069 = -6.9%).
    Unemployment rates are expressed as ratios (e.g. 0.114 = 11.4%).

    Sources:
      gdp_growth_2019       — IMF WEO April 2020 outturn (-6.92%)
      gdp_growth_2020       — IMF WEO April 2021 outturn (-21.40%)
      unemployment_rate_2019 — World Bank WDI 2019 vintage (ILO-modelled, 11.4%)
      unemployment_rate_2020 — World Bank WDI 2020 vintage (ILO-modelled, 11.7%;
                               see known limitation note above re: understatement)
    """

    gdp_growth_2019: Decimal = Decimal("-0.069")
    gdp_growth_2020: Decimal = Decimal("-0.214")

    # WDI ILO-modelled estimates — official figures, structural undercount noted above
    unemployment_rate_2019: Decimal = Decimal("0.114")
    unemployment_rate_2020: Decimal = Decimal("0.117")


ACTUALS = LebanonActuals()


@dataclass(frozen=True)
class FidelityThresholds:
    """Lebanon 2019–2020 DIRECTION_ONLY fidelity thresholds.

    DIRECTION_ONLY: asserts that simulated gdp_growth is negative at
    steps 1 and 2, matching the documented historical contraction in
    2019 (-6.9%) and 2020 (-21.4%).

    No magnitude accuracy is asserted. A structurally correct simulation
    must predict contraction under the combination of bank deposit freeze
    (capital controls), fiscal collapse, and compound crisis (sovereign
    default + Beirut port explosion) — all of which the fixture injects.

    Threshold seeded into backtesting_thresholds as case_id='LEBANON_2019_2020'
    (migration d4b8f3a2e7c1).
    """

    gdp_direction_step1_correct: bool = True
    gdp_direction_step2_correct: bool = True


THRESHOLDS = FidelityThresholds()
