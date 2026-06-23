---
name: m16-g1-sprint-entry
type: sprint-entry
milestone: M16 — Distributional Visibility
sprint-group: G1
status: EL Approved 2026-06-23 — intent document and QA tests must be filed before implementation PR opens
authored-by: PM Agent
authored-date: 2026-06-23
el-approved: 2026-06-23
release-branch: release/m16
sop-reference: docs/process/sprint-planning-sop.md
---

# Sprint Entry — M16, G1: Zone 1A Phase 4 + Zone 1D Delta Annotations

**Status:** Filed — awaiting EL approval before implementation begins
**Date authored:** 2026-06-23
**Release branch:** `release/m16`
**Sprint plan:** `docs/process/sprint-plans/m16-sprint-plan.md` (EL Approved 2026-06-23)

*Authority: `docs/process/sprint-planning-sop.md §Sprint Entry Gate` (Phase C output).
This entry gates G1 specifically. G1 is the first frontend implementation group in M16 and
is the sequential prerequisite for G2 (distributional surface) and the critical-path gate
for G8 (live stakeholder demo #843 — M16 exit gate). No implementation PR may open against
`release/m16` for G1 until this entry document is EL-approved and the intent and QA gates
below are satisfied.*

---

## Section 1 — Sprint Identification

| Field | Value |
|---|---|
| Milestone | M16 — Distributional Visibility |
| GitHub Milestone | #17 |
| Sprint group | G1 — Zone 1A Phase 4 + Zone 1D Delta Annotations |
| Release branch | `release/m16` |
| Sprint plan document | `docs/process/sprint-plans/m16-sprint-plan.md` |
| Exit checklist issue | #985 |
| Sprint groups in scope | G1 only |
| ADR gate | ADR-017 ✅ (accepted 2026-06-22); ADR-015 ✅ (accepted 2026-06-16) |
| Implementing agent | Frontend Architect Agent |
| Wave | Wave 1 — sequential prerequisite for G2; gates G8 (live stakeholder demo) |

---

## Section 2 — Entry Invariants Checklist

*All items must be checked before any implementation PR is opened for G1.
An unchecked invariant blocks implementation from beginning.*

### 2.1 — Structural gates

- [x] **Release branch exists:** `release/m16` cut from `main` 2026-06-23 (commit 07c92b8)
- [x] **CI trigger verified:** `.github/workflows/ci.yml` `pull_request: branches` includes
  `release/m*` — confirmed at kickoff 2026-06-23 (line 5: `branches: [ main, develop, release/m* ]`;
  line 7: `branches: [ main, release/m* ]`). Ruleset ID 17751852 with 6 required checks:
  `changes`, `lint`, `test-backend`, `playwright-e2e`, `compliance-scan`, `branch-naming`.
  KI-005 permanent fix (`do_not_enforce_on_create: true`) applied 2026-06-20 — no Ruleset
  workaround required for this or future release branches.
- [x] **Sprint plan EL-approved:** `docs/process/sprint-plans/m16-sprint-plan.md`
  `el-approved: 2026-06-23` (PR #1148 merged 2026-06-23)

### 2.2 — ADR prerequisite gate

G1 delivers two tightly-coupled Phase 4 outputs specified in ADR-017: the Zone 1A composite
encoding (#845) and the Zone 1D delta annotations (#1147). ADR-017 (Zone 1A Information
Architecture) is the primary authority for #845 — its Decision table is the binding
implementation spec. ADR-015 (Evidence Thread Architecture) covers the self-interpreting
output pattern extended by #1147 AC-5. Both ADRs are accepted. The sprint plan Architect
consultation confirms no new ADR is required: G1 is fully within accepted ADR-017 Phase 4
scope and ADR-015 evidence-thread scope.

| Group | Required ADR | ADR status | Gate |
|---|---|---|---|
| G1 — #845 (Zone 1A Phase 4 composite encoding) | ADR-017 | Accepted 2026-06-22 | **CLEAR** |
| G1 — #1147 (Zone 1D delta annotations) | ADR-017 + ADR-015 | Both accepted | **CLEAR** |

- [x] All G1 ADR prerequisites are clear. Both issues are within accepted ADR-017 Phase 4
  scope and ADR-015 evidence-thread scope. Gate: **CLEAR**.

### 2.3 — Intent document gate

*An intent document must be filed before any G1 implementation PR opens.
(Authority: docs/process/agent-execution-lifecycle.md Step 1)*

- [x] Intent document filed for G1 deliverables — **FILED 2026-06-23**

| Deliverable | ADR reference | Intent document path | Filed? |
|---|---|---|---|
| #845 — Zone 1A Phase 4 composite encoding | ADR-017 Decision table | `docs/process/intents/M16-G1-2026-06-23-zone-1a-phase4-composite.md` | ✅ Filed 2026-06-23 |
| #1147 — Zone 1D delta annotations | ADR-017 §Zone 1D Integration; ADR-015 evidence-thread | (same intent document) | ✅ Filed 2026-06-23 |

Both G1 deliverables are covered by a single intent document since they share a PR,
an implementing agent, and a hard ADR-017 co-dependency (Phase 4 is incomplete without
both). The intent document must derive acceptance criteria from the observable application
states in Section 3.1 — not from implementation interface. The Kryptonite Constraint
Check (Step 5 of the intent template) is required: the key kryptonite risk for G1 is
implementing Zone 1A composite encoding without simultaneously completing Zone 1D delta
annotations, which ADR-017 §Silent Failure Mode explicitly identifies as a degraded
incomplete implementation.

**Completeness gate:** The QA Lead must be able to write Playwright tests for all G1
acceptance criteria from the intent document without reading any implementation code.

### 2.4 — QA test authorship gate

*QA tests must be authored from the intent document's acceptance criteria before
implementation code is written. (Authority: docs/process/agent-execution-lifecycle.md Step 2)*

- [x] QA test file authored for G1 before implementation begins — **AUTHORED 2026-06-23**

| Deliverable | Intent document | Test file path | Authored before implementation? |
|---|---|---|---|
| #845 — Zone 1A Phase 4 composite encoding | `docs/process/intents/M16-G1-2026-06-23-zone-1a-phase4-composite.md` | `frontend/tests/e2e/m16-g1-zone-1a-phase4-composite.spec.ts` | ✅ Yes — 2026-06-23 |
| #1147 — Zone 1D delta annotations | (same) | (same spec file) | ✅ Yes — 2026-06-23 |

*Soft-skip guard (NM-056 follow-up, M15 retrospective action 3a): the QA test file for G1
must contain no `test.skip()` or conditional skip patterns. Any skip must produce an
explicit CI failure, not a silent pass. The M16 sprint exit checklist confirms no active
soft-skip patterns before #985 closes.*

---

## Section 3 — Scope Declaration

### 3.1 — Issues in scope

| Issue | Title | Priority | Observable application state (pre-implementation specification) |
|---|---|---|---|
| #845 | ux: Zone 1A information architecture — Phase 4 implementation | immediate / CRITICAL | At 1280×800, with the ZMB ECF scenario loaded in Mode 1 with a single entity (N=1): Zone 1A displays 4 framework trajectory curves unchanged — no regression in the single-entity rendering path. With 2 entities loaded (N=2, e.g., ZMB + GRC): Zone 1A displays 2 composite lines (one per entity, `composite_score` from trajectory response) with ISO 3166-1 alpha-3 endpoint labels at the final step, Y-axis range [0.0, 1.0], MDA floor per entity as a horizontal dashed line. In Mode 3 (N≤4): Zone 1A displays 2 composite lines per entity (baseline ghost at 50% opacity, `strokeDasharray="4 2"`, and active solid at 100% opacity), with a divergence fill region between them. A confidence tier badge appears adjacent to each composite line's endpoint label. At N>4: Zone 1A renders a legibility-limit notice panel; Zone 1B and Zone 1D continue to display normally. ADR-017 backtesting validation: Mode 1 single-entity ZMB renders 4 framework curves (composite encoding does not apply); Mode 2 multi-entity ZMB+GRC renders 2 composite lines with correct endpoint labels. Both validation cases must be confirmed at Step 4 Verify before the implementation PR is marked ready for review. |
| #1147 | feat(ux): Zone 1D delta annotations — companion to Zone 1A Phase 4 composite encoding | immediate / CRITICAL | At 1280×800 with the ZMB ECF scenario loaded with political economy enabled and advanced to ≥1 step: Zone 1D PSP row displays the current-period PSP value AND the step-over-step delta (e.g., "38% ↓4pp"), with the delta direction visually encoded (green/up for improving, red/down for deteriorating, consistent with Zone 1A palette per ADR-017). At step 0 (no previous step): the delta field is absent — no placeholder, no "N/A", no empty parentheses. A Layer 3 self-interpreting output sentence for the delta is visible at L0 (e.g., "programme survival dropped 4 percentage points this step") without hover or interaction. Delta computation is client-side from existing trajectory state — no new backend endpoint. Playwright: the PSP delta element is visible and contains a non-empty direction indicator after advancing to step 1; at step 0, the delta element is absent from the DOM or has `display:none`. |

### 3.2 — Issues explicitly out of scope

G1's scope is bounded to the two Phase 4 deliverables specified in ADR-017. The following
are explicitly excluded from G1:

| Issue / scope | Rationale for exclusion |
|---|---|
| #986 — Cohort disaggregation on primary surface | G2 scope — requires G2 pre-conditions (CM/DA/ARF/FA sign-offs) and must follow G1 merge |
| #987 — Political risk summary surface | G2 scope — Zone 1D political risk sub-section extends G1's Zone 1D work; must follow G1 merge to avoid component tree conflicts |
| #274 — 25-year human capital trajectory | G3 scope — requires CE feasibility assessment before sprint entry |
| Zone 1D political risk sub-section layout | G2 scope (#987) — Frontend Architect must confirm Zone 1D layout feasibility (delta annotations + political risk sub-section coexistence at 1280×800) as a G2 pre-condition, not a G1 deliverable |
| Any new backend API endpoints | G1 is frontend-only; delta computation (#1147 AC-4) is client-side from existing trajectory state; composite score (#845) uses `composite_score` field already served in trajectory response since M13 |
| ADR-017 Mode 2 multi-entity COMPARE_VIEW with DeltaChoropleth | Outside Phase 4 scope; per ADR-017 Decision table row "Mode 2 multi-entity COMPARE_VIEW" — covered by existing DeltaChoropleth spec |
| ADR-015 interactive cross-examination mode expansion | G1 delivers persistent Layer 3 delta sentence (zero-interaction, L0); interactive expand mode is separate |

G1 is complete when: all observable application states in Section 3.1 are confirmed in the
running application at Step 4 Verify (including ADR-017 backtesting validation cases); the
Customer Agent Layer 3 assessment is on record; and the Business PO has confirmed at Step 5
Validate that Persona 2 (Aicha Mbaye — finance ministry negotiator) can read the Zone 1A
direction-of-effect signal within 15 seconds of a Mode 3 control input for N=2 entities,
and that the Zone 1D PSP delta sentence is visible and self-interpreting at L0 without
specialist mediation.

---

## Section 4 — ADR Prerequisite Summary

| Group | ADR required | ADR status | Implementation may begin? |
|---|---|---|---|
| G1 — #845 (Zone 1A Phase 4) | ADR-017 (Decision table — Phase 4 binding spec) | Accepted 2026-06-22 | **Yes — after EL approves this entry document, intent document is filed, and QA tests are authored** |
| G1 — #1147 (Zone 1D delta annotations) | ADR-017 §Zone 1D Integration; ADR-015 evidence-thread | Both accepted | (same gate) |

**Implementation sequencing for G1:**

1. EL approves this entry document (this step)
2. Frontend Architect Agent authors intent document at
   `docs/process/intents/M16-G1-2026-06-23-zone-1a-phase4-composite.md` — must derive
   acceptance criteria from the Section 3.1 observable application states above; Kryptonite
   Constraint Check required: the primary kryptonite risk is implementing #845 without #1147
   simultaneously (ADR-017 §Silent Failure Mode); both issues must be in scope in the same
   intent document and the same PR
3. QA Lead Agent authors `frontend/tests/e2e/m16-g1-zone-1a-phase4-composite.spec.ts` from
   the intent document before any implementation code is written; all acceptance criteria for
   both #845 and #1147 must be testable from the intent document without reading implementation
   code; no soft-skip patterns (NM-056 follow-up)
4. Implementation PR opens targeting `release/m16` with milestone-scoped branch name
   (e.g., `feat/m16-g1-zone-1a-phase4-composite`)
5. Frontend Architect Agent Step 4 Verify: confirms all observable application states are
   present in the running application — including ADR-017 backtesting validation cases
   (single-entity ZMB: 4 framework curves unchanged; multi-entity ZMB+GRC: 2 composite lines
   with endpoint labels) — before marking the PR ready for review
6. Customer Agent Layer 3 assessment required before Business PO verdict is final — Persona 2
   (finance ministry negotiator) and Persona 3 (political advisor Andreas) both served:
   Zone 1A composite encoding serves Persona 2's Mode 3 direction-of-effect question; Zone 1D
   delta annotations serve Persona 3's PSP trajectory reading
7. Business PO Step 5 Validate: opens live application and confirms (a) Persona 2 can read
   Zone 1A direction-of-effect signal for N=2 entities within 15-second Mode 3 ceiling;
   (b) Zone 1D PSP delta sentence is visible and self-interpreting at step ≥1 without
   specialist mediation; (c) at step 0, delta is correctly absent

**G2 gate dependency:** G2 (distributional surface #986/#987) may not open its implementation
PR until G1 is merged. Both issues touch Zone 1A and Zone 1D component trees. G2 pre-conditions
(CM/DA/ARF/FA sign-offs) should be worked in parallel with G1 implementation.

**G8 gate dependency:** G8 (live stakeholder demo #843 — M16 exit gate) may not open until
G1, G2, and G3 are all merged and BPO-accepted. G1 merge is a necessary but not sufficient
condition for G8 entry.

---

## Section 5 — Near-Miss Sweep

**Near-miss sweep date:** 2026-06-23
**Sweep period:** M15 exit ceremony (2026-06-23) through M16 G1 sprint entry filing (2026-06-23)

| Finding | Category | PI Agent register call issued? | NM entry number |
|---|---|---|---|
| No new process gaps identified in the sweep period. M15 exit ceremony complete; M16 kickoff completed in same session with no deviations from SOP. NM-056 (soft-skip masked AC-4 mock bug) is already filed and its follow-up action is recorded in M16 exit conditions (§Exit Conditions item 6 in sprint plan) and in Section 2.4 QA gate above — no new NM required. | N/A | N/A | N/A |

---

## EL Approval Record

**EL approval:** 2026-06-23

> G1 sprint entry approved. Structural gates confirmed clear. ADR prerequisites clear for both issues (ADR-017 accepted 2026-06-22; ADR-015 accepted 2026-06-16). Observable application states in Section 3.1 are specific enough to gate QA test authorship. Intent document and QA test file must be filed before implementation PR opens — these remain blocking conditions. G2 gate dependency (G2 implementation PR may not open until G1 merges) and G8 gate dependency (#843 may not open until G1 + G2 + G3 are BPO-accepted) noted and accepted. Implementation may proceed once the intent and QA gates are satisfied.
> — @PublicEnemage (2026-06-23)
