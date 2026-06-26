---
name: m18-g2-sprint-entry
type: sprint-entry
milestone: M18 — Full Argument and Demo 7
sprint-group: G2
status: Filed — awaiting EL approval
authored-by: PM Agent
authored-date: 2026-06-26
el-approved: false
release-branch: release/m18
sop-reference: docs/process/sprint-planning-sop.md
---

# Sprint Entry — M18, G2: PSP Driver Decomposition

**Status:** Filed — awaiting EL approval before implementation PR opens
**Date authored:** 2026-06-26
**Release branch:** `release/m18`
**Sprint plan:** `docs/process/sprint-plans/m18-sprint-plan.md` (EL-approved 2026-06-26, PR #1364)
**Sprint journal issue:** #1368

*No implementation PR may open until this entry document is EL-approved.*

---

## Section 1 — Sprint Identification

| Field | Value |
|---|---|
| Milestone | M18 — Full Argument and Demo 7 |
| GitHub Milestone | #19 (API: milestone 19) |
| Sprint group | G2 — PSP Driver Decomposition (Wave 1) |
| Release branch | `release/m18` |
| Sprint sub-branch | `sprint/m18-g2` |
| Sprint plan document | `docs/process/sprint-plans/m18-sprint-plan.md` |
| Exit checklist issue | #1340 |
| Sprint journal issue | #1368 |
| Sprint groups in scope | G2 only |
| Wave coordination tier | **Standard** — 2 concurrent groups (G1 + G2); well within 5-group ceiling |
| Concurrent groups at entry | 2 of 5 max (G1 + G2 opening simultaneously) |
| Cross-group dependencies | None — G2 (Zone 1D / PSP module) and G1 (Zone 1A / banding engine) touch distinct file areas; no merge ordering constraint |

---

## Section 2 — Entry Invariants Checklist

*All items must be confirmed before any G2 implementation PR opens.*

### 2.1 — Structural gates

- [x] **Release branch exists:** `release/m18` cut from `main` 2026-06-26 (commit 8cffc86 after sync PR #1366 merged)
- [x] **CI trigger verified:** `.github/workflows/ci.yml` `pull_request: branches` includes `release/m*` and `sprint/m*` — confirmed 2026-06-26. 6 required checks: `changes`, `lint`, `test-backend`, `playwright-e2e`, `compliance-scan`, `branch-naming`.
- [x] **Sprint plan EL-approved:** `docs/process/sprint-plans/m18-sprint-plan.md` EL-approved 2026-06-26 (PR #1364 merged)

### 2.2 — ADR prerequisite gate

| Group | Required ADR | ADR status | Gate |
|---|---|---|---|
| G2 — #1255 (PSP decomposition, Zone 1D) | ADR-015 (Model Legibility / Evidence Thread Architecture) | **ACCEPTED** 2026-06-16 | **CLEAR** |

- [x] All ADR prerequisites accepted. Gate: **CLEAR**.

ADR-015 authorises Zone 1D basis annotation and evidence threading. PSP driver decomposition exposes which driver categories (governance, fiscal sustainability, external balance, social stability) produced the PSP change at each step — this is a Zone 1D content addition within the existing L0/L1 evidence thread model established by ADR-015 §Decision (Component 3: Zone 1D basis annotation). No new ADR is required.

### 2.3 — Intent document gate

G2 is UX/UI-impacting (new display content in Zone 1D). An intent document is required before the implementation PR opens.

- [ ] Intent document filed: `docs/process/intents/M18-G2-2026-06-26-psp-driver-decomposition.md` — **required before implementation PR opens**

The intent document must specify:
- Zone 1D visual treatment: how the dominant driver category is displayed alongside the PSP severity label (inline text? icon? chip? expandable row?)
- Which driver categories are surfaced and at what granularity (top-1 driver only, or top-3 with percentages?)
- Data contract: what fields the backend PSP module produces and which `docs/schema/` files are updated
- Observable application state: "The PSP severity label in Zone 1D is accompanied by a driver decomposition indicator. For the Senegal Article IV scenario at step 3, the dominant driver category is readable without interaction. Andreas (Persona 3) can cite the dominant driver in a verbal political brief without opening Zone 2."
- Acceptance criteria the QA Lead can assert without reading implementation code

**UX/UI design artifact gate (SOP §Sprint Entry Gate — UX/UI):**

PSP decomposition adds new display content to Zone 1D. Zone 1D is already dense at 1280×800 (four framework scores + PSP severity label + basis annotation). A UX mockup specifying how decomposition fits within the existing Zone 1D space without crowding is required before the implementation PR opens.

- [ ] UX mockup filed and referenced from intent document — **required before implementation PR opens**
- [ ] UX/UI panel review complete (5 agents: UX Designer, Design Thinking, Customer Agent, Frontend Architect, Business PO) — **required before implementation PR opens**

A full UI mockup (new component / new layout zone trigger) is **conditional**: if the decomposition is implemented as an inline text addition to the existing PSP row, a UX mockup suffices. If it requires a new sub-row or expandable zone in Zone 1D, a UI mockup is required. The UX Designer determines this at mockup authorship time.

| Deliverable | ADR reference | Intent document path | Filed? |
|---|---|---|---|
| #1255 — PSP driver decomposition | ADR-015 | `docs/process/intents/M18-G2-2026-06-26-psp-driver-decomposition.md` | No — required before implementation PR opens |

### 2.4 — QA test authorship gate

- [ ] QA test file authored from intent document acceptance criteria before implementation code is written — **required before implementation PR opens**

Expected test files:
- `frontend/tests/e2e/m18-g2-psp-decomposition.spec.ts` — asserts dominant driver category is visible in Zone 1D at the specified breakpoints; PSP severity label is not obscured; driver text is readable at 1280×800 and 1024×768; updates correctly when scenario step changes
- `backend/tests/test_m18_g2_psp_decomposition.py` — asserts PSP module returns driver decomposition fields per step for the Senegal Article IV scenario; dominant driver category matches the calibrated PoliticalEconomyModule weights

| Deliverable | Test file path | Authored before implementation? |
|---|---|---|
| #1255 — PSP decomposition (frontend) | `frontend/tests/e2e/m18-g2-psp-decomposition.spec.ts` | No — required before implementation PR opens |
| #1255 — PSP decomposition (backend) | `backend/tests/test_m18_g2_psp_decomposition.py` | No — required before implementation PR opens |

---

## Section 3 — Scope Declaration

### 3.1 — Issues in scope

| Issue | Title | Priority | Observable application state |
|---|---|---|---|
| #1255 | ux(zone-1d): PSP driver decomposition — dominant signal category visible alongside severity label | High — Demo 7 Act 1 (Senegal Mode 3) | The PSP severity label in Zone 1D shows the dominant driver category for the current step. For Senegal Article IV at step 3, the analyst can read "fiscal sustainability" (or equivalent) as the dominant driver without any interaction beyond reading Zone 1D. Andreas (Persona 3) can cite this driver in a political brief prepared during the Demo 7 Act 1 session. The PSP value, severity tier, and dominant driver are all readable in a single glance at Zone 1D. |

### 3.2 — Issues explicitly out of scope

| Issue | Rationale for exclusion |
|---|---|
| #1254 — CI bands | G1 — Wave 1 parallel group; separate file area |
| #1349 — Counter-scenario comparison | G3 — Wave 2; requires GR close |
| #1217 / control plane | G4 — Wave 2; requires ADR-019 |
| PSP decomposition for N>1 scenarios | G2 scope is single-scenario PSP decomposition; multi-scenario PSP delta is G3 scope (#1349) |
| Zone 1D structural changes (new rows, expanded layout) | UX Designer determination at mockup time; if structural, escalate to PM Agent before implementation PR opens |
| PMM or Zone 1B/1C changes | G2 scope is Zone 1D and the PSP backend module only |

---

## Section 4 — ADR Prerequisite Summary

| Group | ADR required | ADR status | Implementation may begin? |
|---|---|---|---|
| G2 — #1255 | ADR-015 | ACCEPTED 2026-06-16 | Yes — after EL approves this entry; intent document, UX mockup, panel review, and QA tests must exist before implementation PR opens |

**Implementation sequencing for G2:**

1. EL approves this entry document
2. UX Designer produces UX mockup for PSP decomposition Zone 1D treatment (inline text vs. new row — determines if UI mockup is also required)
3. UX/UI panel review (5 agents) — ACCEPT required; note if UI mockup conditional is triggered
4. Frontend Architect Agent (or UX Designer) files intent document `docs/process/intents/M18-G2-2026-06-26-psp-driver-decomposition.md` with panel-approved mockup referenced
5. QA Lead authors `frontend/tests/e2e/m18-g2-psp-decomposition.spec.ts` and `backend/tests/test_m18_g2_psp_decomposition.py` from intent document (red before implementation)
6. Implementing agent opens feature branch `feat/m18-g2-psp-decomposition` from `sprint/m18-g2`
7. Implementation: backend PoliticalEconomyModule driver decomposition extension + frontend Zone 1D display
8. Schema files updated in same PR (`docs/schema/api_contracts.yml`, `docs/schema/simulation_state.yml`)
9. Pre-push gate: `cd backend && ruff check . && mypy app/`; `cd frontend && npm run build` — both exit 0
10. PR targeting `sprint/m18-g2`; set auto-merge
11. Integration PR `sprint/m18-g2` → `release/m18` after feature PR merges; PI Agent gate comment required
12. BPO acceptance and Customer Agent Layer 3 at sprint exit

---

## Section 5 — Near-Miss Sweep

**Near-miss sweep date:** 2026-06-26
**Sweep period:** M17 exit ceremony (2026-06-26) through M18 G2 sprint entry filing (2026-06-26)

| Finding | Category | PI Agent register call issued? | NM entry number |
|---|---|---|---|
| No new process gaps identified. All M17 NM entries (NM-066 through NM-071) were resolved before M18 kickoff and are confirmed resolved. M18 entry blockers all cleared. | N/A | N/A | N/A |

---

## Section 6 — Sprint Group Isolation

### 6.1 — Sprint sub-branch

| Field | Value |
|---|---|
| Sprint sub-branch | `sprint/m18-g2` |
| Cut from | `release/m18` at commit 8cffc86 (2026-06-26) |
| Sprint journal issue | #1368 |

### 6.2 — File-conflict risk assessment

| File | Lane required | Trigger |
|---|---|---|
| `frontend/src/components/` (Zone 1D PSP component) | Sprint sub-branch | Driver decomposition display |
| `backend/app/simulation/political_economy_module.py` | Sprint sub-branch | PSP driver decomposition logic |
| `docs/schema/api_contracts.yml` | Sprint sub-branch (same PR as implementation) | New PSP decomposition response fields |
| `docs/schema/simulation_state.yml` | Sprint sub-branch (same PR as implementation) | New PSP decomposition quantity fields |
| `SESSION_STATE.md` | PM Agent coordination lane | Sprint exit cockpit update |
| `docs/process/near-miss-registry.md` | PM Agent coordination lane (PI Agent authors) | If NM identified |
| `docs/compliance/scan-registry.md` | PM Agent coordination lane | If compliance scan produced |

G2 does not touch `InstrumentCluster.tsx` if decomposition is inline within the existing Zone 1D PSP row. If a structural Zone 1D change is required (new sub-row), PM Agent must assess G1 conflict risk before opening that PR.

### 6.3 — Infrastructure dependency declaration

- [x] No DS-owned file changes required. All G2 writes are to implementation code, test files, and schema files.

#### 6.3a — New output paths declaration

- [x] No new output directories introduced by G2. `backend/test-results/` and `frontend/test-results/` are already covered by `.gitignore` (PR #1346).

### 6.4 — Cross-group dependency declaration

- [x] No cross-group dependencies. G2 (Zone 1D / PSP module) and G1 (Zone 1A / banding engine) touch distinct file areas. G2 need not wait for G1 and G1 need not wait for G2.

### 6.5 — Prior NM verification

**NM verification sweep date:** 2026-06-26
**Sweep period:** M17 exit through M18 G2 sprint entry

| NM entry | Process improvement required | Applied in this sprint? |
|---|---|---|
| NM-069 | New output directories covered by `.gitignore` in same PR | Yes — `backend/test-results/` and `frontend/test-results/` already in `.gitignore`; §6.3a confirmed |
| NM-070 | Pre-push hook enforcing ruff + mypy + npm build | Yes — `.githooks/pre-push` active; step 9 of §4 implementation sequencing requires both gates exit 0 |
| NM-071 | Wave concurrency ceiling check at wave kickoff | Yes — 2 concurrent groups (G1 + G2) = Standard tier; recorded in §1 |
| NM-068 | Prior NM verification field in sprint entry | Yes — this section (§6.5) |

---

## EL Approval Record

**EL approval:** Pending

> {EL approval statement — implementation PR may not open until this record is complete}
> — @PublicEnemage ({date})
