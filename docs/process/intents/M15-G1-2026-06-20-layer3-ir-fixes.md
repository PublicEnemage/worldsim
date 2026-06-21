---
name: M15-G1-layer3-ir-fixes
type: implementation-intent
adr: ADR-015 (Components 1, 3, 4) · ADR-016 (Component 2)
issues: "#1065, #1066, #1068, #1069, #1075"
status: Filed
authored-by: Frontend Architect Agent
authored-date: 2026-06-20
implementing-agent: Frontend Architect Agent
sprint-entry: docs/process/sprint-plans/m15-g1-sprint-entry.md
---

# Implementation Intent: M15-G1 — Layer 3 + IR Fixes

## 1. Source ADR

**ADR:** ADR-015 — Model Legibility Architecture (Evidence Thread Architecture), Components 1, 3, 4  
**ADR:** ADR-016 — Scenario Grounding Architecture, Component 2  
**Status at time of authorship:** Both Accepted 2026-06-16 (PR #998, PR #967)  
**Authored by:** Frontend Architect Agent  
**Date:** 2026-06-20  
**Implementing agent:** Frontend Architect Agent

**Design authority:**
- ADR-015 §Component 4 — Cross-Examination Mode (persistent Layer 3 sentence; G1 delivers the zero-interaction sentence only, not the full interactive mode transformation)
- ADR-015 §Component 1 — Basis Threads (extended to Zone 1A trajectory curves — L0 tier badge; Zone 1D annotations delivered in M14 G5)
- ADR-015 §Component 3 — Programme Survival Probability in Zone 1D (G1 adds the self-interpreting Layer 3 sentence beneath the existing PSP row delivered in M14 G5)
- ADR-016 §Component 2 — Scenario Grounding Strip (disambiguation labels for dual reserve values)
- ADR-015 §Silent Failure Mode — all three component-specific fallback states
- ADR-016 §Silent Failure Mode — grounding strip unavailable state
- IR-001 (#1065), IR-002 (#1066), IR-004 Path A (#1068), IR-005 (#1069), DEMO-099 (#1075) — Independent Review and audience simulation findings from M14 G8

**Prerequisite gates satisfied:**
- G5 COMPLETE 2026-06-18 (PR #1030): ADR-015 Components 1, 2, 3 delivered — Zone 1D annotations, assumption surface, PSP row, Zone 1B full indicator names
- G4 COMPLETE 2026-06-17 (PR #1015–#1018): ADR-016 Component 1 delivered — `/data-quality`, `/initial-state` endpoints in service; GroundingStrip rendering initial-state values
- M14 G5 intent document at `docs/process/intents/M14-G5-2026-06-17-adr015-frontend.md` — consulted for inherited decisions
- All five G1 issues target existing endpoint data: no new backend endpoints required

---

## 2. Persona Trace Elements Targeted

**P-1 — Persona served:**  
Primary: Persona 2 — Finance Ministry Negotiator (Eleni/Aicha archetype). Secondary: Persona 3 — Political Advisor (Andreas archetype) for #1075 PSP sentence specifically. Persona 1 (IMF Programme Analyst — Lucas) reads the same surfaces and must not be degraded. The north star mission: Aicha at the Zambia IMF restructuring table, responding to an IMF challenge within 90 seconds without specialist mediation.

**P-2 — Entry state:**  
Reactive entry state (90-second ceiling, negotiating room context). All five G1 deliverables are zero-interaction persistent surfaces — the analyst reads without taking any action. No preparatory interaction required. ADR-015 §P-2.

**P-3 — Journey reference:**  
- Closes Journey B Step 3 [Near-Term-Gap] (partial — G1 delivers the persistent Zone 1B directive sentence; the full interactive cross-examination mode is a subsequent G-group): the sentence answers "what does this trajectory mean?" at L0, zero interaction.
- Extends Journey F Step 7 (PSP Layer 3 sentence — Persona 3 can brief the Minister from Zone 1D without requiring a separate political economy briefing document).
- Closes IR-001, IR-002, IR-004 Path A, IR-005, DEMO-099 findings from M14 G8 — all five are pre-conditions for the G8 live external demo (#843).

**P-4 — Time/interaction ceiling:**  
All five G1 observable states are present at zero interaction. ADR-015 §P-4: "basis annotation (L0) visible at zero interaction." The Zone 1B directive sentence must be visible without scroll at 1440×900 in the instrument cluster's default view. The PSP sentence must be visible without scroll in Zone 1D at 1440×900. L0 tier badges on Zone 1A trajectory curves must be visible without hover or click.

**P-6 — Negotiating leverage delivered:**  
After G1, Persona 2 can make the following specific arguments from the primary viewport, without specialist translation:

> "Zone 1B shows: Reserve coverage has fallen 2.9 months below the CRITICAL threshold. At current draw rate, full depletion occurs in 4 steps. That is our read — it is computed from T2 IMF BOP data, visible in the confidence badge on the trajectory. Programme survival probability is 65%, meaning there is a 65% chance the programme remains on track through conditionality compliance — that is what the political economy module computes under standard conditionality. The initial reserve position was 3.8 months as of the entry state, which you can see labeled as the entry-state value in the Grounding strip; the 2.9 months is the current simulated position at step 3."

None of this argument was producible from the primary screen before G1. After G1, all five sentences are supported by persistent, zero-interaction on-screen elements.

**P-7 — North star capability delivered:**  
The Zambian Finance Ministry analyst, in the restructuring session, can read the Zone 1B trajectory sentence ("Reserve coverage has fallen 2.9 months below the CRITICAL threshold. At current draw rate, full depletion occurs in 4 steps.") and the PSP sentence ("65% chance of remaining on track through conditionality compliance") without requiring the presenter to translate raw numbers into policy language. This changes Demo 6's dynamic from narrated presentation to self-evident evidence — the screen argues for itself. G1 delivers the persistent-sentence component of ADR-015 Component 4, the Zone 1A L0 badge extension of Component 1, the PSP Layer 3 sentence extension of Component 3, and the Grounding strip disambiguation of ADR-016 Component 2.

---

## 3. Observable Application State

### 3.1 Primary observable state

**#1065 — Zone 1B Layer 3 directive sentence:**  
At viewport 1440×900, with the ZMB ECF scenario loaded and advanced to ≥1 step with at least one active MDA threshold breach: the element `[data-testid="zone-1b-trajectory-sentence"]` exists within the Zone 1B panel, is visible without scroll, and contains a complete directive sentence whose text includes (a) the indicator name or threshold type, (b) a direction and magnitude relative to the threshold floor, and (c) a forward implication (steps to depletion, projected trajectory, or equivalent rate language). Example conforming text: "Reserve coverage has fallen 2.9 months below the CRITICAL threshold. At current draw rate, full depletion occurs in 4 steps." The sentence is not a duplicate of existing label or severity text; it is a distinct element containing new interpretive content.

### 3.2 Secondary observable states

**Secondary state A — #1066: zero consecutive-steps suppression:**  
At step 0, or any Zone 1B state where the top alert's `consecutive_breach_steps` is 0: the text "0 consecutive step" does not appear anywhere within `[data-testid="zone-1b-top-detail"]`. When `consecutive_breach_steps` is ≥1, the element `[data-testid="detail-consecutive"]` displays the accurate non-zero count (e.g., "3 consecutive steps") — not zero.

**Secondary state B — #1068: Zone 1A L0 confidence tier badge:**  
At viewport 1440×900 with the ZMB ECF scenario loaded at any step ≥0: `[data-testid="zone-1a-trajectory"]` contains at least one element matching `[data-testid="zone-1a-l0-badge"]` that is visible in the viewport without interaction. The badge text contains a tier label in the form "T{N}" where N is a digit (e.g., "T2", "[T2]", "T2 ·"). At least one badge per active framework trajectory curve is visible at 1440×900. The badge is not a hover state, tooltip, or popover — it is permanently rendered adjacent to or on the trajectory curve.

**Secondary state C — #1069: Grounding strip dual-value disambiguation:**  
With the ZMB ECF scenario at ≥1 step advanced, with the Grounding strip open (toggle activated): within `[data-testid="grounding-strip"]`, the financial framework section contains two rows (or one row with two value/label groups) for the reserve coverage indicator — one with a label semantically equivalent to "entry-state", "initial", or "step 0" (marking citable primary data), and one with a label semantically equivalent to "current", "model output", or "step N" (marking simulation output). A stakeholder can distinguish which value is the citable T2 source observation and which is the current simulated position without any presenter narration.

**Secondary state D — #1075: PSP Layer 3 sentence in Zone 1D:**  
At viewport 1440×900 with the ZMB ECF scenario loaded with political economy enabled and advanced to ≥1 step: `[data-testid="psp-layer3-sentence"]` exists within `[data-testid="zone-1d-four-framework"]`, is visible without scroll, and contains text that both (a) states the probability value as a percentage and (b) translates that value into a policy-relevant statement about what it means for programme continuation. Example conforming text: "Programme survival probability: 65%. This means the programme has a 65% chance of remaining on track through conditionality compliance." The sentence is not a hover state or tooltip — it is a persistent L0 element.

### 3.3 Silent failure detection

**#1065 (Zone 1B sentence):** If the trajectory data needed to compute the sentence is unavailable or the MDA alert returns no consecutive-step count, `[data-testid="zone-1b-trajectory-sentence"]` renders with fallback text (e.g., "Trajectory analysis unavailable for this alert.") rather than being absent from the DOM. An absent element is indistinguishable from "not implemented"; a present element with fallback text is a transparent disclosure. Detection: QA mock-returns an alert with `consecutive_breach_steps = null` and asserts that `zone-1b-trajectory-sentence` is present in DOM and does not have empty text content.

**#1069 (Grounding strip):** If the trajectory endpoint is unavailable (current step data cannot be fetched), the Grounding strip shows the entry-state value only with the "entry-state" label still visible (not removed), and a muted note such as "Current simulation value unavailable." The label must remain present even when the simulation value is absent — otherwise the stakeholder has no basis for understanding what the single visible value represents.

**#1075 (PSP sentence):** If the PSP computation returns `null` (political economy module error), `[data-testid="psp-layer3-sentence"]` renders fallback text consistent with ADR-015 §Silent Failure Mode for Component 3 (e.g., "Programme survival probability unavailable — computation error.") rather than being absent. Consistent with the existing Component 3 silent failure (the Political Feasibility row itself shows "— [computation error]" rather than being suppressed).

---

## 4. Acceptance Criteria

**AC-1:** In the ZMB ECF scenario at viewport 1440×900 with ≥1 step advanced and at least one active MDA threshold breach, `[data-testid="zone-1b-trajectory-sentence"]` is visible within the Zone 1B panel without scroll.

**AC-2:** In the same ZMB state as AC-1, the text content of `[data-testid="zone-1b-trajectory-sentence"]` is not empty, does not duplicate existing severity label text, and contains at minimum one numerical value and one forward-projection phrase (e.g., contains "steps" or "months" or "rate" — something that tells the analyst what the trajectory implies, not just what the current state is).

**AC-3:** In the ZMB ECF scenario at step 0 (no steps advanced), the text "0 consecutive step" does not appear anywhere inside `[data-testid="zone-1b-top-detail"]`.

**AC-4:** In the ZMB ECF scenario with the scenario advanced to ≥3 steps with a consecutively breached threshold: `[data-testid="detail-consecutive"]` shows a value ≥1 (not zero); and the displayed count is consistent with the actual breach streak — not a static placeholder.

**AC-5:** At viewport 1440×900 with the ZMB ECF scenario loaded at any step, `[data-testid="zone-1a-trajectory"]` contains at least one `[data-testid="zone-1a-l0-badge"]` element that is visible in the viewport without any interaction; the element's text content matches the pattern `T\d` (letter T followed by a digit). Playwright: `expect(page.locator('[data-testid="zone-1a-l0-badge"]').first()).toBeVisible()`.

**AC-6:** With the ZMB ECF scenario at ≥1 step advanced and the Grounding strip opened, `[data-testid="grounding-strip"]` contains an element whose text includes a label semantically indicating "initial", "entry-state", or "step 0" adjacent to (or within the same row as) the reserve coverage months value from the `/initial-state` endpoint.

**AC-7:** In the same Grounding strip state as AC-6, `[data-testid="grounding-strip"]` contains a second distinct element for reserve coverage whose text includes a label semantically indicating "current", "model output", "simulation", or "step N" adjacent to (or within the same row as) a simulated reserve coverage value that differs from the entry-state value.

**AC-8:** At viewport 1440×900 with the ZMB ECF scenario loaded with political economy enabled and advanced to ≥1 step, `[data-testid="psp-layer3-sentence"]` is visible within `[data-testid="zone-1d-four-framework"]` without scroll.

**AC-9:** The text content of `[data-testid="psp-layer3-sentence"]` contains both a probability percentage value and at least one phrase that contextualises its meaning for programme continuation — the word "programme" and either "chance", "probability", "remain", or "track" must all appear in the sentence text.

**AC-10:** In a mock scenario where the top Zone 1B alert has `consecutive_breach_steps = null` or trajectory computation fails, `[data-testid="zone-1b-trajectory-sentence"]` is present in the DOM with non-empty fallback text — it does not vanish silently.

**AC-11:** In a mock scenario where the trajectory endpoint is unavailable when the Grounding strip is opened, the entry-state value row still shows its "entry-state" / "initial" label — the disambiguation label is not removed when the simulation-side value is absent.

---

## 4b. Visual Spec (before/after)

**AC-1/AC-2 (Zone 1B trajectory sentence)**

Before — current Zone 1B top detail slot (no directive sentence):
```
┌─ Zone 1B top detail ─────────────────────────────────────────────┐
│ TERMINAL  Reserve Coverage Months                                  │
│ Current 2.908 / Floor 2.500                                       │
│ BREACH ACTIVE  ·  8 consecutive steps         ← existing elements │
│ [T2 · Citable: peer-reviewed / official statistics]               │
│                                                 ← NO SENTENCE HERE│
└───────────────────────────────────────────────────────────────────┘
```

After — Zone 1B top detail slot with directive sentence:
```
┌─ Zone 1B top detail ─────────────────────────────────────────────┐
│ TERMINAL  Reserve Coverage Months                                  │
│ Current 2.908 / Floor 2.500                                       │
│ BREACH ACTIVE  ·  8 consecutive steps                             │
│ [T2 · Citable: peer-reviewed / official statistics]               │
│ ────────────────────────────────────────────────────────          │
│ Reserve coverage has fallen 0.408 months below the CRITICAL        │
│ threshold. At current draw rate, full depletion occurs in 4 steps.│
│ ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ │
│                        THIS IS THE SENTENCE (data-testid above)   │
└───────────────────────────────────────────────────────────────────┘
```

---

**AC-3/AC-4 (#1066 — consecutive steps)**

Before — "0 consecutive steps" shown at step 0 breach:
```
BREACH ACTIVE  ·  0 consecutive steps
                  ^^^^^^^^^^^^^^^^^^^ BUG: zero should be suppressed
```

After — zero suppressed; positive count shown accurately:
```
BREACH ACTIVE                       ← no consecutive count when zero
                                    (no "· 0 consecutive steps" text)

BREACH ACTIVE  ·  3 consecutive steps  ← only shown when count ≥ 1
```

---

**AC-5 (#1068 — Zone 1A L0 confidence tier badge)**

Before — trajectory curve with no persistent tier badge:
```
 1.0 ─────────────────────────────── Financial ────  ← no tier badge
 0.8 ·············
 0.6             ·········
     step 0    step 4    step 8
```

After — tier badge visible adjacent to trajectory curve rightmost point:
```
 1.0 ─────────────────────────────── Financial ─[T2] ← badge always visible
 0.8 ·············
 0.6             ·········
     step 0    step 4    step 8
```

Badge text: `T{N}` or `[T{N}]` where N is the confidence tier of the last step.  
data-testid: `zone-1a-l0-badge` (one per active framework curve).

---

**AC-6/AC-7 (#1069 — Grounding strip disambiguation)**

Before — Grounding strip with no label distinguishing entry-state from simulation:
```
FINANCIAL
  Reserve Coverage Months:  3.8 months · CBJ 2023-Q4 · T2
  ────────────────────────────────────────────────────
  (no current value; user sees "3.8" and Zone 1B shows "2.9" — no explanation)
```

After — two labeled value contexts:
```
FINANCIAL  ·  Initial conditions (step 0 · source-cited data)
  Reserve Coverage Months:  3.8 months · CBJ 2023-Q4 · T2
  ────────────────────────────────────────────────────
FINANCIAL  ·  Current trajectory (step 3 · model output)
  Reserve Coverage Months:  2.9 months
```

Acceptable variant: the distinction may be achieved with row-level labels, section headers, or inline badges rather than the exact two-section layout shown above, provided the QA reviewer can identify which value is entry-state (source-cited) and which is current simulation output without reading any code.

---

**AC-8/AC-9 (#1075 — PSP Layer 3 sentence)**

Before — PSP row in Zone 1D, value only:
```
Political Feasibility  65% [T3 · political economy module]
                                               ← NO SENTENCE
```

After — PSP row with Layer 3 sentence below:
```
Political Feasibility  65% [T3 · political economy module]
Programme survival probability: 65%. This means the programme has a
65% chance of remaining on track through conditionality compliance.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
data-testid="psp-layer3-sentence"
```

---

## 5. Kryptonite Constraint Check

**Does this implementation's primary observable state require specialist mediation for Persona 2 to act on it in the Reactive entry state (90-second ceiling)?**

`[x]` No — the observable state is interpretable by Persona 2 without an analyst translating it.

**Rationale per deliverable:**

- **#1065 (Zone 1B sentence):** The sentence explicitly states the threshold breach magnitude and forward trajectory in plain language. A finance ministry economist can read "Reserve coverage has fallen 2.9 months below the CRITICAL threshold. At current draw rate, full depletion occurs in 4 steps." and make the argument at the table without a methodology specialist present.
- **#1066 (zero suppression):** Removing the misleading "0 consecutive steps" prevents a stakeholder from asking "why zero?" — a question that would require specialist explanation. Suppression avoids the question entirely.
- **#1068 (Zone 1A badge):** "[T2]" on a trajectory curve tells the ministry analyst "this is Tier 2 — you can cite it" without requiring a data specialist to confirm the provenance. The tier badge is the same system already visible in Zone 1D; extending it to Zone 1A makes the read consistent.
- **#1069 (Grounding strip):** Labeled "initial state" / "model output" values mean Aicha can answer "is the 3.8 or the 2.9 the figure we submitted?" without a briefing note. The labels eliminate the ambiguity that produced DEMO-100 (presenter required to interrupt narration to explain the two values).
- **#1075 (PSP sentence):** "65% chance of remaining on track" translates a probability score into a statement Andreas (political advisor) can use when briefing the Minister. "65% [T3]" alone requires knowing the political economy model's scale; the sentence does not.

---

## 6. Out of Scope

| Out-of-scope item | Rationale |
|---|---|
| ADR-015 Component 4 interactive cross-examination mode (full `?` / "Defend" toggle transforming all Zone 1 elements) | G1 delivers the zero-interaction persistent sentence only. The full mode transformation with inline Zone 1D component decomposition is a subsequent G-group. |
| ADR-015 Component 4 keyboard shortcut or "Defend" button | Same as above — interactive mode not in G1 scope. |
| ADR-016 Component 3 — Fidelity contextualisation (analogous-case content in Fidelity panel) | G4 scope. |
| ADR-016 Component 1 — Data quality preview at scenario creation (#975) | G4 scope. |
| Zone 1A ADR-017 implementation (Phases 2–4 — information architecture redesign of Zone 1A) | G2 scope; requires ADR-017 acceptance. |
| Zone 1B sentence formatting for non-breach states (scenario at step 0 with no active alerts) | When no alert is active, Zone 1B shows "No active threshold breaches." The trajectory sentence element is absent in the no-alert state — the sentence is only present when a top alert exists. |
| New backend API endpoints | G1 is frontend-only. All required data comes from `/initial-state`, `/trajectory`, and `/data-quality` endpoints delivered in M14 G3 and G5. |
| Walkthrough and narration document updates (DEMO-123/124/129) | G5 scope. |
| Any new data computation (the Layer 3 sentence is derived from existing alert fields: `consecutive_breach_steps`, `current_value`, `floor_value`, indicator name) | The sentence construction is client-side logic from existing API response fields. |

---

## 7. Test Authorship Obligation

**QA Lead:** QA Lead Agent  
**Test authorship deadline:** Before any G1 implementation PR is opened  
**Test file location:** `frontend/tests/e2e/m15-g1-layer3-ir-fixes.spec.ts`  
**Relevant acceptance criteria:** AC-1 through AC-11 (§4 above)

**Test authorship notes:**
- AC-1/AC-2 require a ZMB scenario fixture with ≥1 step advanced and an active breach. Use the ZMB ECF fixture pattern from M14 G8 demo tests.
- AC-3/AC-4 require a ZMB scenario at step 0. Verify `zone-1b-top-detail` text content does not include "0 consecutive step".
- AC-5 requires asserting `zone-1a-l0-badge` presence within `zone-1a-trajectory`. Badge visibility must be confirmed at 1440×900 viewport.
- AC-6/AC-7 require opening the Grounding strip (click `grounding-strip-toggle`) and then asserting two distinct value contexts for reserve coverage. Use the route-mock pattern from M14 G5 for `/initial-state` and mock the `/trajectory` current step response for the simulation value.
- AC-8/AC-9 require a ZMB scenario with political economy enabled. Use `modules_config.political_economy.enabled = true` in the fixture.
- AC-10 requires mocking a failed trajectory response and asserting `zone-1b-trajectory-sentence` fallback text is present.
- AC-11 requires mocking a failed `/trajectory` response while `/initial-state` succeeds, asserting the entry-state label persists in the Grounding strip.
- NM-045 string-presence rule: all text-content assertions must use `.toContainText()` or equivalent string-presence check — not exact equality matching — to avoid brittle failures on minor text wording changes.

**QA Lead acknowledgment:**  
`[x]` QA Lead: Tests for AC-1 through AC-11 authored and filed. 2026-06-20 — `frontend/tests/e2e/m15-g1-layer3-ir-fixes.spec.ts`

---

## 8. Step 4 Verify record

**Verifying agent:** Frontend Architect Agent  
**Date:** 2026-06-21  
**Method:** Playwright E2E suite — `frontend/tests/e2e/m15-g1-layer3-ir-fixes.spec.ts`  
**Dev server:** Docker Vite server (localhost:5173) against live backend (localhost:8000)

**Result: 11/11 ACs PASS**

| AC | Result | Observable state confirmed |
|---|---|---|
| AC-1 | PASS | `zone-1b-trajectory-sentence` visible at 1440×900 without scroll when CRITICAL breach active |
| AC-2 | PASS | Sentence contains numerical reserve value and consecutive step count phrase |
| AC-3 | PASS | `0 consecutive step` text absent when `consecutive_breach_steps = 0` |
| AC-4 | PASS | `detail-consecutive` shows accurate count (3) when `consecutive_breach_steps = 3` |
| AC-5 | PASS | `zone-1a-l0-badge` visible in trajectory at 1440×900, text matches `/T\d/` pattern |
| AC-6 | PASS | Grounding strip contains "Initial conditions" label adjacent to entry-state reserve value (3.8) |
| AC-7 | PASS | Grounding strip contains "Current trajectory" label — two value contexts distinguishable |
| AC-8 | PASS | `psp-layer3-sentence` visible at 1440×900 without scroll when PE enabled |
| AC-9 | PASS | Sentence contains probability percentage and "programme/chance/remain" contextualisation |
| AC-10 | PASS | `zone-1b-trajectory-sentence` present with fallback text when `consecutive_breach_steps = null` |
| AC-11 | PASS | Entry-state label persists in grounding strip when trajectory endpoint fails (500) |

**Implementation note (NM-046):** AC-7 revealed a crash path — `getIndicatorDisplayNameAny(undefined)` reached `formatFallback(undefined)` → TypeError → React tree unmount → toggle button detached. Root cause: QA test mock factory used `alert_id`/`indicator_id` field names (matching the test's `MDAAlert` interface) instead of `mda_id`/`indicator_key` (matching `RawMDAAlert`). Fix: one-line null guard at `getIndicatorDisplayNameAny` entry point (PR #1098, commit `a7c1d67`). NM-046 filed.

`[x]` Step 4 Verify: COMPLETE — all 11 ACs confirmed in running application. 2026-06-21

---

## 9. Step 5 Validate record

> *To be filled by the Business PO at Step 5 — Validate.*

`[ ]` Pending Business PO validation.
