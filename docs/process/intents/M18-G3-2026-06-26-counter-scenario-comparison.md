---
name: M18-G3-counter-scenario-comparison
type: implementation-intent
issue: "#1349"
status: UX/UI mockups and panel review complete — implementation PR may open
authored-by: PM Agent
authored-date: 2026-06-26
implementing-agent: Frontend Architect Agent (frontend); Computation Engine Agent (backend)
sprint-entry: "docs/process/sprint-plans/m18-g3-sprint-entry.md — awaiting EL approval"
adr-reference: "None — Architect Option A CLEAR 2026-06-26: comparison summary is a Zone 1B Sub-zone B content extension within ADR-018 Sub-zone B pattern and ADR-007 CI band methodology; no new ADR required"
governing-adrs:
  - "ADR-018 (Sub-zone B proportional allocation — ACCEPTED) — Sub-zone B CohortImpactSection is the implementation surface"
  - "ADR-007 (Synthetic data framework — ACCEPTED) — CI band computation and tier inheritance methodology"
  - "ADR-015 (Evidence Thread Architecture — ACCEPTED) — Zone 1B content model context"
  - "ADR-017 (Zone 1A information architecture — ACCEPTED) — CI bands from G1 consumed by G3 differential computation"
release-branch: release/m18
bpo-acceptance-required: "Yes — new user-facing Zone 1B element (screen recording of Demo 7 Act 2 flow required)"
customer-agent-l3-required: "Yes — Personas 1 and 5 (at sprint exit)"
schema-prerequisite: "docs/schema/api_contracts.yml must be updated with distributional differential endpoint before implementation PR opens"
gr-source: "docs/process/intents/M18-GR-2026-06-26-counter-scenario-comparison.md"
sprint-journal: "#1377"
---

# Implementation Intent: M18-G3 — Counter-Scenario Comparison (#1349)

> **Pre-implementation prerequisites:**
> - [x] UX mockup filed — §8 UX Mockup (2026-06-27, UX Designer)
> - [x] UI mockup filed — §8 UI Mockup (2026-06-27, UX Designer)
> - [x] UX/UI panel review complete — UX Designer ACCEPT, Customer Agent ACCEPT, BPO ACCEPT (2026-06-27, GitHub #1349)
> - [ ] `docs/schema/api_contracts.yml` updated with distributional differential endpoint shape — required in implementation PR
>
> **Design reference for mockup authorship:** GR §2.3 (`docs/process/intents/M18-GR-2026-06-26-counter-scenario-comparison.md`) contains the element specification and ASCII layout. UX Designer authors formal mockups from that specification.
>
> **All four Architect implementation constraints (from sprint entry §0) are encoded in this document and are non-negotiable.**

---

## 0. Architect Implementation Constraints

*Authority: Architect determination on #1349, 2026-06-26. These constraints are not design preferences — they follow from the ADR determination (Option A CLEAR) and the code architecture analysis. Any implementation diverging from these constraints is a process deviation.*

1. **Implementation surface:** The comparison summary is rendered inside `zone1bCohortSection` (Sub-zone B / `CohortImpactSection`) as a **sticky-bottom element** — it is NOT a third occupant in `InstrumentCluster.tsx`, not a new Zone, and not a new column. `InstrumentCluster.tsx` and `ScenarioInstrumentCluster.tsx` are out of scope for G3 (confirmed in sprint entry §2 and §6.2).

2. **Viewport constraint:** At 1280×800, the comparison summary is visible via sticky-bottom positioning while per-scenario threshold rows scroll above it. At 1440×900 (expected Demo 7 viewport), Sub-zone B provides sufficient height for both per-scenario rows and the comparison summary to be simultaneously visible. The implementing agent must verify at implementation time that the comparison summary is not cut off at 1280×800.

3. **Schema prerequisite:** `docs/schema/api_contracts.yml` must be updated with the distributional differential endpoint specification before the G3 implementation PR opens. This is a schema-first requirement per CLAUDE.md §Schema registry. The schema update may be committed on `sprint/m18-g3` in a preparatory commit or included in the implementation PR — it must be on the branch before the PR opens.

4. **Tier inheritance:** The CI band tier classification (T2 or T3) depends on the headcount conversion methodology. If the conversion from composite score delta to poverty headcount uses a regional average or model-derived income distribution (Tier 3), the differential inherits T3 — not T2. The implementing agent determines the correct tier at implementation time from the conversion methodology and documents it in the PR description. T-tier badge in the element must match the determined tier.

---

## 1. Source

**Issue:** #1349 — feat(demo7): counter-scenario comparison — distributional number differential with CI bands for Demo 7 Act 2

**GR source document:** `docs/process/intents/M18-GR-2026-06-26-counter-scenario-comparison.md` — all user stories, persona Layer 3 assessments, and design specification originate here.

**Architect determination:** Option A CLEAR (2026-06-26, comment on #1349). No new ADR required. The comparison summary is a Zone 1B Sub-zone B content addition within existing ADR authority:
- ADR-018 established the Sub-zone B (CohortImpactSection) extension pattern in M17 G3 Phase 3
- ADR-007 authorizes CI band computation methodology; the differential's CI band inherits from ADR-007
- ADR-017 does not govern Zone 1B content; it governs Zone 1A encoding rules (CI bands from G1 operate within ADR-017's authority; G3 consumes that output)

**M17 prerequisite (verified):** #394 (N=3 multi-scenario comparison API) is CLOSED and on `main`. G3 backend computation is a new computation layer on top of the M17 multi-scenario response — the distributional differential endpoint takes M17's per-scenario composite output as its input.

**Demo 7 anchor:** Act 2 — Zambia (ZMB), three restructuring scenarios. The citable claim the Finance Ministry's team must be able to make: *"Under the IMF-proposed terms, 340,000 more Zambians will be below the poverty threshold at programme end than under our counter-proposal. The direction is stable across the full uncertainty range."*

---

## 2. Persona Trace

**P-1 — Personas served:**

| Persona | Entry state | Role in G3 |
|---|---|---|
| Eleni Papadimitriou (Persona 2 — Finance Ministry Negotiator) | Preparatory (evening before session) | Reads comparison summary; enters negotiation with citable number |
| Eleni Papadimitriou (Persona 2) | Active Negotiation (at the table, tablet open) | Cites differential within 90 seconds; no drawer, no interaction |
| Aicha Mbaye (Persona 5 — Finance Minister) | Demonstrative (analyst briefing) | Reads summary in ≤30 seconds; forms position; requires plain language |
| Lucas Ferreira (Persona 1 — Programme Analyst) | Preparatory (building analytical record) | Audits methodology; accesses expandable methodology disclosure |

**P-2 — Entry states and time ceilings:**

- Preparatory: no time ceiling, but output must be citable without further calculation
- Active Negotiation: 90-second ceiling (Persona 2) — element visible without interaction from Zone 1 default view
- Demonstrative: 30-second ceiling (Persona 5 reading the element while analyst narrates)

**P-3 — Journey step:** Journey A Step 6 (N=3 COMPARE_VIEW, three-scenario comparison); Demo 7 Act 2.

**P-4 — Time/interaction ceiling:** 90 seconds (Persona 2 active negotiation), 30 seconds (Persona 5 demonstrative). Element must be visible in Zone 1 without any click, hover, drawer open, or navigation. Zero interactions to reach the number.

**P-6 — Negotiating leverage (Persona 2):**
Eleni can cite: *"Under Option A — the proposed EFF front-loaded terms — our model shows 340,000 more Zambians below the poverty threshold at programme end compared to Option C. The 95% confidence interval runs from 295,000 to 395,000. The direction is stable: this is not a modelling artefact. Regardless of where within the uncertainty range the true value falls, the proposed terms produce worse poverty outcomes than our homegrown programme."*

Before G3: Eleni could show that Option A crosses the CRITICAL threshold (M17) — a binary argument the IMF can challenge by contesting the threshold level. After G3: the argument is distributional and quantified, shifting the IMF's required response from "threshold" to "calibration of the differential."

**P-7 — North star capability delivered:**
The Zambia Ministry of Finance analyst can cite a specific poverty headcount differential between programme options — with a confidence band and direction-stability declaration — that did not require any calculation from the analyst and is engine-derived. The argument changes from binary (threshold crossed / not) to distributional (how many people, with what confidence, stable in direction).

---

## 3. Observable Application State

### 3.1 Primary observable state

**In N=3 COMPARE_VIEW with the Zambia three-scenario fixture loaded (three scenario curves visible in Zone 1A):**

A comparison summary element with `data-testid="distributional-comparison-summary"` is present in Zone 1B, positioned below the per-scenario threshold crossing rows (CRITICAL/WARNING labels from M17). The element is visible at 1280×800 without any scroll, click, hover, or navigation.

The element shows:
- A header: "DISTRIBUTIONAL COMPARISON" with a step label ("step 8 of 8") and a T-tier badge (T2 or T3 — per implementing agent's tier determination)
- For each non-reference scenario (Options A and B, relative to Option C as reference), one row showing:
  - Scenario pair labels in plain language (not only letter codes)
  - A poverty headcount differential as a plain integer with "persons" (e.g., "+340,000 persons")
  - A CI band in the format "X – Y  95% CI" where X and Y are integers in the same units
- A direction disclosure: "Direction stable across uncertainty range" (when CI interval is entirely positive or entirely negative for all pairs) OR a direction-uncertain disclosure (when any CI interval spans zero)

### 3.2 Secondary observable states

**State A — Direction stability fires only when warranted:**
When the CI band for a scenario pair spans zero (lower bound negative, upper bound positive), the direction stability statement does NOT appear. A direction-uncertain disclosure appears instead: "Direction uncertain — model uncertainty exceeds the estimated differential." The implementing agent determines the exact phrasing; the QA test asserts the direction stability text is absent when the CI spans zero.

**State B — Element absent when N < 2 or COMPARE_VIEW not active:**
The comparison summary element (`data-testid="distributional-comparison-summary"`) is not rendered when the Mode 2 view shows a single scenario (N=1) or when the instrument cluster is in single-scenario mode. The element appears only when COMPARE_VIEW is active with ≥2 scenarios loaded and a reference scenario designated.

**State C — Methodology disclosure accessible (Zone 3, not Zone 1):**
An expandable methodology disclosure is accessible from within the comparison summary element (icon or text link — not a drawer). When expanded, it shows: (a) the entity's base population, (b) the income share parameter used for the Q1 cohort, (c) the conversion factor from composite score delta to headcount, and (d) the CI propagation methodology. This is a Zone 3 surface — it must exist but is not required to be visible without interaction. Zone 1 requirement applies only to the headline differential and CI band.

### 3.3 Silent failure detection

**Silent failure — composite score displayed instead of headcount:**
If the element renders "+0.14" instead of "+340,000 persons," the engine is returning the composite score delta, not the headcount conversion. Observable: the displayed value is a decimal less than 1.0 with a format like "0.XX". AC-1349-C and the backend test both catch this — the E2E test asserts the element text does NOT match composite score pattern (`/0\.\d{2}/`); the backend test asserts the endpoint returns an integer headcount, not a float composite delta.

**Silent failure — direction stability fires when CI spans zero:**
If the direction stability statement appears when the CI interval spans zero (CI lower bound is negative while upper bound is positive), the direction gate condition is incorrect. AC-1349-E catches this: when a fixture produces a CI spanning zero, the direction stability text must be absent.

**Silent failure — element requires scroll at 1280×800:**
If the comparison summary is rendered but is below the fold at 1280×800, it is not reachable in 30 seconds without interaction. AC-1349-B (viewport assertion) catches this: at exactly 1280×800, the element's bounding box must be within the viewport without scroll.

---

## 4. Acceptance Criteria

*Derived from user stories US-1349-A through D (GR §4.3) and persona Layer 3 constraints (GR §3). Each criterion is testable from the running application without reading implementation code.*

**AC-1349-A (E2E — element present in COMPARE_VIEW):**
In N=3 COMPARE_VIEW with the Zambia three-scenario fixture loaded, when the instrument cluster renders Zone 1B, then `[data-testid="distributional-comparison-summary"]` is present in the DOM and visible (not display:none, not zero dimensions).
*Source: US-1349-A (Eleni, Preparatory) + US-1349-B (Eleni, Active Negotiation)*

**AC-1349-B (E2E — visible at 1280×800 without scroll):**
In N=3 COMPARE_VIEW at viewport 1280×800, when the comparison scenario view is loaded, then `[data-testid="distributional-comparison-summary"]` has a bounding box entirely within the viewport (bottom edge ≤ 800px) without any scroll event having fired.
*Source: US-1349-B (90-second ceiling, Zone 1 constraint) + GR §3.2 (Persona 2 constraint)*

**AC-1349-C (E2E — plain-language headcount, no composite score notation):**
In N=3 COMPARE_VIEW with the Zambia three-scenario fixture, the text content of `[data-testid="distributional-comparison-summary"]` matches the pattern `/\d{1,3}(,\d{3})+\s+persons/` (i.e., an integer headcount followed by "persons") AND does NOT match `/0\.\d{2}/` (composite score decimal) AND does NOT contain the substring "composite".
*Source: US-1349-C (Persona 5 legibility) + GR §3.3 (Persona 5 kryptonite check)*

**AC-1349-D (E2E — CI band present):**
In N=3 COMPARE_VIEW with the Zambia three-scenario fixture, the text content of `[data-testid="distributional-comparison-summary"]` contains a CI band in the format matching `/\d+[,K]?\s*[–—]\s*\d+[,K]?\s+95%\s+CI/i`.
*Source: US-1349-A + GR §2.3 (CI band format specification)*

**AC-1349-E (E2E — direction stability fires only when CI does not span zero):**
Given a three-scenario Zambia fixture where the CI interval for at least one scenario pair does NOT span zero: `[data-testid="distributional-comparison-summary"]` contains the text "Direction stable" (or the exact phrase determined at implementation). Given a fixture where the CI interval for a pair spans zero: the element does NOT contain "Direction stable" and DOES contain a direction-uncertain disclosure.
*Source: GR §2.3 (direction stability condition) + GR §3.2 (Persona 2 false precision assessment)*

**AC-1349-F (E2E — element absent in single-scenario mode):**
When the instrument cluster is in single-scenario mode (N=1) and Zone 1B is rendered, `[data-testid="distributional-comparison-summary"]` is absent from the DOM or has `display:none`.
*Source: GR §2.3 ("element does not render when N < 3 or when only one reference scenario is designated")*

**AC-1349-G (backend — distributional differential endpoint):**
`POST /api/v1/scenarios/comparison/distributional-differential` (or the endpoint path determined in the schema update) with the Zambia three-scenario fixture input returns:
- Per-step headcount differential for each non-reference scenario vs. reference scenario
- CI band bounds (lower, upper) per step
- Tier classification ("T2" or "T3") in the response body
- Terminal step differential that matches the expected Zambia fixture value within ±5% tolerance
- Response does NOT return a composite score delta field as the primary differential value
*Source: GR §3.1 (Lucas reproducibility + auditability) + sprint entry §2.4 backend test spec*

**AC-1349-H (backend — tier inheritance documented):**
The endpoint response includes a `tier` field indicating T2 or T3. The implementing agent's PR description includes a one-paragraph explanation of tier inheritance: the conversion methodology used (named publication or model assumption), the tier classification of that methodology, and the resulting tier inheritance for the differential. This AC is verified at PR review, not by automated test.
*Source: GR §3.1 (Lucas false precision assessment) + Architect constraint 4 + sprint entry §0*

---

## 4b. Visual Spec (before/after)

**AC-1349-A / AC-1349-C / AC-1349-D (before — Zone 1B, N=3 COMPARE_VIEW, no G3):**
```
Viewport: 1280×800 | Zone: Zone 1B | data-testid="zone-1b-cohort-section"

[Per-scenario threshold crossing rows — M17 capability]

Option A (EFF Front-Loaded): CRITICAL Q1 Poverty headcount · step 2
Option B (IMF Carve-Out): WARNING Q1 Poverty headcount · step 4
Option C (Homegrown): CLEAR

[No comparison summary element. No poverty headcount differential visible.
The analyst must mentally compute the delta from Zone 1A composite scores.]
```

**AC-1349-A / AC-1349-C / AC-1349-D (after — Zone 1B with G3 implemented):**
```
Viewport: 1280×800 | Zone: Zone 1B | data-testid="distributional-comparison-summary"

[Per-scenario rows — M17, scroll above if space is constrained]

Option A (EFF Front-Loaded): CRITICAL Q1 Poverty headcount · step 2
Option B (IMF Carve-Out): WARNING Q1 Poverty headcount · step 4
Option C (Homegrown): CLEAR

──────────────────────────────────────────────── ← sticky-bottom
DISTRIBUTIONAL COMPARISON  [step 8 of 8 · T2]
────────────────────────────────────────────────
Poverty headcount differential

Option A vs. Option C        +340,000 persons
(front-loaded vs. homegrown)   295K – 395K  95% CI

Option B vs. Option C        +210,000 persons
(carve-out vs. homegrown)      175K – 255K  95% CI

→ Direction stable across uncertainty range
────────────────────────────────────────────────
```

*Note: The ASCII layout above is the design specification from GR §2.3. The formal UX mockup (to be filed by UX Designer) may refine visual treatment (typography, color, spacing, T-tier badge placement) — but the layout structure, label format, units, and CI band positioning must match this specification. The implementing agent and panel review the formal mockup for compliance before implementation PR opens.*

**data-testid anchors required:**
- Outer wrapper: `data-testid="distributional-comparison-summary"`
- Per-pair differential row: `data-testid="comparison-pair-{scenarioA-id}-vs-{scenarioB-id}"`
- Direction disclosure: `data-testid="direction-stability-disclosure"`
- T-tier badge: `data-testid="comparison-tier-badge"`

---

## 5. Kryptonite Constraint Check

**Does this implementation require specialist mediation for Persona 2 (Eleni, Active Negotiation, 90-second ceiling)?**

`[x]` **No — provided the element is implemented as specified.** The number "+340,000 persons" with "Direction stable across uncertainty range" is self-interpreting. Eleni does not need to know what a composite score is, what a CI propagation methodology is, or how to convert Q1 poverty headcount from simulation units. The element surfaces the conclusion in the units of the argument she needs to make.

**Kryptonite check by persona:**

| Persona | Kryptonite risk | Assessment |
|---|---|---|
| Persona 1 (Lucas) | None on primary reading. Auditability required — methodology disclosure must exist in Zone 3. | PASS with §3.2 State C |
| Persona 2 (Eleni) | None IF plain-language headcount used and NO composite score notation appears. AC-1349-C guards this. | PASS with AC-1349-C |
| Persona 5 (Aicha) | HIGH RISK if element shows "Q1 composite delta: +0.14" or any decimal value. AC-1349-C explicitly prohibits this pattern. 30-second reading ceiling means the element must be interpretable on first read, zero mediation. | PASS with AC-1349-C + AC-1349-B |

**Kryptonite patterns that would constitute REJECT at BPO acceptance:**
- Any decimal composite score value appearing as the primary differential display
- Text containing "composite," "normalized," or unit-agnostic metric names
- Element requires any interaction (click, hover, expand) for the headline number to be visible
- Element visible only when scrolling below the fold at 1280×800

**Direction stability statement legibility (Persona 5):**
"Direction stable across uncertainty range" must be interpretable by Aicha. Rationale: "stable" and "across uncertainty range" are interpretable as "the model says this is reliable regardless of its own uncertainty" — which matches how the Finance Minister would expect to be briefed. The phrase must NOT use "CI," "confidence interval," or statistical jargon in the direction disclosure itself; those appear only in the CI band notation where Lucas reads them.

---

## 6. Backend Computation Specification

*This section is the backend implementation contract. It must be read alongside `docs/schema/api_contracts.yml` (after the schema update).*

### 6.1 — Input: M17 multi-scenario API output

The distributional differential computation takes as input the M17 N=3 multi-scenario comparison response — specifically, the composite score per scenario per step for the Q1 poverty headcount indicator. The G3 endpoint is a new computation layer on top of the existing M17 comparison API, not a replacement.

### 6.2 — Computation: composite score delta to poverty headcount

**Step 1 — Composite score delta per scenario pair per step:**
For each non-reference scenario S and reference scenario R, compute `delta(t) = score_S(t) - score_R(t)` at each step t. A positive delta means scenario S has a higher poverty headcount than the reference — worse outcome.

**Step 2 — Conversion to poverty headcount:**
Apply the entity's Q1 cohort conversion factor: `headcount_delta(t) = delta(t) × population × q1_income_share_factor`. The conversion factor parameters come from the entity's configuration (Zambia/ZMB). The implementing agent identifies the correct parameter source (entity configuration, calibration registry, or hardcoded Zambia fixture value) and documents this in the PR description.

**Step 3 — CI band propagation:**
The CI band on `headcount_delta(t)` propagates from the CI bands on `score_S(t)` and `score_R(t)`. The uncertainty is propagated through the linear delta and conversion: `ci_headcount(t) = [delta_ci_lower(t) × conversion_factor, delta_ci_upper(t) × conversion_factor]`. If the conversion factor is itself uncertain (T3 — regional average), the CI band widens accordingly and tier inheritance becomes T3.

**Step 4 — Terminal step default:**
The API response includes per-step differentials. The frontend renders the terminal step by default. The step-axis selection behavior (secondary, not required for Demo 7) is deferred — the API must return per-step data to support it without a future breaking change.

**Step 5 — Direction stability flag:**
A `direction_stable: boolean` flag per scenario pair, computed as: `direction_stable = (ci_lower > 0) OR (ci_upper < 0)` — the CI interval does not span zero at the terminal step. This flag drives the frontend's direction stability statement.

### 6.3 — G1 soft dependency

The CI band inputs to G3's computation come from G1's uncertainty banding engine output. G3 backend tests can be authored against a fixture with the G1 uncertainty data shape (from G1's intent document schema spec) before G1 merges. Full end-to-end integration test (real G1 CI band data → G3 differential) requires G1 to be merged to `release/m18` before G3's integration PR exits. PM Agent enforces the merge order at G3 exit.

---

## 7. Schema Prerequisite

**File:** `docs/schema/api_contracts.yml`

**Required addition before implementation PR opens:**

New endpoint documentation for the distributional differential computation. Minimum required fields:

- Endpoint path and HTTP method
- Request body: scenario IDs, reference scenario designation, entity ISO code
- Response shape:
  - Per-step array with: step number, per-pair headcount differential (integer), per-pair CI band lower and upper bounds (integers), direction stability flag (boolean)
  - Terminal step highlighted or clearly indicated
  - Tier classification field (string: "T2" or "T3")
  - Methodology summary field (string — for methodology disclosure)
- Error cases: N < 2 (no reference), entity missing Q1 calibration data

The schema update may be committed to `sprint/m18-g3` as a standalone preparatory commit and referenced in the implementation PR — or included in the implementation PR itself. It must exist on the branch before the implementation PR is opened.

---

## 8. UX/UI Design Artifact Status

*Authority: sprint entry §2.3 (UX/UI design artifact gate — mandatory for new UI elements).*
*Authored: UX Designer, 2026-06-27. Panel review complete. Implementation PR may open.*

---

### 8a. UX Mockup — Placement and Viewport Behaviour

**Authored by:** UX Designer
**Session context:** Same session as panel review — acknowledged
**Governing documents reviewed:** `docs/ux/information-hierarchy.md §1B (Sub-zone B)`, `docs/ux/design-thinking/worldsim-ux-architecture-first-principles.md §Premises 1–2`

**Zone 1B placement diagram:**

```
Zone 1B — CohortImpactSection (MDAAlertPanelZone1B.tsx)
╔══════════════════════════════════════════════════════╗
║  Sub-zone A  (MDA threshold markers — unchanged)     ║
╠══════════════════════════════════════════════════════╣
║  Sub-zone B  (CohortImpactSection)                   ║
║  ┌────────────────────────────────────────────────┐  ║
║  │  Per-scenario Q1 poverty rows (M17 G2)         │  ║  ← scroll if >3 scenarios
║  │  Option A (EFF Front-Loaded): CRITICAL · s2   │  ║
║  │  Option B (IMF Carve-Out):    WARNING  · s4   │  ║
║  │  Option C (Homegrown):        CLEAR           │  ║
║  ├────────────────────────────────────────────────┤  ║  ← sticky-bottom divider (1px border-top)
║  │  G3 DISTRIBUTIONAL COMPARISON  [step 8 · T2]  │  ║  ← sticky-bottom; always visible
║  │  Poverty headcount differential                │  ║
║  │  Option A vs. C    +340,000 persons            │  ║
║  │                    295K – 395K  95% CI         │  ║
║  │  Option B vs. C    +210,000 persons            │  ║
║  │                    175K – 255K  95% CI         │  ║
║  │  → Direction stable across uncertainty range   │  ║
║  └────────────────────────────────────────────────┘  ║
╚══════════════════════════════════════════════════════╝
```

**Viewport behaviour:**

| Viewport | Sub-zone B height | Per-scenario rows | Sticky summary | Both visible simultaneously |
|---|---|---|---|---|
| 1280×800 | ~80px available | 3 rows ≈ 48px | ~32px | Yes — tight but sufficient |
| 1440×900 | ~100px available | 3 rows ≈ 48px | ~32px | Yes — comfortable |
| <1280 wide | Not a Demo 7 target | — | — | Not required |

**Sticky behaviour:** The comparison summary is the `position: sticky; bottom: 0` child of `CohortImpactSection`. Per-scenario rows occupy the scrollable upper section. At N=3 with 3 rows visible, no scroll is needed at 1280×800 — both sections fit. If future N>3 is added, rows scroll above the pinned summary.

**Relationship to existing Zone 1B content:** The sticky-bottom element does not displace or overlay per-scenario rows. The `1px border-top` divider creates visual separation consistent with existing Zone 1B section dividers.

**Implementation requirement (from panel):** The implementing agent must verify at 1280×800 that all three per-scenario rows AND the comparison summary are simultaneously visible without scroll. If this fails, reduce per-scenario row height before touching the sticky summary.

---

### 8b. UI Mockup — Visual Treatment

**Authored by:** UX Designer
**Session context:** Same session as panel review — acknowledged
**Governing documents reviewed:** `docs/ux/information-hierarchy.md §1B`, `docs/ux/north-star.md §Primary Cognitive Tasks`

**Element structure and typography:**

```
┌─────────────────────────────────────────────────────┐
│ DISTRIBUTIONAL COMPARISON    step 8 of 8      [T2]  │  ← header row
│ Poverty headcount differential                       │  ← section label
│                                                      │
│ Option A vs. Option C                +340,000 persons│  ← pair row (value bold)
│   (front-loaded vs. homegrown)   295K – 395K  95% CI│  ← sub-row (subdued)
│                                                      │
│ Option B vs. Option C                +210,000 persons│
│   (carve-out vs. homegrown)      175K – 255K  95% CI│
│                                                      │
│ → Direction stable across uncertainty range          │  ← direction disclosure
└─────────────────────────────────────────────────────┘
```

**Typography and colour spec:**

| Element | Size | Weight | Colour token | Notes |
|---|---|---|---|---|
| Header label "DISTRIBUTIONAL COMPARISON" | 11px | medium | `text-gray-500` | uppercase |
| Step indicator "step 8 of 8" | 11px | normal | `text-gray-400` | right of header label |
| T-tier badge "[T2]" | 10px | medium | `text-gray-600 bg-gray-100` | pill, `rounded-full px-1.5`; NO colour encoding of tier level (a11y) |
| Section label | 12px | normal | `text-gray-600` | italic |
| Scenario pair label | 12px | medium | `text-gray-800` | e.g. "Option A vs. Option C" |
| Scenario sub-label | 11px | normal | `text-gray-500` | e.g. "(front-loaded vs. homegrown)" |
| Differential value | 14px | semibold | `text-amber-700` | e.g. "+340,000 persons" |
| CI band | 11px | normal | `text-gray-500` | e.g. "295K – 395K  95% CI" |
| Direction stable statement | 11px | normal | `text-gray-600` | italic; "→ Direction stable across uncertainty range" |
| Direction uncertain statement | 11px | normal | `text-amber-600` | italic; "→ Direction uncertain: CI spans zero" |

**Container treatment:**
- Background: inherits Zone 1B container background — no elevation, no shadow
- Top boundary: `border-t border-gray-200` — matches existing Zone 1B section dividers
- Padding: `py-2 px-3` — consistent with existing `CohortImpactSection` content padding
- No interactive affordances (no hover, no focus ring, no click handlers)

**State variations:**

| State | Direction disclosure | Amber colour |
|---|---|---|
| All pairs direction-stable | "→ Direction stable across uncertainty range" (grey) | Differential value only |
| Any pair direction-uncertain | "→ Direction uncertain: CI spans zero" (amber) | Disclosure line + differential value |
| No comparison data (single-scenario) | Element absent | N/A |

---

### 8c. Panel Review Record

Panel reviews posted as GitHub comments on issue #1349 (2026-06-27).

- [x] **UX Designer** — ACCEPT (conditional; see below)
- [x] **Customer Agent** — ACCEPT
- [x] **Business PO** — ACCEPT

**UX Designer verdict (same session — acknowledged):**

Governing documents reviewed: `information-hierarchy.md §1B (Sub-zone B content model)`, `north-star.md §Primary Cognitive Tasks`, `worldsim-ux-architecture-first-principles.md §Premises 1–2 (instruments always visible without interaction)`.

Concerns: (1) The implementing agent must verify at exactly 1280×800 that per-scenario rows and sticky summary are simultaneously visible — if space is tight, reduce per-scenario row height before modifying the sticky element. (2) Direction-uncertain amber must be visually distinguishable from direction-stable grey in low-contrast conditions. (3) T-tier badge must not use colour to encode tier level (colour-blind accessibility). All three are implementation requirements, not design blockers.

Verdict: **ACCEPT** — conditional on the three implementation requirements above being verified before the implementation PR is marked ready for review.

**Customer Agent verdict:**

Governing documents reviewed: `docs/ux/personas.md §Persona 5 (Aicha — Finance Minister, 30-second legibility ceiling)`, `§Persona 1 (Lucas — economist, auditability)`, GR §3 (Layer 3 assessment).

Persona 5 (Aicha): "+340,000 persons" + "Direction stable across uncertainty range" is self-interpreting within 30 seconds. No composite score notation. No interaction required for the headline number. The direction disclosure uses plain language ("stable," "uncertain") that maps directly to how a finance minister would expect to be briefed. Layer 3 legibility: PASS.

Persona 1 (Lucas): Methodology disclosure available via Zone 3 (§3.2 State C). T-tier badge provides calibration proxy. Auditability path exists without cluttering the primary display. PASS.

Verdict: **ACCEPT**.

**Business PO verdict:**

Governing documents reviewed: GR §4 (BPO business requirements, US-1349-A through US-1349-D), `docs/process/sprint-plans/m18-sprint-plan.md §North Star Test`.

- US-1349-A (element visible at 1280×800 without scroll): sticky-bottom positioning satisfies. PASS.
- US-1349-B (plain-language headcount, not percentage): "+340,000 persons" satisfies. PASS.
- US-1349-C (CI band present): "295K – 395K 95% CI" satisfies. PASS.
- US-1349-D (direction stability statement): "Direction stable across uncertainty range" satisfies. PASS.

North star test: The Zambian ministry analyst can show "+340,000 more Zambians below the poverty threshold under proposed terms, direction stable across the model's uncertainty range" directly from Zone 1B — without calculation, interaction, or specialist mediation — at the Demo 7 Act 2 live presentation. This is a citable, arguable claim at the negotiating table. PASS.

Verdict: **ACCEPT**.

---

**Binding spec rule (sprint entry §2.3):** All three panel verdicts are ACCEPT. Implementation PR may open. The implementing agent confirms this section exists before opening the feature branch PR.

---

## 9. Out of Scope

**Step-selector interaction (step ≠ terminal):** The comparison summary defaults to the terminal step. Interactive step selection (clicking the Zone 1A step axis to update the differential) is a secondary behavior — the API must return per-step data, but the frontend step-selection behavior is not required for Demo 7. Deferred to capacity-allowing scope.

**Multi-indicator comparison (health, governance, ecological):** G3 scope is poverty headcount differential only. The element design and API must not be architected to prevent future extension to additional indicators, but extending beyond poverty headcount is explicitly out of scope for G3.

**Export / download of comparison summary:** Not required for Demo 7.

**Historical precedent display:** Not in #1349 scope. GR §4.1 confirmed poverty headcount differential is the Demo 7 Act 2 minimum viable deliverable.

**`InstrumentCluster.tsx` and `ScenarioInstrumentCluster.tsx` modifications:** These files are out of scope for G3. The comparison summary is passed via the existing `zone1bCohortSection` prop (per Architect constraint 1). No column restructuring.

**Composite score display in the element:** Not out of scope in the "nice to have" sense — PROHIBITED. The element must not surface composite score deltas. This is a hard constraint, not a deferral.

**CI band methodology redesign:** The CI band computation follows ADR-007. G3 applies the existing methodology to the new differential quantity — it does not amend or extend ADR-007.

---

## 10. Test Authorship Obligation

**QA Lead:** QA Lead Agent (E2E); Computation Engine Agent (backend pytest)

**Test authorship deadline:** Both test files authored and committed to `sprint/m18-g3` before the first implementation code PR opens. Tests run red before implementation; run green after.

**Test file locations:**
- `frontend/tests/e2e/m18-g3-counter-scenario-comparison.spec.ts` — Playwright E2E
- `backend/tests/test_m18_g3_counter_scenario_comparison.py` — pytest

**Criteria covered by E2E test:**
- AC-1349-A: element presence in COMPARE_VIEW
- AC-1349-B: viewport visibility at 1280×800
- AC-1349-C: plain-language headcount, no composite score notation
- AC-1349-D: CI band format present
- AC-1349-E: direction stability fires correctly and does not fire when CI spans zero
- AC-1349-F: element absent in single-scenario mode

**Criteria covered by backend pytest:**
- AC-1349-G: distributional differential endpoint returns headcount differential, CI bands, tier classification, and matches expected Zambia fixture value within ±5% tolerance

**No soft-skip patterns (NM-056 guard):** All E2E assertions must be hard-fail. If a Zambia three-scenario fixture is not achievable before implementation, the implementing agent documents this explicitly in the PR description — the test must be structured to fail, not skipped.

**Pre-push gates (mandatory before any push):**
- Backend: `cd backend && source .venv/bin/activate && ruff check . && mypy app/` — both must exit 0
- Frontend: `cd frontend && npm run build` — must exit 0

**QA Lead acknowledgment:**
- [x] E2E tests for AC-1349-A through AC-1349-F authored and filed at `frontend/tests/e2e/m18-g3-counter-scenario-comparison.spec.ts`. [Date: 2026-06-27, PR #1395]
- [x] Backend tests for AC-1349-G authored and filed at `backend/tests/test_m18_g3_counter_scenario_comparison.py`. [Date: 2026-06-27, PR #1395]

---

*Intent document authority: `docs/process/sprint-plans/m18-g3-sprint-entry.md §2.3` (intent gate) and `docs/process/sprint-plans/m18-g3-sprint-entry.md §4` (implementation sequencing). GR source: `docs/process/intents/M18-GR-2026-06-26-counter-scenario-comparison.md`. Issue: #1349. Sprint journal: #1377. This document is the QA authorship contract and the implementation contract — a discrepancy between the delivered capability and §3 Observable Application State is a Verify-step failure, not a document-update opportunity. Authoring authority: `docs/process/agents.md §Architect Agent`, `docs/process/intent-template.md`. Filed: 2026-06-26.*
