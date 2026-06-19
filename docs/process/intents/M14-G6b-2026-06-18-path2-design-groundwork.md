---
name: M14-G6b-path2-design-groundwork
type: design-intent
issue: "#976"
sprint-plan: docs/process/sprint-plans/m14-sprint-plan.md
status: Filed
authored-by: PM Agent
authored-date: 2026-06-18
design-agents:
  - UX Designer Agent (artifact 1 — field mapping UX concept)
  - Architect Agent (artifact 2 — USER_SUPPLIED provenance type specification)
  - Data Architect Agent (artifact 3 — data isolation model sketch)
sprint-note: >
  Design-only group — no sprint entry document required; no implementation PR; no QA test
  authorship step. Three design artifacts gate M15 scoping and M16 implementation of Path 2.
  Artifacts filed in docs/design/path2-data-upload/ before M14 exit.
---

# Design Intent: M14-G6b — Path 2 Design Groundwork (Ministry-Owned Data Upload)

> **How to use this document:**
> This is a design-intent document, not an implementation-intent document. G6b produces
> three design artifacts, not application code. The adaptation from the standard intent
> template: §3 describes design artifact deliverable states (not running application
> states); §4 describes completion criteria reviewable by EL (not Playwright tests);
> §7 states that no QA test authorship step applies. All other sections follow the
> standard template. Authority: `docs/process/sprint-plans/m14-sprint-plan.md §G6b`.

---

## 1. Source

**Issue:** #976 — Path 2: Ministry-owned / proprietary data upload with field mapping and provenance isolation
**Journey reference:** Journey A, Step 2 — Gap GA-02 (`docs/ux/user-journeys.md §Journey A Step 2`)
**Status at authorship:** Issue #976 filed M14; implementation milestone M16+; G6b design work is M14 deliverable
**Authored by:** PM Agent
**Date:** 2026-06-18

**Design authority:**
- `docs/ux/user-journeys.md §Journey A Step 2` — GA-02 gap marker; four architecture prerequisites; 5-minute ceiling requirement; field mapping risk analysis; failure mode specification
- ADR-016 (ARCH-010) — existing `DataSourceObject` provenance type enumeration; Grounding Strip display contract; source object schema
- `docs/DATA_STANDARDS.md §Transformation Steps` — transformation audit trail standard that Path 2 uploads must satisfy
- Issue #53 — Information Access Architecture (RBAC prerequisite for data isolation)
- ADR-007 (ARCH-001) — synthetic data framework; tier hierarchy that `USER_SUPPLIED` type must slot into

**Producing agents (per `docs/process/sprint-plans/m14-sprint-plan.md §G6b`):**
- **Artifact 1:** UX Designer Agent — Field mapping UX concept
- **Artifact 2:** Architect Agent — `USER_SUPPLIED` provenance type specification (draft ADR-016 amendment)
- **Artifact 3:** Data Architect Agent — Data isolation model sketch

---

## 2. Persona Trace Elements Targeted

**P-1 — Persona served:**
Primary: Persona 2 — Finance Ministry Negotiator (Eleni Papadimitriou / Aicha Diallo archetype). She holds ministry-internal data — actual reserve position, bilateral lending terms, draft budget figures — that are more current and more accurate than publicly available versions. The simulation currently cannot incorporate this data. G6b designs the mechanism that will allow it.

Secondary: Persona 1 — IMF Programme Analyst (Lucas Ferreira archetype) and Persona 6 — Investigative Journalist. Both require reproducibility disclosure when a scenario cannot be replicated from public sources alone. The reproducibility caveat in the field mapping UX concept is their trust requirement.

**P-2 — Entry state:**
Preparatory. She is building the scenario before she walks into the negotiating room. Not under real-time pressure but has limited preparation time. The full Path 2 workflow — upload → map fields → confirm transformation → review provenance → create scenario — must complete within 5 minutes. This is the binding design constraint on Artifact 1.

**P-3 — Journey reference:**
Journey A Step 2 [Near-Term-Gap GA-02]: Starting conditions locked to preloaded data; no mechanism to supply ministry-owned or non-public initial state values. G6b produces the design prerequisites that will close this gap at M16+ implementation time.

**P-4 — Time/interaction ceiling:**
5 minutes: the full Path 2 workflow for a 10-variable spreadsheet dataset in a standard format, operated by a ministry analyst who is not a software engineer. This ceiling is the binding design constraint on Artifact 1 (field mapping UX concept). Any design that exceeds this ceiling will be rushed or skipped in the field.

**P-6 — Negotiating leverage delivered** *(design precondition, not yet delivered):*
After Path 2 is implemented (M16+), Persona 2 will be able to say: "The reserve coverage figure in this run is 2.8 months — that is our internal position as of this morning, not the IMF BoP vintage. That figure is ministry-supplied and is noted as such in the Grounding Strip." The G6b design artifacts make this argument architecturally possible. They do not deliver it — they gate the M15 scoping and M16 implementation that will.

**P-7 — North star capability delivered** *(design-level):*
After M14 G6b, the EL and M15 sprint team can open three design documents that specify without ambiguity: how the ministry uploads data (Artifact 1), what `USER_SUPPLIED` means in the provenance chain (Artifact 2), and what isolation guarantee the system must provide (Artifact 3). A sprint team reading these three artifacts in M15 can begin Path 2 scoping without redesign. The absence of these artifacts means M15 begins with open design questions that force implementation-time decisions — the pattern that produces scope creep and Layer 3 failures.

---

## 3. Design Artifact Deliverable State

> *Adapted from the observable application state section of the standard intent template.
> Since G6b produces design documents rather than running application changes, each
> deliverable state is a filed artifact with specific required content.*
>
> **The test for each statement:** Can the EL review and assess this artifact without
> reading any implementation code or asking the authoring agent for clarification?
> If no — the artifact is incomplete and must be revised before M14 exit.

### 3.1 Primary deliverable state

All three design artifacts exist as committed files at `docs/design/path2-data-upload/`:

1. `field-mapping-ux-concept.md` — UX Designer Agent
2. `user-supplied-provenance-spec.md` — Architect Agent
3. `data-isolation-model-sketch.md` — Data Architect Agent

Each artifact is self-contained: a reader who opens the file for the first time can understand what it specifies without consulting the authoring agent, reading ADR-016 source code, or referring to this intent document for clarification.

### 3.2 Required content per artifact

**Artifact 1 — Field mapping UX concept** (`field-mapping-ux-concept.md`)

A step-by-step upload workflow with timing annotations showing the full sequence — upload file → map fields → confirm transformation → review provenance display → create scenario — completing within 5 minutes for a 10-variable standard-format spreadsheet. Required elements:
- Every screen/modal/step named, with the analyst's visible information and available actions at each step
- The field mapping step shown explicitly: analyst's raw column name → WorldSim canonical variable → transformation applied (unit conversion, sign convention) → confirmation gate before proceeding
- Timing annotation per step; total ≤ 5 minutes for 10 variables
- Both field mapping failure modes addressed: (a) no canonical match found — what the analyst sees and what they can do; (b) ambiguous match — how disambiguation is presented
- Reproducibility caveat placement: "This scenario includes ministry-supplied starting values. Reproduction requires the uploaded dataset." — where it appears in the workflow and where it appears after scenario creation

**Artifact 2 — `USER_SUPPLIED` provenance type specification** (`user-supplied-provenance-spec.md`)

A draft amendment to ADR-016's provenance type enumeration adding `USER_SUPPLIED` as a fifth type alongside `OBSERVED | ESTIMATED_COMPARABLE | SYNTHETIC | STRUCTURAL_ABSENCE`. Required elements:
- Enum value name, display label (plain English, no jargon), and badge convention for Grounding Strip rendering
- Confidence tier assignment rules: `USER_SUPPLIED` is displayed as a distinct provenance class — not conflatable with institutionally-sourced T1, not treated as synthetic; the tier range and display contract specified
- Grounding Strip display example showing the full label format: "Reserve coverage: 2.8 months — Ministry of Finance (internal, 2026-06-15) · user-supplied"
- Position in the tier hierarchy: observed-public → user-supplied → synthetic → structural-absence (per `docs/ux/user-journeys.md §Journey A Step 2`)
- ADR-007 implication stated: the ADR-007 tier stack must be updated when Path 2 ships to reflect `USER_SUPPLIED`'s position above synthetic but below institutionally-observed
- Scope boundary stated: what ADR-016 elements are NOT changed by this amendment (Grounding Strip layout, data quality preview, entity scope decisions)

**Artifact 3 — Data isolation model sketch** (`data-isolation-model-sketch.md`)

A written specification of the data isolation guarantee that Issue #53's Information Access Architecture must provide before Path 2 can be implemented. Required elements:
- Isolation invariant: user-uploaded data is scoped to the uploading user's or institution's scenarios; it does not contaminate the shared `source_registry`; it does not appear in other users' data quality previews
- Three failure modes of insufficient isolation named: (a) uploaded data visible in other users' data quality previews, (b) uploaded data added to the shared source registry and treated as a platform-wide source, (c) uploaded data appearing in exports without the `USER_SUPPLIED` tag
- What Issue #53 must resolve (specifically) for Path 2 to proceed: the isolation boundary, the tenancy model (per-user vs. per-institution), and the access control check at the data quality preview API endpoint
- What Issue #53 is NOT required to solve for Path 2 — preventing scope creep: output visibility tiers for different roles, federation-level access control, public API RBAC
- Database schema implication identified: user-uploaded data requires storage separate from `source_registry`; a `user_supplied_data` table or equivalent must be specified at M15/M16 design time (schema design is out of scope for this sketch)

### 3.3 Silent failure detection

For design artifacts, the silent failure mode is an artifact that exists as a file but does not satisfy its required content — appearing complete while leaving open design questions that will surface as implementation-time ambiguities. The distinguishing characteristic:

- **Artifact 1 silent failure:** A UX concept that describes the workflow in prose but does not show the field mapping step with column-name → canonical-variable → transformation explicitly, or omits timing annotations. A reader attempting to prototype this UI would need to ask the author for decisions not recorded in the document.
- **Artifact 2 silent failure:** A provenance spec that names `USER_SUPPLIED` but does not specify the Grounding Strip display format or confidence tier assignment rules. A backend engineer implementing the type would face undefined display behavior.
- **Artifact 3 silent failure:** A data isolation sketch that states the invariant but does not name the three failure modes or the specific Issue #53 requirements. The Issue #53 design team would not know what the Path 2 prerequisite is.

EL review of AC-1 through AC-9 is the detection mechanism. An artifact that passes a cursory existence check but fails content review has not cleared its AC.

---

## 4. Acceptance Criteria

> *Each criterion is reviewable by the EL without reading any implementation code.
> An artifact that satisfies the AC can be assessed from the document alone.*

**AC-1:** `docs/design/path2-data-upload/field-mapping-ux-concept.md` exists as a committed file with a step-by-step upload workflow that includes timing annotations totaling ≤ 5 minutes for a 10-variable standard-format spreadsheet.

**AC-2:** The field mapping UX concept explicitly shows the field mapping step — analyst's column name → WorldSim canonical variable → transformation description → confirmation gate — in sufficient detail that a frontend engineer could prototype the UI without asking the author for clarification.

**AC-3:** The field mapping UX concept addresses both failure modes: (a) no canonical match for a column, and (b) ambiguous match with multiple candidate canonical variables. Each failure mode shows what the analyst sees and what action is available.

**AC-4:** The field mapping UX concept shows where the reproducibility caveat ("This scenario includes ministry-supplied starting values. Reproduction requires the uploaded dataset.") is displayed in the workflow and where it is carried after scenario creation.

**AC-5:** `docs/design/path2-data-upload/user-supplied-provenance-spec.md` exists as a committed file and defines `USER_SUPPLIED` with: a plain-English display label, a Grounding Strip display example in the format "Reserve coverage: 2.8 months — Ministry of Finance (internal, 2026-06-15) · user-supplied," confidence tier assignment rules, and placement in the tier hierarchy (observed-public → user-supplied → synthetic → structural-absence).

**AC-6:** The provenance type specification states the ADR-007 implication (tier stack update required when Path 2 ships) and states what ADR-016 elements are NOT changed by this amendment.

**AC-7:** `docs/design/path2-data-upload/data-isolation-model-sketch.md` exists as a committed file and states: (a) the isolation invariant, (b) the three failure modes of insufficient isolation, and (c) what Issue #53 must resolve for Path 2 to proceed.

**AC-8:** The data isolation model sketch states what Issue #53 is NOT required to solve for Path 2, preventing scope creep on Issue #53's design.

**AC-9:** All three artifacts are committed to `docs/design/path2-data-upload/` before the M14 sprint exit gate is confirmed by PI Agent.

---

## 4b. Visual Spec (before/after)

**AC-2 (before) — field mapping step: current absent state:**
```
Scenario creation form (current):

  Entity:          [Greece ▾]          ← hardcoded before G1; entity selector after G1
  Steps:           [8]
  Fiscal mult.:    [1.30]
  Political econ:  [☑ enabled]

  [Create Scenario]

No "Upload data" affordance. No "Supply starting values" option.
Ministry analyst has no mechanism to inject internal reserve position,
bilateral lending terms, or draft budget figures.
```

**AC-2 (after) — field mapping step: intended design specification:**
```
Path 2 upload flow — Step 2 of 4: Map Your Data (target: ≤ 90 seconds for 10 vars)

Your column                WorldSim variable           Transformation
──────────────────────────────────────────────────────────────────────────────
"FX reserves (USD bn)"  →  reserve_coverage_months     4.20 bn ÷ import rate
                                                        (1.50 bn USD/month)
                                                        = 2.80 months

"Budget deficit % GDP"  →  fiscal_balance_pct_gdp      Sign convention: deficit
                                                        entered as positive 3.2;
                                                        stored as -3.2

"Unemployment rate"     →  [No match found]             [Select variable ▾] or
                                                        [Skip this column]

[← Back]  [Confirm mapping and continue →]
```

**AC-5 (after) — `USER_SUPPLIED` Grounding Strip display format:**
```
Grounding Strip (Zone 0) — after Path 2 scenario creation:

  Financial framework                                     [2 user-supplied · 2 observed]
  ├── Reserve coverage: 2.8 months — Ministry of Finance (internal, 2026-06-18) · user-supplied
  ├── External debt: 47.2% GDP — IMF DSA 2024-Q1 · T2 · observed
  ├── Fiscal balance: −3.2% GDP — Ministry of Finance (draft budget, 2026-06-18) · user-supplied
  └── Current account: −5.1% GDP — World Bank WDI 2023 · T2 · observed

  ⚠  This scenario includes ministry-supplied starting values.
     Reproduction requires the uploaded dataset. [Learn more]
```

---

## 5. Kryptonite Constraint Check

**Artifact 1 — Field mapping UX concept:**

Does the field mapping workflow require specialist mediation for Persona 2 to complete the upload within the Preparatory entry state ceiling (5 minutes)?

`[ ]` No — the full workflow (upload → map fields → confirm → create) can be completed in under 5 minutes by a ministry analyst who is not a software engineer, using a standard spreadsheet format, without a data scientist or IT specialist.

`[ ]` Yes — [if the design requires specialist mediation, the UX concept is incomplete; UX Designer Agent must revise until the 5-minute ceiling is achievable without specialist assistance, or document the unavoidable constraint and escalate to EL for a scope decision].

**Kryptonite application to Artifact 2:**
The `USER_SUPPLIED` display label in the Grounding Strip must be interpretable by Persona 2 without a glossary. "user-supplied" is plain English and does not require mediation. If the specification proposes a technical label (e.g., `US_PROVENANCE`, `SELF_REPORTED`, `USER_DEFINED`), the Architect Agent must revise to plain-language display before filing.

**Kryptonite application to Artifact 3:**
The data isolation model sketch is an internal architecture document — it specifies what the platform must guarantee, not what the user sees. The kryptonite constraint does not apply to Artifact 3. Its audience is the Issue #53 design team and the M15 implementation sprint, not Persona 2.

---

## 6. Out of Scope

**Implementation code:** No code is produced in G6b. No backend tables, no API endpoints, no frontend components. The design artifacts describe what must be built; they do not build it.

**ADR authorship and panel review:** Artifact 2 is a draft ADR-016 amendment, not a new ADR and not a formal panel review. It does not pass through the ADR acceptance process in M14. That process is triggered at M15 or M16 when Path 2 implementation is scoped.

**Issue #53 resolution:** G6b specifies what Issue #53 must provide; it does not resolve it. Issue #53 scoping and implementation are M15 work.

**Path 1 (approved source query, Issue #975):** Path 1 implementation is M15 scope and is not addressed by G6b. G6b is Path 2 design only.

**Schema design:** Artifact 3 identifies that a `user_supplied_data` table or equivalent is required. Designing that schema is out of scope for M14; it is M15/M16 work gated on Issue #53 resolution.

**Path 2 implementation scoping decisions:** G6b does not determine which milestone Path 2 ships in beyond "M16+." That scoping decision is made in M15 after reviewing these design artifacts and the Issue #53 resolution state.

---

## 7. Test Authorship Obligation

**Design-only sprint — no QA test authorship step.**

G6b produces design artifacts, not implementation code. The verification mechanism is EL review of the three filed artifacts against AC-1 through AC-9 before M14 exit. No Playwright or pytest test can be authored for design documents — nor should one be; the artifacts are inputs to future implementation intent documents that will have their own QA test obligations.

**EL review gate:** Before M14 exit, EL reviews the three artifacts in `docs/design/path2-data-upload/` against AC-1 through AC-9. An artifact that fails an AC must be revised by the responsible authoring agent before the M14 exit gate passes.

**PI Agent confirmation:** PI Agent confirms that all three artifacts exist at the canonical filing location and that each AC is answerable from the artifact content alone — before the M14 sprint exit document is signed. An artifact that exists but leaves open design questions (see §3.3 Silent failure detection) has not cleared its AC.

---

*Design intent version: 2026-06-18. G6b is a design-only sprint group per
`docs/process/sprint-plans/m14-sprint-plan.md §Sprint Groups`. No sprint entry document
required; no implementation PR opens in M14. The three design artifacts produced here gate
M15 scoping and M16 implementation of Path 2. Authoring authority: PM Agent (this
document); UX Designer Agent (Artifact 1); Architect Agent (Artifact 2); Data Architect
Agent (Artifact 3). Review authority: EL before M14 exit.*
