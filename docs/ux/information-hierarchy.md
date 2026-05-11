# Information Hierarchy — WorldSim Dashboard

> Owned by the UX Designer Agent. This document defines the visual weight
> and disclosure depth of every element on the WorldSim dashboard. It is
> the reference for all Frontend Architect decisions about layout, ordering,
> and progressive disclosure. When a proposed component placement conflicts
> with this hierarchy, this document governs — not implementation convenience.
>
> Last updated: 2026-05-11 (founding document; M8 scope; extends
> `north-star.md` and `user-journeys.md`).

---

## Governing Principle

The information hierarchy exists to serve one task: threshold alarm detection
under cognitive load. This is the primary cognitive task established in
`north-star.md §Primary Cognitive Task`.

Every hierarchy decision is evaluated against this question:

> Does this placement help the specialist answer "has any indicator crossed a
> floor?" in under 30 seconds with people in the room and a clock running?

Elements that serve this question directly occupy primary position. Elements
that support it after the first question is answered occupy secondary position.
Elements that require exploration occupy tertiary position — accessible, but
not competing with the primary scan.

---

## The Three Disclosure Zones

### Zone 1 — Primary (no interaction required)

Visible on page load or on drawer open, without scrolling, at any viewport
likely to be used in a negotiation room (desktop 1280×800 minimum,
tablet 1024×768 minimum). Occupies the upper portion of each view.

**The user must be able to complete the primary cognitive task from Zone 1
alone.** If the answer to "has anything crossed a threshold?" requires
leaving Zone 1, the hierarchy is wrong.

### Zone 2 — Secondary (one scroll or one click)

Visible after a single scroll or a single expand/tab action. Provides the
evidence behind the Zone 1 signal: indicator detail, confidence tier,
cohort breakdown, trajectory values. This is the preparation-mode surface.

### Zone 3 — Tertiary (deliberate navigation)

Requires two or more interactions: a click to expand, then a scroll, or
a tab change then a read. Contains methodology disclosures, raw indicator
tables, historical comparison data, and model limitation documentation.
In negotiation mode, Zone 3 content is never needed. In preparation mode,
it supports the argument-building phase but is never the first stop.

---

## Dashboard View Hierarchy (SCENARIO_VIEW / SCENARIO_COMPLETE)

### Zone 1 — Primary

**1A — MDA Alert Panel** *(highest weight)*

The alert panel is the first element the user's eye must reach. Positioned
at the top of the entity detail surface (above all framework tabs) when the
EntityDetailDrawer is open. Positioned as a persistent overlay or banner
in the main view when the drawer is closed and alerts are active.

Requirements:
- Top 1–3 alerts visible without scrolling at all supported viewports
- Each alert row must show: severity (color + label), indicator name,
  step index, and top affected cohort — all readable without expanding
- Severity ordering: TERMINAL before CRITICAL before WARNING
- Framework source visible per alert (financial / human_development /
  ecological / governance) — this is new at M8 and must appear without
  requiring the user to open a framework tab

**1B — Radar Chart** *(secondary primary weight)*

Positioned immediately below the alert panel or alongside it on
wide viewports. The radar chart is the visual argument that a country's
situation cannot be understood through one lens. At M8, with all four
axes live for the first time, this is the most visually significant
element the tool has ever displayed.

Requirements:
- All four axes visible simultaneously — no tabs, no toggles, no "click to
  see ecological"
- Axis labels must be human-readable: "Financial", "Human Development",
  "Ecological", "Governance" — not framework enum values
- Each axis shows the composite score value as a number alongside the
  visual position on the axis
- Step-to-step transitions must be animated (200–300ms ease-in-out) so
  the user sees the deformation happen, not just the result
- When all four composite scores are non-null (M8 target state), the chart
  fills visibly — a partially-filled chart (null axes showing as zero) is
  not acceptable as the default; null axes must be visually distinct from
  zero-value axes

**1C — Coffin Corner / Policy Maneuver Margin Indicator** *(M8 addition)*

New at M8. The Policy Maneuver Margin is the most conceptually powerful
output WorldSim produces — it tells the specialist how much room remains
before the corrective maneuver window closes. It must not appear as a row
in a table or a footnote in an indicator list.

Requirements:
- Dedicated visual treatment: not a row in FrameworkPanel, not a subtitle
  under the radar chart — a distinct widget with its own visual identity
- Must show direction (is the margin growing or shrinking since last step?)
  as a directional indicator (arrow or trend line), not just a current value
- Positioned in Zone 1 — visible without scrolling when EntityDetailDrawer
  is open at minimum supported viewport
- Label must be legible to a non-specialist on first read: "Policy
  Maneuver Margin" is acceptable; "coffin_corner_index" is not

---

### Zone 2 — Secondary

**2A — Framework Panels** (financial, human_development, ecological, governance)

The four FrameworkPanel tabs contain the indicator detail behind each
radar axis. The user reaches Zone 2 after Zone 1 has confirmed which
framework is under stress — she then opens the relevant tab to examine
specific indicators, confidence tiers, and cohort breakdowns.

Requirements at M8:
- Indicator display names must be human-readable (see Gap 1 from UX
  Designer M8 recommendations): `rule_of_law_percentile` → "Rule of Law
  (global percentile)", `co2_concentration_ppm` → "CO2 Contribution (ppm)"
- Confidence tier must be visible per indicator row without expanding —
  it is an argument quality signal the specialist needs to cite
- Cohort breakdown (income quintile, age band) visible within Zone 2 by
  expanding an indicator row — one click, not a separate navigation

**2B — Step Timeline / Scenario Progress**

Shows the step-by-step trajectory of key indicators. Accessed via scroll
in the drawer or a dedicated trajectory tab. The specialist uses this to
identify at which step a deterioration began — required for the
argument ("this threshold is crossed in year 3 of the program").

**2C — Distribution Bands** (M5 forward)

Uncertainty bands on individual indicators. Visible in Zone 2 after
the alert panel has confirmed which indicators to examine. The band
width is the evidence behind the distribution-source alert.

---

### Zone 3 — Tertiary

**3A — Methodology Notes and Mandatory Disclosures**

All methodology disclosures — ia1_disclosure, the ecological normalization
methodology note, the data source citations — belong in Zone 3. They must
be present (ADR-005 Amendment B mandates the ecological note; ADR-006
Decision 13 mandates ia1_disclosure) but must not compete with Zone 1 or
Zone 2 content for visual attention.

Implementation: collapsed info panel accessible via an (i) icon or
"Methodology notes" expandable link. The collapsed state shows only a
one-line indicator that disclosures are available ("ⓘ Methodology notes
— expand for data limitations and model uncertainty disclosure"). The
expanded state shows the full text.

This is the resolution of UX Gap 2 identified in the M8 demo review: the
mandatory ecological note currently renders inline with the composite score.
It is ADR-compliant at Zone 3 — the note is present and accessible — while
no longer occupying Zone 1 attention.

**3B — Raw Indicator Tables**

Full attribute dumps, source registry IDs, data provenance. For
methodology reviewers and contributor workflows, not for the canonical user
during preparation or negotiation.

**3C — Backtesting Fidelity Dashboard**

The per-case pass/fail fidelity view. Used by analysts calibrating the
model and by methodology reviewers, not by the canonical user in the IMF
negotiation context.

---

## BASELINE_VIEW Hierarchy (no scenario selected)

Zone 1: Scenario list with name, status, entity, and creation date — sorted
by most recently modified. The specialist must be able to identify and select
the correct scenario within 10 seconds (Journey B, Step 1).

Zone 2: Scenario creation entry point. Accessible from Zone 1 without
navigating away.

Zone 3: System status, data source registry, configuration.

---

## COMPARE_VIEW Hierarchy (two scenarios active)

Zone 1: DeltaChoropleth — geographic divergence between scenarios, color-coded
by direction and magnitude. The primary question in compare mode is "where do
these scenarios diverge?" and the answer must be visible immediately.

Zone 2: EntityDetailDrawer for the primary scenario — MDA alerts for the
entity of interest in the primary scenario, showing which alerts fire in the
primary but not the comparison (or vice versa).

Zone 3: Side-by-side indicator tables for the two scenarios. Used in preparation
mode to build the detailed counter-proposal argument.

---

## M8 Hierarchy Decisions

These decisions are binding for M8 implementation and must not be overridden
by implementation convenience.

| Decision | Ruling | Rationale |
|---|---|---|
| All four radar axes must appear simultaneously | No tabs, no toggles | The four-framework argument collapses if any axis requires interaction to reveal |
| Null axes must be visually distinct from zero-value axes | Distinct treatment (e.g., dashed outline, "—" label) | A zero governance score and a null governance score are categorically different; conflating them is a precision error |
| Policy Maneuver Margin is Zone 1, not a FrameworkPanel row | Dedicated widget, not a table row | It is the primary instrument for Coffin Corner detection — burying it in a panel defeats the purpose |
| Methodology notes are Zone 3 | Collapsed by default, accessible via (i) | Mandatory ADR-005/006 compliance satisfied without competing with threshold alarm detection |
| Indicator display names are human-readable | Display name mapping layer in frontend | Demo and negotiation-room legibility; internal keys are implementation detail |
| Radar chart step transitions are animated | 200–300ms ease-in-out | The deformation across steps is the visual argument; it must be observable, not just the result |
| MDA alert framework source visible in Zone 1 | Shown per alert row without expanding | At M8, ecological and governance alerts fire for the first time; the specialist must know which framework without opening a tab |

---

## What Belongs in Which Document

| Question | Document |
|---|---|
| Who is the user and what are they trying to do? | `north-star.md` |
| What does the user do step by step? | `user-journeys.md` |
| Where does each element appear and at what depth? | This document |
| How is a specific component implemented? | `docs/frontend/` architecture documents |
| What design decision was made and why? | `docs/frontend/design-decisions.md` |

Hierarchy decisions (this document) govern layout and depth. Implementation
decisions (design-decisions.md) govern how the layout is built. When they
conflict, hierarchy governs — the implementation must adapt to the hierarchy,
not the reverse.
