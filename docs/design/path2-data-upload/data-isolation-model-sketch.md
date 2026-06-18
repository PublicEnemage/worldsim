---
name: path2-data-isolation-model-sketch
type: design-artifact
artifact: 3 of 3
sprint-group: M14-G6b
authored-by: Data Architect Agent
authored-date: 2026-06-18
gates: M15 scoping and M16 implementation of Path 2
intent-document: docs/process/intents/M14-G6b-2026-06-18-path2-design-groundwork.md
acceptance-criteria: AC-7, AC-8
issue-53-ref: Information Access Architecture (RBAC prerequisite)
---

# Data Isolation Model Sketch — Path 2 Ministry-Owned Data Upload

> **What this document is:** A written specification of the data isolation guarantee that
> Issue #53's Information Access Architecture must provide before Path 2 can be implemented.
> It is an internal architecture document — its audience is the Issue #53 design team and
> the M15/M16 implementation sprint, not the end user.
>
> **What it is not:** A schema design, a database migration plan, or an implementation
> specification. Those are M15/M16 work gated on Issue #53 resolution. This document
> specifies the isolation requirements so that Issue #53 scoping is grounded in Path 2's
> concrete needs.
>
> **Authority:** `docs/process/intents/M14-G6b-2026-06-18-path2-design-groundwork.md §AC-7, AC-8`

---

## 1. The Isolation Invariant

User-uploaded data (Path 2) must be fully isolated from shared platform state.

**Invariant statement:**

> A ministry analyst's uploaded data is scoped to scenarios she creates with it.
> It does not modify the shared source registry, does not appear in other users'
> data quality previews, and does not propagate to outputs produced by other users
> or scenarios — under any operation, including export, comparison, or federation.

**Formal statement:** Let U be a user upload, S_U be the set of scenarios created with
data from U, and P be the set of all platform-wide shared tables (including `source_registry`,
`entity_data_quality_coverage`, and any shared output cache). Then:

- The content of U must not appear in P
- The content of U must not appear in any API response for a request not originating from
  the uploading user, except where explicit sharing has been granted
- The content of U must be tagged with `USER_SUPPLIED` provenance in all output contexts
  (Grounding strip, initial-state API, exported outputs) so that any output derived from U
  is traceable to its non-registry provenance

This invariant is a hard requirement. A Path 2 implementation that satisfies the feature
specification (upload → map → scenario creates) but violates the invariant has not satisfied
Path 2's safety requirement.

---

## 2. Three Failure Modes of Insufficient Isolation

These are the concrete failure modes that an insufficiently isolated Path 2 implementation
would produce. Each represents a real harm to the platform's trustworthiness and to other
users.

### Failure Mode A — Uploaded data visible in other users' data quality previews

**What happens:** A Zambian ministry analyst uploads her government's internal reserve
position (2.8 months, 2026-06-18) to calibrate her scenario. Another user — a researcher
using WorldSim for Zambia analysis — opens the scenario creation form, selects ZMB, and
sees "Reserve coverage: 2.8 months · T2" in the data quality preview. The researcher
assumes this is IMF-observed data. It is not — it is the ministry's internal figure, not
publicly disclosed.

**Why this is a serious harm:**
1. It exposes the ministry's non-public position to a third party without consent
2. It misleads the researcher about the data's provenance (T2 observed vs. user-supplied)
3. It contaminates the platform's shared data signal — future users cannot trust that the
   data quality preview reflects only registered, verified sources

**Root cause:** User-supplied data was written into a shared table (e.g., appended to
`source_registry` or `entity_data_quality_coverage`) rather than to user-scoped storage.

**Detection:** Issue #53 must implement an isolation check at the data quality preview
endpoint: the response must not include any values whose `provenance_type` is `USER_SUPPLIED`.

### Failure Mode B — Uploaded data added to the shared source registry

**What happens:** During the upload and field-mapping flow, the backend creates a new
`source_registry` entry for the uploaded file (e.g., `source_id = "user-upload-2026-06-18-zmb"`).
This entry persists after the scenario is created and is visible to all users as a registered
source in any query against `source_registry`.

**Why this is a serious harm:**
1. The source registry is a curated list of platform-approved data sources with declared
   methodology, coverage, and quality tier. A user upload does not satisfy the registration
   criteria (documented methodology, coverage declarations, provenance audit).
2. Other scenarios using ZMB data may accidentally inherit a user-supplied source — if any
   automatic source selection logic prefers the most recently added source for an entity.
3. The shared registry becomes polluted with entries that cannot be audited, versioned, or
   removed without affecting the uploading user's scenario.

**Root cause:** The upload pipeline reuses the `source_registry` table for storage rather
than writing to a separate user-scoped storage layer.

**Detection:** A post-upload query against `source_registry` must not return any entry whose
`source_id` references a user upload. The source registry must remain read-only from the user
upload path.

### Failure Mode C — Exported outputs missing the `USER_SUPPLIED` tag

**What happens:** A researcher exports a scenario's output as PDF or JSON. The exported
reserve coverage indicator shows "2.8 months" without any indication that this value was
user-supplied rather than registry-sourced. The researcher shares the export with colleagues,
who cite it as IMF-observed data.

**Why this is a serious harm:**
1. Persona 1 (Programme Analyst) and Persona 6 (Investigative Journalist) require
   reproducibility. An export that does not carry the `USER_SUPPLIED` provenance label
   cannot be assessed for reproducibility.
2. A third party receiving the export has no mechanism to verify the reserve figure
   against a public source — but the export gives no signal that verification is impossible.
3. The platform's credibility depends on the accuracy of its provenance disclosure. An
   export that misrepresents provenance damages the tool's evidentiary standing.

**Root cause:** The export pathway reads indicator values without reading their `provenance_type`
field, omitting the badge from the rendered output.

**Detection:** The export format specification (part of the Path 2 implementation ADR) must
include `provenance_type` in the output schema for every indicator value, with `USER_SUPPLIED`
rendered as `· user-supplied` (plain-language badge) in the human-readable export format and
as `"provenance_type": "USER_SUPPLIED"` in the machine-readable export format.

---

## 3. What Issue #53 Must Resolve for Path 2

Issue #53 (Information Access Architecture) is the RBAC prerequisite for Path 2. The
following are the specific design decisions Issue #53 must make before Path 2 implementation
can be scoped:

### 3.1 The isolation boundary

**Decision required:** Where does user-uploaded data live — in the database, in session
storage, in a user-scoped schema partition, or in a separate object store?

**What Issue #53 must specify:**
- The storage boundary that prevents user-uploaded data from entering shared tables
- Whether the boundary is enforced at the application layer (before any write to the
  database) or at the database layer (separate table or schema with row-level security)
- What happens to user-uploaded data when a scenario is deleted: is the upload retained
  (for scenario recreation) or deleted with it?

**Why Path 2 cannot proceed without this decision:** The Path 2 backend implementation
must write user-uploaded values somewhere. Without a specified storage boundary, the
implementing agent must choose — and the choice has isolation consequences. The wrong choice
produces Failure Mode B.

### 3.2 The tenancy model

**Decision required:** Is user data scoped per-user (individual analyst) or per-institution
(Jordan Ministry of Finance)?

**Why it matters for Path 2:**
- **Per-user scope:** Eleni uploads her ministry's reserve data. Kofi Otieno (her colleague,
  also using WorldSim) cannot see or use her upload, even within the same institution. Eleni
  must share her scenario explicitly for Kofi to use it.
- **Per-institution scope:** The Ministry of Finance has an institution-level account. Any
  analyst at the ministry can see and use uploads made by other ministry analysts. The
  institution's shared data is isolated from other institutions but shared within the
  ministry's workspace.

**Path 2's isolation requirement is compatible with either model.** The requirement is that
user-supplied data is not visible to *other institutions and external users* — not that it
must be strictly per-user. But the tenancy model determines the API design for the access
control check (per-user token vs. per-institution token).

**What Issue #53 must specify:** Whether the tenancy unit for data isolation purposes is
the individual user account or an institutional workspace, and what the UX for workspace
membership looks like (invite, domain-verified, admin-managed).

### 3.3 The access control check at the data quality preview endpoint

**Decision required:** The `/api/v1/entities/{entity_id}/data-quality` endpoint currently
returns framework-level coverage quality from the shared source registry. After Path 2, an
additional check is required: if the calling user has user-supplied data for this entity, does
the data quality preview reflect it?

**Two options:**
- **Option A — Data quality preview is registry-only (recommended):** The endpoint
  returns only registry-sourced coverage. User-supplied data appears only in the Grounding
  strip after scenario creation, not in the pre-creation preview. This is the cleanest
  isolation: the shared preview is never contaminated by user-specific data.
- **Option B — Data quality preview is user-personalized:** The endpoint returns a
  blended response: registry coverage + "You have 3 user-supplied values for JOR."
  This requires the endpoint to be user-authenticated (currently it may not be) and to
  query user-scoped storage.

**Recommendation:** Option A. The data quality preview's purpose is to tell the analyst
about the platform's available data before she uploads anything. It answers the question
"what does the platform know about Jordan?" — not "what have I uploaded for Jordan?" The
distinction is clear and avoids contaminating the shared signal. Issue #53 should confirm
this option or document the rationale for Option B.

**What Issue #53 must specify:** Whether the data quality preview endpoint becomes
user-authenticated, or remains a public/entity-scoped endpoint that never returns
user-supplied data.

---

## 4. What Issue #53 is NOT Required to Solve for Path 2

The following are explicitly out of scope for Issue #53 as a Path 2 prerequisite. Scoping
Issue #53 to include these concerns would create unnecessary dependency and delay Path 2.

### 4.1 Output visibility tiers for different roles

Issue #53 may eventually define RBAC roles (analyst, viewer, admin). Path 2 does not
require role-based output visibility. The only visibility rule Path 2 requires is: uploaded
data is isolated to the uploader's (or uploader's institution's) scenarios. No role hierarchy
is needed — the isolation invariant is binary (scoped to the uploader, not accessible to
others without explicit sharing).

**What Issue #53 should not do for Path 2:** Define three-tier visibility (admin can see
all uploads, viewer cannot upload, analyst can upload). That scope is correct for a later
milestone but is not required for the Path 2 isolation guarantee.

### 4.2 Federation-level access control

Issue #53's scope may include future federation (multiple WorldSim instances sharing a
user registry). Path 2's isolation requirement is single-instance: user-uploaded data from
Instance A must not appear in Instance B. This is a forward-trace to federation architecture,
but it is not a requirement Issue #53 must solve before Path 2 is scoped. The isolation
invariant in §1 holds at the single-instance level; federation-level enforcement is a
separate concern.

### 4.3 Public API RBAC

If WorldSim exposes a public API (Issue #53 may be motivated in part by this), Path 2 does
not require the public API RBAC design to be complete before implementation. Path 2 uses
the existing authenticated API surface (the same API the frontend uses). No public, unauthenticated
API access to user-supplied data is required or permitted. If Issue #53's RBAC design covers
public API separately, Path 2 does not need to wait for that scope to be finalized.

### 4.4 Audit logging of data uploads

Path 2 will require that transformation steps are auditable (per `docs/DATA_STANDARDS.md
§Transformation Steps`). This is an application-layer audit requirement, not an RBAC
requirement. Issue #53 does not need to design the upload audit log. The implementing agent
for Path 2 holds R for the audit trail design (field mapping → transformation → stored value
chain).

---

## 5. Database Schema Implication (for M15/M16 Design Reference)

This sketch identifies a database schema implication without designing the schema. The
following constraint must be addressed at M15/M16 design time.

**Constraint:** User-uploaded data requires storage separate from `source_registry`.

The `source_registry` table is a shared, curated platform table. Its rows represent
platform-approved data sources with documented methodology, coverage, and quality tier.
User uploads cannot be stored in this table (see Failure Mode B above).

**Candidate storage approaches for M15/M16 design time:**

| Approach | Description | Trade-off |
|---|---|---|
| **`user_supplied_data` table** | A new application table with foreign key to the user account and a nullable foreign key to the scenario. Rows contain indicator-value-provenance tuples. | Simple; no shared-table risk; straightforward access control check. Requires a new table and migration. |
| **JSONB column on `scenarios`** | User-supplied indicator values stored as JSONB in the existing `scenarios` table, alongside the scenario's other metadata. | Avoids a new table; keeps user-supplied data co-located with the scenario it modifies. Access control is inherited from scenario-level access. Query performance for multi-scenario analysis may degrade. |
| **Separate schema partition** | User-uploaded data lives in a `user_data` schema with PostgreSQL row-level security. | Strong database-enforced isolation; more complex migration and ORM setup. Appropriate if federation or multi-tenancy is planned. |

**This sketch does not choose among these approaches.** The choice is M15/M16 work and
depends on Issue #53's tenancy model decision (§3.2 above). A per-institution workspace
model may prefer the separate schema partition approach (stronger isolation); a per-user
model may use the `user_supplied_data` table for simplicity.

**What must be true of any schema choice:**
- The `source_registry` table is not written to during a user upload operation
- The user-supplied data store includes the `provenance_type = 'USER_SUPPLIED'` field on
  each indicator value
- The access control check at the `/initial-state` API endpoint can join user-supplied
  storage to the response for authorized requests, without making user-supplied data
  available to unauthorized requests

---

## 6. Path 2 Prerequisites — Summary for Issue #53 Scoping

Issue #53 must resolve exactly these three questions before Path 2 implementation is scoped:

| Decision | Required for Path 2 | Risk if not decided |
|---|---|---|
| Isolation boundary — where does user-uploaded data live? | The backend cannot write user-supplied values without a defined storage target | Failure Mode B (registry contamination) |
| Tenancy model — per-user or per-institution? | The access control check at every relevant endpoint depends on the tenancy unit | API design is undefined; access control cannot be implemented |
| Access control check at the data quality preview endpoint — Option A or B? | The preview endpoint either becomes user-aware or remains registry-only | Without a decision, the implementing agent defaults to the wrong option |

Everything else listed in §4 (output visibility tiers, federation-level access, public API
RBAC, audit logging) is out of scope for the Issue #53 prerequisite and must not be used
to delay Path 2 scoping.

---

*Artifact 3 of 3 for M14-G6b. Authored by Data Architect Agent. Filed at
`docs/design/path2-data-upload/data-isolation-model-sketch.md`. Acceptance criteria covered:
AC-7 (isolation invariant, three failure modes, Issue #53 requirements), AC-8 (explicit
out-of-scope list for Issue #53, preventing scope creep). See
`docs/process/intents/M14-G6b-2026-06-18-path2-design-groundwork.md` for the full AC list
and EL review gate.*
