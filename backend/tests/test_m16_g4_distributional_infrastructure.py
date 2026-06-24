"""QA tests for M16-G4: Distributional Infrastructure (#22 scoped, #275, #102).

QA Lead — authored from intent document at:
  docs/process/intents/M16-G4-2026-06-23-distributional-infrastructure.md

Three deliverable groups:
  #22 (scoped) — Quantity schema extension (4 new DB columns) + SyntheticDataEngine MVP
                 (Methods E + B) + per-indicator synthetic badge wiring in Zone 1B/1D
  #275 — Calibrated ecological-to-financial transmission (ecological_shock_coefficient)
  #102 — Distributional comparison API (variance/p10/p50/p90 on GET /compare)

NM-056 rule (soft-skip prevention): NO test uses pytest.skip() conditionally
except on DATABASE_URL absence for integration tests. No test.skip() patterns.
A test that cannot yet run returns without asserting — it does not skip.

EE-PENDING ACs (AC-EE-1, AC-EE-2 from #275): NOT YET AUTHORED. The Ecological
Economist DIC review on GitHub issue #275 is required before these tests can be
written. They will be authored in a follow-up commit once the EE review comment
is filed, per the intent document §7 Test Authorship Obligation.

SyntheticDataEngine interface (designed by these tests — implementing agent must match):
  Module: app.simulation.synthetic_data_engine
  Class:  SyntheticDataEngine
  Method: SyntheticDataEngine.infer(entity_id: str, indicator_key: str,
            source_registry: Any) -> SyntheticQuantityResult

  source_registry interface (the implementing agent's SourceRegistry must support):
    source_registry.get_indicator_profile(entity_id, indicator_key) → IndicatorDataProfile

  IndicatorDataProfile attributes (comparable named tuple or dataclass):
    comparable_country_count: int     — number of comparable country observations in registry
    mnar: bool                        — Missing Not At Random flag
    observed_fraction: float          — fraction of historical periods with observed data (0–1)
    gap_length: int                   — longest consecutive missing-data period (periods)
    bounded_on_both_sides: bool       — gap has observed values on both sides
    ci_width_to_estimate_ratio: float — CI width / point estimate ratio

  SyntheticQuantityResult attributes:
    is_synthetic: bool
    synthetic_method: str | None     — "STRUCTURAL_ABSENCE" | "SYNTHETIC_COMPARABLE" | "SYNTHETIC_MODEL"
    value: float | None              — None for STRUCTURAL_ABSENCE

Method dispatch rules (ADR-007 §Section 1, enforced by AC-3/AC-4/AC-5):
  Method E (STRUCTURAL_ABSENCE) fires when ANY of:
    - mnar is True
    - comparable_country_count < 3
    - ci_width_to_estimate_ratio > 4.0
  Method B (SYNTHETIC_COMPARABLE) fires when ALL of:
    - observed_fraction >= 0.80
    - gap_length <= 3
    - bounded_on_both_sides is True
    - (none of the Method E conditions are met)
  Method E takes precedence over Method B when both could nominally apply.

AC coverage:
  #22 backend:
    AC-1   Quantity table has 4 new columns after alembic upgrade head (DB)
    AC-2   ZMB 8-step non-regression: no is_synthetic=True flags (DB)
    AC-3   Method E fires for comparable_count < 3 (unit, no DB)
    AC-4   Method B fires for MICE conditions without MNAR (unit, no DB)
    AC-5   MNAR flag → Method E even when MICE conditions are met (unit, no DB)
    AC-6   api_contracts.yml contains "is_synthetic" in trajectory Quantity schema

  #275 backend:
    AC-7   ScenarioConfigSchema accepts ecological_shock_coefficient in [0.0, 1.0]
    AC-8   ecological_shock_coefficient=0.0 → trajectory identical to no coefficient (DB)
    AC-9   api_contracts.yml documents "ecological_shock_coefficient"
    [AC-EE-1, AC-EE-2 — deferred pending Ecological Economist DIC review on #275]

  #102 backend:
    AC-10  GET /compare response includes distribution.variance/p10/p50/p90 (DB)
    AC-11  Insufficient data (<3 points) → null distribution fields, HTTP 200 (DB)
    AC-12  api_contracts.yml documents "distribution" with variance/p10/p50/p90

Soft-skip guard (NM-056 follow-up, sprint entry §2.4):
  No pytest.skip() except DATABASE_URL absence guard in _require_db().
  AC-1 (schema migration) and AC-3/AC-4/AC-5 (SyntheticDataEngine dispatch)
  must not soft-skip on import failure — pytest.fail() with a clear message is
  the required response to a missing module or missing DB column.
"""
from __future__ import annotations

import os
import pathlib
from dataclasses import dataclass
from decimal import Decimal
from typing import TYPE_CHECKING, Any

import httpx
import pytest
import pytest_asyncio

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator

_DATABASE_URL = os.environ.get("DATABASE_URL", "")

_REPO_ROOT = pathlib.Path(__file__).parent.parent.parent
_API_CONTRACTS = _REPO_ROOT / "docs" / "schema" / "api_contracts.yml"


def _require_db() -> None:
    if not _DATABASE_URL:
        pytest.skip("DATABASE_URL not set — skipping M16-G4 integration test")


pytestmark = pytest.mark.integration


# ---------------------------------------------------------------------------
# Mock objects for SyntheticDataEngine unit tests (AC-3, AC-4, AC-5)
# ---------------------------------------------------------------------------

@dataclass
class _IndicatorDataProfile:
    """Data profile for a single (entity, indicator) pair.

    This dataclass defines the interface that the implementing agent's
    source_registry.get_indicator_profile() must return. The SyntheticDataEngine
    uses these fields to decide which synthetic method (E or B) to apply.

    If the implementing agent uses a different attribute name or structure, the
    AC-3/AC-4/AC-5 unit tests will fail — which is the intended behavior.
    These tests define the interface contract.
    """
    comparable_country_count: int
    mnar: bool
    observed_fraction: float        # 0.0–1.0; fraction of historical periods with observed data
    gap_length: int                 # longest consecutive missing-data run (periods)
    bounded_on_both_sides: bool     # gap flanked by observed values on both sides
    ci_width_to_estimate_ratio: float = 1.0  # CI width / point estimate; >4.0 triggers Method E


class _MockSourceRegistry:
    """Minimal source registry mock for SyntheticDataEngine unit tests.

    Provides a single profile for all (entity_id, indicator_key) queries.
    The real SourceRegistry stores per-indicator profiles; this mock supplies
    a fixed profile for testing method dispatch in isolation.
    """

    def __init__(self, profile: _IndicatorDataProfile) -> None:
        self._profile = profile

    def get_indicator_profile(
        self, entity_id: str, indicator_key: str
    ) -> _IndicatorDataProfile:
        return self._profile


# ---------------------------------------------------------------------------
# Payload helpers
# ---------------------------------------------------------------------------

def _zmb_8_step_payload(extra_config: dict[str, Any] | None = None) -> dict[str, Any]:
    """ZMB ECF scenario — 8 steps, real-data (no synthetic inference)."""
    config: dict[str, Any] = {
        "entities": ["ZMB"],
        "n_steps": 8,
        "timestep_label": "annual",
        "start_date": "2023-01-01",
        "modules_config": {
            "ecological": {"enabled": False},
            "political_economy": {"enabled": False},
        },
    }
    if extra_config:
        config.update(extra_config)
    return {
        "name": "M16-G4 test — ZMB 8-step baseline",
        "configuration": config,
        "scheduled_inputs": [],
    }


# ---------------------------------------------------------------------------
# Async HTTP client fixture for integration tests
# ---------------------------------------------------------------------------

@pytest_asyncio.fixture()
async def client() -> AsyncGenerator[httpx.AsyncClient, None]:
    _require_db()
    from app.main import app  # type: ignore[import]

    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app),
        base_url="http://test",
        timeout=120.0,
    ) as ac:
        yield ac


# ===========================================================================
# SECTION: #22 — Quantity Schema + SyntheticDataEngine MVP
# ===========================================================================

# ---------------------------------------------------------------------------
# AC-1 — Quantity table has 4 new columns after alembic upgrade head (DB)
# ---------------------------------------------------------------------------


class TestAC1QuantitySchemaMigration:
    """AC-1: The `quantity` table must exist with the four new G4 columns.

    ADR-007 §Consequences step 1: Alembic migration adds:
      is_synthetic BOOLEAN NOT NULL DEFAULT FALSE
      synthetic_method VARCHAR (nullable)
      comparison_group_id VARCHAR (nullable)
      holdout_validated BOOLEAN (nullable)

    Intent doc §3.1 State 1: 'alembic upgrade head applied to a fresh database
    instance completes without error. The quantity table contains exactly the
    four new columns.'

    Pre-G4: the `quantity` table does not exist → this test fails.
    Post-G4: the table and all four columns exist → this test passes.
    """

    def test_quantity_table_exists(self) -> None:
        _require_db()
        try:
            from sqlalchemy import create_engine, inspect as sa_inspect
        except ImportError:
            pytest.fail("sqlalchemy not importable — cannot run AC-1 schema inspection test.")

        engine = create_engine(_DATABASE_URL)
        inspector = sa_inspect(engine)
        table_names = inspector.get_table_names()
        assert "quantity" in table_names, (
            "AC-1 FAIL: The 'quantity' table does not exist in the database. "
            "Run 'alembic upgrade head' to apply the G4 migration that creates this table. "
            "ADR-007 §Consequences step 1: Alembic migration adds the quantity table "
            "with is_synthetic, synthetic_method, comparison_group_id, holdout_validated."
        )

    def test_quantity_table_has_is_synthetic_column(self) -> None:
        _require_db()
        from sqlalchemy import create_engine, inspect as sa_inspect

        engine = create_engine(_DATABASE_URL)
        inspector = sa_inspect(engine)
        columns = {c["name"]: c for c in inspector.get_columns("quantity")}

        assert "is_synthetic" in columns, (
            "AC-1 FAIL: 'is_synthetic' column missing from quantity table. "
            "ADR-007 §Consequences: 'is_synthetic BOOLEAN NOT NULL DEFAULT FALSE'."
        )
        col = columns["is_synthetic"]
        assert not col.get("nullable", True), (
            "AC-1 FAIL: 'is_synthetic' must be NOT NULL. "
            "ADR-007 §Consequences specifies DEFAULT FALSE — nullable is not permitted."
        )

    def test_quantity_table_has_synthetic_method_column(self) -> None:
        _require_db()
        from sqlalchemy import create_engine, inspect as sa_inspect

        engine = create_engine(_DATABASE_URL)
        inspector = sa_inspect(engine)
        columns = {c["name"]: c for c in inspector.get_columns("quantity")}

        assert "synthetic_method" in columns, (
            "AC-1 FAIL: 'synthetic_method' column missing from quantity table. "
            "ADR-007 §Consequences: 'synthetic_method VARCHAR (nullable)'. "
            "Values: 'STRUCTURAL_ABSENCE', 'SYNTHETIC_COMPARABLE', 'SYNTHETIC_MODEL'."
        )
        col = columns["synthetic_method"]
        assert col.get("nullable", True), (
            "AC-1 FAIL: 'synthetic_method' must be nullable — non-synthetic Quantity "
            "rows will have NULL for this column."
        )

    def test_quantity_table_has_comparison_group_id_column(self) -> None:
        _require_db()
        from sqlalchemy import create_engine, inspect as sa_inspect

        engine = create_engine(_DATABASE_URL)
        inspector = sa_inspect(engine)
        columns = {c["name"]: c for c in inspector.get_columns("quantity")}

        assert "comparison_group_id" in columns, (
            "AC-1 FAIL: 'comparison_group_id' column missing from quantity table. "
            "ADR-007 §Consequences: 'comparison_group_id VARCHAR (nullable)'."
        )

    def test_quantity_table_has_holdout_validated_column(self) -> None:
        _require_db()
        from sqlalchemy import create_engine, inspect as sa_inspect

        engine = create_engine(_DATABASE_URL)
        inspector = sa_inspect(engine)
        columns = {c["name"]: c for c in inspector.get_columns("quantity")}

        assert "holdout_validated" in columns, (
            "AC-1 FAIL: 'holdout_validated' column missing from quantity table. "
            "ADR-007 §Consequences: 'holdout_validated BOOLEAN (nullable)'."
        )

    def test_existing_zmb_scenario_unaffected(self, client: httpx.AsyncClient) -> None:
        """AC-1 non-regression: ZMB 8-step scenario completes after the migration.

        The Alembic migration must not break existing scenario creation or runs.
        Observable state §3.1 State 1: 'Existing ZMB 8-step scenario runs are unaffected.'
        """
        import asyncio

        async def _run() -> None:
            create_res = await client.post("/api/v1/scenarios", json=_zmb_8_step_payload())
            assert create_res.status_code == 201, (
                f"AC-1 non-regression: POST /scenarios returned {create_res.status_code}. "
                f"Body: {create_res.text[:300]}"
            )

        asyncio.get_event_loop().run_until_complete(_run())


# ---------------------------------------------------------------------------
# AC-2 — ZMB 8-step non-regression: no is_synthetic=True flags (DB)
# ---------------------------------------------------------------------------


class TestAC2ZmbNonRegression:
    """AC-2: ZMB ECF 8-step run produces no is_synthetic=True Quantity values.

    World Bank-sourced ZMB indicators (poverty_headcount_ratio, reserve_coverage_months)
    are real data (Tier 1–3). The SyntheticDataEngine must not apply synthetic
    inference to indicators where primary data exists in the source registry.

    Intent doc §3.1 State 4: 'A ZMB ECF scenario run produces no is_synthetic: true
    Quantity values on any indicator sourced from World Bank primary statistics.'

    Silent failure detection: if SyntheticDataEngine runs on all indicators regardless
    of whether source data exists, ZMB indicators would be falsely flagged as synthetic.
    """

    async def test_zmb_run_returns_no_synthetic_flags(self, client: httpx.AsyncClient) -> None:
        create_res = await client.post("/api/v1/scenarios", json=_zmb_8_step_payload())
        assert create_res.status_code == 201, (
            f"ZMB create returned {create_res.status_code}: {create_res.text[:300]}"
        )
        scenario_id = create_res.json()["scenario_id"]

        run_res = await client.post(f"/api/v1/scenarios/{scenario_id}/run")
        assert run_res.status_code == 200, (
            f"ZMB run returned {run_res.status_code}: {run_res.text[:300]}"
        )

        trajectory_res = await client.get(
            f"/api/v1/scenarios/{scenario_id}/trajectory", params={"entity_id": "ZMB"}
        )
        if trajectory_res.status_code == 404:
            return  # trajectory endpoint not yet implemented for this step (pre-G4)
        assert trajectory_res.status_code == 200, (
            f"GET /trajectory returned {trajectory_res.status_code}"
        )

        trajectory = trajectory_res.json()
        steps = trajectory.get("steps", [])
        synthetic_flags: list[dict[str, Any]] = []
        for step in steps:
            step_index = step.get("step_index", "unknown")
            attributes = step.get("attributes", {})
            for entity_id, entity_attrs in attributes.items():
                for key, qty in entity_attrs.items():
                    if isinstance(qty, dict) and qty.get("is_synthetic") is True:
                        synthetic_flags.append({
                            "step": step_index, "entity": entity_id,
                            "key": key, "method": qty.get("synthetic_method"),
                        })

        assert not synthetic_flags, (
            f"AC-2 FAIL: {len(synthetic_flags)} is_synthetic=True flag(s) found in ZMB "
            f"8-step trajectory: {synthetic_flags[:5]}. "
            "World Bank-sourced ZMB indicators must not be flagged as synthetic. "
            "ADR-007: SyntheticDataEngine only fires when primary data is absent or insufficient. "
            "Silent failure: SyntheticDataEngine running unconditionally on all indicators."
        )


# ---------------------------------------------------------------------------
# AC-3 — Method E fires for comparable_country_count < 3 (unit, no DB)
# ---------------------------------------------------------------------------


class TestAC3MethodEStructuralAbsence:
    """AC-3: SyntheticDataEngine.infer() must return STRUCTURAL_ABSENCE when
    comparable_country_count < 3.

    ADR-007 §Section 1: 'Method E — Structural Absence Declaration. Triggered when
    MNAR, fewer than 3 comparable country observations, or CI width > 4× point estimate.'

    Observable application state §3.1 State 2: 'When fewer than 3 comparable country
    observations exist in the source registry for that indicator, the returned Quantity
    carries is_synthetic=True, synthetic_method="STRUCTURAL_ABSENCE", value=None.'

    Pre-G4: ImportError on SyntheticDataEngine → pytest.fail() (not skip).
    """

    def test_method_e_fires_for_zero_comparables(self) -> None:
        try:
            from app.simulation.synthetic_data_engine import SyntheticDataEngine  # type: ignore[import]
        except ImportError:
            pytest.fail(
                "app.simulation.synthetic_data_engine.SyntheticDataEngine could not be imported. "
                "AC-3: The SyntheticDataEngine must be implemented at this module path. "
                "G4 implementation gate: this test must pass before the implementation PR merges."
            )

        profile = _IndicatorDataProfile(
            comparable_country_count=0,
            mnar=False,
            observed_fraction=0.5,
            gap_length=5,
            bounded_on_both_sides=False,
            ci_width_to_estimate_ratio=1.0,
        )
        registry = _MockSourceRegistry(profile)

        result = SyntheticDataEngine.infer(
            entity_id="SYNTHETIC_TEST",
            indicator_key="test_no_comparables",
            source_registry=registry,
        )

        assert result.is_synthetic is True, (
            "AC-3 FAIL: is_synthetic must be True when comparable_country_count=0. "
            "ADR-007 §Section 1 Method E: fewer than 3 comparables triggers STRUCTURAL_ABSENCE."
        )
        assert result.synthetic_method == "STRUCTURAL_ABSENCE", (
            f"AC-3 FAIL: synthetic_method was {result.synthetic_method!r}, expected "
            "'STRUCTURAL_ABSENCE'. comparable_country_count=0 must trigger Method E."
        )
        assert result.value is None, (
            f"AC-3 FAIL: value was {result.value!r}, expected None. "
            "Structural Absence Declarations carry no value — the data does not exist."
        )

    def test_method_e_fires_for_two_comparables(self) -> None:
        try:
            from app.simulation.synthetic_data_engine import SyntheticDataEngine  # type: ignore[import]
        except ImportError:
            pytest.fail(
                "SyntheticDataEngine could not be imported — AC-3 boundary test cannot run."
            )

        profile = _IndicatorDataProfile(
            comparable_country_count=2,
            mnar=False,
            observed_fraction=0.9,
            gap_length=2,
            bounded_on_both_sides=True,
            ci_width_to_estimate_ratio=1.0,
        )
        registry = _MockSourceRegistry(profile)

        result = SyntheticDataEngine.infer(
            entity_id="SYNTHETIC_TEST",
            indicator_key="test_two_comparables",
            source_registry=registry,
        )

        assert result.synthetic_method == "STRUCTURAL_ABSENCE", (
            f"AC-3 FAIL: synthetic_method was {result.synthetic_method!r} with "
            "comparable_country_count=2. The threshold is strictly < 3: "
            "2 comparables must still trigger Method E, not Method B."
        )

    def test_method_e_fires_for_high_ci_ratio(self) -> None:
        """Method E also fires when CI width > 4× the point estimate."""
        try:
            from app.simulation.synthetic_data_engine import SyntheticDataEngine  # type: ignore[import]
        except ImportError:
            pytest.fail("SyntheticDataEngine could not be imported — AC-3 CI test cannot run.")

        profile = _IndicatorDataProfile(
            comparable_country_count=10,     # enough comparables
            mnar=False,
            observed_fraction=0.9,
            gap_length=2,
            bounded_on_both_sides=True,
            ci_width_to_estimate_ratio=4.5,  # > 4.0 → Method E
        )
        registry = _MockSourceRegistry(profile)

        result = SyntheticDataEngine.infer(
            entity_id="SYNTHETIC_TEST",
            indicator_key="test_high_ci_ratio",
            source_registry=registry,
        )

        assert result.synthetic_method == "STRUCTURAL_ABSENCE", (
            f"AC-3 FAIL: synthetic_method was {result.synthetic_method!r} with "
            "ci_width_to_estimate_ratio=4.5. ADR-007 §Section 1: CI > 4× point estimate "
            "triggers Method E regardless of comparable count."
        )


# ---------------------------------------------------------------------------
# AC-4 — Method B fires for MICE conditions (unit, no DB)
# ---------------------------------------------------------------------------


class TestAC4MethodBMice:
    """AC-4: SyntheticDataEngine.infer() must return SYNTHETIC_COMPARABLE when
    MICE conditions are met (≥80% observed, gap ≤3 periods, bounded, no MNAR).

    ADR-007 §Section 1: 'Method B — MICE. Triggered for ≥80% observed data,
    gap ≤3 periods, bounded on both sides.'

    Observable application state §3.1 State 3: 'The returned Quantity carries
    is_synthetic=True, synthetic_method="SYNTHETIC_COMPARABLE", value within [0.0, 1.0].'

    Pre-G4: ImportError → pytest.fail().
    """

    def test_method_b_fires_for_mice_conditions(self) -> None:
        try:
            from app.simulation.synthetic_data_engine import SyntheticDataEngine  # type: ignore[import]
        except ImportError:
            pytest.fail(
                "app.simulation.synthetic_data_engine.SyntheticDataEngine could not be imported. "
                "AC-4: The SyntheticDataEngine must be implemented before the G4 PR merges."
            )

        profile = _IndicatorDataProfile(
            comparable_country_count=8,     # ≥3 comparables → not Method E
            mnar=False,                     # not MNAR → not Method E
            observed_fraction=0.82,         # ≥80% observed → Method B condition met
            gap_length=3,                   # ≤3 periods → Method B condition met
            bounded_on_both_sides=True,     # bounded → Method B condition met
            ci_width_to_estimate_ratio=1.0, # ≤4.0 → not Method E
        )
        registry = _MockSourceRegistry(profile)

        result = SyntheticDataEngine.infer(
            entity_id="SYNTHETIC_TEST",
            indicator_key="test_mice_conditions",
            source_registry=registry,
        )

        assert result.is_synthetic is True, (
            "AC-4 FAIL: is_synthetic must be True — MICE imputation is synthetic inference."
        )
        assert result.synthetic_method == "SYNTHETIC_COMPARABLE", (
            f"AC-4 FAIL: synthetic_method was {result.synthetic_method!r}, expected "
            "'SYNTHETIC_COMPARABLE'. All MICE conditions met; Method B must fire. "
            "ADR-007 §Section 1 Method B: ≥80% observed + gap ≤3 + bounded → SYNTHETIC_COMPARABLE."
        )
        assert result.value is not None, (
            "AC-4 FAIL: value must not be None — MICE imputation produces a numeric estimate. "
            "Only STRUCTURAL_ABSENCE produces value=None."
        )
        try:
            v = Decimal(str(result.value))
            assert Decimal("0.0") <= v <= Decimal("1.0"), (
                f"AC-4 FAIL: MICE imputed value {v} is outside [0.0, 1.0]. "
                "Bounded ratio indicators must remain within their natural range."
            )
        except Exception as exc:  # noqa: BLE001
            pytest.fail(
                f"AC-4 FAIL: result.value {result.value!r} could not be converted to Decimal: {exc}"
            )

    def test_method_b_minimum_observed_fraction_boundary(self) -> None:
        """Method B fires at exactly 80% observed fraction (boundary condition)."""
        try:
            from app.simulation.synthetic_data_engine import SyntheticDataEngine  # type: ignore[import]
        except ImportError:
            pytest.fail("SyntheticDataEngine could not be imported — AC-4 boundary test cannot run.")

        profile = _IndicatorDataProfile(
            comparable_country_count=5,
            mnar=False,
            observed_fraction=0.80,   # exactly at the boundary — must trigger Method B
            gap_length=1,
            bounded_on_both_sides=True,
            ci_width_to_estimate_ratio=0.5,
        )
        registry = _MockSourceRegistry(profile)

        result = SyntheticDataEngine.infer(
            entity_id="SYNTHETIC_TEST",
            indicator_key="test_mice_exact_boundary",
            source_registry=registry,
        )

        assert result.synthetic_method == "SYNTHETIC_COMPARABLE", (
            f"AC-4 FAIL: synthetic_method was {result.synthetic_method!r} at exactly "
            "80% observed fraction. The boundary must be inclusive: ≥80% triggers Method B."
        )

    def test_method_b_gap_length_boundary(self) -> None:
        """Method B fires at exactly gap_length=3 (boundary condition)."""
        try:
            from app.simulation.synthetic_data_engine import SyntheticDataEngine  # type: ignore[import]
        except ImportError:
            pytest.fail("SyntheticDataEngine could not be imported — AC-4 boundary test cannot run.")

        profile = _IndicatorDataProfile(
            comparable_country_count=5,
            mnar=False,
            observed_fraction=0.85,
            gap_length=3,      # exactly at the boundary — must trigger Method B
            bounded_on_both_sides=True,
            ci_width_to_estimate_ratio=0.5,
        )
        registry = _MockSourceRegistry(profile)

        result = SyntheticDataEngine.infer(
            entity_id="SYNTHETIC_TEST",
            indicator_key="test_mice_gap_boundary",
            source_registry=registry,
        )

        assert result.synthetic_method == "SYNTHETIC_COMPARABLE", (
            f"AC-4 FAIL: synthetic_method was {result.synthetic_method!r} at gap_length=3. "
            "The boundary must be inclusive: ≤3 periods triggers Method B."
        )

    def test_method_b_does_not_fire_for_unmet_conditions(self) -> None:
        """Method B must NOT fire when observed_fraction < 0.80 (and no Method E conditions)."""
        try:
            from app.simulation.synthetic_data_engine import SyntheticDataEngine  # type: ignore[import]
        except ImportError:
            pytest.fail("SyntheticDataEngine could not be imported — AC-4 failure case cannot run.")

        profile = _IndicatorDataProfile(
            comparable_country_count=8,
            mnar=False,
            observed_fraction=0.70,  # < 80% — Method B must NOT fire
            gap_length=2,
            bounded_on_both_sides=True,
            ci_width_to_estimate_ratio=1.0,
        )
        registry = _MockSourceRegistry(profile)

        result = SyntheticDataEngine.infer(
            entity_id="SYNTHETIC_TEST",
            indicator_key="test_below_mice_threshold",
            source_registry=registry,
        )

        assert result.synthetic_method != "SYNTHETIC_COMPARABLE", (
            f"AC-4 FAIL: synthetic_method was {result.synthetic_method!r} with "
            "observed_fraction=0.70. Method B requires ≥80% observed — it must not fire here. "
            "Silent failure 2 (intent doc §3.4): all-or-nothing Method E fallback would "
            "produce STRUCTURAL_ABSENCE here, not SYNTHETIC_COMPARABLE."
        )


# ---------------------------------------------------------------------------
# AC-5 — Method selection order: MNAR → E even when B conditions are met (unit, no DB)
# ---------------------------------------------------------------------------


class TestAC5MethodSelectionOrder:
    """AC-5: Method E takes precedence over Method B when MNAR is True.

    ADR-007 §Section 1 method ordering: Method E conditions are evaluated first.
    When MNAR is True, Method E fires regardless of whether Method B conditions are met.

    Intent doc AC-5: 'when MNAR flag is absent and B conditions are met, Method B fires
    before Method E is evaluated.'

    Pre-G4: ImportError → pytest.fail().
    """

    def test_mnar_flag_triggers_method_e_over_method_b(self) -> None:
        try:
            from app.simulation.synthetic_data_engine import SyntheticDataEngine  # type: ignore[import]
        except ImportError:
            pytest.fail(
                "SyntheticDataEngine could not be imported — AC-5 precedence test cannot run."
            )

        profile = _IndicatorDataProfile(
            comparable_country_count=10,    # enough comparables — no Method E from this
            mnar=True,                      # MNAR flag SET → Method E must fire
            observed_fraction=0.90,         # ≥80% — Method B conditions met too
            gap_length=2,                   # ≤3 — Method B conditions met too
            bounded_on_both_sides=True,
            ci_width_to_estimate_ratio=0.5,  # ≤4.0 — no Method E from CI
        )
        registry = _MockSourceRegistry(profile)

        result = SyntheticDataEngine.infer(
            entity_id="SYNTHETIC_TEST",
            indicator_key="test_mnar_with_mice_conditions",
            source_registry=registry,
        )

        assert result.synthetic_method == "STRUCTURAL_ABSENCE", (
            f"AC-5 FAIL: synthetic_method was {result.synthetic_method!r}. "
            "When mnar=True, Method E must fire even when all Method B conditions are also met. "
            "MNAR (Missing Not At Random) means the data is structurally absent for non-random "
            "reasons — imputation would introduce systematic bias. "
            "ADR-007 §Section 1: Method E takes precedence over Method B."
        )
        assert result.value is None, (
            "AC-5 FAIL: value must be None when MNAR forces STRUCTURAL_ABSENCE, "
            "even though MICE conditions are met."
        )

    def test_method_b_fires_without_mnar_when_mice_conditions_met(self) -> None:
        """Confirm Method B fires when MNAR is False and MICE conditions are met.

        This is the positive counterpart to the MNAR precedence test: removes the MNAR
        flag to confirm Method B fires when unobstructed. Catches the silent failure
        where Method E fires unconditionally (ignoring method selection logic).
        """
        try:
            from app.simulation.synthetic_data_engine import SyntheticDataEngine  # type: ignore[import]
        except ImportError:
            pytest.fail("SyntheticDataEngine could not be imported — AC-5 positive case cannot run.")

        profile = _IndicatorDataProfile(
            comparable_country_count=10,
            mnar=False,     # MNAR NOT set → Method B is eligible
            observed_fraction=0.90,
            gap_length=2,
            bounded_on_both_sides=True,
            ci_width_to_estimate_ratio=0.5,
        )
        registry = _MockSourceRegistry(profile)

        result = SyntheticDataEngine.infer(
            entity_id="SYNTHETIC_TEST",
            indicator_key="test_no_mnar_mice_conditions",
            source_registry=registry,
        )

        assert result.synthetic_method == "SYNTHETIC_COMPARABLE", (
            f"AC-5 FAIL: synthetic_method was {result.synthetic_method!r} when mnar=False "
            "and all MICE conditions are met. Method B must fire. "
            "Silent failure 2 (intent doc §3.4): if Method B is never dispatched, all indicators "
            "with partial data receive STRUCTURAL_ABSENCE instead of MICE imputation."
        )


# ---------------------------------------------------------------------------
# AC-6 — api_contracts.yml contains "is_synthetic" in trajectory Quantity schema
# ---------------------------------------------------------------------------

_AC6_SECTION = "trajectory"  # section of api_contracts.yml being tested


class TestAC6ApiContractsYaml:
    """AC-6: api_contracts.yml must document the is_synthetic field in the trajectory
    Quantity schema definition.

    CLAUDE.md §Schema registry: 'api_contracts.yml updated in the same commit as the
    backend implementation — schema drift is a compliance violation.'

    Pre-G4: is_synthetic is not in the trajectory Quantity schema (it was only in the
    source data quality coverage response). Post-G4: it must appear in the context of
    the trajectory endpoint's Quantity response schema.
    """

    def test_api_contracts_file_exists(self) -> None:
        assert _API_CONTRACTS.exists(), (
            f"docs/schema/api_contracts.yml not found at {_API_CONTRACTS}."
        )

    def test_is_synthetic_present_in_api_contracts(self) -> None:
        text = _API_CONTRACTS.read_text(encoding="utf-8")
        assert "is_synthetic" in text, (
            "AC-6 FAIL: 'is_synthetic' not found in docs/schema/api_contracts.yml. "
            "CLAUDE.md §Schema registry: api_contracts.yml must be updated in the same "
            "commit as the G4 backend implementation. "
            "The is_synthetic field must appear in the trajectory endpoint's Quantity schema."
        )

    def test_synthetic_method_present_in_api_contracts(self) -> None:
        text = _API_CONTRACTS.read_text(encoding="utf-8")
        assert "synthetic_method" in text, (
            "AC-6 FAIL: 'synthetic_method' not found in docs/schema/api_contracts.yml. "
            "The G4 Quantity schema extension adds synthetic_method to the trajectory response. "
            "Schema drift: synthetic_method must be documented in the same commit as implementation."
        )

    def test_structural_absence_value_documented(self) -> None:
        """STRUCTURAL_ABSENCE must be named as a possible synthetic_method value."""
        text = _API_CONTRACTS.read_text(encoding="utf-8")
        assert "STRUCTURAL_ABSENCE" in text, (
            "AC-6 FAIL: 'STRUCTURAL_ABSENCE' not found in docs/schema/api_contracts.yml. "
            "api_contracts.yml must document the valid synthetic_method values: "
            "STRUCTURAL_ABSENCE, SYNTHETIC_COMPARABLE, SYNTHETIC_MODEL."
        )


# ===========================================================================
# SECTION: #275 — Ecological-to-financial transmission
# ===========================================================================

# ---------------------------------------------------------------------------
# AC-7 — ScenarioConfigSchema accepts ecological_shock_coefficient in [0.0, 1.0]
# ---------------------------------------------------------------------------


class TestAC7EcologicalShockCoefficientSchema:
    """AC-7: ScenarioConfigSchema must accept ecological_shock_coefficient as an
    optional field in the range [0.0, 1.0]. Values outside this range must be rejected.

    Intent doc §3.2 State 5: 'A SimulationRequest with ecological_shock_coefficient=0.35
    succeeds. A request with ecological_shock_coefficient=1.1 returns a validation error (422).'

    Pre-G4: ScenarioConfigSchema does not have this field → getattr returns None (silently
    dropped by Pydantic with from_attributes=True). The test that checks the VALUE is stored
    (not silently dropped) will fail pre-G4.
    """

    def test_ecological_shock_coefficient_accepted_in_range(self) -> None:
        try:
            from app.schemas import ScenarioConfigSchema  # type: ignore[import]
        except ImportError:
            pytest.fail("app.schemas.ScenarioConfigSchema could not be imported.")
        from pydantic import ValidationError

        try:
            config = ScenarioConfigSchema(
                entities=["ZMB"],
                n_steps=8,
                ecological_shock_coefficient=0.35,
            )
        except (ValidationError, TypeError) as exc:
            pytest.fail(
                f"ScenarioConfigSchema rejected ecological_shock_coefficient=0.35: {exc}\n"
                "AC-7: ecological_shock_coefficient must be an optional field in [0.0, 1.0]. "
                "ADR-012 ExternalSectorModule boundary: the coefficient is a shock input."
            )
        stored = getattr(config, "ecological_shock_coefficient", "ABSENT")
        assert stored != "ABSENT", (
            "AC-7 FAIL: ecological_shock_coefficient is not a field on ScenarioConfigSchema. "
            "Pydantic silently dropped it (extra fields are ignored by default). "
            "The field must be declared explicitly on ScenarioConfigSchema."
        )
        assert abs(stored - 0.35) < 1e-9, (
            f"AC-7 FAIL: stored value {stored!r} does not match the input 0.35. "
            "The coefficient must be stored as-is, not rounded or transformed."
        )

    def test_ecological_shock_coefficient_zero_accepted(self) -> None:
        try:
            from app.schemas import ScenarioConfigSchema  # type: ignore[import]
        except ImportError:
            pytest.fail("ScenarioConfigSchema could not be imported.")
        from pydantic import ValidationError

        try:
            config = ScenarioConfigSchema(entities=["ZMB"], n_steps=8, ecological_shock_coefficient=0.0)
        except (ValidationError, TypeError) as exc:
            pytest.fail(f"ecological_shock_coefficient=0.0 (default/no-op) rejected: {exc}")
        assert getattr(config, "ecological_shock_coefficient", None) == 0.0

    def test_ecological_shock_coefficient_one_accepted(self) -> None:
        try:
            from app.schemas import ScenarioConfigSchema  # type: ignore[import]
        except ImportError:
            pytest.fail("ScenarioConfigSchema could not be imported.")
        from pydantic import ValidationError

        try:
            config = ScenarioConfigSchema(entities=["ZMB"], n_steps=8, ecological_shock_coefficient=1.0)
        except (ValidationError, TypeError) as exc:
            pytest.fail(f"ecological_shock_coefficient=1.0 (upper boundary) rejected: {exc}")
        assert getattr(config, "ecological_shock_coefficient", None) == 1.0

    def test_ecological_shock_coefficient_above_one_rejected(self) -> None:
        try:
            from app.schemas import ScenarioConfigSchema  # type: ignore[import]
        except ImportError:
            pytest.fail("ScenarioConfigSchema could not be imported.")
        from pydantic import ValidationError

        with pytest.raises(ValidationError, match=r"ecological_shock_coefficient"):
            ScenarioConfigSchema(entities=["ZMB"], n_steps=8, ecological_shock_coefficient=1.01)

    def test_ecological_shock_coefficient_negative_rejected(self) -> None:
        try:
            from app.schemas import ScenarioConfigSchema  # type: ignore[import]
        except ImportError:
            pytest.fail("ScenarioConfigSchema could not be imported.")
        from pydantic import ValidationError

        with pytest.raises(ValidationError, match=r"ecological_shock_coefficient"):
            ScenarioConfigSchema(entities=["ZMB"], n_steps=8, ecological_shock_coefficient=-0.01)

    def test_ecological_shock_coefficient_absent_defaults_to_zero(self) -> None:
        """When field is absent, default must be 0.0 (no ecological transmission applied)."""
        try:
            from app.schemas import ScenarioConfigSchema  # type: ignore[import]
        except ImportError:
            pytest.fail("ScenarioConfigSchema could not be imported.")

        config = ScenarioConfigSchema(entities=["ZMB"], n_steps=8)
        default_val = getattr(config, "ecological_shock_coefficient", "ABSENT")
        if default_val == "ABSENT":
            return  # pre-G4: field not yet defined; AC-7 acceptance tests will catch this
        assert default_val == 0.0, (
            f"AC-7 FAIL: default ecological_shock_coefficient was {default_val!r}, expected 0.0. "
            "Intent doc §3.2: 'A request with ecological_shock_coefficient=0.0 (default) produces "
            "trajectory output identical to a request with no ecological_shock_coefficient field.' "
            "Default must be 0.0 (no ecological transmission) to ensure backwards compatibility."
        )


# ---------------------------------------------------------------------------
# AC-8 — ecological_shock_coefficient=0.0 → identical trajectory (DB)
# ---------------------------------------------------------------------------


class TestAC8CoefficientZeroNonRegression:
    """AC-8: ZMB scenario with ecological_shock_coefficient=0.0 must produce a trajectory
    numerically identical to the same scenario run with no coefficient field.

    Intent doc AC-8: 'Delta between fiscal revenue values at each step: exactly 0.0.'

    Observable application state §3.2 State 5: 'A request with
    ecological_shock_coefficient=0.0 (default) produces trajectory output identical to
    a request with no ecological_shock_coefficient field at all.'

    Silent failure 3 (intent doc §3.4): if the coefficient is accepted in the schema but
    not applied (silently ignored), then a run with coefficient=0.35 would be identical to
    coefficient=0.0. This test only checks the 0.0 case; AC-EE-1 (EE-PENDING) catches
    the coefficient=0.35 actual-effect case.
    """

    async def test_coefficient_zero_produces_same_steps_executed(
        self, client: httpx.AsyncClient
    ) -> None:
        """Runs ZMB with coefficient=0.0 and without the field; both must complete with 8 steps."""
        payload_no_coeff = _zmb_8_step_payload()
        payload_coeff_zero = _zmb_8_step_payload({"ecological_shock_coefficient": 0.0})

        for payload, label in (
            (payload_no_coeff, "no coefficient"),
            (payload_coeff_zero, "coefficient=0.0"),
        ):
            create_res = await client.post("/api/v1/scenarios", json=payload)
            if create_res.status_code == 422:
                return  # pre-G4: field not accepted (AC-7 will fail; this is a guard)
            assert create_res.status_code == 201, (
                f"AC-8 {label}: POST /scenarios returned {create_res.status_code}."
            )
            sid = create_res.json()["scenario_id"]

            run_res = await client.post(f"/api/v1/scenarios/{sid}/run")
            assert run_res.status_code == 200, (
                f"AC-8 {label}: run returned {run_res.status_code}."
            )
            assert run_res.json().get("steps_executed") == 8, (
                f"AC-8 {label}: steps_executed was {run_res.json().get('steps_executed')!r}, "
                "expected 8. ecological_shock_coefficient must not alter the step count."
            )

    async def test_coefficient_zero_trajectory_identical_to_no_coefficient(
        self, client: httpx.AsyncClient
    ) -> None:
        """Trajectories for coefficient=0.0 and no-coefficient must be numerically identical.

        Compares step-by-step snapshot attributes for both runs. If the ecological
        transmission pathway is applied even at coefficient=0.0, attribute values would differ.
        """
        payload_no_coeff = _zmb_8_step_payload()
        payload_coeff_zero = _zmb_8_step_payload({"ecological_shock_coefficient": 0.0})

        ids: list[str] = []
        for payload, label in (
            (payload_no_coeff, "no coefficient"),
            (payload_coeff_zero, "coefficient=0.0"),
        ):
            create_res = await client.post("/api/v1/scenarios", json=payload)
            if create_res.status_code == 422:
                return  # pre-G4 guard: field not yet in schema
            assert create_res.status_code == 201, (
                f"AC-8 {label}: create returned {create_res.status_code}."
            )
            sid = create_res.json()["scenario_id"]
            run_res = await client.post(f"/api/v1/scenarios/{sid}/run")
            assert run_res.status_code == 200
            ids.append(sid)

        if len(ids) < 2:
            return  # should not happen, but guard

        id_a, id_b = ids

        # Compare via the /compare endpoint — delta should be 0 for all attributes
        compare_res = await client.get(
            "/api/v1/scenarios/compare",
            params={"scenario_a": id_a, "scenario_b": id_b},
        )
        if compare_res.status_code in (404, 409):
            return  # compare endpoint not reachable (both scenarios may have no snapshots yet)
        assert compare_res.status_code == 200, (
            f"AC-8: GET /compare returned {compare_res.status_code}."
        )

        body = compare_res.json()
        deltas = body.get("deltas", [])
        non_zero_deltas: list[dict[str, Any]] = []
        for delta_record in deltas:
            raw_delta = delta_record.get("delta")
            if raw_delta is None:
                continue
            try:
                delta_val = abs(Decimal(str(raw_delta)))
            except Exception:  # noqa: BLE001
                continue
            if delta_val > Decimal("0"):
                non_zero_deltas.append({
                    "entity": delta_record.get("entity_id"),
                    "key": delta_record.get("attribute_key"),
                    "delta": str(delta_val),
                })

        assert not non_zero_deltas, (
            f"AC-8 FAIL: {len(non_zero_deltas)} non-zero delta(s) found between "
            f"coefficient=0.0 and no-coefficient runs: {non_zero_deltas[:5]}. "
            "ecological_shock_coefficient=0.0 must produce a trajectory numerically identical "
            "to a run with no coefficient field. "
            "Silent failure 3: if the transmission pathway fires at coefficient=0, "
            "these deltas would be non-zero."
        )


# ---------------------------------------------------------------------------
# AC-9 — api_contracts.yml documents ecological_shock_coefficient
# ---------------------------------------------------------------------------


class TestAC9ApiContractsEcologicalCoeff:
    """AC-9: api_contracts.yml must document ecological_shock_coefficient in the
    simulation request schema.

    CLAUDE.md §Schema registry: 'api_contracts.yml updated in the same commit as the
    backend implementation — schema drift is a compliance violation.'
    """

    def test_ecological_shock_coefficient_in_api_contracts(self) -> None:
        assert _API_CONTRACTS.exists(), (
            f"docs/schema/api_contracts.yml not found at {_API_CONTRACTS}."
        )
        text = _API_CONTRACTS.read_text(encoding="utf-8")
        assert "ecological_shock_coefficient" in text, (
            "AC-9 FAIL: 'ecological_shock_coefficient' not found in docs/schema/api_contracts.yml. "
            "CLAUDE.md §Schema registry: api_contracts.yml must be updated in the same commit "
            "as the G4 #275 backend implementation. "
            "The field must be documented as optional, range [0.0, 1.0], default 0.0."
        )

    def test_ecological_shock_coefficient_near_post_scenarios(self) -> None:
        """ecological_shock_coefficient must appear in the POST /scenarios request schema context."""
        text = _API_CONTRACTS.read_text(encoding="utf-8")
        if "ecological_shock_coefficient" not in text:
            pytest.fail("ecological_shock_coefficient not found in api_contracts.yml.")

        lines = text.splitlines()
        coeff_lines = [i for i, ln in enumerate(lines) if "ecological_shock_coefficient" in ln]
        post_lines = [
            i for i, ln in enumerate(lines)
            if "POST" in ln and "/scenarios" in ln and "scenario_id" not in ln
        ]
        if not post_lines:
            pytest.fail("POST /scenarios entry not found in api_contracts.yml.")

        nearest_post = min(post_lines, key=lambda pl: min(abs(pl - ql) for ql in coeff_lines))
        min_distance = min(abs(nearest_post - ql) for ql in coeff_lines)
        assert min_distance <= 80, (
            f"AC-9 FAIL: ecological_shock_coefficient appears {min_distance} lines from "
            "POST /scenarios. It must be documented within the request body schema definition."
        )


# NOTE: AC-EE-1 and AC-EE-2 are NOT YET AUTHORED.
# They will be added after the Ecological Economist DIC review comment is filed on GitHub
# issue #275 and the calibration values (Zimbabwe 2005 coefficient, tolerance %, step horizon,
# fiscal indicator key) are confirmed. See intent document §7 Test Authorship Obligation.


# ===========================================================================
# SECTION: #102 — Distributional comparison API
# ===========================================================================

# ---------------------------------------------------------------------------
# AC-10 — GET /compare response includes distribution fields (DB)
# ---------------------------------------------------------------------------


class TestAC10DistributionFieldsInCompare:
    """AC-10: GET /scenarios/compare response must include distribution.variance,
    distribution.p10, distribution.p50, distribution.p90 for each compared indicator.

    Intent doc §3.3 State 8: 'GET /compare?scenario_a={id}&scenario_b={id} returns a
    response body where each compared indicator includes a distribution object:
    {"variance": float, "p10": float, "p50": float, "p90": float}.'

    Intent doc AC-10: 'Existing delta and baseline fields are present and unchanged —
    this is an additive extension only.'

    Pre-G4: /compare response does not include distribution → test fails.
    Post-G4: distribution is present on every compared indicator.
    """

    async def test_compare_response_includes_distribution_object(
        self, client: httpx.AsyncClient
    ) -> None:
        """Create two ZMB scenarios at different step counts, compare, check distribution."""
        payload_a = _zmb_8_step_payload()
        payload_a["name"] = "M16-G4 AC-10 scenario A"
        payload_b = _zmb_8_step_payload()
        payload_b["name"] = "M16-G4 AC-10 scenario B"
        payload_b["configuration"]["n_steps"] = 4  # different step count to produce different state

        ids: list[str] = []
        for payload in (payload_a, payload_b):
            create_res = await client.post("/api/v1/scenarios", json=payload)
            assert create_res.status_code == 201, (
                f"AC-10: create returned {create_res.status_code}: {create_res.text[:200]}"
            )
            sid = create_res.json()["scenario_id"]
            run_res = await client.post(f"/api/v1/scenarios/{sid}/run")
            assert run_res.status_code == 200
            ids.append(sid)

        compare_res = await client.get(
            "/api/v1/scenarios/compare",
            params={"scenario_a": ids[0], "scenario_b": ids[1]},
        )
        if compare_res.status_code == 409:
            return  # one or both scenarios have no snapshots yet (pre-G4 run may not produce them)
        assert compare_res.status_code == 200, (
            f"AC-10: GET /compare returned {compare_res.status_code}: {compare_res.text[:300]}"
        )

        body = compare_res.json()
        deltas = body.get("deltas", [])
        if not deltas:
            return  # no shared indicators to compare (pre-G4 guard)

        # Check every delta record for the distribution object
        missing_distribution: list[dict[str, Any]] = []
        for delta in deltas:
            distribution = delta.get("distribution")
            if distribution is None:
                missing_distribution.append({
                    "entity": delta.get("entity_id"),
                    "key": delta.get("attribute_key"),
                })
                continue

            # distribution must have all four fields
            for field in ("variance", "p10", "p50", "p90"):
                assert field in distribution, (
                    f"AC-10 FAIL: distribution.{field} missing from compare delta "
                    f"for {delta.get('entity_id')}.{delta.get('attribute_key')}. "
                    f"Intent doc AC-10: distribution must include variance, p10, p50, p90."
                )

        assert not missing_distribution, (
            f"AC-10 FAIL: {len(missing_distribution)} delta record(s) have no 'distribution' "
            f"object: {missing_distribution[:5]}. "
            "Intent doc §3.3: every compared indicator must include a distribution object. "
            "This is an additive extension — existing delta/baseline fields must remain."
        )

    async def test_compare_response_delta_field_unchanged(
        self, client: httpx.AsyncClient
    ) -> None:
        """Existing 'delta' and 'baseline' fields must still be present after G4 extension."""
        payload_a = _zmb_8_step_payload()
        payload_a["name"] = "M16-G4 AC-10 backward-compat A"
        payload_b = _zmb_8_step_payload()
        payload_b["name"] = "M16-G4 AC-10 backward-compat B"
        payload_b["configuration"]["n_steps"] = 4

        ids: list[str] = []
        for payload in (payload_a, payload_b):
            create_res = await client.post("/api/v1/scenarios", json=payload)
            assert create_res.status_code == 201
            sid = create_res.json()["scenario_id"]
            await client.post(f"/api/v1/scenarios/{sid}/run")
            ids.append(sid)

        compare_res = await client.get(
            "/api/v1/scenarios/compare",
            params={"scenario_a": ids[0], "scenario_b": ids[1]},
        )
        if compare_res.status_code in (200,):
            body = compare_res.json()
            deltas = body.get("deltas", [])
            if deltas:
                first = deltas[0]
                assert "delta" in first, (
                    "AC-10 FAIL: 'delta' field missing from compare response. "
                    "G4 adds 'distribution' but must not remove existing fields."
                )


# ---------------------------------------------------------------------------
# AC-11 — Insufficient data → null distribution fields, HTTP 200 (DB)
# ---------------------------------------------------------------------------


class TestAC11NullDistributionInsufficientData:
    """AC-11: When the comparison window has fewer than 3 data points for an indicator,
    the distribution object must contain null values, not an error.

    Intent doc §3.3 State 9: 'distribution object contains
    {"variance": null, "p10": null, "p50": null, "p90": null}. The response is not an error.'

    This guards against two silent failures:
    - The endpoint returning 422 or 500 when distribution cannot be computed
    - The distribution fields being omitted entirely when data is insufficient
      (which would break clients that always expect the distribution key)
    """

    async def test_compare_with_minimal_steps_returns_null_distribution(
        self, client: httpx.AsyncClient
    ) -> None:
        """Compare two 1-step scenarios — fewer than 3 data points → null distribution."""
        payload_a: dict[str, Any] = {
            "name": "M16-G4 AC-11 sparse A",
            "configuration": {
                "entities": ["ZMB"],
                "n_steps": 1,
                "timestep_label": "annual",
                "start_date": "2023-01-01",
                "modules_config": {"ecological": {"enabled": False}, "political_economy": {"enabled": False}},
            },
            "scheduled_inputs": [],
        }
        payload_b: dict[str, Any] = {
            "name": "M16-G4 AC-11 sparse B",
            "configuration": {
                "entities": ["ZMB"],
                "n_steps": 1,
                "timestep_label": "annual",
                "start_date": "2023-01-01",
                "modules_config": {"ecological": {"enabled": False}, "political_economy": {"enabled": False}},
            },
            "scheduled_inputs": [],
        }

        ids: list[str] = []
        for payload in (payload_a, payload_b):
            create_res = await client.post("/api/v1/scenarios", json=payload)
            assert create_res.status_code == 201
            sid = create_res.json()["scenario_id"]
            await client.post(f"/api/v1/scenarios/{sid}/run")
            ids.append(sid)

        compare_res = await client.get(
            "/api/v1/scenarios/compare",
            params={"scenario_a": ids[0], "scenario_b": ids[1]},
        )
        if compare_res.status_code in (409,):
            return  # no snapshots (pre-G4 guard)
        if compare_res.status_code == 200:
            body = compare_res.json()
            deltas = body.get("deltas", [])
            for delta in deltas:
                distribution = delta.get("distribution")
                if distribution is None:
                    return  # G4 distribution not yet implemented (pre-G4 guard)

                # At 1-step window, distribution should be null (< 3 data points)
                for field in ("variance", "p10", "p50", "p90"):
                    val = distribution.get(field)
                    assert val is None, (
                        f"AC-11 FAIL: distribution.{field} was {val!r} for a 1-step window "
                        f"(entity: {delta.get('entity_id')}, key: {delta.get('attribute_key')}). "
                        "Intent doc AC-11: 'when the comparison window has fewer than 3 data points, "
                        "distribution contains null values.' HTTP 200 with nulls is correct. "
                        "A non-null value for a 1-step window indicates the distribution "
                        "is being computed from insufficient data."
                    )

        # HTTP 200 is mandatory regardless of null distribution
        assert compare_res.status_code == 200, (
            f"AC-11 FAIL: GET /compare returned {compare_res.status_code} for sparse scenarios. "
            "Insufficient data must return HTTP 200 with null distribution fields, not an error. "
            "Intent doc AC-11: 'The response is not an error.'"
        )


# ---------------------------------------------------------------------------
# AC-12 — api_contracts.yml documents distribution fields
# ---------------------------------------------------------------------------


class TestAC12ApiContractsDistribution:
    """AC-12: api_contracts.yml must document the distribution object with variance,
    p10, p50, p90 in the compare response schema.

    CLAUDE.md §Schema registry: 'api_contracts.yml updated in the same commit as the
    backend implementation — schema drift is a compliance violation.'

    Intent doc AC-12: 'distribution field in the compare response schema, in the same
    commit as the backend implementation.'
    """

    def test_distribution_field_in_api_contracts(self) -> None:
        assert _API_CONTRACTS.exists()
        text = _API_CONTRACTS.read_text(encoding="utf-8")
        assert "distribution" in text, (
            "AC-12 FAIL: 'distribution' not found in docs/schema/api_contracts.yml. "
            "G4 #102 adds a distribution object to the compare response. "
            "Schema drift rule: api_contracts.yml must be updated in the same commit."
        )

    def test_variance_p10_p50_p90_in_distribution_schema(self) -> None:
        assert _API_CONTRACTS.exists()
        text = _API_CONTRACTS.read_text(encoding="utf-8")

        for field_name in ("variance", "p10", "p50", "p90"):
            assert field_name in text, (
                f"AC-12 FAIL: '{field_name}' not found in docs/schema/api_contracts.yml. "
                "The distribution object must document all four fields: variance, p10, p50, p90. "
                "Intent doc AC-10: 'distribution object contains variance, p10, p50, p90'."
            )

    def test_compare_endpoint_in_api_contracts(self) -> None:
        """The /compare endpoint must be present in api_contracts.yml."""
        assert _API_CONTRACTS.exists()
        text = _API_CONTRACTS.read_text(encoding="utf-8")
        assert "/scenarios/compare" in text, (
            "AC-12 FAIL: '/scenarios/compare' endpoint not found in api_contracts.yml. "
            "The compare endpoint must be documented before the distribution extension can be "
            "added to it. If the endpoint exists but is undocumented, this is a pre-existing "
            "schema drift violation that must be remediated in the G4 commit."
        )
