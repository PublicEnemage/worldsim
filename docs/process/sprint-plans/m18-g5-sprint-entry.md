---
name: m18-g5-sprint-entry
type: sprint-entry
milestone: M18 — Full Argument and Demo 7
sprint-group: G5 — Demo 7 Readiness
status: EL-approved 2026-06-28
authored-by: PM Agent
authored-date: 2026-06-28
el-approved: 2026-06-28
release-branch: release/m18
sop-reference: docs/process/sprint-planning-sop.md
---

# Sprint Entry — M18, G5: Demo 7 Readiness

**Status:** EL-approved 2026-06-28
**Date authored:** 2026-06-28
**Release branch:** `release/m18`
**Sprint plan:** `docs/process/sprint-plans/m18-sprint-plan.md` (EL-approved 2026-06-26, PR #1364)
**Sprint journal issue:** #1435

*Authority: `docs/process/sprint-planning-sop.md §Sprint Entry Gate` (Phase C output).
G5 delivers two Demo 7 readiness items: (1) the Frame A TTS narration correction (DEMO6-009 bug —
"approaching" contradicts populated Zone 1B; narration-only fix), and (2) the Zone 3 auditability
panel on `DistributionalComparisonSummary` (G3 CA condition — expandable methodology panel for
Persona 1 analytical scrutiny during the live external session). Also includes the NM-076 process
improvement to `docs/CODING_STANDARDS.md` (testid rename crosscheck rule). All G1–G4 groups are
closed; G5 is the sole active group in Wave 3.*

---

## Section 1 — Sprint Identification

| Field | Value |
|---|---|
| Milestone | M18 — Full Argument and Demo 7 |
| GitHub Milestone | #19 |
| Sprint group | G5 — Demo 7 Readiness (Wave 3) |
| Release branch | `release/m18` |
| Sprint sub-branch | `sprint/m18-g5` |
| Sprint plan document | `docs/process/sprint-plans/m18-sprint-plan.md` |
| Exit checklist issue | #1340 |
| Sprint journal issue | #1435 |
| Sprint groups in scope | G5 only |
| Wave coordination tier | **Standard** — 1 concurrent group (G1–G4 all closed at G5 entry). No coordination protocol required. |
| Concurrent groups at entry | 1 of 5 ceiling (G5 only). All G1–G4 integration PRs merged to `release/m18`. |
| Cross-group dependencies | None — all prior groups closed. No shared-file write contention. |

---

## Section 2 — Entry Invariants Checklist

*All items must be confirmed before any G5 implementation PR opens.*

### 2.1 — Structural gates

- [x] **Release branch exists:** `release/m18` cut from `main` 2026-06-26; PR #1434 (state-sync-025) merged; current at `18d7543`
- [x] **CI trigger verified:** `.github/workflows/ci.yml` `pull_request: branches` includes `release/m*` and `sprint/m*` — confirmed 2026-06-26; 6 required checks on sprint branches: `changes`, `lint`, `test-backend`, `playwright-e2e`, `compliance-scan`, `branch-naming`
- [x] **Sprint plan EL-approved:** `docs/process/sprint-plans/m18-sprint-plan.md` EL-approved 2026-06-26 (PR #1364 merged)

### 2.2 — ADR prerequisite gate

Neither G5 deliverable requires a new ADR:

- **#1238 (TTS narration fix):** Narration-only change to `demo-narrated.spec.ts`. No architectural decision involved — correcting narration text to match the populated Zone 1B screen state produced by existing G3 implementation.
- **#1422 (Zone 3 auditability panel):** Expandable panel on `DistributionalComparisonSummary` within Zone 1B. Falls within existing architectural scope of ADR-014 (Zone 1B information architecture) and ADR-018 (Zone 1B proportional allocation). The G3 CA condition explicitly scoped this as a click/expand interaction on an existing Zone 1B element — not a new Zone or new layout zone. Backend data (`methodology_summary` field, `_DISTRIBUTIONAL_TIER`, `_DISTRIBUTIONAL_METHODOLOGY` constants) already exists on the comparison endpoint response. No new architectural boundaries crossed.

| Group | Required ADR | ADR status | Gate |
|---|---|---|---|
| G5 — #1238 + #1422 | None | N/A | **CLEAR** |

- [x] No ADR prerequisite. Gate: **CLEAR.**

### 2.3 — Intent document gate

**#1238 — TTS narration fix:**

This is a bug fix where the implementation and the test artifact are the same file (`demo-narrated.spec.ts`). The acceptance criteria in Issue #1238 are fully specified (AC-1 through AC-4 with exact language requirements and screenshot recapture scope). A separate intent document would duplicate the issue without adding resolution. **For this narration-only bug fix, Issue #1238 ACs serve as the intent document equivalent.** The implementing agent must read #1238 in full before opening a feature branch.

- [x] #1238 ACs on record as binding spec — no separate intent document required

**#1422 — Zone 3 auditability panel:**

User-facing deliverable. Intent document required before implementation PR opens.

- [ ] Intent document filed: `docs/process/intents/M18-G5-2026-06-28-zone3-auditability-panel.md` — **required before #1422 implementation PR opens**

**Observable application state (must be assertable without reading implementation code):**

- "At Zone 1B in the comparison view, the `DistributionalComparisonSummary` element has a single-click expand affordance (e.g., `data-testid="methodology-panel-toggle"`). Clicking it reveals the Zone 3 auditability panel without navigating away from the primary viewport."
- "The expanded methodology panel shows: (1) entity Q1 population used (ZMB: 3,894,625 — UN WPP 2024, 20% Q1 fraction); (2) CI methodology (±13–16% T3 placeholder); (3) `poverty_headcount_ratio` extraction path (Q1 CHT cohort mean; main entity fallback); (4) tier rationale: why T3 (regional aggregate, not calibrated country-level Q1 income share)."
- "Lucas (Persona 1) can open the panel and read all four items without leaving Zone 1B or scrolling to a separate section."

**Content requirements for the intent document:**
- Expand/collapse toggle location and testid on `DistributionalComparisonSummary`
- Panel content: 4 named fields (population, CI methodology, extraction path, tier rationale) with exact values from `_DISTRIBUTIONAL_TIER` and `_DISTRIBUTIONAL_METHODOLOGY` constants and `methodology_summary` field
- No new backend endpoint required — all data is present in the existing comparison endpoint response
- Visual: panel appears inline (not a modal or drawer); does not scroll Zone 1B header out of view
- Acceptance criteria: `data-testid="methodology-panel-toggle"` present; panel content testids for each of the 4 fields

**UX/UI design artifact gate:**

The Zone 3 auditability panel is a click/expand interaction within an existing Zone 1B element. The design scope is constrained by the CA condition spec in the G3 sprint exit §3 (which defines exactly what Lucas needs to see). This is not a new layout zone or new interaction paradigm — it is a standard expand/collapse on an existing card component. No UX mockup or multi-agent panel review is required at the UX architecture level; the G3 CA condition assessment serves as the specification basis.

**Intent document status:**

| Deliverable | ADR reference | Intent document path | Filed? |
|---|---|---|---|
| #1238 — TTS narration fix | N/A | Issue #1238 ACs serve as spec | Yes — issue ACs on record |
| #1422 — Zone 3 auditability panel | ADR-014 (Zone 1B), ADR-018 (proportional allocation) | `docs/process/intents/M18-G5-2026-06-28-zone3-auditability-panel.md` | No — **required before #1422 implementation PR opens** |
| NM-076 — CODING_STANDARDS.md testid rename rule | N/A | Process improvement — no intent document required | N/A |

### 2.4 — QA test authorship gate

**#1238 — TTS narration fix:**

Implementation and QA tests are unified — the change IS to `demo-narrated.spec.ts`. The ACs in Issue #1238 define the pass conditions (no "approaching" language with populated Zone 1B; populated-state language present; spec runs to exit 0; screenshot recaptured). Test authorship and implementation are the same act for this narration-only bug fix.

- [x] #1238 test authorship unified with implementation — no separate test authorship step required

**#1422 — Zone 3 auditability panel:**

E2E test must be authored from the intent document ACs before implementation code is written.

- [ ] QA test file authored: `frontend/tests/e2e/m18-g5-zone3-auditability.spec.ts` — **required before #1422 implementation PR opens**

The E2E test must assert (non-exhaustive — full set derived from intent document):
- `data-testid="methodology-panel-toggle"` is present on the `DistributionalComparisonSummary` element in the comparison view
- Before clicking: panel content is not visible (collapsed by default)
- After clicking toggle: methodology panel is visible and contains entity Q1 population text, CI band range text, `poverty_headcount_ratio` extraction path, and T3 tier rationale — each assertable via a named testid
- Toggle click again: panel collapses
- Panel visible without leaving primary viewport and without Zone 1B header scrolling out of view

**QA test status:**

| Deliverable | Test file path | Authored before implementation? |
|---|---|---|
| #1238 — TTS narration fix | `frontend/tests/e2e/demo-narrated.spec.ts` (modified in place) | Yes — unified with implementation |
| #1422 — Zone 3 auditability panel | `frontend/tests/e2e/m18-g5-zone3-auditability.spec.ts` | No — **required before implementation PR opens** |

---

## Section 3 — Scope Declaration

### 3.1 — Issues in scope

| Issue | Title | Priority | Observable application state |
|---|---|---|---|
| #1238 | Frame A TTS narration fix (DEMO6-009) | **Must fix** — visible contradiction to live Demo 7 audience | Frame A `speak()` call does not contain "approaching the recovery floor" in a context implying Zone 1B is empty; narration references confirmed crossings in populated Zone 1B. `demo-narrated.spec.ts` runs to completion with exit 0. `frame-a-cohort-threshold.png` recaptured. |
| #1422 | Zone 3 auditability panel for DistributionalComparisonSummary | High — G3 CA condition; Demo 7 analytical scrutiny readiness | Lucas (Persona 1) can open the methodology panel from within Zone 1B (single click/expand) and read all four content items (entity Q1 population, CI methodology, extraction path, tier rationale) without leaving the primary viewport or consulting external documentation. |
| NM-076 process improvement | Add testid rename crosscheck rule to CODING_STANDARDS.md | Process — NM-076 filed in G4 | `docs/CODING_STANDARDS.md` contains a testid rename rule: when renaming any `data-testid`, run `grep -r 'old-testid-value' frontend/tests/e2e/` before opening the PR and update every matching locator in the same PR. |

### 3.2 — Issues explicitly out of scope

| Issue | Title | Rationale for exclusion |
|---|---|---|
| #843 | Demo 7 live external session | Scheduling gate, not an implementation deliverable. Unblocked at G4 exit; EL schedules independently. |
| #1340 | M18 Exit Checklist | Exit gate issue — not an implementation deliverable. Opens after Demo 7 runs. |
| #1059 | HCL narration into Demo 5 Frame E | Closed as superseded 2026-06-28 — Demo 7 does not reuse Demo 5 frame structure. |
| Additional Zone 1B interactive features | Any Zone 1B interaction beyond the G3 CA condition expand/collapse scope | Out of scope. Zone 1B content was fully delivered in G3 (#1349). G5 adds only the auditability expand/collapse for the CA condition. |

---

## Section 4 — ADR Prerequisite Summary

| Group | ADR required | ADR status | Implementation may begin? |
|---|---|---|---|
| G5 — #1238 + #1422 + NM-076 improvement | None | N/A | Yes — after EL approves this entry, intent document for #1422 is filed, and QA tests for #1422 are authored before implementation |

**Implementation sequencing for G5:**

1. EL approves this entry document *(approved in session 2026-06-28 — recorded in §EL Approval Record)*
2. Implementing agent reads Issue #1238 ACs and Issue #1422 scope before opening any feature branch
3. PM Agent confirms `sprint/m18-g5` is cut from `release/m18` and records in #1435 *(cut and pushed 2026-06-28)*
4. **#1238 first** (simpler, must-fix): feature branch `feat/m18-g5-narration-fix` from `sprint/m18-g5`; update Frame A `speak()` call; verify step 8 consistency; recapture screenshot; AC-1 through AC-4 verified locally; pre-push gate; PR targeting `sprint/m18-g5`; set auto-merge
5. **#1422 intent document** (Frontend Architect): file `docs/process/intents/M18-G5-2026-06-28-zone3-auditability-panel.md` per §2.3 spec above; PR targeting `sprint/m18-g5`; set auto-merge
6. **#1422 QA tests** (QA Lead): author `frontend/tests/e2e/m18-g5-zone3-auditability.spec.ts` from intent document ACs (red before implementation); PR targeting `sprint/m18-g5`; set auto-merge
7. **#1422 implementation**: feature branch `feat/m18-g5-zone3-auditability` from `sprint/m18-g5` (after intent doc and QA tests merge); add expand/collapse to `DistributionalComparisonSummary.tsx`; populate panel from `methodology_summary` field already in comparison endpoint response; add testids; pre-push gate; PR targeting `sprint/m18-g5`; set auto-merge
8. **NM-076 improvement**: may be included in either the intent doc PR or the implementation PR — `docs/CODING_STANDARDS.md` testid rename rule addition; small, no test required
9. Sprint exit: Business PO ACCEPT for both deliverables; CA L3 for #1422 (Persona 1 — Lucas); north star test artifact; integration PR `sprint/m18-g5` → `release/m18`; PI Agent gate comment; auto-merge

**NM-076 crosscheck application (G5 adds `data-testid` values for #1422 panel):**

Per NM-076 process improvement (to be landed in CODING_STANDARDS.md in this sprint): when any
new `data-testid` is introduced, run `grep -r 'new-testid-value' frontend/tests/e2e/` after
authoring to confirm the QA test references the same strings. For G5 this is a forward-check
(new testids being introduced, not renamed), but the discipline applies equally.

---

## Section 5 — Near-Miss Sweep

**Near-miss sweep date:** 2026-06-28
**Sweep period:** G4 sprint entry filing (2026-06-27) through G5 sprint entry filing (2026-06-28)

| Finding | Category | PI Agent register call issued? | NM entry number |
|---|---|---|---|
| G4 testid renames not crosschecked against E2E corpus before PR #1424; three tests merged broken to sprint/m18-g4; fixed by PR #1426 before integration | near-miss | Yes — filed by PI Agent during G4 session | NM-076 |
| `gh pr create` inferred head from shell CWD (main working tree) rather than worktree branch during G4; PR created with wrong head branch | near-miss | Yes — filed by PM Agent during G4 session | NM-077 |

NM-076 process improvement (CODING_STANDARDS.md testid rename rule) is a named G5 deliverable — included in §3.1 scope. NM-077 is not applicable to G5 (G5 uses the main working tree, single group, no worktrees in use).

---

## Section 6 — Sprint Group Isolation

### 6.1 — Sprint sub-branch

| Field | Value |
|---|---|
| Sprint sub-branch | `sprint/m18-g5` |
| Cut from | `release/m18` — cut 2026-06-28 at commit `18d7543` (post-state-sync-025 merge) |
| Sprint journal issue | #1435 |

Sprint sub-branch already cut and pushed. *(PM Agent action complete 2026-06-28.)*

### 6.2 — File-conflict risk assessment

All G1–G4 groups are closed and their integration PRs are merged to `release/m18`. G5 is the sole active group. No file-conflict risk.

| File | Lane required | Trigger |
|---|---|---|
| `frontend/tests/e2e/demo-narrated.spec.ts` | Sprint sub-branch | #1238 narration fix — lines 400–411 (Frame A speak() call); line ~528 (step 8 consistency check) |
| `frontend/tests/e2e/frame-a-cohort-threshold.png` (screenshot) | Sprint sub-branch | #1238 — recaptured after narration update per AC-4 |
| `frontend/src/components/DistributionalComparisonSummary.tsx` | Sprint sub-branch | #1422 — expand/collapse toggle + methodology panel render |
| `frontend/tests/e2e/m18-g5-zone3-auditability.spec.ts` (new) | Sprint sub-branch | #1422 QA test (authored before implementation) |
| `docs/CODING_STANDARDS.md` | Sprint sub-branch | NM-076 process improvement — testid rename rule addition |
| `docs/process/intents/M18-G5-2026-06-28-zone3-auditability-panel.md` (new) | Sprint sub-branch | #1422 intent document |
| `SESSION_STATE.md` | PM Agent coordination lane | Sprint exit cockpit update |
| `docs/process/near-miss-registry.md` | PM Agent coordination lane (PI Agent authors) | If NM identified during G5 |
| `docs/compliance/scan-registry.md` | PM Agent coordination lane | If compliance scan produced at G5 exit |

### 6.3 — Infrastructure dependency declaration

- [x] No DS-owned file changes required. All G5 writes are to implementation code, test files, documentation, and the intent document.

#### 6.3a — New output paths declaration (NM-069 process improvement)

- [x] No new output directories introduced by G5. `frontend/test-results/`, `frontend/playwright-report/`, `frontend/session-screenshots/` are already covered by `.gitignore` (PR #1346).

No new output paths introduced by this sprint group.

### 6.4 — Cross-group dependency declaration

- [x] No cross-group dependencies. All G1–G4 integration PRs are merged to `release/m18`. G5 starts from a complete M18 Wave 1+2 baseline.

### 6.5 — Prior NM verification (NM-068 process improvement)

**NM verification sweep date:** 2026-06-28
**Sweep period:** G4 sprint entry (2026-06-27) through G5 sprint entry (2026-06-28)

| NM entry | Process improvement required | Applied in this sprint? |
|---|---|---|
| NM-068 | Prior NM verification field in sprint entry | Yes — this section (§6.5) |
| NM-069 | New output directories covered by `.gitignore` in same PR or DS infra lane | Yes — no new output directories; §6.3a confirmed |
| NM-070 | Pre-push hook enforcing ruff + mypy + npm build | Yes — `.githooks/pre-push` active; §4 implementation sequencing requires both gates exit 0 before any push |
| NM-071 | Wave concurrency ceiling check at wave kickoff | Yes — 1 concurrent group (G5 only); Standard tier; ceiling is not a concern |
| NM-075 | Git worktree allocation per sprint group to prevent branch-switch overwrite | N/A — G5 is single-group; main working tree is sufficient. If a second concurrent session were to open, worktree discipline applies. |
| NM-076 | CODING_STANDARDS.md testid rename crosscheck rule | Yes — NM-076 improvement is a named G5 deliverable (§3.1); implementing agent must run testid grep before any PR that introduces or references `data-testid` values |
| NM-077 | `gh pr create` must specify `--head` explicitly when using worktrees | N/A — G5 uses main working tree; no worktrees in use. Applied as awareness context: if worktrees are opened during G5, use `--head sprint/m18-g5` explicitly |

---

## EL Approval Record

**EL approval:** 2026-06-28

> Approved. G5 scope as filed: #1238 (Frame A TTS narration fix — must fix before Demo 7),
> #1422 (Zone 3 auditability panel — G3 CA condition), and NM-076 CODING_STANDARDS.md
> process improvement. No ADR prerequisite. Sprint journal #1435. Sprint branch
> `sprint/m18-g5` cut from `release/m18` at `18d7543`.
> — @PublicEnemage (2026-06-28)
