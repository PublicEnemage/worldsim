---
name: M19-CMA-euro-area-elasticity-calibration
type: implementation-intent
adr: ADR-005 Decision 1 (DemographicModule ELASTICITY_REGISTRY)
issues: "#1623"
status: Filed
authored-by: Chief Methodologist
authored-date: 2026-07-03
implementing-agent: Chief Methodologist
sprint-entry: docs/process/sprint-plans/m19-cm-a-sprint-entry.md
---

# Implementation Intent: M19 CM Sprint A — Euro Area Elasticity Calibration (#1623)

> **Calibration sprint — no ADR.** This intent covers Gap 1 of Issue #1623: installing
> ELASTICITY_REGISTRY entries for Euro area programme countries (GRC entity family priority).
> This is a calibration constant revision within the existing DemographicModule architecture
> established by ADR-005 Decision 1 — the same classification as M17-G1.
>
> **Intent gate structure:** This document satisfies Step 1 of the agent execution lifecycle.
> The CM calibration decision document (`docs/calibration/m19-cm-a-euro-area-calibration-decision.md`)
> is a separate artifact that specifies the chosen constants, uncertainty ranges, and MAGNITUDE
> threshold. It is filed after research and before the implementation PR opens — it closes the
> PENDING gate in sprint entry §2.4 and is the specification the integration test is authored from.
>
> **NM-084 compliance:** The Chief Methodologist is the implementing agent for this sprint.
> Before the implementation PR opens, the CM must post a formal methodological certification
> comment on Issue #1623 certifying the chosen constants and source quality. The PI Agent must
> then post a gate comment confirming sign-off is on record before auto-merge is set.

---

## 1. Source

**Issue:** #1623 — ELASTICITY_REGISTRY non-SSA entity family calibration gap (Gap 1: Euro area)

**ADR reference:** ADR-005 Decision 1 — DemographicModule ELASTICITY_REGISTRY architecture.
No new ADR required. New entries use the existing `CohortElasticity` dataclass and follow the
`source_registry_id` naming convention in `docs/DATA_STANDARDS.md §Data Provenance Requirements`.

**Authored by:** Chief Methodologist
**Date:** 2026-07-03
**Implementing agent:** Chief Methodologist

**Background:** The ELASTICITY_REGISTRY currently covers only Sub-Saharan Africa entity families
(M17-G1 SSA recalibration: Fosu 2011 T3 entries for Q1 informal, Q2 informal, Q1 agricultural).
These entries are appropriate for SEN, ZMB, and SSA comparators. They are structurally
inappropriate for Euro area programme countries (GRC, PRT, IRL, CYP) because:

1. **Fiscal multiplier magnitude differs systematically.** SSA LIC multipliers are calibrated at
   Tier 3 from Fosu (2011) / IMF (2014) LIC evidence. Euro area programme economies are open
   economies with fixed exchange rates (pre-crisis eurozone membership) — Ilzetzki, Mendoza &
   Végh (2013) is the canonical peer-reviewed source for this regime. The IMF (2012) internal
   review "World Economic Outlook Box 1.1" and Blanchard & Leigh (2013) confirm multipliers
   in the 0.9–1.7 range for European fiscal consolidation — materially larger than the SSA
   LIC range.

2. **GDP-to-unemployment transmission structure differs.** SSA Q1 informal poverty responds
   primarily through the GDP growth channel with high elasticity due to thin formal safety
   nets. Euro area countries have structured unemployment insurance systems; the primary
   transmission from fiscal consolidation to household welfare is through unemployment rate
   increase, not directly through the poverty headcount ratio. The Okun's Law coefficient
   for Southern European labour markets (Blanchard & Leigh 2013; OECD Employment Outlook
   2012–2014) is the appropriate calibration source.

3. **Greece 2010 counter-factual is currently DIRECTION_ONLY.** The G2C fixture (#1547)
   compares two fiscal consolidation paths (orthodox IMF primary surplus target vs heterodox
   lower adjustment path). Without Euro area elasticity entries, the DemographicModule cannot
   produce a defensible magnitude claim for the unemployment trajectory divergence between
   paths. The Type B counter-factual comparison is advisory only. This blocks the analytical
   claim that the heterodox path is distinguishable from the orthodox path not just
   directionally but in magnitude — the claim a finance ministry analyst would need to make
   at a restructuring negotiation.

---

## 2. Persona Trace Elements Targeted

> *Calibration infrastructure with no new UI element. Forward trace: calibration change →
> Greece 2010 counter-factual (G2C #1547) produces MAGNITUDE-class unemployment trajectory
> divergence → Persona 2 / Persona 3 analyst can cite a specific defensible unemployment
> differential between the two primary surplus paths at the restructuring table.*

**P-1 — Persona served:**
Indirectly: **Persona 2 — Finance Ministry Negotiator** (Aicha Mbaye archetype,
`docs/ux/personas.md §Persona 2`) and **Persona 3 — Political Advisor** (Andreas
Stefanidis archetype, `docs/ux/personas.md §Persona 3`).

No new UI element is introduced. Forward trace: calibration enables the Greece 2010 Type B
counter-factual to produce a MAGNITUDE-class output — allowing the ministry analyst to state
not just "the heterodox path produces lower unemployment" (DIRECTION_ONLY) but "the
heterodox path produces an unemployment differential of approximately X percentage points
by 2013 under the Ilzetzki multiplier and OECD Okun coefficient, which is within the
calibration uncertainty range of ±Y pp." This constitutes a defensible analytical argument
at the restructuring table, not merely a directional claim.

The Stefanidis persona (Persona 3) specifically needs the auditability of the political
economy claim — "how large is the unemployment consequence?" is his exact question type.
Without MAGNITUDE calibration, the answer is "we can confirm it rises but not by how much."
After calibration, the instrument provides a range with cited sources.

**P-2 — Entry state:**
N/A — Tier 2 calibration infrastructure. Downstream entry state: Greece 2010 scenario
loaded in Mode 1 (Replay) or Mode 2 (Simulation) with counter-factual comparison active.
Journey B Step 3 [Near-Term-Gap] — "Show me what happens under a lower primary surplus path."

**P-3 — Journey reference:** N/A — infrastructure tier. Downstream: Journey B Step 3.

**P-4 — Time/interaction ceiling:** N/A — infrastructure tier. Downstream: the MAGNITUDE
differential must be legible in Zone 1A trajectory view (two-path comparison) within the
Reactive entry state 90-second ceiling. The differential is rendered by the existing
counter-factual comparison UI — not a new element.

**P-6 — Negotiating leverage delivered:**
N/A at calibration tier. Forward trace: calibrated Euro area ELASTICITY_REGISTRY → Greece
2010 counter-factual produces MAGNITUDE-class unemployment divergence → finance ministry
analyst can state "under the heterodox adjustment path, unemployment rises by approximately
[N ± Y] percentage points less by 2013 than under the troika's primary surplus target —
this is the calibrated cost of the fiscal consolidation pace requested by creditors."
The specific N and Y are certified by the CM calibration decision document.

**P-7 — North star capability delivered:**
N/A for calibration infrastructure tier. Forward trace: after Euro area ELASTICITY_REGISTRY
is installed, the Greece 2010 simulation produces a defensible MAGNITUDE estimate of the
unemployment cost differential between fiscal adjustment paths. This enables the Demo 8
evidence portfolio entry for Greece to present the counter-factual not as "direction
confirmed" but as "this is the calibrated magnitude range of what the faster adjustment
path cost in unemployment terms." The ministry analyst can cite direction, order of
magnitude, and uncertainty range — the full analytical argument, not just the direction.

---

## 3. Observable Application State

> *All states are verifiable by an external observer — a QA reviewer or CI system — using
> only the running application and source files. No source code analysis of implementation
> logic is required to confirm any state below.*

### 3.1 Primary observable state — MAGNITUDE integration test

`backend/tests/test_m19_cm_a_elasticity_calibration.py` passes in CI (the `test-backend`
required check is green) when run against the Greece 2010 counter-factual comparison:

- Two scenario runs: (1) GRC entity, orthodox fiscal path (IMF primary surplus target:
  primary balance target of +4.5% GDP by 2014, as in the G2C `build_greece_counterfactual_scenario()`
  fixture); (2) GRC entity, heterodox fiscal path (lower primary surplus: +2.5% GDP by 2014,
  per the documented alternative in #1547)
- The test asserts that the unemployment trajectory divergence between paths at step 4
  (2013, the peak divergence period in historical data) falls within [lower_bound, upper_bound]
  specified in the CM calibration decision document
- Both bounds must be non-zero and the lower bound must be positive (heterodox path produces
  demonstrably lower unemployment at step 4 by a calibrated amount)

**What this confirms:** The ELASTICITY_REGISTRY Euro area entries produce a MAGNITUDE-class
unemployment divergence in the Greece counter-factual — not merely directional confirmation.
The test failing CI is unambiguous evidence the calibration constants are absent or insufficient.

**Dependency on calibration decision document:** AC-1 cannot be authored until the CM
calibration decision document specifies the certified divergence range [lower_bound, upper_bound].
Test authorship follows calibration research, not this intent document.

### 3.2 Secondary observable states

**State A — ELASTICITY_REGISTRY Euro area entries present in source:**
After the implementation PR merges, running:
```
grep -n "ilzetzki\|ILZETZKI\|euro_area\|EURO_AREA\|OECD.*OKUN\|okun" \
  backend/app/simulation/modules/demographic/elasticities.py
```
returns at least one match. All new `CohortElasticity` entries have:
- `confidence_tier=2` — T2 (peer-reviewed academic literature with direct applicability to
  Euro area programme countries; Ilzetzki et al. 2013 published in the Journal of Monetary
  Economics; Blanchard & Leigh 2013 published as an IMF working paper with peer review)
- `source_registry_id` following `ACADEMIC_LITERATURE_*` naming convention
- A non-empty `source` string containing a citable reference with DOI or publication venue

**State B — Calibration decision document filed:**
`docs/calibration/m19-cm-a-euro-area-calibration-decision.md` exists in the repository
and contains (readable by `cat` without source code access):
- A section naming the Euro area entity family and the chosen calibration path
- The fiscal multiplier constant with uncertainty range (point estimate ± range)
- The GDP-to-unemployment elasticity constant with uncertainty range
- The MAGNITUDE threshold: the unemployment divergence [lower_bound, upper_bound] at step 4
  that AC-1 will assert, stated in percentage-point terms
- At least two source citations from `docs/data-sources/approved-sources.md`
- A confidence tier assessment (T2 justification for each source applied)

**State C — Non-regression: SSA entries unchanged:**
After the implementation PR merges:
```
grep -A5 "ACADEMIC_LITERATURE_FOSU_2011" \
  backend/app/simulation/modules/demographic/elasticities.py
```
returns the M17-G1 entry with `elasticity=Decimal("-0.20")` unchanged. All four M17-G1
entries (Fosu 2011 Q1 informal, Ball 2013 Q2 informal, Iceland ADR-020 Channel C,
IMF 2014 Q1 agricultural) remain present with unchanged `source_registry_id` values.

### 3.3 Silent failure detection

**Silent failure — test passes but bounds are too wide to constitute MAGNITUDE:**
If the calibration decision document sets lower_bound=0 or lower_bound is negative, the test
is trivially satisfied without establishing MAGNITUDE fidelity. Detection: the calibration
decision document must explicitly state that the lower bound exceeds the DIRECTION_ONLY
threshold (i.e., lower_bound > 0 pp divergence at step 4). A calibration decision document
with lower_bound ≤ 0 is incomplete and blocks AC-3.

**Silent failure — Euro area entries fire on SSA entities:**
If `CohortElasticity` entries for the Euro area family do not include an entity-family
discriminator, they will fire on all entities including SEN and ZMB. Detection: the
integration test in State 3.1 must include a non-regression assertion that SEN/ZMB
scenarios produce unchanged Q1 informal PHC trajectories after the Euro area entries
are added. If SEN trajectories change, the scoping mechanism is absent and the PR fails.

> **Architecture note:** The current `CohortElasticity` dataclass does not include an
> entity-family field — entries fire on all entities matching event_type and cohort_spec.
> Two implementation options exist:
> (a) Add an `entity_families: list[str] | None` field to `CohortElasticity` (None = all
>     entities, populated = entity-family filter); or
> (b) Use different event_type keys for Euro area events (e.g.,
>     `gdp_growth_change__euro_area_fixed_fx`) — dispatched by a route in the
>     DemographicModule that detects entity family from the entity's currency regime.
>
> Option selection is deferred to the calibration decision document. The CM must select one
> and record the architectural rationale. **The implementing agent must not open the
> implementation PR before this choice is declared in the calibration decision document —
> it is a design decision that affects the non-regression test design (State C above).**

---

## 4. Acceptance Criteria

> *All criteria verifiable from source files and CI output without reading implementation
> logic. Test file: `backend/tests/test_m19_cm_a_elasticity_calibration.py`.*
>
> *AC-1 cannot be authored until AC-3 is satisfied. Sequencing:
> AC-3 (calibration decision document filed) → integration test authored → AC-1 confirmed in CI.*

**AC-1 (MAGNITUDE integration test — #1623):**
In `backend/tests/test_m19_cm_a_elasticity_calibration.py`, running the GRC entity with
the Greece 2010 orthodox vs heterodox counter-factual pair, the test asserts that the
unemployment trajectory divergence at step 4 falls within [lower_bound, upper_bound]
as declared in the CM calibration decision document (State B). Lower bound must be > 0 pp.
The CI `test-backend` check is green on the implementation PR branch.

**AC-2 (ELASTICITY_REGISTRY Euro area entries — #1623):**
At least two new `CohortElasticity` entries in
`backend/app/simulation/modules/demographic/elasticities.py` after the implementation PR
merges, covering:
(a) the fiscal multiplier / GDP channel for Euro area programme economies, OR
(b) a direct fiscal-to-unemployment transmission pathway
All new entries have `confidence_tier=2`, `source_registry_id` following the
`ACADEMIC_LITERATURE_*` convention, and a non-empty `source` string with a citable reference.

**AC-3 (Calibration decision document — #1623):**
`docs/calibration/m19-cm-a-euro-area-calibration-decision.md` exists in the repository
on the implementation PR branch and contains: the named Euro area calibration path, at
least one updated constant with uncertainty range, a MAGNITUDE lower_bound > 0 pp for
step-4 unemployment divergence (or a written defence of why a lower bound of ≤ 0 is the
correct citable position), and at least two source citations. The architectural choice
(entity-family scoping mechanism) is declared and justified.

**AC-4 (Non-regression — SSA calibration unchanged):**
`backend/tests/test_m19_cm_a_elasticity_calibration.py` includes assertions that:
- The SSA Q1 informal `gdp_growth_change` elasticity remains `Decimal("-0.20")`
- SEN entity Q1 informal PHC trajectory under a standard fiscal shock is unchanged from
  the pre-calibration baseline (within floating-point tolerance)
All four M17-G1 `source_registry_id` values remain present and unchanged.

**AC-5 (Entity-family scoping — no cross-contamination):**
If option (a) (entity_families field) is chosen: the new `CohortElasticity` entries have
a non-None `entity_families` field that includes `"GRC"` and excludes `"SEN"` and `"ZMB"`.
If option (b) (event_type routing) is chosen: no `gdp_growth_change__euro_area_fixed_fx`
event fires in SEN or ZMB scenarios (confirmed by the non-regression test in AC-4).

**AC-6 (NM-084 sign-off on record — process gate):**
A Chief Methodologist certification comment is visible on Issue #1623 before the
implementation PR opens. The comment must contain: the point estimate and uncertainty range
for each constant, the MAGNITUDE threshold, the confidence tier assignment with justification,
and the architectural choice for entity-family scoping. A PI Agent gate comment confirming
sign-off is on record is also visible on Issue #1623.

**AC-7 (Pre-push lint gate):**
`cd backend && ruff check . && mypy app/` exits 0 on the implementation PR branch.
The integration test file must pass `mypy` with no new errors introduced.

---

## 4b. Visual Spec (before/after)

N/A — backend only. No UI changes in this sprint group. All acceptance criteria are
source file changes and document artifact verifications confirmable without a browser or
Playwright. The downstream visible change (MAGNITUDE-class output in the Greece 2010
counter-factual view) is confirmed by the integration test, not a Playwright E2E test.

---

## 5. Kryptonite Constraint Check

*Authority: `docs/process/agent-execution-lifecycle.md §Kryptonite Design Constraint (FD-3)`.*

**Does this implementation's primary observable state require specialist mediation for Persona 2
to act on it in the Reactive entry state (90-second ceiling)?**

`[x]` **No — with asymmetry acknowledged.** The calibration change produces a simulation
output (MAGNITUDE-class unemployment divergence between fiscal paths) that is rendered in
the existing Zone 1A counter-factual comparison view. The ministry analyst reads the
divergence as a percentage-point number in the chart — not as a calibration constant.
The calibration constants themselves are in `docs/calibration/m19-cm-a-euro-area-calibration-decision.md`
(methodology transparency, open source as strategy) and are not required reading for use.

**Asymmetry acknowledged:** The T2 confidence tier assignment and the uncertainty range
require methodologist expertise to evaluate. A finance ministry team with in-house economists
can assess whether Ilzetzki et al. (2013) applies to their programme context. A team
without that expertise is not blocked from using the output — they see a number with a
cited source — but they cannot independently verify the calibration choice. This is the
inherent asymmetry in calibration infrastructure: the output is accessible; the methodology
is auditable for those with expertise. Both are served by the open-source transparency
principle.

---

## 6. Out of Scope

**CM Sprint B — Latin America (ARG, ECU, BOL, PER):** Separate sprint entry after CM Sprint A
exits. Céspedes & Velasco (2012) commodity-price transmission and Ilzetzki et al. (2013)
Latin American multiplier range will be addressed in Sprint B.

**CM Sprint C — South and Southeast Asia (PAK, LKA, BGD):** After CM Sprint B. IMF Regional
Economic Outlook Asia-Pacific multiplier estimates and Batini et al. (2012) covered in Sprint C.
May defer to M20.

**Issue #1657 — DemographicModule dead event subscriptions:** This is a separate issue with
its own CM sign-off obligation. CM Sprint A does not modify subscription logic — only
ELASTICITY_REGISTRY entries. Coordination point: if option (a) (entity_families field)
is chosen for scoping, the field addition to `CohortElasticity` must not break existing
subscription handling. The calibration decision document declares the implementation choice
and must include a statement that dead-subscription risk is not introduced.

**GovernanceModule elasticity changes:** Not in scope. CM Sprint A is DemographicModule
ELASTICITY_REGISTRY only.

**Historical Type A fidelity upgrade for Greece 2010:** The existing `test_greece_2010_2012.py`
is DIRECTION_ONLY. This sprint does not attempt to upgrade it to MAGNITUDE_MATCH against
historical actuals — that requires unemployment module endogenous update capability
(capability registry gap). The MAGNITUDE goal here is the counter-factual divergence
between two paths, not simulation-vs-actuals magnitude match.

**Confidence tier upgrade for SSA entries:** The M17-G1 SSA entries remain T3. Upgrading
them to T2 requires Senegal/Zambia quarterly poverty-growth backtesting validation — out
of scope for CM Sprint A.

---

## 7. Test Authorship Obligation

> *The integration test is authored by the Chief Methodologist alongside the calibration
> decision document — the CM holds both the calibration research knowledge and the
> implementation responsibility. The test is authored from the calibration decision document,
> not from this intent document — because the specific divergence threshold [lower_bound,
> upper_bound] is determined by the calibration research and declared in the decision document.*

**QA Lead:** Chief Methodologist (CM holds R for both implementation and test authorship
for #1623, per sprint entry §2.4 and the M17-G1 precedent at sprint entry §2.4.)

**Test authorship deadline:** After the CM calibration decision document is filed (AC-3)
and before the ELASTICITY_REGISTRY implementation PR is opened.

**Test file location:**
- `backend/tests/test_m19_cm_a_elasticity_calibration.py` — MAGNITUDE divergence test (AC-1)
  and non-regression tests (AC-4, AC-5)

**Test structure note:** The test will need to run two separate scenarios (orthodox and
heterodox fiscal paths) for GRC and compare step-4 unemployment trajectories. This requires
the harness infrastructure delivered in G2A (#1546) and the `build_greece_counterfactual_scenario()`
fixture from G2C (#1547). Both are confirmed on `release/m19` (G2D integration PR #1641 merged
2026-07-03).

**No E2E test required.** CM Sprint A has no UI changes. The integration test is the only
QA artifact required.

**QA Lead acknowledgment:**
`[ ]` CM (QA Lead): MAGNITUDE divergence test and non-regression suite authored and filed
      before implementation PR opens. Red-before-implementation confirmed.
      (To be checked when calibration decision document is filed and test is authored.)

---

## Pre-Implementation Obligation Checklist

*Implementing agent must verify all items before opening the implementation PR.*

- [ ] Calibration decision document filed at `docs/calibration/m19-cm-a-euro-area-calibration-decision.md`
- [ ] Entity-family scoping architectural choice declared in calibration decision document
- [ ] Test file `backend/tests/test_m19_cm_a_elasticity_calibration.py` authored, red-before-implementation confirmed
- [ ] CM formal methodological certification comment posted on Issue #1623
- [ ] PI Agent gate comment confirming CM sign-off on record on Issue #1623
- [ ] `git status --porcelain` clean before any branch operations (NM-087)
- [ ] Working from dedicated worktree if G5 session is simultaneously active (NM-088)

---

*Intent document authority: agent-execution-lifecycle.md Step 1.
Sprint entry: `docs/process/sprint-plans/m19-cm-a-sprint-entry.md` (EL Approved 2026-07-03).
Implementing agent: Chief Methodologist. No ADR — calibration constant revision within
ADR-005 Decision 1 (DemographicModule ELASTICITY_REGISTRY).
Issue in scope: #1623 Gap 1 (Euro area entity family — GRC priority).
CM Sprints B and C gated on this sprint's exit.*
