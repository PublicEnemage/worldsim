# M14 Screenshot Brief — UX Designer Agent

> Generated: 2026-06-19. Produced by UX Designer Agent for #1055 / Demo 5 preparation.
> Five frames specified for the M14 stakeholder demo: Zambia 2024 IMF ECF review,
> single entity, trust architecture (ADR-016 Grounding strip + ADR-015 Evidence thread),
> reserve coverage challenge-response as thesis moment.
>
> **Architecture changes from M12 Demo 4:**
> - **ADR-016 Grounding strip:** Source institution, confidence tier, and vintage date for
>   every initial state input are visible in the scenario identity area at zero interaction.
>   The finance ministry analyst can cite the data source without asking a specialist.
> - **ADR-015 L0 basis annotations:** Tier badges and source labels appear inline on
>   Zone 1A trajectory curves at zero interaction — the provenance is on the instrument.
> - **ADR-015 L1 assumption surface:** All scenario inputs visible with tier annotations,
>   accessible from the instrument cluster. The basis statement shows what drove each output.
> - **ADR-015 Component 3 — `programme_survival_probability`:** Visible in Zone 1D as a
>   fifth framework readout alongside financial, HD, ecological, governance composites.
> - **Zone 1B negotiation tier labels:** "Model estimate" (T4), "Synthetic extrapolation" (T5)
>   replace raw tier numbers — self-interpreting for non-specialist audience.
> - **`reserve_coverage_months` in Zone 1B detail:** The indicator name is present in the
>   persistent-detail slot alongside threshold, current value, and confidence tier. Absent in M12.
> - **Single entity (ZMB only):** No two-entity comparison in Demo 5. Zone 1D composites
>   are single-entity (composite score meaningful, percentile rank not required).
> - **No Mode 3:** Control plane zone is visible but not activated. Frame D shifts to
>   political feasibility (PSP) rather than a branch trajectory.

## Thesis Frame

**Frame C — "The Citation at the Table" (Step 2, 2025)**

The single image that most completely communicates the Demo 5 argument: Zone 1B shows
`reserve_coverage_months` declining toward the CRITICAL floor with the full persistent-detail
slot visible — indicator name, current value, threshold, tier label ("T2 · IMF WEO Apr 2024"),
and the Layer 3 self-interpreting statement ("Reserve coverage has fallen below the WARNING
threshold. At the current draw rate, the CRITICAL floor is reached within 2 steps.").
The Grounding strip in the scenario header is also visible, showing the same T2 · IMF WEO
Apr 2024 citation for the initial reserve figure.

This is the challenge-response moment: the creditor says "where does your 3.8 months come
from?" The analyst reads the answer off the screen without opening a drawer or asking a
colleague. The source is the creditor's own institution's publication.

This frame communicates three things simultaneously:
1. The trust architecture is load-bearing — the citation is always present, not discoverable
2. The Layer 3 output tells you what the number means, not just what it is
3. The source is the IMF's own WEO — the creditor has challenged a figure from their own dataset

---

## Five Frames

### Frame A — "The Grounding Strip at Scenario Load" (Step 1, 2024)

**What Zone 1 shows:** ZMB scenario at step 1, all four composite scores live. The Grounding
strip in the scenario header area shows the data quality summary for ZMB: financial T2 (IMF WEO
Apr 2024), human development T2 (World Bank WDI 2023), ecological T4 (synthetic), governance T4
(synthetic). Zone 1B: likely no CRITICAL alert at step 1 (reserve_coverage_months 3.8 months
is above the 3.0-month CRITICAL floor). L0 basis annotation on the reserve trajectory curve
is visible — tier badge and source label.

**Zone 1 requirements:**
- 1A (Trajectory View): ZMB at step 1 anchor. Reserve_coverage_months as primary trajectory
  indicator. Y-axis labeled "Score". L0 basis annotation visible on the reserve curve — tier
  badge (T2) and source label (IMF WEO) readable. Step annotation at step 1 legible.
- 1B (MDA Alert Panel): Either empty ("No active threshold breaches") or a WATCH alert if
  the reserve is already flagged. Persistent-detail slot visible even in empty state.
- 1C (PMM Widget): PMM value computed for ZMB at step 1.
- 1D (Four-Framework): Four composites + PSP visible. Single-entity — no percentile rank
  comparison. The PSP row shows programme_survival_probability — new in M14.

**Grounding strip (key M14 capability):** Source citation visible in the scenario header/
parameters area. If the GroundingStrip component is in the ScenarioParameters panel, that
panel must be visible (or at minimum the Grounding strip chip). The presenter will explicitly
narrate what this shows.

**Zone 2:** Choropleth — ZMB visible and highlighted (single-entity scenario active).
Geographic context, not analytical instrument — per UX-RULING-4.

**Caption:** Zambia, 2024. The Grounding strip shows where every initial number comes from —
source, tier, date — before the analysis begins. Reserve coverage: 3.8 months (IMF WEO
Apr 2024, T2). The trust architecture is visible from moment one.

**UI state:** ZMB scenario active. Step 1 complete. Grounding strip visible.
No drawer open. All Zone 1 instruments rendered.

---

### Frame B — "Reserve Declining: Zone 1B Self-Interpreting" (Step 2, 2025)

**What Zone 1 shows:** Step 2. Reserve coverage has declined to approximately 3.2 months
(one step of drawdown). Zone 1B persistent-detail now shows the reserve coverage alert with
full Layer 3 output: indicator name ("Reserve Coverage (months)"), current value (3.2),
threshold (3.0 CRITICAL / 3.5 WARNING), tier label, and the self-interpreting sentence.
Zone 1A shows the reserve trajectory declining.

**Zone 1 requirements:**
- 1A (Trajectory View): Step 2 position on trajectory. Reserve curve visibly declining.
  L0 basis annotation still readable on the reserve curve.
- 1B (MDA Alert Panel): Persistent-detail slot active — showing either WATCH or WARNING
  alert for reserve_coverage_months. Full detail visible: indicator label (not raw field name),
  tier label ("T2 · IMF WEO Apr 2024" or equivalent human-readable form), current value vs
  threshold, self-interpreting Layer 3 text. This is the M13/M14 capability claim: the detail
  is always visible, not click-to-expand.
- 1C (PMM Widget): PMM tightening as reserve approaches floor.
- 1D (Four-Framework): PSP showing updated value at step 2.

**Caption:** Step 2 (2025): reserve coverage 3.2 months — approaching the 3.0-month CRITICAL
floor. Zone 1B tells you what the number means, not just what it is. The indicator label,
source tier, and direction of risk are on screen without any interaction.

**UI state:** Step 2 complete. Zone 1B detail slot populated. No drawer open.

---

### Frame C — "The Citation at the Table" ← THESIS FRAME (Step 2 or 3)

**What Zone 1 shows:** The challenge-response moment. Zone 1B persistent-detail showing
`reserve_coverage_months` alert with T2 tier label and source citation visible — the answer
to "where does this number come from?" is on screen. The Grounding strip in the scenario
parameters area is also visible, reinforcing the same citation. Zone 1A shows the reserve
trajectory. Zone 1D shows PSP.

**Zone 1 requirements:**
- 1B (MDA Alert Panel): The persistent-detail slot is the compositional focus. The tier
  label must be readable as human-readable text — not "T2" but ideally "T2 · IMF WEO Apr 2024"
  or equivalent. The indicator name "Reserve Coverage (months)" must be readable (not the raw
  DB field name `reserve_coverage_months`). The self-interpreting Layer 3 sentence must be
  visible. Severity badge legible at 1440×900.
- Grounding strip: The GroundingStrip component or scenario identity header must be
  simultaneously visible in the same screenshot — establishing that the source citation
  in Zone 1B and the Grounding strip are saying the same thing.
- 1A: Reserve trajectory visible — the context for the alert.
- 1D: PSP visible — showing political feasibility in the same moment.

**This frame must be self-explaining without presenter narration:** A viewer with domain
experience who has never seen WorldSim should be able to read this screenshot and understand
(a) what the indicator is, (b) where the number comes from, and (c) what the risk level means.

**Caption:** Step 2 (2025 — challenge-response moment): Zone 1B shows reserve coverage at
3.2 months with source citation (IMF WEO Apr 2024, T2). The creditor has just challenged
this figure. The answer is on screen. No drawer. No specialist. Under 10 seconds.

**UI state:** Step 2 (or step 3 if reserve alert is stronger there). Zone 1B detail slot
prominent. Grounding strip visible. Capture after all Zone 1 instruments rendered (400ms).

---

### Frame D — "Political Feasibility in the Same View" (Step 3, 2026)

**What Zone 1 shows:** Step 3. Zone 1D showing all four composites plus PSP
(`programme_survival_probability`). The financial composite reflects the reserve drawdown.
The PSP shows the probability that the IMF ECF program survives the current fiscal trajectory.
This is the M14 political economy capability — programme feasibility is now quantified,
not just asserted.

**Zone 1 requirements:**
- 1D (Four-Framework): PSP row prominently visible alongside financial, HD, ecological,
  governance rows. The PSP value should be meaningful at step 3 (a probability between
  0.4–0.8 reflecting programme pressure, not trivially high or trivially low).
  If Zone 1D renders PSP as a distinct row or section, that distinction must be legible.
- 1B (MDA Alert Panel): Reserve alert likely CRITICAL at step 3 (below 3.0 months).
  Full detail visible. The simultaneity of reserve CRITICAL + PSP at the same step is
  the argument: financial stress and programme viability are linked but distinct signals.
- 1A: Full trajectory arc visible — steps 1–3 showing the reserve decline.
- 1C: PMM very tight at step 3.

**Caption:** Step 3 (2026): reserve coverage CRITICAL (2.7 months). Programme survival
probability: [value]. The political economy module quantifies what the ministry team has
always known — reserve stress and programme viability are not the same constraint. Both
are now on the same instrument.

**UI state:** Step 3 complete. Zone 1D primary compositional focus. No drawer open.

---

### Frame E — "The Evidence Thread: All Sources Named" (Step 5, 2028)

**What Zone 1 shows:** The full evidence thread at step 5 — Zone 1A showing the complete
reserve trajectory arc (5 steps of decline), Zone 1B showing the CRITICAL alert with
Layer 3 self-interpreting text, Zone 1D showing all composites + PSP at the reserve
depletion point. The assumption surface (L1) is either visible inline or the Grounding
strip is prominently displayed — showing that every input that produced this output is
named, sourced, and tiered. This is the closing capability claim: the ministry team can
defend every number.

**Zone 1 requirements:**
- 1A: Full 5-step arc visible — the trajectory from 3.8 months (step 0) through
  depletion. The Y-axis "Score" label visible. L0 basis annotation still readable.
- 1B: CRITICAL alert detail visible at step 5. If reserve coverage has reached
  near-zero or zero, the Zone 1B detail shows the terminal state self-interpretingly.
- 1D: All composites + PSP at step 5. The PSP at this step reflects the programme
  survival probability under sustained reserve pressure — a quantified institutional
  assessment, not a model assumption.
- Assumption surface or Grounding strip visible: either the L1 basis statement
  surface is open showing inputs with tier annotations, or the Grounding strip
  is visible reinforcing the source chain.

**Caption:** Step 5 (2028): the complete trajectory. From 3.8 months reserve coverage at
scenario entry to [value] months at step 5. Every number on this screen has a named source,
a confidence tier, and a self-interpreting label. The ministry team can defend every finding
at the table — without specialist mediation.

**UI state:** Step 5 complete. All Zone 1 instruments rendered. Full arc visible.
Capture after 400ms render settle.

---

## Presentation Sequence

| Order | Frame | Step | Why |
|---|---|---|---|
| 1 | C — The Citation at the Table | 2 | Lead with the thesis — the creditor challenge answered |
| 2 | A — The Grounding Strip at Load | 1 | Pull back to scenario entry — the trust architecture from moment one |
| 3 | B — Zone 1B Self-Interpreting | 2 | Show the alert Layer 3 — what the number means, not just what it is |
| 4 | D — Political Feasibility | 3 | PSP alongside financial trajectory — the M14 political economy capability |
| 5 | E — The Evidence Thread | 5 | Close on the full arc — every number sourced, every output traceable |

Rationale: Lead with the thesis frame (C). The audience immediately understands the Demo 5
argument — the challenge-response moment — before they see the setup. Frame A establishes
the trust architecture was present from the start. Frame B shows Layer 3 in detail. Frame D
introduces the political economy capability. Frame E closes on the capability claim: the
evidence thread is complete.

---

## Pre-Capture Requirements

| Requirement | Source | Must verify |
|---|---|---|
| ZMB in `simulation_entities` and `source_registry` | G3 backend (PR #1011) | `GET /api/v1/entities/ZMB/data-quality?year=2024` returns 200 |
| Grounding strip renders for ZMB scenario | G4 frontend (PR #1015) | Component visible with source/tier/vintage |
| L0 basis annotation visible on reserve trajectory | G5 frontend (PR #1030) | Tier badge on zone-1a trajectory curve |
| Zone 1B persistent-detail shows reserve_coverage_months | G6 frontend (PR #1045) | Indicator name readable (not raw DB field name) |
| PSP visible in Zone 1D | G5 frontend (PR #1030) | programme_survival_probability row present |
| Tier labels human-readable in Zone 1B | G6 frontend (PR #1045) | "Model estimate" / "Synthetic extrapolation" visible |
| Legibility spec passes at 1440×900 | Step 5b gate | `demo-legibility.spec.ts` all pass |

---

## Key Narration Notes

1. **Do not narrate the choropleth as the analytical instrument.** Per UX-RULING-4, say
   "Zone 1A shows..." and "the trajectory view shows..." — not "watch Zambia shift on the map."
   The choropleth anchors geography. The instruments carry the argument.

2. **The source citation is from the creditor's own institution.** The IMF WEO is an IMF
   publication. When the creditor challenges the reserve figure, the Grounding strip is
   citing the IMF's own Article IV / WEO assessment. Name this explicitly in narration.

3. **Synthetic data is honest, not a weakness.** ZMB ecological (T4) and governance (T4)
   data are synthetic from SADC comparable economies. The tool labels this visibly —
   "Synthetic extrapolation" in Zone 1B. This is the No False Precision principle in action:
   the tool tells you what it knows and what it inferred. Narrate it as a capability,
   not an apology.

4. **PSP is a quantified political constraint, not an IMF view.** The programme survival
   probability reflects the model's assessment of programme implementation capacity under
   the current fiscal trajectory. It is not a political prediction. Frame it: "The model
   is asking whether the programme's conditionality terms are achievable given the fiscal
   pressure the country is under. That is a different question from whether the IMF approved
   the programme."

5. **No Mode 3 in Demo 5.** The demonstration does not include a counter-proposal branch.
   If asked, the honest answer: "The counter-proposal capability — testing what the trajectory
   looks like under alternative conditionality terms — is available in the tool. Today we are
   showing the trust architecture: the ability to source and defend every number. The next
   demo cycle will combine both."
