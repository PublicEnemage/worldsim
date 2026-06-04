# ADR-011: Non-Linear Propagation Architecture

## Status
Accepted

**Valid Until:** Milestone 11.5 — Usability Validation and Experience Audit
**License Status:** CURRENT — Accepted 2026-06-04 (M11 exit review)

**Diagram:** `docs/architecture/ADR-011-propagation-modes.mmd`

**Milestone Review Log:**

| Milestone | Review date | Triggers fired | Action |
|---|---|---|---|
| M11 exit | 2026-06-04 | No triggers fired. PropagationMode enum unchanged. No new propagation modes added. Diagram added (`ADR-011-propagation-modes.mmd`). License renewed to M11.5. | CURRENT |

## Context

The current event propagation engine (ADR-001, Amendment 1) applies a linear
diffusion model: `delta × attenuation_factor × edge.weight` per hop. ARCH-REVIEW-001
findings BS-008 (Chief Methodologist) and BS-015 (Social Dynamics) identified this as
a category error for crisis and cascade dynamics:

- **Bank runs** (Lebanon 2019, Northern Rock 2007): self-reinforcing acceleration above
  a tipping threshold — no linear model can represent the discontinuous transition.
- **Currency crises** (Thailand 1997): correlated de-leveraging from herding behaviour
  violates standard additive accumulation assumptions.
- **Debt spirals**: interest rate premium rises with debt, raising deficit, raising debt —
  a compounding feedback the linear engine cannot represent.
- **Social panics**: information cascades propagate faster than any diffusion process.

Issue #29 specifies the required extension: a `PropagationMode` field on `PropagationRule`
with `LINEAR` (backward-compatible default), `THRESHOLD` (tipping-point gate), and
`CASCADE` (self-reinforcing amplification with ceiling) modes. An A/B validation report
against Lebanon 2019–2020 and Thailand 1997–2000 is required before the issue can close.

ADR-001 validity context confirmed CURRENT (M11 review, 2026-06-02). Issue #40 conditions
(STD-REVIEW-001 complete, ADR-001 CURRENT, parameter calibration tier system in place)
are all met at M11 entry.

## Decision

### Decision 1: PropagationMode enum with three values

```python
class PropagationMode(str, Enum):
    LINEAR    = "linear"     # existing behaviour — backward compatible default
    THRESHOLD = "threshold"  # tipping-point gate
    CASCADE   = "cascade"    # self-reinforcing amplification
```

`LINEAR` is the Python default on `PropagationRule.propagation_mode`. All existing
callers that do not set `propagation_mode` receive unchanged behaviour. This is a
strict backward-compatibility guarantee.

### Decision 2: Criteria for selecting propagation mode

`propagation_mode` is set per `PropagationRule`, not per-scenario. This is intentional:
different relationship types in the same scenario have different propagation physics.
A banking contagion edge in a scenario that also has trade edges should be `CASCADE`
while trade edges remain `LINEAR`. A scenario-level toggle would force a single mode
for all relationships and is not the right design.

Selection criteria:

| Relationship type | Mode | Rationale |
|---|---|---|
| Bilateral trade | LINEAR | Structural shocks diffuse gradually via import/export channels |
| IMF conditionality | LINEAR | Policy transmission is deliberate with policy lag |
| Banking system contagion | CASCADE | Self-reinforcing: deposit withdrawal → bank insolvency → further withdrawals |
| Currency peg collapse | CASCADE | Herding behaviour produces correlated de-leveraging |
| Debt spiral | CASCADE | Compounding feedback: debt↑ → rate↑ → deficit↑ → debt↑ |
| Social legitimacy cascade | THRESHOLD | Below threshold: grievances absorbed; above: legitimacy collapse |
| Trade bloc contagion | THRESHOLD | Tipping point: below threshold, partners absorb; above, cascade begins |

### Decision 3: THRESHOLD mode mechanics

A THRESHOLD-mode propagation rule applies per-hop attenuation identically to LINEAR,
but gates accumulation: a computed delta at a target entity is only applied if at
least one attribute's absolute value meets or exceeds `PropagationRule.threshold`.

```
computed_delta = base_delta × attenuation_factor × weight
if max(|computed_delta[attr]| for attr in attrs) >= threshold:
    accumulate(target, computed_delta)
else:
    # delta absorbed — target unchanged for this edge
```

`threshold=0.0` (the default) is mathematically equivalent to LINEAR — all deltas
are above zero and accumulate. Callers that do not set `threshold` get LINEAR behaviour.

THRESHOLD models tipping-point dynamics: small shocks are absorbed by the target
entity's buffer (institutional capacity, reserve coverage, social cohesion) and have
no propagation effect. Large shocks that exceed the buffer cascade to connected entities.

### Decision 4: CASCADE mode mechanics

A CASCADE-mode propagation rule amplifies the delta at each hop instead of attenuating
it. The per-hop scale is `(1 / attenuation_factor) × weight` — the inverse of LINEAR
attenuation. A rule with `attenuation_factor=0.5` amplifies by 2× per hop.

A ceiling parameter caps the total accumulated magnitude relative to the base delta:

```
scale_per_hop = (1 / attenuation_factor) × weight
amplified = current_delta × scale_per_hop
for each attribute k:
    if |amplified[k]| > ceiling × |base_delta[k]|:
        amplified[k] = ceiling × |base_delta[k]| × sign(amplified[k])
```

`ceiling=1.0` (the default) means no amplification beyond the base delta magnitude —
callers must explicitly set `ceiling > 1.0` to enable cascade dynamics. This is a
conservative default that requires explicit intent from the scenario author.

The ceiling is enforced against the original base delta, not the current hop's input.
This prevents unbounded exponential runaway across multi-hop chains.

### Decision 5: Backward compatibility guarantee

- `PropagationRule` default values: `propagation_mode=PropagationMode.LINEAR`, `threshold=0.0`, `ceiling=1.0`
- With these defaults, `_propagate_rule` takes the `LINEAR` branch identically to
  the pre-ADR-011 code path.
- All existing unit tests must pass without modification.
- Verified: 918/918 unit tests pass after ADR-011 implementation.

## Consequences

**Positive:**
- CASCADE mode enables correct modelling of self-reinforcing panics for Lebanon 2019,
  Northern Rock 2007, Thai 1997, and Argentina 2001 — the primary failure modes in the
  WorldSim backtesting corpus.
- THRESHOLD mode enables modelling legitimacy collapse, reserve adequacy tipping points,
  and trade bloc contagion propagation.
- Backward compatibility is strict — no existing scenario, fixture, or test is affected.
- Per-rule granularity enables mixed-mode scenarios (banking=CASCADE, trade=LINEAR)
  that reflect real economic structure.

**Negative:**
- CASCADE parameters (`ceiling`, `attenuation_factor` as amplification) require
  empirical calibration before being used in official backtesting fixtures.
  Calibration is tracked in Issue #44 (parameter calibration tier system).
- The A/B validation report (`docs/backtesting/cascade-validation-report.md`)
  demonstrates that single-entity fixtures are structurally unaffected by mode
  selection. Full A/B validation across multi-entity graphs requires Lebanon and
  Thailand multi-entity fixtures that do not yet exist. This is a M12 deliverable.

**Known blind spots (documented in cascade-validation-report.md):**
- Optimal `ceiling` values for banking contagion, currency crises, and debt spirals
  are not yet calibrated. Default `ceiling=1.0` prevents uncalibrated amplification.
- Amplification factors from Brunnermeier (2009), Gorton (2010), and Gai & Kapadia
  (2010) should be incorporated when multi-entity graphs are built.

## Panel Review

See `docs/adr/reviews/ADR-011-panel-review.md`.

## References

- ARCH-REVIEW-001 BS-008 (Chief Methodologist) and BS-015 (Social Dynamics)
- ADR-001 — Simulation Core Data Model (validity CURRENT, M11)
- Issue #29 — feat: implement non-linear propagation mode
- Issue #40 — ADR: Non-Linear Propagation Architecture (closes)
- Issue #44 — parameter calibration tier system
- `docs/backtesting/cascade-validation-report.md` — A/B validation report
- Brunnermeier (2009), "Deciphering the Liquidity and Credit Crunch 2007–2008"
- Gorton (2010), "Slapped by the Invisible Hand: The Panic of 2007"
- Gai & Kapadia (2010), "Contagion in financial networks"
