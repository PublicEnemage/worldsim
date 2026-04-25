"""Greece 2010–2012 IMF Program — historical actuals and fidelity thresholds.

Sources:
  - IMF World Economic Outlook April 2013 (outturn data for 2010–2012):
      gdp_growth_2010/2011/2012
  - Eurostat Labour Force Survey (Q1 vintage, EUROSTAT_LFS_2010):
      unemployment_rate_2010  — Q1 2010 = 12.7%
      unemployment_rate_2011  — Q1 2011 = 14.9%
      unemployment_rate_2012  — Q1 2012 = 24.5%
      unemployment_rate_2013  — Q1 2013 = 27.5% (within fixture window;
                                labelled 2013 because step 3 projects the
                                2012→2013 annual period)

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
    """Historical outturn values for Greece 2010–2012.

    GDP growth rates are expressed as ratios (e.g. -0.054 = -5.4%).
    Unemployment rates are expressed as ratios (e.g. 0.127 = 12.7%).

    Sources:
      gdp_growth_* — IMF World Economic Outlook April 2013
      unemployment_rate_* — Eurostat Labour Force Survey Q1 vintage
        (Q1 snapshots used to align with EUROSTAT_LFS_2010 initial state;
        step 3 / unemployment_rate_2013 is extrapolated within the fixture
        window as no post-2012 Q1 data was available at fixture creation time)
    """

    gdp_growth_2010: Decimal = Decimal("-0.054")
    gdp_growth_2011: Decimal = Decimal("-0.089")
    gdp_growth_2012: Decimal = Decimal("-0.066")

    # Eurostat LFS Q1 snapshots — aligns with EUROSTAT_LFS_2010 initial state
    unemployment_rate_2010: Decimal = Decimal("0.127")
    unemployment_rate_2011: Decimal = Decimal("0.149")
    unemployment_rate_2012: Decimal = Decimal("0.245")
    unemployment_rate_2013: Decimal = Decimal("0.275")


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

    unemployment_direction_step0_to_step3: asserts that unemployment at step 3
    exceeds the empirically grounded initial value (step 0 = 12.7% from
    EUROSTAT_LFS_2010). This replaces the vacuous step1→step3 check that
    existed when no initial unemployment value was seeded (Issue #149).

    Threshold type rationale: parameter calibration tier system not yet
    implemented (Issue #44). MAGNITUDE thresholds require calibration tier A/B
    per STD-REVIEW-002 SA-02 and are deferred to Milestone 4.
    """

    gdp_direction_correct: bool = True
    unemployment_direction_step0_to_step3: bool = True


THRESHOLDS = FidelityThresholds()
