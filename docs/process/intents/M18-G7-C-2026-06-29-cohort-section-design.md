---
name: M18-G7-C-cohort-section-design
type: implementation-intent
issues:
  - "#1463 — DEMO-134: Informal workers row absent (CohortImpactSection alert-only surface)"
  - "#1469 — DEMO-140: Temporal contradiction in Zone 1B (historical breach = current CRITICAL)"
status: Filed — ADR-010 Amendment 2 accepted (2026-06-29); all gates CLEAR
authored-by: Frontend Architect Agent
authored-date: 2026-06-29
implementing-agent: Frontend Architect Agent
sprint-entry: docs/process/sprint-plans/m18-g7-sprint-entry.md
adr-reference: "ADR-010 Amendment 2 — CohortImpactSection monitored-row state (accepted 2026-06-29)"
governing-adrs:
  - "ADR-010 Decision 4 — Shared step state architecture"
  - "ADR-010 Amendment 2 — Monitored-row state + temporal disambiguation"
root-cause-reference: docs/demo/m18/reviews/2026-06-29-g7-root-cause-analysis.md
release-branch: release/m18
bpo-acceptance-required: "No — CRITICAL bug fix; monitored-row is a corrective capability, not a new feature"
customer-agent-l3-required: "No — bug fix restoring the primary Demo 7 Act 1 argument surface"
ux-implementation-brief-conditions:
  - "MV-001 CVD gate: green #2e7d32 (CLEAR) vs. red #c62828 (CRITICAL) — document CVD coverage in PR description"
  - "Severity-aware ordering: CRITICAL/TERMINAL focal rows render first; CLEAR focal rows render after all CRITICAL/TERMINAL rows (focal or breach-only) but before WARNING rows"
---

# Implementation Intent: M18-G7-C — CohortImpactSection Monitored-Row State

> **Pre-implementation prerequisites (all required before implementation PR opens):**
> - [x] G7-0 root cause analysis filed and EL-approved (2026-06-29)
> - [x] ADR-010 Amendment 2 accepted by EL (2026-06-29) — specifies monitored-row state, temporal disambiguation, data source
> - [x] UX Designer separate-session sign-off on ADR-010 Amendment 2 (2026-06-29) — 2 non-blocking conditions become implementation-brief requirements (see §0 Constraint 3 and §0 Constraint 4)
> - [ ] QA tests authored and committed (red) before implementation code

---

## 0. Implementation Constraints

*Authority: G7-0 root cause analysis §Root Cause 3 + ADR-010 Amendment 2 (accepted 2026-06-29). The two non-blocking UX Designer concerns are implementation-brief requirements here.*

1. **Data source: `scenarios.configuration` JSONB key `monitored_focal_cohorts`.** Focal indicator designation is read from the scenario's configuration field. Do not hardcode the indicator key in the component. For the Demo 7 SEN fixture, `createSenScenario` must include `monitored_focal_cohorts` in its configuration (see §6).

2. **Monitored focal rows render first in `CohortImpactSection` — with severity-aware ordering.** UX Designer non-blocking concern 2 (ordering rule): focal rows in CRITICAL/TERMINAL state render at the top of `CohortImpactSection`; CLEAR-state focal rows render after all CRITICAL/TERMINAL rows (focal or breach-only from `crossings` store) but before WARNING rows. HIST-state focal rows (prior breach, now clear) render with CLEAR-state focal rows.

3. **CVD compliance — MV-001 gate coverage required.** UX Designer non-blocking concern 1: green `#2e7d32` (CLEAR badge) and red `#c62828` (CRITICAL badge) are indistinguishable under deuteranopia. Text labels (CLEAR / CRITICAL / HIST) are the primary signal and provide adequate disambiguation. The implementation PR description must include a note confirming the new Zone 1B CLEAR/CRITICAL badge pair is included in the MV-001 CVD validation gate.

4. **Three and only three row states for focal indicators:** CLEAR (green `#2e7d32`), BREACHED-current (red `#c62828`), PRIOR BREACH NOW CLEAR / HIST (amber `#a06000`). No other badge color is introduced. Badge text labels: "CLEAR", "CRITICAL", "HIST".

5. **Temporal disambiguation applies to all rows, not only focal rows.** Breach-only rows from the `crossings` store that have `crossing.step_index < current_step` also transition to amber "HIST" badge with the "Breached at step N —" prefix. This resolves DEMO-140 for all rows, not only the designated focal indicator.

6. **No new network requests.** All focal row state is derived from existing shared step atom fields: `current_step`, `trajectory`, `crossings`. The `monitored_focal_cohorts` configuration is read from the scenario object already present in component props or store.

7. **DEMO-151 (HD trajectory in Zone 1A comparison mode) is M19 scope — do not implement.**

---

## 1. Source

**Issues:** #1463 (DEMO-134), #1469 (DEMO-140)

**Root cause document:** `docs/demo/m18/reviews/2026-06-29-g7-root-cause-analysis.md §Root Cause 3`

**Governing ADR:** ADR-010 Amendment 2 (monitored-row state — accepted 2026-06-29). ADR-010 Decision 4 (shared step state atom — derivation source).

**Demo 7 anchor:** Act 1 (Senegal Mode 3, step 6). The primary Act 1 finding is: "the bottom quintile informal workers poverty headcount remains at 0.450 — ten points above the 0.40 recovery floor." This is a CLEARED threshold finding. The current `CohortImpactSection` shows only BREACHED indicators — the CLEAR finding is structurally invisible. This fix makes it visible as a designated focal indicator row.

---

## 2. Persona Trace (abbreviated — bug fix with new state)

**Personas affected:** Persona 1 (Lucas — reads focal indicator to verify counter-proposal achieves CLEAR state); Persona 2 (Eleni — cites focal row at negotiating table: "Under our counter-proposal, this indicator remains 10 points above the floor").

**Capability before fix:** Demo 7 Act 1's primary human cost argument is structurally invisible — the CLEAR focal indicator row does not render. Only BREACHED indicators appear. The analyst cannot cite the CLEAR finding from Zone 1B.

**Capability after fix:** `bottom_quintile_informal_workers_poverty_headcount` renders as a designated focal indicator row at every step (CLEAR, BREACHED, or HIST as appropriate). At step 6 counter-proposal state: CLEAR badge, value 0.450, floor 0.400.

**North star relevance:** The Senegalese finance ministry analyst can say at the table: *"Zone 1B is showing CLEAR — the informal workers headcount is 0.450, ten points above the 0.40 floor. Under our counter-proposal, this threshold is not crossed."* Before this fix: the analyst has no Zone 1B surface for this claim.

---

## 3. Observable Application State

### 3.1 Primary observable state

**In SEN Mode 3 comparison at step 6 (counter-proposal branch active, threshold not crossed):**

`[data-testid="focal-cohort-row"]` is present in the DOM within `[data-testid="cohort-impact-section"]`. It contains:
- Indicator display name (human-readable, not raw key)
- Current value: "0.450" (3 decimal places)
- Floor value: "0.400"
- Badge element with text "CLEAR" and green background `#2e7d32`
- T3 confidence badge present

### 3.2 Secondary observable states

**State A — BREACHED focal row:**
When counter-proposal is NOT applied (baseline at step 4 where threshold is crossed): `focal-cohort-row` renders with CRITICAL red badge.

**State B — HIST focal row (prior breach, now clear):**
When focal indicator was BREACHED at step 1 and CLEAR at step 6: `focal-cohort-row` renders with amber (#a06000) "HIST" badge and prefix "Breached at step 1 —".

**State C — Historical breach rows in existing crossings (DEMO-140):**
For `crossings` entries where `step_index < current_step`, the breach row renders with amber badge ("HIST") and "Breached at step N —" prefix. At current step = 6 with crossing at step 1: existing agricultural workers row shows amber "HIST", not red "CRITICAL".

**State D — Focal row ordering (severity-aware):**
Focal row in CLEAR state renders AFTER all CRITICAL and TERMINAL rows (focal or breach-only). Focal row in CRITICAL state renders at the top. At step 6 (focal = CLEAR, existing crossings = HIST amber): focal CLEAR row renders after existing HIST rows (which are now amber, not promoted to CRITICAL priority).

**State E — No focal rows when not configured:**
In a scenario with no `monitored_focal_cohorts` key in configuration: `cohort-impact-section` renders breach-only rows as before (no regressions to existing single-scenario behaviour).

### 3.3 Silent failure detection

**Silent failure — focal row absent despite configuration:**
`monitored_focal_cohorts` is present in `createSenScenario` configuration but `focal-cohort-row` does not render. Observable via testid presence check.

**Silent failure — HIST amber not applied to historical breach rows:**
At step 6 with crossing at step 1, existing agricultural workers row still shows red CRITICAL badge. Observable via badge background color check.

**Silent failure — ordering inversion:**
CLEAR focal row renders before a CRITICAL breach-only row in the DOM. Observable via DOM order check (CRITICAL row must have `compareDocumentPosition(CRITICAL, CLEAR) === DOCUMENT_POSITION_FOLLOWING`).

---

## 4. Acceptance Criteria

**AC-C1 (E2E — focal row present when configured):**
In SEN Mode 3 with `monitored_focal_cohorts` configured (`bottom_quintile_informal_workers_poverty_headcount`, floor 0.40), at step 6 with counter-proposal branch active: `[data-testid="focal-cohort-row"]` is present within `[data-testid="cohort-impact-section"]`. The element has non-zero dimensions.
*Source: §3.1 + ADR-010 Amendment 2 §Monitored Focal Indicators*

**AC-C2 (E2E — CLEAR badge when value above floor):**
When focal indicator current value (0.450) > floor (0.400), `focal-cohort-row` contains a badge element with text content "CLEAR" and computed background-color corresponding to `#2e7d32` (green). Value "0.450" and floor "0.400" are rendered as text within the row.
*Source: §3.2 + ADR-010 Amendment 2 §Monitored-row states table*

**AC-C3 (E2E — HIST amber for historical breach rows, DEMO-140):**
In SEN Mode 3 at step 6 (with crossing at step 1 for agricultural workers): `[data-testid="cohort-impact-row"][data-crossing-step="1"]` (or equivalent) renders with badge text "HIST" and background-color corresponding to `#a06000` (amber). A badge with text "CRITICAL" and red background does NOT appear for this row at step 6.
*Source: §3.2 State C + ADR-010 Amendment 2 §Temporal Disambiguation*

**AC-C4 (E2E — severity-aware focal row ordering):**
In a scenario where a CRITICAL breach-only row and a CLEAR focal row both exist at the current step: the CRITICAL breach row appears before the CLEAR focal row in the DOM. Observable via `compareDocumentPosition`.
*Source: §0 Constraint 2 + ADR-010 Amendment 2 + UX Designer concern 2*

**AC-C5 (E2E — no focal rows when not configured):**
In ZMB Option A (no `monitored_focal_cohorts` in configuration): `[data-testid="focal-cohort-row"]` is absent from the DOM. Existing breach-only rows render normally.
*Source: §3.2 State E + ADR-010 Amendment 2 §Data source*

**AC-C6 (implementation — CVD gate documented):**
The G7-C implementation PR description includes a statement: "MV-001 CVD validation gate: CLEAR (#2e7d32) vs. CRITICAL (#c62828) badge pair included in CVD validation. Text labels are the primary signal. [Pass/Fail confirmation of CVD simulation run.]"
*Source: §0 Constraint 3 + UX Designer concern 1*

---

## 5. Kryptonite Constraint Check

No kryptonite risk from this fix — the monitored-row state is a declarative text display, not a new interaction paradigm. The badge text labels (CLEAR / CRITICAL / HIST) are the primary signal per the UX Designer review, which correctly noted that Persona 2 (Eleni) reads Zone 1B for declarative findings to cite, not for colour coding.

---

## 6. Backend / Data Specification

### 6.1 — SEN scenario fixture update

`createSenScenario` in `frontend/tests/e2e/demo-narrated.spec.ts` must include `monitored_focal_cohorts` in the scenario configuration:

```typescript
configuration: {
  // ... existing fields ...
  monitored_focal_cohorts: [
    {
      indicator_key: "bottom_quintile_informal_workers_poverty_headcount",
      floor_value: 0.40,
      floor_label: "Recovery floor",
      framework: "human_development"
    }
  ]
}
```

### 6.2 — Current value retrieval

The component must read the focal indicator's current value from the trajectory data (shared step atom `state.trajectory`) at `current_step`. If the trajectory does not include this indicator key for the current step, the focal row renders with a "—" current value (not an error state).

### 6.3 — No backend changes required

The `monitored_focal_cohorts` key is a frontend scenario configuration field read at the component level. No backend endpoint change, no database migration, no new API field is required for M18 G7. The backend scenario configuration already stores JSONB fields in `scenarios.configuration`.

---

## 7. Out of Scope

- DEMO-151 (HD trajectory in Zone 1A comparison mode) — M19 scope, explicitly out of scope
- Runtime focal indicator designation by the user (scenario-level JSONB only in M18)
- Focal row interactions (expand, drill-down) beyond the basic row display specified above
- Zone 1A changes of any kind

---

## 8. Test Authorship Obligation

**QA file:** `frontend/tests/e2e/demo-cohort-section.spec.ts` (new file)

**Test authorship deadline:** E2E tests authored and committed to `feat/m18-g7-cluster-c` BEFORE implementation code changes. Tests must run red before fix, green after.

| AC | Test type | Playwright check |
|---|---|---|
| AC-C1 | E2E | `focal-cohort-row` present when `monitored_focal_cohorts` configured |
| AC-C2 | E2E | CLEAR badge text + green color when value > floor |
| AC-C3 | E2E | Amber HIST badge for historical crossing rows at step 6 |
| AC-C4 | E2E | CRITICAL row before CLEAR focal row in DOM |
| AC-C5 | E2E | No focal row when not configured (ZMB scenario) |
| AC-C6 | PR description | CVD gate statement — not an automated test |

**Pre-push gates:** `cd frontend && npm run build` must exit 0.

*Filed: 2026-06-29. Authority: docs/process/agents.md §Frontend Architect Agent.*
