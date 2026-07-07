# WorldSim Analytical Evidence Portfolio — Entry Template

> **Authority:** Analytical Evidence Agent (AEA), External Intelligence Layer  
> **File location:** `docs/evidence/TEMPLATE.md`  
> **Versioned:** This document is the canonical template. Do not modify it to create an entry — copy it and populate the copy.  
> **Naming convention for entries:** `AEP-NNN-ENTITY-YYYY.md` where NNN is a three-digit sequential ID assigned from the AEA's running index, ENTITY is the ISO 3166-1 alpha-3 code, and YYYY is the scenario start year.  
> **Reference:** `docs/evidence/analytical-framework.md` governs calibration family taxonomy, fidelity tier definitions, temporal blindfold protocol, and the error envelope principle. Read it before populating this template.

---

## 1. Header

| Field | Value |
|---|---|
| **Scenario ID** | `AEP-NNN-ENTITY-YYYY` |
| **Entry type** | `Type A — Historical Replay` \| `Type B — Counter-Factual Branch` |
| **Entity** | [ISO 3166-1 alpha-3 code, e.g. `GRC`] |
| **Entity name (common)** | [e.g. Greece] |
| **Scenario start year** | [YYYY] |
| **Branch point year** | [YYYY — the year at which the counter-factual path diverges from historical actuals; omit if Type A] |
| **Branch point step** | [Step number in the harness run at which the branch is introduced; omit if Type A] |
| **Fidelity tier (entry ceiling)** | `DIRECTION_ONLY` \| `MAGNITUDE` \| `CALIBRATED_CI` |
| **Calibration family** | `SSA-LIC` \| `EURO-AREA` \| `LATAM-EM` \| `SOUTH-SE-ASIAN` |
| **Temporal blindfold status** | `BLINDED — config committed YYYY-MM-DD before run` \| `UNBLINDED — acknowledged; weight reduced` \| `N/A — Type A` |
| **Date run** | [YYYY-MM-DD] |
| **Harness version** | [e.g. `v0.19.0`] |
| **Primary analyst** | [Agent name or `AEA` for AEA-commissioned runs] |

---

## 2. Historical Context

*150–300 words. Answer three questions in sequence: (1) Why does this scenario matter — what was at stake politically, economically, and for human welfare? (2) What decision was being made, by whom, and under what constraints? (3) What actually happened — the known historical outcome, including human cost, that this entry benchmarks against. Write in plain language; this section is read by finance ministry analysts without specialist mediation.*

[Replace this paragraph with the 150–300-word historical context narrative. Be specific about actors, dates, and consequences. Avoid hedged generalities. The historical outcome documented here is the anchor against which the harness output will be assessed.]

---

## 3. Question Posed

*One sentence. Phrase it as an analytical question the harness run is designed to answer — the question a finance minister, not a modeller, would ask. The question must be answerable in principle from the harness output (trajectory direction, threshold crossings, branch ordering). Questions about point magnitudes are only valid for MAGNITUDE-tier or CALIBRATED_CI-tier entries.*

**Question:** [Single sentence, ending with a question mark.]

**Scenario type rationale:** [One sentence explaining why this is Type A or Type B. For Type B, name the counter-factual path explicitly: "The counter-factual is the path in which [specific alternative policy] was implemented at [branch point year]."]

---

## 4. Scenario Configuration

*Document the harness inputs exactly as run. The values here must be reproducible — a second analyst reading this entry should be able to reconstruct the identical run.*

| Parameter | Value |
|---|---|
| **Entity** | [ISO 3166-1 alpha-3] |
| **Start year** | [YYYY] |
| **End year** | [YYYY] |
| **Scenario branches** | [List all branches run, e.g. `baseline`, `orthodox-programme`, `heterodox-alternative`] |
| **Branch point step** | [Step N at year YYYY; omit if Type A single-branch run] |

**Control inputs by branch:**

| Input | Baseline | Branch A: [name] | Branch B: [name] |
|---|---|---|---|
| [Parameter name] | [value] | [value] | [value] |
| [Parameter name] | [value] | [value] | [value] |

*If the run has only one branch (Type A or single-path Type B), collapse to a single "Values" column.*

**Pre-branch-point data sources used:** [Name the data sources and their confidence tiers per `docs/DATA_STANDARDS.md`. For Type B runs, only data available before the branch point year may be used in configuration — document this explicitly.]

---

## 5. Harness Output Summary

*Document what the harness actually produced. Do not interpret here — interpretation belongs in sections 6 and 8. Record direction verdicts, threshold crossings, and branch ordering with step-level specificity where meaningful.*

**Per-indicator direction verdicts:**

| Indicator | Branch: [Baseline] | Branch: [Alt A] | Branch: [Alt B] |
|---|---|---|---|
| [Indicator name, e.g. GDP growth] | [UP / DOWN / FLAT / ↓ SUSTAINED] | [direction] | [direction] |
| [Human Development Index proxy] | [direction] | [direction] | [direction] |
| [Poverty headcount] | [direction] | [direction] | [direction] |
| [Current account balance] | [direction] | [direction] | [direction] |
| [Add rows for all primary indicators reported] | | | |

**Threshold crossings:**

| Threshold | Branch | Step crossed | Direction |
|---|---|---|---|
| [e.g. MDA: Poverty headcount > X%] | [branch name] | Step N (year YYYY) | BREACH \| SAFE |

*If no threshold crossings occurred, write "No MDA thresholds breached in any branch."*

**Branch ordering (where applicable):**

*State which branch performed better on which indicators, and the step range over which the ordering held. Example: "Branch A dominated Branch B on GDP trajectory from Step 3 onward; human development indicators showed no sustained directional difference between branches." If only one branch was run, omit.*

[Replace with branch ordering narrative, or write "Single-branch run — no branch ordering applicable."]

---

## 6. Fidelity Assessment

*Declare the fidelity ceiling for this entry and justify it by indicator. The ceiling is the lowest tier across all primary indicators. An entry that is CALIBRATED_CI on one indicator and DIRECTION_ONLY on another has an entry-level ceiling of DIRECTION_ONLY.*

**Entry-level fidelity ceiling:** `[DIRECTION_ONLY | MAGNITUDE | CALIBRATED_CI]`

**Per-indicator fidelity:**

| Indicator | Fidelity tier | Justification |
|---|---|---|
| [Indicator name] | `DIRECTION_ONLY` \| `MAGNITUDE` \| `CALIBRATED_CI` | [State what data or calibration is present/absent and why this tier results. Be specific: "T3 elasticity estimate from Batini et al. 2012; no country-specific fiscal multiplier data available for this entity"] |
| [Indicator name] | | |

**Calibration basis:** [Name the literature source(s) for the elasticity estimates used. Cross-reference the calibration family in `docs/evidence/analytical-framework.md §Calibration Family Taxonomy`. If the entity uses a literature source not in the registered families, flag it explicitly and note that it has not been validated against that family's standard.]

**What a reader can rely on:** [One sentence per tier that applies to this entry.]
- *For DIRECTION_ONLY:* [State which directional claims the harness output supports.]
- *For MAGNITUDE (if applicable):* [State which magnitude comparisons are valid within the error envelope.]
- *For CALIBRATED_CI (if applicable):* [State the CI bounds and their posterior basis.]

---

## 7. Known Limitations

*Bullet list. Honest and specific. Do not hedge with generic caveats — name the specific data gaps, calibration limitations, model blindspots, and boundary conditions that apply to this entry. This section exists because the AEA's epistemic obligation is to represent what the engine actually produces, not to defend it.*

- [ ] [Specific limitation — e.g. "No sub-national distributional data available for [entity]; poverty headcount direction verdict reflects aggregate only"]
- [ ] [Specific limitation — e.g. "Multiplier estimate sourced from [literature]; entity-specific calibration data was unavailable for the [start year]–[end year] period"]
- [ ] [Specific limitation — e.g. "Capital controls channel (ADR-020) not activated in this run; external balance trajectory does not reflect controls-period dynamics"]
- [ ] [Specific limitation — e.g. "Ecological cost ledger outputs are DIRECTION_ONLY in all scenarios; no country-specific carbon intensity data was available"]
- [ ] [Add all additional limitations — err on the side of completeness]

*If a limitation implies that a claim made in §8 must be qualified, note the specific claim it qualifies.*

---

## 8. Plain-Language Synthesis

*1–3 sentences. Write at the level of a finance ministry briefing note — no jargon, no hedged academic qualifications. The synthesis must be directly supported by the harness output documented in §5 and bounded by the fidelity tier declared in §6. A DIRECTION_ONLY entry may not state magnitude claims. The synthesis is what the analyst cites; it must be defensible without reference to this document.*

[Replace this paragraph with 1–3 sentences. Example of appropriate scope for a DIRECTION_ONLY entry: "Under either adjustment path, the harness finds consistent downward direction on human development indicators from the fiscal consolidation step onward. The alternative path delays the steepest decline by approximately two steps but does not avoid it. Both paths breach the poverty headcount MDA threshold — the orthodox path at Step 4, the heterodox path at Step 6." Example of what is not appropriate for a DIRECTION_ONLY entry: "The heterodox path reduces poverty by 12% relative to the orthodox path" — this is a magnitude claim requiring MAGNITUDE or CALIBRATED_CI tier.]

---

## 9. Comparability Note

*State explicitly which other portfolio entries can be directly compared to this one and which cannot. Direct comparison is valid when entries share the same calibration family and the same scenario type (Type A vs Type B). Cross-family comparisons are DIRECTION_ONLY on relative ordering only — magnitude comparisons across families are invalid. Cross-type comparisons (Type A vs Type B) require a separate methodological note.*

**Directly comparable entries (same calibration family, same scenario type):**
- [AEP-NNN or "None yet" — updated as portfolio grows]

**Comparable for relative ordering only (same family, cross-type; or cross-family directional):**
- [AEP-NNN or "None yet"]

**Not comparable (different calibration families or incompatible scenario types):**
- [AEP-NNN or "None yet"]

**Reference:** `docs/evidence/analytical-framework.md §Error Envelope Principle` governs what constitutes a valid comparison. When in doubt, default to DIRECTION_ONLY comparability and document the reasoning.

---

*Entry authored by: [Agent name]*  
*Entry reviewed by: [EL — date]*  
*Status: `DRAFT` \| `EL-REVIEWED` \| `PORTFOLIO-ACTIVE`*
