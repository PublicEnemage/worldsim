"""Constraint-floor binary search — ADR-021 §D-2 (M19 G1 #1540).

Finds the minimum fiscal_multiplier that keeps the focal cohort indicator
at or above floor_value across all simulation steps.

Algorithm (ADR-021 §D-2):
    - `crosses_floor(scenario, fm, focal_cohort)` returns True if the focal
      cohort indicator falls below floor_value at any step when fiscal_multiplier=fm.
    - Binary search converges in O(log2((hi-lo)/tol)) ≈ 8–9 evaluations for
      defaults [0.1, 3.0] at tol=0.01.
    - If hi already crosses the floor → NOT_FOUND (no safe point in range).
    - If lo already does NOT cross the floor → FOUND(boundary=lo) (already safe).

Testability:
    `run_trajectory_fn` is an injection point for tests. Signature:
        run_trajectory_fn(scenario: Any, fiscal_multiplier: float) -> bool
    Returns True if the indicator crosses the floor (is below floor_value
    at any step), False if the trajectory stays safe.

    When `run_trajectory_fn` is None the caller must provide one; if not,
    a ValueError is raised immediately (the endpoint always provides a closure).

Silent failure guard (SF-2, ADR-021 §Silent Failure Mode):
    Any exception raised by `run_trajectory_fn` during an evaluation
    propagates as status=ERROR — never as a FOUND result with a partial boundary.
"""
from __future__ import annotations

import math
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from collections.abc import Callable


def binary_search(
    scenario: object,
    focal_cohort: dict[str, Any],
    lo: float = 0.1,
    hi: float = 3.0,
    tol: float = 0.01,
    run_trajectory_fn: Callable[[Any, float], bool] | None = None,
) -> dict[str, Any]:
    """Binary search for the minimum fiscal_multiplier that avoids the floor.

    Args:
        scenario: Scenario object or config. Passed verbatim to
            `run_trajectory_fn`. Tests may pass a MagicMock; the endpoint
            passes the ScenarioConfigSchema.
        focal_cohort: Dict with at least `indicator_key` and `floor_value`.
        lo: Lower bound of the search range (inclusive). Default 0.1.
        hi: Upper bound of the search range (inclusive). Default 3.0.
        tol: Convergence tolerance. Search stops when hi-lo ≤ tol.
            Default 0.01 (≈ 8–9 evaluations for default range).
        run_trajectory_fn: Callable(scenario, fiscal_multiplier) → bool.
            Returns True if the indicator crosses (falls below) the floor.
            Must be provided; None raises ValueError.

    Returns:
        Dict with keys matching ConstraintFloorSearchResponse fields:
            status: "FOUND" | "NOT_FOUND" | "ERROR"
            boundary: float | None
            uncertainty_lo: float | None
            uncertainty_hi: float | None
            evaluations: int
            search_lo: float
            search_hi: float
            floor_value: float
            indicator_key: str
            error_message: str | None
            data_tier: None (tier lookup deferred to G3)

    Raises:
        ValueError: If run_trajectory_fn is None.
    """
    if run_trajectory_fn is None:
        raise ValueError(
            "run_trajectory_fn must be provided to binary_search(). "
            "The endpoint creates a simulation closure; tests inject a mock."
        )

    indicator_key: str = focal_cohort.get("indicator_key", "")
    floor_value: float = float(focal_cohort.get("floor_value", 0.0))
    evaluations: list[int] = [0]

    def _crosses(fm: float) -> bool:
        evaluations[0] += 1
        return run_trajectory_fn(scenario, fm)

    base = {
        "search_lo": lo,
        "search_hi": hi,
        "floor_value": floor_value,
        "indicator_key": indicator_key,
        "data_tier": None,
    }

    try:
        # Boundary condition 1: hi already crosses the floor → no safe point exists
        if _crosses(hi):
            return {
                **base,
                "status": "NOT_FOUND",
                "boundary": None,
                "uncertainty_lo": None,
                "uncertainty_hi": None,
                "evaluations": evaluations[0],
                "error_message": None,
            }

        # Boundary condition 2: lo does not cross → already safe at minimum param
        if not _crosses(lo):
            return {
                **base,
                "status": "FOUND",
                "boundary": lo,
                "uncertainty_lo": lo,
                "uncertainty_hi": lo + tol,
                "evaluations": evaluations[0],
                "error_message": None,
            }

        # Binary search: lo crosses floor, hi does not → boundary is between them
        cur_lo = lo
        cur_hi = hi
        max_iters = math.ceil(math.log2((hi - lo) / tol)) + 2  # safety margin
        iters = 0
        while cur_hi - cur_lo > tol and iters < max_iters:
            iters += 1
            mid = (cur_lo + cur_hi) / 2.0
            if _crosses(mid):
                cur_lo = mid  # mid unsafe; boundary is in (mid, cur_hi)
            else:
                cur_hi = mid  # mid safe; boundary is in (cur_lo, mid)

        return {
            **base,
            "status": "FOUND",
            "boundary": cur_hi,
            "uncertainty_lo": cur_lo,
            "uncertainty_hi": cur_hi,
            "evaluations": evaluations[0],
            "error_message": None,
        }

    except (ValueError, RuntimeError) as exc:
        # SF-2: any engine exception → ERROR, never partial FOUND
        return {
            **base,
            "status": "ERROR",
            "boundary": None,
            "uncertainty_lo": None,
            "uncertainty_hi": None,
            "evaluations": evaluations[0],
            "error_message": str(exc),
        }
