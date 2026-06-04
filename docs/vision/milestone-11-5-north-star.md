WorldSim Milestone 11.5 — Usability Validation and Experience Audit
North Star Document
Version 1.0 — 2026-06-04
Status: Governing intent document. Methodology to be proposed by assigned agents.

Why This Milestone Exists
WorldSim has been built by people who understand it deeply. The analytical capability is substantial — four frameworks, a crisis arc instrument cluster, an MDA alert system, a political economy module, two validated country fixtures. The personas who should use this tool are defined. Their canonical use cases are documented.
What has not been done is put the tool in front of those personas under conditions that resemble reality — a finance ministry analyst, no orientation, a question they need to answer, a negotiation they're preparing for — and watched what happens.
This milestone answers the question that all the other milestones assumed: can the people this tool is designed for actually use it?

The Three Questions We Are Trying to Answer
1. What can a user actually access?
Not what the engine computes — what a real user, entering with a question and no prior knowledge of WorldSim, can find, understand, and act on. The gap between engine capability and user-accessible capability is the first thing this milestone measures.
2. Where does the experience break down?
At what point in each persona's canonical use case does the interface stop being legible? Where does a user have to already know the answer in order to find the answer?
3. Did we plant the right tree?
Some foundational design decisions were made before the personas were fully defined. With eight defined personas and their canonical use cases now documented, do those decisions serve the people we built this for — or have we built an instrument cluster for specialists and retrofitted it for everyone else?

What This Milestone Is Not
This milestone does not ship features. It does not optimize what exists. It surfaces what is and is not working — and produces the evidence base that determines what M12 and beyond should prioritize. A finding that suggests a foundational design decision was wrong is a success, not a failure. The goal is honest assessment, not validation of prior choices.

Three Pillars
The assigned agents are asked to design the methodology for each pillar. The pillars are named here as intent, not prescription.
Pillar 1 — Instrumentation
The usability audit requires the ability to capture what an agent actually does when navigating the live application — not screenshots, not described behavior, but a full interaction trace: mouse movement, clicks, scrolls, the sequence of actions, the timing between them.
The equivalent in traditional usability research is the combination of screen recording and eye tracking. For WorldSim, the equivalent is session replay technology embedded in the frontend, combined with agent navigation through a live browser interface.
The instrumentation must be:

Self-hosted and privacy-preserving — no third-party session data
Lightweight — enabled for usability sessions without affecting normal use
Timestamped — every event carries a timestamp that can be synchronized with other session artifacts
Replayable — sessions can be reviewed after the fact, scrubbed to specific moments, shared as artifacts

The instrumentation layer is a technical prerequisite for Pillar 2. It must exist before the first usability session runs.
Pillar 2 — Cold-Start Usability Audit with Think-Aloud Protocol
The sessions themselves. Persona agents navigate the live application via a live browser interface, attempting their canonical use case from a cold start — no orientation, no briefing on what WorldSim is or how it works, only their role context and the question they need to answer.
Each session captures two simultaneous streams:
The interaction trace — produced by the instrumentation layer. What the agent did, in sequence, with timing.
The think-aloud narration — produced by the agent. What the agent intended, expected, observed, and concluded at each moment. The narration uses structured intent markers that can be timestamped and synchronized with the interaction trace:

[LOOKING FOR: ...] — what they are trying to find
[EXPECTED: ...] — what they thought would happen
[FOUND: ...] — what they actually found
[CONFUSED: ...] — where the interface did not match expectation
[GAVE UP ON: ...] — what they abandoned and why

The combination of interaction trace and synchronized think-aloud narration is the focus-group camera equivalent — not just what the user clicked, but why, and what they thought was supposed to happen instead.
Sessions must be conducted under genuine cold-start conditions. Agents who already understand WorldSim's architecture cannot simulate first-contact confusion. The methodology must account for this.
Pillar 3 — Session Provenance and the Usability Evidence Record
A usability finding is empirical evidence, not an anecdote. For findings to be comparable across sessions, versions, and agents, every session must be precisely documented at the moment it runs — not reconstructed afterward.
The assigned agents are asked to design a session manifest standard that captures, at minimum:
Application state: What version of WorldSim was running. What commit. What features were enabled. What modules were active.
Agent configuration: Which agent conducted the session. Which persona they embodied. What canonical use case they were attempting. What task or question they were given. Whether the session was cold-start or oriented.
Environmental conditions: Viewport, browser, stack configuration.
Session identity: A unique session ID that links the interaction trace, the think-aloud transcript, and any findings document produced from the session.
The standard must also include a semantic component vocabulary — a naming system for WorldSim's interface components at multiple levels of granularity (zone, component, element) so that findings can be precisely located and compared across sessions. A finding that references "Zone 1B" is less useful than one that references "the MDA alert severity badge in the governance row of the alert panel." The vocabulary must exist before the first session runs.
The provenance standard should be established as a project artifact, versioned alongside the application, so that a finding produced today is fully interpretable six months from now under a different application version by an agent who was not present for the original session.

The Output of This Milestone
Primary deliverable: A structured findings document for each persona session, triaged by severity, linked to session IDs, and referencing the semantic component vocabulary. Findings are empirical evidence with full provenance.
Secondary deliverable: A repeatable methodology — the cold-start protocol, the think-aloud annotation schema, the session manifest standard, the semantic component vocabulary — documented as a project artifact and runnable at every even-numbered milestone alongside the demo.
Tertiary deliverable: An updated feature catalogue — a complete inventory of what WorldSim can do, how each capability is accessed, which persona it serves, and whether the current UI makes that capability discoverable without assistance.

The Exit Criterion
After Milestone 11.5, the project should be able to answer: can a finance ministry analyst with no prior WorldSim orientation use this tool to produce a finding they could cite in a negotiation?
If the answer is yes, with evidence from the sessions, M12 proceeds with confidence. If the answer is no, or partially, the findings document tells us exactly where the gaps are and what M12 must address before Mode 3 (Active Control) is built on top of an interface that hasn't been validated for its intended users.

Assigned Agents
The following agents are asked to review this North Star document and jointly propose the methodology for each pillar. The proposal should specify the process, the artifacts, the tooling, and the sequencing — without being constrained by what has been done before. The North Star is the destination. The methodology is yours to design.

PM Agent — overall methodology coordination, session scheduling, findings triage
UX Designer Agent — semantic component vocabulary, interaction trace interpretation, findings classification
UX Design Thinking Agent — cold-start protocol design, think-aloud annotation schema, session facilitation approach
Product Owner Agent — feature catalogue structure, acceptance criteria for the exit criterion, persona-to-use-case mapping

The Frontend Architect Agent and Data Architect Agent should be consulted on Pillar 1 (instrumentation architecture) and Pillar 3 (session manifest schema) respectively before those designs are finalized.

What This Milestone Does Not Prescribe

The specific tooling for session replay (beyond the instrumentation requirements stated above)
The format of the session manifest
The structure of the semantic component vocabulary
The number of sessions per persona
The order in which personas are tested
The specific questions or tasks given to each agent

These are methodology decisions. They belong to the assigned agents.

The North Star is the question. The methodology is the answer the agents are being asked to design.
