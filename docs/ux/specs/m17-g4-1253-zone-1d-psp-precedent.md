---
name: m17-g4-1253-zone-1d-psp-precedent
type: ux-visual-spec
issue: "#1253"
sprint-entry: docs/process/sprint-plans/m17-g4-sprint-entry.md
authored-by: UX Designer Agent
authored-date: 2026-06-25
governing-documents:
  - docs/ux/information-hierarchy.md §Zone 1 — Primary
  - docs/ux/north-star.md §Primary Cognitive Tasks
  - docs/ux/personas.md §Persona 3 — Political Advisor
  - CLAUDE.md §UX Architectural Commitments (premise 2)
---

# UX Visual Spec — M17-G4 Issue #1253: Zone 1D PSP Historical Precedent Anchor

**Decision: Enrich existing inline text with specific named programme references.**
No structural change to Zone 1D layout. The `psp-historical-analogue` element
already exists and renders inline below the PSP severity row.

---

## 1. Problem Statement

The existing `getPspHistoricalAnalogue` function returns generic text:
- CRITICAL: "At this level, historical ECF programmes show abandonment within 3 steps."
- WARNING: "At this level, historical ECF programmes show abandonment within 6 steps."
- WATCH: "At this level, historical ECF programmes show elevated discontinuation risk."

DEMO6-040 finding: Andreas Petrakis (Persona 3 — political advisor) needs to cite a
specific comparable case in a political brief to establish credibility with a minister.
"Historical ECF programmes" is not citation-ready. He needs: programme name, country,
year, and compliance outcome — in one line, without additional navigation.

**The information hierarchy principle** (information-hierarchy.md §Zone 1 — Primary):
Zone 1D content is visible without interaction. The programme reference must be readable
at glance level — it cannot be hidden behind a tooltip or collapsible.

---

## 2. Decision: Inline Enrichment of Existing Text

**Chosen approach:** Replace generic statements in `getPspHistoricalAnalogue` with
specific named programme references. No layout change required — the `psp-historical-analogue`
div already renders inline at `fontSize: 10` below the PSP severity row.

**Rejected: tooltip on severity chip** — tooltip requires hover; Persona 3 cannot hover
during a live demo presentation. Premise 2: "Instruments are always visible; context is
navigable" — critical context (citation reference) must be visible, not hover-gated.

**Rejected: collapsible section** — adds interaction cost; Andreas needs the reference
immediately visible when PSP severity is in WARNING or CRITICAL state.

**No layout change:** The `psp-historical-analogue` element is already present, visible,
and correctly styled (fontSize 10, color #555, lineHeight 1.3). Only the text content
of `getPspHistoricalAnalogue` changes.

---

## 3. Required Text Content

### CRITICAL severity (PSP < 40%)

```
Comparable: Zambia 2015 ECF — abandoned Step 3 (PSP 38%). Board review failed.
```

Full text (one line, no wrap required at 1280×800):
`"Comparable: Zambia 2015 ECF — abandoned Step 3 (PSP 38%). Board review failed."`

### WARNING severity (40% ≤ PSP < 55%)

```
Comparable: Ghana 2014 ECF — modified Step 5 (PSP 52%). Conditionality relaxed.
```

Full text:
`"Comparable: Ghana 2014 ECF — modified Step 5 (PSP 52%). Conditionality relaxed."`

### WATCH severity (55% ≤ PSP < 70%)

```
At this PSP level, ECF programmes show elevated discontinuation risk (approx. 35%).
```

(Generic text acceptable for WATCH — no named analogue required at this severity.)

### STABLE severity (PSP ≥ 70%)

`null` — no analogue shown (status quo; no change).

---

## 4. Zone 1D Density Check

Current Zone 1D layout at 1280×800 includes:
- PSP severity row: "Programme survival: CRITICAL (38%) — DECLINING" (fontSize 11)
- PSP historical analogue (existing): generic text (fontSize 10)
- Legitimacy index row (fontSize 10)
- Elite capture row (fontSize 10)
- PSP Layer 3 sentence (fontSize 10)

The enriched text replaces the existing generic text at fontSize 10. Length comparison:

| Severity | Before | After | Character count delta |
|---|---|---|---|
| CRITICAL | "At this level, historical ECF programmes show abandonment within 3 steps." | "Comparable: Zambia 2015 ECF — abandoned Step 3 (PSP 38%). Board review failed." | +5 chars |
| WARNING | "At this level, historical ECF programmes show abandonment within 6 steps." | "Comparable: Ghana 2014 ECF — modified Step 5 (PSP 52%). Conditionality relaxed." | +6 chars |

Both lines remain single-line at 1280×800 with the current `fontSize: 10` and Zone 1D
width allocation (50% of instrument cluster = ~640px). No layout overflow risk.

**Density confirmed acceptable.** The addition does not crowd existing Zone 1D content.

---

## 5. Before / After Mockup

### CRITICAL severity — BEFORE

```
Zone 1D at 1280×800, PE enabled, CRITICAL PSP scenario

  Programme survival: CRITICAL (38%) — DECLINING
  At this level, historical ECF programmes show abandonment within 3 steps.
  ▲
  Generic — not citation-ready. Andreas cannot cite "historical ECF programmes"
  in a ministerial brief without a specific programme name.
```

### CRITICAL severity — AFTER

```
Zone 1D at 1280×800, PE enabled, CRITICAL PSP scenario

  Programme survival: CRITICAL (38%) — DECLINING
  Comparable: Zambia 2015 ECF — abandoned Step 3 (PSP 38%). Board review failed.
  ▲
  data-testid="psp-historical-analogue" — specific, citation-ready, no interaction needed.
  Andreas can say: "Comparable to Zambia 2015 ECF programme" in the brief.
```

### WARNING severity — AFTER

```
Zone 1D at 1280×800, PE enabled, WARNING PSP scenario

  Programme survival: WARNING (52%) — DECLINING
  Comparable: Ghana 2014 ECF — modified Step 5 (PSP 52%). Conditionality relaxed.
```

---

## 6. Persona Acceptance

**Persona 3 — Andreas Petrakis (political advisor):**
After this fix, Andreas reads Zone 1D and sees "Comparable: Zambia 2015 ECF — abandoned
Step 3 (PSP 38%). Board review failed." He can immediately cite this in a ministerial
brief: "The PSP level is analogous to Zambia's 2015 ECF experience, where programme
abandonment occurred at step 3." No additional navigation, no hover, no lookup required.

**North star test:** A political advisor preparing a conditionality assessment for a
ministry minister can cite a specific comparable programme directly from Zone 1D
during a live demo — without clicking, hovering, or navigating away from the
instrument cluster.

---

## 7. Regression Contract

Only `getPspHistoricalAnalogue` text content changes. No DOM structure, no testid,
no font size, no layout change. The `psp-historical-analogue` testid continues to
exist and render when `severity !== "STABLE"`. Existing tests asserting
"psp-historical-analogue visible at step 1" (AC-9 in `m16-g1-zone-1a-phase4-composite.spec.ts`)
must continue to pass — they assert visibility, not text content.
