---
name: m20-sprint-g2-entry
type: sprint-entry
milestone: M20 — Analytical Evidence Portfolio and Demo 9
sprint-group: G2
status: Filed
authored-by: PM Agent
authored-date: 2026-07-07
el-approved: true
release-branch: release/m20
sop-reference: docs/process/sprint-planning-sop.md
---

# Sprint Entry — M20 G2 — AEP SSA-LIC and LATAM-EM Entries

**Status:** EL-approved — implementation authorised  
**Date authored:** 2026-07-07  
**Release branch:** `release/m20`  
**Sprint plan:** `docs/process/sprint-plans/m20-sprint-plan.md`

*Authority: `docs/process/sprint-planning-sop.md §Sprint Entry Gate` (Phase C output).*

---

## Section 1 — Sprint Identification

| Field | Value |
|---|---|
| Milestone | M20 — Analytical Evidence Portfolio and Demo 9 |
| GitHub Milestone | #22 |
| Sprint number | G2 |
| Release branch | `release/m20` |
| Sprint plan document | `docs/process/sprint-plans/m20-sprint-plan.md` |
| Exit checklist issue | #1773 |
| Sprint groups in scope | G2 |
| Wave coordination tier | Standard — documentation sprint; no engineering dependencies |
| Concurrent groups at entry | 0 — G4 not yet started |
| Cross-group dependencies | None — G2 AEA documentation is independent of G4 engineering |

---

## Section 2 — Entry Invariants Checklist

### 2.1 — Structural gates

- [x] **Release branch exists:** `release/m20` — confirmed; G1 integration PR #1794 merged 2026-07-07
- [x] **CI trigger verified:** `.github/workflows/ci.yml` `pull_request: branches` includes `release/m*`
- [x] **Sprint plan EL-approved:** `docs/process/sprint-plans/m20-sprint-plan.md` EL-approved in session 2026-07-07

### 2.2 — ADR prerequisite gate

**N/A — AEA documentation sprint.** G2 deliverables are AEP evidence entries authored in `docs/evidence/`. No new ADRs are required. The governing calibration documents (CM-B for LATAM-EM, CM-D for ARG Kirchner, Fosu 2011 for SSA-LIC) are already accepted and on `release/m20`.

| Group | Required ADR | ADR status | Gate |
|---|---|---|---|
| G2 | None | N/A | CLEAR |

### 2.3 — Intent document gate

**Documentation sprint — AEP entries are authorship artifacts.** The coverage audit (`docs/evidence/coverage-audit.md`) serves as the functional intent specification: it identifies which scenarios to run, calibration families, fidelity ceilings, and what each entry should document.

| Deliverable | Coverage audit reference | Intent specification | Gate |
|---|---|---|---|
| AEP-004-ZMB-2005.md | `§Family 1 (c) SSA-2` | coverage-audit.md §Family 1 + analytical-framework.md §1 Family 1 | CLEAR |
| AEP-005-SEN-2000.md | `§Family 1 (c) SSA-1` | coverage-audit.md §Family 1 + analytical-framework.md §1 Family 1 | CLEAR |
| AEP-006-GHA-2022.md | `§Family 1 (c) SSA-3` | coverage-audit.md §Family 1 + analytical-framework.md §1 Family 1 | CLEAR |
| AEP-007-ARG-2001.md | `§Family 3 (c) LAT-1` | coverage-audit.md §Family 3 + analytical-framework.md §1 Family 3 | CLEAR |
| AEP-008-ARG-2003.md | `§Family 3 (c) LAT-2` | coverage-audit.md §Family 3 + calibration decision CM-D | CLEAR |
| AEP-009-ECU-1999.md | `§Family 3 (c) LAT-3` | coverage-audit.md §Family 3 + analytical-framework.md §1 Family 3 | CLEAR |

### 2.4 — QA test authorship gate

**Documentation sprint — no code test files.** AEP entries are reviewed against TEMPLATE.md structural compliance and analytical-framework.md epistemic bounds. EL review is the quality gate. No backend or frontend test files produced by this sprint group.

---

## Section 3 — Scope Declaration

### 3.0 — Scope lock confirmation

- [x] All ADR and calibration decisions affecting this sprint's scope are EL-approved and merged to `release/m20`

**Scope uncertainty (documented):** AEP-008 (ARG 2003-2007 Kirchner recovery) has no pre-existing fixture file — it requires constructing a scenario configuration from CM-D calibration decision parameters (`docs/calibration/m19-cm-d-arg-kirchner-calibration-decision.md`). This adds authorship complexity relative to the other five entries. If CM-D inputs prove insufficient to produce a meaningful harness output, the entry will document this as a scope limitation and declare the fidelity ceiling accordingly.

### 3.1 — Issues in scope

| Deliverable | Sprint journal issue | Priority |
|---|---|---|
| AEP-004-ZMB-2005.md (SSA-LIC Type A) | #1798 | Immediate — Demo 9 north star entry |
| AEP-005-SEN-2000.md (SSA-LIC Type A) | #1798 | Immediate — first within-family cross-entity comparison |
| AEP-006-GHA-2022.md (SSA-LIC Type A) | #1798 | Immediate |
| AEP-007-ARG-2001.md (LATAM-EM Type A+B) | #1798 | Immediate |
| AEP-008-ARG-2003.md (LATAM-EM Type A Kirchner) | #1798 | Immediate — requires CM-D scenario construction |
| AEP-009-ECU-1999.md (LATAM-EM Type A) | #1798 | Immediate |

**Issues filed at G1 AEA briefing — tracked but not G2 implementation scope:**

| Issue | Title | Priority |
|---|---|---|
| #1796 | engine: fin_composite path insensitivity in CF scenarios | M20 tracked; implementation M21+ |
| #1797 | engine: failure mode non-detection in EURO-AREA rapid-onset crises | M20 tracked; implementation M21+ |

### 3.2 — Issues explicitly out of scope

| Item | Horizon | Rationale |
|---|---|---|
| AEP-010–011 (SOUTH-SE-ASIAN) | G3 | Separate sprint group; begins after G2 exits |
| DEMO-217, DEMO-233, DEMO-234, NM-099/#1759, NM-101/#1791 | G4 | Engineering sprint; independent of G2 AEA work |
| ADR-008 renewal (SCAN-029 carry-forward) | M20 (not G2) | Not blocked on G2; assign to Architect Agent |
| #1796, #1797 (engine gaps from G1 AEA briefing) | M21+ | Filed for tracking; no implementation in M20 |
| PRT, BGD, remittance channel gap issues | G3 (filing) | Per sprint plan; gap issues filed at G3 close |

---

## Section 4 — Fixture and Harness Availability

*This section is G2-specific: AEP authorship requires harness output for each scenario.
Type A entries use existing fixtures. Type B entries (AEP-007) additionally require a
counter-factual harness run with temporal blindfold.*

### 4.1 — Fixture status

| Entry | Fixture file | Status | Notes |
|---|---|---|---|
| AEP-004 (ZMB) | `backend/tests/fixtures/zmb_scenario.py` | Exists — M19 backtesting | `build_zmb_scenario()` |
| AEP-005 (SEN) | `backend/tests/fixtures/sen_scenario.py` | Exists — M19 backtesting | `build_sen_scenario()` |
| AEP-006 (GHA) | `backend/tests/fixtures/ghana_2022_scenario.py` | Exists — M19 backtesting | Function name TBD — inspect before run |
| AEP-007 (ARG 2001-2002) | `backend/tests/fixtures/argentina_2001_2002_scenario.py` | Exists — M19 backtesting; CM-D Step 3 inputs included | `build_argentina_scenario()` (baseline) + Zero Deficit CF |
| AEP-008 (ARG 2003-2007) | None — construct from CM-D | Requires scenario construction | Use CM-D decision at `docs/calibration/m19-cm-d-arg-kirchner-calibration-decision.md` |
| AEP-009 (ECU 1999-2000) | `backend/tests/fixtures/ecuador_1999_2000_scenario.py` | Exists — M19 backtesting | `build_ecuador_scenario()` |

### 4.2 — Harness run requirements

| Entry | Run type | Temporal blindfold required? | Blindfold status |
|---|---|---|---|
| AEP-004 (ZMB) | Type A | No | N/A |
| AEP-005 (SEN) | Type A | No | N/A |
| AEP-006 (GHA) | Type A | No | N/A |
| AEP-007 (ARG) baseline | Type A component | No | N/A |
| AEP-007 (ARG) CF | Type B component | Yes | **BLINDED** — `argentina_2001_2002_scenario.py` Zero Deficit CF configuration committed in M19 G2C (Issue #1547, before AEP-007 commissioned) |
| AEP-008 (ARG Kirchner) | Type A | No | N/A (Type A — no blindfold required) |
| AEP-009 (ECU) | Type A | No | N/A |

**NM-101 protocol:** For the AEP-007 Type B run, pre-run the baseline via `POST /api/v1/scenarios/{baseline_id}/run` before calling `run_harness(run_type=TYPE_B, baseline_run_id=...)`.

### 4.3 — Expected fidelity ceilings

| Entry | Family | Expected entry ceiling | Limiting factor |
|---|---|---|---|
| AEP-004 (ZMB) | SSA-LIC | DIRECTION_ONLY (fiscal); MAGNITUDE conditional (human dev., copper channel) | T3 fiscal multiplier (Fosu 2011); T2 WDI enables MAGNITUDE on hd if CM two-condition met |
| AEP-005 (SEN) | SSA-LIC | DIRECTION_ONLY (fiscal); MAGNITUDE conditional (human dev.) | T3 fiscal multiplier; T2 WDI conditional |
| AEP-006 (GHA) | SSA-LIC | DIRECTION_ONLY | T3 fiscal; shorter time window (2022–2023) limits CM two-condition condition 2 |
| AEP-007 (ARG) | LATAM-EM | DIRECTION_ONLY | T3 across all indicators; T2 external balance (Céspedes & Velasco) on commodity channel only |
| AEP-008 (ARG Kirchner) | LATAM-EM | DIRECTION_ONLY | T3 across all indicators; CM-D inputs improve scenario accuracy but not multiplier confidence |
| AEP-009 (ECU) | LATAM-EM | DIRECTION_ONLY | T3 across all indicators; dollarisation channel modelled as DIRECTION_ONLY |

**Entry ceiling note:** Per `docs/evidence/analytical-framework.md §2`, the entry ceiling is the lowest fidelity tier across all primary indicators. For all G2 entries the practical ceiling is DIRECTION_ONLY given T3 fiscal multipliers in both families. ZMB and SEN may have MAGNITUDE sub-entries on human development if the CM two-condition is satisfied; the entry-level ceiling remains DIRECTION_ONLY.

---

## Section 5 — Near-Miss Sweep

**Near-miss sweep date:** 2026-07-07  
**Sweep period:** Since G1 sprint entry (2026-07-07)

| Finding | Category | PI Agent register call issued? | NM entry number |
|---|---|---|---|
| NM-101 | Baseline-not-run bug in Type B tests | Filed in PR #1790 | NM-101 |

No new near-miss findings at G2 entry. NM-101 process improvement applies to AEP-007 Type B run (§4.2 above).

---

## Section 6 — Sprint Group Isolation (M18 onward)

### 6.1 — Sprint sub-branch

| Field | Value |
|---|---|
| Sprint sub-branch | `sprint/m20-g2` |
| Cut from | `release/m20` (at commit `efbd4bb` — post G1 integration and state-sync) |
| Sprint journal issue | #1798 |

### 6.2 — File-conflict risk assessment

| File | Lane required | Trigger |
|---|---|---|
| `SESSION_STATE.md` | PM Agent coordination lane | Sprint exit cockpit update |
| `docs/evidence/AEP-004-ZMB-2005.md` through `AEP-009-ECU-1999.md` | Sprint sub-branch (AEA file authority) | AEP-004–009 authorship |
| `docs/process/near-miss-registry.md` | Sprint sub-branch if new NM filed | Only if new near-miss identified |

### 6.3 — Infrastructure dependency declaration

- [x] No DS-owned file changes required

#### 6.3a — New output paths declaration

- [x] AEP harness output reports: `backend/tests/backtesting/reports/` — existing path; tracked in version control per EL decision 2026-07-07 (PR #1789). No `.gitignore` changes needed.

### 6.4 — Cross-group dependency declaration

- [x] No cross-group dependencies. G2 (AEA documentation) is independent of G4 (engineering).

### 6.5 — Prior NM verification

| NM entry | Process improvement required | Applied in this sprint? |
|---|---|---|
| NM-100 | Pre-PR diff check before any multi-file PR | Yes — `git diff HEAD --name-only` before integration PR |
| NM-101 | Pre-run baseline via `/run` before Type B `run_harness` call | Yes — documented in §4.2 above; applies to AEP-007 Type B |

---

## Section 7 — G1 Findings Carried Forward

The following findings from the G1 AEA briefing (2026-07-07) are noted as context for G2 authorship:

1. **fin_composite path insensitivity** (#1796): expected to recur in ARG counter-factual (AEP-007 Type B). Document in §7 Known Limitations of AEP-007; do not inflate fidelity claims based on hd_composite divergence alone.
2. **Failure mode non-detection** (#1797): expect same pattern in ARG 2001 (canonical crisis), ECU 1999 (banking freeze + dollarisation). Document in §7 of affected entries.
3. **DIRECTION_ONLY ceiling** consistent across both G1 families even with best data. G2 entries are all lower-data-confidence families than EURO-AREA — DIRECTION_ONLY is the expected ceiling for all six entries.

---

## EL Approval Record

**EL approval:** Confirmed in session — "file those first, then proceed to g2"

> "file those first, then proceed to g2"  
> — @PublicEnemage (2026-07-07)
