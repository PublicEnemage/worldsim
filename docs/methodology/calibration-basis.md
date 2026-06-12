# WorldSim — Propagation Parameter Calibration Basis

> Status: Partial calibration — see Issue #44 for full calibration tier system.
> Author: Documentation Agent (M13 G4 — Issue #27)
> Covers parameters in `backend/app/simulation/modules/macroeconomic/module.py`
> and `backend/app/simulation/orchestration/inputs.py`.

---

## Purpose

This document records the calibration basis for the top-level propagation
parameters used in WorldSim's simulation engine. It serves three functions:

1. **Transparency** — a non-technical reviewer can trace a parameter value to
   its claimed empirical basis without reading source code.
2. **Calibration audit** — parameters marked PLACEHOLDER require empirical
   calibration before the engine produces cite-ready outputs in that domain.
3. **Backtesting anchor** — calibrated parameters can be compared against
   historical out-of-sample performance. Placeholder parameters should be
   recalibrated once backtesting data is available.

---

## Fiscal Sector Parameters

### `FISCAL_MULTIPLIERS` — Spending multipliers by economic regime

**Location:** `backend/app/simulation/modules/macroeconomic/module.py` line ~53

| Regime | Value | Basis |
|--------|-------|-------|
| `standard` | 0.5 | Ball, Leigh & Loungani (2019), "Okun's Law: Fit at 50?"; Loayza & Raddatz (2010), "The composition of growth matters for poverty alleviation." Cross-country average for developing economies. |
| `depressed` | 1.5 | Blanchard & Leigh (2013), "Growth Forecast Errors and Fiscal Multipliers"; elevated multiplier in demand-deficient regimes. |
| `zlb` | 2.0 | Christiano, Eichenbaum & Rebelo (2011), "When Is the Government Spending Multiplier Large?"; elevated fiscal multiplier at the zero lower bound. |

**Calibration status:** CALIBRATED (published estimates). Full country-specific
recalibration deferred to Issue #44.

---

### `OKUN_COEFFICIENT` — GDP growth → unemployment transmission

**Location:** `backend/app/simulation/modules/macroeconomic/module.py` line ~70

**Value:** `0.5`

**Basis:** Ball, Leigh & Loungani (2019); Loayza & Raddatz (2010). Developing-economy
estimate for the one-period transmission from 1 percentage point change in GDP
growth to 0.5 percentage point change in unemployment (opposite direction).

**Calibration status:** CALIBRATED (developing-economy cross-country average).
Country-specific recalibration deferred to Issue #44.

---

### `REVERSION_SPEED` — Mean-reversion speed in GDP growth (ADR-006 Amendment 1)

**Location:** `backend/app/simulation/modules/macroeconomic/module.py` line ~81

**Value:** `0.10` (10% per year reversion toward long-run growth rate)

**Basis:** Cerra & Saxena (2008), "Growth Dynamics: The Myth of Economic Recovery."
Estimate based on post-crisis output trajectories in developed economies. This
is an upper bound for developing economies where recovery is typically slower.

**Calibration status:** CALIBRATED for developed economies (Cerra-Saxena 2008).
PLACEHOLDER for individual country trajectories — see Issue #44.

---

### `REGIME_DAMPENER` — Recovery speed scalar by economic regime

**Location:** `backend/app/simulation/modules/macroeconomic/module.py` line ~86

| Regime | Value | Basis |
|--------|-------|-------|
| `zlb` | 0.25 | Reinhart & Rogoff (2009), "This Time Is Different"; median time to recover pre-crisis output ≈7 years following sovereign debt crises. |
| `depressed` | 0.50 | Partial channel active — moderate crisis, no debt restructuring required. |
| `standard` | 1.00 | Full reversion speed applies. |

**Calibration status:** CALIBRATED at regime level (Reinhart-Rogoff 2009).
Country-specific dampener calibration deferred to Issue #44.

---

## Human Cost Ledger Parameters

### `_HCL_TRANSMISSION_FACTOR` — Shock-to-human-development transmission rate

**Location:** `backend/app/simulation/orchestration/inputs.py` line ~1026

**Value:** `0.3`

**Basis:** PLACEHOLDER. This factor scales how much of a commodity price shock
transmits to the bottom-quintile consumption capacity indicator. The 0.3 value
is an interim estimate pending calibration against LSMS household survey data.

Candidate calibration sources:
- World Bank Living Standards Measurement Study (LSMS) — food price pass-through
  to household consumption for developing economies
- FAO food price crisis impact assessments (2008, 2011)
- IMF Working Paper WP/16/218 (Furceri, Loungani, Ostry 2016) — distributional
  consequences of commodity price shocks

**Calibration status:** PLACEHOLDER — empirical calibration required before
the human cost ledger output is cite-ready at Tier 1–2. Current output is
Tier 3 (directionally correct; specific magnitude uncertain).

---

## Propagation Network Parameters

### Synthetic relationship weight — fallback for unregistered entity pairs

**Location:** `backend/app/simulation/repositories/state_repository.py` line ~32

**Value:** `0.1` (weight=0.1, confidence_tier=4)

**Basis:** Conservative placeholder. When two entities in a scenario have no
registered bilateral trade or institutional relationship in the database, the
engine injects a synthetic weak relationship at weight 0.1 and confidence tier 4
to prevent zero propagation. The 0.1 weight reflects a "minimal but non-zero
connectivity" assumption for economies with no observed relationship.

**Calibration status:** PLACEHOLDER — specific pairs should be registered with
empirical trade weight data from UN Comtrade or IMF DOTS when available.

---

## Relationship to Issue #44 (Full Calibration Tier System)

Issue #44 tracks the full calibration tier system for all propagation parameters.
Parameters marked PLACEHOLDER in this document are blocking for Tier 1–2
analytical outputs in the domains they affect. Parameters marked CALIBRATED
carry their cited empirical basis but have not been individually validated
against the WorldSim backtesting suite for out-of-sample performance.

Out-of-sample validation against historical cases is the primary calibration
signal — see `docs/DATA_STANDARDS.md §Backtesting Integrity Rules`.
