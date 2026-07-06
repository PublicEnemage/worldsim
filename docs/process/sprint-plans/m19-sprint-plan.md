---
name: m19-sprint-plan
type: sprint-plan
milestone: M19 — Constraint Search and Empirical Calibration
status: EL-approved 2026-07-02; pre-wave and G1 sprint entries open
authored-by: PM Agent
authored-date: 2026-07-02
el-approved: 2026-07-02
consulted-agents:
  - Business Product Owner (Demo 8 value prioritization; constraint-floor capability as Act 1 anchor; backtesting scope)
  - Computation Engine Agent (Bayesian posterior dependency chain; backtesting fixture sequencing; constraint-floor search algorithm)
  - Frontend Architect (constraint-floor search UX in control plane column; BandResult field surfacing path; focal cohort floor validation)
  - DevSecOps Agent (new test coverage for backtesting fixtures; CI gate implications)
  - Architect (ADR-007 amendment scope; ADR prerequisites for constraint-floor search)
sop-reference: docs/process/sprint-planning-sop.md
---

# M19 Sprint Plan — Constraint Search and Empirical Calibration

**Status:** EL-approved 2026-07-02 (#1535 comment) — pre-wave and G1 sprint entries open
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

Full M19 issue audit completed 2026-07-02 (updated post-filing). Updated 2026-07-03 HORIZON sweep — 5 issues added (#1522, #1524, #1623, #1629, #1630). Updated 2026-07-04 HORIZON sweep — 5 issues added (#1709, #1710, #1711, #1712, #1713 — Demo 8 clearance and Act 2 verification). Updated 2026-07-04 G7 entry — 1 issue added (#1729 — NM-096 corrective action). All 33 M19 issues accounted for.

### Roadmap deliverables — linkage audit

| Roadmap deliverable | Issue | Group | Status |
|---|---|---|---|
| Mode 3 constraint-floor search capability | #1540 | G1 | ✅ Tracked |
| Headless battle-testing harness (Type A/B, configurable output) | #1546 | G2 Phase A | ✅ Tracked |
| SEN backtesting fixture (calibration + harness) | #1541 | G2 Phase B | ✅ Tracked |
| ZMB backtesting fixture (calibration + harness) | #1542 | G2 Phase B | ✅ Tracked |
| Greece 2010–15 primary surplus counter-factual Type B | #1547 | G2 Phase C | ✅ Tracked |
| Argentina 2001 peg-abandonment counter-factual Type B | #1548 | G2 Phase C | ✅ Tracked |
| Sri Lanka 2022–23 Coffin Corner Type A+B | #1549 | G2 Phase C | ✅ Tracked |
| Pakistan 2022–23 programme survival Type B | #1550 | G2 Phase C | ✅ Tracked |
| Turkey 2018–19 Backside of Power Curve Type B | #1551 | G2 Phase C | ✅ Tracked |
| Egypt 2016 devaluation/subsidy reform Type B | #1552 | G2 Phase C | ✅ Tracked |
| Ghana 2022–23 IMF programme Type A+B | #1554 | G2 Phase C | ✅ Tracked |
| Iceland 2008–11 orthodox vs heterodox Type A+B | #1553 | G2 Phase D (blocked: #1532) | ✅ Tracked; blocked by capital controls gap |
| ADR-007 Bayesian posterior layer — empirically grounded CI intervals | #1543 | G3 (blocked: G2 Phase B) | ✅ Tracked; SEN+ZMB gate sprint entry |
| PSP driver arc across programme window + in-viewport auditability panel | #1528 | G4 | ✅ Tracked (DEMO-165) |
| Demo 8 — live stakeholder session | #1544 | Milestone exit gate | ✅ Tracked |
| ELASTICITY_REGISTRY non-SSA calibration — CM Sprint A (Euro area/GRC) | #1623 | CM parallel track | ✅ Tracked — Sprint A M19 priority; B+C lower priority |
| Zone 1A ZMB y-axis tight-scoping (Demo 8 Act 2 display risk) | #1629 | G5 / Wave 3 | ✅ Tracked — added 2026-07-03 HORIZON sweep |
| Demo 8 narration / Mode 3 HD line alignment | #1630 | G5 / Wave 3 (after G4) | ✅ Tracked — EL: separate sprint entry after G4 |
| Zone 1 view model layer retrofit | #1522 | Wave 3+ | ✅ Tracked — EL-added to M19 |
| Zone 1A TrajectoryView interaction (pinch-zoom, thumbwheel, pan) | #1524 | Wave 3+ | ✅ Tracked — EL-added to M19 |
| NM-096 corrective: elasticity rows + NM-056 fix (Demo 8 pre-flight) | #1729 | G7 / Wave 5 | ✅ Tracked — BPO PROCEED 2026-07-04; sprint entry filed |

### Carry-forward and known gaps — linkage audit

| Issue | Title | Group | Priority |
|---|---|---|---|
| #1532 | Capital controls transmission gap (ExternalSectorModule+MacroeconomicModule channels absent) | Pre-wave / known gap | **Immediate — blocks Iceland (#1553)**; known-gap label; partial fix may unblock harness run |
| #1529 | '95% CI' label overstates precision on DistributionalComparisonSummary | G4 (coord: G3) | High — coordinates with Bayesian posterior delivery |
| #1456 | MDAAlertPanelZone1B: scenarioId crash | Pre-wave → G6 | High — crash risk; deferred past G1 but must clear before Demo 8 |
| #1536 | ADR-007 meaninglessness threshold | G3 (coord: Bayesian posterior) | High — coordinate with #1543 |
| #1537 | BandResult visible fields (is_pre_calibration, clipped_lower/upper) | G3 (coord: G3) | High — prerequisite for posterior transition UX |
| #1538 | Focal cohort floor validation (monitored_focal_cohorts schema) | Pre-wave → G6 | High — prerequisite gap; now required before Demo 8 |
| #1657 | NM-090/091: DemographicModule dead subscriptions + elasticity rows + ADR-020 update | G6 | High — CM cert required before impl PR opens |
| #1709 | FOUND state: tolerance band (±0.01) not displayed | G6 | Immediate — Demo 8 Act 1 blocker (Customer Agent L3 on #1540) |
| #1710 | AC-12: resolve `__structural_absence__` placeholder | G6 | Immediate — Demo 8 Act 1 blocker (Customer Agent L3 on #1540) |
| #1711 | Demo 8 Act 2 verification: GRC AC-1 live harness run | Demo 8 Act 2 verification | Near-term — no code changes; DATABASE_URL prerequisite |
| #1712 | Demo 8 Act 2 verification: ARG AC-1 live harness run | Demo 8 Act 2 verification | Near-term — no code changes; DATABASE_URL prerequisite |
| #1713 | Demo 8 Act 2 verification: PAK AC-1 live harness run | Demo 8 Act 2 verification | Near-term — no code changes; DATABASE_URL prerequisite |

### Full issue-to-group mapping

| Issue | Title | Group | Wave | Priority |
|---|---|---|---|---|
| #1535 | M19 Exit Checklist | — (gate) | — | Milestone exit gate |
| #1544 | Demo 8 — live stakeholder session | — (exit gate) | Exit | Primary deliverable |
| #1532 | Capital controls transmission gap | Pre-wave / known gap | Pre-wave | **Immediate — blocks Iceland** |
| #1456 | MDAAlertPanelZone1B: scenarioId crash | G6 | Wave 4 | **Immediate — crash risk** |
| #1538 | Focal cohort floor validation | G6 | Wave 4 | **Immediate — Demo 8 prerequisite** |
| #1540 | Mode 3 constraint-floor search | G1 | Wave 1 | High — Demo 8 Act 1 |
| #1546 | Headless battle-testing harness | G2 Phase A | Wave 1 (parallel to G1) | High — all scenario runs depend on this |
| #1541 | SEN backtesting fixture | G2 Phase B | Wave 1 (after G2A) | High — Bayesian gate + harness calibration |
| #1542 | ZMB backtesting fixture | G2 Phase B | Wave 1 (after G2A) | High — Bayesian gate + harness calibration |
| #1547 | Greece 2010–15 counter-factual Type B | G2 Phase C | Wave 1–2 (after G2A) | Medium — extends existing fixture |
| #1548 | Argentina 2001 counter-factual Type B | G2 Phase C | Wave 1–2 (after G2A) | Medium — extends existing fixture |
| #1549 | Sri Lanka 2022–23 Type A+B | G2 Phase C | Wave 1–2 (after G2A) | Medium |
| #1550 | Pakistan 2022–23 Type B | G2 Phase C | Wave 1–2 (after G2A) | Medium |
| #1551 | Turkey 2018–19 Type B | G2 Phase C | Wave 1–2 (after G2A) | Medium |
| #1552 | Egypt 2016 Type B | G2 Phase C | Wave 1–2 (after G2A) | Medium |
| #1554 | Ghana 2022–23 Type A+B | G2 Phase C | Wave 1–2 (after G2A) | Medium |
| #1553 | Iceland 2008–11 Type A+B | G2 Phase D | Wave 2 (blocked: #1532) | Medium — pre-calibration structural test |
| #1543 | ADR-007 Bayesian posterior layer | G3 | Wave 2 (blocked: G2 Phase B) | High — Demo 8 Act 2 CI grounding |
| #1536 | ADR-007 meaninglessness threshold | G3 | Wave 2 (coord: #1543) | High — same file area as Bayesian posterior |
| #1537 | BandResult visible fields | G3 | Wave 2 (coord: #1543) | High — prerequisite for posterior UX |
| #1528 | PSP driver arc + auditability panel | G4 | Wave 2–3 | High — DEMO-165 |
| #1529 | '95% CI' label precision fix | G4 | Wave 2–3 (coord: G3) | High — coordinate with G3 CI label work |
| #1623 | ELASTICITY_REGISTRY non-SSA calibration gaps (CM Sprint A/B/C) | CM parallel track | Wave 2–3 | High — Sprint A (GRC/Euro area) M19 priority; Sprints B+C lower priority |
| #1629 | Zone 1A ZMB y-axis not tight-scoped — curves collapse | G5 / Wave 3 | Wave 3 | High — Demo 8 Act 2 display fidelity; `computeYDomain` fix |
| #1630 | Demo 8 narration: HD line implied but not rendered | G5 / Wave 3 | Wave 3 (after G4) | High — Demo 8 Act 1 risk; separate sprint entry G5 per EL direction |
| #1522 | View model layer retrofit — Zone 1 composition extraction | Wave 3+ | Wave 3+ | Medium — EL-added to M19; defers to M20 if Wave 3 capacity reached |
| #1524 | Zone 1A TrajectoryView: pinch-zoom, thumbwheel, pan | Wave 3+ | Wave 3+ | Medium — EL-added to M19; defers to M20 if Wave 3 capacity reached |
| #1657 | NM-090/091: DemographicModule dead subscriptions + elasticity rows + ADR-020 update | G6 | Wave 4 | High — CM cert required before impl PR |
| #1709 | FOUND state: tolerance band (±0.01) not displayed | G6 | Wave 4 | High — Demo 8 Act 1 blocker |
| #1710 | AC-12: resolve `__structural_absence__` placeholder | G6 | Wave 4 | High — Demo 8 Act 1 blocker |
| #1711 | Demo 8 Act 2 verification: GRC AC-1 live harness run | Demo 8 Act 2 verification | Wave 4 | High — Demo 8 Act 2 condition (DATABASE_URL only) |
| #1712 | Demo 8 Act 2 verification: ARG AC-1 live harness run | Demo 8 Act 2 verification | Wave 4 | High — Demo 8 Act 2 condition (DATABASE_URL only) |
| #1713 | Demo 8 Act 2 verification: PAK AC-1 live harness run | Demo 8 Act 2 verification | Wave 4 | High — Demo 8 Act 2 condition (DATABASE_URL only) |
| #1729 | fix(g6): missing elasticity rows for imf_program_acceptance + emergency_declaration; NM-056 | G7 | Wave 5 | **Immediate — NM-096 corrective; Demo 8 pre-flight; silent zero-delta on live channels** |

### ADR backlog review

| ADR area | Status | M19 action |
|---|---|---|
| ADR-007 (CI bands) | CURRENT; amendment required for Bayesian posterior layer | PM Agent to verify backlog entry before G3 authorship begins |
| ADR-019 (control plane column) | CURRENT; Valid Until: M19 entry if Mode 3 scope expands | Architecture review required before G1 sprint entry: does constraint-floor search expand the control plane scope? If yes, ADR-019 amendment required. |
| New ADR for constraint-floor search algorithm | Not yet assigned | Architect to confirm whether constraint-floor search warrants its own ADR (ADR-020?) or an ADR-019 amendment |

---

## Wave Plan

### Pre-wave (before G1 sprint entry opens)

**Pre-wave objective:** Close crash risk (#1456), schema gap (#1538), and assess capital controls gap (#1532) before sprint group work begins.

| Task | Issue | Implementing agent | Notes |
|---|---|---|---|
| Close MDAAlertPanelZone1B scenarioId crash | #1456 | Frontend Implementation Agent | Targeted guard; no sprint entry required (scope < one PR) |
| Focal cohort floor Pydantic validation | #1538 | Computation Engine Agent | `list[dict[str, Any]]` → `list[FocalCohortConfig]`; prerequisite for #1540 |
| Capital controls transmission — scope and unblock Iceland | #1532 | Computation Engine Agent | Known gap; determine minimum fix to unblock Iceland harness run (#1553); full fix may extend into Wave 2 |
| ADR review: does constraint-floor search require ADR-020 or ADR-019 amendment? | — | Architect | Must be on record before G1 sprint entry is filed |

### Wave 1 — G1 + G2 Phase A + G2 Phase B (parallel)

**G1: Mode 3 Constraint-Floor Search (#1540)**
- Primary file areas: `frontend/src/components/ControlPlaneColumn.tsx`, `backend/app/api/scenarios.py`, `backend/app/simulation/`
- Sprint branch: `sprint/m19-g1`
- Blocked by: Pre-wave ADR decision, #1538 (focal cohort floor validation)
- Key design question: Does the constraint-floor search run in the backend (endpoint returns boundary value) or in the frontend (multiple API calls until boundary found)? Architecture decision required at sprint entry.

**G2 Phase A: Headless Battle-Testing Harness (#1546)**
- Primary file areas: `backend/app/simulation/`, new `backend/scripts/` or `backend/app/harness/` module
- Sprint branch: `sprint/m19-g2` (harness infrastructure first; scenario runs are PRs within same branch)
- Parallel to G1 — no shared file areas with G1
- Deliverable: Harness that accepts a scenario config, runs it headlessly, and emits ASCII/CSV/JSON/Markdown output per Type A (replay) or Type B (counter-factual) classification

**G2 Phase B: SEN + ZMB Calibration Fixtures (#1541, #1542)**
- On same `sprint/m19-g2` branch, after G2 Phase A harness ships
- SEN and ZMB are both harness runs AND CI build-gate fixtures — they run in CI and contribute calibration data to G3 Bayesian posterior
- Key constraint: Chief Methodologist sign-off on fidelity thresholds before fixtures enter CI. DIRECTION_ONLY acceptable for M19 if MAGNITUDE data insufficient.

### Wave 1–2 — G2 Phase C + D (after G2 Phase A harness ready)

**G2 Phase C: Battle-Testing Scenario Runs (#1547, #1548, #1549, #1550, #1551, #1552, #1554)**
- Seven country scenarios run through the harness; results reviewed but not CI-gated (these are battle-testing runs, not calibration fixtures)
- Can parallelize across scenarios once harness is ready — each scenario is a separate PR
- Greece (#1547) and Argentina (#1548) extend existing fixtures — lower data risk
- Sri Lanka (#1549), Pakistan (#1550), Turkey (#1551), Egypt (#1552), Ghana (#1554) are new cases — Chief Methodologist advises on data sourcing before sprint entries filed

**G2 Phase D: Iceland (#1553, blocked by #1532)**
- Unblocked when #1532 capital controls transmission is sufficiently fixed
- Iceland is designated as the pre-calibration structural test — runs with `is_pre_calibration=True` explicitly and documents what the structural model gets right vs wrong on an orthodox/heterodox counterfactual
- If #1532 is not resolved in time for M19, Iceland defers to M20 with documented rationale on #1553

### Wave 2 — G3 + G4 (after G2 Phase B complete)

**G3: Bayesian Posterior + Band Visibility (#1543, #1536, #1537)**
- Blocked by: G2 (SEN + ZMB calibration data required)
- Primary file areas: `backend/app/simulation/banding_engine.py`, `backend/app/schemas.py`, `frontend/src/components/TrajectoryView.tsx`
- Note: #1536 (meaninglessness threshold) and #1537 (BandResult visible fields) share `banding_engine.py` with #1543 — file these in the same sprint group to avoid merge conflicts and coordinate the design
- ADR-007 amendment must be filed and accepted before implementation begins

**G4: PSP Driver Arc + CI Label Polish (#1528, #1529)**
- Primary file areas: `frontend/src/components/FourFrameworkZone1D.tsx`, `frontend/src/components/TrajectoryView.tsx` (CI label)
- Note: #1529 (CI label) should coordinate with G3 — if G3 changes the label architecture (e.g., `is_pre_calibration` qualifier), G4 must be consistent
- Can begin in parallel with G3 once G3 file areas are confirmed non-overlapping

### Wave 3 — G5 + Demo 8 preparation

**G5: Demo 8 display and narration quality (#1629, #1630)**
- Sprint entry files after G4 exits — EL confirmed 2026-07-03
- #1629 (ZMB Zone 1A y-axis fix): `CompositeChartSVG.computeYDomain` must tight-scope to data range; three ZMB PHR scenario curves collapse visually when spread ≤ 0.05. Fix is self-contained but affects Demo 8 Act 2 legibility.
- #1630 (narration / HD line alignment): Act 1 narration (`demo-narrated.spec.ts` ~line 892) implies a separately visible HD line in Zone 1A that does not exist in Mode 3 (CompositeChartSVG renders single composite). EL decision required at sprint entry: (a) narration text correction only (fast path), or (b) add per-framework lines to Zone 1A in Mode 3 (larger scope, requires UX panel review).
- Sprint branch: `sprint/m19-g5`
- Blocked by: G4 exit (narration fix must be consistent with G4 CI label changes)

**CM parallel track: ELASTICITY_REGISTRY non-SSA calibration (#1623)**
- CM Sprint A (Euro area — GRC priority): Runs concurrently with G4/G5; does not share file areas with G-series sprints
- CM Sprint B (Latin America — ARG priority): After Sprint A exit gate
- CM Sprint C (South Asia — PAK/LKA priority): After Sprint B, may defer to M20
- Sprint branch(es): cut from `release/m19` per CM/CE protocol; CM sign-off required at sprint entry per NM-084 gate

**Wave 3+ — after G5 (#1522, #1524)**
- #1522 (view model layer retrofit) and #1524 (Zone 1A interaction layer) are M19-milestoned at EL direction but are capacity-conditional: if Demo 8 preparation leaves insufficient Wave 3 capacity, both defer to M20 with documented rationale on each issue.
- Sprint entries file after G5 exit; group designation TBD at that point.

### Wave 4 — G6: Demo 8 clearance sprint + Act 2 verification

**G6: Demo 8 Act 1 clearance (#1456, #1538, #1709, #1710)**

- Primary objective: clear all Demo 8 Act 1 blockers, pre-wave crash risk, and NM-090/091 dead-subscription gap before Demo 8 rehearsal
- #1456 (crash fix): `MDAAlertPanel` Zone1B `scenarioId` guard — targeted null-check
- #1538 (focal cohort floor validation): `monitored_focal_cohorts` Pydantic validation — `list[dict[str, Any]]` → `list[FocalCohortConfig]`; G1 prerequisite that remained unimplemented; required before Demo 8 correctness claims hold
- #1709 (tolerance band): FOUND state must render `±tolerance` visually distinct from boundary value in the control plane column; Customer Agent L3 condition from #1540 exit
- #1710 (AC-12): identify real structural-absence indicator key; rewrite AC-12 without the `__structural_absence__` placeholder; CI skip on AC-12 must be removed
- #1657 (NM-090/091): fix 2 dead strings in `DemographicModule._SUBSCRIBED_EVENTS`; add elasticity rows for both newly-wired events; reconcile ADR-020 transmission table against actual `EmergencyInstrument` enum; **CM consultation required before elasticity values are assigned — CM posts cert on #1657 before #1657 implementation PR opens** (NM-084 gate); ADR-020 update required (transmission table correction, not a new ADR)
- Sprint branch: `sprint/m19-g6`
- No new ADR required; ADR-020 update in scope for #1657
- Blocked by: none (Wave 3 fully integrated); #1657 implementation PR additionally gated by CM cert

**Demo 8 Act 2 verification (#1711, #1712, #1713)**

- Not a code-change sprint group — DATABASE_URL harness runs only
- Three live harness runs verifying CM Sprint A/B/C MAGNITUDE forward conditions (GRC, ARG, PAK)
- Can run in parallel once DATABASE_URL is configured; each fixture is independent
- If any bound fails: CM Agent consulted; corrective calibration action documented before Demo 8 proceeds
- Runs in parallel with G6 (no file area overlap)

### Wave 5 — G7: NM-096 corrective action (Demo 8 pre-flight)

**G7: Elasticity rows + NM-056 fix (#1729)**

- Root: NM-096 (2026-07-04) — PR #1722 (G6) fixed dead subscription strings but omitted
  elasticity rows prescribed by NM-090/091; G6 exit reported 9/9 GREEN when state was 7 PASS + 2 SKIP
- Sprint entry filed: `docs/process/sprint-plans/m19-g7-sprint-entry.md` (2026-07-04)
- BPO verdict: PROCEED — HIGH priority; Demo 8 pre-flight; silent zero-delta on live channels
- CM cert: pre-cleared (#1657 comment, 2026-07-04); NM-084 gate satisfied
- Files: `backend/app/simulation/modules/demographic/elasticities.py` (4 rows); `backend/tests/test_m19_g6_demographic_subscriptions.py` (NM-056 fix lines 231, 289)
- Sprint branch: `sprint/m19-g7` (cut from `release/m19` after EL approval)
- No new ADR required (ADR-020 accepted; bug fix only)

**Demo 8 preparation (after G7 + Act 2 verification complete)**
- Demo 8 internal review and IR review
- Walkthrough updates for Demo 8 narrative (constraint-floor Act 1, calibrated CI Act 2 with empirical grounding)
- Stakeholder session (#1544)
- G-remediation group (if Demo 8 internal review finds CRITICAL/HIGH issues)

---

## Sequencing constraints

```
#1456 (crash fix)     ──┐
#1538 (floor schema)  ──┤──► G1: #1540 (constraint-floor search)
ADR decision          ──┘

#1546 (harness) ──► G2B: #1541 (SEN) ──┐
                    G2B: #1542 (ZMB) ──┤──► G3: #1543 (Bayesian posterior) ──► Demo 8 Act 2 CI
                                        └──► G3: #1536 (meaninglessness)         (coordinated)
                                             G3: #1537 (BandResult UX)

#1546 (harness) ──► G2C: #1547/#1548/#1549/#1550/#1551/#1552/#1554 (parallel runs)

#1532 (capital controls) ──► G2D: #1553 (Iceland)

G3 CI label design ──► G4: #1529 (label precision) — coordinate, not block

G4 exit ──► G5: #1629 (ZMB y-axis fix) + #1630 (narration/HD alignment) ──► Demo 8 prep

#1623 (CM Sprint A/B/C — parallel track; no file area overlap with G-series)

G5 exit ──► Wave 3+: #1522 (view model retrofit), #1524 (interaction layer) — capacity-conditional

G5 + #1523 exits ──► G6: #1456 + #1538 + #1709 + #1710 ──► Demo 8 Act 1 clearance

CM Sprint A/B/C exits ──► #1711 (GRC) + #1712 (ARG) + #1713 (PAK) ──► Demo 8 Act 2 clearance

G6 + Act 2 verification ──► Demo 8 internal review ──► #1544 (live session)

NM-096 corrective ──► G7: #1729 (elasticity rows + NM-056) ──► Demo 8 pre-flight clearance
```

---

## Known risks

| Risk | Likelihood | Mitigation |
|---|---|---|
| Constraint-floor search is computationally expensive for Mode 3 real-time use | Medium | Architecture decision at sprint entry: backend binary search (O(log n) API calls) vs frontend scan (O(n)). Backend binary search preferred. |
| SEN/ZMB data availability at required confidence tier | Medium | Chief Methodologist consults at G2B sprint entry; DIRECTION_ONLY acceptable if MAGNITUDE data insufficient |
| ADR-007 Bayesian posterior too thin on two cases | Low | Chief Methodologist confirms whether Greece+Argentina historical cases can serve as informative priors supplementing SEN+ZMB |
| G3 `banding_engine.py` conflicts across #1536, #1537, #1543 | High | Single sprint group G3, one `sprint/m19-g3` branch, coordinated PRs |
| #1532 capital controls gap not fixable in M19 — Iceland defers | Medium | Iceland (#1553) is lower priority than core calibration deliverables; deferral to M20 is acceptable if fix scope is large |
| G2 Phase C new-country scenarios have thin data | Medium | Chief Methodologist data assessment required at each Phase C sprint entry; DIRECTION_ONLY acceptable; scenario may use synthetic T3–T4 data if primary sources unavailable |

---

## Insights log review

**At sprint plan filing (2026-07-02):** 0 open entries requiring action. The three Socratic TEST session gaps promoted to GitHub issues (#1536, #1537, #1538).

**HORIZON sweep (2026-07-03):** 3 open entries reviewed and dispositioned:
- 2026-06-30: ZMB Zone 1A curve collapse → promoted → #1629 (added to M19; G5 Wave 3)
- 2026-06-30: Mode 3 HD narration mismatch → promoted → #1630 (added to M19; G5 Wave 3 after G4 per EL direction)
- 2026-07-02: Headless battle-testing initiative → resolved (all 10 issues filed; ADR-020 accepted; G2D implementation unblocked)

**HORIZON sweep (2026-07-04, sweep 1):** 0 open insights log entries. 5 new issues filed from Demo 8 open conditions:
- Customer Agent L3 condition 1 on #1540 → #1709 (FOUND state tolerance band visibility; G6 Wave 4)
- Customer Agent L3 condition 2 on #1540 → #1710 (AC-12 structural absence placeholder; G6 Wave 4)
- CM Sprint A exit §4 forward condition → #1711 (GRC AC-1 live harness run; Demo 8 Act 2 verification)
- CM Sprint B exit §4 forward condition → #1712 (ARG AC-1 live harness run; Demo 8 Act 2 verification)
- CM Sprint C exit §4 forward condition → #1713 (PAK AC-1 live harness run; Demo 8 Act 2 verification)
Wave 4 G6 sprint definition added. Total M19 issues: 32.

Additionally: #1522 and #1524 added to M19 at EL direction; #1623 (ELASTICITY_REGISTRY calibration gap) filed and added to M19. Total M19 issue count: 27.

**HORIZON sweep (2026-07-04, sweep 2):** 0 open insights log entries. 15 stale GitHub issues closed (PRs merged but no "Fixes #" keywords used): G5 deliverables #1629, #1630, #1522, #1524; fixes #1647, #1632; NM codification batch #1650–#1656; G5 sprint journal #1660; M18 demo prep #1445. All G1–G6 + CM-A/B/C sprint group work is integrated into release/m19. Remaining open: #1711, #1712, #1713 (Demo 8 Act 2 verification — DATABASE_URL prerequisite); #1544 (Demo 8 live session — milestone exit gate); #1535 (M19 Exit Checklist). Next: Demo 8 internal review → IR review → live session (#1544).
