# M11.5 Priority A Sessions — Findings Synthesis

**Document type:** Cross-session synthesis  
**Sessions covered:** 2026-06-04-persona-2-003, 2026-06-04-persona-1-001, 2026-06-04-persona-5-001  
**Authors:** UX Designer Agent, PM Agent  
**Written:** 2026-06-04  
**Milestone:** M11.5 — Usability Validation and Experience Audit  
**Inputs to:** Issue #720 (M11.5 Exit Checklist)

---

## Purpose

This document consolidates findings from all three M11.5 Priority A cold-start usability sessions into a ranked, actionable record. Its purpose is threefold:

1. Identify which findings are structural (appear across multiple personas and use cases) vs. use-case-specific
2. Produce a ranked M12 action table with blocking/non-blocking classification
3. Deliver the formal M11.5 exit criterion verdict with session-level evidence

This is the primary input to Issue #720 (M11.5 Exit Checklist). The session-level documents (transcripts, findings, manifests) are the evidentiary record; this document is the synthesis.

---

## Sessions at a Glance

| Session | Persona | Use case | Valid | Actions | Verdict |
|---|---|---|---|---|---|
| 2026-06-04-persona-2-003 | Finance Ministry Negotiator (P2) | IMF loan evaluation | YES | 5 (0 responses) | PARTIALLY MET |
| 2026-06-04-persona-1-001 | Programme Analyst — Lucas Ferreira (P1) | Fiscal multiplier analysis | YES | 5 (0 responses) | NOT MET |
| 2026-06-04-persona-5-001 | Executive Director, IMF (P5) | Executive board briefing | YES | 3 (0 responses) | PARTIALLY MET |

**A signal present in all three sessions before the first finding:** across 13 combined navigation actions, zero produced a visible UI state change. Every click, scroll, and navigation attempt returned the tool to its initial state. This is not a finding cluster — it is an architectural signal: the tool's current interaction model is display-only. Users can read; they cannot navigate.

---

## Exit Criterion Verdict

> **M11.5 exit criterion:** Can a finance ministry analyst with no prior WorldSim orientation use this tool to produce a finding they could cite in a negotiation?

### Aggregate verdict: NOT READY — EVIDENCE COMPLETE

| Session | Criterion met? | Primary basis for answer |
|---|---|---|
| P2-003 (Finance Ministry Negotiator) | PARTIALLY | ~80% historical domain knowledge; ~20% tool output |
| P1-001 (Programme Analyst) | NOT MET | Primary task feature absent from UI |
| P5-001 (Executive Director) | PARTIALLY | Directional reading of chart; scenario identity and trajectory accuracy unverifiable |

**No session met the criterion from tool output alone.** In two sessions (P2, P5) the agent reached a `[CONCLUDED:]` answer — but the conclusion rested on domain knowledge and directional inference, not tool-provided evidence. In one session (P1) the tool was missing the primary feature the task required.

The audit is evidence-complete: it has produced the findings it was designed to produce. The tool is not ready for Priority A use cases in its current state. M11.5 closes as an audit milestone, not as a readiness certification.

---

## Finding Inventory — All Priority A Sessions

All 13 findings from valid Priority A sessions, de-duplicated and cross-referenced.

| Finding ID | Severity | Dimension | Component | Sessions | Pattern |
|---|---|---|---|---|---|
| GAP-01 | CRITICAL | Action | `zone-1b` alert panel — non-interactive | P2-003, P1-001 | Cross-session (2 of 3) |
| GAP-02 | CRITICAL | Discovery | Active scenario not identifiable from main viewport | P2-003, P1-001, P5-001 | **Universal (3 of 3)** |
| GAP-03 | CRITICAL | Action | Fiscal multiplier parameter absent — no Mode 2 configuration UI | P1-001 | Session-specific (P1) |
| GAP-04 | HIGH | Discovery | Cohort/indicator disaggregation not visible — composite scores only | P2-003, P1-001 | Cross-session (2 of 3) |
| GAP-05 | HIGH | Comprehension | Alert text + trajectory chart illegible at 1440×900 | P2-003 | Session-specific (P2) |
| GAP-06 | HIGH | Comprehension | Financial trajectory completeness — recovery arc absent from chart | P5-001 | Session-specific (P5) |
| GAP-07 | HIGH | Discovery | Poverty headcount and health system capacity not surfaced as named indicators | P1-001 | Session-specific (P1) |
| GAP-08 | MEDIUM | Comprehension | Composite score interpretability — no scale, no baseline, no direction indicator | P5-001 | Session-specific (P5) |
| GAP-09 | MEDIUM | Comprehension | "Primary dimension — see alerts" misdirects to non-interactive panel | P2-003 | Session-specific (P2) |
| GAP-10 | MEDIUM | Action | Zone-1a and zone-1d redundant — both show composites; no sub-indicator drill-in | P1-001 | Session-specific (P1) |
| GAP-11 | MEDIUM | Discovery | Greece not highlighted on map despite scenario loaded | P2-003 | Component of GAP-02 |

Note: GAP-11 is the map-highlighting dimension of GAP-02 (active scenario identity). They share an M12 action.

---

## Cross-Session Pattern Analysis

### Pattern 1 — Universal: Active scenario not identifiable (GAP-02)

Every Priority A persona, regardless of expertise level or task complexity, named scenario identity uncertainty at session start. The severity escalates with the stakes of the task:

| Session | Persona type | Language used | Severity |
|---|---|---|---|
| P2-003 | Policy expert | "Greece doesn't appear highlighted on the map" — 3 turns of uncertainty | MEDIUM |
| P1-001 | Domain expert | "LOOKING FOR: what scenario is loaded, what country is selected" — never resolved | HIGH |
| P5-001 | Non-economist exec | "CRITICAL GAP: Need to confirm which entity is active before answering the Board" | CRITICAL |

**Why this pattern matters:** Scenario identity is not orientation overhead — it is the claim being made. A Board member citing a finding from this tool is asserting "this is data for Greece." If they cannot confirm that claim from the UI, the citation is unverifiable. The severity escalation is not because the UI changed between sessions; it is because higher-stakes users have lower tolerance for unconfirmed claims.

**The fix is a single named element.** A persistent header stating `Scenario: Greece 2010–2015 / Entity: Greece / Status: Complete (6 steps)` resolves this gap for all three personas. No architecture change required — this is a display commitment.

### Pattern 2 — Majority: Alert panel non-interactive (GAP-01)

Two of three Priority A personas explicitly attempted to interact with the TERMINAL alert panel and received zero response. Persona 5 did not attempt it because they concluded before testing the alert; the gap was not absent, it was pre-empted.

| Session | Clicks attempted on alert | Response | Consequence |
|---|---|---|---|
| P2-003 | 3 (Coverage, Financial, TERMINAL) | None | Dead-end at primary output; concluded from historical knowledge |
| P1-001 | 1 (TERMINAL) | None | Confirmed tool non-responsive; primary task feature search abandoned |
| P5-001 | 0 (concluded before testing) | N/A | — |

The TERMINAL alert is the most prominent element in the UI. It is the first thing users read and the element most likely to drive a navigation action. A prominently displayed element that does not respond to user interaction is an anti-affordance: it trains users that the tool does not respond to interaction, which suppresses further exploration.

**The fix requires a design decision:** either (a) alert panel becomes interactive — click expands to indicator time-series, threshold approach curve, and driver attribution — or (b) the alert panel's visual weight is reduced so it reads as a status indicator rather than a call-to-action. Option (a) is the architecturally correct path. Option (b) is a workaround that reduces the information architecture.

### Pattern 3 — Majority: No cohort disaggregation (GAP-04)

Both task-oriented personas (P2 Finance Ministry Negotiator, P1 Programme Analyst) found that the primary question their task required — which cohorts are affected, by how much, at which steps — was unanswerable from the visible UI.

| Session | Task question | Tool's answer | User's workaround |
|---|---|---|---|
| P2-003 | "Which cohorts are crossing thresholds?" | Composite scores only | Historical synthesis (2012 Greece conditionality) |
| P1-001 | "What is the poverty headcount at multiplier 0.5 vs 1.5?" | Composite scores only | Concluded NOT MET; no workaround available |

Persona 5 (Executive Director) did not need cohort disaggregation — their task required a directional verdict, not distributional detail. This is consistent with the persona hierarchy: the non-economist executive needs "up or down," the analyst needs "which cohort, how much, when."

**The implication:** the current instrument cluster is designed for directional reading, not analytical depth. It serves the executive use case partially while failing the analyst use case completely. M12 instrument design must serve both levels simultaneously — composites for orientation, disaggregates for analysis — without requiring the analyst to navigate to a separate view.

---

## Ranked M12 Action Table

Actions are ranked by: (1) cross-session pattern breadth, (2) severity, (3) use-case blocking status.

| Rank | Gap | Severity | Sessions | Blocking | M12 Action |
|---|---|---|---|---|---|
| 1 | GAP-02: Active scenario not identifiable | CRITICAL | All 3 | YES — blocks all Priority A use cases | Persistent header element: scenario name, entity, status. Country highlighted on choropleth when loaded. Visible in any screenshot. |
| 2 | GAP-01: Alert panel non-interactive | CRITICAL | 2 of 3 | YES — blocks IMF loan evaluation and programme analyst use cases | Click on alert expands to: indicator time-series, threshold approach curve, driver attribution per conditionality term. |
| 3 | GAP-03: Fiscal multiplier parameter absent | CRITICAL | P1 only | YES — blocks programme analyst use case entirely | Mode 2 scenario configuration panel: fiscal multiplier input (0.5–2.0 range), side-by-side or overlay comparison mode. |
| 4 | GAP-04: No cohort disaggregation | HIGH | 2 of 3 | YES — blocks IMF loan evaluation and programme analyst use cases | Zone-2b (or equivalent) shows per-cohort indicators without navigation: youth unemployment (15–24), elderly poverty headcount (65+), bottom-quintile income share, health system utilisation. |
| 5 | GAP-06: Financial trajectory completeness | HIGH | P5 only | YES — for executive board briefing: incomplete trajectory produces wrong conclusion | Trajectory must display full arc across all modelled steps. If recovery dynamics are not modelled, display must state "financial stabilisation dynamics not yet modelled" (blindspots-are-documented principle). Links to Issue #221. |
| 6 | GAP-05: Alert text illegible at 1440×900 | HIGH | P2 only | PARTIAL — 3-turn disambiguation cost; not a hard block | Increase alert font size. Human-readable label alongside technical key. `indicator_name` never null (confirms FINDING-2026-06-04-persona-2-002-06). Threshold-crossing vs. data-quality visual distinction. |
| 7 | GAP-07: Named indicators absent | HIGH | P1 only | PARTIAL — absence confirmed NOT MET; named indicators are prerequisite for drill-in | Poverty headcount and health system capacity must be named, disaggregated output indicators accessible from the main view. |
| 8 | GAP-08: Composite score interpretability | MEDIUM | P5 only | PARTIAL — executive user cannot interpret whether scores are good or bad | Each zone-1d composite: current value + direction indicator (↑↓) + scale tooltip (0 = collapse, 1 = full capability). Plain-language label for non-economist users. |
| 9 | GAP-09: "See alerts" misdirection | MEDIUM | P2 only | Resolved by Rank 2 action; independent fix only if alert remains display-only | If alert panel stays display-only: replace "see alerts" with descriptive text ("Financial — threshold breached"). If alert becomes interactive: resolved automatically. |
| 10 | GAP-10: Zone redundancy | MEDIUM | P1 only | LOW — no new information lost, but increases cognitive load | Zone-1a trajectory view should support click-on-line to expand sub-indicator. Zone-1d composites should link to per-indicator breakdown. Reduces redundancy by adding depth. |

**Minimum viable M12 scope for Priority A use case readiness:** Ranks 1–4. These four actions address the universal finding plus the cross-session majority findings. Ranks 5–10 address severity and usability but do not add use cases to the tool's claim.

---

## What the Sessions Reveal About the Architecture

Beyond individual findings, the three sessions collectively reveal a structural gap between the tool's current architecture and its stated use cases.

**The instrument cluster is a status board, not an analytical tool.**  
The current Zone 1 layout shows four composite framework indices and an alert panel. This is appropriate for situational awareness — knowing whether the simulation has produced a crisis. It is insufficient for the analytical task: understanding why the crisis occurred, which intervention would have prevented it, and which cohorts bore the cost. Status boards are the entry point; the analytical layer is what allows a user to form a citable finding.

**The human cost ledger is not accessible at the task level.**  
CLAUDE.md's first principle: "The human cost ledger is primary." In all three sessions, the human cost ledger was inaccessible as a primary output. Persona 2 could not identify which cohorts crossed thresholds. Persona 1 could not find poverty headcount. Persona 5 could not confirm whether the Human Development composite of 2.73 represented improvement or deterioration. The commitment is architectural; the current implementation does not fulfil it at the use-case level.

**Mode 2 (Simulation) does not yet exist as a user-facing capability.**  
Persona 1's task required Mode 2: configure a parameter, run the simulation, observe the output. This is the tool's core differentiating capability — the thing that makes it a flight simulator rather than a history book. Mode 2 is not accessible from the current UI. Until it is, the programme analyst use case — arguably the most important use case for the tool's mission — cannot be served.

**The zero-response rate is diagnostic.**  
13 actions across three sessions, zero UI state changes (excluding `done`). This is not a coincidence of actions chosen. Every user tried clicking the most prominent elements (the TERMINAL alert, the trajectory legend, the map, named text). Every click went unregistered. The tool's interaction model currently offers one affordance: read. The mission requires another: explore.

---

## Priority B Sessions — Recommendation

M11.5 Priority A sessions are complete. Priority B sessions (Persona 6 — Civic Researcher, Persona 8 — Community Leader) are specified in `pillar-2-methodology.md §Persona Sequencing`.

**Recommendation: defer Priority B sessions until Ranks 1–4 M12 actions are implemented.**

Rationale: Priority B personas are less technically expert than P1–P5. Running them against the current interface would produce findings that are dominated by the same structural gaps (scenario identity, alert non-interactivity, no disaggregation) already confirmed across three Priority A sessions. The marginal finding value of Priority B sessions is low until the Priority A gaps are addressed. Running them post-M12 would produce the incremental findings the methodology is designed to surface — persona-specific comprehension and discovery gaps that emerge after the structural interaction model is working.

If EL chooses to run Priority B sessions in the current state, those sessions should be scoped explicitly as gap-replication exercises, not as independent assessments of new use cases.

---

## Document Links

| Document | Path |
|---|---|
| P2-003 transcript | `docs/ux/usability-sessions/transcripts/2026-06-04-persona-2-003-transcript.md` |
| P2-003 findings | `docs/ux/usability-sessions/findings/2026-06-04-persona-2-003-findings.md` |
| P2-003 manifest | `docs/ux/usability-sessions/manifests/2026-06-04-persona-2-003-manifest.md` |
| P1-001 transcript | `docs/ux/usability-sessions/transcripts/2026-06-04-persona-1-001-transcript.md` |
| P1-001 findings | `docs/ux/usability-sessions/findings/2026-06-04-persona-1-001-findings.md` |
| P1-001 manifest | `docs/ux/usability-sessions/manifests/2026-06-04-persona-1-001-manifest.md` |
| P5-001 transcript | `docs/ux/usability-sessions/transcripts/2026-06-04-persona-5-001-transcript.md` |
| P5-001 findings | `docs/ux/usability-sessions/findings/2026-06-04-persona-5-001-findings.md` |
| P5-001 manifest | `docs/ux/usability-sessions/manifests/2026-06-04-persona-5-001-manifest.md` |
| M11.5 Exit Checklist | Issue #720 |
| Mean-reversion channel | Issue #221 (GAP-06 dependency) |
