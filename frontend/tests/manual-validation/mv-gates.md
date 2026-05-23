# Manual Validation Gates — M9 Instrument Cluster

These gates cannot be automated in CI. Each must be completed and recorded
before M9 exits. See `docs/frontend/fa-brief-m9-instrument-cluster.md` §Manual Validation Gates.

Automated CI gates (AC-007, AC-008, AC-009) use Playwright's 4× CPU throttle
(`page.emulate({cpuThrottling: 4})`). MV-002 is the hardware confirmation that
a real 4-core/8GB laptop meets the same constraint — Playwright throttle is not
hardware simulation. See FA brief §Performance Acceptance Criteria.

## MV-001 — CVD Validation (Framework Colors)

**Required:** Four framework colors pass CVD check (deuteranopia + protanopia).

**Tool:** Color Oracle (macOS/Windows, free) or Figma accessibility plugin
(Able or Stark).

**Provisional colors** (from ADR-010 Decision 3 — unvalidated until this gate runs):

| Framework | Provisional hex |
|---|---|
| Financial | `#2D6A8B` |
| Human Development | `#C67C2E` |
| Ecological | `#3A7A4B` |
| Governance | `#5C4A8A` |

**Pairs to validate** (all must pass):
- All 4×3 = 12 inter-framework color pairs
- Policy input blue (`#1A6BAF`) vs. all four framework colors
- Shock orange (`#C45C00`) vs. all four framework colors

**Minimum threshold:** Any two colors that appear more similar than 20% ΔE (CIELAB)
under simulated CVD fail.

**Procedure:**
1. Load all four hex values into Color Oracle or the Figma plugin
2. Run deuteranopia simulation — check all pairs listed above
3. Run protanopia simulation — check all pairs listed above
4. Document any failing pairs
5. If any pair fails: FA Agent documents the pair and UX Designer issues revised
   hex values. No ADR amendment required — colors go directly to
   `frontend/src/constants/frameworkColors.ts` with UX Designer ruling in PR.

**Outcome record** (FA Agent completes before TrajectoryView implementation):

- Date: ___________
- Tool used: ___________
- Outcome: ☐ All pairs pass — provisional values confirmed ☐ Revision required

**UX Designer sign-off on final colors:** ___________

**Status:** ☐ Pending — must run before TrajectoryView implementation begins

---

## MV-002 — Performance on Target Hardware

**Required:** Trajectory view renders within 100ms on an actual 8GB/4-core laptop.

**Why this gate exists:** AC-007/AC-008/AC-009 are CI gates using Playwright's 4×
CPU throttle. On high-core-count CI runners, 4× throttling may produce a faster
effective runtime than an actual 4-core laptop. This gate is the hardware
confirmation before M9 closes. See FA brief §Manual Validation Gates.

**Context:** This tool must work on the hardware that resource-constrained finance
ministries actually have. Performance work that enables a four-core laptop to run
analyses previously requiring expensive compute is first-class feature development.
See CLAUDE.md §Equitable Build Process.

**Procedure:**
1. On an 8GB RAM / 4-core laptop (not a CI runner, not a high-core-count dev machine)
2. Run the Playwright performance tests (AC-007, AC-008, AC-009) without the 4×
   CPU throttle emulation flag — on the real machine
3. Record render time for: (a) initial render, (b) step navigation, (c) full Mode 3
   component set (8 Lines + 4 Areas + 3 shock ReferenceLines)
4. All three must be ≤ 100ms
5. Document hardware specs and measured times in the M9 exit PR description

**Hardware validation record** (developer completes before M9 exit):

- Machine: ___________
- RAM / cores: ___________
- Measured initial render: ___________
- Measured step navigation: ___________
- Measured Mode 3 full set: ___________
- Date: ___________

**Status:** ☐ Pending — run after AC-007/AC-008/AC-009 CI gates pass

---

## MV-003 — UX Designer Sign-Off

**Required:** UX Designer confirms component layout decisions before implementation
begins. This gate ensures the component structure, column widths, stacking order,
alert format, badge placement, and placeholder styling are confirmed at the design
level — not discovered to be wrong after implementation.

**Items confirmed by UX Designer:**
1. Zone 1 two-column layout (480px trajectory + 240px co-primary at 1024×768)
2. Right column vertical stacking order (1B MDA alerts → 1C PMM → 1D Four-Framework)
3. MDA compact alert row format at 240px (3-line format: UD-F1)
4. Framework colors — conditional, pending MV-001 CVD result
5. "(exp)" confidence badge: 11px font (UD-F2), 4px right-of-datapoint placement
   (FA Agent must verify no SVG clip at 480px; may offset above-left if clipping occurs)
6. Control plane placeholder text: ≤ 11px font, ≤ 30% opacity, non-interactive

**UX Designer sign-off reference:** `docs/frontend/fa-brief-m9-instrument-cluster.md`
§UX Designer Sign-Off — 2026-05-22.

**Status:** Completed — sign-off recorded in FA brief (2026-05-22)
