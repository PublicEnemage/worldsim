---
name: m14-g5-sprint-entry
type: sprint-entry
milestone: M14 — Methodology Publication and External Validation
sprint-group: G5
status: Filed — awaiting EL approval
authored-by: PM Agent
authored-date: 2026-06-17
el-approved: 2026-06-17
release-branch: release/m14
sop-reference: docs/process/sprint-planning-sop.md
---

# Sprint Entry — M14, G5: ADR-015 Evidence Thread Architecture (Components 1, 2, 3)

**Status:** EL Approved — 2026-06-17
**Date authored:** 2026-06-17
**Release branch:** `release/m14`
**Sprint plan:** `docs/process/sprint-plans/m14-sprint-plan.md` (EL Approved 2026-06-16)

*Authority: `docs/process/sprint-planning-sop.md §Sprint Entry Gate` (Phase C output).
This entry gates G5 specifically. G5 is the ADR-015 Evidence Thread Architecture implementation
group — L0 basis annotations on Zone 1 primary outputs (Component 1), the Assumption Surface
(Component 2), and programme_survival_probability in Zone 1D (Component 3). Component 4
(cross-examination mode) is deferred to M15. G5 is gated on G2 (ADR-015 Accepted —
COMPLETE 2026-06-16, PR #998) and on Decision 1 from ADR-015 §Decisions Required (step
counter bug — COMPLETE 2026-06-17, PR #1006).*

---

## Section 1 — Sprint Identification

| Field | Value |
|---|---|
| Milestone | M14 — Methodology Publication and External Validation |
| GitHub Milestone | #15 |
| Sprint group | G5 — ADR-015 Evidence Thread Architecture (Components 1, 2, 3) |
| Release branch | `release/m14` |
| Sprint plan document | `docs/process/sprint-plans/m14-sprint-plan.md` |
| Exit checklist issue | #968 |
| Sprint groups in scope | G5 only |
| ADR gate | ADR-015 — Evidence Thread Architecture ✅ Accepted 2026-06-16 (PR #998) |
| G2 gate | G2 COMPLETE ✅ — ADR-015 Accepted 2026-06-16 (PR #998); 6 EL decisions recorded |
| Decision 1 gate | Step counter bug (#962) FIXED ✅ — G1 COMPLETE 2026-06-17 (PR #1006) |
| Implementing agent | Frontend Architect Agent (Components 1, 2, 3); Data Architect Agent (C — API field availability assessment and api_contracts.yml; see §2.2 backend note) |

---

## Section 2 — Entry Invariants Checklist

*All items must be checked before any implementation PR is opened for G5.
An unchecked invariant blocks implementation from beginning.*

### 2.1 — Structural gates

- [x] **Release branch exists:** `release/m14` cut from `main` 2026-06-16
- [x] **CI trigger verified:** `.github/workflows/ci.yml` `pull_request: branches` includes
  `release/m*` — confirmed 2026-06-16 (Ruleset ID 17751852 with 6 required checks: `changes`,
  `lint`, `test-backend`, `playwright-e2e`, `compliance-scan`, `branch-naming`)
- [x] **Sprint plan EL-approved:** `docs/process/sprint-plans/m14-sprint-plan.md`
  `el-approved: 2026-06-16`

### 2.2 — ADR prerequisite gate

G5 implements ADR-015 §Component 1 (basis threads on Zone 1 primary outputs), §Component 2
(assumption surface), and §Component 3 (programme_survival_probability in Zone 1D). It does
not implement §Component 4 (cross-examination mode — M15).

**ADR-015 Decision 1 prerequisite (step counter):** ADR-015 §Decisions Required explicitly
states that the step counter bug must be fixed before any ADR-015 legibility work begins
("every basis annotation (which step does this apply to?) is undermined" if the counter is
wrong). This is satisfied by G1 COMPLETE 2026-06-17 (PR #1006, #962 closed).

**G4 relationship:** G5 is not gated on G4. ADR-015 frontend (Zone 1 instruments —
trajectory view, MDA alert panel, Zone 1D) is a separate component tree from ADR-016
frontend (Zone 0/Zone 2 — scenario creation form, identity header). The Frontend Architect
confirmed no merge conflict risk if G4 merges first. G4 is now COMPLETE (PR #1015, #1016,
#1018), so G5 may proceed immediately after EL approval of this entry document.

**Backend API data assessment (required at intent authorship):** ADR-015 §Chief Engineer
consultation states "no new endpoint requirements — it surfaces existing measurement output
data through a new UI layer, relying on existing API endpoints." However, the L0 basis
annotations on Zone 1D require per-framework data that may not currently be in the trajectory
endpoint response:
- Component 1 (Zone 1D annotation `[T2 · 4 indicators · IMF/Central Bank 2024]`): needs
  minimum-confidence tier, indicator count, and primary source for each framework at the
  current step. The `/initial-state` endpoint (G3) has this at step 0; the trajectory endpoint
  may not carry it for subsequent steps.
- Component 2 (assumption surface): needs fiscal multiplier, PE enabled, conditionality type,
  data vintage from scenario configuration — these are available in the existing scenario
  configuration object; the "3–4 highest-sensitivity inputs from sensitivity attribution"
  fallback may require a backend enhancement or be derived client-side from scenario config.
- Component 3 (`programme_survival_probability`): this value is already present in the
  trajectory response from the political economy module (G6, M13). No backend change required.

**The implementing agent must determine at Step 1 (intent authorship) whether Components 1 and
2 require new fields on existing endpoints.** If they do, those fields must be scoped in the
intent document and Data Architect Agent must confirm the contract and update `api_contracts.yml`
before the implementation PR opens. "No new endpoint" does not mean "no backend change" —
adding fields to existing responses is within scope. The intent document must name the exact
API fields consumed for each Component. The Data Architect holds R on `api_contracts.yml`;
no field may be consumed by the frontend without a matching entry in that file.

| Group | Required ADR | ADR status | Decision 1 gate | G4 gate | Gate |
|---|---|---|---|---|---|
| G5 | ADR-015 — Evidence Thread Architecture | **Accepted 2026-06-16 (PR #998)** | **SATISFIED 2026-06-17 (PR #1006, #962)** | Not required (separate component tree) | **CLEAR** |

- [x] ADR-015 is Accepted. Decision 1 (step counter) satisfied. G5 gates are clear.

### 2.3 — Intent document gate

*An intent document must be filed before any G5 implementation PR opens.
(Authority: CLAUDE.md §Agent Execution Lifecycle Step 1)*

- [ ] Intent document filed for G5 deliverables — **NOT YET FILED — required before
  implementation PR opens**

| Deliverable | ADR reference | Intent document path | Filed? |
|---|---|---|---|
| Zone 1D L0 basis annotations (Component 1) | ADR-015 §Component 1; §UX-3 | `docs/process/intents/M14-G5-2026-06-17-adr015-frontend.md` | ⬜ Required |
| Zone 1B compact row full indicator names (Component 1) | ADR-015 §Component 1 §Zone 1B | (same intent document) | ⬜ Required |
| Zone 1C PMM pre-calibration annotation (Component 1) | ADR-015 §Component 1 §Zone 1C; Decision 3 | (same intent document) | ⬜ Required |
| HCL strip unit + tier meaning expansion (Component 1) | ADR-015 §Component 1 §HCL | (same intent document) | ⬜ Required |
| Assumption surface strip (Component 2) | ADR-015 §Component 2; §UX-3 | (same intent document) | ⬜ Required |
| `programme_survival_probability` in Zone 1D (Component 3) | ADR-015 §Component 3 | (same intent document) | ⬜ Required |

**Intent document completeness gate:** The QA Lead must be able to write Playwright tests for
every acceptance criterion from the intent document without reading any implementation source
code. The intent document must specify:

- Exact `data-testid` values for each new or modified element. ADR-015 §UX-3 specifies
  `data-testid="assumption-surface"` for Component 2. The intent document must assign
  `data-testid` values for: Zone 1D annotation elements, Zone 1B compact row text slots,
  Zone 1C PMM annotation, HCL tier labels, and the `programme_survival_probability` row.
- Observable application states: what the DOM contains and at what viewport, with which
  fixture scenario loaded, at which step. For Component 1, the Hormuz fixture (JOR/EGY,
  step 8) is the primary fixture per §UX-3. For Component 3, a political-economy-enabled
  scenario (e.g., the existing GRC Greece fixture with PE enabled, or the Hormuz scenario
  if PE is enabled) is required — confirm fixture availability.
- API field mapping: for each Component, name the exact API fields consumed (endpoint + field
  path). Flag any field that does not currently exist in the endpoint response — those require
  Chief Engineer confirmation before implementation begins.
- Silent failure observable states per ADR-015 §Silent Failure Mode:
  - Component 1: null tier → `[—]` annotation on affected row
  - Component 2: empty sensitivity attribution → fallback showing user-set inputs only;
    unavailable scenario config → `data-testid="assumption-surface-unavailable"` in DOM
  - Component 3: PE enabled + null survival probability → `Political Feasibility — [computation error]`
- UX constraint compliance checks:
  - Zone 1D annotations must not increase Zone 1D row height such that the four rows
    (plus Component 3 conditional fifth row) require scroll at 1280×800 (UX Concern 2)
  - Assumption surface must be single-line fixed height (max 24px) at all viewports,
    truncating with ellipsis if content overflows (UX Concern 1)
  - `programme_survival_probability` row must be suppressed entirely (not a dash) when
    PE module is not enabled (ADR-015 §Component 3)
  - PMM annotation carries `[T3 composite · pre-cal]` until Chief Methodologist files
    interpretation anchor (Decision 3 — G6 parallel deliverable); intent document must
    specify this placeholder as the observable state for the PMM row

**Implementing agent (Frontend Architect Agent):** authors the intent document, including the
API field mapping section. Chief Engineer Agent is C for any backend field availability
questions. Chief Methodologist Agent is C for the PMM annotation placeholder text.

**Component 4 is explicitly out of scope:** Cross-examination mode (keyboard shortcut `?`,
inline expansion of Zone 1B/1D, Defend button) is deferred to M15. The intent document must
not include Component 4 acceptance criteria.

### 2.4 — QA test authorship gate

*QA tests must be authored from the intent document's acceptance criteria before implementation
code is written. (Authority: CLAUDE.md §Agent Execution Lifecycle Step 2)*

- [ ] QA test file authored for G5 before implementation begins — **NOT YET FILED — required
  before implementation PR opens**

| Deliverable | Intent document | Test file path | Authored before implementation? |
|---|---|---|---|
| Zone 1D L0 annotations (Component 1) | `docs/process/intents/M14-G5-2026-06-17-adr015-frontend.md` | `frontend/tests/e2e/m14-g5-adr015-frontend.spec.ts` | No — author after intent document, before implementation PR |
| Zone 1B compact row names (Component 1) | (same intent document) | (same test file) | No — author after intent document, before implementation PR |
| Zone 1C PMM annotation (Component 1) | (same intent document) | (same test file) | No — author after intent document, before implementation PR |
| HCL tier meaning expansion (Component 1) | (same intent document) | (same test file) | No — author after intent document, before implementation PR |
| Assumption surface (Component 2) | (same intent document) | (same test file) | No — author after intent document, before implementation PR |
| `programme_survival_probability` in Zone 1D (Component 3) | (same intent document) | (same test file) | No — author after intent document, before implementation PR |

**Test authorship notes:**

- ADR-015 §UX-3 specifies two falsifiable acceptance criteria for M14 scope:
  (1) Zone 1D displays tier annotations at zero interaction (pattern `[T{N} · {source_description}]`)
  at 1280×900 with Hormuz fixture, all four rows in viewport without scroll;
  (2) assumption surface `data-testid="assumption-surface"` exists, is not display:none,
  and contains `Fiscal ×{N.NN}` when fiscal multiplier is non-default.
  Both must appear as Playwright tests. No §UX-3 criterion in M14 scope is optional.
- Component 3 test: requires a fixture with political economy enabled. The intent document
  must confirm the fixture (Greece 2012 PE-enabled, or a fresh scenario with PE enabled).
  The test must also assert the PE row is absent when PE is disabled in a separate scenario.
- Silent failure tests: all three §Silent Failure Mode states (Component 1 null tier,
  Component 2 attribution unavailable, Component 3 PE-enabled + null survival probability)
  must have Playwright tests using `page.route()` mocking to inject the failure conditions.
  See NM-045 root cause: silent failures must be tested by observable string assertions,
  not structural regex fallbacks.
- UX constraint tests (from §UX-6 and UX Concerns 1–2): at 1280×800, Zone 1B must show
  two TERMINAL alerts visible without scroll using Greece M8 Demo fixture (§UX-6 acceptance
  criterion); assumption surface must be a single rendered line with no wrapping.
- Zone 1B text truncation test: Zone 1B compact rows must show the full indicator name
  (using the 24-character abbreviation set, not mid-word truncation). Existing Zone 1B tests
  in `m14-g7-*` must pass unchanged — this is an in-place text rendering improvement, not
  a layout change.

---

## Section 3 — Scope Declaration

### 3.1 — Deliverables in scope

G5 is an ADR-implementation group with no specific GitHub issue numbers. G5 implements the
frontend of ADR-015 Evidence Thread Architecture for M14-scoped Components 1, 2, and 3.

| Deliverable | ADR section | Priority | Observable application state |
|---|---|---|---|
| Zone 1D L0 annotations — all 4 framework rows | ADR-015 §Component 1 | immediate | Each of the four framework rows in Zone 1D contains `[T{N} · {source_description}]` annotation text at zero interaction; Hormuz fixture step 8 at 1280×900; all four annotations visible in viewport without scroll — ADR-015 §UX-3 criterion 1 |
| Zone 1D L0 annotation — pre-calibration flag | ADR-015 §Component 1; Decision 3 | immediate | For any framework row where `ia1_disclosure=True`, annotation contains `· pre-cal` verbatim |
| Zone 1B compact rows — full indicator name | ADR-015 §Component 1 §Zone 1B | immediate | Zone 1B compact rows show the full indicator name (or 24-char abbreviation) rather than mid-word truncated text; two TERMINAL alerts visible in Zone 1B at 1280×800 using Greece M8 Demo fixture, both with legible full indicator names — ADR-015 §UX-6 criterion |
| Zone 1C PMM annotation — pre-calibration placeholder | ADR-015 §Component 1 §Zone 1C; Decision 3 | immediate | PMM row annotation shows `[T3 composite · pre-cal]` until Chief Methodologist interpretation anchor is filed |
| HCL strip — unit and tier meaning | ADR-015 §Component 1 §HCL | immediate | HCL indicator rows show unit in parentheses and tier meaning expanded (e.g., `-0.25 (capability index) [T4 · model estimate]`); raw tier code `T4` does not appear without expansion |
| Assumption surface strip | ADR-015 §Component 2 | immediate | `data-testid="assumption-surface"` element exists in DOM, is not display:none, and contains `Fiscal ×{N.NN}` text when fiscal multiplier differs from model default, using Hormuz fixture at step 4 — ADR-015 §UX-3 criterion 2 |
| Assumption surface — single-line constraint | ADR-015 §Component 2; UX Concern 1 | immediate | Assumption surface renders as a single line at max 24px height at all viewport widths ≥ 1280px; content truncates with ellipsis if overflow |
| `programme_survival_probability` in Zone 1D | ADR-015 §Component 3 | immediate | With PE module enabled, Zone 1D displays a fifth row labeled "Political Feasibility" showing the probability as percentage and tier — e.g., `Political Feasibility  59% [T3 · political economy module]`; row is absent (not a dash, absent entirely) when PE is not enabled |

**G5's north star obligation (ADR-015 §North Star Test / P-7 delivery):**

After G5 lands, the Zambian Finance Ministry analyst can respond to a conditionality and
political feasibility challenge at the negotiating table:
- She sees "Political Feasibility 59% [T3]" in Zone 1D at zero interaction (Component 3)
- She sees "Conditionality: standard" in the assumption surface at zero interaction (Component 2)
- She sees `[T2 · 4 indicators · IMF/Central Bank 2024]` under Financial in Zone 1D at zero
  interaction (Component 1 — L0 annotation allows her to say "this is Tier 2 — citable directly")

This satisfies the P-7 north star scenario: the analyst has response material from the screen
without activating any additional mode (Component 4 / cross-examination mode is M15).

**Demo 5 obligation:** G5 is a Demo 5 enhancer (per sprint plan BPO consultation — "ADR-016
implementation is the Demo 5 minimum; ADR-015 is Demo 5 enriched"). G5 is not on the Demo 5
critical path, but it is required for the full north star scenario. Per ADR-015 Decision 5
(Geopolitical Analyst conditional, EL accepted): the Demo 5 scenario script must be designed
so all challenges are answerable from Components 1+2+3 without composite score decomposition.
Issue #997 tracks this constraint.

### 3.2 — Deliverables explicitly out of scope

| Scope item | Rationale for exclusion |
|---|---|
| ADR-015 Component 4 — Cross-examination mode | Deferred to M15 by EL Decision 5 (2026-06-16). Component 4 sprint entry at M15 kickoff. |
| PMM interpretation anchor text (full policy language document) | Chief Methodologist G6 parallel deliverable. PMM annotation carries `[T3 composite · pre-cal]` placeholder until filed. G5 implements the placeholder; G6 delivers the anchor content. |
| Ecological directionality schema fix (Option B) | M15 scope by EL Decision 2 (2026-06-16). G5 implements Option A: directional annotation in L0 that specifies breach type (ceiling vs. floor) in human-readable text — e.g., `[↑ = approaching planetary ceiling — climate]`. Schema-level distinction is M15. |
| Cross-examination mode suppression in Mode 3 | Component 4 scope — M15. No Mode 3 interaction changes in G5. |
| L2 evidence chain (Zone 3 → calibration docs) | ADR-015 L2 references Zone 3 documentation (entity drawer → framework panels → methodology notes). G5 delivers L0 and the assumption surface (L0/Component 2). L1 basis statement surface is part of the L1 hover/interaction layer in Component 1 — the intent document must scope which L1 elements are in G5 vs. deferred. |
| Zone 1A layout changes | Separate concern — G6c (#845 Zone 1A Phase 1 design thinking). Not in G5 scope. |
| Backend endpoint additions beyond G5 intent document scope | The implementing agent must determine at intent authorship whether new fields on existing endpoints are required. Any backend additions must be scoped in the intent document before implementation begins. Backend additions not identified in the intent document are out of G5 scope. |

**L1 scope note:** ADR-015 specifies L0 (always-visible annotation) and L1 (one interaction →
basis statement). For M14 scope with Component 4 deferred, the intent document must clarify
which L1 elements ship in G5 (e.g., a popover on Zone 1D annotation text) and which are
deferred to M15 with Component 4. The ADR §Component 1 states L1 is "one interaction from
Zone 1" — this is implementable without Component 4. The implementing agent must make this
scope decision explicit in the intent document.

---

## Section 4 — ADR Prerequisite Summary

| Group | ADR required | ADR status | Decision 1 gate | Implementation may begin? |
|---|---|---|---|---|
| G5 | ADR-015 — Evidence Thread Architecture | **Accepted 2026-06-16 (PR #998)** | **SATISFIED 2026-06-17 (PR #1006)** | **After EL approval of this entry document** |

**Implementation sequencing for G5:**

1. EL approves this entry document (this step)
2. Frontend Architect Agent authors intent document `docs/process/intents/M14-G5-2026-06-17-adr015-frontend.md`:
   - Derives observable application states from ADR-015 §UX-3 criteria, §Silent Failure Mode,
     §Component 3 visibility rule, and §UX Concerns 1–4
   - Assigns `data-testid` values for all new/modified elements
   - **Maps API fields for each Component** (names exact endpoint + field path consumed)
   - Flags any field not currently in the endpoint response — requires Chief Engineer confirmation
   - Scopes L1 element delivery: which L1 interactions are in G5 vs. deferred to M15
   - Confirms fixture scenarios for Components 1–3 (Hormuz for C1/C2; PE-enabled scenario for C3)
   - **Must complete before Step 3 (any implementation code)**
3. QA Lead Agent authors `frontend/tests/e2e/m14-g5-adr015-frontend.spec.ts` from intent
   document acceptance criteria — **must complete before Step 4 (implementation)**
4. If backend API fields are required: Data Architect Agent updates `api_contracts.yml` and
   coordinates with Chief Engineer Agent on backend implementation. The contract update gates
   the frontend Step 3 if any Component 1/2 acceptance criterion depends on the new fields.
5. Frontend Architect Agent implements:
   - Zone 1D L0 annotations on all four framework rows + pre-calibration flag
   - Zone 1B compact row full indicator name display
   - Zone 1C PMM pre-calibration placeholder annotation
   - HCL strip unit + tier meaning expansion
   - Assumption surface strip (between Zone 0 and Zone 1)
   - `programme_survival_probability` conditional fifth row in Zone 1D
6. Implementation PR opens targeting `release/m14` with branch name `feat/m14-g5-adr015-frontend`
7. Frontend Architect Agent Step 4 Verify: dev server at 1280×900 and 1440×900; confirms
   all §UX-3 criteria pass, all silent failure states render correctly, PE row behaves
   correctly with and without PE module enabled, Zone 1D rows fit at 1280×800 without scroll
8. Business PO Step 5 Validate: confirms north star scenario — Zambian analyst can see
   Political Feasibility, Conditionality assumption, and T2 basis annotation without any
   interaction; Customer Agent Layer 3 assessment on record before verdict

---

## Section 5 — Near-Miss Sweep

**Near-miss sweep date:** 2026-06-17
**Sweep period:** G4 sprint entry approval (2026-06-17) through G5 sprint entry filing (2026-06-17)

| Finding | Category | PI Agent register call issued? | NM entry number |
|---|---|---|---|
| G4 REJECT-001: AC-3 E2E test used generic regex fallback `/[·•]\s*\S/` that matched tier separator `· T2` rather than institution name, masking GroundingStrip field name mismatch through Step 4. Fixed by AC-3 route mock with string-presence assertion. | Near-miss — Step 4 test assertion design | Yes | NM-045 |
| Stale Vite module cache in Docker container masked G4 REJECT-001 fix during post-sprint EL observation. EL Ctrl+F for "CBJ" returned 0 despite API returning correct data. Fixed by `usePolling: true` in vite.config.ts (PR #1021). | Near-miss — dev environment reliability | Yes | NM-046 |

**Structural improvement from NM-045 applied to G5:** Any G5 acceptance criterion that names
an expected string value (a tier label `T2`, a source name `IMF WEO`, the text `Political
Feasibility`, the annotation `[T3 composite · pre-cal]`) must be asserted by string-presence
match in the E2E test — not by a structural regex that could match an adjacent element. This
applies to every Component in G5.

---

## EL Approval Record

**EL approval:** 2026-06-17

> G5 sprint entry approved. All entry invariants satisfied: release branch exists, CI trigger
> verified, sprint plan EL-approved, ADR-015 Accepted (G2), Decision 1 step counter gate
> satisfied (G1). Correction recorded: API field assessment consultation is Data Architect
> (R on api_contracts.yml), not Chief Engineer. Intent document and QA tests required before
> any implementation PR opens.
> — @PublicEnemage (2026-06-17)
