---
name: m20-sprint-g3-entry
type: sprint-entry
milestone: M20 — Analytical Evidence Portfolio and Demo 9
sprint-group: G3
status: Filed
authored-by: PM Agent
authored-date: 2026-07-07
el-approved: true
release-branch: release/m20
sop-reference: docs/process/sprint-planning-sop.md
---

# Sprint Entry — M20 G3 — AEP SOUTH-SE-ASIAN Entries + Gap Closure Issues

**Status:** EL-approved — implementation authorised (in-session 2026-07-07 — EL directive "proceed")
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
| Sprint number | G3 |
| Release branch | `release/m20` |
| Sprint plan document | `docs/process/sprint-plans/m20-sprint-plan.md` |
| Exit checklist issue | #1773 |
| Sprint groups in scope | G3 |
| Wave coordination tier | Standard — documentation sprint; no engineering dependencies |
| Concurrent groups at entry | 0 — G4 not yet started |
| Cross-group dependencies | None — G3 AEA documentation is independent of G4 engineering |

---

## Section 2 — Entry Invariants Checklist

### 2.1 — Structural gates

- [x] **Release branch exists:** `release/m20` — confirmed; G2 integration PR #1809 merged 2026-07-07
- [x] **CI trigger verified:** `.github/workflows/ci.yml` `pull_request: branches` includes `release/m*`
- [x] **Sprint plan EL-approved:** `docs/process/sprint-plans/m20-sprint-plan.md` EL-approved in session 2026-07-07

### 2.2 — ADR prerequisite gate

**N/A — AEA documentation sprint.** G3 deliverables are AEP evidence entries authored in `docs/evidence/`. No new ADRs are required. The governing calibration document (CM-C for SOUTH-SE-ASIAN) is already accepted and on `release/m20`.

| Group | Required ADR | ADR status | Gate |
|---|---|---|---|
| G3 | None | N/A | CLEAR |

### 2.3 — Intent document gate

**Documentation sprint — AEP entries are authorship artifacts.** The coverage audit (`docs/evidence/coverage-audit.md`) serves as the functional intent specification: it identifies which scenarios to run, calibration families, fidelity ceilings, and what each entry should document.

| Deliverable | Coverage audit reference | Intent specification | Gate |
|---|---|---|---|
| AEP-010-LKA-2022.md | `§Family 4 (c) SEA-2` | coverage-audit.md §Family 4 + analytical-framework.md §1 Family 4 | CLEAR |
| AEP-011-PAK-2022.md | `§Family 4 (c) SEA-1` | coverage-audit.md §Family 4 + analytical-framework.md §1 Family 4 | CLEAR |
| Gap closure issue: PRT fixture | `§Coverage Gaps (a)` | coverage-audit.md §Coverage Gaps | CLEAR |
| Gap closure issue: BGD fixture | `§Coverage Gaps (d)` | coverage-audit.md §Family 4 (d) | CLEAR |
| Gap closure issue: remittance channel | `§Coverage Gaps (d)` | coverage-audit.md §Family 4 (d) | CLEAR |

### 2.4 — QA test authorship gate

**Documentation sprint — no code test files.** AEP entries are reviewed against TEMPLATE.md structural compliance and analytical-framework.md epistemic bounds. EL review is the quality gate. Gap closure issues are GitHub issues only — no code in G3. No backend or frontend test files produced by this sprint group.

---

## Section 3 — Scope Declaration

### 3.0 — Scope lock confirmation

- [x] All ADR and calibration decisions affecting this sprint's scope are EL-approved and merged to `release/m20`

**Scope note on AEP-010 (LKA):** The sprint plan describes AEP-010 as "Type A — Coffin Corner entry" (5 annual steps, 2019→2023). The coverage audit §SEA-2 identifies the LKA scenario as "Type A" with no mention of a counter-factual requirement. The fixture `build_sri_lanka_counterfactual_scenario()` exists and is committed; however, per the sprint plan G3 scope, LKA is Type A only. The counter-factual run is out of scope for G3 and may be added as a future AEP entry if warranted. This avoids scope creep while the fixture is available for potential G4+ use.

**Scope note on AEP-011 (PAK):** The sprint plan describes AEP-011 as "Type A + B — SBA compliance + deviation counter-factual." The PAK CF fixture (`build_pakistan_counterfactual_scenario()`) was committed in M19-G2C (#1550) on 2026-07-03, before G3 commissioning. Temporal blindfold satisfied. NM-101 protocol applies to PAK Type B run.

### 3.1 — Issues in scope

| Deliverable | Sprint journal issue | Priority |
|---|---|---|
| AEP-010-LKA-2022.md (SOUTH-SE-ASIAN Type A) | #1811 | Immediate — completes all-six-failure-modes Coffin Corner documentation |
| AEP-011-PAK-2022.md (SOUTH-SE-ASIAN Type A+B) | #1811 | Immediate — first within-family PAK/LKA cross-entity comparison |
| Gap issue: PRT 2010 fixture | #1811 | File at G3 close — M21+ implementation |
| Gap issue: BGD 2022 fixture | #1811 | File at G3 close — M21+ implementation |
| Gap issue: remittance channel (ELASTICITY_REGISTRY) | #1811 | File at G3 close — M21+ implementation |

### 3.2 — Issues explicitly out of scope

| Item | Horizon | Rationale |
|---|---|---|
| AEP-010 Type B (LKA CF — fertiliser ban reversal) | M21+ | CF fixture exists but out of G3 scope per sprint plan |
| DEMO-217, DEMO-233, DEMO-234, NM-099/#1759 | G4 | Engineering sprint; independent of G3 |
| ADR-008 renewal (SCAN-029 carry-forward) | M20 (not G3) | Not blocked on G3; assign to Architect Agent |
| #1796, #1797 (engine gaps from G1/G2 AEA briefing) | M21+ | Filed for tracking; no implementation in M20 |
| BGD, IND fixture implementation | M21+ | Only gap issues filed in G3; no implementation |
| Live interactive constraint-floor search | M21 | Deferred per sprint plan |

---

## Section 4 — Fixture and Harness Availability

*This section is G3-specific: AEP authorship requires harness output for each scenario.
LKA is Type A; PAK is Type A + B. PAK Type B requires temporal blindfold compliance check
and NM-101 pre-run protocol.*

### 4.1 — Fixture status

| Entry | Fixture file | Status | Notes |
|---|---|---|---|
| AEP-010 (LKA) | `backend/tests/fixtures/sri_lanka_2022_scenario.py` | Exists — M19-G2C (#1549), 2026-07-03 | `build_sri_lanka_scenario()` — 5 steps, annual |
| AEP-011 (PAK) baseline | `backend/tests/fixtures/pakistan_2022_scenario.py` | Exists — M19-G2C (#1550), 2026-07-03 | `build_pakistan_scenario()` — 4 steps, biannual |
| AEP-011 (PAK) CF | `backend/tests/fixtures/pakistan_2022_scenario.py` | Exists — M19-G2C (#1550), 2026-07-03 | `build_pakistan_counterfactual_scenario()` |

### 4.2 — Harness run requirements

| Entry | Run type | Temporal blindfold required? | Blindfold status |
|---|---|---|---|
| AEP-010 (LKA) | Type A | No | N/A |
| AEP-011 (PAK) baseline | Type A component | No | N/A |
| AEP-011 (PAK) CF | Type B component | Yes | **BLINDED** — `pakistan_2022_scenario.py` CF config committed in M19-G2C (Issue #1550) on 2026-07-03, before AEP-011 commissioned 2026-07-07 |

**NM-101 protocol:** For the AEP-011 Type B run, pre-run the baseline via `POST /api/v1/scenarios/{baseline_id}/run` before calling `run_harness(run_type=TYPE_B, baseline_run_id=...)`.

### 4.3 — Expected fidelity ceilings

| Entry | Family | Expected entry ceiling | Limiting factor |
|---|---|---|---|
| AEP-010 (LKA) | SOUTH-SE-ASIAN | DIRECTION_ONLY | T3 fiscal multiplier (Batini et al. 2012 / APAC REO); T2 data available for hd and external balance but multiplier is limiting |
| AEP-011 (PAK) | SOUTH-SE-ASIAN | DIRECTION_ONLY | Same family; T3 across all indicators; remittance channel absent (major structural gap documented in coverage audit §Family 4) |

**Entry ceiling note:** Per `docs/evidence/analytical-framework.md §2`, the entry ceiling is the lowest fidelity tier across all primary indicators. Both LKA and PAK are in the SOUTH-SE-ASIAN family (CM-C); all multiplier estimates are T3. DIRECTION_ONLY is the expected ceiling for both entries. Coverage audit §Family 4 confirms: "No entity in this family achieves MAGNITUDE tier at current calibration."

**DIRECTION_ONLY ceiling driver:** Unlike EURO-AREA (CM-A, ADR-007 posterior available) or even SSA-LIC/LATAM-EM (Fosu 2011 / Ilzetzki LAC range as T3 regional), SOUTH-SE-ASIAN relies on Batini et al. (2012) and IMF APAC REO multiplier ranges — both T3. The remittance channel absence (PAK ~8% GDP, LKA ~8% GDP) means the human development channel systematically underweights a major income stabiliser in both cases.

---

## Section 5 — Near-Miss Sweep

**Near-miss sweep date:** 2026-07-07
**Sweep period:** Since G2 sprint entry (2026-07-07)

| Finding | Category | PI Agent register call issued? | NM entry number |
|---|---|---|---|
| SESSION_STATE.md on sprint branch (G2) | Process deviation — shared state on sprint branch | No — minor deviation; content superseded by G2 close state-sync | Note only |

**Note on G2 SESSION_STATE.md deviation:** During G2 sprint entry filing, `SESSION_STATE.md` was committed directly to `sprint/m20-g2` rather than via a `chore/m{N}-state-sync-NNN` branch. Content was correct and was superseded by `chore/m20-state-sync-005` at G2 close. This is a process reminder for G3 entry: `SESSION_STATE.md` updates must go through `chore/m20-state-sync-NNN` → `release/m20` (PM Agent lane), not via sprint branch commits.

No new near-miss findings at G3 entry requiring NM filing.

---

## Section 6 — Sprint Group Isolation (M18 onward)

### 6.1 — Sprint sub-branch

| Field | Value |
|---|---|
| Sprint sub-branch | `sprint/m20-g3` |
| Cut from | `release/m20` (at commit `c9fce95` — post G2 integration and state-sync-005) |
| Sprint journal issue | #1811 |

### 6.2 — File-conflict risk assessment

| File | Lane required | Trigger |
|---|---|---|
| `SESSION_STATE.md` | PM Agent coordination lane (chore/m20-state-sync) | Sprint exit cockpit update — NOT on sprint branch |
| `docs/evidence/AEP-010-LKA-2022.md` | Sprint sub-branch (AEA file authority) | AEP-010 authorship |
| `docs/evidence/AEP-011-PAK-2022.md` | Sprint sub-branch (AEA file authority) | AEP-011 authorship |
| `docs/process/near-miss-registry.md` | Sprint sub-branch if new NM filed | Only if new near-miss identified |

### 6.3 — Infrastructure dependency declaration

- [x] No DS-owned file changes required

#### 6.3a — New output paths declaration

- [x] AEP harness output reports: `backend/tests/backtesting/reports/` — existing path; tracked in version control per EL decision 2026-07-07 (PR #1789). No `.gitignore` changes needed.
- [x] LKA and PAK fixtures are existing files; no new fixture files required for G3 scope.

### 6.4 — Cross-group dependency declaration

- [x] No cross-group dependencies. G3 (AEA documentation) is independent of G4 (engineering).

### 6.5 — Prior NM verification

| NM entry | Process improvement required | Applied in this sprint? |
|---|---|---|
| NM-100 | Pre-PR diff check before any multi-file PR | Yes — `git diff HEAD --name-only` before integration PR |
| NM-101 | Pre-run baseline via `/run` before Type B `run_harness` call | Yes — applies to AEP-011 PAK Type B (§4.2 above) |

---

## Section 7 — G1 and G2 Findings Carried Forward

The following findings from the G1 and G2 AEA briefings are noted as context for G3 authorship:

1. **fin_composite path insensitivity** (#1796): observed in G1 (GRC partial paths) and G2 (AEP-008 most severe: flat across 4 steps). Expect same pattern in PAK/LKA if fiscal impulse signals are moderate. Document in §7 Known Limitations of affected entries; do not inflate fidelity claims based on hd_composite alone.

2. **Failure mode non-detection** (#1797): pattern holds across all nine G1+G2 entries. LKA 2022 is the most important test case for this gap — it is the entry most likely to trigger failure mode detection (all six failure modes documented historically). If failure modes continue to be undetected in LKA, document explicitly in §7 and note the severity of the gap (canonical six-failure-mode case failing to register is a stronger statement than prior entries).

3. **DIRECTION_ONLY ceiling** consistent across G1 and G2. G3 entries are both SOUTH-SE-ASIAN CM-C (T3 multiplier) — DIRECTION_ONLY is the expected ceiling.

4. **CB Cloud composite aggregation gap** (AEP-006 GHA finding, analogous to #1796): if either LKA or PAK shows a simultaneous financial stabilisation / human development deterioration divergence, note whether the composite architecture can reproduce it or masks it (as in GHA).

5. **Remittance channel absence** (coverage audit §Family 4): PAK and LKA both have ~8% GDP remittance inflows not modelled. This is a structural gap that will affect the human development fidelity ceiling beyond just DIRECTION_ONLY — the direction of hd_composite at recovery steps may be understated because the remittance stabilisation channel is absent. Document in §7 of both entries.

6. **Steps 1–2 identical pattern** (GHA AEP-006): biannual step resolution with no composite differentiation. PAK is biannual (4 steps); if PAK shows the same flat initial response pattern, document and note the biannual resolution as a contributing factor.

---

## EL Approval Record

**EL approval:** Confirmed in session — "proceed"

> "proceed"
> — @PublicEnemage (2026-07-07)
