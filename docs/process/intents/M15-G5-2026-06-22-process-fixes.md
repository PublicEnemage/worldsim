---
name: M15-G5-process-fixes
type: implementation-intent
issues: "#1007, #1067, #1083, #1084, #1088, #1089, #1090, #1048, #1004"
status: Filed
authored-by: Frontend Architect Agent + UX Designer Agent + Chief Methodologist Agent + Data Architect Agent + Architect Agent
authored-date: 2026-06-22
implementing-agents: "Frontend Architect Agent (#1007, #1083, #1067); UX Designer Agent (#1088, #1089, #1090); Chief Methodologist Agent (#1084); Data Architect Agent (#1048); Architect Agent (#1004)"
sprint-entry: "docs/process/sprint-plans/m15-g5-sprint-entry.md — EL Approved 2026-06-22"
adr-reference: "No ADR gate — all G5 items are bug fixes, demo artifact production, infrastructure, or process/documentation changes within accepted ADR scope"
release-branch: release/m15
---

# Implementation Intent: M15-G5 — Process Fixes + Walkthrough Updates

## 1. Source Reference

**Sprint entry:** `docs/process/sprint-plans/m15-g5-sprint-entry.md` — EL Approved 2026-06-22
**ADR gate:** None — all G5 items are within accepted ADR scope or are process/infrastructure/documentation changes
**Date authored:** 2026-06-22
**Authored by:** Frontend Architect Agent + UX Designer Agent + Chief Methodologist Agent + Data Architect Agent + Architect Agent (co-authorship; each agent owns their deliverable ACs)
**Implementing agents:**
- Frontend Architect Agent — #1007 (recompute-badge), #1083 (grounding-strip date label), #1067 (M15 screenshots)
- UX Designer Agent — #1088, #1089, #1090 (M15 walkthrough creation + three DEMO fixes)
- Chief Methodologist Agent — #1084 (PSP calibration anchor)
- Data Architect Agent — #1048 (Docker Alembic migrations)
- Architect Agent — #1004 (intent template Visual Spec)

**Issues in scope:**

| Issue | Title | Tier | Implementing agent |
|---|---|---|---|
| #1083 | ux(grounding-strip): date label "2024-Q1" → "Apr 2024" | Tier 1 — gates G8 | Frontend Architect Agent |
| #1067 | demo(screenshots): Frame B and C are same screenshot (IR-003) | Tier 1 — gates G8 | Frontend Architect Agent |
| #1088 | docs(demo): walkthrough — "0 consecutive steps" plain language | Tier 1 — gates G8 | UX Designer Agent |
| #1089 | docs(demo): walkthrough — Grounding strip persistence note | Tier 1 — gates G8 | UX Designer Agent |
| #1090 | docs(demo): walkthrough — methodology documentation URL | Tier 1 — gates G8 | UX Designer Agent |
| #1007 | fix: recompute-badge not visible after apply-control-change | Tier 2 | Frontend Architect Agent |
| #1048 | infra: Docker API container Alembic migrations (NM-049) | Tier 2 | Data Architect Agent |
| #1084 | methodology: PSP historical calibration anchor (DEMO-127) | Tier 2 | Chief Methodologist Agent |
| #1004 | process: Visual Spec section for intent template | Tier 2 | Architect Agent |

---

## 2. Persona Trace Elements Targeted

> *G5 is a mixed sprint with no governing ADR. Persona trace is derived from the user-facing impact of each deliverable. Documentation and infrastructure items trace forward to the persona they unblock.*

**P-1 — Personas served:**
- **Primary:** Persona 2 (Eleni — Finance Ministry Negotiator) and Persona 5 (Aicha — Junior Ministry Analyst) for #1007 and #1083 — both affect the active control and Grounding strip workflows visible to these personas in the Reactive entry state.
- **Secondary:** Persona 1 (Lucas — Non-specialist observer) and all demo personas for #1067 and #1088–#1090 — screenshot quality and walkthrough clarity affect the demo audience directly.
- **Forward trace (infrastructure/process):** #1048 (Docker migrations), #1084 (PSP calibration anchor), #1004 (intent template) serve all personas indirectly by improving platform reliability and implementation accuracy.

**P-2 — Entry state:**
- #1083 (date label): **Reactive** — Grounding strip is visible at L0 (zero interaction) when a scenario is loaded. Persona 2 reads it immediately at scenario open.
- #1007 (recompute-badge): **Active** — Persona 2 has changed a control value and applied it. The badge signals pending recompute during the 90-second window before she advances to the next step.
- #1067, #1088–#1090: **Demo entry** — walkthrough and screenshots are preparation artifacts for the G8 live stakeholder demo (#843).
- #1084, #1048, #1004: No direct entry state — infrastructure and process improvements.

**P-3 — Journey reference:**
- #1083: Journey A Step 0 (Grounding strip reads at scenario load — ADR-016 Component 2 surface; date field is part of the entry-state metadata display)
- #1007: Journey B Step 2 (Fidelity discipline — control-change workflow; badge confirms pending state before step advance)
- #1088–#1090: Journey A prep — walkthrough preparation for G8 live demo (Journey Step pre-conditions)

**P-4 — Time / interaction ceiling:**
- Grounding strip date (#1083): L0 — visible at scenario load with zero interaction; date must be readable in under 3 seconds.
- Recompute-badge (#1007): within 2 seconds of clicking Apply — no additional interaction required.
- Screenshots (#1067): production artifact — no runtime ceiling; distinctness verified by QA test.

**P-7 — North star capability delivered:**
For #1083: Aicha reads "Apr 2024" in the Grounding strip and immediately understands this is the April 2024 starting point for the scenario. She does not need to translate "2024-Q1" into a month before she can say "our initial state is April 2024 — this is from the IMF WEO April 2024 release."

For #1007: Eleni changes fiscal_multiplier from 1.00 to 1.30 and clicks Apply. The recompute badge appears immediately, telling her the current trajectory display reflects the old parameters. She advances the step and the badge clears — she now knows the trajectory is fresh. She can cite the updated reserve coverage figure without uncertainty about whether the model reflects her change.

For #1088–#1090: A presenter running the M15 demo for an external stakeholder can narrate the consecutive-steps count in plain language, explain Grounding strip persistence without confusion, and direct a methodology question to a named document — all without improvising corrections mid-session.

---

## 3. Observable Application State

### 3.1 Primary observable state

**#1083 — Grounding strip date in human-readable format:**

With the WorldSim application running at 1440×900 and the ZMB ECF scenario loaded, the Grounding strip renders the initial-state date in "Mmm YYYY" format — e.g., "Apr 2024". The date label contains no hyphen-separated quarter notation (no "2024-Q1", no "Q1 2024"). The format is identical for all entities with a quarterly-expressed reference date in `initial_state`. A non-technical stakeholder can read the date without knowing what "Q1" means.

### 3.2 Secondary observable states

**Secondary 1 — Recompute-badge signals pending state:**
With a ZMB ECF scenario loaded at step 1, when the user changes a control value (e.g., fiscal_multiplier) and clicks Apply, an element with `data-testid="recompute-badge"` becomes visible. The badge contains text that explains the pending state without requiring mediation (e.g., "Recompute pending" or "Results reflect previous parameters — advance to update"). The badge is absent before the Apply action and clears after step advance.

**Secondary 2 — M15 walkthrough exists with three DEMO fixes applied:**
`docs/demo/m15/stakeholder-walkthrough.md` exists as a preliminary M15 walkthrough (derived from the M14 walkthrough) with the following three corrections applied relative to the M14 source:
- (DEMO-123) No instance of "0 consecutive steps" in raw presenter narration
- (DEMO-124) Explicit note that the Grounding strip shows entry-state data, fixed at scenario creation
- (DEMO-129) At least one reference to a named methodology documentation path

**Secondary 3 — M15 screenshot set contains five distinct frames:**
`docs/demo/m15/screenshots/` contains exactly five PNG files (frame-a.png through frame-e.png). Frame B and Frame C are captured from different application states — different step positions or different Zone visibility — and are not byte-identical. The visual difference is identifiable without knowing the demo script.

### 3.3 Silent failure detection

**SF-1 (#1083 — date renders empty or unchanged):** If the date label renders as an empty string or retains "2024-Q1" after implementation, the grounding strip looks correct to the implementor but is broken for the non-technical stakeholder. Detection: AC-1 (negative assertion that "Q1" notation is absent) and AC-2 (positive assertion that a month-name string is present) together prevent both silent failures — an empty string would fail AC-2; a retained quarter string would fail AC-1.

**SF-2 (#1007 — badge absent after Apply):** The Apply action completes but the recompute badge does not render, leaving the user uncertain whether the model reflects the new parameter. Detection: AC-4 asserts `data-testid="recompute-badge"` is visible within 2 seconds of Apply. AC-3 confirms the badge is absent before Apply, distinguishing the pending state from a stuck-visible badge.

**SF-3 (#1088 — walkthrough contains raw phrase):** The walkthrough is derived from M14 but the "0 consecutive steps" phrase is not edited out, reaching real stakeholders in the G8 live demo. Detection: AC-8 (`grep -c "0 consecutive steps"` returns 0) runs as a CI-passing test before the G8 sprint entry opens.

---

## 4. Acceptance Criteria

> *ACs 1–6 are Frontend Playwright E2E. ACs 7–13 are backend pytest (file-existence, content-presence, and infrastructure).*

**AC-1:** In the running application at 1440×900 with the ZMB ECF scenario loaded, when the Grounding strip is visible, then `expect(page.locator('[data-testid="grounding-strip-date"]')).not.toContainText(/\d{4}-Q\d/)` passes — confirming quarter notation is absent from the date label. (#1083)

**AC-2:** In the running application at 1440×900 with the ZMB ECF scenario loaded, when the Grounding strip is visible, then `page.locator('[data-testid="grounding-strip-date"]').textContent()` matches the pattern `[A-Z][a-z]{2} \d{4}` (e.g., "Apr 2024") — confirming the date is in human-readable month-year format. (#1083)

**AC-3:** In the running application at 1440×900 with the ZMB ECF scenario loaded at step 1 and no control changes applied, then `expect(page.locator('[data-testid="recompute-badge"]')).not.toBeVisible()` passes — confirming the badge is absent in the default step-viewed state. (#1007)

**AC-4:** In the running application at 1440×900, after the user changes a control value (e.g., fiscal_multiplier) and clicks `[data-testid="apply-control-change"]`, then within 2 seconds `expect(page.locator('[data-testid="recompute-badge"]')).toBeVisible()` passes — confirming the badge appears to signal pending recompute. (#1007)

**AC-5:** In the running application at 1440×900, after the recompute-badge is visible following an Apply action, when the user advances to the next step, then `expect(page.locator('[data-testid="recompute-badge"]')).not.toBeVisible()` passes — confirming the badge clears on step advance, indicating the trajectory now reflects the updated parameters. (#1007)

**AC-6:** In the running application at 1440×900 with the ZMB ECF scenario, when a Playwright screenshot is captured at step 1 (the Frame B application state) and another at step 2 (the Frame C application state), then the two screenshots are not pixel-identical — `expect(screenshotStep1).not.toEqual(screenshotStep2)` using Playwright screenshot comparison — confirming Frame B and Frame C derive from genuinely different application states. (#1067)

**AC-7:** `find docs/demo/m15/screenshots -name "frame-*.png" | sort` lists exactly five files: frame-a.png, frame-b.png, frame-c.png, frame-d.png, frame-e.png. Each file is non-empty (size > 0 bytes). `diff <(md5sum docs/demo/m15/screenshots/frame-b.png | awk '{print $1}') <(md5sum docs/demo/m15/screenshots/frame-c.png | awk '{print $1}')` exits non-zero (hashes differ). (#1067)

**AC-8:** `docs/demo/m15/stakeholder-walkthrough.md` exists (file is non-empty). `grep -c "0 consecutive steps" docs/demo/m15/stakeholder-walkthrough.md` returns 0 — confirming the raw phrase from DEMO-123 is absent from presenter narration. Where the consecutive-steps concept is explained, plain language replaces the raw phrase. (#1088)

**AC-9:** `docs/demo/m15/stakeholder-walkthrough.md` contains at least one instance of "entry-state" in context of the Grounding strip narration section. `grep -c "entry-state" docs/demo/m15/stakeholder-walkthrough.md` returns ≥1 — confirming the DEMO-124 correction is present: presenters are told the Grounding strip shows fixed entry-state data and that current values appear in Zone 1B and the trajectory view. (#1089)

**AC-10:** `docs/demo/m15/stakeholder-walkthrough.md` contains at least one reference to a named methodology documentation path in the section where model calibration or methodology is discussed. `grep -c "methodology" docs/demo/m15/stakeholder-walkthrough.md` returns ≥1 in context of a named document or file path (not only in passing prose) — confirming a presenter can direct a participant to the source document directly (DEMO-129). (#1090)

**AC-11:** Starting from a clean Docker environment (`docker compose down -v && docker compose up --build`), `GET /api/v1/health` returns HTTP 200 and `GET /api/v1/entities` returns HTTP 200 with at least one entity in the response — confirming all Alembic migrations applied before the first request is served, not producing a 500 error from an unapplied migration. (#1048)

**AC-12:** `find docs/methodology -name "psp-calibration-anchor.md"` exits 0. The file's content satisfies all of: (1) `grep -c "ECF"` ≥1 (names at least one IMF ECF programme), (2) `grep -c "compliance"` ≥1 (documents compliance outcome), and (3) `grep -ci "imf\|article iv\|ecf review\|public information notice"` ≥1 (cites at least one publicly available source). A human reader can identify country, year, arrangement type, and outcome without searching outside this document. (#1084)

**AC-13:** `grep -c "Visual Spec\|§Visual Spec" docs/process/intent-template.md` returns ≥1 — confirming the section exists. `grep -c "Required when" docs/process/intent-template.md` returns ≥1 — confirming the required-vs-optional rule is stated. `grep -c "data-testid" docs/process/intent-template.md` returns ≥2 — confirming both a minimum-field specification and a concrete example using a `data-testid` selector are present in the section. `grep -c "viewport" docs/process/intent-template.md` returns ≥1 in the §Visual Spec section — confirming viewport is named as a minimum field. (#1004)

---

## 4b. Visual Spec (before/after)

**AC-1 / AC-2 (before) — Grounding strip date: quarter notation:**
```
Grounding strip (current state, ZMB ECF):
  ZMB  ·  2024-Q1  ·  IMF WEO April 2024
           ^^^^^^^
           YYYY-QN format — requires translation by reader
           Non-technical stakeholder must know Q1 = January–March
           to understand the reference date
```

**AC-1 / AC-2 (after) — Grounding strip date: human-readable:**
```
Grounding strip (fixed state, ZMB ECF):
  ZMB  ·  Apr 2024  ·  IMF WEO April 2024
           ^^^^^^^^
           "Mmm YYYY" format — self-interpreting
           A non-technical stakeholder reads this as "April 2024"
           with no translation required
```

---

**AC-4 (before) — Recompute-badge absent after Apply (current broken state):**
```
Control panel — after Apply (current state):
  [fiscal_multiplier: 1.30]  [Apply ✓]

  Zone 1A trajectory chart  (shows old trajectory — fiscal_multiplier=1.00)
  ← no indicator that the displayed output is stale ←
  [no recompute-badge]
  ^^^^^^^^^^^^^^^^^^^ THIS IS THE BUG: user cannot tell whether
                      the chart reflects the new or old parameter
```

**AC-4 (after) — Recompute-badge visible after Apply (fixed state):**
```
Control panel — after Apply (fixed state):
  [fiscal_multiplier: 1.30]  [Apply ✓]

  [data-testid="recompute-badge"]
  ┌────────────────────────────────────────────┐
  │ ⟳  Recompute pending — advance step        │
  │    to see updated trajectory               │
  └────────────────────────────────────────────┘
  Zone 1A trajectory chart  (still shows old trajectory — intentional)
  ← badge signals stale state; clears when user advances ←
```
*Badge must contain explanatory text, not only an icon — required for Kryptonite compliance (Section 5).*

---

## 5. Kryptonite Constraint Check

> *Authority: CLAUDE.md §Agent Execution Lifecycle — Kryptonite Design Constraint (FD-3).*
> *Applied to #1007 and #1083 — both affect Persona 2 in the Reactive entry state and
> Persona 5 in the active-control workflow. Documentation and infrastructure items
> (AC-7–AC-13) are not user-facing and are exempt from this check.*

**Does this implementation's primary observable state require specialist mediation for Persona 2 to act on it in the Reactive entry state (90-second ceiling)?**

`[x]` No — the observable states for #1083 and #1007 are interpretable by Persona 2 without an analyst translating them.

**Verification per deliverable:**

- **Grounding strip date format (#1083 — AC-1/AC-2):** The fix moves FROM "2024-Q1" (which requires a reader to know that Q1 = January–March) TO "Apr 2024" (which any calendar-literate reader understands as April 2024). The change reduces specialist mediation requirements, not increases them. Kryptonite constraint: PASS.

- **Recompute-badge (#1007 — AC-3–5):** The badge must contain explanatory text (see §4b after-state: "Recompute pending — advance step to see updated trajectory"), not only an icon. An icon alone requires the user to know what the icon means; text makes the state self-interpreting. Eleni reads "Recompute pending — advance step" and knows exactly what to do — she does not need a presenter or specialist to explain why the chart looks unchanged after she clicked Apply. If the implementation uses only an icon without text, the kryptonite constraint FAILS and must be revised before Step 4 Verify. Kryptonite constraint: CONDITIONAL on badge containing text — implementation must include explanatory text label or `aria-label` with equivalent content.

---

## 6. Out of Scope

1. **Grounding strip date format for modes other than step-viewed state.** The date label fix (#1083) targets the initial-state reference date. No changes to other date fields in the Grounding strip (e.g., step timestamps in Zone 1A trajectory) are in scope.

2. **Recompute-badge for modes other than the control-change workflow.** The badge fix (#1007) targets the state after Apply is clicked. Recompute state from other triggers (e.g., scenario creation form changes) is not in G5 scope.

3. **M15 screenshot content beyond frame distinctness.** G5 creates a preliminary M15 screenshot set. The content of each frame (which features to highlight) is a G8 decision. G5 only ensures frames B and C are distinct and the full set of 5 files exists. G8 will replace the G5 screenshots with M15-feature-specific frames; the file names and directory structure created by G5 must be preserved.

4. **Full M15 walkthrough authorship.** G5 creates `docs/demo/m15/stakeholder-walkthrough.md` as a derivative of the M14 walkthrough with three DEMO fixes applied. G8 is responsible for the full M15-specific narration update covering new features (Layer 3 sentences, Zone 1A, cohort disaggregation). G8 must not overwrite the three DEMO-123/124/129 fixes established by G5.

5. **Live external data fetch in the Docker migration fix (#1048).** The Docker migration fix ensures migrations run at container startup; it does not change the data population logic or add new seed data.

6. **PSP algorithmic calibration.** The PSP calibration anchor document (#1084) records the historical case and citation for the Chief Methodologist's reference. It does not introduce a new PSP algorithm or change the existing `programme_survival_probability` calculation.

7. **Tier 3 items (#837, #951, #259).** Configuration-driven demo scripts, solo-use review protocol, and CTO legibility metrics dashboard are addressed only if Tier 1 and Tier 2 capacity permits. None of these gate G8 or G5 exit.

---

## 7. Test Authorship Obligation

**QA Lead:** QA Lead Agent
**Test authorship deadline:** Before any G5 implementation PR is opened
**Test file locations:**
- Frontend Playwright: `frontend/tests/e2e/m15-g5-process-fixes.spec.ts` — AC-1 through AC-6 (Frontend Architect items: #1083, #1007, #1067 app-state verification)
- Backend pytest: `backend/tests/test_m15_g5_process_fixes.py` — AC-7 through AC-13 (file-existence, content-presence, infrastructure: #1067 hash check, #1088, #1089, #1090, #1048, #1084, #1004)

**AC assignment summary:**

| AC | Issue | Test file | Authored before implementation? |
|---|---|---|---|
| AC-1 | #1083 — date NOT quarter format | Playwright | No — BLOCKING |
| AC-2 | #1083 — date IS month-year format | Playwright | No — BLOCKING |
| AC-3 | #1007 — badge absent before Apply | Playwright | No — BLOCKING |
| AC-4 | #1007 — badge visible after Apply | Playwright | No — BLOCKING |
| AC-5 | #1007 — badge cleared after advance | Playwright | No — BLOCKING |
| AC-6 | #1067 — Frame B ≠ Frame C pixel comparison | Playwright | No — BLOCKING |
| AC-7 | #1067 — 5 distinct PNG files in m15/screenshots | Backend pytest | No — BLOCKING |
| AC-8 | #1088 — no "0 consecutive steps" in walkthrough | Backend pytest | No — BLOCKING |
| AC-9 | #1089 — "entry-state" note in walkthrough | Backend pytest | No — BLOCKING |
| AC-10 | #1090 — methodology doc reference in walkthrough | Backend pytest | No — BLOCKING |
| AC-11 | #1048 — Docker health + entities after clean start | Backend pytest | No — BLOCKING |
| AC-12 | #1084 — PSP calibration anchor exists with required content | Backend pytest | No — BLOCKING |
| AC-13 | #1004 — intent template has Visual Spec section with viewport + example | Backend pytest | No — BLOCKING |

**QA Lead acknowledgment:**
`[x]` QA Lead: Tests for AC-1 through AC-13 authored and filed. 2026-06-22

---

## 8. Step 4 Verify — PASS (2026-06-22)

*Completed by EL acting as implementing agent reviewer + QA confirmation. All PRs merged
to `release/m15` (#1119, #1121, #1122, #1123). CI green on all PRs (playwright-e2e PASS,
test-backend PASS, compliance-scan PASS, lint PASS). Verification evidence: CI run logs
+ local file checks (grep, md5, find).*

**Frontend Architect Agent — #1007, #1083, #1067:**
- [x] AC-1: `formatVintageDate("2024-Q1")` → "Apr 2024"; `grounding-strip-date` testid at
  GroundingStrip.tsx:247; text does not match `/\d{4}-Q\d/` — CI playwright-e2e PASS (PR #1119)
- [x] AC-2: `grounding-strip-date` text matches `[A-Z][a-z]{2} \d{4}` — "Apr 2024" confirmed
  via `QUARTER_MONTHS` mapping at GroundingStrip.tsx:26–39; CI PASS (PR #1119)
- [x] AC-3: Badge gated to `mode === "MODE_3"` (ScenarioInstrumentCluster.tsx:576); absent
  before Apply in MODE_1/MODE_2; MODE_3 test: badge absent before Apply; CI PASS (PR #1119)
- [x] AC-4: G5 fix: `recomputeStatus: "pending"` set immediately before async branch POST
  (ScenarioInstrumentCluster.tsx:468); badge at line 578 shows "Recompute pending — advance
  step to see updated trajectory" — explanatory text; CI PASS (PR #1119)
- [x] AC-5: Badge clears after step advance (recomputeStatus → idle); CI PASS (PR #1119)
- [x] AC-6: Playwright pixel comparison at step 1 vs step 2 — non-identical; CI PASS (PR #1119)
- [x] AC-7: 5 PNG files confirmed: frame-a through frame-e; frame-b md5=fab826ed1d50e649dfc048d3d8144cfd ≠ frame-c md5=e30e40b17f9194e08b866eac0a40ce44

**UX Designer Agent — #1088, #1089, #1090:**
- [x] AC-8: `grep -c "0 consecutive steps" docs/demo/m15/stakeholder-walkthrough.md` = 0 ✅
- [x] AC-9: `grep -c "entry-state" docs/demo/m15/stakeholder-walkthrough.md` = 9 (≥1) ✅
- [x] AC-10: `grep -c "methodology" docs/demo/m15/stakeholder-walkthrough.md` = 14 (≥1 with named path) ✅

**Data Architect Agent — #1048:**
- [x] AC-11: CI test-backend PASS on PR #1123; `backend/entrypoint.sh` runs `alembic upgrade head`
  before exec; Dockerfile uses ENTRYPOINT + CMD — clean stack start confirmed by CI

**Chief Methodologist Agent — #1084:**
- [x] AC-12: `find docs/methodology -name "psp-calibration-anchor.md"` → exits 0;
  ECF count=14, compliance count=7, IMF citation count=13; country (Zambia/Ghana), year
  (2022/2023), arrangement type (ECF), outcome (mixed compliance) all present

**Architect Agent — #1004:**
- [x] AC-13: Visual Spec count=2 (≥1) ✅; "Required when" count=1 (≥1) ✅;
  data-testid count=4 (≥2) ✅; viewport count=2 (≥1) ✅

**Backend pytest gate:**
- [x] CI test-backend PASS on PR #1122 (AC-7–AC-10, AC-12, AC-13) and PR #1123 (AC-11)

**Step 4 verdict:** PASS — 13/13 ACs confirmed. All Tier 1 and Tier 2 items verified by
CI evidence and local file checks. G8 gate satisfied: five Tier 1 items (#1067, #1083,
#1088, #1089, #1090) all merged to `release/m15`. No Verify failures; no rejection artifacts.
Date: 2026-06-22.

---

## 9. Step 5 Validate — BPO ACCEPT (2026-06-22)

*Business PO: @PublicEnemage (Engineering Lead) acting as Business PO.*
*Date: 2026-06-22*
*Customer Agent Layer 3 assessment: filed in §9a below.*

---

### §9a — Customer Agent Layer 3 Assessment

**Trigger:** #1007 (recompute-badge) and #1083 (grounding-strip date) serve Persona 2 (Eleni)
and Persona 5 (Aicha) in the Reactive/Active entry states — Layer 3 gate required per
`CLAUDE.md §Layer 3 Quality Gate (FD-2)`.

**#1083 — Grounding strip date format:**
- BEFORE: "2024-Q1" — requires reader to know Q1 = January–March (specialist mediation)
- AFTER: "Apr 2024" — any calendar-literate reader understands "April 2024" with zero translation
- Layer 3 quality: The output now *tells the user what the date means* rather than displaying a
  notation code. Aicha reads "Apr 2024" and immediately cites "our initial state is April 2024"
  without needing the presenter to interpret the quarter notation.
- **Layer 3 verdict (#1083): PASS**

**#1007 — Recompute badge:**
- BEFORE: No indicator after Apply — user cannot tell whether the trajectory reflects the new
  or old parameter (DEMO4-001 analog: stale output displayed as current)
- AFTER: "⟳ Recompute pending — advance step to see updated trajectory" — names the state,
  specifies the action, tells the user why the chart looks unchanged
- Layer 3 quality: Badge contains full explanatory text (not icon-only). Kryptonite constraint
  is satisfied: Eleni reads the badge and knows exactly what to do — no presenter mediation,
  no specialist required to decode the state.
- **Layer 3 verdict (#1007): PASS**

---

### §9b — Tier 1 Validation (gates G8)

**#1083 — Grounding strip date "Apr 2024":**
`formatVintageDate()` confirmed at GroundingStrip.tsx:26–39. `QUARTER_MONTHS` mapping produces
"Apr 2024" from "2024-Q1". `data-testid="grounding-strip-date"` present at line 247. CI
playwright-e2e PASS. A non-technical stakeholder sees "Apr 2024" and reads it immediately.
**ACCEPT** ✅

**#1088/#1089/#1090 — Walkthrough DEMO-123/124/129 fixes:**
- DEMO-123: "0 consecutive steps" count = 0 (absent from presenter narration); plain-language
  equivalent present (walkthrough line 675+ confirms step-by-step narration)
- DEMO-124: "entry-state" count = 9; explicit note at line 168: "The Grounding strip shows
  entry-state data only." — DEMO-124 fixed ✅
- DEMO-129: "methodology" count = 14; `docs/onboarding/methodology-overview.md` cited at
  lines 50, 372, 495, 524, 592 — presenter can point methodology question to a named path ✅
A presenter running the M15 demo can narrate all three corrected points without improvising.
**ACCEPT** ✅

**#1067 — Frame B ≠ Frame C screenshots:**
frame-b md5=fab826ed1d50e649dfc048d3d8144cfd ≠ frame-c md5=e30e40b17f9194e08b866eac0a40ce44.
Frame B (step 1) and Frame C (step 3 — confirmed by walkthrough table at line 675: THESIS
frame is `frame-c.png` at step 3 / 6) depict genuinely different application states. Visual
difference is identifiable at a glance without demo script knowledge.
**ACCEPT** ✅

---

### §9c — Tier 2 Validation

**#1084 — PSP calibration anchor:**
`docs/methodology/psp-calibration-anchor.md` is self-contained and citation-complete:
Zambia 2022 ECF and Ghana 2023 ECF; calibration target table (0.80–<0.25 range); three IMF
press release citations. A finance ministry analyst can cite the PSP basis ("calibrated
against Zambia 2022 and Ghana 2023 ECF compliance patterns — published IMF sources") without
calling in a methodologist.
**ACCEPT** ✅

**Navigability note (non-blocking):** `docs/onboarding/methodology-overview.md` references PSP
in passing ("political feasibility constraint," line 58) but does not hyperlink to
`psp-calibration-anchor.md`. A presenter briefed on methodology docs location can navigate in
<1 minute; cold navigation may take longer. G8 action item: add a hyperlink from
`methodology-overview.md §Political Economy module` to `psp-calibration-anchor.md` before
the live external demo.

**#1004 — Intent template §Visual Spec:**
Visual Spec section confirmed present with "Required when" rule, data-testid example (×4 in
section), and viewport requirement (×2). A QA Lead reading the section knows: (1) when a
Visual Spec is required, (2) minimum fields (element selector, viewport, expected content),
(3) a concrete prior-sprint example.
**ACCEPT** ✅

**#1048 — Docker Alembic migrations:**
CI test-backend PASS on PR #1123. `backend/entrypoint.sh` confirmed: `alembic upgrade head`
runs before `exec "$@"`. Dockerfile uses ENTRYPOINT (entrypoint.sh) + CMD (uvicorn). A clean
`docker compose down -v && docker compose up --build` applies all migrations before first
request.
**ACCEPT** ✅

---

### §9d — North Star Assessment

**G5 is a process-fixes sprint.** Primary north star impact is indirect but real:

- **#1083:** Aicha reads "Apr 2024" at Grounding strip load and immediately cites "initial
  state April 2024" without requiring the IMF notation Q1→January translation. One fewer
  mediation step in the 90-second reactive window.
- **#1007:** Eleni changes fiscal_multiplier, sees "Recompute pending — advance step to see
  updated trajectory." She advances and knows the new trajectory reflects her change. She can
  cite the updated reserve coverage figure without uncertainty about parameter state.
- **Walkthrough fixes (#1088–#1090):** Real external participants in the G8 live demo will not
  hear "0 consecutive steps" as raw output; will not be confused about Grounding strip
  persistence; will be directed to a named methodology document when they ask about calibration.
- **#1084 (PSP anchor):** A methodologist question during the demo — "how is programme survival
  calibrated?" — can be answered with "Zambia 2022 and Ghana 2023 ECF compliance patterns,
  public IMF sources" without calling in the Chief Methodologist.

The finance minister's team at the demo table (and in subsequent real negotiations) encounters
fewer friction points and can act on instrument outputs without specialist mediation.

**North star verdict: PASS** — G5 removes small but real mediation layers in the mission-critical
90-second reactive window and prepares the G8 demo for real external participants without
presenting correctable quality gaps.

---

### §9e — Kryptonite Constraint Assessment

- **#1083:** "Apr 2024" requires no specialist knowledge to decode. A calendar-literate
  non-economist reads it directly. Kryptonite constraint: **PASS**
- **#1007:** Badge text "Recompute pending — advance step to see updated trajectory" is
  self-interpreting. No icon-only fallback. The text tells the user what to do. Kryptonite
  constraint: **PASS**

---

**Business PO verdict: ACCEPT**

All Tier 1 and Tier 2 items accepted. Customer Agent Layer 3 PASS for both user-facing
deliverables. North star PASS. Kryptonite PASS. G8 gate is SATISFIED — all five Tier 1
items (#1067, #1083, #1088, #1089, #1090) merged and validated. G8 sprint entry may now open.

One non-blocking action item for G8: add hyperlink from `methodology-overview.md` to
`psp-calibration-anchor.md` during demo walkthrough preparation.

**Date: 2026-06-22**

---

*Intent document filed 2026-06-22. Co-authored by: Frontend Architect Agent (#1007, #1083, #1067), UX Designer Agent (#1088–#1090), Chief Methodologist Agent (#1084), Data Architect Agent (#1048), Architect Agent (#1004). QA Lead files both test files before any implementation PR opens — this is a hard gate. Authority: `CLAUDE.md §Agent Execution Lifecycle`. Template: `docs/process/intent-template.md` (version 2026-06-17).*
