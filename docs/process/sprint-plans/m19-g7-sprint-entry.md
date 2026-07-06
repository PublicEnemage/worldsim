---
name: m19-g7-sprint-entry
type: sprint-entry
milestone: M19 — Constraint Search and Empirical Calibration
sprint-group: G7
status: EL-approved 2026-07-04
authored-by: PM Agent
authored-date: 2026-07-04
el-approved: 2026-07-04
release-branch: release/m19
sop-reference: docs/process/sprint-planning-sop.md
---

# Sprint Entry — M19, Sprint Group G7

**Status:** Filed — awaiting EL approval before implementation begins
**Date authored:** 2026-07-04
**Release branch:** `release/m19`
**Sprint plan:** `docs/process/sprint-plans/m19-sprint-plan.md`
**BPO evaluation:** 2026-07-04 — PROCEED verdict; HIGH priority; Demo 8 pre-flight; see §BPO Assessment below

*Authority: `docs/process/sprint-planning-sop.md §Sprint Entry Gate` (Phase C output).*

---

## Section 1 — Sprint Identification

| Field | Value |
|---|---|
| Milestone | M19 — Constraint Search and Empirical Calibration |
| GitHub Milestone | #21 |
| Sprint number | G7 |
| Release branch | `release/m19` |
| Sprint plan document | `docs/process/sprint-plans/m19-sprint-plan.md` |
| Exit checklist issue | #1535 |
| Sprint groups in scope | G7 |
| Wave coordination tier | Standard — no concurrent active sprint groups at entry |
| Concurrent groups at entry | 0 of 5 max — all G1–G6 + CM-A/B/C integrated |
| Cross-group dependencies | None |

---

## Section 2 — Entry Invariants Checklist

### 2.1 — Structural gates

- [x] **Release branch exists:** `release/m19` cut from `main` 2026-07-02 at 1bf1ecc
- [x] **CI trigger verified:** `.github/workflows/ci.yml` covers `release/m*` and `sprint/m*`
- [x] **Sprint plan EL-approved:** `m19-sprint-plan.md` has `el-approved: 2026-07-02` in frontmatter

### 2.2 — ADR prerequisite gate

- [x] No new ADR required. This is a bug fix sprint restoring behavior designed under ADR-020
  (DemographicModule transmission channels). The fix adds 4 elasticity rows that NM-090/091
  prescribed as part of the original G6 scope — no architectural decision is being made.

**ADR prerequisite status:**

| Group | Required ADR | ADR status | Gate |
|---|---|---|---|
| G7 | N/A — bug fix (ADR-020 already accepted) | Accepted | CLEAR |

### 2.3 — Intent document gate

This sprint is a **bug fix sprint, not a new user-facing deliverable**. The fix restores
behavior that was supposed to exist after G6 (NM-090/091 prescription, partially implemented
by PR #1722). The equivalent of an intent document is:

1. The existing G6 test file `backend/tests/test_m19_g6_demographic_subscriptions.py`
   (already authored; contains 9 acceptance criteria for the expected behavior)
2. The NM-096 near-miss entry (2026-07-04) documenting the gap and required correction
3. The 8 ACs in issue #1729

No separate intent document is required: "Infrastructure sprint — bug fix restoring
previously designed behavior — intent artifacts satisfied by NM-096 and #1729 ACs."

**Intent document status:**

| Deliverable | ADR reference | Intent document path | Filed? |
|---|---|---|---|
| Elasticity rows + NM-056 fix | ADR-020 (accepted) | NM-096 + #1729 ACs serve as intent | Yes — see note above |

### 2.4 — QA test authorship gate

The QA test file was authored during G6 and already contains the failing/skipping test cases.
The G7 implementation work converts 2 `pytest.skip()` stubs into real assertions and adds 4
elasticity rows that cause 4 previously-skipping tests to PASS. No new test file is required.

**QA test status:**

| Deliverable | Intent document | Test file path | Authored before implementation? |
|---|---|---|---|
| Elasticity rows for `imf_program_acceptance` | NM-096 + #1729 ACs | `backend/tests/test_m19_g6_demographic_subscriptions.py` | Yes — file pre-exists from G6 |
| Elasticity rows for `emergency_declaration` | NM-096 + #1729 ACs | `backend/tests/test_m19_g6_demographic_subscriptions.py` | Yes — file pre-exists from G6 |
| NM-056 fix (lines 231, 289) | NM-056 rule | `backend/tests/test_m19_g6_demographic_subscriptions.py` | Yes — test stubs pre-exist |

---

## Section 3 — Scope Declaration

### 3.0 — Scope lock confirmation

- [x] All ADR decisions affecting this sprint's scope are EL-approved and merged to `release/m19`

ADR-020 (DemographicModule transmission channels) accepted and merged. Elasticity values
are CM-certified (see §CM Certification below). No scope uncertainty.

### 3.1 — Issues in scope

| Issue | Title | Group | Priority |
|---|---|---|---|
| #1729 | fix(g6): add missing elasticity rows for imf_program_acceptance and emergency_declaration; fix NM-056 in G6 test file | G7 | **Immediate — Demo 8 pre-flight; silent correctness failure on live channels** |

### 3.2 — Issues explicitly out of scope

| Issue | Title | Horizon | Rationale for exclusion |
|---|---|---|---|
| #1711 | Demo 8 Act 2 verification: GRC AC-1 live harness run | Near-term | DATABASE_URL prerequisite only; no code changes; not a G7 deliverable |
| #1712 | Demo 8 Act 2 verification: ARG AC-1 live harness run | Near-term | DATABASE_URL prerequisite only |
| #1713 | Demo 8 Act 2 verification: PAK AC-1 live harness run | Near-term | DATABASE_URL prerequisite only |

---

## Section 4 — ADR Prerequisite Summary

| Group | ADR required | ADR status | Implementation may begin? |
|---|---|---|---|
| G7 | ADR-020 (prerequisite, not new) | Accepted (M19 G2D, merged to release/m19) | Yes — no new ADR required |

---

## Section 5 — Near-Miss Sweep

**Near-miss sweep date:** 2026-07-04
**Sweep period:** Since G6 close (2026-07-04)

| Finding | Category | PI Agent register call issued? | NM entry number |
|---|---|---|---|
| PR #1722 fixed dead subscription strings but omitted elasticity rows prescribed by NM-090/091 — partial implementation; G6 exit gate accepted false CI signal (7 PASS + 2 SKIP reported as 9/9 GREEN per NM-056 violation) | near-miss | Yes — NM-096 filed 2026-07-04 | NM-096 |

---

## Section 6 — Sprint Group Isolation

### 6.1 — Sprint sub-branch

| Field | Value |
|---|---|
| Sprint sub-branch | `sprint/m19-g7` |
| Cut from | `release/m19` |
| Sprint journal issue | TBD — PM Agent creates at EL approval |

**PM Agent sprint sub-branch cut command (execute after EL approval):**
```bash
git checkout -b sprint/m19-g7 release/m19 && git push -u origin sprint/m19-g7
```

### 6.2 — File-conflict risk assessment

| File | Lane required | Trigger |
|---|---|---|
| `SESSION_STATE.md` | PM Agent coordination lane | Sprint exit cockpit update |
| `docs/process/near-miss-registry.md` | PM Agent coordination lane (PI Agent authors) | NM-096 already filed |
| `backend/app/simulation/modules/demographic/elasticities.py` | Sprint sub-branch | 4 new elasticity rows |
| `backend/tests/test_m19_g6_demographic_subscriptions.py` | Sprint sub-branch | NM-056 fix (lines 231, 289) |

### 6.3 — Infrastructure dependency declaration

- [x] No DS-owned file changes required

No new output directories introduced by this sprint group.

### 6.4 — Cross-group dependency declaration

- [x] No cross-group dependencies

G7 writes only to backend code and test files. No overlap with any active sprint group
(all G1–G6 + CM-A/B/C are fully integrated to `release/m19`).

### 6.5 — Prior NM verification

**NM verification sweep date:** 2026-07-04
**Sweep period:** Since G6 close (2026-07-04)

| NM entry | Process improvement required | Applied in this sprint? |
|---|---|---|
| NM-056 | No `pytest.skip()` in test bodies — must FAIL (not SKIP) when rows absent | Yes — the two violations are the primary fix target in this sprint |
| NM-084 | CM sign-off on issue before PI gate comment before auto-merge | Yes — CM cert already on record (#1657 comment 2026-07-04); gate pre-cleared |
| NM-090 | Subscription string fix + elasticity rows in the same PR | Yes — G7 completes the NM-090 prescription that G6/PR #1722 partially fulfilled |
| NM-091 | Missing elasticity rows = silent zero-delta on live channels | Yes — G7 fixes this directly |
| NM-096 | Partial implementation detected at DS log analysis | Yes — G7 is the corrective action |

---

## CM Certification Record

CM values certified in issue #1657 comment (2026-07-04). No further CM consultation required.

| Event | Cohort | φ | Confidence tier | Source |
|---|---|---|---|---|
| `emergency_policy_imf_program_acceptance` | Q1 INFORMAL | +0.04 | T3 | IMF IEO (2018) mid-range 3–5pp |
| `emergency_policy_imf_program_acceptance` | Q2 INFORMAL | +0.02 | T3 | Ball et al. (2013) 0.60 scaling |
| `emergency_policy_emergency_declaration` | Q1 INFORMAL | +0.06 | T3 | ILO (2020) 20–25% informal contraction |
| `emergency_policy_emergency_declaration` | Q2 INFORMAL | +0.04 | T3 | Ball et al. (2013) 0.60 scaling |
| `entity_families` | — | None (universal) | — | CM cert |

NM-084 gate status: **PRE-CLEARED** — CM cert is on record before this entry is filed.

---

## BPO Assessment (2026-07-04)

**Verdict: PROCEED — M19 scope; HIGH priority; Demo 8 pre-flight**

**Demo 8 impact (CONDITIONAL blocker):** The Zambia Act 2 three-scenario comparison carries
a "+342K" cumulative cohort delta claim. If the demo scenario fires `imf_program_acceptance`
events (architecturally expected in a fiscal conditionality scenario), Q1 informal PHC is
understated by 4pp per affected step. The current figure is a lower bound that understates
human cost — contrary to the project's primary mission principle.

**North star test:** The Zambia Ministry of Finance team at the restructuring table asks: what
does programme acceptance do to Q1 informal poverty headcount? With the fix, the model shows
+4pp Q1 informal PHC on acceptance — consistent with the ILO/IMF empirical record for
informal workers facing austerity. The analyst can cite a specific calibrated cohort effect at
the acceptance step. Without the fix, the model shows zero. **PASS** (conditional on demo
scenario triggering the event).

**NM-056 severity:** The G6 exit was filed as "9/9 GREEN" when the correct state was
"7 PASS + 2 SKIP." The CI gate passed on a false signal. This is a compliance integrity
issue independent of Demo 8.

**Priority:** HIGH. Fix before Demo 8 internal review.

---

## EL Approval Record

**EL approval:** 2026-07-04

> G7 sprint entry approved. Sprint branch `sprint/m19-g7` cut from `release/m19`.
> Scope: 4 elasticity rows + NM-056 fix. CM values pre-certified on #1657. Implementation
> may begin. Sprint journal: #1732.
> — @PublicEnemage (2026-07-04)
