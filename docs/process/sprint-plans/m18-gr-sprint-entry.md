---
name: m18-gr-sprint-entry
type: sprint-entry
milestone: M18 — Full Argument and Demo 7
sprint-group: GR — Requirements Phase for Counter-Scenario Comparison
status: Filed — awaiting EL approval
authored-by: PM Agent
authored-date: 2026-06-26
el-approved: false
release-branch: release/m18
sop-reference: docs/process/sprint-planning-sop.md
---

# Sprint Entry — M18, GR: Requirements Phase for Counter-Scenario Comparison

**Status:** Filed — awaiting EL approval before GR phase output is treated as entry-gate-complete for G3
**Date authored:** 2026-06-26
**Release branch:** `release/m18`
**Sprint plan:** `docs/process/sprint-plans/m18-sprint-plan.md` (EL-approved 2026-06-26, PR #1364)

*SOP exception note: `docs/process/sprint-plans/m18-sprint-plan.md §Sprint Entry Gate Requirements` declares "GR exception — no sprint entry required for #1352 requirements phase." This entry is filed voluntarily for process visibility and tracking, and to ensure GR close conditions are explicit before G3 sprint entry opens. The standard implementation gates (intent document, QA tests, sub-branch) do not apply to a requirements-only phase — see adapted sections below.*

---

## Section 1 — Sprint Identification

| Field | Value |
|---|---|
| Milestone | M18 — Full Argument and Demo 7 |
| GitHub Milestone | #19 (API: milestone 19) |
| Sprint group | GR — Requirements Phase for Counter-Scenario Comparison (Pre-wave) |
| Phase type | Requirements and design capture — no implementation code |
| Release branch | `release/m18` |
| Sprint sub-branch | N/A — requirements artifacts filed via PRs directly to `release/m18` |
| Sprint plan document | `docs/process/sprint-plans/m18-sprint-plan.md` |
| Exit checklist issue | #1340 |
| Sprint journal issue | #1352 (GR work tracked here) |
| Sprint groups in scope | GR only |
| Wave coordination tier | Pre-wave — not counted toward Wave 1/2 concurrency ceiling (NM-071 compliance) |
| Concurrent groups at entry | GR (pre-wave) runs alongside GD (pre-wave), G1 (Wave 1), G2 (Wave 1) — no concurrency conflict; GR produces docs only |
| Cross-group dependencies | G3 sprint entry is blocked until GR close is confirmed. No GR dependency on G1 or G2 output. |

---

## Section 2 — Entry Invariants Checklist

*Structural gates apply to all sprint groups including pre-wave requirements phases.
Implementation-specific gates (intent document, QA tests) are N/A for a requirements phase — GR produces the prerequisites for those gates in G3.*

### 2.1 — Structural gates

- [x] **Release branch exists:** `release/m18` cut from `main` 2026-06-26 (commit 8cffc86 after sync PR #1366 merged)
- [x] **CI trigger verified:** `.github/workflows/ci.yml` `pull_request: branches` includes `release/m*` — confirmed 2026-06-26. GR artifact PRs target `release/m18` directly and will trigger CI.
- [x] **Sprint plan EL-approved:** `docs/process/sprint-plans/m18-sprint-plan.md` EL-approved 2026-06-26 (PR #1364 merged). EL approval explicitly states: "pre-wave phases (GD #1354 and GR #1352) may begin immediately."

### 2.2 — ADR prerequisite gate

N/A — requirements phase. GR produces no implementation code. The question of whether #1349 requires a new ADR (ADR-017 amendment vs. within-scope determination) is an output of GR, not an input. The Architect resolves this at G3 sprint entry based on GR artifacts.

| Group | Required ADR | ADR status | Gate |
|---|---|---|---|
| GR — #1352 (requirements) | None | N/A — requirements phase | CLEAR |

### 2.3 — Intent document gate

N/A — GR IS the requirements phase that produces the prerequisites for the #1349 intent document. No intent document is filed during GR. The intent document for #1349 is filed as the first step of G3, after GR closes.

### 2.4 — QA test authorship gate

N/A — requirements phase. GR produces no implementation code and no testable application behavior. QA tests for #1349 are authored at G3 sprint entry from the intent document's acceptance criteria.

---

## Section 3 — Scope Declaration

### 3.1 — Issues in scope

| Issue | Title | Priority | Output |
|---|---|---|---|
| #1352 | Requirements phase for #1349 — UX journeys, BPO business requirements, Customer Agent Layer 3 | **Immediate** — blocks G3 sprint entry | Three artifacts: UX journey, Customer Agent Layer 3 (Personas 1, 2, 5), BPO business requirements and user stories |

### 3.2 — Issues explicitly out of scope

| Issue | Rationale for exclusion |
|---|---|
| #1349 — Counter-scenario comparison (implementation) | Wave 2 implementation — blocked until GR closes and G3 sprint entry is filed and EL-approved |
| #1254, #1255 — Wave 1 groups | G1 and G2 — separate sprint groups; no GR interaction |
| #1354 / GD design package | Separate pre-wave group; no GR interaction |

---

## Section 4 — Requirements Artifact Delivery Summary

*In place of the standard ADR Prerequisite Summary, GR tracks three mandatory artifacts. All three must be on record before G3 sprint entry is filed.*

| Artifact | Owner agent | Dependent issue | Filed? |
|---|---|---|---|
| **1. UX journey** — how Eleni (Persona 2) or Lucas (Persona 3) initiates counter-scenario comparison; zone layout; reading order; UI surface for the number differential; interaction model (step-configurable vs. canonical point) | UX Designer | #1349 intent document | No — required before GR closes |
| **2. Customer Agent Layer 3 assessment** — Persona 2 (Eleni, Finance Ministry Negotiator) and Persona 5 (Aicha, Finance Minister) kryptonite check; false precision risk on the 340,000 vs. 80,000 figure; whether the number is available without economist mediation | Customer Agent | #1349 intent document; Architect ADR determination | No — required before GR closes |
| **3. BPO business requirements** — minimum viable form of the capability that passes the north star test; acceptance threshold (number sufficient vs. context required); north star test assessment for #1349 | Business Product Owner | #1349 intent document; G3 scope | No — required before GR closes |

**Activation calls (PM Agent to issue upon EL approval of this entry):**

*UX Designer:*
> UX Designer: JOURNEY — counter-scenario comparison (#1349, M18 GR): Author the user journey for the counter-scenario comparison capability. Specific questions to answer: (1) Which user — Eleni (Persona 2) or Aicha (Persona 5) — initiates the counter-scenario comparison in the Demo 7 Act 2 flow? (2) At what moment does she encounter the number differential (e.g., 340,000 vs. 80,000)? What is she doing with it — citing, persuading, defending? (3) Does the number differential require a dedicated UI element, or does it emerge from overlaid Zone 1A trajectories with CI bands (#1254)? (4) What is the interaction model — does the user configure which step to compare, or is the differential surfaced at a canonical point (e.g., terminal step, worst-case step, first MDA crossing)? The journey must be specific enough to write intent document acceptance criteria from. File the artifact in a PR targeting `release/m18`.

*Customer Agent:*
> Customer Agent: AUDIT — counter-scenario comparison (#1349): does the proposed capability (distributional number differential with CI bands) serve Persona 2 (Eleni, Finance Ministry Negotiator) and Persona 5 (Aicha Mbaye, Finance Minister) without kryptonite? Specifically: (1) In what negotiation moment does Eleni cite the 340,000 vs. 80,000 figure? (2) Is the number available in a form she can read without economist mediation? (3) Does surfacing a specific differential introduce false precision risk — and if so, what disclosure is required at the point of citation? Also assess Persona 1 (Thabo Nkosi, Finance Minister) if the capability is presented in Mode 1 replay. File the Layer 3 assessment artifact in a PR targeting `release/m18`.

*Business Product Owner (after UX journey is on record):*
> Business Product Owner: PRIORITIZE — counter-scenario comparison (#1349): what is the minimum viable form of this capability that passes the north star test (a finance minister sitting across from an IMF negotiating team in that moment)? Define: (1) the minimum presentable output (is a number sufficient, or is context — confidence band, scenario labels — required for the number to be usable?); (2) the acceptance threshold (what does "comparison" mean — side-by-side number? overlay chart? summary sentence?); (3) the north star test assessment for this capability — named country, named negotiation moment, named conclusion. File the business requirements artifact in a PR targeting `release/m18`.

---

## Section 5 — Near-Miss Sweep

**Near-miss sweep date:** 2026-06-26
**Sweep period:** M17 exit ceremony (2026-06-26) through M18 GR sprint entry filing (2026-06-26)

| Finding | Category | PI Agent register call issued? | NM entry number |
|---|---|---|---|
| No new process gaps identified. All M17 NM entries (NM-066 through NM-071) were resolved before M18 kickoff and confirmed resolved in G1 and G2 sprint entries filed same session. | N/A | N/A | N/A |

---

## Section 6 — Sprint Group Isolation (Pre-wave adaptation)

*GR produces requirements artifacts (docs) only. Standard isolation protocol adapted for a pre-wave requirements group.*

### 6.1 — Sprint sub-branch

| Field | Value |
|---|---|
| Sprint sub-branch | N/A — requirements phase |
| Branch pattern for artifact PRs | `chore/m18-gr-{artifact-short-name}` targeting `release/m18` directly |
| Sprint journal issue | #1352 |

GR artifacts are filed as docs-only PRs. Each artifact may be its own PR or combined. PM Agent opens PRs for shared-state files (e.g., any SESSION_STATE.md update at GR close) via the standard coordination lane.

### 6.2 — File-conflict risk assessment

| File | Lane required | Trigger |
|---|---|---|
| `docs/ux/user-journeys.md` or new journey doc | GR artifact PR (docs only) | UX journey for counter-scenario comparison |
| Customer Agent Layer 3 artifact file | GR artifact PR (docs only) | Layer 3 assessment for Personas 1, 2, 5 |
| BPO business requirements artifact file | GR artifact PR (docs only) | Business requirements and user stories |
| `SESSION_STATE.md` | PM Agent coordination lane | GR close cockpit update |
| `docs/process/near-miss-registry.md` | PM Agent coordination lane (PI Agent authors) | If NM identified |
| `docs/compliance/scan-registry.md` | PM Agent coordination lane | If compliance scan produced |

No code files in scope. No risk of conflict with G1 (TrajectoryView.tsx / banding engine) or G2 (Zone 1D / PSP module).

### 6.3 — Infrastructure dependency declaration

- [x] No DS-owned file changes required. All GR writes are docs-only artifact files.

#### 6.3a — New output paths declaration

- [x] No new output directories introduced by GR. Requirements artifacts are markdown files in existing `docs/` subdirectories.

### 6.4 — Cross-group dependency declaration

- [x] No upstream cross-group dependencies. GR can proceed immediately.

GR's output is a downstream dependency for G3 (G3 sprint entry requires all three GR artifacts on record). This dependency is recorded in the G3 sprint entry template requirement: "GR close confirmed — all three artifacts on record."

### 6.5 — Prior NM verification

**NM verification sweep date:** 2026-06-26
**Sweep period:** M17 exit through M18 GR sprint entry

| NM entry | Process improvement required | Applied in this sprint? |
|---|---|---|
| NM-069 | New output directories covered by `.gitignore` in same PR | Yes — GR produces no code output; §6.3a confirmed |
| NM-070 | Pre-push hook enforcing ruff + mypy + npm build | N/A — GR produces no code PRs; hook applies to any code PRs in later sprint groups |
| NM-071 | Wave concurrency ceiling check at wave kickoff | Yes — GR is pre-wave; not counted toward ceiling; §1 records this explicitly |
| NM-068 | Prior NM verification field in sprint entry | Yes — this section (§6.5) |

---

## GR Close Conditions

*GR closes when all three artifacts are on record. GR close is confirmed by the PM Agent as a comment on #1352 citing all three artifact paths. G3 sprint entry may not be filed until PM Agent records GR close.*

| Condition | Artifact path | Status |
|---|---|---|
| UX journey on record | TBD at filing | Not yet filed |
| Customer Agent Layer 3 on record | TBD at filing | Not yet filed |
| BPO business requirements on record | TBD at filing | Not yet filed |
| PM Agent close confirmation comment on #1352 | GitHub comment | Not yet filed |

**G3 sprint entry prerequisite statement (to be copied into G3 entry):**
> GR confirmed closed — PM Agent comment on #1352 (date: TBD). UX journey at `{path}`. Customer Agent Layer 3 at `{path}`. BPO business requirements at `{path}`. Architect ADR determination: TBD.

---

## EL Approval Record

**EL approval:** Pending

> {EL approval statement — GR phase may proceed; artifact PRs may target release/m18 directly}
> — @PublicEnemage ({date})
