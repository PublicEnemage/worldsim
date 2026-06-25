---
name: m17-g2-sprint-entry
type: sprint-entry
milestone: M17 — Calibration and Comparative Infrastructure
sprint-group: G2 (Phase 3 — Implementation)
status: Draft — pending Phase 1/2 completion; EL approval required before implementation PR opens
authored-by: PM Agent
authored-date: 2026-06-25
el-approved: false
release-branch: release/m17
sop-reference: docs/process/sprint-planning-sop.md
---

# Sprint Entry — M17, G2: Multi-Scenario Design Sprint (Phase 3 Implementation)

**Status:** Draft — conditions pending Phase 1 and Phase 2 completion; EL approval required before any implementation PR opens
**Date authored:** 2026-06-25
**Release branch:** `release/m17`
**Sprint plan:** `docs/process/sprint-plans/m17-sprint-plan.md` (EL Approved 2026-06-25)

*Authority: `docs/process/sprint-planning-sop.md §Sprint Entry Gate` (Phase C output).
This entry gates G2 Phase 3 implementation only. G2 Phase 1 (design — UX journeys, use stories,
wireframes) and G2 Phase 2 (architecture — ARCH-REVIEW-007 assessment) require NO sprint entry
per sprint plan §G2 Phase 1 exception. This document must be fully satisfied and EL-approved
before the G2 Phase 3 implementation PR opens.*

*Per sprint plan §Wave 2 sequencing: #1249 (Zone 1A curve identifiability) must be merged to
`release/m17` before the G2 Phase 3 implementation PR opens — regardless of when this entry
document is EL-approved. That merge dependency is a hard gate on the implementation PR, not
on this entry document's filing.*

---

## Section 1 — Sprint Identification

| Field | Value |
|---|---|
| Milestone | M17 — Calibration and Comparative Infrastructure |
| GitHub Milestone | #18 |
| Sprint group | G2 — Multi-Scenario Design Sprint (Phase 3: Implementation) |
| Release branch | `release/m17` |
| Sprint plan document | `docs/process/sprint-plans/m17-sprint-plan.md` |
| Exit checklist issue | #982 |
| Sprint groups in scope | G2 Phase 3 only |
| ADR gate | **PENDING** — Architect determines at Phase 2 completion (see §2.2) |
| Implementing agent | Frontend Engineer + QA Lead; Architect consults on N>2 rendering path |
| Wave | Wave 2 (gated on Wave 1 exit ✅ confirmed 2026-06-25) |
| Phase 3 implementation gate | **#1249 merged to `release/m17`** before implementation PR opens (FA constraint) |

**Phase 1 and Phase 2 prerequisite summary (must be complete before this entry can be EL-approved):**

| Prerequisite | Owner | Status |
|---|---|---|
| G2 Phase 1 complete: UX journeys (Journey 1–3), use stories, N>2 zone layout — **UX mockups required at minimum; UI mockups required if feasible** | Design Thinking + UX Designer + Customer Agent | ✅ COMPLETE 2026-06-25 — PR #1280 merged; `ux-journeys-n3.md` + `persona-mvs-n3.md` on release/m17 |
| G2 Phase 1 design artifact panel review: UX mockups (and UI mockups if produced) reviewed and approved by the Phase 1 design panel before BPO acceptance | UX Designer (R) + Design Thinking + Customer Agent + Frontend Architect + Business PO | ✅ COMPLETE 2026-06-25 — 4/4 PASS; panel summary comment #394#issuecomment-4803973123; UX mockups sufficient (no UI mockup conditions triggered) |
| G2 Phase 1 BPO acceptance: BPO accepts Phase 1 design output (use stories + journeys + approved mockups) | Business PO | ✅ BPO ACCEPT 2026-06-25 — #394#issuecomment-4803977557; AC-1–AC-10 all satisfied; Phase 3 fixture-based approach accepted |
| G2 Phase 2 complete: Architect assesses ARCH-REVIEW-007 with UX in hand; ADR determination | Architect + Frontend Architect | ✅ COMPLETE 2026-06-25 — PR #1280 merged; `ARCH-REVIEW-007-m17-n3-assessment.md`; ADR determination option (b): review note on #394 sufficient; no new ADR |
| Intent document filed for #394 implementation (must reference approved mockups) | PM Agent + UX Designer | ⬜ PENDING Phase 1/2 |
| QA test file authored before implementation begins | QA Lead | ⬜ PENDING intent document |
| #1249 merged to `release/m17` | G4 sprint group | ⬜ PENDING G4 |

---

## Section 2 — Entry Invariants Checklist

*All items must be checked before any G2 Phase 3 implementation PR opens.
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

*Authority: sprint plan §Architect — ADR prerequisites (downstream of UX)*

The ADR determination for G2 Phase 3 is PENDING and depends on Phase 2 Architect assessment.
The sprint plan identifies two possible outcomes after the UX journeys are produced:

- **Path A — ARCH-REVIEW-007 amendment:** If N>2 scenario rendering requires structural changes
  to the Zone 1A composite encoding architecture or compare-mode overlay beyond the current
  component boundary, ARCH-REVIEW-007 must be reopened and the decision filed as ARCH-012
  (or ARCH-013 depending on #1252 outcome). Implementation may not open until the ADR is accepted.

- **Path B — Architecture review note on #394:** If N>2 is a straightforward compare-mode
  extension within the existing TrajectoryView component boundary (existing Zone 1A rendering
  path + compare-mode overlay only), the Architect may determine that an ADR is not required —
  only an architecture review note on issue #394. Implementation may open once the note is filed.

Neither path can be determined until Phase 1 UX journeys are produced and Phase 2 Architect
assessment completes. The Architect's Phase 2 assessment is the gate on this condition.

**Additional ADR dependency (Zone 1B per-scenario threshold crossings):**
The sprint plan notes that if Zone 1B per-scenario threshold crossings require a new backend
data structure in the compare endpoint, the Architect must assess whether this constitutes an
architectural decision. The existing `threshold_crossings` field was delivered in G9 (PR #1201);
the question is whether the per-scenario extension is a data contract change that requires a
formal ADR. This is also resolved in Phase 2.

- [x] **ADR prerequisite gate: CLEAR** — Architect Phase 2 assessment filed 2026-06-25
  (`docs/architecture/reviews/ARCH-REVIEW-007-m17-n3-assessment.md`, PR #1280);
  ADR determination: option (b) — review note on #394 sufficient; no new ADR required

**ADR prerequisite status (at filing; to be updated at Phase 2 completion):**

| Group | Required ADR | ADR status | Gate |
|---|---|---|---|
| G2 Phase 3 — #394 (Zone 1A N>2 rendering) | Path B: review note on #394 | **CLEAR 2026-06-25** — compare-mode overlay only; no composite_score path change | **CLEAR** |
| G2 Phase 3 — #394 (Zone 1B per-scenario threshold crossings) | No ADR — client-side composition from N parallel trajectory fetches | **CLEAR 2026-06-25** — no new endpoint; no API contract change | **CLEAR** |
| G2 Phase 3 — #394 (Zone 1D per-scenario PSP) | No ADR — client-side store extension | **CLEAR 2026-06-25** — PSP field already in trajectory response | **CLEAR** |

*These entries must be updated to CLEAR or BLOCKED_ADR before EL approval of this entry.*

### 2.3 — Intent document gate

*For #394 (G2 Phase 3 implementation), an intent document must be filed at
`docs/process/intents/M17-G2-{YYYY-MM-DD}-multi-scenario-comparison.md` before the
implementation PR opens. The QA Lead must be able to write tests from it without reading
implementation code.*

- [ ] **Intent document gate: PENDING** — intent document cannot be authored until Phase 1
  (UX journeys, use stories, N>2 mockups) is complete, panel-reviewed, and BPO-accepted.
  The intent document's acceptance criteria are derived from the Phase 1 use stories and
  Phase 2 component scope. **The intent document must include or reference the approved UX
  mockups (and UI mockups if produced) as the authoritative visual specification — QA Lead
  writes assertions against the mockup-defined observable states, not against implementation
  inference.** If UI mockups were produced and panel-approved, they are the binding visual
  specification; if only UX mockups exist, they are the binding specification.

**Intent document content requirements (to be satisfied at filing):**

The intent document for #394 Phase 3 must specify, at minimum:

1. **Scenario comparison setup (Journey 1):** Observable state when three scenarios are active —
   scenario selector or new entry point; what Zone 1D shows with three scenarios (entity attribution
   in comparison mode).

2. **Zone 1A N>2 rendering (Journey 2):** The exact differentiation scheme (color + line-style +
   terminal label or UX Designer specification from visual spec) for N=3; whether the same scheme
   extends to N=4 or is capped at N=3 for Demo 7. Observable state: the analyst can identify
   which trajectory belongs to which scenario without hovering, at 1280×800 and 768px.

3. **Zone 1B per-scenario threshold crossings (Journey 3 partial):** Observable state — threshold
   crossing summary shown per-scenario (not a union); minimum: Q1 crossing status, step number,
   indicator, for each active scenario. The MDA alert panel must remain readable (≥80px visible,
   per `minHeight: 80px` temporary guarantee) when per-scenario crossings populate the section.

4. **Zone 1D per-scenario PSP (Journey 3 partial):** Observable state — PSP value visible per
   active scenario in Zone 1D; the analyst can read which scenario has highest/lowest programme
   survival probability without narration.

5. **Acceptance criteria — Persona 1 (Lucas Ferreira):** Lucas can select three restructuring
   scenarios and, within 60 seconds, identify which scenario has the worst Q1 poverty trajectory
   over a specified step window — without presenter narration.

6. **Acceptance criteria — Persona 5 (Aicha Mbaye):** Aicha can read the comparison result
   within 90 seconds — which option is least damaging to the bottom quintile — from Zone 1A +
   Zone 1B alone. The display is legible at glance level at 1280×800.

7. **Acceptance criteria — Persona 3 (Andreas Petrakis):** Andreas can read per-scenario PSP
   values in Zone 1D to build a political brief comparing programme survival probability across
   the three restructuring options.

8. **Scope boundary (Demo 7 minimum viable):** What is explicitly out of scope for Phase 3 —
   Mode 3 with N>1 scenarios, N≥4 support, cross-scenario Zone 1D delta, full scenario
   interaction in Active Control mode. These are M18 scope per BPO prioritization.

| Deliverable | ADR reference | Intent document path | Filed? |
|---|---|---|---|
| #394 — Multi-scenario comparison (N>2), Phase 3 implementation | TBD (Phase 2 output) | `docs/process/intents/M17-G2-{YYYY-MM-DD}-multi-scenario-comparison.md` | **No — BLOCKING** |

### 2.4 — QA test authorship gate

*QA tests must be authored from the intent document's acceptance criteria BEFORE implementation
code is written. The test file must be on record before the implementing agent begins.*

- [ ] **QA test gate: PENDING** — cannot be authored until the intent document is filed

**QA test file requirements (to be satisfied at filing):**

The QA test file for G2 Phase 3 is an E2E Playwright test. It must assert, from the intent
document's acceptance criteria:

1. **AC-S1 (scenario setup):** Three scenarios can be created or selected; Zone 1A renders
   three trajectory sets; Zone 1B and Zone 1D update to reflect comparison mode state.

2. **AC-A1 (Zone 1A differentiability):** At N=3, each trajectory is identifiably distinct
   at 1280×800; terminal labels (or line-style differentiation per UX spec) are present.
   Must extend the N=2 differentiation test added for #1249 — the G2 test must assert N=3 in
   the same visual-distinguishability frame (per sprint plan FA constraint: N>2 rendering
   builds on stable Zone 1A after #1249 merges).

3. **AC-B1 (Zone 1B per-scenario):** Threshold crossing summary shows per-scenario rows
   (not a union); MDA alert panel remains visible at ≥80px; cohort impact section does not
   collapse MDA panel (Zone 1B overflow regression guard — M16 retrospective).

4. **AC-D1 (Zone 1D per-scenario PSP):** PSP value is visible for each active scenario;
   the analyst can read the values without interaction.

5. **AC-P1/P5/P3 (Persona acceptance):** Lucas can identify worst Q1 trajectory scenario
   within 60 seconds; Aicha can read the comparison result within 90 seconds; Andreas can
   read per-scenario PSP values. These are timed-task behavioral assertions expressed as
   testid-anchored element presence checks at the minimum legibility size.

**No soft-skip patterns permitted** (NM-056 guard: all assertions must be hard-fail; no
`test.skip()`, `test.fixme()`, or `.only()` without an NM entry authorizing the skip).

| Deliverable | Intent document | Test file path | Authored before implementation? |
|---|---|---|---|
| #394 — Multi-scenario comparison (N>2) | `docs/process/intents/M17-G2-{YYYY-MM-DD}-multi-scenario-comparison.md` | `frontend/tests/e2e/m17-g2-multi-scenario-comparison.spec.ts` | **No — BLOCKING** |

### 2.5 — Phase 1 design artifact standards and panel review gate

*This section stipulates the minimum artifact requirements for G2 Phase 1 output and the
panel review that must pass before BPO acceptance and Phase 2 may begin.*

#### Artifact requirements

**Minimum required — UX mockups:**

UX mockups are structural representations that communicate layout, information hierarchy,
and interaction flow without polished visual styling. They are sufficient to answer the
architectural questions in Phase 2 and to write implementation-ready acceptance criteria.

For G2, UX mockups must cover all three journeys at the zone level:

| Journey | Minimum mockup coverage |
|---|---|
| Journey 1 — Scenario Setup | Entry point for creating/selecting three scenarios; Zone 1D state when three scenarios are active (entity attribution in comparison mode) |
| Journey 2 — Primary Viewport in Comparison Mode | Zone 1A with three trajectory sets: chosen differentiation scheme (color + line-style + terminal label or alternative) at N=3, at 1280×800 and 768px viewports |
| Journey 3 — Threshold Comparison | Zone 1B per-scenario threshold crossing display (not a union); Zone 1D per-scenario PSP value surface; MDA alert panel + cohort section co-existence when all three scenarios have crossings |

Each mockup must be viewport-anchored: produced at 1280×800 (primary presentation) and
768px (tablet legibility, the DEMO6-026/043 constraint). N=3 is the required scenario count.

**Ideally produced — UI mockups:**

UI mockups are higher-fidelity representations that apply the actual design system (colors,
typography, spacing, component states) to the UX layout. They allow the panel to evaluate
visual distinguishability, label legibility, and component density at implementation scale.

For G2, UI mockups are required if any of the following conditions apply:
- The UX mockup for Journey 2 (Zone 1A N>2 differentiation) reveals that the color/line-style
  scheme is ambiguous at 768px — a UI mockup at scale is needed to validate legibility
- The Phase 1 panel review identifies a visual density risk in Zone 1B or Zone 1D under N=3 load
- The Frontend Architect requests a UI-fidelity view to assess component implementation scope

If none of these conditions apply, UX mockups are sufficient and UI mockups are optional.
The UX Designer records in the panel review whether UI mockups were produced and the reason.

#### Panel review — required before BPO acceptance

The Phase 1 design artifact panel reviews all produced mockups (UX at minimum; UI if produced)
before BPO acceptance is requested. The panel does not proceed unless UX mockups for all three
journeys at both viewports are present.

**Panel composition:**

| Agent | Role in review | Minimum assessment required |
|---|---|---|
| UX Designer | R — review lead; confirms mockups satisfy the five governing UX premises (CLAUDE.md §UX Architectural Commitments) | Sign-off confirming all three journeys are covered at both viewports; no governing premise violated |
| Design Thinking Agent | Cognitive task validation — confirms the N>2 comparison supports the primary cognitive task (threshold-crossing profile comparison, not trajectory aesthetics) | Verdict: does Journey 2 allow the analyst to identify which scenario crosses which threshold at which step, without presenter narration? |
| Customer Agent | Persona accessibility — confirms Aicha (Persona 5) can read the comparison result within 90 seconds from the mockup; confirms Andreas (Persona 3) can read per-scenario PSP without narration; confirms Lucas (Persona 1) can identify the worst Q1 trajectory scenario within 60 seconds | Pass/fail verdict for each persona against the mockup, at 1280×800 and 768px |
| Frontend Architect | Technical feasibility — confirms the N>2 zone layout is implementable within the existing TrajectoryView component boundary, or flags structural changes that require Phase 2 ADR coverage | Feasibility verdict on Zone 1A N>2 rendering path; flags any component boundary violations |
| Business PO | Acceptance — reviews panel verdicts before issuing formal Phase 1 BPO acceptance; confirms the minimum viable Demo 7 story is legible from the mockups | ACCEPT / REJECT verdict on Phase 1 design output; ACCEPT required before Phase 2 begins |

**Panel review format:**

Each panel member records their verdict as a comment on GitHub issue #394. The UX Designer
collects the verdicts and produces a panel summary comment on #394 before PM Agent routes to
BPO for formal acceptance. **The panel summary comment must explicitly tag the PM Agent
(@PublicEnemage) — a summary comment without this tag does not constitute a routing signal
and PM Agent is not obligated to act on it.** The panel summary must record:

- Count of panel members who reviewed
- Any REJECT verdict and the specific concern raised
- Whether UI mockups were produced, and if not, why UX mockups are sufficient
- Whether any panel member identified a need for Phase 2 to resolve a design ambiguity
  (these ambiguities become explicit inputs to the Architect's Phase 2 assessment)

**Panel review fail condition:**

If any panel member issues a REJECT verdict, the design artifacts must be revised and
re-reviewed before BPO acceptance is requested. The PM Agent does not route to BPO until
all panel verdicts are PASS (or the rejecting agent explicitly marks their concern resolved
after revision). A BPO acceptance issued without all panel verdicts on record is non-compliant
and the PI Agent blocks Phase 2 from opening.

- [x] **Phase 1 design artifact panel review: COMPLETE 2026-06-25** — 4/4 PASS verdicts
  (UX Designer, Design Thinking Agent, Customer Agent, Frontend Architect); panel summary
  comment: #394#issuecomment-4803973123; UI mockups not required (no triggering conditions
  met); BPO ACCEPT: #394#issuecomment-4803977557; AC-1–AC-10 all satisfied

---

## Section 3 — Scope Declaration

### 3.1 — Issues in scope

| Issue | Title | Priority | Observable application state |
|---|---|---|---|
| #394 | feat: multi-scenario comparison (>2 scenarios) | High — Demo 7 Act 2 | Three-scenario Zambia restructuring comparison: Zone 1A shows three labeled trajectory sets; Zone 1B shows per-scenario threshold crossing summary (not a union); Zone 1D shows per-scenario PSP value. Aicha (Persona 5) can identify the least damaging option within 90 seconds at 1280×800 without narration. FRAME-D sentence behavior at N=3: remains legible; scenario identity is preserved in Zone 1A milestone sentence. |

**Minimum viable Phase 3 scope (per BPO Demo 7 prioritization):**

*Cut order if capacity is constrained within Phase 3 (never cut these):*
1. Zone 1A N=3 trajectory differentiation (core — Demo 7 Act 2 requires it)
2. Zone 1B per-scenario threshold crossing summary (core — Aicha's 90-second read)
3. Zone 1D per-scenario PSP (core — Andreas' political brief)

*Cut to M18 if scope complexity exceeds M17 timeline:*
- N≥4 scenario support (Demo 7 is a three-scenario story; N=4+ is M18)
- Mode 3 multi-scenario interaction (Active Control with N>1 scenarios — M18 north star)
- Cross-scenario Zone 1D delta display (enhancement beyond Demo 7 minimum)
- Full scenario interaction in Mode 3 branching (M18 scope)

**If Phase 3 implementation cannot complete before M17 closes:** The design artifacts (Phase 1
journeys + wireframes + use stories; Phase 2 ADR/review note) are the M17 G2 deliverable.
BPO and Customer Agent assess design artifacts, not implementation. PI Agent records the
implementation carry in the M17 exit document. Implementation continues in M18 with this entry
document remaining active.

### 3.2 — Issues explicitly out of scope

| Issue / scope | Rationale for exclusion |
|---|---|
| #1252 — Zone 1B proportional allocation (G3) | Separate sprint group; own ADR gate; must merge before #394 to avoid Zone 1B conflicts |
| #1249/#1250/#1253/#1239 — DEMO6 CRITICAL (G4) | G4 sprint group; #1249 must merge before G2 Phase 3 implementation PR opens |
| #1220/#1214/#1251 — infrastructure (G5) | Separate sprint group; capacity-allowing after G4 |
| Mode 3 multi-scenario (N>1) | M18 north star; not Demo 7 scope |
| N≥4 scenario rendering | M18 scope; Demo 7 requires N=3 only |
| GovernanceModule Wave 2 implementation (#1248 carry) | Separate from #394; own scope determination |
| Backend CM governance calibration implementation | G1 Wave 2 carry; separate from multi-scenario |

---

## Section 4 — ADR Prerequisite Summary

*To be updated at G2 Phase 2 completion. Architect records the ADR determination here before
this entry can be EL-approved.*

| Group | ADR required | ADR status | Implementation may begin? |
|---|---|---|---|
| G2 Phase 3 — #394 (Zone 1A N>2 rendering path) | Path B — review note on #394 | **CLEAR 2026-06-25** — overlay extension only; no ADR | **Yes — pending intent doc + QA test** |
| G2 Phase 3 — #394 (Zone 1B per-scenario crossings) | No ADR — client-side composition | **CLEAR 2026-06-25** — N parallel trajectory fetches; no endpoint change | **Yes — pending intent doc + QA test** |
| G2 Phase 3 — #394 (Zone 1D per-scenario PSP) | No ADR — client-side store extension | **CLEAR 2026-06-25** — PSP in existing response | **Yes — pending intent doc + QA test** |

**Phase 2 Architect output required before EL approval:**

The Architect must file a determination note on GitHub issue #394 answering:

1. Does Zone 1A N>2 rendering require changes to the composite_score rendering path, or only
   to the compare-mode overlay? If the former: ARCH-012 (or ARCH-013 if #1252 takes ARCH-012)
   must be accepted before Phase 3 begins. If the latter: review note on #394 suffices.

2. Does Zone 1B per-scenario threshold crossings require a new backend data structure in the
   compare endpoint, or is the existing `threshold_crossings` field (G9, PR #1201) sufficient
   with a client-side per-scenario composition? If new backend structure: data contract change
   may require ADR coverage.

3. Does Zone 1D per-scenario PSP require a new endpoint, or is a client-side multi-scenario
   store structure within the existing compare state shape sufficient?

The Architect's answers to all three determine whether this entry's ADR gate reads CLEAR or
BLOCKED_ADR before EL approval.

**Phase 3 implementation sequencing (once ADR gate cleared):**

1. EL approves this entry document (requires Phase 1 BPO acceptance + Phase 2 Architect note + intent document filed + QA tests authored)
2. Confirm #1249 is merged to `release/m17` (FA hard gate)
3. Cut feature branch: `feat/m17-g2-multi-scenario` from `release/m17`
4. Backend (if new data structure required): compare endpoint extension per Architect spec
5. Frontend: Zone 1A N>2 rendering; Zone 1B per-scenario summary; Zone 1D per-scenario PSP; scenario setup UX (Journey 1)
6. Pre-push lint gate: `cd backend && ruff check . && mypy app/` (if backend changes); `cd frontend && npm run build` (frontend changes mandatory)
7. E2E tests pass: `m17-g2-multi-scenario-comparison.spec.ts` — all AC assertions pass; no soft-skips
8. Business PO acceptance and Customer Agent Layer 3 (Personas 1, 3, 5) — required at exit

---

## Section 5 — Near-Miss Sweep

**Near-miss sweep date:** 2026-06-25
**Sweep period:** G1 sprint exit (2026-06-25) through G2 sprint entry filing (2026-06-25)

| Finding | Category | PI Agent register call issued? | NM entry number |
|---|---|---|---|
| No new process gaps identified. Wave 1 exited cleanly. This entry is filed immediately after G1 exit confirmation. PM Agent action items from G1 governance spec (SEN institutional_capacity_index seed; Zone 1D governance horizon tooltip) are noted for next HORIZON sweep — not blocking G2. | N/A | N/A | N/A |

**PM Agent HORIZON sweep note (from G1 exit PI Agent confirmation):**

Two Wave 2 issues must be filed at the next HORIZON sweep:
1. SEN `institutional_capacity_index` seed + GovernanceElasticity co-gated PR (from governance sensitivity specification §Summary Q2)
2. Zone 1D tooltip — governance divergence horizon disclosure (from governance sensitivity specification §Summary Q3)

These are distinct from #394 and do not block G2 Phase 3 filing. They are recorded here for
traceability to the G1 exit PI Agent confirmation (m17-g1-sprint-exit.md §Section 5).

---

## EL Approval Record

**EL approval:** Pending — Phase 1 + Phase 2 COMPLETE (BPO ACCEPT 2026-06-25); ADR gate CLEAR;
remaining blocking items: §2.3 intent document + §2.4 QA test file

*Updated 2026-06-25: Conditions (1) and (2) are now satisfied:*
*(1) G2 Phase 1 complete + BPO ACCEPT 2026-06-25 (#394#issuecomment-4803977557)*
*(2) G2 Phase 2 Architect assessment filed 2026-06-25 (PR #1280; ADR option (b) — review note on #394)*
*Remaining before EL approval:*
*(3) Intent document filed at `docs/process/intents/M17-G2-{date}-multi-scenario-comparison.md`*
*(4) QA test file `frontend/tests/e2e/m17-g2-multi-scenario-comparison.spec.ts` authored and on record*
*Note: §2.1 #1249 merge required before Phase 3 PR opens but does not block EL approval of this entry.*

> {EL approval statement — to be filled at approval time, once §2.3 + §2.4 confirmed}
> — @PublicEnemage ({date})
