---
name: m17-g5-sprint-exit
type: sprint-exit
milestone: M17 — Calibration and Comparative Infrastructure
sprint-group: G5 — Infrastructure Fixes
status: Confirmed — PI Agent exit conditions satisfied 2026-06-26
authored-by: PM Agent
date: 2026-06-26
pi-confirmed: true
release-branch: release/m17
sop-reference: docs/process/sprint-planning-sop.md §Sprint Exit Gate
---

# Sprint Exit — M17, G5: Infrastructure Fixes

**Status:** Confirmed — PI Agent exit conditions satisfied 2026-06-26
**Date produced:** 2026-06-26
**Release branch:** `release/m17`
**Sprint entry document:** `docs/process/sprint-plans/m17-g5-sprint-entry.md`

*Authority: `docs/process/sprint-planning-sop.md §Sprint Exit Gate` (Phase B/C output).*

---

## Section 1 — Sprint Identification and Date

| Field | Value |
|---|---|
| Milestone | M17 — Calibration and Comparative Infrastructure |
| Sprint number | G5 |
| Release branch | `release/m17` |
| Sprint groups | G5 |
| Sprint entry document | `docs/process/sprint-plans/m17-g5-sprint-entry.md` |
| Exit checklist issue | #982 |
| Date implementation completed | 2026-06-26 |
| CI status on release branch | Green |

---

## Section 2 — Implementation Status

| Group | Issue | PR | Merged? | CI status | Notes |
|---|---|---|---|---|---|
| G5-A — #1251 Adaptive y-axis extension | #1251 | #1315 | Yes — 2026-06-25 | Green | Intent doc filed 2026-06-25; BPO ACCEPT on record (Section 3) |
| G5-B — #1214 Startup WARNING | #1214 | #1318 | Yes — 2026-06-25 | Green | Infrastructure; no BPO required |
| G5-C — #1220 G3 spec soft-skip fix | #1220 | #1319 | Yes — 2026-06-26 | Green | AC-F3/AC-CM-2 unblocked by CM-certified parameters; [step N] template fix included |

**Implementation status:** All merged, CI green.

### G5-C implementation note

PR #1319 required two CM-certified parameter corrections (2026-06-26) before CI passed:

1. **Magnitude gap:** `gdp_growth_change` magnitude `"-0.04"` was too small under Wave 1
   elasticities (Q1 informal = −0.20). Δ = 0.008 → poverty 0.388 < Q1_MDA_FLOOR 0.40 →
   milestone sentence never fired. Fixed to `"-0.15"` (Δ = 0.030, poverty 0.410 ≥ 0.40).
   Grounded in IMF WEO SSA severe-crisis peer range.

2. **Year anchor out of range:** `start_date "2024-01-01"` → crossing at step 2 = year 2024,
   outside AC-F3/AC-CM-2 assertion window (2025–2050). Fixed to `"2025-01-01"` → step 2 =
   2025-07-01, year 2025.

3. **Missing `[step N]` in sentence template:** `HumanCapitalTrajectoryPanel.tsx` was rendering
   `by {year}, {cohort}...` rather than the CM-confirmed template `by {year} [step N], {cohort}...`
   (intent doc §AC-CM-2). `MilestoneCrossing.step` was present but not rendered. Fixed.

The old soft-skip guards (`isVisible().catch(() => false)` → early return) had masked all three
gaps since M16-G3 delivery. Their removal (the purpose of #1220) exposed them.

---

## Section 3 — Business PO Acceptance Table

| Deliverable | Work type | Customer Agent Layer 3 assessment | Business PO verdict | Verdict artifact |
|---|---|---|---|---|
| #1251 — Adaptive y-axis extension (Zone 1A visible behavior change) | Frontend | N/A — serves Persona 1 (Lucas Ferreira); not Persona 2/3/5 | ACCEPT | Section 3 below |
| #1214 — Startup WARNING if simulation_entities empty | Backend | N/A — developer-facing diagnostic; not user-facing | Infrastructure — no BPO required | N/A |
| #1220 — G3 spec soft-skip remediation | E2E test | N/A — test infrastructure; not user-facing | Infrastructure — no BPO required | N/A |

**Business PO acceptance status:** All ACCEPT or infrastructure-exempt.

### BPO ACCEPT — #1251 Adaptive Y-Axis Extension

**Acceptance issued:** 2026-06-25 (validation session)

**BPO Acceptance Criteria verification:**

**AC-1251-1 (unit — floor extends yMin):** Verified. `computeYDomain([0.65, 0.70, 0.80, 0.40])`
returns `[yMin, yMax]` where `yMin ≤ 0.40`. Test in `TrajectoryView.test.ts` green in CI.

**AC-1251-2 (unit — floor within data range is no-op):** Verified. Floor already within data
range does not alter domain. Test green in CI.

**AC-1251-3 (E2E — floor line not clamped to chart bottom):** Verified. `y1` attribute of
`[data-testid="zone-1a-mda-floor-ZMB"]` SVG line is numerically less than `MARGIN.top + chartH`
(floor line not at chart bottom edge). Test green in CI via PR #1315.

**AC-1251-R (regression — Zone 1A single-entity recharts unchanged):** Verified. N=1 recharts
mode renders four-framework curves without layout or scale change. Test green.

**Kryptonite check:** The fix REMOVES an existing kryptonite case. Before the fix, an analyst
reading Zone 1A must know that the floor line's position is an artifact of domain clamping
(specialist knowledge) to correctly infer floor headroom. After the fix, the y-axis
proportionality guarantee holds without specialist knowledge. Fix is kryptonite-negative.

**North star test:** MDA floor line in Zone 1A now accurately represents floor headroom when
the floor is below the natural data range. Lucas Ferreira (Persona 1, Ministry Analyst) reading
Zone 1A in a healthy trajectory scenario (composite 0.65–0.80, MDA floor 0.40) no longer sees
the floor line clamped to the chart bottom. The floor line appears in the lower quarter of the
chart at its true proportional position — the analyst can correctly narrate "trajectory at 0.70
is well above the MDA floor at 0.40" without specialist knowledge of domain clamping.

**Verdict: ACCEPT.** All ACs verified against production code and CI. North star test passed.

---

## Section 4 — Open Rejections

No open rejections. Proceed to Section 5.

---

## Section 5 — PI Agent Sprint Exit Confirmation

**Exit conditions checklist (PI Agent):**

- [x] All implementation groups merged; CI green on release branch (Section 2)
  - #1251 → PR #1315 merged 2026-06-25; CI green
  - #1214 → PR #1318 merged 2026-06-25; CI green
  - #1220 → PR #1319 merged 2026-06-26; CI green (re-run passed after AC-F3/AC-CM-2 fix
    and one CI flake on unrelated m14-g6 AC-4; flake confirmed not a regression)
- [x] Business PO ACCEPT verdict filed for each user-facing deliverable (#1251 ACCEPT in
  Section 3; #1214 and #1220 infrastructure-exempt per entry §2.3–§2.4)
- [x] Customer Agent Layer 3 assessment on record for all Persona 2/3/5 deliverables
  — #1251 serves Persona 1 only; no Layer 3 required per entry §2.5 classification
- [x] No open rejection artifacts (Section 4 is empty)
- [x] Near-miss entry filed for each rejection in this sprint — no rejections; no near-miss
  required from Section 4

**PI Agent sprint exit verdict:** Confirmed — all exit conditions satisfied.

**PI Agent confirmation:**

> G5 sprint exit conditions are satisfied as of 2026-06-26. All three G5 issues
> (#1251, #1214, #1220) are merged and closed; CI is green on `release/m17`; BPO ACCEPT is
> on record for #1251 (the only user-facing deliverable); no rejections are outstanding.
>
> One implementation note on record: the soft-skip guard removal in #1220 exposed three
> pre-existing gaps in the M16-G3 milestone sentence implementation (magnitude, year anchor,
> `[step N]` template). These gaps were fixed in PR #1319 under CM advisory (2026-06-26) and
> are not open defects — they are corrected in the same PR that removed the guards. The CM
> diagnosis and fix rationale are documented in Section 2.
>
> The m14-g6 AC-4 CI flake (Zone 1A recharts label timing on GHA shared runner) is confirmed
> not a regression from G5 changes. The test passed on re-run. This flake pattern should be
> monitored; if it recurs, a KI entry is warranted.
>
> G5 sprint is closed.

---

## Sprint Exit Artifact Statement

This document is the sprint exit artifact for G5 of M17. It supersedes any informal exit
notation in SESSION_STATE.md for G5. It is filed at
`docs/process/sprint-plans/m17-g5-sprint-exit.md`.

*The PI Agent confirmation in Section 5 is the gate. The sprint closes when the PI Agent's
verdict is "Confirmed."*
