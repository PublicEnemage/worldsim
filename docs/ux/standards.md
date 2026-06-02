# WorldSim UX/UI Standards

> **Owner (R):** UX Designer Agent
> **Required Consultant (C):** Frontend Architect Agent
> **EL sign-off required** before any new standard is added or any existing standard is changed.
>
> **Established:** 2026-06-02 (Issue #620)
> **Authority:** This document codifies only decisions that are already settled. It records
> what was decided and where to find the source authority. No new decisions are made here.
>
> **Amendment process:** New standards are added via PR with UX Designer as R and EL sign-off.
> Existing standards are not changed without ADR-level rationale. A deviation from any standard
> listed here requires an Engineering Lead decision recorded in `docs/frontend/design-decisions.md`.

---

## 1. Framework Color Contract

**Authority:** UX Designer ruling 2026-05-23, ADR-010 Decision 3, MV-001 CVD validation.
**Implementation:** `frontend/src/constants/frameworkColors.ts`

| Framework | Hex | Notes |
|---|---|---|
| Financial | `#2271B3` | Strengthened from provisional blue to survive 60% opacity ghost curves |
| Human Development | `#D4841A` | Amber; stable under CVD (shifts toward yellow, opposite direction from teal) |
| Ecological | `#1A8FA0` | Teal; CVD substitution for provisional green (#3A7A4B). Green and HD orange became indistinguishable under deuteranopia — teal shifts toward blue, preserving distinction |
| Governance | `#7B50A8` | Purple; saturated to separate from Financial blue under CVD shift |

These values are frozen. Any change requires a UX Designer ruling and MV-001-equivalent CVD
validation. Do not modify without explicit sign-off.

---

## 2. Color Semantic Contract — Policy and Shock

**Authority:** ADR-008; `docs/frontend/design-decisions.md §DD-015`.

| Color role | Hex / treatment | Applied to |
|---|---|---|
| Policy instrument | Blue (`#2271B3` family) | Mode 3 control plane form; policy inflection markers on trajectory |
| Shock event | Orange (`#D4841A` family) | Mode 3 shocks form; shock event markers on trajectory |

Policy inflection markers: blue vertical line across all Zone 1A curves at the step of the
policy input.

Shock event markers: orange vertical line across all Zone 1A curves at the step of the shock.

---

## 3. Zone 1 Always-Visible Constraint

**Authority:** EL Decision 2 (2026-05-21); `docs/ux/information-hierarchy.md §Foundational rule`;
CLAUDE.md §UX Architectural Commitments.

All four Zone 1 instruments (1A Trajectory View, 1B MDA Alert Panel, 1C PMM Widget,
1D Four-Framework Current Position) must be visible in the primary viewport at all times
in all three modes:

- No Zone 1 instrument lives in a drawer, a tab, or behind any navigation action.
- The user must be able to complete the primary cognitive task of the active mode from
  Zone 1 without scrolling, clicking, or navigating away.
- A layout that moves any Zone 1 instrument behind interaction is a hierarchy violation
  regardless of viewport constraints.

---

## 4. Zone Layout Dimensions

**Authority:** `docs/frontend/design-decisions.md §DD-015`; EL ruling 2026-05-22 (FA-C3,
ADR-008 panel review).

| Zone | Width (minimum) | Viewport basis |
|---|---|---|
| Zone 1A — Trajectory View | 480px | 1024×768 minimum supported viewport |
| Zone 1C/1D — Co-primary cluster | 240px | 1024×768 |
| Control plane (Mode 3) | 280px | Always present — rendered at all times as an empty column in Modes 1/2; populated in Mode 3 |

The 280px control plane column is always rendered. A CSS class `mode-3-active` populates
it on Mode 3 entry. The column must not be conditionally removed — a layout reflow on
mode switch violates ADR-008 Decision 13 (instrument layout stability).

At 1280×800: trajectory = 580px, co-primary = 400px, control plane = 280px.

---

## 5. Choropleth Role — Geographic Context Surface (UX-RULING-4)

**Authority:** UX-RULING-4 (2026-06-02), `docs/ux/information-hierarchy.md §Foundational rule`,
`docs/ux/north-star.md`.

The choropleth is a navigable **context surface**, not a Zone 1 instrument and not a change
instrument.

**What the choropleth does:** Anchors the scenario geographically — "we are looking at
Argentina, here is where it sits in the global distribution."

**What the choropleth does not do:** Show quantitative step-to-step change as its primary
purpose. At single-entity global scale the color shift is not reliably visible (DEMO-001
root cause). This is a known limitation pending Option B (scenario-relative color scale,
M11).

**Narration discipline:** Any presenter sentence routing the audience to the choropleth for
quantitative change evidence is a violation of this standard. Quantitative change narration
routes to Zone 1A trajectory curves or Zone 1D composite score readout.

**Correct:** "Watch the trajectory curves — governance composite declining through steps 2–3."
**Incorrect:** "Watch Argentina shift in the choropleth as the crisis accumulates."

This restriction lifts when Option B is implemented and the choropleth visually corroborates
Zone 1A with a scenario-relative color scale.

---

## 6. Zone 1D Content Constraint (UX-RULING-4)

**Authority:** UX-RULING-4 (2026-06-02), `docs/ux/information-hierarchy.md §1D`.

Zone 1D is the four composite score values — a homogeneous [0,1] normalized readout, one
per framework. Its metaphor is an altimeter cluster: four instruments at the same abstraction
level simultaneously.

**Constraints:**
- Zone 1D rows are composite scores only. No raw indicator value rows.
- Zone 1D content is driven by scenario + current step. It has no content dependency on
  Zone 2 control elements (e.g. the choropleth AttributeSelector).
- Adding a fifth or supplementary row requires a new UX Designer ruling explicitly authorising
  a Zone 1D expansion — not a design-decisions.md entry.

---

## 7. Null vs. Zero Rendering Contract

**Authority:** UX-RULING-2 (2026-05-23, US-022); `docs/frontend/design-decisions.md §DD-011`.

A null composite score and a zero composite score are categorically different. The rendering
must make this distinction unambiguous.

| State | CSS class | Opacity | Border/line | Score display |
|---|---|---|---|---|
| Null (data unavailable) | `score-value--null` | ≤ 60% | Dashed | `"—"` |
| Numeric (including zero) | `score-value--numeric` | 100% | Solid | `toFixed(2)` e.g. `"0.00"` |

Zone 1D dashed left border signals null composite. Zone 1A null axis: dashed line with
hollow dot at each step. Filling a null axis with zero values is not acceptable.

---

## 8. MDA Alert Sort Order

**Authority:** `docs/ux/user-stories-instrument-cluster-m9.md §US-014`.
**Implementation:** `frontend/src/components/MDAAlertPanelZone1B.tsx §sortAlerts`.

1. Severity descending: TERMINAL → CRITICAL → WARNING
2. Within same severity: `step_index` ascending (earliest breach first)

This order is invariant across modes. The most severe, earliest alert is always row 1.

---

## 9. Mode-Specific Alert Tense Rule (UX-RULING-1)

**Authority:** UX-RULING-1 (2026-05-23, US-016).

| Mode | Alert line 1 text pattern |
|---|---|
| Mode 1 (Replay) | `"{indicator} crossed {severity} threshold at step {N}."` — historical fact; `"is projected"` and `"Caused by:"` absent |
| Mode 2 (Simulation) | `"{indicator} is projected to cross {severity} threshold at step {N}."` |
| Mode 3 (Active Control) | `"{severity} — {indicator} — {cohort} — step {N}"` — begins with severity; ` — ` separator |

---

## 10. Mode Indicator Label Strings (UX-RULING-3)

**Authority:** UX-RULING-3 (2026-05-23, US-026).

| Mode | Label string |
|---|---|
| Mode 1 | `"Replay"` |
| Mode 2 | `"Simulation"` |
| Mode 3 | `"Active Control"` |

No other label strings are acceptable. These appear in the persistent mode indicator in
the primary viewport header.

---

## 11. Confidence Tier Visual Differentiation

**Authority:** `docs/frontend/fa-brief-m9-instrument-cluster.md §Confidence tier visual`;
ADR-010 Decision 3.

| Tier | Zone 1A curve rendering | Zone 1D / Zone 2 |
|---|---|---|
| Tier 1 — Primary official statistics | Solid, full opacity | Full display |
| Tier 2 — Derived official statistics | Solid, full opacity | Full display |
| Tier 3 — Research estimates | Dashed curve; legend placeholder during ADR-007 deferral period | Full display |
| Tier 4 — Model estimates | Secondary panel only — not rendered in Zone 1 | Zone 2B indicator detail; badge in Zone 1B alert if alert source is Tier 4 |
| Tier 5 — Gap-filled values | Not displayed | Not displayed |

---

## 12. Zustand Atomic Update Contract

**Authority:** `docs/frontend/design-decisions.md §DD-012`.

All four Zone 1 instruments subscribe to a single Zustand store (`scenarioStepStore`).
State updates on step advance are atomic — all four instruments update in the same React
render cycle, not sequentially.

No Zone 1 instrument may maintain its own independent step state. The store is the single
source of truth for `current_step`, `trajectory`, `mda_alerts`, and `pmm_value`.

An entity switch must update all four Zone 1 instruments atomically — not one at a time,
not with separate loading states per instrument (see `information-hierarchy.md §Zone 1`).

---

## 13. Loading and Error State Patterns

**Authority:** `docs/frontend/design-decisions.md §DD-012`; IR-006 (Issue #500).

**Loading state:**
- Container carries `data-loading="true"` attribute.
- Skeleton rows present in DOM with same testids as live rows — E2E tests must be able to
  locate the container immediately without waiting for data.
- Skeleton rows display `"…"` or equivalent placeholder at reduced opacity.

**Error state:**
- Container carries `data-error="true"` attribute.
- Framework rows remain present in DOM (testids still discoverable).
- Inline error indicator rendered above rows (e.g. `data-testid="zone-1d-error"`).
- Scores render as `"—"` (same as pre-fetch null state).

---

## 14. Step Annotation Rule

**Authority:** `docs/frontend/design-decisions.md §DD-014`.

Step labels (shown on Zone 1A x-axis for SIGNIFICANT steps) are constrained to
**≤ 8 words AND ≤ 32 characters**. Both constraints must be satisfied simultaneously.

The 32-character constraint is enforced at fixture authoring time (backend). The 8-word
constraint is a readability gate — labels that require more than 8 words to be meaningful
should be shortened at authoring time, not truncated at render time.

---

## 15. Automatic A/B Split on First Control Input (Mode 3)

**Authority:** `docs/ux/north-star.md`; `docs/ux/information-hierarchy.md §Zone 1A`.

In Mode 3, baseline ghost curves (50% opacity, 1px stroke) appear automatically on Zone 1A
when the first control input is applied — no user action required to invoke them. The active
scenario curves render at 100% opacity, 2px stroke. A divergence fill region (5–10% opacity)
appears where they separate.

This is not a user-toggled feature. The comparison is always live once a control input exists.
