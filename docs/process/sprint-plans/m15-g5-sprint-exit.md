---
name: m15-g5-sprint-exit
type: sprint-exit
milestone: M15 — Human Cost Architecture
sprint-group: G5
status: Confirmed
authored-by: PM Agent + Business PO Agent
date: 2026-06-22
pi-confirmed: true
release-branch: release/m15
sop-reference: docs/process/sprint-planning-sop.md §Sprint Exit Gate
---

# Sprint Exit — M15, G5: Process Fixes + Walkthrough Updates

**Status:** Confirmed — all exit conditions satisfied
**Date produced:** 2026-06-22
**Release branch:** `release/m15`
**Sprint entry document:** `docs/process/sprint-plans/m15-g5-sprint-entry.md` — EL Approved 2026-06-22
**Intent document:** `docs/process/intents/M15-G5-2026-06-22-process-fixes.md`

*Authority: `docs/process/sprint-planning-sop.md §Sprint Exit Gate` (Phase D output).
G5 is a three-tier mixed sprint: Tier 1 items gate G8; Tier 2 items are primary scope;
Tier 3 items are capacity-allowing. Tier 3 items (#837, #951, #259) are not addressed in
this sprint and are not M15 G5 exit conditions. G8 is now UNBLOCKED.*

---

## Section 1 — Sprint Identification and Date

| Field | Value |
|---|---|
| Milestone | M15 — Human Cost Architecture |
| Sprint group | G5 — Process Fixes + Walkthrough Updates |
| Release branch | `release/m15` |
| Sprint entry document | `docs/process/sprint-plans/m15-g5-sprint-entry.md` |
| Intent document | `docs/process/intents/M15-G5-2026-06-22-process-fixes.md` |
| Exit checklist issue | #984 |
| Date implementation completed | 2026-06-22 (PR #1123 merged — last Tier 2 item) |
| CI status on release branch | Green — all required checks pass or skip |

---

## Section 2 — Implementation Status

| Issue | PR | Merged? | CI status | Tier | Notes |
|---|---|---|---|---|---|
| #1083 — Grounding strip date label | #1119 | Yes — 2026-06-22 | Green | Tier 1 | `formatVintageDate()` + `grounding-strip-date` testid |
| #1007 — recompute-badge timing | #1119 | Yes — 2026-06-22 | Green | Tier 2 | Immediate `pending` before async branch POST |
| #1067 — M15 screenshots (Frame B ≠ C) | #1121 | Yes — 2026-06-22 | Green | Tier 1 | 5 distinct PNGs; md5 differ |
| #1088 — walkthrough DEMO-123 | #1121 | Yes — 2026-06-22 | Green | Tier 1 | "0 consecutive steps" count = 0 |
| #1089 — walkthrough DEMO-124 | #1121 | Yes — 2026-06-22 | Green | Tier 1 | "entry-state" count = 9 |
| #1090 — walkthrough DEMO-129 | #1121 | Yes — 2026-06-22 | Green | Tier 1 | `methodology-overview.md` cited ×5 |
| #1084 — PSP calibration anchor | #1122 | Yes — 2026-06-22 | Green | Tier 2 | Zambia 2022 + Ghana 2023 ECF; public IMF sources |
| #1004 — intent template §Visual Spec | #1122 | Yes — 2026-06-22 | Green | Tier 2 | data-testid ×4; viewport ×2; "Required when" rule |
| #1048 — Docker Alembic migrations | #1123 | Yes — 2026-06-22 | Green | Tier 2 | `entrypoint.sh`: alembic upgrade head + exec "$@" |

**Tier 3 items not addressed (no gate dependency):**
| Issue | Title | Disposition |
|---|---|---|
| #837 | feat(demo): configuration-driven demo scripts | Capacity not available; no G5 or G8 gate; remains open |
| #951 | process: solo-use review protocol | Capacity not available; remains open |
| #259 | standards: CTO legibility metrics dashboard | Capacity not available; remains open |

**Implementation status:** All Tier 1 and Tier 2 items merged, CI green. Tier 3 open by
design (capacity-allowing per sprint entry §3.1).

**Pre-push gate compliance:**
- Backend: `ruff check . && mypy app/` — clean on PR #1123 (entrypoint.sh + Dockerfile only;
  no Python model changes); CI lint PASS
- Frontend: `npm run build` — clean on PR #1119 (GroundingStrip.tsx + ScenarioInstrumentCluster.tsx)
- Branch names: `fix/m15-g5-*`, `docs/m15-g5-*`, `feat/m15-g5-*` — milestone prefix present on all

**Step 4 Verify verdict:** PASS — 2026-06-22
13/13 ACs confirmed by CI evidence (playwright-e2e PASS on PR #1119; test-backend PASS on PRs
#1122, #1123) and local file checks (grep, md5, find). Full verdict recorded in intent document §8.

---

## Section 3 — Business PO Acceptance Table

| Deliverable | Work type | Customer Agent L3 | Business PO verdict | Verdict artifact |
|---|---|---|---|---|
| #1083 — Grounding strip date "Apr 2024" | UI bug fix | PASS (§9a in intent doc) | ACCEPT | Intent doc §9b |
| #1007 — Recompute-badge after Apply | UI bug fix | PASS (§9a in intent doc) | ACCEPT | Intent doc §9b |
| #1067 — M15 screenshots (5 distinct frames) | Demo artifact | N/A — no Persona 2/3/5 output | ACCEPT | Intent doc §9b |
| #1088 — Walkthrough DEMO-123 | Documentation | N/A — not user-facing output | ACCEPT | Intent doc §9b |
| #1089 — Walkthrough DEMO-124 | Documentation | N/A — not user-facing output | ACCEPT | Intent doc §9b |
| #1090 — Walkthrough DEMO-129 | Documentation | N/A — not user-facing output | ACCEPT | Intent doc §9b |
| #1084 — PSP calibration anchor | Methodology doc | N/A — not user-facing output | ACCEPT | Intent doc §9c |
| #1004 — Intent template §Visual Spec | Process document | N/A — process improvement | ACCEPT | Intent doc §9c |
| #1048 — Docker Alembic migrations | Infrastructure | N/A — infrastructure | ACCEPT | Intent doc §9c |

**Business PO acceptance status:** All ACCEPT.

### §3a — Customer Agent Layer 3 Assessment

**Trigger:** #1007 (recompute-badge) and #1083 (grounding-strip date) serve Persona 2 (Eleni,
Finance Ministry Negotiator) and Persona 5 (Aicha, Junior Ministry Analyst) in the Reactive
and Active entry states — Layer 3 gate required per `CLAUDE.md §Layer 3 Quality Gate (FD-2)`.

**#1083 — Grounding strip date:**
"2024-Q1" → "Apr 2024". The output now tells the user what the date means without requiring
knowledge of IMF quarter notation. Aicha reads "Apr 2024" and cites "April 2024 starting point"
with zero translation. **Layer 3 verdict: PASS**

**#1007 — Recompute-badge:**
"Recompute pending — advance step to see updated trajectory" — names the state and specifies
the action. No icon-only fallback. Kryptonite constraint satisfied. Eleni understands what to
do without presenter mediation. **Layer 3 verdict: PASS**

### §3b — Business PO Validate Verdict

**North Star Assessment:**

*Scenario:* Eleni (Persona 2) is in a ZMB ECF restructuring session. She changes
fiscal_multiplier from 1.00 to 1.30 and clicks Apply. She reads the Grounding strip at
scenario load.

*Pre-G5 capability:*
- Grounding strip date showed "2024-Q1" — Eleni had to know Q1 means January–March before
  she could cite the reference date
- After clicking Apply, no signal appeared — Eleni could not tell whether the trajectory
  reflected the new or old parameter

*Post-G5 capability:*
- Grounding strip shows "Apr 2024" — Eleni immediately reads "April 2024 starting point" and
  cites it without a translator
- After Apply, "Recompute pending — advance step to see updated trajectory" appears — Eleni
  advances one step and knows the trajectory is fresh; she can cite the updated reserve
  coverage figure with confidence

*Does this change what the minister's team can argue at the table?*
Yes — two small but real friction points in the 90-second reactive window are removed.
Neither requires specialist mediation to act on after G5. The walkthrough fixes ensure real
external participants in G8 receive a polished demo without correctable quality gaps.

**North star verdict: PASS**

**Business PO verdict: ACCEPT** (all nine deliverables)

**G8 gate status:** SATISFIED — all five Tier 1 items merged and validated. G8 sprint entry
may now open.

**Action item for G8 (non-blocking):** Add hyperlink from
`docs/onboarding/methodology-overview.md §Political Economy module` to
`docs/methodology/psp-calibration-anchor.md` during demo walkthrough preparation. Cold
navigation to the PSP anchor without this link may take >1 minute; the link removes the gap.

---

## Section 4 — Open Rejections

No rejection artifacts were produced for G5. Step 4 Verify PASS on first attempt for all
13 ACs. No REJECT-NNN artifact was filed.

---

## Section 5 — Near-Miss Register

No new near-misses to file for G5. Process deviations identified in the overall M15-G5
implementation session were filed separately:
- NM-052: Pre-push mypy gate non-executable locally (filed 2026-06-22; PR #1108)
- NM-053: CM sign-off on #975 timing deviation (G4 item; filed 2026-06-22)
- NM-054: E2E combobox regression from G4 entity-selector change (G4 item; filed 2026-06-22)

No NM entries attributable to G5 process or implementation.

---

## Section 6 — PI Agent Confirmation

> G5 sprint exit conditions per `docs/process/sprint-planning-sop.md §Sprint Exit Gate`:
>
> 1. Business PO acceptance recorded for every user-facing deliverable — ✅ ACCEPT for all
>    nine deliverables (§3b above); all Tier 1 and Tier 2 items accepted
> 2. Customer Agent Layer 3 assessment on record for Persona 2/5 deliverables — ✅ PASS for
>    #1007 and #1083 (§3a above); non-Persona-2/3/5 deliverables confirmed N/A
> 3. No open rejection artifacts — ✅ confirmed (§4 above)
> 4. PI Agent confirms all exit conditions satisfied — ✅ confirmed below
>
> North star test artifact: present (§3b above). Finance ministry scenario (Eleni in ZMB ECF
> restructuring session), specific capability gap (date translation + parameter state uncertainty),
> specific fix (Apr 2024 date format + recompute-badge text). Mission-complete.
>
> Tier 3 items (#837, #951, #259) remain open by design — capacity-allowing exception per
> sprint entry §3.1; no G5 or G8 gate dependency. These remain in the M15 open issues table.
>
> G8 gate: SATISFIED. All five Tier 1 items (#1067, #1083, #1088, #1089, #1090) are merged,
> CI green, and BPO accepted. G8 sprint entry may open immediately.

**PI Agent confirmation:** All exit conditions satisfied. G5 sprint exit is CONFIRMED.
M15-G5 is CLOSED. G8 is UNBLOCKED.

**Date confirmed:** 2026-06-22

---

*Sprint exit document authority: `docs/process/sprint-planning-sop.md §Sprint Exit Gate`.
Three-tier structure authority: `docs/process/sprint-plans/m15-g5-sprint-entry.md §3.1`.
All lifecycle authority: `docs/process/agent-execution-lifecycle.md`.*
