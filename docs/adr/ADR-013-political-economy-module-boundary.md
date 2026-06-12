# ADR-013: Political Economy Module — Conditionality Modelling, Elite Capture, and Political Feasibility

> **Reader Orientation:** This ADR governs the political economy module boundary for M13.
> Read it before: extending PoliticalEconomyModule with new indicators, integrating
> conditionality decomposer output into the measurement framework, modifying the
> programme survival probability calculation, or adding political feasibility signals
> to Zone 1B. G6 (political economy integration) is gated on this ADR's acceptance.

## Tier Classification

**Tier:** 1

**Justification:**
This ADR introduces new analytical capability whose outputs surface in Zone 1B (MDA alerts
for programme survival probability breaches), the trajectory response (political feasibility
as a named framework indicator), and the measurement output (per-term conditionality risk
scores and elite capture divergence index). It defines the confidence tier treatment for
political feasibility estimates, which is a visual treatment for uncertainty — a Tier 1
classification trigger per the template.

**Sections required by tier:**

| Section | Required? |
|---|---|
| Persona Trace (7-element) | Required |
| UX Implication Statement (7-element) | Required — UX Designer sign-off |
| Forward Trace Statement | Not applicable |
| Silent Failure Mode | Required |
| Asymmetry Assessment | Required (analytical capability) |
| North Star Test | Required |
| Mission Impact Statement | Required |

---

## Status

`Accepted`

---

## Validity Context

**Standards Version:** 2026-06-12
**Valid Until:** M14 close, or when any of the renewal triggers below occur
**License Status:** `ACCEPTED` — EL acceptance recorded 2026-06-12 (PR #916)

**Panel:**
- Architect Agent (R — authorship, interface contracts)
- Political Economist (C — political feasibility modelling correctness, elite capture dynamics)
- Chief Methodologist (C — confidence tier assignment for political estimates, calibration honesty)
- Engineering Lead (A — accountable on all ADR decisions)

**Renewal Triggers:**
- A second political feasibility model (e.g. electoral cycle) is added alongside programme survival
- The conditionality decomposer's per-term attribution scope expands beyond fiscal_delta
- Elite capture divergence output moves from per-cohort to sub-cohort disaggregation
- The PROGRAMME_SURVIVAL_FLOOR threshold is changed
- Political economy indicators are promoted from Tier 3 to Tier 2 (requires new calibration evidence)

---

## Date

2026-06-12

---

## Context

### Background

The PoliticalEconomyModule was introduced in M11 (PRs #704/#705) with three internal
capabilities: legitimacy dynamics (legitimacy erosion under fiscal austerity), programme
survival probability (probability that the policy programme survives long enough for
stabilisation to materialise), and elite capture coefficient (divergence in cohort outcomes
under fiscal adjustment).

All three capabilities compute internal model variables and emit events. None surface as named
analytical outputs that Persona 2 can cite in a negotiation room. The conditionality decomposer
(`conditionality_decomposer.py`) exists as a utility but its output is not integrated into the
measurement framework or the MDA alert system.

M13's primary analytical objective is closing this gap: political economy outputs must be
surfaceable in the same way as financial or human development outputs — named, confidence-tiered,
and citable.

### Problem Framing

In Journey A Step 5 (Persona 2 drills down to identify argument components), Eleni encounters
CRITICAL human development and financial alerts but cannot determine whether the programme is
politically viable or which specific conditionality term drives the threshold crossing. She can
see that crossings occur but not whether the programme survives long enough for stabilisation —
and not which creditor-imposed term is the primary driver.

This is a named failure mode in `docs/ux/personas.md §Persona 2`: "the tool cannot tell her
which specific conditionality term drove the threshold crossing (generic deterioration signals
do not support specific challenges)." ADR-013 closes this gap.

Two concrete limitations drive this ADR:

1. **Programme survival probability is an internal model variable, not a named output.** When
   programme survival probability falls below the viability floor, no MDA alert fires. Eleni
   sees threshold crossings at step 2 but not whether the programme is already at risk of
   political collapse before step 2. She cannot cite political feasibility risk as a challenge
   to the conditionality package.

2. **Conditionality decomposer attribution is not surfaced.** The conditionality decomposer
   correctly attributes fiscal delta to each creditor term. This attribution is never surfaced
   in the measurement output. Eleni cannot identify which specific term (VAT rate increase,
   pension cut, public sector wage freeze) is the primary cost driver for the threshold crossing
   she is citing.

---

## Decision

### Decision 1 — Programme Survival Probability as Named Measurement Output

`programme_survival_probability` is promoted from an internal model variable to a named
indicator in the political economy measurement framework, surfaced in the trajectory response
and measurement output API endpoints.

**Output specification:**

- **Indicator key:** `programme_survival_probability`
- **Framework:** `political_economy`
- **Type:** `Quantity` with `VariableType.PROBABILITY` (value in [0.0, 1.0])
- **Confidence tier:** Tier 3 (SYNTHETIC_COMPARABLE) — formula-based approximation calibrated
  against historical programme failure cases (Greece 2010, Argentina 2001, Ecuador 2000).
  The word "synthetic" must appear in the confidence tier disclosure wherever this indicator
  is displayed. The label "formula-calibrated estimate" must be available as a tooltip or
  secondary disclosure.
- **Disclosure phrase (Layer 3 requirement):** "Programme survival probability is a formula-
  calibrated estimate (Tier 3) based on historical programme failure patterns. It is not a
  prediction. A value below 0.25 indicates conditions similar to historically failed programmes."

**MDA alert trigger:**

When `programme_survival_probability` falls below `PROGRAMME_SURVIVAL_FLOOR = 0.25`, emit
a CRITICAL MDA alert in the `political_economy` framework. Alert properties:

- `mda_id`: `"PE-001-programme-survival-critical"`
- `severity`: `"CRITICAL"`
- `indicator_key`: `"programme_survival_probability"`
- `indicator_name`: `"Programme Survival Probability"`
- `floor_value`: `"0.25"` (Decimal string)
- `current_value`: current `programme_survival_probability` (Decimal string, 2 d.p.)

The `PROGRAMME_SURVIVAL_FLOOR` constant is defined in
`backend/app/simulation/modules/political_economy/module.py` and must not be changed
without an ADR amendment.

### Decision 2 — Conditionality Per-Term Risk Attribution as Named Indicators

The conditionality decomposer output is integrated into the measurement framework as named
per-term indicators, one per active conditionality term in the scenario.

**Indicator key pattern:** `conditionality_term_{constraining_actor_id}_{constraint_mechanism}`
(e.g. `conditionality_term_IMF_FISCAL_CONSOLIDATION`, `conditionality_term_ECB_COLLATERAL_HAIRCUT`)

**Value semantics:** Effective fiscal delta for this term (absolute value, Decimal), representing
the fiscal cost attributable to this creditor's specific constraint mechanism at this step.

**Confidence tier:** Inherits from the primary fiscal indicator driving the attribution (typically
`fiscal_balance_pct_gdp`, Tier 2 for countries with IMF programme history).

**MDA alert trigger:** None. Conditionality risk indicators are surfaced in the measurement
output API but do not trigger MDA alerts directly — alerts are triggered by the downstream
threshold crossings they cause (financial or human development), not by the attribution itself.
This is a deliberate boundary: the alert system signals threshold crossings, not causal chains.
Causal attribution is in the measurement output for Eleni to read; the alert is the signal.

**Constraint:** Only scenarios with at least one `ControlInput` with `InputSource.CONDITIONALITY`
produce conditionality term indicators. Scenarios with no conditionality inputs produce an empty
list. The decomposer must not be called when `conditionality_inputs == []`.

### Decision 3 — Elite Capture Divergence Index as Named Indicator with Cohort Breakdown

`elite_capture_divergence_index` is promoted from an emitted event to a named indicator in
the political economy framework.

**Indicator key:** `elite_capture_divergence_index`
**Framework:** `political_economy`
**Value semantics:** Divergence ratio — the ratio of elite cohort fiscal benefit capture to
non-elite cohort fiscal cost share. A value of 1.0 indicates no divergence. A value of 2.0
indicates elite cohorts captured twice the proportional benefit relative to their population
share. A value below 1.0 is not possible under the current formulation (a known limitation).

**Cohort breakdown (required):** Two cohort sub-indicators must accompany the index:
- `elite_capture_divergence_top_quintile`: estimated benefit capture share for the top income quintile
- `elite_capture_divergence_bottom_quintile`: estimated cost burden share for the bottom two income quintiles

These sub-indicators satisfy the income cohort requirement (DE-5 per DIC Roadmap).

**Confidence tier:** Tier 3 (SYNTHETIC_COMPARABLE). Elite capture measurement requires survey
data unavailable for most scenario entities. The estimate is structural (derived from entity
`elite_capture_coefficient` attribute calibrated from World Bank Inequality surveys). The word
"synthetic" must appear in any confidence tier disclosure for this indicator.

**Constraint:** When `elite_capture_coefficient` entity attribute is absent or zero, these
indicators are not computed and the module returns null values. The measurement output must
surface null (not zero) to preserve the null-signal distinction (US-022).

### Decision 4 — Political Economy Framework Composite Score

The `political_economy` framework now participates in the four-framework trajectory output
alongside `financial`, `human_development`, `ecological`, and `governance`.

**Composite score formula:** The political economy composite score is the arithmetic mean of
three normalised inputs:
1. `programme_survival_probability` (already in [0.0, 1.0])
2. `1 - elite_capture_divergence_index / MAX_ELITE_CAPTURE` where `MAX_ELITE_CAPTURE = 5.0`
   (capped to [0.0, 1.0])
3. Governance-normalised legitimacy index (`legitimacy_index` if present in entity attributes,
   else 0.5 neutral)

Higher score = more stable political economy. Score 0 = political collapse conditions. Score 1 =
full programme viability, no elite capture, full legitimacy.

**Confidence tier:** The composite score inherits the maximum tier number (lowest confidence)
of its three inputs. Because all three inputs are Tier 3, the composite is always Tier 3
(SYNTHETIC_COMPARABLE) until full statistical calibration is complete (Issue #44 deferred).

**Zone 1D integration:** The four-framework Zone 1D panel (FourFrameworkZone1D) already renders
four rows: financial, human_development, ecological, governance. This decision does NOT add
political_economy as a fifth row in Zone 1D. Adding a fifth framework requires a separate ADR
addressing the layout impact on Zone 1D (currently designed for exactly four rows).

Political economy composite score is available in the trajectory API and in the measurement
output for programmatic access, but does not appear in Zone 1D until that ADR is authored
and accepted. This is an explicitly deferred capability, not an oversight.

**Open obligation:** A follow-on ADR is required to define how `political_economy` appears in
Zone 1D. The absence of a Zone 1D entry for political economy is a known capability gap.
Tracked in GitHub Issue #392.

---

## Persona and UX Traceability

### [Tier 1] Persona Trace

**P-1 — Persona identification:**
Primary: Persona 2 — Finance Ministry Negotiator (Eleni Papadimitriou archetype, `docs/ux/personas.md §Persona 2`).
Secondary: Persona 3 — Political Advisor (Andreas Stefanidis archetype) — uses political
feasibility and elite capture output to build the political brief for the minister.

**P-2 — Entry state:**
Reactive entry state (90-second total ceiling, negotiation room context) for the programme
survival probability alert (Decision 1). Preparatory entry state (20–40 minutes, desk preparation)
for conditionality term attribution (Decision 2) and elite capture divergence (Decision 3).

**P-3 — Journey reference:**
Primary: Journey A Step 5 (Drill down: identify the argument components). Decision 2
(conditionality term attribution) directly closes the `[Near-Term-Gap]` at Journey A Step 5:
"which specific conditionality term drove the threshold crossing."
Secondary: Journey B Step 3 (Scan: read the top MDA alert). Decision 1 (programme survival
MDA alert) surfaces in Zone 1B as a CRITICAL alert, reaching Persona 2 in the 30-second scan
window without any additional interaction.

**P-4 — Time or interaction ceiling:**
- Decision 1 (programme survival alert): alert visible in Zone 1B without interaction within 5
  seconds of selecting the scenario, provided `programme_survival_probability < 0.25`. Journey B
  Step 3 time ceiling.
- Decision 2 (conditionality attribution): accessible via measurement output API in ≤ 2 API calls
  (trajectory + measurement-output). No new UI interaction required for Journey A Step 5.
- Decision 3 (elite capture): same as Decision 2.
- Decision 4 (composite score): available in trajectory response without additional calls.

**P-5 — Income cohort served:**
Bottom two income quintiles (primary HCL cohort). The elite capture divergence index (Decision 3)
explicitly names the bottom two quintiles as the burden-bearing cohort vs. the top quintile.
The conditionality attribution (Decision 2) enables identifying which creditor terms most affect
bottom-quintile human development indicators.

**P-6 — Negotiating leverage statement:**
After accessing this capability, Persona 2 can make the following specific argument: "The IMF's
FISCAL_CONSOLIDATION conditionality term accounts for an effective delta of 3.2% of GDP in year 2,
which is the primary driver of the poverty headcount CRITICAL alert at step 2. Our counter-proposal
removes this term and replaces it with a revenue measure that achieves the same fiscal target
without triggering the alert. Programme survival probability at that threshold is 0.18 — lower than
any historically completed IMF programme in this region."

**P-7 — North star test answer:**
Does this decision make the tool more useful to a finance minister sitting across from an IMF
negotiating team, in that moment?

Greece, February 2012. The Troika has just presented the second memorandum conditionality package.
The Hellenic Ministry of Finance analyst opens WorldSim with the conditionality package as scenario
inputs. Without ADR-013: she can see that human development indicators cross CRITICAL thresholds
at step 2, but she cannot tell whether this is driven by the pension cut term, the VAT increase,
or the public sector wage freeze. She also cannot tell whether the programme is already at
political viability risk before step 2.

With ADR-013: the measurement output shows that the pension cut term (constraining_actor_id="IMF",
constraint_mechanism="PENSION_CUT") accounts for 68% of the effective fiscal delta driving the
step 2 crossing. The programme survival probability alert fires at step 1 (value: 0.21, below the
0.25 floor), visible as a CRITICAL alert in Zone 1B. The analyst can now make a specific argument:
"The proposed pension cut alone drives the step 2 poverty headcount breach, and programme viability
is already at risk before that breach occurs — both the human cost and the political feasibility
evidence support a restructured timeline."

This closes an asymmetry gap: IMF negotiators routinely present conditionality packages without
disaggregated attribution. The finance ministry team with three economists now has the same
attribution capability that IMF country desk economists use internally to design programme terms.

---

### [Tier 1] UX Implication Statement

**UX-1 — Zone assignment and hierarchy certification:**
Decision 1 (programme survival MDA alert) places a new alert type in Zone 1B. Zone 1B is the
existing MDA alert panel; no new zone is created. The `political_economy` framework as alert
source is new. This assignment is consistent with `information-hierarchy.md` — MDA alerts from
all frameworks surface in Zone 1B without framework-specific routing.

Decision 4 (composite score) places the political economy composite score in the trajectory
response and measurement output API, but NOT in Zone 1D (which shows only the four canonical
framework rows). This is a deliberate deferral pending a follow-on ADR.

**UX-2 — Primary cognitive task alignment:**
Decision 1 (programme survival alert) primarily serves Mode 1 (trajectory reconstruction —
understanding what happened) and Mode 2 (threshold-safe path construction — identifying viable
paths). In Mode 3 (real-time steering), the programme survival probability alert provides a
political feasibility guardrail: if a control input drives `programme_survival_probability` below
the floor, a CRITICAL alert fires immediately after recompute.

Decisions 2 and 3 (conditionality attribution, elite capture) primarily serve Mode 1 and Mode 2
cognitive tasks. They do not affect Mode 3 real-time steering directly.

**UX-3 — Entry state coverage (falsifiable acceptance criteria):**

*Reactive state (Persona 2, Journey B Step 3):*
With the Hellenic Ministry scenario loaded at step 2 and `programme_survival_probability = 0.21`:
Zone 1B must show a CRITICAL alert with indicator name "Programme Survival Probability" without
any interaction, visible at 1280×800 desktop. Acceptance criterion: `[data-testid="mda-alert-row"]`
with text "Programme Survival Probability" and severity badge "CRITICAL" is present in the DOM and
visible (not overflow-clipped) within 5 seconds of scenario selection.

*Preparatory state (Persona 2, Journey A Step 5):*
GET `/api/v1/scenarios/{id}/measurement-output?entity_id=GRC&step=2` returns a JSON object
with `outputs.political_economy.indicators` containing at least one key matching the pattern
`conditionality_term_*` with a non-null `value` when the scenario has CONDITIONALITY inputs.
Acceptance criterion: the measurement output API response includes the conditionality term
indicator for the IMF fiscal consolidation term in the Hellenic scenario fixture.

**UX-4 — HCL parity certification:**
This ADR introduces the elite capture divergence index (Decision 3), which is an HCL output —
it measures the distributional impact of fiscal adjustment on bottom-quintile cohorts. The elite
capture divergence index must have equal visual weight to financial composite scores wherever
both are displayed. The indicator is classified as a human cost output (not a secondary context
indicator). HCL parity is maintained: elite capture divergence is a primary output, not a note.

**UX-5 — Uncertainty display specification:**
All three political economy indicators (programme_survival_probability, conditionality term
attribution, elite_capture_divergence_index) are Tier 3 — SYNTHETIC_COMPARABLE.

- What is displayed: "(Tier 3 — synthetic estimate)" badge adjacent to the indicator value
  wherever shown in the measurement output or drawer context
- Where it appears: inline with the indicator row in FrameworkPanel, adjacent to the composite
  score in trajectory tooltip
- For Tier 3 SYNTHETIC_COMPARABLE: the word "synthetic" must appear verbatim in the disclosure
  text. Acceptable form: "Tier 3 — synthetic calibration"
- For Tier 4: would show "(Tier 4 — insufficient data)" — not applicable for current indicators
- For Structural Absence Declaration: would show "Data absent — see methodology note"

**UX-6 — Irreversibility signal integrity certification:**
Programme survival probability alerts (Decision 1) fire at CRITICAL severity. They are rendered
using the existing MDA alert severity system. TERMINAL rendering remains visually distinct from
CRITICAL with no implementation discretion required. The political economy CRITICAL alert for
programme survival is not TERMINAL — programme collapse is modelled as recoverable (a new
programme can be agreed). This is correct and must not be changed to TERMINAL without an ADR
amendment and Political Economist sign-off.

CI-testable acceptance criterion: with the Hellenic scenario fixture at step 2 with
`programme_survival_probability = 0.21`, at 1280×800, `[data-testid="alert-severity-badge"]`
with text "CRITICAL" (programme survival) is visible without scroll alongside any existing
financial/HCL CRITICAL alerts.

**UX-7 — User journey coverage:**
- Journey A Step 5 `[Near-Term-Gap]` — closed by Decision 2 (conditionality attribution).
  Eleni can now answer "which term drove this crossing?" directly from measurement output.
- Journey B Step 3 — enhanced by Decision 1 (programme survival MDA alert). Zone 1B now
  surfaces political feasibility risk alongside financial and HCL risks.
- Journey A Step 5 — enhanced by Decision 3 (elite capture). Eleni can identify which cohorts
  bear the adjustment cost (bottom quintiles) vs. which capture the benefit (top quintile).

No existing journey steps are removed or impeded.

**UX Designer sign-off:**
`[ ]` UX Designer: UX implication statement elements 1–7 confirmed complete. [Date pending panel review]

---

## Silent Failure Mode

The political economy module fails silently when:

1. **`elite_capture_coefficient` is absent from entity attributes** — the module returns null for
   all elite capture indicators without warning. Detection: the measurement output has
   `elite_capture_divergence_index: null` even when the scenario has conditionality inputs. QA
   check: verify entity attribute is seeded before running scenarios with conditionality inputs.

2. **`programme_survival_probability` is computed but the MDA threshold check is skipped** — if
   `PROGRAMME_SURVIVAL_FLOOR` is not compared correctly (e.g. float comparison instead of Decimal),
   the CRITICAL alert never fires even when the probability is below the floor. Detection: run the
   Hellenic scenario fixture at step 2 and assert the MDA alert fires. This is the primary silent
   failure mode that the acceptance criterion (UX-3 Reactive state) guards against.

3. **Conditionality decomposer is not called** — if the module does not check for CONDITIONALITY
   inputs before calling the decomposer, the per-term indicators are silently absent from measurement
   output. Detection: measurement output API response has no `conditionality_term_*` keys even when
   the scenario has conditionality inputs.

Detection mechanism for all three: the Hellenic fixture scenario (Greece, step 2, with IMF
FISCAL_CONSOLIDATION and PENSION_CUT conditionality inputs, elite_capture_coefficient = 0.3)
is the canonical silent failure detection fixture. If this fixture passes all three acceptance
criteria in UX-3, no silent failure exists.

---

## Asymmetry Assessment

Well-resourced actors — IMF country desk economists, World Bank programme teams, and
investment-bank sovereign risk desks — have proprietary political economy models that:
1. Compute per-creditor-term fiscal attribution as part of programme design
2. Assess programme survival probability using regression models calibrated on historical
   programme data (many more data points than the three cases used in WorldSim's formula)
3. Model elite capture effects using World Bank household survey microdata not publicly available

WorldSim's ADR-013 partially closes this gap by:
1. Surfacing per-term fiscal attribution from the existing conditionality decomposer (closes
   the attribution gap; the decomposer's formula is accessible, so the methodology is transparent)
2. Surfacing programme survival probability with explicit Tier 3 calibration disclosure (the
   creditor side uses proprietary calibrations — WorldSim's formula-based approach is honest
   about its approximation quality)
3. Surfacing elite capture divergence as a named indicator (closes the visibility gap, though
   the estimate quality is lower than microdata-based approaches)

The remaining gap after this ADR: WorldSim's political feasibility model is formula-calibrated
on three historical cases. Creditor-side models use dozens of cases and proprietary data. The
confidence tier system honestly signals this limitation (Tier 3). The Structural Absence
Declaration pathway exists for entities where even Tier 3 calibration is not possible.

---

## North Star Test

Does this decision make the tool more useful to a finance minister sitting across from an IMF
negotiating team, in that moment?

Zambia, 2023. The Ministry of Finance is in the third round of IMF programme negotiations.
The IMF has proposed three structural conditionality terms: a 15% reduction in social transfers,
a pension eligibility reform, and a fuel subsidy removal. The ministry's specialist opens WorldSim
with all three as CONDITIONALITY control inputs. Without ADR-013: she can see that
human_development CRITICAL alerts fire at steps 2 and 3, but she cannot attribute which term
is the primary driver or whether the programme has any reasonable chance of surviving politically.

With ADR-013: the measurement output shows the fuel subsidy removal term accounts for 71% of
the step 2 HCL crossing (the subsidy's transmission to bottom-quintile energy costs). The
programme survival probability alert fires at step 1 (value: 0.19) — before the HCL crossing
even occurs. The minister's team presents to the IMF delegation: "Removing the fuel subsidy
alone crosses our human development threshold and our programme viability threshold is already
breached — we require a phased approach or a targeted social protection measure that offsets the
bottom-quintile burden." This is a specific, citable, evidence-backed counter-position that was
not possible without ADR-013.

This closes the primary asymmetry gap documented in the personas: the IMF delegation designed
the conditionality package with term-level attribution models and political viability assessments.
The ministry team now has the same analytical capability.

---

## Mission Impact Statement

This ADR closes the conditionality attribution gap (ranked as the primary analytical gap in
the asymmetry-closing impact list — DIC Roadmap Section B item 1: "per-term conditionality
attribution for negotiation-room use"). The direct impact on the finance ministry side of a
sovereign debt negotiation is that Persona 2 can challenge a specific conditionality term with
evidence-backed attribution rather than challenging the aggregate package. Aggregate challenges
are routinely dismissed by creditor negotiating teams as "model speculation". Term-specific
attribution with confidence disclosure is harder to dismiss.

Technical completeness — the conditionality decomposer running correctly — is not mission
completeness. Mission completeness requires the attribution to be surfaced as a named, confidence-
tiered, citable output. ADR-013 defines that surfacing.

---

## Minimum Data Tier

**Decision 1 (programme survival probability):** Tier 3. The formula uses `legitimacy_index`
(available from entity attribute seeding for most scenario entities) and `fiscal_balance_pct_gdp`
(Tier 2 for countries with IMF programme history; Tier 3 for others). The output is Tier 3 at
minimum regardless of input quality.

**Decision 2 (conditionality attribution):** Inherits from fiscal_balance input tier. Typically
Tier 2 for IMF programme countries. Tier 3 for data-poor entities.

**Decision 3 (elite capture):** Tier 3 always. Requires `elite_capture_coefficient` entity
attribute which is a structural estimate from World Bank data.

For users in Tier 3–4 data environments: all three outputs remain available at Tier 3 fidelity.
The confidence tier disclosure signals the estimation quality. This is not a capability
accessibility gap — the Tier 3 disclosure makes the limitation transparent rather than hiding it.

---

## Alternatives Considered

### Alternative 1: Separate Political Economy API Endpoint

Rather than integrating political economy outputs into the existing measurement output endpoint
(`/measurement-output`), add a new endpoint `/political-economy-output`.

Rejected: creates a second API call requirement in the Reactive entry state (90-second ceiling).
Eleni's tool already requires GET /trajectory + GET /measurement-output. A third endpoint is
a latency and UX regression. The existing measurement framework supports multi-framework outputs
by design — the correct architectural decision is to add `political_economy` as a new framework
key in the existing endpoint, not to fork the API surface.

### Alternative 2: Promote Political Economy to a Fifth Zone 1D Row

Add `political_economy` as a fifth row in FourFrameworkZone1D alongside the four canonical rows.

Rejected for this ADR: Zone 1D was designed for exactly four rows. The information hierarchy
documented in `docs/ux/information-hierarchy.md` defines the co-primary cluster layout. Adding
a fifth row requires a UX review of the layout impact across all three modes at all three
breakpoints. This is a correct architectural concern — deferring Zone 1D integration to a
follow-on ADR is the right decision. The composite score is available in the trajectory
API immediately without Zone 1D integration.

### Alternative 3: Political Feasibility as a Governance Sub-Indicator

Rather than a separate `political_economy` framework, fold programme survival probability and
elite capture into the existing `governance` framework as sub-indicators.

Rejected: governance and political economy are analytically distinct domains. Governance
measures rule of law, institutional quality, and state capacity. Political economy measures
programme viability, conditionality cost attribution, and distributional adjustment dynamics.
Collapsing them obscures the distinction Persona 3 (Political Advisor) needs: he interprets
political economy signals differently from governance signals. The separate framework boundary
established in M11 is correct and should be preserved.

---

## Consequences

### Positive

- Journey A Step 5 `[Near-Term-Gap]` is closed: Persona 2 can now cite which conditionality term
  drives a threshold crossing
- Zone 1B programme survival alert gives Persona 2 a political feasibility warning in the
  Reactive entry state without additional interaction
- Elite capture divergence promotes HCL cohort visibility for distributional equity analysis
- All three capabilities use existing module infrastructure — no new module boundary introduced
- Confidence tier disclosure is explicit (Tier 3 for all political estimates) — the tool is
  honest about its approximation quality

### Negative

- Political economy composite score is not in Zone 1D — this is a capability gap that requires
  a follow-on ADR. Persona 3 (Political Advisor) cannot see political economy composite score
  in the primary viewport without opening the drawer.
- The programme survival probability formula is calibrated on three cases. As additional
  programme failure cases are documented (Issue #44), the formula will change — this is
  technical debt that will require a calibration update and potential MDA floor adjustment.
- Conditionality attribution only works for scenarios with `InputSource.CONDITIONALITY` inputs.
  Scenarios without structured conditionality inputs receive no attribution. This is correct
  behaviour, not a limitation, but may surprise users who expect political economy indicators
  in all scenarios.

### Known Limitations

- Programme survival probability model is calibrated on Greece, Argentina, Ecuador — all middle-
  income countries with IMF programme history. Low-income country dynamics (dependency on bilateral
  donors, food security vulnerability, external shock sensitivity) are not captured. This is a
  known weak fidelity domain. The Tier 3 disclosure signals it; the methodology documentation
  (`docs/methodology/calibration-basis.md`) must document it explicitly.
- Elite capture coefficient is a single scalar per entity. It does not vary by step (elite capture
  dynamics are not modelled as time-varying). This limitation affects Persona 3 more than Persona 2.
- Political economy composite score (Decision 4) is not backed by empirical validation. It is an
  architectural placeholder that makes the framework slot available for downstream ADRs. Issue #44
  tracks the full calibration obligation.
