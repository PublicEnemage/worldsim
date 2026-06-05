# Pillar 2 — Cold-Start Usability Audit Methodology

**Milestone 11.5 — Usability Validation and Experience Audit**

| | |
|---|---|
| Authors | UX Design Thinking Agent (§2–4), Product Owner Agent (§5–6), UX Designer Agent (§7–8), PM Agent (§1, §9) |
| Status | PROPOSED — awaiting joint approval (see §9) |
| Issue | #718 |
| Version | 1.0 (2026-06-04) |

---

## §1 — Purpose and Scope (PM Agent)

This document is the governing methodology for Pillar 2 usability audit sessions in
Milestone 11.5. No session may begin until this methodology has received joint approval
from PM, UX Designer, UX Design Thinking, and PO agents (see §9).

The methodology specifies:

- How sessions are configured and conducted under genuine cold-start conditions (§2)
- The think-aloud annotation schema (§3)
- The session facilitation approach from URL handoff to artifact production (§4)
- Which personas are tested, in what order, and what task each agent is given (§5)
- The minimum session count required for M11.5 findings to be actionable (§6)
- How the interaction trace is interpreted against the think-aloud record (§7)
- How findings are classified by severity and type (§8)

Sessions are conducted using the Pillar 1 instrumentation layer (PR #724). Each session
produces two artifacts: an rrweb interaction trace (written to `backend/sessions/`) and a
think-aloud transcript (produced by the agent). The combination is the unit of evidence
for M11.5 findings.

---

## §2 — Cold-Start Protocol (UX Design Thinking Agent)

### The cold-start requirement

A cold-start session is valid only if the agent has no prior operational knowledge of
WorldSim seeded in context at session start. This is the governing constraint on session
design — it is not a procedural nicety. An agent who knows that the instrument cluster
is in Zone 1, that the MDA alerts are in Zone 1B, or that scenarios must be created
before they can be explored has already broken the cold-start condition. The simulation
of first-contact confusion is not first-contact confusion.

**What constitutes a valid cold-start context:**

The agent's context at session start contains exactly:

1. Their persona identity and role context (who they are, what they know professionally)
2. The question they need to answer
3. The URL of the application

Nothing else. No description of WorldSim. No description of what the application does.
No pointer to any feature, panel, or navigation element. No explanation of what rrweb is
or that a recording is active.

**What breaks the cold-start condition:**

- Any prior session in the same conversation context that explored WorldSim
- Any description of WorldSim's architecture, layout, or features in the context
- Knowledge of the instrument cluster, zone layout, or MDA alert system
- Knowledge that the application is a simulation tool (rather than whatever the agent
  infers from the landing screen)

**Coordinator responsibility:**

The coordinator constructs the session URL (per `how-to-run-a-session.md`), assigns the
session ID, and prepares the task prompt (§5). The coordinator sends the agent exactly
the task prompt from Appendix A plus the URL — no additional framing. The coordinator
then observes silently.

### Session environment

- Frontend running at `http://localhost:5173`
- Backend running at `http://localhost:8000`
- Both must be confirmed running before the session URL is sent to the agent
- No pre-loaded scenario; the agent encounters the landing screen as a genuine first contact
- Recording is activated by the `?usability_session=<id>` URL parameter

### Time limit

Sessions have a hard 45-minute limit. If the agent has not clicked End Session within 45
minutes, the coordinator clicks End Session. The 45-minute limit is not communicated to
the agent in advance — it is a backstop, not a design constraint on the session.

---

## §3 — Think-Aloud Annotation Schema (UX Design Thinking Agent)

The think-aloud record is the agent's narration of their internal state during navigation.
It is produced inline — emitted at the moment of the corresponding cognitive event, not
reconstructed afterward. Post-hoc narration is not a valid think-aloud record.

### Core markers (from North Star)

```
[LOOKING FOR: ...]    What the agent is trying to find at this moment
[EXPECTED: ...]       What the agent thought would happen next
[FOUND: ...]          What the agent actually found
[CONFUSED: ...]       Where the interface did not match expectation
[GAVE UP ON: ...]     What the agent abandoned and why
```

### Extended markers (methodology addition)

Two markers are added to complete the schema. The North Star markers cover intent and
outcome but not action. The `[TRIED: ...]` marker fills the gap between intention and
observation. The `[CONCLUDED: ...]` marker closes the loop at task completion or
abandonment.

```
[TRIED: ...]          The specific action taken (what was clicked, typed, scrolled)
[CONCLUDED: ...]      The agent's summary finding at task completion or abandonment
```

### Usage rules

**Emit before acting, not after.** `[LOOKING FOR: ...]` precedes the navigation action.
`[FOUND: ...]` or `[CONFUSED: ...]` follows it. This ordering is what makes
synchronization with the rrweb event stream possible.

**Markers are not performance.** The agent should not be trying to produce well-formed
narration. The think-aloud record is evidence, not prose. Incomplete sentences,
interrupted thoughts, and corrections are valid data. Tidied narration is not.

**Every `[GAVE UP ON: ...]` requires a reason.** "I gave up on this" is not a finding.
"I gave up on this because I could not determine whether the number in the instrument
panel was the current value or a projected value, and I needed the current value to
make my argument" is a finding.

**Every `[CONCLUDED: ...]` states whether the task was completed.** "I concluded that I
had found what I needed" or "I concluded that I could not complete this task with the
information visible" — the verdict matters for findings classification.

### Example sequence

```
[LOOKING FOR: a way to see what happens to poverty if the fiscal multiplier is higher]
[TRIED: clicked "New Scenario" in the top navigation]
[FOUND: a form asking for country, date, and module configuration]
[EXPECTED: the form to have a field labelled "fiscal multiplier" or similar]
[CONFUSED: I see options for modules but no parameter controls; I don't know if I
           set the multiplier here or somewhere else]
[TRIED: opened "EcologicalModule" toggle to see if parameter fields appear]
[FOUND: a toggle but no parameters visible after enabling]
[GAVE UP ON: finding fiscal multiplier controls in the scenario creation form;
             will try creating a scenario first and looking inside it]
```

---

## §4 — Session Facilitation Approach (UX Design Thinking Agent)

### Session runner (updated 2026-06-05)

Two session runners exist. The **Interactive Playwright loop** is the canonical default:

| Runner | Script | Requirement | When to use |
|---|---|---|---|
| Interactive Playwright loop | `scripts/run_usability_session_interactive.py` | Python + Playwright only; no API key | **Default.** Claude Code drives the browser via Playwright in the same terminal session. Think-aloud is produced inline. Artifact handoff is manual (coordinator saves transcript). |
| Computer-use runner | `scripts/run_usability_session.py` | `ANTHROPIC_API_KEY` + Anthropic API credits | When you need a fully autonomous headless run without coordinator involvement. Requires API credits — not free. |

**The Interactive Playwright loop is the default because:**
- Requires no API key or credits — accessible to any contributor
- Claude Code controls the browser directly via Playwright, producing the think-aloud transcript inline
- The coordinator can observe in real time and take field notes
- Sessions completed in M11.5 all used this runner

The computer-use runner exists for fully automated batch runs when API access is available; it is not the canonical method and should not be assumed as the default by future coordinators.

### Before the session

1. Coordinator assigns a session ID in the format `YYYY-MM-DD-<persona-id>-<seq>`.
   Example: `2026-06-04-persona-2-001`

2. Coordinator constructs the session URL:
   ```
   http://localhost:5173/?usability_session=<session_id>&persona=<persona_id>&use_case=<use_case_label>
   ```

3. Coordinator verifies that backend and frontend are running and that the session URL
   activates the red recording banner before handing off to the agent.

4. Coordinator prepares a fresh agent context containing exactly the task prompt from
   Appendix A for the assigned persona — no additional framing.

### Handoff

The coordinator sends the agent:

1. The task prompt from Appendix A (verbatim — do not paraphrase or supplement)
2. The session URL

Nothing else. The agent is not told: what WorldSim is, that a recording is active, that
there is a red banner, what the session ID means, or what the expected navigation path is.

### During the session

The coordinator observes silently. The coordinator does not:

- Answer questions about the interface
- Confirm or deny that the agent is on the right track
- Point to features or hint at navigation paths
- Correct misunderstandings about what the tool does

If the agent asks the coordinator a direct question, the coordinator responds with exactly:
"I can't help with that — navigate as you would if you were alone."

The coordinator takes timestamped field notes on:
- Moments of extended hesitation (>30 seconds without a navigational action)
- Expressions of surprise (positive or negative)
- Moments where the agent appears to have found what they were looking for
- Any moment where the agent seems to be choosing between two paths

### Closing the session

The session ends when one of the following occurs:

1. **Agent clicks End Session** — the agent has declared the task complete or abandoned
2. **Agent emits `[CONCLUDED: ...]`** — the agent's verdict is on record; coordinator
   clicks End Session on the agent's behalf
3. **45-minute limit reached** — coordinator clicks End Session; agent did not finish

After End Session is clicked:
- The interaction trace artifact is written to `backend/sessions/<session_id>.json`
- The coordinator saves the think-aloud transcript alongside the artifact
- The coordinator writes a one-paragraph field note capturing the coordinator's
  direct observation of the session (what was unexpected, what was smooth, any
  moment the coordinator would highlight for the findings review)

### Artifact package

Each session produces:

| Artifact | Location | Author |
|---|---|---|
| rrweb interaction trace | `backend/sessions/<session_id>.json` | Pillar 1 instrumentation |
| Think-aloud transcript | `docs/ux/usability-sessions/transcripts/<session_id>-transcript.md` | Agent |
| Coordinator field notes | `docs/ux/usability-sessions/transcripts/<session_id>-field-notes.md` | Coordinator |

The three artifacts together constitute the session record. A session with a missing
transcript or field notes is incomplete and cannot produce a valid finding.

---

## §5 — Persona Sequencing and Task Design (PO Agent)

### Sequencing rationale

Persona sessions are sequenced by the severity of failure that cold-start breakdown
represents for each persona. The persona for whom a Layer 3 failure is most consequential
runs first.

**Priority A — must run in M11.5 (ordered):**

| Position | Persona | Why this position |
|---|---|---|
| 1 | Persona 2 — Finance Ministry Negotiator | Core beneficiary. If the tool fails here, it fails at its stated mission. The 90-minute reactive window makes cold-start legibility existential. |
| 2 | Persona 1 — Programme Analyst | Domain expert who will stress the analytical layer. Surfaces failures a technical user encounters — different failure surface than Persona 2. |
| 3 | Persona 5 — Institutional Decision-Maker | Most demanding Layer 3 test: 5-minute window, non-economist, executive context. Surfaces whether the instrument cluster is self-interpreting. |

**Priority B — run if capacity allows (unordered):**

| Position | Persona | Why priority B |
|---|---|---|
| 4 | Persona 6 — Investigative Journalist | Plain-language test. Surfaces whether a non-analyst can produce a citable sentence from the MDA alert panel without specialist mediation. |
| 5 | Persona 8 — Civil Society Monitor | Accountability tracking sub-mode. Tests a use pattern the platform partially serves and partially doesn't — surfaces the boundary. |

Personas 3, 4, 7, and 4V are deferred to the next usability cycle. Their canonical use
cases require capabilities (comparison mode, backtesting interface, export) that M11.5
is testing rather than assuming.

### Task prompts

Task prompts are in Appendix A. Each prompt is the complete text sent to the agent at
session start — verbatim. Prompts are designed with three properties:

1. **Role-grounded:** The agent is given their persona's identity and professional
   context, not just a label
2. **Question-anchored:** The agent is given a specific question they need to answer,
   not a task description ("use the simulation to find X")
3. **Stakes-present:** The prompt communicates why the answer matters — the negotiation,
   the vote, the story — so the agent's urgency is calibrated to the persona's reality

Prompts do not contain: the word "WorldSim," any description of what the tool does,
any navigation guidance, or any hint that a specific feature will answer the question.

---

## §6 — Session Count (PM Agent + PO Agent)

### M11.5 minimum

The minimum for M11.5 is **one session per Priority A persona** — three sessions total.

**Rationale:**

Standard usability literature (Nielsen 1993) identifies ~85% of usability issues with
five human participants. Agent sessions differ from human sessions in one important
respect: an AI agent is more consistent within a persona archetype than an individual
human participant, which reduces within-persona variance. A second session with the same
persona in the same context would surface within-persona variance (how the same cognitive
profile responds on a different attempt) rather than between-persona variance (how
different user types encounter different failure surfaces).

M11.5's primary goal is to identify **systemic Layer 3 failures** — failures that occur
across the core user types this tool was built for. One session per Priority A persona
surfaces three distinct failure surfaces with three distinct cognitive profiles, which
is sufficient evidence to identify systemic failures and produce actionable findings for
M12 prioritization.

A second session per persona is warranted if Session 1 produces ambiguous findings (the
`[CONCLUDED: ...]` marker is absent or inconclusive, or the coordinator field notes
identify session-specific confounds). The decision to run a second session is made by PM
Agent after Session 1 findings are reviewed.

### Per-session evidence standard

A session produces a valid finding if:

- The interaction trace is complete (Start Session → End Session with events captured)
- The think-aloud transcript contains at least one marker from each of: `[LOOKING FOR:]`,
  `[FOUND:]` or `[CONFUSED:]`, and `[CONCLUDED:]`
- The coordinator field notes are written

A session that does not meet this standard is recorded as incomplete and may be re-run
with the same persona using a new session ID.

---

## §7 — Interaction Trace Interpretation (UX Designer Agent)

### Segmentation

The rrweb event stream is segmented by the timestamps of think-aloud markers. Each
segment runs from one marker to the next and represents a unit of navigational intent:
what the agent was trying to do, expressed as a sequence of interface actions.

The rrweb event types relevant to interpretation:

| Event type | Interpretation signal |
|---|---|
| Mouse movement → click on element | Intentional navigation action |
| Mouse movement with no click for >20s | Hesitation or reading; not action |
| Click on non-interactive element | Discoverability failure (expected interactivity) |
| Rapid back-navigation (<30s round trip) | Path abandoned; confusion |
| Scroll → no further action for >15s | Lost in page; no obvious next step |
| Same element clicked twice within 10s | Expected different response |

### Confusion signals

A confusion signal is a trace pattern that indicates the interface did not produce the
expected result. Confusion signals are the primary mechanism for locating where think-aloud
`[CONFUSED: ...]` and `[GAVE UP ON: ...]` markers originate in the trace.

| Signal | Definition | Severity indicator |
|---|---|---|
| Dead click | Click on non-interactive element | Discovery failure |
| Rapid return | Navigate away and return within 60s | Path failure |
| Hover accumulation | >30s on one element without action | Legibility failure |
| Abandonment | `[GAVE UP ON: ...]` marker followed by silence | Task failure |
| Repeated attempt | Same interaction repeated >2x | Feedback failure |

### Synchronization

The coordinator field notes provide human-observed timestamps for moments of surprise,
hesitation, and resolution. Where field note timestamps overlap with trace confusion
signals, the overlap is a high-confidence finding location — the agent's internal state
and the trace both indicate breakdown at the same moment.

---

## §8 — Findings Classification (UX Designer Agent)

### Severity

| Severity | Definition |
|---|---|
| CRITICAL | Task abandoned or goal impossible — the persona cannot achieve their canonical use case |
| HIGH | Task completed with >3 confusion markers, or with a workaround the persona would not have found independently |
| MEDIUM | Task completed with 1–3 confusion markers, or with a navigation path significantly longer than optimal |
| LOW | Incidental friction — the task was completed efficiently but a specific element was confusing or suboptimal |

### Classification dimensions

Each finding is classified along three dimensions:

**Discovery** — Can the user find the feature?
A Discovery finding means the capability exists but the user could not locate it from
the landing screen under cold-start conditions. The capability is present; the path to
it is not legible.

**Comprehension** — Can the user understand the output?
A Comprehension finding means the user reached the output but could not interpret it
accurately enough to answer their question. The output is present; its meaning is not
self-interpreting.

**Action** — Can the user act on what they found?
An Action finding means the user understood the output but could not use it to make a
decision or produce a deliverable (a negotiating position, a citable sentence, a board
briefing). Understanding is present; the path from understanding to action is broken.

A finding may carry more than one dimension. A feature that is hard to find AND hard to
interpret carries both Discovery and Comprehension.

### Finding format

Each finding in the session findings document uses this structure:

```
## FINDING-<session_id>-<nn>

Severity: CRITICAL | HIGH | MEDIUM | LOW
Dimension: Discovery | Comprehension | Action (one or more)
Persona: <persona_id>
Session: <session_id>
Component: <semantic vocabulary reference — e.g. "Zone 1B / MDA alert severity badge">
Canonical use case: <use_case_label>

**Observation:** One sentence describing what happened in the trace.

**Evidence:**
- Think-aloud: `[marker text]` (timestamp ~HH:MM from session start)
- Trace: <confusion signal type> at <component reference> (~HH:MM)
- Field notes: <coordinator observation>

**Implication:** What this finding means for the persona's ability to achieve their goal.

**M12 action:** What would close this finding (design change, copy change, navigation change).
```

### Session findings document

Each session produces one findings document at:
`docs/ux/usability-sessions/findings/<session_id>-findings.md`

The session findings document is authored by UX Designer with PM triage review. It is
produced within 48 hours of the session. Findings from all Priority A sessions are then
synthesized into the M11.5 findings report (separate artifact, PM R).

---

## §9 — Joint Approval Gate (PM Agent)

This methodology document must receive explicit approval from all four assigned agents
before Session 1 begins. Approval is recorded as a comment on GitHub Issue #718.

| Agent | Role in approval | Status |
|---|---|---|
| UX Design Thinking Agent | §2–4: cold-start protocol, annotation schema, facilitation | PROPOSED |
| Product Owner Agent | §5–6: persona sequencing, task design, session count | PROPOSED |
| UX Designer Agent | §7–8: trace interpretation, findings classification | PROPOSED |
| PM Agent | §1, §9: coordination, gate | PROPOSED |

Session 1 may not begin until all four statuses read APPROVED and that approval is
recorded on Issue #718.

---

## Appendix A — Task Prompts

These prompts are sent verbatim to the agent at session start. No additional text.
No description of WorldSim. No navigation guidance.

---

### Persona 2 — Finance Ministry Negotiator

**Session task prompt:**

You are Eleni Papadopoulos, Deputy Finance Minister of Greece. The year is 2012.
The Troika — IMF, ECB, and European Commission — has just circulated a draft
conditionality package for Greece's second bailout. The package includes minimum wage
cuts of 22%, further pension reductions, and an accelerated privatisation schedule.
Your negotiating session begins in the morning. You have tonight to identify which
specific terms cross human cost thresholds — and to build a counter-proposal that
achieves the same fiscal consolidation target while protecting the cohorts most
vulnerable to the proposed measures.

You have been given access to an analytical tool. Use it to answer this question:
**Which specific terms in the conditionality package drive critical threshold crossings,
at which step, and for which cohorts — and what is the minimum modification that avoids
those crossings?**

Here is the URL: [COORDINATOR INSERTS SESSION URL]

---

### Persona 1 — Programme Analyst

**Session task prompt:**

You are Lucas Ferreira, Country Economist at the IMF Fiscal Affairs Department. You are
building the Article IV consultation for a mid-size European economy facing early-stage
fiscal stress. The programme design your team is developing assumes a fiscal multiplier
of 0.5 — the IMF consensus estimate. You have seen internal literature suggesting the
true multiplier may be closer to 1.5. Before the design meeting tomorrow, you want to
understand what the difference means for human development threshold crossings.

You have been given access to an analytical tool. Use it to answer this question:
**What happens to poverty headcount and health system capacity threshold crossings if
the fiscal multiplier is 1.5 instead of 0.5 — at which step, and in which income
cohort does the difference become critical?**

Here is the URL: [COORDINATOR INSERTS SESSION URL]

---

### Persona 5 — Institutional Decision-Maker

**Session task prompt:**

You are an Executive Director at the IMF, representing a developing-country
constituency. The Executive Board session on the Greek programme resumes in 5 minutes.
You have read the 80-page staff report. You are not an economist. Your question going
into the room is whether the financial recovery the programme is producing is being
purchased at proportionate or disproportionate human cost — and whether there were
alternative paths.

You have been given access to an analytical tool. Use it to answer this question:
**Has the Greek programme produced financial recovery and human development deterioration
simultaneously — and if so, was that tradeoff avoidable?**

Here is the URL: [COORDINATOR INSERTS SESSION URL]

---

### Persona 6 — Investigative Journalist

**Session task prompt:**

You are Farida Haidari, economics correspondent at Dawn in Karachi. Pakistan is under
IMF conditionality. Energy subsidies were removed in June 2022. One month later, the
worst floods in Pakistan's recorded history began — submerging one-third of the country
and destroying agricultural livelihoods across Sindh and Balochistan. The IMF's
targeted subsidy scheme was designed to protect the bottom quintile from subsidy removal.
It was not designed for a simultaneous 30% agricultural income collapse.

You have been given access to an analytical tool. You have two hours before your editor
deadline. Use it to answer this question:
**Did Pakistan's IMF programme design expose the bottom-quintile population to a combined
shock — subsidy removal plus flood income loss — that crossed a critical human cost
threshold it was explicitly designed to prevent?**

Here is the URL: [COORDINATOR INSERTS SESSION URL]

---

### Persona 8 — Civil Society Monitor

**Session task prompt:**

You are Abena Osei, research coordinator at SEND Ghana in Accra. Ghana is in its fourth
year under an IMF ECF programme. The programme includes a social protection floor
commitment — a guaranteed minimum level of social transfers. You have field data from
three northern regions suggesting the floor is not being maintained in practice. Before
your quarterly report to the board, you want to understand whether the programme's
design includes the specific commitments your field data is measuring against.

You have been given access to an analytical tool. Use it to answer this question:
**Does the programme design include a verifiable social protection floor commitment —
and does the simulation show whether it is being maintained across the programme steps?**

Here is the URL: [COORDINATOR INSERTS SESSION URL]

---

## Appendix B — Transcript Template

Save at: `docs/ux/usability-sessions/transcripts/<session_id>-transcript.md`

```markdown
# Think-Aloud Transcript — <session_id>
# Persona: <persona_id>
# Date: YYYY-MM-DD
# Canonical use case: <use_case_label>
# Session duration: MM:SS

[TRANSCRIPT BEGINS]

MM:SS [LOOKING FOR: ...]
MM:SS [TRIED: ...]
MM:SS [EXPECTED: ...]
MM:SS [FOUND: ...]   OR   [CONFUSED: ...]
...
MM:SS [CONCLUDED: ...]

[TRANSCRIPT ENDS]
```

Timestamps are minutes:seconds from session start (when the URL was first loaded).
Emit markers inline — do not reconstruct after the session.
