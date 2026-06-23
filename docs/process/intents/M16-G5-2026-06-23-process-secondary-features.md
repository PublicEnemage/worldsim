---
name: M16-G5-process-secondary-features
type: implementation-intent
issues: "#1145, #837, #951, #259"
status: Filed
authored-by: "PM Agent (#837); PI Agent (#951); Technical Standards Agent (#259); #1145 is EL-authored and self-reviewed"
authored-date: 2026-06-23
implementing-agents: "EL (#1145); PM Agent (#837); PI Agent (#951); Technical Standards Agent (#259)"
sprint-entry: "docs/process/sprint-plans/m16-g5-sprint-entry.md — EL approval pending"
adr-reference: "No ADR gate — all G5 items are documentation, process, or tooling changes within accepted ADR scope"
release-branch: release/m16
note: "Sprint entry §2.3 waives the intent document requirement for this infrastructure sprint. This document is filed at EL request to formalise the acceptance criteria and test authorship obligation before implementation begins."
---

# Implementation Intent: M16-G5 — Process + Secondary Features

## 1. Source Reference

**Sprint entry:** `docs/process/sprint-plans/m16-g5-sprint-entry.md` — awaiting EL approval
**ADR gate:** None — all G5 items are documentation, process, or tooling changes; no new application surface
**Date authored:** 2026-06-23
**Authored by:** PM Agent (#837) + PI Agent (#951) + Technical Standards Agent (#259); #1145 is EL-authored and self-reviewed
**Implementing agents:**
- EL — #1145 (founding document addition; EL-authored, EL self-reviewed)
- PM Agent — #837 (configuration-driven demo scripts)
- PI Agent — #951 (solo-use review protocol)
- Technical Standards Agent — #259 (CTO legibility metrics dashboard)

**Issues in scope:**

| Issue | Title | Priority | Implementing agent |
|---|---|---|---|
| #1145 | docs(founding): add AC-001 and AC-002 as explicit permanent constraints in founding document | immediate / HIGH — EL-action | EL |
| #837 | feat(demo): configuration-driven demo scripts | near-term / MEDIUM | PM Agent |
| #951 | process: solo-use review protocol | near-term / MEDIUM | PI Agent |
| #259 | standards: CTO legibility metrics dashboard | near-term / LOW | Technical Standards Agent |

---

## 2. Persona Trace Elements Targeted

> *G5 is an infrastructure sprint with no user-facing deliverables in the UX persona sense. Persona trace is forward-facing — each issue traces to the persona it protects or unblocks, not to a direct user interaction.*

**P-1 — Personas served:**
- **Forward trace — #1145 (founding document):** All personas. AC-001 makes the open-access constraint explicit: private, proprietary, or ministry-owned data inputs are architecturally prohibited. Without this constraint written down, a future contributor could reasonably introduce a proprietary data dependency that removes the tool from the reach of the actors it exists to serve. Persona 2 (Eleni — Finance Ministry Negotiator) and Persona 3 (Pita — Parliamentary Research Fellow) depend on the tool remaining accessible and its methodology remaining inspectable — both are directly protected by this constraint being permanent.
- **Forward trace — #837 (configuration-driven demo scripts):** Demo audience = Persona 1 (Lucas — Non-specialist Observer) and real external stakeholders attending the G8 live demo (#843). A PM Agent running a new milestone's demo cannot currently switch demo cycles without editing demo script source directly — a process error in that edit would surface to real participants. Configuration-driven parameterisation eliminates that risk and is a forward gate on G8.
- **Forward trace — #951 (solo-use review):** Customer Agent (Persona 1-analog — non-specialist user without specialist mediation) is the designated solo-use reviewer in the Step 6b panel. The solo-use protocol catches CRITICAL and HIGH usability defects that specialist reviewers miss because they apply domain knowledge that real external participants lack. Protects the G8 live demo audience from a DEMO4-001-class failure reaching real participants.
- **Forward trace — #259 (legibility metrics):** All personas, via contributor accessibility. A developer who cannot read the codebase without significant ramp-up time cannot fix bugs or add features that serve any persona. Legibility metrics create a visible quality floor with threshold accountability — a tool built on opaque infrastructure cannot be maintained or audited by the resource-constrained contributors it aims to attract.

**P-2 — Entry state:**
- None of the four issues directly affect the running application's entry state. Forward trace only.

**P-3 — Journey reference:**
- #1145: No journey step — founding document change; permanent constraint made explicit.
- #837: Pre-condition to G8 Journey — demo preparation standard (Step 6b) requires a runnable demo script. Configuration-driven parameterisation is a prerequisite to running a new milestone's demo without source edits.
- #951: Step 6b panel (demo-preparation-standard.md) — solo-use gate is added to the existing Step 6b review protocol.
- #259: No journey step — CI/documentation artifact; milestone exit checklist component.

**P-4 — Time / interaction ceiling:**
- Not applicable — infrastructure sprint with no direct runtime interaction.

**P-7 — North star capability delivered:**
- **#1145:** A contributor reading `docs/vision/worldsim-founding-document.md §Open Source as Strategy` understands that private data inputs are not merely discouraged — they are architecturally prohibited (AC-001), and that synthetic estimates are explicitly permitted under named conditions (AC-002). The founding document is now self-contained on data input architecture; no separate consultation of `docs/architecture/constraints.md` is required to understand the full constraint.
- **#837:** A PM Agent preparing the G8 demo (or any future milestone's demo) runs `scripts/demo.sh --milestone 16` with no in-place content edits to either the script or the Playwright narration spec. The correct milestone's content is derived automatically.
- **#951:** A Step 6b panel reviewer designated as the solo-use reviewer evaluates screenshots before reading the walkthrough — findings are tagged `[SOLO]` and, if CRITICAL or HIGH, block Step 7 under the same criteria as all other findings. A DEMO4-001-class failure (output surfaces to real participants without non-specialist legibility check) cannot pass Step 6b unreported.
- **#259:** The M16 exit checklist includes a legibility section with four Tier 1 threshold values and current-milestone measurements. Future EL or contributor can confirm at a glance whether the codebase is within the green/yellow/red band for cognitive complexity, function length, silent failure surface count, and test-to-implementation ratio.

---

## 3. Observable Application State

> *G5 has no application runtime states. Observable states are document-level (file existence, content presence) and tooling-level (script execution). These are verifiable by an agent other than the implementor using file access and shell execution — no application launch required.*

### 3.1 Primary observable state

**#1145 — AC-001 and AC-002 named as permanent architectural constraints:**

`docs/vision/worldsim-founding-document.md §Open Source as Strategy` (or a clearly labelled subsection within it) contains all of:
1. "AC-001" as a named label — identifying the constraint that private, proprietary, or ministry-owned data inputs are architecturally prohibited, with rationale (reproducibility requires both parties to inspect the same public sources)
2. "AC-002" as a named label — identifying the standing permission for synthetic estimates from comparable economies, regional distributions, and historical patterns, with conditions: mandatory indicator-level disclosure, T3 confidence tier floor, and meaninglessness threshold suppression
3. Both AC-001 and AC-002 characterised as "permanent architectural constraints" (the word "permanent" must appear in proximity to the constraint declarations) — not as guidelines, preferences, or strategic commitments

A contributor reading the founding document can identify and cite both constraints without consulting `docs/architecture/constraints.md`.

### 3.2 Secondary observable states

**Secondary 1 — #837 — Configuration-driven demo scripts:**

`scripts/demo.sh --milestone 16` executes without error (exit code 0) and produces presenter guide output that references M16 demo document content (`docs/demo/m16/stakeholder-walkthrough.md` and `docs/demo/m16/screenshot-brief.md`). Neither `scripts/demo.sh` nor `frontend/tests/e2e/demo-narrated.spec.ts` contains hardcoded M10 Argentina content outside of historical demo directories (`docs/demo/m10/`). `--milestone N` is the sole input required to switch demo cycles; no in-place source edit of either file is required to run a new milestone's demo.

**Secondary 2 — #951 — Solo-use gate in demo-preparation-standard.md §Step 6b:**

`docs/process/demo-preparation-standard.md §Step 6b` (or an added subsection within it) contains a named solo-use gate specifying all of:
1. At least one Step 6b panel reviewer must evaluate screenshots without reading the walkthrough first
2. Findings from this reviewer are tagged `[SOLO]` in the finding format
3. A CRITICAL or HIGH solo-use finding blocks Step 7 under the same three-condition criteria as all other Step 6b findings
4. Customer Agent (Layer 3 usability — non-specialist user without specialist mediation) is the designated solo-use reviewer

**Secondary 3 — #259 — Legibility metrics artifact:**

`docs/standards/legibility-baseline-m16.md` exists and contains the four Tier 1 tolerance thresholds from issue #259 (mean cognitive complexity green/yellow/red bands, p90 function length, silent failure surface count, test-to-implementation ratio) with current-milestone values for each. Tier 2 and Tier 3 metrics are documented as out of scope for M16 with a forward note.

### 3.3 Silent failure detection

**SF-1 (#1145 — constraints appear as notes, not named constraints):** AC-001/AC-002 are added as prose observations or inline asides in the founding document rather than as explicitly named, labelled constraints. A contributor skimming the section would see the principle but not recognise it as an architectural constraint with a stable reference number. Detection: AC-3 asserts "permanent" appears in proximity to the constraint declarations; AC-1 and AC-2 assert the label strings "AC-001" and "AC-002" are present — prose-only additions without labels fail AC-1/AC-2.

**SF-2 (#837 — flag accepted but content still hardcoded):** `scripts/demo.sh` accepts `--milestone N` as an argument but ignores it and still derives content from hardcoded M10 sources. The script exits 0 but the output is M10 Argentina content, not M16 content. Detection: AC-5 asserts M10/Argentina strings are absent from both files; AC-4b asserts the output contains a reference derived from M16 documents.

**SF-3 (#951 — solo-use gate present but Customer Agent not named):** The solo-use gate section is added to the document and defines the `[SOLO]` tag, but omits the Customer Agent designation — leaving the solo-use reviewer role unoccupied. In practice, no agent knows they hold the solo-use responsibility. Detection: AC-8 asserts "Customer Agent" appears in the §Step 6b context.

**SF-4 (#259 — threshold table present but values are blank placeholders):** `docs/standards/legibility-baseline-m16.md` is created with the four Tier 1 threshold labels but the current-milestone value cells are blank, left as `TBD`, or contain only the threshold band (no measured value). The file exists and looks correct but provides no actual measurement. Detection: AC-9 asserts current-milestone values are present alongside thresholds.

---

## 4. Acceptance Criteria

> *All ACs are document-level or script-execution checks. No Playwright E2E tests — G5 has no application runtime states. All ACs are backend pytest (file existence, content presence, subprocess execution).*

**AC-1 (#1145):** `grep -c "AC-001" docs/vision/worldsim-founding-document.md` returns ≥1 — confirming AC-001 is explicitly named as a labelled constraint in the founding document.

**AC-2 (#1145):** `grep -c "AC-002" docs/vision/worldsim-founding-document.md` returns ≥1 — confirming AC-002 is explicitly named as a labelled constraint in the founding document.

**AC-3 (#1145):** `grep -c "permanent" docs/vision/worldsim-founding-document.md` returns ≥1 in the §Open Source as Strategy section — confirming both constraints are characterised as permanent architectural constraints rather than guidelines or strategic commitments.

**AC-4 (#837):** `bash scripts/demo.sh --milestone 16` exits 0 — confirming the script accepts the `--milestone` parameter and runs without error for milestone 16.

**AC-4b (#837):** The stdout of `scripts/demo.sh --milestone 16` contains at least one reference to M16 demo document content (e.g., a string derived from `docs/demo/m16/stakeholder-walkthrough.md` or `docs/demo/m16/screenshot-brief.md`) — confirming content derivation is milestone-specific, not hardcoded from M10.

**AC-5 (#837):** `grep -ci "argentina" scripts/demo.sh` returns 0 AND `grep -ci "argentina" frontend/tests/e2e/demo-narrated.spec.ts` returns 0 — confirming hardcoded M10 Argentina content is absent from both script files. (Historical demo directory content under `docs/demo/m10/` is excluded from this check.)

**AC-6 (#951):** `grep -ci "solo.use\|solo use" docs/process/demo-preparation-standard.md` returns ≥1 — confirming a named solo-use gate is present in the document.

**AC-7 (#951):** `grep -c "\[SOLO\]" docs/process/demo-preparation-standard.md` returns ≥1 — confirming the `[SOLO]` tag convention for solo-use reviewer findings is defined.

**AC-8 (#951):** `grep -c "Customer Agent" docs/process/demo-preparation-standard.md` returns ≥1 in the §Step 6b context — confirming the Customer Agent is designated as the solo-use reviewer, not left as an anonymous "reviewer" role.

**AC-9 (#259):** `find docs/standards -name "legibility-baseline-m16.md"` exits 0 — confirming the legibility metrics artifact exists. `grep -ci "cognitive complexity" docs/standards/legibility-baseline-m16.md` returns ≥1 AND `grep -ci "function length" docs/standards/legibility-baseline-m16.md` returns ≥1 AND `grep -ci "test-to-implementation" docs/standards/legibility-baseline-m16.md` returns ≥1 — confirming at minimum three of four Tier 1 threshold labels are documented. The file contains at least one numeric value per threshold (not a blank or `TBD` placeholder) — confirming current-milestone measurements are recorded alongside the threshold bands.

---

## 4b. Visual Spec (before/after)

N/A — all ACs are document-level or script-execution checks with no text display, label format, or layout in the running application. No Playwright-testable application states are involved.

---

## 5. Kryptonite Constraint Check

> *Authority: docs/process/agent-execution-lifecycle.md — Kryptonite Design Constraint (FD-3).*

**Does this implementation's primary observable state require specialist mediation for Persona 2 to act on it in the Reactive entry state (90-second ceiling)?**

`[x]` N/A — infrastructure sprint. None of the four issues introduce or modify a user-facing analytical output in the running application. The kryptonite constraint applies at Step 1 to implementations that surface outputs to Persona 2 in the Reactive entry state. G5 outputs are documents, scripts, and process rules — not runtime instrument outputs. Constraint check is not required.

**Forward kryptonite note:** #837 and #951 protect the G8 live demo from surfacing un-mediated content to real external participants. By ensuring demo scripts are configuration-driven and the solo-use review is structurally enforced, G5 closes two pathways by which a kryptonite failure (output requiring specialist mediation reaching a non-specialist) could reach Persona 1 during the G8 external demo. This is a kryptonite-protective function, not a kryptonite-triggering one.

---

## 6. Out of Scope

1. **Full AC-001/AC-002 cross-document consistency sweep** — #1145 is bounded to adding the explicit constraint labels to `docs/vision/worldsim-founding-document.md §Open Source as Strategy`. A comprehensive audit of all downstream documents (`docs/DATA_STANDARDS.md`, `docs/architecture/constraints.md`, `docs/adr/`) for AC-001/AC-002 consistency is a separate initiative, not in G5 scope.

2. **#837 Phase 2 automation — structured `demo-config.yml` generation tooling** — G5 scope is CLI parameterisation (`--milestone N`) and content derivation from existing walkthrough and screenshot-brief documents. YAML generation tooling and fully automated demo pipeline construction are a future phase if #837 is extended.

3. **#259 Tier 2/3 metrics** — Blind audit mean score and assumption documentation rate are semi-automated and qualitative; not CI-computable for M16. These are recorded in the legibility baseline as qualitative / future work with no current-milestone values required.

4. **Any frontend or backend application component changes** — G5 contains no application code changes. `frontend/tests/e2e/demo-narrated.spec.ts` is demo tooling, not an application component; changes to it under #837 are in scope only to remove hardcoded M10 content.

5. **Playwright E2E tests** — G5 has no application runtime states. No Playwright tests are required or expected. All tests are backend pytest (file existence, content presence, subprocess execution).

6. **#843 live stakeholder demo execution** — G5 is a prerequisite enabler for G8, not G8 itself. G5 delivers the demo tooling and review protocol improvements; G8 delivers the live demo.

---

## 7. Test Authorship Obligation

> *The QA Lead is notified before implementation begins. Tests are authored before the implementing agent opens any G5 PR.*

**QA Lead:** QA Lead Agent
**Test authorship deadline:** Before any G5 implementation PR is opened
**Test file location:** `backend/tests/test_m16_g5_process_secondary_features.py` — AC-1 through AC-9 (document existence, content presence, subprocess execution)
**No Playwright E2E file required:** G5 has no application runtime states.

**AC assignment summary:**

| AC | Issue | Check type | Authored before implementation? |
|---|---|---|---|
| AC-1 | #1145 — AC-001 named in founding document | grep count | No — BLOCKING |
| AC-2 | #1145 — AC-002 named in founding document | grep count | No — BLOCKING |
| AC-3 | #1145 — "permanent" characterises both constraints | grep count in section | No — BLOCKING |
| AC-4 | #837 — `--milestone 16` exits 0 | subprocess.run exit code | No — BLOCKING |
| AC-4b | #837 — output references M16 content | subprocess.run stdout check | No — BLOCKING |
| AC-5 | #837 — no Argentina/M10 in scripts | grep count (expect 0) | No — BLOCKING |
| AC-6 | #951 — solo-use gate named | grep count | No — BLOCKING |
| AC-7 | #951 — `[SOLO]` tag defined | grep count | No — BLOCKING |
| AC-8 | #951 — Customer Agent designated | grep count in context | No — BLOCKING |
| AC-9 | #259 — legibility file exists with thresholds + values | find + grep count | No — BLOCKING |

**QA Lead acknowledgment:**
`[x]` QA Lead: Tests for AC-1 through AC-9 authored and filed. 2026-06-23 — `backend/tests/test_m16_g5_process_secondary_features.py`

---

*Intent document filed 2026-06-23. Authored by: PM Agent (#837), PI Agent (#951), Technical Standards Agent (#259); #1145 is EL-authored and self-reviewed by EL before PR opens. QA Lead files test file before any G5 implementation PR opens — this is a hard gate. Authority: `docs/process/agent-execution-lifecycle.md`. Template: `docs/process/intent-template.md` (version 2026-06-17). Sprint entry §2.3 waives the formal intent document requirement for this infrastructure sprint; this document is filed at EL request to formalise acceptance criteria before implementation begins.*
