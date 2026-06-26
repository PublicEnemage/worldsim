---
name: M17-G3-zone-1b-proportional-allocation
type: design-and-implementation-intent
issue: "#1252"
status: >
  Phase 2 ADR accepted — ADR-018 (ARCH-012, Path B) accepted 2026-06-25. [ADR-VALUE]
  resolved at 80px (Sub-zone A floor, all breakpoints). Phase 1 BPO accepted 2026-06-25.
  Phase 3 implementation gated on: (1) QA test file authored; (2) EL sprint entry approval;
  (3) #1250 merged to release/m17. Intent document satisfies sprint entry §2.3 content
  requirements in full — pixel values and implementation contract complete per ADR-018.
authored-by: UX Designer Agent (Phase 1 design decisions) + PM Agent (document framing)
authored-date: 2026-06-25
adr-reference: >
  ADR-018 — Zone 1B Proportional Allocation (ARCH-012, Path B). New ADR required — overflow
  contract and multi-occupant allocation are new decisions not derivable from ADR-017 (Zone 1A)
  or ADR-014 (single-occupant; Valid Until clause fires). Accepted 2026-06-25.
release-branch: release/m17
sprint-entry: docs/process/sprint-plans/m17-g3-sprint-entry.md (draft — awaiting EL approval)
---

# Design and Implementation Intent: M17-G3 — Zone 1B Proportional Allocation (#1252)

> **Dual-function document.** This document serves two purposes:
>
> 1. **Phase 1 UX brief** — §3 answers the four allocation questions that the sprint entry
>    requires before Phase 2 (ADR authorship) begins. The Phase 1 panel review (UX Designer,
>    Design Thinking, Customer Agent) and BPO acceptance are conducted against §3. Panel review
>    format: verdicts recorded as comments on GitHub issue #1252; panel summary @PublicEnemage.
>
> 2. **Phase 3 implementation intent** — §4 (observable states) and §5 (acceptance criteria)
>    are the implementation contract that the QA Lead authors tests from and the implementing
>    agent satisfies. Pixel values in §4 marked [ADR-VALUE] are placeholders; the Phase 2
>    Architect fills them in the accepted ADR before any implementation PR opens.
>
> **Filing note:** Authoring this document does NOT satisfy the sprint entry's intent document
> gate (§2.3). The gate is satisfied when: (a) Phase 1 panel review produces all-PASS verdicts;
> (b) BPO accepts Phase 1; (c) Phase 2 ADR is accepted; (d) [ADR-VALUE] placeholders in §4
> are replaced with ADR-specified values. EL approval of the sprint entry follows.
>
> **Authority:** `docs/process/sprint-plans/m17-g3-sprint-entry.md §2.3 and §2.5`.

---

## 1. Source

**Issue:** #1252 — arch(zone-1b): Zone 1B proportional allocation — MDA alert vs cohort sections

**Background:**
Zone 1B currently has two occupants — the MDA alert panel and the CohortImpactSection — whose
space claims are negotiated at render time via CSS flex (`flex: "1 1 80px"` on the MDA wrapper,
`flex: "0 0 auto"` on the cohort section). The `overflow: "auto"` on the Zone 1B container
allows the zone to scroll as a unit when combined height exceeds Zone 1B's allocated height.
The `minHeight: 80` on the MDA panel wrapper is a temporary guarantee (PR #1235, cited in
`docs/process/sprint-plans/m17-g3-sprint-entry.md §2.2` as temporary constraint not treated
as accepted architecture).

The M16 retrospective identified that under high cohort load (8+ crossing entries), the MDA
panel can be collapsed or displaced. Root cause: the flex model negotiates height in real time
without a formal proportional allocation rule, and the `overflow: auto` on the Zone 1B
container means the whole zone scrolls rather than each occupant staying in its allocated space.

G3 replaces this ad-hoc flex negotiation with an ADR-grounded proportional allocation model.
The temporary `minHeight: 80px` guarantee is superseded by the permanent ADR contract.

**ADR reference:** TBD — Path A (ADR-017 amendment) or Path B (new ADR, ARCH-012).
See §Phase 2 ADR Gate for the two-path determination criteria.

**Authored by:** UX Designer Agent (Phase 1 design decisions); PM Agent (framing)
**Date:** 2026-06-25

---

## 2. Persona Trace Elements Targeted

> *G3 serves two personas with distinct but compatible Zone 1B reading requirements.*

### Primary persona — Aicha Mbaye (Persona 5 — Finance Minister / Senior Ministry Official)

**P-1 — Persona served:**
Persona 5 — Finance Ministry Senior Official (Finance Minister or Deputy). Aicha reads Zone 1B
for the breach headline: severity label + indicator name + distance below floor. She does not
operate the tool at the table — she reads the primary viewport display prepared by her analyst.
The MDA panel headline is her primary anchor in Zone 1B.

**P-2 — Entry state:**
Reactive — Journey B Step 3. Zone 1B is visible in the primary viewport without interaction.
Aicha must read the MDA headline within the 90-second Reactive ceiling without requiring Zone 1B
to scroll or any drawer to open.

**P-3 — Journey reference:**
Journey B Step 3 [Near-Term-Gap GA-B3]: Reactive defence of distributional output.
Zone 1B cohort crossings are the evidence that the bottom quintile is affected; the MDA panel
headline is the breach severity summary Aicha reads at a glance.

**P-4 — Time/interaction ceiling:**
90 seconds (Reactive entry state). The MDA panel headline (`data-testid="zone-1b-top-detail"`)
must be visible without scrolling Zone 1B (`data-testid="zone-1b"`), regardless of cohort load.

**P-6 — Negotiating leverage delivered:**
Aicha can state at the table: "Q1 informal sector poverty headcount has crossed CRITICAL — 3.5%
below the humanitarian safety floor — and has been there for two steps." This sentence is read
directly from the MDA panel top-detail area, without requiring the analyst to scroll or narrate.

**P-7 — North star capability delivered:**
After G3 implementation, a Senegal finance ministry analyst can show that Zone 1B's MDA alert
panel headline is visible at the primary viewport without scrolling — at any cohort crossing
load — so Aicha can read the breach severity and direction in the Reactive entry state without
analyst mediation.

---

### Secondary persona — Lucas Ferreira (Persona 1 — Programme Analyst / Ministry Analyst)

**P-1:** Lucas reads both the MDA panel (breach detail, trajectory sentence) and the
CohortImpactSection (specific cohort crossing rows, indicators, floor distances) to construct
the full human cost argument.

**P-4 — Time/interaction ceiling:**
No fixed ceiling for Preparatory entry state. Lucas reads Zone 1B in depth. His constraint:
the CohortImpactSection must be readable in its allocated space — not truncated below
the ADR-specified max-display count, not requiring Zone 1B outer scroll to reveal it.

**P-7:** After G3 implementation, Lucas can read the CohortImpactSection crossing entries
within Zone 1B's allocated cohort sub-zone, with internal scroll available for entries beyond
the visible allotment, without the Zone 1B container scrolling as a unit and without the
MDA panel being absent from view.

---

## 3. Phase 1 UX Brief — Design Decisions

> *This section IS the Phase 1 UX brief. Panel reviewers (UX Designer, Design Thinking,
> Customer Agent) assess this section against the five governing UX premises (CLAUDE.md
> §UX Architectural Commitments) and the reading-order constraint (sprint entry §2.5).
> BPO accepts or rejects based on panel verdicts. Phase 2 (ADR authorship) may not begin
> until BPO acceptance of this section is on record.*

### 3.1 — Q1: Proportional model

**Decision: Explicit static allocation with MDA panel guaranteed minimum, CohortImpactSection
taking remaining height with internal scroll.**

Zone 1B's inner layout changes from flex-height-negotiation to an **explicit two-sub-zone
allocation**:

- **Sub-zone A (MDA panel):** `flex: 1 1 80px, minHeight: 80px, overflow: hidden` — ADR-018
  specifies 80px as the permanent floor (unchanged from current). Sub-zone A uses growable
  flex (not fixed `flex: 0 0 80px`) so it expands to full Zone 1B height in the empty-state
  (Case A) without a JS toggle. The `minHeight: 80px` temporary guarantee (PR #1235) is
  superseded by this ADR-grounded permanent contract. See ADR-018 §Decision for the refinement
  from the Phase 1 brief's `flex: 0 0 [ADR-VALUE]px` description to the ADR-specified
  `flex: 1 1 80px` — observable states are identical; implementation mechanism is simpler.

- **Sub-zone B (CohortImpactSection):** `flex: 1 1 0` — takes all remaining Zone 1B height
  after Sub-zone A. `overflow-y: auto` — internal scroll only. Cohort crossing entries that
  exceed Sub-zone B's height scroll within Sub-zone B; the Zone 1B outer container does not
  scroll.

**Zone 1B outer container change:** `overflow: "auto"` → `overflow: "hidden"`. This prevents
the zone from scrolling as a unit, forcing each occupant to stay within its allocated space.

**Rationale:** The cognitive task hierarchy (MDA panel = primary instrument; CohortImpactSection
= supplementary evidence) requires the primary instrument to be visible unconditionally. A
fixed-height allocation for the MDA panel — independent of cohort load — is the only model
that satisfies Aicha's Reactive ceiling without requiring interaction. Static allocation is
chosen over dynamic allocation because:
(a) The MDA panel content is relatively stable in height (severity chip + top detail + trajectory
    sentence = approximately the same height across scenarios); dynamic allocation would provide
    no benefit over static.
(b) Static allocation is deterministic — the same proportional split applies at every step,
    making the layout testable by bounding box assertion without scenario-specific knowledge.

**What is left to Phase 2 (ADR determination):**
The specific pixel value for Sub-zone A at each breakpoint (1024×768, 1280×800, 1440×900)
is an ADR output. The Architect measures the MDA panel's natural content height at each
breakpoint with the Senegal T3 scenario, selects a minimum that covers the top-detail area
(`data-testid="zone-1b-top-detail"`) plus the trajectory sentence
(`data-testid="zone-1b-trajectory-sentence"`), and declares these values in the ADR. Until
the ADR is accepted, [ADR-VALUE] in this document is a placeholder. **ADR-018 resolved this at 80px for all breakpoints.** The 80px floor covers zone-1b-top-detail; the trajectory sentence may be partially visible at low Zone 1B heights (1280: ~60px Sub-zone B leaves limited MDA visible height).

**Governing premise satisfied:** UX Architectural Commitment Premise 2 — "Instruments are
always visible; no primary instrument lives behind a click or scroll." The MDA alert panel is
a primary instrument. Fixed-height allocation ensures it is visible unconditionally.

---

### 3.2 — Q2: Overflow handling

**Decision: CohortImpactSection scrolls internally. Zone 1B outer container does not scroll.
MDA panel sub-zone is never compressed under any cohort load.**

When CohortImpactSection content (cohort crossing entries) exceeds Sub-zone B's height:
- Entries scroll within Sub-zone B (`overflow-y: auto` on the CohortImpactSection wrapper)
- Zone 1B outer container does not scroll (enforced by `overflow: hidden` on `data-testid="zone-1b"`)
- Sub-zone A (MDA panel) remains at its fixed ADR-specified height — not displaced by cohort overflow

**Regression condition (non-negotiable from M16 retrospective):**
A scenario producing 8 or more cohort crossing entries must NOT cause Sub-zone A to collapse
to zero or below its ADR-specified minimum height. This condition is verified by the
pre-implementation red assertion in AC-A2.

**No truncation with count label:** The overflow model uses internal scroll, not truncation.
A "and N more" count label is not required at this stage. This is consistent with Lucas's use
case — he needs to scroll through all entries, not be told a count of hidden ones. If a future
ADR determines that scroll is inadequate and a max-display constraint is needed, a count label
may be introduced in a subsequent G-group. G3 does not implement truncation.

---

### 3.3 — Q3: Empty-state behavior

**Decision: Single-occupant states use full Zone 1B height for the active occupant.**

Three cases:

**Case A — MDA breaches only (no cohort crossings):**
Sub-zone B (CohortImpactSection) is hidden — `display: none` or `height: 0`. Sub-zone A
(MDA panel) expands to full Zone 1B height using `flex: 1 1 0` in the single-occupant
layout path (or by the CohortImpactSection being removed from the DOM).

Verification: `data-testid="cohort-empty-state"` is visible (the existing empty-state
element), OR `data-testid="zone-1b-cohort-impact"` has zero bounding box height.
`data-testid="zone-1b-top-detail"` is visible at full height within Zone 1B.

**Case B — Cohort crossings present AND MDA breaches present (normal dual-occupant state):**
Both Sub-zone A and Sub-zone B are populated. Proportional split per Q1. This is the
primary case addressed by G3.

**Case C — No MDA breaches, no cohort crossings (no-data state):**
Zone 1B shows its existing no-data / loading state. No layout change from current behavior.
G3 does not modify this case.

**Note on Case A implementation:** The CohortImpactSection's existing store-connected behavior
already handles the empty case (renders `data-testid="cohort-empty-state"` when no cohort
crossings). G3 must ensure that in Case A, Sub-zone A takes the full Zone 1B height rather
than a fixed ADR-value height — otherwise Zone 1B shows large empty space below the MDA panel.
ADR-018 resolves this without a JS toggle: Sub-zone A uses `flex: 1 1 80px, minHeight: 80px`
(grows when Sub-zone B is absent) and Sub-zone B wrapper uses `maxHeight: calc(100% - 80px)`.
When Sub-zone B has minimal content (empty-state), Sub-zone A grows to fill Zone 1B. The
observable expansion is confirmed by comparing the MDA panel bounding box height in Case A vs Case B.

---

### 3.4 — Q4: Viewport contract

**Decision: MDA panel top-detail area must be visible without Zone 1B scroll at all supported
breakpoints, including 768px tablet. Minimum heights are ADR-specified per breakpoint.**

Required viewport observable states (pixel values resolved at Phase 2):

| Breakpoint | Zone 1B total height | Sub-zone A minimum | Sub-zone B available | Observable condition |
|---|---|---|---|---|
| 1024×768 | ~185px (est.) | 80px (ADR-018) | ~105px (~4 rows) | `zone-1b-top-detail` visible without Zone 1B scroll |
| 1280×800 | ~138px (est.) | 80px (ADR-018) | ~58px (~2 rows) | `zone-1b-top-detail` visible; `zone-1b-cohort-impact` has non-zero height |
| 1440×900 | ~182px (est.) | 80px (ADR-018) | ~102px (~3–4 rows) | Both sub-zones visible at their minimum heights |
| 768px (tablet) | ~185px (est.) | 80px (ADR-018) | ~105px (~4 rows) | `zone-1b-top-detail` visible; no Zone 1B outer scroll required |

> **Note on estimated heights:** Zone 1B heights are computed from LAYOUT × ZONE_PROPORTIONS +
> estimated cohortPanel height (~75px). The implementing engineer must confirm at runtime using
> browser dev tools before QA numeric thresholds are finalized. Row height reference: ~26px
> per cohort crossing row (ADR-014 measurement). QA test assertions use ≥ 80px for Sub-zone A
> (not the estimated Zone 1B total).

**768px (tablet) constraint:** DEMO6-026/043 (#1250) revealed tablet legibility failures at
768px. G3 must confirm that the proportional allocation model does not worsen the tablet
legibility problem. If the ADR-specified minimum for Sub-zone A at 768px results in
Sub-zone B having less than a legible minimum height (defined by #1250's implementation),
the Architect flags this conflict in the Phase 2 assessment and routes to the BPO for a
scope decision. G3 does NOT own the font/sizing legibility fix — that is #1250 scope. G3
owns the proportional allocation model that ensures both sections have non-zero height at 768px.

**Note on Zone 1B height measurement:** Zone 1B height at each breakpoint is determined by
the ZONE_PROPORTIONS percentages (35% at 1280, 50% at 1024, 40% at 1440) of the co-primary
column height, which depends on the page layout. The Phase 2 Architect measures actual Zone 1B
heights at each breakpoint by running the application and using browser dev tools. Measurements
are required before ADR-VALUE placeholders can be resolved.

---

### 3.5 — Reading-order constraint confirmation (from sprint entry §2.5)

> Non-negotiable from `docs/process/sprint-plans/m17-g3-sprint-entry.md §2.5`:
> "A proportional model that resolves Zone 1B allocation but fails the reading-order constraint
> is a REJECT at panel review."

**UX Designer confirmation:** The Q1 decision (Sub-zone A fixed height, Sub-zone B remaining
with internal scroll, Zone 1B no outer scroll) satisfies the reading-order constraint:

- **Aicha's use (MDA headline first):** Sub-zone A is the top sub-zone. It is always at its
  ADR-specified height, always visible without Zone 1B scroll. MDA panel headline is at the
  primary visual anchor position.
- **Lucas's use (CohortImpactSection fully readable):** Sub-zone B occupies all remaining
  Zone 1B height with internal scroll — Lucas can scroll Sub-zone B to read all entries without
  scrolling Zone 1B or opening a drawer. The CohortImpactSection is co-primary for Lucas;
  it is supplementary for Aicha. The allocation model serves both simultaneously.

---

## 4. Observable Application State

> *All states are verifiable by an external observer using only the running application.
> States referencing [ADR-VALUE] are verifiable once the ADR-specified pixel values are
> substituted. QA Lead substitutes these values when authoring tests from this document.*

### 4.1 Primary observable state

Zone 1B (`data-testid="zone-1b"`), Senegal T3 conditionality scenario at step 2 (MDA alerts
active; Q1 cohort crossings present):

1. `data-testid="zone-1b-top-detail"` has positive bounding box height and is visible (not
   hidden by overflow) **without any scroll event on `data-testid="zone-1b"`**.

2. `data-testid="zone-1b-cohort-impact"` has positive bounding box height and at least one
   `data-testid="cohort-row-0"` is visible within it **without any scroll event on `data-testid="zone-1b"`**.

3. `data-testid="zone-1b"` does NOT have a non-zero `scrollTop` value at the initial
   viewport state — the layout does not require Zone 1B to scroll to show its primary content.

These three states together confirm the proportional allocation model is in place: both
occupants are visible in their allocated sub-zones without Zone 1B scrolling.

---

### 4.2 Secondary observable states

**State A — Overflow regression guard:**
With a scenario producing 8 or more cohort crossing entries (confirmed by
`data-testid^="cohort-row-"` count ≥ 8), `data-testid="zone-1b-top-detail"` has positive
bounding box height within `data-testid="zone-1b"`. The MDA panel sub-zone (`data-testid=
"zone-1b-mda-panel-wrapper"` — new testid added by G3; see §6 note) has bounding box height
≥ 80px (ADR-018). This confirms the M16 regression failure mode does not recur.

**State B — Empty-state (MDA only):**
At a step where Zone 1B has MDA alerts but no cohort crossings (e.g., step 1 of the Senegal
T3 scenario before the first crossing event), `data-testid="zone-1b-top-detail"` is visible
and `data-testid="zone-1b-cohort-impact"` either has zero bounding box height OR shows
`data-testid="cohort-empty-state"`. Zone 1B does not show a large empty space below the
MDA panel (confirming the single-occupant expansion behavior from Q3 Case A).

**State C — Viewport contract at 768px:**
At 768px viewport width (Playwright `page.setViewportSize({width: 768, height: 1024})`),
with Senegal T3 at a step with active MDA alerts and cohort crossings,
`data-testid="zone-1b-top-detail"` has positive bounding box height and is visible without
requiring any scroll on `data-testid="zone-1b"`. Sub-zone B (`data-testid="zone-1b-cohort-impact"`)
has positive bounding box height.

---

### 4.3 Silent failure detection

**Silent failure — `minHeight: 80px` retained as sole mechanism:**
If G3 implementation merges without replacing the `flex: "1 1 80px" / minHeight: 80` pattern
with the ADR-grounded allocation, the MDA panel may still show correctly at current test
scenarios (because the scenario's cohort section is short enough not to trigger displacement)
while remaining vulnerable to the M16 failure mode at higher cohort load.

**Detection:** AC-A2 is the primary detection mechanism — it requires an 8+ cohort row
scenario that triggered the failure mode. The QA Lead must NOT use a soft scenario fixture;
the test must confirm the regression condition with at least 8 cohort crossing rows active.
A passing AC-A2 with fewer than 8 active rows does not confirm the regression guard.

**Silent failure — Zone 1B `overflow: "auto"` retained:**
If the Zone 1B outer container's `overflow` is not changed from `auto` to `hidden`, the
zone can still scroll as a unit. AC-A1 detects this: if Zone 1B can scroll, the initial
state may still show both sections via outer scroll rather than via the sub-zone allocation
model. Detection: assert that `data-testid="zone-1b"` has `overflow-y` computed style of
`hidden` (or assert that a synthetic scroll event on `data-testid="zone-1b"` does not change
which elements are in the viewport).

---

## 5. Acceptance Criteria

> *Criteria match the QA test requirements from `docs/process/sprint-plans/m17-g3-sprint-entry.md §2.4`.
> The QA Lead authors `frontend/tests/e2e/m17-g3-zone-1b-allocation.spec.ts` from these criteria
> before the implementation PR opens.*
>
> *ADR-018 accepted 2026-06-25. Sub-zone A floor = 80px at all breakpoints. Zone 1B heights are
> estimated (see §3.4 table); implementing engineer must confirm at runtime before QA thresholds
> are finalized. QA Lead may author test structure now; update numeric thresholds after runtime
> measurement confirms Zone 1B heights at each breakpoint.*

**AC-A1 (proportional model — dual-occupant state):**
In the Senegal T3 conditionality scenario at step 2 (or the Greece backtesting fixture at a
step where both MDA alerts and cohort crossings are active), when Zone 1B is rendered at
1280×800:
- `data-testid="zone-1b-mda-panel-wrapper"` (the MDA sub-zone wrapper) has bounding box height
  ≥ 80px (ADR-018)
- `data-testid="zone-1b-cohort-impact"` has bounding box height > 0
- `data-testid="zone-1b"` scrollTop is 0 (Zone 1B outer container is not scrolled)

**AC-A2 (overflow regression guard — red-before-green, M16 retrospective):**
With a scenario fixture that populates Zone 1B with 8 or more cohort crossing entries (count:
`data-testid` matching `cohort-row-{n}` for n = 0 through 7 or more), at 1280×800:
- `data-testid="zone-1b-mda-panel-wrapper"` bounding box height ≥ 80px (ADR-018) — confirming the MDA panel is not displaced

**This assertion must be red before G3 implementation is applied** — the QA Lead must confirm
that the pre-implementation fixture at 8+ cohort rows causes the assertion to fail (either
because `zone-1b-mda-panel-wrapper` doesn't exist yet, or because its height is below the ADR
minimum). The post-implementation green confirms the regression is resolved. A test that passes
before AND after implementation does not confirm the fix.

**The QA test file must include a comment citing the M16 retrospective as the regression
evidence source** — reference `docs/process/sprint-plans/m17-g3-sprint-entry.md §2.2
(Standing constraint)` and the PR #1235 note.

**`test.fail()` annotation — EX-002 (2026-06-25):**
AC-A2 is annotated with `test.fail()` in `m17-g3-zone-1b-allocation.spec.ts` during the
pre-G3-implementation window. CI treats the expected failure as a passing state. When G3 Phase 3
adds `data-testid="zone-1b-mda-panel-wrapper"`, AC-A2 will pass — triggering a CI "unexpected
pass" that signals the implementing engineer to remove `test.fail()`. See EX-002
(`docs/compliance/exceptions.md`) and NM-065 (`docs/process/near-miss-registry.md`).

`test.fail()` is not a soft-skip. The test still runs and still must fail before implementation.
This does not violate the NM-056 guard against soft-skip patterns (`test.skip()`, `test.fixme()`,
conditional early-returns suppress execution; `test.fail()` does not).

**Phase 3 reversal steps (required in the G3 implementation PR):**
1. Add `data-testid="zone-1b-mda-panel-wrapper"` to `InstrumentCluster.tsx` (line ~143)
2. Run playwright locally — AC-A2 should pass (testid present, height ≥ 80px)
3. Playwright will report "unexpected pass" because `test.fail()` is still present
4. Remove `test.fail()` and its four-line comment block from AC-A2 in the test file
5. Re-run playwright — AC-A2 passes cleanly; update EX-002 Status to Resolved

**No soft-skip patterns** (NM-056 guard): `test.skip()`, `test.fixme()`, and conditional
early-returns remain prohibited for AC-A2. Only `test.fail()` + EX-NNN is an approved
alternative (NM-065).

**AC-A3 (viewport contract at 768px):**
With the Senegal T3 scenario at a step where both MDA alerts and cohort crossings are active,
at `page.setViewportSize({width: 768, height: 1024})`:
- `data-testid="zone-1b-top-detail"` is visible (positive bounding box height, within viewport)
- `data-testid="zone-1b"` scrollTop is 0
- `data-testid="zone-1b-cohort-impact"` has positive bounding box height
- `data-testid="zone-1b-mda-panel-wrapper"` bounding box height ≥ 80px (ADR-018)

**AC-A4 (empty-state — MDA only):**
At a step where Zone 1B has MDA alerts but no cohort crossings (assert: `data-testid=
"cohort-row-0"` is absent from the DOM OR `data-testid="cohort-empty-state"` is present):
- `data-testid="zone-1b-top-detail"` is visible (positive bounding box height)
- `data-testid="zone-1b-cohort-impact"` has bounding box height ≤ 60px — confirming it is hidden or shows only the empty-state element (cohort-empty-state message + optional header; no crossing rows)

**AC-P5 (Persona 5 — Aicha, 90-second ceiling):**
In the Senegal T3 conditionality scenario at step 2, with Zone 1B fully populated (MDA alerts
+ 4+ cohort crossing rows), at 1280×800:
- `data-testid="zone-1b-top-detail"` is visible at the initial viewport state (no scroll, no
  hover, no interaction) — confirming Aicha can read the MDA headline without Zone 1B scrolling
- `data-testid="detail-indicator-name"` (inside `zone-1b-top-detail`) is visible — confirming
  the indicator name is legible
- `data-testid="detail-status"` (inside `zone-1b-top-detail`) is visible — confirming the
  floor-distance status label is legible

**AC-P1 (Persona 1 — Lucas, cohort section readable):**
In the Senegal T3 conditionality scenario at step 2, at 1280×800:
- `data-testid="zone-1b-cohort-impact"` is visible (positive height) in Zone 1B without
  Zone 1B outer scroll
- `data-testid="cohort-row-0"` is visible within `data-testid="zone-1b-cohort-impact"` —
  confirming at least the first cohort crossing row is accessible
- If the scenario has more cohort rows than fit in Sub-zone B's visible height, Sub-zone B
  shows a vertical scroll indicator (CSS `overflow-y: auto` with content exceeding height) —
  confirming internal scroll is active; the QA Lead may assert this via bounding-box comparison
  between Sub-zone B container height and its scroll height

---

## 5b. Visual Spec (before/after)

**AC-A2 — overflow regression guard (illustrative; exact heights resolved at Phase 2):**

**Before (current — 8+ cohort rows causing MDA panel displacement):**
```
Viewport: 1280×800 | Zone: zone-1b | data-testid="zone-1b"
Senegal T3 conditionality · Step 2 · 8 cohort crossing rows loaded

Zone 1B (overflow: auto — SCROLLS AS A UNIT):
┌─────────────────────────────────────────────────┐
│ Zone 1B ↑                                       │  ← Zone 1B may scroll as a unit
│ [zone-1b-top-detail]                            │
│ CRITICAL — poverty_headcount_ratio               │
│ 3.5% below floor · Q1 Informal · T3             │
│────────────────────────────────────────────────  │
│ [zone-1b-cohort-impact] — CohortImpactSection   │
│  CRIT Q1 Informal · poverty_headcount_ratio ...  │
│  CRIT Q1 Informal · school_enrollment_rate ...   │
│  WARN Q2 Formal · employment_to_population ...   │
│  INFO Q1 Agricultural · gdp_per_capita ...       │
│  INFO Q2 Informal · ...                          │
│  INFO Q2 Agricultural · ...                      │
│  INFO Q1 Formal · ...                            │
│  INFO Q2 Agricultural (2nd indicator) · ...      │ ← rows 5-8 push the zone beyond height
│ ↓                                               │
└─────────────────────────────────────────────────┘

FAILURE MODE: MDA panel (`zone-1b-mda-panel-wrapper`) may have
bounding box height = 0 (displaced) or Zone 1B scrolls to show cohort
rows, leaving MDA panel off-screen below the scroll origin.
AC-A2 assertion FAILS before fix.
```

**After (G3 fix — explicit sub-zone allocation):**
```
Viewport: 1280×800 | Zone: zone-1b | data-testid="zone-1b"
Senegal T3 conditionality · Step 2 · 8 cohort crossing rows loaded

Zone 1B (overflow: hidden — NO OUTER SCROLL):
┌─────────────────────────────────────────────────┐
│ Zone 1B                                         │
│ [zone-1b-mda-panel-wrapper] — Sub-zone A        │  ← 80px min (ADR-018)
│   [zone-1b-top-detail]                          │
│   CRITICAL — poverty_headcount_ratio             │
│   3.5% below floor · Q1 Informal · T3           │
│   [zone-1b-trajectory-sentence]                  │
│   "HDI score crossed below floor at step 1..."  │
├─────────────────────────────────────────────────┤
│ [zone-1b-cohort-impact] — Sub-zone B            │  ← remaining height, internal scroll
│  CRIT Q1 Informal · poverty_headcount_ratio ...  │
│  CRIT Q1 Informal · school_enrollment_rate ...   │
│  WARN Q2 Formal · employment_to_population ...   │
│  [↓ scroll within Sub-zone B for rows 4-8]      │
└─────────────────────────────────────────────────┘

FIXED: zone-1b-mda-panel-wrapper always ≥ 80px (ADR-018).
zone-1b-cohort-impact scrolls internally. Zone 1B scrollTop = 0.
AC-A2 assertion PASSES after fix.
```

---

**AC-A4 — empty-state (MDA only, no cohort crossings):**

**After (G3 fix — MDA panel occupies full Zone 1B in single-occupant state):**
```
Viewport: 1280×800 | Zone: zone-1b | data-testid="zone-1b"
Senegal T3 conditionality · Step 1 (before first cohort crossing)

Zone 1B (overflow: hidden):
┌─────────────────────────────────────────────────┐
│ Zone 1B                                         │
│ [zone-1b-mda-panel-wrapper] — Sub-zone A        │  ← expands to full Zone 1B height
│   [zone-1b-top-detail]                          │     (single-occupant layout)
│   CRITICAL — reserves_coverage_months            │
│   2.1 months above floor · T3                   │
│   [zone-1b-trajectory-sentence]                  │
│   [zone-1b-compact]                              │
│                                                  │
│                                                  │
├─────────────────────────────────────────────────┤
│ [zone-1b-cohort-impact] — Sub-zone B            │  ← hidden or zero-height
│   [cohort-empty-state]                           │     when no crossings
└─────────────────────────────────────────────────┘

NOTE: cohort-section-header may still be visible with cohort-empty-state below it.
AC-A4 asserts: cohort-row-0 absent OR cohort-empty-state present.
```

---

## 6. Kryptonite Constraint Check

**Does this implementation's primary observable state require specialist mediation for
Persona 5 (Aicha) to act on it in the Reactive entry state (90-second ceiling)?**

`[x]` **No.** The proportional allocation model is a layout fix — it does not change the
content or semantics of Zone 1B. The MDA panel headline (severity chip, indicator name,
floor-distance) is already self-interpreting (DEMO6-010 fix in #1239 corrects the floor-label
direction). G3 ensures the MDA panel headline is visible without Zone 1B scroll. The layout
change is transparent to Aicha — she sees the MDA headline at the primary visual anchor
position, as she expects, without requiring the analyst to scroll.

**Note on Sub-zone B internal scroll:**
If Lucas scrolls within Sub-zone B to see additional cohort rows, Aicha does NOT see those
rows (she is at the table, not at the workstation). The scrollable state of Sub-zone B is
irrelevant to Aicha's 90-second ceiling. Aicha's critical information (MDA headline) is
always in Sub-zone A, always visible without interaction.

---

## 7. Out of Scope

**G2 Zone 1B per-scenario threshold crossings in comparison mode (#394):**
G2 Phase 3 will extend CohortImpactSection to show per-scenario threshold crossings.
G3 must not introduce a proportional allocation constraint that breaks the G2 data contract.
The Architect's Phase 2 assessment (§Phase 2 ADR Gate, Q2) confirms ADR compatibility
with the G2 per-scenario extension. G3 does not implement or define the G2 comparison-mode
Zone 1B layout.

**Zone 1B tablet legibility — font/sizing (#1250):**
#1250 (G4) fixes font size and minimum label size at 768px. G3's Q4 viewport contract confirms
that both Sub-zone A and Sub-zone B have non-zero height at 768px; it does not fix font
legibility. If #1250's font-size decisions affect the minimum readable height for Sub-zone A
or B, the G3 Architect consults #1250 implementation before finalizing ADR pixel values.
#1250 must merge before G3 Phase 3 implementation PR opens (per sprint entry hard gate).

**`minHeight: 80px` temporary constraint cleanup:**
G3 Phase 3 replaces the `minHeight: 80px` with the ADR-grounded allocation. The cleanup is
part of G3 implementation — it is not a separate cleanup PR. The implementation PR must
demonstrate (via the overflow regression guard test AC-A2) that the replacement is effective.

**Truncation with count label ("and N more"):**
Not in G3 scope. CohortImpactSection scrolls internally. A max-display count with count label
is a future enhancement that may be introduced if scroll UX is found to be inadequate in
practice. Not required for Demo 7.

**`data-testid="zone-1b-mda-panel-wrapper"` introduction:**
The MDA panel sub-zone wrapper in InstrumentCluster.tsx currently has no testid. G3 Phase 3
must add `data-testid="zone-1b-mda-panel-wrapper"` to the inner `<div>` that wraps the
mdaPanel slot (line 143 in `InstrumentCluster.tsx` as of 2026-06-25). This is a mandatory
implementation step — the QA bounding-box assertions in AC-A1, AC-A2, and AC-A3 depend on it.
The testid addition is NOT a separate issue — it is part of the G3 Phase 3 implementation PR.

**Mode 3 Zone 1B behavior:**
Mode 3 instrument layout will reference the G3 ADR for Zone 1B allocation. Mode 3 Zone 1B
behavior is M18+ scope. G3 implements Modes 1 and 2 allocation only.

---

## Phase 2 ADR Gate

> *To be completed by the Architect at Phase 2, after Phase 1 BPO acceptance.*

The Architect must file a determination note on GitHub issue #1252 answering three questions:

**Q1 — ADR path (Path A or Path B):**
Does the Zone 1B proportional allocation in §3.1 constitute an extension of ADR-017 (Zone 1A
information architecture — the governing premise "primary instruments always visible" is already
established there), or a standalone architectural decision requiring its own ADR?

- **Path A (ADR-017 amendment, ARCH-011 extension):** If the proportional allocation is a
  direct expression of Premise 2 already established in ADR-017, an amendment to ADR-017 is
  sufficient. The amendment must address the specific overflow contract, the sub-zone
  implementation, and the `minHeight: 80px` supersession.
- **Path B (new ADR, ARCH-012):** If the overflow contract, the single-vs-dual-occupant
  toggle, or the Zone 1B container `overflow` change represents a new architectural decision
  not derivable from ADR-017's premises, a new ADR is required. ARCH-012 must be assigned
  from the ADR backlog before drafting (per CLAUDE.md §No significant feature without an ADR).

**Q2 — G2 Phase 3 compatibility:**
Does the fixed-height Sub-zone A model (§3.1) create a forward constraint that conflicts with
G2 Phase 3's per-scenario Zone 1B threshold crossing display? Specifically: if G2 Phase 3
requires Zone 1B to show per-scenario threshold crossing rows (one row per scenario label),
does the G3 Sub-zone B allocation accommodate this without requiring a further ADR amendment?
The Architect must explicitly confirm compatibility or identify the conflict for EL scope
decision.

**Q3 — `minHeight: 80px` supersession:**
Does the ADR explicitly declare the `minHeight: 80px` temporary constraint (PR #1235) as
superseded? The ADR must include a statement that the permanent allocation contract governs
Zone 1B layout post-G3, removing any ambiguity about which constraint applies.

**[ADR-VALUE] resolution — COMPLETE:**
ADR-018 specifies Sub-zone A floor = **80px at all breakpoints** (codifying the PR #1235
temporary guarantee as the permanent architectural minimum). Estimated Zone 1B heights per
breakpoint are in §3.4. The implementing engineer must confirm measured Zone 1B heights at
runtime before QA thresholds are finalized. All [ADR-VALUE] placeholders in this document
have been replaced with resolved values (80px for Sub-zone A assertions; ≤ 60px for AC-A4
empty-state check; §3.4 table has estimated Zone 1B totals).

**Architect determination acknowledgment (to be filled at Phase 2):**
`[x]` Architect: ADR path determined (Path B — new ADR-018, ARCH-012). [ADR-VALUE] = 80px
      at all breakpoints. G2 compatibility confirmed (per FA review, ADR-018-panel-review.md).
      `minHeight: 80px` supersession declared in ADR-018 §Decision. 2026-06-25

---

## 8. Review Obligation

### Phase 1 review — Panel and BPO

*Review is conducted against §3 (Phase 1 UX brief decisions) and the reading-order constraint
in `docs/process/sprint-plans/m17-g3-sprint-entry.md §2.5`.*

**Panel members and minimum assessments:**

| Agent | Verdict required |
|---|---|
| UX Designer | Sign-off: all four Q1-Q4 answers satisfy the five governing UX premises (CLAUDE.md §UX Architectural Commitments); Premise 2 satisfied at 1280×800 and 768px; no governing premise violated |
| Design Thinking Agent | Verdict: Q1 proportional model keeps the MDA alert panel's severity headline visible without scrolling, under maximum expected cohort load; CohortImpactSection's internal scroll does not violate any cognitive task hierarchy requirement |
| Customer Agent | Pass/fail per persona: (a) Aicha can read MDA headline without Zone 1B scroll at 1280×800 and 768px; (b) Lucas can read CohortImpactSection content (at least partial view, with internal scroll accessible) at 1280×800. Any FAIL triggers a REJECT and document revision before BPO acceptance is requested. |
| Business PO | ACCEPT or REJECT after panel verdicts are all PASS. ACCEPT must be on record before Phase 2 begins. |

**Panel review format:** Each panel member records verdict as a comment on GitHub issue #1252.
UX Designer collects verdicts and produces a panel summary comment on #1252, tagging
@PublicEnemage. Panel summary must state: count of panel members reviewed, any REJECT verdict
and specific concern, whether the 768px constraint required a viewport-anchored mockup (and if
not, why prose specification was sufficient).

**BPO acknowledgment:**
`[ ]` Business PO: Phase 1 UX brief decisions (§3) satisfy the reading-order constraint and
      serve both Aicha and Lucas. Phase 2 (ADR authorship) may begin. [Date]

---

### Phase 3 QA test authorship

**QA Lead:** QA Lead Agent (Frontend)
**Test authorship deadline:** Before the #1252 Phase 3 implementation PR is opened against
`release/m17`. [ADR-VALUE] placeholders must be resolved before test numeric thresholds can
be finalized; QA Lead may author test structure before ADR is accepted.
**Test file:** `frontend/tests/e2e/m17-g3-zone-1b-allocation.spec.ts`

**Assertions required (from §5 ACs):**
- AC-A1: bounding box height checks for `zone-1b-mda-panel-wrapper` and `zone-1b-cohort-impact`; `zone-1b` scrollTop = 0
- AC-A2: 8+ cohort row scenario; `zone-1b-mda-panel-wrapper` height ≥ ADR minimum; **must be red before implementation** (comment citing sprint entry §2.2)
- AC-A3: viewport resize to 768px; `zone-1b-top-detail` visible; Zone 1B no outer scroll
- AC-A4: MDA-only step; `cohort-row-0` absent or `cohort-empty-state` present
- AC-P5: `zone-1b-top-detail`, `detail-indicator-name`, `detail-status` visible without interaction
- AC-P1: `cohort-row-0` visible within `zone-1b-cohort-impact`; Sub-zone B shows internal scroll when content exceeds height

**No soft-skip patterns** (NM-056 guard): All assertions must be hard-fail. Exception: AC-A2
uses `test.fail()` per EX-002 (approved 2026-06-25; see AC-A2 note above).

**Testid reconciliation (2026-06-25):** AC-A2 locator updated from `zone-1b-mda-panel` to
`zone-1b-mda-panel-wrapper` (aligning with ADR-018 and intent doc §5). Change applied in
same PR as `test.fail()` annotation.

**QA Lead acknowledgment:**
`[ ]` QA Lead: Tests for AC-A1 through AC-P1 authored and filed in
      `frontend/tests/e2e/m17-g3-zone-1b-allocation.spec.ts`. AC-A2 red confirmed before
      implementation. AC-A2 annotated with `test.fail()` (EX-002); reversal steps documented above.
      Date: [to be completed]

---

### Phase 3 implementation exit

**Implementing agent:** Frontend Engineer
**Pre-push gate:** `cd frontend && npm run build` — must exit 0 before feature branch is pushed (CLAUDE.md §Frontend pre-push build gate)
**Backend impact:** None — proportional allocation is a frontend-only layout change
**Required at exit:** Business PO acceptance + Customer Agent Layer 3 assessment (Persona 5 — Aicha, Persona 1 — Lucas)

---

*Design and implementation intent version: 2026-06-25. Issue #1252 (Zone 1B proportional
allocation) authorized as M17 G3 Wave 2 scope per `docs/process/sprint-plans/m17-sprint-plan.md
§Sprint Groups`. Phase 1 UX brief decisions (§3) authored by UX Designer Agent 2026-06-25.
Phase 2 ADR path pending Architect determination. Phase 3 implementation gated on: (1) Phase 1
BPO acceptance; (2) Phase 2 ADR accepted; (3) #1252 intent document [ADR-VALUE] placeholders
resolved; (4) QA test file authored; (5) #1250 merged to `release/m17`. Full sprint entry gate
conditions: `docs/process/sprint-plans/m17-g3-sprint-entry.md §EL Approval Record`. File
authority: UX Designer holds R on §3 (Phase 1 design decisions); PM Agent holds R on
document framing; QA Lead holds R on §8 Phase 3 QA acknowledgment.*
