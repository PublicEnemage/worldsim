# Cohort Disaggregation on Primary Surface — Design Document

> **Author:** UX Designer Agent
> **Date:** 2026-06-21
> **Issue:** #986 — feat(ux): cohort disaggregation on primary surface
> **Phase:** M15 G3 — Design-only (implementation is M16 scope)
> **Intent document:** `docs/process/intents/M15-G3-2026-06-21-cohort-disaggregation-design.md`
> **Status:** Filed for Architecture Review Facilitator and Chief Methodologist review
>
> **Governing documents read:**
> - `docs/ux/information-hierarchy.md §Zone 1`, `§Zone 2`, `§Dashboard View Hierarchy`
> - `docs/ux/north-star.md §Primary Cognitive Tasks by Mode`
> - `docs/ux/design-thinking/worldsim-ux-architecture-first-principles.md §Question 1`
> - `docs/ux/design-thinking/zone-1a-information-architecture.md §Information Allocation`
> - `CLAUDE.md §UX Architectural Commitments` (commitments 1–5)
> - `docs/ux/personas.md §Persona 2`, `§Persona 5`
> - `docs/ux/user-journeys.md §Journey A`, `§Journey B`

---

## Design Context

The engine's DemographicModule produces cohort-level indicator data: poverty headcount by income
quintile, school enrollment by cohort, child malnutrition by age group. This data is invisible at
the instrument level.

M11.5 Session 3 FINDING-03 (HIGH severity): "No cohort disaggregation visible — CONCLUDED answer
was ~80% historical knowledge, not tool output." Persona 2 (Eleni, Aicha) in the Reactive entry
state cannot answer "Which cohort is most affected and when?" from the primary viewport — they
must rely on domain knowledge not anchored in the tool's output. This design closes that gap.

**Design task:** Specify which Zone hosts cohort threshold alerts on the primary surface, which
cohort dimensions and indicators appear in M16, the zero-interaction display format, and the
relationship to ADR-017 (Zone 1A, #845 Phase 3).

---

# Zone Placement

**Decision: Zone 1B (MDA Alert Panel)**

Zone 1B's primary cognitive task, per `docs/ux/information-hierarchy.md §Zone 1`:

> *"Threshold crossing alerts from the trajectory computation. Positioned within the primary
> viewport (instrument cluster) — not inside the EntityDetailDrawer."*

Cohort-level threshold crossings ARE threshold crossing alerts — they are the disaggregated form
of the MDA alerts Zone 1B already produces. The `information-hierarchy.md §Zone 1 / 1B` already
specifies "top affected cohort" as a field in each alert row. This design promotes cohort threshold
crossings from a secondary field inside aggregate alert rows to a first-class sub-section of Zone
1B.

**Zone 1B cognitive task served (not conflicted):**

The extended Zone 1B layout allocates the existing top area to aggregate MDA alerts (unchanged)
and adds a "Cohort Impact" sub-section below a visual divider. The cognitive task — "has anything
crossed a threshold?" — is served in both sub-sections. A CRITICAL cohort threshold crossing is
as mission-critical as a CRITICAL MDA aggregate alert; co-locating them in Zone 1B makes the
threshold detection task complete in one Zone 1 read.

**Zone 1B capacity check:**

Adding cohort rows does not crowd the threshold breach alerting function of Zone 1B because:
- Aggregate MDA alert rows occupy the upper sub-section (unchanged — top 1–3 alerts visible
  without scroll per existing spec)
- Cohort threshold rows occupy the lower sub-section, separated by a horizontal divider
- Maximum 2 cohort rows visible without scroll at 1440×900 (see §Zero-Interaction Display Format)
- Scroll is available for additional cohort rows below the 2-row visible area; the top 2 cohort
  rows (sorted severity-first) surface the most urgent cohort findings without scroll

**Rejected alternatives:**

- **Zone 1A:** Adding cohort trajectory curves to Zone 1A would increase the combinatorial
  tension documented in `zone-1a-information-architecture.md §Combinatorial Tension`. The Phase 1
  allocation table explicitly places cohort breakdowns in Zone 2B. Cohort THRESHOLD ALERTS (not
  full trajectories) belong at Zone 1 — the distinction is: Zone 1B shows the crossing event
  (which cohort, which indicator, which step, which severity); Zone 2B shows the full indicator
  trajectory for that cohort on drill-down.
- **Zone 1D:** Zone 1D's cognitive task is "four-framework current position readout." Cohort
  threshold alerts are cross-framework distributional findings, not per-framework composite values.
  Mixing them into Zone 1D disrupts the current-step readout structure.
- **New Zone 1E:** A new primary zone requires a layout ADR and is disproportionate for content
  that fits naturally within Zone 1B's existing cognitive task.

---

## Cohort Scope Definition

### M16 scope: income quintile (REQUIRED)

Income quintile disaggregation is the primary M16 cohort dimension. Rationale tied to Persona 2's
negotiating argument: "Under current conditionality terms, the bottom income quintile crosses the
poverty headcount CRITICAL threshold at step 2." This argument requires income quintile
disaggregation. Geographic or demographic cohort arguments are secondary to the distributional
impact argument Persona 2 makes at the table.

Five quintiles (Q1 = bottom, Q5 = top). Display label convention:
- Q1 → "Bottom income quintile"
- Q2 → "Lower-middle income quintile"
- Q3 → "Middle income quintile"
- Q4 → "Upper-middle income quintile"
- Q5 → "Top income quintile" (shown only if crossing a threshold — alert-triggered display)

### M16 scope: age cohort (INCLUDED — limited)

Two age bands included in M16 for indicators where age disaggregation is analytically critical:
- Under-5 (for child malnutrition rate)
- Under-18 (for school enrollment rate)

Rationale: child malnutrition and school enrollment are the human development indicators most
sensitive to short-term austerity programmes and most commonly challenged at IMF negotiations.
Age-disaggregated data is available in the DemographicModule output for these indicators. Data
Architect must confirm availability before M16 sprint entry (see §M16 Implementation Gate).

Display label convention:
- Under-5 → "Under-5 age cohort"
- Under-18 → "School-age cohort (under-18)"

### Deferred (explicitly): gender cohort

Deferred to M17. Rationale: gender-disaggregated calibration requires separate coefficient sets
not present in the M16 data architecture. Including gender disaggregation without calibrated
coefficients would produce T4–T5 (model estimate / synthetic extrapolation) outputs with
uncertainty bands too wide for negotiating argument use. Deferral target: M17, contingent on
gender-disaggregated historical data availability for the approved source set.

### Deferred (explicitly): subnational / regional cohort

Deferred to M17+. Rationale: geographic disaggregation requires GIS integration not in the
current data architecture (single-entity, national-level modelling). Re-open trigger: the first
institutional user articulates a specific subnational argument need that cannot be served by the
national-level cohort display.

---

## Indicator Scope Definition

Three indicators in M16. Each includes: cohort dimension, threshold type, and severity tier
schema.

### Indicator 1 — Poverty headcount rate

| Field | Value |
|---|---|
| Indicator name (display) | Poverty headcount rate |
| Cohort dimension | Income quintile (Q1 and Q2 displayed; Q3–Q5 shown only at CRITICAL) |
| Framework | Human Development |
| Threshold type | MDA-derived (existing floor system — `min_descent_altitude` per entity per indicator) |
| Severity tier schema | CRITICAL: current value is below MDA floor; WARNING: current value is within 10% above floor; WATCH: current value is within 25% above floor |
| Data tier | T2 (World Bank PovcalNet / HIES surveys); T3 for synthetic extrapolation in data-sparse entities |
| Methodological note for CM | The poverty headcount floor is the entity-calibrated MDA value from the Human Development framework. No new cohort-specific threshold is introduced — the MDA floor applies to the quintile value directly. CM must confirm that applying the aggregate MDA floor to quintile-level poverty rates is methodologically defensible (i.e., the floor was calibrated at the population level, not the quintile level). If not, CM specifies the adjustment in their sign-off. |

### Indicator 2 — School enrollment rate

| Field | Value |
|---|---|
| Indicator name (display) | School enrollment rate |
| Cohort dimension | School-age cohort (under-18) and income quintile Q1 (if available; T4 if absent) |
| Framework | Human Development |
| Threshold type | MDA-derived |
| Severity tier schema | Same as Indicator 1 |
| Data tier | T2 (UNESCO Institute for Statistics); T3 for synthetic extrapolation |
| Methodological note for CM | School enrollment quintile disaggregation may require T3–T4 synthetic extrapolation for some entities in the approved source set. CM must confirm that displaying T3/T4 quintile school enrollment rates with proper tier labeling is within the platform's disclosure standard. |

### Indicator 3 — Child malnutrition rate

| Field | Value |
|---|---|
| Indicator name (display) | Child malnutrition rate |
| Cohort dimension | Under-5 age cohort |
| Framework | Human Development |
| Threshold type | MDA-derived |
| Severity tier schema | Same as Indicator 1 |
| Data tier | T2 (UNICEF / DHS); T3 for synthetic extrapolation |
| Methodological note for CM | Child malnutrition under-5 data availability varies by entity and time period. CM must confirm the floor calibration source for each entity in the approved set (GRC, JOR, EGY, ZMB) before M16 sprint entry. |

**Threshold type summary:** All three indicators use the MDA-derived threshold (existing floor
system). No new cohort-specific threshold calibration is introduced in M16. This is a deliberate
scope decision: using the existing MDA floors for cohort-level indicators produces conservative
alerts (since quintile rates for Q1 are typically worse than population averages, the MDA floor
is more often triggered at the quintile level than at the aggregate level — making the alert
system appropriately sensitive). Cohort-specific floor calibration is M17 scope.

---

## Zero-Interaction Display Format

The following shows the EXACT display visible in Zone 1B at the primary viewport with zero user
interaction. A QA reviewer reading this section should be able to complete: "In a ZMB ECF Mode 2
scenario at step 2, Zone 1B shows [this]."

```
━━━ Zone 1B | Step 2 | ZMB ECF | Mode 2 ━━━━━━━━━━━━━━━━━━━━━━

MDA ALERTS
──────────────────────────────────────────────────────────────
CRITICAL  Reserve coverage
          2.3 months · 6 consecutive steps · T2 · CBJ 2023-Q4
WARNING   Governance quality
          Approaching floor at step 4 · T3 · WGI 2023

──────────── COHORT IMPACT ────────────

CRITICAL  Bottom income quintile — Poverty headcount
          Threshold crossed at step 2 · was 3.8% above floor
WARNING   Under-5 cohort — Child malnutrition
          4.1% · approaching CRITICAL floor (3.8 pp above)

[2 further cohorts above WARNING threshold — not displayed]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Max 2 cohort rows visible without scroll at 1440×900.
Sorted: CRITICAL first, then WARNING; within same severity, step-ascending.
```

**Format specification (each cohort row):**

```
[SEVERITY BADGE]  [Plain-language cohort label] — [Plain-language indicator label]
                  [Threshold proximity sentence] · [T-tier label] · [Source citation]
```

- **Severity badge:** Color-coded (CRITICAL = red, WARNING = amber, WATCH = yellow). Same
  visual treatment as MDA aggregate alert severity badges.
- **Cohort label:** Plain language only. Never a field key (`hh_exp_q1` is not acceptable).
  "Bottom income quintile" is the label for Q1. Field keys are implementation detail.
- **Indicator label:** Plain language. "Poverty headcount" not `poverty_headcount_rate_pct`.
- **Threshold proximity sentence:**
  - CRITICAL (at or below floor): "Threshold crossed at step [N] · was [X%] above floor"
  - WARNING (within 10% of floor): "[current value] · approaching CRITICAL floor ([X pp] above)"
  - WATCH (within 25% of floor): "[current value] · elevated — [X pp] above WARNING boundary"
- **Tier label:** T1–T5 per `docs/DATA_STANDARDS.md §Confidence Tier System`
- **Source citation:** "[Source abbreviation] [period]" (e.g., "WB PovcalNet 2023-Q4")

**Sorted order:** Severity-first (CRITICAL before WARNING before WATCH). Within same severity:
step-ascending (earliest crossing first, as the most urgent signal). If two cohort rows have the
same severity and same step, indicator alphabetical order applies.

**Viewport limits:**
- 1440×900: 2 cohort rows visible without scroll
- 1280×800: 2 cohort rows visible without scroll
- 1024×768: 1 cohort row visible without scroll

The divider between MDA Alerts and Cohort Impact sub-sections is a labeled horizontal rule
("COHORT IMPACT") to orient the user. Both sub-sections are part of Zone 1B — the divider
is visual structure, not a navigation boundary.

---

## Mode-Specific Display Contract

### Mode 1 (Replay) — Historical cohort threshold events

Zone 1B Cohort Impact sub-section shows cohort threshold crossings as historical facts.

**Tense and framing:** Past tense — these events occurred in the loaded historical fixture.
- CRITICAL row text: "Threshold crossed at step [N]"
- WARNING row text: "[value] at step [N] — was [X pp] above floor"
- The sub-section header shows "COHORT IMPACT (HISTORICAL)" to distinguish from Mode 2 projections

**Update behaviour:** Cohort rows reflect the loaded step in the historical fixture. At step 0:
rows show which cohorts entered the scenario already at or near threshold. At step 4: rows show
crossings that occurred at or before step 4. Rows are always the "worst-to-date" state — once a
cohort crosses CRITICAL, the CRITICAL badge persists until the scenario is reset, with the step
number showing when the crossing occurred.

**When no cohort crosses a threshold in Mode 1:** The "COHORT IMPACT" sub-section shows:
"No cohort threshold crossings at or before this step." This is the empty state. It is displayed
explicitly — the absence of cohort alerts is itself information.

### Mode 2 (Simulation) — Projected cohort threshold events

Zone 1B Cohort Impact sub-section shows projected crossings based on the current path.

**Tense and framing:** Future-leaning — projections based on the current scenario state.
- CRITICAL row text (crossing at current step): "Threshold crossed at this step"
- CRITICAL row text (crossing projected ahead): "Projected to cross at step [N]"
- WARNING row text: "[value] · approaching CRITICAL floor (projected to cross at step [N] if
  current trajectory continues)"
- The sub-section header shows "COHORT IMPACT" (no qualifier — the Mode 2 context is shown in
  the persistent mode indicator in the header)

**Update behaviour:** Cohort rows update at each step advance. After advancing from step 2 to
step 3, all cohort threshold proximity calculations are recomputed from the new state. A cohort
that was WARNING at step 2 may show CRITICAL at step 3.

**When no cohort crosses a threshold in Mode 2:** Same empty state as Mode 1, with text:
"No cohort threshold crossings projected on current path."

### Mode 3 (Active Control) — Live-updating cohort threshold events

Zone 1B Cohort Impact sub-section updates after each control input propagation.

**Tense and framing:** Same as Mode 2, plus a "(updated)" label on any row whose severity
changed from the previous state (i.e., a control input caused a cohort to escalate from WARNING
to CRITICAL, or de-escalate from CRITICAL to WARNING after a corrective input).

**Update behaviour:** Cohort rows recompute after each control input application — same cycle as
the aggregate MDA alert panel update. The "updated" label appears for one render cycle, then
clears on the next step advance or control input.

---

## ADR-017 Interplay Statement

**Disposition (b): Cohort disaggregation proceeds independently of ADR-017.**

Placement in Zone 1B does not depend on Zone 1A encoding decisions. The Zone 1A architecture
ADR (ADR-017, #845 Phase 3) governs the trajectory curve encoding and information allocation for
Zone 1A. Zone 1B is governed by ADR-014 (Alert Panel Zone 1B master-detail, M13-G7). Adding a
Cohort Impact sub-section to Zone 1B is an extension of ADR-014's accepted display contract —
it does not require Zone 1A architectural decisions.

**Non-conflict with Zone 1A Phase 1 information allocation (`zone-1a-information-architecture.md
§Information Allocation`):**

The Phase 1 allocation table states: "Per-entity trajectory comparison (N>1, per-framework)" →
"Zone 1D (current step) and Zone 2B (FrameworkPanels, full history)." The allocation of
*trajectory detail* to Zone 2B is preserved by this design. Zone 1B shows only the threshold
crossing EVENT (cohort, indicator, severity, step) — not the full cohort trajectory. The full
cohort trajectory remains Zone 2B content (one-click expand within FrameworkPanel). This design
does not displace any Zone 1A allocation.

**What this means for M16 sprint entry:** M16 sprint entry for #986 implementation does not
require waiting for ADR-017 to be accepted. The ADR-017 panel may be informed by this design
document (as evidence that Zone 1B will host cohort threshold alerts), but ADR-017 acceptance
is not a blocking dependency for M16 #986 implementation.

---

## Secondary States

### Zone cognitive task conflict check

**Confirmed: proposed placement does not degrade Zone 1B's primary cognitive task.**

Zone 1B's primary cognitive task — threshold crossing alert detection — is served by both the
aggregate MDA alert sub-section (unchanged) and the new Cohort Impact sub-section (new content).
The two sub-sections address the same cognitive task at different granularities. Visual separation
(labeled horizontal divider) prevents visual competition.

**Capacity check at minimum viewport (1024×768):** At 1024×768, only 1 cohort row is visible
without scroll. The most severe cohort row (CRITICAL first) remains visible. If no CRITICAL cohort
row exists, the first WARNING row is visible. This is acceptable: at 1024×768, the user can scroll
to see additional cohort rows; the most urgent signal is always in the visible area.

### Mode-specific display contract

Satisfied by §Mode-Specific Display Contract above. Mode 1, Mode 2, and Mode 3 are specified
separately. The display differentiates: past-tense historical facts (Mode 1), projected crossings
that update per step advance (Mode 2), and live-updating rows after control input propagation
(Mode 3).

### Silent failure detection test

A QA reviewer can complete this sentence from this document alone:

> "In a ZMB ECF Mode 2 scenario at step 2, Zone 1B shows a 'COHORT IMPACT' sub-section below
> the MDA aggregate alerts, with at most 2 rows visible without scroll. The first row shows
> 'CRITICAL — Bottom income quintile — Poverty headcount — Threshold crossed at step 2 · was
> 3.8% above floor' and the second row shows 'WARNING — Under-5 cohort — Child malnutrition —
> 4.1% · approaching CRITICAL floor (3.8 pp above).' Two additional cohort rows exist but are
> below the visible area."

This sentence is completable from this document without reading any implementation code or
simulation engine output. The silent failure test is satisfied.

---

# M16 Implementation Gate

The following dependencies must be cleared before a M16 sprint entry for #986 implementation
is filed. Each is named specifically.

1. **Chief Methodologist sign-off (required):** CM confirms that the three indicator selections
   (poverty headcount, school enrollment, child malnutrition) and the use of MDA-derived floors
   as cohort-level threshold values are methodologically defensible per `docs/DATA_STANDARDS.md`.
   Specifically: CM confirms that applying aggregate MDA floors to quintile-level indicator values
   is consistent with the platform's calibration basis — or specifies an adjustment. CM sign-off
   is recorded as a review acknowledgment at the bottom of this document or as a comment on
   GitHub issue #986.

2. **DemographicModule cohort output verification (required):** Data Architect confirms which
   cohort dimensions are available in the DemographicModule's output for each entity in the
   approved source set (GRC, JOR, EGY, ZMB). Specifically: confirms that income quintile
   poverty headcount, under-18 school enrollment, and under-5 child malnutrition are available
   as named output fields in the DemographicModule before M16 implementation begins. If any
   field is absent, the M16 sprint entry scope is adjusted to exclude that indicator. Data
   Architect sign-off is recorded on GitHub issue #986.

3. **Architecture Review Facilitator confirmation (required):** AC-1 through AC-6 confirmed
   satisfied for this document. M16 sprint entry for #986 may be filed on process grounds.
   (The ADR-017 dependency is explicitly NOT a requirement — see §ADR-017 Interplay Statement.)

4. **ADR-017 dependency: NOT required.** M16 sprint entry for #986 may be filed when
   dependencies 1–3 above are cleared, regardless of whether ADR-017 has been accepted. The
   Zone 1B placement is independent of Zone 1A architectural decisions.

---

## Review Acknowledgments

*(Completed by reviewer at time of review — before any M16 sprint entry for #986 is filed)*

`[ ]` **Chief Methodologist:** Indicator scope (poverty headcount, school enrollment, child
malnutrition) and use of MDA-derived floors as cohort-level threshold values confirmed
methodologically defensible per AC-3. CM adjustment (if any): ________________. M16 sprint
entry for #986 may proceed on CM grounds. [Date]

`[ ]` **Architecture Review Facilitator:** AC-1 through AC-6 satisfied. M16 sprint entry for
#986 may be filed. ADR-017 dependency: NONE (Zone 1B, independent). [Date]

---

*Design document version: 2026-06-21. Issue #986. M15 G3 parallel track. Implementation scope:
M16. UX Designer Agent authored. Full lifecycle authority: `CLAUDE.md §Agent Execution Lifecycle`.*
