---
name: m18-g1-sprint-exit
type: sprint-exit
milestone: M18 — Full Argument and Demo 7
sprint-group: G1 — CI Bands on Zone 1A
status: Confirmed
authored-by: Business PO / PI Agent
date: 2026-06-28
pi-confirmed: true
release-branch: release/m18
sop-reference: docs/process/sprint-planning-sop.md §Sprint Exit Gate
---

# Sprint Exit — M18, G1: CI Bands on Zone 1A

**Status:** Confirmed — all exit conditions satisfied
**Date produced:** 2026-06-28
**Release branch:** `release/m18`
**Sprint entry document:** `docs/process/sprint-plans/m18-g1-sprint-entry.md` — EL Approved 2026-06-26

*Authority: `docs/process/sprint-planning-sop.md §Sprint Exit Gate` (Phase D output).
G1 delivers 80% CI bands on Zone 1A composite trajectories (#1254): the BandingEngine
computes per-step lower/upper bounds from a half-width schedule (step 1 ±10%, step 2 ±20%,
steps 3–5 ±35%, >5 ±50%) scaled by tier multipliers (T1:1.0, T2:1.2, T3:1.5, T4:2.0, T5:3.0).
CI ribbons render as semi-transparent fills around each framework's composite trajectory line
in `TrajectoryView.tsx`. The Demo 7 Act 2 epistemic foundation — "confidence band on the
340,000 vs. 80,000 differential" — is computable from backend data and visually grounded in
Zone 1A.*

---

## Section 1 — Sprint Identification and Date

| Field | Value |
|---|---|
| Milestone | M18 — Full Argument and Demo 7 |
| Sprint group | G1 — CI Bands on Zone 1A (Wave 1) |
| Release branch | `release/m18` |
| Sprint entry document | `docs/process/sprint-plans/m18-g1-sprint-entry.md` |
| Exit checklist issue | #1340 |
| Sprint journal issue | #1367 |
| Date implementation completed | 2026-06-28 (PR #1404 merged to `sprint/m18-g1`) |
| CI status on sprint branch | Green — playwright-e2e PASS, test-backend PASS, lint PASS, compliance-scan PASS, branch-naming PASS, changes PASS |

---

## Section 2 — Implementation Status

| Issue | PR | Merged? | CI status | Notes |
|---|---|---|---|---|
| #1254 — CI bands on Zone 1A (BandingEngine + TrajectoryView + QA tests) | #1404 | ✅ Yes | Green | `backend/tests/test_m18_g1_ci_bands.py`; `frontend/tests/e2e/m18-g1-ci-bands.spec.ts`; BandingEngine; `TrajectoryView.tsx` CI ribbon rendering |
| #1254 — integration conflict resolution (divergence fill fix) | #1411 | ✅ Yes | Green | `resolve/m18-g1-integration` → `release/m18`; divergence fill `<Area>` kryptonite fix: `fill="none"` when `showBaseline=false` |

**Implementation status:** #1254 fully delivered via PR #1404 (merged 2026-06-28 to `sprint/m18-g1`). Integration PR #1411 (`resolve/m18-g1-integration` → `release/m18`) merged 2026-06-28 after divergence fill AC-1254-1 fix. All CI checks green on integration PR.

**Files changed in G1:**
- `backend/app/simulation/banding_engine.py` — `BandingEngine` class: `_HALF_WIDTH_SCHEDULE` (step 1 ±10%, step 2 ±20%, steps 3–5 ±35%, >5 ±50%); `_TIER_MULTIPLIERS` (T1:1.0, T2:1.2, T3:1.5, T4:2.0, T5:3.0); `compute_bands()` → `lower`, `upper` per step per framework; `BandResult` dataclass
- `backend/app/api/scenarios.py` — uncertainty output endpoint serving `lower`/`upper` bounds per step per framework via `BandingEngine`
- `docs/schema/api_contracts.yml` — uncertainty output endpoint added with full request/response shape
- `frontend/src/components/TrajectoryView.tsx` — CI band `<Area>` at line 1085: `fillOpacity={showBaseline ? CI_BAND_OPACITY_MODE3 : CI_BAND_OPACITY}`; exported constants `CI_BAND_OPACITY = 0.12` (line 46), `CI_BAND_OPACITY_MODE3 = 0.05` (line 48); divergence fill `<Area>` fix: `fill={showBaseline ? FRAMEWORK_COLORS[fw] : "none"}` + `fillOpacity={0.12}` (lines 1099–1100)
- `backend/tests/test_m18_g1_ci_bands.py` — backend integration tests for BandingEngine and uncertainty endpoint (AC-1254-HW schedule verification, tier multiplier checks, endpoint response shape)
- `frontend/tests/e2e/m18-g1-ci-bands.spec.ts` — E2E tests (AC-1254-1 through AC-1254-HW): CI ribbon visible at 1280×800; fill-opacity not zero when CI data available; no invisible bands (`hasInvisibleBands` false); graceful degradation when uncertainty data unavailable

**AC-1254-1 test heuristic (divergence fill fix context):**
AC-1254-1 detects invisible bands by finding `path[fill-opacity='0']` elements with a non-null,
non-`none`, non-transparent fill color. The divergence fill `<Area>` in `CompositeChartSVG` originally
used `fillOpacity={showBaseline ? 0.12 : 0}` with `fill={FRAMEWORK_COLORS[fw]}`, producing
`fill-opacity="0"` on real-colored paths in N=1 mode (`showBaseline=false`). This triggered the
heuristic as a false positive. Fix applied on `resolve/m18-g1-integration`: changed to
`fill={showBaseline ? FRAMEWORK_COLORS[fw] : "none"}` + `fillOpacity={0.12}` — the test's
`fill !== "none"` discriminator excludes this element. CI bands themselves always use
`CI_BAND_OPACITY` or `CI_BAND_OPACITY_MODE3` (never zero); fix targeted divergence fill only.

**Pre-push gate confirmation:** ruff clean, mypy clean, tsc clean, vite build clean — confirmed
at each push via `.githooks/pre-push`.

**Step 4 Verify — implementation completeness checks:**
- `BandingEngine.compute_bands()`: steps 1 and 2 use fixed half-widths; steps 3–5 use ±35%;
  step >5 uses ±50%. Each half-width multiplied by `_TIER_MULTIPLIERS[tier]` before application.
  Lower = value × (1 − half_width); upper = value × (1 + half_width).
- Backend endpoint: returns `lower` and `upper` per step per framework for the requested scenario.
  Tier derived from scenario state tier assignment (ADR-007 tier hierarchy).
- `TrajectoryView.tsx` CI band: `<Area>` with `dataKey="upper"` and `dataKey="lower"` rendered per
  framework in both single-scenario and comparison modes. `showBaseline` flag controls Mode 3 vs.
  standard opacity (`CI_BAND_OPACITY_MODE3 = 0.05` vs. `CI_BAND_OPACITY = 0.12`).
- Divergence fill `<Area>` correctly uses `fill="none"` when `showBaseline=false`: no real-color
  path with `fill-opacity="0"` remains after fix.

---

## Section 3 — Business PO Acceptance Table

| Deliverable | Work type | Customer Agent Layer 3 assessment | Business PO verdict | Verdict artifact |
|---|---|---|---|---|
| #1254 — CI bands on Zone 1A (BandingEngine + CI ribbon rendering in TrajectoryView) | Backend + Frontend | PASS — see Layer 3 assessment below (Persona 5 and Persona 1) | **ACCEPT** 2026-06-28 | Section 3 below |

**Business PO acceptance status:** ACCEPT. No open rejections.

---

### Customer Agent Layer 3 Assessment

*G1 delivers a new visual element on Zone 1A (CI ribbon) and a new backend computation
(BandingEngine). The CI ribbon is visible to all personas viewing Zone 1A. Customer Agent
Layer 3 is required for Persona 5 (Aicha, Finance Minister) per CLAUDE.md §Entry and Exit
Invariants (deliverable serves Persona 5). Persona 1 (Lucas, Economist) assessment included
as primary analytical consumer.
Session context: Same session as BPO verdict authorship — acknowledged.*

**Assessment method:** Kryptonite constraint check per `docs/process/agent-execution-lifecycle.md
§Kryptonite Design Constraint`. Does the primary observable state require specialist mediation
for the target persona to act on it within the time ceiling?

---

**#1254 — Persona 5: Aicha Mbaye (Finance Minister, Demonstrative entry state)**

The primary observable state: Zone 1A shows composite trajectory curves with semi-transparent
CI ribbons. The ribbon width varies per step — narrower at steps 1–2 (±10%, ±20%), wider at
steps 3+ (±35–50% × tier multiplier). At T3 data, the ribbon covers a meaningful range around
the trajectory. The ribbon renders at `CI_BAND_OPACITY = 0.12` (12% opacity) in standard mode.

*Layer 3 check:* Does Aicha require specialist mediation to interpret the CI ribbon on Zone 1A?

The ribbon is a visual uncertainty indicator — wider ribbon means more uncertainty at that step.
This is a geometric/intuitive encoding. Aicha does not need to know the half-width schedule
(±35%) or the tier multiplier (1.5 for T3). She reads: "the band is wide" = "less certain at
this point." The ribbon does not require reading numerical values or performing any calculation.

*Kryptonite patterns evaluated:*
- "CI band half-width: ±35% × 1.5 (T3 multiplier) at step 3" → KRYPTONITE if displayed as text — NOT present; rendered as ribbon width, not text annotation
- "Lower bound: 0.42, Upper bound: 0.68" → KRYPTONITE if primary display — NOT the primary display; ribbon is the primary display
- Ribbon width as geometric encoding of uncertainty magnitude → PASS — visual width communicating "more uncertain" is interpretable without domain training

*Time ceiling (Demonstrative, 30 seconds):* Zone 1A is the primary viewport in COMPARE_VIEW.
The CI ribbon is visible on Zone 1A trajectories without interaction. Aicha sees "trajectory with
bands" in one glance. She does not need to read the bands quantitatively to understand they
represent uncertainty. The analytical claim ("we have quantified our uncertainty") is
communicated by the ribbon's presence, not its precise width. 30-second ceiling: PASS.

*What Aicha takes from Zone 1A CI ribbons in the negotiation:* "Our projections are not point
estimates. We have quantified the uncertainty range." This is a first-order framing claim —
defensible at L0 without interaction.

**Layer 3 verdict — Persona 5 (Aicha): PASS.** CI ribbon is a geometric encoding of uncertainty
(wider = less certain) — interpretable without economic training. Visible at L0 in Zone 1A
without interaction. The ribbon communicates "uncertainty is quantified and displayed" in one
glance. 30-second Demonstrative ceiling: PASS. No kryptonite numeric text rendered as primary
display.

---

**#1254 — Persona 1: Lucas Oliveira (Economist / Analytical Lead, Preparatory entry state)**

Use case: Lucas needs to explain and defend the CI bands under IMF peer scrutiny.

*Layer 3 check:* Does Lucas require additional methodology disclosure beyond what G1 delivers?

G1 delivers: the ribbon width reflects the half-width schedule (±10/20/35/50%) × tier multiplier.
The tier is visible via the T-badge on Zone 1A (ADR-017). Lucas reads: "T3 data, step 3+ half-width
is ±35% × 1.5 = ±52.5%." This is available in the backend response and the tier badge.

*Auditability (Lucas's use case):* Lucas can state: "The CI bands derive from ADR-007: the
half-width schedule is step-indexed (±10% at step 1 through ±50% at step 5+) scaled by the
data confidence tier (T3 = 1.5×). For this scenario, at step 5, the half-width is ±75%. The
ribbon on Zone 1A reflects this." The methodology is in the BandingEngine constants, the tier
badge is on Zone 1A, and the ADR-007 reference is in the simulation framework docs. Lucas can
defend this under peer scrutiny.

**Layer 3 verdict — Persona 1 (Lucas): PASS.** Tier badge on Zone 1A + half-width schedule in
BandingEngine constants + ADR-007 reference provides full auditability. No Zone 3 expandable
panel is required for G1 — the band geometry is governed by a documented schedule, not an
opaque model. Analytical lead can cite ADR-007 directly.

**Customer Agent Layer 3 summary: PASS for Persona 5 (Aicha) and Persona 1 (Lucas).
Layer 3 filed before BPO verdict per acceptance-protocol.md §1.1.**

---

### BPO Verdict — #1254 CI Bands on Zone 1A

*Assessed per acceptance-protocol.md §1.1 (Frontend Feature + Backend Extension).*

**Observable state confirmed:**

1. `BandingEngine` in `backend/app/simulation/banding_engine.py`: `_HALF_WIDTH_SCHEDULE` maps
   step number to half-width fraction (1:0.10, 2:0.20, 3–5:0.35, >5:0.50). `_TIER_MULTIPLIERS`
   maps tier string to multiplier (T1:1.0, T2:1.2, T3:1.5, T4:2.0, T5:3.0). `compute_bands()`
   returns `BandResult(lower, upper)` per step per framework.

2. Backend uncertainty endpoint: returns `lower`/`upper` per step per framework for the
   requested scenario. Tier derived from scenario state tier assignment (ADR-007 tier hierarchy).
   Registered in `docs/schema/api_contracts.yml`.

3. `TrajectoryView.tsx` CI band `<Area>` (line 1085): `fillOpacity={showBaseline ? CI_BAND_OPACITY_MODE3 : CI_BAND_OPACITY}`
   — standard mode opacity 0.12; Mode 3 overlay opacity 0.05. Renders per framework in both
   single-scenario and comparison modes. `fill={FRAMEWORK_COLORS[fw]}` uses the framework's
   color at reduced opacity.

4. Divergence fill `<Area>` (lines 1099–1100): `fill={showBaseline ? FRAMEWORK_COLORS[fw] : "none"}`
   + `fillOpacity={0.12}`. In N=1 mode (`showBaseline=false`), divergence fill uses `fill="none"`,
   excluded by AC-1254-1 `fill !== "none"` discriminator. CI bands themselves never use
   `fill-opacity="0"` — they use `CI_BAND_OPACITY` or `CI_BAND_OPACITY_MODE3`.

5. AC-1254-1 E2E test: verifies no `path[fill-opacity='0']` element with a real, non-`none`,
   non-transparent fill color exists when CI data is available. Passes in CI on PR #1411
   after divergence fill fix.

6. Graceful degradation: when uncertainty data is unavailable, CI band `<Area>` is not rendered
   (conditional on data presence). AC-1254-1 degradation test passes.

7. QA tests: `backend/tests/test_m18_g1_ci_bands.py` (BandingEngine half-width schedule,
   tier multipliers, endpoint response shape) and `frontend/tests/e2e/m18-g1-ci-bands.spec.ts`
   (AC-1254-1 through AC-1254-HW). Both authored before implementation code; pass in CI on PR #1404.

**DEMO4 class check (dynamic output):** The CI band `<Area>` in `TrajectoryView.tsx` renders
`lower`/`upper` values from the backend uncertainty endpoint (fetched per scenario). E2E tests
use scenario fixture data to assert band presence, not static defaults. DEMO4 check: PASS.

**Kryptonite check (Persona 5 — Aicha):** CI ribbon is geometric encoding (width = uncertainty
magnitude) — no numeric text annotation in primary display. Visible at L0 in Zone 1A without
interaction. Demonstrative 30-second ceiling: PASS. Kryptonite check: PASS.

**BPO acceptance threshold (GR §4.2):**
- ✅ CI ribbon visible on Zone 1A composite trajectory curves for Zambia baseline at 1280×800
- ✅ Band width reflects tier-scaled half-width schedule (ADR-007 compliant)
- ✅ Standard opacity `CI_BAND_OPACITY = 0.12`; Mode 3 overlay opacity `CI_BAND_OPACITY_MODE3 = 0.05`
- ✅ No invisible bands (AC-1254-1 `hasInvisibleBands` false after divergence fill fix)
- ✅ Graceful degradation: ribbon absent when uncertainty data unavailable
- ✅ Backend endpoint registered in `api_contracts.yml`; BandingEngine tier multipliers T1–T5 implemented
- ✅ QA tests authored before implementation; all pass in CI

> VALIDATED — 2026-06-28. Frontend: `TrajectoryView.tsx` CI band `<Area>` at line 1085 —
> `fillOpacity` from `CI_BAND_OPACITY` (0.12 standard) or `CI_BAND_OPACITY_MODE3` (0.05 Mode 3);
> renders per framework in standard and COMPARE_VIEW modes. Divergence fill fix at lines 1099–1100:
> `fill="none"` when `showBaseline=false` — AC-1254-1 `hasInvisibleBands` false confirmed on PR #1411 CI.
>
> Backend: BandingEngine half-width schedule (1:±10%, 2:±20%, 3–5:±35%, >5:±50%) × tier
> multipliers (T1:1.0, T2:1.2, T3:1.5, T4:2.0, T5:3.0). Endpoint returns `lower`/`upper` per
> step per framework. Schema: `api_contracts.yml` updated. DEMO4 check: bands populated from
> backend fetch, not static default.
>
> CI failure on integration PR #1411 (AC-1254-1 `hasInvisibleBands` true) root cause: divergence
> fill `<Area>` used `fillOpacity=0` with real fill color in N=1 mode. Fix: `fill="none"` when
> `showBaseline=false`. This fix went into `resolve/m18-g1-integration` (the conflict resolution
> branch) rather than a new feature PR — the issue was discovered during integration. Fix is part
> of PR #1411 commit a19c432.
>
> Sprint entry UX/UI panel review conditions fulfilled: CI ribbon color derived from
> `FRAMEWORK_COLORS[fw]` (ADR-017 framework color encoding); opacity 0.12 (standard) / 0.05
> (Mode 3 overlay); no interaction in scope for G1 (tooltip-on-hover deferred per sprint entry).
>
> North star test: see Section 3 artifact below. Verdict: **ACCEPT**.

---

### North Star Test Artifact

*Required for user-facing deliverables per CLAUDE.md §North Star Test (Process Gate).
#1254 is a user-facing deliverable (new visual element on Zone 1A). Authored by Business PO
per authority assignment.*

**North star question:** Does this decision make the tool more useful to a finance minister
sitting across from an IMF negotiating team, in that moment?

**Finance minister scenario:** The Zambia Ministry of Finance analyst team is in a Demo 7
Act 2 session. They have used WorldSim to run three programme scenarios. Zone 1A shows
composite score trajectories for all three scenarios. The IMF team has been presented with
Zone 1A trajectory curves and challenges the Ministry's analyst: "Your trajectory shows
decline under Option A — but how do we know your model isn't just expressing parameter
assumptions? Are these trajectories confident or speculative?"

**Capability evaluated:** BandingEngine CI ribbons on Zone 1A composite trajectories —
semi-transparent bands around each framework's trajectory line, width reflecting the
half-width schedule (±35–50% at steps 3+) scaled by the data confidence tier (T3 = 1.5×
for Zambia's UN WPP 2024 data).

**Does this capability change what the Ministry's team can argue at the table?**

**YES — specifically and measurably.**

Before G1: Zone 1A shows composite score trajectory lines without uncertainty bands. The IMF
challenges: "Your model produces a trajectory — but you haven't quantified the uncertainty."
The Ministry's analyst has no visual artifact in Zone 1A to point to in response. They can
only assert that uncertainty is documented in the methodology. The IMF's challenge stands
without a visual counter.

After G1: Zone 1A shows CI ribbons. The Ministry's analyst responds: "The bands on Zone 1A
ARE the uncertainty quantification. Each ribbon reflects the ADR-007 confidence tier for
this data — T3 for Zambia, meaning a ±52.5% half-width at step 3 and ±75% at step 5.
The direction of the trajectory — downward under Option A — holds even at the upper bound
of the CI ribbon at programme end. We are not hiding uncertainty. We are displaying it."

The IMF must now either (a) challenge ADR-007's tier classification methodology, (b) challenge
the half-width schedule, or (c) engage with the trajectory direction claim on its merits.
"You haven't quantified uncertainty" is no longer a valid objection.

This is a shift from a defensive posture ("we have methodology documents") to an evidentiary
posture ("here is the uncertainty, displayed — what specifically is your challenge to it?").

**North star test verdict: PASS** — CI ribbons on Zone 1A change the character of the IMF's
challenge from "unquantified speculation" to "here is our quantified uncertainty; challenge
the tier classification or engage with the direction." The Ministry's team gains a visual
artifact that makes the epistemic claim concrete and negotiation-ready, not just documented.

---

## Section 4 — Open Rejections

No open rejections. ACCEPT verdict recorded in Section 3. No REJECT verdicts issued.

**Near-miss entries required for each rejection:** N/A — no rejections in G1.

**CI failures caught and fixed within G1 (not sprint rejections):**
1. AC-1254-1 `hasInvisibleBands` true on integration PR #1411 — root cause: divergence fill
   `<Area>` used `fillOpacity=0` with real fill color in N=1 mode. Fixed in `resolve/m18-g1-integration`
   by changing to `fill="none"` when `showBaseline=false`. Fix is in PR #1411 commit a19c432.
   Caught by CI before any EL review. Implementation correction, not a sprint rejection.

No REJECT artifacts filed. No NM entries required for CI-caught failures.

---

## Section 5 — PI Agent Sprint Exit Confirmation

**Exit conditions checklist (PI Agent):**

- [x] **All implementation groups merged; CI green on sprint branch (Section 2)**
  PR #1404 merged 2026-06-28 to `sprint/m18-g1`. All CI checks green (playwright-e2e PASS,
  test-backend PASS, lint PASS, compliance-scan PASS, branch-naming PASS, changes PASS).
  Integration PR #1411 (`resolve/m18-g1-integration` → `release/m18`) merged 2026-06-28 with
  all checks green including playwright-e2e PASS after divergence fill fix.
  QA test files `backend/tests/test_m18_g1_ci_bands.py` and `frontend/tests/e2e/m18-g1-ci-bands.spec.ts`
  authored before implementation code (NM-055 compliant).

- [x] **Business PO ACCEPT verdict filed for each user-facing deliverable (Section 3)**
  #1254 ACCEPT — verdict filed in Section 3, dated 2026-06-28.

- [x] **Customer Agent Layer 3 assessment on record for all Persona 2/3/5 deliverables (Section 3)**
  G1 serves Persona 5 (Aicha) as primary (CI ribbon visible in Zone 1A at L0) and Persona 1
  (Lucas) for analytical defence.
  Persona 5 (Aicha) Layer 3 PASS: geometric uncertainty encoding, 30-second Demonstrative ceiling.
  Persona 1 (Lucas) PASS: tier badge + half-width schedule + ADR-007 reference fully auditable.
  Layer 3 filed before BPO verdict.

- [x] **No open rejection artifacts (Section 4)**
  No REJECT verdicts issued in G1. One CI failure caught and corrected within integration
  (divergence fill fix); not a sprint rejection.

- [x] **Near-miss entry filed for each rejection (Section 4)**
  N/A — no rejections. CI failure is an implementation correction, not a sprint rejection.

- [x] **North star test artifact on record (Section 3)**
  Filed in Section 3. Finance minister scenario: Zambia Ministry analyst in Demo 7 Act 2 in
  debt restructuring negotiation with IMF. Before G1: IMF challenge "you haven't quantified
  uncertainty" stands without visual counter. After G1: Ministry analyst points to Zone 1A
  CI ribbons — "The bands ARE the uncertainty quantification. T3 data, ±52.5% half-width at
  step 3. Direction holds at upper bound." IMF must challenge the tier classification or
  engage with the direction — not dismiss as "unquantified." Not aspirational. Specific scenario.

**PI Agent sprint exit verdict: CONFIRMED — all exit conditions satisfied**

**PI Agent confirmation:**

> G1 sprint exit conditions are satisfied as of 2026-06-28. #1254 (CI bands on Zone 1A
> trajectories — `BandingEngine` + `TrajectoryView.tsx` CI ribbon) is delivered via PR #1404
> merged 2026-06-28 to `sprint/m18-g1`. CI is green on sprint branch — all 6 required checks
> PASS. Integration PR #1411 (`resolve/m18-g1-integration` → `release/m18`) merged 2026-06-28;
> all checks green including playwright-e2e PASS after divergence fill `fill="none"` fix.
>
> Business PO ACCEPT verdict on record for #1254 (Section 3, dated 2026-06-28). Customer Agent
> Layer 3 assessments filed before verdict — Persona 5 (Aicha): PASS (geometric uncertainty
> encoding; 30-second Demonstrative ceiling); Persona 1 (Lucas): PASS (tier badge + half-width
> schedule + ADR-007 reference auditable without additional disclosure panel).
>
> North star test artifact filed and specific: Zambia Ministry of Finance in Demo 7 Act 2.
> IMF challenges "unquantified uncertainty." Ministry analyst points to Zone 1A CI ribbons:
> "T3 data, ±52.5% half-width at step 3 — direction holds at upper bound." IMF must now
> challenge the tier classification, not dismiss direction as speculation. Shift from defensive
> to evidentiary posture. North star test: PASS. Specific, not aspirational.
>
> Step 4 Verify source code checks:
> - `BandingEngine._HALF_WIDTH_SCHEDULE`: 1:0.10, 2:0.20, 3:0.35, 4:0.35, 5:0.35, >5:0.50
> - `BandingEngine._TIER_MULTIPLIERS`: T1:1.0, T2:1.2, T3:1.5, T4:2.0, T5:3.0
> - `BandingEngine.compute_bands()`: lower = value × (1 − hw); upper = value × (1 + hw)
> - `TrajectoryView.tsx` line 1085 CI band `<Area>`: `fillOpacity={showBaseline ? CI_BAND_OPACITY_MODE3 : CI_BAND_OPACITY}`
> - `CI_BAND_OPACITY = 0.12` (line 46); `CI_BAND_OPACITY_MODE3 = 0.05` (line 48)
> - Divergence fill lines 1099–1100: `fill={showBaseline ? FRAMEWORK_COLORS[fw] : "none"}` + `fillOpacity={0.12}`
> - No real-color path with `fill-opacity="0"` present after fix (AC-1254-1 `hasInvisibleBands` false)
> - QA tests: `test_m18_g1_ci_bands.py` + `m18-g1-ci-bands.spec.ts` — authored before implementation; all pass in CI
>
> No open REJECT verdicts. No open rejection artifacts.
>
> G1 merge ordering constraint (sprint entry §6.4): No cross-group dependency declared between
> G1 and G2 (distinct file areas). G1 integration PR #1411 merged to `release/m18` before
> G3 integration PR #1417 merged — G3 sprint exit §5 noted G1 merge ordering constraint;
> constraint satisfied (G1 merged first, G3 integration opened and merged after).
>
> **G1 is CLOSED as of 2026-06-28.**
>
> — PI Agent, 2026-06-28

---

## Sprint Exit Artifact Statement

This document is the sprint exit artifact for M18-G1. It supersedes any informal exit notation
in `SESSION_STATE.md` and in sprint journal issue #1367 comments for this sprint. It is filed at
`docs/process/sprint-plans/m18-g1-sprint-exit.md`.

The PI Agent confirmation in Section 5 is the gate. G1 is closed as of 2026-06-28.

**Downstream integration:** Integration PR #1411 (`resolve/m18-g1-integration` → `release/m18`)
merged 2026-06-28. G1 deliverables are on `release/m18`.
