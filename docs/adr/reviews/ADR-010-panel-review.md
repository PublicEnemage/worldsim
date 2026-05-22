# ADR-010 Panel Review

> **Artifact type:** ADR Panel Review
> **ADR:** ADR-010 — Trajectory View Component Architecture
> **ADR file:** `docs/adr/ADR-010-trajectory-view.md`
> **Status:** Disposition recommendations pending EL decision
> **Review date:** 2026-05-22
> **Convention:** `docs/adr/reviews/ADR-NNN-panel-review.md`

---

## Panel

| Reviewer | Role | Status |
|---|---|---|
| Frontend Architect Agent | C — implementing agent (required per panel composition rule) | Conditional sign-off ✓ |
| UX Designer Agent | C — Zone 1A component decisions | Conditional sign-off ✓ |
| Chief Methodologist | C — confidence tier visual contracts, uncertainty band obligations | Conditional sign-off ✓ |
| Engineering Lead | A — accountable on all ADR decisions | Pending |

---

## Findings Register

| ID | Source | Finding | Type | Severity | ADR change required? | Status |
|---|---|---|---|---|---|---|
| FA-R1 | Frontend Architect | Mode 3 ComposedChart performance: explicit FA brief validation gate required | Non-blocking | No — FA brief requirement | Resolved ✓ (BRIEF) |
| FA-R2 | Frontend Architect | Divergence fill implementation: SVG clipPath vs Recharts Area — brief-level choice | Non-blocking | No — FA brief decision | Resolved ✓ (BRIEF) |
| FA-R3 | Frontend Architect | Trajectory endpoint behavior for partially-computed scenarios: absent vs. sparse | Non-blocking | Yes — clarify Decision 2 | Pending EL |
| FA-R4 | Frontend Architect | Framework color hex values: provisional commitment; CVD validation may require revision | Non-blocking | Yes — editorial, Decision 3 | Pending EL |
| FA-R5 | Frontend Architect | Minimum trajectory view dimensions: must be named requirements in FA brief | Non-blocking | No — FA brief requirement | Resolved ✓ (BRIEF) |
| UD-R1 | UX Designer | Framework color hex values: UX Designer holds authority; ADR commitment is to criteria | Non-blocking | Yes — editorial, Decision 3 (combined with FA-R4) | Pending EL |
| UD-R2 | UX Designer | Multi-case Mode 1 tick rendering: dual entity dates stacked per tick | Non-blocking | No — FA brief requirement | Resolved ✓ (BRIEF) |
| UD-R3 | UX Designer | Confidence badge on curve label (not only legend) for Mode 3 real-time legibility | Non-blocking | No — FA brief requirement | Resolved ✓ (BRIEF) |
| CM-R1 | Chief Methodologist | ADR-007 deferral: band absence must be visible (placeholder label), not silent | Substantive | Yes — add to Decision 10 | Pending EL |
| CM-R2 | Chief Methodologist | Composite confidence tier reflects weakest indicator — methodology correct; log only | Logged — no action | No | Resolved ✓ (LOG) |
| CM-R3 | Chief Methodologist | MDA floor lines must be composite-score-level only; indicator-level floors in Zone 2B | Substantive | Yes — clarify Decision 6 | Pending EL |

---

## Full Finding Texts

### Frontend Architect Agent Findings

**FA-R1 — Mode 3 ComposedChart Performance: No Acceptance Criterion**

At full Mode 3 activation, the ComposedChart includes 4 active Lines, 4 ghost
Lines, 4 Area divergence fills, N MDA floor ReferenceLines, M shock vertical
ReferenceLines, and K policy dot markers. This SVG DOM configuration has not
been validated on the target hardware (8GB/4-core). The ADR correctly notes
this risk in Consequences §Open Risks but does not create an enforcement gate.
The FA brief must include a named acceptance criterion: render time ≤ 100ms
at initial load and on step navigation, measured on a 4-core machine. This is
a BRIEF requirement, not an ADR text change.

**FA-R2 — Divergence Fill Implementation: Two Competing Approaches in ADR Text**

Decision 8 describes two competing divergence fill implementation approaches
("a `<defs>` + `<clipPath>` SVG pattern, or a custom `<Area>` component with
`baseLine` prop") without selecting one. These are not equivalent in complexity
or resilience to step count mismatches. The FA brief must select the approach
after a proof-of-concept render at Mode 3 entry state and document the choice
as a design decision. BRIEF, no ADR change required.

**FA-R3 — Trajectory Endpoint: Partial Computation Behavior**

Decision 2 does not specify whether the trajectory endpoint returns a sparse
array (6 entries with null values at uncomputed positions) or a dense array of
only computed steps (3 entries if 3 of 6 steps complete). This distinction
affects the frontend data handling — a null `composite_score` in a returned
step must mean governance-in-validation, not uncomputed. If both meanings of
null are possible in the same response, the frontend cannot distinguish them.
The ADR must clarify: the endpoint returns only computed steps (dense array,
not sparse). INCORPORATE — Decision 2 clarification.

**FA-R4 — Framework Color Hex Values: Provisional Commitment**

Decision 3 commits to specific hex values for four framework colors without
CVD simulation having been run. If the CVD check fails after ADR acceptance,
changing the colors constitutes an amendment. Two paths to resolve: (a) run
CVD validation before ADR acceptance (blocks ADR acceptance); or (b) explicitly
state hex values are provisional and UX Designer may revise post-CVD without
an amendment. Recommendation: path (b) — provisional commitment with UX
Designer authority. INCORPORATE — editorial note in Decision 3.

**FA-R5 — Minimum Trajectory View Dimensions: Named FA Brief Requirement**

ADR-008 panel finding FA-C1 deferred minimum column widths to the FA brief. This
ADR references minimum width constraints but does not state the actual values.
The FA brief must document as named acceptance criteria: (a) minimum trajectory
view width at 1024×768, (b) minimum width at 1280×800, (c) minimum height at
any supported viewport. Without named values, the "minimum layout contract" has
no contract. BRIEF, no ADR text change.

---

### UX Designer Agent Findings

**UD-R1 — Framework Color Authority: UX Designer Jurisdiction**

Decision 3 proposes specific hex values for four framework colors. Color
selection for Zone 1A instruments is a UX component decision (RACI Row 3:
UX Designer R). The Architect correctly establishes the criteria (distinguishable
from blue/orange, CVD accessible, sufficient contrast) — those are constraint
specifications within Architect authority. However, the specific hex values are
a UX Designer ruling. The ADR text should state that hex values are provisional
and the UX Designer holds authority to revise them after CVD validation. A
failed CVD check does not require an ADR amendment — the UX Designer issues
a revised color ruling. INCORPORATE — editorial note in Decision 3 (combined
with FA-R4 resolution).

**UD-R2 — Multi-Case Mode 1 Tick Rendering: UX Ruling Needed**

Decision 7 states that multi-case Mode 1 alignment uses programme steps, and
that "a secondary 'entity A: MMM YYYY / entity B: MMM YYYY' annotation may
appear per tick." The UX ruling is: this secondary annotation must appear,
not "may appear." When two historical entities are on the same step axis with
different calendar bases, both entities' calendar dates must be visible per tick
so Andreas can simultaneously see the programme-step alignment and the calendar
correspondence. The FA brief must implement stacked per-entity date display per
tick for multi-case Mode 1 — this is a requirement, not an option. BRIEF, no
ADR text change required.

**UD-R3 — Confidence Badge on Curve Label for Mode 3 Legibility**

Decision 10 places the confidence badge only in the Recharts Legend. In Mode 3
active steering, the user's focus is on the trajectory view body (where curves
are updating) — the Legend may be in peripheral vision. A Tier 4-5 curve that
activates during Mode 3 real-time steering must carry a badge visible on the
curve face, not only in the legend. UX ruling: the FA brief must add a small
"(exp)" label adjacent to the most recent data point on Tier 4-5 curves, visible
in the chart body as well as the legend. This is a brief-level component decision.
BRIEF, no ADR text change required.

---

### Chief Methodologist Findings

**CM-R1 — ADR-007 Deferral: Band Absence Must Be Visible, Not Silent**

Decision 10 specifies that uncertainty band rendering is deferred until ADR-007
defines Tier 3-5 width constants. The current text says band rendering "produces
no visible output" during deferral. This is methodologically problematic: a user
who sees a Tier 3 curve and expects an uncertainty band (because Zone 2B shows
banded indicator values) will encounter a trajectory view with no band and no
explanation. Invisible deferrals violate the No False Precision principle —
the tool appears to have more precision than it does (because the band is absent
rather than communicated as deferred). A placeholder label on Tier 3-5 curve
legend entries makes the deferral visible: "(band rendering pending ADR-007)".
This is a substantive methodological requirement. INCORPORATE — add to Decision 10.

**CM-R2 — Composite Tier = Max Indicator Tier: Correctly Stated**

Decision 2 specifies `confidence_tier` at the framework composite score level.
ADR-001 establishes that composite tier propagates via `max()` — the composite's
tier equals the tier of its weakest (highest-numbered) constituent indicator.
This is correct methodology. A governance composite score at Tier 4 because one
of six indicators is Tier 4 renders the full curve dashed at 60% opacity — this
may appear overly conservative when five of six indicators are Tier 1-2. The
max-tier rule is the correct application of the No False Precision principle:
a composite with any Tier 4 component cannot be cited with the confidence of
a pure Tier 1-2 composite. No ADR change required. LOG for institutional memory.

**CM-R3 — MDA Floor Lines: Composite-Score Level Only**

Decision 6 specifies MDA floor overlays at `floor_value` without clarifying
whether these are composite-score-level floors or indicator-level floors projected
onto the composite score axis. The `mda_thresholds` table stores indicator-level
floors (e.g., `poverty_headcount < 0.40`). Projecting these to a composite score
floor would require deriving which composite score corresponds to the indicator
crossing its threshold — a mapping that implies precision in the projection that
does not exist (multiple indicator combinations can produce the same composite
score). The trajectory view must use only composite-score-level MDA floors.
Indicator-level detail belongs in Zone 2B. INCORPORATE — clarify Decision 6.

---

## Architect Agent Disposition Recommendations

| Finding | Recommended Disposition | Rationale |
|---|---|---|
| FA-R1 | **BRIEF** | Named performance acceptance criterion in FA brief. No ADR text change. |
| FA-R2 | **BRIEF** | Implementation approach selected in FA brief after proof-of-concept render. No ADR text change. |
| FA-R3 | **INCORPORATE** | Absent vs. sparse distinction is load-bearing for frontend null handling. Decision 2 clarification applied. |
| FA-R4 | **INCORPORATE** | Combined with UD-R1. Provisional hex values + UX Designer authority note applied to Decision 3. |
| FA-R5 | **BRIEF** | Named dimension acceptance criteria in FA brief. No ADR text change. |
| UD-R1 | **INCORPORATE** | Combined with FA-R4. Single editorial note in Decision 3 resolves both. |
| UD-R2 | **BRIEF** | UX ruling on multi-case tick format is a brief requirement. UX Designer ruling recorded above. |
| UD-R3 | **BRIEF** | Curve-face confidence label is a brief-level component decision. |
| CM-R1 | **INCORPORATE** | Invisible deferrals are a No False Precision violation. Placeholder label spec applied to Decision 10. |
| CM-R2 | **LOG** | Methodology is correct. Institutional memory note only. |
| CM-R3 | **INCORPORATE** | Composite-score-level floors only. Indicator-level floor projection is methodologically dishonest. Decision 6 clarification applied. |

### Architect's Revision Summary

Four INCORPORATE items have been applied to the ADR prior to this panel review's
completion (incorporated during review — pre-EL acceptance pass):

| Location | Change Applied |
|---|---|
| Decision 2 — Trajectory Endpoint | Added: partial computation behavior; endpoint returns computed steps only (dense, not sparse); null composite_score = governance-in-validation, not uncomputed step |
| Decision 3 — Framework Colors | Added: hex values are provisional; ADR-level commitment is to the criteria; UX Designer holds authority to revise after CVD validation without amendment |
| Decision 6 — MDA Floor Overlay | Added: composite-score-level floors only; indicator-level thresholds belong in Zone 2B; projection from indicator to composite is not architecturally supported |
| Decision 10 — Confidence Tier | Added: deferral period placeholder label `"(band rendering pending ADR-007)"` on Tier 3-5 legend entries; disappears when ci values become non-null |

---

## Engineering Lead Decision Record

*To be completed by the Engineering Lead.*

**Review decision date:** ___________

**On the four INCORPORATE items (already applied to ADR text):**

| Finding | Decision | Notes |
|---|---|---|
| FA-R3 (endpoint partial computation) | ☐ Approve ☐ Reject | |
| FA-R4 + UD-R1 (color hex provisional + UX Designer authority) | ☐ Approve ☐ Reject | |
| CM-R1 (band deferral placeholder) | ☐ Approve ☐ Reject | |
| CM-R3 (composite-score floors only) | ☐ Approve ☐ Reject | |

**ADR-010 final acceptance:**

Once all INCORPORATE items are approved:

☐ ADR-010 status changed from Proposed → Accepted
☐ PR approved for merge

**Engineering Lead sign-off:** ___________
