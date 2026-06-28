---
name: m18-g2-sprint-exit
type: sprint-exit
milestone: M18 — Full Argument and Demo 7
sprint-group: G2 — PSP Driver Decomposition
status: Confirmed
authored-by: Business PO / PI Agent
date: 2026-06-28
pi-confirmed: true
release-branch: release/m18
sop-reference: docs/process/sprint-planning-sop.md §Sprint Exit Gate
---

# Sprint Exit — M18, G2: PSP Driver Decomposition

**Status:** Confirmed — all exit conditions satisfied
**Date produced:** 2026-06-28
**Release branch:** `release/m18`
**Sprint entry document:** `docs/process/sprint-plans/m18-g2-sprint-entry.md` — EL Approved 2026-06-26

*Authority: `docs/process/sprint-planning-sop.md §Sprint Exit Gate` (Phase D output).
G2 delivers PSP driver decomposition for Zone 1D (#1255): `psp-driver-row` renders the dominant
causal driver category ("Driver: fiscal sustainability" or governance / external balance / social
stability) alongside the PSP severity badge at every simulation step. Persona 3 (Andreas, Political
Advisor) can cite the driver in a verbal ministerial brief without any interaction beyond reading
Zone 1D.*

---

## Section 1 — Sprint Identification and Date

| Field | Value |
|---|---|
| Milestone | M18 — Full Argument and Demo 7 |
| Sprint group | G2 — PSP Driver Decomposition (Wave 1) |
| Release branch | `release/m18` |
| Sprint entry document | `docs/process/sprint-plans/m18-g2-sprint-entry.md` |
| Exit checklist issue | #1340 |
| Sprint journal issue | #1368 |
| Date implementation completed | 2026-06-28 (PR #1401 merged to `sprint/m18-g2`) |
| CI status on sprint branch | Green — test-backend PASS, lint PASS, compliance-scan PASS, playwright-e2e PASS; backtesting SKIPPED |

---

## Section 2 — Implementation Status

| Issue | PR | Merged? | CI status | Notes |
|---|---|---|---|---|
| #1255 — PSP driver decomposition (backend + frontend) | #1401 | ✅ Yes — 2026-06-28 | Green | `_attribute_dominant_driver()` helper; `psp_dominant_driver` in event metadata + QuantitySchema + API injection block; `psp-driver-row` in FourFrameworkZone1D; state threaded in ScenarioInstrumentCluster; schema docs updated |
| QA tests (authored before implementation — PR #1387) | #1387 | ✅ Yes — 2026-06-27 | Green | `backend/tests/test_m18_g2_psp_decomposition.py` (13 tests, 13 pass); `frontend/tests/e2e/m18-g2-psp-decomposition.spec.ts` (AC-1255-1 through AC-1255-7) |

**Implementation status:** #1255 delivered via PR #1401, merged 2026-06-28 to `sprint/m18-g2`.
All CI checks green. QA test files authored in PR #1387 before implementation began (entry document
requirement satisfied). 13/13 backend QA tests pass; E2E tests pass via Playwright CI.

**Files changed in PR #1401 (8 files):**
- `backend/app/simulation/modules/political_economy/module.py` — `_attribute_dominant_driver()` helper + `psp_dominant_driver` in `programme_survival_update` metadata
- `backend/app/api/scenarios.py` — injection block threading `psp_dominant_driver` from event metadata into `programme_survival_probability` QuantitySchema; TypeAlias fix for `CompositeStrategy`
- `backend/app/schemas.py` — `psp_dominant_driver: str | None = None` field on `QuantitySchema`
- `frontend/src/components/FourFrameworkZone1D.tsx` — `pspDominantDriver` prop, `DRIVER_LABELS` constant, `psp-driver-row` conditional render
- `frontend/src/components/ScenarioInstrumentCluster.tsx` — `pspDominantDriver` state, cast extension, PE-disabled reset, prop threaded to `<FourFrameworkZone1D>`
- `docs/schema/api_contracts.yml` — M18-G2 note on `programme_survival_probability` extension
- `docs/schema/simulation_state.yml` — PoliticalEconomyModule section documenting `psp_dominant_driver` in event metadata
- `backend/tests/test_m18_g2_psp_decomposition.py` — lint fixes (remove unused `import pytest`, shorten 3 E501 lines)

**Pre-push gate confirmation:** ruff clean (57 files), mypy clean (57 files), tsc clean,
vite build clean — all confirmed at push via pre-push hook (`.githooks/pre-push`).

**Step 4 Verify — implementation completeness checks:**

*Backend driver attribution:* `_attribute_dominant_driver()` in `module.py` computes per-step
causal attribution from `prior_events` using `LEGITIMACY_EROSION_ELASTICITY = 0.08` and
`EMERGENCY_EROSION_FACTOR = 0.10`. `FRAGILITY_AMPLIFIER = 1.5` applied when
`current_legitimacy < FRAGILITY_THRESHOLD (0.5)`. Tie-breaking priority:
governance > fiscal_sustainability > external_balance. Social stability fires when entity is
fragile with no other event contributions. `psp_dominant_driver` stored in
`programme_survival_update` event metadata alongside existing `legitimacy_input` and
`calibration_note` fields.

*API threading:* `scenarios.py` injection block (after note block, before cohort_crossings)
reads `programme_survival_update` from `events_snapshot` for `political_economy` framework,
extracts `psp_dominant_driver` from metadata, and injects into the existing
`programme_survival_probability` QuantitySchema via `model_copy(update={...})`. The field is
present only when the framework is `political_economy` and `programme_survival_probability`
is in indicators — it does not affect other frameworks.

*Frontend rendering:* `FourFrameworkZone1D.tsx` renders `<div data-testid="psp-driver-row">
Driver: {DRIVER_LABELS[pspDominantDriver]}</div>` between `psp-severity-row` and the
`{analogue && ...}` conditional. Silent null treatment: element is absent from DOM when
`pspDominantDriver` is null. `DRIVER_LABELS` mapping: `fiscal_sustainability → "fiscal
sustainability"`, `external_balance → "external balance"`, `governance → "governance"`,
`social_stability → "social stability"`. `ScenarioInstrumentCluster.tsx` sets
`pspDominantDriver` state from `entry.psp_dominant_driver ?? null`; resets to null when PE
is disabled.

*Schema contracts:* `QuantitySchema.psp_dominant_driver: str | None = None` (schemas.py:180).
`api_contracts.yml` note filed. `simulation_state.yml` PoliticalEconomyModule section added
documenting the event metadata field, enum values, tie-breaking priority, and frontend threading
path.

*13/13 backend QA tests pass:*
- AC-1255-B1: `programme_survival_update.metadata` contains `psp_dominant_driver` key
- AC-1255-B2: Senegal step-3 representative fixture → `fiscal_sustainability`
- AC-1255-B3: null driver when no prior events and legitimacy above threshold
- AC-1255-B4: all four driver categories + tiebreaker priority (governance > fiscal, fiscal > external)

*Regression guard:* No structural changes to Zone 1D DOM (no row removal, no position change
of existing elements). The `psp-driver-row` is inserted between `psp-severity-row` content and
`{analogue && ...}` conditional — the `psp-historical-analogue` element remains after the driver
row. Existing tests referencing `psp-historical-analogue` are not positional selectors; they
use `data-testid` selectors. No selector updates required.

---

## Section 3 — Business PO Acceptance Table

| Deliverable | Work type | Customer Agent Layer 3 assessment | Business PO verdict | Verdict artifact |
|---|---|---|---|---|
| #1255 — PSP driver decomposition (Zone 1D + PoliticalEconomyModule) | Frontend + Backend | PASS — see Layer 3 assessment below (Persona 3 + Persona 2) | **ACCEPT** 2026-06-28 | Section 3 below |

**Business PO acceptance status:** ACCEPT. No open rejections.

---

### Customer Agent Layer 3 Assessment

*G2 serves Persona 3 (Andreas Petrakis, Political Advisor) as primary and Persona 2
(Aicha Mbaye, Finance Ministry Negotiator) as secondary — Customer Agent Layer 3 is required
per CLAUDE.md §Entry and Exit Invariants. Assessment conducted prior to BPO verdict.
Session context: Same session as BPO verdict authorship — acknowledged.*

**Assessment method:** Kryptonite constraint check per `docs/process/agent-execution-lifecycle.md §Kryptonite Design Constraint`. Does the primary observable state require specialist mediation for the target persona to act on it within the P-4 time ceiling (90 seconds, Reactive)?

**#1255 — PSP driver decomposition (Persona 3 — Andreas Petrakis, Political Advisor):**

The primary observable state: in Zone 1D, below the PSP severity badge, a `psp-driver-row`
reads "Driver: fiscal sustainability" (or another category). Andreas reads this line and has the
causal sentence for a political brief — without opening Zone 2, without hovering, without any
interaction.

*Layer 3 check:* Does Andreas require specialist mediation to act on "Driver: fiscal sustainability"?
The label is plain-language political brief vocabulary. "Fiscal sustainability is the dominant
pressure on programme survival" is a sentence Andreas composes directly from the Zone 1D output —
it does not require a model expert to translate "0.XX probability" into a causal claim. The
driver categories (fiscal sustainability, external balance, governance, social stability) map
directly to the political risk vocabulary Andreas uses when briefing a minister. The label is
self-interpreting at the persona's domain level. No specialist mediation required within the
90-second Reactive ceiling.

*What changed from pre-G2 state:* Zone 1D previously showed PSP severity (CRITICAL / WARNING /
STABLE), PSP value (38%), direction (DECLINING), and historical analogue. The causal "why" was
absent from Zone 1D — Andreas would have needed to open Zone 2 or inspect the event log to
identify fiscal sustainability as the driver. After G2: the dominant driver is visible at L0 in
Zone 1D. The causal sentence is composable from Zone 1D alone.

**Layer 3 verdict — Persona 3 (Andreas): PASS.** Driver label is self-interpreting at political
advisor vocabulary level. Visible at L0, zero interaction required. Satisfies the P-4 time
ceiling (90 seconds, Reactive). No CA conditions.

**#1255 — PSP driver decomposition (Persona 2 — Aicha Mbaye, Finance Ministry Negotiator):**

Secondary persona. Aicha uses the PSP driver label to ground the causal argument when constructing
the L1 basis statement in the negotiating room: "The fiscal austerity package is the dominant
driver of the programme survival risk at this step — not an external shock or governance failure."
The driver label enables the causal framing distinction that matters in IMF negotiations (fiscal
adjustment vs. external balance vs. governance), without requiring Aicha to open Zone 2 or consult
the event log.

*Layer 3 check:* Does Aicha require specialist mediation to use "Driver: fiscal sustainability"
in a negotiating context? The driver categories correspond to the causal frameworks that IMF
conditionality discussions operate within. "Fiscal sustainability" maps directly to fiscal
adjustment measures; "external balance" maps to BOP adjustment; "governance" maps to
institutional compliance. Aicha reads the label and constructs the causal argument — no
economist translation required for the negotiation-room use case.

**Layer 3 verdict — Persona 2 (Aicha): PASS.** Driver label maps to IMF negotiation vocabulary.
No specialist mediation required. No CA conditions.

**Customer Agent Layer 3 summary: PASS for Persona 3 (primary) and Persona 2 (secondary).
No CA conditions raised. Layer 3 assessment filed before BPO verdict per acceptance-protocol.md §1.1.**

---

### BPO Verdict — #1255 PSP Driver Decomposition

*Assessed per acceptance-protocol.md §1.1 (Frontend Feature + Backend Extension).*

**Observable state confirmed:**

1. `FourFrameworkZone1D.tsx`: `psp-driver-row` renders between `psp-severity-row` content and
   `{analogue && ...}` conditional, gated on `pspDominantDriver != null && DRIVER_LABELS[pspDominantDriver]`.
   Font: `fontSize: 10, color: "#555"` — same visual weight as historical analogue row.
   Confirmed from `FourFrameworkZone1D.tsx`.

2. `ScenarioInstrumentCluster.tsx`: `pspDominantDriver` state (`useState<string | null>(null)`).
   Cast block reads `entry.psp_dominant_driver ?? null`. PE-disabled reset: `setPspDominantDriver(null)`.
   Prop `pspDominantDriver={pspDominantDriver}` passed to `<FourFrameworkZone1D>`.
   Confirmed from `ScenarioInstrumentCluster.tsx`.

3. Backend `_attribute_dominant_driver()`: `LEGITIMACY_EROSION_ELASTICITY = 0.08`,
   `EMERGENCY_EROSION_FACTOR = 0.10`, `FRAGILITY_AMPLIFIER = 1.5 when legitimacy < 0.5`.
   Tie-breaking: `max(priority, key=lambda cat: (contributions[cat], -priority.index(cat)))` —
   governance takes priority over fiscal_sustainability on equal contribution.
   Social stability fires only when total contributions == 0 and legitimacy < FRAGILITY_THRESHOLD.
   Confirmed from `module.py`.

4. Schema: `QuantitySchema.psp_dominant_driver: str | None = None` at `schemas.py:180`.
   API injection block in `scenarios.py` threading from event metadata into QuantitySchema.
   `api_contracts.yml` note filed. `simulation_state.yml` section added.

5. QA tests: 13/13 backend tests pass (`test_m18_g2_psp_decomposition.py`). E2E tests
   (AC-1255-1 through AC-1255-7) pass in CI playwright-e2e check on PR #1401.

6. Pre-push gates: ruff clean, mypy clean (57 files), tsc clean, vite build clean — all
   confirmed at push via pre-push hook.

**DEMO4 class check (dynamic output):** The `psp-driver-row` renders a value extracted from the
measurement-output API response — specifically `indicators.programme_survival_probability.psp_dominant_driver`.
This value is injected from the `programme_survival_update` event metadata at the step currently
being viewed. The E2E tests confirm the value updates when the step advances (AC-1255-3) and is
absent when the API response contains `psp_dominant_driver: null` (AC-1255-4). Neither test can
pass against a static default. DEMO4 check: PASS.

**Kryptonite check:** The driver label is plain-language political brief vocabulary. "Driver: fiscal
sustainability" requires no specialist translation for Persona 3 (political advisor briefing a
minister) or Persona 2 (finance ministry negotiator constructing a causal argument). The label is
visible at L0 in Zone 1D, zero interaction required, within the 90-second Reactive ceiling. PASS.

> VALIDATED — 2026-06-28. Frontend: Zone 1D `psp-driver-row` rendering `Driver: {category}`.
> Backend: `_attribute_dominant_driver()` in PoliticalEconomyModule; `psp_dominant_driver` in
> `programme_survival_update` metadata; API injection into `programme_survival_probability`
> QuantitySchema. DEMO4 check: AC-1255-3 (step-advance update) + AC-1255-4 (null driver absent
> from DOM) both assert against live injected values, not static defaults. E2E tests use
> `page.route()` mocks to control `psp_dominant_driver` value per test — correct isolation.
>
> Step 4 Verify source code checks: `psp-driver-row` between severity content and analogue at
> `FourFrameworkZone1D.tsx`; silent null gate: `pspDominantDriver != null && DRIVER_LABELS[...]`.
> `ScenarioInstrumentCluster.tsx`: cast reads `entry.psp_dominant_driver ?? null`; PE-disabled
> reset `setPspDominantDriver(null)`. `_attribute_dominant_driver()`: tiebreak priority =
> governance > fiscal_sustainability > external_balance; social_stability fires only when
> total contributions == 0 and legitimacy < 0.5. Schema contracts: `QuantitySchema`,
> `api_contracts.yml`, `simulation_state.yml` all updated in same PR.
>
> Analytical intent: Persona 3 (Andreas Petrakis, Political Advisor) reads Zone 1D and composes
> "Programme survival: WARNING — fiscal sustainability is the dominant pressure" without opening
> Zone 2. Persona 2 (Aicha Mbaye) uses the driver label for causal framing at the IMF negotiating
> table. Layer 3: PASS both personas. Kryptonite: PASS.
> Verdict: **ACCEPT**.

---

### North Star Test Artifact

*Required for user-facing deliverables per CLAUDE.md §North Star Test (Process Gate).
#1255 is a user-facing deliverable. Assessment authored by Business PO.*

**North star question:** Does this decision make the tool more useful to a finance minister
sitting across from an IMF negotiating team, in that moment?

**North star assessment:**

*Scenario:* Demo 7 Act 1 — Senegal Mode 3 active control session, Step 3. A Senegalese finance
ministry team includes Andreas (Political Advisor archetype) who must brief the minister before
the IMF negotiating session. Zone 1D is visible. The minister's team has 90 seconds to scan the
instrument cluster before the session resumes.

*Capability evaluated:* Zone 1D now shows — alongside the PSP severity badge ("WARNING, 52%,
DECLINING") — the line "Driver: fiscal sustainability". This line is visible at L0 with no
interaction.

*Before G2:* Zone 1D showed what the PSP is and when comparable programmes failed. The causal
"why" was absent from Zone 1D. Andreas would have to open Zone 2, read the event log, and
identify which events were driving legitimacy erosion — a 3–5 minute operation at best, not
available in the 90-second Reactive window. The political brief lacked a causal sentence grounded
in the simulation's per-step attribution.

*After G2:* Zone 1D shows what, when comparable programmes failed, AND why at this step. Andreas
reads: "Programme survival: WARNING (52%) — DECLINING. Driver: fiscal sustainability." He composes
the ministerial brief sentence: "Our fiscal austerity posture — not an external shock, not a
governance failure — is the dominant causal pressure on programme survival at step 3. The IMF
team is not seeing an uncontrollable external balance problem. They are seeing a fiscal choice."

*Does this change what the minister's team can argue at the table?* Yes, specifically. The
distinction between "fiscal sustainability driver" and "external balance driver" is the distinction
between a negotiable fiscal adjustment schedule and an exogenous shock argument. If the driver
is fiscal sustainability, the minister can argue that the conditionality pace is the variable —
not an external shock outside anyone's control. If the driver is external balance, the argument
shifts to requesting programme flexibility in response to external headwinds. The driver label
tells the minister's team which argument to make in the room.

Before G2, the minister's team lacked the per-step causal attribution to make this distinction
from Zone 1D. After G2, Andreas can read it in one glance and prepare the minister for the
"which argument" decision in the 90-second window before the session resumes.

**North star test verdict:** PASS — PSP driver decomposition directly enables the causal
argument distinction at the IMF negotiating table. Assessment is specific: names the Demo 7
Act 1 Senegal scenario (Step 3), the persona (Andreas, Political Advisor), the pre/post
capability state (no Zone 1D causal attribution vs. L0 driver label), and the argument structure
the driver label enables (fiscal choice vs. external shock distinction in IMF conditionality
negotiation). Not aspirational.

---

## Section 4 — Open Rejections

No open rejections. ACCEPT verdict recorded in Section 3. No REJECT verdicts issued.

**Near-miss entries required for each rejection:** N/A — no rejections in G2.

**NM-075 filed (process gap, not sprint rejection):** The concurrent Claude Code session
branch-switching that disrupted G2 implementation is documented as NM-075 (filed via
`chore/m18-state-sync-015`, PR #1406, merged 2026-06-28 to `release/m18`). NM-075 is a process
gap entry, not a sprint rejection artifact — the implementation ultimately succeeded and all
QA tests pass.

---

## Section 5 — PI Agent Sprint Exit Confirmation

**Exit conditions checklist (PI Agent):**

- [x] **All implementation groups merged; CI green on sprint branch (Section 2)**
  PR #1401 merged 2026-06-28 to `sprint/m18-g2`. All CI checks green: playwright-e2e PASS,
  lint PASS, test-backend PASS, compliance-scan PASS; backtesting SKIPPED. QA test file authored
  in PR #1387 before implementation began (entry requirement satisfied — NM-055 compliant).
  13/13 backend tests pass; E2E tests AC-1255-1 through AC-1255-7 all pass in CI.

- [x] **Business PO ACCEPT verdict filed for each user-facing deliverable (Section 3)**
  #1255 ACCEPT — verdict filed in Section 3 of this document, dated 2026-06-28.

- [x] **Customer Agent Layer 3 assessment on record for all Persona 2/3/5 deliverables (Section 3)**
  #1255 serves Persona 3 (Andreas Petrakis) as primary and Persona 2 (Aicha Mbaye) as secondary.
  Persona 3 Layer 3 PASS: driver label self-interpreting at political advisor vocabulary level,
  visible at L0 within 90-second Reactive ceiling. Persona 2 Layer 3 PASS: driver label maps to
  IMF negotiation causal framework vocabulary. Layer 3 filed before BPO verdict.

- [x] **No open rejection artifacts (Section 4)**
  No rejections in G2. Zero REJECT verdicts on record. NM-075 process gap filed separately.

- [x] **Near-miss entry filed for each rejection (Section 4)**
  N/A — no rejections. NM-075 filed for implementation process gap (not a sprint rejection).

- [x] **North star test artifact on record (Section 3)**
  Filed in Section 3 above. Specific: names Demo 7 Act 1 Senegal scenario (Step 3), Andreas
  persona (Political Advisor), pre/post capability state (no Zone 1D causal attribution vs. L0
  driver label), and the argument structure enabled (fiscal choice vs. external shock distinction
  in IMF conditionality negotiation). Not aspirational.

**PI Agent sprint exit verdict: CONFIRMED — all exit conditions satisfied**

**PI Agent confirmation:**

> G2 sprint exit conditions are satisfied as of 2026-06-28. #1255 (PSP driver decomposition —
> Zone 1D `psp-driver-row` + `PoliticalEconomyModule._attribute_dominant_driver()`) is delivered
> via PR #1401, merged 2026-06-28 to `sprint/m18-g2`. CI is green — playwright-e2e PASS
> confirmed at PR merge.
>
> Business PO ACCEPT verdict on record for #1255 (Section 3, dated 2026-06-28). Customer Agent
> Layer 3 assessments filed before verdict — Persona 3 (Andreas) PASS: driver label self-
> interpreting at political advisor vocabulary level, L0 visible. Persona 2 (Aicha) PASS: driver
> label maps to IMF negotiation causal framework vocabulary. No CA conditions raised.
>
> North star test artifact filed and specific: Demo 7 Act 1 Senegal Step 3; Andreas reads "Driver:
> fiscal sustainability" in Zone 1D at L0 within 90-second Reactive window; composes the
> "fiscal choice vs. external shock" argument for the IMF negotiating session without opening
> Zone 2. Passes the north star test: names the scenario, the persona, the pre/post capability
> delta, and the argument structure enabled at the table.
>
> Step 4 Verify source code checks recorded:
> - `_attribute_dominant_driver()`: `module.py` after `_compute_legitimacy_delta()`;
>   FRAGILITY_AMPLIFIER at legitimacy < 0.5; tiebreak priority governance > fiscal > external;
>   social_stability fires only when total contributions == 0 and fragile.
> - `psp_dominant_driver` in `programme_survival_update` metadata: `module.py:204`
>   (psp_dominant_driver = `_attribute_dominant_driver(prior_events, new_legitimacy)`)
> - API injection: `scenarios.py` — after note block, before cohort_crossings loop;
>   `model_copy(update={"psp_dominant_driver": _psp_driver})` on `programme_survival_probability`
> - `QuantitySchema.psp_dominant_driver: str | None = None` at `schemas.py:180`
> - `psp-driver-row` in `FourFrameworkZone1D.tsx` between severity content and analogue
> - `setPspDominantDriver` state in `ScenarioInstrumentCluster.tsx`; PE-disabled reset
> - Schema contracts: `api_contracts.yml` note + `simulation_state.yml` section
>
> NM-075 filed (process gap): concurrent Claude Code sessions sharing main working tree caused
> branch switches to overwrite in-progress G2 implementation multiple times. Root cause documented
> and process improvement proposed (git worktree per sprint group at sprint entry). Filed via
> PR #1406, merged 2026-06-28 to `release/m18`. Not a sprint rejection — implementation
> ultimately succeeded; QA tests all pass.
>
> No open REJECT verdicts. No open rejection artifacts.
>
> **G2 is CLOSED as of 2026-06-28.**
>
> — PI Agent, 2026-06-28

---

## Sprint Exit Artifact Statement

This document is the sprint exit artifact for M18-G2. It supersedes any informal exit notation
in `SESSION_STATE.md` for this sprint. It is filed at
`docs/process/sprint-plans/m18-g2-sprint-exit.md`.

The PI Agent confirmation in Section 5 is the gate. G2 is closed as of 2026-06-28.

**Downstream gates cleared by G2:** Integration PR `sprint/m18-g2` → `release/m18` may now be
opened. The PSP driver decomposition feature is available in `release/m18` for Demo 7 Act 1
integration testing after the integration PR merges.
