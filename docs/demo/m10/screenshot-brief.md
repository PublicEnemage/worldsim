# M10 Screenshot Brief — UX Designer Agent

> Generated: 2026-06-02. Produced by UX Designer Agent for Issue #634 / M10 Demo 3 preparation.
> Five frames specified for the M10 stakeholder demo: Argentina 2001–2004, four live radar axes.
>
> **Architecture change from M8:** Zone 1A (Trajectory View) is now the primary analytical
> surface. The choropleth (Zone 2A) is geographic context only (UX-RULING-4). Frame
> specifications target the Zone 1 instrument cluster, not the drawer or the choropleth.

## Thesis Frame

**Frame C — "The Divergence" (Step 3, 2003)**

The single image that most completely communicates the WorldSim argument if only one
screenshot is shared. Zone 1A shows the financial trajectory curve rising as the Kirchner
recovery begins; the governance curve remains flat in the breach zone. Zone 1D shows
ecological and governance composite scores live; Zone 1B shows the governance WARNING
alert still active despite the financial rebound. The argument — institutional recovery
lags financial recovery, sometimes by years — requires no caption.

For Demo 3, this frame also demonstrates two M10 claims simultaneously:
1. GovernanceModule is live (not dashed, not null) — governance is a real analytical axis.
2. Platform Principle — the same engine, instruments, and UX that ran Greece now runs
   Argentina. Same workflow, different crisis arc.

---

## Five Frames

### Frame A — "The Instrument" (Step 1, 2001)

**What Zone 1 shows:** All four Zone 1 instruments fully loaded with Argentina data at
programme entry. Zone 1A trajectory starts with the initial seed values; step label
"Zero Deficit Plan / Blindaje" visible on the step axis. Zone 1D shows the ecological
(1.07 — 7% beyond the CO2 planetary boundary) and governance (0.71) composite scores.
Zone 1B: no MDA alerts yet at step 1. Zone 1C: PMM computed for the baseline.

**Zone 1 requirements:**
- 1A (Trajectory View): Argentina visible at step 1 anchor. Step annotation "Zero Deficit
  Plan / Blindaje" readable on the step axis. Four curves laid out (two dashed Path A for
  financial/HD, two solid for ecological/governance).
- 1B (MDA Alert Panel): "No active threshold breaches" or minimal alerts — baseline state.
- 1C (PMM Widget): Computed value visible (not "—" or loading).
- 1D (Four-Framework): Ecological score (~1.07) and governance score (~0.71) visible with
  values. Financial and HD showing null treatment (per DD-011). Ecological "(1.0 = boundary)"
  annotation visible (IR-M10-002 fix required before capture).

**Zone 2:** Default framework tab. No change required. Choropleth shows Argentina
colored with the seed attribute — geographic context, not analytical instrument.
**Zone 3:** Collapsed.

**Caption:** Argentina at programme entry (2001): Zone 1 instruments loaded with
crisis-arc initial state. Ecological boundary already exceeded at 1.07.

**UI state:** ARG scenario active. Step 1 complete. No EntityDetailDrawer open.
All Zone 1 instruments visible in the primary viewport. Capture after 400ms for
Zone 1A animation to settle.

---

### Frame B — "The Crisis" (Step 2, 2002)

**What Zone 1 shows:** Zone 1A trajectory curves drop at step 2 — the default/devaluation
inflection point. Step annotation "Default / Peso devaluation" prominent. Zone 1B shows
MDA alerts accumulating (financial or reserve threshold breaches). Zone 1C PMM shows a
compressed margin at the default step. Zone 1D governance score reflects early deterioration.

**Zone 1 requirements:**
- 1A (Trajectory View): Step 2 inflection clearly visible. "Default / Peso devaluation"
  step label legible on the step axis. The curve drop from step 1 → step 2 should be
  the dominant visual signal.
- 1B (MDA Alert Panel): At least one alert visible. Severity badge and step index readable.
- 1C (PMM Widget): Directionally meaningful value (not same as step 1).
- 1D (Four-Framework): Governance score starting to decline. Ecological score ticking up
  slightly (CO2 accumulation).

**Zone 2:** Default. Choropleth shows ARG colored — geographic context only.
**Zone 3:** Collapsed.

**Caption:** Step 2 (2002): sovereign default and peso devaluation — the sharpest inflection
in the Argentina arc. All Zone 1 instruments respond simultaneously.

**UI state:** ARG scenario active. Step 2 complete. No EntityDetailDrawer open.

---

### Frame C — "The Divergence" ← THESIS FRAME (Step 3, 2003)

**What Zone 1 shows:** Zone 1A asymmetric curve posture — the financial curve (dashed,
Path A: gdp_growth) rising from the step 2 trough (Kirchner recovery begins), while the
governance curve (solid) remains at or below the breach floor. The two curves are visibly
out of phase. Zone 1B: governance WARNING alert fires here (democratic_quality_score = 0.665,
below MDA-GOV-DEMOCRACY-FLOOR of 0.70). Zone 1D: governance composite score still below
0.70 despite financial trajectory improving. The divergence is readable in three separate
Zone 1 instruments simultaneously — this is the primary demo surface.

**Zone 1 requirements:**
- 1A (Trajectory View): Financial curve rising from step 2 nadir. Governance curve flat/
  declining. Step annotation "Kirchner recovery begins" legible. The visual divergence
  between the two out-of-phase curves must be the dominant compositional element.
- 1B (MDA Alert Panel): Governance WARNING alert visible with full detail — severity badge
  (WARNING), indicator name ("democratic_quality_score"), step index (3), framework label
  ("governance"). Alert must be the first visible item in the panel.
- 1C (PMM Widget): Recovery direction signal visible — PMM should show improved margin
  vs step 2 (fiscal pressure easing).
- 1D (Four-Framework): Governance score (0.665) visibly below ecological score (1.07+).
  Ecological "(1.0 = boundary)" annotation visible. Financial and HD null treatment
  consistent with DD-011.

**Zone 2:** Not compositional focus. Choropleth visible as geographic context.
**Zone 3:** Collapsed.

**Caption:** Step 3 (2003 — Kirchner recovery): GDP trajectory rising while governance
composite remains below the MDA floor. Financial recovery and institutional recovery are
not the same event.

**UI state:** ARG scenario active. Step 3 complete. No EntityDetailDrawer open. All Zone 1
instruments visible in the primary viewport. Capture after 400ms for Zone 1A animation.

---

### Frame D — "The Evidence" (Step 3, MDA alert panel)

**What Zone 1 shows:** Zone 1B (MDA Alert Panel) is the compositional focus — captures
that the governance finding is structured, citeable evidence. The governance WARNING card
fully readable without scrolling.

**Zone 1 requirements:**
- 1B (MDA Alert Panel): Full governance WARNING card readable — severity badge, indicator
  name, step index ("Step 3"), consecutive breach count ("1 consecutive step(s)"), framework
  label. This is the "evidence sentence" a negotiator could read aloud across a table.
- 1A (Trajectory View): Visible in background, not the primary focus. Same step 3 state
  as Frame C.
- 1C, 1D: Visible but not primary focus.

**Zone 2:** Visible. Choropleth as geographic context.
**Zone 3:** Collapsed.

**Caption:** Each governance threshold breach is rendered as structured evidence —
indicator, severity, step, framework — specific enough to cite in a negotiation.

**UI state:** Same as Frame C. Zone 1B scroll at top so WARNING card is fully visible.

---

### Frame E — "Recovery Without Restoration" (Step 4, 2004)

**What Zone 1 shows:** Zone 1D at the growth consolidation step — Kirchner recovery is
entrenched, GDP growing strongly (+9%), but governance composite remains below threshold
(or marginally above — recovery is slow). Ecological score has ticked upward (CO2
accumulation continues). The Zone 1D four-framework display shows two live scores and two
honest nulls — this is the full M10 instrument claim: four frameworks measured, two
composites live, two deferred pending multi-entity comparison (#193).

This frame closes on the Platform Principle argument: the same Zone 1 instrument cluster
that ran Greece now shows Argentina at year 4 of the crisis arc. Different country, same
analytical discipline, same UX.

**Zone 1 requirements:**
- 1D (Four-Framework): All four framework rows visible. Ecological and governance scores
  with their step-4 values. Financial and HD null treatment (DD-011 — dash or "—", not
  zero). "(1.0 = boundary)" annotation on ecological row visible.
- 1A (Trajectory View): Step 4 anchor visible — the trajectory arc through all four steps
  visible together. The financial/HD dashed curves vs ecological/governance solid curves
  distinction readable.
- 1B (MDA Alert Panel): Whether governance WARNING persists at step 4 or clears — either
  is analytically honest. If it clears, the narration notes that institutional recovery
  takes longer than one year. If it persists, the narration notes the continuing breach.
- 1C (PMM Widget): Expansion direction — recovery step should show wider PMM margin.

**Zone 2:** Not compositional focus.
**Zone 3:** Collapsed.

**Caption:** Step 4 (2004 — growth consolidation): GDP trajectory recovering strongly.
Governance composite healing slowly. Platform Principle — same engine as Greece,
same analytical discipline, different crisis arc.

**UI state:** ARG scenario active. Step 4 complete (all steps run). No EntityDetailDrawer
open. Zone 1D fully rendered.

---

## Presentation Sequence

| Order | Frame | Step | Why |
|---|---|---|---|
| 1 | C — The Divergence | 3 | Lead with the argument — governance WARNING during recovery is the thesis |
| 2 | A — The Instrument | 1 | Pull back to programme entry — show the before-picture |
| 3 | B — The Crisis | 2 | Show the inflection that produced the divergence |
| 4 | D — The Evidence | 3 | Show what the specialist can cite — the alert is structured evidence |
| 5 | E — Recovery Without Restoration | 4 | Close on Platform Principle — same engine, full arc visible |

Rationale: Lead with the thesis frame. The audience understands why the tool matters before
they understand how it works. Frame E closes on capability, not crisis — leave the audience
with an image of what "analytical standing in a negotiation" looks like in practice.

---

## Pre-Capture Requirements

The following fixes must be implemented before screenshots are captured (Step 6 of Issue #634).
Screens captured before these fixes may not match the spec.

| Requirement | Issue | Component | Status |
|---|---|---|---|
| Ecological "(1.0 = boundary)" annotation | IR-M10-002 | FourFrameworkZone1D.tsx | Must fix before capture |
| AttributeSelector human-readable labels | IR-M10-003 | AttributeSelector.tsx | Must fix before capture |
| Argentina MDA floor breach verified | IR-M10-001 / #345 | Argentina fixture | Must verify before capture |

---

## Key Narration Notes for Spec Author (Step 4)

1. **Do not narrate the choropleth as the thesis visualization.** Per UX-RULING-4, the
   choropleth is geographic context (Zone 2A). The demo presenter should say
   "the trajectory view shows..." not "watch Argentina shift in the choropleth."

2. **The dashed curve convention needs one sentence of explanation.** Financial and HD
   Zone 1A curves are dashed (Path A — normalized_absolute scoring requires ≥2 entities,
   #193). The narration should acknowledge this: "two curves are dashed because they use
   a different scoring strategy than the two solid curves — that is disclosed in the
   methodology note, not hidden."

3. **Governance is no longer null.** The M8 narration noted "Governance — in validation."
   For Demo 3, governance is live. The narration should be: "All four axes are now live.
   Governance shows a composite score derived from WGI Rule of Law and V-Dem Liberal
   Democracy Index data." Do not say "honest null" for governance in M10 — that was
   the M8 state.

4. **The MAGNITUDE milestone.** Argentina 2002 (step 2) is the first MAGNITUDE-validated
   result in WorldSim backtesting. The demo narration for the backtesting section should
   name this explicitly: "The Argentina 2002 step is also the first case where the model
   is validated not just on direction but on magnitude — the simulated GDP contraction
   of negative 10.55 percent against the historical negative 10.9 percent."
