# Demo Preparation Standard

**Established:** 2026-05-18
**Last revised:** 2026-06-11 (M13 planning — Step 6c ordering corrected: 6b → 7 → 6c → 9; IR Agent is technical quality gate before persona panel; Step 6c north star gate now blocks Step 9 not Step 7; table and body reordered accordingly; Steps 7 and 6c require release→main merge as prerequisite)
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
    stakeholder-walkthrough.md           — presenter script for this milestone
    screenshot-brief.md                  — UX Agent frame brief
    screenshots/
      frame-a-<label>.png
      frame-b-<label>.png
      frame-c-<label>.png                ← thesis frame
      frame-d-<label>.png
      frame-e-<label>.png
    reviews/
      YYYY-MM-DD-v{version}-internal-review.md     ← Step 6b: nine-agent internal panel
      YYYY-MM-DD-v{version}-audience-simulation.md ← Step 6c: persona-based audience simulation
      YYYY-MM-DD-v{version}-ir-review.md           ← Step 7: IR Agent pre-demo quality gate
      PENDING-v{version}-stakeholder-review.md     ← placeholder created at milestone close
      YYYY-MM-DD-v{version}-stakeholder-review.md  ← Step 9: filled after live demo runs
      YYYY-MM-DD-v{version}-pre-gate-triage.md     ← optional; pre-gate only
  stakeholder-walkthrough.md             — current version (updated each demo cycle)
```

**Two distinct review artifacts — mandatory distinction (EL decision 2026-06-10):**

| Artifact | Filename | When created | Who authors |
|---|---|---|---|
| IR review | `YYYY-MM-DD-v{version}-ir-review.md` | Step 7 — after screenshots captured | Independent Review Agent (fresh Claude instance) |
| Stakeholder review | `YYYY-MM-DD-v{version}-stakeholder-review.md` | Step 9 — after live demo runs | Acting agent from session notes |

The IR review is a pre-demo quality gate conducted by a simulated domain expert. The stakeholder
review is a post-demo artifact capturing what real stakeholders said, asked, and identified.
These are not the same artifact and must not share a filename. A `PENDING-v{version}-stakeholder-review.md`
placeholder is created at milestone close (before the live demo runs) and renamed once the
demo is complete.

**Naming rule — IR review (Step 7):**
Before saving the IR review, run:
```bash
find docs/demo/ -name "*-ir-review*"
```
Confirm the new filename matches `YYYY-MM-DD-v{version}-ir-review.md`. The M12 file
(`2026-06-10-v0.12.0-ir-review.md`) is the canonical reference instance (first milestone
to use this naming).

**Naming rule — Stakeholder review (Step 9):**
Before saving the stakeholder review, run:
```bash
find docs/demo/ -name "*-stakeholder-review*"
```
Confirm the filename matches `YYYY-MM-DD-v{version}-stakeholder-review.md`. Prior to the
EL decision (M6, M8, M10), the IR Agent's output was saved under this name — those files
are historically named correctly for their milestone and must not be renamed. From M12
forward, `stakeholder-review.md` is post-live-demo only.

**Pre-gate triage reviews** (conducted before screenshots are captured) are a distinct
artifact from the Step 7 IR review. If a pre-gate triage IR is run, save it as
`YYYY-MM-DD-v{version}-pre-gate-triage.md` in the same `reviews/` folder. Add a header
note identifying it as pre-gate. NM-031 documents the M10 deviation.

Playwright specs are similarly versioned:

```
frontend/tests/e2e/
  demo-narrated.spec.ts            — current milestone
  demo-narrated-m{N-2}.spec.ts     — previous milestone archive
```

Scripts are NOT milestone-versioned — `scripts/demo.sh` and `scripts/speak.sh`
are updated in place. They are operational tools, not artifacts.

---

## Four-Tier Review Structure (M10 forward; Step 6c added M14 forward)

Every demo cycle passes through four review tiers in sequence. No tier may be skipped.

| Tier | Step | Who | Gate |
|---|---|---|---|
| Self-check | 5a / 5b / 5c | Acting agent | Narration instrument check + Playwright legibility + NARRATION-RULING-1 all pass |
| **Internal team review** | **6b** | **Nine-agent panel (PM Agent orchestrates)** | **All CRITICAL findings resolved + filed; all HIGH findings filed — before Step 7** |
| Independent review | 7 | Fresh Claude instance (IR Agent) | All CRITICAL and HIGH findings from IR filed as GitHub issues — before Step 6c |
| **Audience simulation** | **6c** | **Persona panel: Personas 1, 2, 5 (PM Agent orchestrates)** | **Persona 5 north star verdict PASS; all CRITICAL persona findings resolved — before Step 9** |

The tiers are sequential and non-negotiable. Step 7 must not be activated until the Step 6b gate is satisfied. Step 6c must not be activated until the Step 7 gate is satisfied. The stakeholder session (Step 9) must not occur until the Step 6c gate is satisfied.

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

**Syntax validation gate (mandatory — NM-041):**
After any edit to `scripts/demo.sh`, run:
```bash
bash -n scripts/demo.sh
```
The command must exit 0 before the file is committed. A syntax error in `demo.sh` makes the entire stack startup sequence inaccessible — the presenter guide, all timed narration cues, and the stack-ready confirmation all live inside this script. Root cause: M12 — a missing `)` closing a `$(bold ...)` command substitution on line 208 was undetected throughout M12 development and only surfaced when attempting to record the post-closure screen recording (PR #890, NM-041).

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

#### Solo-Use Gate (mandatory — #951)

The nine-agent Step 6b panel is composed of specialists with institutional memory of the
codebase. They will apply domain knowledge that real external participants lack, and
specialist familiarity can suppress findings that a non-specialist would immediately notice.
The solo-use gate closes this gap structurally.

**Requirement:** At least one Step 6b panel reviewer must evaluate the screenshots
*without reading the walkthrough first* — in the same condition as a real attendee who
arrives at the demo without advance preparation. This reviewer is the designated solo-use
reviewer. Their findings are tagged `[SOLO]` in the finding format.

**Designated solo-use reviewer:** **Customer Agent** (Layer 3 usability — non-specialist
user without specialist mediation). The Customer Agent is the designated solo-use reviewer
for every Step 6b panel. Their lens is: "Can a non-specialist user read this output and
understand what action it implies, without asking an economist to interpret it?"

**Protocol:**
1. PM Agent provides the Customer Agent with only the screenshots in UX Agent brief
   presentation sequence — no walkthrough, no framing context, no lens description beyond
   the solo-use question above.
2. The Customer Agent produces findings using the standard finding format, tagging each
   with `[SOLO]`.
3. After completing solo-use findings, the Customer Agent may receive the walkthrough and
   produce additional findings under their standard Layer 3 usability lens.

**Blocking criteria for `[SOLO]` findings:** A `[SOLO]`-tagged CRITICAL or HIGH finding
blocks Step 7 under the same three-condition criteria as all other Step 6b findings — the
finding must be (a) fixed and merged, (b) scoped out with a GitHub issue and EL rationale,
or (c) explicitly accepted by EL with a comment on the filed issue. The `[SOLO]` tag does
not reduce the severity or the blocking criteria — it identifies the reviewer context, not
a secondary track.

**Rationale:** DEMO4-001 (first instance of un-mediated non-specialist output surfacing to
real participants without a legibility check) was filed after the M12 demo cycle. The
solo-use gate is the structural countermeasure. It cannot be satisfied by a specialist
reviewer who applies domain knowledge before viewing the screenshots.

### Step 7 — Independent Review Agent

**Prerequisite — merge `release/m{N}` → `main` first.** Steps 7 and 6c are post-release-merge
quality gates. The IR Agent and persona panel must review the artifacts as they exist on `main`
— the branch that represents the shipped milestone state. The Engineering Lead performs the
admin merge (`release/m{N}` → `main`) before Step 7 is activated. Claude Code does not merge
release branches to main.

Activate a fresh Claude instance. Follow `docs/process/independent-review-prompt.md` exactly:

- Message 1: context setting (no screenshots yet)
- Message 2: attach screenshots in UX Agent brief sequence (C, A, B, D, E), ask four-part review task

The reviewer persona: senior policy analyst, 15 years fiscal adjustment experience, sat on both sides
of IMF negotiations. Permission to be direct and critical given explicitly before screenshots are shared.

---

### Step 6c — Audience Simulation Panel (M14 forward — Issue #865)

Activate a persona-based panel after the Step 7 (IR Agent) gate is cleared and before the
live stakeholder session. Each panel member is instantiated from their full profile in
`docs/ux/personas.md` and evaluates the screenshots and walkthrough **in-character** — not
as an internal quality reviewer, but as an audience member experiencing the demo for the
first time.

This step tests a different question from Step 7: not *does the demo have technical defects?*
but *does the presentation arc hold up under the challenges this specific audience would pose?*
The IR Agent finds what slipped through the internal team. The persona panel evaluates whether
the technically correct demo lands with the actual audience. Running persona panel after IR
ensures the panel evaluates the post-fix, technically validated state.

**Panel composition:**

| Persona | Who | In-character question |
|---|---|---|
| **Persona 1 — Programme Analyst** | Lucas Ferreira, IMF Country Economist | "Does this output carry what I need to defend it in an IMF review board?" |
| **Persona 2 — Ministry Negotiator** | Eleni Papadimitriou, Deputy Director, Hellenic Ministry of Finance | "Can I retrieve a specific threshold crossing in under 90 seconds in the room?" |
| **Persona 5 — Institutional Decision-Maker** | Aicha Mbaye, Finance Minister, Senegal | "Does this change my position? Can I state the key finding without asking an economist?" |

**When to add Persona 3:** Add Andreas Stefanidis (Political Advisor) when the demo features
governance or political economy outputs — specifically when the political feasibility module
or social dynamics indicators are in scope. Andreas tests whether the governance signal
is translatable into a political brief without economist mediation.

**Activation:** PM Agent instantiates each persona agent with: (1) the persona's full profile
from `docs/ux/personas.md` — identity, entry state, trust threshold, failure mode, preferred
information format; (2) screenshots in UX Agent brief presentation sequence; (3)
`docs/demo/stakeholder-walkthrough.md`. Each persona agent responds in-character. Findings are
produced independently, then aggregated by PM Agent — this is not a cross-agent discussion.

**Finding format (per persona):**

```
[DEMO-NNN]: [one-line title]
Severity: CRITICAL / HIGH / MEDIUM / LOW
Persona: [number and name]
In-character observation: [what this persona would think or say at this moment in the demo]
Presenter preparation: [the question the presenter must be able to answer]
Recommendation: [specific artifact change — or "Presenter prep only" if no change needed]
```

**Finding numbering:** Persona simulation findings continue the `DEMO-NNN` namespace from
the last number assigned in Step 7. PM Agent checks the last assigned number before
beginning aggregation.

**Severity calibration for persona findings:**

| Severity | Meaning |
|---|---|
| CRITICAL | A failure that, in-character, causes this persona to close the tool or dismiss the demo (trust threshold breached or failure mode triggered per `docs/ux/personas.md`) |
| HIGH | A question the presenter cannot currently answer, or a navigation path the persona cannot complete within their stated time window |
| MEDIUM | An observation that degrades comprehension but does not trigger a failure mode |
| LOW | A preference or style note that does not affect the persona's ability to use the output |

**North star gate — Persona 5 (mandatory):**
At the end of Aicha Mbaye's section, the persona agent must produce a mandatory north star verdict:

```
North star verdict: PASS / FAIL
Primary finding sentence: "[The single sentence Aicha would take away from this demo,
  stated without specialist mediation — or CANNOT BE STATED if she cannot articulate it]"
Gate: Step 9 MAY PROCEED / BLOCKED — [reason if blocked]
```

The Persona 5 north star verdict gates Step 9. If Aicha cannot articulate the primary
finding in one sentence without economist interpretation, the walkthrough or narration
must be revised before the live session runs. The sentence that passes is also the
sprint-level north star test artifact for this demo cycle (CLAUDE.md §North Star Test).

**Artifact format** (`YYYY-MM-DD-v{version}-audience-simulation.md` in `docs/demo/m{N}/reviews/`):
1. One section per persona — each agent's findings in the format above, in-character and unedited.
2. PM Agent presenter preparation summary: numbered list of questions the presenter must
   be able to answer, consolidated from all persona findings, ranked by severity.
3. North star gate declaration: Persona 5 verdict and primary finding sentence, promoted
   to the summary level for direct reference by PM Agent and EL.

**Gate:** Persona 5 north star verdict is PASS, and all CRITICAL persona findings are
resolved (same three-condition criteria as Step 6b) before Step 9.

**Naming rule:**
Before saving, run:
```bash
find docs/demo/ -name "*-audience-simulation*"
```
Confirm the filename matches `YYYY-MM-DD-v{version}-audience-simulation.md`. The M14
instance will be the canonical reference for this step.

### Step 8 — File and triage findings

File DEMO-NNN issues from review output. PM Agent TRIAGE mode on each finding.

**Tracking requirement (M10 forward — Issue #664 Gap 4):** File a GitHub issue for every
CRITICAL and HIGH finding before the stakeholder session (Step 9). The issue number must
appear in the review artifact summary table. MEDIUM and LOW findings are filed at PM Agent
discretion.

Fix CRITICAL items before the stakeholder session.
HIGH items: acknowledge honestly in narration if unfixed.
Save the IR review to `docs/demo/m{N}/reviews/YYYY-MM-DD-v{version}-ir-review.md`.

Create the stakeholder-review placeholder if it does not already exist:
`docs/demo/m{N}/reviews/PENDING-v{version}-stakeholder-review.md`
(Use the template in `docs/templates/` or follow the structure of the M12 instance.)

**GitHub release page completeness check (mandatory — demo-cycle milestones):**
Verify the GitHub release page for the current version tag is self-contained. If the current tag is a patch release (`v{N}.{N}.1`) that supersedes an earlier tag (`v{N}.{N}.0`) without a public release page, the patch page must cover the full milestone arc — not just the delta since the prior tag.

Checklist:
- [ ] Release title includes the milestone name and demo theme
- [ ] Body documents all major deliverables (not only since last tag)
- [ ] Demo recording URL is present (add once Step 9b is complete)
- [ ] Verify with: `gh release view v{N}.{N}.{P}`

If the page is incomplete, use `gh release edit v{N}.{N}.{P} --notes "..."` to rewrite it before Step 9. Reference: v0.12.1 release page was rewritten at M12 exit after it was found to describe only the patch delta; no v0.12.0 release page existed (PR #896 context, M12 exit ceremony gap).

### Step 9 — Live stakeholder session

Use `docs/demo/m{N}/stakeholder-walkthrough.md` as the presenter script.
Use `scripts/speak.sh` if text-to-speech narration is needed.
Use `scripts/demo.sh` to start the stack before the audience arrives.

**Post-session artifact (mandatory):**
After the session, complete the stakeholder-review placeholder and rename it:

```bash
mv docs/demo/m{N}/reviews/PENDING-v{version}-stakeholder-review.md \
   docs/demo/m{N}/reviews/YYYY-MM-DD-v{version}-stakeholder-review.md
```

Fill in: date, attendees, questions raised, most compelling moment, most questioned element,
north star test answer (specific — not aspirational), and follow-up actions. File GitHub
issues for any new capability gaps named by real stakeholders. Update SESSION_STATE.md to
record the demo as complete and cite the stakeholder-review artifact path.

### Step 9b — Screen recording and release upload (demo-cycle milestones)

A screen recording of the demo walkthrough is a required artifact for every even-numbered milestone demo cycle. It is the permanent visual record of what the tool could do at that milestone — future sessions, external reviewers, and potential institutional users cannot reconstruct the live application state from screenshots alone.

**When to record:** After all post-Step-9 UI fixes are merged and main is current. The recording reflects the final shipped state, not a rehearsal.

**What to record:** Use `scripts/demo.sh` to start the stack (the presenter guide printout should be visible in the terminal), then `scripts/demo.sh --run` for the Playwright walkthrough. Screen-record from launch through the final Zone 1D composite frame. Audio narration is optional but the terminal presenter guide must be visible during the startup phase so the recording is self-explanatory without live narration.

**Upload and link:**
```bash
gh release upload v{N}.{N}.{P} /path/to/recording.mp4
```
Then edit the release body to include a direct link:
```bash
gh release edit v{N}.{N}.{P} --notes-file /path/to/updated-notes.md
```

**Record in SESSION_STATE:** Add to the SESSION_STATE M{N} block:
`**Demo screen recording uploaded to GitHub release v{N}.{N}.{P}** — [URL]`

Reference: M12 screen recording uploaded to `github.com/PublicEnemage/worldsim/releases/tag/v0.12.1` (2026-06-11). Recording was only possible after fixing the demo.sh syntax error (PR #890, NM-041) — the bash -n gate in Step 3 closes this gap for future milestones.

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
| M12 | #755 | IR: `docs/demo/m12/reviews/2026-06-11-v0.12.1-ir-review.md` (14 findings DEMO-056–069; 3 retracted) — Audience sim: `2026-06-11-v0.12.1-audience-simulation.md` (DEMO-070–096; gate PASS) — Stakeholder: `2026-06-11-v0.12.1-stakeholder-review.md` (simulated session; north star PASS; real external session #843 outstanding) |
