# Demo Preparation Standard

**Established:** 2026-05-18
**Cadence:** Every two milestones (M6, M8, M10, M12...)
**Reference cases:** Issue #220 (M6), Issue #333 (M8)

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
      YYYY-MM-DD-v{version}-stakeholder-review.md
  stakeholder-walkthrough.md       — current version (updated each demo cycle)
```

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

### Step 6 — Run the demo and capture screenshots

```bash
./scripts/demo.sh          # Start stack, run migrations, seed data
./scripts/demo.sh --run    # Launch Playwright walkthrough (captures screenshots)
```

Screenshots land in `docs/demo/m{N}/screenshots/`. Verify five frames match the UX Agent brief.

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
| M8 | #333 | `docs/demo/m8/reviews/` (pending) |
