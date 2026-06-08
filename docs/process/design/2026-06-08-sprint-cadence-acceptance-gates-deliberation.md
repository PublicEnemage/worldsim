# Design Deliberation — Sprint Cadence, Acceptance Gates, Agent Execution Protocol, and Session Boundary Discipline

**Date:** 2026-06-08  
**Status:** Pre-endorsement — deliberation complete, EL endorsement pending  
**Session:** M12 active / release/m12  
**Participants:** Engineering Lead, PI Agent, Business PO Agent, PM Agent  
**No files were created or modified during this deliberation.** Implementation is blocked pending EL endorsement of the sequencing plan.

---

## Engineering Lead — Intent Prompt

**Intent: Sprint Cadence, Acceptance Gates, Agent Execution Protocol, and Session Boundary Discipline**

**Background**

WorldSim has developed strong delivery discipline — ADRs, near-miss registry, compliance scans, sprint plans — but M12 revealed a structural gap between delivery and verification. Features were merged and marked done without anyone with accountability for the product's mission verifying that they worked as intended, in the interface where they're supposed to work, serving the user they're supposed to serve. The Demo 4 failure was the clearest symptom: a demo script shipped as a document, not as a demonstrated capability. Individual PRs passed CI. The milestone as a whole failed its primary purpose.

Three contributing causes:

First, the usability audit findings went directly to issue creation and implementation without a strategic review of what they meant for the product's direction. The step that was skipped was synthesis before action.

Second, there is no definition of done that requires a real human or a real agent to verify that a feature works as intended in the live application. Done currently means merged and CI green. That is a necessary condition, not a sufficient one.

Third, the quarterback function — holding the full picture of what is in flight, what is blocked, and what the next move is — has been living implicitly in Claude Code's context window rather than explicitly in written documents. As sessions lengthen and context compacts, this degrades silently. The M12 sprint ran continuously across what should have been natural verification boundaries, accumulating work without accumulating accountability.

**What needs to change**

1. **Sprint cadence as a formal milestone subdivision**

Issue groups, as practised in M12, should become formal sprints within a milestone. Each sprint has a defined scope, a defined entry document, and a defined exit gate. The next sprint does not open until the current sprint's exit gate passes. The PM Agent owns sprint planning and sprint review orchestration, consulting the Business PO, UX Designer, and Development Economist as standing sprint review participants. The PI Agent owns the integrity of the sprint boundary — ensuring the entry and exit invariants are enforced and filing a near-miss if a sprint opens without a complete entry document or closes without complete exit artifacts.

2. **Business PO acceptance as a mandatory sprint exit gate**

A sprint is not done when issues are closed and CI is green. A sprint is done when the Business PO has verified the delivered capability in the live application. The Business PO acceptance protocol must define what verification looks like for different types of work: frontend features require UI demonstration, backend capabilities require observable output in the application, documentation requires legibility confirmation from a non-author. The Business PO can reject a sprint, which opens an exception path — findings are filed, remediation is scoped, and the sprint does not close until acceptance is granted. The PI Agent should co-author this protocol because it is a process integrity question: what does it mean for work to be genuinely complete, and what are the consequences when the gate is skipped or weakened.

3. **Agent execution protocol — a shared definition of done**

Every agent, regardless of role, should operate with a consistent execution lifecycle when handling a piece of work: Plan, Execute, Verify (does the output match the intent?), Validate (does the output serve the mission?), and either Accept or escalate via a defined exception path. Right now agents produce artifacts but the Verify and Validate steps are implicit, optional, or absent. This needs to be made explicit — either as a shared section in CLAUDE.md that all agents inherit, or as a base protocol referenced in each agent definition in agents.md. The PI Agent should author this protocol in consultation with the PM Agent, QA Lead, and Business PO. The Architect Agent should be consulted on how the protocol interacts with existing compliance gates.

4. **Session boundary discipline — sprints and milestones**

Claude Code's context window is a working surface, not a memory store. The quarterback function — knowing what is in flight, what is blocked, what the next move is — must live in written documents, not in accumulated context. Two invariants must be enforced at every level:

Entry invariant: If it isn't written down, it doesn't exist. A new sprint session reads only from written documents. A sprint entry document must be complete before the session opens. A new milestone reads only from the roadmap, the previous milestone's exit artifacts, and the HORIZON sweep findings. Anything not captured in writing before a session or milestone opens does not exist for that session or milestone.

Exit invariant: If it wasn't written down, it never happened. A sprint session ends only when all exit artifacts are written and complete — the sprint review artifact, the SESSION_STATE update, the sprint plan status, any near-miss filings. A milestone ends only when the exit checklist is complete and the EL has merged the release branch to main. Anything not written before the session closes or the merge happens did not happen.

The practical enforcement mechanism: each sprint starts in a fresh Claude Code session. The previous session's exit artifacts are the new session's only context beyond the permanent documents. This is not a convenience — it is the architectural decision that prevents implicit dependency on long-running context from becoming a compounding liability. The PI Agent should file a near-miss if a sprint opens without a complete entry document, or if a session closes with deferred exit artifacts.

The three levels and their natural enforcers:

- Sprint — Claude Code session boundary. Fresh session enforces entry. Exit artifacts required before session closes.
- Milestone — EL merge boundary. Release branch enforces entry (main is clean). Exit checklist and merge enforces exit.
- Product — Founding document and roadmap. These exist before any milestone opens and survive every session reset.

**The north star test**

Before any implementation begins, the PI Agent and Business PO should answer one question together and post their findings as a joint assessment: if M12 had included these four mechanisms, at which point would the Demo 4 failure have been caught, and by whom? If the answer is not "before the internal demo," the mechanisms are not strong enough.

**Sequencing**

No files should be created or modified until the following sequence is complete:

1. PI Agent and Business PO answer the north star test question jointly and post their assessment.
2. PM Agent proposes a sequencing plan for the four changes — which agents author which documents, in what order, and what the review chain looks like before anything is committed to the repository.
3. PI Agent reviews the sequencing plan for integrity.
4. EL endorses the sequencing plan.

The goal is to design the process correctly before encoding it. The agents designing this protocol should themselves follow the protocol they are designing — deliberate, reviewed, sequenced, written down before acted upon.

---

## Step 1: PI Agent + Business PO — Joint North Star Assessment

**Process Integrity Agent** and **Business PO Agent** activating for joint assessment. The north star test: *If M12 had included these four mechanisms, at which point would the Demo 4 failure have been caught, and by whom?*

### What actually failed in Demo 4

Before answering the north star question, we must be precise about the failure. There were two critical defects and one infrastructure gap:

- **DEMO4-001:** `ExternalSectorModule` (PR #773, G5) emitted `import_price_inflation` events, but no downstream consumer translated those events into `reserve_coverage_months` changes. Reserves were seeded at scenario start and never modified. The module was marked done. No one ran the engine and verified that the attribute it was supposed to affect actually moved.

- **DEMO4-002:** `MacroeconomicModule` had no Okun's law channel. GDP changed; unemployment did not follow. Same root structure: the feature was wired at one end but untested at the other end.

- **DEMO4-009:** The demo script was broken in the ASGITransport path — pool not initialized, database unreachable. The script had never been run against a live database before internal demo day.

The unifying root cause: **"done" was defined as "code merged and CI green."** The question "does the output match the analytical intent?" was never asked.

### Tracing each mechanism

**Mechanism 3 — Agent execution protocol (Verify + Validate steps)**

This is the earliest-catching mechanism. It operates at the individual PR level, before sprint boundaries or acceptance gates come into play.

If the implementing agent for G5/PR #773 had a mandatory Verify step — *does the output match the intent?* — they would have been required to demonstrate that a commodity price shock produced a visible change in `reserve_coverage_months`. Running the engine post-implementation, before opening the PR, would have immediately shown reserves frozen at the seeded value across all steps. The PR couldn't have been opened with an honest Verify attestation attached.

**Catch point: PR #773, G5 implementation phase, before the PR was opened.**  
**Caught by: the implementing agent.**  
**Timing: weeks before the internal demo.**

**Mechanism 2 — Business PO acceptance as sprint exit gate**

G5 closed when PR #773 merged. If Business PO acceptance required observable output in the running application — specifically, running a scenario and verifying that a commodity price shock produced reserve drawdown — the acceptance gate would have failed immediately. Reserves frozen at 7.1 months across all 8 steps is an unambiguous analytical failure. The Business PO would reject.

**Catch point: G5 sprint exit, Business PO acceptance.**  
**Caught by: Business PO.**  
**Timing: before G6 opened, well before the internal demo.**

**Mechanism 1 — Sprint cadence with formal exit gate**

The sprint exit artifact for G5 would need to include a statement like: *"ExternalSectorModule verified — commodity price shocks produce observable reserve drawdown in the running engine."* That sentence cannot be written honestly when reserves are frozen. The exit artifact requirement creates a forcing function: either the verification is done and written down, or the sprint cannot close.

**Catch point: G5 sprint exit artifact.**  
**Caught by: PM Agent (exit orchestration) or PI Agent (entry invariant enforcement on G6).**  
**Timing: same as mechanism 2.**

**Mechanism 4 — Session boundary discipline**

This mechanism addresses a different failure mode — the degradation of the quarterback function across sessions. It does not directly catch DEMO4-001/002, but it closes a secondary gap: the implicit assumption that "G5 is done" could not persist unchallenged across a session boundary if G6's entry document required an explicit reference to G5's completed exit artifacts. If those artifacts didn't exist, G6 couldn't open.

**Catch point: G6 sprint entry — secondary backstop.**  
**Caught by: PI Agent (entry invariant enforcement).**  
**Timing: indirect; surfaces missing G5 exit artifacts when G6 tries to open.**

### Verdict

The mechanisms are sufficient. The north star test passes.

The Demo 4 failure would have been caught:
- **First** by mechanism 3 (execution protocol Verify step) — before PR #773 was opened, by the implementing agent.
- **Second** by mechanism 2 (Business PO acceptance) — at G5 sprint exit, by the Business PO.
- **Third** by mechanism 1 (sprint exit artifact requirement) — same timing as mechanism 2.
- **Fourth** by mechanism 4 (session boundary discipline) — when G6 tried to open without G5's exit artifacts, by PI Agent.

All four catch points precede the internal demo. The mechanisms are not redundant — they operate at different levels and catch different failure modes. Mechanism 3 catches implementation defects before merge. Mechanism 2 catches analytical defects that survive merge. Mechanism 1 creates institutional record that prevents silent sprint close. Mechanism 4 prevents cross-session amnesia from compounding missed catches.

**One integrity caveat from PI Agent:** Mechanism 3 only catches failures during sessions where agents actually execute the Verify step. It is not self-enforcing — it depends on agents treating the lifecycle as a genuine gate, not a checkbox. This is why mechanisms 1 and 2 are not redundant: they provide external verification of the internal lifecycle's completeness. A process that relies solely on self-attestation has a known failure mode. The three-level redundancy (agent self-verify, Business PO acceptance, sprint exit artifact) compensates for that.

**One mission-grounding note from Business PO:** DEMO4-001 and DEMO4-002 were not just technical defects. The reserve drawdown arc and the unemployment response to fiscal austerity are the primary human cost signals in Demo 4. The finance minister in Amman watching reserves drain in the instrument cluster — that is the product's thesis made visible. Shipping a demo where those signals were frozen was not just a CI failure; it was a mission failure. The Business PO acceptance gate exists specifically to prevent technically-green work from being mission-incomplete. This is why the acceptance protocol must be authored against the mission — not against test coverage metrics.

---

## Step 2: PM Agent — Sequencing Proposal

**PM Agent activating.** Before proposing sequence, one architectural observation: mechanism 3 (execution protocol) is the foundation. Mechanisms 1 and 2 reference what "verified" means — they cannot be written clearly until mechanism 3 defines the Verify/Validate steps. Mechanism 4 (session boundary discipline) is the container for all three. The sequencing follows naturally from this dependency structure.

### Proposed sequence

**Phase A — Foundation (mechanism 3)**

**What:** Author the shared agent execution lifecycle — Plan / Execute / Verify / Validate / Accept-or-escalate.

**Who authors:** PI Agent.  
**Consultations required before first draft:**
- PM Agent: milestone coordination impact — how does the Verify step interact with PR merge gates and session end timing?
- QA Lead: how does the execution lifecycle align with existing test gates? The Verify step must not duplicate what CI already enforces, and must not be satisfiable by CI alone.
- Business PO: what does "Validate" mean for different work types? (Frontend feature: observable in UI. Backend capability: observable in application output. Documentation: legible to a non-author. Analytics: output matches analytical intent.)
- Architect Agent: how does the lifecycle interact with existing compliance gates in CLAUDE.md §Architectural Principles?

**Where it lands:** A new section in CLAUDE.md — shared by all agents, not in any single agent definition. Every agent operating in this codebase inherits the lifecycle.

**Review chain:** PM Agent (milestone coordination check) → Architect Agent (compliance gate alignment) → EL endorsement.

**Output artifact:** Draft text for CLAUDE.md §Agent Execution Lifecycle (not committed until EL endorses the sequencing plan and the draft clears its review chain).

---

**Phase B — Acceptance definition (mechanism 2)**

**What:** Define what Business PO acceptance looks like for each work type, and what the exception path is when acceptance is rejected.

**Who authors:** Business PO (verification criteria by work type). PI Agent co-authors the integrity enforcement language and the exception path.  
**Consultations required:**
- PM Agent: sprint scheduling impact — how much time is built into a sprint for the acceptance cycle?
- UX Designer: what UI verification requires (viewport, user state, interaction sequence) so acceptance criteria are precise, not vague.
- The execution lifecycle (Phase A output) is a prerequisite — the acceptance protocol references the Validate step's output.

**Where it lands:** Two places. (1) New ACCEPT mode in agents.md §Business Product Owner Agent. (2) Amendment to sprint-planning-sop.md §Sprint Exit Gate.

**Review chain:** PI Agent (integrity check — does the exception path have teeth?) → PM Agent (feasibility) → EL endorsement.

---

**Phase C — Sprint cadence formalization (mechanism 1)**

**What:** Define the sprint entry and exit document templates; make sprint boundary enforcement explicit in the PM Agent's role definition and sprint-planning-sop.md.

**Who authors:** PM Agent.  
**Dependencies:** Phase A (execution lifecycle) and Phase B (acceptance criteria) must be complete — the sprint exit template references the Business PO acceptance attestation and the agent execution lifecycle's Verify/Validate output.

**Where it lands:** (1) Amendment to sprint-planning-sop.md — sprint entry and exit sections. (2) Entry and exit document templates at `docs/process/sprint-plans/templates/`. (3) PI Agent obligation in agents.md §Process Integrity Agent — file near-miss if sprint opens without complete entry document.

**Review chain:** PI Agent (integrity check — are the exit invariants enforceable, or performative?) → EL endorsement.

---

**Phase D — Session boundary discipline (mechanism 4)**

**What:** Codify the entry and exit invariants as architectural commitments, not as guidelines.

**Who authors:** PI Agent.  
**Dependencies:** All three prior phases complete — session boundary discipline references the sprint entry/exit artifacts (Phase C), the Business PO acceptance artifact (Phase B), and the execution lifecycle (Phase A).

**Where it lands:** CLAUDE.md §Session Continuity — new subsection §Entry and Exit Invariants. The language must be architectural, not aspirational. "If it isn't written down, it doesn't exist" is the entry invariant stated plainly; the section encodes the consequences.

**Review chain:** PM Agent (practical enforceability in a single-principal governance context) → EL endorsement.

---

### What is not in scope for this sequence

The PI Agent flagged the self-attestation problem: mechanism 3's Verify step is only as strong as the agent executing it honestly. The sequencing proposal does not solve this — it acknowledges it. The mitigation is mechanism 2 (Business PO as external verifier) and mechanism 1 (sprint exit artifact as institutional record). Solving the self-attestation problem in mechanism 3 alone would require tooling (automated output verification against expected analytical behavior) that is out of scope for this design work. File as a known limitation in the execution lifecycle document.

---

### Timeline dependency summary

```
Phase A (mechanism 3) — no dependencies — can open immediately after EL endorsement
Phase B (mechanism 2) — depends on Phase A complete
Phase C (mechanism 1) — depends on Phase B complete
Phase D (mechanism 4) — depends on Phase C complete
```

No parallel authorship. The dependency chain is linear. The logic: each phase's output is a prerequisite input to the next phase's author. Parallel authorship would produce documents that reference placeholders in documents not yet finalized — which is exactly the kind of implicit dependency these mechanisms are designed to eliminate.

---

## Step 3: PI Agent — Review of Sequencing Proposal

**Process Integrity Agent** reviewing PM Agent's sequencing proposal against one question: does the sequence itself follow the protocol being designed?

**Finding 1 — The sequence is ordered correctly.** The dependency chain (3 → 2 → 1 → 4) is correct. Mechanism 3 defines what "Verify" means; without that, mechanism 2's acceptance criteria cannot be written precisely; without both, the sprint exit template in mechanism 1 cannot reference them coherently; without all three, mechanism 4's invariants are assertions without referents. Linear sequencing is the right call.

**Finding 2 — The review chain is appropriately distributed.** Each phase's review chain brings a different authority to bear: Phase A gets architectural alignment (Architect Agent), Phase B gets integrity teeth check (PI Agent primary), Phase C gets enforceability check (PI Agent), Phase D gets practical single-principal governance check (PM Agent). No single agent reviews their own work.

**Finding 3 — One gap in the proposal.** Phase B's review chain says "PI Agent (integrity check — does the exception path have teeth?)" but does not specify what "teeth" means. If a Business PO rejection has no enforcement mechanism — if the sprint can close anyway under EL override with no documented record — the exception path is not a gate, it is an advisory. PI Agent recommends the Phase B output include an explicit requirement: a rejected sprint must produce a written rejection artifact (naming the defect, the remediation scope, and the re-acceptance date) before any work in the next sprint group begins. This is the near-miss registry principle applied to sprint acceptance: a rejection that produces no written record has not been properly resolved.

**Finding 4 — Session boundary discipline placement.** PM Agent proposes Phase D lands in CLAUDE.md §Session Continuity. PI Agent agrees, with one precision: the entry and exit invariants must be stated as architecture, not process guidance. The existing §Architectural Principles section enforces pre-push lint gates and PR merge gates as hard stops — "must stop all git operations." The session boundary invariants should carry the same enforcement language. "Does not open a new sprint session without a complete entry document" should read the same way as "must stop all git operations after opening a PR targeting main." The difference between guidance and a gate is whether the language creates an obligation.

**PI Agent assessment: the sequencing proposal is sound with the one amendment in Finding 3.** It can proceed to EL for endorsement.

---

## Engineering Lead — Scope Question 1

> I am curious if this is the right level to also ensure that intent authorship (for the intent blocks) as downstream from approved ADRs, as well as the independent application code implementation, and test cases and test code development, should be captured. Would we need to loop in the QA Lead, Architect and Frontend Architect Agents to opine?

---

## Agent Response — Scope Expansion: Intent Authorship, Tests, Implementation

**The gap the user is identifying:**

The current mechanism 3 draft focuses on the **back end** of the execution lifecycle — Verify and Validate after implementation. But the Demo 4 failure had an earlier root cause: no one had authored an intent for *"ExternalSectorModule → reserve_coverage_months depletion channel"* before implementing the module. The ADR-012 decisions described commodity price shock distribution — but the downstream analytical consequence (reserves drain) was an inference, not a written specification. If the intent had existed, the Verify step would have had something to check against. Without it, "Verify" becomes subjective: verify against what?

The full chain the user is pointing at:

```
Approved ADR
    └─► Intent authorship (what specifically will this code do?)
            └─► Test case authorship (how will we know it did it?)
                    └─► Implementation
                            └─► Verify (does output match intent?)
                                    └─► Validate (does it serve the mission?)
```

Right now the execution lifecycle design only covers the bottom two steps. The top three — intent authorship from ADR, test authorship from intent, independent implementation — are implicit. That is where Demo 4 actually broke.

**What each agent would contribute:**

**Architect Agent:** Owns the ADR → intent chain. ADRs are the institutional record of *what was decided*. The Architect is the right agent to define what "intent authorship from an approved ADR" looks like — specifically: what is the minimum specification that constitutes a valid intent block, and who holds R for authoring it? Is the intent a section in the ADR itself, a separate artifact, or inline in the implementation PR? The Architect also needs to opine on the boundary between ADR decisions (architectural commitments) and intent blocks (feature specifications) — those are different levels of abstraction and conflating them would create a governance problem.

**QA Lead:** Owns test authorship as a first-class step, not a trailing step. If intent blocks are the specification, acceptance tests should be authored *from* the intent — before implementation begins. This is the forcing function that makes the Verify step honest: you can't write a meaningful acceptance test from a vague intent, so intent authorship quality is gated by whether a test can be written from it. The QA Lead's input on this step would define what "testable intent" means — and would make mechanism 3 self-reinforcing rather than dependent on agent self-attestation (the gap PI Agent flagged in Finding 4).

**Frontend Architect:** The chain looks different for frontend work. An approved ADR may not be the upstream document — a UX brief from the UX Designer is the specification for frontend features, and the Frontend Architect translates that into a component spec before implementation. If the execution lifecycle only references ADRs as the upstream source, it will be incomplete for frontend work. The Frontend Architect needs to define the equivalent chain: UX Brief → component spec → intent → test → implementation → Verify against the component spec.

**Recommendation:**

Yes, all three should be consulted in Phase A — not as separate phases. Their input changes the *content* of Phase A's output (the execution lifecycle document), not its position in the dependency chain. Mechanism 3 must work for all work types — backend analytical modules, frontend features, and documentation — so the Phase A consultation needs to produce a lifecycle that is general enough to cover all three without being so abstract it loses the forcing function.

One sequencing implication: the Phase A consultation list is now PM Agent + QA Lead + Business PO + Architect Agent + Frontend Architect. That is a larger deliberation surface than originally proposed. The PM Agent should account for this in the time allocation — Phase A is the most complex phase in the sequence.

**One thing to hold:** the user's framing puts intent authorship as *downstream from approved ADRs*. That is correct for backend analytical capabilities (where the ADR is the upstream authority). For frontend features, UX briefs and information hierarchy rulings are the upstream authority. For documentation, the equivalent is the standards review or the near-miss finding that motivated the document. The execution lifecycle should name all three upstream source types — not only ADRs — or frontend and documentation work will be ungoverned by the lifecycle in practice.

**PI Agent notes this scope expansion as a near-miss candidate:** the original mechanism 3 framing focused only on post-implementation verification, which would have left the intent authorship gap unaddressed. The EL's question caught this before any documents were drafted. That is the mechanism working as designed — deliberation before encoding.

**This is still pre-endorsement.** No files should be created until the EL confirms: (a) the expanded Phase A scope with these three additional agents, and (b) whether the three agents should opine in this session now, or whether their consultation is deferred to Phase A authorship when PI Agent initiates it formally.

---

## Engineering Lead — Scope Question 2

> Lastly, should we also connect how User Experiences, and User Persons should guide the ADR development process, without which Architecture could meaningless at worst or miopic at best?

---

## Agent Response — UX/Persona Traceability Upstream of ADR Development

**The gap this identifies:**

The current ADR process has a technical panel and an architectural authority (the Architect Agent). What it does not have is a formal requirement that the ADR demonstrate:

1. **Which user need it serves** — traceable to a named persona or documented use case, not just a technical motivation
2. **What the UX implications of the decision are** — consulted with the UX Designer for any decision that affects how users encounter the capability

ADR-012 (ExternalSectorModule) is the illustrative case. The panel defined commodity price shock distribution mechanics with precision. But "how will the finance minister in Amman see the reserve drawdown arc in the instrument cluster?" was not a panel question. DEMO4-005 — the HCL indicator computed but invisible — is a direct consequence: the ADR scoped the module's event emissions without specifying how those events would surface to the user. If persona traceability had been in the ADR scope, "HCL visible in Zone 1D" would have been a documented requirement before a line of code was written.

The full chain, once this is included:

```
User Personas + User Journeys + North Star UX
    └─► Problem framing: which named persona, in which journey step, is served?
            └─► ADR authorship (with UX Designer + Business PO as panel members
                    for user-facing decisions)
                        └─► Intent authorship (downstream from approved ADR)
                                └─► Test authorship (from intent)
                                        └─► Implementation
                                                └─► Verify (against intent)
                                                        └─► Validate (against mission)
```

Without this, "Validate" at the bottom of the chain is checking against an abstract mission statement. With it, Validate checks against a documented user need that was already agreed upon at ADR time — which is a much harder test to satisfy performatively.

**The three distinct authorities involved:**

**UX Designer** — the right agent to define what UX traceability *looks like* in an ADR. Not every ADR requires UX Designer approval, but every ADR that introduces a new capability or changes how users encounter existing capabilities should require a documented UX implication statement. The UX Designer's rulings in agents.md are already described as "binding" — this formalizes when that binding authority applies upstream, not just to UI implementation.

**Business PO** — the right agent to define what persona traceability looks like in ADR scope definition. The Business PO already asks "are we building the right thing?" This adds: that question must be answered and documented *before the ADR is accepted*, not after the feature ships. Every ADR should name the persona(s) it serves and the journey step it addresses. ADRs that cannot name a persona (pure infrastructure decisions) should document that explicitly and carry an obligation to trace the capability they enable to a persona need.

**Architect Agent** — the right agent to define where the line is. Not every ADR needs the same UX input. An ADR about matrix engine computation (ADR-009) has an indirect UX connection — it enables performance, which enables more scenarios, which serves the finance minister. That is two levels of indirection. An ADR about a new measurement module (ADR-012) has a direct UX connection — it produces outputs that land in Zone 1D. The Architect needs to define a tiering: which ADRs require UX Designer on the panel, which require only a documented persona trace, and which may waive both with explicit documentation of why the UX connection is sufficiently indirect.

**What this adds to the sequencing:**

This is a Phase 0 — upstream of everything PM Agent proposed. It does not replace any phase; it anchors them. The execution lifecycle's "Plan" step currently reads as "reference the approved ADR." Once this is incorporated, "Plan" reads as "reference the approved ADR, which must already carry a documented user need and UX implication." The Verify and Validate steps at the end of the lifecycle become more rigorous because they have a richer upstream specification to check against.

The three agents who should opine — UX Designer, Business PO, and Architect Agent — should be consulted during Phase A, but specifically on the *ADR traceability requirement* as a distinct question from the execution lifecycle's Verify/Validate mechanics. Those are related but separable: one governs what must be in an ADR before implementation begins, the other governs how an implementing agent checks their own work.

**One structural observation before endorsement:**

The sequencing proposal now has five phases (Phase 0 through Phase D) and a Phase A consultation that includes seven agents. That is a significant deliberation surface. Before endorsement, the EL should decide whether all four mechanisms plus Phase 0 are scoped to a single design sprint, or whether Phase 0 (UX/persona → ADR traceability) is the first sprint and Phases A–D follow in a subsequent sprint once Phase 0 is accepted and committed. Trying to design all five phases in one session risks producing documents that reference each other before any of them are finished — which is the exact failure mode of implicit cross-session dependencies that mechanism 4 is designed to prevent.

The design work should itself follow the protocol it is designing.

---

## Engineering Lead — Scope Question 3

> There is probably also a role for the expert agents on the DIC at the Phase 0 level to provide guardrails for the UX experience, as well as the business lense what is the "art of possible".

---

## Agent Response — DIC Role at Phase 0

**Correct — and this completes the upstream chain in a way that none of the other agents can.**

The UX Designer, Business PO, and Architect Agent can define how persona traceability works as a process requirement. But they cannot answer the deeper question: *what should the persona actually be able to see and do, given the real analytical complexity of the domain they operate in?* That is DIC territory.

**The two distinct functions the DIC serves at Phase 0:**

**Function 1 — Domain guardrails for UX experience**

The UX Designer optimizes for legibility and cognitive load. The risk is that legibility and the mission can diverge — the most legible indicators are often the most financially-conventional ones, which are precisely the indicators that sophisticated actors already have. If the UX hierarchy is designed without domain guardrails, it can produce an interface that is excellent by conventional product standards and mission-subversive in practice.

The DIC agents are the counterweight. Each holds a domain that the mission explicitly requires to have equal weight with financial indicators, and each has a specific failure mode to guard against:

| Agent | Guardrail |
|---|---|
| **Development Economist** | Human cost ledger must carry equal visual weight to financial indicators — never demoted to secondary position by UX hierarchy decisions |
| **Chief Methodologist** | Uncertainty must not be suppressed or rendered invisible by design choices that prioritize clean outputs over honest ones |
| **Intergenerational Advocate** | Irreversible thresholds must never be renderable as ignorable — MDA floors cannot be visually minimized |
| **Ecological Economist** | Ecological boundaries must not be frameable as optional — the planetary boundary crossing should read with the same severity as a reserve CRITICAL floor |
| **Community Resilience** | Aggregate indicators must not be the only visible output — distributional effects on cohorts must surface, not be abstracted away |

These are not design preferences. They are domain-grounded requirements that the UX Designer cannot derive alone from information hierarchy principles. The Development Economist's authority over the human cost ledger is not advisory at Phase 0 — it should be binding in the same way the UX Designer's rulings are binding on implementation.

**Function 2 — The art of the possible**

The Business PO asks: "are we building the right thing?" from a product management frame. The DIC asks the same question from a domain knowledge frame — and the answers are often different, because the domain frame knows things the product frame does not.

Two specific contributions:

**Investment Agent** speaks to the capability gap from the competitive landscape. The Investment Agent knows what well-resourced sovereign wealth funds and sophisticated financial institutions actually have access to. That gap — between what the powerful can see and what WorldSim's intended users can currently see — is the product roadmap stated as a domain fact. ADR scope that does not close part of that gap is not serving the mission, regardless of how well it satisfies the persona's articulated needs.

**Development Economist** speaks to what would genuinely change a minister's decision. Not what the persona says they want, and not what the product manager infers from user journeys — but what a practitioner in sovereign fiscal policy would actually need to shift their judgment under pressure. This is the "art of the possible" from the mission side: what is the minimum analytical capability that makes the tool useful to the person sitting across from the IMF, and what is the maximum the tool can currently claim to provide honestly?

Together these two functions — guardrails (what the UX must never compromise) and art of the possible (what the roadmap should target) — mean the DIC is not downstream from ADRs and UX design. For WorldSim, it is upstream.

**The structural implication:**

The DIC's current activation pattern is analytical — SCENARIO, CHALLENGE, VALIDATE applied to economic situations. What the user is proposing is a second activation mode: applied to *design decisions and roadmap definition*. The Council Orchestrator already has a ROADMAP activation pattern (`Council Orchestrator: ROADMAP — [gap]`). Phase 0 would use this pattern to ask: given the domain complexity of sovereign fiscal decision-making, what must the UX experience never compromise, and what capability gaps should the roadmap prioritize closing?

This is a meaningful expansion of the DIC's mandate, and it should be named as such rather than treated as an incremental extension. The DIC was designed to make competing analytical interests visible in scenario outputs. Making those same interests visible in design and architectural decisions is a natural extension — but it changes the DIC's relationship to the development process from advisory-on-outputs to authoritative-on-requirements.

Not all nine DIC agents need standing Phase 0 roles. The four with the most direct Phase 0 relevance are: Development Economist (human cost ledger guardrail), Chief Methodologist (uncertainty integrity guardrail), Intergenerational Advocate (irreversibility guardrail), and Investment Agent (art of the possible / capability gap framing). The remaining five — Political Economist, Geopolitical Analyst, Ecological Economist, Community Resilience, Social Dynamics — should be consulted domain-specifically when an ADR or UX decision touches their domain, but do not need standing Phase 0 participation for every design decision.

**The full upstream chain, now complete:**

```
DIC (guardrails + art of the possible)
    └─► User Personas + User Journeys + North Star UX
            └─► Problem framing (named persona, journey step, domain-validated need)
                    └─► ADR authorship
                         (Architect + UX Designer + Business PO + relevant DIC agents)
                                └─► Intent authorship
                                        └─► Test authorship
                                                └─► Implementation
                                                        └─► Verify
                                                                └─► Validate
```

**Summary of what is on the table before any file is created:**

- **Phase 0** — UX/persona traceability upstream of ADR development. Participants: UX Designer, Business PO, Architect Agent, Council Orchestrator (DIC, four standing agents + domain-specific). This may be a separate sprint from Phases A–D given its scope.
- **Phase A** — Execution lifecycle (mechanism 3). Participants: PI Agent (author), PM Agent, QA Lead, Business PO, Architect Agent, Frontend Architect.
- **Phase B** — Business PO acceptance protocol (mechanism 2). Authors: BPO + PI Agent.
- **Phase C** — Sprint cadence formalization (mechanism 1). Author: PM Agent.
- **Phase D** — Session boundary discipline (mechanism 4). Author: PI Agent.

The question before the EL: should Phase 0 be a separate sprint with its own entry/exit gate, or does it proceed in parallel with Phases A–D? And are there any participants, guardrails, or scope boundaries that the EL wants to adjust before the design is committed to documents?

---

## Engineering Lead — Documentation Request

> Before I endorse, can you kindly document the above conversation starting from my prompt that started with "Intent: Sprint Cadence," verbatim with absolutely no summarization. Please find an appropriate places in the docs/ section of our github repo to save the MD file, and let me know so I can review it once drafted.

*This document is the result of that request. Filed at `docs/process/design/2026-06-08-sprint-cadence-acceptance-gates-deliberation.md` pending EL review and EL endorsement of the sequencing plan.*

---

## Engineering Lead — North Star as Apex

> One last question to add to the chaining of phases, does it make to envision the north star document as the over-arching guiding document on our mission and vision, and why we exist?

---

## Agent Response — Founding Document as Apex of the Chain

Yes — and it already exists in this repo. The founding document at `docs/vision/worldsim-founding-document.md` is precisely that: the reasoning behind every principle, the why beneath the what.

But your question is pointing at a gap in the chain as currently drawn. The chain starts at the DIC, but the DIC's guardrails themselves derive from somewhere — from the mission. If that source is not named at the top of the chain, the chain is floating. Someone can always ask "why is the human cost ledger non-negotiable?" and the answer lives in the founding document, not in the DIC agent's definition.

The complete chain with the north star document at the apex:

```
Founding Document + North Star
(why we exist; the quinoa farmer; the finance minister across the table)
    └─► DIC (guardrails + art of the possible)
         (domain experts translating the mission into analytical requirements)
            └─► User Personas + User Journeys + North Star UX
                 (named humans the mission serves; how they actually move through the tool)
                    └─► Problem framing
                         (named persona, journey step, domain-validated need)
                            └─► ADR authorship
                                 (Architect + UX Designer + BPO + relevant DIC agents)
                                    └─► Intent authorship
                                            └─► Test authorship
                                                    └─► Implementation
                                                            └─► Verify
                                                                    └─► Validate
```

The Validate step at the bottom of the chain now has a direct line back to the top: you validate against the founding document's north star, not against an abstract "mission." That closes the loop. Every implementation decision is traceable — through intent, through ADR, through persona, through DIC guardrails — back to the quinoa farmer.

One practical implication: the founding document should be mandatory reading at Phase 0, not just for orientation. When the DIC is asked "what guardrails must the UX experience never compromise?", those guardrails should be derivable from the founding document's reasoning — not invented fresh each time. The founding document is the authority the DIC agents appeal to when their guardrails are challenged.

---

## Engineering Lead — North Star Gaps

> Yes, add that to the document, and whether there are gaps in the formulation of the north star documents that need to be addressed, and if left open, could amplify cracks in the process leading to future breakages?

---

## Agent Response — Gap Analysis of the North Star Documents

*Both `docs/vision/worldsim-founding-document.md` and `docs/ux/north-star.md` were read in full before this analysis was written.*

The founding document is the most complete statement of mission and reasoning that exists in this project. The UX north star is a rigorous instrument-cluster design authority. Both are genuine assets. The gaps below are not criticisms of what is there — they are cracks in what is missing that, left unaddressed, will propagate into the development process as recurring breakage.

---

### Founding Document Gaps

**Gap FD-1 — The north star test exists as a statement, not as an operationalized artifact**

CLAUDE.md §North Star states: "Does this decision make the tool more useful to that person in that moment? If yes, proceed. If no, reconsider." That is a powerful test. But it has no artifact form, no home, no requirement to be documented, and no agent who holds R for running it. The EL ran a north star test at the opening of this deliberation — the PI Agent and BPO produced a joint assessment. That was entirely ad hoc. If it had not been explicitly requested, it would not have happened.

The crack this creates: architectural decisions, sprint reviews, and ADR acceptances can all be completed without anyone formally running the north star test. The test is aspirational, not structural. Future breakage mode: a technically sound, CI-green, Business-PO-accepted sprint that is analytically correct but mission-subversive — because the north star test was never asked.

**Gap FD-2 — The three-layer information asymmetry is described but the third layer has no design owner**

Part Four of the founding document identifies three layers of information asymmetry: data availability (addressed by the synthetic data framework), data quality (addressed by the confidence tier system), and institutional capacity asymmetry — the user with limited technical background who needs self-interpreting outputs. The third layer is named and its importance is clear: "the instrument must tell the user what the number means, not just display the number." But there is no agent who holds R for the third layer. The UX Designer owns information hierarchy. The Chief Methodologist owns statistical integrity. But "self-interpreting outputs for non-technical users" — which is the Layer 3 design requirement — is claimed by no one.

The crack this creates: Layer 3 requirements are routinely deferred because they have no advocate with process authority. The Customer Agent's mandate partially covers this — "does this output make sense to Aicha Mbaye's chief of staff, alone with a tablet, in five minutes?" — but the Customer Agent is not on any standard ADR panel or sprint review. Future breakage mode: outputs that are analytically correct and display-compliant but require specialist mediation to interpret — which precisely replicates the asymmetry the tool is designed to counter.

**Gap FD-3 — The kryptonite frame is a values statement without design constraints**

Part Five names the tool's orientation explicitly: "it is on the side of the finance ministry team with three economists facing a team of forty." This is important and honest. But it is never operationalized as a design constraint. What does "on the side of the finance ministry" mean when the UX Designer is deciding whether to put the uncertainty band above or below the trend line? What does it mean when the Architect is deciding how to tier an ADR's panel? There is no translation layer between the kryptonite frame and the decisions it should govern.

The crack this creates: when implementation decisions require tradeoffs — legibility vs. completeness, speed vs. honesty, simplicity vs. calibration — there is no kryptonite-frame test to apply. The founding document's orientation disappears at the moment it is most needed. Future breakage mode: UX decisions that are internally consistent within information hierarchy principles but that systematically prioritize the most-legible (most-financially-conventional) indicators over the indicators that most matter to the less powerful party.

**Gap FD-4 — "What WorldSim Does Not Do" is static and not linked to visible disclosure**

Part Six is genuine institutional honesty: WorldSim does not model real-time market dynamics, does not model geopolitical constraints on programme design, does not model cascade dynamics across sectors. These are real limitations. But the document is static — it was written at a point in time and has no update mechanism. More importantly, it is not linked to any in-tool disclosure mechanism. A finance ministry analyst using WorldSim to model the Zambia debt default has no guaranteed path to encountering the statement "WorldSim does not model cascade dynamics across sectors" unless they read the founding document.

The crack this creates: the tool's stated epistemic honesty — "blindspots are documented, not hidden" — is honored in the document but not in the instrument. Future breakage mode: a user cites WorldSim's analysis in a negotiation without knowing the limitation that makes that specific use of the analysis unreliable. The tool's credibility — which depends on its honesty — is damaged not by dishonesty but by the gap between documented honesty and displayed honesty.

**Gap FD-5 — The flywheel has no operational pathway**

Part Five describes the long-game strategy: "the tool makes users better, better users make the tool better." This is the community intelligence flywheel. But there is no mechanism through which a Kenyan central banker who has run twenty scenarios can contribute what they have learned back to the model. There is no scenario contribution process, no backtesting case submission protocol, no community forum, no feedback loop. The flywheel is a stated aspiration in the founding document and an absent mechanism in every operational document.

The crack this creates: this gap does not cause near-term process breakage — it causes long-term mission failure. The tool cannot fulfill its democratization mission if it is a one-way transfer of capability from the project to users. Future breakage mode: accumulated user knowledge that could improve the model evaporates rather than feeding back. The flywheel never spins.

---

### UX North Star Gaps

**Gap NS-1 — The canonical user is singular; the tool serves a persona hierarchy**

The north star opens with "a debt restructuring specialist at a finance ministry." This is Persona 2. But the five-persona hierarchy in `docs/ux/personas.md` includes Persona 1 (Programme Analyst / Lucas Ferreira — working-level implementation), Persona 3 (Political Advisor — political feasibility), Persona 4 (Academic Economist — backtesting and calibration), and Persona 5 (Institutional Decision-Maker / Executive Director — strategic oversight). If ADR panels and sprint reviewers reference the canonical user and stop there, capabilities serving Personas 1, 3, 4, and 5 will be systematically deprioritized.

The crack this creates: design decisions default to Persona 2 whenever there is no explicit alternative advocate. The M11.5 usability audit found that Persona 1 (Lucas Ferreira) could not complete a single task successfully — in part because the tool had been designed with Persona 2 implicitly dominant. Future breakage mode: each ADR panel and each sprint review implicitly optimizes for the most-salient persona without documenting which persona is being served — accumulating directional bias over time.

**Gap NS-2 — The document is out of date relative to Mode 3 delivery**

The north star was last revised 2026-05-22 against ADR-008. Mode 3 (Active Control) shipped in M12 (PR #778). The north star's Mode 3 section is written in future tense: "Active negotiation: proposed terms applied as control inputs in real time." That is no longer a future state. A document governing all frontend design decisions that describes a live capability as hypothetical is an active source of confusion for agents reading it in future sessions.

The crack this creates: agents referencing the north star for Mode 3 design guidance will find aspirational description rather than design authority. The authority gap will either produce redundant re-derivation of decisions already made, or produce decisions inconsistent with the delivered capability. Future breakage mode: a future Mode 3 enhancement is designed against the hypothetical description in the north star rather than against the delivered architecture — producing a feature that conflicts with what was already shipped.

**Gap NS-3 — The distribution visualization acceptance criteria are milestone-pinned, not living standards**

The three acceptance criteria at the bottom of the north star document reference M5 distribution rendering work explicitly. The document does not indicate whether these criteria have been met, superseded, or extended for subsequent milestones. They are frozen at a point in time. If an agent reads the north star document expecting authoritative acceptance criteria for current distribution visualization work, they will find M5-era criteria that may or may not apply.

The crack this creates: acceptance criteria that are milestone-pinned rather than living standards will be applied to work they were never designed to govern. Future breakage mode: a future PR includes distribution visualization changes that satisfy the M5 criteria but break something that was implemented in M6 through M12 — because no one updated the criteria to reflect what was built.

**Gap NS-4 — Failure modes for the user experience are not defined**

The north star defines success: "understanding whether a proposed fiscal adjustment path crosses human cost thresholds." But it does not define what the user experiences when the tool fails — when data is so thin the output is directionally meaningless, when an MDA alert fires on a data artifact rather than a real signal, when the synthetic data estimate is so wide it cannot support any negotiating position. Failure handling from the user's perspective has no acceptance criteria.

The crack this creates: failure modes are handled by engineering judgment in the absence of a UX standard. The "No False Precision" principle requires the tool to say "this output is directionally meaningless" rather than generating an uninterpretable band — but what the user sees when that declaration is made is undefined. Future breakage mode: a user in an active negotiation encounters a Structural Absence Declaration or a meaninglessness threshold and has no guidance from the instrument on what to do next. The tool fails honestly but not helpfully.

**Gap NS-5 — Cognitive load is stated as a constraint but not quantified**

"They need to get to the relevant signal in minutes, not hours." This is a real constraint. But "minutes" is not a measurable acceptance criterion. The M11.5 usability sessions were designed to measure cognitive load empirically — but their findings have not been translated back into quantified north star acceptance criteria. The cognitive load standard remains narrative.

The crack this creates: design decisions that increase cognitive load can be accepted because there is no quantified threshold to violate. The M11.5 findings (which identified specific failure points — non-interactive alert panel, illegible text at 1440×900, missing cohort disaggregation) are in session records but not in the north star as updated acceptance criteria. Future breakage mode: cognitive load accumulates across features, each individually acceptable, until the aggregate is the tool that Lucas Ferreira couldn't use.

---

### Cross-Document Gaps

**Gap XD-1 — The founding document's north star figure and the UX north star's canonical user are not explicitly connected**

The founding document's north star is "a finance minister of a small, vulnerable country" — a decision-maker. The UX north star's canonical user is "a debt restructuring specialist at a finance ministry" — a working-level analyst. These are not the same person. The minister is Persona 5 (Institutional Decision-Maker); the specialist is Persona 2 (Finance Ministry Negotiator). The founding document implicitly grounds the entire mission in the minister's position; the UX north star implicitly grounds all design decisions in the specialist's workflow. Neither document names the other's figure. Neither document resolves who the primary design target is when the two personas have conflicting needs.

The crack this creates: there is no authoritative answer to "which persona governs when two personas conflict?" The founding document suggests the minister (mission level); the UX north star suggests the specialist (implementation level). Without an explicit resolution, ADR panels will apply whichever persona is more convenient for the argument being made. Future breakage mode: a UX decision that serves Persona 2's workflow is accepted on north star grounds, while being inconsistent with the founding document's mission framing — with no process mechanism to surface the conflict.

**Gap XD-2 — Neither document is formally referenced in the ADR template or ADR acceptance process**

ADRs reference CLAUDE.md's guiding principles. CLAUDE.md references the founding document as background reading. But no ADR template requires: "which passage in the founding document supports this decision?" or "which persona does this decision primarily serve, per the UX north star?" The north star documents are reference material, not process gates.

The crack this creates: the chain from founding document through DIC through personas through ADR is described in this deliberation but encoded nowhere in the existing process. An ADR can be authored, reviewed by a panel, and accepted — all without anyone checking whether the decision is traceable to a founding document passage or a named persona. This is the structural gap that makes everything upstream of implementation advisory rather than authoritative. Future breakage mode: every Demo 4-equivalent failure, where technically correct work is mission-incomplete, because the mission-to-implementation traceability was never required by any process gate.

---

### Summary: Gaps and Their Failure Modes

| Gap | Document | Failure mode if left open |
|---|---|---|
| FD-1 | Founding | North star test never formally run — mission-subversive work accepted as done |
| FD-2 | Founding | Layer 3 (self-interpreting outputs) has no process owner — systematically deferred |
| FD-3 | Founding | Kryptonite frame never governs tradeoffs — financially-conventional indicators win by default |
| FD-4 | Founding | Limitations documented but not displayed — user cites unreliable analysis in negotiation |
| FD-5 | Founding | Flywheel never spins — mission fails in the long term |
| NS-1 | UX North Star | Persona 2 dominates by default — Personas 1/3/4/5 systematically deprioritized |
| NS-2 | UX North Star | Mode 3 guidance is stale — future enhancements conflict with delivered architecture |
| NS-3 | UX North Star | Acceptance criteria are milestone-pinned — applied to work they were never designed for |
| NS-4 | UX North Star | Failure modes have no UX standard — tool fails honestly but not helpfully |
| NS-5 | UX North Star | Cognitive load accumulates unchecked — tool becomes unusable incrementally |
| XD-1 | Both | Minister vs. specialist conflict unresolved — whichever persona is convenient wins |
| XD-2 | Both | Mission-to-implementation traceability never required — every Demo 4 recurs |

**The highest-priority gaps for Phase 0** are XD-2 (neither document is a formal process gate in the ADR or sprint process), FD-1 (the north star test has no artifact form or agent owner), and XD-1 (the founding document's north star figure and the UX canonical user are not reconciled). These three gaps are the structural root of the process problem the EL's original intent prompt was designed to solve. Closing them is what makes Phase 0 more than a documentation exercise — it is what makes the founding document and north star genuinely authoritative upstream of every implementation decision.

---

*Document complete as of 2026-06-08. Pending EL review and endorsement of the sequencing plan before any implementation begins.*
