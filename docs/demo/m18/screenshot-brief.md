# M18 Screenshot Brief — UX Designer Agent

> Generated: 2026-06-28. Produced by UX Designer Agent (PM Agent in same session,
> same-session authorship disclosed) for #1445 / Demo 7 preparation.
>
> Five frames specified for the M18 stakeholder demo: two-act structure.
> Act 1 — Senegal 2024, Mode 3 active control (ControlPlaneColumn Form 1 + Zone 1A branch).
> Act 2 — Zambia debt restructuring, three-scenario distributional comparison
> (DistributionalComparisonSummary Zone 1B sticky-bottom).
>
> **Step 5d dependency:** Frame A step number and FiscalMultiplier value are
> TBD — to be confirmed by the two-agent panel (Development Economist + Chief
> Methodologist) per `docs/demo/m18/reviews/scenario-evaluation-mode3-deliberation.md`.
> All other frame specifications are final.
>
> **Architecture changes from M16 Demo 6:**
> - **Two-act demo:** Act 1 Senegal (Mode 3 active control) + Act 2 Zambia
>   (three-scenario comparison). Prior demos were single-entity single-act.
> - **ControlPlaneColumn (ADR-019, G4):** A column-mounted control plane occupies
>   the right layout zone in Mode 3. Form 1 (FiscalMultiplier slider + LegitimacyConstraint)
>   and Form 2 (7 shock types) are mounted in the column — no bottom-bar, no scroll.
>   When Form 1 is applied, Zone 1A shows baseline + branch trajectories simultaneously.
>   Mode 2 shows Mode2ColumnSurface (scenario identity + "Enter Active Control" button).
> - **CI bands on Zone 1A (G1):** All composite trajectory lines carry semi-transparent
>   confidence ribbons. Width = step half-width schedule × data tier multiplier. In Mode 3:
>   opacity 5% (reduced to avoid obscuring baseline/branch split). In Mode 1/2: opacity 12%.
> - **PSP driver label in Zone 1D (G2):** `psp-driver-row` shows dominant causal driver
>   ("Driver: fiscal sustainability" / "Driver: governance" / "Driver: external balance" /
>   "Driver: social stability") beneath the PSP severity badge at every step.
> - **DistributionalComparisonSummary in Zone 1B (G3):** Sticky-bottom element visible
>   when ≥2 scenarios loaded for the same entity. Shows poverty headcount differential,
>   CI band, tier badge, direction stability statement.
> - **Zone 3 auditability panel (G5):** Expand/collapse methodology panel on
>   DistributionalComparisonSummary — visible in Zone 1B without drawer navigation.
> - **No choropleth narration (UX-RULING-4):** The choropleth is geographic context.
>   All five frames show instruments (Zone 1A/1B/1C/1D + control column) as the primary
>   surface. Do not narrate quantitative change from the choropleth.

---

## Thesis Frame

**Frame A — "The Instrument" (Act 1, Senegal Mode 3, Form 1 Applied)**

The single image that most completely communicates the Demo 7 argument: Mode 3 active,
`ControlPlaneColumn` visible on the right, FiscalMultiplier slider set to the Step 5d-
recommended value. Zone 1A showing two simultaneous trajectory sets — the baseline (original
programme terms) and the counter-trajectory branch — both visible without scrolling at
1280×800 or 1440×900. CI bands present on both sets at Mode 3 reduced opacity (5%).

This frame communicates the Demo 7 thesis in one image: the finance ministry's analyst can
adjust the multiplier and see the consequence in Zone 1A before finishing the explanation.
The counter-proposal is not a document — it is a live trajectory branch visible at the same
time as the control input.

---

## Five Frames

### Frame A — "The Instrument" ← THESIS FRAME (Act 1, Senegal, Mode 3, Step TBD)

**What Zone 1 + control column shows:** Senegal at the step identified by the Step 5d panel
as showing maximum baseline/branch divergence (expected: step 3–4). Mode 3 active.
`ControlPlaneColumn` visible on the right side of the viewport. Form 1 visible: FiscalMultiplier
slider at the Step 5d-recommended value; branch_from_step selector visible; `apply-policy-input`
button (applied). Zone 1A: two trajectory sets — baseline (all frameworks, lighter weight or
labeled "Baseline") and counter-trajectory branch (bolder or labeled with the branch step).
CI bands visible on both sets at 5% opacity (Mode 3 reduced). Zone 1B: CohortImpactSection
visible alongside MDA alert panel. Zone 1D: PSP severity badge + `psp-driver-row` readable.

**Zone 1 requirements:**
- **1A (Trajectory View + CI bands):** Two complete trajectory sets (baseline + branch) visible
  without overlap confusion. CI ribbons present — semi-transparent fills around each curve.
  The branch anchor step visible (labeled or line annotation). Y-axis auto-scaled to show both
  sets without clipping. Step axis labeled; current step annotation visible.
- **1B (MDA Alert + CohortImpactSection):** Cohort row for bottom quintile informal workers
  visible — indicator name, current value, 0.40 recovery floor. MDA alert panel present.
  `DistributionalComparisonSummary` sticky-bottom NOT present (Act 1 is single-scenario;
  Act 2 loads the comparison).
- **1C (PMM Widget):** PMM value rendered; not empty.
- **1D (Four-Framework + PSP + driver):** PSP severity badge (WARNING or WATCH expected at
  mid-programme step). `psp-driver-row` visible: "Driver: fiscal sustainability" or whichever
  driver is dominant at this step per the Step 5d run. Both items readable at 1440×900.
- **ControlPlaneColumn:** Form 1 visible — FiscalMultiplier slider with current value labeled;
  `apply-policy-input` button; branch anchor label confirming the branch step. Form 2 shock
  types below (may be collapsed or partially visible; Form 1 must dominate the visible area).

**Zone 2 (choropleth):** SEN visible and highlighted. Geographic context only — not analytical
instrument per UX-RULING-4. May be partially visible at the left; does not need to be the
compositional focus.

**Caption:** Senegal, Mode 3 active. FiscalMultiplier: [Step 5d value]. Zone 1A shows the
baseline trajectory and the counter-trajectory branch simultaneously. CI bands on both — no
scroll required to hold the control input and its consequence in the same view.

**UI state:** Mode 3 active. Form 1 applied (branch exists). Both trajectories visible in
Zone 1A at the same time. Control column visible at right. No drawer open.

**Step 5d gate:** Confirm step number and FiscalMultiplier value from the deliberation file
before capture. Caption "[Step 5d value]" is a placeholder.

---

### Frame B — "The Uncertainty Envelope" (Act 1, Senegal, Mode 3, Step 3)

**What Zone 1 + control column shows:** Senegal at step 3 in Mode 3. Zone 1A CI bands visible
— the semi-transparent ribbons around each framework's composite trajectory line. The Human
Development curve (T3 data at T3 tier multiplier 1.5×) carries the widest band. Zone 1D shows
PSP severity badge + `psp-driver-row` ("Driver: [dominant driver at step 3]"). ControlPlaneColumn
still visible with Form 1 state persisted (FiscalMultiplier unchanged from Frame A).

**Zone 1 requirements:**
- **1A (CI bands focus):** CI ribbons must be photographically distinguishable from the
  trajectory lines — semi-transparent fill clearly present, not invisible (opacity 5% minimum
  must be rendering above the background). The width difference between frameworks (wider for
  T3 data, narrower for T1) should be visible if multiple frameworks render at different tiers.
  Both baseline and branch trajectory sets present (Mode 3 active). The bands on each set
  should be visible.
- **1D (PSP driver):** This is Frame B's secondary focus. The `psp-driver-row` must be readable
  at capture resolution (1440×900) — font size and truncation must allow reading "Driver:
  fiscal sustainability" or whichever driver is live. The PSP severity badge must be legible.
- **1B:** Cohort section still visible; no comparison summary (single-scenario Act 1).
- **1C:** PMM value present.
- **ControlPlaneColumn:** Form 1 state unchanged from Frame A. Must be simultaneously visible.

**Caption:** Step 3, Q3 2024. Zone 1A carries confidence ribbons — the uncertainty envelope
is calibrated to the data tier, not decorative. Zone 1D names the dominant driver: [driver at
step 3]. The political advisor can cite both the risk level and the source of the risk.

**UI state:** Mode 3 active. Same Form 1 state as Frame A. Step 3 active.

---

### Frame C — "The Act 1 Finding" (Act 1, Senegal, Mode 3, Step 6)

**What Zone 1 shows:** Senegal at step 6 (two years in). Mode 3 active or Mode 3 analysis
result being shown. Zone 1B CohortImpactSection front and center: bottom quintile informal
workers poverty headcount row — current value vs. 0.40 recovery floor. The finding is whatever
the simulation shows at the Step 5d-recommended configuration; both outcomes are valid.
Zone 1A showing trajectory at step 6. ControlPlaneColumn may still be visible.

**Zone 1 requirements:**
- **1B (CohortImpactSection — primary focus):** The bottom quintile informal worker row must
  be the compositional focus of this frame. Requirements: (a) indicator name readable ("Bottom
  quintile informal workers poverty headcount" or equivalent display label — NOT the raw DB
  field name); (b) current value at step 6 readable; (c) recovery floor 0.40 readable;
  (d) T3 tier badge visible; (e) whether the value is above or below 0.40 must be
  unambiguous — this is the Act 1 finding. If the value is above 0.40 (threshold avoided),
  the green/safe state should be visible if the component uses color coding. If at or below
  0.40 (threshold crossed), the alert state should be visible.
- **1A:** Zone 1A trajectory at step 6 visible — showing both baseline and branch arc over
  the full 6-step programme window (or however many steps are visible).
- **1D:** PSP severity at step 6 visible alongside driver label.
- **1C:** PMM at step 6.

**Caption — two versions depending on Step 5d outcome:**
- *If avoided:* Step 6, Q2 2026. Bottom quintile poverty headcount at [value] — above the
  0.40 recovery floor. At FiscalMultiplier [value], the threshold is not crossed. This is
  the ministry's Act 1 finding.
- *If crossed:* Step 6, Q2 2026. Bottom quintile poverty headcount at [value] — the 0.40
  recovery floor is crossed regardless of FiscalMultiplier configuration tested. The
  threshold crossing is structural to the programme design, not a multiplier assumption.

**UI state:** Step 6 complete. Zone 1B CohortImpactSection prominent. Mode 3 active (or
result visible). ControlPlaneColumn present if layout permits without obscuring Zone 1B.

---

### Frame D — "The Counter-Proposal as a Number" (Act 2, Zambia, Terminal Step)

**What Zone 1 shows:** Act 2. Zambia. Three scenarios loaded: Option A (EFF Front-Loaded),
Option B (EFF Gradual), Option C (Homegrown Programme, reference). Zone 1A showing three
composite trajectory curves with CI bands (Mode 1 or Mode 2, full opacity 12%). Zone 1B
sticky-bottom: `DistributionalComparisonSummary` visible — the primary content of this frame.

**Zone 1 requirements:**
- **1B sticky-bottom (DistributionalComparisonSummary — primary focus):** The comparison
  summary must be clearly readable at 1440×900. Requirements: (a) differential number
  readable — "+340,000 persons below poverty threshold" (or current simulation output — do
  not manually set this value; capture what the simulation shows); (b) CI band bounds readable
  — "295K – 395K" format; (c) confidence marker readable — "95% CI"; (d) tier badge readable —
  "T3"; (e) direction stability text readable — "Direction stable"; (f) reference scenario
  label visible ("vs. Option C" or "Option C (Reference)"); (g) the `psp-driver-row` or any
  Zone 1D content does not obscure Zone 1B.
  The Zone 3 auditability panel must be **collapsed** in this frame — Frame E shows it expanded.
- **1A (three-scenario trajectories + CI bands):** All three scenario curves visible —
  distinguishable by color or label. CI bands at full opacity (Mode 1/2, 12%). Option A,
  Option B, Option C trajectories readable as distinct. The trajectory divergence between
  Option A and Option C visible (this is the visual counterpart to the 340,000 number).
- **1D:** PSP driver visible for the active entity at the terminal step.
- **1C:** PMM present.

**Zone 2:** ZMB visible on choropleth — geographic context only.

**Caption:** Zambia, programme end. Three scenarios: Option A (IMF Front-Loaded), Option B
(Gradual), Option C (Ministry counter-proposal). Zone 1B reads: "+340,000 persons below
poverty threshold · 295K–395K · T3 · Direction stable." The counter-proposal is a number,
not an assertion.

**UI state:** Three scenarios loaded. Terminal step (step 8 per programme window configuration).
DistributionalComparisonSummary visible and collapsed. No drawer open. Mode 1 or 2 (not
Mode 3 — Act 2 is comparison, not active control).

---

### Frame E — "The Analytical Defence" (Act 2, Zambia, Terminal Step, Zone 3 Expanded)

**What Zone 1 shows:** Same Zambia state as Frame D — terminal step, three scenarios, Zone 1A
trajectories with CI bands. Zone 1B: `DistributionalComparisonSummary` visible with Zone 3
auditability panel **expanded** below it. The expanded panel shows the methodology narrative:
computation approach, reference scenario label, CI methodology note (BandingEngine, step-based
half-width, tier multiplier), confidence tier declaration.

**Zone 1 requirements:**
- **1B (DistributionalComparisonSummary + Zone 3 expanded — primary focus):** The expanded
  Zone 3 panel must be visible in the screenshot without requiring scroll. Requirements:
  (a) the comparison summary (**above** the expanded panel) still readable — number, bounds,
  tier, direction must be visible in the collapsed header or the summary row;
  (b) the methodology panel expanded below it — BandingEngine note, half-width schedule
  reference, tier multiplier value, direction-stability condition text must be readable;
  (c) the expand/collapse affordance visible (so the audience can see it is interactive).
  If the full expanded panel requires scroll to show, capture the top portion — the
  BandingEngine CI methodology note is the most important text to have in frame.
- **1A:** Three-scenario trajectories with CI bands still visible above Zone 1B.
  Trajectory context is important — the expanded panel should not completely occlude Zone 1A.
- **1D + 1C:** Present; not the compositional focus of this frame.

**Caption:** Zone 3 expanded — the methodology behind the 340,000 figure, visible in Zone 1B
without drawer navigation. The BandingEngine note shows the CI derivation. Persona 1 (Lucas)
can defend the methodology under IMF scrutiny from the primary viewport.

**UI state:** Zone 3 methodology panel expanded (via user click or Playwright click action
during capture). DistributionalComparisonSummary summary row still visible. Zone 1A trajectory
context visible above.

---

## Presentation Sequence

| Order | Frame | Act | Step | Why |
|---|---|---|---|---|
| 1 — THESIS | A — The Instrument | Act 1 (SEN) | TBD (Step 5d) | Lead with the capability claim — the counter-proposal instrument live |
| 2 | B — The Uncertainty Envelope | Act 1 (SEN) | 3 | CI bands + PSP driver — epistemic transparency layer |
| 3 | C — The Act 1 Finding | Act 1 (SEN) | 6 | The question answered — either outcome is the argument |
| 4 | D — The Counter-Proposal | Act 2 (ZMB) | Terminal | 340,000 — the number that must be engaged with |
| 5 | E — The Analytical Defence | Act 2 (ZMB) | Terminal | Zone 3 expanded — the methodology visible under scrutiny |

**Rationale:** Lead with the Act 1 active-control thesis (A) — it establishes Demo 7's
primary capability claim (agency, not just visibility) before the uncertainty envelope
(B) and conclusion (C). Act 2 frames D and E follow in argument order: the number first,
the defence posture second. The presentation flows: instrument → epistemic grounding →
finding → quantified counter-proposal → analytical defence.

---

## Pre-Capture Requirements

| Requirement | Source | Must verify |
|---|---|---|
| SEN scenario loaded at 100 steps, programme window = 8 | G4 backend scenario fixture | `GET /api/v1/scenarios/{id}` returns `step_count: 100` |
| Mode 3 entry via "Enter Active Control" button | G4 frontend (ADR-019) | `data-testid="enter-active-control"` present and clickable |
| ControlPlaneColumn Form 1 visible in Mode 3 | G4 frontend | `data-testid="policy-input-type-selector"` and `data-testid="apply-policy-input"` visible |
| Zone 1A shows both baseline and branch in Mode 3 | G4 frontend | Two trajectory sets visible simultaneously after `apply-policy-input` click |
| CI bands render at Mode 3 opacity (0.05) | G1 frontend (TrajectoryView.tsx) | Semi-transparent fills visible; `CI_BAND_OPACITY_MODE3 = 0.05` |
| CI bands render at standard opacity (0.12) in Mode 1/2 | G1 frontend | Frame B and frames D/E have visually wider bands than Frame A |
| `psp-driver-row` visible in Zone 1D | G2 frontend (FourFrameworkZone1D.tsx) | "Driver: [category]" readable at 1440×900 |
| ZMB three scenarios loaded simultaneously | G3 demo fixture | Three scenario IDs registered; `comparisonScenarios.length === 3` |
| DistributionalComparisonSummary renders at terminal step | G3 frontend | `data-testid="distributional-comparison-summary"` visible and non-empty |
| Zone 3 auditability panel collapses/expands | G5 frontend | Panel collapsed for Frame D; panel open for Frame E |
| Zone 1B sticky-bottom does not obscure Zone 1A | G3 CSS (overflow + sticky) | Zone 1A still partially visible with DistributionalComparisonSummary sticky |
| Viewport set to 1440×900 in `demo-narrated.spec.ts` | Pre-capture gate (Step 6) | `page.setViewportSize({ width: 1440, height: 900 })` before first `page.goto()` |
| Legibility gate passes at 1440×900 | Step 5b (PASS — 2026-06-28) | ✅ Confirmed 16/16 tests pass |
| Step 5d Mode 3 configuration confirmed | Step 5d panel | Frame A step + FiscalMultiplier value from deliberation file |

---

## Key Narration Notes

1. **UX-RULING-4: No choropleth narration for quantitative change.** Say "Zone 1A shows
   the trajectory split" — not "watch Senegal shift on the map." The choropleth anchors
   geography. The instruments carry the argument.

2. **Both Act 1 outcomes are narratively equal.** If the threshold is avoided under the
   tested multiplier, the finding is "here is the configuration that avoids it." If the
   threshold is crossed regardless, the finding is "the crossing is structural to the
   programme design, not a multiplier assumption." Frame C caption has two versions — use
   whichever the simulation shows. Do not pre-declare the outcome in this brief.

3. **Frame A FiscalMultiplier value is Step 5d gated.** The caption placeholder "[Step 5d
   value]" must be filled from `docs/demo/m18/reviews/scenario-evaluation-mode3-
   recommendation.md` before screenshots are finalized. Do not use an estimated value.

4. **Frame D comparison summary values are simulation output.** The "+340,000 persons" and
   "295K–395K" figures in this brief are the expected output from G3 sprint exit validation.
   Capture what the live simulation shows — if the values differ, use the actual output and
   update the walkthrough caption for Section 2 Step 4.

5. **Zone 3 expanded panel (Frame E):** The expand action is a user interaction (click on
   the methodology toggle). In the Playwright spec, this requires a `page.click()` on the
   expand affordance before screenshot capture. The `data-testid` for the expand toggle
   should be confirmed from `frontend/src/components/DistributionalComparisonSummary.tsx`
   before authoring the spec step.

---

*Screenshot brief authored by UX Designer Agent (PM Agent, same session, disclosed),
2026-06-28. Demo prep issue: #1445. Walkthrough: `docs/demo/m18/stakeholder-walkthrough.md`.*
*Demo prep standard: `docs/process/demo-preparation-standard.md`.*
*Step 5d dependency: `docs/demo/m18/reviews/scenario-evaluation-mode3-deliberation.md` (pending).*
