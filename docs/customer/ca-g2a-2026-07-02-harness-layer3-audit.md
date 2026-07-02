---
name: ca-g2a-harness-layer3-audit
type: customer-agent-audit
deliverable: M19 G2A — Headless Battle-Testing Harness (#1546)
intent-document: docs/process/intents/M19-G2A-2026-07-02-headless-battle-testing-harness.md
authored-by: Customer Agent
date: 2026-07-02
verdict: PASS
scope-boundary: Analyst-mediated — not direct Persona 5 output
---

# Customer Agent Layer 3 Audit — G2A Headless Battle-Testing Harness

**Deliverable:** Mode 3 headless battle-testing harness (`backend/app/harness/mode3_harness.py`)
**Intent document:** `docs/process/intents/M19-G2A-2026-07-02-headless-battle-testing-harness.md`
**Audit date:** 2026-07-02
**Activation:** Customer Agent: AUDIT — G2A headless battle-testing harness (Layer 3 precondition for Business PO ACCEPT)

---

## Layer 3 Assessment

### Primary question
*Does this output tell the user what the number means, or only display the number?*

### Target user and entry state
**Persona:** Persona 2 — Ministry Analyst (quantitative analyst on a finance ministry team). Not the Finance Minister directly. Operating in **analytical preparation mode** — preparing evidence for a restructuring session or creditor review. The intent document's P-1 makes this explicit: the harness is analytical preparation material, not a 90-second table-side instrument.

### Applicable gates

**5-minute preparation gate:**
Can the Ministry Analyst, sitting with the harness output during session preparation, extract calibration evidence meaning in under 5 minutes without specialist mediation?

**Checked against all four format outputs (Markdown — most likely to be shared):**

| Output element | What it says | Self-interpreting? |
|---|---|---|
| `fidelity_tier: DIRECTION_ONLY` | Tier label alone | Partially — label is self-describing but requires knowing the tier hierarchy |
| `fidelity_rationale: "..."` | Brief explanation of why this tier was assigned | YES — plain-language explanation immediately follows the label |
| `known_limitations` block | e.g., "⚠ DIRECTION_ONLY at most — threshold-crossing step counts unreliable (Issue #30)" | YES for analyst — the consequence is stated in plain language; the issue number is citation context, not load-bearing interpretation |
| `direction_verdict: COUNTER_FACTUAL_BETTER` | Verdict label | YES — three-state enum with self-describing labels |
| Per-step `fin_composite`, `hd_composite`, etc. | Decimal values | PARTIAL — values are interpretable as trends (rising/falling composite scores) but require familiarity with the composite score range to interpret absolute values |

**5-minute gate verdict:** PASS. The analyst can extract the key calibration message — "the model achieves DIRECTION_ONLY fidelity on Greece 2010–12; the two known limitations are stock-flow accounting and frozen bilateral weights" — from the Markdown or ASCII output within 5 minutes of opening it. The `fidelity_rationale` field is the critical Layer 3 feature: it ensures the label is accompanied by a plain-language explanation. The implementation includes this field in the `summary` block.

**90-second table-side gate:**
This gate does NOT apply to the harness output. Per intent document §5 (Kryptonite), the harness is not a Persona 2 direct action tool in the reactive 90-second window. It is analytical preparation material that feeds the analyst's understanding, which in turn shapes the CI bounds displayed in the instrument panel. The table-side artifact for Demo 8 is the instrument panel's CI band display (G3 output) — not the harness report.

**Layer 3 issue numbers in known_limitations:**
The `known_limitations` list includes Issue numbers (#30, #35, #1532) alongside plain-language descriptions. For the target user (Ministry Analyst), the issue number is useful citation context — "Issue #30" is a citable reference for the stock-flow accounting gap. For a non-technical user, the issue number is opaque. Assessment:
- For the Ministry Analyst: adequate — the consequence is stated in plain language, the issue number is a citation supplement
- For the Institutional Decision-Maker (Persona 5): NOT adequate without the analyst serving as the interpretive layer

This is an acceptable scope boundary, not a failure — see §Scope Boundary below.

---

## Scope Boundary — Documented Constraint

**The harness output is designed for Persona 2 (Ministry Analyst) — NOT for direct presentation to Persona 5 (Institutional Decision-Maker / World Bank evaluator).**

Raw harness output shown directly to Aicha Mbaye (Persona 5) in Demo 8 without analyst mediation would fail the Customer Agent's Layer 3 standard for Persona 5. Issue numbers, composite score decimal values, and fidelity tier labels require analyst interpretation before reaching a non-technical decision-maker.

**The Demo 8 narrative chain is correct:** harness output → analyst interprets → CI intervals displayed in instrument panel → Aicha sees the instrument panel plus the analyst's verbal characterisation ("these bounds are grounded in empirical backtesting — here is the fidelity tier result"). This chain preserves Layer 3 usability at each audience level.

**If Demo 8 deviates:** If the Demo 8 script ever shows raw harness output to the stakeholder audience directly (e.g., a terminal printout or Markdown report as a slide), the Customer Agent flags this as a Layer 3 failure before the demo rehearsal. The rehearsal review (Independent Review Agent step 7) should catch this — but the Customer Agent's standing mandate includes flagging it before IR, not only catching it at IR.

---

## Customer Agent Verdict

**PASS — Persona 2 (Ministry Analyst) analytical preparation context.**

The harness output is self-interpreting for its target user in the preparation context where it is used. The `fidelity_tier` + `fidelity_rationale` + `known_limitations` block together answer the analyst's calibration evidence question without requiring specialist mediation beyond what the Ministry Analyst IS.

**Scope boundary recorded:** Harness output is not suitable for direct Persona 5 presentation without analyst mediation. Demo 8 narrative must route through the analyst layer. Customer Agent holds standing watch on this boundary through the Demo 8 internal review.

**Precondition satisfied:** Business PO may now execute the ACCEPT step for G2A.

---

*Authority: docs/process/acceptance-protocol.md §1.4 (Analytics); docs/process/agents.md §Customer Agent.*
*Filed as precondition for Business PO ACCEPT — docs/process/intents/M19-G2A-2026-07-02-headless-battle-testing-harness.md.*
