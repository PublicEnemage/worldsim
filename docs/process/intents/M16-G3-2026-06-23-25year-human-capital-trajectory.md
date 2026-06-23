---
name: M16-G3-25year-human-capital-trajectory
type: implementation-intent
issues: "#274"
status: >
  CM-confirmed 2026-06-23 — all ACs finalized; QA may now author tests for
  AC-CM-1/AC-CM-2/AC-CM-3. CM review comment: #274 (2026-06-23).
  Implementation PR may open once QA tests for all ACs are filed.
authored-by: Chief Engineer Agent
authored-date: 2026-06-23
implementing-agents:
  - "Chief Engineer Agent — backend: ScenarioConfigSchema extension, adaptive resolution override, trajectory endpoint"
  - "Frontend Architect Agent — frontend: projection panel Zone placement, Layer 3 milestone sentence, step axis"
sprint-entry: "docs/process/sprint-plans/m16-g3-sprint-entry.md — EL Approved 2026-06-23"
ce-assessment: "docs/process/sprint-plans/m16-g3-sprint-entry.md §2.5 — four binding decisions"
cm-review-gate: "SATISFIED 2026-06-23 — CM review comment at #274 (2026-06-23); AC-CM-1/AC-CM-2/AC-CM-3 confirmed"
adr-reference: "None — DemographicModule M4 extension within existing module boundary (Architect consultation, sprint plan §ADR Prerequisites)"
release-branch: release/m16
---

# Implementation Intent: M16-G3 — 25-Year Human Capital Depletion Trajectory

> **Two implementing agents, one document.** The backend (Chief Engineer Agent) and frontend
> (Frontend Architect Agent) deliverables are co-dependent: a backend that extends the
> trajectory endpoint to 100 steps without a frontend projection panel produces no observable
> Demo 6 capability; a frontend projection panel without the adaptive resolution override
> (CE Assessment Decision 1) silently produces degenerate output on crisis-period scenarios.
> Splitting into two intent documents would allow either to ship independently.
>
> **CM-PENDING ACs.** CE Assessment Decision 3 gates indicator-specific ACs (AC-CM-1 through
> AC-CM-3) on a Chief Methodologist review comment on #274. QA tests for AC-1 through AC-10
> and AC-F1 through AC-F8 may be authored from this document immediately. QA tests for the
> three CM-PENDING ACs must not be authored until the CM review is filed and the authoring
> agent updates those ACs in-place with the CM-confirmed values.

---

## 1. Source Authority

**ADR:** None — DemographicModule M4 extension within existing module boundary.
Architect consultation confirmed no new ADR required (sprint plan §ADR Prerequisites;
G3 sprint entry §2.2). The CE Assessment (`docs/process/sprint-plans/m16-g3-sprint-entry.md §2.5`)
is the G3-specific design authority and replaces the ADR gate for this sprint.

**CE Assessment binding decisions:**

| Decision | Requirement | AC enforcing |
|---|---|---|
| Decision 1 | `adaptive_resolution: false` when `projection_steps > 8`; no daily-resolution switching in 100-step mode; must be an explicit parameter, not a silent constant | AC-5 |
| Decision 2 | Extend existing `/simulate`-equivalent endpoint with optional `projection_steps` (integer, `1 ≤ projection_steps ≤ 100`); `api_contracts.yml` updated in same commit | AC-1, AC-2, AC-3, AC-8 |
| Decision 3 | CM review comment on #274 required before indicator-selection ACs finalize (see AC-CM-1 through AC-CM-3 below) | AC-CM-1, AC-CM-2, AC-CM-3 |
| Decision 4 | Implementing agent must dry-run SEN at `projection_steps=100` before PR ready; record wall time and per-indicator min/max; FAIL if any value outside [0.0, 1.0] or wall time > 60 s | AC-6, AC-F8, Step 4 Verify |

**Issue in scope:** #274 — feat(simulation): 25-year human capital depletion trajectory

**Authored by:** Chief Engineer Agent
**Date:** 2026-06-23
**Implementing agents:** Chief Engineer Agent (backend); Frontend Architect Agent (trajectory display)

---

## 2. Persona Trace Elements Targeted

*Derived from sprint plan §Demo 6 North Star and sprint entry §3.1 observable application state.
G3 has no parent ADR; persona trace is derived from the mission deliverable and Demo 6 context.*

**P-1 — Personas served:**
- **Persona 2 — Finance Ministry Negotiator** (Eleni Papadimitriou archetype,
  `docs/ux/personas.md §Persona 2`). Operational user. In the Demo 6 Preparatory context
  (Article IV consultation preparation), Persona 2 runs the SEN projection and extracts
  the "for this long" argument from the 25-year trajectory panel for the minister's briefing.
- **Persona 5 — Finance Minister** (Aicha Mbaye archetype, `docs/ux/personas.md §Persona 5`).
  Mission validation reference. Demo 6 is her scenario: the Senegalese Finance Minister's
  team must be able to name the generation-length human capital consequence of proposed IMF
  programme conditions, visible in the primary viewport without specialist translation.

**P-2 — Entry state:**
Preparatory (3-hour briefing preparation window; conditionality document has arrived;
Persona 2 is building the Demo 6 argument "this cohort, at this step, for this long").
The 25-year trajectory is a desk tool for analytical construction, not a Reactive-state
90-second retrieval. The Layer 3 milestone sentence is the element that bridges to Reactive
use: visible at L0 and citeable without cursor interaction.

**P-3 — Journey reference:**
Demo 6 context — Senegalese Finance Minister scenario, Article IV consultation.
Sprint plan north star: "the Senegalese Finance Minister's team walks into an Article IV
consultation with a screen showing bottom-quintile threshold crossings at step 2, a 25-year
human capital trajectory, and PSP trajectory — all visible in the primary viewport without
drawer navigation." G3 closes the third element: the 25-year human capital trajectory.
Without G3, Demo 6 can show "this cohort, at this step" but not "for this long."

**P-4 — Time and interaction ceiling:**
- Projection run time: ≤ 60 seconds from scenario load to panel render on 4-core hardware
  (CE Assessment Decision 4 — non-negotiable performance gate; AC-F8)
- Panel access: zero additional interaction — visible in primary viewport without drawer,
  tab, or navigation action (UX Architectural Commitment 2; AC-F1)
- Milestone sentence read: L0 — visible without hover or click (AC-F3)

**P-6 — Negotiating leverage delivered (Demo 6 / Persona 5 context):**
The Senegalese finance ministry analyst, with the SEN scenario loaded at `projection_steps=100`
in Mode 1, can state at the Article IV table: "Under the proposed programme terms,
[CM-confirmed indicator plain name] in the [CM-confirmed cohort plain name] crosses the
recovery floor by [year] — a generation-length consequence that persists beyond the programme
window." This argument was not available before G3: the simulation previously showed programme-
length consequences (8 steps ≈ 2 years); G3 extends visibility to 100 quarterly steps (25 years),
making the intergenerational consequence citeable rather than asserted.

**P-7 — North star capability delivered:**
The Senegalese finance ministry analyst, with the SEN scenario loaded in Mode 1 at
`projection_steps=100`, can read the 25-year human capital depletion trajectory in the
primary viewport and cite the Layer 3 milestone sentence — "by [year] [step N], [indicator]
in [cohort] falls below the recovery floor" — without drawer navigation, without specialist
mediation, and within the 60-second projection ceiling. The Demo 6 "for this long" argument
is completeable from the primary viewport alone.

---

## 3. Observable Application State

*All states verifiable by an external observer using only the running application.
No source code reading, no CI report reference, no implementation knowledge required.*

### 3.1 Primary observable state — Backend trajectory endpoint

At a scenario request with `projection_steps=100` and the SEN entity loaded:

1. The trajectory response contains **exactly 100 step objects**.
2. All 100 steps have `effective_from` dates spaced by exactly 3 months (quarterly resolution)
   — no sub-quarterly steps appear. CE Assessment Decision 1 (adaptive resolution override) is active.
3. All DemographicModule-derived Quantity values across all 100 steps are within [0.0, 1.0].
4. With `projection_steps` absent or ≤ programme length: ZMB ECF returns 8 steps —
   existing behaviour unchanged.
5. `projection_steps=0` or `projection_steps=101` → 422 validation error.

### 3.2 Primary observable state — Frontend projection panel

At **1280×800** with the SEN scenario loaded in **Mode 1** and `projection_steps=100`:

1. `data-testid="human-capital-trajectory-panel"` is **visible in the primary viewport**
   without opening a drawer, a tab, or navigating away from the instrument cluster
   (UX Architectural Commitment 2).
2. `data-testid="zone-1a-trajectory"`, `data-testid="zone-1c-pmm"`, and
   `data-testid="zone-1d-four-framework"` remain **visible within the 1280×800 viewport**
   — not displaced by the projection panel. Scroll or zoom within the projection panel
   is acceptable; displacement of Zone 1A/1C/1D is not.
3. `data-testid="projection-panel-header"` contains the **exact text**:
   `"25-year projection · quarterly resolution"` (middle dot ·, spaces on both sides).
4. The panel contains **≥3 SVG path elements** matching `data-testid="projection-curve-{indicatorKey}"`,
   displayed on `data-testid="projection-panel-step-axis"`.
5. At the first step where any indicator crosses its MDA floor,
   `data-testid="projection-milestone-sentence"` is **visible at L0 without hover or click**,
   in a format that includes: a year anchor, a step index, an indicator description, a cohort
   reference, and a consequence phrase ("falls below the recovery floor"). [Exact template —
   CM-PENDING for AC-CM-2]
6. Each indicator curve derived from synthetic data carries
   `data-testid="projection-tier-badge-{indicatorKey}"` adjacent to its curve endpoint.

### 3.3 Secondary observable states

**State A — ADR-017 non-regression:**
At 1280×800 with ZMB ECF in Mode 1 and no `projection_steps`, `data-testid="human-capital-trajectory-panel"`
is absent from the DOM or `display: none`. `data-testid="zone-1a-trajectory"` contains exactly
4 SVG path elements (N=1 Mode 1 four-framework encoding unchanged from pre-G3).

**State B — api_contracts.yml schema currency:**
`docs/schema/api_contracts.yml` contains the `projection_steps` field in the trajectory request
schema, updated in the same commit as the backend implementation (schema drift rule — CLAUDE.md
§Schema registry).

**State C — Performance ceiling:**
End-to-end time from scenario load to `data-testid="human-capital-trajectory-panel"` becoming
visible: ≤ 60 seconds on 4-core hardware (CE Assessment Decision 4 dry-run).

### 3.4 Silent failure detection

*Derived from CE Assessment §2.5 and the DemographicModule feasibility analysis.*

**Silent failure 1 — Adaptive resolution not overridden:**
If Decision 1 was not implemented, daily resolution during a crisis event produces up to
9,125 steps rather than 100 quarterly steps — causing response timeout or memory exhaustion.
Detection: the `steps` array must contain exactly 100 elements when `projection_steps=100`
is sent. An array shorter (timeout/error) or longer (sub-quarterly steps emitted) is a
silent engine failure. AC-7 catches this.

**Silent failure 2 — Indicator decay unbounded:**
If a decay function is unbounded, the 25-year run produces negative or super-unitary values
that appear as valid Decimal strings but represent physically impossible states. The API will
not reject them — only the CE Assessment Decision 4 dry-run gate and AC-6 catch this.

**Silent failure 3 — Projection panel behind drawer:**
If the panel is inside a drawer, it may be present in the DOM but have zero visible dimensions
at 1280×800 without interaction. Detection: `data-testid="human-capital-trajectory-panel"`
must have non-zero `getBoundingClientRect` dimensions without any user gesture. AC-F1 catches this.

**Silent failure 4 — ZMB regression (panel renders on 8-step default scenarios):**
If `projection_steps` is absent but the panel renders anyway, Zone 1A's 4-curve Mode 1 path
is displaced or occluded. Detection: ZMB ECF with no `projection_steps` must show no
`data-testid="human-capital-trajectory-panel"` in the DOM. AC-F7 catches this.

---

## 4. Acceptance Criteria

*Each criterion verifiable by an external observer using only the running application.
"CI passes" is not an AC. AC-1 through AC-10 and AC-F1 through AC-F8 are unblocked for
QA test authorship. AC-CM-1/AC-CM-2/AC-CM-3 require CM review comment on #274 first.*

---

### Backend ACs

*Test file: `backend/tests/test_m16_g3_25year_human_capital_trajectory.py`*

**AC-1 — `projection_steps` field accepted:**
`ScenarioConfigSchema(entities=["SEN"], n_steps=8, projection_steps=100)` instantiates
without validation error. The field is accessible.

**AC-2 — `projection_steps=0` rejected:**
`ScenarioConfigSchema(..., projection_steps=0)` raises `ValidationError`
(or the API returns 422 at the scenario endpoint).

**AC-3 — `projection_steps=101` rejected:**
`ScenarioConfigSchema(..., projection_steps=101)` raises `ValidationError`
(or the API returns 422).

**AC-4 — Non-regression: `projection_steps` absent → `n_steps` governs:**
`ScenarioConfigSchema(entities=["ZMB"], n_steps=8)` with no `projection_steps` field
instantiates without error. Integration: ZMB 8-step scenario runs to completion with
`steps_executed == 8`. Pre-G3 behaviour unchanged.

**AC-5 — Adaptive resolution override explicit at `projection_steps > 8`:**
`WebScenarioRunner` passes `adaptive_resolution=False` to the engine when
`projection_steps > 8`. Verified via a unit test that constructs a scenario config with
`projection_steps=100` and asserts the runner's engine invocation carries the flag explicitly
— a silent constant or an implicit default does not satisfy this AC.

**AC-6 — DemographicModule indicator bounds [0.0, 1.0] across all 100 steps:**
Integration: after running a synthetic SEN fixture with `projection_steps=100` with at least
one subscribed event (`gdp_growth_change`, `imf_program_acceptance`, `capital_controls_imposition`,
or `emergency_declaration`) fired at step 1, all snapshot attribute values for
`poverty_headcount_ratio` (and any CM-confirmed indicator keys) across steps 1–100 are in
[0.0, 1.0] inclusive. Uses a dedicated synthetic SEN fixture — not ZMB values transposed
(CE Assessment Decision 4 dry-run criterion; see Step 4 Verify obligation in §7).

**AC-7 — Trajectory endpoint returns exactly `projection_steps` step objects:**
Integration: after running a SEN scenario with `projection_steps=100`,
`GET /scenarios/{id}/trajectory?entity_id=SEN` returns `step_count == 100` and the
`steps` array has exactly 100 elements.

**AC-8 — `api_contracts.yml` documents `projection_steps`:**
`docs/schema/api_contracts.yml` contains the string `"projection_steps"` within the
trajectory/simulate endpoint request schema definition. Schema updated in the same commit
as the backend implementation (schema drift compliance — CLAUDE.md §Schema registry).

---

### Frontend ACs

*Test file: `frontend/tests/e2e/m16-g3-25year-human-capital-trajectory.spec.ts`*

**AC-F1 — Projection panel visible in primary viewport (no drawer):**
At 1280×800, with SEN scenario and `projection_steps=100` loaded in Mode 1:
`data-testid="human-capital-trajectory-panel"` is visible — `getBoundingClientRect`
shows width > 0 and height > 0 — without any user interaction (no drawer open, no tab click,
no navigation).

**AC-F2 — ≥3 indicator curves displayed:**
Within `data-testid="human-capital-trajectory-panel"`, ≥3 elements matching
`data-testid` pattern `projection-curve-*` are present. (Exact indicator keys in
AC-CM-1 once CM review is filed; minimum pre-CM scope: `projection-curve-poverty_headcount_ratio`
is present.)

**AC-F3 — Layer 3 milestone sentence visible at L0 (no hover):**
At 1280×800 with SEN scenario and `projection_steps=100` loaded and the trajectory rendered,
`data-testid="projection-milestone-sentence"` is visible in the DOM (non-zero bounding box)
without hover or click interaction. The text is non-empty and contains both a year anchor
(a 4-digit year in the range 2025–2050) and a step number in the format "[step N]".

**AC-F4 — Panel header exact text:**
`data-testid="projection-panel-header"` contains the exact string
`"25-year projection · quarterly resolution"`.
Middle-dot character (·, U+00B7). Space on both sides of ·. No leading or trailing whitespace.

**AC-F5 — 100-step axis present:**
`data-testid="projection-panel-step-axis"` is present within the projection panel and visible.
The step axis accommodates 100 steps — it may scroll or zoom internally but must not displace
Zone 1A, Zone 1C, or Zone 1D from the primary viewport.

**AC-F6 — Zone 1A/1C/1D not displaced from primary viewport:**
At 1280×800 with SEN scenario, `projection_steps=100`, and projection panel visible:
`data-testid="zone-1a-trajectory"`, `data-testid="zone-1c-pmm"`, and
`data-testid="zone-1d-four-framework"` are all visible within the 800px viewport height
(each element's `getBoundingClientRect.top` ≤ 800 and `getBoundingClientRect.bottom` > 0).
None are scrolled off-screen by the projection panel.

**AC-F7 — ADR-017 non-regression (ZMB 8-step path unchanged):**
At 1280×800 with ZMB ECF fixture in Mode 1 and no `projection_steps`:
`data-testid="human-capital-trajectory-panel"` is absent from the DOM or has
`display: none`. `data-testid="zone-1a-trajectory"` contains exactly 4 SVG path elements
(N=1 Mode 1 four-framework encoding — unchanged from pre-G3).

**AC-F8 — Performance: panel renders within 60 seconds:**
From the start of the scenario request with `projection_steps=100` to
`data-testid="human-capital-trajectory-panel"` becoming visible: elapsed time ≤ 60,000 ms
on 4-core hardware. (CE Assessment Decision 4 wall-time gate; also confirmed in Step 4 Verify dry-run.)

---

### CM-Confirmed Acceptance Criteria

*CM review filed 2026-06-23 — comment at #274 (2026-06-23). All three ACs are now
finalized. QA Lead may author tests for these ACs immediately.*

*CM findings summary:*
- *Only `poverty_headcount_ratio` has registered elasticities in the current DemographicModule.*
  *`health_index` and `food_insecurity_rate` are in the MDA table but have no elasticity entries*
  *— they produce null curves and must not appear in G3 scope.*
- *Three cohort curves confirmed: Q1 informal, Q1 agriculture, Q2 informal — all `poverty_headcount_ratio`.*
- *`MDA-HD-POVERTY-Q1` floor (≥ 0.40) applies directly to 100-step projection without recalibration.*
- *Bounding risk advisory: the entity attribute store must clamp `VariableType.RATIO` values to*
  *[0.0, 1.0]; the DemographicModule does not clamp internally. CE Assessment Decision 4 dry-run*
  *required before PR is marked ready.*
- *No `MDA-HD-POVERTY-Q2` floor registered; Q2 curve is displayed but cannot trigger a milestone*
  *sentence. Do not fabricate a Q2 floor.*

**AC-CM-1 (Frontend — named indicator curves):** *(CM-confirmed 2026-06-23)*
At 1280×800 with SEN and `projection_steps=100`, the projection panel contains exactly 3 elements
with `data-testid` values matching `projection-curve-*`:

| `data-testid` | Plain label | Cohort entity ID |
|---|---|---|
| `projection-curve-SEN%3ACHT%3A1-25-54-INFORMAL` | "bottom quintile, informal workers" | `SEN:CHT:1-25-54-INFORMAL` |
| `projection-curve-SEN%3ACHT%3A1-25-54-AGRICULTURE` | "bottom quintile, agricultural workers" | `SEN:CHT:1-25-54-AGRICULTURE` |
| `projection-curve-SEN%3ACHT%3A2-25-54-INFORMAL` | "second quintile, informal workers" | `SEN:CHT:2-25-54-INFORMAL` |

Each curve's Y-axis range is [0.0, 1.0]. All three are `poverty_headcount_ratio` (same indicator,
distinct cohort entities). No `health_index` or `food_insecurity_rate` curves appear — those
indicators have no elasticity entries and must not be displayed.

*Note on testid encoding:* Cohort entity IDs contain colons; the `data-testid` attribute uses
URL-encoded colons (`%3A`) or a safe substitution (e.g., dashes). The implementing agent must
choose a consistent encoding scheme and document it; QA tests use the same encoding. The table
above uses `%3A` as the placeholder — the implementing agent may choose a different safe scheme
provided it is consistent across all three curves.

**AC-CM-2 (Frontend — Layer 3 milestone sentence format):** *(CM-confirmed 2026-06-23)*
At 1280×800 with SEN and `projection_steps=100`, at the **first step where `poverty_headcount_ratio`
on any Q1 cohort entity (`SEN:CHT:1-*`) crosses the `MDA-HD-POVERTY-Q1` floor (≥ 0.40)**:
`data-testid="projection-milestone-sentence"` is visible at L0 (no hover, no click) with text
matching the pattern:

> "by [year] [step N], [cohort plain name] poverty headcount crosses the recovery floor — at this level, capability restoration takes a decade or more"

Example (step 20, Q1 informal workers, year 2030):
> "by 2030 [step 20], bottom quintile informal workers poverty headcount crosses the recovery floor — at this level, capability restoration takes a decade or more"

Requirements:
- `[year]` is a 4-digit calendar year derived from `effective_from` at the crossing step
- `[step N]` is the step index (e.g., "step 20")
- `[cohort plain name]` is the plain-language label for the first Q1 cohort to cross
- "decade or more" derives from `MDA-HD-POVERTY-Q1.recovery_horizon_years=10` — the implementing
  agent must derive this phrase from the threshold record, not hardcode it
- If both Q1 cohort curves cross at the same step, the milestone sentence names the lower value

The Q2 informal worker curve (`SEN:CHT:2-*`) has no registered MDA floor and cannot trigger a
milestone sentence. If only the Q2 curve is active and the Q1 curves never cross, no milestone
sentence appears. This is correct behavior — do not fabricate a sentence for an unregistered floor.

**AC-CM-3 (Frontend — Tier 3 badges for all three curves):** *(CM-confirmed 2026-06-23)*
At 1280×800 with SEN and `projection_steps=100`, all three cohort curves carry a Tier 3 confidence
badge adjacent to the curve endpoint:

| Badge `data-testid` | Text content |
|---|---|
| `projection-tier-badge-SEN%3ACHT%3A1-25-54-INFORMAL` (or equivalent) | `"T3"` |
| `projection-tier-badge-SEN%3ACHT%3A1-25-54-AGRICULTURE` (or equivalent) | `"T3"` |
| `projection-tier-badge-SEN%3ACHT%3A2-25-54-INFORMAL` (or equivalent) | `"T3"` |

All three are Tier 3 confidence: values are synthetic SEN data, and the elasticity relationships
are derived from literature (Tier 3 per `docs/DATA_STANDARDS.md §Confidence Tier System`).
No curve is higher than Tier 3 under current data conditions.

---

## 4b. Visual Spec (before/after)

*Required per template §4b — projection panel introduces text display, label format,
and layout states that a QA reviewer must match exactly.*

### AC-F1 / AC-F6 — Projection panel in primary viewport (layout)

**Before (pre-G3, SEN scenario, no projection_steps):**
```
Viewport: 1280×800 | Zone: Primary viewport | data-testid="human-capital-trajectory-panel"

SEN scenario loaded, Mode 1, projection_steps NOT SET:
┌─────────────────────────────────────────────────┐  ← 0px
│ Zone 1A: zone-1a-trajectory — VISIBLE           │
│ Zone 1B: zone-1b-mda-alerts — VISIBLE           │
│ Zone 1C: zone-1c-pmm — VISIBLE                  │
│ Zone 1D: zone-1d-four-framework — VISIBLE       │
└─────────────────────────────────────────────────┘  ← 800px

data-testid="human-capital-trajectory-panel": ABSENT or display:none
```

**After (G3, SEN scenario, projection_steps=100):**
```
Viewport: 1280×800 | Zone: Primary viewport | data-testid="human-capital-trajectory-panel"

SEN scenario loaded, Mode 1, projection_steps=100:
┌─────────────────────────────────────────────────┐  ← 0px
│ Zone 1A: zone-1a-trajectory — VISIBLE ✓        │
│ Zone 1B: zone-1b-mda-alerts — VISIBLE ✓        │
│ Zone 1C: zone-1c-pmm — VISIBLE ✓               │
│ Zone 1D: zone-1d-four-framework — VISIBLE ✓    │
├─────────────────────────────────────────────────┤
│ data-testid="human-capital-trajectory-panel"    │  ← VISIBLE, width > 0, height > 0
│ ┌─────────────────────────────────────────────┐ │
│ │ projection-panel-header:                   │ │
│ │ "25-year projection · quarterly resolution" │ │
│ │                                             │ │
│ │ — projection-curve-poverty_headcount_ratio  │ │
│ │ — projection-curve-{CM indicator B}    T3  │ │  ← projection-tier-badge-{key}
│ │ — projection-curve-{CM indicator C}    T3  │ │
│ │                                             │ │
│ │ projection-milestone-sentence (L0, visible) │ │
│ │ "by 2031 [step 20], poverty headcount in   │ │
│ │  the bottom quintile falls below the        │ │
│ │  recovery floor"                            │ │
│ │                                             │ │
│ │ projection-panel-step-axis: Q0 ─── Q100   │ │
│ └─────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────┘  ← 800px (panel may clip internally)

Key constraint: Zone 1A, 1C, 1D remain VISIBLE above the panel.
Scroll within the panel's own step axis is acceptable.
Displacement of Zone 1A/1C/1D off-screen is NOT acceptable.
```

### AC-F4 — Panel header exact string

**Before:**
```
Viewport: 1280×800 | Zone: human-capital-trajectory-panel | data-testid="projection-panel-header"

BEFORE: Element absent from DOM.
```

**After:**
```
Viewport: 1280×800 | Zone: human-capital-trajectory-panel | data-testid="projection-panel-header"

AFTER:  "25-year projection · quarterly resolution"
         ^                  ^ ^
         │                  │ └── "quarterly resolution" — exact casing, no trailing space
         │                  └── middle-dot U+00B7, space on both sides — not a hyphen
         └── "25-year projection" — exact casing, no leading space
```

### AC-F3 / AC-CM-2 — Layer 3 milestone sentence (example; CM confirms exact template)

**Before (at step 0, no MDA floor crossed yet):**
```
Viewport: 1280×800 | Zone: human-capital-trajectory-panel | data-testid="projection-milestone-sentence"

BEFORE (step 0 or no floor crossing in range):
  Element absent from DOM OR display:none.
  No placeholder text ("Calculating...", "N/A", "—") is acceptable in this position.
```

**After (at first step where indicator crosses MDA floor):**
```
Viewport: 1280×800 | Zone: human-capital-trajectory-panel | data-testid="projection-milestone-sentence"

AFTER (CM-confirmed template — see AC-CM-2):
  "by 2030 [step 20], bottom quintile informal workers poverty headcount
   crosses the recovery floor — at this level, capability restoration
   takes a decade or more"
   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
   Visible at L0 — no hover, no click.
   Required elements (all confirmed by CM 2026-06-23):
     • Year anchor: 4-digit year derived from effective_from at crossing step
     • Step reference: "[step N]" format
     • Cohort plain name: one of the CM-confirmed plain labels (not raw enum)
     • Trigger phrase: "crosses the recovery floor"
     • Consequence phrase: "capability restoration takes a decade or more"
       (derived from MDA-HD-POVERTY-Q1.recovery_horizon_years=10)
```

---

## 5. Kryptonite Constraint Check

*Authority: `docs/process/agent-execution-lifecycle.md §Kryptonite Design Constraint (FD-3)`.*

**Does this implementation's primary observable state require specialist mediation for Persona 2
to act on it in the Reactive entry state (90-second ceiling)?**

`[x]` **No** — conditioned on the Layer 3 milestone sentence (AC-F3 / AC-CM-2) being present
and correctly authored.

Rationale:

- **Milestone sentence (Layer 3 — primary Demo 6 citable output):** "by 2031 [step 20],
  poverty headcount in the bottom income quintile falls below the recovery floor" is
  self-interpreting. Persona 2 can read it in under 10 seconds and cite it at the table.
  No demographic expertise is required to understand "falls below the recovery floor."
  The sentence is the argument; the 100-step curve is the supporting evidence.

- **Trajectory curves (Layer 2 — supporting visual):** The 100-step indicator curves
  require demographic expertise to interpret in detail — rate of change, recovery timeline,
  elasticity decomposition. This is an accepted asymmetry: G3 is a Preparatory tool. The
  milestone sentence extracts the Reactive-state-usable argument from the curves so that
  Persona 2 does not need to interpret curves under negotiation pressure.

- **Kryptonite test:** A finance ministry analyst on Persona 5's team can cite the milestone
  sentence at the Article IV table without specialist translation. The 100-step curve is the
  evidence behind the claim. The Layer 3 output satisfies the kryptonite constraint; the Layer 2
  curve does not violate it because it is not the cited artifact.

**Named asymmetry gap (accepted, not hidden):** A well-resourced analytical team can interpret
the full 100-step curve shape and extract additional insights (rate-of-change decomposition,
elasticity-level attribution, recovery bifurcation analysis). The Senegalese ministry team
can cite the milestone sentence but cannot perform that deeper analysis in the Reactive state
without specialist support. This gap is documented. Forward trace: per-cohort 25-year drill-down
is a post-G3 Layer 3 improvement — not in G3 scope.

**Kryptonite failure condition:** If the milestone sentence uses raw attribute keys
(`poverty_headcount_ratio: 0.47 [MDA FLOOR: 0.45]`) instead of plain language ("poverty
headcount in the bottom income quintile falls below the recovery floor"), the kryptonite
constraint fails. The Customer Agent Layer 3 assessment at Step 5 Validate will catch this.

---

## 6. Out of Scope

**Multi-entity long-run projection (N > 1 at 100 steps):**
Demo 6 is single-entity (SEN). Multi-entity at 100 steps is not assessed in the CE Assessment.

**Real SEN data preparation:**
Covered by #843 demo preparation. G3 tests use a synthetic SEN fixture. Real-data integration
is a demo prep task, not a G3 code deliverable.

**Mode 2/3 long-run projection:**
Mode 1 replay at extended horizon is the Demo 6 requirement. Mode 2/3 long-run projection
involves control-plane interaction not assessed for 100-step depth.

**New `/project` endpoint:**
CE Assessment Decision 2 specifies Option A (extend existing endpoint). No new endpoint.

**Adaptive-resolution-aware long-run mode design:**
CE Assessment Decision 1 specifies disable-only (`adaptive_resolution: false`). The flag
is a simple parameter override, not a new resolution strategy.

**G2 deliverables (#986 cohort disaggregation, #987 political risk summary):**
G3 must not touch Zone 1D layout or the cohort disaggregation component. The projection
panel is a standalone primary-viewport element separate from G2's surface changes.

**Zone 1B step axis expansion to 100 steps:**
The projection panel provides its own 100-step axis (`data-testid="projection-panel-step-axis"`).
Zone 1B's 8-step MDA alert axis is not modified by G3.

---

## 7. Test Authorship Obligation

**QA Lead:** QA Lead Agent
**Test authorship deadline (non-CM-gated):** Before any G3 implementation PR opens against `release/m16`
**Test authorship deadline (CM-PENDING ACs):** After CM review comment on #274 is filed

**Test file locations:**
- Backend pytest: `backend/tests/test_m16_g3_25year_human_capital_trajectory.py`
- Frontend E2E: `frontend/tests/e2e/m16-g3-25year-human-capital-trajectory.spec.ts`

**ACs available for immediate QA test authorship:**
AC-1, AC-2, AC-3, AC-4, AC-5, AC-6, AC-7, AC-8 (backend)
AC-F1, AC-F2, AC-F3, AC-F4, AC-F5, AC-F6, AC-F7, AC-F8 (frontend)

**ACs blocked pending CM review comment on #274:**
AC-CM-1, AC-CM-2, AC-CM-3

**Soft-skip guard (NM-056 follow-up, sprint entry §2.4):**
Neither test file may contain `test.skip()` or conditional skip patterns. The 100-step backend
projection test (AC-7) must not soft-skip on backend startup failure — the G3 implementation
PR must not merge until this test runs and passes in CI. M16 exit checklist (#985) confirms
no active soft-skip patterns before it closes.

**CE Assessment Decision 4 dry-run obligation (Step 4 Verify gate):**
Before marking the G3 implementation PR ready for review, the implementing agent must perform
a dry-run of the SEN scenario at `projection_steps=100` on 4-core hardware and record in the
Step 4 Verify verdict: (a) end-to-end wall time; (b) min/max of each DemographicModule indicator
across all 100 steps. If wall time > 60 seconds or any indicator value is outside [0.0, 1.0],
Step 4 Verify verdict is FAIL — the PR must not be marked ready.

**QA Lead acknowledgment:**
`[x]` QA Lead: Tests for AC-1 through AC-8 and AC-F1 through AC-F8 authored and filed. [2026-06-23]
`[x]` QA Lead: Tests for AC-CM-1 through AC-CM-3 authored and filed (CM-confirmed 2026-06-23 — may proceed). [2026-06-23]

---

*Intent document authority: `docs/process/intent-template.md` (version 2026-06-17).
Sprint entry: `docs/process/sprint-plans/m16-g3-sprint-entry.md` (EL Approved 2026-06-23).
CE Assessment authority: `docs/process/sprint-plans/m16-g3-sprint-entry.md §2.5`.
Implementing agents: Chief Engineer Agent (backend); Frontend Architect Agent (trajectory display).
No parent ADR — Architect consultation confirmed M4 DemographicModule boundary satisfied.*
