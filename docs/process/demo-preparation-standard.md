# Demo Preparation Standard

**Established:** 2026-05-18
**Last revised:** 2026-06-10 (M12 — Step 4 UI architecture rules: no-drawer Zone 1, app-ready sentinel, Mode 3 slider pattern, API scenario creation; Step 5d: Mode 3 branch configuration evaluation; Step 3: ExternalSector reserve invariant mandatory disclosure; NM-039)
**Cadence:** Every two milestones (M6, M8, M10, M12...)
**Reference cases:** Issue #220 (M6), Issue #333 (M8), Issue #261 (M10), Issue #755 (M12)

---

## The Cadence

WorldSim runs a stakeholder demo review every two milestones. The demo
serves two purposes simultaneously:

1. **External validation:** The Independent Review Agent (fresh Claude
   instance, no institutional memory) evaluates the live application as
   a domain expert stakeholder would. It finds what development sessions
   accumulate sunk-cost blindness to.

2. **Milestone artifact:** The review output and screenshots are the
   permanent record of what the tool could do at this milestone.
   Methodologically honest — both what works and what does not.

---

## Folder Structure

All demo artifacts are milestone-versioned. Nothing is overwritten in place.

```
docs/demo/
  m{N}/
    stakeholder-walkthrough.md     — presenter script for this milestone
    screenshot-brief.md            — UX Agent frame brief
    screenshots/
      frame-a-<label>.png
      frame-b-<label>.png
      frame-c-<label>.png          ← thesis frame
      frame-d-<label>.png
      frame-e-<label>.png
    reviews/
      YYYY-MM-DD-v{version}-stakeholder-review.md   ← canonical Step 7 review
      YYYY-MM-DD-v{version}-pre-gate-triage.md      ← optional; pre-gate only
  stakeholder-walkthrough.md       — current version (updated each demo cycle)
```

**Naming rule — mandatory pre-creation check:**
Before saving any review document, run:
```bash
find docs/demo/ -name "*stakeholder-review*"
```
Confirm the new filename matches the pattern `YYYY-MM-DD-v{version}-stakeholder-review.md`
exactly — same prefix, same separator style, same suffix. The M8 file
(`2026-05-18-v0.8.0-stakeholder-review.md`) is the canonical reference instance.

**Pre-gate triage reviews** (conducted before screenshots are captured) are a distinct
artifact from the canonical Step 7 review. If a pre-gate triage IR is run, save it as
`YYYY-MM-DD-v{version}-pre-gate-triage.md` in the same `reviews/` folder. Add a header
note identifying it as pre-gate. The canonical Step 7 review must still be conducted
separately (with screenshots) and saved under the `*-stakeholder-review.md` name. Do not
use a descriptive suffix (e.g. `demo3-screenshot-ir`, `demo3-ir`) in place of the
canonical name — the suffix is always `-stakeholder-review.md` for Step 7 and
`-pre-gate-triage.md` for pre-gate work. NM-031 documents the M10 deviation.

Playwright specs are similarly versioned:

```
frontend/tests/e2e/
  demo-narrated.spec.ts            — current milestone
  demo-narrated-m{N-2}.spec.ts     — previous milestone archive
```

Scripts are NOT milestone-versioned — `scripts/demo.sh` and `scripts/speak.sh`
are updated in place. They are operational tools, not artifacts.

---

## Three-Tier Review Structure (M10 forward)

Every demo cycle passes through three review tiers in sequence. No tier may be skipped.

| Tier | Step | Who | Gate |
|---|---|---|---|
| Self-check | 5a / 5b / 5c | Acting agent | Narration instrument check + Playwright legibility + NARRATION-RULING-1 all pass |
| **Internal team review** | **6b** | **Nine-agent panel (PM Agent orchestrates)** | **All CRITICAL findings resolved + filed; all HIGH findings filed — before Step 7** |
| Independent review | 7 | Fresh Claude instance (IR Agent) | All CRITICAL and HIGH findings from IR filed as GitHub issues — before Step 9 |

The tiers are sequential and non-negotiable. The IR Agent (Step 7) must not be activated until the Step 6b gate is satisfied. The stakeholder session (Step 9) must not occur until the Step 8 gate is satisfied.

---

## Preparation Steps — In Order

### Step 1 — File the demo preparation issue

File a GitHub issue titled `demo: M{N} stakeholder demo preparation — v0.{N}.0 / Milestone {N}`.
Assign to current milestone. Label: `documentation,horizon:immediate`.
Body must include: what is new at this milestone vs the previous demo, the primary demo argument,
and the preparation checklist. Reference: M6 Issue #220, M8 Issue #333.

### Step 2 — UX Agent screenshot brief

Activate UX Designer Agent (fresh session). Provide: current milestone state, scenario details
(step count, live axes, null axes, key frames). Ask for five frames, zone requirements, captions,
sequence, and thesis frame identification.

Save output to `docs/demo/m{N}/screenshot-brief.md`. This is a permanent artifact — do not discard.

### Step 3 — Update `scripts/demo.sh` presenter guide

Update the presenter guide section of `demo.sh` to reflect current milestone state: which axes
are live, which are null, what the honest disclosures are, what the roadmap section says.

Do NOT update the North Star closing. It does not change.
Do NOT update the backtesting credibility section unless new cases were added.

**ExternalSector + Mode 3 reserve invariant — mandatory disclosure (M12 forward):**
If the demo scenario uses `ExternalSectorModule` (ADR-012) and Mode 3 Active Control
simultaneously, the honest disclosures section of `demo.sh` MUST include the following caveat:

> *Reserve depletion is identical in the baseline and the Mode 3 branch. Better conditionality
> terms improve GDP and unemployment trajectories. They do not change the entity's structural
> import dependency during the external shock. State this explicitly when presenting the
> Mode 3 comparison — the reserve crisis is survived under better conditions, not avoided.*

This is not optional context — it is the honest answer to what Mode 3 can and cannot change.
The reserve drawdown curve is driven by `ExternalSectorModule` independently of fiscal policy;
Mode 3 operates only on the fiscal channel. Omitting this caveat allows a stakeholder to
incorrectly conclude that better conditionality terms resolve the reserve crisis.
Documented in Mode 3 scenario evaluation panel deliberation (M12, 2026-06-10).

### Step 4 — Archive and update the narrated Playwright spec

```bash
cp frontend/tests/e2e/demo-narrated.spec.ts \
   frontend/tests/e2e/demo-narrated-m{N-2}.spec.ts
```

Update `demo-narrated.spec.ts` for the current milestone:

- Scenario step count (`n_steps`)
- Key frame capture points (per UX Agent brief)
- Narration strings for new features (ecological axis, governance null, PMM widget state)
- Screenshot output paths pointing to `docs/demo/m{N}/screenshots/`
- **Capture viewport — mandatory:** At the top of the test body, add `await page.setViewportSize({ width: 1440, height: 900 })` before `page.goto()`. Do NOT rely on the `playwright.config.ts` default (1280×720). The capture viewport must match the legibility gate (1440×900) and the presenter display. Root cause of NM-032 (DEMO-020 invisible to review chain at 1280×720). Issue #675.

**App-ready sentinel — mandatory (NM-039):**
The first `await` after `page.goto("/")` must wait for the application shell to be interactive.
Use exactly this pattern:

```typescript
await page.waitForFunction(
  () => typeof (window as Record<string, unknown>).__worldsim_selectEntity === "function",
  { timeout: 15_000 },
);
```

Do NOT wait for a map container testid (`worldsim-map`, `zone-1a-trajectory-container`, etc.).
The choropleth testid changes with UI revisions; `zone-1a-trajectory-container` is only present
after scenario selection, not on initial load. The `__worldsim_selectEntity` function is stable
across milestone UI changes — it is also the sentinel used by `demo-legibility.spec.ts` and
`demo-advancement-flow.spec.ts`. Before writing the sentinel, check what those two files use.
Root cause: NM-039.

**Zone 1 always-visible UI — no-drawer pattern (M10 forward):**
From M10 onward, Zone 1 instruments (`zone-1a-trajectory-container`, `zone-1b-mda-alerts`,
`zone-1c-pmm`, `zone-1d-four-framework`) are in the main viewport at all times. Do NOT:

- Call `window.__worldsim_selectEntity(entityId)` to open a drawer for instrument access
- Wait for `getByLabel("Close drawer")` or click it
- Use tab buttons inside a drawer to switch framework views

Screenshots are taken of the full viewport — the instrument cluster is always visible.
The M8 drawer-based pattern (`__worldsim_selectEntity` → drawer opens → tab switch → screenshot → close drawer) is archived in `demo-narrated-m8.spec.ts` and must not be replicated.

**Mode 3 React controlled input — slider pattern:**
The `fiscal-multiplier-slider` (and any similar React controlled input) cannot be set with
`fill()` or direct `el.value = "..."`. React intercepts the DOM property write and does not
fire the synthetic change event. Use the native input setter pattern:

```typescript
await page.locator('[data-testid="fiscal-multiplier-slider"]').evaluate(
  (el, value) => {
    const slider = el as HTMLInputElement;
    const nativeInputValueSetter = Object.getOwnPropertyDescriptor(
      window.HTMLInputElement.prototype,
      "value",
    )?.set;
    nativeInputValueSetter?.call(slider, value);
    slider.dispatchEvent(new Event("input", { bubbles: true }));
  },
  "1.30",
);
```

Wait for `[data-testid="recompute-badge"]` to disappear and `[data-testid="branch-anchor-label"]`
to appear before taking the Mode 3 screenshot — the branch trajectory computation is async.

**API scenario creation for complex scenarios:**
When the demo scenario requires `commodity_price_shocks`, `governance` module seeds, or
multi-entity initial attributes, create the scenario via `page.request.post()` before opening
the Scenarios panel — do not use the form UI (`.scenario-btn--create`). The form UI supports
only the basic configuration. The narrated spec creates the scenario via API, then selects it
from the panel. The `beforeAll` cleanup deletes stale runs from previous executions by matching
on the scenario name prefix.

**Frame E placement — at the divergence peak step, not the branch application step:**
For Mode 3 demos, the final frame must be captured at the step where the branch/baseline
divergence peaks, not at the step where Mode 3 was applied. For the Jordan/Egypt Hormuz
fixture, Mode 3 is applied at step 3 but the divergence peaks at step 5 (austerity removal
lag). Always advance to the peak divergence step before capturing the Mode 3 comparison frame.
The screenshot brief specifies this step — follow it explicitly.

### Step 5 — Update `docs/demo/stakeholder-walkthrough.md`

Copy current version to `docs/demo/m{N-2}/stakeholder-walkthrough.md` (archive).
Update the current version for this milestone:

- Section 2 (Live Application): reflect current axis state
- Section 4 (Roadmap): past-tense completed milestones, next milestone description
- Honest Disclosure section: current null/deferred items

Do NOT change Section 3 (Backtesting Credibility) or Section 5 (North Star).

### Step 5a — Narration instrument check (M10 forward — UX-RULING-4)

Before screenshots are captured, review the presenter script and any narration in
`scripts/demo.sh` for the following violation:

> Any sentence that routes the audience to the choropleth for quantitative step-to-step
> change (e.g. "watch [entity] shift in the choropleth") is incorrect per UX-RULING-4.

The choropleth is a navigable context surface — it provides geographic anchoring, not
quantitative signal. Quantitative change narration must route to Zone 1A (trajectory
curves) or Zone 1D (composite score readout).

**Correction template:**
- Remove: "Watch [entity] shift in the choropleth as [event] accumulates"
- Replace: "Watch the trajectory curves — [framework] composite score [direction] through steps [N]–[N+1]"
- Choropleth narration scope: "The choropleth anchors us — we are looking at [entity], a single country in the global distribution"

This check closes Issue #628 for each demo cycle. It recurs each milestone until
Option B (scenario-relative color scale) is implemented in M11, after which the
choropleth will visually corroborate Zone 1A and the narration restriction lifts.

### Step 5b — Legibility validation at 1440×900 (M10 forward — Issue #377)

Before capturing screenshots, run the legibility E2E suite at 1440×900:

```bash
cd frontend
npx playwright test tests/e2e/demo-legibility.spec.ts --project=chromium
npx playwright test tests/e2e/demo-advancement-flow.spec.ts --project=chromium
```

All tests must pass before screenshots are captured. A legibility failure means a
frame will be illegible in the review — the same defect class as DEMO-002, DEMO-003,
DEMO-005. Fix the failing assertion before proceeding to Step 6.

### Step 5c — Narration structure self-check (M10 forward — NARRATION-RULING-1)

Before the Independent Review Agent sees the script, apply a self-check to every
live-application step in Section 2 of `docs/demo/stakeholder-walkthrough.md`.
For each step, verify all three of:

- [ ] **Umbrella present.** One to two sentences orient the audience before any
  instrument reading is stated. The step does not open with a fact.
- [ ] **Synthesis present.** After the instrument output, one to two sentences
  draw the implication for the decision context (negotiating room, ministry brief,
  policy headroom).
- [ ] **Transitions present where required.** If the step's argument depends on
  the prior step's finding, a connective sentence bridges them. Steps in a causal
  chain are not self-contained.

Authority: NARRATION-RULING-1 (`docs/ux/standards.md §16`).

This check gates against the class of defect documented in Issue #652: narration
that presents instrument output without framing or implication, introducing
presenter-skill dependency for the "so what" the audience needs.

### Step 5d — Mode 3 branch configuration evaluation (M12 forward — when Mode 3 is used)

**Applies when:** the demo includes Mode 3 Active Control for the first time, or when the
demo scenario fixture changes between milestones and the branch configuration has not been
re-validated against live simulation output.

**Does NOT apply when:** Mode 3 fixture and branch parameters are unchanged from the
previous demo cycle and no engine changes affect fiscal transmission coefficients.

**Evaluation protocol:**

1. Identify the candidate branch configurations: at minimum, the current fixture (baseline)
   plus any plausible alternatives (different branch step, multiplier, GCC magnitude, or
   austerity severity).
2. Run each configuration as a live simulation — observe step-level GDP, unemployment, and
   reserve output from the API, not estimated from model formulae.
3. Document observed step-level output for each option in a deliberation file under
   `docs/demo/m{N}/reviews/scenario-evaluation-mode3-deliberation.md`.
4. Two-agent panel: Development Economist Agent + Chief Methodologist Agent. Both must agree
   on the recommendation before the branch configuration is locked. File the recommendation
   as `docs/demo/m{N}/reviews/scenario-evaluation-mode3-recommendation.md`.

**What the panel must explicitly address:**

- Which step shows the maximum divergence between baseline and branch trajectories in
  Zone 1A? (This is the step for Frame E.)
- Is the reserve depletion curve affected by the branch, or is it driven by ExternalSectorModule
  independently of fiscal policy? (If the latter, the mandatory disclosure from Step 3 applies.)
- Is the branch scenario narratively coherent? A branch that removes the IMF entirely (by
  branching before IMF entry) is a different scenario than "negotiate better conditionality terms."
  The counterfactual must match what a finance minister can actually argue at the table.
- Are the observed GDP and unemployment changes consistent with the engine's documented
  fiscal transmission coefficients? If not, the discrepancy must be explained before proceeding.

**The key rule:** evaluate against live simulation output, not model assumption estimates.
The M12 Mode 3 evaluation ran four option variants (A/B/D/E) against the live database before
recommending the current fixture. The panel's deliberation file shows that Option B (higher GCC
value) tested a different scenario than the 1.30× multiplier — a distinction invisible without
running both. See `docs/demo/m12/reviews/scenario-evaluation-mode3-deliberation.md` as the
canonical reference for this step.

### Step 6 — Run the demo and capture screenshots

**Pre-capture gate — viewport confirmation (M10 forward — Issue #675):**
Before running, confirm that `demo-narrated.spec.ts` contains `page.setViewportSize({ width: 1440, height: 900 })` before the first `page.goto()`. If absent, add it (Step 4 requirement). Capturing at 1280×720 (the playwright.config.ts default) means the review chain sees a rendering the stakeholder will not — viewport-dependent defects are invisible. This gate exists because NM-032 was not caught by either the internal panel or the IR Agent because of this mismatch.

```bash
./scripts/demo.sh          # Start stack, run migrations, seed data
./scripts/demo.sh --run    # Launch Playwright walkthrough (captures screenshots)
```

Screenshots land in `docs/demo/m{N}/screenshots/`. Verify five frames match the UX Agent brief.

**Screenshot naming requirement (M10 forward — DEMO-008 / Issue #349):**
Screenshots must be named in presentation order, not capture order. If the UX Agent
brief specifies a sequence (e.g. C → A → B → D → E), the filenames must reflect
that sequence:

```
frame-01-thesis.png        ← presentation order 1 (may be capture frame C)
frame-02-instrument.png    ← presentation order 2
frame-03-step1.png         ← presentation order 3
...
```

Alternatively, include a `SEQUENCE.md` in `docs/demo/m{N}/screenshots/` that maps
capture names to presentation order explicitly. Either convention is acceptable;
capture-order-only filenames are not.

### Step 6b — Internal Team Review (M10 forward — Issue #663)

Activate the nine-agent panel before the Independent Review Agent sees any screenshots.
Each agent reviews the captured screenshots and the narration script independently against
their defined lens. This is not a cross-agent discussion — findings are produced in parallel,
then aggregated by PM Agent.

**Activation:** PM Agent provides each agent with: (1) the screenshot set in UX Agent brief
presentation sequence, (2) `docs/demo/stakeholder-walkthrough.md`, and (3) their lens below.

**Panel and lenses:**

| Agent | Lens |
|---|---|
| Frontend Architect | Rendering fidelity, layout contract vs. spec (ADR-008/ADR-010), component behavior |
| UX Designer | Design system compliance, `docs/ux/standards.md` conformance, visual hierarchy |
| UX Design Thinking Agent | Mode-specific cognitive task alignment, instrument legibility, NARRATION-RULING-1 conformance |
| PO Agent | User story acceptance criteria alignment — does the demo deliver on the stated stories? |
| Customer Agent | Layer 3 usability — can the non-specialist user read this without specialist mediation? |
| QA Lead | Acceptance criteria coverage — does the demo surface what the test suite asserts? |
| Data Architect | Data fidelity — provenance indicators, synthetic flags, confidence tiers correctly displayed? |
| Chief Methodologist (DIC) | No False Precision — uncertainty signals, bands, tiers correctly surfaced? |
| Development Economist (DIC) | Human cost ledger — is human impact given equal visual weight to financial indicators? |

**Finding format (per agent):**

```
[DEMO-NNN]: [one-line title]
Severity: CRITICAL / HIGH / MEDIUM / LOW
Screenshot ref: [frame label or step number]
What is shown: [description]
What should be shown / what is missing: [description]
Recommendation: [specific actionable change]
```

**Finding numbering:** Internal review findings enter the `DEMO-NNN` namespace, continuing
from the last number used in the most recent milestone's IR review. PM Agent checks the
last assigned `DEMO-NNN` before beginning aggregation.

**Artifact format** (`YYYY-MM-DD-vX.X.X-internal-review.md` in `docs/demo/m{N}/reviews/`):
1. One section per agent — each agent's findings in the format above, unedited.
2. PM Agent consolidated summary table:
   `| Finding ID | Agent | Severity | One-line description | Status |`
3. Gate status declaration: which CRITICAL findings are resolved (with disposition), which
   HIGH findings are filed with GitHub issue numbers.

**CRITICAL finding resolution criteria** — one of the following must be true before Step 7:
- (a) A fix is committed and the PR is merged.
- (b) The finding is out of scope for this milestone — a rationale comment exists on the filed GitHub issue.
- (c) The EL explicitly accepts it as a known gap — an EL comment exists on the filed GitHub issue.
"Filed" without one of these three verdicts does not satisfy the gate.

**Gate:** All CRITICAL findings resolved (per criteria) and filed as GitHub issues before
Step 7. All HIGH findings filed as GitHub issues before Step 7. MEDIUM and LOW at PM Agent
discretion.

### Step 7 — Independent Review Agent

Activate a fresh Claude instance. Follow `docs/process/independent-review-prompt.md` exactly:

- Message 1: context setting (no screenshots yet)
- Message 2: attach screenshots in UX Agent brief sequence (C, A, B, D, E), ask four-part review task

The reviewer persona: senior policy analyst, 15 years fiscal adjustment experience, sat on both sides
of IMF negotiations. Permission to be direct and critical given explicitly before screenshots are shared.

### Step 8 — File and triage findings

File DEMO-NNN issues from review output. PM Agent TRIAGE mode on each finding.

**Tracking requirement (M10 forward — Issue #664 Gap 4):** File a GitHub issue for every
CRITICAL and HIGH finding before the stakeholder session (Step 9). The issue number must
appear in the review artifact summary table. MEDIUM and LOW findings are filed at PM Agent
discretion.

Fix CRITICAL items before the stakeholder session.
HIGH items: acknowledge honestly in narration if unfixed.
Save review document to `docs/demo/m{N}/reviews/YYYY-MM-DD-v{version}-stakeholder-review.md`.

### Step 9 — Stakeholder session

Use `docs/demo/m{N}/stakeholder-walkthrough.md` as the presenter script.
Use `scripts/speak.sh` if text-to-speech narration is needed.
Use `scripts/demo.sh` to start the stack before the audience arrives.

---

## What Does NOT Change Between Milestones

- North Star closing (the quinoa farmer paragraph) — permanent
- Backtesting credibility section — updated only when new cases are added
- Independent review prompt structure — the four-part task, the domain expert framing, the root cause analysis requirement
- Issue structure — always file a GitHub issue, always reference the previous milestone's issue

## What ALWAYS Changes Between Milestones

- Which axes are live vs null in the radar chart
- The honest disclosure section (current limitations)
- The roadmap section (past milestones to past tense, next milestone description)
- The Playwright spec (frame sequence, step count, narration strings)
- The screenshot brief (UX Agent re-activated fresh for each milestone)
- The Mode 3 branch configuration (step, multiplier, fixture) — re-validate via Step 5d
  whenever the demo scenario or engine fiscal transmission changes between cycles

---

## Reference Cases

| Milestone | Issue | Review |
|---|---|---|
| M6 | #220 | `docs/demo/m6/reviews/2026-05-07-v0.6.0-stakeholder-review.md` |
| M8 | #333 | `docs/demo/m8/reviews/2026-05-18-v0.8.0-stakeholder-review.md` |
| M10 | #261 | `docs/demo/m10/reviews/2026-06-02-v0.10.0-stakeholder-review.md` |
| M12 | #755 | `docs/demo/m12/reviews/` (IR review pending — M12 merged to main 2026-06-11) |
