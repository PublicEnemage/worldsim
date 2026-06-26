---
name: m18-g3-sprint-entry
type: sprint-entry
milestone: M18 — Full Argument and Demo 7
sprint-group: G3
status: EL-approved 2026-06-26
authored-by: PM Agent
authored-date: 2026-06-26
el-approved: 2026-06-26
release-branch: release/m18
sop-reference: docs/process/sprint-planning-sop.md
---

# Sprint Entry — M18, G3: Counter-Scenario Comparison

**Status:** EL-approved 2026-06-26
**Date authored:** 2026-06-26
**Release branch:** `release/m18`
**Sprint plan:** `docs/process/sprint-plans/m18-sprint-plan.md` (EL-approved 2026-06-26, PR #1364)
**Sprint journal issue:** #1377

*EL-approved 2026-06-26. `sprint/m18-g3` sub-branch cut from `release/m18` same session.*

---

## GR Close Citation (Required at G3 Entry)

GR (#1352) confirmed closed: PM Agent comment on #1352 (2026-06-26), citing PR #1375 merged to
`release/m18`. All three GR artifacts on record:

| Artifact | Location | Status |
|---|---|---|
| UX journey — who, mode, element design, interaction model | `docs/process/intents/M18-GR-2026-06-26-counter-scenario-comparison.md §2` | ✅ Filed 2026-06-26 |
| Customer Agent Layer 3 — Personas 1, 2, 5 kryptonite, false precision, 90s ceiling | `docs/process/intents/M18-GR-2026-06-26-counter-scenario-comparison.md §3` | ✅ Filed 2026-06-26 |
| BPO business requirements — minimum viable form, acceptance threshold, user stories, north star test | `docs/process/intents/M18-GR-2026-06-26-counter-scenario-comparison.md §4` | ✅ Filed 2026-06-26 |

## Architect ADR Determination Citation (Required at G3 Entry)

**Determination:** Option A — CLEAR. No new ADR required.
**Recorded:** Comment on #1349 (2026-06-26), Architect Agent.
**Authority:** `docs/process/sprint-plans/m18-sprint-plan.md §Architect consultation §G3`;
GR intent document `docs/process/intents/M18-GR-2026-06-26-counter-scenario-comparison.md §6.1`

**ADRs surveyed:** ADR-017 (not affected — governs Zone 1A, not Zone 1B), ADR-018 (comparison
summary follows Sub-zone B pattern established by M17 G2 Phase 3 — not a third occupant),
ADR-015 (not affected — basis threads, not comparison summary), ADR-007 (no new ADR — CI band
methodology applied to new computation within existing scope).

**Implementation constraints recorded in Architect determination (must flow into intent document):**
1. Comparison summary rendered inside `zone1bCohortSection` (Sub-zone B / CohortImpactSection)
   as a sticky-bottom element — NOT as a third occupant in `InstrumentCluster.tsx`
2. G3 intent document must note the 1280×800 Sub-zone B constraint: at 1280×800, the comparison
   summary is visible via sticky-bottom positioning while per-scenario rows scroll above it;
   at 1440×900 (expected Demo 7 viewport), Sub-zone B provides ~100px — sufficient for both
3. `docs/schema/api_contracts.yml` must be updated with the distributional differential endpoint
   before the G3 implementation PR opens
4. Implementing agent must confirm CI band tier inheritance at implementation time — if headcount
   conversion uses a Tier 3 regional average income distribution, the differential inherits Tier 3
   (not Tier 2); document in PR description

## Wave 2 Entry Gate — ScenarioInstrumentCluster.tsx Determination

Per `docs/process/sprint-plans/m18-sprint-plan.md §Wave 2 Entry Gates` condition 5:
> "G4 has exited OR PM Agent confirms G3 scope does not touch ScenarioInstrumentCluster.tsx"

**PM Agent determination (2026-06-26): G3 scope does NOT touch `ScenarioInstrumentCluster.tsx`.**

Evidence from Architect determination and code inspection:
- `InstrumentCluster.tsx` receives `zone1bCohortSection?: React.ReactNode` as a prop (line 54)
  and renders it at line 154 — it does not own Zone 1B content
- `ScenarioInstrumentCluster.tsx` passes `zone1bCohortSection={<CohortImpactSection .../>}`
  to the MDA alert panel — it does not need modification for a new Zone 1B content type
- G3's comparison summary is a new content element inside `CohortImpactSection`
  (in `MDAAlertPanelZone1B.tsx`) — following the same Sub-zone B pattern as M17 G2 Phase 3
  per-scenario rows, which were also added without touching `ScenarioInstrumentCluster.tsx`

**Condition 5 status: SATISFIED — G3 may open without waiting for G4.**

The Frontend Architect's original assessment (sprint plan §Frontend Architect) identified
`ScenarioInstrumentCluster.tsx` as a potential G3 file based on a broader scope ("new rendering
path for comparison mode"). The GR requirements phase narrowed G3 scope to a Zone 1B sticky-bottom
element, resolving this concern. The code inspection confirms CohortImpactSection is the correct
implementation surface.

---

## Section 1 — Sprint Identification

| Field | Value |
|---|---|
| Milestone | M18 — Full Argument and Demo 7 |
| GitHub Milestone | #19 (API: milestone 19) |
| Sprint group | G3 — Counter-Scenario Comparison (Wave 2) |
| Release branch | `release/m18` |
| Sprint sub-branch | `sprint/m18-g3` |
| Sprint plan document | `docs/process/sprint-plans/m18-sprint-plan.md` |
| Exit checklist issue | #1340 |
| Sprint journal issue | #1377 |
| Sprint groups in scope | G3 only |
| Wave coordination tier | **Standard** — G3 alone in Wave 2 at entry; if G1/G2 still active at entry time, max concurrent = 3 of 5 ceiling (Standard). G4 not yet open (blocked by ADR-019). |
| Concurrent groups at entry | ≤ 3 of 5 max (G3 + G1 + G2 if Wave 1 still in progress; G3 alone if Wave 1 has exited) |
| Cross-group dependencies | G3 requires G1 (`sprint/m18-g1`) to be merged to `release/m18` before the G3 backend integration test can validate CI band propagation through the distributional differential computation. This is a **soft dependency on G3 exit, not G3 entry** — G3 implementation can begin while G1 is still in progress. See §6.4. |

---

## Section 2 — Entry Invariants Checklist

*All items must be confirmed before any G3 implementation PR opens.*

### 2.1 — Structural gates

- [x] **Release branch exists:** `release/m18` cut from `main` 2026-06-26 (commit 8cffc86 after sync PR #1366 merged)
- [x] **CI trigger verified:** `.github/workflows/ci.yml` `pull_request: branches` includes `release/m*` and `sprint/m*` — confirmed 2026-06-26. 6 required checks: `changes`, `lint`, `test-backend`, `playwright-e2e`, `compliance-scan`, `branch-naming`.
- [x] **Sprint plan EL-approved:** `docs/process/sprint-plans/m18-sprint-plan.md` EL-approved 2026-06-26 (PR #1364 merged)

### 2.2 — ADR prerequisite gate

| Group | Required ADR | ADR status | Gate |
|---|---|---|---|
| G3 — #1349 (counter-scenario comparison) | None — Architect: Option A CLEAR | N/A — no new ADR required | **CLEAR** |

- [x] Architect determination on record. Gate: **CLEAR**.

The comparison summary element is a Zone 1B Sub-zone B content extension within existing ADR
authority (ADR-018 Sub-zone B pattern; ADR-007 CI band methodology). No ADR-017 amendment
required. Architect determination recorded on #1349, 2026-06-26.

### 2.3 — Intent document gate

G3 is user-facing (new Zone 1B comparison summary visible in N=3 COMPARE_VIEW). An intent
document is required before the implementation PR opens.

- [ ] Intent document filed: `docs/process/intents/M18-G3-2026-06-26-counter-scenario-comparison.md` — **required before implementation PR opens**

The intent document must be derived from GR artifacts (user stories US-1349-A through US-1349-D,
Persona Layer 3 constraints as design guardrails, §2.3 element design specification) and must
include all four Architect implementation constraints (§0 above). Specific requirements:

- Observable application state: "In N=3 COMPARE_VIEW, the Zone 1B comparison summary element
  is visible at the bottom of the Zone 1B area at 1280×800 without interaction, showing the
  poverty headcount differential between the reference scenario and each other scenario at the
  terminal step, with CI band and direction stability statement (when applicable)."
- Acceptance criteria assertable without reading implementation code (per US-1349-A through D)
- Kryptonite constraint check per Persona (from GR §3): no composite-score notation in
  the comparison summary; direction stability statement fires only when CI interval does not
  span zero; element visible in Zone 1 without scrolling or interaction
- Backend computation specification: engine-derived headcount differential (not client-side
  from chart values); CI band propagation methodology and tier inheritance determination
- 1280×800 viewport constraint noted explicitly (sticky-bottom ensures summary visible;
  per-scenario rows scroll above)
- Schema prerequisite confirmation: `docs/schema/api_contracts.yml` updated in same PR

**UX/UI design artifact gate (SOP §Sprint Entry Gate — UX/UI):**

The comparison summary element is a new Zone 1B content type with a new text pattern
("Direction stable across uncertainty range") and new numerical display format (CI band
on distributional headcount). This warrants design review before implementation.

- [ ] UX mockup filed and referenced from intent document — **required before implementation PR opens**
- [ ] UI mockup filed (element layout: differential value, CI band, direction statement, step label,
  T-tier badge; plain-language label vs. composite-score notation; sticky-bottom positioning) — **required before implementation PR opens**
- [ ] UX/UI panel review complete (minimum: UX Designer, Customer Agent confirming plain-language
  legibility for Persona 5, BPO confirming acceptance threshold match) — **required before implementation PR opens**

| Deliverable | ADR reference | Intent document path | Filed? |
|---|---|---|---|
| #1349 — comparison summary element (frontend) | ADR-018 Sub-zone B + ADR-007 CI bands | `docs/process/intents/M18-G3-2026-06-26-counter-scenario-comparison.md` | No — required before implementation PR opens |
| #1349 — distributional differential endpoint (backend) | ADR-007 CI band methodology | `docs/process/intents/M18-G3-2026-06-26-counter-scenario-comparison.md` | No — required before implementation PR opens |

### 2.4 — QA test authorship gate

- [ ] QA test files authored from intent document acceptance criteria before implementation code is written — **required before implementation PR opens**

Expected test files:

`frontend/tests/e2e/m18-g3-counter-scenario-comparison.spec.ts`
The E2E test must assert:
- Comparison summary element is present in Zone 1B when N=3 COMPARE_VIEW is active
- Element is visible without scrolling at 1280×800 viewport
- Element text contains poverty headcount differential in plain language (number + "persons") — no composite-score notation (assert text does not match composite score pattern e.g. "0.XX")
- CI band text present alongside differential ("95% CI" or equivalent)
- Direction stability statement present when applicable (or direction-uncertain disclosure when CI spans zero)
- No economist mediation required: element visible and readable with zero clicks or hovers (Persona 5 legibility gate)

`backend/tests/test_m18_g3_counter_scenario_comparison.py`
The backend test must assert:
- Distributional differential endpoint returns headcount differential per step for the Zambia three-scenario fixture
- CI band bounds are returned per step alongside differential
- Terminal step differential matches expected value within tolerance (fixture-anchored)
- Tier inheritance is explicit in the response (T2 or T3 depending on conversion methodology)

| Deliverable | Test file path | Authored before implementation? |
|---|---|---|
| #1349 — comparison summary (frontend) | `frontend/tests/e2e/m18-g3-counter-scenario-comparison.spec.ts` | No — required before implementation PR opens |
| #1349 — distributional differential (backend) | `backend/tests/test_m18_g3_counter_scenario_comparison.py` | No — required before implementation PR opens |

---

## Section 3 — Scope Declaration

### 3.1 — Issues in scope

| Issue | Title | Priority | Observable application state |
|---|---|---|---|
| #1349 | feat(demo7): counter-scenario comparison — distributional number differential with CI bands for Demo 7 Act 2 | High — Demo 7 Act 2 primary deliverable | In N=3 COMPARE_VIEW (Zambia three-scenario), Zone 1B shows a comparison summary element below per-scenario threshold rows. Element shows poverty headcount differential between reference scenario and each alternative at the terminal step, with CI band and direction stability statement. The Demo 7 Act 2 claim "340,000 more Zambians below the poverty threshold under proposed terms" is readable from Zone 1B without calculation or interaction. |

**M17 multi-scenario endpoint prerequisite verification:**
Per sprint plan §Computation Engine Agent: "#394 (M17 N=3 multi-scenario comparison API) must
be verified as on `main` and working before G3 sprint entry is filed."

- [x] **#394 verified CLOSED:** M17 N=3 multi-scenario comparison infrastructure confirmed on `main`
  (#394 state: CLOSED). G3 backend computation extends this API — the new distributional
  differential endpoint is a new computation layer on top of the M17 multi-scenario response.

### 3.2 — Issues explicitly out of scope

| Issue | Rationale for exclusion |
|---|---|
| #1254 — CI bands on Zone 1A | G1 (Wave 1). G3 consumes G1's uncertainty data for CI propagation on the differential — G1 is a soft exit dependency for G3's integration test, not a G3 scope item. |
| #1255 — PSP decomposition | G2 (Wave 1). No G3 interaction. |
| #1217 / control plane column | G4 (Wave 2). ScenarioInstrumentCluster.tsx confirmed not in G3 scope — G3 does not block or depend on G4. |
| Multi-indicator comparison (health, governance) | Capacity-allowing. G3 scope is poverty headcount differential only — sufficient for Demo 7 Act 2. Extension to additional indicators is not in scope for G3. |
| Step-selector interaction (step ≠ terminal) | Nice-to-have. Terminal step default is the minimum viable form (GR §4.1). Interactive step selection deferred — not required for Demo 7. |
| Export / download of comparison summary | Not required for Demo 7. |
| Historical precedent display | Not in #1349 scope. BPO confirmed poverty headcount differential is the Demo 7 Act 2 deliverable. |

---

## Section 4 — ADR Prerequisite Summary

| Group | ADR required | ADR status | Implementation may begin? |
|---|---|---|---|
| G3 — #1349 | None (Architect: Option A CLEAR) | N/A | Yes — after EL approves this entry; intent document, UX/UI mockups, panel review, QA tests, and schema prerequisite must exist before implementation PR opens |

**Implementation sequencing for G3:**

1. EL approves this entry document
2. PM Agent cuts `sprint/m18-g3` from `release/m18`
3. UX Designer produces UX mockup + UI mockup for the Zone 1B comparison summary element
   (sticky-bottom positioning, CI band format, direction stability statement, T-tier badge,
   plain-language labels per Persona 5 legibility requirement)
4. UX/UI panel review (minimum: UX Designer, Customer Agent, BPO) — ACCEPT required
5. Frontend Architect / implementing agent files intent document
   `docs/process/intents/M18-G3-2026-06-26-counter-scenario-comparison.md` incorporating:
   - All four Architect implementation constraints (§0 above)
   - User stories US-1349-A through D (from GR §4.3)
   - Persona Layer 3 constraints as design guardrails (from GR §3)
   - Observable application state and acceptance criteria
   - Backend computation specification and tier inheritance determination
   - Schema prerequisite confirmation
6. `docs/schema/api_contracts.yml` updated with distributional differential endpoint shape
   (this may be a pre-implementation PR or included in step 7; must be on `sprint/m18-g3`
   before the implementation PR opens)
7. QA Lead authors `frontend/tests/e2e/m18-g3-counter-scenario-comparison.spec.ts` and
   `backend/tests/test_m18_g3_counter_scenario_comparison.py` from intent document
   acceptance criteria (red before implementation)
8. Implementing agent opens feature branch `feat/m18-g3-counter-scenario-comparison`
   from `sprint/m18-g3`
9. Implementation:
   - Backend: distributional differential computation in simulation engine + new endpoint
   - Frontend: `CohortImpactSection` extension in `MDAAlertPanelZone1B.tsx` (or new
     `DistributionalComparisonSummary` component imported by CohortImpactSection);
     sticky-bottom positioning within Sub-zone B
   - Tier inheritance determination documented in PR description
10. Schema file updated in same PR: `docs/schema/api_contracts.yml` (if not done in step 6)
11. Pre-push gate: `cd backend && ruff check . && mypy app/`; `cd frontend && npm run build` — both exit 0
12. PR targeting `sprint/m18-g3`; set auto-merge
13. Before G3 integration exit: confirm G1 (`sprint/m18-g1` → `release/m18`) is merged so
    the CI band propagation integration test can pass with real uncertainty data
14. Integration PR `sprint/m18-g3` → `release/m18` after feature PR(s) merge; PI Agent
    gate comment required
15. BPO acceptance (screen recording of Demo 7 Act 2 flow; Persona 5 legibility test);
    Customer Agent Layer 3 at sprint exit (Personas 1 and 5)
16. North star test artifact on record at exit (from GR §4.4 — PASS verdict already
    recorded; implementing agent confirms the delivered capability matches the assessed scope)

---

## Section 5 — Near-Miss Sweep

**Near-miss sweep date:** 2026-06-26
**Sweep period:** M17 exit ceremony (2026-06-26) through M18 G3 sprint entry filing (2026-06-26)

| Finding | Category | PI Agent register call issued? | NM entry number |
|---|---|---|---|
| No new process gaps identified. All M17 NM entries (NM-066 through NM-071) resolved before M18 kickoff and confirmed resolved in G1, G2, GR sprint entries filed same session. G3 entry filed same session — no additional gaps identified. | N/A | N/A | N/A |

---

## Section 6 — Sprint Group Isolation

### 6.1 — Sprint sub-branch

| Field | Value |
|---|---|
| Sprint sub-branch | `sprint/m18-g3` |
| Cut from | `release/m18` — after EL approves this entry; after intent document, UX/UI review, and QA tests are complete |
| Sprint journal issue | #1377 |

**PM Agent sprint sub-branch cut command:**
```bash
git checkout -b sprint/m18-g3 release/m18 && git push -u origin sprint/m18-g3
```

*Cut timing: After EL approves this entry and all pre-implementation prerequisites (§2.3 and §2.4) are satisfied. The sub-branch is cut once — not at entry filing time but immediately before the first feature branch opens.*

### 6.2 — File-conflict risk assessment

| File | Lane required | Trigger |
|---|---|---|
| `frontend/src/components/MDAAlertPanelZone1B.tsx` | Sprint sub-branch | CohortImpactSection extension — comparison summary rendered here as sticky-bottom element |
| `frontend/src/components/DistributionalComparisonSummary.tsx` (new) | Sprint sub-branch | New component for comparison summary element (if extracted from CohortImpactSection) |
| `frontend/src/stores/` | Sprint sub-branch | New data type for distributional comparison response |
| `backend/app/simulation/` (comparison differential module) | Sprint sub-branch | New distributional differential computation; extends M17 N=3 comparison API |
| `docs/schema/api_contracts.yml` | Sprint sub-branch (same PR as implementation or pre-implementation) | New distributional differential endpoint — mandatory schema-first per CLAUDE.md §Schema registry |
| `SESSION_STATE.md` | PM Agent coordination lane | Sprint exit cockpit update |
| `docs/process/near-miss-registry.md` | PM Agent coordination lane (PI Agent authors) | If NM identified |
| `docs/compliance/scan-registry.md` | PM Agent coordination lane | If compliance scan produced |

**File area analysis (confirmed no conflict with G4):**

G3 primary files: `MDAAlertPanelZone1B.tsx` (CohortImpactSection), new comparison summary
component, backend comparison module.
G4 primary files: `InstrumentCluster.tsx` (column 3 restructuring), `ControlPlane.tsx`,
new `ControlPlaneForm*.tsx` components, `ScenarioInstrumentCluster.tsx`.

These file sets do not overlap. G3 and G4 can proceed in parallel if scheduling permits,
notwithstanding the sprint plan's original wave sequencing concern (resolved above by
ScenarioInstrumentCluster.tsx determination). PM Agent must confirm no G4 incidental
writes to `MDAAlertPanelZone1B.tsx` before any concurrent opening.

G3 does NOT write to `InstrumentCluster.tsx` or `ScenarioInstrumentCluster.tsx` — the
comparison summary is passed via the existing `zone1bCohortSection` prop mechanism.

### 6.3 — Infrastructure dependency declaration

- [x] No DS-owned file changes required. All G3 writes are to implementation code, test files,
  documentation, and schema files.

#### 6.3a — New output paths declaration (NM-069 process improvement)

- [x] No new output directories introduced by G3. `backend/test-results/` and
  `frontend/test-results/` are already covered by `.gitignore` (PR #1346 from M18 kickoff prep).

No new output paths introduced by this sprint group.

### 6.4 — Cross-group dependency declaration

- [x] Yes — soft dependency on G1 for integration test (not a hard entry gate)

**Dependency:** G3's backend integration test (`test_m18_g3_counter_scenario_comparison.py`)
requires the CI band data format from G1 (`sprint/m18-g1` → `release/m18`) to validate
uncertainty propagation through the distributional differential computation.

**Nature of dependency:** Soft — G3 implementation can proceed using the uncertainty data
format specification from the G1 intent document (schema-first). The integration test can
run against a fixture with the expected uncertainty shape before G1 merges. Full end-to-end
validation (real G1 uncertainty data → G3 differential CI band) requires G1 to be on
`release/m18`. G3 must not exit before this validation is confirmed.

**Merge ordering constraint:** G1 (`sprint/m18-g1` integration PR) should merge to
`release/m18` before the G3 integration PR merges. PM Agent monitors this at G3 exit.

No upstream dependency on G2 (PSP decomposition is Zone 1D only — no G3 interaction).
No upstream dependency on G4 (ScenarioInstrumentCluster.tsx confirmed out of G3 scope).

### 6.5 — Prior NM verification (NM-068 process improvement)

**NM verification sweep date:** 2026-06-26
**Sweep period:** M17 exit through M18 G3 sprint entry

| NM entry | Process improvement required | Applied in this sprint? |
|---|---|---|
| NM-068 | Prior NM verification field in sprint entry | Yes — this section (§6.5) |
| NM-069 | New output directories covered by `.gitignore` in same PR | Yes — no new output directories; §6.3a confirmed |
| NM-070 | Pre-push hook enforcing ruff + mypy + npm build | Yes — `.githooks/pre-push` active; step 11 of §4 implementation sequencing requires both gates exit 0 before any push |
| NM-071 | Wave concurrency ceiling check at wave kickoff | Yes — G3 alone in Wave 2 at entry; max 3 concurrent groups if G1/G2 still active → Standard tier; recorded in §1 |

---

## EL Approval Record

**EL approval:** 2026-06-26

> G3 sprint entry approved. GR close confirmed, Architect ADR determination (Option A CLEAR)
> on record, ScenarioInstrumentCluster.tsx determination confirmed by PM Agent. `sprint/m18-g3`
> sub-branch may be cut. Pre-implementation prerequisites (intent document, UX/UI mockups + panel
> review, QA tests, schema update) must be satisfied before any feature PR opens on this group.
> — @PublicEnemage (2026-06-26)
