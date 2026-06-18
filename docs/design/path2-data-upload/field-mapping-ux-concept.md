---
name: path2-field-mapping-ux-concept
type: design-artifact
artifact: 1 of 3
sprint-group: M14-G6b
authored-by: UX Designer Agent
authored-date: 2026-06-18
gates: M15 scoping and M16 implementation of Path 2
intent-document: docs/process/intents/M14-G6b-2026-06-18-path2-design-groundwork.md
acceptance-criteria: AC-1, AC-2, AC-3, AC-4
---

# Path 2 Field Mapping UX Concept — Ministry-Owned Data Upload

> **What this document is:** A step-by-step specification of the field mapping workflow for
> Path 2 (ministry-owned data upload), sufficient for a frontend engineer to prototype the UI
> without consulting the authoring agent. It is a design specification, not a functional
> implementation.
>
> **Binding constraint:** The full workflow — upload file → map fields → confirm transformation
> → review provenance display → create scenario — must complete within 5 minutes for a
> ministry analyst who is not a software engineer, working from a 10-variable standard-format
> spreadsheet. Every step has a timing annotation. The 5-minute ceiling reflects the
> Preparatory entry state: she is building the scenario before a negotiation session, not
> under real-time pressure, but her preparation time is finite.

---

## 1. Entry Point

**Where Path 2 begins:** The scenario creation form, after the analyst has selected an entity
and steps. A new affordance appears below the standard parameter fields:

```
  Entity:          [Jordan (JOR)  ▾]
  Steps:           [8]
  Fiscal mult.:    [1.30]
  Political econ:  [☑ enabled]

  ──────────────────────────────────────────
  Starting values   ○ Use preloaded data  (default)
                    ● Upload ministry data
  ──────────────────────────────────────────

  [Upload spreadsheet or CSV...]
```

Selecting "Upload ministry data" replaces the default-data path for **initial state only**.
Control inputs (fiscal multiplier, political economy settings) are unaffected; they remain
the analyst's scenario parameters. The Grounding strip will show which indicators were
supplied by the ministry and which came from the preloaded source registry.

**Triggers Path 2 workflow when:** analyst clicks "Upload spreadsheet or CSV…"

---

## 2. Step-by-Step Workflow

### Step 1 — File Upload (≤ 30 seconds)

**What the analyst sees:**

```
  Upload Ministry Data — Step 1 of 4

  ┌────────────────────────────────────────────────────┐
  │                                                    │
  │   Drag and drop your spreadsheet here, or          │
  │   [Browse files]                                   │
  │                                                    │
  │   Accepted formats: .xlsx, .xls, .csv              │
  │   Max file size: 5 MB                              │
  │                                                    │
  └────────────────────────────────────────────────────┘

  ⓘ  Your data stays private. It is scoped to your
     session and is not added to the platform's
     shared source registry.
```

**What happens after upload:**
The system parses the first row (header) and the first data row to extract column names and
detect data types. It does not yet infer canonical variable mappings — that is Step 2.

**Loading state:** "Reading your file… (column headers detected: 12)"

**Error states:**
- File cannot be parsed: "This file cannot be read. Check that it is a standard spreadsheet
  or CSV and that the first row contains column headers. [Try again]"
- File has no header row detectable: "No column headers found. Please ensure row 1 contains
  variable names. [Try again]"
- File exceeds size limit: "File is too large (max 5 MB). Please reduce the number of rows
  or split across two uploads. [Try again]"

**Timing target:** File selection and upload: ≤ 15 seconds. Parsing feedback: ≤ 5 seconds.
Subtotal: **≤ 30 seconds.**

---

### Step 2 — Map Your Data (≤ 90 seconds for 10 variables)

This is the highest Layer 3 risk step in the entire Path 2 workflow. The ministry's column
names will not match WorldSim's canonical variable names. The transformation (unit conversion,
sign convention) must be made explicit and confirmed before proceeding. A mapping error that
goes undetected produces a misconfigured scenario cited with false confidence.

**What the analyst sees:**

```
  Upload Ministry Data — Step 2 of 4: Map Your Data

  Your column                 WorldSim variable                  Transformation
  ─────────────────────────────────────────────────────────────────────────────
  "FX reserves (USD bn)"  →   reserve_coverage_months        ✓  4.20 bn ÷ import
                                                                 rate 1.50 bn/mo
                                                                 = 2.80 months
                              [Change ▾]                        [Edit]

  "Budget deficit % GDP"  →   fiscal_balance_pct_gdp         ✓  Deficit 3.2 entered
                                                                 as positive; stored
                                                                 as −3.2 (WorldSim
                                                                 sign convention)
                              [Change ▾]                        [Edit]

  "Current account % GDP" →   current_account_pct_gdp        ✓  Direct mapping.
                                                                 No conversion.
                              [Change ▾]                        [Edit]

  "Unemployment rate (%)" →   unemployment_rate_pct          ✓  Direct mapping.
                              [Change ▾]                        [Edit]

  "External debt (USD bn)">   [No match found — select below]    —
                              [Select WorldSim variable ▾]       [Skip this column]

  "HDI score"             →   [Multiple matches — select one]    —
                              human_development_index      ← (recommended)
                              hdi_composite_score
                              [Select ▾]                         [Skip this column]

  "Reserves (months)"     →   reserve_coverage_months        ⚠  Possible duplicate:
                                                                 "FX reserves (USD bn)"
                                                                 maps to this variable
                                                                 above. If these are the
                                                                 same indicator in
                                                                 different units, keep
                                                                 one only.
                              [Remove this row]                  [Keep both — I intend
                                                                  to override]

  ─────────────────────────────────────────────────────────────────────────────
  3 columns skipped (not mapped):  "Notes", "Date", "Reviewer"
  These columns will not be included in the scenario.       [Show skipped ▾]

  ─────────────────────────────────────────────────────────────────────────────
  [← Back]                                    [Confirm mapping and continue →]
```

**Column-to-variable matching logic:**
1. Exact match on canonical variable name: auto-confirmed, shown as ✓
2. High-confidence semantic match (fuzzy name similarity + unit compatibility): auto-suggested,
   shown as ✓ with "[Change ▾]" available
3. No match: "No match found — select below" row with a searchable [Select WorldSim variable ▾]
4. Multiple matches: "Multiple matches — select one" row with the highest-confidence suggestion
   pre-selected and a selector showing alternatives
5. Duplicate detection: same canonical variable mapped from two source columns shows ⚠ with
   an explicit resolution prompt

**Skipped columns:** Non-quantitative or unrecognized columns (dates, notes, reviewer names)
are silently excluded from mapping and listed in the collapsed "3 columns skipped" footer.
The analyst can expand to confirm skipped columns are correctly excluded.

**[Select WorldSim variable ▾] selector:**
Searchable dropdown organized by framework:
```
  Financial:
    reserve_coverage_months — Reserve coverage (months of import)
    fiscal_balance_pct_gdp — Fiscal balance (% GDP)
    current_account_pct_gdp — Current account balance (% GDP)
    external_debt_pct_gdp — External debt stock (% GDP)
    ...
  Human Development:
    unemployment_rate_pct — Unemployment rate (%)
    ...
  [Search all variables...]
```

**Timing target:** Auto-mapping renders: ≤ 5 seconds after Step 1. Analyst review + manual
resolution of 3 unmatched/ambiguous columns: ≤ 85 seconds.
Subtotal: **≤ 90 seconds.**

---

### Step 3 — Confirm Transformation Details (≤ 90 seconds)

Before proceeding, the analyst reviews a human-readable summary of every transformation that
will be applied to her data. This is the explicit confirmation gate required by the DATA_STANDARDS
`§Transformation Steps` audit trail obligation.

**What the analyst sees:**

```
  Upload Ministry Data — Step 3 of 4: Confirm Transformations

  You are about to apply these transformations. Review each one before confirming.

  reserve_coverage_months
    Your value:    4.20 USD billions  (from "FX reserves (USD bn)")
    Conversion:    ÷ import rate of 1.50 USD billion/month (Jordan 2023, IMF BOP)
    WorldSim value: 2.80 months of import coverage
    [Edit import rate]

  fiscal_balance_pct_gdp
    Your value:    3.2 (deficit entered as positive)
    Sign applied:  × −1 (WorldSim convention: surplus positive, deficit negative)
    WorldSim value: −3.2% GDP
    [No edit needed]

  current_account_pct_gdp
    Your value:    −6.1% GDP
    Conversion:    None — direct mapping
    WorldSim value: −6.1% GDP
    [No edit needed]

  unemployment_rate_pct
    Your value:    10.8%
    Conversion:    None — direct mapping
    WorldSim value: 10.8%
    [No edit needed]

  external_debt_pct_gdp
    Your value:    74.3 USD billions  (from "External debt (USD bn)")
    Conversion:    ÷ GDP of 48.0 USD billion (Jordan 2023, World Bank WDI)
    WorldSim value: 154.8% GDP
    [Edit GDP figure]

  human_development_index
    Your value:    0.732
    Conversion:    None — direct mapping (dimensionless 0–1 scale)
    WorldSim value: 0.732
    [No edit needed]

  ─────────────────────────────────────────────────────────────────────────────
  These values will override the preloaded source registry values for Jordan (JOR)
  for this scenario only. The Grounding strip will label them "user-supplied."

  ⚠  This scenario includes ministry-supplied starting values. Reproduction
     requires the uploaded dataset. [Learn more about reproducibility]

  ─────────────────────────────────────────────────────────────────────────────
  [← Back]                                           [Apply and create scenario →]
```

**[Edit import rate] / [Edit GDP figure]:** Inline editable field that accepts a corrected
reference rate (with a link to the source the system used to derive the default). The analyst
is not required to correct these; the system's reference values are pre-filled and the analyst
confirms or overrides.

**Reproducibility caveat placement:** The caveat appears in Step 3 at the confirmation gate —
the last decision point before scenario creation. It also appears in the Grounding strip after
scenario creation (Step 4 below). It is not surfaced in Steps 1 or 2 to avoid noise during
the mapping process.

**Timing target:** Review 6 transformed indicators: ≤ 60 seconds. Edit one reference rate
if needed: ≤ 30 seconds.
Subtotal: **≤ 90 seconds.**

---

### Step 4 — Provenance Review in Grounding Strip (≤ 60 seconds)

The scenario is created. The analyst is brought to the instrument cluster with the new scenario
loaded. The Grounding strip opens automatically (or is surfaced by Zone 0) to show the
blended provenance state.

**What the analyst sees in the Grounding Strip (Zone 2):**

```
  Grounding  ▲                              Jordan (JOR) · 2023 · Mode 2

  Financial framework                      [2 user-supplied · 2 observed]
  ├── Reserve coverage: 2.80 months   — Ministry of Finance (internal, 2026-06-18) · T2 · user-supplied
  ├── Fiscal balance:  −3.2% GDP      — Ministry of Finance (draft budget, 2026-06-18) · T2 · user-supplied
  ├── Current account: −6.1% GDP      — IMF Article IV 2023 · T2 · observed
  └── External debt:  154.8% GDP      — Ministry of Finance (internal, 2026-06-18) · T2 · user-supplied

  Human Development framework              [1 user-supplied · 1 observed]
  ├── Unemployment:    10.8%          — Ministry of Finance (internal, 2026-06-18) · T2 · user-supplied
  └── HDI:             0.732          — UNDP Human Development Report 2023 · T2 · observed

  ⚠  This scenario includes ministry-supplied starting values.
     Reproduction requires the uploaded dataset.  [Learn more]
```

**Badge convention:**
- `· user-supplied` — right-aligned badge in the Grounding strip citation line (see
  `user-supplied-provenance-spec.md` for the full display contract)
- `[2 user-supplied · 2 observed]` — per-framework count chip at framework header level,
  matching the existing `[T2 · IMF]` chip pattern

**Timing target:** Grounding strip loads: ≤ 3 seconds. Analyst review of provenance state:
≤ 60 seconds.
Subtotal: **≤ 60 seconds.**

---

## 3. End-to-End Timing Summary

| Step | Content | Target |
|---|---|---|
| Step 1 — File upload | Select file, upload, parse | ≤ 30 s |
| Step 2 — Map fields | Auto-mapping + analyst resolves 3 gaps | ≤ 90 s |
| Step 3 — Confirm transformations | Review 6 transformed values, confirm | ≤ 90 s |
| Step 4 — Provenance review | Grounding strip review | ≤ 60 s |
| **Total** | 10-variable standard-format spreadsheet | **≤ 4 min 30 s** |

The 5-minute ceiling (300 seconds) includes 30 seconds of headroom for file selection delay,
network latency at creation, and modal transitions.

---

## 4. Both Field Mapping Failure Modes

### Failure Mode A — No Canonical Match Found

When the system cannot find any plausible canonical variable for a column:

```
  "Long-term debt service (USD mn)"  →  [No match found]
                                         ─────────────────────────────────────
                                         WorldSim does not have a canonical
                                         variable for this column name.

                                         [Search for a variable ▾]   [Skip column]
```

**What the analyst can do:**
1. **Search for a variable** — opens the full variable selector (searchable, organized by
   framework). She can manually identify the best-fit canonical variable.
2. **Skip column** — the column is excluded from the upload. A note in the Step 3 summary
   states "2 columns excluded — no canonical match found."

**No silent inclusion:** An unmatched column is never silently included using a fallback
variable. If the analyst skips a column that would have been material (e.g., she had a
long-term debt service figure that should have mapped to `external_debt_service_ratio`), the
consequence is that this indicator remains at its preloaded registry value — not that it is
mapped incorrectly. The analyst must make an explicit decision.

### Failure Mode B — Ambiguous Match (Multiple Candidate Variables)

When two or more canonical variables are plausible for the same column name:

```
  "Government spending (% GDP)"  →  [Multiple matches — select one]
                                     ─────────────────────────────────────
                                     ● government_expenditure_pct_gdp  ← recommended
                                     ○ fiscal_balance_pct_gdp
                                     ○ government_consumption_pct_gdp

                                     The recommended match is based on column name
                                     similarity. Review descriptions before confirming.

                                     [View variable descriptions]   [Confirm selection]  [Skip]
```

**Why recommended is pre-selected:** The system ranks candidates by column-name fuzzy match
score. The top-ranked candidate is pre-selected but not auto-confirmed — the analyst must
click "Confirm selection" to proceed. The distinction matters: "Government spending" could be
government consumption (national accounts definition) or total government expenditure
(budget definition). A ministry spreadsheet could use either. The analyst is the authoritative
source on which of her variables this column represents.

**[View variable descriptions]:** Inline expansion showing the WorldSim definition for each
candidate (unit, typical range, framework): "government_expenditure_pct_gdp — Total
government expenditure including transfers and interest payments, as % of GDP. Financial
framework. Typical range: 18–45% GDP for MENA economies."

---

## 5. Reproducibility Caveat — Placement Specification

The reproducibility caveat — "This scenario includes ministry-supplied starting values.
Reproduction requires the uploaded dataset." — appears in two locations:

**Location 1 — Step 3 (Confirm Transformations) confirmation gate:**
Displayed immediately above the [Apply and create scenario →] button. The analyst cannot
confirm without seeing the caveat. It is not a modal — it is inline text. The caveat is
readable, not dismissible (no close button). It does not block the creation action; it
informs the analyst's choice.

**Location 2 — Grounding strip after scenario creation:**
Displayed as a ⚠ banner at the bottom of the Grounding strip, below the framework
sections. It appears for any scenario whose Grounding strip contains at least one
`user-supplied` indicator. It is permanent (not dismissible). It links to a "Learn more"
page explaining what reproducibility means in this context and who else can use the scenario.

**What "Learn more" contains:**
- "Who can see this scenario: [currently only you — see your sharing settings]"
- "Can others reproduce this scenario? Only if you share the original uploaded dataset."
- "What happens if I share the scenario without the dataset? Others can run it using the
  same starting values you supplied, but they cannot verify those values against a public
  source."
- "Is this disclosed in the output? Yes. Every output display showing a user-supplied
  indicator carries the · user-supplied label in the citation."

**Location 3 — Exported outputs (out of scope for this document):**
The export/PDF/share pathway must carry the caveat. This is an output-layer design concern
deferred to the Path 2 implementation ADR. The caveat text is specified here so the
implementation ADR can reference it.

---

## 6. Kryptonite Constraint Confirmation

The mapping workflow — as specified above — can be completed in under 5 minutes by a
ministry analyst who is not a software engineer, using a standard spreadsheet export format,
without a data scientist or IT specialist.

Evidence:
- Step 1 (upload) is a standard file-picker action
- Step 2 (mapping) auto-resolves exact and high-confidence matches; the analyst resolves
  only unmatched and ambiguous columns (expected ≤ 3 of 10 for a standard fiscal spreadsheet)
- Step 3 (confirm) shows human-readable transformation summaries, not formula strings;
  the analyst reviews derived values, not derivation code
- The [Edit import rate] affordance gives her a correction path without requiring her to
  understand the unit conversion calculation
- The 30 seconds of headroom in the 5-minute total accounts for analyst reading time

The specialist mediation condition is not met: no data scientist, no IT specialist, no
command-line tool required.

---

## 7. Out of Scope for This Concept

The following design questions are deferred to the Path 2 implementation ADR:

- **Multiple-file uploads:** This concept covers a single spreadsheet upload. Multi-file
  upload (e.g., one file for fiscal data and one for demographic data) is out of scope.
- **Template downloads:** Pre-filled spreadsheet templates by data category (fiscal template,
  reserve template) that pre-name columns with WorldSim canonical variable names. Referenced
  in `docs/ux/user-journeys.md §GA-02` as a path to reducing Step 2 time below 90 seconds
  for standard cases. Out of scope for this concept.
- **Versioning and re-upload:** If the analyst uploads new data for a scenario that already
  has user-supplied starting values, the versioning behavior (replace vs. append) is out of
  scope.
- **Sharing and access control:** Who can view a scenario whose starting values are
  user-supplied is governed by Issue #53 (Information Access Architecture). Out of scope.
- **Mobile and tablet:** This concept targets desktop (1280×900 and above). Mobile path 2
  upload is out of scope.

---

*Artifact 1 of 3 for M14-G6b. Authored by UX Designer Agent. Filed at
`docs/design/path2-data-upload/field-mapping-ux-concept.md`. Acceptance criteria covered:
AC-1 (step-by-step workflow with timing ≤ 5 min), AC-2 (field mapping step explicit detail),
AC-3 (both failure modes addressed), AC-4 (reproducibility caveat placement). See
`docs/process/intents/M14-G6b-2026-06-18-path2-design-groundwork.md` for the full AC list
and EL review gate.*
