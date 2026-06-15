# WorldSim UX Legibility Audit — Minister-in-the-Chair Exercise
## M14 Evidence Record for ADR-015

> **Date:** 2026-06-15  
> **Session type:** Live application audit — UI at localhost:5173, backend at localhost:8000  
> **Conducted by:** Architect Agent, using Playwright screenshots of the running application  
> **Referenced by:** ADR-015 (Model Legibility Architecture)  
> **Scenarios observed:** Jordan/Egypt 2024 Hormuz Demo 4 (558a27fe, completed, Mode 2 Fiscal ×1.3); Greece 2010-2015 M8 Demo (ee1bc771, completed, Mode 1)  
> **Purpose:** Empirical ground truth for the model legibility gap family that ADR-015 proposes to address. This document captures the full session exchange, live UI observations, gap taxonomy, and domain intelligence council consultations that produced the ADR-015 framework proposal. Nothing in this document is summarized.

---

## Part I — The Exercise

The exercise instruction: *Imagine you are a finance minister sitting in front of WorldSim for the first time. You are looking at the output screen. Ask yourself: what went into producing what I am seeing, why does the model show what it shows, and how confident should I be in it? Try to answer those questions using only what is visible in the UI. Document what you can and cannot answer.*

The audit was conducted by loading the live application at localhost:5173, taking Playwright screenshots of each instrument zone, and reading the screen as a first-time user would — without reference to source code or methodology documentation.

---

## Part II — Live UI Observations

### 2.1 — The Landing State (No Scenario Loaded)

**What is on screen:**

The screen is a world map. It takes approximately 90% of the viewport. The header is a dark bar at the top containing: "WorldSim" (application name), a dropdown labeled **"Gdp Usd Millions (USD_millions_cur▼)"** (a raw database field name, verbatim from the internal schema), a checkbox labeled "Compare scenarios," a button "Scenarios ▼," and a button "Fidelity ▼." The map is colored in shades of blue ranging from near-white to near-black. There is no visible legend for the choropleth colors. Map controls (+, −, ▲) appear at top right. "MapLibre ⓘ" appears at bottom right.

**What a first-time user faces:** No orientation. No explanation of what the tool does. No indication of what the map is showing. No invitation to begin. No scenario is loaded. The raw database field name "USD_millions_cur" is the first label visible after the product name. There is no sentence explaining the purpose of the application or what the user should do.

### 2.2 — Opening the Scenarios Panel

**What is on screen after clicking "Scenarios ▼":**

A panel opens showing a scrollable list of scenarios. Each row shows a scenario name and a colored status badge (green "completed", orange "running"). Scenario names visible include: "SriLanka-2022-BPO-Validate," "G8b-REG-multiplier-1781374921053," "G8b-AC1-1781374914869" — internal test names constructed from test harness identifiers. Two buttons appear per row: "Select" and "+ Compare." A "NEW SCENARIO" form at right contains a year input (pre-populated "2025") and a "Create" button. A refresh button (↻) appears next to the "Scenarios" section header.

**What a first-time user faces:** Scenario names do not indicate what analytical question they address. A first-time user without prior context cannot identify which scenario is relevant to their negotiating situation. The creation form provides no guidance on what parameters are required or what the year field represents relative to the country situation being modeled.

### 2.3 — Hormuz Demo 4 Loaded (Mode 2, Fiscal ×1.3, Completed, 8 Steps)

This is the primary scenario used for the audit — the Jordan/Egypt Hormuz Demo, which represents the closest to a real-world negotiating room scenario in the current fixture library.

**Identity strip (Zone 0 — always visible):**
> `Scenario: Jordan/Egypt 2024 Hormuz Demo 4 — 2026-06-12-9m6nqt [branch]  /  Entities: JOR, EGY  /  Mode: 2 (Fiscal ×1.3)  /  Status: Complete (8 steps)`

**Header control bar:**
Mode selector shows three options: **"Replay" | "Simulation" (highlighted in blue, active) | "Active Control"**. A separate button labeled **"Mode 3"** appears alongside. Step counter reads: **"Step 0 / 8"**. A "Next Step ▶" button is present.

**Immediately visible contradiction:** The identity strip says "Status: Complete (8 steps)" — the scenario has already run to completion and the full 8-step trajectory is displayed in the chart. But the step counter reads "Step 0 / 8." A first-time user looking at both simultaneously cannot determine whether they are viewing step 0 output or the full trajectory. The trajectory chart shows 8 steps of data; the step counter implies the user is at step 0. This is the most immediately disorienting element in the interface for a new user.

**Trajectory chart (Zone 1A):**

Four colored curves on a step axis labeled "Step 0" through "Step 8," with dual date annotations below each step tick: "JOR: Dec 2023" / "EGY: Dec 2023" through "JOR: Dec 2030" / "EGY: Dec 2030." The Y-axis spans 0.00 to 1.40, with tick marks at 0.00, 0.35, 0.70, 1.05, 1.40. One dashed horizontal line is labeled "Planetary boundary" — positioned at approximately y=1.0. The trajectory shows two lines spending significant time above this dashed reference line.

Legend: "Ecological (JOR · EGY)," "Financial (JOR · EGY)," "Governance (JOR · EGY)," "Human Development (JOR · EGY)."

Below the chart: *"Each curve is a framework composite across JOR and EGY. Both entities contribute to each trajectory."*

**Alert panel (Zone 1B):**

Top detail slot (always visible, no interaction required):
> **TERMINAL** — CO₂ Boundary Proximity — **ECO** — **JOR**
> Step 8
> Current **1.203**  ·  Floor **1.000**
> **BREACH PROJECTED at step 8** · **8 consecutive steps**
> *Moderate confidence — cite with caveat*

Compact rows below (scan-only, no click targets):
> `TERM  JOR  FIN  Reserve Coverage ...  Stp 8`
> `TERM  JOR  GOV  Democratic Qualit...  Stp 8`

Both compact rows are truncated mid-name with an ellipsis.

**PMM Widget (Zone 1C):**
> Policy Maneuver Margin — projected
> **1.00 →**
> ↓ lower = more constrained

**Four-Framework Current Position (Zone 1D):**
> JOR · EGY
> Financial  **0.81**
> Human Development  **0.75**
> Ecological  *1.0 = boundary*  **0.60**
> Governance  **0.37**

**Human Cost Ledger strip (below Zone 1A):**
> HUMAN COST LEDGER
> Bottom Quintile ...  **-0.25  T4**  ·  Unemployment **16.4%  T4**
> Poverty **—**  ·  Income Share — ...  **—**
> Access to Health...  **—**

**Choropleth map (below instrument cluster, occupying ~55% of total viewport):**

World map colored by an attribute. The attribute selector in the header still reads "Gdp Usd Millions (USD_millions_cur▼)." No error message visible in this view. The geographic relationship between the choropleth and the Hormuz scenario above it is not stated.

### 2.4 — Greece 2010-2015 M8 Demo (Mode 1, Completed, 6 Steps)

**Identity strip:**
> `Scenario: Greece 2010-2015 M8 Demo — 2026-06-11-9gsm8f  /  Entity: GRC  /  Status: Complete (6 steps)`

**Trajectory chart (Zone 1A):**

Four curves. Y-axis: 0.00 to 1.40. Dashed "Planetary boundary" line at ~y=1.0. One curve (Ecological, teal) sits consistently above 1.0 throughout all 6 steps (approximately at 1.10-1.14). Financial (blue, labeled "(single-country index)") starts at approximately 0.27 at step 0 and drops to approximately 0.05 by step 2, remaining near-zero through step 6. Human Development (gold, "(single-country index)") starts at approximately 0.77 and declines to approximately 0.50 by step 6. Governance (purple) is flat at approximately 0.37 throughout.

Below the chart: *"Scores reflect absolute indicator position, not ranking. Cross-scenario comparison is not valid."*

Note: the legend labels for Greece Financial and Human Development include the qualifier "(single-country index)" as part of the legend text. No equivalent qualifier appears for Ecological or Governance.

**Alert panel (Zone 1B):**

Top detail slot:
> **TERMINAL** — Reserve Coverage (months) — **FIN** — **GRC**
> Step 6
> Current **2.000**  ·  Floor **2.500**
> **crossed threshold at step 6** · **6 consecutive steps**
> *Moderate confidence — cite with caveat*

Compact row:
> `TERM  GRC  ECO  CO₂ Boundary Prox...  Stp 6`

**PMM Widget (Zone 1C):**
> Policy Maneuver Margin — historical
> **— —** (two dashes; direction arrows visible as formatting artifacts)
> ↓ lower = more constrained
> *All thresholds breached — see alerts* (in red)

**Four-Framework Current Position (Zone 1D):**
> Financial  **0.08**
> Human Development  **0.49**
> Ecological  *1.0 = boundary*  **1.11**
> Governance  **—**

---

## Part III — What the Finance Minister Can and Cannot Answer

The following table is the empirical record from the live audit. Each question was asked as a first-time user; the answer reflects only what is visible on screen without opening drawers, navigating to Zone 3, or reading documentation.

| Question | Answerable from screen? | If yes, from what? |
|---|---|---|
| Has any threshold been crossed? | **Yes** | Zone 1B top detail slot — TERMINAL label and severity color |
| Which frameworks are most stressed? | **Roughly** | Zone 1D score comparison; alert panel severity |
| Is the situation getting better or worse? | **Direction only** | Trajectory curves (slope visible, no quantified change rate) |
| Which outputs are citable at a negotiating table? | **Partially** | "Moderate confidence — cite with caveat" / "High confidence — cite directly" labels in Zone 1B top slot only |
| What does Financial 0.81 mean in real terms? | **No** | No scale anchor, no reference range, no indicator list visible in Zone 1 |
| What does Human Development 0.75 mean for actual people? | **No** | Framework label only; no indicator breakdown, no cohort information in Zone 1 |
| What does Governance 0.37 mean? | **No** | Framework label only; no component information |
| What is the ecological "Planetary boundary"? | **Partially** | The label "Planetary boundary" appears on the chart; what boundary (CO₂? biodiversity? water?) is not stated in Zone 1 |
| Is being above or below the Planetary boundary line bad? | **Not clearly** | The chart shows the ecological composite above 1.0 for Greece (score 1.11) and below 1.0 for Hormuz (score 0.60); both have TERMINAL ecological alerts; the directionality relationship between composite score, the reference line, and the alert is not explained |
| What does PMM = 1.00 mean in policy space? | **No** | "↓ lower = more constrained" is the only reference point; the neutral point, maximum, and minimum are unstated; the policy interpretation (what can the ministry still do at this margin?) is absent |
| What is "— —" in Zone 1C for Greece (All thresholds breached)? | **Partially** | The red text explains the null state; but a user unfamiliar with the metric cannot tell what it means that the PMM has no computable value |
| What caused the Financial score to drop sharply at steps 4–5? | **No** | No causal attribution in Mode 1 or Mode 2 |
| What model assumptions produced this trajectory? | **Partially** | "Mode: 2 (Fiscal ×1.3)" appears in the identity strip — fiscal multiplier only; political economy parameters, conditionality schedule, initial attributes, data vintage are invisible |
| What data sources underlie these scores? | **No** | No source citations in Zone 1 or Zone 2 visible on screen |
| What is "T4" next to Bottom Quintile -0.25? | **No** | T4 is a raw confidence tier code with no expansion or explanation visible in Zone 1 |
| What does "-0.25" mean for Bottom Quintile? | **No** | No unit, no baseline, no reference range |
| Why are Poverty, Income Share, and Access to Health showing dashes? | **No** | No explanation whether dashes represent missing data, inapplicable metric, zero value, or computation failure |
| What does "Moderate confidence — cite with caveat" mean concretely? | **No** | No caveat text is provided; "cite to whom" and "with what caveat wording" are not specified |
| What does "(single-country index)" mean in the legend? | **No** | The label is a methodological qualifier; its implication (that cross-scenario comparison is invalid) appears only as a footnote below the chart, not inline |
| Is this trajectory historically unusual? | **No** | No historical positioning; no comparable case reference |
| What is the programme_survival_probability? | **No** | Political economy module output is not visible anywhere in Zone 1 |
| What does "Irreversible" mean when shown for Human Development? | **Not answerable in Zone 1** | The reversibility label (visible in Mode 3 and Zone 1D when alerts are active per Rider #271) shows "Irreversible" or "Recoverable (N yrs)" — but the timeframe, the definition of recovery, and the affected cohort are not stated |
| What does "[branch]" in the scenario name mean? | **No** | The identity strip includes "[branch]" in the scenario name; its significance (this is a Mode 2 branched scenario from a baseline, not an original run) is not explained |
| Why is the Step counter showing "Step 0 / 8" when Status says "Complete (8 steps)"? | **No** | The contradiction between these two display elements is not resolved by any visible text; a first-time user cannot determine whether they are at step 0 or viewing a completed scenario |

---

## Part IV — The Full Family of Gaps

The questions-and-answers table above reveals not a list of isolated missing features but a structural pattern. Seven gap families, each a different face of the same problem: **WorldSim renders outputs without the reasoning that produced them.**

### ML-1 — Score Anchoring

The composite scores displayed in Zone 1D and on the trajectory chart are dimensionless values without reference frames. "Financial: 0.81" conveys direction (compared to a lower score) and relative position (compared to the other three frameworks), but not meaning. 0.81 of what? Is 0.81 in a healthy range? Does 0.81 for Greece represent a different absolute condition than 0.81 for Jordan? (For single-country index scenarios, it does.)

The only framework with any scale annotation is Ecological: "1.0 = boundary." This tells the user the boundary is at 1.0. It does not tell the user that above 1.0 is bad (for Greece, Ecological = 1.11 → TERMINAL; the score exceeds the boundary threshold) or that below 1.0 is also bad in a different way (for Hormuz, Ecological = 0.60 → different type of TERMINAL breach via CO₂ proximity indicator). There is apparent directional inconsistency between scenarios for the same framework, which is genuinely confusing on first encounter.

For Financial, Human Development, and Governance: no scale annotation at all. A score can range from 0.08 (Greece Financial, near-collapse) to 0.85 (Hormuz Financial, relatively healthy) with no visible indication of what range represents "stable" versus "at risk" versus "in crisis."

**What the user needs that is absent:** A minimal reference frame per framework — either the historical normal range for comparable countries at this type of scenario, or a explicit label of what value represents the boundary between safe and at-risk territory. This is a Zone 1 anchor problem, not a Zone 3 documentation problem.

### ML-2 — Directionality Confusion (Ecological)

The Ecological framework exhibits a directionality that is opposite to user intuition and inconsistent with the other three frameworks. For Financial, Human Development, and Governance: higher scores are intuitively better (more financial stability, better human development, stronger governance). For Ecological: the relationship between the composite score and the direction of danger is not readable from the chart.

Evidence from the live audit:
- Greece Ecological = 1.11 (above the "Planetary boundary" dashed line at 1.0) → TERMINAL alert
- Hormuz Ecological = 0.60 (below the "Planetary boundary" dashed line at 1.0) → TERMINAL alert

Both scenarios have TERMINAL ecological alerts but the composite scores are on opposite sides of the 1.0 reference line. A first-time user observing these two scenarios consecutively would be unable to determine whether ecological safety is above or below 1.0.

The root cause: the ecological "composite" in these two scenarios is computed differently (one is a proximity score, one reflects a different underlying measurement), and the "Planetary boundary" dashed line in the trajectory chart is the MDA floor for the warning-level ecological threshold — not a universal directional marker for the composite score. The composite and the MDA floor operate on different scales in some configurations. The chart does not explain this.

**What the user needs:** Either a single consistent directional convention across all frameworks (green = good, and the boundary is labeled as such), or explicit directional annotation on each curve. "↑ = further from boundary" / "↓ = approaching boundary" per framework, visible in the trajectory chart.

### ML-3 — Assumption Invisibility

The model assumptions that produced the visible trajectory are not co-visible with the output. What is visible:
- Fiscal multiplier ×1.3 (from identity strip, only when Mode 2 is active)
- Mode (Replay / Simulation / Active Control)
- Entity and step count

What is not visible:
- Political economy parameters (legitimacy index, conditionality structure, elite capture coefficient)
- Data vintage (are these 2024 or 2020 inputs?)
- Conditionality schedule (if one is applied)
- Initial attribute overrides
- Which sensitivity regime the model is operating in (has any scenario shock been injected?)

When the IMF team challenges "why does your model show a TERMINAL Financial alert at step 8?" the minister's analyst cannot answer from the primary screen with anything more than "the fiscal multiplier was 1.3." The assumptions that shape the trajectory are creation-time inputs that disappear from the primary reading surface once the scenario is created.

**What the user needs:** A persistent, minimal "active assumptions" display — not all parameters, but the 3–4 inputs that the sensitivity analysis identifies as most explanatory of the current trajectory shape.

### ML-4 — Evidence Basis Labeled but Unexplained

Confidence tier information appears on screen in two forms:
- Zone 1B top detail slot: "Moderate confidence — cite with caveat" / "High confidence — cite directly" / "Early estimate — confirm before citing" (negotiation-defensibility labels)
- Human Cost Ledger: "T4" codes

Both are labeled but unexplained. "Moderate confidence — cite with caveat" is an instruction ("cite with caveat") without the caveat. A minister challenged on the number needs to say: "We cite this with the caveat that [specific limitation]." That caveat text is not available from Zone 1.

"T4" is a raw tier code. A user who has not read DATA_STANDARDS.md cannot know that T4 means "Model estimate — synthetic inference from comparable economies, not observed data for this country." The tier system is real and important; its Zone 1 representation is opaque code.

Additionally: the distinction between *data quality* (what the tier represents — is the underlying data from IMF BOP or from synthetic inference?) and *model calibration* (whether the model relationship transforming that data into a composite score has been validated against historical cases) is completely invisible. A Tier 2 data source fed into an uncalibrated model relationship produces an output that appears as "Moderate confidence" — when the real uncertainty is not in the data but in the model relationship.

**What the user needs:** The confidence tier label at Zone 1 must be expandable to (at minimum) three pieces of information: what source type underlies the indicator, whether the model relationship is calibrated or pre-calibration, and the specific caveat text the ministry team should use when citing this output.

### ML-5 — Causal Chain Absent

Why did the Financial score drop at steps 4–5 in the Hormuz scenario? What drove the Reserve Coverage breach in Greece at step 6? The model has answers to these questions — the propagation chain records which indicator driving what composite score crossing which threshold. None of this is visible in Mode 1 or Mode 2.

Causal attribution exists for Mode 3 control inputs only: "Caused by: fiscal multiplier ×1.3 applied at step 3." This is the right form — it names the cause. But it fires only when the user has applied a control input in Mode 3. For the intrinsic dynamics of the model (what would have happened without any control input, what historical events drove a trajectory), no causal explanation is provided.

The Greek crisis scenario is the paradigm case: the Financial collapse is visible in the chart (a steep descent from step 2 onward) but unexplained. A user cannot tell from the chart whether the drop is driven by debt service costs, fiscal consolidation effects, banking sector collapse, or some other mechanism the model tracks. They see the effect; the cause is invisible.

**What the user needs:** Per-alert causal attribution in Modes 1 and 2 — not as detailed as the Mode 3 control-input attribution, but a minimum of: what indicator drove the threshold crossing, and what the model identifies as the primary propagation source for that indicator's movement.

### ML-6 — Cross-Examination Surface Absent

The path from a challenged output to its methodological basis in the current UI:
1. Note which Zone 1B alert or Zone 1D score is being challenged
2. Click the entity label or navigate to the entity detail drawer
3. Find the relevant framework panel (Zone 2)
4. Expand the indicator row
5. Locate the methodology note (Zone 3, collapsed by default)
6. Read the methodology note

Six steps. Under negotiating room time pressure, with an IMF team waiting for a response, this path fails. The minister's analyst needs to produce the basis for a challenged number in under 30 seconds. The current navigation architecture does not support this.

There is no "defend this" mode. There is no path from a specific challenged number directly to the evidence chain behind it. The methodology documentation exists; it is not traversable from the challenged output under time pressure.

**What the user needs:** A two-interaction maximum path from any challenged Zone 1 output to its basis statement, accessible without navigating away from the primary viewport.

### ML-7 — Orientation Absence (Landing State)

The very first thing a first-time user sees is a world map and the label "Gdp Usd Millions (USD_millions_cur▼)." This is a trust problem before any of the model legibility problems apply. If a user does not understand what the tool does in the first 30 seconds, they will not engage deeply enough to reach the instrument cluster.

For Demo 5 — the live external demo with real participants that closes M14 — this gap is a demo-critical risk. External participants who have never seen WorldSim will see a world map and a database field name as their first impression of a tool designed to help a finance minister defend sovereign decisions. The mismatch between mission and first impression is acute.

**What the user needs:** A minimal orientation layer — one or two sentences stating what the tool does and who it is for, visible on landing before any scenario is selected. Not a tutorial. A single sentence: "WorldSim models the fiscal, human, ecological, and governance impacts of economic policy decisions. Load a scenario to begin analysis."

---

## Part V — DIC Agent Consultations

The following consultations were conducted in the session that produced this audit. They represent the standard activation protocol: `[Agent Name]: CHALLENGE — [topic]`. The consultations are recorded verbatim as they occurred.

---

### Chief Methodologist: CHALLENGE — model legibility for pre-calibration outputs

The most fundamental legibility problem is one this design consistently under-weights: the outputs currently displayed are pre-calibration outputs, and the confidence tier labels do not adequately communicate what that means. "High confidence — cite directly" on a pre-calibration output is misleading. High confidence relative to what? The tier describes the data quality of the underlying indicator, but not the calibration status of the model relationship that transforms that indicator into a composite score.

There are two distinct epistemic layers that the current display conflates: *data quality* (Tier 1–5, based on source reliability and vintage) and *model calibration* (whether the model relationship has been validated against historical cases). An indicator can be Tier 1 data fed into an uncalibrated model relationship, producing an output that carries a "High confidence" label despite having never been validated against an actual historical trajectory.

The ia1_disclosure exists precisely to address this. That it lives in Zone 3 by design is not acceptable for the mission. It must be zone-zero — permanently visible, not collapsible, on every output screen. Not as a wall of text but as a persistent signal: one visual indicator that tells the minister whether she is looking at calibrated or pre-calibration output, and what the consequence of that distinction is for her negotiating argument.

The PMM is the clearest example of this problem. It is a novel metric — the "coffin corner index" — that has no external reference point a minister could cite. It is not a number you find in the World Bank's database or the IMF's Article IV staff reports. Displaying it as "1.00" with only "↓ lower = more constrained" implies it has a defensible quantitative basis. Unless that basis is explicitly stated and traceable, the number is a liability at the table, not an asset. Before the PMM can appear in Zone 1C as a primary instrument, the screen must answer: 1.00 of what? What is the policy interpretation of moving from 1.00 to 0.80? What historical cases validate this metric?

---

### Development Economist: CHALLENGE — Human Development score interpretability and the Human Cost Ledger

A Human Development composite score of 0.75 tells the minister's analyst almost nothing about what is actually happening to real people. The label "Human Development" is correct at the framework level. It is useless at the decision level.

The relevant question at the negotiating table is not "what is the Human Development composite?" It is: "which income quintile crosses a critical capability threshold, and at what step?" The current Zone 1 display answers the first question and not the second.

The human cost ledger strip addresses this — it shows poverty, unemployment, access to health — but in its current state it is largely blank or showing values without units or reference points. "-0.25  T4" for Bottom Quintile is unreadable. -0.25 of what? Compared to what baseline? The T4 tag is unexplained. "Poverty —" and "Access to Health... —" with dashes everywhere suggests either the model is not computing these or the data is absent — but the user cannot tell which.

The strip appears to be mostly empty. This is the primary human cost display visible without opening a drawer. For a tool whose founding document states "the human cost ledger is never a footnote — it is a primary output with equal visual weight to financial indicators," the current state of this strip is mission-critical failure in its current form.

The "Irreversible" label on Human Development (visible in Mode 3 via the reversibility classification system, Rider #271) is the most consequential single piece of information that can appear in Zone 1. It means a capability loss that the model predicts cannot be recovered within the projection horizon. A minister must be able to state: irreversible by what measure, over what timeframe, affecting which population. These answers are not on screen.

---

### Political Economist: CHALLENGE — political economy module visibility

The political economy module (G6, ADR-013) computes `programme_survival_probability`. This is the metric that most directly answers the negotiating room question: "will this programme survive long enough to produce the fiscal adjustment it promises?" At step 1 of the Greece scenario with legitimacy_index=0.40, the probability was 0.595. That number is not visible anywhere in Zone 1, Zone 2, or the primary viewport.

This is a severe legibility gap. The finance ministry team may be defending a fiscal path that the model believes has a 40% chance of political collapse by step 3 — and that finding is invisible in the primary viewport. It is accessible through the measurement output API and appears in Zone 2 (entity detail drawer, framework panels), but is not surfaced to the user without navigating away from the instrument cluster.

The political economy outputs — conditionality decomposition, elite capture coefficient, legitimacy dynamics, implementation capacity scaling — are computed but not surfaced. From the minister's perspective, the model is showing her economic trajectories while silently running political feasibility assessments she cannot see.

This is the most direct violation of the mission. The tool is built specifically to surface the political constraints that the IMF side can see (they have political economy staff) but the ministry side cannot. That advantage is eliminated if the political economy outputs are invisible to the ministry's analyst.

---

### Geopolitical Analyst: CHALLENGE — what "trust at the table" actually requires

The minister is at a table where the creditor side has challenged her on a number. The specific scenario: the IMF analyst says "your reserve coverage estimate is overstated — your model assumes a fiscal multiplier of 1.3 but the evidence base for that in this context is weak."

What the minister needs to respond is not another number. It is a provenance chain: "The fiscal multiplier of 1.3 is drawn from the peer-reviewed range for middle-income economies under external pressure — Ilzetzki et al. 2013 and Batini et al. 2014 — which places the range at 0.8–1.5 for this country type. Our model uses the midpoint with ±0.2 sensitivity band, reflected in the Tier 2 confidence rating you see on this output."

That response is possible in principle — WorldSim has calibration documentation. But it is not achievable from the primary screen. It requires the minister's analyst to have pre-memorized or pre-printed the methodology documentation. The tool fails at the moment of highest-stakes use precisely because the reasoning chain is not traversable from the output under time pressure.

The scenario identity strip shows "[branch]" in the name — the scenario is a Mode 2 branch from a baseline. A first-time user does not know what this means for how to interpret the outputs. Is a branch more or less reliable than an original scenario? What does branching from a baseline at step 3 imply for the trajectory at steps 1–3? These questions are unanswered by the display.

The minimum viable trust architecture for a negotiating room is: every primary number must be reachable from challenge to evidence in two interactions. Not three. Not "open a separate document." Two clicks from the challenged number to the basis statement. One more to the full methodology. That is the kryptonite design constraint operationalized: three economists on the ministry side need to be able to respond to a challenge as fast as one hundred economists on the IMF side can make it.

---

### Council Orchestrator: VALIDATE — proposed framework against north star test

The north star question: does this decision make the tool more useful to a finance minister sitting across from an IMF negotiating team, in that moment?

The current model legibility architecture fails this test in a specific and traceable way: it optimizes for signal detection (are thresholds being crossed?) while providing no support for signal defense (what produced the crossing, and is it defensible?). The minister can use the tool to discover that something is wrong. She cannot use it to argue why what is wrong matters or what the model's basis for saying so is.

The proposed framework — Evidence Thread Architecture — passes the north star test at the paradigm level if (and only if) it meets four conditions:

1. The evidence thread must be visible without any interaction at L0 (tier + basis type on every primary output)
2. The basis statement at L1 must be reachable in one interaction from any primary output
3. The cross-examination mode must be activatable with a single action, not buried in settings
4. The political economy outputs must be Zone 1, not Zone 3

The north star test fails if these threads increase cognitive load in Mode 3 (active steering). The architecture must distinguish between preparation mode (where evidence depth is valued) and negotiation mode (where speed of the primary read is paramount). The threads must add information at L0 without adding visual weight that competes with the primary cognitive task.

---

## Part VI — Proposed Framework: Evidence Thread Architecture

The core diagnosis stated precisely: **WorldSim renders outputs without the reasoning that produced them. The reasoning exists — in the engine, in the data, in the calibration records — but it is inaccessible from the primary reading surface under the time and cognitive constraints of actual use.**

The information hierarchy (Zone 1 → Zone 2 → Zone 3) organizes by *interaction depth* — how many clicks to reach content. The Evidence Thread Architecture organizes by *reasoning depth* — how many causal steps from output to basis. These are orthogonal axes. Currently: high visual primacy = shallow reasoning depth visible. The proposed change: high visual primacy + shallow reasoning depth visible at L0 (zero interaction), medium reasoning depth at L1 (one interaction), full reasoning depth at L2 (existing Zone 3). The visual hierarchy does not change. The reasoning accessibility does.

### Component 1 — Basis Threads on Every Primary Output

Every primary number carries a minimal, always-visible basis annotation. Not a tooltip. Not a Zone 3 note. A persistent one-line annotation that answers "what produced this and can I trust it."

**Zone 1D current:** `Financial  0.81`  
**Zone 1D proposed:** `Financial  0.81  [Tier 2 · 4 indicators · IMF/Central Bank 2024]`

**Zone 1C current:** `1.00 →` with `↓ lower = more constrained`  
**Zone 1C proposed:** `1.00 →` with an interpretation anchor: `neutral point 1.0 — values below 0.5 indicate critical constraint — [Tier 3 composite · pre-calibration]`

**Zone 1B compact rows current:** `TERM  JOR  FIN  Reserve Coverage ...  Stp 8` (truncated mid-name)  
**Zone 1B compact rows proposed:** Full indicator name visible, or a defined 24-character abbreviation that does not truncate mid-word

**Human Cost Ledger current:** `-0.25  T4`  
**Human Cost Ledger proposed:** `-0.25 (capability index) [T4 · model estimate]`  with unit and tier meaning inline

### Component 2 — The Assumption Surface

A persistent strip between the identity header and the instrument cluster, visible whenever a scenario has been advanced beyond step 0, showing the model inputs that most explain the current trajectory shape:

> `Fiscal ×1.30 · Political economy: enabled · Conditionality: standard · Data: 2024-Q1 vintage`

Not all parameters — the 3–4 inputs that the sensitivity analysis identifies as most explanatory. The backend's sensitivity computation already exists; this surface makes the top-sensitivity inputs visible without requiring the user to navigate to a configuration screen.

### Component 3 — Political Economy in Zone 1D

`programme_survival_probability` belongs in Zone 1D as a fifth row, labeled "Political Feasibility," visible when the political economy module is enabled. At a minimum: the survival probability, its confidence tier, and whether it is declining. The political economy module's most mission-relevant output should not require opening a drawer.

### Component 4 — The Cross-Examination Mode

A single-action mode (keyboard shortcut or persistent "Defend" button in the header) that transforms the primary viewport for the negotiating room moment. When active:
- All Zone 1B alerts expand to show full indicator name, floor basis, and source statement inline
- All Zone 1D scores show the 3–4 component indicators beneath each composite (inline, not in drawer)
- The PMM widget shows its interpretation anchor (what 0.5 means, what 1.5 means, in policy language)
- Programme_survival_probability appears inline with programme_collapse scenarios if available

This mode does not change the layout architecture. It adds the L1 basis layer inline. When toggled off, Zone 1 returns to its current compact form. The toggle is designed for the 90-second window when a specific number is challenged.

### The Paradigm Statement

The current design treats transparency as a *destination* — navigate to Zone 3 to reach it. The proposed design treats transparency as *metadata on every output* — visible at L0 (always present, minimal), expandable to L1 (one interaction, basis statement), and navigable to L2 (existing Zone 3 content, accessed from the output rather than from a separate documentation entry point).

The minister can read the current UI. She cannot defend it. The Evidence Thread Architecture closes the gap between reading and defending without rebuilding the layout.

---

## Part VII — Pre-Implementation Decisions Required

These are not implementation decisions. They are framework decisions that implementation must follow. They are recorded here for EL resolution at the ADR acceptance stage.

**Decision 1 — Step counter bug.** The header shows "Step 0 / 8" when the scenario is Complete and the trajectory shows 8 steps. This is a verifiable display bug that creates an immediate trust failure for first-time users. This should be fixed as a prerequisite to any legibility work — a broken step indicator undermines trust in everything else on screen.

**Decision 2 — Directionality of Ecological composite scores.** The Ecological framework exhibits apparent directional inconsistency between the Greece scenario (Ecological = 1.11, above "Planetary boundary" at 1.0 → TERMINAL) and the Hormuz scenario (Ecological = 0.60, below "Planetary boundary" → TERMINAL via CO₂ proximity indicator). The directionality relationship between the composite score, the MDA floor reference line, and the alert severity is not readable from the chart. This requires either a design decision about consistent directionality conventions or explicit directional annotation on the Ecological curve before any basis-threading work is done.

**Decision 3 — PMM interpretation anchor.** The Chief Methodologist must define what PMM values mean in policy language before the PMM can carry an L0 basis thread. The neutral point, the critical threshold, and the policy interpretation of moving between values must be methodology commitments, not frontend labels. This is a Chief Methodologist deliverable before the PMM component of Evidence Thread Architecture can be specified.

**Decision 4 — Programme_survival_probability in Zone 1D.** Placing political economy outputs in Zone 1D changes the primary instrument cluster layout. Does this require an amendment to ADR-008 (UX Architecture — instrument cluster layout) and/or ADR-013 (Political Economy module boundary)? The EL must decide the architectural path before implementation.

**Decision 5 — Cross-examination surface scope for M14.** The live external demo (#843) that closes M14 is the natural forcing function for the cross-examination surface. If external participants will challenge outputs — and they will — the minister's analyst needs to answer from the screen. Does M14 scope include the full cross-examination surface, or does it scope only the assumption surface and Zone 1D basis threads (with cross-examination mode deferred to M15)?

**Decision 6 — Landing orientation.** The bare landing state is a trust problem before model legibility issues apply. A first-time Demo 5 participant seeing a world map and "Gdp Usd Millions (USD_millions_cur▼)" as their introduction to WorldSim will be confused before reaching the instrument cluster. Does M14 scope include landing orientation, or is it deferred?

---

*This document is the evidence record for ADR-015. It is not summarized. The complete DIC consultations, live UI observations, gap taxonomy, and framework proposal are preserved in full as the basis for the architectural decision.*
