---
name: M18-G4-control-plane-column
type: implementation-intent
issues:
  - "#1217 — Mode 3 render optimization (Recharts memoization, lazy ControlPlane)"
  - "#TBD — Control Plane Column implementation (to be filed with G4 sprint entry)"
status: "Filed — implementation PR blocked until ADR-019 accepted and G1+G2 exits confirmed (see §0)"
authored-by: Frontend Architect Agent
authored-date: 2026-06-28
implementing-agent: "Frontend Architect Agent (frontend); Computation Engine Agent (backend shock endpoint)"
sprint-entry: "Not yet filed — pending ADR-019 acceptance and G1+G2 exits (CLAUDE.md §Wave 2 Entry Gates)"
adr-reference: "ADR-019 (ARCH-013 ASSIGNED) — Control Plane Column; required before implementation PR opens"
governing-adrs:
  - "ADR-008 (UX Architecture — ACCEPTED) — six-type shock taxonomy authority; Mode 2/3 column zone sizing"
  - "ADR-019 (ARCH-013 ASSIGNED) — Control Plane Column; provides shock parameter schemas, mode transition spec, EX-001 resolution path"
gd-source:
  - "docs/process/intents/M18-GD-2026-06-26-control-plane-scope-decision.md — Decisions 1–3 EL-approved; Decision 4 (GrowthShock) pending"
release-branch: release/m18
bpo-acceptance-required: "Yes — new Mode 2+3 user-facing interaction (screen recording of Demo 7 Act 1 flow required)"
customer-agent-l3-required: "Yes — Personas 2 and 5 (at sprint exit, per sprint plan §Exit Conditions G4)"
ux-ui-mockups-required: "Yes — UX mockup (column layout, mode transition), UI mockup (blue/orange visual system, form layouts) — required before implementation PR opens"
ex-001-reference: "docs/compliance/exceptions.md §EX-001 — resolution recorded at G4 exit per Decision 3"
sprint-journal: "TBD — opened by PM Agent at sprint entry"
---

# Implementation Intent: M18-G4 — Control Plane Column

> **Pre-implementation prerequisites (all required before any implementation PR opens):**
> - [ ] ADR-019 accepted (separate-session UX Designer sign-off, Tier 1, NM-042 compliance) — **BLOCKING**
> - [ ] G1 and G2 exits confirmed by PI Agent (InstrumentCluster.tsx conflict avoidance) — **BLOCKING**
> - [ ] G4 sprint entry filed and EL-approved — **BLOCKING**
> - [ ] UX mockup filed (§8a) — required before implementation PR
> - [ ] UI mockup filed (§8b) — required before implementation PR
> - [ ] UX/UI panel review complete (UX Designer ACCEPT, Customer Agent ACCEPT, BPO ACCEPT) — required before implementation PR
> - [ ] `docs/schema/api_contracts.yml` updated with shock injection endpoint shape — in implementation PR
> - [ ] EX-001 resolution path recorded in `docs/compliance/exceptions.md §EX-001` before G4 begins (PI Agent process condition from Decision 3)
>
> **This intent is filed early** (before ADR-019 authorship) to establish the specification for UX/UI
> mockup work and to enable test authorship as soon as ADR-019 is accepted. The scope is derived
> from the EL-approved GD design package (Decisions 1–3, Scope Decision Document 2026-06-26).
> Decision 4 (GrowthShock as seventh shock type) is pending EL approval — see §10.

---

## 0. Implementation Constraints

*Authority: GD Scope Decision Document (EL-approved 2026-06-26) and ADR-019 (to be accepted before
implementation begins). These constraints are not design preferences — they follow from EL decisions
and the GD panel findings. Any implementation diverging from these constraints is a process
deviation.*

1. **Two-component architecture (Decision 1 panel condition):** Column 3 is implemented as two
   distinct React components — `Mode2ColumnSurface` and `ControlPlane` — with conditional rendering
   in `InstrumentCluster.tsx`. These are NOT conditional branches within a single component. This
   constraint enables the lazy mounting required for render optimization (EX-001 / Decision 3).

2. **Activation button label (Customer Agent kryptonite finding, Decision 1):** The Mode 2 column 3
   activation button label is `"Enter Active Control"` — not `"Enter Mode 3"`. `"Mode 3"` is
   internal technical terminology. Personas 2 (Eleni) and 5 (Aicha) interpret it as jargon.
   Any implementation using `"Enter Mode 3"` as a button label is a kryptonite violation and will
   REJECT at Customer Agent Layer 3 review.

3. **Mode 2 column visual treatment (UX Designer ruling, Decision 1):** The Mode 2 column (`Mode2ColumnSurface`)
   has a subdued visual treatment signaling "pre-active" state — blue border, reduced-opacity content.
   This signals the zone is real and available without signaling it is currently active.
   ADR-019 will specify the exact border colour tokens.

4. **Shock taxonomy scope — six types in M18 (Decision 2):** Form 2 ships with all six ADR-008
   shock types: `ElectionShock`, `CurrencyAttack`, `CreditorDefection`, `GeopoliticalShock`,
   `NaturalDisaster`, `ContagionShock`. Parameter schemas and data dependency status for all six
   are specified in ADR-019 before G4 sprint entry. `CreditorDefection` (creditor class taxonomy)
   and `ContagionShock` (linkage approach) are unresolved at the CE Agent level — ADR-019 resolves
   them. `GrowthShock` (seventh type) is pending Decision 4 EL approval — see §10.

5. **Render optimization in the same PR as column restructuring (Frontend Architect finding):**
   Recharts memoization and lazy `ControlPlane` mounting must be implemented in the same G4 PR as
   the column restructuring. A separate optimization-only PR on a component being actively
   restructured creates rebase risk. The two-component architecture (constraint 1) enables lazy
   mounting by construction — `ControlPlane` only mounts when the mode transitions to Mode 3.

6. **`ScenarioInstrumentCluster.tsx` bottom-bar removal:** The current `ControlPlane` rendering
   at line 983–989 of `ScenarioInstrumentCluster.tsx` (G6b pattern, Issue #753) is removed in G4.
   The ControlPlane moves to the `InstrumentCluster.tsx` column 3. This is the primary structural
   change.

7. **testid conflict resolution:** `ControlPlane.tsx` currently uses `data-testid="zone-control-plane"`
   on its root element, which conflicts with the `data-testid="zone-control-plane"` on the
   InstrumentCluster column 3 container. G4 resolves this: the column container retains
   `data-testid="zone-control-plane"`; the ControlPlane component root uses
   `data-testid="control-plane"`.

---

## 1. Source

**Issues:** #1217 (render optimization — Recharts memoization, lazy mounting) + TBD control plane
implementation issue (filed with G4 sprint entry).

**GD source documents:**
- `docs/process/intents/M18-GD-2026-06-26-control-plane-scope-decision.md` — EL Decisions 1–3 (Decisions 1–3 approved 2026-06-26; Decision 4 pending)
- `docs/process/intents/M18-GD-2026-06-26-control-plane-scope-decision-deliberation.md` — panel findings for Decisions 1–3

**Governing ADR:** ADR-019 (ARCH-013 ASSIGNED) — must be accepted before implementation begins.
ADR-019 will specify: Mode 2 column content and interaction spec, shock type parameter schemas and
data dependency tiers, EX-001 resolution path, and information hierarchy §Control Plane Reserved
Zone amendment.

**Demo 7 anchor:** Act 1 — Senegal (SEN), Mode 3 Active Control. The analyst must be able to:
(1) see the scenario summary in Mode 2 column 3; (2) activate Mode 3 via "Enter Active Control";
(3) apply a fiscal counter-proposal via Form 1; (4) observe the live A/B trajectory comparison in
Zone 1A; (5) read the causal attribution in Zone 1B for the counter-scenario. All five steps must
complete in ≤60 seconds from Mode 2 loaded state. The outcome may be CLEAR (configuration avoids
0.40 floor) or CRITICAL at a later step — both are valid Demo 7 answers.

**G1 dependency note:** The A/B trajectory comparison in Zone 1A (AC-G4-C) benefits from G1's CI
band ribbons, but is not blocked by G1 — the baseline vs. counter-scenario trajectory
differentiation is a Mode 3 feature independent of uncertainty bands. G4 must not
modify `TrajectoryView.tsx` in ways that conflict with G1's CI band rendering. The Frontend
Architect verifies this at PR submission; PM Agent confirms merge order at G4 exit.

---

## 2. Persona Trace

**P-1 — Personas served:**

| Persona | Entry state | Role in G4 |
|---|---|---|
| Eleni Papadimitriou (Persona 2 — Finance Ministry Negotiator) | Active Control (live negotiation session, Mode 3 running) | Applies Form 1 (fiscal counter-proposal); observes A/B trajectory; reads Zone 1B causal attribution |
| Eleni Papadimitriou (Persona 2) | Preparatory (evening before, scenario configuration review) | Reads Mode 2 column scenario summary; intentionally transitions to Mode 3 |
| Aicha Mbaye (Persona 5 — Finance Minister) | Demonstrative (watching analyst work) | Sees "Enter Active Control" button label; reads A/B trajectory without analyst interpretation |
| Lucas Ferreira (Persona 1 — Programme Analyst) | Exploratory (shock scenario construction) | Uses Form 2 shock injection; reads history list of applied interventions; audits shock parameter choices |

**P-2 — Entry states and time ceilings:**

- Preparatory: Scenario loaded in Mode 2; Persona 2 reviewing summary in column 3. No time ceiling on the review — but the transition to Mode 3 must be a single visible, intentional affordance.
- Active Control: Mode 3 is live; Form 1 is applied. ≤60 seconds from Mode 2 loaded state to A/B trajectory visible in Zone 1A. This ceiling covers: read Mode 2 summary → click "Enter Active Control" → enter fiscal adjustment in Form 1 → click Apply → observe trajectory.
- Demonstrative: Persona 5 watching Persona 1 or 2 operate. No interaction required from Persona 5 — she observes. The column content and trajectory must be interpretable in ≤30 seconds of observation without narration.

**P-3 — Journey step:** Journey C (Mode 3 Active Control flow) — Step 1 (Mode 2 scenario loaded → column 3 shows summary) through Step 4 (Form 1 applied → A/B trajectory visible → Zone 1B causal attribution read). Journey C is updated as Artifact 7 (#1361) in the GD design package — the specific step numbering follows that update.

**P-4 — Time/interaction ceiling:**

- Mode 2 → Mode 3 transition: one click ("Enter Active Control")
- Form 1 apply: ≤3 interactions (value entry + Apply click; optional branch step adjustment)
- A/B trajectory visible: immediately on Apply (no reload, no navigation)
- ≤60 seconds total from Mode 2 loaded to counter-trajectory visible

**P-6 — Negotiating leverage (Persona 2):**
Eleni can say at the table: *"We ran our counter-proposal through the model live. Under the IMF-proposed conditions, the bottom quintile crosses the 0.40 poverty floor at step 4. Under our fiscal adjustment — reducing the primary surplus target by 1.5 percentage points at step 3 — the crossing is pushed to step 8, within the programme window where our own reform implementation kicks in. The tool is open source and our methodology is public. If you want to contest the calibration, the parameters are in the repository."*

Before G4: Eleni can run Mode 3 only through the bottom-bar ControlPlane (which appears to be a technical appendage, not a primary instrument). After G4: the control plane is column 3 — a co-primary instrument at the same visual weight as Zone 1A and Zone 1B.

**P-7 — North star capability delivered:**
The Senegalese Finance Ministry's analyst can apply a specific fiscal counter-proposal in Mode 3 and observe in real time whether it avoids the bottom quintile poverty floor crossing — with the counter-trajectory visible as a distinct second curve in Zone 1A alongside the baseline, and the causal attribution readable in Zone 1B without any scroll, navigation, or additional interaction. The control plane is a visible co-primary instrument at the negotiating table, not a bottom-bar appendage.

---

## 3. Observable Application State

### 3.1 Primary observable state

**In Mode 3 with the Senegal Article IV scenario loaded and Form 1 applied (fiscal adjustment entered and Apply clicked):**

Zone 1A shows two trajectory curves simultaneously — `[data-testid="trajectory-baseline"]` (muted, lower opacity) and `[data-testid="trajectory-counter"]` (highlighted, full opacity, colour-differentiated) — visible at 1280×800 without scroll, navigation, or interaction. The fork point between curves is visible at the step at which Form 1 was applied. Both curves are present in the same Zone 1A panel; no drawer, no tab, no navigation to reach the comparison.

Column 3 of InstrumentCluster shows `[data-testid="control-plane"]` with the orange visual system active (orange left border, orange Apply button). `[data-testid="control-plane-form1"]` is the active form and is visible without tab interaction.

### 3.2 Secondary observable states

**State A — Mode 2 column 3 populated:**
In Mode 2 with any scenario loaded, column 3 of InstrumentCluster shows `[data-testid="mode2-column-surface"]` with: scenario name, entity ISO code, calibration vintage, and run horizon displayed as read-only text. `[data-testid="enter-active-control-btn"]` is present with label text `"Enter Active Control"` (exact string — no variant). No editable form fields are present. The column has blue left border and subdued content (per visual system spec to be finalised in ADR-019 and UX/UI mockups). The ghost text "Control plane (Mode 3)" (current state) is absent.

**State B — Form 2 shock types accessible:**
In Mode 3, clicking the Form 2 tab renders `[data-testid="control-plane-form2"]` with shock type selectors for all six ADR-008 types: `ElectionShock`, `CurrencyAttack`, `CreditorDefection`, `GeopoliticalShock`, `NaturalDisaster`, `ContagionShock`. Each type has a `[data-testid="shock-type-{type}"]` selector (e.g., `data-testid="shock-type-election-shock"`). A shock injection applied via Form 2 produces a branched trajectory in Zone 1A using the same A/B pattern as Form 1.

**State C — History list present:**
In Mode 3 after any Form 1 or Form 2 intervention is applied, `[data-testid="control-plane-history"]` is present and shows at least one entry. Each entry shows the intervention type and the step at which it was applied. The history list is visible in the column without scroll at 1280×800 when one or two entries are present.

**State D — ControlPlane not in bottom-bar position:**
In Mode 3, no element with the purple bottom-bar visual treatment (`background: "#f8f4ff"`, `borderTop: "2px solid #8b5cf6"`) is rendered below Zone 1D. The ScenarioInstrumentCluster.tsx Mode 3 conditional rendering block (lines 983–989) is removed. The ControlPlane content exists only in InstrumentCluster column 3.

### 3.3 Silent failure detection

**Silent failure — Mode 2 column 3 empty (Mode2ColumnSurface fails to mount):**
Column 3 in Mode 2 shows the ghost text `"Control plane (Mode 3)"` (current state) or is visually empty. The "Enter Active Control" button is absent. Observable via `data-testid="mode2-column-surface"` absent from DOM.

**Silent failure — ControlPlane not in column 3 (column population fails):**
In Mode 3, column 3 shows only the reserved-zone ghost text, and the purple bottom-bar ControlPlane re-appears at the foot of ScenarioInstrumentCluster. Observable via: `data-testid="control-plane"` absent from inside `data-testid="zone-control-plane"`; AND `data-testid="zone-control-plane"` (ControlPlane.tsx root element, now renamed `control-plane`) present in the bottom-bar position.

**Silent failure — A/B trajectory absent (branch computation fails):**
Zone 1A shows only a single trajectory curve after Form 1 Apply. Observable via: `data-testid="trajectory-counter"` absent from Zone 1A DOM after Apply is triggered. The "Apply" button re-enables immediately without visible trajectory change.

**Silent failure — MV-002 performance regression (render optimization absent):**
Mode 3 full component set renders in >100ms on ProBook hardware after G4 implementation. Observable via `npm run profile:mode3` local gate at G4 exit — the implementing agent records the measurement in the PR description. A measurement above 100ms triggers the "Won't Fix" resolution path per Decision 3.

---

## 4. Acceptance Criteria

*Each criterion is testable from the running application without reading implementation code.*

**AC-G4-A (E2E — Mode 2 column 3 populated with scenario summary and activation button):**
In Mode 2 with any scenario loaded, `[data-testid="mode2-column-surface"]` is present in the DOM within `[data-testid="zone-control-plane"]`. The text content of the element includes the active entity's ISO code (e.g., "SEN"). `[data-testid="enter-active-control-btn"]` has `textContent === "Enter Active Control"` (exact match). `[data-testid="enter-active-control-btn"]` does NOT contain the substring "Mode 3".
*Source: §3.2 State A + Decision 1 Customer Agent kryptonite finding*

**AC-G4-B (E2E — "Enter Active Control" transitions to Mode 3 column):**
When `[data-testid="enter-active-control-btn"]` is clicked in Mode 2, `[data-testid="mode2-column-surface"]` is removed from the DOM and `[data-testid="control-plane"]` appears within `[data-testid="zone-control-plane"]`. `[data-testid="control-plane-form1"]` is visible without any additional interaction (tab click, scroll, navigation). The column visual treatment changes from blue to orange.
*Source: §3.1 + §3.2 State A + Decision 1 + Constraint 1 (two-component architecture)*

**AC-G4-C (E2E — Form 1 Apply produces A/B trajectory in Zone 1A):**
In Mode 3 with the Senegal Article IV fixture loaded, when a fiscal adjustment is entered in `[data-testid="control-plane-form1"]` and `[data-testid="apply-control-change"]` is clicked, then: `[data-testid="trajectory-baseline"]` AND `[data-testid="trajectory-counter"]` are both present in `[data-testid="zone-1a-trajectory"]`. Both elements are visible (non-zero dimensions, not `display:none`) without any additional click, scroll, or navigation.
*Source: §3.1 + §P-7*

**AC-G4-D (E2E — Form 2 shock type selectors present):**
In Mode 3, the Form 2 tab is clickable and renders `[data-testid="control-plane-form2"]`. The following testids are present within the form: `data-testid="shock-type-election-shock"`, `data-testid="shock-type-currency-attack"`, `data-testid="shock-type-creditor-defection"`, `data-testid="shock-type-geopolitical-shock"`, `data-testid="shock-type-natural-disaster"`, `data-testid="shock-type-contagion-shock"`. [If Decision 4 is approved before implementation: `data-testid="shock-type-growth-shock"` is also present.]
*Source: §3.2 State B + Decision 2*

**AC-G4-E (E2E — history list present after intervention):**
In Mode 3 after `[data-testid="apply-control-change"]` is clicked at least once, `[data-testid="control-plane-history"]` is present and contains at least one child element. The child element's text content includes the intervention step number as a numeral.
*Source: §3.2 State C + Sprint Plan BPO consultation §Demo 7 Act 1 minimum*

**AC-G4-F (E2E — bottom-bar ControlPlane absent in Mode 3):**
In Mode 3, no element with `style.background === "rgb(248, 244, 255)"` (the current purple `#f8f4ff` background) is present in the DOM that is positioned below Zone 1D. Alternatively: no element with `data-testid="control-plane"` appears as a direct child of `ScenarioInstrumentCluster` at the foot of the component tree (i.e., outside `data-testid="zone-control-plane"`).
*Source: §3.2 State D + Constraint 6*

**AC-G4-G (E2E — Mode 2 column 3 visible at 1280×800 without scroll):**
In Mode 2 at viewport 1280×800, `[data-testid="mode2-column-surface"]` has a bounding box entirely within the viewport (right edge ≤ 1280px, bottom edge ≤ 800px) without any scroll event having fired. The column is the rightmost of three columns in InstrumentCluster.
*Source: §3.2 State A + ADR-008 column sizing (280px reserved)*

**AC-G4-H (performance — MV-002 measurement at G4 exit):**
On ProBook hardware (no CPU throttle), `npm run profile:mode3` reports Mode 3 full component set render time ≤ 100ms. This is a local developer gate, not a Playwright assertion — the implementing agent records the measurement verbatim in the G4 implementation PR description. A measurement above 100ms triggers the Decision 3 "Won't Fix" resolution path; the implementing agent documents this in the PR description, EX-001 is closed Won't Fix, and AC-009 is removed from the CI suite permanently.
*Source: #1217 + Decision 3 + Constraint 5*

**AC-G4-I (backend — shock injection endpoint smoke test):**
`POST /api/v1/scenarios/{id}/branch/shock` (or the endpoint path specified in ADR-019) with a valid `ElectionShock` payload (`inject_at_step: 3`) against the Zambia baseline scenario returns HTTP 200 with a trajectory response that diverges from the baseline at step 3 (composite score at step 3+ differs from the unshocked baseline by a non-zero amount). Response body includes `shock_type` field echoing the injected type.
*Source: §3.2 State B backend + Decision 2*

---

## 4b. Visual Spec (before/after)

*UX Designer authors formal UX and UI mockups (§8) before implementation PR opens. This section
provides the design specification baseline that the formal mockups must satisfy.*

**AC-G4-A / AC-G4-B (before — Mode 2 column 3, current empty reserved zone):**
```
Viewport: 1280×800 | Zone: InstrumentCluster Column 3 | data-testid="zone-control-plane"

╔══════════════════════════════╗
║                              ║
║                              ║
║                              ║
║                              ║
║                              ║
║                              ║
║                              ║
║   Control plane (Mode 3)     ║  ← ghost text, position: absolute, bottom: 16,
║                              ║     fontSize: 11, color: rgba(0,0,0,0.25)
╚══════════════════════════════╝

No data-testid="mode2-column-surface"
No "Enter Active Control" button
```

**AC-G4-A / AC-G4-B (after — Mode 2 column 3, Mode2ColumnSurface):**
```
Viewport: 1280×800 | Zone: InstrumentCluster Column 3 | data-testid="mode2-column-surface"

╔══════════════════════════════╗  ← blue left border (pre-active state)
║  SCENARIO SUMMARY            ║     subdued content (exact tokens in ADR-019 / §8b)
║  Senegal — Article IV 2024   ║
║  SEN · 2023 Q4               ║
║  Steps 1–12                  ║
║  ─────────────────────────── ║
║  [  Enter Active Control  ]  ║  ← data-testid="enter-active-control-btn"
║                              ║     exact text: "Enter Active Control"
║                              ║     (not "Enter Mode 3")
╚══════════════════════════════╝
```

**AC-G4-C / AC-G4-F (before — Mode 3, bottom-bar ControlPlane, column 3 empty):**
```
Viewport: 1280×800 | Zone: ScenarioInstrumentCluster

[Zone 1A | Zone 1B | column 3 empty ]  ← column 3 shows ghost text in Mode 3 too

╔══════════════════════════════════════════════════════════════════╗
║ [Zone 1A trajectory]  [Zone 1B cohort]  [Zone 1C PMM]  [ emp ] ║
║                                                                  ║
║ [Zone 1D four-framework]                [Zone 1D PSP]   [ ... ] ║
╠══════════════════════════════════════════════════════════════════╣
║  [purple bar]  ControlPlane — fiscal_multiplier  [Apply]         ║  ← bottom-bar,
╚══════════════════════════════════════════════════════════════════╝     purple bg,
                                                                          BELOW Zone 1D
```

**AC-G4-C / AC-G4-F (after — Mode 3, ControlPlane in column 3, bottom-bar absent):**
```
Viewport: 1280×800 | Zone: InstrumentCluster | data-testid="control-plane" in column 3

[Zone 1A (A/B) | Zone 1B | control-plane col ]

╔════════════╬════════════╬════════════════════════╗
║            ║            ║ data-testid=           ║
║  Zone 1A   ║  Zone 1B   ║ "control-plane"        ║  ← orange left border
║            ║            ║                        ║
║ [baseline] ║  Q1 rows   ║ ACTIVE CONTROL         ║
║ [counter]  ║  CRITICAL  ║ SEN · Step 3 of 12     ║
║            ║  at s4     ║ ──────────────────── ──║
╠════════════╬════════════╣ [Form 1] [Form 2]      ║
║  Zone 1C   ║  Zone 1D   ║                        ║
║            ║            ║ Fiscal adj: [_____]    ║
╚════════════╩════════════╣ [     Apply     ]      ║  ← orange Apply btn
                          ║ ──────────────────── ──║
                          ║ HISTORY                ║
                          ║ · Fiscal –1.5% at s3   ║
                          ╚════════════════════════╝

No purple bottom-bar below Zone 1D. ControlPlane exclusively in column 3.
```

**data-testid anchors required (G4 introduces or clarifies):**
- Column 3 container: `data-testid="zone-control-plane"` (existing — retained on InstrumentCluster container)
- Mode 2 content: `data-testid="mode2-column-surface"`
- Activation button: `data-testid="enter-active-control-btn"`
- Mode 3 control plane root: `data-testid="control-plane"` (replaces current `zone-control-plane` on ControlPlane.tsx root — see Constraint 7)
- Form 1: `data-testid="control-plane-form1"`
- Form 2: `data-testid="control-plane-form2"`
- History list: `data-testid="control-plane-history"`
- Per shock type: `data-testid="shock-type-{kebab-case-type}"` (e.g., `shock-type-election-shock`)
- Counter trajectory curve: `data-testid="trajectory-counter"`
- Baseline trajectory curve: `data-testid="trajectory-baseline"` (may already exist — verify at implementation)

---

## 5. Kryptonite Constraint Check

**Does this implementation require specialist mediation for Persona 2 (Eleni, Active Control,
60-second ceiling) to apply a fiscal intervention and read the counter-trajectory?**

`[x]` **No — provided the constraints in §0 are satisfied.** Specifically:
- "Enter Active Control" is plain English. No technical terminology.
- The A/B trajectory comparison in Zone 1A is self-interpreting: two curves visible simultaneously,
  one muted (baseline), one highlighted (counter). The fork point is the visual answer.
- Zone 1B causal attribution (existing Zone 1B capability — not new in G4) shows CRITICAL / CLEAR
  for the counter-scenario.

**Kryptonite check by persona:**

| Persona | Kryptonite risk | Assessment |
|---|---|---|
| Persona 2 (Eleni) | **HIGH RISK if** activation button says "Enter Mode 3". Eleni is not a technical user in the Active Control entry state — she is running a live counter-proposal. "Mode 3" signals system state, not action intent. | **PASS** with AC-G4-A (exact string "Enter Active Control") |
| Persona 2 (Eleni) | **HIGH RISK if** A/B trajectory requires interaction to distinguish — e.g., hover tooltip, legend click, tab switch to see the counter-curve. | **PASS** with AC-G4-C (both curves visible simultaneously without interaction) |
| Persona 5 (Aicha) | **HIGH RISK if** Form 2 shock type names are unexplained technical labels (e.g., "ContagionShock" with no description). Aicha watches without interaction. Form 2 labels must be interpretable on observation. | **Conditional PASS** — Form 2 label display spec to be determined in ADR-019 and UX/UI mockups. The shock type `data-testid` anchors use camelCase type names internally; the displayed label must be plain English. UX Designer must specify plain-language Form 2 labels in §8. |
| Persona 1 (Lucas) | Low risk — Lucas is comfortable with shock taxonomy technical names. Form 2 parameter inputs must include unit labels (not raw float fields). | **Addressed in ADR-019 parameter schema spec** |

**Kryptonite patterns that would constitute REJECT at Customer Agent Layer 3 review:**
- Activation button text containing "Mode 3", "mode3", or any internal mode identifier
- A/B trajectory visible only on hover, tooltip, or tab interaction
- Form 2 shock type labels displayed as raw enum names without plain-language equivalents (e.g., `"ContagionShock"` with no label — Persona 5 cannot read this in 30 seconds)
- Control plane visible only in a drawer, tab, or behind a navigation action in Mode 3

---

## 6. Backend Computation Specification

*Authority: GD Scope Decision Document §Decision 2 (shock taxonomy scope) and CE Agent finding
(Decision 2 deliberation). Full parameter schemas to be specified in ADR-019 before G4 sprint
entry.*

### 6.1 — Existing Mode 3 branching endpoint

Form 1 (policy instruments — fiscal_multiplier, branch_from_step) uses the existing Mode 3
branching endpoint. The G4 implementation verifies this endpoint is on `main` and functional
before the implementation PR opens. If the endpoint has drifted from the `branch_from_step`
computation in `ControlPlane.tsx`, that gap is resolved in G4.

### 6.2 — New shock injection endpoint (Form 2)

**Endpoint pattern (exact path to be specified in ADR-019):**
`POST /api/v1/scenarios/{id}/branch/shock`

**Request shape (discriminated union — from CE Agent Decision 2 finding):**
```
{
  "shock_type": "ElectionShock" | "CurrencyAttack" | "CreditorDefection" |
                "GeopoliticalShock" | "NaturalDisaster" | "ContagionShock",
  "parameters": { type-specific dict — validated against shock_type },
  "inject_at_step": int
}
```

**Per-type parameter resolution (pending ADR-019):**

| Shock type | CE Agent status | ADR-019 action required |
|---|---|---|
| `ElectionShock` | Data dependency: scenario's existing polity data. Tier 2. | Confirm parameter schema in ADR-019 |
| `CurrencyAttack` | Data dependency: FX reserves and peg status — already in scenario. Tier 2. | Confirm parameter schema |
| `CreditorDefection` | `creditor_class` enum taxonomy unresolved — CE Agent finding. | **ADR-019 must resolve `creditor_class` enum before G4 sprint entry** |
| `GeopoliticalShock` | Coarse magnitude parameter. No external data beyond scenario. Tier 2. | Confirm parameter schema |
| `NaturalDisaster` | GDP shock magnitude. No external data beyond scenario. Tier 2. | Confirm parameter schema |
| `ContagionShock` | Linkage approach (pre-populated table vs. simplified model) unresolved — CE Agent finding. | **ADR-019 must resolve linkage approach before G4 sprint entry** |

**Response shape:**
The endpoint returns a branched trajectory response in the same shape as the existing Mode 3
branching endpoint, with an added `shock_applied` object in the response body echoing the shock
type and parameters. The implementing agent verifies the response shape matches
`docs/schema/api_contracts.yml` after the schema update.

### 6.3 — Schema prerequisite

**File:** `docs/schema/api_contracts.yml`

Required addition before implementation PR opens: the shock injection endpoint documentation,
including the discriminated union request shape, per-shock parameter schemas (after ADR-019
resolves the two outstanding items), and response shape. The schema update may be committed as
a preparatory commit on `sprint/m18-g4` before the implementation PR opens.

---

## 7. Render Optimization Specification

*Authority: #1217, Decision 3 (EX-001 disposition), Constraint 5 (same-PR requirement).*

### 7.1 — Recharts memoization

Wrap `ComposedChart` data arrays in `useMemo` with stable dependencies. Apply `React.memo` to
`TrajectoryView.tsx` (or the relevant chart-rendering component). The target is to prevent
re-renders when upstream state changes do not affect chart data — specifically, when ControlPlane
form state changes do not propagate to the trajectory chart until Apply is clicked.

### 7.2 — Lazy ControlPlane mounting

The two-component architecture (Constraint 1) achieves lazy mounting by construction: `ControlPlane`
only mounts when the mode transitions to Mode 3. In Mode 2, only `Mode2ColumnSurface` is mounted.
This avoids the current unconditional ControlPlane mounting pattern.

### 7.3 — EX-001 resolution at G4 exit

At G4 exit, the implementing agent runs `npm run profile:mode3` (the local developer gate replacing
AC-009) on ProBook hardware and records the measurement in the G4 PR description.

- **≤ 100ms:** EX-001 closes as **Resolved**. Entry in `docs/compliance/exceptions.md §EX-001`
  records the MV-002 re-run measurement and closure label. AC-009 `test.fixme()` block is removed
  from the Playwright suite, with a comment: `// AC-009 removed — EX-001 closed Resolved at G4 exit [PR #NNN]; local gate: npm run profile:mode3`.
- **> 100ms:** EX-001 closes as **Won't Fix** (KI-006 infrastructure limitation persists). Same
  AC-009 removal and comment. `docs/compliance/exceptions.md §EX-001` records the measurement,
  the Won't Fix label, and a reference to the local gate.

In both cases, AC-009 is removed from the CI suite permanently. PI Agent confirms EX-001 closure
entry is present in `docs/compliance/exceptions.md` before G4 exit gate passes.

### 7.4 — `npm run profile:mode3` gate

The implementing agent adds `profile:mode3` to `frontend/package.json` scripts before the G4
implementation PR opens. This script runs the Mode 3 full component set mount/render sequence
and reports timing to stdout. The exact implementation (Playwright trace, performance API, or
`react-render-tracker`) is at the implementing agent's discretion — the criterion is that the
output is a single numeric measurement (milliseconds) that can be verified against the 100ms
target without interpretation.

---

## 8. UX/UI Design Artifact Status

*Authority: G4 sprint entry §2.3 (UX/UI design artifact gate — mandatory for new UI elements).
Formal mockups must be authored by UX Designer before implementation PR opens.*

*Status: Not yet authored — pending ADR-019 acceptance. The GD Scope Decision Document
(§Decision 1 + deliberation) provides the specification baseline. UX Designer authors formal
mockups after ADR-019 is accepted and before the G4 sprint entry is filed.*

---

### 8a. UX Mockup — Column Layout and Mode Transition

**To be authored by:** UX Designer
**When:** After ADR-019 accepted
**Required content:**
- Column 3 layout at 1280×800 and 1440×900 for both Mode 2 and Mode 3 states
- Mode 2 → Mode 3 transition interaction (click → column content swap)
- Form 1 and Form 2 tab layout within the column
- History list position within the column (below forms, visible without scroll for ≤2 entries at 1280×800)
- A/B trajectory layout in Zone 1A (two curves, fork-point visibility)
- Governing documents to review: `docs/ux/information-hierarchy.md §Control Plane Reserved Zone`,
  `docs/ux/design-thinking/worldsim-ux-architecture-first-principles.md §Premise 5`,
  `docs/ux/north-star.md §Primary Cognitive Tasks (Mode 3)`

---

### 8b. UI Mockup — Blue/Orange Visual System and Form Layouts

**To be authored by:** UX Designer
**When:** After ADR-019 accepted
**Required content:**
- Blue/orange column border colour tokens (Mode 2: blue; Mode 3: orange)
- `Mode2ColumnSurface` typography and spacing spec
- "Enter Active Control" button visual treatment (contained, blue → active / orange in Mode 3)
- Form 1 field labels, value display format (existing fiscal_multiplier format function must be used)
- Form 2 shock type selector treatment — plain-language labels (Persona 5 kryptonite guard)
- Form 2 parameter input labels with units
- History list entry format (intervention type + step; typography)
- Apply button visual treatment (orange, primary)
- Governing documents to review: `docs/ux/information-hierarchy.md §1B visual system`,
  `docs/ux/north-star.md §Primary Cognitive Tasks`

---

### 8c. Panel Review Record

Panel reviews to be posted as GitHub comments on the G4 implementation issue before implementation PR opens.

- [ ] **UX Designer** — pending (after mockup authorship)
- [ ] **Customer Agent** — pending (Layer 3 for Personas 2 and 5)
- [ ] **Business PO** — pending

**Binding spec rule (sprint entry §2.3):** Implementation PR may not open until all three panel verdicts are ACCEPT.

---

## 9. Out of Scope

**Scenario parameter adjustment in Mode 2 column 3:** `Mode2ColumnSurface` is read-only. Scenario initial condition editing, calibration overrides, and structural assumption changes are deferred. The surface surfaces the active scenario's configuration — it does not modify it.

**Multiple active branches simultaneously in Mode 3:** G4 implements single-branch A/B comparison. Branching from multiple steps simultaneously (e.g., fork at step 2 AND step 5) is deferred.

**GrowthShock (Decision 4 pending):** If Decision 4 is approved before the G4 sprint entry is filed, `GrowthShock` is added as the seventh Form 2 shock type with parameter schema `{growth_rate_delta: float, duration_steps: int, distribution_asymmetry: float}`. If Decision 4 is deferred, Form 2 ships with six types and GrowthShock is tracked in a post-M18 issue. The implementing agent confirms Decision 4 status with PM Agent at sprint entry time.

**Export/download of session history:** The history list is in-session only. Export is deferred.

**Mode 1 column 3:** Mode 1 column 3 remains empty-reserved (ADR-019 will confirm). No content is added to column 3 in Mode 1 as part of G4.

**`TrajectoryView.tsx` structural changes beyond memoization:** G4's Recharts memoization wraps existing chart rendering — it does not restructure the component's internal layout, data binding model, or the Zone 1A encoding rules (ADR-017's authority). CI band rendering (G1) is additive to the existing trajectory view; G4 must leave the extension point available.

**Mode 3 narrator narration integration:** The Demo 7 narrator script is authored separately in Demo 7 preparation. G4 does not implement in-app narration.

---

## 10. Decision 4 — GrowthShock Status

Decision 4 (GrowthShock as seventh shock type) is a post-approval escalation in the GD Scope
Decision Document (§Decision 4 EL Approval Record — "EL decision pending" as of 2026-06-28).

**Impact on G4 scope:**
- If Decision 4 is **approved before ADR-019 is authored:** ADR-019 includes GrowthShock in the Form 2 taxonomy with the parameter schema specified in the Scope Decision Document (§Decision 4). G4 ships seven shock types. AC-G4-D adds `data-testid="shock-type-growth-shock"` to the required testids. Backend endpoint discriminated union adds `GrowthShock` case.
- If Decision 4 is **deferred:** ADR-019 records the explicit deferral with rationale. G4 ships six shock types. Demo 7 Step 4 methodology note is required (analyst uses `fiscal_multiplier` as growth proxy; limitation documented in demo script).

**PM Agent action required:** PM Agent confirms Decision 4 EL status before G4 sprint entry is filed. The sprint entry records the Decision 4 resolution in §3 (Scope Declaration) — not as a footnote.

---

## 11. Test Authorship Obligation

**QA Lead:** QA Lead Agent (E2E); Computation Engine Agent (backend pytest)

**Test authorship deadline:** Both test files authored and committed to `sprint/m18-g4` before any implementation code PR opens. Tests run red before implementation; run green after.

**Test file locations:**
- `frontend/tests/e2e/m18-g4-control-plane-column.spec.ts` — Playwright E2E
- `backend/tests/test_m18_g4_control_plane.py` — pytest (shock endpoint smoke test)

**Criteria covered by E2E test:**
- AC-G4-A: Mode 2 column scenario summary + "Enter Active Control" exact label
- AC-G4-B: Mode 3 column activation on button click
- AC-G4-C: A/B trajectory present in Zone 1A after Form 1 Apply
- AC-G4-D: Form 2 shock type selectors present
- AC-G4-E: History list present after intervention
- AC-G4-F: No bottom-bar ControlPlane in Mode 3
- AC-G4-G: Mode 2 column visible at 1280×800 without scroll

**Criteria covered by backend pytest:**
- AC-G4-I: Shock injection endpoint smoke test (ElectionShock at step 3, branched trajectory diverges)

**AC-G4-H (performance):** Not a Playwright criterion — recorded in PR description by implementing agent.

**No soft-skip patterns (NM-056 guard):** All E2E assertions must be hard-fail. If the Senegal
Article IV fixture is not achievable before implementation, the implementing agent documents this
explicitly in the PR description — the test must be structured to fail, not skipped.

**Pre-push gates (mandatory before any push):**
- Backend: `cd backend && source .venv/bin/activate && ruff check . && mypy app/` — both must exit 0
- Frontend: `cd frontend && npm run build` — must exit 0

**QA Lead acknowledgment:**
- [ ] E2E tests for AC-G4-A through AC-G4-G authored and filed at `frontend/tests/e2e/m18-g4-control-plane-column.spec.ts`. [Date pending — after ADR-019 accepted]
- [ ] Backend tests for AC-G4-I authored and filed at `backend/tests/test_m18_g4_control_plane.py`. [Date pending — after ADR-019 accepted]

---

*Intent document authority: G4 sprint entry §2.3 (intent gate) and CLAUDE.md §Agent Execution
Lifecycle Step 1. GD source: `docs/process/intents/M18-GD-2026-06-26-control-plane-scope-decision.md`.
Issues: #1217 + TBD. This document is the QA authorship contract and the implementation contract —
a discrepancy between the delivered capability and §3 Observable Application State is a Verify-step
failure, not a document-update opportunity. This intent is filed before ADR-019 acceptance to
establish the specification baseline; implementation is blocked until all §0 prerequisites are
satisfied. Authoring authority: `docs/process/agents.md §Frontend Architect Agent`.
Filed: 2026-06-28.*
