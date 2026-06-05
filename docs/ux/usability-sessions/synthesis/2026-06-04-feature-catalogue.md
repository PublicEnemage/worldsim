# WorldSim Feature Catalogue — M11.5 Discoverability Assessment

**Document type:** Tertiary M11.5 deliverable (per North Star `docs/vision/milestone-11-5-north-star.md`)  
**Version:** 1.0 — 2026-06-04  
**Baseline:** v0.11.0 (git `b536421`)  
**Authors:** UX Designer Agent, PM Agent  
**Scope:** All capabilities present in the v0.11.0 UI, assessed against M11.5 Priority A session evidence  
**Inputs:** M11.5 Priority A session transcripts and findings; `docs/ux/usability-sessions/vocabulary.md`

---

## Purpose

The North Star defines the tertiary M11.5 deliverable as:

> "An updated feature catalogue — a complete inventory of what WorldSim can do, how each capability is accessed, which persona it serves, and whether the current UI makes that capability discoverable without assistance."

This document provides that inventory. Each entry states:
- **What it does** — the user-facing value of the capability
- **How it's accessed** — zone token(s), interaction cost (no click / one interaction / two or more / not UI-accessible)
- **Personas served** — from the canonical use case definitions in `docs/ux/personas.md`
- **Discoverability** — what the M11.5 sessions revealed; sources cited by session ID

**Discoverability scale:**

| Rating | Meaning |
|---|---|
| **ACCESSIBLE** | User located and correctly interpreted without guidance, confirmed by session evidence |
| **VISIBLE** | User located the element but could not correctly interpret it without additional context |
| **OBSCURED** | Element exists in the UI but was not found, or found after significant friction |
| **NOT ACCESSIBLE** | Capability exists in the engine/API but has no UI entry point in v0.11.0 |
| **NOT BUILT** | Capability is on the roadmap but not implemented in v0.11.0 |

---

## Section 1 — Always-Visible Instrument Cluster (Zone 1)

These capabilities are present in the primary viewport without any scroll or navigation action. They are the tool's primary output surface.

### 1.1 Trajectory Visualization

**What it does:** Displays the four composite framework indices (Financial, Human Development, Ecological, Governance) as time-series curves across all simulation steps, with a confidence interval band on each curve.

**Zone:** `zone-1a`  
**Interaction cost:** None — always visible  
**Personas served:** All five (P1–P5); primary instrument for every canonical use case

**Discoverability: VISIBLE**

All three Priority A personas immediately located the trajectory chart and read the directional trend (declining lines). None were able to use it for the precise analytical task their use case required:
- P2 (S003): Read "lines declining or flat at low levels" — directional signal captured, but step-level thresholds and cohort attribution not extractable from composites
- P1 (P1-001): Read four composite lines — confirmed tool did not surface the fiscal-multiplier-sensitive indicators (poverty headcount, health system capacity)
- P5 (P5-001): Read "financial and human development BOTH flat/declining" — formed the joint-design-failure reframe from this reading, but could not confirm whether the financial recovery arc was absent from the simulation or just not displayed

**Gap:** The chart shows what-direction-are-we-going but not why-are-we-going-there or who-bears-the-cost. Sub-indicator drill-in and cohort disaggregation are the missing capabilities.

**M12 action:** Click on a trajectory curve line to expand per-indicator detail for that framework. [GAP-04, GAP-10]

---

### 1.2 MDA Alert Panel

**What it does:** Displays threshold-crossing alerts for any Hard Minimum Descent Altitude breached during the simulation. Shows severity (TERMINAL/WARNING), the breached indicator, the step of crossing, and the threshold value.

**Zone:** `zone-1b`  
**Interaction cost:** None — always visible  
**Personas served:** P1 (Programme Analyst), P2 (Finance Ministry Negotiator), P5 (Executive Director); all three Priority A personas

**Discoverability: VISIBLE (visibility high; interactivity absent)**

The TERMINAL alert was the first element located by every Priority A persona. It successfully communicated severity and urgency. Its interactivity failure is the single highest-friction finding across Priority A sessions:
- P2 (S003): 3 click attempts on alert elements — Coverage, Financial, TERMINAL — zero response. Dead-end at the tool's most prominent output.
- P1 (P1-001): 1 click attempt on TERMINAL — confirmed non-interactive. Stated explicitly: "alert panel non-interactive."
- P5 (P5-001): Did not attempt to click — concluded before testing. Alert was read as a status indicator only.

The alert text legibility is a secondary issue: P2 misread `MDA-FIN-RESERVES` as "726MDA" and spent three turns disambiguating "coverage months" (threshold crossing? data gap warning?).

**Gap:** A non-interactive alert at the most prominent UI position trains users that the tool doesn't respond to interaction — suppressing all subsequent exploration.

**M12 action:** Alert panel becomes interactive. Click expands to indicator time-series, threshold approach curve, and causal attribution per conditionality term. Human-readable label alongside technical key. `indicator_name` never null. [GAP-01, GAP-05]

---

### 1.3 Policy Maneuver Margin (PMM) Widget

**What it does:** Displays a single scalar metric (0.00–1.00) representing the overall policy room remaining before irreversible threshold crossings. Shows direction trend (↑/↓/→). Displays "—" when all thresholds are breached.

**Zone:** `zone-1c`  
**Interaction cost:** None — always visible  
**Personas served:** P2 (Finance Ministry Negotiator), P5 (Executive Director) — quick-read policy space indicator

**Discoverability: NOT ASSESSED**

No Priority A persona explicitly interacted with or commented on the PMM widget in their think-aloud. P5 reported composite panel values (`Financial ~0.58, Human Development ~2.73`) which are `zone-1d` composites, not the PMM.

**Inference from sessions:** The PMM widget was either not noticed or not named. Its value (`—` when all thresholds breached, which is the state in the Greece fixture) may have blended visually into the composite score panel. A `—` state without explanation does not communicate "all thresholds breached" to a non-expert user.

**M12 action:** When PMM is `—`, display explanatory text inline: "All thresholds breached — policy room exhausted." This converts a cryptic null state into the most alarming finding the widget can display. [GAP-08 adjacent; see also Issue #673]

---

### 1.4 Four-Framework Current Position

**What it does:** Displays the composite score for each of the four frameworks (Financial, Human Development, Ecological, Governance) at the current simulation step. Provides a snapshot of the current state across all measurement dimensions.

**Zone:** `zone-1d`  
**Interaction cost:** None — always visible  
**Personas served:** All five; primary position-at-a-glance surface

**Discoverability: VISIBLE (located; not interpretable)**

The composite scores were read by P2 and P5:
- P2 (S003): Read Financial ~0.28 — could not determine whether this was a collapse reading or a moderate position without a scale reference
- P5 (P5-001): Read Financial ~0.58, Human Development ~2.73 — "unclear if high or low relative to baseline." Human Development ~2.73 is anomalous for a 0–1 normalized score; P5 could not determine if this represented the scale range or a data error

Neither the scale (0 = collapse, 1 = full capability) nor the direction of change (↑/↓ from previous step) is displayed. For a non-economist executive, an unlabelled composite score is not actionable.

**M12 action:** Each `zone-1d / framework-row` must display: current value, direction indicator (↑↓), scale tooltip ("0 = complete collapse, 1 = full capability"), and a plain-language label ("Deteriorating," "Stable," "Recovering") for non-economist users. [GAP-08]

---

### 1.5 Choropleth Map / Active Scenario Indicator

**What it does:** Displays a world choropleth coloured by a simulation attribute. In the M11.5 session configuration, used to provide geographic context for the loaded scenario country.

**Zone:** `zone-choropleth` / `zone-header`  
**Interaction cost:** None — always visible  
**Personas served:** All five — primary confirmation that the correct country/scenario is loaded

**Discoverability: NOT ACCESSIBLE (active scenario identity)**

This is the universal finding across all three Priority A sessions (GAP-02). No persona could confirm which scenario was loaded from the map or any other viewport element:
- P2 (S003): "Greece doesn't appear highlighted on the map" — 3 turns of uncertainty
- P1 (P1-001): "LOOKING FOR: what scenario is loaded, what country is selected" — never resolved across 5 turns
- P5 (P5-001): "CRITICAL GAP: Cannot confirm Greece is the selected entity" — explicitly named before concluding

The `zone-header / entity-selector` exists in the vocabulary but did not display a persistent, legible scenario identity label in any session. The choropleth map showed a blue gradient without a highlighted active entity.

**M12 action (blocking):** Persistent scenario identity header: `Scenario: Greece 2010–2015 / Entity: Greece / Status: Complete (6 steps)`. Active country highlighted on choropleth with border emphasis. Visible without scroll, present in any screenshot. [GAP-02]

---

## Section 2 — Zone 2 Capabilities (One Scroll or Click)

These capabilities require one additional navigation action to reach. They are not visible in the initial viewport.

### 2.1 Radar Chart

**What it does:** Multi-framework comparison in a radar/spider polygon. Provides a visual summary of the relative balance across all four framework scores at the current step.

**Zone:** `zone-2a`  
**Interaction cost:** One scroll  
**Personas served:** P5 (Executive Director) — executive comparison surface; P3 (Academic/NGO Researcher) — comparative analysis

**Discoverability: NOT ASSESSED**

No Priority A persona scrolled to Zone 2. P1 attempted `scroll_down:300` but did not observe or report Zone 2 content in their think-aloud. The radar chart was not a factor in any Priority A session outcome.

---

### 2.2 Framework Detail Panels (Per-Indicator Breakdown)

**What it does:** Per-framework expandable panels showing each individual indicator within the framework — name, current value, unit, confidence tier. This is where sub-composite indicator detail lives.

**Zone:** `zone-2b`  
**Interaction cost:** One scroll  
**Personas served:** P1 (Programme Analyst), P2 (Finance Ministry Negotiator) — indicator-level analysis

**Discoverability: NOT ACCESSIBLE (in practice)**

This is the architectural location of the per-indicator disaggregation that GAP-04 identifies as missing. The capability exists in Zone 2, but:
1. No Priority A persona reached Zone 2 during their task
2. The cohort-level indicators (youth unemployment, elderly poverty, health system capacity) are not confirmed to be present in `zone-2b` at the indicator-row level for the Greece fixture
3. Even if present in Zone 2, the North Star's commitment to "instruments always visible" (`docs/ux/information-hierarchy.md`) places disaggregated indicators in Zone 1 for the use cases that require them

**Gap:** Cohort disaggregation exists architecturally (zone-2b) but is not surfaced at the Zone 1 level where Priority A tasks require it. Zone 2 accessibility also depends on whether the indicators are populated in the fixture.

**M12 action:** Key cohort indicators (youth unemployment 15–24, elderly poverty 65+, bottom-quintile income share, health system utilisation) visible in Zone 1 without scroll for the IMF loan evaluation and Programme Analyst use cases. [GAP-04, GAP-07]

---

### 2.3 Methodology Notes

**What it does:** Disclosure panels explaining model limitations, synthetic data flags, and known gaps for the current scenario and step.

**Zone:** `zone-3a`  
**Interaction cost:** Two or more interactions  
**Personas served:** P1 (Programme Analyst), academic users — epistemic calibration; implements "blindspots are documented, not hidden" principle

**Discoverability: NOT ASSESSED**

No Priority A persona reached Zone 3. Methodology notes are a Zone 3 element and were not part of any Priority A session outcome. Their existence addresses the "No False Precision" and "Blindspots documented" principles; their inaccessibility to Priority A users means those principles are not being communicated to the users who most need epistemic calibration before citing a finding.

**M12 consideration:** The financial trajectory completeness gap (GAP-06) is precisely the type of limitation that `zone-3a / methodology-note` is designed to document. Until the mean-reversion arc is modelled (Issue #221), a methodology note stating "Financial stabilisation dynamics not yet modelled — trajectory does not show recovery arc" should be surfaced at Zone 1 level, not Zone 3 only.

---

## Section 3 — Scenario Management

### 3.1 Scenario Creation

**What it does:** Form to create a new simulation scenario — country selection, start year, step count, module toggles.

**Zone:** `zone-scenario-create`  
**Interaction cost:** One click from landing state  
**Personas served:** P1 (Programme Analyst), P2 (Finance Ministry Negotiator) — Mode 1 entry; P4/P6/P8 in their respective use cases

**Discoverability: PARTIALLY ACCESSIBLE**

P1 attempted `click:New Scenario` — this produced no visible change in the session. Whether the click reached the intended element or failed is unclear from the session record. P1 did not succeed in reaching the scenario creation form. This may be because the button was not visible at the scroll position, or because the interaction did not register.

**M12 action:** Ensure `zone-scenario-create` entry point is visible and accessible from the instrument cluster view (scenario already loaded), not only from the landing/list view.

---

### 3.2 Scenario Step Advancement

**What it does:** Advances the simulation one step. The primary action in Mode 2 (Simulation) — triggers engine computation for the next step and updates all Zone 1 instruments.

**Zone:** `zone-scenario-controls / advance-step-btn`  
**Interaction cost:** One click  
**Personas served:** P1 (Programme Analyst), P2 (Finance Ministry Negotiator) in Mode 2

**Discoverability: NOT ASSESSED (pre-advanced scenario)**

All M11.5 sessions used a pre-advanced Greece fixture (6 steps complete). No Priority A persona tested step advancement. This is a Mode 2 capability that was not the subject of any Priority A session task.

---

## Section 4 — Capabilities Without UI Entry Points (v0.11.0)

These capabilities exist in the engine or were specified for M12 but have no user-facing UI entry point in the current version. They are listed here so that the gap between engine capability and user-accessible capability is explicit.

### 4.1 Fiscal Multiplier Configuration

**What it does:** Sets the fiscal multiplier assumption (0.5 to 1.5+) that governs how fiscal policy changes propagate to output and employment. The core parameter for multiplier sensitivity analysis.

**Engine status:** Implemented in the simulation engine as a configurable parameter  
**UI entry point:** None in v0.11.0  
**Personas served (when built):** P1 (Programme Analyst) — primary task feature  
**Discoverability: NOT ACCESSIBLE**

P1's entire task (fiscal multiplier analysis: compare 0.5 vs 1.5) was blocked by the absence of this UI entry point. The task produced a NOT MET verdict. [GAP-03]

**M12 action (blocking for P1 use case):** Mode 2 configuration panel with fiscal multiplier input and side-by-side / overlay scenario comparison. [GAP-03]

---

### 4.2 Cohort-Level Indicator Disaggregation (Zone 1)

**What it does:** Displays per-cohort indicator values (youth unemployment 15–24, elderly poverty headcount 65+, bottom-quintile income share, health system utilisation) alongside the composite scores in Zone 1.

**Engine status:** Cohort-level indicators are in the simulation state; composite scores aggregate them  
**UI entry point:** Composites visible in Zone 1; per-indicator detail in Zone 2 (zone-2b) but not confirmed accessible for Priority A task cohorts  
**Personas served (when built):** P1, P2 — required for both programme analyst and finance ministry negotiator tasks  
**Discoverability: NOT ACCESSIBLE at Zone 1**

P2 and P1 both required cohort-level data and could not find it. P2 concluded with historical knowledge as substitute. P1 reached NOT MET. [GAP-04, GAP-07]

**M12 action (blocking for P1 and P2 use cases):** Key cohort indicators visible in Zone 1 for the IMF loan evaluation and programme analyst use cases. [GAP-04]

---

### 4.3 Counter-Scenario Creation (Duplicate and Modify)

**What it does:** Creates an alternate scenario from an existing one, changing one or more parameters to enable direct comparison.

**Engine status:** POST /scenarios/restore endpoint implemented (M11 G20); scenario-from-tombstone reconstruction available  
**UI entry point:** None — API only  
**Personas served (when built):** P1, P2  
**Discoverability: NOT ACCESSIBLE**

Developer audit session (2026-06-04-persona-2-002) confirmed this is API-only. No UI path exists.

---

### 4.4 Political Economy Module Parameters

**What it does:** Configures conditionality structured inputs, implementation capacity, legitimacy dynamics, and elite capture coefficient — the political economy layer of the simulation.

**Engine status:** Implemented (M11 G16a/G16b, PRs #704/#705)  
**UI entry point:** None — engine only  
**Personas served (when built):** P2 (Finance Ministry Negotiator) — conditionality feasibility; P3 (Academic Researcher) — distributional analysis  
**Discoverability: NOT ACCESSIBLE**

---

### 4.5 Mode 3 — Active Control

**What it does:** Real-time policy steering within human cost constraints. The north star interaction mode.

**Engine status:** Engine supports step advancement; Mode 3 control plane not built  
**UI entry point:** Not built — `zone-control-plane` reserved in layout  
**Personas served (when built):** All — primary interaction mode for M12+  
**Discoverability: NOT BUILT**

---

## Section 5 — Summary Discoverability Matrix

| Capability | Zone | Interaction cost | Discoverability | Blocking use case |
|---|---|---|---|---|
| Trajectory visualization | `zone-1a` | None | VISIBLE | — |
| MDA Alert Panel (display) | `zone-1b` | None | VISIBLE | — |
| MDA Alert Panel (interactive) | `zone-1b` | None | NOT ACCESSIBLE | P1, P2 |
| PMM Widget | `zone-1c` | None | NOT ASSESSED | — |
| Four-Framework Current Position | `zone-1d` | None | VISIBLE (not interpretable) | P5 |
| Active scenario identity | `zone-header` / `zone-choropleth` | None | NOT ACCESSIBLE | **All (universal)** |
| Radar Chart | `zone-2a` | One scroll | NOT ASSESSED | — |
| Framework Detail Panels | `zone-2b` | One scroll | NOT ACCESSIBLE (in practice) | P1, P2 |
| Methodology Notes | `zone-3a` | 2+ interactions | NOT ASSESSED | — |
| Scenario creation | `zone-scenario-create` | One click | PARTIALLY ACCESSIBLE | P1 |
| Fiscal multiplier configuration | — | — | NOT ACCESSIBLE | **P1 (blocks task)** |
| Cohort disaggregation (Zone 1) | — | — | NOT ACCESSIBLE | **P1, P2 (blocks task)** |
| Counter-scenario creation | — | — | NOT ACCESSIBLE | P1, P2 |
| Political economy parameters | — | — | NOT ACCESSIBLE | P2, P3 |
| Mode 3 Active Control | — | — | NOT BUILT | All |

**Accessible without assistance (M11.5 session evidence):** 0 of the above at the task-completion level. Directional information is accessible; analytical depth is not.

---

## Section 6 — Per-Persona Discoverability Summary

| Persona | Canonical use case | Can they complete their task today? | Primary blocker |
|---|---|---|---|
| P1 — Programme Analyst | Fiscal multiplier analysis | NO | Fiscal multiplier parameter absent (GAP-03) |
| P2 — Finance Ministry Negotiator | IMF loan evaluation | PARTIALLY | Alert non-interactive + no cohort disaggregation (GAP-01, GAP-04) |
| P3 — Academic/NGO Researcher | Policy scenario exploration | NOT TESTED | Likely: no cohort disaggregation, no counter-scenario UI |
| P4 — Civil Society Advocate | Human impact documentation | NOT TESTED | Likely: composite scores uninterpretable, no cohort data |
| P5 — Executive Director, IMF | Executive board briefing | PARTIALLY | Scenario identity unconfirmed + financial trajectory possibly incomplete (GAP-02, GAP-06) |
| P6 — Civic Researcher | Civil society campaigning | NOT TESTED | Deferred — Priority B |
| P8 — Community Leader | Community organising | NOT TESTED | Deferred — Priority B |

---

## Document Links

| Document | Path |
|---|---|
| Priority A synthesis | `docs/ux/usability-sessions/synthesis/2026-06-04-priority-a-synthesis.md` |
| Semantic vocabulary | `docs/ux/usability-sessions/vocabulary.md` |
| Module capability registry | `docs/scenarios/module-capability-registry.md` |
| M11.5 North Star | `docs/vision/milestone-11-5-north-star.md` |
| M11.5 Exit Checklist | Issue #720 |
