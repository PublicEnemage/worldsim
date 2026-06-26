---
name: m17-g2-sprint-exit
type: sprint-exit
milestone: M17 — Calibration and Comparative Infrastructure
sprint-group: G2 — Multi-Scenario Comparison (Phase 3 Implementation)
status: Confirmed
authored-by: Business PO / PI Agent
date: 2026-06-26
pi-confirmed: true
release-branch: release/m17
sop-reference: docs/process/sprint-planning-sop.md §Sprint Exit Gate
---

# Sprint Exit — M17, G2: Multi-Scenario Comparison (Phase 3)

**Status:** Confirmed — all exit conditions satisfied
**Date produced:** 2026-06-26
**Release branch:** `release/m17`
**Sprint entry document:** `docs/process/sprint-plans/m17-g2-sprint-entry.md` — EL Approved 2026-06-25

*Authority: `docs/process/sprint-planning-sop.md §Sprint Exit Gate` (Phase D output).
G2 Phase 3 delivers N>2 scenario comparison (#394): N=3 curves in Zone 1A with triple-channel
differentiation (color + stroke), per-scenario threshold crossing rows in Zone 1B, and
per-scenario programme survival probability in Zone 1D — all wired through App.tsx and
verified by E2E test suite. Delivered across PR #1311 (component layer) and PR #1314
(App.tsx wiring + E2E activation), both merged to `release/m17`.*

---

## Section 1 — Sprint Identification and Date

| Field | Value |
|---|---|
| Milestone | M17 — Calibration and Comparative Infrastructure |
| Sprint group | G2 — Multi-Scenario Comparison, Phase 3 Implementation (Wave 2) |
| Release branch | `release/m17` |
| Sprint entry document | `docs/process/sprint-plans/m17-g2-sprint-entry.md` |
| Exit checklist issue | #982 |
| Date implementation completed | 2026-06-26 (PR #1314 merged to `release/m17`) |
| CI status on release branch | **Green** — playwright-e2e PASS (8m25s), lint PASS, test-backend PASS, compliance-scan PASS, branch-naming PASS, changes PASS, backtesting SKIPPED |

---

## Section 2 — Implementation Status

| Issue/Component | PR | Merged? | CI status | Notes |
|---|---|---|---|---|
| #394 — Zone 1A/1B/1D component layer (SCENARIO_COMPARISON_PALETTE, ScenarioComparisonConfig, N=3 curves, per-scenario Zone 1B rows, per-scenario Zone 1D PSP, ScenarioInstrumentCluster trajectory fetch) | #1311 | ✅ Yes — 2026-06-25 | Green | Component-boundary implementation; App.tsx wiring deferred to PR #1314 |
| #394 — App.tsx wiring + E2E test activation (comparisonScenarios state, `__worldsim_setComparisonScenarios` window function, prop to ScenarioInstrumentCluster, 7-test suite with route mocks and inject pattern) | #1314 | ✅ Yes — 2026-06-26 | Green | playwright-e2e PASS (8m25s); all 7 AC assertions hard-fail |

**Implementation status:** Both PRs merged to `release/m17`. CI green.
Frontend pre-push build gate (`cd frontend && npm run build`) confirmed at push for both PRs —
exit 0, TypeScript clean, 619 modules. No soft-skip patterns in E2E test file (NM-056 compliant).

**Step 4 Verify — implementation completeness checks:**

*App.tsx wiring (PR #1314):*
- `import { type ScenarioComparisonConfig } from "./components/TrajectoryView"` — confirmed in `frontend/src/App.tsx` line 19.
- `const [comparisonScenarios, setComparisonScenarios] = useState<ScenarioComparisonConfig[]>([])` — line 106.
- `__worldsim_setComparisonScenarios` window function in DEV useEffect — lines 199–202; guarded by `if (!import.meta.env.DEV) return` — eliminated from production builds.
- `comparisonScenarios={comparisonScenarios.length > 0 ? comparisonScenarios : undefined}` passed to `ScenarioInstrumentCluster` — line 373. Non-empty guard ensures `undefined` is passed when no comparison is active, preserving cluster default behavior.

*E2E test activation (PR #1314):*
- `injectComparisonScenarios` helper calls `__worldsim_setComparisonScenarios` via `page.evaluate` — returns `false` if function not present (guard for future regressions).
- All 7 tests: route-mock `**/api/v1/scenarios/${scenarioId}/trajectory*` for each of the three comparison scenarios before navigation; navigate to `/?scenario=zmb-zambia-baseline`; call `injectComparisonScenarios`; hard-assert AC testids.
- Guards (`isVisible().catch(() => false)` early return) removed — all assertions are hard-fail per NM-056 standard.

*ScenarioInstrumentCluster useEffect (PR #1311):*
- `comparisonScenarios?.map(...)` → parallel fetch of trajectories via `comparisonScenariosKey` dependency — one fetch per active scenario config.
- `pspValue` extracted from `political_economy.indicators.programme_survival_probability.value` in trajectory response.
- `thresholdCrossings` extracted from `threshold_crossings` array in trajectory response.
- `loadedComparisonScenarios` state populated after all parallel fetches resolve.

*Zone 1A (PR #1311 — TrajectoryView.tsx):*
- `SCENARIO_COMPARISON_PALETTE` constant: 5 slots (steel blue solid, amber dashed, green dotted, purple long-dash, rose dash-dot). N=3 uses slots 0–2.
- `zone1a-curve-scenario-{slug}` path elements (slug = `sc.scenarioId.replace(/^[a-z]{3}-/, "")`).
- `zone1a-terminal-label-scenario-{slug}` text elements at terminal data point.
- `zone1a-mda-floor-line` on first comparison scenario's MDA floor line (regression guard from #1249).
- `comparisonScenarios.length === 0` gates: entity trajectory paths suppress when comparison mode active.

*Zone 1B (PR #1311 — MDAAlertPanelZone1B.tsx):*
- Per-scenario grouped rows: `zone1b-scenario-header-{slug}`, `zone1b-threshold-row-scenario-{slug}`, `zone1b-no-crossings-{slug}`.
- Rendered when `comparisonScenarios.length > 0` in a bounded container below the alert panel — MDA alert panel `minHeight: 80px` preserved.

*Zone 1D (PR #1311 — FourFrameworkZone1D.tsx):*
- Per-scenario PSP rows inside `peEnabled && pspValue !== undefined` guard: `zone1d-psp-row-scenario-{slug}`, `zone1d-psp-value-{slug}`.
- PSP numeric: `Math.round(parseFloat(sc.pspValue) * 100)` → percentage display. All three rows simultaneously visible without interaction.

---

## Section 3 — Business PO Acceptance Table

| Deliverable | Work type | Customer Agent Layer 3 assessment | Business PO verdict | Verdict artifact |
|---|---|---|---|---|
| #394 — N=3 multi-scenario comparison (Zone 1A/1B/1D + App.tsx wiring) | Frontend | PASS — see Layer 3 assessment below (Persona 1 + 3 + 5) | **ACCEPT** 2026-06-26 | Section 3 below |

**Business PO acceptance status:** ACCEPT. No open rejections.

---

### Customer Agent Layer 3 Assessment

*#394 serves Personas 1, 3, and 5 — Customer Agent Layer 3 is required per CLAUDE.md
§Entry and Exit Invariants. Assessment conducted prior to BPO verdict.
Session context: Same session as BPO verdict authorship — acknowledged.*

**Assessment method:** Kryptonite constraint check per `docs/process/agent-execution-lifecycle.md §Kryptonite Design Constraint`. For each persona: does the primary observable state require specialist mediation to act on it within the P-4 time ceiling (90 seconds, Reactive)?

---

**#394 — Persona 5 (Aicha Mbaye, Finance Minister — Reactive, 90-second ceiling):**

The primary observable state for Persona 5 is: Zone 1A showing three trajectory curves with terminal labels "A", "B", "C" at the rightmost data point; Zone 1B showing "Option C: [no crossings through step 8]"; Zone 1D showing Option A: 58%, Option B: 67%, Option C: 74% simultaneously — all on the primary viewport without interaction.

*Layer 3 check:* Are the labels "A", "B", "C" self-interpreting for Aicha Mbaye, who is looking at three restructuring options she selected before entering the comparison view? Yes — "A", "B", "C" are scenario-set labels attached to the options at selection time. Aicha does not need to translate a legend; the label at the curve endpoint corresponds to the option she named. "no crossings through step 8" is plain language — no specialist vocabulary. "74%" as a PSP percentage is a number in a range; the relative ordering (74% > 67% > 58%) is directly interpretable: higher is safer.

The single semantic demand is understanding that "no crossings" means the poverty threshold is not breached. This is unambiguous from context — Zone 1B has already displayed crossing rows for Options A and B; "no crossings" contrasts with them directly. No specialist mediation required.

**Layer 3 verdict — Persona 5: PASS.** Labels are scenario-context self-interpreting. "no crossings" contrasts with visible crossing rows. PSP percentage is unambiguous comparative. No conditions.

---

**#394 — Persona 1 (Lucas Ferreira, IMF Programme Analyst):**

The primary observable state for Persona 1 is: Zone 1A with three curves differentiable by terminal label ("A", "B", "C") and triple-channel visual encoding (color + stroke + label). Lucas can cite: "At step 4, Option C's Q1 poverty headcount trajectory is 0.14 units higher than Option A — Option C stays above the MDA floor while A and B breach it."

*Layer 3 check:* Does the trajectory divergence require specialist mediation for Lucas to cite it? No — Lucas selected the three scenarios. The three curves are labeled at their terminal endpoints by the scenario identifiers he assigned at selection. The y-axis is the composite score he is already analyzing. The MDA floor line (from #1249) marks the minimum descent altitude he knows from prior Zone 1B interaction. The Q1 composite score differential is a numeric quantity readable from the chart's y-axis scale — no intermediate translation.

**Layer 3 verdict — Persona 1: PASS.** No specialist mediation required. No conditions.

---

**#394 — Persona 3 (Andreas Petrakis, Political Advisor):**

The primary observable state for Persona 3 is: Zone 1D showing three PSP values simultaneously — "Option A: 58%", "Option B: 67%", "Option C: 74%" — without any click, hover, or view-switch between readings.

*Layer 3 check:* Does reading three PSP percentages simultaneously require specialist mediation? PSP (Programme Survival Probability) is established Zone 1D vocabulary from M16. Andreas reads political risk for a living; PSP as a probability percentage is native vocabulary. The simultaneous display removes a comparative inference step — Andreas does not compute "Option C has higher PSP than Option A" from separate readings; he reads it directly from three co-displayed values. The simultaneity is the Layer 3 benefit: no view-switch needed to compare.

**Layer 3 verdict — Persona 3: PASS.** PSP percentage is domain-native for target persona. Simultaneous display eliminates comparative inference step. No conditions.

---

**Customer Agent Layer 3 summary: PASS for all three target personas. No CA conditions raised. Layer 3 assessment filed before BPO verdict per acceptance-protocol.md §1.1 step 8.**

---

### BPO Verdict — #394 N=3 Multi-Scenario Comparison

*Assessed per acceptance-protocol.md §1.1 (Frontend Feature).*

**Observable state confirmed:**

1. **E2E CI evidence:** `playwright-e2e` PASS (8m25s) on PR #1314. Seven test cases across AC-S1, AC-A1, AC-B1, AC-D1, AC-P5, AC-P1, AC-P3 — all hard-fail assertions, no guards. This is the primary evidence that all seven ACs produce the expected testid-visible output at 1280×800.

2. **AC-S1 (scenario setup):** After `__worldsim_setComparisonScenarios` fires via `page.evaluate`, route mocks for `zmb-option-a`, `zmb-option-b`, `zmb-option-c` intercept trajectory fetches. `loadedComparisonScenarios` state populates → Zone 1A/1B/1D comparison renderers activate. Testids `zone1a-curve-scenario-option-a/b/c`, `zone1b-scenario-header-option-a`, `zone1d-psp-row-scenario-option-a` — all visible and hard-asserted in CI.

3. **AC-A1 (Zone 1A differentiability):** Terminal labels `zone1a-terminal-label-scenario-option-a/b/c` contain text "A", "B", "C". `zone1a-mda-floor-line` visible (regression guard from #1249). All three curves simultaneously visible. Hard-asserted in CI.

4. **AC-B1 (Zone 1B per-scenario rows):** `zone1b-scenario-header-option-a/b/c` visible. `zone1b-threshold-row-scenario-option-a` contains "CRITICAL". `zone1b-no-crossings-option-c` visible with text matching `/no crossings/i`. MDA panel height ≥ 80px. Hard-asserted in CI.

5. **AC-D1 (Zone 1D PSP simultaneously visible):** `zone1d-psp-row-scenario-option-a/b/c` all visible. `zone1d-psp-value-option-c` matches `/74|0\.74/`. No click or hover required between readings. Hard-asserted in CI.

6. **AC-P5 (Aicha 90-second legibility gate):** At step 4 of ZMB N=3 comparison with Q1 poverty headcount mock data: Zone 1A terminal label "C" visible, Zone 1B Option C "no crossings" visible, Zone 1B Option A "CRITICAL" visible. No drawer interaction required. Viewport 1280×800, no overflow clipping. Hard-asserted in CI.

7. **AC-P1 / AC-P3 (Lucas / Andreas persona gates):** Option A and Option C curves both visible with distinct stroke attributes. Three PSP value rows visible simultaneously; `zone1d-psp-value-option-c` ≥ `zone1d-psp-value-option-a` (74% vs 58%). Hard-asserted in CI.

**DEMO4 class check (dynamic output):** Zone 1A curves derive from trajectory API responses fetched in parallel by `ScenarioInstrumentCluster` for each comparison scenario config. Zone 1B crossing rows derive from `threshold_crossings` in those same trajectory responses. Zone 1D PSP values derive from `political_economy.indicators.programme_survival_probability.value` in each trajectory response. None of the AC-visible outputs are static defaults — they are computed from route-mocked API data whose fixture values differ across the three scenarios (Option A Q1=0.58, Option B Q1=0.59, Option C Q1=0.72; PSP 58%, 67%, 74%). E2E test assertions on specific values (CRITICAL text, "74%", "no crossings") cannot pass with frozen or static defaults.

**Kryptonite check (intent §6):**

- Opening a drawer to see Zone 1B threshold crossings: **PASS** — Zone 1B per-scenario rows are on the primary surface.
- Hovering Zone 1A curves to read scenario labels: **PASS** — terminal endpoint labels ("A", "B", "C") are always visible without hover.
- Navigating between scenario views to compare PSP: **PASS** — three PSP values shown simultaneously in Zone 1D.

All three kryptonite constraints satisfied by the implementation as delivered.

> VALIDATED — 2026-06-26. Frontend: #394 N=3 multi-scenario comparison (Zone 1A/1B/1D + App.tsx).
> DEMO4 check: Zone 1A curves, Zone 1B crossing rows, and Zone 1D PSP values all derive from
> route-mocked trajectory API responses with fixture-distinct values — not static defaults.
> AC-S1/A1/B1/D1/P5/P1/P3: all seven hard-asserted in CI (playwright-e2e PASS 8m25s, PR #1314).
> Kryptonite: PASS on all three constraints. Layer 3: PASS for Personas 1, 3, and 5.
> Verdict: **ACCEPT**.

---

### North Star Test Artifact

*Required for user-facing deliverables per CLAUDE.md §North Star Test (Process Gate).
#394 is user-facing (Zone 1A/1B/1D primary surface). Assessment authored by Business PO
with input from Customer Agent (Persona 5 trace per intent §2).*

**North star question:** Does this decision make the tool more useful to a finance minister
sitting across from an IMF negotiating team, in that moment?

**North star assessment:**

*Scenario:* Demo 7 Act 2 — Zambia debt restructuring. Aicha Mbaye (Finance Minister archetype)
is presenting to a joint IMF/creditor negotiating panel. Three restructuring options are on the
table: Option A (conventional austerity), Option B (hybrid programme), Option C (Homegrown
Programme). The panel has asked which option the ministry is recommending and why. Aicha's team
has 90 seconds to identify the dominant option before responding. The session is live — no
additional navigation, no drawer interactions.

*Capability evaluated:* Before G2 Phase 3, WorldSim supported only two-scenario comparison
(the primary scenario vs. one comparator). Three restructuring options required loading each
comparison separately and holding the prior comparison in memory — a recall burden under the
reactive 90-second ceiling. After G2 Phase 3, Zone 1A shows all three trajectory curves
simultaneously with terminal labels A/B/C; Zone 1B shows per-scenario threshold crossings with
"Option C: [no crossings through step 8]" immediately distinguishable from Options A and B
which show CRITICAL crossings; Zone 1D shows all three PSP values (58%, 67%, 74%)
simultaneously in one view.

*What the ministry team can argue at the table:*

From the primary viewport alone, in under 90 seconds, Aicha can state: "Option C — the
Homegrown Programme — does not cross the poverty threshold. Both external options breach it
in the first year of implementation. Option C also shows the highest programme survival
probability at 74%, compared to Option A at 58% and Option B at 67%. Our recommendation is
Option C." This statement is supported by three simultaneously-visible data points (Zone 1A
curves, Zone 1B crossing status, Zone 1D PSP values) — not by sequential navigation.

*Does this change what the team can argue?* Yes, specifically. Before G2 Phase 3, the ministry
team could compare two options at a time — the third option required a context switch and memory
of the prior comparison. Under a 90-second reactive ceiling, this sequential comparison
structure disadvantaged the team relative to a negotiating counterpart who could hold all three
option profiles in memory simultaneously. After G2 Phase 3, the tool holds all three profiles
simultaneously on the primary surface. The ministry team's working memory is freed to focus on
the argument, not on the comparison logistics.

The north star question — "does this make the tool more useful to a finance minister in that
moment?" — is answered by the observable outcome: Aicha Mbaye can say "Option C" and cite three
independent supporting data points, all from one viewport observation, in under 90 seconds,
without opening a drawer or switching views. The argument is available at the table, not after it.

**North star test verdict:** PASS — specific. Names the Demo 7 Act 2 scenario (Zambia restructuring,
three-option panel presentation), the capability evaluated (simultaneous N=3 comparison vs. sequential
two-at-a-time), the concrete argument enabled ("Option C does not cross the poverty threshold; 74% PSP
dominates"), and the mechanism by which the capability changes what can be said at the table (primary
surface simultaneity removes working-memory burden under 90-second reactive ceiling). Not aspirational.

---

## Section 4 — Open Rejections

No open rejections. ACCEPT verdict recorded in Section 3. No REJECT verdicts issued.

**Near-miss entries required for each rejection:** N/A — no rejections in G2 Phase 3.

---

## Section 5 — PI Agent Sprint Exit Confirmation

**Exit conditions checklist (PI Agent):**

- [x] **All implementation groups merged; CI green on release branch (Section 2)**
  PR #1311 merged 2026-06-25; PR #1314 merged 2026-06-26. Both to `release/m17`.
  CI green on `release/m17` — playwright-e2e PASS (8m25s), lint PASS, test-backend PASS,
  compliance-scan PASS, branch-naming PASS, changes PASS, backtesting SKIPPED.
  Frontend pre-push build gate confirmed for both PRs (exit 0, TypeScript clean, 619 modules).
  No soft-skip patterns in E2E test file (NM-056 compliant).

- [x] **Business PO ACCEPT verdict filed for each user-facing deliverable (Section 3)**
  #394 ACCEPT verdict filed in Section 3, dated 2026-06-26. One deliverable, one verdict.

- [x] **Customer Agent Layer 3 assessment on record for all Persona 2/3/5 deliverables (Section 3)**
  #394 serves Personas 1, 3, and 5. All three Layer 3 assessments filed in Section 3 before
  the BPO verdict. All three: PASS, no CA conditions raised. Layer 3 → BPO verdict sequence satisfied.

- [x] **No open rejection artifacts (Section 4)**
  No rejections in G2 Phase 3. Zero REJECT verdicts on record.

- [x] **Near-miss entry filed for each rejection (Section 4)**
  N/A — no rejections.

- [x] **North star test artifact on record (Section 3)**
  Filed in Section 3 above. Specific: names the Demo 7 Act 2 scenario (Zambia restructuring,
  three-option panel presentation), the concurrent capability enabled versus the sequential
  constraint before G2, and the exact argument Aicha Mbaye can make at the table from the
  primary viewport alone. Not aspirational.

**Step 4 Verify source code checks recorded:**

- `__worldsim_setComparisonScenarios` window function: present in App.tsx DEV useEffect, guarded
  by `import.meta.env.DEV` — eliminated from production builds. ✅
- `comparisonScenarios` state typed as `ScenarioComparisonConfig[]`: imported from TrajectoryView.tsx,
  defaulting to `[]` (not null). Non-empty guard on prop: `comparisonScenarios.length > 0 ? comparisonScenarios : undefined`. ✅
- `zone1a-curve-scenario-{slug}` pattern: slug derived from `sc.scenarioId.replace(/^[a-z]{3}-/, "")` —
  `zmb-option-a` → `option-a`. Consistent between component and E2E test expectations. ✅
- `loadedComparisonScenarios` useEffect in ScenarioInstrumentCluster: `comparisonScenariosKey`
  dependency (scenario IDs joined with `,`) triggers refetch when scenario set changes. ✅
- PSP extraction: `political_economy.indicators.programme_survival_probability.value` from
  trajectory response — consistent with Zone 1D's live-data path for the primary scenario. ✅

**PI Agent sprint exit verdict: CONFIRMED — all exit conditions satisfied**

**PI Agent confirmation:**

> G2 Phase 3 sprint exit conditions are satisfied as of 2026-06-26.
>
> The G2 Phase 3 deliverable (#394 — N>2 multi-scenario comparison) is fully merged to
> `release/m17` across two PRs: PR #1311 (component layer, merged 2026-06-25) and PR #1314
> (App.tsx wiring + E2E test activation, merged 2026-06-26). CI is green on both —
> playwright-e2e PASS (8m25s) confirmed at PR #1314 merge.
>
> Business PO ACCEPT verdict on record (Section 3, dated 2026-06-26). Customer Agent Layer 3
> assessments for Personas 1, 3, and 5 filed before verdict — all three PASS, no CA conditions
> raised. North star test artifact filed and specific: Demo 7 Act 2 Zambia restructuring
> scenario named; three-option simultaneous comparison capability versus sequential two-at-a-time
> constraint named; "Option C does not cross the poverty threshold; 74% PSP dominates" argument
> identified as the concrete output enabled. Not aspirational.
>
> Seven E2E ACs (AC-S1, AC-A1, AC-B1, AC-D1, AC-P5, AC-P1, AC-P3) all hard-asserted in
> CI — no soft-skip patterns, NM-056 compliant. DEMO4 check PASS: Zone 1A curves, Zone 1B
> crossing rows, and Zone 1D PSP values all derive from fixture-distinct trajectory API data.
> Kryptonite check PASS: no drawer, no hover, no view-switch required for the primary
> observable states.
>
> Step 4 Verify source code checks complete: window function DEV-guarded, comparisonScenarios
> non-empty guard on prop, slug pattern consistent with test expectations, useEffect dependency
> key confirmed, PSP extraction path consistent with Zone 1D live-data pattern.
>
> No near-misses required — clean sprint exit. The ghost branch confusion (`b8f9f85` landing
> on `feat/m17-g3-zone-1b-allocation`) was resolved without process harm by cherry-picking
> onto a clean `feat/m17-g2-wiring` branch; the G3 PR (#1313) remains open with correct
> base-relative diff once G2 merges. Not a near-miss — no artifact was at risk and no
> process gate was bypassed.
>
> **G2 Phase 3 is CLOSED as of 2026-06-26. Issue #394 may be closed.**
>
> — PI Agent, 2026-06-26

---

## Sprint Exit Artifact Statement

This document is the sprint exit artifact for M17-G2 Phase 3. It supersedes any informal
exit notation in `SESSION_STATE.md` for this sprint. It is filed at
`docs/process/sprint-plans/m17-g2-sprint-exit.md`.

The PI Agent confirmation in Section 5 is the gate. G2 Phase 3 is closed as of 2026-06-26.

**Downstream actions:**
- Issue #394: close — G2 Phase 3 complete, BPO ACCEPT on record
- #982 exit checklist: note G2 Phase 3 CLOSED
- SESSION_STATE.md: update #394 row to BPO ACCEPT + sprint exit CONFIRMED
