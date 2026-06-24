---
name: M16-G10-predemo-polish
type: implementation-intent
issues: "#1162, #1177, #1178, #1179, #1184"
status: ACTIVE — EL override of G10 sprint entry §2.3 no-intent declaration; intent document required
authored-by: PM Agent (pre-implementation spec; Frontend Developer Agent takes implementation authority at Step 3)
authored-date: 2026-06-24
implementing-agent: Frontend Developer Agent
sprint-entry: "docs/process/sprint-plans/m16-g10-sprint-entry.md — EL Approved 2026-06-24"
adr-reference: "None — all five fixes are bounded rendering changes within existing components; no new architectural surface"
release-branch: release/m16
---

# Implementation Intent: M16-G10 — Pre-Demo Polish

> **Five CA-condition-bounded frontend fixes.** All five issues derive from Customer Agent
> Layer 3 assessments produced at G1, G3, and G4 sprint exits. Each fix is the minimum
> change that satisfies the named CA condition. Scope must not expand beyond what the CA
> condition and observable state together define.
>
> **EL override.** The G10 sprint entry (§2.3) declared that no separate intent document
> was required and that the sprint entry §3.1 observable state declarations would serve as
> the implementation specification. The EL has overridden that declaration. This intent
> document supersedes the §2.3 no-intent ruling and is now the binding specification for
> all five G10 fixes. Test authorship proceeds from this document.
>
> **G8 gate.** All five G10 fixes are G8 pre-conditions (#843 live demo). G8 may not be
> scheduled until the PM Agent confirms all five issues are merged to `release/m16`. This
> intent document gates QA test authorship and implementation PRs for all five issues.
>
> **Recommended batch sequencing (from sprint entry §4 step 3):**
> - Batch A: #1178 + #1184 (badge legibility — same badge component rendering path)
> - Batch B: #1177 + #1179 (trajectory annotation — same 25-year trajectory rendering context)
> - Independent: #1162 (Zone 1A divergence fill — separate component)

---

## 1. Source Authority

All five issues derive from Customer Agent Layer 3 conditions filed at sprint exits. There
is no governing ADR for G10 items — they are bounded fixes within existing component
boundaries established by G1 (ADR-017/ADR-015), G3 (DemographicModule, no ADR), and G4
(ADR-007). The CA source for each issue is the binding specification anchor.

| Issue | CA source | Source sprint exit | Governing component boundary |
|---|---|---|---|
| #1162 | G1 C1 — "Zone 1A divergence fill needs proximate entity attribution anchor before live demo (#843)" | G1 (2026-06-23) | `DivergenceFillLayer` component (Zone 1A) — ADR-017 Phase 4 boundary |
| #1177 | G3 CA-1 — "`[step N]` reference in milestone sentence is technical noise for Persona 5; year anchor sufficient" | G3 (2026-06-24) | Milestone sentence output template / trajectory annotation — G3 scope |
| #1178 | G3 CA-2 — "`T3` badge text not self-interpreting at L0; hover tooltip provides context but not visible without interaction" | G3 (2026-06-24) | Badge/tooltip component — G2/G4 scope (`ConfidenceTierBadge` or equivalent) |
| #1179 | G3 CA-3 — "Q2 curve silence unexplained on-screen; no MDA-HD-POVERTY-Q2 floor is registered (correct) but asymmetry not labeled" | G3 (2026-06-24) | Chart annotation/legend — G3 25-year trajectory rendering context |
| #1184 | G4 CA-G4-1 — `"SAD" badge text not self-interpreting at L0 — needs tooltip or expanded label before Demo 6` | G4 (2026-06-24) | Same badge/tooltip component as #1178 — consistent treatment required |

**Authored by:** PM Agent (pre-implementation spec)
**Date:** 2026-06-24
**Implementing agent:** Frontend Developer Agent (takes implementation authority at Step 3)

---

## 2. Persona Trace Elements Targeted

*G10 is a Demo 6 legibility sprint. All five fixes exist to close Layer 3 quality gaps that
would degrade the live demo experience for Persona 5 on first encounter. Persona 2 is
secondarily affected by #1162 and #1184.*

**P-1 — Personas served:**
- **Persona 5 — Finance Minister** (`docs/ux/personas.md §Persona 5`). Unnarrated session,
  first encounter with the live application. #1177 (milestone sentence year anchor), #1178
  (T3 badge expansion), #1179 (Q2 suppression label), and #1184 (SAD badge expansion) all
  address legibility gaps that surface when Persona 5 encounters specialist notation without
  a guide to translate it.
- **Persona 2 — Finance Ministry Negotiator** (`docs/ux/personas.md §Persona 2`). Operational
  user in Reactive state (90-second ceiling). #1162 (divergence fill attribution) and #1184
  (SAD badge expansion) close gaps that surface when Persona 2 reads Zone 1A and Zone 1B
  without prior familiarity with the current rendering.

**P-2 — Entry state:**
Reactive (90-second ceiling) — all five fixes are evaluated against the unnarrated Demo 6
walkthrough. The Finance Minister and the negotiator team are in first-encounter Reactive
state during the live demo session.

**P-3 — Journey reference:**
Demo 6 — Senegalese Finance Minister scenario (Article IV consultation, 2026). The analyst
team loads the SEN scenario in Mode 1, navigating Zone 1A (trajectory), Zone 1B (cohort
impact + milestone sentence), and Zone 1D (political risk) without narration. All five
G10 fixes address legibility failures that appear in this walkthrough.

**P-4 — Time/interaction ceiling:**
90-second Reactive state ceiling. Each G10 fix must be legible with zero additional user
interaction beyond what the Demo 6 walkthrough already requires. No hover-only, no click-
to-reveal, no drawer navigation for primary interpretation.

**P-6 — Negotiating leverage delivered (Persona 2):**

*#1162:* Persona 2 can identify which entity pair a Zone 1A divergence fill represents
without cross-referencing a legend or hovering over a line — the attribution is present
in the default viewport state. In the Demo 6 context, this prevents the zone from appearing
to show unexplained shaded regions, which would undermine the precision of the distributional
argument at the table.

*#1184:* Persona 2 can correctly understand that a "SAD" badge means "no primary data
exists for this entity and indicator" — not a low-confidence estimate — without specialist
mediation. This distinction matters in the consultation: citing a Structural Absence
Declaration ("the World Bank does not have primary poverty headcount data for Senegal for
this cohort") is a more credible position than citing an unknown "SAD" flag.

**P-7 — North Star capability delivered:**
Before G10: a Finance Minister in an unnarrated Demo 6 walkthrough would encounter "T3",
"SAD", "[step 12]", and unlabeled shaded fills — notation that requires specialist
interpretation not available to the minister without a guide. After G10: each of these
elements is self-interpreting at L0 — the minister's analyst can cite the 25-year milestone
in calendar years, understand what tier badges mean without hover, see why Q2 data is absent,
and identify which entity pair a divergence fill represents, all within the 90-second ceiling.

---

## 3. Observable Application State

*All states verifiable by an external observer using only the running application.
No source code reading, no CI report reference, no implementation knowledge required.*

---

### 3.1 — #1162: Zone 1A divergence fill attribution anchor

**State 1 — Attribution visible in default viewport state:**
In Zone 1A, when a divergence fill is rendered between two entity trajectories (e.g., SEN
trajectory A vs. SEN trajectory B in a two-branch comparison), an element with
`data-testid="divergence-fill-attribution"` is present in the DOM and has a non-zero
`getBoundingClientRect` (visible, not hidden) without any user gesture. The element contains
text identifying the entity pair (e.g., "SEN Branch A vs. Branch B" or an equivalent label
derived from the entity/branch identifiers). The attribution is visible in the default
(non-hover, non-interaction) viewport state at 1280×800 and 1440×900.

**State 2 — Attribution absent when no divergence fill is rendered:**
In Zone 1A with a single-entity, single-branch trajectory (no comparison active),
`data-testid="divergence-fill-attribution"` is either absent from the DOM or has
`display: none`. The attribution element does not appear when there is no divergence fill.

---

### 3.2 — #1177: Milestone sentence step-reference → year anchor

**State 3 — Calendar year in milestone sentence:**
In Zone 1B (or trajectory annotation, whichever surface displays the 25-year milestone
sentence from G3), the element with `data-testid="milestone-sentence"` contains a calendar
year (e.g., "by 2030", "by 2038", "by 2049") derived from the scenario start date and step
resolution. The string pattern `[step` followed by a digit does not appear as the sole
time reference in this element. The year resolves correctly: for a scenario starting in
2024 with quarterly step resolution, step 24 maps to "by 2030" (6 years).

**State 4 — Step reference may coexist but is not the primary temporal anchor:**
If the implementing agent chooses to retain `[step N]` as a secondary annotation (e.g.,
"by 2030 [step 24]"), the calendar year must appear first and the step reference must be
visually subordinate (smaller, lower contrast, or parenthetical). The calendar year is the
primary anchor; the step reference is supplementary. `data-testid="milestone-sentence"`
content starts with the year-anchored phrase.

---

### 3.3 — #1178: T3 badge L0 legibility

**State 5 — T3 badge expanded label visible at L0:**
The confidence tier badge for a Tier 3 indicator displays an expanded label legible
without hover or interaction. One of the following must be present at L0:

(a) `data-testid="confidence-tier-badge"` contains text "T3 — Inferred" (or "T3 —
Synthetic estimate" if the indicator is synthetic — the expansion must accurately reflect
the tier type), or

(b) An element with `data-testid="confidence-tier-badge-sublabel"` is present immediately
adjacent to the badge and contains the tier meaning in plain language (e.g., "Inferred
from comparable economies"), visible without hover, with a non-zero `getBoundingClientRect`.

Hover tooltip may remain as supplementary detail but must not be the sole source of
interpretation. The choice of (a) or (b) is the implementing agent's; the QA test targets
whichever form is implemented and the implementing agent documents the choice.

**State 6 — T3 badge legibility at 1280×800 and 1440×900:**
At both viewport sizes, the expanded label or sub-label is visible without scroll, without
hover, and without zone resize. It does not displace or overlap any Zone 1B or Zone 1D
content rows. A new `getBoundingClientRect` check confirms no overlap with adjacent
cohort row text.

---

### 3.4 — #1179: Q2 curve asymmetry label

**State 7 — Q2 suppression explanation visible without interaction:**
In the 25-year human capital trajectory display (Zone 1B or its extended panel from G3),
when the Q2 (second quintile) poverty headcount trajectory is absent or suppressed (because
no MDA floor is registered for Q2), an on-screen explanation is present without hover or
drawer navigation. One of the following must be present:

(a) A legend entry with `data-testid="q2-suppression-legend"` containing text explaining
the suppression (e.g., "Q2 — no floor threshold registered", "Q2 suppressed: floor not
defined", or equivalent), or

(b) A chart annotation with `data-testid="q2-suppression-annotation"` positioned at or
near where the Q2 curve would appear, containing the suppression explanation.

The explanation must be visible in the default viewport state at 1280×800 and 1440×900
without any user gesture.

**State 8 — Explanation absent when Q2 is not suppressed:**
If a scenario configuration produces a Q2 curve (Q2 floor is registered and data is
present), the suppression annotation/legend entry is not present. The annotation must
not appear for non-suppressed indicators.

---

### 3.5 — #1184: SAD badge L0 legibility

**State 9 — SAD badge expanded label visible at L0:**
The Structural Absence Declaration badge displays an expanded label legible without hover
or interaction. Treatment must be consistent with #1178 (T3 badge) — the same component
rendering pattern must be used for both badges. One of the following must be present:

(a) `data-testid="sad-badge"` (or `data-testid="confidence-tier-badge"` if SAD uses the
same badge component) contains text "SAD — Structural Absence" (or "SAD — No primary data"),
not bare "SAD", or

(b) An element with `data-testid="sad-badge-sublabel"` (or `data-testid="confidence-
tier-badge-sublabel"`) is present immediately adjacent to the badge and contains the SAD
meaning in plain language (e.g., "No primary data for this entity"), visible without hover.

**Consistency requirement:** If #1178 implements sub-label option (b), #1184 must also
implement sub-label option (b) using the same component. If #1178 implements inline
expansion option (a), #1184 must also implement inline expansion option (a). The
implementing agent documents the choice in the PR description.

**State 10 — SAD badge legibility at 1280×800 and 1440×900:**
At both viewport sizes, the expanded label or sub-label is visible without scroll, without
hover, and without zone resize. No overlap with adjacent cohort row text or Zone 1D rows.

---

### 3.6 — Silent failure detection

**Silent failure 1 — Attribution still hover-only (#1162):**
If the attribution element exists but is only visible on hover (e.g., a tooltip class
applied to the fill element), `getBoundingClientRect` at rest will report a zero-height
or zero-width element. Detection: AC-1 asserts non-zero `getBoundingClientRect` without
any `hover()` call — if the attribution is hover-only, this assertion fails.

**Silent failure 2 — Step reference survives as primary anchor (#1177):**
If the milestone sentence template is updated but `[step N]` is not removed or subordinated,
the regex pattern `\[step \d+\]` will still match as the leading/only time reference.
Detection: AC-3 asserts that `data-testid="milestone-sentence"` text matches a year pattern
(4-digit number) and does not match the `[step N]` pattern as a standalone string at the
start of the element.

**Silent failure 3 — Badge expansion tooltip-only (#1178 and #1184):**
If the expansion is delivered as a hover tooltip only (CSS `:hover` or `title` attribute),
the expansion text will not appear in the DOM at rest. Detection: AC-5 and AC-9 assert that
the expanded text is present in the DOM (`textContent` check) without any prior `hover()`
call in the Playwright test sequence.

**Silent failure 4 — Q2 annotation only fires in the wrong scenario context (#1179):**
If the suppression annotation is tied to a particular scenario fixture that happens to
suppress Q2, but fails to render in a different valid suppression context, the fix is
partially implemented. Detection: AC-7 uses a fixture where no Q2 MDA floor is registered,
and AC-8 uses a fixture where Q2 floor is registered — both assertions must hold.

---

## 4. Acceptance Criteria

*Each criterion verifiable by an external observer using only the running application.
"CI passes" is not an AC.*

---

### #1162 — Zone 1A divergence fill attribution anchor

*Test file: `frontend/tests/e2e/m16-g10-predemo-polish.spec.ts` (or extend
`frontend/tests/e2e/m16-g1-zone1a-phase4-composite.spec.ts`), describe block `#1162`*

**AC-1 — Attribution anchor visible at rest in comparison rendering:**
With two entity trajectories loaded in Zone 1A (any SEN or ZMB two-branch comparison
fixture), `page.locator('[data-testid="divergence-fill-attribution"]')` is present and
`getBoundingClientRect().height > 0` and `getBoundingClientRect().width > 0` — without
any `hover()`, `click()`, or drawer navigation. The element's `textContent` contains the
entity or branch identifier(s) for the active divergence fill.

**AC-2 — Attribution absent in single-entity rendering:**
With a single-entity, single-branch trajectory loaded in Zone 1A (no comparison active),
`page.locator('[data-testid="divergence-fill-attribution"]')` either does not exist in
the DOM or has `getBoundingClientRect().height === 0`. No spurious attribution label
appears in the default single-entity view.

---

### #1177 — Milestone sentence step-reference → year anchor

*Test file: `frontend/tests/e2e/m16-g10-predemo-polish.spec.ts` (or extend
`frontend/tests/e2e/m16-g3-25year-human-capital-trajectory.spec.ts`), describe block `#1177`*

**AC-3 — Milestone sentence contains calendar year:**
With the G3 25-year trajectory panel rendered for the SEN scenario at default step
resolution: `page.locator('[data-testid="milestone-sentence"]').textContent()` matches the
regex `/\b(20\d{2})\b/` (a 4-digit year in the 2000s). The textContent does not match
`/^\[step \d+\]/` (does not begin with a bare step reference as the sole time anchor).

**AC-4 — Year resolves correctly for scenario start date:**
With a scenario configured with start year 2024 and quarterly step resolution: the milestone
sentence references year 2030 (step 24 → 6 years from 2024) or the year corresponding to
the step where the trajectory crosses the named threshold — whichever applies per G3
milestone logic. The year is not hardcoded; it derives from the scenario's start date and
step resolution configuration.

---

### #1178 — T3 badge L0 legibility

*Test file: `frontend/tests/e2e/m16-g10-predemo-polish.spec.ts`, describe block `#1178`*

**AC-5 — T3 badge expanded label present in DOM at rest:**
With a Zone 1B cohort row displaying a Tier 3 (T3) badge: the expanded label text
("T3 — Inferred", "T3 — Inferred", "Inferred from comparable economies", or equivalent
per implementing agent's choice) is present in the DOM — either within
`data-testid="confidence-tier-badge"` textContent or within
`data-testid="confidence-tier-badge-sublabel"` — without any prior `hover()` or `click()`
call. The `textContent` of the badge or sub-label element is not empty.

**AC-6 — T3 badge legibility at both breakpoints:**
At viewport `1280×800`: the badge and its expanded label are visible (non-zero
`getBoundingClientRect`) and do not overlap any cohort row text (no bounding box
intersection with `data-testid="cohort-row-value"` elements). Repeat at `1440×900`.

---

### #1179 — Q2 curve asymmetry label

*Test file: `frontend/tests/e2e/m16-g10-predemo-polish.spec.ts`, describe block `#1179`*

**AC-7 — Q2 suppression annotation visible when Q2 floor is unregistered:**
With the G3 25-year trajectory rendered for a fixture where no MDA floor is registered
for poverty_headcount_ratio Q2: one of the following is present and visible at rest
(non-zero `getBoundingClientRect`):
- `page.locator('[data-testid="q2-suppression-legend"]')` with textContent containing
  "Q2" and a suppression/floor-related word (e.g., "floor", "suppressed", "not registered"),
- OR `page.locator('[data-testid="q2-suppression-annotation"]')` with equivalent content.
No `hover()` or drawer navigation required.

**AC-8 — Q2 suppression annotation absent when Q2 floor is registered:**
With a fixture where a Q2 MDA floor is registered and Q2 trajectory data is present:
neither `data-testid="q2-suppression-legend"` nor `data-testid="q2-suppression-annotation"`
is present in the DOM (or both have `display: none`). The annotation does not appear when
Q2 is not suppressed.

---

### #1184 — SAD badge L0 legibility

*Test file: `frontend/tests/e2e/m16-g10-predemo-polish.spec.ts`, describe block `#1184`*

**AC-9 — SAD badge expanded label present in DOM at rest:**
With a Zone 1B cohort row displaying a Structural Absence Declaration (SAD) badge
(i.e., `is_synthetic=True`, `synthetic_method="STRUCTURAL_ABSENCE"`): the expanded label
text ("SAD — Structural Absence", "SAD — No primary data", or equivalent) is present in
the DOM without any prior `hover()` or `click()`. The implementation uses the same badge
component pattern as AC-5 (#1178): if #1178 uses sub-label, #1184 uses sub-label; if
#1178 uses inline expansion, #1184 uses inline expansion.

**AC-10 — SAD badge consistency with T3 badge (same component, same pattern):**
The Playwright test confirms that both `data-testid="confidence-tier-badge-sublabel"` (or
the inline expansion element, per implementing agent's choice) appears for the T3 fixture
(AC-5) and the SAD fixture (AC-9) using the same selector and the same DOM structure —
not two different rendering mechanisms. The implementing agent documents in the PR
description which pattern was chosen and why.

**AC-11 — SAD badge legibility at both breakpoints:**
At viewport `1280×800` and `1440×900`: the SAD badge and its expanded label are visible
(non-zero `getBoundingClientRect`) and do not overlap adjacent cohort row content.

---

## 4b. Visual Spec (before/after)

*All G10 fixes are display-format changes. Before/after visual specs are required per
`docs/process/intent-template.md §4b`.*

---

### AC-1/AC-2 — #1162: Divergence fill attribution anchor

**AC-1 (before — attribution absent, fill unexplained):**
```
Zone 1A at 1280×800, two-branch SEN comparison:

┌──────────────────────────────────────────────────────────────────┐
│ Zone 1A — SEN trajectory                                         │
│                                                                  │
│   ════════════════════════════════════════  [Branch A line]     │
│   ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  [divergence fill]  │
│   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─  [Branch B line]     │
│                                                                  │
│   [No label. User must hover the fill to learn what it is.]     │
│            ^^^^ THIS IS THE BUG                                 │
└──────────────────────────────────────────────────────────────────┘
```

**AC-1 (after — attribution visible at L0):**
```
Zone 1A at 1280×800, two-branch SEN comparison:

┌──────────────────────────────────────────────────────────────────┐
│ Zone 1A — SEN trajectory                                         │
│                                                                  │
│   ════════════════════════════════════════  [Branch A line]     │
│   ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  [divergence fill]  │
│                  ▲ "SEN — Branch A vs. Branch B"               │
│   [data-testid="divergence-fill-attribution"]                   │
│   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─  [Branch B line]     │
│                                                                  │
│   Attribution visible at rest — no hover required ✓             │
└──────────────────────────────────────────────────────────────────┘
```

---

### AC-3/AC-4 — #1177: Milestone sentence year anchor

**AC-3 (before — step reference as sole temporal anchor):**
```
Zone 1B at 1280×800, 25-year trajectory, SEN scenario:
[data-testid="milestone-sentence"]

Current text:
  "Human capital depletion reaches critical threshold at [step 24]"
                                                          ^^^^^^^^
                                         THIS IS THE BUG — technical noise
                                         for Persona 5; year required
```

**AC-3 (after — calendar year as primary anchor):**
```
Zone 1B at 1280×800, 25-year trajectory, SEN scenario:
[data-testid="milestone-sentence"]

Fixed text (option a — year only):
  "Human capital depletion reaches critical threshold by 2030"
                                                        ^^^^
                                         Calendar year — self-interpreting ✓

Fixed text (option b — year primary, step supplementary):
  "Human capital depletion reaches critical threshold by 2030 (step 24)"
                                                        ^^^^
                                         Year leads; step is parenthetical ✓
```

---

### AC-5/AC-6 — #1178: T3 badge L0 legibility

**AC-5 (before — bare abbreviation, meaning hover-only):**
```
Zone 1B COHORT IMPACT at 1280×800:
[data-testid="cohort-tier-badge"] textContent: "T3"
                                               ^^^
                   Bare abbreviation — tooltip only on hover
                   Persona 5 first encounter: uninterpretable ↑ THIS IS THE BUG

Hover tooltip (not visible at L0): "Tier 3 — Inferred from comparable economies"
```

**AC-5 (after — option a: inline expansion):**
```
Zone 1B COHORT IMPACT at 1280×800:
[data-testid="confidence-tier-badge"] textContent: "T3 — Inferred"
                                                    ^^^^^^^^^^^
                           Self-interpreting at L0 — no hover required ✓

Hover tooltip may remain for supplementary detail.
```

**AC-5 (after — option b: sub-label):**
```
Zone 1B COHORT IMPACT at 1280×800:

  [T3]
  [data-testid="confidence-tier-badge"] textContent: "T3"
  Inferred from comparable economies
  [data-testid="confidence-tier-badge-sublabel"] textContent: "Inferred from comparable economies"
  — visible without hover, non-zero getBoundingClientRect ✓
```

*Implementing agent chooses (a) or (b) and documents in PR description. QA tests target
whichever form is implemented.*

---

### AC-7/AC-8 — #1179: Q2 curve asymmetry label

**AC-7 (before — Q2 absence silent):**
```
Zone 1B 25-year trajectory at 1280×800, Q2 suppressed:

Q1 curve: ══════════════════════════════════════════════
Q2 curve: [ABSENT — no MDA floor registered for Q2]
Q3 curve: ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─
                   ↑
       Gap between Q1 and Q3 — no explanation visible
       Persona 5: "Is Q2 missing? Is the chart broken?"
       THIS IS THE BUG
```

**AC-7 (after — Q2 suppression labeled):**
```
Zone 1B 25-year trajectory at 1280×800, Q2 suppressed:

Q1 curve: ══════════════════════════════════════════════
[data-testid="q2-suppression-legend"]
  ⚬ Q2 — floor threshold not registered (suppressed)
Q3 curve: ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

Legend annotation visible at L0 — no hover required ✓
Absence is labeled, not silent ✓
```

---

### AC-9/AC-10/AC-11 — #1184: SAD badge L0 legibility

**AC-9 (before — bare "SAD" abbreviation, meaning hover-only):**
```
Zone 1B COHORT IMPACT at 1280×800, SEN indicator with Structural Absence:
[data-testid="sad-badge"] textContent: "SAD"
                                       ^^^
                  Bare abbreviation — tooltip only on hover
                  Persona 5 first encounter: "What is SAD?"
                  Specialist mediation required ↑ THIS IS THE BUG
```

**AC-9 (after — consistent with #1178 treatment):**
```
Zone 1B COHORT IMPACT at 1280×800, SEN indicator with Structural Absence:

Option a (inline expansion — consistent with #1178 option a):
[data-testid="confidence-tier-badge"] textContent: "SAD — Structural Absence"
                                                    ^^^^^^^^^^^^^^^
                                    Self-interpreting at L0 ✓

Option b (sub-label — consistent with #1178 option b):
  [SAD]
  No primary data for this entity
  [data-testid="confidence-tier-badge-sublabel"] — visible at L0 ✓

Same DOM structure as #1178 — same component, same selector, consistent pattern ✓
```

---

## 5. Kryptonite Constraint Check

*Authority: `docs/process/agent-execution-lifecycle.md §Kryptonite Design Constraint (FD-3)`.*

**Does any G10 deliverable's primary observable state require specialist mediation for
Persona 5 or Persona 2 to act on it in the Reactive entry state (90-second ceiling)?**

`[x]` **No** — these fixes exist specifically to eliminate the specialist mediation
requirement identified at sprint exit. Each fix is a direct Layer 3 remediation:
the CA condition named the specialist mediation gap, and the fix closes it at L0.

**Per issue:**
- #1162: Attribution anchor eliminates the need to hover-to-learn which entity pair
  the fill represents. No specialist mediation required after the fix.
- #1177: Calendar year eliminates the need to know step resolution to interpret time.
  A Finance Minister understands "by 2030" without a briefing.
- #1178: The expanded T3 label ("T3 — Inferred" or "Inferred from comparable economies")
  communicates tier meaning in plain language. No statistics expertise required.
- #1179: The Q2 legend note ("floor not registered — suppressed") explains the absence
  in plain language. No methodology expertise required to understand why the curve is absent.
- #1184: The expanded SAD label ("SAD — Structural Absence" or "No primary data for this
  entity") converts an opaque badge into a self-explanatory statement.

**No EL exception required.** All five fixes are designed to satisfy the kryptonite
constraint, not to work around it.

---

## 6. Out of Scope

| Scope item | Rationale for exclusion |
|---|---|
| Zone 1A divergence fill colouring or trigger logic (#1162) | CA condition names attribution only; fill rendering is correct and within G1 scope |
| Milestone sentence backend projection logic (#1177) | Fix is in the output template/rendering function only; backend step-to-date logic is unchanged |
| Confidence tier logic or data storage (#1178) | Fix is badge component rendering only; tier assignment logic is unchanged |
| MDA floor registration logic (#1179) | The floor's absence is correct; the fix is labeling the absence, not changing the logic |
| Suppression logic for cohort indicators (#1179) | ADR-007 §Section 5 and G2 suppression rules unchanged; this fix adds a label, not a behavior change |
| SAD logic or SyntheticDataEngine behavior (#1184) | Fix is badge component rendering only; Structural Absence Declaration firing logic is unchanged |
| Full badge system redesign or design-language audit | G10 scope is the minimum fix for #1178 and #1184 per sprint entry §3.2; systematic redesign is future work |
| Zone 1A/1B/1D layout changes | All five G10 fixes are text/label additions — no layout restructuring |
| Any backend changes | All five G10 fixes are frontend rendering changes only |
| G1/G2/G3/G4 scoped items | Those sprint groups are closed; G10 must not modify files beyond the five fix boundaries |
| ADR-017 P-6 per-framework delta baseline (G1 C3) | Scope-alignment note in G1 exit; not a G10 item |
| CA-G4-2 Zone 1D badge wiring deferral (#22 AC-F6) | Forward gap per G4 intent §6 deferral clause; no Demo 6 impact; not a G10 item |

---

## 7. Test Authorship Obligation

**QA Lead:** QA Lead Agent
**Test authorship deadline:** Before any G10 implementation PR is opened against `release/m16`
**Test file location:** `frontend/tests/e2e/m16-g10-predemo-polish.spec.ts`
(or extend `frontend/tests/e2e/m16-g1-zone1a-phase4-composite.spec.ts` for #1162 and
`frontend/tests/e2e/m16-g3-25year-human-capital-trajectory.spec.ts` for #1177/#1179 —
implementing agent specifies the extension strategy in the PR; QA Lead authors accordingly)

**All ten ACs are available for immediate test authorship.** No PENDING conditions block
QA test authorship for any G10 item.

**ACs by issue:**
- #1162: AC-1, AC-2
- #1177: AC-3, AC-4
- #1178: AC-5, AC-6
- #1179: AC-7, AC-8
- #1184: AC-9, AC-10, AC-11

**Implementation choice documentation requirement:**
Before QA Lead authors AC-5/AC-9 (badge expansion), the implementing agent must confirm
which pattern was chosen (inline expansion or sub-label) and which `data-testid` values
will be used. QA Lead tests against the confirmed choice. If implementing #1178 and #1184
together (recommended per sprint entry), one confirmation covers both.

**Pre-push gates mandatory before each push:**
- Frontend: `cd frontend && npm run build` — must exit 0 before any push modifying `frontend/src/`

**Soft-skip guard (NM-056 follow-up):**
No test in `m16-g10-predemo-polish.spec.ts` may contain `test.skip()` or conditional skip
patterns. All ten ACs must run and pass in CI before the last G10 PR merges.

**QA Lead acknowledgment:**
`[x]` QA Lead: Tests for AC-1 through AC-11 authored and filed 2026-06-24 in `frontend/tests/e2e/m16-g10-predemo-polish.spec.ts` — before first G10 implementation PR opens.

---

## 8. Step 4 Verify Record

*To be completed by the implementing agent before marking each implementation PR ready for review.*

**Verify date:** [pending]
**Verifier:** Frontend Developer Agent
**PRs:** [pending — up to three PRs per sprint entry §4 sequencing: Batch A (#1178+#1184),
Batch B (#1177+#1179), Independent (#1162)]

*Required verify elements before each PR is marked ready:*
- Confirm the relevant observable states in §3 are present in the running application
  at both 1280×800 and 1440×900
- Confirm no adjacent Zone content is displaced or overlapped (visual regression check)
- Confirm the soft-skip guard: no `test.skip()` in the authored test file
- Confirm frontend build exits 0 (`cd frontend && npm run build`)

---

*Intent document authority: `docs/process/intent-template.md` (version 2026-06-17).
Sprint entry: `docs/process/sprint-plans/m16-g10-sprint-entry.md` (EL Approved 2026-06-24).
This document supersedes the no-intent declaration in sprint entry §2.3 per EL direction.
Implementing agent: Frontend Developer Agent (Step 3 authority).
All five fixes are frontend rendering changes only — no backend involvement, no new ADR.*
