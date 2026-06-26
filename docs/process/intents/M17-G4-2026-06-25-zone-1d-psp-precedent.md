---
name: M17-G4-zone-1d-psp-precedent
type: implementation-intent
issues: "#1253"
status: Step 1 authored — QA tests may be authored; implementation begins after #1249 merges
authored-by: Frontend Architect Agent
authored-date: 2026-06-25
implementing-agent: Frontend Engineer
sprint-entry: "docs/process/sprint-plans/m17-g4-sprint-entry.md — EL Approved 2026-06-25"
ux-visual-spec: "docs/ux/specs/m17-g4-1253-zone-1d-psp-precedent.md"
adr-reference: "N/A — content addition within ADR-017 Zone 1D boundary; no architectural decision required"
release-branch: release/m17
---

# Implementation Intent: M17-G4 — Zone 1D PSP Historical Precedent Anchor (#1253)

> **UX visual spec governs.** All observable state requirements are derived from
> `docs/ux/specs/m17-g4-1253-zone-1d-psp-precedent.md`.
>
> **FA implementation sequence:** #1253 is the 2nd issue in FA sequence
> (#1249 → #1253 → #1250 → #1239). Implementation PR opens after #1249 merges.

---

## 1. Source

**Issue:** #1253 — ux(zone-1d): DEMO6-040 PSP historical precedent anchor

**Root cause:** `getPspHistoricalAnalogue(severity: PspSeverity)` in
`FourFrameworkZone1D.tsx` (line 155) returns generic text for CRITICAL and WARNING
severities:
- CRITICAL: `"At this level, historical ECF programmes show abandonment within 3 steps."`
- WARNING: `"At this level, historical ECF programmes show abandonment within 6 steps."`

This text is rendered correctly in the existing `psp-historical-analogue` element (lines
499–506, `fontSize: 10, color: #555`). The rendering infrastructure is complete.

**The gap:** The text lacks a specific programme name, country, year, and compliance
outcome. Persona 3 (Andreas Petrakis — political advisor) needs to cite a specific
comparable case in a ministerial brief. "Historical ECF programmes" is not citation-ready.

**The fix:** Update the return values in `getPspHistoricalAnalogue` to include named
programme references per `docs/ux/specs/m17-g4-1253-zone-1d-psp-precedent.md §3`.

**Scope constraint:** This is a one-function text change. No DOM structure, no testid,
no layout, no rendering logic changes. Only the return values of `getPspHistoricalAnalogue`
are modified.

---

## 2. Required Text Values

```typescript
function getPspHistoricalAnalogue(severity: PspSeverity): string | null {
  if (severity === "CRITICAL")
    return "Comparable: Zambia 2015 ECF — abandoned Step 3 (PSP 38%). Board review failed.";
  if (severity === "WARNING")
    return "Comparable: Ghana 2014 ECF — modified Step 5 (PSP 52%). Conditionality relaxed.";
  if (severity === "WATCH")
    return "At this PSP level, ECF programmes show elevated discontinuation risk (approx. 35%).";
  return null;
}
```

These values are binding. The QA test asserts the exact text (or a substring) for each
severity. Any deviation from this spec requires a UX visual spec revision, not an
implementation judgement call.

---

## 3. Persona Trace Elements Targeted

**P-1 — Persona served:** **Persona 3 — Andreas Petrakis (Political Advisor)**
(`docs/ux/personas.md §Persona 3`). Zone 1D PSP severity row with historical analogue is
the governance intelligence instrument. Andreas uses PSP severity to assess programme
survival risk; the historical analogue is the citation he uses in a ministerial brief
to establish credibility.

Secondary: **Persona 2 — Aicha Mbaye (Finance Ministry Negotiator)** who presents
the PSP context to a minister during a conditionality negotiation.

**P-4 — Time/interaction ceiling:** 90 seconds (Reactive). The analogue must be readable
inline without hover or click.

**P-7 — North star capability delivered:**
After this fix, a political advisor reading Zone 1D in a CRITICAL PSP scenario can
immediately state: "This is comparable to Zambia's 2015 ECF programme — which was
abandoned at Step 3 following a board review failure." The citation is on-screen and
requires no additional navigation. This is the cite-in-brief capability the demo
needs to demonstrate.

---

## 4. Observable Application State

### 4.1 Primary observable state

Zone 1D with PE enabled, in a scenario where PSP severity is CRITICAL:

The element at `data-testid="psp-historical-analogue"` is visible (no scroll required)
and contains the text "Zambia 2015 ECF" AND "abandoned".

For WARNING severity: the element contains "Ghana 2014 ECF" AND "modified".

For STABLE severity: `psp-historical-analogue` is NOT present in the DOM (null return
value — no element rendered per the existing `{analogue && ...}` conditional).

### 4.2 Silent failure detection

**Silent failure — text updated but element not visible:**
If `psp-historical-analogue` is present in the DOM but not visible (e.g., overflow
hidden by Zone 1D container), the QA test passes but the user cannot read it.
The QA assertion must use `.toBeVisible()` not just `.toBeAttached()`.

**Silent failure — existing test AC-9 regression:**
`m16-g1-zone-1a-phase4-composite.spec.ts:1026:3` (`AC-9: psp-historical-analogue visible
at L0 (no interaction) at step 1; contains historical risk language`) uses
`.toContainText` with a broad assertion. The updated text still contains "historical" in
the WATCH case, and "ECF" in the CRITICAL/WARNING case. The existing AC-9 assertion
checks for "historical risk language" — confirm after implementation that AC-9 still
passes with the new CRITICAL text ("Comparable: Zambia 2015 ECF..."). If AC-9's
`toContainText` argument is too specific, update it as part of this PR.

---

## 5. Acceptance Criteria

**AC-1253-1 (CRITICAL severity — named programme reference):**
In a scenario where Zone 1D shows PSP severity CRITICAL, `data-testid="psp-historical-analogue"`
is visible and contains the text `"Zambia 2015 ECF"`.

**AC-1253-2 (WARNING severity — named programme reference):**
In a scenario where Zone 1D shows PSP severity WARNING (PSP 40–55%), 
`data-testid="psp-historical-analogue"` is visible and contains the text `"Ghana 2014 ECF"`.

**AC-1253-3 (STABLE severity — no analogue element):**
In a scenario where PSP severity is STABLE, `data-testid="psp-historical-analogue"`
is NOT present in the DOM (or not visible — consistent with the existing `{analogue && ...}`
conditional rendering when `null` is returned).

**AC-1253-R (regression — existing PSP severity row unaffected):**
The `psp-severity-row` and `psp-severity-badge` testids are present and visible alongside
the updated analogue text. The severity badge text (CRITICAL/WARNING/WATCH/STABLE) is
unchanged.

---

## 6. Kryptonite Constraint Check

`[x]` **No specialist mediation required.** The named programme reference ("Comparable:
Zambia 2015 ECF — abandoned Step 3 (PSP 38%). Board review failed.") is self-interpreting
at glance level. Persona 3 reads it inline and has the citation they need without opening
a drawer, hovering, or navigating away.

---

## 7. Out of Scope

**PSP data source changes:** The PSP comparable programme references are hardcoded in
`getPspHistoricalAnalogue`. This is intentional — the references are methodology
constants (not live data) that the Chief Methodologist validated for the demo scenarios
in scope. A data-driven comparable programme lookup is future work.

**lte threshold direction, entity attribution, other Zone 1D fields:** Unchanged.

---

## 8. Test Authorship Obligation

**Test file:** `frontend/tests/e2e/m17-g4-demo6-critical-polish.spec.ts` — `#1253` describe block

**Existing test regression check:** After implementation, run
`m16-g1-zone-1a-phase4-composite.spec.ts` locally and confirm AC-9 still passes.
If AC-9's `toContainText` assertion uses text that no longer appears in the new CRITICAL
analogue, update AC-9 as part of this PR (the testid is the same; only the content changed).

**No soft-skip patterns** (NM-056 guard): All ACs must be hard-fail assertions.
