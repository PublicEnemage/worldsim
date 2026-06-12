---
name: G4-documentation
type: intent
sprint-group: G4
issues: "#27, #822, #847"
milestone: M13
authored-by: Documentation Agent
authored-date: 2026-06-12
implementing-agent: Documentation Agent
adr-reference: None — methodology transparency and narration fix
---

# Implementation Intent: G4 — Documentation

## 1. Source ADR

**ADR:** None — documentation deliverables. #822 satisfies a confidence tier system
disclosure requirement.
**Status at time of authorship:** N/A
**Authored by:** Documentation Agent
**Date:** 2026-06-12
**Implementing agent:** Documentation Agent

---

## 2. Persona Trace Elements Targeted

**P-1 — Persona served:** Persona 3 — Chief Methodologist / External Reviewer.
A domain expert reviewing WorldSim's methodology documentation for public release.

**P-2 — Entry state:** Exploratory — reviewer reading methodology docs from entry point
(docs/methodology/ or docs/DATA_STANDARDS.md) to evaluate a specific claim.

**P-3 — Journey step:** J-E Step 2 — Navigate from calibration claim to supporting
parameter documentation.

**P-4 — Time/interaction ceiling:** 5 minutes. A non-author reviewer must reach the key
finding from each document's entry point in under 5 minutes.

**P-6 — Negotiating leverage delivered:** N/A — methodology transparency documentation.

**P-7 — North star capability delivered:** A finance ministry analyst reading the Demo 4
walkthrough will understand what "Irreversible" means for the Human Development framework
without needing a presenter to explain it. An external reviewer can trace the propagation
attenuation parameters to their calibration basis without asking the development team.

---

## 3. Observable Application State

### 3.1 Primary observable state

**#847 (DEMO-046 — Irreversible label):** The M13 demo walkthrough narration
(`docs/demo/m13/walkthrough.md` or the equivalent narration artifact) contains a
parenthetical or inline explanation of "Irreversible" that a finance ministry reader
can understand without presenter mediation. Example: "Irreversible (recovery horizon
exceeds the projection window — this capability loss cannot be reversed by any
scenario pathway in this analysis)".

### 3.2 Secondary observable states

**Secondary 1 (#27 — calibration basis):** At least three propagation attenuation
parameter sites in the backend codebase contain a comment referencing either a
calibration source or an explicit placeholder marking the parameter as requiring
calibration. OR a methodology document at `docs/methodology/calibration-basis.md`
exists and covers the top-level attenuation parameters used in the simulation engine.

**Secondary 2 (#822 — ecological composite disclosure):** `docs/DATA_STANDARDS.md`
or the ecological module documentation contains a IA-1 disclosure note explaining
that the ecological composite score denominator changes when the proximity indicator
first activates mid-scenario, and that this shift affects confidence tier assignment.

### 3.3 Silent failure detection

#847 silent failure: The word "Irreversible" appears in the narration but without
context — a reader unfamiliar with the model cannot determine whether "irreversible"
means "permanent" or "outside the projection window." Distinguishing characteristic:
the text "recovery horizon" or "projection window" appears in proximity to any
"Irreversible" label mention.

---

## 4. Acceptance Criteria

**AC-1 (#847):** The demo walkthrough narration file contains the string "Irreversible"
followed (within 100 characters) by a parenthetical or colon-introduced explanation
referencing either recovery horizon or projection window.

**AC-2 (#27):** A calibration basis document exists at `docs/methodology/calibration-basis.md`
with at least 3 named parameters and their calibration source or placeholder notation.
OR: at least 3 Python files under `backend/app/simulation/` contain inline comments
with the string "calibration:" or "calibration basis:".

**AC-3 (#822):** The string "denominator change" or "proximity indicator activation"
appears in either `docs/DATA_STANDARDS.md` or the ecological module's documentation,
adjacent to guidance on IA-1 disclosure and confidence tier impact.

---

## 5. Kryptonite Constraint Check

**Does this implementation's primary observable state require specialist mediation for
Persona 2 to act on it in the Reactive entry state (90-second ceiling)?**

`[x]` No — adding the Irreversible label explanation removes the specialist mediation
requirement. After the fix, the term is interpretable directly in the narration text.

---

## 6. Out of Scope

- Full calibration study or parameter re-estimation.
- ADR-007 (synthetic data framework) — that is a separate ADR, not a G4 deliverable.
- Rewriting the ecological module's composite scoring methodology.
- New data source registrations.

---

## 7. Test Authorship Obligation

**QA Lead:** QA Lead Agent
**Test authorship deadline:** Before G4 implementation PR is opened
**Test file location:** Business PO navigability check (manual) per acceptance-protocol.md §Documentation
**Relevant ADR acceptance criteria:** AC-1 through AC-3

**QA Lead acknowledgment:**
`[x]` QA Lead: Documentation navigability check criteria confirmed. 2026-06-12
