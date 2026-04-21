"""Unit tests for TerritorialValidator — ADR-003 Decision 4.

All five POLICY.md territorial positions are covered:
  TWN — Taiwan prohibited names
  PSE — Palestine prohibited codes
  XKX — Kosovo prohibited codes
  ESH — Western Sahara prohibited codes
  CRIMEA — Crimea as top-level country entity

Tests are pure Python; no database connection required.
"""
from __future__ import annotations

import pytest

from app.db.territorial_validator import TerritorialValidationError, TerritorialValidator


@pytest.fixture()
def validator() -> TerritorialValidator:
    return TerritorialValidator()


# ---------------------------------------------------------------------------
# Clean data — must pass all checks
# ---------------------------------------------------------------------------


def test_clean_us_feature_passes(validator: TerritorialValidator) -> None:
    props = {"NAME": "United States of America", "ISO_A3": "USA", "ADM0_A3": "USA"}
    assert validator.validate_entity("USA", props) == []


def test_clean_taiwan_acceptable_name_passes(validator: TerritorialValidator) -> None:
    props = {"NAME": "Taiwan", "ISO_A3": "TWN", "ADM0_A3": "TWN"}
    assert validator.validate_entity("TWN", props) == []


def test_clean_palestine_pse_code_passes(validator: TerritorialValidator) -> None:
    props = {"NAME": "Palestine", "ISO_A3": "PSE", "ADM0_A3": "PSE"}
    assert validator.validate_entity("PSE", props) == []


def test_clean_kosovo_xkx_code_passes(validator: TerritorialValidator) -> None:
    props = {"NAME": "Kosovo", "ISO_A3": "-99", "ADM0_A3": "XKX"}
    assert validator.validate_entity("XKX", props) == []


def test_clean_western_sahara_esh_code_passes(validator: TerritorialValidator) -> None:
    props = {"NAME": "Western Sahara", "ISO_A3": "ESH", "ADM0_A3": "ESH"}
    assert validator.validate_entity("ESH", props) == []


def test_clean_ukraine_with_subnational_passes(validator: TerritorialValidator) -> None:
    props = {"NAME": "Ukraine", "ISO_A3": "UKR", "ADM0_A3": "UKR"}
    assert validator.validate_entity("UKR", props) == []


# ---------------------------------------------------------------------------
# TWN — Taiwan
# ---------------------------------------------------------------------------


def test_taiwan_province_of_china_blocked(validator: TerritorialValidator) -> None:
    props = {"NAME": "Taiwan, Province of China", "ISO_A3": "TWN"}
    errors = validator.validate_entity("TWN", props)
    assert len(errors) == 1
    assert "[TWN]" in errors[0]
    assert "Taiwan, Province of China" in errors[0]


def test_taiwan_chinese_taipei_blocked(validator: TerritorialValidator) -> None:
    props = {"NAME": "Chinese Taipei", "ISO_A3": "TWN"}
    errors = validator.validate_entity("TWN", props)
    assert len(errors) == 1
    assert "[TWN]" in errors[0]
    assert "Chinese Taipei" in errors[0]


def test_taiwan_formosa_blocked(validator: TerritorialValidator) -> None:
    props = {"NAME": "Formosa", "ISO_A3": "TWN"}
    errors = validator.validate_entity("TWN", props)
    assert len(errors) == 1
    assert "[TWN]" in errors[0]


def test_taiwan_prohibited_name_in_long_name_field_blocked(validator: TerritorialValidator) -> None:
    props = {
        "NAME": "Taiwan",
        "NAME_LONG": "Taiwan, Province of China",
        "ISO_A3": "TWN",
    }
    errors = validator.validate_entity("TWN", props)
    assert len(errors) == 1


def test_taiwan_check_only_fires_for_twn(validator: TerritorialValidator) -> None:
    props = {"NAME": "Taiwan, Province of China"}
    errors = validator.validate_entity("CHN", props)
    assert errors == []


# ---------------------------------------------------------------------------
# PSE — Palestine
# ---------------------------------------------------------------------------


def test_palestine_isr_code_blocked(validator: TerritorialValidator) -> None:
    props = {"NAME": "Palestine", "ISO_A3": "ISR"}
    errors = validator.validate_entity("PSE", props)
    assert len(errors) == 1
    assert "[PSE]" in errors[0]
    assert "ISR" in errors[0]


def test_palestine_il_alpha2_code_blocked(validator: TerritorialValidator) -> None:
    props = {"NAME": "Palestine", "ADM0_A3": "IL"}
    errors = validator.validate_entity("PSE", props)
    assert len(errors) == 1
    assert "[PSE]" in errors[0]


def test_palestine_check_only_fires_for_pse(validator: TerritorialValidator) -> None:
    props = {"NAME": "Israel", "ISO_A3": "ISR"}
    errors = validator.validate_entity("ISR", props)
    assert errors == []


def test_palestine_with_correct_pse_code_passes(validator: TerritorialValidator) -> None:
    props = {"NAME": "Palestine", "ISO_A3": "PSE", "ADM0_A3": "PSE"}
    assert validator.validate_entity("PSE", props) == []


# ---------------------------------------------------------------------------
# XKX — Kosovo
# ---------------------------------------------------------------------------


def test_kosovo_srb_code_blocked(validator: TerritorialValidator) -> None:
    props = {"NAME": "Kosovo", "ISO_A3": "-99", "ADM0_A3": "SRB"}
    errors = validator.validate_entity("XKX", props)
    assert len(errors) == 1
    assert "[XKX]" in errors[0]
    assert "SRB" in errors[0]


def test_kosovo_rs_alpha2_code_blocked(validator: TerritorialValidator) -> None:
    props = {"NAME": "Kosovo", "ADM0_A3": "RS"}
    errors = validator.validate_entity("XKX", props)
    assert len(errors) == 1
    assert "[XKX]" in errors[0]


def test_kosovo_check_only_fires_for_xkx(validator: TerritorialValidator) -> None:
    props = {"NAME": "Serbia", "ISO_A3": "SRB"}
    errors = validator.validate_entity("SRB", props)
    assert errors == []


# ---------------------------------------------------------------------------
# ESH — Western Sahara
# ---------------------------------------------------------------------------


def test_western_sahara_mar_code_blocked(validator: TerritorialValidator) -> None:
    props = {"NAME": "Western Sahara", "ISO_A3": "MAR"}
    errors = validator.validate_entity("ESH", props)
    assert len(errors) == 1
    assert "[ESH]" in errors[0]
    assert "MAR" in errors[0]


def test_western_sahara_ma_alpha2_code_blocked(validator: TerritorialValidator) -> None:
    props = {"NAME": "Western Sahara", "ADM0_A3": "MA"}
    errors = validator.validate_entity("ESH", props)
    assert len(errors) == 1
    assert "[ESH]" in errors[0]


def test_western_sahara_check_only_fires_for_esh(validator: TerritorialValidator) -> None:
    props = {"NAME": "Morocco", "ISO_A3": "MAR"}
    errors = validator.validate_entity("MAR", props)
    assert errors == []


# ---------------------------------------------------------------------------
# CRIMEA
# ---------------------------------------------------------------------------


def test_crimea_as_top_level_entity_blocked(validator: TerritorialValidator) -> None:
    props = {"NAME": "Crimea", "ISO_A3": "-99"}
    errors = validator.validate_entity("CRM", props)
    assert len(errors) == 1
    assert "[CRIMEA]" in errors[0]


def test_republic_of_crimea_blocked(validator: TerritorialValidator) -> None:
    props = {"NAME": "Republic of Crimea"}
    errors = validator.validate_entity("CRM", props)
    assert len(errors) == 1
    assert "[CRIMEA]" in errors[0]


def test_autonomous_republic_of_crimea_blocked(validator: TerritorialValidator) -> None:
    props = {"NAME": "Autonomous Republic of Crimea"}
    errors = validator.validate_entity("UA43", props)
    assert len(errors) == 1
    assert "[CRIMEA]" in errors[0]


def test_crimea_check_fires_regardless_of_entity_id(validator: TerritorialValidator) -> None:
    """Crimea check is name-based, not code-based — fires for any entity_id."""
    props = {"NAME": "Crimea"}
    errors = validator.validate_entity("UKR", props)
    assert len(errors) == 1


# ---------------------------------------------------------------------------
# validate_all — batch behaviour
# ---------------------------------------------------------------------------


def test_validate_all_clean_batch_passes(validator: TerritorialValidator) -> None:
    entities = [
        ("USA", {"NAME": "United States of America", "ISO_A3": "USA"}),
        ("TWN", {"NAME": "Taiwan", "ISO_A3": "TWN"}),
        ("PSE", {"NAME": "Palestine", "ISO_A3": "PSE"}),
        ("XKX", {"NAME": "Kosovo", "ISO_A3": "-99", "ADM0_A3": "XKX"}),
        ("ESH", {"NAME": "Western Sahara", "ISO_A3": "ESH"}),
        ("UKR", {"NAME": "Ukraine", "ISO_A3": "UKR"}),
    ]
    validator.validate_all(entities)  # must not raise


def test_validate_all_single_violation_raises(validator: TerritorialValidator) -> None:
    entities = [
        ("USA", {"NAME": "United States of America", "ISO_A3": "USA"}),
        ("TWN", {"NAME": "Taiwan, Province of China", "ISO_A3": "TWN"}),
    ]
    with pytest.raises(TerritorialValidationError) as exc_info:
        validator.validate_all(entities)
    assert "[TWN]" in str(exc_info.value)
    assert "no records written" in str(exc_info.value).lower()


def test_validate_all_multiple_violations_collected(validator: TerritorialValidator) -> None:
    entities = [
        ("TWN", {"NAME": "Taiwan, Province of China", "ISO_A3": "TWN"}),
        ("PSE", {"NAME": "Palestine", "ISO_A3": "ISR"}),
        ("ESH", {"NAME": "Western Sahara", "ISO_A3": "MAR"}),
    ]
    with pytest.raises(TerritorialValidationError) as exc_info:
        validator.validate_all(entities)
    msg = str(exc_info.value)
    assert "[TWN]" in msg
    assert "[PSE]" in msg
    assert "[ESH]" in msg
    assert "3 territorial validation violation(s)" in msg


def test_validate_all_empty_batch_passes(validator: TerritorialValidator) -> None:
    validator.validate_all([])  # must not raise


def test_validate_all_halts_pipeline_message(validator: TerritorialValidator) -> None:
    entities = [("TWN", {"NAME": "Chinese Taipei", "ISO_A3": "TWN"})]
    with pytest.raises(TerritorialValidationError) as exc_info:
        validator.validate_all(entities)
    assert "Pipeline halted" in str(exc_info.value)
    assert "POLICY.md" in str(exc_info.value)
