# M10 Screenshot Sequence — Presentation Order Manifest and Capture Attestation

**Milestone:** 10 (v0.10.0)
**Scenario:** Argentina 2001–2004 sovereign default and Kirchner recovery, four steps
**Filing issues:** #667 (DEMO-010), #668 (DEMO-011)

## Presentation Order

| Presentation order | Filename | Caption |
|---|---|---|
| 1 (THESIS) | `frame-c-step3-divergence.png` | Step 3 — financial recovery vs. governance lag — thesis frame |
| 2 | `frame-a-step1-instrument.png` | Step 1 — Zone 1 instrument cluster — scenario loaded |
| 3 | `frame-b-step2-crisis.png` | Step 2 — financial floor — Zero Deficit Plan impact |
| 4 | `frame-d-step3-evidence.png` | Step 3 — MDA alert panel — governance WARNING citeable evidence |
| 5 | `frame-e-step4-recovery.png` | Step 4 — recovery arc — GDP growth vs. governance lag |

## Capture State Attestation — DEMO-010 / DEMO-011

**Finding:** These screenshots are present locally but were never committed to the
repository. Capture provenance (date, branch, commit SHA) cannot be verified from
git history — the files are untracked.

**Consequence:** Post-fix state for DEMO-003 (axis label overflow, PRs #337) and
DEMO-005 (Zone 1A legend overlap, PR #345) cannot be confirmed without pixel
comparison against those fix commits. Frame D specifically (DEMO-011) was the
primary frame affected by DEMO-005 and cannot be attested as post-fix.

**Status:** UNATTESTED — capture provenance unknown.

**Required action:** Re-capture this screenshot set before the next stakeholder
presentation or review cycle. Use the updated `demo-narrated.spec.ts` (viewport
fixed to 1440×900 per Issue #675) to produce a committed, traceable capture.
After re-capture, update this file with:
- Capture date
- Branch / commit SHA at time of capture
- Confirmation that DEMO-003 and DEMO-005 fixes are visible in all frames
- Frame D attestation: legend area legible, no overlap

## Capture Viewport Note

The M10 screenshots were captured at an undocumented viewport. The legibility
gate (Step 5b) runs at 1440×900. The `demo-narrated.spec.ts` defaulted to
1280×720 (playwright.config.ts) during M10 — this mismatch is the root cause
documented in NM-032. The viewport was corrected in Issue #675.
