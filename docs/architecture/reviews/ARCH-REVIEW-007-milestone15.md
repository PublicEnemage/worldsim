# ARCH-REVIEW-007: Zone 1A Information Architecture — Phase 2 Architecture Review

**Review type:** Full — Phase 2 Architecture Review for Zone 1A multi-dimensional encoding (#845)
**Scope:** Phase 2 readiness gate questions (Q1, Q2, Q3); binding decisions on four Phase 1 open
questions from `docs/ux/design-thinking/zone-1a-information-architecture.md §Phase 2 Readiness`
**Facilitated by:** Architecture Review Facilitator
**Date:** 2026-06-22
**Status:** Complete — all three readiness questions addressed; all four open questions resolved;
ADR-017 authorship unblocked per sprint entry §4 sequencing note step 6
**Input document:** `docs/ux/design-thinking/zone-1a-information-architecture.md` (M14 G6c, PR #1033, BPO ACCEPT 2026-06-18)
**Sprint entry:** `docs/process/sprint-plans/m15-g2-sprint-entry.md` (EL Approved 2026-06-21)
**Intent document:** `docs/process/intents/M15-G2-2026-06-21-zone-1a-adr.md`

**Panel:**

| Agent | Role | Scope |
|---|---|---|
| Architecture Review Facilitator | R — facilitates, records decisions | All questions |
| Architect Agent | R — authors decisions | All questions; ADR-017 author |
| UX Designer Agent | C — encoding channel validity, UX constraints | Q2, Q3, open questions (a) and (d) |
| Frontend Architect Agent | C — implementation feasibility | Q3, open question (d) endpoint collision |
| Chief Methodologist | C — composite aggregation rule | Open question (c) |
| Business PO | C — mission-critical use case confirmation | P-7 north star scenario |
| Customer Agent | C — Layer 3 interpretability | Open question (a), kryptonite check |
| Engineering Lead | A — decision authority | All decisions |

---

## Purpose

This Architecture Review completes Phase 2 of the Zone 1A information architecture work
(Issue #845, Phase 2 of four phases). It addresses three Phase 2 readiness questions and
makes binding decisions on four open questions identified in the Phase 1 design thinking
document (`docs/ux/design-thinking/zone-1a-information-architecture.md §Phase 2 Readiness`).

The four open questions must be resolved before ADR-017 can be authored. This review is the
evidence base for ADR-017. Phase 1 established the primary question per mode, the dimensional
analysis, and the concrete design directions. Phase 2 resolves the four design questions that
Phase 1 explicitly deferred to the Architecture Review panel.

---

## Phase 2 Readiness Gate — Three Questions

The Architecture Review Facilitator confirms that all three Phase 2 readiness questions are
answered in the input document. Each answer is reproduced here and confirmed as the ADR-017
evidence base.

### Q1: What is Zone 1A's Primary Question Per Mode?

*Reproduced from `zone-1a-information-architecture.md §Phase 2 Readiness Q1` — confirmed
binding for ADR-017:*

| Mode | Zone 1A Primary Question | Time Ceiling |
|---|---|---|
| Mode 1 (Replay) | "At which step did the first MDA threshold crossing occur — and which framework's trajectory crossed first?" (single-entity); or "which entity crossed first?" (multi-entity) | 30 seconds |
| Mode 2 (Simulation) | "After this step advance, does any framework trajectory project a crossing below its MDA floor in the remaining steps?" (single-entity); or "which entity is at risk on the current path?" (multi-entity) | 30 seconds |
| Mode 3 (Active Control) | "Did the applied control input move the programme trajectory away from or toward the nearest MDA threshold crossing — relative to the baseline path?" | 15 seconds — **binding constraint** |

**Panel confirmation:** All three questions are specific, bounded, and answerable from Zone 1A
alone (with Zone 1D supplementing for the per-framework follow-up in multi-entity context).
The Mode 3 question at 15 seconds is the binding design constraint — the encoding for ALL modes
must be compatible with the encoding chosen to satisfy the Mode 3 ceiling.

### Q2: Which Encoding Channels Does the Proposed Design Use?

*Reproduced and confirmed from `zone-1a-information-architecture.md §Phase 2 Readiness Q2`:*

| Mode / Context | Encoding channels | Dimension expressed |
|---|---|---|
| Mode 1/2 single-entity | X-axis (time/steps); Y-axis (composite score); color (4 framework lines); horizontal dashed line (MDA floor per framework) | Framework identity, trajectory shape, threshold floor |
| Mode 1/2 multi-entity (N>1) | X-axis (steps); Y-axis (composite score); line position (entity trajectory); endpoint label (entity code at final step) | Entity identity, composite trajectory, threshold floor |
| Mode 3 N=1 | X-axis (steps); Y-axis (composite score); opacity (100% active, 50% ghost/baseline); divergence fill (5–10%); endpoint label | Branch identity (active vs. baseline), direction-of-effect |
| Mode 3 N>1 | X-axis (steps); Y-axis (composite score); opacity (100% active, 50% ghost/baseline); endpoint label (entity code) | Entity identity, branch identity, direction-of-effect per entity |

**Panel confirmation (UX Designer):** The encoding channels are correctly scoped per mode.
The color channel in single-entity mode (4 framework colors) and the opacity channel in Mode 3
(active vs. baseline ghost) are the two load-bearing encoding decisions. All other channels
(line style, endpoint label) are secondary disambiguation aids. This is consistent with
`information-hierarchy.md §Zone 1 — 1A` requirements.

### Q3: What Are the N/M Limits Before Legibility Breaks?

*Reproduced and confirmed from `zone-1a-information-architecture.md §Phase 2 Readiness Q3`:*

| Mode | N limit (entities) | M limit (branches) | Breaking point | Consequence at breaking point |
|---|---|---|---|---|
| Mode 1/2 single-entity (4-framework) | N=1 | M=1 | N=2: 8 lines stresses 30-second read | Switch to composite per-entity encoding |
| Mode 1/2 multi-entity (composite) | N≤4 | M=1 | N=5: endpoint label collision becomes unmanageable | Legibility-limit notice; entity selector required |
| Mode 3 (composite per-entity) | N≤4 | M=1 (baseline + active auto) | N=5: 10 lines exceed 15-second ceiling | Legibility-limit notice; entity selector required |
| Mode 3 COMPARE_VIEW | N=1–2 per fixture | M=2 (via COMPARE_VIEW) | M>2: out of scope for Phase 4 | COMPARE_VIEW with M>2 branches deferred |

**Panel confirmation (Frontend Architect):** The N≤4 limit is implementable with the existing
Recharts-based trajectory chart. The legibility-limit notice at N>4 is a conditional render —
straightforward to implement. The breaking point at N=5 is confirmed: 10 lines on a shared step
axis with 15-second read time exceeds what any labeling scheme can make legible.

---

## Four Phase 1 Open Questions — Binding Decisions

### Open Question (a): Mode 3 Single-Entity Encoding Choice

**Question from Phase 1 (§Phase 2 Readiness open question 1):**
Should Mode 3 single-entity adopt the composite encoding (2 lines: baseline ghost + active solid)
for consistency with Mode 3 multi-entity — or retain the 4-framework per-branch encoding (8 lines)
on grounds that the per-framework direction question is valuable within the 15-second ceiling?

**Panel deliberation:**

*Architect Agent:* The 4-framework 8-line encoding in Mode 3 single-entity is at the legibility
ceiling. It works today only because the opacity channel (ghost vs. solid) creates two visually
distinct groups of 4 lines each. Adding a second entity under the 4-framework encoding produces 16
lines — guaranteed legibility failure. There is a consistency benefit: if single-entity and
multi-entity Mode 3 use the same composite encoding, the user's mental model of Zone 1A in Mode 3
is uniform regardless of how many entities are loaded.

*UX Designer:* The Mode 3 primary question is directional: "did this help or hurt?" This is a
composite-level question. Zone 1D (always visible in the instrument cluster) answers "which
framework contributed to the directional change?" at the current step without any interaction.
The 4-framework encoding in Mode 3 gives the user more information than the primary question
requires, at the cost of legibility.

*Customer Agent (Layer 3 assessment):* For Persona 2 (Eleni/Aicha — Finance Ministry Negotiator)
in a live Mode 3 session, the 2-line composite encoding is more interpretable under cognitive load.
"The composite trajectory moved away from the floor after the fiscal multiplier was applied" is the
Layer 3 output. Zone 1D delta annotations ("Financial: +0.04 vs baseline") provide the follow-up
without requiring additional interaction. The 4-framework encoding introduces a mediation step
("the user must group the 8 lines visually") that the composite encoding eliminates.

**Decision:** Mode 3 single-entity adopts the composite encoding (2 lines: baseline ghost
composite + active solid composite). This is a consistent encoding across all Mode 3 contexts
(N=1 through N=4). The 4-framework per-branch encoding (8 lines) is deprecated for Mode 3.
Per-framework breakdown in Mode 3 is served by Zone 1D delta annotations (always visible,
zero interaction). ADR-017 records this as a binding encoding contract for Phase 4 implementation.

### Open Question (b): Multi-Entity COMPARE_VIEW (Mode 1 and Mode 2)

**Question from Phase 1 (§Phase 2 Readiness open question 2):**
The current COMPARE_VIEW spec (`information-hierarchy.md §COMPARE_VIEW`) is single-entity-per-fixture.
Multi-entity COMPARE_VIEW (Mode 1 and Mode 2 with N>1 entity per fixture) has no specified Zone 1A
encoding. The Phase 2 panel must address this gap.

**Panel deliberation:**

*Architect Agent:* Multi-entity COMPARE_VIEW requires comparing two fixtures (or two paths) where
each fixture contains N entities. At N=2 entities per fixture and 2 fixtures: 4 composite lines
on Zone 1A. The encoding channels already in use (opacity for fixture identity, endpoint label for
entity identity) can extend to this case. However, the cross-product of entity × fixture identity
requires two disambiguation channels simultaneously — one for entity (color) and one for fixture
(opacity/line style). At N=2 entities, this is manageable. At N>2 per fixture, it is not.

*UX Designer:* Mode 1 COMPARE_VIEW already uses opacity (solid = Fixture A, ghost = Fixture B).
For multi-entity Mode 1 COMPARE_VIEW with N=2 per fixture: Zone 1A shows 4 composite lines —
Fixture A entities (solid, color by entity), Fixture B entities (ghost, color by entity). Endpoint
labels include entity code and fixture indicator (e.g., "JOR-A", "JOR-B"). This preserves the
existing COMPARE_VIEW visual contract while extending it to composite per entity.

*Frontend Architect:* At N=2 per fixture (4 lines total), the existing Recharts implementation
can support this with endpoint label additions. At N>2 per fixture (>4 lines in COMPARE_VIEW),
the encoding fails legibility within the 30-second Mode 1 ceiling.

**Decisions:**

1. **Mode 1 COMPARE_VIEW multi-entity:** Zone 1A supports N≤2 entities per fixture in Mode 1
   COMPARE_VIEW. Encoding: 1 composite line per entity per fixture (Fixture A = solid 100%,
   Fixture B = ghost 50% dashed). Entity identity: color channel (from entity palette, max 2
   colors = 2 entities). Endpoint labels: `{ENTITY}-A` and `{ENTITY}-B` (e.g., "JOR-A", "JOR-B").
   At N>2 entities per fixture: Zone 1A shows only the lowest-composite entity per fixture with a
   notice: "Showing 1 of N entities per fixture. Use entity selector for per-entity comparison."

2. **Mode 2 COMPARE_VIEW multi-entity:** Already specified in `information-hierarchy.md §COMPARE_VIEW
   Mode 2 — Multi-entity scenarios` as DeltaChoropleth. This is confirmed binding. Zone 1A in
   multi-entity Mode 2 COMPARE_VIEW defers to the DeltaChoropleth for the primary question; Zone 1A
   in this context shows the entity-selector-scoped single-entity comparison trajectory when an
   entity is selected via the entity selector.

3. **Both modes:** Multi-entity COMPARE_VIEW is a Phase 4 implementation scope item. The
   single-entity COMPARE_VIEW (Mode 1) and DeltaChoropleth (Mode 2 multi-entity) are already
   implemented; the multi-entity Mode 1 COMPARE_VIEW extension specified here is a Phase 4 addition.

### Open Question (c): Composite Score Aggregation Rule for Zone 1A Multi-Entity

**Question from Phase 1 (§Phase 2 Readiness open question 3):**
When Zone 1A shows a composite line per entity (framework-aggregated) in multi-entity context,
which aggregation rule applies — simple average of 4 framework scores, minimum (floor-constrained),
or weighted by scenario analytical focus?

**Chief Methodologist consultation:**

The composite score used for Zone 1A multi-entity must be:
1. **Consistent** with the composite score shown in Zone 1D (the four-framework current position
   panel) — if they differ, the user will encounter contradictory readings between Zone 1A and 1D.
2. **Scale-invariant** — not penalizing frameworks whose absolute scores are structurally lower
   due to their normalization domain (e.g., ecological governance indices have different absolute
   ranges than financial ratios).
3. **Risk-sensitive** — ideally reflecting the framework most at risk, not just the average
   distance from floors.
4. **Already computed** by the simulation engine — introducing a new aggregation formula specific
   to Zone 1A creates a parallel computation not validated against the historical calibration base.

The simulation engine already outputs a `composite_score` per entity per step in the trajectory
response. This is the existing aggregate used in Zone 1D and in the radar chart. It has been
validated against historical calibration cases. Introducing a Zone-1A-specific composite (minimum,
normalized, or weighted) would create a semantic gap: Zone 1A says the composite is 0.4, Zone 1D
reads the four frameworks at values whose average is 0.55.

**Decision:** Zone 1A multi-entity composite lines use the **existing simulation engine
`composite_score` output** — the same value displayed in Zone 1D. No new aggregation formula
is introduced. This is not an avoidance of the question — it is the correct answer: the
`composite_score` is already the canonical aggregate, and Zone 1A reusing it ensures consistency
between the trajectory view (Zone 1A) and the current-position readout (Zone 1D). The Chief
Methodologist's constraint: the composite_score displayed in Zone 1A must be accompanied by
a confidence tier annotation (the Tier badge from the lowest-tier framework, as the binding
confidence constraint) to prevent false precision in the composite aggregate.

### Open Question (d): Endpoint Label Collision at N=4

**Question from Phase 1 (§Phase 2 Readiness open question 4):**
At N=4 entities with close composite scores at the final step, endpoint labels ("JOR", "EGY",
"GRC", "ZMB") may overlap. The collision handling rule must be specified before Phase 3 ADR
acceptance.

**Panel deliberation (Frontend Architect + UX Designer):**

The endpoint label collision problem arises when two or more entity composite trajectories
converge to similar Y-values at the final step. A static label offset (all labels at the same
x-position, step 8) will produce overlap when trajectories are within 16–20px of each other.

Options evaluated:
- **Hover-to-reveal:** Rejected. Mode 3 15-second ceiling cannot accommodate a hover interaction
  to read entity identity.
- **Staggered x-position (labels at step 7, step 8, or step 8+):** Partially viable but
  introduces the question of which label is "at" which data point.
- **Dynamic y-offset at render time:** Viable. Sort labels by final-step Y-value; if any two
  labels are within `labelHeight` (≈18px), offset the lower label downward by 20px. Apply
  iteratively. No interaction required.
- **Numbered legend:** Fallback. If the dynamic offset produces a visually cluttered result,
  a numbered legend (1=JOR, 2=EGY, etc.) below the chart removes labels from the chart surface
  entirely. This is a mode-last-resort, not the primary handling.

**Decision:** **Dynamic y-offset algorithm.** At render time: (1) collect all endpoint label
positions (Y-value in pixels at the final step); (2) sort labels by Y-value ascending; (3) for
any two adjacent labels within 18px vertically, offset the lower label downward by 20px; (4)
apply iteratively until all labels are ≥18px apart or 3 iterations are exhausted; (5) after 3
iterations, render at computed positions — minor overlaps at N=4 are acceptable as less disruptive
than a legend switch. For N>4: the legibility-limit notice replaces all entity labels (label
collision is moot because Zone 1A is in notice mode). ADR-017 records this as the Phase 4
frontend implementation spec.

---

## Summary — Zone 1A Encoding Contract (ADR-017 Input)

This summary provides the binding encoding contract that ADR-017 must record. All four
decisions above are incorporated.

**Zone 1A encoding table (post-Phase 2 decisions):**

| Context | Lines in Zone 1A | Encoding channels | Legibility ceiling |
|---|---|---|---|
| Mode 1/2, N=1 | 4 framework + 4 MDA floor | color=framework, Y=score, X=step | 30 sec ✅ |
| Mode 1/2, 1<N≤4 | 1 composite per entity + 1 MDA floor per entity | Y=score, X=step, endpoint label=entity code | 30 sec ✅ |
| Mode 1/2, N>4 | Legibility-limit notice | — | — |
| Mode 3, N≤4 | 2 per entity (baseline ghost + active solid) | opacity=branch, Y=score, X=step, endpoint label=entity code | 15 sec ✅ |
| Mode 3, N>4 | Legibility-limit notice | — | — |
| Mode 1 COMPARE_VIEW, N≤2/fixture | 2 per entity (Fixture A solid + Fixture B ghost) | opacity=fixture, color=entity, endpoint label=ENTITY-A/B | 30 sec ✅ |
| Mode 1 COMPARE_VIEW, N>2/fixture | Single lowest-composite entity per fixture + notice | — | — |
| Mode 2 multi-entity COMPARE_VIEW | DeltaChoropleth (existing spec) | — | — |

**Composite aggregation (Q3 decision):** Use existing simulation engine `composite_score` field —
no new formula introduced. Same value as Zone 1D.

**Endpoint collision handling (Q4 decision):** Dynamic y-offset algorithm at render time;
N>4 handled by legibility-limit notice.

---

## ADR-017 Authorship Unblocked

All Phase 2 readiness gates are satisfied:

- [x] Q1 answered: primary question per mode confirmed for Modes 1, 2, 3
- [x] Q2 answered: encoding channels specified per mode context
- [x] Q3 answered: N and M numeric limits stated per mode; breaking points identified
- [x] Open question (a) resolved: Mode 3 single-entity adopts composite encoding (2 lines)
- [x] Open question (b) resolved: Mode 1 COMPARE_VIEW supports N≤2/fixture; Mode 2 uses
  DeltaChoropleth (existing spec); multi-entity Mode 1 COMPARE_VIEW extension is Phase 4 scope
- [x] Open question (c) resolved: Zone 1A composite = existing `composite_score` engine output
- [x] Open question (d) resolved: dynamic y-offset algorithm; N>4 → legibility-limit notice

**Architect Agent may now proceed to ADR-017 authorship per sprint entry §4 sequencing note step 7.**

The Architect Agent must:
1. Use `docs/adr/template.md` as starting point
2. Reference this ARCH-REVIEW-007 as the primary evidence source alongside the Phase 1 design
   thinking document
3. Obtain UX Designer independent sign-off (NM-042 compliant — four named fields, declared
   Session context)
4. Include Chief Methodologist consultation record (open question (c) decision)
5. Submit ADR-017 for EL acceptance before sprint exit

*ARCH-REVIEW-007 complete — 2026-06-22. Facilitated by Architecture Review Facilitator.*
