---
name: M16-G2-distributional-surface
type: implementation-intent
issues: "#986, #987, #1163"
status: Filed 2026-06-23 — QA tests must be authored before implementation PR opens
authored-by: Frontend Architect Agent
authored-date: 2026-06-23
implementing-agent: Frontend Architect Agent
sprint-entry: "docs/process/sprint-plans/m16-g2-sprint-entry.md — EL Approved 2026-06-23"
adr-reference: "ADR-017 (Zone 1A/1D Information Architecture); ADR-015 (Model Legibility Architecture); ADR-014 (Alert Panel Zone 1B)"
release-branch: release/m16
---

# Implementation Intent: M16-G2 — Distributional Visibility on Primary Surface

> **Three issues, one document.** #986 (cohort disaggregation — Zone 1B), #987 (political
> risk summary — Zone 1D), and #1163 (PSP threshold legibility — closed by #987) are G2's
> three issues. They ship in a single PR because they share a layout change (Zone 1B/1C/1D
> proportion rebalance from DD-016), an implementing agent, and a sequential dependency (#987
> Zone 1D changes must not conflict with #986 Zone 1B changes in the same component tree
> render cycle). #1163 has no separate observable state — its acceptance is embedded in #987's
> AC-8 (PSP severity labels make the absolute PSP level self-interpreting). Splitting these
> into three intent documents would allow a PR to satisfy Zone 1B without the layout rebalance,
> or satisfy the layout rebalance without retiring the G1 testids — both silent failures.

---

## 1. Source ADRs and Design Authorities

**Primary ADR — Zone 1D:** ADR-017 — Zone 1A Information Architecture
**Companion ADR — Zone 1D evidence thread:** ADR-015 — Model Legibility Architecture
**Zone 1B authority:** ADR-014 — Alert Panel Zone 1B master-detail
**Layout authority:** `docs/frontend/fa-brief-m16-g2-zone-1d-layout.md` (DD-016)

**Status at time of authorship:** All accepted.

**Authored by:** Frontend Architect Agent
**Date:** 2026-06-23
**Implementing agent:** Frontend Architect Agent

**Issues in scope:**

| Issue | Title | Authority |
|---|---|---|
| #986 | feat(ux): cohort disaggregation on primary surface | `docs/ux/design-thinking/cohort-disaggregation-design.md` (UX Designer Agent, 2026-06-21) |
| #987 | feat(ux): political risk summary surface (Persona 3) | `docs/ux/design-thinking/political-risk-summary-design.md` (UX Designer Agent, 2026-06-21) |
| #1163 | ux(zone-1d): PSP threshold anchor — absolute PSP level legibility | Resolved by #987 severity-labeled display; closes when #987 implementation merges |

**Key M16 scope restriction (DA sign-off, #986):** The DemographicModule's ELASTICITY_REGISTRY
contains entries only for `poverty_headcount_ratio` (Q1 informal, Q2 informal, Q1 agriculture).
No entries exist for `school_enrollment_rate` or `child_malnutrition_rate`. The M16 scope for
#986 is limited to poverty headcount ratio by income quintile. School enrollment and child
malnutrition are M17 scope. Q3, Q4, Q5 quintiles produce zero delta in the engine (no elasticity
rows) and are suppressed from display as T5 (no data) — they are never shown as zero.

---

## 2. Persona Trace Elements Targeted

*Derived from `docs/ux/personas.md`, design documents, and customer agent assessment.*

**P-1 — Personas served:**
- **Persona 2 — Finance Ministry Negotiator** (Aicha Mbaye archetype). Primary for #986: Aicha
  must be able to state at the table "Under current conditionality, the bottom income quintile
  crosses the poverty headcount threshold at step 2" — reading this from Zone 1B without a data
  economist present.
- **Persona 3 — Political Advisor** (Andreas Stefanidis archetype, `docs/ux/personas.md §Persona 3`).
  Primary for #987: Andreas must read the full political risk situation (PSP, legitimacy, elite
  capture) from Zone 1D within 30 seconds, without knowing what "PSP" stands for or what
  threshold values are "bad."
- **Persona 5 — External Review / Institutional Partner.** Secondary for #987: an external
  partner reviewing the scenario output can read "Programme survival: CRITICAL (38%) — DECLINING"
  without WorldSim expertise.

**P-2 — Entry state:**
Reactive entry state (90-second total ceiling, negotiating room context, Journey B).
#986 ceiling: read Zone 1B cohort threshold row within 15 seconds of scenario loading.
#987 ceiling: read full Zone 1D political risk sub-section within 30 seconds of step advance.

**P-3 — Journey references:**
- Journey B Step 3 [Near-Term-Gap]: Persona 2 defends a challenged output — #986 provides the
  cohort threshold argument (which quintile, which indicator, which step) without Zone 2B navigation.
- Journey A Step 2 [Preparatory]: Persona 3 checks political risk position before session — #987
  provides the self-interpreting summary without political economy expertise.

**P-4 — Time or interaction ceiling:**
- #986 cohort row read: **15 seconds**, zero interaction beyond scenario load
- #987 political risk sub-section read: **30 seconds**, zero interaction (L0 display)
- Both capabilities operate at L0 — no hover, no click, no expand

**P-6 — Negotiating leverage delivered (Persona 2 and Persona 3):**

*#986 (Persona 2):*
After accessing Zone 1B in Mode 2 with the ZMB ECF fixture at step 2, Persona 2 can state:
"Under current conditionality, the bottom income quintile crosses the poverty headcount threshold
at step 2 — this is confirmed by the simulation's historical elasticity estimates. The bottom
quintile was within 3.8 percentage points of the CRITICAL floor at the previous step." This
argument is speakable at the table and does not require a data economist present to translate.

*#987 (Persona 3):*
After accessing Zone 1D in Mode 2 with the ZMB ECF fixture at step 3, Persona 3 can state:
"Programme survival is at 38% and declining — CRITICAL. Historical programmes at this level show
abandonment within 3 steps. Legitimacy is declining and 0.07 above the fragility threshold.
Fiscal benefits are concentrating, not distributing." This is readable within 30 seconds without
knowing what PSP stands for or what makes 38% bad.

**P-7 — North star capability delivered:**
The Zambia ministry analyst at step 3 in Mode 2 can now simultaneously read: (1) from Zone 1B —
which income cohort is most affected and whether it has crossed a threshold; (2) from Zone 1D —
whether the programme will survive and whether political legitimacy is holding. Both reads are
at L0, within 30-second Reactive ceiling, without specialist mediation. The two capabilities
together answer the full "human cost + political risk" question that the finance minister must
answer at the table.

---

## 3. Observable Application State

*All states verifiable by an external observer using the running application at 1280×800
minimum viewport width with the ZMB 2023–2024 IMF ECF fixture, political economy module
enabled. No source code reading required.*

### 3.1 Primary observable state — Zone 1B Cohort Impact sub-section (#986)

At **1280×800**, ZMB ECF fixture loaded in **Mode 2**, political economy enabled, advanced to
**step 2**:

Zone 1B (`data-testid="zone-1b"`) contains a `data-testid="zone-1b-cohort-impact"` element
below the MDA aggregate alerts, separated by a horizontal rule labeled "COHORT IMPACT".

The first row of the Cohort Impact sub-section (`data-testid="cohort-row-0"`) displays in this
exact format:

```
CRITICAL   Bottom income quintile — Poverty headcount
           Threshold crossed at step 2 · was X% above floor · T3 · [source citation]
```

Where:
- "CRITICAL" is a severity badge (red, same visual treatment as MDA aggregate severity badges)
- "Bottom income quintile" is the plain-language label for Q1 (never "hh_exp_q1" or "Q1")
- "Poverty headcount" is the plain-language label for poverty_headcount_ratio (never the field key)
- "T3" is the tier label (never "T2" — elasticity-derived from Lustig 2017/Ball 2013 is T3)
- The source citation is present and non-empty

No Q3, Q4, or Q5 cohort rows appear in Zone 1B — they are suppressed (T5/no-data is not displayed).

At **step 0** (no steps advanced): the sub-section shows the empty state message
(`data-testid="cohort-empty-state"`) — "No cohort threshold crossings at or before this step."
in Mode 1, or "No cohort threshold crossings projected on current path." in Mode 2.

### 3.2 Secondary observable states

**State A — Zone 1D political risk sub-section (#987):**

At **1280×800**, ZMB ECF fixture in **Mode 2**, political economy enabled, **step 3** (PSP=0.38):

Zone 1D contains `data-testid="zone-1d-political-risk"` below the four-framework rows. The
sub-section header `data-testid="zone-1d-political-risk-header"` shows "POLITICAL RISK" with a
preceding horizontal divider. The sub-section contains exactly:

```
Programme survival: CRITICAL (38%) — DECLINING    [data-testid="psp-severity-row"]
At this level, historical ECF programmes show abandonment within 3 steps.
                                                  [data-testid="psp-historical-analogue"]

Legitimacy index: 0.42 — declining (floor: 0.35) [data-testid="legitimacy-index-row"]
  0.07 above fragility threshold                  [data-testid="legitimacy-floor-proximity"]

Elite capture divergence: widening — fiscal benefits concentrating
                                                  [data-testid="elite-capture-row"]
```

The G1 testids `zone-1d-political-feasibility`, `psp-delta`, `psp-layer3-sentence`, and
`psp-delta-sentence` are **absent from the DOM** — these elements are retired by G2.

At 1280×800: all four framework rows AND the political risk sub-section header AND the first
political risk element (`psp-severity-row`) are visible within the Zone 1D height (160px)
without scroll. The `overflow-y: auto` property allows scroll to reach lower elements.

The Zone 1D container has `flex: 0 0 50%` at 1280 (yielding 160px of chartHeight=320px).

**State B — PSP severity thresholds (#987, #1163):**

For four PSP value ranges, the severity badge and historical analogue in `psp-severity-row`
and `psp-historical-analogue` must match:

| PSP value | Severity badge text | Historical analogue |
|---|---|---|
| PSP = 0.38 (< 0.40) | "CRITICAL" | "...show abandonment within 3 steps." |
| PSP = 0.47 (0.40–0.55) | "WARNING" | "...show abandonment within 6 steps." |
| PSP = 0.62 (0.55–0.70) | "WATCH" | "...show elevated discontinuation risk." |
| PSP = 0.78 (> 0.70) | "STABLE" | (historical analogue omitted for STABLE) |

**State C — Political economy empty state (#987):**

When political economy module is NOT enabled for the loaded scenario: Zone 1D shows
`data-testid="political-risk-empty"` containing "Political risk: not modelled in this
fixture." The four-framework rows remain visible. The Cohort Impact sub-section in Zone 1B
also shows its corresponding empty state.

**State D — Zone 1D proportion and G1 testid retirement (FA brief DD-016):**

At **1280×800**: `data-testid="zone-1d-four-framework"` has computed CSS height of 160px
(±2px measurement tolerance). The following testids are **absent from the DOM**:
`zone-1d-political-feasibility`, `psp-delta`, `psp-layer3-sentence`, `psp-delta-sentence`.
Their absence is confirmable by `page.locator('[data-testid="psp-delta"]').count()` === 0.

### 3.3 Silent failure detection

**Silent failure 1 — Q3/Q4/Q5 shown as zero rather than suppressed:**
If Q3/Q4/Q5 quintile rows appear in Zone 1B with a value of 0% or "no change," the
DemographicModule's zero-delta output is being displayed rather than suppressed. Detection:
in the ZMB ECF step 2 Mode 2 scenario, Zone 1B must contain NO row with label "Middle income
quintile", "Upper-middle income quintile", or "Top income quintile". If any such label appears,
the T5 suppression logic is absent.

**Silent failure 2 — T2 tier label displayed instead of T3:**
If any cohort row in Zone 1B shows "T2" as the tier label for poverty headcount data, the
elasticity-derived source (T3 per Lustig 2017/Ball 2013) has been mislabeled. Detection: any
text matching "T2 ·" adjacent to the cohort rows is a silent failure.

**Silent failure 3 — G1 testids present post-G2:**
If `data-testid="psp-delta"` or `data-testid="psp-layer3-sentence"` or
`data-testid="psp-delta-sentence"` are present in the DOM after G2 implementation, the
replacement mandate was not executed — the G2 political risk sub-section was added alongside
G1 elements rather than replacing them. This creates Zone 1D content height ~228px in a
160px container. Detection: AC-13 and AC-14 catch this.

**Silent failure 4 — Severity badge shows wrong level:**
If PSP=0.38 shows "WARNING" rather than "CRITICAL", or PSP=0.47 shows "CRITICAL" rather than
"WARNING," the threshold boundary logic is wrong. Detection: load ZMB ECF at a step where
PSP=0.38 (CRITICAL boundary) — badge must show "CRITICAL". At PSP=0.41 (just above CRITICAL):
badge must show "WARNING".

---

## 4. Acceptance Criteria

*Each criterion is testable from the running application by the QA Lead without reading
implementation source code. Test file: `frontend/tests/e2e/m16-g2-distributional-surface.spec.ts`.*
*G1 test updates: `frontend/tests/e2e/m16-g1-zone-1a-phase4-composite.spec.ts` (4 testids retired).*

### #986 — Cohort disaggregation (Zone 1B)

**AC-1 (Cohort Impact sub-section present in Zone 1B):**
In the ZMB ECF fixture in Mode 2 at 1280×800, political economy enabled, advanced to step 2:
`data-testid="zone-1b-cohort-impact"` is present in the DOM and visible. A labeled horizontal
rule `data-testid="cohort-section-header"` contains the text "COHORT IMPACT". The element
appears below all MDA aggregate alert rows within Zone 1B.

**AC-2 (Bottom income quintile CRITICAL row format):**
In the ZMB ECF fixture in Mode 2 at 1280×800, advanced to step 2 with Q1 poverty headcount
crossing the MDA floor:
`data-testid="cohort-row-0"` is present and its visible text includes:
- The string "CRITICAL" (severity badge)
- The string "Bottom income quintile" (plain-language label — not "Q1" or "hh_exp_q1")
- The string "Poverty headcount" (plain-language indicator — not "poverty_headcount_rate_pct")
- The string "T3" (tier label)
The string "T2" must NOT appear in `data-testid="cohort-row-0"`.

**AC-3 (Q3/Q4/Q5 suppression):**
In the ZMB ECF fixture in Mode 2 at 1280×800, advanced to step 2:
No element within `data-testid="zone-1b-cohort-impact"` contains the text "Middle income
quintile", "Upper-middle income quintile", or "Top income quintile". The count of visible
`data-testid="cohort-row-{n}"` elements in Zone 1B is ≥ 0 and all visible rows correspond
to Q1 or Q2 ("Bottom income quintile" or "Lower-middle income quintile") only.

**AC-4 (Cohort empty state — Mode 2):**
In the ZMB ECF fixture in Mode 2 at 1280×800, at step 0 (no steps advanced, no threshold
crossings):
`data-testid="cohort-empty-state"` is visible and contains the text
"No cohort threshold crossings projected on current path."
No `data-testid="cohort-row-0"` is present.

**AC-5 (Cohort empty state — Mode 1 header):**
In the ZMB ECF fixture in Mode 1 at 1280×800, at a step where no cohort crosses a threshold:
`data-testid="cohort-section-header"` contains the text "COHORT IMPACT (HISTORICAL)"
(not "COHORT IMPACT").
`data-testid="cohort-empty-state"` contains the text
"No cohort threshold crossings at or before this step."

**AC-6 (Zone 1B visible row count at 1280 — revised per DD-016):**
In the ZMB ECF fixture in Mode 2 at 1280×800, advanced to step 2:
All MDA aggregate alerts are present in `data-testid="zone-1b"`. The top CRITICAL MDA alert
row is visible without vertical scroll on Zone 1B. The top CRITICAL cohort row (`cohort-row-0`)
is visible without scroll. Any second MDA alert row or second cohort row may require scroll —
this is the accepted 1+1 visibility limit at 1280 per DD-016 (FA brief UX Designer sign-off).
*(At 1440×900, run the same test with a 1440 viewport: verify 2 MDA alert rows + 2 cohort rows
visible without scroll.)*

### #987 — Political risk sub-section (Zone 1D)

**AC-7 (Political risk sub-section present in Zone 1D):**
In the ZMB ECF fixture in Mode 2 at 1280×800, political economy enabled, advanced to step 3:
`data-testid="zone-1d-political-risk"` is present in the DOM and visible.
`data-testid="zone-1d-political-risk-header"` contains the text "POLITICAL RISK".
`data-testid="psp-severity-row"` is visible and contains the string "Programme survival".
The element appears below `data-testid="zone-1d-four-framework"` rows within Zone 1D.

**AC-8 (PSP severity badge — CRITICAL threshold at PSP < 0.40):**
In the ZMB ECF fixture in Mode 2 at 1280×800, at a step where PSP = 0.38:
`data-testid="psp-severity-row"` contains the text "CRITICAL" and the text "38%".
At a step where PSP = 0.47 (0.40–0.55): `data-testid="psp-severity-row"` contains
"WARNING" and "47%". At PSP = 0.62 (0.55–0.70): "WATCH" and "62%". At PSP = 0.78 (> 0.70):
"STABLE" and "78%". *(Requires scenario fixture to expose specific PSP values at named steps.)*

*Note: AC-8 is the closure condition for #1163 — the severity badge makes the absolute PSP
level self-interpreting. #1163 is confirmed closed when AC-8 passes.*

**AC-9 (Historical analogue sentence — CRITICAL and WARNING values):**
In the ZMB ECF fixture in Mode 2 at 1280×800, at a step where PSP < 0.40 (CRITICAL):
`data-testid="psp-historical-analogue"` contains the text "within 3 steps".
At a step where PSP is in the WARNING range (0.40–0.55):
`data-testid="psp-historical-analogue"` contains the text "within 6 steps".
For WATCH or STABLE: `data-testid="psp-historical-analogue"` contains "elevated discontinuation
risk" (placeholder) or is absent from the DOM.

**AC-10 (Legitimacy index row):**
In the ZMB ECF fixture in Mode 2 at 1280×800, political economy enabled, at step 3:
`data-testid="legitimacy-index-row"` is visible and its text includes "Legitimacy index" and
a numeric value followed by "declining", "stable", or "improving" based on the step-over-step
change in legitimacy index.
`data-testid="legitimacy-floor-proximity"` is visible and contains one of: "above fragility
threshold", "AT fragility threshold", or "below fragility threshold".

**AC-11 (Political economy empty state):**
In the ZMB ECF fixture in Mode 2 at 1280×800, political economy module DISABLED:
`data-testid="political-risk-empty"` is visible and contains the text
"Political risk: not modelled in this fixture."
`data-testid="psp-severity-row"` is absent from the DOM.
`data-testid="zone-1d-four-framework"` (the four framework rows) remains visible — the four
framework rows are not removed when political economy is disabled.

### Layout and G1 testid retirement

**AC-12 (Zone 1D flex proportion at 1280):**
At 1280×800, `data-testid="zone-1d-four-framework"` (or the Zone 1D container) has computed
CSS height of 160px (±4px measurement tolerance). This confirms the `flex: 0 0 50%` allocation
against `chartHeight=320px`.

**AC-13 (Zone 1C proportion at 1280):**
At 1280×800, `data-testid="zone-1c-pmm"` (or the Zone 1C container) has computed CSS height
of 48px (±4px measurement tolerance). This confirms the `flex: 0 0 15%` allocation.

**AC-14 (G1 testid retirement — all four retired testids absent):**
At 1280×800, ZMB ECF fixture in Mode 2, political economy enabled, step ≥ 1:
`page.locator('[data-testid="zone-1d-political-feasibility"]').count()` === 0
`page.locator('[data-testid="psp-delta"]').count()` === 0
`page.locator('[data-testid="psp-layer3-sentence"]').count()` === 0
`page.locator('[data-testid="psp-delta-sentence"]').count()` === 0
*(All four G1 Zone 1D testids are absent — confirming the replacement mandate is executed.)*

---

## 4b. Visual Spec (before/after)

### AC-2 — Zone 1B cohort row format

**AC-2 (before):**
```
Viewport: 1280×800 | Zone: 1B | data-testid="zone-1b"

ZMB ECF Mode 2 at step 2:
[MDA ALERTS section]
CRITICAL  Reserve coverage
          2.3 months · 6 consecutive steps · T2 · CBJ 2023-Q4

[No cohort impact sub-section present]
[No "COHORT IMPACT" divider]
[No cohort threshold crossings visible at any viewport]
```

**AC-2 (after):**
```
Viewport: 1280×800 | Zone: 1B | data-testid="zone-1b-cohort-impact"

ZMB ECF Mode 2 at step 2:
[MDA ALERTS section]
CRITICAL  Reserve coverage
          2.3 months · 6 consecutive steps · T2 · CBJ 2023-Q4
——————————— COHORT IMPACT ———————
CRITICAL  Bottom income quintile — Poverty headcount
          Threshold crossed at step 2 · was 3.8% above floor · T3 · WB PovcalNet 2023

[Scroll to see additional rows: 2nd MDA alert, 2nd cohort row]

Notes:
- "Bottom income quintile" (not "Q1") — kryptonite constraint
- "T3" (not "T2") — CM condition
- Q3/Q4/Q5 are absent entirely
```

### AC-7 / AC-8 — Zone 1D political risk sub-section (before/after)

**AC-7/AC-8 (before — G1 state, step 3, PSP=0.38):**
```
Viewport: 1280×800 | Zone: 1D | data-testid="zone-1d-four-framework"

Zone 1D at step 3, PSP=0.38, political economy enabled:
  Financial:         0.72
  Human Development: 0.61
  Ecological:        0.84
  Governance:        0.55

  Political Feasibility   38% ↓4pp    [data-testid="zone-1d-political-feasibility"]
                              ^^^^ psp-delta (red-coloured)

  programme survival dropped 4 percentage points this step.
                                       [data-testid="psp-layer3-sentence"]

  [psp-delta-sentence also present — verbose M14 sentence]

Problems:
- "Political Feasibility 38%" — not self-interpreting (38% of what? is 38% bad?)
- "↓4pp" — the delta is layer 3; the absolute level (38%) is not  ← #1163
- "PSP" acronym not decoded anywhere (though this element avoids it)
- Total Zone 1D content ≈ 148px in 96px container — 52px overflowing (clipped)
```

**AC-7/AC-8 (after — G2 state, step 3, PSP=0.38):**
```
Viewport: 1280×800 | Zone: 1D | data-testid="zone-1d-political-risk"

Zone 1D at step 3, PSP=0.38, political economy enabled:
  Financial:         0.72
  Human Development: 0.61
  Ecological:        0.84
  Governance:        0.55

  ——————— POLITICAL RISK ——————————————
  Programme survival: CRITICAL (38%) — DECLINING
                      ^^^^^^^^ psp-severity-badge — makes 38% self-interpreting (#1163)
                               [data-testid="psp-severity-row"]

  At this level, historical ECF programmes show abandonment within 3 steps.
                      [data-testid="psp-historical-analogue"]

  Legitimacy index: 0.42 — declining (floor: 0.35)
                      [data-testid="legitimacy-index-row"]
    0.07 above fragility threshold
                      [data-testid="legitimacy-floor-proximity"]

  Elite capture divergence: widening — fiscal benefits...
                      [data-testid="elite-capture-row"] (truncated with ellipsis)

G1 testids absent: zone-1d-political-feasibility, psp-delta, psp-layer3-sentence, psp-delta-sentence
Zone 1D total height: ~156px in 160px container — no overflow
```

### AC-14 — G1 testid retirement confirmation

**AC-14 (before — G1 state):**
```
Viewport: 1280×800 | Zone: 1D | political economy enabled, step 1

DOM contains:
  [data-testid="zone-1d-political-feasibility"] — present, visible
  [data-testid="psp-delta"] — present if step ≥ 1
  [data-testid="psp-layer3-sentence"] — present, visible
  [data-testid="psp-delta-sentence"] — present, visible
```

**AC-14 (after — G2 state):**
```
Viewport: 1280×800 | Zone: 1D | political economy enabled, step 1

DOM contains:
  [data-testid="zone-1d-political-risk"] — present (new)
  [data-testid="psp-severity-row"] — present (new)
  [data-testid="psp-historical-analogue"] — present (new)

DOM does NOT contain:
  [data-testid="zone-1d-political-feasibility"] — ABSENT ← count() === 0
  [data-testid="psp-delta"] — ABSENT ← count() === 0
  [data-testid="psp-layer3-sentence"] — ABSENT ← count() === 0
  [data-testid="psp-delta-sentence"] — ABSENT ← count() === 0
```

---

## 5. Kryptonite Constraint Check

*Authority: `docs/process/agent-execution-lifecycle.md §Kryptonite Design Constraint (FD-3)`.*

**Does this implementation's primary observable state require specialist mediation for Persona 2
(#986) or Persona 3 (#987) to act on it in the Reactive entry state (90-second ceiling)?**

`[x]` **No** — both observable states are designed to be self-interpreting.

Rationale:

**#986 (Persona 2):** The cohort row text "Bottom income quintile — Poverty headcount — Threshold
crossed at step 2" is fully plain-language. No field keys ("hh_exp_q1", "poverty_headcount_rate_pct"),
no acronyms, no threshold values requiring domain knowledge. "CRITICAL" is the severity label that
contextualizes the threshold crossing without requiring knowledge of the floor value. Persona 2 can
form the negotiating argument ("the bottom income quintile crosses the poverty headcount threshold
at step 2") directly from the Zone 1B display. Kryptonite constraint satisfied.

**#987 (Persona 3):** The political risk sub-section eliminates every specialist-mediation surface
identified in the design doc's §Jargon eliminated list: "PSP" → "Programme survival"; "0.38" →
"CRITICAL (38%)"; "legitimacy_index" → "Legitimacy index: 0.42 — declining"; "elite_capture_divergence"
→ "Elite capture divergence: widening — fiscal benefits concentrating". The historical analogue
sentence ("within 3 steps") converts the PSP severity into a time-bounded institutional reference
that a governance professional understands. Kryptonite constraint satisfied.

**Residual gap (documented, not hidden):**
- The historical analogue sentence precision (CRITICAL = "within 3 steps") is calibrated against
  Zambia 2022 and Ghana 2023 (CM sign-off). The precision degrades for entities whose political
  economy dynamics differ materially from the calibration set. This is a known model limitation —
  documented in `docs/DATA_STANDARDS.md §Model Limitations`, not hidden from the user.
- The legitimacy floor value ("floor: 0.35") is entity-calibrated and shown in context but is
  not self-explained. A user who asks "why is 0.35 the floor?" needs Zone 2B content. At L0, the
  "X above fragility threshold" sub-line provides enough actionability without explaining the
  methodology.

---

## 6. Out of Scope

**#986 age-band cohort disaggregation:** School enrollment (under-18) and child malnutrition
(under-5) are M17 scope. DemographicModule has no elasticity rows for these indicators.

**Q3/Q4/Q5 display:** Zero-delta quintiles are suppressed as T5. Cohort-specific floor
calibration for Q3–Q5 is M17 scope. The current display correctly shows "no data" by showing
nothing (rather than zero) for these quintiles.

**Zone 1D interactive expand mode:** ADR-015 L1/L2 cross-examination is a separate deliverable.
G2 delivers L0 only (zero-interaction display of all political risk elements).

**Mode 3 PSP direction reversal marker:** Mode 3 adds "(reversal from previous input)" to the
PSP severity row. G2 scope covers Mode 1 and Mode 2 only. Mode 3 extension is G2b if capacity
allows.

**Backend API changes:** G2 is frontend-only. All data (cohort thresholds, political risk
indicators) is derived from existing trajectory response fields in the frontend state.

**Zone 1A changes:** No changes to Zone 1A in G2. The G1 composite encoding and divergence fill
are untouched.

**#1162 (entity attribution anchor):** Pre-demo fix; separate issue filed by Customer Agent.
Not a G2 deliverable.

**G1 test content:** The G2 PR updates G1 test selectors (retired testids) but does not change
G1 test AC coverage or assertions. AC-7 through AC-11 in the G1 spec are updated to use
replacement testids only — no AC is removed and no coverage is lost.

---

## 7. Test Authorship Obligation

**QA Lead:** QA Lead Agent
**Test authorship deadline:** Before any G2 implementation PR is opened against `release/m16`
**Primary test file:** `frontend/tests/e2e/m16-g2-distributional-surface.spec.ts`
**G1 test update file:** `frontend/tests/e2e/m16-g1-zone-1a-phase4-composite.spec.ts`
**Acceptance criteria covered:** AC-1 through AC-14 (G2 spec file); G1 AC-7/AC-8/AC-9/AC-10 updated

**G1 test update scope (binding):**

| G1 AC | Testid change required |
|---|---|
| AC-7 (psp-delta present at step ≥1) | Update selector: `psp-delta` → `psp-severity-row`; text assertion: check for direction text in severity row |
| AC-8 (psp-delta absent at step 0) | Update selector: assert `psp-severity-row` IS present at step 0 (shows PSP % without direction), but direction indicator is absent from within it |
| AC-9 (psp-delta-sentence at L0) | Update selector: `psp-delta-sentence` → `psp-historical-analogue`; text assertion: check for historical analogue text content |
| AC-10 (psp-delta colour encoding) | Update selector: move colour assertion from `psp-delta` to `psp-severity-badge`; severity badge carries the CRITICAL (red) / STABLE (green) visual encoding in G2 |
| AC-11 (no new endpoint) | Unchanged |

**QA Lead acknowledgment:**
`[ ]` QA Lead: Tests for AC-1 through AC-14 authored in G2 spec file, and G1 spec file
updated for 4 retired testids. Both files filed before any G2 implementation PR opens. [Date]

---

*Intent document authority: `docs/process/intent-template.md` (version 2026-06-17).
Sprint entry: `docs/process/sprint-plans/m16-g2-sprint-entry.md` (EL Approval pending).
Design authorities: `docs/ux/design-thinking/cohort-disaggregation-design.md`;
`docs/ux/design-thinking/political-risk-summary-design.md`.
FA layout brief: `docs/frontend/fa-brief-m16-g2-zone-1d-layout.md` (DD-016).
Implementing agent: Frontend Architect Agent. Layer 3 assessment: Customer Agent required
(Persona 2 and Persona 3 served — both require Layer 3 gate before BPO verdict).*
