# Engine Performance Artifacts

This directory contains performance measurement artifacts for the simulation engine.
All measurements are run on the target hardware (GitHub Actions free-tier CI runner:
2-core, 7 GiB RAM, Ubuntu) as required by CLAUDE.md §Equitable Build Process.

## Artifact Index

| File | Type | Issue | Date |
|---|---|---|---|
| `phase1-iterative-baseline.md` | Phase 1 baseline — iterative engine | #514, #406 | 2026-05-31 |
| `phase2-ab-comparison.md` | Phase 2 A/B — iterative vs. matrix (PENDING) | #406 | TBD — requires matrix engine |

## Pending Artifacts

**Phase 2 A/B Comparison Report** (`phase2-ab-comparison.md`):
Required before the iterative engine can be retired (ADR-009 §Decision 1). Must include:
- Matrix engine vs. iterative engine wall time comparison at all benchmark dimensions
- Equivalence gate confirmation (|delta| ≤ 1e-10 on all Quantity.value fields)
- Sparse profiler output (sparsity ratio, fill-in rate, matrix construction vs.
  multiplication time)
- Explicit confirmation that the matrix engine meets the ADR-009 §Decision 3 target
  on the CI runner (1,000 MC runs on Greece scenario within 60 seconds)

This report is authored by the Chief Engineer after the matrix engine proof-of-concept
is integrated. Its completion unblocks the iterative engine retirement procedure.

## Adding a New Report

1. Name the file descriptively: `phase2-ab-comparison.md`, `stress-test-results-m11.md`
2. Include: hardware spec, methodology, raw results, and high-water mark identification
3. Update this README index
4. Reference the corresponding GitHub issue and ADR decision
