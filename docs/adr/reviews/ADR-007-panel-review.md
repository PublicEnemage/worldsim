# ADR-007 Panel Review

> **Artifact type:** ADR Panel Review
> **ADR:** ADR-007 — Synthetic Data Framework
> **ADR file:** `docs/adr/ADR-007-synthetic-data-framework.md`
> **Status:** Accepted — EL decision recorded 2026-05-23
> **Review date:** 2026-05-23
> **Convention:** `docs/adr/reviews/ADR-NNN-panel-review.md`

---

## Panel

| Reviewer | Role | Status |
|---|---|---|
| Chief Methodologist (DIC) | C — authored consultation, methodological foundation | Consultation complete ✓ (PR #373, 2026-05-19) |
| Data Architect Agent | C — `Quantity` schema extension, comparison group registry structure | Conditional sign-off ✓ |
| Development Economist (DIC) | C — human development indicator disclosure requirements, MDA behavior | Conditional sign-off ✓ |
| Engineering Lead | A — accountable on all ADR decisions | Accepted ✓ (2026-05-23) |

---

## Findings Register

| ID | Source | Type | Severity | ADR change required? | Status |
|---|---|---|---|---|---|
| CM-F1 | Chief Methodologist | Consultation document is the founding review; all seven decisions validated | Substantive — source | No (consultation doc is authoritative) | Resolved ✓ |
| DA-F1 | Data Architect | Comparison group registry: no format spec or schema reference in ADR | INCORPORATE | Yes — add one-sentence registry format note | Resolved ✓ |
| DA-F2 | Data Architect | `Quantity` field count: Consequences says 4 fields but lists `is_synthetic` which may already exist | Confirm | Yes — clarify `is_synthetic` is new | Resolved ✓ |
| DA-F3 | Data Architect | `SyntheticDataEngine` has no ADR-defined boundary with `BandingEngine` | Non-blocking | No — FA brief required before implementation | Resolved ✓ |
| DE-F1 | Development Economist | Mode 3 suppression of Tier 4 HD signals: correct but rationale should be explicit | INCORPORATE | Yes — add rationale sentence to Section 5 | Resolved ✓ |
| DE-F2 | Development Economist | Reverse-false-positive risk: synthetic data conforming to baseline could validate suspect official stats | Logged — no action | Add to Anomaly Detection open risks note | Resolved ✓ |
| DE-F3 | Development Economist | Per-indicator badge: poverty and cohort-level indicators need badge even when derived from synthetic aggregate | Non-blocking | No — implementation gate; FA brief | Resolved ✓ |

---

## Chief Methodologist Review (CM-F1)

The Chief Methodologist consultation (`docs/architecture/synthetic-data-consultation.md`, PR #373, 2026-05-19) is the founding document for this ADR. The consultation answered five questions across: method hierarchy and selection conditions; epistemically honest presentation and disclosure requirements; the meaninglessness threshold; MDA alert interaction by tier; and anomaly detection scope and governance. The ADR sections map directly to the consultation answers.

The CM's methodological positions are validated for the WorldSim use case and are not reopened by this review. The two methodologically substantive points from the consultation carry forward:

1. **Calibrated honesty, not blanket refusal**: The framework correctly distinguishes between data poverty (which the tool must work through) and hopeless uncertainty (where Structural Absence Declaration is correct). The meaninglessness threshold conditions are appropriately composite.

2. **Anomaly detection is dual-use**: The TSC governance gate before production deployment is essential, not optional. This must not be treated as a deferred nice-to-have — it is a condition of the feature's existence.

**CM sign-off:** Consultation complete. The ADR faithfully represents the consultation's conclusions. No additional CM review required at acceptance.

---

## Data Architect Review

### DA-F1 — Comparison Group Registry Format (INCORPORATE)

**Finding:** Section 1 and the Consequences section both reference a "comparison group registry" as new infrastructure required before Method A deployment. The ADR does not specify what format this registry takes, whether it follows the existing `source_registry` schema pattern, or where it lives.

Without a format specification, the implementing engineer must invent the format — creating a second undocumented registry that may conflict with or duplicate the existing `source_registry` architecture.

**Required ADR addition:** Add one sentence to the Consequences section: "The comparison group registry follows the existing `source_registry` pattern in `docs/schema/database.yml` and is managed by the Data Quality Agent (Issue #300); a new registry table definition is required before Method A deployment."

**Status:** Applied (see ADR-007 Consequences, comparison group registry note).

### DA-F2 — `is_synthetic` Field Clarity (INCORPORATE)

**Finding:** The Consequences section says "`Quantity` gains four new fields: `is_synthetic: bool`, `synthetic_method: str | None`, `comparison_group_id: str | None`, `holdout_validated: bool | None`." The Quantity schema in `docs/schema/simulation_state.yml` should be checked: if `is_synthetic` already exists (it may, as a forward-compatibility placeholder), the migration only adds three new fields. The ADR should be unambiguous.

**Required ADR addition:** Add a note confirming `is_synthetic` is new (not a rename) and that the Alembic migration adds all four fields as new columns.

**Status:** Applied (see ADR-007 Consequences note on `is_synthetic`).

### DA-F3 — SyntheticDataEngine / BandingEngine boundary (Non-blocking)

**Finding:** The ADR states that BandingEngine does not change and synthetic inference bands are "a separate output alongside model uncertainty bands." This is architecturally sound, but the interface between `SyntheticDataEngine` and the scenario runner is not specified. A Frontend Architect brief should define the interface before implementation.

**Required action:** FA brief required before `SyntheticDataEngine` implementation begins. No ADR change.

**Data Architect sign-off:** Conditional — subject to DA-F1 and DA-F2 applied before implementation. Schema extension is compatible with existing `quantity_to_jsonb` / `quantity_from_jsonb` serialization contracts. No blocking structural issues.

---

## Development Economist Review

### DE-F1 — Mode 3 Tier 4 Suppression Rationale (INCORPORATE)

**Finding:** Section 5 states "In Mode 3 (Active Control), Tier 4 exploratory signals are suppressed from the session entirely." This is correct — Mode 3 is real-time steering and the user cannot simultaneously manage low-confidence data quality signals. However, the rationale is not explicit in the ADR text. A future implementer might soften this rule without understanding why it was set.

Human development indicators near MDA floors (poverty rate, child mortality) are exactly the indicators most likely to be synthetic in data-poor contexts. Suppressing their Tier 4 signals in Mode 3 means an analyst making real-time decisions on a country with poor HD data cannot rely on the instrument cluster to surface HD deterioration warnings. This is the right trade-off — a false alarm from a low-confidence synthetic HD signal could cause worse decisions than no signal — but the rationale must be on record.

**Required ADR addition:** Add rationale sentence in Section 5, Mode 3 Tightening paragraph: "This suppression is intentional — in Mode 3, a false HD deterioration signal from a low-confidence synthetic estimate causes worse decisions than a missing signal. Analysts who need Tier 4 signals should shift to Mode 2 for data quality review before Mode 3 steering."

**Status:** Applied.

### DE-F2 — Reverse False-Positive Risk (Logged)

**Finding:** Section 7 (Anomaly Detection) documents the false positive risk (flag fires when there is no manipulation). There is a reverse risk: when a country's official data closely matches the synthetic baseline, an analyst might interpret this as validation of their data quality. In a negotiation context, "our data matches the WorldSim synthetic baseline" is not a valid quality certification — the baseline itself has uncertainty. This is not a reason to change the ADR, but should be documented as an open risk.

**Required action:** Add a brief note in Section 7 open risks or Consequences: "Synthetic baseline conformance is not a data quality certification. Close agreement between official data and the synthetic baseline is a coincidence, not a validation."

**Status:** Applied to ADR-007 Anomaly Detection governance note.

### DE-F3 — Per-Indicator Badge on Derived Cohort Indicators (Non-blocking)

**Finding:** The per-indicator badge requirement (Section 2) applies at the indicator level. For human development cohort-level outputs (unemployment by cohort, poverty by age group), the cohort-level number may be derived from a synthetic aggregate. The badge must appear on the cohort-level output, not just on the aggregate indicator. This is a frontend implementation constraint, not an ADR structural issue.

**Required action:** FA brief to include: "Per-indicator synthetic badge applies to all displayed data slots, including cohort-level derived outputs, when any contributing indicator is synthetic."

**Development Economist sign-off:** Conditional — subject to DE-F1 and DE-F2 applied, and FA brief commitment on DE-F3.

---

## Engineering Lead Decision

**ADR-007 is accepted.** The seven decisions in the ADR are sound, the methodological foundation is the Chief Methodologist consultation (complete), and the three panel INCORPORATE items have been applied. The ADR enters ACCEPTED status as of 2026-05-23.

**Conditions carried forward as implementation prerequisites (not blocking acceptance):**
- FA brief required before `SyntheticDataEngine` implementation (covers DA-F3 and DE-F3)
- Comparison group registry table definition required before Method A deployment (DA-F1)
- Anomaly detection feature requires TSC sign-off before production deployment (Section 7 governance gate — not a M9 or M10 item)

**License:** ACCEPTED — Valid Until: Milestone 10 — Engine Integrity and Instrument Delivery.
