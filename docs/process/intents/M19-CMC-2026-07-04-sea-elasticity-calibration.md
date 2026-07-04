---
name: M19-CMC-sea-elasticity-calibration
type: implementation-intent
adr: ADR-005 Decision 1 (DemographicModule ELASTICITY_REGISTRY)
issues: "#1623"
status: Filed
authored-by: Chief Methodologist
authored-date: 2026-07-04
implementing-agent: Chief Methodologist
sprint-entry: docs/process/sprint-plans/m19-cm-c-sprint-entry.md
---

# Implementation Intent: M19 CM Sprint C — South/Southeast Asia Elasticity Calibration (#1623)

> **Calibration sprint — no ADR.** This intent covers Gap 3 of Issue #1623: installing
> ELASTICITY_REGISTRY entries for South and Southeast Asian programme countries
> (PAK, LKA, BGD priority). This is a calibration constant revision within the existing
> DemographicModule architecture established by ADR-005 Decision 1 — the same classification
> as M17-G1, CM Sprint A, and CM Sprint B.
>
> **Intent gate structure:** This document satisfies Step 1 of the agent execution lifecycle.
> The CM calibration decision document (`docs/calibration/m19-cm-c-sea-calibration-decision.md`)
> is a separate artifact filed after research and before implementation. It closes the
> PENDING gate in sprint entry §2.4 and is the specification the integration test is authored from.
>
> **NM-084 compliance:** The Chief Methodologist is the implementing agent for this sprint.
> Before the implementation PR opens, the CM must post a formal methodological certification
> comment on Issue #1623 certifying the chosen constants and source quality. The PI Agent must
> then post a gate comment confirming sign-off is on record before auto-merge is set.

---

## 1. Source

**Issue:** #1623 — ELASTICITY_REGISTRY non-SSA entity family calibration gap (Gap 3: South/SE Asia)

**ADR reference:** ADR-005 Decision 1 — DemographicModule ELASTICITY_REGISTRY architecture.
No new ADR required. New entries use the existing `CohortElasticity` dataclass with the
`entity_families: frozenset[str] | None` field (added in CM Sprint A) and follow the
`source_registry_id` naming convention in `docs/DATA_STANDARDS.md §Data Provenance Requirements`.

**Authored by:** Chief Methodologist
**Date:** 2026-07-04
**Implementing agent:** Chief Methodologist

**Background:** CM Sprint A (GRC, 2026-07-03) and CM Sprint B (ARG/ECU/BOL/PER, 2026-07-04)
delivered the `entity_families` scoping field and Euro area and LAC calibrations respectively.
Gap 3 targets South and Southeast Asian programme countries. The current ELASTICITY_REGISTRY
applies SSA-calibrated informal-sector entries (Fosu 2011, −0.20 for Q1 INFORMAL,
`entity_families=None`) to ALL entities including PAK/LKA/BGD. For South Asian programme
episodes this produces structural problems:

1. **Wrong multiplier basis.** The Fosu (2011) calibration is grounded in SSA income-growth
   elasticity of poverty headcount — appropriate for SSA LIC economies where subsistence
   agriculture and informal petty trade are the main poverty-exposure channels. South Asian
   crisis episodes (Pakistan 2022–23 IMF programme; Sri Lanka 2022 sovereign default) transmit
   through a mix of formal and informal channels, with significant urban professional class
   exposure to import price inflation, fuel subsidies, and currency depreciation that is
   structurally distinct from SSA subsistence poverty dynamics.

2. **Wrong regional multiplier magnitude.** Batini, Callegari & Melina (2012) estimates of
   fiscal multipliers for emerging Asia (0.4–0.7 range) are substantially lower than both
   the SSA Fosu calibration basis and the Euro area Blanchard & Leigh (2013) basis. The IMF
   Regional Economic Outlook: Asia-Pacific provides country-specific fiscal consolidation
   impact estimates for Pakistan and Sri Lanka that are not well-represented by the SSA
   informal-sector elasticity.

3. **Priority for 2022–23 live cases.** Pakistan 2022–23 and Sri Lanka 2022 are the most
   current and politically resonant evidence cases in the evidence portfolio. MAGNITUDE
   fidelity on these cases is a Demo 8 relevance condition: without South Asian calibration,
   WorldSim cannot make a defensible magnitude claim for the fiscal balance and welfare
   trajectory divergence between orthodox IMF programme terms and heterodox path alternatives
   for the most recent real-world cases.

---

## 2. Persona Trace Elements Targeted

> *Calibration infrastructure with no new UI element. Forward trace: calibration change →
> Pakistan 2022–23 and Sri Lanka 2022 counter-factual harness runs produce MAGNITUDE-class
> human development trajectory divergence under orthodox vs heterodox fiscal paths.*

| Persona | Use case | Forward-trace claim |
|---|---|---|
| Persona 2 (Finance ministry, programme country) | Scenario analysis — South Asian IMF programme | Pakistani or Sri Lankan analyst can show calibrated cohort welfare impact from orthodox IMF programme vs heterodox path grounded in South Asian-specific literature |
| Persona 5 (Researcher) | Historical backtesting | PAK 2022–23 Type B counter-factual produces defensible HD-composite magnitude divergence within calibrated South Asian bounds |
| Persona 3 (Negotiating team) | Counter-factual comparison | Counter-factual between IMF programme path and heterodox lower-adjustment path shows South Asian-calibrated poverty response, not SSA proxy |

---

## 3. Architecture

**No new architecture.** The `entity_families` field was added to `CohortElasticity` in
CM Sprint A. CM Sprint C uses the identical mechanism: new `CohortElasticity` instances with
`entity_families=frozenset({"PAK", "LKA", "BGD"})` appended to `ELASTICITY_REGISTRY`.

**Transmission channel assessment (to be confirmed in calibration decision):**

South Asian programme episodes have a more mixed transmission profile than LAC (FORMAL-primary)
or SSA (INFORMAL-primary):
- Pakistan 2022–23: fiscal consolidation + energy subsidy removal + import compression.
  Urban formal sector (civil service, formal private sector) absorbs subsidy removal;
  urban informal sector absorbs import compression and inflation. Both channels significant.
- Sri Lanka 2022: fuel shortages + sovereign default. Agricultural and informal sectors
  severely impacted (fuel for transport/agriculture); formal sector affected via import
  collapse. Both channels significant.
- Bangladesh: export-oriented formal sector (garments) with distinct vulnerability profile.

**Design question requiring calibration decision resolution:** The CM calibration decision
document must address whether:
- (a) South Asian entries target FORMAL sector cohorts only (additive, as in CM Sprint A/B),
- (b) South Asian entries target INFORMAL sector cohorts only (replacing the SSA proxy for
  these entities — but note: SSA Q1 INFORMAL fires at −0.20 on ALL entities; an INFORMAL
  entry would double-count unless a suppression mechanism exists),
- (c) Both FORMAL and INFORMAL entries are added, accepting that LAC Q1 INFORMAL continues
  to receive the SSA entry's delta PLUS the new South Asian entry's delta (summed effect), or
- (d) A mechanism to restrict SSA INFORMAL entries from firing on PAK/LKA/BGD is designed
  (requires module.py changes — broader scope than a calibration sprint)

Option (a) — FORMAL-only — is the minimum-scope approach consistent with CM Sprint A/B
precedent. Option (b) INFORMAL-only may overstate the INFORMAL channel for Pakistan (where
formal-sector consolidation was the primary IMF-mandated adjustment). The CM calibration
decision resolves this choice with reference to South Asian literature.

**Backtesting fixtures:** Both `pakistan_2022_scenario.py` (n_steps=4, biannual) and
`sri_lanka_2022_scenario.py` (n_steps=5, annual) exist in
`backend/tests/fixtures/`. No Bangladesh fixture; BGD included in `entity_families` for
structural completeness.

---

## 4. Acceptance Criteria

### AC-1: MAGNITUDE divergence (integration test, DATABASE_URL required)

For PAK Type B counter-factual (orthodox vs heterodox fiscal path), the `hd_composite`
divergence at a specified step satisfies:

```
lower_bound <= per_step_diff[N] <= upper_bound
```

Bounds TBD in calibration decision document. These certify the South Asian calibration
produces a detectable, non-trivial, non-overfit response on the HD composite scale.

### AC-2: South Asian entries present with correct scoping

At least 1 entry in `ELASTICITY_REGISTRY` with:
- `entity_families` contains `"PAK"`
- `attribute_key == "poverty_headcount_ratio"`

### AC-3: South Asian entry values

For the primary South Asian entry (quintile/sector TBD in calibration decision):
- `event_type == "gdp_growth_change"`
- `elasticity == <TBD in calibration decision>`
- `confidence_tier == 3` (T3 — regional South Asian inference; T2 requires country-specific)

### AC-4: SSA and prior sprint non-regression

All SSA M17-G1, CM Sprint A (GRC), and CM Sprint B (LAC) entries unchanged.

### AC-5: Cross-contamination guard

New South Asian entries must not fire on SEN, ZMB, GRC, ARG, ECU, BOL, or PER.

---

## 5. Forward Conditions

PAK/LKA AC-1 harness live runs require a live DATABASE_URL. Classified as forward conditions
for Demo 8 (same classification as CM Sprint A and B). Unit tests (AC-2 through AC-5) fully
certify the implementation. Full magnitude validation runs at Demo 8 Act 2.

---

## 6. Issue #1657 Coordination

Issue #1657 (DemographicModule dead event subscriptions) is unblocked by CM Sprint A.
CM Sprint C does not conflict with #1657 �� Sprint C targets elasticities.py only;
#1657 targets module.py. File-area separation ensures no conflict.

---

*Intent document authority: sprint-planning-sop.md §Sprint Entry Gate (Step 1).
Sprint entry: `docs/process/sprint-plans/m19-cm-c-sprint-entry.md` (filed concurrently).
Author: Chief Methodologist. Date: 2026-07-04.*
