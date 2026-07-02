---
name: ADR-021-constraint-floor-search
type: architecture-decision-record
adr-number: 21
arch-backlog-entry: ARCH-015
issues:
  - "#1540 — Mode 3 constraint-floor search"
status: accepted
tier: 1
authored-by: Architect Agent
authored-date: 2026-07-02
accepted-date: 2026-07-02
panel:
  - "Architect Agent (R — author)"
  - "Frontend Architect Agent (C — ControlPlaneColumn rendering, Form 3 layout, result display)"
  - "Computation Engine Agent (C — binary search algorithm, endpoint design, convergence contract)"
  - "Chief Methodologist (C — uncertainty display for boundary results, floor value defensibility)"
  - "UX Designer Agent (independent sign-off ✓ 2026-07-02, separate EL-triggered session, NM-042 compliant, 3 concerns resolved)"
  - "Business PO (C — Demo 8 Act 1 acceptance criteria, north star test)"
  - "Engineering Lead (A — accepted ✓ 2026-07-02)"
---

# ADR-021: Mode 3 Constraint-Floor Search — Interaction Model, Backend Algorithm, and Result Display Contract

## Tier Classification

**Tier:** 1

**Justification:**
This ADR introduces a new primary interaction model for Mode 3 — the constraint-floor search.
The search result renders in the Zone 1 control plane column (`ControlPlaneColumn.tsx`,
`gridColumn: 3` of `InstrumentCluster`), which is a primary Zone 1 surface visible at all
supported viewports without scroll. The capability changes what the Mode 3 primary cognitive
task ("real-time steering within human cost constraints") means in practice: the instrument
now *finds* the safe operating boundary rather than requiring the user to sweep it manually.
This is a structural change to the interaction model, not a content-only change within
existing ADR-019 contracts.

**Sections required by tier:** All Tier 1 sections required: Persona Trace (7-element),
UX Implication Statement (7-element) + independent UX Designer sign-off, Silent Failure Mode,
Asymmetry Assessment, North Star Test, Mission Impact Statement.

---

## Status

`Accepted` — 2026-07-02. UX Designer sign-off filed (separate EL-triggered session, NM-042
compliant, 3 concerns resolved and tracked — Concern 3 closed in governing documents;
Concerns 1 and 2 tracked as #1564 and #1563 respectively; both are pre-ship conditions
for G1). EL acceptance vote: @PublicEnemage, 2026-07-02. ADR-019 remains the governing
authority for column layout, mode transition, and blue/orange visual system; this ADR
governs the search interaction model and result display contract only.

---

## Validity Context

**Standards Version:** 2026-07-02 (CLAUDE.md, M19 entry)
**Valid Until:** When constraint-floor search expands beyond `fiscal_multiplier` to multi-parameter joint constraint (M20+); when the backend binary search is replaced by async streaming (SSE); when `monitored_focal_cohorts` source changes from `ScenarioConfigSchema` to a separate endpoint.
**License Status:** `PROPOSED → ACCEPTED` on 2026-07-02

**Panel:**
- Architect Agent (R — author, ADR determination and algorithm contract)
- Frontend Architect Agent (C — Form 3 layout, ControlPlaneColumn rendering, result display)
- Computation Engine Agent (C — binary search algorithm, endpoint design, convergence contract)
- Chief Methodologist (C — uncertainty display for boundary results, floor value defensibility)
- UX Designer Agent (independent sign-off ✓ 2026-07-02, separate EL-triggered session, NM-042 compliant)
- Business PO (C — Demo 8 Act 1 acceptance criteria, north star test)
- Engineering Lead (A — accepted ✓ 2026-07-02)

**Renewal Triggers:**
1. Constraint search parameter scope expands beyond `fiscal_multiplier` — algorithmic and UX contracts must be extended
2. Backend timeout > 30s at free-tier CI runner — async/SSE redesign required
3. `monitored_focal_cohorts` source changes — floor value provenance in D-5 must be updated
4. Multi-cohort joint constraint added (M20+) — new ADR required (not an amendment here)
**Valid Until:** M20 entry — review if constraint-floor search is extended beyond
`fiscal_multiplier` to other policy parameters (LegitimacyConstraint, shock types), or if
a multi-parameter search mode is introduced.

**Panel:**
- Architect Agent (R — lead author, owns this document)
- Frontend Architect Agent (C — Form 3 layout and result display contract)
- Computation Engine Agent (C — binary search algorithm, convergence contract, endpoint)
- Chief Methodologist (C — uncertainty display for boundary results; floor value defensibility)
- UX Designer Agent (independent sign-off — separate EL-triggered session, NM-042)
- Business PO (C — Demo 8 Act 1 acceptance criteria)
- Engineering Lead (A — accountable on all ADR decisions)

**Renewal Triggers:**
- Constraint-floor search extended to parameters beyond `fiscal_multiplier`
- Multi-parameter search (joint boundary over two or more parameters) introduced
- Floor constraint source changed from `monitored_focal_cohorts` to a new configuration mechanism
- Binary search algorithm replaced with a different optimization method
- CI band integration changes the boundary uncertainty display contract

---

## Date

2026-07-02

---

## Context

### Background

ADR-019 (Control Plane Column, M18) specified `ControlPlaneColumn.tsx` with two forms:
Form 1 (Policy Instruments, blue) and Form 2 (Scenario Shocks, orange). Both forms are
one-at-a-time manual inputs: the user specifies a parameter value, applies it, and observes
the trajectory response. This is a point-search interaction model — one configuration at a
time, evaluated sequentially.

At M18 Demo 7, Aicha Mbaye (IMF Executive Board observer) can see that the Zambia scenario
produces a CRITICAL poverty headcount breach with `fiscal_multiplier=0.95`. The demo
demonstrates that a higher multiplier (1.2) avoids the breach. But the demo requires two
manual branch operations to establish the upper bound. The ministry analyst watching cannot
determine the *minimum* safe multiplier from these two data points alone — she would need
additional manual sweeps to narrow the boundary. This sweep cost is the analytical asymmetry
being addressed.

The constraint-floor search capability (#1540) allows the user to specify a floor constraint
(e.g., "poverty headcount must stay above 0.40") and ask the instrument: "What is the minimum
fiscal multiplier that keeps the trajectory above this floor?" The instrument finds the
boundary rather than requiring the user to sweep it.

ADR-019 Valid Until clause states: "M19 entry — review if Mode 3 active control scope
expands beyond the seven shock types and two policy instrument types specified in this ADR."
The constraint-floor search expands the interaction model beyond one-at-a-time inputs; this
ADR is the required review.

### Problem Framing

In Journey A Step 6 (Preparatory state, Eleni Papadimitriou, ≤ 20-minute preparation
window), after building the counter-proposal evidence, Eleni needs to establish a specific,
defensible boundary value to present at the negotiating table: "The proposed fiscal multiplier
of 0.95 falls below the safe boundary. Our analysis shows the minimum safe value is X."

Without constraint-floor search, establishing X requires manual parameter sweeping: apply
fiscal_multiplier=1.0, observe trajectory; apply 1.1, observe; apply 1.2, observe — each
operation is a backend branch call with ~2–5 second round trip. Narrowing the boundary to
two decimal places requires approximately 7–10 operations (binary search by hand), consuming
20–35 seconds of wall-clock time and significant cognitive load. An analyst under preparation
time pressure will either accept imprecision ("somewhere around 1.1–1.2") or spend time that
should go to argument construction.

The IMF negotiating team's internal models can compute safe operating ranges directly. The
ministry analyst currently cannot replicate this capability with WorldSim. This is the
asymmetry that constraint-floor search closes.

---

## Decision

### D-1: Constraint Search as Form 3 in ControlPlaneColumn (SEARCH FLOOR)

A third form section is added to `ControlPlaneColumn.tsx` below Form 2 (Scenario Shocks):

**Form 3 — Constraint Search (teal `#0d9488`):**
```
CONSTRAINT SEARCH                                    [teal header, #0d9488]
─────────────────────────────────────────────────
Floor constraint: [indicator label from focal cohort config]
Floor value:      0.400 (from scenario config)
Search over:      Fiscal multiplier [0.1, 3.0]
                  ┌──────────────────────────────┐
                  │ [Find safe boundary]          │ ← teal button, #0d9488
                  └──────────────────────────────┘

RESULT AREA — see D-4 for display contract
```

**Color:** Teal `#0d9488` — distinct from blue (policy inputs) and orange (shocks), consistent
with the two-color cross-layer system in ADR-019 §D-3. Teal is reserved for constraint
search; no other element in the control plane uses this color.

**`data-testid` assignments:**
- `data-testid="constraint-search-section"` — the Form 3 container
- `data-testid="constraint-floor-label"` — the indicator label display
- `data-testid="constraint-floor-value"` — the floor value display (e.g., "0.400")
- `data-testid="constraint-search-btn"` — the "Find safe boundary" button
- `data-testid="constraint-search-result"` — the result area (present whether pending, found, not-found, or error)

Form 3 is visible only when `monitoredFocalCohorts` has at least one entry with a valid
`floor_value`. When the array is empty or absent, Form 3 renders with a
`data-testid="constraint-search-unavailable"` message: "Configure a focal cohort floor in
scenario settings to enable constraint search." This prevents the form from appearing for
scenarios that predate `monitored_focal_cohorts` support.

---

### D-2: Backend Binary Search Endpoint

New endpoint: `POST /scenarios/{scenario_id}/constraint-floor-search`

The backend performs a binary search over `fiscal_multiplier ∈ [0.1, 3.0]` to find the
minimum value that keeps the focal cohort indicator at or above `floor_value` across all
`n_steps`.

**Why backend (not frontend sweep):**
- Frontend sweep requires O(n) branch calls per parameter granularity — narrowing to 2
  decimal places over [0.1, 3.0] at step 0.01 requires 290 sequential API calls
- Backend binary search requires O(log₂(n)) calls to the simulation engine internally:
  log₂(290) ≈ 8–9 evaluations to converge, all within a single HTTP round trip
- Frontend only observes one progress event (SEARCHING → RESULT); no polling loop required
- Timeout: 30-second server-side timeout; frontend shows "Search timed out" if exceeded

**Algorithm (backend):**
```
function binary_search_floor(scenario, focal_cohort, lo=0.1, hi=3.0, tol=0.01):
    if crosses_floor(scenario, hi, focal_cohort):
        return NOT_FOUND  # even max multiplier crosses the floor
    if not crosses_floor(scenario, lo, focal_cohort):
        return RESULT(boundary=lo)  # even min multiplier is safe
    while hi - lo > tol:
        mid = (lo + hi) / 2
        if crosses_floor(scenario, mid, focal_cohort):
            lo = mid  # mid is unsafe; search right half
        else:
            hi = mid  # mid is safe; search left half
    return RESULT(boundary=hi, uncertainty_interval=(lo, hi))
```

`crosses_floor(scenario, fiscal_multiplier, focal_cohort)` runs the full simulation with
`fiscal_multiplier` overriding the scenario config value and returns `True` if the focal
cohort indicator falls below `floor_value` at any step.

**Scope (M19):** Search is over `fiscal_multiplier` only. Other parameters (LegitimacyConstraint,
shock types) are deferred to M20. If `monitored_focal_cohorts` has multiple entries, the search
uses `monitored_focal_cohorts[0]` — the primary focal cohort — for the floor constraint.

---

### D-3: Request and Response Schema

**Request** (`ConstraintFloorSearchRequest`):
```python
class ConstraintFloorSearchRequest(BaseModel):
    focal_cohort_index: int = Field(default=0, ge=0)
    lo: float = Field(default=0.1, ge=0.1, le=3.0)
    hi: float = Field(default=3.0, ge=0.1, le=3.0)
    tolerance: float = Field(default=0.01, ge=0.001, le=0.1)
```

`focal_cohort_index` selects which `monitored_focal_cohorts` entry to use as the constraint.
Default 0 (primary focal cohort). Frontend always sends the default for M19.

**Response** (`ConstraintFloorSearchResponse`):
```python
class ConstraintFloorSearchStatus(str, Enum):
    FOUND = "FOUND"
    NOT_FOUND = "NOT_FOUND"
    ERROR = "ERROR"

class ConstraintFloorSearchResponse(BaseModel):
    status: ConstraintFloorSearchStatus
    boundary: float | None           # minimum safe multiplier; null if NOT_FOUND or ERROR
    uncertainty_lo: float | None     # binary search convergence interval lower bound
    uncertainty_hi: float | None     # binary search convergence interval upper bound
    evaluations: int                 # number of simulation runs performed
    search_lo: float                 # parameter range searched (echoed from request)
    search_hi: float
    floor_value: float               # floor constraint used (echoed for display)
    indicator_key: str               # focal cohort indicator (echoed for display)
    error_message: str | None        # non-null if status == ERROR
```

`uncertainty_lo` / `uncertainty_hi` represent the binary search convergence interval: the
true boundary is known to lie within [uncertainty_lo, uncertainty_hi]. At default tolerance
0.01, this interval is ≤ 0.01 multiplier units wide. The frontend displays this as the
search precision, not as a CI band — CI band integration is G3 scope (ADR-007 Bayesian
posterior layer).

---

### D-4: Result Display Contract

The `data-testid="constraint-search-result"` area renders one of four states:

**State 1 — PENDING (search in progress):**
```
[teal spinner] Searching... (N evaluations)
```
The backend streams progress events via SSE or returns immediately; for M19 the endpoint
returns synchronously (no streaming). The frontend shows a loading indicator from button
click until response arrives.
`data-testid="constraint-search-pending"`

**State 2 — FOUND:**
```
Safe boundary found:

fiscal multiplier ≥ 1.18
  (search precision: ±0.01)

N evaluations  ·  [0.1, 3.0] searched
```
`data-testid="constraint-search-found"` on the result container.
`data-testid="constraint-boundary-value"` on the "1.18" value.

The result renders in teal `#0d9488`. The boundary value is displayed to 2 decimal places.
The search precision interval ("±0.01") is displayed as a precision disclosure, not a CI
band — it is the binary search convergence width, not a statistical confidence interval.
A CM-endorsed note: "This is the binary search precision, not a statistical confidence
interval. Empirical CI bounds will be available in G3 after backtesting calibration."

**State 3 — NOT_FOUND:**
```
No safe configuration found.

Poverty headcount falls below floor 0.400
at all tested multiplier values in [0.1, 3.0].

The proposed scenario path does not have a safe
operating point for this parameter within the
searched range.
```
`data-testid="constraint-search-not-found"`. This state must be honest — it tells
the analyst that the floor cannot be met with fiscal multiplier alone within the
parameter range. It must not suggest that the result is a model failure.

**State 4 — ERROR (timeout or internal failure):**
```
Search failed.
[error_message from response]
Try again or reduce search range.
```
`data-testid="constraint-search-error"`.

---

### D-5: Floor Constraint Source

The floor constraint displayed in Form 3 is read from
`activeScenarioDetail.configuration.monitored_focal_cohorts[0]`:
- `floor_value` → displayed as "Floor value: 0.400"
- `indicator_key` → displayed as the indicator label (via `getIndicatorDisplayNameAny()`)
- `floor_label` → displayed as the floor label if present

The constraint-floor search uses the same floor that drives the CLEAR badge in
`CohortImpactSection`. These two surfaces share a single source of truth: the
`FocalCohortConfig` Pydantic model introduced in #1538.

No separate configuration UI is introduced for the search floor in M19. The floor is
authored at scenario creation time (via `monitored_focal_cohorts` in `ScenarioConfigSchema`)
and is read-only within the Mode 3 session. This preserves the pre-authorship CM review
process for floor values (see #1538 issue §Process gate).

---

### D-6: ADR-019 Validity — What This ADR Does and Does Not Change

This ADR **does not change:**
- The column width (280px, set by `InstrumentCluster.tsx`)
- The two-component architecture (D-1 in ADR-019)
- Form 1 (Policy Instruments, blue) — content, layout, testids
- Form 2 (Scenario Shocks, orange) — content, layout, testids
- Mode transition behavior (`Mode2ColumnSurface` → `ControlPlaneColumn`)
- The blue/orange cross-layer visual system

This ADR **adds:**
- Form 3 (Constraint Search, teal) — new section in `ControlPlaneColumn.tsx`
- `POST /scenarios/{id}/constraint-floor-search` — new backend endpoint
- `ConstraintFloorSearchRequest` / `ConstraintFloorSearchResponse` — new schemas
- `ConstraintFloorSearchStatus` — new enum

ADR-019 renewal condition "Mode 3 active control scope expands beyond two policy instrument
types" is satisfied by this ADR. ADR-019 remains ACCEPTED and governing for everything
outside ADR-021's scope.

---

## Persona and UX Traceability

### [Tier 1] Persona Trace

**P-1 — Persona identification:**
Primary: Persona 2 — Finance Ministry Negotiator (Eleni Papadimitriou archetype, Deputy
Director of Debt Management). Secondary: Persona 5 — IMF Executive Board Observer (Aicha
Mbaye archetype, observing the capability at Demo 8 Act 1).

**P-2 — Entry state:**
Primary: Preparatory entry state (20–40 minute desk preparation window, Journey A Step 6).
Secondary: Reactive entry state (Eleni in the negotiation room, 90-second ceiling, Journey
B Step 5 stretch use case — Mode 3 active control in the room).

The search is most naturally used in the Preparatory state (evening before), where Eleni
constructs the counter-proposal and needs the specific boundary value to anchor her argument.
The Reactive state use case (finding the boundary in the room during a session) requires the
search to complete in under 10 seconds — the 30-second backend timeout must be monitored
against this real-world ceiling.

**P-3 — Journey reference:**
Closes Journey A Step 6 [Near-Term-Gap] — boundary sweep currently requires 7–10 manual
branch operations. With ADR-021, boundary establishment is one Form 3 action.

Extends Journey C Step 2 — the active control input (manual) and the constraint search
(automated boundary-finding) are complementary: the analyst may apply a manual control
input first to observe the trajectory response, then run the constraint search to find
the minimum safe value.

**P-4 — Time or interaction ceiling:**
Preparatory state (Journey A): no strict ceiling for the search itself, but the total
preparation window is 20–40 minutes. A single "Find safe boundary" click that completes
in under 15 seconds preserves the preparation flow without disrupting it.

Reactive state (Journey B Step 5): 90-second total ceiling for the entire Mode 3 branch
in the room. Mode switch costs ~3 seconds. Control input costs ~10 seconds. That leaves
~77 seconds — the constraint search must complete in under 30 seconds in this state.
The 30-second backend timeout is therefore the binding reactive-state constraint.

**P-5 — Income cohort served:**
Bottom income quintile — the `monitored_focal_cohorts[0]` floor constraint in M19 is
anchored to `bottom_quintile_informal_workers_poverty_headcount` (per Demo 7 configuration,
CM-reviewed, `floor_value=0.40`). The constraint search establishes the safe boundary for
the cohort most exposed to fiscal consolidation. Per-cohort disaggregation beyond the primary
focal cohort is deferred: M19 searches one cohort; multi-cohort joint constraint is M20+.

**P-6 — Negotiating leverage statement (Persona 2):**
After the constraint search, Eleni can make the following specific argument:
"Our analysis finds that the minimum fiscal multiplier that keeps poverty headcount above the
recovery floor of 0.40 is 1.18. The proposed programme multiplier is 0.95. This is 0.23
multiplier points below the safe boundary. To protect the bottom income quintile, the
programme multiplier must be at or above 1.18, or the conditionality structure must be
redesigned to compensate."

This is a citable, specific argument with an indicator, a step-range result, a floor value,
and a named gap. It was previously unavailable without manual sweeping.

**P-7 — North star test answer:**
A Zambian Ministry of Finance analyst is preparing for an IMF restructuring session. She
has run the Zambia scenario in Mode 2 and established that `fiscal_multiplier=0.95` (the
proposed programme value) produces a CRITICAL poverty headcount breach at step 3. She
needs to tell the IMF: "Our counter-proposal requires a minimum multiplier of X to keep
the bottom quintile above the poverty recovery floor." Before ADR-021, she would manually
test 1.0, then 1.1, then 1.15, then 1.18 — four branch operations consuming 20–35 seconds.
With ADR-021, she clicks "Find safe boundary" in Form 3. In under 15 seconds, the result
reads "fiscal multiplier ≥ 1.18 (search precision: ±0.01)." She enters the restructuring
session with a specific, defensible floor: "Your proposed 0.95 is 0.23 below the safe
boundary. We require at minimum 1.18." The IMF team, who computed their own safe range
internally, now face a ministry counterpart who has matched their analytical capability at
the number level — not just the directional level. This closes the asymmetry described in
the founding document.

---

### [Tier 1] UX Implication Statement

**UX-1 — Zone assignment and hierarchy certification:**
This ADR places Form 3 (Constraint Search) in the Zone 1 control plane column — `gridColumn: 3`
of `InstrumentCluster`, `data-testid="zone-control-plane"`. This is the same zone as ADR-019
Forms 1 and 2 — no zone reassignment. The assignment is consistent with
`information-hierarchy.md §UX Architectural Commitments` Premise 5 (control plane zone
reserved for Mode 3 input surfaces) and `information-hierarchy.md §Control Plane Reserved Zone`
(interactive control inputs belong in column 3, not in Zones 1A or 1B).

**UX-2 — Primary cognitive task alignment:**
This capability primarily serves Mode 3's primary cognitive task (real-time steering within
human cost constraints). The constraint-floor search is the first instrument capability that
inverts the steering question: instead of "is this configuration safe?" it answers "what is
the minimum configuration that is safe?" In Mode 2 (threshold-safe path construction), the
capability is not directly accessible — it requires Mode 3 activation. In Mode 1 (trajectory
reconstruction), the control plane column is not rendered; this capability is absent in Mode 1.

**UX-3 — Entry state coverage (falsifiable acceptance criteria):**
*Preparatory entry state (Journey A Step 6, Persona 2):*
Acceptance criterion: In a scenario with `monitored_focal_cohorts` configured, the analyst
clicks "Find safe boundary" from Mode 3 Form 3. Within 15 seconds, `data-testid="constraint-search-found"` is visible and `data-testid="constraint-boundary-value"` displays a value
in the format "1.18" (two decimal places). Observable in the live application: no navigation
required; the result appears in the column alongside the trajectory view.

*Reactive entry state (Journey B Step 5, Persona 2):*
Acceptance criterion: The search completes and result is visible within 30 seconds of button
click at tablet viewport (1024×768). The trajectory view must remain visible alongside Form 3
during the search — no navigation required.

*CLEAR badge consistency:*
Acceptance criterion: The `floor_value` displayed in `data-testid="constraint-floor-value"`
must match the `floor_value` displayed in `data-testid="focal-cohort-floor"` in
`CohortImpactSection`. They derive from the same `monitored_focal_cohorts[0]` source.

**UX-4 — HCL parity certification:**
This ADR does not affect HCL visual weight relative to financial indicators. The constraint
search surface operates on focal cohort data (human development indicators), not financial
composite scores. The Form 3 result ("fiscal multiplier ≥ 1.18") is a human cost threshold
determination — the CLEAR badge equivalent expressed as a policy parameter boundary. HCL
parity is maintained: the constraint search result is as prominently positioned as the
boundary value it represents.

**UX-5 — Uncertainty display specification:**
(a) Confidence tier information displayed: the search precision interval (convergence width,
default ±0.01) is displayed as a precision disclosure in State 2 (FOUND). No confidence tier
number is displayed on the boundary value itself in M19 — the tier of the boundary result
is determined by the underlying focal cohort indicator tier, which is visible in Zone 1B.
(b) Location: below the boundary value in `data-testid="constraint-search-found"`.
(c) Tier 3 SYNTHETIC_COMPARABLE: If the focal cohort indicator is synthetic (Tier 3),
the result area includes the word "synthetic" in the source disclosure: "Floor constraint
derived from a synthetic indicator (Tier 3). Result is directional." This disclosure is
required by DATA_STANDARDS.md §Confidence Tier System for synthetic inputs.
(d) Tier 4: "Floor constraint derived from a model estimate (Tier 4). Treat boundary
as an order-of-magnitude estimate; do not cite without verification."
(e) Structural Absence Declaration: if `indicator_key` resolves to a Structural Absence
Declaration, Form 3 renders "Constraint search unavailable: focal cohort indicator is a
structural absence." The search does not run. `data-testid="constraint-search-structural-absence"`.

**UX-6 — Irreversibility signal integrity certification:**
This ADR does not modify the MDA alert panel (Zone 1B) or severity display. TERMINAL alerts
remain visually distinct from CRITICAL. The constraint search result does not introduce new
severity labels. The boundary value ("fiscal multiplier ≥ 1.18") is not severity-coded —
it is a threshold boundary, not an alert. No change to irreversibility signal integrity.
CI-testable: existing AC-008 (TERMINAL/CRITICAL visual distinction) is unchanged by this ADR.

**UX-7 — User journey coverage:**
Journey A Step 6 (Preparatory — counter-proposal construction): the constraint search closes
the boundary-sweep gap. Previously, Eleni needed 7–10 manual branch operations to establish
a defensible boundary. Form 3 delivers this in one operation.

Journey C Step 2 (Active Control — apply modification): Form 3 complements Form 1 without
replacing it. The analyst may apply a manual multiplier first (Form 1) to observe the live
trajectory divergence, then run the constraint search (Form 3) to establish the formal
boundary. These are independent operations on independent forms.

Journey B Step 5 (Reactive stretch use case): the constraint search is accessible in the
Reactive state during the 90-second ceiling, provided the Mode 3 transition has been
completed (~3 seconds).

**UX Designer sign-off:**
This sign-off is a precondition for the acceptance vote. An ADR with an incomplete sign-off
block cannot proceed to acceptance vote and cannot be given `Accepted` status. All four
fields below are required — a checkbox without the structured attestation is non-compliant.

**Reviewing agent:** UX Designer Agent
**Session context:** Separate session, EL-triggered 2026-07-02
**Governing documents reviewed:**
- `docs/ux/north-star.md §Primary Cognitive Tasks by Mode` — confirmed Mode 3 task
  definition ("real-time steering within human cost constraints") and Mode 1 absence
  claim for Form 3; confirmed Mode 2 task definition for UX-2 assessment
- `docs/ux/north-star.md §Canonical User` — confirmed Preparatory and Reactive entry
  state characterizations against the canonical user description
- `docs/ux/information-hierarchy.md §Control Plane Reserved Zone` — confirmed Mode 1
  empty-column specification, Mode 2 two-component architecture, Mode 3 two-form layout
  and simultaneous visibility requirement; verified ADR-021 does not displace Forms 1/2
  headers
- `docs/ux/information-hierarchy.md §CVD Color Specification` — identified Concern 1
  (MV-001 three-way CVD gate not extended to teal)
- `docs/ux/information-hierarchy.md §Simultaneous Visibility Requirement` — performed
  three-form height accounting; identified Concern 2 (tablet viewport column overflow)
- `docs/ux/information-hierarchy.md §The Three Disclosure Zones` — confirmed Zone 1/2/3
  criteria and scroll definitions; confirmed column-internal scroll precedent from
  history list specification
- `docs/ux/information-hierarchy.md §Zone 1A — Confidence Display` — confirmed Tier 3
  display treatment consistent with UX-5 "synthetic" word requirement
- `docs/ux/user-journeys.md §Journey A Step 6` — identified Concern 3 (Step 6 not
  documented as constraint-search workflow; Near-Term-Gap annotation absent)
- `docs/ux/user-journeys.md §Journey C Steps 1–4` — confirmed Mode 3 entry sequence
  and ADR-019 acceptance criteria context for Form 3 complement claim in UX-7
- `docs/ux/user-journeys.md §Journey B Step 5` — confirmed Reactive stretch use case
  characterization and 90-second ceiling for UX-3
- `docs/ux/user-journeys.md §Journey Dependency Map` — confirmed Step 6 governing
  dependency is EL Decision 3 (COMPARE_VIEW), not constraint search
- `docs/adr/ADR-019-control-plane-column.md §D-3` — confirmed simultaneous visibility
  requirement for Forms 1 and 2 and verified Form 3 does not displace these headers
- `docs/adr/ADR-019-control-plane-column.md §UX Implication Statement UX-1` — confirmed
  zone assignment consistency; no conflict with ADR-021 placement in gridColumn: 3
**Concerns found:** 3 — see Pre-Implementation and Pre-Ship conditions below

`[x]` UX Designer sign-off. 2026-07-02

**Pre-Implementation conditions (before any G1 implementation PR is opened):**

- **[Concern 3 — UX-7]** `user-journeys.md §Journey A Step 6` must be updated to
  document the Mode 2 → Mode 3 → Form 3 → Mode 2 boundary-establishment sub-workflow,
  with the clarification that the "reset active branch" caution does not apply when no
  Form 1 or Form 2 inputs have been applied in the Mode 3 session. The Journey
  Dependency Map must be updated to add the ADR-021 dependency for Step 6
  boundary-establishment. This grounds the UX-7 "closes Journey A Step 6" claim in
  the governing document and must be committed before the G1 feature branch opens.

**Pre-Ship conditions (before any G1 PR merges to the sprint branch):**

- **[Concern 1 — UX-1]** MV-001 CVD validation must be extended to validate all three
  control plane colors — blue `#0284c7`, orange `#ea580c`, and teal `#0d9488` — under
  deuteranopia and protanopia simulation. Blue-vs-teal distinguishability under
  deuteranopia must be confirmed with a simulation tool (Sim Daltonism, Coblis, or
  equivalent). Blue/teal luminance contrast ratio is ~1.14:1, insufficient for luminance-
  only discrimination; empirical hue simulation is required. If not empirically
  distinguishable, a teal replacement is documented with candidates in
  `information-hierarchy.md §CVD Color Specification` — update this ADR §D-1 with the
  replacement hex value. Tracked: #1564.

- **[Concern 2 — UX-1]** A new CI assertion (`AC-016`) must be added confirming that
  the Form 3 section header (`data-testid="constraint-search-section"`) is visible
  within the 280px column at 1280×800 with Forms 1 and 2 in minimum state (no history
  entries). At 1024×768, the assertion must verify Form 3 is reachable within one
  column-internal scroll from column top. This assertion must be in the same PR as the
  Form 3 implementation — not filed as a follow-up. Tracked: #1563.

---

## Silent Failure Mode

**Primary failure mode:** The `POST /scenarios/{id}/constraint-floor-search` endpoint returns
a 200 with `status: "ERROR"` but the frontend does not render `data-testid="constraint-search-error"` — the result area remains blank. This produces a state where the user clicked
"Find safe boundary," the button is no longer spinning, and nothing is shown. The analyst
does not know the search failed; she may interpret the blank as "no result found" rather than
"search errored."

**Detection mechanism:** `data-testid="constraint-search-result"` must always render one of
four states (PENDING, FOUND, NOT_FOUND, ERROR) after the search button is clicked. A QA
reviewer can verify by: (1) clicking "Find safe boundary" in a scenario without `monitored_focal_cohorts` configured (should show NOT_FOUND or `constraint-search-unavailable`);
(2) simulating a backend timeout (should show ERROR with message).

**Backend silent failure:** The binary search runs 8–9 engine evaluations internally. If
one internal evaluation fails silently (exception swallowed), the search may converge to an
incorrect boundary. Mitigation: each internal engine evaluation must raise on error rather
than returning a default value; the endpoint must propagate the error to the response rather
than returning a boundary derived from partial results.

---

## Asymmetry Assessment

Well-resourced sovereign creditor teams (IMF internal models, BlackRock sovereign analytics,
Citi sovereign desk) can currently compute safe operating parameter ranges for fiscal
multiplier sensitivity in minutes — this is a core capability of proprietary sovereign risk
models. WorldSim's proposed ADR-021 closes this gap by enabling a ministry analyst to
establish the same boundary in a single Form 3 interaction (~10–15 seconds). The remaining
gap after this ADR: the boundary uncertainty in M19 is expressed as binary search precision
(±0.01 convergence interval), not as a statistically calibrated confidence interval. G3
(Bayesian posterior layer, #1543) will close this remaining uncertainty gap by grounding the
CI bands in empirical backtesting. After G3, the boundary result will carry empirically
grounded uncertainty that matches the uncertainty quantification available to sophisticated
creditor teams.

---

## North Star Test

The Zambian Ministry of Finance analyst at Demo 8 (Persona 5 — Aicha observing) can see that
the ministry's specialist enters one number into Form 3 ("Find safe boundary") and within 15
seconds receives "fiscal multiplier ≥ 1.18 (±0.01)." The IMF representative across the table
knows from internal models that the safe boundary is approximately 1.15–1.20. The two parties
are now working from the same number, derived by the same method, visible to both. The
ministry did not need a $50,000 Bloomberg terminal or a proprietary DSGE model to establish
this boundary. They ran WorldSim. This is the founding document's asymmetry claim made
concrete: the tool gives the finance minister the same analytical standing as the institution
sitting across the table. Yes — this decision makes the tool more useful to a finance minister
in that moment.

---

## Mission Impact Statement

This ADR closes the "boundary sweep" capability gap — the last step in the Mode 3 Active
Control experience that required manual iteration rather than instrument-assisted search. The
constraint-floor search is the first WorldSim capability that operates on the IMF's core
question in reverse: not "will this programme configuration cross human cost thresholds?" but
"what is the minimum programme parameter that avoids them?" This is the mode of inquiry that
sophisticated creditor analytics have always supported — the ministry side of the table is
now able to meet it with an equally specific answer. The direct impact: a Zambian Ministry of
Finance analyst can enter a boundary number into the IMF restructuring session derived from
the same simulation engine, the same historical calibration data, and the same uncertainty
quantification framework — not from assertion or experience, but from computation. This
closes the single most significant analytical asymmetry in the sovereign debt negotiation use
case.

---

## Minimum Data Tier

Minimum data tier: Tier 2. The constraint search runs the focal cohort indicator through the
simulation engine; the floor comparison requires at minimum an estimated-comparable indicator
(Tier 2) to produce a directional result. At Tier 3 (synthetic), the boundary result is
produced but must be disclosed as derived from a synthetic indicator. At Tier 4 (model
estimate), the boundary is an order-of-magnitude estimate only. At Tier 5 or Structural
Absence, the search does not run.

For the primary M19 use case (ZMB poverty headcount, bottom quintile), the indicator is
Tier 2 (estimated comparable from World Bank and UNDP sources). The search produces a
defensible result at Tier 2 fidelity — citable with confidence tier caveat.

---

## Alternatives Considered

### Alternative 1: ADR-019 Amendment

Add Form 3 as a Decision amendment to ADR-019 without a new ADR. Rejected because:
- ADR-019 governs the *layout and visual contract* of the control plane column; the
  constraint-floor search changes the *interaction model* (the instrument now finds the
  boundary rather than applying a specified value) — a structurally different question
- ADR-019's Valid Until clause explicitly anticipated this review: "M19 entry — review if
  Mode 3 active control scope expands"
- An amendment to an Accepted ADR changes its validity context; if the amendment is
  substantial enough to require independent UX Designer sign-off, it should be a new ADR
- The backend algorithm (binary search endpoint) is a new architectural decision that has
  no home in ADR-019's scope

### Alternative 2: Frontend Parameter Sweep

The frontend iterates through `fiscal_multiplier` values (0.1, 0.11, …, 3.0) using
sequential `POST /branch` calls until it finds the boundary. Rejected because:
- O(n) API calls: 290 sequential calls to narrow to 0.01 precision over [0.1, 3.0]
- Wall-clock cost: 290 × 2–5 seconds per call = 10–24 minutes of sequential API calls
  (the equivalent of the human manual sweep, just automated)
- Network overhead: 290 API calls vs. 1 API call
- No improvement over manual parameter sweeping from the user's perspective

### Alternative 3: Grid Search with Cached Results

Pre-compute the trajectory at a grid of `fiscal_multiplier` values (every 0.1) and cache
the results; the constraint search interpolates from the cache. Rejected because:
- Pre-computation cost: 29 trajectories × n_steps per scenario at scenario creation time;
  too expensive as a default behavior
- Cache invalidation: any change to the scenario configuration (shock injection, new policy
  input) invalidates the cache entirely
- Interpolation error is bounded only if the function is monotone in the parameter — the
  simulation is not guaranteed monotone (non-linear propagation via ADR-011)

---

## Consequences

### Positive

- Closes the boundary-sweep capability gap in Journey A Step 6 (Preparatory state)
- Provides a citable, specific boundary value ("fiscal multiplier ≥ 1.18") that can be
  cited at the negotiating table with the same specificity as a threshold crossing alert
- Single HTTP round trip (O(log n) engine evaluations) vs. O(n) manual sweeps
- Floor constraint source (`monitored_focal_cohorts`) shared with the CLEAR badge — one
  source of truth for the focal cohort floor value
- Form 3 is visible only when the floor constraint is configured — no UI noise for
  scenarios that do not use the focal cohort floor

### Negative

- The binary search precision (±0.01) is not a statistical CI — analysts must be informed
  it is search precision, not uncertainty quantification (G3 will add empirical CI)
- 30-second backend timeout may be insufficient for long scenarios or slow compute
  environments; resource-constrained contributors may experience timeouts
- M19 searches `fiscal_multiplier` only; analysts who want to constrain other parameters
  (LegitimacyConstraint, shock magnitude) cannot use Form 3 in M19
- Form 3 is only available in Mode 3; analysts who prefer Mode 2 workflow cannot access
  the constraint search without first transitioning to Mode 3

### Known Limitations

- **Single-parameter search only (M19):** The constraint-floor search finds the boundary
  for `fiscal_multiplier` only. Joint constraint search over two or more parameters (e.g.,
  "what (fiscal_multiplier, legitimacy_index) pairs are safe?") requires an optimization
  surface computation that is out of scope for M19. Affects Persona 2 in the case where
  the programme design involves multiple interacting terms.
- **Single focal cohort only (M19):** The search uses `monitored_focal_cohorts[0]`. If
  multiple cohorts have conflicting safe boundaries, the analyst must run the search once
  per cohort manually in M19. Multi-cohort joint constraint is M20+.
- **No streaming progress:** The backend returns synchronously after the search completes.
  For long searches (scenarios with many steps), the frontend shows a spinner with no
  intermediate progress. Streaming (via SSE or chunked response) is deferred.
- **Equitable Build Process:** The binary search runs the full simulation 8–9 times per
  search. On a 4-core machine with a 20-step scenario, a single search takes ~5–10 seconds.
  On the GitHub Actions free-tier runner (2-core), the same search should complete within
  the 30-second timeout, but must be profiled during G1 development. If the backend binary
  search exceeds 30 seconds on the free-tier runner, a lighter tolerance (0.05 instead of
  0.01) may be required for M19 with a note for the user.

---

## Diagram

`docs/architecture/ADR-021-constraint-floor-search.mmd` — authored at ADR acceptance
(2026-07-02). Shows the single HTTP round trip: Form 3 → `POST /constraint-floor-search`
→ backend binary search loop (O(log n) ≈ 8–9 evaluations) → `ConstraintFloorSearchResponse`
→ Form 3 result display.

---

## Backtesting Validation Anchor

The binary search uses the same simulation engine paths as `POST /branch`. No new
measurement methodology is introduced — the constraint search finds a parameter boundary
using existing trajectory computation. No independent backtesting validation anchor is
required for the search algorithm itself.

The *floor value* used as the search constraint (`monitored_focal_cohorts[0].floor_value`)
is a CM-reviewed constant (Demo 7: 0.40 for `bottom_quintile_informal_workers_poverty_headcount`, per CM review recorded in `HumanCapitalTrajectoryPanel.tsx:23`). The constraint
search inherits the CM endorsement of the floor value. No additional backtesting is required
for ADR-021. G3 (Bayesian posterior layer, #1543) adds empirical calibration to the CI
bands used in conjunction with the boundary result; G3's validation anchors are specified
in the ADR-007 amendment.
