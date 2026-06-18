---
name: M14-G6-methodology-calibration
type: implementation-intent
adr: "N/A — standalone fixes and calibration within ADR-005/ADR-014/ADR-016 boundaries"
issues: "#22, #884, #885, #823, #824, #950 + PMM interpretation anchor"
status: Filed
authored-by: Chief Engineer Agent (backend); Frontend Architect Agent (frontend); Chief Methodologist Agent (documentation)
authored-date: 2026-06-18
implementing-agent: "Chief Engineer Agent (#823, #824, #884); Frontend Architect Agent (#885, #950); Chief Methodologist Agent (#22, PMM anchor)"
sprint-entry: docs/process/sprint-plans/m14-g6-sprint-entry.md
---

# Implementation Intent: M14-G6 — Methodology, Calibration, and Instrument Legibility

## 1. Source ADR

**ADR:** N/A — G6 implements standalone fixes and calibration updates within existing
architectural boundaries. No new ADR required.
**Sprint plan reference:** `docs/process/sprint-plans/m14-sprint-plan.md §G6`
**Status at time of authorship:** EL-approved sprint plan (2026-06-16)
**Authored by:** Chief Engineer Agent (backend sections), Frontend Architect Agent
(frontend sections), Chief Methodologist Agent (documentation sections)
**Date:** 2026-06-18

**Issues in scope:**
- **#885** — Zone 1B negotiation defensibility label: "Exploratory — do not cite" is returned for
  T4 and T5 MDA alerts. T4 means "model estimate" per ADR-015 §UX-5; T5 means "synthetic
  extrapolation." Neither is "Exploratory." The label is shown in the Zone 1B detail slot to
  help Persona 2 decide what to cite at the table — a wrong label is a negotiation mistake.
- **#950** — Zone 1A trajectory chart has no Y axis label. The recharts `<YAxis>` element has
  no `label` prop. The Y axis shows numerical tick values (0.00, 0.25, …) but no label
  describing what dimension is being plotted.
- **#884** — `reserve_coverage_months` does not appear in `GET /scenarios/{id}/initial-state`
  for JOR/EGY/ZMB scenarios, because the indicator is seeded as a FLOW delta (engine effect)
  not as a source-attributed STOCK in the entity's step-0 state_data. The initial-state endpoint
  requires a `source_registry_id` and `measurement_framework` in the Quantity envelope to
  include an indicator.
- **#823** — Ecological composite denominator and confidence_tier: the
  `_boundary_proximity_strategy` returns a correct denominator (current `len(proximity_scores)`)
  but the `confidence_tier` is hardcoded at 2 for the ecological composite (line 866 of
  `scenarios.py`). Unlike governance and financial composites, ecological does not derive the
  tier from its constituent indicators. CM constraint: the tier must be max() of the ecological
  indicators' individual tiers, consistent with the lower-of-two rule (memory:
  `feedback_confidence_tier_max.md`). The zero-indicator → None path is already correct.
- **#824** — MENA arid-economy water scarcity calibration: JOR/ZMB entities with
  `biome_class=arid_semiarid` have no water scarcity elasticity in the
  `ECOLOGICAL_ELASTICITY_REGISTRY`. CM + Ecological Economist approved (2026-06-13):
  add `water_stress_index` elasticity = −0.04, Tier 3, FAO GFR arid-subset/ICARDA,
  `biome_class=arid_semiarid`, fallback to `high_forest_cover` with WARNING.
- **#22** (M14 scope) — Confidence tier methodology documentation: the methodology publication
  M14 primary goal requires publishing how confidence tiers 1–5 are assigned to each indicator
  family. Full distributional bands (CI intervals) are M16.
- **PMM interpretation anchor** — Chief Methodologist deliverable. G5 implements
  `[T3 composite · pre-cal]` as a placeholder in Zone 1C. This document explains what the
  PMM composite score represents and the rationale for its pre-calibration status.

**Prerequisite state (all satisfied before implementation begins):**
- G5 PR #1030 merged 2026-06-18 — L0 annotations, assumption surface, PMM placeholder in Zone 1C
- G3 COMPLETE 2026-06-17 (PR #1011) — `/data-quality`, `/initial-state` endpoints in service
- G4 COMPLETE 2026-06-17 (PR #1015/#1016/#1018) — ADR-016 frontend delivered
- CM+EE approval for #823 and #824 recorded 2026-06-13 (M13 G8a)

---

## 2. Persona Trace Elements Targeted

**P-1 — Persona served:**
Primary: Persona 2 — Finance Ministry Negotiator (Eleni Papadimitriou / Aicha Diallo archetype).
The Zone 1B negotiation defensibility label (#885) is the direct interface for Persona 2 to
decide what to cite in the reactive state. A label reading "Exploratory" for a T4 model estimate
is a negotiation error — it causes the ministry team to under-state the defensibility of their
data. Secondary: Persona 1 — IMF Programme Analyst, who uses calibration documentation (#22,
PMM anchor) to audit the model's assumptions before or after a session.

**P-2 — Entry state:**
- **Reactive** (Persona 2, #885): Zone 1B detail is open with a TERMINAL or WARNING alert.
  The negotiation defensibility label is visible in the detail slot. Time ceiling: 90 seconds
  to decide whether to cite the figure. The label must correctly communicate T4 defensibility
  so the ministry team does not discard an argument they could have made.
- **Preparatory** (Persona 1, #22 / PMM anchor): before the session, Persona 1 reviews the
  methodology documentation to audit assumptions. Time ceiling: 5 minutes to navigate from the
  calibration index to the relevant methodology section.
- **Ambient** (Persona 2, #950): the Zone 1A Y axis label is visible on every panel load — no
  interaction required. A blank axis label is an ambient legibility gap.

**P-3 — Journey reference:**
- Closes Journey B Step 3 [Near-Term-Gap] (partial complement to G5 L0 annotations): the Zone 1B
  negotiation label ensures the defensibility guidance is correct so Persona 2 can act on it.
- Closes Journey F Step 1 [Near-Term-Gap]: methodology documentation (#22) enables Persona 1
  to audit input assumptions before the session.

**P-4 — Time/interaction ceiling:**
- #885 Zone 1B label: visible when Zone 1B detail is open — zero additional interactions beyond
  those already required to open the detail. Time to read: immediate.
- #950 Y axis: visible on Zone 1A load — zero interactions.
- #22 / PMM anchor: 5 minutes to navigate from methodology index to the specific section
  (Business PO documentation test).

**P-6 — Negotiating leverage delivered:**
After G6, Persona 2 sees `[data-testid="alert-negotiation-label"]` showing "Model estimate —
verify before citing" for a T4 alert. She can say: "This breach indicator is a model estimate —
we are prepared to share the calibration basis. The IMF uses the same class of indicators in
comparable assessments." Before G6, she would see "Exploratory — do not cite" and abandon a
defensible argument.

**P-7 — North star capability delivered:**
The Zambian Finance Ministry team is reviewing a T4-tier breach indicator on their screen during
the debt restructuring session. The Zone 1B detail shows "Model estimate — verify before citing."
The Chief Economist says: "That means it is a model estimate — let us share the calibration
section." She opens the PMM interpretation anchor in two interactions and shows the IMF team
the calibration methodology. Before G6: the label said "Exploratory — do not cite" and the
calibration document did not exist. After G6: both the label and the document are correct.

---

## 3. Observable Application State

### 3.1 Primary observable state

**Zone 1B negotiation label (#885):**

With a Zone 1B MDA alert detail open where the alert has `confidence_tier = 4` (mocked via
`page.route()` interception of the MDA alert response): the element with
`[data-testid="alert-negotiation-label"]` (or the Zone 1B detail slot that contains the
defensibility label) is visible and contains the text "Model estimate" as a substring. It does
NOT contain "Exploratory". At `confidence_tier = 5`, the label contains "Synthetic extrapolation"
and "do not cite" as substrings, and does NOT contain "Exploratory".

> **Implementing agent note:** The existing `getNegotiationLabel(tier: number)` function in
> `MDAAlertPanelZone1B.tsx` returns `"Exploratory — do not cite"` for `tier >= 4`. The fix is
> to distinguish T4 from T5 and return proper ADR-015 §UX-5 tier-meaning labels. The testid for
> the label element must be confirmed in the intent: if the detail slot element does not have
> `data-testid="alert-negotiation-label"`, the Frontend Architect Agent must add it before
> QA tests are authored.

### 3.2 Secondary observable states

**Secondary state A — Zone 1A Y axis label (#950):**

With any completed scenario loaded at viewport 1280×900 (or any viewport): `[data-testid="zone-1a-trajectory"]` (or the recharts container wrapping the Y axis) contains a visible text element displaying "Score" (or the confirmed axis label) as the Y axis description. The text is rendered at a non-zero bounding box height and is not hidden. The tick labels (0.00, 0.25, …) remain present and are not affected by the label addition.

> **Implementing agent note (Zone 1A Y axis):** The Y axis label should describe the composite
> score dimension. Confirm the label text with the Chief Methodologist: options include "Score"
> (simple), "Composite Score" (explicit), or "Framework Score [0–1]" (with range hint). The
> label must fit within the existing YAxis `width={44}` allocation without clipping. A vertical
> rotated label (angle=-90, position="insideLeft") is the standard recharts approach.
> The intent document commits to "Score" as the default; if the Chief Methodologist specifies
> a different label in the G6 PMM anchor consultation, use that value.

**Secondary state B — reserve_coverage_months in initial-state (#884):**

`GET /api/v1/scenarios/{scenario_id}/initial-state` for the JOR Hormuz scenario (or any JOR
scenario that has been advanced at least one step) returns an `InitialStateResponse` where
`frameworks["financial"].indicators` contains at least one entry with `name: "reserve_coverage_months"`
and a non-null `value`. The indicator also carries a non-null `source` (provider string from
source_registry) and a `confidence_tier` of 2 or 3.

> **Chief Engineer note (#884):** The root cause is that `reserve_coverage_months` is applied
> as a FLOW event delta by the external sector module (affected_attributes in module.py line 196)
> but is NOT present in the entity's seed state_data at step 0 as a source-attributed STOCK.
> The initial-state endpoint at line 273 skips indicators without `measurement_framework` in
> their Quantity envelope. Fix options:
> (A) Seed reserve_coverage_months as a proper STOCK in the JOR/EGY/ZMB entity seed migration
>     with `source_registry_id`, `measurement_framework=financial`, and `confidence_tier`; OR
> (B) Add reserve_coverage_months to the step-0 entity state_data with a real Central Bank
>     source entry in source_registry, then ensure it persists through propagation.
> The Chief Engineer determines the correct approach; the intent document commits to the
> observable outcome (visible in /initial-state) regardless of implementation path.

**Secondary state C — Ecological composite confidence_tier derives from indicators (#823):**

At step 1 of the Greece 2012 scenario (`GET /api/v1/scenarios/{scenario_id}/trajectory`), the
ecological `TrajectoryFrameworkPoint.confidence_tier` value is NOT 2 (hardcoded) but is equal
to the max() of the individual ecological indicator confidence_tiers for that step. Specifically:
if all ecological indicators at step 1 for GRC have `confidence_tier = 2` (per the ecological
module's tier assignments), the composite returns 2. If any ecological indicator has `confidence_tier = 3`,
the composite returns 3. The fixed value 2 must not appear as the sole result of the hardcoded
line — it must be derived.

> **Chief Engineer note (#823):** Line 866 of `scenarios.py` has `confidence_tier=2` hardcoded
> for the ecological composite. The fix follows the governance branch pattern (lines 874–882):
> `indicator_min_tier = min(qty.confidence_tier for ecological indicators, default=T3_FLOOR)`;
> `tier = max(indicator_min_tier, ECOLOGICAL_MIN_TIER)`. The zero-indicator → None guard at
> line 1923–1924 is already correct and must not be changed. The `confidence_tier` for zero-
> indicator case is irrelevant (composite_score is null). Confirm the ecological MIN_TIER floor
> value with the Chief Methodologist: the current hardcoded T2 may or may not be the correct
> floor for the ecological framework.

**Secondary state D — MENA water scarcity calibration applied (#824):**

At step 1 of the JOR Hormuz scenario, `GET /api/v1/scenarios/{scenario_id}/measurement-output?entity_id=JOR&step=1`
returns the ecological framework's indicators array including an entry for `water_stress_index`
(or the canonical water scarcity indicator key as confirmed by Chief Engineer) with a non-null
value. This confirms the elasticity is active and producing outputs for arid_semiarid entities.

> **Chief Engineer note (#824):** Implementation requires three coordinated changes:
> 1. Add a new `EcologicalElasticity` entry to `ECOLOGICAL_ELASTICITY_REGISTRY` in
>    `backend/app/simulation/modules/ecological/elasticities.py`:
>    `event_type="fiscal_policy_spending_change"` (or the relevant triggering event),
>    `indicator_key="water_stress_index"`, `elasticity=Decimal("-0.04")`, `confidence_tier=3`,
>    source citing FAO GFR arid-subset/ICARDA (source_registry_id to be assigned).
> 2. Set `biome_class=arid_semiarid` on JOR and ZMB entity configurations (entity seed data
>    or a Alembic migration updating existing entity records).
> 3. Add a biome-class-conditional dispatch in the ecological module so the water scarcity
>    elasticity is only applied when `entity.biome_class == "arid_semiarid"`. For entities
>    without biome_class or with `biome_class=high_forest_cover`, emit a WARNING log and
>    skip the water scarcity entry (CM constraint: "fallback to `high_forest_cover` with WARNING").
> The Chief Engineer must confirm the triggering event type (what economic event causes water
> scarcity change in the JOR model context) and the canonical indicator key name before
> implementation begins.

**Secondary state E — PMM interpretation anchor exists (#22 / PMM anchor):**

A document exists at `docs/calibration/pmm-interpretation-anchor.md` (if this path is wrong, the
Chief Methodologist determines the canonical path; the path must appear in `docs/calibration/README.md`
or equivalent index). A non-author can navigate from the calibration index to the PMM anchor and
locate the explanation of what the PMM composite score represents within 5 minutes of opening the
document.

A second document exists at `docs/calibration/confidence-tier-assignment-methodology.md` (#22)
documenting how confidence tiers 1–5 are assigned to each indicator family in WorldSim, with
rationale for each tier assignment. This document is the M14 scope of the uncertainty
quantification methodology publication goal.

### 3.3 Silent failure detection

**#885 Zone 1B label — silent failure:**
The existing label "Exploratory — do not cite" is not an empty or missing state — it is a
plausible-sounding but incorrect string. The distinguishing observable characteristic: the
string "Exploratory" must NOT appear in `[data-testid="alert-negotiation-label"]` at any tier.
A test that only checks the label IS present (non-empty) would pass the current broken state.
The test MUST assert the absence of "Exploratory" AND the presence of the correct tier-specific
string.

**#884 reserve_coverage_months — silent failure:**
If the indicator is absent from the `/initial-state` response, the response returns an empty
`frameworks.financial.indicators` array or the array omits reserve_coverage_months with no
error. There is no 404 or error — the response is 200 with a short list. The test must assert
that `reserve_coverage_months` IS in the indicators list (not just that the list is non-empty).

**#823 ecological composite tier — silent failure:**
If the hardcoded `confidence_tier=2` is not fixed, the composite still returns a non-null value
and passes most tests. The distinguishing observable: when the ecological indicators have a
mix of T2 and T3 data, the composite must return T3 (max rule). If it returns T2 regardless of
indicator tiers, the bug is present. Tests must use a scenario with known T3 ecological
indicators to confirm T3 is propagated.

---

## 4. Acceptance Criteria

**AC-1 (#885 — Zone 1B T4 label: "Model estimate — verify before citing"):**
When the Zone 1B MDA alert panel is loaded with a mocked response where the alert's
`confidence_tier` is 4 (via `page.route()` intercepting the Zone 1B alert API response): the
element containing the negotiation defensibility label contains "Model estimate" as a substring
AND does NOT contain "Exploratory" as a substring. Assert: `expect(labelText).toContain("Model estimate")` AND `expect(labelText).not.toContain("Exploratory")`.

**AC-2 (#885 — Zone 1B T5 label: "Synthetic extrapolation — do not cite"):**
When the Zone 1B MDA alert panel is loaded with a mocked response where the alert's
`confidence_tier` is 5: the negotiation defensibility label contains "Synthetic extrapolation"
as a substring AND contains "do not cite" as a substring AND does NOT contain "Exploratory".
Assert each by direct string-presence match.

**AC-3 (#885 — Zone 1B T1/T2/T3 labels unchanged):**
When `confidence_tier` is 1: label contains "High confidence" AND "cite directly". When
`confidence_tier` is 2: label contains "High confidence" AND "cite directly". When
`confidence_tier` is 3: label contains "Moderate confidence" AND "cite with caveat". None of
these three tiers return "Exploratory". Assert by direct string-presence match for each tier.

**AC-4 (#950 — Zone 1A Y axis label visible):**
With any completed scenario loaded in Zone 1 at viewport 1280×900: Zone 1A contains a visible
Y axis label element. The element's text is non-empty and matches the agreed label value (e.g.,
"Score"). Assert: the recharts `<YAxis>` label text node is present in the DOM and
`getBoundingClientRect().height > 0`. Assert the text content equals the agreed label string
(exact match — not regex).

**AC-5 (#884 — reserve_coverage_months in /initial-state for JOR):**
`GET /api/v1/scenarios/{scenario_id}/initial-state` for a JOR scenario that has been advanced
at least one step returns `HTTP 200`. The response body's `frameworks.financial.indicators`
array contains at least one entry where `name === "reserve_coverage_months"` AND `value !== null`.
Assert using pytest+httpx on the JOR Hormuz test scenario fixture.

**AC-6 (#823 — ecological composite confidence_tier derived, not hardcoded):**
`GET /api/v1/scenarios/{scenario_id}/trajectory` for the Greece 2012 scenario at step 1 returns
the ecological `TrajectoryFrameworkPoint` with `confidence_tier` equal to the expected value
derived from the ecological indicators' max() tier rule — NOT unconditionally equal to 2 when
ecological indicators have a mix of tiers. Verify using a test fixture where at least one
ecological indicator has `confidence_tier = 3`, confirming the composite returns 3.

**AC-7 (#823 — zero ecological indicator → null composite, unchanged):**
`GET /api/v1/scenarios/{scenario_id}/trajectory` for a scenario entity where no ecological
boundary constants are active returns `composite_score: null` for the ecological framework (not
`"0.0000"` or `"0"`). This constraint is already implemented; this AC confirms it is not
broken by the AC-6 fix.

**AC-8 (#824 — MENA water scarcity calibration applied to JOR):**
`GET /api/v1/scenarios/{scenario_id}/measurement-output?entity_id=JOR&step=1` for the JOR
Hormuz scenario returns the ecological framework's indicators array containing an entry for the
water scarcity indicator (key to be confirmed by Chief Engineer — `water_stress_index` or
canonical name) with a non-null `value` and `confidence_tier = 3`. This confirms the elasticity
entry is active and the JOR entity has `biome_class=arid_semiarid` configured.
Assert using pytest+httpx on the JOR Hormuz test scenario fixture.

**AC-9 (#22 + PMM anchor — documentation navigable):**
A file exists at `docs/calibration/pmm-interpretation-anchor.md` (Chief Methodologist confirms
canonical path). `find docs/calibration/ -name "pmm-interpretation-anchor.md"` exits 0.
A file exists at `docs/calibration/confidence-tier-assignment-methodology.md` (or equivalent
path confirmed by Chief Methodologist). `find docs/ -name "confidence-tier-assignment-methodology.md"`
exits 0. Both documents are referenced in a calibration index at `docs/calibration/README.md`
or equivalent. Business PO validates 5-minute navigation test at Step 5.

---

## 4b. Visual Spec (before/after)

**AC-1 / AC-2 — Zone 1B negotiation label (before — T4):**
```
┌───────────────────────────────────────────────────────┐
│ Zone 1B DETAIL                                        │
│ ── Reserve Coverage (months) ───────────────────────  │
│ TERMINAL  crossed threshold at step 3                 │
│                                                       │
│ Exploratory — do not cite       ← WRONG for T4       │
│ ^^^^^^^^^^^                                           │
│ "Exploratory" is T4's label currently;                │
│ T4 = model estimate, which IS citable with caveat     │
└───────────────────────────────────────────────────────┘
```

**AC-1 — Zone 1B negotiation label (after — T4):**
```
┌───────────────────────────────────────────────────────┐
│ Zone 1B DETAIL                                        │
│ ── Reserve Coverage (months) ───────────────────────  │
│ TERMINAL  crossed threshold at step 3                 │
│                                                       │
│ Model estimate — verify before citing   ← T4          │
│ ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^                  │
│ data-testid="alert-negotiation-label"                 │
└───────────────────────────────────────────────────────┘
```

**AC-2 — Zone 1B negotiation label (after — T5):**
```
┌───────────────────────────────────────────────────────┐
│ Zone 1B DETAIL                                        │
│ ── Bottom Quintile Consumption ─────────────────────  │
│ TERMINAL  crossed threshold at step 2                 │
│                                                       │
│ Synthetic extrapolation — do not cite   ← T5          │
└───────────────────────────────────────────────────────┘
```

**AC-4 — Zone 1A Y axis (before — no label):**
```
┌────────────────────────────────────────────────────┐
│ Zone 1A — Trajectory                               │
│                                                    │
│  1.00 ┤═══════════════════════════════════════     │
│  0.75 ┤                                            │
│  0.50 ┤                                            │
│  0.25 ┤                                            │
│       └──────────────────────────────────          │
│         ^^^^ Y axis: tick values only; no label    │
│         User sees 0.00–1.00 but not what 1.00      │
│         represents                                  │
└────────────────────────────────────────────────────┘
```

**AC-4 — Zone 1A Y axis (after — label present):**
```
┌────────────────────────────────────────────────────┐
│ Zone 1A — Trajectory                               │
│                                                    │
│       S  1.00 ┤════════════════════════════════    │
│       c  0.75 ┤                                    │
│       o  0.50 ┤                                    │
│       r  0.25 ┤                                    │
│       e       └────────────────────────────        │
│         ^^^^ Y axis: "Score" label added (rotated) │
│         Tick values unchanged                      │
└────────────────────────────────────────────────────┘
```

---

## 5. Kryptonite Constraint Check

**Does this implementation's primary observable state require specialist mediation for Persona 2
to act on it in the Reactive entry state (90-second ceiling)?**

`[x]` No — the observable states are directly actionable by Persona 2 without specialist translation.

Justification:
- **#885 Zone 1B label:** "Model estimate — verify before citing" is plain English. A finance
  ministry negotiator understands "model estimate" and knows whether her team can verify it in
  the session. She does not need a methodologist to interpret the label. Contrast with
  "Exploratory — do not cite," which caused her to discard a valid argument.
- **#950 Zone 1A Y axis label:** "Score" is plain English. A ministry economist reading a chart
  labeled "Score" on the Y axis understands the axis represents a composite score dimension
  without needing a specialist to interpret the axis.
- **#884, #823, #824:** These backend fixes ensure correct data is returned. Correctness is a
  precondition for any user action; a wrong reserve_coverage_months value or a hardcoded T2 tier
  that should be T3 causes downstream defensibility errors. These are infrastructure fixes
  that enable correct user actions.
- **#22 / PMM anchor:** Documentation is navigable and self-contained. A finance ministry
  economist (Persona 1 archetype) can read the confidence tier methodology and understand what
  T1–T5 means without specialist mediation — that is the explicit design requirement for the
  tier label system (ADR-015 §UX-5).

Kryptonite constraint: satisfied. No G6 output requires the ministry team to engage a fourth
specialist who understands model internals in order to use the G6 deliverables at the table.

---

## 6. Out of Scope

**#22 full distributional bands (Monte Carlo CI intervals):**
The M14 scope of #22 is methodology documentation only — how confidence tiers are assigned
and published. Full CI intervals (bootstrap, Monte Carlo — the `ci_lower`/`ci_upper` fields in
`TrajectoryFrameworkPoint` are currently null and ADR-007-gated) are deferred to M16. No
implementation of statistical uncertainty quantification in G6.

**PMM calibration completion and ADR-007:**
The PMM interpretation anchor documents the pre-calibration status and methodology. It does not
complete the calibration. ADR-007 (PMM calibration) remains future work. Zone 1C PMM annotation
continues to show `[T3 composite · pre-cal]` after G6; the anchor document explains what this
means, not that calibration is done.

**Zone 1B L1 inline expansion (Component 4):**
Deferred to M15 by EL Decision 5. G6 fixes the text of the existing Zone 1B negotiation label —
it does not add any new Zone 1B interaction or inline expansion of alert detail.

**Zone 1A layout redesign (#845, G6c):**
G6 delivers only the Y axis label fix (#950). No layout changes to Zone 1A. The G6c Phase 1
design thinking document (UX Designer deliverable) is separate and not in scope for this intent.

**Water stress elasticity for entities beyond GRC/JOR/EGY/ZMB (#824 scope):**
The biome_class implementation covers only the four M14 ADR-016 entities. Other entities
receive the fallback behavior (WARNING log, no water scarcity elasticity applied) until M15.

**Ecological indicator seeding for all entities:**
G6 ensures reserve_coverage_months appears in /initial-state for JOR/EGY/ZMB. Completing source
attribution for all possible financial indicators on all four entities is out of scope.

---

## 7. Test Authorship Obligation

**QA Lead:** QA Lead Agent
**Test authorship deadline:** Before any G6 implementation PR is opened
**Test file locations:**
- Frontend Playwright E2E: `frontend/tests/e2e/m14-g6-methodology-calibration.spec.ts`
- Backend pytest: `backend/tests/test_m14_g6_methodology_calibration.py`

**AC coverage by test type:**

| AC | Test type | Test file |
|---|---|---|
| AC-1 | Playwright E2E (route mock — T4) | `m14-g6-methodology-calibration.spec.ts` |
| AC-2 | Playwright E2E (route mock — T5) | `m14-g6-methodology-calibration.spec.ts` |
| AC-3 | Playwright E2E OR React unit test | `m14-g6-methodology-calibration.spec.ts` |
| AC-4 | Playwright E2E (zone 1a, any scenario) | `m14-g6-methodology-calibration.spec.ts` |
| AC-5 | pytest + httpx (JOR fixture) | `test_m14_g6_methodology_calibration.py` |
| AC-6 | pytest + httpx (GRC trajectory, step 1) | `test_m14_g6_methodology_calibration.py` |
| AC-7 | pytest + httpx (zero-indicator fixture) | `test_m14_g6_methodology_calibration.py` |
| AC-8 | pytest + httpx (JOR measurement-output, step 1) | `test_m14_g6_methodology_calibration.py` |
| AC-9 | Shell `find` assertion + BPO 5-min nav test | N/A (BPO Step 5 Validate) |

**NM-045 rule (mandatory for all G6 Playwright tests):**
Every AC that asserts a string value ("Model estimate", "Synthetic extrapolation", "Exploratory",
"Score", etc.) MUST be asserted by direct string-presence or string-absence match — not by
structural regex that could match an adjacent element. `expect(text).toContain("Model estimate")`
is correct; `/[A-Z][a-z]+.*(tier|label)/` is not.

**Prerequisite data-testid values (Frontend Architect Agent must confirm before QA test authorship):**

The QA Lead requires the following testids before authoring AC-1, AC-2, AC-3, AC-4:

| Element | Proposed testid | Location |
|---|---|---|
| Zone 1B negotiation defensibility label | `alert-negotiation-label` | Zone 1B detail slot |
| Zone 1A trajectory chart container | `zone-1a-trajectory` | TrajectoryView.tsx outer wrapper |
| Zone 1A Y axis label text | Derived from recharts DOM structure | recharts YAxis label element |

If `alert-negotiation-label` is not currently a `data-testid` on the label element in
`MDAAlertPanelZone1B.tsx`, the Frontend Architect Agent must add it as part of the G6
implementation. QA tests cannot use structural selectors for string assertion.

**AC-3 test note (T1/T2/T3 unchanged):**
AC-3 can be implemented as a React unit test in `MDAAlertPanelZone1B.test.ts` (existing test
file already has `getNegotiationLabel` tests at line 205) — this is faster and does not require
a fixture scenario. The QA Lead may author AC-3 as unit test additions to the existing test
file rather than a new Playwright spec, provided the AC-1/AC-2 Playwright tests cover the live
application state change.

**Backend test fixture requirements:**
- **AC-5 (JOR /initial-state):** The JOR Hormuz scenario from the existing test database (used
  in G3/G4 tests) should work if G6's #884 fix is correctly applied. Chief Engineer confirms
  the JOR scenario ID for the fixture.
- **AC-6 (GRC trajectory ecological tier):** The Greece 2012 scenario fixture is used in
  existing backtesting tests. Chief Engineer confirms the GRC scenario ID and ensures the
  ecological indicators for GRC include at least one T3 indicator (to distinguish derived tier
  from hardcoded T2).
- **AC-7 (zero-indicator null composite):** Requires either a dedicated minimal test entity
  with no ecological boundary constants, or a patched test that removes boundary constants from
  the context dict. Chief Engineer specifies the approach in the implementation.
- **AC-8 (JOR MENA calibration):** Requires the JOR Hormuz scenario to have been advanced at
  least one step with the water scarcity elasticity active. Chief Engineer confirms the fixture.

**Open decisions blocking test authorship:**
DA-G6-1 and DA-G6-2 require Data Architect resolution; CM-G6-1 requires Chief Methodologist
resolution. The Chief Engineer implements once these decisions are recorded. QA tests for
AC-5, AC-6, AC-8 may not be authored until all three decisions are resolved here.

**DA-G6-1 — CONFIRMED 2026-06-18 (Data Architect):**
Canonical key: `water_stress_index`. Convention: consistent with `_{dimension}_index` pattern
(land_use_pressure_index, health_index). Type: RATIO, range [0.0, 2.0] in boundary-proximity
scoring. confidence_tier: 3 (FAO GFR arid-subset/ICARDA — CM+EE approved 2026-06-13).
source_registry_id: `ACADEMIC_LITERATURE_FAO_GFR_ARID_ICARDA_WATER_STRESS` (new registry entry,
Chief Engineer seeds via migration).
Schema updates required in same PR:
- `docs/schema/simulation_state.yml` — add `water_stress_index` to EcologicalModule
  affected_attributes block with full description
- `docs/schema/api_contracts.yml` — add `water_stress_index` QuantitySchema entry under
  measurement-output ecological framework indicators; mark `nullable_when: entity
  biome_class != arid_semiarid`
Update §3.2 Secondary state D: indicator key is `water_stress_index`.

**DA-G6-2 — CONFIRMED 2026-06-18 (Data Architect): OPTION A — Alembic seed migration**
Seed `reserve_coverage_months` as a source-attributed STOCK in the JOR/EGY/ZMB entity seed data
via new or amended Alembic migration. Required Quantity envelope fields:
- `value`: entity-specific initial reserve coverage in months (JOR: ~7.1; EGY/ZMB: from
  Central Bank / IMF BOP source entries from G3 migration `a1b3c5d7e9f2`)
- `unit`: "months", `variable_type`: "stock", `measurement_framework`: "financial"
- `confidence_tier`: 2 (CBJ/CBE official statistics)
- `source_registry_id`: reference existing JOR/EGY/ZMB financial source entries from G3
- `_envelope_version`: "1"
Rationale for rejecting Option B: external sector module initialisation may run AFTER the
step-0 snapshot is written — Option B creates ordering fragility. Option A is deterministic.
`api_contracts.yml` — no new fields required; existing contract at line 977 is satisfied once
migration is applied. Add note: "G6 #884: reserve_coverage_months seeded via OPTION A migration."

**CM-G6-1 — CONFIRMED 2026-06-18 (Chief Methodologist): T3 floor**
Ecological composite minimum tier floor = 3. Derivation: `max(indicator_min_tier, 3)`.
Rationale: the boundary_proximity methodology combines a planetary boundary constant (which
carries its own measurement uncertainty) with entity indicators. `land_use_pressure_index` is T3
(FAO GFR 5-year data with annual interpolation required); `water_stress_index` entering via #824
is T3 (arid-zone proxy). A composite that averages a T1 measurement with T3 proxies cannot be
T2 without misrepresenting the chain. The current hardcoded T2 is incorrect — it has been
labelling the ecological composite as "official statistics, citable directly," which it is not.
Floor may be revised to T2 only at ADR-007 if T2 quality is achieved for both the boundary
constants and the land_use / water_stress indicator series.
AC-6 must assert: GRC ecological composite confidence_tier == 3 (not 2).

**QA Lead acknowledgment:**
`[ ]` QA Lead: Tests for AC-1 through AC-9 authored and filed. [Date]

---

## Appendix: Open Decisions — Data Architect (DA-G6-1, DA-G6-2) and Chief Methodologist (CM-G6-1)

*These decisions must be resolved and recorded here before the backend implementation PR opens.
The Frontend Architect Agent may proceed with AC-1 through AC-4 (frontend only) independently —
no DA or CM decision required for those. Authority for this reassignment: G5 sprint entry
correction PR #1023 ("API field assessment consultation is Data Architect (R on api_contracts.yml),
not Chief Engineer.").*

**DA-G6-1 — Water stress indicator key for #824 (Data Architect):**
The MENA calibration adds a water scarcity elasticity to the ecological module. What is the
canonical `indicator_key` for the water stress indicator? The key must be registered in
`api_contracts.yml` under the ecological framework's measurement-output response before
the new `EcologicalElasticity` entry is added to the registry. Options: `water_stress_index`,
`water_scarcity_ratio`, or a new key. Data Architect updates `api_contracts.yml`; Chief Engineer
implements the registry entry. Update §3.2 Secondary state D with the confirmed key.

**DA-G6-2 — reserve_coverage_months seeding approach for #884 (Data Architect):**
Two implementation paths: (A) Add a step-0 Quantity entry for reserve_coverage_months in the
JOR/EGY/ZMB entity seed data (new or amended Alembic migration), with `source_registry_id`
referencing the entity's financial data source and `measurement_framework=financial`; OR
(B) Attribute the initial value at scenario creation via the external sector module setup path
rather than as a delta event. Data Architect decides which approach is consistent with the
`source_registry` attribution contract and whether `api_contracts.yml` requires any update for
the `/initial-state` response. Chief Engineer implements the chosen path.

**CM-G6-1 — Ecological composite minimum tier floor for #823 (Chief Methodologist):**
The existing governance and financial composites use `_NORMALIZED_ABSOLUTE_MIN_TIER` as a floor.
For the ecological composite, what is the correct minimum tier floor? Options: T2 (same as the
current hardcoded value — consistent with existing boundary constant quality), T3 (conservative
ecological data quality floor), or derive dynamically with no floor. Chief Methodologist records
the decision here and the calibration rationale. Chief Engineer implements the derivation logic.
The AC-6 test asserts the expected composite tier for GRC — cannot be authored until this floor
is confirmed.

---

*Intent document version: 2026-06-18. Authored by implementing agents (Chief Engineer, Frontend
Architect, Chief Methodologist) for M14 G6 — Methodology, Calibration, and Instrument Legibility.
Sprint entry: `docs/process/sprint-plans/m14-g6-sprint-entry.md` (EL approval pending).
CE-G6-1 through CE-G6-3 must be resolved before backend implementation PR opens. AC-1 through
AC-4 (frontend) may proceed after EL sprint entry approval. Full lifecycle authority:
`CLAUDE.md §Agent Execution Lifecycle`.*
