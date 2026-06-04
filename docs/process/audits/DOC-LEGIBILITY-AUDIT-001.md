# DOC-LEGIBILITY-AUDIT-001: Documentation Legibility Audit

**Date:** 2026-06-03
**Issue:** #621 — Documentation legibility audit (M11)
**Reviewer role:** Senior software engineer encountering the WorldSim project for
the first time. Reviewing without institutional memory of past decisions, agent
personas, or accumulated project context.
**Method:** Independent agent review — three-question format per document.
**Documents audited:** 5 (CLAUDE.md, ADR-008, ADR-010, ADR-007, ux-architecture-first-principles.md)

---

## Review Question Template

For each document:
1. **What problem does this document solve?** (plain language, one sentence)
2. **What does a developer need to know before making a change in this area?**
3. **Where did I have to re-read or stop and infer?** (legibility gaps)

---

## Document 1: CLAUDE.md

### Q1 — What problem does this document solve?

CLAUDE.md establishes the invariant context for all agents working in this
codebase — the mission, principles, architectural commitments, and process rules that
a developer (human or AI) must hold before making any decision.

The one-sentence version is clear to me: *"This is the permanent constitution — read
it before touching anything."* That sentence actually appears in the document implicitly.
It should appear explicitly in the first paragraph.

### Q2 — What does a developer need to know before making a change?

The document answers this — thoroughly. Session Continuity, Role-based mandatory
reading, the Guiding Principles, the Platform Principle, and the Architectural
Principles for Claude Code Sessions give a comprehensive brief. A developer who reads
CLAUDE.md fully before working is well-equipped.

The problem is that CLAUDE.md is long (400+ lines) and does not signal which parts
are must-reads vs. reference material. A developer who skims for the relevant section
may miss the process rules that are most likely to cause compliance violations if not
followed (pre-push lint gate, PR merge gate, file authority).

### Q3 — Legibility gaps

**Gap 1 — No entry-point paragraph.** CLAUDE.md opens with metadata ("Last significant
revision") and immediately launches into "What This Project Is." A developer who has
just been told "read CLAUDE.md first" does not get a sentence that says "this document
is the constitution — here is how to use it." The Session Continuity section tells you
what to read in what order, but it appears in section 3, not section 0.

**Gap 2 — The process rules are buried.** The most consequential process rules —
PR merge gate, backend pre-push lint gate, frontend pre-push build gate, file authority
— appear in §Architectural Principles for Claude Code Sessions. This section is accurate
and important. But "Architectural Principles for Claude Code Sessions" does not signal
to a new developer that it contains a gate they will trigger on their first push. A
heading like "Process Gates and Authority Rules" would be more accurate.

**Gap 3 — The canonical artifact locations table has no quick-reference use instructions.**
The table lists artifact types and naming conventions but does not say "before creating
any document, use the pre-creation checklist below." The checklist exists — it is three
paragraphs below — but the table does not point to it.

**Severity:** MEDIUM. The document is not illegible — it is information-dense. A
developer who reads it carefully is well-equipped. The gaps are entry-point and
navigation gaps, not comprehension gaps.

---

## Document 2: ADR-008 — UX Architecture

### Q1 — What problem does this document solve?

ADR-008 solves the problem that WorldSim's M8 UX had the instruments in a drawer
instead of the primary viewport, which would fail when Mode 3 (Active Control) requires
always-visible instruments.

This is stated clearly in the Context section. The "Case B Finding" subsection explains
the problem in plain language. The phrase "inversion" is precise and memorable.

### Q2 — What does a developer need to know before making a change?

The Renewal Triggers section is excellent — specific, named, actionable. A developer
who reads the Renewal Triggers knows exactly what changes would require re-opening
the ADR. The Decision sections give the specific contracts (zone sizes, color
assignments, simultaneous update requirement).

The main thing a developer needs to know: **there are five numbered Decisions in this
ADR, and any change in the areas they cover requires checking whether it touches a
Renewal Trigger.** That fact is not stated directly — a developer must infer it from
the Validity Context structure.

### Q3 — Legibility gaps

**Gap 1 — The Validity Context block is front-loaded before the Context.** The first
thing a new reader sees after "Status: Accepted" is a dense Validity Context block with
standards version, license status, M10 exit review notes, and renewal triggers. This
block is essential reference material for maintenance — but it is not what a new reader
needs to understand what the ADR is about. Recommendation: move Validity Context after
the Context and Decision sections, or add a one-sentence Summary before it.

**Gap 2 — "Case B" is unexplained jargon.** "The UX Design Thinking Agent critique...
produced a Case B verdict" — a new reader does not know what Case A and Case B mean
without reading a different document. If Case B is a technical term with a specific
meaning (appears to mean "requires rethink before implementation"), that meaning should
be defined inline.

**Gap 3 — The five governing premises appear both here and in CLAUDE.md.** A developer
encounters the same five premises in two places with slightly different wording. Which
is authoritative? The ADR is more specific. But CLAUDE.md calls them "architectural
commitments" while ADR-008 calls them "governing premises." A note that CLAUDE.md's
§UX Architectural Commitments cites ADR-008 as the authority would close the loop.

**Severity:** LOW. ADR-008 is well-structured. The gaps are navigation and
cross-reference gaps, not missing content.

---

## Document 3: ADR-010 — Trajectory View Component Architecture

### Q1 — What problem does this document solve?

ADR-010 specifies how the trajectory view is built: component boundary, data contract,
rendering approach, and state management — deferring these decisions that ADR-008
explicitly left open.

The Context §Background section states this clearly: "ADR-008 defers the following
questions explicitly to this ADR." This is effective — it tells the reader exactly
why this ADR exists.

### Q2 — What does a developer need to know before making a change?

The Renewal Triggers section is specific and well-organized. The Decision sections give
precise contracts (Recharts-specific primitives, strokeDasharray values, opacity thresholds).

A frontend developer making a change to the trajectory view needs to: (1) read the
relevant Decision section, (2) check if the change touches a Renewal Trigger, (3) check
if it touches ADR-008's contracts (which ADR-010 implements). Step (3) is not stated
explicitly — a developer must infer that changes to ADR-010's implementation layer
might also require re-checking ADR-008.

### Q3 — Legibility gaps

**Gap 1 — Rendering technology names appear without rationale.** "Recharts/SVG" is
specified as the rendering technology. A developer who wants to understand *why* this
was chosen finds no rationale in the ADR — only the constraint that changing it fires
a Renewal Trigger. The absence of a rationale means the next developer who encounters
a performance problem cannot evaluate whether the chosen technology is still the right
call without re-opening the ADR.

**Gap 2 — The Zone 1A designation is used without definition.** The ADR refers to
"Zone 1A" throughout. A developer reading this ADR without having read ADR-008 first
does not know what Zone 1A is. The background section says "Zone 1A — the primary
instrument" but does not explain Zone 1's structure or the A designation. A reader
needs ADR-008 as a prerequisite, and that prerequisite is not stated.

**Gap 3 — The Acceptance Criteria section exists but its relationship to the Decisions
is unclear.** The ADR has both a Decision section and an Acceptance Criteria section.
The ACs test the decisions — but the mapping between specific ACs and specific Decisions
is not explicit. A developer writing a test cannot easily identify which Decision their
test validates.

**Severity:** LOW-MEDIUM. The ADR is well-organized. The prerequisite gap (ADR-008
must be read first) and the missing rationale are the most consequential.

---

## Document 4: ADR-007 — Synthetic Data Framework

### Q1 — What problem does this document solve?

ADR-007 solves the problem that WorldSim cannot serve data-poor environments (its
primary constituency) if it requires high-quality real data to function. It establishes
a synthetic data generation framework that allows the tool to operate honestly in
data-poor conditions.

The Context section states this well: "Data poverty is not a methodological edge case;
it is a structural feature of the environments where the tool's democratization value
is highest." This is plain-language and motivating.

### Q2 — What does a developer need to know before making a change?

ADR-007 is the most technically dense of the five documents. It specifies: seven
sections covering generation methods, confidence tier extension, disclosure
architecture, scenario banding, MDA alert interaction, anomaly detection governance,
and a Quantity schema extension. A developer making a change needs to know which of
the seven sections their change touches.

The Renewal Triggers section identifies the specific changes that require re-review.
A developer who checks the Renewal Triggers before any change is protected.

### Q3 — Legibility gaps

**Gap 1 — Seven sections with no map.** The ADR has seven numbered sections after
the Decision statement. A developer encounters Section 1 (Synthetic Data Generation
Methods) without knowing that Section 3 (Disclosure Architecture) is also relevant
to their change. A one-paragraph guide ("if you are changing the generation methods,
read Section 1; if you are changing what is displayed to users, read Section 3")
would reduce navigation burden significantly.

**Gap 2 — "max() rule" appears in Renewal Triggers without explanation.** "The
confidence tier arithmetic (max() rule) is changed in `docs/DATA_STANDARDS.md`" —
a developer encounters this trigger without knowing what the max() rule is. This is
an important contract (when synthetic data is involved, the confidence tier is the
maximum of the input confidence tiers, not the minimum). It should be defined in the
ADR, not only in DATA_STANDARDS.md.

**Gap 3 — The meaninglessness threshold section (Section 6) is the most consequential
gap and the hardest to find.** Section 6 specifies when the tool must refuse to generate
an output because uncertainty is so large the output would mislead. This is one of the
most important decisions in the ADR — it determines when WorldSim says "I cannot
compute this" instead of producing a misleading estimate. Its title ("Meaninglessness
Threshold — Output Refusal Conditions") is accurate but not attention-signaling. A
developer who does not read to Section 6 might implement a synthetic data consumer
that displays outputs the framework is supposed to suppress.

**Severity:** MEDIUM. The ADR is comprehensive but navigation-heavy. The meaninglessness
threshold gap is the most consequential legibility failure.

---

## Document 5: docs/ux/design-thinking/worldsim-ux-architecture-first-principles.md

### Q1 — What problem does this document solve?

This document solves the problem that the M8 UX architecture would fail Mode 3
(Active Control) — and derives five governing premises from first principles rather
than by iteration, to ensure the rethink produces an architecture that survives the
full product vision rather than the current mode.

The opening section states this clearly: "This document does not optimize the current
UX. It evaluates whether the current UX architecture can survive the product WorldSim
is becoming." This is an unusually direct and useful orientation statement.

### Q2 — What does a developer need to know before making a change?

The five governing premises and four Mode 3 requirements (R1–R4) are the core
deliverable. A developer making a UX change must check whether it violates any of the
five premises. The premises are stated clearly in the document.

The key thing to know: this document is the *derivation* of ADR-008, not a separate
standard. ADR-008 is the canonical authority; this document explains why ADR-008 was
written the way it was. A developer who changes something this document says should not
change must check whether they have triggered an ADR-008 Renewal Trigger.

### Q3 — Legibility gaps

**Gap 1 — The relationship to ADR-008 is unstated.** A developer reading this document
does not know that ADR-008 is the canonical authority derived from it. The document
says "CLAUDE.md §UX Architectural Commitments" is derived from it, but ADR-008 is not
mentioned. A developer who treats this document as authoritative (rather than ADR-008)
may act on its derivations without checking the ADR's Renewal Triggers.

**Gap 2 — The document is long and its conclusion is buried.** The five governing
premises — the document's primary deliverable — appear about halfway through, after
extensive derivation. A reader who needs the premises but not the derivation must read
through pages of reasoning to reach them. A summary box at the top listing the five
premises with section references would serve most readers better.

**Gap 3 — "Case A" and "Case B" are defined here but used in ADR-008 without reference.**
This document introduces the Case A / Case B terminology. A developer reading ADR-008
first (which cites "a Case B verdict") encounters undefined jargon without knowing this
document is where the terminology originated. A bidirectional cross-reference is missing.

**Severity:** LOW-MEDIUM. This document is well-reasoned and the derivation is valuable.
The main gap is that its relationship to ADR-008 is unclear — it reads like an authority
when it is actually the derivation.

---

## Summary Table

| Document | Q1 clarity | Most consequential gap | Severity |
|---|---|---|---|
| CLAUDE.md | Clear — but entry point missing | No summary of must-read vs. reference; process gates buried under architectural heading | MEDIUM |
| ADR-008 | Clear — Case B and inversion explanation effective | Validity Context front-loaded before Context; "Case B" undefined | LOW |
| ADR-010 | Clear — "ADR-008 defers the following" framing effective | Recharts rationale absent; Zone 1A prerequisite unstated | LOW-MEDIUM |
| ADR-007 | Clear — data poverty framing strong | Seven sections without a map; meaninglessness threshold findability | MEDIUM |
| UX first-principles | Clear — orientation statement strong | Relationship to ADR-008 unstated; five premises buried halfway through | LOW-MEDIUM |

---

## Cross-Cutting Finding

All five documents share one root cause: **no document explains to the reader how to
use it before presenting its content.** The orientation for each document — "read this
when X, skip Y if you only need Z, ADR-NNN is the authority on this topic" — is absent
or embedded deep in the document body.

This is a structural gap, not a content gap. The content is accurate and thorough.
The navigation problem is that a new contributor must read the whole document to know
which part of it applies to their situation.

---

## Proposed Documentation Standard

The following one-paragraph standard should appear in `docs/CONTRIBUTING.md §Document
Authoring Standard` and in the MILESTONE_RUNBOOK.md:

> Every document that an agent or developer consults before making a decision must
> open with a **Reader Orientation** paragraph (three sentences maximum). The paragraph
> answers: (1) What problem does this document solve? (2) Who should read this document,
> and under what circumstances? (3) What is the canonical authority for this topic —
> is this document the authority, or does a specific ADR or standard supersede it?
> This paragraph appears immediately after the document title and metadata, before any
> technical content.

---

## EL Decision on Remediation Scope

**Decision date:** 2026-06-03

**Scope accepted for M11:**
- Add Reader Orientation paragraph to `CLAUDE.md` and `ADR-007` — MEDIUM severity, highest traffic
- Add ADR-008 ↔ ux-architecture-first-principles cross-reference — LOW cost, closes a genuine gap
- No full rewrites — the content is accurate; the navigation is the problem

**Scope deferred to M12:**
- Reader Orientation paragraphs for ADR-008, ADR-010, ux-architecture-first-principles
- Renaming §Architectural Principles for Claude Code Sessions in CLAUDE.md
- ADR-007 navigation guide ("if you are changing X, read Section N")
- Proposed Documentation Standard in CONTRIBUTING.md — implement when the first new ADR
  is written in M12 so it can be applied immediately to a new artifact

**Scope declined:**
- Restructuring the Validity Context block in ADRs — the front-loaded position is a
  deliberate convention for maintenance efficiency; the cost of changing it across all
  ADRs exceeds the legibility benefit

---

*Audit closed: 2026-06-03 — closes Issue #621*
