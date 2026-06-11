# M12 Screenshot Brief — UX Designer Agent

> Generated: 2026-06-06. Produced by UX Designer Agent for Issue #793 / Demo 4 preparation.
> Five frames specified for the M12 stakeholder demo: Jordan/Egypt Strait of Hormuz, all
> four composite scores live, ExternalSectorModule (ADR-012), Mode 3 Active Control debut.
>
> **Architecture changes from M10 Demo 3:**
> - All four composite scores are now live simultaneously (JOR + EGY ≥2 entities — Issue #193 guard lifted).
>   Financial and human_development composites are no longer null.
> - ExternalSectorModule (ADR-012) introduces commodity price shocks as a new M12 input class.
>   The shock distribution by import dependency is a new Zone 1A signal: two entities, same
>   shock, different exposure profiles, divergent trajectories.
> - Mode 3 (Active Control) is live for the first time. The control plane zone is now
>   populated — not reserved-but-empty as in M10. Frame D is the first demo frame to show
>   a live branch trajectory in Mode 3.

## Thesis Frame

**Frame C — "The Divergence" (Step 3, 2026 — Dual Shock Peak)**

The single image that most completely communicates the Demo 4 argument if only one
screenshot is shared. Zone 1A shows two entity trajectory bundles diverging: Jordan's
reserve trajectory approaching the CRITICAL floor while Egypt's governance trajectory
breaches the MDA-GOV-DEMOCRACY-FLOOR. Same external shock (Hormuz disruption). Same
engine. Same instruments. Different exposure profiles routing the shock to different
populations through different channels.

This is the WorldSim thesis across two dimensions simultaneously:
1. Financial pressure ≠ human cost (GDP trajectory vs reserve trajectory vs bottom-quintile)
2. The same shock can require different policy responses in different countries

For Demo 4, this frame also demonstrates the M12 capability milestone:
1. ExternalSectorModule live — shock distribution by import dependency is a real analytical signal.
2. All four composite scores live — financial and human_development are no longer null.
3. Two-entity comparison is live — the percentile rank composite is the design target for this.

---

## Five Frames

### Frame A — "The Instrument" (Step 1, 2024)

**What Zone 1 shows:** Both JOR and EGY loaded at scenario entry with fuel shock active
(step 1). Zone 1A trajectory view shows both entity trajectories at step 1 anchor.
Step label "Hormuz disruption / fuel shock" visible on the step axis. Zone 1D shows all
four composite scores with non-null values — this is the first Demo where all four are live.
Zone 1B: possible early reserve alert for JOR (7.1 months at entry — above SIGNIFICANT
threshold of 4.0, so no alert at step 1; the instrument is clean at baseline).

**Zone 1 requirements:**
- 1A (Trajectory View): JOR and EGY visible at step 1 anchor. Step annotation
  "Hormuz disruption / fuel shock" legible. Two entity sets of curves (4 curves each,
  or combined display per trajectory design). ExternalSectorModule effect visible
  in the trajectory — fuel shock starts pulling the financial curve at step 1.
- 1B (MDA Alert Panel): Likely no alerts at step 1 — baseline state above all floors.
  If any alert fires (Egypt governance at 0.07 is already far below 0.70 floor),
  it should be the first visible item and accurately labeled.
- 1C (PMM Widget): Computed value visible for the primary entity (JOR).
- 1D (Four-Framework): All four framework rows showing non-null composite scores.
  This is the M12 claim — four live axes. Financial and HD show percentile rank values
  (not dash or "—"). Caption: "Financial: live. Human Development: live. Ecological: live.
  Governance: live." The dual-null Demo 3 state should never recur in this demo.

**Zone 2:** Default framework tab. Choropleth shows JOR and EGY colored — geographic
context for the MENA scenario, not the analytical instrument.
**Zone 3:** Collapsed. Control plane zone visible but Mode 3 not yet active.

**Caption:** Jordan and Egypt at scenario entry (2024): fuel price shock begins. All four
framework composite scores live for the first time in WorldSim demo history. Reserve
coverage (JOR: 7.1 months, EGY: 5.3 months) above threshold — but the shock has started.

**UI state:** JOR/EGY scenario active. Step 1 complete. Mode 3 inactive. No EntityDetailDrawer
open. Zone 1D fully rendered with all four non-null composite scores.

---

### Frame B — "The Escalation" (Step 2, 2025)

**What Zone 1 shows:** Food shock joins the fuel shock. Zone 1A shows the step 2 inflection
as the second commodity shock hits both economies. Egypt's human_development trajectory
should show a sharper bend (food dependency 0.35 > Jordan's 0.28). Jordan's financial
trajectory shows the reserve burn beginning as fuel costs rise. Step annotation
"Food supply chain disruption" prominent on the step axis.

**Zone 1 requirements:**
- 1A (Trajectory View): Step 2 inflection clearly visible — the second shock's entry
  creates a sharper downward bend than step 1. Two entity trajectories diverging:
  Egypt's human_development curve declining more steeply (food exposure); Jordan's
  financial curve declining more steeply (fuel/reserve exposure).
- 1B (MDA Alert Panel): Egypt governance alert may fire here (0.07 < 0.70 MDA floor).
  If so: severity badge (CRITICAL), indicator ("democratic_quality_score"), entity (EGY).
  Note to presenter: Egypt's governance alert fires immediately from the initial seed
  (0.07 far below 0.70) — this demonstrates that the tool reads the pre-existing
  governance deficit, not just the shock-induced change.
- 1C (PMM Widget): JOR PMM — tightening margin as dual shock accumulates.
- 1D (Four-Framework): Financial composite showing the percentile rank divergence
  between JOR and EGY beginning. Both still live (non-null). Ecological ticking up.

**Zone 2:** Choropleth — MENA geographic context.
**Zone 3:** Collapsed.

**Caption:** Step 2 (2025): food price shock joins fuel shock. Egypt's human development
trajectory bends more steeply (food import dependency 0.35). Jordan's reserve trajectory
begins the drawdown arc (fuel import dependency 0.42). The same external shock hits
different populations.

**UI state:** Step 2 complete. Mode 3 inactive. No drawer open.

---

### Frame C — "The Divergence" ← THESIS FRAME (Step 3, 2026)

**What Zone 1 shows:** Dual shock peak. Jordan's IMF program has just been triggered.
Egypt's emergency declaration has been issued. Zone 1A shows two entity trajectory bundles
in divergent posture: Jordan's reserve-linked financial curve approaching the CRITICAL MDA
floor (2.5 months); Egypt's governance and human_development curves breaching their
respective floors under food price pressure + emergency conditions. Zone 1B shows alerts
for both entities simultaneously. Zone 1D shows all four composite scores with the
divergence readable — JOR and EGY financial composites moving in opposite directions
despite facing the same global shock.

**Zone 1 requirements:**
- 1A (Trajectory View): Step 3 labeled "Dual shock peak / IMF + GCC." Two entity
  trajectory bundles visibly diverging. Jordan financial/reserve curve approaching the
  CRITICAL floor visible in the display. Egypt human_development curve at its steepest
  descent. The divergence between the two entity postures is the dominant compositional
  element — the reader must be able to identify two different crisis profiles in the
  same instrument cluster without any explanatory caption.
- 1B (MDA Alert Panel): Alerts for both JOR and EGY visible. Minimum: JOR reserve
  SIGNIFICANT or CRITICAL (depending on drawdown speed); EGY governance CRITICAL
  (0.07 << 0.70 floor; consecutive breach count should be 3 by step 3).
  Entity labels on each alert card must be readable (JOR / EGY disambiguation required
  if the UI shows both entities' alerts in the same panel).
- 1C (PMM Widget): JOR PMM — compressed margin under dual shock + austerity-incoming.
- 1D (Four-Framework): All four composite scores. JOR vs EGY financial composite
  divergence visible. Governance composite: EGY score far lower than JOR (0.07 baseline
  vs 0.21 — the gap is wide and analytically meaningful).

**Zone 2:** Choropleth with both JOR and EGY visible. Geographic context for the
MENA crisis arc.
**Zone 3:** Collapsed. Mode 3 control plane zone visible (reserved but inactive).

**Caption:** Step 3 (2026 — dual shock peak): Jordan and Egypt hit the same external
shock through different exposure channels. Jordan: reserve drawdown approaching CRITICAL
floor (fuel dependency 0.42). Egypt: governance and human development deterioration
under food pressure (food dependency 0.35). The tool surfaces both — simultaneously.

**UI state:** Step 3 complete. Mode 3 inactive (next frame activates it). Both JOR and
EGY trajectories visible. All Zone 1 instruments rendered. Capture after 400ms.

---

### Frame D — "Mode 3 Active Control" (Step 3 — branch creation)

**What Zone 1 shows:** Mode 3 active for the first time in Demo history. The control
plane zone is populated — fiscal multiplier slider moved to 1.3 (stimulative,
representing emergency GCC fiscal support arriving in parallel with the IMF program).
Zone 1A shows the live branch trajectory — the original Jordan trajectory and the
Mode 3 branch trajectory diverging from step 3. The "Branched" annotation visible at
the branch anchor. The recompute badge has cleared (computation complete).

This frame answers the question a finance minister in Amman would actually ask:
"What happens to our reserve trajectory if we secure Gulf Cooperation Council emergency
support and increase effective fiscal stimulus by 30%? Does that buy us enough runway
to avoid the reserve CRITICAL floor?"

**Zone 1 requirements:**
- 1A (Trajectory View): Branch anchor annotation ("Branched") visible at step 3.
  Two trajectories for Jordan: baseline (original) and Mode 3 branch (GCC aid scenario).
  The branch trajectory should show the reserve-linked financial curve diverging
  upward from the baseline — the intervention is visible as a trajectory split.
  Step annotation "Dual shock peak / IMF + GCC" remains legible.
- Control Plane Zone: Fiscal multiplier slider at 1.3. "Apply Change" button visible.
  The Mode 3 toggle in its active state. Recompute badge cleared (not "Recomputing...").
- 1B (MDA Alert Panel): If the branch trajectory clears the reserve CRITICAL threshold,
  the JOR reserve alert should disappear or show reduced severity in the branch view.
  If it doesn't clear (depends on simulation output), the alert persists — either is
  analytically honest and should be presented as such.
- 1D (Four-Framework): Branch composite scores (if displayed separately from baseline)
  should show the fiscal stimulus effect in the financial framework.

**Zone 2:** Choropleth — geographic context.
**Zone 3:** Collapsed.

**Caption:** Mode 3 Active Control: fiscal multiplier adjusted to 1.3 (GCC emergency
support scenario). The branch trajectory shows Jordan's reserve arc under the counterfactual.
Does Gulf support buy enough runway? The instrument answers the question the finance
minister is actually asking.

**UI state:** Mode 3 active. Control plane visible. Step 3 branch complete (recompute
badge cleared). JOR scenario primary. Branch trajectory and baseline trajectory both
visible in Zone 1A.

---

### Frame E — "All Four Axes — The Capability Claim" (Step 5, 2028)

**What Zone 1 shows:** All four composite scores live at the peak reserve stress step.
Zone 1D is the compositional focus: four framework rows, four non-null values. This is
the M12 capability milestone — the engine simultaneously measures financial (reserve
drawdown), human development (bottom-quintile consumption capacity eroded by HCL
transmission), ecological (CO2 accumulation independent of the shock), and governance
(Egypt's ongoing deterioration). No axis is dashed. No honest null.

This frame closes on the Platform Principle: the same engine and instruments that ran
Greece (2010 austerity) and Argentina (2001 default) now run Jordan and Egypt under a
commodity price shock scenario. The engine is situation-agnostic. Only data inputs changed.

**Zone 1 requirements:**
- 1D (Four-Framework): All four framework rows fully rendered with non-null composite
  scores at step 5. Financial: JOR vs EGY percentile rank divergence maximally visible
  (reserve pressure has widened the gap). Human Development: bottom-quintile consumption
  capacity reduction visible across 5 steps of HCL transmission. Ecological: CO2 ticking
  upward (scenario-independent CO2 accumulation). Governance: EGY score unchanged (already
  at floor from initial seed); JOR governance stable (0.21 — Jordan's monarchy provides
  institutional stability even under economic stress).
- 1A (Trajectory View): 5-step arc visible — the full crisis trajectory through peak
  reserve pressure. Both entity trajectory bundles visible from steps 1–5.
- 1B (MDA Alert Panel): Peak alert density — reserve CRITICAL for JOR; governance
  CRITICAL (persistent, consecutive: 5 steps) for EGY. Both alerts visible without scroll.
- 1C (PMM Widget): Minimal margin at step 5 — the policy space is most compressed here.

**Zone 2:** Choropleth — both JOR and EGY visible in MENA context.
**Zone 3:** Collapsed. Control plane zone visible (Mode 3 may or may not be active).

**Caption:** Step 5 (2028 — reserve drawdown critical): all four framework composite scores
live. The engine simultaneously measures what the finance minister can control (reserve
coverage, fiscal policy) and what the shock will do to people who will never know this
tool exists (bottom-quintile consumption capacity). Platform Principle — same engine as
Greece and Argentina. Different crisis. Same analytical discipline.

**UI state:** Step 5 complete. All Zone 1 instruments rendered. Zone 1D primary compositional
focus. Capture with all four framework rows visible without scroll.

---

## Presentation Sequence

| Order | Frame | Step | Why |
|---|---|---|---|
| 1 | C — The Divergence | 3 | Lead with the argument — two countries, same shock, different crises |
| 2 | A — The Instrument | 1 | Pull back to scenario entry — the before-picture |
| 3 | B — The Escalation | 2 | Show the second shock joining — the compound pressure builds |
| 4 | D — Mode 3 Active Control | 3 | Show the steering capability — the counterfactual |
| 5 | E — All Four Axes | 5 | Close on capability — same engine, four live axes, full arc visible |

Rationale: Lead with the thesis frame. The audience understands why the tool matters before
they understand how it works. Frame D introduces Mode 3 — the key M12 delivery — in context
of a real decision scenario (does GCC support clear the reserve CRITICAL floor?). Frame E
closes on the platform principle claim: same engine, different crisis, four live axes.

---

## Pre-Capture Requirements

The following must be verified before screenshots are captured:

| Requirement | Issue/ADR | Component | Status |
|---|---|---|---|
| JOR and EGY in simulation_entities | natural_earth_loader | DB seed | Must verify before run |
| ExternalSectorModule producing events at step 1 | ADR-012 | ExternalSectorModule | Must verify via measurement-output |
| All four composite scores non-null at step 1 | Issue #193 | MeasurementFramework | Must verify — 2 entities required |
| Mode 3 toggle and ControlPlane visible | G6b / Issue #753 | ControlPlane.tsx | Must verify (G6b shipped) |
| Branch trajectory annotation visible | G6b | InstrumentCluster.tsx | Must verify |
| Zone 1D renders four non-null scores | M12 | FourFrameworkZone1D | Must verify |

---

## Key Narration Notes for Demo Presenter

1. **Do not narrate the choropleth as the thesis visualization.** Per UX-RULING-4, the
   choropleth is geographic context (Zone 2A). Say "the trajectory view shows..." not
   "watch Jordan shift in the choropleth."

2. **Egypt's governance alert fires from step 1.** This is correct — Egypt's democratic
   quality seed (0.07) is already far below the MDA-GOV-DEMOCRACY-FLOOR (0.70). The
   narration should acknowledge this: "The tool reads the pre-existing governance deficit,
   not just the shock-induced change. Egypt enters the scenario already in a governance
   breach state. The emergency declaration at step 3 deepens it — it does not cause it."

3. **The Mode 3 answer may not be 'yes'.** If the fiscal multiplier branch (1.3) does not
   fully clear Jordan's reserve CRITICAL threshold, that is the correct answer. Do not
   imply the tool gives a "success" answer — it gives an honest answer. The narration:
   "The Mode 3 branch shows whether GCC support is sufficient to clear the reserve floor.
   The tool does not recommend — it shows the consequence. The decision is the minister's."

4. **Financial and human_development composites are now live.** Unlike Demo 3 (Argentina,
   single entity), this is the first Demo where financial and HD composite scores are
   non-null. Acknowledge this explicitly: "For the first time in Demo history, all four
   composite axes are simultaneously live. Two entities — Jordan and Egypt — activate the
   percentile rank comparison that was deferred in prior demos."

5. **ExternalSectorModule is new infrastructure.** The commodity price shock distribution
   by import dependency coefficient is ADR-012 — a new analytical capability in M12. Name
   it explicitly: "The engine is now able to model a global commodity price shock and
   distribute its effects to each country proportional to their actual import exposure.
   Jordan absorbs more of the fuel shock. Egypt absorbs more of the food shock. The
   distribution is in the data — not a model assumption."

---

## Internal Demo Protocol

Per EL decision (2026-06-06), the internal demo runs from the `release/m12` branch.
All agents participate as reviewers. Issues identified during internal demo are filed
as GitHub issues targeting `release/m12` before the branch closes.

The Independent Review and stakeholder demo follow after M12 closes (EL merges
`release/m12` → `main`). Stakeholder demo runs from `main`.
