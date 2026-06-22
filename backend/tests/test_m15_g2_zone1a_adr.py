"""Content-presence tests for M15-G2 Zone 1A Information Architecture ADR.

QA Lead step 2 — authored from intent document at:
  docs/process/intents/M15-G2-2026-06-21-zone-1a-adr.md

G2 is an architecture/design sprint with two primary deliverables:
  Phase 2: docs/architecture/reviews/ARCH-REVIEW-007-milestone15.md
  Phase 3: docs/adr/ADR-017-zone-1a-information-architecture.md

All 11 tests fail until the Architect Agent completes Phases 2 and 3. No
database, server, or simulation engine required — pure filesystem checks.
The observable application state is the state of filed documents at their
canonical paths, verifiable by grep and file reads (intent doc §3).

AC coverage (intent doc §4, AC-1 through AC-11):
  AC-1   ARCH-REVIEW-007-milestone15.md exists at docs/architecture/reviews/
  AC-2   ARCH-REVIEW-007 addresses Zone 1A's primary question in each mode
         (Mode 1, Mode 2, and Mode 3 each named in a primary-question context)
  AC-3   ARCH-REVIEW-007 names encoding channels per mode — at least 3 of:
         X-axis, Y-axis, color, opacity, line style, endpoint label
  AC-4   ARCH-REVIEW-007 states specific numeric N-entity and M-branch limits
         — N<=\\d or N=\\d appears at least twice (intent doc AC-4 pattern)
  AC-5   ARCH-REVIEW-007 records binding decisions on all four Phase 1 open
         questions: Mode 3 single-entity encoding choice, multi-entity
         COMPARE_VIEW, composite aggregation rule, endpoint label collision
  AC-6   docs/architecture/backlog.md ARCH-011 row contains
         'ASSIGNED — ADR-017' (not 'PENDING_NUMBER')
  AC-7   docs/adr/ADR-017-zone-1a-information-architecture.md exists
  AC-8   ADR-017 contains required structural content: 'tier:' (frontmatter or
         tier field), 'Persona and UX Traceability', 'UX Implication',
         'Silent Failure Mode', 'North Star Test', 'Mission Impact', and a
         fenced code block containing 'mermaid' (mandatory diagram)
  AC-9   ADR-017 UX Designer sign-off has all four NM-042 fields:
         'Reviewing agent:', 'Session context:', 'Governing documents
         reviewed:', 'Concerns found:'
  AC-10  ADR-017 UX Designer Session context field contains one of the two
         valid NM-042 values (not blank or placeholder)
  AC-11  ADR-017 UX Designer sign-off block contains ≥2 § section citations
         in the Governing documents reviewed field (not generic references)

Silent failure guards (intent doc §3.3):
  AC-5: an ARCH-REVIEW that restates the four open questions without making
        binding decisions has not resolved them. Detection: each question
        pattern must appear in a non-question sentence (not ending in '?').
  AC-10: a Session context field with placeholder '[...]' or blank value is
         non-compliant per NM-042 and CLAUDE.md §UX Designer sign-off.
  AC-11: § count is checked only within the sign-off block (from 'Governing
         documents reviewed:' to the next field or end of sign-off) to avoid
         false positives from § symbols elsewhere in the document.
"""
from __future__ import annotations

import pathlib
import re

import pytest

_REPO_ROOT = pathlib.Path(__file__).parent.parent.parent

_ARCH_REVIEW = (
    _REPO_ROOT
    / "docs"
    / "architecture"
    / "reviews"
    / "ARCH-REVIEW-007-milestone15.md"
)

_ADR_017 = (
    _REPO_ROOT / "docs" / "adr" / "ADR-017-zone-1a-information-architecture.md"
)

_BACKLOG = _REPO_ROOT / "docs" / "architecture" / "backlog.md"

# Encoding channel names from the design thinking doc §Encoding Under Pressure.
# AC-3 requires ≥ 3 of these 6 to appear in ARCH-REVIEW-007.
_ENCODING_CHANNELS = ["X-axis", "Y-axis", "color", "opacity", "line style", "endpoint label"]


# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------


def _text(path: pathlib.Path) -> str:
    return path.read_text(encoding="utf-8")


def _sign_off_block(text: str) -> str:
    """Return just the UX Designer sign-off block from ADR-017.

    Extracts from 'Governing documents reviewed:' to the next '**' field
    label or end of file. Used for AC-11 § counting to avoid false positives
    from § symbols elsewhere in the document (intent doc §3.3).
    """
    gd_start = text.find("**Governing documents reviewed:**")
    if gd_start == -1:
        return ""
    # Find the next '**' bold marker that begins a new field (Concerns found)
    next_field = text.find("**Concerns found:**", gd_start)
    if next_field != -1:
        return text[gd_start:next_field]
    return text[gd_start : gd_start + 800]


# ===========================================================================
# AC-1 — ARCH-REVIEW-007 exists
# ===========================================================================


class TestAC1ArchReviewExists:
    """AC-1: ARCH-REVIEW-007-milestone15.md exists at docs/architecture/reviews/.

    Canonical location verified by pattern of ARCH-REVIEW-001 through
    ARCH-REVIEW-006 (CLAUDE.md §Canonical Artifact Locations — Architecture
    Reviews row). Intent doc §4 AC-1.
    """

    def test_file_exists(self) -> None:
        assert _ARCH_REVIEW.exists(), (
            "docs/architecture/reviews/ARCH-REVIEW-007-milestone15.md must exist. "
            "This is the Phase 2 deliverable for M15-G2 (#845 Phase 2). "
            "Intent doc §4 AC-1: os.path.isfile('docs/architecture/reviews/"
            "ARCH-REVIEW-007-milestone15.md')."
        )

    def test_file_not_empty(self) -> None:
        if not _ARCH_REVIEW.exists():
            pytest.skip("ARCH-REVIEW-007-milestone15.md not yet authored — Step 3 pending")
        text = _text(_ARCH_REVIEW)
        assert len(text.strip()) > 500, (
            "ARCH-REVIEW-007-milestone15.md must contain substantive content "
            "(>500 characters). A stub does not satisfy the Phase 2 observable state "
            "(intent doc §3.1). AC-1."
        )


# ===========================================================================
# AC-2 — ARCH-REVIEW-007 addresses primary question per mode
# ===========================================================================


class TestAC2PrimaryQuestionPerMode:
    """AC-2: ARCH-REVIEW-007 contains text addressing Mode 1, Mode 2, and Mode 3
    zone primary questions.

    Intent doc §4 AC-2: file content contains 'Mode 1', 'Mode 2', and 'Mode 3'
    each at least once in the context of the zone primary question or equivalent.

    Q1 primary questions from design thinking doc §Phase 2 Readiness:
      Mode 1: threshold crossing — which framework crossed first?
      Mode 2: step advance — does any framework project a crossing?
      Mode 3: control input — did it move toward or away from threshold?
    """

    def test_mode_1_threshold_question(self) -> None:
        if not _ARCH_REVIEW.exists():
            pytest.skip("ARCH-REVIEW-007-milestone15.md not yet authored — Step 3 pending")
        text = _text(_ARCH_REVIEW)
        assert re.search(r"Mode\s*1|Replay", text, re.IGNORECASE), (
            "ARCH-REVIEW-007 must reference 'Mode 1' in Q1 coverage. AC-2."
        )
        assert re.search(
            r"threshold crossing|MDA.{0,30}(crossing|floor)|which framework",
            text,
            re.IGNORECASE,
        ), (
            "ARCH-REVIEW-007 must address Mode 1's primary question — threshold "
            "crossing and which framework crossed first. AC-2 (intent doc §4 AC-2)."
        )

    def test_mode_2_step_advance_question(self) -> None:
        if not _ARCH_REVIEW.exists():
            pytest.skip("ARCH-REVIEW-007-milestone15.md not yet authored — Step 3 pending")
        text = _text(_ARCH_REVIEW)
        assert re.search(r"Mode\s*2|Simulation", text, re.IGNORECASE), (
            "ARCH-REVIEW-007 must reference 'Mode 2' in Q1 coverage. AC-2."
        )
        assert re.search(
            r"step advance|remaining steps?|project.{0,30}(crossing|floor)"
            r"|threshold.safe",
            text,
            re.IGNORECASE,
        ), (
            "ARCH-REVIEW-007 must address Mode 2's primary question — step advance "
            "and projected crossing in remaining steps. AC-2."
        )

    def test_mode_3_control_input_question(self) -> None:
        if not _ARCH_REVIEW.exists():
            pytest.skip("ARCH-REVIEW-007-milestone15.md not yet authored — Step 3 pending")
        text = _text(_ARCH_REVIEW)
        assert re.search(r"Mode\s*3|Active Control", text, re.IGNORECASE), (
            "ARCH-REVIEW-007 must reference 'Mode 3' in Q1 coverage. AC-2."
        )
        assert re.search(
            r"control input|toward.{0,30}(floor|threshold)|away.{0,30}(floor|threshold)"
            r"|relative to.{0,30}baseline",
            text,
            re.IGNORECASE,
        ), (
            "ARCH-REVIEW-007 must address Mode 3's primary question — whether the "
            "control input moved the trajectory toward or away from the threshold "
            "relative to baseline. AC-2."
        )

    def test_all_three_modes_present(self) -> None:
        if not _ARCH_REVIEW.exists():
            pytest.skip("ARCH-REVIEW-007-milestone15.md not yet authored — Step 3 pending")
        text = _text(_ARCH_REVIEW)
        m1 = bool(re.search(r"Mode\s*1|Replay", text, re.IGNORECASE))
        m2 = bool(re.search(r"Mode\s*2|Simulation", text, re.IGNORECASE))
        m3 = bool(re.search(r"Mode\s*3|Active Control", text, re.IGNORECASE))
        assert m1 and m2 and m3, (
            "ARCH-REVIEW-007 must address all three modes in Q1 coverage. "
            f"Found: Mode 1={m1}, Mode 2={m2}, Mode 3={m3}. AC-2."
        )


# ===========================================================================
# AC-3 — ARCH-REVIEW-007 names encoding channels (≥3 of 6)
# ===========================================================================


class TestAC3EncodingChannels:
    """AC-3: ARCH-REVIEW-007 names the encoding channels used per mode —
    at least 3 of: X-axis, Y-axis, color, opacity, line style, endpoint label.

    Intent doc §4 AC-3: 'file contains at least three of the following strings:
    "X-axis", "Y-axis", "color", "opacity", "line style", "endpoint label".
    Pytest: intersection count ≥ 3.'

    These are the six channels from design thinking doc §Combinatorial Tension
    §Encoding Under Pressure table.
    """

    def test_at_least_three_channels_named(self) -> None:
        if not _ARCH_REVIEW.exists():
            pytest.skip("ARCH-REVIEW-007-milestone15.md not yet authored — Step 3 pending")
        text = _text(_ARCH_REVIEW)
        found = [ch for ch in _ENCODING_CHANNELS if ch.lower() in text.lower()]
        assert len(found) >= 3, (
            "ARCH-REVIEW-007 must name at least 3 of the 6 encoding channels to "
            "satisfy Q2 of the Phase 2 readiness gate. "
            f"Channels found ({len(found)}/6): {found}. "
            "Full channel list (from design thinking doc §Encoding Under Pressure): "
            f"{_ENCODING_CHANNELS}. "
            "Intent doc §4 AC-3: intersection count ≥ 3."
        )

    def test_color_for_framework_named(self) -> None:
        if not _ARCH_REVIEW.exists():
            pytest.skip("ARCH-REVIEW-007-milestone15.md not yet authored — Step 3 pending")
        text = _text(_ARCH_REVIEW)
        assert re.search(
            r"color.{0,30}framework|framework.{0,30}color"
            r"|color.{0,30}(financial|HD|ecological|governance)",
            text,
            re.IGNORECASE,
        ), (
            "ARCH-REVIEW-007 must name the color channel as the encoding for "
            "framework identity (financial, HD, ecological, governance). "
            "This is the primary encoding channel — absence suggests Q2 was not "
            "fully addressed. AC-3."
        )

    def test_opacity_for_branch_named(self) -> None:
        if not _ARCH_REVIEW.exists():
            pytest.skip("ARCH-REVIEW-007-milestone15.md not yet authored — Step 3 pending")
        text = _text(_ARCH_REVIEW)
        assert re.search(
            r"opacity|ghost.{0,20}(curve|line)|50%.opacity|baseline.ghost",
            text,
            re.IGNORECASE,
        ), (
            "ARCH-REVIEW-007 must name opacity as the branch identity channel "
            "(active solid vs. baseline ghost). AC-3."
        )


# ===========================================================================
# AC-4 — ARCH-REVIEW-007 states numeric N/M limits
# ===========================================================================


class TestAC4NMLimits:
    """AC-4: ARCH-REVIEW-007 states specific numeric N-entity and M-branch limits.

    Intent doc §4 AC-4: 'file contains numeric limit statements — at minimum,
    strings matching N≤\\d or N=\\d or N > \\d appear at least twice
    (one per mode group). Pytest: re.findall(r"N[≤<=]\\d", content) count ≥ 2.'

    Design thinking doc §Phase 2 Readiness Q3 table establishes N≤4 in Mode 3
    as the binding constraint — the review must state these limits explicitly.
    """

    def test_n_limit_appears_at_least_twice(self) -> None:
        if not _ARCH_REVIEW.exists():
            pytest.skip("ARCH-REVIEW-007-milestone15.md not yet authored — Step 3 pending")
        text = _text(_ARCH_REVIEW)
        matches = re.findall(r"N[≤<=]\d|N\s*[≤<=]\s*\d|N\s*>\s*\d|\bN=\d", text)
        assert len(matches) >= 2, (
            "ARCH-REVIEW-007 must contain at least 2 numeric N-entity limit "
            f"statements. Found {len(matches)}: {matches!r}. "
            "Intent doc §4 AC-4: re.findall(r'N[≤<=]\\d', content) count ≥ 2. "
            "Design thinking doc §Phase 2 Readiness Q3 table requires per-mode limits."
        )

    def test_m_limit_addressed(self) -> None:
        if not _ARCH_REVIEW.exists():
            pytest.skip("ARCH-REVIEW-007-milestone15.md not yet authored — Step 3 pending")
        text = _text(_ARCH_REVIEW)
        assert re.search(
            r"\bM\s*[=≤]\s*\d|\bM=1|\d+\s*branch|branch.{0,20}limit"
            r"|baseline.{0,20}active|COMPARE.VIEW",
            text,
            re.IGNORECASE,
        ), (
            "ARCH-REVIEW-007 must address M (branch) limits for Zone 1A "
            "(e.g., M=1 baseline+active, COMPARE_VIEW for M>1). "
            "Q3 requires both N and M limits per mode. AC-4."
        )

    def test_breaking_point_identified(self) -> None:
        if not _ARCH_REVIEW.exists():
            pytest.skip("ARCH-REVIEW-007-milestone15.md not yet authored — Step 3 pending")
        text = _text(_ARCH_REVIEW)
        assert re.search(
            r"breaking point|legibility break|15.second.ceiling"
            r"|N\s*>\s*4|legibility.limit.notice|exceed.{0,20}ceiling",
            text,
            re.IGNORECASE,
        ), (
            "ARCH-REVIEW-007 must identify a breaking point — where the encoding "
            "fails legibility constraints. Stating limits without naming the failure "
            "mode at those limits has not satisfied Q3. AC-4."
        )


# ===========================================================================
# AC-5 — ARCH-REVIEW-007 records binding decisions on four open questions
# ===========================================================================


class TestAC5FourOpenQuestions:
    """AC-5: ARCH-REVIEW-007 records binding decisions on all four Phase 1 open
    questions from design thinking doc §Phase 2 Readiness.

    Intent doc §4 AC-5: each of four patterns must appear 'with at least one
    surrounding sentence that does not end in "?" (i.e., it is a statement,
    not a question).'

    Silent failure: deferring to 'Phase 3 panel decision' restates the question
    without resolving it. AC-5 checks for resolution statements, not restatements
    (intent doc §3.3 ARCH-REVIEW-007 nominal vs. substantive).
    """

    def _has_statement_not_question(self, text: str, pattern: str) -> bool:
        """Return True if the pattern appears in a sentence not ending with '?'."""
        for m in re.finditer(pattern, text, re.IGNORECASE | re.DOTALL):
            pos = m.start()
            # Extract surrounding sentence (look back up to 300 chars for .\n or start)
            start = max(0, pos - 300)
            end = min(len(text), pos + 300)
            chunk = text[start:end]
            # Find sentence containing the match — split by sentence-ending punctuation
            sentences = re.split(r"(?<=[.!])\s+", chunk)
            for sent in sentences:
                if re.search(pattern, sent, re.IGNORECASE) and not sent.rstrip().endswith("?"):
                    return True
        return False

    def test_5a_mode3_single_entity_decision(self) -> None:
        if not _ARCH_REVIEW.exists():
            pytest.skip("ARCH-REVIEW-007-milestone15.md not yet authored — Step 3 pending")
        text = _text(_ARCH_REVIEW)
        pattern = r"Mode\s*3.{0,200}single.entity|single.entity.{0,200}Mode\s*3"
        assert re.search(pattern, text, re.IGNORECASE | re.DOTALL), (
            "ARCH-REVIEW-007 must address open question (a): Mode 3 single-entity "
            "encoding choice (composite 2-line vs. 4-framework 8-line). "
            "Design thinking doc §Phase 2 Readiness — open question 1. AC-5(a)."
        )
        assert self._has_statement_not_question(text, pattern), (
            "ARCH-REVIEW-007 Mode 3 single-entity content must be a binding decision "
            "statement — not a question or deferral to Phase 3. "
            "Silent failure guard per intent doc §3.3. AC-5(a)."
        )

    def test_5b_compare_view_multi_entity_decision(self) -> None:
        if not _ARCH_REVIEW.exists():
            pytest.skip("ARCH-REVIEW-007-milestone15.md not yet authored — Step 3 pending")
        text = _text(_ARCH_REVIEW)
        pattern = (
            r"COMPARE.VIEW.{0,200}multi.entity|multi.entity.{0,200}COMPARE.VIEW"
            r"|COMPARE.VIEW.{0,100}(Mode\s*1|Mode\s*2)"
        )
        assert re.search(pattern, text, re.IGNORECASE | re.DOTALL), (
            "ARCH-REVIEW-007 must address open question (b): multi-entity COMPARE_VIEW "
            "for Mode 1 and Mode 2. Design thinking doc §Phase 2 Readiness — open "
            "question 2. AC-5(b)."
        )
        assert self._has_statement_not_question(text, pattern), (
            "ARCH-REVIEW-007 COMPARE_VIEW multi-entity content must be a binding "
            "decision — not a question restatement. AC-5(b)."
        )

    def test_5c_composite_aggregation_rule_decision(self) -> None:
        if not _ARCH_REVIEW.exists():
            pytest.skip("ARCH-REVIEW-007-milestone15.md not yet authored — Step 3 pending")
        text = _text(_ARCH_REVIEW)
        pattern = (
            r"aggregation rule|composite.{0,30}aggregation"
            r"|simple average|minimum.{0,30}(floor|framework)"
            r"|weighted.{0,30}(composite|score)"
        )
        assert re.search(pattern, text, re.IGNORECASE | re.DOTALL), (
            "ARCH-REVIEW-007 must address open question (c): composite score "
            "aggregation rule (simple average / minimum / weighted). "
            "Design thinking doc §Phase 2 Readiness — open question 3. AC-5(c)."
        )
        assert self._has_statement_not_question(text, pattern), (
            "ARCH-REVIEW-007 composite aggregation content must be a binding "
            "decision — not a question restatement. AC-5(c)."
        )

    def test_5d_endpoint_label_collision_decision(self) -> None:
        if not _ARCH_REVIEW.exists():
            pytest.skip("ARCH-REVIEW-007-milestone15.md not yet authored — Step 3 pending")
        text = _text(_ARCH_REVIEW)
        pattern = (
            r"label collision|endpoint.{0,30}collision"
            r"|label.{0,30}(offset|overlap|nudge)"
            r"|N=4.{0,100}(label|collision)"
        )
        assert re.search(pattern, text, re.IGNORECASE | re.DOTALL), (
            "ARCH-REVIEW-007 must address open question (d): endpoint label collision "
            "at N=4 — specifying offset, nudge, or hover-to-label handling. "
            "Design thinking doc §Phase 2 Readiness — open question 4. AC-5(d)."
        )
        assert self._has_statement_not_question(text, pattern), (
            "ARCH-REVIEW-007 endpoint label collision content must be a binding "
            "decision — not a question restatement. AC-5(d)."
        )


# ===========================================================================
# AC-6 — backlog ARCH-011 marked ASSIGNED — ADR-017
# ===========================================================================


class TestAC6BacklogAssignment:
    """AC-6: docs/architecture/backlog.md ARCH-011 row contains
    'ASSIGNED — ADR-017' (not 'PENDING_NUMBER').

    Intent doc §4 AC-6: 'grep "ARCH-011" docs/architecture/backlog.md output
    contains "ASSIGNED — ADR-017" (not "PENDING_NUMBER"). This must be true
    before ADR-017 authorship begins; the QA test verifies the final state.'

    The Architect Agent marks ASSIGNED as the first Phase 3 step before
    beginning ADR-017 authorship (sprint entry §4 sequencing note step 5).
    """

    def test_backlog_exists(self) -> None:
        assert _BACKLOG.exists(), (
            "docs/architecture/backlog.md must exist. AC-6."
        )

    def test_arch_011_row_present(self) -> None:
        if not _BACKLOG.exists():
            pytest.skip("backlog.md not found")
        text = _text(_BACKLOG)
        arch_011_lines = [ln for ln in text.splitlines() if "ARCH-011" in ln]
        assert arch_011_lines, (
            "docs/architecture/backlog.md must contain an ARCH-011 row. "
            "ARCH-011 was added at M15 kickoff for the Zone 1A ADR. AC-6."
        )

    def test_arch_011_assigned_adr_017(self) -> None:
        if not _BACKLOG.exists():
            pytest.skip("backlog.md not found")
        text = _text(_BACKLOG)
        arch_011_lines = [ln for ln in text.splitlines() if "ARCH-011" in ln]
        if not arch_011_lines:
            pytest.skip("ARCH-011 row absent — checked by test above")
        arch_011_text = "\n".join(arch_011_lines)
        assert re.search(r"ASSIGNED.{0,20}ADR.017|ADR.017.{0,20}ASSIGNED", arch_011_text), (
            "The ARCH-011 row must contain 'ASSIGNED — ADR-017'. "
            f"Current ARCH-011 line(s): {arch_011_text!r}. "
            "Intent doc §4 AC-6. Sprint entry §4 sequencing note step 5."
        )

    def test_arch_011_not_pending_number(self) -> None:
        if not _BACKLOG.exists():
            pytest.skip("backlog.md not found")
        text = _text(_BACKLOG)
        arch_011_lines = [ln for ln in text.splitlines() if "ARCH-011" in ln]
        if not arch_011_lines:
            pytest.skip("ARCH-011 row absent — checked by prior test")
        arch_011_text = "\n".join(arch_011_lines)
        assert "PENDING_NUMBER" not in arch_011_text, (
            "ARCH-011 row still contains 'PENDING_NUMBER' — Architect Agent must "
            "update to 'ASSIGNED — ADR-017' before authoring ADR-017. "
            f"Current value: {arch_011_text!r}. AC-6."
        )


# ===========================================================================
# AC-7 — ADR-017 exists
# ===========================================================================


class TestAC7ADR017Exists:
    """AC-7: docs/adr/ADR-017-zone-1a-information-architecture.md exists.

    Intent doc §4 AC-7: os.path.isfile('docs/adr/ADR-017-zone-1a-information-
    architecture.md'). Canonical location: docs/adr/ (CLAUDE.md §Canonical
    Artifact Locations — Architecture Decision Records row).
    """

    def test_file_exists(self) -> None:
        assert _ADR_017.exists(), (
            "docs/adr/ADR-017-zone-1a-information-architecture.md must exist. "
            "Phase 3 deliverable for M15-G2 (issue #845 Phase 3). "
            "Intent doc §4 AC-7."
        )

    def test_file_not_empty(self) -> None:
        if not _ADR_017.exists():
            pytest.skip("ADR-017 not yet authored — Step 3 pending")
        text = _text(_ADR_017)
        assert len(text.strip()) > 1000, (
            "ADR-017 must contain substantive content (>1000 characters). "
            "A Tier 1 ADR has 15+ required sections — a stub does not satisfy AC-7."
        )


# ===========================================================================
# AC-8 — ADR-017 contains required structural content
# ===========================================================================


class TestAC8StructuralContent:
    """AC-8: ADR-017 contains all required structural content.

    Intent doc §4 AC-8: 'file must contain all of the following strings:
    "tier:", "Persona and UX Traceability", "UX Implication", "Silent Failure
    Mode", "North Star Test", "Mission Impact", and a fenced code block
    beginning with "mermaid" (the mandatory diagram).'

    The mermaid diagram is mandatory per docs/CODING_STANDARDS.md for all ADRs.
    The tier: field identifies Tier 1 classification (may appear in frontmatter
    or in the Tier Classification section as '**Tier:** 1').
    """

    _REQUIRED_STRINGS = [
        "Persona and UX Traceability",
        "UX Implication",
        "Silent Failure Mode",
        "North Star Test",
        "Mission Impact",
    ]

    def test_tier_field_present(self) -> None:
        if not _ADR_017.exists():
            pytest.skip("ADR-017 not yet authored — Step 3 pending")
        text = _text(_ADR_017)
        assert re.search(r"tier:\s*1|\*\*Tier:\*\*\s*1|\bTier:\s*1\b", text, re.IGNORECASE), (
            "ADR-017 must declare Tier 1 classification — via frontmatter 'tier: 1' "
            "or '**Tier:** 1' in the Tier Classification section. "
            "Zone 1A is a Zone 1 surface; Tier 1 is mandatory (template.md). "
            "Intent doc §4 AC-8 ('tier:' string required)."
        )

    def test_mermaid_diagram_present(self) -> None:
        if not _ADR_017.exists():
            pytest.skip("ADR-017 not yet authored — Step 3 pending")
        text = _text(_ADR_017)
        assert re.search(r"```mermaid", text, re.IGNORECASE), (
            "ADR-017 must contain a fenced mermaid code block ('```mermaid'). "
            "Mermaid diagrams are mandatory for all ADRs per "
            "docs/CODING_STANDARDS.md §Diagram Standards. "
            "Intent doc §4 AC-8 (fenced code block beginning with 'mermaid')."
        )

    def test_required_sections_present(self) -> None:
        if not _ADR_017.exists():
            pytest.skip("ADR-017 not yet authored — Step 3 pending")
        text = _text(_ADR_017)
        missing = [s for s in self._REQUIRED_STRINGS if s not in text]
        assert not missing, (
            f"ADR-017 is missing required structural content: {missing}. "
            "Intent doc §4 AC-8 requires all of: "
            f"{self._REQUIRED_STRINGS} plus 'tier:' and mermaid fence. "
            "These are Tier 1 mandatory sections from docs/adr/template.md."
        )

    def test_p_elements_present(self) -> None:
        """Persona Trace P-1 through P-7 must all appear (Tier 1 requirement)."""
        if not _ADR_017.exists():
            pytest.skip("ADR-017 not yet authored — Step 3 pending")
        text = _text(_ADR_017)
        missing = []
        for i in range(1, 8):
            if not re.search(rf"\*\*P-{i}\s*[—-]|\*\*P-{i}:", text, re.IGNORECASE):
                missing.append(f"P-{i}")
        assert not missing, (
            f"ADR-017 Persona Trace is missing elements: {missing}. "
            "All seven P-elements are required for Tier 1 ADRs "
            "(template.md: 'A trace missing any element is incomplete'). AC-8."
        )

    def test_ux_elements_present(self) -> None:
        """UX Implication Statement UX-1 through UX-7 must all appear."""
        if not _ADR_017.exists():
            pytest.skip("ADR-017 not yet authored — Step 3 pending")
        text = _text(_ADR_017)
        missing = []
        for i in range(1, 8):
            if not re.search(rf"\*\*UX-{i}\s*[—-]|\*\*UX-{i}:", text, re.IGNORECASE):
                missing.append(f"UX-{i}")
        assert not missing, (
            f"ADR-017 UX Implication Statement is missing elements: {missing}. "
            "All seven UX-elements are required for Tier 1 ADRs. AC-8."
        )

    def test_p7_north_star_names_specific_scenario(self) -> None:
        """P-7 must name a specific country/scenario — not aspirational language."""
        if not _ADR_017.exists():
            pytest.skip("ADR-017 not yet authored — Step 3 pending")
        text = _text(_ADR_017)
        p7_pos = text.find("**P-7")
        if p7_pos == -1:
            pytest.skip("P-7 not found — checked by test_p_elements_present")
        p7_text = text[p7_pos : p7_pos + 800]
        assert re.search(
            r"\b(ZMB|Zambia|JOR|Jordan|GRC|Greece|EGY|Egypt|finance ministr|Zambian)",
            p7_text,
            re.IGNORECASE,
        ), (
            "ADR-017 P-7 must name a specific country scenario "
            "(per intent doc §2 P-7 and CLAUDE.md §North Star Test (Process Gate)). "
            "'Improves situational awareness' is not sufficient. AC-8."
        )

    def test_ux3_contains_observable_state(self) -> None:
        """UX-3 must name a viewport and time ceiling — not aspirational."""
        if not _ADR_017.exists():
            pytest.skip("ADR-017 not yet authored — Step 3 pending")
        text = _text(_ADR_017)
        ux3_pos = text.find("**UX-3")
        if ux3_pos == -1:
            pytest.skip("UX-3 not found — checked by test_ux_elements_present")
        ux3_text = text[ux3_pos : ux3_pos + 600]
        assert re.search(
            r"(Zone\s*1A|1440.900|1280.800|1024.768|15.second|30.second)"
            r".{0,200}(visible|shows|displays|without.interaction)",
            ux3_text,
            re.IGNORECASE | re.DOTALL,
        ), (
            "ADR-017 UX-3 must name a viewport, Zone, and time ceiling with an "
            "observable state (not 'improves usability'). Template §UX-3: "
            "'a specific falsifiable acceptance criterion verifiable by observation "
            "in the live application.' AC-8."
        )


# ===========================================================================
# AC-9 — NM-042 four fields present
# ===========================================================================


class TestAC9NM042Fields:
    """AC-9: ADR-017 UX Designer sign-off block contains all four NM-042 fields.

    Intent doc §4 AC-9: 'file contains all four of: "Reviewing agent:",
    "Session context:", "Governing documents reviewed:", "Concerns found:".'

    CLAUDE.md §UX Designer sign-off: 'All four fields below are required —
    a checkbox without the structured attestation is non-compliant.'
    """

    def test_all_four_fields_present(self) -> None:
        if not _ADR_017.exists():
            pytest.skip("ADR-017 not yet authored — Step 3 pending")
        text = _text(_ADR_017)
        fields = {
            "Reviewing agent:": "**Reviewing agent:**",
            "Session context:": "**Session context:**",
            "Governing documents reviewed:": "**Governing documents reviewed:**",
            "Concerns found:": "**Concerns found:**",
        }
        missing = [label for label, marker in fields.items() if marker not in text]
        assert not missing, (
            f"ADR-017 UX Designer sign-off missing {len(missing)} NM-042 field(s): "
            f"{missing}. "
            "All four fields required (CLAUDE.md §UX Designer sign-off — NM-042). "
            "Intent doc §4 AC-9."
        )


# ===========================================================================
# AC-10 — Session context declared with valid value
# ===========================================================================


class TestAC10SessionContext:
    """AC-10: ADR-017 UX Designer Session context field contains one of the two
    valid NM-042 values.

    Intent doc §4 AC-10: 'the line following "Session context:" contains either
    "Same session as ADR authorship" or "Separate session, EL-triggered".'

    CLAUDE.md: 'Absence of a Session context declaration is a non-compliant
    sign-off. Treat it as Same session as ADR authorship — acknowledged until
    a properly declared review is obtained.'
    """

    def test_session_context_is_valid(self) -> None:
        if not _ADR_017.exists():
            pytest.skip("ADR-017 not yet authored — Step 3 pending")
        text = _text(_ADR_017)
        # Allow value on same line as field label or on the next line
        sc_match = re.search(
            r"\*\*Session context:\*\*\s*`?([^\n`]{1,200})`?",
            text,
        )
        if not sc_match:
            pytest.skip("Session context field not found — checked by AC-9")
        sc_value = sc_match.group(1).strip()

        is_placeholder = bool(re.match(
            r"^\[|^$|^N/A$|^TBD$|^TODO$", sc_value, re.IGNORECASE
        ))
        assert not is_placeholder, (
            f"ADR-017 Session context is a placeholder: {sc_value!r}. "
            "Must be one of two valid NM-042 values. AC-10."
        )

        valid_separate = bool(re.search(
            r"Separate session.{0,20}EL-triggered\s+\d{4}-\d{2}-\d{2}",
            sc_value,
            re.IGNORECASE,
        ))
        valid_same = bool(re.search(
            r"Same session as ADR authorship.{0,10}acknowledged",
            sc_value,
            re.IGNORECASE,
        ))
        assert valid_separate or valid_same, (
            f"ADR-017 Session context {sc_value!r} does not match either valid NM-042 form.\n"
            "Valid values:\n"
            "  'Separate session, EL-triggered YYYY-MM-DD'\n"
            "  'Same session as ADR authorship — acknowledged'\n"
            "CLAUDE.md §UX Designer sign-off (NM-042). AC-10."
        )


# ===========================================================================
# AC-11 — Governing documents reviewed: ≥2 § citations in sign-off block
# ===========================================================================


class TestAC11GoverningDocsSectionCitations:
    """AC-11: ADR-017 Governing documents reviewed field in the UX Designer
    sign-off block contains at least two § section citations.

    Intent doc §4 AC-11: 'content[content.index("Governing documents reviewed:"):
    ].count("§") ≥ 2 in the sign-off block.'

    CLAUDE.md: 'Named sections (information-hierarchy.md §1B, north-star.md
    §Primary Cognitive Tasks) do satisfy. Generic references ("governing
    premises", "first principles") do not.'

    The § count is taken only from the sign-off block (Governing documents
    reviewed → Concerns found) to avoid false positives from § elsewhere in
    the document (intent doc §3.3).
    """

    def test_sign_off_block_has_two_section_citations(self) -> None:
        if not _ADR_017.exists():
            pytest.skip("ADR-017 not yet authored — Step 3 pending")
        text = _text(_ADR_017)
        block = _sign_off_block(text)
        if not block:
            pytest.skip(
                "Governing documents reviewed field not found in sign-off block — "
                "checked by AC-9"
            )
        count = block.count("§")
        assert count >= 2, (
            f"ADR-017 sign-off block contains only {count} § citation(s) in "
            "'Governing documents reviewed' — requires ≥ 2. "
            "Named section examples: 'information-hierarchy.md §Zone 1A', "
            "'north-star.md §Primary Cognitive Tasks by Mode'. "
            "Generic references ('governing premises') do not satisfy NM-042. "
            "Intent doc §4 AC-11."
        )

    def test_ux_document_cited_in_sign_off(self) -> None:
        """At least one Zone 1A-relevant UX governing document must be named."""
        if not _ADR_017.exists():
            pytest.skip("ADR-017 not yet authored — Step 3 pending")
        text = _text(_ADR_017)
        block = _sign_off_block(text)
        if not block:
            pytest.skip("Sign-off block not found — checked by AC-9")
        assert re.search(
            r"information-hierarchy|north-star|user-journeys"
            r"|worldsim-ux-architecture-first-principles",
            block,
            re.IGNORECASE,
        ), (
            "ADR-017 sign-off 'Governing documents reviewed' must name at least one "
            "Zone 1A UX governing document (information-hierarchy.md, north-star.md, "
            "user-journeys.md, or worldsim-ux-architecture-first-principles.md). "
            "AC-11."
        )

    def test_el_acceptance_status(self) -> None:
        """Sprint exit gate: ADR-017 Status must be Accepted before G2 closes.

        This test is skipped if ADR-017 is still in Proposed state — the sprint
        exit document cannot be filed until this passes. The EL records acceptance
        by updating '## Status' to 'Accepted' (pattern from ADR-016).
        """
        if not _ADR_017.exists():
            pytest.skip("ADR-017 not yet authored — Step 3 pending")
        text = _text(_ADR_017)
        status_section = re.search(
            r"^#{1,3}\s+Status\s*\n(.{0,200})",
            text,
            re.IGNORECASE | re.MULTILINE,
        )
        if status_section is None:
            pytest.skip("## Status section not found in ADR-017 — draft incomplete")
        status_text = status_section.group(1)
        assert re.search(r"`Accepted`|\bAccepted\b", status_text), (
            "ADR-017 '## Status' must contain 'Accepted' before G2 sprint exit. "
            "A 'Proposed' status means EL acceptance has not yet been recorded. "
            "Sprint exit gate: intent doc §3.2 Secondary state B; sprint entry §3.1."
        )
