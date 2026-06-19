---
name: m14-g6b-sprint-exit
type: sprint-exit
milestone: M14 — Methodology Publication and External Validation
sprint-group: G6b
status: Confirmed
authored-by: PM Agent
date: 2026-06-18
pi-confirmed: true
release-branch: release/m14
sop-reference: docs/process/sprint-planning-sop.md §Sprint Exit Gate
---

# Sprint Exit — M14, G6b: Path 2 Design Groundwork (Ministry-Owned Data Upload)

**Status:** Confirmed — all exit conditions satisfied
**Date produced:** 2026-06-18
**Release branch:** `release/m14`
**Sprint entry document:** N/A — design-only; sprint plan explicitly waives sprint entry requirement for G6b

*Authority: `docs/process/sprint-planning-sop.md §Sprint Exit Gate` (Phase D output).
G6b is a design-only deliverable authorized as a parallel track by EL directive 2026-06-16.
No sprint entry document required per `docs/process/sprint-plans/m14-sprint-plan.md §G6b`.
No implementation PR. No QA Lead test obligation. The deliverable is three Markdown design
artifacts that gate M15 scoping and M16 implementation of Path 2 (ministry-owned data upload).*

---

## Section 1 — Sprint Identification and Date

| Field | Value |
|---|---|
| Milestone | M14 — Methodology Publication and External Validation |
| Sprint group | G6b — Path 2 Design Groundwork |
| Release branch | `release/m14` |
| Sprint entry document | N/A — design-only; sprint plan §G6b waives requirement |
| Intent document | `docs/process/intents/M14-G6b-2026-06-18-path2-design-groundwork.md` |
| Design artifacts (deliverables) | `docs/design/path2-data-upload/field-mapping-ux-concept.md` |
| | `docs/design/path2-data-upload/user-supplied-provenance-spec.md` |
| | `docs/design/path2-data-upload/data-isolation-model-sketch.md` |
| Issue | #976 — Path 2: ministry-owned / proprietary data upload (design M14; implementation M16+) |
| Exit checklist issue | #968 |
| Date design completed | 2026-06-18 |
| PR merged | PR #1034 → release/m14 |
| CI status on release branch | Green — PR #1034 passed all required checks |

---

## Section 2 — Implementation Status

| Group | PR | Merged? | CI status | Notes |
|---|---|---|---|---|
| G6b — Path 2 design artifacts (3 documents) | #1034 | Yes — 2026-06-18 | Green | Design-only; no Python or frontend/src/ files modified; no pre-push lint or build gate required |

**Implementation status:** All three design artifacts merged, CI green.

**Pre-push gate compliance:**
- Backend: No Python files modified — backend gate not required
- Frontend: No `frontend/src/` files modified — frontend build gate not required
- Branch name: `feat/m14-g6b-path2-design-artifacts` — milestone prefix present, naming check passed

**Step 4 Verify:** Design-only deliverable. Observable states are the three documents themselves.
AC-1 through AC-9 verifiable by any agent reading the filed artifacts without referencing
implementation code. Verified by Business PO at Step 5 (Section 3 below), per intent document
§7: "EL review of AC-1 through AC-9 is the detection mechanism."

---

## Section 3 — Business PO Acceptance Table

| Deliverable | Work type | Customer Agent Layer 3 assessment | Business PO verdict | Verdict artifact |
|---|---|---|---|---|
| `field-mapping-ux-concept.md` (Artifact 1) | Documentation | N/A — no user-facing indicator output | ACCEPT | Session 2026-06-18; recorded in this exit document §3b |
| `user-supplied-provenance-spec.md` (Artifact 2) | Documentation | N/A — no user-facing indicator output | ACCEPT | Session 2026-06-18; recorded in this exit document §3b |
| `data-isolation-model-sketch.md` (Artifact 3) | Documentation | N/A — no user-facing indicator output | ACCEPT | Session 2026-06-18; recorded in this exit document §3b |

**Business PO acceptance status:** All three artifacts ACCEPT.

---

### §3a — Layer 3 Assessment

Layer 3 trigger condition: "Any implementation that introduces or modifies a user-facing
indicator label, alert text, output narrative, or confidence tier disclosure."

G6b produces three design artifacts — specifications for future implementation. They introduce
no user-facing output in the running application. The Layer 3 gate does not trigger.

The *design specifications* in the artifacts were assessed for kryptonite compliance at intent
authorship time (intent document §5) and confirmed at BPO Validate (§3b below): the 5-minute
field mapping workflow was explicitly evaluated against the specialist-mediation test and
confirmed to be achievable by a ministry analyst who is not a software engineer, without a
data scientist or IT specialist. That assessment is recorded in the BPO verdict, not in the
Layer 3 gate.

---

### §3b — Business PO Validate Verdict (Step 5)

*Filed by Business PO — 2026-06-18.*

**Work type:** Documentation (three design artifacts)
**Documentation Validate criterion:** A non-author can navigate to the key finding from the
document's entry point in under five minutes.

**AC-by-AC review (Business PO, 2026-06-18):**

| AC | Description | Status | Finding |
|---|---|---|---|
| AC-1 | `field-mapping-ux-concept.md` exists; step-by-step workflow; timing ≤ 5 min for 10-variable spreadsheet | PASS | 4 steps: 30s + 90s + 90s + 60s = 4:30 with 30s headroom; timing table explicit in §3 |
| AC-2 | Field mapping step shows column name → canonical variable → transformation → confirmation gate in prototype-ready detail | PASS | Step 2 mock shows all four elements; 5-rule matching logic specified; visual mock, dropdown structure, error states all present |
| AC-3 | Both failure modes addressed: (a) no canonical match; (b) ambiguous match | PASS | Section 4 gives dedicated coverage; each mode shows analyst's visible information and available actions; no-silent-inclusion rule explicit |
| AC-4 | Reproducibility caveat placement: in-workflow location and post-creation location specified | PASS | Section 5: Step 3 inline (above [Apply and create scenario →], not dismissible); Grounding strip permanent ⚠ banner; "Learn more" content specified |
| AC-5 | `user-supplied-provenance-spec.md` exists; USER_SUPPLIED defined with plain-English label, Grounding Strip example, tier rules, tier hierarchy position | PASS | Display label "user-supplied" with rejected-label table; canonical example "· T2 · user-supplied"; §3.1 tier table; simplified hierarchy present |
| AC-6 | ADR-007 implication and ADR-016 unchanged elements stated | PASS | §5 names ADR-007 update with verbatim statement text; §6 lists 6 ADR-016 elements unchanged with status and rationale |
| AC-7 | `data-isolation-model-sketch.md` exists; isolation invariant, three failure modes, Issue #53 requirements | PASS | §1 gives narrative + formal set-theoretic invariant; §2 gives three failure modes each with root cause and detection; §3 gives three specific Issue #53 decisions |
| AC-8 | What Issue #53 is NOT required to solve stated, preventing scope creep | PASS | §4 names four explicit out-of-scope items with rationale; §6 summary table distills the three required decisions |
| AC-9 | All three artifacts committed to canonical path before M14 exit | PASS | `docs/design/path2-data-upload/` contains all three files; M14 exit gate not yet confirmed |

**Two findings noted (neither blocking):**

- **F-1 (Minor — documentation):** Intent document §5 Kryptonite checkboxes are both `[ ]` unchecked. The substantive confirmation is in Artifact 1 §6 "Kryptonite Constraint Confirmation." The template checkbox was not updated to mark the applicable condition; the artifact satisfies the substance. No remediation required.
- **F-2 (Observation):** AC-5 example format in intent document shows `"· user-supplied"` without a tier label; both artifacts correctly use `"· T2 · user-supplied"` consistent with the §3.2 visual spec. Artifact is richer than the abbreviated AC example. No remediation required.

**North Star Test (P-7, design-level forward trace):**

G6b's north star is a design-level gate: "After M14 G6b, the EL and M15 sprint team can open
three design documents that specify without ambiguity: how the ministry uploads data (Artifact 1),
what USER_SUPPLIED means in the provenance chain (Artifact 2), and what isolation guarantee the
system must provide (Artifact 3). A sprint team reading these three artifacts in M15 can begin
Path 2 scoping without redesign."

Test result: **PASS.** After M14 G6b:

- A frontend engineer opening `field-mapping-ux-concept.md` can prototype the upload UI from
  the Step 2 visual mock, 5-rule matching logic, and failure mode specifications without asking
  the authoring agent for any decision.
- The Path 2 implementation ADR author opening `user-supplied-provenance-spec.md` has the enum
  value, display label, rejected-label rationale, tier assignment table, tier hierarchy position,
  ADR-007 update statement, and scope boundary — all specified without ambiguity.
- The Issue #53 design team opening `data-isolation-model-sketch.md` has the isolation invariant
  (narrative + formal), three concrete failure modes (each with root cause and detection), and
  exactly three required decisions scoped — not more, not less.

The concrete argument enabled after Path 2 implementation (M16+): "The reserve coverage figure
in this run is 2.8 months — that is our internal position as of this morning, not the IMF BoP
vintage. That figure is ministry-supplied and is noted as such in the Grounding Strip." This
argument was architecturally unavailable before G6b. G6b makes it architecturally specified.
M15/M16 implementation will make it available in the running application.

**Navigation test:** The key finding per artifact:
- Artifact 1 → §3 End-to-End Timing Summary table (≤1 min from open)
- Artifact 2 → §2.2 Display Label + §3.1 Tier Table (≤2 min from open)
- Artifact 3 → §1 Isolation Invariant + §6 Prerequisites Summary table (≤2 min from open)

All three navigable to key finding within 5 minutes from document entry point. PASS.

**Kryptonite Constraint:** Satisfied. Artifact 1 §6 provides explicit evidence that the
5-minute ceiling is achievable without specialist mediation — file picker (standard), auto-mapping
handles ~70% of columns, transformation summaries show derived values not formula strings, inline
edit affordances handle edge cases without requiring a data scientist.

**Business PO Validate verdict:** **ACCEPT**

---

## Section 4 — Open Rejections

No open rejections. Proceed to Section 5.

---

## Section 5 — PI Agent Sprint Exit Confirmation

**Exit conditions checklist (PI Agent):**

- [x] All three design artifacts merged to release/m14; CI green (Section 2) — PR #1034 merged 2026-06-18; all required checks passed; branch name milestone-compliant
- [x] Business PO ACCEPT verdict filed for all three design artifact deliverables (Section 3) — ACCEPT recorded in §3b (2026-06-18); AC-1 through AC-9 each reviewed and passed
- [x] Customer Agent Layer 3 assessment: not required — Layer 3 gate not triggered for documentation deliverables with no user-facing indicator output (Section 3a confirmed)
- [x] No open rejection artifacts (Section 4) — confirmed none; two observations (F-1, F-2) are non-blocking and do not produce rejection artifacts
- [x] Near-miss entries: none required — no rejections filed; F-1 and F-2 are documentation observations below NM threshold
- [x] North Star forward trace present in Business PO verdict (§3b) — Zambian/Jordanian analyst argument named; Path 2 architectural prerequisites now specified without ambiguity; M15 sprint team can begin scoping without redesign
- [x] Intent document AC-1 through AC-9 each verified by Business PO reading the filed artifacts from `docs/design/path2-data-upload/`
- [x] Issue #976 status consistent — issue remains open (M16+ implementation scope); design deliverable for M14 is complete; no premature closure

**Additional PI check — no sprint entry deviation NM required:**
The sprint plan (`docs/process/sprint-plans/m14-sprint-plan.md §G6b`) explicitly states the
design-only exception for G6b and G6c — "no sprint entry document required; no implementation PR."
This is a sprint plan authorization, not a deviation. No near-miss entry is required for the
absent sprint entry document.

**Additional PI check — F-1 Kryptonite checkbox gap assessment:**
F-1 (unchecked Kryptonite checkboxes in intent document §5) is a documentation gap in the
template completion, not a process violation. The kryptonite constraint substance is satisfied
by Artifact 1 §6 with explicit evidence. A NM is not warranted — the gap produced no design
ambiguity and was detected and named by the BPO at Validate time. The observation is on record
in §3b. The intent document template could benefit from a note clarifying that design-only
intents may satisfy the Kryptonite check in the artifact rather than the intent document — this
is a candidate for the next intent template revision, not an emergency NM.

**PI Agent sprint exit verdict:** Confirmed — all exit conditions satisfied

> G6b delivers three self-contained design artifacts specifying Path 2 (ministry-owned data
> upload) across three dimensions: upload and field mapping UX workflow (Artifact 1), the
> USER_SUPPLIED provenance type for ADR-016 (Artifact 2), and the data isolation guarantee
> that Issue #53 must provide (Artifact 3).
>
> All 9 acceptance criteria (AC-1 through AC-9) pass by document inspection. Business PO
> ACCEPT recorded with a specific north star forward trace: the "ministry-supplied reserve
> figure" argument for Persona 2, architecturally unavailable before G6b, is now fully
> specified for M16+ implementation.
>
> Two non-blocking observations noted (F-1 intent template checkbox, F-2 AC example
> abbreviation). Neither produces a rejection artifact or near-miss. Both are on record.
>
> Layer 3 gate not triggered — documentation deliverable with no user-facing indicator
> output. No rejections filed. No open artifacts. Issue #976 remains open at M16+ scope
> (correct — design work is M14; implementation is M16+).
>
> M15 Path 2 scoping is unblocked. Issue #53 design team has an exact three-decision
> prerequisite specification. G6b is complete.

---

## Sprint Exit Artifact Statement

This document is the sprint exit artifact for G6b of M14. It supersedes any informal exit
notation in SESSION_STATE.md for G6b. It is filed at
`docs/process/sprint-plans/m14-g6b-sprint-exit.md`.

The PI Agent confirmation in Section 5 is the gate. G6b closes as of this document.
No subsequent sprint group is blocked by G6b — the release branch is clean and CI is green.
