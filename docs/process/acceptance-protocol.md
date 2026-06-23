---
name: acceptance-protocol
type: process-protocol
phase: Phase B — Business PO Acceptance Protocol
status: Active
authored-by: Business PO (Part 1 — Steps 1–2); PI Agent (Part 2 — exception path)
authored-date: 2026-06-12
el-endorsement-required: true
phase-entry: docs/process/sprint-plans/process-redesign-phaseB-sprint-entry.md
phaseA-inputs:
  - docs/process/agent-execution-lifecycle.md (Step 5 — Validate)
  - docs/process/agent-execution-lifecycle.md — When Verify or Validate fails
  - docs/process/agent-execution-lifecycle.md — Layer 3 Quality Gate
  - docs/process/agent-execution-lifecycle.md — Kryptonite Design Constraint
  - docs/process/intent-template.md
deliberation-source: docs/process/design/2026-06-08-sprint-cadence-acceptance-gates-deliberation.md §Phase B
---

# Business PO Acceptance Protocol — WorldSim

**Owner:** Business Product Owner (R)
**Enforcer:** PI Agent (R — sprint exit confirmation; near-miss filing on rejection)
**Accountable:** Engineering Lead
**Authority:** `docs/process/agent-execution-lifecycle.md — Step 5 (Validate)`

This document specifies what Business PO acceptance looks like for each work type, what
constitutes a passing validation, and what the exception path is when acceptance is rejected.
It makes the Validate step (Step 5 of the Agent Execution Lifecycle) repeatable rather than
improvised. Every sprint containing a user-facing deliverable uses this protocol — it is not
optional, and it is not a judgment call that varies by sprint.

**Activation:** `PO: ACCEPT — [intent document path or PR number]`

---

## Part 1 — Per-Work-Type Verification Criteria

*Authored by Business PO. Authority: docs/process/agent-execution-lifecycle.md — Step 5.*

### 1.1 Frontend Feature

**What the Business PO does:**

1. **Reads the intent document** (Section 3 — Observable Application State; Section 2 — Persona
   Trace). Identifies the fixture scenario, viewport, zone, step, and specific value or element
   that constitute the observable state for this feature.

2. **Opens the running application** at the fixture scenario named in Section 3.1. The fixture
   scenario is the canonical test context — the Business PO does not substitute a different
   scenario unless Section 3 explicitly permits it. If the fixture scenario is not loaded, the
   validation cannot proceed.

3. **Sets viewport to 1440×900** unless the intent document specifies a different viewport. This
   is the canonical demo viewport. Viewport is set before starting the validation clock.

4. **Navigates from the application's natural entry state** to the observable state using only
   UI elements. No direct API calls, no developer tools, no URL manipulation that bypasses normal
   navigation. The navigation path must be the path Persona 2 in a Reactive entry state would
   follow — not a developer shortcut.

5. **Confirms the time ceiling.** The P-4 time ceiling in the intent document is the maximum
   elapsed time from entry state to observable state. If reaching the observable state requires
   longer than P-4, the time ceiling check fails even if the observable state is eventually
   reached. A capability that passes the observable state check but exceeds P-4 has not passed
   the Validate step.

6. **Confirms the observable state** named in Section 3.1 of the intent document is visually
   present in the running application. "Visually present" means: readable without developer
   tooling, on-screen and interpretable, in the zone specified. A value that appears only in
   browser devtools or in an API response not surfaced in the UI is not present in the observable
   state for a frontend feature.

7. **Confirms silent failure is absent.** The Business PO checks the silent failure condition
   named in Section 3.3 — verifying that the observable state is genuine output, not a frozen
   or default value. For any output that should change over the scenario's steps, the Business PO
   confirms the value at step N differs from the value at step 0.

8. **Obtains the Customer Agent Layer 3 assessment** before delivering the verdict, for any
   capability serving Personas 2, 3, or 5. This assessment is a required input to the verdict —
   not a consultation the Business PO may skip. A verdict delivered without the Layer 3
   assessment for a Persona 2/3/5 capability is a process violation.

**What constitutes a passing verdict:**

The Business PO must answer YES to all of the following:
- [ ] The named persona can reach the observable state within the P-4 time ceiling navigating only UI elements from the natural entry state
- [ ] The observable state named in Section 3.1 is visually present in the running application at the named fixture scenario, viewport, and step
- [ ] The silent failure indicators in Section 3.3 are absent — the output value differs from the step-0 value at the step named in Section 3
- [ ] For Persona 2/3/5 capabilities: the Customer Agent Layer 3 assessment is on record and returns PASS
- [ ] Section 5 (Kryptonite Constraint) is satisfied — the observable state does not require specialist mediation for Persona 2 in the Reactive entry state

**Passing verdict artifact:**

Filed as a PR comment or appended to the intent document:

> VALIDATED — [date]. Persona [N] reached [observable state from Section 3.1] in [M] seconds at
> 1440×900 with [fixture scenario name] active. Silent failure check: value at step [N] = [X],
> differs from step-0 value [Y]. Customer Agent Layer 3: [PASS / N/A — Persona 1/4/6+].
> Kryptonite check: PASS. Verdict: ACCEPT.

---

### 1.2 Backend Capability

**What the Business PO does:**

1. **Reads the intent document** (Section 3 — Observable Application State). Identifies the
   specific API endpoint(s), fixture scenario(s), step(s), and field values that constitute the
   observable state for this capability.

2. **Requests the implementing agent** to execute the API calls in the Business PO's review
   context. The Business PO reviews the responses; the implementing agent executes the calls.
   The implementing agent must use the fixture scenario and parameters named in Section 3 — not
   a substitute scenario.

3. **Confirms the specific field values** named in Section 3 are present in the API response.
   "Present" means: the field is non-null, the value is within the range the intent document
   specified, and the value changes across scenario steps — it is not frozen at the initial state.
   The DEMO4 class check is mandatory: the field value at step N must differ from the value at
   step 0 for any output representing a dynamic state. A frozen output is a silent failure
   regardless of CI status.

4. **Confirms the analytical intent.** The Business PO asks: does this API response change what
   the named persona can argue at the negotiating table? The Business PO must produce a specific
   answer — naming the persona, the argument, and why this argument was unavailable before.
   "Improves situational awareness" is not an answer. "The Zambian ministry analyst can now
   quantify that the foreign-currency rollover threshold was breached at step 3, and cite the
   specific MDA threshold in the restructuring session" is an answer.

5. **Confirms silent failure distinguishability.** The Business PO validates at least one
   scenario variant where the expected field value is non-trivially different from the initial
   state. If the implementation shows the same value under all scenario conditions, the Business
   PO cannot distinguish genuine output from a silent failure — the check fails.

**What constitutes a passing verdict:**

The Business PO must answer YES to all of the following:
- [ ] The API response contains the field(s) named in Section 3 with non-null values for the named fixture scenario and step(s)
- [ ] DEMO4 class check: the field value at step N differs from the value at step 0 for any dynamic-state output
- [ ] The Business PO can name a specific argument the named persona can now make that was unavailable before this implementation
- [ ] The argument passes the asymmetry test: usable by a ministry team with three economists, without specialist mediation the creditor side provides that the ministry side cannot

**Passing verdict artifact:**

> VALIDATED — [date]. API: [endpoint]. Fixture: [scenario name]. Field [name] = [value] at
> step [N], differs from step-0 value [Y]. DEMO4 check: PASS. Analytical intent: [named persona]
> can now argue: "[specific argument]". Prior limitation: [what was absent]. Asymmetry test:
> PASS. Verdict: ACCEPT.

---

### 1.3 Documentation

**What the Business PO does:**

1. **Identifies the canonical entry point.** The intent document's Section 3.1 names the entry
   point — the path a first-time reader follows to discover this document (e.g., CLAUDE.md
   §section → linked document → key finding). If no canonical entry point is named in the
   intent document, the Business PO looks for the natural navigation path from the project's
   standard entry points (CLAUDE.md, SESSION_STATE.md, agents.md).

2. **Navigates from the entry point to the document.** The Business PO follows the link chain
   from the named entry point as if discovering the document for the first time — without using
   the document's file path directly. If there is no navigation path from a canonical entry point
   to the document, the navigability test has failed before the five-minute clock starts. A
   document with no inbound links from any project navigation entry point is not discoverable.

3. **Starts a five-minute clock** from the entry point. The clock runs until the Business PO
   locates and reads the key finding named in the intent document's Section 3.

4. **Evaluates navigability.** Can a non-author navigate to the key finding from the entry point
   in under five minutes? The non-author simulation: the Business PO navigates as if the document
   is unknown — no prior knowledge of its existence, no shortcut to the file path.

**What constitutes a passing verdict:**

The Business PO must answer YES to all of the following:
- [ ] A navigation path exists from a canonical entry point (CLAUDE.md, SESSION_STATE.md, or agents.md) to this document — not just a direct file path
- [ ] The key finding named in Section 3.1 is reachable in under five minutes from the entry point
- [ ] The key finding is explicitly named or headed in the document — it does not require section-by-section reading to locate

**Passing verdict artifact:**

> VALIDATED — [date]. Navigation path: [entry point] → [link/section] → [document name].
> Key finding "[finding description]" reached in [M] minutes. Verdict: ACCEPT.

---

### 1.4 Analytics

**What the Business PO does:**

1. **Reads the analytical output** named in the intent document's Section 3 — the indicator
   value, composite score, trajectory, or model result.

2. **Applies the Kryptonite frame.** Does this output change what the named persona can argue
   at the negotiating table? The Business PO must name:
   - The specific persona (by name and number from `docs/ux/personas.md` — not "a user")
   - The specific argument: a concrete, citable claim, not a capability description
   - Why this argument was unavailable before: what was the prior limitation — absent indicator,
     unavailable disaggregation, opaque causal chain, or unquantified uncertainty?

3. **Applies the asymmetry test.** Could the ministry team with three economists use this
   argument at the table, or does deploying it require specialist mediation that the creditor
   side can provide and the ministry side cannot? If specialist mediation is required and no EL
   exception exists, the Kryptonite constraint is not satisfied. "This is as complex as the
   domain allows" does not satisfy the constraint — the constraint is satisfied when the output
   is interpretable by a finance ministry economist without further translation.

4. **Requests a Customer Agent AUDIT** if the output is user-facing — before delivering the
   verdict. The AUDIT must confirm Layer 3 usability: the output tells the user what the number
   means, not only displays the number.

**What constitutes a passing verdict:**

The Business PO must answer YES to all of the following:
- [ ] The analytical output is present and matches the observable state named in Section 3
- [ ] The Business PO can name the specific argument the named persona can make — not aspirational, not "improves situational awareness"
- [ ] The argument passes the asymmetry test: usable by the ministry team without specialist mediation the creditor side can provide and the ministry side cannot
- [ ] For user-facing output: Customer Agent AUDIT is on record and confirms Layer 3 usability

**Passing verdict artifact:**

> VALIDATED — [date]. Persona [N] ([name]): can now argue "[specific citable argument]".
> Prior limitation: [what was absent]. Asymmetry test: PASS — usable without specialist mediation.
> Customer Agent Layer 3: [PASS / N/A — infrastructure]. Verdict: ACCEPT.

---

## Part 2 — Exception Path Specification

*Authored by PI Agent. Authority: docs/process/agent-execution-lifecycle.md — When Verify or Validate
fails; deliberation source §Phase B PI Agent Finding 3.*

### 2.1 When the Business PO Triggers a Rejection

A rejection is triggered when the Business PO cannot answer YES to all passing checklist items
for the relevant work type in Part 1. The threshold is binary: the passing checklist is either
complete or it is not. There is no partial pass.

The Business PO does not reject for reasons outside the passing checklist. If the implementation
passes all checklist items, the Business PO accepts — even if the Business PO has opinions about
design or quality not captured in the checklist. Those opinions are backlog scope items routed
to PM Agent, not rejection grounds. The checklist is repeatable precisely because it is not a
judgment call.

**Rejection triggers by work type:**

| Work type | Rejection triggers |
|---|---|
| Frontend feature | Observable state absent or incorrect; time ceiling exceeded; silent failure present (output frozen at step-0 value); Customer Agent Layer 3 FAIL without EL exception; Kryptonite constraint violated without EL exception |
| Backend capability | API field null or frozen at initial value (DEMO4 class failure); analytical intent (P-7) cannot be stated specifically; asymmetry test fails without EL exception |
| Documentation | No canonical navigation path from any project entry point; key finding not reachable in under five minutes |
| Analytics | Specific argument cannot be named; argument requires specialist mediation without EL exception; Customer Agent Layer 3 FAIL for user-facing output without EL exception |

### 2.2 Rejection Artifact Requirements

When a rejection is triggered, the Business PO produces a rejection artifact per
`docs/process/agent-execution-lifecycle.md — When Verify or Validate fails`.

**Location:** `docs/process/rejections/REJECT-NNN-YYYY-MM-DD-short-description.md`
(NNN is the next sequential rejection number from the rejections directory)

**Required contents common to all work types:**
- Source intent document (ADR reference + intent document path)
- Which acceptance criterion failed (reference the checklist item number from Part 1)
- What was expected vs. what was observed
- Whether the gap is in the intent document (imprecise specification) or the implementation
  (implementation did not satisfy the intent)
- Remediation scope: what must change; which step the implementing agent returns to (Step 1 —
  Intent authorship; not Step 3 — Implementation)
- Re-acceptance condition: the specific, named check the Business PO will execute at re-acceptance

**Additional required content by work type:**

*Frontend feature:*
- The observable state expected: exact quote from Section 3.1 of the intent document
- What the Business PO observed in the running application at the named fixture scenario, viewport, and step
- Customer Agent Layer 3 finding on record (presence required even when not the primary rejection reason)

*Backend capability:*
- The API endpoint called, the fixture scenario loaded, and the actual field value returned
- DEMO4 class check result: whether the field value was frozen (same as initial state)

*Documentation:*
- The navigation path attempted and where the chain broke
- Whether the gap is a missing inbound link (not discoverable) or a navigability failure (link chain exists but key finding not reachable in five minutes)

*Analytics:*
- The specific argument that could not be named, or the mediation required to deploy the argument
- Whether the Kryptonite constraint is the primary failure

**Near-miss entry requirement:** Every rejection artifact requires a near-miss registry entry
filed by the PI Agent in the same session. The near-miss records: what happened, what was at
risk, what caught it, and what process improvement resulted. A rejection that produces no
near-miss entry has not been properly processed institutionally — the intent-to-implementation
gap it evidenced must become permanent institutional memory.

### 2.3 Re-Acceptance Process

**Return-to-Step-1 requirement:** Per `docs/process/agent-execution-lifecycle.md`, the implementing
agent returns to Intent authorship (Step 1), not Implementation (Step 3). A Verify or Validate
failure is evidence that the intent-to-implementation chain had a gap. The intent must be
re-examined before the code is corrected — the intent may be the source of the gap.

**Re-acceptance gate:** The implementing agent and Business PO use the re-acceptance condition
named in the rejection artifact as the only acceptance criterion at re-acceptance. The Business
PO does not introduce new requirements at re-acceptance that were not in the original passing
checklist. New requirements belong in a new intent document for a new scope.

**Re-acceptance verdict artifact:** The Business PO files a re-acceptance verdict in the same
format as the original verdict, with this appended line:
> "RE-ACCEPTED — [date]. Rejection [REJECT-NNN] resolved. Re-acceptance condition satisfied:
> [condition from rejection artifact]."

**Sprint exit block:** The sprint cannot close until the Business PO re-acceptance verdict
artifact is filed and the PI Agent confirms the rejection is resolved. PI Agent holds R for
confirming resolution before the sprint exit gate passes.

### 2.4 EL Exception Path

If the Engineering Lead determines that proceeding despite a rejection is necessary (scope
constraint, milestone pressure, or known acceptable limitation at this milestone):

1. **EL appends an exception** to the rejection artifact in a new section:
   > "EL Exception — [date]. Reason: [why the rejection is accepted as-is]. Accepted limitation:
   > [what the limitation is and why it is acceptable]. Forward trace: [milestone and capability
   > that will address this limitation]."

2. **The exception substitutes for re-acceptance.** The sprint may close with the exception on
   record. The rejection artifact is not deleted or modified — the exception is appended to it.

3. **The exception is not a verdict reversal.** The Business PO's rejection finding is permanent
   institutional record. The EL exception acknowledges the project is proceeding with a known
   limitation — and that the limitation is documented with a forward trace.

4. **PI Agent files a near-miss** referencing the EL exception in the same session. An
   exception-closed rejection is still institutional evidence of a process gap; the near-miss
   entry ensures it becomes a systemic prompt rather than an isolated incident.

### 2.5 PI Agent Enforcement Review

This protocol has teeth if and only if:

1. **The passing checklist items are observable, not interpretable.** Each checklist item in Part 1
   names a specific, confirmable condition — not a quality judgment. "The observable state is
   visually present" is confirmable; "the feature is well-implemented" is not. The protocol's
   specificity is its enforcement mechanism.

2. **The rejection artifact format is mandatory, not suggested.** A Business PO finding that is
   not filed as a rejection artifact (e.g., communicated verbally, recorded only in a PR comment
   without the canonical location and sequential number) has not satisfied the format requirement.
   PI Agent holds R for confirming that every rejection is filed at the canonical location.

3. **The near-miss entry is filed in the same session as the rejection.** A near-miss entry filed
   in a subsequent session is not the same as one filed in the session the gap was found — the
   institutional evidence trail depends on the near-miss being tied to the session that produced it.

4. **The re-acceptance condition names a specific check.** "Address the Business PO's concerns"
   is not a re-acceptance condition. "GET /api/v1/scenarios/{id}/trajectory returns
   reserve_coverage_months ≠ 7.1 at step 3 for the JOR entity with the Hormuz fixture" is a
   re-acceptance condition. The specificity is what makes re-acceptance a gate rather than
   a renegotiation.

**PI Agent verdict on Part 2:** Enforcement language is obligation, not aspiration. Each gate
names who enforces it. Rejection artifacts have teeth: they block sprint exit, require near-miss
entries, and mandate return to Step 1. The exception path preserves the Business PO's finding
as institutional record while providing the EL an explicit override path. This protocol is
adequate for Phase B exit.

---

## Application Notes

**This protocol applies to every sprint containing a user-facing deliverable.** It does not apply
to pure infrastructure work (Tier 3 ADRs with no direct user-visible output). When in doubt about
work type, the Business PO asks the implementing agent to confirm the ADR tier.

**Multiple work types in one sprint:** A sprint containing frontend features, backend capabilities,
documentation, and analytics work applies this protocol per-deliverable. The sprint exit gate does
not close until all deliverables have received a Business PO verdict.

**The Customer Agent Layer 3 assessment is a precondition, not a follow-up.** For Persona 2/3/5
capabilities, the Business PO requests the Customer Agent AUDIT before the Business PO Validate
step begins — not after. A verdict delivered without it is a process violation.

**This protocol is the gate, not the relationship.** The Business PO and implementing agent may
have aligned views on quality; the protocol exists for the case when they do not. Applying it
consistently — accepting when the checklist is complete, rejecting when it is not — is what
makes sprint exit a gate rather than a rubber stamp.

---

*This document is the canonical Phase B output. It references Phase A outputs
(`docs/process/agent-execution-lifecycle.md`) and feeds Phase C (sprint cadence formalization via
the sprint exit gate reference in `docs/process/sprint-planning-sop.md §Sprint Exit Gate`).
Changes require Business PO and PI Agent review and EL endorsement.*
