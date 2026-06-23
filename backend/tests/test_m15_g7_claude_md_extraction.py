"""Tests for M15-G7 CLAUDE.md extraction — AC-1 through AC-14.

QA Lead step 2 — authored BEFORE extraction begins, from acceptance criteria at:
  docs/process/sprint-plans/m15-g7-sprint-entry.md §Section 3.1

Sprint entry: docs/process/sprint-plans/m15-g7-sprint-entry.md
Issue: #1091

AC coverage:
  AC-1   docs/process/agent-execution-lifecycle.md exists
  AC-2   agent-execution-lifecycle.md contains all 5 lifecycle step headings
         ("Step 1 — Intent authorship" through "Step 5 — Validate")
  AC-3   agent-execution-lifecycle.md contains "Rejection artifact requirements"
  AC-4   agent-execution-lifecycle.md contains "Layer 3 Quality Gate"
  AC-5   agent-execution-lifecycle.md contains "Kryptonite Design Constraint"
  AC-6   agent-execution-lifecycle.md contains "Observable Application State"
  AC-7   docs/process/milestone-exit-sop.md exists
  AC-8   milestone-exit-sop.md contains all 4 exit ceremony step headings
         ("Step 1 — Open issue audit" through "Step 4 — Fresh session continuity test")
  AC-9   milestone-exit-sop.md contains 3 retrospective question phrases
         ("What defects evaded", "What process gaps", "What testing improvements")
  AC-10  CLAUDE.md line count ≤ 800 (pre-extraction baseline: 1082 lines)
  AC-11  CLAUDE.md contains "agent-execution-lifecycle.md" ≥1 time (see link retained)
  AC-12  CLAUDE.md contains "milestone-exit-sop.md" ≥1 time (see link retained)
  AC-13  grep -rn "CLAUDE.md §Agent Execution Lifecycle" docs/ returns 0 results
  AC-14  grep -rn "CLAUDE.md §Milestone Exit" or "CLAUDE.md §Milestone Retrospective"
         in docs/ returns 0 results

Pre-extraction state: AC-1, AC-7, AC-10 (line count), AC-11, AC-12 all FAIL —
child docs do not yet exist and CLAUDE.md is 1082 lines. Tests must be runnable
as failing before extraction begins. AC-13 and AC-14 may pass pre-extraction
if no docs/ cross-references to those anchors exist yet (confirmed at authoring
time: grep returns 0 for both).

All AC-1–AC-12 checks are filesystem/content checks — no database required.
AC-13 and AC-14 are grep checks across docs/.
"""

from __future__ import annotations

import pathlib
import re
import subprocess

import pytest

# ---------------------------------------------------------------------------
# Path constants
# ---------------------------------------------------------------------------

_REPO_ROOT = pathlib.Path(__file__).parent.parent.parent

_LIFECYCLE_DOC = _REPO_ROOT / "docs" / "process" / "agent-execution-lifecycle.md"
_EXIT_SOP = _REPO_ROOT / "docs" / "process" / "milestone-exit-sop.md"
_CLAUDE_MD = _REPO_ROOT / "CLAUDE.md"
_DOCS_DIR = _REPO_ROOT / "docs"

# ---------------------------------------------------------------------------
# AC-1: agent-execution-lifecycle.md exists
#
# Sprint entry §3.1 AC-1:
# os.path.exists("docs/process/agent-execution-lifecycle.md")
# Pre-extraction: file does not exist — test expected to FAIL until extraction lands.
# ---------------------------------------------------------------------------


def test_ac1_agent_execution_lifecycle_doc_exists() -> None:
    """AC-1: docs/process/agent-execution-lifecycle.md exists after extraction."""
    assert _LIFECYCLE_DOC.exists(), (
        "docs/process/agent-execution-lifecycle.md does not exist — "
        "Architect Agent has not yet extracted the Agent Execution Lifecycle section "
        "from CLAUDE.md (#1091). This test is expected to fail before extraction lands."
    )


# ---------------------------------------------------------------------------
# AC-2: agent-execution-lifecycle.md contains all 5 step headings
#
# Sprint entry §3.1 AC-2:
# grep -c "Step [1-5] —" docs/process/agent-execution-lifecycle.md returns 5
# The five headings are:
#   "Step 1 — Intent authorship"
#   "Step 2 — Test authorship"
#   "Step 3 — Implementation"
#   "Step 4 — Verify"
#   "Step 5 — Validate"
# ---------------------------------------------------------------------------


def test_ac2_lifecycle_doc_contains_all_five_step_headings() -> None:
    """AC-2: agent-execution-lifecycle.md has all 5 lifecycle step headings.

    Each of the five steps from the Agent Execution Lifecycle must appear in
    the child document as a heading. A child document that abbreviates or
    omits steps fails the completeness requirement (sprint entry §3.1).
    """
    if not _LIFECYCLE_DOC.exists():
        pytest.skip("agent-execution-lifecycle.md absent — G7 not yet implemented")

    content = _LIFECYCLE_DOC.read_text(encoding="utf-8")

    expected_headings = [
        "Step 1 — Intent authorship",
        "Step 2 — Test authorship",
        "Step 3 — Implementation",
        "Step 4 — Verify",
        "Step 5 — Validate",
    ]
    missing = [h for h in expected_headings if h not in content]
    assert not missing, (
        f"agent-execution-lifecycle.md is missing {len(missing)} step heading(s): "
        f"{missing} — the child document must be a complete transplant, not a summary. "
        "Every sentence from CLAUDE.md §Agent Execution Lifecycle must appear verbatim (#1091)."
    )


def test_ac2_step_heading_count_is_exactly_five() -> None:
    """AC-2 (count guard): 'Step N —' pattern matches exactly 5 headings.

    Belt-and-suspenders: confirms the grep-based AC-2 criterion from the sprint entry.
    Extra step headings (e.g. from nested subsections) would indicate content additions
    not in the original CLAUDE.md — the extraction must be verbatim.
    """
    if not _LIFECYCLE_DOC.exists():
        pytest.skip("agent-execution-lifecycle.md absent — G7 not yet implemented")

    content = _LIFECYCLE_DOC.read_text(encoding="utf-8")
    matches = re.findall(r"Step [1-5] —", content)
    assert len(matches) == 5, (
        f"Expected exactly 5 'Step N —' headings, found {len(matches)} — "
        "agent-execution-lifecycle.md must contain the five lifecycle steps and "
        "no additional or missing steps (#1091)."
    )


# ---------------------------------------------------------------------------
# AC-3: agent-execution-lifecycle.md contains "Rejection artifact requirements"
#
# Sprint entry §3.1 AC-3:
# grep -c "Rejection artifact requirements" returns ≥1
# The rejection artifact section is a mandatory component of the lifecycle doc —
# it defines what blocking artifacts look like when Verify or Validate fails.
# ---------------------------------------------------------------------------


def test_ac3_lifecycle_doc_contains_rejection_artifact_requirements() -> None:
    """AC-3: 'Rejection artifact requirements' appears ≥1 time in lifecycle doc.

    The rejection artifact section must be present as a complete transplant.
    Its absence would mean agents are operating without the documented
    rejection protocol — a silent process gap.
    """
    if not _LIFECYCLE_DOC.exists():
        pytest.skip("agent-execution-lifecycle.md absent — G7 not yet implemented")

    content = _LIFECYCLE_DOC.read_text(encoding="utf-8")
    count = content.count("Rejection artifact requirements")
    assert count >= 1, (
        f"'Rejection artifact requirements' appears {count} time(s) in "
        "agent-execution-lifecycle.md — the rejection artifact section must be "
        "transplanted in full from CLAUDE.md §When Verify or Validate fails (#1091)."
    )


# ---------------------------------------------------------------------------
# AC-4: agent-execution-lifecycle.md contains "Layer 3 Quality Gate"
#
# Sprint entry §3.1 AC-4:
# grep -c "Layer 3 Quality Gate" returns ≥1
# The Layer 3 Quality Gate (FD-2) defines self-interpreting output requirements
# and Customer Agent authority — must be present in the lifecycle doc.
# ---------------------------------------------------------------------------


def test_ac4_lifecycle_doc_contains_layer3_quality_gate() -> None:
    """AC-4: 'Layer 3 Quality Gate' appears ≥1 time in lifecycle doc."""
    if not _LIFECYCLE_DOC.exists():
        pytest.skip("agent-execution-lifecycle.md absent — G7 not yet implemented")

    content = _LIFECYCLE_DOC.read_text(encoding="utf-8")
    count = content.count("Layer 3 Quality Gate")
    assert count >= 1, (
        f"'Layer 3 Quality Gate' appears {count} time(s) in "
        "agent-execution-lifecycle.md — the Layer 3 Quality Gate (FD-2) section "
        "must be transplanted in full from CLAUDE.md (#1091)."
    )


# ---------------------------------------------------------------------------
# AC-5: agent-execution-lifecycle.md contains "Kryptonite Design Constraint"
#
# Sprint entry §3.1 AC-5:
# grep -c "Kryptonite Design Constraint" returns ≥1
# The Kryptonite constraint (FD-3) — finance ministry team accessibility test —
# must be present as it gates Step 1 intent authorship.
# ---------------------------------------------------------------------------


def test_ac5_lifecycle_doc_contains_kryptonite_design_constraint() -> None:
    """AC-5: 'Kryptonite Design Constraint' appears ≥1 time in lifecycle doc."""
    if not _LIFECYCLE_DOC.exists():
        pytest.skip("agent-execution-lifecycle.md absent — G7 not yet implemented")

    content = _LIFECYCLE_DOC.read_text(encoding="utf-8")
    count = content.count("Kryptonite Design Constraint")
    assert count >= 1, (
        f"'Kryptonite Design Constraint' appears {count} time(s) in "
        "agent-execution-lifecycle.md — the Kryptonite Design Constraint (FD-3) "
        "section must be transplanted in full from CLAUDE.md (#1091)."
    )


# ---------------------------------------------------------------------------
# AC-6: agent-execution-lifecycle.md contains "Observable Application State"
#
# Sprint entry §3.1 AC-6:
# grep -c "Observable Application State" returns ≥1
# The architectural definition of observable application state is required for
# QA Lead test authorship — its absence makes Step 2 unenforceable.
# ---------------------------------------------------------------------------


def test_ac6_lifecycle_doc_contains_observable_application_state() -> None:
    """AC-6: 'Observable Application State' appears ≥1 time in lifecycle doc."""
    if not _LIFECYCLE_DOC.exists():
        pytest.skip("agent-execution-lifecycle.md absent — G7 not yet implemented")

    content = _LIFECYCLE_DOC.read_text(encoding="utf-8")
    count = content.count("Observable Application State")
    assert count >= 1, (
        f"'Observable Application State' appears {count} time(s) in "
        "agent-execution-lifecycle.md — the architectural definition section "
        "must be transplanted in full from CLAUDE.md (#1091)."
    )


# ---------------------------------------------------------------------------
# AC-7: milestone-exit-sop.md exists
#
# Sprint entry §3.1 AC-7:
# os.path.exists("docs/process/milestone-exit-sop.md")
# Pre-extraction: file does not exist — test expected to FAIL until extraction lands.
# ---------------------------------------------------------------------------


def test_ac7_milestone_exit_sop_exists() -> None:
    """AC-7: docs/process/milestone-exit-sop.md exists after extraction."""
    assert _EXIT_SOP.exists(), (
        "docs/process/milestone-exit-sop.md does not exist — "
        "Architect Agent has not yet extracted the Milestone Exit Ceremony and "
        "Retrospective sections from CLAUDE.md (#1091). "
        "This test is expected to fail before extraction lands."
    )


# ---------------------------------------------------------------------------
# AC-8: milestone-exit-sop.md contains all 4 exit ceremony step headings
#
# Sprint entry §3.1 AC-8:
# grep -c "Step [1-4] —" docs/process/milestone-exit-sop.md returns 4
# The four steps are:
#   "Step 1 — Open issue audit (GitHub)"
#   "Step 2 — Milestone reference audit"
#   "Step 3 — SESSION_STATE internal consistency check"
#   "Step 4 — Fresh session continuity test"
# ---------------------------------------------------------------------------


def test_ac8_exit_sop_contains_all_four_step_headings() -> None:
    """AC-8: milestone-exit-sop.md has all 4 exit ceremony step headings.

    A child document missing any step heading has truncated the exit ceremony —
    a future session would miss a mandatory gate without any indication.
    """
    if not _EXIT_SOP.exists():
        pytest.skip("milestone-exit-sop.md absent — G7 not yet implemented")

    content = _EXIT_SOP.read_text(encoding="utf-8")

    expected_headings = [
        "Step 1 — Open issue audit",
        "Step 2 — Milestone reference audit",
        "Step 3 — SESSION_STATE internal consistency check",
        "Step 4 — Fresh session continuity test",
    ]
    missing = [h for h in expected_headings if h not in content]
    assert not missing, (
        f"milestone-exit-sop.md is missing {len(missing)} step heading(s): "
        f"{missing} — the child document must be a complete transplant of "
        "CLAUDE.md §Milestone Exit Ceremony (#1091)."
    )


def test_ac8_exit_step_heading_count_is_exactly_four() -> None:
    """AC-8 (count guard): 'Step N —' pattern matches exactly 4 headings in exit SOP."""
    if not _EXIT_SOP.exists():
        pytest.skip("milestone-exit-sop.md absent — G7 not yet implemented")

    content = _EXIT_SOP.read_text(encoding="utf-8")
    matches = re.findall(r"Step [1-4] —", content)
    assert len(matches) == 4, (
        f"Expected exactly 4 'Step N —' headings in milestone-exit-sop.md, "
        f"found {len(matches)} — exit SOP must contain the four ceremony steps "
        "and no additional or missing steps (#1091)."
    )


# ---------------------------------------------------------------------------
# AC-9: milestone-exit-sop.md contains 3 retrospective question phrases
#
# Sprint entry §3.1 AC-9:
# grep -c "What defects evaded\|What process gaps\|What testing improvements"
# returns 3
# The three named questions from §Milestone Retrospective Process must all appear.
# ---------------------------------------------------------------------------


def test_ac9_exit_sop_contains_retrospective_what_defects_evaded() -> None:
    """AC-9a: 'What defects evaded' appears in milestone-exit-sop.md."""
    if not _EXIT_SOP.exists():
        pytest.skip("milestone-exit-sop.md absent — G7 not yet implemented")

    content = _EXIT_SOP.read_text(encoding="utf-8")
    assert "What defects evaded" in content, (
        "'What defects evaded' not found in milestone-exit-sop.md — "
        "the retrospective's first question must be present (#1091)."
    )


def test_ac9_exit_sop_contains_retrospective_what_process_gaps() -> None:
    """AC-9b: 'What process gaps' appears in milestone-exit-sop.md."""
    if not _EXIT_SOP.exists():
        pytest.skip("milestone-exit-sop.md absent — G7 not yet implemented")

    content = _EXIT_SOP.read_text(encoding="utf-8")
    assert "What process gaps" in content, (
        "'What process gaps' not found in milestone-exit-sop.md — "
        "the retrospective's second question must be present (#1091)."
    )


def test_ac9_exit_sop_contains_retrospective_what_testing_improvements() -> None:
    """AC-9c: 'What testing improvements' appears in milestone-exit-sop.md."""
    if not _EXIT_SOP.exists():
        pytest.skip("milestone-exit-sop.md absent — G7 not yet implemented")

    content = _EXIT_SOP.read_text(encoding="utf-8")
    assert "What testing improvements" in content, (
        "'What testing improvements' not found in milestone-exit-sop.md — "
        "the retrospective's third question must be present (#1091)."
    )


def test_ac9_all_three_retrospective_questions_present() -> None:
    """AC-9 (combined): all 3 retrospective question phrases present (sprint entry grep form).

    Mirrors the sprint entry grep: the three phrases together confirm the full
    retrospective section was transplanted, not truncated after the heading.
    """
    if not _EXIT_SOP.exists():
        pytest.skip("milestone-exit-sop.md absent — G7 not yet implemented")

    content = _EXIT_SOP.read_text(encoding="utf-8")
    phrases = ["What defects evaded", "What process gaps", "What testing improvements"]
    found = sum(1 for p in phrases if p in content)
    assert found == 3, (
        f"{found}/3 retrospective question phrases found in milestone-exit-sop.md — "
        "all three must be present: 'What defects evaded', 'What process gaps', "
        "'What testing improvements' (#1091)."
    )


# ---------------------------------------------------------------------------
# AC-10: CLAUDE.md line count ≤ 800
#
# Sprint entry §3.1 AC-10:
# subprocess.run(["wc", "-l", "CLAUDE.md"]) output integer ≤ 800
# Pre-extraction baseline: 1082 lines (2026-06-23).
# Target requires ≥ 282 lines extracted (~25% reduction).
# ---------------------------------------------------------------------------

_CLAUDE_MD_PRE_EXTRACTION_LINES = 1082
_CLAUDE_MD_LINE_CEILING = 800


def test_ac10_claude_md_line_count_at_most_800() -> None:
    """AC-10: CLAUDE.md line count is ≤ 800 after extraction.

    Pre-extraction baseline: 1082 lines (2026-06-23).
    The three extractions (lifecycle ~200 lines, exit ceremony ~65 lines,
    DIC deduplication ~25 lines) target a ≥ 282-line reduction.
    A line count above 800 means at least one extraction is incomplete.
    """
    assert _CLAUDE_MD.exists(), "CLAUDE.md not found at repository root"

    result = subprocess.run(  # noqa: S603
        ["wc", "-l", str(_CLAUDE_MD)],  # noqa: S607
        capture_output=True,
        text=True,
        check=False,
    )
    # wc -l output: "  1082 /path/to/CLAUDE.md"
    line_count = int(result.stdout.split()[0])

    assert line_count <= _CLAUDE_MD_LINE_CEILING, (
        f"CLAUDE.md has {line_count} lines — must be ≤ {_CLAUDE_MD_LINE_CEILING} "
        f"after G7 extraction (pre-extraction baseline: {_CLAUDE_MD_PRE_EXTRACTION_LINES} lines). "
        "One or more extraction sections may not have been removed from CLAUDE.md (#1091)."
    )


# ---------------------------------------------------------------------------
# AC-11: CLAUDE.md retains "agent-execution-lifecycle.md" link
#
# Sprint entry §3.1 AC-11:
# grep -c "agent-execution-lifecycle.md" CLAUDE.md returns ≥1
# The extracted section must be replaced with a summary sentence + see link,
# not deleted entirely. An agent reading only CLAUDE.md must be able to
# navigate to the full lifecycle doc.
# ---------------------------------------------------------------------------


def test_ac11_claude_md_retains_lifecycle_doc_link() -> None:
    """AC-11: CLAUDE.md contains 'agent-execution-lifecycle.md' ≥1 time.

    After extraction the lifecycle section body is replaced with a summary
    sentence and a 'see docs/process/agent-execution-lifecycle.md' link.
    A CLAUDE.md with no such link silently hides the lifecycle from any agent
    that reads only the top-level file without following every reference.
    """
    assert _CLAUDE_MD.exists(), "CLAUDE.md not found at repository root"

    content = _CLAUDE_MD.read_text(encoding="utf-8")
    count = content.count("agent-execution-lifecycle.md")
    assert count >= 1, (
        f"'agent-execution-lifecycle.md' appears {count} time(s) in CLAUDE.md — "
        "CLAUDE.md must retain a 'see docs/process/agent-execution-lifecycle.md' link "
        "in the position of the extracted §Agent Execution Lifecycle section (#1091)."
    )


# ---------------------------------------------------------------------------
# AC-12: CLAUDE.md retains "milestone-exit-sop.md" link
#
# Sprint entry §3.1 AC-12:
# grep -c "milestone-exit-sop.md" CLAUDE.md returns ≥1
# Same rationale as AC-11 — the exit ceremony must remain discoverable from
# CLAUDE.md even though the full content lives in the child doc.
# ---------------------------------------------------------------------------


def test_ac12_claude_md_retains_exit_sop_link() -> None:
    """AC-12: CLAUDE.md contains 'milestone-exit-sop.md' ≥1 time.

    After extraction the exit ceremony section body is replaced with a summary
    sentence and a 'see docs/process/milestone-exit-sop.md' link.
    A missing link means a future session misses the exit ceremony without
    any navigation path from CLAUDE.md.
    """
    assert _CLAUDE_MD.exists(), "CLAUDE.md not found at repository root"

    content = _CLAUDE_MD.read_text(encoding="utf-8")
    count = content.count("milestone-exit-sop.md")
    assert count >= 1, (
        f"'milestone-exit-sop.md' appears {count} time(s) in CLAUDE.md — "
        "CLAUDE.md must retain a 'see docs/process/milestone-exit-sop.md' link "
        "in the position of the extracted §Milestone Exit Ceremony section (#1091)."
    )


# ---------------------------------------------------------------------------
# AC-13: No navigation cross-reference in docs/ points to
#         "CLAUDE.md §Agent Execution Lifecycle"
#
# Sprint entry §3.1 AC-13:
# grep -rn "CLAUDE.md §Agent Execution Lifecycle" docs/ returns 0 results
# The Architect Agent must update all cross-references found in the mandatory
# pre-extraction audit. A surviving stale reference is a broken pointer —
# it directs a reader to an anchor that no longer exists in CLAUDE.md.
#
# Exclusions (planning artifacts — contain the pattern as grep command text
# or extraction-mapping table cells, NOT as navigation authority citations):
#   - docs/process/sprint-plans/m15-g7-sprint-entry.md  (describes the work)
#   - docs/process/intents/M15-G7-*  (intent doc for the extraction)
# All other occurrences are navigation authority citations that must be updated.
# ---------------------------------------------------------------------------

# Files that legitimately contain the pattern as grep-command or extraction-table
# text rather than as navigation references — excluded from AC-13/14 checks.
_G7_PLANNING_DOCS = {
    str(_DOCS_DIR / "process" / "sprint-plans" / "m15-g7-sprint-entry.md"),
}
# Intent doc name contains the date so match by prefix pattern resolved at runtime
_G7_INTENT_PREFIX = str(_DOCS_DIR / "process" / "intents" / "M15-G7-")


def _filter_stale_refs(raw_output: str) -> list[str]:
    """Return only files from grep output that are genuine navigation references.

    Excludes the G7 sprint entry and G7 intent doc, which mention the pattern
    as grep command text or extraction-table cells, not as navigation citations.
    """
    files = [f for f in raw_output.strip().splitlines() if f]
    return [
        f for f in files
        if f not in _G7_PLANNING_DOCS and not f.startswith(_G7_INTENT_PREFIX)
    ]


def test_ac13_no_docs_crossreference_to_claude_md_agent_execution_lifecycle() -> None:
    """AC-13: no file in docs/ has a navigation reference to 'CLAUDE.md §Agent Execution Lifecycle'.

    The Architect Agent must update all authority-citation cross-references found
    in the pre-extraction audit (sprint entry §Section 4 step 3) to point to
    docs/process/agent-execution-lifecycle.md. A surviving stale reference is a
    broken pointer — readers are sent to a section that no longer exists in CLAUDE.md.

    Excluded from this check (contain the pattern as grep-command text or extraction
    table cells, not as navigation citations): m15-g7 sprint entry, M15-G7 intent doc.
    """
    result = subprocess.run(  # noqa: S603
        ["grep", "-rl", "CLAUDE.md §Agent Execution Lifecycle", str(_DOCS_DIR)],  # noqa: S607
        capture_output=True,
        text=True,
        check=False,
    )
    stale_files = _filter_stale_refs(result.stdout)

    assert not stale_files, (
        f"{len(stale_files)} file(s) in docs/ still have navigation references to "
        "'CLAUDE.md §Agent Execution Lifecycle' — "
        "update to docs/process/agent-execution-lifecycle.md:\n"
        + "\n".join(stale_files)
        + "\nRun: grep -rn \"CLAUDE.md §Agent Execution Lifecycle\" docs/ (#1091)."
    )


# ---------------------------------------------------------------------------
# AC-14: No navigation cross-reference in docs/ points to
#         "CLAUDE.md §Milestone Exit Ceremony" or "CLAUDE.md §Milestone Retrospective"
#
# Sprint entry §3.1 AC-14:
# grep -rn "CLAUDE.md §Milestone Exit\|CLAUDE.md §Milestone Retrospective" docs/
# returns 0 results (excluding G7 planning docs — same rationale as AC-13).
# ---------------------------------------------------------------------------


def test_ac14_no_docs_crossreference_to_claude_md_milestone_exit() -> None:
    """AC-14a: no file in docs/ has a navigation ref to 'CLAUDE.md §Milestone Exit'."""
    result = subprocess.run(  # noqa: S603
        ["grep", "-rl", "CLAUDE.md §Milestone Exit", str(_DOCS_DIR)],  # noqa: S607
        capture_output=True,
        text=True,
        check=False,
    )
    stale_files = _filter_stale_refs(result.stdout)

    assert not stale_files, (
        f"{len(stale_files)} file(s) in docs/ still reference 'CLAUDE.md §Milestone Exit' "
        "— update to docs/process/milestone-exit-sop.md:\n"
        + "\n".join(stale_files)
        + "\nRun: grep -rn \"CLAUDE.md §Milestone Exit\" docs/ (#1091)."
    )


def test_ac14_no_docs_crossreference_to_claude_md_milestone_retrospective() -> None:
    """AC-14b: no file in docs/ has a navigation ref to 'CLAUDE.md §Milestone Retrospective'."""
    result = subprocess.run(  # noqa: S603
        ["grep", "-rl", "CLAUDE.md §Milestone Retrospective", str(_DOCS_DIR)],  # noqa: S607
        capture_output=True,
        text=True,
        check=False,
    )
    stale_files = _filter_stale_refs(result.stdout)

    assert not stale_files, (
        f"{len(stale_files)} file(s) in docs/ still reference "
        "'CLAUDE.md §Milestone Retrospective' — update to docs/process/milestone-exit-sop.md:\n"
        + "\n".join(stale_files)
        + "\nRun: grep -rn \"CLAUDE.md §Milestone Retrospective\" docs/ (#1091)."
    )


def test_ac14_combined_no_stale_exit_or_retrospective_refs() -> None:
    """AC-14 (combined): no stale §Milestone Exit or §Milestone Retrospective refs in docs/.

    Belt-and-suspenders: confirms both anchor patterns absent across the full
    docs/ tree in a single assertion. Excludes G7 planning docs (same as AC-13/14a/b).
    """
    for pattern in ("CLAUDE.md §Milestone Exit", "CLAUDE.md §Milestone Retrospective"):
        result = subprocess.run(  # noqa: S603
            ["grep", "-rl", pattern, str(_DOCS_DIR)],  # noqa: S607
            capture_output=True,
            text=True,
            check=False,
        )
        stale_files = _filter_stale_refs(result.stdout)
        assert not stale_files, (
            f"Pattern '{pattern}' still found in {len(stale_files)} file(s):\n"
            + "\n".join(stale_files)
            + "\nUpdate all refs to docs/process/milestone-exit-sop.md (#1091)."
        )
