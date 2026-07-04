---
name: M19-CMB-lac-elasticity-calibration
type: implementation-intent
adr: ADR-005 Decision 1 (DemographicModule ELASTICITY_REGISTRY)
issues: "#1623"
status: Filed
authored-by: Chief Methodologist
authored-date: 2026-07-03
implementing-agent: Chief Methodologist
sprint-entry: docs/process/sprint-plans/m19-cm-b-sprint-entry.md
---

# Implementation Intent: M19 CM Sprint B — LAC Elasticity Calibration (#1623)

> **Calibration sprint — no ADR.** This intent covers Gap 2 of Issue #1623: installing
> ELASTICITY_REGISTRY entries for Latin American and Caribbean programme countries
> (ARG, ECU, BOL, PER entity family priority). This is a calibration constant revision
> within the existing DemographicModule architecture established by ADR-005 Decision 1 —
> the same classification as M17-G1 and M19 CM Sprint A.
>
> **Intent gate structure:** This document satisfies Step 1 of the agent execution lifecycle.
> The CM calibration decision document (`docs/calibration/m19-cm-b-lac-calibration-decision.md`)
> is a separate artifact filed after research and before implementation. It closes the
> PENDING gate in sprint entry §2.4 and is the specification the integration test is authored from.
>
> **NM-084 compliance:** The Chief Methodologist is the implementing agent for this sprint.
> Before the implementation PR opens, the CM must post a formal methodological certification
> comment on Issue #1623 certifying the chosen constants and source quality. The PI Agent must
> then post a gate comment confirming sign-off is on record before auto-merge is set.

---

## 1. Source

**Issue:** #1623 — ELASTICITY_REGISTRY non-SSA entity family calibration gap (Gap 2: LAC)

**ADR reference:** ADR-005 Decision 1 — DemographicModule ELASTICITY_REGISTRY architecture.
No new ADR required. New entries use the existing `CohortElasticity` dataclass (now with
`entity_families: frozenset[str] | None` field added in CM Sprint A) and follow the
`source_registry_id` naming convention in `docs/DATA_STANDARDS.md §Data Provenance Requirements`.

**Authored by:** Chief Methodologist
**Date:** 2026-07-03
**Implementing agent:** Chief Methodologist

**Background:** CM Sprint A (2026-07-03) delivered the `entity_families` scoping field and
Euro area (GRC) calibration. Gap 2 targets Latin American and Caribbean programme countries.
The current ELASTICITY_REGISTRY applies SSA-calibrated informal-sector entries
(Fosu 2011, -0.20 for Q1 INFORMAL, entity_families=None) to ALL entities including
ARG/ECU/BOL/PER. For LAC countries this produces two structural problems:

1. **Wrong cohort as primary transmission channel.** The SSA calibration targets Q1
   INFORMAL workers as the primary vulnerable cohort — appropriate for SSA LIC economies
   where subsistence agriculture and informal petty trade are the main poverty-exposure
   channels. For LAC programme episodes the primary vulnerable cohort is formal sector
   workers: Argentina 2001 currency collapse destroyed formal-sector savings and employment;
   Ecuador 1999 banking crisis freeze (salvazo) hit formal-sector depositors hardest; Bolivia
   and Peru structural adjustments of the 1980s-90s transmitted primarily through public-sector
   and formal-sector employment cuts.

2. **Wrong elasticity reference for informal sector.** The M17-G1 SSA recalibration
   explicitly doubled the prior -0.10 calibration (which was derived from Lustig 2017
   Latin American episodes) to -0.20 because SSA poverty-growth elasticities are 1.5–2×
   larger than LAC comparators at equivalent inequality levels (Fosu 2011; Ravallion 2012).
   The SSA entry comment documents this provenance directly. Applying the SSA-calibrated
   -0.20 to LAC entities reverses the calibration reasoning — it is equivalent to applying
   the doubled value back to the population it was doubled from.

---

## 2. Persona Trace Elements Targeted

> *Calibration infrastructure with no new UI element. Forward trace: calibration change →
> Argentina 2001-2002 counter-factual (G2C #1548) and Ecuador 1999-2000 backtesting
> produce MAGNITUDE-class human development trajectory divergence between orthodox and
> heterodox fiscal paths, rather than DIRECTION_ONLY advisory assessments.*

| Persona | Use case | Forward-trace claim |
|---|---|---|
| Persona 2 (Finance ministry, programme country) | Scenario analysis — LAC IMF programme | Bolivian or Peruvian analyst can show calibrated cohort welfare impact from orthodox vs heterodox adjustment path grounded in LAC-specific literature rather than SSA proxy |
| Persona 5 (Researcher) | Historical backtesting | Argentina 2001-2002 Type B counter-factual produces defensible HD-composite magnitude divergence |
| Persona 3 (Negotiating team) | Counter-factual comparison | Counter-factual between IMF programme path and heterodox lower-adjustment path shows LAC-calibrated formal-sector poverty response, not SSA proxy |

---

## 3. Architecture

**No new architecture.** The `entity_families` field was added to `CohortElasticity` in
CM Sprint A (`docs/calibration/m19-cm-a-euro-area-calibration-decision.md §1.2`). CM Sprint B
uses the identical mechanism: new `CohortElasticity` instances with
`entity_families=frozenset({"ARG", "ECU", "BOL", "PER"})` appended to `ELASTICITY_REGISTRY`.

**Cohort targets:** LAC formal-sector vulnerability pattern is analogous to GRC (CM Sprint A)
but literature basis differs:
- GRC entries: Blanchard & Leigh (2013) + Eurostat AROPE fiscal multiplier evidence
- LAC entries: Lustig (2017) CEQ assessments + Gasparini & Lustig (2011) distributional
  impact of Argentina crisis + ECLAC poverty data for ECU/BOL/PER programme episodes

**Formal sector primary channel:** CM Sprint A established that formal-sector calibration
is appropriate when the primary transmission mechanism is employment-destruction rather than
subsistence-income loss. LAC programme episodes fit this profile. The DemographicModule
existing filter (`if row.entity_families is not None and entity.id not in row.entity_families: continue`)
ensures SSA entries continue to fire on SSA entities only — but SSA entries currently have
`entity_families=None` so they fire on ALL entities. The LAC entries are ADDITIVE to the SSA
INFORMAL entries unless the calibration decision specifies otherwise.

**Design question requiring calibration decision resolution:** The CM calibration decision
document must address whether:
- (a) LAC entries target FORMAL sector cohorts only (additive; SSA informal entries continue to
  fire on LAC Q1 INFORMAL at SSA-calibrated magnitude), OR
- (b) LAC INFORMAL entries are also added, accepting that LAC Q1 INFORMAL will receive
  BOTH the SSA entry's delta AND the LAC-specific delta (summed effect), OR
- (c) A mechanism to prevent the SSA Q1 INFORMAL entry from firing on LAC entities is designed

Option (a) is the minimum-scope approach and is consistent with CM Sprint A precedent (GRC
formal sector entries only). Option (c) requires modifying existing SSA entries or adding
a DemographicModule entity-family exclusion mechanism — broader scope than a calibration sprint.
The CM calibration decision document resolves this choice.

---

## 4. Acceptance Criteria

### AC-1: MAGNITUDE divergence (integration test, DATABASE_URL required)

For ARG Type B counter-factual (orthodox vs heterodox fiscal path), the `hd_composite`
divergence at step 3 (mid-crisis) satisfies:

```
lower_bound <= per_step_diff[2] <= upper_bound
```

Bounds TBD in calibration decision document. These are the bounds that will certify the
LAC calibration is producing a detectable, non-trivial, non-overfit response on the HD
composite scale.

### AC-2: LAC entries present with correct scoping

At least 2 entries in `ELASTICITY_REGISTRY` with:
- `entity_families` is not None
- `"ARG" in entry.entity_families` (or ECU, BOL, PER — all must be in the frozenset)
- `attribute_key == "poverty_headcount_ratio"`

### AC-3: LAC FORMAL entry values

For the primary LAC Q1 FORMAL entry:
- `event_type == "gdp_growth_change"`
- `cohort_spec.income_quintile == IncomeQuintile.Q1`
- `cohort_spec.employment_sector == EmploymentSector.FORMAL`
- `elasticity == <TBD in calibration decision>`
- `confidence_tier == 3` (T3 — LAC regional inference; T2 upgrade requires country-level backtesting)

### AC-4: SSA non-regression

The four SSA entries from M17-G1 and CM Sprint A GRC entries are unchanged:
- SSA Q1 INFORMAL elasticity == Decimal("-0.20")
- SSA Q2 INFORMAL elasticity == Decimal("-0.133")
- SSA Q1 AGRICULTURE elasticity == Decimal("-0.16")
- ADR-020 Channel C (credit_contraction) elasticity == Decimal("-0.30")
- GRC Q1 FORMAL elasticity == Decimal("-0.25")
- GRC Q2 FORMAL elasticity == Decimal("-0.15")
- All above `entity_families` values unchanged

### AC-5: Cross-contamination guard

The new LAC-scoped entries must not fire on SSA entities. For `entity_id="SEN"`:
```python
lac_entries_for_sen = [
    e for e in ELASTICITY_REGISTRY
    if e.entity_families is not None and "SEN" in e.entity_families
]
assert len(lac_entries_for_sen) == 0
```

---

## 5. Forward Condition

The AC-1 harness live run (GRC orthodox vs heterodox `hd_composite` divergence) requires
a live DATABASE_URL. This condition is classified as a "forward condition for Demo 8"
(same classification as CM Sprint A). Unit tests (AC-2 through AC-5) fully certify the
implementation. The full magnitude validation runs at Demo 8 Act 2.

---

## 6. Issue #1657 Coordination

Issue #1657 (DemographicModule dead event subscriptions) is unblocked by CM Sprint A.
CM Sprint B must not conflict with any #1657 implementation PR that opens between Sprint A
confirmation and Sprint B completion. The `entity_families` field syntax is already available.
A co-dependent fixture issue does not apply here — Sprint B and #1657 target separate files
and separate registry entries.

---

*Intent document authority: sprint-planning-sop.md §Sprint Entry Gate (Step 1).
Sprint entry: `docs/process/sprint-plans/m19-cm-b-sprint-entry.md` (to be filed concurrently).
Author: Chief Methodologist. Date: 2026-07-03.*
