---
name: m13-sprint-plan
type: sprint-plan
milestone: M13 — Political Economy and Instrument Credibility
status: Approved
authored-by: PM Agent
authored-date: 2026-06-12
el-approved: 2026-06-12
consulted-agents:
  - Business Product Owner (value prioritization)
  - Frontend Architect (file area grouping)
  - Chief Engineer (backend dependency sequencing)
  - Architect (ADR prerequisites)
sop-reference: docs/process/sprint-planning-sop.md
---

# M13 Sprint Plan — Political Economy and Instrument Credibility

**Status:** Draft — awaiting EL approval before any implementation PR opens
**Release branch:** `release/m13` (cut from `main` 2026-06-12)
**Exit checklist issue:** #264
**Primary objective:** Make "Can this government actually deliver this programme?" answerable
at the negotiating table. Political economy module live. Instrument legibility demo-ready.

---

## Four-Agent Consultation Summary

Before grouping, PM Agent ran four consultations per `docs/process/sprint-planning-sop.md`.
Findings are incorporated into the grouping decisions below.

**Business Product Owner (value prioritization):**
Highest user value: G1 legibility first (if unreadable at presentation scale, everything else
is moot), then G2 trajectory/Mode 3 comparison (Mode 3 A/B comparison is the differentiated
capability), then G6 political economy (primary M13 analytical gap closure). If scope must be
cut under time pressure: G4 documentation and G3 reserves fix are lowest risk to defer. G3
is low-effort and high-correctness-value — keep unless forced. G4 can be deferred to early M14.

**Frontend Architect (file area grouping):**
G1 (Zone 1 CSS/layout, alert panel positioning) and G2 (TrajectoryView, PMM component,
multi-entity chart rendering) touch different component trees — no merge conflict risk.
G6 political economy may need a G6a/G6b split (backend/frontend) if the diff exceeds ~800
lines after ADR-013 defines the scope. Defer the split decision to ADR-013 acceptance.

**Chief Engineer (backend dependency sequencing):**
G3 (#799) is independent — pure attribute update fix, no schema changes. G6 (#392) builds on
the existing PoliticalEconomyModule from M11 G16a/G16b and must wait for ADR-013 to define
the constraint modeling boundary. No hidden schema dependencies between G3 and G6. G6 may
require schema migration if ADR-013 adds new political_context fields — assess at ADR-013
acceptance.

**Architect (ADR prerequisites):**
ADR-013: ASSIGNED (number 13, per `docs/architecture/backlog.md` ARCH-007). Panel confirmed:
Architect Agent (author), Political Economist, Chief Methodologist, Engineering Lead. Begin
drafting immediately — this is the critical path for G6.
Alert panel ADR: NOT YET IN BACKLOG. New GitHub issue must be filed before a backlog entry
can be created and a number assigned. Scope gap flagged in §HORIZON Sweep below.
All other groups (G1–G4): no new ADR required.

---

## HORIZON Sweep — M13 Scope Completeness

Run against `CLAUDE.md §Milestone 13` and `docs/roadmap/worldsim-roadmap.md §Milestone 13`.

| Roadmap deliverable | Issue | Status |
|---|---|---|
| ADR-013 authored and accepted | #792 | Tracked ✓ |
| Political economy module (conditionality, elite capture, political feasibility) | #392 | Tracked ✓ |
| Alert panel UX (Zone 1B) master-detail | #852 | Tracked ✓ |
| Alert panel ADR (gates #852 implementation) | **UNTRACKED** | **scope-gap — see below** |
| Instrument legibility — DEMO-059 (#871) | #871 | Tracked ✓ |
| Instrument legibility — DEMO-060 (#872) | #872 | Tracked ✓ |
| Instrument legibility — DEMO-061 (#874) | #874 | Tracked ✓ |
| Instrument legibility — DEMO-062 (#873) | #873 | Tracked ✓ |
| Instrument legibility — DEMO-063 (#875) | #875 | Tracked ✓ |
| Instrument legibility — DEMO-064 (#876) | #876 | Tracked ✓ |
| Process Redesign Phase A deliverables | — | COMPLETE (all phases 0–D closed PR #906) |

**Scope gap — Alert panel ADR:** The EL decision (2026-06-11) on #852 requires "Frontend
architecture review + ADR + UX Designer + Design Thinking agent input before implementation."
The ADR has no GitHub issue and no backlog entry. This is `scope-gap:untracked`. Action at
kickoff: file GitHub issue for "docs(adr): alert panel master-detail UX architecture" and add
PENDING_NUMBER entry to `docs/architecture/backlog.md`.

---

## Grouping Rationale

Issues are grouped by shared file area first, then by dependency. DEMO-059–064 issues are
split across two groups: G1 handles CSS/layout fixes (low risk, short feedback cycle); G2
handles chart rendering and Mode 3 data-flow issues (higher complexity, longer cycle). This
split keeps each PR reviewable and avoids coupling a simple CSS fix to a complex chart change.

Documentation issues are batched in G4 — none require code review, and they can progress in
parallel with all Wave 1 groups.

G5 (ADR-013 authorship) is Wave 1 work but gates Wave 2. It is not blocked by any other group.
Begin immediately — the critical path is ADR-013 acceptance → G6 implementation.

G7 (alert panel) is blocked until its own ADR is authored, accepted, and has an EL-approved
UX design. It is listed as a separate blocked group — not in any wave until that gate clears.

---

## Wave 1 — Parallel (no inter-group dependencies)

### G1 — DEMO Legibility Fixes

**Issues:** #872 (DEMO-060), #874 (DEMO-061)
**Type:** Frontend CSS/layout fix
**ADR prerequisite:** None

**Why grouped:** Both issues are CSS/layout defects in Zone 1 components. DEMO-060 is the
CRITICAL FIN alert clipping below the Zone 1B boundary; DEMO-061 is the instrument cluster
and alert panel unreadable at 1440×900 presentation scale. Both are fixed in layout stylesheets
and component sizing — same file area, low merge risk.

**Shared files:** `frontend/src/` — Zone 1B styles, instrument cluster CSS/size constraints

**Tests required:**
- Playwright assertion: CRITICAL FIN alert fully visible within Zone 1B viewport at 1440×900
- Playwright assertion: instrument cluster text is legible (font-size ≥ threshold) at 1440×900

**Acceptance gate (Business PO Validate step):**
Persona 2 (Finance Ministry Negotiator) opens the Hormuz scenario at step 5 at 1440×900 and
can read the CRITICAL FIN alert text without scroll. Instrument cluster indicators are readable
without zoom. P-4 time ceiling: 90 seconds.

**What this gates:** Demo 5 readiness. These are the most visible legibility failures from
Demo 4.

---

### G2 — DEMO Trajectory and Comparison Display

**Issues:** #871 (DEMO-059), #873 (DEMO-062), #875 (DEMO-063), #876 (DEMO-064)
**Type:** Frontend chart rendering + Mode 3 data flow
**ADR prerequisite:** None

**Why grouped:** All four issues touch the trajectory display layer — PMM value propagation,
multi-entity chart rendering, entity label overlays, and Mode 3 branch comparison output.
They share TrajectoryView.tsx and the multi-entity chart configuration. Grouping avoids
duplicate modifications to the same component.

**Shared files:** `frontend/src/components/trajectory/TrajectoryView.tsx`, PMM component,
multi-entity chart adapter, Mode 3 comparison output panel

**Tests required:**
- Playwright assertion: PMM displays the fiscal multiplier value set in Mode 3 branch at
  step 5 (not 1.00) when fiscal_multiplier=1.30 was applied at step 3
- Playwright assertion: Zone 1D shows distinct curves for JOR and EGY at step 5 in the
  Hormuz scenario
- Playwright assertion: trajectory curves display inline entity labels at rightmost data point
- Playwright assertion: Mode 3 branch comparison panel shows quantitative delta values
  (e.g., reserve coverage delta) at step 5

**Acceptance gate (Business PO Validate step):**
Persona 2 opens the Hormuz scenario in Mode 3, applies fiscal multiplier 1.30× at step 3,
advances to step 5. PMM shows a value different from 1.00. Zone 1D shows two distinct entity
curves. Inline labels identify JOR and EGY. The comparison panel displays a named reserve
coverage delta. P-4 time ceiling: 90 seconds.

**What this gates:** Mode 3's quantitative value proposition. Without comparison output (#876),
Mode 3 is a visual demonstration, not an analytical instrument.

---

### G3 — Engine Fix: Reserves Non-Negativity Floor

**Issue:** #799
**Type:** Backend simulation engine fix
**ADR prerequisite:** None

**Why grouped:** Single-issue backend fix. Reserves reaching −0.04 months (JOR step 7 in
Demo 4) is analytically incorrect — stock attributes cannot go below zero in a physical
simulation. The fix is a floor constraint at attribute update time, independent of all other
groups.

**Shared files:** `backend/app/simulation/` — attribute update path for stock attributes

**Tests required:**
- Unit test: reserves_coverage_months cannot be negative after any simulation step
  with any event combination
- Regression test: Greece and Argentina backtesting fixtures still pass with the floor active

**Acceptance gate (Business PO Validate step):**
Run the Hormuz scenario 8 steps. JOR reserves_coverage_months at step 7 is 0.0 (floored),
not negative. All existing backtesting fixtures still pass.

**What this gates:** Analytical correctness. A stock attribute going negative is a hard
simulation integrity violation.

---

### G4 — Documentation

**Issues:** #27 (calibration docs), #822 (ecological composite disclosure), #847 (DEMO-046)
**Type:** Documentation
**ADR prerequisite:** None

**Why grouped:** Three documentation deliverables with no code dependencies. All can be
authored in parallel with code groups.

**Issues:**
- #27: Document calibration basis for propagation attenuation parameters — methodology or
  explicit placeholder at each parameter site
- #822: Ecological composite denominator-change disclosure — IA-1 note when the proximity
  indicator first activates mid-scenario, per the confidence tier system
- #847: Human Development 'Irreversible' label — contextualize in walkthrough narration so
  a finance ministry reader understands what "irreversible" means analytically

**Shared files:** `docs/methodology/`, `docs/demo/m13/` (walkthrough narration update if
needed), `docs/data-sources/`

**Tests required:** Business PO navigability test (per acceptance protocol for documentation):
a non-author can navigate from each document's entry point to the key finding in under
5 minutes.

**Acceptance gate (Business PO Validate step):**
Per work-type verification protocol (`docs/process/acceptance-protocol.md §Documentation`).

**What this gates:** Methodology transparency obligations. #822 directly satisfies a
confidence tier system disclosure requirement.

---

### G5 — ADR-013: Political Economy Module Boundary

**Issue:** #792
**Type:** Architecture document (ADR authorship)
**ADR prerequisite:** N/A (this group IS the ADR)
**Infrastructure sprint exception applies** for Phase D's intent/QA gates.

**Why grouped:** Single-focus architecture work. ADR-013 is ASSIGNED (number 13, confirmed
in `docs/architecture/backlog.md`). Panel: Architect Agent (author), Political Economist,
Chief Methodologist, Engineering Lead. The ADR defines the exact boundary of the political
economy module in M13 — which capabilities are in scope, which are deferred, and what the
integration point is with the existing M11 PoliticalEconomyModule.

**Shared files:** `docs/adr/ADR-013-political-economy-module-boundary.md`,
`docs/adr/reviews/ADR-013-panel-review.md`, `docs/architecture/backlog.md` (ARCH-007
status update: ASSIGNED → ACCEPTED)

**Acceptance gate:** ADR-013 status is ACCEPTED, panel review is filed, and ARCH-007 in
the backlog is marked ACCEPTED. EL approval is recorded in the ADR document.

**What this gates:** G6 (political economy integration). G6 may not open its implementation
PR until ADR-013 is ACCEPTED.

---

## Wave 2 — After ADR-013 Accepted

### G6 — Political Economy Integration

**Issue:** #392
**Type:** Backend + (potentially) frontend
**ADR prerequisite:** ADR-013 (BLOCKED_ADR until accepted)

**Why grouped:** #392 (political economy constraint modeling) is the primary M13 analytical
deliverable. Implementation scope is determined by ADR-013. Based on the existing M11 module
(G16a/G16b, PRs #704/#705), this group extends the PoliticalEconomyModule with:
- Constraint modeling as structured scenario inputs (Argentina and Ukraine/Pakistan marquee cases)
- Political feasibility as a named analytical output (not just a model variable)
- Integration with the confidence tier system for political feasibility outputs

May be split into G6a (backend extension) and G6b (frontend visualization) if the diff
exceeds ~800 lines. Decision deferred to ADR-013 acceptance — the ADR will define the
scope precisely.

**Shared files:** `backend/app/simulation/modules/political_economy/`,
`backend/app/api/`, and (if G6b split) `frontend/src/` zone components for constraint
visualization

**Tests required:** Intent document required before implementation PR opens. Tests authored
from intent document acceptance criteria. Playwright E2E assertions ship in the same PR as
any frontend changes.

**Acceptance gate:** Per ADR-013 north star test (Element P-7 of the ADR template). The
finance minister scenario anchored in ADR-013's persona trace is the acceptance test.

**What this gates:** M13's primary user-facing capability. The political economy module
is what separates M13 from M12 in terms of analytical capability.

---

## Blocked — Awaiting Alert Panel ADR

### G7 — Alert Panel Master-Detail UX

**Issue:** #852
**Type:** Frontend architecture + UX
**ADR prerequisite:** Alert panel ADR (PENDING_NUMBER — not yet in backlog)
**Status: BLOCKED_ADR**

**Why blocked:** EL decision 2026-06-11: "Frontend architecture review + ADR + UX Designer
+ Design Thinking agent input required before implementation." The alert panel ADR has no
GitHub issue and no backlog entry — this is the scope gap identified in the HORIZON sweep.

**Required before G7 can open:**
1. GitHub issue filed for "docs(adr): alert panel master-detail UX architecture"
2. Backlog entry added (PENDING_NUMBER)
3. Architect Agent claims next available ADR number, marks ASSIGNED
4. ADR authored with full panel (Architect, Frontend Architect, UX Designer, EL)
5. UX Designer and Design Thinking agent input documented in ADR
6. ADR accepted (EL sign-off)
7. Intent document filed per Phase A lifecycle

**What this gates:** Nothing in Wave 1 or Wave 2. G7 is the most architecturally complex
M13 deliverable and may slip to M14 if the ADR process takes the full milestone.

---

## Wave 3 — Mid-Milestone (HORIZON Sweep 2026-06-13)

All G1–G7 waves complete. HORIZON sweep promoted five issues to G8a and one to G8b.
Sprint entry: `docs/process/sprint-plans/m13-g8-sprint-entry.md` (PR #939, merged 2026-06-13).
Awaiting EL approval before any G8 implementation PR opens.

### G8a — Standards, Methodology, and Calibration

**Issues:** #45, #27 residuals (R1–R3), #271 (metadata tag only), #823, #824
**Type:** Standards update / documentation / backend calibration
**ADR prerequisite:** None
**Infrastructure sprint exception:** Applies — no intent documents required

**Issues:**
- #45: Add HCL output field standards (5 fields, units, effect size thresholds, 4 test
  requirements) to `CODING_STANDARDS.md`; cross-reference in `DATA_STANDARDS.md`
- #27 R1: Add Propagation Rules section to `docs/methodology/calibration-basis.md` covering
  `TARIFF_ATTENUATION = 0.6` / `TARIFF_MAX_HOPS = 2` with PLACEHOLDER declaration
- #27 R2: Update `backend/scripts/demo_scenario.py` docstring to reference calibration doc
- #27 R3: Add single-sentence calibration status note to ADR-001 current review entry
- #271: Add `reversibility` field (`recoverable` / `delayed_recovery` / `irreversible`) to
  simulation output indicators — **scope-limited to metadata tag only**; no MDA recalibration;
  no display-layer changes; MDA calibration deferred to M14 as named follow-on
- #823: Fix ecological composite denominator at scenario initialisation; hold indicator set
  constant for full run; disclose absent indicators separately
- #824: Derive biome-specific elasticity for arid/semi-arid economies from FAO GFR arid-country
  subset; update `ECOLOGICAL_ELASTICITY_REGISTRY` with MENA-calibrated row and source citation

**Domain agent sign-offs required before merge:**
- #823: Chief Methodologist sign-off on denominator-fixing approach
- #824: Chief Methodologist + Ecological Economist sign-off on elasticity derivation

**What this gates:** Methodology transparency obligations, calibration credibility for Demo 5
(Hormuz fixture uses the mis-calibrated MENA elasticity), and HCL test actionability (#45
closes the SA-04 gap that makes HCL tests unactionable).

---

### G8b — Mode Transition UX

**Issues:** #393
**Type:** Frontend UX fix
**ADR prerequisite:** None (mode transition design on record in PR #390 Gap 5)
**Full Phase A lifecycle required:** Intent document gates implementation

**Why promoted:** The Sri Lanka 2022 marquee case requires a Mode 1 → Mode 2 transition
within a single session without context reconstruction. Without step-position carry-forward,
the analyst must manually reconstruct the simulation start point — an interaction tax that
defeats the 90-second reactive entry ceiling.

**Intent document required at:**
`docs/process/intents/G8b-2026-06-13-mode-transition-step-preservation.md`

**Acceptance gate (Business PO Validate step):**
Execute the Sri Lanka 2022 case entry (Mode 1 replay to the shock entry point → Mode 2
simulation) in a single session without re-entry. Step position preserved; entity
configuration carried forward; confirmation modal names what is preserved.

**What this gates:** Sri Lanka marquee case execution; Mode 1→2 workflow for the external
validation audience in M14 Demo 5.

---

## Near-Term Backlog — Deferred to M14

The following issues were on the M13 board but were deferred to M14 at the HORIZON sweep
(2026-06-13). No further M13 promotion is planned. These are candidates for the M14 sprint
plan and should be revisited at M14 kickoff.

| Issue | Title | Disposition | Rationale |
|---|---|---|---|
| #22 | Uncertainty quantification | **Defer to M14** — primary deliverable candidate | Major ADR-gated architectural undertaking; pairs with methodology publication |
| #35 | Dynamic relationship weight updating | **Defer to M14** | ADR required; significant engine change; not aligned with M13 focus |
| #102 | Distributional scenario comparison | **Defer to M14** | Hard dependency on #22 |
| #274 | 25-year human capital trajectory | **Defer to M14** | Hard dependency on #271 full implementation + backtesting validation |
| #394 | Multi-scenario comparison (>2 scenarios) | **Defer to M14** | ADR required; architecture change; Kenya TC-3 marquee case |
| #837 | Configuration-driven demo scripts | **Defer to M14** | Developer tooling; no demo cycle in M13; M14 Demo 5 prep |
| #271 MDA recalibration | MDA threshold recalibration for irreversible indicators | **Defer to M14** — named follow-on to G8a #271 | Depends on #271 metadata field in production; calibration work scoped for M14 |

---

## Dependency Map

```
Wave 1 (parallel)
│
├── G1 — DEMO Legibility (#872, #874)                    → no downstream deps
├── G2 — DEMO Trajectory/Mode 3 (#871,#873,#875,#876)   → no downstream deps
├── G3 — Engine Fix (#799)                               → no downstream deps
├── G4 — Documentation (#27, #822, #847)                 → no downstream deps
└── G5 — ADR-013 (#792)
         │
         ▼
Wave 2 (after ADR-013 accepted)
└── G6 — Political Economy Integration (#392)            → M13 primary deliverable

Wave 3 (HORIZON sweep; after G1–G7 complete; parallel sub-groups)
├── G7 — Alert Panel UX (#852)                           → COMPLETE 2026-06-13
├── G8a — Standards/Methodology/Calibration              → no downstream deps within M13
│         (#45, #27 R1-R3, #271 tag, #823, #824)
└── G8b — Mode Transition UX (#393)                      → no downstream deps within M13
```

**Critical path:** G5 (ADR-013) → G6 (political economy integration) — COMPLETE.
G8a and G8b have no inter-dependencies and may run in parallel.

---

## ADR Prerequisites

| Group | Required ADR | Current status | Gate |
|---|---|---|---|
| G1 | None | N/A | ✅ COMPLETE 2026-06-12 |
| G2 | None | N/A | ✅ COMPLETE 2026-06-12 |
| G3 | None | N/A | ✅ COMPLETE 2026-06-12 |
| G4 | None | N/A | ✅ COMPLETE 2026-06-12 |
| G5 | ADR-013 (this group is the ADR) | ACCEPTED 2026-06-12 (PR #916) | ✅ COMPLETE |
| G6 | ADR-013 | ACCEPTED 2026-06-12 (PR #916) | ✅ COMPLETE 2026-06-12 |
| G7 | ADR-014 | ACCEPTED 2026-06-12 (PR #926) | ✅ COMPLETE 2026-06-13 |
| G8a | None | N/A | CLEAR — awaiting EL sprint entry approval |
| G8b | None | N/A | CLEAR — awaiting EL sprint entry approval + intent document |

---

## EL Approval Record

**Status:** Approved 2026-06-12

> Sprint plan approved. Wave 1 groups (G1–G5) may proceed once intent documents are filed
> per the Phase A execution lifecycle. G6 implementation is blocked pending ADR-013 acceptance.
> G7 is blocked pending alert panel ADR (#908) acceptance. Critical path is G5 → G6.
> — @PublicEnemage (2026-06-12)
