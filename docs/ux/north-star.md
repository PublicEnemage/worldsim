# UX North Star

> Owned by the UX Designer Agent. This document is the authoritative source
> for who we are building for, what they are trying to do, and what the
> experience must make possible. All frontend decisions are evaluated against
> it. Last updated: 2026-04-27 (stub — open questions to be resolved before
> M6 frontend work begins).

---

## Canonical User

A debt restructuring specialist at a finance ministry. They are working
alongside IMF staff on a program design — not as a passive recipient of
conditionality terms, but as a counterpart who needs to understand the
structural implications of what is being proposed and where the proposed
path becomes politically and humanly unsustainable.

They have a graduate-level economics background. They are not a data
scientist. They do not have time to learn a new analytical tool from
scratch during an active negotiation. They need to get to the relevant
signal in minutes, not hours.

They are operating under cognitive load. There are people in the room,
a document on the table, and a clock running. The tool must work for
them in that context, not in a calm research environment.

---

## Primary Use Case

Understanding whether a proposed fiscal adjustment path crosses human
cost thresholds that would make the program politically and socially
unsustainable — and being able to articulate specifically which
indicators cross which thresholds, at what point in the program
timeline, and for which population cohorts.

The output of this use case is not a chart. It is a defensible argument
in a negotiation: "This path produces these human consequences by year
three, which in comparable historical cases produced political
instability that caused program collapse. Here is the evidence."

The tool exists to give the finance ministry the same analytical
standing as the institution sitting across the table.

---

## Open Questions (to be resolved before M6 frontend work begins)

**1. Primary cognitive task when reading a distribution output**

When the user scans a scenario output showing distributions across
multiple indicators, what is their primary cognitive task? Are they
looking for threshold crossings (has any indicator breached a floor),
trajectory shapes (where is this heading if nothing changes), or
scenario comparisons (how does this path compare to the alternative
we proposed)?

The answer determines the primary visual grammar of the output — alarm
indicators, trajectory lines, or comparison panels — and only one of
these can be primary. Everything else is secondary.

**2. Information needs during active negotiation vs. preparation**

Does the user's relationship to the tool change between a preparation
session (the night before, exploring the full scenario space) and an
active negotiation session (tablet open on the table, needing a specific
number in 90 seconds)?

If these are distinct modes, they may require distinct information
hierarchies. The preparation view surfaces the full distribution and
supports exploration. The negotiation view surfaces the specific threshold
crossing with its supporting evidence. Designing for one collapses the
other.

**3. How the user experiences the human cost ledger professionally**

Does a finance ministry official experience the human cost indicators
as confirming concerns they already hold (making the data a negotiating
tool that is aligned with their professional identity), as evidence they
did not previously have access to (making the tool genuinely informative),
or as a constraint they are being asked to manage alongside fiscal
targets (making the human cost ledger feel adversarial to their role)?

The answer shapes whether human cost data should be presented as warning
signals (adversarial framing, "this crosses a floor"), as evidence
(neutral framing, "this is what the data shows"), or as capability
analysis (aligned framing, "this is what this path does to the people
your ministry serves"). All three are true simultaneously. Only one
should be primary.
