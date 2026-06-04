# WorldSim Semantic Component Vocabulary

**Milestone 11.5 — Usability Validation and Experience Audit**

| | |
|---|---|
| Authors | UX Designer Agent (zone/component classification), Frontend Architect Agent (element naming) |
| Authority | Pillar 3 provenance standard (`pillar-3-provenance.md §4.2`) |
| Status | v1.0 — effective for all M11.5 sessions |
| Issue | #719 |

---

## Purpose

This vocabulary is the naming system for WorldSim's interface components at three levels
of granularity: **zone**, **component**, and **element**. Every usability finding that
locates a failure in the interface must cite the canonical term from this document in
its `Component:` field.

A finding that references "Zone 1B" is precise enough to locate the panel but not the
specific failure. A finding that references `zone-1b / alert-severity-badge` is precise
enough to drive a targeted design or implementation fix.

**Citing the vocabulary:** Use the format `<zone-token> / <component-token> / <element-token>`
(omit levels that are not needed for precision). Examples:

- `zone-1b` — the entire MDA Alert Panel
- `zone-1b / alert-row` — a single alert row within the panel
- `zone-1b / alert-row / severity-badge` — the CRITICAL/WARNING badge on a row

---

## Level 1 — Zones

Zones are the top-level regions of the WorldSim viewport. They correspond directly to
the zones defined in `docs/ux/information-hierarchy.md`.

| Token | Display name | Location | Requires interaction to reach |
|---|---|---|---|
| `zone-header` | Persistent Header | Above all zones, always visible | Never |
| `zone-1a` | Trajectory View | Zone 1, primary instrument | Never |
| `zone-1b` | MDA Alert Panel | Zone 1, co-primary | Never |
| `zone-1c` | PMM Widget | Zone 1, co-primary | Never |
| `zone-1d` | Four-Framework Current Position | Zone 1, co-primary | Never |
| `zone-2a` | Radar Chart | Zone 2 | One scroll or one click |
| `zone-2b` | Framework Panels | Zone 2 | One scroll or one click |
| `zone-3a` | Methodology Notes | Zone 3 | Two or more interactions |
| `zone-3b` | Raw Indicator Tables | Zone 3 | Two or more interactions |
| `zone-scenario-list` | Scenario List | Landing state (no scenario loaded) | Never (landing state) |
| `zone-scenario-create` | Scenario Creation Form | Zone 2 | One click from landing |
| `zone-entity-drawer` | Entity Detail Drawer | Slide-in drawer | Drawer open action |
| `zone-choropleth` | Choropleth Map | Geographic context surface | Never (always visible in scenario view) |
| `zone-control-plane` | Control Plane | Reserved — Mode 3 (not yet built) | N/A |
| `zone-replay-viewer` | Session Replay Viewer | Shown when `?replay_session=` in URL | N/A |
| `zone-session-banner` | Session Recording Banner | Fixed overlay, top of viewport | Never (shown when `?usability_session=` in URL) |

---

## Level 2 — Components

Components are the distinct interactive or informational units within each zone.

### zone-header

| Token | Display name | Description |
|---|---|---|
| `zone-header / entity-selector` | Entity Selector | Dropdown or label showing the current entity name |
| `zone-header / mode-indicator` | Mode Indicator | Replay / Simulation / Active Control label |

### zone-1a — Trajectory View

| Token | Display name | Description |
|---|---|---|
| `zone-1a / trajectory-chart` | Trajectory Chart | The Recharts ComposedChart canvas |
| `zone-1a / step-axis` | Step Axis | The shared horizontal step axis |
| `zone-1a / financial-curve` | Financial Composite Curve | The financial framework composite score line |
| `zone-1a / human-dev-curve` | Human Development Curve | The human development composite score line |
| `zone-1a / ecological-curve` | Ecological Composite Curve | The ecological composite score line |
| `zone-1a / governance-curve` | Governance Composite Curve | The governance composite score line |
| `zone-1a / ci-band` | Confidence Interval Band | Shaded uncertainty band around a curve |
| `zone-1a / step-marker` | Step Event Marker | Label on step axis for a significant event |
| `zone-1a / legend` | Chart Legend | Curve identification legend |
| `zone-1a / attribute-selector` | Attribute Selector | Dropdown for selecting a single indicator to overlay |

### zone-1b — MDA Alert Panel

| Token | Display name | Description |
|---|---|---|
| `zone-1b / alert-list` | Alert List | The scrollable container of all active alerts |
| `zone-1b / alert-row` | Alert Row | A single MDA alert entry |
| `zone-1b / no-alerts-state` | No Alerts State | Empty state shown when no thresholds are breached |
| `zone-1b / overflow-indicator` | Overflow Indicator | "+N more alerts" count when alerts exceed visible height |

### zone-1b / alert-row — Alert Row Elements

| Token | Display name | Description | `data-testid` |
|---|---|---|---|
| `zone-1b / alert-row / severity-badge` | Severity Badge | CRITICAL or WARNING label | `alert-line-1` (compact) |
| `zone-1b / alert-row / framework-tag` | Framework Tag | financial / human\_development / ecological / governance source label | `alert-framework-source` |
| `zone-1b / alert-row / indicator-name` | Indicator Name | The name of the breached indicator | `alert-line-1` |
| `zone-1b / alert-row / threshold-value` | Threshold Value | The MDA floor value that was crossed | `alert-line-2` |
| `zone-1b / alert-row / mode-text` | Mode Text | "crossed" / "is projected to cross" depending on mode | `alert-mode-text` |
| `zone-1b / alert-row / causal-attribution` | Causal Attribution | "Caused by:" attribution line | `alert-causal-attribution` |
| `zone-1b / alert-row / negotiation-label` | Negotiation Label | The negotiation-context framing text | `alert-negotiation-label` |

### zone-1c — PMM Widget

| Token | Display name | Description | `data-testid` |
|---|---|---|---|
| `zone-1c / pmm-label` | PMM Label | "Policy Maneuver Margin" heading | `pmm-label` |
| `zone-1c / pmm-value` | PMM Value | The numeric PMM value (0.00–1.00) | `pmm-value` |
| `zone-1c / pmm-direction-arrow` | Direction Arrow | Trend arrow (↑ / ↓ / →) | `pmm-direction-arrow` |
| `zone-1c / pmm-breached-note` | Breached Note | "—" state label when all thresholds breached | `pmm-breached-note` |
| `zone-1c / pmm-pending` | Pending State | Loading/pending state before first computation | `pmm-pending` |

### zone-1d — Four-Framework Current Position

| Token | Display name | Description |
|---|---|---|
| `zone-1d / framework-row` | Framework Row | Single row for one framework (financial / human\_development / ecological / governance) |
| `zone-1d / framework-row / score` | Framework Score | The numeric composite score for the framework |
| `zone-1d / framework-row / label` | Framework Label | The framework name |
| `zone-1d / framework-row / null-indicator` | Null Score Indicator | Dashed border style when score is null/unavailable |
| `zone-1d / ecological-boundary-note` | Ecological Boundary Note | "1.0 = boundary" sub-label on the ecological row |

### zone-2a — Radar Chart

| Token | Display name | Description |
|---|---|---|
| `zone-2a / radar-chart` | Radar Chart Canvas | The SVG radar chart |
| `zone-2a / radar-axis` | Radar Axis | A single axis (one per framework) |
| `zone-2a / radar-polygon` | Score Polygon | The filled polygon representing the current composite scores |

### zone-2b — Framework Panels

| Token | Display name | Description |
|---|---|---|
| `zone-2b / framework-panel` | Framework Panel | A single framework's detail panel |
| `zone-2b / indicator-row` | Indicator Row | A single indicator within a framework panel |
| `zone-2b / indicator-row / name` | Indicator Name | Display name of the indicator |
| `zone-2b / indicator-row / value` | Indicator Value | Current value and unit |
| `zone-2b / indicator-row / confidence-badge` | Confidence Badge | Tier 1–5 confidence label |

### zone-3a — Methodology Notes

| Token | Display name | Description |
|---|---|---|
| `zone-3a / methodology-note` | Methodology Note | Collapsed disclosure for a specific model limitation or synthetic data flag |

### zone-3b — Raw Indicator Tables

| Token | Display name | Description |
|---|---|---|
| `zone-3b / indicator-table` | Indicator Table | Full tabular view of all indicator values across all steps |

### zone-scenario-list

| Token | Display name | Description |
|---|---|---|
| `zone-scenario-list / scenario-card` | Scenario Card | A single scenario entry in the list |
| `zone-scenario-list / create-btn` | Create Scenario Button | The primary action to create a new scenario |
| `zone-scenario-list / scenario-card / name` | Scenario Name | The scenario's display name |
| `zone-scenario-list / scenario-card / status` | Scenario Status | pending / running / complete status label |
| `zone-scenario-list / scenario-card / entity` | Entity Label | The scenario's country/entity name |

### zone-scenario-create

| Token | Display name | Description |
|---|---|---|
| `zone-scenario-create / country-field` | Country Field | Country/entity input |
| `zone-scenario-create / start-year-field` | Start Year Field | Scenario start year input |
| `zone-scenario-create / steps-field` | Steps Field | Number of steps input |
| `zone-scenario-create / module-toggle` | Module Toggle | Enable/disable toggle for a simulation module (one per module) |
| `zone-scenario-create / submit-btn` | Submit Button | Create scenario action button |

### zone-scenario-controls

| Token | Display name | Description | `data-testid` |
|---|---|---|---|
| `zone-scenario-controls / advance-step-btn` | Advance Step Button | Runs the next simulation step | `advance-step-btn` |
| `zone-scenario-controls / step-counter` | Step Counter | Current step / total steps display | — |

### zone-session-banner

| Token | Display name | Description | `data-testid` |
|---|---|---|---|
| `zone-session-banner / recording-indicator` | Recording Indicator | Red dot + session ID text | `session-recording-banner` |
| `zone-session-banner / end-session-btn` | End Session Button | Stops recording and saves artifact | `end-session-btn` |
| `zone-session-banner / save-success` | Save Success State | Green success confirmation after save | — |

### zone-choropleth

| Token | Display name | Description | `data-testid` |
|---|---|---|---|
| `zone-choropleth / map-canvas` | Map Canvas | The choropleth SVG map | `choropleth-map` |
| `zone-choropleth / entity-highlight` | Entity Highlight | The highlighted region for the active entity | — |

### zone-entity-drawer

| Token | Display name | Description |
|---|---|---|
| `zone-entity-drawer / drawer-panel` | Drawer Panel | The slide-in detail panel |
| `zone-entity-drawer / close-btn` | Close Button | Closes the drawer |

---

## Level 3 — Elements

Level 3 elements are listed inline within the component tables above (see the element
rows under `zone-1b / alert-row` and `zone-1d / framework-row`). For zones where no
element-level vocabulary exists yet, add entries here as findings require the precision.

---

## Vocabulary Usage in Findings

When writing a finding, use the most precise vocabulary level that is needed to locate
the failure. If the failure is visible anywhere within Zone 1B, cite `zone-1b`. If the
failure is specific to the severity badge on a single alert row, cite
`zone-1b / alert-row / severity-badge`.

**Preferred form:**
```
Component: zone-1b / alert-row / severity-badge
```

**Acceptable for zone-level findings:**
```
Component: zone-1b
```

**Not acceptable (non-canonical):**
```
Component: the red badge in the alerts section
Component: the alert panel
Component: Zone 1B alert severity
```

---

## Changelog

| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-06-04 | Initial vocabulary established for M11.5 (Issue #719). Covers all components present in v0.11.0 / PR #724 baseline. |
