---
name: m17-g4-1250-zone-1b-tablet-legibility
type: ux-visual-spec
issue: "#1250"
sprint-entry: docs/process/sprint-plans/m17-g4-sprint-entry.md
authored-by: UX Designer Agent
authored-date: 2026-06-25
governing-documents:
  - docs/ux/information-hierarchy.md §Zone 1 — Primary
  - CLAUDE.md §UX Architectural Commitments (premise 2)
  - CLAUDE.md §Architectural Principles — Equitable Build Process (item 5)
---

# UX Visual Spec — M17-G4 Issue #1250: Zone 1B Tablet Legibility at 768px

**Decision: Increase CohortImpactSection font sizes at ≤ 1023px viewport width
via a local breakpoint hook in `CohortImpactSection`. No change to Zone 1B layout
structure or any existing component at wider viewports.**

---

## 1. Problem Statement

DEMO6-026/043: At 768px viewport width (tablet, or presenter display at reduced resolution),
Zone 1B CohortImpactSection cohort crossing rows are rendered at very small font sizes
(row: 10px, severity badge: 9px, tier badge: 8px, sublabel: 7px). These sizes are
unreadable at tablet viewing distance during a live demo.

**Equitable access principle:** Demo presentations may occur on shared or tablet devices
at 768px viewport width. Zone 1B must be legible at this viewport width for the demo
to serve Persona 2 (Aicha Mbaye — finance ministry negotiator).

---

## 2. Decision: Conditional Font Sizes at ≤ 1023px

**Chosen approach:** In `CohortImpactSection`, add a local breakpoint check using
`useViewportBreakpoint()` (which returns 1024 for all viewports < 1280px, including
768px). When the breakpoint is 1024, apply the increased font sizes defined below.

**Rejected: CSS media queries** — components use inline styles throughout; adding a
`<style>` block or external CSS for one component introduces an inconsistent pattern.

**Rejected: changing the shared `useViewportBreakpoint` hook** — the hook serves
InstrumentCluster layout allocation. Its existing 1024 return covers 768px already.
CohortImpactSection can consume it directly without changes.

---

## 3. Required Font Sizes

### At ≤ 1023px viewport (breakpoint returns 1024)

| Element | Current size | Required size at ≤1023px | testid anchor |
|---|---|---|---|
| Row container | 10px | **11px** | (parent div of cohort row) |
| Severity badge | 9px | **10px** | (first `<span>` in row) |
| Tier badge | 8px | **10px** | `cohort-tier-badge-{indicator_key}` |
| Tier sublabel | 7px | **9px** | `confidence-tier-badge-sublabel` |

### At ≥ 1280px viewport (breakpoint returns 1280 or 1440)

All current sizes unchanged:
| Element | Size |
|---|---|
| Row container | 10px |
| Severity badge | 9px |
| Tier badge | 8px |
| Tier sublabel | 7px |

---

## 4. Before / After Mockup

### Zone 1B CohortImpactSection — 768px viewport, BEFORE

```
Zone 1B at 768px viewport width

  Zone 1B — MDA Alert Panel
  ┌──────────────────────────────────┐
  │ CRITICAL  Q1 Informal — poverty  │  ← row: 10px (tiny at 768px)
  │           Crossed step 1 ·       │
  │           3.50% below floor ·T3  │  ← tier badge: 8px (very hard to read)
  │                       No primary │  ← sublabel: 7px (illegible)
  └──────────────────────────────────┘

  At tablet viewing distance, "T3" and "No primary data" are illegible.
  Severity badge "CRITICAL" at 9px is strained.
```

### Zone 1B CohortImpactSection — 768px viewport, AFTER

```
Zone 1B at 768px viewport width

  Zone 1B — MDA Alert Panel
  ┌──────────────────────────────────┐
  │ CRITICAL  Q1 Informal — poverty  │  ← row: 11px
  │           Crossed step 1 ·       │
  │           3.50% below floor · T3 │  ← tier badge: 10px (legible)
  │                   No primary data│  ← sublabel: 9px (readable)
  └──────────────────────────────────┘

  Legible at tablet viewing distance. No layout change — same structure.
```

### Zone 1B at 1280×800 — NO CHANGE (regression guard)

```
Zone 1B at 1280×800 (primary presentation viewport)

  Current font sizes unchanged:
  row: 10px | severity badge: 9px | tier badge: 8px | sublabel: 7px
```

---

## 5. Testid-Anchored Layout Description for QA Lead

The following testids have measurable font sizes that QA can assert:

| testid | At ≤1023px | At ≥1280px |
|---|---|---|
| `cohort-tier-badge-{indicator_key}` | fontSize ≥ 10px | fontSize ≥ 8px |
| `confidence-tier-badge-sublabel` | fontSize ≥ 9px | fontSize ≥ 7px |

The row container and severity badge do not have explicit testids — their font sizes
are not directly assertable by Playwright. The QA AC for #1250 focuses on the
testid-anchored elements above.

---

## 6. Regression Contract

- Only `CohortImpactSection` font sizes change at the 1024 breakpoint
- Zero changes at 1280×800 or 1440px viewports — existing tests at those viewports pass without modification
- The `confidence-tier-badge-sublabel` testid is retained (it must be present post-fix)
- No layout structure changes: row flex layout, badge positioning, indicator label display are unchanged

---

## 7. Implementation Notes for Frontend Engineer

In `CohortImpactSection` (`MDAAlertPanelZone1B.tsx`):

```typescript
// Add near top of CohortImpactSection:
const bp = useViewportBreakpoint();
const is768 = bp === 1024; // covers all viewports < 1280px, including 768px

// Apply conditional font sizes:
// Row container: fontSize: is768 ? 11 : 10
// Severity badge: fontSize: is768 ? 10 : 9
// Tier badge: fontSize: is768 ? 10 : 8
// Tier sublabel: fontSize: is768 ? 9 : 7
```

`useViewportBreakpoint` is already imported from `InstrumentCluster.tsx`
(check import path — it may be in a shared utils file). If not exported, it
can be extracted to a shared hook or inlined as a simple `useWindowWidth` hook
in `CohortImpactSection`.

The implementing agent must confirm `useViewportBreakpoint` is importable from
`CohortImpactSection`'s file location before implementing. If import requires
refactoring, a simple local version is acceptable:

```typescript
function useIsNarrow(): boolean {
  const [narrow, setNarrow] = useState(window.innerWidth < 1280);
  useEffect(() => {
    const handler = () => setNarrow(window.innerWidth < 1280);
    window.addEventListener("resize", handler);
    return () => window.removeEventListener("resize", handler);
  }, []);
  return narrow;
}
```
