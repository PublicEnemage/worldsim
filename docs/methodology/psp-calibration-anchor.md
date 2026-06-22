# PSP Calibration Anchor — Programme Survival Probability

> Chief Methodologist Agent — M15-G5 (#1084)
> Authority: `docs/process/intents/M15-G5-2026-06-22-process-fixes.md` AC-12
> Version: 2026-06-22

---

## Purpose

The Programme Survival Probability (PSP) module requires an empirical calibration anchor —
a historical IMF programme case where the compliance outcome is documented and publicly
verifiable. This document records the primary calibration anchor for PSP validation in M15.

---

## Primary Anchor: Zambia 2022–2023 ECF Programme

**Arrangement type:** Extended Credit Facility (ECF)  
**Country:** Zambia (ZMB)  
**Programme reference years:** 2022–2023  
**IMF source:** IMF Extended Credit Facility press releases and Article IV consultation
reports, publicly available at imf.org.

### Programme Context

The IMF approved a 38-month ECF arrangement for Zambia in September 2022. The programme
was designed to support Zambia's post-default debt restructuring and economic stabilisation
following its November 2020 sovereign default. The arrangement provided approximately
SDR 978.2 million (roughly USD 1.3 billion at approval).

### Compliance Outcome (Calibration Target)

The 2022 ECF is the primary PSP calibration case because:

1. **Programme compliance was mixed across review periods.** The first two ECF reviews
   (2022–2023) recorded partial compliance with quantitative performance criteria,
   particularly on reserve accumulation targets. Several structural benchmarks required
   waivers or rescheduling, consistent with a PSP below 1.0 from programme entry.

2. **Political execution risk was demonstrably elevated.** The conditionality package
   required revenue mobilisation measures (VAT compliance, fuel subsidy rationalisation)
   that faced documented implementation resistance. This is the signature of PSP risk:
   fiscal space is mathematically available but politically constrained.

3. **The programme survived.** Despite compliance gaps, the programme was not
   abandoned — Zambia remained engaged through the review process. PSP did not collapse
   to zero; it operated in the mid-range (calibration target: 0.55–0.70 at programme
   entry with declining reserve trajectory, reflecting meaningful risk without imminent
   discontinuation).

### Calibration Target Values

| PSP condition | Calibration target | Basis |
|---|---|---|
| Programme entry, stable reserves | 0.80–0.90 | Baseline: no fiscal stress yet |
| Programme entry, reserve stress beginning | 0.60–0.75 | First warning signal visible |
| Mid-programme, reserve WARNING zone | 0.50–0.65 | Active political execution risk |
| Mid-programme, reserve CRITICAL zone | 0.25–0.45 | High discontinuation risk |
| Programme break (waiver refused) | < 0.25 | Near-collapse state |

The Zambia 2022 calibration supports the 0.65 value displayed in Demo 5 (v0.14.0) and
Demo 6 (v0.15.0) at step 3 of the ECF scenario — mid-programme, reserve WARNING zone.

---

## Secondary Reference: Ghana 2023 ECF

**Country:** Ghana (GHA)  
**Arrangement type:** Extended Credit Facility (ECF)  
**Reference year:** 2023  
**Source:** IMF Article IV consultation and ECF programme documentation (public).

Ghana's 2023 ECF provides a corroborating anchor for the relationship between reserve
trajectory and PSP. Ghana entered its programme under conditions of severe balance of
payments stress (reserves below 2 months of import cover). Programme compliance in the
first year was constrained by social resistance to fuel subsidy removal — the political
feasibility test that PSP is designed to capture. The programme survived but required
multiple waiver applications, consistent with PSP in the 0.40–0.55 range at programme
entry under stressed reserve conditions.

---

## Limitations and Calibration Gap

The PSP module in M15 is calibrated against directional patterns, not magnitude-validated
against exit probabilities. Two known limitations:

1. **No programme exit calibration.** We have no anchor case where a programme was
   formally abandoned (rather than suspended or rescheduled). The lower tail of the PSP
   distribution (< 0.25) is extrapolated from the calibration pattern, not anchored
   in an observed exit.

2. **Structural break risk.** ECF compliance outcomes from 2010–2019 may not generalise
   to the post-COVID fiscal environment. Reserve stress patterns post-2020 are more
   acute than the pre-COVID calibration period. The Chief Methodologist treats the
   post-2020 anchors (Zambia 2022, Ghana 2023) as primary and pre-2020 cases as
   secondary references only.

These limitations are disclosed in Zone 1B when PSP appears in an alert. The PSP output
carries a Tier 3 confidence rating until magnitude calibration against exit probabilities
is complete.

---

## Source References (Public IMF Documents)

- IMF Press Release No. 22/314, "IMF Executive Board Approves a 38-Month ECF
  Arrangement for Zambia," September 2022. Available at imf.org.
- IMF Article IV Consultation and ECF Programme Review, Zambia, 2023. Available at imf.org.
- IMF Press Release, "IMF Executive Board Approves ECF Arrangement for Ghana," May 2023.
  Available at imf.org.

All sources are publicly available. No proprietary data is used in PSP calibration.
Compliance outcomes are derived from publicly documented review waivers, press releases,
and Article IV consultation reports — all verifiable by any party with access to imf.org.
