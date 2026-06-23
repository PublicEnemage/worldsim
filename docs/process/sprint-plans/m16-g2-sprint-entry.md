---
name: m16-g2-sprint-entry
type: sprint-entry
milestone: M16 — Distributional Visibility
sprint-group: G2
status: EL Approved 2026-06-23 — QA tests must be filed before implementation PR opens
authored-by: PM Agent
authored-date: 2026-06-23
el-approved: 2026-06-23
release-branch: release/m16
sop-reference: docs/process/sprint-planning-sop.md
---

# Sprint Entry — M16, G2: Distributional Visibility on Primary Surface

**Status:** Filed — awaiting EL approval before implementation begins
**Date authored:** 2026-06-23
**Release branch:** `release/m16`
**Sprint plan:** `docs/process/sprint-plans/m16-sprint-plan.md` (EL Approved 2026-06-23)

*Authority: `docs/process/sprint-planning-sop.md §Sprint Entry Gate` (Phase C output).
G2 covers cohort disaggregation (#986), political risk summary surface (#987), and PSP threshold
legibility (#1163, resolved by #987). No implementation PR may open against `release/m16` for
G2 until this entry document is EL-approved and the intent document and QA tests are filed.
G2 may not open its implementation PR until G1 is confirmed merged and BPO-accepted — this
sequencing invariant is enforced by the branch gate in Section 2.1.*

---

## Section 1 — Sprint Identification

| Field | Value |
|---|---|
| Milestone | M16 — Distributional Visibility |
| GitHub Milestone | #17 |
| Sprint group | G2 — Distributional Visibility on Primary Surface |
| Release branch | `release/m16` |
| Sprint plan document | `docs/process/sprint-plans/m16-sprint-plan.md` |
| Exit checklist issue | #985 |
| Sprint groups in scope | G2 only |
| ADR gate | ADR-017 ✅ (accepted 2026-06-22); ADR-015 ✅ (accepted 2026-06-16); No new ADR required |
| Implementing agent | Frontend Architect Agent |
| Wave | Wave 2 — depends on G1 (sequential); gates G8 (live stakeholder demo) |

---

## Section 2 — Entry Invariants Checklist

*All items must be checked before any implementation PR is opened for G2.
An unchecked invariant blocks implementation from beginning.*

### 2.1 — Structural gates

- [x] **Release branch exists:** `release/m16` — confirmed present and CI-protected (see G1
  sprint entry §2.1 for Ruleset verification).
- [x] **G1 merge gate (G2 sequencing invariant):** G1 (#845 and #1147) is merged to
  `release/m16` (PR #1160, 2026-06-23) and BPO-accepted (Step 5 Validate complete 2026-06-23).
  G2 implementation PR may now target `release/m16`.
- [x] **Sprint plan EL-approved:** `docs/process/sprint-plans/m16-sprint-plan.md`
  `el-approved: 2026-06-23` (PR #1148 merged 2026-06-23). G2 row updated to include #1163
  (PR #1166 merged 2026-06-23).

### 2.2 — Domain pre-conditions gate

Six domain pre-conditions were required before G2 sprint entry could be filed. All six are
satisfied as of 2026-06-23.

| # | Pre-condition | Who | Status | Evidence |
|---|---|---|---|---|
| 1 | Chief Methodologist sign-off on #986 cohort scope | CM | ✅ 2026-06-23 | `cohort-disaggregation-design.md §Review Acknowledgments` |
| 2 | Data Architect sign-off on DemographicModule output | DA | ✅ 2026-06-23 | GitHub issue #986 comment; scope restricted to poverty_headcount_ratio Q1/Q2 only |
| 3 | Architecture Review Facilitator sign-off on #986 (AC-1–AC-6) | ARF | ✅ 2026-06-23 | `cohort-disaggregation-design.md §Review Acknowledgments` |
| 4 | Chief Methodologist sign-off on #987 PSP severity thresholds | CM | ✅ 2026-06-23 | `political-risk-summary-design.md §Review Acknowledgments` |
| 5 | Architecture Review Facilitator sign-off on #987 (AC-7–AC-11) | ARF | ✅ 2026-06-23 | `political-risk-summary-design.md §Review Acknowledgments` |
| 6 | Frontend Architect brief with UX Designer sign-off — Zone 1D layout | FA + UXD | ✅ 2026-06-23 | `docs/frontend/fa-brief-m16-g2-zone-1d-layout.md` |

**Pre-condition 6 detail:** The FA discovered that Zone 1D was already overflowing post-G1
(148px content in 96px container). G2 could not simply add the political risk sub-section.
The FA brief specifies new proportion constants (1280: 35%/15%/50%), the replacement mandate
(G1 PSP elements retired, not supplemented), and Zone 1D font/spacing spec. UX Designer
accepted the Zone 1B 1280 visible-row regression (1+1 vs. design spec 2+2). This is the only
UX regression introduced; it is named and documented.

### 2.3 — ADR prerequisite gate

G2 is fully within the accepted scope of ADR-017 (Zone 1A/1D Information Architecture) and
ADR-015 (Model Legibility Architecture). No new ADR is required.

| Issue | Required ADR | Status | Gate |
|---|---|---|---|
| #986 — Cohort disaggregation (Zone 1B) | ADR-017 is not required (Zone 1B independent of Zone 1A); ADR-014 (Alert Panel) covers Zone 1B extension | ADR-014 accepted | **CLEAR** |
| #987 — Political risk sub-section (Zone 1D) | ADR-017 (Zone 1D Integration — existing accepted contract); ADR-015 (evidence thread pattern) | Both accepted | **CLEAR** |
| #1163 — PSP threshold legibility | Resolved by #987 design; no new ADR | N/A | **CLEAR** |

- [x] All G2 ADR prerequisites are clear. Both ADR-014 and ADR-017/ADR-015 are accepted.
  No new ADR is required per ARF confirmation (both design documents' ADR disposition sections).
  Gate: **CLEAR**.

### 2.4 — Intent document gate

*An intent document must be filed before any G2 implementation PR opens.
(Authority: `docs/process/agent-execution-lifecycle.md Step 1`)*

- [x] Intent document filed for G2 deliverables — **FILED 2026-06-23**

| Deliverable | Intent document path | Filed? |
|---|---|---|
| #986 — Cohort disaggregation on primary surface | `docs/process/intents/M16-G2-2026-06-23-distributional-surface.md` | ✅ Filed 2026-06-23 |
| #987 — Political risk summary surface | (same intent document) | ✅ Filed 2026-06-23 |
| #1163 — PSP threshold legibility | (resolved by #987 within the same document) | ✅ Filed 2026-06-23 |

All three issues are covered by a single intent document. #986 and #987 are co-primary
deliverables in the same G2 PR; #1163 closes as a consequence of #987 (PSP severity labels
are the threshold indicator #1163 requested — no separate implementation required).

### 2.5 — QA test authorship gate

*QA tests must be authored from the intent document's acceptance criteria before
implementation code is written. (Authority: `docs/process/agent-execution-lifecycle.md Step 2`)*

- [ ] QA test files authored for G2 before implementation begins — **PENDING**

| Deliverable | Test file path | Authored before implementation? |
|---|---|---|
| #986 — Cohort disaggregation (Zone 1B) | `frontend/tests/e2e/m16-g2-distributional-surface.spec.ts` | ⬜ Pending |
| #987 — Political risk sub-section (Zone 1D) | (same spec file) | ⬜ Pending |
| G1 test updates (retired testids) | `frontend/tests/e2e/m16-g1-zone-1a-phase4-composite.spec.ts` | ⬜ Pending (G2 PR retires 4 G1 testids — QA Lead must update G1 spec before G2 implementation PR opens) |

**Soft-skip guard (NM-056 follow-up):** The QA test files must contain no `test.skip()` or
conditional skip patterns. Any test scenario requiring a backend fixture not yet available must
fail explicitly. The M16 sprint exit checklist confirms no active soft-skip patterns before
#985 closes.

**G1 testid retirement (FA brief requirement):** The G2 implementation retires 4 testids
from FourFrameworkZone1D.tsx: `zone-1d-political-feasibility`, `psp-delta`,
`psp-layer3-sentence`, `psp-delta-sentence`. The QA Lead must update G1 Playwright tests
to use replacement testids BEFORE the G2 implementation PR opens — otherwise G1 ACs become
silent passes (element not found). This is the same failure mode as NM-056.

---

## Section 3 — Scope Declaration

### 3.1 — Issues in scope

| Issue | Title | Priority | Observable application state (pre-implementation specification) |
|---|---|---|---|
| #986 | feat(ux): cohort disaggregation on primary surface | immediate | At 1280×800 with the ZMB ECF Mode 2 scenario advanced to step 2 with political economy enabled: Zone 1B shows a "COHORT IMPACT" sub-section below the MDA aggregate alerts, separated by a labeled horizontal rule. The sub-section shows a CRITICAL row for "Bottom income quintile — Poverty headcount" with format "CRITICAL · Bottom income quintile — Poverty headcount · Threshold crossed at step 2 · was X% above floor · T3 · [source]". Q3, Q4, Q5 cohorts are NOT shown — they are suppressed (T5 — no elasticity data). All tier labels show "T3" (not "T2"). In Mode 1, the sub-section header reads "COHORT IMPACT (HISTORICAL)". When no cohort crosses a threshold, the sub-section shows "No cohort threshold crossings projected on current path." (Mode 2) or "No cohort threshold crossings at or before this step." (Mode 1). At 1280×800: 1 cohort row visible without scroll (revised per FA brief DD-016); at 1440×900: 2 cohort rows visible without scroll. |
| #987 | feat(ux): political risk summary surface (Persona 3) | immediate | At 1280×800 with the ZMB ECF Mode 2 scenario advanced to step 3 (PSP=0.38, political economy enabled): Zone 1D shows a "POLITICAL RISK" sub-section below the four-framework rows, separated by a labeled horizontal rule. The sub-section shows: "Programme survival: CRITICAL (38%) — DECLINING", "At this level, historical ECF programmes show abandonment within 3 steps.", "Legitimacy index: 0.42 — declining (floor: 0.35)", "0.07 above fragility threshold", "Elite capture divergence: widening — fiscal benefits concentrating". The G1 testids `zone-1d-political-feasibility`, `psp-delta`, `psp-layer3-sentence`, `psp-delta-sentence` are absent from the DOM (retired). PSP severity thresholds: CRITICAL < 0.40, WARNING 0.40–0.55, WATCH 0.55–0.70, STABLE > 0.70. Historical analogue sentence: CRITICAL shows "within 3 steps"; WARNING shows "within 6 steps". When political economy is not enabled: "Political risk: not modelled in this fixture." Zone 1D flex proportion at 1280 is 50% of chartHeight (160px). All four framework rows remain visible without scroll. |
| #1163 | ux(zone-1d): PSP threshold anchor — absolute PSP level legibility for Persona 3 | immediate | Closed by #987 implementation. The "CRITICAL (38%)" severity-labeled display answers the #1163 requirement: Persona 3 can now interpret the absolute PSP level (38%) as "critical range" without knowing the threshold value. No separate implementation required — #1163 closes when #987 implementation is merged. |

### 3.2 — Issues explicitly out of scope

| Issue / scope | Rationale for exclusion |
|---|---|
| #986 age-band cohort disaggregation (under-5, under-18) | DA sign-off established M16 scope is poverty_headcount_ratio by income quintile only. DemographicModule has no under-5 or under-18 age-band outputs. School enrollment and child malnutrition deferred to M17. |
| Q3/Q4/Q5 cohort rows (non-suppressed display) | No elasticity rows in ELASTICITY_REGISTRY for Q3–Q5. These quintiles produce zero delta — display would be misleading. Suppressed as T5. Cohort-specific floor calibration for Q3–Q5 is M17 scope. |
| Gender cohort disaggregation | Explicitly deferred to M17 in design spec — no calibrated coefficients available |
| Subnational / regional cohort disaggregation | Deferred to M17+ — requires GIS integration not in current data architecture |
| Zone 1D per-framework delta vs. baseline (+0.04 notation) | G1 Customer Agent Layer 3 C3 gap — scope to future sprint; not a G2 deliverable |
| #987 Mode 3 PSP direction reversal marker "(reversal from previous input)" | G2 scope restriction: implement Mode 1 and Mode 2 display contracts first. Mode 3 reversal marker is an enhancement over baseline; defer to G2b if capacity allows |
| Zone 1D interactive expand mode (L1/L2 cross-examination) | ADR-015 interactive expand mode is a separate deliverable; G2 delivers L0 (zero-interaction) political risk display |
| Any new backend API endpoints | G2 is frontend-only. Cohort threshold data is derived from existing DemographicModule trajectory output. Political risk data is derived from existing political economy module trajectory output. No new endpoints. |
| G3 (25-year human capital trajectory) | Separate sprint with separate entry document |

G2 is complete when: all observable application states in Section 3.1 are confirmed in the
running application at Step 4 Verify; Customer Agent Layer 3 assessment is on record (required
for Persona 2 and Persona 3 capabilities); and the Business PO confirms at Step 5 Validate that
Persona 2 can form the cohort argument ("Bottom income quintile crosses poverty headcount
threshold at step 2") from Zone 1B without specialist mediation, and Persona 3 can read the
political risk situation from Zone 1D within 30 seconds without specialist mediation.

---

## Section 4 — ADR Prerequisite Summary

| Issue | ADR | Status | Implementation may begin? |
|---|---|---|---|
| #986 (Zone 1B cohort impact) | ADR-014 (Alert Panel Zone 1B) — covers Zone 1B extension | Accepted (M13-G7) | After EL approves this entry, intent filed, QA tests authored |
| #987 (Zone 1D political risk) | ADR-017 (Zone 1D Integration); ADR-015 (evidence thread) | Both accepted | (same gate) |
| #1163 (PSP threshold legibility) | None — resolved by #987 | N/A | Closes when #987 PR merges |

**Implementation sequencing for G2:**

1. EL approves this entry document (this step)
2. QA Lead Agent authors `frontend/tests/e2e/m16-g2-distributional-surface.spec.ts` from the
   G2 intent document acceptance criteria, AND updates
   `frontend/tests/e2e/m16-g1-zone-1a-phase4-composite.spec.ts` for the 4 retired testids
   (FA brief §Replacement Mandate). Both files authored before any G2 implementation code.
3. Implementation PR opens targeting `release/m16` with name `feat/m16-g2-distributional-surface`
4. Implementation must: (a) rebalance Zone 1D/1C/1B flex proportions per DD-016; (b) replace
   G1 Zone 1D PSP elements with structured political risk sub-section; (c) add Cohort Impact
   sub-section to Zone 1B
5. Frontend Architect Agent Step 4 Verify: confirms all observable application states present;
   confirms all 4 G1 testids are absent from DOM; confirms Zone 1D proportion is 50% at 1280
6. Customer Agent Layer 3 assessment required before BPO verdict — Persona 2 (#986 cohort
   argument) and Persona 3 (#987 political risk read) both served
7. Business PO Step 5 Validate: confirms (a) Persona 2 can form the cohort argument from Zone
   1B at L0; (b) Persona 3 can read full political risk situation from Zone 1D within 30 seconds;
   (c) #1163 closed (PSP level is self-interpreting via severity label)

**G8 gate dependency:** G8 (live stakeholder demo #843 — M16 exit gate) may not open until
G1, G2, and G3 are all BPO-accepted. G2 merge is a necessary but not sufficient condition for G8.

---

## Section 5 — Near-Miss Sweep

**Near-miss sweep date:** 2026-06-23
**Sweep period:** G1 BPO acceptance (2026-06-23) through G2 sprint entry filing (2026-06-23)

| Finding | Category | Action |
|---|---|---|
| Zone 1D overflow condition (52px post-G1) was present from G1 merge but not detected by any AC in the G1 test suite. Silent regression: `overflow:hidden` clipped content without test failure. | Near-miss precursor — no NM filed (condition caught at G2 pre-conditions, before it caused user-visible harm) | FA brief documents overflow finding; DD-016 specifies corrected proportions; overflow-y:auto added as prevention. No NM filed because the overflow was caught in pre-conditions — it never reached a shipped state or a user. If it had reached Step 4 Verify and passed, it would be NM-worthy. |
| G1 testid retirement (4 testids) creates silent-pass risk in G1 Playwright tests if not updated before G2 implementation PR opens. This is the same failure mode as NM-056. | Process risk | FA brief explicitly names 4 affected G1 ACs and requires QA Lead to update G1 test spec before G2 implementation PR opens (Section 2.5 QA gate). No new NM filed — NM-056 already covers this pattern; applying NM-056 countermeasure here. |
| CM sign-off on #987 specifies "WARNING historical analogue sentence should use 'within 6 steps'" — this is a correction to the design doc placeholder. | Scope clarification | Design document already updated to reflect CM-specified values. No process gap. |

---

## EL Approval Record

**EL approval:** 2026-06-23

> G2 sprint entry approved. All 6 pre-conditions confirmed satisfied: CM, DA, ARF sign-offs on #986 and #987; FA brief with UX Designer sign-off filed (DD-016). ADR prerequisites clear for all three issues (ADR-014, ADR-017, ADR-015 all accepted; no new ADR required). Observable application states in Section 3.1 are specific enough to gate QA test authorship. Zone 1B 1280 viewport regression (1+1 visible without scroll vs. design spec 2+2) is accepted per UX Designer sign-off in FA brief — named, not hidden. G1 testid retirement requirement (4 testids, QA Lead must update G1 spec before G2 implementation PR opens) noted and accepted as a QA gate condition in Section 2.5. #1163 closes as a consequence of #987 AC-8 — no separate implementation required. G8 gate dependency (#843 may not open until G1+G2+G3 are BPO-accepted) noted. Implementation may proceed once QA tests are authored and filed.
> — @PublicEnemage (2026-06-23)
