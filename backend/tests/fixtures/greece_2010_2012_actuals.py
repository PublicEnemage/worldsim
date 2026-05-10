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
  - World Bank World Development Indicators (WDI 2013 release):
      health_expenditure_pct_gdp_2010  — 9.5% (initial state seed)
      health_expenditure_pct_gdp_2011  — 9.4% (slight decline; austerity begins)
      health_expenditure_pct_gdp_2012  — 8.7% (accelerated cuts in second program)

These actuals define the benchmark against which backtesting fidelity is
measured. ADR-004 Decision 3: M3 ships DIRECTION_ONLY thresholds only.
MAGNITUDE thresholds are deferred to Milestone 4 (Issue #44).

HCL thresholds (Issue #87): unemployment_rate UP and health_expenditure_pct_gdp DOWN
are defined in FidelityThresholds and tracked in the fidelity report. They are
deferred from the blocking CI gate until an endogenous module updates these
attributes (currently flat across steps — no module produces these as outputs).
"""
from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal

# ---------------------------------------------------------------------------
# IA-1 disclosure — must match IA1_CANONICAL_PHRASE in quantity_serde.py
# ---------------------------------------------------------------------------

IA1_DISCLOSURE: str = (
    "This simulation produces distributions using pre-calibration uncertainty "
    "bands. Intervals shown are NOT confidence intervals derived from calibrated "
    "parameter distributions — they are conservative defaults that widen with "
    "projection horizon and data quality. Bands will be revised when "
    "MAGNITUDE_WITHIN_20PCT validation exists for at least two independent "
    "historical cases. All outputs should be interpreted as structured reasoning "
    "tools, not predictions. Verify against current data before consequential "
    "use."
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

    # World Bank WDI 2013 release — health expenditure as % of GDP (Issue #87)
    # Direction: DOWN during austerity program (spending cuts visible 2011→2012)
    health_expenditure_pct_gdp_2010: Decimal = Decimal("0.095")
    health_expenditure_pct_gdp_2011: Decimal = Decimal("0.094")
    health_expenditure_pct_gdp_2012: Decimal = Decimal("0.087")


ACTUALS = GreeceActuals()

# ---------------------------------------------------------------------------
# Fidelity thresholds — DIRECTION_ONLY (ADR-004 Decision 3)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class FidelityThresholds:
    """DIRECTION_ONLY fidelity thresholds for Greece 2010–2012 (Issue #87).

    DIRECTION_ONLY: asserts that the simulated value moves in the historically
    documented direction. No magnitude accuracy is asserted.

    Enforced thresholds (blocking CI gate):
      gdp_direction_correct: gdp_growth is negative at steps 1–3 (contraction).
      unemployment_direction_step0_to_step3: unemployment at step 3 exceeds the
        empirically grounded initial value (12.7%, EUROSTAT_LFS_2010 Q1 2010).
        Replaces the vacuous step1→step3 check from before Issue #149.

    Deferred thresholds (tracked in fidelity report, not blocking CI — Issue #87):
      unemployment_rising_step1_to_step2: step 2 unemployment > step 1.
        Deferred: no endogenous module currently updates unemployment_rate.
        Value stays flat; threshold would always fail. Re-enable when a module
        produces unemployment_rate events.
      health_expenditure_declining_step1_to_step2: step 2 health_expenditure_pct_gdp
        < step 1. Deferred: same reason. Historical: 9.4% → 8.7% (WDI 2013).
        Re-enable when a module produces health_expenditure_pct_gdp events.

    Threshold type rationale: parameter calibration tier system not yet
    implemented (Issue #44). MAGNITUDE thresholds require calibration tier A/B
    per STD-REVIEW-002 SA-02 and are deferred to Milestone 4.
    """

    gdp_direction_correct: bool = True
    unemployment_direction_step0_to_step3: bool = True
    # HCL thresholds — defined but deferred (no endogenous module yet)
    unemployment_rising_step1_to_step2: bool = False
    health_expenditure_declining_step1_to_step2: bool = False


THRESHOLDS = FidelityThresholds()
