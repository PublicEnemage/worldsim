"""Content-presence tests for M15-G3 cohort disaggregation and political risk
summary design documents.

QA Lead note — authored from intent document at:
  docs/process/intents/M15-G3-2026-06-21-cohort-disaggregation-design.md

G3 is a design-only deliverable. The intent document states "No QA Lead test
authorship obligation" — but the observable application states ARE the design
documents meeting specific completeness criteria, verifiable by any agent
reading the files. These tests are the automatable equivalent of the
Architecture Review Facilitator's acceptance check (§7 of the intent doc).

All tests fail until the UX Designer Agent files the two design documents
(Step 3). No database, server, or simulation engine required — pure filesystem
checks. The Architecture Review Facilitator confirmation (§7) remains a
required manual gate at Step 5; these tests confirm the machine-verifiable
preconditions for that confirmation.

Files under test:
  docs/ux/design-thinking/cohort-disaggregation-design.md  (issues #986)
  docs/ux/design-thinking/political-risk-summary-design.md  (issue #987)

AC coverage:
  AC-1   cohort-disaggregation: Zone Placement section — names Zone + cognitive
         task + information-hierarchy.md reference
  AC-2   cohort-disaggregation: Cohort scope definition — income quintile;
         rationale tied to Persona 2 negotiating argument
  AC-3   cohort-disaggregation: Indicator scope — ≥1 poverty/HD indicator;
         threshold type per indicator; CRITICAL/WARNING/WATCH schema
  AC-4   cohort-disaggregation: Literal display format — code block with cohort
         label, indicator, severity, step; max rows and sort order stated
  AC-5   cohort-disaggregation: ADR-017 interplay — explicit disposition (a) or (b)
  AC-6   cohort-disaggregation: M16 Implementation Gate section with named deps
  AC-7   political-risk-summary: Zone Placement + Zone 1D conflict check
  AC-8   political-risk-summary: Mode-specific display contract — separate
         Mode 1 / Mode 2 sections with named indicators and update behaviour
  AC-9   political-risk-summary: Literal sentence example — ZMB ECF step 3
         PSP≈0.38; historical analogue present
  AC-10  political-risk-summary: 30-second legibility check — names jargon
         eliminated
  AC-11  political-risk-summary: ADR disposition (new ADR or not) + M16
         Implementation Gate with #1084 dependency addressed

Silent failure guards (§3.3 of intent doc):
  AC-4: a prose description without a literal text block / code fence FAILS.
        "Zone 1B will display cohort alerts clearly" is NOT a display contract.
  AC-9: a sentence template without ZMB+step3+PSP value FAILS.
        "Programme survival will be shown as CRITICAL (NN%)" is NOT specific.
"""

from __future__ import annotations

import pathlib
import re

import pytest

_REPO_ROOT = pathlib.Path(__file__).parent.parent.parent

_COHORT_DESIGN = (
    _REPO_ROOT
    / "docs"
    / "ux"
    / "design-thinking"
    / "cohort-disaggregation-design.md"
)

_POLITICAL_RISK_DESIGN = (
    _REPO_ROOT
    / "docs"
    / "ux"
    / "design-thinking"
    / "political-risk-summary-design.md"
)

# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------


def _text(path: pathlib.Path) -> str:
    return path.read_text(encoding="utf-8")


def _section_text(full: str, heading_pattern: str) -> str | None:
    """Return the text of a section starting at a matching heading.

    Returns everything from the heading up to (but not including) the next
    same-level heading, or end of file.
    """
    m = re.search(heading_pattern, full, re.IGNORECASE | re.MULTILINE)
    if not m:
        return None
    start = m.start()
    # Find next heading at same or higher level
    level_match = re.match(r"(#{1,6})\s", full[start:])
    if not level_match:
        return full[start:]
    level = len(level_match.group(1))
    next_heading = re.search(
        r"^#{1," + str(level) + r"}\s",
        full[start + 1 :],
        re.MULTILINE,
    )
    if next_heading:
        return full[start : start + 1 + next_heading.start()]
    return full[start:]


# ============================================================================
# AC-1 — cohort-disaggregation: Zone Placement section
# ============================================================================


class TestAC1ZonePlacement:
    """AC-1: cohort-disaggregation-design.md names a Zone for cohort
    disaggregation, references information-hierarchy.md, and names the
    receiving zone's primary cognitive task."""

    def test_file_exists(self) -> None:
        assert _COHORT_DESIGN.exists(), (
            "docs/ux/design-thinking/cohort-disaggregation-design.md must exist. "
            "This is the primary G3 deliverable for issue #986."
        )

    def test_zone_placement_section_present(self) -> None:
        text = _text(_COHORT_DESIGN)
        assert re.search(
            r"^#{1,4}\s+.*Zone Placement",
            text,
            re.IGNORECASE | re.MULTILINE,
        ), (
            "cohort-disaggregation-design.md must contain a section heading "
            "matching 'Zone Placement' (AC-1). "
            "The section must name which Zone (1A, 1B, 1D, or new surface) "
            "hosts cohort disaggregation on the primary surface."
        )

    def test_zone_named_in_placement(self) -> None:
        text = _text(_COHORT_DESIGN)
        section = _section_text(text, r"^#{1,4}\s+.*Zone Placement")
        assert section is not None, "Zone Placement section must be present (checked above)"
        assert re.search(r"\bZone\s+1[ABCD]\b|\bnew\s+surface\b|\bZone\s+2\b", section), (
            "Zone Placement section must name a specific Zone "
            "(Zone 1A, Zone 1B, Zone 1D, or 'new surface'). "
            "'We should place cohort data prominently' is not a placement decision."
        )

    def test_information_hierarchy_reference(self) -> None:
        text = _text(_COHORT_DESIGN)
        section = _section_text(text, r"^#{1,4}\s+.*Zone Placement")
        assert section is not None, "Zone Placement section must be present (checked above)"
        assert re.search(r"information-hierarchy", section, re.IGNORECASE), (
            "Zone Placement rationale must reference information-hierarchy.md "
            "by name (AC-1). The rationale must be derived from a named section "
            "of that document — not from general principles."
        )

    def test_cognitive_task_named(self) -> None:
        text = _text(_COHORT_DESIGN)
        section = _section_text(text, r"^#{1,4}\s+.*Zone Placement")
        assert section is not None, "Zone Placement section must be present (checked above)"
        assert re.search(
            r"cognitive task|primary task|primary function|primary purpose",
            section,
            re.IGNORECASE,
        ), (
            "Zone Placement rationale must name the receiving zone's primary cognitive task "
            "(AC-1). A rationale that does not name the cognitive task cannot confirm "
            "that cohort disaggregation serves (not conflicts with) that task."
        )


# ============================================================================
# AC-2 — cohort-disaggregation: Cohort scope definition
# ============================================================================


class TestAC2CohortScope:
    """AC-2: cohort-disaggregation-design.md names income quintile as the
    minimum cohort dimension with rationale tied to Persona 2's negotiating
    argument. Additional cohort dimensions are included or deferred with rationale."""

    def test_income_quintile_present(self) -> None:
        text = _text(_COHORT_DESIGN)
        assert re.search(
            r"income quintile|bottom quintile|poorest quintile|quintile",
            text,
            re.IGNORECASE,
        ), (
            "cohort-disaggregation-design.md must name income quintile as a "
            "cohort dimension (AC-2). Income quintile is the minimum required "
            "cohort dimension per the intent document §4 AC-2."
        )

    def test_persona_2_rationale(self) -> None:
        text = _text(_COHORT_DESIGN)
        assert re.search(
            r"Persona\s*2|negotiating argument|negotiat\w+|finance ministr",
            text,
            re.IGNORECASE,
        ), (
            "cohort-disaggregation-design.md must tie the cohort selection rationale "
            "to Persona 2's negotiating argument (AC-2). "
            "'Data is available for income quintiles' is not an acceptable rationale — "
            "the selection must be mission-driven (which cohort argument is most "
            "critical at the negotiating table)."
        )

    def test_additional_cohorts_addressed(self) -> None:
        text = _text(_COHORT_DESIGN)
        # At least one additional cohort dimension must be named and explicitly
        # included or deferred — age/regional/gender cohort are the examples.
        assert re.search(
            r"age cohort|regional cohort|gender cohort|rural.urban|deferred",
            text,
            re.IGNORECASE,
        ), (
            "cohort-disaggregation-design.md must explicitly address additional "
            "cohort dimensions beyond income quintile (AC-2): include with rationale "
            "or defer with a named target milestone. "
            "Silence on additional cohorts is not an acceptable design document."
        )


# ============================================================================
# AC-3 — cohort-disaggregation: Indicator scope definition
# ============================================================================


class TestAC3IndicatorScope:
    """AC-3: cohort-disaggregation-design.md names cohort-level indicators
    with at least one poverty/HD indicator, threshold type per indicator,
    and CRITICAL/WARNING/WATCH severity tier schema."""

    def test_poverty_or_hd_indicator_present(self) -> None:
        text = _text(_COHORT_DESIGN)
        assert re.search(
            r"poverty headcount|poverty gap|child malnutrition|school enrollment"
            r"|stunting|wasting|undernourish|education",
            text,
            re.IGNORECASE,
        ), (
            "cohort-disaggregation-design.md must name at least one poverty or "
            "human development indicator (AC-3): poverty headcount, poverty gap, "
            "child malnutrition, school enrollment rate, or equivalent. "
            "Chief Methodologist confirmation of methodological defensibility "
            "requires this specificity."
        )

    def test_threshold_type_per_indicator(self) -> None:
        text = _text(_COHORT_DESIGN)
        assert re.search(
            r"MDA.{0,40}threshold|threshold.{0,40}MDA"
            r"|cohort.specific threshold|cohort-specific"
            r"|threshold type|threshold basis",
            text,
            re.IGNORECASE,
        ), (
            "cohort-disaggregation-design.md must state the threshold type for "
            "each surfaced indicator (AC-3): whether derived from the MDA architecture "
            "(existing floor system) or a cohort-specific threshold requiring new "
            "calibration. This is the Chief Methodologist sign-off precondition."
        )

    def test_severity_tier_schema_present(self) -> None:
        text = _text(_COHORT_DESIGN)
        assert "CRITICAL" in text and "WARNING" in text and "WATCH" in text, (
            "cohort-disaggregation-design.md must define the severity tier schema "
            "for cohort thresholds — how CRITICAL, WARNING, and WATCH map to cohort "
            "threshold proximity (AC-3). All three severity tiers must be named."
        )


# ============================================================================
# AC-4 — cohort-disaggregation: Zero-interaction display format
# ============================================================================


class TestAC4DisplayFormat:
    """AC-4: cohort-disaggregation-design.md shows the exact display format
    as a literal text block or wireframe — not prose description.

    Silent failure guard from intent doc §3.3:
    'Zone 1B will display cohort alerts clearly' FAILS this check.
    A code fence with specific cohort label, indicator, severity, and step PASSES.
    """

    def test_literal_format_block_present(self) -> None:
        text = _text(_COHORT_DESIGN)
        # Must be a code fence or a structured ASCII block — not prose
        has_code_fence = bool(re.search(r"```", text))
        has_ascii_table = bool(re.search(r"─{10,}|={10,}|\|.*\|", text))
        assert has_code_fence or has_ascii_table, (
            "cohort-disaggregation-design.md must contain a literal text block or "
            "wireframe (code fence or ASCII table) showing the display format (AC-4). "
            "Prose description ('Zone 1B will display cohort threshold alerts') "
            "does NOT satisfy AC-4. "
            "A QA reviewer must be able to complete the sentence: "
            "'In a ZMB ECF Mode 2 scenario at step 2, Zone [N] shows [specific format]' "
            "from this block alone."
        )

    def test_severity_badge_in_format_block(self) -> None:
        text = _text(_COHORT_DESIGN)
        # Look for CRITICAL or WARNING inside or near code fences
        code_blocks = re.findall(r"```.*?```", text, re.DOTALL)
        ascii_tables = re.findall(r"(?:─{10,}|={10,}).*?(?:─{10,}|={10,})", text, re.DOTALL)
        candidate_blocks = code_blocks + ascii_tables
        if not candidate_blocks:
            # If no code fence or ascii table, check the full text for severity labels
            found = bool(re.search(r"\bCRITICAL\b|\bWARNING\b|\bWATCH\b", text))
        else:
            found = any(
                re.search(r"\bCRITICAL\b|\bWARNING\b|\bWATCH\b", block)
                for block in candidate_blocks
            )
        assert found, (
            "The literal display format block in cohort-disaggregation-design.md "
            "must show a severity badge (CRITICAL, WARNING, or WATCH) in the format "
            "itself — not only in a separate section (AC-4). "
            "The format block must be self-interpreting for a QA reviewer."
        )

    def test_cohort_label_in_format_block(self) -> None:
        text = _text(_COHORT_DESIGN)
        # Cohort label must use plain language — "Bottom quintile" not "hh_exp_q1"
        assert re.search(
            r"(?:bottom|lower|middle|upper|top)\s+(?:quintile|income|cohort)"
            r"|(?:quintile)\s+\d",
            text,
            re.IGNORECASE,
        ), (
            "The literal display format block must use plain-language cohort labels "
            "('Bottom quintile', 'Lower-middle quintile', etc.) — not field keys "
            "('hh_exp_q1'). Kryptonite constraint from intent doc §5: "
            "any display requiring Persona 2 to know which field key maps to which "
            "cohort does NOT satisfy the constraint."
        )

    def test_max_rows_stated(self) -> None:
        text = _text(_COHORT_DESIGN)
        assert re.search(
            r"\d+\s*rows?\s*(max|maximum|visible|without scroll)"
            r"|max(?:imum)?\s+\d+\s*rows?",
            text,
            re.IGNORECASE,
        ), (
            "cohort-disaggregation-design.md must state the maximum number of rows "
            "visible without scroll at 1440×900 (AC-4). "
            "The 90-second zero-interaction ceiling (P-4) requires an explicit row limit — "
            "'as many as needed' is not a design decision."
        )

    def test_sort_order_stated(self) -> None:
        text = _text(_COHORT_DESIGN)
        assert re.search(
            r"sort(?:ed)?|order(?:ed)?|rank(?:ed)?|severity.first|CRITICAL.first",
            text,
            re.IGNORECASE,
        ), (
            "cohort-disaggregation-design.md must state the sort order for cohort rows "
            "(AC-4): by severity, by step, alphabetical, or other — explicitly named. "
            "Unstated sort order prevents implementation from matching the design."
        )


# ============================================================================
# AC-5 — cohort-disaggregation: ADR-017 interplay statement
# ============================================================================


class TestAC5ADR017Interplay:
    """AC-5: cohort-disaggregation-design.md contains one of two explicit
    ADR-017 disposition statements — (a) subsumed into ADR-017 or
    (b) proceeds independently with non-conflict statement."""

    def test_adr_017_mentioned(self) -> None:
        text = _text(_COHORT_DESIGN)
        assert re.search(r"ADR.017|ADR-017", text, re.IGNORECASE), (
            "cohort-disaggregation-design.md must mention ADR-017 (AC-5). "
            "Issue #986 body states: 'The design may be subsumed into the Zone 1A "
            "ADR (#845 Phase 3) if cohort data belongs in Zone 1A.' "
            "G3 exists to answer this question — silence is not an answer."
        )

    def test_explicit_disposition_present(self) -> None:
        text = _text(_COHORT_DESIGN)
        # Check for disposition (a): subsumed into ADR-017
        disposition_a = bool(re.search(
            r"subsumed.{0,60}ADR.017|ADR.017.{0,60}subsumed"
            r"|input.{0,60}ADR.017.{0,60}panel|ADR.017.{0,60}panel.{0,60}input",
            text,
            re.IGNORECASE,
        ))
        # Check for disposition (b): proceeds independently
        disposition_b = bool(re.search(
            r"proceeds independently|independent.{0,60}ADR.017"
            r"|does not depend.{0,60}ADR.017|non.conflict",
            text,
            re.IGNORECASE,
        ))
        assert disposition_a or disposition_b, (
            "cohort-disaggregation-design.md must contain an explicit ADR-017 "
            "disposition statement (AC-5): either (a) cohort disaggregation is "
            "subsumed into ADR-017 as input, or (b) it proceeds independently "
            "with a non-conflict statement. "
            "A statement that defers this question to M16 is not acceptable — "
            "G3 exists to resolve it before M16 sprint entry is filed."
        )


# ============================================================================
# AC-6 — cohort-disaggregation: M16 Implementation Gate section
# ============================================================================


class TestAC6M16GateCohort:
    """AC-6: cohort-disaggregation-design.md ends with a M16 Implementation Gate
    section listing named dependencies (not 'see above')."""

    def test_m16_gate_section_present(self) -> None:
        text = _text(_COHORT_DESIGN)
        assert re.search(
            r"^#{1,4}\s+.*M16 Implementation Gate",
            text,
            re.IGNORECASE | re.MULTILINE,
        ), (
            "cohort-disaggregation-design.md must contain a section titled "
            "'M16 Implementation Gate' (or equivalent) (AC-6). "
            "This section prevents M16 sprint entry from reopening ADR-017 and "
            "Chief Methodologist threshold calibration questions."
        )

    def test_named_dependencies_not_see_above(self) -> None:
        text = _text(_COHORT_DESIGN)
        gate_section = _section_text(text, r"^#{1,4}\s+.*M16 Implementation Gate")
        # "checked above" — AC-6 test_m16_gate_section_present covers existence
        assert gate_section is not None, "M16 Implementation Gate section must exist"
        # Must not be a stub that just says "see above"
        assert "see above" not in gate_section.lower(), (
            "M16 Implementation Gate section must list named dependencies — "
            "'see above' is not an acceptable entry (AC-6). "
            "Named examples: 'ADR-017 must be accepted', "
            "'CM must confirm threshold calibration', "
            "'No blocking dependencies — M16 sprint entry may be filed when G3 "
            "design documents are accepted by the Architecture Review Facilitator.'"
        )

    def test_dependency_list_present(self) -> None:
        text = _text(_COHORT_DESIGN)
        gate_section = _section_text(text, r"^#{1,4}\s+.*M16 Implementation Gate")
        assert gate_section is not None, "M16 Implementation Gate section must exist"
        has_named_dep = bool(re.search(
            r"ADR.017|Chief Methodologist|CM\s+must|no blocking|Architecture Review"
            r"|threshold calibration|no dependencies",
            gate_section,
            re.IGNORECASE,
        ))
        assert has_named_dep, (
            "M16 Implementation Gate section must contain at least one named dependency "
            "or an explicit 'no blocking dependencies' statement (AC-6). "
            "A section that lists no dependencies and does not explicitly confirm "
            "'no blocking' has not completed its gate function."
        )


# ============================================================================
# AC-7 — political-risk-summary: Zone Placement + Zone 1D conflict check
# ============================================================================


class TestAC7PoliticalRiskZonePlacement:
    """AC-7: political-risk-summary-design.md names the Zone for the political
    risk summary, checks conflict with Zone 1D, and explicitly states whether
    the display replaces, extends, or supplements Zone 1D."""

    def test_file_exists(self) -> None:
        assert _POLITICAL_RISK_DESIGN.exists(), (
            "docs/ux/design-thinking/political-risk-summary-design.md must exist. "
            "This is the primary G3 deliverable for issue #987."
        )

    def test_zone_placement_section_present(self) -> None:
        text = _text(_POLITICAL_RISK_DESIGN)
        assert re.search(
            r"^#{1,4}\s+.*Zone Placement",
            text,
            re.IGNORECASE | re.MULTILINE,
        ), (
            "political-risk-summary-design.md must contain a Zone Placement section "
            "naming which Zone hosts the political risk summary for Persona 3 (AC-7)."
        )

    def test_zone_1d_conflict_addressed(self) -> None:
        text = _text(_POLITICAL_RISK_DESIGN)
        assert re.search(r"Zone\s*1D", text, re.IGNORECASE), (
            "political-risk-summary-design.md must address the Zone 1D conflict check "
            "(AC-7). Zone 1D already displays the PSP composite — the placement decision "
            "must confirm whether the political risk summary replaces, extends, or "
            "supplements Zone 1D's existing display."
        )

    def test_zone_1d_relationship_explicit(self) -> None:
        text = _text(_POLITICAL_RISK_DESIGN)
        assert re.search(
            r"replac\w+|extend\w+|supplement\w+|in addition to|instead of"
            r"|Layer 3 enhancement|does not replace|separate from",
            text,
            re.IGNORECASE,
        ), (
            "political-risk-summary-design.md must explicitly state the relationship "
            "to Zone 1D: replaces, extends, supplements, or is a Layer 3 enhancement. "
            "AC-7 states: 'the document must explicitly state whether the political risk "
            "summary replaces, extends, or supplements Zone 1D's existing display — "
            "it may not leave this ambiguous.'"
        )

    def test_30_second_ceiling_referenced(self) -> None:
        text = _text(_POLITICAL_RISK_DESIGN)
        assert re.search(r"30.second|30\s*sec", text, re.IGNORECASE), (
            "political-risk-summary-design.md must reference the 30-second ceiling "
            "for Persona 3 in the Zone Placement rationale (AC-7, P-4). "
            "The zone selection must be justified against this cognitive time constraint."
        )


# ============================================================================
# AC-8 — political-risk-summary: Mode-specific display contract
# ============================================================================


class TestAC8ModeSpecificContract:
    """AC-8: political-risk-summary-design.md has separate Mode 1 (Replay) and
    Mode 2 (Simulation) sections with named indicators and update behaviour."""

    def test_mode_1_section_present(self) -> None:
        text = _text(_POLITICAL_RISK_DESIGN)
        assert re.search(
            r"Mode\s*1|Replay",
            text,
            re.IGNORECASE,
        ), (
            "political-risk-summary-design.md must contain a Mode 1 (Replay) section "
            "(AC-8). A unified display contract that does not distinguish Mode 1 "
            "from Mode 2 does not satisfy AC-8."
        )

    def test_mode_2_section_present(self) -> None:
        text = _text(_POLITICAL_RISK_DESIGN)
        assert re.search(
            r"Mode\s*2|Simulation",
            text,
            re.IGNORECASE,
        ), (
            "political-risk-summary-design.md must contain a Mode 2 (Simulation) "
            "section (AC-8). Step-advance update behaviour must be specified for Mode 2."
        )

    def test_psp_named_in_each_mode(self) -> None:
        text = _text(_POLITICAL_RISK_DESIGN)
        assert re.search(r"programme survival|PSP|program.{0,10}survival", text, re.IGNORECASE), (
            "political-risk-summary-design.md must name programme survival probability "
            "(PSP) as a displayed indicator (AC-8). "
            "PSP is the minimum required indicator per the intent document §4 AC-8."
        )

    def test_legitimacy_index_addressed(self) -> None:
        text = _text(_POLITICAL_RISK_DESIGN)
        _legitimacy_pat = (
            r"legitimacy index|legitimacy_index"
            r"|legitimacy.{0,20}(included|deferred|excluded|not included)"
        )
        assert re.search(_legitimacy_pat, text, re.IGNORECASE), (
            "political-risk-summary-design.md must address the legitimacy index (AC-8): "
            "included, deferred, or excluded — with rationale for each disposition. "
            "'Included' without rationale does not satisfy AC-8."
        )

    def test_step_advance_update_behaviour_stated(self) -> None:
        text = _text(_POLITICAL_RISK_DESIGN)
        assert re.search(
            r"(?:step advance|each step|step.{0,20}updat|updat.{0,20}step"
            r"|static|updat.{0,20}each)",
            text,
            re.IGNORECASE,
        ), (
            "political-risk-summary-design.md must specify update behaviour in "
            "Mode 2 — which elements update at each step advance and which are "
            "static (AC-8). A display specification that does not address this "
            "cannot be implemented without additional design decisions."
        )


# ============================================================================
# AC-9 — political-risk-summary: Literal sentence example
# ============================================================================


class TestAC9LiteralSentenceExample:
    """AC-9: political-risk-summary-design.md shows the exact plain-language
    sentence for ZMB ECF step 3, PSP≈0.38.

    Silent failure guard from intent doc §3.3:
    'The political risk surface will show PSP in plain language' FAILS.
    A literal example with ZMB + step 3 + 0.38 value PASSES.
    """

    def test_zmb_ecf_example_present(self) -> None:
        text = _text(_POLITICAL_RISK_DESIGN)
        assert re.search(r"\bZMB\b", text, re.IGNORECASE), (
            "political-risk-summary-design.md must include a ZMB ECF scenario "
            "example (AC-9). The literal example must be specific — not a template "
            "with placeholder variables."
        )

    def test_step_3_reference_in_example(self) -> None:
        text = _text(_POLITICAL_RISK_DESIGN)
        assert re.search(r"step\s*3", text, re.IGNORECASE), (
            "political-risk-summary-design.md must reference step 3 in the ZMB ECF "
            "example (AC-9). The intent document specifies: ZMB ECF programme at "
            "step 3, PSP≈0.38, legitimacy index≈0.42."
        )

    def test_psp_value_in_example(self) -> None:
        text = _text(_POLITICAL_RISK_DESIGN)
        # Accept 0.38, 38%, or "38 percent" as the PSP value
        assert re.search(r"0\.3[5-9]|3[5-9]\s*%|3[5-9]\s*percent", text, re.IGNORECASE), (
            "political-risk-summary-design.md must show the PSP value for the ZMB ECF "
            "step 3 example — approximately 0.38 or 38% (AC-9). "
            "A sentence template without a specific value does not satisfy AC-9."
        )

    def test_historical_analogue_sentence_present(self) -> None:
        text = _text(_POLITICAL_RISK_DESIGN)
        assert re.search(
            r"historical.{0,60}(abandon|programme|program|ECF|show)"
            r"|abandon.{0,60}within.{0,30}step"
            r"|historical analogue"
            r"|historical ECF",
            text,
            re.IGNORECASE,
        ), (
            "political-risk-summary-design.md must include a historical analogue "
            "sentence in the literal example (AC-9). "
            "The intent doc requires: 'At this level, historical ECF programmes show "
            "abandonment within 3 steps.' — a plain-language consequence statement, "
            "not just a severity badge."
        )

    def test_severity_label_in_example(self) -> None:
        text = _text(_POLITICAL_RISK_DESIGN)
        assert re.search(r"\bCRITICAL\b|\bWARNING\b|\bWATCH\b", text), (
            "political-risk-summary-design.md must include a severity label "
            "(CRITICAL, WARNING, or WATCH) in the literal example (AC-9). "
            "Persona 3 interprets severity through the badge — 'low probability' "
            "without a severity label requires domain knowledge to interpret."
        )


# ============================================================================
# AC-10 — political-risk-summary: 30-second legibility check
# ============================================================================


class TestAC10LegibilityCheck:
    """AC-10: political-risk-summary-design.md contains an explicit legibility
    confirmation naming at least one piece of jargon eliminated."""

    def test_legibility_check_section_present(self) -> None:
        text = _text(_POLITICAL_RISK_DESIGN)
        assert re.search(
            r"legibility|legible|30.second|readability|non.expert|no formal",
            text,
            re.IGNORECASE,
        ), (
            "political-risk-summary-design.md must contain an explicit legibility "
            "check confirming the display is readable by Persona 3 — a senior policy "
            "advisor with no formal economics training — within 30 seconds (AC-10)."
        )

    def test_jargon_elimination_named(self) -> None:
        text = _text(_POLITICAL_RISK_DESIGN)
        assert re.search(
            r"jargon|composite.{0,30}(removed|eliminated|translated|replaced)"
            r"|removed|eliminated|translated.{0,30}plain"
            r"|plain.language|no.{0,20}prior knowledge"
            r"|without.{0,30}(specialist|mediati|economics|training)",
            text,
            re.IGNORECASE,
        ), (
            "political-risk-summary-design.md must name at least one piece of "
            "jargon or composite score that was eliminated or translated into "
            "plain language (AC-10). "
            "A legibility check that only says 'readable by non-experts' without "
            "naming what was changed does not satisfy AC-10."
        )


# ============================================================================
# AC-11 — political-risk-summary: ADR disposition + M16 Implementation Gate
# ============================================================================


class TestAC11ADRDispositionAndGate:
    """AC-11: political-risk-summary-design.md explicitly answers whether a new
    ADR is required, and ends with a M16 Implementation Gate section addressing
    the #1084 PSP calibration dependency."""

    def test_adr_requirement_addressed(self) -> None:
        text = _text(_POLITICAL_RISK_DESIGN)
        # Must be one of two explicit dispositions
        new_adr = bool(re.search(
            r"new ADR.{0,60}required|ADR.{0,40}required|new ADR is required",
            text,
            re.IGNORECASE,
        ))
        no_new_adr = bool(re.search(
            r"no new ADR.{0,60}required|no ADR.{0,40}required"
            r"|ADR.{0,40}not required|does not require.{0,40}ADR",
            text,
            re.IGNORECASE,
        ))
        assert new_adr or no_new_adr, (
            "political-risk-summary-design.md must explicitly answer whether a "
            "new ADR is required for the political risk surface (AC-11). "
            "Issue #987 flags this as an open question. The design document must "
            "close it: either 'A new ADR is required' or 'No new ADR is required' "
            "with rationale."
        )

    def test_m16_gate_section_present(self) -> None:
        text = _text(_POLITICAL_RISK_DESIGN)
        assert re.search(
            r"^#{1,4}\s+.*M16 Implementation Gate",
            text,
            re.IGNORECASE | re.MULTILINE,
        ), (
            "political-risk-summary-design.md must contain a M16 Implementation Gate "
            "section (AC-11). The gate prevents M16 sprint entry from reopening the "
            "ADR question and the PSP calibration dependency."
        )

    def test_psp_calibration_dependency_addressed(self) -> None:
        text = _text(_POLITICAL_RISK_DESIGN)
        gate_section = _section_text(text, r"^#{1,4}\s+.*M16 Implementation Gate")
        assert gate_section is not None, "M16 Implementation Gate section must exist"
        assert re.search(
            r"#1084|PSP.{0,40}calibration|calibration.{0,40}PSP"
            r"|historical calibration|historical analogue.{0,40}calibration"
            r"|PSP historical",
            gate_section,
            re.IGNORECASE,
        ), (
            "M16 Implementation Gate in political-risk-summary-design.md must "
            "address the PSP historical calibration dependency (#1084, G5 scope) "
            "(AC-11). The plain-language historical analogue sentence in AC-9 "
            "depends on this calibration — the gate section must state whether "
            "#1084 must be complete before M16 sprint entry or not."
        )

    def test_no_see_above_in_gate(self) -> None:
        text = _text(_POLITICAL_RISK_DESIGN)
        gate_section = _section_text(text, r"^#{1,4}\s+.*M16 Implementation Gate")
        assert gate_section is not None, "M16 Implementation Gate section must exist"
        assert "see above" not in gate_section.lower(), (
            "M16 Implementation Gate section must list named dependencies — "
            "'see above' is not an acceptable entry (AC-11). "
            "Named examples: 'ADR number must be assigned from backlog', "
            "'#1084 PSP calibration must be complete before plain-language "
            "historical analogue can be implemented', or "
            "'No blocking dependencies beyond ADR requirement disposition above.'"
        )


# ============================================================================
# Cross-document: both design documents must be filed before M15 exit
# ============================================================================


class TestBothDocumentsRequired:
    """Both design documents must exist at M15 exit. The Architecture Review
    Facilitator confirmation (§7 of intent doc) requires both files to be present
    and satisfy their respective ACs. A partial delivery (one document without
    the other) does not satisfy the M15 G3 design gate."""

    def test_both_design_documents_exist(self) -> None:
        cohort_exists = _COHORT_DESIGN.exists()
        political_risk_exists = _POLITICAL_RISK_DESIGN.exists()
        assert cohort_exists and political_risk_exists, (
            "Both design documents must exist before the Architecture Review "
            "Facilitator confirmation can be given (§7 of G3 intent doc): "
            f"cohort-disaggregation-design.md exists={cohort_exists}, "
            f"political-risk-summary-design.md exists={political_risk_exists}. "
            "A partial delivery does not satisfy the M15 G3 design gate."
        )

    def test_cohort_design_not_empty(self) -> None:
        if not _COHORT_DESIGN.exists():
            pytest.skip("cohort-disaggregation-design.md not yet authored — Step 3 pending")
        text = _text(_COHORT_DESIGN)
        assert len(text.strip()) > 500, (
            "cohort-disaggregation-design.md must contain substantive content "
            "(>500 characters). A stub file does not satisfy the G3 design gate."
        )

    def test_political_risk_design_not_empty(self) -> None:
        if not _POLITICAL_RISK_DESIGN.exists():
            pytest.skip("political-risk-summary-design.md not yet authored — Step 3 pending")
        text = _text(_POLITICAL_RISK_DESIGN)
        assert len(text.strip()) > 500, (
            "political-risk-summary-design.md must contain substantive content "
            "(>500 characters). A stub file does not satisfy the G3 design gate."
        )
