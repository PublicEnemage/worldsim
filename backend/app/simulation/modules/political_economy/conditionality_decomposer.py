"""Conditionality decomposer — Issue #272.

Utility for attributing per-term fiscal costs across conditionality packages.
A conditionality package consists of one or more ControlInputs with
InputSource.CONDITIONALITY, each tagged with a constraining_actor_id and
constraint_mechanism. The decomposer attributes the total fiscal delta to
each term and each constraining actor so the scenario output can show
which creditor imposed which cost.

Intended consumers:
- Human Cost Ledger (to allocate human costs to creditor terms)
- Conditionality audit trail (to distinguish voluntary vs coerced adjustments)

Design is pure-function / stateless: no side effects, no DB I/O.
"""
from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.simulation.orchestration.inputs import ControlInput


def decompose_conditionality(
    inputs: list[ControlInput],
    entity_id: str,
) -> list[dict[str, object]]:
    """Attribute per-term fiscal costs across a conditionality package.

    Filters to CONDITIONALITY-sourced inputs for entity_id, then for each
    input computes the primary fiscal delta from its affected_attributes and
    returns a record per term.

    Args:
        inputs: All ControlInputs for the scenario step (may include non-conditionality).
        entity_id: Entity to compute decomposition for.

    Returns:
        List of attribution dicts, one per conditionality term. Each dict has:
          - constraining_actor_id: str (e.g. "IMF", "ECB")
          - constraint_mechanism: str (e.g. "DISBURSEMENT_SUSPENSION")
          - input_type: str (class name of the ControlInput)
          - fiscal_delta: Decimal | None (primary magnitude from affected_attributes)
          - implementation_capacity: Decimal (scaling factor applied)
          - effective_delta: Decimal | None (fiscal_delta × implementation_capacity)

        Returns [] if no CONDITIONALITY inputs target entity_id.
    """
    from app.simulation.orchestration.inputs import InputSource  # noqa: PLC0415

    results: list[dict[str, object]] = []

    for inp in inputs:
        if inp.source != InputSource.CONDITIONALITY:
            continue
        if inp.target_entity != entity_id:
            continue

        raw_events = inp.to_events(inp.effective_date or _EPOCH_SENTINEL)
        fiscal_delta: Decimal | None = None
        if raw_events:
            first_event = raw_events[0]
            if first_event.affected_attributes:
                fiscal_delta = next(iter(first_event.affected_attributes.values())).value

        effective_delta: Decimal | None = (
            fiscal_delta * inp.implementation_capacity
            if fiscal_delta is not None
            else None
        )

        results.append({
            "constraining_actor_id": inp.constraining_actor_id,
            "constraint_mechanism": inp.constraint_mechanism,
            "input_type": type(inp).__name__,
            "fiscal_delta": fiscal_delta,
            "implementation_capacity": inp.implementation_capacity,
            "effective_delta": effective_delta,
        })

    return results


def summarise_by_actor(
    decomposition: list[dict[str, object]],
) -> dict[str, Decimal]:
    """Aggregate effective_delta by constraining_actor_id.

    Args:
        decomposition: Output of decompose_conditionality().

    Returns:
        Dict mapping constraining_actor_id → total effective_delta.
        Entries with None effective_delta are excluded.
    """
    totals: dict[str, Decimal] = {}
    for term in decomposition:
        actor = str(term["constraining_actor_id"])
        delta = term["effective_delta"]
        if delta is None:
            continue
        totals[actor] = totals.get(actor, Decimal("0")) + delta  # type: ignore[operator]
    return totals


# Sentinel date used only when ControlInput.effective_date is None and we need
# to call to_events() to extract the magnitude. The exact date does not affect
# the magnitude computation (events carry the value from the input directly).
from datetime import UTC, datetime  # noqa: E402

_EPOCH_SENTINEL = datetime(2000, 1, 1, tzinfo=UTC)
