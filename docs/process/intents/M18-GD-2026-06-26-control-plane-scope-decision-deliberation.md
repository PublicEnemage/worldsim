---
name: M18-GD-control-plane-scope-decision-deliberation
type: deliberation-record
companion-to: "docs/process/intents/M18-GD-2026-06-26-control-plane-scope-decision.md"
artifact: "Artifact 5 — GD Design Package (#1359)"
status: "Panel findings recorded — awaiting EL review and decision"
authored-by: PM Agent (panel assembly); agent findings recorded in session
authored-date: 2026-06-26
el-decision-pending: true
release-branch: release/m18
---

# Deliberation Record — Artifact 5 Panel Review

This document records the panel assembly, individual agent findings, and synthesis
for EL review prior to the Artifact 5 approval decision. It is a companion to
`docs/process/intents/M18-GD-2026-06-26-control-plane-scope-decision.md`.

---

## Part I — Panel Assembly Record

### Derivation basis

Artifact 5 spans three distinct authority domains. The panel was derived by decision
rather than by a single ADR type per `docs/process/agent-raci.md §ADR Panel Composition`.
The Architect Agent is not on the review panel — Architect is the ADR-019 author and
receives panel findings as inputs, not votes.

### Panel composition

| # | Agent | Assigned decisions | Authority basis |
|---|---|---|---|
| 1 | UX Designer Agent | 1, 2 | R on UX frame changes; §Control Plane Reserved Zone is a current ruling — changing Mode 2 column content requires UX Designer ruling, not downstream discretion |
| 2 | Frontend Architect Agent | 1, 3 | Primary G4 implementer; RACI C on frontend architecture + UX decisions; EX-001 is a frontend performance gate they own |
| 3 | Business Product Owner | 2 | RACI C on all scope decisions; Demo 7 minimum viable authority |
| 4 | Customer Agent | 1 | RACI C on user-visible changes; working agreement with Architect: Layer 3 finding before panel review for new instrument/interaction changes |
| 5 | Computation Engine Agent | 2 | RACI C on decisions with computational/API implications; shock injection is a new backend endpoint |
| 6 | DevSecOps Agent | 3 | CI gate configuration authority; KI-006 (GHA infrastructure) is on record under their domain |
| 7 | PI Agent | 3 | Exception expiry compliance; EX-001 has now passed its M17 exit expiry date |

### Activation calls issued

```
UX Designer: REVIEW — Mode 2 column 3 content scope (Decision 1) and shock taxonomy
visual system consistency (Decision 2) for Artifact 5 (#1359, M18 GD)

Customer Agent: AUDIT — Mode 2 → Mode 3 transition control for Personas 2 and 5,
Artifact 5 Decision 1 (#1359)

Frontend Architect: REVIEW — Mode 2 column 3 feasibility and EX-001 optimization
path assessment, Artifact 5 Decisions 1 and 3 (#1359)

Business PO: REVIEW — shock taxonomy M18 scope decision, Artifact 5 Decision 2 (#1359)

Computation Engine Agent: REVIEW — shock injection API scope for all six vs. subset
of Form 2 taxonomy, Artifact 5 Decision 2 (#1359)

DevSecOps Agent: REVIEW — EX-001 disposition and AC-009 resolution path,
Artifact 5 Decision 3 (#1359)

Process Integrity Agent: REVIEW — EX-001 expiry compliance and process conditions
for whichever resolution path EL selects, Artifact 5 Decision 3 (#1359)
```

---

## Part II — Agent Findings

### UX Designer Agent — Decisions 1 and 2

**Session context:** Same session as panel chair — acknowledged.

---

**Decision 1 — Mode 2 column 3 content**

The current ruling is in `docs/ux/information-hierarchy.md §Control Plane Reserved Zone`,
established M9 (PR #390):

> "In Mode 1 and Mode 2, this zone is empty — it holds no content and is not collapsed
> or hidden; it is reserved. In Mode 3, it is populated with the control plane."

This is not advisory language — it is a ruling. The M9 ruling table at §M9 Hierarchy
Decisions records: "Control plane zone reserved from M9 onward (Premise 5, PR #390) —
Empty reserved zone in Mode 1 and Mode 2."

**My assessment:** The proposed change is justified but requires an explicit ruling
amendment, not just a downstream implementation choice. The "empty reserved zone" design
principle served a specific purpose: it prevented the zone from being filled with
secondary content before Mode 3 existed, which would have created a retrofitting problem.
That risk is now past — Mode 3 is built. The zone was sized for the Mode 3 control plane.
A minimal Mode 2 surface does not undermine the sizing rationale.

**Ruling — Decision 1:**

The Mode 3 activation control belongs in column 3 in Mode 2. I approve the draft
recommendation with three required refinements for ADR-019:

1. **Visual treatment must signal "pre-active" state.** The Mode 2 column 3 content
   must use a visually subdued treatment relative to Mode 3 — reduced weight, muted
   palette. The column in Mode 2 should communicate "this zone activates when you
   enter Active Control," not "this zone is currently active." A subtle border or
   background change on mode transition reinforces the state shift.

2. **No editable elements in Mode 2 column 3.** The scenario summary is read-only.
   The Mode 3 activation affordance is the only interactive element. Any additional
   elements (run configuration edits, parameter adjustments) are out of scope and
   would conflict with Mode 2's cognitive task (threshold-safe path construction
   requires undistracted trajectory reading, not configuration).

3. **Information hierarchy ruling table must be updated.** The §M9 Hierarchy Decisions
   ruling: "Empty reserved zone in Mode 1 and Mode 2" becomes "Empty in Mode 1; minimal
   read-only surface in Mode 2 (scenario summary + Mode 3 activation control); populated
   with control plane in Mode 3." This update is Artifact 7 scope (#1361, Journey C and
   architecture update) — it must reference this ruling change.

**The information hierarchy §Control Plane Reserved Zone prose must also be amended.**
ADR-019 authors this amendment as part of the Artifact 6 / 7 package.

**Decision 1 verdict: APPROVE** — with the three refinements above required in ADR-019.

---

**Decision 2 — Shock taxonomy visual system**

Six shock types: `ElectionShock`, `CurrencyAttack`, `CreditorDefection`,
`GeopoliticalShock`, `NaturalDisaster`, `ContagionShock`.

The blue/orange epistemic separation is about the *category* of input, not the
*sub-type*. Policy instruments = blue (controlled by the analyst). Exogenous shocks =
orange (events the simulation observes, not the analyst chooses). All six shock types
are exogenous — they all carry orange treatment without exception. The visual system
is not strained by six types versus two.

**Decision 2 verdict (visual system only): APPROVE.** Full taxonomy is consistent with
the existing visual system. No new ruling required. The shock type selector in Form 2 is
a dropdown or radio group within the orange-treated form — the type selection does not
introduce new color semantics.

---

### Customer Agent — Decision 1

**Layer 3 assessment — Personas 2 and 5**

---

**Persona 2 (Eleni Papadimitriou, Finance Ministry Negotiator)**

Eleni's working mode is reactive — she arrives at the tool with a specific question and
90 seconds to answer it. The Mode 2 → Mode 3 transition is a deliberate choice, not a
reflex. She would take this step when she wants to test a counter-proposal live — the
"apply and see" action.

**Finding 1 — KRYPTONITE (major): "Mode 3" is an internal system label.**

The draft recommendation uses "Enter Mode 3" as the button label and "Mode 3 branching"
in the caution notice. Eleni does not use the phrase "Mode 3" — she is using a simulation
tool that has states, not modes she named. "Mode 3" is WorldSim's internal taxonomy.
Presenting it as a user-facing label requires Eleni to have internalized a WorldSim
vocabulary category. She will not have done this in the 90-second retrieval window.

This is a kryptonite vector: Eleni needs specialist knowledge (what is "Mode 3"?) to
operate the primary transition control in the column. The column is the zone she will
interact with most intensively during Demo 7 Act 1.

**Required change:** The button label must be in plain language. Recommendation:
**"Enter Active Control"** — this describes what the state does ("you are actively
controlling the scenario"), not what the system calls it. The caution notice rewrite:
*"Active Control creates a live analysis path from the current step. You can return to
the original scenario at any time by exiting Active Control."*

**Finding 2 — POSITIVE: scenario summary calibration vintage serves Eleni directly.**

The proposed scenario summary includes calibration vintage (e.g., "Calibrated against
Q3 2024 IMF Article IV data"). For Eleni, the calibration vintage is a negotiation
asset — she needs to know whether the data is current before citing a number across a
table. The scenario summary in Mode 2 column 3 is exactly the right pre-flight
confirmation surface. She can check the vintage, confirm the entity, confirm the
horizon, and then commit to Active Control. This is not noise — it is productive context
within Mode 2's cognitive task.

**Layer 3 verdict — Persona 2:** Approve the concept with kryptonite fix applied
(relabel to plain language before ADR-019 commits the interaction pattern).

---

**Persona 5 (Aicha Mbaye, Finance Minister)**

Aicha is a demonstration consumer, not a direct user. She does not interact with the
Mode 2 column 3 — she observes a presenter doing so. However, she may read column 3
content over the presenter's shoulder and will form an immediate opinion on whether
the tool looks like something a serious institution would use.

**Finding 3 — KRYPTONITE (moderate): "Mode 3 branching" in visible caution text.**

If Aicha reads the caution notice during the Mode 3 activation moment and sees
"branching" or "Mode 3," she will categorize this as technical jargon from a prototype
tool. Per Persona 5: "Aicha terminates the demonstration and does not revisit the tool
if she encounters unexplained jargon." The activation moment is high-stakes — it is
the moment the tool demonstrates that it can do something the IMF's analytical software
cannot. The interface must be authoritative, not technical-looking.

The plain-language rewrite (Finding 1) also resolves this finding.

**Finding 4 — POSITIVE: column 3 as the designated control zone.**

For a demonstration audience, having a dedicated control zone (column 3) that visibly
activates when the presenter enters Active Control is a strong demo signal. Aicha sees:
here is where the analyst's inputs live; there is the trajectory; here is what happens
when the analyst applies a policy. The column 3 architecture communicates the simulation
model's causal structure visually. This is the right design.

**Layer 3 verdict — Persona 5:** Approve with kryptonite fix applied (same as Persona 2
fix — plain language throughout column 3 user-facing text).

---

### Frontend Architect Agent — Decisions 1 and 3

---

**Decision 1 — Mode 2 column 3 feasibility**

The proposed Mode 2 surface (read-only scenario summary + activation control) is
architecturally clean under one condition: column 3 in Mode 2 and column 3 in Mode 3
must be **two separate components**, not one component with conditional rendering.

If a single component handles both Mode 2 (read-only summary) and Mode 3 (full control
plane with two forms), the component manages internal mode state and has conditional
render paths. This pattern is harder to test and creates risk of state leakage —
particularly the risk that a policy input applied in Mode 3 partially persists when the
user returns to Mode 2 and re-examines the scenario summary.

Recommended pattern: **Mode2ColumnSurface** (lightweight — scenario metadata from store,
one activation button, no form state) + **ControlPlane** (full Mode 3 component,
existing or restructured). The parent `InstrumentCluster` mounts one or the other based
on active mode. Zero state sharing between them.

The mode transition event from `Mode2ColumnSurface` dispatches via the existing mode
state in the Zustand store (or equivalent). No new global state patterns required.

**The scenario summary data (entity name, calibration vintage, run horizon) is already
available in the scenario store.** No new API calls. Rendering cost is negligible.

**Decision 1 feasibility verdict:** Achievable in G4 scope. ADR-019 must specify the
two-component pattern explicitly — this is not an implementation detail for the engineer
to choose; it is an architectural constraint. If ADR-019 leaves this unspecified, the
risk of a coupled single-component implementation is real.

---

**Decision 3 — EX-001 optimization path**

EX-001 context: first real AC-009 CI measurement was 179ms (4× throttled, M16-G6 fix).
M17 status update: AC-009 converted to `test.fixme()` after CI returned 712–771ms vs.
200ms threshold — the GHA runner produces measurements 3–4× above the exception
threshold, not because the code is slow but because the CI environment is not the right
tool for this measurement.

**G4 structural optimization:** The G4 column restructuring replaces the bottom-bar
ControlPlane with a column-resident component and adds a Mode 2 surface (Decision 1).
This changes the Mode 3 render profile in a structurally significant way:

- **Lazy mounting is a structural consequence, not an added optimization.** In the new
  architecture, `ControlPlane` (Mode 3 full component) only mounts when Mode 3 is
  active. In Mode 1 and Mode 2, `Mode2ColumnSurface` mounts instead. The old bottom-bar
  ControlPlane was mounted at all times; the new column-resident component is not. This
  alone is likely to move the Mode 3 *initial activation* render cost — the first mount
  is the expensive one; subsequent steps are incremental Recharts updates.

- **Recharts memoization** (React.memo on series data) requires identifying which props
  trigger unnecessary re-renders. The primary candidate: trajectory data passed as new
  object references on every parent state change. Memoization with stable prop comparison
  is achievable but requires careful implementation — it must not suppress legitimate
  re-renders when trajectory data actually changes.

**My honest assessment:** After G4 lazy mounting, the MV-002 ProBook re-run (1× speed,
no throttle) will very likely show improvement over the current 50.5ms baseline. Mode 3
initial render will be faster because `ControlPlane` doesn't pre-render in Mode 1/2.

The CI gate is not recoverable. KI-006 is structural — GHA free-tier runners at 4×
throttle are not the right environment for measuring a Recharts-heavy UI. Even after
optimization, the CI measurement will likely still exceed 200ms (the exception threshold)
on GHA runners. Maintaining AC-009 as a CI assertion — at any threshold — provides no
regression signal on this infrastructure.

**Decision 3 recommendation:**

1. G4 implements structural optimization (lazy mounting via two-component pattern,
   Recharts memoization where straightforward).
2. At G4 exit, re-run MV-002 on ProBook hardware. Record result. If ≤ 100ms: close
   EX-001 as **Resolved** (the original specification is met on the hardware it was
   designed for).
3. Remove `test.fixme()` from AC-009 entirely — do not restore it to `test()`. The CI
   environment cannot support this assertion. Permanent removal.
4. If MV-002 re-run exceeds 100ms despite optimization: close EX-001 as **Won't Fix**
   with measurement evidence on record. This should not happen given lazy mounting, but
   is the fallback.

---

### Business Product Owner — Decision 2

**North star test for shock taxonomy scope:**

The question is not "what does Demo 7 require?" — the question is "what does the tool
need to look like for a Finance Minister's team to use it confidently in a live session?"

A control plane with a Form 2 that shows two of six shock types is a prototype. An
experienced Finance Ministry analyst (Persona 2) will notice that the taxonomy is
incomplete — she has been in rooms with IMF analysts using tools that do not show their
limitations. An incomplete taxonomy in a live demo signals that this is early-stage
software. That signal undermines the primary Demo 7 objective, which is establishing
that the tool is ready for the negotiating table.

**Demo 7 Act 1 script does not exercise Form 2.** I have confirmed this — the Act 1
narrative is about Form 1 (fiscal counter-proposal). But Form 2 is visible in the
column during Act 1. A participant who asks "what are those orange controls?" must
receive a complete answer. "These are the scenario shock types available — here is a
currency attack, here is a creditor defection" is a strong demo moment. "These are
two of the six shock types we've implemented so far" is not.

**CE Agent input on backend effort is the deciding variable.** If all six types require
equivalent backend structure (a `ShockEvent` discriminator with type-specific parameter
schemas), there is no cost argument for deferral. The scope question becomes purely a
question of parameter schema completeness — and the CE Agent's assessment addresses this.

**Decision 2 verdict: all six in M18**, contingent on CE Agent confirming that the
backend endpoint structure supports all six without disproportionate additional effort.
The parameter schemas for all six must be specified in ADR-019 before G4 implementation
begins.

---

### Computation Engine Agent — Decision 2

**Backend endpoint analysis — Form 2 shock injection**

The API contract (`api_contracts.yml:608`) already includes `shock_events` in the
response schema: `event_type: {type: string}, metadata: {type: object}`. This is the
*output* format — shock events are already recorded in run outputs.

The *input* format for Mode 3 shock injection is currently unspecified. The existing
Mode 3 mechanism (`branch_from_step`) accepts a step and policy inputs. Form 2 requires
a parallel injection mechanism: a `ShockEvent` object with a type discriminator and
type-specific parameters.

**All six types share the same endpoint pattern.** The structural work is one endpoint
(or extension of the branching endpoint) accepting a `ShockEvent` with:

```
shock_type: enum[ElectionShock, CurrencyAttack, CreditorDefection,
                 GeopoliticalShock, NaturalDisaster, ContagionShock]
parameters: {type-specific dict — validated against shock_type}
inject_at_step: int
```

**Parameter complexity varies by type.** My assessment:

| Type | Parameters | Data dependency |
|---|---|---|
| `ElectionShock` | severity (float), political_uncertainty (float) | Self-contained |
| `NaturalDisaster` | affected_sectors (list), gdp_impact (float) | Self-contained — sectors from scenario taxonomy |
| `GeopoliticalShock` | regime_change_probability (float), regional_contagion (bool) | Self-contained |
| `CurrencyAttack` | attack_magnitude (float), duration_steps (int) | Self-contained |
| `CreditorDefection` | creditor_class (enum), share_affected (float) | Requires creditor taxonomy — may need reference data |
| `ContagionShock` | source_country (ISO3), transmission_rate (float) | Requires contagion linkage table — data-dependent |

**Key finding:** `CreditorDefection` and `ContagionShock` have data-dependent parameters
that may require reference tables not currently in the database. `creditor_class` needs
a defined taxonomy (bilateral, multilateral, commercial, Eurobond, etc.).
`source_country` requires a contagion linkage table for the scenario entity.

**This is a pre-implementation risk, not a reason to defer.** ADR-019 must resolve:
(1) define the `creditor_class` taxonomy, and (2) specify whether `ContagionShock`
requires a pre-populated linkage table or uses a simplified transmission model. If
either requires new database tables, the schema update must be in the G4 sprint entry
scope declaration.

**Effort difference between 2 types and 6 types:** Minimal — the endpoint structure
is the same. Parameter schema definitions are the incremental work per type. Deferring
two data-dependent types would save parameter schema definition work for those two types
only. This is not a meaningful scope reduction for a milestone whose primary deliverable
is a live external demo.

**Decision 2 verdict: all six in M18**, with the condition that ADR-019 specifies
parameter schemas and data dependency status for all six types before G4 sprint entry.
Specifically: `creditor_class` taxonomy and `ContagionShock` linkage table approach
must be resolved in ADR-019. Failing to resolve these before G4 implementation begins
risks the same class of runtime failure as the `name_en` / `name` incident.

---

### DevSecOps Agent — Decision 3

**CI gate configuration assessment — EX-001 / AC-009**

KI-006 documents the technical constraint: GHA free-tier 2-core shared runners at
4× CPU throttle return 512–771ms for the Mode 3 full render test. The 100ms threshold
(original AC-009 pass criterion) and the 200ms exception threshold (EX-001) are both
unachievable on this infrastructure. This is not a code problem — it is a measurement
environment problem.

**Options assessment:**

**(a) Remove AC-009 from CI, replace with local gate:** Achievable. A `npm run profile`
script can invoke Playwright with the `--trace` flag on a single tagged test
(`@perf-mode3`) and record `performance.measure()` entries. The pass criterion at ≤ 100ms
is enforced by the developer running `npm run profile` locally and reading the output.
Risk: no automated enforcement. If the developer skips the profile step, regressions
are not caught.

**(b) Playwright `--trace` annotation (record without assert):** This produces trace
files in `frontend/playwright-report/` that will accumulate silently. No one will look
at them without a regression incident prompting the look. This is surveillance without
accountability. I do not recommend this option.

**(c) Close as Won't Fix after G4 optimization, with MV-002 ProBook as evidence:**
The ProBook measurement (50.5ms at 1× speed) is the meaningful real-world number.
If G4 lazy mounting reduces the Mode 3 initial render cost further (expected — see FA
finding), the ProBook number improves. "Won't Fix" with a measured ProBook result of
≤ 100ms is a defensible closure: the code meets the original specification on the hardware
it was designed for. The CI environment cannot validate this; the real hardware can.

**My recommendation: option (c).** Close EX-001 as Won't Fix after G4 exit, with
MV-002 ProBook re-run ≤ 100ms as the closure evidence. Remove `test.fixme()` from
AC-009 permanently. The test file still exists (the test is not deleted) but the
`test.fixme()` annotation is removed and replaced with a `// AC-009: closed via MV-002
ProBook re-run — see docs/compliance/exceptions.md §EX-001` comment. This preserves
the test structure for any future decision to restore the assertion.

The local developer gate (option a) provides regression monitoring but only if enforced.
I would scope the local profile script regardless — as a non-CI tool for any developer
who wants to check render performance. It should not be called a "gate" unless it is
enforced at PR time (which it cannot be in CI).

---

### PI Agent — Decision 3

**Compliance assessment — EX-001 expiry**

EX-001 status: expired at M17 exit. The M17 status update (2026-06-25) was EL-authorized,
deferred the resolution decision to Artifact 5, and named three options. The deferral is
documented — no near-miss has been created for the M18 entry window. The Artifact 5
scope decision document is the mechanism that resolves the deferral.

**FA and DS findings are compatible.** FA recommends close as Resolved if MV-002 ≤ 100ms,
Won't Fix if MV-002 exceeds 100ms. DS recommends Won't Fix preemptively. The substance
is the same: close EX-001 at G4 exit using MV-002 ProBook measurement as evidence,
remove AC-009 from CI. The "Resolved" vs. "Won't Fix" label is a classification decision
for EL (see §Part III — Open Question 1).

**Three process conditions required regardless of which label EL selects:**

**Condition 1 — Record resolution path in exceptions registry before G4 begins.**
`docs/compliance/exceptions.md §EX-001` must be updated with a "Resolution Path Record"
entry before the G4 sprint entry is filed. The entry states: (a) which resolution path
EL selected, (b) what evidence is required at G4 exit (MV-002 re-run ≤ 100ms), and
(c) the AC-009 disposition (permanent removal of `test.fixme()`, per DS recommendation).
If this update happens after G4 begins, the implementing agent has no process obligation
to deliver the optimization — it must be on record before the sprint entry.

**Condition 2 — G4 sprint entry must name EX-001 resolution as an explicit deliverable.**
The G4 sprint entry scope declaration (§3.1) must include EX-001 resolution as a named
item, alongside the column implementation and render optimization. An optimization that
is implied but not named in the sprint entry can be deprioritized under sprint pressure.
Naming it makes it a reviewable deliverable at G4 exit gate.

**Condition 3 — Final closure entry in exceptions registry at G4 exit.**
At G4 exit, the implementing agent adds a Resolution Record to `docs/compliance/exceptions.md
§EX-001` with: date, MV-002 measurement result, AC-009 status change, and EL confirmation
that the exception is closed. PI Agent reviews this entry before G4 exit confirmation.

**EX-001 process verdict:** No NM filing required at this stage — the deferral was
EL-authorized and Artifact 5 is the resolution mechanism. The three conditions above
are the process safeguards. If G4 exits without the Resolution Record in the exceptions
registry, PI Agent files a process near-miss at G4 exit gate review.

---

## Part III — Synthesis

### Decision 1 — Mode 2 column 3 scope

| Agent | Verdict | Key condition |
|---|---|---|
| UX Designer | APPROVE | Three refinements required in ADR-019: (1) subdued visual treatment, (2) no editable elements, (3) information hierarchy ruling update |
| Customer Agent | APPROVE | Kryptonite fix required: relabel "Enter Mode 3" → "Enter Active Control" and rewrite caution text to plain language (applies to Personas 2 and 5) |
| Frontend Architect | APPROVE | ADR-019 must specify two-component architecture (Mode2ColumnSurface + ControlPlane) — not a single component with conditional rendering |

**Consensus: YES — three agents approve the minimal read-only surface.**

Three concrete ADR-019 requirements emerge from the panel:
1. Button label: "Enter Active Control" (Customer Agent, kryptonite — major)
2. Visual treatment: subdued/pre-active state (UX Designer)
3. Architecture: two separate components, not conditional rendering (Frontend Architect)

None of these are contradictory. All three are additive specifications for ADR-019.

---

### Decision 2 — Shock taxonomy M18 vs. deferred

| Agent | Verdict | Key condition |
|---|---|---|
| UX Designer | APPROVE (all six) | Visual system holds; no new ruling required |
| Business PO | APPROVE (all six) | Demo credibility requires complete taxonomy; CE backend effort is the deciding variable |
| Computation Engine Agent | APPROVE (all six) | Backend structure is equivalent across six types; incremental cost per type is low |

**Consensus: YES — all six shock types in M18.**

One required ADR-019 input from CE Agent:

ADR-019 must specify, before G4 sprint entry, the parameter schemas and data dependency
status for all six shock types. Specifically:
- `creditor_class` enum taxonomy for `CreditorDefection` must be defined
- `ContagionShock` linkage table approach (pre-populated table vs. simplified model)
  must be resolved

These are not blocking the M18 scope decision — they are required inputs to ADR-019.

---

### Decision 3 — EX-001 disposition

| Agent | Verdict | Key condition |
|---|---|---|
| Frontend Architect | Close at G4 exit via MV-002 re-run; Resolved if ≤ 100ms, Won't Fix otherwise | Permanent AC-009 removal from CI |
| DevSecOps Agent | Won't Fix after G4 optimization; MV-002 ProBook as evidence | Permanent removal of test.fixme(); test structure preserved with comment |
| PI Agent | Either label; three process conditions required | Conditions apply before G4 begins, at sprint entry, and at G4 exit |

**Consensus: YES on substance.** FA, DS, and PI converge on:
- Close EX-001 at G4 exit using MV-002 ProBook re-run (≤ 100ms) as evidence
- Remove AC-009 `test.fixme()` permanently
- Three PI Agent process conditions apply regardless of label

**Open Question 1 — resolution label for EL:**
FA allows "Resolved" if MV-002 ≤ 100ms; DS recommends "Won't Fix" preemptively.
Both outcomes use the same evidence and the same AC-009 disposition. The difference:

- **Resolved** signals the optimization achieved the original specification on the
  intended hardware. This is the stronger positive signal — the tool meets its own
  performance contract on real devices.
- **Won't Fix** signals a deliberate choice not to pursue CI-level enforcement, with
  an implicit acknowledgement that the spec is aspirational for CI environments.

This is an EL classification decision, not a technical one. Panel is neutral on the
label — both closures are process-compliant with PI conditions satisfied.

---

### Full consensus summary

| Decision | Consensus | Conditions for ADR-019 |
|---|---|---|
| 1 — Mode 2 column scope | **YES** | (a) "Enter Active Control" label, (b) subdued visual treatment, (c) two-component architecture |
| 2 — Shock taxonomy | **YES — all six in M18** | ADR-019 must specify parameter schemas + data dependency status for all six types before G4 sprint entry |
| 3 — EX-001 disposition | **YES on substance** | PI conditions required; EL decides label (Resolved vs. Won't Fix) |

**No dissenting findings.** All panel members reached compatible conclusions across
all three decisions. The open question on Decision 3 label is not a dissent — it is
a preference difference that the panel leaves to EL as the accountable decision-maker.

---

## Part IV — EL Decision Space

**What EL is deciding:**

1. **Decision 1:** Approve the panel recommendation — Mode 2 column 3 populated with
   read-only scenario summary + "Enter Active Control" button, two-component architecture,
   subdued visual treatment. OR amend any of the three ADR-019 conditions.

2. **Decision 2:** Approve all six shock types in M18, with ADR-019 parameter schema
   specification as a pre-G4-entry requirement. OR specify a deferred subset.

3. **Decision 3, substance:** Approve — close EX-001 at G4 exit via MV-002 re-run,
   remove AC-009 from CI permanently, PI conditions apply.

3. **Decision 3, label:** Choose **Resolved** (if optimization achieves ≤ 100ms local,
   per FA path) or **Won't Fix** (preemptive, per DS path). Both are process-compliant.

**EL records approval or amendment in**
`docs/process/intents/M18-GD-2026-06-26-control-plane-scope-decision.md §EL Approval Record`.

---

*Deliberation record authored: 2026-06-26. Panel findings represent agent deliberations
grounded in session-current project documents. Architect Agent (ADR-019 author) did not
participate in the panel — they receive this record as inputs.*
