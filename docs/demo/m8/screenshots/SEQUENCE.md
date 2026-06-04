# M8 Screenshot Sequence — Presentation Order Manifest

**Milestone:** 8 (v0.8.0)
**Scenario:** Greece 2010–2015 IMF programme, six steps
**Capture date:** 2026-05-18 (pre-M9)
**Filing issue:** #349 (DEMO-008 retroactive fix)

## Capture-to-Presentation Order Mapping

Files are named in capture order (A–E). The UX Agent brief (Issue #233) specified
presentation order **C → A → B → D → E** (thesis-first sequence). Use this manifest
when presenting or reviewing these artifacts.

| Presentation order | Filename | Caption |
|---|---|---|
| 1 (THESIS) | `frame-c-step5-divergence.png` | Step 5 — HD tab — divergence frame (thesis visualization) |
| 2 | `frame-a-step1-instrument.png` | Step 1 — full Zone 1 — instrument cluster setup |
| 3 | `frame-b-step3-collapse.png` | Step 3 — Financial tab — maximum fiscal stress |
| 4 | `frame-d-step3-evidence.png` | Step 3 — MDA alert panel prominent — citeable evidence |
| 5 | `frame-e-step3-ecological.png` | Step 3 — Ecological tab + note expanded |

## Why This File Exists

DEMO-008 (M8 stakeholder review, 2026-05-18): screenshot filenames were assigned
alphabetically in capture order, not in the presentation order specified by the
UX Agent brief. A reviewer reading frame-a before frame-c encounters the instrument
view before the thesis, which changes the quality of the review analysis.

`docs/process/demo-preparation-standard.md §Step 6` now requires either
presentation-order filenames or a SEQUENCE.md for all future milestones.
This file is the retroactive SEQUENCE.md for M8.
