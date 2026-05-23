"""Fixture CI gate — step_event_label schema validation (AC-012).

Validates that any step_metadata in scenario fixtures conforms to the
≤ 8 words AND ≤ 32 characters constraint (FA brief Decision C, ADR-010 Decision 7).

Background:
    step_metadata is stored as a JSONB key in scenarios.configuration per FA brief
    §Decision C. Structure:
        {
          "step_metadata": {
            "1": {"step_event_label": "...", "step_significance": "SIGNIFICANT"},
            "3": {"step_event_label": "...", "step_significance": "SIGNIFICANT"}
          }
        }
    Absence of a key means ROUTINE. Only SIGNIFICANT and ROUTINE are valid values.
    'STANDARD' is incorrect (Arch-F1 correction — ADR-010 Decision 7 is authoritative).

The Greece fixture currently has NO step_metadata. That is expected and correct:
    - The loop body in test_greece_fixture_step_metadata_conforms never executes.
    - The validator unit tests pass immediately (they test the validator logic directly).
    - When step_metadata is added to the Greece fixture, these tests will enforce
      the constraints and reject violations.

Run as:
    pytest tests/fixtures/test_greece_fixture_step_metadata.py -v

CI integration:
    This test runs as part of pytest tests/fixtures/ on every PR (QA-F6).
    It is a CI gate: any scenario fixture whose SIGNIFICANT step labels exceed
    8 words or 32 characters must fail CI before reaching the UI render layer.

Sources:
    docs/frontend/fa-brief-m9-instrument-cluster.md §Mode 1 Step Axis Annotation (FA-C5)
    docs/frontend/fa-brief-m9-instrument-cluster.md §Named Acceptance Criteria (AC-012)
    docs/frontend/fa-brief-m9-instrument-cluster.md §Decision C (step_metadata JSONB)
    docs/ux/user-stories-instrument-cluster-m9.md US-005 (step annotation)
"""
from __future__ import annotations

# ---------------------------------------------------------------------------
# Validator functions — these are the fixture CI gate logic.
# When the backend trajectory endpoint is implemented, these constraints must
# also be enforced server-side. The CI gate catches violations at fixture
# authoring time, not at runtime.
# ---------------------------------------------------------------------------


def validate_step_event_label(label: str) -> list[str]:
    """Validate a step_event_label against the FA-C5 constraints.

    Constraints (FA brief §Mode 1 Step Axis Annotation — binding):
        - ≤ 32 characters (including spaces)
        - ≤ 8 words

    Both constraints must hold. Either violation alone is a CI failure.

    At 480px trajectory view width / 6 steps / 11px font (6px/char average):
        32 chars ≈ 192px — wraps into 2–3 lines at 80px tick cell width.
        8 words ≈ 8 × avg_word_length — the word constraint catches labels
        that are short in chars but long in word count.

    Args:
        label: The step_event_label string from the fixture step_metadata.

    Returns:
        A list of violation strings. Empty list = valid. Callers must assert
        not violations, which produces a useful assertion message including
        the violation description.
    """
    violations: list[str] = []

    if len(label) > 32:
        violations.append(
            f"label exceeds 32 characters: {len(label)} chars in '{label}'"
        )

    word_count = len(label.split())
    if word_count > 8:
        violations.append(
            f"label exceeds 8 words: {word_count} words in '{label}'"
        )

    return violations


def validate_step_significance(value: str) -> bool:
    """Validate a step_significance value.

    Per ADR-010 Decision 7 (authoritative) and FA brief Arch-F1 correction:
        Valid values: "SIGNIFICANT" | "ROUTINE"
        Invalid value: "STANDARD" — this is the Arch-F1 corrected term.
        "STANDARD" was used in early FA brief drafts; ADR-010 Decision 7
        defines "ROUTINE" as the correct value.

    Args:
        value: The step_significance string from the fixture step_metadata.

    Returns:
        True if valid, False if invalid.
    """
    return value in ("SIGNIFICANT", "ROUTINE")


# ---------------------------------------------------------------------------
# Fixture tests — these run against the actual scenario fixture objects.
# ---------------------------------------------------------------------------


def test_greece_fixture_step_metadata_conforms() -> None:
    """Greece fixture step_metadata (if present) must pass label and significance validation.

    The Greece fixture currently has no step_metadata. When step_metadata is added
    (as part of implementing Mode 1 step annotations per AC-011), this test will
    enforce the constraints on every SIGNIFICANT step label.

    Expected behavior:
        - With no step_metadata: loop body never executes; test passes trivially.
        - With step_metadata: every label must satisfy both constraints; every
          significance value must be SIGNIFICANT or ROUTINE (never STANDARD).

    This is the pre-implementation gate: the test passes now, will continue to
    pass for compliant fixtures, and will fail CI for any fixture that violates
    the constraints.
    """
    from tests.fixtures.greece_2010_scenario import build_greece_scenario

    scenario = build_greece_scenario()
    scenario_config = scenario.configuration.model_dump(mode="json")

    # Navigate to step_metadata inside the configuration JSONB.
    # Per FA brief §Decision C: key is "step_metadata" at the top level of
    # the configuration dict. Absence is valid (no step_metadata yet).
    step_metadata: dict[str, dict[str, str | None]] = scenario_config.get(
        "step_metadata", {}
    )

    # This loop is currently a no-op because the Greece fixture has no step_metadata.
    # It will enforce the constraints once step_metadata is added.
    for step_key, meta in step_metadata.items():
        label: str | None = meta.get("step_event_label")
        significance: str | None = meta.get("step_significance")

        if label is not None:
            violations = validate_step_event_label(label)
            assert not violations, (
                f"Step {step_key} step_event_label violation: {violations}"
            )

        if significance is not None:
            assert validate_step_significance(significance), (
                f"Step {step_key}: invalid step_significance '{significance}' — "
                f"must be 'SIGNIFICANT' or 'ROUTINE' per ADR-010 Decision 7. "
                f"'STANDARD' is the incorrect term (Arch-F1 correction)."
            )


# ---------------------------------------------------------------------------
# Validator unit tests — these test the validator logic directly.
# These pass immediately regardless of fixture state.
# ---------------------------------------------------------------------------


def test_step_event_label_validator_accepts_valid_short_label() -> None:
    """Validator accepts labels that are within both constraints."""
    # Valid: 4 words, 25 chars
    violations = validate_step_event_label("IMF programme begins")
    assert not violations, f"Unexpected violations: {violations}"


def test_step_event_label_validator_accepts_label_at_32_char_boundary() -> None:
    """Validator accepts a label that is exactly 32 characters."""
    # "Capital controls imposed 2015" is 29 chars — within limit
    label_32 = "A" * 32
    violations = validate_step_event_label(label_32)
    # A single 32-char word is valid for char count but: 1 word <= 8 words.
    # However, 32 'A' chars is valid. Assert no char-count violation.
    char_violations = [v for v in violations if "32 characters" in v]
    assert not char_violations, f"32-char label should pass char check: {char_violations}"


def test_step_event_label_validator_rejects_overlong_chars() -> None:
    """Validator correctly rejects labels that exceed 32 characters.

    The canonical over-length label from FA brief §Mode 1 Step Axis Annotation:
    'Structural adjustment programme second phase announced' would exceed 32 chars.
    """
    # 58 characters — well over the 32-character limit
    long_label = "Structural adjustment programme second phase begins announced"
    violations = validate_step_event_label(long_label)
    assert any("32 characters" in v for v in violations), (
        f"Expected a '32 characters' violation but got: {violations}"
    )


def test_step_event_label_validator_rejects_too_many_words() -> None:
    """Validator correctly rejects labels with more than 8 words.

    Nine words is invalid per FA brief §Mode 1 Step Axis Annotation.
    """
    nine_word_label = "one two three four five six seven eight nine"
    violations = validate_step_event_label(nine_word_label)
    assert any("8 words" in v for v in violations), (
        f"Expected an '8 words' violation but got: {violations}"
    )


def test_step_event_label_validator_rejects_exactly_nine_words() -> None:
    """Labels with exactly 9 words are invalid (> 8 words threshold)."""
    # 9 short words — might be under 32 chars but over 8 words
    nine_word_short = "a b c d e f g h i"
    violations = validate_step_event_label(nine_word_short)
    word_violations = [v for v in violations if "8 words" in v]
    assert word_violations, (
        f"9-word label should produce a word-count violation: {violations}"
    )


def test_step_event_label_validator_accepts_exactly_eight_words() -> None:
    """Labels with exactly 8 words are valid (at the word limit, not over)."""
    eight_word_label = "a b c d e f g h"
    violations = validate_step_event_label(eight_word_label)
    word_violations = [v for v in violations if "8 words" in v]
    assert not word_violations, (
        f"8-word label should not produce a word-count violation: {violations}"
    )


def test_step_significance_accepts_significant() -> None:
    """SIGNIFICANT is a valid step_significance value."""
    assert validate_step_significance("SIGNIFICANT"), (
        "'SIGNIFICANT' must be accepted as a valid step_significance value."
    )


def test_step_significance_accepts_routine() -> None:
    """ROUTINE is a valid step_significance value."""
    assert validate_step_significance("ROUTINE"), (
        "'ROUTINE' must be accepted as a valid step_significance value."
    )


def test_step_significance_rejects_standard() -> None:
    """'STANDARD' is the incorrect value and must be rejected.

    'STANDARD' was used in early FA brief drafts. ADR-010 Decision 7 defines
    'ROUTINE' as the correct value. Arch-F1 corrected the brief. The fixture
    CI gate enforces the ADR-authoritative term.
    """
    assert not validate_step_significance("STANDARD"), (
        "'STANDARD' must be rejected — the correct term is 'ROUTINE' per "
        "ADR-010 Decision 7 (Arch-F1 correction)."
    )


def test_step_significance_rejects_lowercase() -> None:
    """Lowercase variants are invalid — values must match exactly."""
    assert not validate_step_significance("significant")
    assert not validate_step_significance("routine")
    assert not validate_step_significance("standard")


def test_step_significance_rejects_empty_string() -> None:
    """Empty string is not a valid step_significance value."""
    assert not validate_step_significance("")


def test_step_significance_rejects_arbitrary_string() -> None:
    """Arbitrary strings are invalid step_significance values."""
    assert not validate_step_significance("MAJOR")
    assert not validate_step_significance("KEY")
    assert not validate_step_significance("IMPORTANT")
