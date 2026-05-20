# ARCH-REVIEW-M8-socratic-test — M8 Socratic Architecture Test

**Date:** 2026-05-19
**Authored by:** Socratic Agent
**Scope:** Three M8 architectural areas — ecological composite strategy dispatch,
null governance axis rendering, demo spec test seam.
**Method:** Three probing questions per area; correct answers; PASS/FAIL verdict.
**Reading basis:** `backend/app/api/scenarios.py`, `backend/app/simulation/modules/ecological/module.py`,
`frontend/src/components/RadarChart.tsx`, `frontend/src/App.tsx`,
`frontend/tests/e2e/demo-narrated.spec.ts`, `frontend/playwright.config.ts`,
`frontend/playwright.demo.config.ts`, `SESSION_STATE.md §Architectural State`.

---

## Area 1 — Ecological Composite Strategy Dispatch

### Question 1

> `_compute_composite_score()` in `backend/app/api/scenarios.py` has three branches.
> Name them in dispatch order and state which framework lands in each branch.

**Correct answer:**

Branch 1 — Registered strategy (`if framework in _COMPOSITE_STRATEGIES`): fires for
`"ecological"`. Calls `_boundary_proximity_strategy` after fetching active boundary
constants from `simulation_reference_constants` via `_fetch_active_boundary_constants()`.

Branch 2 — Validated percentile-rank framework (`elif framework in _PERCENTILE_RANK_VALIDATED_FRAMEWORKS`):
fires for `"financial"` and `"human_development"`. Calls `_percentile_rank_strategy`
directly with no additional context fetching.

Branch 3 — Unknown framework (`else`): fires for any framework not in either set — currently
`"governance"` (M9 deferred per Decision M8-4). Emits a `[SIM-INTEGRITY]` WARNING, then
falls back to `_percentile_rank_strategy`.

---

### Question 2

> `[SIM-INTEGRITY]` WARNING appears in several locations in the M8 ecological code.
> Name every condition that triggers it in the composite score path and state what
> it signals in each case.

**Correct answer:**

Three distinct trigger conditions in the composite path:

1. **Unknown framework in `_compute_composite_score()`** (`scenarios.py:1029`): framework is not
   in `_COMPOSITE_STRATEGIES` and not in `_PERCENTILE_RANK_VALIDATED_FRAMEWORKS`. Signals that
   governance (or any future unregistered framework) is falling back to percentile rank without
   a validated methodology. This warning is expected at M8 for `"governance"`.

2. **Boundary constant absent at simulation time in `_boundary_proximity_strategy()`**
   (`scenarios.py:959`): a proximity indicator key is in `_ECOLOGICAL_INDICATOR_BOUNDARY_CONFIG`
   but its `boundary_constant_id` is NOT in the `boundary_constants` dict fetched from the DB.
   Signals that either migration `c1a4e7f2d9b3` (confidence_tier) or `b3c5d7e9f1a2`
   (reference constants seed) has not run, OR the simulation timestep predates the constant's
   `effective_from`. The indicator is excluded from the composite.

3. **Base stock attribute absent from `_compute_proximity_indicators()` in `module.py`**
   (`module.py:148`): `entity.attributes.get(base_key)` returns `None`. Signals that the
   EcologicalModule has not yet accumulated a stock reading for this entity — typically
   the first step before any ecological event has propagated. The proximity indicator is
   skipped for that step.

A fourth trigger — boundary constant temporally inactive — appears as a WARNING in
`_compute_proximity_indicators()` (`module.py:137`) when `timestep < effective_from`
for a configured boundary constant (relevant for `planetary_boundary_land_use_proximity`
before 2023-09-13).

---

### Question 3 (two parts)

> (a) Why is ecological exempt from the single-entity guard that suppresses composite scores
> for financial and human development?
>
> (b) What is the STOCK delta path contract for `co2_concentration_ppm`? State the exact
> value that is emitted and why emitting the raw elasticity delta would corrupt the scenario.

**Correct answers:**

**(a) Single-entity exemption:**

Percentile rank is meaningless for a single entity — it requires a distribution of ≥2 entities
to produce a valid rank. In a single-entity Greece scenario, financial and human development
composite scores are suppressed (`is_single_entity and fw not in _SINGLE_ENTITY_GUARD_EXEMPT_FRAMEWORKS`
at `scenarios.py:1171`). Ecological boundary proximity is physically meaningful for a single
entity because it measures how close the entity is to an absolute planetary threshold —
boundary proximity is not a relative rank, it is an absolute ratio. A single country's
CO2 trajectory relative to 350 ppm is a well-defined quantity regardless of how many other
entities are in the scenario. This is documented in ADR-005 Amendment 3 Decision M8-2 and
enforced via `_SINGLE_ENTITY_GUARD_EXEMPT_FRAMEWORKS = frozenset({"ecological"})`.

**(b) STOCK delta path contract:**

`co2_concentration_ppm` is `VariableType.STOCK`. The propagation engine **replaces** STOCK
attributes — it does not accumulate deltas. Therefore the EcologicalModule must emit the
new **absolute level** (`current_val + delta`), not the raw elasticity delta.

The code path (`module.py:267–274`):
```python
current_qty = entity.attributes.get(key)
current_val = (Decimal(str(current_qty.value)) if current_qty is not None else Decimal("0"))
emit_value = current_val + delta
```

If the raw delta (`~−0.08 ppm` for a contraction step) were emitted, the propagation engine
would write `−0.08` into `co2_concentration_ppm`, overwriting the 388 ppm NOAA MLO 2010 seed.
All subsequent proximity computations (`co2_concentration_ppm / 350`) would produce a small
negative fraction rather than `~1.11` — silently corrupting the ecological composite for
every remaining step. This fix is recorded in SESSION_STATE.md §Key Decisions ("EcologicalModule
delta path bug fixed, PR #328").

**Area 1 verdict: PASS**

---

## Area 2 — Null Governance Axis Rendering

### Question 1

> What is the exact string value of `GOVERNANCE_IN_VALIDATION_LABEL` as it appears in the
> source? Why is it an exported constant rather than an inline string?

**Correct answer:**

```
"Governance — in validation"
```

The dash is an **em dash** (`—`, U+2014), not a hyphen or en dash. The exact value matters
because it is the text displayed on the radar axis label and narrated in the demo spec
(`demo-narrated.spec.ts:424`).

It is an exported constant because ADR-005 Decision M8-5 requires text changes to have a
corresponding ADR amendment (see design-decisions.md DD-011). Exporting the constant (a)
makes it referenceable in tests without string duplication, (b) ensures a lint-visible
dependency that forces test updates when the text changes, and (c) prevents accidental
divergence between label text and tooltip text.

---

### Question 2

> Describe every visual difference between a `composite_score = null` axis and a
> `composite_score = 0.0` axis in the rendered radar chart — label, dot, polygon vertex,
> tooltip, and animation.

**Correct answer:**

| Property | `composite_score = null` | `composite_score = 0.0` |
|---|---|---|
| Axis label | `"Governance — in validation"` | `"Governance"` (or `FRAMEWORK_LABELS["governance"]`) |
| Dot | Hollow dashed circle: `fill="none"`, `stroke="#aaa"`, `strokeDasharray="2 2"`, `r=4` | Filled blue circle: `fill="#1a6eb5"`, `stroke="#0d4f8a"`, `r=4` |
| Polygon vertex | **Absent** — Recharts skips null dataKey values, leaving a gap in the polygon | Present at the polygon center (origin) |
| Tooltip | Shows `GOVERNANCE_IN_VALIDATION_TOOLTIP` with explanation and promotion criteria | Shows `"0%"` |
| Animation | Disabled — `animationActive` is false when `hasNullAxis` is true (null→number interpolation is undefined in Recharts) | Animation active if `!prefersReducedMotion` |

The distinction between null and 0.0 is semantically critical: 0.0 would imply governance
failure (score at the MDA floor); null means the composite was not computed (no methodology
yet). The design-decisions sentinel DD-011 documents this distinction.

---

### Question 3

> What does `computeFinalScore(null, 1.0)` return? Trace the code path. What does Recharts
> render when a `Radar` component's `dataKey` value is `null` on a polygon vertex?

**Correct answer:**

`computeFinalScore(null, 1.0)` returns **`null`**.

Code path (`RadarChart.tsx:37–43`):
```typescript
export function computeFinalScore(composite_score: number | null, weight: number): number | null {
  if (composite_score === null) return null;
  return Math.min(1, composite_score * weight);
}
```

The null check fires immediately; the multiplication branch is never reached.

In the `chartData` mapping:
```typescript
const final_score = computeFinalScore(d.composite_score, weight);
return { ...d, final_score };  // final_score: null for governance
```

Recharts `<Radar>` with `dataKey="final_score"` receives `null` for the governance vertex.
Recharts treats null as a missing data point on a polygon — it **does not draw a line segment
to that vertex** and **does not fill the polygon area** at that point. The result is a
three-sided filled polygon (financial, human_development, ecological) with an open gap where
governance would be. This is the "honest null" rendering — the radar visually signals absence
of data, not presence of a zero score.

**Area 2 verdict: PASS**

---

## Area 3 — Demo Spec Test Seam

### Question 1

> What are `__worldsim_selectEntity` and `__worldsim_setAttributeName`? State where they are
> defined, what they expose, under what condition they are available, and why they exist
> rather than using Playwright's standard locator-based click.

**Correct answer:**

Both are `window`-level globals attached in `App.tsx` inside a `useEffect`:

```typescript
// frontend/src/App.tsx:52–58
useEffect(() => {
  if (!import.meta.env.DEV) return;
  (window as unknown as Record<string, unknown>).__worldsim_selectEntity = (id: string) =>
    setSelectedEntityId(id);
  (window as unknown as Record<string, unknown>).__worldsim_setAttributeName = (key: string) =>
    setAttributeName(key);
}, [setSelectedEntityId, setAttributeName]);
```

`__worldsim_selectEntity(id)` calls `setSelectedEntityId` — opens the entity analysis
drawer for the given entity ID (e.g. `"GRC"`).

`__worldsim_setAttributeName(key)` calls `setAttributeName` — switches the choropleth
to display a different indicator (e.g. `"gdp_growth"`).

**Availability:** DEV mode only. The `if (!import.meta.env.DEV) return` guard means the
globals are **never attached in production builds** (Vite's tree-shaking eliminates the dead
branch entirely from a `vite build` output).

**Why they exist:** The choropleth is rendered on a WebGL canvas (Maplibre GL). Playwright
cannot reliably click specific geographic features on a WebGL canvas in headless Chromium
because the exact pixel coordinate of "Greece" depends on the current map zoom level,
pan position, and projection — all variable across test runs. By exposing the React state
setter directly as a `window` function, the spec can trigger the drawer open via
`page.evaluate(() => window.__worldsim_selectEntity("GRC"))` without canvas interaction.
The spec waits for the globals to be present before proceeding (`page.waitForFunction`).

---

### Question 2

> Why is `demo-narrated.spec.ts` excluded from CI test runs? State the exact mechanism
> that excludes it, not just the reason.

**Correct answer:**

`demo-narrated.spec.ts` is tagged with `{ tag: ["@demo"] }` at the test declaration
(`demo-narrated.spec.ts:97`).

The CI Playwright config (`playwright.config.ts:11`) sets:
```typescript
grep: /^(?!.*@demo)/,
```

This regex **matches only test titles that do NOT contain `@demo`** (negative lookahead).
Playwright's `grep` option filters tests by title; a test with `{ tag: ["@demo"] }` has
`@demo` appended to its effective title for grep matching. The demo spec therefore does
not match the `grep` pattern and is never collected by the CI runner.

The `playwright.demo.config.ts` has no `grep` option, so it collects all tests in
`testDir: "./tests/e2e"` — it runs the demo spec explicitly when invoked with
`--config playwright.demo.config.ts`.

The reasons the exclusion is warranted:
- Requires a live stack (`docker compose up`) — CI runs unit and integration tests without
  the full compose stack
- Requires macOS TTS (`scripts/speak.sh` calls `say`) — CI runs on Ubuntu GitHub Actions runners
- Test timeout is 20 minutes (`test.setTimeout(20 * 60 * 1000)`) — CI has strict time budgets

---

### Question 3

> What does `playwright.demo.config.ts` configure differently from `playwright.config.ts`,
> and why does each difference exist?

**Correct answer:**

| Configuration | `playwright.config.ts` (CI) | `playwright.demo.config.ts` (Demo) | Why |
|---|---|---|---|
| `headless` | `true` | `false` | Demo requires visible browser for screen recording |
| `slowMo` | not set | `800` | 800 ms between actions paces the demo for presenter narration |
| `timeout` | `30_000` | `60_000` | Demo has live TTS pauses that exceed the CI timeout |
| `viewport` | `1280×720` | `1440×900` | Wider viewport for more legible demo recording |
| `--start-fullscreen` | not set | set | Hides address bar, tab strip, OS chrome — recordings show only the app |
| `--hide-crash-restore-bubble` | not set | set | Suppresses Chromium's session-restore prompt after a prior killed run |
| `reporter` | `html + list` | `list` only | No HTML report needed for demo runs; just stdout per step |
| `grep` | `/^(?!.*@demo)/` | not set (all tests) | CI excludes `@demo`; demo config collects `@demo` tests |

The demo config is invoked by `scripts/demo.sh --run` or directly:
```
cd frontend && npx playwright test tests/e2e/demo-narrated.spec.ts \
  --config playwright.demo.config.ts --headed
```

The M6-era equivalent (`demo-narrated-m6.spec.ts`) is archived; the demo config now targets
the M8 spec by path convention.

**Area 3 verdict: PASS**

---

## Summary

| Area | Verdict | Notes |
|---|---|---|
| Area 1 — Ecological composite strategy dispatch | **PASS** | Three-branch dispatch, [SIM-INTEGRITY] triggers, single-entity exemption rationale, STOCK delta path contract all correctly documented in source |
| Area 2 — Null governance axis rendering | **PASS** | Exact label string (em dash), visual distinction null vs 0.0, computeFinalScore null propagation, Recharts polygon gap — all confirmed in RadarChart.tsx |
| Area 3 — Demo spec test seam | **PASS** | Window globals DEV-only, exact grep exclusion mechanism, full config diff rationale — all confirmed in App.tsx + playwright configs |

**Overall: PASS — M8 architectural implementation is consistent with session records and
source code. No gaps or discrepancies identified between SESSION_STATE.md, ADR-005 Amendment 3,
and the live code in `scenarios.py`, `module.py`, `RadarChart.tsx`, and the demo spec.**
