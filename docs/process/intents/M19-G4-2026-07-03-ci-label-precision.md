---
name: M19-G4-ci-label-precision
type: implementation-intent
adr: ADR-007 Amendment 1 (ARCH-016) §8.7 — display contract for band_method states
issues: "#1529"
status: Filed
authored-by: PM Agent
authored-date: 2026-07-03
implementing-agent: Frontend Architect Agent
sprint-entry: docs/process/sprint-plans/m19-g4-sprint-entry.md
---

# Implementation Intent: G4 — CI Label Precision Fix (#1529)

## 1. Source Issue and Architecture Authority

**Issue:** #1529 — fix(zone1b): '95% CI' label on DistributionalComparisonSummary overstates
statistical precision — consider 'declared interval' or tooltip (DEMO-163)
**ADR prerequisite:** ADR-007 Amendment 1 (ARCH-016) §8.7 — ACCEPTED 2026-07-03. §8.7 establishes
the four-state display contract for `band_method` and delegates label text strings to G4 #1529.
G3 #1537 delivered the `data-testid="ci-calibration-status"` structural element; G4 delivers
the text for each state.
**Authored by:** PM Agent
**Date:** 2026-07-03
**Implementing agent:** Frontend Architect Agent

**Architecture authority:**
This deliverable has two distinct changes, both pure frontend, no backend modification:

**Deliverable A — `ci-calibration-status` label text (Demo 8 gate):**
G3 #1537 created `data-testid="ci-calibration-status"` in the CI label component and left
text content empty — delegated to G4. ADR-007 Amendment 1 §8.7 establishes four `band_method`
states. G4 fills in the exact text for each state. This is the Demo 8 Act 2 gate: "G4 #1529
CI label text for `PRE_CALIBRATION_PROVISIONAL_DIRECTIONAL` state must land"
(SESSION_STATE.md Demo 8 Open Conditions).

**Deliverable B — DistributionalComparisonSummary label fix:**
`MDAAlertPanelZone1B.tsx` line 801 renders `"95% CI"` as the interval label on the
DistributionalComparisonSummary. This label overstates statistical precision — the BandingEngine
produces a structural uncertainty model (step-based half-width schedule, tier multiplier),
not a frequentist confidence interval. Fix: replace `"95% CI"` with `"declared interval"` and
add a tooltip explaining the structural model. The Zone 3 methodology panel (`▶ Methodology`,
`data-testid="methodology-panel-toggle"`) already provides full methodological context; the
label change removes the first-impression precision overclaim.

**G3 coordination gate satisfied:**
The four `band_method` enum values (`PRE_CALIBRATION_STRUCTURAL_PRIOR`,
`PRE_CALIBRATION_PROVISIONAL_DIRECTIONAL`, `BAYESIAN_POSTERIOR_CALIBRATED`,
`SUPPRESSED_MEANINGLESS`) were frozen in the G3 #1537 merge. G4 reads these values from the
merged code; this intent document does not rename or extend them.

---

## 2. Persona Trace Elements Targeted

**P-1 — Persona served:**
Primary: Persona 1 (Lucas Ferreira, IMF Senior Economist) — raised DEMO-163 explicitly: "This
label implies a statistical precision the methodology does not claim." Lucas is the challenge
persona for statistical precision language in a programme review setting.
Secondary: Persona 2 (Eleni, Ministry of Finance analyst) — will cite the comparison summary
label in programme review submissions. If the label says "95% CI" in a formal submission, it
becomes a first-impression overclaim that the creditor team can challenge.

**P-2 — Entry state:**
Scenario comparison is active (two or more scenarios loaded); Zone 1B DistributionalComparison-
Summary is visible at the sticky bottom; the methodology panel (Zone 3) is closed. Lucas is
reading the summary sentence — he has not yet clicked "▶ Methodology". The "95% CI" label is
the first data label he encounters.

**P-3 — Journey step:**
Programme Review journey (Persona 1 — analytical session). Lucas is reading the comparison
summary before the negotiating team presents it to the IMF board. He flags that "95% CI" will
be challenged by IMF statisticians who will know the interval is structural, not frequentist.

**P-4 — Time/interaction ceiling:**
Label change: zero user interaction — the label is always visible. Tooltip: appears on hover
within 500ms. No ceiling concern for either deliverable.

**P-6 — Negotiating leverage delivered:**
Persona 2 (Eleni) can cite the comparison summary in a programme review submission using the
label "declared interval — BandingEngine structural uncertainty model" without triggering an
IMF statistical challenge. The Zone 3 methodology panel answers "how was this interval computed?"
and the label no longer makes a claim the methodology does not support.

**P-7 — North star capability delivered:**
Lucas (Persona 1, IMF Senior Economist) reads the comparison summary at Demo 8 and cannot
challenge the precision label — because it no longer overclaims. The ministry team enters the
programme review session with defensible interval language and a calibration status disclosure
that matches the actual `band_method` state (`PRE_CALIBRATION_PROVISIONAL_DIRECTIONAL` at Demo 8
Act 2).

---

## 3. Observable Application State

### 3.1 Deliverable A — ci-calibration-status text

The CI label component (in `TrajectoryView.tsx` or the zone rendering the trajectory CI bands)
has a `data-testid="ci-calibration-status"` element. After G4, this element has non-empty text
content for all non-suppressed `band_method` states:

| `band_method` value | Expected `ci-calibration-status` text |
|---|---|
| `"PRE_CALIBRATION_STRUCTURAL_PRIOR"` | `"structural prior — not yet empirically calibrated"` |
| `"PRE_CALIBRATION_PROVISIONAL_DIRECTIONAL"` | `"provisional — directional calibration only"` |
| `"BAYESIAN_POSTERIOR_CALIBRATED"` | `"empirically calibrated interval"` |
| `"SUPPRESSED_MEANINGLESS"` | (element absent — CI bounds hidden per G3 §4 display contract) |

**Demo 8 gate:** At Demo 8 Act 2, the ZMB/SEN scenario will be in state
`PRE_CALIBRATION_PROVISIONAL_DIRECTIONAL`. `data-testid="ci-calibration-status"` must be
present and contain `"provisional — directional calibration only"` exactly.

### 3.2 Deliverable B — DistributionalComparisonSummary label

At `1440×900` with a comparison session active (two scenarios loaded, Zone 1B
DistributionalComparisonSummary visible):

- The interval label previously rendered as `"95% CI"` now renders as `"declared interval"`
- A tooltip is present on the label: hovering `data-testid="distributional-ci-label"` for ≥ 500ms
  shows the tooltip text: `"Structural uncertainty model — BandingEngine step-based schedule; not
  a frequentist confidence interval. See methodology panel for details."`
- The rest of the comparison summary sentence is unchanged:
  `"298K – 398K  declared interval"` (or the values from the current fixture)

### 3.3 Silent failure detection

**SF-1 (ci-calibration-status present but empty):** G3 #1537 created the element; if G4 does
not wire in the text content, the element is present but has empty `.textContent`. Detection:
assert `.textContent.trim().length > 0` on `ci-calibration-status` for each non-suppressed state.
This is the Demo 8 gate failure mode — G3 conditional PASS becomes FAIL.

**SF-2 (distributional CI label unchanged — "95% CI" still rendered):** G4 implementation PR
did not update line 801 of `MDAAlertPanelZone1B.tsx`. Detection: assert that
`data-testid="distributional-ci-label"` text does NOT contain "95% CI" and DOES contain
"declared interval". A test that only checks the tooltip without checking the label text has
not guarded SF-2.

**SF-3 (tooltip present but empty):** The `title` attribute or tooltip element is present but
has empty text. Detection: assert tooltip text length > 0 on hover of `distributional-ci-label`.

---

## 4. Acceptance Criteria

**AC-1 (STRUCTURAL_PRIOR state — ci-calibration-status text):**
In a scenario where `band_method="PRE_CALIBRATION_STRUCTURAL_PRIOR"` for the financial
framework at step 2, when the trajectory is displayed, then
`data-testid="ci-calibration-status"` has text content
`"structural prior — not yet empirically calibrated"`.

**AC-2 (PROVISIONAL_DIRECTIONAL state — ci-calibration-status text — Demo 8 gate):**
In a scenario where `band_method="PRE_CALIBRATION_PROVISIONAL_DIRECTIONAL"` for the financial
framework at step 2, when the trajectory is displayed, then
`data-testid="ci-calibration-status"` has text content
`"provisional — directional calibration only"` and `.textContent.trim().length > 0`.

**AC-3 (BAYESIAN_POSTERIOR_CALIBRATED state — ci-calibration-status text):**
In a scenario where `band_method="BAYESIAN_POSTERIOR_CALIBRATED"` for the financial framework
at step 2, when the trajectory is displayed, then `data-testid="ci-calibration-status"` has
text content `"empirically calibrated interval"`.

**AC-4 (SUPPRESSED_MEANINGLESS state — ci-calibration-status absent):**
In a scenario where `band_method="SUPPRESSED_MEANINGLESS"` for a framework, when the trajectory
is displayed, then `data-testid="ci-calibration-status"` is NOT present in the DOM (consistent
with G3 §4 display contract: CI bounds hidden, suppression message shown instead).

**AC-5 (distributional CI label — "declared interval" replaces "95% CI"):**
In a comparison session with two scenarios loaded (Zone 1B DistributionalComparisonSummary
visible), then `data-testid="distributional-ci-label"` text content is `"declared interval"`
and does NOT contain the string `"95%"` or `"CI"` alone.

**AC-6 (distributional CI label — tooltip present with correct text):**
In the same comparison session, when `data-testid="distributional-ci-label"` is hovered,
then a tooltip (via `title` attribute or tooltip element) is visible and contains the text
`"Structural uncertainty model"` and `"BandingEngine"` and `"not a frequentist confidence
interval"`.

**AC-7 (SF-1 guard — ci-calibration-status non-empty for PROVISIONAL state):**
In a scenario with `band_method="PRE_CALIBRATION_PROVISIONAL_DIRECTIONAL"`, assert
`data-testid="ci-calibration-status"` `.textContent.trim()` has `.length > 0`.
(This directly guards the Demo 8 gate failure mode.)

**AC-8 (SF-2 guard — "95% CI" string absent from comparison summary):**
In a comparison session, assert that the full rendered text of the
`data-testid="distributional-comparison-summary"` container does NOT contain the exact string
`"95% CI"`.

**AC-9 (regression — G3 suppression text unchanged):**
In a scenario with `band_method="SUPPRESSED_MEANINGLESS"`, the CI band slot shows exactly
`"Data range too wide for confidence interval"` (the G3-specified string — verify G4 did not
alter it).

---

## 4b. Visual Spec (before/after)

**AC-5/AC-6/AC-8 — DistributionalComparisonSummary (before):**
```
Viewport: 1440×900 | Zone: Zone 1B sticky-bottom | data-testid="distributional-comparison-summary"

DISTRIBUTIONAL COMPARISON  step 8          T3     ▶ Methodology
Poverty headcount differential
  Option A vs. Option C    +342,700 persons
  298K – 398K  95% CI          ← "95% CI" here is the overclaim
→ Direction stable across uncertainty range
```

**AC-5/AC-6 — DistributionalComparisonSummary (after):**
```
Viewport: 1440×900 | Zone: Zone 1B sticky-bottom | data-testid="distributional-comparison-summary"

DISTRIBUTIONAL COMPARISON  step 8          T3     ▶ Methodology
Poverty headcount differential
  Option A vs. Option C    +342,700 persons
  298K – 398K  declared interval  [data-testid="distributional-ci-label"]
               ↑ hover → tooltip: "Structural uncertainty model — BandingEngine step-based
                                   schedule; not a frequentist confidence interval.
                                   See methodology panel for details."
→ Direction stable across uncertainty range
```

**AC-1 / AC-2 / AC-3 — ci-calibration-status element (after, by state):**
```
Viewport: 1440×900 | Zone: Zone 1A TrajectoryView CI band | data-testid="ci-calibration-status"

State STRUCTURAL_PRIOR:
  [CI band rendered normally]
  data-testid="ci-calibration-status": "structural prior — not yet empirically calibrated"

State PROVISIONAL_DIRECTIONAL (Demo 8 Act 2 state):
  [CI band rendered normally]
  data-testid="ci-calibration-status": "provisional — directional calibration only"

State BAYESIAN_POSTERIOR_CALIBRATED:
  [CI band rendered normally]
  data-testid="ci-calibration-status": "empirically calibrated interval"

State SUPPRESSED_MEANINGLESS (G3 §4 — unchanged by G4):
  [CI bounds hidden]
  "Data range too wide for confidence interval"
  data-testid="ci-calibration-status": (absent)
```

---

## 5. Kryptonite Constraint Check

**Does this implementation's primary observable state require specialist mediation for Persona 2
to act on it in the Reactive entry state (90-second ceiling)?**

`[x]` No — "declared interval" and `"provisional — directional calibration only"` are
interpretable by Persona 2 (Eleni, ministry analyst) and Persona 1 (Lucas, IMF economist)
without specialist translation.

**Rationale:** The label `"declared interval"` tells a non-statistician that this is a stated
range — not an inferred or computed probability interval. The tooltip provides the technical
context for those who need it (Lucas). The `ci-calibration-status` text `"provisional —
directional calibration only"` is self-describing: the analyst knows the CI is calibrated
provisionally and the evidence is directional. The Zone 3 methodology panel (already present,
one click) answers "what does this mean in detail?"

No mediation required. The level of disclosure matches the practitioner audience without
demanding specialist interpretation.

---

## 6. Out of Scope

- **`band_method` propagation to DistributionalSummaryData** — the `DistributionalSummaryData`
  type does not currently carry a `band_method` field. G4 #1529 changes the label
  unconditionally ("declared interval" always) rather than conditionally per `band_method`. A
  conditional label on the distributional comparison (e.g., showing "provisional" when the
  distributional CI is derived from a provisional banding state) is deferred to M20. The
  unconditional label change is sufficient to resolve DEMO-163.
- **Trajectory CI label text above `"declared interval"`** — the trajectory CI label component
  gains calibration-state text via `ci-calibration-status`; it does not gain a secondary
  "declared interval" label. The calibration-status element is the primary precision disclosure
  for trajectory bands. Adding a redundant "declared interval" label on top of the calibration
  status would be duplication.
- **Methodology panel content changes** — Zone 3 (`▶ Methodology` panel in
  DistributionalComparisonSummary) is unchanged. G4 does not modify `methodology_detail` content
  or the existing methodology panel expand/collapse behaviour.
- **`"95% CI"` label in other components** — only the `DistributionalComparisonSummary` line 801
  (`MDAAlertPanelZone1B.tsx`) is changed. If `"95% CI"` appears elsewhere in the frontend, those
  are out of scope for G4.
- **Backend label computation** — no backend changes. All changes are in frontend components.

---

## 7. Test Authorship Obligation

**QA Lead:** QA Lead Agent
**Test authorship deadline:** Before any G4 implementation PR opens on `sprint/m19-g4`
**Test file location:** `frontend/tests/e2e/m19-g4-ci-label-precision.spec.ts`

**NM-086 gate:** Deliverable A reads `band_method` from the trajectory API response. The QA Lead
must confirm that:
1. `band_method` is declared in `docs/schema/api_contracts.yml §trajectory` (per-framework-point
   field — added by G3 #1537 in the same PR that updated api_contracts.yml)
2. Any E2E mock helper that stubs `band_method` for the four states uses the exact enum strings
   from the merged G3 #1537 code (not from this document) before filing the acknowledgment below.

Deliverable B reads no new API fields — `DistributionalSummaryData` shape is unchanged.
No new mock routes for Deliverable B.

**Required test coverage (Playwright E2E):**

- **AC-1:** Load ZMB scenario; mock trajectory response with `band_method="PRE_CALIBRATION_STRUCTURAL_PRIOR"` on financial framework at step 2; assert `ci-calibration-status` text is `"structural prior — not yet empirically calibrated"`.
- **AC-2:** Mock `band_method="PRE_CALIBRATION_PROVISIONAL_DIRECTIONAL"`; assert `ci-calibration-status` text is `"provisional — directional calibration only"` and length > 0 (SF-1 guard).
- **AC-3:** Mock `band_method="BAYESIAN_POSTERIOR_CALIBRATED"`; assert `ci-calibration-status` text is `"empirically calibrated interval"`.
- **AC-4:** Mock `band_method="SUPPRESSED_MEANINGLESS"`; assert `ci-calibration-status` not in DOM (G3 suppression path).
- **AC-5:** Load comparison session (two scenarios); assert `distributional-ci-label` text is `"declared interval"` and does NOT contain `"95%"`.
- **AC-6:** Hover `distributional-ci-label`; assert tooltip text contains `"Structural uncertainty model"` and `"BandingEngine"` and `"not a frequentist confidence interval"`.
- **AC-7 (SF-1 guard):** Same as AC-2 — assert `.textContent.trim().length > 0`. Write as a separate assertion block so the guard is visible as a distinct test.
- **AC-8 (SF-2 guard):** In comparison session; assert full text of `distributional-comparison-summary` does NOT contain `"95% CI"` as a substring.
- **AC-9 (G3 regression):** Mock `band_method="SUPPRESSED_MEANINGLESS"`; assert CI band slot shows exactly `"Data range too wide for confidence interval"` (G3 string unchanged).

**QA Lead acknowledgment:**
`[ ]` QA Lead: Tests for AC-1 through AC-9 authored and filed. [Date]
`[ ]` QA Lead: `band_method` confirmed declared in `api_contracts.yml §trajectory` per-framework
fields before mock helpers authored. Enum strings taken from merged G3 #1537 code. [Date]

---

*Intent document version: 2026-07-03. ADR prerequisite: ARCH-016 accepted 2026-07-03.
Sprint entry: `docs/process/sprint-plans/m19-g4-sprint-entry.md`.
See `docs/process/agent-execution-lifecycle.md` for the five-step lifecycle this document gates.*
