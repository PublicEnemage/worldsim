---
name: m16-g4-sprint-entry
type: sprint-entry
milestone: M16 — Distributional Visibility
sprint-group: G4
status: EL Approved 2026-06-24 — implementation in progress
authored-by: PM Agent
authored-date: 2026-06-23
el-approved: 2026-06-24
release-branch: release/m16
sop-reference: docs/process/sprint-planning-sop.md
---

# Sprint Entry — M16, G4: Distributional Infrastructure

**Status:** EL Approved 2026-06-24 — implementation in progress
**Date authored:** 2026-06-23
**Release branch:** `release/m16`
**Sprint plan:** `docs/process/sprint-plans/m16-sprint-plan.md` (EL Approved 2026-06-23)

*Authority: `docs/process/sprint-planning-sop.md §Sprint Entry Gate` (Phase C output).
G4 covers distributional infrastructure: `Quantity` schema extension + SyntheticDataEngine MVP
(#22 scoped), distributional comparison variance/percentile API (#102), and calibrated
ecological-to-financial transmission (#275). G4 is capacity-allowing — it is not on the
Demo 6 critical path and is the first group to be cut if scope is constrained after G1/G2/G3.
The sprint plan explicitly designates G4 as the scope cut target before any other group.
G4 implementation PR may not open until (a) G2 is BPO-accepted (Wave 3 dependency), (b) the
intent document is filed, and (c) QA tests are authored. The ADR-007 coverage assessment for
#22 is embedded in §2.2 below and replaces the need for a separate Architect consultation on
ARCH-012 — no new ARCH entry is required.*

---

## Section 1 — Sprint Identification

| Field | Value |
|---|---|
| Milestone | M16 — Distributional Visibility |
| GitHub Milestone | #17 |
| Sprint group | G4 — Distributional Infrastructure |
| Release branch | `release/m16` |
| Sprint plan document | `docs/process/sprint-plans/m16-sprint-plan.md` |
| Exit checklist issue | #985 |
| Sprint groups in scope | G4 only |
| ADR gate | #22 scoped: ADR-007 SUFFICIENT (§2.2 assessment); #102: no ADR; #275: ADR-012 ACCEPTED |
| ARCH-012 required? | **No** — ADR-007 scope is sufficient for the M16-scoped #22 deliverable; §2.2 documents the basis |
| Implementing agents | Chief Engineer Agent (backend: schema migration, SyntheticDataEngine, ecological transmission, comparison API); Frontend Architect Agent (per-indicator synthetic badge in Zone 1B/1D disclosure) |
| Wave | Wave 3 — no earlier than G2 BPO-accepted; G8 gate (#843) does not depend on G4 |

---

## Section 2 — Entry Invariants Checklist

*All items must be checked before any implementation PR is opened for G4.
An unchecked invariant blocks implementation from beginning.*

### 2.1 — Structural gates

- [x] **Release branch exists:** `release/m16` cut from `main` 2026-06-23 (commit 07c92b8)
- [x] **CI trigger verified:** `.github/workflows/ci.yml` `pull_request: branches` includes
  `release/m*` — confirmed at M16 kickoff 2026-06-23. Required checks: `changes`, `lint`,
  `test-backend`, `playwright-e2e`, `compliance-scan`, `branch-naming`. KI-005 permanent fix
  (`do_not_enforce_on_create: true`) applied 2026-06-20.
- [x] **Sprint plan EL-approved:** `docs/process/sprint-plans/m16-sprint-plan.md`
  `el-approved: 2026-06-23` (PR #1148 merged 2026-06-23)

### 2.2 — ADR prerequisite gate

*The sprint plan (§ADR Prerequisites) marks G4 #22 as CONDITIONAL pending ADR-007 coverage
confirmation at sprint entry. That confirmation is embedded here. Per the sprint plan:
"If coverage is insufficient, file ARCH-012 and author an amendment." The assessment below
determines whether ARCH-012 is needed.*

---

**ADR-007 Coverage Assessment for Scoped #22**
**Authored:** 2026-06-23
**Scope:** Issue #22 — uncertainty quantification, scoped to M16 Demo 6 requirements only:
`Quantity` schema extension + `SyntheticDataEngine` MVP (Methods E and B) + per-indicator
synthetic badges on Zone 1B cohort rows and Zone 1D indicators.

#### ADR-Coverage-1 — Quantity Schema Extension

ADR-007 §Consequences explicitly requires four new fields on `Quantity` when `is_synthetic:
True`: `is_synthetic: bool`, `synthetic_method: str | None`, `comparison_group_id: str | None`,
`holdout_validated: bool | None`. An Alembic migration is required for all four fields.

This is the primary deliverable that has been deferred across M12–M15 (ADR-007 Validity
Context renewal history). The M16 scoped #22 begins this implementation.

**Coverage verdict: FULLY COVERED by ADR-007 §Consequences.** No new architectural decision
is required. The Alembic migration pattern follows existing `Quantity` field migration
precedents.

#### ADR-Coverage-2 — SyntheticDataEngine Implementation Scope

ADR-007 §Consequences specifies: "SyntheticDataEngine — responsible for method selection,
execution, and absence declaration." §Consequences §Implementation Sequence orders:
(1) `Quantity` schema extension + migration; (2) comparison group registry structure; (3)
SyntheticDataEngine — Method E (structural absence) and Method B (MICE) first; (4) Method A
(Hierarchical Bayesian) — requires comparison group registry populated; (5–7) UI disclosure,
anomaly detection.

The M16 G4 scope covers steps (1) and partial (3): schema extension + Method E + Method B
only. Method A (Hierarchical Bayesian) requires the comparison group registry to be populated
first — that is explicitly out of G4 scope (see §3.2). Comparison group registry structure
(step 2) is a prerequisite for Method A, not for Methods E and B; G4 does not need to
implement it.

Method E (Structural Absence Declaration): triggered when MNAR, fewer than 3 comparables,
or CI width > 4× point estimate — ADR-007 §Section 1 and §Section 6. The SEN scenario will
require Method E declarations for any human capital indicator where World Bank coverage
is unavailable for Senegal.

Method B (MICE — Multiple Imputation by Chained Equations): triggered for ≥80% observed
data, gap ≤3 periods, bounded on both sides — ADR-007 §Section 1. Applicable where SEN
has partial historical coverage.

**Coverage verdict: FULLY COVERED by ADR-007 §Section 1 and §Consequences §Implementation
Sequence.** No new synthetic method is proposed. No holdout gate thresholds are changed.
No new architectural decision is required beyond what ADR-007 specifies.

#### ADR-Coverage-3 — Per-Indicator Synthetic Badge (Frontend)

ADR-007 §Section 2 specifies: "Per-indicator synthetic badge — every indicator slot in the
UI carries a distinct badge when its value is synthetic. The badge must be visible without
hovering, clicking, or opening a drawer."

Zone 1B cohort rows already display a tier label (e.g., "T3") from the G2 implementation.
The G4 scoped #22 connects this label to the actual `Quantity.is_synthetic` and
`Quantity.synthetic_method` fields: "T3" for `SYNTHETIC_COMPARABLE`, "T4" for
`SYNTHETIC_MODEL`, "T5/SAD" for `STRUCTURAL_ABSENCE`. For real-data indicators (no
`is_synthetic: True`), the tier label remains the existing confidence tier display.

This is a disclosure wiring task: connecting the G2 Zone 1B tier label rendering to the
newly populated `Quantity` fields, not a new UI pattern. Zone 1D indicators are treated
identically.

**Coverage verdict: FULLY COVERED by ADR-007 §Section 2.** No new UI pattern is introduced.
The badge is already present in G2; G4 makes it data-driven.

#### ADR-Coverage-4 — Scenario Banding (Out of Full G4 Scope — Not Needed for Demo 6)

ADR-007 §Section 3 defines the Scenario Banding Specification: P10/P50/P90 from comparison
group posterior distributions, labeled as inference uncertainty bands distinct from
BandingEngine model uncertainty bands.

Full scenario banding display (the "distributional bands on cohort output" named in the
sprint plan for #22) would require the comparison group registry to be populated and Method A
to be implemented — both out of G4 scope. However, the `Quantity` schema extension (step 1)
and Methods E + B (step 3 partial) are prerequisites for scenario banding, and G4 delivers
those prerequisites.

Demo 6 does not require rendered P10/P50/P90 bands — it requires structural absence
declarations and MICE tier labels where SEN data is unavailable. The M16 scoped #22 does
not implement Section 3 banding display; it implements the prerequisite schema and engine
that Section 3 depends on.

**Coverage verdict: Section 3 is architecturally COVERED by ADR-007 for future
implementation. The M16 scoped deliverable does not implement Section 3 banding display;
the implementation sequence (ADR-007 §Consequences) correctly defers it to after
comparison group registry is populated.**

#### ADR-Coverage Conclusion

| Scoped deliverable | ADR-007 coverage | Gate |
|---|---|---|
| `Quantity` schema extension (4 fields + migration) | §Consequences — explicit | **CLEAR** |
| SyntheticDataEngine Method E (Structural Absence) | §Section 1, §Section 6, §Consequences §Seq step 3 | **CLEAR** |
| SyntheticDataEngine Method B (MICE) | §Section 1, §Consequences §Seq step 3 | **CLEAR** |
| Per-indicator synthetic badge in Zone 1B/1D | §Section 2 — explicit; G2 label already present | **CLEAR** |
| Comparison group registry structure | §Consequences — out of G4 scope (Method A prerequisite) | **OUT OF SCOPE** |
| Method A (Hierarchical Bayesian) | §Section 1, §Consequences §Seq step 4 | **OUT OF SCOPE — registry required first** |
| Section 3 banding display (P10/P50/P90) | §Section 3 — architecturally covered; not G4 deliverable | **OUT OF SCOPE — deferred** |
| Anomaly detection | §Section 7 — TSC gate required; permanently out of G4 scope | **OUT OF SCOPE — TSC gate** |

**ARCH-012 required: NO.** ADR-007 is sufficient for all G4 deliverables on #22. No sixth
synthetic method is proposed, no holdout gate is changed, no meaninglessness threshold is
adjusted, no `Quantity` field is renamed — none of ADR-007's renewal triggers fire. ARCH-012
does not need to be filed.

---

**ADR gate status table:**

| Group issue | Required ADR | ADR status | Gate |
|---|---|---|---|
| G4 — #22 (Quantity schema + SyntheticDataEngine MVP + badges) | ADR-007 | ACCEPTED 2026-05-23 — §2.2 confirms scope coverage | **CLEAR** |
| G4 — #102 (distributional comparison API) | None — API extension within existing `/compare` endpoint patterns per Architect consultation | N/A | **CLEAR** |
| G4 — #275 (ecological-to-financial transmission) | ADR-012 (External Sector Module, ARCH-006) — ACCEPTED 2026-06-05 | ACCEPTED | **CLEAR** |

- [x] All G4 ADR prerequisites are clear. ADR-007 is sufficient for scoped #22 (§2.2 assessment).
  ADR-012 covers #275 module boundary. No ADR is required for #102.
  ARCH-012 is **not required**. Gate: **CLEAR**.

### 2.3 — Intent document gate

*An intent document must be filed before any G4 implementation PR opens.
(Authority: `docs/process/agent-execution-lifecycle.md` Step 1)*

- [x] Intent document filed for all G4 deliverables — **FILED 2026-06-24**

| Deliverable | ADR reference | Intent document path | Filed? |
|---|---|---|---|
| #22 (scoped) — Quantity schema + SyntheticDataEngine MVP + per-indicator badges | ADR-007 (§Consequences §Implementation Sequence steps 1 + 3 partial) | `docs/process/intents/M16-G4-2026-06-23-distributional-infrastructure.md` | **Yes — FILED 2026-06-24** |
| #102 — Distributional comparison variance/percentile | None | (same intent document) | **Yes — FILED 2026-06-24** |
| #275 — Calibrated ecological-to-financial transmission | ADR-012 module boundary | (same intent document) | **Yes — FILED 2026-06-24** |

**Completeness gate for #22:** The QA Lead must be able to write backend tests for the
`Quantity` schema migration (4 fields; Alembic upgrade head applies cleanly; existing ZMB
8-step scenario unaffected), the SyntheticDataEngine method dispatch (Method E fired for
MNAR/< 3 comparables/CI > 4×; Method B fired for ≥80% observed data/gap ≤3 periods), and
the per-indicator badge wiring (Zone 1B cohort row tier label is data-driven from
`Quantity.is_synthetic` and `Quantity.synthetic_method`, not hardcoded) — all without
reading implementation code.

**Completeness gate for #102:** The QA Lead must be able to write backend tests for the
`GET /compare` response shape extension (variance, p10, p50, p90 per indicator) and
frontend tests for the Zone 1A variance band display.

**Completeness gate for #275:** The QA Lead must be able to write backend tests for the
ecological-to-financial transmission coefficient application and a historical validation
case (Zimbabwe agricultural collapse ± tolerance band on trajectory delta at N steps).

### 2.4 — QA test authorship gate

*QA tests must be authored from the intent document's acceptance criteria before
implementation code is written. (Authority: `docs/process/agent-execution-lifecycle.md` Step 2)*

- [x] QA test files authored for G4 before implementation begins — **AUTHORED 2026-06-24**

| Deliverable | Intent document | Test file path | Authored before implementation? |
|---|---|---|---|
| #22 (scoped) — backend (schema migration; SyntheticDataEngine dispatch; indicator bounds) | `docs/process/intents/M16-G4-2026-06-23-distributional-infrastructure.md` | `backend/tests/test_m16_g4_distributional_infrastructure.py` | **Yes — AUTHORED 2026-06-24** |
| #22 (scoped) — frontend (synthetic badge wiring in Zone 1B/1D) | (same intent document) | `frontend/tests/e2e/m16-g4-distributional-infrastructure.spec.ts` | **Yes — AUTHORED 2026-06-24** |
| #102 — backend (compare API distribution shape) + frontend (variance band display) | (same intent document) | (same test files, separate describe blocks) | **Yes — AUTHORED 2026-06-24** |
| #275 — backend (ecological transmission coefficient + historical validation) | (same intent document) | (same backend test file, separate describe block) | **Yes — AUTHORED 2026-06-24 (AC-EE-1/AC-EE-2 deferred — EE DIC review on #275 required first)** |

*Soft-skip guard (NM-056 follow-up, M16 exit condition 6): No `test.skip()` or conditional
skip patterns in any G4 test file. The `Quantity` schema migration test must not soft-skip
on database startup failure — the G4 implementation PR must not merge until these tests
run and pass in CI.*

### 2.5 — Wave 3 dependency gate (G2 BPO-acceptance required)

*The sprint plan §Sprint Sequencing places G4 in Wave 3: "no earlier than G2 complete."
This gate is a sequencing constraint — the G4 implementation PR may not open until G2 is
BPO-accepted. The sprint entry document may be filed and EL-approved before G2 exits;
EL approval of this entry does not authorize the implementation PR to open before G2 exits.*

- [x] G2 BPO-acceptance on record — **CONFIRMED 2026-06-24**
  G2 sprint exit document filed (`docs/process/sprint-plans/m16-g2-sprint-exit.md`;
  PI Agent confirmed 2026-06-24; PR #1174 + #1176 merged to `release/m16`).
  G2 implementation: PR #1173 merged 2026-06-24; 209/209 E2E tests passing; BPO ACCEPT
  on record for #986, #987, #1163. G3 also confirmed closed (PR #1180 merged 2026-06-24).
  Wave 3 gate: **CLEAR.**

**Wave 3 gate confirmation:** G2 sprint exit is PI-confirmed. The G4 implementation PR may
open once §2.3 (intent document) and §2.4 (QA tests) are satisfied.

---

## Section 3 — Scope Declaration

### 3.1 — Issues in scope

*Observable application states are pre-implementation specifications. All must be confirmed
in the running application at Step 4 Verify before the G4 implementation PR may merge.*

| Issue | Title | Priority | Observable application state |
|---|---|---|---|
| #22 (scoped) | feat: uncertainty quantification — distributional scenario bands (M16 scope: Quantity schema + SyntheticDataEngine MVP) | near-term / capacity-allowing | (a) **Schema:** `alembic upgrade head` applies cleanly; the `quantity` table in the database has four new columns: `is_synthetic BOOLEAN NOT NULL DEFAULT FALSE`, `synthetic_method VARCHAR`, `comparison_group_id VARCHAR`, `holdout_validated BOOLEAN`. Existing ZMB 8-step and SEN 100-step scenario runs are unaffected — `is_synthetic` defaults to False for all indicators where no synthetic inference is applied. (b) **Engine — Method E:** When a DemographicModule indicator for SEN has fewer than 3 comparable country observations in the source registry, the `SyntheticDataEngine` sets `is_synthetic: True`, `synthetic_method: "STRUCTURAL_ABSENCE"`, and the `Quantity.value` is `None`. The simulation returns a Structural Absence Declaration for that indicator slot. (c) **Engine — Method B:** When a DemographicModule indicator for SEN has ≥80% observed historical data with a gap ≤3 periods bounded on both sides, the `SyntheticDataEngine` applies MICE imputation, sets `is_synthetic: True`, `synthetic_method: "SYNTHETIC_COMPARABLE"`, and populates `Quantity.value` with the imputed estimate. Tier sub-label is T3 (short gap, strong flanking) or T4 (longer gap) per ADR-007 §Section 4. (d) **Frontend badge:** In Zone 1B, a cohort row whose underlying `Quantity.is_synthetic` is True displays a tier sub-label badge reflecting the actual `synthetic_method`: "T3" for SYNTHETIC_COMPARABLE (validated), "T4" for SYNTHETIC_MODEL, "T5/SAD" for STRUCTURAL_ABSENCE — not a hardcoded value. The badge is visible without hover, click, or drawer navigation (ADR-007 §Section 2 mandatory disclosure). Real-data indicators (e.g., ZMB poverty_headcount_ratio from World Bank) show their existing confidence tier label unchanged. (e) **Non-regression:** `GET /simulate` for ZMB ECF at default step count (≤8 steps) returns identical trajectory data to pre-G4; no `is_synthetic: True` flags appear on indicators with Path 1 real data sources. The 25-year SEN projection (`projection_steps=100`) continues to run and display per G3 observable state. |
| #275 | feat(simulation): calibrated ecological-to-financial transmission | near-term / capacity-allowing | (a) **Transmission pathway:** The simulation engine accepts a calibrated ecological coefficient `ecological_shock_coefficient` (dimensionless, range 0.0–1.0) on `SimulationRequest`. When provided, the engine applies the ADR-012 ExternalSectorModule boundary: a soil-degradation-to-agricultural-export-to-fiscal-revenue transmission pathway reduces the fiscal sector's revenue projection by `ecological_shock_coefficient × base_agricultural_export_share × arable_land_degradation_rate` per step. `api_contracts.yml` is updated in the same commit to document the optional `ecological_shock_coefficient` parameter (capped at 1.0; default: 0.0 → no ecological transmission applied; no regression for existing requests). (b) **Historical validation:** The implementing agent must run the ZMB scenario with the ecological coefficient set to the Zimbabwe 2005 land reform parameter (to be derived by the Chief Engineer from World Bank agricultural data and documented in the Step 4 Verify verdict) and confirm the resulting fiscal revenue trajectory stays within ±30% of the documented Zimbabwe agricultural-to-fiscal impact at 4-step horizon. The calibrated coefficient value and validation result must appear in the Step 4 Verify verdict. (c) **Ecological Economist DIC review:** The calibrated coefficient must be reviewed by the Ecological Economist DIC agent before the implementation PR is marked ready — the transmission pathway is within their domain. A comment on #275 or in the intent document records the review. |
| #102 | arch(api): distributional scenario comparison variance/percentile by cohort | near-term / capacity-allowing | (a) **API response shape:** `GET /compare?scenario_a=<id>&scenario_b=<id>` response body is extended with a `distribution` object for each compared indicator. The `distribution` object contains: `variance: float`, `p10: float`, `p50: float`, `p90: float`. Existing `delta` and `baseline` fields are unchanged — this is an additive extension only. `api_contracts.yml` is updated in the same commit. (b) **Backward compatibility:** Clients that do not read `distribution` are unaffected. The field is always present (not optional) when two valid scenario IDs are provided; values are `null` when the comparison window has fewer than 3 data points (non-meaningful distribution). (c) **Zone 1A variance band:** In Zone 1A, when the multi-entity or multi-branch comparison rendering is active (ADR-017 Phase 4 composite encoding, G1), the P10/P90 band for each compared indicator is available as a shaded band around the trajectory curve. The band is opt-in (toggled by a control, not visible by default) — Zone 1A at 1280×800 does not add visual complexity without user intent. (d) **Cohort distributional comparison:** The `distribution` object is also present in the cohort-level comparison response when cohort disaggregation data is available (requires G2 implementation). Cohort rows in Zone 1B comparison view display P10/P50/P90 for the bottom quintile threshold crossing step, labeled as "Distributional range across N scenarios." |

### 3.2 — Issues explicitly out of scope

| Issue / scope | Rationale for exclusion |
|---|---|
| Comparison group registry population (ADR-007 §Consequences step 2) | Required for Method A (Hierarchical Bayesian); G4 implements Methods E and B only. Registry structure may be scaffolded if time allows, but population is a data-architecture task separate from G4 engine implementation. |
| Method A (Hierarchical Bayesian) — #22 | Requires comparison group registry to be populated with ≥10 comparable countries per indicator. Population is not a G4 deliverable. Method A is post-G4 scope. |
| Full scenario banding display (P10/P50/P90 rendered in Zone 1A from synthetic inference) | Requires Method A and comparison group registry. Not Demo 6 critical — Demo 6 requires Structural Absence Declarations and MICE tier labels, not rendered posterior percentile bands. Deferred to M17 or later. |
| Anomaly detection (ADR-007 §Section 7) | Requires separate TSC sign-off — ADR-007 §Section 7 governance constraint 6. Permanently excluded from G4 and any routine milestone delivery until TSC approval is obtained. |
| MDA alert behavior under synthetic data (ADR-007 §Section 5 Tier 3/4 advisory alerts) | The advisory alert visual treatment (amber dashed indicator, "Cannot determine MDA status" blue marker) is a frontend component that requires per-indicator tier sub-label data from the engine. The G4 engine deliverable provides the data; the full advisory alert visual treatment is a separate frontend deliverable — it may be included in the G4 implementation PR if the frontend Architect Agent can deliver it within G4 scope, or carried to a subsequent sprint. |
| #102 multi-branch comparison (more than 2 scenarios) | `GET /compare` extension covers pairwise comparison. Multi-branch comparison (N > 2) is a separate API design decision. |
| #275 Mode 2 ecological control input (user-steerable coefficient) | G4 delivers backend transmission calculation with a fixed calibrated coefficient. Mode 2 steering interface for ecological coefficient is Mode 3-adjacent — out of G4 scope. |
| G2 (#986, #987, #1163) | G2 scope; fully separate sprint. |
| G3 (#274) | G3 scope; fully separate sprint. |
| G6 (#569) | Accessibility/performance validation; Wave 3 but separate sprint entry. |

**G4 is complete when:** All observable application states in Section 3.1 are confirmed in
the running ZMB and SEN scenarios at Step 4 Verify; the Ecological Economist DIC review on
#275 is on record; the Business PO confirms at Step 5 Validate that the G4 deliverables
either (a) improve Demo 6 scenario accuracy (SEN synthetic disclosure) or (b) improve the
comparison capability for Persona 2 (#102); and CI is green on `release/m16`.

Note: G4 does not gate G8 (live stakeholder demo #843). If G4 is not complete at G8 time,
Demo 6 proceeds with G3 data and G2 cohort disclosure without G4 synthetic flag wiring.
The sprint plan designates G4 as the first scope cut.

---

## Section 4 — ADR Prerequisite Summary

| Issue | ADR required | ADR status | Implementation may begin? |
|---|---|---|---|
| #22 (scoped) — Quantity schema + SyntheticDataEngine MVP | ADR-007 — ACCEPTED 2026-05-23; §2.2 coverage assessment COMPLETE | ACCEPTED — SUFFICIENT | After EL approves this entry, G2 is BPO-accepted, intent document is filed, and QA tests are authored |
| #102 — Comparison variance/percentile API | None — API extension within `/compare` endpoint pattern; Architect consultation: CLEAR | N/A | Same gate |
| #275 — Ecological-to-financial transmission | ADR-012 (External Sector Module, ARCH-006) — ACCEPTED 2026-06-05; #275 is within the ExternalSectorModule boundary | ACCEPTED | Same gate; Ecological Economist DIC review required before implementation PR merges |

**ARCH-012 disposition:** Not required. The §2.2 assessment confirms ADR-007 covers all
G4 deliverables on #22. No new ARCH entry will be filed for G4. If a future sprint delivers
Method A or full scenario banding display, a targeted ADR-007 amendment is the appropriate
mechanism (renewal trigger: "A sixth synthetic data method is proposed beyond the five
enumerated in Section 1" would not fire; but if the comparison group registry introduces a
new data governance pattern not covered by ADR-007 §Consequences, an amendment would be
warranted at that point).

---

## Section 5 — Near-Miss Sweep

**Near-miss sweep date:** 2026-06-23
**Sweep period:** M16 G3 sprint entry EL-approval (2026-06-23) through G4 sprint entry
filing (2026-06-23)

| Finding | Category | PI Agent register call issued? | NM entry number |
|---|---|---|---|
| No process gaps identified in the sweep period. G3 QA tests were refreshed (CM-updated) and G3 implementation committed on the feature branch. No SOP deviations occurred. The Wave 3 dependency (G4 waits for G2 BPO-acceptance) is a planned sequencing constraint, not a process gap. The §2.2 ADR-007 coverage assessment closes the CONDITIONAL gate from the sprint plan without triggering any renewal condition. | N/A | N/A | N/A |

*NM-056 follow-up (M16 exit condition 6 — no active soft-skip patterns): G4 test authorship
gate (§2.4) explicitly requires no `test.skip()` patterns. G4 implementation PR pre-push gates:
`cd backend && ruff check . && mypy app/` (mandatory for Python files per CLAUDE.md);
`cd frontend && npm run build` (mandatory if any `frontend/src/` files are modified).*

---

## EL Approval Record

**EL approval:** 2026-06-24

> G4 sprint entry approved. All gates confirmed clear: Wave 3 (G2 BPO-accepted 2026-06-24),
> intent document filed 2026-06-24, QA tests authored 2026-06-24, ADR-007 coverage confirmed
> sufficient (ARCH-012 not required). Implementation PR may open immediately. EE-PENDING ACs
> (AC-EE-1, AC-EE-2) remain deferred until Ecological Economist DIC review on #275 is on record.
> — @PublicEnemage (2026-06-24)
