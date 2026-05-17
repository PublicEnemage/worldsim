# Frontend Architect Brief — Milestone 8

**Author:** Frontend Architect Agent (activated 2026-05-17, Issue #298)
**UX Designer sign-off required before any implementation begins.**
**Scope:** M8 UI issues #265–268; cross-ADR type fix for null governance axis
**ADR references:** ADR-005 Decisions M8-5 (null axis rendering), M8-6 (ecological proximity attributes); ADR-005 Amendment 3 panel synthesis (cross-ADR type obligation)
**Information hierarchy source:** `docs/ux/information-hierarchy.md` (binding M8 hierarchy decisions table)

---

## Context

Four M8 UI issues (#265–268) were deferred pending: (1) ADR-005 Amendment 3 acceptance, and (2) this Frontend Architect brief with UX Designer sign-off. The ADR-005 panel synthesis (PR #303) identified a cross-ADR type obligation that must be resolved before any radar chart implementation work begins.

This brief covers five areas. Each area specifies: the binding UX decision, the current code state, the required change, the affected files, and any cross-file sequencing constraints.

---

## Area 1 — Null Governance Axis: Type Fix and Rendering Contract

### Binding decision (information-hierarchy.md)

> Null governance axis renders as dashed outline with "—" score and "Governance — in validation" label. Zero-value render is prohibited. This is a binding M8 hierarchy decision.

### Cross-ADR obligation (panel synthesis — must-resolve M8-5)

`RadarAxisDatum.composite_score` is currently typed as `number` (see `frontend/src/types.ts:134`). This type cannot represent the null governance state: the panel synthesis finding is that the em dash "—" display requires `null`, not `0`. Using `0` for null governance violates the information-hierarchy prohibition on zero-value rendering.

**Required type change:**

```typescript
// frontend/src/types.ts — ADR-005 Decision 4
export interface RadarAxisDatum {
  framework: string;
  label: string;
  composite_score: number | null;  // null = not yet implemented; 0.0–1.0 when active
  is_implemented: boolean;
  has_critical_breach: boolean;
  breach_count: number;
}
```

This is a same-commit cross-ADR obligation: the type change in `types.ts` and the rendering implementation in `RadarChart.tsx` must ship in the same commit as any reference to null governance in ADR-005.

### Current code state

`EntityDetailDrawer.tsx:81`:
```typescript
composite_score: output?.composite_score != null ? parseFloat(output.composite_score) : 0,
is_implemented: output?.composite_score != null,
```

The fallback to `0` is the source of the zero-value render violation. It must become `null`.

### Required rendering contract (RadarChart.tsx)

The radar chart must handle three states for each axis:

| State | `composite_score` | `is_implemented` | Visual |
|---|---|---|---|
| Active with data | `number` (0.0–1.0) | `true` | Filled polygon, normal dot |
| Null / not yet active | `null` | `false` | Dashed outline, hollow dot |
| Active with critical breach | `number` | `true` | Red dot, bold label |

For the null axis:
- The axis outline must render as a **dashed stroke**, not a filled polygon segment at zero.
- The axis label must show **"Governance — in validation"** (not "Governance").
- The tooltip must display **"—"** in place of a numeric score.
- The `final_score` passed to Recharts for the null axis must be `null` (Recharts will treat this as a gap in the polygon). Do not pass `0`.

### Affected files

1. `frontend/src/types.ts` — type change (same commit as implementation)
2. `frontend/src/components/EntityDetailDrawer.tsx:81` — null fallback instead of `0`
3. `frontend/src/components/RadarChart.tsx` — null-state dot, dashed outline, tooltip, label

### Sequencing constraint

This is the prerequisite for all other radar chart work (#267 animation). The type change must land first. Any animation implementation (Area 5) that touches `chartData` mapping must operate on `number | null`, not `number`.

---

## Area 2 — Coffin Corner / Policy Maneuver Margin: Zone 1 Widget

### Binding decision (information-hierarchy.md)

> Coffin Corner / PMM is Zone 1C — a dedicated widget with directional indicator. It is not embedded in the radar chart or any framework panel. Zone 1C placement is mandatory.

### Current code state

No PMM widget exists. Issue #268 is not yet started.

### Required architecture

The PMM widget is a **standalone component** at Zone 1 level — placed in `EntityDetailDrawer` between the MDA alert panel (Zone 1A) and the radar chart (Zone 1B), not inside either.

Component: `frontend/src/components/PMMLedger.tsx` (new file)

Props contract:
```typescript
interface PMMLedgerProps {
  pmm_score: number | null;           // 0.0–1.0 composite; null if uncomputed
  pmm_trend: "improving" | "stable" | "deteriorating" | null;
  pmm_components: PMMMComponentRow[]; // fiscal space, reserves, political capital, time
}

interface PMMMComponentRow {
  dimension: string;
  value: number | null;
  unit: string;
  trend: "improving" | "stable" | "deteriorating" | null;
}
```

Visual spec:
- Primary display: a large number (0–100 scale or 0.0–1.0) with a directional arrow (↑ / → / ↓) derived from `pmm_trend`.
- Color coding: green (>0.6), amber (0.3–0.6), red (<0.3). Same threshold logic as MDA CRITICAL/WARNING/TERMINAL — but PMM color is a continuous gradient, not a step function.
- No breach badge — PMM is a composite margin indicator, not an alert. The MDA panel handles alerts.
- Collapsed by default. The Zone 1C position shows the headline score + trend arrow. Component breakdown is one-click expand (Zone 2 territory once expanded).
- If `pmm_score` is null: render placeholder text "Policy Maneuver Margin — computing…" with a spinner. Do not render a 0 or show a misleading zero margin.

### Data dependency

PMM score is not yet computed by the backend. Issue #268 is blocked on ADR-005 amendment acceptance. The frontend component must be built to accept `null` gracefully — the placeholder state is the M8 render state. The PMM widget ships M8 with the null placeholder; the live score ships when the backend computation is complete.

### Affected files

1. `frontend/src/components/PMMLedger.tsx` — new component
2. `frontend/src/components/EntityDetailDrawer.tsx` — import and render between MDA panel and RadarChart

---

## Area 3 — Indicator Display Name Mapping Layer

### Binding decision (information-hierarchy.md)

> Zone 2A framework panels display human-readable indicator names. The mapping layer lives in the frontend, is extensible per framework, and does not require backend changes.

### Current code state

`FrameworkPanel.tsx` renders indicator names directly from the API key string (e.g., `gdp_growth_rate`, `poverty_headcount_ratio`). These are database field names, not display names. Issue #265 is the gap.

### Required architecture

A **display name registry** module: `frontend/src/lib/indicatorDisplayNames.ts`

Structure:
```typescript
// framework → indicator_key → display name
const INDICATOR_DISPLAY_NAMES: Record<string, Record<string, string>> = {
  financial: {
    gdp_growth_rate: "GDP Growth Rate",
    current_account_balance: "Current Account Balance",
    // ... extend per indicator
  },
  human_development: {
    poverty_headcount_ratio: "Poverty Headcount",
    // ...
  },
  ecological: {
    planetary_boundary_co2_proximity: "CO₂ Boundary Proximity",
    planetary_boundary_land_use_proximity: "Land Use Boundary Proximity",
  },
  governance: {
    // populated when GovernanceModule activates (M9+)
  },
};

export function getIndicatorDisplayName(framework: string, key: string): string {
  return INDICATOR_DISPLAY_NAMES[framework]?.[key] ?? formatFallback(key);
}

// Fallback: convert snake_case to Title Case for unmapped keys
function formatFallback(key: string): string {
  return key.replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());
}
```

`getIndicatorDisplayName` is the single access point. All indicator name rendering in `FrameworkPanel.tsx` routes through this function. The fallback ensures unmapped keys (new ecological indicators from M8-6) display as readable strings rather than raw keys.

### Extension contract

When a new indicator is added to any framework:
1. Add the `indicator_key → display name` entry to the relevant framework block in `indicatorDisplayNames.ts`.
2. No other file requires a change for the display name to appear.

This is the extension contract. Do not inline display names in component JSX — all names flow through the registry.

### Affected files

1. `frontend/src/lib/indicatorDisplayNames.ts` — new registry module
2. `frontend/src/components/FrameworkPanel.tsx` — replace raw key renders with `getIndicatorDisplayName(framework, key)` calls

---

## Area 4 — Mandatory Ecological Note: Zone 3 Expandable

### Binding decision (information-hierarchy.md)

> The mandatory ecological note moves to Zone 3A — a collapsed "(i)" expandable. Zone 3A is deliberate navigation: the note is always accessible but requires a click to expand. The ecological composite score remains Zone 1B (radar chart axis). The note explains the methodology; it does not replace the score.

### Current code state

The ecological note is currently rendered inline in the ecological framework panel (Zone 2). This violates the M8 Zone 3A assignment once the ecological axis has real data. Issue #266 is the gap.

### Required architecture

The Zone 3A expandable is a generic pattern applicable beyond ecological notes. Implement it as a reusable component: `frontend/src/components/MethodologyNote.tsx`

```typescript
interface MethodologyNoteProps {
  label: string;           // e.g., "Ecological methodology note"
  children: React.ReactNode;
}
```

Renders as: `(i) Ecological methodology note ▼` (collapsed) → full note text (expanded on click). No animation required — this is Zone 3, and the user has navigated deliberately. A simple CSS `display: none / block` toggle is sufficient.

The ecological note text (ADR-005 M8-6 compliance requirement: explain planetary boundary normalization formula and cap-at-2.0 discriminating-power limitation) must be included as the note content when Issue #266 is implemented.

### Affected files

1. `frontend/src/components/MethodologyNote.tsx` — new generic expandable
2. `frontend/src/components/FrameworkPanel.tsx` — replace inline ecological note with `<MethodologyNote>` wrapper; note content is props, not hardcoded in the component

### ADR compliance note

ADR-005 M8-1 must-resolve finding: "cap-at-2.0 discriminating-power loss [is] undisclosed." The Zone 3A ecological note is where this disclosure lives. The note must include: the normalization formula (`min(current_value / boundary_value, 2.0)`), the meaning of values >1.0 (boundary exceeded), and the discriminating-power limitation above 2.0. This disclosure is not optional — it is a must-resolve ADR panel finding.

---

## Area 5 — Radar Chart Step Transition Animation

### Binding decision (information-hierarchy.md)

> Radar chart polygon transitions between steps use 200–300ms ease-in-out animation. `prefers-reduced-motion` must disable the animation. Ownership: Frontend Architect Brief (this document) → Implementation Agent.

### Current code state

`RadarChart.tsx` uses Recharts `<Radar>` component with no animation configuration. Recharts has built-in animation via `isAnimationActive` and `animationDuration` props on the `<Radar>` element.

### Required change

```typescript
// In RadarChart.tsx <Radar> element:
<Radar
  name="Framework scores"
  dataKey="final_score"
  stroke="#1a6eb5"
  fill="#1a6eb5"
  fillOpacity={0.25}
  isAnimationActive={!prefersReducedMotion}
  animationDuration={250}
  animationEasing="ease-in-out"
  dot={...}
/>
```

`prefersReducedMotion` must be read from the browser's `prefers-reduced-motion` media query. Implement as a React hook: `frontend/src/hooks/usePrefersReducedMotion.ts`

```typescript
export function usePrefersReducedMotion(): boolean {
  const [prefersReduced, setPrefersReduced] = useState(
    () => window.matchMedia("(prefers-reduced-motion: reduce)").matches
  );
  useEffect(() => {
    const mq = window.matchMedia("(prefers-reduced-motion: reduce)");
    const handler = (e: MediaQueryListEvent) => setPrefersReduced(e.matches);
    mq.addEventListener("change", handler);
    return () => mq.removeEventListener("change", handler);
  }, []);
  return prefersReduced;
}
```

### Constraint: animation must not apply during null-to-active transition

When a governance axis transitions from null (dashed, M8 placeholder) to active (data available, future milestone), the polygon interpolation from `null → number` is undefined in Recharts. Disable animation for any frame where `composite_score` transitions from `null`. Implementation agents must guard this case.

### Affected files

1. `frontend/src/hooks/usePrefersReducedMotion.ts` — new hook
2. `frontend/src/components/RadarChart.tsx` — consume hook, apply to `<Radar>` props

---

## Implementation Sequencing

The five areas have a dependency ordering that implementation agents must follow:

```
Area 1 (type fix + null rendering)
  └── Area 5 (animation) — must build on top of the number | null type
Area 3 (display name registry) — independent, can run in parallel with Area 1
Area 4 (Zone 3 expandable) — independent, can run in parallel with Area 1
Area 2 (PMM widget) — independent; placeholder render only in M8
```

**No implementation PR for Area 5 opens before Area 1 merges.** The `chartData` mapping in `RadarChart.tsx` that Area 5 modifies must already handle `number | null` before animation is added.

Areas 2, 3, 4 can be implemented in any order relative to each other and in parallel with Area 1.

---

## Cross-ADR Obligations Summary

| Obligation | Source | Same-commit requirement |
|---|---|---|
| `RadarAxisDatum.composite_score: number → number | null` | ADR-005 panel synthesis M8-5 | Yes — type change + null render + ADR-005 Decision 4 update in one commit |
| Ecological note discloses cap-at-2.0 limitation | ADR-005 panel synthesis M8-1 | Note content is the disclosure — must include the formula and limitation text |

---

## UX Designer Sign-off Required

Per `docs/process/agents.md`: UX Designer sign-off is required on all Frontend Architect briefs before implementation begins. The UX Designer must confirm:

1. The null governance axis dashed outline and "—" label satisfy the Zone 1B null ≠ zero requirement.
2. The PMM Zone 1C widget placement (between MDA panel and radar chart) is consistent with the Zone hierarchy.
3. The Zone 3A expandable "(i)" pattern for the ecological note is consistent with Zone 3 deliberate-navigation intent.
4. The 200–300ms animation duration is consistent with the information hierarchy's motion guidance.

**Implementation does not begin until UX Designer sign-off is recorded below.**

---

**UX Designer sign-off — 2026-05-17**

All four criteria confirmed against `docs/ux/information-hierarchy.md` M8 Hierarchy Decisions table (binding):

1. **Null axis rendering (Area 1):** Confirmed. Hierarchy §1B: "null axes must be visually distinct from zero-value axes | Distinct treatment (e.g., dashed outline, '—' label)." The dashed outline + "—" label is the reference implementation from the hierarchy document itself.

2. **PMM Zone 1C placement (Area 2):** Confirmed. Hierarchy §1C positions PMM as the dedicated Zone 1 widget. The ordering MDA (1A) → Radar (1B) → PMM (1C) is the canonical Zone 1 stack.

3. **Ecological note Zone 3A (Area 4):** Confirmed. Hierarchy §3A: "Methodology notes are Zone 3 | Collapsed by default, accessible via (i)." The collapsed "(i)" pattern is the reference implementation. ADR-005/006 compliance is maintained — note is present and accessible.

4. **200–300ms animation (Area 5):** Confirmed. Hierarchy §2B (M8 decisions table): "Radar chart step transitions are animated | 200–300ms ease-in-out." The deformation across steps must be observable. `prefers-reduced-motion` disable is required — a user who has opted out of motion must not have this forced on them.

**Sign-off: UX Designer Agent. Implementation may proceed in dependency order specified in §Implementation Sequencing.**
