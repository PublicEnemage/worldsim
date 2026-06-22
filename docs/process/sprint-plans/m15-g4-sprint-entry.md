---
name: m15-g4-sprint-entry
type: sprint-entry
milestone: M15 — Human Cost Architecture
sprint-group: G4
status: EL Approved 2026-06-22 — intent document, DA decisions, Architect confirmation, CM logic, and QA tests must be on record before implementation begins
authored-by: PM Agent
authored-date: 2026-06-22
el-approved: 2026-06-22
release-branch: release/m15
sop-reference: docs/process/sprint-planning-sop.md
---

# Sprint Entry — M15, G4: Path 1 + ADR-016 Component 3

**Status:** EL Approved 2026-06-22 — intent document, DA decisions, Architect confirmation, CM analogous-case logic, and QA tests must be on record before implementation begins
**Date authored:** 2026-06-22
**Release branch:** `release/m15`
**Sprint plan:** `docs/process/sprint-plans/m15-sprint-plan.md` (EL Approved 2026-06-20; amended 2026-06-21 — G4 scope confirmed post-AC-001)

*Authority: `docs/process/sprint-planning-sop.md §Sprint Entry Gate` (Phase C output).
This entry gates G4 specifically. G4 is a parallel sprint — no other sprint group is
sequentially blocked on G4, but G4 deliverables are prerequisites for G8 (#843 live external
demo) indirectly through the overall M15 exit conditions (#975 and Component 3 are in the
M15 exit scope). No implementation PR may open against `release/m15` for G4 until this entry
document is EL-approved and the intent and QA gates below are satisfied.*

*Pre-implementation gate note: Two within-sprint prerequisites must be resolved before G4
implementation code is written: (1) Architect confirmation that #975 is within ADR-016
Component 1 scope or identification of an ADR amendment requirement; (2) Chief Methodologist
definition of the analogous-case selection logic for ADR-016 Component 3. These are blocking
conditions for implementation, not for this entry document or EL approval.*

---

## Section 1 — Sprint Identification

| Field | Value |
|---|---|
| Milestone | M15 — Human Cost Architecture |
| GitHub Milestone | #16 |
| Sprint group | G4 — Path 1 + ADR-016 Component 3 |
| Release branch | `release/m15` |
| Sprint plan document | `docs/process/sprint-plans/m15-sprint-plan.md` |
| Exit checklist issue | #984 |
| Sprint groups in scope | G4 only |
| ADR gate | ADR-016 ✅ (accepted 2026-06-16); see §2.2 for within-sprint Architect confirmation gate |
| Implementing agents | Data Architect Agent (backend API, source query mechanism); Frontend Architect Agent (creation form extension, Fidelity panel contextualisation); Chief Methodologist (analogous-case selection logic — pre-implementation gate for Component 3) |
| Wave | Parallel (G1 ✅ complete; no sequential dependency on G2, G3, G5, G6, G7) |
| Issues in scope | #975 (Path 1 — approved source network query); ADR-016 Component 3 (Fidelity panel contextualisation) |
| Hard stop cleared | ✅ 2026-06-21 — constraints PR #1102 merged to `release/m15` (AC-001 + AC-002; #53 permanently closed; G4 scope confirmed as #975 + ADR-016 Component 3 only) |

---

## Section 2 — Entry Invariants Checklist

*All items must be checked before any implementation PR is opened for G4.
An unchecked invariant blocks implementation from beginning.*

### 2.1 — Structural gates

- [x] **Release branch exists:** `release/m15` cut from `main` 2026-06-20 (commit 500e50d)
- [x] **CI trigger verified:** `.github/workflows/ci.yml` `pull_request: branches` includes
  `release/m*` — confirmed 2026-06-20 (line 5: `branches: [ main, develop, release/m* ]`;
  line 7: `branches: [ main, release/m* ]`). Ruleset ID 17751852 with 6 required checks:
  `changes`, `lint`, `test-backend`, `playwright-e2e`, `compliance-scan`, `branch-naming`.
  KI-005 permanent fix (`do_not_enforce_on_create: true`) applied 2026-06-20.
- [x] **Sprint plan EL-approved:** `docs/process/sprint-plans/m15-sprint-plan.md`
  `el-approved: 2026-06-20` (PR #1094 — EL approval recorded 2026-06-20); amended 2026-06-21
  confirming G4 scope as #975 + ADR-016 Component 3 only (AC-001 removes #53).
- [x] **Constraint record PR merged:** PR #1102 merged to `release/m15` 2026-06-21
  (AC-001 private data prohibition + AC-002 synthetic substitution; #53 permanently closed;
  G4 scope confirmed). Hard stop cleared.

### 2.2 — ADR prerequisite gate

G4 delivers two distinct capabilities, both within the scope of the accepted ADR-016
(Scenario Grounding Architecture, accepted 2026-06-16):

**#975 (Path 1 — extends ADR-016 Component 1):**
Issue #975 explicitly states "An ADR or ADR amendment is required before implementation
begins; scope TBD at M15 planning." The sprint plan places #975 under "ADR-016 ✅" as an
extension of Component 1 (entity selection and pre-creation data quality preview). The
extension adds two capabilities to the existing Component 1 surface: (a) entity selector
searches beyond the four preloaded entities to all registered source coverage entities;
(b) data quality preview distinguishes "loaded" vs. "available — click to load" states,
with a data pull action for non-preloaded entities.

**Architect prerequisite (within-sprint step):** Before G4 implementation code is written,
the Architect Agent must confirm whether the #975 scope — specifically the `/data-availability`
endpoint or a new `loadable` field on `/data-quality`, and the data pull trigger mechanism —
is within ADR-016 Component 1 scope or constitutes a material extension requiring an ADR
amendment. This determination is made at intent authorship time and recorded in the intent
document. If an amendment is required, the amendment must be EL-accepted before the G4
implementation PR opens for #975.

**ADR-016 Component 3 (Fidelity panel contextualisation):**
Component 3 design is fully specified in ADR-016 §Component 3. No new ADR is required.
The Frontend Architect note in the sprint plan confirms: "No new ADR required — the design
is in ADR-016 §Component 3."

**Chief Methodologist pre-implementation gate (Component 3):** ADR-016 §Component 3 is
explicit: "Component 3 (analogous case selection) is a methodology commitment that the Chief
Methodologist must define and validate. An ADR cannot specify what this logic is — only that
it must exist before Component 3 can be implemented." The CM must define the similarity
algorithm (which crisis mechanism types, which entity-characteristic matching criteria)
before Component 3 implementation begins. This definition is required in the intent document
as a Decision gate; implementation of Component 3 is blocked until the CM definition is
on record (comment on #975 or as a filed methodology note referenced in the intent document).

| Issue / Component | Required ADR | ADR status | Gate |
|---|---|---|---|
| #975 (Path 1 — Component 1 extension) | ADR-016 Component 1 | Accepted 2026-06-16; Architect confirms scope before impl | **CLEAR for entry; within-sprint Architect confirmation required before impl** |
| ADR-016 Component 3 (Fidelity contextualisation) | ADR-016 Component 3 | Accepted 2026-06-16 | **CLEAR for ADR gate; BLOCKED for impl until CM analogous-case logic defined** |

- [ ] All G4 ADR prerequisites satisfied for implementation to begin — **BLOCKED pending: (1) Architect scope confirmation for #975; (2) CM analogous-case logic for Component 3. Both must be on record before implementation PRs open.**

### 2.3 — Intent document gate

*An intent document must be filed before any G4 implementation PR opens.
(Authority: CLAUDE.md §Agent Execution Lifecycle Step 1)*

- [ ] Intent document filed for G4 deliverables — **MUST FILE BEFORE IMPLEMENTATION PR OPENS**

| Deliverable | ADR reference | Intent document path | Filed? |
|---|---|---|---|
| #975 — Path 1 approved source network query (entity selector + data pull) | ADR-016 Component 1 (extension) | `docs/process/intents/M15-G4-2026-06-22-path1-fidelity-contextualisation.md` | No — BLOCKING |
| ADR-016 Component 3 — Fidelity panel contextualisation | ADR-016 Component 3 | (same intent document) | No — BLOCKING |

Both G4 deliverables may be covered by a single intent document
(`M15-G4-2026-06-22-path1-fidelity-contextualisation.md`). The intent document must:
- Derive acceptance criteria from the observable application states in Section 3.1 below
- Document the Architect's ADR scope confirmation for #975 (or flag an amendment requirement)
- Record the CM's analogous-case selection logic for Component 3 as a pre-implementation
  Decision gate (Section 3 of the intent template: "Decisions Required")
- Record the Data Architect's `api_contracts.yml` decision for any new G4 endpoints
- Complete the Kryptonite Constraint Check (Section 5 of the intent template): confirm that
  the entity selector search, "available/loadable" state, and Fidelity contextualisation
  section are all interpretable by a finance ministry economist without specialist mediation

**Completeness gate:** The QA Lead must be able to write Playwright and backend tests for
both deliverables from the intent document without reading any implementation code. The intent
document's acceptance criteria must specify observable application states — not function
return values or implementation contracts.

### 2.4 — QA test authorship gate

*QA tests must be authored from the intent document's acceptance criteria before
implementation code is written. G4 is a full-stack sprint — backend tests cover the
source query API and data pull mechanism; frontend Playwright tests cover the creation form
and Fidelity panel.
(Authority: CLAUDE.md §Agent Execution Lifecycle Step 2)*

- [ ] QA test files authored for G4 before implementation begins — **MUST FILE BEFORE IMPLEMENTATION BEGINS**

| Deliverable | Intent document | Test file path | Authored before implementation? |
|---|---|---|---|
| #975 (backend: source query API, data pull mechanism) | `docs/process/intents/M15-G4-2026-06-22-path1-fidelity-contextualisation.md` | `backend/tests/test_m15_g4_path1_fidelity_contextualisation.py` | No — BLOCKING |
| #975 + Component 3 (frontend: creation form + Fidelity panel) | (same intent document) | `frontend/tests/e2e/m15-g4-path1-fidelity-contextualisation.spec.ts` | No — BLOCKING |

**Expected backend test coverage:**
- `/data-quality` or `/data-availability` endpoint returns a `loadable` status for at least
  one entity with registered source coverage but no preloaded data
- Data pull trigger endpoint creates a scenario record with the same provenance contract as
  admin-preloaded data (source_institution, vintage, confidence tier)
- ADR-007 synthetic fallback: `/data-quality` returns T3/T4 provenance for an entity with
  no registered source coverage
- `analogous_case` API field or endpoint returns one of the five validated historical cases
  (GRC, ARG, LBN, THA, ECU) for a loaded scenario; fallback response when no case matches

**Expected frontend test coverage (Playwright):**
- Entity selector in creation form: searching an entity beyond the four preloaded ones returns
  a result (not an empty dropdown)
- `[data-testid="data-quality-preview"]` contains text matching "available" or "loadable"
  for a non-preloaded entity
- `[data-testid="fidelity-contextualisation"]` is visible (not a tooltip or hover state) with
  a ZMB scenario loaded; contains "ZMB" or "Zambia"; references a historical case name
- Fallback: `[data-testid="fidelity-contextualisation"]` renders with "No analogous validation
  case identified" when no case matches (section must always render when a scenario is active)

---

## Section 3 — Scope Declaration

### 3.1 — Issues in scope

| Issue | Title | Priority | Observable application state (pre-implementation specification) |
|---|---|---|---|
| #975 | feat(data): Path 1 — approved source network query at scenario creation | immediate | (a) The scenario creation form entity selector, when a user types the name or ISO code of a country not currently preloaded (e.g., "SEN", "Senegal", "PAK", "Pakistan"), returns at least one matching result in the dropdown — demonstrating that the selector searches registered source coverage, not only the preloaded entity set. (b) With a non-preloaded entity and a year selected, `[data-testid="data-quality-preview"]` renders and contains a status indicator distinguishing "loaded" (preloaded data present) from "available — click to load" (registered source has coverage; pull not yet triggered) for at least one framework row. (c) Clicking the load/pull action produces a visible progress state (`[data-testid="data-pull-progress"]` visible or equivalent) within 5 seconds; the pull completes within 5 minutes for a standard World Bank or IMF coverage entity. (d) After the pull, `GET /api/v1/scenarios/{id}/trajectory` for a scenario created from a pulled entity returns a valid response with the same `outputs` structure as admin-preloaded entities — reserve_coverage_months, programme_survival_probability, etc. (e) For an entity with no registered source coverage, `[data-testid="data-quality-preview"]` contains text matching "T3", "T4", or "synthetic" — ADR-007 synthetic fallback activated and disclosed. (f) A user completing the full flow (entity search → non-preloaded selection → year entry → pull → scenario creation) for Senegal 2023 can create a runnable scenario within 5 minutes without any admin intervention. |
| ADR-016 Component 3 | ux(fidelity): Fidelity panel contextualisation (deferred from M14 G4) | immediate | (a) With any scenario loaded (GRC, JOR, EGY, or ZMB), the Fidelity panel contains an element `[data-testid="fidelity-contextualisation"]` that is visible at L0 — without hover, click, or interaction beyond opening the Fidelity panel. (b) The contextualisation section text contains the active scenario's entity identifier (e.g., "ZMB" or "Zambia") and a reference to one of the five validated historical cases: GRC, ARG, LBN, THA, ECU — naming the case and its relevance (crisis mechanism type or structural similarity). (c) When no analogous validation case is identified for the active entity's crisis mechanism type, `[data-testid="fidelity-contextualisation"]` still renders and contains the text "No analogous validation case identified for this scenario type. Global backtesting results apply — see validation cases below." The section is never absent when a scenario is active. (d) Playwright: with ZMB scenario loaded, `expect(page.locator('[data-testid="fidelity-contextualisation"]')).toBeVisible()` and the locator's text content contains "ZMB" or "Zambia" and at least one of: "Greece", "GRC", "Argentina", "ARG", "Lebanon", "LBN", "Thailand", "THA", "Ecuador", "ECU". |

### 3.2 — Issues explicitly out of scope

G4's scope is bounded to #975 (Path 1 source query extension to Component 1) and ADR-016
Component 3 (Fidelity contextualisation). The following are explicitly excluded:

| Issue / scope | Rationale for exclusion |
|---|---|
| #53 — RBAC design | ✅ CLOSED 2026-06-21 — will-not-implement (AC-001, permanent prohibition); removed from G4 scope |
| #976 — Path 2 proprietary data upload | ✅ CLOSED 2026-06-21 — will-not-implement (AC-001) |
| ADR-016 Component 2 (Grounding strip) | ✅ Complete in M14 G4 (PR #1015); not in G4 scope |
| ADR-016 Component 1 base entity selector for GRC/JOR/EGY/ZMB | ✅ Complete in M14 G3/G4; G4 extends to all registered-source entities |
| ADR-016 Component 4 (Parameter persistence) | ✅ Complete in M14 (PR #1015 ModeSelector onWrapperClick fix) |
| #845 — Zone 1A ADR-017 | G2 scope — Architecture Review + ADR-017 authorship |
| #986/#987 — Cohort disaggregation / political risk surface | G3 design scope (✅ design complete M15); implementation M16 |
| ADR-007 full synthetic data framework implementation | Pre-existing; G4 activates and surfaces the existing ADR-007 fallback path — it does not implement ADR-007 |
| #990 — Accessibility validation | G6 scope |
| G1 (#1065, #1066, #1068, #1069, #1075) | ✅ Complete 2026-06-21 (PR #1097) |
| IC-6 — choropleth disconnect | Static header mitigation applied M14; full resolution deferred per ADR-016 |
| Admin source onboarding / license verification | The admin process remains unchanged; G4 does not modify it |

G4 is complete when: (a) a user can search registered source coverage entities beyond the
four preloaded ones in the creation form; (b) the data quality preview distinguishes
"loaded" vs. "available/loadable" for non-preloaded entities; (c) a data pull can be
triggered and completes within 5 minutes; (d) the Fidelity panel contextualisation section
renders for all four entities with an analogous historical case reference or the defined
fallback message; AND (e) Business PO has confirmed (Step 5 Validate) that Eleni (Persona 2
— Finance Ministry Negotiator) can create a scenario for an entity outside the preloaded set
within the 5-minute Preparatory entry state ceiling and that the Fidelity contextualisation
section gives her actionable trust calibration without specialist mediation.

---

## Section 4 — ADR Prerequisite Summary

| Group | ADR required | ADR status | Implementation may begin? |
|---|---|---|---|
| G4 — #975 (Path 1, Component 1 extension) | ADR-016 Component 1 (extension) | ADR-016 accepted 2026-06-16; Architect scope confirmation required | **Yes — after EL approves this entry, intent doc filed, QA tests filed, and Architect confirms within-scope (or amendment EL-accepted)** |
| G4 — ADR-016 Component 3 (Fidelity contextualisation) | ADR-016 Component 3 | ADR-016 accepted 2026-06-16; no new ADR needed | **Yes for intent/QA authorship; implementation BLOCKED until CM defines analogous-case selection logic** |

**Implementation sequencing for G4:**

1. EL approves this entry document
2. Data Architect Agent and Architect Agent jointly author the intent document at
   `docs/process/intents/M15-G4-2026-06-22-path1-fidelity-contextualisation.md`:
   - Architect confirms #975 is within ADR-016 Component 1 scope or flags amendment requirement
   - Data Architect documents new endpoint decisions (DA-G4-1: whether `/data-availability`
     is a new endpoint or a `loadable` field on the existing `/data-quality` response)
   - Data Architect updates `docs/schema/api_contracts.yml` for any new endpoints before
     implementation begins (sprint plan requirement)
   - Chief Methodologist analogous-case logic decision recorded as Decision gate in intent
     document (must precede Component 3 implementation)
3. QA Lead authors both test files from intent document acceptance criteria before
   implementation code is written
4. Chief Methodologist defines analogous-case selection logic (similarity algorithm for
   Component 3) — comment on #975 or as a filed methodology note referenced in the intent doc
5. If Architect confirms #975 requires an ADR amendment: amendment drafted, panel sign-offs
   obtained, EL accepts amendment — then implementation may begin
6. Backend implementation PR opens targeting `release/m15` with milestone-scoped branch name
   (`feat/m15-g4-path1-backend` or equivalent); Data Architect Agent authors
7. Frontend implementation PR opens targeting `release/m15` (`feat/m15-g4-path1-frontend` or
   equivalent); Frontend Architect Agent authors; may open in parallel with backend PR or
   after, depending on endpoint readiness
8. Data Architect Agent (backend) + Frontend Architect Agent (frontend) Step 4 Verify:
   confirm all observable application states from Section 3.1 are present in the running
   application before marking PRs ready for review
9. Customer Agent Layer 3 assessment required before Business PO verdict is final (Persona 2
   — Eleni as finance ministry negotiator creating a non-preloaded scenario; Persona 2 also
   for Fidelity contextualisation confirming trust calibration without mediation)
10. Business PO Step 5 Validate:
    - For #975: confirms Eleni can create a scenario for a non-preloaded entity within the
      5-minute Preparatory entry state ceiling; confirms "available/loadable" state is
      unambiguous without presenter explanation; confirms pull failure shows a visible fallback
    - For Component 3: confirms the Fidelity contextualisation section provides actionable
      trust calibration — the finance ministry analyst can identify the most analogous
      historical case and the direction of the model's validation for her entity's crisis
      mechanism without requiring methodology specialist mediation
11. G4 sprint exit document filed

**Data Architect pre-implementation decisions (to be recorded in intent document):**

| Decision ID | Question | Authority | Required before |
|---|---|---|---|
| DA-G4-1 | New `/data-availability` endpoint vs. `loadable` flag on existing `/data-quality` response | Data Architect Agent | G4 backend implementation begins |
| DA-G4-2 | Data pull trigger endpoint design (sync/async, timeout handling, progress mechanism) | Data Architect Agent | G4 backend implementation begins |
| DA-G4-3 | `api_contracts.yml` update for any new G4 endpoints | Data Architect Agent | G4 frontend implementation begins (sprint plan requirement) |
| DA-G4-4 | Analogous-case data field: embedded in existing endpoint vs. new `GET /scenarios/{id}/analogous-case` endpoint | Data Architect Agent | Component 3 implementation begins |

**Kryptonite constraint check (pre-implementation gate):**
The intent document Section 5 must confirm that:
(a) A finance ministry analyst (not a data architect) can read the "available — click to load"
    state in the data quality preview and understand what it means and what to do — without
    tooltip, without documentation, within 30 seconds
(b) The Fidelity contextualisation section tells the analyst *what* the historical case
    means for her scenario — not just *which* case is most analogous — in plain language
    the analyst can use at the table without calling in a methodologist
If either check fails in the intent document, the implementing agent must redesign the output
before implementation begins.

---

## Section 5 — Near-Miss Sweep

**Near-miss sweep date:** 2026-06-22
**Sweep period:** Since M15-G3 sprint closure (2026-06-22 — same session)

| Finding | Category | PI Agent register call issued? | NM entry number |
|---|---|---|---|
| No process gaps identified in the sweep period. G3 was design-only; 45/45 QA tests passed before commit; no new near-misses arose. NM-052 (mypy gate non-executable locally) was filed during M15-G3 in a prior session and is already on record. Constraint record (AC-001 + AC-002) filed as EL architectural decisions — positive scope clarifications; not near-miss material. | N/A | N/A | N/A |

---

## EL Approval Record

**EL approval:** 2026-06-22

> G4 sprint entry approved. Structural gates confirmed clear — release branch exists, CI trigger verified, sprint plan EL-approved (amended 2026-06-21), constraint record PR #1102 merged. ADR gate clear: ADR-016 accepted 2026-06-16; both Component 1 extension (#975) and Component 3 (Fidelity contextualisation) are within ADR-016 scope per sprint plan. Three within-sprint prerequisites correctly documented as blocking implementation (not blocking this approval): (1) Architect scope confirmation on whether #975 requires an ADR amendment; (2) CM analogous-case selection logic definition before Component 3 implementation; (3) Data Architect API decisions (DA-G4-1–4) and `api_contracts.yml` update. Implementing agents confirmed: Data Architect (backend) + Frontend Architect (frontend). Intent document and QA test files must be filed before implementation begins — these remain blocking conditions. Kryptonite constraint check in intent document Section 5 is required before implementation.
> — @PublicEnemage (2026-06-22)
