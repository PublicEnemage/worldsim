# Exceptions Registry

Append-only. Each exception has a unique EX-NNN identifier.

An exception is a time-bounded, EL-approved deviation from a project specification,
threshold, architectural principle, or security requirement. Exceptions are not
permanent — every exception has an expiry condition. At expiry, the exception is either
resolved (specification restored), renewed (new EL decision required), or promoted to
a permanent specification change (which requires the same process as the original
specification).

**Types:** `threshold` | `architecture` | `security` | `process` | `data`

**Expiry discipline:** An exception that passes its expiry milestone without a renewal
or resolution decision is a compliance finding. File in `docs/compliance/scan-registry.md`
as a SCAN entry at the expired milestone's exit gate. The PI Agent holds R for flagging
expired exceptions at sprint exit.

---

## Exception Index

| ID | Type | Summary | Expiry | Status |
|---|---|---|---|---|
| EX-001 | threshold | AC-009 CI throttled render threshold raised 100ms → 200ms | M17 exit | Active |

---

## EX-001 — AC-009 CI throttled render threshold

**Type:** threshold
**Status:** Active
**EL Approved:** 2026-06-24
**Expiry:** M17 exit

At M17 sprint entry, this exception must be explicitly renewed (new EL decision,
new expiry) or resolved. An exception that reaches M17 exit without a decision is
a compliance finding — see expiry discipline above.

### Specification

`docs/frontend/fa-brief-m9-instrument-cluster.md §AC-009`:
AC-009 pass criterion: Mode 3 full component set render ≤ **100ms** on CI 4× throttled
profile.

### Approved Deviation

AC-009 CI throttled threshold raised to **200ms** for the duration of this exception.
The ProBook hardware validation target (MV-002, no throttle) remains ≤ 100ms —
this exception applies to the CI throttled gate only.

### Rationale

AC-009 silently skipped since Mode 3 shipped in M12 (NM-058 — wrong testid). When
corrected in M16-G6, the first real measurement produced **179ms** on the 4× throttled
CI runner. Chief Engineer assessment (2026-06-24):

- Browser-side performance marks are sound; 179ms is real (~40ms estimated at 1× speed)
- Mode 3 renders ~15 additional Recharts series elements on activation; ~40ms at 1× is
  not a usability problem for any target persona
- Threshold at 200ms (179ms + 21ms headroom) preserves regression sensitivity — any
  change that pushes past 200ms on 4× throttle represents a substantial regression
- Raising to 250ms or higher loses meaningful signal
- Genuine optimization (Recharts memoization, lazy ControlPlane mounting) is non-trivial
  and appropriate for a dedicated future sprint

### Baseline

| Measurement | Value | Environment | Date |
|---|---|---|---|
| First real AC-009 CI run (post NM-058 fix) | 179ms | GitHub Actions (ubuntu-latest, 2-core), 4× CPU throttle | 2026-06-24 |

### Linked Issue

Mode 3 render optimization enhancement issue: filed at M16-G6 exit.
Carries into M17 planning as a named obligation. If M17 exits without delivering the
optimization, a new EL decision is required to renew EX-001.

### Renewal / Resolution Conditions

At M17 sprint entry (or earlier if optimization is delivered mid-M17):

- **Resolve:** Mode 3 render optimization delivered and CI AC-009 passes at ≤ 100ms.
  Update Status to Resolved; add Resolution Record below.
- **Renew:** Optimization not delivered. New EL decision required with updated expiry.
  Renewal without a new EL decision is a process violation.
- **Promote:** If 200ms is confirmed as the correct specification (hardware measurements
  and CE assessment support it), file a permanent specification change via the FA brief
  amendment process and close this exception.

---

## Registry Maintenance

Exception entries are permanent — never delete or modify a closed entry.
When an exception is resolved or renewed, update **Status** in the index table and
append a **Resolution Record** or **Renewal Record** to the entry body (date, outcome,
approver).

Expiry ≠ resolution. An expired, unrenewed exception is a compliance finding.
