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
**Status:** open

---

**Date:** 2026-06-24
**Source:** EL observation during M16-G8 Demo 6 session
**Finding:** Demo 7 opening act: Mode 3 active control on the Senegal Article IV scenario as a continuation of Demo 6. Same scenario, step 2, Mode 3 activates. Analyst interrogates whether any available fiscal instrument prevents Q1 informal workers crossing the 0.40 recovery floor. If yes: counter-proposal found. If no: conditionality structure itself is the binding constraint — the most powerful finding the tool can produce. Prerequisite: Chief Methodologist review of fiscal-to-cohort-poverty transmission elasticity (filed from Step 5b calibration finding, Issue #1229). This is M17 scope. Demo 7 second act: Zambia restructuring, three-scenario comparison.
**Detail:** Demo 7 is structurally dependent on two M17 deliverables: (1) Mode 3 Active Control, which is the north star instrument design; (2) calibrated fiscal-to-cohort-poverty elasticity so that the Mode 3 instrument search is analytically meaningful rather than searching a mis-calibrated response surface. The Demo 6 → Demo 7 continuity (same entity, same step, Mode 3 activates) is the demonstration arc that takes the tool from analytical standing to active decision support. "Counter-proposal found" and "conditionality structure is the binding constraint" are both defensible outcomes — the tool's value is in answering the question precisely, not in producing a preferred result.
**Status:** open
