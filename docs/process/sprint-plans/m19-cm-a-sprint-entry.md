---
name: m19-cm-a-sprint-entry
type: sprint-entry
milestone: M19 — Constraint Search and Empirical Calibration
sprint-group: CM Sprint A — Euro area elasticity calibration (parallel track)
status: Filed
authored-by: PM Agent
authored-date: 2026-07-03
el-approved: 2026-07-03
release-branch: release/m19
sop-reference: docs/process/sprint-planning-sop.md
---

# Sprint Entry — M19, CM Sprint A: Euro Area Elasticity Calibration

**Status:** Filed — EL Approved 2026-07-03
**Date authored:** 2026-07-03
**Release branch:** `release/m19`
**Sprint plan:** `docs/process/sprint-plans/m19-sprint-plan.md`

*Authority: `docs/process/sprint-planning-sop.md §Sprint Entry Gate` (Phase C output).
Changes to this template require PM Agent authorship and EL endorsement.*

---

## Section 1 — Sprint Identification

| Field | Value |
|---|---|
| Milestone | M19 — Constraint Search and Empirical Calibration |
| GitHub Milestone | #21 |
| Sprint number | CM Sprint A (parallel track — Wave 3, concurrent with G5) |
| Release branch | `release/m19` |
| Sprint plan document | `docs/process/sprint-plans/m19-sprint-plan.md` |
| Exit checklist issue | #1535 |
| Sprint groups in scope | CM Sprint A |
| Wave coordination tier | Standard — parallel track; no file-area overlap with G5 or any active G-series sprint |
| Concurrent groups at entry | 2 (G5 + CM Sprint A; no shared files) |
| Cross-group dependencies | None — CM Sprint A touches `backend/app/simulation/modules/demographic/elasticities.py` and `docs/calibration/`; G5 is frontend-only (`CompositeChartSVG`, `FourFrameworkZone1D`, Zone 1 view model). G2D integration PR #1641 (`sprint/m19-g2 → release/m19`) pending auto-merge — no file-area overlap. |

---

## Section 2 — Entry Invariants Checklist

*All items must be checked before any implementation PR is opened for this sprint.
An unchecked invariant blocks the sprint from opening.*

### 2.1 — Structural gates

- [x] **Release branch exists:** `release/m19` cut from `main` 2026-07-02 at 1bf1ecc
- [x] **CI trigger verified:** `.github/workflows/ci.yml` `pull_request: branches` includes `release/m*` (verified at M19 kickoff; sprint-branch-ci-gate Ruleset active)
- [x] **Sprint plan EL-approved:** `docs/process/sprint-plans/m19-sprint-plan.md` — EL-approved 2026-07-02; CM parallel track explicitly authorized therein (§Wave Plan §CM parallel track)

### 2.2 — ADR prerequisite gate

*CM Sprint A is a calibration constant revision within the existing module architecture —
same classification as M17-G1 (see `docs/process/intents/M17-G1-2026-06-25-cm-calibration.md`).
The elasticity constants installed are within the DemographicModule ELASTICITY_REGISTRY
established by ADR-005 Decision 1. No new architectural decision is required.*

- [x] All groups with `BLOCKED_ADR` status have their required ADR accepted — **CLEAR: no BLOCKED_ADR for CM Sprint A**

**ADR prerequisite status:**

| Group | Required ADR | ADR status | Gate |
|---|---|---|---|
| CM Sprint A — ELASTICITY_REGISTRY Euro area family (#1623) | None — calibration constant revision within ADR-005 Decision 1 (DemographicModule) scope | N/A | CLEAR |

### 2.3 — Intent document gate

*CM Sprint A follows the calibration sprint pattern established at M17-G1: the intent document
is filed after EL entry approval; the calibration decision document (specifying the chosen
constants and uncertainty ranges) is filed before the implementation PR opens. The calibration
decision document is a prerequisite for test authorship (§2.4).*

- [ ] Intent document filed for #1623 — to be filed after EL approves this entry

**Intent document status:**

| Deliverable | ADR reference | Intent document path | Filed? |
|---|---|---|---|
| ELASTICITY_REGISTRY — Euro area family calibration (#1623) | ADR-005 Decision 1 (DemographicModule ELASTICITY_REGISTRY) | `docs/process/intents/M19-CMA-2026-07-03-euro-area-elasticity-calibration.md` | Pending — to be filed after EL entry approval |

*The intent document must declare the CM calibration decision document path
(`docs/calibration/m19-cm-a-euro-area-calibration-decision.md`) as a prerequisite artifact
that is filed before the implementation PR opens. This mirrors the M17-G1 pattern where
the calibration decision document was filed before `test_m17_g1_frame_d_calibration.py` could
be authored.*

### 2.4 — QA test authorship gate

*Per the M17-G1 pattern, the CM authors both the calibration decision document and the
integration test from that document — the test bounds are determined by the calibration
research, not this intent document. Test authorship is therefore gated on the calibration
decision document (not on this entry approval).*

*NM-084 obligation (see §6.5): CM must post a formal methodological certification comment
on Issue #1623 before the implementation PR opens. PI Agent must post a gate comment
confirming sign-off is on record before auto-merge is set on the implementation PR.*

- [ ] Calibration decision document filed at `docs/calibration/m19-cm-a-euro-area-calibration-decision.md`
- [ ] QA test file authored for #1623 — to be filed after calibration decision document, before implementation PR opens

**QA test status:**

| Deliverable | Prerequisite artifact | Test file path | Authored before implementation? |
|---|---|---|---|
| Euro area ELASTICITY_REGISTRY calibration (#1623) | `docs/calibration/m19-cm-a-euro-area-calibration-decision.md` | `backend/tests/test_m19_cm_a_elasticity_calibration.py` | Pending — authored from calibration decision document; before implementation PR opens |

*NM-086 process requirement: N/A. CM Sprint A is backend-only calibration — no E2E mock
routes are introduced. No `api_contracts.yml` mock-helper verification is required for this
sprint group.*

---

## Section 3 — Scope Declaration

### 3.0 — Scope lock confirmation (NM-081; sprint-planning-sop.md §Scope lock precondition)

- [x] All ADR decisions affecting this sprint's scope are EL-approved and merged to `release/m19`

**Scope uncertainty:** None. CM Sprint A installs calibration constants for the Euro area
entity family within the existing ELASTICITY_REGISTRY architecture. No pending EL decisions
affect this scope. CM Sprints B and C (Latin America and South Asia families) are explicitly
out of scope for this entry — separate sprint entries will be filed after CM Sprint A exits.

### 3.1 — Issues in scope

| Issue | Title | Group | Priority |
|---|---|---|---|
| #1623 | ELASTICITY_REGISTRY — non-SSA entity family calibration gap (Gap 1: Euro area / GRC priority) | CM Sprint A | High — unblocks Greece 2010 counter-factual MAGNITUDE fidelity; M19 priority per sprint plan |

### 3.2 — Issues explicitly out of scope

| Issue | Title | Horizon | Rationale for exclusion |
|---|---|---|---|
| #1623 Gap 2 — Latin America (ARG, ECU, BOL, PER) | CM Sprint B | After CM Sprint A exit | Sequential CM sprint; separate sprint entry required |
| #1623 Gap 3 — South and SE Asia (PAK, LKA, BGD) | CM Sprint C | After CM Sprint B | Sequential CM sprint; may defer to M20 |
| #1657 | DemographicModule dead event subscriptions + missing elasticity rows | CM gate pending | CM sign-off required before implementation PR opens; separate issue; will coordinate with CM Sprint A exit |
| #1544 | Demo 8 — live stakeholder session | Wave 3 (exit gate) | Post-G5 deliverable; milestone exit gate |
| #1535 | M19 Exit Checklist | Gate issue | Milestone exit gate — not an implementation deliverable |

---

## Section 4 — ADR Prerequisite Summary

| Group | ADR required | ADR status | Implementation may begin? |
|---|---|---|---|
| CM Sprint A — #1623 Euro area ELASTICITY_REGISTRY | None — calibration constant revision within ADR-005 Decision 1 | N/A | Yes — after EL approves entry, intent document filed, calibration decision document filed, CM sign-off on record, and PI Agent gate comment posted on Issue #1623 |

*CM Sprint A does not extend the DemographicModule architecture — it installs calibration
constants for a previously unregistered entity family using the existing `CohortElasticity`
structure. The source citation and `source_registry_id` requirements of ADR-005 §Data Provenance
and `docs/DATA_STANDARDS.md §Data Provenance Requirements` apply to all new ELASTICITY_REGISTRY
entries.*

---

## Section 5 — Near-Miss Sweep

**Near-miss sweep date:** 2026-07-03
**Sweep period:** Since G5 sprint entry (2026-07-03, same session — CM Sprint A is inaugural entry for this parallel track)

| Finding | Category | PI Agent register call issued? | NM entry number |
|---|---|---|---|
| No new process gaps identified in CM Sprint A-specific domain since G5 entry | N/A | N/A | N/A |

*All NMs filed since G4 sprint entry (NM-092, NM-093, NM-094 — DS infra review) are addressed
in §6.5 below. The NM-084 gate is the highest-relevance process improvement for CM Sprint A
and receives explicit treatment in §2.4 and §6.5.*

---

## Section 6 — Sprint Group Isolation (M18 onward)

### 6.1 — Sprint sub-branch

| Field | Value |
|---|---|
| Sprint sub-branch | `sprint/m19-cm-a` |
| Cut from | `release/m19` |
| Sprint journal issue | #1671 |

**PM Agent sprint sub-branch cut command (run after EL approval):**
```bash
git checkout -b sprint/m19-cm-a release/m19 && git push -u origin sprint/m19-cm-a
```

*Per NM-087 and NM-088: run `git status --porcelain` before any checkout. If the main
working tree is dirty, stop and report to EL before proceeding. If a G5 CC session is
active simultaneously, a dedicated worktree must be allocated before branch operations begin:
`git worktree add /tmp/worldsim-cm-a sprint/m19-cm-a`.*

*Per NM-092: if a worktree is used, verify `.git` symlink integrity in the worktree path
(`ls -la /tmp/worldsim-cm-a/.git`) before running any git operations from within it.*

### 6.2 — File-conflict risk assessment

| File | Lane required | Trigger |
|---|---|---|
| `SESSION_STATE.md` | PM Agent coordination lane | Sprint exit cockpit update |
| `docs/process/near-miss-registry.md` | PM Agent coordination lane (PI Agent authors) | If NM identified during sprint |
| `docs/compliance/scan-registry.md` | PM Agent coordination lane | If compliance scan produced at sprint exit |
| `backend/app/simulation/modules/demographic/elasticities.py` | Sprint sub-branch | Primary implementation file — ELASTICITY_REGISTRY Euro area entries |
| `docs/calibration/m19-cm-a-euro-area-calibration-decision.md` | Sprint sub-branch | CM calibration decision document — new file |
| `backend/tests/test_m19_cm_a_elasticity_calibration.py` | Sprint sub-branch | QA test file — new file |
| `docs/process/intents/M19-CMA-2026-07-03-euro-area-elasticity-calibration.md` | Sprint sub-branch | Intent document — new file |

**No file-area overlap with G5:** G5 writes exclusively to frontend source
(`frontend/src/components/CompositeChartSVG.tsx`, `FourFrameworkZone1D.tsx`, Zone 1 view model
files) and frontend tests. `elasticities.py` is not touched by any active G-series sprint.

**No file-area overlap with G2D integration PR #1641:** G2D writes to
`backend/app/simulation/modules/external_sector/`, `macroeconomic/`, and the Iceland
backtesting fixture file. No overlap with `demographic/elasticities.py`.

*Per NM-093: CM Sprint A must not write to shared state files (`SESSION_STATE.md`,
`docs/process/near-miss-registry.md`, `docs/compliance/scan-registry.md`) directly from
the `sprint/m19-cm-a` branch. All shared state updates route through the PM Agent
coordination lane (`chore/m19-state-sync-NNN → release/m19`).*

### 6.3 — Infrastructure dependency declaration

- [x] No DS-owned file changes required

No changes to `.github/workflows/`, `.githooks/`, or `.gitignore` are anticipated. CM Sprint A
introduces no new backend modules, no new output directories, and no new CI workflow steps
beyond the standard `test-backend` check that already runs `pytest backend/tests/`.

#### 6.3a — New output paths declaration (NM-069)

- [x] No new output directories — all generated paths are already covered by `.gitignore`

*CM Sprint A is a pure backend calibration change — a calibration decision document in
`docs/calibration/` (tracked) and new test/source entries. No new output directories are
introduced.*

### 6.4 — Cross-group dependency declaration

- [x] No cross-group dependencies

**CM Sprint A is fully independent of G5.** The ELASTICITY_REGISTRY change in
`backend/app/simulation/modules/demographic/elasticities.py` is the only code file modified,
and no active sprint group touches this file. The integration test validates MAGNITUDE fidelity
by invoking the existing Greece 2010 backtesting harness (G2C #1547, confirmed and on
`release/m19`) with the updated elasticity constants — no new harness infrastructure is
required.

**Sequence note:** CM Sprint A's exit gate (Greece 2010 harness MAGNITUDE output) depends on
the G2C Greece 2010 fixture (#1547) being on `release/m19`. G2D integration PR #1641
(`sprint/m19-g2 → release/m19`) merged 2026-07-03 — Greece 2010 fixture is confirmed on
`release/m19`. Sprint branch `sprint/m19-cm-a` may be cut immediately after EL entry approval.

### 6.5 — Prior NM verification (NM-068 process improvement)

**NM verification sweep date:** 2026-07-03
**Sweep period:** Since G5 sprint entry (2026-07-03)

| NM entry | Process improvement required | Applied in this sprint? |
|---|---|---|
| NM-084 | CM sign-off on calibration/fixture PRs must precede auto-merge; PI Agent posts gate comment before implementing agent sets auto-merge | **Yes — primary gate for CM Sprint A.** Special handling: CM is the implementing agent. Mechanism: (1) CM posts a formal methodological certification comment on Issue #1623, explicitly certifying the chosen constants, uncertainty ranges, and source quality before the implementation PR opens. (2) PI Agent posts a gate comment on Issue #1623 confirming the CM certification comment is on record. (3) Auto-merge may not be set on the implementation PR until the PI Agent gate comment exists. This two-step mechanism satisfies NM-084 in a self-certifying sprint. |
| NM-085 | Sprint entry §6.2 must document co-dependent fixture CI ordering risk | Yes — declared in §6.4. G2D integration PR #1641 confirmed merged 2026-07-03; Greece 2010 fixture is on `release/m19`. Dependency satisfied before entry filing. Sprint branch may be cut immediately after EL approval. |
| NM-086 | QA Lead mock-helper verification against `api_contracts.yml` before intent document is approved | N/A — CM Sprint A is backend-only calibration. No E2E mock routes. |
| NM-087 | Pre-checkout dirty-tree guard before any `git checkout` or `git checkout -b` | Yes — declared in §6.1 branch-cut note. CM implementing agent runs `git status --porcelain` before cutting `sprint/m19-cm-a`. |
| NM-088 | If parallel CC session active, each session uses dedicated worktree | Yes — declared in §6.1. If G5 session and CM session are active simultaneously, each must operate in a dedicated worktree. |
| NM-092 | Worktree `.git` symlink integrity check before any git operations from worktree | Yes — declared in §6.1. If a worktree is used for CM Sprint A, symlink integrity verified before any operations. |
| NM-093 | Bidirectional shared-state lane prohibition: sprint branches must not carry shared-state commits | Yes — declared in §6.2. All shared state updates from CM Sprint A route through PM Agent coordination lane. |
| NM-094 | PI Agent must verify test file is present on sprint branch before exit gate passes | Yes — applies at exit gate. PI Agent confirms `backend/tests/test_m19_cm_a_elasticity_calibration.py` is present on `sprint/m19-cm-a` before confirming exit conditions satisfied. |

---

## CM Sprint A: Calibration Summary

*For reference by the implementing agent (Chief Methodologist).*

**Gap being closed:** ELASTICITY_REGISTRY has no Euro area entity family entries. Greece 2010
counter-factual (#1547) is currently DIRECTION_ONLY — cannot produce a defensible magnitude
claim for the unemployment trajectory divergence under the heterodox primary-surplus counter-factual.

**Required calibration sources (minimum):**
- Fiscal multiplier for open economies with fixed exchange rates: Ilzetzki, Mendoza & Végh (2013) — "How Big (Small?) are Fiscal Multipliers?" — JME; `ACADEMIC_LITERATURE_ILZETZKI_2013` source_registry_id
- GDP-to-unemployment elasticity for Southern European labour markets: OECD Employment Outlook (Southern Europe panel, 2010–2015 era) or Blanchard & Leigh (2013) IMF WP "Growth Forecast Errors and Fiscal Multipliers"; source_registry_id to be assigned at calibration decision document filing

**Exit gate:** Greece 2010 backtesting harness run (using existing G2C fixture `#1547` on
`release/m19`) produces a MAGNITUDE-class verdict (not DIRECTION_ONLY) for both:
1. GDP trajectory divergence between orthodox (IMF-recommended primary surplus) and
   heterodox (lower fiscal adjustment) counter-factual paths
2. Unemployment trajectory divergence between the same two paths

MAGNITUDE verdict requires the delta between paths to exceed the calibration uncertainty
range declared in the calibration decision document. The calibration decision document
must specify both the constant value and the uncertainty range before the test can be
authored.

**Confidence tier target:** T2 (academic literature with peer review) for the multiplier
constants. The exit gate test will assert T2 entries are present. T3 entries may supplement
where T2 sources are unavailable for specific cohort linkages, per `docs/DATA_STANDARDS.md
§Confidence Tier System`.

---

## EL Approval Record

*EL reviews this entry document before any implementation PR opens. Approval is recorded here
or as a comment on the exit checklist issue #1535.*

**EL approval:** Approved — 2026-07-03

> CM Sprint A entry approved. Parallel track authorized per M19 sprint plan §CM parallel track.
> G2D integration PR #1641 confirmed merged — Greece 2010 fixture on release/m19 (exit gate
> dependency cleared). Sprint journal issue #1671 opened. Sprint branch sprint/m19-cm-a cut
> from release/m19. Intent document authorized; calibration decision document and QA test to
> be filed before implementation PR opens. NM-084 two-step CM sign-off mechanism active.
> — @PublicEnemage (2026-07-03)
