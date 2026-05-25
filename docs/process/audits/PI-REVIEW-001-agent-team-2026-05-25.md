# PI-REVIEW-001 — Agent Team Organization Review

**Date:** 2026-05-25
**Reviewed by:** Process Integrity Agent
**Activation:** `PI Agent: REVIEW — agent team organization`
**Scope:** All 20 defined agent roles assessed against the Founding Document frame and current
milestone requirements.

---

## Required Reading Completed

Before this document was drafted, the following were read in full in order:

1. `docs/vision/worldsim-founding-document.md` — Founding vision; set the frame
2. `CLAUDE.md` — Project constitution; UX commitments, Platform Principle, governance
3. `docs/process/agents.md` — Full agent roster (20 roles, NM-019 update through PR #505)
4. `docs/process/agent-raci.md` — RACI matrix and file ownership table
5. `docs/process/near-miss-registry.md` — NM-001 through NM-022
6. Open GitHub issues labeled `documentation` (30 open; none assigned)

---

## Frame: The Three-Layered Asymmetry Problem

The Founding Document defines WorldSim's mission in terms of three distinct information
asymmetry layers, each requiring a different structural response:

| Layer | Problem | WorldSim Response |
|---|---|---|
| Layer 1 | Data availability — country may simply not have the data | Synthetic Data Framework (ADR-007, CM owns) |
| Layer 2 | Data quality — data exists but is low quality or delayed | Confidence Tier System (DA + DQ Agent own) |
| Layer 3 | Institutional capacity — the finance ministry's analytical team is five people with no dedicated economists | The tool itself; but who ensures the tool serves them? |

The agent team has built explicit ownership for Layers 1 and 2. **Layer 3 has no dedicated
agent.** This is the primary structural finding of this review.

---

## Agent Roster Summary (as of 2026-05-25)

| Agent | Status | Core mandate |
|---|---|---|
| Engineering Lead | Human | Final decision authority |
| PM Agent | Active | Execution governance; HORIZON; scope |
| Process Integrity Agent | Active | Process adherence; registry maintenance; audits |
| Architect Agent | Active | ADR authorship; system design |
| Implementation Agents | Active | Feature delivery against ADR contracts |
| Data Architect Agent | Active | Schema ownership; data standards |
| QA Lead Agent | Active | CI gates; test strategy; backtesting infrastructure |
| Security and Review Agent | Active | Vulnerability audit; dual-use review |
| Independent Review Agent | Active | Cold-read stakeholder perspective |
| Socratic Agent | Active | Architecture comprehension for EL |
| Chief Engineer Agent | Defined-inactive | Compute substrate; matrix benchmarks |
| Frontend Architect Agent | Active | Frontend implementation; performance on target hardware |
| UX Designer Agent | Active | Instrument cluster architecture; UX north star |
| Business Product Owner Agent | Active | User story decomposition; mission-aligned scope |
| UX Design Thinking Agent | Active | First-principles UX derivation; stress-testing |
| Domain Intelligence Council (9) | Active | Domain-specific challenge across measurement frameworks |
| Council Orchestrator | Active | DIC coordination; blind interview facilitation |
| Architecture Review Facilitator | Active | Full/targeted architecture reviews via DIC |
| Intent Block Author Agent | **Proposed** | Spec block authorship; segregation of duties (Issue #299) |
| Data Quality Agent | **Proposed** | Field certification; data admission testing (Issue #300) |

---

## Findings

### F-001 — Layer 3 Asymmetry (Institutional Capacity) Has No Dedicated Agent

**Severity:** High
**Type:** Mandate gap — Founding Document requirement with no agent owner

**Finding:**
The Founding Document's third asymmetry layer — "the capacity gap between the analytical teams
available to a Bolivian finance ministry (five people, no dedicated economists, data six months
delayed) and those available to the IMF (teams of economists, real-time data, sophisticated
models)" — has no agent whose standing mandate is to ensure WorldSim serves users with limited
institutional capacity.

The UX Designer owns cognitive load in the interface (instrument cluster layout, Mode 3 zone
reservation). The Business Product Owner owns mission-aligned scope decomposition. Neither has a
standing mandate to ask: *Can a five-person finance ministry team with limited analytical training
actually use this output in a negotiation room? Can the minister defend the numbers without a
specialist in the room? Does the tool teach as it informs?*

This gap has two consequences:

1. **Architectural decisions about output narrative, explanation depth, and teaching affordances**
   are made without a standing advocate for the low-capacity user.

2. **The Flywheel's "users get better" arm has no designer.** The Founding Document states:
   "The community intelligence that accumulates through use is as valuable as the codebase."
   For that to happen, users must develop capability. No agent owns the learning pathway.

**What the Founding Document requires:**
> "A user who cannot understand and challenge our methodology cannot genuinely use our tool —
> they can only depend on it. Dependency is not leveling."

Dependency vs. leveling is the exact failure mode Layer 3 is meant to prevent. Building a
sophisticated tool that a five-person team depends on but cannot interrogate reproduces the
asymmetry rather than correcting it.

**Recommendation:**
Two options (EL decision):

- **Option A:** Expand the Business Product Owner Agent's mandate to explicitly include
  institutional capacity advocacy — a standing obligation to ask "can the Bolivian finance
  ministry team use this?" before any feature acceptance. Requires a working agreement update
  and a new RACI row for `docs/ux/personas.md` as a co-owned file.

- **Option B:** Commission a new "User Empowerment Agent" with domain expertise in capacity
  building for under-resourced institutions. Higher standing than an expanded PO mandate;
  appropriate if the Flywheel architecture becomes a first-class design concern in M10/M11.

The Independent Review Agent's "user testing variant" (first-time user, five minutes before
a meeting) is the closest existing mechanism — but it is activated episodically (before demos
and milestones), not as a standing architectural voice.

**Filed:** Issue #[TBD-F001]

---

### F-002 — Backtesting Eureka Function Has No Named Owner

**Severity:** High
**Type:** Mandate gap — Founding Document principle with no execution owner

**Finding:**
The Founding Document: *"The gap between model prediction and historical outcome is not a
failure — it is the primary signal for improvement. We know where our model is wrong by running
it against history."*

This "primary signal for improvement" requires two distinct functions:

1. **Infrastructure function:** Does the backtest pass? — QA Lead owns the CI gates,
   the backtesting fixture suite, the fidelity threshold registry (Issue #123).

2. **Learning function:** What does the gap tell us? — **No agent owns this.**

The learning function is: given that the model predicted X for Greece 2010–2015 and the actual
trajectory was Y, which assumptions were wrong, what relationships need recalibration, and what
does the divergence reveal about model blindspots? This requires domain economics expertise and
a defined workflow for translating backtesting divergences into model improvements.

**Current gap evidence from open issues:**
- Issue #27: "document calibration basis for propagation attenuation parameters — methodology
  or explicit placeholder." Unassigned, M11.
- Issue #103: "multi-country validation suite design — statistical validity requires more than
  2-step single-country pass." Unassigned, M11.
- Issue #160: "add statistical power statement to all fidelity reports." Unassigned, M11.

All three are in the backtesting learning gap — they require someone to think about *what
backtesting tells us*, not just *whether backtesting passes*.

**Candidates for ownership:**
- Chief Methodologist: Statistical integrity is CM's core mandate. Interpreting backtesting
  divergences fits — but CM is a DIC member (activated episodically), not an operational agent
  with HORIZON obligations.
- Development Economist: Domain expertise for economic relationships. Can diagnose why a
  Greece sovereign debt trajectory diverged from model predictions. But no standing mandate.
- QA Lead: Owns the infrastructure. An extension of mandate to include gap analysis is possible
  but may be overloading a CI-focused role with domain economics work.

**Recommendation:**
Add a backtesting gap analysis obligation to the Chief Methodologist's DIC working agreement:
"After any backtesting run that produces a DIRECTION_ONLY FAIL or a fidelity score below the
registered threshold, the CM is the primary analyst for the gap interpretation brief — what the
divergence reveals about model assumptions, to be filed as an issue before the next milestone
begins." The Development Economist co-authors when the gap is in economic relationship territory.

This does not require a new agent — it requires encoding an existing agent's domain expertise
into a standing obligation.

**Filed:** Issue #[TBD-F002]

---

### F-003 — IB and DQ Agents Must Be Defined Before M10 Implementation Begins

**Severity:** High
**Type:** Role readiness gap — proposed agents with M10 prerequisites are undefined

**Finding:**
Two proposed agents have M10 milestone assignments and represent prerequisites for M10
implementation work. Both remain at stub definition ("Proposed — definition pending Issue #NNN"):

**Intent Block Author Agent (Issue #299, M10):**
The IB Agent is needed for all non-trivial functions in M10 implementation. The segregation
of duties principle — "the agent that wrote the implementation cannot write the intent block
for that implementation" — cannot be enforced without a defined IB Agent. M10 is the
instrument cluster implementation milestone (TrajectoryView, MDA Alert Panel, PMM + Four-
Framework). These components will produce significant new Python and TypeScript code. Issue #258
(mandatory intent blocks for all simulation modules) and Issue #286 (scripts/intent_gap_check.py)
are both M10, both assigned to no one.

If IB is not defined before M10 implementation issues are opened, the implementation agents
will write their own intent blocks — precisely the conflict the IB Agent was designed to prevent.

**Data Quality Agent (Issue #300, M10):**
DQ was targeted for M9 activation. The milestone closed without activation. Issue #252
(field-level data certification) is M10. Without a defined DQ Agent, certification work in
M10 has no authoritative owner, and the independence requirement ("should not be the same agent
that designed the data standard being applied") has no mechanism for enforcement.

**What "stub definition" means in practice:**
Both agents have activation triggers and an independence requirement. Neither has:
- A working agreement (what I commit to doing / where I will ask for help)
- A RACI position (which file rows show DQ or IB as R or C)
- An activation prompt template (the prompt is "[pending Issue #NNN]" for both)

Without these, the agents cannot be activated correctly. An agent following the working agreement
standard defined by all other agents in the roster would be improvising for IB and DQ.

**Recommendation:**
Define both agents (full working agreement, RACI position, activation prompt template) before
any M10 implementation issue is opened. This is a milestone kickoff gate, not a parallel track.

**Filed:** Issue #[TBD-F003]

---

### F-004 — Chief Engineer Activation Timing Is Ambiguous at M10 Start

**Severity:** High
**Type:** Activation timing gap — Phase 1 benchmarks require CE knowledge profile; CE is
still defined-inactive

**Finding:**
NM-020 filed Issue #514 (Phase 1 baseline benchmarks) as an M10 deliverable. The benchmarks
are a hard prerequisite for ADR-009 authoring. The Chief Engineer is the appropriate agent for
this work — per the CE working agreement, the CE owns "engine performance decisions, baseline
benchmarks, A/B validation methodology, and stress test design."

The CE's activation trigger per agents.md: "Before ADR-009 authoring begins; when Phase 1
baseline benchmarks are commissioned."

Issue #514 exists. The benchmarks are commissioned. The activation trigger has been met.

But CE is defined-inactive, with the EL as gate-keeper until activation. No mechanism converts
"Issue #514 filed" into "CE activated." The PM Agent HORIZON does not audit defined-inactive
agent activation triggers against open issues. No agent has a standing obligation to flag that
the CE's activation trigger has been satisfied.

The failure mode: Issue #514 sits on the M10 board without a CE working on it, because the CE
was never formally activated, because no one noticed the activation trigger had fired. This is
NM-020's contributing factor (the Chief Engineer is defined-inactive) recurring in a different
form — this time inside M10 rather than across milestone boundaries.

**Recommendation:**
Two parts:

1. **Immediate:** At M10 kickoff, the EL explicitly activates the Chief Engineer for Phase 1
   baseline benchmarks (Issue #514). This is an EL decision — the gate-keeper role is the EL.

2. **Process:** Add to the PM Agent HORIZON sweep: "For each Defined-inactive agent, check
   whether any open issue matches that agent's activation trigger. If yes, flag for EL
   activation decision." This is a HORIZON step 7 addition.

**Filed:** Issue #[TBD-F004]

---

### F-005 — Mode 3 Compatibility Has No Standing Implementation Gate

**Severity:** Medium
**Type:** Process gap — architectural commitment without an enforcement mechanism

**Finding:**
CLAUDE.md UX commitment 5: *"The control plane layout zone is reserved before the control plane
is built. Mode 3 requires a dedicated screen zone for control inputs. That zone is reserved in
the layout from M9 onward — not retrofitted when Mode 3 arrives."*

M10 is heavy frontend implementation work (instrument cluster redesign, TrajectoryView, MDA
Alert Panel, PMM + Four-Framework). Every frontend PR in M10 has the potential to violate the
Mode 3 zone reservation — not through malice but through incremental layout decisions that
individually seem innocuous and collectively erode the reserved zone.

The UX Designer defined the zone. The Frontend Architect owns implementation. But the Frontend
Architect's working agreement and pre-PR checklist (Implementation Agents Pre-PR Checklist, item
5 as of PR #519) does not include a Mode 3 zone verification step.

The failure mode is exactly the retrograde pattern CLAUDE.md warns against: the zone is
nominally reserved but incrementally violated across M10 PRs, and Mode 3 arrives in M12 to find
the zone occupied by committed layout elements that must be restructured.

**Recommendation:**
Add to the Frontend Architect's working agreement pre-PR checklist: "For any PR modifying layout
zones or component positioning: verify that the Mode 3 control plane zone (as specified in
`docs/ux/information-hierarchy.md`) is not occupied by any element in this PR's changes."

This is a two-sentence addition. It converts an architectural commitment in CLAUDE.md into a
standing implementation gate.

**Filed:** Issue #[TBD-F005]

---

### F-006 — DIC Blind Interview Protocol Not Encoded in Individual Member Working Agreements

**Severity:** Medium
**Type:** Working agreement coherence gap — mandatory process not visible at point of activation

**Finding:**
The DIC blind interview process (NM-013) states: "All nine DIC members are independently
interviewed before major architectural decisions. Each is asked cold — with no prior exposure to
existing design choices — whether the approach will serve the intended users."

This process is documented in:
- `docs/process/council-interview-prompt.md`
- `docs/process/agents.md §Domain Intelligence Council` (general DIC activation guidance)

But individual DIC member activation patterns (from CLAUDE.md) are:
```
Development Economist: [SCENARIO|CHALLENGE|VALIDATE] — [topic]
```

There is no `BLIND_INTERVIEW` mode in any individual DIC member's activation signature. An agent
(e.g., the Architect Agent preparing an ADR) that activates the Development Economist directly
using `Development Economist: CHALLENGE — [ADR topic]` bypasses the Council Orchestrator and
the blind interview protocol.

This is the structural precondition for NM-006 recurring in DIC form: the panel was wrong
because the consultation structure was inherited from a prior context. If an agent can activate
DIC members directly without the CO's blind interview coordination, the "independently interviewed
before major decisions" principle depends on the activating agent knowing to route through the CO.

**Recommendation:**
Add to each DIC member's activation pattern documentation: "When activated as part of a pre-ADR
review, this agent must be activated through the Council Orchestrator's blind interview protocol,
not directly. Direct activation (`Development Economist: CHALLENGE`) is for episodic consultation
on specific questions, not for pre-ADR foundational review." This encodes the protocol at the
point of use.

**Filed:** Issue #[TBD-F006]

---

### F-007 — Issue #278 (Technocratic Emigration) Has No Owner and No Triage Verdict

**Severity:** Medium
**Type:** Orphaned issue — domain gap directly relevant to Layer 3 asymmetry, no agent
has claimed it, no triage has assigned it or closed it

**Finding:**
Issue #278: "research: technocratic class emigration as feedback loop — sovereign crises destroy
the analytical capacity to use WorldSim." Open, unassigned, labeled M9 (closed milestone).

This issue addresses the third layer of information asymmetry directly: during the crises WorldSim
is designed to address, the institutional capacity of the government using the tool degrades in
real time. Economists emigrate. Staff with analytical training leave. The five-person team becomes
a three-person team. The tool's usability depends on institutional capacity that the crisis is
actively destroying.

This is not a research curiosity — it is a modeling question. Does WorldSim's engine model the
degradation of the government's own analytical capacity as a feedback loop? The "Coffin Corner"
aviation failure mode (the aircraft's performance envelope narrows to a sliver at high altitude)
is the direct analogue: as the crisis deepens, the decision-maker's capacity to use the tool
narrows precisely when the tool's guidance is most critical.

The issue has been open since approximately M6-M7. It was labeled M9 but received no work in
M9. Its milestone needs reassignment.

**Recommendation:**
Triage as M10 NEXT MILESTONE or M11, and assign to Development Economist + Political Economist
for a joint SCENARIO session. Frame the research question as: "Does the simulation engine need
a governmental capacity degradation term, and if so, where does it live in the propagation
model?" This converts an open research question into a scoped analytical task.

**Filed:** Comment on Issue #278 (no new issue needed)

---

## Systemic Observations

### S-001 — Agent Creation Has Shifted from Reactive to Anticipatory, But Two Proposed Agents Remain Stubs

Reading the near-miss registry chronologically:

- **Reactive creations:** PM (NM-001), Data Architect (NM-003/NM-011), UX Designer (NM-010),
  CE (NM-012) — each created after a near-miss revealed a structural gap.
- **Anticipatory creations:** Development Economist (NM-008), Investment Agent (NM-009),
  Community Resilience (NM-009 sequence), CE (NM-012 — anticipatory although reactive in
  trigger) — created before a failure from the EL's pattern recognition.

The trend is positive: the team has moved from reactive gap-filling to anticipatory gap-sensing.
NM-008 through NM-013 are six consecutive anticipatory catches.

But IB and DQ are counterexamples: both needs are clearly derivable from existing requirements
without waiting for a near-miss (the segregation of duties principle for intent blocks; the
independence requirement for data certification). Yet both remain stubs two milestones after
their needs were identified. This is not a safety culture failure — it is a prioritization gap.
Both should be defined in the M10 kickoff gate, not deferred to "when they are needed."

### S-002 — The RACI Matrix Has No Milestone-Boundary Review Cadence

The file ownership table in `agent-raci.md` is updated reactively (NM-007, NM-021). No
milestone exit gate includes a step: "review RACI matrix for completeness — are all active
agents represented in the file ownership table? Are all recently activated or proposed agents
in the matrix?"

The PI Agent inaugural audit identified this gap when checking PI Agent's own RACI coverage.
This is a structural maintenance gap: the RACI is authoritative for the file authority rule,
but its own currency is not audited on a schedule.

**Recommended addition to MILESTONE_RUNBOOK.md (Issue #503 scope):** "RACI completeness check
— for each agent activated in this milestone, verify that it has at least one R row in the file
ownership table. For each newly proposed agent, verify that a RACI stub is filed."

### S-003 — Four Active Agents Have No Explicit File Ownership Rows

Examining the file ownership table in `agent-raci.md`, four active agents do not appear to have
R rows for any file or directory:

- UX Design Thinking Agent (produces `docs/ux/design-thinking/` artifacts)
- Socratic Agent (produces no persistent artifacts — this may be intentional)
- Security and Review Agent (produces compliance scan entries — SCAN entries, which PI now owns)
- Independent Review Agent (produces DEMO-N issue lists and review documents, but no canonical
  directory is registered in the artifact locations table in CLAUDE.md)

The Socratic Agent is correctly excluded — it produces understanding, not documents.

The others represent either missing file ownership rows or missing canonical artifact locations.
If the IR Agent produces a governance review report, where does it go? If the UX Design
Thinking Agent produces a derivation document, the canonical location is `docs/ux/design-
thinking/` (per existing files), but the RACI does not reflect this.

This is a low-severity gap in isolation — no near-miss has resulted from it. But it creates
ambiguity for the file authority rule: if an agent writes to a document in `docs/ux/design-
thinking/`, which agent holds R, and must be consulted before a PR touches it?

### S-004 — The Founding Document's "Defense, Not Offense" Principle Has a Single Point of Failure

The Security and Review Agent owns dual-use review. This agent's mandate includes: "Is this
feature more useful for executing financial attacks than for defending against them?"

But dual-use concerns do not only arise on security-sensitive features. They can arise in:
- Methodology publication (exposing which calibration parameters can be exploited)
- Scenario output design (outputs that can be repurposed to identify attack vectors)
- Data source disclosure (revealing which country data gaps create exploitable blindspots)

The current activation trigger ("Any feature touching sensitive country data, financial attack
surface modeling, or dual-use concerns") requires the activating agent to recognize dual-use
concerns before activating the Security Agent. If the activating agent doesn't recognize a
dual-use concern, the Security Agent never fires.

This is a single-point-of-failure architecture for the most critical principle in the
Founding Document. A near-miss here would not be a process error — it would be a mission
violation.

**Recommendation:** Add dual-use scan to the PM Agent HORIZON sweep (step 8 candidate): "For
each PR merged since the last HORIZON sweep that added a new analytical capability: verify the
Security Agent was consulted or confirm dual-use concern is absent based on stated criteria."
This converts a reactive activation to a retroactive coverage check — the same pattern used
for file authority (step 5).

---

## GitHub Issues Filed

| Finding | Issue Number | Title | Milestone |
|---|---|---|---|
| F-001 | #521 | `process(agents): Layer 3 asymmetry — define institutional capacity advocate mandate` | M10 |
| F-002 | #522 | `process(agents): backtesting Eureka function — CM gap analysis obligation in working agreement` | M10 |
| F-003 | #523 | `process(agents): IB and DQ must be fully defined before M10 implementation begins` | M10 (kickoff gate) |
| F-004 | #524 | `process(agents): CE activation — Phase 1 benchmark trigger has fired; HORIZON step 7 for defined-inactive agents` | M10 |
| F-005 | #525 | `process(agents): Mode 3 zone compatibility gate in Frontend Architect pre-PR checklist` | M10 |
| F-006 | #526 | `process(agents): DIC blind interview protocol — encode CO routing in individual member activation docs` | M10 |
| S-002 | #527 | `process(raci): RACI completeness check in MILESTONE_RUNBOOK.md milestone exit gate` | M10 |
| S-003 | #528 | `process(raci): file ownership rows missing for UX Design Thinking, Security, and IR agents` | M10 |
| S-004 | #529 | `process(agents): dual-use scan in HORIZON sweep — retroactive coverage check for new capabilities` | M10 |

Issue #278 — existing issue. PI comment filed (#278#issuecomment-4536646673) with triage
recommendation: M11, Development Economist + Political Economist SCENARIO session.

---

## Self-Assessment: PI Lens on This Review

The PI Agent is the author of this document and the subject of some of its findings.
Independence concern: the PI Agent cannot be fully independent when reviewing processes the PI
Agent itself is responsible for maintaining.

**Where this review may be systematically weak:**
- PI Agent's own RACI completeness is assessed (S-003 partial) but not with the same depth as
  other agents' coverage gaps, due to the conflict of interest.
- The inaugural audit (PR #519) found NM-021 and NM-022 — gaps produced in PRs that predated
  PI activation. This review's findings are forward-looking (M10 gaps) not backward-looking
  (PI's own prior gaps). A separate, independent review of PI Agent performance at M11 exit
  would be the correct complement.

**The one finding this review most wants the EL to act on:**
F-001 (Layer 3 asymmetry). The Founding Document's north star is the quinoa farmer who will
never know this tool exists, but whose government may make better decisions because it does.
The tool currently has no standing agent speaking for the government that must make those
decisions with limited analytical capacity. That is the deepest structural gap the agent team
has.

---

*Document filed by Process Integrity Agent (R: `docs/process/audits/`) — 2026-05-25*
