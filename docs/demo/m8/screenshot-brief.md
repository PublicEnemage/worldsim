# M8 Screenshot Brief — UX Designer Agent

> Generated: 2026-05-18. Produced by UX Designer Agent for Issue #233 / M8 demo preparation.
> Five frames specified for the M8 stakeholder demo: Greece 2010–2015, three live radar axes.

## Thesis Frame

**Frame C — "The Divergence" (Step 5, 2014)**

The single image that most completely communicates the WorldSim argument if only one screenshot is shared. Asymmetric radar deformation: financial axis partially extended, human development axis at crisis depth. Renders the argument — financial recovery is not the same as recovery — without requiring any caption.

---

## Five Frames

### Frame A — "The Instrument" (Step 1, 2010)

**What the radar shows:** Three active axes fully rendered at program entry. Governance axis: dashed hollow dot, labeled "Governance — in validation." The radar is relatively full at step 1 — this is the before-picture, not a crisis frame.

**Zone 1 required:**
- 1A (MDA Alert Panel): reserve_coverage_months CRITICAL alert already firing. Framework source label visible.
- 1B (Radar Chart): All four axes labeled with human-readable display names. Governance axis visually distinct (dashed, hollow).
- 1C (PMM Widget): "computing..." placeholder visible.

**Zone 2:** Default framework tab. No change required.
**Zone 3:** Collapsed.

**Caption:** Greece at IMF program entry, May 2010: reserve coverage already below the critical floor before the first austerity package lands.

**UI state:** GRC selected → EntityDetailDrawer open. Step 1. No Zone 3 panels expanded. Radar animation settled (capture after 250ms).

---

### Frame B — "The Collapse" (Step 3, 2012)

**What the radar shows:** All three active axes visibly compressed relative to Frame A. Maximum-stress posture — third memorandum consolidation.

**Zone 1 required:**
- 1A (MDA Alert Panel): Multiple alerts visible. Top two or three fully readable without scrolling.
- 1B (Radar Chart): Deformation from Frame A visually apparent.

**Zone 2:** Financial tab showing gdp_growth contraction. Confidence tier visible.
**Zone 3:** Collapsed.

**Caption:** Three rounds of fiscal consolidation produce simultaneous deterioration across financial, human development, and ecological frameworks — the tool surfaces the full cost, not just the headline deficit number.

**UI state:** GRC selected → EntityDetailDrawer open. Step 3. Financial tab active. No Zone 3 panels.

---

### Frame C — "The Divergence" ← THESIS FRAME (Step 5, 2014)

**What the radar shows:** Asymmetric deformation. Financial axis partially extended from Step 3 nadir. Human development axis remains near maximum compression. Two axes visibly out of phase.

**Zone 1 required:**
- 1B (Radar Chart): Financial and human development composite score values both legible. Spatial divergence is the primary message.
- 1A (MDA Alert Panel): Continuing human development alerts alongside easing financial signals.
- 1C (PMM Widget): Visible.

**Zone 2:** Human Development tab open — unemployment_rate at ~26.5%.
**Zone 3:** Collapsed.

**Caption:** 2014: financial indicators show partial recovery while unemployment remains at 26.5% — financial "recovery" and human recovery are not the same event.

**UI state:** GRC selected → EntityDetailDrawer open. Step 5. Human Development tab active. No Zone 3 panels.

---

### Frame D — "The Evidence" (Step 3, MDA close-up)

**What the radar shows:** Radar visible but not dominant. MDA alert panel is the compositional focus.

**Zone 1 required:**
- 1A (MDA Alert Panel): Occupies visual center of mass. Top three alerts fully readable: severity badge, indicator name, step index, framework source, top cohort.
- 1B (Radar Chart): Visible in background.

**Zone 2:** Visible but not focus.
**Zone 3:** Collapsed.

**Caption:** Each threshold breach is rendered as structured evidence — indicator, severity, step, affected population — ready to cite across a negotiating table.

**UI state:** GRC selected → EntityDetailDrawer open. Step 3. Alert panel scroll at top.

---

### Frame E — "The Planetary Dimension" (Step 3, Ecological tab)

**What the radar shows:** Ecological axis prominently labeled with CO2 boundary proximity score.

**Zone 1 required:**
- 1B (Radar Chart): Ecological axis with composite score. Axis is live — not null, not dashed.

**Zone 2:** Ecological tab active. co2_concentration_ppm indicator row showing value and confidence tier.

**Zone 3:** EcologicalNoteDrawer expanded — boundary normalization disclosure visible. Demonstrates methodology disclosed inline.

**Caption:** Milestone 8: planetary boundary proximity tracking live for the first time — ecological consequences are now a first-class measurement axis, not a footnote.

**UI state:** GRC selected → EntityDetailDrawer open. Step 3. Ecological tab active. EcologicalNoteDrawer expanded.

---

## Presentation Sequence

| Order | Frame | Step | Why |
|---|---|---|---|
| 1 | C — The Divergence | 5 | Lead with the argument |
| 2 | A — The Instrument | 1 | Pull back to program entry |
| 3 | B — The Collapse | 3 | Show the path that produced the divergence |
| 4 | D — The Evidence | 3 | Show what the specialist can cite |
| 5 | E — The Planetary Dimension | 3 | Close on M8's new capability |

Rationale: Lead with the thesis frame. The audience understands why the tool matters before they understand how it works.
