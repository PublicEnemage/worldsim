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
