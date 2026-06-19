---
name: m14-g4-sprint-exit
type: sprint-exit
milestone: M14 — Methodology Publication and External Validation
sprint-group: G4
status: Confirmed
authored-by: PM Agent
date: 2026-06-17
pi-confirmed: true
release-branch: release/m14
sop-reference: docs/process/sprint-planning-sop.md §Sprint Exit Gate
---

# Sprint Exit — M14, G4: ADR-016 Frontend (Grounding Strip + Data Quality Preview + Parameter Persistence + IC-4/IC-6 Mitigations)

**Status:** Confirmed — PI Agent sprint exit verdict recorded (Section 5)
**Date produced:** 2026-06-17
**Release branch:** `release/m14`
**Sprint entry document:** `docs/process/sprint-plans/m14-g4-sprint-entry.md`

*Authority: `docs/process/sprint-planning-sop.md §Sprint Exit Gate` (Phase B/C output).
Changes to this template require PM Agent authorship and EL endorsement.*

---

## Section 1 — Sprint Identification and Date

| Field | Value |
|---|---|
| Milestone | M14 — Methodology Publication and External Validation |
| Sprint number | G4 |
| Release branch | `release/m14` |
| Sprint groups | G4 — ADR-016 Frontend |
| Sprint entry document | `docs/process/sprint-plans/m14-g4-sprint-entry.md` |
| Exit checklist issue | #968 |
| Date implementation completed | 2026-06-17 |
| CI status on release branch | Green — all required checks pass (PR #1018, run `27727653243`) |

---

## Section 2 — Implementation Status

*All groups must be merged and CI must be green on the release branch. This is necessary but
not sufficient for sprint exit. (Authority: sprint-planning-sop.md §Sprint Exit Gate condition 1)*

| Group | PR | Merged? | CI status | Notes |
|---|---|---|---|---|
| G4 — ADR-016 Frontend (main implementation) | #1015 | Yes | Green | Entity selector + data quality preview + grounding strip + parameter persistence + IC-4/IC-6 headers |
| G4 — AC-5 text fix (fidelity-contextualisation substring) | #1016 | Yes | Green | "does not validate input data" → "— not input data" to satisfy contiguous substring check at Step 4 |
| G4 — REJECT-001 fix (GroundingIndicator field names + E2E test hardening) | #1018 | Yes | Green | `source_institution`→`source`, `data_vintage`→`vintage`; AC-3 route mock; AC-4 regex; AC-7 timing fix |

**Implementation status:** All merged, CI green.

---

## Section 3 — Business PO Acceptance Table

| Deliverable | Work type | Customer Agent Layer 3 assessment | Business PO verdict | Verdict artifact |
|---|---|---|---|---|
| Entity selector + data quality preview (ADR-016 §Component 1) | Frontend | Filed: intent doc §9 — PASS | ACCEPT | `docs/process/intents/M14-G4-2026-06-17-adr016-frontend.md §9` |
| Grounding strip — button + panel (ADR-016 §Component 2) | Frontend | Filed: intent doc §9 — PASS | ACCEPT | `docs/process/intents/M14-G4-2026-06-17-adr016-frontend.md §9` |
| Parameter persistence display (ADR-016 §Component 4) | Frontend | Filed: intent doc §9 — PASS (Persona 3 retrospective state) | ACCEPT | `docs/process/intents/M14-G4-2026-06-17-adr016-frontend.md §9` |
| IC-4 mitigation — static Fidelity panel header (`fidelity-contextualisation`) | Frontend | Filed: intent doc §9 — PASS | ACCEPT | `docs/process/intents/M14-G4-2026-06-17-adr016-frontend.md §9` |
| IC-6 mitigation — choropleth reference header | Frontend | Filed: intent doc §9 — PASS | ACCEPT | `docs/process/intents/M14-G4-2026-06-17-adr016-frontend.md §9` |
| "None" framework filter in Grounding strip | Frontend | Filed: intent doc §9 — PASS | ACCEPT | `docs/process/intents/M14-G4-2026-06-17-adr016-frontend.md §9` |

**Business PO acceptance status:** All ACCEPT. Initial REJECT-001 issued (AC-3), resolved, and re-accepted. No outstanding rejections.

### Notes on Customer Agent Layer 3 assessments

| Deliverable | Serves Persona 2/3/5? | Layer 3 filed before verdict? |
|---|---|---|
| Entity selector + data quality preview | Yes — Persona 2 (Preparatory entry state) | Yes — intent doc §9 Customer Agent Layer 3 Assessment |
| Grounding strip | Yes — Persona 2 (Reactive entry state; 90s ceiling) | Yes — intent doc §9 Customer Agent Layer 3 Assessment |
| Parameter persistence display | Yes — Persona 3 (Retrospective entry state) | Yes — intent doc §9 Customer Agent Layer 3 Assessment |
| IC-4 Fidelity header | Yes — Persona 2 (scope clarification, indirect) | Yes — intent doc §9 Customer Agent Layer 3 Assessment |
| IC-6 choropleth header | Yes — Persona 2 (scope clarification, indirect) | Yes — intent doc §9 Customer Agent Layer 3 Assessment |
| "None" framework filter | Yes — Persona 2 (prevents false framework sections) | Yes — intent doc §9 Customer Agent Layer 3 Assessment |

**Layer 3 finding summary (intent doc §9):** PASS. Grounding strip output (`Reserve coverage: 7.1 months · CBJ · 2023-Q4 · T2`) is self-interpreting — value in human units, source institution named, vintage in calendar notation, tier stated. Ministry-side analyst can cite this at the negotiating table without specialist mediation. Data quality preview's synthetic flag (`T4 synthetic — MENA comparable economies 2022-2023`) names the inference basis explicitly. No mediation asymmetry introduced by G4.

---

## Section 4 — Open Rejections

| Rejection artifact | Deliverable | Defect named | Remediation scope | Resolution status |
|---|---|---|---|---|
| `docs/process/rejections/REJECT-001-2026-06-17-grounding-strip-missing-source-citations.md` | Grounding strip (AC-3) | Source institution names (`CBJ`, `IMF`, `DOS`) absent from every indicator row in the Grounding strip despite being present at the API | Return to Step 1 (field name contract re-examination) → Step 3 (code fix) → Step 4 (E2E test hardening) → Step 5 (BPO re-validate) | **Re-accepted** — PR #1018 merged 2026-06-17. BPO re-validate: PASS. |

**Near-miss entries required for each rejection:**

| Rejection | Near-miss entry | NM number |
|---|---|---|
| REJECT-001 | Filed — `docs/process/near-miss-registry.md §NM-045` | NM-045 |

**REJECT-001 root cause summary:** `GroundingIndicator` in `frontend/src/types.ts` declared field names from the `/data-quality` endpoint (`source_institution`/`data_vintage`) rather than the `/initial-state` endpoint (`source`/`vintage` per `api_contracts.yml`). `GroundingStrip.tsx` read `ind.source_institution` and `ind.data_vintage`, both `undefined` at runtime, producing an empty citation string for every row. The AC-3 E2E test used a generic regex fallback `/[·•]\s*\S/` that matched the tier separator `· T2` rather than an institution name, masking the defect through Step 4. Data Architect review (EL-requested 2026-06-17) confirmed the API contract is correct and requires no update; the fix was frontend-only.

**Additional CI hardening in PR #1018 (not defects in the implementation):**
- AC-3 converted to `page.route()` mock for `/initial-state` — same pattern as AC-9 — because in CI the source_registry has no JOR entries seeded; a live endpoint always returns `source: null` in that environment. The mock injects `{"source": "CBJ", "vintage": "2023-Q4"}` and tests that `GroundingStrip.tsx` renders the citation correctly.
- AC-4 base year regex: `\b(19|20|21)\d{2}\b` → `(19|20|21)\d{2}` — `textContent()` concatenates spans without separator so "2023" appears as "year2023" where `\b` before "2" fails (`r`→`2` are both `\w`).
- AC-4 steps regex: `\b[1-9]\d*\b` → `[1-9]\d*` — same reason ("Steps3Fiscal" has no word boundary around "3").
- AC-3/AC-7 timing: `await expect(strip).not.toContainText("Loading grounding data", { timeout: 8_000 })` added before text assertions to prevent race condition between `toBeVisible()` and the `/initial-state` fetch completing.
- `createJORCompletedScenario` fixture: added `start_date: "2023-01-01"` to the configuration payload so AC-4 base year renders "2023" in CI (previously showed "(not recorded)").

Frontend Architect consultations: AC-3 route-mock approach confirmed correct; AC-4 textContent word-boundary analysis documented in commit; AC-3 CI race root cause analysis documented in commit.

---

## Section 5 — PI Agent Sprint Exit Confirmation

**Exit conditions checklist (PI Agent):**

- [x] All implementation groups merged; CI green on release branch (Section 2) — PRs #1015, #1016, #1018 all merged; CI all-green on PR #1018 run `27727653243`
- [x] Business PO ACCEPT verdict filed for each user-facing deliverable, or EL exception on record (Section 3) — BPO ACCEPT 2026-06-17, intent doc §9; REJECT-001 issued, resolved, and re-accepted
- [x] Customer Agent Layer 3 assessment on record for all Persona 2/3/5 deliverables, filed before Business PO verdict (Section 3) — intent doc §9 Layer 3 Assessment PASS, filed in same session as BPO verdict
- [x] No open rejection artifacts (Section 4) — REJECT-001 resolved; re-acceptance confirmed by BPO
- [x] Near-miss entry filed for each rejection in this sprint (Section 4) — NM-045 filed for REJECT-001

**PI Agent sprint exit verdict:** Confirmed — all exit conditions satisfied.

**PI Agent confirmation:**

> All five sprint exit conditions are satisfied for M14 G4. Business PO ACCEPT is on record
> in the intent document §9 for all six user-facing deliverables. Customer Agent Layer 3
> assessment PASS was filed before the BPO verdict and confirms no mediation asymmetry.
> REJECT-001 was issued, tracked in `docs/process/rejections/`, remediated in PR #1018,
> and re-accepted by BPO with observable states confirmed. NM-045 is filed in the
> near-miss registry. CI is green on `release/m14`. No open rejection artifacts remain.
>
> North star test (P-7) is PASS: the Zambian finance ministry analyst can open the Grounding
> strip and respond to an input challenge with a source citation ("CBJ · 2023-Q4 · T2")
> in under 90 seconds from a loaded scenario, with no specialist mediation required. This
> capability was unavailable from the screen before G4. G3 placed the data at the API;
> G4 put it on screen. Both are now on `release/m14`.
>
> G5 (ADR-015 Evidence Thread) is unblocked. No subsequent sprint group is blocked by G4.
>
> — PI Agent, 2026-06-17

---

## Sprint Exit Artifact Statement

This document is the sprint exit artifact for G4 of M14. It supersedes any informal
exit notation in SESSION_STATE.md for this sprint. It is filed at
`docs/process/sprint-plans/m14-g4-sprint-exit.md`.

*The PI Agent confirmation in Section 5 is the gate. The sprint closes when the PI Agent's
verdict is "Confirmed." No subsequent sprint group begins until this verdict is recorded.*
