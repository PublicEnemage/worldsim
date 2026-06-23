# Agent Execution Lifecycle

> *Authority: `docs/process/sprint-plans/process-redesign-phaseA-sprint-entry.md`. Changes to this
> document require Architect Agent review and EL endorsement.*

Every agent implementing a feature — regardless of role — operates within a five-step execution
lifecycle from "ADR accepted" to "sprint exit validated." This lifecycle closes the intent-to-
implementation gap that allowed DEMO4-001 and DEMO4-002 to reach a live demo with frozen outputs
despite "CI green" status. Phase 0 encoded traceability requirements into ADRs. Phase A makes
those requirements operative at implementation time: an ADR with a complete persona trace cannot
prevent a mission failure if the implementing agent ignores the trace at implementation time.

**The five steps:**

**Step 1 — Intent authorship** (before implementation begins)
The implementing agent authors an Implementation Intent document using
`docs/process/intent-template.md` and files it at
`docs/process/intents/M{N}-{G-suffix-or-ADR-NNN}-{YYYY-MM-DD}-{short-name}.md`. The intent document derives the
implementation's observable application state from the ADR's persona trace and UX implication
statement elements. Completeness gate: the QA Lead must be able to write a test from the intent
document without reading any implementation code. An intent document the QA Lead cannot test
from is incomplete and blocks Step 2.

**Step 2 — Test authorship** (after intent authorship; before implementation begins)
The QA Lead writes tests from the intent document's acceptance criteria before any implementation
code is written. Tests are authored from observable application states — not from the
implementation interface. "CI passes" is not a test. "Zone 1B shows the top MDA alert text
without scroll at 1440×900 with the Greece 2012 fixture at step 4" is a test. The test file is
filed before the implementation PR opens. A test authored in the same session as the
implementation it covers has not satisfied this step.

**Step 3 — Implementation**
The implementing agent writes code to satisfy the intent document's acceptance criteria. An
implementation that is not verifiable against the intent document's observable application states
is not complete, regardless of CI status.

**Step 4 — Verify** (does output match intent?)
The implementing agent confirms the observable application state defined in the intent document
is present in the running application. This is a live-application observation — not a CI check.
The verification artifact is a named Playwright test result, a recorded screen observation, or
a referenced CI test that observes the live application state against the intent document's
acceptance criteria. The implementing agent produces the verification artifact before the PR is
marked ready for review.

**Step 5 — Validate** (does output serve the mission?)
The Business PO confirms the implementation serves the mission as stated in the ADR's north star
test (Element P-7) and the intent document. Validation is a user-need confirmation — not a
technical review. CI green is not validation. Validation criteria by work type:

- **Frontend feature:** Business PO opens the live application and confirms the named persona can
  reach the observable state within the ADR's time ceiling (P-4). Customer Agent provides Layer 3
  quality assessment (see §Layer 3 Quality Gate below) before the Business PO verdict is final.
- **Backend capability:** Business PO confirms via API response or application output that the
  analytical intent is satisfied — e.g., a commodity price shock produces reserve drawdown visible
  in the trajectory response.
- **Documentation:** Business PO confirms a non-author can navigate to the key finding from the
  document's entry point in under five minutes.
- **Analytics:** Business PO confirms the output changes what the persona can argue at the
  negotiating table — naming the specific argument and why it was unavailable before.

**Business PO Acceptance as Sprint Exit Gate:** A sprint does not close when issues are closed
and CI is green. A sprint closes when the Business PO has completed the Validate step for every
user-facing deliverable in the sprint. If the Business PO cannot validate, the Business PO
produces a rejection artifact (see below). Sprint exit is blocked until the rejection is resolved.

---

## When Verify or Validate fails — the Rejection Artifact

If, at Step 4 (Verify) or Step 5 (Validate), the observable application state defined in the
intent document is absent or the mission validation fails, the finding produces a rejection
artifact. The rejection artifact is not an advisory — it blocks sprint exit.

**Rejection artifact requirements:**

1. **Named location:** `docs/process/rejections/REJECT-NNN-YYYY-MM-DD-short-description.md`
   where NNN is a sequential rejection number (zero-padded to three digits).
2. **Required contents:**
   - Source intent document (ADR reference + intent document path)
   - Which acceptance criterion failed
   - What the observable application state actually showed vs. what the intent document specified
   - Whether the gap is in the intent document (imprecise specification) or the implementation
     (implementation did not satisfy the intent)
   - Remediation scope — what must change and which step the implementing agent returns to
3. **Return to Step 1, not Step 3:** The implementing agent returns to Intent authorship, not
   Implementation. The intent must be re-examined before the implementation is corrected — a
   Verify failure is evidence that the intent-to-implementation chain had a gap, not that only
   the code needs fixing.
4. **Near-miss entry required:** Every rejection produces a near-miss registry entry filed by
   the PI Agent in the same session. A Verify or Validate failure is institutional evidence of a
   process gap and must not evaporate without a record.
5. **Sprint exit block:** The sprint cannot close, and no subsequent sprint group begins, until
   the rejection is resolved and the Business PO or implementing agent confirms the observable
   state is present.

**Business PO rejection exception path:** The Business PO produces the rejection artifact naming
the defect, the remediation scope, and the re-acceptance condition before any remediation begins.
The implementing agent must satisfy the re-acceptance condition before the sprint closes. A
Business PO rejection handled only via verbal correction — without a written rejection artifact —
has not been properly resolved. The written record prevents the same gap from appearing in the
next sprint.

---

## Layer 3 Quality Gate (FD-2)

Every user-facing capability that ships through this lifecycle must pass the Layer 3 quality
gate at the Validate step. This closes gap FD-2: self-interpreting output quality previously
had no process owner. The Customer Agent now holds that ownership.

Layer 3 quality: the output tells the user what the number means — not only displays the number.
An alert showing "−2.1%" without labeling the indicator, direction's meaning, or crossed threshold
is a Layer 2 output. A Layer 3 output for the same data: "Reserve coverage has fallen 2.1 months
below the CRITICAL threshold. At current draw rate, full depletion occurs in 4 steps."

**Agent authority:**
- Customer Agent holds R for Layer 3 quality assessment for any capability serving Persona 2, 3,
  or 5. Customer Agent produces the assessment before the Business PO delivers the Validate verdict.
- Business PO holds R for the Validate step verdict; Customer Agent's Layer 3 finding is a
  required input to that verdict — not an optional consultation.
- A Validate step that proceeds without a Customer Agent Layer 3 finding for a Persona 2/3/5
  capability is a process violation. PI Agent blocks sprint exit confirmation if absent.

**Trigger:** Any implementation that introduces or modifies a user-facing indicator label, alert
text, output narrative, or confidence tier disclosure. Does not apply to infrastructure work with
no direct user-visible output.

---

## Kryptonite Design Constraint (FD-3)

This closes gap FD-3: the founding document's kryptonite frame — "on the side of the finance
ministry team with three economists, not the IMF side with one hundred" — previously had no
operational form in the execution lifecycle. It is now a concrete tradeoff rule applied at the
Intent authorship step and enforced at the Validate step.

**The constraint:** When authoring an intent document, if there is a tradeoff between:
- Analytical depth vs. interpretability in the Reactive entry state (90-second ceiling)
- Model sophistication vs. data accessibility at Tier 3 data environments
- Output richness vs. 90-second retrieval for Persona 2

Choose the option that serves the finance ministry team. The test: could the ministry team with
three economists use this output to make a specific argument at the table, or does it require
specialist mediation that the creditor side can provide and the ministry side cannot?

**Application in Step 1 (Intent authorship):** Section 5 of the intent template (Kryptonite
Constraint Check) is a required gate at authorship. An intent document with Section 5 unchecked
is incomplete and blocks Step 2.

**Application in Step 5 (Validate):** A Validate step that passes despite the Customer Agent
identifying required specialist mediation — without an EL exception recorded — is a process
violation. "This is as simple as the domain allows" does not satisfy the kryptonite constraint.
The constraint is satisfied when: the output is interpretable by a finance ministry economist
without further translation, or the required mediation is documented as an accepted asymmetry
gap with EL approval and a forward trace to a Layer 3 improvement.

**Authority:** `docs/process/design/2026-06-08-sprint-cadence-acceptance-gates-deliberation.md §Gap FD-3`.
**Phase 0 origin:** `docs/process/sprint-plans/process-redesign-phase0-exit.md §Part III`.

---

## Observable Application State — architectural definition

An observable application state is a state of the running application — in the UI, the API, or
the database — confirmable by an agent other than the implementor using only external observation
(Playwright, curl, direct API call), without reading implementation source code.

Not observable application state:
- "CI passes" / "tests are green"
- "The function returns the correct result"
- "The feature is wired correctly"

Observable application state:
- "Zone 1B shows the top MDA alert text without scroll at 1440×900 with the Greece 2012 fixture
  loaded at step 4"
- "GET /api/v1/scenarios/{id}/trajectory returns `reserve_coverage_months` as a non-null float
  for each of 8 steps when the Jordan entity is loaded"
- "The PMM in Zone 1A displays 1.30 at step 3 when fiscal_multiplier=1.30 was set in the
  scenario configuration"

Test for a statement: can a QA reviewer confirm it by running the application, with no knowledge
of the implementation? If no — revise until yes.

---

## Lifecycle canonical document locations

| Artifact | Canonical location | Authored by |
|---|---|---|
| Intent document template | `docs/process/intent-template.md` | Architect Agent |
| Implementation Intent documents | `docs/process/intents/M{N}-{G-suffix-or-ADR-NNN}-{YYYY-MM-DD}-{short-name}.md` | Implementing agent (per ADR panel) |
| Rejection artifacts | `docs/process/rejections/REJECT-NNN-YYYY-MM-DD-short-description.md` | Implementing agent or Business PO |
| Phase A exit artifact | `docs/process/sprint-plans/process-redesign-phaseA-exit.md` | PM Agent + PI Agent |

**Self-attestation limitation (documented):** The Verify step (Step 4) depends on the
implementing agent executing it honestly. The Business PO Validate step (Step 5) and the sprint
exit gate provide external verification that compensates for this risk but does not eliminate it.
Future tooling may automate observable state verification against fixture scenarios; until then,
the three-level structure (self-verify → Business PO validate → sprint exit artifact) is the
mitigation. This limitation is recorded in `docs/process/sprint-plans/process-redesign-phaseA-exit.md
§Known Limitations`.
