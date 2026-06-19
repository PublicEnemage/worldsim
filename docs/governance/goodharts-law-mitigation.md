# Goodhart's Law Mitigation Framework

> **Authority:** This document is the Technical Steering Committee (TSC) founding
> mandate document for parameterization integrity. It was authored by the PM Agent
> and is subject to EL review before TSC adoption. Issue #988.
>
> **Goodhart's Law (as applied to WorldSim):**
> "When a measure becomes a target, it ceases to be a good measure."
> Applied to simulation parameters: when a user can choose parameter values
> that make the simulation output any desired result, the outputs lose their
> analytical value. This framework establishes what constitutes legitimate
> calibration variation versus parameterization gaming, and what the TSC
> must do when gaming is suspected.

---

## Section 1: What Constitutes Parameterization Gaming

### Definition

**Parameterization gaming** is the practice of choosing simulation parameter
values specifically to produce a desired output narrative — rather than to
produce an accurate representation of the entity's economic situation — while
presenting the output as if it were an objective simulation result.

**Legitimate calibration variation** is the practice of choosing parameter
values because they are better supported by the available data, reflect a
specific analytical hypothesis being tested, or acknowledge a documented
calibration uncertainty range.

The line between gaming and legitimate variation is the relationship between
the parameter choice and the evidence basis. Gaming has no evidentiary basis
for the choice; legitimate variation has one.

### Concrete Gaming Examples

**fiscal_multiplier gaming:**
The fiscal multiplier parameter controls how fiscal policy shocks propagate
to GDP. The calibrated range for the fiscal multiplier in WorldSim is 0.8
(standard conditions) to 1.5 (depressed regime, unemployment > 15%), grounded
in post-2008 cross-country evidence. Setting `fiscal_multiplier = 0.3` to show
that a severe fiscal consolidation has minimal GDP impact — and presenting this
as WorldSim's output — is gaming. There is no evidence basis for a 0.3 multiplier
in a sovereign fiscal adjustment context; its function is to reverse the
simulation's honest assessment of austerity costs.

**legitimacy_index gaming:**
The legitimacy_index parameter seeds the PoliticalEconomyModule's programme
survival probability calculation. Setting `legitimacy_index = 0.95` for an
entity with documented political opposition to IMF conditionality — to show
a high programme survival probability and argue the programme is politically
feasible — is gaming when the actual V-Dem-derived governance indicators
support a 0.3–0.5 range.

**reserve_coverage floor gaming:**
Setting a custom MDA threshold for reserve coverage well below the calibrated
TERMINAL floor — to suppress a TERMINAL alert that would otherwise appear —
is gaming. The MDA threshold system exists to make critical breaches visible;
suppressing an alert by adjusting the floor without an evidence-based rationale
defeats the system's purpose.

**conditionality sequencing gaming:**
The conditionality module models how IMF programme conditions interact with
the political economy over time. Adjusting conditionality parameters to remove
the modeled implementation lag — showing that all conditions are implemented
immediately at full effect — to produce a more favorable programme survival
trajectory is gaming when the historical record shows implementation lags
are the norm, not the exception.

### Legitimate Variation

- Adjusting `fiscal_multiplier` within the calibrated range (0.8–1.5) based
  on documented evidence about the specific entity's fiscal transmission
  characteristics — with the evidence cited
- Setting alternative starting values for an indicator based on a different
  but credible primary source — with the source disclosed and a data quality
  tier assigned
- Running multiple scenarios with different parameter settings to show the
  sensitivity of conclusions to parameter uncertainty — the full range is
  disclosed, not only the most favorable result
- Adjusting the fiscal multiplier for Mode 3 "what if" branching — this is
  the explicit purpose of Mode 3 Active Control and is disclosed by the mode
  indicator in the UI

---

## Section 2: How the Tool Signals When Parameters Are at the Edge of the Validated Range

### Parameter Range Warnings

WorldSim maintains a validated range for each configurable parameter. When a
user sets a parameter to a value outside this range, the simulation signals
the deviation. This is not a prohibition — users may operate outside the
validated range for hypothesis testing — but the deviation must be visible.

**Signal types:**

| Signal | Trigger | Display location |
|---|---|---|
| Range edge warning | Parameter set within 10% of the validated range boundary | Scenario parameter panel — yellow indicator |
| Out-of-range warning | Parameter set outside the validated range | Scenario parameter panel — orange indicator with "Outside validated range" label |
| Calibration basis disclosure | Any parameter with a documented calibration basis | Grounding strip tooltip — links to calibration-basis.md section |

**For fiscal_multiplier specifically:**
- In-range: 0.8–1.5 (regime-dependent; the engine switches at 15% unemployment)
- Range edge: 0.65–0.79 or 1.51–1.75 — yellow warning appears
- Out-of-range: < 0.65 or > 1.75 — orange warning with disclosure obligation

The out-of-range warning generates a disclosure string that appears in any
export of scenario results: "Fiscal multiplier set to [value] — outside the
calibrated range of 0.8–1.5. Results reflect a hypothesis, not a calibrated
projection."

**For legitimacy_index:**
- The seeding range derived from V-Dem data for the entity is shown in the
  parameter panel before the value is set
- Setting outside the V-Dem-derived range triggers a disclosure: "Legitimacy
  index set above/below the V-Dem-derived range for [entity] in [period]"

**Parameter limit enforcement:**
Some parameter boundaries are hard limits — the simulation will not compute
with values outside them because the underlying model equations become
undefined or produce physically impossible results. Hard limits are enforced
at the API boundary; out-of-range values are rejected with an error message
explaining the valid range.

---

## Section 3: TSC Monitoring and Response Obligations

### When Gaming Is Suspected

The Technical Steering Committee must respond to a suspected parameterization
gaming report within the timeframes defined below. These are obligations, not
aspirational targets.

**TSC monitoring obligations:**

1. **Maintain a public parameterization audit log.** The TSC must maintain
   a public record of all scenario configurations that triggered out-of-range
   warnings. This log is updated automatically from the scenario export pipeline.
   TSC must review entries weekly and flag any patterns consistent with systematic
   gaming (recurring out-of-range settings from a single source or for a single
   entity).

2. **Respond to community gaming reports within 14 days.** When a community
   member files a gaming report (see Section 4 for the reporting pathway),
   a TSC member must acknowledge receipt within 48 hours and issue a preliminary
   finding within 14 days. The finding must either (a) confirm the report and
   specify what public disclosure is required, or (b) explain why the parameter
   choice constitutes legitimate variation with the evidentiary basis cited.

3. **Publish findings on confirmed gaming reports.** When a gaming report
   is confirmed, the TSC must publish a finding that names the scenario,
   the parameter values that were gamed, the intended versus actual calibrated
   range, and the remediation required before the scenario can be cited publicly.
   The finding is permanent — it is not removed if the scenario is subsequently
   corrected.

4. **Conduct quarterly parameterization reviews.** TSC must review the
   distribution of parameter settings across publicly published WorldSim
   scenarios each quarter. Outliers — parameter values that fall consistently
   at the extreme of the calibrated range across multiple scenarios from
   the same source — are investigated under the gaming definition above.

5. **Escalate systemic gaming to the Engineering Lead.** If a pattern of
   confirmed gaming is identified from a single institutional source, TSC
   must escalate to the Engineering Lead for a decision about whether access
   restrictions or mandatory disclosure requirements are appropriate.

**TSC response chain:**

| Event | TSC obligation | Timeframe |
|---|---|---|
| Community gaming report filed | Acknowledge receipt | 48 hours |
| Gaming report — preliminary finding | Confirm or dispute with evidence | 14 days |
| Gaming confirmed | Publish finding | 7 days after confirmation |
| Quarterly audit | Publish parameterization distribution summary | Last day of each quarter |

---

## Section 4: Open-Source Audit Pathway

### How the Community Can Audit Parameterization Choices

WorldSim is open source by design. The open-source audit pathway is the primary
mechanism for detecting systematic parameterization gaming that is not caught
by automated range-warning signals.

**Git history as the audit record:**
Every scenario configuration is stored in the simulation database with the git
commit hash of the WorldSim version used to produce it. The parameterization
history for any published scenario can be reconstructed from the database
record. The git log for `backend/app/db/seed/` and the scenario configuration
endpoint provide the full configuration history.

```bash
# Retrieve scenario configuration for audit
GET /api/v1/scenarios/{scenario_id}
# Returns: entity, parameter settings, engine_version_hash, step configurations

# Retrieve the WorldSim version used
git log --follow --oneline -- backend/
# Match against engine_version_hash in scenario record
```

**Public configuration export:**
Any scenario can be exported as a JSON configuration file via:
```bash
GET /api/v1/scenarios/{scenario_id}/export
```

The export includes all parameter settings, the data quality preview for the
entity, the calibrated ranges for each parameter at the time of scenario
creation, and any out-of-range warnings that were triggered. This export can
be shared publicly as a reproducibility artifact.

**Community challenge mechanism:**
To file a parameterization gaming challenge:

1. Open a GitHub issue at the WorldSim repository using the issue template
   `[Gaming Report]`
2. Include: the scenario ID or export JSON, the specific parameter(s) in
   question, the claimed gaming definition violation (citing Section 1 of
   this document), and the evidence basis for the calibrated range you
   believe applies
3. The TSC is notified automatically via the issue label `tsc:gaming-report`
4. TSC responds per Section 3 obligations

**Community audit tooling:**
The `scripts/audit_parameterization.py` script (added in M14) reads any
scenario export JSON and compares each parameter value against the calibrated
range table, flagging out-of-range values and generating a human-readable
audit report. It is designed to run without any WorldSim API access — purely
on the exported JSON.

```bash
python backend/scripts/audit_parameterization.py --scenario-export scenario_export.json
```

**Open calibration documentation:**
The full calibration basis for every modeled parameter — evidence sources,
calibrated ranges, and known uncertainty — is documented in:
- `docs/methodology/calibration-basis.md` — per-indicator calibration summary
- `docs/adr/ADR-013-political-economy-module-boundary.md` — political economy
  parameter calibration (political_stability_index, legitimacy_index,
  programme survival probability)
- `docs/DATA_STANDARDS.md §Confidence Tier System` — tier assignment rules

Anyone can inspect, challenge, and improve the calibration assumptions. That
transparency is the source of the tool's credibility.

---

*This document is the TSC founding mandate for parameterization integrity.
It is subject to EL review before TSC adoption. Changes to the gaming
definition (Section 1) or TSC obligations (Section 3) require EL approval.
Changes to the audit pathway tooling (Section 4) follow the standard
implementation lifecycle.*
