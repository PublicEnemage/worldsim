---
name: M18-G7-E-capture-narration
type: implementation-intent
issues:
  - "#1459 — DEMO-130: Frame B byte-identical to Frame A"
  - "#1464 — DEMO-135: Frame A captured at step 3 (not step 8, max divergence)"
  - "#1465 — DEMO-136: Frame C shows delta ≈ 0.00 (wrong step)"
  - "#1468 — DEMO-139: Choropleth centered on North America (not ZMB) in Act 2"
  - "#1471 — DEMO-142: 'Policy Malevolent Margin' jargon in DistributionalComparisonSummary"
  - "#1473 — DEMO-144: Walkthrough value '340,000' vs. actual ~342,700"
  - "DEMO-146 — Walkthrough Screenshot Reference table: filename mismatch"
  - "DEMO-147 — T3→T4 tier degradation at step 6 unacknowledged in narration"
  - "DEMO-148 — 8 NARRATION-RULING-1 transitions missing"
  - "DEMO-152 — Presenter note for breadcrumb showing 'OptionC'"
  - "DEMO-153 — Act 1 narration missing people-count translation"
status: "Filed — no ADR gate; all gates CLEAR. Sequencing: label fix (DEMO-142) FIRST before any recapture"
authored-by: Frontend Architect Agent
authored-date: 2026-06-29
implementing-agent: Frontend Architect Agent
sprint-entry: docs/process/sprint-plans/m18-g7-sprint-entry.md
adr-reference: "None — spec, walkthrough doc, and component label fixes"
root-cause-reference: docs/demo/m18/reviews/2026-06-29-g7-root-cause-analysis.md
release-branch: release/m18
bpo-acceptance-required: "No — correction to existing demo specification and walkthrough document"
customer-agent-l3-required: "No — spec and label corrections"
---

# Implementation Intent: M18-G7-E — Capture Sequence, Narration, and Label Fixes

> **Pre-implementation prerequisites (all required before implementation PR opens):**
> - [x] G7-0 root cause analysis filed and EL-approved (2026-06-29)
> - [x] No ADR gate (spec/doc/label fixes)
> - [x] BPO priority escalations acknowledged: DEMO-142 first, DEMO-146 walkthrough first, DEMO-148 before recapture
> - [ ] Clusters A, B, C, D code fixes confirmed (screenshot recapture only runs after code fixes)
> - [ ] QA: `demo-narrated.spec.ts` updated with correct capture sequence before recapture runs

---

## 0. Implementation Constraints

*Authority: G7-0 root cause analysis §Root Cause 5 + G7 sprint entry §Section 2 EL Note 1 (BPO priority escalations).*

1. **DEMO-142 (jargon label) is the first fix in this cluster — before any screenshot recapture.** The label "Policy Malevolent Margin" must be corrected to "Policy Maneuver Margin" before any new screenshot frames are captured. A jargon exposure in a stakeholder session is a professional credibility failure. If the jargon fix lands after recapture, the new frames carry the same defect.

2. **DEMO-146 (walkthrough filename table) is the first doc fix — before the screenshot recapture so the walkthrough matches the correct filenames from the start.**

3. **DEMO-148 (act transition sentences) must be authored before recapture so the walkthrough is correct at the point frames are captured.** The presenting analyst reads from the walkthrough — if transitions are missing at capture time, the walkthrough is wrong for the session.

4. **Corrected capture sequence** (from root cause analysis §Root Cause 5 §Fix):
   - **Frame B:** captured at step 3 (after policy input → PSP driver visible; before advancing to step 8)
   - **Frame A:** captured at step 8 (maximum divergence between baseline and counter-proposal)
   - **Frame C:** captured at step 8 (same state as Frame A — Zone 1B cohort section)
   - **Frame D/E:** ZMB Act 2 frames after `centerOnEntity('ZMB')` is called

5. **Frame A and Frame B must have different byte content.** The root cause was capturing both at the same UI state. After the fix: Frame B is at step 3 (policy input applied, PSP driver visible); Frame A is at step 8 (maximum divergence). These are different UI states — MD5 hashes will differ.

6. **Choropleth center on ZMB before Act 2 frames.** After `page.goto(/?scenario=${zmbCId})`, call `window.__worldsim_centerOnEntity('ZMB')` before Frame D capture. Allow 800ms pan animation.

7. **Do not change demo logic, scenario creation, or component architecture.** Cluster E changes are limited to: component label text (DEMO-142), spec capture sequence (DEMO-130/135/136), choropleth center call (DEMO-139), walkthrough document text (DEMO-144/146/147/148/152/153).

---

## 1. Source

**Issues:** #1459 (DEMO-130), #1464 (DEMO-135), #1465 (DEMO-136), #1468 (DEMO-139), #1471 (DEMO-142), #1473 (DEMO-144), DEMO-146, DEMO-147, DEMO-148, DEMO-152, DEMO-153

**Root cause document:** `docs/demo/m18/reviews/2026-06-29-g7-root-cause-analysis.md §Root Cause 5`

**Governing ADR:** None.

**Demo 7 anchor:** All five demo frames (Frame A–E) must be distinct, captured at the correct steps, with the choropleth centered correctly for Act 2. The walkthrough must match actual demo behavior.

---

## 2. Change Inventory

### 2.1 — Code changes

**DEMO-142: Label fix in `DistributionalComparisonSummary.tsx`**

Find the string "Policy Malevolent Margin" (or its source constant/variable) and replace with "Policy Maneuver Margin". Check both hardcoded strings and any i18n/constants files. Run `grep -r "Malevolent" frontend/src/` to find all occurrences.

### 2.2 — Spec changes (`frontend/tests/e2e/demo-narrated.spec.ts`)

**DEMO-130/135/136 — Corrected capture sequence:**

```typescript
// OLD sequence (broken):
// Frame A: captured at step 3 (after branch renders)
// Frame B: captured at step 3 (after narration speech — same state as Frame A)
// Frame C: captured at step 6 (3 nextStep clicks from step 3)

// NEW sequence (correct):
// Step 3: Apply policy input → capture Frame B
//   (PSP driver visible, step 3 context, distinct from Frame A)
// Steps 3→8: Advance 5 more steps (5 × nextStep clicks)
// Step 8: Maximum divergence
//   → capture Frame A (Zone 1A trajectory with CI bands at max divergence)
//   → capture Frame C (Zone 1B cohort section — CLEAR state)
```

The Frame B / Frame A ordering in the spec may differ from the narrative order (narration presents Frame A first) — this is acceptable; the spec captures frames in whatever order is logically cleanest. The walkthrough describes the frames in presentation order.

**DEMO-139 — Choropleth ZMB centering:**

After `page.goto(\`/?scenario=${zmbCId}\`)` and before Frame D screenshot:

```typescript
await page.evaluate(() => {
  const fn = (window as Record<string, unknown>).__worldsim_centerOnEntity as
    ((id: string) => void) | undefined;
  if (fn) fn('ZMB');
});
await page.waitForTimeout(800); // pan animation
```

### 2.3 — Walkthrough document changes (`docs/demo/m18/stakeholder-walkthrough.md`)

**DEMO-144:** Replace "340,000" with "approximately 342,700" (or match the actual simulation output once recapture is complete; use the exact figure from Frame A/C after recapture runs).

**DEMO-146:** Update Screenshot Reference table filenames to match the actual output filenames from `demo-narrated.spec.ts` screenshot configuration. Run the spec once and confirm filenames before updating the table.

**DEMO-147:** Add one sentence to Frame C narration acknowledging T3→T4 tier degradation: *"The confidence tier moves to exploratory at step 8 — this reflects the BandingEngine's step-depth rule: deeper projections carry wider uncertainty. The directional finding remains valid."*

**DEMO-148:** Add 8 NARRATION-RULING-1 transition sentences. Priority: Frame C→D act-break transition. Draft transitions:
- After Frame A → before Frame B: *"Now let's look at what this means at the moment the policy is applied."*
- Frame B → Frame C: *"Three steps later — at the point of maximum divergence."*
- Frame C → Frame D: *"We now shift to Zambia, where the Finance Ministry is negotiating debt restructuring with three competing proposals."* (highest-priority: act break)
- For remaining 5 transitions: follow the logical flow of the demo narrative established in the walkthrough; the exact wording is at the implementing agent's discretion unless BPO provides specific text.

**DEMO-152:** Add presenter note before Act 2 Frame D: *"Breadcrumb shows the reference scenario identifier — all three options are loaded and can be compared using the entity selector."*

**DEMO-153:** Add one sentence to Act 1 narration translating the 0.40 floor into people: *"That 0.40 floor represents approximately [X] million people in the informal workers cohort below the poverty threshold."* Use the actual figure from the simulation or a verified estimate; do not use a round-number approximation without a source.

---

## 3. Observable Application State

### 3.1 Primary observable state

**After Cluster E fixes, in `demo-narrated.spec.ts` run:**

Five screenshots are produced with distinct byte content (no two frames identical). Frame A and Frame B have different MD5 hashes. Frame D choropleth is centered on sub-Saharan Africa / ZMB.

`[data-testid="distributional-comparison-summary"]` label text does NOT contain "Malevolent" anywhere in the DOM.

### 3.2 Walkthrough document state

`docs/demo/m18/stakeholder-walkthrough.md` contains:
- "approximately 342,700" (not "340,000")
- T3→T4 acknowledgment sentence in Frame C section
- 8 act transition sentences (confirmed by line count or section headers)
- Breadcrumb presenter note before Act 2 Frame D
- People-count translation sentence in Act 1

### 3.3 Silent failure detection

**Silent failure — Frame A still at step 3:**
After spec update, Frame A screenshot is taken before advancing to step 8. Observable via E2E assertion that Zone 1D shows step 8 value when Frame A is captured.

**Silent failure — jargon not fully replaced:**
`grep -r "Malevolent" frontend/src/` returns results after the fix. Observable: grep check in test or pre-push hook.

**Silent failure — choropleth not centered:**
Frame D choropleth still centered on North America. Observable: visual review or choropleth center state assertion.

---

## 4. Acceptance Criteria

**AC-E1 (unit/grep — jargon removed):**
`grep -r "Malevolent" frontend/src/` returns zero results. The string "Policy Maneuver Margin" appears in the rendered DOM when `DistributionalComparisonSummary` is active.
*Source: §2.1 + DEMO-142 + EL Note 1 (BPO escalation: first fix in cluster E)*

**AC-E2 (E2E — Frame B at step 3, Frame A at step 8):**
After spec update: Frame B is captured when `current_step === 3` (assert Zone 1D or step indicator shows "3"). Frame A is captured when `current_step === 8`. The spec must include explicit step-state assertions before each screenshot call.
*Source: §0 Constraint 4 + DEMO-130/135/136*

**AC-E3 (E2E — Frame A and Frame B have different byte content):**
MD5 or SHA-256 hash comparison of Frame A file and Frame B file returns unequal values. This assertion must be in the spec or in a post-spec verification step.
*Source: §3.1 + NM-083 QA-first gate — "frame-a and frame-b MD5s differ"*

**AC-E4 (E2E — choropleth centered on ZMB before Frame D):**
Before Frame D screenshot: `window.__worldsim_centerOnEntity('ZMB')` is called and 800ms wait is observed. The choropleth center coordinates correspond to ZMB bounding box (approximately lat -15, lon 28). Assert via `page.evaluate(() => window.__worldsim_getMapCenter())` if the function is available; otherwise document as a visual review check.
*Source: §0 Constraint 6 + DEMO-139*

**AC-E5 (doc check — walkthrough value updated):**
`grep "340,000" docs/demo/m18/stakeholder-walkthrough.md` returns zero results. `grep "342" docs/demo/m18/stakeholder-walkthrough.md` returns at least one result.
*Source: §2.3 DEMO-144*

**AC-E6 (doc check — T3→T4 acknowledgment present):**
`grep -i "step-depth" docs/demo/m18/stakeholder-walkthrough.md` returns at least one result (or equivalent wording from DEMO-147 determination sentence). The Frame C narration section includes the acknowledgment.
*Source: §2.3 DEMO-147 + EL G7-0 determination: "Intentional — add acknowledgment sentence"*

**AC-E7 (doc check — act transitions present):**
`docs/demo/m18/stakeholder-walkthrough.md` contains 8 transition sentences between frames. The Frame C→D act-break transition is present as the first of the 8 sentences authored.
*Source: §2.3 DEMO-148 + EL Note 1 (BPO escalation: Frame C→D highest priority)*

---

## 5. Kryptonite Constraint Check

**DEMO-142 kryptonite risk:** "Policy Malevolent Margin" in a live external session is a professional credibility failure for Persona 5 (Aicha, Finance Minister) and would undermine the demonstration's authority. This is the highest-priority single fix in Cluster E and must land before any screenshot recapture.

No other kryptonite risk from Cluster E changes. The capture sequence fix and narration additions do not introduce new interaction affordances or user-facing text that could be misread.

---

## 6. Out of Scope

- Narration audio re-recording (text fix only — no TTS changes in scope for G7)
- Screenshot recapture itself (Cluster E fixes the spec; recapture runs after all code fixes A/B/C/D are also confirmed)
- Mode 1 step annotation changes
- Any frontend component changes beyond the label fix (DEMO-142)

---

## 7. Test Authorship Obligation

Cluster E is primarily spec and doc work. The "tests" for E are:
1. Updated `demo-narrated.spec.ts` with correct capture sequence (must pass before recapture)
2. Grep assertions for jargon removal and walkthrough content

**QA obligations before recapture:**

| AC | Verification method |
|---|---|
| AC-E1 | `grep -r "Malevolent" frontend/src/` — zero results |
| AC-E2 | Spec: step-state assertion before each screenshot call |
| AC-E3 | Spec: MD5 comparison of Frame A and Frame B |
| AC-E4 | Spec: `centerOnEntity('ZMB')` call present + 800ms wait before Frame D |
| AC-E5 | `grep "340,000" docs/demo/m18/stakeholder-walkthrough.md` — zero results |
| AC-E6 | `grep "step-depth" docs/demo/m18/stakeholder-walkthrough.md` — result |
| AC-E7 | Manual line count of transition sentences in walkthrough (8 minimum) |

**Screenshot recapture runs last** — after all five clusters (A, B, C, D, E code/label fixes) are confirmed and merged to `sprint/m18-g7`, run `demo-narrated.spec.ts` to produce new Frame A–E screenshots. Screenshots go to `docs/demo/m18/screenshots/`.

**Pre-push gates:** `cd frontend && npm run build` must exit 0.

*Filed: 2026-06-29. Authority: docs/process/agents.md §Frontend Architect Agent.*
