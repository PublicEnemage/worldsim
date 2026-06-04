# Findings — 2026-06-04-persona-2-003

**Session ID:** 2026-06-04-persona-2-003  
**Session valid:** YES — genuine cold-start, visual UI navigation (Interactive Playwright loop)  
**Persona:** Finance Ministry Negotiator — Eleni Papadopoulos (persona-2)  
**Use case:** IMF loan evaluation  
**Authors:** UX Designer Agent, PM Agent  
**Written:** 2026-06-04  

---

## Summary

A genuine cold-start Persona 2 session using the Interactive Playwright loop methodology (Option 2). The agent navigated the visual UI only — no API access, no WorldSim architecture context. The agent reached a [CONCLUDED:] marker but the conclusion was synthesized approximately 80% from historical domain knowledge of 2012 Greece and 20% from simulation output. Five usability findings identified, three of which are structural and require M12 action.

The primary usability gap: the TERMINAL alert is the tool's most prominent output but the most locked-down interaction point. The agent made four distinct click attempts on alert-related elements with zero navigation response. The task question ("which cohorts, at which steps") was not answerable from the UI alone.

---

## FINDING-2026-06-04-persona-2-003-01

**Severity:** CRITICAL  
**Dimension:** Action  
**Persona:** persona-2  
**Session:** 2026-06-04-persona-2-003  
**Component:** `zone-1b` (MDA alert panel)  
**Canonical use case:** IMF loan evaluation  

**Observation:** The TERMINAL alert panel is prominently displayed but entirely non-interactive. The agent made three distinct click attempts on alert-related text (Coverage, Financial, TERMINAL) — none produced any navigation response, expansion, additional detail, or visual feedback. The panel is a pure display element with no affordance distinguishing it from an interactive element.

**Evidence:**
- Think-aloud: `[EXPECTED: Clicking on the red alert box should expand it to show me exactly which cohorts are crossing thresholds at which simulation step.]` (~T+00:03) — expectation formed, never met
- Think-aloud: `[STRATEGY: Click on the red "TERMINAL" alert box to expand or navigate to detailed alert view showing which cohort and conditionality term drove the crossing.]` (~T+00:08)
- Actions attempted: click:Coverage → no change; click:Financial → no change; click:TERMINAL → no change
- Field notes: The agent continued attempting to expand the alert across multiple turns, demonstrating persistent user expectation that a prominent threshold alert would be interactive.

**Implication:** A finance ministry negotiator whose primary tool interaction is "find the threshold crossing" cannot proceed when the threshold crossing panel is a display wall. The alert announces a finding without providing a navigation path to the evidence behind it. In a time-critical negotiation context, a dead-end at the tool's primary output is equivalent to tool failure.

**M12 action:** The TERMINAL alert panel (zone-1b) must be interactive. Clicking on an alert should navigate to or expand a detail view showing: (a) the breached indicator's time-series across all steps, (b) the threshold value and the step-by-step approach to it, (c) which conditionality input is the primary driver (elasticity attribution). This is the core affordance gap blocking task completion.

---

## FINDING-2026-06-04-persona-2-003-02

**Severity:** HIGH  
**Dimension:** Comprehension  
**Persona:** persona-2  
**Session:** 2026-06-04-persona-2-003  
**Component:** `zone-1b` / alert text; `zone-1a` / trajectory-chart  
**Canonical use case:** IMF loan evaluation  

**Observation:** At 1440×900 viewport, alert text and trajectory chart labels are not legible. The agent misread "reserve coverage months" as potentially meaning data coverage completeness (not the reserve indicator). The agent misread the MDA identifier as "726MDA" and "156MMax" (actual: MDA-FIN-RESERVES). The trajectory chart's y-axis and step labels were read as approximations ("~0.00–0.30", "steps 1–12") without precision.

**Evidence:**
- Think-aloud: `[CONFUSED: The alert text seems to be about "coverage months" — unsure if this is a data gap warning or a genuine threshold crossing.]` (~T+00:03) — resolution took two additional turns
- Think-aloud: Alert text read as "Reserve coverage months crossed 726MDA, threshold at step 8" (session 002 developer audit confirmed actual text: `MDA-FIN-RESERVES`, `indicator_name: null`, floor value 750)
- Think-aloud: `[READING: Alert box — "TERMINAL" header in red. Text: "Reserve coverage months crossed [MDA threshold], threshold at step 8."]` — agent could not read the MDA identifier precisely (~T+00:12)
- Field notes: The agent spent approximately three turns (T+00:00 to T+00:08) in uncertainty about whether the alert was a threshold crossing or a data quality warning — entirely due to text illegibility.

**Implication:** When the user cannot read the alert that contains the primary finding, the tool's output is inaccessible. The alert text's ambiguity ("coverage months" as terminology) combined with small rendering size created a 3-turn resolution delay for the most prominent element on screen. In a 45-minute session limit, this is a significant friction cost.

**M12 action:** (a) Increase font size on alert panel — indicator name and threshold value must be legible at 1440×900 without zoom. (b) Add a human-readable label alongside the technical indicator key: "Reserve Coverage" rather than `reserve_coverage_months` or `MDA-FIN-RESERVES`. (c) Ensure `indicator_name` is never null in alert responses (confirmed gap in FINDING-2026-06-04-persona-2-002-06). (d) Add a brief disambiguation label distinguishing threshold-crossing alerts from data quality warnings — these are visually identical in the current rendering.

---

## FINDING-2026-06-04-persona-2-003-03

**Severity:** HIGH  
**Dimension:** Discovery  
**Persona:** persona-2  
**Session:** 2026-06-04-persona-2-003  
**Component:** `zone-2b` (cohort indicators); `zone-scenario-create` (conditionality instruments)  
**Canonical use case:** IMF loan evaluation  

**Observation:** No cohort-level disaggregation was discoverable from the main view. The agent's [CONCLUDED:] answer was synthesized from historical knowledge of 2012 Greek conditionality, not from simulation output. The task question ("which cohorts") was not answerable from what the tool displayed.

**Evidence:**
- Think-aloud: `[SYNTHESIZING — drawing on historical knowledge of 2012 Greek conditionality to interpret simulation output:]` (~T+00:17) — explicit statement that the conclusion draws on prior knowledge, not tool output
- Think-aloud: Cohort assignments (65+ cohort, youth cohort 18–25, children under 12) and step estimates (steps 3–5, steps 2–6, step 3) were not read from the tool — they were inferred from historical knowledge
- Field notes: Approximately 80% of the CONCLUDED content was historical synthesis; approximately 20% was derived from visible tool output (TERMINAL designation, step 8, four declining indices, values ~0.09–0.10)
- Replication of FINDING-2026-06-04-persona-2-002-02: This finding is confirmed by genuine UI navigation rather than API exploration

**Implication:** The task is not completable from the tool alone for a user without deep prior knowledge of the specific historical case. A finance ministry analyst who does not already know which conditionality terms affected which cohorts cannot learn this from the tool's current interface. This is the primary use-case failure: the tool is designed to give the finance minister information they don't already have, but in its current state it only confirms what they already know.

**M12 action:** Cohort-level indicator disaggregation must be visible from the main instrument cluster without requiring expansion or navigation. At minimum, the zone-2b indicator panel must show per-cohort values for: youth unemployment rate (15–24), elderly poverty headcount (65+), bottom-quintile income share, and health system utilization (as a proxy for healthcare access). These are the cohorts named in the Persona 2 task prompt and the minimum required for IMF loan evaluation to be a completable task.

---

## FINDING-2026-06-04-persona-2-003-04

**Severity:** MEDIUM  
**Dimension:** Discovery  
**Persona:** persona-2  
**Session:** 2026-06-04-persona-2-003  
**Component:** `zone-1c` (choropleth / map); `zone-header` (active scenario indicator)  
**Canonical use case:** IMF loan evaluation  

**Observation:** Greece is not visibly highlighted on the map despite the Greece scenario being loaded. The agent expressed uncertainty about whether the scenario was active across three consecutive turns (T+00:00, T+00:03, T+00:05), spending significant cognitive load on scenario load confirmation rather than scenario analysis.

**Evidence:**
- Think-aloud: `[EXPECTED: I would see Greece highlighted or selected, with the conditionality package scenario already loaded]` (~T+00:00) — expectation stated immediately
- Think-aloud: `[CONFUSED: Greece doesn't appear highlighted on the map. The instrument values suggest the scenario data may not be fully visible yet.]` (~T+00:03)
- Think-aloud: `[CONFUSED: Greece not visibly highlighted on map. Unclear if Greece scenario is loaded.]` (~T+00:05)
- Think-aloud: `[UNDERSTOOD: Scenario IS loaded. Step 8 is where a threshold crossing occurs.]` (~T+00:08) — only resolved after TERMINAL text was read, not from any visual map indicator

**Implication:** The first cognitive task of every session is "am I in the right scenario?" If this cannot be confirmed from the primary viewport in the first ten seconds, the user spends the next several minutes navigating uncertainty rather than the scenario itself. Map highlighting is the most natural confirmation signal — it is the visual affordance users expect.

**M12 action:** When a scenario is loaded for a specific country entity, that country must be visually highlighted (choropleth color change + border emphasis) on the map. The active scenario name must appear as a persistent label in the header or the instrument cluster — not buried in a URL parameter or a recording banner. The confirmation signal must be unambiguous from the first screenshot.

---

## FINDING-2026-06-04-persona-2-003-05

**Severity:** MEDIUM  
**Dimension:** Comprehension  
**Persona:** persona-2  
**Session:** 2026-06-04-persona-2-003  
**Component:** `zone-1d` (framework current position) / right panel  
**Canonical use case:** IMF loan evaluation  

**Observation:** The right-panel text "Primary dimension — see alerts" directed the agent toward the alert panel, but the alert panel had no interaction response. This text creates a navigation expectation ("see alerts" implies alerts are explorable) that the UI does not fulfill. The result is a misdirection: the text promises a navigation path that terminates at a display wall.

**Evidence:**
- Think-aloud: `[FOUND in right-side panel: Text "Primary dimension — see alerts" visible]` (~T+00:05)
- Think-aloud: `[STRATEGY: Click on the red "TERMINAL" alert box to expand or navigate to detailed alert view]` (~T+00:08) — the strategy was directly prompted by the "see alerts" text
- Actions: click:TERMINAL → no change — the strategy prompted by "see alerts" produced no result

**Implication:** "See alerts" is a navigation instruction without a navigation destination. In a high-stakes decision context, false navigation signals are worse than no signals: they consume user time and erode trust in the interface.

**M12 action:** Either (a) make the alert panel interactive (addresses FINDING-01 and removes the misdirection simultaneously), or (b) if alerts remain display-only, change "Primary dimension — see alerts" to text that describes the display rather than implying a navigation action — e.g., "Primary dimension: Financial (threshold breached — see panel above)."

---

## Positive Finding: TERMINAL Alert Visibility

The TERMINAL alert is immediately visible from the initial screenshot without any navigation. This is correct — the most urgent signal should be the first thing a user sees. The alert's persistence across turns confirms it is always-on, not hidden behind a click.

The "reserve coverage months" reading (even misread as "coverage") was correctly interpreted as a financial threshold by the agent without any system guidance. The TERMINAL designation conveyed severity appropriately. These are working affordances that M12 should preserve while adding interactivity.

---

## M11.5 Exit Criterion Assessment

> **Exit criterion:** Can a finance ministry analyst with no prior WorldSim orientation use this tool to produce a finding they could cite in a negotiation?

**Verdict: PARTIALLY MET**

| Component | Status |
|---|---|
| Agent navigated the tool cold (visual UI only) | ✓ |
| Agent produced a [CONCLUDED:] marker | ✓ |
| Agent could read the primary alert | ✓ (TERMINAL at step 8, after 3-turn delay) |
| Agent answered the primary task question from tool output | ✗ (answered from prior historical knowledge) |
| Agent found cohort-level threshold data | ✗ (not visible in the UI) |
| Agent could expand alerts for detail | ✗ (alert panel non-interactive) |
| Agent confirmed which scenario was active | ✗ (resolved indirectly, not from visual map) |

The agent completed the task in the narrow sense (reached CONCLUDED with a substantive answer). The tool did not complete the task — the agent's historical knowledge did. This distinction is the primary finding of session 003: the tool's output layer is insufficient for a cold-start user to answer the task question without prior domain expertise about the specific historical case.

The genuine M11.5 exit criterion requires the tool — not the user's prior knowledge — to be the primary source of the finding.
