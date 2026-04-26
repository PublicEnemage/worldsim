# Component Standards — WorldSim Frontend

> Binding standards for all React components in `frontend/src/`. Owned by the
> UI/Frontend Architect Agent. Applies from M5 onward; M4 components are legacy
> and will be migrated incrementally per modularization-strategy.md.

---

## File Organization

```
frontend/src/
  components/       — React UI components
  hooks/            — custom React hooks
  types.ts          — all TypeScript API response and domain types
  App.tsx           — root orchestrator
  App.css           — global layout styles
  main.tsx          — React entry point
```

Rules:
- One default export per file.
- Internal sub-components that are not used outside the file may be
  co-located in the same file.
- Component filenames: `PascalCase.tsx`.
- Hook filenames: `useCamelCase.ts` — must start with `use`.
- No `index.ts` barrel files. Import by full path.

---

## Component Anatomy

Every component follows this structure:

```tsx
// 1. Imports — external, then internal
import { useState } from "react";
import type { MyType } from "../types";
import styles from "./MyComponent.module.css";  // M5+ components

// 2. Local constants (not exported)
const MAX_ITEMS = 50;

// 3. Local sub-components (not exported)
function SubComponent({ ... }: { ... }) { ... }

// 4. Props interface (always named Props)
interface Props {
  requiredProp: string;
  optionalProp?: number;
  onEvent: (value: string) => void;
}

// 5. Default export — component function (named, matches filename)
export default function MyComponent({ requiredProp, optionalProp = 0, onEvent }: Props) {
  // state
  const [localState, setLocalState] = useState(false);

  // effects
  useEffect(() => { ... }, [deps]);

  // derived values
  const isVisible = localState && requiredProp.length > 0;

  // event handlers
  const handleClick = () => { onEvent(requiredProp); };

  // render
  return ( ... );
}
```

---

## Styling Rules

### M5+ New Components: CSS Modules

All new components from M5 onward must use CSS modules:

```tsx
import styles from "./MyComponent.module.css";
// Usage: className={styles.container}
```

Do not add new inline styles. Do not add new global CSS classes.

### M4 Legacy Inline Styles

Existing M4 components use inline styles. Do not migrate them mid-feature —
migrate as a dedicated CSS module PR when a component is touched for functional
reasons. Do not mix inline styles and CSS modules in the same component.

### Style Constraints

- No z-index above 100 without a comment explaining the stacking context.
  Current z-indices: EntityDetailDrawer = 10.
- No `!important`.
- Responsive layout: the application assumes a desktop viewport (minimum 1024px
  wide). Mobile layout is not in scope before M7.

---

## Props Contract Rules

- Required props come first; optional props last.
- Callback props start with `on`: `onClick`, `onStepChange`, `onClose`.
- Boolean props avoid negation: `disabled` not `notEnabled`.
- Do not pass raw object literals as default prop values — they create new
  references on every render and defeat memoization. Use `useState(defaultValue)`
  or module-level constants.
- Do not spread unknown props (`{...rest}`). Be explicit.

---

## State Rules

- `useState` initialization value runs only once. If you need state to
  re-initialize when a prop changes, use a `useEffect` that watches the specific
  prop — but only if watching that prop will not fire more often than intended.
  See DD-004 in design-decisions.md for the canonical anti-pattern.
- Never use `useState` for values that can be derived synchronously from props
  or other state. Compute them in the render body.
- `useRef` for: MapLibre instances, mutable values that must not trigger re-renders,
  stable callback refs to avoid stale closures.

---

## Effect Rules

- Every `useEffect` that does async work must use the `cancelled` flag pattern.
- Dependency arrays must be accurate and complete. Do not silence ESLint's
  `exhaustive-deps` rule with `// eslint-disable-line` without a comment.
- Effects that initialise external resources (MapLibre, third-party libraries)
  must clean up in the return function.

---

## Type Rules

- All API response shapes in `types.ts`. One interface per API response shape.
- `Decimal`-as-string values typed as `string`. No `number` for monetary or
  Quantity values from the API.
- Avoid `any`. Use `unknown` and narrow explicitly. If a third-party library
  forces `any`, scope it to the minimum surface and add a comment.
- `Record<string, unknown>` is acceptable for open-ended API metadata fields.

---

## Accessibility Baseline

- All interactive elements have either visible text content or `aria-label`.
- Buttons that are icon-only (e.g. close ✕) must have `aria-label`.
- `<select>` elements must have an associated `<label>` or `aria-label`.
- Color must not be the only indicator of state (e.g. MDA severity is
  communicated via badge text and color, not color alone).

Full WCAG compliance is a M7 deliverable. These rules are the M5 baseline.

---

## Performance Constraints

- Do not import a full library when a subset would do. Example: import specific
  Recharts components, not the entire library.
- MapLibre layers must be removed before being re-added. Never accumulate layers.
- Avoid calling `JSON.parse` or `JSON.stringify` in render functions.
  Serialize/deserialize in effects or event handlers.
- `useCallback` and `useMemo` are not required by default. Add them only when
  profiling confirms a performance problem, not preemptively.
