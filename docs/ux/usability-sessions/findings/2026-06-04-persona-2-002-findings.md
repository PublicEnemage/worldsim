# Findings — 2026-06-04-persona-2-002

**Session ID:** 2026-06-04-persona-2-002  
**Session valid:** YES  
**Persona:** Finance Ministry Negotiator — Eleni Papadopoulos (persona-2)  
**Use case:** IMF loan evaluation  
**Authors:** UX Designer Agent, PM Agent  
**Written:** 2026-06-04  

---

## Summary

The primary M11.5 exit criterion — "Can a finance ministry analyst with no prior WorldSim orientation use this tool to produce a finding they could cite in a negotiation?" — is **partially met**. The agent produced one citable finding (reserve coverage breach pre-conditionality; TERMINAL by 2012). The primary task — identifying human cost threshold crossings by conditionality term — **could not be completed**. Six findings documented below.

---

## FINDING-2026-06-04-persona-2-002-01

**Severity:** CRITICAL  
**Dimension:** Action  
**Persona:** persona-2  
**Session:** 2026-06-04-persona-2-002  
**Component:** `zone-1b` (human development framework alerts — absent)  
**Canonical use case:** IMF loan evaluation  

**Observation:** Human development indicators (unemployment_rate, net_enrollment_secondary, health_expenditure_pct_gdp) are frozen at their 2010 initial values across all six simulated years; no human development MDA alerts fire; the human cost ledger produces no output.

**Evidence:**
- Think-aloud: `[CONFUSED: the human_development composite score is exactly 0.8014 at every single step — from baseline through capital controls. This cannot be a correct representation of Greece's human development reality. Unemployment rose from 12.7% in 2010 to over 27% by 2013.]` (~T+03:00)
- Think-aloud: `[FOUND: there are zero MDA alerts in the human_development framework across all seven steps. The human development indicators do not move. Threshold crossing analysis for human cost is not possible because the human cost model is not responding to the policy inputs.]` (~T+04:30)
- Field notes: Agent identified the freeze within ~3 minutes of first API exploration. Confirmed by reading all seven steps of measurement-output.

**Implication:** A finance ministry negotiator whose primary task is to identify human cost threshold crossings — which is the tool's stated primary purpose — cannot do so. The human cost ledger is architecturally present (zone-1b renders, framework label "Human Development" appears in Zone 1D) but produces no live output. The presence of the framework structure without functioning indicators is misleading: it looks like the tool ran and answered the question when the answer is that no output was computed.

**M12 action:** The human development module must respond to fiscal spending changes with updates to unemployment, health expenditure, and enrollment indicators. At minimum, a spending_change input should propagate into unemployment_rate via a labor market elasticity. The `MacroeconomicModule` or a dedicated `HumanDevelopmentModule` must implement this linkage. MDA floors for unemployment (e.g., floor at 20% → WARNING; 25% → CRITICAL) and health expenditure (e.g., floor at 8% → WARNING) must fire when thresholds are breached.

---

## FINDING-2026-06-04-persona-2-002-02

**Severity:** CRITICAL  
**Dimension:** Discovery  
**Persona:** persona-2  
**Session:** 2026-06-04-persona-2-002  
**Component:** `zone-2b` (indicator-level data — cohort disaggregation absent)  
**Canonical use case:** IMF loan evaluation  

**Observation:** No cohort-level disaggregation exists anywhere in the tool's output — minimum wage workers, pensioners, and youth are not tracked as distinct cohorts; only population-level aggregates are available.

**Evidence:**
- Think-aloud: `[FOUND: no cohort-level disaggregation exists in the API output for this scenario. The indicators tracked are population-level aggregates. There is no youth unemployment rate, no pensioner poverty rate, no low-wage worker income indicator, no Gini coefficient, no poverty headcount. The cohorts most affected by the conditionality package — workers at minimum wage, pensioners, the youth — are invisible to the measurement framework as currently implemented.]` (~T+05:00)
- Think-aloud: `[CONCLUDED: (B) Cohort-level disaggregation does not exist. The conditionality terms most dangerous to vulnerable populations — minimum wage workers, pensioners, youth jobseekers — are not tracked as distinct cohorts.]`
- Field notes: Agent explicitly noted this as the second part of their four-part CONCLUDED verdict.

**Implication:** The core promise of WorldSim's mission — identifying which specific cohorts bear the cost of structural adjustment — cannot be delivered. A finance ministry negotiator cannot say "the minimum wage cut crosses a threshold for workers in the bottom quintile at step 2" because the bottom quintile does not exist as a measurement unit. This is a structural gap in the simulation framework's output layer, not a UI problem.

**M12 action:** Introduce at minimum: youth unemployment rate (15–24), pensioner poverty headcount, informal sector employment share, and bottom-quintile income share as distinct indicators in the human development and financial frameworks. These are the cohorts named in the Persona 2 task prompt and are necessary for the IMF loan evaluation use case to be completable.

---

## FINDING-2026-06-04-persona-2-002-03

**Severity:** HIGH  
**Dimension:** Comprehension  
**Persona:** persona-2  
**Session:** 2026-06-04-persona-2-002  
**Component:** `zone-1a / trajectory-chart` (composite score display) and `zone-2b / indicator-row / value`  
**Canonical use case:** IMF loan evaluation  

**Observation:** The `/trajectory` endpoint returns composite scores (financial: 0.2271, human_development: 0.8014) while the `/measurement-output` endpoint states "Composite score not meaningful in single-entity scenarios — percentile rank requires at least two entities for comparison." The agent explicitly stated they could not determine which to trust.

**Evidence:**
- Think-aloud: `[FOUND — TRAJECTORY NOTE: the financial composite score in the trajectory endpoint shows 0.2271→0.2329→0.0833 and then flatlines at 0.0833. But the measurement-output endpoint returns null for composite scores in all steps, with the note: "Composite score not meaningful in single-entity scenarios." This discrepancy... is a UX inconsistency I cannot resolve as a user. I don't know which number to trust.]` (~T+04:00)
- Usability observation: "Composite score discrepancy between /trajectory and /measurement-output is disorienting."

**Implication:** A user who sees composite scores in the trajectory view (Zone 1A) and then opens the measurement-output (Zone 2B) will encounter contradictory signals about the validity of the numbers they are relying on. In a negotiation context, citing a number that the tool itself says is "not meaningful" is worse than citing no number at all.

**M12 action:** Either (a) remove composite scores from the `/trajectory` response for single-entity scenarios and show a "requires multiple entities" placeholder in Zone 1A, or (b) surface the "not meaningful in single-entity scenarios" caveat prominently in Zone 1A's legend or tooltip, not buried in a measurement-output API field. The current state — displaying the number prominently in the chart while simultaneously flagging it as meaningless in a secondary API response — is the worst possible UX: false confidence.

---

## FINDING-2026-06-04-persona-2-002-04

**Severity:** HIGH  
**Dimension:** Action  
**Persona:** persona-2  
**Session:** 2026-06-04-persona-2-002  
**Component:** `zone-scenario-create / module-toggle` (conditionality instrument granularity)  
**Canonical use case:** IMF loan evaluation  

**Observation:** All conditionality terms (minimum wage cut, pension reductions, privatisation schedule) are aggregated into a single `spending_change` instrument; the agent could not isolate individual terms to test a counter-proposal.

**Evidence:**
- Think-aloud: `[CONFUSED: the scenario encodes these as aggregate fiscal spending changes (step 1: -8%, step 2: -5%, etc.) and structural inputs (privatisation at step 5). There is no separate minimum-wage instrument or pension-cut instrument in the scheduled inputs. This matters for my counter-proposal work: I cannot currently ask the tool "what happens if the minimum wage cut is 12% instead of 22%?" — the wage cut is folded into the spending_change aggregate.]` (~T+02:00)
- Think-aloud: `[CONCLUDED: (C) There is no way to isolate individual conditionality terms (minimum wage cut vs. pension cut vs. privatisation timing) in separate scenario runs because these instruments are aggregated into spending_change.]`

**Implication:** The counter-proposal task — "what is the minimum modification that avoids the threshold crossings?" — requires the ability to test individual conditionality terms in isolation. Without instrument-level granularity, the tool can model the aggregate effect of austerity but cannot support the specific negotiating task of trading one conditionality for another. This is a significant constraint on the IMF loan evaluation use case.

**M12 action:** Add named conditionality instruments to the scheduled_inputs schema: `minimum_wage_change_pct`, `pension_replacement_rate_change_pct`, `health_spending_change_pct_gdp`, `privatisation_schedule` (phased vs. immediate). These must propagate into the human development and financial indicator layers with documented elasticities. A finance ministry needs to test "accept pensions cut, reject wage cut" as a distinct scenario.

---

## FINDING-2026-06-04-persona-2-002-05

**Severity:** MEDIUM  
**Dimension:** Discovery  
**Persona:** persona-2  
**Session:** 2026-06-04-persona-2-002  
**Component:** `zone-scenario-create` (counter-scenario creation path)  
**Canonical use case:** IMF loan evaluation  

**Observation:** No counter-scenario creation capability is discoverable from the interface or API without developer-level knowledge of the request schema.

**Evidence:**
- Think-aloud: `[FOUND: POST /api/v1/scenarios/{scenario_id}/advance and POST /api/v1/scenarios exist. However, I cannot construct a counter-scenario without knowing what input format would encode a 12% minimum wage cut specifically — the existing scenario only uses spending_change as an aggregate instrument. There is no "minimum_wage_change" instrument visible in the scheduled_inputs or the OpenAPI schema I examined. I cannot surgically test the minimum wage term in isolation.]` (~T+05:30)
- Usability observation: "No counter-scenario capability is discoverable from the interface or API documentation without developer knowledge."

**Implication:** The comparative scenario analysis that is central to negotiation preparation (base case vs. modified conditionality) requires the user to know the POST request schema for creating a scenario with specific policy inputs. This knowledge is not available from the UI or from the OpenAPI spec alone. The tool's core Mode 2 (Simulation) workflow is invisible to a non-developer first-time user.

**M12 action:** Add a "Duplicate and modify" action to the scenario card in zone-scenario-list. The UI should allow a user to clone a scenario and edit its scheduled_inputs through a form interface — not require them to know the JSON schema. This is the entry point for counter-scenario analysis, which is Mode 2's primary cognitive task per the UX architectural commitments.

---

## FINDING-2026-06-04-persona-2-002-06

**Severity:** MEDIUM  
**Dimension:** Comprehension  
**Persona:** persona-2  
**Session:** 2026-06-04-persona-2-002  
**Component:** `zone-1b / alert-row / indicator-name` (MDA alert indicator display)  
**Canonical use case:** IMF loan evaluation  

**Observation:** The MDA-FIN-RESERVES alert correctly identifies a pre-conditionality TERMINAL breach; however, the `indicator_name` field in the alert is `null` in the API response, meaning the alert's human-readable label for the breached indicator is missing.

**Evidence:**
- API response: `{"mda_id": "MDA-FIN-RESERVES", "indicator_key": "reserve_coverage_months", "indicator_name": null, ...}`
- Field notes: The session runner screenshot shows the alert rendered in Zone 1B as "TERMINAL — reserve coverage months crossed 750M/Mar, threshold at step 8" — suggesting the frontend is rendering from `indicator_key` fallback rather than `indicator_name`.
- Note: The agent was able to read the alert correctly via API (`indicator_key` and `floor_value` were present), but the null `indicator_name` would be confusing if surfaced in the UI without fallback handling.

**Implication:** If the frontend renders `null` as "null" instead of falling back to a human-readable form of `indicator_key`, users will see "null crossed threshold" in the MDA alert panel. The backend should populate `indicator_name` from the MDA threshold registry.

**M12 action:** Populate `indicator_name` in the MDA alert response from the registered threshold's display label (e.g., "Reserve Coverage" for MDA-FIN-RESERVES). Add a backend test asserting `indicator_name` is never null in a valid alert. Add a frontend fallback that converts `indicator_key` to title case if `indicator_name` is null.

---

## Positive Finding: MDA Alert System

The MDA-FIN-RESERVES alert system worked correctly and produced the session's only citable finding:

- Alert escalation (WARNING → CRITICAL → TERMINAL over consecutive breach steps) is correctly calibrated
- The pre-conditionality nature of the breach was discoverable and analytically potent: Greece entered the IMF program already below the reserve coverage floor
- The severity ladder (CRITICAL at step 1, TERMINAL from step 2 onward) provides the temporal precision a negotiator needs: "by the time the Second Memorandum was signed, we were already in TERMINAL territory on reserves"

This finding could be cited in a negotiation. It is the proof of concept for the MDA alert architecture. The M12 priority is extending this same architecture to the human development framework.

---

## M11.5 Exit Criterion Assessment

> **Exit criterion:** Can a finance ministry analyst with no prior WorldSim orientation use this tool to produce a finding they could cite in a negotiation?

**Verdict: PARTIALLY MET**

| Component | Status |
|---|---|
| Agent navigated the tool cold | ✓ |
| Agent produced at least one citable finding | ✓ (MDA-FIN-RESERVES pre-conditionality breach, TERMINAL at step 2) |
| Agent answered the primary task question | ✗ (human cost threshold crossings not computable — FINDING-01 and FINDING-02) |
| Agent could test a counter-proposal | ✗ (instrument granularity insufficient — FINDING-04) |

The tool serves as a financial stress signal system (reserve coverage, GDP trajectory) but does not yet function as a human cost threshold tool. The primary use case for Persona 2 — building a counter-proposal that protects vulnerable cohorts — requires FINDING-01 and FINDING-02 to be closed before the exit criterion can be fully met.
