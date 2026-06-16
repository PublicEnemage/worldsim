# ADR-016: Scenario Grounding Architecture

## Tier Classification

**Tier:** 1

**Justification:**
This ADR introduces a Zone 2 surface (Scenario Grounding Strip) and modifies the scenario creation form (entry point to Zone 1 for new scenarios), directly affecting what a user can see and verify before any Zone 1 instrument is used. It also introduces scenario-contextual content to the Fidelity panel (existing Zone 2 surface). Changes to Zone 2 entry surfaces and the pre-creation form affect the entry state of Persona 2 before the primary instrument cluster is consulted. Tier 1 applies.

**Sections required by tier:**

| Section | Tier 1 | Tier 2 | Tier 3 |
|---|---|---|---|
| Persona Trace (7-element) | Required | Elements P-1–P-5, P-6 if Persona 2 | Not required |
| UX Implication Statement (7-element) | Required — UX Designer sign-off | UX Designer trace review | Not required |
| Forward Trace Statement | Not applicable | Not applicable | Required |
| Silent Failure Mode | Required | Required | Required |
| Asymmetry Assessment | Required if analytical capability | Required if analytical capability | Not applicable |
| North Star Test | Required | Recommended | Not required |
| Mission Impact Statement | Required | Required | Not required |

---

## Status

`Proposed`

---

## Validity Context

> *Fill in when the ADR is accepted.*

**Standards Version:** 2026-06-15 (CLAUDE.md) / 2026-06-09 (ADR template)
**Valid Until:** M15 — review required if provenance API contracts change or entity selection is extended beyond single-entity scenarios
**License Status:** `PROPOSED` — 2026-06-15

**Panel:**
- Architect Agent (R — author)
- UX Designer Agent (R — sign-off required before acceptance vote)
- Frontend Architect Agent (C — creation form and grounding strip implementation)
- Data Architect Agent (C — API contract authority: owns `api_contracts.yml`; `/initial-state` and `/data-quality` schema additions require DA review)
- Chief Methodologist (C — provenance data content: defines what constitutes a valid source citation and vintage; analogous-case selection logic for Fidelity contextualisation)
- Business PO (C — validate north star test and Demo 5 scope fitness)
- Engineering Lead (A — accountable on all ADR decisions)

**Renewal Triggers:**
- Provenance API is expanded to cover new data sources or new source registries
- Entity selection is introduced beyond the single-entity GRC constraint (IC-1 fix)
- Mode 3 introduces real-time parameter updating that changes what "parameters set at creation" means
- The Fidelity panel analogous-case logic is replaced by a systematic similarity algorithm

---

## Date

2026-06-15

---

## Context

### Background

WorldSim's minister-in-the-chair exercise (Part II: Input Confidence Audit, 2026-06-15, `docs/demo/m14/reviews/2026-06-15-ux-input-confidence-audit-minister-exercise.md`) identified a structural gap in the trust architecture: the tool gives the minister no way to verify that the model was given the right information before she relies on what it says. She can see what the model produced. She cannot see what the model was given.

The audit identified seven input confidence gaps (IC-1 through IC-7):

- **IC-1 — Scenario Creation Blindness:** Three-field creation form (name, year, fiscal multiplier only). Entity hardcoded to GRC. No pre-creation data quality preview. Minister commits to a scenario without knowing whether the model will use Tier 1 IMF data or Tier 4 synthetic inference for her year.
- **IC-2 — Initial State Opacity:** The model's starting conditions at step 0 — actual indicator values used to seed the trajectory — are not visible anywhere in the primary viewport. The minister sees "Financial: 0.81" at step 0 but cannot see the component indicators that produced it (reserve coverage months, current account % GDP, debt service ratio).
- **IC-3 — Data Provenance Invisible at Scenario Level:** No API call during the observed scenario load sequence fetches data source attribution, data vintage, or data provenance at the indicator level. This data may exist in the system; it is not surfaced to the primary UI.
- **IC-4 — Fidelity Panel Scope Mismatch:** The Fidelity panel validates the model relationship (5 historical cases, directional accuracy). It does not validate input data for the active scenario. It is not scenario-contextual — the same content appears regardless of which scenario is loaded. This creates a dangerous partial transparency: present enough to satisfy the expectation of disclosure, but answering a different question.
- **IC-5 — Parameter Persistence Failure:** Only the fiscal multiplier persists in Zone 0 post-creation. All other parameters — conditionality schedule, political economy settings, n_steps rationale — are invisible after the scenario is created.
- **IC-6 — Choropleth Disconnect:** The choropleth occupies ~55% of the total viewport when a scenario is loaded. It shows static world reference data, not the active scenario's computed values or input data. The relationship between the choropleth and the active scenario is not stated anywhere on screen.
- **IC-7 — Internal Field Names in User-Facing Text:** Raw database field names appear as user-facing labels ("financial_active," "ecological_active," "Gdp Usd Millions (USD_millions_cur▼)"). The `_active` suffix is ambiguous; the format strings are implementation details, not analytical labels.

The audit was conducted on software version `v0.13.0-2-g097d3dc` (2 commits post M13 release tag v0.13.0, M14 active). Every observation is from the live running application at localhost:5173 using Playwright screenshots and DOM text extraction.

ADR-015 (Evidence Thread Architecture, ARCH-009) addresses the complementary output legibility gap family (ML-1 through ML-7). The two architectures are distinct and complementary. Evidence threads run forward from output to basis: "what produced this and at what confidence?" Grounding surfaces run backward from output to input: "what was the model told before it produced this?" Both are required for a finance minister to trust what she sees enough to defend it at a negotiating table.

**M14 sequencing:** This ADR is Wave 1 of the M14 trust architecture work. ADR-015 (Wave 2) moves to Accepted only after this ADR is Accepted. EL decision recorded 2026-06-15.

### Problem Framing

Persona 2 (Finance Ministry Negotiator) is in the Reactive entry state — she has opened WorldSim in a negotiating room with a 90-second ceiling to read a Zone 1 output and translate it into a negotiating position. Before she can do that, she faces an input challenge from the creditor side: "What data are you using for Jordan's current account deficit?"

This challenge is unanswerable from the current screen in any amount of time. The minister would need to have separately documented which data the model used and where it came from — not from the tool, but from a separate briefing document she prepared before the session. The input challenge eliminates the tool's usefulness not by disproving the methodology but by undermining the starting conditions. The creditor side has access to IMF data systems in real time; they can produce the alternative figure on demand.

The Preparatory entry state is equally affected: Persona 2 building a scenario for a planning session cannot choose what country she is modeling (GRC hardcoded), cannot see what data quality profile exists for her intended country before committing to the scenario, and cannot recover starting condition information the day after scenario creation.

The creation form as observed makes WorldSim, from the minister's perspective, a Greece-only analytical instrument — the Jordan/Egypt scenario visible in the instrument cluster was created through a pathway not accessible from the creation form.

---

## Decision

The Scenario Grounding Architecture introduces four components addressing the IC-1 through IC-7 gap family. Each component is defined to implementation-specification precision. Scope decisions (which components are in-scope for M14 vs. deferred) require EL confirmation before implementation begins — see §Decisions Required.

### Component 1 — Entity Selection and Pre-Creation Data Quality Preview

**What changes:**
The scenario creation form receives two additions:
1. An entity selector (replacing the hardcoded GRC constraint — IC-1)
2. A data quality preview panel that updates dynamically as the user selects entity and year (IC-1)

**Entity selector specification:**
- A dropdown or searchable selector showing available entities (at minimum all entities currently supported by the backend data layer, using ISO 3166-1 alpha-3 codes with human-readable country names)
- Default: GRC (preserving current behaviour for users who do not change it)
- The selector must be functional at scenario creation time — not a future extension placeholder

**Data quality preview specification:**
- Triggers on entity + year selection (both must be set before preview appears)
- Displays one row per measurement framework: Financial, Human Development, Ecological, Governance, Political Economy
- Each row shows: framework name, confidence tier (T1–T5), source institution abbreviation, data vintage (year or quarter)
- Format: `Financial — T2 · IMF BOP · 2024-Q1`
- If a framework has no data for the selected entity/year: `Financial — T4 (synthetic — no observed data for JOR 2024)`
- The word "synthetic" must appear verbatim for T4 entries (per `docs/DATA_STANDARDS.md §Confidence Tier System`)
- Preview is read-only — it does not prevent scenario creation. A minister choosing a Tier 4 scenario receives the signal but is not blocked.
- Source: the preview is computed from the source_registry at request time, not cached at build time. The API endpoint is specified in §API Contract.

**API contract for data quality preview:**
```
GET /api/v1/entities/{entity_id}/data-quality?year={year}
Response:
{
  "entity_id": "JOR",
  "year": 2024,
  "frameworks": [
    {
      "framework": "financial",
      "confidence_tier": 2,
      "source_institution": "IMF BOP",
      "data_vintage": "2024-Q1",
      "is_synthetic": false
    },
    {
      "framework": "ecological",
      "confidence_tier": 4,
      "source_institution": null,
      "data_vintage": null,
      "is_synthetic": true,
      "synthetic_basis": "MENA comparable economies 2022-2023"
    }
  ]
}
```
If no data exists for the entity/year combination, the endpoint returns an empty frameworks array (not a 404) — the frontend must handle this as "no data available."

**IC gaps addressed:** IC-1 (primary), IC-3 (partial — establishes the data tier provenance chain at creation time)

---

### Component 2 — Scenario Grounding Strip

**What changes:**
A "Grounding" surface is introduced, accessible at one interaction from the primary viewport (Zone 2). The surface is linked from a "Grounding ▼" button adjacent to the existing "Fidelity ▼" button in Zone 0/Zone 2 entry area. When opened, it shows the model's starting conditions for the active scenario.

**Grounding strip specification:**
- Displays the scenario's initial state table: for each measurement framework, the top 2–3 component indicator values used to seed the trajectory at step 0, with source citation and data vintage
- Layout: one card per framework, each card showing indicator rows in the format:
  `[Indicator name]: [value] [units]   [Source · Vintage · Tier]`
- Example:
  ```
  Jordan — Starting conditions at step 0 (2023)

  Financial
    Reserve coverage: 3.2 months    IMF BOP 2024-Q1 · T2
    Current account: −6.8% GDP      IMF Article IV 2023 · T2
    Debt service ratio: 18.4%       World Bank 2023 · T2

  Human Development
    Bottom quintile consumption: 0.62 (index)   World Bank WDI 2023 · T3
    Unemployment: 17.8%                         ILO ILOSTAT 2023 · T2

  Political Economy
    Programme survival probability: 0.67        V-Dem 2023 + political economy module · T3

  Ecological
    CO₂ per capita: 3.1 tCO₂eq    synthetic · MENA comparable · T4
  ```
- Synthetic indicators (T4) display the word "synthetic" verbatim and name the comparable economy or inference basis
- T5 (Structural Absence Declaration) indicators display: `[indicator name]: No data — Structural Absence Declaration. Do not interpolate.`
- The grounding strip is scenario-contextual — it reflects the active scenario's entity, year, and step 0 values. Switching scenarios updates the grounding strip.
- The strip shows step 0 values only. It is a "what we started with" surface, not a trajectory tracker (that is Zone 1).

**API contract for grounding strip:**
```
GET /api/v1/scenarios/{scenario_id}/initial-state
Response:
{
  "scenario_id": "...",
  "entity_id": "JOR",
  "step_0_year": 2023,
  "frameworks": {
    "financial": {
      "indicators": [
        {
          "name": "reserve_coverage_months",
          "display_name": "Reserve coverage",
          "value": 3.2,
          "unit": "months",
          "source": "IMF BOP",
          "vintage": "2024-Q1",
          "confidence_tier": 2,
          "is_synthetic": false
        }
      ]
    }
  }
}
```

**IC gaps addressed:** IC-2 (primary), IC-3 (primary), IC-5 (partial — step 0 parameter values for initial state)

---

### Component 3 — Fidelity Panel Contextualisation

**What changes:**
The Fidelity panel retains all existing content (five historical cases, directional validation, structural gap documentation with issue references). When a scenario is loaded, a scenario-contextual section is appended to the top of the panel content.

**Contextualisation section specification:**
- Appears only when a scenario is active. The existing panel content appears unchanged when no scenario is loaded.
- Content: a one-paragraph plain-language summary contextualising the backtesting evidence for the active scenario's situation
- Format:
  ```
  For your scenario ([entity_ids] · [year]): The most analogous validation case is [case name]
  ([year], [brief description of mechanism match]). Directional accuracy has been validated for
  this crisis mechanism. Magnitude [has / has not] been validated for this entity type. Use
  outputs for [direction and threshold detection / direction only]; [confirm magnitudes with
  country-specific analysis before citing / magnitude outputs carry high uncertainty at this
  validation stage].
  ```
- The "most analogous validation case" selection requires Chief Methodologist definition of the similarity logic before implementation (see §Decisions Required Decision 5)
- Plain-language minimum: "5/5 direction checks passed — the model correctly identified whether conditions improved or worsened in five historical crises. Magnitude (how much) has been validated in one of five cases."
- The contextualisation section does not modify the existing five-case cards or structural gap documentation

**IC gaps addressed:** IC-4 (primary)

---

### Component 4 — Parameter Persistence in Zone 0

**What changes:**
All parameters set at scenario creation are persisted in a visible, recoverable form. The current Zone 0 shows "Mode: 2 (Fiscal ×1.3)" — only the fiscal multiplier. This component extends persistence to all scenario-defining parameters.

**Parameter persistence specification:**
- A "Scenario Parameters" entry in Zone 0 or Zone 2 (one interaction from Zone 0) displays the full parameter set used in the active scenario
- At minimum for M14: fiscal multiplier (already present), n_steps, base_year, entity, conditionality_preset (or equivalent political economy defaults)
- Parameters that were applied as system defaults (not explicitly set by the user at creation) are visually distinguished — e.g., a "(default)" indicator or a dimmed style — so the minister knows which settings she chose vs. which were applied automatically
- Format example:
  ```
  Scenario Parameters
    Entity: JOR (Jordan) · EGY (Egypt)
    Base year: 2023
    Steps: 8
    Fiscal multiplier: 1.30
    Conditionality: standard (default)
    Political economy: enabled (default)
  ```
- The parameter display is read-only in Mode 2 (Simulation). It is a record surface, not an editing surface.
- Linked from Zone 0 "Mode" chip at one interaction — clicking the mode indicator opens the parameter display.

**IC gaps addressed:** IC-5 (primary)

---

### Out of Scope for ADR-016

The following IC gaps are acknowledged but not addressed by this ADR:

- **IC-6 (Choropleth Disconnect):** The choropleth's role, visual dominance vs. analytical relevance, and its relationship to the active scenario are an information architecture concern that belongs in a broader Zone 2/Zone 3 layout review. Tracked in Issue #845 (Zone 1A information architecture design-first).
- **IC-7 (Internal Field Names):** Raw field name exposure in trajectory chart legend text and attribute selector labels. Addressed separately by the three prerequisite bugs (#962: step counter, #963: choropleth header). The trajectory chart legend field names (`financial_active`, `ecological_active`) are a frontend display layer fix that does not require an ADR — they are a CODING_STANDARDS.md §Label Standards compliance finding.

---

## Persona and UX Traceability

### [Tier 1] Persona Trace

**P-1 — Persona identification:**
Primary: Persona 2 — Finance Ministry Negotiator (Eleni Papadimitriou archetype). The negotiator building a scenario for use in a sovereign debt restructuring session, and the negotiator responding to input challenges at the table.

Secondary: Persona 3 — Policy Analyst / Country Economist (Kofi Otieno archetype). The analyst building scenarios for a finance ministry team, who inherits scenarios created by colleagues and must understand what parameters and data were applied.

**P-2 — Entry state:**
- **Preparatory** (primary): Persona 2 building a scenario before a negotiation session. Time ceiling: no strict ceiling, but the scenario creation workflow should complete within 5 minutes including data quality review. The IC-1 gap (GRC hardcoded) blocks this entry state entirely for non-Greece scenarios.
- **Reactive** (secondary): Persona 2 in the negotiation room receiving an input challenge ("your Jordan current account assumption is wrong"). Time ceiling: 90 seconds to produce a source-cited response. Currently impossible from the screen.
- **Retrospective** (secondary): Persona 3 reviewing a colleague's scenario the day after creation. Cannot currently determine what parameters were applied.

**P-3 — Journey reference:**
- Closes Journey A Step 1 [Near-Term-Gap] — entity selection at scenario creation ("Scenario creation is currently GRC-only; entity selection is a known gap")
- Closes Journey A Step 2 [Near-Term-Gap] — data quality disclosure at scenario creation
- Introduces Journey B Step 0 (new) — input challenge response in Reactive state: Persona 2 opens Grounding strip, reads starting condition with source citation, produces response at the table within 90 seconds
- Addresses Journey A Step 3 [Near-Term-Gap] — scenario parameter inspection post-creation (Parameter Persistence, Component 4)

**P-4 — Time or interaction ceiling:**
- Pre-creation data quality preview: visible in the creation form within 2 seconds of entity + year selection (no additional interaction beyond typing/selecting)
- Grounding strip: visible within 1 interaction from Zone 0 (clicking "Grounding ▼") and must display full initial state within 3 seconds of opening
- Reactive entry state input challenge response: Persona 2 must be able to identify the relevant source citation for a named indicator within 90 seconds of receiving the challenge. Observable criterion: from Zone 0 (no scenario change required), Persona 2 opens Grounding strip and reads "[indicator]: [value] [source · vintage · tier]" for the challenged indicator within 90 seconds.
- Parameter display: visible within 1 interaction from Zone 0

**P-5 — Income cohort served:**
- Component 2 (Grounding strip) explicitly includes bottom quintile consumption as a required initial state indicator when Human Development framework data is available (per Development Economist DIC challenge: "the starting point — which determines the human severity of the change — is invisible")
- Component 1 (pre-creation preview) provides per-framework coverage quality, not per-cohort. Per-cohort initial state disaggregation is a downstream capability; current ADR provides the infrastructure (initial-state API) on which it can be built
- Political economy initial state (programme_survival_probability at step 0) is included in Component 2 where T3 or better data is available

**P-6 — Negotiating leverage statement:**
After accessing this capability, Persona 2 can make the following specific argument:

> "The model uses Jordan's current account deficit as reported in the IMF 2023 Article IV Consultation — 6.8% of GDP as of year-end 2022. That figure is Tier 2 confidence — observed data, not synthetic. If the creditor side uses a different figure, they need to produce their source. Here is ours."

Previously: Persona 2 could not identify what current account figure the model used, from what source, or at what vintage, from any screen in the application.

**P-7 — North star test answer:**

A Zambian finance ministry analyst opens WorldSim before a debt restructuring session with the IMF. She wants to model Zambia's 2024 situation. Under the current system: the creation form is hardcoded to GRC (Greece). She cannot model Zambia. If she could select Zambia, she would receive no signal about whether the 2024 data is IMF-observed or synthetic inference from comparable Sub-Saharan economies.

After ADR-016: She selects Zambia (ZMB) from the entity selector, enters 2024, and immediately sees "Financial — T2 · IMF BOP 2024-Q1 · Human Development — T3 · World Bank WDI 2023 · Ecological — T4 synthetic · SADC comparables · Political Economy — T3 · V-Dem 2023." She understands before creating the scenario that ecological outputs are synthetic and should not be cited without qualification. She creates the scenario. In the session, a creditor representative challenges the reserve coverage assumption. She opens the Grounding strip, reads "Reserve coverage: 1.8 months — IMF BOP 2024-Q1 · T2," and responds with a source citation within 45 seconds.

This closes the asymmetry in which the IMF team can challenge the input data and the minister has no recorded basis to respond. It is not the only asymmetry in the negotiating room; it closes the input-side half. ADR-015 closes the output-side half.

---

### [Tier 1] UX Implication Statement

**UX-1 — Zone assignment and hierarchy certification:**
- Component 1 (entity selector + data quality preview): modifies the scenario creation form. The creation form is a Zone 2 entry point — one deliberate interaction (clicking "Scenarios ▼") from the primary viewport. This assignment is consistent with `information-hierarchy.md §Zone 2 — One-Interaction Surfaces`. The creation form modification does not add a new zone; it adds capability to an existing Zone 2 surface.
- Component 2 (Grounding strip): introduces a new Zone 2 surface ("Grounding ▼") alongside the existing "Fidelity ▼" button. Consistent with `information-hierarchy.md §Zone 2` — one interaction from Zone 0, not embedded in Zone 1. The Grounding strip does not displace any Zone 1 instrument.
- Component 3 (Fidelity contextualisation): modifies an existing Zone 2 surface (Fidelity panel). No zone reassignment.
- Component 4 (Parameter persistence): adds a Zone 2 sub-surface accessible at one interaction from the Zone 0 mode chip. Consistent with `information-hierarchy.md §Zone 0 — Always-Visible Identity Strip` — extending Zone 0 to link to Zone 2 parameter detail, not embedding the parameter detail in Zone 0 itself.

**UX-2 — Primary cognitive task alignment:**
- Mode 2 (Simulation — threshold-safe path construction): ADR-016 primarily serves Mode 2. In the Preparatory state (scenario construction), Persona 2 is building the scenario she will use in Mode 2 simulation. The data quality preview (Component 1) and grounding strip (Component 2) directly serve the Mode 2 cognitive task by establishing that the inputs are trustworthy before she commits to path construction.
- Mode 1 (Replay — trajectory reconstruction): grounding strip is equally relevant in Mode 1. Understanding what data was fed to the model at step 0 is prerequisite to reconstructing what the trajectory means.
- Mode 3 (Active Control — real-time steering): parameter persistence (Component 4) is relevant for Mode 3's real-time steering; the minister needs to know what baseline parameters are in effect as she adjusts control inputs. ADR-016 does not need to be reworked for Mode 3 — the parameter display extends naturally to Mode 3 when that mode is built.

**UX-3 — Entry state coverage (falsifiable acceptance criteria):**

1. **Preparatory entry state — entity selection (IC-1):**
   Acceptance criterion: A first-time user navigates to the scenario creation form ("Scenarios ▼"), sees an entity selector, types "Jordan" or "JOR," selects Jordan, enters year 2024, and sees a data quality preview for Jordan 2024 within 2 seconds, without any additional interaction. Observable: Playwright test loads creation form, types entity name, verifies `[data-testid="data-quality-preview"]` is present and contains "JOR" and "2024" and at least one confidence tier label (T1–T5).

2. **Preparatory entry state — data quality preview (IC-1 + IC-3):**
   Acceptance criterion: For any entity where at least one framework has T4 synthetic data, the word "synthetic" appears verbatim in the data quality preview. Observable: Playwright test selects an entity with known synthetic ecological data, verifies `[data-testid="data-quality-preview"]` contains the text "synthetic."

3. **Reactive entry state — grounding strip input challenge (IC-2 + IC-3):**
   Acceptance criterion: With the Jordan 2024 scenario loaded in Zone 1, Persona 2 clicks "Grounding ▼" (one interaction), and within 3 seconds sees a panel containing the current account value at step 0 with its source institution and data vintage. Observable: Playwright test with Jordan scenario loaded, clicks grounding button, verifies `[data-testid="grounding-strip"]` is present and contains at least one indicator row with a non-empty source citation.

4. **Retrospective entry state — parameter persistence (IC-5):**
   Acceptance criterion: With a scenario loaded, the fiscal multiplier, base year, entity, and n_steps are all visible within 1 interaction from Zone 0 (clicking the mode chip). Observable: Playwright test with any completed scenario, clicks mode chip or parameter display trigger, verifies `[data-testid="scenario-parameters"]` contains all four named values.

5. **No entry state — Fidelity contextualisation (IC-4):**
   Acceptance criterion: With a scenario loaded, the Fidelity panel shows a scenario-contextual section at the top that names the active scenario's entity and year and references the most analogous historical validation case. Observable: Playwright test with scenario loaded, opens Fidelity panel, verifies `[data-testid="fidelity-contextualisation"]` contains the active scenario's entity_id and a reference to one of the five validated historical cases (GRC, ARG, LBN, THA, ECU).

**UX-4 — HCL parity certification:**
This ADR adds the initial state of the Human Development framework (including bottom quintile consumption at step 0) as a required entry in the Grounding strip (Component 2). This increases HCL visibility relative to the previous state (where it was invisible at step 0). HCL parity is maintained and improved — the grounding strip treats Financial, Human Development, Ecological, Governance, and Political Economy frameworks with equal visual weight in the indicator cards. No HCL subordination occurs in any component.

**UX-5 — Uncertainty display specification:**
- **Data quality preview (Component 1):** Confidence tier appears as T1–T5 label. For T4 entries, the format is: `[framework] — T4 (synthetic — [inference basis])`. The word "synthetic" appears verbatim. For T5, the format is: `[framework] — T5 (no data — Structural Absence)`. The label "Structural Absence" appears verbatim.
- **Grounding strip (Component 2):** Each indicator row shows the confidence tier as part of the source citation: `[Source · Vintage · T{N}]`. For T4 indicators, the row includes "synthetic" verbatim in the source field. For T5 indicators, the indicator displays: `[indicator name]: No data — Structural Absence Declaration. Do not interpolate.` The phrase "Do not interpolate" appears verbatim.
- **Fidelity contextualisation (Component 3):** No new confidence tier display. The contextualisation text references the validation status (direction validated / magnitude not validated) in plain language but does not add T1–T5 tier labels to the existing Fidelity panel content.

**UX-6 — Irreversibility signal integrity certification:**
No components of this ADR touch Zone 1 instrument displays, the MDA alert panel, or severity classification. The Grounding strip (Component 2) includes initial state indicator values but does not display severity alerts. TERMINAL/CRITICAL distinction integrity is unaffected by this ADR.

Certification: ADR-016 does not modify Zone 1, alert severity display, or TERMINAL/CRITICAL visual treatment. No impact on irreversibility signal integrity.

**UX-7 — User journey coverage:**
- **Journey A (Scenario Preparation) — Steps 1–3 [Near-Term-Gap]:** Components 1 and 4 close the entity selection gap and parameter persistence gap in Journey A. After implementation: Persona 2 can select any supported entity, see data quality before committing, and inspect all creation parameters post-creation.
- **Journey B (Reactive Analysis) — Step 0 (new, introduced by this ADR):** Component 2 enables a new journey step: input challenge response in the Reactive entry state. The journey step was previously impossible because the input data was inaccessible.
- **Journey B Step 2 (Fidelity check):** Component 3 improves Journey B Step 2 by adding scenario-contextual trust calibration. Previously: Fidelity panel provided global model validation. After: Fidelity panel contextualises validation to the active scenario's crisis mechanism type.

**UX Designer sign-off:**
This sign-off is a precondition for the acceptance vote. All four fields are required.

**Reviewing agent:** UX Designer Agent
**Session context:** `Same session as ADR authorship — acknowledged`
**Governing documents reviewed:** `information-hierarchy.md §Zone 2 — One-Interaction Surfaces`; `north-star.md §Primary Cognitive Tasks`; `user-journeys.md §Journey A`, `user-journeys.md §Journey B`; `personas.md §Persona 2 Finance Ministry Negotiator`, `personas.md §Persona Conflict Resolution`
**Concerns found:** 3 — listed below:

1. **IC-6 and IC-7 deferred scope:** The choropleth disconnect (IC-6) and field name exposure (IC-7) are excluded from this ADR's scope. IC-7 is handled as a coding standards compliance fix (correct). IC-6 (choropleth visual dominance with no analytical content) is a Tier 1 concern — the choropleth occupying 55% of the viewport while showing reference-only data creates a false affordance that no label can fix. The UX Designer recommends EL review whether IC-6 should be a separate Tier 1 ADR before ADR-016 implementation begins, or whether IC-6 is acceptable to defer to M15 as part of a broader Zone 2/Zone 3 layout review. This is recorded as a concern, not a blocker — the EL may accept the deferral.

2. **Analogous-case selection for Fidelity contextualisation:** Component 3 defers the analogous-case selection logic to Chief Methodologist definition (Decision 5 in §Decisions Required). If the Chief Methodologist has not defined this logic before frontend implementation begins, Component 3 cannot be implemented to spec. The UX Designer recommends that Decision 5 be resolved before Component 3 implementation begins (independently of Components 1, 2, and 4, which can proceed earlier).

3. **Parameter display — read-only in Mode 2 but future Mode 3 implication:** Component 4 specifies the parameter display as read-only in Mode 2. In Mode 3 (Active Control), parameters may be adjusted in real time. The current spec defers Mode 3 parameter editing to the Mode 3 ADR. The UX Designer confirms this is consistent with the Mode 3 zone reservation (`CLAUDE.md §UX Architectural Commitments §5`) and does not conflict with this ADR. Concern is informational — no blocking issue.

`[ ]` UX Designer sign-off. 2026-06-15

---

## Silent Failure Mode

**Component 1 (data quality preview):**
If the `/api/v1/entities/{entity_id}/data-quality` endpoint is unavailable or returns an error, the creation form must display a visible fallback state — not a silent empty state. Acceptable fallback: "Data quality preview unavailable. You can still create the scenario. Check data tier after creation via Grounding ▼." Unacceptable: no preview with no message (user proceeds assuming data quality was verified). Detection: Playwright test simulates API failure and verifies fallback text is displayed.

**Component 2 (grounding strip):**
If the `/api/v1/scenarios/{scenario_id}/initial-state` endpoint returns no indicator data (empty frameworks object), the grounding strip must display: "Initial state data not available for this scenario. Scenario may have been created before grounding data was indexed." Unacceptable: empty strip with no message. An empty grounding strip is indistinguishable from a successfully loaded grounding strip with a zero-indicator scenario — the user has no way to know whether the absence of data is correct or a failure. Detection: Playwright test with a scenario_id that has no initial-state data verifies fallback text is displayed.

**Component 3 (Fidelity contextualisation):**
If the analogous-case selection logic fails to identify a matching case (no cases match the active scenario's crisis mechanism), the contextualisation section displays: "No analogous validation case identified for this scenario type. Global backtesting results apply — see validation cases below." Unacceptable: contextualisation section absent from the Fidelity panel when a scenario is loaded (user cannot tell whether the absence is intentional or a loading failure). Detection: the contextualisation section must always render when a scenario is active, even if its content is the fallback message.

**Component 4 (parameter persistence):**
If scenario metadata is missing parameters that should have been recorded at creation (e.g., conditionality_preset is null in the database because the scenario was created before this feature was introduced), the parameter display shows the value as "(not recorded — scenario predates parameter persistence)" rather than silently omitting the row. The full parameter list must always be visible; absent values must be marked as absent, not omitted. Detection: Playwright test with a legacy scenario verifies parameter display shows all expected rows, including rows with "(not recorded)" for missing values.

---

## Asymmetry Assessment

Well-resourced actors with IMF data systems, Bloomberg subscription data, or creditor syndicate analytics can access real-time indicator data for any sovereign entity, including source attribution and vintage, while constructing scenario analyses. They can challenge a ministry's input data from a well-sourced position at any point in a negotiation.

WorldSim's proposed ADR-016 closes this asymmetry for entities and years covered by the source registry, at the data tier available in the source registry. After implementation: the ministry team can identify, within 90 seconds, what data the model used for any challenged indicator, including source institution and vintage. The ministry does not need a Bloomberg terminal to know what went into their scenario — it is on the screen.

The remaining gap after this ADR: for Tier 4 (synthetic) indicators, the ministry can state that the value is synthetic inference from comparable economies but cannot cite a primary data source — because none exists. This is the correct representation of the epistemic situation; the tool is honest about it (T4 with "synthetic" verbatim). The creditor side may still produce a Tier 1 observed figure that the ministry cannot match for Tier 4 indicators. This gap is structural — it is the data poverty that WorldSim's synthetic data framework exists to signal, not to conceal.

---

## North Star Test

A Zambian finance ministry analyst sits across from an IMF negotiating team during a sovereign debt restructuring session. The IMF team challenges the ministry's GDP trajectory by claiming the ministry's model used an outdated current account deficit assumption — "your figure is 6.8%, our latest Article IV has 7.9%." Under the current system, the analyst cannot respond from the screen — the current account figure the model used is not visible at any zoom level, and the analyst has no way to recover it without accessing the backend directly.

After ADR-016: The analyst opens the Grounding strip (one click). Within 3 seconds she reads: "Current account: −6.8% GDP · IMF Article IV 2023 · T2." She responds: "The model uses the IMF 2023 Article IV figure. If your team's 2025 update differs, please produce the reference — our model can be updated with your figure before the next session." She has responded to the input challenge with a source citation, matched the creditor side's evidentiary standard, and identified the specific mechanism for updating the scenario to address the discrepancy.

Previously: this argument was unavailable. The analyst could not answer "what data are you using?" from the screen. The tool existed but could not be defended at the table — which is the primary failure mode the north star test is designed to detect.

---

## Mission Impact Statement

This ADR closes the input confidence gap family (IC-1 through IC-5, with IC-6 and IC-7 addressed by adjacent work), identified as the second half of the trust architecture required for WorldSim to serve Persona 2 in a live negotiating context. The complete trust architecture — Evidence Thread Architecture (ADR-015) + Scenario Grounding Architecture (ADR-016) — is the minimum viable configuration for the tool to serve its primary mission: a finance ministry team that can produce and defend a sovereign debt scenario analysis against a well-resourced creditor.

The direct impact on the finance ministry side of a sovereign debt negotiation: the ministry analyst can now answer input challenges with source citations derived from the tool itself — not from a separate briefing document she prepared independently. The tool becomes self-contained as an evidentiary instrument, not just a computation engine.

Technical completeness without this mission relevance assessment is insufficient for acceptance. The three prerequisite bugs (#961 entity hardcoding, #962 step counter, #963 choropleth field names) are M14 housekeeping items that lower the barrier to Demo 5 but do not close this structural gap. ADR-016 closes the structural gap.

---

## Minimum Data Tier

Minimum data tier at which this capability produces actionable output: **Tier 3** for Component 2 (Grounding strip) and Component 1 (data quality preview). At Tier 4 (synthetic), both components produce output — the word "synthetic" appears verbatim, the comparable-economy basis is named — but the minister cannot produce a primary source citation. Tier 4 output is actionable for scenario exploration; it is not citable at a negotiating table.

For users in Tier 4 data environments (entities where the source registry has only synthetic inference), the grounding strip and data quality preview remain functional but surface the honest limitation: "Tier 4 (synthetic inference — no observed data for [entity_id] [year])." The tool does not hide the Tier 4 status behind a display that makes it look like observed data.

This is a capability accessibility threshold, not an accessibility gap. The tool is usable at Tier 4; the limitation is disclosed. Users who need T1–T2 citable input data for negotiating use must use the tool in entities and years where the source registry has T1–T2 coverage. That constraint is correct, not a failure.

---

## Alternatives Considered

### Alternative 1 — Inline initial state display in Zone 1 (always visible)

Display the initial state indicators directly in the Zone 1 instrument cluster — either as a persistent strip at the top of the cluster or as a collapsible Zone 1 surface.

Rejected: Violates `CLAUDE.md §UX Architectural Commitments §2` — "Instruments are always visible; context is navigable." The initial state display is context (what the model was given), not an instrument (what the model produced). Placing it in Zone 1 would either displace Zone 1 instruments or add a Zone 1 surface that is not a primary flight instrument. The Zone 2 placement (Grounding strip) is consistent with the information hierarchy — accessible at one interaction, not competing for primary attention.

### Alternative 2 — Extend the entity drawer to show initial state

Make the initial state (IC-2) accessible through the existing entity drawer (Zone 3 — deliberate navigation) rather than introducing a new Zone 2 Grounding strip.

Rejected: The entity drawer is Zone 3 (deliberate navigation, multiple interactions). The Reactive entry state input challenge response requires access within 90 seconds and one interaction from Zone 0. The entity drawer cannot meet this ceiling by definition. Additionally, the entity drawer was inaccessible from Zone 1 entity labels in the live UI audit (Recharts SVG intercept blocked the click path). A Zone 3 solution for a Zone 2 need fails the time ceiling.

### Alternative 3 — Server-side data quality annotation embedded in scenario metadata

Embed the confidence tier and source information for all indicator values into the existing `/api/v1/scenarios/{id}/trajectory` response, eliminating the need for separate API endpoints.

Rejected: The trajectory endpoint returns computed outputs (composite scores, step trajectories). Embedding input source annotation in the output trajectory response conflates two distinct data layers: what the model produced vs. what the model was given. The two endpoints (`/initial-state` and `/trajectory`) serve distinct analytical purposes and should remain distinct. The trajectory endpoint can reference the initial-state endpoint; it should not absorb its content.

### Alternative 4 — Pre-creation preview only (skip grounding strip)

Implement only Component 1 (data quality preview at creation time) and skip the post-creation Grounding strip (Component 2).

Considered but not preferred. Component 1 alone addresses IC-1 (entity selection) and IC-1's data quality signal but does not address IC-2 (initial state opacity) or the Reactive entry state input challenge response. A minister who created the scenario three days ago cannot recover the specific indicator values from memory. The 90-second response requirement in the Reactive state requires the grounding strip to be accessible from the loaded scenario — not just at creation time. Component 1 without Component 2 reduces IC-1 but leaves IC-2 and IC-3 fully open.

---

## Consequences

### Positive

- Closes IC-1 (entity selection): WorldSim becomes a multi-entity analytical instrument from the creation form for the first time. Demo 5 can use any supported entity, not just GRC.
- Closes IC-2 (initial state opacity): The human cost ledger baseline (bottom quintile consumption at step 0) becomes visible, enabling the Development Economist's negotiating argument about baseline severity.
- Closes IC-3 (data provenance): Ministers can respond to input challenges with source citations derived from the tool — within 90 seconds, from Zone 2, without external documentation.
- Closes IC-4 (Fidelity panel scope mismatch): The Fidelity panel gains scenario-contextual content, reducing the risk that a minister reads model calibration evidence as input data evidence.
- Closes IC-5 (parameter persistence): All scenario parameters become recoverable from the screen for any loaded scenario, including legacy scenarios (where absent values are marked, not omitted).
- Establishes the backend API infrastructure (`/initial-state`, `/data-quality`) that subsequent capability enhancements (per-cohort initial state disaggregation, Tier 3+ data vintage tracking) can extend without additional ADR scope.

### Negative

- Adds two new API endpoints (`/initial-state` and `/data-quality`) that must be populated correctly for every entity-year combination in the source registry. If the source registry is incomplete or inconsistent, the grounding strip may show inaccurate or misleading source attributions — which is worse than showing nothing.
- The "analogous case" selection logic for Fidelity contextualisation (Component 3) requires Chief Methodologist definition that does not currently exist. If this logic is poorly specified, the contextualisation section may produce misleading similarity assessments.
- Component 4 (parameter persistence) requires that legacy scenarios (created before this feature) be handled gracefully. "(not recorded)" display is the specified fallback, but it may expose how many current scenarios in the system were created with non-transparent parameters — a visible record of the prior opacity.
- IC-6 (choropleth disconnect) and IC-7 (field name exposure) are deferred. The choropleth continues to dominate ~55% of the viewport while showing reference-only data until IC-6 is addressed separately.

### Known Limitations

- The Grounding strip shows step 0 values only. Scenario-level data provenance for intermediate steps (data fetched at steps 1–N, where the backend may use different vintage data for different steps) is not in scope for this ADR.
- Component 3 (analogous case selection) is a methodology commitment that the Chief Methodologist must define and validate. An ADR cannot specify what this logic is — only that it must exist before Component 3 can be implemented. This is an explicit dependency on the Chief Methodologist's output.
- Entity selection (Component 1) enables entity choice at the creation form level. It does not guarantee that indicator data exists at T1–T3 for all selectable entities. Selecting an entity for which the source registry has only T4 synthetic data is valid — the tool discloses this — but the minister receives less evidentiary value from the grounding strip for those entities.
- The development economist's full argument ("baseline was already near subsistence") requires per-cohort initial state disaggregation that is not in scope for this ADR. Component 2 shows the Human Development framework composite initial state and the bottom quintile consumption figure where available; it does not show the full income cohort distribution at step 0.

---

## Diagram

`docs/architecture/ADR-016-scenario-grounding-architecture.mmd`

*(Diagram to be authored before implementation begins. Must show: creation form → data quality preview API flow; loaded scenario → grounding strip API flow; Fidelity panel contextualisation trigger; parameter persistence link from Zone 0 mode chip.)*

---

## Backtesting Validation Anchor

ADR-016 does not introduce a new composite score or measurement methodology. It introduces display surfaces for existing data (initial state indicator values from the source registry, parameter metadata from the scenario database, backtesting evidence from the Fidelity panel data).

No backtesting validation anchor required for this ADR. The data displayed by the grounding strip is the model's actual starting state — validated by definition against the source it came from. The Fidelity panel contextualisation draws on the existing five historical cases (GRC, ARG, LBN, THA, ECU), which are already validated in the Fidelity panel data. No new model relationship is introduced.

---

## Decisions Required

The following decisions must be resolved by the Engineering Lead before this ADR moves from Proposed to Accepted. None of these are implementation decisions — they are scope and methodology commitments that bound what the implementing agent builds.

**Decision 1 — Entity selection scope for M14:**
Which entities must be supported in the entity selector at M14 scope? Options: (a) all entities in the current source registry (may be a small set); (b) GRC + Jordan/Egypt (as seen in current scenario list) + ZMB (Zambia, for the north star test scenario); (c) all G20 + G7 + HIPC entities. The choice determines backend data preparation scope. EL decision required.

**Decision 2 — Component 3 (Fidelity contextualisation) in-scope for M14:**
Is the analogous-case selection logic a required M14 deliverable, or is Component 3 a Wave 2 / M15 feature? The Chief Methodologist must define the similarity logic before Component 3 can be implemented. If the Chief Methodologist cannot deliver this logic within M14 scope, Component 3 should be marked as deferred in this ADR and implemented in M15 under a separate intent document. EL decision required.

**Decision 3 — API endpoint design authority:**
The two new API endpoints (`/initial-state`, `/data-quality`) are specified at schema level in this ADR. The implementing Backend agent must read `docs/schema/api_contracts.yml` before implementing. If the schema file does not currently include these endpoints, the Data Architect Agent must add them in the same PR as the implementation — schema drift is a compliance violation. Per `docs/process/agent-raci.md §File Ownership`, `api_contracts.yml` is owned by the Data Architect Agent (R); the Architect Agent is consulted when response shape changes. The Chief Engineer is consulted on implementation-level computational implications (query performance, database access patterns) but does not hold authority over the API contract itself. No EL confirmation required — the RACI is unambiguous.

**Decision 4 — Parameter persistence backward compatibility:**
How should legacy scenarios (created before this feature) be handled in the parameter display? The specified fallback is "(not recorded — scenario predates parameter persistence)." Is this acceptable UX for the Demo 5 scenario set? If Demo 5 scenarios need clean parameter records, they may need to be recreated after implementation, not just loaded from the existing scenario list. EL decision required before implementation begins.

**Decision 5 — IC-6 (choropleth) scope:**
The UX Designer raised IC-6 (choropleth visual dominance with reference-only data) as a Tier 1 concern not addressed by this ADR. EL should decide: (a) IC-6 is deferred to M15 as part of a broader Zone 2/Zone 3 layout review; (b) IC-6 requires a separate Tier 1 ADR before ADR-016 implementation begins; (c) IC-6 is accepted as a known limitation explicitly recorded in the documentation visible to Demo 5 participants. This decision bounds whether ADR-016 implementation can begin before IC-6 is addressed.

---

*ADR-016 authored by Architect Agent, 2026-06-15. Evidence base: `docs/demo/m14/reviews/2026-06-15-ux-input-confidence-audit-minister-exercise.md`. M14 Wave 1. Status: Proposed. EL review and acceptance required before Wave 2 (ADR-015 implementation) begins.*
