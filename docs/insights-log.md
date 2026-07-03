# WorldSim Insights Log

> **Append-only. Never delete or edit entries — add a new entry if a finding is superseded.**
> Pre-GitHub inbox for findings, open questions, and insights that arise in agent deliberations
> or EL observations but are not yet ready to become GitHub issues or near-miss entries.
> PM Agent reviews and promotes or resolves all open entries at each HORIZON sweep.

## Format

Each entry has four fields:

| Field | Value |
|---|---|
| **Date** | YYYY-MM-DD |
| **Source** | Which session, deliberation, or observation |
| **Finding** | One sentence |
| **Status** | `open` / `promoted → #NNN` / `resolved — [reason]` |

---

## Entries

---

**Date:** 2026-06-12
**Source:** ADR-014 Zone 1B design deliberation
**Finding:** The compact overflow list interaction model question (scan-only vs access surface) was resolved in deliberation but the governing principle — Zone 1B is a zero-interaction reactive-state surface — was not written into CLAUDE.md explicitly.
**Status:** promoted → added to sprint entry §5.2 governing principle

---

**Date:** 2026-06-12
**Source:** Zone 1B stress test deliberation
**Finding:** Alert collision, deduplication, causal grouping, and alert storm handling were identified as unaddressed scope gaps in ADR-014.
**Status:** promoted → G7 sprint entry §5 deliberation

---

**Date:** 2026-06-13
**Source:** EL live app observation during M13 UI walkthrough
**Finding:** Zone 1A trajectory chart Y axis has no label or unit — composite score scale is uninterpretable without presenter narration; solo use cannot establish what 1.0 means.
**Status:** promoted → #950

---

**Date:** 2026-06-13
**Source:** EL live app observation during M13 UI walkthrough
**Finding:** All M12/M13 reviews were conducted in presented-demo context; solo unnarrated use was never tested as a review gate.
**Status:** promoted → #951

---

**Date:** 2026-06-12
**Source:** NM-042 deliberation
**Finding:** The agent sign-off mechanism has no structural independence guarantee in a single-session single-principal context — same-session sign-offs are self-reported.
**Status:** promoted → NM-042 process amendment PR #930

---

**Date:** 2026-06-16
**Source:** EL review of CLAUDE.md structure
**Finding:** CLAUDE.md is 1,080 lines / ~9,000 words and mixes constitutional principles with detailed operational procedures; three sections (Agent Execution Lifecycle ~200 lines, Domain Intelligence Council table ~25 lines, Milestone Exit Ceremony + Retrospective ~65 lines) are candidates for extraction into child docs to reduce the file by ~25% without information loss.
**Status:** promoted → #1091 (M14 closed 2026-06-20; deferral condition met; issue filed for M15 scope)

---

**Date:** 2026-06-17
**Source:** QA Lead + Frontend Architect deliberation during M14-G1 test authorship (PR #1001)
**Finding:** The intent document template has no Visual Spec section; AC-6 (#963 label scope) required the QA Lead to read `AttributeSelector.tsx` source to resolve a prose ambiguity about whether "no underscore in option text" applied to the full string or only the label portion — a before/after annotated screenshot would have made scope self-answering without any code read.
**Detail:** The specific failure mode: intent document §3.2 described the correct observable state in prose ("Reserve Coverage (months)") without capturing what the current broken state looked like in the running app. QA Lead had to make a judgment call (label portion vs. full text content including unit metadata), which caused a two-commit fix sequence. A "Visual Spec (before/after)" section in `docs/process/intent-template.md` — optional for backend/infrastructure ACs, encouraged for any AC involving text display, label format, or layout — would eliminate this class of scope ambiguity at authorship time. The ADR is not the right home for this material; the intent document is, because that is where QA-testable observable states are specified.
**Status:** promoted → #1004

---

**Date:** 2026-06-21
**Source:** EL permanent architectural decisions AC-001 and AC-002 (recorded in `docs/architecture/constraints.md`)
**Finding:** The public data axiom (AC-001 — private data inputs prohibited) and the synthetic substitution principle (AC-002 — synthetic substitution from public sources permitted with mandatory indicator-level disclosure) should be reflected in the founding document as permanent governing constraints — they currently appear only in CLAUDE.md §Synthetic Data and the Data Inference Layer (AC-002 partial) and derive from the founding document's §Open Source as Strategy (AC-001 implicit), but neither is stated as an explicit architectural constraint in the founding document itself.
**Action required:** EL to author an addition to `docs/vision/worldsim-founding-document.md §Open Source as Strategy` naming the public data axiom and synthetic substitution principle as explicit constraints, not only as strategic commitments. The addition should make clear that AC-001 is a permanent prohibition and AC-002 is a standing permission with conditions — so that future contributors reading the founding document understand the full data input architecture without needing to read `docs/architecture/constraints.md` separately.
**Status:** promoted → #1145

---

**Date:** 2026-06-24
**Source:** M16-G8 Step 5b demo preparation verification — Chief Methodologist scope
**Finding:** The fiscal spending cut → cohort-level poverty headcount transmission path is underspecified in the current elasticity calibration. The DemographicModule's ELASTICITY_REGISTRY contains entries for `gdp_growth_change` → Q1 `poverty_headcount_ratio` (elasticity: −0.10, Lustig 2017), but the chain from a fiscal spending cut to that GDP effect to the cohort poverty change produces ~+0.0015pp per step under the standard regime multiplier (0.5 × −0.030 spend = −0.015pp GDP growth change × −0.10 elasticity = +0.0015pp poverty delta). This is insufficient to drive a cohort-level crossing of the 0.40 MDA floor within an 8-step quarterly programme window starting from the SEN T3 national aggregate (0.385). The `imf_program_acceptance` event is in `_SUBSCRIBED_EVENTS` but has no elasticity entries — the programme acceptance event produces no direct demographic transmission effect. Two gaps: (1) the fiscal multiplier chain produces too small a poverty delta for realistic conditionality shocks; (2) programme acceptance has no direct poverty pathway despite being a subscribed event.
**Detail:** Surfaced during M16-G8 Step 5b gate verification when the demo scenario failed to produce the expected step-2 Q1 crossing. The correct response was not to adjust initial attributes to manufacture the crossing (which would have misrepresented what T3 Inferred means) but to document the calibration gap and proceed with what the data shows. The Demo 6 walkthrough narration has been updated accordingly. This is a methodology question for the Chief Methodologist: what is the empirically defensible elasticity for the fiscal spending cut → Q1 poverty headcount channel, and does programme acceptance have a direct poverty transmission pathway distinct from the GDP channel?
**Action required:** Chief Methodologist review of DemographicModule elasticity calibration for the fiscal-to-cohort-poverty transmission path. Candidate sources: IMF (2014) Fiscal Policy and Income Inequality; Lustig (2017); Ball et al. (2013) — all already in ELASTICITY_REGISTRY. The question is whether `fiscal_policy_spending_change` should have direct elasticity entries (bypassing the GDP multiplier chain), or whether the GDP multiplier should be larger for social spending cuts specifically, or whether the current calibration accurately represents the uncertainty at T3 and the demo argument should stay at the structural trajectory level rather than claiming step-level crossing precision. M17 scope.
**Status:** promoted → #1229

---

**Date:** 2026-06-24
**Source:** M16-G8 Demo 6 live session — EL observation + five-agent panel (UX Designer, Design Thinking, Frontend Architect, Architect, Business PO)
**Finding:** Zone 1B lacks a formal proportional allocation between the MDA alert panel (primary instrument) and the CohortImpactSection (supplementary). When cohort crossings fill Zone 1B's natural height, the MDA alert panel collapses to zero due to `flex: "1 1 0"` with `minHeight: 0`. Demo 6 immediate fix: `minHeight: 80px` guarantee on the MDA panel wrapper. M17 architecture decision required: explicit proportional allocation (e.g., 50/50 split, or separate scrollable sub-zones) between the two Zone 1B occupants, captured in ADR-017 amendment or new ADR.
**Status:** promoted → #1252

---

**Date:** 2026-06-24
**Source:** EL observation during M16-G8 Demo 6 session
**Finding:** Demo 7 opening act: Mode 3 active control on the Senegal Article IV scenario as a continuation of Demo 6. Same scenario, step 2, Mode 3 activates. Analyst interrogates whether any available fiscal instrument prevents Q1 informal workers crossing the 0.40 recovery floor. If yes: counter-proposal found. If no: conditionality structure itself is the binding constraint — the most powerful finding the tool can produce. Prerequisite: Chief Methodologist review of fiscal-to-cohort-poverty transmission elasticity (filed from Step 5b calibration finding, Issue #1229). This is M17 scope. Demo 7 second act: Zambia restructuring, three-scenario comparison.
**Detail:** Demo 7 is structurally dependent on two M17 deliverables: (1) Mode 3 Active Control, which is the north star instrument design; (2) calibrated fiscal-to-cohort-poverty elasticity so that the Mode 3 instrument search is analytically meaningful rather than searching a mis-calibrated response surface. The Demo 6 → Demo 7 continuity (same entity, same step, Mode 3 activates) is the demonstration arc that takes the tool from analytical standing to active decision support. "Counter-proposal found" and "conditionality structure is the binding constraint" are both defensible outcomes — the tool's value is in answering the question precisely, not in producing a preferred result.
**Status:** promoted → #843 (Demo 7 live external session); two-act structure and M17 calibration prerequisites fully captured in roadmap §M18, SESSION_STATE §M18 kickoff, and Demo 7 arc narrative

---

**Date:** 2026-06-24
**Source:** M16-G8 IR-001 diagnosis — EL decision during Zone 1A curve separation fix
**Finding:** Governance composite barely responds to fiscal conditionality in the Senegal Article IV scenario (GOV stays ~0.51 across all 8 steps while FIN declines from 0.56 to 0.51). The immediate fix (adaptive y-axis scaling, PR #1243) makes the overlap visible, but the root cause is under-calibrated governance sensitivity to fiscal adjustment. IMF fiscal conditionality should produce measurable governance stress (institutional capacity, rule of law, political feasibility) — especially in Senegal's 2024 Article IV context. The current governance framework scoring does not pick up these channels.
**Detail:** EL explicitly deferred calibration work (Option 2) to M17. The M17 deliverable is: Chief Methodologist review of governance module sensitivity to fiscal conditionality events, specifically (1) whether the governance composite scoring accounts for institutional capacity degradation under austerity, (2) whether political feasibility (`imf_program_acceptance`) has direct governance transmission, and (3) whether the 8-step window is long enough to manifest governance divergence or whether governance stress is a longer-horizon signal.
**Status:** promoted → #1248

---

**Date:** 2026-06-25
**Source:** EL decision at M16-G8 Step 6c north star gate
**Finding:** EL has decided to defer the Step 9 live external stakeholder demo (#843) from M16 to Demo 7. Rationale: the four CRITICAL findings from the Step 6c audience simulation (DEMO6-014 curve identifiability, DEMO6-015 CI bands, DEMO6-026/043 tablet legibility, DEMO6-040 PSP historical precedent) and the Frame D milestone sentence calibration gap are best addressed holistically in M17 and M18 rather than as pre-demo patches. Demo 7 is structurally dependent on Mode 3 (M17 north star) and calibrated fiscal-to-cohort elasticity — deferring aligns the live demo with the tool state that can actually answer "counter-proposal found" or "conditionality structure is the binding constraint." Demo 6 preparatory work (Steps 1–6c, DEMO6-001–049 findings record, north star finding sentence, audience simulation artifact) is retained as the specification foundation for Demo 7.
**Detail:** Implication for M16 exit: #843 is no longer the M16 exit gate. M16 closes on the strength of distributional visibility delivery (G1/G2/G3/G4/G6/G9/G10 complete). CLAUDE.md §What We Are Building First M16 description and the M16 exit gate condition must be updated before M16 exit ceremony. #843 moves to M17. DEMO6-014 through DEMO6-049 are reference findings for M17/M18 planning — they do not need to be filed as individual GitHub issues in M16; PM Agent promotes to GitHub at M17 sprint planning HORIZON sweep as appropriate.
**Status:** resolved — EL decision fully recorded in SESSION_STATE.md exit ceremony, CLAUDE.md §M16+M17, and #843 GitHub issue moved to M17; all required artifact updates complete; no further promotion needed

---

**Date:** 2026-06-25
**Source:** M17-G2 sprint entry authorship — EL direction
**Finding:** The UX mockup + UI mockup + named panel review gate established in M17-G2 sprint entry §2.5 is not yet part of the sprint planning SOP — any UX/UI-impacting sprint group can currently proceed to implementation without a design artifact gate or multi-agent panel review requirement.
**Detail:** The M17-G2 sprint entry §2.5 established a pattern that should be generalised: (1) UX mockups (structural, viewport-anchored at 1280×800 and 768px) are a minimum required artifact for any sprint group whose primary deliverable includes user-facing UX/UI changes; (2) UI mockups (higher-fidelity, design-system-applied) are required when any panel member identifies a visual density risk or legibility ambiguity that UX mockups cannot resolve; (3) a named panel review — UX Designer (R), Design Thinking Agent (cognitive task validation), Customer Agent (persona accessibility), Frontend Architect (technical feasibility), Business PO (acceptance) — must pass before the BPO can issue formal Phase 1 acceptance; (4) the UX Designer's panel summary comment must tag the PM Agent (@PublicEnemage) for the BPO routing to be trackable. Prior to G2, sprint entries for UX/UI-impacting groups (e.g., M16-G1 Zone 1A Phase 4, M16-G2 cohort disaggregation, G10 pre-demo polish) accepted prose intent documents and individual agent sign-offs without a consolidated panel review gate or a mockup-as-minimum-artifact requirement. The G7 intent document visual spec gap (insights log entry #7, promoted → #1004) identified the related problem at the intent document level; this finding is the upstream SOP-level fix.
**Action required:** PM Agent to file a GitHub issue for an amendment to `docs/process/sprint-planning-sop.md` adding a "UX/UI design artifact gate" section: for any sprint group classified as UX/UI-impacting (determined at sprint entry filing), the entry must include UX mockups at minimum and a panel review with the five named agents before EL approval is granted. The amendment should also specify: (a) what "UX/UI-impacting" means (any AC that includes a visual observable state — layout, label, color, interaction, viewport behavior); (b) that the panel review summary comment must tag PM Agent; (c) that the intent document must reference the panel-approved mockups as the binding visual specification so QA assertions are anchored to approved design, not implementation inference.
**Status:** promoted → #1277

---

**Date:** 2026-06-26
**Source:** EL observation during session startup — SESSION_STATE.md file size review
**Finding:** `SESSION_STATE.md` has grown to 2,038 lines / 301 KB, exceeding the Claude Code 256 KB read ceiling. The session continuity guarantee cannot currently be satisfied in full — agents reading the file at session start receive truncated content. This is a live failure, not a future risk. Filed as NM-066 and GitHub Issue #1328.
**Action required:** EL direction decision on remediation model (archive-and-rotate, sprint journal issue, cockpit-card, or hybrid) must be made and recorded before M18 kickoff. This is an M18 entry blocker: no M18 sprint group may begin implementation until `SESSION_STATE.md` is at or below a defined size limit and an archival/rotation protocol is documented in `CLAUDE.md §Session Continuity`. PM Agent: promote to M18 sprint planning agenda at next HORIZON sweep; flag as pre-M18 infrastructure item requiring EL decision before sprint entry gate opens.
**Status:** promoted → NM-066, #1328

---

**Date:** 2026-06-26
**Source:** EL pattern recognition across M15–M17 PR history
**Finding:** The current release branch workflow has no sprint group isolation protocol for parallel workstreams. When ≥ 2 Claude Code sessions run concurrent sprint groups, shared-file overwrites, duplicate PRs, wrong-target merges, and post-exit rework recur without any process gate to prevent them. Documented instances across M15–M17: 6 CLOSED PRs with lost state, duplicate same-named PRs (#1293/#1294, #1307/#1308), wrong-target merge (#1303 to `main`), and a post-exit spec fix (#1319 after G3 exit). M18 is expected to have parallel sprint groups. This gap will recur unless addressed before M18 kickoff. Filed as NM-067 and GitHub Issue #1329.
**Action required:** EL direction decision on branching model (sprint group sub-branches, wave integration branch, PM Agent coordination lane, or hybrid) must be made and recorded before M18 kickoff. Required protocol changes: (1) `CLAUDE.md §Release Branch Workflow` updated; (2) sprint entry template amended to include file-conflict risk assessment field; (3) cross-group dependency declaration added to sprint entry gate. PM Agent: promote to M18 sprint planning agenda at next HORIZON sweep; flag as pre-M18 infrastructure item requiring EL decision before sprint entry gate opens.
**Status:** promoted → NM-067, #1329

---

**Date:** 2026-06-26
**Source:** EL pattern recognition across NM registry — NM-027 class has recurred four times across M12–M17
**Finding:** The sprint entry gate has no step requiring the implementing agent to verify that prior NM process improvements relevant to the sprint group's domain are in effect. The NM-027 no-op guard pattern has recurred as NM-027, NM-028, NM-047, NM-058, and NM-061 despite working agreement amendments after each instance. A second chain: NM-016 established the mypy gate; NM-052 revealed it had been non-functional for 8 milestones. Filed as NM-068 and GitHub Issue #1332.
**Action required:** Sprint entry template amended before M18 kickoff to include a "Prior NM applicability check" field — implementing agent confirms which prior NM process improvements apply to the sprint group's domain and that each is in effect. PM Agent checks the field before recommending EL approval. For the NM-027 class specifically, a curated lookup list for frontend E2E sprints is more actionable than a full registry scan. This is an M18 entry blocker: first M18 sprint group must demonstrate the check. PM Agent: promote to M18 sprint planning agenda at next HORIZON sweep.
**Status:** promoted → NM-068, #1332

---

**Date:** 2026-06-26
**Source:** EL observation — persistent untracked test artifact directories in git status across multiple M17 sessions
**Finding:** `backend/test-results/`, `frontend/playwright-report/`, `frontend/session-screenshots/`, `frontend/test-results/`, and `*.test-marker` files are not covered by `.gitignore`. They appear as untracked in every session. A `git add -A` would stage them; large binary artifacts committed to history require destructive git operations to remove. The `near-miss-registry.md.test-marker` file's provenance is unknown. Filed as NM-069 and GitHub Issue #1333.
**Action required:** One-PR fix — add the four directory patterns and `*.test-marker` to `.gitignore`; investigate and delete or gitignore the `near-miss-registry.md.test-marker` artifact. Sprint entry template amended with a "New output paths" field so future test frameworks land in `.gitignore` in the same PR that introduces them. This is not an M18 kickoff blocker but should be resolved in the first M18 infrastructure PR. PM Agent: include in first M18 HORIZON sweep as an open housekeeping item.
**Status:** promoted → NM-069, #1333

---

**Date:** 2026-06-26
**Source:** EL pattern recognition across NM-016, NM-052, NM-054 — same structural absence underlies all three
**Finding:** The pre-push gates (`ruff check . && mypy app/` for backend; `npm run build` for frontend) are mandatory in `CLAUDE.md` but enforced only by agent compliance — no git hook runs them automatically. NM-052 documented that the mypy gate was non-functional locally for 8 milestones (M8–M16) because the Python 3.13 venv requirement was undocumented; agents who ran it received meaningless output and believed the gate had passed. NM-054 documented that the frontend build gate does not catch E2E breakage. The root cause common to both is the absence of a hook that enforces the gate structurally regardless of agent compliance. Filed as NM-070 and GitHub Issue #1334.
**Action required:** Implement a git pre-push hook (`.githooks/pre-push`) before M18 kickoff that (1) detects changed files, (2) runs the backend gate only when `backend/` files are touched — failing loudly if `.venv` is absent rather than running silently in the wrong environment, (3) runs the frontend build gate only when `frontend/src/` files are touched, (4) exits non-zero on any failure. Document hook installation as a required setup step in `docs/CONTRIBUTING.md`. This is an M18 entry blocker: all M18 sprint groups must run with hook enforcement from the first push. PM Agent: promote to M18 sprint planning agenda at next HORIZON sweep; flag alongside #1328 and #1329 as pre-M18 infrastructure.
**Status:** promoted → NM-070, #1334

---

**Date:** 2026-06-26
**Source:** EL pattern recognition — upstream planning gap enabling NM-067 coordination failures
**Finding:** The sprint planning SOP has no wave-level coordination check. There is no defined threshold above which a coordination protocol is required before parallel sprint groups begin implementation. M17 ran seven concurrent groups with no coordination budget, making NM-067's merge conflicts and lost updates structurally inevitable. Even with the branching model fix from Issue #1329, seven simultaneous groups sharing a PM Agent coordination lane would exceed the lane's capacity. Filed as NM-071 and GitHub Issue #1335.
**Action required:** `docs/process/sprint-planning-sop.md` amended before M18 kickoff with a wave kickoff coordination check: PM Agent lists all groups in the wave, their shared-file write scope, and cross-group dependencies, then assigns a coordination tier (standard / recommended / required) based on group count. Recommended starting ceiling: 5 parallel groups per wave. Dependency merge sequence documented before any downstream group opens an implementation PR. This is an M18 entry blocker: wave kickoff coordination check must be completed before M18 Wave 1 implementation begins. PM Agent: promote to M18 sprint planning agenda at next HORIZON sweep alongside #1329.
**Status:** promoted → NM-071, #1335

---

**Date:** 2026-06-30
**Source:** EL live observation during M18-G7 Step 6 screenshot recapture run 5 — Act 2 Zone 1A
**Finding:** Act 2 Zone 1A shows a single overlapping line with colour speckles instead of three visually distinct ZMB scenario curves. Root cause: ZMB PHR values (Option A: 0.628, Option B: 0.584, Option C: 0.540) differ by only ~0.04–0.05 per step; the y-axis is not tight-scoped to the actual data range, so all three curves collapse visually into a single band. CompositeChartSVG `computeYDomain` uses `[0, 1]` or a padded range rather than [min(data), max(data)] with appropriate margin.
**Status:** promoted → #1629

---

**Date:** 2026-06-30
**Source:** EL live observation during M18-G7 Step 6 screenshot recapture run 5 — Act 1 Mode 3 Zone 1A narration
**Finding:** Act 1 narration at line 892 of demo-narrated.spec.ts says "the human development composite is higher at every step from three onward" implying a separately visible HD line in Zone 1A — but Mode 3 uses CompositeChartSVG which renders a single composite average line, not per-framework lines. The HD contribution is included in the composite average but not separately visualised. The narration creates an expectation the chart does not satisfy; audience may ask to see the HD line and be unable to find it.
**Status:** promoted → #1630

---

**Date:** 2026-07-02
**Source:** EL multi-agent consultation — headless engine battle-testing deliberation; agents: Architect, CE Agent, Chief Methodologist, Chief Economist, UX Designer, Design Thinking, Customer Agent, Business PO; PM Agent documenting
**Finding:** The UI is beginning to function as a limiting factor in understanding what the simulation engine can produce; a headless battle-testing initiative running 10 real-world scenarios directly through the API would validate active control (Mode 3) capability across real counter-factuals and surface display debt from the outside.
**Detail:** Full multi-agent deliberation on record in session context (2026-07-02). Consensus findings: (1) Headless path already exists — `POST /scenarios/{id}/advance` + httpx + `tests/backtesting/` pattern is the tested Mode 3 interface. No new plumbing required. (2) Missing piece: a Mode 3 harness script layer (loop, control input injection, per-step capture, counter-factual differential) — new work but thin. (3) Chief Methodologist: two run categories must be distinguished — Type A (backtesting vs historical actuals, fidelity tier assigned) and Type B (counter-factual, compared to baseline run, CI band differential is the argument). (4) Output format: configurable input parameter — ASCII, CSV, JSON, Markdown table (EL decision). (5) Business PO: exercise tests whether engine is core asset or UI is load-bearing. (6) Scope: M19 (EL decision). (7) Iceland timing: pre-calibration structural test — runs before M19 empirical calibration to distinguish structural gap from calibration gap (EL decision). Capital control representability check conducted same session: `EmergencyInstrument.CAPITAL_CONTROLS` exists but ExternalSectorModule and MacroeconomicModule are silent; DemographicModule has dead subscription (wrong event string). Issue #1532 filed; ARCH-014 added to ADR backlog (PENDING_NUMBER, ADR-020). Issues #30 and #35 assessed as DIRECTION_ONLY impact on 4 of 10 scenarios (Greece, Argentina, Sri Lanka, Iceland — reserve/debt stock floor timing unreliable).
**Ten scenarios approved:** (1) Zambia constraint-floor search (Type B, #1542+#1540); (2) Senegal Article IV full Mode 3 (Type B, #1541+#1540); (3) Greece primary surplus counter-factual (Type B, #1547); (4) Argentina peg-abandonment timing (Type B, #1548); (5) Sri Lanka 2022–23 (Type A+B, #1549); (6) Pakistan 2022–23 programme survival (Type B, #1550); (7) Turkey 2018–19 rate-cut counter-factual (Type B, #1551); (8) Egypt 2016 phased vs shock devaluation (Type B, #1552); (9) Iceland 2008–11 orthodox vs heterodox pre-calibration structural test (Type B, #1553 — blocked by #1532); (10) Ghana 2022–23 IMF programme (Type A+B, #1554). Harness infrastructure: #1546.
**Status:** resolved — All 10 scenario issues filed (#1546–#1554), harness #1546, capital controls #1532 on M19 milestone; ARCH-014 → ADR-020 accepted 2026-07-03; G2D implementation unblocked. Fully reflected in GitHub — no further promotion required. (Resolved at M19 HORIZON sweep 2026-07-03.)
