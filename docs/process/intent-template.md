---
name: intent-template
type: template
version: 2026-06-12
phase: Phase A — Agent Execution Lifecycle
canonical-authority: This template is the canonical Implementation Intent authorship reference from Phase A onward.
prerequisite-sources:
  - docs/adr/template.md
  - docs/process/sprint-plans/process-redesign-phaseA-sprint-entry.md
  - docs/process/agents.md §Architect Agent
  - docs/process/agents.md §QA Lead Agent
---

# Implementation Intent Template — WorldSim

> **How to use this template:**
> Copy this file to `docs/process/intents/M{N}-{G-suffix-or-ADR-NNN}-{YYYY-MM-DD}-{short-name}.md` before
> implementation begins. The intent document is the contract the implementation must satisfy
> and the specification the QA Lead writes tests from.
>
> **Who authors it:** The implementing agent named in the ADR panel (Architect Agent for backend
> modules; Frontend Architect Agent for frontend features). The authoring agent may not be the
> same session that writes the tests — the QA Lead authors tests independently.
>
> **When it is authored:** After the ADR is accepted; before any implementation PR is opened
> and before any implementation code is written for this feature.
>
> **Completeness test:** The QA Lead must be able to write a Playwright or pytest test from
> Section 3 (Observable Application State) without reading any implementation code. If the
> QA Lead cannot write a test from this document alone, the document is incomplete.
>
> **Distinct from Intent Blocks:** This document is a pre-implementation feature specification.
> Intent Blocks (`docs/process/intent-block-author-prompt.md`) are post-implementation,
> function-level documentation for divergence detection. These are different artifacts.

---

# Implementation Intent: ADR-NNN — [Short Name]

## 1. Source ADR

**ADR:** ADR-NNN — [title]
**Status at time of authorship:** Accepted
**Authored by:** [Agent name]
**Date:** [YYYY-MM-DD]
**Implementing agent:** [Agent name or role — must match ADR panel]

---

## 2. Persona Trace Elements Targeted

> *Derived directly from the ADR's §Persona and UX Traceability section.
> Copy the relevant elements. If the ADR is Tier 3, state which Tier 1/Tier 2 ADR this
> infrastructure eventually serves, and leave remaining elements blank with "N/A — Tier 3."*

**P-1 — Persona served:** [Persona name and number from the ADR]

**P-2 — Entry state:** [Entry state and time ceiling from the ADR]

**P-3 — Journey step:** [Journey reference from the ADR — Journey Letter + Step Number]

**P-4 — Time/interaction ceiling:** [Maximum time or interaction count from the ADR]

**P-6 — Negotiating leverage delivered** *(if Persona 2):*
[Copy the P-6 statement from the ADR verbatim. If this implementation only partially delivers
P-6, state which part it delivers and which part remains for a subsequent implementation.]

**P-7 — North star capability delivered:**
[In one sentence: what can the finance minister or her specialist now do that they could not
before this implementation? Must match the ADR's P-7 or explicitly name which part of P-7
this implementation delivers and what is deferred.]

---

## 3. Observable Application State

> *The single most important section. This defines what "done" means.
> Every statement must be verifiable by an external observer using only the running application —
> no source code reading, no test reports, no implementation knowledge.*
>
> **The test for each statement:** Can a QA reviewer with no knowledge of this implementation
> confirm this state by opening the application and observing? If the answer is no, the
> statement is not an observable application state — it is an implementation assumption.
>
> **Bad:** "The fiscal multiplier is correctly propagated."
> **Bad:** "CI passes."
> **Bad:** "The function returns the correct result."
>
> **Good:** "At step 3 of the Jordan/Egypt Hormuz scenario with fiscal_multiplier=1.30,
> Zone 1A's PMM instrument displays the value 1.30 (not 1.00)."
> **Good:** "Zone 1B shows the top MDA alert text without requiring scroll at 1440×900,
> with the Greece 2012 fixture scenario loaded at step 4."
> **Good:** "GET /api/v1/scenarios/{id}/trajectory returns reserve_coverage_months as a
> non-null float for all steps when the Jordan entity is loaded."

### 3.1 Primary observable state

[The core user-visible outcome. What is present in the running application after implementation
that was absent before? Name the scenario context, the viewport, the zone, and the specific
value or element expected.]

### 3.2 Secondary observable states

[Additional observable states, if any. Maximum three. If more are required, consider whether
the scope exceeds one intent document — split if so.]

### 3.3 Silent failure detection

[What does the application show or return when this capability appears to work but the underlying
data, event, or computation is absent? Derived from the ADR's §Silent Failure Mode. A QA
reviewer needs to distinguish genuine output from a silent failure — name the distinguishing
observable characteristic.]

---

## 4. Acceptance Criteria

> *Each criterion is derived from Section 3. Each must reference the observable application
> state it verifies. Write in a form that a Playwright test or pytest fixture can directly
> implement — naming the scenario, the action, and the expected observable output.*
>
> *Format:*
> **AC-N:** In [scenario context, fixture, or entry state], when [user action or system condition],
> then [specific observable outcome — element text, field value, timing, zone presence].
>
> *These criteria are what the QA Lead authors tests from, before implementation begins.
> A criterion the QA Lead cannot test without reading the implementation is invalid.*

**AC-1:** In [scenario], when [condition], then [observable outcome].

**AC-2:** In [scenario], when [condition], then [observable outcome].

[Add criteria as needed. One criterion per observable state plus one for silent failure detection.]

---

## 4b. Visual Spec (before/after)

> *Required when: any AC in Section 4 involves text display, label format, layout, or visual
> hierarchy — i.e., when the observable state is a string value, element appearance, or
> spatial arrangement that a QA reviewer must match exactly.*
>
> *Optional when: all ACs are backend-only (API responses, database state, computation outputs)
> with no text-display component.*
>
> *What to provide:* For each display-format AC, show:
> - **Before** — the current broken or absent state (screenshot, annotated text block, or
>   wireframe excerpt). Label what is wrong: which string is raw, which element is absent,
>   which layout is violated.
> - **After** — the intended fixed state. Label what "done" looks like: the exact string
>   the option must display, the exact zone the element must occupy, the exact label format.
>
> *Minimum fields for each AC block:* viewport (e.g., `1440×900`), the specific zone
> (`Zone 1B`, `Zone 1A`, etc.), and at least one `data-testid` selector that a Playwright
> test can target. A visual spec without a `data-testid` anchor cannot be tested from the
> intent document alone — the QA Lead will be forced to read implementation source code,
> which violates the Step 2 independence requirement.
>
> *Why this exists:* Prose descriptions of text display states have an inherent scope ambiguity —
> "no underscore in option text" does not distinguish label portion from unit metadata. A
> before/after visual eliminates that ambiguity without requiring the QA Lead to read source
> code. Authority: insights log entry 2026-06-17; M14-G1 AC-6 incident; #1004.
>
> *Format:* Inline fenced text blocks are sufficient when screenshots are unavailable. Mark
> the bug location explicitly (e.g., `^^^^ THIS IS THE BUG`). A marked-up text block is
> better than prose; a screenshot is better than a text block.

**AC-N (before):**
```
Viewport: 1440×900 | Zone: [Zone ID] | data-testid="[testid-of-element]"
[Paste current broken output here. Annotate the specific wrong string or missing element.]
```

**AC-N (after):**
```
Viewport: 1440×900 | Zone: [Zone ID] | data-testid="[testid-of-element]"
[Paste intended fixed output here. Annotate the specific correct string or present element.]
```

[Repeat for each display-format AC. Leave this section blank with "N/A — backend only" if
no AC involves text display, label format, or layout.]

---

## 5. Kryptonite Constraint Check

> *Authority: CLAUDE.md §Agent Execution Lifecycle — Kryptonite Design Constraint (FD-3).
> Required for any implementation that introduces or modifies a user-facing analytical output.
> An intent document with this section unchecked is incomplete and blocks test authorship.*

**Does this implementation's primary observable state require specialist mediation for Persona 2
to act on it in the Reactive entry state (90-second ceiling)?**

`[ ]` No — the observable state is interpretable by Persona 2 without an analyst translating it.

`[ ]` Yes — [describe the required mediation and provide EL exception reference, or revise the
observable state until the answer is No].

---

## 6. Out of Scope

> *Explicit scope boundaries prevent implementation drift and make the Verify step tractable.
> Name at least one item that is NOT included in this implementation, however adjacent it is.*

[State at least one out-of-scope concern. "Nothing is out of scope" means scope has not been
bounded — this section cannot be left empty or marked N/A.]

---

## 7. Test Authorship Obligation

> *The QA Lead is notified before implementation begins. Tests are written before the
> implementation PR is opened — not alongside it, not after it.*

**QA Lead:** [Agent name — typically QA Lead Agent]
**Test authorship deadline:** Before any implementation PR is opened
**Test file location:** [Playwright E2E: `frontend/tests/e2e/m{N}-g{N}-{short-name}.spec.ts`
Backend pytest: `backend/tests/test_m{N}_g{N}_{short_name}.py`]
**Relevant ADR acceptance criteria:** [Reference AC-1 through AC-N from Section 4 above]

**QA Lead acknowledgment:**
`[ ]` QA Lead: Tests for AC-1 through AC-N authored and filed. [Date]

---

*Template version: 2026-06-17. Phase A encoded; §4b Visual Spec added (#1004). Authoring
authority: `docs/process/agents.md §Architect Agent`. The intent document is the contract;
the implementation is the execution. A discrepancy between them is a Verify-step failure —
not a document-update opportunity. For the full lifecycle this template feeds into, see
`CLAUDE.md §Agent Execution Lifecycle`.*
