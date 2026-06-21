# WorldSim Architectural Constraints

> **Authority:** Engineering Lead permanent decisions.
> These constraints are not capacity deferrals. They are permanent architectural boundaries derived
> from the founding document. They do not expire at milestone close or with changing team size.
> Changes to this document require Engineering Lead sign-off and a dated record of the decision.

---

## AC-001 — Private Data Inputs Are Prohibited

**Date recorded:** 2026-06-21
**Decided by:** Engineering Lead

### Constraint statement

Private, proprietary, or ministry-owned data inputs are architecturally prohibited in WorldSim.
The simulation operates exclusively on public data sources registered in the `source_registry`.
No user-supplied data upload path, field-mapping interface, or proprietary data isolation layer
may be implemented at any milestone.

### Founding document citation

`docs/vision/worldsim-founding-document.md §Open Source as Strategy`:

> "Open source also provides the methodological transparency that gives the tool credibility.
> Anyone can inspect the assumptions. Anyone can challenge the normalization methodology. Anyone
> can propose improvements. The epistemics of the tool — its claim to be honest about what it
> knows, what it infers, and what it does not know — are only credible if the methodology is
> inspectable. Credibility through transparency is different from credibility through authority,
> and it is the only kind of credibility that is appropriate for a tool designed to challenge
> authority."

The shared public dataset guarantee is the epistemic foundation of WorldSim's negotiating
authority. A finance ministry's ability to cite initial conditions derived from IMF WEO or CBJ
official data — and have those citations independently verifiable by the creditor side — depends
on the analysis running on the same public sources that both parties can inspect. Private data
inputs sever reproducibility: the creditor cannot verify a claim that depends on data only the
ministry holds. This is not a technical limitation; it is the mechanism by which the tool's
authority is constituted. Severing it destroys the tool's primary value.

### Affected issues

| Issue | Title | Disposition |
|---|---|---|
| #976 | feat(data): Path 2 — ministry-owned / proprietary data upload | CLOSED — will not implement (AC-001) |
| #53 | arch: Information Access Architecture — RBAC design | CLOSED — will not implement (AC-001; #53 was a prerequisite for Path 2) |
| G6b design artifacts (`docs/design/path2-data-upload/`) | Path 2 design groundwork filed M14 G6b | Archived — superseded by AC-001; design artifacts retained for historical record only |

### Trigger condition for revisiting

**None — this is a permanent prohibition.** The constraint derives from the founding document's
epistemic foundation, not from implementation difficulty. A future Engineering Lead who believes
this constraint should be revisited must first author a revision to the founding document's
`§Open Source as Strategy` section demonstrating why the reproducibility requirement does not
apply to the proposed use case. That revision must precede any re-opening of the affected issues.

---

## AC-002 — Synthetic Substitution from Public Sources Is Permitted with Mandatory Indicator-Level Disclosure

**Date recorded:** 2026-06-21
**Decided by:** Engineering Lead

### Constraint statement

When real data for a required indicator is unavailable, sparse, or of insufficient quality,
WorldSim may generate synthetic estimates derived from comparable economies, regional
distributions, and historical patterns — subject to three mandatory conditions:

1. **Indicator-level disclosure:** Every synthetic output is flagged at the indicator level, not
   at the session or scenario level. Mixed-mode outputs show per-indicator provenance. A user
   must be able to identify which specific values are synthetic without reading implementation code.

2. **Confidence tier floor:** Synthetic estimates are always Tier 3 or lower in the confidence
   tier system (`docs/DATA_STANDARDS.md §Confidence Tier System`). No synthetic estimate may
   carry a tier annotation implying citable official data.

3. **Meaninglessness threshold:** When uncertainty is so large that the output is directionally
   meaningless, the tool says so and does not generate an uninterpretable distribution band.
   The three-condition meaninglessness threshold from the Chief Methodologist consultation
   (PR #373) applies.

### Founding document citation

`docs/vision/worldsim-founding-document.md §Open Source as Strategy` and
`CLAUDE.md §Synthetic Data and the Data Inference Layer`:

> "Data poverty is not a blocker. WorldSim generates synthetic data via statistical inference
> from comparable economies, regional distributions, and historical patterns when real data is
> unavailable or of insufficient quality. [...] This is what makes the democratization mission
> operationally real. A global south finance ministry with thin, delayed, or unreliable data
> can still use WorldSim — and the tool is honest about what it knows and what it inferred."

The sparse-data problem is addressed through ADR-007 and the confidence tier system, not through
private data uploads. AC-002 and AC-001 are the two halves of the same principle: the public
epistemic foundation is preserved (AC-001), and the accessibility mission is preserved even
under data poverty (AC-002).

### Affected issues and future scope

| Item | Status |
|---|---|
| ADR-007 — Synthetic Data Framework | Future scope — the five-method hierarchy and MDA alert tier table from the Chief Methodologist consultation (PR #373) |
| Methodology audit of ADR-007 against data-sparse countries (Chad, Yemen, Myanmar) | Future scope item — filed for post-ADR-007 completion; not a new capability; validates the framework against real data-poverty conditions |

A methodology audit of ADR-007 against data-sparse countries (Chad, Yemen, Myanmar) is a
future scope item — not a new capability. The audit validates the synthetic substitution
framework against real data-poverty conditions after ADR-007 is complete. It does not change
the synthetic substitution permission; it verifies its implementation.

### Trigger condition for revisiting

**Not applicable — this is a permission with conditions, not a restriction.** The conditions
(indicator-level disclosure, T3 floor, meaninglessness threshold) are standing requirements.
They do not require revisiting; they require implementation compliance. If the Chief
Methodologist determines that the three-condition meaninglessness threshold is producing
overcautious suppression in specific country contexts, that is an ADR-007 calibration decision,
not a constraint revision.

---

## Constraint Log

| Constraint | Date | Decision type | EL action |
|---|---|---|---|
| AC-001 | 2026-06-21 | Permanent prohibition | Issued verbally; recorded here by PM Agent |
| AC-002 | 2026-06-21 | Permission with conditions | Issued verbally; recorded here by PM Agent |
