---
name: m19-g8-sprint-entry
type: sprint-entry
milestone: M19 — Constraint Search and Empirical Calibration
sprint-group: G8
status: pending EL approval
authored-by: PM Agent
authored-date: 2026-07-04
el-approved: pending
release-branch: release/m19
sop-reference: docs/process/sprint-planning-sop.md
---

# Sprint Entry — M19, Sprint Group G8

**Status:** Pending EL approval
**Date authored:** 2026-07-04
**Release branch:** `release/m19`
**Sprint plan:** `docs/process/sprint-plans/m19-sprint-plan.md`
**BPO evaluation:** 2026-07-04 — PROCEED verdict; HIGH priority; Demo 8 Act 2 blocker; see §BPO Assessment below

*Authority: `docs/process/sprint-planning-sop.md §Sprint Entry Gate` (Phase C output).*

---

## Section 1 — Sprint Identification

| Field | Value |
|---|---|
| Milestone | M19 — Constraint Search and Empirical Calibration |
| GitHub Milestone | #21 |
| Sprint number | G8 |
| Release branch | `release/m19` |
| Sprint plan document | `docs/process/sprint-plans/m19-sprint-plan.md` |
| Exit checklist issue | #1535 |
| Sprint groups in scope | G8 |
| Wave coordination tier | Standard — no concurrent active sprint groups at entry |
| Concurrent groups at entry | 0 of 5 max — all G1–G7 + CM-A/B/C integrated |
| Cross-group dependencies | None |

---

## Section 2 — Entry Invariants Checklist

### 2.1 — Structural gates

- [x] **Release branch exists:** `release/m19` — current; all G1–G7 + CM-A/B/C integrated
- [x] **CI trigger verified:** `.github/workflows/ci.yml` covers `release/m*` and `sprint/m*`
- [x] **Sprint plan EL-approved:** `m19-sprint-plan.md` has `el-approved: 2026-07-02` in frontmatter

### 2.2 — ADR prerequisite gate

- [x] No new ADR required. The fix is a bug correction to an accepted implementation:
  `_classify_direction` at `mode3_harness.py:358` accepts `primary_indicator` but the
  body never uses it. This is an implementation gap, not an architectural decision. No
  change to the interface contract or data model is required.

**ADR prerequisite status:**

| Group | Required ADR | ADR status | Gate |
|---|---|---|---|
| G8 | N/A — bug fix (implementation gap in existing function) | N/A | CLEAR |

### 2.3 — Intent document gate

This sprint is a **bug fix sprint**. The equivalent of an intent document is:

1. NM-098 near-miss entry (`docs/process/near-miss-registry.md`, 2026-07-04) documenting
   the root cause and prescribing the fix
2. Issue #1739 (filed 2026-07-04) with acceptance criteria and proposed code change
3. Issue #1711 comment (2026-07-04) recording GRC trajectory data confirming the fix path

No separate intent document is required: "Infrastructure sprint — bug fix restoring
correct primary_indicator semantics — intent artifacts satisfied by NM-098 and #1739 ACs."

**Intent document status:**

| Deliverable | ADR reference | Intent document path | Filed? |
|---|---|---|---|
| `_classify_direction` primary_indicator fix | N/A (bug fix) | NM-098 + #1739 ACs | Yes |

### 2.4 — QA test authorship gate

The CM Sprint A/B/C test files (`test_m19_cm_a/b/c_elasticity_calibration.py`) are the
acceptance tests. They call `run_harness(..., primary_indicator="hd_composite")` and assert
hd_composite-consistent bounds. After the fix, these tests exercise the correct code path.

Additional unit tests for `_classify_direction` must be authored or updated before implementation:
- New test: `primary_indicator="hd_composite"` uses hd_composite field
- New test: `primary_indicator="fin_composite"` uses fin_composite field
- Regression test: `primary_indicator=None` still uses PSP → fin_composite fallback

**QA test status:**

| Deliverable | Intent document | Test file path | Authored before implementation? |
|---|---|---|---|
| `_classify_direction` primary_indicator | NM-098 + #1739 | `backend/tests/test_mode3_harness.py` | Must be authored in this sprint before implementation PR |

---

## Section 3 — Scope Declaration

### 3.0 — Scope lock confirmation

- [x] All ADR decisions affecting this sprint's scope are EL-approved

### 3.1 — Issues in scope

| Issue | Title | Group | Priority |
|---|---|---|---|
| #1739 | fix(harness): _classify_direction ignores primary_indicator | G8 | **Immediate — Demo 8 Act 2 blocker; GRC #1711 cannot pass without this fix** |
| #1711 | Demo 8 Act 2 verification: GRC AC-1 live harness run | G8 | **Immediate — close after #1739 verified** |

### 3.2 — Issues explicitly out of scope

| Issue | Title | Horizon | Rationale for exclusion |
|---|---|---|---|
| #1712 | Demo 8 Act 2 verification: ARG AC-1 | Near-term | Separate fixture design constraint; requires CM consultation on baseline n_steps and bounds recalibration |

**Note on #1712 — CM consultation result (2026-07-04):** The CM Agent was activated
during this session to advise on Option A (extend baseline to n_steps=3) vs Option B
(change assertion step index). The CM approved Option A in principle. An empirical live
run was performed to calibrate expected bounds:

| Step | BL hd | CF hd | diff |
|------|-------|-------|------|
| 1 | 0.5464 | 0.6107 | 0.0643 |
| 2 | 0.3723 | 0.5393 | 0.1670 |
| 3 (extended BL, no inputs) | 0.3723 | 0.5750 | 0.2027 |

Finding: the engine produces **no recovery** at baseline step 3 without explicit
fiscal recovery inputs. BL hd_composite stays flat at the post-default trough (0.3723).
The step-3 diff (0.2027) is larger than step 2 — divergence widens, not converges.
The [0.003, 0.050] bounds are unachievable; the CM Sprint B AC-1 spec assumed convergence
behavior that requires explicit Kirchner recovery inputs at baseline step 3.

**This is a fixture design problem requiring a separate CM sprint (CM-D):**
- Design Kirchner 2003 recovery inputs for ARG baseline step 3 (fiscal loosening,
  debt restructuring parameters) with historical sourcing
- Re-run empirical calibration to observe actual step-3 diff with recovery inputs
- Certify bounds from observed value (±50% tolerance, T3 confidence tier)

G8 scope remains #1739 + #1711 only. ARG (#1712) requires CM-D.

---

## Section 4 — ADR Prerequisite Summary

| Group | ADR required | ADR status | Implementation may begin? |
|---|---|---|---|
| G8 | None — bug fix only | N/A | Yes, pending EL approval of this entry |

---

## Section 5 — Near-Miss Sweep

**Near-miss sweep date:** 2026-07-04
**Sweep period:** Since G7 close (2026-07-04)

| Finding | Category | PI Agent register call issued? | NM entry number |
|---|---|---|---|
| `_classify_direction` ignores primary_indicator; GRC Act 2 verification blocked | near-miss | Yes — NM-098 filed 2026-07-04 | NM-098 |

---

## Section 6 — Sprint Group Isolation

### 6.1 — Sprint sub-branch

| Field | Value |
|---|---|
| Sprint sub-branch | `sprint/m19-g8` |
| Cut from | `release/m19` |
| Sprint journal issue | #1741 |

**PM Agent sprint sub-branch cut command (execute after EL approval):**
```bash
git checkout -b sprint/m19-g8 release/m19 && git push -u origin sprint/m19-g8
```

### 6.2 — File-conflict risk assessment

| File | Lane required | Trigger |
|---|---|---|
| `SESSION_STATE.md` | PM Agent coordination lane | Sprint exit cockpit update |
| `backend/app/harness/mode3_harness.py` | Sprint sub-branch | `_classify_direction` fix |
| `backend/tests/test_mode3_harness.py` | Sprint sub-branch | New/updated unit tests for primary_indicator branch |

### 6.3 — Infrastructure dependency declaration

- [x] No DS-owned file changes required

### 6.4 — Cross-group dependency declaration

- [x] No cross-group dependencies

G8 writes only to harness code and test files. No overlap with any other sprint.

### 6.5 — Prior NM verification

**NM verification sweep date:** 2026-07-04

| NM entry | Process improvement required | Applied in this sprint? |
|---|---|---|
| NM-098 | Accepted parameters must be used or documented as reserved | Yes — this sprint implements the fix NM-098 prescribed |
| NM-097 | CM test skip guard should verify data presence | Deferred — NM-097 fix requires DATABASE_URL seeding work; out of scope for G8 |

---

## BPO Assessment (2026-07-04)

**Verdict: PROCEED — M19 scope; HIGH priority; Demo 8 Act 2 pre-flight**

**Demo 8 impact (BLOCKER):** The Demo 8 Act 2 narrative demonstrates that calibrated
elasticity values produce measurable hd_composite divergence between scenario and
counter-factual. For GRC, this divergence (0.1561 at step 4) is visible only in
hd_composite — not in fin_composite. Without the primary_indicator fix, the harness
always reports INDISTINGUISHABLE for GRC, making the Act 2 demonstration impossible.

**North star test:** The Zambia/GRC analyst at a restructuring session asks: "Does a smaller
IMF programme (0.30 vs 0.48 GDP ratio) produce meaningfully better human development outcomes?"
The GRC counter-factual fixture answers this. After the fix, the harness correctly measures
hd_composite divergence (0.1561 at step 4), confirming the calibrated difference is
instrument-visible. The analyst can point to a specific measured gap. Without the fix, the
harness reports zero divergence — undermining the core demonstration.

**Priority:** HIGH. Must be delivered before Demo 8 Act 2 live verification.

---

## EL Approval Record

**EL approval:** pending
