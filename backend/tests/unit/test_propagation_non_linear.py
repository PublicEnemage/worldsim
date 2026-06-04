"""Unit tests for non-linear propagation modes — ADR-011, Issue #29.

Covers PropagationMode.THRESHOLD and PropagationMode.CASCADE.
PropagationMode.LINEAR backward compatibility is also verified to confirm
that existing callers without explicit propagation_mode get unchanged behaviour.

Test structure:
  TestLinearBackwardCompat  — LINEAR default preserves existing behaviour
  TestThresholdMode         — THRESHOLD gates propagation on tipping-point logic
  TestCascadeMode           — CASCADE amplifies with ceiling cap
  TestMixedModeEvents       — one event carries both LINEAR and CASCADE rules
"""
from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from app.simulation.engine.models import (
    Event,
    MeasurementFramework,
    PropagationMode,
    PropagationRule,
    Relationship,
    ResolutionConfig,
    ScenarioConfig,
    SimulationEntity,
    SimulationState,
)
from app.simulation.engine.propagation import propagate
from app.simulation.engine.quantity import Quantity, VariableType

# ---------------------------------------------------------------------------
# Shared helpers (mirrors test_propagation.py conventions)
# ---------------------------------------------------------------------------

_EPOCH = datetime(2020, 1, 1)


def _q(value: float, confidence_tier: int = 1) -> Quantity:
    return Quantity(
        value=Decimal(str(value)),
        unit="ratio",
        variable_type=VariableType.RATIO,
        measurement_framework=MeasurementFramework.FINANCIAL,
        confidence_tier=confidence_tier,
    )


def _entity(entity_id: str, **attrs: float) -> SimulationEntity:
    return SimulationEntity(
        id=entity_id,
        entity_type="country",
        attributes={k: _q(v) for k, v in attrs.items()},
        metadata={"name": entity_id},
    )


def _state(
    entities: dict[str, SimulationEntity],
    relationships: list[Relationship] | None = None,
) -> SimulationState:
    return SimulationState(
        timestep=_EPOCH,
        resolution=ResolutionConfig(),
        entities=entities,
        relationships=relationships or [],
        events=[],
        scenario_config=ScenarioConfig(
            scenario_id="test",
            name="Test",
            description="",
            start_date=_EPOCH,
            end_date=datetime(2025, 1, 1),
        ),
    )


def _rel(source: str, target: str, weight: float = 1.0) -> Relationship:
    return Relationship(source_id=source, target_id=target,
                        relationship_type="trade", weight=weight)


def _event(
    source: str,
    attrs: dict[str, float],
    rules: list[PropagationRule],
) -> Event:
    return Event(
        event_id="evt-1",
        source_entity_id=source,
        event_type="shock",
        affected_attributes={k: _q(v) for k, v in attrs.items()},
        propagation_rules=rules,
        timestep_originated=_EPOCH,
        framework=MeasurementFramework.FINANCIAL,
    )


def _gav(state: SimulationState, entity_id: str, attr: str) -> Decimal:
    """Get attribute value as Decimal."""
    return state.entities[entity_id].get_attribute_value(attr, Decimal("0"))


# ---------------------------------------------------------------------------
# TestLinearBackwardCompat
# ---------------------------------------------------------------------------


class TestLinearBackwardCompat:
    """PropagationRule with no explicit mode defaults to LINEAR — existing tests pass."""

    def test_default_mode_is_linear(self) -> None:
        rule = PropagationRule(relationship_type="trade", attenuation_factor=0.5)
        assert rule.propagation_mode == PropagationMode.LINEAR

    def test_linear_attenuates_delta_across_one_hop(self) -> None:
        """LINEAR: target receives delta × attenuation × weight."""
        src = _entity("SRC", gdp_growth=0.0)
        tgt = _entity("TGT", gdp_growth=0.0)
        st = _state({"SRC": src, "TGT": tgt}, [_rel("SRC", "TGT", weight=1.0)])

        rule = PropagationRule(
            relationship_type="trade",
            attenuation_factor=0.4,
            propagation_mode=PropagationMode.LINEAR,
        )
        evt = _event("SRC", {"gdp_growth": -0.10}, [rule])
        nxt = propagate(st, [evt])

        # Source: full delta −0.10
        assert _gav(nxt, "SRC", "gdp_growth") == Decimal("-0.10")
        # Target: −0.10 × 0.4 × 1.0 = −0.04
        assert _gav(nxt, "TGT", "gdp_growth") == Decimal("-0.04")

    def test_explicit_linear_equals_default(self) -> None:
        """Explicit LINEAR= and implicit default produce identical results."""
        rels = [_rel("SRC", "TGT", weight=0.5)]

        rule_default = PropagationRule("trade", attenuation_factor=0.5, max_hops=1)
        rule_explicit = PropagationRule(
            "trade", attenuation_factor=0.5, max_hops=1,
            propagation_mode=PropagationMode.LINEAR,
        )

        nxt_default = propagate(_state({"SRC": _entity("SRC", val=0.0),
                                        "TGT": _entity("TGT", val=0.0)}, rels),
                                [_event("SRC", {"val": -0.20}, [rule_default])])
        nxt_explicit = propagate(_state({"SRC": _entity("SRC", val=0.0),
                                         "TGT": _entity("TGT", val=0.0)}, rels),
                                 [_event("SRC", {"val": -0.20}, [rule_explicit])])

        assert _gav(nxt_default, "TGT", "val") == _gav(nxt_explicit, "TGT", "val")


# ---------------------------------------------------------------------------
# TestThresholdMode
# ---------------------------------------------------------------------------


class TestThresholdMode:
    """THRESHOLD mode gates propagation on tipping-point logic."""

    def test_delta_above_threshold_is_applied(self) -> None:
        """THRESHOLD: a delta above threshold propagates normally."""
        src = _entity("SRC", gdp_growth=0.0)
        tgt = _entity("TGT", gdp_growth=0.0)
        st = _state({"SRC": src, "TGT": tgt}, [_rel("SRC", "TGT", weight=1.0)])

        rule = PropagationRule(
            relationship_type="trade",
            attenuation_factor=1.0,  # no attenuation so computed delta = base delta
            propagation_mode=PropagationMode.THRESHOLD,
            threshold=0.05,  # require at least |0.05| to propagate
        )
        # Delta magnitude |−0.10| > threshold 0.05 → should propagate
        evt = _event("SRC", {"gdp_growth": -0.10}, [rule])
        nxt = propagate(st, [evt])

        assert _gav(nxt, "TGT", "gdp_growth") == Decimal("-0.10")

    def test_delta_below_threshold_is_suppressed(self) -> None:
        """THRESHOLD: a delta below threshold is absorbed — target unchanged."""
        src = _entity("SRC", gdp_growth=0.0)
        tgt = _entity("TGT", gdp_growth=0.0)
        st = _state({"SRC": src, "TGT": tgt}, [_rel("SRC", "TGT", weight=1.0)])

        rule = PropagationRule(
            relationship_type="trade",
            attenuation_factor=0.1,  # computed delta = base × 0.1 × 1.0 = −0.01
            propagation_mode=PropagationMode.THRESHOLD,
            threshold=0.05,  # |−0.01| < 0.05 → suppressed
        )
        # Base delta −0.10, attenuated to −0.01 at target: below threshold
        evt = _event("SRC", {"gdp_growth": -0.10}, [rule])
        nxt = propagate(st, [evt])

        # Source always receives full delta; target suppressed
        assert _gav(nxt, "SRC", "gdp_growth") == Decimal("-0.10")
        assert _gav(nxt, "TGT", "gdp_growth") == Decimal("0")

    def test_threshold_zero_behaves_as_linear(self) -> None:
        """THRESHOLD with threshold=0.0 applies all deltas — identical to LINEAR."""
        rels = [_rel("SRC", "TGT", weight=1.0)]

        rule_thresh = PropagationRule(
            "trade", attenuation_factor=0.5, propagation_mode=PropagationMode.THRESHOLD,
            threshold=0.0,
        )
        rule_linear = PropagationRule("trade", attenuation_factor=0.5)

        nxt_thresh = propagate(
            _state({"SRC": _entity("SRC", val=0.0), "TGT": _entity("TGT", val=0.0)}, rels),
            [_event("SRC", {"val": -0.08}, [rule_thresh])],
        )
        nxt_linear = propagate(
            _state({"SRC": _entity("SRC", val=0.0), "TGT": _entity("TGT", val=0.0)}, rels),
            [_event("SRC", {"val": -0.08}, [rule_linear])],
        )

        assert _gav(nxt_thresh, "TGT", "val") == _gav(nxt_linear, "TGT", "val")

    def test_threshold_suppresses_second_hop_but_not_first(self) -> None:
        """THRESHOLD: first hop above threshold propagates; second hop below is suppressed."""
        src = _entity("SRC", v=0.0)
        mid = _entity("MID", v=0.0)
        dst = _entity("DST", v=0.0)
        st = _state(
            {"SRC": src, "MID": mid, "DST": dst},
            [_rel("SRC", "MID", weight=1.0), _rel("MID", "DST", weight=1.0)],
        )
        # Base delta −0.10; hop1: −0.10×0.5 = −0.05 (>= 0.05 → applied)
        # hop2: −0.05×0.5 = −0.025 (< 0.05 → suppressed)
        rule = PropagationRule(
            "trade", attenuation_factor=0.5, max_hops=2,
            propagation_mode=PropagationMode.THRESHOLD, threshold=0.05,
        )
        nxt = propagate(st, [_event("SRC", {"v": -0.10}, [rule])])

        assert _gav(nxt, "MID", "v") == Decimal("-0.05")
        assert _gav(nxt, "DST", "v") == Decimal("0")


# ---------------------------------------------------------------------------
# TestCascadeMode
# ---------------------------------------------------------------------------


class TestCascadeMode:
    """CASCADE mode amplifies delta per hop, capped by ceiling."""

    def test_cascade_amplifies_at_first_hop(self) -> None:
        """CASCADE: target receives delta × (1/attenuation) × weight."""
        src = _entity("SRC", gdp_growth=0.0)
        tgt = _entity("TGT", gdp_growth=0.0)
        st = _state({"SRC": src, "TGT": tgt}, [_rel("SRC", "TGT", weight=1.0)])

        rule = PropagationRule(
            relationship_type="trade",
            attenuation_factor=0.5,   # amplification = 1/0.5 = 2×
            propagation_mode=PropagationMode.CASCADE,
            ceiling=10.0,  # high ceiling — no cap active at 2×
        )
        # Source: −0.08; Target: −0.08 × 2.0 × 1.0 = −0.16
        evt = _event("SRC", {"gdp_growth": -0.08}, [rule])
        nxt = propagate(st, [evt])

        assert _gav(nxt, "SRC", "gdp_growth") == Decimal("-0.08")
        assert _gav(nxt, "TGT", "gdp_growth") == Decimal("-0.16")

    def test_cascade_ceiling_caps_amplification(self) -> None:
        """CASCADE ceiling: amplified delta capped at ceiling × |base|."""
        src = _entity("SRC", gdp_growth=0.0)
        tgt = _entity("TGT", gdp_growth=0.0)
        st = _state({"SRC": src, "TGT": tgt}, [_rel("SRC", "TGT", weight=1.0)])

        rule = PropagationRule(
            relationship_type="trade",
            attenuation_factor=0.1,   # would amplify by 10× without ceiling
            propagation_mode=PropagationMode.CASCADE,
            ceiling=3.0,              # cap at 3× base = 3 × 0.08 = 0.24
        )
        evt = _event("SRC", {"gdp_growth": -0.08}, [rule])
        nxt = propagate(st, [evt])

        # Without ceiling: −0.08 × 10 = −0.80; with ceiling=3.0: max |delta| = 0.24
        result = _gav(nxt, "TGT", "gdp_growth")
        assert result == Decimal("-0.24"), f"Expected −0.24 (ceiling=3×base), got {result}"

    def test_cascade_amplifies_more_than_linear_same_factor(self) -> None:
        """CASCADE must produce strictly larger |delta| at target than LINEAR."""
        factor = 0.5
        linear_nxt = propagate(
            _state({"SRC": _entity("SRC", v=0.0), "TGT": _entity("TGT", v=0.0)},
                   [_rel("SRC", "TGT", weight=1.0)]),
            [_event("SRC", {"v": -0.10},
                    [PropagationRule("trade", attenuation_factor=factor)])],
        )
        cascade_nxt = propagate(
            _state({"SRC": _entity("SRC", v=0.0), "TGT": _entity("TGT", v=0.0)},
                   [_rel("SRC", "TGT", weight=1.0)]),
            [_event("SRC", {"v": -0.10},
                    [PropagationRule("trade", attenuation_factor=factor,
                                     propagation_mode=PropagationMode.CASCADE,
                                     ceiling=5.0)])],
        )

        linear_val = abs(_gav(linear_nxt, "TGT", "v"))
        cascade_val = abs(_gav(cascade_nxt, "TGT", "v"))
        assert cascade_val > linear_val, (
            f"CASCADE ({cascade_val}) should exceed LINEAR ({linear_val})"
        )

    def test_cascade_two_hop_compounds_amplification(self) -> None:
        """CASCADE multi-hop: effect compounds (amplified again at second hop)."""
        src = _entity("SRC", v=0.0)
        mid = _entity("MID", v=0.0)
        dst = _entity("DST", v=0.0)
        st = _state(
            {"SRC": src, "MID": mid, "DST": dst},
            [_rel("SRC", "MID", weight=1.0), _rel("MID", "DST", weight=1.0)],
        )
        # attenuation_factor=0.5 → scale_per_hop = 2.0; ceiling=10.0 (inactive)
        # hop1: MID gets −0.08 × 2.0 = −0.16
        # hop2: DST gets −0.16 × 2.0 = −0.32, still below 10× base = 0.80
        rule = PropagationRule(
            "trade", attenuation_factor=0.5, max_hops=2,
            propagation_mode=PropagationMode.CASCADE, ceiling=10.0,
        )
        nxt = propagate(st, [_event("SRC", {"v": -0.08}, [rule])])

        assert _gav(nxt, "MID", "v") == Decimal("-0.16")
        assert _gav(nxt, "DST", "v") == Decimal("-0.32")

    def test_cascade_ceiling_preserves_sign(self) -> None:
        """Ceiling cap preserves the sign of the amplified delta."""
        src = _entity("SRC", v=0.0)
        tgt = _entity("TGT", v=0.0)
        st = _state({"SRC": src, "TGT": tgt}, [_rel("SRC", "TGT", weight=1.0)])

        rule = PropagationRule(
            "trade", attenuation_factor=0.1,  # 10× amplification
            propagation_mode=PropagationMode.CASCADE, ceiling=2.0,
        )
        # Positive base delta: cap should preserve positive sign
        evt = _event("SRC", {"v": 0.05}, [rule])
        nxt = propagate(st, [evt])

        tgt_val = _gav(nxt, "TGT", "v")
        assert tgt_val > Decimal("0"), "Ceiling-capped CASCADE delta must preserve positive sign"
        assert tgt_val == Decimal("0.10"), f"Expected 2×0.05=0.10, got {tgt_val}"


# ---------------------------------------------------------------------------
# TestMixedModeEvents
# ---------------------------------------------------------------------------


class TestMixedModeEvents:
    """One event may carry both LINEAR and CASCADE rules for different edge types."""

    def test_event_with_linear_and_cascade_rules(self) -> None:
        """An event with two rules (LINEAR trade, CASCADE banking) applies both."""
        src = _entity("SRC", v=0.0)
        trade_tgt = _entity("TRADE_TGT", v=0.0)
        bank_tgt = _entity("BANK_TGT", v=0.0)
        st = _state(
            {"SRC": src, "TRADE_TGT": trade_tgt, "BANK_TGT": bank_tgt},
            relationships=[
                Relationship("SRC", "TRADE_TGT", "trade", weight=1.0),
                Relationship("SRC", "BANK_TGT", "banking", weight=1.0),
            ],
        )

        linear_rule = PropagationRule("trade", attenuation_factor=0.5)
        cascade_rule = PropagationRule(
            "banking", attenuation_factor=0.5,
            propagation_mode=PropagationMode.CASCADE, ceiling=5.0,
        )
        evt = _event("SRC", {"v": -0.10}, [linear_rule, cascade_rule])
        nxt = propagate(st, [evt])

        # LINEAR: −0.10 × 0.5 = −0.05
        assert _gav(nxt, "TRADE_TGT", "v") == Decimal("-0.05")
        # CASCADE: −0.10 × (1/0.5) = −0.20 (below ceiling 5×0.10=0.50)
        assert _gav(nxt, "BANK_TGT", "v") == Decimal("-0.20")
        # Source always gets full delta regardless of mode
        assert _gav(nxt, "SRC", "v") == Decimal("-0.10")
