# Independent AI Stakeholder Review — Reusable Prompt Template

> Pattern documented after M6 demo recording session 2026-05-07.
> This pattern produced DEMO-001 through DEMO-010, which correctly identified
> four critical issues sharing a single root cause (Issue #227).
>
> Apply before: any stakeholder demo, any milestone exit ceremony, any
> methodology publication submission.

---

## Why This Works

A fresh Claude instance with only documentation artifacts as context has no
institutional memory of decisions made, no stake in the outcome, and no
developed affinity for the work. The independence is real. It will apply
domain expertise and UX judgment without the sunk-cost framing that
accumulates in a development session.

The four design decisions that make this different from asking the
development agent to self-review:

1. **No technical knowledge instruction.** The reviewer is explicitly told it
   cannot see source code, only the live application. This forces evaluation
   from the user's perspective, not the implementer's perspective.

2. **Domain expertise framing.** The reviewer is cast as a policy analyst or
   finance ministry counterpart — the canonical user from `CLAUDE.md`. This
   activates domain judgment about whether outputs are legible and useful,
   not just technically present.

3. **Early permission to be critical.** Given explicitly before the review
   begins. Without this, language models default toward encouragement. The
   permission statement shifts the prior.

4. **Root cause analysis closing requirement.** After individual issues,
   the reviewer must identify shared root causes. This surfaces systemic
   patterns (e.g., "four of these issues have the same root cause: no
   scheduled inputs") that item-by-item review misses.

---

## Message 1 — Context Setting

Send this first, before attaching any screenshots or asking any questions.

```
You are reviewing WorldSim — an open-source geopolitical-economic simulation
platform designed to give finance ministries and vulnerable-country governments
the same quality of scenario analysis that sophisticated institutional actors
(IMF, World Bank, sovereign wealth funds) bring to negotiations.

The canonical user is a finance ministry specialist sitting across a table
from an IMF negotiating team. The tool gives her analytical standing: scenario
modeling, human cost consequence outputs, historical pattern recognition.
The mission is documented at: https://github.com/PublicEnemage/worldsim

Relevant artifacts for this review:
- Demo walkthrough script: docs/demo/stakeholder-walkthrough.md
- Project mission and principles: CLAUDE.md §Guiding Principles
- Public methodology position: docs/POLICY.md

You have no access to source code. You will evaluate the live application
from screenshots only — exactly as a domain expert stakeholder would experience
it in a demo session.

Before I share the screenshots: you have full permission to be direct and
critical. This is a pre-demo review. Identifying problems now is more valuable
than encouragement. Do not soften findings.
```

---

## Message 2 — Review Task

Send after Message 1, with screenshots attached in sequence.

```
I am attaching [N] screenshots from a live run of the WorldSim stakeholder
demo. The screenshots follow the sequence in docs/demo/stakeholder-walkthrough.md
§Section 2. Each screenshot is labeled with its step number.

You are a senior policy analyst who has worked on fiscal adjustment programmes
for the last fifteen years. You have sat on both sides of IMF negotiations.
You understand conditionality frameworks, fiscal multipliers, and what
analytical outputs are actually useful in a negotiation room versus what looks
impressive in a slide deck.

Your task has four parts:

**Part 1 — Narration vs. visual match**
For each step, evaluate whether the visual output matches what the narration
claims. The narration script is in docs/demo/stakeholder-walkthrough.md.
Flag any step where the visual contradicts, undermines, or fails to support
the narration. Be specific: "Step 4 narration says X, visual shows Y."

**Part 2 — Domain expert UX feedback**
As the policy analyst described above, evaluate whether the outputs are
legible and useful to you. Not whether they are technically present — whether
you could actually use them. Specific questions to consider:
- Would the choropleth color scheme communicate anything meaningful to you?
- Would the MDA alert panel give you a finding you could cite in a negotiation?
- Would the radar chart tell you which dimensions are under stress?
- Would the compare mode give you evidence for a counter-proposal?

**Part 3 — Structured issue list**
For each problem identified in Parts 1 and 2, produce a structured entry:

  DEMO-[N]: [one-line title]
  Severity: CRITICAL / HIGH / MEDIUM / LOW
  What the audience sees: [description]
  What they should see: [description]
  Root cause hypothesis: [your best guess at the underlying cause]

**Part 4 — Summary table and root cause analysis**
Produce a summary table: | ID | Severity | One-line description |

Then answer: do any of these issues share a root cause? If yes, identify the
shared root cause and list which issues it explains. A shared root cause
that explains multiple CRITICAL/HIGH issues is the highest-priority fix —
more important than fixing each issue individually.
```

---

## When to Apply This Pattern

**Before any stakeholder demo.**
Run 24–48 hours before the demo. File issues from the output. Fix CRITICAL
items before the session. HIGH items should be acknowledged honestly in the
narration if unfixed.

**Before any milestone exit ceremony.**
Apply to the exit checklist itself, not just the software. Provide the
checklist and the ADRs as context. Ask: "What would a sceptical external
reviewer say is missing or overstated?"

**Before any methodology publication submission.**
Provide the methodology document and the backtesting results. Ask: "As a
development economist who will cite this work, what would make you decline
to cite it? What would make you cite it with a caveat?"

**After any significant feature ships.**
Provide the user journey documentation and screenshots of the new feature.
Ask: "Does this feature serve the canonical user (finance ministry
specialist in a negotiation), or does it serve a different user?"

---

## Adapting the Pattern

### Code Review Variant

Replace the domain expert framing with a security or reliability framing:

```
You are a senior engineer who has never seen this codebase. You are reviewing
a pull request. You have no context on why decisions were made. Evaluate
only what is in front of you. Your job is to find what would break in
production, not to validate what the author intended.
```

Append the root cause analysis requirement unchanged.

### Governance Review Variant

Replace the domain expert framing with an institutional trust framing:

```
You are an external governance advisor evaluating whether this project's
decision-making process is trustworthy enough for a finance ministry to
rely on its outputs. You are not evaluating the technical quality —
you are evaluating whether the process that produced the outputs is
auditable, accountable, and free of conflicts of interest.
```

Provide: CLAUDE.md §Governance, docs/COMPLIANCE.md, the milestone exit
checklist, and the compliance scan registry.

### User Testing Variant

Replace the domain expert framing with a first-time-user framing:

```
You have just been handed this tool by a colleague who said "this might be
useful for your programme work." You have five minutes before a meeting.
You have read nothing about it. Walk through what you would do, what you
would be confused by, and at what point you would give up and close the tab.
```

Omit the structured issue format. Ask instead for a narrative walkthrough
of confusion points in the order they occur.

---

## Output Handling

Issues produced by the independent review should be:
1. Filed in GitHub with `bug` or `documentation` label as appropriate
2. Assigned to the current milestone if they block a deliverable in scope
3. Triaged by the PM Agent (TRIAGE mode) before being acted on

The review output is evidence, not a work order. The Engineering Lead
decides which issues to act on and when.

### Storage Convention (Issue #234)

Every stakeholder review produces a permanent artifact committed to the repository.
Canonical location: `docs/demo/{milestone}/reviews/YYYY-MM-DD-vX.X.X-stakeholder-review.md`

Example: `docs/demo/m10/reviews/2026-05-30-v0.10.0-stakeholder-review.md`

This path matches the CLAUDE.md §Canonical Artifact Locations table and the
`docs/demo/{milestone}/reviews/*-stakeholder-review.md` file ownership row in
`docs/process/agent-raci.md` (IR Agent holds Responsible).

### Report Template

The review instance writes the findings section. The development instance
adds issue numbers and status before committing. Template:

```markdown
# Stakeholder Review — vX.X.X (YYYY-MM-DD)

**Scenario run:** [scenario name and configuration]
**Reviewer role context:** [persona applied — e.g., Lucas Ferreira, Programme Analyst]
**Mode exercised:** [Mode 1 / Mode 2 / Mode 3]

## Findings

| # | Area | Finding | Severity | GitHub Issue | Status |
|---|---|---|---|---|---|
| 1 | [UI / Data / Narrative / Methodology] | [finding description] | [Critical / Major / Minor / Observation] | #NNN | [Open / Fixed / Won't Fix] |

## What Worked

[Narrative — what the tool communicated clearly and correctly]

## What Confused or Misled

[Narrative — confusion points in the order they occurred; include at what point
a real user would abandon the task]

## Blocking Items for Next Demo

[List any findings that must be resolved before the next milestone demo]
```

### Handover Protocol

The two-instance protocol closes the loop between review and development:

1. **Review instance** — runs the scenario, applies the persona, writes findings
   in the template above. Leaves GitHub Issue column as `UNTRACKED` where not yet filed.
2. **Development instance** — receives the completed findings section, files GitHub
   issues for each finding, fills in the Issue column, updates Status for any findings
   already addressed in the current milestone, and commits the completed artifact to
   `docs/demo/{milestone}/reviews/`.

The committed artifact is the permanent audit trail of stakeholder feedback alongside
the code that addresses it. A review that produces findings but no committed artifact
has not completed the handover.

---

*Pattern documented from M6 session 2026-05-07. Related issues: #227–#232, #234.*
