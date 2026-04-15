# Architecture Diagram Library

This directory contains all architecture diagrams for WorldSim. Every diagram
is a [Mermaid](https://mermaid.js.org/) `.mmd` file — text-based,
version-controlled alongside code, and rendered natively by GitHub.

No binary diagram formats (PNG, draw.io, PDF) live here. A diagram that cannot
be reviewed in a pull request is not a diagram — it is an undocumented assertion.

---

## Naming Convention

```
ADR-NNN-diagram-type.mmd
```

Examples:
```
ADR-001-class-diagram.mmd          ← data model for simulation core
ADR-002-schema-diagram.mmd         ← PostGIS database schema
ADR-003-sequence-event-propagation.mmd  ← event flow through the engine
ADR-004-state-coffin-corner.mmd    ← Coffin Corner failure mode transitions
```

The `ADR-NNN` prefix ties each diagram to its Architecture Decision Record
in `docs/adr/`. The diagram-type suffix identifies what kind of structural
question the diagram answers.

---

## Diagram Types by Use Case

| Subject | Mermaid Type | Example filename |
|---|---|---|
| Data models and class relationships | `classDiagram` | `ADR-001-class-diagram.mmd` |
| Request / event flows between modules | `sequenceDiagram` | `ADR-003-sequence-event-propagation.mmd` |
| Failure modes and regime transitions | `stateDiagram-v2` | `ADR-NNN-state-coffin-corner.mmd` |
| System component topology | `graph TD` or `graph LR` | `ADR-NNN-component-graph.mmd` |
| Ingestion pipeline flows | `flowchart TD` | `ADR-NNN-ingestion-flow.mmd` |
| Deployment and infrastructure | `graph LR` | `ADR-NNN-deployment.mmd` |

---

## How Diagrams Relate to ADRs

Every ADR in `docs/adr/` must have at least one diagram in this directory.
The ADR text references the diagram file. The diagram captures the structural
decision visually in a way that prose cannot — it forces precision and makes
the decision reviewable.

When an ADR is **accepted**, its diagram is created in the same pull request.

When a module interface changes — and a new ADR or ADR amendment is written —
the diagram is updated in the same commit as the interface change. A pull
request that changes a class signature, a data flow, or a state transition
without updating the corresponding diagram will not be merged.

The diagram update requirement is not optional documentation hygiene. It is
a review gate. Reviewers check that diagrams match the code.

---

## Rendering Diagrams Locally

GitHub renders Mermaid diagrams natively in markdown and `.mmd` files.

To render locally for development:

```bash
npm install -g @mermaid-js/mermaid-cli
mmdc -i docs/architecture/ADR-001-class-diagram.mmd -o /tmp/diagram.svg
open /tmp/diagram.svg
```

Or use the VS Code Mermaid Preview extension, which renders `.mmd` files inline.

---

## Current Diagrams

| File | ADR | What it shows |
|---|---|---|
| `ADR-001-class-diagram.mmd` | ADR-001 | Simulation core data model: SimulationEntity, SimulationState, Event, Relationship, SimulationModule |
| `ADR-001-flowchart-mutable-state-problem.mmd` | ADR-001 | Why mutable state creates non-determinism; how immutable state + events solves it |
| `ADR-001-sequence-timestep-cycle.mmd` | ADR-001 | Full timestep cycle: engine calls modules, collects Events, applies deltas to State[T+1] |
| `ADR-001-flowchart-event-propagation.mmd` | ADR-001 | How a single Event propagates through the relationship graph with attenuation across hops |

*This table is updated when diagrams are added. New diagrams added without
updating this table will be flagged in pull request review.*
