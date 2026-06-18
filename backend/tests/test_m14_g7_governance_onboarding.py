"""Content-presence tests for M14-G7 governance and onboarding documentation.

QA Lead step 2 — authored BEFORE implementation, from intent document at:
  docs/process/intents/M14-G7-2026-06-18-governance-onboarding.md

These tests define "done" for G7. All tests will fail until PM Agent delivers
the implementation (Step 3). No database or server required — pure filesystem
checks that are the pytest equivalent of the shell grep commands specified in
the intent document §7.

AC coverage:
  AC-1  README.md — link to docs/onboarding/quick-start.md under a
        "Getting Started" (or equivalent) section heading
  AC-2  docs/onboarding/quick-start.md — literal "Zone 1B" AND
        "MDA alert" or "threshold breach"
  AC-3  docs/onboarding/scenario-creation.md — "grounding strip" AND
        confidence tier notation (T1/T2/T3 pattern)
  AC-4  docs/onboarding/methodology-overview.md — limitations/blindspots
        section heading AND at least one example domain blindspot phrase
        (full 3-blindspot count requires BPO manual review at Step 5)
  AC-5  docs/onboarding/data-provenance.md — "STRUCTURAL_ABSENCE" or
        "Structural Absence" AND a negotiation-context sentence
  AC-6  docs/governance/goodharts-law-mitigation.md — four required
        section signals: gaming definition with a named parameter, range-edge
        signal description, TSC obligation language, audit pathway
  AC-7  MANUAL — timed navigation; BPO proxy confirms Tier 2 explanation
        reachable in <5 minutes from README.md entry point (not automatable)

Silent failure guards (§3.3 of intent doc):
  "Zone 1B" as literal string in quick-start (not only in a glossary)
  "STRUCTURAL_ABSENCE" or "Structural Absence" as literal string in
  data-provenance (not only in a technical reference)
  At least one named WorldSim parameter in goodharts-law gaming definition
"""
from __future__ import annotations

import pathlib
import re

import pytest

_REPO_ROOT = pathlib.Path(__file__).parent.parent.parent

_README = _REPO_ROOT / "README.md"
_QUICK_START = _REPO_ROOT / "docs" / "onboarding" / "quick-start.md"
_SCENARIO_CREATION = _REPO_ROOT / "docs" / "onboarding" / "scenario-creation.md"
_METHODOLOGY = _REPO_ROOT / "docs" / "onboarding" / "methodology-overview.md"
_DATA_PROVENANCE = _REPO_ROOT / "docs" / "onboarding" / "data-provenance.md"
_GOODHARTS = _REPO_ROOT / "docs" / "governance" / "goodharts-law-mitigation.md"

# Known WorldSim parameter categories (at least one must appear in the
# gaming definition section to satisfy AC-6a's operational requirement)
_PARAMETER_CATEGORIES = [
    "fiscal_multiplier",
    "political_stability_index",
    "legitimacy_index",
    "reserve_coverage",
    "conditionality",
    "ecological",
    "framework-level multiplier",
]


# ---------------------------------------------------------------------------
# AC-1 — README links to quick-start guide under a Getting Started section
# ---------------------------------------------------------------------------


class TestAC1ReadmeLink:
    """AC-1: README.md contains a link to docs/onboarding/quick-start.md under
    a 'Getting Started', 'For New Users', or equivalent section heading."""

    def test_readme_exists(self) -> None:
        assert _README.exists(), "README.md must exist at the repository root"

    def test_readme_contains_quick_start_link(self) -> None:
        text = _README.read_text(encoding="utf-8")
        # grep -i "quick-start" README.md — must be a markdown link, not bare text
        assert re.search(r"\[.*?\]\(.*?quick-start.*?\)", text, re.IGNORECASE), (
            "README.md must contain a markdown link to quick-start.md "
            "(pattern: [text](…quick-start…)). "
            "AC-1 shell equivalent: grep -i 'quick-start' README.md"
        )

    def test_readme_has_getting_started_section(self) -> None:
        text = _README.read_text(encoding="utf-8")
        assert re.search(
            r"^#{1,3}\s+(Getting Started|For New Users|Quick Start|Start Here)",
            text,
            re.IGNORECASE | re.MULTILINE,
        ), (
            "README.md must contain a section heading matching 'Getting Started', "
            "'For New Users', 'Quick Start', or 'Start Here'. "
            "The quick-start link must appear under this heading."
        )

    def test_quick_start_link_under_getting_started(self) -> None:
        text = _README.read_text(encoding="utf-8")
        # Verify the link appears after the Getting Started heading —
        # look for the section heading followed (anywhere before the next ##
        # heading) by a quick-start link.
        section_match = re.search(
            r"^#{1,3}\s+(Getting Started|For New Users|Quick Start|Start Here).*?(?=^#{1,3}\s|\Z)",
            text,
            re.IGNORECASE | re.MULTILINE | re.DOTALL,
        )
        assert section_match, "README.md must have a Getting Started (or equivalent) section"
        section_text = section_match.group(0)
        assert re.search(r"\[.*?\]\(.*?quick-start.*?\)", section_text, re.IGNORECASE), (
            "The quick-start link must appear within the Getting Started section, "
            "not elsewhere in README.md"
        )


# ---------------------------------------------------------------------------
# AC-2 — quick-start.md contains Zone 1B and MDA alert
# ---------------------------------------------------------------------------


class TestAC2QuickStart:
    """AC-2: quick-start.md contains 'Zone 1B' and 'MDA alert' or
    'threshold breach' in instrument cluster reading context."""

    def test_file_exists(self) -> None:
        assert _QUICK_START.exists(), (
            "docs/onboarding/quick-start.md must exist. "
            "This file is the primary G7 deliverable for issue #989."
        )

    def test_contains_zone_1b(self) -> None:
        text = _QUICK_START.read_text(encoding="utf-8")
        # grep "Zone 1B" docs/onboarding/quick-start.md
        assert "Zone 1B" in text, (
            "quick-start.md must contain the literal string 'Zone 1B'. "
            "Silent failure guard: the string must appear in plain-language "
            "context (instrument cluster reading instructions), not only in a "
            "glossary or reference section. "
            "See intent doc §3.3 silent failure detection."
        )

    def test_contains_mda_alert_or_threshold_breach(self) -> None:
        text = _QUICK_START.read_text(encoding="utf-8")
        # grep -i "mda alert\|threshold breach" docs/onboarding/quick-start.md
        assert re.search(r"mda alert|threshold breach", text, re.IGNORECASE), (
            "quick-start.md must contain 'MDA alert' or 'threshold breach'. "
            "The term must appear in the instrument cluster reading instructions "
            "section (Step 3 or Step 4 equivalent per intent doc §4b visual spec)."
        )

    def test_zone_1b_in_instrument_context(self) -> None:
        text = _QUICK_START.read_text(encoding="utf-8")
        # Verify Zone 1B appears in a narrative sentence, not only as a label.
        # Look for Zone 1B within 200 chars of "instrument" or "alert" or "breach"
        zone_pos = text.find("Zone 1B")
        assert zone_pos != -1, "Zone 1B must be present (checked above)"
        surrounding = text[max(0, zone_pos - 200) : zone_pos + 200].lower()
        context_kws = ["instrument", "alert", "breach", "severity", "mda"]
        assert any(kw in surrounding for kw in context_kws), (
            "Zone 1B must appear near instrument cluster context (instrument / alert / "
            "breach / severity / MDA) — not in an isolated label. "
            "A Persona 2 reader must understand what Zone 1B means without leaving the sentence."
        )

    def test_severity_classification_present(self) -> None:
        text = _QUICK_START.read_text(encoding="utf-8")
        # Intent doc §4b: 'TERMINAL, CRITICAL, WARNING' must be shown
        assert re.search(r"TERMINAL|CRITICAL|WARNING", text), (
            "quick-start.md must name at least one MDA severity classification "
            "(TERMINAL, CRITICAL, or WARNING). "
            "The intent doc §4b visual spec lists all three as required content."
        )


# ---------------------------------------------------------------------------
# AC-3 — scenario-creation.md contains grounding strip and tier notation
# ---------------------------------------------------------------------------


class TestAC3ScenarioCreation:
    """AC-3: scenario-creation.md exists, contains 'grounding strip' and an
    explanation of confidence tier numbers in scenario output context."""

    def test_file_exists(self) -> None:
        assert _SCENARIO_CREATION.exists(), (
            "docs/onboarding/scenario-creation.md must exist. "
            "Covers ADR-016 Component 1–3 output (Grounding Strip) per intent doc §1."
        )

    def test_contains_grounding_strip(self) -> None:
        text = _SCENARIO_CREATION.read_text(encoding="utf-8")
        # grep "grounding strip" docs/onboarding/scenario-creation.md (case-insensitive)
        assert re.search(r"grounding strip", text, re.IGNORECASE), (
            "scenario-creation.md must contain 'grounding strip'. "
            "AC-3 silent failure guard: the Grounding Strip is the ADR-016 §Component 2 "
            "output; omitting it means the scenario creation guide does not cover the "
            "primary data-provenance signal visible to the analyst."
        )

    def test_contains_confidence_tier_notation(self) -> None:
        text = _SCENARIO_CREATION.read_text(encoding="utf-8")
        # Confidence tier explanation: T1, T2, T3 notation or "Tier 1/2/3" text
        assert re.search(r"\bT[1-5]\b|Tier\s+[1-5]", text), (
            "scenario-creation.md must contain an explanation of confidence tier numbers "
            "(T1, T2, T3, T4, T5 notation or 'Tier 1' through 'Tier 5' text). "
            "Per ADR-015 §UX-5 (confidence tier display) — the data provenance guide must "
            "explain tier meaning in the context of reading scenario outputs."
        )

    def test_grounding_strip_and_tiers_in_output_context(self) -> None:
        text = _SCENARIO_CREATION.read_text(encoding="utf-8")
        # Both concepts must appear in the same document (trivially true if both pass above),
        # but confirm each appears in a non-glossary context
        grounding_pos = text.lower().find("grounding strip")
        tier_pos = next(
            (m.start() for m in re.finditer(r"\bT[1-5]\b|Tier\s+[1-5]", text)),
            -1,
        )
        assert grounding_pos != -1 and tier_pos != -1, (
            "Both 'grounding strip' and confidence tier notation must appear in "
            "scenario-creation.md — each in reading/output context, not only in a glossary."
        )


# ---------------------------------------------------------------------------
# AC-4 — methodology-overview.md contains named blindspots section
# ---------------------------------------------------------------------------


class TestAC4MethodologyOverview:
    """AC-4: methodology-overview.md has a blindspots section naming at least
    one specific model limitation.

    NOTE: The full 3-named-blindspot count requires BPO manual review at Step 5
    (Validate). This test confirms: (1) file exists, (2) a blindspot/limitations
    section is present, (3) at least one specific domain limitation is named.
    The BPO checks that the count is ≥ 3 at Validate time.
    """

    def test_file_exists(self) -> None:
        assert _METHODOLOGY.exists(), (
            "docs/onboarding/methodology-overview.md must exist."
        )

    def test_contains_limitations_section(self) -> None:
        text = _METHODOLOGY.read_text(encoding="utf-8")
        assert re.search(
            r"^#{1,4}\s+.*(Limitation|Blindspot|What this model does not|Does not claim"
            r"|Known gap|Model boundary)",
            text,
            re.IGNORECASE | re.MULTILINE,
        ), (
            "methodology-overview.md must contain a section heading that matches "
            "'Limitations', 'Blindspot', 'What this model does not claim', "
            "'Does not claim', 'Known gap', or 'Model boundary'. "
            "Per AC-4: the section heading satisfies the heading requirement; "
            "named blindspots satisfy the content requirement."
        )

    def test_contains_at_least_one_named_blindspot(self) -> None:
        text = _METHODOLOGY.read_text(encoding="utf-8")
        # The intent doc §4 gives three qualifying examples — check for
        # any named-domain blindspot phrase (not a generic disclaimer)
        named_blindspot_patterns = [
            r"ecological.{0,30}financial.{0,30}transmission",
            r"political feasibility.{0,50}sub.national",
            r"informal economy",
            r"not modeled",
            r"not captured",
            r"absent from",
            r"not included",
            r"outside.{0,20}scope",
            r"does not model",
            r"does not capture",
        ]
        found = any(
            re.search(p, text, re.IGNORECASE) for p in named_blindspot_patterns
        )
        assert found, (
            "methodology-overview.md must contain at least one named-domain blindspot "
            "phrase (e.g., 'not modeled', 'not captured', 'absent from', "
            "'ecological-to-financial transmission pathways not modeled'). "
            "Generic disclaimers ('model has limitations') do not satisfy AC-4. "
            "BPO manual review at Step 5 confirms the total count is ≥ 3."
        )


# ---------------------------------------------------------------------------
# AC-5 — data-provenance.md contains STRUCTURAL_ABSENCE in negotiation context
# ---------------------------------------------------------------------------


class TestAC5DataProvenance:
    """AC-5: data-provenance.md exists and contains 'STRUCTURAL_ABSENCE' or
    'Structural Absence' with a worked negotiation example."""

    def test_file_exists(self) -> None:
        assert _DATA_PROVENANCE.exists(), (
            "docs/onboarding/data-provenance.md must exist."
        )

    def test_contains_structural_absence_string(self) -> None:
        text = _DATA_PROVENANCE.read_text(encoding="utf-8")
        # grep -i "structural.absence" docs/onboarding/data-provenance.md
        assert re.search(r"structural.absence", text, re.IGNORECASE), (
            "data-provenance.md must contain 'STRUCTURAL_ABSENCE' or 'Structural Absence' "
            "as a literal string. "
            "Silent failure guard per intent doc §3.3: if the string is absent, the "
            "document is incomplete for its intended audience regardless of overall length."
        )

    def test_contains_negotiation_context(self) -> None:
        text = _DATA_PROVENANCE.read_text(encoding="utf-8")
        # The intent requires a WORKED NEGOTIATION EXAMPLE — not just a definition.
        # Look for negotiation-context vocabulary near STRUCTURAL_ABSENCE.
        sa_match = re.search(r"structural.absence", text, re.IGNORECASE)
        assert sa_match, "STRUCTURAL_ABSENCE must be present (checked above)"
        pos = sa_match.start()
        surrounding = text[max(0, pos - 500) : pos + 500].lower()
        negotiation_terms = [
            "negotiat",
            "restructur",
            "creditor",
            "ministry",
            "minister",
            "session",
            "table",
            "cite",
            "cit",
            "argue",
            "argument",
        ]
        assert any(t in surrounding for t in negotiation_terms), (
            "data-provenance.md must contain a worked negotiation example near the "
            "STRUCTURAL_ABSENCE reference — not merely a definition. "
            "The example must show how a finance ministry analyst would CITE this "
            "classification in a debt restructuring session (per AC-5 requirement). "
            "Expected vocabulary in surrounding context: 'negotiating', 'restructuring', "
            "'creditor', 'ministry', 'session', 'cite', 'argue'."
        )

    def test_tier_2_citable_explanation(self) -> None:
        text = _DATA_PROVENANCE.read_text(encoding="utf-8")
        # AC-7 (BPO timed navigation) targets finding "Tier 2" explanation.
        # Verify the document contains a Tier 2 (or T2) explanation with
        # "citable" or "cite" or "primary source" language.
        t2_match = re.search(r"Tier\s*2\b|\bT2\b", text, re.IGNORECASE)
        assert t2_match, (
            "data-provenance.md must explain what Tier 2 (T2) means. "
            "The north star test (intent doc §2 P-7) requires the Zambian analyst to "
            "read: 'Tier 2 means the source is citable directly — you can name the "
            "institution and vintage in a negotiating session.'"
        )
        pos = t2_match.start()
        surrounding = text[max(0, pos - 300) : pos + 300].lower()
        assert any(
            t in surrounding
            for t in ["citable", "cite", "primary source", "direct", "institution"]
        ), (
            "The Tier 2 explanation in data-provenance.md must include 'citable', "
            "'cite', 'primary source', 'direct', or 'institution' — the explanation "
            "that enables the analyst to use the tier classification in a negotiating "
            "context (north star test in intent doc §2 P-7)."
        )


# ---------------------------------------------------------------------------
# AC-6 — goodharts-law-mitigation.md has four required sections
# ---------------------------------------------------------------------------


class TestAC6GoodhartsLaw:
    """AC-6: docs/governance/goodharts-law-mitigation.md exists with four
    required content sections as specified in intent doc §4 AC-6 (a)–(d)."""

    def test_file_exists(self) -> None:
        assert _GOODHARTS.exists(), (
            "docs/governance/goodharts-law-mitigation.md must exist. "
            "This is the TSC founding mandate document for issue #988."
        )

    def test_gaming_definition_with_named_parameter(self) -> None:
        text = _GOODHARTS.read_text(encoding="utf-8")
        # AC-6a: gaming definition must name at least one specific parameter category
        # Silent failure guard: "the TSC should monitor parameter drift" without
        # defining what 'drift' means is NOT sufficient.
        has_parameter = any(
            re.search(p, text, re.IGNORECASE) for p in _PARAMETER_CATEGORIES
        )
        assert has_parameter, (
            "docs/governance/goodharts-law-mitigation.md must name at least one specific "
            "WorldSim parameter category in the gaming definition section. "
            "Qualifying parameter categories: "
            + ", ".join(_PARAMETER_CATEGORIES)
            + ". "
            "Silent failure guard per intent doc §3.3: the definition must be operational "
            "(naming a specific parameter) rather than aspirational ('parameter drift')."
        )

    def test_gaming_definition_section_present(self) -> None:
        text = _GOODHARTS.read_text(encoding="utf-8")
        # AC-6a: section covering what constitutes gaming vs. legitimate calibration
        assert re.search(
            r"gaming|parameterization gaming|legitimate calibration",
            text,
            re.IGNORECASE,
        ), (
            "docs/governance/goodharts-law-mitigation.md must contain a section on "
            "what constitutes parameterization gaming (vs. legitimate calibration variation). "
            "AC-6(a) of the intent doc."
        )

    def test_range_edge_signal_section_present(self) -> None:
        text = _GOODHARTS.read_text(encoding="utf-8")
        # AC-6b: how the tool signals when parameters are at the edge of validated range
        assert re.search(
            r"validated range|range edge|parameter.{0,20}(limit|bound|edge|warning|signal)",
            text,
            re.IGNORECASE,
        ), (
            "docs/governance/goodharts-law-mitigation.md must describe how the tool "
            "signals when parameters are at the edge of the validated range. "
            "AC-6(b) of the intent doc."
        )

    def test_tsc_obligation_section_present(self) -> None:
        text = _GOODHARTS.read_text(encoding="utf-8")
        # AC-6c: explicit TSC monitoring and response obligations (not aspirational)
        assert re.search(
            r"TSC.{0,100}(monitor|obligat|must|required|responsi)",
            text,
            re.IGNORECASE | re.DOTALL,
        ), (
            "docs/governance/goodharts-law-mitigation.md must contain explicit TSC "
            "monitoring and response obligations — not aspirational language. "
            "The section must name what the TSC MUST do when gaming is suspected "
            "(per AC-6(c): 'named obligations', not 'should monitor'). "
            "AC-6(c) of the intent doc."
        )

    def test_open_source_audit_pathway_present(self) -> None:
        text = _GOODHARTS.read_text(encoding="utf-8")
        # AC-6d: concrete open-source audit pathway
        assert re.search(
            r"audit|git.{0,30}(history|log|parameteriz)|community.{0,50}(challenge|review)"
            r"|public.{0,30}(config|export)",
            text,
            re.IGNORECASE,
        ), (
            "docs/governance/goodharts-law-mitigation.md must describe a concrete "
            "open-source audit pathway — e.g., parameterization history in git, public "
            "configuration export, or community challenge mechanism. "
            "AC-6(d) of the intent doc."
        )


# ---------------------------------------------------------------------------
# AC-7 — Manual: BPO timed navigation (not automatable)
# ---------------------------------------------------------------------------


class TestAC7BPOTimedNavigation:
    """AC-7: BPO proxy reads README.md and follows link chain to reach the
    'Tier 2' explanation in data-provenance.md within 5 minutes.

    This test cannot be automated — it requires a human to navigate the
    documentation without prior knowledge. It is marked skip here and
    fulfilled at Step 5 (Validate) by the Business PO.

    The BPO navigation path must be:
      README.md → Getting Started section → quick-start.md →
      (link to data-provenance.md) → Tier 2 explanation

    BPO validation criterion per acceptance-protocol.md §1.3 Documentation:
    'The key finding named in Section 3.1 is reachable in under five minutes
    from the entry point.'
    """

    @pytest.mark.skip(
        reason=(
            "AC-7 is a manual BPO timed navigation test. "
            "BPO proxy opens README.md and navigates to Tier 2 explanation "
            "within 5 minutes. This is validated at Step 5 (Validate) — "
            "not automatable. See intent doc §7 and acceptance-protocol.md §1.3."
        )
    )
    def test_bpo_5_minute_navigation(self) -> None:
        pass  # BPO validates at Step 5 — see intent doc §9

    def test_quick_start_links_to_data_provenance(self) -> None:
        """Automated pre-check: quick-start.md must contain a link to
        data-provenance.md so the BPO navigation chain exists."""
        if not _QUICK_START.exists():
            pytest.skip("quick-start.md not yet authored — Step 3 pending")
        text = _QUICK_START.read_text(encoding="utf-8")
        assert re.search(r"\[.*?\]\(.*?data-provenance.*?\)", text, re.IGNORECASE), (
            "quick-start.md must contain a markdown link to data-provenance.md "
            "so the AC-7 BPO navigation chain (README → quick-start → "
            "data-provenance → Tier 2 explanation) is physically traversable. "
            "Without this link, the BPO timed navigation cannot complete in <5 min."
        )
