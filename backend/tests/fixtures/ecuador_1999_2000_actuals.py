"""Ecuador 1999–2000 dollarization crisis — historical actuals and thresholds.

Sources:
  IMF World Economic Outlook October 1999 (1999 GDP outturn):
      gdp_growth_1999 = -6.3%  (rounded from -6.27%)
  IMF World Economic Outlook April 2001 (2000 GDP outturn):
      gdp_growth_2000 = +2.8%  (rounded from +2.80%)
  World Bank World Development Indicators (1999 vintage, INEC / ILO-modelled):
      unemployment_rate_1999 = 14.4%
  World Bank World Development Indicators (2000 vintage, INEC / ILO-modelled):
      unemployment_rate_2000 = 14.1%

Data provenance:
  IMF WEO data is public domain data published by the International Monetary Fund.
  World Bank WDI unemployment figures use ILO-modelled estimates sourced from
  Ecuador's National Statistics Institute (INEC), published under the CC BY 4.0
  International license. Both sources comply with the open-licensed data
  requirement in CLAUDE.md §Equitable Build Process.

Known limitation on unemployment actuals:
  Ecuador's formal unemployment figures significantly understate labour market
  distress during the 1999 crisis. A large share of the workforce is in informal
  and agricultural employment, with widespread underemployment that official
  unemployment statistics do not capture. The CEPAL / ECLAC assessment of
  effective labour market deterioration in 1999 substantially exceeds the
  formal 14.4% figure. This is documented as a model blind spot.

Structural note on step 2 (2000) recovery:
  Ecuador's 2000 GDP recovery (+2.8%) was driven by dollarization (January 2000),
  which ended hyperinflation and restored monetary stability, combined with
  rising oil prices (Ecuador is a significant oil exporter) and post-crisis
  rebound effects. The M6 simulation's MacroeconomicModule does not model
  dollarization stabilization effects directly — the step 2 threshold is
  therefore designed as 'not deeper than step 1' rather than asserting positive
  recovery. Full dollarization stabilization modeling requires a StructuralModule
  capable of reading institutional reform events (Issue #29 area).

DIRECTION_ONLY thresholds — Ecuador is the first backtesting case where
the fidelity gate applies to step 1 contraction only. Step 2 is assessed
as 'not deeper contraction' (step2 GDP >= step1 GDP) rather than negative
direction, reflecting the historical recovery dynamic that the M6 simulation
does not yet fully model.
"""
from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal

from app.simulation.repositories.quantity_serde import IA1_CANONICAL_PHRASE

IA1_DISCLOSURE: str = IA1_CANONICAL_PHRASE

PARAMETER_CALIBRATION_DISCLOSURE: str = (
    "Ecuador 1999–2000 thresholds are DIRECTION_ONLY — magnitude accuracy "
    "is not asserted. The step 1 contraction threshold asserts that simulated "
    "GDP is negative (-6.3% historical). The step 2 threshold asserts 'not "
    "deeper contraction' (step2 >= step1), reflecting the historical recovery "
    "(+2.8% actual) that the M6 simulation does not yet fully model. "
    "DISTRIBUTION_COMBINED thresholds require calibrated uncertainty bands; "
    "infrastructure is in place (Issue #194) but calibration is deferred. "
    "Dollarization stabilization effects (monetary credibility, inflation "
    "termination, fiscal discipline signal) are not captured by "
    "MacroeconomicModule — structural reform modeling is deferred to a "
    "future milestone. See DATA_STANDARDS.md Known Limitation."
)


@dataclass(frozen=True)
class EcuadorActuals:
    """Historical outturn values for Ecuador 1999–2000.

    GDP growth rates are expressed as ratios (e.g. -0.063 = -6.3%).
    Unemployment rates are expressed as ratios (e.g. 0.144 = 14.4%).

    Note: gdp_growth_2000 is POSITIVE — Ecuador recovered after dollarization.
    This makes Ecuador the first backtesting case with a recovery at step 2.

    Sources:
      gdp_growth_1999        — IMF WEO October 1999 outturn (-6.27%)
      gdp_growth_2000        — IMF WEO April 2001 outturn (+2.80%)
      unemployment_rate_1999 — World Bank WDI 1999 vintage (INEC/ILO-modelled, 14.4%)
      unemployment_rate_2000 — World Bank WDI 2000 vintage (INEC/ILO-modelled, 14.1%;
                               see known limitation note above re: understatement)
    """

    gdp_growth_1999: Decimal = Decimal("-0.063")
    gdp_growth_2000: Decimal = Decimal("0.028")   # POSITIVE — recovery year

    # INEC / ILO-modelled estimates — structural undercount documented above
    unemployment_rate_1999: Decimal = Decimal("0.144")
    unemployment_rate_2000: Decimal = Decimal("0.141")


ACTUALS = EcuadorActuals()


@dataclass(frozen=True)
class FidelityThresholds:
    """Ecuador 1999–2000 DIRECTION_ONLY fidelity thresholds.

    Ecuador is structurally different from Greece, Argentina, Lebanon, and
    Thailand: step 2 shows RECOVERY (+2.8%) rather than continued contraction.

    Two thresholds:
      gdp_direction_step1_correct:
        DIRECTION_ONLY: step 1 GDP must be negative (1999 contraction: -6.3%).
      gdp_step2_not_deeper_than_step1:
        RECOVERY GATE: step 2 GDP must be >= step 1 GDP (not further contraction).
        The M6 simulation cannot model dollarization stabilization dynamics
        directly, so the gate is set to 'not worse' rather than asserting
        positive recovery. Satisfies 'at minimum not deeper contraction'.

    Threshold seeded into backtesting_thresholds as case_id='ECUADOR_1999_2000'
    (migration f8a3c7e2d1b5).
    """

    gdp_direction_step1_correct: bool = True
    gdp_step2_not_deeper_than_step1: bool = True


THRESHOLDS = FidelityThresholds()
