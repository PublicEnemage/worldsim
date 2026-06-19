# Zone 1A Information Architecture — Phase 1 Design Thinking

> **Author:** UX Designer Agent
> **Date:** 2026-06-18
> **Issue:** #845 — Zone 1A information architecture — multi-dimensional encoding
> **Phase:** Phase 1 — Design Thinking Document (of four phases)
> **Intent document:** `docs/process/intents/M14-G6c-2026-06-18-zone-1a-design-thinking.md`
> **Status:** Phase 1 complete. Gates Phase 2 Architecture Review at M15 kickoff.
>
> **Governing documents read:**
> - `docs/ux/north-star.md §Primary Cognitive Tasks by Mode`
> - `docs/ux/information-hierarchy.md §Dashboard View Hierarchy`
> - `docs/ux/design-thinking/worldsim-ux-architecture-first-principles.md §Question 1`
> - `CLAUDE.md §UX Architectural Commitments` (commitments 1–5)
> - `docs/ux/user-journeys.md §Journey B` (Reactive entry state)
> - `docs/ux/personas.md §Persona 2` (Finance Ministry Negotiator)

---

## Purpose of This Document

Zone 1A is the primary flight instrument: the four-framework composite score trajectory view on a shared step axis. Its current encoding contract — one line per framework, all four simultaneously visible, one entity at a time — was designed for a single cognitive task in a single-entity scenario.

That contract is now under pressure from four simultaneous dimensions:

| Dimension | Current M14 scope | At scale |
|---|---|---|
| Frameworks | 4 (fixed) | 4 (fixed) |
| Entities | GRC, JOR, EGY, ZMB (4 entities; entity selector scopes view to one) | Unbounded |
| Branches | Mode 3: baseline ghost + active trajectory | Multiple what-ifs in future |
| Modes | 3 distinct cognitive tasks with different time ceilings | Fixed at 3 |

At the Hormuz scenario scale (2 entities simultaneously visible, Mode 3 baseline + active): **4 × 2 × 2 = 16 lines** on one axis. At 3 entities, 2 branches: **4 × 3 × 2 = 24 lines**. No labeling scheme makes 24 same-axis lines legible in 15 seconds.

The current architecture handles N=1 entity in Mode 1 and Mode 2 correctly. It begins to fail at N=2 in Mode 3. It fails completely at N≥3 in any mode.

**The governing question for Phase 1:** What is the single Persona 2 question Zone 1A must answer, in each mode, within the mode's time ceiling? Encoding channels and information allocation follow from the answer. They cannot be designed before the question is answered.

This document answers that question for each mode, names the breaking points where the current encoding fails, proposes concrete design directions, and allocates displaced information to named destinations.

---

## Governing Constraints (Non-Negotiable)

Before any design direction is evaluated, four constraints apply:

**C-1 — The step axis is shared and inviolable** (`CLAUDE.md §UX Architectural Commitments, Commitment 3`): All instruments showing temporal data share a single step axis. Zone 1A redesign cannot break this.

**C-2 — Zone 1A is situation-agnostic** (`CLAUDE.md §The Platform Principle`): Zone 1A cannot become entity-specific or scenario-specific in its design contract. Any proposed encoding must work for Bolivia, Zambia, Greece, and Jordan without structural modification.

**C-3 — Per-mode cognitive task governs encoding** (`north-star.md §Primary Cognitive Tasks by Mode`, `information-hierarchy.md §Governing Principle`): The encoding must serve the active mode's primary cognitive task first. Zone 1A in Mode 3 has a harder constraint (15 seconds) than Zone 1A in Mode 1 (30 seconds). The Mode 3 constraint is the binding design constraint.

**C-4 — DEMO-044 framing is rejected** (Issue #845, EL directive 2026-06-15): Curve endpoint labels as a fix for legibility is not the design direction. The design must address the encoding contract, not add labels to a broken encoding.

---

## Mode 1 — Trajectory Reconstruction

### Primary Cognitive Task (per `north-star.md`)

Trajectory reconstruction and historical pattern recognition. The user examines a completed programme to understand what happened, when thresholds were crossed, and whether the trajectory followed a recognizable pre-crisis pattern.

### Persona 2 Question (time ceiling: 30 seconds after Mode 1 entry)

> **"At which step did the first MDA threshold crossing occur — and which framework's trajectory crossed first?"**

This question is specific and bounded:
- The answer is a step number (e.g., "step 3") plus a framework name (e.g., "human development")
- It can be answered by reading two things from Zone 1A: which curve dips below its MDA floor line first, and at which step along the shared step axis
- It does not require opening a drawer, selecting a tab, or performing any interaction
- It is answerable within 30 seconds at the single-entity scale: four labeled curves, four horizontal MDA floor lines, and the step axis

**Journey reference:** Journey B Step 3 [Near-Term-Gap]: Persona 2 defends a challenged output. "At which step did the threshold cross?" is the exact question she is asked by a counterparty. Zone 1A must answer it directly.

### Information Zone 1A Needs in Mode 1 (single entity, N=1)

| Dimension | Required in Zone 1A | Why |
|---|---|---|
| Frameworks | All 4 | The primary question requires identifying *which* framework crossed — all 4 must be visible simultaneously to answer the question without interaction |
| Entities | 1 (entity selector governs) | The trajectory reconstruction question is per-entity; in single-entity Mode 1, this is satisfied |
| Branches | N/A (replay mode — no branches) | Historical fixture has one trajectory per framework |
| Step axis | Full horizon | The "at which step" portion of the question requires the full trajectory on the shared axis |

**Minimum dimensionality (single-entity Mode 1):** 4 lines (one per framework) + 4 MDA floor lines. This is the current encoding. It works.

### Mode 1 Multi-Entity (N > 1) — See §Combinatorial Tension

---

## Mode 2 — Simulation / Threshold-Safe Path

### Primary Cognitive Task (per `north-star.md`)

Threshold-safe path construction. The user is constructing a path — choosing policy parameters, advancing steps — and needs to know at each advance whether the path is still above all MDA floors, or whether it has projected a threshold crossing.

### Persona 2 Question (time ceiling: 30 seconds after each scenario advance)

> **"After this step advance, does any framework trajectory project a crossing below its MDA floor in the remaining steps — and if so, which framework and at which step?"**

This question is:
- Mode-specific: it requires trajectory data that updates at each step advance (not answerable from a static snapshot — at step N, the trajectory has changed)
- Specific: the answer is yes/no, plus framework name and step number if yes
- Bounded: the answer tells the user whether their current path is safe or not, and where the first failure is

**Journey reference:** Journey A Step 2 [Preparatory]: Persona 2 checks trajectory shape before the session. "Is the threshold-safe path still intact after this policy change?" is her question at each step.

### Information Zone 1A Needs in Mode 2 (single entity, N=1)

| Dimension | Required in Zone 1A | Why |
|---|---|---|
| Frameworks | All 4 | The question requires knowing *which* framework is projecting a crossing — all 4 must be visible to answer without interaction |
| Entities | 1 (entity selector governs) | Path construction is per-entity |
| Branches | 0 or 1 (baseline vs. comparison, via COMPARE_VIEW) | Single-path construction uses 1 trajectory; comparison uses COMPARE_VIEW which is separately specified |
| Step axis | Full projected horizon | The "in the remaining steps" portion requires the full future projection |

**Minimum dimensionality (single-entity Mode 2):** 4 lines (one per framework) + 4 MDA floor lines. This is the current encoding. It works for single-entity Mode 2.

**Mode 2 multi-entity:** When a scenario models multiple entities simultaneously, Zone 1A cannot show 4 × N lines and still answer the Mode 2 question within 30 seconds at N > 2. See §Combinatorial Tension for the breaking point and proposed allocation.

---

## Mode 3 — Active Control

### Primary Cognitive Task (per `north-star.md`)

Real-time steering within human cost constraints. The user applies a control input (e.g., a fiscal multiplier adjustment at step 3) and reads the trajectory response immediately. This is the hardest constraint across all modes.

### Persona 2 Question (time ceiling: 15 seconds after control input application)

> **"Did the applied control input move the programme trajectory away from or toward the nearest MDA threshold crossing — relative to the baseline path?"**

This question is:
- Relative: "relative to baseline" — the answer is a direction (toward / away) and a magnitude (how much the trajectory diverged)
- Bounded: yes/no on direction, plus a magnitude read (the divergence fill region between baseline and active curves makes this visual, not numeric)
- Mode-specific: it requires both the baseline trajectory (ghost curves) and the active trajectory (current curves) simultaneously on the same axis
- Time-hard: 15 seconds. The user is in a live negotiation. The IMF proposed a term. She applied it. She needs the answer before the discussion moves on.

### Compatibility Assessment: Is the Current Encoding Compatible with the 15-Second Ceiling?

**For single-entity Mode 3 (N=1):** Current encoding: 4 frameworks × 2 branches (baseline + active) = **8 lines**. With color differentiation between baseline (ghost, 50% opacity) and active (solid, 100%), and the divergence fill region between them, 8 lines is at the edge of legibility in 15 seconds. It is compatible, but only because the opacity encoding (ghost vs. solid) creates two visually distinct groups of 4 lines each — baseline is recognizable as a group, active as a group. The user reads the group separation, not individual line labels.

**For multi-entity Mode 3 (N=2):** 4 frameworks × 2 entities × 2 branches = **16 lines**. With 16 lines of similar colors and weights, no labeling scheme resolves "which framework of which entity crossed whose baseline?" in 15 seconds. The group-opacity encoding that works at N=1 breaks at N=2: 8 baseline lines and 8 active lines are each too dense to read individually.

**Verdict: The current 4-framework per-entity encoding is NOT compatible with the 15-second ceiling at N > 1 in Mode 3.**

### Maximum Dimensionality Zone 1A Can Carry in Mode 3

The 15-second question ("did this control input move the trajectory toward or away from a threshold crossing?") requires knowing:
- Direction of movement (toward / away)
- Approximate magnitude (the divergence between baseline and active paths)
- Whether any threshold floor was crossed

This question is answerable at the **composite level**, not the per-framework level. The user does not need to know "which framework is closest to its floor?" in 15 seconds — that is a Zone 1D question (current position readout, always visible). The Zone 1A question is the directional question: did the aggregate trajectory move in the right direction?

**Maximum dimensionality Zone 1A can carry in Mode 3 without exceeding the 15-second ceiling:**
- **1 composite trajectory line per entity** (framework-aggregated)
- **2 lines per entity** in Mode 3: baseline ghost (50% opacity, 1px, dashed) and active composite (100% opacity, 2px, solid)
- Entities distinguished by position and label (not by color channel)

At this dimensionality:
- N=1: 2 lines (baseline + active composite). 15 seconds: ✅
- N=2: 4 lines (2 per entity). 15 seconds: ✅ — entity labels at line endpoints distinguish them
- N=3: 6 lines. 15 seconds: ✅ borderline
- N=4: 8 lines. 15 seconds: ✅ borderline — approaching ceiling
- N>4: Zone 1A is not the primary instrument for >4-entity scenarios in Mode 3. A dedicated comparative surface is required. The Architecture Review Facilitator is flagged that Zone 1A in Mode 3 is designed for N≤4 entities.

### Where Excess Dimensions Are Allocated in Mode 3

| Dimension not in Zone 1A | Destination | Why that destination |
|---|---|---|
| Per-framework breakdown (which framework diverged) | Zone 1D (Four-Framework Current Position) | Zone 1D already shows all four current-step values simultaneously, no interaction required; it answers "which framework" at the current step |
| Per-framework baseline vs. active delta | Zone 1D annotation (delta value in parentheses per framework row) | Current step delta is sufficient; full trajectory per framework is Zone 2 (framework panels) |
| Entity-specific per-framework trajectory (Mode 3, multi-entity) | Zone 1D scoped to selected entity; entity switcher (persistent header) | The entity switcher already allows switching entity without leaving the instrument cluster; per-framework detail is per-entity |

---

## Combinatorial Tension

### The Encoding Under Pressure

The current Zone 1A encoding can express at most these dimensions simultaneously:

| Encoding channel | Dimension expressed |
|---|---|
| X-axis | Time (steps) |
| Y-axis | Composite score value |
| Line color (4 colors) | Framework (financial, HD, ecological, governance) |
| Line opacity (100% vs 50%) | Branch (active vs. baseline, in Mode 3) |
| Line style (solid vs. dashed) | Branch qualifier (active vs. baseline) |

There is no remaining encoding channel for **entity identity**. Entity identity has no visual channel in Zone 1A beyond position (which line is at which Y-value at which step). With multiple entities, position overlaps when trajectories are close in value.

### Specific Breaking Points

**Breaking point 1: Mode 3, N=2 entities, M=1 branch**
4 frameworks × 2 entities × 2 branches (baseline + active) = **16 lines**.
There is no labeling scheme that makes 16 lines on a shared axis legible in 15 seconds. The color channel is exhausted by 4 frameworks. Opacity is exhausted by 2 branches. Line style (solid/dashed) is exhausted by branch identity. Entity identity has no remaining channel.

**Breaking point 2: Mode 1 or Mode 2, N=3 entities, M=1 branch**
4 frameworks × 3 entities × 1 branch = **12 lines**.
The 30-second ceiling for Mode 1 trajectory reconstruction ("which framework crossed first?") cannot be met when 12 lines of overlapping color must be disambiguated. The per-framework question requires reading individual lines, not groups. At 12 lines, individual line reading within 30 seconds is not reliably achievable.

**Breaking point 3: Mode 2 comparison, N=2 entities, M=2 paths**
4 frameworks × 2 entities × 2 paths = **16 lines** in COMPARE_VIEW.
The Zone 1A COMPARE_VIEW delta alert panel spec (information-hierarchy.md §Mode 1 COMPARE_VIEW) was specified for two historical fixtures, each single-entity. Multi-entity COMPARE_VIEW is unspecified. This is a Phase 2 question — G6c identifies it as a gap, not a resolved allocation.

---

## Information Allocation

### Allocation Table

For each dimension that Zone 1A cannot carry at the specified breaking points, the following allocations are proposed. All allocations must be consistent with the receiving zone's cognitive task as defined in `docs/ux/information-hierarchy.md`.

| Displaced dimension | Context | Proposed destination | Zone cognitive task (must not conflict) | Non-conflict rationale |
|---|---|---|---|---|
| **Entity trajectory comparison (N>1, per-framework)** | Mode 1, Mode 2: N>2 entities loaded simultaneously | Zone 1A shows 1 composite line per entity (framework-aggregated). Per-framework detail: Zone 1D (current step) and Zone 2B (FrameworkPanels, full history) | Zone 1D: four composite score values at current step. Zone 2B: indicator detail, confidence tiers, cohort breakdowns. | Zone 1D's requirement — "all four values visible simultaneously" — is served by per-framework current values for the selected entity. Adding a delta annotation for multi-entity context extends, not conflicts, Zone 1D. Zone 2B (FrameworkPanels) already carries per-framework indicator detail — adding trajectory history for a second entity is a Zone 2 expansion, not a Zone 1 displacement. |
| **Entity trajectory comparison (N>1, Mode 3 live A/B)** | Mode 3: N>1 entities, baseline + active | Zone 1A shows 2 composite lines per entity (baseline ghost + active solid, composite). Per-framework divergence: Zone 1D delta annotation per framework row. | Zone 1D: four composite score values. | Composite trajectory per entity on Zone 1A answers the Mode 3 directional question ("did this input help?") per entity. Per-framework delta in Zone 1D answers "which framework diverged?" at the current step without requiring interaction. |
| **Branch comparison (M>1, Mode 3 multiple what-ifs)** | Mode 3: M=2+ simultaneous what-if branches | Zone 1A carries only M=1 (baseline vs. current active). Additional what-if branches enter COMPARE_VIEW, which is separately specified for Mode 3 temporal divergence. | Zone 1A in Mode 3: baseline + active (M=1 pattern). COMPARE_VIEW Mode 3: two trajectories on shared axis (existing spec). | Mode 3 COMPARE_VIEW is already specified as "baseline vs. active trajectory on a shared step axis — always temporal, never choropleth" (`information-hierarchy.md §Mode 3 COMPARE_VIEW`). M>1 what-if branches are served by entering COMPARE_VIEW with a different active scenario, not by encoding M branches simultaneously on Zone 1A. |
| **Multi-entity COMPARE_VIEW (Mode 1 and 2 with N>1)** | Mode 1 or 2 COMPARE_VIEW: comparing multi-entity historical fixtures | Unresolved — flagged for Phase 2. Current COMPARE_VIEW spec (information-hierarchy.md) is single-entity per fixture. Multi-entity COMPARE_VIEW is a Phase 2 Architecture Review question. | Phase 2 question. | This gap is identified, not resolved, in Phase 1. The Architecture Review panel must address multi-entity COMPARE_VIEW as a specific question — it is not answerable from Phase 1 first-principles reasoning alone. |

### What Zone 1A Owns (After These Allocations)

Zone 1A owns the **trajectory shape question** at the appropriate resolution for the active mode:

- **Mode 1 (single entity):** 4 framework lines. Trajectory shape at full framework resolution. The "which framework crossed first?" question is answerable directly.
- **Mode 1 (N>1 entities, not COMPARE_VIEW):** 1 composite line per entity (framework-aggregated). The "which entity crossed first?" question is answerable. "Which framework within entity X?" requires Zone 1D current position + entity selector switch.
- **Mode 2 (single entity):** 4 framework lines. Same as Mode 1 single entity.
- **Mode 2 (N>1 entities, not COMPARE_VIEW):** 1 composite line per entity. Same allocation as Mode 1 multi-entity.
- **Mode 3 (any entity count ≤4):** 1 composite line per entity × 2 (baseline ghost + active solid). The "did this control input help or hurt?" question is answerable per entity.

Zone 1A does NOT own:
- The "which framework within entity X diverged?" question in multi-entity context (→ Zone 1D)
- The "how does entity X compare to entity Y at the indicator level?" question (→ Zone 2B / entity selector switch)
- The "what is the full per-framework trajectory for entity Y?" question in Mode 3 multi-entity (→ Zone 1D + entity switch → Zone 2B after Zone 1 read)

---

## Concrete Design Directions

### Mode 1 — Trajectory Reconstruction

**Single-entity (N=1):** No change from current encoding. 4 framework lines, 4 MDA floor lines, shared step axis. Step annotations for SIGNIFICANT steps (calendar date + event label). The "which framework crossed first?" question is directly answerable.

**Multi-entity (N>1, not COMPARE_VIEW):**
Zone 1A displays 1 composite line per entity (overall composite score, not per-framework), with MDA floor lines derived from the lowest-threshold framework (the binding constraint). Entity labels at curve endpoints (abbreviated entity code: JOR, EGY, GRC, ZMB) distinguish lines by position.

*Named scenario:* JOR (Jordan) + EGY (Egypt) + ZMB (Zambia), Mode 1, 3 entities, 1 branch.
Zone 1A shows 3 composite trajectory lines, one per entity, labeled "JOR", "EGY", "ZMB" at their step-8 endpoints. MDA floor line shown as a single dashed horizontal (the most restrictive threshold across all four frameworks for each entity — per-entity floor). The user reads: "ZMB composite crossed the floor at step 2, JOR at step 4, EGY has not crossed." This is the "which entity crossed first?" answer within 30 seconds.
Per-framework detail for any entity: entity selector switch → Zone 1D shows 4 framework current values for the selected entity.

**Kryptonite check (Mode 1 multi-entity):** The composite composite trajectory per entity is interpretable by Persona 2 without specialist mediation. "ZMB: composite score crosses floor at step 2" is a self-describing finding. No translation required. Zone 1D provides the "which framework?" follow-up within the same 30-second window after entity selection.

### Mode 2 — Simulation / Threshold-Safe Path

**Single-entity (N=1):** No change from current encoding. 4 framework lines, 4 MDA floor lines, shared step axis. The "does any framework project a crossing in remaining steps?" question is answered by reading whether any curve dips below its floor line in the projected future.

**Multi-entity (N>1, not COMPARE_VIEW):**
Same allocation as Mode 1 multi-entity: 1 composite line per entity. In Mode 2, the composite line is a projected trajectory (not a historical replay). MDA floor lines apply per entity.

*Named scenario:* JOR + EGY, Mode 2, 2 entities, scenario advanced to step 4.
Zone 1A shows 2 projected composite lines, labeled "JOR" and "EGY". The step axis shows steps 0–8 with current step marker at step 4. JOR composite is projected to cross the MDA floor at step 7. EGY composite is projected to remain above the floor. The user reads: "JOR is the entity at risk; EGY is safe on the current path." Per-framework drill-down: entity selector → JOR → Zone 1D shows which of JOR's four frameworks is pulling the composite down.

**Kryptonite check (Mode 2 multi-entity):** "JOR composite is heading below the MDA floor at step 7" is self-describing. Per-framework follow-up is one entity selector action (persistent header, no navigation) + Zone 1D read. Ministry economist does not require specialist mediation for either read.

### Mode 3 — Active Control

**Single-entity (N=1):**
Current encoding works with modification: 4 framework baseline ghost curves (50% opacity, 1px, dashed) + 4 framework active curves (100% opacity, 2px, solid) + divergence fill region. The "did this input move the trajectory toward or away from the floor?" question is answerable from the divergence fill region in 15 seconds.

However: the 4 per-framework encoding in Mode 3 single-entity creates 8 lines, which is at the legibility ceiling. The Architecture Review (Phase 2) should evaluate whether Mode 3 single-entity should also adopt the composite-per-entity encoding (reducing to 2 lines: 1 baseline ghost + 1 active composite) for consistency with multi-entity Mode 3. This is flagged as a Phase 2 decision, not resolved in Phase 1.

**Multi-entity (N=2, Mode 3 live A/B):**
Zone 1A displays 2 composite lines per entity: baseline ghost (50% opacity, 1px, dashed, composite) + active solid (100% opacity, 2px, solid, composite). Entities distinguished by endpoint label (JOR, EGY) and vertical position. Divergence fill region between baseline and active for each entity.

*Named scenario:* JOR + EGY, Mode 3, 2 entities, fiscal_multiplier=1.30 applied at step 3 (JOR only).
Zone 1A shows 4 lines: JOR-baseline (ghost, composite), JOR-active (solid, composite), EGY-baseline (ghost, composite), EGY-active (solid, composite). After the JOR multiplier is applied: JOR-active line diverges upward from JOR-baseline starting at step 3 (improvement). EGY lines run parallel (EGY is unaffected by the JOR control input). The user reads: "The JOR input moved the JOR trajectory away from the floor; EGY is unchanged." Answer time: within 15 seconds.
Per-framework breakdown of JOR improvement: Zone 1D shows JOR's 4 framework values with per-row delta annotation ("Financial: 0.71 (+0.04 vs baseline)"). No interaction required — Zone 1D is always visible.

**Multi-entity (N=3, Mode 3):**
Zone 1A shows 6 lines: 2 per entity (baseline + active composite). 6 lines on a shared axis with endpoint labels. This is at the limit of 15-second legibility. The Architecture Review panel should specify the maximum N for Mode 3 Zone 1A use — Phase 1 proposes N≤4, with a flag shown to the user when N>4 that Zone 1A is operating at its legibility limit.

*Named scenario N>4:* If a scenario contains 5 or more entities, Zone 1A displays a legibility-limit notice: "Zone 1A shows individual entity trajectories for up to 4 entities. This scenario contains [N] entities. Use the entity selector to view individual trajectories." The composite view for each selected entity is still Zone 1A; the simultaneous display of all N entities is not attempted at N>4.

**Kryptonite check (Mode 3 multi-entity):** "JOR composite trajectory moved away from the floor after the fiscal multiplier was applied" is self-describing. Entity label at line endpoint ("JOR") removes ambiguity. Zone 1D per-framework delta annotation ("Financial: +0.04 vs baseline") removes specialist mediation for the follow-up framework question. No translation required. A Zambian finance ministry economist can read this in 15 seconds without a specialist present.

---

## Phase 2 Readiness

The Architecture Review Facilitator uses these three questions to gate Phase 2. Each question is answered below with a pointer to the document section where the full treatment is found.

**Question 1: What is Zone 1A's primary question in each mode?**

| Mode | Zone 1A Primary Question | Section |
|---|---|---|
| Mode 1 | "At which step did the first MDA threshold crossing occur — and which framework's trajectory crossed first?" (or: "which entity crossed first?" in multi-entity) | §Mode 1 — Trajectory Reconstruction |
| Mode 2 | "After this step advance, does any framework trajectory project a crossing below its MDA floor in the remaining steps?" (or: "which entity is at risk?" in multi-entity) | §Mode 2 — Simulation / Threshold-Safe Path |
| Mode 3 | "Did the applied control input move the programme trajectory away from or toward the nearest MDA threshold crossing — relative to the baseline path?" | §Mode 3 — Active Control |

**Question 2: Which encoding channels does the proposed design use to answer the primary question?**

| Mode | Encoding | Section |
|---|---|---|
| Mode 1 single-entity | 4 framework lines (color channel), 4 MDA floor lines, shared step axis | §Mode 1 — Concrete Design Direction |
| Mode 1 multi-entity | 1 composite line per entity (position + endpoint label for entity identity), single MDA floor per entity | §Mode 1 — Concrete Design Direction |
| Mode 2 single-entity | Same as Mode 1 single-entity | §Mode 2 — Concrete Design Direction |
| Mode 2 multi-entity | Same as Mode 1 multi-entity | §Mode 2 — Concrete Design Direction |
| Mode 3 single-entity | 4 framework lines × 2 branches (opacity for branch, color for framework) — or composite × 2 (Phase 2 decision) | §Mode 3 — Concrete Design Direction |
| Mode 3 multi-entity | 1 composite line per entity × 2 branches (opacity for branch, endpoint label for entity) | §Mode 3 — Concrete Design Direction |

**Question 3: What are the design's constraints on M (branches) and N (entities) before legibility breaks?**

| Mode | N limit | M limit | Breaking point | Section |
|---|---|---|---|---|
| Mode 1 (4-framework encoding) | N=1 (single-entity) | M=1 | N=2: 8 lines begin to strain 30-second read | §Combinatorial Tension |
| Mode 1 (composite encoding) | N≤4 (30-second ceiling) | M=1 | N=5 approaches endpoint label collision | §Concrete Design Directions |
| Mode 2 (4-framework encoding) | N=1 | M=1 | N=2: same as Mode 1 | §Combinatorial Tension |
| Mode 2 (composite encoding) | N≤4 | M=1 | Same as Mode 1 composite | §Concrete Design Directions |
| Mode 3 (composite per-entity) | N≤4 | M=1 (baseline + active auto) | N=5: 10 lines; 15-second ceiling exceeded | §Mode 3 — Concrete Design Direction |
| Mode 3 (composite per-entity, COMPARE_VIEW) | N=1–2 per COMPARE_VIEW fixture | M=2 (baseline + one what-if) | M=3: 3 trajectory groups × labels; Phase 2 question | §Information Allocation |

**Open questions for Phase 2 panel (not resolved in Phase 1):**

1. **Mode 3 single-entity encoding choice:** Should Mode 3 single-entity also use composite encoding (2 lines: baseline ghost + active solid) for consistency with Mode 3 multi-entity — or should it retain the 4-framework per-branch encoding (8 lines) on grounds that the per-framework direction question ("which framework improved?") is valuable within the 15-second ceiling? This is a Phase 2 Architecture Review decision requiring a panel evaluation of the cognitive task at the 15-second ceiling.

2. **Multi-entity COMPARE_VIEW (Mode 1 and Mode 2):** The current COMPARE_VIEW spec is single-entity-per-fixture. Multi-entity COMPARE_VIEW has no specified Zone 1A encoding. The Phase 2 panel must address this gap before the ADR (Phase 3) can make the binding decision.

3. **Composite score definition for Zone 1A multi-entity:** When Zone 1A shows a composite per entity (framework-aggregated), which aggregation rule applies? Simple average of 4 framework scores? Minimum (the floor-constrained reading)? Weighted by the current scenario's analytical focus? This is a Data Architect + Chief Methodologist question for Phase 2 — it has policy implications (minimum composite penalizes frameworks with lower absolute scores; simple average may obscure a framework near its MDA floor).

4. **Endpoint label collision at N=4:** At N=4 entities with close composite scores at the final step, endpoint labels may overlap. Phase 2 must specify the collision handling rule (label offset, slight y-position nudge, or hover-to-label). This is an implementation detail but needs a specified rule before Phase 3 ADR acceptance.

---

*Phase 1 complete — 2026-06-18. Intent document: `docs/process/intents/M14-G6c-2026-06-18-zone-1a-design-thinking.md`. This document must exist in `release/m14` before the M14 exit ceremony. Architecture Review Facilitator confirms Phase 2 readiness at M15 kickoff by verifying AC-1 through AC-8 of the intent document against this file.*
