# M19 Screenshot Brief — UX Designer Agent

> Generated: 2026-07-05. Produced by UX Designer Agent for Demo 8 / M19 stakeholder demo preparation.
>
> Five frames specified for the M19 stakeholder demo: two-act structure.
> Act 1 — Zambia 2010, Mode 3 active control, constraint-floor search FOUND state
>   (ControlPlaneColumn Form 3, ZMB Option C baseline, fiscal multiplier boundary = 0.83).
> Act 2 — Zambia debt restructuring, three-scenario distributional comparison
>   with Bayesian posterior-calibrated CI bounds and "declared interval (BandingEngine)" label.
>
> **Architecture changes from M18 Demo 7:**
> - **ControlPlaneColumn Form 3 — Constraint Search (ADR-021, G1 #1540):** A third form
>   section ("CONSTRAINT SEARCH", teal Emerald-700 `#047857`) is mounted below Forms 1 and 2.
>   When a focal cohort is configured, Form 3 displays the floor constraint and a
>   "Find safe boundary" button. On successful search, the column transitions to the
>   FOUND state: three teal-styled lines — "Safe boundary found:", the boundary value
>   ("fiscal multiplier ≥ 0.83"), and the precision band ("±0.01 precision") — followed
>   by the evaluations count and the searched range. `data-testid="constraint-search-found"`,
>   `data-testid="constraint-boundary-value"`, `data-testid="constraint-tolerance-band"`.
> - **PSP driver arc in Zone 1D (G4 #1528):** `psp-driver-arc` renders a horizontal row of
>   per-step driver abbreviation badges across the full programme window — not only the
>   current step. The badge for the current step is bold-bordered; prior/future steps are
>   dimmed. This allows the presenter to show the causal driver trajectory across the
>   programme arc, not just at the active moment.
> - **CI label precision (#1529):** `DistributionalComparisonSummary` `distributional-ci-label`
>   now reads "declared interval (BandingEngine)" — replacing the prior "95% CI" string.
>   This is an epistemic precision improvement: the interval is a structural uncertainty model
>   output, not a frequentist confidence interval.
> - **Zone 1D delta annotations (ADR-017):** In Mode 3, each framework score in Zone 1D
>   carries a coloured delta annotation vs. the baseline — `(+0.04)` green or `(−0.02)` amber.
>   `data-testid="framework-delta-{key}"` for each of the four frameworks.
> - **Bayesian posterior CI (ADR-007 G3 #1537):** The Zone 3 methodology panel expansion
>   now shows posterior-calibrated tier multipliers. The `methodology-ci-band` field in the
>   expanded panel describes the Bayesian posterior calibration methodology rather than the
>   prior T3 placeholder description.
> - **No choropleth narration (UX-RULING-4):** The choropleth is geographic context only.
>   All five frames show instruments (Zone 1A/1B/1C/1D + control column) as the primary
>   surface. Do not narrate quantitative change from the choropleth.

---

## Thesis Frame

**Frame A — "The Boundary Found" (Act 1, Zambia, Mode 3, Form 3 FOUND)**

The single image that most completely communicates the Demo 8 argument: Mode 3 active,
`ControlPlaneColumn` visible on the right with Form 3 showing the FOUND state. The teal
"Safe boundary found: fiscal multiplier ≥ 0.83" text is the thesis in two lines. Zone 1A
shows the Option C baseline trajectory and the branch at the found boundary simultaneously.
The instrument did not display a slider value entered by the analyst — it returned an answer.

This frame communicates the Demo 8 thesis in one image: the constraint-floor instrument
locates the safe boundary automatically. The finance ministry analyst does not test
multiplier values one by one hoping to find one that avoids the threshold. The instrument
finds it and reports it. The counter-proposal has a number — and the number came from the tool.

---

## Five Frames

### Frame A — "The Boundary Found" ← THESIS FRAME (Act 1, ZMB, Mode 3, Form 3 FOUND, fm=0.83)

**What Zone 1 + control column shows:** Zambia at a mid-programme step (expected: step 4–5,
whichever shows the sharpest baseline/branch divergence in Zone 1A with Option C as baseline).
Mode 3 active. `ControlPlaneColumn` visible at right with all three form sections visible;
Form 3 ("CONSTRAINT SEARCH", teal header) is in the FOUND state — the search has completed
and the result is rendered. The FOUND state text occupies the lower portion of the column.
Zone 1A shows two simultaneous trajectory sets: the Option C baseline (lighter/labeled) and
the branch at fiscal multiplier 0.83 (bolder/labeled), with CI ribbons at Mode 3 reduced
opacity (5%). Zone 1D shows the four-framework current position with per-framework delta
annotations visible in green/amber against the baseline. Zone 1B shows the focal cohort
(bottom quintile poverty headcount) at or above the 0.40 floor.

**Zone 1 requirements:**

- **1A (Trajectory View + CI bands):** Two complete trajectory sets visible — Option C
  baseline and the 0.83 branch — without overlap confusion. CI ribbons present at 5%
  opacity around each curve. MDA floor lines overlaid as horizontal dashed threshold lines.
  Both sets clearly above the human development MDA floor at this step. Step axis labeled.
  The divergence region (5–10% fill between baseline and branch) visible where they separate.

- **1B (MDA Alert Panel + CohortImpactSection):** Focal cohort row visible — bottom quintile
  poverty headcount indicator name, current value at this step, "≥ 0.400" floor label.
  If the value is above 0.400, the CLEAR badge (green) should be visible. MDA alert panel
  present. `DistributionalComparisonSummary` sticky-bottom NOT present (Act 1 is single-scenario;
  Act 2 loads the three-scenario comparison).

- **1C (PMM Widget):** PMM value rendered at this step; direction indicator present.

- **1D (Four-Framework + PSP + driver + delta annotations):** All four framework scores
  visible simultaneously. PSP severity badge present. `psp-driver-row` readable — "Driver:
  fiscal sustainability" or whichever driver is dominant at the captured step. Per-framework
  delta annotations visible: `framework-delta-financial`, `framework-delta-human_development`,
  `framework-delta-ecological`, `framework-delta-governance` — coloured green for positive
  delta, amber for negative. Both `psp-driver-row` and delta annotations readable at 1440×900.

- **ControlPlaneColumn (Form 3 FOUND — primary focus of this frame):**
  - Form 1 ("POLICY INSTRUMENTS", blue) header visible at top of column — may be collapsed
    or minimised; must not obscure Form 3.
  - Form 2 ("SCENARIO SHOCKS", orange) header visible below Form 1.
  - Form 3 ("CONSTRAINT SEARCH", teal Emerald-700) full FOUND state visible:
    - Floor label: `data-testid="constraint-floor-label"` — e.g. "Poverty headcount floor: ≥ 0.400"
    - `data-testid="constraint-search-found"` container present
    - `data-testid="constraint-boundary-value"` — "fiscal multiplier ≥ 0.83" in teal 14px bold
    - `data-testid="constraint-tolerance-band"` — "±0.01 precision" in gray 11px
    - Evaluations line — "{N} evaluations · [0.1, 3.0] searched" in gray 10px
    - Precision disclosure — "This is the binary search precision, not a statistical confidence
      interval." in light gray 10px
  - Form 3 FOUND state is the compositional anchor of the control column in this frame.

**Zone 2 (choropleth):** ZMB visible and highlighted. Geographic context only — not
analytical instrument per UX-RULING-4. May be partially visible at the left; not the
compositional focus.

**Caption:** Zambia, Mode 3 active. CONSTRAINT SEARCH returns: **fiscal multiplier ≥ 0.83**
(±0.01 precision). The instrument found the boundary — no manual multiplier search required.
Zone 1A shows the Option C baseline and the boundary-found branch simultaneously.

**UI state:** Mode 3 active. Form 3 search completed: FOUND state rendered. Branch applied
at fiscal multiplier = 0.83. Both trajectories visible in Zone 1A at the same time. Control
column visible at right. No drawer open.

**Viewport:** 1440×900 (mandatory per demo-preparation-standard.md Step 4).

**Presenter direction:** Point to Form 3 FOUND state first — read "fiscal multiplier ≥ 0.83"
aloud. Then sweep left to Zone 1A and indicate the two trajectories. The argument is:
"the instrument found the answer; Zone 1A confirms what it means for the trajectory."
Do not open Zone 2 (choropleth). Do not open the drawer.

---

### Frame B — "The Arc of the Boundary" (Act 1, ZMB, Mode 3, Step 4, PSP driver arc)

**What Zone 1 + control column shows:** Zambia at step 4 in Mode 3, with the 0.83 fiscal
multiplier branch applied. The compositional focus of this frame is the PSP driver arc in
Zone 1D: the horizontal row of per-step driver abbreviation badges visible across the full
programme window, showing which causal driver dominated at each step. The current-step badge
(step 4) is bold-bordered; other steps are dimmed. Zone 1A shows the Mode 3 CI bands at
5% opacity. ControlPlaneColumn remains visible with Form 3 FOUND state persisted from Frame A.

**Zone 1 requirements:**

- **1A (CI bands focus):** CI ribbons must be photographically distinguishable from the
  trajectory lines — semi-transparent fill clearly present at Mode 3 opacity (5%). Both
  baseline and branch trajectory sets present. The branch trajectory above all MDA floor
  lines at step 4. Step 4 annotation visible on step axis.

- **1D (PSP driver arc — primary focus of this frame):**
  - `data-testid="psp-driver-arc"` — the horizontal badge row must be visible and readable
    at 1440×900. The row shows abbreviated driver labels (e.g. "FS" for fiscal sustainability,
    "ES" for external balance, "SS" for social stability, "GV" for governance) at each step
    index across the full programme window (steps 1–N).
  - The step 4 badge carries `fontWeight: 700` and a `1px solid #555` border — visually
    distinguishable from the dimmed badges at other steps.
  - `data-testid="psp-driver-row"` shows the current-step driver label: "Driver: [category]".
    This must be readable — font size and truncation must not hide the driver name.
  - Per-framework delta annotations (`framework-delta-{key}`) visible below each score.

- **1B:** Focal cohort section still visible; CLEAR badge present if value above 0.40 floor.
  No comparison summary (single-scenario Act 1).

- **1C:** PMM value present at step 4.

- **ControlPlaneColumn:** Form 3 FOUND state persisted from Frame A. All three form headers
  visible. Must be simultaneously visible with Zone 1 instruments.

**Caption:** Step 4, [calendar date]. Zone 1D PSP driver arc: the dominant causal driver
at each programme step, named and sequenced. At step 4, the driver is [driver name]. Zone 1A
CI bands confirm the branch trajectory holds above MDA floors at 5% opacity.

**UI state:** Mode 3 active. Same Form 3 FOUND state as Frame A (0.83 fiscal multiplier
branch applied). Step 4 active. `psp-driver-arc` visible in Zone 1D.

**Viewport:** 1440×900.

**Presenter direction:** Point to the `psp-driver-arc` badge row in Zone 1D first — "each
badge is one programme step; the bold one is now." Then scan left to Zone 1A. Do not narrate
from the choropleth. The arc is the narrative: this is not one number at one moment, it is
the causal story of the whole programme window.

---

### Frame C — "The Act 1 Finding" (Act 1, ZMB, Mode 3, focal cohort CLEAR at 0.83)

**What Zone 1 shows:** Zambia at the terminal programme step in Mode 3, with the 0.83 fiscal
multiplier branch applied. The compositional focus is Zone 1B CohortImpactSection: the bottom
quintile poverty headcount focal cohort row. The finding is the CLEAR badge (green) — at
fiscal multiplier 0.83, the poverty headcount indicator remains at or above the 0.40 floor
at programme end. Zone 1A showing the full programme trajectory arc for both baseline and
branch, with CI ribbons. ControlPlaneColumn still visible with Form 3 FOUND state.

**Zone 1 requirements:**

- **1B (CohortImpactSection — primary focus):** The bottom quintile poverty headcount focal
  cohort row must be the compositional focus of this frame. Requirements:
  (a) indicator display name readable — not the raw DB field key;
  (b) current value at the terminal step readable (e.g. 0.412 or whichever value the
      simulation produces — do not pre-declare; capture simulation output);
  (c) "≥ 0.400" floor label visible alongside the value;
  (d) CLEAR badge (green, `#2e7d32`) visible — confirming the threshold is not crossed
      at the boundary-found configuration;
  (e) T3 tier badge visible;
  (f) the framing is capability analysis, not alarm: "above the floor" is a finding, not a relief.
  If the simulation shows the value at or below 0.400 despite the 0.83 boundary, this frame
  must reflect the actual simulation output — see narration note below.

- **1A (Trajectory View):** Zone 1A trajectory at the terminal step — the full programme
  arc visible for both baseline and branch, from step 1 to terminal. Both arcs above MDA
  floor lines. CI ribbons at 5% opacity.

- **1D:** PSP severity at terminal step, driver label, delta annotations vs. baseline.

- **1C:** PMM at terminal step.

- **ControlPlaneColumn:** Form 3 FOUND state persisted. Column visible but not the
  compositional focus — Zone 1B is the focus.

**Caption — two versions depending on simulation output:**
- *If CLEAR (expected):* Terminal step, [calendar date]. Zone 1B focal cohort: poverty
  headcount at [value] — above the 0.40 floor. At fiscal multiplier 0.83, the threshold
  is not crossed. This is the ministry's Act 1 answer.
- *If CROSSED (unexpected):* Terminal step, [calendar date]. Zone 1B focal cohort: poverty
  headcount at [value] — below the 0.40 floor despite the searched boundary. The crossing
  is structural to the programme design at this resolution. See presenter narration note 2.

**UI state:** Mode 3 active. Fiscal multiplier = 0.83 branch applied. Terminal step active.
Zone 1B CohortImpactSection focal cohort row prominent. Form 3 FOUND state visible at right.

**Viewport:** 1440×900.

**Presenter direction:** Point to Zone 1B focal cohort row first — read the value and the
floor aloud. Then reference the Form 3 FOUND state on the right: "the instrument found 0.83;
Zone 1B confirms the indicator holds." This is the Act 1 close: from search invocation
(Frame A) to human cost confirmation (Frame C). Transition to Act 2 after this frame.

---

### Frame D — "The Counter-Proposal as a Declared Interval" (Act 2, ZMB, Terminal Step)

**What Zone 1 shows:** Act 2. Zambia. Three scenarios loaded: Option A (EFF Front-Loaded),
Option B (EFF Gradual), Option C (Homegrown Programme, reference). Zone 1A showing three
composite trajectory curves with Bayesian posterior-calibrated CI bands (Mode 1 or Mode 2,
full opacity 12%). Zone 1B sticky-bottom: `DistributionalComparisonSummary` visible — the
primary content of this frame. The M19 distinction from M18 Frame D: the CI label now reads
"declared interval (BandingEngine)" rather than "95% CI."

**Zone 1 requirements:**

- **1B sticky-bottom (DistributionalComparisonSummary — primary focus):** The comparison
  summary must be clearly readable at 1440×900. Requirements:
  (a) differential number readable — "+342,700 persons" (or the actual simulation output —
      do not manually set this value; capture what the simulation shows);
  (b) CI band bounds readable — "{lower}K – {upper}K" format;
  (c) CI label readable — `data-testid="distributional-ci-label"` must show **"declared
      interval (BandingEngine)"**, not "95% CI". This is the M19 epistemic precision change
      and must be legible in the screenshot;
  (d) tier badge readable — "T3";
  (e) direction stability text readable — "→ Direction stable across uncertainty range"
      or equivalent (whichever string the component renders);
  (f) reference scenario label visible ("vs. Option C" or "Option C (Reference)");
  (g) the Zone 3 auditability panel must be **collapsed** in this frame — Frame E shows it
      expanded. The methodology-panel-toggle affordance should be visible (so the audience
      can see it is interactive).

- **1A (three-scenario trajectories + CI bands):** All three scenario curves visible —
  distinguishable by color or label. CI bands at full opacity (Mode 1/2, 12%), Bayesian
  posterior-calibrated widths. Option A, Option B, Option C trajectories readable as
  distinct. The trajectory divergence between Option A and Option C visible (visual
  counterpart to the "+342,700 persons" number). MDA floor lines overlaid.

- **1D:** PSP driver present for the active entity at the terminal step; no delta annotations
  (delta annotations require Mode 3; Act 2 is Mode 1 or Mode 2).

- **1C:** PMM present.

**Zone 2 (choropleth):** ZMB visible — geographic context only per UX-RULING-4.

**Caption:** Zambia, programme end. Three scenarios: Option A (IMF Front-Loaded), Option B
(Gradual), Option C (Ministry counter-proposal). Zone 1B reads: "+342,700 persons · [bounds]K
· **declared interval (BandingEngine)** · T3 · Direction stable." The epistemic label is
precise: this is a structural uncertainty model, not a frequentist confidence interval.

**UI state:** Three scenarios loaded for ZMB. Terminal step active. `DistributionalComparisonSummary`
visible and collapsed (Zone 3 panel closed). Mode 1 or Mode 2 (not Mode 3 — Act 2 is
comparison, not active control). No drawer open. `distributional-ci-label` readable.

**Viewport:** 1440×900.

**Presenter direction:** Point to `DistributionalComparisonSummary` in Zone 1B first. Read
the differential number. Then specifically call out the "declared interval (BandingEngine)"
label — contrast it with "95% CI" explicitly: "this is not a frequentist confidence interval;
it is the structural uncertainty model's declared range." Then gesture to the collapsed
methodology-panel-toggle: "we can open the methodology if challenged." Frame E is the
follow-through on that sentence.

---

### Frame E — "The Bayesian Posterior Defence" (Act 2, ZMB, Terminal Step, Zone 3 Expanded)

**What Zone 1 shows:** Same Zambia state as Frame D — terminal step, three scenarios, Zone 1A
trajectories with Bayesian posterior-calibrated CI bands. Zone 1B: `DistributionalComparisonSummary`
with Zone 3 methodology panel **expanded** below it (`data-testid="zone3-methodology-panel"`).
The expanded panel shows the posterior calibration methodology: Q1 population base, CI band
methodology description (BandingEngine with posterior-calibrated tier multipliers), extraction
path, and tier rationale.

**Zone 1 requirements:**

- **1B (DistributionalComparisonSummary + Zone 3 expanded — primary focus):**
  - The summary row above the expanded panel must still be readable — differential number,
    bounds, "declared interval (BandingEngine)" label, tier, direction stability must remain
    visible in the collapsed header or summary row.
  - The methodology panel expanded below — `data-testid="zone3-methodology-panel"` visible:
    - `data-testid="methodology-q1-population"` — "Q1 population: ZMB: [N] (UN WPP 2024,
      20% Q1 fraction)" readable.
    - `data-testid="methodology-ci-band"` — the CI band methodology description readable.
      In M19, this field contains the Bayesian posterior calibration methodology — the tier
      multiplier override via `CalibrationStore`, the posterior correction factor κ, and the
      ADR-007 §8.2–§8.5 reference. This is the key M19 methodological advancement visible
      here: the interval is posterior-calibrated, not a structural prior alone.
    - `data-testid="methodology-extraction-path"` — extraction path readable.
    - `data-testid="methodology-tier-rationale"` — tier rationale readable.
  - The expand/collapse affordance (`data-testid="methodology-panel-toggle"`) visible above
    the expanded content — so the audience can see it is interactive and user-invoked.
  - If the full expanded panel requires scroll to show all four fields, capture the top
    two — Q1 population and CI band methodology are the most important. The CI band
    methodology field (Bayesian posterior) is the content that traces back to the
    "declared interval" label in Frame D.

- **1A:** Three-scenario trajectories with CI bands still visible above Zone 1B. Zone 1A
  must not be completely occluded by the expanded methodology panel — trajectory context
  confirms we are looking at the same Zambia comparison, not a different view.

- **1D + 1C:** Present; not the compositional focus of this frame.

**Caption:** Zone 3 expanded — Bayesian posterior calibration methodology visible from Zone 1B
without drawer navigation. The "declared interval (BandingEngine)" label in Frame D traces
to this: posterior-calibrated tier multipliers (ADR-007 §8.2–§8.5), not a frequentist 95% CI.
Persona 1 (Lucas) can defend the methodology under IMF scrutiny from the primary viewport.

**UI state:** Zone 3 methodology panel expanded (via user click or Playwright click on
`methodology-panel-toggle` before screenshot capture). `DistributionalComparisonSummary`
summary row still visible above. Zone 1A trajectory context visible above. Three scenarios
still loaded. Terminal step.

**Viewport:** 1440×900.

**Presenter direction:** Point to `methodology-panel-toggle` first — "this is the expand
affordance." Then read the "CI band:" field aloud — reference the Bayesian posterior
calibration explicitly. This is the Demo 8 methodological close: the constraint search found
the boundary (Act 1); the calibrated interval defends the differential (Act 2); and here is
the methodology behind both claims, visible in Zone 1B without opening a drawer.

---

## Presentation Sequence

| Order | Frame | Act | ZMB Step | Why |
|---|---|---|---|---|
| 1 — THESIS | A — The Boundary Found | Act 1 (ZMB Mode 3) | ~4–5 (max divergence) | Lead with the constraint search result — the instrument found the answer |
| 2 | B — The Arc of the Boundary | Act 1 (ZMB Mode 3) | 4 | PSP driver arc + delta annotations — the causal and quantitative arc across the programme |
| 3 | C — The Act 1 Finding | Act 1 (ZMB Mode 3) | Terminal | CLEAR badge — the human cost confirmation at the found boundary |
| 4 | D — The Declared Interval | Act 2 (ZMB, 3-scenario) | Terminal | "+342,700 persons · declared interval (BandingEngine)" — the counter-proposal as a precisely labelled number |
| 5 | E — The Bayesian Posterior Defence | Act 2 (ZMB, 3-scenario) | Terminal | Zone 3 expanded — the methodology behind the declared interval, visible under scrutiny |

**Rationale:** Lead with the Act 1 constraint-search thesis (A) — it establishes Demo 8's
primary capability claim (the instrument finds the boundary rather than the analyst searching
manually). The driver arc frame (B) grounds the boundary in the causal structure across the
programme arc. Frame C closes Act 1 with the human cost confirmation that justifies the boundary
claim. Act 2 frames D and E follow in argument order: the quantified counter-proposal first
(with the M19 epistemic label change as the visible signal), the posterior methodology defence
second. The presentation flows: search result → causal arc → human cost confirmation → declared
interval → methodological defence.

---

## Pre-Capture Requirements

| Requirement | Source | Must verify |
|---|---|---|
| ZMB scenario loaded with Option C as Mode 3 baseline | G1 backend scenario fixture (ADR-021) | `GET /api/v1/scenarios/{id}` returns ZMB, Option C |
| Focal cohort configured for ZMB: poverty headcount, floor = 0.400 | G1 backend scenario config | `focal_cohorts[0].floor_value == 0.400` in scenario fixture |
| Mode 3 entry via "Enter Active Control" button | G4 frontend (ADR-019) | `data-testid="enter-active-control"` present and clickable |
| ControlPlaneColumn Form 3 visible in Mode 3 with FOUND state | G1 frontend (ADR-021) | `data-testid="constraint-search-found"` present after search completion |
| `constraint-boundary-value` shows "fiscal multiplier ≥ 0.83" | G1 backend + frontend | Value from constraint-floor-search API response |
| `constraint-tolerance-band` shows "±0.01 precision" | G1 backend + frontend | Tolerance computed from `uncertainty_hi - uncertainty_lo` |
| Evaluations count line present | G1 frontend | `{N} evaluations · [0.1, 3.0] searched` visible in Form 3 FOUND |
| Zone 1A shows both baseline and branch at found multiplier | G1 frontend | Two trajectory sets visible simultaneously after constraint search completes |
| CI bands render at Mode 3 opacity (0.05) | G1 frontend (TrajectoryView.tsx) | Semi-transparent fills visible at 5% opacity |
| `psp-driver-arc` visible in Zone 1D | G4 frontend (FourFrameworkZone1D.tsx) | `data-testid="psp-driver-arc"` present; badge row rendered across programme window |
| Current-step arc badge is bold-bordered | G4 frontend | `fontWeight: 700` and `border: "1px solid #555"` on current-step badge |
| Per-framework delta annotations visible in Zone 1D (Mode 3) | G4 frontend (ADR-017) | `data-testid="framework-delta-{key}"` present for all four frameworks |
| ZMB three scenarios loaded simultaneously for Act 2 | G3 demo fixture | Three scenario IDs registered; `comparisonScenarios.length === 3` |
| `DistributionalComparisonSummary` renders at terminal step | G3 frontend | `data-testid="distributional-comparison-summary"` visible and non-empty |
| `distributional-ci-label` reads "declared interval (BandingEngine)" | G4 frontend (#1529) | NOT "95% CI" — M19 epistemic precision change |
| Zone 3 methodology panel collapsed for Frame D, expanded for Frame E | G5 frontend | `data-testid="zone3-methodology-panel"` absent in Frame D; present in Frame E |
| `methodology-ci-band` shows Bayesian posterior calibration text | G3 backend + frontend (#1537) | Field content references posterior-calibrated tier multiplier, not T3 placeholder |
| CI bands render at standard opacity (0.12) in Mode 1/2 for Act 2 | G1 frontend | Frames D/E have visually wider/more opaque bands than Frames A–C |
| Zone 1B sticky-bottom does not obscure Zone 1A | G3 CSS (overflow + sticky) | Zone 1A still partially visible with DistributionalComparisonSummary sticky |
| Zone 3 expanded panel visible without scroll (or CI band field in top portion) | G5 frontend | `zone3-methodology-panel` renders with `methodology-q1-population` and `methodology-ci-band` in viewport |
| Viewport set to 1440×900 in `demo-narrated.spec.ts` | Pre-capture gate (Step 6) | `page.setViewportSize({ width: 1440, height: 900 })` before first `page.goto()` |

---

## Key Narration Notes

1. **UX-RULING-4: No choropleth narration for quantitative change.** Say "Zone 1A shows
   the trajectory split" or "Form 3 returns the boundary" — not "watch Zambia shift on
   the map." The choropleth anchors geography. The instruments carry the argument.

2. **Frame C outcome is simulation output.** If the simulation shows the focal cohort
   value above 0.400 at the found boundary (CLEAR badge, expected), use the CLEAR caption.
   If the value is below 0.400 despite the search (unexpected — would indicate a boundary
   precision or floor definition issue), use the alternative caption and escalate to the
   engineering team before the demo. Do not pre-declare the outcome in preparation.

3. **"declared interval" is the epistemic signal of M19.** Emphasise the label change
   from M18 ("95% CI") to M19 ("declared interval (BandingEngine)") in Frame D narration.
   This is not a cosmetic change — it is a statement about what the interval is. The Bayesian
   posterior calibration in Frame E is the methodological substance behind the label.
   NARRATION-RULING-1 applies: umbrella first ("we are looking at the uncertainty interval
   behind the differential"), then fact ("the label reads 'declared interval (BandingEngine)'"),
   then synthesis ("this is the structural uncertainty model — not a frequentist CI").

4. **Constraint search boundary value 0.83 must be confirmed from simulation output.**
   The value 0.83 is the expected output from the G1 sprint and is carried in this brief
   as the reference value. Before screenshots are finalised, confirm the live constraint-floor
   search returns `boundary = 0.83` for the ZMB Option C scenario with the 0.400 poverty
   headcount floor. If the search returns a different value, update the brief captions and
   the walkthrough accordingly. Do not use a manually forced value.

5. **Zone 3 expanded panel (Frame E):** The expand action requires a user interaction
   (click on `methodology-panel-toggle`). In the Playwright spec, this requires a
   `page.click('[data-testid="methodology-panel-toggle"]')` before screenshot capture.
   Confirm the `data-testid` from `frontend/src/components/MDAAlertPanelZone1B.tsx`
   line 764 before authoring the spec step.

6. **PSP driver arc frame (Frame B):** The arc badge row renders as small text (8px) in
   a flex row. At 1440×900 this should be readable, but verify during the legibility gate
   (Step 5b) that the badge row is not truncated or overflowing at the column width.
   The bold border on the current-step badge is the visual anchor — confirm it is
   photographically distinguishable from the dimmed badges.

---

*Screenshot brief authored by UX Designer Agent, 2026-07-05.*
*Demo 8 is the M19 exit demo. Demo 7 (M18) reference: `docs/demo/m18/screenshot-brief.md`.*
*Demo prep standard: `docs/process/demo-preparation-standard.md`.*
*ADR references: ADR-021 (Constraint Search, Form 3), ADR-007 (CI Bands, Bayesian posterior),*
*ADR-017 (Zone 1D delta annotations), ADR-019 (ControlPlaneColumn, Mode 3).*
*Governing rulings: UX-RULING-4, NARRATION-RULING-1 (`docs/ux/standards.md §5`, `§16`).*
