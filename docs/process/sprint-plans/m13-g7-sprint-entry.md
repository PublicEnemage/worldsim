---
name: m13-g7-sprint-entry
type: sprint-entry
milestone: M13 — Political Economy and Instrument Credibility
sprint-group: G7
status: Filed — awaiting EL approval before implementation begins
authored-by: PM Agent
authored-date: 2026-06-12
el-approved: false
release-branch: release/m13
sop-reference: docs/process/sprint-planning-sop.md
adr-gate: ADR-014 — ACCEPTED 2026-06-12 (PR #926)
---

# Sprint Entry — M13, G7: Alert Panel Master-Detail UX

**Status:** Filed — awaiting EL approval before implementation begins
**Date authored:** 2026-06-12
**Release branch:** `release/m13`
**Sprint plan:** `docs/process/sprint-plans/m13-sprint-plan.md`

*Authority: `docs/process/sprint-planning-sop.md §Sprint Entry Gate` (Phase C output).
This document gates G7 specifically. The M13 Sprint 1 entry (`m13-sprint-1-entry.md`)
listed G7 as `BLOCKED_ADR`. ADR-014 was accepted 2026-06-12 (PR #926); this entry
document satisfies the unblock condition stated in the Sprint 1 entry before
implementation may begin.*

---

## Section 1 — Sprint Identification

| Field | Value |
|---|---|
| Milestone | M13 — Political Economy and Instrument Credibility |
| GitHub Milestone | #9 |
| Sprint number | 1 (Wave 3 — G7 unblock entry) |
| Release branch | `release/m13` |
| Sprint plan document | `docs/process/sprint-plans/m13-sprint-plan.md` |
| Exit checklist issue | #264 |
| Sprint groups in scope | G7 only |
| ADR gate cleared | ADR-014 — ACCEPTED 2026-06-12 (PR #926) |
| Implementing agent | Frontend Architect Agent (per ADR-014 panel) |

---

## Section 2 — Entry Invariants Checklist

*All items must be checked before any implementation PR is opened for G7.
An unchecked invariant blocks implementation from beginning.*

### 2.1 — Structural gates

- [x] **Release branch exists:** `release/m13` cut from `main` 2026-06-12 (verified in M13 Sprint 1 entry)
- [x] **CI trigger verified:** `.github/workflows/ci.yml` `pull_request: branches` includes
  `release/m*` — confirmed at M13 kickoff (pre-existing NM-035 fix)
- [x] **Sprint plan EL-approved:** `docs/process/sprint-plans/m13-sprint-plan.md` approved 2026-06-12

### 2.2 — ADR prerequisite gate

The M13 Sprint 1 entry listed G7 as `BLOCKED_ADR` (alert panel ADR PENDING_NUMBER). ADR-014
was authored, accepted, and merged 2026-06-12. This gate is now CLEAR.

| Group | Required ADR | ADR status | Gate |
|---|---|---|---|
| G7 | ADR-014 — alert panel master-detail | ACCEPTED 2026-06-12 (PR #926) | **CLEAR** |

- [x] G7's ADR prerequisite is satisfied. ADR-014 status: `Accepted`.

### 2.3 — Intent document gate

*Intent document must be filed at `docs/process/intents/ADR-014-YYYY-MM-DD-alert-panel-ux.md`
before any G7 implementation PR opens.*
*(Authority: CLAUDE.md §Agent Execution Lifecycle Step 1)*

- [ ] Intent document filed for G7 alert panel UX deliverable — **BLOCKING IMPLEMENTATION**

| Deliverable | ADR reference | Intent document path | Filed? |
|---|---|---|---|
| G7 — Alert panel Zone 1B persistent-detail (#852) | ADR-014 | `docs/process/intents/ADR-014-2026-06-12-alert-panel-ux.md` | No — must file before G7 PR opens |

**Three mandatory elements from UX Designer conditional sign-off (ADR-014 §UX Implication Statement):**
The intent document must include explicit specification for all three UX Designer sign-off
conditions before any implementation PR opens. A G7 PR opened without these in the intent
document is a process violation.

1. **Compact row height constraint** — max 26px per row (single-line truncated) to preserve
   "top 1–3 visible without scroll" at 1024×768 minimum viewport
   (Reference: UX-1 / `docs/ux/information-hierarchy.md §1B`)
2. **Mode-dependent tense in detail slot** — explicit specification of how "BREACHED" / "N%
   above floor" status language is mode-contextualized per `information-hierarchy.md §1B`
   ("Alert tense is mode-dependent") (Reference: UX-2)
3. **Compact row cohort omission** — explicit documentation that compact rows are exempt from
   `information-hierarchy.md §1B` "top affected cohort" requirement, with rationale. Ruling
   already recorded in ADR-014: compact rows are a severity-rank scan surface, not an evidence
   surface. Intent document must document the deviation and cite the ruling. (Reference: UX-7)

### 2.4 — QA test authorship gate

*QA tests must be authored from the intent document's acceptance criteria before implementation
code is written.*
*(Authority: CLAUDE.md §Agent Execution Lifecycle Step 2)*

- [ ] QA test file authored for G7 before implementation begins — **BLOCKING IMPLEMENTATION**

| Deliverable | Intent document | Test file path | Authored before implementation? |
|---|---|---|---|
| G7 — Alert panel (#852) | `docs/process/intents/ADR-014-2026-06-12-alert-panel-ux.md` | `frontend/tests/` — Zone 1B Playwright spec | No — must be authored after intent document is filed, before implementation PR opens |

**Required test coverage (from ADR-014 acceptance criteria and silent failure modes):**

The QA Lead authors tests covering the four observable application states from the ADR:

- **UX-3 acceptance criterion:** Playwright — Greece 2012 fixture at step 4; assert
  `data-testid="zone-1b-top-detail"` is visible within Zone 1B bounds, `detail-indicator-name`
  non-empty, `detail-current-value` non-empty numeric — no click or scroll between fixture
  load and assertion
- **UX-6 acceptance criterion:** Playwright — fixture with ≥1 TERMINAL alert; assert
  `data-testid="zone-1b-top-detail"` has `data-severity="TERMINAL"` and is visible at 1440×900
  without any click or scroll events; bounding-box assertion confirms within Zone 1B bounds
- **Silent failure 1:** Assert `data-testid="zone-1b-top-detail"` has `clientHeight > 0`
  immediately after fixture load at 1024×768, 1280×800, and 1440×900 — no user interactions
- **Silent failure 2:** Advance scenario one step; assert `data-testid="detail-consecutive"`
  text matches current step's `consecutive_breach_steps` for the top-ranked alert
- **Silent failure 3:** Assert no compact row (`data-testid="compact-alert-row"`) has cursor
  style other than `default`; assert clicking a compact row produces no change to
  `data-testid="zone-1b-top-detail"` content
- **Silent failure 4 (Mode 3):** Fire a control input causing a new highest-severity alert;
  assert `data-testid="detail-new-badge"` is present and visible before any user interaction

---

## Section 3 — Scope Declaration

### 3.1 — Issues in scope

| Issue | Title | Group | Priority |
|---|---|---|---|
| #852 | ux: alert panel (Zone 1B) needs master-detail layout | G7 | near-term |

### 3.2 — Issues explicitly out of scope

All other M13 issues are either complete (G1–G6) or in the near-term backlog. No
additional issues are being added to G7. Alert panel scope is bounded by ADR-014:
Zone 1B persistent-detail + scan-only compact list layout. Per-cohort income disaggregation
beyond the `cohort` subheader field, full provenance disclosure, and sparkline are
explicitly excluded from G7 per ADR-014 §Known Limitations and §Detail Slot Content.

| Issue | Rationale for exclusion |
|---|---|
| #22, #35, #102, #271, #274, #393, #394, #823, #824, #837 | Near-term backlog — not in any wave; revisit at M13 midpoint HORIZON sweep |

---

## Section 4 — ADR Prerequisite Summary

| Group | ADR required | ADR status | Implementation may begin? |
|---|---|---|---|
| G7 | ADR-014 | ACCEPTED 2026-06-12 (PR #926) | **Yes — after EL approves this entry document, intent document is filed, and QA tests are authored** |

**Implementation sequencing for G7:**
1. EL approves this entry document (this step)
2. Frontend Architect Agent authors intent document at `docs/process/intents/ADR-014-2026-06-12-alert-panel-ux.md` — must include all three UX Designer sign-off conditions
3. QA Lead authors test file before implementation PR opens
4. Implementation PR opens targeting `release/m13`
5. Viewport verification required before PR is marked ready for review (per ADR-014 §Height Budget): actual Zone 1B computed height at 1024×768, 1280×800, and 1440×900 must be measured and confirmed
6. Business PO Step 5 Validate and Customer Agent Layer 3 assessment required before sprint exit

---

## Section 5 — Near-Miss Sweep

**Near-miss sweep date:** 2026-06-12
**Sweep period:** Since M13 Sprint 1 entry filed (2026-06-12, same session)

| Finding | Category | PI Agent register call issued? | NM entry number |
|---|---|---|---|
| None — G7 was correctly listed as BLOCKED_ADR in Sprint 1 entry; ADR-014 authored and accepted in same session; no process gap identified in the G7 unblock sequence | N/A | N/A | N/A |

*Note on NM-042 and UX Designer sign-off:* NM-042 (structured sign-off attestation, PR #930)
amended the UX Designer sign-off protocol to require four named fields: Reviewing agent, Session
context, Governing documents reviewed (named sections), and Concerns found. ADR-014's sign-off
block was authored in the pre-NM-042 format and was updated to the four-field structured
attestation form as a housekeeping step at sprint entry filing (2026-06-12), before any
implementation PR was opened. The updated sign-off reads: `Same session as ADR authorship —
acknowledged`; seven governing document sections named; three concerns on record. EL is required
to verify the governing document citations (named sections, not generic references) at ADR
acceptance, per CLAUDE.md §UX Designer sign-off. No further near-miss action required for G7
from NM-042.

---

## EL Approval Record

**EL approval:** Pending

> {EL approval statement — to be filled at approval time}
> — @PublicEnemage ({date})
