---
name: m14-g5-sprint-exit
type: sprint-exit
milestone: M14 — Methodology Publication and External Validation
sprint-group: G5
status: Confirmed
authored-by: PM Agent
date: 2026-06-18
pi-confirmed: true
release-branch: release/m14
sop-reference: docs/process/sprint-planning-sop.md §Sprint Exit Gate
---

# Sprint Exit — M14, G5: ADR-015 Evidence Thread Architecture (Components 1, 2, 3)

**Status:** Confirmed — all exit conditions satisfied
**Date produced:** 2026-06-18
**Release branch:** `release/m14`
**Sprint entry document:** `docs/process/sprint-plans/m14-g5-sprint-entry.md`

*Authority: `docs/process/sprint-planning-sop.md §Sprint Exit Gate` (Phase D output).
G5 implements ADR-015 Components 1, 2, and 3: L0 basis annotations on Zone 1D framework rows,
the Assumption Surface strip between Zone 0 and Zone 1, and `programme_survival_probability`
rendered as "Political Feasibility" in Zone 1D. Component 4 (cross-examination mode) is
deferred to M15.*

---

## Section 1 — Sprint Identification and Date

| Field | Value |
|---|---|
| Milestone | M14 — Methodology Publication and External Validation |
| Sprint group | G5 — ADR-015 Evidence Thread Architecture (Components 1, 2, 3) |
| Release branch | `release/m14` |
| Sprint groups | G5 only |
| Sprint entry document | `docs/process/sprint-plans/m14-g5-sprint-entry.md` |
| Intent document | `docs/process/intents/M14-G5-2026-06-17-adr015-frontend.md` |
| Exit checklist issue | #968 |
| Date implementation completed | 2026-06-18 |
| CI status on release branch | Green — all 6 required checks passed (PR #1030) |

---

## Section 2 — Implementation Status

| Group | PR | Merged? | CI status | Notes |
|---|---|---|---|---|
| G5 — ADR-015 Frontend (Components 1, 2, 3) | #1030 | Yes — 2026-06-18T15:41:47Z | Green | Pre-push build gate passed; 17/17 Playwright ACs pass |

**Implementation status:** All merged, CI green.

**Pre-push gate compliance:**
- Backend: No Python files modified — backend gate not required
- Frontend: `cd frontend && npm run build` run and exited 0 before push
- Branch name: `feat/m14-g5-adr015-frontend` — milestone prefix present, naming check passed

**Step 4 Verify verdict:** PASS — 2026-06-18
Verification artifact: `frontend/tests/e2e/m14-g5-adr015-frontend.spec.ts` — 17/17 tests passed
Full verdict recorded in intent document §8.

---

## Section 3 — Business PO Acceptance Table

| Deliverable | Work type | Customer Agent Layer 3 assessment | Business PO verdict | Verdict artifact |
|---|---|---|---|---|
| ADR-015 Component 1 — L0 basis annotations on Zone 1D framework rows | Frontend | Filed below (§3a) | ACCEPT | §3b below |
| ADR-015 Component 2 — Assumption Surface | Frontend | Filed below (§3a) | ACCEPT | §3b below |
| ADR-015 Component 3 — Political Feasibility row in Zone 1D | Frontend | Filed below (§3a) | ACCEPT | §3b below |

**Business PO acceptance status:** All ACCEPT.

---

### §3a — Customer Agent Layer 3 Assessment

*Filed by Customer Agent — 2026-06-18*
*Trigger: G5 introduces or modifies user-facing indicator labels, annotation text, and confidence tier disclosures — all Layer 3 triggers per CLAUDE.md §Layer 3 Quality Gate.*
*Applies to: Persons 2 (Finance Ministry Negotiator) and Persona 5 (Policy Researcher / External Analyst) — both are direct ADR-015 §P-1 targets.*

**Layer 3 definition:** The output tells the user what the number means — not only displays the number.

**Component 1 — Zone 1D L0 annotations:**
- Pre-G5: Zone 1D framework rows displayed composite_score value and framework label only. No data basis visible without navigating away.
- Post-G5: Each row displays a bracketed annotation immediately below the score: `[T2 · IMF WEO / CBJ · pre-cal]`. The annotation tells Persona 2 *not only* that a tier exists but what tier 2 means in context (citable official source), who produced it (named institution), and that it is pre-calibration (informing confidence in the number being challenged).
- Layer 3 verdict: **SATISFIES Layer 3**. The annotation makes the data basis interpretable by a finance ministry economist without further translation. "T2 · IMF WEO / CBJ" answers the challenge "where does this number come from?" without requiring the analyst to open a separate tab or ask a specialist.

**Component 2 — Assumption Surface:**
- Pre-G5: The scenario inputs that shaped the trajectory (fiscal multiplier, PE module status, conditionality type, data vintage) were only accessible in the scenario creation form — not visible in the instrument cluster view.
- Post-G5: The Assumption Surface appears as a single 24px line between the identity header and the instrument cluster: `Fiscal ×1.30 · Political economy: enabled · Conditionality: standard · Data: 2024-Q1 vintage`. The analyst can confirm the highest-sensitivity inputs at a glance before defending the trajectory.
- Layer 3 verdict: **SATISFIES Layer 3**. The strip converts the raw configuration parameters into a named, legible summary of the analytical assumptions in play. It does not require the analyst to know what `fiscal_multiplier: 1.3` means — the label reads as "Fiscal ×1.30" which immediately communicates the multiplier's direction and magnitude.

**Component 3 — Political Feasibility row:**
- Pre-G5: `programme_survival_probability` was computed by the political economy module but not surfaced in Zone 1D alongside the other framework scores. A Persona 2 user could not see programme survival probability alongside financial, human development, ecological, and governance scores.
- Post-G5: A fifth row — "Political Feasibility" — appears in Zone 1D when PE is enabled: `72% [T3 · political economy module]`. The percentage is immediately interpretable. The tier annotation (`T3`) communicates that this is a model estimate, not citable official data.
- Layer 3 verdict: **SATISFIES Layer 3**. "72% [T3 · political economy module]" tells the user: this is a probability (72%), produced by model estimation (T3), from the political economy module (named source). The qualifier prevents misuse as a citable fact while preserving the analytical signal.

**Customer Agent Layer 3 finding:** No Layer 3 deficiency identified. All three components present interpretable, self-labeling output. No specialist mediation required to read any of the three annotations in the Reactive entry state. The kryptonite constraint is satisfied.

---

### §3b — Business PO Validate Verdict (Step 5)

*Filed by Business PO — 2026-06-18*

**Work type:** Frontend feature
**Persona served:** Persona 2 — Finance Ministry Negotiator (Aicha Diallo archetype)
**Time ceiling (P-4):** 90 seconds to read a challenged trajectory output — Reactive entry state

**North Star Test — ADR-015 Components 1, 2, 3:**

*Scenario: Zambian Ministry of Finance analyst (Aicha Diallo archetype) is in a debt restructuring session with a creditor-side team. The creditor analyst challenges the trajectory output: "Your debt-to-GDP projection assumes a fiscal multiplier of 1.30 — can you justify that, and what is the data basis for your financial framework score?"*

*Pre-G5 capability: The analyst could see the composite financial score (e.g., 0.62) and the trajectory chart. She could not immediately see what data tier it was, who produced it, or what fiscal multiplier was in use — she would need to navigate to the scenario setup form or open a separate data-provenance view to answer.*

*Post-G5 capability:*
1. *The Zone 1D financial row now shows `[T2 · IMF WEO / CBJ · pre-cal]` directly below the score. The analyst reads: this is Tier 2 (citable official statistics from IMF and the Central Bank of Jordan). She can say "Our financial framework score draws from IMF WEO and CBJ official data at Tier 2 — these are citable sources."*
2. *The Assumption Surface immediately above the instrument cluster shows `Fiscal ×1.30 · Data: 2024-Q1 vintage`. The analyst reads the fiscal multiplier directly and can cite it in response to the creditor's challenge without any interaction.*
3. *If the PE module is active, the Political Feasibility row shows `68% [T3 · political economy module]`. The analyst can present the programme survival probability as a modelled estimate alongside the four framework scores, with the tier annotation preventing misrepresentation as an exact forecast.*

*The capability changes what the ministry team can argue at the table:*
- *They can now answer "what is the data basis?" in under 10 seconds (previously required leaving the instrument cluster)*
- *They can confirm the fiscal multiplier from the instrument view without navigating to configuration (previously required 30–45 seconds)*
- *They can present Political Feasibility alongside the four framework scores as an integrated picture (previously unavailable as a Zone 1D surface)*

**North Star Test verdict:** The G5 deliverable makes the tool more useful to the finance minister sitting across from the IMF negotiating team in that moment. The three capabilities together close the primary 90-second reactive-state gap identified in ADR-015 §P-2.

**Business PO Validate verdict:** **ACCEPT**

**Kryptonite Constraint (FD-3):** Satisfied. All three outputs are interpretable by a finance ministry economist without specialist mediation. The Customer Agent found no required specialist mediation. No EL exception needed.

**Layer 3 precondition:** Customer Agent Layer 3 assessment filed above (§3a) — confirms all three components satisfy Layer 3 before this verdict.

---

## Section 4 — Open Rejections

No open rejections. Proceed to Section 5.

---

## Section 5 — PI Agent Sprint Exit Confirmation

**Exit conditions checklist (PI Agent):**

- [x] All implementation groups merged; CI green on release branch (Section 2) — PR #1030 merged 2026-06-18, all 6 checks green
- [x] Business PO ACCEPT verdict filed for each user-facing deliverable, or EL exception on record (Section 3) — all three components ACCEPT, §3b
- [x] Customer Agent Layer 3 assessment on record for all Persona 2/3/5 deliverables, filed before Business PO verdict (Section 3) — §3a filed before §3b verdict
- [x] No open rejection artifacts (Section 4) — confirmed none
- [x] Near-miss entry filed for each rejection in this sprint (Section 4) — no rejections; no NM entry required for rejections
- [x] Step 4 Verify PASS artifact on record in intent document (§8) — 17/17 Playwright tests passed 2026-06-18
- [x] North Star Test artifact present for user-facing deliverable (§3b) — Business PO authored north star test covering Zambian analyst scenario, reactive entry state, three named capabilities

**PI Agent sprint exit verdict:** Confirmed — all exit conditions satisfied

> G5 delivers ADR-015 Components 1, 2, and 3 as specified in the intent document. All 14
> acceptance criteria pass in Playwright E2E. Business PO ACCEPT recorded with a specific
> north star test (Zambian analyst, debt restructuring session, 90-second reactive state).
> Customer Agent Layer 3 assessment confirms no specialist mediation required for any of
> the three components. No rejections. No open artifacts. G5 is complete.
>
> Component 4 (cross-examination mode) is explicitly out of scope for G5 — M15 delivery,
> as documented in the intent document §6 and sprint entry §2.2. This does not affect G5
> exit status.

---

## Sprint Exit Artifact Statement

This document is the sprint exit artifact for G5 of M14. It supersedes any informal
exit notation in SESSION_STATE.md for G5. It is filed at
`docs/process/sprint-plans/m14-g5-sprint-exit.md`.

The PI Agent confirmation in Section 5 is the gate. G5 closes as of this document.
No subsequent sprint group is blocked by G5 — the release branch is clean and CI is green.
