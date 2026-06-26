---
name: m17-g4-sprint-entry
type: sprint-entry
milestone: M17 — Calibration and Comparative Infrastructure
sprint-group: G4 — DEMO6 CRITICAL Polish
status: EL Approved 2026-06-25 — UX visual specs may begin; #1239 intent document and QA
  test may be filed immediately; no implementation PR may open until per-issue gates are met
authored-by: PM Agent
authored-date: 2026-06-25
el-approved: 2026-06-25
release-branch: release/m17
sop-reference: docs/process/sprint-planning-sop.md
---

# Sprint Entry — M17, G4: DEMO6 CRITICAL Polish

**Status:** EL Approved 2026-06-25 — UX Designer may begin visual specs (#1249 first per FA sequence); #1239 intent document and QA test may be filed immediately; no implementation PR may open until per-issue gates are met
**Date authored:** 2026-06-25
**Release branch:** `release/m17`
**Sprint plan:** `docs/process/sprint-plans/m17-sprint-plan.md` (EL Approved 2026-06-25)

*Authority: `docs/process/sprint-planning-sop.md §Sprint Entry Gate` (Phase C output).
G4 covers four DEMO6 findings that must be resolved before the live Demo 7 session is
scheduled: #1249 (Zone 1A curve identifiability), #1250 (Zone 1B tablet legibility at 768px),
#1253 (Zone 1D PSP historical precedent anchor), and #1239 (Zone 1B inverted floor label bug).*

*G4 has a per-issue gate structure authorized in the sprint plan §G4 UX visual spec gate: for
each DEMO6 CRITICAL issue (#1249, #1250, #1253), the UX Designer's before/after visual spec
must exist before that issue's implementation PR opens. The visual spec is a per-issue
pre-condition on the implementation PR, not on this sprint entry document. #1239 (inverted
label — clear bug fix) requires no visual spec and proceeds to implementation once this entry
is EL-approved and its intent document and QA test are filed. Single sprint entry covers all
four issues. FA-recommended implementation sequence: #1249 → #1253 → #1250 → #1239.*

---

## Section 1 — Sprint Identification

| Field | Value |
|---|---|
| Milestone | M17 — Calibration and Comparative Infrastructure |
| GitHub Milestone | #18 |
| Sprint group | G4 — DEMO6 CRITICAL Polish |
| Release branch | `release/m17` |
| Sprint plan document | `docs/process/sprint-plans/m17-sprint-plan.md` |
| Exit checklist issue | #982 |
| Sprint groups in scope | G4 only |
| Issues in scope | #1249, #1250, #1253, #1239 |
| ADR gate | N/A — all G4 fixes are within existing zone architecture (ADR-017 governs zone layout; no structural changes required) |
| Implementing agents | UX Designer (visual specs); Frontend Engineer (implementation); QA Lead (test authorship) |
| Wave | Wave 2 (Wave 1 exit confirmed 2026-06-25 — `docs/process/sprint-plans/m17-g1-sprint-exit.md`) |
| Demo dependency | All four issues required before live Demo 7 session is scheduled (#843, M18) |

**Per-issue gate summary:**

| Issue | Title | Visual spec required? | Sequence position |
|---|---|---|---|
| #1249 | Zone 1A curve identifiability | Yes — UX Designer before/after mockup at 1280×800 | 1st |
| #1253 | Zone 1D PSP historical precedent anchor | Yes — UX Designer layout spec (inline/collapsible/tooltip decision) | 2nd |
| #1250 | Zone 1B tablet legibility at 768px | Yes — UX Designer font-size and layout spec at 768px | 3rd |
| #1239 | Zone 1B inverted floor label | No — clear bug fix; intent document + QA test only | 4th |

---

## Section 2 — Entry Invariants Checklist

*All structural gates must be confirmed before any G4 implementation PR opens.
Per-issue conditions (UX visual spec → intent document → QA test) apply sequentially
per the FA-recommended implementation sequence — each issue's gates must be met before
that issue's implementation PR opens. An unchecked structural invariant blocks all G4
implementation. An unchecked per-issue condition blocks that issue's implementation PR.*

### 2.1 — Structural gates

- [x] **Release branch exists:** `release/m17` cut from `main` 2026-06-25 (commit d806957)
- [x] **CI trigger verified:** `.github/workflows/ci.yml` `pull_request: branches` includes
  `release/m*` — confirmed at M17 kickoff 2026-06-25. Required checks: `changes`, `lint`,
  `test-backend`, `playwright-e2e`, `compliance-scan`, `branch-naming`.
  KI-005 permanent fix (`do_not_enforce_on_create: true`) applied 2026-06-20 — no Ruleset
  workaround required.
- [x] **Sprint plan EL-approved:** `docs/process/sprint-plans/m17-sprint-plan.md`
  `el-approved: 2026-06-25` (recorded 2026-06-25)
- [x] **Wave 1 exit gate confirmed:** G1 sprint exit document at
  `docs/process/sprint-plans/m17-g1-sprint-exit.md`; PI Agent confirmation on record
  2026-06-25; Wave 2 implementation sprint entries unblocked

**Structural gates: CLEAR.** All four checked.

### 2.2 — ADR prerequisite gate

*G4 issues are UX polish fixes and a bug fix within the existing zone architecture established
by ADR-017 (Zone 1A information architecture, ARCH-011, accepted M16). No G4 issue introduces
a new zone, a new data contract, a new encoding scheme, or a new component boundary. Each fix
is an implementation refinement within the boundaries already decided:*

- **#1249** (Zone 1A curve identifiability): adds terminal endpoint labels or line-style
  differentiation to existing compare-mode curve rendering. Zone 1A rendering path and
  compare-mode overlay are ADR-017 scope. The fix is an encoding addition within the existing
  path — not a structural change. No ADR amendment required.

- **#1250** (Zone 1B tablet legibility): adjusts font sizes and layout reflow at 768px for
  existing Zone 1B cohort rows. Zone 1B component layout is ADR-017 scope. Responsive
  breakpoint tuning is not an architectural decision. No ADR amendment required.

- **#1253** (Zone 1D PSP historical precedent anchor): adds a content element (comparable
  programme reference) to the existing Zone 1D PSP severity surface. Zone 1D component
  exists; this is a content addition within its layout. The data source (PSP comparable
  programme reference) is a display-layer addition. No ADR amendment required.

- **#1239** (Zone 1B inverted floor label): bug fix correcting label semantics in Zone 1B
  distance display. No architectural implication. No ADR amendment required.

*Constraint for #1249 at implementation:* The identifiability scheme chosen by the UX Designer
must be validated at N=3 (not only N=2) per the sprint plan §UX Designer — G4 DEMO6 CRITICAL
visual spec requirement. A solution that solves N=2 but requires rework at N=3 (when G2 Phase 3
implements multi-scenario comparison) is not acceptable. The implementing agent must confirm
N=3 visual compatibility in the Step 4 Verify verdict before the #1249 PR merges.

**ADR prerequisite status:**

| Issue | Required ADR | ADR status | Gate |
|---|---|---|---|
| #1249 — Zone 1A curve identifiability | None — encoding addition within ADR-017 Zone 1A compare-mode boundary | N/A | **CLEAR** |
| #1250 — Zone 1B tablet legibility at 768px | None — responsive tuning within ADR-017 Zone 1B boundary | N/A | **CLEAR** |
| #1253 — Zone 1D PSP historical precedent anchor | None — content addition within ADR-017 Zone 1D boundary | N/A | **CLEAR** |
| #1239 — Zone 1B inverted floor label | None — bug fix | N/A | **CLEAR** |

- [x] **ADR prerequisite gate: CLEAR.** No new ADR required for any G4 issue.

### 2.3 — Intent document gate

*For each G4 issue, an intent document must be filed before that issue's implementation PR
opens. (Authority: `docs/process/agent-execution-lifecycle.md` Step 1)*

*For #1249, #1250, and #1253: the intent document may not be authored until the UX Designer's
visual spec for that issue exists. The intent document must include or reference the approved
UX visual spec as the binding specification — QA Lead writes assertions against the
spec-defined observable states, not against implementation inference.*

*For #1239: no UX visual spec is required. The intent document documents the defect, the
correct label behavior, and the observable state. It may be filed immediately.*

- [ ] **Intent document gate for #1249 — PENDING** UX visual spec (per-issue gate; not blocking this entry)
- [ ] **Intent document gate for #1253 — PENDING** UX visual spec (per-issue gate; not blocking this entry)
- [ ] **Intent document gate for #1250 — PENDING** UX visual spec (per-issue gate; not blocking this entry)
- [x] **Intent document gate for #1239 — FILED** 2026-06-25 — `docs/process/intents/M17-G4-2026-06-25-zone-1b-inverted-floor-label.md`

**Intent document paths (to be filed per issue, in FA-recommended sequence):**

| Issue | UX visual spec pre-condition | Intent document path | Filed? |
|---|---|---|---|
| #1249 — Zone 1A curve identifiability | UX Designer before/after mockup at 1280×800 + 768px, N=2 and N=3 validation | `docs/process/intents/M17-G4-{date}-zone-1a-curve-identifiability.md` | **No — PENDING visual spec** |
| #1253 — Zone 1D PSP historical precedent anchor | UX Designer layout decision (inline/collapsible/tooltip) with Zone 1D density spec | `docs/process/intents/M17-G4-{date}-zone-1d-psp-precedent.md` | **No — PENDING visual spec** |
| #1250 — Zone 1B tablet legibility at 768px | UX Designer font-size and reflow spec at 768px, testid-anchored layout description | `docs/process/intents/M17-G4-{date}-zone-1b-tablet-legibility.md` | **No — PENDING visual spec** |
| #1239 — Zone 1B inverted floor label | None | `docs/process/intents/M17-G4-2026-06-25-zone-1b-inverted-floor-label.md` | **Yes — filed 2026-06-25** |

**Intent document content requirements (minimum per issue):**

**#1249 — Zone 1A curve identifiability:**
1. The differentiation scheme chosen (terminal endpoint labels, dashed/solid line-style, or
   combination) — referencing the UX visual spec as the binding specification.
2. Observable state at N=2: each trajectory curve is identifiably distinct at 1280×800
   without hovering.
3. N=3 compatibility: the same scheme must work for three trajectories without modification
   (G2 Phase 3 builds on this fix per FA sequencing constraint).
4. Persona acceptance criterion — Lucas Ferreira (Persona 1): can identify which trajectory
   belongs to which scenario without hovering, at 1280×800.
5. Regression guard: existing single-scenario Zone 1A rendering is unaffected.

**#1253 — Zone 1D PSP historical precedent anchor:**
1. Surface approach (inline/collapsible/tooltip) — referencing the UX visual spec as binding.
2. Content requirements: comparable programme reference must include enough information for
   Andreas Petrakis (Persona 3) to cite a comparable case with a known compliance outcome in
   a political brief without additional interaction.
3. Observable state: the reference is readable without hover or click at 1280×800.
4. Zone 1D layout impact: the addition does not collapse or obscure existing PSP severity label.
5. Regression guard: existing Zone 1D content (PSP severity, entity attribution) is unaffected.

**#1250 — Zone 1B tablet legibility at 768px:**
1. Minimum font sizes — referencing the UX visual spec as binding: current value, floor, and
   T3 badge at 768px viewport width.
2. Layout reflow specification (if any): whether the badge moves below the value row or scales.
3. Observable state: all three elements (current value, floor, badge) are readable without
   zoom at 768px.
4. Testid-anchored layout description: the QA Lead can write assertions against element
   minimum sizes from this spec.
5. Regression guard: Zone 1B layout at 1280×800 (primary presentation viewport) is unaffected.

**#1239 — Zone 1B inverted floor label:**
1. Defect description: Zone 1B distance display shows semantically incorrect label when an
   indicator value is below the MDA floor threshold (DEMO6-010 finding — "above floor" shown
   when the value is below the floor).
2. Correct behavior: when value < floor, label reads "below floor" (or equivalent correct
   formulation); when value ≥ floor, label reads "above floor" (or equivalent).
3. Observable state: for the Greece backtesting fixture at Step 1 (where Q1 poverty headcount
   is above the floor threshold), Zone 1B shows the correct above/below label. For a Senegal
   T3 conditionality scenario where Q1 crosses the floor, Zone 1B shows "below floor" at the
   crossing step.
4. Regression guard: existing floor distance numeric display is unaffected; label fix is
   isolated to the boolean above/below display.

### 2.4 — QA test authorship gate

*QA tests must be authored from the intent document's acceptance criteria before implementation
code is written. The test file must be on record before the implementing agent begins.
(Authority: `docs/process/agent-execution-lifecycle.md` Step 2)*

*Per-issue: QA test authorship is gated on the intent document for that issue being filed.
The test authorship gate applies in FA-recommended sequence: QA tests for #1249 before
#1249 implementation begins; then tests for #1253; then #1250; then #1239.*

- [ ] **QA test gate for #1249 — PENDING** intent document (per-issue gate; not blocking this entry)
- [ ] **QA test gate for #1253 — PENDING** intent document (per-issue gate; not blocking this entry)
- [ ] **QA test gate for #1250 — PENDING** intent document (per-issue gate; not blocking this entry)
- [x] **QA test gate for #1239 — FILED** 2026-06-25 — `frontend/tests/e2e/m17-g4-demo6-critical-polish.spec.ts` #1239 describe block (AC-1239-1, AC-1239-2, AC-1239-R)

**QA test file structure (single E2E Playwright test file covers all G4 issues):**

`frontend/tests/e2e/m17-g4-demo6-critical-polish.spec.ts`

Each issue has a dedicated `describe` block. The file grows sequentially as each issue's
intent document is filed and QA tests are authored. The complete file is present before any
G4 implementation PR merges.

*Assertions required per issue describe block:*

**#1249 describe block — Zone 1A curve identifiability:**
- AC-1249-1: In compare mode with two scenarios active, each Zone 1A trajectory curve has
  a distinct visual identifier (terminal label or line-style per UX spec) at 1280×800 viewport.
- AC-1249-2: The identifiers are present without hover interaction.
- AC-1249-3 (N=3 guard): With three scenario trajectories active, all three curves remain
  identifiably distinct without hover — the differentiation scheme scales to N=3.
- AC-1249-R: Single-scenario Zone 1A rendering is unaffected (non-regression).

**#1253 describe block — Zone 1D PSP historical precedent anchor:**
- AC-1253-1: Zone 1D shows the PSP comparable programme reference in the location specified
  by the UX visual spec (inline/collapsible/tooltip).
- AC-1253-2: The reference content is readable without hover or click at 1280×800.
- AC-1253-3: Zone 1D existing PSP severity label and entity attribution remain visible and
  unaffected (non-regression).

**#1250 describe block — Zone 1B tablet legibility at 768px:**
- AC-1250-1: At 768px viewport width, Zone 1B cohort row elements (current value, floor,
  tier badge) are each at or above the minimum font size specified in the UX visual spec.
- AC-1250-2: Elements are readable without zoom (no horizontal scroll of Zone 1B content).
- AC-1250-3: At 1280×800 viewport, Zone 1B layout is unaffected by the 768px fix
  (non-regression at primary presentation viewport).

**#1239 describe block — Zone 1B inverted floor label:**
- AC-1239-1: For a scenario where an indicator value is below the MDA floor, Zone 1B
  displays "below floor" (or the correct formulation per intent document).
- AC-1239-2: For a scenario where an indicator value is above the MDA floor, Zone 1B
  displays "above floor" (or the correct formulation per intent document).
- AC-1239-R: Floor distance numeric display is unaffected (non-regression).

**No soft-skip patterns permitted** (NM-056 guard): All assertions must be hard-fail. No
`test.skip()`, `test.fixme()`, or `.only()` without an NM entry authorizing the skip. The
G4 test file must not import or use the soft-skip pattern from the G3 spec (NM-061 upstream;
#1220 is G5 scope — the G3 soft-skip is a known infrastructure bug, not a template).

### 2.5 — Per-issue UX visual spec gate

*Authority: `docs/process/sprint-plans/m17-sprint-plan.md §G4 UX visual spec gate` and
`§UX Designer — G4 DEMO6 CRITICAL visual spec requirement`. This section is G4-specific —
it has no equivalent in the standard sprint entry template.*

*For each DEMO6 CRITICAL issue (#1249, #1250, #1253), the UX Designer must produce a
before/after visual spec before that issue's implementation PR opens. The spec is a
constrained visual decision — lighter than a design sprint. Each spec takes one session to
produce. The sprint plan specifies minimum content per issue:*

- [ ] **#1249 UX visual spec — PENDING:**
  - Before/after annotated mockup at presentation scale (1280×800 at 80% zoom, the IR review
    audience simulation condition)
  - Decision: terminal endpoint labels, dashed/solid line-style differentiation, or combination
  - N=3 validation: the chosen scheme must differentiate three curves without modification
    (G2 Phase 3 dependency; a solution that solves N=2 but fails N=3 is not acceptable)
  - Filed as a comment on GitHub issue #1249 or as a document at `docs/ux/specs/` (UX Designer chooses)

- [ ] **#1253 UX visual spec — PENDING:**
  - Layout decision: inline text below PSP severity label, collapsible section, or tooltip on severity chip
  - Zone 1D density check at 1280×800 — the spec must confirm the addition does not crowd
    existing Zone 1D content at presentation viewport
  - Design Thinking input: Andreas (Persona 3) needs the reference citation-ready and
    immediately readable — not hidden behind an interaction
  - Filed as a comment on #1253 or as a document at `docs/ux/specs/`

- [ ] **#1250 UX visual spec — PENDING:**
  - Minimum font sizes at 768px: current value, floor, and tier badge — expressed in measurable
    terms (e.g., minimum 14px body, minimum 12px label)
  - Layout reflow specification: whether badge moves below value row or elements scale
  - Testid-anchored layout description that the QA Lead can use to write size assertions
  - Filed as a comment on #1250 or as a document at `docs/ux/specs/`

**UX visual spec filing order:** The sprint plan and FA sequencing recommend specs be produced
in the same order as implementation: #1249 first, then #1253, then #1250. The UX Designer may
produce all three in a single session or sequentially — as long as each spec precedes its
issue's intent document filing and implementation PR.

**#1239 exception:** No UX visual spec required. The correct label behavior is unambiguous
(the defect is "above floor" shown when value is below floor). Intent document and QA test
proceed without a visual spec.

### 2.6 — Wave 2 dependency gate

*The sprint plan §Wave structure places G4 in Wave 2, blocked on Wave 1 exit. Wave 1 exit
was confirmed 2026-06-25. This gate is satisfied.*

- [x] **Wave 1 exit gate: CONFIRMED 2026-06-25**
  G1 sprint exit document: `docs/process/sprint-plans/m17-g1-sprint-exit.md`
  PI Agent confirmation: CONFIRMED — all Wave 1 exit conditions satisfied (BPO ACCEPT on
  #1229 and #1248; FRAME-D CI test passing; governance sensitivity specification on record)
  Session state: "Wave 2 implementation sprint entries now unblocked" (SESSION_STATE.md
  2026-06-25)

**Wave 2 gate: CLEAR.**

---

## Section 3 — Scope Declaration

### 3.1 — Issues in scope

*Observable application states are pre-implementation specifications. All must be confirmed
in the running application at Step 4 Verify before each issue's implementation PR may merge.
Observable states for #1249, #1250, #1253 are subject to revision when UX visual specs are
produced — the spec takes precedence over any presumed detail below.*

| Issue | Title | Priority | Observable application state |
|---|---|---|---|
| #1249 | ux(zone-1a): DEMO6-014 curve identifiability | **DEMO6 CRITICAL** | In Zone 1A compare mode with two scenarios active at 1280×800, each trajectory curve is identifiably distinct without hovering or clicking. The differentiation scheme (terminal endpoint labels or line-style per UX visual spec) makes scenario identity readable at glance level. The scheme must scale to N=3 without modification — with three trajectory curves active, all three are distinguishable. The FRAME-D milestone sentence, if visible in compare mode, identifies its scenario correctly. Single-scenario Zone 1A rendering is unaffected. |
| #1253 | ux(zone-1d): DEMO6-040 PSP historical precedent anchor | **DEMO6 CRITICAL** | Zone 1D shows a comparable programme reference adjacent to or below the PSP severity label. The reference is readable without hover or click at 1280×800. The reference contains enough information for Andreas Petrakis (Persona 3) to cite a comparable case (programme name, compliance outcome) in a political brief without additional navigation. Zone 1D existing content — PSP severity label, entity attribution — remains visible and unaffected. Zone 1D layout at 1280×800 does not overflow or crowd with the reference present. |
| #1250 | ux(zone-1b): DEMO6-026/043 tablet legibility at 768px | **DEMO6 CRITICAL** | At 768px viewport width, Zone 1B cohort impact section displays current value, MDA floor, and tier badge (e.g., T3) at or above the minimum font sizes specified in the UX visual spec — readable without zoom. No Zone 1B element requires horizontal scroll at 768px. Zone 1B layout at 1280×800 (primary presentation viewport) is unaffected — the responsive fix does not alter the primary viewport rendering. |
| #1239 | ux(zone-1b): DEMO6-010 inverted floor label — "above floor" when below | Bug | When an indicator value is below the MDA floor threshold, Zone 1B displays the semantically correct label (e.g., "below floor"). When an indicator value is at or above the floor, Zone 1B displays the semantically correct label (e.g., "above floor"). The label correctly reflects the below/above relationship in all cases across all indicator types. Floor distance numeric display is unaffected. Regression check: the Greece backtesting fixture and Zambia 8-step scenario both show correct above/below labels at their respective threshold-crossing steps. |

### 3.2 — Issues explicitly out of scope

| Issue / scope | Rationale for exclusion |
|---|---|
| #394 — Multi-scenario comparison (G2 Phase 3) | G2 sprint group; separate sprint entry; implementation must start after #1249 (Zone 1A curve identifiability) is merged. G4 produces the Zone 1A foundation that G2 Phase 3 builds on. |
| #1252 — Zone 1B proportional allocation (G3) | G3 sprint group; requires ADR; G3 Phase 3 implementation must not begin until #1250 is merged (Zone 1B conflict avoidance per FA sequencing). |
| #1220 — G3 E2E spec soft-skip fix (G5) | G5 sprint group; test infrastructure bug; NM-061 upstream. The G4 test file must not copy the soft-skip pattern from the G3 spec. |
| #1214 — Startup WARNING for empty simulation_entities (G5) | G5 sprint group; observability fix; NM-060 upstream. |
| #1251 — Adaptive y-axis extension audit (G5) | G5 sprint group; capacity-allowing; `computeYDomain()` extension. |
| N=3 multi-scenario rendering implementation | G2 Phase 3 scope. #1249 must validate N=3 compatibility of the identifiability scheme, but does NOT implement N=3 multi-scenario comparison. The N=3 compatibility check is a constraint on the G4 fix, not a deliverable. |
| Zone 1D Mode 3 branch comparison values | M16 G9 deliverable; already implemented. G4 #1253 is a content addition (PSP precedent reference), not a Zone 1D structural change. |
| Zone 1B overflow regression fix (#1252 scope) | G3 Phase 3 scope. The #1250 tablet legibility fix must not introduce a Zone 1B overflow regression (regression guard in §2.4 AC-1250-3); the full overflow architecture is G3. |
| Demo script narration (#1238) | M18 scope per sprint plan §HORIZON scope-completeness check. |

---

## Section 4 — ADR Prerequisite Summary

| Issue | ADR required | ADR status | Implementation may begin? |
|---|---|---|---|
| #1249 — Zone 1A curve identifiability | None — encoding addition within ADR-017 Zone 1A compare-mode boundary | N/A | Yes — after EL approves this entry, UX visual spec is produced, intent document is filed, and QA tests are authored |
| #1253 — Zone 1D PSP historical precedent anchor | None — content addition within ADR-017 Zone 1D boundary | N/A | Yes — same per-issue gate as #1249; implementation sequence: after #1249 merges (FA recommendation) |
| #1250 — Zone 1B tablet legibility at 768px | None — responsive tuning within ADR-017 Zone 1B boundary | N/A | Yes — same per-issue gate; implementation sequence: after #1253 merges (FA recommendation) |
| #1239 — Zone 1B inverted floor label | None — bug fix | N/A | Yes — after EL approves this entry, intent document is filed, and QA test is authored (no UX visual spec required) |

**No ARCH entry required.** All G4 deliverables are within the zone architecture established
by ADR-017. The Zone 1A identifiability scheme (#1249) must scale to N=3 — this is a design
constraint on the fix, not an architectural decision. If at implementation the N=3 validation
reveals that the chosen identifiability scheme requires changes to the Zone 1A composite
encoding architecture (beyond compare-mode overlay), the implementing agent must escalate to
the Architect before proceeding — this would trigger an ADR-017 amendment or ARCH-012
assessment. Escalation path: stop implementation, file a finding on #1249, route to Architect
and PM Agent before proceeding.

---

## Section 5 — Near-Miss Sweep

**Near-miss sweep date:** 2026-06-25
**Sweep period:** G1 sprint exit (2026-06-25) through G4 sprint entry filing (2026-06-25)

| Finding | Category | PI Agent register call issued? | NM entry number |
|---|---|---|---|
| No new process gaps identified in the sweep period. Wave 1 exited cleanly (PI Agent confirmed 2026-06-25). G2 and G4 sprint entries are filed on the same day as Wave 1 exit. No SOP deviations occurred. The G4 per-issue visual spec gate structure is authorized by the EL-approved sprint plan (§G4 UX visual spec gate) and does not constitute a process deviation from the SOP intent document requirement — the intent document for each CRITICAL issue is gated behind the visual spec, which is produced per-issue before that issue's implementation PR opens. | N/A | N/A | N/A |

**NM-056 follow-up guard (no soft-skip patterns):**

`frontend/tests/e2e/m17-g4-demo6-critical-polish.spec.ts` must not contain `test.skip()`,
`test.fixme()`, `.only()`, or conditional skip patterns when the G4 implementation PR is
opened. This is a hard requirement — not a recommendation. If any assertion cannot be made
to pass in CI at implementation time, the implementing agent must file a finding on the
relevant issue rather than soft-skipping the test.

**Pre-push gates (mandatory for all G4 implementation PRs):**

All G4 issues touch `frontend/src/` — the frontend pre-push build gate applies:
`cd frontend && npm run build` — must exit 0 before any G4 feature branch is pushed.

G4 issues do not modify `backend/` files — the backend lint gate (`cd backend && ruff check . && mypy app/`) does not apply unless the #1253 PSP precedent anchor requires a new data field from the backend. If any G4 implementation PR modifies Python files, the backend gate applies.

---

## EL Approval Record

**EL approval:** 2026-06-25

> G4 sprint entry approved. Structural gates confirmed clear. ADR N/A confirmed. Wave 2 gate
> clear (Wave 1 exit confirmed 2026-06-25). UX Designer authorized to begin visual specs in
> FA-recommended sequence: #1249 first, then #1253, then #1250. #1239 intent document and QA
> test may be filed immediately — implementation PR for #1239 may open once both are on record.
> No CRITICAL issue (#1249/#1253/#1250) implementation PR may open until its per-issue UX
> visual spec → intent document → QA test chain is fully satisfied.
> — @PublicEnemage (2026-06-25)
