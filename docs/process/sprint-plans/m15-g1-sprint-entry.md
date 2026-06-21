---
name: m15-g1-sprint-entry
type: sprint-entry
milestone: M15 — Human Cost Architecture
sprint-group: G1
status: EL Approved 2026-06-20 — intent document and QA tests must be filed before implementation PR opens
authored-by: PM Agent
authored-date: 2026-06-20
el-approved: 2026-06-20
release-branch: release/m15
sop-reference: docs/process/sprint-planning-sop.md
---

# Sprint Entry — M15, G1: Layer 3 + IR Fixes

**Status:** EL Approved 2026-06-20 — intent document and QA tests must be filed before implementation PR opens
**Date authored:** 2026-06-20
**Release branch:** `release/m15`
**Sprint plan:** `docs/process/sprint-plans/m15-sprint-plan.md` (EL Approved 2026-06-20)

*Authority: `docs/process/sprint-planning-sop.md §Sprint Entry Gate` (Phase C output).
This entry gates G1 specifically. G1 is the first implementation group to open in M15 and
is the prerequisite gate for G8 (live external demo #843). No implementation PR may open
against `release/m15` for G1 until this entry document is EL-approved and the intent and
QA gates below are satisfied.*

---

## Section 1 — Sprint Identification

| Field | Value |
|---|---|
| Milestone | M15 — Human Cost Architecture |
| GitHub Milestone | #16 |
| Sprint group | G1 — Layer 3 + IR Fixes |
| Release branch | `release/m15` |
| Sprint plan document | `docs/process/sprint-plans/m15-sprint-plan.md` |
| Exit checklist issue | #984 |
| Sprint groups in scope | G1 only |
| ADR gate | ADR-015 ✅ (accepted 2026-06-16); ADR-016 ✅ (accepted 2026-06-16) |
| Implementing agent | Frontend Architect Agent |
| Wave | Wave 1 — gates G8 (live external demo) |

---

## Section 2 — Entry Invariants Checklist

*All items must be checked before any implementation PR is opened for G1.
An unchecked invariant blocks implementation from beginning.*

### 2.1 — Structural gates

- [x] **Release branch exists:** `release/m15` cut from `main` 2026-06-20 (commit 500e50d)
- [x] **CI trigger verified:** `.github/workflows/ci.yml` `pull_request: branches` includes
  `release/m*` — confirmed 2026-06-20 (line 5: `branches: [ main, develop, release/m* ]`;
  line 7: `branches: [ main, release/m* ]`). Ruleset ID 17751852 with 6 required checks:
  `changes`, `lint`, `test-backend`, `playwright-e2e`, `compliance-scan`, `branch-naming`.
  KI-005 permanent fix (`do_not_enforce_on_create: true`) applied 2026-06-20 — future release
  branches need no Ruleset workaround.
- [x] **Sprint plan EL-approved:** `docs/process/sprint-plans/m15-sprint-plan.md`
  `el-approved: 2026-06-20` (PR #1094 — EL approval recorded 2026-06-20)

### 2.2 — ADR prerequisite gate

G1 delivers Layer 3 outputs on three surfaces: Zone 1B (directive sentence — ADR-015
Component 4), Zone 1A trajectory curves (L0 badges — ADR-015 Component 1), Zone 1D PSP
sentence (ADR-015 Component 3), and the Grounding strip disambiguation fix (ADR-016
Component 2). All required ADRs are accepted. No new ADR is required for G1: the sprint
plan includes an Architect Agent note confirming G1 is within accepted ADR-015 and ADR-016
scope. EL confirmation of ADR-015 Component 4 scope for #1065 is recorded in the sprint
plan §Four-Agent Consultation Summary.

| Group | Required ADR | ADR status | Gate |
|---|---|---|---|
| G1 — #1065 (Zone 1B sentence) | ADR-015 Component 4 | Accepted 2026-06-16 | **CLEAR** |
| G1 — #1066 (suppress zero steps) | None (UI fix — no new surface) | N/A | **CLEAR** |
| G1 — #1068 (Zone 1A L0 badges) | ADR-015 Component 1 | Accepted 2026-06-16 | **CLEAR** |
| G1 — #1069 (Grounding strip disambiguation) | ADR-016 Component 2 | Accepted 2026-06-16 | **CLEAR** |
| G1 — #1075 (PSP sentence in Zone 1D) | ADR-015 Component 3 | Accepted 2026-06-16 | **CLEAR** |

- [x] All G1 ADR prerequisites are clear. All five issues are within the scope of accepted
  ADR-015 (Components 1, 3, 4) and ADR-016 (Component 2). Gate: **CLEAR**.

### 2.3 — Intent document gate

*An intent document must be filed before any G1 implementation PR opens.
(Authority: CLAUDE.md §Agent Execution Lifecycle Step 1)*

- [ ] Intent document filed for G1 deliverables — **MUST FILE BEFORE IMPLEMENTATION PR OPENS**

| Deliverable | ADR reference | Intent document path | Filed? |
|---|---|---|---|
| #1065 — Zone 1B Layer 3 trajectory sentence | ADR-015 Component 4 | `docs/process/intents/M15-G1-2026-06-20-layer3-ir-fixes.md` | No — BLOCKING |
| #1066 — Suppress "0 consecutive steps" when zero | None (UI fix) | (same intent document) | No — BLOCKING |
| #1068 — L0 badge on Zone 1A trajectory curves | ADR-015 Component 1 | (same intent document) | No — BLOCKING |
| #1069 — Grounding strip dual reserve disambiguation | ADR-016 Component 2 | (same intent document) | No — BLOCKING |
| #1075 — PSP self-interpreting sentence in Zone 1D | ADR-015 Component 3 | (same intent document) | No — BLOCKING |

All five G1 deliverables may be covered by a single intent document
(`M15-G1-2026-06-20-layer3-ir-fixes.md`) since they share a PR, an implementing agent,
and a sprint group. All are frontend-only changes to component surfaces that do not require
new backend endpoints.

**Completeness gate:** The QA Lead must be able to write a Playwright test for each of the
five deliverables from the intent document without reading any implementation code. The
intent document must derive acceptance criteria from the observable application states in
Section 3 below — not from implementation interface.

### 2.4 — QA test authorship gate

*QA tests must be authored from the intent document's acceptance criteria before
implementation code is written. (Authority: CLAUDE.md §Agent Execution Lifecycle Step 2)*

- [ ] QA test file authored for G1 before implementation begins — **MUST FILE BEFORE G1 PR OPENS**

| Deliverable | Intent document | Test file path | Authored before implementation? |
|---|---|---|---|
| #1065 — Zone 1B sentence | `docs/process/intents/M15-G1-2026-06-20-layer3-ir-fixes.md` | `frontend/tests/e2e/m15-g1-layer3-ir-fixes.spec.ts` | No — author after intent document, before implementation PR |
| #1066 — Suppress zero steps | (same) | (same spec file) | No — author after intent document, before implementation PR |
| #1068 — L0 badges | (same) | (same spec file) | No — author after intent document, before implementation PR |
| #1069 — Grounding strip labels | (same) | (same spec file) | No — author after intent document, before implementation PR |
| #1075 — PSP sentence | (same) | (same spec file) | No — author after intent document, before implementation PR |

---

## Section 3 — Scope Declaration

### 3.1 — Issues in scope

| Issue | Title | Priority | Observable application state (pre-implementation specification) |
|---|---|---|---|
| #1065 | ux(zone-1b): Layer 3 trajectory sentence — Zone 1B | immediate / CRITICAL | At 1440×900, with the ZMB ECF scenario loaded and advanced to ≥1 step, Zone 1B contains an element (e.g., `data-testid="zone-1b-trajectory-sentence"`) whose text content is a complete Layer 3 directive sentence — e.g., "Reserve coverage has fallen 2.9 months below the CRITICAL threshold. At current draw rate, full depletion occurs in 4 steps." — visible without interaction, without scroll. The sentence is not merely a severity label plus a count; it conveys the meaning of the trajectory in terms a minister can use without specialist mediation. |
| #1066 | ux(zone-1b): suppress "0 consecutive steps" when zero | immediate / HIGH | With ZMB scenario at step 0 (or any state where no threshold has been consecutively breached at the current step), Zone 1B does not contain text matching "0 consecutive steps" anywhere in the visible panel. When a threshold is breached for the first time at step N, the consecutive-steps count displays "1 consecutive step" (or the accurate non-zero count) — not zero. |
| #1068 | ux(zone-1a): L0 badge on Zone 1A trajectory curves | immediate / HIGH | At 1440×900 with ZMB scenario loaded, each visible trajectory curve in Zone 1A has an associated confidence tier badge visible at L0 (e.g., text content "T2" or "[T2]") — visible without hover, without click, without interaction. At least one badge is visible per active framework curve without scroll. Playwright: `expect(page.locator('[data-testid="zone-1a-l0-badge"]').first()).toBeVisible()` at 1440×900. |
| #1069 | ux(grounding-strip): dual reserve values without disambiguation | immediate / CRITICAL | In the Grounding strip with ZMB scenario at ≥1 step advanced, the reserve coverage indicator row displays two distinctly labeled values: the entry-state value (step 0, source-cited, e.g., "3.8 months · CBJ 2023-Q4 · T2") with a label indicating it is the initial state, and the current simulated value (e.g., "2.9 months · step 3 · simulation") with a label indicating it is the model output. The labels are visible in the Grounding strip panel without interaction beyond opening the strip. A stakeholder reading both values can distinguish which is citable primary data and which is simulation output without presenter explanation. |
| #1075 | ux(zone-1d): PSP self-interpreting sentence absent | immediate / CRITICAL | At 1440×900 with ZMB ECF scenario loaded with political economy enabled and advanced to ≥1 step, Zone 1D contains an interpretive sentence element associated with the programme_survival_probability row — e.g., "Programme survival probability: 65%. This means the programme has a 65% chance of remaining on track through conditionality compliance." — visible without interaction in Zone 1D. The sentence is not a tooltip or hover state; it is persistent at L0. Playwright: `expect(page.locator('[data-testid="psp-layer3-sentence"]')).toBeVisible()`. |

### 3.2 — Issues explicitly out of scope

G1's scope is bounded to the five listed Layer 3 output fixes — all persistent, zero-interaction improvements. The following are explicitly excluded:

| Issue / scope | Rationale for exclusion |
|---|---|
| ADR-015 Component 4 interactive cross-examination mode (full mode transformation) | G1 delivers the persistent Layer 3 sentence (zero-interaction) within Component 4 scope; the interactive expand-all mode is a separate capability not required to fix #1065 |
| ADR-016 Component 3 (Fidelity contextualisation) | G4 scope |
| ADR-016 Component 1 (Data quality preview at scenario creation) | G4 scope |
| Zone 1A ADR-017 implementation (Phases 2–4) | G2 scope — requires ADR-017 acceptance |
| Cohort disaggregation | G3 scope (design-only in M15) |
| Path 1 source network query | G4 scope |
| Any new backend API endpoints | G1 is frontend-only; all data is available from existing `/initial-state`, `/trajectory`, and `/data-quality` endpoints implemented in M14 G3 and G5 |
| Walkthrough updates (DEMO-123/124/129) | G5 scope — low-risk; may proceed in parallel with G1 |

G1 is complete when all five observable application states are confirmed in the running application (Step 4 Verify) and the Business PO has confirmed that Persona 2 (Eleni, finance ministry negotiator) can read the Zone 1B trajectory sentence, the PSP sentence, the disambiguation labels, and the L0 badges without specialist mediation in the Reactive entry state (90-second ceiling) — Step 5 Validate.

---

## Section 4 — ADR Prerequisite Summary

| Group | ADR required | ADR status | Implementation may begin? |
|---|---|---|---|
| G1 — #1065 | ADR-015 (Component 4) | Accepted 2026-06-16 | **Yes — after EL approves this entry document, intent document is filed, and QA tests are authored** |
| G1 — #1066 | None | N/A | (same gate) |
| G1 — #1068 | ADR-015 (Component 1) | Accepted 2026-06-16 | (same gate) |
| G1 — #1069 | ADR-016 (Component 2) | Accepted 2026-06-16 | (same gate) |
| G1 — #1075 | ADR-015 (Component 3) | Accepted 2026-06-16 | (same gate) |

**Implementation sequencing for G1:**
1. EL approves this entry document (this step)
2. Frontend Architect Agent authors intent document at
   `docs/process/intents/M15-G1-2026-06-20-layer3-ir-fixes.md` — must derive acceptance
   criteria from the Section 3.1 observable application states above; Kryptonite Constraint
   Check (Section 5 of the intent template) required for all five deliverables
3. QA Lead Agent authors `frontend/tests/e2e/m15-g1-layer3-ir-fixes.spec.ts` from intent
   document before implementation begins; all five ACs must be testable from the intent
   document without reading any implementation code
4. Implementation PR opens targeting `release/m15` with milestone-scoped branch name
   (`feat/m15-g1-layer3-ir-fixes` or equivalent)
5. Frontend Architect Agent Step 4 Verify: confirms all five observable application states
   are present in the running application before marking PR ready for review
6. Customer Agent Layer 3 assessment required before Business PO verdict is final (Personas
   2, 3, 5 — all five deliverables directly affect the Layer 3 output quality for Persona 2
   in the Reactive entry state; PSP sentence (#1075) directly serves Persona 3 — political
   advisor Andreas)
7. Business PO Step 5 Validate: opens live application and confirms Persona 2 can read Zone
   1B trajectory sentence and PSP sentence without specialist mediation within 90-second
   ceiling; confirms Grounding strip disambiguation is unambiguous to a non-specialist

**G8 gate dependency:** G8 (live external demo #843) may not open until G1 is merged and
Step 5 Validate is complete. The sprint plan records: "G1 must be merged" as the explicit
G8 gate. Real external participants must not attend a session where the Zone 1B trajectory
sentence and PSP sentence are absent — the north star test fails without them.

---

## Section 5 — Near-Miss Sweep

**Near-miss sweep date:** 2026-06-20
**Sweep period:** M14 exit (2026-06-20) through M15 G1 sprint entry filing (2026-06-20)

| Finding | Category | PI Agent register call issued? | NM entry number |
|---|---|---|---|
| No process gaps identified in the sweep period. M14 exit ceremony and M15 kickoff completed same session; KI-005 (release-branch-ci-gate bootstrapping problem) was resolved with a permanent fix (`do_not_enforce_on_create: true`) and is already a Known Issue entry — not a new NM. | N/A | N/A | N/A |

---

## EL Approval Record

**EL approval:** 2026-06-20

> G1 sprint entry approved. Structural gates confirmed clear. ADR prerequisites clear for all five issues (ADR-015 Components 1, 3, 4; ADR-016 Component 2 — all accepted 2026-06-16). Observable application states in Section 3.1 are specific enough to gate QA test authorship. Intent document and QA test file must be filed before implementation PR opens — these remain blocking conditions. G8 gate dependency on G1 merge noted and accepted. Implementation may proceed once the Step 2 and Step 3 gates are satisfied.
> — @PublicEnemage (2026-06-20)
