---
name: m19-g3-sprint-entry
type: sprint-entry
milestone: M19 — Constraint Search and Empirical Calibration
sprint-group: G3 — Bayesian Posterior Calibration
status: Filed
authored-by: PM Agent
authored-date: 2026-07-02
el-approved: false
release-branch: release/m19
sop-reference: docs/process/sprint-planning-sop.md
---

# Sprint Entry — M19, G3: Bayesian Posterior Calibration

**Status:** Filed — awaiting EL approval before implementation begins
**Date authored:** 2026-07-02
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
| Sprint number | 4 (G3 — Wave 2) |
| Release branch | `release/m19` |
| Sprint plan document | `docs/process/sprint-plans/m19-sprint-plan.md` |
| Exit checklist issue | #1535 |
| Sprint groups in scope | G3 |
| Wave coordination tier | Standard (G3 solo at entry; G2C/G4 to join Wave 2 after G3 ADR-007 amendment accepted) |
| Concurrent groups at entry | 1 (G3 only) |
| Cross-group dependencies | G4 #1529 CI label text must coordinate with G3 before either PR opens — see §6.4 |

---

## Section 2 — Entry Invariants Checklist

*All items must be checked before any implementation PR is opened for this sprint.
An unchecked invariant blocks the sprint from opening.*

### 2.1 — Structural gates

- [x] **Release branch exists:** `release/m19` cut from `main` 2026-07-02 at 1bf1ecc
- [x] **CI trigger verified:** `.github/workflows/ci.yml` `pull_request: branches` includes `release/m*` (verified at M19 kickoff; sprint-branch-ci-gate Ruleset active)
- [x] **Sprint plan EL-approved:** `docs/process/sprint-plans/m19-sprint-plan.md` — EL-approved 2026-07-02

### 2.2 — ADR prerequisite gate

*BLOCKED_ADR: ADR-007 amendment (ARCH-016) is ASSIGNED but not yet accepted. G3 implementation
PRs must not open until the amendment is accepted. The sprint branch may be cut and the sprint
journal issue opened now; intent documents are deferred until after amendment acceptance (see §2.3).*

- [ ] All groups with `BLOCKED_ADR` status have their required ADR accepted — **NOT CLEARED: ADR-007 amendment (ARCH-016) in progress**

**ADR prerequisite status:**

| Group | Required ADR | ADR status | Gate |
|---|---|---|---|
| G3 — Bayesian posterior (#1543) | ADR-007 amendment (ARCH-016) | ASSIGNED — authorship in progress | BLOCKED_ADR |
| G3 — Meaninglessness threshold (#1536) | ADR-007 amendment (ARCH-016) — Section 6 implementation clause | ASSIGNED — authorship in progress | BLOCKED_ADR |
| G3 — BandResult visible fields (#1537) | ADR-007 amendment (ARCH-016) — is_pre_calibration display contract | ASSIGNED — authorship in progress | BLOCKED_ADR |

**BLOCKED_ADR gate condition:**
> G3 implementation PRs (`feat/m19-g3-*`) may not be opened until:
> 1. ADR-007 amendment (ARCH-016) is accepted by EL, AND
> 2. PI Agent posts gate comment on the sprint journal issue confirming ARCH-016 acceptance
>
> The sprint branch (`sprint/m19-g3`) may be cut now. Intent documents and QA tests are
> deferred until ARCH-016 acceptance — their content depends on posterior calibration method
> decisions made in the ADR.

### 2.3 — Intent document gate

*Intent documents for all three G3 deliverables are deferred until ADR-007 amendment (ARCH-016)
is accepted. The amendment determines: (a) the posterior calibration method for #1543,
(b) the exact suppression condition for #1536, (c) the is_pre_calibration display contract
for #1537. Filing intent documents before these are decided would produce intent documents
that contradict the accepted ADR.*

- [ ] Intent document filed for every user-facing deliverable — **DEFERRED: pending ARCH-016 acceptance**

**Intent document status:**

| Deliverable | ADR reference | Intent document path | Filed? |
|---|---|---|---|
| ADR-007 Bayesian posterior layer (#1543) | ADR-007 amendment (ARCH-016) | `docs/process/intents/M19-G3-{date}-bayesian-posterior.md` | No — BLOCKED_ADR |
| Meaninglessness threshold (#1536) | ADR-007 amendment (ARCH-016) | `docs/process/intents/M19-G3-{date}-meaninglessness-threshold.md` | No — BLOCKED_ADR |
| BandResult visible fields (#1537) | ADR-007 amendment (ARCH-016) | `docs/process/intents/M19-G3-{date}-bandresult-visible-fields.md` | No — BLOCKED_ADR |

*Intent documents are user-facing deliverables for #1537 (frontend surface) and methodology
deliverables for #1543/#1536. All three require ARCH-016 acceptance before filing.*

### 2.4 — QA test authorship gate

*QA tests are deferred pending intent documents, which are deferred pending ARCH-016 acceptance.
The test authorship gate is not blocked independently — it is blocked transitively by the
BLOCKED_ADR condition.*

- [ ] QA test file authored for every user-facing deliverable — **DEFERRED: pending intent documents (pending ARCH-016)**

**QA test status:**

| Deliverable | Intent document | Test file path | Authored before implementation? |
|---|---|---|---|
| ADR-007 Bayesian posterior (#1543) | Deferred | `backend/tests/test_m19_g3_bayesian_posterior.py` | No — pending intent document |
| Meaninglessness threshold (#1536) | Deferred | `backend/tests/test_m19_g3_meaninglessness_threshold.py` | No — pending intent document |
| BandResult visible fields (#1537) | Deferred | `backend/tests/test_m19_g3_bandresult_visible_fields.py` | No — pending intent document |

---

## Section 3 — Scope Declaration

### 3.0 — Scope lock confirmation (NM-081)

- [ ] All ADR decisions affecting this sprint's scope are EL-approved and merged — **NOT CLEARED: ARCH-016 in progress**

**Scope uncertainty:** ADR-007 amendment (ARCH-016) is ASSIGNED but not yet accepted. Known
scope dependencies on the amendment:
- The posterior calibration method (Section 8) determines the implementation shape of #1543
- The meaninglessness suppression condition (Section 6) determines the exact threshold for #1536
- The is_pre_calibration display contract determines which #1537 fields surface to the frontend

EL has acknowledged this uncertainty at G3 sprint entry approval. Sprint branch may be cut; scope
lock is confirmed at ADR-007 amendment acceptance. Implementation PRs do not open until scope is locked.

### 3.1 — Issues in scope

| Issue | Title | Group | Priority |
|---|---|---|---|
| #1543 | ADR-007 Bayesian posterior layer — fit CI coverage multipliers to SEN/ZMB outcomes; is_pre_calibration=False gate | G3 | High — Demo 8 Act 2 CI credibility |
| #1536 | ADR-007 meaninglessness threshold — suppress T5 indicators at step 7+ producing [0,1] bands | G3 | High — required per ADR-007 Section 6 design |
| #1537 | BandResult visible fields — expose is_pre_calibration and band_method to frontend; update CI label display contract | G3 | High — posterior UX prereq; coord with G4 #1529 |

### 3.2 — Issues explicitly out of scope

| Issue | Title | Horizon | Rationale for exclusion |
|---|---|---|---|
| #1529 | '95% CI' label precision fix | G4 (Wave 2) | Deferred to G4 — content depends on G3 #1537 band_method field; G4 must not open until G3 #1537 terminology is settled |
| #1528 | PSP driver arc + auditability panel (DEMO-165) | G4 (Wave 2) | Separate G4 sprint; no dependency on G3 |
| #1538 | Focal cohort floor validation | Pre-wave / standalone | Filed as prerequisite to G1 #1540; not in G3 scope |
| #1456 | MDAAlertPanel Zone1B: scenarioId crash | Pre-wave | Standalone crash fix; not in G3 scope |
| G2C fixtures | Greece, Argentina, Sri Lanka, Pakistan, Turkey, Egypt, Ghana | G2C (Wave 2) | Parallel with G3 but separate sprint group; not in G3 scope |

---

## Section 4 — ADR Prerequisite Summary

| Group | ADR required | ADR status | Implementation may begin? |
|---|---|---|---|
| G3 — All three issues | ADR-007 amendment (ARCH-016) | ASSIGNED — authorship in progress | No — awaiting ARCH-016 acceptance |

**Path to CLEAR:**
1. Architect Agent authors ADR-007 amendment (Section 8 + Section 6 implementation clause)
2. CM and CE panel review (C — mandatory per ARCH-016 panel)
3. UX Designer consultation on is_pre_calibration display contract (C — for #1537)
4. EL acceptance
5. PI Agent posts gate comment on G3 sprint journal issue: "ARCH-016 accepted — BLOCKED_ADR cleared"
6. PM Agent updates this document §2.2 gate to CLEAR
7. Intent documents filed; QA tests authored; implementation PRs open

---

## Section 5 — Near-Miss Sweep

**Near-miss sweep date:** 2026-07-02
**Sweep period:** Since G2B close (2026-07-02)

| Finding | Category | PI Agent register call issued? | NM entry number |
|---|---|---|---|
| CM sign-off obtained after feature PRs opened (auto-merge firing risk) | Near-miss | Yes — filed at G2B exit | NM-084 |
| Co-dependent fixture PRs produce transient cross-test failures on sprint branch | Near-miss | Yes — filed at G2B exit | NM-085 |
| E2E mock route not verified against api_contracts.yml before implementation PR | Near-miss | Yes — filed at G1 exit review | NM-086 |

*All three are codified. G3 process improvements to apply are declared in §6.5.*

---

## Section 6 — Sprint Group Isolation (M18 onward)

### 6.1 — Sprint sub-branch

| Field | Value |
|---|---|
| Sprint sub-branch | `sprint/m19-g3` |
| Cut from | `release/m19` |
| Sprint journal issue | TBD — PM Agent creates at EL approval |

**PM Agent sprint sub-branch cut command (run after EL approval):**
```bash
git checkout -b sprint/m19-g3 release/m19 && git push -u origin sprint/m19-g3
```

### 6.2 — File-conflict risk assessment

| File | Lane required | Trigger |
|---|---|---|
| `SESSION_STATE.md` | PM Agent coordination lane | Sprint exit cockpit update |
| `docs/process/near-miss-registry.md` | PM Agent coordination lane (PI Agent authors) | If NM identified |
| `docs/compliance/scan-registry.md` | PM Agent coordination lane | If compliance scan produced |
| `backend/app/simulation/banding_engine.py` | Sprint sub-branch | Primary implementation file for #1543/#1536 |
| `backend/app/schemas.py` | Sprint sub-branch | BandResult field additions for #1537 |
| `docs/adr/ADR-007-synthetic-data-framework.md` | Sprint sub-branch | Amendment Section 8 authored during sprint |
| `frontend/src/` (CI label component) | Sprint sub-branch | #1537 display contract update |

**CM pre-merge review gate (NM-084):**
> #1543 (posterior calibration) requires CM sign-off before auto-merge is set.
> Protocol: implementing agent activates CM → CM posts sign-off on issue #1543 →
> PI Agent posts gate comment on the #1543 PR confirming sign-off → only then auto-merge is set.
> Auto-merge must not be set on the #1543 PR before PI Agent gate comment is posted.

**No co-dependent fixture sequencing issue (NM-085 check):**
> G3 issues are not backtesting fixtures — they are engine modifications. NM-085 co-dependent
> fixture sequencing does not apply. Each issue is a standalone PR with no transient cross-test
> failure risk from co-dependent test shells.

### 6.3 — Infrastructure dependency declaration

- [x] No DS-owned file changes required

No changes to `.github/workflows/`, `.githooks/`, or `.gitignore` are anticipated.

#### 6.3a — New output paths declaration (NM-069)

- [x] No new output directories — all generated paths are already covered by `.gitignore`

*`backend/app/simulation/banding_engine.py` modifications do not introduce new output directories.*

### 6.4 — Cross-group dependency declaration

- [x] Yes — soft dependency declared below

**G4 #1529 coordination requirement:**
> G4 issue #1529 ('95% CI' label precision fix) must coordinate with G3 #1537 (BandResult
> visible fields) before either implementation PR opens. Specifically: the `band_method` field
> introduced in G3 #1537 determines what terminology G4 #1529 uses in the CI label.
>
> Merge ordering constraint: G3 #1537 implementation PR must be merged to `sprint/m19-g3`
> before G4 #1529 implementation PR opens. PM Agent notifies G4 team when G3 #1537 is merged.
>
> This is not a blocking dependency at sprint entry — G4 can begin sprint entry and cut its
> sprint branch in parallel with G3. G4 #1529 implementation PR does not open until G3 #1537
> terminology is settled (field names, band_method enum values confirmed in the accepted PR).

### 6.5 — Prior NM verification (NM-068 process improvement)

**NM verification sweep date:** 2026-07-02
**Sweep period:** Since G2B close

| NM entry | Process improvement required | Applied in this sprint? |
|---|---|---|
| NM-084 | CM sign-off on fixture/calibration PRs must precede auto-merge; PI Agent posts gate comment confirming sign-off before implementing agent sets auto-merge | Yes — §6.2 CM pre-merge review gate declared for #1543 |
| NM-085 | Sprint entry §6.2 must document co-dependent fixture sequencing risk; `backtesting` non-required statement required if applicable | Yes — §6.2 explicitly confirms NM-085 does not apply (G3 is not fixture work); confirmed in writing |
| NM-086 | QA Lead mock-helper verification is a blocking checklist item on intent authorship; E2E mock routes must match `api_contracts.yml` before implementation PR opens | Yes — #1537 has frontend surface; QA Lead must verify any E2E mock helpers match `api_contracts.yml` before intent document is approved. This is a blocking condition on the QA test authorship gate for #1537. |

---

## EL Approval Record

*EL reviews this entry document before any implementation PR opens. Approval is recorded here
or as a comment on the exit checklist issue #1535.*

**EL approval:** Pending

> {EL approval statement — to be filled at approval time}
> — @PublicEnemage ({date})
