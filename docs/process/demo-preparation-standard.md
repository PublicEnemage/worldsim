# Demo Preparation Standard

**Established:** 2026-05-18
**Last revised:** 2026-06-02 (M10 — screenshot naming, legibility gate, narration instrument check, NARRATION-RULING-1 self-check, review naming convention enforcement; closes #379, NM-031)
**Cadence:** Every two milestones (M6, M8, M10, M12...)
**Reference cases:** Issue #220 (M6), Issue #333 (M8), Issue #261 (M10)

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

Do NOT update the North Star closing (§18:00–19:00). It does not change.
Do NOT update the backtesting credibility section unless new cases were added.

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

### Step 6 — Run the demo and capture screenshots

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

### Step 7 — Independent Review Agent

Activate a fresh Claude instance. Follow `docs/process/independent-review-prompt.md` exactly:

- Message 1: context setting (no screenshots yet)
- Message 2: attach screenshots in UX Agent brief sequence (C, A, B, D, E), ask four-part review task

The reviewer persona: senior policy analyst, 15 years fiscal adjustment experience, sat on both sides
of IMF negotiations. Permission to be direct and critical given explicitly before screenshots are shared.

### Step 8 — File and triage findings

File DEMO-NNN issues from review output. PM Agent TRIAGE mode on each finding.
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

---

## Reference Cases

| Milestone | Issue | Review |
|---|---|---|
| M6 | #220 | `docs/demo/m6/reviews/2026-05-07-v0.6.0-stakeholder-review.md` |
| M8 | #333 | `docs/demo/m8/reviews/2026-05-18-v0.8.0-stakeholder-review.md` |
| M10 | #261 | `docs/demo/m10/reviews/2026-06-02-v0.10.0-stakeholder-review.md` |
