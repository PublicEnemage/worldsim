# ADR-008 Panel Review

> **Artifact type:** ADR Panel Review
> **ADR:** ADR-008 — UX Architecture: Instrument Cluster, Viewport, and Interaction Model
> **ADR file:** `docs/adr/ADR-008-ux-architecture.md`
> **Status:** Disposition recommendations pending EL decision
> **Review date:** 2026-05-22
> **Convention:** `docs/adr/reviews/ADR-NNN-panel-review.md` — first instance of this artifact type

---

## Panel

| Reviewer | Role | Status |
|---|---|---|
| UX Designer Agent | C — UX frame and component decisions | Conditional sign-off ✓ |
| Frontend Architect Agent | C — implementing agent (required per panel composition rule) | Conditional sign-off ✓ |
| Chief Methodologist | C — confidence tier visual system and epistemic obligations | Conditional sign-off ✓ |
| Engineering Lead | A — accountable on all ADR decisions | Pending |

---

## Findings Register

| ID | Source | Type | Severity | ADR change required? | Status |
|---|---|---|---|---|---|
| UX-F1 | UX Designer | Zone 1 co-primary spatial arrangement unspecified | Non-blocking | Add Open Risks note only | Pending EL |
| UX-F2 | UX Designer | "COMPARE\_VIEW Zone 1C" label is ambiguous | Non-blocking | Yes — editorial | Pending EL |
| UX-F3 | UX Designer | Alert tap expansion rendering mechanism under-specified | Non-blocking | Yes — one-sentence boundary | Pending EL |
| UX-F4 | UX Designer | Blue/orange color accessibility — shape distinction not explicit | Non-blocking | Yes — one sentence | Pending EL |
| FA-C1 | Frontend Architect | Four Zone 1 instruments at 1024×768: layout constraint unspecified | Non-blocking | Add Open Risks note only | Pending EL |
| FA-C2 | Frontend Architect | Decision 14 atomicity: state management design decision required | Non-blocking | No — FA brief + design-decisions.md | Pending EL |
| FA-C3 | Frontend Architect | Decision 17 control plane zone: minimum width unspecified; requires UX ruling | Non-blocking | No — joint EL+UX ruling then FA brief | Pending EL |
| FA-C4 | Frontend Architect | Decision 13 uncertainty bands: "narrow/wide" not linked to ADR-006 schedule | Non-blocking | Yes — reference ADR-006 | Pending EL |
| FA-C5 | Frontend Architect | Decision 11 step axis annotation: 6-step render width at 1024px not validated | Non-blocking | No — FA brief validation | Pending EL |
| CM-1 | Chief Methodologist | Tier 4-5 WARNING-only rule: rationale missing from ADR; risks future override | Substantive | Yes — rationale paragraph | Pending EL |
| CM-2 | Chief Methodologist | "Narrow/wide" uncertainty band widths: must reference ADR-007 or prohibit until specified | Substantive | Yes — replace with ADR-007 deferral | Pending EL |
| CM-3 | Chief Methodologist | Negotiation-defensibility labels: pre-calibration compatibility | Logged — no action | No | Pending EL |

---

## Full Finding Texts

### UX Designer Agent Findings

**UX-F1 — Zone 1 Co-Primary Spatial Arrangement Unspecified**

Decision 2 names four Zone 1 instruments (1A–1D) but does not specify the spatial arrangement of 1B, 1C, and 1D relative to each other. This is correctly a component-level decision for the FA brief — not an ADR-level decision. Two constraints must be honored in that brief: (a) the MDA alert panel has primacy among co-primary instruments — severity ordering (TERMINAL > CRITICAL > WARNING) governs, not framework ordering; (b) all three co-primary instruments must be simultaneously scannable without eye movement longer than the trajectory view scan.

**UX-F2 — "COMPARE_VIEW Zone 1C" Label Is Ambiguous**

Decision 9 uses the label "COMPARE_VIEW Zone 1C: Fiscal equivalence header." In the main instrument cluster, Zone 1C is the PMM widget. A Frontend Architect reading Decision 9 may interpret the fiscal equivalence header as occupying the PMM widget's position in the comparison view — which is not the intended meaning. The fiscal equivalence header is a Zone 1-level element in the comparison view structure, not an assignment to the Zone 1C slot of the main instrument cluster schema. Proposed fix: replace "COMPARE_VIEW Zone 1C" with "COMPARE_VIEW Zone 1 header."

**UX-F3 — Alert Tap Expansion Rendering Mechanism Under-Specified**

Decision 5 states: "tapping an alert expands to show the trajectory view for that indicator at that step — not the entity drawer." The rendering mechanism (inline expansion, sidebar, or coordinated trajectory view update) is not specified. This is a component-level decision for the FA brief. However, the ADR must set one constraint: the trajectory view must remain visible during the expansion. A full-screen overlay occluding the instrument cluster is not acceptable. Proposed addition to Decision 5: "The mechanism must keep Zone 1A visible — a full-screen overlay occluding the instrument cluster is not acceptable. The specific rendering mechanism is a Frontend Architect brief decision."

**UX-F4 — Blue/Orange Color Accessibility: Shape Distinction Not Made Explicit**

Decision 12 specifies the blue/orange visual system. The distinction is already reinforced by shape (filled circle for policy inputs; vertical line across all curves for shocks) — this is the correct pattern for CVD accessibility. The finding is that this shape-based secondary distinction is not stated explicitly as an accessibility requirement. Proposed addition: "Color is not the only distinguishing element — the shape difference (filled circle for policy inputs; vertical line for shocks) is consistent across all three layers, ensuring legibility for users with color vision deficiencies."

---

### Frontend Architect Agent Findings

**FA-C1 — Four Zone 1 Instruments at 1024×768: Layout Constraint Unspecified**

Decision 2 and Decision 1 together require four Zone 1 instruments visible without scroll at 1024×768. At that viewport, after browser chrome (~80px) and persistent header, usable height is ~640–680px. The FA identifies that a two-column layout (trajectory view left, co-primary cluster right) is feasible but the minimum column widths are not specified. The FA brief must define: (a) minimum trajectory view width at 1024×768 (proposed: 560px); (b) minimum right column width (proposed: 400px); (c) vertical stacking order of 1B/1C/1D in the right column. Surfaced jointly to UX Designer and Engineering Lead: if trajectory view minimum exceeds ~620px, the right column drops below 400px and MDA alert panel legibility degrades at tablet font sizes.

**FA-C2 — Decision 14 Atomicity: State Management Architecture Required Before Implementation**

Decision 14 requires all four Zone 1 instruments to update in a single render cycle. React 18 automatic batching covers synchronous updates and updates within a single async callback, but if the four instruments subscribe to state independently (each with its own `useEffect`/`useQuery`), they re-render in four separate cycles. The atomicity contract requires a single shared state atom for `scenarioStep` (current step + all computed instrument data) that all four instruments derive from. The M8 EntityDetailDrawer architecture had instruments with their own loading states — moving to Zone 1 may require a state management refactor. This must be resolved in a design decision in `design-decisions.md` before M9 implementation begins.

**FA-C3 — Decision 17 Control Plane Zone: Minimum Width Unspecified; Joint UX + EL Ruling Required**

Decision 17 requires the control plane reserved zone to accommodate both forms without scroll, but does not specify minimum width. Stacked forms (one above the other) are feasible at ~280px width at 800px height. Side-by-side forms require ~520–560px. At desktop minimum (1280px), side-by-side constrains the trajectory view to ~700px — tight but feasible. The FA cannot set the width constant without a UX ruling on whether "simultaneously visible" means both form headers visible (stacked sufficient) or all form fields visible simultaneously (side-by-side required). This joint decision gates M9 layout implementation.

**FA-C4 — Decision 13 Uncertainty Bands: Not Linked to ADR-006 Band Schedule**

Decision 13 uses "narrow uncertainty band" (Tier 3) and "wide uncertainty band" (Tier 4-5). These are design approximations, not derived from the ADR-006 Decision 1 pre-calibration band schedule (±10% at 1yr, ±35% at 3–5yr). An implementation agent will choose widths by visual preference without this reference, risking false precision. The ADR should reference the ADR-006 band schedule explicitly. Note: Tier 3-5 multipliers for the schedule are not yet defined in ADR-006 — see CM-2 for the Tier 3-5 gap.

**FA-C5 — Decision 11 Step Annotation: Six-Step Render Width at 1024px Not Validated**

At 1024px trajectory view width with 6 steps, each step marker has ~90–100px horizontal space. Three fields (step index, date, event label ≤ 8 words) may overflow at standard font size. The ≤ 8-word constraint partially mitigates this. The FA brief must validate the render width at exactly 1024px with a 6-step scenario and confirm whether the word-count constraint is sufficient or needs a character-count constraint in addition.

---

### Chief Methodologist Findings

**CM-1 — Tier 4-5 WARNING-Only Rule: Rationale Missing, Risks Future Override**

Decision 13 states that Tier 4-5 data produces WARNING-only regardless of computed severity. The rule is methodologically correct: severity labels (WARNING / CRITICAL / TERMINAL) carry an implicit confidence claim about the underlying data. A CRITICAL alert from Tier 1-2 data asserts that a threshold is crossed with high confidence. The same label from SYNTHETIC_MODEL data would assert equivalent confidence — which the data cannot support. The WARNING + "(exploratory — do not cite)" treatment preserves the signal (human cost ledger principle) while honestly representing the epistemic standing (No False Precision principle). The rationale is not in the ADR. An implementation agent reading only the table will see "WARNING-only regardless of computed severity" and may override it as a display bug. The rationale must appear in Decision 13 verbatim to survive session boundaries.

**CM-2 — Uncertainty Band Widths: "Narrow/Wide" Must Be Replaced with ADR-007 Deferral**

Decision 13 specifies visual band treatment for Tier 3 ("narrow uncertainty band") and Tier 4-5 ("wide uncertainty band") without defining the widths. ADR-006 Decision 1 defines the Tier 1-2 pre-calibration band schedule (±10% at 1yr, ±35% at 3–5yr). The Tier 3-5 multipliers for this schedule are not established in any current ADR — they belong in ADR-007 (synthetic data framework). An implementation agent working from "narrow" and "wide" alone will choose widths by visual approximation, producing bands inconsistent with the declared methodology. The band width rendering is ADR-007-gated. The ADR-008 text should state this explicitly rather than implying the widths are already specified.

**CM-3 — Negotiation-Defensibility Labels: Pre-Calibration Compatibility — Logged, No Action**

Decision 5's defensibility labels ("High confidence — cite directly" for Tier 1-2) could appear to conflict with the global ia1_disclosure pre-calibration caveat that applies to all simulation outputs. The labels communicate input data quality of the underlying indicator, not the simulation's overall calibration state — these are distinct claims. The ia1_disclosure in Zone 3 (always present per information-hierarchy.md) resolves the apparent conflict: the specialist has access to the pre-calibration caveat and can frame it appropriately. No ADR change required. Finding logged for institutional memory.

---

## Architect Agent Disposition Recommendations

*The Architect Agent authored ADR-008 and recommends dispositions for all twelve findings. The FA Agent's concurrence on FA-specific items is noted where applicable.*

### Disposition Table

| Finding | Recommended Disposition | Rationale |
|---|---|---|
| UX-F1 | **BRIEF + Open Risks note** | Spatial arrangement of co-primary instruments is a component-level layout decision; the two constraints (MDA primacy, simultaneous scannability) are FA brief requirements. Add one-sentence note to ADR Consequences §Open Risks to make the brief requirement explicit. |
| UX-F2 | **INCORPORATE** | Label is wrong; creates a real implementation ambiguity. One-word fix: "Zone 1C" → "Zone 1 header." |
| UX-F3 | **INCORPORATE** | The "instrument cluster remains visible" constraint is an ADR-level commitment. One sentence. |
| UX-F4 | **INCORPORATE** | Shape-based secondary distinction is load-bearing for CVD accessibility. One sentence makes it a hard contract. |
| FA-C1 | **BRIEF + Open Risks note** | Minimum column widths are brief-level decisions. The joint UX+EL tension (trajectory view minimum vs. right column legibility) is already in Open Risks implicitly; make it explicit with the specific viewport constraint. |
| FA-C2 | **BRIEF** | State management architecture is a Frontend Architect brief + design-decisions.md entry. ADR-008 correctly specifies the *requirement* (atomic update); how it is satisfied is implementation architecture, not ADR. |
| FA-C3 | **JOINT EL+UX RULING → BRIEF** | The "simultaneously visible" definition for control plane forms is a UX ruling that gates the layout constant. Cannot resolve in ADR-008 text — it is not a text change, it is a decision. Recommend EL and UX Designer resolve stacked vs. side-by-side at M9 brief kickoff. |
| FA-C4 | **INCORPORATE** | The ADR should reference ADR-006 Decision 1 for the base band schedule and state that Tier 3-5 multipliers are ADR-007-gated. This is an ADR-level reference, not a brief-level decision. Aligns with CM-2 disposition. |
| FA-C5 | **BRIEF** | Character-count validation at 1024px is a brief-time rendering check, not an ADR specification. The ≤ 8-word constraint remains in Decision 11. |
| CM-1 | **INCORPORATE** | The WARNING-only rationale is essential institutional memory. Without it the rule reads as a display limitation and will be overridden. One paragraph in Decision 13. |
| CM-2 | **INCORPORATE** | "Narrow/wide" replaced with explicit ADR-007 deferral statement. This aligns with FA-C4: both findings point to the same gap. The band width rendering for Tier 3-5 is gated on ADR-007 acceptance. Single combined fix resolves both. |
| CM-3 | **LOG** | No change required. Reasoning documented above for future reference. |

### Architect's Revision Summary

If all INCORPORATE dispositions are approved, ADR-008 requires changes in six locations:

| Location | Change |
|---|---|
| Decision 5 — MDA Alert Panel | Add: "The mechanism [for alert tap expansion] must keep Zone 1A visible — a full-screen overlay occluding the instrument cluster is not acceptable. The specific rendering mechanism is a Frontend Architect brief decision." |
| Decision 9 — Comparison Mode | Replace "COMPARE_VIEW Zone 1C: Fiscal equivalence header" with "COMPARE_VIEW Zone 1 header — Fiscal equivalence header" |
| Decision 12 — Blue/Orange System | Add: "Color is not the only distinguishing element — the shape difference (filled circle for policy inputs; vertical line for shocks) is consistent across all three layers, ensuring legibility for users with color vision deficiencies." |
| Decision 13 — Confidence Tier | Add WARNING-only rationale paragraph (CM-1) and replace "narrow uncertainty band" / "wide uncertainty band" with ADR-007 deferral language (CM-2 + FA-C4 combined) |
| Consequences §Open Risks | Add note: Zone 1 co-primary spatial arrangement constraint (minimum column widths, simultaneous scannability test) is a Frontend Architect brief requirement; see FA-C1 and UX-F1. |
| Consequences §Open Risks | Add note: Control plane zone minimum width constant requires UX ruling on stacked vs. side-by-side form visibility before M9 layout implementation begins (FA-C3). |

---

## Frontend Architect Concurrence

The Frontend Architect Agent concurs with the Architect's disposition recommendations for all five FA findings.

Additional specification on FA-C3 disposition: The UX ruling needed is narrow and binary — stacked forms (both form headers visible without scroll at 800px height, ~280px zone width) vs. side-by-side forms (all form fields visible without scroll, ~560px zone width). Either answer is acceptable from an implementation standpoint. The ruling gates whether the M9 reserved zone width constant is 280px or 560px. This decision should be made before M9 layout implementation begins, not at Mode 3 introduction.

---

## Pending Joint EL + UX Decision (FA-C3)

Before the M9 Frontend Architect brief begins, the Engineering Lead and UX Designer must resolve:

> **"Simultaneously visible" in Decision 17 / Decision 12 means:**
> - (A) Both policy instruments form **header** and scenario shocks form **header** visible without scroll — stacked layout acceptable, ~280px zone width
> - (B) Both forms' **full fields** visible without scroll — side-by-side layout required, ~560px zone width

The answer determines the reserved zone width constant locked into the M9 layout from day one. Stacked (A) is less invasive to the trajectory view width. Side-by-side (B) preserves the epistemic visual separation more clearly but compresses the trajectory view more at 1280px.

---

## Engineering Lead Decision Record

*To be completed by the Engineering Lead.*

**Review decision date:** ___________

**On the six INCORPORATE items:**

| Finding | Decision | Notes |
|---|---|---|
| UX-F2 (Zone 1C label fix) | ☐ Approve ☐ Reject | |
| UX-F3 (Alert tap boundary) | ☐ Approve ☐ Reject | |
| UX-F4 (Shape distinction) | ☐ Approve ☐ Reject | |
| FA-C4 + CM-2 (Band widths → ADR-007 deferral) | ☐ Approve ☐ Reject | |
| CM-1 (WARNING-only rationale) | ☐ Approve ☐ Reject | |
| UX-F1 + FA-C1 Open Risks note | ☐ Approve ☐ Reject | |

**On the joint EL + UX ruling (FA-C3):**

Control plane "simultaneously visible" means:
☐ (A) Headers only — stacked forms, ~280px reserved zone
☐ (B) Full fields — side-by-side forms, ~560px reserved zone

**ADR-008 final acceptance:**

Once approved INCORPORATE items are applied and the FA-C3 ruling is recorded:

☐ ADR-008 status changed from Proposed → Accepted
☐ PR #416 approved for merge

**Engineering Lead sign-off:** ___________

---

## Process Note — This Artifact Type Is New

This is the first ADR Panel Review document in the WorldSim codebase. The artifact type has been added to CLAUDE.md §Canonical Artifact Locations and CODING_STANDARDS.md §ADR Requirements in the same commit as this document. See those files for the canonical naming convention and process description going forward.
