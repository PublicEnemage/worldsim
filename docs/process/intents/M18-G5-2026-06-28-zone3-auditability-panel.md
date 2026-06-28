---
name: M18-G5-zone3-auditability-panel
type: implementation-intent
issue: "#1422"
status: Filed — QA tests required before implementation PR opens
authored-by: PM Agent
authored-date: 2026-06-28
implementing-agent: Frontend Architect Agent (frontend); Computation Engine Agent (backend)
sprint-entry: "docs/process/sprint-plans/m18-g5-sprint-entry.md — EL-approved 2026-06-28"
adr-reference: "None — Zone 3 auditability panel is a click/expand interaction within existing Zone 1B surface. Falls within ADR-014 (Zone 1B information architecture) and ADR-018 (Zone 1B proportional allocation) scope. Architect determination: no new ADR required — documented in G3 sprint exit §3 CA condition."
governing-adrs:
  - "ADR-014 (Zone 1B information architecture — ACCEPTED) — Zone 1B surface and content model"
  - "ADR-018 (Zone 1B proportional allocation — ACCEPTED) — Sub-zone B CohortImpactSection pattern"
  - "ADR-007 (Synthetic data framework — ACCEPTED) — T3 tier classification and CI band methodology"
release-branch: release/m18
bpo-acceptance-required: "Yes — user-facing Zone 1B interaction"
customer-agent-l3-required: "Yes — Persona 1 (Lucas) at sprint exit"
schema-prerequisite: "docs/schema/api_contracts.yml must be updated with methodology_detail field before implementation PR opens"
sprint-journal: "#1435"
---

# Implementation Intent: M18-G5 — Zone 3 Auditability Panel for DistributionalComparisonSummary (#1422)

> **Pre-implementation prerequisites:**
> - [ ] `docs/schema/api_contracts.yml` updated with `methodology_detail` field in `DistributionalDifferentialResponse` — required in same PR as backend implementation
> - [ ] `frontend/tests/e2e/m18-g5-zone3-auditability.spec.ts` authored (red before implementation) — **required before implementation PR opens**
> - [x] Architect determination on record: no new ADR required (G3 sprint exit §3 CA condition)
> - [x] Backend data constants verified in `backend/app/api/scenarios.py`: `_ENTITY_Q1_POPULATION`, `_DISTRIBUTIONAL_TIER`, `_DISTRIBUTIONAL_METHODOLOGY` exist and can be used to populate `methodology_detail`

---

## 0. Implementation Constraints

*These constraints follow from the G3 CA condition specification (G3 sprint exit §3) and the
existing Zone 1B architecture. They are not design preferences.*

1. **Expand/collapse surface only.** The Zone 3 panel is an in-place expand/collapse on
   `DistributionalComparisonSummary`. It is NOT a modal, drawer, tooltip, or navigation target.
   Lucas reads the panel without leaving Zone 1B. The Zone 1 (always-visible) content —
   headline differential, CI band, direction disclosure — must remain visible when the panel is
   collapsed AND when it is expanded.

2. **Backend must enrich the response.** The `methodology_summary` string in the current
   `DistributionalDifferentialResponse` does not include the entity-specific Q1 population
   value or the extraction path. A `methodology_detail` object must be added to the response
   (new field on the existing endpoint — no new endpoint). The frontend must not hardcode
   values that come from the backend data model.

3. **Schema-first.** `docs/schema/api_contracts.yml` must be updated with the
   `methodology_detail` field in the same PR as the backend implementation. The store type
   `DistributionalSummaryData` in `frontend/src/store/scenarioStepStore.ts` must be updated
   in the same PR as the frontend implementation. Schema drift is a compliance violation.

4. **No Zone 1 displacement.** The panel toggle and the expanded panel must not push the
   headline differential or direction disclosure out of the viewport at 1280×800. If space is
   constrained, the panel expands upward (bottom: sticky) or overlays — it does not reflow the
   parent container. Implementation must verify at 1280×800 that Zone 1 content stays visible.

5. **NM-076 crosscheck.** All new `data-testid` values introduced by this implementation must
   be cross-referenced against the full E2E corpus (`grep -r 'new-testid' frontend/tests/e2e/`)
   before the PR opens, to confirm no existing test references a testid being introduced or
   conflicting. Per the NM-076 process improvement being landed in CODING_STANDARDS.md in G5.

---

## 1. Source

**Issue:** #1422 — feat(demo7): Zone 3 auditability panel for DistributionalComparisonSummary (#1349 CA condition)

**CA condition origin:** G3 sprint exit §3 (CA condition — Lucas, Persona 1). BPO validation
at `#1349#issuecomment-4826830111`. The G3 BPO accepted the distributional comparison summary
(US-1349-A through US-1349-C) unconditionally, with #1422 filed as a capacity-allowing CA
condition for US-1349-D (Lucas auditability path).

**Demo 7 relevance:** The live external session (#843) is the pressure point. If the IMF
analytical team challenges the 340,000 headcount figure during the session, Lucas needs to open
the methodology panel and answer in the room. Without the panel, the T3 badge is an epistemic
signal with no substantive backing accessible to the analyst without leaving the primary
viewport.

**What already exists (G3 delivery):**
- `DistributionalComparisonSummary` component in `MDAAlertPanelZone1B.tsx` (lines 710–788)
  — renders headline differential, CI band, direction disclosure
- `data-testid="distributional-comparison-summary"` — outer wrapper
- `data-testid="comparison-tier-badge"` — T3 badge (epistemic proxy)
- `data-testid="direction-stability-disclosure"` — direction line
- `methodology_summary: string` field in `DistributionalSummaryData` store type (line 127
  of `scenarioStepStore.ts`) and in the backend `DistributionalDifferentialResponse`
- `_DISTRIBUTIONAL_TIER = "T3"` and `_DISTRIBUTIONAL_METHODOLOGY` constants in
  `backend/app/api/scenarios.py` (lines 2794–2799)
- `_ENTITY_Q1_POPULATION = {"ZMB": 3_894_625, ...}` (line 2784)

**What G5 adds:**
- `methodology_detail` field in `DistributionalDifferentialResponse` (backend)
- `methodology_detail` field in `DistributionalSummaryData` store type (frontend)
- Expand/collapse toggle on `DistributionalComparisonSummary` with `data-testid="methodology-panel-toggle"`
- Expanded methodology panel with 4 named fields and individual testids

---

## 2. Persona Trace

**P-1 — Personas served:**

| Persona | Entry state | Role in G5 |
|---|---|---|
| Lucas Ferreira (Persona 1 — Programme Analyst) | Preparatory — building analytical record for programme review | Primary user. Opens methodology panel; reads 4 fields; can defend the 340,000 figure under IMF peer scrutiny without consulting external documentation. |
| Eleni Papadimitriou (Persona 2 — Finance Ministry Negotiator) | Active Negotiation | Not a primary G5 user — Eleni reads the headline number (Zone 1). The panel is available if the IMF challenges methodology, but Eleni's 90-second ceiling does not depend on it. |

**P-2 — Entry states and time ceilings:**

- Lucas (Preparatory): no strict time ceiling; needs full auditability access
- The panel is not required for Persona 2 or Persona 5 in their primary entry states

**P-3 — Journey step:** Demo 7 Act 2, Zambia three-scenario comparison, analytical scrutiny
phase (following the Demonstrative presentation to Aicha).

**P-4 — Interaction budget:** Lucas operates with a 1-click budget to open the panel. The
panel content must be readable without further interaction (no secondary expansion, no
navigation).

**P-6 — Analytical leverage (Lucas):**

Lucas can open the panel and state: *"The 340,000 figure uses the ZMB Q1 population of
3,894,625 (UN WPP 2024, 20% Q1 income fraction). The CI band is a T3 placeholder of ±13–16%
pending ADR-007 full integration. The poverty headcount ratio is extracted as the mean of Q1
CHT cohort entities; if no cohort data is present, we fall back to the main entity attribute.
T3 means this is derived from regional comparable economies, not primary country-level income
survey data."* This is the complete methodological defence — delivered from within Zone 1B,
without consulting external documentation.

**P-7 — North star capability delivered:**
Lucas can defend the quantitative claim under peer scrutiny without leaving the primary
viewport. The auditability path closes the gap between "the tool says 340,000" and
"here is the methodology you can audit."

---

## 3. Observable Application State

### 3.1 Primary observable state (collapsed — default)

**In N=3 COMPARE_VIEW with the Zambia three-scenario fixture loaded:**

`DistributionalComparisonSummary` renders exactly as in G3 delivery. A toggle affordance
(`data-testid="methodology-panel-toggle"`) is present in the component — visible as a small
clickable element (e.g., "▶ Methodology" label or chevron icon adjacent to the T3 badge).
The methodology panel is NOT visible in the collapsed state. The Zone 1 content — headline
differential, CI band, direction disclosure — is unaffected by the toggle presence.

### 3.2 Secondary observable state (expanded)

**After clicking `data-testid="methodology-panel-toggle"`:**

The methodology panel is visible in-place (no navigation, no modal, no drawer). It contains
4 fields, each with a named `data-testid`:

| Field | Content | `data-testid` |
|---|---|---|
| Q1 population | "ZMB: 3,894,625 (UN WPP 2024, 20% Q1 fraction)" | `methodology-q1-population` |
| CI methodology | "±13–16% of point estimate — T3 placeholder pending ADR-007 full CI band integration" | `methodology-ci-band` |
| Extraction path | "Q1 CHT cohort mean; falls back to main entity poverty_headcount_ratio if no cohort data" | `methodology-extraction-path` |
| Tier rationale | "T3: derived from regional comparable economies (ECOWAS), not calibrated country-level Q1 income share data" | `methodology-tier-rationale` |

The Zone 1 content (headline differential, CI band, direction disclosure) remains visible
at 1280×800 when the panel is expanded. The panel does not push those elements out of the
viewport.

### 3.3 Secondary observable state (collapsed again)

**After clicking `data-testid="methodology-panel-toggle"` a second time:**

The methodology panel is no longer visible. The `DistributionalComparisonSummary` returns to
its G3 baseline appearance.

### 3.4 Silent failure detection

**Silent failure — panel hardcodes ZMB values:**
If the Q1 population field shows "ZMB: 3,894,625" when the entity is SEN (Senegal), the
frontend is hardcoding Zambia values rather than using `methodology_detail.q1_population`
from the backend response. The QA test covers the ZMB fixture; the AC language specifies
that the field value must come from `methodology_detail` — not from a frontend constant.

**Silent failure — panel is a modal or navigates away:**
If clicking the toggle opens a dialog or navigates to a new route, Zone 1 content is no longer
visible and Lucas's 1-click budget is exceeded. The QA test must assert that the Zone 1
content (`data-testid="distributional-comparison-summary"`) is still visible after the panel
toggle click.

**Silent failure — Zone 1 content displaced at 1280×800:**
If the expanded panel pushes the headline differential below the fold, the implementation
violates constraint 4. The QA test must assert `data-testid="distributional-comparison-summary"`
bounding box remains within the viewport after the toggle click at 1280×800.

---

## 4. Acceptance Criteria

*Each criterion is testable from the running application without reading implementation code.
The QA test file is `frontend/tests/e2e/m18-g5-zone3-auditability.spec.ts`.*

**AC-1422-A (E2E — toggle present in COMPARE_VIEW):**
In N=3 COMPARE_VIEW with the Zambia three-scenario fixture loaded, `[data-testid="methodology-panel-toggle"]` is present in the DOM and visible within `[data-testid="distributional-comparison-summary"]`.
*Source: US-1349-D (Lucas auditability path)*

**AC-1422-B (E2E — panel collapsed by default):**
On initial COMPARE_VIEW load, none of `[data-testid="methodology-q1-population"]`,
`[data-testid="methodology-ci-band"]`, `[data-testid="methodology-extraction-path"]`,
`[data-testid="methodology-tier-rationale"]` are visible (either absent from DOM or `display:none`).
*Source: Constraint 1 — Zone 1 content must not be cluttered by default*

**AC-1422-C (E2E — panel expands on toggle click; all 4 fields visible):**
After clicking `[data-testid="methodology-panel-toggle"]`, all four panel fields are visible:
`[data-testid="methodology-q1-population"]` is visible AND contains "3,894,625";
`[data-testid="methodology-ci-band"]` is visible AND contains "13" and "16" (the ±13–16% range);
`[data-testid="methodology-extraction-path"]` is visible AND contains "Q1 CHT";
`[data-testid="methodology-tier-rationale"]` is visible AND contains "T3".
*Source: US-1349-D (Lucas reads all four items without external documentation)*

**AC-1422-D (E2E — Zone 1 content visible at 1280×800 after expansion):**
After clicking the toggle at viewport 1280×800, `[data-testid="distributional-comparison-summary"]`
has a bounding box with bottom edge ≤ 800px (still within the viewport). The headline
differential text (`_formatHeadcount` output) is still visible in the DOM.
*Source: Constraint 4 — no Zone 1 displacement*

**AC-1422-E (E2E — panel collapses on second toggle click):**
After clicking `[data-testid="methodology-panel-toggle"]` a second time, the four panel
field testids are no longer visible (either absent from DOM or `display:none`).
*Source: Constraint 1 — expand/collapse behaviour*

**AC-1422-F (E2E — toggle absent when COMPARE_VIEW not active):**
In single-scenario mode (N=1), `[data-testid="methodology-panel-toggle"]` is absent from
the DOM or not visible. (`data-testid="distributional-comparison-summary"` is also absent
in single-scenario mode per G3 AC-1349-F, so this AC follows from G3 state B.)
*Source: Consistent with G3 AC-1349-F — element only present in COMPARE_VIEW*

**AC-1422-G (backend — methodology_detail in response):**
`POST /api/v1/scenarios/comparison/distributional-differential` with the Zambia three-scenario
fixture returns a `methodology_detail` object with 4 fields:
- `q1_population: int` — value is 3,894,625 for entity_id "ZMB"
- `ci_methodology: str` — contains "13" and "16" (the ±13–16% band description)
- `extraction_path: str` — contains "Q1 CHT" and "fallback"
- `tier_rationale: str` — contains "T3" and "regional"
*Source: Constraint 2 — backend enrichment; Lucas defence without external documentation*

---

## 4b. Visual Spec (before/after)

**Before (G3 delivery — collapsed, no toggle):**
```
Viewport: 1280×800 | DistributionalComparisonSummary (sticky-bottom)

┌─────────────────────────────────────────────────────┐
│ DISTRIBUTIONAL COMPARISON  step 8        [T3]       │
│ Poverty headcount differential                       │
│                                                      │
│ Option A vs. Option C              +340,000 persons  │
│                              295K – 395K  95% CI    │
│ Option B vs. Option C              +210,000 persons  │
│                              175K – 255K  95% CI    │
│                                                      │
│ → Direction stable across uncertainty range          │
└─────────────────────────────────────────────────────┘
```
*Lucas sees "T3" badge — epistemic signal only. No auditability path.*

**After — collapsed (G5, default state):**
```
Viewport: 1280×800 | DistributionalComparisonSummary (sticky-bottom)

┌─────────────────────────────────────────────────────┐
│ DISTRIBUTIONAL COMPARISON  step 8  [T3] ▶ Methodology│
│ Poverty headcount differential                       │
│                                                      │
│ Option A vs. Option C              +340,000 persons  │
│                              295K – 395K  95% CI    │
│ Option B vs. Option C              +210,000 persons  │
│                              175K – 255K  95% CI    │
│                                                      │
│ → Direction stable across uncertainty range          │
└─────────────────────────────────────────────────────┘
```
*Toggle "▶ Methodology" (or chevron) appears adjacent to T3 badge. Zone 1 content unchanged.*

**After — expanded (G5, panel open):**
```
Viewport: 1280×800 | DistributionalComparisonSummary (sticky-bottom)

┌─────────────────────────────────────────────────────┐
│ DISTRIBUTIONAL COMPARISON  step 8  [T3] ▼ Methodology│
│ Poverty headcount differential                       │
│                                                      │
│ Option A vs. Option C              +340,000 persons  │
│                              295K – 395K  95% CI    │
│ Option B vs. Option C              +210,000 persons  │
│                              175K – 255K  95% CI    │
│                                                      │
│ → Direction stable across uncertainty range          │
│ ┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄     │
│ Q1 population:   ZMB: 3,894,625 (UN WPP 2024, 20%) │
│ CI band:         ±13–16% of point estimate (T3)     │
│ Extraction path: Q1 CHT cohort mean; main entity    │
│                  fallback                            │
│ Tier rationale:  T3 — regional comparables (ECOWAS) │
└─────────────────────────────────────────────────────┘
```
*Panel appears in-place, below direction disclosure, inside the sticky element.
Zone 1 content remains visible (headline + CI band + direction line above the panel).*

**Visual treatment:**
- Toggle: `fontSize: 10, color: "#6b7280"` — muted, adjacent to T3 badge
- Panel separator: `borderTop: "1px dashed #e5e7eb"` — dashed to distinguish from Zone 1B hard divider
- Panel label/value rows: `fontSize: 11, color: "#4b5563"` — consistent with Zone 1B subdued palette
- Label prefix: `fontWeight: 500` (e.g., "Q1 population:"); value: `fontWeight: 400`
- No background change, no elevation — panel is part of the same sticky container

**data-testid anchors required:**
- Toggle button: `data-testid="methodology-panel-toggle"`
- Q1 population field: `data-testid="methodology-q1-population"`
- CI methodology field: `data-testid="methodology-ci-band"`
- Extraction path field: `data-testid="methodology-extraction-path"`
- Tier rationale field: `data-testid="methodology-tier-rationale"`

---

## 5. Kryptonite Constraint Check

**Does this implementation create kryptonite risk for Persona 5 (Aicha)?**

No. The toggle and panel are inert for Persona 5's Demonstrative entry state — she reads the
headline number, which remains fully visible and unaffected. The toggle ("▶ Methodology") uses
a non-prominent visual treatment that does not draw attention away from the differential value.
The analyst narrating to Aicha does not need to interact with the toggle.

**Does the panel itself contain kryptonite?**

The panel content is technical — "Q1 CHT cohort mean," "ADR-007," "ECOWAS comparables" — and
would be kryptonite for Persona 5 if exposed without mediation. This is correct: the panel is
a Zone 3 surface for Persona 1 (Lucas), not a Zone 1 surface. Lucas has the domain knowledge
to interpret all four fields without mediation. The panel's collapse-by-default behaviour
ensures Persona 5 never encounters it during a Demonstrative presentation.

**Kryptonite check by persona:**

| Persona | Kryptonite risk | Assessment |
|---|---|---|
| Persona 1 (Lucas) | None — all four fields are domain-native for a programme analyst | PASS |
| Persona 2 (Eleni) | None — toggle is muted; panel collapsed by default; Zone 1 headline unaffected | PASS |
| Persona 5 (Aicha) | Panel content would be kryptonite — but panel is collapsed by default and Aicha's presentation flow does not require toggle interaction | PASS — by design (collapsed default) |

---

## 6. Backend Implementation Specification

### 6.1 — New field: `methodology_detail` in `DistributionalDifferentialResponse`

Add a `methodology_detail` field to the existing response schema with 4 sub-fields.
The field is populated at response time from existing backend constants and logic descriptions.

**Pydantic model addition (in `backend/app/schemas.py` or inline in `scenarios.py`):**

```python
class MethodologyDetail(BaseModel):
    q1_population: int
    ci_methodology: str
    extraction_path: str
    tier_rationale: str
```

**Population in `post_distributional_differential`:**

```python
methodology_detail = MethodologyDetail(
    q1_population=_ENTITY_Q1_POPULATION.get(entity_id, 0),
    ci_methodology=(
        f"±13–16% of point estimate — T3 placeholder "
        f"pending ADR-007 full CI band integration. "
        f"Lower bound factor: {_CI_FACTOR_LOWER}; upper bound factor: {_CI_FACTOR_UPPER}."
    ),
    extraction_path=(
        "Q1 CHT cohort mean (entities matching '<entity_id>:CHT:1-*'); "
        "falls back to main entity poverty_headcount_ratio if no cohort data present."
    ),
    tier_rationale=(
        "T3: derived from ECOWAS regional comparable economy distributions, "
        "not calibrated country-level Q1 income share survey data. "
        "Forward trace: ADR-007 full implementation will replace this T3 placeholder."
    ),
)
```

The `extraction_path` string interpolates the description of `_poverty_ratio_from_state`
logic into human-readable text — it does not call the function. The description must match
the actual behaviour of the function (CHT cohort mean → main entity fallback).

### 6.2 — Store type update

Add `methodology_detail` to `DistributionalSummaryData` in
`frontend/src/store/scenarioStepStore.ts`:

```typescript
export interface MethodologyDetail {
  q1_population: number;
  ci_methodology: string;
  extraction_path: string;
  tier_rationale: string;
}

export interface DistributionalSummaryData {
  // ... existing fields ...
  methodology_detail: MethodologyDetail;
}
```

The `methodology_detail` field should be optional (`methodology_detail?: MethodologyDetail`)
if there is any code path where the response may be generated without it — but given that G5
adds it to all `DistributionalDifferentialResponse` instances, it can be required.

### 6.3 — Schema prerequisite

`docs/schema/api_contracts.yml` must be updated with the `methodology_detail` field in the
same PR as the backend implementation. The update must document:
- Field name: `methodology_detail`
- Type: object
- Sub-fields: `q1_population` (integer), `ci_methodology` (string), `extraction_path`
  (string), `tier_rationale` (string)
- Required: yes

This is mandatory per CLAUDE.md §Schema registry — schema update must be in the same PR as
the backend change.

---

## 7. Frontend Implementation Specification

### 7.1 — Changes to `DistributionalComparisonSummary` in `MDAAlertPanelZone1B.tsx`

The component already accepts `{ summary: DistributionalSummaryData }`. With `methodology_detail`
added to `DistributionalSummaryData`, no prop signature change is needed — `summary.methodology_detail`
is available inside the component.

**State addition:**

```tsx
const [panelOpen, setPanelOpen] = React.useState(false);
```

**Toggle affordance** (rendered in the header row, adjacent to the T3 badge):

```tsx
<button
  data-testid="methodology-panel-toggle"
  onClick={() => setPanelOpen((v) => !v)}
  style={{ fontSize: 10, color: "#6b7280", cursor: "pointer",
           background: "none", border: "none", padding: "0 2px" }}
  aria-expanded={panelOpen}
>
  {panelOpen ? "▼ Methodology" : "▶ Methodology"}
</button>
```

**Methodology panel** (rendered below the direction disclosure line, inside the sticky container):

```tsx
{panelOpen && summary.methodology_detail && (
  <div
    style={{ borderTop: "1px dashed #e5e7eb", marginTop: 4, paddingTop: 4 }}
  >
    <div data-testid="methodology-q1-population" style={rowStyle}>
      <span style={labelStyle}>Q1 population:</span>{" "}
      {entityLabel}: {summary.methodology_detail.q1_population.toLocaleString("en-US")} (UN WPP 2024, 20% Q1 fraction)
    </div>
    <div data-testid="methodology-ci-band" style={rowStyle}>
      <span style={labelStyle}>CI band:</span>{" "}
      {summary.methodology_detail.ci_methodology}
    </div>
    <div data-testid="methodology-extraction-path" style={rowStyle}>
      <span style={labelStyle}>Extraction path:</span>{" "}
      {summary.methodology_detail.extraction_path}
    </div>
    <div data-testid="methodology-tier-rationale" style={rowStyle}>
      <span style={labelStyle}>Tier rationale:</span>{" "}
      {summary.methodology_detail.tier_rationale}
    </div>
  </div>
)}
```

Where `entityLabel` is derived from `summary.entity_id` (already in `DistributionalSummaryData`)
and `rowStyle`/`labelStyle` use `fontSize: 11, color: "#4b5563"` / `fontWeight: 500`.

### 7.2 — Files modified

| File | Change | Lane |
|---|---|---|
| `backend/app/api/scenarios.py` | Add `MethodologyDetail` model; populate in `post_distributional_differential`; add to `DistributionalDifferentialResponse` | Sprint sub-branch |
| `backend/app/schemas.py` (if `MethodologyDetail` defined there) | Add `MethodologyDetail` Pydantic model | Sprint sub-branch |
| `frontend/src/store/scenarioStepStore.ts` | Add `MethodologyDetail` interface; add `methodology_detail` field to `DistributionalSummaryData` | Sprint sub-branch |
| `frontend/src/components/MDAAlertPanelZone1B.tsx` | Add toggle + panel to `DistributionalComparisonSummary` | Sprint sub-branch |
| `docs/schema/api_contracts.yml` | Add `methodology_detail` to `DistributionalDifferentialResponse` shape | Same PR as backend (mandatory) |
| `frontend/tests/e2e/m18-g5-zone3-auditability.spec.ts` (new) | E2E tests for AC-1422-A through AC-1422-F | Sprint sub-branch — authored before implementation PR |

---

## 8. Out of Scope

**Interactive step selection on the methodology panel:** The panel shows the methodology for
the terminal-step computation. Step-specific methodology variation (if any) is not in scope.

**Editing or overriding the methodology values:** The panel is read-only. Lucas reads it;
he does not modify parameters via the panel.

**Methodology panel for single-scenario mode:** Not applicable — the panel is part of
`DistributionalComparisonSummary`, which is absent in single-scenario mode.

**Collapsible sub-sections within the panel:** The panel is a flat 4-field display.
No nested accordion or sub-expansion.

**Export or citation generation:** Lucas reads the panel values and cites them verbally.
No export, no copy-to-clipboard, no auto-generated citation string.

**`methodology_summary` string deprecation:** The existing `methodology_summary: string` field
remains in the response for backwards compatibility. G5 does not remove it. The `methodology_detail`
object is additive.

---

## 9. Test Authorship Obligation

**QA Lead:** QA Lead Agent (E2E); Computation Engine Agent (backend)

**Test authorship deadline:** `frontend/tests/e2e/m18-g5-zone3-auditability.spec.ts` authored
and committed to `sprint/m18-g5` **before the implementation PR opens**. Tests run red before
implementation; run green after. Backend test additions go into
`backend/tests/test_m18_g3_counter_scenario_comparison.py` (extend existing file — AC-1422-G
adds a new assertion to the existing test suite, not a separate file).

**E2E test file:** `frontend/tests/e2e/m18-g5-zone3-auditability.spec.ts`

Criteria covered:
- AC-1422-A: toggle present in COMPARE_VIEW
- AC-1422-B: panel collapsed by default (4 field testids absent/hidden)
- AC-1422-C: panel expands; all 4 fields visible with expected content fragments
- AC-1422-D: Zone 1 content visible at 1280×800 after expansion
- AC-1422-E: panel collapses on second toggle click
- AC-1422-F: toggle absent in single-scenario mode

**Backend test addition:** Extend `backend/tests/test_m18_g3_counter_scenario_comparison.py`
with one new assertion function:
- AC-1422-G: `methodology_detail` present in response; `q1_population` is 3,894,625 for ZMB;
  `ci_methodology`, `extraction_path`, `tier_rationale` are non-empty strings containing
  the expected substrings

**Pre-push gates (mandatory before any push):**
- Backend: `cd backend && source .venv/bin/activate && ruff check . && mypy app/` — both must exit 0
- Frontend: `cd frontend && npm run build` — must exit 0

**NM-076 crosscheck (mandatory before PR opens):**
For each new `data-testid` introduced: `grep -r '<testid-value>' frontend/tests/e2e/` —
confirm the QA test references the same string. No existing test should reference
`methodology-panel-toggle`, `methodology-q1-population`, `methodology-ci-band`,
`methodology-extraction-path`, or `methodology-tier-rationale` (these are new).

---

*Intent document authority: `docs/process/sprint-plans/m18-g5-sprint-entry.md §2.3` (intent
gate). Issue: #1422. Sprint journal: #1435. This document is the QA authorship contract and
implementation contract — a discrepancy between the delivered capability and §3 Observable
Application State is a Verify-step failure, not a document-update opportunity. Filed: 2026-06-28.*
