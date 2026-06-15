# WorldSim UX Input Confidence Audit — Minister-in-the-Chair Exercise, Part II
## M14 Evidence Record for ADR-015 Amendment / ADR-016

> **Date:** 2026-06-15  
> **Session type:** Live application audit — UI at localhost:5173, backend at localhost:8000  
> **Software version audited:** `v0.13.0-2-g097d3dc` (2 commits post M13 release tag v0.13.0; M14 active; commit 097d3dc — Merge PR #959 docs/adr-015-model-legibility)  
> **Conducted by:** Architect Agent, using Playwright screenshots and live DOM text extraction of the running application  
> **Companion document:** `docs/demo/m14/reviews/2026-06-15-ux-legibility-audit-minister-exercise.md` (Part I — output legibility family)  
> **Surfaces audited:** Scenario creation form, Fidelity panel (full scrolled content), choropleth attribute selector, entity label interaction attempt, API call log on scenario load, visible text extraction at each surface  
> **Purpose:** Part I of the audit addressed the output legibility gap family (ML-1 through ML-7). This document addresses the input confidence gap family — the dimension of the original ask that Part I did not fully develop: "what went into producing what I am seeing?" Nothing in this document is summarized.

---

## Part I — What the Original Ask Required

The original exercise instruction included three questions the minister should ask herself:

> *"Ask yourself: what went into producing what I am seeing, why does the model show what it shows, and how confident should I be in it?"*

The instruction also specified: *"identify the full family of user experience gaps this exercise reveals — not just the input layer, but every dimension of model legibility."*

The phrase "not just the input layer" signals that the input layer was the expected starting gap — the obvious one — and the exercise asked for the full family beyond it. Part I found and documented the output legibility family (ML-1 through ML-7) and the Evidence Thread Architecture as the framework for that family. The input layer was present in Part I only as ML-3 (Assumption Invisibility) — a minimal treatment of one corner of what is, on live examination, a distinct gap family with its own members and its own required architectural response.

This document completes the exercise by observing the input-facing surfaces of the live UI with the same empirical discipline applied in Part I: look at what is on screen; document what the minister can and cannot answer from it alone.

---

## Part II — Live UI Observations: Input-Facing Surfaces

### 2.1 — The Scenario Creation Form

**Method:** Clicked "Scenarios ▼" from the landing state. Extracted all form fields via Playwright DOM inspection.

**What is on screen:**

A panel opens on the left showing the scenario list (scrollable). To the right is a "NEW SCENARIO" section containing:

- A text input labeled **"Scenario name"** (placeholder: "Scenario name", currently blank)
- A number input (no visible label) with **value: 2020**, min: 1900, max: 2100
- A **range slider** with value: 1, min: 0.1, max: 3 (no visible label on the slider itself)
- A **"Create"** button

Below the range slider, visible hint text: *"Creates a GRC scenario with 3 annual steps starting at the given year. Fiscal multiplier 1.0 = standard; >1.0 = expansionary amplification; <1.0 = contractionary."*

The scenario list shows names including: "SriLanka-2022-BPO-Validate," "G8b-REG-multiplier-1781374921053," "G8b-REG-noop-1781374919943," "G8b-AC2-1781374833182" — internal test harness identifiers. Status badges show "completed," "running," "pending." The "Fiscal multiplier:" label and the value "1.0" appear in the scenario list for some rows (visible for the first selected scenario: `G8b-REG-multiplier-1781374921053 / running / Fiscal multiplier: 1.0`).

**What a first-time user faces at scenario creation:**

The entity to be modeled is hardcoded to GRC (Greece) — this is visible only in the hint text ("Creates a **GRC** scenario"). There is no entity selection in the form. The minister cannot choose what country she is modeling from the creation form.

The number field (year) accepts 1900–2100 with no indication of what years have underlying data, at what quality, or from what source. A minister entering "2024" receives no signal about whether 2024 data exists for GRC, whether it is observed or synthetic, or what its confidence tier will be.

The fiscal multiplier slider is the only model parameter visible at creation time. No political economy parameters, no conditionality settings, no data source selection, no n_steps override, no external shock injection. These either do not exist in the current UI or are inaccessible from the creation form.

After clicking "Create": the form submits and the scenario appears in the list. No confirmation screen showing what data will be loaded. No pre-creation data quality preview. The minister has committed to a scenario without seeing what data the model will use.

**Three-field input → eight-step trajectory producing TERMINAL alerts.** The creation form is the only point at which the minister influences what goes into the model. She has three fields: a name, a year, and a multiplier. The trajectory that results — including TERMINAL alert classifications that will be cited at a negotiating table — flows from inputs the minister never had a chance to verify.

### 2.2 — The Fidelity Panel

**Method:** Clicked "Fidelity ▼" from the landing state (no scenario loaded). Playwright extracted all visible text content at three scroll positions (top, mid, bottom). Full text preserved verbatim below.

**What is on screen — Fidelity panel, from top:**

Header row: `DIRECTION_ONLY: 5/5 cases ✓ | MAGNITUDE: /2 cases for ADR-006 upgrade`

Section heading: **Backtesting Validation — Five historical crises — sign checks**

Descriptive text: *"The model is tested on whether it gets the sign right. Consistent directional accuracy across five distinct crisis mechanisms is evidence of real causal dynamics — not a coincidence. Magnitude calibration is the next validation layer. We are not claiming it before we have evidence."*

Five cases presented in cards:

**GRC — Greece — DIR ✓ — 2010 — All gates PASS**  
Period: 2010–2012 / Fiscal consolidation / external conditionality  
Step data: DIR ✓ 2010 / DIR ✓ 2011 / DIR ✓ 2012  
Explanatory text: *"Three consecutive years of GDP contraction correctly predicted. MAGNITUDE deferred to M11 — accumulation-only model lacks mean-reversion channel (Issue #221)."*

**ARG — Argentina — DIR ✓ — 2001 — All gates PASS**  
Period: 2001–2002 / Sovereign default / convertibility peg collapse  
Step data: DIR ✓ 2002 / MAGNITUDE ✓ 2002  
Explanatory text: *"Step 2 is the first MAGNITUDE-validated result in WorldSim. Mechanism: depressed-regime multiplier (1.5×) applied to Zero Deficit Plan spending cut (−6.5% of GDP). Step 1 MAGNITUDE deferred to M11 — one-step lag structural gap (Issue #222)."*  
Sub-display: **FIRST MAGNITUDE-VALIDATED RESULT** — Model **−10.55%** vs actual **−10.9%** — deviation **3.2%** / Tolerance ±20% → [−13.08%, −8.72%]

**LBN — Lebanon — DIR ✓ — 2019 — All gates PASS**  
Period: 2019–2020 / Banking collapse / compound crisis  
Explanatory text: *"Cascade case — banking collapse, currency crisis, sovereign default, and Beirut port explosion. Full cascade propagation dynamics deferred to Issue #29."*

**THA — Thailand — DIR ✓ — 1997 — All gates PASS**  
Period: 1997–1998 / External contagion / balance-sheet deterioration  
Explanatory text: *"Externally-triggered currency speculative attack producing domestic balance-sheet deterioration — distinct crisis mechanism from all other cases."*

**ECU — Ecuador — DIR ✓ — 1999 — All gates PASS**  
Period: 1999–2000 / Banking collapse / dollarization  
Explanatory text: *"First case with a recovery at step 2 (+2.8% historical outturn). Fidelity gate: 'not deeper than step 1' (not 'predict contraction'). Model passes — reports equal GDP (−6.3%), satisfying the ≥ threshold. Documented blind spot: dollarization stabilization and oil recovery channels not yet modeled."*

**Fidelity panel, scrolled to bottom:**

Section: **Documented Structural Gaps — Deferred to M7**

**ARG step 1 (2001) MAGNITUDE — Issue #222 — M11**  
*"One-step lag: Zero Deficit Plan fires at step 1 but MacroeconomicModule processes prior-step events only. Step 1 reports the initial seed (−0.8%) while the historical outturn (−4.4%) reflects the contemporaneous shock. Model deviation: 82%. Not fixable by parameter calibration."*  
Sub-display: −0.8% model vs −4.4% actual (82% deviation)

**GRC steps 2–3 (2011–2012) MAGNITUDE — Issue #221 — M11**  
*"GDP is a pure accumulation stock — it only moves when a fiscal event fires and never receives an endogenous recovery impulse. The Greek economy improved from −8.9% to −6.6% without a positive fiscal shock in the fixture. Requires a mean-reversion channel in MacroeconomicModule (Chief Methodologist + Chief Engineer joint ADR)."*  
Sub-display: GRC step 2: −21.4% model vs −8.9% actual (140%); step 3: −31.4% vs −6.6% (376%)

Footer: *"1 of 2 required MAGNITUDE cases achieved. Argentina 2002 (step 2) is the first. One additional MAGNITUDE case (deferred to M11) unlocks the full DISTRIBUTION_COMBINED threshold infrastructure and uncertainty band calibration."*

**What the Fidelity panel reveals and does not reveal:**

The Fidelity panel IS a genuine model calibration disclosure. It shows backtesting results with explicit deviation percentages, documents structural gaps by name (one-step lag, mean-reversion channel absence), and names the deferred issue numbers. This is more methodological transparency than most analytical tools provide.

What the Fidelity panel does NOT answer: the minister's input-side question. It validates the model relationship (does the model get the sign right for historical cases?). It does not tell the minister what data was used to seed her specific scenario, whether that data is current, what its source is, or whether the scenario's starting conditions correspond to reality. A minister loading a Jordan 2024 scenario can read that Argentina 2001 passed the direction check — but this gives her no information about the quality or accuracy of the Jordan data her model is using.

Additionally: the Fidelity panel is not scenario-contextual. It is the same content regardless of which scenario is loaded. It does not show the data quality profile for the active scenario's entities. It is global to the model, not specific to the minister's analytical situation.

The Fidelity panel content requires methodological literacy to interpret. "DIRECTION_ONLY: 5/5 cases ✓, MAGNITUDE: /2 cases for ADR-006 upgrade" requires the reader to understand what direction-only vs. magnitude validation means in a backtesting context. "Tolerance ±20% → [−13.08%, −8.72%]" requires understanding of tolerance intervals. There is no entry-level plain-language summary: "What this means for using this tool: direction of effects is validated. Size of effects is partially validated in one case. Here is what to do with that uncertainty."

### 2.3 — The Choropleth Attribute Selector

**Method:** Inspected the dropdown options in the choropleth attribute selector (the element showing "Gdp Usd Millions (USD_millions_cur▼)" in the header).

**What is on screen when opened:**

Six options:
- "Economy Tier (dimensionless, dimensionless)"
- "Gdp Usd Millions (USD_millions_current, flow)"
- "Income Group (dimensionless, dimensionless)"
- "Map Color Group (dimensionless, dimensionless)"
- "Pop Rank (dimensionless, dimensionless)"
- "Population Total (persons, stock)"

**What this reveals:**

The choropleth displays static reference world attributes — entity classification data (economy tier, income group, population) — not the active scenario's computed values. The choropleth occupies approximately 55% of the total viewport when a scenario is loaded (the large map below the instrument cluster). A first-time user observing the map alongside the instrument cluster may reasonably assume the map is showing the scenario's computed outputs for the scenario entities — it is not. It is showing reference classification data that does not change as the scenario advances through steps.

The relationship between the choropleth and the active scenario is nowhere stated on screen. Is the choropleth background context? Is it a data input visualization? Is it showing the output for a different attribute? The minister cannot answer this from the screen.

The option labels use technical format strings: "USD_millions_current, flow" — unit and stock/flow type encoded in the label, in a format more suited to a data engineer than a finance minister.

### 2.4 — Entity Drawer Accessibility

**Method:** Attempted to click `[data-testid="entity-label-0"]` (the "JOR" label in the instrument cluster header). The click was blocked by a Recharts SVG element that intercepts pointer events. Force-clicking the entity-labels-overlay and the ScenarioIdentityHeader produced no drawer.

**What this reveals:**

The entity detail drawer — Zone 2, one interaction from Zone 1, which is the primary path to any per-indicator data — is not reachable by clicking the entity labels that appear in the instrument cluster. The SVG trajectory chart intercepts pointer events in the region where entity labels are rendered. There is no visible alternative path to the entity drawer from Zone 1.

The `data-testid="entity-labels-overlay"` element renders "JOREGY" as a combined string — two entity labels concatenated with no separator, suggesting the overlay label rendering may have a layout issue.

Whether the entity drawer contains initial state data, indicator-level data provenance, or input values is not determinable from this audit because the drawer is not accessible from the Zone 1 surface.

### 2.5 — Internal Field Names in the UI

**Method:** Visible text extraction from the full page with Hormuz scenario loaded.

**What is on screen:**

The visible text at the trajectory chart area includes:
- `ecological_active`
- `financial_active`
- `governance_active`
- `human_development_active`

These appear at y-positions 231, 257, 283, 309 — within the trajectory chart's visible area, likely as recharts legend or tooltip text. They are raw internal field names using database/API naming conventions.

The choropleth attribute selector default label is "Gdp Usd Millions (USD_millions_cur▼)" — also a raw field name with unit encoding.

**What this reveals:**

The raw field names (with `_active` suffix, underscore separators, abbreviated unit suffixes) appear in the UI as user-facing text. A minister who understands "Financial" as a framework composite does not know what "financial_active" means. Does "_active" distinguish from a baseline version? Is there a "financial_inactive" state? The suffix carries semantic meaning the user is not told.

### 2.6 — API Calls on Scenario Load (Network Observation)

**Method:** Monitored network requests during scenario load and replay.

**API calls observed:**
- `/api/v1/attributes/available`
- `/api/v1/scenarios/{id}` (scenario metadata)
- `/api/v1/scenarios/{id}/trajectory` (trajectory data — outputs, not inputs)
- `/api/v1/choropleth/gdp_usd_millions` (static world reference data)
- `/api/v1/choropleth/gdp_usd_millions?scenario_id={id}&step=8` (scenario-step choropleth)
- `/api/v1/scenarios/{id}/measurement-output?entity_id=JOR&step=8` (measurement output for step 8)

**What this reveals:**

No API call fetches data provenance, input source attribution, initial state indicator values, or data vintage for the active scenario. The calls fetch: scenario metadata, computed trajectory outputs, measurement outputs, and static reference data. The input data used to seed the scenario (the actual indicator values at step 0, their sources, their vintages) is not fetched by any API call during the primary UI load sequence. Whether this data exists in the API at other endpoints is not determinable from this audit — but it is not surfaced to the UI during normal scenario viewing.

---

## Part III — What the Finance Minister Can and Cannot Answer About Inputs

| Question | Answerable from screen? | From what? |
|---|---|---|
| What data is the model using for Jordan's current account deficit? | **No** | Not visible at any zoom level in the primary viewport |
| Where did that data come from (source institution)? | **No** | Not visible anywhere in Zone 1 or Zone 2 (Zone 2 unreachable from Zone 1 in this test) |
| How old is the data underlying my scenario? | **No** | No vintage information visible at scenario level |
| Was the data observed or synthesized? | **No** | Confidence tier labels (T4, "Moderate confidence") appear on outputs; they do not appear on the input data itself before the scenario runs |
| What were Jordan's starting indicator values at step 0? | **No** | The trajectory chart begins at Step 0 but shows the composite score, not the component indicator values that fed it |
| What entity am I modeling in this scenario? | **Partially** | GRC is named in the creation form hint text; JOR/EGY appear in the identity strip after scenario creation, but the creation form itself does not show entity selection |
| What data would I get if I entered year 2017 instead of 2024? | **No** | No data availability preview before scenario creation |
| Has the model been validated for a situation like mine? | **Partially** | Fidelity panel shows validation for 5 historical cases; it does not indicate which case (if any) is most analogous to the minister's scenario |
| What does "5/5 DIR ✓" mean for my Jordan 2024 scenario? | **No** | The Fidelity panel validates the model on historical cases; it does not translate validation confidence to the active scenario |
| What parameters were set when this scenario was created other than the fiscal multiplier? | **No** | Only the fiscal multiplier appears in Zone 0 post-creation; political economy settings, conditionality, n_steps rationale are invisible |
| What does the world map show — my scenario's outputs or background data? | **No** | The choropleth relationship to the active scenario is not stated; it shows static reference data |
| What does "financial_active" mean vs. "Financial"? | **No** | Internal field name exposed in the chart UI; "_active" suffix unexplained |
| Is the scenario I selected from the list a good starting point for my analytical question? | **No** | Scenario names are internal test harness identifiers; no analytical description, no indication of what question each scenario addresses |

---

## Part IV — The Input Confidence Gap Family

The observations above reveal not a collection of isolated missing features but a structural pattern distinct from the output legibility family documented in Part I. The unifying diagnosis:

**WorldSim does not give the minister any way to verify that the model was given the right information before she relies on what it says. She can see what the model produced. She cannot see what the model was given.**

Seven gap members, forming the Input Confidence (IC) family:

### IC-1 — Scenario Creation Blindness

The creation form has three fields: name, year, fiscal multiplier. The entity is hardcoded to GRC with no selection available. There is no pre-creation data quality preview — no indication of what data exists at what quality for the requested entity and year before the scenario is created. The minister commits to a scenario without knowing whether the model will use Tier 1 IMF data or Tier 4 synthetic inference for her year.

The most consequential form of this gap: the minister cannot choose what country she is modeling. GRC is hardcoded. The creation form as observed models only Greece — making the tool, in its current creation surface, a Greece-only analytical instrument from the minister's perspective. The Jordan/Egypt scenario visible in the instrument cluster was presumably created through a different pathway (direct API or backend configuration), not through the creation form visible to a first-time user.

### IC-2 — Initial State Opacity

The model's representation of the country's situation at step 0 — the actual indicator values used to seed the trajectory — is not visible anywhere in the primary viewport or accessible via the entity interaction paths observed in this audit. The minister sees "Financial: 0.81" at step 0 but cannot see the component indicators that produced 0.81 (reserve coverage = ? months, current account = ?% of GDP, debt service ratio = ?).

This is consequential for two reasons: (1) the minister cannot verify that the model's starting state corresponds to her understanding of the actual situation, and (2) she cannot provide the creditor side with the specific figures the model used when challenged on input accuracy.

### IC-3 — Data Provenance Invisible at Scenario Level

The API call sequence on scenario load includes `/api/v1/scenarios/{id}/measurement-output?entity_id=JOR&step=8` — the measurement output contains indicator-level data. No API call during the observed load sequence fetches data source attribution, data vintage, or data provenance at the indicator level. Whether this information exists in the API is not determinable from this audit, but it is not surfaced to the primary UI during normal scenario viewing.

The minister knows (from confidence tier labels) that some outputs are T2 ("Moderate confidence") and some are T4 ("model estimate"). She does not know which specific data sources were used for the T2 indicators, or which comparable economies were used for the T4 synthetic inference.

### IC-4 — Fidelity Panel Scope Mismatch

The Fidelity panel is the only existing input/calibration transparency surface. It is substantively valuable — five historical cases, explicit deviation percentages, named structural gaps with issue references. But it answers a different question than what the minister is asking. It validates the model relationship; it does not validate the input data for the active scenario.

A minister who reads the Fidelity panel may believe she has seen the input confidence disclosure. She has only seen the model calibration disclosure. This is the most dangerous gap in the family — not because the content is wrong, but because it is present enough to satisfy the expectation of transparency while leaving the actual input question unaddressed. Partial transparency that looks complete is more dangerous than no transparency at all.

The Fidelity panel is also not scenario-contextual. The same five historical cases appear regardless of what scenario is loaded. The panel does not show the data quality profile for the active scenario's entities, does not indicate which validation case is most analogous to the minister's scenario, and does not adapt to the entities, year, or analytical question in the active scenario.

### IC-5 — Parameter Persistence Failure

Only the fiscal multiplier persists in Zone 0 after scenario creation ("Mode: 2 (Fiscal ×1.3)"). All other parameters — conditionality schedule, political economy settings, n_steps rationale, any external shock injected — are invisible after creation. The creation form's hint text ("Creates a GRC scenario with 3 annual steps starting at the given year") is the only visible reference to the hardcoded n_steps default. After the scenario is created, even this hint disappears.

A minister reviewing her scenario the day after creating it cannot recall from the screen what parameters were used. A minister inheriting a scenario created by a colleague has no way to determine from the screen what parameters were set.

### IC-6 — Choropleth Disconnect

The choropleth occupies approximately 55% of the total viewport when a scenario is loaded. It shows static world reference data (economy tier, income group, population, GDP classification) — not the active scenario's computed values and not the scenario's input data. The relationship between the choropleth and the active scenario is not stated anywhere on screen.

A first-time user reasonably assumes the largest visual element on screen is showing the most analytically relevant data. It is showing background classification data. The disconnect between the choropleth's visual dominance and its analytical irrelevance to the active scenario is a form of input confusion — the minister cannot tell what the map is telling her.

### IC-7 — Internal Field Names in User-Facing Text

Raw database field names appear as user-facing text: "ecological_active," "financial_active," "governance_active," "human_development_active" in the trajectory chart area; "Gdp Usd Millions (USD_millions_cur▼)" in the header; "Economy Tier (dimensionless, dimensionless)" in the attribute selector. The `_active` suffix, `_usd_millions` naming convention, and `(dimensionless, dimensionless)` format string are implementation details, not analytical labels. They expose the internal data model to the user without explaining it.

"financial_active" specifically is ambiguous: does "active" distinguish from a baseline or counterfactual version? A user who has read the ADR documentation knows that "active" refers to the active scenario branch in Mode 2/3. A first-time user does not. The label creates a question ("active as opposed to what?") that the screen does not answer.

---

## Part V — DIC Agent Deliberations

The following deliberations were conducted during this audit session. They represent the standard activation protocol. Captured verbatim.

---

### Chief Methodologist: CHALLENGE — the Fidelity panel's scope and what it does not answer

The Fidelity panel is a real attempt at disclosure — five historical cases, directional accuracy documented (5/5 ✓), magnitude limitations named explicitly with issue numbers and deviation percentages. "GDP is a pure accumulation stock — it only moves when a fiscal event fires and never receives an endogenous recovery impulse." That sentence appearing in the UI is more methodological honesty than most analytical tools provide. But it answers a different question than what the minister is asking.

The minister's input-side question is: *were the data fed into my scenario accurate?* The Fidelity panel answers: *has the model relationship been validated against historical cases?* These are related but distinct. Validating that the model correctly predicted Greece's directional contraction does not tell the minister whether the reserve coverage figure used for Jordan 2024 is current, sourced correctly, or synthetic. A minister who reads the Fidelity panel may believe she has seen the input confidence disclosure. She has only seen the model calibration disclosure.

Three distinct epistemic questions about inputs:
1. Is the model relationship valid? — Fidelity panel answers this.
2. Is the input data for my specific scenario accurate? — not answered anywhere.
3. Were the scenario parameters set appropriately for my context? — not answered anywhere.

Additionally: the Fidelity panel content is highly technical. "MAGNITUDE: 1/2 cases for ADR-006 upgrade" and "Tolerance ±20% → [−13.08%, −8.72%]" require familiarity with backtesting methodology to interpret. These are meaningful to a methodologist; they are not interpretable by a finance minister who has not read the backtesting documentation. The panel has no entry-level plain-language summary: "This model has been tested on five historical crises and correctly predicted the direction of all five. The magnitude of the effect has been validated in one case. Here is what that means for how to use these outputs."

The creation form is the most acute input confidence failure. The minister provides a year (2020), a fiscal multiplier (slider, 0.1–3, default 1), and a name. There is no indication of what data exists for that year before creation, what quality that data is, or what the model will use to seed the initial state. She is asked to specify inputs without knowing what data the model will use for those inputs.

---

### Development Economist: CHALLENGE — initial state invisibility and what baseline means for human impact

The income cohort question is acutely affected by initial state opacity. The bottom quintile consumption figure at step 0 is the baseline against which all subsequent "-0.25" changes are measured. If the minister cannot see what the baseline consumption level was for the bottom quintile in Jordan in 2024 before the model ran, she cannot know whether "-0.25" is catastrophic (if baseline was already near subsistence) or moderate (if baseline was significantly above it). The direction and magnitude of the change are visible. The starting point — which determines the human severity of the change — is invisible.

This is not a labeling problem. It is a structural omission. The human cost ledger strip shows trajectory change but not trajectory origin. A finance ministry arguing against an austerity programme needs to say: "Your proposed conditionality brings bottom-quintile consumption from X to X−0.25. X is already at subsistence level. This step crosses from hardship into humanitarian crisis." She cannot make that argument from the screen because X is not on the screen.

The same applies across all human development indicators. "Human Development 0.75" is a current-position composite. But 0.75 from what starting point? If the scenario starts at 0.80 and declines to 0.75 over 8 steps, that is a different situation than if it starts at 0.76 and holds at 0.75 under a severe shock. The trajectory chart shows the shape of the decline but the initial condition — what the country's baseline human development position was before the scenario began — is invisible.

---

### Geopolitical Analyst: CHALLENGE — the input verification moment and the input challenge

There are two distinct challenge types in a negotiating room. An output challenge: "your model shows reserve coverage dropping to 2 months — that's wrong." The minister can respond by traversing the evidence thread (ADR-015 architecture). An input challenge: "your model assumes Jordan's current account deficit is 8.5% of GDP — the IMF's latest staff report puts it at 11.2%. Your entire trajectory is seeded from wrong data." The minister cannot respond to the second challenge from the current screen. She would need to have separately documented which data the model used and where it came from — not from the tool, but from a separate briefing document she prepared before the session.

The input challenge is the more dangerous one in a negotiating room. It does not require challenging the model's methodology. It only requires producing a different data point. The creditor side has access to IMF data systems in real time. They can produce the 11.2% figure on demand. The minister cannot verify from her screen what figure her model used — let alone produce the source citation for it. The input challenge eliminates the tool's usefulness not by disproving the methodology but by undermining the starting conditions.

The scenario creation form's hardcoded GRC entity and minimal input surface (year + fiscal multiplier only) makes this worse. The minister is not choosing what data goes in; she is choosing a year, and the model silently loads whatever data it has for that year. She cannot tell, before or after the scenario runs, what that data was or whether it matches what the creditor side will use as the ground truth.

---

### Council Orchestrator: VALIDATE — the input confidence family and its relationship to the ML output legibility family

The original ask had three questions. The first audit addressed primarily the third (output confidence). This audit addresses the first (what went in). The second (why does it show what it shows) is partially addressed by ML-5 (causal chain) in the first audit but also has an input-side dimension: the model shows what it shows partly because of how the inputs were structured. A model seeded with incorrect initial state data will show wrong trajectories for reasons the minister cannot detect.

The two families are complementary, not redundant. A minister who has full output legibility (Evidence Thread Architecture, ADR-015) but no input confidence can trace every output to its basis — but the basis was computed from inputs she cannot verify. A minister who has full input confidence but no output legibility can see exactly what went in — but cannot understand or defend what came out. Both are required for the tool to serve the mission.

The north star test for the input confidence family: a finance minister opens WorldSim, loads a scenario for her country, and can answer the creditor's challenge — "what data are you using for Jordan's current account deficit?" — from the screen in under 60 seconds. That question is currently unanswerable from the screen in any amount of time. Addressing it is not a data availability problem; the data is in the system. It is a surface architecture problem: the input data is never brought to the primary viewport.

---

## Part VI — Proposed Framework: Scenario Grounding Architecture

The Evidence Thread Architecture (ADR-015) makes outputs traversable: every Zone 1 primary output carries a basis thread that answers "what produced this and at what confidence?" The Scenario Grounding Architecture makes inputs visible: every scenario carries a grounding surface that answers "what was the model told before it produced this?"

The two architectures are complementary. Evidence threads run forward from output to basis. Grounding surfaces run backward from output to input. Together they close the reasoning chain in both directions — the minister can verify what went in and defend what came out.

### Component 1 — Pre-Creation Data Quality Preview

Before the minister commits to a scenario, the creation form shows the data quality profile for the requested entity and year. When she types "2024" in the year field, the form updates to show:

`Jordan 2024: Financial indicators — T2 (IMF BOP 2024-Q1) · Human Development — T3 (World Bank WDI 2023) · Ecological — T4 (synthetic) · Political Economy — T3 (V-Dem 2023 + synthetic)`

This is a one-line data quality signal per framework, computed from the source registry at the moment of form entry. It answers the question "what will I be working with?" before the scenario is created. It does not prevent creation — a Tier 4 synthetic scenario is valid for exploratory analysis — but it makes the input quality visible before the minister commits to it.

This also requires the entity selection to be made available in the creation form. The hardcoded GRC entity is a current implementation constraint, not an architectural principle. The minister must be able to select which country she is modeling before seeing the data quality preview.

### Component 2 — Scenario Grounding Strip

A persistent strip accessible at one interaction from the primary viewport (a "Grounding" tab adjacent to the Fidelity button, or a Zone 2 surface directly linked from the assumption surface introduced in ADR-015) showing the model's starting conditions for the active scenario:

**Initial state table:** For each framework, the top 2–3 component indicator values at step 0, with source and vintage.

Example:
```
Jordan — Starting conditions at step 0 (Dec 2023)

Financial
  Reserve coverage: 3.2 months  [IMF BOP 2024-Q1, T2]
  Current account: −6.8% GDP    [IMF Article IV 2023, T2]
  Debt service ratio: 18.4%     [World Bank 2023, T2]

Human Development
  Bottom quintile consumption: 0.62 (index)  [World Bank WDI 2023, T3]
  Unemployment: 17.8%                        [ILO ILOSTAT 2023, T2]
  
Ecological
  CO₂ per capita: 3.1 tCO₂eq   [synthetic — comparable MENA economies, T4]
```

This surface does not replace the entity drawer or the Zone 3 methodology documentation. It is a minister-facing surface showing the model's representation of the country's actual situation, grounded in cited sources, before any model computation is applied.

### Component 3 — Fidelity Panel Contextualisation

The Fidelity panel retains its current content (five historical cases, directional validation, structural gap documentation) and adds a scenario-contextual section when a scenario is loaded:

`For your scenario (JOR · EGY, 2024): The most analogous validation case is THA 1997 (external current account pressure, middle-income open economy). Directional accuracy has been validated for this crisis mechanism. Magnitude has not been validated for this entity type. Use outputs for direction and threshold detection; confirm magnitudes with country-specific analysis before citing.`

This section requires the Chief Methodologist to define the "analogous case" selection logic — which validation case applies to which scenario type. It is not automatic text; it is a methodology commitment that produces a scenario-specific trust signal. Without this, the Fidelity panel remains a model-level disclosure that does not translate to the minister's specific situation.

### Component 4 — Parameter Persistence in Zone 0

All parameters set at scenario creation (not just the fiscal multiplier) are persisted in Zone 0. The assumption surface introduced in ADR-015 partially addresses this for the most explanatory parameters. The Scenario Grounding Architecture extends this to the full parameter set: a "Scenario Parameters" section accessible at one interaction from Zone 0, showing every parameter used in the scenario with its value and (where applicable) the evidence basis for that value.

The scenario creation form should also surface these parameters as editable fields rather than silently applying defaults. The minister who did not set conditionality to "standard" — it was applied as a default — should be able to see that default was applied and understand what it means.

---

## Part VII — Relationship to ADR-015 and Filing Implications

ADR-015 (Model Legibility Architecture — Evidence Thread Architecture) addresses the output legibility family. It is correctly scoped and does not need to be restructured to accommodate this family.

The IC family (IC-1 through IC-7) and the Scenario Grounding Architecture are a distinct architectural scope. They require their own ADR (ADR-016 candidate), their own panel (including Chief Methodologist as primary author on the data provenance questions, Backend/API as implementing agent, UX Designer for the creation form and grounding strip), and their own implementation sequence.

**Sequencing recommendation:** IC-1 (Scenario Creation Blindness) and IC-2 (Initial State Opacity) are prerequisites for the Scenario Grounding Strip (Component 2) and block Demo 5 more acutely than some ADR-015 components — a real external participant who creates a scenario from the creation form and cannot choose their country cannot run a meaningful demo. The EL should consider IC-1 resolution for M14 scope independently of the full ADR-016 scope.

**The complete trust architecture now has two halves:**
- Half 1 (output side): Evidence Thread Architecture — ADR-015 — "here is why this output is what it is"
- Half 2 (input side): Scenario Grounding Architecture — ADR-016 — "here is what the model was told before it produced this"

Both halves are required for a finance minister to sit in front of WorldSim and trust what she sees enough to defend it at a table. ADR-015 addresses one half. This document provides the empirical evidence and framework for the second.

---

*This document is the evidence record for the input confidence gap family (IC-1 through IC-7). It is a companion to `docs/demo/m14/reviews/2026-06-15-ux-legibility-audit-minister-exercise.md`. Software version audited: v0.13.0-2-g097d3dc. DIC deliberations captured verbatim. Nothing in this document is summarized.*
