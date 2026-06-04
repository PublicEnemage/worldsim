# ADR-009 Panel Review

> **Artifact type:** ADR Panel Review
> **ADR:** ADR-009 — Simulation Engine Computation Model
> **ADR file:** `docs/adr/ADR-009-simulation-engine-computation-model.md`
> **Status:** Accepted — EL decision recorded 2026-06-03
> **Review date:** 2026-06-03
> **Convention:** `docs/adr/reviews/ADR-NNN-panel-review.md`

---

## Panel

| Reviewer | Role | Status |
|---|---|---|
| Chief Engineer Agent | C — performance baseline, transition strategy, hardware equity | Conditional sign-off ✓ |
| Chief Methodologist (DIC) | C — precision boundary, equivalence testing, statistical integrity | Conditional sign-off ✓ |
| Engineering Lead | A — accountable on all ADR decisions | Accepted ✓ (2026-06-03) |

*Panel composition derived from `docs/process/agent-raci.md §ADR Panel Composition`
(simulation engine ADR: Architect Agent author, Chief Engineer C, Chief Methodologist
via DIC C, Engineering Lead A).*

---

## Findings Register

| ID | Source | Type | Severity | ADR change required? | Status |
|---|---|---|---|---|---|
| CE-F1 | Chief Engineer | Parallel-run CI cost must be bounded | INCORPORATE | Yes — note 2× backtesting cost in Consequences | Resolved ✓ |
| CE-F2 | Chief Engineer | Matrix visualizer scope: must not require browser UI | INCORPORATE | Yes — specify CLI tool, not browser UI | Resolved ✓ |
| CE-F3 | Chief Engineer | Performance target derivation must cite Phase 1 data | INCORPORATE | Yes — cite 174ms ProBook baseline explicitly | Resolved ✓ |
| CM-F1 | Chief Methodologist | Precision loss analysis: max_hops assumption must be explicit | INCORPORATE | Yes — state max_hops = 10 in tolerance derivation | Resolved ✓ |
| CM-F2 | Chief Methodologist | str() conversion justification must be explicit | INCORPORATE | Yes — explain str() avoids binary float artifacts | Resolved ✓ |
| CM-F3 | Chief Methodologist | Equivalence gate must state tolerance is derived, not arbitrary | INCORPORATE | Yes — add derivation note to §Decision 2 | Resolved ✓ |
| EL-F1 | Engineering Lead | Hard cutover must be explicitly rejected with rationale | INCORPORATE | Yes — add rejection rationale to §Decision 1 | Resolved ✓ |

---

## Chief Engineer Review

**CE-F1 — Parallel-run CI cost.**
The parallel-run strategy doubles the backtesting suite runtime during the transition
window. For one milestone this cost is acceptable. The CI cost must be noted explicitly
in Consequences so that future reviewers can re-evaluate if the backtesting suite grows
significantly. INCORPORATE — add to Consequences. Resolved ✓.

**CE-F2 — Matrix visualizer must be a CLI tool.**
A "matrix visualizer" that requires a browser UI would create a Node.js or browser
dependency in the backend test infrastructure — violating the backend/frontend boundary.
The visualizer must produce text or JSON output from a CLI script, compatible with the
existing `backend/scripts/` pattern. INCORPORATE — specify "CLI tool producing JSON or
text output; not a browser UI" in §Decision 4. Resolved ✓.

**CE-F3 — Performance target must be grounded in measured data.**
Issue #217 requires that the performance target be "measured, not estimated." The target
must cite the Phase 1 ProBook baseline (174ms for 1,000 runs) as the derivation basis.
The 60-second target is correct given the safety margin; the derivation must be explicit.
INCORPORATE. Resolved ✓.

---

## Chief Methodologist Review

**CM-F1 — max_hops assumption.**
The precision loss calculation (`10 × 2.22e-16`) assumes `max_hops = 10`. This is the
default `PropagationRule.max_hops` value in the codebase. If `max_hops` is configurable
at the scenario level, a scenario with `max_hops = 50` would have accumulated error
`50 × 2.22e-16 ≈ 1.11e-14` — still well within the `1e-10` tolerance but the assumption
must be stated explicitly. INCORPORATE — state "default `PropagationRule.max_hops`" in
§Decision 5 and add the renewal trigger: "If the 10-hop maximum is revised, the tolerance
derivation must be re-computed." Resolved ✓.

**CM-F2 — str() conversion.**
`Decimal(float_value)` produces the exact binary representation of the float, which may
have a non-terminating decimal expansion. `Decimal(str(float_value))` produces the
human-readable string representation, which is the value the user would recognize.
The justification for using `str()` is non-obvious — it must be stated in the ADR.
INCORPORATE. Resolved ✓.

**CM-F3 — Tolerance derivation.**
A tolerance of `1e-10` that appears in an ADR without a derivation will be revised by a
future implementer who does not know why it was chosen. The derivation (`max_hops ×
float64_epsilon × 1e5`) must appear in the ADR. INCORPORATE. Resolved ✓.

---

## Engineering Lead Review

**EL-F1 — Hard cutover rejection.**
The ADR chooses parallel run over hard cutover. The rationale — "bounded cost preferable
to unbounded risk" — must be stated explicitly in the ADR, not left implicit. A future
Engineering Lead who inherits this decision and wants to change it must be able to read
what the current EL thought and why. INCORPORATE. Resolved ✓.

**Acceptance decision:** All seven findings are INCORPORATE severity and have been
incorporated into the ADR before acceptance. No REJECT findings. The ADR is accepted.
Engineering Lead sign-off: 2026-06-03.
