---
name: m17-g3-sprint-entry
type: sprint-entry
milestone: M17 — Calibration and Comparative Infrastructure
sprint-group: G3 (Phase 3 — Implementation)
status: EL Approved 2026-06-25 — Phase 1 UX brief may begin; implementation PR requires all §2.2–§2.5 conditions satisfied
authored-by: PM Agent
authored-date: 2026-06-25
el-approved: 2026-06-25
release-branch: release/m17
sop-reference: docs/process/sprint-planning-sop.md
---

# Sprint Entry — M17, G3: Zone 1B Deconflict (Phase 3 Implementation)

**Status:** EL Approved 2026-06-25 — Phase 1 UX brief may begin; implementation PR requires all §2.2–§2.5 conditions satisfied
**Date authored:** 2026-06-25
**Release branch:** `release/m17`
**Sprint plan:** `docs/process/sprint-plans/m17-sprint-plan.md` (EL Approved 2026-06-25)

*Authority: `docs/process/sprint-planning-sop.md §Sprint Entry Gate` (Phase C output).
This entry gates G3 Phase 3 implementation only. G3 Phase 1 (UX brief — Zone 1B allocation
model, overflow handling, empty-state, viewport contract) and G3 Phase 2 (ADR authorship)
require NO sprint entry per sprint plan §G3 Phase 1 exception. This document must be fully
satisfied and EL-approved before the G3 Phase 3 implementation PR opens.*

*Per sprint plan §Wave 2 sequencing: #1250 (Zone 1B tablet legibility) must be merged to
`release/m17` before the G3 Phase 3 implementation PR opens — both touch Zone 1B layout and
cannot be in-flight concurrently. That merge dependency is a hard gate on the implementation
PR, not on this entry document's filing.*

---

## Section 1 — Sprint Identification

| Field | Value |
|---|---|
| Milestone | M17 — Calibration and Comparative Infrastructure |
| GitHub Milestone | #18 |
| Sprint group | G3 — Zone 1B Deconflict (Phase 3: Implementation) |
| Release branch | `release/m17` |
| Sprint plan document | `docs/process/sprint-plans/m17-sprint-plan.md` |
| Exit checklist issue | #982 |
| Sprint groups in scope | G3 Phase 3 only |
| ADR gate | **PENDING** — Architect determines at Phase 2 completion: ADR-017 amendment (ARCH-011 extension) or new ADR (ARCH-012). See §2.2. |
| Implementing agent | Frontend Engineer + QA Lead; Architect holds R on ADR determination |
| Wave | Wave 2 (gated on Wave 1 exit ✅ confirmed 2026-06-25) |
| Phase 3 implementation gate | **#1250 merged to `release/m17`** before implementation PR opens (FA constraint — Zone 1B layout conflict) |

**Phase 1 and Phase 2 prerequisite summary (must be complete before this entry can be EL-approved):**

| Prerequisite | Owner | Status |
|---|---|---|
| G3 Phase 1 complete: UX brief filed answering four allocation questions (proportional model, overflow handling, empty-state behavior, viewport contract) — at minimum a written specification with viewport-anchored decisions; mockup if proportional model is ambiguous at 1280×800 or 768px | UX Designer (R) + Design Thinking + Customer Agent | ⬜ NOT STARTED |
| G3 Phase 1 brief panel review: brief reviewed by Phase 1 panel before BPO acceptance — UX Designer confirms governing premises satisfied; Design Thinking confirms MDA primary instrument preserved; Customer Agent confirms Aicha/Lucas reading order is satisfied | UX Designer (R) + Design Thinking + Customer Agent + Business PO | ⬜ PENDING Phase 1 artifact |
| G3 Phase 1 BPO acceptance: BPO accepts Phase 1 brief output | Business PO | ⬜ PENDING panel review |
| G3 Phase 2 complete: Architect determines ADR path — ADR-017 amendment or new ARCH-012; ADR authored and accepted | Architect | ⬜ PENDING Phase 1 BPO + Wave 1 exit (✅ Wave 1 exited 2026-06-25) |
| Intent document filed for #1252 implementation (must reference accepted ADR and UX brief) | PM Agent | ⬜ PENDING Phase 1/2 |
| QA test file authored before implementation begins | QA Lead | ⚠️ EARLY FILED 2026-06-25 — `frontend/tests/e2e/m17-g3-zone-1b-allocation.spec.ts`; authored from sprint entry §2.4 ACs; pixel constants (MDA_PANEL_MIN_HEIGHT_PX, COHORT_MAX_DISPLAY) are placeholders pending ADR spec; update required when formal intent document is filed |
| #1250 merged to `release/m17` | G4 sprint group | ⬜ PENDING G4 |

---

## Section 2 — Entry Invariants Checklist

*All items must be checked before any G3 Phase 3 implementation PR opens.
Items marked PENDING are blocking — this entry may not be EL-approved until they are resolved.*

### 2.1 — Structural gates

- [x] **Release branch exists:** `release/m17` cut from `main` 2026-06-25 (commit d806957)
- [x] **CI trigger verified:** `.github/workflows/ci.yml` `pull_request: branches` includes
  `release/m*` — confirmed at M17 kickoff 2026-06-25. Ruleset ID 17751852 with 6 required checks:
  `changes`, `lint`, `test-backend`, `playwright-e2e`, `compliance-scan`, `branch-naming`.
  KI-005 permanent fix (`do_not_enforce_on_create: true`) applied 2026-06-20 — no Ruleset workaround required.
- [x] **Sprint plan EL-approved:** `docs/process/sprint-plans/m17-sprint-plan.md`
  `el-approved: 2026-06-25` (recorded 2026-06-25)

**Structural gates: CLEAR.** All three checked.

### 2.2 — ADR prerequisite gate

*Authority: sprint plan §ADR backlog review and §Architect — ADR prerequisites (downstream of UX)*

The ADR determination for G3 Phase 3 is PENDING and depends on Phase 1 UX brief acceptance
and Phase 2 Architect assessment. The sprint plan identifies two possible outcomes:

- **Path A — ADR-017 amendment (ARCH-011 extension):** If Zone 1B proportional allocation
  is a direct extension of the Zone 1A information architecture decision (ADR-017 governs
  Zone 1A encoding hierarchy, proportional allocation is a consistent layout expression of
  the same governing premise — primary instrument visible at all times), the Architect may
  determine that an amendment to ADR-017 is the correct form. ARCH-011 is the assigned number.
  The amendment must be accepted before Phase 3 begins.

- **Path B — New ADR (ARCH-012):** If Zone 1B proportional allocation requires standalone
  architectural decision-making — e.g., because the overflow contract, scroll container
  architecture, or max-cohort-display constraint represents a new architectural decision not
  derivable from ADR-017 — the Architect files ARCH-012 in the ADR backlog and authors a new
  ADR. ARCH-012 must be assigned from the backlog before drafting (per CLAUDE.md §No significant
  feature without an ADR). Implementation may not open until the new ADR is accepted.

Neither path can be determined until Phase 1 UX brief is produced, panel-reviewed, and
BPO-accepted, and Phase 2 Architect assessment completes. The Phase 1 brief's answer to the
four allocation questions (proportional model, overflow handling, empty-state, viewport
contract) is the direct input to the Architect's ADR scope determination.

**Standing constraint:** The temporary `minHeight: 80px` guarantee on the MDA panel wrapper
(introduced as a Demo 6 immediate fix, PR #1235) must not be treated as accepted architecture.
G3 Phase 3 must replace this temporary constraint with an ADR-grounded allocation model.
The implementation PR may not merge with `minHeight: 80px` as the sole Zone 1B allocation
mechanism — the ADR-grounded model must be in place.

- [ ] **ADR prerequisite gate: PENDING** — Phase 1 UX brief and Phase 2 Architect determination
  required; cannot be resolved until Phase 1 brief is filed, panel-reviewed, and BPO-accepted

**ADR prerequisite status (at filing; to be updated at Phase 2 completion):**

| Group | Required ADR | ADR status | Gate |
|---|---|---|---|
| G3 Phase 3 — #1252 (Zone 1B proportional allocation model) | Path A: ADR-017 amendment (ARCH-011) / Path B: ARCH-012 (new ADR) | Pending Phase 2 Architect determination | **PENDING — BLOCKING** |
| G3 Phase 3 — #1252 (Zone 1B overflow handling contract) | Included in same ADR as allocation model (same decision unit) | Pending Phase 2 determination | **PENDING** |
| G3 Phase 3 — #1252 (Zone 1B empty-state behavior) | Likely covered by same ADR; simple enough to not require standalone entry | Pending Phase 2 determination | **PENDING** |

*These entries must be updated to CLEAR or BLOCKED_ADR before EL approval of this entry.*

### 2.3 — Intent document gate

*For #1252 (G3 Phase 3 implementation), an intent document must be filed at
`docs/process/intents/M17-G3-{YYYY-MM-DD}-zone-1b-proportional-allocation.md` before the
implementation PR opens. The QA Lead must be able to write tests from it without reading
implementation code.*

- [ ] **Intent document gate: PENDING** — intent document cannot be authored until Phase 1
  UX brief is complete, panel-reviewed, and BPO-accepted, AND Phase 2 ADR is accepted. The
  intent document's acceptance criteria are derived from the UX brief's four allocation
  decisions and the ADR's implementation contract. **The intent document must reference the
  accepted ADR as the authoritative architectural specification and the UX brief as the
  authoritative visual/interaction specification — QA Lead writes assertions against the
  brief-defined and ADR-grounded observable states, not against implementation inference.**

**Intent document content requirements (to be satisfied at filing):**

The intent document for #1252 Phase 3 must specify, at minimum:

1. **Proportional model (UX brief Question 1):** The chosen allocation scheme — static pixel
   split (e.g., MDA panel fixed height / Cohort takes remainder with internal scroll), dynamic
   proportional split (e.g., 60/40 or ADR-specified ratio), or separate scrollable sub-zones.
   Observable state: at a defined breakpoint (1280×800), the MDA alert panel occupies a named
   pixel height and the CohortImpactSection occupies a named pixel height. Both are visible
   without scrolling the Zone 1B container.

2. **Overflow handling (UX brief Question 2):** The contract for when cohort crossings exceed
   the CohortImpactSection's allotted height. Observable state: if a scenario produces more
   cohort crossing entries than the section's max-display count — (a) they scroll internally
   within the Cohort section, or (b) they are truncated to max-N with a count label ("and N
   more"), or (c) another ADR-specified behavior — the MDA alert panel remains at its allotted
   height. The MDA panel must not collapse below `minHeight: 80px` under any cohort load —
   this is the regression guard from the M16 retrospective.

3. **Empty-state behavior (UX brief Question 3):** Observable state when Zone 1B has MDA
   breaches but no cohort crossings — MDA panel occupies full Zone 1B height or its defined
   allocation; CohortImpactSection is hidden or shows an empty state. Observable state when
   there are cohort crossings but no MDA breach — behavior as specified by the UX brief.

4. **Viewport contract (UX brief Question 4):** Minimum readable height for MDA panel and
   CohortImpactSection at 1024×768, 1280×800, and 1440×900. Observable state: both sections
   meet minimum height at each specified breakpoint; CohortImpactSection does not collapse
   MDA panel below minimum at any breakpoint. If the proportional split changes across
   breakpoints, each breakpoint's split is declared.

5. **Acceptance criteria — Persona 5 (Aicha Mbaye):** Aicha's use requires the MDA panel
   headline (severity label + indicator + distance below floor) to be visible without scrolling
   at 1280×800. Observable state: the MDA panel severity label and indicator are visible without
   any user interaction, regardless of how many cohort crossings are present, within Zone 1B's
   primary viewport position.

6. **Acceptance criteria — Persona 1 (Lucas Ferreira):** Lucas's use requires the CohortImpactSection
   to be fully readable, not truncated beyond the ADR-specified max-display count, at 1280×800.
   Observable state: the CohortImpactSection shows the ADR-specified number of cohort crossing
   entries; if more entries exist, a count label ("and N more") is visible and accessible.

7. **M16 retrospective regression guard:** Observable state: a scenario with 8+ cohort crossing
   entries does not cause the MDA alert panel wrapper to collapse to zero. The pre-implementation
   test must confirm this was a failure mode before the fix (red before implementation) and the
   post-implementation assertion confirms it does not occur.

| Deliverable | ADR reference | Intent document path | Filed? |
|---|---|---|---|
| #1252 — Zone 1B proportional allocation, Phase 3 implementation | TBD (Phase 2 output — Path A: ADR-017 amendment; Path B: ARCH-012) | `docs/process/intents/M17-G3-{YYYY-MM-DD}-zone-1b-proportional-allocation.md` | **No — BLOCKING** |

### 2.4 — QA test authorship gate

*QA tests must be authored from the intent document's acceptance criteria BEFORE implementation
code is written. The test file must be on record before the implementing agent begins.*

- [x] **QA test gate: EARLY FILED 2026-06-25** — `frontend/tests/e2e/m17-g3-zone-1b-allocation.spec.ts` authored from sprint entry §2.4 ACs (AC-A1, AC-A2, AC-A3, AC-A4, AC-P5, AC-P1); pixel constants (MDA_PANEL_MIN_HEIGHT_PX, COHORT_MAX_DISPLAY) are placeholders requiring update at Phase 3 handoff when formal intent document and ADR specifications are accepted; pre-implementation guard pattern applied to new G3 testids per NM-056

**QA test file requirements (to be satisfied at filing):**

The QA test file for G3 Phase 3 is an E2E Playwright test. It must assert, from the intent
document's acceptance criteria:

1. **AC-A1 (proportional model):** At 1280×800, the MDA alert panel occupies its ADR-specified
   minimum height and the CohortImpactSection is visible below it; neither section is zero-height.
   Assert via testid-anchored bounding box checks for both sections.

2. **AC-A2 (overflow regression guard):** A scenario with 8+ cohort crossing entries does not
   collapse the MDA panel below the ADR-specified minimum height. This assertion must be
   **red before implementation** (confirming the M16 failure mode existed before the fix) and
   green after. The test file must include a comment citing the M16 retrospective source
   (near-miss or retrospective document) as the regression evidence.
   **No soft-skip patterns permitted** (NM-056 guard: all assertions must be hard-fail).

3. **AC-A3 (viewport contract):** At 768px (tablet), both sections meet minimum readable height
   per UX brief specification; CohortImpactSection does not collapse MDA panel below minimum.
   Assert via testid-anchored bounding box checks at 768px viewport.

4. **AC-A4 (empty-state behavior):** When Zone 1B has MDA breaches but no cohort crossings,
   MDA panel is visible at full allocated height; CohortImpactSection shows its empty state.
   Assert both conditions via testid presence and bounding box.

5. **AC-P5 (Persona 5 — Aicha):** MDA panel severity label and indicator are visible without
   scrolling at 1280×800, regardless of cohort load. Assert via testid-anchored element
   visibility check after populating Zone 1B with a high-cohort-load scenario.

6. **AC-P1 (Persona 1 — Lucas):** CohortImpactSection shows the ADR-specified max-display
   count at 1280×800; if more entries exist, count label is visible. Assert via testid on
   cohort entry items and count label.

| Deliverable | Intent document | Test file path | Authored before implementation? |
|---|---|---|---|
| #1252 — Zone 1B proportional allocation | `docs/process/intents/M17-G3-{YYYY-MM-DD}-zone-1b-proportional-allocation.md` | `frontend/tests/e2e/m17-g3-zone-1b-allocation.spec.ts` | **Early — filed 2026-06-25 from sprint entry ACs; update required at Phase 3 handoff with formal intent doc pixel specs** |

### 2.5 — Phase 1 UX brief standards and panel review gate

*This section stipulates the minimum artifact requirements for G3 Phase 1 output and the
panel review that must pass before BPO acceptance and Phase 2 may begin.*

*Rationale for panel review gate: Pattern established in M17-G2 sprint entry §2.5 (design
artifact panel review required before BPO acceptance for design-led sprint phases). The
insights-log entry filed 2026-06-25 records this as a finding for SOP amendment at the next
HORIZON sweep. This entry applies the G2 precedent to G3 while the SOP amendment is pending.*

#### Artifact requirements

**Required — written UX brief:**

The UX brief is a written specification document that answers the four allocation questions
from the sprint plan (not a wireframe — the decision space is constrained enough that prose
plus annotated viewport measurements are the sufficient artifact form). The brief must:

| Question | Minimum specification required |
|---|---|
| Q1: Proportional model | Named allocation scheme with declared pixel heights at 1280×800; if dynamic, the rule for computing allocation at each supported breakpoint |
| Q2: Overflow handling | Named overflow behavior (internal scroll / truncate to max-N / expand-at-cost-of-MDA); if truncation, the max-N value; the regression condition statement ("MDA panel must not collapse below N pixels under any cohort load") |
| Q3: Empty-state behavior | Stated behavior for MDA-breach-only state and cohort-crossing-only state; stated behavior for neither populated (existing behavior) |
| Q4: Viewport contract | Named minimum heights for MDA panel and CohortImpactSection at 1024×768, 1280×800, and 1440×900; whether proportional split changes at each breakpoint |

A viewport-anchored mockup or annotated screenshot is required if — and only if — the
proportional model decision is ambiguous at 768px legibility (i.e., the prose specification
is insufficient to determine whether both sections meet minimum readable height without
rendering the layout). If produced, the mockup must be at 768px to resolve the specific
legibility question.

**Reading-order constraint (non-negotiable from sprint plan §Customer Agent — Zone 1B reading order):**

The brief must explicitly confirm that the chosen proportional model satisfies the reading
order constraint: MDA panel is the primary visual anchor (Aicha's use — headline visible first,
without scrolling), while the CohortImpactSection is fully readable without truncation at
the ADR-specified max-display count (Lucas's use — co-primary for detailed analysis). A
proportional model that resolves Zone 1B allocation but fails the reading-order constraint
is a REJECT at panel review.

#### Panel review — required before BPO acceptance

The Phase 1 brief panel reviews the written specification before BPO acceptance is requested.

**Panel composition:**

| Agent | Role in review | Minimum assessment required |
|---|---|---|
| UX Designer | R — review lead; confirms brief satisfies the five governing UX premises (CLAUDE.md §UX Architectural Commitments), specifically Premise 2 (instruments always visible; no primary instrument lives behind a click or scroll) | Sign-off confirming all four questions are answered; Premise 2 satisfied at 1280×800 and 768px; no governing premise violated |
| Design Thinking Agent | Cognitive task validation — confirms Zone 1B dual-occupant state preserves the primary cognitive task (threshold breach evidence) with the MDA panel as primary instrument; CohortImpactSection as supplementary | Verdict: does the proportional model keep the MDA alert panel's severity headline visible without scrolling, under the maximum expected cohort load? |
| Customer Agent | Persona accessibility — confirms (a) Aicha (Persona 5) can read the MDA headline without scrolling at 1280×800; (b) Lucas (Persona 1) can read the full CohortImpactSection content at the ADR-specified display count without the section being truncated below his minimum usable state | Pass/fail verdict for each persona; any FAIL triggers a REJECT and brief revision |
| Business PO | Acceptance — reviews panel verdicts and issues formal Phase 1 BPO acceptance; confirms the brief produces a Zone 1B allocation that serves the Demo 7 Senegal scenario without Zone 1B becoming a demo legibility risk | ACCEPT / REJECT verdict; ACCEPT required before Phase 2 begins |

**Panel review format:**

Each panel member records their verdict as a comment on GitHub issue #1252. The UX Designer
collects the verdicts and produces a panel summary comment on #1252 before PM Agent routes to
BPO for formal acceptance. **The panel summary comment must explicitly tag the PM Agent
(@PublicEnemage) — a summary comment without this tag does not constitute a routing signal
and PM Agent is not obligated to act on it.** The panel summary must record:

- Count of panel members who reviewed
- Any REJECT verdict and the specific concern raised
- Whether a viewport-anchored mockup was produced, and if not, why prose specification was sufficient
- Whether any panel member identified a design ambiguity that must be resolved in Phase 2
  (these ambiguities become explicit inputs to the Architect's ADR authorship)

**Panel review fail condition:**

If any panel member issues a REJECT verdict, the brief must be revised and re-reviewed before
BPO acceptance is requested. The PM Agent does not route to BPO until all panel verdicts are
PASS (or the rejecting agent explicitly marks their concern resolved after revision). A BPO
acceptance issued without all panel verdicts on record is non-compliant and the PI Agent
blocks Phase 2 from opening.

- [ ] **Phase 1 UX brief panel review: PENDING** — brief not yet produced; panel cannot convene
  until all four allocation questions are answered and filed on #1252

---

## Section 3 — Scope Declaration

### 3.1 — Issues in scope

| Issue | Title | Priority | Observable application state |
|---|---|---|---|
| #1252 | arch(zone-1b): Zone 1B proportional allocation — MDA alert vs cohort sections | Medium — ADR-gated; demo-quality improvement | At 1280×800: Zone 1B shows MDA alert panel (severity label + indicator + distance-below-floor) and CohortImpactSection simultaneously, each occupying a declared proportional allocation, with neither section collapsed to zero under maximum cohort load. MDA panel is visible without scrolling. A scenario with 8+ cohort entries does not collapse the MDA panel (M16 retrospective regression resolved). At 768px: both sections meet minimum readable height per UX brief viewport contract. |

**Minimum viable Phase 3 scope:**

The entire scope of #1252 is required — there is no sub-scope cut order, because the
proportional allocation model is atomic: it either resolves the Zone 1B dual-occupant conflict
or it does not. The M16 retrospective overflow regression fix is non-negotiable (it is the
primary motivation for the issue). The viewport contract (Q4) is the Demo 7 legibility gate —
the Zone 1B must be legible at 768px per DEMO6-026/043 context.

**If Phase 3 implementation cannot complete before M17 closes:** Phase 1 and Phase 2 artifacts
(UX brief + accepted ADR) are the M17 G3 deliverables. The `minHeight: 80px` temporary
guarantee remains in place through Demo 7 as documented in the sprint plan. BPO assesses
the design and architecture artifacts at M17 close if implementation has not shipped; implementation
carries to M18 with this entry document remaining active.

### 3.2 — Issues explicitly out of scope

| Issue / scope | Rationale for exclusion |
|---|---|
| #1250 — Zone 1B tablet legibility (G4) | G4 sprint group; must merge before G3 Phase 3 to avoid Zone 1B layout conflicts; #1250 resolves font/sizing at 768px, not the proportional allocation architecture |
| #1249/#1253/#1239 — other DEMO6 CRITICAL fixes (G4) | Separate sprint group; no Zone 1B overlap except #1250 |
| #394 — multi-scenario Zone 1B per-scenario threshold crossings (G2) | G2 sprint group; Zone 1B in comparison mode is G2 Phase 3 scope; G3 must not introduce proportional allocation constraints that break the G2 per-scenario threshold crossing layout. G3 ADR must acknowledge the G2 Zone 1B extension as a downstream consumer and confirm the ADR-grounded allocation model is compatible with per-scenario data. |
| #1220/#1214/#1251 — infrastructure (G5) | Separate sprint group; no Zone 1B overlap |
| Mode 3 Zone 1B behavior | M18 scope; Mode 3 instrument layout will reference the G3 ADR for Zone 1B allocation |

---

## Section 4 — ADR Prerequisite Summary

*To be updated at G3 Phase 2 completion. Architect records the ADR determination here before
this entry can be EL-approved.*

| Group | ADR required | ADR status | Implementation may begin? |
|---|---|---|---|
| G3 Phase 3 — #1252 (Zone 1B proportional allocation + overflow contract + empty-state) | Path A: ADR-017 amendment (ARCH-011) / Path B: new ADR (ARCH-012) | **PENDING Phase 2 Architect determination** | **No — awaiting Phase 1 BPO acceptance + Architect Phase 2 output** |

**Phase 2 Architect output required before EL approval:**

The Architect must file a determination note on GitHub issue #1252 answering:

1. Does the Zone 1B proportional allocation decision constitute an extension of ADR-017
   (Zone 1A information architecture — ARCH-011) or a standalone architectural decision
   requiring its own ADR (ARCH-012)? Criteria: if the proportional model is a direct
   expression of the governing premise already established in ADR-017 (primary instrument
   always visible — Premise 2 from CLAUDE.md §UX Architectural Commitments), an amendment
   may suffice. If the overflow contract, scroll container architecture, or max-cohort-display
   constraint represents a new decision not derivable from ADR-017's premises, a new ADR is required.

2. Does the ADR need to address the G2 Phase 3 compatibility constraint (per-scenario Zone 1B
   threshold crossings in comparison mode)? The allocation model must be compatible with the
   G2 data contract for per-scenario crossings. If G2 Phase 3 is expected to require Zone 1B
   structural changes beyond the G3 proportional model, the ADR should declare the forward
   compatibility constraint explicitly rather than leaving it to the G2 implementation.

3. Is the `minHeight: 80px` temporary guarantee (PR #1235) formally superseded by the ADR?
   The ADR must include an explicit statement replacing the temporary guarantee with the
   permanent allocation contract, so there is no ambiguity about which constraint governs
   Zone 1B layout post-G3.

**Phase 3 implementation sequencing (once ADR gate cleared):**

1. EL approves this entry document (requires Phase 1 BPO acceptance + Phase 2 Architect ADR acceptance + intent document filed + QA tests authored)
2. Confirm #1250 is merged to `release/m17` (FA hard gate — Zone 1B conflict prevention)
3. Cut feature branch: `feat/m17-g3-zone-1b-allocation` from `release/m17`
4. Frontend: implement Zone 1B proportional allocation per ADR spec; replace `minHeight: 80px` temporary constraint with ADR-grounded allocation model
5. Pre-push build gate: `cd frontend && npm run build` (TypeScript errors are a compliance finding per CLAUDE.md §Frontend pre-push build gate)
6. E2E tests pass: `m17-g3-zone-1b-allocation.spec.ts` — all AC assertions pass; overflow regression guard red-before-green confirmed; no soft-skips (NM-056 guard)
7. Business PO acceptance and Customer Agent Layer 3 (Persona 5 — Aicha, Persona 1 — Lucas) — required at exit

---

## Section 5 — Near-Miss Sweep

**Near-miss sweep date:** 2026-06-25
**Sweep period:** G2 sprint entry filing (2026-06-25) through G3 sprint entry filing (2026-06-25)

| Finding | Category | PI Agent register call issued? | NM entry number |
|---|---|---|---|
| Insights log entry (2026-06-25): G2 §2.5 panel review pattern (UX mockup minimum, panel review, PM Agent tag) is not yet in sprint-planning-sop.md — applied here by precedent; SOP amendment pending | N/A — open finding in insights-log.md; recorded for PM Agent to promote to SOP amendment issue at next HORIZON sweep | N/A — not yet a process gap (SOP amendment is the correct path; G3 applies the pattern proactively) | N/A |
| No other process gaps identified in the sweep period. | N/A | N/A | N/A |

**PM Agent HORIZON sweep note:**

At the next HORIZON sweep, PM Agent must:
1. Promote the insights-log.md UX panel review finding (filed 2026-06-25) to a GitHub issue
   for a `sprint-planning-sop.md` amendment — the §2.5 design artifact panel review gate should
   be formal SOP, not a per-sprint-entry convention. Both G2 and G3 have now applied it; the
   pattern is proven and should be codified. (Note: #1277 was filed from insights log entry 13
   for this SOP amendment — confirm that #1277 covers this or file a new issue if scope differs.)
2. File the two Wave 2 issues from G1 governance sensitivity specification §Summary:
   (a) SEN `institutional_capacity_index` seed + GovernanceElasticity co-gated PR;
   (b) Zone 1D tooltip — governance divergence horizon disclosure.
   (Carried from G1 sprint exit PI Agent confirmation — not blocking G3; recorded here for
   traceability. Note: #1275 and #1276 were filed at the HORIZON sweep 2026-06-25 — confirm
   these issues are assigned to correct M17 groups.)

---

## EL Approval Record

**EL approval:** Approved 2026-06-25

*The structural gates (§2.1) are CLEAR. The remaining PENDING conditions (§2.2 ADR gate,
§2.3 intent document, §2.4 QA tests, §2.5 panel review) must be satisfied before any
Phase 3 implementation PR opens — EL approval of this entry document does not substitute
for those per-phase gates. Phase 1 (UX brief) may begin immediately.*

> G3 sprint entry approved. Phase 1 UX brief (Zone 1B allocation brief — four questions:
> proportional model, overflow handling, empty-state behavior, viewport contract) may begin.
> Implementation PR may not open until §2.2–§2.5 are satisfied.
> — @PublicEnemage (2026-06-25)
