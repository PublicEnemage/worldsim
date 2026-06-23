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
