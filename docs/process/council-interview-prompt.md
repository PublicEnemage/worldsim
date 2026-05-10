# Domain Intelligence Council Blind Stakeholder Interview — Prompt Template

> Related issue: #235
> Gate condition: must be completed before ARCH-REVIEW-005 (Issue #218) is authored.
> Follow-on artifact: docs/process/council-interview-YYYY-MM-DD.md

---

## Section 1 — Overview

### What This Interview Is

A structured blind interview of each Domain Intelligence Council member on the foundational question the project has not yet asked them directly: **does this approach actually work for the people it is designed to serve, and are we building the right thing?**

Each council member is interviewed independently in a fresh chat instance with no development history, no ADR context, and no knowledge of decisions already made. The independence is structural, not nominal — the member receives only what a domain expert outside the project would have access to.

### Why the Blind Design Matters

Throughout M1–M6, council members have been used in a bounded technical role: validating ADR decisions, contributing domain citations, flagging methodological gaps within a specified scope. That use is valuable but produces a specific failure mode — domain experts who have read the implementation decisions tend to validate them, because the framing of the question already encodes the answer. The blind design removes that framing.

A council member who has read ADR-005 will evaluate the four-framework measurement approach within the constraints ADR-005 establishes. A council member who has not read ADR-005 will evaluate whether the approach is the right one in the first place. These are different questions. Only the second one is useful at M8 entry.

### When to Run

- **M8 entry gate** — required before ARCH-REVIEW-005 (causal meta-map) is authored. Council feedback is an input to architectural decisions, not a post-hoc validation.
- **Before any methodology publication submission** — external reviewers will ask the same three questions; surface their likely objections before submission.
- **After any significant expansion of scope** — if the simulation adds a new resolution level (subnational, demographic cohort), interview the council members whose frameworks are most affected.

### How This Differs from Prior Council Use

| Prior use | This interview |
|---|---|
| Bounded technical validation within an ADR scope | Foundational validity question with no scope constraint |
| Council member reads the implementation before responding | Council member receives only mission and methodology summary |
| Question: "Is this ADR decision sound?" | Question: "Is this approach addressing the right problem?" |
| Validation of decisions made | Input to decisions not yet made |

---

## Section 2 — Context Package

Send this context to each council member before the interview prompt. Send it as a single message and ask them to confirm they have read it before you send the interview questions.

**Do not share:** ADRs, implementation decisions, governance documents, the milestone roadmap, or any artifact that encodes decisions already made. The value of this exercise is uncontaminated domain judgment.

---

### Context Package — Exact Text to Send

```
Before I ask you three questions, I want to give you context on the project
you are being asked to evaluate. Please read this in full and confirm when
you are ready for the questions.

---

## What WorldSim Is

WorldSim is an open-source geopolitical-economic simulation platform designed
to level the playing field between sophisticated financial and political actors
and the governments, communities, and people most vulnerable to their actions.

It is a flight simulator for national decision-making.

The mission is to give a finance minister sitting across from an IMF negotiating
team the same quality of scenario analysis, risk assessment, and historical
pattern recognition that the most sophisticated sovereign wealth funds and
financial institutions currently reserve for themselves.

The tool exists for the quinoa farmer in Bolivia who will never know it exists,
but whose government may make better decisions because it does.

## The Canonical User

A finance minister in a small, vulnerable country is sitting across a table
from an IMF negotiating team. They have limited time, limited staff, and
generational consequences riding on the decision they are about to make.

Every design decision is evaluated against this question: does this make the
tool more useful to that person in that moment?

## Methodological Commitments

The full methodology position is at: https://github.com/PublicEnemage/worldsim/blob/main/docs/POLICY.md

Key commitments relevant to your evaluation:
- The simulation produces distributions, not point predictions. Uncertainty is
  displayed, not hidden.
- Outputs are simultaneously measured in four frameworks: financial, human
  development, ecological, and governance. No master conversion rate between
  them — false aggregation is not acceptable.
- The model's blindspots are documented and visible to users.
- Backtesting against historical cases is the primary validation discipline.
  The gap between model output and historical outcome is the signal for
  improvement, not a failure to hide.

## Backtesting Results — Five Historical Cases (v0.6.0)

The simulation has been validated against five historical crisis cases, each
representing a distinct crisis mechanism:

| Case | Period | Mechanism | Fidelity threshold | Result |
|---|---|---|---|---|
| Greece | 2010–2012 | Fiscal consolidation under external conditionality | DIRECTION_ONLY | Pass — contraction predicted at each step |
| Argentina | 2001–2002 | Sovereign default and currency crisis | DIRECTION_ONLY | Pass — contractionary dynamics captured |
| Lebanon | 2019–2020 | Compound banking/currency/sovereign crisis + external shock | DIRECTION_ONLY | Pass — contraction at both steps |
| Thailand | 1997–2000 | Externally induced currency speculative attack | DIRECTION_ONLY | Pass — contraction in both crisis years |
| Ecuador | 1999–2000 | Banking collapse, hyperinflation, dollarization | DIRECTION_ONLY | Pass — contraction at step 1; no deeper contraction at step 2 |

DIRECTION_ONLY means the model is tested on whether it gets the sign right
(did GDP go down or up?). Magnitude calibration is the next validation layer
and has not yet been completed.

## The Four-Framework Measurement Approach

Rather than producing a single composite score, WorldSim measures scenario
outputs simultaneously across four frameworks — financial (GDP trajectory,
fiscal balance, debt sustainability), human development (poverty headcount,
health system capacity, education access), ecological (planetary boundary
proximity, natural capital depletion), and governance (institutional quality,
rule of law, political freedom). These four frameworks are displayed as a
radar chart. No aggregate score collapses them — a programme that achieves
fiscal stability while producing governance deterioration is required to show
both, not a weighted average that obscures either. Hard floors (Minimum
Descent Altitudes) fire unconditionally when any dimension crosses a critical
threshold, regardless of performance in other dimensions.

---

Please confirm when you have read this context and I will send you three
questions.
```

---

## Section 3 — Interview Prompt

Send this after the council member confirms they have read the context package. Substitute `[ROLE]` with the council member's title.

---

### Interview Prompt — Exact Text to Send

```
You are the [ROLE] on the WorldSim Domain Intelligence Council. Your role
speaks for [domain] — you evaluate simulation design from that perspective,
not from a technical implementation perspective.

I am going to ask you three questions. For each, I want a direct answer that
prioritises what is missing or wrong over what is working. The value of this
exercise is in the gaps and challenges, not the affirmations. Do not soften
findings or hedge toward encouragement. If an aspect of the approach is
inadequate from your domain perspective, say so directly.

---

**Question 1 — Validity**

Does this approach address the problem as you understand it from your domain
expertise?

I want to know: what is the approach getting right, and what is it missing
entirely? Not missing in the sense of "this could be improved" — missing in
the sense of "a domain expert in your field would consider this approach
incomplete or inadequate without it." If the four-framework measurement
approach has a fundamental gap from your perspective, name it. If the
backtesting case selection has a systematic bias, name it. If the canonical
user description does not match the actual decision-maker in the situations
this tool is designed for, say so.

Expected depth: one substantive paragraph. Concrete, not general.

---

**Question 2 — Credibility**

If a finance ministry analyst used this tool in a real negotiation with the
IMF, would the outputs be defensible?

Specifically: what would a sophisticated counterparty challenge first? The IMF
programme team is not naive — they have their own models and will probe the
methodology. What is the weakest point in the approach as presented? What
claim does this tool implicitly make that a competent counterparty would
immediately contest? If the DIRECTION_ONLY fidelity threshold is insufficient
for a real negotiating context, say so and explain why.

Expected depth: one substantive paragraph identifying the single most
challengeable element, with enough specificity that a development team could
act on it.

---

**Question 3 — Priority**

If you could add one capability to this model in the next development phase
that would most increase its real-world usefulness for the canonical user,
what would it be?

Not the most technically interesting addition. Not the most conceptually
elegant. The one that, in a real negotiation room, would make the most
difference to the finance ministry analyst sitting across from the IMF team.
The addition that would give her a finding she does not currently have and
cannot easily get elsewhere.

Expected depth: one paragraph naming the capability, one sentence explaining
why this one above all others.

---

**Final request — one finding the team may not have considered**

After answering the three questions: what is the single most important thing
about this domain — a dynamic, a constraint, a historical pattern — that you
believe the development team is unlikely to have factored in, and that would
change the design if they had? This can be brief. It does not need to map to
a specific question above. It is the thing you would say if you had five
minutes with the team before they locked the next milestone's scope.
```

---

## Section 4 — Synthesis Instructions

### Collection Protocol

1. Run all nine interviews before comparing any responses. Open each in a
   separate chat instance. Do not share responses between instances.
2. Record each response verbatim in a working document before synthesis begins.
3. Note the council member role alongside each response so attributions are
   preserved in the synthesis.

### Analysis Steps

**Step 1 — Individual summaries**
For each council member, write a three-sentence summary: one sentence per
question, capturing the core finding. Keep the role attribution.

**Step 2 — Cross-cutting themes**
A theme is cross-cutting if three or more council members independently raise
the same gap, challenge, or priority — without having seen each other's
responses. These are the highest-signal findings. List each theme with the
council members who raised it.

**Step 3 — Contradictions**
Where council members contradict each other, do not resolve the contradiction.
Surface it explicitly. Contradictions between domain experts on a
methodological question are genuine tensions, not errors to correct. They
require a design decision, not a synthesis. Flag each contradiction for the
Engineering Lead.

**Step 4 — Priority ranking**
Rank the Priority question responses by: (a) number of council members who
named the same or similar capability, and (b) alignment with the canonical
user's actual decision context. Note where the ranking from (a) and (b)
diverge — that divergence is itself a finding.

**Step 5 — M8 scope impact**
For each cross-cutting theme and top-ranked priority: does it belong in M8
scope, or is it a later milestone? Apply the PM Agent TRIAGE verdicts
(BLOCKING NOW / THIS MILESTONE / NEXT MILESTONE / PARKING LOT). File a
GitHub issue for any gap that belongs in M8.

### Output Document Structure

Save to `docs/process/council-interview-YYYY-MM-DD.md`. Follow the handover
artifact convention from `docs/demo/reviews/`:

```markdown
# Domain Intelligence Council Interview — YYYY-MM-DD

## Interview Conditions
[Date, milestone context, gate condition this satisfies]

## Individual Responses

### [Role]
**Validity:** [one-sentence summary]
**Credibility:** [one-sentence summary]
**Priority:** [one-sentence summary]
**Unprompted finding:** [verbatim or close paraphrase]

[repeat for all nine]

## Cross-Cutting Themes
[Theme 1 — raised by: Role A, Role B, Role C]
[Theme 2 — ...]

## Contradictions Requiring Design Decisions
[Contradiction 1 — Role A says X, Role B says Y]

## Priority Ranking — Capability Additions
| Rank | Capability | Raised by | M8 fit |
|---|---|---|---|

## Recommended M8 Scope Impact
[Bullet list of scope additions, removals, or reframings the interview supports]

## Issues Filed
[List of GitHub issue numbers and titles filed from this synthesis]
```

### When to File Issues

File a GitHub issue for any finding that:
- Names a missing capability that belongs in M8 scope
- Identifies a credibility gap that should be closed before methodology publication
- Surfaces a contradiction that requires an explicit ADR decision

Do not file issues for findings that are already in scope, already filed, or
belong in a later milestone. TRIAGE first, then file.

---

*Pattern documented 2026-05-08. Gate condition: #235. Related: docs/process/independent-review-prompt.md*
