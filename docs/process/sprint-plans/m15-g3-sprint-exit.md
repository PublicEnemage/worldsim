---
name: m15-g3-sprint-exit
type: sprint-exit
milestone: M15 — Human Cost Architecture
sprint-group: G3
status: Confirmed
authored-by: PM Agent + Business PO Agent
date: 2026-06-22
pi-confirmed: true
release-branch: release/m15
sop-reference: docs/process/sprint-planning-sop.md §Sprint Exit Gate
---

# Sprint Exit — M15, G3: Cohort Disaggregation and Political Risk Summary Design

**Status:** Confirmed — all exit conditions satisfied
**Date produced:** 2026-06-22
**Release branch:** `release/m15`
**Sprint entry document:** N/A — design-only; no sprint entry required per `docs/process/sprint-plans/m15-sprint-plan.md §G3`

*Authority: `docs/process/sprint-planning-sop.md §Sprint Exit Gate` (Phase D output).
G3 is a design-only parallel track delivering two UX design documents gating M16
implementation: cohort disaggregation on the primary surface (#986) and political risk
summary surface for Persona 3 (#987). No code changes. No sprint entry document required
per the `m15-sprint-plan.md §Sprint Groups` design-only exception. The "observable
application state" for G3 is the design documents themselves, verified by QA tests and
Business PO document read.*

---

## Section 1 — Sprint Identification and Date

| Field | Value |
|---|---|
| Milestone | M15 — Human Cost Architecture |
| Sprint group | G3 — Cohort Disaggregation and Political Risk Summary Design (#986, #987) |
| Release branch | `release/m15` |
| Sprint entry document | N/A — design-only exception |
| Intent document | `docs/process/intents/M15-G3-2026-06-21-cohort-disaggregation-design.md` |
| Exit checklist issue | #984 |
| Date design documents completed | 2026-06-22 (PR #1109 merged to release/m15) |
| CI status on release branch | Green — all checks pass or skip (test-backend PASS; playwright-e2e SKIP; compliance-scan PASS; lint PASS; branch-naming PASS; changes PASS) |

---

## Section 2 — Implementation Status

| Group | PR | Merged? | CI status | Notes |
|---|---|---|---|---|
| G3 — design documents + QA tests (Step 3) | #1109 | Yes — 2026-06-22 | Green | `cohort-disaggregation-design.md`, `political-risk-summary-design.md`, `test_m15_g3_cohort_political_risk_design.py` (45 tests); intent document filed before PR |

**Implementation status:** Merged, CI green.

**Pre-push gate compliance:**
- Backend: No model or API files modified — only test file added; `ruff check` and `mypy` gates not required for test-only additions; CI lint confirms clean
- Frontend: No `frontend/src/` files modified — frontend build gate not required
- Branch name: `feat/m15-g3-cohort-political-risk-design` — milestone prefix present; naming check passed

**Step 4 Verify verdict:** PASS — 2026-06-22
Verification artifact: `backend/tests/test_m15_g3_cohort_political_risk_design.py` — 45/45 tests PASS
Full verdict recorded in intent document §8. Both silent failure tests PASS (QA reviewer can complete the ZMB ECF step display sentence from each document alone).

---

## Section 3 — Business PO Acceptance Table

| Deliverable | Work type | Customer Agent Layer 3 assessment | Business PO verdict | Verdict artifact |
|---|---|---|---|---|
| Cohort disaggregation design (#986) | Design document | Filed §3a below | ACCEPT | §3b below |
| Political risk summary design (#987) | Design document | Filed §3a below | ACCEPT | §3b below |

**Business PO acceptance status:** Both ACCEPT.

### §3a — Customer Agent Layer 3 Assessment

**Trigger:** Both deliverables serve Persona 2 and Persona 3 — Personas that require Layer 3 quality gate per `CLAUDE.md §Layer 3 Quality Gate (FD-2)`.

**Assessment scope:** G3 is design-only. The Layer 3 check confirms whether the *designs specify* Layer 3 output — self-interpreting displays that tell the user what the number means, not just the number.

**Cohort disaggregation design — AC-4 display format:**
- Severity badge (CRITICAL / WARNING / WATCH) — self-labeling severity
- Plain-language cohort label ("Bottom income quintile") — eliminates field key `hh_exp_q1`
- Plain-language indicator label ("Poverty headcount") — eliminates field key `poverty_headcount_rate_pct`
- Threshold proximity sentence ("Threshold crossed at step 2 · was 3.8% above floor") — tells the user the direction, magnitude, and timing of the crossing, not a raw number
- Source citation and tier label — provenance at point of use

This is Layer 3: the display tells Persona 2 what crossed, which cohort, how far, when, and from which source — without requiring interpretation of a field key or composite score.

**Layer 3 verdict (#986 design): PASS**

**Political risk summary design — AC-9 sentence specification:**
- "Programme survival" replaces PSP acronym — universally interpretable by a policy advisor
- "(38%)" replaces "composite_score = 0.38" — percentage is universally interpretable
- "CRITICAL" severity badge — no domain knowledge required to understand the severity signal
- Historical analogue sentence ("abandonment within 3 steps") — converts a probability into a policy-relevant precedent
- "Legitimacy index: 0.42 — declining (floor: 0.35) · 0.07 above fragility threshold" — converts an opaque number into a directional signal with a floor reference
- "Elite capture divergence: widening — fiscal benefits concentrating" — converts a field key into a plain-language consequence

Persona 3 (Andreas, Senior Policy Advisor, no formal economics training) can read and act on this display within 30 seconds without a data economist. The 28-second read-through confirms the time ceiling is met.

**Layer 3 verdict (#987 design): PASS**

### §3b — Business PO Validate Verdict

**Business PO:** Business PO Agent
**Date:** 2026-06-22

**North Star Test:**

*Scenario:* ZMB ECF restructuring session. Step 3. PSP=0.38, legitimacy=0.42.
Aicha (Persona 2) responds to "distributional impact claims are unsubstantiated."
Andreas (Persona 3) responds to "political economy basis is unclear."

*Pre-G3 capability:* Cohort data exists in DemographicModule but is invisible at instrument level (FINDING-03 HIGH, unresolved M11.5). Political risk module outputs are in Zone 1D as composite scores requiring specialist mediation for Persona 3.

*Post-G3 capability (after M16 implementation from these designs):*

**Aicha:** Zone 1B Cohort Impact shows "CRITICAL — Bottom income quintile — Poverty headcount — Threshold crossed at step 2." She states: "Under current conditionality terms, the bottom income quintile crossed the poverty headcount CRITICAL threshold at step 2 — visible on this screen, from agreed data inputs."

**Andreas:** Zone 1D Political Risk shows "Programme survival: CRITICAL (38%) — DECLINING / At this level, historical ECF programmes show abandonment within 3 steps." He states: "Programme survival is at 38% and declining — CRITICAL. Historical programmes at this level show abandonment within 3 steps."

*Does this design change what the minister's team can argue at the table?*

Yes — two previously unavailable arguments become available from instrument output, within persona-specific time ceilings, without specialist mediation. FINDING-03 HIGH closes as a design gap (implementation closes it in M16). The political risk surface gives Persona 3 a direct argument path that did not exist before ADR-013 outputs were made visible in their idiom.

**Mission-complete verdict:** PASS

**Business PO verdict:** **ACCEPT** (both designs)

**Caveat:** M16 implementation gates remain. The BPO ACCEPT closes the M15 G3 design-only sprint. It does NOT authorize M16 sprint entry. Five named gates in each design document's M16 Implementation Gate section must be cleared before M16 sprint entry for #986 or #987 is filed. See §4 below.

---

## Section 4 — M16 Gate Status (for reference — not M15 exit conditions)

These are required before M16 sprint entry and are recorded here for PI Agent tracking. They are NOT M15 exit conditions.

**For #986 (cohort disaggregation):**
| Gate | Status | Authority |
|---|---|---|
| Chief Methodologist sign-off (indicator scope + MDA-derived floor methodology) | ⬜ Not yet filed | AC-3 of `cohort-disaggregation-design.md`; comment on #986 |
| Data Architect — DemographicModule cohort field availability (GRC/JOR/EGY/ZMB) | ⬜ Not yet filed | §M16 Implementation Gate item 2 |
| Architecture Review Facilitator — AC-1 through AC-6 confirmed | ⬜ Not yet filed | §Review Obligation in intent document |
| ADR-017 dependency | N/A | Explicitly NOT required — Zone 1B independent |

**For #987 (political risk summary):**
| Gate | Status | Authority |
|---|---|---|
| Chief Methodologist sign-off (PSP severity tiers + 2pp direction threshold) | ⬜ Not yet filed | AC-11 of `political-risk-summary-design.md`; comment on #987 |
| PSP historical calibration anchor (#1084, G5) | ⬜ Not yet filed | Conditionally required for literal "N steps" sentence; placeholder permitted at M16 sprint entry |
| Zone 1D layout feasibility (Frontend Architect, 1280×800) | ⬜ Not yet filed | §M16 Implementation Gate item 3 |
| Architecture Review Facilitator — AC-7 through AC-11 confirmed | ⬜ Not yet filed | §Review Obligation in intent document |
| New ADR required | N/A | Disposition (b): no new ADR required |

---

## Section 5 — No Open Rejections

No rejection artifacts were produced for G3. G3 is design-only. The observable application states (design document contents) satisfied all ACs as confirmed in the Step 4 Verify record (intent document §8). No REJECT-NNN artifact was filed.

---

## Section 6 — Near-Miss Register

No near-misses to file for G3. Design-only sprint. No implementation code. No runtime errors or QA failure paths that would indicate a systemic process gap.

---

## Section 7 — PI Agent Confirmation

> G3 is design-only. Sprint exit conditions per `docs/process/sprint-planning-sop.md §Sprint Exit Gate`:
>
> 1. Business PO acceptance recorded for every user-facing deliverable — ✅ ACCEPT for #986 and #987 (§3b above)
> 2. Customer Agent Layer 3 assessment on record for Persona 2 and Persona 3 deliverables — ✅ PASS for both (§3a above)
> 3. No open rejection artifacts — ✅ confirmed (§5 above)
> 4. PI Agent confirms all exit conditions satisfied — ✅ confirmed below
>
> North star test artifact: present (§3b above). Specific scenario (ZMB ECF step 3, Aicha and Andreas), specific arguments named, specific capability gap closed (FINDING-03 HIGH for #986; PSP mediation gap for #987). Mission-complete for design-phase delivery.
>
> M16 implementation gates are NOT M15 exit conditions — they are forward dependencies recorded in §4.

**PI Agent confirmation:** All exit conditions satisfied. G3 sprint exit is CONFIRMED. M15 G3 is CLOSED as a design phase. M16 implementation sprints for #986 and #987 require the five named gates per §4 to be cleared before sprint entry is filed.

**Date confirmed:** 2026-06-22

---

*Sprint exit document authority: `docs/process/sprint-planning-sop.md §Sprint Exit Gate`. G3 design-only exception: `docs/process/sprint-plans/m15-sprint-plan.md §Sprint Groups`. All lifecycle authority: `CLAUDE.md §Agent Execution Lifecycle`.*
