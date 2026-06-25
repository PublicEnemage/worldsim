"""Tests for M16-G5 process + secondary features — AC-1 through AC-9.

QA Lead step 2 — authored BEFORE implementation, from intent document at:
  docs/process/intents/M16-G5-2026-06-23-process-secondary-features.md

Sprint entry: docs/process/sprint-plans/m16-g5-sprint-entry.md

AC coverage:
  AC-1   docs/vision/worldsim-founding-document.md names "AC-001" as a labelled
         constraint in §Open Source as Strategy (#1145)
  AC-2   founding document names "AC-002" as a labelled constraint (#1145)
  AC-3   "permanent" appears in §Open Source as Strategy section — both constraints
         are characterised as permanent architectural constraints, not guidelines (#1145)
  AC-4   bash scripts/demo.sh --milestone 16 exits 0 — flag accepted without error (#837)
  AC-4b  stdout of scripts/demo.sh --milestone 16 contains M16 demo document content,
         not hardcoded M10/M14 Argentina content (#837)
  AC-5   "argentina" is absent from scripts/demo.sh and
         frontend/tests/e2e/demo-narrated.spec.ts (case-insensitive) (#837)
  AC-6   "solo-use" or "solo use" appears ≥1 time in
         docs/process/demo-preparation-standard.md — named solo-use gate present (#951)
  AC-7   "[SOLO]" appears ≥1 time in demo-preparation-standard.md — tag convention
         defined for solo-use reviewer findings (#951)
  AC-8   "Customer Agent" appears in §Step 6b in the context of the solo-use reviewer
         designation — Customer Agent is the named solo-use reviewer, not anonymous (#951)
  AC-9   docs/standards/legibility-baseline-m16.md exists; contains the four Tier 1
         threshold labels; contains at least one numeric value per threshold (not blank
         or TBD) — current-milestone measurements are recorded (#259)

Silent failure guards (from intent doc §3.3):
  SF-1 (#1145): AC-001/AC-002 added as prose without label strings fails AC-1/AC-2.
       "permanent" missing from §Open Source as Strategy fails AC-3.
  SF-2 (#837): --milestone flag accepted but output still serves M10/Argentina content
       fails AC-4b and AC-5.
  SF-3 (#951): solo-use gate added but Customer Agent not named as designated reviewer
       fails AC-8.
  SF-4 (#259): legibility file exists but values are blank or TBD fails AC-9 numeric check.

AC-1–AC-3, AC-5–AC-9 are filesystem content checks — no database or Docker required.
AC-4/AC-4b invoke scripts/demo.sh via subprocess; skipped when Docker is not running
and the script is found to require it. Tests that depend on a missing predecessor file
skip rather than fail so they do not obscure the root blocker.
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

_FOUNDING_DOC = _REPO_ROOT / "docs" / "vision" / "worldsim-founding-document.md"
_DEMO_SCRIPT = _REPO_ROOT / "scripts" / "demo.sh"
_DEMO_NARRATED_SPEC = (
    _REPO_ROOT / "frontend" / "tests" / "e2e" / "demo-narrated.spec.ts"
)
_DEMO_PREP_STANDARD = _REPO_ROOT / "docs" / "process" / "demo-preparation-standard.md"
_LEGIBILITY_BASELINE = _REPO_ROOT / "docs" / "standards" / "legibility-baseline-m16.md"

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _extract_markdown_section(content: str, heading_text: str) -> str:
    """Return the text body under the first heading that contains heading_text.

    Scans for any ATX heading (# through ######) whose text contains
    heading_text (case-insensitive).  Returns everything from that heading
    line up to (but not including) the next heading of the same or higher
    level, or end-of-file.  Returns "" if the heading is not found.
    """
    heading_re = re.compile(r"^(#{1,6})\s+(.*)", re.MULTILINE)
    target_match: re.Match[str] | None = None
    target_level: int = 0

    for m in heading_re.finditer(content):
        if heading_text.lower() in m.group(2).lower():
            target_match = m
            target_level = len(m.group(1))
            break

    if target_match is None:
        return ""

    start = target_match.start()
    end_re = re.compile(r"^#{1," + str(target_level) + r"}\s+", re.MULTILINE)
    end_match = end_re.search(content, target_match.end())
    end = end_match.start() if end_match else len(content)
    return content[start:end]


# ---------------------------------------------------------------------------
# AC-1: "AC-001" labelled in docs/vision/worldsim-founding-document.md (#1145)
#
# Intent doc §4 AC-1:
# grep -c "AC-001" docs/vision/worldsim-founding-document.md returns ≥1.
# Confirms the open-access constraint is explicitly named — not only present
# as prose reasoning — so contributors can cite it by stable reference number.
# Pre-implementation: "AC-001" is absent (count = 0).
# ---------------------------------------------------------------------------


def test_ac1a_founding_document_exists() -> None:
    """AC-1a: docs/vision/worldsim-founding-document.md exists."""
    assert _FOUNDING_DOC.exists(), (
        "docs/vision/worldsim-founding-document.md does not exist — "
        "path may have changed or file was not committed"
    )


def test_ac1b_founding_doc_names_ac001() -> None:
    """AC-1b: 'AC-001' appears ≥1 time in the founding document (#1145).

    SF-1 guard: prose-only additions without the label string fail this test.
    A contributor must be able to cite the constraint as 'AC-001' without
    reading docs/architecture/constraints.md.
    """
    if not _FOUNDING_DOC.exists():
        pytest.skip("founding document absent — cannot verify AC-1")

    content = _FOUNDING_DOC.read_text(encoding="utf-8")
    count = content.count("AC-001")
    assert count >= 1, (
        f"'AC-001' appears {count} time(s) in worldsim-founding-document.md — "
        "EL must add the explicit AC-001 constraint label to §Open Source as Strategy (#1145). "
        "Pre-implementation count is 0 — this test is expected to fail until #1145 lands."
    )


# ---------------------------------------------------------------------------
# AC-2: "AC-002" labelled in docs/vision/worldsim-founding-document.md (#1145)
#
# Intent doc §4 AC-2:
# grep -c "AC-002" docs/vision/worldsim-founding-document.md returns ≥1.
# Confirms the standing synthetic-estimate permission is explicitly named —
# not only present as prose reasoning.
# Pre-implementation: "AC-002" is absent (count = 0).
# ---------------------------------------------------------------------------


def test_ac2_founding_doc_names_ac002() -> None:
    """AC-2: 'AC-002' appears ≥1 time in the founding document (#1145).

    SF-1 guard: prose-only additions without the label string fail this test.
    A contributor must be able to cite the synthetic-estimate permission as
    'AC-002' without separate consultation of constraints.md.
    """
    if not _FOUNDING_DOC.exists():
        pytest.skip("founding document absent — cannot verify AC-2")

    content = _FOUNDING_DOC.read_text(encoding="utf-8")
    count = content.count("AC-002")
    assert count >= 1, (
        f"'AC-002' appears {count} time(s) in worldsim-founding-document.md — "
        "EL must add the explicit AC-002 constraint label to §Open Source as Strategy (#1145). "
        "Pre-implementation count is 0 — this test is expected to fail until #1145 lands."
    )


# ---------------------------------------------------------------------------
# AC-3: "permanent" in §Open Source as Strategy — constraints are permanent (#1145)
#
# Intent doc §4 AC-3:
# grep -c "permanent" in the §Open Source as Strategy section returns ≥1.
# Confirms AC-001/AC-002 are characterised as "permanent architectural constraints"
# rather than guidelines, preferences, or strategic commitments.
# Pre-implementation: "permanent" exists elsewhere in the document but NOT in
# §Open Source as Strategy — AC-3 is expected to fail until #1145 lands.
# ---------------------------------------------------------------------------


def test_ac3a_open_source_section_exists() -> None:
    """AC-3a: '§Open Source as Strategy' section is present in the founding document."""
    if not _FOUNDING_DOC.exists():
        pytest.skip("founding document absent — cannot verify AC-3a")

    content = _FOUNDING_DOC.read_text(encoding="utf-8")
    section = _extract_markdown_section(content, "Open Source as Strategy")
    assert section, (
        "§Open Source as Strategy section not found in worldsim-founding-document.md — "
        "section heading may have been renamed or removed"
    )


def test_ac3b_permanent_in_open_source_section() -> None:
    """AC-3b: 'permanent' appears in §Open Source as Strategy — constraints are permanent.

    SF-1 guard: if 'permanent' only appears in other sections (e.g., Mode 3 exclusion)
    but not in the §Open Source as Strategy section alongside AC-001/AC-002, this test
    fails — confirming the constraints are guidelines rather than permanent constraints.
    """
    if not _FOUNDING_DOC.exists():
        pytest.skip("founding document absent — cannot verify AC-3b")

    content = _FOUNDING_DOC.read_text(encoding="utf-8")
    section = _extract_markdown_section(content, "Open Source as Strategy")
    if not section:
        pytest.skip("§Open Source as Strategy section not found — AC-3a prerequisite fails")

    count = section.lower().count("permanent")
    assert count >= 1, (
        f"'permanent' appears {count} time(s) in §Open Source as Strategy — "
        "both AC-001 and AC-002 must be characterised as permanent architectural "
        "constraints (the word 'permanent' must appear in proximity to the declarations) "
        "per #1145. Note: 'permanent' exists elsewhere in the document but must also "
        "appear in this section."
    )


# ---------------------------------------------------------------------------
# AC-4: scripts/demo.sh --milestone 16 exits 0 (#837)
#
# Intent doc §4 AC-4:
# bash scripts/demo.sh --milestone 16 exits 0 — confirming the script accepts
# the --milestone parameter and runs without error for milestone 16.
# Pre-implementation: --milestone is an unknown flag → exits 1.
# Docker dependency: if Docker is not running and the script requires it,
# the test is skipped rather than failed — the flag-acceptance issue is distinct
# from Docker availability.
# ---------------------------------------------------------------------------


def test_ac4_demo_script_exists() -> None:
    """AC-4 pre-check: scripts/demo.sh exists."""
    assert _DEMO_SCRIPT.exists(), "scripts/demo.sh does not exist"


def test_ac4_demo_script_accepts_milestone_flag() -> None:
    """AC-4: scripts/demo.sh --milestone 16 does not reject the --milestone flag (#837).

    Pre-implementation the script exits 1 with "Unknown flag: --milestone".
    Post-implementation it exits 0 (or non-zero only for Docker/infrastructure
    reasons, not flag parsing).
    """
    if not _DEMO_SCRIPT.exists():
        pytest.skip("scripts/demo.sh absent — cannot run AC-4 subprocess check")

    result = subprocess.run(  # noqa: S603
        ["bash", str(_DEMO_SCRIPT), "--milestone", "16"],  # noqa: S607
        capture_output=True,
        text=True,
        timeout=30,
    )

    combined_output = result.stdout + result.stderr

    # If the flag was rejected → implementation not done
    if "Unknown flag: --milestone" in combined_output:
        pytest.fail(
            "scripts/demo.sh rejected '--milestone 16' with 'Unknown flag' — "
            "#837 not yet implemented. The --milestone parameter must be accepted "
            "by the argument parser."
        )

    # If Docker is not running → skip (infrastructure gap, not implementation gap)
    if result.returncode != 0 and "Docker is not running" in combined_output:
        pytest.skip(
            "Docker is not running — AC-4 subprocess test requires Docker. "
            "The --milestone flag was accepted (no 'Unknown flag' error) but "
            "the full stack cannot be verified without Docker."
        )

    assert result.returncode == 0, (
        f"scripts/demo.sh --milestone 16 exited {result.returncode}.\n"
        f"stdout: {result.stdout[:500]}\nstderr: {result.stderr[:500]}"
    )


# ---------------------------------------------------------------------------
# AC-4b: stdout of demo.sh --milestone 16 references M16 content (#837)
#
# Intent doc §4 AC-4b:
# The stdout contains at least one reference to M16 demo document content —
# docs/demo/m16/stakeholder-walkthrough.md or docs/demo/m16/screenshot-brief.md.
# Confirms content derivation is milestone-specific, not hardcoded from M10/M14.
# SF-2 guard: flag accepted but output still references hardcoded M14/Argentina
# content fails this test via absence of M16 document references.
# ---------------------------------------------------------------------------


def test_ac4b_demo_script_milestone16_output_references_m16_content() -> None:
    """AC-4b: stdout of demo.sh --milestone 16 contains M16 demo document reference (#837).

    SF-2 guard: if the script accepts --milestone 16 but derives output from
    hardcoded M14 Zambia/Argentina content, the M16 document paths will be absent.
    """
    if not _DEMO_SCRIPT.exists():
        pytest.skip("scripts/demo.sh absent — cannot run AC-4b subprocess check")

    result = subprocess.run(  # noqa: S603
        ["bash", str(_DEMO_SCRIPT), "--milestone", "16"],  # noqa: S607
        capture_output=True,
        text=True,
        timeout=30,
    )

    combined_output = result.stdout + result.stderr

    if "Unknown flag: --milestone" in combined_output:
        pytest.skip(
            "scripts/demo.sh rejected '--milestone 16' — AC-4 prerequisite not met; "
            "AC-4b cannot be verified until AC-4 passes"
        )

    if result.returncode != 0 and "Docker is not running" in combined_output:
        pytest.skip(
            "Docker not running — cannot capture full stdout for AC-4b check"
        )

    stdout = result.stdout
    has_m16_reference = bool(
        "m16" in stdout.lower()
        or "milestone 16" in stdout.lower()
        or "docs/demo/m16" in stdout
        or "screenshot-brief" in stdout
        or "stakeholder-walkthrough" in stdout
    )
    assert has_m16_reference, (
        "stdout of 'scripts/demo.sh --milestone 16' does not reference M16 demo "
        "document content — SF-2: flag accepted but output still hardcoded to an "
        "earlier milestone. Expected reference to docs/demo/m16/stakeholder-walkthrough.md "
        "or docs/demo/m16/screenshot-brief.md in the presenter guide output (#837).\n"
        f"stdout (first 800 chars): {stdout[:800]}"
    )


# ---------------------------------------------------------------------------
# AC-5: no "argentina" in scripts/demo.sh or demo-narrated.spec.ts (#837)
#
# Intent doc §4 AC-5:
# grep -ci "argentina" scripts/demo.sh returns 0
# AND grep -ci "argentina" frontend/tests/e2e/demo-narrated.spec.ts returns 0.
# Historical demo directory content under docs/demo/m10/ is excluded.
# Pre-implementation: scripts/demo.sh contains 2 case-insensitive "argentina"
# references (hardcoded M14 Demo 5 content). demo-narrated.spec.ts has 0.
# ---------------------------------------------------------------------------


def test_ac5a_demo_script_contains_no_argentina() -> None:
    """AC-5a: 'argentina' is absent from scripts/demo.sh (case-insensitive) (#837).

    SF-2 guard: hardcoded M10/M14 Argentina content in demo.sh means --milestone N
    cannot produce correct content for other milestones — the script is not truly
    configuration-driven. Pre-implementation count is 2.
    """
    if not _DEMO_SCRIPT.exists():
        pytest.skip("scripts/demo.sh absent — cannot verify AC-5a")

    content = _DEMO_SCRIPT.read_text(encoding="utf-8")
    count = len(re.findall(r"argentina", content, re.IGNORECASE))
    assert count == 0, (
        f"'argentina' appears {count} time(s) in scripts/demo.sh — "
        "hardcoded M10/M14 Argentina content must be removed and replaced with "
        "configuration-driven milestone content (#837). "
        "Pre-implementation count is 2 — expected to fail until #837 lands."
    )


def test_ac5b_demo_narrated_spec_contains_no_argentina() -> None:
    """AC-5b: 'argentina' is absent from frontend/tests/e2e/demo-narrated.spec.ts (#837).

    Pre-implementation this already passes (count = 0). Test guards against
    regressions introduced during #837 implementation.
    """
    if not _DEMO_NARRATED_SPEC.exists():
        pytest.skip("demo-narrated.spec.ts absent — cannot verify AC-5b")

    content = _DEMO_NARRATED_SPEC.read_text(encoding="utf-8")
    count = len(re.findall(r"argentina", content, re.IGNORECASE))
    assert count == 0, (
        f"'argentina' appears {count} time(s) in demo-narrated.spec.ts — "
        "hardcoded M10/M14 Argentina content must be absent from both script "
        "files per #837 AC-5 (docs/demo/m10/ historical content is excluded "
        "from this check)."
    )


# ---------------------------------------------------------------------------
# AC-6: named solo-use gate present in demo-preparation-standard.md (#951)
#
# Intent doc §4 AC-6:
# grep -ci "solo.use|solo use" docs/process/demo-preparation-standard.md returns ≥1.
# Confirms a named solo-use gate was added — not just any review by any panel
# member without specialist awareness.
# Pre-implementation: "solo" is absent (count = 0).
# ---------------------------------------------------------------------------


def test_ac6a_demo_preparation_standard_exists() -> None:
    """AC-6a: docs/process/demo-preparation-standard.md exists."""
    assert _DEMO_PREP_STANDARD.exists(), (
        "docs/process/demo-preparation-standard.md does not exist — "
        "path may have changed"
    )


def test_ac6b_solo_use_gate_named_in_standard() -> None:
    """AC-6b: 'solo-use' or 'solo use' appears ≥1 time in demo-preparation-standard.md (#951).

    Confirms that PI Agent has added a named solo-use gate to the standard —
    not just a generic 'usability check' that could be performed by any reviewer
    including specialists who apply domain knowledge non-specialists lack.
    Pre-implementation count is 0 — expected to fail until #951 lands.
    """
    if not _DEMO_PREP_STANDARD.exists():
        pytest.skip("demo-preparation-standard.md absent — cannot verify AC-6b")

    content = _DEMO_PREP_STANDARD.read_text(encoding="utf-8")
    count = len(re.findall(r"solo.use|solo use", content, re.IGNORECASE))
    assert count >= 1, (
        f"'solo-use' or 'solo use' appears {count} time(s) in demo-preparation-standard.md — "
        "PI Agent must add a named solo-use gate to §Step 6b (#951). "
        "Pre-implementation count is 0 — expected to fail until #951 lands."
    )


# ---------------------------------------------------------------------------
# AC-7: "[SOLO]" tag convention defined in demo-preparation-standard.md (#951)
#
# Intent doc §4 AC-7:
# grep -c "\[SOLO\]" docs/process/demo-preparation-standard.md returns ≥1.
# Confirms the tag convention is defined so panel reviewers can consistently
# mark solo-use findings for the three-condition blocking criteria check.
# Pre-implementation: "[SOLO]" is absent.
# ---------------------------------------------------------------------------


def test_ac7_solo_tag_defined_in_standard() -> None:
    """AC-7: '[SOLO]' tag appears ≥1 time in demo-preparation-standard.md (#951).

    A Step 6b reviewer designated as solo-use reviewer must know to tag their
    findings '[SOLO]' so that CRITICAL or HIGH solo-use findings trigger the
    same three-condition blocking criteria as all other Step 6b findings.
    Without this tag, solo-use CRITICAL findings could be filed without triggering
    the Step 7 block — a DEMO4-001-class silent failure path.
    Pre-implementation count is 0 — expected to fail until #951 lands.
    """
    if not _DEMO_PREP_STANDARD.exists():
        pytest.skip("demo-preparation-standard.md absent — cannot verify AC-7")

    content = _DEMO_PREP_STANDARD.read_text(encoding="utf-8")
    count = content.count("[SOLO]")
    assert count >= 1, (
        f"'[SOLO]' appears {count} time(s) in demo-preparation-standard.md — "
        "PI Agent must define the [SOLO] tag convention so solo-use reviewer "
        "findings are identifiable and can trigger Step 7 blocking criteria (#951). "
        "Pre-implementation count is 0 — expected to fail until #951 lands."
    )


# ---------------------------------------------------------------------------
# AC-8: "Customer Agent" designated as solo-use reviewer in §Step 6b (#951)
#
# Intent doc §4 AC-8:
# grep -c "Customer Agent" docs/process/demo-preparation-standard.md returns ≥1
# in the §Step 6b context — Customer Agent is named as the solo-use reviewer,
# not left as an anonymous "reviewer" role.
# SF-3 guard: a solo-use gate that does not name the Customer Agent leaves the
# solo-use reviewer role unoccupied — no agent knows they hold the obligation.
# Pre-implementation: "Customer Agent" exists in §Step 6b as a general panel
# member but NOT yet in the context of the solo-use reviewer designation.
# ---------------------------------------------------------------------------


def test_ac8_customer_agent_designated_as_solo_use_reviewer() -> None:
    """AC-8: 'Customer Agent' named as designated solo-use reviewer in §Step 6b (#951).

    SF-3 guard: the solo-use gate could be added (AC-6 passes) and [SOLO] defined
    (AC-7 passes) but the reviewer role could be left anonymous — 'the solo-use
    reviewer' without naming who holds it. This test verifies that 'Customer Agent'
    appears in §Step 6b alongside solo-use language, confirming the designation.

    Note: 'Customer Agent' already appears in the existing §Step 6b panel table
    as the general usability reviewer. This test looks for co-occurrence with solo-use
    language — a stricter check that the Customer Agent role is specifically tied
    to the solo-use gate, not just the general panel.
    """
    if not _DEMO_PREP_STANDARD.exists():
        pytest.skip("demo-preparation-standard.md absent — cannot verify AC-8")

    content = _DEMO_PREP_STANDARD.read_text(encoding="utf-8")

    # Extract the §Step 6b section for context-scoped check
    step_6b = _extract_markdown_section(content, "Step 6b")
    if not step_6b:
        pytest.skip(
            "§Step 6b section not found in demo-preparation-standard.md — "
            "cannot verify Customer Agent designation in context"
        )

    has_customer_agent = "Customer Agent" in step_6b
    has_solo_language = bool(
        re.search(r"solo.use|solo use|\[SOLO\]", step_6b, re.IGNORECASE)
    )

    # SF-3: both must be present in the same section — either alone is insufficient
    assert has_customer_agent and has_solo_language, (
        "§Step 6b does not contain both 'Customer Agent' and solo-use language — "
        f"Customer Agent present: {has_customer_agent}, "
        f"solo-use language present: {has_solo_language}. "
        "PI Agent must designate 'Customer Agent' as the named solo-use reviewer "
        "within §Step 6b so the role is not anonymous (#951). "
        "Pre-implementation: solo-use language is absent — expected to fail until #951 lands."
    )


# ---------------------------------------------------------------------------
# AC-9: legibility metrics artifact exists with thresholds and numeric values (#259)
#
# Intent doc §4 AC-9:
# find docs/standards -name "legibility-baseline-m16.md" exits 0.
# grep -ci "cognitive complexity" ≥1
# grep -ci "function length" ≥1
# grep -ci "test-to-implementation" ≥1
# At least one numeric value per threshold (not blank or TBD).
# SF-4 guard: file exists but values are TBD or blank — no actual measurement.
# Pre-implementation: file does not exist.
# ---------------------------------------------------------------------------


def test_ac9a_legibility_baseline_exists() -> None:
    """AC-9a: docs/standards/legibility-baseline-m16.md exists (#259).

    Pre-implementation: file is absent — expected to fail until #259 lands.
    """
    assert _LEGIBILITY_BASELINE.exists(), (
        "docs/standards/legibility-baseline-m16.md does not exist — "
        "Technical Standards Agent must create the legibility metrics artifact "
        "with Tier 1 threshold values for M16 (#259). "
        "Pre-implementation: file is absent — expected to fail until #259 lands."
    )


def test_ac9b_cognitive_complexity_threshold_present() -> None:
    """AC-9b: 'cognitive complexity' appears ≥1 time in legibility baseline (#259)."""
    if not _LEGIBILITY_BASELINE.exists():
        pytest.skip("legibility-baseline-m16.md absent — AC-9a prerequisite fails")

    content = _LEGIBILITY_BASELINE.read_text(encoding="utf-8")
    count = len(re.findall(r"cognitive complexity", content, re.IGNORECASE))
    assert count >= 1, (
        f"'cognitive complexity' appears {count} time(s) in legibility-baseline-m16.md — "
        "Tier 1 threshold for mean cognitive complexity (green/yellow/red bands) "
        "must be documented (#259)"
    )


def test_ac9c_function_length_threshold_present() -> None:
    """AC-9c: 'function length' appears ≥1 time in legibility baseline (#259)."""
    if not _LEGIBILITY_BASELINE.exists():
        pytest.skip("legibility-baseline-m16.md absent — AC-9a prerequisite fails")

    content = _LEGIBILITY_BASELINE.read_text(encoding="utf-8")
    count = len(re.findall(r"function length", content, re.IGNORECASE))
    assert count >= 1, (
        f"'function length' appears {count} time(s) in legibility-baseline-m16.md — "
        "Tier 1 threshold for p90 function length must be documented (#259)"
    )


def test_ac9d_test_to_implementation_ratio_present() -> None:
    """AC-9d: 'test-to-implementation' appears ≥1 time in legibility baseline (#259)."""
    if not _LEGIBILITY_BASELINE.exists():
        pytest.skip("legibility-baseline-m16.md absent — AC-9a prerequisite fails")

    content = _LEGIBILITY_BASELINE.read_text(encoding="utf-8")
    count = len(re.findall(r"test.to.implementation", content, re.IGNORECASE))
    assert count >= 1, (
        f"'test-to-implementation' appears {count} time(s) in legibility-baseline-m16.md — "
        "Tier 1 threshold for test-to-implementation ratio must be documented (#259)"
    )


def test_ac9e_legibility_baseline_contains_numeric_values() -> None:
    """AC-9e: legibility baseline contains at least one numeric value — not all TBD (#259).

    SF-4 guard: file exists with threshold labels but current-milestone measurement
    cells are blank, 'TBD', or 'N/A' — the artifact looks complete but provides
    no actual measurement data. This test requires at least one number (integer
    or decimal) to be present in the file.
    """
    if not _LEGIBILITY_BASELINE.exists():
        pytest.skip("legibility-baseline-m16.md absent — AC-9a prerequisite fails")

    content = _LEGIBILITY_BASELINE.read_text(encoding="utf-8")

    # Check for any numeric value (integer or decimal) that is not part of a heading
    # and is not a pure year reference (4-digit year alone is not a measurement value)
    numeric_matches = re.findall(r"\b\d+(?:\.\d+)?\b", content)
    # Filter out 4-digit year-like values used only as labels
    non_year_numbers = [n for n in numeric_matches if not re.fullmatch(r"20\d{2}", n)]

    assert len(non_year_numbers) >= 1, (
        "legibility-baseline-m16.md contains no numeric measurement values — "
        "SF-4: threshold labels are present but current-milestone values are absent. "
        "Technical Standards Agent must record actual measured values (not TBD or blank) "
        "alongside each Tier 1 threshold band (#259)."
    )


def test_ac9f_no_tbd_placeholders_for_tier1_values() -> None:
    """AC-9f: Tier 1 measurement rows do not contain bare 'TBD' placeholders (#259).

    SF-4 belt-and-suspenders: a file can contain numeric values in the threshold
    band columns while leaving the current-measurement column as 'TBD'.
    This test flags any remaining TBD values in Tier 1 rows.
    """
    if not _LEGIBILITY_BASELINE.exists():
        pytest.skip("legibility-baseline-m16.md absent — AC-9a prerequisite fails")

    content = _LEGIBILITY_BASELINE.read_text(encoding="utf-8")

    # Count bare TBD occurrences (table cells, not inline prose explanations)
    tbd_count = len(re.findall(r"\bTBD\b", content))

    assert tbd_count == 0, (
        f"'TBD' appears {tbd_count} time(s) in legibility-baseline-m16.md — "
        "all Tier 1 current-milestone measurement cells must have actual values, "
        "not placeholders. Tier 2/3 future-work rows may use 'N/A' or 'see forward note' "
        "but must not use bare TBD (#259)."
    )
