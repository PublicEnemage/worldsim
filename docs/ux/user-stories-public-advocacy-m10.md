# User Stories — M10 Public Advocacy Personas

> **Owned by:** Business Product Owner Agent (R), UX Designer Agent (C)
> **Authored:** 2026-06-02 — Issue #576
> **Status:** All 19 stories are final. Panel decisions recorded below. QA may begin
> writing acceptance tests against all [Playwright] criteria immediately.
> [Near-Term-Gap] and [Phase-3-TBD] stories are blocked pending scope decision — do not
> begin implementation without a filed tracking issue and EL sign-off.
>
> **Consumers:**
> - **QA Lead** — writes acceptance tests from the Given/When/Then criteria before
>   implementation begins. This is the independent quality gate.
> - **Frontend Architect** — implements to these stories as the user-value specification
>   that governs tradeoff decisions. When an implementation choice conflicts with a story,
>   the story governs — not implementation convenience.
>
> **Source documents read:**
> `docs/ux/personas.md` (Personas 6, 7, 8, 4V — public advocacy section, Issue #575),
> `docs/ux/user-journeys.md` (Journeys E–H, Issue #576),
> `docs/ux/north-star.md`, `docs/ux/information-hierarchy.md`,
> `docs/ux/user-stories-instrument-cluster-m9.md` (format reference, US-001–US-029)
>
> **Panel consulted (Issue #576):**
> PO Agent (R), UX Designer Agent (C), Customer Agent (C).
> Domain experts (Development Economist, Political Economist) not required for this file —
> the architectural classification questions raised by Journeys G and H are UX/PO scope,
> not domain accuracy scope.

---

## Panel Decisions

**Decision 1 — [Phase-3-TBD] scope line**
The threshold between [Phase-3-TBD] and [Near-Term-Gap] is architectural novelty:
[Phase-3-TBD] = no current architectural path (new data ingestion mode, new rendering mode,
new output layer); [Near-Term-Gap] = unbuilt but architecturally straightforward (export,
source attribution display, field label copy, methodology documentation link).
Four stories carry [Phase-3-TBD]: US-039, US-042, US-043, US-048.

**Decision 2 — Layer 3 constraint**
Personas 6, 7, and 8 cannot use specialist mediation. US-030 (plain-language MDA alert)
and US-032 (configuration without specialist) are current-capability [Playwright] stories.
If either fails in QA, it is a blocker — not a deferral.

**Decision 3 — Option C for Persona 8 (civil society monitor)**
Journey G uses Mode 2 to reproduce the committed programme baseline (Scenario A) and an
observed-below-committed spending scenario (Scenario B). The comparison is within current
platform capability. The observed-actuals overlay (Step 6) and community-audience output
layer (Step 7) are [Phase-3-TBD]. No false adequacy: the platform delivers genuine service
(baseline reproduction from an authoritative transparent source) while being honest about
what it cannot yet do. Customer Agent finding recorded in personas.md Persona 8.

**Decision 4 — [Near-Term-Gap] stories**
Nine stories are [Near-Term-Gap]: US-031, US-032, US-034, US-036, US-037, US-044, US-045,
US-046, US-047. These are filed as tracking gaps — acceptance criteria are written to spec
what "done" looks like, but implementation is blocked until an EL-approved tracking issue
exists and CI capacity is confirmed. QA should not begin writing tests for these until
the tracking issue is filed.

---

## How to Read These Stories

Each story uses the project standard format:

**As** [named persona] in [mode / entry state],
**I need** [specific observable capability],
**so that** [goal — traced to the north-star cognitive task for the active mode].

Acceptance criteria use Given/When/Then format. Each criterion is independently testable
without requiring interpretation of the story context. Test method is noted per criterion:

- `[Playwright]` — automated E2E assertion
- `[Vitest]` — unit or component test
- `[RTL]` — React Testing Library component test
- `[pytest]` — backend / fixture validation
- `[Manual]` — human verification gate

**[Near-Term-Gap]** marks stories for capabilities that are architecturally straightforward
but not yet built. Acceptance criteria specify the done-state. Implementation blocked until
a tracking issue is filed and EL sign-off obtained.

**[Phase-3-TBD]** marks stories for capabilities with no current architectural path. The
story specifies the user need and acceptance criteria but cannot be implemented in M10.
A DIC panel must scope the implementation approach before any work begins. These stories
are the formal input to Issue #577 (Phase 3 technical concept review).

Numbering continues from M9 stories US-001–US-029.

---

## Story Groups

| Group | Capability | Stories | Tag |
|---|---|---|---|
| A | MDA Alert Panel — plain language and layer 3 access | US-030, US-032, US-033 | [Playwright] |
| B | Source attribution at indicator level | US-031, US-034 | [Near-Term-Gap] |
| C | Scenario configuration without specialist mediation | US-032 | [Near-Term-Gap] |
| D | Mode 2 comparison — two scenarios on shared step axis | US-035, US-038, US-040, US-041 | [Playwright] |
| E | Methodology documentation path | US-036 | [Near-Term-Gap] |
| F | Downloadable and exportable output | US-037, US-046 | [Near-Term-Gap] |
| G | Real-time parameter change (Mode 3) | US-039 | [Phase-3-TBD] |
| H | Observed-actuals overlay and community output | US-042, US-043 | [Phase-3-TBD] |
| I | Agricultural income chain and divergence explainability | US-044, US-045, US-047 | [Near-Term-Gap] |
| J | X-ray structural dependency layer | US-048 | [Phase-3-TBD] |

---

## Group A — MDA Alert Panel: Plain Language and Layer 3 Access

### US-030 — MDA alert text is readable without specialist interpretation

**As** Farida Haidari (Persona 6 — Investigative Journalist) in Mode 2 Investigative entry
state, with a 2-hour session cap and no economist available for mediation,
**I need** each MDA alert to include a plain-language sentence that states the finding
in non-technical terms alongside the technical indicator name,
**so that** I can extract a citable, publication-ready finding without an economist
interpreting the instrument cluster for me — the Layer 3 constraint means the tool
either serves me directly or does not serve me at all.

**Acceptance criteria:**
- Given a CRITICAL or WARNING MDA alert in Mode 2, when the alert panel renders, then each
  alert row contains a text element with attribute `data-plain-language="true"` containing a
  complete, grammatical sentence without abbreviation or technical notation
  [Playwright — assert `data-plain-language` element present per alert row]
- Given a plain-language sentence, then it does not contain the strings "composite_score",
  "confidence_tier", "MDA", or any raw database field name
  [Playwright — assert raw field name strings absent from plain-language element]
- Given a plain-language sentence for a food security threshold crossing, then it references
  the human consequence in plain terms (e.g., "food security" rather than "HDI composite");
  the exact phrasing is FA authority subject to UX Designer review
  [Manual — spot-check at QA gate]
- Given a TERMINAL alert in any mode, then the plain-language element is present with the
  same format as CRITICAL and WARNING [Playwright — assert `data-plain-language` present on
  TERMINAL alert rows]

**Journey anchor:** Journey E Step 4
**Layer 3 constraint:** Journalist cannot use tool if this criterion fails — not a deferral
**Tag:** [Playwright]

---

### US-033 — Comparison scenario produces differentiated MDA alert output

**As** Farida Haidari in Mode 2, having run Scenario A (programme-only baseline) and
Scenario B (programme + combined agricultural income shock),
**I need** the alert panel in the Scenario B compare view to show which alerts appeared only
in Scenario B and were absent in Scenario A,
**so that** I can confirm the specific human-cost consequence of the combined shock scenario
vs. the baseline and build the comparison sentence that is the core of my story.

**Acceptance criteria:**
- Given a compare view with Scenario A and Scenario B loaded, when the alert panel renders
  for Scenario B, then alert rows produced by Scenario B that were absent in Scenario A
  carry a visual distinction element (e.g., badge or indicator) signaling they are
  comparison-only alerts [Playwright — assert distinction element present on scenario-B-only
  alert rows; assert element absent on alerts shared by both scenarios]
- Given the comparison distinction element renders, then it does not use color as the sole
  differentiator (CVD compliance: shape or text marker required alongside any color treatment)
  [Playwright — assert comparison badge contains non-color text or shape identifier]
- Given both scenarios have a WARNING for the same indicator at the same step, then that
  alert row does not carry the comparison distinction element [Playwright — assert shared
  alerts have no distinction marker]

**Journey anchor:** Journey E Step 4
**Tag:** [Playwright]

---

## Group B — Source Attribution at Indicator Level

### US-031 — Source registry ID visible at indicator level in alert detail

**As** Farida Haidari in Mode 2, having identified a food security MDA alert,
**I need** the source registry ID and confidence tier to be visible at the individual
indicator level within the alert detail view,
**so that** I can cite the source in my article and assess whether the indicator carries
the evidentiary weight that publication requires — a Tier 3 indicator cited without
disclosure is a journalistic liability.

**Acceptance criteria:**
- Given an MDA alert for a specific indicator, when the alert detail drawer opens, then
  a text element shows the `source_registry_id` value for the indicator that crossed the
  threshold [Playwright — assert source registry ID text present in drawer for the alerting
  indicator]
- Given the source registry ID is visible, then it is accompanied by a human-readable
  source description (not only the registry ID string)
  [Playwright — assert source description text element present alongside registry ID]
- Given the indicator has a confidence tier value, then the tier is displayed as
  "Tier N" (e.g., "Tier 2") adjacent to the source registry ID — not as a raw integer
  [Playwright — assert "Tier N" string format present in alert detail]
- Given the indicator source is synthetic (Tier 4 or 5), then a visual indicator flags
  the synthetic provenance alongside the source attribution
  [Playwright — assert synthetic flag element present when confidence_tier ≥ 4]

**Journey anchor:** Journey E Step 5
**Tag:** [Near-Term-Gap]
**Tracking issue required before implementation begins.**

---

### US-034 — Citable source attribution per alert row (without opening drawer)

**As** Farida Haidari in Mode 2, within a 2-hour session cap,
**I need** a citable source attribution visible in the alert row itself — without requiring
the alert detail drawer to open — that I can copy directly into my notes,
**so that** the time cost of source verification does not consume session budget that I need
for scenario comparison — the drawer path in US-031 is for deep review; this story is for
the working journalist's primary flow.

**Acceptance criteria:**
- Given an MDA alert row in the alert panel at 1280×800, then the row contains an inline
  citation element showing the primary source name (not the full registry ID, not the
  detail drawer) [Playwright — assert inline citation text element present in each alert row
  at 1280×800]
- Given an inline citation, then it contains the source institution name and data vintage
  year (e.g., "IMF WEO 2022") sufficient for journalistic attribution
  [Playwright — assert citation text matches pattern `[Institution] [Year]` or equivalent]
- Given a Tier 4/5 synthetic indicator, then the inline citation reads "Synthetic estimate"
  rather than an institution name [Playwright — assert "Synthetic estimate" text when
  confidence_tier ≥ 4]

**Journey anchor:** Journey E Step 5
**Tag:** [Near-Term-Gap]
**Tracking issue required before implementation begins.**

---

## Group C — Configuration Without Specialist Mediation

### US-032 — Scenario configuration for shock injection without specialist knowledge

**As** Farida Haidari in Mode 2 Investigative entry state,
**I need** to be able to configure an agricultural income displacement shock (30% reduction,
2-step duration) without requiring economist interpretation of configuration field labels,
**so that** I can create Scenario B — the combined-shock case that is the core of my story —
within the session time budget and without a specialist who is not available.

**Acceptance criteria:**
- Given the scenario configuration panel is open, then all field labels use plain-language
  descriptions of what the field controls, not internal instrument type names
  [Playwright — assert no field label contains "EmergencyPolicyInput" or "FiscalPolicyInput"
  verbatim as the display label; assert human-readable labels present for all fields]
- Given a field that sets the magnitude of an income shock, then a tooltip or inline
  description explains what the value represents in natural language terms
  [Playwright — assert tooltip or description element present on numeric shock magnitude
  input fields]
- Given a user without prior WorldSim training sets an agricultural income shock to
  "-0.30" for "2 steps", then the configuration form accepts these values without requiring
  a dropdown of internal instrument identifiers [Playwright — assert form accepts
  plain-numeric input for shock magnitude and step duration fields]

**Journey anchor:** Journey E Step 3
**Layer 3 constraint:** Journalist cannot use tool if this criterion fails
**Tag:** [Near-Term-Gap]
**Tracking issue required before implementation begins.**

---

## Group D — Mode 2 Comparison: Two Scenarios on Shared Step Axis

### US-035 — Two scenarios visible on shared step axis in compare view

**As** James Ochieng (Persona 7 — Parliamentary Economist) in Mode 2 Preparatory entry
state, preparing a committee brief 72 hours before a hearing,
**I need** two scenarios (3.5% fiscal consolidation vs. 2% alternative) to be simultaneously
visible on a shared step axis in the compare view,
**so that** I can identify at which step the two paths diverge, which framework is responsible,
and whether either path crosses an MDA floor — the specificity is what makes findings
citable in Hansard.

**Acceptance criteria:**
- Given two scenarios created and advanced in Mode 2, when the compare view loads, then
  both scenario trajectory sets are rendered on a single shared step axis (shared x-domain)
  [Playwright — assert both scenario curve sets present; assert shared x-axis domain]
- Given the compare view, then each scenario's trajectory curves are visually distinct —
  at minimum by line style (solid vs. dashed) or color treatment, both CVD-compliant
  [Playwright — assert distinct visual treatment per scenario; CVD: non-color differentiator
  present alongside any color treatment]
- Given the compare view at 1024×768, then both scenario curve sets and the shared step axis
  are visible without horizontal scroll [Playwright — assert no horizontal overflow on
  compare view at 1024×768]

**Journey anchor:** Journey F Steps 3–4
**Cognitive task:** Mode 2: threshold-safe path construction (two-scenario comparison)
**Tag:** [Playwright]

---

### US-038 — Confidence tier visible per indicator in compare view

**As** James Ochieng in Mode 2 compare view,
**I need** the confidence tier for each indicator visible in the compare view — either on
the trajectory curve legend or in the divergence summary panel,
**so that** when I draft the committee brief I can note which confidence tier backs each
finding and satisfy the Hansard standard that cited findings are reproducible and
epistemically attributed.

**Acceptance criteria:**
- Given the compare view with two scenarios loaded, then the trajectory curve legend or
  divergence summary contains a "Tier N" text element for each framework shown
  [Playwright — assert "Tier N" string present in compare view for each visible framework]
- Given a Tier 4 or 5 framework in the compare view, then the confidence tier element
  carries the "(exp)" notation consistent with US-012 [Playwright — assert "(exp)" present
  adjacent to Tier 4/5 curve legend entry in compare view]
- Given a Tier 1–3 framework, then no "(exp)" notation appears on that framework's curve
  legend entry [Playwright — assert "(exp)" absent from Tier 1–3 entries]

**Journey anchor:** Journey F Step 4
**Cognitive task:** Mode 2: threshold-safe path construction
**Tag:** [Playwright]

---

### US-040 — Committed programme baseline reproduced in Mode 2

**As** Abena Osei (Persona 8 — Civil Society Monitor) in Mode 2 Retrospective
(accountability sub-mode), running a 30-day accountability monitoring cycle,
**I need** Mode 2 to reproduce a committed programme baseline from its input parameters
(social protection spending 1.2% of GDP, 4 annual steps),
**so that** I have an authoritative, transparent, reproducible reference trajectory against
which to compare observed government spending — the baseline that has no other
independently transparent analytical source.

**Acceptance criteria:**
- Given a Mode 2 scenario configured with social protection spending at 1.2% of GDP for
  4 annual steps, when the scenario is advanced to step 4, then the trajectory view shows
  a trajectory consistent with the configured spending level across all 4 steps
  [Playwright — assert trajectory data point at each step is present and non-null for the
  configured social protection spending scenario]
- Given the scenario is fully advanced, then the trajectory state is
  `SCENARIO_RUNNING` or `COMPLETE` with no error state [Playwright — assert
  scenario state element does not contain error indicator after 4-step advance]
- Given a new Mode 2 session using the same input parameters, then the trajectory output
  is identical (deterministic within the same model version) — reproducibility is the
  Hansard-equivalent requirement for civil society accountability work
  [pytest — fixture test: two scenario runs with identical inputs produce identical
  trajectory outputs]

**Journey anchor:** Journey G Step 2
**Cognitive task:** Mode 2: committed baseline reproduction for accountability monitoring
**Tag:** [Playwright]

---

### US-041 — Compare view: committed vs. observed spending divergence

**As** Abena Osei in Mode 2, having created Scenario A (committed 1.2% GDP social
protection) and Scenario B (observed 0.9% GDP — below-committed),
**I need** the compare view to show which framework thresholds are crossed in Scenario B
but not in Scenario A,
**so that** I can document the consequence of the commitment gap — specifically that child
nutrition crosses a WARNING threshold under observed spending where it does not under
committed spending — and make that finding legible to SEND Ghana's policy team.

**Acceptance criteria:**
- Given compare view with Scenario A (committed) and Scenario B (observed below-committed),
  when the MDA alert panel renders in compare view, then alerts present in Scenario B but
  absent in Scenario A are visually marked as comparison-only (consistent with US-033
  comparison distinction treatment) [Playwright — assert comparison distinction element on
  Scenario-B-only alert rows in compare view]
- Given the child nutrition indicator crosses WARNING at step 2 in Scenario B but not
  Scenario A, then the compare view alert panel shows a WARNING for child nutrition at
  step 2 with the comparison distinction marker [Playwright — assert WARNING alert with
  comparison marker present for the threshold-crossing indicator at step 2]
- Given the compare view, then Scenario A and Scenario B labels are visible and human-
  readable (not internal scenario IDs) in the compare panel header
  [Playwright — assert scenario name text elements visible in compare panel header]

**Journey anchor:** Journey G Step 4
**Cognitive task:** Mode 2: committed vs. observed comparison for accountability
**Tag:** [Playwright]

---

## Group E — Methodology Documentation Path

### US-036 — Methodology documentation accessible by ADR reference from instrument cluster

**As** James Ochieng in Mode 2, 72 hours before a committee hearing,
**I need** to access the methodology documentation for any displayed indicator — including
the ADR reference number for the computation approach — without leaving the instrument
cluster,
**so that** I can cite the methodology in the committee brief under the standard that
committee findings must be reproducible within the hearing day — "run the scenario with
these inputs, consult ADR-NNN for the computation model" is the Hansard citation.

**Acceptance criteria:**
- Given any indicator visible in the instrument cluster, then an accessible documentation
  link or info trigger is present that opens the methodology documentation for that
  indicator [Playwright — assert documentation trigger element present per indicator in
  instrument cluster]
- Given the methodology documentation opens, then it includes the ADR reference number
  for the computation approach used for that indicator
  [Playwright — assert "ADR-" prefixed text present in methodology documentation view]
- Given the methodology documentation is open, then it can be accessed without closing
  or navigating away from the instrument cluster primary viewport — the documentation
  opens in a side panel or drawer, not a separate page
  [Playwright — assert instrument cluster Zone 1 elements remain in DOM while
  documentation panel is open]
- Given the methodology documentation for an indicator with synthetic data, then the
  documentation notes which of the five synthesis methods (ADR-007) was used
  [Playwright — assert synthetic method description present in methodology docs when
  indicator is synthetic]

**Journey anchor:** Journey F Step 5
**Critical constraint:** Hansard citation standard — missing ADR reference is a blocker
**Tag:** [Near-Term-Gap]
**Tracking issue required before implementation begins.**

---

## Group F — Downloadable and Exportable Output

### US-037 — Downloadable tabular output for committee brief

**As** James Ochieng in Mode 2, having completed a two-scenario comparison,
**I need** to download the trajectory data and alert summary as a tabular file (CSV or
structured PDF),
**so that** I can construct the four-page committee brief from authoritative trajectory
data — the downstream document that justifies alternative policy parameters before a
parliamentary committee.

**Acceptance criteria:**
- Given a Mode 2 scenario in SCENARIO_RUNNING or COMPLETE state, then a download control
  is visible without scroll in the instrument cluster or adjacent action bar
  [Playwright — assert download control element present without scroll]
- Given the user activates the download control, then a file is downloaded within 10 seconds
  [Playwright — assert file download event fires within 10 seconds of control activation]
- Given the downloaded file, then it contains the trajectory data for each step × framework
  in tabular format with column headers (step, framework, composite_score, confidence_tier)
  [pytest — assert CSV/JSON schema validates against required columns]
- Given a compare view with two scenarios, then the download contains both scenarios' data
  in clearly labeled columns or sections [pytest — assert both scenario labels present in
  download output]

**Journey anchor:** Journey F Step 6
**Tag:** [Near-Term-Gap]
**Tracking issue required before implementation begins.**

---

### US-046 — Trajectory data export for journal data appendix

**As** Dr. Priya Krishnaswamy (Persona 4V — Personal-Connection Researcher) in Mode 1
Retrospective entry state, following a backtesting session that produced a 5pp divergence
finding,
**I need** to export the simulated trajectory data — including the confidence tier and
comparison group metadata — in a format suitable for a journal data appendix,
**so that** the divergence finding is reproducible by peer reviewers, which is the
standard that makes it citable in an academic publication.

**Acceptance criteria:**
- Given a completed Mode 1 backtesting scenario, then an export control is accessible in
  the instrument cluster without opening a separate page
  [Playwright — assert export control element present in Mode 1 completed scenario]
- Given the user activates the export control, then the download includes simulation
  parameters (input values, entity, n_steps, timestep_label), trajectory data per step,
  confidence tier per framework, and the comparison group label (e.g., "Maharashtra state
  average" rather than an internal entity ID) [pytest — assert exported file schema
  contains all required metadata fields]
- Given the exported file, then it is in a format readable by standard data analysis
  tools (CSV or JSON with documented schema) [pytest — assert file passes schema
  validation for CSV or JSON structure]

**Journey anchor:** Journey H Step 6
**Tag:** [Near-Term-Gap]
**Tracking issue required before implementation begins.**

---

## Group G — Real-Time Parameter Change (Mode 3)

### US-039 — Real-time parameter change without new scenario creation

**As** James Ochieng in Mode 3 Active Control, running a committee hearing simulation,
**I need** to change a fiscal consolidation parameter (e.g., from 3.5% to 2.0%) and see
the trajectory update in real time without creating a new scenario,
**so that** I can answer a committee member's "what if the consolidation were less severe?"
question within the hearing session — a new scenario creation flow breaks the
parliamentary tempo.

**Note:** Mode 3 real-time parameter change is not a current platform capability. The
Mode 3 control plane is architecturally reserved (US-027, US-028) but not yet populated
with fiscal consolidation controls. This story is [Phase-3-TBD] pending DIC panel scope
assessment (Issue #577). The acceptance criteria below specify the done-state for when
this capability is implemented.

**Acceptance criteria (done-state specification):**
- Given Mode 3 is active with a committed baseline scenario loaded, then a parameter
  input field is visible in the control plane zone for at least one fiscal consolidation
  instrument [Playwright — assert parameter input element present in control plane zone
  in Mode 3]
- Given the user changes the fiscal consolidation value and activates it, then the
  trajectory view updates within 10 seconds to reflect the new value — consistent with
  US-018 Mode 3 computation latency requirement [Playwright — assert trajectory update
  within 10 seconds of parameter change activation]
- Given the updated trajectory, then the baseline ghost curves remain visible (consistent
  with US-007) and the divergence fill updates to reflect the new parameter's consequence
  [Playwright — assert ghost curves still present after parameter change; assert divergence
  fill element updates]

**Journey anchor:** Journey F (Mode 3 extension, not yet in current journey map)
**Tag:** [Phase-3-TBD]
**Phase 3 scope assessment required (Issue #577) before implementation begins.**

---

## Group H — Observed-Actuals Overlay and Community Output Layer

### US-042 — Observed-actuals input overlay on committed baseline trajectory

**As** Abena Osei in Mode (TBD — see note), having run the committed programme baseline
trajectory in Mode 2,
**I need** to input observed actual spending values for each programme year and have them
overlaid on the committed baseline trajectory in the instrument cluster,
**so that** I can produce a documented record of the commitment gap with the authoritative
baseline and observed actuals on the same chart — the accountability claim requires both
elements visible together.

**Note:** Observed-actuals input is not a current platform capability. Mode 1 reconstructs
known history; Mode 2 projects from configured inputs. Neither mode has a data ingestion
path for observed actuals measured after scenario creation. The Customer Agent finding
(recorded in personas.md Persona 8) confirms this gap. This story is [Phase-3-TBD] pending
DIC panel scope assessment of implementation approach: Mode 1 extension, Mode 4, or
post-processing overlay layer. See Issue #577.

**Acceptance criteria (done-state specification):**
- Given a completed Mode 2 scenario representing the committed programme baseline, then
  an "Add observed actuals" input path is accessible from the scenario view
  [Playwright — assert observed actuals entry point present on completed scenario]
- Given the user inputs observed spending values for steps 1–4, then those values are
  overlaid on the committed baseline trajectory as distinct data points (visually
  differentiated from the simulation curve) [Playwright — assert observed actuals data
  point elements present in trajectory view; assert distinct visual treatment from
  simulation curve elements]
- Given both committed baseline and observed actuals are in the view, then the MDA alert
  panel shows which thresholds the observed-actuals trajectory crosses that the committed
  baseline does not [Playwright — assert comparison alert panel reflects actuals vs. baseline
  divergence]

**Journey anchor:** Journey G Step 6
**Tag:** [Phase-3-TBD]
**Phase 3 scope assessment required (Issue #577) before implementation begins.**

---

### US-043 — Community-audience output layer for civil society publication

**As** Abena Osei, preparing a civil society accountability report readable by community
members and programme beneficiaries — not specialist economists,
**I need** a community-audience rendering of the trajectory comparison that uses plain
language, replaces technical confidence tier notation with plain-language epistemic
disclosure, and is formatted for the publication formats SEND Ghana uses
(A4 two-column, screen-readable PDF),
**so that** the accountability finding — "the government spent less than it committed on
social protection, and child nutrition crossed a warning threshold as a result" — reaches
the communities that are the intended beneficiaries of the programme and the primary
audience for accountability.

**Note:** Community-audience output is not a current platform capability. The platform
renders one output format per view. A separate plain-language rendering with different
vocabulary, confidence disclosure conventions, and export formats is a new output layer
with no current architectural path. This story is [Phase-3-TBD] pending DIC panel scope
assessment. See Issue #577.

**Acceptance criteria (done-state specification):**
- Given a completed scenario comparison in Mode 2, then a "Community report" export path
  is accessible from the compare view [Playwright — assert community export control present
  in compare view]
- Given the community report export is activated, then the output document contains no
  technical notation as primary content: no "composite_score", no "confidence_tier N",
  no "MDA", no "Tier N" strings appear as lead findings or section headers
  [pytest — assert technical notation strings absent from primary-content elements of
  community report output; see epistemic disclosure criterion below]
- Given any indicator in the community report has confidence_tier ≥ 3, then the report
  contains a plain-language epistemic disclosure for that indicator, consistent with the
  vocabulary mapping standard: Tier 3 → "Based on a model estimate from comparable
  countries"; Tier 4 → "This is an estimated figure — independent verification
  recommended"; Tier 5 → "Insufficient data — the model could not compute this reliably";
  this disclosure replaces, and does not omit, the confidence tier notation
  [pytest — assert disclosure string present adjacent to each Tier 3+ indicator finding
  in community report output; assert no Tier 3+ indicator appears without disclosure]
- Given the community report, then the primary finding is stated as a plain-language
  sentence explaining the consequence for people — not for indicators
  [Manual — spot-check that no indicator-centric language appears as the lead finding]
- Given the community report is exported, then the file format is A4 PDF or equivalent
  screen-readable document format [pytest — assert file MIME type is PDF or declared
  community-readable format]

**Journey anchor:** Journey G Step 7
**Tag:** [Phase-3-TBD]
**Phase 3 scope assessment required (Issue #577) before implementation begins.**
**Correction applied 2026-06-02 (PI-REVIEW-002 F-005):** North-star sentence updated from
"removes confidence tier notation" to "replaces technical confidence tier notation with
plain-language epistemic disclosure." Technical-notation criterion scoped to primary content
only. Epistemic disclosure criterion added (Tier 3/4/5 vocabulary mapping standard). The
No False Precision principle is absolute — stripping uncertainty disclosure entirely from
any WorldSim output is not acceptable regardless of audience. Chief Methodologist is
Required Consultant (C) on the vocabulary mapping standard before implementation begins.

---

## Group I — Agricultural Income Chain and Divergence Explainability

### US-044 — Methodology documentation for agricultural income transmission chain

**As** Dr. Priya Krishnaswamy in Mode 1 Evaluative entry state, verifying that the
simulation's agricultural income transmission model is coherent before trusting it with
her field data comparison,
**I need** to read the methodology documentation for the agricultural income transmission
chain — the multi-hop path from MSP price floor change → farm gate price → farm income
→ debt service → food expenditure → child malnutrition — and find the ADR reference,
**so that** I can assess whether the comparison group and measurement assumptions match
the Wardha district context closely enough to make the divergence meaningful.

**Acceptance criteria:**
- Given Mode 1 with an agricultural income indicator visible in the instrument cluster,
  then a methodology documentation trigger is accessible for that indicator (consistent
  with US-036) [Playwright — assert documentation trigger present for agricultural income
  indicator]
- Given the methodology documentation opens, then it describes the transmission chain
  with at least the following hops documented: price floor → farm gate price → farm income
  → food expenditure; a complete N-hop chain description is preferred but 4-hop minimum
  is the acceptance criterion [Playwright — assert multi-hop chain description present
  in methodology docs]
- Given the methodology documentation, then it specifies the comparison group used for
  the simulation (e.g., state-level average, district-level, regional) so the user can
  assess comparison group validity [Playwright — assert comparison group text present
  in methodology docs]

**Journey anchor:** Journey H Step 1
**Tag:** [Near-Term-Gap]
**Tracking issue required before implementation begins.**

---

### US-045 — Agricultural income trajectory visible with confidence tier

**As** Dr. Priya Krishnaswamy in Mode 1 Retrospective entry state, having configured
an India backtesting scenario with MSP price floor removal at step 1,
**I need** the trajectory view to show an agricultural income trajectory curve with
confidence tier visible, consistent with the four-framework visualization in US-003 and
US-012,
**so that** I can read the simulated agricultural income decline across the 4-step window
and compare it against my field data — the comparison requires both the trajectory and
the confidence tier, because a Tier 3 estimate compared against survey data requires an
explicit caveat.

**Acceptance criteria:**
- Given a Mode 1 scenario with agricultural income in the active indicator set, when the
  trajectory view renders, then an agricultural income trajectory curve is visible on the
  shared step axis [Playwright — assert agricultural income curve element present in
  trajectory view]
- Given the agricultural income curve renders, then the confidence tier is visible —
  either as a "(exp)" badge per US-012 for Tier 4/5, or as the tier visible in the
  curve legend for all tiers [Playwright — assert confidence tier element present in
  curve legend or adjacent to curve]
- Given the scenario fixture for India agricultural income is loaded, then the trajectory
  data point at step 2 shows a negative value consistent with farm income decline following
  MSP removal [pytest — fixture validation: step 2 agricultural income value is negative
  relative to step 0 baseline when MSP removal input is applied at step 1]

**Journey anchor:** Journey H Step 3
**Tag:** [Near-Term-Gap]
**Tracking issue required before implementation begins.**

---

### US-047 — Divergence explainability: assumption visible at indicator level

**As** Dr. Priya Krishnaswamy in Mode 1, having observed a 5pp divergence between the
simulated 18% agricultural income decline and her field-recorded 23% decline,
**I need** the instrument cluster or detail drawer to show the specific assumption that
produces the divergence — specifically, that the comparison group is Maharashtra state
average, not Wardha district — without me having to interpret the simulation model myself,
**so that** I can qualify the divergence in my journal article with the specific assumption
responsible (not "the model is imprecise" but "the comparison group is Maharashtra state
average vs. Wardha district field data").

**Acceptance criteria:**
- Given a divergence between simulation output and an externally noted field value, then
  the indicator detail drawer includes an "Assumptions" section that lists the primary
  comparison group and geographic scope used for the indicator computation
  [Playwright — assert "Assumptions" section present in indicator detail drawer;
  assert comparison group text present within that section]
- Given the comparison group assumption is Maharashtra state average, then the assumption
  text reads "Maharashtra state average" or equivalent — not an internal entity ID
  [Playwright — assert human-readable comparison group label in Assumptions section]
- Given the Assumptions section is present, then it is accessible from the trajectory
  view without closing the trajectory or navigating away from the instrument cluster
  [Playwright — assert drawer opens without Zone 1 instruments leaving DOM]

**Journey anchor:** Journey H Step 5
**Tag:** [Near-Term-Gap]
**Tracking issue required before implementation begins.**

---

## Group J — X-Ray Structural Dependency Layer

### US-048 — X-ray layer: structural dependency visualization for causal chain

**As** Dr. Priya Krishnaswamy in Mode 1, having accepted that the divergence is within
plausible range given the comparison group, now wanting to understand the causal structure
that produced the simulated trajectory,
**I need** a structural dependency visualization (X-ray layer) that shows the multi-hop
causal path from the MSP price floor removal input through to the child malnutrition
outcome — visible as a navigable graph in Zone 2,
**so that** I can assess whether the causal model reflects the agricultural income
transmission mechanisms I observed in Wardha district and qualify the structural
assumptions in my journal methodology section.

**Note:** The X-ray structural dependency visualization is not a current platform
capability. It requires a new rendering mode for the causal graph data structure,
a Zone 2 panel allocation, and backend support for traversing the event-propagation
dependency graph per indicator at each step. There is no current architectural path for
this feature. It is [Phase-3-TBD] pending DIC panel scope assessment of M11 vs. M12
placement and implementation approach. The X-ray layer lives in Zone 2 (navigable
context), not Zone 1 (instrument cluster) — consistent with CLAUDE.md Governing Premise 2
(instruments always visible; context navigable). No Premise 1 or Premise 2 conflict.
See Issue #577 for DIC panel scope assessment.

**Acceptance criteria (done-state specification):**
- Given Mode 1 with an agricultural income indicator active, then an "X-ray" or equivalent
  structural dependency trigger is visible in Zone 2 navigation
  [Playwright — assert X-ray trigger element present in Zone 2]
- Given the X-ray trigger is activated, then Zone 1 instruments remain visible (Zone 2
  panel opens alongside Zone 1, not replacing it)
  [Playwright — assert all four Zone 1 instruments present in DOM while X-ray panel is open]
- Given the X-ray panel renders for the agricultural income indicator, then it shows a
  directed graph from the price floor input node through at least: farm gate price →
  farm income → food expenditure → child malnutrition (4-hop minimum)
  [Playwright — assert at minimum 4 node elements connected in directed sequence in
  the X-ray graph rendering]
- Given a node in the X-ray graph is selected, then the trajectory view highlights the
  corresponding indicator curve — shared step axis integration maintained
  [Playwright — assert curve highlight behavior on X-ray node selection]

**Journey anchor:** Journey H Step 7
**Tag:** [Phase-3-TBD]
**Phase 3 scope assessment required (Issue #577) before implementation begins.**

---

## Story Coverage Matrix

| Journey | Step coverage | Personas served | Stories |
|---|---|---|---|
| E — Story Investigation (Farida) | Steps 3–5 | P6 | US-030, US-032, US-033, US-034 |
| F — Legislative Brief (James) | Steps 3–6 | P7 | US-035, US-036, US-037, US-038, US-039 |
| G — Accountability Monitoring (Abena) | Steps 2–7 | P8 | US-040, US-041, US-042, US-043 |
| H — Backtesting with Personal Observation (Priya) | Steps 1–7 | P4V | US-044, US-045, US-046, US-047, US-048 |

| Tag | Count | Stories |
|---|---|---|
| [Playwright] — current capability | 6 | US-030, US-033, US-035, US-038, US-040, US-041 |
| [Near-Term-Gap] — blocked pending tracking issue | 9 | US-031, US-032, US-034, US-036, US-037, US-044, US-045, US-046, US-047 |
| [Phase-3-TBD] — blocked pending Issue #577 DIC panel | 4 | US-039, US-042, US-043, US-048 |

**Total stories: 19 (US-030 through US-048)**
**M10 [Playwright] gate: 6 stories — QA may begin writing acceptance tests immediately**
**[Near-Term-Gap] gate: BLOCKED** — tracking issues required per Decision 4
**[Phase-3-TBD] gate: BLOCKED** — Issue #577 DIC panel required
**Formal input to Issue #577:** US-039, US-042, US-043, US-048
