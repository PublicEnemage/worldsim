# WorldSim Scenario Library

The scenario library is the collection of structured scenario specifications
that define what the simulation is asked to model, how it is seeded, and how
we know whether it got anything right.

A scenario specification is not code. It is a design document that precedes
implementation — the structured expression of what we are trying to learn,
what inputs we are injecting, what direction of effects we expect, and what
the simulation cannot yet model. Writing the specification before running
the simulation forces clarity about the question being asked. Running the
simulation first and writing the specification after inverts causation.

---

## What a Scenario Specification Is

A scenario specification is a complete description of one simulation run:

1. **Classification** — what kind of scenario, what modules it requires,
   what modules it cannot use yet.

2. **Historical grounding** — what precedent cases this scenario draws from,
   and the important ways this scenario differs from those precedents.

3. **Initial conditions** — the starting state of each entity, with data
   sources cited by dataset name, release, and access date. Not "World Bank"
   but "World Bank WDI 2024 release, accessed 2026-04-16".

4. **Injected events** — the `ControlInput` specifications that define the
   exogenous shocks: who acts, when, with what instrument, at what magnitude.

5. **Expected direction of effects** — what direction the simulation should
   move key indicators, based on economic theory and historical precedent.
   Direction, not magnitude. The simulation is not a prediction engine.

6. **Domain Intelligence Council review** — at least three council agent
   perspectives documenting what each framework reveals and flags as
   concerning. Written before the simulation runs.

7. **Validation approach** — how we evaluate whether the simulation got it
   directionally right, with specific variables and sources.

8. **Known model limitations** — explicit documentation of what the current
   simulation cannot model, and why that matters for interpreting results.

---

## Scenario Status Values

| Status | Meaning |
|---|---|
| `PROPOSED` | Specification drafted, not yet reviewed |
| `REVIEWED` | Council review complete, ready to implement |
| `ACTIVE` | Currently being run or actively developed |
| `VALIDATED` | Run against historical record, fidelity documented |
| `ARCHIVED` | Superseded or no longer maintained |

A scenario moves from PROPOSED to REVIEWED only after at least three Domain
Intelligence Council agents have completed their review sections. A scenario
moves to VALIDATED only after a backtesting run has been completed and the
results documented in `docs/compliance/scan-registry.md`.

---

## Directory Structure

```
docs/scenarios/
    README.md                           # this file
    template.md                         # scenario specification template
    module-capability-registry.md       # what the simulation can and cannot model
    proposed/
        USA-tariff-escalation-2025.md   # first demo scenario
    reviewed/
        (scenarios that have passed council review)
    active/
        (scenarios currently running or in development)
    validated/
        (scenarios with documented backtesting results)
    archived/
        (superseded or retired scenarios)
```

---

## Domain Intelligence Council Interaction

Before any significant simulation result from a scenario is presented as
meaningful, at least three Domain Intelligence Council agents must have
reviewed the specification. The council review sections in the template
are filled in before the simulation runs — not after. Post-hoc council
review that has already seen the output is not independent analysis.

The council review sections are not a formality. They are the primary
mechanism through which competing analytical frameworks surface tradeoffs
that no single framework can see. A scenario specification whose council
sections are empty or contain only "N/A" has not been properly reviewed
and should not be used to inform policy analysis.

---

## Adding a New Scenario

1. Copy `template.md` to `proposed/[ISO3-country]-[event-type]-[year].md`
2. Fill in all sections completely. Leave no section empty.
3. Check `module-capability-registry.md` — document explicitly what your
   scenario requires that is not yet built.
4. Activate at least three Domain Intelligence Council agents and complete
   their review sections before marking the scenario as REVIEWED.
5. Open a GitHub Issue linking to the specification if the scenario requires
   new simulation modules or data sources not yet in the codebase.
