---
name: ADR-014-alert-panel-ux
type: implementation-intent
adr: ADR-014
status: Filed
authored-by: Frontend Architect Agent
authored-date: 2026-06-13
implementing-agent: Frontend Architect Agent
---

# Implementation Intent: ADR-014 — Alert Panel Zone 1B Persistent-Detail Layout

## 1. Source ADR

**ADR:** ADR-014 — Alert Panel (Zone 1B) — Persistent Alert Detail with Scan-Only Compact List
**Status at time of authorship:** Accepted (2026-06-12)
**Authored by:** Frontend Architect Agent
**Date:** 2026-06-13
**Implementing agent:** Frontend Architect Agent (per ADR-014 panel)

---

## 2. Persona Trace Elements Targeted

**P-1 — Persona served:**
Primary: Persona 2 — Finance Ministry Negotiator (Eleni Papadimitriou archetype).
Secondary: Persona 3 — Political Advisor (Andreas Stefanidis archetype).

**P-2 — Entry state:**
Reactive entry state — 90-second total ceiling, negotiation room context. Journey B Step 3
establishes a 5-second ceiling for the alert read. After this implementation, that ceiling
covers the full breach evidence (severity, indicator, current vs. floor, consecutive breach
count, confidence label) with **zero interactions** from the moment Zone 1B is visible.

**P-3 — Journey reference:**
- Journey B Step 3 — "Scan: read the top MDA alert" — 5-second ceiling; full evidence now zero-interaction
- Journey B Step 4 — "Cite: formulate the argument" — breach evidence available immediately on instrument cluster load
- Journey C Step 3 — Mode 3 causal attribution appears in Zone 1B-detail for top alert without user action
- Journey D Step 2 — threshold orientation: Zone 1B-detail confirms specific threshold crossed and by how much

**P-4 — Time/interaction ceiling:**
**Zero interactions** to read the top alert's full evidence from the moment Zone 1B is visible
at 1440×900. Zero clicks. Zero scrolls. The instrument delivers argument evidence automatically.

**P-6 — Negotiating leverage delivered:**
After this layout change, Persona 2 can make the following specific argument at the moment she
opens the instrument cluster, with zero interactions:
> "The TERMINAL alert for reserve coverage has been active for 4 consecutive steps. Current
> value is 1.842 months against a floor of 3.0 — fully breached. Under your proposed adjustment
> timeline, this has already crossed the irreversible threshold. This is not a one-period
> anomaly; it is a structural drawdown that predates this negotiation session."

**P-7 — North star capability delivered:**
A Zambian finance ministry analyst in a live debt restructuring session can read the top
threshold breach's full evidence (severity, indicator, current vs. floor, consecutive step count,
confidence label, entity identity) from Zone 1B without any interaction from the moment the
instrument cluster loads — removing the interaction tax (scroll or click) that previously
prevented the ministry team from accessing the same evidence as the creditor side in the same
timeframe.

---

## 3. Observable Application State

### 3.1 Primary observable state

With the Greece 2012 scenario fixture loaded at step 4 in the live application at 1440×900,
`data-testid="zone-1b-top-detail"` is visible within Zone 1B bounds, contains
`data-testid="detail-indicator-name"` with non-empty text, `data-testid="detail-current-value"`
with a non-empty numeric string, and `data-testid="detail-consecutive"` with a non-empty text
value — **without any click or scroll event fired between fixture load and assertion**.

The detail slot is the topmost element in Zone 1B. A compact list sub-zone
(`data-testid="zone-1b-compact"`) appears below it. No click or scroll event is required to
read the detail slot contents.

### 3.2 Secondary observable states

**Secondary state A — TERMINAL auto-ranking:**
With a fixture containing ≥1 TERMINAL and ≥1 CRITICAL alert, at 1440×900 without any user
interaction: `data-testid="zone-1b-top-detail"` has `data-severity="TERMINAL"` and is
visible within Zone 1B bounds. The CRITICAL alert does not occupy the detail slot.

**Secondary state B — compact list is scan-only:**
With ≥2 active alerts loaded, compact rows (`data-testid="compact-alert-row"`) are rendered
in `data-testid="zone-1b-compact"` with `cursor: default`. Clicking any compact row produces
no change to the content of `data-testid="zone-1b-top-detail"`.

**Secondary state C — entity ISO code present:**
With the Hormuz JOR/EGY fixture loaded (two entities with simultaneous alerts), the detail
slot header contains a three-letter ISO code (`data-testid="detail-entity-id"`) and each
compact row contains a three-letter ISO code (`data-testid="compact-row-entity-id"`).

### 3.3 Silent failure detection

**SF-1 (detail collapses):** If Zone 1B-detail collapses (CSS specificity override, height 0),
the compact list fills all of Zone 1B with no visible detail above it — no error is thrown.
Detection: `data-testid="zone-1b-top-detail"` has `clientHeight > 0` at all three reference
viewports without user interactions.

**SF-2 (stale consecutive count):** If memoisation holds stale `mda_alerts[0]` across step
advances, Zone 1B-detail shows old `consecutive_breach_steps` while the compact list shows
updated alerts. Detection: after a step advance, assert `data-testid="detail-consecutive"` text
matches the current step's `consecutive_breach_steps` value for the top-ranked alert.

**SF-3 (click handler on compact rows):** If a refactor attaches an `onClick` to compact rows,
clicking them may trigger undefined behavior or silently promote an alert. Detection: assert
no compact row has cursor style other than `default`, and clicking a compact row produces no
change to `data-testid="zone-1b-top-detail"` content.

**SF-4 ([NEW] badge missing):** If `showNewBadge` change-detection uses array reference equality
instead of `mda_id` string comparison, the badge never fires when the top alert changes in
Mode 3. Detection: in a Mode 3 fixture, fire a control input causing a new highest-severity
alert; assert `data-testid="detail-new-badge"` is visible before any user interaction.

---

## 4. Acceptance Criteria

**AC-1 (UX-3 — primary, zero-interaction detail):**
In the Greece 2012 fixture scenario at step 4 at 1440×900, when the fixture loads (no clicks or
scrolls), then `data-testid="zone-1b-top-detail"` is visible within Zone 1B bounds and contains
`data-testid="detail-indicator-name"` with non-empty text and `data-testid="detail-current-value"`
with a non-empty numeric string.

**AC-2 (UX-6 — TERMINAL auto-ranking):**
In a fixture with ≥1 TERMINAL and ≥1 CRITICAL alert at 1440×900, when the fixture loads (no
clicks or scrolls), then `data-testid="zone-1b-top-detail"` has `data-severity="TERMINAL"` and
is visible (bounding-box within Zone 1B bounds confirmed by Playwright).

**AC-3 (SF-1 — detail height invariant across viewports):**
With any fixture containing ≥1 active alert, immediately after fixture load at each of 1024×768,
1280×800, and 1440×900, then `data-testid="zone-1b-top-detail"` has `clientHeight > 0` and
`data-testid="zone-1b-compact"` is present.

**AC-4 (SF-2 — consecutive count liveness):**
With a fixture where the top-ranked alert has `consecutive_breach_steps = N` at step S, when
the scenario advances to step S+1 (where the same alert persists with count N+1), then
`data-testid="detail-consecutive"` text reflects N+1 (not the stale value N). No memoisation
on alert list reference equality — the render must invalidate on every step advance.

**AC-5 (SF-3 — compact rows scan-only):**
With ≥2 active alerts loaded, when the compact sub-zone renders, then:
(a) every `data-testid="compact-alert-row"` element has computed `cursor: default`;
(b) clicking any compact row produces no change to `data-testid="zone-1b-top-detail"` content
    (no attribute changes, no text changes, no CSS class changes).

**AC-6 (SF-4 — [NEW] badge on mda_id change in Mode 3):**
In a Mode 3 fixture with an active CRITICAL alert in the detail slot, when a control input fires
causing a new TERMINAL alert (different `mda_id`), then `data-testid="detail-new-badge"` is
present and visible in `data-testid="zone-1b-top-detail"` before any user interaction within
Zone 1B.

**AC-7 (UX sign-off condition 1 — compact row height):**
With any fixture containing ≥2 active alerts at 1024×768, each `data-testid="compact-alert-row"`
element has computed height ≤ 26px. Single-line truncated text only — no multi-line overflow.

**AC-8 (UX sign-off condition 2 — mode-dependent tense in detail slot):**
(a) In Mode 1 with a breached alert: `data-testid="detail-status"` text contains "crossed" or
    historical past tense reflecting that the breach occurred at the named step.
(b) In Mode 2 with a projected breach: `data-testid="detail-status"` text contains "projected"
    or forward tense.
(c) In Mode 3 with an active breach: `data-testid="detail-status"` text contains "BREACHED".

**AC-9 (entity ISO code — Q1 ruling):**
With the Hormuz JOR/EGY fixture loaded, `data-testid="zone-1b-top-detail"` contains
`data-testid="detail-entity-id"` with a non-empty three-letter ISO string, and each
`data-testid="compact-alert-row"` contains `data-testid="compact-row-entity-id"` with a
non-empty three-letter ISO string.

**AC-10 (confidence tier per-step — Q4 ruling):**
With a fixture where the top TERMINAL alert persists for 4+ steps, when the scenario advances
from step 1 to step 4, then `data-testid="detail-negotiation-label"` text is identical at step 1
and step 4 — confidence tier label does not change as a function of consecutive count.

---

## 5. Kryptonite Constraint Check

**Does this implementation's primary observable state require specialist mediation for Persona 2
to act on it in the Reactive entry state (90-second ceiling)?**

`[x]` No — the observable state is interpretable by Persona 2 without an analyst translating it.

Rationale: The persistent-detail layout eliminates the interaction tax that previously prevented
the ministry-side analyst from reading breach evidence in the reactive window. The data (current
vs. floor, consecutive steps, confidence label) is self-interpreting per the negotiation-
defensibility label system. No specialist is required to translate "BREACHED · 4 consecutive
steps · Moderate confidence — cite with caveat." This is precisely the kryptonite test: the
ministry team reads the same evidence as the creditor side without mediation.

---

## 6. Out of Scope

The following are explicitly outside this implementation and must not appear in the G7 PR:

**Out of scope per ADR-014 §Alternatives Considered and §Known Limitations:**
- Sparkline in Zone 1B-detail (explicitly excluded — height budget decision; Zone 1A covers
  trajectory visualization)
- Per-cohort income disaggregation beyond the named `cohort` subheader field
- Full synthetic data provenance disclosure in Zone 1B (Zone 3 surface)

**Out of scope per Section 5 deferred rulings in `m13-g7-sprint-entry.md`:**
- Zone 1B causal grouping for Mode 1/2 (Q2 deferred — backend schema gap, follow-on ADR required)
- Alert storm visual indicator / count pill (Q3 partial deferral — follow-on ADR amendment)
- Alert lifecycle management — dismiss and archive (Q5 deferred — governing premise conflict)
- Zone 1A/1B bidirectional coupling — alert-triggered trajectory highlight (Q6 deferred)
- Any hover or click handler on Zone 1B-detail or Zone 1B-compact rows for Zone 1A coupling

**Level 4 entity population tiebreak:** Entity population data is not available in the current
`mda_alerts` API response or any accessible frontend store without a new API call. Level 4 of
the ranking rule (entity population DESC) falls back to **stable insertion-order sort** for any
alerts tying on levels 1–3. This resolution is observable: two TERMINAL alerts with the same
step_index and confidence_tier from different entities appear in a consistent, stable order
on every render. A future PR may add population to the API payload to enable true Level 4.

---

## 7. Implementation Specification

### 7.1 Component changes

**`Zone1BAlert` interface (`frontend/src/store/scenarioStepStore.ts`):**
Add `entity_id: string` field. This field is already present in `RawMDAAlert` and is populated
by the backend; it was not previously mapped into `Zone1BAlert`.

**`parseMdaAlerts` in `frontend/src/components/ScenarioInstrumentCluster.tsx`:**
Add `entity_id: raw.entity_id` to the `Zone1BAlert` object constructed for each alert.

**`sortAlerts` in `frontend/src/components/MDAAlertPanelZone1B.tsx`:**
Extend from 2-level to 4-level ranking rule (per §5.3 of sprint entry):
1. `severity` DESC (TERMINAL=0, CRITICAL=1, WARNING=2)
2. `step_index` ASC (earlier breach first)
3. `confidence_tier` ASC (lower number = higher confidence)
4. Stable insertion-order sort (Level 4 population fallback — population data not available)

**`MDAAlertPanelZone1B` component (`frontend/src/components/MDAAlertPanelZone1B.tsx`):**

Remove:
- `focusedAlertMdaId` prop
- `onSelectAlert` prop
- Inline `AlertDetailPanel` render from `MDAAlertPanelZone1B`'s JSX
- `mda-more-alerts` overflow indicator (replaced by `+N more ↕` in compact sub-zone)

Add:
- `TopAlertDetail` internal sub-component: renders the detail slot for the top-ranked alert
  without sparkline. Fields: severity pill, indicator display name, framework abbrev, step,
  entity ISO code, cohort subheader (conditional — omit for "all cohorts"), current/floor
  values row, mode-dependent status text row, consecutive breach steps, negotiation label,
  causal attribution (Mode 3 only). `data-testid="zone-1b-top-detail"`, `data-severity`,
  `data-alert-id` on the outer container.
- `CompactAlertList` internal sub-component: renders remaining alerts (all except top-ranked)
  as scan-only rows. Each row: severity abbrev in severity color, entity ISO code, indicator
  name (truncated), step. No `onClick`. No `onMouseEnter`. `cursor: default` on all rows.
  `data-testid="compact-alert-row"` on each row. `data-testid="zone-1b-compact"` on the
  container. `+N more ↕` indicator when list overflows.
- `showNewBadge` state (`boolean`) + change-detection: compare `mda_alerts[0]?.mda_id` to
  previous render's top alert `mda_id` using a `useRef`-tracked previous value. Set
  `showNewBadge = true` when `mda_id` changes. Clear on any user interaction within Zone 1B
  (scroll of compact list, click anywhere within Zone 1B bounds). `data-testid="detail-new-badge"`
  on the badge element.

Outer container layout change:
- `overflowY: "auto"` → `display: "flex"; flexDirection: "column"; height: "100%"; overflow: "hidden"`
- `TopAlertDetail`: `flex: "0 0 auto"; overflow: "hidden"`
- `CompactAlertList` container: `flex: "1 1 auto"; overflowY: "auto"`

**`AlertDetailPanel` — export and retain:**
Export `AlertDetailPanel` from `MDAAlertPanelZone1B.tsx` for future `EntityDetailDrawer` use.
The scroll-into-view `useEffect` (lines 162–163 in current file) is retained in the exported
component as it will be needed by EntityDetailDrawer. `AlertDetailPanel` is NOT rendered by
`MDAAlertPanelZone1B` after this change.

**`ScenarioInstrumentCluster.tsx`:**
Remove `focusedAlertMdaId` state and `onSelectAlert` handler (lines ~235, ~619–620).
Remove the props passed to `MDAAlertPanelZone1B`.

### 7.2 Mode-dependent tense in detail slot (UX sign-off condition 2)

Per `information-hierarchy.md §1B` ("Alert tense is mode-dependent"):

The detail slot's status row (`data-testid="detail-status"`) renders:

| Mode | `approach_pct_remaining ≤ 0` | `approach_pct_remaining > 0` |
|---|---|---|
| MODE_1 | "crossed threshold at step N" | "N% above floor at step N" |
| MODE_2 | "BREACH PROJECTED at step N" | "N% above floor (projected)" |
| MODE_3 | "BREACHED" | "N% above floor" |

Where N is the `step_index` of the alert. This replaces the current `AlertDetailPanel`'s
"BREACHED" / "N% remaining" approach text.

The Mode 3 causal attribution line ("Caused by: …") is displayed below the status row,
conditional on `alert.causal_attribution !== null`.

### 7.3 Compact row height constraint (UX sign-off condition 1)

Compact rows are single-line, max 26px height, with text truncation (indicator name ≤ 22 chars).
CSS: `height: 24px; maxHeight: 26px; overflow: hidden; whiteSpace: nowrap; textOverflow: ellipsis`
on the row container. No multi-line wrapping.

### 7.4 Compact row cohort omission (UX sign-off condition 3)

Compact rows do NOT display the `cohort` field. Rationale (ADR-014 ruling, recorded here per
UX sign-off condition 3): compact rows are a severity-rank scan surface, not an evidence surface.
The `information-hierarchy.md §1B` "top affected cohort" requirement applied to the stacked-list
design and predates the persistent-detail model. Under the persistent-detail model, cohort detail
belongs in the Zone 1B-detail slot (shown as a subheader when not "all cohorts") and Zone 2.
This deviation is accepted; documented here as required by the UX Designer conditional sign-off.

### 7.5 "+N more ↕" count

N = `(total_alerts - 1) - visibleCompactRowCount`, where `visibleCompactRowCount` is the number
of compact rows that fit within Zone 1B-compact's visible height at max 26px per row. When N > 0,
render: `+{N} more ↕` in a muted style at the bottom of Zone 1B-compact.
`data-testid="compact-more-indicator"` on this element.

### 7.6 [NEW] badge persistence rule

Badge clears on the next user interaction within Zone 1B bounds:
- `onScroll` on Zone 1B-compact container → clear badge
- `onClick` anywhere on Zone 1B outer container → clear badge

Badge does NOT clear on a timer, after a fixed duration, or when only `consecutive_breach_steps`
increments (same `mda_id` persisting). Badge only fires on `mda_id` change at position 0 of
the sorted alert list.

---

## 8. Test Authorship Obligation

**QA Lead:** QA Lead Agent
**Test authorship deadline:** Before any implementation PR is opened
**Test file location:** `frontend/src/components/__tests__/zone1b-persistent-detail.spec.ts`
**Relevant ADR acceptance criteria:** AC-1 through AC-10 (Section 4 above)

**Additional test references from ADR-014 silent failure modes:**
- SF-1: `clientHeight > 0` at 1024×768, 1280×800, 1440×900 — no user interactions
- SF-2: consecutive count liveness after step advance
- SF-3: cursor default on compact rows; click produces no detail slot change
- SF-4: [NEW] badge fires on mda_id change in Mode 3

**QA Lead acknowledgment:**
`[x]` QA Lead: Tests for AC-1 through AC-10 authored and filed. 2026-06-13
- E2E Playwright tests: `frontend/tests/e2e/zone1b-persistent-detail.spec.ts`
- Unit tests (sortAlerts 4-level, getDetailStatusText, entity_id): `frontend/src/components/__tests__/zone1b-persistent-detail.test.ts`

---

*Intent document version: 2026-06-13. ADR-014 accepted 2026-06-12. Implementing agent: Frontend
Architect Agent. Kryptonite constraint: PASS — zero specialist mediation required. Three UX
Designer sign-off conditions resolved in §7.2 (mode-dependent tense), §7.3 (compact row height),
and §7.4 (compact row cohort omission). All Section 5 resolved specifications from sprint entry
document `m13-g7-sprint-entry.md` encoded in §7 and §6.*
