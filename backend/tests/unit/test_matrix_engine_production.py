"""
ADR-009 §Decision 1 Production Migration — unit tests (Issue #749, G4).

Verifies that:
  - The engine package `propagate` export points to propagate_matrix (not propagate iterative)
  - ScenarioRunner.tick() calls propagate_matrix, not propagate (iterative)
  - A single step advance via ScenarioRunner produces valid State[T+1] (smoke test)
  - No silent fallback — if propagate_matrix raises, the exception propagates

These are structural tests that guard the migration invariant. Correctness of
propagate_matrix itself is covered by test_equivalence_harness.py.
"""
from __future__ import annotations

from datetime import datetime, timedelta
from decimal import Decimal

import pytest

from app.simulation.engine.matrix_propagation import propagate_matrix
from app.simulation.engine.models import (
    ResolutionConfig,
    ScenarioConfig,
    SimulationEntity,
    SimulationModule,
    SimulationState,
)
from app.simulation.engine.quantity import Quantity, VariableType
from app.simulation.orchestration import AuditLog, ScenarioRunner

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_BASE_DATE = datetime(2010, 1, 1)
_STEP_DELTA = timedelta(days=365)


def _q(value: float) -> Quantity:
    return Quantity(
        value=Decimal(str(value)),
        unit="dimensionless",
        variable_type=VariableType.RATIO,
    )


def _make_state(entity_id: str = "GRC", **attrs: float) -> SimulationState:
    return SimulationState(
        entities={
            entity_id: SimulationEntity(
                id=entity_id,
                entity_type="country",
                attributes={k: _q(v) for k, v in attrs.items()},
                metadata={},
            )
        },
        relationships=[],
        events=[],
        timestep=_BASE_DATE,
        scenario_config=ScenarioConfig(
            scenario_id="test-g4",
            name="G4 test",
            description="",
            start_date=_BASE_DATE,
            end_date=_BASE_DATE + _STEP_DELTA * 5,
        ),
        resolution=ResolutionConfig(),
    )


# ---------------------------------------------------------------------------
# 1. Engine package `propagate` export is propagate_matrix
# ---------------------------------------------------------------------------


def test_engine_package_propagate_is_matrix_engine() -> None:
    """engine.__init__.propagate must be propagate_matrix after G4 migration."""
    from app.simulation.engine import propagate  # noqa: PLC0415
    assert propagate is propagate_matrix, (
        "engine.propagate is not propagate_matrix — call site was not swapped "
        "(ADR-009 §Decision 1 production migration not complete)"
    )


# ---------------------------------------------------------------------------
# 2. ScenarioRunner.tick() uses propagate_matrix (not iterative propagate)
# ---------------------------------------------------------------------------


class _NullModule(SimulationModule):
    def compute(  # type: ignore[override]
        self,
        entity: SimulationEntity,
        state: SimulationState,
        timestep: datetime,
    ) -> list:
        return []

    def get_subscribed_events(self) -> list[str]:
        return []


def test_runner_tick_uses_matrix_engine_via_exception(monkeypatch: pytest.MonkeyPatch) -> None:
    """Verify ScenarioRunner.advance_timestep() calls propagate_matrix, not iterative."""
    import app.simulation.engine.matrix_propagation as matrix_mod  # noqa: PLC0415

    call_count = [0]
    original = propagate_matrix

    def _spy(state: SimulationState, events: list) -> SimulationState:
        call_count[0] += 1
        return original(state, events)

    monkeypatch.setattr(matrix_mod, "propagate_matrix", _spy)

    state = _make_state(gdp_growth=0.02)
    modules = [_NullModule()]
    runner = ScenarioRunner(
        initial_state=state,
        scheduled_inputs=[],
        modules=modules,
        n_steps=1,
        session_id="test-spy",
        timestep_delta=_STEP_DELTA,
        audit_log=AuditLog(),
    )
    runner.advance_timestep(current_state=state, modules=modules, scheduled_inputs=[])

    assert call_count[0] == 1, (
        "propagate_matrix was not called by advance_timestep() — "
        "iterative engine may still be the call site"
    )


# ---------------------------------------------------------------------------
# 3. Smoke test — advance_timestep() produces a valid State[T+1]
# ---------------------------------------------------------------------------


def test_runner_tick_advances_timestep() -> None:
    """ScenarioRunner.advance_timestep() must advance timestep by exactly one step delta."""
    state = _make_state(gdp_growth=0.02)
    modules = [_NullModule()]
    runner = ScenarioRunner(
        initial_state=state,
        scheduled_inputs=[],
        modules=modules,
        n_steps=1,
        session_id="test-smoke",
        timestep_delta=_STEP_DELTA,
        audit_log=AuditLog(),
    )
    next_state = runner.advance_timestep(
        current_state=state, modules=modules, scheduled_inputs=[]
    )
    expected_ts = _BASE_DATE + _STEP_DELTA
    assert next_state.timestep == expected_ts


def test_runner_tick_preserves_entities() -> None:
    """State[T+1] must contain the same entities as State[T] (no entity loss)."""
    state = _make_state("GRC", gdp_growth=0.02, unemployment_rate=0.12)
    modules = [_NullModule()]
    runner = ScenarioRunner(
        initial_state=state,
        scheduled_inputs=[],
        modules=modules,
        n_steps=1,
        session_id="test-preserve",
        timestep_delta=_STEP_DELTA,
        audit_log=AuditLog(),
    )
    next_state = runner.advance_timestep(
        current_state=state, modules=modules, scheduled_inputs=[]
    )
    assert "GRC" in next_state.entities


def test_runner_tick_no_event_produces_unchanged_attributes() -> None:
    """When no events are generated, entity attributes must be unchanged at T+1."""
    state = _make_state("GRC", gdp_growth=0.02)
    modules = [_NullModule()]
    runner = ScenarioRunner(
        initial_state=state,
        scheduled_inputs=[],
        modules=modules,
        n_steps=1,
        session_id="test-nochange",
        timestep_delta=_STEP_DELTA,
        audit_log=AuditLog(),
    )
    next_state = runner.advance_timestep(
        current_state=state, modules=modules, scheduled_inputs=[]
    )
    grc_t1 = next_state.entities["GRC"]
    assert grc_t1.attributes["gdp_growth"].value == Decimal("0.02")


# ---------------------------------------------------------------------------
# 4. No silent fallback — propagate_matrix exception propagates to caller
# ---------------------------------------------------------------------------


def test_matrix_engine_exception_propagates(monkeypatch: pytest.MonkeyPatch) -> None:
    """A propagate_matrix failure must not be swallowed — no silent iterative fallback."""
    import app.simulation.engine.matrix_propagation as matrix_mod  # noqa: PLC0415

    def _raise(state: SimulationState, events: list) -> SimulationState:
        raise RuntimeError("matrix engine simulated failure")

    monkeypatch.setattr(matrix_mod, "propagate_matrix", _raise)

    state = _make_state("GRC", gdp_growth=0.02)
    modules = [_NullModule()]
    runner = ScenarioRunner(
        initial_state=state,
        scheduled_inputs=[],
        modules=modules,
        n_steps=1,
        session_id="test-nofallback",
        timestep_delta=_STEP_DELTA,
        audit_log=AuditLog(),
    )
    with pytest.raises(RuntimeError, match="matrix engine simulated failure"):
        runner.advance_timestep(
            current_state=state, modules=modules, scheduled_inputs=[]
        )
