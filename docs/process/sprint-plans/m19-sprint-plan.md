---
name: m19-sprint-plan
type: sprint-plan
milestone: M19 — Constraint Search and Empirical Calibration
status: filed 2026-07-02; EL approval pending
authored-by: PM Agent
authored-date: 2026-07-02
el-approved: pending
consulted-agents:
  - Business Product Owner (Demo 8 value prioritization; constraint-floor capability as Act 1 anchor; backtesting scope)
  - Computation Engine Agent (Bayesian posterior dependency chain; backtesting fixture sequencing; constraint-floor search algorithm)
  - Frontend Architect (constraint-floor search UX in control plane column; BandResult field surfacing path; focal cohort floor validation)
  - DevSecOps Agent (new test coverage for backtesting fixtures; CI gate implications)
  - Architect (ADR-007 amendment scope; ADR prerequisites for constraint-floor search)
sop-reference: docs/process/sprint-planning-sop.md
---

# M19 Sprint Plan — Constraint Search and Empirical Calibration

**Status:** Filed 2026-07-02 — EL approval required before G1 sprint entries open
**Release branch:** `release/m19` — cut from `main` 2026-07-02 at commit 1bf1ecc (after doc corrections PR #1539)
**Exit checklist issue:** #1535 (M19 Exit Checklist — blocks milestone closure)
**GitHub Milestone:** #21

**Primary objective:** Demo 8 — the constraint-floor capability and empirically calibrated confidence intervals. Two acts: Act 1 (Zambia or Senegal, Mode 3 constraint-floor search) asks "what is the minimum fiscal multiplier that avoids the human cost floor?" — the instrument finds the boundary rather than requiring one-at-a-time search. Act 2 (Zambia three-scenario) shows the +342K distributional differential with CI bounds now grounded in empirical backtesting (Bayesian posterior layer), not just the structural schedule.

**M19 exit gate:** PI Agent exit gate confirmation, with BPO acceptance for all user-facing deliverables. Demo 8 live session (#1544) is the milestone north star — it is the last mandatory deliverable before M19 closes. #1535 closes last.

**M19 thesis:** M18 proved the instrument is a counter-proposal tool. M19 makes it a search instrument — not just "is this configuration safe?" but "what configurations are safe?" — and gives the confidence intervals their first empirical grounding. The ministry analyst enters the negotiating session with a specific, defensible boundary value and CI bounds that have been tested against real fiscal outcomes.

---

## Kickoff Prerequisites (Status at Sprint Plan Filing)

| Step | Status | Notes |
|---|---|---|
| 1. EL merges `release/m18` → `main` (admin bypass) | ✅ DONE 2026-07-02 | PR #1534 merged; `main` at 1bf1ecc after doc corrections |
| 2. PM Agent authors `m19-sprint-plan.md` | ✅ THIS DOCUMENT | Filed 2026-07-02 |
| 3. EL approves sprint plan | ⏳ PENDING | EL approval required before G1 sprint entries open |
| 4. `release/m19` cut from `main` | ✅ DONE 2026-07-02 | Branch created via GitHub API at commit 1bf1ecc |
| 5. CI trigger verified | ✅ CLEAR | `.github/workflows/ci.yml` covers `release/m*` and `sprint/m*` |
| 6. #1535 named M19 Exit Checklist | ✅ DONE | Auto-created by GitHub; title updated 2026-07-02 |
| 7. Issue audit complete | ✅ DONE | Full HORIZON sweep below |

---

## HORIZON Scope-Completeness Check

Full M19 issue audit completed 2026-07-02. All 12 M19 issues accounted for.

### Roadmap deliverables — linkage audit

| Roadmap deliverable | Issue | Group | Status |
|---|---|---|---|
| Mode 3 constraint-floor search capability | #1540 | G1 | ✅ Tracked |
| Senegal (SEN) backtesting fixture | #1541 | G2 | ✅ Tracked |
| Zambia (ZMB) backtesting fixture | #1542 | G2 | ✅ Tracked |
| ADR-007 Bayesian posterior layer — empirically grounded CI intervals | #1543 | G3 (blocked: G2) | ✅ Tracked; backtesting fixtures gate sprint entry |
| PSP driver arc across programme window + in-viewport auditability panel | #1528 | G4 | ✅ Tracked (DEMO-165) |
| Demo 8 — live stakeholder session | #1544 | Milestone exit gate | ✅ Tracked |

### Carry-forward from M18 — linkage audit

| Issue | Title | Group | Priority |
|---|---|---|---|
| #1529 | '95% CI' label overstates precision on DistributionalComparisonSummary | G4 (coord: G3) | High — label precision coordinates with Bayesian posterior delivery |
| #1456 | MDAAlertPanelZone1B: scenarioId unguarded at line 1121 | G1 pre-work | High — crash risk; address before G1 begins |
| #1536 | ADR-007 meaninglessness threshold | G3 (coord: Bayesian posterior) | High — coordinate with #1543 |
| #1537 | BandResult visible fields (is_pre_calibration, clipped_lower/upper) | G3 (coord: G3) | High — prerequisite for posterior transition UX |
| #1538 | Focal cohort floor validation (monitored_focal_cohorts schema) | G1 pre-work | High — prerequisite for constraint-floor search (#1540) |

### Full issue-to-group mapping

| Issue | Title | Group | Wave | Priority |
|---|---|---|---|---|
| #1535 | M19 Exit Checklist | — (gate) | — | Milestone exit gate |
| #1544 | Demo 8 — live stakeholder session | — (exit gate) | Exit | Primary deliverable |
| #1456 | MDAAlertPanelZone1B: scenarioId crash | G1 pre-work | Pre-wave | **Immediate — crash risk** |
| #1538 | Focal cohort floor validation | G1 pre-work | Pre-wave | **Immediate — constraint-floor prerequisite** |
| #1540 | Mode 3 constraint-floor search | G1 | Wave 1 | High — Demo 8 Act 1 |
| #1541 | SEN backtesting fixture | G2 | Wave 1 (parallel to G1) | High — Bayesian gate |
| #1542 | ZMB backtesting fixture | G2 | Wave 1 (parallel to G1) | High — Bayesian gate |
| #1543 | ADR-007 Bayesian posterior layer | G3 | Wave 2 (blocked: G2) | High — Demo 8 Act 2 CI grounding |
| #1536 | ADR-007 meaninglessness threshold | G3 | Wave 2 (coord: #1543) | High — same file area as Bayesian posterior |
| #1537 | BandResult visible fields | G3 | Wave 2 (coord: #1543) | High — prerequisite for posterior UX |
| #1528 | PSP driver arc + auditability panel | G4 | Wave 2–3 | High — DEMO-165 |
| #1529 | '95% CI' label precision fix | G4 | Wave 2–3 (coord: G3) | High — coordinate with G3 CI label work |

### ADR backlog review

| ADR area | Status | M19 action |
|---|---|---|
| ADR-007 (CI bands) | CURRENT; amendment required for Bayesian posterior layer | PM Agent to verify backlog entry before G3 authorship begins |
| ADR-019 (control plane column) | CURRENT; Valid Until: M19 entry if Mode 3 scope expands | Architecture review required before G1 sprint entry: does constraint-floor search expand the control plane scope? If yes, ADR-019 amendment required. |
| New ADR for constraint-floor search algorithm | Not yet assigned | Architect to confirm whether constraint-floor search warrants its own ADR (ADR-020?) or an ADR-019 amendment |

---

## Wave Plan

### Pre-wave (before G1 sprint entry opens)

**Pre-wave objective:** Close crash risk (#1456) and schema gap (#1538) before sprint group work begins. Both are small, targeted fixes that gate downstream work and carry safety risk if deferred.

| Task | Issue | Implementing agent | Notes |
|---|---|---|---|
| Close MDAAlertPanelZone1B scenarioId crash | #1456 | Frontend Implementation Agent | Targeted guard; no sprint entry required (scope < one PR) |
| Focal cohort floor Pydantic validation | #1538 | Computation Engine Agent | `list[dict[str, Any]]` → `list[FocalCohortConfig]`; prerequisite for #1540 |
| ADR review: does constraint-floor search require ADR-020 or ADR-019 amendment? | — | Architect | Must be on record before G1 sprint entry is filed |

### Wave 1 — G1 + G2 (parallel)

**G1: Mode 3 Constraint-Floor Search (#1540)**
- Primary file areas: `frontend/src/components/ControlPlaneColumn.tsx`, `backend/app/api/scenarios.py`, `backend/app/simulation/`
- Sprint branch: `sprint/m19-g1`
- Blocked by: Pre-wave ADR decision, #1538 (focal cohort floor validation)
- Key design question: Does the constraint-floor search run in the backend (endpoint returns boundary value) or in the frontend (multiple API calls until boundary found)? Architecture decision required at sprint entry.

**G2: SEN + ZMB Backtesting Fixtures (#1541, #1542)**
- Primary file areas: `backend/tests/`, `backend/app/db/seed/`, source registry
- Sprint branch: `sprint/m19-g2`
- Parallel to G1 — no shared file areas
- Key constraint: Fidelity thresholds must be approved by Chief Methodologist before fixtures enter CI as build gates. Fixtures run as DIRECTION_ONLY until CM sign-off on MAGNITUDE thresholds.

### Wave 2 — G3 + G4 (after G2 complete)

**G3: Bayesian Posterior + Band Visibility (#1543, #1536, #1537)**
- Blocked by: G2 (SEN + ZMB calibration data required)
- Primary file areas: `backend/app/simulation/banding_engine.py`, `backend/app/schemas.py`, `frontend/src/components/TrajectoryView.tsx`
- Note: #1536 (meaninglessness threshold) and #1537 (BandResult visible fields) share `banding_engine.py` with #1543 — file these in the same sprint group to avoid merge conflicts and coordinate the design
- ADR-007 amendment must be filed and accepted before implementation begins

**G4: PSP Driver Arc + CI Label Polish (#1528, #1529)**
- Primary file areas: `frontend/src/components/FourFrameworkZone1D.tsx`, `frontend/src/components/TrajectoryView.tsx` (CI label)
- Note: #1529 (CI label) should coordinate with G3 — if G3 changes the label architecture (e.g., `is_pre_calibration` qualifier), G4 must be consistent
- Can begin in parallel with G3 once G3 file areas are confirmed non-overlapping

### Wave 3 — Demo 8 preparation

- Walkthrough updates for Demo 8 narrative (constraint-floor Act 1, calibrated CI Act 2)
- Internal review, IR review, stakeholder session (#1544)
- G5 remediation group (if Demo 8 internal review finds CRITICAL/HIGH issues)

---

## Sequencing constraints

```
#1456 (crash fix)     ──┐
#1538 (floor schema)  ──┤──► G1: #1540 (constraint-floor search)
ADR decision          ──┘

#1541 (SEN)  ──┐
#1542 (ZMB)  ──┤──► G3: #1543 (Bayesian posterior) ──► Demo 8 Act 2 CI
               └──► G3: #1536 (meaninglessness threshold)    (coordinated)
                    G3: #1537 (BandResult UX)

G3 CI label design ──► G4: #1529 (label precision) — coordinate, not block
```

---

## Known risks

| Risk | Likelihood | Mitigation |
|---|---|---|
| Constraint-floor search algorithm is computationally expensive for Mode 3 real-time use | Medium | Architecture decision at sprint entry: backend binary search (bounded API calls) vs frontend scan. Backend binary search preferred — O(log n) calls vs O(n). |
| SEN/ZMB data availability at required confidence tier | Medium | Chief Methodologist consults at G2 sprint entry; DIRECTION_ONLY thresholds acceptable for M19 if MAGNITUDE data is insufficient |
| ADR-007 Bayesian posterior requires more calibration data than SEN + ZMB provide | Low | Two cases is a thin posterior. Chief Methodologist must confirm whether two cases are sufficient for M19 or whether additional cases (Greece, Argentina) are used as informative priors. |
| G3 `banding_engine.py` changes conflict across #1536, #1537, #1543 | High | Address in one sprint group (G3) — not split across multiple groups. File a single sprint branch `sprint/m19-g3` and deliver all three in coordinated PRs. |

---

## Insights log review (2026-07-02)

Open entries reviewed at sprint plan filing: 0 open entries requiring action. The three Socratic TEST session gaps have been promoted to GitHub issues (#1536, #1537, #1538 — all filed 2026-07-02). No entries remain at `open` status requiring M19 disposition at this time.
