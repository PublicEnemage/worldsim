"""Unit tests for scenario Pydantic schemas — ADR-004 Decision 1.

Key invariants tested:
  - ScenarioCreateRequest rejects empty name
  - n_steps boundary values (0, 1, 100, 101)
  - QuantitySchema.value is str in initial_attributes
  - ScheduledInputSchema step index range
  - ScenarioConfigSchema defaults
  - ScenarioResponse and ScenarioDetailResponse field presence
  - _validate_create_request step range boundary values (Issue #201)
"""
from __future__ import annotations

import pytest
from fastapi import HTTPException

from app.api.scenarios import _validate_create_request, effective_tier
from app.schemas import (
    QuantitySchema,
    ScenarioConfigSchema,
    ScenarioCreateRequest,
    ScenarioDetailResponse,
    ScenarioResponse,
    ScheduledInputSchema,
)

# ---------------------------------------------------------------------------
# ScenarioConfigSchema
# ---------------------------------------------------------------------------


def test_scenario_config_defaults() -> None:
    cfg = ScenarioConfigSchema(entities=["GRC", "DEU"], n_steps=3)
    assert cfg.timestep_label == "annual"
    assert cfg.initial_attributes == {}


def test_scenario_config_entities_list() -> None:
    cfg = ScenarioConfigSchema(entities=["GRC"], n_steps=1)
    assert cfg.entities == ["GRC"]


def test_scenario_config_initial_attributes_quantity_value_is_str() -> None:
    cfg = ScenarioConfigSchema(
        entities=["GRC"],
        n_steps=2,
        initial_attributes={
            "GRC": {
                "gdp_usd_millions": QuantitySchema(
                    value="200000",
                    unit="USD_millions_current",
                    variable_type="FLOW",
                    confidence_tier=2,
                )
            }
        },
    )
    qty = cfg.initial_attributes["GRC"]["gdp_usd_millions"]
    assert isinstance(qty.value, str)
    assert qty.value == "200000"


# ---------------------------------------------------------------------------
# ScenarioCreateRequest — name validation
# ---------------------------------------------------------------------------


def test_create_request_empty_name_is_valid_schema() -> None:
    # Pydantic accepts empty string — rejection happens in endpoint validation
    req = ScenarioCreateRequest(
        name="",
        configuration=ScenarioConfigSchema(entities=["GRC"], n_steps=1),
    )
    assert req.name == ""


def test_create_request_name_set() -> None:
    req = ScenarioCreateRequest(
        name="Greece austerity baseline",
        configuration=ScenarioConfigSchema(entities=["GRC"], n_steps=3),
    )
    assert req.name == "Greece austerity baseline"


def test_create_request_description_optional() -> None:
    req = ScenarioCreateRequest(
        name="Test",
        configuration=ScenarioConfigSchema(entities=["GRC"], n_steps=1),
    )
    assert req.description is None


# ---------------------------------------------------------------------------
# n_steps boundary values
# ---------------------------------------------------------------------------


def test_n_steps_minimum_valid() -> None:
    cfg = ScenarioConfigSchema(entities=["GRC"], n_steps=1)
    assert cfg.n_steps == 1


def test_n_steps_maximum_valid() -> None:
    cfg = ScenarioConfigSchema(entities=["GRC"], n_steps=100)
    assert cfg.n_steps == 100


def test_n_steps_zero_accepted_by_schema() -> None:
    # Pydantic doesn't enforce 1–100; that's endpoint validation
    cfg = ScenarioConfigSchema(entities=["GRC"], n_steps=0)
    assert cfg.n_steps == 0


def test_n_steps_101_accepted_by_schema() -> None:
    cfg = ScenarioConfigSchema(entities=["GRC"], n_steps=101)
    assert cfg.n_steps == 101


# ---------------------------------------------------------------------------
# ScheduledInputSchema
# ---------------------------------------------------------------------------


def test_scheduled_input_fields() -> None:
    si = ScheduledInputSchema(
        step=2,
        input_type="FiscalPolicyInput",
        input_data={"instrument": "SPENDING_CHANGE", "value": "-0.05"},
    )
    assert si.step == 2
    assert si.input_type == "FiscalPolicyInput"
    assert si.input_data["value"] == "-0.05"


def test_create_request_scheduled_inputs_default_empty() -> None:
    req = ScenarioCreateRequest(
        name="Test",
        configuration=ScenarioConfigSchema(entities=["GRC"], n_steps=5),
    )
    assert req.scheduled_inputs == []


def test_create_request_with_scheduled_inputs() -> None:
    req = ScenarioCreateRequest(
        name="Test",
        configuration=ScenarioConfigSchema(entities=["GRC"], n_steps=3),
        scheduled_inputs=[
            ScheduledInputSchema(
                step=0,
                input_type="EmergencyPolicyInput",
                input_data={"instrument": "IMF_PROGRAM_ACCEPTANCE"},
            ),
        ],
    )
    assert len(req.scheduled_inputs) == 1
    assert req.scheduled_inputs[0].step == 0


# ---------------------------------------------------------------------------
# ScenarioResponse
# ---------------------------------------------------------------------------


def test_scenario_response_fields() -> None:
    resp = ScenarioResponse(
        scenario_id="abc-123",
        name="Test scenario",
        description=None,
        status="pending",
        version=1,
        created_at="2026-04-23T10:00:00+00:00",
    )
    assert resp.scenario_id == "abc-123"
    assert resp.status == "pending"
    assert resp.version == 1
    assert resp.description is None


def test_scenario_response_with_description() -> None:
    resp = ScenarioResponse(
        scenario_id="x",
        name="n",
        description="Some description",
        status="completed",
        version=2,
        created_at="2026-04-23T10:00:00+00:00",
    )
    assert resp.description == "Some description"


# ---------------------------------------------------------------------------
# ScenarioDetailResponse
# ---------------------------------------------------------------------------


def test_scenario_detail_response_fields() -> None:
    from app.schemas import build_temporal_scope_note

    detail = ScenarioDetailResponse(
        scenario_id="abc",
        name="Greece test",
        description=None,
        status="pending",
        version=1,
        created_at="2026-04-23T10:00:00+00:00",
        configuration=ScenarioConfigSchema(entities=["GRC"], n_steps=3),
        scheduled_inputs=[],
        temporal_scope_note=build_temporal_scope_note(3, "annual", None),
    )
    assert detail.configuration.entities == ["GRC"]
    assert detail.configuration.n_steps == 3
    assert detail.scheduled_inputs == []
    assert "3 annual" in detail.temporal_scope_note
    assert "intergenerational" in detail.temporal_scope_note


def test_scenario_detail_response_with_inputs() -> None:
    from app.schemas import build_temporal_scope_note

    detail = ScenarioDetailResponse(
        scenario_id="abc",
        name="Test",
        description=None,
        status="pending",
        version=1,
        created_at="2026-04-23T10:00:00+00:00",
        configuration=ScenarioConfigSchema(entities=["GRC"], n_steps=2),
        scheduled_inputs=[
            ScheduledInputSchema(
                step=0,
                input_type="FiscalPolicyInput",
                input_data={"k": "v"},
            )
        ],
        temporal_scope_note=build_temporal_scope_note(2, "annual", "2010-01-01"),
    )
    assert len(detail.scheduled_inputs) == 1
    assert detail.scheduled_inputs[0].input_type == "FiscalPolicyInput"


# ---------------------------------------------------------------------------
# effective_tier — horizon degradation (Issue #69)
# ---------------------------------------------------------------------------



def test_effective_tier_step_zero_no_degradation() -> None:
    assert effective_tier(1, 0) == 1


def test_effective_tier_step_4_no_degradation() -> None:
    # floor(4/5) = 0 — degradation only starts at step 5
    assert effective_tier(1, 4) == 1


def test_effective_tier_step_5_degrades_by_one() -> None:
    assert effective_tier(1, 5) == 2


def test_effective_tier_step_10_degrades_by_two() -> None:
    assert effective_tier(1, 10) == 3


def test_effective_tier_higher_source_step_5() -> None:
    assert effective_tier(3, 5) == 4


def test_effective_tier_capped_at_5() -> None:
    assert effective_tier(5, 100) == 5


def test_effective_tier_cap_prevents_exceeding_5() -> None:
    # tier 4 + floor(10/5)=2 would be 6 without cap
    assert effective_tier(4, 10) == 5


def test_effective_tier_boundary_step_9() -> None:
    # floor(9/5) = 1 — one degradation step
    assert effective_tier(1, 9) == 2


# ---------------------------------------------------------------------------
# _validate_create_request — step range boundary tests (Issue #201)
#
# The valid range for scheduled_input step is [0, n_steps] inclusive.
# Step k injects inputs during the advance from step k-1 → step k.
# Step 0 = initial state; step n_steps = last advance.
#
# These tests guard against the off-by-one that was silently present before
# commit 89a2c5e (step > n-1 → step > n). Greece never caught it because its
# highest input step was n_steps - 1. Argentina's step == n_steps exposed it.
# ---------------------------------------------------------------------------


def _req(n_steps: int, steps: list[int]) -> ScenarioCreateRequest:
    """Build a minimal ScenarioCreateRequest with the given step values."""
    return ScenarioCreateRequest(
        name="Boundary test",
        configuration=ScenarioConfigSchema(entities=["GRC"], n_steps=n_steps),
        scheduled_inputs=[
            ScheduledInputSchema(
                step=s,
                input_type="FiscalPolicyInput",
                input_data={"instrument": "spending_change", "value": "-0.05"},
            )
            for s in steps
        ],
    )


def test_step_zero_is_accepted() -> None:
    """step == 0 (initial state injection) must not raise."""
    _validate_create_request(_req(n_steps=3, steps=[0]))


def test_step_n_steps_is_accepted() -> None:
    """step == n_steps (last advance injection) must not raise — regression for Issue #201."""
    _validate_create_request(_req(n_steps=3, steps=[3]))


def test_step_n_steps_minus_one_is_accepted() -> None:
    """step == n_steps - 1 is squarely within range — always was accepted."""
    _validate_create_request(_req(n_steps=3, steps=[2]))


def test_step_n_steps_plus_one_is_rejected() -> None:
    """step == n_steps + 1 is out of range — must raise 422."""
    with pytest.raises(HTTPException) as exc_info:
        _validate_create_request(_req(n_steps=3, steps=[4]))
    assert exc_info.value.status_code == 422
    assert "4" in str(exc_info.value.detail)


def test_step_negative_one_is_rejected() -> None:
    """step == -1 is below valid range — must raise 422."""
    with pytest.raises(HTTPException) as exc_info:
        _validate_create_request(_req(n_steps=3, steps=[-1]))
    assert exc_info.value.status_code == 422
    assert "-1" in str(exc_info.value.detail)


def test_empty_scheduled_inputs_accepted() -> None:
    """Empty scheduled_inputs with valid n_steps must not raise."""
    _validate_create_request(_req(n_steps=5, steps=[]))


def test_argentina_case_step_equals_n_steps_accepted() -> None:
    """Regression: n_steps=2, step=2 — the Argentina fixture that exposed the bug."""
    _validate_create_request(_req(n_steps=2, steps=[2]))


def test_all_valid_steps_accepted() -> None:
    """All steps in [0, n_steps] simultaneously must not raise."""
    _validate_create_request(_req(n_steps=3, steps=[0, 1, 2, 3]))


def test_mixed_valid_and_invalid_steps_rejected() -> None:
    """When any step is out of range the whole request must be rejected (422)."""
    with pytest.raises(HTTPException) as exc_info:
        _validate_create_request(_req(n_steps=3, steps=[1, 4]))
    assert exc_info.value.status_code == 422


def test_invalid_step_error_lists_out_of_range_values() -> None:
    """The 422 detail must include the out-of-range step values for diagnostics."""
    with pytest.raises(HTTPException) as exc_info:
        _validate_create_request(_req(n_steps=3, steps=[-1, 5]))
    detail = str(exc_info.value.detail)
    assert "-1" in detail
    assert "5" in detail


def test_empty_name_rejected() -> None:
    """_validate_create_request rejects an empty or whitespace-only name."""
    req = ScenarioCreateRequest(
        name="   ",
        configuration=ScenarioConfigSchema(entities=["GRC"], n_steps=3),
    )
    with pytest.raises(HTTPException) as exc_info:
        _validate_create_request(req)
    assert exc_info.value.status_code == 422


def test_n_steps_zero_rejected() -> None:
    """n_steps=0 is below the valid 1–100 range — must raise 422."""
    req = ScenarioCreateRequest(
        name="Test",
        configuration=ScenarioConfigSchema(entities=["GRC"], n_steps=0),
    )
    with pytest.raises(HTTPException) as exc_info:
        _validate_create_request(req)
    assert exc_info.value.status_code == 422


def test_n_steps_101_rejected() -> None:
    """n_steps=101 is above the valid 1–100 range — must raise 422."""
    req = ScenarioCreateRequest(
        name="Test",
        configuration=ScenarioConfigSchema(entities=["GRC"], n_steps=101),
    )
    with pytest.raises(HTTPException) as exc_info:
        _validate_create_request(req)
    assert exc_info.value.status_code == 422
