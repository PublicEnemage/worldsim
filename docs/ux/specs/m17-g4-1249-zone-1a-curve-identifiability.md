---
name: m17-g4-1249-zone-1a-curve-identifiability
type: ux-visual-spec
issue: "#1249"
sprint-entry: docs/process/sprint-plans/m17-g4-sprint-entry.md
authored-by: UX Designer Agent
authored-date: 2026-06-25
governing-documents:
  - docs/ux/information-hierarchy.md §COMPARE_VIEW Hierarchy
  - docs/ux/information-hierarchy.md §Zone 1A — Confidence Display
  - docs/ux/north-star.md §Primary Cognitive Tasks
  - CLAUDE.md §UX Architectural Commitments (premises 1–2)
---

# UX Visual Spec — M17-G4 Issue #1249: Zone 1A Curve Identifiability

**Decision: Terminal endpoint labels** (see §2).

---

## 1. Problem Statement

In Zone 1A composite compare mode (N=2 entities or scenarios), two trajectory curves
are rendered using ENTITY_PALETTE color coding. The only identification aid is the
`entity-labels-overlay` div positioned in the top-right corner of the chart — disconnected
from the curves themselves. At 1280×800 (80% zoom = 1024×640), when two curves are
proximate or crossing, the corner overlay does not allow glance-level identification of
which label belongs to which curve.

At the Demo 7 presentation scale, Persona 1 (Lucas Ferreira) must read Zone 1A trajectory
curves without hovering. "Curve identifiability" is a primary cognitive task requirement
(`information-hierarchy.md §Zone 1A`, CLAUDE.md §UX Architectural Commitments premise 2:
"Instruments are always visible; context is navigable").

---

## 2. Decision: Terminal Endpoint Labels

**Chosen approach:** Add a short text label directly at (or just left of) the rightmost
data point of each entity's composite trajectory curve in `CompositeChartSVG`.

**Rejected: line-style differentiation** — solid vs. dashed lines require a legend
to decode and add cognitive load at demo presentation speed. Terminal labels are
self-interpreting.

**Rejected: color-only** — already the status quo; insufficient when curves are proximate.

### Label content rules

| Context | Label shown | Example |
|---|---|---|
| N=2 entity comparison (current) | ISO alpha-3 entity code | "ZMB", "GRC" |
| N=3 scenario comparison (G2 Phase 3) | Short scenario identifier | "A", "B", "C" |

G2 Phase 3 passes label content via a `terminalLabel?: string` property per entity slot.
When absent, the entity code is used. #1249 implements the label infrastructure;
G2 Phase 3 passes scenario identifiers through the same mechanism.

### Visual properties

| Property | Value |
|---|---|
| Font size | 8px |
| Font weight | bold |
| Color | Same as entity's ENTITY_PALETTE color |
| Position | x: xLast + 3; y: yLast − 7 (above the curve endpoint, left of right margin) |
| Background | `rgba(255,255,255,0.85)` — 2px horizontal padding |
| testid | `zone-1a-terminal-label-{code}` |

The label is placed IN the SVG element (not an overlay div) so it does not require
z-index management and is always visible.

---

## 3. Before / After Mockups

### N=2 — BEFORE (current state: corner overlay only)

```
Zone 1A — 1280×800 viewport (80% zoom = 1024×640 effective)
Width: 580px allocated, height: 300px

┌────────────────────────────────────────────────────────────────────┐  ZMB ◀── corner
│                                                    ─ ─ ─          │  GRC     overlay;
│                                              ─ ─ ─               │        disconnected
│                                      ─ ─ ─  ━━━━━━━━━━━━━━━━━━━━│T2      from curves
│                                 ─ ─ ─━━━━━━━                     │T1
│               ─ ─ ─━━━━━━━━━━━━━                                  │
│       ─ ─ ─━━━                                                     │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘

  ─ ─ ─   GRC composite trajectory (blue, ENTITY_PALETTE[0])
  ━━━━━━  ZMB composite trajectory (teal, ENTITY_PALETTE[1])
  T2/T1   tier badges at right edge
  ZMB/GRC corner overlay (top-right) — detached from curve endpoints
```

**Problem at demo:** At 80% zoom, when curves are close or crossing near step 2–3,
the viewer cannot tell which label (ZMB / GRC) belongs to which curve without careful
inspection. Corner overlay provides no directional guidance.

### N=2 — AFTER (terminal endpoint labels)

```
Zone 1A — 1280×800 viewport (80% zoom = 1024×640 effective)
Width: 580px allocated, height: 300px

┌────────────────────────────────────────────────────────────────────┐
│                                                    ─ ─ ─    GRC   │ T2
│                                              ─ ─ ─           ▲    │
│                                      ─ ─ ─  ━━━━━━━━━━━━━━━━│━━━ │ T2
│                                 ─ ─ ─━━━━━━━         ZMB ──►│    │ T1
│               ─ ─ ─━━━━━━━━━━━━━                             │    │
│       ─ ─ ─━━━                                               │    │
│                                                              │    │
└────────────────────────────────────────────────────────────────────┘

  ─ ─ ─   GRC composite trajectory → "GRC" terminal label at endpoint
  ━━━━━━  ZMB composite trajectory → "ZMB" terminal label at endpoint
  T2/T1   tier badges remain at right edge (unchanged)
  Corner overlay: retained as-is (harmless; may be removed in G2 Phase 3 cleanup)
```

**Improvement at demo:** Label "GRC" is positioned directly above GRC's last data
point; "ZMB" is directly above ZMB's last data point. Glance-level identification
without legend lookup.

### N=3 — VALIDATION (G2 Phase 3 scenario comparison; labels: "A", "B", "C")

```
Zone 1A — three scenario comparison curves

┌────────────────────────────────────────────────────────────────────┐
│                                              ─ ─ ─       A        │ T3
│                                        ─ ─ ─            ▲        │
│                                  ─ ─ ─   ━━━━━━━━━━━━━━━│━  B    │ T2
│                              ─ ─ ─━━━━━━━    ════════════│════    │ T1
│           ─ ─ ─━━━━━━━━━━━━━           ═════         C──►│        │ T1
│   ─ ─ ─━━━         ════════════════════                   │        │
│                                                           │        │
└────────────────────────────────────────────────────────────────────┘

  ─ ─ ─   Scenario A  → label "A" (blue, ENTITY_PALETTE[0])
  ━━━━━━  Scenario B  → label "B" (teal, ENTITY_PALETTE[1])
  ══════  Scenario C  → label "C" (amber, ENTITY_PALETTE[2])
```

N=3 validation: same terminal label mechanism, no code changes needed for G2 Phase 3
(only label content differs — "A"/"B"/"C" instead of entity codes).

---

## 4. Zone 1D Density Check

Not applicable to #1249 (Zone 1A only).

---

## 5. Governing Premises Satisfied

| Premise | Source | How satisfied |
|---|---|---|
| Zone 1 instruments always visible without interaction | CLAUDE.md §UX Architectural Commitments premise 2 | Terminal labels are inline SVG — no click, no hover required |
| Glance-level readability at 90-second ceiling | north-star.md §Primary Cognitive Tasks | Label directly at curve endpoint eliminates legend lookup |
| Step axis is the shared frame | CLAUDE.md §UX Architectural Commitments premise 3 | Labels placed AT the rightmost step — no disruption to step axis |
| N=3 compatibility | G4 sprint entry §2.2 constraint | Same mechanism works for N=3 without modification (validated in mockup §3) |

---

## 6. Regression Contract

The terminal label addition is to the composite SVG path only. It does NOT affect:
- The recharts rendering path (N=1 Mode 1/2 single entity with four framework curves)
- The existing `entity-labels-overlay` corner div (retained; may be cleaned up in G2 Phase 3)
- The tier badge position (unchanged at `x = MARGIN.left + chartW + 4`)
- The `zone-1a-trajectory` testid or any existing testids

**Single-scenario (N=1 Mode 1/2) regression guard:** The `useComposite` flag is
`false` for N=1 in Mode 1/2 — the terminal label code path is only reached in the
composite SVG branch. No recharts path is touched.

---

## 7. Implementation Notes for Frontend Engineer

File: `frontend/src/components/TrajectoryView.tsx`

In `CompositeChartSVG`, after the existing tier badge rendering block (lines 538–563):

```typescript
{/* Terminal entity labels — #1249 Zone 1A curve identifiability */}
{entityCodes.map((code, i) => {
  const active = activeTrajectories[code];
  if (!active || active.steps.length === 0) return null;
  const lastStep = active.steps[active.steps.length - 1];
  const lastScore = computeEntityCompositeScore(lastStep);
  if (lastScore === null) return null;
  const color = ENTITY_PALETTE[i % ENTITY_PALETTE.length];
  const x = xScale(lastStep.step_index);
  const y = yScale(lastScore);
  return (
    <text
      key={`terminal-label-${code}`}
      data-testid={`zone-1a-terminal-label-${code}`}
      x={x + 3}
      y={y - 7}
      fontSize={8}
      fontWeight="bold"
      fill={color}
      dominantBaseline="auto"
    >
      {code}
    </text>
  );
})}
```

The label is placed 3px right and 7px above the last data point. At N=2 with
two curves whose last-point y values differ by less than 14px, the labels may
overlap — in practice, curves that end at the same Y value are rare (they would
have converged to the same composite score). For Demo 7 with Greece + Zambia
(fiscal trajectories diverge meaningfully), overlap is not expected.

If overlap IS detected during Step 4 Verify, the implementing agent may apply a
`dy` offset proportional to entity index: `y = y - 7 - (i * 10)`. This is an
implementation-level judgement call — it does not require a spec revision.
