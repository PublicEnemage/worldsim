---
name: m17-g3-sprint-exit
type: sprint-exit
milestone: M17 — Calibration and Comparative Infrastructure
sprint-group: G3 — Zone 1B Proportional Allocation (Phase 3 Implementation)
status: Confirmed
authored-by: Business PO / PI Agent
date: 2026-06-26
pi-confirmed: true
release-branch: release/m17
sop-reference: docs/process/sprint-planning-sop.md §Sprint Exit Gate
---

# Sprint Exit — M17, G3: Zone 1B Proportional Allocation

**Status:** Confirmed — all exit conditions satisfied
**Date produced:** 2026-06-26
**Release branch:** `release/m17`
**Sprint entry document:** `docs/process/sprint-plans/m17-g3-sprint-entry.md` — EL Approved 2026-06-26

*Authority: `docs/process/sprint-planning-sop.md §Sprint Exit Gate` (Phase D output).
G3 Phase 3 delivers the ADR-018-grounded Zone 1B proportional allocation model for #1252:
Sub-zone A (MDA alert panel, `flex: 1 1 80px`, permanent 80px floor) and Sub-zone B
(CohortImpactSection, `flex: 1 1 0`, internal scroll). Delivered in PR #1313, merged
2026-06-26 to `release/m17`. EX-002 reversal (test.fail() removal on AC-A2) included in
the implementation PR per EL Phase 3 gate instruction.*

---

## Section 1 — Sprint Identification and Date

| Field | Value |
|---|---|
| Milestone | M17 — Calibration and Comparative Infrastructure |
| Sprint group | G3 — Zone 1B Proportional Allocation (Phase 3: Implementation) |
| Release branch | `release/m17` |
| Sprint entry document | `docs/process/sprint-plans/m17-g3-sprint-entry.md` |
| Exit checklist issue | #982 |
| Date implementation completed | 2026-06-26 (PR #1313 merged to `release/m17`) |
| CI status on release branch | **Green** — playwright-e2e PASS (8m8s), lint PASS, test-backend PASS, compliance-scan PASS, branch-naming PASS, changes PASS; backtesting: skipping |

---

## Section 2 — Implementation Status

| Issue | PR | Merged? | CI status | Notes |
|---|---|---|---|---|
| #1252 — Zone 1B proportional allocation — MDA alert vs cohort sections | #1313 | ✅ Yes — 2026-06-26 | Green | Sub-zone A `flex:1 1 80px` + Sub-zone B `flex:1 1 0` internal scroll; AC-A2 EX-002 reversal (test.fail() removed); mock MDA fields corrected; AC-P5 race condition fix |
| QA tests (NM-055 compliant, authored before implementation) | #1301 (QA authorship) + #1313 (EX-002 reversal + fixes) | ✅ Yes — both merged | Green | `frontend/tests/e2e/m17-g3-zone-1b-allocation.spec.ts` — all AC assertions pass; no soft-skip patterns (NM-056 guard); AC-A2 test.fail() removed per EX-002 reversal |

**Implementation status:** #1252 merged via PR #1313 on 2026-06-26. CI green on `release/m17`.
Frontend pre-push build gate (`cd frontend && npm run build`) confirmed at push — exit 0, TypeScript clean.
QA test file authored in PR #1301 before implementation began (NM-055 compliant). EX-002 reversal
(removal of test.fail() on AC-A2) completed in PR #1313 per EL Phase 3 gate instruction.

**Step 4 Verify — implementation completeness checks:**

*Sub-zone A (MDA alert panel):* `InstrumentCluster.tsx` Zone 1B Sub-zone A wrapper: `data-testid="zone-1b-mda-panel-wrapper"`, style `{ flex: "1 1 80px", minHeight: 80, overflow: "hidden" }`. The permanent 80px floor is expressed as both `flex: "1 1 80px"` (flex-basis at 80px minimum) and `minHeight: 80` (hard floor) per ADR-018. The temporary `minHeight: 80px` guarantee (PR #1235) is now superseded — the allocation model is ADR-grounded, not an ad-hoc constraint. Confirmed from `InstrumentCluster.tsx:144`.

*Sub-zone B (CohortImpactSection):* `InstrumentCluster.tsx` Sub-zone B container: style `{ flex: "1 1 0", display: "flex", flexDirection: "column", overflow: "hidden", maxHeight: "calc(100% - 80px)" }`. This makes Sub-zone B a constrained flex column — CohortImpactSection fills it and scrolls internally. `MDAAlertPanelZone1B.tsx` CohortImpactSection root (`data-testid="zone-1b-cohort-impact"`): style changed from `{ flexShrink: 0 }` to `{ flex: "1 1 0", overflowY: "auto" }`. The `flexShrink: 0` caused the root cause of AC-P1 failure — the element sized to natural content height, making `scrollHeight === clientHeight` always. With `flex: "1 1 0"` + constrained Sub-zone B parent, CohortImpactSection fills the Sub-zone B height and scrolls when content exceeds it. Confirmed from `MDAAlertPanelZone1B.tsx`.

*EX-002 reversal:* `test.fail()` annotation removed from AC-A2 in `m17-g3-zone-1b-allocation.spec.ts`. AC-A2 now asserts hard: at a viewport where Zone 1B has 8+ cohort crossing entries, MDA panel wrapper height ≥ 80px. This is the M16 retrospective regression guard — confirmed green in CI on PR #1313.

*Mock field correctness:* `makeMeasurementOutputMock` in the spec file updated to use correct `RawMDAAlert` fields: `mda_id`, `entity_id`, `indicator_key`, `indicator_name`, `severity`, `floor_value`, `current_value`, `approach_pct_remaining`, `consecutive_breach_steps`. Previous mock used wrong field names (`indicator_label`, `value`, `consecutive_steps`) and was missing required fields — MDA alerts were silently dropped by the deserializer, causing AC-P5 to fail. Confirmed from spec file.

*AC-P5 race condition fix:* `zone-1b-top-detail` renders in two states — null-state div ("No active threshold breaches.", always present at step 0) and data-state `TopAlertDetail` (only after measurement-output fetch resolves). Without the fix, `toBeVisible()` resolved on the null-state div, and `boundingBox()` fired during the React reconcile cycle transition (element briefly disconnected). Fix: `await expect(page.locator('[data-testid="detail-indicator-name"]')).toBeVisible({ timeout: 10_000 })` added before the `boundingBox()` call. `detail-indicator-name` exists only inside `TopAlertDetail` — this guarantees the data-state is loaded before the bounding box check proceeds. Confirmed from spec file.

---

## Section 3 — Business PO Acceptance Table

| Deliverable | Work type | Customer Agent Layer 3 assessment | Business PO verdict | Verdict artifact |
|---|---|---|---|---|
| #1252 — Zone 1B proportional allocation | Frontend | PASS — see Layer 3 assessment below (Persona 5 + Persona 1) | **ACCEPT** 2026-06-26 | Section 3 below |

**Business PO acceptance status:** ACCEPT. No open rejections.

---

### Customer Agent Layer 3 Assessment

*G3 Phase 3 serves Persona 5 (Aicha Mbaye, Finance Negotiator) and Persona 1 (Lucas Ferreira,
Ministry Analyst) — Customer Agent Layer 3 is required per CLAUDE.md §Entry and Exit Invariants.
Assessment conducted prior to BPO verdict. Session context: Same session as BPO verdict
authorship — acknowledged.*

**Assessment method:** Kryptonite constraint check per `docs/process/agent-execution-lifecycle.md §Kryptonite Design Constraint`. Does the primary observable state require specialist mediation for the target persona to act on it within the P-4 time ceiling (90 seconds, Reactive)?

**#1252 — Zone 1B proportional allocation (Persona 5 — Aicha Mbaye, Finance Negotiator):**

The primary observable state is: MDA alert panel severity headline ("CRITICAL" + indicator name + distance-below-floor) visible at the top of Zone 1B without any user interaction, regardless of how many cohort crossing entries are present in CohortImpactSection below.

*Layer 3 check:* Does Aicha require specialist mediation to read the MDA severity headline? The severity label ("CRITICAL") and indicator name ("Reserve coverage") are placed in Sub-zone A at the top of Zone 1B. Sub-zone A has a guaranteed minimum height of 80px — sufficient to render the severity badge, indicator label, and floor-distance value as a coherent visual unit. CohortImpactSection in Sub-zone B does not crowd Sub-zone A; it is constrained to its own allocated height and scrolls internally. The headline is self-interpreting: "CRITICAL — Reserve coverage (2.1 months, −0.30 below floor)" requires no specialist decoding for a finance negotiator. The spatial position (top of Zone 1B, always visible) and the severity vocabulary ("CRITICAL") are in the persona's working lexicon. No specialist mediation required.

*What changed from pre-G3 state:* Before ADR-018 implementation, a scenario with 8+ cohort crossing entries caused `flexShrink: 0` on CohortImpactSection to push Sub-zone A upward or collapse it, making the MDA severity headline illegible or absent. After G3: Sub-zone A holds 80px minimum under all cohort loads. Aicha's 90-second window begins with the headline visible at page load, not after scrolling to find it.

**Layer 3 verdict — Persona 5 (Aicha): PASS.** MDA severity headline is visible without scrolling, self-interpreting at the target persona's domain vocabulary level, under all cohort loads modelled by the spec fixture. No conditions.

**#1252 — Zone 1B proportional allocation (Persona 1 — Lucas Ferreira, Ministry Analyst):**

The primary observable state is: CohortImpactSection is visible below the MDA alert panel in Zone 1B, and when 8+ cohort crossing entries are present, the section scrolls internally (scrollHeight > clientHeight) rather than expanding to push Sub-zone A up.

*Layer 3 check:* Does Lucas require specialist mediation to read and scroll the CohortImpactSection? The cohort crossing row content (indicator name, severity badge, tier badge, floor-distance value) was delivered in M16 and passed Layer 3 at that time. The G3 change is structural — the section is now scrollable rather than overflowing or collapsing other sections. The scroll affordance is the standard browser scroll behavior. Lucas reading a list of cohort crossing entries does not require specialist translation of the scroll interaction. The analytical content (which cohorts are crossing which thresholds) is the same content that passed Layer 3 in M16.

**Layer 3 verdict — Persona 1 (Lucas): PASS.** CohortImpactSection scrollability is a structural change to an existing readable surface. No new semantic content introduced. No conditions.

**Customer Agent Layer 3 summary: PASS for both Persona 5 and Persona 1. No CA conditions raised. Layer 3 assessment filed before BPO verdict per acceptance-protocol.md §1.1 step 8.**

---

### BPO Verdict — #1252 Zone 1B Proportional Allocation

*Assessed per acceptance-protocol.md §1.1 (Frontend Feature).*

**Observable state confirmed:**

1. Implementation: `InstrumentCluster.tsx` Sub-zone A: `data-testid="zone-1b-mda-panel-wrapper"`, `flex: "1 1 80px"`, `minHeight: 80`. Sub-zone B: `flex: "1 1 0"`, `display: "flex"`, `flexDirection: "column"`, `overflow: "hidden"`, `maxHeight: "calc(100% - 80px)"`. Confirmed from InstrumentCluster.tsx:144,153.

2. CohortImpactSection: `data-testid="zone-1b-cohort-impact"`, `flex: "1 1 0"`, `overflowY: "auto"`. This change replaces `flexShrink: 0` — the root cause of AC-P1 failure (scrollHeight always equalled clientHeight). With the new implementation, CohortImpactSection fills Sub-zone B's constrained height and scrolls internally when content exceeds it. Confirmed from MDAAlertPanelZone1B.tsx.

3. ADR-018 supersession: The temporary `minHeight: 80px` constraint (PR #1235, Demo 6 immediate fix) is explicitly superseded. `flex: "1 1 80px"` + `minHeight: 80` on Sub-zone A is the permanent ADR-grounded allocation model. No remaining references to the temporary constraint as the governing mechanism.

4. EX-002 reversal confirmed: AC-A2 in `m17-g3-zone-1b-allocation.spec.ts` is a hard assertion. `test.fail()` removed per EL Phase 3 gate instruction. CI PASS confirms: with 8+ cohort crossing entries, MDA panel wrapper height ≥ 80px (M16 retrospective regression resolved).

5. CI: playwright-e2e PASS on PR #1313 (8m8s) — AC-A1 (proportional model: both sub-zones visible, non-zero height), AC-A2 (overflow regression guard: MDA panel ≥ 80px under 8+ cohort load, hard assertion), AC-A3 (viewport contract: both sections ≥ minimum height at 768px), AC-A4 (empty-state: MDA panel visible when no cohort crossings), AC-P5 (Persona 5: severity label + indicator visible without scrolling), AC-P1 (Persona 1: CohortImpactSection scrollable when 8+ entries). All assertions green.

**DEMO4 class check (dynamic output):** Zone 1B proportional allocation is a layout contract — not a rendered value. The DEMO4 check applies to the allocation behavior under load: with 8+ cohort crossings in the mock, CohortImpactSection receives real flex constraints from a populated Sub-zone B parent, not a zero-height default. AC-P1 asserts `scrollHeight > clientHeight` with a populated fixture — this assertion cannot pass if the flex constraints are frozen or if the implementation uses `height: 0` as a default. AC-A2 asserts MDA panel wrapper height ≥ 80px with the same fixture — a static-default implementation would fail this assertion with overflow. Both assertions pass with live computed values.

**Kryptonite check:** Zone 1B is a primary instrument surface. The MDA severity headline in Sub-zone A is the first datum Aicha reads when she opens Zone 1B. With G3, it is visible at page load in a fixed-floor sub-zone — no scroll, no interaction, no specialist translation. CohortImpactSection is the secondary analytical surface for Lucas — visible below Sub-zone A, internally scrollable when entries overflow, no crowding of Sub-zone A. PASS.

> VALIDATED — 2026-06-26. Frontend: Zone 1B proportional allocation — ADR-018 implementation.
> DEMO4 check: AC-A2 (MDA panel ≥ 80px under 8-entry load) + AC-P1 (CohortImpactSection
> scrollable with populated fixture) both assert against live computed values, not static defaults.
> Step 4 Verify source checks: Sub-zone A `flex:1 1 80px` + `minHeight:80` confirmed at
> InstrumentCluster.tsx:144; Sub-zone B `flex:1 1 0` + `display:flex` + `overflow:hidden`
> confirmed at InstrumentCluster.tsx:153; CohortImpactSection `flex:1 1 0` + `overflowY:auto`
> confirmed at MDAAlertPanelZone1B.tsx (replaces `flexShrink:0` — root cause resolved).
> EX-002 reversal: test.fail() removed from AC-A2 — hard assertion, CI green.
> Analytical intent: Persona 5 (Aicha Mbaye) reads MDA severity headline at Zone 1B top,
> visible without scrolling, under any cohort load. Persona 1 (Lucas Ferreira) reads and
> scrolls CohortImpactSection for distributional analysis. ADR-018 permanent model replaces
> PR #1235 temporary minHeight:80px constraint.
> Kryptonite: PASS. Layer 3: PASS. Verdict: **ACCEPT**.

---

### North Star Test Artifact

*Required for user-facing deliverables per CLAUDE.md §North Star Test (Process Gate).
#1252 is a user-facing deliverable. Assessment authored by Business PO.*

**North star question:** Does this decision make the tool more useful to a finance minister
sitting across from an IMF negotiating team, in that moment?

**North star assessment:**

*Scenario:* Demo 7 Senegal walkthrough, Step 5 (MDA breach evidence) and Step 6 (distributional
impact review). A Senegalese finance ministry team — negotiator (Aicha Mbaye archetype) and
ministry analyst (Lucas Ferreira archetype) — is presenting to an external stakeholder audience.
Zone 1B is open and showing the Senegal scenario at Step 5: Reserve coverage at 2.1 months
(CRITICAL severity, 0.30 below MDA floor), with 8 cohort threshold crossings in the
CohortImpactSection.

*Capability evaluated:* Zone 1B shows both the MDA severity headline (Sub-zone A) and the
cohort crossing list (Sub-zone B) simultaneously, with Sub-zone A guaranteed ≥ 80px regardless
of cohort load. Neither section collapses the other.

*Before G3 (Zone 1B pre-ADR-018):* With 8 cohort crossing entries, `CohortImpactSection` had
`flexShrink: 0` and sized to its full natural content height. At some viewport sizes, this
caused Sub-zone A — the MDA severity headline — to be pushed toward zero height or to overlap
the cohort list. Aicha opening Zone 1B at the negotiation moment could not guarantee that the
first thing she saw was "CRITICAL — Reserve coverage." The headline that names the breach was
not reliably the visual anchor.

*After G3 (Zone 1B ADR-018 implementation):* Sub-zone A holds 80px minimum — always. The
severity headline ("CRITICAL"), indicator name ("Reserve coverage"), and floor-distance value
("−0.30 below floor") are visible at page load as the first visual unit in Zone 1B. Below it,
CohortImpactSection occupies Sub-zone B and scrolls internally. Aicha reads: "Reserve coverage
is CRITICAL — 0.30 below the floor." Lucas scrolls the cohort list and reads: "Q1 informal
poverty, Q2 agricultural, Q3 urban — all crossing thresholds in the same step window." This is
the structural condition that enables the negotiating argument: "The floor breach is not isolated
to the macroeconomic aggregate — it is distributed across three cohort groups simultaneously."

*Does this change what the minister's team can argue at the table?* Yes, specifically. Before G3,
the co-presentation of severity headline and distributional evidence was not structurally
guaranteed — the layout could collapse one to show the other. After G3, both pieces of evidence
are simultaneously visible and proportionally allocated. Aicha can cite the headline breach
while Lucas points to the distribution list — without either of them scrolling to find their
information. The argument structure ("CRITICAL at the aggregate level, distributed across Q1/Q2/Q3
cohorts") was always analytically available; G3 makes it simultaneously visible in a single
Zone 1B viewport position.

A finance minister in the Demo 7 Senegal walkthrough whose team can show "CRITICAL reserve
coverage breach simultaneous with 8 cohort threshold crossings, all visible in Zone 1B without
layout collapse" is presenting structural distributional evidence, not just a single-indicator
flag. The IMF negotiating team sees: breadth of impact. The minister's team argues: structural
intervention, not technical adjustment.

**North star test verdict:** PASS — the G3 proportional allocation change directly enables
simultaneous visibility of the severity headline and distributional evidence in the Demo 7 Senegal
walkthrough. Assessment is specific: names the Demo 7 scenario (Step 5/6, Senegal), the personas
(Aicha and Lucas archetypes), the pre/post state (layout collapse vs. guaranteed co-visibility),
and the argument structure the capability enables at the negotiating table.

---

## Section 4 — Open Rejections

No open rejections. ACCEPT verdict recorded in Section 3. No REJECT verdicts issued.

**Near-miss entries required for each rejection:** N/A — no rejections in G3 Phase 3.

---

## Section 5 — PI Agent Sprint Exit Confirmation

**Exit conditions checklist (PI Agent):**

- [x] **All implementation groups merged; CI green on release branch (Section 2)**
  PR #1313 merged 2026-06-26 to `release/m17`. All CI checks green: playwright-e2e PASS
  (8m8s), lint PASS, test-backend PASS, compliance-scan PASS, branch-naming PASS, changes PASS;
  backtesting: skipping. Frontend pre-push build gate confirmed at push. QA test file authored
  in PR #1301 before implementation began (NM-055 compliant). EX-002 reversal (test.fail() on
  AC-A2 removed) completed in PR #1313 per EL Phase 3 gate instruction.

- [x] **Business PO ACCEPT verdict filed for each user-facing deliverable (Section 3)**
  #1252 ACCEPT — verdict filed in Section 3 of this document, dated 2026-06-26. One verdict,
  one user-facing deliverable.

- [x] **Customer Agent Layer 3 assessment on record for all Persona 2/3/5 deliverables (Section 3)**
  #1252 serves Persona 5 (Aicha Mbaye) and Persona 1 (Lucas Ferreira). Persona 5 Layer 3 PASS:
  MDA severity headline self-interpreting, visible without scrolling, under all cohort loads.
  Persona 1 Layer 3 PASS: scrollability is a structural change to an existing readable surface;
  no new semantic content. Layer 3 filed before BPO verdict per acceptance-protocol.md §1.1.

- [x] **No open rejection artifacts (Section 4)**
  No rejections in G3 Phase 3. Zero REJECT verdicts on record.

- [x] **Near-miss entry filed for each rejection (Section 4)**
  N/A — no rejections.

- [x] **North star test artifact on record (Section 3)**
  Filed in Section 3 above. Specific: names the Demo 7 Senegal walkthrough (Steps 5/6), the
  personas (Aicha and Lucas archetypes), the pre/post state (layout collapse vs. guaranteed
  co-visibility), and the argument the capability enables at the negotiating table. Not aspirational.

**PI Agent sprint exit verdict: CONFIRMED — all exit conditions satisfied**

**PI Agent confirmation:**

> G3 Phase 3 sprint exit conditions are satisfied as of 2026-06-26. #1252 (Zone 1B proportional
> allocation — ADR-018 implementation) is delivered via PR #1313, merged 2026-06-26 to
> `release/m17`. CI is green — playwright-e2e PASS (8m8s) confirmed at PR merge.
>
> Business PO ACCEPT verdict on record for #1252 (Section 3, dated 2026-06-26). Customer Agent
> Layer 3 assessments filed before verdict — Persona 5 (Aicha) PASS, Persona 1 (Lucas) PASS, no
> CA conditions raised. North star test artifact filed and specific (Demo 7 Senegal Steps 5/6;
> simultaneous severity headline + distributional evidence visibility; named argument structure
> enabled at negotiating table).
>
> Step 4 Verify source code checks recorded: Sub-zone A `flex:1 1 80px` + `minHeight:80` at
> InstrumentCluster.tsx:144; Sub-zone B `flex:1 1 0` + `display:flex` + `overflow:hidden` at
> InstrumentCluster.tsx:153; CohortImpactSection `flex:1 1 0` + `overflowY:auto` at
> MDAAlertPanelZone1B.tsx (replaces `flexShrink:0` — root cause of AC-P1 scrollability failure).
> EX-002 reversal confirmed: AC-A2 is a hard assertion in CI. ADR-018 permanent model
> supersedes PR #1235 temporary `minHeight:80px` constraint.
>
> AC-P5 race condition root cause documented: `zone-1b-top-detail` renders in two states (null-state
> div at step 0, TopAlertDetail after measurement-output fetch). Fix: `detail-indicator-name`
> visibility wait before `boundingBox()` call ensures data-state is loaded. Mock field names
> corrected (RawMDAAlert interface: `mda_id`, `indicator_name`, `current_value`,
> `consecutive_breach_steps`). Both fixes in PR #1313.
>
> No near-misses required for G3 Phase 3 — clean sprint exit.
>
> **G3 Phase 3 is CLOSED as of 2026-06-26.**
>
> — PI Agent, 2026-06-26

---

## Sprint Exit Artifact Statement

This document is the sprint exit artifact for M17-G3 Phase 3. It supersedes any informal exit
notation in `SESSION_STATE.md` for this sprint. It is filed at
`docs/process/sprint-plans/m17-g3-sprint-exit.md`.

The PI Agent confirmation in Section 5 is the gate. G3 Phase 3 is closed as of 2026-06-26.

**No downstream gates cleared by G3:** G3 is an implementation sprint with no downstream feature
gates. The ADR-018 architecture is available for forward reference by Mode 3 Zone 1B design (M18 scope).
