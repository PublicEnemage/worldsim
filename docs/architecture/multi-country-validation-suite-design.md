# Multi-Country Validation Suite Design

**Issue:** #103
**Finding:** ARCH-REVIEW-002 BI2-N-12
**Date:** 2026-06-05
**Ships with:** G6a — multi-country scenario backend (PR targeting release/m12)

---

## Problem Statement

The Greece 2010–2012 backtesting case produces two data points (step 1, step 2). Under a null (uncalibrated) model, the probability of passing both DIRECTION_ONLY thresholds by chance is 25% — two independent sign checks, each with p=0.5. A 25% false-positive rate means one in four random models would pass the M3 backtesting gate.

The current backtesting architecture must be understood as a **plausibility check**, not an empirical validation. Statistical validity requires either: (a) a longer time series (same country, more steps), (b) multiple countries with the same crisis pattern, or (c) both.

This document specifies the multi-country extension plan to bring the backtesting suite to statistical significance.

---

## Statistical Validity Requirement

A directional pass across N independent data points has probability (0.5)^N of occurring by chance. To reach a false-positive rate of ≤ 5%:

| Data points required | Max false-positive rate |
|---|---|
| 1 | 50% |
| 2 (current) | 25% |
| 5 | 3.1% |
| 7 | 0.8% |

**Minimum target:** 5 independent directional checks. This can be achieved through any combination of:
- Additional steps in the Greece case (longer time series)
- Additional sovereign debt crisis cases (same crisis pattern, different countries)
- Both

The preferred approach is both — additional cases improve generalizability, while additional steps within each case improve temporal fidelity.

---

## Candidate Extension Cases

The following sovereign debt crisis cases have the same structural pattern as Greece (fiscal stress → external financing shock → austerity programme → social cost cascade) with documented IMF programme timelines and WEO actuals:

### Case 1 — Ireland 2010–2012

| Field | Value |
|---|---|
| Crisis trigger | Banking sector collapse → sovereign guarantees → fiscal shock |
| Programme start | November 2010 (EU/IMF/EFSF) |
| Programme end | December 2013 |
| Available steps | 3 annual steps (2010, 2011, 2012) |
| IMF WEO data | Readily available; WEO database October 2010 vintage |
| Pattern match to Greece | High — same external adjustment, same fiscal consolidation pressure, same unemployment response |
| Differentiator | Banking channel dominates (vs. debt issuance in Greece); GDP contraction earlier |

**ControlInput sequence:** Fiscal shock 2010 (banking guarantee → primary balance deterioration); structural adjustment 2011–2012 (banking recapitalisation → growth recovery path).

### Case 2 — Portugal 2011–2014

| Field | Value |
|---|---|
| Crisis trigger | Sovereign spreads → market access loss → IMF request |
| Programme start | May 2011 (EU/IMF) |
| Programme end | May 2014 |
| Available steps | 3 annual steps (2011, 2012, 2013) |
| IMF WEO data | WEO April 2011 vintage for baseline; WEO October 2012/2013 for actuals |
| Pattern match to Greece | Very high — same crisis mechanism, same EU/IMF programme structure |
| Differentiator | Faster external adjustment; less severe social cost cascade than Greece |

**ControlInput sequence:** Fiscal shock 2011 (market access loss → austerity programme); structural adjustment 2012–2013; social stabilisation 2014.

### Case 3 — Cyprus 2012–2013

| Field | Value |
|---|---|
| Crisis trigger | Banking sector (overexposure to Greek sovereign debt) → deposit bail-in |
| Programme start | March 2013 (EU/IMF) |
| Programme end | March 2016 |
| Available steps | 2 annual steps (2013, 2014) — shorter timeline |
| IMF WEO data | WEO April 2013 vintage; deposit haircut parameters from troika programme documentation |
| Pattern match to Greece | Moderate — bank channel dominant; deposit bail-in is distinct from Greece |
| Differentiator | Deposit freeze creates unique distributional effects not in the base Greece model |
| Fit for multi-country suite | Conditional — valuable for the banking channel coverage, but the deposit bail-in mechanism may require a new ControlInput type |

**ControlInput sequence:** Bilateral financial shock 2013 (banking sector → sovereign); structural adjustment 2013–2014.

---

## Priority Order

| Priority | Case | Rationale |
|---|---|---|
| 1 | Ireland 2010–2012 | Best pattern match; 3 steps; data readily available; no new ControlInput types needed |
| 2 | Portugal 2011–2014 | Very high pattern match; 3 additional steps; validates the same programme mechanism |
| 3 | Cyprus 2012–2013 | Adds banking channel; may require new ControlInput type — scope as a separate issue |

Ireland + Portugal alone add 6 directional data points to the 2 from Greece — bringing the suite to 8 total, well above the ≤5% false-positive threshold (0.5^8 = 0.4%).

---

## Implementation Plan

### Phase 1 — Ireland case (Target: M12 or M13)

1. Acquire IMF WEO actuals for Ireland 2010–2012 (WEO April 2011, October 2011, October 2012 vintages)
2. Define ControlInput sequence for the banking channel shock (see above)
3. Write fixture: `backend/tests/fixtures/ireland_2010_fixture.py`
4. Write backtesting case: `backend/tests/backtesting/test_ireland_backtesting.py`
5. Set DIRECTION_ONLY thresholds for Ireland — do not reuse Greece thresholds without validation
6. Add Ireland case to CI backtesting job in `ci.yml`

### Phase 2 — Portugal case (Target: M13)

1. Acquire IMF WEO actuals for Portugal 2011–2013
2. Write fixture and backtesting case following the Ireland pattern
3. Add Portugal case to CI backtesting job

### Phase 3 — Statistical reporting (Target: M14)

1. Add a backtesting summary report that computes the false-positive rate across all active cases
2. Report: "N directional checks across M cases; probability of passing by chance: P%"
3. Set a minimum threshold: CI fails if the suite's aggregate false-positive rate exceeds 10% (not yet at 5% target)

---

## Data Requirements

All backtesting fixtures must comply with `docs/DATA_STANDARDS.md`:

| Requirement | Detail |
|---|---|
| Vintage dating | Each fixture must record the WEO vintage used for actuals (e.g. "WEO October 2012") |
| Confidence tier | IMF WEO actuals are Tier 1 where available; model-derived interpolations are Tier 3 |
| Territorial declarations | No contested territories in the Ireland/Portugal/Cyprus cases — standard ISO 3166-1 |
| Open-licensed data | IMF WEO data is publicly available; no proprietary data in fixture files |

---

## Relationship to G6a

This document ships in the same PR as G6a (multi-country scenario backend). The multi-country backend is the prerequisite infrastructure for running multi-entity backtesting scenarios — Ireland and Portugal cases will use the multi-entity path added in G6a to simultaneously run the crisis country alongside a commodity reference entity for external sector shocks.

---

## References

- ARCH-REVIEW-002 BI2-N-12: `docs/architecture/reviews/ARCH-REVIEW-002-milestone2.md`
- Greece backtesting case: `backend/tests/backtesting/`
- DATA_STANDARDS.md §Confidence Tier System
- IMF WEO database: publicly accessible at imf.org/external/datamapper
