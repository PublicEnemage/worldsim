# Screenshot Brief — M16 Demo 6 (v0.16.0)

> Generated: 2026-06-24. Produced by UX Designer Agent for G8 sprint (#1225 / Demo 6 preparation).
> Five frames specified for the M16 stakeholder demo: Senegal 2024, Article IV consultation,
> distributional human cost argument. Single entity. No Mode 3.
> Sprint entry: `docs/process/sprint-plans/m16-g8-sprint-entry.md` (EL Approved 2026-06-24).
>
> **Architecture changes from M14 Demo 5:**
> - **Zone 1A Phase 4 composite encoding (#845):** Primary trajectory now shows multi-curve
>   composite encoding. The distributional signal and four-framework trajectories are encoded
>   into the primary Zone 1A visualization. L0 composite labels visible on curve endpoints.
> - **Zone 1D delta annotations (#1147):** Step-over-step PSP change direction is annotated
>   inline — "↓ −0.04 vs prev step" visible at L0. No hover required for direction signal.
> - **Zone 1B cohort disaggregation (#986):** The `CohortImpactSection` is a flex sibling
>   of the MDA alert panel. Bottom-quintile threshold crossings show by cohort — indicator
>   name, current value, recovery floor, T3 tier badge with "Inferred" sublabel.
> - **Zone 1D political risk summary (#987):** Structured PSP severity display — CRITICAL/
>   WARNING/WATCH/STABLE with plain-language interpretation ("programme implementation
>   faces political execution risk"). Visible without drawer navigation.
> - **25-year human capital trajectory (#274):** `HumanCapitalTrajectoryPanel` visible in
>   primary viewport below Zone 1 instruments. Three cohort curves (Q1 informal, Q1
>   agriculture, Q2 informal) over 100 quarterly steps. Layer 3 milestone sentence at L0.
> - **Single entity (SEN only):** Article IV consultation context. No Mode 3.

---

## Thesis Frame

**Frame A — "This Cohort, at This Step"** (Step 2, Q2 2024)

The single image that most completely communicates the Demo 6 argument: Zone 1B's
`CohortImpactSection` shows the bottom quintile informal workers (`SEN:CHT:1-25-54-INFORMAL`)
poverty headcount at or above the recovery floor (0.40) at step 2 — six months into the
proposed conditionality programme. This is not aggregate GDP declining. This is a specific
population group — bottom quintile informal sector workers — crossing the threshold at which
capability restoration takes a decade or more.

Simultaneously visible in the same frame:
- Zone 1A composite encoding — the trajectory that produced this outcome
- Zone 1D showing PSP WARNING severity — the political constraint running alongside

This frame communicates three things simultaneously:
1. The cost is distributional, not aggregate — a specific cohort is identified, not "the poor"
2. The threshold crossing happens at step 2 — not at programme end, but six months in
3. The cohort signal and the financial trajectory share the same instrument surface —
   the ministry team does not need to open a separate panel to make the distributional argument

---

## Five Frames

### Frame A — "This Cohort, at This Step" ← THESIS FRAME (Step 2, Q2 2024)

**What Zone 1 shows:** SEN at step 2. Zone 1B `CohortImpactSection` shows the bottom quintile
informal worker poverty headcount at or crossing the 0.40 recovery floor. T3 Inferred badge
visible adjacent to the cohort row. Zone 1A composite encoding shows four-framework trajectory
curves diverging as conditionality begins. Zone 1D shows PSP severity label (WARNING or CRITICAL
depending on configured legitimacy_index) with delta annotation.

**Zone 1 requirements:**
- **1B (Cohort Impact Section — primary focus):** The cohort row for `bottom quintile, informal
  workers` must be visible with: (a) indicator plain name ("bottom quintile informal workers
  poverty headcount"), (b) current value at or above 0.40, (c) recovery floor value (0.40),
  (d) T3 badge with "Inferred" sublabel visible at 1440×900. This is the compositional center.
  The MDA alert section and cohort section are visible as flex siblings.
- **1A (Composite encoding):** Four-framework encoding curves visible. L0 composite labels
  readable on curve endpoints. Step 2 position marked. No choropleth in the argument —
  instruments carry the claim.
- **1D (Political risk):** PSP severity label visible ("WARNING" or "WATCH"). Delta annotation
  showing direction (↓ or →). Plain-language interpretation sentence legible.
- **1C (PMM Widget):** PMM value at step 2.

**This frame must show two things simultaneously without overlap or truncation:**
1. The cohort threshold crossing in Zone 1B (the "who bears the cost" argument)
2. The political risk label in Zone 1D (the "and the government can't protect them" constraint)

**Caption:** Senegal, Q2 2024. Step 2 — six months into the proposed Article IV
conditionality. Zone 1B shows bottom quintile informal workers crossing the poverty recovery
floor. T3 — Inferred. The demographic weights derive from ECOWAS comparable economy
distributions. The precision of who bears the cost is visible. Not aggregate. Not a trend.
This cohort, at this step.

**UI state:** SEN scenario active. Step 2 complete. Cohort impact section populated.
No drawer open. All Zone 1 instruments rendered. Viewport: 1440×900.

---

### Frame B — "The Composite Encoding — Four Trajectories at Once" (Step 4, Q4 2024)

**What Zone 1 shows:** SEN at step 4. Zone 1A composite encoding showing four-framework
trajectory curves — financial, human development, ecological, governance — as a multi-curve
composite. The human development curve is declining; the governance curve is holding or
declining. The encoding makes cross-framework comparison readable at a glance — the
distributional signal is not isolated in a drawer but encoded into the primary trajectory view.

**Zone 1 requirements:**
- **1A (Composite encoding — primary focus):** Four distinguishable curves visible. L0 labels
  on curve endpoints readable at 1440×900 — "Financial", "Human Dev.", "Ecological",
  "Governance" (or their current display labels). Step 4 position marked on shared step axis.
  Y-axis labeled "Composite Score" (or equivalent). L0 confidence tier annotations visible on
  at least one curve.
- **1B:** Cohort impact section visible — cohort rows may or may not show threshold status
  at step 4 depending on trajectory; persistence of the cohort section as a visible surface
  is required.
- **1D:** Zone 1D delta annotation visible on PSP row — direction indicator.
- **1C:** PMM showing pressure state at step 4.

**Caption:** Step 4 (Q4 2024): four frameworks in one encoding. Human development declining.
Financial composite compressed by conditionality. The trajectory view shows what is happening
across all measurement frameworks simultaneously — not one chart per framework.

**UI state:** Step 4 complete. Zone 1A composite encoding four-curve rendering. No drawer open.

---

### Frame C — "The Political Constraint — PSP Severity Labeled" (Step 4, Q4 2024)

**What Zone 1 shows:** SEN at step 4. Zone 1D political risk summary section showing PSP
severity label (WARNING or CRITICAL based on scenario legitimacy_index) with plain-language
interpretation and delta annotation. This is the G2 (#987) capability: the political
feasibility question is no longer a raw decimal — it is labeled in the severity vocabulary
the minister's team can use in a briefing note.

**Zone 1 requirements:**
- **1D (Political risk summary — primary focus):** The structured PSP display must be visible:
  (a) PSP severity label ("CRITICAL" / "WARNING" / "WATCH" / "STABLE") in distinct visual
  treatment, (b) plain-language interpretation sentence ("programme implementation faces
  political execution risk" or equivalent), (c) delta annotation showing direction and magnitude.
  This section must be legible at 1440×900 without any interaction.
- **1A:** Composite encoding visible — context for the PSP reading.
- **1B:** Cohort impact section visible as sibling — establishes the distributional cost
  alongside the political constraint.
- **1C:** PMM value.

**Compositional requirement:** Frame C pairs with Frame A — the political constraint frame
and the cohort cost frame are presented together to make the argument: "the conditionality
lands on this cohort AND the political system faces execution risk in delivering it."

**Caption:** Step 4 (Q4 2024): programme survival probability — WARNING. Zone 1D renders
the political constraint in plain language: the conditionality's political feasibility is not
assumed. It is quantified, labeled, and on screen. The finance ministry can state the
constraint without needing a political economist to translate it.

**UI state:** Step 4 complete. Zone 1D political risk summary visible. PSP severity labeled.
No drawer open. Viewport: 1440×900.

---

### Frame D — "For This Long — The 25-Year Trajectory" (step context varies — panel always visible)

**What Zone 1 shows:** The `HumanCapitalTrajectoryPanel` in the primary viewport below
Zone 1 instruments. Three cohort curves (Q1 informal, Q1 agriculture, Q2 informal) over
100 quarterly steps. The Layer 3 milestone sentence visible at L0: "by [year], bottom quintile
informal workers poverty headcount crosses the recovery floor — at this level, capability
restoration takes a decade or more." T3 Inferred badges on all three curves.

**Zone 1 requirements — primary focus is the projection panel:**
- **Projection panel (`human-capital-trajectory-panel`):** All three curve labels readable.
  Milestone sentence visible at L0 — the full sentence fits within the panel without truncation.
  Calendar year anchor is the leading element of the milestone sentence. T3 badges adjacent
  to curve endpoints readable at 1440×900. Panel header ("25-year projection · quarterly
  resolution") legible.
- **Zone 1A/1B/1C/1D:** All four instrument zones remain visible in the 1440×900 viewport
  above the projection panel — no displacement (AC-F6 confirmed). The panel's own step axis
  (100-step quarterly) is distinct from Zone 1A's programme-window step axis.

**Caption:** "By [year], bottom quintile informal workers poverty headcount crosses the
recovery floor — at this level, capability restoration takes a decade or more." The 25-year
projection answers the question the programme window cannot: not just what happens during
the programme, but what the conditionality commits this cohort to for the decade beyond.
The "for this long" argument. Visible at L0 from the primary viewport without drawer navigation.

**UI state:** SEN scenario with `projection_steps=100` active. Projection panel visible
below Zone 1 instruments. Step context: any step where Zone 1 instruments are rendered
(step 2 or step 4 sufficient). Capture after milestone sentence has loaded (wait for
`projection-milestone-sentence` to appear).

---

### Frame E — "All Arguments on One Screen" (Step 8, Q4 2025)

**What Zone 1 shows:** Full viewport at step 8 — the end of the programme window (8
quarterly steps = 2 years). Zone 1A composite encoding showing divergence from baseline
across eight steps. Zone 1B cohort impact section showing cumulative distributional state.
Zone 1D political risk summary at the programme window close — PSP trajectory across eight
steps. Projection panel below showing the full 25-year human capital arc, including the
milestone sentence.

The closing argument: all four Demo 6 capabilities visible simultaneously. The minister
does not need to open a drawer, navigate to a different panel, or ask a specialist to
assemble the complete picture. It is on one screen.

**Zone 1 requirements:**
- **1A:** Full eight-step composite encoding arc visible. Step 8 position marked.
- **1B:** Cohort impact section showing final programme-window state. Cumulative threshold
  status for Q1 informal workers visible.
- **1C:** PMM value at step 8.
- **1D:** PSP severity at step 8. Delta annotation showing direction over the programme window.
- **Projection panel:** 25-year arc visible. Milestone sentence visible at L0.
  All Zone 1 instruments NOT displaced by the panel.

**Caption:** Step 8 (Q4 2025): the programme window closes. Every Demo 6 argument is on
this screen simultaneously. Who bears the cost (Zone 1B cohort disaggregation). What is
changing (Zone 1A composite encoding). Whether the government can deliver the conditionality
(Zone 1D political risk). For how long the consequences persist (25-year trajectory panel
milestone sentence). No drawer navigation. No specialist mediation. One screen.

**UI state:** Step 8 complete. All Zone 1 instruments rendered. Projection panel visible.
All instruments non-displaced (viewport verification from AC-F6). Viewport: 1440×900.

---

## Presentation Sequence

| Order | Frame | Step | Why |
|---|---|---|---|
| 1 | A — "This Cohort, at This Step" | 2 (Q2 2024) | Lead with the thesis — the cohort threshold crossing at step 2 |
| 2 | B — "Composite Encoding" | 4 (Q4 2024) | Pull back to show what's driving the distributional outcome |
| 3 | C — "Political Constraint" | 4 (Q4 2024) | The PSP severity label alongside the cohort cost |
| 4 | D — "For This Long" | any | 25-year trajectory — the "for this long" argument |
| 5 | E — "All Arguments" | 8 (Q4 2025) | Close on the complete picture — all Demo 6 capabilities simultaneously |

Rationale: Lead with the distributional thesis (who bears the cost, at what step). Frame B
provides the composite encoding context. Frame C shows the political constraint that runs
alongside. Frame D answers "for how long" — the intergenerational argument. Frame E closes
by showing the minister's team everything they need on one screen at programme window close.

---

## Pre-Capture Requirements

| Requirement | Source | Must verify |
|---|---|---|
| SEN in `simulation_entities` and `source_registry` | G3 implementation (PR #1172) | `GET /api/v1/entities/SEN/data-quality?year=2024` returns 200 |
| Q1 cohort poverty headcount ≥ 0.40 at step 2 | EL design decision 2026-06-24 | Run demo-narrated.spec.ts; check Zone 1B cohort row at step 2; adjust initial `poverty_headcount_ratio` if crossing not achieved |
| Milestone sentence calendar year anchor leads | G10/#1177 (PR #1199) + EL 2026-06-24 | Confirm `projection-milestone-sentence` text begins with `"by [YYYY]"` — 4-digit year is primary element |
| Zone 1B cohort impact section visible | G2 implementation (PR #1173) | `CohortImpactSection` renders for SEN scenario at step 2 with T3 Inferred badge |
| Zone 1D political risk summary visible | G2 implementation (PR #1173) | PSP severity label ("WARNING" etc.) and plain-language sentence legible at 1440×900 |
| Zone 1D delta annotation visible | G1 implementation (PR #1160) | `psp-delta-annotation` or equivalent renders at L0 |
| Zone 1A composite encoding four-curve | G1 implementation (PR #1160) | Four curves visible in Zone 1A composite encoding at 1440×900 |
| Projection panel non-displacement | G3 AC-F6 (PR #1172 PASS) | Zone 1A/1B/1C/1D remain visible above projection panel at 1440×900 |
| Legibility spec passes | Step 5b gate | `demo-legibility.spec.ts` all pass at 1440×900 before screenshots captured |
| `demo-narrated.spec.ts` viewport set | Step 4 gate | `page.setViewportSize({ width: 1440, height: 900 })` present before `page.goto()` |

---

## Key Narration Notes

1. **Do not narrate the choropleth as the analytical instrument.** Per UX-RULING-4: "Watch
   Zone 1A as the composite encoding diverges across frameworks" — not "watch Senegal shift
   on the map." The choropleth anchors geography. The instruments carry the argument.

2. **The T3 Inferred badge is the challenge response.** When the creditor challenges the
   cohort distribution methodology, the analyst points to the T3 badge with "Inferred" sublabel
   and the confidence tier metadata: "Tier 3 — synthetic estimate from ECOWAS comparable
   economy distributions. This is declared, labeled, and on screen. The demographic weighting
   is in the published methodology." Frame the badge as precision about uncertainty, not a
   weakness.

3. **Step 2 threshold crossing is the distributional thesis.** The argument is not that
   poverty gets worse over time — it is that the threshold crossing happens at step 2, six
   months in. The timeline specificity is what makes this citeable at the table: "Under the
   proposed programme terms, this cohort crosses the recovery floor by Q2 2024."

4. **The milestone sentence is the "for this long" argument.** Narrate it directly:
   "The instrument tells us: by [year], bottom quintile informal workers poverty headcount
   crosses the recovery floor. Capability restoration takes a decade or more. The programme
   lasts 2 years. The consequence lasts ten. That is the argument the ministry team could
   not make before Demo 6."

5. **PSP severity is a political feasibility constraint, not a political prediction.**
   "The political risk summary is not a forecast of whether the government survives. It is
   the model's assessment of whether the programme's conditionality terms are deliverable
   given the political economy of the country at this step. That is a different question —
   and it now has a labeled, plain-language answer in Zone 1D."

6. **No Mode 3 in Demo 6.** If asked: "The counter-proposal capability — testing what the
   trajectory looks like under alternative conditionality terms — is available. M17 combines
   Mode 3 Active Control with distributional constraints: you can not just test an alternative
   path, you can specify that the alternative must protect a particular cohort. That is the
   M17 argument. Demo 6 is the distributional visibility argument — the prerequisite for
   that capability to be meaningful."

---

*Brief authored by UX Designer Agent, 2026-06-24. Sprint entry: `docs/process/sprint-plans/m16-g8-sprint-entry.md`. Demo prep standard: `docs/process/demo-preparation-standard.md §Step 2`.*
