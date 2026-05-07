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

M6 MAGNITUDE status — partial implementation per feasibility assessment
(migration a3d9e7c2f4b1, Issues #208/#210):
  Step 2 achieves MAGNITUDE_WITHIN_20PCT. Steps 1, GRC 2, GRC 3 deferred to M7.
  See MAGNITUDE_CALIBRATION_NOTE below.
"""
from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal

from app.simulation.repositories.quantity_serde import IA1_CANONICAL_PHRASE

IA1_DISCLOSURE: str = IA1_CANONICAL_PHRASE

PARAMETER_CALIBRATION_DISCLOSURE: str = (
    "Argentina 2001–2002 partial MAGNITUDE calibration (M6, Issues #208/#210): "
    "step 2 achieves MAGNITUDE_WITHIN_20PCT at 3.2% deviation (model −10.55% vs "
    "actual −10.9%), seeded by migration a3d9e7c2f4b1. "
    "Step 1 remains DIRECTION_ONLY — structural gap (one-step lag, Issue #222, M7). "
    "Greece steps 2–3 remain DIRECTION_ONLY — structural gap (accumulation without "
    "mean reversion, Issue #221, M7). "
    "See MAGNITUDE_CALIBRATION_NOTE for full root-cause analysis."
)

MAGNITUDE_CALIBRATION_NOTE: str = (
    "MAGNITUDE calibration status for Argentina 2001–2002 and Greece 2010–2012 "
    "(feasibility assessment: commit a3d9e7c2f4b1 context, Issues #208/#210):\n"
    "\n"
    "PASSES — ARG step 2 (2002): model −10.55% vs actual −10.9% → 3.2% deviation.\n"
    "  Mechanism: MacroeconomicModule depressed-regime multiplier (1.5) applied to\n"
    "  Zero Deficit Plan spending cut (−6.5% of GDP) on initial gdp_growth of −0.8%.\n"
    "  formula: gdp_delta = −0.065 × 1.5 = −0.0975; new = −0.008 + (−0.0975) = −0.1055.\n"
    "  This is a structural coincidence of correctly-calibrated inputs — not overfitting.\n"
    "  Tolerance band: ±20% of |−0.109| → [−0.1308, −0.0872]. Model at −0.1055 is inside.\n"
    "\n"
    "DEFERRED — ARG step 1 (2001): model −0.8% vs actual −4.4% → 82% deviation.\n"
    "  Cause: one-step lag. Zero Deficit Plan fires as events at step 1 but\n"
    "  MacroeconomicModule only processes prior-step events — at step 1 there are none.\n"
    "  Model reports the initial seed (2000 recession baseline) while the actual 2001\n"
    "  contraction reflects the contemporaneous real-world shock effect. Not fixable\n"
    "  by parameter calibration. M7 Issue #222: Engineering Lead decision required\n"
    "  (Option A: contemporaneous path; B: revised seeding; C: permanent DIRECTION_ONLY).\n"
    "\n"
    "DEFERRED — GRC step 2 (2011): model −21.4% vs actual −8.9% → 140% deviation.\n"
    "DEFERRED — GRC step 3 (2012): model −31.4% vs actual −6.6% → 376% deviation.\n"
    "  Cause: gdp_growth is a pure accumulation stock — it only moves when a fiscal\n"
    "  event fires and never receives an endogenous recovery impulse. The Greek economy\n"
    "  improved from −8.9% to −6.6% without a positive fiscal shock in the fixture.\n"
    "  The model cannot reproduce improvement without a positive impulse. The required\n"
    "  ZLB multiplier to match step 2 would be 0.22–0.66 — below the standard multiplier\n"
    "  (0.5), contradicting the regime hierarchy. M7 Issue #221: mean-reversion channel\n"
    "  in MacroeconomicModule required (Chief Methodologist + Chief Engineer joint ADR).\n"
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
