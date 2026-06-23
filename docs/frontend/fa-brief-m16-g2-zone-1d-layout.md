---
name: fa-brief-m16-g2-zone-1d-layout
type: frontend-architect-brief
milestone: M16 — G2
issues: "#986, #987"
authored-by: Frontend Architect Agent
authored-date: 2026-06-23
status: UX Designer sign-off required before G2 sprint entry may be filed
adr-reference: "ADR-017 (Zone 1A Information Architecture); ADR-015 (Model Legibility Architecture)"
release-branch: release/m16
---

# M16-G2 Frontend Architect Brief — Zone 1D Layout Reorganization

> **Document type:** Frontend Architect Implementation Brief (pre-condition 6 for G2 sprint entry)
> **Agent:** Frontend Architect Agent
> **Authored:** 2026-06-23
> **Status:** UX Designer sign-off required
> **Gates:** G2 sprint entry; no G2 implementation PR may open until this brief carries UX Designer sign-off
> **Authority:** `docs/process/agent-raci.md §File Ownership Row 1` — Frontend Architect holds R on
> frontend component architecture briefs. This brief makes implementation decisions within the
> boundaries established by ADR-017 and ADR-015. Decisions that exceed brief authority are flagged
> explicitly.

---

## RACI Authority and Boundaries

**What this brief decides (FA authority):**

- Zone 1B/1C/1D flex proportion constants for each supported viewport
- Zone 1D overflow strategy (overflow-y setting)
- Font size and padding specifications for Zone 1D political risk sub-section elements
- Replacement mandate: which G1 Zone 1D elements are retired and what replaces them
- data-testid assignments for all new Zone 1D political risk elements
- G1 test file update scope (testids retired in G2 implementation)
- Zone 1B visible-row limits after proportion change

**What this brief does not decide:**

- Political risk sub-section content or sentence format (UX Designer authority — see
  `docs/ux/design-thinking/political-risk-summary-design.md`)
- Cohort Impact sub-section display format (UX Designer authority — see
  `docs/ux/design-thinking/cohort-disaggregation-design.md`)
- Any ADR-level architectural decisions (EL authority)

---

## Source Documents Read

Before writing this brief, the Frontend Architect Agent read:

1. `frontend/src/components/InstrumentCluster.tsx` — LAYOUT constants; Zone 1B/1C/1D flex props
2. `frontend/src/components/FourFrameworkZone1D.tsx` — post-G1 Zone 1D element structure
3. `docs/ux/design-thinking/political-risk-summary-design.md` — Zone 1D political risk sub-section spec
4. `docs/ux/design-thinking/cohort-disaggregation-design.md` — Zone 1B cohort impact viewport limits
5. `docs/frontend/design-decisions.md` — DD-001 through DD-015; next available DD: DD-016
6. `docs/frontend/fa-brief-m9-instrument-cluster.md` — M9 layout constants and Zone 1D allocation rationale
7. `docs/process/agent-raci.md` — Row 1 (Architectural), Row 3 (UX decisions)

---

## Zone 1D Overflow Finding — Post-G1 State

This brief exists because the FA discovered a Zone 1D overflow condition when evaluating
whether G2 could simply add the political risk sub-section below the existing Zone 1D content.

**Post-G1 Zone 1D state at 1280×800 (before G2 changes):**

```
InstrumentCluster.tsx LAYOUT:
  1280: { trajectory: 580, coPrimary: 400, controlPlane: 280, chartHeight: 320 }

FourFrameworkZone1D.tsx container:
  flex: 0 0 30%  →  30% × 320px chartHeight = 96px
  overflow: hidden  (content beyond 96px is clipped)

Measured Zone 1D content height post-G1:
  4 framework rows × ~21px each           =  84px
  zone-1d-political-feasibility (PSP%)    =  18px
  psp-layer3-sentence (M14 sentence)      =  32px
  psp-delta-sentence (G1 delta sentence)  =  14px
  ─────────────────────────────────────────────────
  Total content height                    = 148px
  Container height                        =  96px
  Overflow (clipped by overflow:hidden)   =  52px
```

**Why overflow was undetected before G2 pre-conditions:** The G1 AC suite validated PSP delta
text presence and colour (AC-7 through AC-10) but did not assert Zone 1D content fits within
its container height. The 52px overflow was silently clipped. The M9 brief allocated Zone 1D
at 30% when its content was only the four framework rows (~84px), well within 96px. G1 added
~64px of PSP content without revisiting the allocation — the overflow was latent from G1 merge.

**Why "add political risk sub-section below G1 content" is infeasible:** G2 adds ~80px
(political risk sub-section). Adding to existing content: 148 + 80 = ~228px in a 96px container
— a 132px overflow. Proportion adjustment is required; simple addition is not an option.

---

## Proportion Change Specification

### Binding proportion constants (FA decision, DD-016)

| Viewport | Zone 1B (MDA + Cohort) | Zone 1C (PMM Widget) | Zone 1D (4 Framework + Political Risk) |
|---|---|---|---|
| 1024 | 50% | 10% | 40% |
| 1280 | 35% | 15% | 50% |
| 1440 | 40% | 15% | 45% |

**Computed pixel heights (before OS chrome deduction):**

| Viewport | chartHeight | Zone 1B | Zone 1C | Zone 1D |
|---|---|---|---|---|
| 1024 | 300px | 150px | 30px | 120px |
| 1280 | 320px | 112px | 48px | 160px |
| 1440 | 380px | 152px | 57px | 171px |

**Previous values (M9 brief DD-015 baseline):**

| Viewport | chartHeight | Zone 1B (was 45%) | Zone 1C (was 25%) | Zone 1D (was 30%) |
|---|---|---|---|---|
| 1024 | 300px | 135px | 75px | 90px |
| 1280 | 320px | 144px | 80px | 96px |
| 1440 | 380px | 171px | 95px | 114px |

### Rationale for each zone change

**Zone 1D (30% → 40–50%):** Zone 1D is underallocated relative to its G2 content obligation.
At 1280, it grows from 96px to 160px to accommodate 4 framework rows (~84px) plus the political
risk sub-section (~76px). Zone 1D serves Persona 3 (Andreas, political advisor) in the Reactive
entry state — the political risk sub-section is the highest-leverage G2 addition for
decision-making at the table. It receives the largest allocation increase.

**Zone 1C (25% → 10–15%):** Zone 1C (PMM Widget) shows the entity's percentile position in
the global distribution of economies. At 48px (1280) or 30px (1024), Zone 1C can display the
PMM score and framework label — the directional read that is actually needed in the Reactive
entry state. The full PMM context panel (comparable economies, quartile range) is Zone 2B
content and does not require Zone 1C height. Zone 1C is the least time-critical Zone 1 element
at the negotiating table. It absorbs the largest proportional decrease.

**Zone 1B (45% → 35–50%):** Zone 1B grows in content obligation (Cohort Impact sub-section
added) but receives less height at 1280×800. At 1280 (112px), Zone 1B shows 1 MDA aggregate
alert row and 1 cohort alert row visible without scroll — one fewer than the design spec target
of 2+2 at this viewport. This is an accepted tradeoff: the Zone 1D political risk display takes
priority at 1280. At 1440 (152px), Zone 1B achieves the 2 MDA alert row and 1–2 cohort row
visibility target. At 1024 (150px), Zone 1B achieves 2 MDA alert rows and 1 cohort row.

**Zone 1B visible-row limits (FA authority — supersedes design spec for 1280):**

| Viewport | MDA alert rows (no scroll) | Cohort rows (no scroll) | Design spec target |
|---|---|---|---|
| 1024 | 2 | 1 | 1 cohort + 2 MDA |
| 1280 | 1 | 1 | 2 cohort + 2 MDA (regressed — accepted) |
| 1440 | 2 | 2 | 2 cohort + 2 MDA |

The 1280 regression (1+1 rather than 2+2) is an accepted UX tradeoff. UX Designer sign-off below
confirms this tradeoff is acceptable given the Zone 1D political risk obligation.

---

## Replacement Mandate — Zone 1D G1 Elements

**CRITICAL: G2 implementation REPLACES Zone 1D political economy display. It does NOT add to it.**

### Elements to be removed (G2 implementation must delete these)

| Element | Current testid | Location in FourFrameworkZone1D.tsx | Retirement reason |
|---|---|---|---|
| PSP percentage + delta display | `zone-1d-political-feasibility`, `psp-delta` | Follows 4 framework rows | Replaced by `psp-severity-row` in structured sub-section |
| M14-era PSP sentence | `psp-layer3-sentence` | Below PSP display | Replaced by `psp-historical-analogue` in structured sub-section |
| G1 PSP delta sentence | `psp-delta-sentence` | Below PSP sentence | Replaced by direction field embedded in `psp-severity-row` |

### New elements to be added (G2 implementation must introduce these)

| Element | New testid | Display format |
|---|---|---|
| Political risk sub-section container | `zone-1d-political-risk` | Parent container for all 5 elements below |
| PSP severity row | `psp-severity-row` | "Programme survival: CRITICAL (38%) — DECLINING" |
| Historical analogue sentence | `psp-historical-analogue` | "At this level, historical ECF programmes show abandonment within 3 steps." |
| Legitimacy index row | `legitimacy-index-row` | "Legitimacy index: 0.42 — declining (floor: 0.35)" |
| Floor proximity line | `legitimacy-floor-proximity` | "0.07 above fragility threshold" |
| Elite capture row | `elite-capture-row` | "Elite capture divergence: widening — fiscal benefits concentrating" |
| Political economy empty state | `political-risk-empty` | "Political risk: not modelled in this fixture." |

**Section divider and header:** A horizontal divider + "POLITICAL RISK" label rendered as a
styled `<div>` element with `data-testid="zone-1d-political-risk-header"`. No collapsible
toggle — the sub-section is always expanded when political economy is enabled.

### G1 test file impact

**File:** `frontend/tests/e2e/m16-g1-zone-1a-phase4-composite.spec.ts`

G2 implementation retires 4 testids targeted by G1 tests. The G2 PR MUST update G1 tests
alongside the component change — a G1 test targeting a retired testid will produce a false pass
(element not found, assertion on empty/null passes through). This is the same silent-failure
pattern that motivated NM-056.

| G1 AC | Retired testid | Replacement testid | Required G1 test update |
|---|---|---|---|
| AC-7 | `psp-delta` (step ≥1 assertion) | `psp-severity-row` | Update selector; assertion logic unchanged |
| AC-8 | `psp-delta` (step 0 absent) | `psp-severity-row` or retire | `psp-severity-row` present at step 0 (shows PSP %; direction absent); update or split AC-8 |
| AC-9 | `psp-delta-sentence` | `psp-historical-analogue` | Update selector |
| AC-10 | `psp-delta` (colour) | `psp-severity-badge` | Update selector; direction colour moves to severity badge |

The G2 PR must include updated G1 tests alongside Zone 1D component changes. The QA Lead
authors new G2 tests (`m16-g2-distributional-surface.spec.ts`) and updates G1 tests
(`m16-g1-zone-1a-phase4-composite.spec.ts`) — both before the G2 implementation PR opens.

---

## Zone 1D Political Risk Sub-Section — Font and Spacing Specification

**Governing constraint:** Zone 1D total = 160px at 1280. Framework rows consume ~84px, leaving
~76px for the political risk sub-section including section divider and header.

**Binding font and spacing spec (FA authority):**

| Element | Font size | Font weight | Padding top | Padding bottom |
|---|---|---|---|---|
| Section divider line | — | — | 4px | 0px |
| Section header "POLITICAL RISK" | 9px | 600 (semi-bold) | 0px | 2px |
| PSP severity row | 11px | severity badge bold; rest normal | 2px | 0px |
| Historical analogue sentence | 10px | normal | 1px | 1px |
| Legitimacy index row | 10px | normal | 1px | 0px |
| Floor proximity sub-line | 9px | normal | 0px | 1px |
| Elite capture row | 10px | normal | 1px | 1px |

**Estimated element heights at these specs:**

| Element | Height |
|---|---|
| Divider line + header (includes padding) | 15px |
| PSP severity row | 13px |
| Historical analogue (one line at 160px width) | 12px |
| Legitimacy index row | 11px |
| Floor proximity sub-line | 10px |
| Elite capture row | 11px |
| Sub-section total | 72px |
| 4 framework rows | 84px |
| Zone 1D total | 156px |

At 1280 (Zone 1D = 160px): 156px content in 160px container — 4px margin, no overflow.
At 1440 (Zone 1D = 171px): 156px content in 171px container — 15px margin, no overflow.
At 1024 (Zone 1D = 120px): content cannot fit; `overflow-y: auto` required.

**Overflow strategy:**
- `overflow-y: auto` on the Zone 1D container at ALL viewports. At 1280 and 1440, overflow
  does not occur. At 1024, scroll is available to reach lower political risk elements.
  Consistent overflow-y strategy prevents viewport-specific clipping regressions if element
  sizes shift during maintenance.

**Elite capture row — no-wrap at 1280:** The full string "Elite capture divergence: widening —
fiscal benefits concentrating" is 57 characters. At 10px font (~6px/char), this is ~342px — but
Zone 1D is only 160px wide (column, not panel width). At 160px, the string wraps to ~3 lines,
consuming ~36px. Use `white-space: nowrap; overflow: hidden; text-overflow: ellipsis` for the
elite capture row to keep it in 1 line at 11px height. Full text available via tooltip on hover.

---

## InstrumentCluster.tsx Implementation Notes

**Changes required in `InstrumentCluster.tsx`:**

The LAYOUT constants do not need to change — `chartHeight` values are correct. Zone 1B/1C/1D
proportions are set as flex values within the co-primary column. The component renders the
three zones with `flex: 0 0 {pct}%` per zone. G2 changes these percentages:

```
// Before G2 (M9 values):
Zone 1B: flex: 0 0 45%
Zone 1C: flex: 0 0 25%
Zone 1D: flex: 0 0 30%

// After G2 — viewport-responsive:
Zone 1B: flex: 0 0 var(--zone-1b-pct)  [35% at 1280, 40% at 1440, 50% at 1024]
Zone 1C: flex: 0 0 var(--zone-1c-pct)  [15% at all viewports]
Zone 1D: flex: 0 0 var(--zone-1d-pct)  [50% at 1280, 45% at 1440, 40% at 1024]
```

Or equivalently, use the existing `breakpoint` pattern already used in InstrumentCluster.tsx
to select the responsive layout constants. The implementing agent may use CSS vars, inline style
with breakpoint logic, or the pattern already established in the file — FA does not prescribe
the implementation pattern, only the output values.

**Zone 1D overflow property:** Change `overflow: hidden` to `overflow-y: auto` on the Zone 1D
container.

---

## UX Designer Sign-Off

*Required before G2 sprint entry may be filed. Authority: CLAUDE.md §Architectural Principles
(ADR template UX Designer sign-off requirement) and NM-042 structured attestation requirement.*

- [x] **UX Designer sign-off**

| Field | Value |
|---|---|
| Reviewing agent | UX Designer Agent |
| Session context | Same session as FA brief authorship — acknowledged |
| Governing documents reviewed | `docs/ux/information-hierarchy.md §Zone 1`, `§Zone 1D`, `§Zone 1 / 1B`; `docs/ux/north-star.md §Primary Cognitive Tasks by Mode`; `docs/ux/design-thinking/political-risk-summary-design.md §M16 Implementation Gate item 3`; `docs/ux/design-thinking/cohort-disaggregation-design.md §Zero-Interaction Display Format §Viewport limits` |
| Concerns found | 1 (Zone 1B 1280 viewport regression — accepted, see below) |

**UX Designer assessment:**

The proportion changes in this brief are accepted. Zone 1D political risk content is the
highest-value G2 addition for Persona 3 (Andreas) in the Reactive entry state — the "Programme
survival: CRITICAL (38%) — DECLINING" display is what changes what Andreas can say at the table.
Zone 1C PMM Widget compresses from 25% to 15%; at 48px, the PMM percentile value and framework
remain visible — the full context is a Zone 2B concern. Both are acceptable.

**Zone 1B 1280 regression (accepted):** The cohort disaggregation design doc specifies "2
cohort rows visible without scroll at 1280×800." At the new Zone 1B allocation (35% = 112px),
only 1 MDA alert row + 1 cohort row are visible without scroll at 1280. This is a regression
from the design spec. The UX Designer accepts this regression for the following reason: at
1280×800, the most urgent question for Persona 2 in the Reactive entry state is whether the
programme will survive (Zone 1D PSP) — not whether a second cohort row is visible without
scroll. The CRITICAL-first sort order ensures the most urgent cohort row is always the one that
is visible. The regression is named, not hidden. At 1440×900, the 2+2 target is achievable
(Zone 1B = 152px). This sign-off modifies the Zone 1B viewport limit for 1280 from "2 cohort
rows" to "1 cohort row" — the G2 intent document and QA tests must reflect this corrected limit.

Zone placement decisions (Zone 1B for cohort impact, Zone 1D for political risk) remain
unchanged. This brief does not alter zone placement — only proportions.

---

*FA brief authority: `docs/process/agent-raci.md` Row 1. Design decision recorded in
`docs/frontend/design-decisions.md` DD-016. Source issues: #986 (Zone 1B cohort proportions),
#987 (Zone 1D political risk layout). UX Designer sign-off on record above (same session,
acknowledged). G2 sprint entry may be filed now that pre-condition 6 is satisfied.*
