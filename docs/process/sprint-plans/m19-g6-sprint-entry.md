---
name: m19-g6-sprint-entry
type: sprint-entry
milestone: M19 — Constraint Search and Empirical Calibration
sprint-group: G6
status: Filed — awaiting EL approval
authored-by: PM Agent
authored-date: 2026-07-04
el-approved: false
release-branch: release/m19
sop-reference: docs/process/sprint-planning-sop.md
---

# Sprint Entry — M19, G6: Demo 8 Clearance

**Status:** Filed — awaiting EL approval before implementation begins
**Date authored:** 2026-07-04
**Release branch:** `release/m19`
**Sprint plan:** `docs/process/sprint-plans/m19-sprint-plan.md`

*Authority: `docs/process/sprint-planning-sop.md §Sprint Entry Gate` (Phase C output).*

---

## Section 1 — Sprint Identification

| Field | Value |
|---|---|
| Milestone | M19 — Constraint Search and Empirical Calibration |
| GitHub Milestone | #21 |
| Sprint group | G6 |
| Release branch | `release/m19` |
| Sprint plan document | `docs/process/sprint-plans/m19-sprint-plan.md §Wave 4` |
| Exit checklist issue | #1535 |
| Sprint journal issue | #1716 |
| Wave coordination tier | Standard — no concurrent active groups at entry |
| Concurrent groups at entry | 0 |
| Cross-group dependencies | None — Wave 3 fully integrated to `release/m19` |

---

## Section 2 — Entry Invariants Checklist

### 2.1 — Structural gates

- [x] **Release branch exists:** `release/m19` cut from `main` at M19 kickoff (2026-07-02 at 1bf1ecc)
- [x] **CI trigger verified:** `.github/workflows/ci.yml` `pull_request: branches` includes `release/m*`
- [x] **Sprint plan EL-approved:** `docs/process/sprint-plans/m19-sprint-plan.md` — EL-approved 2026-07-02; G6 Wave 4 section added 2026-07-04 (PR #1714 merged)

### 2.2 — ADR prerequisite gate

G6 contains no items requiring a new ADR. #1657 requires an update to the accepted ADR-020 (transmission table correction to reflect verified subscription strings and enum reconciliation) — this is documentation of a correction to an already-accepted ADR, not a new architectural decision. ADR-020 amendment does not block implementation; it must merge in the same PR as the #1657 implementation.

| Group | Required ADR | ADR status | Gate |
|---|---|---|---|
| G6 — #1456 | N/A | N/A | CLEAR |
| G6 — #1538 | N/A | N/A | CLEAR |
| G6 — #1657 | ADR-020 update (transmission table only) | Accepted; update in scope | CLEAR — update ships with implementation |
| G6 — #1709 | N/A | N/A | CLEAR |
| G6 — #1710 | N/A | N/A | CLEAR |

### 2.3 — Intent document gate

#1709 (tolerance band UI) is the only user-facing deliverable in G6 — it adds a new visible element to the FOUND state of the constraint-floor search panel. An intent document is required before implementation.

All other G6 items are non-user-facing: #1456 (runtime defensive guard), #1538 (backend schema enforcement), #1657 (engine subscription fix + calibration rows + ADR correction), #1710 (test correction).

| Deliverable | ADR reference | Intent document path | Filed? |
|---|---|---|---|
| #1709 — FOUND state tolerance band display | N/A (within ADR-021 constraint-floor architecture) | `docs/process/intents/M19-G6-2026-07-04-found-tolerance-band.md` | **No — BLOCKING** |

**Blocking gate:** The intent document for #1709 must be filed and EL-approved before the #1709 implementation PR opens. The implementation PR for #1456, #1538, and #1710 may open before the intent document is filed — they are independent of #1709 and non-user-facing.

### 2.4 — QA test authorship gate

Two items require tests authored before implementation code is written:

**#1709 (tolerance band UI):** An E2E assertion confirming the tolerance band element is visible in the FOUND state must be authored before the implementation PR opens. This can be added to the existing constraint-floor E2E spec (`frontend/tests/e2e/m19-g1-constraint-floor.spec.ts`) or as a targeted addition to the demo narration spec.

**#1657 (DemographicModule subscriptions + elasticity rows):** Unit tests covering the two new event→demographic paths (`emergency_policy_imf_program_acceptance` and `emergency_policy_emergency_declaration`) must be authored before the implementation PR opens. CM cert must be on record before elasticity values are assigned and tests are parameterised (NM-084 gate — see §2.5).

| Deliverable | Intent document | Test file | Authored before implementation? |
|---|---|---|---|
| #1709 — tolerance band display | `docs/process/intents/M19-G6-2026-07-04-found-tolerance-band.md` | `frontend/tests/e2e/m19-g1-constraint-floor.spec.ts` (addition) | **No — BLOCKING** |
| #1657 — subscription fix + elasticity rows | CM cert on #1657 | `backend/tests/test_m19_g6_demographic_subscriptions.py` | **No — BLOCKING** |

**#1456 and #1538 and #1710:** These are fixes and corrections, not new features. Tests are updated or corrected in the same PR rather than authored separately before. Gate N/A for these three.

### 2.5 — CM certification gate (#1657 specific)

**NM-084 gate:** CM Agent must post a cert comment on issue #1657 confirming elasticity values for `emergency_policy_imf_program_acceptance` and `emergency_policy_emergency_declaration` before the #1657 implementation PR opens. PI Agent posts the integration-PR gate comment after the cert is on record.

This is the same two-step gate used for CM Sprints A, B, and C.

- [ ] **CM cert on #1657:** Chief Methodologist posts calibration cert on issue #1657 before #1657 implementation PR opens — **BLOCKING for #1657 PR only**

The #1657 CM cert does not block #1456, #1538, #1709, or #1710 implementation PRs.

---

## Section 3 — Scope Declaration

### 3.0 — Scope lock confirmation

- [x] All ADR decisions affecting this sprint's scope are EL-approved and merged to `release/m19`. No new ADR is required. ADR-020 (accepted) covers the subscription and emergency instrument architecture; the G6 update to its transmission table is a correction within the accepted architecture, not a new decision.

**Scope uncertainty:** None.

### 3.1 — Issues in scope

| Issue | Title | Priority | Implementing area |
|---|---|---|---|
| #1456 | MDAAlertPanelZone1B: scenarioId crash guard | Immediate — crash risk | `frontend/src/components/MDAAlertPanelZone1B.tsx` |
| #1538 | Focal cohort floor Pydantic validation | Immediate — correctness | `backend/app/schemas.py` (new `FocalCohortConfig` model) |
| #1657 | NM-090/091: dead subscriptions + elasticity rows + ADR-020 update | High — engine correctness | `backend/app/simulation/modules/demographic/module.py`, `elasticities.py`, `docs/adr/ADR-020-*.md` |
| #1709 | FOUND state: tolerance band (±0.01) not displayed | Immediate — Demo 8 Act 1 | `frontend/src/components/ControlPlaneColumn.tsx` |
| #1710 | AC-12: resolve `__structural_absence__` placeholder | Immediate — Demo 8 Act 1 | `backend/tests/` (AC-12 test rewrite) + simulation engine (structural absence key identification) |

### 3.2 — Issues explicitly out of scope

| Issue | Title | Rationale |
|---|---|---|
| #1711 | GRC AC-1 live harness run | DATABASE_URL run only — no code; runs in parallel outside sprint group |
| #1712 | ARG AC-1 live harness run | DATABASE_URL run only — no code; runs in parallel outside sprint group |
| #1713 | PAK AC-1 live harness run | DATABASE_URL run only — no code; runs in parallel outside sprint group |
| #1544 | Demo 8 live session | Milestone exit gate — not a G6 deliverable |
| #1535 | M19 Exit Checklist | Milestone gate — closes last |

---

## Section 4 — ADR Prerequisite Summary

| Group | ADR required | ADR status | Implementation may begin? |
|---|---|---|---|
| G6 — #1456 | None | N/A | Yes |
| G6 — #1538 | None | N/A | Yes |
| G6 — #1657 | ADR-020 update (transmission table correction) | ADR-020 accepted; update ships with impl PR | Yes — update is documentation of corrections, not a new decision |
| G6 — #1709 | None | N/A | Yes (after intent document + E2E test filed) |
| G6 — #1710 | None | N/A | Yes |

---

## Section 5 — Near-Miss Sweep

**Near-miss sweep date:** 2026-07-04
**Sweep period:** Since CM Sprint C close (2026-07-04)

No new near-misses have been filed in the sweep period (CM Sprint C closed today). The most recent applicable NM codifications from G5 pre-flight (2026-07-03) are verified in §6.5.

| Finding | Category | PI Agent register call issued? | NM entry |
|---|---|---|---|
| No new findings in sweep period | N/A | N/A | N/A |

---

## Section 6 — Sprint Group Isolation

### 6.1 — Sprint sub-branch

| Field | Value |
|---|---|
| Sprint sub-branch | `sprint/m19-g6` |
| Cut from | `release/m19` |
| Sprint journal issue | #1716 |

**PM Agent sprint sub-branch cut command (after EL approval):**
```bash
git checkout -b sprint/m19-g6 release/m19 && git push -u origin sprint/m19-g6
```

### 6.2 — File-conflict risk assessment

| File | Lane required | Trigger |
|---|---|---|
| `SESSION_STATE.md` | PM Agent coordination lane | Sprint exit cockpit update |
| `docs/process/near-miss-registry.md` | PM Agent coordination lane (PI Agent authors) | If NM identified |
| `docs/adr/ADR-020-*.md` | Sprint sub-branch (no coordination needed — correction to own ADR file) | #1657 ADR-020 transmission table update |
| `backend/app/simulation/modules/demographic/module.py` | Sprint sub-branch | #1657 subscription strings |
| `backend/app/simulation/modules/demographic/elasticities.py` | Sprint sub-branch | #1657 new elasticity rows |
| `backend/app/schemas.py` | Sprint sub-branch | #1538 FocalCohortConfig model |
| `frontend/src/components/MDAAlertPanelZone1B.tsx` | Sprint sub-branch | #1456 scenarioId guard |
| `frontend/src/components/ControlPlaneColumn.tsx` | Sprint sub-branch | #1709 tolerance band display |

No shared-file conflicts anticipated between G6 items. `elasticities.py` is touched by both #1657 (new rows) and no other G6 item — single-author, no conflict risk within the group. If #1657 and another G6 item land in separate PRs, sequence #1657 before any other PR that reads `elasticities.py`.

### 6.3 — Infrastructure dependency declaration

- [x] No DS-owned file changes required

No new `.github/workflows/`, `.githooks/`, or `.gitignore` changes needed.

#### 6.3a — New output paths declaration

- [x] No new output directories — all generated paths are already covered by `.gitignore`

### 6.4 — Cross-group dependency declaration

- [x] No cross-group dependencies

G6 is the only active sprint group. The Act 2 verification items (#1711–#1713) are DATABASE_URL runs outside the sprint group — no file area overlap.

### 6.5 — Prior NM verification

**NM verification sweep date:** 2026-07-04
**Sweep period:** Since G5 close (2026-07-03)

| NM entry | Process improvement required | Applied in this sprint? |
|---|---|---|
| NM-084 | CM cert on issue before CM-related impl PR opens; PI Agent posts gate comment on PR | Yes — §2.5 CM cert gate declared; applies to #1657 impl PR |
| NM-086 | E2E mock routes verified against `api_contracts.yml` before impl PR opens | Yes — #1709 E2E test author must verify constraint-floor endpoint mock shape against `docs/schema/api_contracts.yml` before the E2E test PR opens |
| NM-090 | DemographicModule dead subscription strings | Yes — #1657 is the resolution |
| NM-091 | ADR-020 registry/enum mismatch | Yes — #1657 includes ADR-020 transmission table reconciliation |
| NM-094 | Test file presence check before integration PR | Yes — PI Agent verifies test files present before G6 integration PR opens |

---

## EL Approval Record

**EL approval:** Pending

> {EL approval statement — to be filled at approval time}
> — @PublicEnemage ({date})
