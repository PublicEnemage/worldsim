---
name: m19-g4-sprint-exit
type: sprint-exit
milestone: M19 — Constraint Search and Empirical Calibration
sprint-group: G4 — PSP Driver Arc + CI Label Polish
status: Confirmed
authored-by: PM Agent
date: 2026-07-03
pi-confirmed: true
release-branch: release/m19
sop-reference: docs/process/sprint-planning-sop.md §Sprint Exit Gate
---

# Sprint Exit — M19, G4: PSP Driver Arc + CI Label Polish

**Status:** Confirmed — PI Agent exit conditions satisfied 2026-07-03
**Date produced:** 2026-07-03
**Release branch:** `release/m19`
**Sprint entry document:** `docs/process/sprint-plans/m19-g4-sprint-entry.md`

*Authority: `docs/process/sprint-planning-sop.md §Sprint Exit Gate` (Phase B/C output).
Changes to this template require PM Agent authorship and EL endorsement.*

---

## Section 1 — Sprint Identification and Date

| Field | Value |
|---|---|
| Milestone | M19 — Constraint Search and Empirical Calibration |
| Sprint number | 5 (G4 — PSP Driver Arc + CI Label Polish) |
| Release branch | `release/m19` |
| Sprint groups | G4 |
| Sprint entry document | `docs/process/sprint-plans/m19-g4-sprint-entry.md` |
| Exit checklist issue | #1535 |
| Date implementation completed | 2026-07-03 |
| CI status on sprint branch | Green — both implementation PRs auto-merged to `sprint/m19-g4` with all required checks passing (including Playwright E2E) |

---

## Section 2 — Implementation Status

*All groups must be merged and CI must be green on the sprint branch. This is necessary but
not sufficient for sprint exit. (Authority: sprint-planning-sop.md §Sprint Exit Gate condition 1)*

**Process PRs (prerequisite, not user-facing deliverables):**

| PR | Content | Merged? |
|---|---|---|
| (via #1631) | G4 intent documents, sprint entry, QA test files | Yes — via chore/m19-state-sync-025, 2026-07-03 |

**Implementation PRs (user-facing deliverables):**

| Group | PR | Merged? | CI status | Notes |
|---|---|---|---|---|
| PSP driver arc + methodology panel (#1528) | #1633 | Yes — 2026-07-03 | Green — all required checks including Playwright E2E | 11 ACs; psp-driver-arc, psp-driver-methodology-panel, fragility amplifier |
| CI label precision fix (#1529) | #1634 | Yes — 2026-07-03 | Green — all required checks including Playwright E2E | 9 ACs; ci-calibration-status text; distributional label fix |

**Implementation status:** Both implementation PRs merged to `sprint/m19-g4`; all required checks green on both, including Playwright E2E (11 ACs for #1528, 9 ACs for #1529). Pre-push frontend build gate passed before each push (TypeScript build clean, no TS errors). G3 #1537 coordination gate was satisfied before G4 opened — `band_method` enum values frozen in merged codebase.

**Demo 8 forward condition resolved:** G3 sprint exit §6 held a forward condition: "G4 #1529 CI label precision fix must land before Demo 8 Act 2 for the provisional calibration label to be visible." PR #1634 merged 2026-07-03. The `PRE_CALIBRATION_PROVISIONAL_DIRECTIONAL` → "provisional — directional calibration only" text is now live in `sprint/m19-g4`. **Forward condition closed.**

---

## Section 3 — Customer Agent Layer 3 Assessments

*G4 deliverables serve Persona 3 (Andreas Stefanidis, Political Advisor — #1528) and
Persona 1 (Lucas Ferreira, IMF Senior Economist) and Persona 2 (Eleni, Ministry Analyst) — #1529.
Customer Agent Layer 3 assessment is a precondition for Business PO verdicts.*

*Same-session Layer 3 assessment — disclosed: assessments were conducted in the same session
as implementation. Governing documents reviewed: `docs/ux/personas.md §Persona 3 (Andreas)`,
`docs/ux/personas.md §Persona 1 (Lucas)`, `docs/ux/personas.md §Persona 2 (Eleni)`,
`docs/ux/north-star.md §Primary Cognitive Tasks`, `docs/ux/user-journeys.md §Programme Review`,
`docs/adr/ADR-019-control-plane-column.md §Zone 1D`, `docs/adr/ADR-007-synthetic-data-framework.md §Amendment 1 §8.7`.*

*Layer 3 assessment artifact: sprint journal #1624 comment (2026-07-03). Referenced below.*

---

### Layer 3 Assessment — #1528 PSP Driver Arc + Methodology Panel

**Scenario:** Andreas (Persona 3, Political Advisor to the ZMB finance ministry) is in a
programme review session. The IMF programme officer challenges: "How exactly is 'fiscal
sustainability' attributed as the dominant driver at Step 4?" Previously, Andreas had no
in-session answer — he would have needed to call a technical officer or reference external
documentation, costing credibility and time.

**Layer 1 (Does it work?):** Arc renders with correct abbreviations (FISC/EXT/GOV/SOC/—).
Current step badge has fontWeight 700 + border (CSS-observable, not colour-only). Expand panel
opens on click showing all four `psp-driver-category-{cat}` elements with non-empty text.
Fragility amplifier status correctly derived from `parseFloat(legitimacyValue) < parseFloat(legitimacyFloor)`.
Panel collapses on second click. All 11 AC testids wired and Playwright-confirmed. PASS.

**Layer 2 (Does it make sense to an informed user?):** Category descriptions use plain English:
"spending cuts or tax increases in this step (legitimacy erosion)" is interpretable by a
political advisor without econometric training. The "⚠ Fragility amplifier active" warning
is surfaced as a plain indicator, not a model parameter. The tiebreaker rule is a one-line
disclosure. The arc shows programme-window driver history in compact text badges. PASS.

**Layer 3 (Does it create unexpected burden or risk for Andreas?):** No specialist mediation
required for Andreas to understand and act on this output within the 30-second ceiling
(P-4 in intent doc). The expand panel opens in-viewport — no navigation, no drawer, no scroll.
Andreas can read the methodology and close the panel without leaving Zone 1D. No cognitive
overhead imposed: the panel is click-in, click-out. The information is additive —
Andreas can ignore the expand affordance and still see the driver label as before.
**Layer 3 verdict: PASS.**

---

### Layer 3 Assessment — #1529 CI Label Precision Fix

**Scenario:** Lucas (Persona 1, IMF Senior Economist) reads the distributional comparison
summary before the programme review session. The label previously said "95% CI" — a
frequentist precision claim the BandingEngine structural model does not support. Lucas
knows the methodology; he would have challenged this label in the session, undermining
Eleni's (Persona 2) ability to cite the comparison summary in submissions.

**Layer 1 (Does it work?):** `ci-calibration-status` element renders with correct text for
all three non-suppressed `band_method` states. Element absent for SUPPRESSED_MEANINGLESS.
"declared interval" replaces "95% CI" unconditionally in DistributionalComparisonSummary.
Tooltip contains required strings ("Structural uncertainty model", "BandingEngine", "not a
frequentist confidence interval"). All 9 ACs Playwright-confirmed. Demo 8 gate (AC-2,
PRE_CALIBRATION_PROVISIONAL_DIRECTIONAL → "provisional — directional calibration only") green. PASS.

**Layer 2 (Does it make sense?):** "Declared interval" is accurate — it describes a stated
range, not a probabilistic one. "Provisional — directional calibration only" is self-describing.
The `ci-calibration-status` element appears as a sub-label, not as a warning or error —
it is additional information, not a correction. The tooltip is optional context for those
who press for technical detail. PASS.

**Layer 3 (Does it create unexpected burden or risk for Lucas or Eleni?):** No burden created.
The label change resolves a first-impression precision overclaim that previously *created*
burden for Eleni (she would have had to pre-emptively disclaim the label in submissions).
After G4, she can cite the summary using language that withstands statistical scrutiny.
Lucas cannot challenge the label — because it no longer overclaims. The `ci-calibration-status`
text adds information; it does not reframe or complicate what was already visible.
**Layer 3 verdict: PASS.**

---

## Section 4 — Business PO Acceptance Table

*Business PO verdicts recorded in sprint journal #1624 comment (2026-07-03).*

| Deliverable | Work type | Customer Agent Layer 3 | Business PO verdict | Conditions |
|---|---|---|---|---|
| #1528 — PSP driver arc + methodology panel | Frontend (Zone 1D) | PASS (Section 3) | **ACCEPT (unconditional)** | All 11 ACs confirmed; Playwright E2E green; kryptonite check CLEAR |
| #1529 — CI label precision fix | Frontend (Zone 1A + Zone 1B) | PASS (Section 3) | **ACCEPT (unconditional)** | All 9 ACs confirmed; Demo 8 gate cleared; kryptonite check CLEAR |

**Business PO acceptance status:** Both deliverables ACCEPT (unconditional). No open rejections.

### Notes on Customer Agent Layer 3 assessments

| Deliverable | Serves Persona 2/3/5? | Layer 3 filed before verdict? |
|---|---|---|
| #1528 — PSP driver arc + methodology panel | Yes — Persona 3 (Andreas, Political Advisor, P-2/3/4/6/7 in intent doc) | Yes — sprint journal #1624, same session, before verdicts |
| #1529 — CI label precision fix | Yes — Persona 1 (Lucas) and Persona 2 (Eleni) | Yes — sprint journal #1624, same session, before verdicts |

**G3 Demo 8 forward condition resolved:**
G3 sprint exit §6 carried a forward condition: "G4 #1529 CI label precision fix must land before
Demo 8 Act 2 for the provisional calibration label to be visible to Aicha." PR #1634 merged
2026-07-03. The condition is now satisfied. PI Agent to update exit checklist issue #1535.

---

## Section 5 — Open Rejections

No open rejections. Proceed to Section 6.

---

## Section 5b — Forward Conditions and Known Gaps

**Forward condition — api_contracts.yml §trajectory `band_method` gap (Issue #1632):**

G3 #1537 (BandResult visible fields) was required to update `docs/schema/api_contracts.yml`
in the same PR (per intent doc §3). The update did not land. G4 #1529 QA ack block carries
an open NM-086 gate (`[ ]`) for the `band_method` field not found in `api_contracts.yml §trajectory`.

**Status:** Filed as issue #1632 (2026-07-03). Scoped to G5 (schema-only fix, no code change).
The E2E mock helpers for G4 #1529 use `band_method` values from the G3 #1537 intent doc §2
frozen enum table — this is correct. The implementation works; the documentation gap is a
schema drift compliance finding. **G4 exit is not blocked** by this gap, because:
1. Implementation is correct and tests pass (including E2E)
2. The gap is a G3 delivery gap, not a G4 implementation defect
3. Issue #1632 is filed and scoped to G5

**PI Agent forward condition:** Issue #1632 must be resolved (api_contracts.yml updated) before
G5 closes. PI Agent to track on exit checklist issue #1535.

---

## Section 6 — PI Agent Sprint Exit Confirmation

*PI Agent reviews all exit conditions and confirms they are satisfied before the sprint exit
checklist issue is closed.*

**PI Agent — Near-Miss Sweep (G4 sprint period: 2026-07-03):**

| Finding | Category | Action |
|---|---|---|
| `band_method` not in api_contracts.yml — G3 delivery gap (Section 5b) | Known delivery gap | Filed as issue #1632; scoped to G5; NOT a near-miss (it is a G3 obligation not met, not a G4 process failure) |
| No new NMs identified during G4 implementation | — | No new NM entries required |

Most recent NM: NM-089. No new entries required for G4 sprint period.

**Exit conditions checklist (PI Agent):**

- [x] All implementation PRs merged; CI green on sprint branch (Section 2) — SATISFIED: PRs #1633 and #1634 merged to `sprint/m19-g4`; all required checks green on both including Playwright E2E. Pre-push frontend build gate passed before both pushes.
- [x] Business PO ACCEPT verdict filed for each user-facing deliverable (Section 4) — SATISFIED: ACCEPT (unconditional) on record for #1528 and #1529 (sprint journal #1624, 2026-07-03)
- [x] Customer Agent Layer 3 assessment on record for all Persona 2/3/5 deliverables, filed before Business PO verdict (Section 3) — SATISFIED: Layer 3 for #1528 (Persona 3) and #1529 (Persona 1/2) in Section 3 above, same session, before verdicts. Same-session disclosed.
- [x] No open rejection artifacts (Section 5) — SATISFIED
- [x] Near-miss sweep conducted for sprint period (Section 6 above) — SATISFIED: no new NMs; api_contracts.yml gap filed as issue #1632 (delivery gap, not near-miss)
- [x] North star test artifact present and specific for user-facing deliverables (Section 7) — SATISFIED: north star test authored in sprint journal #1624, 2026-07-03; names Zambia ECF scenario, named personas, concrete capability changes
- [x] G3 Demo 8 forward condition — RESOLVED: G4 #1529 (`PRE_CALIBRATION_PROVISIONAL_DIRECTIONAL` text) now live on `sprint/m19-g4`; PR #1634 merged 2026-07-03
- [x] G3 coordination gate — satisfied at sprint entry (band_method enum values frozen in G3 merge); no residual gate obligations

**PI Agent sprint exit verdict: CONFIRMED — all exit conditions satisfied.**

**PI Agent confirmation:**

> All G4 exit conditions are satisfied as of 2026-07-03. Both implementation PRs (#1633 for
> #1528 PSP driver arc, #1634 for #1529 CI label precision) are merged to `sprint/m19-g4` with
> all required checks green, including Playwright E2E (11 ACs for #1528, 9 ACs for #1529).
> Business PO ACCEPT verdicts (unconditional) are on record for both deliverables in sprint
> journal #1624. Customer Agent Layer 3 assessments for Persona 3 (#1528) and Persona 1/2
> (#1529) are filed in the same sprint journal comment, before verdicts — same-session
> disclosure noted.
>
> North star test artifact (Section 7) is specific: names the Zambia ECF programme review
> scenario, Andreas as the political advisor fielding the driver attribution challenge, Lucas as
> the IMF economist who cannot challenge "declared interval" precision language. Both capabilities
> are assessed as changing concrete negotiating outcomes, not aspirationally improving the tool.
>
> One forward condition carried forward: api_contracts.yml §trajectory missing `band_method`
> field (issue #1632, G3 delivery gap). Filed and scoped to G5. Does not block G4 exit —
> implementation is correct, tests pass, gap is documentation only.
>
> G3 Demo 8 forward condition is resolved: G4 #1529 merged, `PRE_CALIBRATION_PROVISIONAL_DIRECTIONAL`
> → "provisional — directional calibration only" is live. PI Agent to update exit checklist
> issue #1535 to close this condition.
>
> **Next step:** PM Agent to open integration PR `sprint/m19-g4` → `release/m19`.
> PI Agent to post gate comment on integration PR. Set auto-merge.
>
> — PI Agent (in-session, 2026-07-03)

---

## Section 7 — North Star Test Artifact

*Required per CLAUDE.md §North Star Test (Process Gate) for user-facing capabilities.
Authored by Business PO (sprint journal #1624, 2026-07-03). PI Agent confirms presence and specificity.*

### G4 Combined North Star Test — Driver Attribution Auditability + Interval Label Precision

**Sprint-level deliverables assessed:** #1528 (PSP driver arc + methodology panel) and #1529
(CI label precision fix) — assessed together because they serve the same programme review
session at Demo 8.

**North star test verdict: PASS (unconditional)**

---

**Scenario:**

Zambia ECF programme review, Step 4 of 8. The ministry team includes Andreas (Political Advisor,
Persona 3) and Eleni (Ministry Analyst, Persona 2). Across the table is Lucas (IMF Senior
Economist, Persona 1). Two challenges arrive simultaneously.

**Challenge 1 (Lucas to Andreas):** "How exactly is 'fiscal sustainability' attributed as the
dominant driver at Step 4? What is the computation basis?"

*Before #1528:* Andreas has no in-session answer. He sees "Driver: fiscal sustainability" but
cannot explain it from the instrument. He must call the technical team or concede the point.

*After #1528:* Andreas clicks "▶ Driver: fiscal sustainability." In under 5 seconds, a panel
opens in Zone 1D showing:
- "spending cuts or tax increases in this step (legitimacy erosion)" — why fiscal sustainability
  fires at this step
- "⚠ Fragility amplifier active — contributions amplified by fragility factor at current
  legitimacy" — why the attribution is amplified
- The arc showing FISC at steps 1–4, with GOV at step 3 (emergency policy action in that step)
- Tiebreaker rule: governance > fiscal sustainability > external balance

Andreas says: "The fiscal sustainability attribution at Step 4 is computed from the spending-cut
events in this step applying the legitimacy erosion elasticity, amplified because current
legitimacy is 0.42 — three points below the 0.45 fragility threshold. Here is the computation
in the panel." He closes the panel and returns to the instrument view in under 10 seconds.
**Lucas cannot dismiss this as a black box. The attribution is explained, in-session, in Zone 1D.**

**Challenge 2 (Lucas to Eleni's summary):** "This '95% CI' label on your distributional
comparison implies a frequentist confidence interval. Your methodology doesn't support that
precision claim."

*Before #1529:* Eleni has no response to this. The label said "95% CI." She would need to
disclaim it or request a recess to clarify. The ministry's comparison summary is challenged
before it is discussed.

*After #1529:* The label reads "declared interval." The hover tooltip explains: "Structural
uncertainty model — BandingEngine step-based schedule; not a frequentist confidence interval."
The `ci-calibration-status` element in Zone 1A shows: "provisional — directional calibration
only." Eleni says: "The interval is a declared structural range, not a frequentist CI — the
label reflects this. The calibration state is provisional-directional: direction is empirically
validated on ZMB/SEN backtesting; magnitude fidelity is not yet claimed." **Lucas's challenge
has no traction. The label was already accurate.**

**What these capabilities change at the table:**

Both capabilities shift the epistemic burden. The driver methodology panel means the IMF team
must engage with the attribution argument, not dismiss it as opaque. The interval label means
the IMF team cannot challenge statistical precision language that no longer overclaims. Together,
they close two first-impression challenges that previously had no in-session answer.

**PI Agent specificity confirmation:** Test names the finance minister scenario (Zambia ECF,
Step 4), the challenge persona (Lucas, IMF), and the responding personas (Andreas, Eleni).
It names concrete argument changes: attribution from "black box" to "here is the computation";
interval label from "95% CI" (challengeable) to "declared interval" (not challengeable).
Test is specific, not aspirational. Unconditional PASS — no forward conditions required.

---

## Section 8 — Integration PR

*Per sprint group isolation protocol (CLAUDE.md §Release Branch Workflow), the integration PR
fires after PI Agent exit confirmation.*

**Integration PR target:** `sprint/m19-g4` → `release/m19`
**Required steps:**
1. PM Agent opens PR: `sprint/m19-g4` → `release/m19`
2. PI Agent posts gate comment on integration PR confirming G4 exit conditions satisfied
3. PM Agent sets auto-merge: `gh pr merge <number> --merge --auto`
4. Pull release branch: `git pull origin release/m19`

---

## Sprint Exit Artifact Statement

This document is the sprint exit artifact for Sprint 5 (G4 — PSP Driver Arc + CI Label Polish)
of M19. It supersedes any informal exit notation in `SESSION_STATE.md` for this sprint. It is
filed at `docs/process/sprint-plans/m19-g4-sprint-exit.md`.

*The PI Agent confirmation in Section 6 is the gate. The sprint closes when the PI Agent's
verdict is "Confirmed" — recorded above, 2026-07-03.*
