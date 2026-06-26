---
name: M17-G4-zone-1a-curve-identifiability
type: implementation-intent
issues: "#1249"
status: Step 1 authored — QA tests may be authored immediately; implementation PR may open once tests are filed
authored-by: Frontend Architect Agent
authored-date: 2026-06-25
implementing-agent: Frontend Engineer
sprint-entry: "docs/process/sprint-plans/m17-g4-sprint-entry.md — EL Approved 2026-06-25"
ux-visual-spec: "docs/ux/specs/m17-g4-1249-zone-1a-curve-identifiability.md"
adr-reference: "N/A — encoding addition within ADR-017 Zone 1A compare-mode boundary; no architectural decision required"
release-branch: release/m17
---

# Implementation Intent: M17-G4 — Zone 1A Curve Identifiability (#1249)

> **UX visual spec governs.** All observable state requirements are derived from
> `docs/ux/specs/m17-g4-1249-zone-1a-curve-identifiability.md`.
>
> **FA implementation sequence:** #1249 is the 1st issue in FA sequence
> (#1249 → #1253 → #1250 → #1239). This must merge before any other G4 issue.
> G2 Phase 3 (#394) implementation PR is gated on #1249 merging.

---

## 1. Source

**Issue:** #1249 — ux(zone-1a): DEMO6-014 curve identifiability

**Root cause:** In `CompositeChartSVG` (TrajectoryView.tsx lines 389–563), each entity's
active composite trajectory is rendered as an SVG `<path>` element with a color from
`ENTITY_PALETTE`. The existing identification mechanism is the `entity-labels-overlay`
div (positioned as an absolute-positioned overlay in the top-right corner of Zone 1A)
which shows entity codes ("ZMB", "GRC") stacked vertically. This overlay is spatially
disconnected from the curve endpoints — at 80% zoom during a live demo, it is not
possible to tell at glance level which label corresponds to which curve when curves are
proximate or crossing.

**The fix:** Add `<text>` terminal label elements to `CompositeChartSVG`, positioned
directly at (x+3, y-7) relative to each entity's last data point. Labels show the
entity code (or, when G2 Phase 3 provides it, a scenario identifier). Testids:
`zone-1a-terminal-label-{code}`.

**N=3 compatibility constraint (sprint entry §2.2):** The same terminal label approach
works for N=3 without modification — ENTITY_PALETTE has 4 slots (positions 0–3);
three entities / scenarios use positions 0–2. G2 Phase 3 passes label content via
entity codes (or scenario identifiers that are treated as entity codes in the existing
composite path). Step 4 Verify must confirm N=3 visual compatibility at the Greece+Zambia
N=2 baseline AND at a hypothetical N=3 layout check.

---

## 2. Persona Trace Elements Targeted

**P-1 — Persona served:** **Persona 1 — Lucas Ferreira (Ministry Analyst)**
(`docs/ux/personas.md §Persona 1`). Zone 1A trajectory curves in compare mode present
the structural evidence used in conditionality comparisons. Lucas needs to identify
which trajectory belongs to which scenario/entity at glance level to narrate the
divergence pattern to a minister.

Secondary: **Persona 3 — Andreas Petrakis** who reads Zone 1A curve divergence in
COMPARE_VIEW to construct political-economy pattern arguments.

**P-2 — Entry state:** Reactive — Journey B Step 3 and COMPARE_VIEW. Compare mode
is entered by selecting a second entity or scenario; the Zone 1A view immediately
shows two curves.

**P-3 — Journey reference:** Journey B Step 3 (COMPARE_VIEW multi-entity); Journey 3
Step AC-S1 (G2 Phase 3 scenario comparison — dependent future journey).

**P-4 — Time/interaction ceiling:** 90 seconds (Reactive). Zone 1A must be readable
at glance level. No hover or click required to identify curves.

**P-6 — Negotiating leverage delivered (Persona 1):**
Lucas can narrate: "The blue curve is ZMB — it diverges from GRC at step 2, dropping
below the MDA floor by step 4." Without terminal labels, he must first trace which
curve is which — consuming attention during a live demo.

**P-7 — North star capability delivered:**
After this fix, any analyst reading Zone 1A in compare mode can identify which curve
belongs to which entity or scenario directly from the curve endpoint label, without
consulting a separate legend. This is required for the Demo 7 live presentation where
two-scenario comparison is a primary walkthrough step.

---

## 3. Observable Application State

### 3.1 Primary observable state

Zone 1A in COMPARE_VIEW with two entities active (e.g., GRC and ZMB), at 1280×800:

Two `<text>` SVG elements are present at the right edge of the trajectory chart area,
each positioned adjacent to the last data point of its entity's composite path:
- `data-testid="zone-1a-terminal-label-GRC"` (or ZMB) is visible without scrolling
- Each label text matches the entity code (e.g., "GRC", "ZMB")
- Each label is colored in the entity's ENTITY_PALETTE color

Observable confirmation without source code: Load a two-entity scenario (e.g., ZMB +
GRC), navigate to the trajectory view at 1280×800, and inspect the right edge of Zone 1A.
Two short text labels should appear at the curve endpoints — one per entity, adjacent to
the curve's rightmost data point, vertically aligned to the curve's y-position.

### 3.2 Secondary observable states

**State A — Single-entity regression:**
In N=1 single-entity Mode 1/2 (recharts path), no `zone-1a-terminal-label-*` elements
are present. The recharts path is unaffected by this fix. The existing recharts Legend
remains the sole labeling mechanism for single-entity four-framework curves.

**State B — N=2 labels distinct:**
In N=2 compare mode, the two terminal labels are visually distinct at 1280×800 — neither
label obscures the other. (Implementation note: if y-positions of the two curve endpoints
differ by less than 14px, the implementing agent applies a `dy` offset — see UX spec §7.)

**State C — tier badges unaffected:**
The tier badges (`zone-1a-tier-badge-{code}`) remain at `x = MARGIN.left + chartW + 4`
and are not moved or obscured by the terminal label addition.

### 3.3 Silent failure detection

**Silent failure — labels present but wrong entity code:**
If `code` is taken from `entityCodes` array but rendered labels use stale or incorrect
codes (e.g., always "entity0"), the visual test still passes (testid present) but the
label is wrong. The QA test must assert that the TEXT CONTENT of
`zone-1a-terminal-label-GRC` contains "GRC" (or the entity code matches the testid key).

**Silent failure — labels outside chart bounds:**
If the SVG `overflow: visible` is not set on `CompositeChartSVG`'s SVG element,
terminal labels positioned at `x = MARGIN.left + chartW + 3` may be clipped. The
SVG root element already has `overflow: visible` (line 390 — `style={{ display: "block", overflow: "visible" }}`).
Verify this persists after the edit.

---

## 4. Acceptance Criteria

**AC-1249-1 (primary — terminal labels present):**
In COMPARE_VIEW with two entities active (GRC and ZMB), at 1280×800 viewport, both
`data-testid="zone-1a-terminal-label-GRC"` and `data-testid="zone-1a-terminal-label-ZMB"`
are visible without scroll. Each element contains the matching entity code as text.

**AC-1249-2 (interaction-free — no hover required):**
The terminal labels in AC-1249-1 are visible WITHOUT triggering any hover, click, or
tooltip interaction. They are present at page load in compare mode.

**AC-1249-3 (N=3 guard — three curves remain distinguishable):**
With a hypothetical three-entity scenario (or the QA test mocking three entity
trajectories), `data-testid="zone-1a-terminal-label-GRC"`,
`data-testid="zone-1a-terminal-label-ZMB"`, and `data-testid="zone-1a-terminal-label-JOR"`
are all visible and contain their respective entity codes. (If a three-entity scenario
is not available in the Playwright session, this AC is validated by the implementing
agent's Step 4 Verify — not an E2E assertion.)

**AC-1249-R (regression — N=1 recharts path unaffected):**
In a single-entity scenario (N=1 Mode 1), NO `zone-1a-terminal-label-*` testids exist
in the DOM. The recharts Legend remains the sole labeling mechanism.

---

## 5. Kryptonite Constraint Check

**Does this implementation's primary observable state require specialist mediation for
Persona 1 to act on it in the Reactive entry state?**

`[x]` **No.** A short text label ("ZMB", "GRC") directly at the curve endpoint is
self-interpreting. No legend, no tooltip, no specialist explanation needed. The label
is visible at glance level at 1280×800.

---

## 6. Out of Scope

**N=3 scenario comparison implementation (G2 Phase 3):** #1249 implements the terminal
label infrastructure for entity codes. G2 Phase 3 passes scenario labels ("A", "B", "C")
through the same entity code slot. G4 does NOT implement the scenario comparison logic
itself.

**Recharts single-entity path terminal labels:** The recharts Legend already serves the
N=1 case. No terminal labels are added to the recharts path. Framework curve identifiability
(FIN, HDI, ECO, GOV) in N=1 Mode 1/2 is served by the Legend — this is not a DEMO6
finding.

**entity-labels-overlay removal:** The existing corner overlay is not removed in this fix.
It may be cleaned up in G2 Phase 3 once scenario labels replace entity codes.

---

## 7. Test Authorship Obligation

**QA Lead:** QA Lead Agent

**Test file:** `frontend/tests/e2e/m17-g4-demo6-critical-polish.spec.ts` — `#1249` describe block

**Implementation completeness check (Step 4 Verify):**
After the implementation PR is opened, the implementing agent confirms:
- `CompositeChartSVG` in `TrajectoryView.tsx` renders a `<text>` element with
  `data-testid={`zone-1a-terminal-label-${code}`}` for each entity code
- The label is positioned at `(xScale(lastStep.step_index) + 3, yScale(lastScore) - 7)`
- `SVG overflow: visible` is confirmed on the SVG root element (prevents clipping)
- N=3 visual compatibility is confirmed (no overlap or layout break with three labels)

**No soft-skip patterns** (NM-056 guard): All ACs must be hard-fail assertions.

---

*Intent document authority: `docs/process/intent-template.md`.
Sprint entry: `docs/process/sprint-plans/m17-g4-sprint-entry.md` (EL Approved 2026-06-25).
UX visual spec: `docs/ux/specs/m17-g4-1249-zone-1a-curve-identifiability.md`.
Issue in scope: #1249 (Zone 1A curve identifiability).
Pre-push gate: `cd frontend && npm run build` — must exit 0 before pushing.*
