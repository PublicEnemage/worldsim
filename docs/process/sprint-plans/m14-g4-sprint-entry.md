---
name: m14-g4-sprint-entry
type: sprint-entry
milestone: M14 — Methodology Publication and External Validation
sprint-group: G4
status: EL Approved — 2026-06-17
authored-by: PM Agent
authored-date: 2026-06-17
el-approved: 2026-06-17
release-branch: release/m14
sop-reference: docs/process/sprint-planning-sop.md
---

# Sprint Entry — M14, G4: ADR-016 Frontend (Grounding Strip + Data Quality Preview + Parameter Persistence)

**Status:** Awaiting EL Approval
**Date authored:** 2026-06-17
**Release branch:** `release/m14`
**Sprint plan:** `docs/process/sprint-plans/m14-sprint-plan.md` (EL Approved 2026-06-16)

*Authority: `docs/process/sprint-planning-sop.md §Sprint Entry Gate` (Phase C output).
This entry gates G4 specifically. G4 is the ADR-016 frontend group — entity selector,
data quality preview, Grounding strip, parameter persistence, and M14-scoped IC-4/IC-6
mitigations. G4 is gated on G3 (API endpoints must exist and AC-1 + AC-6 must pass in
the running application). That gate is now satisfied (G3 BPO ACCEPT 2026-06-17, PR #1012).*

---

## Section 1 — Sprint Identification

| Field | Value |
|---|---|
| Milestone | M14 — Methodology Publication and External Validation |
| GitHub Milestone | #15 |
| Sprint group | G4 — ADR-016 Frontend |
| Release branch | `release/m14` |
| Sprint plan document | `docs/process/sprint-plans/m14-sprint-plan.md` |
| Exit checklist issue | #968 |
| Sprint groups in scope | G4 only |
| ADR gate | ADR-016 — Scenario Grounding Architecture ✅ Accepted 2026-06-16 (PR #967) |
| G3 gate | G3 COMPLETE — BPO ACCEPT 2026-06-17 (PR #1012); AC-1 and AC-6 confirmed in running application |
| Implementing agent | Frontend Architect Agent |

---

## Section 2 — Entry Invariants Checklist

*All items must be checked before any implementation PR is opened for G4.
An unchecked invariant blocks implementation from beginning.*

### 2.1 — Structural gates

- [x] **Release branch exists:** `release/m14` cut from `main` 2026-06-16 (PR #991 merged)
- [x] **CI trigger verified:** `.github/workflows/ci.yml` `pull_request: branches` includes
  `release/m*` — confirmed 2026-06-16 (Ruleset ID 17751852 with 6 required checks: `changes`,
  `lint`, `test-backend`, `playwright-e2e`, `compliance-scan`, `branch-naming`)
- [x] **Sprint plan EL-approved:** `docs/process/sprint-plans/m14-sprint-plan.md`
  `el-approved: 2026-06-16` (PR #992)

### 2.2 — ADR prerequisite gate

G4 implements ADR-016 §Component 1 (entity selector + data quality preview), §Component 2
(Grounding strip), and §Component 4 (parameter persistence) at the frontend layer. It also
delivers two M14-scoped IC mitigations: IC-4 (static Fidelity panel header) and IC-6
(choropleth reference header label). ADR-016 is Accepted.

**G3 gate (hard prerequisite):** G4 cannot be implemented or verified without G3's API
layer. The G3 gate is satisfied: `GET /api/v1/entities/JOR/data-quality?year=2024` (AC-1)
and `GET /api/v1/scenarios/{id}/initial-state` returning `reserve_coverage_months` with
`source: "CBJ"` (AC-6/AC-7) both confirmed in the running application during G3 BPO Step 5
validation (2026-06-17).

| Group | Required ADR | ADR status | G3 gate | Gate |
|---|---|---|---|---|
| G4 | ADR-016 — Scenario Grounding Architecture | **Accepted 2026-06-16 (PR #967)** | **SATISFIED 2026-06-17 (PR #1012)** | **CLEAR** |

- [x] ADR-016 is Accepted. G3 gate is satisfied. G4 ADR and dependency gates are clear.

**G4 forwarded constraint from G3 BPO Step 5:** The `/initial-state` endpoint returns a
`"None"` framework key for legacy simulation attributes lacking a `measurement_framework`
field (e.g., `pop_rank`, `economy_tier`). The Grounding strip must filter to named framework
keys only — `financial`, `human_development`, `ecological`, `governance`,
`political_economy`. The `"None"` key must not render as a framework section in the UI.

### 2.3 — Intent document gate

*An intent document must be filed before any G4 implementation PR opens.
(Authority: CLAUDE.md §Agent Execution Lifecycle Step 1)*

- [ ] Intent document filed for G4 deliverables — **NOT YET FILED — required before implementation PR opens**

| Deliverable | ADR reference | Intent document path | Filed? |
|---|---|---|---|
| Entity selector (Component 1) | ADR-016 §Component 1 | `docs/process/intents/M14-G4-2026-06-17-adr016-frontend.md` | ⬜ Required |
| Data quality preview panel (Component 1) | ADR-016 §Component 1 | (same intent document) | ⬜ Required |
| Grounding strip — button + panel (Component 2) | ADR-016 §Component 2 | (same intent document) | ⬜ Required |
| Parameter persistence display (Component 4) | ADR-016 §Component 4 | (same intent document) | ⬜ Required |
| IC-4 mitigation — static Fidelity header (M14 scope) | ADR-016 EL Decision 2 | (same intent document) | ⬜ Required |
| IC-6 mitigation — choropleth reference header | ADR-016 EL Decision 5 | (same intent document) | ⬜ Required |

**Intent document completeness gate:** The QA Lead must be able to write Playwright tests
for every acceptance criterion from the intent document without reading any implementation
source code. The intent document must specify:
- Exact `data-testid` values for each new component (ADR-016 §UX-3 specifies testids for
  `data-quality-preview`, `grounding-strip`, `scenario-parameters`, and
  `fidelity-contextualisation`; intent document must confirm or extend these)
- Observable application states: what the DOM contains and at what viewport, with which
  scenario loaded, after which interactions
- Silent failure observable states: what the DOM shows when the API returns empty frameworks
  (ADR-016 §Silent Failure Mode specifies required fallback text verbatim for each component)
- The "None" framework filter: Grounding strip does not render a section for the `"None"`
  framework key from `/initial-state`

**Implementing agent (Frontend Architect Agent):** authors the intent document. Chief Engineer
Agent is C for any API integration questions. Data Architect Agent is C for any
`api_contracts.yml` clarification.

**Component 3 is explicitly out of scope:** Fidelity contextualisation with analogous-case
selection is deferred to M15 (ADR-016 EL Decision 2). The intent document must not include
Component 3 acceptance criteria.

### 2.4 — QA test authorship gate

*QA tests must be authored from the intent document's acceptance criteria before implementation
code is written. (Authority: CLAUDE.md §Agent Execution Lifecycle Step 2)*

- [ ] QA test file authored for G4 before implementation begins — **NOT YET FILED — required before implementation PR opens**

| Deliverable | Intent document | Test file path | Authored before implementation? |
|---|---|---|---|
| Entity selector + data quality preview (Component 1) | `docs/process/intents/M14-G4-YYYY-MM-DD-adr016-frontend.md` | `frontend/tests/e2e/m14-g4-adr016-frontend.spec.ts` (Playwright) | No — author after intent document, before implementation PR |
| Grounding strip (Component 2) | (same intent document) | (same test file) | No — author after intent document, before implementation PR |
| Parameter persistence (Component 4) | (same intent document) | (same test file) | No — author after intent document, before implementation PR |
| IC-4 Fidelity header (M14 mitigation) | (same intent document) | (same test file) | No — author after intent document, before implementation PR |
| IC-6 choropleth header | (same intent document) | (same test file) | No — author after intent document, before implementation PR |
| "None" framework filter | (same intent document) | (same test file) | No — author after intent document, before implementation PR |

**Test authorship notes:**
- ADR-016 §UX-3 specifies four falsifiable acceptance criteria (criteria 1–4). All four
  must appear as Playwright tests in `m14-g4-adr016-frontend.spec.ts`. No criterion in §UX-3
  is optional.
- Each test must use the `data-testid` values specified in the intent document. Tests must not
  assert on CSS class names, element positions, or implementation internals.
- Silent failure tests: the test suite must include tests for each of the three silent failure
  states specified in ADR-016 §Silent Failure Mode (API unavailable for Component 1; empty
  frameworks for Component 2; missing parameters for Component 4). These require API mocking
  or fixture scenarios at the Playwright level.
- The "None" framework filter test: load a pre-G3 scenario or one with only `"None"`-keyed
  attributes; assert the grounding strip does not render a section labelled with blank or
  "None."
- Fixture requirement: a completed JOR scenario (or fixture scenario with `/initial-state`
  data) is required for Component 2 and Component 4 tests. The QA Lead must confirm whether
  the G3 `68b31277` JOR scenario remains valid as a test fixture or whether a new scenario
  must be created in the test setup.

---

## Section 3 — Scope Declaration

### 3.1 — Deliverables in scope

G4 is an ADR-implementation group with no GitHub issue numbers directly assigned. G4 is the
frontend half of ADR-016 Scenario Grounding Architecture. All five deliverables below must be
in the same G4 PR (Frontend Architect recommendation — all touch overlapping component trees
in `ScenarioCreationPanel.tsx` and Zone 0/Zone 2 surface areas; sequential PRs would create
merge conflict risk).

| Deliverable | ADR section | Priority | Observable application state |
|---|---|---|---|
| Entity selector — scenario creation form | ADR-016 §Component 1 | immediate | `[data-testid="data-quality-preview"]` visible after entity + year selection; contains entity code and at least one T1–T5 tier label — ADR-016 §UX-3 criterion 1 |
| Data quality preview panel — synthetic flag | ADR-016 §Component 1 | immediate | For entities with T4 synthetic data (ZMB ecological), the word "synthetic" appears verbatim in `[data-testid="data-quality-preview"]` — ADR-016 §UX-3 criterion 2 |
| Grounding strip — button + panel | ADR-016 §Component 2 | immediate | With JOR scenario loaded, clicking "Grounding ▼" opens `[data-testid="grounding-strip"]` within 3 seconds containing at least one indicator row with non-empty source citation — ADR-016 §UX-3 criterion 3 |
| Parameter persistence display | ADR-016 §Component 4 | immediate | With any completed scenario, clicking mode chip opens `[data-testid="scenario-parameters"]` showing fiscal multiplier, base year, entity, and n_steps — ADR-016 §UX-3 criterion 4 |
| IC-4 mitigation — static Fidelity panel header | ADR-016 EL Decision 2 | immediate | Fidelity panel contains `[data-testid="fidelity-contextualisation"]` with static header text clarifying the panel validates model relationships, not input data for the active scenario |
| IC-6 mitigation — choropleth reference header | ADR-016 EL Decision 5 | immediate | Choropleth panel contains a header stating "Reference data — not scenario outputs" (verbatim per EL Decision 5 ruling) |
| "None" framework filter | G3 BPO ACCEPT forwarded observation | immediate | Grounding strip does not render a section for the `"None"` framework key; only named frameworks (financial, human_development, ecological, governance, political_economy) are displayed |

**G4's north star obligation (ADR-016 §North Star Test / P-7 full delivery):**
After G4 lands on top of G3's API layer, Persona 2 can open the Grounding strip, see
"Reserve coverage: 7.1 months · CBJ 2023-Q4 · T2" for the Jordan scenario, and respond
to an input challenge with a source citation within 90 seconds. G3 confirmed the data
exists; G4 puts it on screen.

**Demo 5 prerequisite:** G4 is required for Demo 5 (Issue #843). The north star scenario
(Zambian finance ministry analyst responding to an input challenge) requires the Grounding
strip to be visible and populated. Without G4, Demo 5 can proceed only by having the analyst
open a raw API response — not a viable demo scenario.

### 3.2 — Deliverables explicitly out of scope

| Scope item | Rationale for exclusion |
|---|---|
| ADR-016 Component 3 — Fidelity contextualisation with analogous-case selection | Deferred to M15 by EL Decision 2 (2026-06-16). Chief Methodologist analogous-case selection logic is not available in M14. Static header only (IC-4 mitigation) ships in M14. |
| G4 unit tests for new React components | Playwright E2E tests cover observable application states; unit tests for stateless presentational components are not required at the sprint entry gate. Frontend Architect Agent may add them but they are not an entry precondition. |
| G5 — ADR-015 Evidence Thread frontend | Separate sprint group; no frontend dependency on G4. G5 touches Zone 1 instruments (trajectory view, MDA alert panel) — separate component trees from G4's Zone 0/Zone 2 surfaces. |
| Choropleth full information architecture refactor (IC-6 full closure) | M15+ per EL Decision 5. G4 delivers the header label only. |
| Per-cohort initial state disaggregation in Grounding strip | ADR-016 §Known Limitations — M15+. Grounding strip shows nation-level indicators only. |
| Zone 1A layout changes | Separate concern — #845 (Zone 1A Phase 1 design thinking, G6c). Not in G4 scope. |

---

## Section 4 — ADR Prerequisite Summary

| Group | ADR required | ADR status | G3 gate | Implementation may begin? |
|---|---|---|---|---|
| G4 | ADR-016 — Scenario Grounding Architecture | **Accepted 2026-06-16 (PR #967)** | **SATISFIED 2026-06-17 (PR #1012)** | **After EL approval of this entry document** |

**Implementation sequencing for G4:**

1. EL approves this entry document (this step)
2. Frontend Architect Agent authors intent document `docs/process/intents/M14-G4-YYYY-MM-DD-adr016-frontend.md`
   from ADR-016 §UX-3 criteria 1–4, §Silent Failure Mode, §Component 2 "None" filter
   constraint, and §Component 4 "(not recorded)" fallback — **must complete before Step 3**
3. QA Lead Agent authors `frontend/tests/e2e/m14-g4-adr016-frontend.spec.ts` from intent
   document acceptance criteria — **must complete before Step 4 (implementation)**
4. Frontend Architect Agent authors implementation:
   - Entity selector in scenario creation form (replaces hardcoded GRC)
   - Data quality preview panel with live `/data-quality` API call on entity + year change
   - Grounding strip button ("Grounding ▼") in Zone 0/Zone 2 area adjacent to "Fidelity ▼"
   - Grounding strip panel (reads `/initial-state`; renders per-framework indicator cards;
     filters `"None"` framework; shows silent failure fallback per ADR-016 §Silent Failure Mode)
   - Parameter persistence display (reads `scenario.configuration`; shows "(not recorded)"
     for absent fields per ADR-016 EL Decision 4)
   - IC-4 mitigation: static Fidelity panel header (no new API call)
   - IC-6 mitigation: choropleth reference header label
5. Implementation PR opens targeting `release/m14` with branch name `feat/m14-g4-adr016-frontend`
6. Frontend Architect Agent Step 4 Verify: dev server at 1440×900; confirms all §UX-3 criteria
   pass (entity selector visible, data quality preview shows T-labels, "Grounding ▼" opens
   grounding strip, parameter display opens from mode chip); confirms silent failure states
   render fallback text; confirms "None" framework does not render
7. Business PO Step 5 Validate: confirms north star scenario — opens ZMB or JOR scenario,
   opens Grounding strip, reads indicator with source citation within 90-second ceiling;
   Customer Agent Layer 3 assessment on record before verdict

**Step 4 note for Frontend Architect Agent:** The dev server will be running the G3 migration
already applied. If running locally without Docker, confirm `alembic upgrade head` has been
run in the API container before attempting to verify the data quality preview and grounding
strip endpoints. See G3 intent doc §8 Step 4 observation.

---

## Section 5 — Near-Miss Sweep

**Near-miss sweep date:** 2026-06-17
**Sweep period:** G3 sprint entry approval (2026-06-17) through G4 sprint entry filing (2026-06-17)

| Finding | Category | PI Agent register call issued? | NM entry number |
|---|---|---|---|
| G3 Step 4 Verify: migration not pre-applied at initial probe (500 error until `alembic upgrade head`). The implementing agent's commit noted `ruff check . ✓` and `mypy app/ ✓` but did not record a live endpoint probe as Step 4 evidence. Recorded as a Step 4 discipline observation in intent doc §8. Not a near-miss threshold — CI would catch this; no systematic process gap. | Step 4 discipline note — not near-miss threshold | No | N/A |
| No findings meeting near-miss threshold in the G3-exit → G4-entry sweep period. | — | No | N/A |

*Sweep period is same session as G3 exit. G3 exit document (2026-06-17) confirmed no rejections,
no near-miss obligation from rejections. The G3 Step 4 migration observation does not meet the
near-miss threshold (process failure would require CI to pass with broken observable state; CI
would have caught the 500 — the gap is in the pre-push verification protocol, not the overall
safety net). Recorded as institutional learning in intent doc §8.*

---

## EL Approval Record

**EL approval:** 2026-06-17

> G4 sprint entry approved. All entry invariants satisfied: release branch exists, CI trigger
> verified, sprint plan EL-approved, ADR-016 Accepted, G3 gate satisfied (AC-1 and AC-6
> confirmed in running application). Intent document and QA tests required before
> implementation PR opens — frontend Architect Agent authors intent doc next, QA Lead authors
> tests from it before any implementation code is written.
> — @PublicEnemage (2026-06-17)
