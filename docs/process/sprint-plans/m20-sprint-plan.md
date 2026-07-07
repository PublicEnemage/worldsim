# M20 Sprint Plan — Analytical Evidence Portfolio and Demo 9

> **Filed:** 2026-07-07  
> **EL approval:** Confirmed in session — scope decomposition approved 2026-07-07  
> **Milestone:** M20 (GitHub milestone #22)  
> **Release branch:** `release/m20` (cut 2026-07-07 from main `5fadd00`)  
> **Exit gate:** #1773 (M20 Exit Checklist)

---

## Milestone Objective

Build the WorldSim Analytical Evidence Portfolio (AEP) — 11 structured entries across all four registered calibration families — and deliver Mode 3 instrument polish. The AEP grounds the engine's outputs in a citable, quality-tiered evidence record that finance ministry analysts can use. Demo 9 demonstrates the portfolio to a live stakeholder audience.

**North star test (M20):** A Zambian finance ministry analyst reviewing AEP-004 (ZMB 2005–2015) can see what the engine found in the copper crisis, compare it directionally to Senegal (AEP-005), cite the comparison with appropriate confidence qualification, and understand why the magnitude comparison is not valid — all without specialist mediation.

---

## What is deferred

| Item | Original M20 scope | Reason for deferral | Target |
|---|---|---|---|
| Live interactive constraint-floor search | M20 primary | Requires full sprint; AEP needs the milestone bandwidth | M21 |
| DEMO-235 PSP multi-scenario view (#1777) | M20 instrument polish | More substantial than DEMO-217/233/234; would compress AEP work | M21 |

---

## Sprint Groups

### M20-G1 — AEP EURO-AREA Entries (AEA)

**Sprint objective:** File the first three AEP entries using EURO-AREA family fixtures — the most mature calibration (CM-A, ADR-007 posterior, CALIBRATED_CI tier available for GRC). These are the highest-fidelity entries in the portfolio and set the quality standard for subsequent groups.

**Deliverables:**

| Entry ID | Entity | Period | Type | Fixture | Fidelity ceiling |
|---|---|---|---|---|---|
| AEP-001 | GRC | 2010–2015 | A — Troika adjustment replay | `greece_2010_scenario.py` | CALIBRATED_CI (fiscal multiplier, ADR-007); MAGNITUDE (human dev., labour) |
| AEP-002 | GRC | 2010–2015 | B — heterodox alternative counter-factual | `greece_2010_scenario.py` counter-factual branch | CALIBRATED_CI / MAGNITUDE; temporal blindfold mandatory |
| AEP-003 | ISL | 2008–2011 | B — heterodox vs orthodox | `isl_2008_heterodox.py` + `isl_2008_orthodox_counterfactual.py` | MAGNITUDE (ADR-020 capital controls channel) |

**Entry conditions:**
- AEA has access to harness output from existing fixtures (greece_2010_2012_actuals.py, fidelity_report.py, reports/greece_2010_2015-2026-07-05-65ff77d7.json)
- For AEP-002 (Type B): temporal blindfold protocol — configuration committed before run; output read before consulting historical actuals
- All entries follow TEMPLATE.md; fidelity claims bounded by analytical-framework.md

**North star test (G1):** An external economist reviewing AEP-001 can verify that the engine's direction verdicts for the 2010–2015 GRC Troika period are consistent with the documented historical outcome, and can assess the CALIBRATED_CI claim against the ADR-007 methodology.

**File locations:** `docs/evidence/AEP-001-GRC-2010.md`, `docs/evidence/AEP-002-GRC-2010-B.md`, `docs/evidence/AEP-003-ISL-2008.md`

---

### M20-G2 — AEP SSA-LIC and LATAM-EM Entries (AEA)

**Sprint objective:** File six AEP entries across the SSA-LIC and LATAM-EM calibration families, enabling the first within-family cross-entity comparisons.

**Deliverables:**

| Entry ID | Entity | Period | Type | Fixture | Fidelity ceiling |
|---|---|---|---|---|---|
| AEP-004 | ZMB | 2005–2015 | A — copper cycle replay | `zmb_scenario.py` | DIRECTION_ONLY (fiscal); MAGNITUDE conditional (human dev., copper channel) |
| AEP-005 | SEN | 2000–2015 | A — structural adjustment and growth | `sen_scenario.py` | DIRECTION_ONLY (fiscal); MAGNITUDE conditional (human dev.) |
| AEP-006 | GHA | 2022–2023 | A — IMF programme entry | `ghana_2022_scenario.py` | DIRECTION_ONLY |
| AEP-007 | ARG | 2001–2002 | A + B — default/exit + Zero Deficit counter-factual | `argentina_2001_2002_scenario.py` | DIRECTION_ONLY; temporal blindfold for B |
| AEP-008 | ARG | 2003–2007 | A — Kirchner recovery | CM-D inputs (config from ELASTICITY_REGISTRY CM-D) | DIRECTION_ONLY |
| AEP-009 | ECU | 1999–2000 | A — dollarisation crisis | `ecuador_1999_2000_scenario.py` | DIRECTION_ONLY |

**Key comparisons enabled by G2:**
- ZMB vs SEN (within SSA-LIC family): first within-family cross-entity directional ordering
- ARG 2001 vs ARG 2003 (LATAM-EM): crisis entry vs recovery — direction reversal documented

**North star test (G2):** A Zambian finance ministry analyst can open AEP-004 and AEP-005 together and see that the ZMB copper cycle and the SEN structural adjustment show comparable directional patterns on human development — and that the comparison is valid (shared SSA-LIC error envelope) while the magnitude comparison is not.

**File locations:** `docs/evidence/AEP-004-ZMB-2005.md` through `docs/evidence/AEP-009-ECU-1999.md`

---

### M20-G3 — AEP SOUTH-SE-ASIAN Entries + Gap Closure Issues (AEA + PM)

**Sprint objective:** Complete family coverage with two SOUTH-SE-ASIAN entries (LKA and PAK 2022), then file three gap closure issues that define the M21 implementation backlog for the AEP.

**Deliverables:**

| Entry ID | Entity | Period | Type | Fixture | Fidelity ceiling |
|---|---|---|---|---|---|
| AEP-010 | LKA | 2022–2023 | A — Coffin Corner entry | `sri_lanka_2022_scenario.py` | DIRECTION_ONLY (all dimensions); multi-dimension simultaneous breach |
| AEP-011 | PAK | 2022–2023 | A + B — SBA compliance + deviation counter-factual | `pakistan_2022_scenario.py` | DIRECTION_ONLY; temporal blindfold for B |

**Gap closure issues (filed at G3 close, implementation M21+):**

| Issue | Title | Priority | Coverage audit reference |
|---|---|---|---|
| TBD | feat: Portugal 2010 backtesting fixture | High — enables first EURO-AREA cross-entity MAGNITUDE comparison | Coverage audit §Family 2 (d) |
| TBD | feat: Bangladesh 2022 backtesting fixture | High — completes SOUTH-SE-ASIAN CM-C family | Coverage audit §Family 4 (d) |
| TBD | feat: remittance channel in ELASTICITY_REGISTRY (PAK/LKA/BGD) | High — structural gap affecting human development fidelity | Coverage audit §Family 4 (d) |

**Key comparison enabled by G3:**
- LKA vs PAK (within SOUTH-SE-ASIAN family): LKA Coffin Corner entry vs PAK SBA compliance — directional ordering is the primary claim; LKA shows earlier multi-threshold breach

**North star test (G3):** A Sri Lankan finance ministry analyst can open AEP-010 and see the Coffin Corner documented as a simultaneous multi-dimension downward trajectory — fiscal, external, human development, governance — with explicit comparison to Pakistan's SBA compliance path showing a different timing and severity ordering.

**File locations:** `docs/evidence/AEP-010-LKA-2022.md`, `docs/evidence/AEP-011-PAK-2022.md`

---

### M20-G4 — DEMO Maintenance and Test Fix (Engineering)

**Sprint objective:** Close the Demo 8 instrument polish backlog (three frontend/backend fixes) and resolve the carry-forward test fix.

**Deliverables:**

| Issue | Title | Type | Size |
|---|---|---|---|
| DEMO-217 | In-viewport Act 1 → Act 2 navigation link | Frontend | Small |
| #1775 / DEMO-233 | WARNING badge alongside CLEAR in Zone 1B | Frontend | Small |
| #1776 / DEMO-234 | Binary-search precision label vs CI label (±0.01 vs 0.08 CI width) | Frontend/backend | Small |
| #1759 / NM-099 | asgi_client pool ordering fix in test_m19_cm_b | Test fix | Small |

**Note:** DEMO-235 (PSP multi-scenario comparison) is deferred to M21. It was assessed as more substantial than the other three DEMO fixes and would compress AEP work if included in M20.

**North star test (G4):** The Zone 1B instrument displays WARNING alongside CLEAR when the constraint floor is met but margin is narrow; the Act 1→Act 2 navigation link is visible in-viewport; the precision label distinguishes ±0.01 binary-search tolerance from the 0.08 CI width.

---

## Demo 9

**Format:** Live stakeholder session at M20 close (same format as Demo 8).

**Story:** *"The Zambian finance ministry analyst pulls up AEP-004. The engine found consistent downward direction on human development from the copper crash step onward — the same pattern as Senegal's structural adjustment period (AEP-005). The directional ordering is valid within the shared SSA-LIC error envelope. Magnitude comparison is not valid — the framework says why. She then runs a new scenario for her own country and sees where it sits relative to the documented cases."*

**Acceptance criterion:** The analyst can navigate from the AEP to a live scenario run and back, with the fidelity tier and comparability status visible throughout. Demo 9 is the M20 exit gate.

---

## HORIZON Sweep — Insights Log

Open entries in `docs/insights-log.md` to be reviewed at each sprint group close. Current status: not yet reviewed for M20 (review at G1 entry).

---

## Parallel stream note

G1–G3 (AEA work — docs only) and G4 (engineering — backend/frontend) are independent and may proceed in parallel. AEA work does not require a DATABASE_URL for entry authorship (entries are written from existing harness output reports and fixture file review); Type B entries require a harness run with DATABASE_URL for the temporal blindfold protocol.

---

## ADR-008 renewal (carry-forward)

SCAN-029 flagged ADR-008 renewal as a carry-forward. Must complete before M20 close. Assign to Architect Agent at M20 sprint planning; not blocked on any G1–G4 work.
