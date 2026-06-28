---
name: M18-G2-psp-driver-decomposition
type: implementation-intent
issues: "#1255"
status: Step 2 complete — QA tests authored and red-confirmed (2026-06-26); implementation may begin on feat/m18-g2-psp-decomposition from sprint/m18-g2
authored-by: Frontend Architect Agent
authored-date: 2026-06-26
implementing-agent: Computation Engine Agent (backend); Frontend Engineer (frontend)
sprint-entry: "docs/process/sprint-plans/m18-g2-sprint-entry.md — EL Approved 2026-06-26"
adr-reference: "ADR-015 §Component 3 — Zone 1D PSP row content addition within existing L0/L1 evidence thread model; no new ADR required"
release-branch: release/m18
sprint-branch: sprint/m18-g2
---

# Implementation Intent: M18-G2 — PSP Driver Decomposition (#1255)

## 1. Source

**Issue:** #1255 — `ux(zone-1d): PSP driver decomposition — dominant signal category visible alongside severity label`
**Status at time of authorship:** Open — EL-approved sprint entry on record; G2 sub-branch `sprint/m18-g2` cut 2026-06-26
**Authored by:** Frontend Architect Agent
**Date:** 2026-06-26
**Implementing agent:** Computation Engine Agent (backend: `PoliticalEconomyModule` extension); Frontend Engineer (frontend: `FourFrameworkZone1D.tsx` driver row)

---

**Motivation:** During Demo 7 Act 1 (Senegal Mode 3 active control), the analyst applies a fiscal counter-proposal and watches the PSP change step-by-step. Zone 1D currently shows *what* the PSP is (severity tier + value + direction) and *when* comparable programmes failed (historical analogue). It does not show *why* the PSP changed at the current step. Andreas (Persona 3) needs to cite the driver category in a verbal ministerial brief without opening Zone 2 or any sub-navigation. The sentence "Programme survival: WARNING — fiscal sustainability is the dominant pressure" must be composable from Zone 1D alone, in one glance, within the 90-second Reactive ceiling.

**Governing ADR:** ADR-015 §Component 3 authorises Zone 1D PSP row content additions within the existing L0/L1 evidence thread model. The driver decomposition is a content addition to the existing `zone-1d-political-risk` section — it does not change Zone 1D structural layout, introduce a new measurement framework, or add a new Zone 1D row for a previously absent indicator.

---

## 2. Persona Trace Elements Targeted

**P-1 — Persona served:**
Primary: **Persona 3 — Andreas Petrakis (Political Advisor)** (`docs/ux/personas.md §Persona 3`). Andreas reads Zone 1D to assess programme survival risk and translate findings into a political brief. The dominant driver label is the causal sentence he needs to brief the minister. Secondary: Persona 2 — Finance Ministry Negotiator (Aicha Mbaye), who uses the PSP driver to ground the causal argument in the negotiating room.

**P-2 — Entry state:**
Reactive (48-hour decision window, Demo 7 Act 1 live session) and Preparatory (building political brief before minister meets the IMF team). The 90-second total read ceiling applies: driver label must be visible at L0 without any interaction.

**P-3 — Journey reference:**
Journey B Step 3 (Reactive — scan Zone 1D for PSP status and causal attribution). The driver row extends Zone 1D from "what is the PSP level" to "why is the PSP at this level at this step" — the causal layer that supports the political brief.

**P-4 — Time/interaction ceiling:**
Zero interaction. `psp-driver-row` visible at L0 alongside `psp-severity-row` — no hover, no click, no keyboard shortcut required. Total Zone 1D read time including driver row: under 10 seconds for a user familiar with the instrument.

**P-5 — Income cohort served:**
Bottom two income quintiles and public sector workers — the cohorts most exposed to programme discontinuation. The driver label ("fiscal sustainability" / "governance") names the mechanism that threatens programme survival and thus the protection those programmes provide to lower-income cohorts.

**P-7 — North star capability delivered:**
After this implementation, Andreas can state from Zone 1D alone — without opening any drawer or navigating away: "Programme survival is at WARNING level; fiscal sustainability is the dominant driver at step 3; the comparable historical case (Ghana 2014 ECF) shows this configuration risks conditionality relaxation rather than programme abandonment." This sentence is composable from three visible Zone 1D elements: severity badge, driver row, and historical analogue. It is the political brief citation Demo 7 Act 1 requires.

---

## 3. UX/UI Panel Review Record

**Panel:** UX Designer, Design Thinking Agent, Customer Agent, Frontend Architect, Business PO
**Review date:** 2026-06-26
**Session context:** Same session as intent authorship — acknowledged (per CLAUDE.md §UX Designer sign-off protocol for same-session reviews)
**Governing documents reviewed:** `docs/ux/information-hierarchy.md §Zone 1D`, `docs/ux/north-star.md §Primary Cognitive Tasks`, `docs/ux/personas.md §Persona 3`, `docs/ux/personas.md §Persona 2`

### 3.1 Visual treatment determination

**UX Designer determination:** Inline sub-row treatment. A full UI mockup is NOT required.

**Rationale:** Zone 1D at 1280×800 already renders the following in the POLITICAL RISK section (from top to bottom):
- PSP severity row: `Programme survival: CRITICAL (38%) — DECLINING`
- Historical analogue: `Comparable: Zambia 2015 ECF — abandoned Step 3 (PSP 38%). Board review failed.`
- Legitimacy index row
- Elite capture rows (when available)

Adding a driver sub-row between the PSP severity row and the historical analogue introduces one line at `fontSize: 10` — the same visual weight as the historical analogue. The Zone 1D container scrolls vertically (`overflowY: "auto"`, `InstrumentCluster.tsx:172`), so vertical space is constrained but not fixed. No DOM structural change required: a single conditional `<div>` inside the existing `zone-1d-political-risk` block.

### 3.2 ASCII mockup

**Before (current Zone 1D POLITICAL RISK section):**
```
Viewport: 1280×800 | Zone: 1D | data-testid="zone-1d-political-risk"

─── POLITICAL RISK ───────────────────────
Programme survival: WARNING (52%) — DECLINING
Comparable: Ghana 2014 ECF — modified Step 5 (PSP 52%). Conditionality relaxed.
Legitimacy index: 0.52 — declining
```
The "why" is absent. Andreas reads severity + historical analogue but cannot say which mechanism is driving the deterioration.

**After (G2 implementation — Senegal fixture step 3):**
```
Viewport: 1280×800 | Zone: 1D | data-testid="zone-1d-political-risk"

─── POLITICAL RISK ───────────────────────
Programme survival: WARNING (52%) — DECLINING
Driver: fiscal sustainability                  ← new: data-testid="psp-driver-row"
Comparable: Ghana 2014 ECF — modified Step 5 (PSP 52%). Conditionality relaxed.
Legitimacy index: 0.52 — declining
```
"Driver: fiscal sustainability" occupies the structural slot between "what is the PSP level" (severity row) and "what does history say" (analogue). Placement is semantically correct: it answers "why" before the historical precedent answers "what happened in comparable cases."

### 3.3 Display format specification

```
Driver: {category_label}
```

| Backend value | Display label |
|---|---|
| `"fiscal_sustainability"` | `fiscal sustainability` |
| `"external_balance"` | `external balance` |
| `"governance"` | `governance` |
| `"social_stability"` | `social stability` |
| `null` | (sub-row omitted — no placeholder) |

**Typography:** `fontSize: 10, color: "#555"` — matching historical analogue row weight. No badge, no icon, no expandable, no percentage. Plain text satisfies the Persona 3 cite-in-brief requirement.

**Confidence tier display:** Not required on the driver row. The PSP severity row already carries the T3 tier association. The driver is an attribution derived from the same T3 computation — tier inheritance is implicit.

**When omitted:** If `psp_dominant_driver` is `null` or absent (no events drove a legitimacy delta at the current step), the Driver sub-row is not rendered. No placeholder text, no dash, no "—". Omission is the silent treatment; the severity row, historical analogue, and legitimacy rows display exactly as before G2 implementation.

### 3.4 Panel verdicts

**UX Designer: ACCEPT**
The inline sub-row treatment is consistent with the Zone 1D evidence thread pattern (ADR-015 §Component 3). The driver row occupies the semantic slot between "what" (PSP severity) and "precedent" (historical analogue) — correctly placed as the causal explanation layer. No layout regression at 1280×800: one additional line at fontSize 10 in a scrollable container is within the established Zone 1D density pattern. Font weight and color match the historical analogue row — appropriate visual weight for secondary contextual content.
Watchpoint: at 1024×768, Zone 1D width = 40% (InstrumentCluster.tsx:26). The longest driver label ("fiscal sustainability", ~17 chars) at fontSize 10 should render inline within that width. QA test at both 1280×800 and 1024×768 required.

**Design Thinking Agent: ACCEPT**
The driver row answers the "why" question that the PSP severity row (the "what") leaves open. "Driver: fiscal sustainability" is not a technical decomposition — it is a single plain-language category name in the vocabulary Andreas already uses for political briefs. The Persona 3 failure mode ("requires interpretation by an economist to understand") is explicitly avoided: the driver label translates directly into brief language without mediation. The information sequence — severity (what) → driver (why) → historical precedent (comparable case) — is a natural narrative structure for a non-economist reader.

**Customer Agent: ACCEPT (Persona 3 legibility gate)**
Kryptonite test (Persona 3, Reactive state): Andreas scans Zone 1D and reads: "Programme survival: WARNING (52%) — DECLINING / Driver: fiscal sustainability / Comparable: Ghana 2014 ECF — modified Step 5." He can produce: "This is at WARNING level; fiscal sustainability is the primary pressure; Ghana 2014 shows this configuration typically ends in conditionality relaxation, not programme abandonment." This sentence is composable from three Zone 1D lines, zero interactions, under 10 seconds. Passes the Persona 3 cite-in-brief requirement for Demo 7 Act 1.
Additional check (Persona 3 failure mode 2): "Governance outputs are null or unavailable." The driver row is a conditional addition — when null, it is absent rather than showing "—". Absence does not break the existing PSP severity display. Persona 3 still reads severity + analogue as before G2. No regression on the null-driver case.

**Frontend Architect: ACCEPT (implementation feasibility confirmed)**
One conditional `<div>` inside the existing `zone-1d-political-risk` block, between `psp-severity-row` and the `{analogue && ...}` conditional. `data-testid="psp-driver-row"`. Backend adds `psp_dominant_driver` to the measurement output; frontend reads new prop `pspDominantDriver?: string | null`. Prop flows through `InstrumentCluster.tsx → FourFrameworkZone1D` — same threading path as `pspValue` and `pspTier`. No structural change to InstrumentCluster.tsx layout. No file-conflict risk with G1 (TrajectoryView.tsx / banding engine are entirely separate file areas).
Schema-first mandatory: `docs/schema/api_contracts.yml` must be updated with `psp_dominant_driver` before the implementation PR opens (CLAUDE.md §Schema registry).

**Business PO: ACCEPT**
PSP driver decomposition is the Demo 7 Act 1 "why" layer. North star capability confirmed: the Senegal Ministry analyst can say from Zone 1D alone — "Programme survival is declining because fiscal sustainability is the dominant driver at step 3 — and historical precedent (Ghana 2014) shows this configuration risks conditionality relaxation." This sentence is the Demo 7 Act 1 causal attribution deliverable. The Zone 1D minimum viable demo condition for Act 1 is satisfied: PSP driver is readable without interaction within the 90-second Reactive ceiling.
Calibration check required at acceptance: confirm Senegal Article IV fixture at step 3 returns `psp_dominant_driver = "fiscal_sustainability"`. This is the Demo 7 Act 1 anchor.

---

## 4. Backend Specification

### 4.1 Driver category → event type mapping

The `PoliticalEconomyModule.compute()` method processes `prior_events` from `state.events`. Each event type maps to a driver category. The dominant driver is the category with the largest absolute contribution to `legitimacy_delta` at the current step.

| Driver category | Event types |
|---|---|
| `"fiscal_sustainability"` | `fiscal_policy_spending_change`, `fiscal_policy_tax_rate_change` |
| `"external_balance"` | `gdp_growth_change` |
| `"governance"` | `emergency_policy_capital_controls`, `emergency_policy_bank_holiday`, `emergency_policy_imf_program_acceptance`, `emergency_policy_default_declaration`, `emergency_policy_emergency_declaration`, conditionality events (`metadata.input_source == "conditionality"`) |
| `"social_stability"` | legitimacy fragility amplification path — applies when `FRAGILITY_AMPLIFIER (1.5×)` is the operative factor (i.e., `current_legitimacy < FRAGILITY_THRESHOLD = 0.5`) and no other event category produced a legitimacy contribution in this step |

### 4.2 Dominant driver computation

1. For each `prior_event` in the step, compute the absolute legitimacy contribution using the same coefficient applied in `_compute_legitimacy_delta` — specifically: `LEGITIMACY_EROSION_ELASTICITY × |fiscal_delta|` for fiscal events; `EMERGENCY_EROSION_FACTOR` per emergency event; GDP proportional contribution for `gdp_growth_change`.
2. Group contributions by driver category; sum per category.
3. If total `|legitimacy_delta|` ≈ 0 or no events produced a contribution: `psp_dominant_driver = None`.
4. Otherwise: `psp_dominant_driver = argmax(category_total_contribution)`.
5. Tie-breaking priority (descending): `governance`, `fiscal_sustainability`, `external_balance`, `social_stability`.

**Social stability trigger:** When `FRAGILITY_AMPLIFIER` applies and no other event category has a non-zero contribution, the amplification itself signals structural political fragility as the operative pressure. `psp_dominant_driver = "social_stability"` in that case only. When fiscal/emergency/GDP events are also present, those take priority over the amplification path.

### 4.3 Output — extend `programme_survival_update` event metadata

Add `psp_dominant_driver` to the `metadata` dict of the existing `programme_survival_update` event emitted by `PoliticalEconomyModule.compute()`:

```python
metadata={
    # existing keys remain unchanged:
    "current_legitimacy": str(current_legitimacy),
    "new_legitimacy": str(new_legitimacy),
    # new key:
    "psp_dominant_driver": psp_dominant_driver,  # str | None
}
```

The implementing agent must NOT change the event_type, event_id format, or existing metadata keys. The addition is additive.

### 4.4 API surface — how `psp_dominant_driver` reaches the frontend

`psp_dominant_driver` is forwarded via the existing measurement output API path that already surfaces `programme_survival_probability` under `political_economy.indicators`. The implementing agent must confirm which API response handler reads `programme_survival_update` event metadata and extend it to forward `psp_dominant_driver` alongside the existing `value` and `confidence_tier` fields.

**New field in the trajectory/measurement API response**, under `political_economy.indicators.programme_survival_probability`:
```
psp_dominant_driver: string | null
```

### 4.5 Tier inheritance

`psp_dominant_driver` inherits T3 (the PSP tier). No separate confidence tier field is required on this attribution. The implementing agent documents the inheritance in the PR description per the sprint entry requirement.

---

## 5. Observable Application State

### 5.1 Primary observable state

Zone 1D with PE enabled, Senegal Article IV fixture active, step 3:

The element at `data-testid="psp-driver-row"` is visible (no scroll required at 1280×800 viewport) and contains the text `"fiscal sustainability"` — the dominant driver for the Senegal fixture at step 3.

The element `data-testid="psp-severity-row"` remains present and visible alongside `psp-driver-row` (regression check: severity badge not displaced or hidden).

### 5.2 Secondary observable states

**Step-change behavior:** When the active step advances (trajectory scrubbing or Mode 3 step advance), `psp-driver-row` updates to reflect the new step's dominant driver. The driver label changes reactively without page reload or user interaction beyond the step-change itself.

**Null driver state (silent treatment):** When `psp_dominant_driver` is `null` (no events drove a legitimacy delta at the current step), `psp-driver-row` is NOT present in the DOM. The PSP severity row, historical analogue, legitimacy index row, and elite capture rows display as they did before G2 implementation.

### 5.3 Silent failure detection

**Silent failure — driver present in DOM but not visible:**
If `psp-driver-row` is attached to the DOM but scrolled outside the Zone 1D visible area at 1280×800, the QA assertion must use `.toBeVisible()` not `.toBeAttached()`. The driver row must be in the first screenful of the Zone 1D POLITICAL RISK section without scrolling the Zone 1D container.

**Silent failure — stale driver on step change:**
If `psp-driver-row` shows the step-N driver after advancing to step N+1 (i.e., the driver prop is not reactive), the element is present and readable but incorrect. The AC-1255-3 step-change assertion catches this: assert the driver text changes when the step changes.

**Silent failure — driver row present when driver is null:**
If the driver row is rendered even when `psp_dominant_driver` is `null` (e.g., showing "Driver: null" or "Driver: —"), the AC-1255-4 null-driver assertion catches this: assert `psp-driver-row` is NOT in the DOM when the step has no legitimacy-driving events.

---

## 4b. Visual Spec (before/after)

**AC-1255-1 (before):**
```
Viewport: 1280×800 | Zone: 1D | data-testid="psp-severity-row"

Programme survival: WARNING (52%) — DECLINING
[driver row absent — no "why" visible]
Comparable: Ghana 2014 ECF — modified Step 5 (PSP 52%). Conditionality relaxed.
```

**AC-1255-1 (after):**
```
Viewport: 1280×800 | Zone: 1D | data-testid="psp-driver-row"

Programme survival: WARNING (52%) — DECLINING
Driver: fiscal sustainability          ← present, visible, no interaction required
Comparable: Ghana 2014 ECF — modified Step 5 (PSP 52%). Conditionality relaxed.
```

**AC-1255-4 (null driver — before and after identical):**
```
Viewport: 1280×800 | Zone: 1D

Programme survival: STABLE (78%) — STABLE
[psp-driver-row NOT present in DOM]
Legitimacy index: 0.72 — stable
```
No driver row rendered when `psp_dominant_driver` is null. No regression to the existing PSP display.

---

## 6. Acceptance Criteria

**AC-1255-1 (driver row present — Senegal fixture step 3):**
In the Senegal Article IV scenario at step 3 with PE enabled, `data-testid="psp-driver-row"` is visible and contains the text `"fiscal sustainability"`.

**AC-1255-2 (driver row position — between severity and analogue):**
In any scenario with a non-null driver, `psp-driver-row` appears in the DOM after `psp-severity-row` and before `psp-historical-analogue`. Assert DOM ordering within `zone-1d-political-risk`.

**AC-1255-3 (driver row updates on step change):**
When the active step advances from step 3 to step 4 in the Senegal fixture, the text content of `psp-driver-row` is re-evaluated (it may stay the same category or change — assert that the element reflects the step-4 driver, not that it changes to a specific value).

**AC-1255-4 (null driver — no driver row in DOM):**
In a scenario fixture where the current step has no legitimacy-driving events (legitimacy delta ≈ 0, PSP flat), `psp-driver-row` is NOT present in the DOM.

**AC-1255-5 (severity row regression — not displaced):**
`data-testid="psp-severity-row"` and `data-testid="psp-severity-badge"` are present and visible alongside `psp-driver-row`. The severity badge text (CRITICAL/WARNING/WATCH/STABLE) is unchanged by the addition of the driver row.

**AC-1255-6 (breakpoint legibility — 1280×800):**
`psp-driver-row` is visible at 1280×800 viewport without scrolling the Zone 1D container. Use `.toBeVisible()` (not `.toBeAttached()`).

**AC-1255-7 (breakpoint legibility — 1024×768):**
`psp-driver-row` is visible at 1024×768 viewport within the Zone 1D POLITICAL RISK section without vertical scrolling of that section. The longest driver label ("fiscal sustainability") fits inline at `fontSize: 10` within Zone 1D's 40% width allocation at 1024px.

**AC-1255-B1 (backend — driver field in API response):**
The measurement output endpoint for the Senegal Article IV fixture returns `political_economy.indicators.programme_survival_probability.psp_dominant_driver` as a non-null string at step 3.

**AC-1255-B2 (backend — Senegal step 3 = fiscal_sustainability):**
The Senegal Article IV fixture at step 3 returns `psp_dominant_driver = "fiscal_sustainability"`.

**AC-1255-B3 (backend — null driver for flat step):**
A fixture step with no fiscal, external, governance, or social stability events returns `psp_dominant_driver = None` (null in JSON).

**AC-1255-B4 (backend — all four categories exercised):**
Unit tests confirm each of the four driver category values (`"fiscal_sustainability"`, `"external_balance"`, `"governance"`, `"social_stability"`) is returned given the appropriate mock event configuration. Four unit tests, one per category.

---

## 5. Kryptonite Constraint Check

`[x]` **No specialist mediation required.** "Driver: fiscal sustainability" is self-interpreting for Persona 3. The label is plain-language political brief vocabulary — not an indicator code, not a composite score value, not a confidence interval. Persona 3 reads the driver label and has the causal sentence he needs for a ministerial brief without asking an economist what the output means.

**No composite-score notation:** The driver row displays a category label, not a numeric value. No "0.XX" notation. No percentage. This passes the Persona 3 kryptonite constraint: output does not require specialist mediation in the Reactive entry state.

**Persona 2 secondary check:** Aicha (Finance Ministry Negotiator, Persona 2) also benefits — "Driver: governance" or "Driver: fiscal sustainability" maps to the causal framing she uses when constructing the L1 basis argument in the negotiating room. The driver label does not require interpretation at the Reactive 90-second ceiling.

---

## 6. Schema Prerequisite

Per CLAUDE.md §Schema registry: schema files must be updated in the same PR as the implementation that introduces the new field.

**`docs/schema/api_contracts.yml`** — add under `political_economy.indicators.programme_survival_probability` in the measurement output section:
```yaml
psp_dominant_driver:
  type: string | null
  enum: ["fiscal_sustainability", "external_balance", "governance", "social_stability", null]
  description: >
    Dominant driver category for PSP change at current step, as attributed by
    PoliticalEconomyModule from prior-step events. null if no events produced a
    non-zero legitimacy delta. Inherits T3 confidence tier from PSP computation.
    Values: fiscal_sustainability (fiscal_policy_* events), external_balance
    (gdp_growth_change), governance (emergency_policy_* and conditionality events),
    social_stability (fragility amplification path only, no other events present).
```

**`docs/schema/simulation_state.yml`** — add under `political_economy` module outputs:
```yaml
psp_dominant_driver:
  type: string | null
  description: >
    Driver category with largest absolute contribution to legitimacy_delta at
    current step. Set in programme_survival_update event metadata by
    PoliticalEconomyModule. null when legitimacy_delta ≈ 0 or no subscribed
    events present. Exposed via measurement output API alongside
    programme_survival_probability.
```

---

## 7. Out of Scope

| Item | Rationale |
|---|---|
| Top-3 driver breakdown with percentages | Not required for Demo 7. Andreas needs the dominant driver label for cite-in-brief, not a decomposition table. Single dominant driver satisfies the observable state. |
| PSP decomposition for N>1 comparison scenarios | G2 scope is single-scenario PSP decomposition only. Multi-scenario PSP driver delta is outside G2 scope — no requirement in #1255. |
| Driver confidence tier badge on driver row | PSP T3 association is established by the severity row. Driver inherits T3 implicitly. No separate badge needed; adding one would increase Zone 1D density without legibility gain. |
| Zone 1D structural change (new sections, column layout) | Not triggered by the inline sub-row treatment. If Zone 1D structural change is later required (e.g., driver history over multiple steps), that is a separate intent document. |
| Driver persistence / smoothing across steps | No temporal smoothing. Current-step driver reflects current-step events only. Step-change behavior is reactive. |
| PSP driver in Zone 2 / entity drawer deep drill | The Zone 2 driver is a future enhancement. G2 delivers the L0 label; the L1 basis statement (percentage contribution breakdown) is deferred. |

---

## 8. Test Authorship Obligation

**QA Lead:** QA Lead Agent
**Test authorship deadline:** Before any implementation PR for `feat/m18-g2-psp-decomposition` is opened; tests must be red (failing, not passing) before implementation begins
**Test file locations:**
- `frontend/tests/e2e/m18-g2-psp-decomposition.spec.ts` — Playwright E2E
- `backend/tests/test_m18_g2_psp_decomposition.py` — pytest

**Frontend test file must assert:** AC-1255-1 through AC-1255-7
Fixture: Senegal Article IV scenario (existing Demo 7 Act 1 fixture, PE enabled, step 3)
Viewport tests: 1280×800 (AC-1255-6) and 1024×768 (AC-1255-7)
Step-change test: AC-1255-3 — advance from step 3 to step 4, assert driver row reflects step-4 driver
Null-driver test: AC-1255-4 — a step with no legitimacy-driving events; assert `psp-driver-row` not in DOM

**Backend test file must assert:** AC-1255-B1 through AC-1255-B4
Fixture: Senegal Article IV fixture at step 3; plus a flat-step fixture for AC-1255-B3
Unit tests: mock event configurations for all four driver categories (AC-1255-B4)

**Regression guard:** After implementation, run `m16-g1-zone-1a-phase4-composite.spec.ts` locally and confirm `AC-9: psp-historical-analogue visible at L0 (no interaction) at step 1` still passes. The driver row sits above the historical analogue — DOM positional selectors (`.nth()`, `:has(+ div)`) in existing tests must be reviewed. Update any selectors in that file that assume `psp-historical-analogue` is the first child after `psp-severity-row`. Include this regression check in the G2 implementation PR.

**QA Lead acknowledgment:**
`[x]` QA Lead: Tests for AC-1255-1 through AC-1255-7 and AC-1255-B1 through AC-1255-B4 authored and filed before implementation PR opens. 2026-06-26

---

## 9. Implementation Sequencing

1. QA Lead authors test files (red) on `sprint/m18-g2`
2. Implementing agents open `feat/m18-g2-psp-decomposition` from `sprint/m18-g2`
3. **Computation Engine Agent (backend):**
   - Extend `_compute_legitimacy_delta` (or introduce a new private helper `_attribute_legitimacy_delta`) to return `(legitimacy_delta, psp_dominant_driver)` using the mapping in §4.1
   - Thread `psp_dominant_driver` into the `programme_survival_update` event metadata dict (§4.3)
   - Extend the measurement output API handler to forward `psp_dominant_driver` alongside the existing PSP fields
   - Update `docs/schema/api_contracts.yml` and `docs/schema/simulation_state.yml` in the same commit
4. **Frontend Engineer:**
   - Add `pspDominantDriver?: string | null` prop to `FourFrameworkZone1DProps` interface
   - Add a `DRIVER_LABELS` mapping object (backend value → display text per §3.3) in `FourFrameworkZone1D.tsx`
   - Render `<div data-testid="psp-driver-row" ...>{`Driver: ${DRIVER_LABELS[pspDominantDriver]}`}</div>` between `psp-severity-row` and the `{analogue && ...}` conditional, gated on `pspDominantDriver != null`
   - Add `pspDominantDriver` prop to `InstrumentCluster.tsx` — thread from store/API data alongside existing `pspValue` prop; same prop-path as `pspValue` and `pspTier`
5. Pre-push gate: `cd backend && ruff check . && mypy app/` + `cd frontend && npm run build` — both must exit 0 before any push
6. PR targets `sprint/m18-g2`; set auto-merge (`gh pr merge <number> --merge --auto`)
7. **Step 4 — Verify:** Playwright observation confirms `psp-driver-row` is visible in the Demo 7 Act 1 Senegal fixture at step 3 with text "fiscal sustainability". Implementing agent produces this observation before the PR is marked ready for review.
8. Integration PR `sprint/m18-g2` → `release/m18` after feature PR merges; PI Agent gate comment required
9. **Step 5 — Validate (BPO acceptance):** Business PO opens the live application, confirms Andreas persona can cite "Driver: fiscal sustainability" from Zone 1D alone for the Senegal step-3 scenario without interaction. Customer Agent Layer 3 at sprint exit.
