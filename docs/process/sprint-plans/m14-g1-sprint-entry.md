---
name: m14-g1-sprint-entry
type: sprint-entry
milestone: M14 — Methodology Publication and External Validation
sprint-group: G1
status: Filed — EL approval required before implementation PR opens
authored-by: PM Agent
authored-date: 2026-06-16
el-approved: false
release-branch: release/m14
sop-reference: docs/process/sprint-planning-sop.md
---

# Sprint Entry — M14, G1: Prerequisite Bug Fixes

**Status:** Filed — EL approval required before implementation PR opens
**Date authored:** 2026-06-16
**Release branch:** `release/m14`
**Sprint plan:** `docs/process/sprint-plans/m14-sprint-plan.md` (EL Approved 2026-06-16)

*Authority: `docs/process/sprint-planning-sop.md §Sprint Entry Gate` (Phase C output).
This entry gates G1 specifically. G1 is the first group to open in M14 and has no ADR
prerequisite — it proceeds after this entry document is EL-approved and intent + QA gates are
satisfied.*

---

## Section 1 — Sprint Identification

| Field | Value |
|---|---|
| Milestone | M14 — Methodology Publication and External Validation |
| GitHub Milestone | #15 |
| Sprint group | G1 — Prerequisite bug fixes |
| Release branch | `release/m14` |
| Sprint plan document | `docs/process/sprint-plans/m14-sprint-plan.md` |
| Exit checklist issue | #968 |
| Sprint groups in scope | G1 only |
| ADR gate | None — G1 bugs have no ADR prerequisite |
| Implementing agent | Frontend Architect Agent |

---

## Section 2 — Entry Invariants Checklist

*All items must be checked before any implementation PR is opened for G1.
An unchecked invariant blocks implementation from beginning.*

### 2.1 — Structural gates

- [x] **Release branch exists:** `release/m14` cut from `main` 2026-06-16 (PR #991 merged)
- [x] **CI trigger verified:** `.github/workflows/ci.yml` `pull_request: branches` includes
  `release/m*` — confirmed 2026-06-16 (PR #977 `branch-naming` workflow; Ruleset ID 17751852
  with 6 required checks: `changes`, `lint`, `test-backend`, `playwright-e2e`,
  `compliance-scan`, `branch-naming`)
- [x] **Sprint plan EL-approved:** `docs/process/sprint-plans/m14-sprint-plan.md`
  `el-approved: 2026-06-16` (PR #992)

### 2.2 — ADR prerequisite gate

G1 is composed entirely of pre-existing UI bug fixes. No ADR is required for any G1 issue.
ADR-016 (Scenario Grounding Architecture) is accepted and provides context for the entity
selector fix (#961), but G1's scope does not implement ADR-016 Component 1 or 2 — it only
unblocks the entity selection path that ADR-016 requires. G4 (ADR-016 frontend) is the ADR-016
implementation group.

| Group | Required ADR | ADR status | Gate |
|---|---|---|---|
| G1 | None | N/A | **CLEAR** |

- [x] G1 has no ADR prerequisite. Gate is clear.

### 2.3 — Intent document gate

*An intent document must be filed before any G1 implementation PR opens.
(Authority: CLAUDE.md §Agent Execution Lifecycle Step 1)*

- [ ] Intent document filed for G1 deliverables — **MUST FILE BEFORE G1 PR OPENS**

| Deliverable | ADR reference | Intent document path | Filed? |
|---|---|---|---|
| #961 — Entity selector (GRC hardcoded) | ADR-016 context | `docs/process/intents/G1-2026-06-16-prerequisite-bugs.md` | No — file before PR opens |
| #962 — Step counter display | None | (same intent document) | No — file before PR opens |
| #963 — Choropleth attribute labels | None | (same intent document) | No — file before PR opens |

All three bugs may be covered by a single intent document (`G1-2026-06-16-prerequisite-bugs.md`)
since they share a PR, a implementing agent, and a sprint group. The intent document must derive
acceptance criteria from the observable application states in Section 3 below — not from
implementation interface.

**Completeness gate for the intent document:** The QA Lead must be able to write a Playwright
test for each of the three bugs from the intent document without reading any implementation
code.

### 2.4 — QA test authorship gate

*QA tests must be authored from the intent document's acceptance criteria before implementation
code is written. (Authority: CLAUDE.md §Agent Execution Lifecycle Step 2)*

- [ ] QA test file authored for G1 before implementation begins — **MUST FILE BEFORE G1 PR OPENS**

| Deliverable | Intent document | Test file path | Authored before implementation? |
|---|---|---|---|
| #961 — Entity selector | `docs/process/intents/G1-2026-06-16-prerequisite-bugs.md` | `frontend/tests/g1-prerequisite-bugs.spec.ts` (Playwright) | No — author after intent document, before implementation PR |
| #962 — Step counter | (same) | (same spec file) | No — author after intent document, before implementation PR |
| #963 — Choropleth labels | (same) | (same spec file) | No — author after intent document, before implementation PR |

---

## Section 3 — Scope Declaration

### 3.1 — Issues in scope

| Issue | Title | Priority | Observable application state (pre-implementation specification) |
|---|---|---|---|
| #961 | bug(frontend): entity hardcoded to GRC in scenario creation form | immediate | `data-testid="entity-selector"` (or equivalent) is present in the scenario creation form with ≥4 options (GRC, JOR, EGY, ZMB); selecting ZMB and submitting creates a scenario with `entity_id = "ZMB"` in the API response |
| #962 | bug(frontend): step counter shows 'Step 0 / 8' on completed scenarios loaded via URL param | immediate | When a completed scenario is loaded via URL param, the step counter element shows "Step {N} / {max}" where N = the scenario's current step count (equal to max for a completed scenario) — not "Step 0 / {max}" — without any user interaction after load |
| #963 | bug(frontend): choropleth attribute selector displays raw DB field names as user-facing labels | immediate | The choropleth attribute selector shows human-readable labels (e.g., "Reserve Coverage (months)") with no underscores and no raw snake_case DB field names visible; `reserve_coverage_months`, `gdp_growth_rate`, `unemployment_rate` are not visible as selectable option text |

### 3.2 — Issues explicitly out of scope

G1's scope is bounded to fixing the three listed bugs without introducing new features or
touching ADR-016 Component 1–4 implementation. The following are explicitly excluded from G1:

| Issue / scope | Rationale for exclusion |
|---|---|
| ADR-016 Component 1 (data quality preview) | G4 scope — requires backend endpoints from G3 |
| ADR-016 Component 2 (Grounding strip) | G4 scope — new component; ADR-016 Accepted |
| ADR-016 Component 4 (parameter persistence) | G4 scope |
| Full entity data source wiring (source registry population for ZMB/JOR/EGY) | G3 backend scope |
| Any new UI surface beyond the three bug fixes | Out of scope — bugs only |

G1 is complete when the three bugs are fixed and the Business PO validates the observable
application states. G1 does not gate G3/G4 — G3 and G6 may proceed in parallel.

---

## Section 4 — ADR Prerequisite Summary

| Group | ADR required | ADR status | Implementation may begin? |
|---|---|---|---|
| G1 | None | N/A | **Yes — after EL approves this entry document, intent document is filed, and QA tests are authored** |

**Implementation sequencing for G1:**
1. EL approves this entry document (this step)
2. Frontend Architect Agent authors intent document at `docs/process/intents/G1-2026-06-16-prerequisite-bugs.md` — must derive acceptance criteria from Section 3.1 observable application states above
3. QA Lead Agent authors `frontend/tests/g1-prerequisite-bugs.spec.ts` from intent document before implementation begins
4. Implementation PR opens targeting `release/m14` with milestone-scoped branch name (`feat/m14-g1-{description}`)
5. Implementing agent Step 4 Verify: confirms observable application states present in running application before marking PR ready for review
6. Business PO Step 5 Validate: opens live application and confirms observable states within the reactive mode time ceiling (90 seconds for Persona 2)
7. Customer Agent Layer 3 assessment required before Business PO verdict is final (Personas 2, 3, 5 — entity selector directly affects Persona 2's scenario access path)

---

## Section 5 — Near-Miss Sweep

**Near-miss sweep date:** 2026-06-16
**Sweep period:** M13 exit (2026-06-15) through M14 G1 sprint entry filing (2026-06-16)

| Finding | Category | PI Agent register call issued? | NM entry number |
|---|---|---|---|
| `docs/ux/user-journeys.md` written in PR #974 (Journey A GA-01/GA-02 gap markers) without activating UX Designer Agent; `user-journeys.md` owner is UX Designer per `docs/process/agent-raci.md §File Ownership`. Finding surfaced at HORIZON Step 5 (file authority audit, 2026-06-16). Caught as an anticipatory finding before any downstream consequence materialized. | Near-miss (file authority violation — anticipatory) | Yes — register call issued to PI Agent | NM number assigned by PI Agent at registry filing time |

**Register call note:** PM Agent issues this call to PI Agent at sprint entry filing (2026-06-16). PI Agent holds R for writing the registry entry and assigning the NM number. Recommended countermeasure for PI Agent consideration: HORIZON Step 5 (file authority audit) should include an explicit check that any file with non-PM-Agent ownership was reviewed and approved by the owning agent before the PR merged. The GA-01/GA-02 content is sound — this is a process gap in file authority compliance, not a content defect.

---

## EL Approval Record

**EL approval:** Pending

> {EL approval statement}
> — @PublicEnemage ({date})
